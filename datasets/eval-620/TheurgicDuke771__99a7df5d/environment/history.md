> DEVELOPER

Can you optimize and update the QA verifier and UI tester agents as required.
one of the sample bug to refer for UI tester - https://github.com/TheurgicDuke771/DataQ/issues/617 [this is just one example don't be influenced by this]

> AGENT

I'll look at the current agent definitions and the referenced issue to understand what needs updating.

> TOOL

tool_use Bash
id: toolu_0126uwSnACrbF6JNHs6bazMq
```json
{
  "command": "ls /home/<USER>/Coding/Python/DataQ/.claude/agents/",
  "description": "List agent definitions"
}
```

> TOOL

tool_result
id: toolu_0126uwSnACrbF6JNHs6bazMq
```
docs-consistency-guard.md
entire-search.md
migration-safety.md
orchestration-abstraction-guard.md
qa-verifier.md
ui-tester.md
```

> TOOL

tool_use Bash
id: toolu_01Y3SPzdj2FEtYmYJzm4tjUw
```json
{
  "command": "gh issue view 617 --repo TheurgicDuke771/DataQ --json title,body,labels,state,comments --jq '{title, state, labels: [.labels[].name], body} '",
  "description": "Fetch issue #617 details"
}
```

> TOOL

tool_result
id: toolu_01Y3SPzdj2FEtYmYJzm4tjUw
```
{"body":"## Summary\n\nThe app is effectively unusable on a mobile / narrow viewport. Several layouts were built for desktop widths only and never collapse, stack, or provide horizontal scroll. Originally reported from a phone (screenshots): tables have no scrollbar and columns are cut off, and the **suite detail** page renders its title/description **one character per line**.\n\nI swept every top-level screen with Playwright at a **390×844** viewport (iPhone-class, dev-bypass auth, seeded demo data). The reported issues reproduce and there are more of the same family. Grouped below by root cause, most severe first.\n\nTested routes: `/dashboard`, `/connections`, `/suites`, `/suites/:id`, `/results` (Runs + Pipeline runs), `/results/:runId`, `/profile`, `/settings`, `/admin`, `/suites/:id/checks/new` (+ form).\n\n---\n\n### Bug 1 — Suite detail two-panel layout never stacks → title/description wrap one char per line (**critical**, the primary report)\n\n**Repro:** open any suite (`/suites/:id`) at ≤ ~430px wide.\n\n**Observed:** the list panel + detail panel stay side-by-side. The detail pane is squeezed to a ~20px sliver on the far right, so the suite title and description render vertically (one character per line), largely off-screen. The per-suite notification section (`Send alerts for this suite`, `Teams webhook`) does the same.\n\n**Measured (Playwright `getBoundingClientRect`):** the detail `\u003ch4\u003e` title is **60px wide × 224px […]

> TOOL

tool_use Read
id: toolu_01Y3sUDqk4f8DLo1A8wYjbLC
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md"
}
```

> TOOL

tool_result
id: toolu_01Y3sUDqk4f8DLo1A8wYjbLC
```
1	---
2	name: qa-verifier
3	description: QA/QE agent that (1) runs the full local verification battery mirroring CI's required checks before any commit/push/PR, (2) audits test quality on changed code — failure-mode coverage, mocked-seam smells, coverage on changed files (Week-8 ≥80% gate), and (3) exercises the running application with data-level scenarios — authoring suites/checks through the real API, negative and edge-case inputs, authz probes — against the local stack's seeded demo data. Use proactively before pushing a branch or opening a PR, after writing or modifying tests, or when the user asks "run the gate", "is this ready to push?", "is this tested enough?", or "smoke the app with bad data".
4	tools: Read, Grep, Glob, Bash
5	model: sonnet
6	---
7	
8	You are the QA/QE agent for the DataQ project. You have three modes; run the one that matches the request, or all when asked to fully qualify a branch (1 → 2 → 3).
9	
10	**Bash usage:** you MAY execute the verification toolchain (formatters in check mode, linters, type checkers, SAST, test runners, coverage) and, in Mode 3, drive the local app's HTTP API — that's your job. You MUST […]

> TOOL

tool_use Read
id: toolu_01UAmK6kCycP2725HkJhbTuL
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md"
}
```

