"""Deny selected risky Copilot CLI tool calls for the public demo."""
from __future__ import annotations

import json
import re
import sys
from typing import Any

DENY_RULES = (
    (re.compile(r"\bgit\s+(?:push|commit|merge|rebase)\b", re.I),
     "Repository publication or history changes require human review."),
    (re.compile(r"\bgit\s+(?:reset\s+--hard|clean\s+-[fdx]+)\b", re.I),
     "Destructive Git operations require human review."),
    (re.compile(r"\b(?:rm|rmdir)\b[^\n]*(?:-r|-f|--recursive|--force)", re.I),
     "Recursive or forced deletion requires human review."),
    (re.compile(r"\bsudo\b", re.I),
     "Elevated commands are outside the demo scope."),
    (re.compile(r"\b(?:pip|pip3|npm|pnpm|yarn|uv)\s+(?:install|add|update|remove)\b", re.I),
     "Package changes require a separately reviewed action."),
    (re.compile(r"\b(?:python|python3)\s+-m\s+pip\s+install\b", re.I),
     "Package changes require a separately reviewed action."),
    (re.compile(r"\b(?:winget|brew)\s+(?:install|upgrade|uninstall)\b", re.I),
     "System package changes require a separately reviewed action."),
)


def _command_from_args(tool_args: Any) -> str:
    if isinstance(tool_args, str):
        try:
            return _command_from_args(json.loads(tool_args))
        except json.JSONDecodeError:
            return tool_args
    if isinstance(tool_args, dict):
        for key in ("command", "cmd", "script"):
            if isinstance(tool_args.get(key), str):
                return tool_args[key]
        return json.dumps(tool_args, sort_keys=True)
    return ""


def decision_for_payload(payload: Any) -> dict[str, str]:
    """Return {} for normal permission flow or a deny decision."""
    if not isinstance(payload, dict):
        return {"permissionDecision": "deny",
                "permissionDecisionReason": "The hook received an invalid tool payload."}
    tool_name = payload.get("toolName", payload.get("tool_name", ""))
    if tool_name not in {"bash", "powershell", "shell", "Bash"}:
        return {}
    command = _command_from_args(payload.get("toolArgs", payload.get("tool_input", {})))
    normalised = command.replace("\\", "/")
    if "fixtures/" in normalised and re.search(r"(?:>|>>|\b(?:tee|cp|mv|touch|rm)\b)", normalised, re.I):
        return {"permissionDecision": "deny",
                "permissionDecisionReason": "Fixture writes require an explicit task scope."}
    for pattern, reason in DENY_RULES:
        if pattern.search(command):
            return {"permissionDecision": "deny", "permissionDecisionReason": reason}
    return {}


def main() -> int:
    try:
        result = decision_for_payload(json.load(sys.stdin))
    except (json.JSONDecodeError, OSError) as exc:
        result = {"permissionDecision": "deny",
                  "permissionDecisionReason": f"The hook could not read its input: {exc}"}
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
