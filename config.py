from pathlib import Path
from typing import Optional
import os
import subprocess
import shlex

type Project = dict[str, str | Path]


#NOTE:Required Parameters (Must be filled)
PROJECTS_FILE: Path = Path(__file__).parent / "projects.json"
PROJ_OPEN_COMMAND: str = "alacritty --title \"{}\" --working-directory \"{}\" "
DEFAULT_PATH: Path = Path(os.path.join(os.path.expanduser("~"), "Projects"))

#NOTE: Optional parameters (Can be None)
ROFI_THEME: Optional[str | Path] = None
GIT_INIT_COMMAND: Optional[list[str]] = ["gh repo create \"{}\" --private"]
PYTHON_INIT_COMMAND: Optional[list[str]] = ["uv init", "uv venv", "bash -c \"source .venv/bin/activate\""]
RUST_INIT_COMMAND: Optional[list[str]] = ["cargo init"]

GIT_DELETE_COMMAND: Optional[list[str]] = ["gh repo delete \"{}\" --yes"]


def init_git(proj: Project):
    if GIT_INIT_COMMAND is not None:
        for cmd in GIT_INIT_COMMAND:
            subprocess.run(
                shlex.split(cmd.format(proj['label'].replace(' ', '-'))),
                cwd=proj['path']
            )

def init_python(proj: Project):
    if PYTHON_INIT_COMMAND is not None:
        for cmd in PYTHON_INIT_COMMAND:
            subprocess.run(
                shlex.split(cmd),
                cwd=proj['path']
            )

def init_rust(proj: Project):
    if RUST_INIT_COMMAND is not None:
        for cmd in RUST_INIT_COMMAND:
            subprocess.run(
                shlex.split(cmd),
                cwd=proj['path']
            )

def del_git(proj: Project):
    if GIT_DELETE_COMMAND is not None:
        for cmd in GIT_DELETE_COMMAND:
            subprocess.run(
                shlex.split(cmd.format(proj['label'].replace(' ', '-'))),
                cwd=proj['path']
            )

#INFO: Add other parameters and their implementations below:


#NOTE: Init implementations

ADDITIONAL_IMPLEMENTATIONS: dict[str, list] = {
    # (Name, Function, optional)
    'open': [],
    'create': [("Initialize Python Environment", init_python, 1), 
               ("Initialize Rust Environment", init_rust, 1),
               ("Initialize Github repo", init_git, 1)],
    'import': [],
    'remove': [("Delete Github Repo", del_git, 0)]

}

