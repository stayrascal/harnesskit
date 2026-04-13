---
name: proactive_ci_verification
description: Proactively verify CI status after pushing changes
type: feedback
---

## Proactive CI Verification Rule

**Rule**: After pushing changes to GitHub, proactively check CI status and fix any failures without waiting for user to report them.

**Why**: Red X marks on commits indicate CI failures that should be addressed immediately. Waiting for user to report issues delays feedback and leaves the repository in a broken state.

**How to apply**:

1. **After every `git push`**: Run `gh api repos/<owner>/<repo>/commits/<sha>/statuses` to check commit status

2. **If status is "failure"**:
   - Identify which check failed (GitHub Actions, pre-commit.ci, etc.)
   - Use `gh run list` or `gh run view <run-id>` to get details
   - Analyze the error and fix it locally
   - Push the fix
   - Re-verify the new commit

3. **Common failure patterns**:
   - **pre-commit.ci ruff-format failure**: Version mismatch between local and CI
     - Fix: Update `.pre-commit-config.yaml` to match local ruff version
   - **pre-commit.ci "files were modified"**: Hook modified files during CI
     - Fix: Run the hook locally, commit changes, push again
   - **GitHub Actions test failure**: Tests failing in CI but passing locally
     - Fix: Check environment differences, update tests or dependencies

4. **For this project (harnesskit)**:
   - Always check pre-commit.ci status after push
   - Use `ghgh api repos/stayrascal/harnesskit/commits/<sha>/statuses`
   - If pre-commit.ci fails, check `https://results.pre-commit.ci/run/...` URL for details

5. **Verification command**:
   ```bash
   gh api repos/stayrascal/harnesskit/commits/$(git rev-parse HEAD)/statuses
   ```

**Remember**: A green checkmark on the latest commit is the definition of "done". Don't claim success until CI passes.
