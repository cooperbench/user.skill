> DEVELOPER

the web e2e test after merging phase 68.2 was cancelled, potentially timed out: https://github.com/FSM1/cipher-box/actions/runs/28811365951/job/85439945331

> AGENT

I'll investigate the cancelled/timed-out web e2e run.

> TOOL

tool_use Bash
id: toolu_01JsY2JdB5epkZRqKt2U12Pq
```json
{
  "command": "env -u GITHUB_TOKEN gh run view 28811365951 --repo FSM1/cipher-box 2>&1 | head -60",
  "description": "View failed workflow run details"
}
```

> TOOL

tool_result
id: toolu_01JsY2JdB5epkZRqKt2U12Pq
```
X main CI E2E Tests · 28811365951
Triggered via push about 38 minutes ago

JOBS
✓ Detect Changes in 37s (ID 85439815581)
X Web E2E / Web E2E Tests in 20m16s (ID 85439945331)
- Desktop E2E in 0s (ID 85439946545)
✓ Re-trigger Release Gate in 5s (ID 85444049946)

ANNOTATIONS
X The job has exceeded the maximum execution time of 20m0s
Web E2E / Web E2E Tests: .github#1

X The operation was canceled.
Web E2E / Web E2E Tests: .github#14483


For more information about a job, try: gh run view --job=<job-id>
View this run on GitHub: https://github.com/FSM1/cipher-box/actions/runs/28811365951
```

> AGENT

Confirmed: hit the 20-minute hard timeout. Let me pull the log to see where it hung.

> TOOL

tool_use Bash
id: toolu_019fveDqzwvnsDydoYeEUtG1
```json
{
  "command": "env -u GITHUB_TOKEN gh run view --job=85439945331 --repo FSM1/cipher-box --log 2>&1 | tail -120",
  "description": "View job log tail"
}
```

> TOOL

tool_result
id: toolu_019fveDqzwvnsDydoYeEUtG1
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_012deod42h4dV5egvKq11NWd
```json
{
  "command": "env -u GITHUB_TOKEN gh run view --job=85439945331 --repo FSM1/cipher-box --log 2>&1 | wc -l; echo \"---STATUS $?\"",
  "description": "Check log length"
}
```

> TOOL

tool_result
id: toolu_012deod42h4dV5egvKq11NWd
```
       0
---STATUS 0
```

> TOOL

tool_use Bash
id: toolu_01NcFK13T9vSXqTn6UY4jrZy
```json
{
  "command": "env -u GITHUB_TOKEN gh run view --job=85439945331 --repo FSM1/cipher-box --log-failed 2>&1 | tail -80",
  "description": "View failed step logs"
}
```

> TOOL

tool_result
id: toolu_01NcFK13T9vSXqTn6UY4jrZy
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01FGvzHsCpCHq4yCsg2igT8T
```json
{
  "command": "cd \"$CLAUDE_JOB_DIR/tmp\" && env -u GITHUB_TOKEN gh api repos/FSM1/cipher-box/actions/jobs/85439945331/logs > joblog.txt 2>err.txt; echo \"exit=$?\"; wc -l joblog.txt; head -3 err.txt",
  "description": "Download job log via API"
}
```

> TOOL

tool_result
id: toolu_01FGvzHsCpCHq4yCsg2igT8T
```
exit=0
   15790 joblog.txt
Shell cwd was reset to /Users/myankelev/Code/random/cipher-box
```

> TOOL

tool_use Bash
id: toolu_01NNzTJfW3i6vFcbA4hDUZgm
```json
{
  "command": "grep -nE \"✓|✘|×|passed|failed|Running|\\.spec\\.ts|Serial|worker|Timed out|timeout|Error\" \"$CLAUDE_JOB_DIR/tmp/joblog.txt\" | tail -80",
  "description": "Scan log for test results and errors"
}
```

> TOOL

