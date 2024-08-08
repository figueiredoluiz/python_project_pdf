.PHONY: all build test clean test-coverage

PYTHON = python3.11
PIP = pip

all: build

build:
	$(PIP) install -r requirements.txt
	pyinstaller project-pdf.spec

test:
	$(PYTHON) -m pytest tests/

clean:
	rm -rf dist __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -r {} +

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) src/main.py $(ARGS)

test-coverage:
	coverage run -m pytest tests/
	coverage report
	coverage html