PYTHON = python3

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py 

debug:
	$(PYTHON) -m pdb main.py

test:
	pytest
	make clean

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict