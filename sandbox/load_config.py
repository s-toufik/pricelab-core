from pprint import pprint

from pricelab_core.bootstrap.dependency_injection.container import load_application_configuration
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration


def run_load_configuration() -> AppConfiguration:
    return load_application_configuration()


def main() -> None:
    pprint(run_load_configuration())


if __name__ == "__main__":
    main()
