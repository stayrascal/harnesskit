"""Shared test fixtures."""

from __future__ import annotations

from harnesskit.config import Language, ProjectConfig, ProjectType


def make_config(
    name: str = "testproject",
    language: Language = Language.PYTHON,
    project_type: ProjectType = ProjectType.LIBRARY,
    addons: list[str] | None = None,
    git_init: bool = False,
) -> ProjectConfig:
    """Create a ProjectConfig for testing."""
    return ProjectConfig(
        project_name=name,
        description="A test project",
        author="testuser",
        language=language,
        project_type=project_type,
        addons=addons or [],
        git_init=git_init,
    )
