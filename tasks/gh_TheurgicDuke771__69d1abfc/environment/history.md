> DEVELOPER

Can you optimize and update the QA verifier and UI tester agents as required. one of the sample bug to refer for UI tester - https://github.com/TheurgicDuke771/DataQ/issues/617 [this is just one example don't be influenced by this]

> AGENT

I'll look at the current agent definitions and the referenced issue to understand what needs updating.

> AGENT

A literal NUL byte slipped into the file (making it binary to grep) — fixing to the textual escape:

> AGENT

Finally, the parity-audit example refresh and the report-section dedup rule:

> AGENT

Both agents are updated. Here's what changed and why: ## qa-verifier ([.claude/agents/qa-verifier.md](.claude/agents/qa-verifier.md)) - **Fixed CI drift in the gate table**: the frontend tests gate now runs `pnpm test:coverage` (what CI actually runs since #558 — plain `pnpm test` skips the `lines: 80` gate entirely). The addopts gotcha also now warns that `--cov-fail-under=80` rides pytest's addopts, so a targeted subset run spuriously fails the 80% floor unless you pass `-o addopts=`. - **dbt is now a first-class provider** (ADR 0029): the Mode-2 "parametrize over providers" flag and the Mode-3 webhook-hostility scenario both cover `adf`/`airflow`/`dbt` instead of the old two. - **Encoded the #567/#570 lesson**: NUL bytes (`\x00`) and control characters are now an explicit, always-include hostile input in the check-authoring battery — that exact input 500'd all of v1 and was only caught at the pre-tag QA workout. - **New PAT probe scenario** (ADR 0026/#613): uniform 401 for garbage/expired/revoked `dq_live_…` tokens, owner-scoped authz, and no plaintext token in any read-back. - **Monitor-kind edge cases**: `freshness`/`volume` checks with kind-inappropriate config must 422, not persist. - **Known-issue dedup**: findings are checked against open issues first and reported as `known — #N (still reproduces)` rather than as fresh findings. ## ui-tester ([.claude/agents/ui-tester.md](.claude/agents/ui-tester.md)) - **Known-issue […]