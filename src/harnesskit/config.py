"""Configuration model for project generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Language(Enum):
    """Supported programming languages."""

    PYTHON = "python"
    TYPESCRIPT = "typescript"


class ProjectType(Enum):
    """Supported project types."""

    LIBRARY = "library"
    CLI_TOOL = "cli_tool"
    MICROSERVICE = "microservice"
    WEB_APP = "web_app"


SERVER_TYPES: frozenset[ProjectType] = frozenset({ProjectType.MICROSERVICE, ProjectType.WEB_APP})

DEFAULT_ADDONS: dict[ProjectType, list[str]] = {
    ProjectType.LIBRARY: ["cicd"],
    ProjectType.CLI_TOOL: ["cicd"],
    ProjectType.MICROSERVICE: ["cicd", "docker"],
    ProjectType.WEB_APP: ["cicd"],
}


@dataclass
class ProjectConfig:
    """Holds all user selections for project generation.

    This is the single source of truth passed from prompts -> generator.
    """

    project_name: str
    description: str
    author: str
    language: Language
    project_type: ProjectType
    addons: list[str] = field(default_factory=lambda: list[str]())
    frontend_framework: str | None = None  # Only for TS Web App
    git_init: bool = True

    @property
    def project_slug(self) -> str:
        """Normalized project name for directory and package naming.

        Python: snake_case (dashes -> underscores)
        TypeScript: kebab-case (keeps dashes)
        """
        name = self.project_name.lower().strip()
        if self.language == Language.PYTHON:
            return name.replace("-", "_")
        return name.replace("_", "-")

    @property
    def needs_server(self) -> bool:
        """Whether this project type runs a server process."""
        return self.project_type in SERVER_TYPES

    @staticmethod
    def default_addons(project_type: ProjectType) -> list[str]:
        """Return default addon list for a project type."""
        return list(DEFAULT_ADDONS.get(project_type, []))

    def template_context(self) -> dict[str, object]:
        """Return a flat dict for Jinja2 template rendering."""
        return {
            "project_name": self.project_name,
            "project_slug": self.project_slug,
            "description": self.description,
            "author": self.author,
            "language": self.language.value,
            "project_type": self.project_type.value,
            "is_python": self.language == Language.PYTHON,
            "is_typescript": self.language == Language.TYPESCRIPT,
            "is_library": self.project_type == ProjectType.LIBRARY,
            "is_cli_tool": self.project_type == ProjectType.CLI_TOOL,
            "is_microservice": self.project_type == ProjectType.MICROSERVICE,
            "is_web_app": self.project_type == ProjectType.WEB_APP,
            "needs_server": self.needs_server,
            "addons": self.addons,
            "frontend_framework": self.frontend_framework,
            "git_init": self.git_init,
        }
