# HarnessKit

AI Native Repository Generator — create project repos optimized for AI code agents.

## Installation

```bash
pip install harnesskit
```

## Quick Start

```bash
hk new myproject
# or
harnesskit new myproject
```

## Development

```bash
make setup       # Initialize dev environment
make lint        # Ruff lint check
make format      # Ruff format
make typecheck   # Pyright type check
make test        # Run tests
make check       # Full check (lint + typecheck + test)
```

## Project Structure

```
harnesskit/
├── src/harnesskit/
│   ├── cli.py           # CLI entry point
│   ├── config.py        # Configuration model
│   ├── generator.py     # Generation engine
│   ├── prompts.py       # Interactive TUI
│   └── templates/       # Jinja2 templates
├── tests/               # Tests
├── CLAUDE.md            # AI agent instructions
└── Makefile             # Unified commands
```
