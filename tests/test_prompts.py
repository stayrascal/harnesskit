"""Tests for interactive prompts module."""

from harnesskit.config import Language, ProjectType
from harnesskit.prompts import (
    LANGUAGE_CHOICES,
    PROJECT_TYPE_CHOICES,
    get_addon_defaults,
    validate_project_name,
)


def test_validate_project_name_valid() -> None:
    """Valid project names pass validation."""
    assert validate_project_name("myproject") is True
    assert validate_project_name("my-project") is True
    assert validate_project_name("my_project") is True
    assert validate_project_name("project123") is True


def test_validate_project_name_invalid() -> None:
    """Invalid project names return error string."""
    result = validate_project_name("")
    assert isinstance(result, str)
    result = validate_project_name("My Project")
    assert isinstance(result, str)
    result = validate_project_name("123start")
    assert isinstance(result, str)
    result = validate_project_name(".hidden")
    assert isinstance(result, str)


def test_language_choices_match_enum() -> None:
    """Language choices cover all Language enum values."""
    choice_values = {c["value"] for c in LANGUAGE_CHOICES}
    enum_values = {lang.value for lang in Language}
    assert choice_values == enum_values


def test_project_type_choices_match_enum() -> None:
    """Project type choices cover all ProjectType enum values."""
    choice_values = {c["value"] for c in PROJECT_TYPE_CHOICES}
    enum_values = {pt.value for pt in ProjectType}
    assert choice_values == enum_values


def test_get_addon_defaults_for_microservice() -> None:
    """Microservice has cicd and docker pre-selected."""
    defaults = get_addon_defaults(ProjectType.MICROSERVICE)
    assert "cicd" in defaults
    assert "docker" in defaults


def test_get_addon_defaults_for_library() -> None:
    """Library has only cicd pre-selected."""
    defaults = get_addon_defaults(ProjectType.LIBRARY)
    assert defaults == ["cicd"]
