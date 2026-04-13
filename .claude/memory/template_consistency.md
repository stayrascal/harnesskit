---
name: template_consistency
description: Ensure changes to project config are also reflected in templates
type: feedback
---

## Template-Project Consistency Rule

**Rule**: When modifying configuration files that have template counterparts, always check and update both the project file and the template file.

**Why**: This project (harnesskit) is a code generator. The `.pre-commit-config.yaml` in the root is the project's own config config, but `src/harnesskit/templates/**/.pre-commit-config.yaml.j2` are templates used to generate new projects. Changes to tooling configurations (ruff, biome, commitlint, etc.) must be applied to both to ensure consistency between the generator itself and the projects it generates.

**How to apply**:

1. **Before making changes**: Use `Glob` to find all related files
   - For `.pre-commit-config.yaml` → search `**/.pre-commit-config*`
   - For `pyproject.toml` → search `**/pyproject.toml*`
   - For `Makefile` → search `**/Makefile*`

2. **Identify template files**: Files under `src/harnesskit/templates/` with `.j2` extension are Jinja2 templates

3. **Decision framework**:
   - **Tooling version changes** (ruff, biome, eslint, etc.) → Update BOTH project and templates
   - **Project-specific settings** (author name, description) → Update ONLY templates
   - **Generator-specific settings** (harnesskit's own dependencies) → Update ONLY project
   - **Shared patterns** (lint rules, formatting style) → Update BOTH

4. **After making changes**: Run `make check` to verify both project and generated templates work correctly

**Examples**:
- ✅ Updating ruff version → Change `.pre-commit-config.yaml` AND `**/.pre-commit-config.yaml.j2`
- ✅ Adding new lint rule → Change project config AND template config
- ❌ Changing project name → Only change template (project name is a variable)
- ❌ Adding generator-specific dependency → Only change root `pyproject.toml`
