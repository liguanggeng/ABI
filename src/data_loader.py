"""Utilities for loading sample market performance data for analysis models."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


@dataclass(frozen=True)
class MarketRecord:
    market: str
    model: str
    period: str
    is_post_countermeasure: bool
    countermeasure_id: Optional[str]
    sales: int
    complaints: int
    customer_satisfaction: float
    warranty_cost: float
    issue_category: str

    @property
    def complaint_rate(self) -> float:
        return self.complaints / self.sales if self.sales else 0.0


def _parse_bool(value: str) -> bool:
    return value.lower() in {"true", "1", "yes"}


def load_market_performance_data(path: Path) -> List[MarketRecord]:
    """Load the market performance dataset into ``MarketRecord`` objects."""

    records: List[MarketRecord] = []
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                MarketRecord(
                    market=row["market"],
                    model=row["model"],
                    period=row["period"],
                    is_post_countermeasure=_parse_bool(row["is_post_countermeasure"]),
                    countermeasure_id=row["countermeasure_id"] or None,
                    sales=int(row["sales"]),
                    complaints=int(row["complaints"]),
                    customer_satisfaction=float(row["customer_satisfaction"]),
                    warranty_cost=float(row["warranty_cost"]),
                    issue_category=row["issue_category"],
                )
            )
    return records


__all__ = ["MarketRecord", "load_market_performance_data"]
