from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pipeline_ops.pipeline_core import generate_records, validate_records  # noqa: E402


class PipelineCoreTests(unittest.TestCase):
    def test_generation_is_reproducible(self):
        self.assertEqual(generate_records(seed=4, count=20), generate_records(seed=4, count=20))

    def test_generated_records_validate(self):
        records = generate_records(seed=4, count=40)
        result = validate_records(records)
        self.assertEqual(result["records_checked"], 40)
        self.assertEqual(result["schema_errors"], 0)

    def test_missing_field_is_evidence(self):
        records = generate_records(seed=4, count=20)
        del records[3]["event_count"]
        result = validate_records(records)
        self.assertEqual(result["missing_required_values"], 1)
        self.assertEqual(result["errors"][0]["code"], "MISSING_FIELD")

    def test_duplicate_id_is_evidence(self):
        records = generate_records(seed=4, count=20)
        records[1]["record_id"] = records[0]["record_id"]
        result = validate_records(records)
        self.assertEqual(result["duplicate_rows"], 1)


if __name__ == "__main__":
    unittest.main()
