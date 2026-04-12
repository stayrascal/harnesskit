"""CLI entry point for harnesskit.

Commands:
    hk new [name]  -- Generate a new AI Native Repository
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import click
from rich.console import Console

from harnesskit import __version__
from harnesskit.generator import ProjectGenerator
from harnesskit.prompts import collect_inputs

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="harnesskit")
def main() -> None:
    """HarnessKit -- AI Native Repository Generator."""


@main.command()
@click.argument("name", required=False)
@click.option("--output-dir", type=click.Path(path_type=Path), default=None, help="Output directory")
def new(name: str | None, output_dir: Path | None) -> None:
    """Generate a new AI Native Repository."""
    console.print("\n[bold]HarnessKit[/bold] -- AI Native Repository Generator\n")

    config = collect_inputs(project_name=name)
    target = output_dir or Path.cwd()

    generator = ProjectGenerator(config=config, output_dir=target)

    try:
        project_path = generator.generate()
    except FileExistsError as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise SystemExit(1) from e

    if config.git_init:
        _git_init(project_path)

    lang_label = config.language.value.title()
    type_label = config.project_type.value.replace("_", " ").title()
    console.print(f"\n Created [bold green]{config.project_name}/[/bold green]" +
                  f" with {lang_label} + {type_label} template")

    if config.addons:
        console.print(f"   Addons: {', '.join(config.addons)}")

    console.print("\n Next steps:")
    console.print(f"   cd {config.project_name}")
    console.print("   make setup")
    if config.needs_server:
        console.print("   make dev")
    console.print()


def _git_init(project_path: Path) -> None:
    """Initialize git repo and make first commit."""
    try:
        subprocess.run(["git", "init"], cwd=project_path, capture_output=True, check=True)  # noqa: S603, S607
        subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True, check=True)  # noqa: S603, S607
        subprocess.run(  # noqa: S603, S607
            ["git", "commit", "-m", "feat: initial project scaffold by harnesskit"],
            cwd=project_path,
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[yellow]Warning:[/yellow] Git init failed, skipping.")
