from typing import cast
from unittest.mock import MagicMock, create_autospec, patch
from pricelab_core.infrastructure.app_configuration.adapter.load_configuration import (
    LoadConfiguration,
)
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.logger.port.logger import Logger

FAKE_CONFIG = {
    "app_configuration": {
        "env": "debug",
        "run": "async",
        "connector": {},
        "operation": {},
        "cronjob": [],
    }
}


class TestLoadConfiguration:
    def setup_method(self):
        LoadConfiguration._instance = None

    @staticmethod
    def _create_logger_mock():
        return create_autospec(Logger, instance=True)

    @staticmethod
    def _mock_handler(mock_handler, config=None):
        if config is None:
            config = FAKE_CONFIG
        handler_instance = MagicMock()
        handler_instance.read.return_value = config
        mock_handler.return_value = handler_instance
        return handler_instance

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_should_cache_configuration(self, mock_handler):
        handler_instance = self._mock_handler(mock_handler)
        logger_mock = self._create_logger_mock()
        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=cast(Logger, logger_mock),
        )
        result1 = loader.load()
        result2 = loader.load()
        assert isinstance(result1, AppConfiguration)
        assert result1 is result2
        handler_instance.read.assert_called_once()
        logger_mock.critical.assert_not_called()

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_should_reload_configuration(self, mock_handler):
        handler_instance = self._mock_handler(mock_handler)
        logger_mock = self._create_logger_mock()
        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=cast(Logger, logger_mock),
        )
        cached_result = loader.load()
        reloaded_result = loader.reload()
        assert isinstance(cached_result, AppConfiguration)
        assert isinstance(reloaded_result, AppConfiguration)
        assert cached_result is not reloaded_result
        assert handler_instance.read.call_count == 2
        logger_mock.critical.assert_not_called()

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_should_return_cached_instance_after_reload(self, mock_handler):
        handler_instance = self._mock_handler(mock_handler)
        logger_mock = self._create_logger_mock()
        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=cast(Logger, logger_mock),
        )
        reloaded = loader.reload()
        cached = loader.load()
        assert reloaded is cached
        handler_instance.read.assert_called_once()

    @patch("pricelab_core.infrastructure.app_configuration.adapter.load_configuration.Handler")
    def test_should_log_critical_when_handler_fails(self, mock_handler):
        handler_instance = MagicMock()
        handler_instance.read.side_effect = RuntimeError("configuration failure")
        mock_handler.return_value = handler_instance
        logger_mock = self._create_logger_mock()
        loader = LoadConfiguration(
            file_path="dummy.yaml",
            logger=cast(Logger, logger_mock),
        )

        result = loader.load()
        assert result is None
        logger_mock.critical.assert_called_once()

    def test_should_behave_as_singleton(self):
        logger_mock = self._create_logger_mock()
        loader1 = LoadConfiguration(
            file_path="config1.yaml",
            logger=cast(Logger, logger_mock),
        )
        loader2 = LoadConfiguration(
            file_path="config2.yaml",
            logger=cast(Logger, logger_mock),
        )
        assert loader1 is loader2
