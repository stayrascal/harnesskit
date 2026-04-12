# HarnessKit Phase 1 — Core CLI + Python Templates MVP

## Implementation Plan

**Date**: 2026-04-12
**Spec**: `docs/specs/2026-04-12-harnesskit-design.md`
**Goal**: Deliver a working `hk new` command that generates all 4 Python project types with full harness engineering setup.

---

## Plan Header

### Goal
Ship `hk new myproject` → interactive CLI → generates Python Library / CLI Tool / Microservice / Web App with CLAUDE.md, AGENTS.md, Makefile, .gitignore, README.md, harness-check, pre-commit, pyproject.toml, and git init + first commit.

### Architecture
```
CLI (click) → Prompts (questionary) → Config (dataclass) → Generator (Jinja2) → Git init
```

### Tech Stack
- Python 3.11+ / uv / click / questionary / Jinja2 / rich
- Linter: Ruff / Type check: pyright strict / Test: pytest
- Pre-commit: ruff + pyright + commitlint

---

## File Structure (Final State after Phase 1)

```
harnesskit/
├── .github/workflows/ci.yml
├── .pre-commit-config.yaml
├── .python-version
├── CLAUDE.md
├── AGENTS.md
├── Makefile
├── pyproject.toml
├── README.md
├── docs/
│   ├── adr/
│   │   └── 001-template-engine.md
│   └── specs/
│       ├── 2026-04-12-harnesskit-design.md
│       └── 2026-04-12-harnesskit-phase1-plan.md
├── src/
│   └── harnesskit/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── generator.py
│       ├── prompts.py
│       └── templates/
│           ├── base/
│           │   ├── CLAUDE.md.j2
│           │   ├── AGENTS.md.j2
│           │   ├── Makefile.j2
│           │   ├── .gitignore.j2
│           │   ├── README.md.j2
│           │   ├── LICENSE.j2
│           │   ├── docs/
│           │   │   ├── adr/
│           │   │   │   └── 000-template.md.j2
│           │   │   └── architecture.md.j2
│           │   └── scripts/
│           │       └── harness-check.sh.j2
│           └── python/
│               ├── _shared/
│               │   ├── pyproject.toml.j2
│               │   ├── .pre-commit-config.yaml.j2
│               │   └── .python-version.j2
│               ├── library/
│               │   ├── src/{{project_slug}}/__init__.py.j2
│               │   ├── src/{{project_slug}}/core.py.j2
│               │   └── tests/test_core.py.j2
│               ├── cli_tool/
│               │   ├── src/{{project_slug}}/__init__.py.j2
│               │   ├── src/{{project_slug}}/__main__.py.j2
│               │   ├── src/{{project_slug}}/cli.py.j2
│               │   ├── src/{{project_slug}}/core.py.j2
│               │   ├── tests/test_cli.py.j2
│               │   └── tests/test_core.py.j2
│               ├── microservice/
│               │   ├── src/{{project_slug}}/__init__.py.j2
│               │   ├── src/{{project_slug}}/app.py.j2
│               │   ├── src/{{project_slug}}/config.py.j2
│               │   ├── src/{{project_slug}}/routes/__init__.py.j2
│               │   ├── src/{{project_slug}}/routes/health.py.j2
│               │   ├── src/{{project_slug}}/models/__init__.py.j2
│               │   ├── src/{{project_slug}}/services/__init__.py.j2
│               │   ├── tests/conftest.py.j2
│               │   ├── tests/test_health.py.j2
│               │   ├── Dockerfile.j2
│               │   └── scripts/test-e2e.sh.j2
│               └── web_app/
│                   ├── src/{{project_slug}}/__init__.py.j2
│                   ├── src/{{project_slug}}/app.py.j2
│                   ├── src/{{project_slug}}/config.py.j2
│                   ├── src/{{project_slug}}/routes/__init__.py.j2
│                   ├── src/{{project_slug}}/routes/health.py.j2
│                   ├── src/{{project_slug}}/routes/pages.py.j2
│                   ├── src/{{project_slug}}/static/style.css.j2
│                   ├── src/{{project_slug}}/templates/index.html.j2
│                   ├── tests/conftest.py.j2
│                   ├── tests/test_health.py.j2
│                   ├── tests/test_pages.py.j2
│                   ├── Dockerfile.j2
│                   └── scripts/test-e2e.sh.j2
└── tests/
    ├── conftest.py
    ├── test_cli.py
    ├── test_config.py
    ├── test_generator.py
    ├── test_prompts.py
    └── test_templates/
        ├── test_python_library.py
        ├── test_python_cli_tool.py
        ├── test_python_microservice.py
        └── test_python_web_app.py
```

---

## Tasks

### Task 1: Project Scaffolding — harnesskit itself

**Goal**: Initialize harnesskit as a uv-managed Python project with all harness engineering practices.

#### Step 1.1: Create pyproject.toml

**File**: `pyproject.toml`

```toml
[project]
name = "harnesskit"
version = "0.1.0"
description = "AI Native Repository Generator"
requires-python = ">=3.11"
license = "MIT"
authors = [{ name = "kuaige" }]
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
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM", "TCH"]

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
include = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.hatch.build.targets.wheel]
packages = ["src/harnesskit"]
```

#### Step 1.2: Create Makefile

**File**: `Makefile`

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

#### Step 1.3: Create CLAUDE.md

**File**: `CLAUDE.md`

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

#### Step 1.4: Create AGENTS.md, .pre-commit-config.yaml, .python-version, .github/workflows/ci.yml, README.md

**File**: `AGENTS.md`

```markdown
# AGENTS.md

This project uses harness engineering practices. See CLAUDE.md for full details.

## Cross-Agent Conventions
- Run `make check` before committing
- Follow conventional commits: type(scope): description (≤200 chars)
- Keep files under 300 lines
- Strict types: pyright strict mode
```

**File**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/RobertCraiwordie/pyright-python
    rev: v1.1.390
    hooks:
      - id: pyright
        additional_dependencies:
          - click>=8.1
          - questionary>=2.0
          - jinja2>=3.1
          - rich>=13.0
          - pytest>=8.0

  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.18.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
```

**File**: `.python-version`

```
3.11
```

**File**: `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --dev
      - name: Lint
        run: make lint
      - name: Type Check
        run: make typecheck
      - name: Test
        run: make test
```

**Verify**: All scaffolding files exist.

```bash
ls pyproject.toml Makefile CLAUDE.md AGENTS.md .pre-commit-config.yaml .python-version .github/workflows/ci.yml README.md
```

**Commit**: `feat: initialize harnesskit project scaffolding`

---

### Task 2: Config Model — `src/harnesskit/config.py`

**Goal**: Define the dataclass that holds all user selections. This is the contract between prompts and generator.

#### Step 2.1: Write failing test

**File**: `tests/test_config.py`

```python
"""Tests for harnesskit config model."""

from harnesskit.config import Language, ProjectConfig, ProjectType


