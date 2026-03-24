import pytest

from src.domain.models.prediction import Prediction


class TestPrediction:

    def test_prediction_creation(self):
        prediction = Prediction(
            symbol="foo",
            predicted_price=1,
            confidence=0.2,
            horizon_ms=3,
            timestamp=100
        )

        assert prediction.symbol == "foo"
        assert prediction.predicted_price == 1
        assert prediction.confidence == 0.2
        assert prediction.horizon_ms == 3
        assert prediction.timestamp == 100

    def test_prediction_validation(self):
        with pytest.raises(ValueError):
            Prediction(symbol="foo", predicted_price=-1, confidence=0.2, horizon_ms=3, timestamp=100)
            Prediction(symbol="foo", predicted_price=1, confidence=0.2, horizon_ms=-3, timestamp=100)
            Prediction(symbol="foo", predicted_price=1, confidence=2, horizon_ms=-3, timestamp=-100)
            Prediction(symbol="foo", predicted_price=1, confidence=0.2, horizon_ms=3, timestamp=100)
            Prediction(symbol="", predicted_price=1, confidence=2, horizon_ms=3, timestamp=-100)
