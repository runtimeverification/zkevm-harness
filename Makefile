UV     := uv
UV_RUN := $(UV) run --


default: check test-unit

all: check cov

.PHONY: clean
clean:
	rm -rf dist .coverage cov-* .mypy_cache .pytest_cache
	find -type d -name __pycache__ -prune -exec rm -rf {} \;

.PHONY: build
build:
	$(UV) build


# Kompilation

kdist: kdist-build

.PHONY: kdist-build
kdist-build:
	$(UV_RUN) kdist --verbose build -j4 'zkevm-semantics.*'

.PHONY: kdist-clean
kdist-clean:
	$(UV_RUN) kdist clean


# Tests

TEST_ARGS :=

test: test-all

.PHONY: test-all
test-all:
	$(UV_RUN) pytest src/tests --maxfail=1 --verbose --durations=0 --numprocesses=4 --dist=worksteal $(TEST_ARGS)

.PHONY: test-unit
test-unit:
	$(UV_RUN) pytest src/tests/unit --maxfail=1 --verbose $(TEST_ARGS)

.PHONY: test-integration
test-integration:
	$(UV_RUN) pytest src/tests/integration --maxfail=1 --verbose --durations=0 --numprocesses=4 --dist=worksteal $(TEST_ARGS)


# Coverage

COV_ARGS :=

cov: cov-all

cov-%: TEST_ARGS += --cov=zkevm_harness --no-cov-on-fail --cov-branch --cov-report=term

cov-all: TEST_ARGS += --cov-report=html:cov-all-html $(COV_ARGS)
cov-all: test-all

cov-unit: TEST_ARGS += --cov-report=html:cov-unit-html $(COV_ARGS)
cov-unit: test-unit

cov-integration: TEST_ARGS += --cov-report=html:cov-integration-html $(COV_ARGS)
cov-integration: test-integration


# Checks and formatting

format: autoflake isort black
check: check-flake8 check-mypy check-autoflake check-isort check-black

.PHONY: check-flake8
check-flake8:
	$(UV_RUN) flake8 src

.PHONY: check-mypy
check-mypy:
	$(UV_RUN) mypy src

.PHONY: autoflake
autoflake:
	$(UV_RUN) autoflake --quiet --in-place src

.PHONY: check-autoflake
check-autoflake:
	$(UV_RUN) autoflake --quiet --check src

.PHONY: isort
isort:
	$(UV_RUN) isort src

.PHONY: check-isort
check-isort:
	$(UV_RUN) isort --check src

.PHONY: black
black:
	$(UV_RUN) black src

.PHONY: check-black
check-black:
	$(UV_RUN) black --check src


# Optional tools

SRC_FILES := $(shell find src -type f -name '*.py')

.PHONY: pyupgrade
pyupgrade:
	$(UV_RUN) pyupgrade --py310-plus $(SRC_FILES)