def test_project_config_creation() -> None:
    """ProjectConfig can be created with required fields."""
    config = ProjectConfig(
        project_name="myproject",
        description="Test project",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_name == "myproject"
    assert config.project_slug == "myproject"
    assert config.language == Language.PYTHON
    assert config.project_type == ProjectType.LIBRARY
    assert config.addons == []
    assert config.git_init is True


def test_project_slug_normalizes_dashes() -> None:
    """Project slug converts dashes to underscores for Python."""
    config = ProjectConfig(
        project_name="my-cool-project",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_slug == "my_cool_project"


def test_project_slug_keeps_dashes_for_typescript() -> None:
    """Project slug keeps dashes for TypeScript (kebab-case)."""
    config = ProjectConfig(
        project_name="my-cool-project",
        description="",
        author="testuser",
        language=Language.TYPESCRIPT,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_slug == "my-cool-project"


def test_project_config_with_addons() -> None:
    """ProjectConfig accepts addon list."""
    config = ProjectConfig(
        project_name="myproject",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.MICROSERVICE,
        addons=["cicd", "docker"],
    )
    assert config.addons == ["cicd", "docker"]


def test_default_addons_for_microservice() -> None:
    """Microservice should have cicd and docker as default addons."""
    defaults = ProjectConfig.default_addons(ProjectType.MICROSERVICE)
    assert "cicd" in defaults
    assert "docker" in defaults


def test_default_addons_for_library() -> None:
    """Library should have only cicd as default addon."""
    defaults = ProjectConfig.default_addons(ProjectType.LIBRARY)
    assert defaults == ["cicd"]


def test_template_context_returns_dict() -> None:
    """template_context() returns a dict suitable for Jinja2 rendering."""
    config = ProjectConfig(
        project_name="myproject",
        description="A test",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.CLI_TOOL,
    )
    ctx = config.template_context()
    assert ctx["project_name"] == "myproject"
    assert ctx["project_slug"] == "myproject"
    assert ctx["description"] == "A test"
    assert ctx["author"] == "testuser"
    assert ctx["language"] == "python"
    assert ctx["project_type"] == "cli_tool"
    assert ctx["is_python"] is True
    assert ctx["is_typescript"] is False
    assert ctx["is_microservice"] is False
    assert ctx["is_web_app"] is False
    assert ctx["is_cli_tool"] is True
    assert ctx["is_library"] is False
    assert ctx["needs_server"] is False
```

**Run**: `uv run pytest tests/test_config.py` → expect FAIL (module not found)

#### Step 2.2: Implement config model

**File**: `src/harnesskit/__init__.py`

```python
"""HarnessKit — AI Native Repository Generator."""

__version__ = "0.1.0"
```

**File**: `src/harnesskit/config.py`

```python
"""Configuration model for project generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Language(Enum):
    """Supported programming languages."""

    PYTHON = "python"
    TYPESCRIPT = "typescript"


class ProjectType(Enum):
    """Supported project types."""

    LIBRARY = "library"
    CLI_TOOL = "cli_tool"
    MICROSERVICE = "microservice"
    WEB_APP = "web_app"


SERVER_TYPES: frozenset[ProjectType] = frozenset({ProjectType.MICROSERVICE, ProjectType.WEB_APP})

DEFAULT_ADDONS: dict[ProjectType, list[str]] = {
    ProjectType.LIBRARY: ["cicd"],
    ProjectType.CLI_TOOL: ["cicd"],
    ProjectType.MICROSERVICE: ["cicd", "docker"],
    ProjectType.WEB_APP: ["cicd"],
}


@dataclass
class ProjectConfig:
    """Holds all user selections for project generation.

    This is the single source of truth passed from prompts → generator.
    """

    project_name: str
    description: str
    author: str
    language: Language
    project_type: ProjectType
    addons: list[str] = field(default_factory=list)
    frontend_framework: str | None = None  # Only for TS Web App
    git_init: bool = True

    @property
    def project_slug(self) -> str:
        """Normalized project name for directory and package naming.

        Python: snake_case (dashes → underscores)
        TypeScript: kebab-case (keeps dashes)
        """
        name = self.project_name.lower().strip()
        if self.language == Language.PYTHON:
            return name.replace("-", "_")
        return name.replace("_", "-")

    @property
    def needs_server(self) -> bool:
        """Whether this project type runs a server process."""
        return self.project_type in SERVER_TYPES

    @staticmethod
    def default_addons(project_type: ProjectType) -> list[str]:
        """Return default addon list for a project type."""
        return list(DEFAULT_ADDONS.get(project_type, []))

    def template_context(self) -> dict[str, object]:
        """Return a flat dict for Jinja2 template rendering."""
        return {
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "description": self.description,
            "author": self.author,
            "language": self.language.value,
            "project_type": self.project_type.value,
            "is_python": self.language == Language.PYTHON,
            "is_typescript": self.language == Language.TYPESCRIPT,
            "is_library": self.project_type == ProjectType.LIBRARY,
            "is_cli_tool": self.project_type == ProjectType.CLI_TOOL,
            "is_microservice": self.project_type == ProjectType.MICROSERVICE,
            "is_web_app": self.project_type == ProjectType.WEB_APP,
            "needs_server": self.needs_server,
            "addons": self.addons,
            "frontend_framework": self.frontend_framework,
            "git_init": self.git_init,
        }
```

**Run**: `uv run pytest tests/test_config.py -v` → expect ALL PASS

**Commit**: `feat(config): add ProjectConfig model with language/type enums`

---

### Task 3: Generator Engine — `src/harnesskit/generator.py`

**Goal**: Core engine that takes a `ProjectConfig`, resolves template layers, renders Jinja2 templates, writes files to disk.

#### Step 3.1: Write failing test

**File**: `tests/test_generator.py`

```python
"""Tests for the project generator engine."""

from pathlib import Path

from harnesskit.config import Language, ProjectConfig, ProjectType
from harnesskit.generator import ProjectGenerator


def _make_config(
    name: str = "testproject",
    language: Language = Language.PYTHON,
    project_type: ProjectType = ProjectType.LIBRARY,
) -> ProjectConfig:
    return ProjectConfig(
        project_name=name,
        description="A test project",
        author="testuser",
        language=language,
        project_type=project_type,
        git_init=False,  # Don't git init in tests
    )


def test_generator_creates_output_directory(tmp_path: Path) -> None:
    """Generator creates the project directory."""
    config = _make_config()
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()
    assert (tmp_path / "testproject").is_dir()


def test_generator_creates_base_layer_files(tmp_path: Path) -> None:
    """Generator creates all base layer files."""
    config = _make_config()
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "CLAUDE.md").is_file()
    assert (project_dir / "AGENTS.md").is_file()
    assert (project_dir / "Makefile").is_file()
    assert (project_dir / ".gitignore").is_file()
    assert (project_dir / "README.md").is_file()
    assert (project_dir / "LICENSE").is_file()
    assert (project_dir / "docs" / "adr" / "000-template.md").is_file()
    assert (project_dir / "docs" / "architecture.md").is_file()


def test_generator_creates_harness_check_script(tmp_path: Path) -> None:
    """Generator creates harness-check script and it is executable-ready."""
    config = _make_config()
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    script = tmp_path / "testproject" / "scripts" / "harness-check.sh"
    assert script.is_file()
    content = script.read_text()
    assert "harness-check" in content


def test_generator_creates_python_shared_files(tmp_path: Path) -> None:
    """Generator creates Python shared layer files."""
    config = _make_config()
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "pyproject.toml").is_file()
    assert (project_dir / ".pre-commit-config.yaml").is_file()
    assert (project_dir / ".python-version").is_file()


def test_generator_python_library_structure(tmp_path: Path) -> None:
    """Python Library has correct source and test structure."""
    config = _make_config(project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "src" / "testproject" / "__init__.py").is_file()
    assert (project_dir / "src" / "testproject" / "core.py").is_file()
    assert (project_dir / "tests" / "test_core.py").is_file()


def test_generator_python_cli_tool_structure(tmp_path: Path) -> None:
    """Python CLI Tool has CLI entry point and __main__.py."""
    config = _make_config(project_type=ProjectType.CLI_TOOL)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "src" / "testproject" / "__main__.py").is_file()
    assert (project_dir / "src" / "testproject" / "cli.py").is_file()
    assert (project_dir / "tests" / "test_cli.py").is_file()


def test_generator_python_microservice_structure(tmp_path: Path) -> None:
    """Python Microservice has app, routes, Dockerfile, e2e script."""
    config = _make_config(project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "src" / "testproject" / "app.py").is_file()
    assert (project_dir / "src" / "testproject" / "routes" / "health.py").is_file()
    assert (project_dir / "src" / "testproject" / "config.py").is_file()
    assert (project_dir / "Dockerfile").is_file()
    assert (project_dir / "scripts" / "test-e2e.sh").is_file()
    assert (project_dir / "tests" / "conftest.py").is_file()
    assert (project_dir / "tests" / "test_health.py").is_file()


def test_generator_python_web_app_structure(tmp_path: Path) -> None:
    """Python Web App has templates, static, pages route."""
    config = _make_config(project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project_dir = tmp_path / "testproject"
    assert (project_dir / "src" / "testproject" / "routes" / "pages.py").is_file()
    assert (project_dir / "src" / "testproject" / "static" / "style.css").is_file()
    assert (project_dir / "src" / "testproject" / "templates" / "index.html").is_file()
    assert (project_dir / "tests" / "test_pages.py").is_file()


def test_generator_pyproject_contains_project_name(tmp_path: Path) -> None:
    """Rendered pyproject.toml contains the correct project name."""
    config = _make_config(name="awesome-lib")
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "awesome-lib" / "pyproject.toml").read_text()
    assert 'name = "awesome-lib"' in content


def test_generator_claude_md_contains_project_name(tmp_path: Path) -> None:
    """Rendered CLAUDE.md contains the project name."""
    config = _make_config(name="awesome-lib")
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "awesome-lib" / "CLAUDE.md").read_text()
    assert "awesome-lib" in content


def test_generator_makefile_has_dev_for_microservice(tmp_path: Path) -> None:
    """Microservice Makefile includes dev and test-e2e targets."""
    config = _make_config(project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "testproject" / "Makefile").read_text()
    assert "dev:" in content
    assert "test-e2e:" in content


def test_generator_makefile_no_dev_for_library(tmp_path: Path) -> None:
    """Library Makefile does NOT include dev target."""
    config = _make_config(project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "testproject" / "Makefile").read_text()
    assert "dev:" not in content


def test_generator_raises_if_directory_exists(tmp_path: Path) -> None:
    """Generator raises error if output project directory already exists."""
    config = _make_config()
    (tmp_path / "testproject").mkdir()

    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    try:
        gen.generate()
        msg = "Expected FileExistsError"
        raise AssertionError(msg)
    except FileExistsError:
        pass
```

**Run**: `uv run pytest tests/test_generator.py` → expect FAIL (module not found)

#### Step 3.2: Implement generator engine

**File**: `src/harnesskit/generator.py`

```python
"""Project generation engine.

Resolves template layers, renders Jinja2 templates, writes output files.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, StrictUndefined

if TYPE_CHECKING:
    from harnesskit.config import ProjectConfig

TEMPLATES_DIR = Path(__file__).parent / "templates"


class ProjectGenerator:
    """Generates a project from a ProjectConfig using layered Jinja2 templates.

    Layer 1: base/          → Files every project gets
    Layer 2: {lang}/_shared → Language shared files
    Layer 3: {lang}/{type}/ → Language + type specific files
    """

    def __init__(self, config: ProjectConfig, output_dir: Path | None = None) -> None:
        self.config = config
        self.output_dir = output_dir or Path.cwd()
        self.project_dir = self.output_dir / self.config.project_name
        self.context = self.config.template_context()
        self._env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )

    def generate(self) -> Path:
        """Generate the full project. Returns the project directory path."""
        if self.project_dir.exists():
            msg = f"Directory already exists: {self.project_dir}"
            raise FileExistsError(msg)

        self.project_dir.mkdir(parents=True)

        self._render_layer("base")
        lang = self.config.language.value
        self._render_layer(f"{lang}/_shared")
        self._render_layer(f"{lang}/{self.config.project_type.value}")
        self._make_scripts_executable()

        return self.project_dir

    def _render_layer(self, layer_path: str) -> None:
        """Render all templates in a layer directory to the project dir."""
        layer_dir = TEMPLATES_DIR / layer_path
        if not layer_dir.is_dir():
            return

        for template_file in layer_dir.rglob("*.j2"):
            rel_path = template_file.relative_to(layer_dir)
            # Remove .j2 extension
            output_rel = Path(str(rel_path)[:-3])
            # Resolve {{project_slug}} in path components
            output_rel = self._resolve_path_vars(output_rel)
            output_path = self.project_dir / output_rel

            # Render template
            template_key = f"{layer_path}/{rel_path}"
            template = self._env.get_template(template_key.replace(os.sep, "/"))
            content = template.render(self.context)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)

    def _resolve_path_vars(self, path: Path) -> Path:
        """Replace {{project_slug}} in path components with actual slug."""
        parts: list[str] = []
        for part in path.parts:
            resolved = part.replace("{{project_slug}}", self.config.project_slug)
            parts.append(resolved)
        return Path(*parts) if parts else path

    def _make_scripts_executable(self) -> None:
        """Make shell scripts in scripts/ executable."""
        scripts_dir = self.project_dir / "scripts"
        if scripts_dir.is_dir():
            for script in scripts_dir.glob("*.sh"):
                current = script.stat().st_mode
                script.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
```

#### Step 3.3: Create all Jinja2 templates

This step creates every template file referenced above. Templates are listed below grouped by layer.

> **Note**: Each template file is a separate `.j2` file. They contain the rendered content for generated projects. Full template contents are provided in Task 6 (Template Content).

**Run**: `uv run pytest tests/test_generator.py -v` → expect ALL PASS (after templates are created in Task 6)

**Commit**: `feat(generator): add layered Jinja2 template engine`

---

### Task 4: Interactive Prompts — `src/harnesskit/prompts.py`

**Goal**: questionary-based interactive prompts that collect user input and return a `ProjectConfig`.

#### Step 4.1: Write test

**File**: `tests/test_prompts.py`

```python
"""Tests for interactive prompts module.

Note: Interactive prompts are hard to unit test directly. We test the
non-interactive helper functions and validation logic. Full interactive
flow is covered by integration/manual testing.
"""

from harnesskit.config import Language, ProjectType
from harnesskit.prompts import (
    LANGUAGE_CHOICES,
    PROJECT_TYPE_CHOICES,
    get_addon_defaults,
    validate_project_name,
)


def test_validate_project_name_valid() -> None:
    """Valid project names pass validation."""
    assert validate_project_name("myproject") is True
    assert validate_project_name("my-project") is True
    assert validate_project_name("my_project") is True
    assert validate_project_name("project123") is True


def test_validate_project_name_invalid() -> None:
    """Invalid project names return error string."""
    result = validate_project_name("")
    assert isinstance(result, str)
    result = validate_project_name("My Project")
    assert isinstance(result, str)
    result = validate_project_name("123start")
    assert isinstance(result, str)
    result = validate_project_name(".hidden")
    assert isinstance(result, str)


def test_language_choices_match_enum() -> None:
    """Language choices cover all Language enum values."""
    choice_values = {c["value"] for c in LANGUAGE_CHOICES}
    enum_values = {lang.value for lang in Language}
    assert choice_values == enum_values


def test_project_type_choices_match_enum() -> None:
    """Project type choices cover all ProjectType enum values."""
    choice_values = {c["value"] for c in PROJECT_TYPE_CHOICES}
    enum_values = {pt.value for pt in ProjectType}
    assert choice_values == enum_values


def test_get_addon_defaults_for_microservice() -> None:
    """Microservice has cicd and docker pre-selected."""
    defaults = get_addon_defaults(ProjectType.MICROSERVICE)
    assert "cicd" in defaults
    assert "docker" in defaults


def test_get_addon_defaults_for_library() -> None:
    """Library has only cicd pre-selected."""
    defaults = get_addon_defaults(ProjectType.LIBRARY)
    assert defaults == ["cicd"]
```

#### Step 4.2: Implement prompts

**File**: `src/harnesskit/prompts.py`

```python
"""Interactive TUI prompts using questionary.

Collects user input and returns a ProjectConfig.
"""

from __future__ import annotations

import re

import questionary

from harnesskit.config import Language, ProjectConfig, ProjectType

LANGUAGE_CHOICES: list[dict[str, str]] = [
    {"name": "Python", "value": "python"},
    {"name": "TypeScript", "value": "typescript"},
]

PROJECT_TYPE_CHOICES: list[dict[str, str]] = [
    {"name": "Library", "value": "library"},
    {"name": "CLI Tool", "value": "cli_tool"},
    {"name": "Microservice", "value": "microservice"},
    {"name": "Web App", "value": "web_app"},
]

ADDON_CHOICES: list[dict[str, str]] = [
    {"name": "CI/CD (GitHub Actions)", "value": "cicd"},
    {"name": "Docker Compose", "value": "docker"},
    {"name": "Agent Project (.claude/skills, agents, hooks)", "value": "agent_project"},
    {"name": "DevContainer", "value": "devcontainer"},
]

_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*$")


def validate_project_name(name: str) -> bool | str:
    """Validate project name. Returns True if valid, error string if not."""
    if not name:
        return "Project name cannot be empty"
    if not _NAME_PATTERN.match(name):
        return "Must start with lowercase letter, contain only [a-z0-9_-]"
    return True


def get_addon_defaults(project_type: ProjectType) -> list[str]:
    """Return default addon selections for a project type."""
    return ProjectConfig.default_addons(project_type)


def collect_inputs(project_name: str | None = None) -> ProjectConfig:
    """Run interactive prompts and return a ProjectConfig.

    Args:
        project_name: If provided, skip the project name prompt.
    """
    if project_name is None:
        project_name = questionary.text(
            "Project name:",
            validate=validate_project_name,
        ).unsafe_ask()

    description: str = questionary.text(
        "Description:",
        default="",
    ).unsafe_ask()

    author: str = questionary.text(
        "Author:",
        default="",
    ).unsafe_ask()

    language_value: str = questionary.select(
        "Language:",
        choices=[questionary.Choice(c["name"], value=c["value"]) for c in LANGUAGE_CHOICES],
    ).unsafe_ask()
    language = Language(language_value)

    type_value: str = questionary.select(
        "Project type:",
        choices=[questionary.Choice(c["name"], value=c["value"]) for c in PROJECT_TYPE_CHOICES],
    ).unsafe_ask()
    project_type = ProjectType(type_value)

    # Frontend framework choice (TS Web App only)
    frontend_framework: str | None = None
    if language == Language.TYPESCRIPT and project_type == ProjectType.WEB_APP:
        frontend_framework = questionary.select(
            "Frontend framework:",
            choices=[
                questionary.Choice("React (Vite + React)", value="react"),
                questionary.Choice("Vue (Vite + Vue)", value="vue"),
                questionary.Choice("Hono JSX (lightweight SSR)", value="hono_jsx"),
                questionary.Choice("None (API + static files only)", value="none"),
            ],
        ).unsafe_ask()

    defaults = get_addon_defaults(project_type)
    addon_values: list[str] = questionary.checkbox(
        "Select addons:",
        choices=[
            questionary.Choice(c["name"], value=c["value"], checked=c["value"] in defaults)
            for c in ADDON_CHOICES
        ],
    ).unsafe_ask()

    git_init: bool = questionary.confirm(
        "Initialize git repo and make first commit?",
        default=True,
    ).unsafe_ask()

    return ProjectConfig(
        project_name=project_name,
        description=description,
        author=author,
        language=language,
        project_type=project_type,
        addons=addon_values,
        frontend_framework=frontend_framework,
        git_init=git_init,
    )
```

**Run**: `uv run pytest tests/test_prompts.py -v` → expect ALL PASS

**Commit**: `feat(prompts): add interactive questionary prompts`

---

### Task 5: CLI Entry Point — `src/harnesskit/cli.py`

**Goal**: `hk new [name]` command wired to prompts + generator + optional git init.

#### Step 5.1: Write failing test

**File**: `tests/test_cli.py`

```python
"""Tests for CLI commands."""

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from harnesskit.cli import main
from harnesskit.config import Language, ProjectConfig, ProjectType


def _mock_config(name: str = "testproject") -> ProjectConfig:
    return ProjectConfig(
        project_name=name,
        description="Test",
        author="tester",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
        git_init=False,
    )


def test_cli_new_with_name(tmp_path: Path) -> None:
    """hk new myproject generates a project directory."""
    runner = CliRunner()
    with patch("harnesskit.cli.collect_inputs", return_value=_mock_config()):
        result = runner.invoke(main, ["new", "testproject", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / "testproject").is_dir()


def test_cli_new_without_name(tmp_path: Path) -> None:
    """hk new (no name) still works via prompts."""
    runner = CliRunner()
    with patch("harnesskit.cli.collect_inputs", return_value=_mock_config()):
        result = runner.invoke(main, ["new", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0


def test_cli_version() -> None:
    """hk --version shows version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output
```

#### Step 5.2: Implement CLI

**File**: `src/harnesskit/cli.py`

```python
"""CLI entry point for harnesskit.

Commands:
    hk new [name]  — Generate a new AI Native Repository
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import click
from rich.console import Console

from harnesskit import __version__
from harnesskit.generator import ProjectGenerator
from harnesskit.prompts import collect_inputs

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="harnesskit")
def main() -> None:
    """HarnessKit — AI Native Repository Generator."""


@main.command()
@click.argument("name", required=False)
@click.option("--output-dir", type=click.Path(path_type=Path), default=None, help="Output directory")
def new(name: str | None, output_dir: Path | None) -> None:
    """Generate a new AI Native Repository."""
    console.print("\n🔧 [bold]HarnessKit[/bold] — AI Native Repository Generator\n")

    config = collect_inputs(project_name=name)
    target = output_dir or Path.cwd()

    generator = ProjectGenerator(config=config, output_dir=target)

    try:
        project_path = generator.generate()
    except FileExistsError as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise SystemExit(1) from e

    if config.git_init:
        _git_init(project_path)

    console.print(f"\n✨ Created [bold green]{config.project_name}/[/bold green]", end="")
    console.print(f" with {config.language.value.title()} + {config.project_type.value.replace('_', ' ').title()} template")

    if config.addons:
        console.print(f"   Addons: {', '.join(config.addons)}")

    console.print(f"\n👉 Next steps:")
    console.print(f"   cd {config.project_name}")
    console.print(f"   make setup")
    if config.needs_server:
        console.print(f"   make dev")
    console.print()


def _git_init(project_path: Path) -> None:
    """Initialize git repo and make first commit."""
    try:
        subprocess.run(["git", "init"], cwd=project_path, capture_output=True, check=True)
        subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "feat: initial project scaffold by harnesskit"],
            cwd=project_path,
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[yellow]Warning:[/yellow] Git init failed, skipping.")
```

**File**: `src/harnesskit/__main__.py`

```python
"""Allow running harnesskit as a module: python -m harnesskit."""

from harnesskit.cli import main

main()
```

**Run**: `uv run pytest tests/test_cli.py -v` → expect ALL PASS

**Commit**: `feat(cli): add hk new command with git init`

---

### Task 6: Jinja2 Templates — All Python Template Files

**Goal**: Create every `.j2` template referenced in the file structure. This is the largest task.

#### Step 6.1: Write template snapshot tests

**File**: `tests/conftest.py`

```python
"""Shared test fixtures."""

from pathlib import Path

import pytest

from harnesskit.config import Language, ProjectConfig, ProjectType


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Provide a clean temporary output directory."""
    return tmp_path


def make_config(
    name: str = "testproject",
    language: Language = Language.PYTHON,
    project_type: ProjectType = ProjectType.LIBRARY,
    addons: list[str] | None = None,
    git_init: bool = False,
) -> ProjectConfig:
    """Create a ProjectConfig for testing."""
    return ProjectConfig(
        project_name=name,
        description="A test project",
        author="testuser",
        language=language,
        project_type=project_type,
        addons=addons or [],
        git_init=git_init,
    )
```

**File**: `tests/test_templates/test_python_library.py`

```python
"""Snapshot tests for Python Library template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_python_library_generates_all_expected_files(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "testproject"
    expected_files = [
        "CLAUDE.md", "AGENTS.md", "Makefile", ".gitignore", "README.md", "LICENSE",
        "docs/adr/000-template.md", "docs/architecture.md",
        "scripts/harness-check.sh",
        "pyproject.toml", ".pre-commit-config.yaml", ".python-version",
        "src/testproject/__init__.py", "src/testproject/core.py",
        "tests/test_core.py",
    ]
    for f in expected_files:
        assert (project / f).is_file(), f"Missing: {f}"


def test_python_library_pyproject_is_valid(tmp_path: Path) -> None:
    config = make_config(name="mylib", language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "mylib" / "pyproject.toml").read_text()
    assert 'name = "mylib"' in content
    assert "hatchling" in content
    assert "ruff" in content
    assert "pyright" in content


def test_python_library_makefile_targets(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "testproject" / "Makefile").read_text()
    for target in ["setup:", "lint:", "format:", "typecheck:", "test:", "check:", "build:"]:
        assert target in content
    assert "dev:" not in content  # Library has no dev server
```

**File**: `tests/test_templates/test_python_cli_tool.py`

```python
"""Snapshot tests for Python CLI Tool template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_python_cli_tool_has_click_entry(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.CLI_TOOL)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "testproject"
    cli_content = (project / "src" / "testproject" / "cli.py").read_text()
    assert "click" in cli_content

    pyproject = (project / "pyproject.toml").read_text()
    assert "[project.scripts]" in pyproject


def test_python_cli_tool_has_main(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.CLI_TOOL)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    assert (tmp_path / "testproject" / "src" / "testproject" / "__main__.py").is_file()
```

**File**: `tests/test_templates/test_python_microservice.py`

```python
"""Snapshot tests for Python Microservice template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_python_microservice_has_fastapi_app(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "testproject"
    app_content = (project / "src" / "testproject" / "app.py").read_text()
    assert "FastAPI" in app_content


def test_python_microservice_has_health_endpoint(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    health = (tmp_path / "testproject" / "src" / "testproject" / "routes" / "health.py").read_text()
    assert "healthz" in health


def test_python_microservice_makefile_has_dev(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    makefile = (tmp_path / "testproject" / "Makefile").read_text()
    assert "dev:" in makefile
    assert "test-e2e:" in makefile
    assert "docker-build:" in makefile


def test_python_microservice_has_dockerfile(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    assert (tmp_path / "testproject" / "Dockerfile").is_file()
```

**File**: `tests/test_templates/test_python_web_app.py`

```python
"""Snapshot tests for Python Web App template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_python_web_app_has_templates_and_static(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "testproject"
    assert (project / "src" / "testproject" / "templates" / "index.html").is_file()
    assert (project / "src" / "testproject" / "static" / "style.css").is_file()


def test_python_web_app_has_pages_route(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    pages = (tmp_path / "testproject" / "src" / "testproject" / "routes" / "pages.py").read_text()
    assert "pages" in pages.lower() or "template" in pages.lower()


def test_python_web_app_has_jinja2_dep(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    pyproject = (tmp_path / "testproject" / "pyproject.toml").read_text()
    assert "jinja2" in pyproject
```

**File**: `tests/test_templates/__init__.py`

```python
```

#### Step 6.2: Create base layer templates

> All template files listed below. Each is written as a separate file.

**Template**: `src/harnesskit/templates/base/CLAUDE.md.j2`

````
# {{ project_name }}

{{ description }}

## Tech Stack
{% if is_python -%}
- Python 3.11+ / uv / Ruff / pyright strict / pytest
{% if is_microservice -%}
- Framework: FastAPI + uvicorn / Logging: structlog
{% elif is_web_app -%}
- Framework: FastAPI + Jinja2 / Logging: structlog
{% elif is_cli_tool -%}
- CLI: click
{% endif -%}
{% endif -%}

## Commands
- `make setup` — Initialize environment
- `make lint` — Lint check
- `make format` — Auto format
- `make typecheck` — Type check
- `make test` — Run tests
- `make check` — Full check (lint + typecheck + test)
{% if needs_server -%}
- `make dev` — Start dev server
- `make test-e2e` — End-to-end test
{% endif -%}

## Project Structure
{% if is_python -%}
- `src/{{ project_slug }}/` — Source code
{% if is_microservice or is_web_app -%}
- `src/{{ project_slug }}/app.py` — FastAPI application
- `src/{{ project_slug }}/routes/` — Route handlers
- `src/{{ project_slug }}/config.py` — Configuration
{% endif -%}
{% if is_cli_tool -%}
- `src/{{ project_slug }}/cli.py` — CLI entry point
{% endif -%}
{% endif -%}
- `tests/` — Tests, mirroring src structure

## Workflow
- Plan first, then implement. Use Plan Mode for complex changes.
- Run `make check` after changes, before commit.
- Write/update tests first, then implement feature.

## Boundaries
### Always Do
- Strict types (pyright strict)
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
- No `type: ignore` without comment explaining why
````

**Template**: `src/harnesskit/templates/base/AGENTS.md.j2`

```
# AGENTS.md

This project uses harness engineering practices. See CLAUDE.md for full details.

## Cross-Agent Conventions
- Run `make check` before committing
- Follow conventional commits: type(scope): description (≤200 chars)
- Keep files under 300 lines
- Strict types: {{ "pyright strict" if is_python else "tsconfig strict" }}
```

**Template**: `src/harnesskit/templates/base/Makefile.j2`

```
.PHONY: setup lint format typecheck test test-cov check clean{% if needs_server %} dev test-e2e docker-build docker-run{% endif %}{% if is_library or is_cli_tool %} build{% endif %}{% if is_library %} publish{% endif %} harness-check

{% if is_python -%}
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
	uv run pytest tests/ -v --cov=src/{{ project_slug }} --cov-report=term-missing

check:            ## Full check (CI use)
	make lint && make typecheck && make test

clean:            ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info
{% if is_library or is_cli_tool %}
build:            ## Build distribution
	uv build
{% endif %}
{% if is_library %}
publish:          ## Publish to PyPI
	uv publish
{% endif %}
{% if is_cli_tool %}
run:              ## Run the CLI
	uv run {{ project_slug }}
{% endif %}
{% if needs_server %}
dev:              ## Start dev server
	uv run uvicorn {{ project_slug }}.app:app --reload --port 8000

test-e2e:         ## End-to-end test
	bash scripts/test-e2e.sh

docker-build:     ## Build Docker image
	docker build -t {{ project_name }} .

docker-run:       ## Run Docker container
	docker run -p 8000:8000 {{ project_name }}
{% endif %}
{% endif -%}
harness-check:    ## Run harness engineering checks
	bash scripts/harness-check.sh
```

**Template**: `src/harnesskit/templates/base/.gitignore.j2`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
venv/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml

# pyright / mypy
.pyright/
.mypy_cache/

# uv
.python-version-*
```

**Template**: `src/harnesskit/templates/base/README.md.j2`

```
# {{ project_name }}

{{ description }}

## Quick Start

```bash
make setup
{% if needs_server -%}
make dev
{% else -%}
make test
{% endif -%}
```

## Development

```bash
make lint        # Lint check
make format      # Auto format
make typecheck   # Type check
make test        # Run tests
make check       # Full check (lint + typecheck + test)
```

## Project Structure

```
{{ project_name }}/
├── src/{{ project_slug }}/   # Source code
├── tests/                     # Tests
├── CLAUDE.md                  # AI agent instructions
├── Makefile                   # Unified commands
└── scripts/
    └── harness-check.sh      # Harness engineering checks
```
```

**Template**: `src/harnesskit/templates/base/LICENSE.j2`

```
MIT License

Copyright (c) 2026 {{ author }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Template**: `src/harnesskit/templates/base/docs/adr/000-template.md.j2`

```
# ADR-000: Template

## Status
Accepted

## Context
Describe the context and problem statement.

## Decision
Describe the decision that was made.

## Consequences
Describe the consequences of the decision.
```

**Template**: `src/harnesskit/templates/base/docs/architecture.md.j2`

```
# Architecture — {{ project_name }}

## Overview
{{ description }}

## Directory Structure
{% if is_python -%}
- `src/{{ project_slug }}/` — Main application code
{% if is_microservice or is_web_app -%}
- `src/{{ project_slug }}/routes/` — HTTP route handlers
- `src/{{ project_slug }}/services/` — Business logic
- `src/{{ project_slug }}/models/` — Data models
{% endif -%}
{% endif -%}
- `tests/` — Unit and integration tests
- `scripts/` — Helper scripts (harness-check, e2e tests)
- `docs/` — Documentation and ADRs

## Key Decisions
See `docs/adr/` for Architecture Decision Records.
```

**Template**: `src/harnesskit/templates/base/scripts/harness-check.sh.j2`

```
#!/usr/bin/env bash
# harness-check — Verify harness engineering conventions
# Run: make harness-check

set -euo pipefail

EXIT_CODE=0
WARN_COUNT=0
ERROR_COUNT=0

warn() { echo "harness-check: WARN   $1"; WARN_COUNT=$((WARN_COUNT + 1)); }
error() { echo "harness-check: ERROR  $1"; ERROR_COUNT=$((ERROR_COUNT + 1)); EXIT_CODE=1; }
info() { echo "harness-check: INFO   $1"; }

# --- Check CLAUDE.md exists ---
if [ ! -f "CLAUDE.md" ]; then
    error "CLAUDE.md not found in project root."
fi

# --- Check file sizes ---
{% if is_python -%}
SOURCE_DIR="src/"
{% else -%}
SOURCE_DIR="src/"
{% endif -%}

if [ -d "$SOURCE_DIR" ]; then
    while IFS= read -r -d '' file; do
        lines=$(wc -l < "$file")
        if [ "$lines" -gt 1000 ]; then
            error "$file:1-$lines — File exceeds 1000 line limit ($lines lines). Must split."
        elif [ "$lines" -gt 500 ]; then
            warn "$file:1-$lines — File exceeds 500 line limit ($lines lines). Consider splitting by responsibility."
        fi
    done < <(find "$SOURCE_DIR" -name "*.py" -o -name "*.ts" -o -name "*.tsx" | tr '\n' '\0')
fi

# --- Check test coverage (each src module has a test) ---
{% if is_python -%}
if [ -d "src/{{ project_slug }}" ]; then
    for src_file in src/{{ project_slug }}/*.py; do
        [ -f "$src_file" ] || continue
        basename=$(basename "$src_file" .py)
        [ "$basename" = "__init__" ] && continue
        [ "$basename" = "__main__" ] && continue
        test_file="tests/test_${basename}.py"
        if [ ! -f "$test_file" ]; then
            warn "$src_file — Missing test file. Expected: $test_file"
        fi
    done
fi
{% endif -%}

# --- Check directory naming (snake_case for Python, kebab-case for TS) ---
{% if is_python -%}
if [ -d "src/{{ project_slug }}" ]; then
    for dir in src/{{ project_slug }}/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        if ! echo "$dirname" | grep -qE '^[a-z][a-z0-9_]*$'; then
            warn "$dir — Directory should use snake_case naming."
        fi
    done
fi
{% endif -%}

# --- Summary ---
echo ""
echo "harness-check: $ERROR_COUNT error(s), $WARN_COUNT warning(s)"
exit $EXIT_CODE
```

#### Step 6.3: Create Python shared templates

**Template**: `src/harnesskit/templates/python/_shared/pyproject.toml.j2`

```
[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = ">=3.11"
license = "MIT"
authors = [{ name = "{{ author }}" }]
dependencies = [
{% if is_cli_tool -%}
    "click>=8.1",
{% endif -%}
{% if is_microservice -%}
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "pydantic-settings>=2.0",
    "structlog>=24.0",
{% endif -%}
{% if is_web_app -%}
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "pydantic-settings>=2.0",
    "structlog>=24.0",
    "jinja2>=3.1",
{% endif -%}
]

{% if is_cli_tool -%}
[project.scripts]
{{ project_slug }} = "{{ project_slug }}.cli:main"

{% endif -%}
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
{% if is_microservice or is_web_app -%}
    "httpx>=0.27",
{% endif -%}
]

[tool.ruff]
target-version = "py311"
line-length = 120
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM", "TCH"]

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
include = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.hatch.build.targets.wheel]
packages = ["src/{{ project_slug }}"]
```

**Template**: `src/harnesskit/templates/python/_shared/.pre-commit-config.yaml.j2`

```
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.18.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
```

**Template**: `src/harnesskit/templates/python/_shared/.python-version.j2`

```
3.11
```

#### Step 6.4: Create Python Library templates

**Template**: `src/harnesskit/templates/python/library/src/{{project_slug}}/__init__.py.j2`

```
"""{{ project_name }} — {{ description }}"""

__version__ = "0.1.0"
```

**Template**: `src/harnesskit/templates/python/library/src/{{project_slug}}/core.py.j2`

```
"""Core module for {{ project_name }}.

This is an example module. Replace with your own code.
"""

from __future__ import annotations


def greet(name: str) -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}! Welcome to {{ project_name }}."


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        Sum of a and b.
    """
    return a + b
```

**Template**: `src/harnesskit/templates/python/library/tests/test_core.py.j2`

```
"""Tests for core module."""

from {{ project_slug }}.core import add, greet


def test_greet_returns_message() -> None:
    result = greet("World")
    assert "Hello, World!" in result


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

#### Step 6.5: Create Python CLI Tool templates

**Template**: `src/harnesskit/templates/python/cli_tool/src/{{project_slug}}/__init__.py.j2`

```
"""{{ project_name }} — {{ description }}"""

__version__ = "0.1.0"
```

**Template**: `src/harnesskit/templates/python/cli_tool/src/{{project_slug}}/__main__.py.j2`

```
"""Allow running as: python -m {{ project_slug }}."""

from {{ project_slug }}.cli import main

main()
```

**Template**: `src/harnesskit/templates/python/cli_tool/src/{{project_slug}}/cli.py.j2`

```
"""CLI entry point for {{ project_name }}."""

from __future__ import annotations

import click

from {{ project_slug }} import __version__
from {{ project_slug }}.core import greet


@click.group()
@click.version_option(version=__version__, prog_name="{{ project_name }}")
def main() -> None:
    """{{ description }}"""


@main.command()
@click.argument("name", default="World")
def hello(name: str) -> None:
    """Greet someone."""
    click.echo(greet(name))
```

**Template**: `src/harnesskit/templates/python/cli_tool/src/{{project_slug}}/core.py.j2`

```
"""Core logic for {{ project_name }}."""

from __future__ import annotations


def greet(name: str) -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}! Welcome to {{ project_name }}."
```

**Template**: `src/harnesskit/templates/python/cli_tool/tests/test_cli.py.j2`

```
"""Tests for CLI commands."""

from click.testing import CliRunner

from {{ project_slug }}.cli import main


def test_hello_default() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_hello_with_name() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output
```

**Template**: `src/harnesskit/templates/python/cli_tool/tests/test_core.py.j2`

```
"""Tests for core module."""

from {{ project_slug }}.core importgreet


def test_greet_returns_message() -> None:
    result = greet("World")
    assert "Hello, World!" in result
```

#### Step 6.6: Create Python Microservice templates

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/__init__.py.j2`

```
"""{{ project_name }} — {{ description }}"""

__version__ = "0.1.0"
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/app.py.j2`

```
"""FastAPI application for {{ project_name }}."""

from __future__ import annotations

import structlog
from fastapi import FastAPI

from {{ project_slug }}.routes.health import router as health_router

logger = structlog.get_logger()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="{{ project_name }}",
        description="{{ description }}",
        version="0.1.0",
    )
    application.include_router(health_router)

    @application.on_event("startup")
    async def on_startup() -> None:
        logger.info("application_started", app="{{ project_name }}")

    return application


app = create_app()
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/config.py.j2`

```
"""Application configuration using pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "{{ project_name }}"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {"env_prefix": "{{ project_slug | upper }}_"}


settings = Settings()
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/routes/__init__.py.j2`

```
"""Route handlers for {{ project_name }}."""
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/routes/health.py.j2`

```
"""Health check endpoint."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        A dict with status "ok".
    """
    return {"status": "ok"}
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/models/__init__.py.j2`

```
"""Data models for {{ project_name }}."""
```

**Template**: `src/harnesskit/templates/python/microservice/src/{{project_slug}}/services/__init__.py.j2`

```
"""Business logic services for {{ project_name }}."""
```

**Template**: `src/harnesskit/templates/python/microservice/tests/conftest.py.j2`

```
"""Test fixtures for {{ project_name }}."""

from __future__ import annotations

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from {{ project_slug }}.app import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

**Template**: `src/harnesskit/templates/python/microservice/tests/test_health.py.j2`

```
"""Tests for health endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthz_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Template**: `src/harnesskit/templates/python/microservice/Dockerfile.j2`

```
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install production dependencies
RUN uv sync --no-dev --frozen

# Copy source code
COPY src/ src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "{{ project_slug }}.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Template**: `src/harnesskit/templates/python/microservice/scripts/test-e2e.sh.j2`

```
#!/usr/bin/env bash
# End-to-end test: start server → healthcheck → stop
set -euo pipefail

echo "Starting {{ project_name }}..."
uv run uvicorn {{ project_slug }}.app:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait for server
for i in $(seq 1 30); do
    if curl -sf http://127.0.0.1:8000/healthz > /dev/null 2>&1; then
        echo "Server is up!"
        break
    fi
    sleep 0.5
done

# Run health check
echo "Running health check..."
RESPONSE=$(curl -sf http://127.0.0.1:8000/healthz)
echo "Response: $RESPONSE"

if echo "$RESPONSE" | grep -q '"status":"ok"'; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Cleanup
kill $SERVER_PID 2>/dev/null || true
echo "Done."
```

#### Step 6.7: Create Python Web App templates

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/__init__.py.j2`

```
"""{{ project_name }} — {{ description }}"""

__version__ = "0.1.0"
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/app.py.j2`

```
"""FastAPI web application for {{ project_name }}."""

from __future__ import annotations

from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from {{ project_slug }}.routes.health import router as health_router
from {{ project_slug }}.routes.pages import router as pages_router

logger = structlog.get_logger()

BASE_DIR = Path(__file__).parent


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="{{ project_name }}",
        description="{{ description }}",
        version="0.1.0",
    )

    application.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    application.include_router(health_router)
    application.include_router(pages_router)

    @application.on_event("startup")
    async def on_startup() -> None:
        logger.info("application_started", app="{{ project_name }}")

    return application


app = create_app()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/config.py.j2`

```
"""Application configuration using pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "{{ project_name }}"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {"env_prefix": "{{ project_slug | upper }}_"}


settings = Settings()
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/routes/__init__.py.j2`

```
"""Route handlers for {{ project_name }}."""
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/routes/health.py.j2`

```
"""Health check endpoint."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/routes/pages.py.j2`

```
"""Page routes for {{ project_name }}."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from {{ project_slug }}.app import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Render the home page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "{{ project_name }}",
    })
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/static/style.css.j2`

```
/* {{ project_name }} — Base styles */

:root {
    --color-primary: #2563eb;
    --color-bg: #ffffff;
    --color-text: #1f2937;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--color-text);
    background: var(--color-bg);
    line-height: 1.6;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

h1 { color: var(--color-primary); margin-bottom: 1rem; }
```

**Template**: `src/harnesskit/templates/python/web_app/src/{{project_slug}}/templates/index.html.j2`

Note: This file uses `{% raw %}` to prevent Jinja2 from processing the inner template tags during harnesskit's rendering:

```
{% raw %}<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p>Welcome to your new project. Edit this template in <code>src/templates/index.html</code>.</p>
    </div>
</body>
</html>{% endraw %}
```

**Template**: `src/harnesskit/templates/python/web_app/tests/conftest.py.j2`

(Same as microservice conftest)

```
"""Test fixtures for {{ project_name }}."""

from __future__ import annotations

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from {{ project_slug }}.app import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

**Template**: `src/harnesskit/templates/python/web_app/tests/test_health.py.j2`

```
"""Tests for health endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthz_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

**Template**: `src/harnesskit/templates/python/web_app/tests/test_pages.py.j2`

```
"""Tests for page routes."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_home_page_returns_html(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
```

**Template**: `src/harnesskit/templates/python/web_app/Dockerfile.j2`

```
FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY src/ src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "{{ project_slug }}.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Template**: `src/harnesskit/templates/python/web_app/scripts/test-e2e.sh.j2`

```
#!/usr/bin/env bash
# End-to-end test: start server → healthcheck → page load → stop
set -euo pipefail

echo "Starting {{ project_name }}..."
uv run uvicorn {{ project_slug }}.app:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

for i in $(seq 1 30); do
    if curl -sf http://127.0.0.1:8000/healthz > /dev/null 2>&1; then
        echo "Server is up!"
        break
    fi
    sleep 0.5
done

echo "Checking health endpoint..."
curl -sf http://127.0.0.1:8000/healthz | grep -q '"status":"ok"' && echo "✅ Health OK" || { echo "❌ Health failed"; kill $SERVER_PID; exit 1; }

echo "Checking home page..."
curl -sf http://127.0.0.1:8000/ | grep -q "<html" && echo "✅ Home page OK" || { echo "❌ Home page failed"; kill $SERVER_PID; exit 1; }

kill $SERVER_PID 2>/dev/null || true
echo "Done."
```

**Run**: `uv run pytest tests/ -v` → expect ALL PASS

**Commit**: `feat(templates): add all Python project templates (library, cli, microservice, web_app)`

---

### Task 7: Integration — Wire Everything Together

**Goal**: Ensure end-to-end `hk new` works for all 4 Python project types.

#### Step 7.1: Integration test

**File**: `tests/test_integration.py`

```python
"""Integration tests — generate each Python template and verify structure."""

from pathlib import Path

from harnesskit.config import Language, ProjectConfig, ProjectType
from harnesskit.generator import ProjectGenerator


ALL_PYTHON_TYPES = [
    ProjectType.LIBRARY,
    ProjectType.CLI_TOOL,
    ProjectType.MICROSERVICE,
    ProjectType.WEB_APP,
]


def _generate(tmp_path: Path, project_type: ProjectType) -> Path:
    config = ProjectConfig(
        project_name="integration_test",
        description="Integration test project",
        author="tester",
        language=Language.PYTHON,
        project_type=project_type,
        git_init=False,
    )
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    return gen.generate()


def test_all_python_types_generate_base_files(tmp_path: Path) -> None:
    """Every Python type produces the base layer files."""
    for i, pt in enumerate(ALL_PYTHON_TYPES):
        out = tmp_path / str(i)
        out.mkdir()
        project_dir = _generate(out, pt)
        for f in ["CLAUDE.md", "AGENTS.md", "Makefile", ".gitignore", "README.md", "LICENSE"]:
            assert (project_dir / f).is_file(), f"Missing {f} in {pt.value}"


def test_all_python_types_have_pyproject(tmp_path: Path) -> None:
    """Every Python type has pyproject.toml with correct name."""
    for i, pt in enumerate(ALL_PYTHON_TYPES):
        out = tmp_path / str(i)
        out.mkdir()
        project_dir = _generate(out, pt)
        content = (project_dir / "pyproject.toml").read_text()
        assert 'name = "integration_test"' in content, f"Wrong name in {pt.value}"


def test_all_python_types_have_harness_check(tmp_path: Path) -> None:
    """Every Python type has harness-check script."""
    for i, pt in enumerate(ALL_PYTHON_TYPES):
        out = tmp_path / str(i)
        out.mkdir()
        project_dir = _generate(out, pt)
        assert (project_dir / "scripts" / "harness-check.sh").is_file()


def test_makefile_check_target_for_all_types(tmp_path: Path) -> None:
    """Every Makefile has the 'check' target."""
    for i, pt in enumerate(ALL_PYTHON_TYPES):
        out = tmp_path / str(i)
        out.mkdir()
        project_dir = _generate(out, pt)
        content = (project_dir / "Makefile").read_text()
        assert "check:" in content, f"Missing check: in {pt.value}"
```

**Run**: `uv run pytest tests/ -v` → expect ALL PASS

**Commit**: `test: add integration tests for all Python project types`

---

### Task 8: Self-Harness — Apply harness-check to harnesskit itself

**Goal**: Run harness-check and ensure harnesskit passes its own standards.

#### Step 8.1: Verify all harnesskit source files are < 300 lines

```bash
find src/ -name "*.py" -exec wc -l {} \; | sort -rn | head -20
```

#### Step 8.2: Verify each src module has a test

```
src/harnesskit/cli.py        → tests/test_cli.py        ✓
src/harnesskit/config.py     → tests/test_config.py     ✓
src/harnesskit/generator.py  → tests/test_generator.py  ✓
src/harnesskit/prompts.py    → tests/test_prompts.py    ✓
```

#### Step 8.3: Run full check

```bash
make check   # lint + typecheck + test
```

**Commit**: `chore: verify harnesskit passes its own harness standards`

---

## Execution Order Summary

| # | Task | Files | Commit Message |
|---|---|---|---|
| 1 | Project scaffolding | pyproject.toml, Makefile, CLAUDE.md, AGENTS.md, CI, pre-commit | `feat: initialize harnesskit project scaffolding` |
| 2 | Config model | config.py, test_config.py | `feat(config): add ProjectConfig model with language/type enums` |
| 3 | Generator engine | generator.py, test_generator.py | `feat(generator): add layered Jinja2 template engine` |
| 4 | Interactive prompts | prompts.py, test_prompts.py | `feat(prompts): add interactive questionary prompts` |
| 5 | CLI entry point | cli.py, __main__.py, test_cli.py | `feat(cli): add hk new command with git init` |
| 6 | All templates | 40+ .j2 files, 4 test files | `feat(templates): add all Python project templates` |
| 7 | Integration tests | test_integration.py | `test: add integration tests for all Python project types` |
| 8 | Self-harness verify | (no new files) | `chore: verify harnesskit passes its own harness standards` |

---

## Self-Review Checklist

- [x] Every task starts with a failing test, then implements
- [x] Every step has exact file paths and complete code — no placeholders
- [x] Config model is the contract between prompts and generator
- [x] Generator uses 3-layer template resolution (base → lang shared → lang+type)
- [x] All 4 Python project types have templates and snapshot tests
- [x] CLAUDE.md template is under 80 lines, differentiated by project type
- [x] Makefile targets match spec (dev/test-e2e only for server types)
- [x] harness-check script covers: file size, CLAUDE.md, dir naming, test coverage
- [x] harnesskit itself follows harness engineering (uv, Ruff, pyright strict, pre-commit)
- [x] Each task has a conventional commit message
- [x] No dependencies on Phase 2 (TypeScript) or Phase 3 (Addons)
