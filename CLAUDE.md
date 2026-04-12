# HarnessKit

Python CLI tool for generating AI Native Repositories.

## Tech Stack
- Python 3.11+ / uv / click + questionary / Jinja2
- Linter: Ruff / Type check: pyright strict / Test: pytest

## Commands
- `make setup` — Initialize dev environment
- `make lint` — Ruff lint check
- `make lint-fix` — Auto-fix lint issues
- `make format` — Ruff format
- `make typecheck` — pyright strict
- `make test` — pytest
- `make check` — lint + typecheck + test (CI)
- `bash scripts/harness-check.sh` — Validate harness practices

## Project Structure
- `src/harnesskit/cli.py` — CLI entry point (click)
- `src/harnesskit/config.py` — ProjectConfig dataclass, enums
- `src/harnesskit/prompts.py` — Interactive TUI prompts
- `src/harnesskit/generator.py` — 4-layer template rendering engine
- `src/harnesskit/templates/` — Jinja2 template tree
- `tests/` — mirrors src structure

## Workflow
1. Run `make check` after changes, before commit
2. Write tests first, then implement
3. Conventional commits: type(scope): description (≤200 chars)

## Boundaries
### Always
- Type hints everywhere, pass pyright strict
- New modules need corresponding tests
- Files under 300 lines (500 warn, 1000 error)
- Run `make lint-fix` before committing

### Ask First
- Adding new dependencies
- Changing template layer structure
- Modifying CI config

### Never
- No `type: ignore` without explaining why
- No hardcoded project names in templates
- No `Any` types