> TOOL

tool_result
id: toolu_01UAmK6kCycP2725HkJhbTuL
```
1	---
2	name: ui-tester
3	description: End-to-end UI QA agent that exercises DataQ's frontend on BOTH desktop and mobile viewports (functionality + rendering) against the running app, AND audits backend↔frontend feature parity — flagging backend capabilities with no frontend surface (and frontend calls with no backend). Use when the user asks to "test the UI", "check mobile rendering", "find backend/frontend gaps", "is this feature wired end-to-end", or before a release. Drives a live browser via the Playwright MCP and reads code for the parity audit.
4	tools: *
5	model: sonnet
6	---
7	
8	You are DataQ's UI QA agent. You have three missions, run in order, against the **running app** and the **repo source**. You **test and report** — you never modify app code, never `git push`, never open PRs, never deploy. Temporary artifacts (a throwaway spec, screenshots) are fine if you clean them up.
9	
10	## The app under test
11	
12	- **Frontend:** React + Vite + Ant Design (antd v6), Monaco, recharts. Routes are deep-linkable pages (ADR 0022): `/dashboard`, `/connections`, `/connections/new`, `/suites`, `/suites/:id`, `/suites/new`, check editor under a suite, `/results`, run detail, `/profile`, `/settings`, `/admin`.
13	- **Backend:** FastAPI […]

> TOOL

tool_use Bash
id: toolu_01TAx2Kt1viLEZJjCM82yvBz
```json
{
  "command": "grep -n \"run:\" /home/<USER>/Coding/Python/DataQ/.github/workflows/ci.yml | head -40",
  "description": "List CI job commands"
}
```

> TOOL

tool_result
id: toolu_01TAx2Kt1viLEZJjCM82yvBz
```
27:        run: pip install -r backend/requirements-tooling.txt
30:        run: black --check backend/
33:        run: ruff check backend/
39:        run: python scripts/check-typecheck-deps.py
54:        run: |
59:        run: mypy backend/app/
73:        run: pip install -r backend/requirements-tooling.txt
76:        run: bandit -c pyproject.toml -r backend/app/
90:        run: pip install pip-audit==2.10.0
106:        run: |
162:        run: |
171:        run: mypy backend/tests/
181:        run: pytest backend/tests/
211:        run: |
231:        run: |
247:      run:
261:        run: pnpm install --frozen-lockfile
264:        run: pnpm format:check
267:        run: pnpm lint
270:        run: pnpm typecheck
276:      run:
290:        run: pnpm install --frozen-lockfile
293:        run: pnpm test:coverage
345:        run: |
351:        run: |
357:        run: |
377:        run: pnpm install --frozen-lockfile
381:        run: pnpm exec playwright install --with-deps chromium
389:        run: pnpm e2e
403:      run:
417:        run: pnpm install --frozen-lockfile
423:        run: pnpm audit --audit-level=high
```

> TOOL

tool_use Bash
id: toolu_01XkZXiXgzeM7LYxyWwmwhEM
```json
{
  "command": "grep -rn \"dbt\" /home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts /home/<USER>/Coding/Python/DataQ/frontend/src/api/connectionSources.ts 2>/dev/null | head; echo ---; grep -rn \"scroll={{\" /home/<USER>/Coding/Python/DataQ/frontend/src --include=\"*.tsx\" -l | head; echo ---; grep -n \"projects:\" -A 20 /home/<USER>/Coding/Python/DataQ/frontend/playwright.config.ts",
  "description": "Check dbt in frontend enums, table scroll props, playwright projects"
}
```

> TOOL

tool_result
id: toolu_01XkZXiXgzeM7LYxyWwmwhEM
```
/home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts:5: * ADF, Airflow + dbt are orchestration providers, not datasources, but they are
/home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts:16:  'dbt',
/home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts:37:  dbt: 'orchestration',
/home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts:68:  dbt: null,
/home/<USER>/Coding/Python/DataQ/frontend/src/api/connections.ts:120:  dbt: 'dbt',
---
---
41:  projects: [
42-    liveBaseURL
43-      ? { name: 'live-smoke', use: { ...devices['Desktop Chrome'] } }
44-      : { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
45-  ],
46-  webServer: liveBaseURL
47-    ? undefined
48-    : {
49-        command: 'pnpm dev --host --port 3000',
50-        url: baseURL,
51-        // Locally: reuse the compose/`pnpm dev` server already on :3000. In CI:
52-        // start a fresh one (the api is already up on :8000 from a prior step).
53-        reuseExistingServer: !process.env.CI,
54-        timeout: 120_000,
55-        env: {
56-          VITE_AUTH_DEV_BYPASS: 'true',
57-          VITE_API_PROXY_TARGET: process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000',
58-        },
59-      },
60-});
```

> TOOL

tool_use Bash
id: toolu_01MgZZZybnR7bZQN92FzaRVs
```json
{
  "command": "grep -rn \"events/\" /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/orchestration*.py | grep -i \"post\\|router\" | head; echo ---; grep -rn \"ORCHESTRATION_PROVIDERS\\|'dbt'\" /home/<USER>/Coding/Python/DataQ/backend/app/db/models.py | head -5; echo ---; grep -n \"addopts\" /home/<USER>/Coding/Python/DataQ/pyproject.toml",
  "description": "Check dbt webhook endpoint, provider enum, pytest addopts"
}
```

> TOOL

tool_result
id: toolu_01MgZZZybnR7bZQN92FzaRVs
```
/home/<USER>/Coding/Python/DataQ/backend/app/api/v1/orchestration.py:7:- `POST /orchestration/events/adf` — Azure Monitor. Auth = shared secret in the
/home/<USER>/Coding/Python/DataQ/backend/app/api/v1/orchestration.py:10:- `POST /orchestration/events/airflow` — our DAG callback snippet. Auth =
/home/<USER>/Coding/Python/DataQ/backend/app/api/v1/orchestration.py:14:- `POST /orchestration/events/dbt` — our post-build callback snippet. Same
---
/home/<USER>/Coding/Python/DataQ/backend/app/db/models.py:40:ORCHESTRATION_PROVIDERS = ("adf", "airflow", "dbt")
/home/<USER>/Coding/Python/DataQ/backend/app/db/models.py:132:                "type IN (" + ", ".join(f"'{p}'" for p in ORCHESTRATION_PROVIDERS) + ")"
/home/<USER>/Coding/Python/DataQ/backend/app/db/models.py:441:        _in_check("provider", ORCHESTRATION_PROVIDERS, "provider_valid"),
/home/<USER>/Coding/Python/DataQ/backend/app/db/models.py:467:        _in_check("provider", ORCHESTRATION_PROVIDERS, "provider_valid"),
---
101:addopts = "--cov=backend/app --cov-report=term-missing --cov-fail-under=80"
125:# bring the whole importable package + tests + this config, and `-o addopts=`
133:pytest_add_cli_args = ["-o", "addopts="]
```

> TOOL

tool_use Bash
id: toolu_019cgPYnKuQ4LCde2QH6CBWZ
```json
{
  "command": "ls /home/<USER>/Coding/Python/DataQ/frontend/src/pages/; echo ---; gh issue list --repo TheurgicDuke771/DataQ --state open --label bug --json number,title --jq '.[] | \"#\\(.number) \\(.title)\"' | head -15",
  "description": "List frontend pages and open bug issues"
}
```

> TOOL

tool_result
id: toolu_019cgPYnKuQ4LCde2QH6CBWZ
```
Admin.tsx
CheckEdit.tsx
CheckNew.tsx
ConnectionEdit.tsx
ConnectionNew.tsx
Connections.tsx
Dashboard.tsx
NotFound.tsx
Profile.tsx
Results.tsx
RunDetail.tsx
Settings.tsx
SuiteEdit.tsx
SuiteNew.tsx
Suites.tsx
---
#640 Flaky LiveRunProgress test in CI ('polls until the run is terminal')
#618 Profile & Settings show stale "Azure AD (MSAL)" auth label after MSAL→generic-OIDC cutover (ADR 0028)
#617 Mobile/narrow-viewport UI broken: non-responsive layouts (suite-detail char-per-line, tables clip with no scroll, ☰ overlaps headings)
#601 pnpm format:check fails locally on gitignored e2e-live/.auth/session.json (missing .prettierignore entry)
#573 Flaky in CI: SchedulesPanel 'deletes a schedule after confirmation' (antd Popconfirm timing under jsdom)
#571 RunRead.checks_total shows 0 for runs that fail before dispatch (progress endpoint correctly shows the total)
#568 Threshold ordering/sign not validated on expectation-kind checks (warn≤fail≤critical assumed, never enforced)
#541 audit: remaining FKs without ondelete — connection/user delete paths may 500 like #540
#424 Run-detail sample: header says 'values redacted' even when non-PII values now surface (#417 follow-up)
#322 Flaky frontend test: LiveRunProgress "polls until the run is terminal, then stops and links to results"
#306 fix: validate provider/env query params on orchestration read endpoints (silent 200 [] on typo)
#237 ImportSuiteDrawer: unreachable empty-connections hint (dead UI)
```

> TOOL

tool_use Bash
id: toolu_01NUC9NukiX1sLpyZx4X3G3W
```json
{
  "command": "ls /home/<USER>/Coding/Python/DataQ/.claude/skills/ 2>/dev/null; ls /home/<USER>/Coding/Python/DataQ/.claude/commands/ 2>/dev/null",
  "description": "Check for repo-local skills/commands"
}
```

> TOOL

tool_result ERROR
id: toolu_01NUC9NukiX1sLpyZx4X3G3W
```
Exit code 1
adr-create
gh-issue-from-finding
security-scan
```

> TOOL

tool_use Edit
id: toolu_01D8yoY7avGWXLaWUcgKamrX
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "| Types | `pnpm typecheck` |\n| Tests | `pnpm test` |",
  "new_string": "| Types | `pnpm typecheck` |\n| Tests + coverage gate | `pnpm test:coverage` |"
}
```

