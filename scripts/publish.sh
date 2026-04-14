#!/usr/bin/env bash
# Publish harnesskit to PyPI

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT_TOML="${REPO_ROOT}/pyproject.toml"
DIST_DIR="${REPO_ROOT}/dist"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

get_version() {
    grep "^version" "${PYPROJECT_TOML}" | head -1 | sed 's/version = "\(.*\)"/\1/' | tr -d '"'
}

check_git_clean() {
    if [[ -n "$(git status --porcelain)" ]]; then
        log_error "Working directory is not clean. Please commit or stash changes first."
        return 1
    fi
}

check_on_main() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [[ "${current_branch}" != "main" ]]; then
        log_warn "Not on main branch (current: ${current_branch})"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
}

run_checks() {
    log_info "Running pre-publish checks..."
    cd "${REPO_ROOT}"

    log_info "Running make check..."
    if ! make check; then
        log_error "Checks failed. Aborting."
        return 1
    fi

    log_info "Running make harness-check..."
    if ! make harness-check; then
        log_error "Harness check failed. Aborting."
        return 1
    fi

    log_info "All checks passed!"
}

build_package() {
    log_info "Building package..."
    cd "${REPO_ROOT}"

    make clean
    make build

    if [[ ! -d "${DIST_DIR}" ]] || [[ -z "$(ls -A "${DIST_DIR}")" ]]; then
        log_error "Build failed - no distribution files found."
        return 1
    fi

    log_info "Built packages:"
    ls -lh "${DIST_DIR}"
}

check_build() {
    log_info "Checking built package with twine..."
    cd "${REPO_ROOT}"

    if ! uv run twine check "${DIST_DIR}"/*; then
        log_error "Package check failed. Aborting."
        return 1
    fi

    log_info "Package check passed!"
}

publish_testpypi() {
    log_info "Publishing to TestPyPI..."
    cd "${REPO_ROOT}"

    if ! uv publish --index testpypi; then
        log_error "Publishing to TestPyPI failed."
        return 1
    fi

    log_info "Published to TestPyPI successfully!"
    log_info "Install with: pip install --index-url https://test.pypi.org/simple/ harnesskit"
}

publish_pypi() {
    log_info "Publishing to PyPI..."
    cd "${REPO_ROOT}"

    if ! uv publish --index pypi; then
        log_error "Publishing to PyPI failed."
        return 1
    fi

    log_info "Published to PyPI successfully!"
    log_info "Install with: pip install harnesskit"
}

create_git_tag() {
    local version=$1
    local tag_name="v${version}"

    log_info "Creating git tag: ${tag_name}"

    if git rev-parse "${tag_name}" >/dev/null 2>&1; then
        log_warn "Tag ${tag_name} already exists."
        read -p "Delete and recreate? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git tag -d "${tag_name}"
            git push origin ":refs/tags/${tag_name}" 2>/dev/null || true
        else
            return 0
        fi
    fi

    git tag -a "${tag_name}" -m "Release ${version}"
    git push origin "${tag_name}"

    log_info "Git tag pushed: ${tag_name}"
}

# Main
main() {
    cd "${REPO_ROOT}"

    local version
    version=$(get_version)
    log_info "Current version: ${version}"

    # Parse arguments
    local target="pypi"
    local skip_checks=false
    local skip_git_check=false
    local create_tag=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --testpypi)
                target="testpypi"
                shift
                ;;
            --skip-checks)
                skip_checks=true
                shift
                ;;
            --skip-git-check)
                skip_git_check=true
                shift
                ;;
            --tag)
                create_tag=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --testpypi        Publish to TestPyPI instead of PyPI"
                echo "  --skip-checks     Skip pre-publish checks"
                echo "  --skip-git-check   Skip git working directory check"
                echo "  --tag             Create and push git tag after publishing"
                echo "  --help            Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Git checks
    if [[ "${skip_git_check}" == "false" ]]; then
        check_git_clean || exit 1
        check_on_main || exit 1
    fi

    # Pre-publish checks
    if [[ "${skip_checks}" == "false" ]]; then
        run_checks || exit 1
    fi

    # Build
    build_package || exit 1
    check_build || exit 1

    # Confirm
    log_warn "About to publish harnesskit ${version} to ${target}"
    if [[ "${target}" == "pypi" ]]; then
        log_warn "This will publish to the public PyPI!"
    fi
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Aborted."
        exit 0
    fi

    # Publish
    if [[ "${target}" == "testpypi" ]]; then
        publish_testpypi || exit 1
    else
        publish_pypi || exit 1
    fi

    # Create git tag
    if [[ "${create_tag}" == "true" ]]; then
        create_git_tag "${version}"
    fi

    log_info "Done!"
}

main "$@"
