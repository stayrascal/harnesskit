# HarnessKit — AI Native Repository Generator

## Design Spec

**Date**: 2026-04-12
**Author**: stayrascal
**Status**: Draft

---

## 1. Overview

### 1.1 What is HarnessKit?

A Python CLI tool that helps users quickly scaffold **AI code agent-friendly project repositories**. The generated repositories are not agent projects themselves — they are normal software projects with structure, tooling, and conventions optimized for AI code agents (Claude Code, Cursor, Trae, etc.) to work efficiently.

Core philosophy from Harness Engineering: **Let the repo's structure, type system, lint rules, and test cases "teach" the AI, rather than piling up documentation.**

### 1.2 Installation & Usage

```bash
pip install harnesskit

# Full command
harnesskit new myproject

# Short alias
hk new myproject
```

### 1.3 What This Is NOT

- Not a cookiecutter/copier wrapper — it's a standalone generator with its own template engine
- Not an agent framework — generated repos are normal projects, not AI agent projects
- Not an SDD tool — it does not enforce spec-driven development workflows
- Not opinionated about AI models — works with any code agent

---

## 2. Architecture

### 2.1 Tech Stack (HarnessKit itself)

HarnessKit itself is a Python CLI Library project that follows the same harness engineering practices it generates.

| Dimension | Choice | Rationale |
|---|---|---|
| Package management & build | **uv** | Extremely fast (Rust), replaces pip/poetry/pdm, supports lockfile, virtualenv, publishing |
| Project metadata | **pyproject.toml (PEP 621)** | Single config file, uv native support |
| Linter | **Ruff** | 10-100x faster than flake8, fast AI feedback loop |
| Formatter | **Ruff format** | Replaces Black, unified with Ruff lint |
| Type checking | **pyright strict** | Faster than mypy, strict mode ensures type completeness |
| Testing | **pytest + pytest-cov** | AI's most familiar Python test framework |
| Pre-commit | **pre-commit framework** | ruff check, ruff format, pyright, commitlint |
| Commit convention | **Conventional Commits + commitlint** | Relaxed to 200 chars, AI-compatible |
| CLI framework | **click** | Mature, stable, good composability |
| Interactive TUI | **questionary** | Arrow-key selection, space-toggle checkboxes, based on prompt_toolkit |
| Template engine | **Jinja2** | Mature, stable, harnesskit's only heavy dependency |
| Rich output | **rich** | Beautiful terminal output, progress bars, tables |
| CI | **GitHub Actions** | Community standard, highest AI familiarity |

### 2.2 HarnessKit Project Structure

```
harnesskit/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # lint + type-check + test
│       └── release.yml            # publish to PyPI
├── .pre-commit-config.yaml        # pre-commit hooks config
├── CLAUDE.md                      # harnesskit's own AI instructions
├── AGENTS.md                      # cross-agent instructions → references CLAUDE.md
├── Makefile                       # unified command entry
├── pyproject.toml                 # uv + project metadata + ruff/pyright config
├── uv.lock                        # lockfile
├── README.md
├── docs/
│   └── adr/                       # Architecture Decision Records
│       └── 001-template-engine.md
├── src/
│   └── harnesskit/
│       ├── __init__.py
│       ├── __main__.py            # python -m harnesskit entry
│       ├── cli.py                 # click command definitions
│       ├── generator.py           # generation engine core
│       ├── config.py              # config model (dataclass)
│       ├── prompts.py             # questionary interactive logic
│       ├── addons/
│       │   ├── __init__.py
│       │   ├── base.py            # Addon base class
│       │   ├── cicd.py
│       │   ├── docker.py
│       │   ├── agent_project.py
│       │   └── devcontainer.py
│       └── templates/             # Jinja2 templates
│           ├── base/              # shared base files
│           │   ├── CLAUDE.md.j2
│           │   ├── AGENTS.md.j2
│           │   ├── Makefile.j2
│           │   ├── .gitignore.j2
│           │   └── README.md.j2
│           ├── python/
│           │   ├── _shared/       # Python shared templates
│           │   │   ├── pyproject.toml.j2
│           │   │   ├── .pre-commit-config.yaml.j2
│           │   │   └── ruff.toml.j2
│           │   ├── library/
│           │   ├── cli_tool/
│           │   ├── microservice/
│           │   └── web_app/
│           └── typescript/
│               ├── _shared/       # TS shared templates
│               │   ├── package.json.j2
│               │   ├── tsconfig.json.j2
│               │   └── biome.json.j2
│               ├── library/
│               ├── cli_tool/
│               ├── microservice/
│               └── web_app/
│                   ├── react/
│                   ├── vue/
│                   ├── hono_jsx/
│                   └── none/
└── tests/
    ├── conftest.py
    ├── test_cli.py
    ├── test_generator.py
    ├── test_addons/
    └── test_templates/            # template rendering snapshot tests
```

