#!/usr/bin/env bash
# harness-check.sh — Validate harness engineering practices for harnesskit itself
set -euo pipefail

errors=0
warns=0

info()  { echo "  [INFO]  $*"; }
warn()  { echo "  [WARN]  $*"; warns=$((warns + 1)); }
error() { echo "  [ERROR] $*"; errors=$((errors + 1)); }

echo "=== Harness Check: harnesskit ==="

# 1. CLAUDE.md length
if [ -f "CLAUDE.md" ]; then
    claude_lines=$(wc -l < CLAUDE.md)
    if [ "$claude_lines" -gt 80 ]; then
        warn "CLAUDE.md is $claude_lines lines (target ≤80)"
    else
        info "CLAUDE.md: $claude_lines lines — OK"
    fi
else
    error "CLAUDE.md not found"
fi

# 2. AGENTS.md exists
if [ -f "AGENTS.md" ]; then
    info "AGENTS.md found"
else
    error "AGENTS.md not found"
fi

# 3. Makefile targets
if [ -f "Makefile" ]; then
    for target in lint lint-fix format typecheck test check; do
        if grep -q "^${target}:" Makefile; then
            info "Makefile target '$target' — OK"
        else
            error "Makefile missing target: $target"
        fi
    done
else
    error "Makefile not found"
fi

# 4. Commit lint config (conventional-pre-commit in .pre-commit-config.yaml)
if [ -f ".pre-commit-config.yaml" ]; then
    if grep -q "conventional-pre-commit\|commitlint" .pre-commit-config.yaml; then
        info "Commit message linting configured"
    else
        warn "No commit message linting in .pre-commit-config.yaml"
    fi
else
    error ".pre-commit-config.yaml not found"
fi

# 5. File size checks (src only)
echo ""
echo "--- File size check (src/) ---"
while IFS= read -r -d '' f; do
    lines=$(wc -l < "$f")
    if [ "$lines" -gt 1000 ]; then
        error "$f: $lines lines (max 1000)"
    elif [ "$lines" -gt 500 ]; then
        warn "$f: $lines lines (target <500)"
    elif [ "$lines" -gt 300 ]; then
        info "$f: $lines lines (consider splitting)"
    fi
done < <(find src/ -name "*.py" -print0)

# 6. Test directory exists
if [ -d "tests" ]; then
    test_count=$(find tests/ -name "test_*.py" | wc -l)
    info "Found $test_count test files"
else
    error "tests/ directory not found"
fi

# 7. Strict type checking configured
if [ -f "pyproject.toml" ]; then
    if grep -q 'typeCheckingMode.*=.*"strict"' pyproject.toml; then
        info "pyright strict mode enabled"
    else
        warn "pyright strict mode not configured"
    fi
else
    error "pyproject.toml not found"
fi

# Summary
echo ""
echo "=== Summary: $errors error(s), $warns warning(s) ==="
if [ "$errors" -gt 0 ]; then
    exit 1
fi
