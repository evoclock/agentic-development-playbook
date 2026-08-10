"""Classify optional context-pressure telemetry for a supervised session."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

CHECKPOINT_PERCENT = 60.0
EMERGENCY_PERCENT = 90.0


def classify(percent: float | None) -> dict[str, Any]:
    if percent is None:
        return {"percent": None, "band": "UNKNOWN", "checkpoint_required": False,
                "compact_required": False, "short_turn_only": True,
                "substantive_work_allowed": False,
                "action": "Obtain telemetry before a long turn"}
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    if percent < CHECKPOINT_PERCENT:
        return {"percent": percent, "band": "NORMAL", "checkpoint_required": False,
                "compact_required": False, "short_turn_only": False,
                "substantive_work_allowed": True, "action": "Normal work is allowed"}
    if percent < EMERGENCY_PERCENT:
        return {"percent": percent, "band": "CHECKPOINT_REQUIRED", "checkpoint_required": True,
                "compact_required": True, "short_turn_only": True,
                "substantive_work_allowed": False,
                "action": "Write a checkpoint and compact before substantive work"}
    return {"percent": percent, "band": "EMERGENCY_CHECKPOINT", "checkpoint_required": True,
            "compact_required": True, "short_turn_only": True,
            "substantive_work_allowed": False,
            "action": "Checkpoint active state, compact, and stop substantive work"}


def read_percent() -> tuple[float | None, str]:
    raw = os.environ.get("AGENT_CONTEXT_PERCENT")
    if raw is None:
        return None, "unavailable"
    try:
        return float(raw), "AGENT_CONTEXT_PERCENT"
    except ValueError as exc:
        raise ValueError("AGENT_CONTEXT_PERCENT is not numeric") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--percent", type=float)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        percent, source = (args.percent, "command_line") if args.percent is not None else read_percent()
        result = classify(percent)
        result["source"] = source
    except ValueError as exc:
        print(f"context-pressure diagnostic failed: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        shown = "unavailable" if result["percent"] is None else f"{result['percent']:.1f}%"
        print(f"Band: {result['band']}")
        print(f"Measured usage: {shown} (source: {result['source']})")
        print(f"Action: {result['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
