#!/usr/bin/env python3
"""Generate model-routing runtime roster from a Copilot prompt response."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RAW = Path(__file__).with_name("models.raw.jsonl")
DEFAULT_RUNTIME = Path(__file__).with_name("models.runtime.json")
ROLES = ["implementation", "planning", "review"]
EFFORTS = ["none", "minimal", "low", "medium", "high", "xhigh", "max"]


PROMPT = (
    "List available models as strict JSON array. "
    "Each item must be an object with exactly these fields: id, label."
)


def _run_copilot(prompt: str, cwd: Path) -> str:
    command = ["copilot", "-p", prompt, "-s"]
    result = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, check=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "unknown error").strip()
        raise ValueError(f"copilot command failed: {message}")
    return result.stdout.strip()


def _extract_json_array(text: str) -> list[dict[str, str]]:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("copilot output did not include a JSON array")
    payload = json.loads(text[start:end + 1])
    if not isinstance(payload, list) or not payload:
        raise ValueError("model list must be a non-empty JSON array")
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        model_id = item.get("id")
        label = item.get("label")
        if not isinstance(model_id, str) or not model_id.strip():
            continue
        if not isinstance(label, str) or not label.strip():
            continue
        model_id = model_id.strip()
        if model_id in seen:
            continue
        seen.add(model_id)
        items.append({"id": model_id, "label": label.strip()})
    if not items:
        raise ValueError("no valid model entries found in Copilot output")
    return items


def _runtime_roster(models: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "models": [
            {
                "id": model["id"],
                "label": model["label"],
                "provider": "copilot",
                "available": True,
                "cost_tier": "unspecified",
                "capabilities": ROLES,
                "efforts": EFFORTS,
            }
            for model in models
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--raw-output", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--runtime-output", type=Path, default=DEFAULT_RUNTIME)
    args = parser.parse_args()

    raw_text = _run_copilot(args.prompt, ROOT)
    args.raw_output.write_text(raw_text + "\n", encoding="utf-8")

    models = _extract_json_array(raw_text)
    runtime = _runtime_roster(models)
    args.runtime_output.write_text(json.dumps(runtime, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "raw_output": str(args.raw_output),
                "runtime_output": str(args.runtime_output),
                "models_count": len(models),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
