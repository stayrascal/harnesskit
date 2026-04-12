"""Snapshot tests for Python Web App template."""

from pathlib import Path

from harnesskit.config import Language, ProjectType
from harnesskit.generator import ProjectGenerator
from tests.conftest import make_config


def test_python_web_app_has_templates_and_static(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    project = tmp_path / "testproject"
    assert (project / "src" / "testproject" / "templates" / "index.html").is_file()
    assert (project / "src" / "testproject" / "static" / "style.css").is_file()


def test_python_web_app_has_pages_route(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    pages = (tmp_path / "testproject" / "src" / "testproject" / "routes" / "pages.py").read_text()
    assert "pages" in pages.lower() or "template" in pages.lower()


def test_python_web_app_has_jinja2_dep(tmp_path: Path) -> None:
    config = make_config(language=Language.PYTHON, project_type=ProjectType.WEB_APP)
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    gen.generate()

    pyproject = (tmp_path / "testproject" / "pyproject.toml").read_text()
    assert "jinja2" in pyproject
