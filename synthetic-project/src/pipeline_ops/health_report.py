"""Create a deterministic health report for a synthetic pipeline run."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_MIN_AUC = 0.80
DEFAULT_MAX_SCHEMA_ERRORS = 0
DEFAULT_MIN_ROW_RETENTION = 0.99
DEFAULT_MIN_TEST_ROWS = 50
EXIT_CODES = {"healthy": 0, "warning": 1, "failed": 2}
VALID_STATUSES = {"passed", "warning", "failed"}


def load_manifest(path: Path) -> dict[str, Any]:
    """Load and validate the run-manifest contract."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Manifest is not valid JSON: {exc.msg}") from exc
    except OSError as exc:
        raise ValueError(f"Manifest cannot be read: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Manifest must contain a JSON object")
    for field in ("run_id", "pipeline", "dataset", "stages"):
        if field not in data:
            raise ValueError(f"Manifest is missing required field: {field}")
    stages = data["stages"]
    if not isinstance(stages, list) or not stages:
        raise ValueError("Manifest stages must be a non-empty list")
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            raise ValueError(f"Stage {index} must be an object")
        for field in ("name", "status"):
            if field not in stage:
                raise ValueError(f"Stage {index} is missing required field: {field}")
        if stage["status"] not in VALID_STATUSES:
            raise ValueError(f"Stage {stage['name']} has an unsupported status")
    return data


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number")
    return float(value)


def evaluate_manifest(
    manifest: dict[str, Any], *, min_auc: float = DEFAULT_MIN_AUC,
    max_schema_errors: int = DEFAULT_MAX_SCHEMA_ERRORS,
    min_row_retention: float = DEFAULT_MIN_ROW_RETENTION,
    min_test_rows: int = DEFAULT_MIN_TEST_ROWS,
) -> dict[str, Any]:
    """Evaluate checks without changing the input manifest."""
    for field in ("run_id", "pipeline", "dataset", "stages"):
        if field not in manifest:
            raise ValueError(f"Manifest is missing required field: {field}")
    checks: list[dict[str, str]] = []
    failed = False
    warning = False
    records_in: float | None = None
    for stage in manifest["stages"]:
        name = str(stage["name"])
        status = str(stage["status"])
        check_status = "pass" if status == "passed" else status
        checks.append({"name": f"stage.{name}", "status": check_status,
                       "detail": f"stage status is {status}"})
        failed = failed or status == "failed"
        warning = warning or status == "warning"
        metrics = stage.get("metrics", {})
        if not isinstance(metrics, dict):
            raise ValueError(f"Metrics for stage {name} must be an object")
        if name == "ingest" and "records_in" in metrics:
            records_in = _number(metrics["records_in"], "ingest.records_in")
            if records_in <= 0:
                raise ValueError("ingest.records_in must be greater than zero")
        if "schema_errors" in metrics:
            errors = _number(metrics["schema_errors"], f"{name}.schema_errors")
            check_status = "pass" if errors <= max_schema_errors else "failed"
            checks.append({"name": f"{name}.schema_errors", "status": check_status,
                           "detail": f"{errors:g} <= {max_schema_errors:g}"})
            failed = failed or check_status == "failed"
        if name == "features" and records_in is not None and "rows_out" in metrics:
            rows_out = _number(metrics["rows_out"], "features.rows_out")
            retention = rows_out / records_in
            check_status = "pass" if retention >= min_row_retention else "warning"
            operator = ">=" if check_status == "pass" else "<"
            checks.append({"name": "features.row_retention", "status": check_status,
                           "detail": f"{retention:.3f} {operator} {min_row_retention:.3f}"})
            warning = warning or check_status == "warning"
        if name == "evaluate" and "test_rows" in metrics:
            test_rows = _number(metrics["test_rows"], "evaluate.test_rows")
            check_status = "pass" if test_rows >= min_test_rows else "warning"
            operator = ">=" if check_status == "pass" else "<"
            checks.append({"name": "evaluate.test_rows", "status": check_status,
                           "detail": f"{test_rows:g} {operator} {min_test_rows:g}"})
            warning = warning or check_status == "warning"
        if "auc" in metrics:
            auc = _number(metrics["auc"], f"{name}.auc")
            check_status = "pass" if auc >= min_auc else "warning"
            operator = ">=" if check_status == "pass" else "<"
            checks.append({"name": f"{name}.auc", "status": check_status,
                           "detail": f"{auc:.3f} {operator} {min_auc:.3f}"})
            warning = warning or check_status == "warning"
    overall = "failed" if failed else "warning" if warning else "healthy"
    stages = manifest["stages"]
    counts = {
        "total": len(stages),
        "passed": sum(s["status"] == "passed" for s in stages),
        "warning": sum(s["status"] == "warning" for s in stages),
        "failed": sum(s["status"] == "failed" for s in stages),
    }
    recommendations = {
        "healthy": "Run passed the configured checks.",
        "warning": "Review warning checks before promotion.",
        "failed": "Resolve failed checks before rerunning the pipeline.",
    }
    return {"run_id": manifest["run_id"], "pipeline": manifest["pipeline"],
            "dataset": manifest["dataset"], "status": overall, "stages": counts,
            "checks": checks, "recommendation": recommendations[overall]}


def render_text(report: dict[str, Any]) -> str:
    """Render a stable terminal report."""
    stages = report["stages"]
    lines = [f"Run: {report['run_id']}", f"Pipeline: {report['pipeline']}",
             f"Dataset: {report['dataset']}", f"Overall status: {report['status'].upper()}",
             (f"Stages: {stages['total']} total | {stages['passed']} passed | "
              f"{stages['warning']} warning | {stages['failed']} failed"), "Checks:"]
    labels = {"pass": "PASS", "warning": "WARN", "failed": "FAIL"}
    for check in report["checks"]:
        lines.append(f"  {labels[check['status']]} {check['name']}: {check['detail']}")
    lines.append(f"Recommendation: {report['recommendation']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--min-auc", type=float, default=DEFAULT_MIN_AUC)
    parser.add_argument("--max-schema-errors", type=int, default=DEFAULT_MAX_SCHEMA_ERRORS)
    parser.add_argument("--min-row-retention", type=float, default=DEFAULT_MIN_ROW_RETENTION)
    parser.add_argument("--min-test-rows", type=int, default=DEFAULT_MIN_TEST_ROWS)
    args = parser.parse_args(argv)
    try:
        report = evaluate_manifest(load_manifest(args.manifest), min_auc=args.min_auc,
                                   max_schema_errors=args.max_schema_errors,
                                   min_row_retention=args.min_row_retention,
                                   min_test_rows=args.min_test_rows)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return EXIT_CODES[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
