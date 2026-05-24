import os
import dotenv
from pathlib import Path
from pprint import pprint

from pricelab_core.bootstrap.dependency_injection.logging import logger
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


def main() -> None:
    pprint(load_application_configuration())


if __name__ == "__main__":
    main()
