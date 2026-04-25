.PHONY: run test lint

run:
	python -m socbot.cli run --input data/alerts.csv --output out --config config.yaml

test:
	pytest -q

lint:
	ruff check .
