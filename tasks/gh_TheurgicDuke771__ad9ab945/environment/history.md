> DEVELOPER

Hey, can you do a Architecture review of this project. 
After that check the marketplace listing readyness and prepare a chechlist for marketplace listing pre-requisite and good to haves

> AGENT

I'll do this in two phases: first an architecture review (code-level, not just docs), then a marketplace-readiness assessment against ADR 0013 and the known gaps (G-h, G-i). Let me fan out three parallel explorers to gather evidence while I read the key ADRs myself.

> TOOL

tool_use Agent
id: toolu_01SqsqSV27sQQ72m3w7QBPH8
```json
{
  "description": "Backend architecture review sweep",
  "subagent_type": "Explore",
  "prompt": "You are doing an architecture review sweep of the DataQ repo at /Users/arijit/Coding/Python/DataQ. Search breadth: very thorough. Focus ONLY on the backend + overall code architecture (another agent covers deploy/infra, a third covers marketplace/docs).\n\nAssess and report on:\n1. Layering: backend/app/{core,db,api,services,orchestration,datasources,mcp} — does the dependency direction hold (api → services → db; no service importing api)? Any layering violations (e.g. routers with business logic, services doing raw SQL bypassing models, circular imports)?\n2. The seams: ConnectionAdapter, CheckRunner, OrchestrationProvider, SecretStore, ResultPublisher, get_current_user. For each: where defined, how implementations register (registry pattern?), and whether any code bypasses the seam (e.g. isinstance checks on provider type, `if provider == 'adf'` branching in services, Azure-specific imports in business logic).\n3. Datasource layer: how the 5 datasources (snowflake, adls, s3, unity_catalog, iceberg) share gx_runner.py / flatfile.py; duplication or divergence between runners.\n4. check.kind monitor seam: how expectation vs freshness/volume kinds dispatch; is it extensible for schema_drift/anomaly.\n5. Config: Pydantic Settings usage, any hardcoded Azure endpoints/resource names in app code (grep for azure, vault.azure.net, applicationinsights, azurecontainerapps outside the intended adapter modules).\n6. DB models: table inventory, pipeline_runs vs runs separation, trigger_bindings shape, any FK/cascade smells.\n7. Error handling + logging: […]

> TOOL

tool_result
id: toolu_01SqsqSV27sQQ72m3w7QBPH8
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a1410494cce1a5896 (internal ID - do not mention to user. Use SendMessage with to: 'a1410494cce1a5896', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a1410494cce1a5896.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01W8AyTcAYiv4M6khsiXqPis
```json
{
  "description": "Deploy/infra/security review sweep",
  "subagent_type": "Explore",
  "prompt": "You are doing an architecture review sweep of the DataQ repo at /Users/arijit/Coding/Python/DataQ. Search breadth: very thorough. Focus ONLY on deployment, infrastructure, CI/CD, security posture, and operational architecture (another agent covers backend code architecture, a third covers marketplace/docs).\n\nAssess and report on:\n1. deploy/terraform/azure/ — module structure, what resources it stands up, how parameterized vs hardcoded (resource names, regions, the shared dataq-cae/dataq-pg assumptions), whether a second customer could `terraform apply` this cleanly into their own subscription. Note any harness/demo coupling baked into the IaC.\n2. Portability seams per ADR 0010/0013/0028: is Azure genuinely one impl behind seams? Check: SecretStore implementations (Key Vault + what else? env/file/local?), observability (OTel core vs Azure exporter — is there a non-Azure logging path?), auth (fastapi-azure-auth — is there a generic OIDC path or is backend token validation Azure-AD-only?), object storage.\n3. Docker/compose: docker-compose.yml for local dev, Dockerfiles (backend slim image ADR 0025, frontend nginx runtime-config image ADR 0028) — could a customer run this fully locally/on-prem (local-first posture #591)? What's missing for docker-compose-only production-ish deployment (e.g. secrets without Key Vault, auth without Azure AD)?\n4. CI/CD: .github/workflows inventory — quality gates, the Deploy workflow shape (GHCR, […]

> TOOL

tool_result
id: toolu_01W8AyTcAYiv4M6khsiXqPis
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a76d5ce23536a8072 (internal ID - do not mention to user. Use SendMessage with to: 'a76d5ce23536a8072', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a76d5ce23536a8072.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01GffNLXdi2VCzESFwJrE6VU
```json
{
  "description": "Marketplace readiness evidence sweep",
  "subagent_type": "Explore",
  "prompt": "You are gathering evidence for a marketplace-listing readiness assessment of the DataQ repo at /Users/arijit/Coding/Python/DataQ (a single-tenant data-quality platform the owner may want to list on a marketplace — e.g. Azure Marketplace / GitHub Marketplace / general commercial distribution). Search breadth: very thorough. Focus ONLY on marketplace/distribution/commercial readiness (other agents cover code architecture and infra).\n\nGather and report on:\n1. docs/adr/0013-marketplace-distribution-and-anti-lock-in.md — read fully; summarize what distribution model was decided (container images? Terraform? marketplace offer type?) and what it lists as prerequisites.\n2. Any other ADRs touching distribution/commercial use: ADR 0026 (PATs), 0027 (access tiers), 0028 (cloud-neutral), 0024/0025 (deploy/images), 0029, 0030 — one-line relevance each. Also read docs/adr/README.md index for anything else relevant.\n3. Gap register: search the repo (docs/, context/post-v1-roadmap.md, deploy/README.md, docs/progress.md) for gaps G-a through G-i, especially G-h (Databricks Free Edition — paid workspace before commercial use) and G-i (pre-marketplace harness teardown: strip Flows A/B/C, harness connections, demo users). Quote what each requires.\n4. Licensing: is there a LICENSE file? Any license headers? What do README/docs say about license/commercial terms? Check dependency licenses risk surface briefly (GX Core, FastMCP, Ant Design — any copyleft in requirements.txt worth flagging?).\n5. README.md […]

> TOOL

tool_result
id: toolu_01GffNLXdi2VCzESFwJrE6VU
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a7ffa111fde3c9ffb (internal ID - do not mention to user. Use SendMessage with to: 'a7ffa111fde3c9ffb', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a7ffa111fde3c9ffb.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

While those run, let me read the ADR index and the marketplace ADR myself.

> TOOL

tool_use Read
id: toolu_014xFWi2w29CZ8e1FY3meQou
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/README.md"
}
```

> TOOL

tool_result
id: toolu_014xFWi2w29CZ8e1FY3meQou
```
1	# Architecture Decision Records (ADRs)
2	
3	Each ADR captures a single significant architecture decision: the context, the decision, the consequences, and the alternatives considered. New ADRs are append-only — supersede an old decision by adding a new ADR and marking the old one's status as `Superseded by ADR-NNNN`.
4	
5	## Format
6	
7	- File name: `NNNN-short-kebab-slug.md` (zero-padded 4-digit sequence)
8	- Frontmatter fields:
9	  - **Status** — one of `Proposed`, `Accepted`, `Deprecated`, `Superseded by ADR-NNNN` (title-case)
10	  - **Date** — `YYYY-MM-DD`
11	  - **Deciders** — who made the call
12	  - **Consulted** *(optional)* — stakeholders whose sign-off the decision needed (e.g. product owner for ADR 0005). Omit when none.
13	  - **Supersedes** *(optional)* — `ADR-NNNN` this decision replaces. Omit when none.
14	  - **Superseded by** *(optional)* — `ADR-NNNN` that later replaced this one. Add when the status flips to `Superseded by`.
15	- Sections: Context, Decision, Consequences, Alternatives considered, Related (optional)
16	- Keep each ADR short — 1–2 pages. If it grows past that, the decision is probably two decisions.
17	
18	### Template
19	
20	```markdown
21	# ADR NNNN — <title>
22	
23	- **Status:** Proposed
24	- **Date:** […]

> TOOL

tool_use Read
id: toolu_01DR7erHjaNSMDGfp9nLCLyP
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md"
}
```

> TOOL

tool_result
id: toolu_01DR7erHjaNSMDGfp9nLCLyP
```
1	# ADR 0013 — Marketplace distribution (customer-deployed BYOL) and anti-vendor-lock-in guardrails
2	
3	- **Status:** Accepted
4	- **Date:** 2026-06-01
5	- **Deciders:** @TheurgicDuke771
6	
7	## Context
8	
9	We are evaluating listing DataQ on the **Azure, AWS, and GCP marketplaces**. Two questions follow: is it viable given the current architecture, and what must change to keep the option open without derailing the 8-week v1.
10	
11	There are two fundamentally different ways to be on a cloud marketplace, with very different engineering cost:
12	
13	| | **Vendor-hosted SaaS** | **Customer-deployed (BYOL)** |
14	|---|---|---|
15	| We operate | one multi-tenant service | nothing — the customer deploys into *their own* subscription/account |
16	| Tenancy | **multi-tenant required** | single-tenant is fine — one isolated instance per customer |
17	| Billing | marketplace metering-API integration | "bring your own license", billed outside the meter |
18	| Auth | customer IdP federates into ours | customer's own IdP, in their tenant |
19	| Fit for DataQ | ❌ requires a tenant-isolation rebuild | ✅ aligns with the current design |
20	
21	DataQ v1 is **explicitly single-tenant** (CLAUDE.md §1). […]

> AGENT

I've read the ADR index and ADR 0013 (marketplace distribution — customer-deployed BYOL, with its Phase 2 portability prerequisites spelled out). Three explorers are now sweeping the codebase in parallel — backend architecture, deploy/infra/security, and marketplace-readiness evidence (gap register G-a–G-i, licensing, docs, demo residue). I'll synthesize the architecture review and the marketplace checklist once they report back.

> AGENT

The infra/security sweep is back — key findings: backend token validation is Azure-AD-only (the biggest lock-in), no non-Azure production secret store, Terraform is coupled to the personal harness environment, and there's no rate limiting. Still waiting on the backend-architecture and marketplace-evidence sweeps before I synthesize.

> AGENT

Backend sweep is back too — layering and seams check out cleanly, with a handful of refinement-level findings (a second type-dispatch site in `run_target.py`, a missing `ondelete` on `pipeline_runs.connection_id`, the monitor-kind chain not being open/closed). One sweep remaining: the marketplace-evidence agent.

> AGENT

All three sweeps are in. Here's the synthesis — the full architecture review first, then the marketplace-readiness verdict and checklist.

---

# Part 1 — Architecture review

**Overall verdict: this is an unusually disciplined codebase for its size and age.** The layering direction holds with zero violations found (`api → services → {db, datasources, orchestration, core}`; no service imports a router, no business logic in routers). Every architectural seam the docs claim — `ConnectionAdapter`, `CheckRunner`/`MonitorRunner`, `OrchestrationProvider`, `SecretStore`, `ResultPublisher`, `get_current_user` — is a real `Protocol` with registry dispatch, not just a naming convention, and none of them are bypassed in service code. The weaknesses found are refinement-level ("second dispatch site", "not open/closed yet"), not structural faults.

## What's genuinely strong

- **Seam discipline.** The connection registry ([registry.py](backend/app/datasources/registry.py)) cleanly serves both datasources and orchestration providers off one `_ADAPTERS` map, and all five datasource runners share [gx_runner.py](backend/app/datasources/gx_runner.py); ADLS and S3 are thin ~90-line adapters over one shared [flatfile.py](backend/app/datasources/flatfile.py) runner. The MCP server's 8 tools are thin wrappers over the same service functions with the same per-suite authz — no duplicated logic, and it fail-closes (doesn't mount `/mcp` at all if auth is unconfigured).
- **Observability is the best seam in the repo.** [otel.py](backend/app/core/otel.py) […]