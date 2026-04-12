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
