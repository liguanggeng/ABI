from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.data_loader import load_market_performance_data
from src.modeling import ComplaintRateLookupModel, train_complaint_rate_model


def test_model_trains_and_returns_metrics():
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_market_performance.csv"
    records = load_market_performance_data(data_path)
    result = train_complaint_rate_model(records, test_size=0.3, random_state=0)
    assert result.rmse >= 0
    assert -1 <= result.r2 <= 1
    assert isinstance(result.model, ComplaintRateLookupModel)


def test_model_predicts_reasonable_values():
    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_market_performance.csv"
    records = load_market_performance_data(data_path)
    model = train_complaint_rate_model(records, test_size=0.1, random_state=1).model
    predictions = model.predict(records[:3])
    assert len(predictions) == 3
    assert all(0 <= value <= 1 for value in predictions)
