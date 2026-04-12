"""Snapshot tests for TypeScript Web App template — all 4 framework variants."""

from pathlib import Path

from harnesskit.config import Language, ProjectConfig, ProjectType
from harnesskit.generator import ProjectGenerator


def _make_ts_web_app(tmp_path: Path, framework: str) -> Path:
    config = ProjectConfig(
        project_name="testwebapp",
        description="Test web app",
        author="tester",
        language=Language.TYPESCRIPT,
        project_type=ProjectType.WEB_APP,
        frontend_framework=framework,
        git_init=False,
    )
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    return gen.generate()


def test_react_variant(tmp_path: Path) -> None:
    project = _make_ts_web_app(tmp_path, "react")
    assert (project / "src" / "App.tsx").is_file()
    assert (project / "src" / "main.tsx").is_file()
    assert (project / "vite.config.ts").is_file()
    assert (project / "public" / "index.html").is_file()


def test_vue_variant(tmp_path: Path) -> None:
    project = _make_ts_web_app(tmp_path, "vue")
    assert (project / "src" / "App.vue").is_file()
    assert (project / "src" / "main.ts").is_file()
    assert (project / "vite.config.ts").is_file()


def test_hono_jsx_variant(tmp_path: Path) -> None:
    project = _make_ts_web_app(tmp_path, "hono_jsx")
    assert (project / "src" / "app.ts").is_file()
    assert (project / "src" / "views" / "index.tsx").is_file()
    assert (project / "src" / "routes" / "pages.tsx").is_file()
    assert (project / "Dockerfile").is_file()


def test_none_variant(tmp_path: Path) -> None:
    project = _make_ts_web_app(tmp_path, "none")
    assert (project / "src" / "app.ts").is_file()
    assert (project / "src" / "routes" / "health.ts").is_file()
    assert (project / "src" / "public" / "style.css").is_file()
    assert (project / "Dockerfile").is_file()


def test_all_variants_have_base_files(tmp_path: Path) -> None:
    """All 4 variants produce base layer files."""
    for i, fw in enumerate(["react", "vue", "hono_jsx", "none"]):
        out = tmp_path / str(i)
        out.mkdir()
        project = _make_ts_web_app(out, fw)
        for f in ["CLAUDE.md", "AGENTS.md", "Makefile", "package.json", "tsconfig.json", "biome.json"]:
            assert (project / f).is_file(), f"Missing {f} in {fw} variant"
