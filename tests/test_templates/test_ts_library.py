"""Snapshot tests for TypeScript Library template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_ts_library_generates_expected_files(tmp_path: Path) -> None:
    config = make_config(name="my-ts-lib", language=Language.TYPESCRIPT, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "my-ts-lib"
    for f in ["CLAUDE.md", "AGENTS.md", "Makefile", ".gitignore", "README.md",
              "package.json", "tsconfig.json", "biome.json", ".pre-commit-config.yaml",
              "src/index.ts", "src/core.ts", "tests/core.test.ts"]:
        assert (project / f).is_file(), f"Missing: {f}"


def test_ts_library_makefile_uses_bun(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    makefile = (tmp_path / "testproject" / "Makefile").read_text()
    assert "bun install" in makefile
    assert "bun test" in makefile
    assert "bun run biome" in makefile
    assert "dev:" not in makefile  # Library has no dev


def test_ts_library_package_json(tmp_path: Path) -> None:
    config = make_config(name="cool-lib", language=Language.TYPESCRIPT, project_type=ProjectType.LIBRARY)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    content = (tmp_path / "cool-lib" / "package.json").read_text()
    assert '"cool-lib"' in content
    assert "biome" in content
