# ADR-001: Standalone Jinja2 Template Engine

## Status
Accepted

## Context
We considered using cookiecutter or copier as the template engine. Both are mature
but add heavy dependencies and constrain our template layout to their conventions.

## Decision
Use Jinja2 directly with a custom 3-layer template resolution system
(base → language shared → language+type).

## Consequences
- Full control over template rendering and path resolution
- Lighter dependency tree
- Must implement template discovery and rendering ourselves
- Can evolve template structure without upstream constraints
