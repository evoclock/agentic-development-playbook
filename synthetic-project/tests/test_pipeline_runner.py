from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipeline_ops.pipeline_runner import run_pipeline  # noqa: E402


class PipelineRunnerTests(unittest.TestCase):
    def run_case(self, scenario: str):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return Path(temp.name), run_pipeline(Path(temp.name), scenario=scenario, seed=17)

    def test_healthy_run_writes_evidence(self):
        output, (code, report) = self.run_case("healthy")
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "healthy")
        for name in ("raw_records.jsonl", "validation.json", "features.jsonl", "model.json",
                     "evaluation.json", "provenance.json", "run_manifest.json",
                     "failure_log.jsonl", "health_report.json"):
            self.assertTrue((output / name).is_file(), name)
        evaluation = json.loads((output / "evaluation.json").read_text())
        self.assertGreater(evaluation["auc"], evaluation["target_auc"])

    def test_evaluation_warning_is_computed(self):
        output, (code, report) = self.run_case("evaluation-warning")
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "warning")
        evaluation = json.loads((output / "evaluation.json").read_text())
        self.assertLess(evaluation["auc"], evaluation["target_auc"])

    def test_row_loss_is_recorded_for_the_retention_task(self):
        output, (code, report) = self.run_case("row-loss")
        manifest = json.loads((output / "run_manifest.json").read_text())
        ingest = manifest["stages"][0]["metrics"]["records_in"]
        features = manifest["stages"][2]["metrics"]["rows_out"]
        self.assertLess(features / ingest, 0.99)
        self.assertEqual(report["status"], "warning")
        self.assertEqual(code, 1)
        self.assertIn("features.row_retention", [check["name"] for check in report["checks"]])

    def test_schema_failure_stops_before_features(self):
        output, (code, report) = self.run_case("schema-failure")
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "failed")
        self.assertFalse((output / "features.jsonl").exists())
        failures = (output / "failure_log.jsonl").read_text().splitlines()
        self.assertEqual(json.loads(failures[0])["code"], "SCHEMA_INVALID")


if __name__ == "__main__":
    unittest.main()
