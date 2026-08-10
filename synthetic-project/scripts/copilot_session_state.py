"""Emit a read-only Copilot session-start summary for this repository."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TASK_PATH = "synthetic-project/DEMO-TICKET.md"
TEST_COMMAND = "python3 -m unittest discover -s synthetic-project/tests -v"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                            text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def review_repo(repo: Path = REPO_ROOT) -> dict[str, Any]:
    """Read branch and working-tree state without changing the repository."""
    status_lines = [line for line in _git(repo, "status", "--short").splitlines() if line]
    return {
        "branch": _git(repo, "branch", "--show-current") or "(detached)",
        "head": _git(repo, "rev-parse", "--short", "HEAD"),
        "status": status_lines,
        "diff_stat": _git(repo, "diff", "--stat") or "(clean)",
    }


def render_context(state: dict[str, Any], payload: dict[str, Any] | None = None) -> str:
    """Render short context for a new or resumed Copilot session."""
    source = (payload or {}).get("source", "unknown")
    lines = [
        "SESSION STATE (read-only)",
        f"Session source: {source}",
        f"Branch: {state['branch']} @ {state['head']}",
        f"Working tree: {'clean' if not state['status'] else 'review required'}",
        f"Demo task: {TASK_PATH}",
        f"Test command: {TEST_COMMAND}",
        "Next action: inspect the task, state a bounded plan, then run focused checks.",
    ]
    if state["status"]:
        lines.append("Changed paths:")
        lines.extend(f"  - {line}" for line in state["status"][:12])
    lines.append(f"Diff summary: {state['diff_stat']}")
    return "\n".join(lines)


def hook_output(payload: dict[str, Any] | None = None, *, repo: Path = REPO_ROOT) -> dict[str, str]:
    """Return the native Copilot sessionStart output shape."""
    try:
        state = review_repo(repo)
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
