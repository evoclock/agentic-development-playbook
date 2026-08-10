"""Feature construction and deterministic baseline evaluation."""
from __future__ import annotations

import random
from typing import Any


def build_features(records: list[dict[str, Any]], window_days: int = 30) -> list[dict[str, Any]]:
    """Keep records in the feature window and derive three numeric features."""
    if not 0 <= window_days <= 30:
        raise ValueError("window_days must be between 0 and 30")
    rows = []
    for record in records:
        if record["days_since_event"] > window_days:
            continue
        rows.append({
            **record,
            "features": {
                "event_count_norm": round(record["event_count"] / 20, 6),
                "recency_norm": round((30 - record["days_since_event"]) / 30, 6),
                "segment_norm": round(record["segment"] / 2, 6),
            },
        })
    return rows


def _vector(row: dict[str, Any]) -> list[float]:
    values = row["features"]
    return [values["event_count_norm"], values["recency_norm"], values["segment_norm"]]


def train_model(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Fit a mean-difference linear baseline from training rows."""
    train = [row for row in rows if row["split"] == "train"]
    positive = [_vector(row) for row in train if row["label"] == 1]
    negative = [_vector(row) for row in train if row["label"] == 0]
    if not positive or not negative:
        raise ValueError("training data must contain both label classes")
    pos_mean = [sum(row[i] for row in positive) / len(positive) for i in range(3)]
    neg_mean = [sum(row[i] for row in negative) / len(negative) for i in range(3)]
    weights = [pos_mean[i] - neg_mean[i] for i in range(3)]
    intercept = -0.5 * sum(weights[i] * (pos_mean[i] + neg_mean[i]) for i in range(3))
    return {
        "method": "mean_difference_linear_baseline",
        "rows": len(train),
        "positive_rows": len(positive),
        "negative_rows": len(negative),
        "intercept": round(intercept, 6),
        "weights": [round(weight, 6) for weight in weights],
    }


def _score(model: dict[str, Any], row: dict[str, Any]) -> float:
    return model["intercept"] + sum(weight * value for weight, value in zip(model["weights"], _vector(row)))


def calculate_auc(labels: list[int], scores: list[float]) -> float:
    """Calculate rank-based AUC without an external dependency."""
    if len(labels) != len(scores):
        raise ValueError("labels and scores must have equal lengths")
    positives = sum(labels)
    negatives = len(labels) - positives
    if not positives or not negatives:
        raise ValueError("evaluation data must contain both label classes")
    ranked = sorted(zip(scores, labels), key=lambda pair: pair[0])
    rank_sum = 0.0
    index = 0
    while index < len(ranked):
        end = index + 1
        while end < len(ranked) and ranked[end][0] == ranked[index][0]:
            end += 1
        average_rank = (index + 1 + end) / 2
        rank_sum += average_rank * sum(label for _, label in ranked[index:end])
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def evaluate_model(model: dict[str, Any], rows: list[dict[str, Any]], *, seed: int = 17,
                   invert_scores: bool = False, target_auc: float = 0.80) -> dict[str, Any]:
    """Score test rows and return calculated evaluation evidence."""
    test = [row for row in rows if row["split"] == "test"]
    labels = [row["label"] for row in test]
    scores = []
    for index, row in enumerate(test):
        jitter = (random.Random(seed + index + 1000).random() - 0.5) * 0.7
        score = _score(model, row) + jitter
        scores.append(-score if invert_scores else score)
    auc = calculate_auc(labels, scores)
    return {
        "test_rows": len(test),
        "positive_rows": sum(labels),
        "negative_rows": len(labels) - sum(labels),
        "auc": round(auc, 6),
        "target_auc": target_auc,
        "score_mode": "inverted" if invert_scores else "normal",
    }
