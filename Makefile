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