### 2.3 HarnessKit's Own Makefile

```makefile
.PHONY: setup dev lint format typecheck test test-cov clean build publish check

setup:            ## Initialize dev environment
	uv sync --dev

lint:             ## Ruff lint check
	uv run ruff check src/ tests/

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

clean:            ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info

build:            ## Build distribution
	uv build

publish:          ## Publish to PyPI
	uv publish
```

### 2.4 HarnessKit's Own CLAUDE.md

```markdown
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
- `src/harnesskit/addons/` — optional addon modules
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
```

### 2.5 pyproject.toml

```toml
[project]
name = "harnesskit"
version = "0.1.0"
description = "AI Native Repository Generator"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
    "click>=8.1",
    "questionary>=2.0",
    "jinja2>=3.1",
    "rich>=13.0",
]

[project.scripts]
harnesskit = "harnesskit.cli:main"
hk = "harnesskit.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pyright>=1.1",
    "ruff>=0.8",
    "pre-commit>=4.0",
]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM", "TCH"]

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 3. User Interaction Flow

```
$ hk new myproject

🔧 HarnessKit — AI Native Repository Generator

? Project name: myproject
? Description: My awesome project
? Author: kuaige

? Language:
  ❯ Python
    TypeScript

? Project type:
  ❯ Library
    CLI Tool
    Microservice
    Web App

# Only shown when TypeScript + Web App is selected:
? Frontend framework:
  ❯ React (Vite + React)
    Vue (Vite + Vue)
    Hono JSX (lightweight SSR)
    None (API + static files only)

? Select addons: (space to toggle)
  ◉ CI/CD (GitHub Actions)
  ◯ Docker Compose
  ◯ Agent Project (.claude/skills, agents, hooks)
  ◯ DevContainer

? Git: Initialize repo and make first commit? (Y/n)

✨ Created myproject/ with Python + Microservice template
   Addons: ci

👉 Next steps:
   cd myproject
   make setup
   make dev