tool_result
id: toolu_01NNzTJfW3i6vFcbA4hDUZgm
```
105:2026-07-06T17:43:52.4238623Z ##[command]/usr/bin/docker create --name 0a771ae286c1465ea30a680668ff2ccf_postgres16alpine_15b7b1 --label 3a805b --network github_network_574cfbbb49ab49d1bed9f234c0ff5d31 --network-alias postgres -p 5432:5432 --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5 -e "POSTGRES_USER=postgres" -e "POSTGRES_PASSWORD=REDACTED -e "POSTGRES_DB=cipherbox_test" -e GITHUB_ACTIONS=true -e CI=true postgres:16-alpine
164:2026-07-06T17:43:55.2838606Z ##[command]/usr/bin/docker create --name d127142185dc41ed9340f457726b4ae3_ipfskubov0420_728472 --label 3a805b --network github_network_574cfbbb49ab49d1bed9f234c0ff5d31 --network-alias ipfs -p 5001:5001 -p 8080:8080 --health-cmd "ipfs id" --health-interval 10s --health-timeout 5s --health-retries 10 --health-start-period 30s -e GITHUB_ACTIONS=true -e CI=true ipfs/kubo:v0.42.0
214:2026-07-06T17:43:56.6100838Z ##[command]/usr/bin/docker create --name d84735c11d8a4d15abb3c39404919105_redis7alpine_1dd5d4 --label 3a805b --network github_network_574cfbbb49ab49d1bed9f234c0ff5d31 --network-alias redis -p 6379:6379 --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 5s --health-retries 5 -e GITHUB_ACTIONS=true -e CI=true redis:7-alpine
357:2026-07-06T17:44:12.1639457Z ##[group]Running self-installer...
675:2026-07-06T17:44:46.8368914Z Running kernel seems to be up-to-date.
872:2026-07-06T17:45:33.5801426Z [32m✓[39m 2767 modules transformed.
882:2026-07-06T17:45:34.6589734Z [2mdist/[22m[2massets/[22m[32mencrypt.worker-B6JnJnif.js       [39m[1m[2m  170.67 kB[22m[1m[22m
883:2026-07-06T17:45:34.6591421Z [2mdist/[22m[2massets/[22m[32mpdf.worker.min-wgc6bjNh.mjs      [39m[1m[2m1,078.61 kB[22m[1m[22m
893:2026-07-06T17:45:34.6606139Z [32m✓ built in 9.42s[39m
1123:2026-07-06T17:45:44.5797771Z [WebServer] [32m[Nest] 5892  - [39m07/06/2026, 5:45:44 PM [32m    LOG[39m [38;5;3m[TeeService] [39m[32mTEE worker healthy, current epoch: undefined[39m
1124:2026-07-06T17:45:44.5868760Z [WebServer] [33m[Nest] 5892  - [39m07/06/2026, 5:45:44 PM [33m   WARN[39m [38;5;3m[TeeService] [39m[33mTEE worker unavailable during initialization: TEE worker public key request failed: HTTP 404[39m
1125:2026-07-06T17:45:44.5872018Z [WebServer] [33m[Nest] 5892  - [39m07/06/2026, 5:45:44 PM [33m   WARN[39m [38;5;3m[TeeService] [39m[33mTEE republishing will not work until the TEE worker is available. This is expected in development without a TEE simulator.[39m
1151:2026-07-06T17:45:50.4376936Z Running 213 tests using […]

> AGENT

213 tests on 1 worker, hit the 20-min wall. Let me see the actual test progress — which spec was executing when it got killed, and whether tests were passing or hanging.

> TOOL

tool_use Bash
id: toolu_017EcZq5UYFjif7rHM1dRzgr
```json
{
  "command": "cd \"$CLAUDE_JOB_DIR/tmp\" && perl -pe 's/\\x1b\\[[0-9;]*m//g' joblog.txt > clean.txt; grep -nE \"\\[chromium\\]|\\bok\\b|✓|✘|passed \\(|failed \\(|flaky|did not run|\\.spec\\.ts:[0-9]\" clean.txt | grep -vE \"query failed|at /home\" | tail -60",
  "description": "Find playwright test status lines"
}
```

> TOOL

tool_result
id: toolu_017EcZq5UYFjif7rHM1dRzgr
```
872:2026-07-06T17:45:33.5801426Z ✓ 2767 modules transformed.
893:2026-07-06T17:45:34.6606139Z ✓ built in 9.42s
15631:2026-07-06T18:03:59.9677120Z  fixing permissions on existing directory /var/lib/postgresql/data ... ok
15632:2026-07-06T18:03:59.9677526Z  creating subdirectories ... ok
15637:2026-07-06T18:03:59.9679052Z  creating configuration files ... ok
15638:2026-07-06T18:03:59.9679324Z  running bootstrap script ... ok
15639:2026-07-06T18:03:59.9679614Z  performing post-bootstrap initialization ... ok
15640:2026-07-06T18:03:59.9679920Z  syncing data to disk ... ok
Shell cwd was reset to /Users/myankelev/Code/random/cipher-box
```

> TOOL

tool_use Bash
id: toolu_017bx9GHQ9MgLeUVB11Qt2FN
```json
{
  "command": "cd \"$CLAUDE_JOB_DIR/tmp\" && sed -n '1151,1200p' clean.txt | cut -c1-160",
  "description": "View lines after test start"
}
```

> TOOL

tool_result
id: toolu_017bx9GHQ9MgLeUVB11Qt2FN
```
2026-07-06T17:45:50.4376936Z Running 213 tests using 1 worker
2026-07-06T17:45:54.1811193Z [WebServer] [Nest] 5892  - 07/06/2026, 5:45:54 PM     LOG [IdentityController] Wallet login: userId=775d2e38-f10f-4cd4-8cbd-fe636fb
2026-07-06T17:46:05.3181618Z [WebServer] [Nest] 5892  - 07/06/2026, 5:46:05 PM     LOG [AuthService] Resolving placeholder publicKey for user 775d2e38-f10f-4cd4
2026-07-06T17:46:09.5630406Z [WebServer] [Nest] 5892  - 07/06/2026, 5:46:09 PM     LOG [DelegatedRoutingClient] IPNS record published successfully for k51qzi5uq
2026-07-06T17:46:09.5636271Z [WebServer] [17:46:09.557] INFO (5796): incoming request
2026-07-06T17:46:09.5637148Z [WebServer]     reqId: "req-4"
2026-07-06T17:46:09.5637800Z [WebServer]     req: {
2026-07-06T17:46:09.5638328Z [WebServer]       "method": "PUT",
2026-07-06T17:46:09.5639467Z [WebServer]       "url": "/routing/v1/ipns/REDACTED",
2026-07-06T17:46:09.5640478Z [WebServer]       "host": "localhost:3001",
2026-07-06T17:46:09.5641105Z [WebServer]       "remoteAddress": "127.0.0.1",
2026-07-06T17:46:09.5641721Z [WebServer]       "remotePort": 50426
2026-07-06T17:46:09.5642185Z [WebServer]     }
2026-07-06T17:46:09.5643979Z [WebServer] [17:46:09.559] INFO (REDACTED/5796): Stored IPNS record
2026-07-06T17:46:09.5645328Z [WebServer]     size: 397
2026-07-06T17:46:09.5645987Z [WebServer]     totalRecords: 1
2026-07-06T17:46:09.5646962Z [WebServer] [17:46:09.560] INFO (5796): request completed
2026-07-06T17:46:09.5647822Z [WebServer]     reqId: "req-4"
2026-07-06T17:46:09.5648781Z [WebServer]     res: {
2026-07-06T17:46:09.5649340Z [WebServer]       "statusCode": 200
2026-07-06T17:46:09.5649823Z [WebServer]     }
2026-07-06T17:46:09.5650511Z [WebServer]     responseTime: 2.5209069999982603
2026-07-06T17:46:09.6114355Z [WebServer] [17:46:09.608] INFO (5796): incoming request
2026-07-06T17:46:09.6115501Z [WebServer]     reqId: "req-5"
2026-07-06T17:46:09.6138850Z [WebServer]     req: {
2026-07-06T17:46:09.6139498Z [WebServer]       "method": "PUT",
2026-07-06T17:46:09.6140382Z [WebServer]       "url": "/routing/v1/ipns/REDACTED",
2026-07-06T17:46:09.6141795Z [WebServer]       "host": "localhost:3001",
2026-07-06T17:46:09.6142646Z [WebServer]       "remoteAddress": "127.0.0.1",
2026-07-06T17:46:09.6143663Z [WebServer]       "remotePort": 50426
2026-07-06T17:46:09.6144386Z [WebServer]     }
2026-07-06T17:46:09.6147409Z [WebServer] [Nest] 5892  - 07/06/2026, 5:46:09 PM     LOG [DelegatedRoutingClient] IPNS record published successfully for k51qzi5uq
2026-07-06T17:46:09.6152077Z [WebServer] [17:46:09.608] INFO (REDACTED/5796): Stored IPNS record
2026-07-06T17:46:09.6153906Z [WebServer] […]

