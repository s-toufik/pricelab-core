from unittest.mock import patch, MagicMock

from pricelab_core.infrastructure.app_configuration.adapter.load_configuration import (
    LoadConfiguration,
)
from pricelab_core.infrastructure.app_configuration.model.configuration import (
    AppConfiguration,
)

FAKE_CONFIG = {
    "app_configuration": {
        "env": "debug",
        "run": "async",
        "datasource": {},
        "use_case": {},
        "telemetry": {},
    }
}


class TestLoadConfiguration:
    def _reset_singleton(self):
        LoadConfiguration._instance = None

    def _reset_loader(self, loader: LoadConfiguration):
        loader._cached_config = None

    def _mock_handler(self, mock_handler):
        mock_instance = MagicMock()
        mock_instance.read.return_value = FAKE_CONFIG
        mock_handler.return_value = mock_instance
        return mock_instance

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_load_cache(self, mock_handler):
        self._reset_singleton()

        mock_instance = self._mock_handler(mock_handler)
        mock_logger = MagicMock()

        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=mock_logger,
        )

        self._reset_loader(loader)

        result1 = loader.load()
        result2 = loader.load()

        assert isinstance(result1, AppConfiguration)
        assert result1 is result2
        assert mock_instance.read.call_count == 1

        mock_logger.critical.assert_not_called()

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_reload(self, mock_handler):
        self._reset_singleton()

        mock_instance = self._mock_handler(mock_handler)
        mock_logger = MagicMock()

        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=mock_logger,
        )

        self._reset_loader(loader)

        result1 = loader.load()
        result2 = loader.reload()

        assert isinstance(result1, AppConfiguration)
        assert isinstance(result2, AppConfiguration)
        assert result1 is not result2
        assert mock_instance.read.call_count == 2

        mock_logger.critical.assert_not_called()
