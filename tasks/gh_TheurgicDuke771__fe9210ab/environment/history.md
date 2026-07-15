> DEVELOPER

What's pending for week 2?

> AGENT

I'll check the live tracker and GitHub milestone for v1.1 Week 2.

> TOOL

tool_use Bash
id: toolu_01Y1wuJpdfYfHGqoxSHtFqhn
```json
{
  "command": "gh issue list --milestone \"v1.1 Week 2\" --state all --json number,title,state,labels --limit 50 2>&1 | head -c 4000",
  "description": "List issues in v1.1 Week 2 milestone"
}
```

> TOOL

tool_use Bash
id: toolu_014QzaB5337SiUmS8xG2sbhs
```json
{
  "command": "grep -n -i \"week 2\\|W2\\b\" docs/progress.md | head -40",
  "description": "Find Week 2 references in progress.md"
}
```

> TOOL

tool_result
id: toolu_01Y1wuJpdfYfHGqoxSHtFqhn
```
[]
```

> TOOL

tool_result
id: toolu_014QzaB5337SiUmS8xG2sbhs
```
27:| **Open issues** | **64** (W2 2026-07-05 — **UI-gap remediation batch** (user-reported: "these aren't in the UI"): six gaps where a backend feature shipped without its frontend, each built → agentic-reviewed → merged → **[#630](https://github.com/TheurgicDuke771/DataQ/issues/630) dbt connection UI** ([#637](https://github.com/TheurgicDuke771/DataQ/pull/637)), **[#631](https://github.com/TheurgicDuke771/DataQ/issues/631) PAT management UI** ([#636](https://github.com/TheurgicDuke771/DataQ/pull/636)), **[#632](https://github.com/TheurgicDuke771/DataQ/issues/632) stale RunNowPanel stub** ([#638](https://github.com/TheurgicDuke771/DataQ/pull/638)), **[#633](https://github.com/TheurgicDuke771/DataQ/issues/633) per-suite Slack/email** (full-stack: migration `d2e3f4a5b6c7` + both publishers + panel, [#639](https://github.com/TheurgicDuke771/DataQ/pull/639)), **[#635](https://github.com/TheurgicDuke771/DataQ/issues/635) policy-panel catalog dropdown** ([#641](https://github.com/TheurgicDuke771/DataQ/pull/641)), **[#634](https://github.com/TheurgicDuke771/DataQ/issues/634) auto-classify column-policy on suite create** (async, fail-soft, [#642](https://github.com/TheurgicDuke771/DataQ/pull/642)); follow-ups filed [#640](https://github.com/TheurgicDuke771/DataQ/issues/640) (flaky LiveRunProgress) + [#643](https://github.com/TheurgicDuke771/DataQ/issues/643) (stale policy on target change). **Deployed to prod 2026-07-05** (run 28757740586, sha b394a889): the migrate job applied `d2e3f4a5b6c7` (the #633 `suite_notifications` columns) then rolled api/worker/frontend — prod healthy (frontend 200, api 401 auth-enforced), App Insights clean (no schema/column errors). A **`ui-tester` agent** (desktop+mobile UI + backend↔frontend parity audit) was added ([#645](https://github.com/TheurgicDuke771/DataQ/pull/645)) to catch this gap class going forward. — **#524 + #589 closed via [#628](https://github.com/TheurgicDuke771/DataQ/pull/628)** — opencensus→OTel log migration + generic OTLP endpoint, both behind a new shared `otel.py` exporter seam; agentic review (code-reviewer + silent-failure-hunter) folded in; **deployed + parity live-verified** (local OTLP Collector received spans+logs redacted over the wire; prod App Insights `traces` now carry `cloud_RoleName=dataq-api/worker` via the OTel exporter, marker probe […]

> AGENT

The GitHub milestone query returned empty — let me check the exact milestone name and read the W2 section of the tracker.

> TOOL

tool_use Read
id: toolu_01DhPAxBGAxr9y3jWS3G5Y5z
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "offset": 150,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01DhPAxBGAxr9y3jWS3G5Y5z
```
150	### v1.1 W2 — Portability: OTel logs, secrets lifecycle, dry-run depth (due 2026-07-18) — 6/14
151	
152	Land the vendor-neutral seams **while App Insights / Key Vault / live `/mcp` still exist to
153	verify parity against** (ADR 0010/0013/0028 discipline). Live checks from here on run on the
154	W1 admin/member PATs instead of the Azure-CLI token workaround (#565).
155	
156	| Status | Task | Theme / gap |
157	|---|---|---|
158	| ✅ | [#609](https://github.com/TheurgicDuke771/DataQ/issues/609) Self-hosted dbt Core lineage on Snowflake (RETAIL→ANALYTICS_STG views→ANALYTICS dynamic tables; runs as `DATAQ_LOADER`) — `dbt build` green local + ACA Job, DataQ suite (checks + freshness) green on `MART_ORDER_REVENUE`, artifacts to ADLS (2026-07-05); unblocks #611 | Theme 14 / G-d |
159	| ✅ | [#611](https://github.com/TheurgicDuke771/DataQ/issues/611) dbt as a **third `OrchestrationProvider`** (ADR 0029) — `DbtProvider` + adapter + 3-scheme artifact reader (adls/s3/file) + HMAC `POST /orchestration/events/dbt` + 10-min poll + migration + `integrations/dbt/` snippet (#620, agentic review + migration-safety addressed). **Deployed to prod + live-verified 2026-07-05**: signed webhook → `pipeline_run` (dbt, succeeded) → bound mart suite fired + ran green against the #609 dynamic table. Poll-path live ADLS read deferred to [#622](https://github.com/TheurgicDuke771/DataQ/issues/622) (api UAMI read-only on KV) | […]

> TOOL

tool_use Bash
id: toolu_01RCFP9EiehYw5PrU9d1Ldk9
```json
{
  "command": "gh api repos/TheurgicDuke771/DataQ/milestones --jq '.[] | \"\\(.title) — open:\\(.open_issues) closed:\\(.closed_issues)\"' 2>&1 | head -20",
  "description": "List all milestones with counts"
}
```

> TOOL

tool_result
id: toolu_01RCFP9EiehYw5PrU9d1Ldk9
```
v1.1 Backlog — open:1 closed:37
v1.1 Week 2 — Portability: OTel logs, secrets lifecycle, dry-run depth — open:20 closed:35
v1.1 Week 3 — Azure wind-down + local-first posture — open:10 closed:0
v1.1 Week 4 — schema_drift monitor kind — open:7 closed:0
v1.1 Week 5 — anomaly monitor kind + metric trends — open:8 closed:0
v1.1 Week 6 — scale-aware execution + hardening + cycle close — open:14 closed:0
v1.1 Week 7 — stretch (backlog burn-down) — open:9 closed:0
```

> AGENT

The milestone title has a suffix. Let me pull the open issues directly.

> TOOL

tool_use Bash
id: toolu_01Vh9fTBBuMwraUafmQarZEG
```json
{
  "command": "gh issue list --milestone \"v1.1 Week 2 — Portability: OTel logs, secrets lifecycle, dry-run depth\" --state open --json number,title --limit 50 --jq '.[] | \"#\\(.number)  \\(.title)\"' 2>&1",
  "description": "List open issues in v1.1 Week 2 milestone"
}
```

> TOOL

tool_result
id: toolu_01Vh9fTBBuMwraUafmQarZEG
```
#654  feat(frontend): connection version history has no UI (asymmetric with check version history)
#653  feat(frontend): expose per-check alert snooze/suppression in the UI
#652  fix(frontend): dbt orchestration provider missing from Suite Triggers dropdown + Pipeline-runs filter
#651  fix(checks): expectation-kind check authoring doesn't validate expectation_type/config — invalid checks silently persist
#647  admin webhook-config surface mislabels dbt connections as airflow (two-provider if/else missed by ADR 0029)
#643  Auto-classify: a target change on an already-policied suite leaves the policy stale (invisibly)
#640  Flaky LiveRunProgress test in CI ('polls until the run is terminal')
#618  Profile & Settings show stale "Azure AD (MSAL)" auth label after MSAL→generic-OIDC cutover (ADR 0028)
#617  Mobile/narrow-viewport UI broken: non-responsive layouts (suite-detail char-per-line, tables clip with no scroll, ☰ overlaps headings)
#605  Runs that fail before/inside the runner show status='failed' with no user-visible reason
#584  MCP QA: natural-language tool-selection spot-check — verify an LLM client picks the right tool for the 4 canonical queries
#571  RunRead.checks_total shows 0 for runs that fail before dispatch (progress endpoint correctly shows the total)
#532  Dry-run preview is Snowflake-only — extend to Unity Catalog + flat-file suites
#488  Extend workspace-admin workspace-wide visibility to MCP tools + schedules list
#416  Enrich […]

> AGENT

Here's what's still open in **v1.1 Week 2** (Portability: OTel logs, secrets lifecycle, dry-run depth — due 2026-07-18). The big portability seams already landed and are prod-verified (dbt provider #609/#611, OTel logs #524/#589, `SecretStore.delete` #372/#622). What remains is **20 open issues**, split into the originally-planned work and follow-ups that got mapped into the milestone:

## Originally-planned W2 work still pending
**Alerting vendor-neutrality batch** (one batch PR — same code area):
- [#386](https://github.com/TheurgicDuke771/DataQ/issues/386) — tie `dedup._RANK` to a shared severity source
- [#387](https://github.com/TheurgicDuke771/DataQ/issues/387) — `suppression.py` early-return on `run.status == 'failed'`
- [#388](https://github.com/TheurgicDuke771/DataQ/issues/388) — single-source the `alert_on` literals
- [#389](https://github.com/TheurgicDuke771/DataQ/issues/389) — rename `teams_webhook_secret_name` → channel-neutral (the vendor-neutrality item)
- [#416](https://github.com/TheurgicDuke771/DataQ/issues/416) — enrich Slack/email alerts (deep link, expected-vs-observed, sample, metadata)

**Dry-run depth & MCP:**
- [#532](https://github.com/TheurgicDuke771/DataQ/issues/532) — extend dry-run preview Snowflake-only → UC + flat-file
- [#584](https://github.com/TheurgicDuke771/DataQ/issues/584) — MCP NL tool-selection spot-check vs live `/mcp` (4 canonical queries, PAT-auth)
- [#488](https://github.com/TheurgicDuke771/DataQ/issues/488) — workspace-admin visibility in MCP tools + schedules

## Follow-ups / gaps mapped into W2
- [#647](https://github.com/TheurgicDuke771/DataQ/issues/647) — admin webhook-config mislabels dbt connections as airflow (ADR 0029 two-provider if/else miss)
- [#651](https://github.com/TheurgicDuke771/DataQ/issues/651) — expectation-kind checks don't validate `expectation_type`/config (invalid checks silently persist)
- [#652](https://github.com/TheurgicDuke771/DataQ/issues/652) — dbt provider missing from Suite Triggers dropdown […]