```

### 3.1 Smart Defaults

| Project Type | Pre-selected Addons |
|---|---|
| Library | CI/CD |
| CLI Tool | CI/CD |
| Microservice | CI/CD, Docker Compose |
| Web App | CI/CD |

---

## 4. Template Layer Model

Generated projects are composed of three layers:

```
Layer 1: base/              → Files every project gets
Layer 2: {lang}/{type}/     → Language + project type specific files
Layer 3: addons/            → User-selected optional components
```

### 4.1 Layer 1: Base (All Projects)

| File | Content |
|---|---|
| `CLAUDE.md` | Project-level AI instructions (varies by lang/type, see §4.5) |
| `AGENTS.md` | One line pointing to CLAUDE.md + cross-agent conventions |
| `Makefile` | Unified command entry (setup, dev, lint, format, typecheck, test, check) |
| `.gitignore` | Language-specific (Python / Node+Bun) |
| `README.md` | Project name, description, quick start, directory structure |
| `docs/adr/000-template.md` | ADR template for recording architecture decisions |
| `docs/architecture.md` | Project architecture overview (AI's map) |
| `LICENSE` | MIT (default) |

### 4.2 Layer 2: Language + Project Type

#### Python Ecosystem

All Python projects share:

| File | Description |
|---|---|
| `pyproject.toml` | uv + PEP 621, with ruff/pyright config |
| `uv.lock` | Lockfile (generated on `make setup`) |
| `.pre-commit-config.yaml` | ruff check + ruff format + pyright + commitlint |
| `.python-version` | `3.11` |

#### TypeScript Ecosystem (Bun)

All TypeScript projects share:

| File | Description |
|---|---|
| `package.json` | Scripts: lint, format, typecheck, test, dev, build |
| `tsconfig.json` | strict: true |
| `biome.json` | Biome lint + format config (replaces ESLint + Prettier) |
| `.pre-commit-config.yaml` | biome check + tsc --noEmit + commitlint |
| `bun.lock` | Bun lockfile |

All TS Makefile commands use `bun`:

```makefile
setup:       bun install
dev:         bun run --hot src/index.ts
lint:        bun run biome check src/
format:      bun run biome format --write src/
typecheck:   bun run tsc --noEmit
test:        bun test
check:       make lint && make typecheck && make test
build:       bun build src/index.ts --outdir dist
```

### 4.3 The 8 Base Combinations

#### Python Library

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   └── core.py              # Example module (~50 lines)
├── tests/
│   └── test_core.py         # Example test as pattern reference
├── pyproject.toml            # build-system = hatchling
└── ...base layer files
```

- Makefile targets: `setup`, `lint`, `format`, `typecheck`, `test`, `test-cov`, `check`, `build`, `publish`
- No `dev` or `healthcheck`

#### Python CLI Tool

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   ├── __main__.py           # python -m entry
│   ├── cli.py                # click example command
│   └── core.py
├── tests/
│   ├── test_cli.py           # CLI test example (click.testing.CliRunner)
│   └── test_core.py
├── pyproject.toml            # [project.scripts] entry
└── ...
```

- Extra dependency: `click`
- Makefile adds `run` target

#### Python Microservice

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   ├── app.py                # FastAPI example app
│   ├── routes/
│   │   ├── __init__.py
│   │   └── health.py         # GET /healthz
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── config.py             # pydantic-settings config
├── tests/
│   ├── test_health.py        # Integration test example
│   └── conftest.py           # httpx AsyncClient fixture
├── pyproject.toml
├── Dockerfile
└── scripts/
    └── test-e2e.sh           # Start server → healthcheck → run tests → stop server
```

- Dependencies: `fastapi`, `uvicorn`, `pydantic-settings`, `structlog`, `httpx` (test)
- Makefile adds: `dev` (uvicorn --reload), `test-e2e`, `docker-build`, `docker-run`
- Default structured logging (structlog, JSON output)
- Built-in healthcheck endpoint

#### Python Web App

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   ├── app.py                # FastAPI + Jinja2 templates
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── pages.py          # Page routes example
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   └── index.html        # Jinja2 template example
│   └── config.py
├── tests/
│   ├── test_health.py
│   └── test_pages.py
├── pyproject.toml
├── Dockerfile
└── scripts/
    └── test-e2e.sh
```

- Similar to Microservice, adds `static/` and `templates/`
- Extra dependency: `jinja2` (FastAPI template rendering)

#### TypeScript Library

```
myproject/
├── src/
│   ├── index.ts              # Export entry
│   └── core.ts               # Example module
├── tests/
│   └── core.test.ts          # bun test example
├── package.json
├── tsconfig.json
├── biome.json
└── ...base layer files
```

- Test: `bun test`
- Build: `bun build`
- Makefile: `setup`, `lint`, `format`, `typecheck`, `test`, `check`, `build`

#### TypeScript CLI Tool

```
myproject/
├── src/
│   ├── index.ts
│   ├── cli.ts                # commander example command
│   └── core.ts
├── tests/
│   ├── cli.test.ts
│   └── core.test.ts
├── package.json              # "bin" field
└── ...
```

- Extra dependency: `commander`
- `package.json` has `bin` field

#### TypeScript Microservice

```
myproject/
├── src/
│   ├── index.ts              # App startup entry
│   ├── app.ts                # Hono app config
│   ├── routes/
│   │   ├── index.ts
│   │   └── health.ts         # GET /healthz
│   ├── services/
│   │   └── index.ts
│   ├── models/
│   │   └── index.ts
│   └── config.ts             # Env config (zod validation)
├── tests/
│   ├── health.test.ts        # Integration test
│   └── setup.ts              # Test setup
├── package.json
├── Dockerfile
└── scripts/
    └── test-e2e.sh
