from src.domain.models.market_price import MarketPrice
from src.ports.outbound.binary_serializer import BinarySerializer


class MarketPriceBinarySerializer(BinarySerializer):
    pass

MarketPriceBinarySerializer.setup(
    MarketPrice,
    [
        ("source", str, 32),
        ("symbol", str, 0),
        ("timestamp", int, 0),
        ("bid", float, 0),
        ("ask", float, 0),
        ("last", float, 0),
        ("volume", float, 0)
    ]
)