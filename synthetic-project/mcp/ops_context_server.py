"""Read-only MCP context server for the synthetic pipeline project."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_FILES = {
    "overview": PROJECT_ROOT / "README.md",
    "runbook": PROJECT_ROOT / "runbooks" / "pipeline-triage.md",
    "ticket": PROJECT_ROOT / "DEMO-TICKET.md",
    "fixture_manifest": PROJECT_ROOT / "fixtures" / "run_manifest.json",
}
EVIDENCE = [
    "synthetic-project/README.md",
    "synthetic-project/DEMO-TICKET.md",
    "synthetic-project/runbooks/pipeline-triage.md",
    "synthetic-project/fixtures/run_manifest.json",
]
TOOLS = [
    {
        "name": "get_pipeline_context",
        "description": "Read one tracked synthetic pipeline context item.",
        "inputSchema": {
            "type": "object",
            "properties": {"item": {"type": "string", "enum": list(CONTEXT_FILES)}},
            "required": ["item"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_evidence",
        "description": "List tracked relative evidence files for the walkthrough.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


def _text_result(text: str, *, error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": error}


def _context(item: str) -> str:
    if item not in CONTEXT_FILES:
        raise ValueError("item must be overview, runbook, ticket, or fixture_manifest")
    try:
        return CONTEXT_FILES[item].read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"context item cannot be read: {exc}") from exc


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one JSON-RPC request, returning None for notifications."""
    method = request.get("method")
    request_id = request.get("id")
    params = request.get("params") or {}
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": request_id, "result": {
            "protocolVersion": params.get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "dsops-context", "version": "0.2.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            if name == "get_pipeline_context":
                result = _text_result(_context(arguments.get("item", "")))
            elif name == "list_evidence":
                result = _text_result(json.dumps(EVIDENCE, indent=2))
            else:
                raise ValueError("unknown tool")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except ValueError as exc:
            return {"jsonrpc": "2.0", "id": request_id,
                    "result": _text_result(str(exc), error=True)}
    return {"jsonrpc": "2.0", "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError("request must be a JSON object")
            response = handle_request(request)
            if response is not None:
                print(json.dumps(response, separators=(",", ":")), flush=True)
        except (json.JSONDecodeError, ValueError) as exc:
            print(json.dumps({"jsonrpc": "2.0", "id": None,
                              "error": {"code": -32700, "message": str(exc)}},
                             separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