> AGENT

The reporter only flushes a summary at the end, which never came (process killed). Two things to establish: (1) is this a new regression from 68.2, and (2) was it a genuine hang or just the suite outgrowing the 20-min budget. Let me check recent Web E2E history on main and what 68.2 touched.

> TOOL

tool_use Bash
id: toolu_01T8f2nJGFGBxNfQVftjRJb9
```json
{
  "command": "env -u GITHUB_TOKEN gh run list --repo FSM1/cipher-box --workflow \"CI E2E Tests\" --branch main --limit 12 2>&1 | cat",
  "description": "List recent CI E2E runs on main"
}
```

> TOOL

tool_result
id: toolu_01T8f2nJGFGBxNfQVftjRJb9
```
completed	cancelled	feat: SDK-owned read chain and resolved folder listings (#589)	CI E2E Tests	main	push	28811365951	21m5s	2026-07-06T17:43:05Z
completed	cancelled	feat: integrate web client with node/v3 read and write runtime (#588)	CI E2E Tests	main	push	28757141880	21m15s	2026-07-05T22:32:09Z
completed	cancelled	feat: web rotation UX and durable anti-rollback client state (#587)	CI E2E Tests	main	push	28588396792	21m10s	2026-07-02T12:01:40Z
completed	success	chore: dedupe encryptedIpnsKey rename todo (#586)	CI E2E Tests	main	push	28523500256	52s	2026-07-01T14:05:37Z
completed	cancelled	feat: rewrite TEE republish as a verify-in-enclave lease renewer (#585)	CI E2E Tests	main	push	28517794604	21m3s	2026-07-01T12:33:24Z
completed	cancelled	feat: atomic IPNS publish-gate, tombstone, and share schema cutover (…	CI E2E Tests	main	push	28476607011	21m8s	2026-06-30T21:19:53Z
completed	cancelled	feat: SDK write-chain, write-revocation, bin re-link, and invite clai…	CI E2E Tests	main	push	28446820251	21m4s	2026-06-30T13:10:04Z
completed	failure	chore(ci): bump actions/cache from 5.0.5 to 6.1.0 (#581)	CI E2E Tests	main	push	28404156812	22m21s	2026-06-29T21:34:03Z
completed	success	chore(ci): bump tauri-apps/tauri-action from 0.6.2 to 1.0.0 (#580)	CI E2E Tests	main	push	28403445490	1m1s	2026-06-29T21:20:30Z
completed	cancelled	feat: rotation soundness — content-key, inner-grant, concurrent-add, …	CI E2E Tests	main	push	28403349496	21m6s	2026-06-29T21:18:39Z
completed	cancelled	feat: read-chain navigation, grants, and […]

> AGENT

This is the key finding: **every substantive push to main since #578 (June 29) has cancelled at ~21 min** — only trivial chore commits (that skip the web-e2e job via path filter) go green. This is not a 68.2-specific regression; the full web-e2e suite has been blowing the 20-min budget for a week. Let me confirm the config levers (workers, retries, timeout).

> TOOL

tool_use Bash
id: toolu_01KjuQwZea3hM86ZniNMfaBm
```json
{
  "command": "cat tests/web-e2e/playwright.config.ts 2>/dev/null | grep -nE \"worker|ret\\b|retries|timeout|fullyParallel|forbidOnly\" ; echo \"=== reporter ===\"; grep -nE \"reporter\" tests/web-e2e/playwright.config.ts",
  "description": "Inspect playwright config workers/retries"
}
```

> TOOL

tool_result
id: toolu_01KjuQwZea3hM86ZniNMfaBm
```
26:  fullyParallel: false,
27:  workers: 1,
30:  forbidOnly: !!process.env.CI,
32:  // No retries - fix flakiness immediately (per CONTEXT.md)
33:  retries: 0,
72:            timeout: 30000,
81:            timeout: 120000,
90:            timeout: 120000,
=== reporter ===
36:  reporter: process.env.CI ? [['html', { open: 'never' }]] : 'list',
```

> AGENT

Config confirms it: **1 worker, fully serial, retries:0, 213 tests, 20-min job cap.** The HTML-only CI reporter is why stdout shows no per-test results. Let me pull the report artifact to see how far it got and whether any single test hung vs. the suite just not fitting.

> TOOL

tool_use Bash
id: toolu_01VSrdNbwJuwz72Ct7ooNbBA
```json
{
  "command": "env -u GITHUB_TOKEN gh api repos/FSM1/cipher-box/actions/runs/28811365951/artifacts --jq '.artifacts[] | \"\\(.name)\\t\\(.size_in_bytes)\\t\\(.id)\"' 2>&1 | cat",
  "description": "List run artifacts"
}
```

> TOOL

tool_result
id: toolu_01VSrdNbwJuwz72Ct7ooNbBA
```
(Bash completed with no output)
```

> AGENT

No artifacts — the job was killed before the upload step, so the HTML report is lost (a diagnosability gap in itself). Let me estimate progress from the server logs — count logins/publishes as a proxy for how many tests actually ran before the kill.

> TOOL

tool_use Bash
id: toolu_01EfWWw69pVDK7F2ksLYbGar
```json
{
  "command": "cd \"$CLAUDE_JOB_DIR/tmp\"\necho \"Wallet logins: $(grep -c 'Wallet login: userId' clean.txt)\"\necho \"Root IPNS first-publishes (seq via PUT /routing): $(grep -c 'IPNS record published successfully' clean.txt)\"\necho \"Republish jobs fired: $(grep -c 'Republish job complete' clean.txt)\"\necho \"--- last 3 meaningful test-side timestamps ---\"\ngrep -nE \"Test ended|Test timeout|locator|expect|TimeoutError|page.goto|Cleanup\" clean.txt | tail -8 | cut -c1-140",
  "description": "Estimate test progress from server logs"
}
```

> TOOL

tool_result
id: toolu_01EfWWw69pVDK7F2ksLYbGar
```
Wallet logins: 18
Root IPNS first-publishes (seq via PUT /routing): 168
Republish jobs fired: 1
--- last 3 meaningful test-side timestamps ---
375:2026-07-06T17:44:16.7619961Z [WARN] Detected a pnpm v10 installation layout at PNPM_HOME. The pnpm shims at PNPM_HOME have been refreshe
1125:2026-07-06T17:45:44.5872018Z [WebServer] [Nest] 5892  - 07/06/2026, 5:45:44 PM    WARN [TeeService] TEE republishing will not work unti
5537:2026-07-06T17:49:26.8035072Z Cleanup of conflict test items failed: locator.waitFor: Test ended.
5539:2026-07-06T17:49:26.8070093Z   - waiting for locator('.file-list-item:not(.upload-inline-row)').filter({ hasText: 'conflict-folder-1783
5540:2026-07-06T17:49:26.8074125Z     14 × locator resolved to visible <div role="row" tabindex="0" draggable="true" class="file-list-item f
Shell cwd was reset to /Users/myankelev/Code/random/cipher-box
```

> AGENT

Only **18 wallet logins in ~18 minutes** before the kill — the suite does heavy real IPNS round-trips per test, fully serialized. 213 tests at that rate can't fit in 20 minutes; it's not close. Let me confirm where the 20-min cap lives and whether the suite is shardable, so I can give a concrete fix.

> TOOL

tool_use Bash
id: toolu_01E1f8rvDSfJ1ZSXdMVhNrBz
```json
{
  "command": "cd /Users/myankelev/Code/random/cipher-box\necho \"=== workflow files mentioning web-e2e / timeout-minutes ===\"\ngrep -rlE \"web-e2e|Web E2E\" .github/workflows/ | cat\necho \"=== timeout-minutes in web-e2e workflow ===\"\ngrep -rnE \"timeout-minutes|--shard|shard|workers|playwright test\" .github/workflows/*.yml | grep -iE \"web|e2e|shard|timeout\" | cat",
  "description": "Find CI timeout and shard config"
}
```

> TOOL

tool_result
id: toolu_01E1f8rvDSfJ1ZSXdMVhNrBz
```
=== workflow files mentioning web-e2e / timeout-minutes ===
.github/workflows/tag-staging.yml
.github/workflows/release-gate.yml
.github/workflows/ci-e2e.yml
.github/workflows/web-e2e.yml
=== timeout-minutes in web-e2e workflow ===
.github/workflows/ci.yml:373:    timeout-minutes: 15
.github/workflows/load-test.yml:61:    timeout-minutes: 60
.github/workflows/release-gate.yml:141:    timeout-minutes: 60
.github/workflows/desktop-e2e.yml:18:    timeout-minutes: 45
.github/workflows/web-e2e.yml:18:    timeout-minutes: 20
```

> TOOL

tool_use Bash
id: toolu_01GygsY7SRwWRWSihjujW7G8
```json
{
  "command": "cd /Users/myankelev/Code/random/cipher-box\nsed -n '1,60p' .github/workflows/web-e2e.yml",
  "description": "Read web-e2e workflow head"
}
```

> TOOL

tool_result
id: toolu_01GygsY7SRwWRWSihjujW7G8
```
name: Web E2E Tests

on:
  workflow_dispatch:
  workflow_call:
    inputs:
      ref:
        description: 'Git ref to checkout (tag, branch, or SHA)'
        required: false
        type: string

permissions: {}

jobs:
  web-e2e:
    name: Web E2E Tests
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions:
      contents: read

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: cipherbox_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      ipfs:
        image: ipfs/kubo:v0.42.0
        ports:
          - 5001:5001
          - 8080:8080
        options: >-
          --health-cmd "ipfs id"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 10
          --health-start-period 30s

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
```

> TOOL

tool_use Bash
id: toolu_01Y3yWrpMpJTYcQr4MmkJQC6
```json
{
  "command": "cd /Users/myankelev/Code/random/cipher-box\ngrep -nE \"playwright|pnpm .*e2e|test:web|run:.*test|upload-artifact|if:\" .github/workflows/web-e2e.yml | cat",
  "description": "Find test run + artifact steps in web-e2e workflow"
}
```

> TOOL

tool_result
id: toolu_01Y3yWrpMpJTYcQr4MmkJQC6
```
96:        run: pnpm --filter @cipherbox/web-e2e exec playwright install chromium --with-deps
141:        run: pnpm --filter @cipherbox/web-e2e test
174:        if: failure()
175:        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1
177:          name: playwright-report
179:            tests/web-e2e/playwright-report/
```

> AGENT

Root cause confirmed. Here's the picture.

## This is not a phase 68.2 regression

The Web E2E job has hit its **20-minute `timeout-minutes` cap and been auto-cancelled on every substantive push to main since #578 (June 29)** — #585, #587, #588, and now #589. The only green runs in that window (#586, #580) are trivial chore commits where `Detect Changes` skips the web-e2e job entirely via path filter. So 68.2 merging cleanly and then "failing" is the same wall every recent feature PR has hit.

## Why it times out

`tests/web-e2e/playwright.config.ts`: `workers: 1`, `fullyParallel: false`, `retries: 0` — **213 tests, fully serial**, each doing real IPNS round-trips against the live API/Kubo/Postgres/Redis stack. From the server log, only **~18 wallet logins in ~18 minutes** of execution before the kill (~1 test/min, 168 IPNS publishes). At that rate the full suite needs ~an hour serially; it doesn't come close to fitting in 20 min.

What changed recently: the v2.0/v3 web runtime got **un-stubbed** (#588/#589). Previously those "not implemented — phase 63" throws made tests fail *fast*; now they do real, slow work — so the suite crossed the 20-min line and stays there.

Not the cause, but noted: `conflict-detection.spec.ts:120` hit its own […]