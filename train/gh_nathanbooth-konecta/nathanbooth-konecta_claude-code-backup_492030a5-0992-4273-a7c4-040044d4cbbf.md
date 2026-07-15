> DEVELOPER

Implement the following plan:

# Replace workflow_dispatch with GitHub Issue Forms

## Context

The current image request flow requires users to navigate to the Actions tab, find the workflow, click "Run workflow", and fill in a dispatch form. GitHub Issue Forms provide a much better UX: users click "New Issue", pick the template, and fill in a rich form. A workflow triggers automatically on issue creation, processes the request, and comments back with a PR link.

## Files to Create

### 1. `.github/ISSUE_TEMPLATE/request-image.yml`

Issue Form template with fields matching the current workflow inputs:
- `registry` — dropdown (dockerhub, ghcr, quay, custom)
- `image_name` — text input
- `tag` — text input
- `description` — text input (optional)
- `custom_host` — text input (optional, for custom registries)
- `auth_required` — checkbox
- `justification` — textarea

Auto-applies label `image-request` on issue creation (this triggers the workflow).

### 2. `.github/ISSUE_TEMPLATE/config.yml`

Minimal config — `blank_issues_enabled: true`.

### 3. `.github/workflows/process-image-request.yml`

New workflow triggered by `issues: opened` with `image-request` label.

**Permissions:** `contents: write`, `issues: write`

**Steps:**
1. Checkout main
2. Setup Python 3.12 + install ruamel.yaml/pyyaml
3. **Parse issue body** — extract fields from the markdown rendered by Issue Forms (`### Heading` / value pairs) using `awk`/`sed` in bash. Issue body passed via `env:` (not `${{ }}` interpolation) to prevent script injection.
4. Derive target name (last path segment)
5. Run `scripts/add-image.py` with parsed values
6. Run `scripts/validate-manifest.py`
7. Create branch `image-request/<issue#>-<target>-<tag>` and push
8. **On success:** Comment on issue with PR creation link via `actions/github-script@v7`
9. **On failure:** Comment on issue with error + link to workflow run, add `failed` label

## Files to Modify

### 4. `.github/workflows/request-image.yml`

Add deprecation notice — rename to `[Deprecated] Request Container Image` and add a warning step pointing users to the issue form. Keep the workflow functional during transition.

### 5. `README.md`

- Update badge link: point to `issues/new?template=request-image.yml` instead of Actions workflow
- Update steps: "Open an issue" instead of "Run workflow"
- Update flow diagram to reflect issue-based flow
- Update files table with new files

### 6. `CLAUDE.md`

Update file references and workflow table to reflect new issue-based flow.

## Security

- Issue body is passed via `env: ISSUE_BODY` variable, **not** interpolated into `run:` blocks — prevents script injection from malicious issue content
- Branch names include issue number to avoid collisions

## Verification

1. After merge, go to **Issues > New issue** — confirm the form template appears
2. Submit a test issue — confirm the workflow triggers, parses fields, creates a branch, and comments back
3. Test edge cases: optional fields left blank (`_No response_`), checkbox checked/unchecked, custom registry
4. Confirm old workflow still works but shows deprecation warning


If you need specific details from before exiting plan mode (like exact code snippets, error messages, or content you generated), read the full transcript at: /home/nathan_booth/.claude/projects/-home-nathan-booth-code-konecta-ix-platform-kix-platform-images/492030a5-0992-4273-a7c4-040044d4cbbf.jsonl

> AGENT

I'll start by reading the existing files I need to modify, then implement all changes.

> AGENT

Now I have all the context needed. Let me also check if the `.github/ISSUE_TEMPLATE` directory exists.

> AGENT

Now I'll create all the new files and modify the existing ones. Let me create the task list and work through everything.

> AGENT

Now the main workflow. The key security concern is parsing the issue body without interpolating it into `run:` blocks.

> AGENT

Let me fix a bug in the failure step — `repo` variable needs to be `context.repo`.

> AGENT

Now add the deprecation notice to the old workflow.

> AGENT

Now add a deprecation warning step at the beginning of the job steps.

> AGENT

Now update the README.

> AGENT

Now update CLAUDE.md — the data flow, file structure, workflow table, and workflow details sections.

> AGENT

Now update the Workflow Details section for the Request Image workflow.

> AGENT

Now update the Development Notes section that references the old workflow.

> AGENT

Let me do a final review of all the created/modified files to make sure everything is correct.

> AGENT

Everything looks good. Let me verify the final state of the README and CLAUDE.md as well.

> AGENT

All files look correct. Let me verify the git status to confirm all changes are tracked.

> AGENT

All changes are in place. Here's a summary of what was implemented:

**New files created:**

1. **`.github/ISSUE_TEMPLATE/request-image.yml`** — Issue Form template with all fields matching the old workflow inputs: registry dropdown, image name/tag inputs, optional description and custom host, auth checkbox, and justification textarea. Auto-applies the `image-request` label.

