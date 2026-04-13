.PHONY: setup dev lint lint-fix format typecheck test test-cov clean build publish publish-test check harness-check

setup:            ## Initialize dev environment
	uv sync --dev
	uv run pre-commit install --hook-type commit-msg

lint:             ## Ruff lint check
	uv run ruff check src/ tests/

lint-fix:         ## Auto-fix lint issues
	uv run ruff check --fix --unsafe-fixes src/ tests/

format:           ## Ruff format
	uv run ruff format src/ tests/

typecheck:        ## Pyright type check
	uv run pyright src/

test:             ## Run tests
	uv run pytest tests/ -v

test-cov:         ## Run tests + coverage
	uv run pytest tests/ -v --cov=src/harnesskit --cov-report=term-missing

check:            ## Full check (CI use)
	make lint && make typecheck && make test

harness-check:    ## Validate harness engineering practices
	bash scripts/harness-check.sh

clean:            ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info

build:            ## Build distribution
	uv build

publish:          ## Publish to PyPI (with checks and optional git tag)
	bash scripts/publish.sh

publish-test:     ## Publish to TestPyPI (for testing)
	bash scripts/publish.sh --testpypi
