import pytest

from pricelab_core.adapter.outbound.file_handler.handler import Handler

class TestFileHandler:

    @pytest.fixture
    def provider(self):
        return Handler

    def test_read_yaml(self, tmp_path, provider):
        file = tmp_path / "test.yml"

        file.write_text("key: value")

        result = provider(str(file)).read()

        assert isinstance(result, dict)
        assert result["key"] == "value"

    def test_write_yaml(self, tmp_path, provider):
        file = tmp_path / "test.yml"

        data = {"hello": "world"}

        provider(str(file)).write(data)

        result = provider(str(file)).read()

        assert result == data

    def test_read_file_not_found(self, provider):
        with pytest.raises(FileNotFoundError):
            provider("missing.yml").read()

    def test_extension_not_found(self, tmp_path, provider):
        file = tmp_path / "test.foo"
        file.write_text("key: value")
        
        with pytest.raises(NotImplementedError):
                provider(str(file)).read()

        with pytest.raises(NotImplementedError):
                provider(str(file)).write({"key": "value"})