2. **`.github/ISSUE_TEMPLATE/config.yml`** — Minimal config allowing blank issues.

3. **`.github/workflows/process-image-request.yml`** — New workflow triggered on `issues: opened` with the `image-request` label. It:
   - Parses the issue body using `awk`/`sed` via `env: ISSUE_BODY` (not `${{ }}` interpolation) to prevent script injection
   - Handles `_No response_` for optional fields
   - Parses the checkbox for auth_required
   - Runs `add-image.py` and `validate-manifest.py`
   - Creates branch `image-request/<issue#>-<target>-<tag>` (includes issue number to avoid collisions)
   - On success: comments on issue with a PR creation link
   - On failure: comments with error details and adds `failed` label

**Modified files:**

4. **`.github/workflows/request-image.yml`** — Renamed to `[Deprecated] Request Container Image` with a deprecation warning step at the top that points users to the issue form. Still fully functional.

5. **`README.md`** — Badge now links to `issues/new?template=request-image.yml`, steps updated for issue-based flow, flow diagram updated, files table includes new files.

6. **`CLAUDE.md`** — Data flow, file structure (new Issue Templates section), workflow table, and workflow details all updated to reflect the issue-based flow.

> DEVELOPER

also add a check on PR thats mandatory that validates images.yaml

> AGENT

The workflow already exists but only triggers on PRs that modify `images.yaml` (via `paths: [images.yaml]`). The issue is that with the `paths` filter, the check won't appear as a required status check on PRs that don't touch `images.yaml` — and for PRs that do touch it, it needs to be configured as required in branch protection rules. But the workflow itself only runs conditionally, which makes it unsuitable as a required check (GitHub marks path-filtered required checks as "expected" and blocks merge when the file isn't changed).

The standard fix is to make the workflow always trigger on PRs, then skip gracefully when `images.yaml` isn't changed — so it always reports a green status.

> AGENT

The change removes `paths: [images.yaml]` from the trigger so the workflow runs on **every PR**, making it eligible as a required status check in branch protection. When `images.yaml` isn't modified, it detects that early and skips validation/summary steps (passing green). When it is modified, it runs the full validation.

To make this mandatory, you'll need to add `validate` (the job name) as a required status check in your branch protection rules for `main` in the repo settings (Settings > Branches > Branch protection rule for `main` > Require status checks > search for "validate").

> DEVELOPER

ok, commit and push

> AGENT

Committed and pushed as `be2c75a` to `feat/image-request-workflow-v2`. The 7 files changed:

- **Created:** `.github/ISSUE_TEMPLATE/request-image.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/workflows/process-image-request.yml`
- **Modified:** `.github/workflows/request-image.yml` (deprecation notice), `.github/workflows/validate-manifest.yml` (runs on all PRs for required check), `README.md`, `CLAUDE.md`

To make the validation check mandatory, add `validate` as a required status check in your branch protection rules for `main` (Settings > Branches > `main` rule > Require status checks).

> DEVELOPER

does the blue image pass accessiblity tests?

> AGENT

The badge uses white text on `#2088FF`:

```
https://img.shields.io/badge/...-2088FF?style=for-the-badge&logoColor=white
```

The contrast ratio of white (`#FFFFFF`) on `#2088FF` is approximately **3.5:1**.

- **WCAG AA normal text (4.5:1):** Fails
- **WCAG AA large text (3:1):** Passes — the `for-the-badge` style renders large bold text, so this technically qualifies
- **WCAG AAA (7:1):** Fails

It's borderline. If you want to be safe and meet AA for normal text, you could darken the blue. For example, `#0969DA` bumps the ratio to ~4.5:1. Want me to update it?

> DEVELOPER

does the blue request button  pass accessiblity tests?

> AGENT

I covered this in my previous response — the badge at `#2088FF` with white text has a contrast ratio of ~3.5:1. It passes WCAG AA for large text (3:1) but fails for normal text (4.5:1). Want me to darken the blue to something like `#0969DA` to meet the stricter threshold?

> DEVELOPER

ok, lets improve it

> AGENT

Updated the badge color from `#2088FF` to `#0969DA`. This brings the contrast ratio with white text to ~4.5:1, passing WCAG AA for normal text.

> DEVELOPER

can you plan for me a seperate workflow to pull down images from CrewAI, it's an authenticated registry, i'll supply CREWAI_USER and CREWAI_TOKEN via github secrets fo pulling the images from images.crewai.com, can you just pull all the images from there? as i dont know which i need, and put them into a seperate path on the existing GCP artifact repository

> AGENT

Let me explore the existing sync workflow to understand the current patterns, and research what CrewAI's registry looks like.

> AGENT

I have a few questions before putting the plan together.

> AGENT

Good, I have the full picture. Let me write the plan.
