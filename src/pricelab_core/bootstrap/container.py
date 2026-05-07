from pricelab_core.adapter.inbound.analytics_cli import AnalyticsCLI
from pricelab_core.application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from pricelab_core.application.use_case.analyse_candles import AnalyseCandlesUseCase
from pricelab_core.application.use_case.analyse_quotes import AnalyseQuotesUseCase
from pricelab_core.bootstrap.common import compute_engine, logger
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote


def build_candles_cli() -> AnalyticsCLI:
    use_case: AnalyseSeriesUseCase[Candle] = AnalyseCandlesUseCase(
        compute_engine,
        logger,
    )
    return AnalyticsCLI(use_case, logger, {"window": 2})


def build_quote_cli() -> AnalyticsCLI:
    use_case: AnalyseSeriesUseCase[Quote] = AnalyseQuotesUseCase(
        compute_engine,
        logger,
    )
    return AnalyticsCLI(use_case, logger, {"window": 2})
