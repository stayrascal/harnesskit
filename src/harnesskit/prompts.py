"""Interactive TUI prompts using questionary.

Collects user input and returns a ProjectConfig.
"""

from __future__ import annotations

import re

import questionary

from harnesskit.config import Language, ProjectConfig, ProjectType

LANGUAGE_CHOICES: list[dict[str, str]] = [
    {"name": "Python", "value": "python"},
    {"name": "TypeScript", "value": "typescript"},
]

PROJECT_TYPE_CHOICES: list[dict[str, str]] = [
    {"name": "Library", "value": "library"},
    {"name": "CLI Tool", "value": "cli_tool"},
    {"name": "Microservice", "value": "microservice"},
    {"name": "Web App", "value": "web_app"},
]

ADDON_CHOICES: list[dict[str, str]] = [
    {"name": "CI/CD (GitHub Actions)", "value": "cicd"},
    {"name": "Docker Compose", "value": "docker"},
    {"name": "Agent Project (.claude/skills, agents, hooks)", "value": "agent_project"},
    {"name": "DevContainer", "value": "devcontainer"},
]

_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*$")


def validate_project_name(name: str) -> bool | str:
    """Validate project name. Returns True if valid, error string if not."""
    if not name:
        return "Project name cannot be empty"
    if not _NAME_PATTERN.match(name):
        return "Must start with lowercase letter, contain only [a-z0-9_-]"
    return True


def get_addon_defaults(project_type: ProjectType) -> list[str]:
    """Return default addon selections for a project type."""
    return ProjectConfig.default_addons(project_type)


def collect_inputs(project_name: str | None = None) -> ProjectConfig:
    """Run interactive prompts and return a ProjectConfig.

    Args:
        project_name: If provided, skip the project name prompt.
    """
    project: str = project_name or questionary.text(
        "Project name:",
        validate=validate_project_name,
    ).unsafe_ask()

    description: str = questionary.text(
        "Description:",
        default="",
    ).unsafe_ask()

    author: str = questionary.text(
        "Author:",
        default="",
    ).unsafe_ask()

    language_value: str = questionary.select(
        "Language:",
        choices=[questionary.Choice(c["name"], value=c["value"]) for c in LANGUAGE_CHOICES],
    ).unsafe_ask()
    language = Language(language_value)

    type_value: str = questionary.select(
        "Project type:",
        choices=[questionary.Choice(c["name"], value=c["value"]) for c in PROJECT_TYPE_CHOICES],
    ).unsafe_ask()
    project_type = ProjectType(type_value)

    # Frontend framework choice (TS Web App only)
    frontend_framework: str | None = None
    if language == Language.TYPESCRIPT and project_type == ProjectType.WEB_APP:
        frontend_framework = questionary.select(
            "Frontend framework:",
            choices=[
                questionary.Choice("React (Vite + React)", value="react"),
                questionary.Choice("Vue (Vite + Vue)", value="vue"),
                questionary.Choice("Hono JSX (lightweight SSR)", value="hono_jsx"),
                questionary.Choice("None (API + static files only)", value="none"),
            ],
        ).unsafe_ask()

    defaults = get_addon_defaults(project_type)
    addon_values: list[str] = questionary.checkbox(
        "Select addons:",
        choices=[
            questionary.Choice(c["name"], value=c["value"], checked=c["value"] in defaults)
            for c in ADDON_CHOICES
        ],
    ).unsafe_ask()

    git_init: bool = questionary.confirm(
        "Initialize git repo and make first commit?",
        default=True,
    ).unsafe_ask()

    return ProjectConfig(
        project_name=project,
        description=description,
        author=author,
        language=language,
        project_type=project_type,
        addons=addon_values,
        frontend_framework=frontend_framework,
        git_init=git_init,
    )
