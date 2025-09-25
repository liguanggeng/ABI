"""Model training utilities that transform business questions into predictions."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from .data_loader import MarketRecord


@dataclass
class ModelTrainingResult:
    """Container with the fitted model and evaluation metrics."""

    model: "ComplaintRateLookupModel"
    rmse: float
    r2: float


class ComplaintRateLookupModel:
    """A lightweight model that memorises complaint rates per feature combo."""

    def __init__(self, lookup: Dict[Tuple[str, str, str, bool], float], default: float):
        self._lookup = lookup
        self._default = default

    def predict(self, records: Sequence[MarketRecord]) -> List[float]:
        predictions: List[float] = []
        for record in records:
            key = (
                record.market,
                record.model,
                record.issue_category,
                record.is_post_countermeasure,
            )
            predictions.append(self._lookup.get(key, self._default))
        return predictions


def _train_lookup(records: Sequence[MarketRecord]) -> ComplaintRateLookupModel:
    grouped: Dict[Tuple[str, str, str, bool], List[float]] = {}
    for record in records:
        key = (
            record.market,
            record.model,
            record.issue_category,
            record.is_post_countermeasure,
        )
        grouped.setdefault(key, []).append(record.complaint_rate)

    lookup = {
        key: sum(values) / len(values)
        for key, values in grouped.items()
        if values
    }
    default = sum(r.complaint_rate for r in records) / len(records)
    return ComplaintRateLookupModel(lookup=lookup, default=default)


def _split_records(
    records: Sequence[MarketRecord], test_size: float, random_state: int
) -> Tuple[List[MarketRecord], List[MarketRecord]]:
    rng = random.Random(random_state)
    records = list(records)
    rng.shuffle(records)
    split_index = max(1, int(len(records) * (1 - test_size)))
    return records[:split_index], records[split_index:]


def train_complaint_rate_model(
    records: Iterable[MarketRecord],
    test_size: float = 0.2,
    random_state: int = 42,
) -> ModelTrainingResult:
    """Train a simple lookup-based regression model that predicts complaint rate."""

    records = list(records)
    train_records, test_records = _split_records(records, test_size, random_state)
    model = _train_lookup(train_records)

    if not test_records:
        test_records = train_records

    predictions = model.predict(test_records)
    actuals = [record.complaint_rate for record in test_records]
    mse = sum((pred - actual) ** 2 for pred, actual in zip(predictions, actuals)) / len(
        actuals
    )
    mean_actual = sum(actuals) / len(actuals)
    ss_tot = sum((actual - mean_actual) ** 2 for actual in actuals)
    ss_res = sum((pred - actual) ** 2 for pred, actual in zip(predictions, actuals))
    rmse = math.sqrt(mse)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0

    return ModelTrainingResult(model=model, rmse=rmse, r2=r2)


__all__ = ["train_complaint_rate_model", "ModelTrainingResult", "ComplaintRateLookupModel"]
