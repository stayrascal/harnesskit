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
    assert "dev:" not in content
