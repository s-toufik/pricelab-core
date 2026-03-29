from adapters.inbound.analytics_cli import AnalyticsCLI
from adapters.outbound.numpy.sequence_analytics_engine import NumpySequenceAnalyticsEngine
from application.use_case.analyse_candles import AnalyseCandles
from application.use_case.analyse_quotes import AnalyseQuotes
from domain.models.candles.candle import Candle
from domain.models.quotes.quote import Quote


engine = NumpySequenceAnalyticsEngine()

def run_quote_usecase():
    use_case = AnalyseQuotes(computation_engine=engine)

    cli = AnalyticsCLI(use_case, {"window": 2})

    quotes = [
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:00:00Z", bid=175.0, ask=175.5, last=175.2,
              volume=1000),
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:01:00Z", bid=175.2, ask=175.6, last=175.4,
              volume=1200),
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:02:00Z", bid=175.4, ask=175.8, last=175.6,
              volume=900),
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:03:00Z", bid=175.6, ask=176.0, last=175.9,
              volume=1100),
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:04:00Z", bid=175.8, ask=176.2, last=176.0,
              volume=950),
        Quote(source="NASDAQ", symbol="AAPL", timestamp="2026-03-30T10:05:00Z", bid=176.0, ask=176.4, last=176.2,
              volume=1050),
    ]

    cli.run(quotes)


def run_candles_usecase():
    use_case = AnalyseCandles(computation_engine=engine)

    cli = AnalyticsCLI(use_case, {"window": 2})

    candles = [
        Candle(symbol="BTC/USD", timestamp="2024-01-01T00:00:00", source="binance",
               open=42000.0, high=43500.0, low=41800.0, close=43200.0, volume=1200.5),
        Candle(symbol="BTC/USD", timestamp="2024-01-01T01:00:00", source="binance",
               open=43200.0, high=44100.0, low=42900.0, close=43800.0, volume=980.3),
        Candle(symbol="BTC/USD", timestamp="2024-01-01T02:00:00", source="binance",
               open=43800.0, high=45200.0, low=43600.0, close=44900.0, volume=1540.7),
        Candle(symbol="BTC/USD", timestamp="2024-01-01T03:00:00", source="binance",
               open=44900.0, high=45500.0, low=44200.0, close=44500.0, volume=870.2),
        Candle(symbol="BTC/USD", timestamp="2024-01-01T04:00:00", source="binance",
               open=44500.0, high=46000.0, low=44300.0, close=45800.0, volume=2100.0),
        Candle(symbol="BTC/USD", timestamp="2024-01-01T05:00:00", source="binance",
               open=45800.0, high=46200.0, low=45100.0, close=45600.0, volume=760.8),
    ]

    cli.run(candles)

def main() -> None:

    run_candles_usecase()

    run_quote_usecase()


if __name__ == "__main__":
    main()
