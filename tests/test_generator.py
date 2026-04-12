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
        git_init=False,
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
    """Generator creates harness-check script."""
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
