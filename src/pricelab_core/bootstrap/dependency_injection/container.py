import os
from pathlib import Path

import dotenv

from pricelab_core.adapter.inbound.analytics_cli import AnalyticsCLI
from pricelab_core.application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from pricelab_core.application.use_case.analyse_candles import AnalyseCandlesUseCase
from pricelab_core.application.use_case.analyse_quotes import AnalyseQuotesUseCase
from pricelab_core.bootstrap.dependency_injection.common import compute_engine, logger
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote
from pricelab_core.infrastructure.app_configuration.adapter.load_configuration import (
    LoadConfiguration,
)
from pricelab_core.infrastructure.app_configuration.adapter.omega_configuration_reader import (
    OmegaConfigurationReader,
)
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.app_configuration.port.configuration import Configuration
from pricelab_core.infrastructure.app_configuration.port.configuration_reader import (
    ConfigurationReader,
)


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


def load_application_configuration() -> AppConfiguration:
    dotenv.load_dotenv()
    run_type_environment: RunTypeEnvironment = RunTypeEnvironment(os.getenv("APP_ENV", "dev"))
    configuration_directory: Path = Path(os.getenv("CONFIGURATION_DIR", ""))

    logger.info(f"Loading configuration for {run_type_environment} environment")
    if not configuration_directory:
        exception = FileNotFoundError("No configuration file path provided")
        logger.critical(exception.__str__())
        raise exception

    configuration_reader: ConfigurationReader = OmegaConfigurationReader(
        run_type_environment, configuration_directory
    )

    configuration_loader: Configuration = LoadConfiguration(configuration_reader, logger)
    configuration = configuration_loader.load()
    if not configuration:
        exception = ValueError("No configuration loaded")
        logger.critical(exception.__str__())
        raise ValueError("No configuration loaded")

    return configuration
