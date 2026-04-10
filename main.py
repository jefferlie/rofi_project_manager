from rofi import Rofi
from pathlib import Path
import subprocess
import json
import shlex
import os

PROJECTS_FILE = Path(__file__).parent / "projects.json"
PROJ_OPEN_COMMAND = "alacritty --title \"{}\" --working-directory \"{}\""
DEFAULT_PATH = Path("/home/laplas14/Projects/")

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
        json.dump(projects, f)

def open_project(proj: dict[str, str] | None) -> None:
    in_editor, q = r.select("Open Project", ('In terminal', 'In editor'))

    if proj is None:
        return

    subprocess.Popen(shlex.split((PROJ_OPEN_COMMAND + '-e nvim .' * (in_editor - q)).format(proj['label'], proj['path'])))

def _rofi_choose_name() -> str | None:
    proj_labels = [proj['label'] for proj in projects]

    proj_name: str | None = r.text_entry("Project Name: ")

    while (proj_name is not None and proj_name in proj_labels):
        proj_name: str | None = r.text_entry("Project Name: ", "Please choose a different name")
    
    return proj_name

def _rofi_choose_

def _rofi_choose_path(path: Path = DEFAULT_PATH) -> Path | None:
    while (not (idx := r.select("Select dir", \
            (a := ['Select', '..'] + [fpath for fpath in os.listdir(path) if os.path.isdir(path / fpath)])))[1]):

        if not idx[0]:
            return path

        path = path / a[idx[0]]

    return None

def _rofi_create_dir(dir_name: str) -> None:
    ...

def rofi_proj_manager() -> dict[str, str] | None:
    match (r.select("Select option", ('Select Project', 'Add Project', 'Remove Project', 'Make Backup'))[0]):
        case 0:
            projects_str = [f"{proj['label']:>10} | {proj['path']:<10}" for proj in projects]
            idx, q = r.select("Choose Project", projects_str)

            if q:
                return

            update_proj_list(proj=projects[idx])
            return projects[idx]

        case 1:
            label = _rofi_choose_name()
            if label is None:
                return

            match (r.select("Select option", ('Create new project', 'Import exsiting project'))[0]):
                case 0:
                    path = _rofi_choose_path()


                case 1:
                    path = _rofi_choose_path()

                case _:
                    return None

            confirm, q = r.select(f"Do you confirm your changes?", ('Yes', 'No'))

            return None

        case _:
            return None

def main():
    load_proj_list()
    print(rofi_proj_manager())

if __name__ == "__main__":
    main()
