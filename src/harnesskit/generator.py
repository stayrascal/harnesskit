"""Project generation engine.

Resolves template layers, renders Jinja2 templates, writes output files.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, StrictUndefined

if TYPE_CHECKING:
    from harnesskit.config import ProjectConfig

TEMPLATES_DIR = Path(__file__).parent / "templates"


class ProjectGenerator:
    """Generates a project from a ProjectConfig using layered Jinja2 templates.

    Layer 1: base/              -> Files every project gets
    Layer 2: {lang}/_shared     -> Language shared files
    Layer 3: {lang}/{type}/     -> Language + type specific files
    Layer 4: {lang}/{type}/{fw} -> Frontend framework (TS Web App only)
    """

    def __init__(self, config: ProjectConfig, output_dir: Path | None = None) -> None:
        self.config = config
        self.output_dir = output_dir or Path.cwd()
        self.project_dir = self.output_dir / self.config.project_name
        self.context = self.config.template_context()
        self._env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )

    def generate(self) -> Path:
        """Generate the full project. Returns the project directory path."""
        if self.project_dir.exists():
            msg = f"Directory already exists: {self.project_dir}"
            raise FileExistsError(msg)

        self.project_dir.mkdir(parents=True)

        self._render_layer("base")
        lang = self.config.language.value
        self._render_layer(f"{lang}/_shared")
        self._render_layer(f"{lang}/{self.config.project_type.value}")

        # TS Web App: render frontend framework sub-layer
        if self.config.frontend_framework:
            fw_layer = f"{lang}/{self.config.project_type.value}/{self.config.frontend_framework}"
            self._render_layer(fw_layer)

        # Addons
        for addon_name in self.config.addons:
            addon_layer = f"addons/{addon_name}"
            self._render_layer(addon_layer)

        self._make_scripts_executable()

        return self.project_dir

    def _render_layer(self, layer_path: str) -> None:
        """Render all templates in a layer directory to the project dir."""
        layer_dir = TEMPLATES_DIR / layer_path
        if not layer_dir.is_dir():
            return

        for template_file in layer_dir.rglob("*.j2"):
            rel_path = template_file.relative_to(layer_dir)
            # Remove .j2 extension
            output_rel = Path(str(rel_path)[:-3])
            # Resolve {{project_slug}} in path components
            output_rel = self._resolve_path_vars(output_rel)
            output_path = self.project_dir / output_rel

            # Render template
            template_key = f"{layer_path}/{rel_path}"
            template = self._env.get_template(template_key.replace(os.sep, "/"))
            content = template.render(self.context)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)

    def _resolve_path_vars(self, path: Path) -> Path:
        """Replace {{project_slug}} in path components with actual slug."""
        parts: list[str] = []
        for part in path.parts:
            resolved = part.replace("{{project_slug}}", self.config.project_slug)
            parts.append(resolved)
        return Path(*parts) if parts else path

    def _make_scripts_executable(self) -> None:
        """Make shell scripts in scripts/ executable."""
        scripts_dir = self.project_dir / "scripts"
        if scripts_dir.is_dir():
            for script in scripts_dir.glob("*.sh"):
                current = script.stat().st_mode
                script.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
