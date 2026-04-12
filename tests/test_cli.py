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
