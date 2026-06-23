PYTHON = python3

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py map.txt

debug:
	$(PYTHON) -m pdb main.py

test:
	pytest
	make clean
	clear

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	flake8 . --exclude .venv
	mypy . --exclude '\.venv' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict