from rofi import Rofi
from pathlib import Path
import subprocess
import shlex
import shutil
import json
import os

from config import *

projects: list[dict[str, str]] = []
r = Rofi()


def load_proj_list() -> None:
    global projects

    try:
        with open(PROJECTS_FILE) as f:
            projects = json.load(f)

    except Exception as ex:
        print(ex)
        raise Exception


def update_proj_list(proj: dict[str, str], remove: bool = False) -> None:
    if proj in projects:
        projects.remove(proj)

    if not remove:
        projects.insert(0, proj)

    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=4)


def open_project(proj: dict[str, str] | None) -> None:
    if proj is None:
        return

    in_editor, q = r.select("Open Project", ('In terminal', 'In editor'))
    if q:
        return None

    subprocess.Popen(shlex.split(
        (
            PROJ_OPEN_COMMAND + '--command nvim .' * (in_editor - q)
        ).format(proj['label'], proj['path'])
    ))


def _validate_proj(proj: dict[str, str | Path]) -> dict[str, str]:
    return {'label': str(proj['label']), 'path': str(proj['path'])}


def _create_dir(path: Path) -> bool:
    try:
        os.mkdir(path=path)
        return True

    except FileExistsError as ex:
        raise ex

    except Exception as ex:
        raise ex

def _remove_dir(path: Path) -> bool:
    try:
        shutil.rmtree(path=path)
        return True

    except Exception as ex:
        raise ex


def _rofi_choose_name() -> str | None:
    proj_labels = [proj['label'] for proj in projects]

    proj_name: str | None = r.text_entry("Project Name")

    while (proj_name is not None and proj_name in proj_labels):
        proj_name: str | None = r.text_entry("Project Name",
                                             "Please choose a different name")

    return proj_name


def _rofi_choose_path(path: Path = DEFAULT_PATH) -> Path | None:
    while (not (idx := r.select(
                "Select dir",
                (a := ['󰉓 Select', '\t󰉙 ..'] +
                      [f"\t󰉒 {fpath}"
                       for fpath in os.listdir(path)
                       if (os.path.isdir(path / fpath) and not fpath.startswith('.'))]))
                )[1]):

        match idx[0]:
            case 0:
                print(path)
                return path

            case 1:
                path = path.parent

            case _:
                path = path / a[idx[0]][3:]

    return None


def _rofi_create_project(project: dict[str, Path]) -> str | None:
    dir_name = r.text_entry("󰉗 Directory name")
    if not dir_name:
        return None

    while dir_name in [dir_ for dir_ in os.listdir(project['path'])
                       if (os.path.isdir(project['path'] / dir_) and not dir_.startswith('.'))]:
        dir_name = r.text_entry("󰉗 Directory name", "A folder with that name already exists! Choose a different one")
        if not dir_name:
            return None


    if not _rofi_confirm():
        return None

    _create_dir(path=project['path'] / dir_name)

    project['path'] = project['path'] / dir_name

    for name, impl, optional in ADDITIONAL_IMPLEMENTATIONS['create']:
        if not optional:
            impl(project)

        elif optional and _rofi_skip_impl(name):
            impl(project)

    return dir_name


def _rofi_confirm() -> bool:
    confirm, q = r.select(f"Do you confirm your changes?", ('Yes', 'No'))

    return not confirm and (q != -1)

def _rofi_skip_impl(name: str) -> bool:
    skip, q = r.select(f"Do you wanna apply this implementation", ('Apply', 'Skip'), name)

    print(not skip and (q != -1))
    return not skip and (q != -1)


def rofi_proj_manager() -> dict[str, str] | None:
    match (r.select("Select option",
           (
               'Select Project',
               'Add Project',
               'Remove Project',
               'Make Backup'
            )
            )[0]):

        case x if x in (0, 2):
            projects_str = [f"{proj['label']:>10} | {proj['path']:<10}"
                            for proj in projects]
            idx, q = r.select("Choose Project", projects_str)

            if q:
                return None

            if x:
                if not _rofi_confirm():
                    return None

                _remove_dir(Path(projects[idx]['path']))

            update_proj_list(proj=projects[idx], remove=bool(x))

            return projects[idx] if not x else None

        case 1:
            label = _rofi_choose_name()
            if label is None:
                return

            match (r.select("Select option",
                            ('Create new project',
                             'Import exsiting project'))[0]):
                case x if x in (0, 1):
                    path = _rofi_choose_path()
                    if path is None:
                        return None

                    project = {'label': label, 'path': path}

                    if not x:
                        dir_name = _rofi_create_project(project=project)
                        if dir_name is None:
                            return None

                    else:
                        if not _rofi_confirm():
                            return None

                    update_proj_list(proj=_validate_proj(proj=project))

                    return _validate_proj(project)

                case _:
                    return None

        case 3:
            r.error("\n\n\tThis method is still in development... \n\t\tSorry :(\n\n")

        case _:
            return None


def main():
    load_proj_list()
    open_project(rofi_proj_manager())


if __name__ == "__main__":
    main()
