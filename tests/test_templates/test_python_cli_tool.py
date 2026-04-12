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
