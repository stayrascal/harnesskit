"""Snapshot tests for TypeScript Microservice template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_ts_microservice_has_hono(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    app = (tmp_path / "testproject" / "src" / "app.ts").read_text()
    assert "Hono" in app

    pkg = (tmp_path / "testproject" / "package.json").read_text()
    assert "hono" in pkg


def test_ts_microservice_has_health_route(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    health = (tmp_path / "testproject" / "src" / "routes" / "health.ts").read_text()
    assert "healthz" in health


def test_ts_microservice_makefile_has_dev(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    makefile = (tmp_path / "testproject" / "Makefile").read_text()
    assert "dev:" in makefile
    assert "docker-build:" in makefile


def test_ts_microservice_has_dockerfile(tmp_path: Path) -> None:
    config = make_config(language=Language.TYPESCRIPT, project_type=ProjectType.MICROSERVICE)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    assert (tmp_path / "testproject" / "Dockerfile").is_file()
    content = (tmp_path / "testproject" / "Dockerfile").read_text()
    assert "bun" in content
