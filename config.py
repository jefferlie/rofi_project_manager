from pathlib import Path
import subprocess
import shlex

#NOTE:Required Parameters (Must be filled)
PROJECTS_FILE: Path = Path(__file__).parent / "projects.json"
PROJ_OPEN_COMMAND: str = "alacritty --title \"{}\" --working-directory \"{}\" "
DEFAULT_PATH: Path = Path("/home/laplas14/Projects/")

#NOTE: Optional parameters (Can be None)
GIT_INIT_COMMAND: str | None = "cd \"{}\" && git init"
PYTHON_INIT_COMMAND: list[str] | None = ["uv init", "uv venv", "bash -c \"source .venv/bin/activate\""]
RUST_INIT_COMMAND: str | None = "cd \"{}\" && cargo init"


def init_git(proj: dict[str, str | Path]):
    if GIT_INIT_COMMAND is not None:
        for cmd in GIT_INIT_COMMAND:
            subprocess.Popen(
                shlex.split(cmd),
                cwd=proj['path']
            )

def init_python(proj: dict[str, str | Path]):
    if PYTHON_INIT_COMMAND is not None:
        for cmd in PYTHON_INIT_COMMAND:
            subprocess.Popen(
                shlex.split(cmd),
                cwd=proj['path']
            )

def init_rust(proj: dict[str, str | Path]):
    if RUST_INIT_COMMAND is not None:
        for cmd in RUST_INIT_COMMAND:
            subprocess.Popen(
                shlex.split(cmd),
                cwd=proj['path']
            )

#INFO: Add other parameters and their implementations below:


#NOTE: Init implementations

ADDITIONAL_IMPLEMENTATIONS: dict[str, list] = {
    # (Name, Function, optional)
    'open': [],
    'create': [("Initialize Github repo", init_git, 1), 
               ("Initialize Python Environment", init_python, 1), 
               ("Initialize Rust Environment", init_rust, 1)],
    'import': [],
}

