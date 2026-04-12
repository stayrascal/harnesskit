"""Tests for addon generation."""

from pathlib import Path

from harnesskit.config import Language, ProjectConfig, ProjectType
from harnesskit.generator import ProjectGenerator


def _make_with_addons(tmp_path: Path, addons: list[str], lang: Language = Language.PYTHON) -> Path:
    config = ProjectConfig(
        project_name="addontest",
        description="Addon test",
        author="tester",
        language=lang,
        project_type=ProjectType.MICROSERVICE,
        addons=addons,
        git_init=False,
    )
    gen = ProjectGenerator(config=config, output_dir=tmp_path)
    return gen.generate()


def test_cicd_addon_creates_workflows(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["cicd"])
    assert (project / ".github" / "workflows" / "ci.yml").is_file()
    assert (project / ".github" / "workflows" / "ai-review.yml").is_file()

    ci = (project / ".github" / "workflows" / "ci.yml").read_text()
    assert "make lint" in ci
    assert "harness-check" in ci.lower().replace("-", "").replace("_", "") or "harness" in ci


def test_cicd_addon_python_uses_uv(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["cicd"], lang=Language.PYTHON)
    ci = (project / ".github" / "workflows" / "ci.yml").read_text()
    assert "uv" in ci


def test_cicd_addon_ts_uses_bun(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["cicd"], lang=Language.TYPESCRIPT)
    ci = (project / ".github" / "workflows" / "ci.yml").read_text()
    assert "bun" in ci


def test_docker_addon_creates_compose(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["docker"])
    assert (project / "docker-compose.yml").is_file()
    content = (project / "docker-compose.yml").read_text()
    assert "postgres" in content
    assert "redis" in content


def test_agent_project_addon(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["agent_project"])
    assert (project / ".claude" / "skills" / "fix-issue" / "SKILL.md").is_file()
    assert (project / ".claude" / "skills" / "review-code" / "SKILL.md").is_file()
    assert (project / ".claude" / "agents" / "security-reviewer.md").is_file()
    assert (project / ".claude" / "settings.json").is_file()


def test_devcontainer_addon_python(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["devcontainer"], lang=Language.PYTHON)
    dc = project / ".devcontainer" / "devcontainer.json"
    assert dc.is_file()
    content = dc.read_text()
    assert "python" in content


def test_devcontainer_addon_ts(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["devcontainer"], lang=Language.TYPESCRIPT)
    dc = project / ".devcontainer" / "devcontainer.json"
    assert dc.is_file()
    content = dc.read_text()
    assert "bun" in content


def test_multiple_addons(tmp_path: Path) -> None:
    project = _make_with_addons(tmp_path, ["cicd", "docker", "devcontainer"])
    assert (project / ".github" / "workflows" / "ci.yml").is_file()
    assert (project / "docker-compose.yml").is_file()
    assert (project / ".devcontainer" / "devcontainer.json").is_file()
