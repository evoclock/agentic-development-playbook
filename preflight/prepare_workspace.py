from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = Path(__file__).resolve().parent
GENERATED_MODEL_STATE = (
    "models.raw.jsonl",
    "models.runtime.json",
    "models.assignments.json",
)


def copy_fixture(target: Path) -> None:
    if target.exists():
        raise FileExistsError(f"workspace already exists: {target}")
    target.mkdir(parents=True)
    fixture = target / "preflight"
    shutil.copytree(
        FIXTURE_ROOT,
        fixture,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    for name in ("README.md", "AGENTS.md", "TASKS.md", ".gitignore", "src"):
        source = fixture / name
        destination = target / name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    github = target / ".github"
    shutil.copytree(
        REPO_ROOT / ".github" / "skills",
        github / "skills",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", *GENERATED_MODEL_STATE),
    )
    shutil.copytree(REPO_ROOT / ".github" / "hooks", github / "hooks")
    shutil.copy2(
        fixture / ".github" / "copilot-instructions.md",
        github / "copilot-instructions.md",
    )
    runbooks = target / "runbooks"
    runbooks.mkdir()
    shutil.copy2(
        REPO_ROOT / "runbooks" / "10-skill-preflight.md",
        runbooks / "10-skill-preflight.md",
    )


def initialize_git(target: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=target, check=True)
    subprocess.run(
        ["git", "config", "user.email", "preflight@example.invalid"],
        cwd=target,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "preflight fixture"],
        cwd=target,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=target, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "initialize disposable preflight"],
        cwd=target,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="exact empty directory to create; defaults to a temporary directory",
    )
    args = parser.parse_args()
    if args.output:
        target = args.output.expanduser().resolve()
    else:
        parent = Path(tempfile.mkdtemp(prefix="copilot-skill-preflight-"))
        target = parent / "workspace"
    copy_fixture(target)
    initialize_git(target)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