> TOOL

tool_result
id: toolu_01D8yoY7avGWXLaWUcgKamrX
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01C3zkg3vQYJBWRx4Jy1jJmg
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "- **pytest addopts carry `--cov`** — a second `--cov` on the CLI is a pytest usage error (exit 4). Use `--cov=<module> --cov-report=term-missing -o addopts=` when you need targeted coverage.",
  "new_string": "- **pytest addopts carry `--cov` AND `--cov-fail-under=80`** — a second `--cov` on the CLI is a pytest usage error (exit 4), and a targeted subset run will spuriously fail the repo-wide 80% floor. Use `--cov=<module> --cov-report=term-missing -o addopts=` when you need targeted coverage. Frontend equivalent: the `lines: 80` gate only runs under `pnpm test:coverage`, not `pnpm test`."
}
```

> TOOL

tool_result
id: toolu_01C3zkg3vQYJBWRx4Jy1jJmg
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_015wkNwEwaBoEusNBzxTXpkM
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "2. **Orchestration tests covering only one provider** — parametrize over both `adf` and `airflow` (ADF-only fixtures mean the abstraction is rotting).",
  "new_string": "2. **Orchestration tests covering only one provider** — parametrize over the full `ORCHESTRATION_PROVIDERS` tuple (`adf`, `airflow`, `dbt` since ADR 0029), not a hardcoded subset (single-provider fixtures mean the abstraction is rotting)."
}
```

