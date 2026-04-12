# Architecture Overview

## System Design

HarnessKit is a CLI tool that generates AI Native Repositories through layered template rendering.

## Core Components

```
CLI (click)
  → Prompts (questionary) → ProjectConfig
  → Generator (Jinja2)    → Rendered Project
```

| Component | File | Responsibility |
|-----------|------|---------------|
| CLI | `cli.py` | Entry point, `new` command, git init |
| Config | `config.py` | `ProjectConfig` dataclass, enums, validation |
| Prompts | `prompts.py` | Interactive TUI, input collection |
| Generator | `generator.py` | 4-layer template rendering engine |

## Template Layer Model

Rendering order (each layer overlays the previous):

1. **base/** — shared files (CLAUDE.md, AGENTS.md, Makefile, .gitignore, etc.)
2. **{lang}/_shared/** — language-level config (pyproject.toml / package.json)
3. **{lang}/{type}/** — project-type-specific source code
4. **{lang}/{type}/{framework}/** — frontend framework (TS Web App only)
5. **addons/{name}/** — optional layers (cicd, docker, agent_project, devcontainer)

## Key Design Decisions

- See `docs/adr/` for recorded ADRs
- Template engine: Jinja2 (see ADR-001)
- File naming: `.j2` suffix stripped, directory structure preserved
- No inheritance/includes between layers — simple file overlay
