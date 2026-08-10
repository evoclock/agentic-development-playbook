"""Deterministic synthetic records and input validation."""
from __future__ import annotations

import random
from typing import Any

REQUIRED_FIELDS = ("record_id", "event_count", "days_since_event", "segment", "label", "split")


def generate_records(seed: int = 17, count: int = 400) -> list[dict[str, Any]]:
    """Generate public-safe records from a reproducible seed."""
    if count < 20:
        raise ValueError("count must be at least 20")
    rng = random.Random(seed)
    records = []
    for index in range(count):
        event_count = rng.randint(1, 20)
        days_since_event = rng.randint(0, 30)
        segment = rng.choice((0, 1, 2))
        segment_weight = (-0.4, 0.0, 0.35)[segment]
        latent_risk = 0.11 * event_count + 0.04 * (30 - days_since_event) + segment_weight
        label = int(latent_risk + (rng.random() - 0.5) * 0.9 > 1.25)
        records.append({
            "record_id": f"record-{index:05d}",
            "event_count": event_count,
            "days_since_event": days_since_event,
            "segment": segment,
            "label": label,
            "split": "train" if index < int(count * 0.75) else "test",
        })
    return records


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate records and return machine-readable evidence."""
    errors: list[dict[str, Any]] = []
    missing_required_values = 0
    duplicate_rows = 0
    seen_ids: set[str] = set()
    for index, record in enumerate(records):
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            missing_required_values += len(missing)
            errors.append({"row": index, "code": "MISSING_FIELD", "fields": missing})
            continue
        record_id = record["record_id"]
        if record_id in seen_ids:
            duplicate_rows += 1
            errors.append({"row": index, "code": "DUPLICATE_ID", "record_id": record_id})
        seen_ids.add(record_id)
        if not isinstance(record["event_count"], int) or isinstance(record["event_count"], bool):
            errors.append({"row": index, "code": "INVALID_EVENT_COUNT"})
        if not isinstance(record["days_since_event"], int) or not 0 <= record["days_since_event"] <= 30:
            errors.append({"row": index, "code": "INVALID_EVENT_AGE"})
        if record["segment"] not in (0, 1, 2):
            errors.append({"row": index, "code": "INVALID_SEGMENT"})
        if record["label"] not in (0, 1):
            errors.append({"row": index, "code": "INVALID_LABEL"})
        if record["split"] not in ("train", "test"):
            errors.append({"row": index, "code": "INVALID_SPLIT"})
    return {
        "records_checked": len(records),
        "schema_errors": len(errors),
        "missing_required_values": missing_required_values,
        "duplicate_rows": duplicate_rows,
        "errors": errors,
    }
