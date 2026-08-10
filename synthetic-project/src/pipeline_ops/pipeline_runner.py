"""Orchestrate the deterministic synthetic pipeline and write evidence."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .health_report import EXIT_CODES, evaluate_manifest
from .pipeline_core import generate_records, validate_records
from .pipeline_model import build_features, evaluate_model, train_model

PIPELINE_NAME = "synthetic-churn-training"
DATASET_NAME = "synthetic_customer_events_v1"
SOURCE_REVISION = "synthetic-source-v1"
GENERATOR_VERSION = "0.2.0"
SCENARIOS = ("healthy", "evaluation-warning", "row-loss", "schema-failure")


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def run_pipeline(output_dir: Path, *, scenario: str = "healthy", seed: int = 17,
                 record_count: int = 400) -> tuple[int, dict[str, Any]]:
    """Run one scenario and return its health-report exit code and report."""
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    if record_count < 20:
        raise ValueError("record_count must be at least 20")
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = f"demo-{scenario}-{seed}"
    provenance = {
        "run_id": run_id,
        "pipeline": PIPELINE_NAME,
        "dataset": DATASET_NAME,
        "source_revision": SOURCE_REVISION,
        "generator": "pipeline_ops.pipeline_runner",
        "generator_version": GENERATOR_VERSION,
        "scenario": scenario,
        "random_seed": seed,
        "record_count": record_count,
        "deterministic": True,
    }
    _write_json(output_dir / "provenance.json", provenance)
    records = generate_records(seed=seed, count=record_count)
    if scenario == "schema-failure":
        del records[3]["event_count"]
    _write_jsonl(output_dir / "raw_records.jsonl", records)
    stages: list[dict[str, Any]] = [{
        "name": "ingest", "status": "passed",
        "metrics": {"records_in": len(records), "source_revision": SOURCE_REVISION},
        "artifacts": ["raw_records.jsonl"],
    }]
    validation = validate_records(records)
    _write_json(output_dir / "validation.json", validation)
    validation_status = "failed" if validation["schema_errors"] else "passed"
    stages.append({
        "name": "validate", "status": validation_status,
        "metrics": {key: validation[key] for key in
                     ("records_checked", "schema_errors", "missing_required_values", "duplicate_rows")},
        "artifacts": ["validation.json"],
    })
    failures: list[dict[str, Any]] = []
    if validation_status == "failed":
        failures.append({
            "stage": "validate", "severity": "error", "code": "SCHEMA_INVALID",
            "message": "Generated records failed the required input contract.",
            "evidence": "validation.json",
        })
        manifest = {"run_id": run_id, "pipeline": PIPELINE_NAME, "dataset": DATASET_NAME,
                    "source_revision": SOURCE_REVISION, "scenario": scenario, "seed": seed,
                    "stages": stages}
        _write_jsonl(output_dir / "failure_log.jsonl", failures)
        _write_json(output_dir / "run_manifest.json", manifest)
        report = evaluate_manifest(manifest)
        _write_json(output_dir / "health_report.json", report)
        return EXIT_CODES[report["status"]], report

    window_days = 15 if scenario == "row-loss" else 30
    feature_rows = build_features(records, window_days=window_days)
    _write_jsonl(output_dir / "features.jsonl", feature_rows)
    stages.append({
        "name": "features", "status": "passed",
        "metrics": {"rows_in": len(records), "rows_out": len(feature_rows),
                    "feature_columns": 3, "window_days": window_days},
        "artifacts": ["features.jsonl"],
    })
    model = train_model(feature_rows)
    _write_json(output_dir / "model.json", model)
    stages.append({"name": "train", "status": "passed", "metrics": model,
                   "artifacts": ["model.json"]})
    evaluation = evaluate_model(
        model, feature_rows, seed=seed, invert_scores=(scenario == "evaluation-warning")
    )
    _write_json(output_dir / "evaluation.json", evaluation)
    stages.append({"name": "evaluate", "status": "passed", "metrics": evaluation,
                   "artifacts": ["evaluation.json"]})
    manifest = {"run_id": run_id, "pipeline": PIPELINE_NAME, "dataset": DATASET_NAME,
                "source_revision": SOURCE_REVISION, "scenario": scenario, "seed": seed,
                "stages": stages}
    _write_jsonl(output_dir / "failure_log.jsonl", failures)
    _write_json(output_dir / "run_manifest.json", manifest)
    report = evaluate_manifest(manifest)
    _write_json(output_dir / "health_report.json", report)
    return EXIT_CODES[report["status"]], report
