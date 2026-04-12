# HarnessKit

Python CLI tool for generating AI Native Repositories.

## Tech Stack
- Python 3.11+ / uv / click + questionary / Jinja2
- Linter: Ruff / Type check: pyright strict / Test: pytest

## Commands
- `make setup` — Initialize dev environment
- `make lint` — Ruff lint
- `make format` — Ruff format (auto-fix)
- `make typecheck` — pyright strict
- `make test` — pytest
- `make check` — lint + typecheck + test (for CI)

## Project Structure
- `src/harnesskit/cli.py` — CLI entry point
- `src/harnesskit/generator.py` — project generation engine
- `src/harnesskit/prompts.py` — interactive TUI prompts
- `src/harnesskit/config.py` — configuration model
- `src/harnesskit/templates/` — Jinja2 template tree
- `tests/` — tests, mirroring src structure

## Workflow
- Plan first, then implement. Use Plan Mode for complex changes.
- Run `make check` after changes, before commit.
- Write tests first, then implement.

## Boundaries
### Always Do
- Use type hints, pass pyright strict
- New modules must have corresponding tests
- Keep files under 300 lines

### Ask First
- Adding new dependencies
- Modifying CI config
- Changing template structure

### Never Do
- No `type: ignore` without comment explaining why
- No hardcoded project names in templates
- No `any` types
