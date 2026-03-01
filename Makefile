.PHONY: install install-dev run test lint format typecheck check

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app tests

check: lint typecheck test