```

- Framework: Hono (lightweight, high AI familiarity, Express-like API)
- Config validation: zod
- Structured logging: pino
- Makefile adds: `dev`, `test-e2e`, `docker-build`, `docker-run`

#### TypeScript Web App

Depends on frontend framework choice:

**React variant:**

```
myproject/
├── src/
│   ├── main.tsx              # React entry
│   ├── App.tsx               # Root component
│   ├── components/
│   │   └── HelloWorld.tsx    # Example component
│   ├── pages/
│   │   └── Home.tsx
│   └── vite-env.d.ts
├── public/
│   └── index.html
├── tests/
│   └── App.test.tsx
├── vite.config.ts
├── package.json
└── ...
```

- Vite + React 18 + TypeScript
- Dependencies: `react`, `react-dom`, `vite`, `@vitejs/plugin-react`

**Vue variant:**

```
myproject/
├── src/
│   ├── main.ts               # Vue entry
│   ├── App.vue                # Root component
│   ├── components/
│   │   └── HelloWorld.vue     # Example component
│   ├── pages/
│   │   └── Home.vue
│   └── vite-env.d.ts
├── public/
│   └── index.html
├── tests/
│   └── App.test.ts
├── vite.config.ts
├── package.json
└── ...
```

- Vite + Vue 3 + TypeScript
- Dependencies: `vue`, `vite`, `@vitejs/plugin-vue`

**Hono JSX variant:**

```
myproject/
├── src/
│   ├── index.ts
│   ├── app.ts                 # Hono app
│   ├── routes/
│   │   ├── index.ts
│   │   ├── health.ts
│   │   └── pages.ts
│   ├── views/
│   │   └── index.tsx          # Hono JSX template
│   ├── public/
│   │   └── style.css
│   └── config.ts
├── tests/
│   ├── health.test.ts
│   └── pages.test.ts
├── package.json
├── Dockerfile
└── scripts/
    └── test-e2e.sh
```

- Server-side rendering with Hono's built-in JSX
- No Vite, lightweight

**None variant:**

- Same as TS Microservice + `public/` directory for static files

### 4.4 Frontend Framework Choice (TS Web App Only)

| Option | Scaffolding | Key Deps |
|---|---|---|
| **React** | Vite + React 18 + TS | react, react-dom, vite |
| **Vue** | Vite + Vue 3 + TS | vue, vite |
| **Hono JSX** | Hono built-in JSX (SSR) | hono |
| **None** | Hono + static files | hono |

Python Web App does not offer frontend framework choice — Python frontend ecosystem is immature; FastAPI + Jinja2 templates is sufficient. Users wanting a full frontend can pair a Python Microservice with a separate TS Web App.

### 4.5 CLAUDE.md Template Content Strategy

Follows the "minimize documentation" principle. CLAUDE.md is differentiated by project type but kept under **80 lines**:

```markdown
# {{ project_name }}

{{ description }}

## Tech Stack
{{ auto-generated by language/type, with version numbers }}

## Commands
- `make setup` — Initialize environment
- `make lint` — Lint check
- `make format` — Auto format
- `make typecheck` — Type check
- `make test` — Run tests
- `make check` — Full check (lint + typecheck + test)
{% if project_type in ['microservice', 'web_app'] %}
- `make dev` — Start dev server
- `make test-e2e` — End-to-end test
{% endif %}

## Project Structure
{{ auto-generated directory description }}

