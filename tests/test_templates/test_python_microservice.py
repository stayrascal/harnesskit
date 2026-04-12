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
