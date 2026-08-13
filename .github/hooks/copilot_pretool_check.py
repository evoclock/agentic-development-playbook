"""Deny selected risky Copilot CLI tool calls for the public demo."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
HISTORY_PATTERN = re.compile(r"\bgit\s+(?:push|commit|merge|rebase)\b", re.I)

DENY_RULES = (
    (HISTORY_PATTERN,
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


# Small, standard-library-only content checks informed by Hillstar/Testudo
# patterns. This is a public demo boundary, not a complete DLP or WAF.
HIDDEN_UNICODE_PATTERN = re.compile(
    "[\u200b\u200c\u200d\u2060\u2066\u2067\u2068\u2069\u202a\u202b\u202c\u202d\u202e\ufeff]"
)
HIDDEN_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)

SECURITY_REDACTION_RULES = (
    ("pii", "email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
     "[REDACTED-PII-EMAIL]"),
    ("pii", "uk-nhs-number", re.compile(r"\b\d{3}\s?\d{3}\s?\d{4}\b"),
     "[REDACTED-PII-NHS]"),
    ("secret", "api-key", re.compile(
        r"(?i)\bapi[_ -]?key\s*[:=]\s*['\"]?[A-Za-z0-9._-]{12,}"
    ), "[REDACTED-SECRET-API-KEY]"),
    ("secret", "bearer-token", re.compile(
        r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"
    ), "[REDACTED-SECRET-BEARER]"),
    ("secret", "private-key-marker", re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ), "[REDACTED-SECRET-PRIVATE-KEY]"),
)

SECURITY_REJECTION_RULES = (
    ("prompt-injection", "ignore-previous-instructions", re.compile(
        r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|earlier)\s+instructions\b"
    ), "high"),
    ("prompt-injection", "role-hijack", re.compile(
        r"(?i)\byou\s+are\s+now\s+(?:in\s+)?(?:admin|root|debug|maintenance)\s+mode\b"
    ), "high"),
    ("prompt-injection", "safety-bypass", re.compile(
        r"(?i)\b(?:bypass|disable|override|ignore)\s+(?:all\s+)?(?:safety|security)\s+(?:checks|filters|restrictions)\b"
    ), "high"),
    ("prompt-injection", "tool-override", re.compile(
        r"(?i)\b(?:execute|run|call)\s+the\s+following\s+(?:command|tool|function)\b"
    ), "high"),
    ("mcp-threat", "tool-poisoning", re.compile(
        r"(?i)\b(?:also|additionally)\s+(?:exfiltrate|send|forward|leak)\b"
    ), "high"),
    ("mcp-threat", "indirect-injection", re.compile(
        r"(?i)\bwhen\s+(?:you\s+)?(?:read|process|see)\s+this[,.]?\s+(?:execute|run|call|send|forward|leak)\b"
    ), "high"),
    ("mcp-threat", "credential-relay", re.compile(
        r"(?i)\b(?:forward|relay|send)\s+(?:my|the|this)\s+(?:token|credential|api[_-]?key)\b"
    ), "high"),
)


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


def _security_finding(category: str, rule: str, severity: str) -> dict[str, str]:
    """Return a public-safe finding without matched sensitive content."""
    return {"category": category, "rule": rule, "severity": severity}


def security_review(content: str) -> dict[str, Any]:
    """Review content with accept/redact/reject semantics.

    Hidden characters, PII, and secrets are redacted. Prompt-injection and
    MCP-threat findings reject. The returned content is safe for a
    reviewer to inspect, but this small detector is not production assurance.
    """
    if not isinstance(content, str):
        return {
            "decision": "reject",
            "content": "",
            "findings": [_security_finding("input", "invalid-content", "high")],
        }

    cleaned = content
    findings: list[dict[str, str]] = []
    for pattern, marker, category, rule in (
        (HIDDEN_UNICODE_PATTERN, "[REDACTED-HIDDEN-UNICODE]", "hidden-unicode", "control-character"),
        (HIDDEN_COMMENT_PATTERN, "[REDACTED-HIDDEN-COMMENT]", "hidden-payload", "html-comment"),
    ):
        matches = list(pattern.finditer(cleaned))
        findings.extend(_security_finding(category, rule, "high") for _ in matches)
        cleaned = pattern.sub(marker, cleaned)

    for category, rule, pattern, marker in SECURITY_REDACTION_RULES:
        matches = list(pattern.finditer(cleaned))
        findings.extend(_security_finding(category, rule, "high") for _ in matches)
        cleaned = pattern.sub(marker, cleaned)

    rejection_findings: list[dict[str, str]] = []
    for category, rule, pattern, severity in SECURITY_REJECTION_RULES:
        rejection_findings.extend(
            _security_finding(category, rule, severity)
            for _ in pattern.finditer(cleaned)
        )
    findings.extend(rejection_findings)

    if rejection_findings:
        decision = "reject"
    elif findings:
        decision = "redact"
    else:
        decision = "accept"
    return {"decision": decision, "content": cleaned, "findings": findings}


def task_receipt_ready(repo: Path = REPO_ROOT) -> bool:
    """Return whether TASKS.md contains a usable subtask receipt."""
    path = repo / "TASKS.md"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    required = ("## Receipts", "Files changed:", "Checks:", "Evidence:", "Next decision:")
    return all(marker in text for marker in required)


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


def decision_for_payload(payload: Any, *, repo: Path | None = None) -> dict[str, str]:
    """Return {} for normal permission flow or a deny decision."""
    if not isinstance(payload, dict):
        return {"permissionDecision": "deny",
                "permissionDecisionReason": "The hook received an invalid tool payload."}
    tool_name = payload.get("toolName", payload.get("tool_name", ""))
    if tool_name not in {"bash", "powershell", "shell", "Bash"}:
        return {}
    command = _command_from_args(payload.get("toolArgs", payload.get("tool_input", {})))
    normalised = command.replace("\\", "/")
    security = security_review(command)
    if security["decision"] != "accept":
        categories = sorted({finding["category"] for finding in security["findings"]})
        if security["decision"] == "redact":
            reason = "Security review found sensitive content; redact it before tool use."
        else:
            reason = "Security review rejected possible injection or threat content."
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{reason} Categories: {', '.join(categories)}.",
        }
    if "fixtures/" in normalised and re.search(r"(?:>|>>|\b(?:tee|cp|mv|touch|rm)\b)", normalised, re.I):
        return {"permissionDecision": "deny",
                "permissionDecisionReason": "Fixture writes require an explicit task scope."}
    resolved_repo = repo or _resolve_repo(payload)
    for pattern, reason in DENY_RULES:
        if pattern.search(command):
            if pattern is HISTORY_PATTERN and not task_receipt_ready(resolved_repo):
                reason = f"{reason} Update TASKS.md with the subtask receipt first."
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
