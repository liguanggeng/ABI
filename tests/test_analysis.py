from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analysis import (
    compute_market_model_summary,
    evaluate_countermeasure_effectiveness,
    identify_problem_hotspots,
)
from src.data_loader import load_market_performance_data


def load_records():
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_market_performance.csv"
    return load_market_performance_data(data_path)


def test_summary_contains_expected_keys():
    summary = compute_market_model_summary(load_records())
    assert summary, "summary should not be empty"
    expected_keys = {
        "market",
        "model",
        "total_sales",
        "total_complaints",
        "avg_complaint_rate",
        "avg_customer_satisfaction",
        "avg_warranty_cost",
    }
    assert expected_keys.issubset(summary[0].keys())


def test_hotspot_detection_flags_high_complaint_rate():
    hotspots = identify_problem_hotspots(load_records(), complaint_rate_threshold=0.07)
    assert hotspots, "hotspots should not be empty"
    assert any(row["avg_complaint_rate"] >= 0.07 for row in hotspots)


def test_countermeasure_effectiveness_improves_metrics():
    effectiveness = evaluate_countermeasure_effectiveness(load_records(), min_periods=1)
    assert effectiveness, "effectiveness should not be empty"
    assert any(row["complaint_rate_delta"] < 0 for row in effectiveness)
