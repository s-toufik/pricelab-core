from src.domain.models.prediction import Prediction
from src.ports.outbound.binary_serializer import BinarySerializer


class PredictionSerializer(BinarySerializer):
    pass

PredictionSerializer.setup(
    Prediction,
    [
        ("symbol", str, 32),
        ("predicted_price", float, 0),
        ("confidence", float, 0),
        ("horizon_ms", int, 0),
        ("timestamp", int, 0),
    ]
)