from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipeline_ops.pipeline_core import generate_records  # noqa: E402
from pipeline_ops.pipeline_model import (  # noqa: E402
    build_features,
    evaluate_model,
    train_model,
)


class PipelineModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = generate_records(seed=17, count=400)

    def test_feature_window_records_row_retention(self):
        rows = build_features(self.records, window_days=30)
        self.assertEqual(len(rows), 400)
        reduced = build_features(self.records, window_days=10)
        self.assertLess(len(reduced) / len(self.records), 0.99)

    def test_baseline_evaluation_is_above_threshold(self):
        rows = build_features(self.records)
        report = evaluate_model(train_model(rows), rows, seed=17)
        self.assertGreater(report["auc"], report["target_auc"])

    def test_inverted_scores_create_warning_metric(self):
        rows = build_features(self.records)
        report = evaluate_model(train_model(rows), rows, seed=17, invert_scores=True)
        self.assertLess(report["auc"], report["target_auc"])


if __name__ == "__main__":
    unittest.main()
