"""Emit a read-only Copilot session-start summary for this repository."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TASK_PATH = "TASK.md"
TASK_REGISTER_PATH = "TASKS.md"
HANDOVER_PATH = "HANDOVER.md"
TEST_COMMAND = "python3 -m unittest discover -s .github/skills/model-routing/tests -v"


def _resolve_repo(payload: dict[str, Any] | None = None) -> Path:
    candidates: list[Path] = []
    cwd = (payload or {}).get("cwd")
    if isinstance(cwd, str) and cwd:
        candidates.append(Path(cwd).resolve())
    else:
        candidates.append(Path(".").resolve())
    candidates.append(REPO_ROOT)
    for base in candidates:
        probe = subprocess.run(["git", "-C", str(base), "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, check=False)
        if probe.returncode == 0 and probe.stdout.strip():
            return Path(probe.stdout.strip())
    return base


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                            text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def _document_state(repo: Path, relative_path: str) -> dict[str, str]:
    path = repo / relative_path
    if not path.is_file():
        return {"path": relative_path, "status": "missing"}
    marker = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        lowered = line.lower()
        if any(token in lowered for token in
               ("`in progress`", "`ready for review`", "`blocked`", "`complete`")):
            marker = line.strip()
            break
        if lowered.startswith("status:"):
            marker = line.strip()
            break
    return {"path": relative_path, "status": "present", "marker": marker}


def review_repo(repo: Path) -> dict[str, Any]:
    """Read branch, task, handover, and working-tree state without writing."""
    status_lines = [line for line in _git(repo, "status", "--short").splitlines() if line]
    return {
        "branch": _git(repo, "branch", "--show-current") or "(detached)",
        "head": _git(repo, "rev-parse", "--short", "HEAD"),
        "status": status_lines,
        "diff_stat": _git(repo, "diff", "--stat") or "(clean)",
        "task_contract": _document_state(repo, TASK_PATH),
        "task_register": _document_state(repo, TASK_REGISTER_PATH),
        "handover": _document_state(repo, HANDOVER_PATH),
    }


def render_context(state: dict[str, Any], payload: dict[str, Any] | None = None) -> str:
    """Render short context for a new or resumed Copilot session."""
    source = (payload or {}).get("source", "unknown")
    lines = [
        "SESSION STATE (read-only)",
        f"Session source: {source}",
        f"Branch: {state['branch']} @ {state['head']}",
        f"Working tree: {'clean' if not state['status'] else 'review required'}",
        f"Task source: {TASK_PATH}",
        f"Task contract: {state['task_contract']['status']} ({TASK_PATH})",
        f"Task register: {state['task_register']['status']} ({TASK_REGISTER_PATH})",
        f"Handover: {state['handover']['status']} ({HANDOVER_PATH})",
        "Receipt sequence: /task-list-update then /handover at a subtask stop.",
        f"Test command: {TEST_COMMAND}",
        "Next action: inspect the task, state a bounded plan, then run focused checks.",
    ]
    if state["status"]:
        lines.append("Changed paths:")
        lines.extend(f"  - {line}" for line in state["status"][:12])
    if state["task_register"].get("marker"):
        lines.append(f"Task register marker: {state['task_register']['marker']}")
    if state["handover"].get("marker"):
        lines.append(f"Handover marker: {state['handover']['marker']}")
    lines.append(f"Diff summary: {state['diff_stat']}")
    return "\n".join(lines)


def hook_output(payload: dict[str, Any] | None = None, *, repo: Path | None = None) -> dict[str, str]:
    """Return the native Copilot sessionStart output shape."""
    try:
        state = review_repo(repo or _resolve_repo(payload))
        return {"additionalContext": render_context(state, payload)}
    except (OSError, RuntimeError, ValueError) as exc:
        return {"additionalContext": f"SESSION STATE REVIEW ERROR: {exc}. Review the repository manually."}


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            payload = {}
    except json.JSONDecodeError:
        payload = {}
    print(json.dumps(hook_output(payload), separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
