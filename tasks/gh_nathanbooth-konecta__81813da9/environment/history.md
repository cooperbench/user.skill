> AGENT

Looking at the "Generate image metadata" step (line 153), the non-prod branch already builds tags including the SHA and a branch-specific prefix. To add a `develop` tag when the source branch is `develop`, I just need to append it to the `TAGS` string in that conditional block.

> AGENT

Done. When the source branch is `develop`, the image will now be pushed with an additional `develop` tag alongside the existing `<sha>`, `dev-<sha>`, and `latest` tags. This is added at [docker-build-push.yml:183-186](.github/workflows/docker-build-push.yml#L183-L186).

> AGENT

Now let me create a branch, commit, and push.

> AGENT

The diff looks correct - both files have the same `develop` tag addition. Let me create a new branch, commit, and push.

> AGENT

Done. Branch `feature/develop-docker-tag` has been pushed with changes to both workflow files:

- [docker-build-push.yml](.github/workflows/docker-build-push.yml#L182-L185) - added `develop` tag
- [docker-build-push-python.yml](.github/workflows/docker-build-push-python.yml#L541-L545) - added `develop` tag

When the source branch is `develop`, images will now be tagged with `<sha>`, `dev-<sha>`, `latest`, and `develop`.

Want me to create a PR for this?

> DEVELOPER

yes

> AGENT

PR created: https://github.com/konecta-ix-applications/.github-private/pull/3

> DEVELOPER

rebase on develop

> AGENT

There's no `develop` branch on the remote. Let me check what branches are available.

> AGENT

No `develop` branch exists on this remote. The available branches are:

- `main`
- `feat/shared-reusable-workflows`
- `feature/develop-docker-tag` (current)
- `feature/python-build`

Which branch did you want to rebase onto?

> DEVELOPER

main

> AGENT

Already up to date with `main` — no changes needed.

> DEVELOPER

review this PR for me https://github.com/konecta-ix-applications/.github-private/pull/2/changes

> AGENT

Here's my review of PR #2:

## PR #2: Feature/python build

**Summary:** Adds a new reusable workflow `docker-build-push-python.yml` that combines Python CI (lint, format, type check, test, security scan) with the existing Docker build/push/scan/sign pipeline.

---

### Issues

**1. CI failures don't block the Docker build** (lines 218-222, 456)

All CI steps use `continue-on-error: true`, and the `build-push` job has `needs: ci` with no condition checking CI outcomes. This means the Docker build will proceed even if linting, tests, or security scans fail. The CI job outputs (`lint_passed`, `tests_passed`, etc.) are set but never consumed by the `build-push` job. If CI is meant to be a gate, `build-push` needs an `if:` condition like:

```yaml
if: needs.ci.outputs.tests_passed == 'true'
```

Otherwise the CI job is purely informational, which should be documented.

**2. Bandit step has redundant error suppression** (line 277)

The step uses both `continue-on-error: true` and `|| true` at the end of the command. The `|| true` masks the exit code, so `steps.security.outcome` will always be `success` even when bandit finds issues. The `security_passed` output will therefore always be `true`. Same issue with `pip-audit` on line 301.

**3. Environment naming inconsistency** (line 131)

The `environment` input description says `(dev, stg, […]

> DEVELOPER

could the outputting of the result be improved?

> AGENT

Yes, a few ways:

**1. Reduce the repetitive if/else blocks with a helper function**

The CI Summary step (lines 376-449) repeats the same pattern 6 times. A bash function would cut that significantly:

```bash
report_check() {
  local name="$1" enabled="$2" outcome="$3"
  if [ "$enabled" == "true" ]; then
    if [ "$outcome" == "success" ]; then
      echo "| $name | Passed |" >> $GITHUB_STEP_SUMMARY
    else
      echo "| $name | **FAILED** |" >> $GITHUB_STEP_SUMMARY
    fi
  else
    echo "| $name | Skipped |" >> $GITHUB_STEP_SUMMARY
  fi
}

report_check "Ruff Lint" "${{ inputs.enable_lint }}" "${{ steps.lint.outcome }}"
report_check "Ruff Format" "${{ inputs.enable_format_check }}" "${{ steps.format-check.outcome }}"
# ...etc
```

**2. Show all tags in the Docker Summary**

The Docker summary only shows the primary `image_uri`. It would be more useful to list all tags that were pushed, since callers may need to reference them:

```bash
echo "**Tags:**" >> $GITHUB_STEP_SUMMARY
IFS=',' read -ra TAG_ARRAY <<< "${{ steps.meta.outputs.tags }}"
for t in "${TAG_ARRAY[@]}"; do
  echo "- \`${t}\`" >> $GITHUB_STEP_SUMMARY
done
```

**3. Surface CI results in the Docker summary too**

The two jobs produce separate summaries, so the Docker summary has no indication of CI health. Adding a row like `| Python CI | Passed (85% coverage) […]

> DEVELOPER

rebase on develop, and implement all of the fixes above

> AGENT

Now let me re-read both files after the rebase to work from the current state.

> AGENT

Now let me implement all the fixes. Starting with the Python workflow.

**Fix 1: CI gate on build-push job + Fix 2: Remove `|| true` from bandit/pip-audit + Fix 3: Environment naming + Fix 5: Cosign scan check + Fix 6: pip cache-dependency-path + Fix 7: Use trivy_severity input + Fix 8: Improve summaries**

> AGENT

Now add the CI gate condition to the build-push job.

> AGENT

Now fix cosign to check scan result.

> AGENT

Now fix the trivy_severity usage (replace hardcoded values in both Trivy steps).

> AGENT

Now the big one — replace the CI Summary and Docker Summary with improved versions.

> AGENT

Now replace the Docker Summary step.

> AGENT

Let me verify the Python file looks correct after all edits, then move on to the base workflow.

> AGENT

Python workflow looks good. Now let me apply matching fixes to the base `docker-build-push.yml`.

> AGENT

Now apply the matching fixes to the base workflow: cosign scan check, trivy_severity input, and improved summary.

> AGENT

Now replace the Summary step in the base workflow with the improved version.

> AGENT

Now let me check the diff and commit.

> AGENT

Diff looks correct. Let me commit and push.

> AGENT

Pushed to `fix/workflow-improvements`. All fixes applied to both workflows:

1. **CI gate** - `build-push` job now skipped if tests fail (`if: needs.ci.outputs.tests_passed == 'true'`)
2. **Bandit/pip-audit** - removed `|| true` so `continue-on-error` properly tracks outcomes
3. **Environment naming** - corrected to `(dev, qa, prd)`
4. **Cosign** - now checks `enable_cosign`, `push`, and `scan_passed` before signing
5. **pip cache** - added `cache-dependency-path` for non-root working directories
6. **trivy_severity** - Trivy steps now use the input instead of hardcoded values
7. **CI Summary** - refactored with `report_check()` helper function
8. **Docker Summary** - uses heredocs for static blocks and lists all pushed tags

Want me to create a PR for this?

> AGENT

Scanning before pushing is a better practice — it prevents vulnerable images from reaching the registry at all. However, there's a constraint with cosign: keyless signing operates on the image digest in the registry, so signing must happen after push.

The improved flow would be:

1. **Build** (load locally, don't push yet)
2. **Trivy scan** the local image
3. **Push** only if scan passes
4. **Cosign sign** the pushed image

The main change is splitting the `docker/build-push-action` into a local build first (`push: false`, `load: true`), then a separate push step gated on scan results. Want me to implement that?