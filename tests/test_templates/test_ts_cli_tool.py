"""Snapshot tests for TypeScript CLI Tool template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_ts_cli_tool_has_commander(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.CLI_TOOL)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    cli = (tmp_path / "testproject" / "src" / "cli.ts").read_text()
    assert "commander" in cli.lower() or "Command" in cli

    pkg = (tmp_path / "testproject" / "package.json").read_text()
    assert "commander" in pkg
    assert '"bin"' in pkg
