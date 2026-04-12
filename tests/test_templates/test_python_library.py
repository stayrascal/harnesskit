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
        "commitlint.config.js",
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
    for target in ["setup:", "lint:", "lint-fix:", "format:", "typecheck:", "test:", "check:", "build:"]:
        assert target in content, f"Missing target: {target}"
    assert "dev:" not in content


def test_python_library_claude_md_under_80_lines(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    claude_md = (tmp_path / "testproject" / "CLAUDE.md").read_text()
    line_count = len(claude_md.strip().splitlines())
    assert line_count <= 80, f"CLAUDE.md is {line_count} lines, target ≤80"


def test_python_library_commitlint_config(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "testproject" / "commitlint.config.js").read_text()
    assert "conventional" in content
    assert "200" in content  # header-max-length = 200


def test_harness_check_validates_claude_md_length(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    script = (tmp_path / "testproject" / "scripts" / "harness-check.sh").read_text()
    assert "claude_lines" in script or "CLAUDE.md" in script
    assert "80" in script  # checks 80 line limit
    assert "300" in script  # file size recommendation
    assert "500" in script  # file size warning
    assert "1000" in script  # file size error
    assert "commitlint" in script  # checks commitlint config