> TOOL

tool_result
id: toolu_015wkNwEwaBoEusNBzxTXpkM
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01D29EGPPDfoTQgYS29PtiTR
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "1. **Check-authoring edge cases** — through `POST/PATCH` on suites/checks: unknown expectation type; args missing/wrong-typed; thresholds inverted (warn worse than critical) or out of range; column names with quotes/unicode/SQL metacharacters; oversized strings. Expect 422/400 envelopes, never a 500 or a silently-persisted invalid check.",
  "new_string": "1. **Check-authoring edge cases** — through `POST/PATCH` on suites/checks: unknown expectation type; args missing/wrong-typed; thresholds inverted (warn worse than critical) or out of range; column names with quotes/unicode/SQL metacharacters/**NUL bytes and control characters** (`\u0000` in a string field 500'd all of v1 until #570 — always include it); oversized strings. Cover non-`expectation` kinds too: a `freshness`/`volume` check with kind-inappropriate or missing config must 422, not persist. Expect 422/400 envelopes, never a 500 or a silently-persisted invalid check."
}
```

> TOOL

tool_result
id: toolu_01D29EGPPDfoTQgYS29PtiTR
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01SVCsNbLdnKyQ7S1EoxEV4y
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "5. **Authz probes** — with a second demo user (seeded), verify: view-only user gets 403 on edit endpoints; non-shared suite invisible in lists AND 403/404 by direct id (no IDOR); admin endpoints 403 for non-admins.\n6. **Webhook hostility** — POST to `/api/v1/orchestration/events/{adf,airflow}` with: missing/wrong auth (secret/HMAC), valid auth + malformed JSON, valid JSON missing required fields, duplicate delivery (dedup index #456 should absorb it). Expect 401/422 envelopes and no phantom `pipeline_runs` rows.",
  "new_string": "5. **Authz probes** — with a second demo user (seeded), verify: view-only user gets 403 on edit endpoints; non-shared suite invisible in lists AND 403/404 by direct id (no IDOR); admin endpoints 403 for non-admins.\n5a. **PAT surface** (ADR 0026, #613) — garbage, expired, and revoked `dq_live_…` tokens must all return a **uniform 401** (no oracle distinguishing \"unknown\" from \"expired\"); a valid PAT must carry the owner's authz scope, not more; the plaintext token must never appear in any read-back after mint (sha256-at-rest, show-once).\n6. **Webhook hostility** — POST to `/api/v1/orchestration/events/{adf,airflow,dbt}` with: missing/wrong auth (secret/HMAC per provider), valid auth + malformed JSON, valid JSON missing required fields, duplicate delivery (dedup index #456 should absorb it). Expect 401/422 envelopes and […]

> TOOL

tool_use Edit
id: toolu_01PhLp2DtHHQpYuon96GSK6V
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "old_string": "Findings that warrant deferred work should be called out for `/gh-issue-from-finding` (working-agreement #3) — never silently dropped.",
  "new_string": "Before reporting a finding as new, check it against open issues (`gh issue list --state open --search \"<keywords>\"`) — a rediscovery of a known issue is reported as `known — #N (still reproduces)`, not as a fresh finding, and doesn't count toward the verdict unless the diff was supposed to fix it. Findings that warrant deferred work should be called out for `/gh-issue-from-finding` (working-agreement #3) — never silently dropped."
}
```

> TOOL

tool_result
id: toolu_01SVCsNbLdnKyQ7S1EoxEV4y
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_result
id: toolu_01PhLp2DtHHQpYuon96GSK6V
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01RGKJY6Bt5xBZaTcQvnLz9e
```json
{
  "command": "grep -n \"NUL\" /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md | cat -v",
  "description": "Verify NUL-byte edit rendered cleanly"
}
```

> TOOL

tool_result
id: toolu_01RGKJY6Bt5xBZaTcQvnLz9e
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01CJtc1JWrVEnjAFKvjsKht8
```json
{
  "command": "grep -an \"NUL\" /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md | cat -v",
  "description": "Check for literal NUL byte in file (binary-safe grep)"
}
```

> TOOL

tool_result
id: toolu_01CJtc1JWrVEnjAFKvjsKht8
```
87:1. **Check-authoring edge cases** M-bM-^@M-^T through `POST/PATCH` on suites/checks: unknown expectation type; args missing/wrong-typed; thresholds inverted (warn worse than critical) or out of range; column names with quotes/unicode/SQL metacharacters/**NUL bytes and control characters** (`^@` in a string field 500'd all of v1 until #570 M-bM-^@M-^T always include it); oversized strings. Cover non-`expectation` kinds too: a `freshness`/`volume` check with kind-inappropriate or missing config must 422, not persist. Expect 422/400 envelopes, never a 500 or a silently-persisted invalid check.
```

> AGENT

A literal NUL byte slipped into the file (making it binary to grep) — fixing to the textual escape:

> TOOL

tool_use Bash
id: toolu_0152FuzB6aStFVPa5TKgwq99
```json
{
  "command": "perl -pi -e 's/\\x00/\\\\x00/g' /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md && grep -n \"x00\" /home/<USER>/Coding/Python/DataQ/.claude/agents/qa-verifier.md",
  "description": "Replace literal NUL byte with \\x00 escape text"
}
```

> TOOL

tool_result
id: toolu_0152FuzB6aStFVPa5TKgwq99
```
87:1. **Check-authoring edge cases** — through `POST/PATCH` on suites/checks: unknown expectation type; args missing/wrong-typed; thresholds inverted (warn worse than critical) or out of range; column names with quotes/unicode/SQL metacharacters/**NUL bytes and control characters** (`\x00` in a string field 500'd all of v1 until #570 — always include it); oversized strings. Cover non-`expectation` kinds too: a `freshness`/`volume` check with kind-inappropriate or missing config must 422, not persist. Expect 422/400 envelopes, never a 500 or a silently-persisted invalid check.
```

> TOOL

tool_use Edit
id: toolu_01QfxCRnDjN3D56wdcGSey6X
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md",
  "old_string": "- **Frontend:** React + Vite + Ant Design (antd v6), Monaco, recharts. Routes are deep-linkable pages (ADR 0022): `/dashboard`, `/connections`, `/connections/new`, `/suites`, `/suites/:id`, `/suites/new`, check editor under a suite, `/results`, run detail, `/profile`, `/settings`, `/admin`.",
  "new_string": "- **Frontend:** React + Vite + Ant Design (antd v6), Monaco, recharts. Routes are deep-linkable pages (ADR 0022): `/dashboard`, `/connections`, `/connections/new`, `/connections/:id/edit`, `/suites`, `/suites/:id`, `/suites/new`, suite edit, check editor + check edit under a suite, `/results` (Runs + Pipeline runs tabs), run detail, `/profile`, `/settings`, `/admin`, plus the 404 page. `frontend/src/pages/` is the authoritative list — check it for screens added since this file was written."
}
```

> TOOL

tool_result
id: toolu_01QfxCRnDjN3D56wdcGSey6X
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01SGs4spj2nYzAKUu1PNBMqV
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md",
  "old_string": "Before starting, get oriented cheaply: `git log --oneline -5`, and skim `frontend/src/api/` + `frontend/src/pages/` + `backend/app/api/v1/`.",
  "new_string": "Before starting, get oriented cheaply: `git log --oneline -5`, and skim `frontend/src/api/` + `frontend/src/pages/` + `backend/app/api/v1/`.\n\n**Known-issue triage (do this first):** pull the open bug list — `gh issue list --state open --label bug --json number,title` — before the sweep. A defect that matches an open issue is reported as **`known — #N (still reproduces)`**, never as a new finding; only genuinely new symptoms (or a known issue's stated scope clearly not covering what you see) go in the findings list. This keeps the report actionable and avoids re-filing e.g. an open mobile-responsiveness umbrella issue screen by screen."
}
```

> TOOL

tool_result
id: toolu_01SGs4spj2nYzAKUu1PNBMqV
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01TH1gvwYpdSVsXT2JBk21K7
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md",
  "old_string": "- **Horizontal overflow:** the page `<body>` must not scroll sideways. Check via `browser_evaluate` → `document.documentElement.scrollWidth > document.documentElement.clientWidth`. Wide content (tables, the Monaco editor, charts, run-detail rows) must scroll **inside its own container**, not push the page.\n- **Navigation:** the sidebar/nav must be reachable (collapsed/hamburger) and every route still navigable by tap.\n- **Forms & modals:** the add-connection drawer, check editor, notifications panel, and modals (create-PAT, run-now) must be usable — inputs reachable, buttons not off-screen, Selects openable, the copy-once PAT token visible.\n- **Tap targets & truncation:** controls aren't overlapping or clipped; labels truncate rather than break layout.\n- Exercise at least one **core flow** on mobile (e.g. open a suite → open the notifications panel → toggle a threshold) to prove functionality, not just rendering.\n\nCapture a screenshot of any screen that misbehaves at mobile width — it's the clearest evidence.",
  "new_string": "- **Horizontal overflow:** the page `<body>` must not scroll sideways. Check via `browser_evaluate` → `document.documentElement.scrollWidth > document.documentElement.clientWidth`. Wide content (tables, the Monaco editor, charts, run-detail rows) must scroll **inside its own container**, not push the page.\n- **Navigation:** the sidebar/nav must be reachable (collapsed/hamburger) and every route still navigable by tap.\n- **Forms […]

> TOOL

tool_result
id: toolu_01TH1gvwYpdSVsXT2JBk21K7
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Finally, the parity-audit example refresh and the report-section dedup rule:

> TOOL

tool_use Edit
id: toolu_01AUvew3zpcDroUkReGsBpyx
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md",
  "old_string": "- Find the frontend client for each: `frontend/src/api/*.ts`. A backend router with **no** matching client, or endpoints a client never calls, is a candidate gap (e.g. the historic `api_keys` router with no `apiKeys.ts`, or `dbt` missing from `CONNECTION_TYPES`).",
  "new_string": "- Find the frontend client for each: `frontend/src/api/*.ts`. A backend router with **no** matching client, or endpoints a client never calls, is a candidate gap (historic examples, both since fixed: the `api_keys` router shipping with no `apiKeys.ts`; `dbt` landing in the backend enums before the frontend `CONNECTION_TYPES`)."
}
```

> TOOL

tool_use Edit
id: toolu_01FcpLKfoMcSv4WjS88tX4rn
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md",
  "old_string": "- **Summary line:** desktop OK/issues, mobile OK/issues, N parity gaps.\n- **Desktop findings** and **Mobile findings**: each with the screen/route, what's wrong (with a repro: viewport + steps), severity (**blocker** = broken/unusable · **major** = degraded but usable · **minor** = cosmetic), and a screenshot reference where you took one. Call out console errors and 4xx/5xx `/api` calls explicitly.",
  "new_string": "- **Summary line:** desktop OK/issues, mobile OK/issues, N parity gaps, N known issues re-confirmed.\n- **Desktop findings** and **Mobile findings**: each with the screen/route, what's wrong (with a repro: viewport + steps + measured numbers where you probed), severity (**blocker** = broken/unusable · **major** = degraded but usable · **minor** = cosmetic), the root-cause `file:line` where found, and a screenshot path where you took one. Call out console errors and 4xx/5xx `/api` calls explicitly. List `known — #N` re-confirmations separately from new findings."
}
```

> TOOL

tool_result
id: toolu_01AUvew3zpcDroUkReGsBpyx
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_result
id: toolu_01FcpLKfoMcSv4WjS88tX4rn
```
The file /home/<USER>/Coding/Python/DataQ/.claude/agents/ui-tester.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Both agents are updated. Here's what changed and why:

## qa-verifier ([.claude/agents/qa-verifier.md](.claude/agents/qa-verifier.md))

- **Fixed CI drift in the gate table**: the frontend tests gate now runs `pnpm test:coverage` (what CI actually runs since #558 — plain `pnpm test` skips the `lines: 80` gate entirely). The addopts gotcha also now warns that `--cov-fail-under=80` rides pytest's addopts, so a targeted subset run spuriously fails the 80% floor unless you pass `-o addopts=`.
- **dbt is now a first-class provider** (ADR 0029): the Mode-2 "parametrize over providers" flag and the Mode-3 webhook-hostility scenario both cover `adf`/`airflow`/`dbt` instead of the old two.
- **Encoded the #567/#570 lesson**: NUL bytes (`\x00`) and control characters are now an explicit, always-include hostile input in the check-authoring battery — that exact input 500'd all of v1 and was only caught at the pre-tag QA workout.
- **New PAT probe scenario** (ADR 0026/#613): uniform 401 for garbage/expired/revoked `dq_live_…` tokens, owner-scoped authz, and no plaintext token in any read-back.
- **Monitor-kind edge cases**: `freshness`/`volume` checks with kind-inappropriate config must 422, not persist.
- **Known-issue dedup**: findings are checked against open issues first and reported as `known — #N (still reproduces)` rather than as fresh findings.

## ui-tester ([.claude/agents/ui-tester.md](.claude/agents/ui-tester.md))

- **Known-issue […]