## Workflow
- Plan first, then implement. Use Plan Mode for complex changes.
- Run `make check` after changes, before commit.
- Write/update tests first, then implement feature.

## Boundaries
### Always Do
- Strict types ({{ 'pyright strict' if python else 'tsconfig strict' }})
- New modules must have corresponding tests
- Keep files under 300 lines
- Commit format: type(scope): description (≤200 chars)

### Ask First
- Adding new dependencies
- Modifying CI configuration
- Deleting public APIs

### Never Do
- No hardcoded secrets or passwords
- No skipping pre-commit hooks
- {{ 'No type: ignore without comment' if python else 'No @ts-ignore or any' }}
```

### 4.6 Layer 3: Addons

| Addon | Generated Files | Trigger |
|---|---|---|
| **CI/CD** | `.github/workflows/ci.yml` (lint + typecheck + test + harness-check), `.github/workflows/ai-review.yml` (AI code review, configurable model) | User selects |
| **Docker Compose** | `docker-compose.yml` (postgres + redis example), Makefile appends `infra-up` / `infra-down` targets | User selects |
| **Agent Project** | `.claude/skills/fix-issue/SKILL.md`, `.claude/skills/review-code/SKILL.md`, `.claude/agents/security-reviewer.md`, `.claude/settings.json` (hooks config) | User selects |
| **DevContainer** | `.devcontainer/devcontainer.json` | User selects |

---

## 5. harness-check Script

Generated with every project. Runs as part of CI and can be added to pre-commit. Checks harness engineering conventions that standard linters cannot cover.

### 5.1 Check Items

| Check | Severity | Rule |
|---|---|---|
| File size | warning >500 lines, error >1000 lines | Source files only (excludes tests, types, config, lockfiles) |
| CLAUDE.md exists | error | Root directory must have CLAUDE.md |
| Directory naming | warning | `src/` subdirs must follow snake_case (Python) or kebab-case (TypeScript) |
| Test coverage | warning | Each `src/` module should have a corresponding test file in `tests/` |
| Type annotation (Python) | warning | Public functions must have type hints |
| no-any check (TypeScript) | warning | Scans for `: any` occurrences |
| Duplicate code detection | info | Uses basic AST comparison for obvious duplicates |

### 5.2 Output Format

Structured, parseable error messages so code agents can auto-fix:

```
harness-check: ERROR  src/myproject/routes/api.py:1-523 — File exceeds 500 line limit (523 lines). Consider splitting by responsibility.
harness-check: WARN   src/myproject/utils.py — Missing test file. Expected: tests/test_utils.py
harness-check: ERROR  CLAUDE.md not found in project root.
```

---

## 6. CI/CD Addon Detail

### 6.1 ci.yml (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Language-specific setup (uv for Python, bun for TS)
      - name: Lint
        run: make lint
      - name: Type Check
        run: make typecheck
      - name: Test
        run: make test
      - name: Harness Check
        run: make harness-check
```

### 6.2 ai-review.yml (AI Code Review)

Template for PR-triggered AI code review. Uses `claude -p` in non-interactive mode to review PR diffs:

```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Get PR diff
        run: git diff origin/${{ github.base_ref }}...HEAD > /tmp/pr.diff
      - name: AI Review
        run: |
          cat /tmp/pr.diff | claude -p \
            "Review this PR diff. Check for: bugs, security issues, \
             missing tests, harness convention violations (file size, \
             type safety, naming). Be concise." \
            --output-format json > review.json
      # Post review as PR comment (configurable)
```

Users configure their API key and preferred model in repository secrets.

---

## 7. Design Principles

### 7.1 From the AI Native Repository Article

Key principles absorbed into harnesskit's template design:

