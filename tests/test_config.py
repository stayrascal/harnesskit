"""Tests for harnesskit config model."""

from harnesskit.config import Language, ProjectConfig, ProjectType


def test_project_config_creation() -> None:
    """ProjectConfig can be created with required fields."""
    config = ProjectConfig(
        project_name="myproject",
        description="Test project",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_name == "myproject"
    assert config.project_slug == "myproject"
    assert config.language == Language.PYTHON
    assert config.project_type == ProjectType.LIBRARY
    assert config.addons == []
    assert config.git_init is True


def test_project_slug_normalizes_dashes() -> None:
    """Project slug converts dashes to underscores for Python."""
    config = ProjectConfig(
        project_name="my-cool-project",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_slug == "my_cool_project"


def test_project_slug_keeps_dashes_for_typescript() -> None:
    """Project slug keeps dashes for TypeScript (kebab-case)."""
    config = ProjectConfig(
        project_name="my-cool-project",
        description="",
        author="testuser",
        language=Language.TYPESCRIPT,
        project_type=ProjectType.LIBRARY,
    )
    assert config.project_slug == "my-cool-project"


def test_project_config_with_addons() -> None:
    """ProjectConfig accepts addon list."""
    config = ProjectConfig(
        project_name="myproject",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.MICROSERVICE,
        addons=["cicd", "docker"],
    )
    assert config.addons == ["cicd", "docker"]


def test_default_addons_for_microservice() -> None:
    """Microservice should have cicd and docker as default addons."""
    defaults = ProjectConfig.default_addons(ProjectType.MICROSERVICE)
    assert "cicd" in defaults
    assert "docker" in defaults


def test_default_addons_for_library() -> None:
    """Library should have only cicd as default addon."""
    defaults = ProjectConfig.default_addons(ProjectType.LIBRARY)
    assert defaults == ["cicd"]


def test_template_context_returns_dict() -> None:
    """template_context() returns a dict suitable for Jinja2 rendering."""
    config = ProjectConfig(
        project_name="myproject",
        description="A test",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.CLI_TOOL,
    )
    ctx = config.template_context()
    assert ctx["project_name"] == "myproject"
    assert ctx["project_slug"] == "myproject"
    assert ctx["description"] == "A test"
    assert ctx["author"] == "testuser"
    assert ctx["language"] == "python"
    assert ctx["project_type"] == "cli_tool"
    assert ctx["is_python"] is True
    assert ctx["is_typescript"] is False
    assert ctx["is_microservice"] is False
    assert ctx["is_web_app"] is False
    assert ctx["is_cli_tool"] is True
    assert ctx["is_library"] is False
    assert ctx["needs_server"] is False


def test_needs_server_for_microservice() -> None:
    """Microservice needs server."""
    config = ProjectConfig(
        project_name="myproject",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.MICROSERVICE,
    )
    assert config.needs_server is True


def test_needs_server_false_for_library() -> None:
    """Library does not need server."""
    config = ProjectConfig(
        project_name="myproject",
        description="",
        author="testuser",
        language=Language.PYTHON,
        project_type=ProjectType.LIBRARY,
    )
    assert config.needs_server is False
