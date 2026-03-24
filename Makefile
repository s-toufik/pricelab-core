venv:
	uv venv

install:
	uv sync

install_dev:
	uv sync --group dev

run:
	uv run uvicorn price.main:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

build:
	rm -rf dist
	rm -rf src/*.egg-info
	uv build

publish_dev:
	UV_PUBLISH_TOKEN=$$TEST_PYPI_TOKEN
	uv publish --publish-url https://test.pypi.org/legacy/

publish:
	@echo "INFO: Make sure that UV_PUBLISH_TOKEN env variable is set"
	UV_PUBLISH_TOKEN=$$RELEASE_PYPI_TOKEN
	uv publish

