"""Core analytical routines for market and product performance assessment."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from .data_loader import MarketRecord


def compute_market_model_summary(records: Iterable[MarketRecord]) -> List[Dict[str, float]]:
    """Summarise key metrics per market and model."""

    aggregates: Dict[Tuple[str, str], Dict[str, float]] = defaultdict(
        lambda: {
            "total_sales": 0.0,
            "total_complaints": 0.0,
            "sum_complaint_rate": 0.0,
            "sum_customer_satisfaction": 0.0,
            "sum_warranty_cost": 0.0,
            "count": 0.0,
        }
    )
    for record in records:
        key = (record.market, record.model)
        agg = aggregates[key]
        agg["total_sales"] += record.sales
        agg["total_complaints"] += record.complaints
        agg["sum_complaint_rate"] += record.complaint_rate
        agg["sum_customer_satisfaction"] += record.customer_satisfaction
        agg["sum_warranty_cost"] += record.warranty_cost
        agg["count"] += 1

    summary: List[Dict[str, float]] = []
    for (market, model), values in aggregates.items():
        count = max(values["count"], 1.0)
        summary.append(
            {
                "market": market,
                "model": model,
                "total_sales": values["total_sales"],
                "total_complaints": values["total_complaints"],
                "avg_complaint_rate": values["sum_complaint_rate"] / count,
                "avg_customer_satisfaction": values[
                    "sum_customer_satisfaction"
                ]
                / count,
                "avg_warranty_cost": values["sum_warranty_cost"] / count,
            }
        )

    summary.sort(key=lambda item: item["avg_complaint_rate"], reverse=True)
    return summary


def identify_problem_hotspots(
    records: Iterable[MarketRecord],
    complaint_rate_threshold: float = 0.07,
    satisfaction_threshold: float = 75,
) -> List[Dict[str, float]]:
    """Highlight market-model combinations that exceed risk thresholds."""

    summary = compute_market_model_summary(records)
    hotspots = [
        row
        for row in summary
        if row["avg_complaint_rate"] >= complaint_rate_threshold
        or row["avg_customer_satisfaction"] <= satisfaction_threshold
    ]
    return hotspots


def evaluate_countermeasure_effectiveness(
    records: Iterable[MarketRecord],
    min_periods: int = 1,
) -> List[Dict[str, float]]:
    """Compare performance metrics before and after countermeasures."""

    records_by_vehicle: Dict[Tuple[str, str], List[MarketRecord]] = defaultdict(list)
    for record in records:
        records_by_vehicle[(record.market, record.model)].append(record)

    results: List[Dict[str, float]] = []
    for (market, model), vehicle_records in records_by_vehicle.items():
        pre_records = [r for r in vehicle_records if not r.is_post_countermeasure]
        post_buckets: Dict[str, List[MarketRecord]] = defaultdict(list)
        for record in vehicle_records:
            if record.is_post_countermeasure and record.countermeasure_id:
                post_buckets[record.countermeasure_id].append(record)

        for countermeasure_id, post_records in post_buckets.items():
            if len(pre_records) < min_periods or len(post_records) < min_periods:
                continue
            pre_count = len(pre_records)
            post_count = len(post_records)
            avg_pre_complaint = sum(r.complaint_rate for r in pre_records) / pre_count
            avg_post_complaint = (
                sum(r.complaint_rate for r in post_records) / post_count
            )
            avg_pre_satisfaction = (
                sum(r.customer_satisfaction for r in pre_records) / pre_count
            )
            avg_post_satisfaction = (
                sum(r.customer_satisfaction for r in post_records) / post_count
            )
            avg_pre_warranty = sum(r.warranty_cost for r in pre_records) / pre_count
            avg_post_warranty = (
                sum(r.warranty_cost for r in post_records) / post_count
            )
            avg_pre_sales = sum(r.sales for r in pre_records) / pre_count
            avg_post_sales = sum(r.sales for r in post_records) / post_count

            results.append(
                {
                    "countermeasure_id": countermeasure_id,
                    "market": market,
                    "model": model,
                    "periods_pre": pre_count,
                    "periods_post": post_count,
                    "complaint_rate_delta": avg_post_complaint - avg_pre_complaint,
                    "customer_satisfaction_delta": avg_post_satisfaction
                    - avg_pre_satisfaction,
                    "warranty_cost_delta": avg_post_warranty - avg_pre_warranty,
                    "sales_delta": avg_post_sales - avg_pre_sales,
                }
            )

    results.sort(key=lambda item: item["complaint_rate_delta"])
    return results


__all__ = [
    "compute_market_model_summary",
    "identify_problem_hotspots",
    "evaluate_countermeasure_effectiveness",
]
