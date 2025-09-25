"""Command line entry point to run the analysis workflow on the sample data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .analysis import (
    compute_market_model_summary,
    evaluate_countermeasure_effectiveness,
    identify_problem_hotspots,
)
from .data_loader import load_market_performance_data
from .modeling import train_complaint_rate_model


def _format_summary(rows: Iterable[dict]) -> str:
    if not rows:
        return "(no data)"
    headers = list(rows[0].keys())
    lines = [" | ".join(headers)]
    for row in rows:
        formatted = []
        for col in headers:
            value = row[col]
            if isinstance(value, float):
                formatted.append(f"{value:.4f}")
            else:
                formatted.append(str(value))
        lines.append(" | ".join(formatted))
    return "\n".join(lines)


def run_report(data_path: Path) -> None:
    records = load_market_performance_data(data_path)

    print("=== Market & Model Summary ===")
    summary = compute_market_model_summary(records)
    print(_format_summary(summary))

    print("\n=== Problem Hotspots ===")
    hotspots = identify_problem_hotspots(records)
    print(_format_summary(hotspots))

    print("\n=== Countermeasure Effectiveness ===")
    effectiveness = evaluate_countermeasure_effectiveness(records)
    print(_format_summary(effectiveness))

    print("\n=== Complaint Rate Model ===")
    result = train_complaint_rate_model(records)
    print(
        "RMSE: {rmse:.4f} | R^2: {r2:.3f}".format(
            rmse=result.rmse,
            r2=result.r2,
        )
    )


if __name__ == "__main__":
    run_report(Path(__file__).resolve().parents[1] / "data" / "sample_market_performance.csv")
