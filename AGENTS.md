# AGENTS.md

This project follows harness engineering practices. See CLAUDE.md for commands and boundaries.

## Cross-Agent Conventions

### Before Committing
- Run `make check` (lint + typecheck + test)
- Run `make lint-fix` to auto-fix lint issues
- Follow conventional commits: `type(scope): description` (≤200 chars)
- Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

### Code Quality
- Strict types: pyright strict mode, no `Any`
- Keep source files under 300 lines (500 warn, 1000 error)
- Every module in `src/` must have corresponding tests in `tests/`
- CLAUDE.md must stay under 80 lines

### Template Development
- Templates live in `src/harnesskit/templates/` with `.j2` suffix
- Layer order: base → lang/_shared → lang/type → lang/type/framework → addons
- Use `{{ project_name }}`, `{{ project_slug }}` — never hardcode names
- Test every new template type in `tests/test_templates/`

### Validation
- Run `bash scripts/harness-check.sh` for full harness practice validation