1. **Code is infrastructure, documentation is supplement** — Type systems, lint rules, test cases, clear directory structure are the "living documentation" that never goes stale. CLAUDE.md is icing, not foundation.
2. **Automate over document** — Coding conventions go into linter rules, not CLAUDE.md. Format goes to Prettier/Ruff/Biome, not documentation.
3. **Fast feedback loops** — High-performance linters (Ruff, Biome) and fast test runners (bun test, pytest) keep the AI's generate → check → fix cycle fast.
4. **File size control** — Default 300 lines, warn at 500, error at 1000. AI understands small, focused files better.
5. **Strict types** — pyright strict / tsconfig strict. Types are AI's best friend for understanding code.
6. **Example code as pattern reference** — One good example > 100 lines of spec documentation.
7. **Commit convention adapted for AI** — Relaxed to 200 chars. AI tends to generate descriptive commit messages.
8. **Plan-first workflow** — Encouraged in CLAUDE.md, not enforced by tooling. No SDD tool dependency.

### 7.2 What We Explicitly Don't Do

- **No SDD/OpenSpec/OPSX integration** — Plan-first habit is encouraged in CLAUDE.md, but no spec-driven development tool dependency. SDD adds document bloat that conflicts with our "minimize documentation" principle.
- **No Codified Context heavy documentation** — We target <5% doc-to-code ratio, not 24.2%.
- **No .cursorrules** — AGENTS.md is the cross-agent standard; tool-specific files can reference it.
- **No framework opinions for Python web** — FastAPI + Jinja2 is sufficient; Python frontend frameworks are immature.

---

## 8. Implementation Milestones

### Phase 1: Core CLI + Python Templates (MVP)

- [ ] Project scaffolding: `hk new` with interactive prompts
- [ ] Python Library template
- [ ] Python CLI Tool template
- [ ] Python Microservice template
- [ ] Python Web App template
- [ ] Base layer: CLAUDE.md, AGENTS.md, Makefile, .gitignore, README.md
- [ ] harness-check script
- [ ] Pre-commit configuration
- [ ] Git init + first commit
- [ ] Unit tests for generator and templates

### Phase 2: TypeScript Templates

- [ ] TypeScript Library template (bun)
- [ ] TypeScript CLI Tool template (bun + commander)
- [ ] TypeScript Microservice template (bun + Hono)
- [ ] TypeScript Web App template with framework choice (React / Vue / Hono JSX / None)
- [ ] Bun ecosystem integration across all TS templates

### Phase 3: Addons

- [ ] CI/CD addon (GitHub Actions)
- [ ] AI Code Review addon
- [ ] Docker Compose addon
- [ ] Agent Project addon (.claude/skills, agents, hooks)
- [ ] DevContainer addon

### Phase 4: Polish & Publish

- [ ] `hk list` — list available templates and addons
- [ ] `hk check` — run harness-check on current project (standalone use)
- [ ] Comprehensive tests (snapshot tests for all 8+ template combinations)
- [ ] Documentation (README, examples)
- [ ] PyPI publish workflow
- [ ] Future: Claude Code skill wrapper (`/hk-init`)

---

## 9. Open Questions (Resolved)

| Question | Resolution |
|---|---|
| cookiecutter dependency? | No. Standalone Jinja2 generator. |
| SDD/OpenSpec integration? | No. Plan-first encouraged in CLAUDE.md, not enforced by tools. |
| .cursorrules? | No. AGENTS.md only. |
| Which TS runtime? | Bun for all TS projects. |
| Frontend framework choice? | Yes, for TS Web App only. React / Vue / Hono JSX / None. |
| File size limits? | 300 recommended, 500 warn, 1000 error. |
| CLAUDE.md length? | Under 80 lines. Minimal documentation principle. |

---

## 10. References

- [Harness Engineering — OpenAI](https://openai.com/index/harness-engineering/) — Agent-first development paradigm
- [How to Write a Great agents.md — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) — 2500+ repo analysis
- [Best Practices for Claude Code — Anthropic](https://code.claude.com/docs/en/best-practices) — Claude Code official best practices
- [Improve Your AI Code Output with AGENTS.md — Builder.io](https://www.builder.io/blog/agents-md) — AGENTS.md practical tips
- [Claude Code's Technology Picks — Amplifying AI](https://amplifying.ai/research/claude-code-picks/report) — AI model tech stack preferences
