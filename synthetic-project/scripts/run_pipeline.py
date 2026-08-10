#!/usr/bin/env python3
"""Run one synthetic pipeline scenario from the project directory."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipeline_ops.health_report import render_text  # noqa: E402
from pipeline_ops.pipeline_runner import SCENARIOS, run_pipeline  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, default="healthy")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--records", type=int, default=400)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    output = args.output_dir or ROOT / "runs" / f"{args.scenario}-{args.seed}"
    try:
        code, report = run_pipeline(output, scenario=args.scenario, seed=args.seed,
                                    record_count=args.records)
    except (OSError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
        try:
            location = output.relative_to(ROOT.parent)
        except ValueError:
            location = output
        print(f"Artifacts: {len(list(output.iterdir()))} files in {location}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
