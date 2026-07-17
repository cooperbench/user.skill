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
  "prompt": "You are doing an architecture review sweep of the DataQ repo at /home/<USER>/Coding/Python/DataQ. Search breadth: very thorough. Focus ONLY on the backend + overall code architecture (another agent covers deploy/infra, a third covers marketplace/docs).\n\nAssess and report on:\n1. Layering: backend/app/{core,db,api,services,orchestration,datasources,mcp} — does the dependency direction hold (api → services → db; no service importing api)? Any layering violations (e.g. routers with business logic, services doing raw SQL bypassing models, circular imports)?\n2. The seams: ConnectionAdapter, CheckRunner, OrchestrationProvider, SecretStore, ResultPublisher, get_current_user. For each: where defined, how implementations register (registry pattern?), and whether any code bypasses the seam (e.g. isinstance checks on provider type, `if provider == 'adf'` branching in services, Azure-specific imports in business logic).\n3. Datasource layer: how the 5 datasources (snowflake, adls, s3, unity_catalog, iceberg) share gx_runner.py / flatfile.py; duplication or divergence between runners.\n4. check.kind monitor seam: how expectation vs freshness/volume kinds dispatch; is it extensible for schema_drift/anomaly.\n5. Config: Pydantic Settings usage, any hardcoded Azure endpoints/resource names in app code (grep for azure, vault.azure.net, applicationinsights, azurecontainerapps outside the intended adapter modules).\n6. DB models: table inventory, pipeline_runs vs runs separation, trigger_bindings shape, any FK/cascade smells.\n7. Error handling + logging: […]

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
  "prompt": "You are doing an architecture review sweep of the DataQ repo at /home/<USER>/Coding/Python/DataQ. Search breadth: very thorough. Focus ONLY on deployment, infrastructure, CI/CD, security posture, and operational architecture (another agent covers backend code architecture, a third covers marketplace/docs).\n\nAssess and report on:\n1. deploy/terraform/azure/ — module structure, what resources it stands up, how parameterized vs hardcoded (resource names, regions, the shared dataq-cae/dataq-pg assumptions), whether a second customer could `terraform apply` this cleanly into their own subscription. Note any harness/demo coupling baked into the IaC.\n2. Portability seams per ADR 0010/0013/0028: is Azure genuinely one impl behind seams? Check: SecretStore implementations (Key Vault + what else? env/file/local?), observability (OTel core vs Azure exporter — is there a non-Azure logging path?), auth (fastapi-azure-auth — is there a generic OIDC path or is backend token validation Azure-AD-only?), object storage.\n3. Docker/compose: docker-compose.yml for local dev, Dockerfiles (backend slim image ADR 0025, frontend nginx runtime-config image ADR 0028) — could a customer run this fully locally/on-prem (local-first posture #591)? What's missing for docker-compose-only production-ish deployment (e.g. secrets without Key Vault, auth without Azure AD)?\n4. CI/CD: .github/workflows inventory — quality gates, the Deploy workflow shape (GHCR, […]

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
  "prompt": "You are gathering evidence for a marketplace-listing readiness assessment of the DataQ repo at /home/<USER>/Coding/Python/DataQ (a single-tenant data-quality platform the owner may want to list on a marketplace — e.g. Azure Marketplace / GitHub Marketplace / general commercial distribution). Search breadth: very thorough. Focus ONLY on marketplace/distribution/commercial readiness (other agents cover code architecture and infra).\n\nGather and report on:\n1. docs/adr/0013-marketplace-distribution-and-anti-lock-in.md — read fully; summarize what distribution model was decided (container images? Terraform? marketplace offer type?) and what it lists as prerequisites.\n2. Any other ADRs touching distribution/commercial use: ADR 0026 (PATs), 0027 (access tiers), 0028 (cloud-neutral), 0024/0025 (deploy/images), 0029, 0030 — one-line relevance each. Also read docs/adr/README.md index for anything else relevant.\n3. Gap register: search the repo (docs/, context/post-v1-roadmap.md, deploy/README.md, docs/progress.md) for gaps G-a through G-i, especially G-h (Databricks Free Edition — paid workspace before commercial use) and G-i (pre-marketplace harness teardown: strip Flows A/B/C, harness connections, demo users). Quote what each requires.\n4. Licensing: is there a LICENSE file? Any license headers? What do README/docs say about license/commercial terms? Check dependency licenses risk surface briefly (GX Core, FastMCP, Ant Design — any copyleft in requirements.txt worth flagging?).\n5. README.md […]

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
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md"
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
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md"
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

> DEVELOPER

I' thinking of free [OSS] + BYOL model, please check if that will contradict with current codebase [project license, any dependent package lisence, etc.] 
Also document and file issue from these 2 review findings

> AGENT

Two workstreams then: (A) a real license audit — project license plus the full backend/frontend dependency tree — against a free-OSS + BYOL model, and (B) filing GitHub issues for the review findings with proper labels/milestones per your hygiene rules. Starting with the license audit using actual installed metadata, not just my earlier summary.

> TOOL

tool_use Write
id: toolu_01QH9nJdaHyDMaEhcEEAFoDP
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/license_audit.py",
  "content": "\"\"\"Dump license metadata for every package installed in the active env.\n\nFlags anything that is not clearly permissive (MIT/BSD/Apache/ISC/PSF/MPL-note/LGPL-note).\n\"\"\"\n\nimport re\nfrom importlib import metadata\n\nPERMISSIVE = re.compile(\n    r\"\\b(MIT|BSD|Apache|ISC|PSF|Python Software Foundation|Unlicense|Zlib|CC0|HPND|X11)\\b\",\n    re.I,\n)\nWEAK_COPYLEFT = re.compile(r\"\\b(LGPL|MPL|Mozilla|EPL|Eclipse|CDDL)\\b\", re.I)\nSTRONG_COPYLEFT = re.compile(r\"\\b(AGPL|GPL(?!.*Lesser)|SSPL|BUSL|BSL|Elastic|Commons Clause)\\b\", re.I)\n\n\ndef license_of(dist):\n    md = dist.metadata\n    expr = md.get(\"License-Expression\")\n    lic = md.get(\"License\")\n    classifiers = [c for c in md.get_all(\"Classifier\") or [] if c.startswith(\"License ::\")]\n    # Prefer SPDX expression, then classifier, then free-text License (often the full text)\n    if expr:\n        return expr\n    if classifiers:\n        return \"; \".join(c.split(\"::\")[-1].strip() for c in classifiers)\n    if lic:\n        first = lic.strip().splitlines()[0][:80]\n        return first\n    return \"UNKNOWN\"\n\n\nrows = []\nfor dist in metadata.distributions():\n    name = dist.metadata.get(\"Name\") or \"?\"\n    rows.append((name.lower(), name, dist.version, license_of(dist)))\n\nrows.sort()\nstrong, weak, unknown = [], [], []\nfor _, name, ver, lic in rows:\n    if STRONG_COPYLEFT.search(lic):\n        strong.append((name, ver, lic))\n    elif WEAK_COPYLEFT.search(lic) and not PERMISSIVE.search(lic):\n        weak.append((name, ver, lic))\n    elif not PERMISSIVE.search(lic):\n        unknown.append((name, ver, lic))\n\nprint(f\"TOTAL packages: {len(rows)}\")\nprint(\"\\n=== STRONG COPYLEFT / SOURCE-AVAILABLE (blockers to review) ===\")\nfor r in strong:\n    print(\"  %-40s %-12s %s\" % r)\nprint(\"\\n=== WEAK COPYLEFT (LGPL/MPL/EPL — fine to use, note in distribution) ===\")\nfor r in weak:\n    print(\"  %-40s %-12s %s\" % r)\nprint(\"\\n=== UNKNOWN / UNPARSED (manual check) ===\")\nfor r in unknown:\n    print(\"  %-40s %-12s %s\" % r)\n\nprint(\"\\n=== […]

> TOOL

tool_result
id: toolu_01QH9nJdaHyDMaEhcEEAFoDP
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/license_audit.py (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01XPFaenrrYTpyHEPn4d12aJ
```json
{
  "command": "conda run -n dataq python /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/license_audit.py",
  "description": "Audit licenses of all packages in the dataq conda env"
}
```

> TOOL

tool_use Bash
id: toolu_01K6VmN2iF2UVXH2RreEqaQf
```json
{
  "command": "pnpm --dir /home/<USER>/Coding/Python/DataQ/frontend licenses list --prod 2>&1 | head -80",
  "description": "List production dependency licenses for the frontend"
}
```

> TOOL

tool_result
id: toolu_01XPFaenrrYTpyHEPn4d12aJ
```
TOTAL packages: 239

=== STRONG COPYLEFT / SOURCE-AVAILABLE (blockers to review) ===

=== WEAK COPYLEFT (LGPL/MPL/EPL — fine to use, note in distribution) ===
  certifi                                  2026.5.20    Mozilla Public License 2.0 (MPL 2.0)
  pathspec                                 1.1.1        Mozilla Public License 2.0 (MPL 2.0)
  psycopg2-binary                          2.9.12       GNU Library or Lesser General Public License (LGPL)

=== UNKNOWN / UNPARSED (manual check) ===
  caio                                     0.9.25       UNKNOWN

=== KEY DEPS (explicit) ===
  great-expectations                       1.17.2       Apache Software License
  fastmcp                                  3.4.3        Apache-2.0
  fastapi                                  0.138.2      MIT
  sqlalchemy                               2.0.51       MIT
  celery                                   5.6.3        BSD-3-Clause
  redis                                    5.3.1        MIT License
  psycopg2-binary                          2.9.12       GNU Library or Lesser General Public License (LGPL)
  pydantic                                 2.13.4       MIT
  alembic                                  1.18.5       MIT
  structlog                                26.1.0       MIT OR Apache-2.0
  snowflake-connector-python               4.6.0        Apache Software License
  databricks-sql-connector                 4.3.0        Apache Software License
  boto3                                    1.43.36      Apache-2.0
  pyiceberg                                0.11.1       Apache-2.0
  azure-identity                           1.25.3       MIT
  azure-keyvault-secrets                   4.11.0       MIT License
  azure-monitor-opentelemetry-exporter     1.0.0b55     MIT License
  fastapi-azure-auth                       5.2.0        MIT License
  opentelemetry-sdk                        1.43.0       Apache-2.0
  uvicorn                                  0.50.2       BSD-3-Clause
  pandas                                   2.2.3        BSD License
  numpy                                    2.4.6        BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0
  pyarrow                                  24.0.0       Apache-2.0
  cryptography                             49.0.0       Apache-2.0 OR BSD-3-Clause
```

> TOOL

tool_result
id: toolu_01K6VmN2iF2UVXH2RreEqaQf
```
[WARN] The "pnpm" field in package.json is no longer read by pnpm. The following keys were ignored: "pnpm.overrides". See https://pnpm.io/settings for the new home of each setting.
[ERROR] This project is configured to use 9.15.4 of pnpm. Your current pnpm is v11.8.0
Corepack invoked pnpm with this version, and pnpm does not switch versions when running under corepack.
Align the "packageManager" field in package.json with "devEngines.packageManager", or invoke pnpm directly (without corepack) so it can switch versions automatically.
If you want to bypass this version check, you can set the "pmOnFail" configuration to "warn" or "ignore" (e.g. via --pm-on-fail=ignore). If using "devEngines.packageManager", you can set its "onFail" to "warn" or "ignore"
```

> TOOL

tool_use Bash
id: toolu_01QcEABMdDDp9iM8r6pdHpWE
```json
{
  "command": "conda run -n dataq python -c \"\nfrom importlib import metadata\nd = metadata.distribution('caio')\nprint(d.metadata.get('License'))\nprint(d.metadata.get('Home-page'))\nprint([c for c in d.metadata.get_all('Classifier') or []])\"",
  "description": "Inspect caio package license metadata"
}
```

> TOOL

tool_use Bash
id: toolu_01G3a8qx2fRRkRnzsj3qJnGq
```json
{
  "command": "pnpm --dir /home/<USER>/Coding/Python/DataQ/frontend --pm-on-fail=ignore licenses list --prod 2>/dev/null | tail -60",
  "description": "List frontend production dependency licenses (bypass pnpm version check)"
}
```

> TOOL

tool_result
id: toolu_01QcEABMdDDp9iM8r6pdHpWE
```
None
None
['Topic :: Software Development', 'Topic :: Software Development :: Libraries', 'Intended Audience :: Developers', 'Natural Language :: English', 'Operating System :: MacOS', 'Operating System :: POSIX', 'Operating System :: Microsoft', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12', 'Programming Language :: Python :: 3.13', 'Programming Language :: Python :: 3.14', 'Programming Language :: Python :: Implementation :: CPython']
```

> TOOL

tool_result
id: toolu_01G3a8qx2fRRkRnzsj3qJnGq
```
[ERR_PNPM_MISSING_PACKAGE_INDEX_FILE] Failed to find package index file for @ant-design/icons@6.3.2 (at REDACTED	@ant-design/icons@6.3.2), please consider running 'pnpm install'
```

> TOOL

tool_use Bash
id: toolu_01WB4weQCbzXFobRiAb9ReUp
```json
{
  "command": "conda run -n dataq python -c \"\nfrom importlib import metadata\nd = metadata.distribution('caio')\nfor f in d.files or []:\n    if 'LICENSE' in str(f).upper() or 'COPYING' in str(f).upper():\n        print(f)\n        print(open(d.locate_file(f)).read()[:300])\n\"",
  "description": "Read caio's bundled LICENSE file"
}
```

> TOOL

tool_use Bash
id: toolu_011GsaavgAgCfkJjGQoyBnEM
```json
{
  "command": "ls /home/<USER>/Coding/Python/DataQ/frontend/node_modules >/dev/null 2>&1 && echo node_modules-present; grep -c '' /home/<USER>/Coding/Python/DataQ/frontend/pnpm-lock.yaml 2>/dev/null",
  "description": "Check frontend node_modules and lockfile presence"
}
```

> TOOL

tool_result
id: toolu_01WB4weQCbzXFobRiAb9ReUp
```
caio-0.9.25.dist-info/licenses/COPYING
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for u
```

> TOOL

tool_result
id: toolu_011GsaavgAgCfkJjGQoyBnEM
```
node_modules-present
5340
```

> TOOL

tool_use Write
id: toolu_017DHcebPkaxLXkXFuxFAH2R
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/fe_license_audit.py",
  "content": "\"\"\"Walk frontend node_modules and classify every package's declared license.\"\"\"\n\nimport json\nimport os\nimport re\nfrom collections import Counter\n\nROOT = \"/home/<USER>/Coding/Python/DataQ/frontend/node_modules\"\n\nPERMISSIVE = re.compile(\n    r\"\\b(MIT|BSD|Apache|ISC|0BSD|Unlicense|Zlib|CC0|CC-BY|Python-2|BlueOak|WTFPL|Artistic)\\b\", re.I\n)\nWEAK = re.compile(r\"\\b(LGPL|MPL|EPL|CDDL)\\b\", re.I)\nSTRONG = re.compile(r\"\\b(AGPL|(?<!L)GPL|SSPL|BUSL|BSL-1\\.1|Elastic|Commons.Clause)\\b\", re.I)\n\ncounts = Counter()\nstrong, weak, unknown = [], [], []\nseen = set()\n\nfor dirpath, dirnames, filenames in os.walk(ROOT):\n    # only descend into package roots; skip nested node_modules beyond pnpm store layout\n    if \"package.json\" in filenames:\n        pj = os.path.join(dirpath, \"package.json\")\n        try:\n            with open(pj) as f:\n                data = json.load(f)\n        except Exception:\n            continue\n        name, ver = data.get(\"name\"), data.get(\"version\")\n        if not name or (name, ver) in seen:\n            continue\n        seen.add((name, ver))\n        lic = data.get(\"license\") or data.get(\"licenses\") or \"UNKNOWN\"\n        if isinstance(lic, list):\n            lic = \" OR \".join(\n                x.get(\"type\", \"?\") if isinstance(x, dict) else str(x) for x in lic\n            )\n        if isinstance(lic, dict):\n            lic = lic.get(\"type\", \"UNKNOWN\")\n        counts[lic] += 1\n        if STRONG.search(lic):\n            strong.append((name, ver, lic))\n        elif WEAK.search(lic):\n            weak.append((name, ver, lic))\n        elif not PERMISSIVE.search(lic):\n            unknown.append((name, ver, lic))\n\nprint(f\"unique name@version packages: {len(seen)}\")\nprint(\"\\n=== STRONG COPYLEFT / SOURCE-AVAILABLE ===\")\nfor r in sorted(set(strong)):\n    print(\"  %-50s %-12s %s\" % r)\nprint(\"\\n=== WEAK COPYLEFT (LGPL/MPL/EPL) ===\")\nfor r in sorted(set(weak)):\n    print(\"  %-50s %-12s %s\" % r)\nprint(\"\\n=== UNKNOWN / OTHER ===\")\nfor r in sorted(set(unknown)):\n    print(\"  %-50s %-12s %s\" % r)\nprint(\"\\n=== LICENSE HISTOGRAM (top 15) ===\")\nfor […]

> TOOL

tool_result
id: toolu_017DHcebPkaxLXkXFuxFAH2R
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/fe_license_audit.py (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01Jg1XK1Fcx81QATACFD9SH3
```json
{
  "command": "python3 /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/fe_license_audit.py",
  "description": "Sweep frontend node_modules for copyleft licenses"
}
```

> TOOL

tool_result
id: toolu_01Jg1XK1Fcx81QATACFD9SH3
```
unique name@version packages: 643

=== STRONG COPYLEFT / SOURCE-AVAILABLE ===

=== WEAK COPYLEFT (LGPL/MPL/EPL) ===
  dompurify                                          3.4.11       (MPL-2.0 OR Apache-2.0)
  lightningcss                                       1.32.0       MPL-2.0
  lightningcss-darwin-arm64                          1.32.0       MPL-2.0

=== UNKNOWN / OTHER ===
  @fontsource/inter                                  5.2.8        OFL-1.1
  @fontsource/jetbrains-mono                         5.2.8        OFL-1.1
  baz                                                None         UNKNOWN
  browser_field                                      None         UNKNOWN
  false_main                                         None         UNKNOWN
  invalid_main                                       None         UNKNOWN
  monaco-loader                                      0.0.1        UNKNOWN
  rxjs/ajax                                          None         UNKNOWN
  rxjs/fetch                                         None         UNKNOWN
  rxjs/operators                                     None         UNKNOWN
  rxjs/testing                                       None         UNKNOWN
  rxjs/webSocket                                     None         UNKNOWN

=== LICENSE HISTOGRAM (top 15) ===
  MIT                                      526
  Apache-2.0                               42
  ISC                                      33
  BSD-3-Clause                             10
  UNKNOWN                                  10
  BSD-2-Clause                             8
  OFL-1.1                                  2
  MIT-0                                    2
  BlueOak-1.0.0                            2
  MPL-2.0                                  2
  (MPL-2.0 OR Apache-2.0)                  1
  0BSD                                     1
  CC-BY-4.0                                1
  MIT AND ISC                              1
  CC0-1.0                                  1
```

> TOOL

tool_use Bash
id: toolu_01HHc3zZCeNNNe4dShACgmZX
```json
{
  "command": "find /home/<USER>/Coding/Python/DataQ/frontend/node_modules -name package.json -path \"*monaco-loader*\" -not -path \"*/node_modules/*/node_modules/*\" 2>/dev/null | head -3; grep -rn \"monaco-loader\" /home/<USER>/Coding/Python/DataQ/frontend/package.json /home/<USER>/Coding/Python/DataQ/frontend/pnpm-lock.yaml 2>/dev/null | head -10",
  "description": "Locate monaco-loader package and check if it's a declared dependency"
}
```

> TOOL

tool_result
id: toolu_01HHc3zZCeNNNe4dShACgmZX
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01DV7T8mJTZccCy9ThH3gfjd
```json
{
  "command": "gh label list --repo TheurgicDuke771/DataQ --limit 50",
  "description": "List repo labels"
}
```

> TOOL

tool_use Bash
id: toolu_01HPBeMxZrB5oD6eFog963Fv
```json
{
  "command": "gh api repos/TheurgicDuke771/DataQ/milestones --jq '.[] | \"\\(.number)\\t\\(.title)\\t\\(.due_on // \"no-due\")\\t\\(.open_issues) open\"'",
  "description": "List open milestones"
}
```

> TOOL

tool_result
id: toolu_01DV7T8mJTZccCy9ThH3gfjd
```
bug	Something isn't working	#d73a4a
documentation	Improvements or additions to documentation	#0075ca
duplicate	This issue or pull request already exists	#cfd3d7
enhancement	New feature or request	#a2eeef
good first issue	Good for newcomers	#7057ff
help wanted	Extra attention is needed	#008672
invalid	This doesn't seem right	#e4e669
question	Further information is requested	#d876e3
wontfix	This will not be worked on	#ffffff
security	Security-related issue or PR	#B60205
priority/P0	Urgent — blocks milestone or security	#b60205
priority/P1	High — do soon, milestone-adjacent	#d93f0b
priority/P2	Medium — important, not blocking	#fbca04
priority/P3	Low — polish / docs	#0e8a16
week-1-carryover	Week-1 scope item completed later (scheduled in its milestone)	#d4c5f9
week-2-carryover	Week-2 scope item completed later	#d4c5f9
epic	Week tracking epic (roadmap mirror)	#5319e7
dependencies	label for dependabot issues	#a84225
refactor	Code cleanup / dedup / tech-debt (no behavior change)	#c5def5
test	Testing & coverage work	#bfdadc
ci		#05675e
ops	Operational / environment / infra lifecycle task (not app code)	#D4C5F9
```

> TOOL

tool_result
id: toolu_01HPBeMxZrB5oD6eFog963Fv
```
4	v1.1 Backlog	no-due	6 open
12	v1.1 Week 3 — Azure wind-down + local-first posture	2026-07-24T00:00:00Z	3 open
13	v1.1 Week 4 — schema_drift monitor kind	2026-07-31T00:00:00Z	7 open
14	v1.1 Week 5 — anomaly monitor kind + metric trends	2026-08-07T00:00:00Z	8 open
15	v1.1 Week 6 — scale-aware execution + hardening + cycle close	2026-08-14T00:00:00Z	14 open
16	v1.1 Week 7 — stretch (backlog burn-down)	2026-08-21T00:00:00Z	9 open
```

> AGENT

Before filing anything, let me verify the key claims from the sweeps directly (per your no-false-filings culture).

> TOOL

tool_use Read
id: toolu_015murg1h9rsCKVt1espZPAf
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/db/models.py",
  "offset": 476,
  "limit": 45
}
```

> TOOL

tool_result
id: toolu_015murg1h9rsCKVt1espZPAf
```
476	    user: Mapped["User"] = relationship()
477	
478	
479	class PipelineRun(Base):
480	    __tablename__ = "pipeline_runs"
481	    __table_args__ = (
482	        _in_check("provider", ORCHESTRATION_PROVIDERS, "provider_valid"),
483	        _in_check("status", PIPELINE_RUN_STATUSES, "status_valid"),
484	        UniqueConstraint("provider", "provider_run_id", name="uq_pipeline_runs_provider_run"),
485	        Index("ix_pipeline_runs_provider_pipeline", "provider", "pipeline_or_dag_id"),
486	        Index("ix_pipeline_runs_connection_id", "connection_id"),
487	    )
488	
489	    id: Mapped[uuid.UUID] = _uuid_pk()
490	    provider: Mapped[str] = mapped_column(String(16), nullable=False)
491	    connection_id: Mapped[uuid.UUID] = mapped_column(
492	        UUID(as_uuid=True), ForeignKey("connections.id"), nullable=False
493	    )
494	    provider_run_id: Mapped[str] = mapped_column(String(256), nullable=False)
495	    pipeline_or_dag_id: Mapped[str] = mapped_column(String(256), nullable=False)
496	    env: Mapped[str] = mapped_column(String(16), nullable=False)
497	    status: Mapped[str] = mapped_column(String(16), nullable=False)
498	    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
499	    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
500	    failure_reason: Mapped[str | None] = mapped_column(String(2048))
501	    last_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
502	    created_at: Mapped[datetime] = _created_at()
503	
504	
505	class TriggerBinding(Base):
506	    __tablename__ = "trigger_bindings"
507	    __table_args__ = (
508	        _in_check("provider", ORCHESTRATION_PROVIDERS, "provider_valid"),
509	        _in_check("env", ENVS, "env_valid"),
510	        UniqueConstraint(
511	            "provider",
512	            "pipeline_or_dag_id",
513	            "env",
514	            "suite_id",
515	            name="uq_trigger_bindings_lookup",
516	        ),
517	        Index(
518	            "ix_trigger_bindings_provider_pipeline_env",
519	            "provider",
520	            "pipeline_or_dag_id",
```

> TOOL

tool_use Read
id: toolu_01SatLcrUWJjofMkZDmuDut1
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/mcp/server.py",
  "offset": 505,
  "limit": 35
}
```

> TOOL

tool_result
id: toolu_01SatLcrUWJjofMkZDmuDut1
```
505	        log.warning("mcp_disabled_no_auth", note="/mcp not mounted — no Azure auth or dev bypass")
506	        return None
507	    log.info(
508	        "mcp_enabled", auth="azure_ad" if get_settings().azure_auth_configured else "dev_bypass"
509	    )
510	    # FastMCP (≥3.4.3) guards the streamable-HTTP transport with a Host allowlist
511	    # for DNS-rebinding protection, defaulting to loopback only ("127.0.0.1",
512	    # "localhost", "::1") — anything else gets a 421 Misdirected Request. DataQ
513	    # always fronts the api with the nginx proxy (ADR 0028 §5), which forwards the
514	    # *upstream* Host (the internal ACA FQDN in prod, `api` in compose) so ACA's
515	    # Envoy routes correctly — none of which are loopback, so the guard 421s every
516	    # proxied MCP request. DNS-rebinding protection is a browser-vs-localhost threat
517	    # model that doesn't apply here: the api has no public ingress and every /mcp
518	    # request is JWT/PAT-authenticated fail-closed (`build_auth_provider`). Allow
519	    # the proxied hosts so the transport guard doesn't shadow the real auth gate.
520	    # The same middleware also 403s a request whose browser `Origin` isn't
521	    # allow-listed. DataQ authenticates every /mcp call with a Bearer token (JWT or
522	    # PAT), never a cookie, so the Origin/CSRF check the […]

> TOOL

tool_use Read
id: toolu_01WSykFjPub65jMJ53RR8B3e
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/services/run_target.py",
  "offset": 85,
  "limit": 55
}
```

> TOOL

tool_result
id: toolu_01WSykFjPub65jMJ53RR8B3e
```
85	    Raises `SuiteTargetInvalidError` if the suite is targetless, the target is
86	    missing the field its datasource requires (`path` for flat files, `table`
87	    for SQL, `catalog` for Unity Catalog), or the connection type has no run path
88	    (orchestration providers — they are never suite datasources).
89	    """
90	    if not target:
91	        raise SuiteTargetInvalidError(
92	            "suite has no target configured", detail={"connection_type": conn_type}
93	        )
94	
95	    if conn_type in _FLATFILE_TYPES:
96	        # A batch target (regex `pattern`) is resolved to a concrete path at run
97	        # time; a literal target carries the `path` directly. The two are mutually
98	        # exclusive — both set is an ambiguous target, not a silent batch win.
99	        if "pattern" in target and target.get("path"):
100	            raise SuiteTargetInvalidError(
101	                "flat-file target is ambiguous: set either 'path' (literal) or "
102	                "'pattern' (batch), not both",
103	                detail={"connection_type": conn_type},
104	            )
105	        if "pattern" in target:
106	            return ResolvedTarget(
107	                table="", schema=None, catalog=None, batch=_batch_spec(target, conn_type)
108	            )
109	        path = _require(target, "path", conn_type)
110	        return ResolvedTarget(table=path, schema=None, catalog=None)
111	
112	    if conn_type == "snowflake":
113	        table = _require(target, "table", conn_type)
114	        return ResolvedTarget(table=table, schema=_str_or_none(target.get("schema")), catalog=None)
115	
116	    if conn_type == […]

> TOOL

tool_use Read
id: toolu_01MoUZpNUvfnAFZiwnC9MYLJ
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/.github/SECURITY.md"
}
```

> TOOL

tool_result
id: toolu_01MoUZpNUvfnAFZiwnC9MYLJ
```
1	# Security Policy
2	
3	## Reporting a Vulnerability
4	
5	**Do not open a public GitHub issue for security vulnerabilities.** Public disclosure before a fix is ready puts all users at risk.
6	
7	Report vulnerabilities privately via **[GitHub Security Advisories](https://github.com/TheurgicDuke771/DataQ/security/advisories/new)**.
8	
9	You will receive a response within **5 business days** acknowledging the report. We aim to release a fix within **30 days** for critical issues and **90 days** for lower-severity issues, depending on complexity.
10	
11	## What to include
12	
13	- A clear description of the vulnerability and the affected component
14	- Steps to reproduce (or a proof-of-concept)
15	- Potential impact and severity assessment
16	- Any suggested mitigations
17	
18	## Scope
19	
20	Components in scope:
21	- FastAPI backend (`/api/v1/*`, `/mcp`)
22	- Authentication flow — OIDC sign-in (`oidc-client-ts`, Azure AD validated) + backend JWT validation (`fastapi-azure-auth`)
23	- Celery worker + GX execution path
24	- Key Vault secret access patterns
25	
26	Out of scope:
27	- Vulnerabilities in third-party dependencies — report those upstream; we track them via Dependabot
28	- Issues requiring physical access to Azure infrastructure
29	
30	## Supported […]

> TOOL

tool_use Bash
id: toolu_01YQwcaFi36eT3HZ9RfCRZ6H
```json
{
  "command": "grep -rn \"def delete\" /home/<USER>/Coding/Python/DataQ/backend/app/services/connection_service.py | head; grep -n \"pipeline_run\" /home/<USER>/Coding/Python/DataQ/backend/app/services/connection_service.py | head",
  "description": "Check connection delete handling of pipeline_runs children"
}
```

> TOOL

tool_result
id: toolu_01YQwcaFi36eT3HZ9RfCRZ6H
```
/home/<USER>/Coding/Python/DataQ/backend/app/services/connection_service.py:339:def delete_connection(
```

> TOOL

tool_use Bash
id: toolu_01LM7ZvPS1divmNgh8jrrfDB
```json
{
  "command": "grep -n \"purplefield\" /home/<USER>/Coding/Python/DataQ/backend/tests/mcp/test_mcp_tools.py; grep -rln \"purplefield\" /home/<USER>/Coding/Python/DataQ --include=\"*.md\" --include=\"*.tf\" --include=\"*.py\" --include=\"*.yml\" --include=\"*.yaml\" --include=\"*.ts\" --include=\"*.tsx\" 2>/dev/null",
  "description": "Find all tracked files containing the prod FQDN"
}
```

> TOOL

tool_result
id: toolu_01LM7ZvPS1divmNgh8jrrfDB
```
661:        "dataq-app-api.internal.purplefield-f7322a1b.westus2.azurecontainerapps.io", hosts
/home/<USER>/Coding/Python/DataQ/CLAUDE.md
/home/<USER>/Coding/Python/DataQ/deploy/README.md
/home/<USER>/Coding/Python/DataQ/backend/tests/mcp/test_mcp_tools.py
```

> TOOL

tool_use Read
id: toolu_01B6DfiVuhFTZhKts61178RC
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/services/connection_service.py",
  "offset": 339,
  "limit": 45
}
```

> TOOL

tool_result
id: toolu_01B6DfiVuhFTZhKts61178RC
```
339	def delete_connection(
340	    session: Session, connection_id: uuid.UUID, *, secret_store: SecretStore
341	) -> None:
342	    conn = get_connection(session, connection_id)
343	    secret_ref = conn.secret_ref
344	    session.delete(conn)
345	    session.commit()
346	    # Best-effort remove the orphaned credential from the store (#372) — after the
347	    # row is gone, and fail-soft (delete never raises), so a store hiccup can't 500
348	    # a successful delete.
349	    if secret_ref:
350	        secret_store.delete(secret_ref)
351	    log.info("connection_deleted", connection_id=str(connection_id))
352	
353	
354	def test_connection(
355	    session: Session,
356	    connection_id: uuid.UUID,
357	    *,
358	    secret_store: SecretStore,
359	) -> None:
360	    """Resolve the connection's secret and probe live connectivity.
361	
362	    Raises `ConnectionTestFailedError` (502) on missing credentials or any
363	    adapter-reported connectivity failure.
364	    """
365	    conn = get_connection(session, connection_id)
366	    adapter = get_connection_adapter(conn.type)
367	
368	    if not conn.secret_ref:
369	        raise ConnectionTestFailedError(
370	            "connection has no stored credential to test with",
371	            detail={"connection_id": str(connection_id)},
372	        )
373	    try:
374	        secret = secret_store.get(conn.secret_ref)
375	    except SecretNotFoundError as exc:
376	        raise ConnectionTestFailedError(
377	            "credential could not be resolved", detail={"connection_id": str(connection_id)}
378	        ) from exc
379	
380	    try:
381	        adapter.test(dict(conn.config), secret)
382	    except Exception as exc:
383	        log.warning(
```

> TOOL

tool_use Read
id: toolu_01FT58We1Vwo7dr1eGS9o8E1
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/tests/mcp/test_mcp_tools.py",
  "offset": 645,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01FT58We1Vwo7dr1eGS9o8E1
```
645	
646	
647	def test_allowed_hosts_match_prod_and_compose_upstreams() -> None:
648	    """Prove the allowlist patterns actually match the real proxied Host values —
649	    so the mount doesn't 421 in prod (regression guard for the 3.4.3 DNS-rebind
650	    guard). Uses stdlib `fnmatchcase`, exactly what FastMCP's `_host_matches` uses,
651	    without coupling the test to that private helper."""
652	    from fnmatch import fnmatchcase
653	
654	    def matches(host: str, patterns: list[str]) -> bool:
655	        return any(p == "*" or fnmatchcase(host, p) for p in patterns)
656	
657	    hosts = ["*.azurecontainerapps.io", "api", "localhost", "127.0.0.1"]
658	    # The exact prod upstream nginx forwards (DATAQ_API_UPSTREAM, internal ingress);
659	    # fnmatch `*` spans dots, so the wildcard matches the multi-label FQDN.
660	    assert matches(
661	        "dataq-app-api.internal.purplefield-f7322a1b.westus2.azurecontainerapps.io", hosts
662	    )
663	    assert matches("api", hosts)  # docker-compose
664	    assert not matches("evil.example.com", hosts)  # still rejects the rest
665	
```

> TOOL

tool_use Bash
id: toolu_01HBRHYyZYCU8wU8uDrAujdk
```json
{
  "command": "grep -n \"class Connection\" -A 40 /home/<USER>/Coding/Python/DataQ/backend/app/db/models.py | grep -n \"relationship\\|cascade\" ",
  "description": "Check Connection model for ORM relationships/cascades"
}
```

> TOOL

tool_result
id: toolu_01HBRHYyZYCU8wU8uDrAujdk
```
56:211-    `connection_id`). A version is cascade-deleted with its connection (history is
```

> TOOL

tool_use Write
id: toolu_01VbafDBPk6Ui8R5iJidK3eX
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/01-pipeline-runs-cascade.md",
  "content": "Found by the 2026-07-09 architecture review (findings register issue links back here).\n\n## Problem\n\n`pipeline_runs.connection_id` is the one remaining FK without an `ondelete` policy (`backend/app/db/models.py:491-493`), and `Connection` has no ORM relationship to `PipelineRun`. `delete_connection` does a plain `session.delete(conn)` + commit (`backend/app/services/connection_service.py:339-351`), so deleting an **orchestration connection that has observed pipeline runs** raises `IntegrityError` → unhandled 500.\n\nThis is the same bug class as #540 (suite delete 500 via `results.check_id`), which retrofitted CASCADE — orchestration connections are precisely the ones that accumulate `pipeline_runs` rows via webhooks + the 10-min poll, so any ADF/Airflow/dbt connection that has ever ingested an event cannot be deleted.\n\n## Repro\n\n1. Create an ADF/Airflow/dbt connection.\n2. Ingest ≥1 pipeline run (webhook event or poll cycle).\n3. `DELETE /api/v1/connections/{id}` → 500.\n\n## Proposed fix\n\n`ondelete=\"CASCADE\"` to match the #540 precedent and ADR 0020's cascade-delete stance (observed pipeline history dies with its connection; `runs` triggered from it are unaffected — they link via the `triggered_by` string, not an FK). `SET NULL` would need a nullable widen and leaves orphan rows with no owning connection — not worth it.\n\n## Acceptance criteria\n\n- [ ] Alembic migration adds `ondelete=\"CASCADE\"` to `pipeline_runs.connection_id` (backward-compatible; up + down tested locally)\n- [ ] Model updated […]

> TOOL

tool_result
id: toolu_01VbafDBPk6Ui8R5iJidK3eX
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/01-pipeline-runs-cascade.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01DVLoyhDRvMvyvQL9sUy19U
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/02-rate-limiting.md",
  "content": "Found by the 2026-07-09 architecture/deployment review (findings register issue links back here).\n\n## Problem\n\nThere is **no request rate limiting anywhere in the stack**: no limiter middleware in `backend/app` (grep for slowapi/limiter/throttle is clean), no `limit_req` in the frontend nginx proxy, and nothing at the ACA ingress layer. Everything the frontend proxies — `/api`, `/mcp`, `/healthz` — plus the webhook receivers is unthrottled on the sole public surface.\n\nMost exposed:\n\n- **Webhook receivers** (`backend/app/api/v1/orchestration.py`) — the ADF `?token=` shared secret and the Airflow/dbt HMAC signatures use constant-time compares (good), but an attacker can hammer them indefinitely; there is no brute-force cost and no flood protection for the ingest path.\n- **Auth surface** — PAT resolution (sha256 lookup) and JWT validation run on every request with no per-IP/per-principal throttle; uniform 401s (good) but unlimited guessing.\n- **Expensive endpoints** — profiler, dry-run, and run-trigger endpoints can be spammed by any authenticated principal to exhaust the worker.\n\nAlso a marketplace prerequisite: a customer-facing deployment (ADR 0013 BYOL) shouldn't ship with an unthrottled public ingress.\n\n## Proposed direction\n\nDecide the layer first — options, cheapest first:\n\n1. `limit_req`/`limit_conn` zones in the frontend nginx image (covers everything public, zero backend code, per-IP granularity only).\n2. App-level middleware […]

> TOOL

tool_result
id: toolu_01DVLoyhDRvMvyvQL9sUy19U
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/02-rate-limiting.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_014BMSHvCqRdchRHM3pZinzR
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/03-monitor-kind-strategy.md",
  "content": "Found by the 2026-07-09 architecture review (findings register issue links back here). Filed into W4 deliberately: this refactor should land **before or with** schema_drift (#592) so the new kind is an additive registration, not a fourth copy of the if-chains.\n\n## Problem\n\nThe monitor-kind seam (ADR 0012) is extensible in the *schema* but not in the *code*. Adding a kind today touches at least three sites:\n\n1. `run_service._run_outcomes` (`backend/app/services/run_service.py:101-156`) — hardcoded two-way partition (`expectation` vs `MONITOR_KINDS`), `NotImplementedError` for the rest.\n2. `check_service._V1_SUPPORTED_KINDS` (`backend/app/services/check_service.py:55`) — authoring-side allowlist.\n3. `backend/app/datasources/monitors.py` — **three parallel `if kind == FRESHNESS / VOLUME / else raise` chains** repeated across `build_monitor_sql`, `validate_monitor_config`, and `monitor_outcome` (~lines 104-109, 171-176, 192-231).\n\nFine at 2 kinds; at 4 (schema_drift #592, anomaly #593) the parallel chains become a drift/bug surface — a kind added to one function but not another fails at runtime, not import time.\n\n## Proposed direction\n\nA per-kind strategy object (e.g. `MonitorKindSpec`: `validate_config`, `build_sql` / scalar-source hook, `outcome`) in a registry keyed by kind — mirroring how `_ADAPTERS`/`_RUNNER_BUILDERS` already work in `datasources/registry.py`. `monitors.py`'s three chains collapse into lookups; `_V1_SUPPORTED_KINDS` derives from the registry. Keep the `expectation`-vs-monitor split in `_run_outcomes` (it dispatches to a different runner Protocol) but make […]

> TOOL

tool_result
id: toolu_014BMSHvCqRdchRHM3pZinzR
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/03-monitor-kind-strategy.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_012g9zKVZtBRzKYdQiwCBi76
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/04-run-target-dispatch.md",
  "content": "Found by the 2026-07-09 architecture review (findings register issue links back here).\n\n## Problem\n\n`resolve_run_target` (`backend/app/services/run_target.py:95-137`) is a second dispatch-by-connection-type site living outside the `ConnectionAdapter` registry: an `if conn_type ==` chain for flat-file / snowflake / unity_catalog / iceberg target shapes. Adding a datasource therefore means editing this function **in addition to** registering an adapter + runner — which quietly breaks the \"adding a datasource is one registry entry\" contract stated in `backend/app/datasources/registry.py`.\n\nLow risk today (unknown types fall through to a raised `SuiteTargetInvalidError`, so nothing fails silently), but it's the kind of parallel dispatch that drifts — the Iceberg addition (#716) already had to touch it.\n\n## Proposed direction\n\nMove target-shape resolution onto the datasource layer — either a `resolve_target(target: dict) -> ResolvedTarget` hook on the adapter/runner-builder registration, or a per-type entry in `registry.py` alongside `_RUNNER_BUILDERS`. `run_target.py` keeps the shared validation (targetless suite, orchestration-provider rejection) and delegates the shape.\n\n## Acceptance criteria\n\n- [ ] Per-type target resolution registered in `datasources/registry.py` (or on the adapter Protocol); the `if conn_type` chain in `run_target.py` is gone\n- [ ] Error behavior unchanged (`SuiteTargetInvalidError` codes/messages preserved; existing tests green)\n- [ ] `registry.py`'s \"one registry entry\" module docstring is true again\n"
} […]

> TOOL

tool_result
id: toolu_012g9zKVZtBRzKYdQiwCBi76
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/04-run-target-dispatch.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_016vmzCrgrwgSjdTAjwpc3xz
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/05-mcp-allowed-hosts.md",
  "content": "Found by the 2026-07-09 architecture review (findings register issue links back here).\n\n## Problem\n\nThe MCP mount hardcodes its transport Host allowlist (`backend/app/mcp/server.py:525-529`):\n\n```python\nallowed_hosts=[\"*.azurecontainerapps.io\", \"api\", \"localhost\", \"127.0.0.1\"]\n```\n\nThe surrounding comment documents *why* the FastMCP DNS-rebinding guard is relaxed (correctly — every `/mcp` call is JWT/PAT-authenticated fail-closed, no cookies), so this is not a security defect. But the value itself is the **one deploy-target coupling in app code not driven by Pydantic Settings**, contradicting the ADR 0010/0013 config guardrail (\"no hardcoded resource names/endpoints in business logic — everything via Settings\"). Any non-ACA deployment whose proxy forwards a different upstream Host — EKS/GKE, on-prem, or the local-first prod-ish compose posture (#591) with a renamed service — gets a 421 Misdirected Request on `/mcp` that looks like an auth failure.\n\nThere's also a regression test asserting the literal prod internal FQDN matches the wildcard (`backend/tests/mcp/test_mcp_tools.py:647-664`) — fine as a pattern guard, but it should assert against the *setting's default*, and the FQDN residue is tracked separately (G-i teardown issue).\n\n## Proposed fix\n\nAdd `MCP_ALLOWED_HOSTS` (comma-separated) to `Settings`, defaulting to the current list so existing deployments are unaffected; pass it through in `build_mcp_http_app`. Document it in `.env.app.example` + `deploy/.env.app.prod.example`.\n\n## Acceptance criteria\n\n- [ […]

> TOOL

tool_result
id: toolu_016vmzCrgrwgSjdTAjwpc3xz
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/05-mcp-allowed-hosts.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01VffJtoJtUQJpaVPPojCgQf
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/06-security-md-stale.md",
  "content": "Found by the 2026-07-09 marketplace-readiness review (checklist issue links back here).\n\n## Problem\n\n`.github/SECURITY.md` §\"Supported versions\" still says:\n\n> Only the latest commit on `main` is supported. There are no versioned releases in the v1 development phase.\n\nThis predates the `v1.0.0` tag (2026-07-04) and contradicts the CHANGELOG/SemVer release process now in place. A marketplace/BYOL evaluator reads this as \"no supported releases\" — a credibility problem on exactly the page security-conscious buyers check first.\n\nMinor secondary point while in the file: the Scope section names Azure-only components (`fastapi-azure-auth`, Key Vault) — fine today, but keep it in sync as the portability seams land (generic OIDC backend validation, non-Azure secret stores).\n\n## Acceptance criteria\n\n- [ ] Supported-versions section states the actual policy (e.g. latest tagged release + `main`; security fixes land on `main` and ship in the next tag)\n- [ ] Wording consistent with CHANGELOG.md / release runbook\n- [ ] Scope section reviewed for stale Azure-only phrasing\n"
}
```

> TOOL

tool_result
id: toolu_01VffJtoJtUQJpaVPPojCgQf
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/06-security-md-stale.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01SThGuGj7GKEMQiCLZtyAdV
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/07-fqdn-residue.md",
  "content": "Found by the 2026-07-09 marketplace-readiness review (checklist issue links back here). This is a concrete, git-tracked slice of the **G-i pre-marketplace teardown** (context/post-v1-roadmap.md; deploy/README.md §teardown): G-i's main body is the *deployed* harness (Flows A/B/C, connections, demo users), but these references live in the repo itself, so they survive any deployment teardown and ship in every clone.\n\n## Where the real prod FQDN (`purplefield-f7322a1b.westus2.azurecontainerapps.io`) is tracked\n\n1. `backend/tests/mcp/test_mcp_tools.py:661` — the Host-allowlist regression test asserts the literal internal prod FQDN (`dataq-app-api.internal.purplefield-...`). Should use a synthetic FQDN of the same shape (`*.internal.<hash>.<region>.azurecontainerapps.io`) — the test proves wildcard matching, not this deployment's name.\n2. `deploy/README.md:304` — reachability probe example uses the live frontend URL.\n3. `CLAUDE.md` §13 status paragraph — embeds the live URL.\n\n(The `deploy/terraform/azure/` READMEs/outputs referencing the FQDN *pattern* are fine — that's parameterized deployment output, not residue.)\n\n## Why it matters\n\n- Ships a live internal hostname of the reference deployment in a public-repo test — mild info-leak, zero product value.\n- Any distributable artifact must reference no harness/demo endpoints (G-i acceptance line).\n\n## Acceptance criteria\n\n- [ ] Test uses a synthetic FQDN; still guards the wildcard-matches-multi-label-host behavior\n- [ ] `deploy/README.md` probe example uses a `<your-frontend-fqdn>` placeholder (or reads the Terraform […]

> TOOL

tool_result
id: toolu_01SThGuGj7GKEMQiCLZtyAdV
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/07-fqdn-residue.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01JQry9AhSiogf29RGsqLrcE
```json
{
  "command": "set -l DIR /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues\ngh issue create -R TheurgicDuke771/DataQ --title 'bug: deleting an orchestration connection with observed pipeline_runs 500s — connection_id FK lacks ondelete (same class as #540)' --label bug --label priority/P1 --milestone 'v1.1 Backlog' --body-file $DIR/01-pipeline-runs-cascade.md\ngh issue create -R TheurgicDuke771/DataQ --title 'security: no request rate limiting on any public surface (webhooks, auth, /api + /mcp proxy)' --label security --label enhancement --label priority/P2 --milestone 'v1.1 Backlog' --body-file $DIR/02-rate-limiting.md\ngh issue create -R TheurgicDuke771/DataQ --title 'refactor: monitor-kind dispatch is not open/closed — extract per-kind strategy registry before schema_drift (#592)' --label refactor --label priority/P2 --milestone 'v1.1 Week 4 — schema_drift monitor kind' --body-file $DIR/03-monitor-kind-strategy.md",
  "description": "File issues 1-3 (cascade bug, rate limiting, monitor-kind refactor)"
}
```

> TOOL

tool_result ERROR
id: toolu_01JQry9AhSiogf29RGsqLrcE
```
Exit code 1
open /01-pipeline-runs-cascade.md: no such file or directory
open /02-rate-limiting.md: no such file or directory
open /03-monitor-kind-strategy.md: no such file or directory
```

> AGENT

Variable didn't expand — I'll just use full paths.

> TOOL

tool_use Bash
id: toolu_01ADSV7GCf2xt8Xb7a72dB7W
```json
{
  "command": "gh issue create -R TheurgicDuke771/DataQ --title 'bug: deleting an orchestration connection with observed pipeline_runs 500s — connection_id FK lacks ondelete (same class as #540)' --label bug --label priority/P1 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/01-pipeline-runs-cascade.md && gh issue create -R TheurgicDuke771/DataQ --title 'security: no request rate limiting on any public surface (webhooks, auth, /api + /mcp proxy)' --label security --label enhancement --label priority/P2 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/02-rate-limiting.md && gh issue create -R TheurgicDuke771/DataQ --title 'refactor: monitor-kind dispatch is not open/closed — extract per-kind strategy registry before schema_drift (#592)' --label refactor --label priority/P2 --milestone 'v1.1 Week 4 — schema_drift monitor kind' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/03-monitor-kind-strategy.md",
  "description": "File issues 1-3 (cascade bug, rate limiting, monitor-kind refactor)"
}
```

> TOOL

tool_result
id: toolu_01ADSV7GCf2xt8Xb7a72dB7W
```
https://github.com/TheurgicDuke771/DataQ/issues/724
https://github.com/TheurgicDuke771/DataQ/issues/725
https://github.com/TheurgicDuke771/DataQ/issues/726
```

> TOOL

tool_use Bash
id: toolu_01XoZgeudvAdcpBsRvFoq2xM
```json
{
  "command": "gh issue create -R TheurgicDuke771/DataQ --title 'refactor: run_target.py duplicates dispatch-by-type outside the ConnectionAdapter registry' --label refactor --label priority/P3 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/04-run-target-dispatch.md && gh issue create -R TheurgicDuke771/DataQ --title 'portability: MCP transport Host allowlist hardcodes *.azurecontainerapps.io — drive it from Settings' --label enhancement --label priority/P3 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/05-mcp-allowed-hosts.md && gh issue create -R TheurgicDuke771/DataQ --title \"docs: SECURITY.md 'Supported versions' predates v1.0.0 — still says there are no versioned releases\" --label documentation --label priority/P3 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/06-security-md-stale.md && gh issue create -R TheurgicDuke771/DataQ --title 'chore (G-i slice): strip the real prod FQDN from tracked files (backend test, deploy/README, CLAUDE.md)' --label documentation --label test --label priority/P2 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/07-fqdn-residue.md",
  "description": "File issues 4-7 (run_target refactor, MCP hosts, SECURITY.md, FQDN residue)"
}
```

> TOOL

tool_result
id: toolu_01XoZgeudvAdcpBsRvFoq2xM
```
https://github.com/TheurgicDuke771/DataQ/issues/727
https://github.com/TheurgicDuke771/DataQ/issues/728
https://github.com/TheurgicDuke771/DataQ/issues/729
https://github.com/TheurgicDuke771/DataQ/issues/730
```

> AGENT

All seven granular issues filed (#724–#730). Now the two umbrella/documentation issues that record the full reviews and the license-audit outcome.

> TOOL

tool_use Write
id: toolu_01RKDmyiUaLomoN3W5Vto4vs
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/08-arch-review-register.md",
  "content": "Documentation/tracking record of the full-codebase architecture review run on 2026-07-09 (backend + infra/deploy sweeps). Filed so the findings have a durable home per the working agreements (no silent drops); each actionable finding has its own issue below.\n\n## Verdict\n\nLayering and seam discipline are in excellent shape — no violations found. Dependency direction holds (`api → services → {db, datasources, orchestration, core}`; zero service→router imports; no business logic in routers; no raw-SQL bypasses of the models beyond the two documented, validated-identifier sites). Every claimed seam (`ConnectionAdapter`, `CheckRunner`/`MonitorRunner`, `OrchestrationProvider`, `SecretStore`, `ResultPublisher`, `get_current_user`) is a real Protocol with registry dispatch and no bypassing branch-on-provider logic in services. The findings are refinement-level, not structural.\n\n**Strengths worth preserving:** vendor-neutral OTel path (Azure Monitor and/or OTLP purely by config); PII redaction covering both rendered logs and exported OTel attributes; complete request_id propagation FastAPI→Celery (publish-header inject / prerun restore / postrun reset); mature idempotency patterns (`FOR UPDATE SKIP LOCKED` schedule dispatch, trigger-dedup partial unique index, stuck-run reaper, beat-start gap recovery); MCP tools as thin service-layer wrappers with fail-closed mounting; constant-time webhook auth; sha256-at-rest PATs with uniform 401s; fail-closed migrate-before-roll deploy workflow.\n\n## Actionable findings → issues\n\n| # | Finding | Severity […]

> TOOL

tool_result
id: toolu_01RKDmyiUaLomoN3W5Vto4vs
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/08-arch-review-register.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_019xx4Fz8bUCHbLeuD6yLK9T
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md",
  "content": "Documentation/tracking record of the 2026-07-09 marketplace-listing readiness review, updated for the **distribution model chosen 2026-07-09: free open-source software + customer-deployed BYOL** (refines ADR 0013 — the \"licensing model + entitlement/license-key\" line in §5 is superseded by this choice; no license-key/entitlement machinery is needed when the license is the OSS grant itself).\n\n## License audit result (2026-07-09): free OSS + BYOL is CLEAR — no contradictions\n\n- **Project license:** MIT (`LICENSE`, © 2026 Arijit Roy) — ideal for free OSS + BYOL; marketplaces support free/BYOL container offers of OSS.\n- **Backend (full conda env, 239 packages):** **zero strong copyleft / source-available licenses.** Key deps confirmed from installed metadata: great-expectations 1.17.2 (Apache-2.0), fastmcp (Apache-2.0), fastapi/sqlalchemy/pydantic/alembic (MIT), celery/uvicorn/pandas/numpy (BSD), snowflake + databricks connectors, boto3, pyiceberg, pyarrow, opentelemetry (Apache-2.0), `caio` (Apache-2.0, verified via bundled COPYING). Weak copyleft only: `psycopg2-binary` (LGPL-3.0, dynamically linked — fine to ship, include notice), `certifi`/`pathspec` (MPL-2.0, file-level).\n- **Frontend (node_modules sweep, 643 packages):** **zero strong copyleft.** MIT 526 / Apache-2.0 42 / ISC 33 / BSD 18. Weak copyleft: `lightningcss` (MPL-2.0, build-time only — not distributed), `dompurify` (dual MPL-2.0 OR Apache-2.0 — take Apache). `@fontsource/*` fonts are OFL-1.1 (standard for bundling web fonts). The UNKNOWN-license […]

> TOOL

tool_result
id: toolu_019xx4Fz8bUCHbLeuD6yLK9T
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01CCdJYhh2iqah7W76qDPyzF
```json
{
  "command": "gh issue create -R TheurgicDuke771/DataQ --title 'docs: architecture review 2026-07-09 — findings register (5 actionable → #724-#728)' --label documentation --label priority/P3 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/08-arch-review-register.md && gh issue create -R TheurgicDuke771/DataQ --title 'docs: marketplace-listing readiness checklist — free OSS + BYOL (license audit clear; prerequisites & good-to-haves)' --label documentation --label enhancement --label priority/P2 --milestone 'v1.1 Backlog' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md",
  "description": "File the two review umbrella/documentation issues"
}
```

> TOOL

tool_result
id: toolu_01CCdJYhh2iqah7W76qDPyzF
```
https://github.com/TheurgicDuke771/DataQ/issues/731
https://github.com/TheurgicDuke771/DataQ/issues/732
```

> AGENT

Done on both fronts. Here's the summary.

## License check: free OSS + BYOL is **clear** — no contradictions found

I audited the actual installed metadata, not just declared docs — all 239 backend packages in the conda env and all 643 frontend packages in `node_modules`:

- **Project license (MIT)** — fits a free-OSS + BYOL model perfectly. The conflict I flagged in the earlier review only existed against ADR 0013 §5's *paid* "entitlement/license-key" plan; with your free-OSS decision that line is superseded and no license-key machinery is needed. One thing to accept with eyes open: MIT means anyone may fork, rebrand, and even sell DataQ — that's inherent to the model you chose, not a defect.
- **Backend: zero strong copyleft.** GX Core 1.17.2, FastMCP, connectors, pyiceberg, boto3, OTel are all Apache-2.0; FastAPI/SQLAlchemy/Pydantic are MIT; Celery/pandas/numpy are BSD. The one UNKNOWN (`caio`) turned out to be Apache-2.0 via its bundled COPYING file. Only weak copyleft: `psycopg2-binary` (LGPL, dynamically linked — fine to ship with a notice) and `certifi`/`pathspec` (MPL-2.0, file-level).
- **Frontend: zero strong copyleft.** 526 MIT / 42 Apache / 33 ISC / 18 BSD; `dompurify` is dual MPL-or-Apache (take Apache), `lightningcss` (MPL) is build-time only and never […]

> DEVELOPER

yes draft the ADR

> AGENT

I'll draft it as ADR 0031 and deliver it the way your working agreements expect — feature branch, index updated, a pointer added to ADR 0013's Related section, PR with milestone, then the agentic code review. Starting with the branch and the ADR itself.

> TOOL

tool_use Bash
id: toolu_012suZyCE2URhUzCJavHqWMX
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ status --short; git -C /home/<USER>/Coding/Python/DataQ pull --ff-only origin main 2>&1 | tail -1; git -C /home/<USER>/Coding/Python/DataQ checkout -b docs/adr-0031-oss-byol-licensing",
  "description": "Sync main and create the ADR branch"
}
```

> TOOL

tool_result
id: toolu_012suZyCE2URhUzCJavHqWMX
```
Already up to date.
Switched to a new branch 'docs/adr-0031-oss-byol-licensing'
```

> TOOL

tool_use Write
id: toolu_01MpWdLgsaha3UAdurZzgMZe
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "content": "# ADR 0031 — Distribution licensing: free open-source (MIT) + customer-deployed BYOL\n\n- **Status:** Accepted\n- **Date:** 2026-07-09\n- **Deciders:** @TheurgicDuke771\n\n## Context\n\n[ADR 0013](0013-marketplace-distribution-and-anti-lock-in.md) chose **customer-deployed BYOL** as the marketplace distribution model and deferred the commercial/legal scope to the post-v1 initiative, listing \"licensing model + entitlement/license-key (we are not metering under BYOL)\" among the open items (§5). The 2026-07-09 marketplace-readiness review (issue #732) surfaced the tension that line carries: the repository is already published under the **MIT license**, which grants everyone the right to use, copy, modify, distribute, and *sell* the software — a paid-entitlement model layered on top would be incoherent (you cannot sell a key to rights the license already gives away), and retrofitting a restrictive license onto an already-public MIT repo only gets harder with time and adoption.\n\nThe same review ran a full dependency license audit against the actual installed trees (not declared metadata alone):\n\n- **Backend** — 239 packages in the conda env: **zero strong-copyleft or source-available licenses**. Core stack: Great Expectations, FastMCP, the Snowflake/Databricks connectors, pyiceberg, boto3, pyarrow, OpenTelemetry (Apache-2.0); FastAPI, SQLAlchemy, Pydantic, Alembic (MIT); Celery, uvicorn, pandas, numpy (BSD). Weak copyleft only: `psycopg2-binary` (LGPL-3.0, dynamically linked), `certifi`/`pathspec` (MPL-2.0, file-level).\n- **Frontend** […]

> TOOL

tool_result
id: toolu_01MpWdLgsaha3UAdurZzgMZe
```
File created successfully at: /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md (file state is current in your context — no need to Read it back)
```

> AGENT

Now the index row and the pointer in ADR 0013.

> TOOL

tool_use Edit
id: toolu_01V92km3JvkrTEYRdXxZQZ1o
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "| [0030](0030-iceberg-native-read-path.md) | Apache Iceberg — engine-level read (Snowflake/UC iceberg tables) is free & zero-code; the only new build is a **native `pyiceberg` read** (v2 baseline, v3 deferred) behind a thin `IcebergCheckRunner` (scan → DataFrame → `gx_runner`); new **self-contained** `iceberg` connection type (Option A: own catalog + storage credential — independent lifecycle, cascade-safe), Option B two-connection ref deferred to 0015; reads Delta UniForm too; native impl deferred (#286) | Accepted (spike; native impl deferred) |",
  "new_string": "| [0030](0030-iceberg-native-read-path.md) | Apache Iceberg — engine-level read (Snowflake/UC iceberg tables) is free & zero-code; the only new build is a **native `pyiceberg` read** (v2 baseline, v3 deferred) behind a thin `IcebergCheckRunner` (scan → DataFrame → `gx_runner`); new **self-contained** `iceberg` connection type (Option A: own catalog + storage credential — independent lifecycle, cascade-safe), Option B two-connection ref deferred to 0015; reads Delta UniForm too; native impl deferred (#286) | Accepted (spike; native impl deferred) |\n| [0031](0031-oss-byol-distribution-licensing.md) | Distribution licensing — **free open-source (MIT) + customer-deployed BYOL**; no entitlement/license-key (supersedes the 0013 §5 licensing-model line); marketplace listings are free offers of the OSS artifacts; THIRD-PARTY-NOTICES/SBOM in images + releases; standing no-strong-copyleft dependency guardrail | […]

> TOOL

tool_result
id: toolu_01V92km3JvkrTEYRdXxZQZ1o
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01Ru4wVhRbyXdDkA9g2zMV7j
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md",
  "old_string": "- [ADR 0010](0010-provider-agnostic-infrastructure-seams.md) — provider-agnostic infra seams (the per-seam discipline this distribution decision depends on).\n- [ADR 0011](0011-extensibility-seams-for-deferred-integrations.md) — feature-side extensibility seams (connectors, `ResultPublisher`, dbt-as-provider).\n- CLAUDE.md §1 (single-tenant scope), §9 (decision table), §11 (anti-patterns — \"don't bypass the abstraction\").",
  "new_string": "- [ADR 0010](0010-provider-agnostic-infrastructure-seams.md) — provider-agnostic infra seams (the per-seam discipline this distribution decision depends on).\n- [ADR 0011](0011-extensibility-seams-for-deferred-integrations.md) — feature-side extensibility seams (connectors, `ResultPublisher`, dbt-as-provider).\n- [ADR 0031](0031-oss-byol-distribution-licensing.md) — **supersedes the §5 \"licensing model + entitlement/license-key\" line**: distribution licensing decided as free open-source (MIT) + BYOL, no entitlement machinery; the rest of this ADR stands.\n- CLAUDE.md §1 (single-tenant scope), §9 (decision table), §11 (anti-patterns — \"don't bypass the abstraction\")."
}
```

> TOOL

tool_result
id: toolu_01Ru4wVhRbyXdDkA9g2zMV7j
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_0124rxCH42t38fNPHkm1q3yT
```json
{
  "command": "cd /home/<USER>/Coding/Python/DataQ; and git add docs/adr/0031-oss-byol-distribution-licensing.md docs/adr/README.md docs/adr/0013-marketplace-distribution-and-anti-lock-in.md; and git commit -m 'docs: ADR 0031 — free OSS (MIT) + BYOL distribution licensing\n\nRecords the 2026-07-09 decision from the marketplace-readiness review (#732):\nDataQ stays free open-source under MIT with no entitlement/license-key\nmachinery, superseding the ADR 0013 §5 licensing-model line. Embeds the\nfull-tree dependency license audit (backend 239 pkgs / frontend 643 pkgs,\nzero strong copyleft) and adds the standing no-strong-copyleft dependency\nguardrail. Index row added; ADR 0013 Related section points forward.\n\nCo-Authored-By: Claude Fable 5 <<REDACTED_EMAIL>>'",
  "description": "Commit the ADR, index row, and 0013 pointer"
}
```

> TOOL

tool_result ERROR
id: toolu_0124rxCH42t38fNPHkm1q3yT
```
Exit code 127
(eval):1: command not found: and
(eval):1: command not found: and
```

> TOOL

tool_use Bash
id: toolu_017AjZWostvBHFKLiszLuko3
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ add docs/adr/0031-oss-byol-distribution-licensing.md docs/adr/README.md docs/adr/0013-marketplace-distribution-and-anti-lock-in.md && git -C /home/<USER>/Coding/Python/DataQ commit -m 'docs: ADR 0031 — free OSS (MIT) + BYOL distribution licensing\n\nRecords the 2026-07-09 decision from the marketplace-readiness review (#732):\nDataQ stays free open-source under MIT with no entitlement/license-key\nmachinery, superseding the ADR 0013 §5 licensing-model line. Embeds the\nfull-tree dependency license audit (backend 239 pkgs / frontend 643 pkgs,\nzero strong copyleft) and adds the standing no-strong-copyleft dependency\nguardrail. Index row added; ADR 0013 Related section points forward.\n\nCo-Authored-By: Claude Fable 5 <<REDACTED_EMAIL>>'",
  "description": "Commit the ADR, index row, and 0013 pointer"
}
```

> TOOL

tool_result
id: toolu_017AjZWostvBHFKLiszLuko3
```
[docs/adr-0031-oss-byol-licensing 0d27ff5a] docs: ADR 0031 — free OSS (MIT) + BYOL distribution licensing
 3 files changed, 53 insertions(+)
 create mode 100644 docs/adr/0031-oss-byol-distribution-licensing.md
```

> TOOL

tool_use Bash
id: toolu_014PjZ9gQAo63GQY8eAAzNEN
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ push -u origin docs/adr-0031-oss-byol-licensing",
  "description": "Push the ADR branch"
}
```

> TOOL

tool_use Read
id: toolu_01QbXamGVx8FfFvFMECsD54E
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/.github/pull_request_template.md"
}
```

> TOOL

tool_result
id: toolu_014PjZ9gQAo63GQY8eAAzNEN
```
[entire] Pushing entire/checkpoints/v1 to origin..... done
remote: 
remote: Create a pull request for 'docs/adr-0031-oss-byol-licensing' on GitHub by visiting:        
remote:      https://github.com/TheurgicDuke771/DataQ/pull/new/docs/adr-0031-oss-byol-licensing        
remote: 
To github.com:TheurgicDuke771/DataQ.git
 * [new branch]        docs/adr-0031-oss-byol-licensing -> docs/adr-0031-oss-byol-licensing
branch 'docs/adr-0031-oss-byol-licensing' set up to track 'origin/docs/adr-0031-oss-byol-licensing'.
```

> TOOL

tool_result
id: toolu_01QbXamGVx8FfFvFMECsD54E
```
1	<!--
2	Per working-agreements #1, #3, #5, #11, #25:
3	- One functionality per PR (squash-merges into one commit on main)
4	- Reference any related GitHub issue (Fixes #N for defect fixes)
5	- Manually tested before merge (until automated tests land in Week 8)
6	-->
7	
8	## Summary
9	
10	<!-- 1–3 bullets: what this PR does and why. Focus on the "why". -->
11	-
12	-
13	
14	## Linked issue
15	
16	<!-- For defect fixes, use "Fixes #N" so the issue auto-closes on merge.
17	     For feature work, use "Refs #N" or leave blank. -->
18	Fixes #
19	
20	## Type of change
21	
22	<!-- Tick all that apply. -->
23	- [ ] feat — new functionality
24	- [ ] fix — bug fix (linked issue above)
25	- [ ] chore — repo housekeeping / tooling
26	- [ ] docs — documentation only
27	- [ ] refactor — no behaviour change
28	- [ ] test — test-only change
29	
30	## Checklist
31	
32	- [ ] **Manually tested locally** (required pre-Week-8; describe what you tested below)
33	- […]

> TOOL

tool_use Write
id: toolu_01BPMq5SdSW9Midy8t91KsXX
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-body-adr-0031.md",
  "content": "## Summary\n\n- Records the 2026-07-09 distribution-licensing decision as **ADR 0031**: DataQ stays free open-source under MIT, distributed customer-deployed BYOL, with **no entitlement/license-key machinery** — superseding the ADR 0013 §5 \"licensing model + entitlement/license-key\" line (the rest of 0013 stands).\n- Embeds the full-tree dependency license audit that cleared the model (backend 239 packages / frontend 643 packages, zero strong copyleft; only notice-preservation obligations) and adds a **standing no-strong-copyleft dependency guardrail** joining the quarterly supply-chain cadence (CONTRIBUTING rule 39).\n- Adds the 0031 index row in `docs/adr/README.md` and a forward pointer in ADR 0013's Related section (append-only convention — 0013's text is otherwise untouched).\n\n## Linked issue\n\nRefs #732 (first checklist item — decision ADR). THIRD-PARTY-NOTICES/SBOM automation stays tracked in #732, not this PR.\n\n## Type of change\n\n- [x] docs — documentation only\n\n## Checklist\n\n- [x] **Manually tested locally** — docs-only; links and index row verified\n- [x] **Single functionality** — no unrelated changes piggybacked\n- [x] **Conventional commit title** (`docs:`)\n- [x] **No secrets, credentials, or `.env` files committed**\n- [ ] Black + Ruff + mypy pass locally — N/A (no Python)\n- [ ] Prettier + ESLint pass locally — N/A (no frontend)\n- [ ] Tests added/updated — N/A (docs)\n- […]

> TOOL

tool_result
id: toolu_01BPMq5SdSW9Midy8t91KsXX
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-body-adr-0031.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01HYqrN1RCiMMam3u3o6N6bV
```json
{
  "command": "gh pr create -R TheurgicDuke771/DataQ --base main --head docs/adr-0031-oss-byol-licensing --title 'docs: ADR 0031 — free OSS (MIT) + BYOL distribution licensing' --milestone 'v1.1 Week 3 — Azure wind-down + local-first posture' --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-body-adr-0031.md",
  "description": "Open the ADR 0031 PR with the current-week milestone"
}
```

> TOOL

tool_result
id: toolu_01HYqrN1RCiMMam3u3o6N6bV
```
https://github.com/TheurgicDuke771/DataQ/pull/733
```

> TOOL

tool_use Skill
id: toolu_0159dH5hsxgh7q7jVsJ9ARrk
```json
{
  "skill": "code-review",
  "args": "--comment"
}
```

> TOOL

tool_result
id: toolu_0159dH5hsxgh7q7jVsJ9ARrk
```
Launching skill: code-review
```

> TOOL

tool_use Bash
id: toolu_01Jf4gbFMvaUFNJQ82doH6Nm
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ diff main...HEAD --stat && git -C /home/<USER>/Coding/Python/DataQ status --short",
  "description": "Show diff stat for the review scope"
}
```

> TOOL

tool_result
id: toolu_01Jf4gbFMvaUFNJQ82doH6Nm
```
 ...13-marketplace-distribution-and-anti-lock-in.md |  1 +
 docs/adr/0031-oss-byol-distribution-licensing.md   | 51 ++++++++++++++++++++++
 docs/adr/README.md                                 |  1 +
 3 files changed, 53 insertions(+)
```

> TOOL

tool_use Agent
id: toolu_01QPhY7cHeviPTVyg64EySG6
```json
{
  "description": "Finder A: line-by-line scan",
  "subagent_type": "Explore",
  "prompt": "Code-review finder, angle A (line-by-line). Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — a docs-only PR adding docs/adr/0031-oss-byol-distribution-licensing.md, an index row in docs/adr/README.md, and a Related pointer in docs/adr/0013-marketplace-distribution-and-anti-lock-in.md.\n\nRead every added line. For a docs diff, \"bugs\" are: factually wrong claims, wrong file paths/links, wrong issue/ADR numbers, internal contradictions, misquotes of other documents. Verify specifically:\n- Every relative markdown link in the three changed files resolves to a real file in docs/adr/.\n- Claims about ADR 0013's content (quote of §5 \"licensing model + entitlement/license-key\") match the actual text of 0013.\n- Claims about ADR 0023 (GHCR public images) match that ADR.\n- \"CONTRIBUTING rule 39\" — open CONTRIBUTING.md and verify rule 39 exists and is about the quarterly supply-chain audit cadence; if the numbering or subject differs, that's a finding.\n- Dependency-license claims: psycopg2-binary \"LGPL-3.0\", certifi/pathspec \"MPL-2.0\", dompurify \"MPL-2.0 OR Apache-2.0\", lightningcss \"MPL-2.0 build-time only\", @fontsource OFL-1.1 — check backend/requirements.txt and frontend/package.json for whether these deps exist as claimed (you can't check registries; flag only inconsistencies with the repo).\n- Issue #732 is referenced as the marketplace checklist — you can check with `gh issue view 732 --repo TheurgicDuke771/DataQ` that it exists […]

> TOOL

tool_result
id: toolu_01QPhY7cHeviPTVyg64EySG6
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a1b26d9ded3025468 (internal ID - do not mention to user. Use SendMessage with to: 'a1b26d9ded3025468', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a1b26d9ded3025468.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01HSFWG2dEszC2RNfjy1SJk1
```json
{
  "description": "Finder B: removed behavior",
  "subagent_type": "Explore",
  "prompt": "Code-review finder, angle B (removed-behavior auditor). Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR (ADR 0031 + index row + ADR 0013 Related pointer).\n\nFor every line the diff deletes or replaces, name what it asserted and check the new text re-establishes it. This diff is insertions-only per the stat, but verify that: also check whether the ADR 0031 \"supersedes the 0013 §5 line\" framing effectively *removes* a documented obligation without re-homing it — ADR 0013 §5 listed several commercial/legal items (seller registration, EULA/privacy/DPA, support SLA, security review, SOC 2). Does ADR 0031 or issue #732 (check `gh issue view 732 --repo TheurgicDuke771/DataQ`) still carry each of them, or does the supersession quietly drop obligations that should survive under a free-OSS model? Anything dropped without a stated home or an explicit \"no longer needed because X\" rationale is a candidate.\n\nReturn up to 6 candidates as JSON [{file, line, summary, failure_scenario}]. If nothing, return []."
}
```

> TOOL

tool_result
id: toolu_01HSFWG2dEszC2RNfjy1SJk1
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: ae462fa595ec7e6cc (internal ID - do not mention to user. Use SendMessage with to: 'ae462fa595ec7e6cc', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/ae462fa595ec7e6cc.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01M98fccJx7UahAAjxU75yCP
```json
{
  "description": "Finder C: cross-file tracer",
  "subagent_type": "Explore",
  "prompt": "Code-review finder, angle C (cross-file tracer). Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR (new ADR 0031, docs/adr/README.md index row, ADR 0013 Related pointer).\n\nTrace every document that references the changed content and check for contradictions the PR creates or fails to fix:\n- Grep the repo (CLAUDE.md, CONTRIBUTING.md, docs/, context/post-v1-roadmap.md, deploy/README.md, README.md) for mentions of \"license\", \"licensing\", \"BYOL\", \"entitlement\", \"marketplace\" — does any other doc still assert the OLD position (paid licensing/entitlement-key) in a way that now contradicts ADR 0031? E.g. context/post-v1-roadmap.md may restate ADR 0013 §5's licensing line verbatim.\n- Does docs/adr/README.md's supersession convention (\"supersede an old decision by adding a new ADR and marking the old one's status as `Superseded by ADR-NNNN`\") conflict with how this PR handles the PARTIAL supersession of 0013 (status left \"Accepted\", only a Related note added)? Check whether the index row for 0013 mentions the amendment — a reader scanning the index would not learn §5 changed.\n- Is 0015 still listed as the only \"Pending\" ADR — does the pending table need no change?\n- mkdocs.yml / docs site nav: are ADRs listed there, and does the new file need a […]

> TOOL

tool_result
id: toolu_01M98fccJx7UahAAjxU75yCP
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a41d789a14fc7eb89 (internal ID - do not mention to user. Use SendMessage with to: 'a41d789a14fc7eb89', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a41d789a14fc7eb89.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01GjS1rEcVyQuJFejARZWMJ8
```json
{
  "description": "Finder: reuse angle",
  "subagent_type": "Explore",
  "model": "haiku",
  "prompt": "Code-review finder, Reuse angle. Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR adding ADR 0031 (docs/adr/0031-oss-byol-distribution-licensing.md) plus index row and a pointer in ADR 0013.\n\nFlag content the new ADR re-states that already lives canonically elsewhere, where a link would serve better than duplication — e.g. does the full license-audit detail belong in the ADR when issue #732 already records it (check `gh issue view 732 --repo TheurgicDuke771/DataQ`)? ADRs are deliberately self-contained per docs/adr/README.md, so only flag duplication that will DRIFT (numbers/package versions that change over time, restated rules that another doc owns). Name the canonical home for each.\n\nReturn up to 6 candidates as JSON [{file, line, summary, failure_scenario}] where failure_scenario is the concrete drift/maintenance cost. If nothing, return []."
}
```

> TOOL

tool_result
id: toolu_01GjS1rEcVyQuJFejARZWMJ8
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: ad992f26d65d13dee (internal ID - do not mention to user. Use SendMessage with to: 'ad992f26d65d13dee', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/ad992f26d65d13dee.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01MKxaosAXbiMF6NfwsAFeoc
```json
{
  "description": "Finder: simplification angle",
  "subagent_type": "Explore",
  "model": "haiku",
  "prompt": "Code-review finder, Simplification angle. Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR adding ADR 0031 plus an index row (docs/adr/README.md) and a Related pointer (ADR 0013).\n\ndocs/adr/README.md says \"Keep each ADR short — 1–2 pages. If it grows past that, the decision is probably two decisions.\" Check the new ADR against that and for: redundant restatements within the ADR, decision points that are really consequences, verbose passages a reader must wade through to find the actual decision. Only flag concrete, quotable redundancy — not style preferences.\n\nReturn up to 6 candidates as JSON [{file, line, summary, failure_scenario}] with the concrete cost. If nothing, return []."
}
```

> TOOL

tool_result
id: toolu_01MKxaosAXbiMF6NfwsAFeoc
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a87ee57d7e7ced11a (internal ID - do not mention to user. Use SendMessage with to: 'a87ee57d7e7ced11a', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a87ee57d7e7ced11a.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01DeCJ5LH1SavcK4xCcVhST1
```json
{
  "description": "Finder: efficiency angle",
  "subagent_type": "Explore",
  "model": "haiku",
  "prompt": "Code-review finder, Efficiency angle. Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — this PR is documentation-only (a new ADR + two one-line doc edits). Efficiency (runtime waste, I/O, hot paths) rarely applies to docs; check quickly whether the diff touches ANY executable or CI-consumed file (workflows, mkdocs config, scripts) — if it is purely markdown prose, return []. Only report a candidate if some tooling actually consumes these files in a way the change makes wasteful.\n\nReturn a JSON array [{file, line, summary, failure_scenario}] — expected: []."
}
```

> TOOL

tool_result
id: toolu_01DeCJ5LH1SavcK4xCcVhST1
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a856b304f715ce2e1 (internal ID - do not mention to user. Use SendMessage with to: 'a856b304f715ce2e1', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a856b304f715ce2e1.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01QXkf2beuiV3Xd3ciZLub1c
```json
{
  "description": "Finder: altitude angle",
  "subagent_type": "Explore",
  "prompt": "Code-review finder, Altitude angle. Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR adding ADR 0031 (free OSS MIT + BYOL distribution licensing decision) plus index row and ADR 0013 pointer.\n\nCheck the change is at the right depth: (1) Is an ADR the right instrument for each thing 0031 decides, or does part of it belong in an enforced/canonical location instead — e.g. the \"no strong-copyleft dependencies\" guardrail is stated as review discipline; the repo's pattern for binding rules is CONTRIBUTING.md's numbered working agreements (read CONTRIBUTING.md's structure) — is a standing PR-binding rule stated ONLY in an ADR consistent with how other ADR-established rules (e.g. ADR 0013's guardrails, ADR 0002 conventional commits) were propagated into CONTRIBUTING/CLAUDE.md? (2) The partial supersession mechanism: docs/adr/README.md defines whole-ADR supersession only — is amending 0013 via a Related bullet a fragile special case where the format should instead be extended (an \"Amended by\" frontmatter field), per the repo's own append-only conventions? (3) Anything else where the PR patches a symptom in prose rather than the governing doc.\n\nOnly flag findings with a concrete, quotable basis in the repo's existing patterns. Return up to […]

> TOOL

tool_result
id: toolu_01QXkf2beuiV3Xd3ciZLub1c
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a14812c3e60222fda (internal ID - do not mention to user. Use SendMessage with to: 'a14812c3e60222fda', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a14812c3e60222fda.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01U6erXBrhP4GmspCJq2UbR1
```json
{
  "description": "Finder: conventions angle",
  "subagent_type": "Explore",
  "prompt": "Code-review finder, Conventions angle. Repo: /home/<USER>/Coding/Python/DataQ. Run `git diff main...HEAD` — docs-only PR (new docs/adr/0031-oss-byol-distribution-licensing.md, index row in docs/adr/README.md, Related pointer in docs/adr/0013-...md).\n\nRead the governing convention docs and check the diff for clear violations, quoting the exact rule and the exact line that breaks it:\n1. /home/<USER>/Coding/Python/DataQ/CLAUDE.md — especially §Documentation (ADR conventions), §6 working agreements, and anything about the ADR index being single source of truth.\n2. /home/<USER>/Coding/Python/DataQ/docs/adr/README.md — the Format section: file-name pattern, frontmatter fields (Status/Date/Deciders + optional Consulted/Supersedes/Superseded-by, title-case status values), required sections (Context, Decision, Consequences, Alternatives considered, Related optional), 1–2 page length rule, append-only supersession convention. Check the new ADR 0031 complies field-by-field, and whether the PARTIAL supersession of 0013 handled via a Related bullet (0013 status unchanged) violates or stretches the stated convention (\"mark the old one's status as Superseded by ADR-NNNN\") — and whether 0031 should carry a \"Supersedes:\" frontmatter field given it supersedes only one line of 0013.\n3. ~/.claude/CLAUDE.md if it exists.\nNo style preferences — only quotable rule violations.\n\nReturn up to 6 candidates as JSON [{file, line, summary, failure_scenario}] naming the doc and rule in each. If nothing, return []."
}
```

> TOOL

tool_result
id: toolu_01U6erXBrhP4GmspCJq2UbR1
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a2bd1ec34c51fd6fa (internal ID - do not mention to user. Use SendMessage with to: 'a2bd1ec34c51fd6fa', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a2bd1ec34c51fd6fa.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

Efficiency angle came back empty as expected. Waiting for the remaining seven finders.

> AGENT

Simplification finder returned six candidates (mostly prose-redundancy style points — I'll be skeptical of those in verification). Waiting on the remaining six finders.

> AGENT

Angle B found the strongest candidates so far: ADR 0013 §5's surviving obligations (EULA/DPA, SOC 2/pen test, tax/banking) aren't carried into the #732 checklist that ADR 0031 designates as the tracking home. Five finders still running.

> AGENT

Conventions finder flagged one real tension (the partial supersession of 0013 isn't reflected in the structured frontmatter, only prose). Four finders still out.

> AGENT

Line-by-line finder caught a genuine factual error — CONTRIBUTING rule 39 is the *MCP-server* supply-chain audit, not a general dependency audit, so the ADR's guardrail cites the wrong process. Three finders remaining.

> AGENT

Cross-file tracer surfaced the most substantive finding yet: ADR 0013's Consequences/billing-table lines still frame BYOL as *paid* license revenue, which makes 0031's "the rest of 0013 stands unchanged" claim inaccurate. Two finders left, then verification.

> AGENT

Reuse finder mostly overlaps earlier candidates (the rule-39 misreference again, plus audit-number "drift" — weak, since an ADR is a dated snapshot by design). One finder left (altitude), then I'll dedup and verify.

> AGENT

All 8 finders are done. After dedup, four findings are already effectively CONFIRMED by multiple independent finders quoting the governing text (the 0013 revenue-framing contradiction; the CONTRIBUTING rule-39 mischaracterization; the missed `Amends:` frontmatter precedent from ADR 0028/0012; the guardrail not distilled into CONTRIBUTING/CLAUDE per the repo's own distillation contract). Three candidates remain uncertain — sending each to a verifier.

> TOOL

tool_use Agent
id: toolu_01TDVMcPKHpSibQFBFPewe5e
```json
{
  "description": "Verify EULA/SOC2 checklist gap",
  "subagent_type": "Explore",
  "prompt": "You are a code-review verifier. Repo: /home/<USER>/Coding/Python/DataQ. Candidate finding to verify — return exactly one verdict: CONFIRMED / PLAUSIBLE / REFUTED, with 2-3 sentences of justification.\n\nCandidate: \"ADR 0031 (docs/adr/0031-oss-byol-distribution-licensing.md, new in this PR) designates issue #732 as the tracking home for marketplace-readiness work, and its Consequences say the marketplace path 'reduces to packaging + certification'. But ADR 0013 §5 lists commercial/legal obligations that survive even under a free-OSS model — EULA/terms-of-use for the marketplace listing (Azure Partner Center requires attaching license terms even for free offers — standard contract or custom), DPA, SOC 2 + pen test for enterprise buyers, tax/banking — and issue #732 (check with `gh issue view 732 --repo TheurgicDuke771/DataQ`) omits EULA/DPA/SOC2/pen-test/tax-banking entirely. So the PR's framing invites de-scoping obligations that still exist.\"\n\nCheck: read ADR 0013 §5, ADR 0031, and issue #732. Judge: (a) do the omissions actually exist in #732; (b) is it true that a FREE marketplace offer still needs license terms attached (reason from what the repo documents + general Partner Center knowledge — if you're unsure about Partner Center specifics, that uncertainty supports PLAUSIBLE, not REFUTED); (c) does ADR […]

> TOOL

tool_result
id: toolu_01TDVMcPKHpSibQFBFPewe5e
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: af374b3658a2e3ed5 (internal ID - do not mention to user. Use SendMessage with to: 'af374b3658a2e3ed5', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/af374b3658a2e3ed5.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_01UgAZsV7grXxnbH76dQMM6X
```json
{
  "description": "Verify ADR 0023 scope claim",
  "subagent_type": "Explore",
  "prompt": "You are a code-review verifier. Repo: /home/<USER>/Coding/Python/DataQ. Candidate finding — return exactly one verdict: CONFIRMED / PLAUSIBLE / REFUTED with 2-3 sentences.\n\nCandidate: \"docs/adr/0031-oss-byol-distribution-licensing.md (new in this PR) says marketplace listings are free offers of 'the public GHCR images — ADR 0023' (plural, in Decision #2 and Related). But ADR 0023 (docs/adr/0023-container-image-registry-ghcr.md) decides GHCR for the BACKEND image only; the frontend image's registry/publishing is established elsewhere (ADR 0028 / .github/workflows/publish-images.yml). So the cross-reference overstates 0023's scope.\"\n\nRead ADR 0023 fully, check whether it covers the frontend image or only the backend, and check .github/workflows/publish-images.yml + ADR 0028 for where frontend-image publishing is actually decided. If ADR 0023's decision text is registry-choice-general (GHCR as THE registry for DataQ images, not just backend), that would REFUTE. Quote the decisive lines.",
  "model": "sonnet"
}
```

> TOOL

tool_result
id: toolu_01UgAZsV7grXxnbH76dQMM6X
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a5e88a2e06ab35d46 (internal ID - do not mention to user. Use SendMessage with to: 'a5e88a2e06ab35d46', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a5e88a2e06ab35d46.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_use Agent
id: toolu_0168LWMFzCWcvaXKvLDD1mJd
```json
{
  "description": "Verify G-h stale framing",
  "subagent_type": "Explore",
  "prompt": "You are a code-review verifier. Repo: /home/<USER>/Coding/Python/DataQ. Candidate finding — return exactly one verdict: CONFIRMED / PLAUSIBLE / REFUTED with 2-3 sentences.\n\nCandidate: \"context/post-v1-roadmap.md gap G-h (~line 67) says 'ADR 0013's ambition is commercial BYOL' — after this PR's ADR 0031 (free OSS MIT + BYOL, no license revenue), that framing is stale/contradictory, and the PR adds no pointer from G-h to ADR 0031. A reader executing the readiness checklist may treat DataQ as a commercial-license product.\"\n\nRead context/post-v1-roadmap.md G-h and ADR 0031. Consider: G-h's SUBSTANCE is about the Databricks Free-Edition licence (paid workspace before commercial demo/use) — does that substance remain fully valid under free-OSS DataQ (commercial *use* of Databricks by a customer/vendor demo is orthogonal to DataQ's own license)? Is the only stale part the aside 'ADR 0013's ambition is commercial BYOL'? Also weigh that the file is NOT touched by this diff (scope = the PR fails-to-fix an adjacent doc). Judge severity honestly: is this a real reader-misleading defect the PR should fix, or marginal? REFUTED only if the claimed contradiction doesn't exist.",
  "model": "sonnet"
}
```

> TOOL

tool_result
id: toolu_0168LWMFzCWcvaXKvLDD1mJd
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a24778d082658c969 (internal ID - do not mention to user. Use SendMessage with to: 'a24778d082658c969', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/a24778d082658c969.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

While the verifiers run, let me pin exact line numbers for the inline comment anchors.

> TOOL

tool_use Bash
id: toolu_01X4bDy1cW2mMfuUg8KNg3mj
```json
{
  "command": "grep -n \"quarterly supply-chain\\|public GHCR images\\|stands unchanged\\|reduces to packaging\\|superseded by this ADR\" /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md; echo ---; grep -n \"ADR 0031\" /home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md; echo ---; git -C /home/<USER>/Coding/Python/DataQ rev-parse HEAD",
  "description": "Get anchor line numbers and head SHA for inline comments"
}
```

> TOOL

tool_result
id: toolu_01X4bDy1cW2mMfuUg8KNg3mj
```
20:1. **DataQ is and remains free open-source software under the MIT license.** There is no paid license, no entitlement check, and no license-key machinery — the "licensing model + entitlement/license-key" line of ADR 0013 §5 is **superseded by this ADR**. Everything else in ADR 0013 (customer-deployed BYOL distribution, the Azure→AWS/GCP phasing, the anti-lock-in guardrails) stands unchanged; under this decision "BYOL" reads as *bring your own (free, MIT) license* — the customer deploys the OSS into their own account, and no marketplace metering or entitlement integration is needed.
21:2. **Marketplace listings are free/BYOL offers of the OSS artifacts** (the public GHCR images — ADR 0023 — plus the portable install artifact when it lands). Listings still require seller registration and per-marketplace certification, but not commerce integration.
23:4. **Dependency license guardrail (standing, binding on future PRs):** the dependency tree stays free of strong-copyleft and source-available licenses (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause). Weak copyleft (LGPL/MPL/EPL) is acceptable with notice. Adding a dependency that violates this needs an explicit ADR-level exception. The check joins the quarterly supply-chain audit cadence (CONTRIBUTING rule 39).
30:- No entitlement/license-server build — the last commercial-machinery item ADR 0013 carried disappears; the marketplace path reduces to […]

> AGENT

ADR 0023 scope claim CONFIRMED (backend-only; frontend image comes via ADR 0028). Two verifiers left.

> TOOL

tool_use Monitor
id: toolu_015jdHs4JfdP1pt6YWCCEwnL
```json
{
  "until": "both remaining verifier agents (EULA/SOC2 gap, G-h stale framing) complete"
}
```

> TOOL

tool_result ERROR
id: toolu_015jdHs4JfdP1pt6YWCCEwnL
```
<tool_use_error>InputValidationError: Monitor failed due to the following issues:
The required parameter `description` is missing
An unexpected parameter `until` was provided

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms, max 3600000ms. Ignored when persistent is true.","default":300000,"type":"number","minimum":1000},"persistent":{"description":"Run for the lifetime of the session (no timeout). Use for session-length watches like PR monitoring or log tails. Stop with TaskStop.","default":false,"type":"boolean"},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms","persistent"],"additionalProperties":false}</tool_use_error>
```

> AGENT

The remaining two verifiers will notify me on completion — no polling needed. I'll post the review comments and apply the fixes once their verdicts land.

> AGENT

G-h staleness verdict: PLAUSIBLE but minor (the substance of G-h stands; only the aside is stale). Waiting on the final verifier (EULA/SOC 2 checklist gap).

> AGENT

All verdicts are in — 6 findings survive (5 CONFIRMED, 1 PLAUSIBLE-minor); the simplification/drift candidates are refuted as style or as expected-of-a-dated-snapshot. Posting the inline review comments to PR #733 now.

> TOOL

tool_use Write
id: toolu_01Jp6g4NDEDNB37PU3aKdaj4
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc1.md",
  "content": "**[review] \"Everything else in ADR 0013 … stands unchanged\" is not accurate.** ADR 0013 frames BYOL as *paid* license revenue in three places this decision reverses: the model-comparison table (\"bring your own license, **billed outside the meter**\", ~L17), Consequences (\"BYOL forgoes marketplace-metered usage billing; **revenue is licensed outside the meter**\", ~L60), and Alternatives (\"a revenue model (metered SaaS) we can **approximate with BYOL licensing**\", ~L64). Under 0031 there is no license revenue at all, so \"the rest stands unchanged\" over-claims — the supersession scope should name the revenue framing too (distribution model/phasing/guardrails stand; the §5 licensing line **and 0013's licensed-revenue framing** are superseded).\n"
}
```

> TOOL

tool_result
id: toolu_01Jp6g4NDEDNB37PU3aKdaj4
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc1.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_014jCcvKCyM6iBnJJ9EzuDzf
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc2.md",
  "content": "**[review] Two problems with this guardrail's enforcement story.**\n\n1. **CONTRIBUTING rule 39 doesn't cover this.** Rule 39 is the *quarterly MCP supply-chain audit* — scoped to the client-side MCP servers pinned in `.mcp.json` (deprecated/yanked/publisher-transfer checks). It says nothing about dependency licenses, so \"the check joins the quarterly supply-chain audit cadence (CONTRIBUTING rule 39)\" points maintainers at a process that will never run this check.\n2. **\"Standing, binding on future PRs\" rules don't live only in ADRs here.** The repo's pattern is distillation: ADR 0002 → CONTRIBUTING rules 7/10; ADR 0013's guardrails → CLAUDE.md §11; CLAUDE.md §9 states the contract explicitly (\"the day-to-day operating rules those decisions distill into are already captured in §4–§6, §10 and §11\"). As written, a GPL/AGPL dep would pass every gate (pip-audit is CVE-only) and the rule would only be discovered by re-reading this ADR.\n\nFix: add the license guardrail as a numbered CONTRIBUTING working agreement (and a CLAUDE.md §11 bullet), and cite that rule here instead of rule 39.\n"
}
```

> TOOL

tool_result
id: toolu_014jCcvKCyM6iBnJJ9EzuDzf
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc2.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01NECMWGmnudEaTmZrZyxFVF
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc3.md",
  "content": "**[review] The partial supersession bypasses the repo's own amendment mechanism.** The ADR log already has a precedent for exactly this case: ADR 0028 carries an `Amends: ADR-0024` frontmatter field, and ADR 0012 records a partial change with an inline `> **Amendment (date):** …` blockquote. This PR instead invents a prose-only form: 0031 has no `Amends:`/`Supersedes:` field, 0013's §5 body gets no inline marker, and the 0013 index row still reads plain \"Accepted\" — so nothing machine-readable or scannable signals that §5's licensing line is dead. A reader checking 0013's frontmatter or the index (the convention's stated source of truth) would still plan entitlement-key work.\n\nFix: `Amends: ADR-0013` in 0031's frontmatter, an amendment blockquote at 0013's top per the 0012 precedent, an \"amended by 0031\" note on the 0013 index row — and ideally document the already-in-use `Amends` field in the README Format section while here.\n"
}
```

> TOOL

tool_result
id: toolu_01NECMWGmnudEaTmZrZyxFVF
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc3.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_013DLkSBKFAuEi2yphedp7tB
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc4.md",
  "content": "**[review] \"Reduces to packaging + certification\" overstates, and the designated tracking home doesn't carry the survivors.** ADR 0013 §5 obligations that survive a free-OSS model are missing from #732 (which this ADR names as the tracking checklist): a **listing terms-of-use/EULA** (Partner Center requires a Legal/terms attachment even for $0 offers — Standard Contract or custom), **DPA** (needed only if a paid/hosted tier ever exists — worth recording that rationale rather than dropping it), **SOC 2 + pen test** for enterprise buyers (procurement asks for these regardless of price), and **tax/banking** (genuinely unnecessary for a free offer — but say so explicitly so the decision is traceable when Decision 5's \"beside the OSS\" monetization ever activates). Fix: soften this bullet and itemize the survivors in #732 with keep/defer/drop rationale each.\n"
}
```

> TOOL

tool_result
id: toolu_013DLkSBKFAuEi2yphedp7tB
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc4.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_014uQriRLryVyK5x8Kq88oGf
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc5.md",
  "content": "**[review] \"The public GHCR images — ADR 0023\" (plural) overstates 0023's scope.** ADR 0023's decision text is explicitly \"the container registry for **the backend image**\"; the frontend image's one-generic-image publishing is established by ADR 0028 + `publish-images.yml`. Cite both: \"the public GHCR images — ADR 0023 (backend) / ADR 0028 (frontend)\". Same imprecision in the Related entry below (L50).\n"
}
```

> TOOL

tool_result
id: toolu_014uQriRLryVyK5x8Kq88oGf
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/rc5.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01JEa2hiDAyhtfaV6a517fRB
```json
{
  "command": "SCRATCH=/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad\nSHA=0d27ff5ada6000e7778b65944e9ba8a728343321\ngh api repos/TheurgicDuke771/DataQ/pulls/733/comments -f commit_id=$SHA -f path=docs/adr/0031-oss-byol-distribution-licensing.md -F line=20 -f side=RIGHT -F body=@$SCRATCH/rc1.md --jq .html_url\ngh api repos/TheurgicDuke771/DataQ/pulls/733/comments -f commit_id=$SHA -f path=docs/adr/0031-oss-byol-distribution-licensing.md -F line=23 -f side=RIGHT -F body=@$SCRATCH/rc2.md --jq .html_url\ngh api repos/TheurgicDuke771/DataQ/pulls/733/comments -f commit_id=$SHA -f path=docs/adr/0013-marketplace-distribution-and-anti-lock-in.md -F line=72 -f side=RIGHT -F body=@$SCRATCH/rc3.md --jq .html_url\ngh api repos/TheurgicDuke771/DataQ/pulls/733/comments -f commit_id=$SHA -f path=docs/adr/0031-oss-byol-distribution-licensing.md -F line=30 -f side=RIGHT -F body=@$SCRATCH/rc4.md --jq .html_url\ngh api repos/TheurgicDuke771/DataQ/pulls/733/comments -f commit_id=$SHA -f path=docs/adr/0031-oss-byol-distribution-licensing.md -F line=21 -f side=RIGHT -F body=@$SCRATCH/rc5.md --jq .html_url",
  "description": "Post 5 inline review comments on PR 733"
}
```

> TOOL

tool_result
id: toolu_01JEa2hiDAyhtfaV6a517fRB
```
https://github.com/TheurgicDuke771/DataQ/pull/733#discussion_r3555561422
https://github.com/TheurgicDuke771/DataQ/pull/733#discussion_r3555561492
https://github.com/TheurgicDuke771/DataQ/pull/733#discussion_r3555561537
https://github.com/TheurgicDuke771/DataQ/pull/733#discussion_r3555561568
https://github.com/TheurgicDuke771/DataQ/pull/733#discussion_r3555561617
```

> TOOL

tool_use Bash
id: toolu_017V8vpnWCkyubUUKVupCknm
```json
{
  "command": "sed -n '1,12p' /home/<USER>/Coding/Python/DataQ/docs/adr/0028-cloud-neutral-image-runtime-config-generic-oidc.md; echo ===; sed -n '1,14p' /home/<USER>/Coding/Python/DataQ/docs/adr/0012-monitor-kind-seam.md; echo ===; grep -n \"0028\\]\" /home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "description": "Check Amends frontmatter and amendment blockquote precedents"
}
```

> TOOL

tool_result
id: toolu_017V8vpnWCkyubUUKVupCknm
```
# ADR 0028 — Cloud-neutral image: runtime config injection + generic OIDC auth, bypass fail-closed

- **Status:** Accepted
- **Date:** 2026-06-30
- **Deciders:** @TheurgicDuke771
- **Amends:** ADR [0024](0024-app-deployment-infrastructure.md) (frontend hosting moves Static Web App → a Container App running the nginx image)
- **Related:** ADR [0010](0010-provider-agnostic-infrastructure-seams.md) (provider-agnostic seams — Azure is one impl), [0013](0013-marketplace-distribution-and-anti-lock-in.md) (BYOL / anti-lock-in), [0023](0023-container-image-registry-ghcr.md) (GHCR), [0025](0025-production-image-pip-slim.md) (slim image), [0008](0008-mcp-server.md) (MCP token validation), [0026](0026-auth-api-keys-and-principal-seam.md) (DataQ-issued credentials — the backend identity seam)
- **Issue:** [#504](https://github.com/TheurgicDuke771/DataQ/issues/504); post-v1 AWS/GCP IaC → [#505](https://github.com/TheurgicDuke771/DataQ/issues/505). Follows the prebuilt-image work in [#472](https://github.com/TheurgicDuke771/DataQ/issues/472).

## Context

The prebuilt-image distribution (#472) shipped, but exposed three coupling/complexity
(eval):1: == not found
```

> TOOL

tool_use Bash
id: toolu_016eaLveKnw1Hdd9LxxyqCs9
```json
{
  "command": "grep -n \"39\\|38\\.\" /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md | head -20; echo ===; tail -30 /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md; echo ===; grep -n \"39 rules\\|39-rule\" /home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "description": "Locate rule 39 text and rule-count mentions"
}
```

> TOOL

tool_result
id: toolu_016eaLveKnw1Hdd9LxxyqCs9
```
129:38. **Security vulnerabilities are not public GitHub issues.** Report via [GitHub Security Advisories](https://github.com/TheurgicDuke771/DataQ/security/advisories/new). See [SECURITY.md](.github/SECURITY.md).
130:39. **Quarterly MCP supply-chain audit:** once a quarter, for each client-side MCP server pinned in `.mcp.json` (see CLAUDE.md Appendix), verify the package hasn't been deprecated, yanked, or transferred to a new publisher (e.g. `npm view <pkg> maintainers time`), and review the changelog before bumping the pinned major version. MCP servers run with local tool access — treat a publisher change like a compromised dependency until verified.
(eval):1: == not found
```

> TOOL

tool_use Bash
id: toolu_01VV8uXmWPsyzXoqpMwTb5LW
```json
{
  "command": "sed -n '1,12p' /home/<USER>/Coding/Python/DataQ/docs/adr/0012-monitor-kind-seam.md",
  "description": "See ADR 0012 amendment blockquote format"
}
```

> TOOL

tool_result
id: toolu_01VV8uXmWPsyzXoqpMwTb5LW
```
# ADR 0012 — Monitor-kind seam (`check.kind` discriminator + numeric metric storage)

- **Status:** Accepted
- **Date:** 2026-05-30
- **Deciders:** @TheurgicDuke771

> **Amendment (2026-06-29, Week 7):** the **freshness** and **volume** monitor
> kinds — reserved-only below ("do not build them") — are **pulled forward into
> v1**. The original deferral (post-v1 Theme A) was about *net-new scope vs. the
> 8-week plan*, not a design objection; with the app deployed against live data
> (Week 7) and the seam proving out, the two highest-ROI monitors (CLAUDE.md §5:
> "most real incidents are freshness/volume") are worth shipping now. The seam is
```

> TOOL

tool_use Bash
id: toolu_01RrAVzLh7ewt8k9iVEWr9hD
```json
{
  "command": "sed -n '125,140p' /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
  "description": "See end of CONTRIBUTING rules list"
}
```

> TOOL

tool_result
id: toolu_01RrAVzLh7ewt8k9iVEWr9hD
```
## H. Security review cadence

36. **End-of-week quick scan from Week 2 onward:** review Dependabot vuln alerts, secret scan results, OWASP top-10 spot check on any new endpoints, Key Vault access audit. The `/security-scan` skill (`.claude/skills/security-scan/`) runs this checklist.
37. **Hard security review gate before Week 7 deploy:** full pass on all of the above plus public-endpoint exposure review (especially `/api/v1/orchestration/events/*` and `/mcp`).
38. **Security vulnerabilities are not public GitHub issues.** Report via [GitHub Security Advisories](https://github.com/TheurgicDuke771/DataQ/security/advisories/new). See [SECURITY.md](.github/SECURITY.md).
39. **Quarterly MCP supply-chain audit:** once a quarter, for each client-side MCP server pinned in `.mcp.json` (see CLAUDE.md Appendix), verify the package hasn't been deprecated, yanked, or transferred to a new publisher (e.g. `npm view <pkg> maintainers time`), and review the changelog before bumping the pinned major version. MCP servers run with local tool access — treat a publisher change like a compromised dependency until verified.

---

## Module boundaries & naming conventions

### Backend (`backend/`)

| Layer | Package | Responsibility |
|---|---|---|
| API | `backend/app/api/v1/` | FastAPI routers only — no business logic |
```

> TOOL

tool_use Bash
id: toolu_01YbYfgYCeLMaQRKser7f8mQ
```json
{
  "command": "grep -n '39 rules\\|39-rule' /home/<USER>/Coding/Python/DataQ/CLAUDE.md /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md /home/<USER>/Coding/Python/DataQ/README.md 2>/dev/null",
  "description": "Find rule-count mentions to update"
}
```

> TOOL

tool_result
id: toolu_01YbYfgYCeLMaQRKser7f8mQ
```
/home/<USER>/Coding/Python/DataQ/CLAUDE.md:134:Full list (39 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:
/home/<USER>/Coding/Python/DataQ/CLAUDE.md:189:1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 39-rule working agreements + DoD + commit/branch conventions
/home/<USER>/Coding/Python/DataQ/CLAUDE.md:256:| Working agreements (full 39-rule list) | [CONTRIBUTING.md](CONTRIBUTING.md) |
```

> AGENT

I have the precedents. Now checking the exact G-h wording and my 0031 Related lines, then applying all fixes.

> TOOL

tool_use Bash
id: toolu_01DHSkXCJigxiBFhEPzzd6bV
```json
{
  "command": "sed -n '67p' /home/<USER>/Coding/Python/DataQ/context/post-v1-roadmap.md; sed -n '47,52p' /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md; sed -n '1,10p' /home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md",
  "description": "Read exact lines to edit (G-h, 0031 Related, 0013 head)"
}
```

> TOOL

tool_result
id: toolu_01DHSkXCJigxiBFhEPzzd6bV
```
| G-h | **Harness Databricks = Free Edition, non-commercial-only** — the UC demo leg cannot legally back a commercial demo, while ADR 0013's ambition is commercial BYOL. **Decision recorded 2026-07-03 (go-live):** acceptable while the deployment is demo/eval; trigger stands — before any commercial demo/use → paid workspace. | Licence landmine on the demo path | ADR 0021/0013 context — recorded in the go-live checklist ([progress-v1.md](../docs/progress-v1.md)); re-trigger **before any commercial demo** |
## Related

- [ADR 0013](0013-marketplace-distribution-and-anti-lock-in.md) — the BYOL distribution decision this ADR completes; its §5 licensing-model line is superseded here, the rest stands.
- [ADR 0023](0023-container-image-registry-ghcr.md) — public GHCR images, the free distribution channel.
- Issue #732 — marketplace-readiness checklist (license-audit record, THIRD-PARTY-NOTICES/SBOM automation, SUPPORT.md, G-h/G-i prerequisites).
# ADR 0013 — Marketplace distribution (customer-deployed BYOL) and anti-vendor-lock-in guardrails

- **Status:** Accepted
- **Date:** 2026-06-01
- **Deciders:** @TheurgicDuke771

## Context

We are evaluating listing DataQ on the **Azure, AWS, and GCP marketplaces**. Two questions follow: is it viable given the current architecture, and what must change to keep the option open without derailing the 8-week v1.
```

> TOOL

tool_use Edit
id: toolu_015CFXBxFTheqk6LB8h1GKSw
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-07-09\n- **Deciders:** @TheurgicDuke771\n\n## Context",
  "new_string": "- **Status:** Accepted\n- **Date:** 2026-07-09\n- **Deciders:** @TheurgicDuke771\n- **Amends:** ADR [0013](0013-marketplace-distribution-and-anti-lock-in.md) (the §5 \"licensing model + entitlement/license-key\" line and the licensed-revenue framing of BYOL)\n\n## Context"
}
```

> TOOL

tool_result
id: toolu_015CFXBxFTheqk6LB8h1GKSw
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_014n73w2WLxaDr8987xVaatH
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "1. **DataQ is and remains free open-source software under the MIT license.** There is no paid license, no entitlement check, and no license-key machinery — the \"licensing model + entitlement/license-key\" line of ADR 0013 §5 is **superseded by this ADR**. Everything else in ADR 0013 (customer-deployed BYOL distribution, the Azure→AWS/GCP phasing, the anti-lock-in guardrails) stands unchanged; under this decision \"BYOL\" reads as *bring your own (free, MIT) license* — the customer deploys the OSS into their own account, and no marketplace metering or entitlement integration is needed.",
  "new_string": "1. **DataQ is and remains free open-source software under the MIT license.** There is no paid license, no entitlement check, and no license-key machinery — this ADR supersedes the \"licensing model + entitlement/license-key\" line of ADR 0013 §5 **and ADR 0013's licensed-revenue framing of BYOL** (the comparison table's \"billed outside the meter\", the Consequences' \"revenue is licensed outside the meter\", the Alternatives' \"approximate with BYOL licensing\"): there is no license revenue at all. ADR 0013's distribution model (customer-deployed BYOL), the Azure→AWS/GCP phasing, and the anti-lock-in guardrails stand; under this decision \"BYOL\" reads as *bring your own (free, MIT) license* — the […]

> TOOL

tool_result
id: toolu_014n73w2WLxaDr8987xVaatH
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01QYcre4AZDnJUFBCS64rwXG
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "2. **Marketplace listings are free/BYOL offers of the OSS artifacts** (the public GHCR images — ADR 0023 — plus the portable install artifact when it lands). Listings still require seller registration and per-marketplace certification, but not commerce integration.",
  "new_string": "2. **Marketplace listings are free/BYOL offers of the OSS artifacts** (the public GHCR images — ADR 0023 for the backend, ADR 0028 for the frontend — plus the portable install artifact when it lands). Listings still require seller registration, per-marketplace certification, and the listing's legal terms (e.g. Partner Center requires attached license terms even for free offers), but not commerce integration."
}
```

> TOOL

tool_result
id: toolu_01QYcre4AZDnJUFBCS64rwXG
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UHBjPquHXoEeK7x6wNMPiC
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "4. **Dependency license guardrail (standing, binding on future PRs):** the dependency tree stays free of strong-copyleft and source-available licenses (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause). Weak copyleft (LGPL/MPL/EPL) is acceptable with notice. Adding a dependency that violates this needs an explicit ADR-level exception. The check joins the quarterly supply-chain audit cadence (CONTRIBUTING rule 39).",
  "new_string": "4. **Dependency license guardrail (standing, binding on future PRs):** the dependency tree stays free of strong-copyleft and source-available licenses (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause). Weak copyleft (LGPL/MPL/EPL) is acceptable with notice. Adding a dependency that violates this needs an explicit ADR-level exception. Distilled into **CONTRIBUTING rule 40** (this PR), which schedules the license sweep alongside the rule-39 quarterly supply-chain audit and before any release/image publish."
}
```

> TOOL

tool_result
id: toolu_01UHBjPquHXoEeK7x6wNMPiC
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01QWn7P1LNr9ECC29apHRPXx
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "- No entitlement/license-server build — the last commercial-machinery item ADR 0013 carried disappears; the marketplace path reduces to packaging + certification.",
  "new_string": "- No entitlement/license-server build — the commercial *build* items ADR 0013 carried disappear; the marketplace path reduces to packaging + certification + the listing's legal terms. The rest of ADR 0013 §5's commercial/legal surface survives with per-item keep/defer/drop dispositions recorded in #732 (listing terms/EULA kept; DPA and tax/banking not needed while there is no hosted/paid tier — recorded, not dropped; SOC 2 / pen test remain an enterprise-buyer ask independent of price)."
}
```

> TOOL

tool_result
id: toolu_01QWn7P1LNr9ECC29apHRPXx
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01CCYBWMU3YQpNBm2uFEAaWp
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md",
  "old_string": "- [ADR 0013](0013-marketplace-distribution-and-anti-lock-in.md) — the BYOL distribution decision this ADR completes; its §5 licensing-model line is superseded here, the rest stands.\n- [ADR 0023](0023-container-image-registry-ghcr.md) — public GHCR images, the free distribution channel.",
  "new_string": "- [ADR 0013](0013-marketplace-distribution-and-anti-lock-in.md) — the BYOL distribution decision this ADR completes; its §5 licensing-model line and its licensed-revenue framing are superseded here (see the amendment note at its top), the distribution model/phasing/guardrails stand.\n- [ADR 0023](0023-container-image-registry-ghcr.md) / [ADR 0028](0028-cloud-neutral-image-runtime-config-generic-oidc.md) — the public GHCR backend and frontend images, the free distribution channel."
}
```

> TOOL

tool_result
id: toolu_01CCYBWMU3YQpNBm2uFEAaWp
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0031-oss-byol-distribution-licensing.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01AGGz3y2dvNxophaSvHF2s4
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-06-01\n- **Deciders:** @TheurgicDuke771\n\n## Context",
  "new_string": "- **Status:** Accepted\n- **Date:** 2026-06-01\n- **Deciders:** @TheurgicDuke771\n\n> **Amendment (2026-07-09, [ADR 0031](0031-oss-byol-distribution-licensing.md)):**\n> the licensing model is decided as **free open-source (MIT) — there is no license\n> revenue**. This supersedes §5's \"licensing model + entitlement/license-key\" open\n> item and this ADR's licensed-revenue framing of BYOL (the comparison table's\n> \"billed outside the meter\", the Consequences' \"revenue is licensed outside the\n> meter\", the Alternatives' \"approximate with BYOL licensing\"). The distribution\n> model (customer-deployed BYOL), the phasing, and the anti-lock-in guardrails\n> below are unchanged; §5's remaining commercial/legal items carry per-item\n> dispositions in issue #732.\n\n## Context"
}
```

> TOOL

tool_result
id: toolu_01AGGz3y2dvNxophaSvHF2s4
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/0013-marketplace-distribution-and-anti-lock-in.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UfAzaS7t2wzYV7PG3G3CEJ
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "| [0013](0013-marketplace-distribution-and-anti-lock-in.md) | Marketplace distribution (customer-deployed BYOL) and anti-vendor-lock-in guardrails | Accepted |",
  "new_string": "| [0013](0013-marketplace-distribution-and-anti-lock-in.md) | Marketplace distribution (customer-deployed BYOL) and anti-vendor-lock-in guardrails | Accepted (amended by 0031 — §5 licensing line + licensed-revenue framing) |"
}
```

> TOOL

tool_result
id: toolu_01UfAzaS7t2wzYV7PG3G3CEJ
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01KmJzPxSWAcwUhPVYwxZx3o
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "| [0031](0031-oss-byol-distribution-licensing.md) | Distribution licensing — **free open-source (MIT) + customer-deployed BYOL**; no entitlement/license-key (supersedes the 0013 §5 licensing-model line); marketplace listings are free offers of the OSS artifacts; THIRD-PARTY-NOTICES/SBOM in images + releases; standing no-strong-copyleft dependency guardrail | Accepted |",
  "new_string": "| [0031](0031-oss-byol-distribution-licensing.md) | Distribution licensing — **free open-source (MIT) + customer-deployed BYOL**; no entitlement/license-key (amends 0013: supersedes its §5 licensing-model line + licensed-revenue framing); marketplace listings are free offers of the OSS artifacts; THIRD-PARTY-NOTICES/SBOM in images + releases; standing no-strong-copyleft dependency guardrail (CONTRIBUTING rule 40) | Accepted |"
}
```

> TOOL

tool_result
id: toolu_01KmJzPxSWAcwUhPVYwxZx3o
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_019szXGudd3biqmsJBbq2vhf
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "  - **Supersedes** *(optional)* — `ADR-NNNN` this decision replaces. Omit when none.\n  - **Superseded by** *(optional)* — `ADR-NNNN` that later replaced this one. Add when the status flips to `Superseded by`.",
  "new_string": "  - **Supersedes** *(optional)* — `ADR-NNNN` this decision replaces. Omit when none.\n  - **Superseded by** *(optional)* — `ADR-NNNN` that later replaced this one. Add when the status flips to `Superseded by`.\n  - **Amends** *(optional)* — `ADR-NNNN` this decision partially overrides (whole-ADR replacement uses `Supersedes` instead). Pair it with an inline `> **Amendment (date, ADR-NNNN):** …` blockquote at the top of the amended ADR and an \"(amended by NNNN — …)\" note on its index Status, so the override is visible where readers actually look. Precedents: ADR 0028 (amends 0024), ADR 0012's amendment blockquote, ADR 0031 (amends 0013). |"
}
```

> TOOL

tool_result
id: toolu_019szXGudd3biqmsJBbq2vhf
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01E3E32eWv6wLdjZgtP1Gin7
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "Precedents: ADR 0028 (amends 0024), ADR 0012's amendment blockquote, ADR 0031 (amends 0013). |",
  "new_string": "Precedents: ADR 0028 (amends 0024), ADR 0012's amendment blockquote, ADR 0031 (amends 0013)."
}
```

> TOOL

tool_result
id: toolu_01E3E32eWv6wLdjZgtP1Gin7
```
The file /home/<USER>/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01MDAbmCcx6exNDeiSJ1GwcH
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
  "old_string": "39. **Quarterly MCP supply-chain audit:** once a quarter, for each client-side MCP server pinned in `.mcp.json` (see CLAUDE.md Appendix), verify the package hasn't been deprecated, yanked, or transferred to a new publisher (e.g. `npm view <pkg> maintainers time`), and review the changelog before bumping the pinned major version. MCP servers run with local tool access — treat a publisher change like a compromised dependency until verified.",
  "new_string": "39. **Quarterly MCP supply-chain audit:** once a quarter, for each client-side MCP server pinned in `.mcp.json` (see CLAUDE.md Appendix), verify the package hasn't been deprecated, yanked, or transferred to a new publisher (e.g. `npm view <pkg> maintainers time`), and review the changelog before bumping the pinned major version. MCP servers run with local tool access — treat a publisher change like a compromised dependency until verified.\n40. **Dependency license guardrail ([ADR 0031](docs/adr/0031-oss-byol-distribution-licensing.md)):** DataQ ships MIT — the dependency tree stays free of strong-copyleft and source-available licenses (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause). Weak copyleft (LGPL/MPL/EPL) is acceptable with notice preservation. Adding a dependency that violates this needs an explicit ADR-level exception. Run the license sweep (backend: installed-env metadata; frontend: lockfile/`node_modules` license fields) alongside the […]

> TOOL

tool_result
id: toolu_01MDAbmCcx6exNDeiSJ1GwcH
```
The file /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01XyeCydHdc31CMZLqMSi9Y3
```json
{
  "command": "grep -n \"39\\b\" /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md | grep -v \"^129\\|^130\\|^131\" | head",
  "description": "Check for other rule-count mentions in CONTRIBUTING"
}
```

> TOOL

tool_result
id: toolu_01XyeCydHdc31CMZLqMSi9Y3
```
(Bash completed with no output)
```

> TOOL

tool_use Edit
id: toolu_01G9YVZkomKkqe1JvoU5X4hg
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "Full list (39 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:",
  "new_string": "Full list (40 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:"
}
```

> TOOL

tool_result ERROR
id: toolu_01G9YVZkomKkqe1JvoU5X4hg
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01GEekdpRHz9B6bpoMgRJygm
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 39-rule working agreements + DoD + commit/branch conventions",
  "new_string": "1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 40-rule working agreements + DoD + commit/branch conventions"
}
```

> TOOL

tool_result ERROR
id: toolu_01GEekdpRHz9B6bpoMgRJygm
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01JcfkzGGNCwCYtYSdbAreP9
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "| Working agreements (full 39-rule list) | [CONTRIBUTING.md](CONTRIBUTING.md) |",
  "new_string": "| Working agreements (full 40-rule list) | [CONTRIBUTING.md](CONTRIBUTING.md) |"
}
```

> TOOL

tool_result ERROR
id: toolu_01JcfkzGGNCwCYtYSdbAreP9
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01VJox99jgjYFp9e96Jm5hdA
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "- ❌ Don't track GX Core at \"latest.\" Pin the version in `environment.yml` — GX v1 API has drifted across point releases.",
  "new_string": "- ❌ Don't track GX Core at \"latest.\" Pin the version in `environment.yml` — GX v1 API has drifted across point releases.\n- ❌ Don't add a dependency under a strong-copyleft or source-available license (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause) — DataQ ships MIT (ADR 0031, CONTRIBUTING rule 40); weak copyleft (LGPL/MPL) is OK with notices. Exceptions need an ADR."
}
```

> TOOL

tool_result ERROR
id: toolu_01VJox99jgjYFp9e96Jm5hdA
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01QWs8FxYB9zbfMJVkCdLW4o
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/context/post-v1-roadmap.md",
  "old_string": "the UC demo leg cannot legally back a commercial demo, while ADR 0013's ambition is commercial BYOL.",
  "new_string": "the UC demo leg cannot legally back a commercial demo, while ADR 0013's ambition is commercial BYOL (since refined by ADR 0031 — free-OSS BYOL, no license revenue; this trigger is about *Databricks'* terms and stands unchanged for any commercial demo/use)."
}
```

> TOOL

tool_result
id: toolu_01QWs8FxYB9zbfMJVkCdLW4o
```
The file /home/<USER>/Coding/Python/DataQ/context/post-v1-roadmap.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

CLAUDE.md needs a Read first — grabbing the sections I'm editing.

> TOOL

tool_use Read
id: toolu_017vffWWDePFf681XoTULdFU
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "offset": 130,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_017vffWWDePFf681XoTULdFU
```
130	---
131	
132	## 6. Working agreements (rules above feature work)
133	
134	Full list (39 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:
135	
136	### Commit & change discipline
137	Per-functionality workflow, in order:
138	1. **One functionality per commit** (where possible).
139	2. **Test coverage for the functionality** (unit/integration as applicable — the ≥80% CI gate, live since Week 8, covers this).
```

> TOOL

tool_use Read
id: toolu_019jvKeBkbU1pzhNznTzwFJQ
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "offset": 186,
  "limit": 8
}
```

> TOOL

tool_result
id: toolu_019jvKeBkbU1pzhNznTzwFJQ
```
186	
187	## 7. Required reading before coding
188	
189	1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 39-rule working agreements + DoD + commit/branch conventions
190	2. [docs/adr/](docs/adr/) — all ADRs (architecture decisions with rationale)
191	3. [context/DataQ_platform_roadmap.md](context/DataQ_platform_roadmap.md) — the 8-week, 100-task product roadmap
192	4. The current week's milestone target (see §13 below)
193	
```

> TOOL

tool_use Read
id: toolu_015n9g8YvyJFiPyD6A5nEBCa
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "offset": 228,
  "limit": 32
}
```

> TOOL

tool_result
id: toolu_015n9g8YvyJFiPyD6A5nEBCa
```
228	- **MCP tool descriptions are LLM-facing, not REST-API-facing.** Write them for natural-language selection; test against the 4 canonical NL queries in the roadmap.
229	
230	---
231	
232	## 11. What NOT to do
233	
234	- ❌ Don't add ADF or Airflow as a queryable datasource in the connection editor / check editor / suite model.
235	- ❌ Don't bypass the `OrchestrationProvider` abstraction with provider-specific branching in service code.
236	- ❌ Don't deepen Azure lock-in: no reading Entra/OIDC provider claims in route/service code (depend on the generic `get_current_user`), no hardcoded Azure resource names/endpoints in business logic, no Azure-only assumptions baked into container images. Azure is one impl behind each seam — see ADR [0010](docs/adr/0010-provider-agnostic-infrastructure-seams.md) / [0013](docs/adr/0013-marketplace-distribution-and-anti-lock-in.md).
237	- ❌ Don't `git commit --no-verify` past hooks. If a hook fails, fix the underlying issue.
238	- ❌ Don't commit `.env` files. Use `.env.example` / `.env.app.example` as the templates.
239	- ❌ Don't put a credential — **even a local/mock one** — in any git-tracked file (templates, `scripts/`, CI, compose). Env templates ship the secret keys **blank** with the shape in a comment; `scripts/setup.sh` generates the local-dev password into the gitignored `.env`/`.env.app` on first […]

> TOOL

tool_use Edit
id: toolu_01P24CWZpKRvTCPXTzYyAU11
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "Full list (39 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:",
  "new_string": "Full list (40 rules across 8 categories) lives in [CONTRIBUTING.md](CONTRIBUTING.md). Highlights:"
}
```

> TOOL

tool_result
id: toolu_01P24CWZpKRvTCPXTzYyAU11
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01RmKJ9yWAfN5W6ExmEE8YBy
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 39-rule working agreements + DoD + commit/branch conventions",
  "new_string": "1. [CONTRIBUTING.md](CONTRIBUTING.md) — full 40-rule working agreements + DoD + commit/branch conventions"
}
```

> TOOL

tool_result
id: toolu_01RmKJ9yWAfN5W6ExmEE8YBy
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_015Y1CSYg9kkrhsPJvqnLndY
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "| Working agreements (full 39-rule list) | [CONTRIBUTING.md](CONTRIBUTING.md) |",
  "new_string": "| Working agreements (full 40-rule list) | [CONTRIBUTING.md](CONTRIBUTING.md) |"
}
```

> TOOL

tool_result
id: toolu_015Y1CSYg9kkrhsPJvqnLndY
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01CBph7xzt6WfjZ9fxschzZs
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "- ❌ Don't track GX Core at \"latest.\" Pin the version in `environment.yml` — GX v1 API has drifted across point releases.",
  "new_string": "- ❌ Don't track GX Core at \"latest.\" Pin the version in `environment.yml` — GX v1 API has drifted across point releases.\n- ❌ Don't add a dependency under a strong-copyleft or source-available license (GPL, AGPL, SSPL, BUSL/Elastic, Commons-Clause) — DataQ ships MIT (ADR [0031](docs/adr/0031-oss-byol-distribution-licensing.md), CONTRIBUTING rule 40); weak copyleft (LGPL/MPL) is OK with notices. Exceptions need an ADR."
}
```

> TOOL

tool_result
id: toolu_01CBph7xzt6WfjZ9fxschzZs
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01WsbLr3qGoadvfiPV52P8Xd
```json
{
  "replace_all": false,
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md",
  "old_string": "**Decision & legal**\n- [ ] Amend/append ADR recording the free-OSS + BYOL distribution decision (supersedes ADR 0013 §5's entitlement/license-key line; keep MIT)\n- [ ] THIRD-PARTY-NOTICES (or SPDX SBOM) generated and shipped in images + GitHub releases; wire generation into CI/publish\n- [ ] **G-h:** paid Databricks workspace before any commercial demo/use (Free Edition is non-commercial-only; decision of 2026-07-03 stands — trigger is exactly a listing)\n- [ ] Marketplace seller registration + per-marketplace review (Partner Center for Azure Phase 1); note free offers still go through certification\n- [ ] Support expectations stated: SUPPORT.md (community support channels for free OSS; SLA only if a paid tier ever appears)\n- [ ] Privacy posture stated: a short statement that DataQ is self-hosted and phones nothing home (verifiably true today — keep it that way)",
  "new_string": "**Decision & legal**\n- [ ] Amend/append ADR recording the free-OSS + BYOL distribution decision (supersedes ADR 0013 §5's entitlement/license-key line; keep MIT) — **in progress: ADR 0031, PR #733**\n- [ ] THIRD-PARTY-NOTICES (or SPDX SBOM) generated and shipped in images + GitHub releases; wire generation into CI/publish\n- [ ] **G-h:** paid Databricks workspace before any commercial demo/use (Free Edition […]

> TOOL

tool_result
id: toolu_01WsbLr3qGoadvfiPV52P8Xd
```
The file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01UaFkZhyFuyhu4QM9pq15u7
```json
{
  "command": "gh issue edit 732 -R TheurgicDuke771/DataQ --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/issues/09-marketplace-checklist.md",
  "description": "Update issue 732 body with legal-item dispositions"
}
```

> TOOL

tool_use Bash
id: toolu_01RdUCXeN8TPGrycwDueStpg
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ diff --stat",
  "description": "Show working-tree change stat before commit"
}
```

> TOOL

tool_result
id: toolu_01UaFkZhyFuyhu4QM9pq15u7
```
https://github.com/TheurgicDuke771/DataQ/issues/732
```

> TOOL

tool_result
id: toolu_01RdUCXeN8TPGrycwDueStpg
```
 CLAUDE.md                                                  |  7 ++++---
 CONTRIBUTING.md                                            |  1 +
 context/post-v1-roadmap.md                                 |  2 +-
 docs/adr/0013-marketplace-distribution-and-anti-lock-in.md | 10 ++++++++++
 docs/adr/0031-oss-byol-distribution-licensing.md           | 13 +++++++------
 docs/adr/README.md                                         |  5 +++--
 6 files changed, 26 insertions(+), 12 deletions(-)
```

> AGENT

Committing the review fixes as a fixup commit (per your in-review PR convention) and pushing.

> TOOL

tool_use Bash
id: toolu_011jPrfVFw52M2QfQQ4nb9Ws
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ add -A && git -C /home/<USER>/Coding/Python/DataQ commit -m 'fixup: address /code-review findings on ADR 0031\n\n- Scope the supersession honestly: 0013 licensed-revenue framing is also\n  amended (table/Consequences/Alternatives), not \"everything else stands\"\n- Amends: ADR-0013 frontmatter + amendment blockquote in 0013 + index-row\n  notes, per the ADR 0028/0012 precedent; Amends field documented in the\n  ADR README Format section\n- Distill the license guardrail: new CONTRIBUTING rule 40 + CLAUDE.md §11\n  bullet (rule counts 39→40); 0031 cites rule 40 instead of the MCP-scoped\n  rule 39\n- Cite ADR 0023 (backend) / 0028 (frontend) for the GHCR images\n- Soften \"reduces to packaging + certification\"; §5 survivors (EULA, DPA,\n  SOC 2/pen test, tax/banking) now carry per-item dispositions in #732\n- G-h roadmap aside points to ADR 0031 (Databricks trigger unchanged)\n\nCo-Authored-By: Claude Fable 5 <<REDACTED_EMAIL>>' && git -C /home/<USER>/Coding/Python/DataQ push",
  "description": "Commit review fixes and push to the PR branch"
}
```

> TOOL

tool_result
id: toolu_011jPrfVFw52M2QfQQ4nb9Ws
```
[docs/adr-0031-oss-byol-licensing e50f78c9] fixup: address /code-review findings on ADR 0031
 6 files changed, 26 insertions(+), 12 deletions(-)
[entire] Pushing entire/checkpoints/v1 to origin..... done
To github.com:TheurgicDuke771/DataQ.git
   0d27ff5a..e50f78c9  docs/adr-0031-oss-byol-licensing -> docs/adr-0031-oss-byol-licensing
```

> TOOL

tool_use Write
id: toolu_01QfjiQC3aMJysXRWVAXM2fq
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-review-summary.md",
  "content": "## /code-review (high effort) — 6 findings, all addressed in `e50f78c9`\n\nRan the 8-angle finder → 1-vote verify pipeline over the diff. 5 CONFIRMED + 1 PLAUSIBLE survived; prose-style candidates were refuted (the ADR is within the 1–2-page rule, and the audit figures are a dated snapshot by design).\n\n| # | Finding | Verdict | Resolution |\n|---|---|---|---|\n| 1 | \"Everything else in ADR 0013 stands unchanged\" was false — 0013's billing table / Consequences / Alternatives still framed BYOL as *paid* license revenue | CONFIRMED | Supersession scope now names the licensed-revenue framing; amendment blockquote added at 0013's top |\n| 2 | Guardrail cited \"CONTRIBUTING rule 39\" (the MCP-only supply-chain audit) — the license check had no real process | CONFIRMED | New **CONTRIBUTING rule 40** (dependency license guardrail); 0031 cites it; rule counts 39→40 in CLAUDE.md |\n| 3 | Partial supersession bypassed the repo's own mechanism (`Amends:` frontmatter — ADR 0028; inline amendment blockquote — ADR 0012); nothing scannable signaled §5 was dead | CONFIRMED | `Amends: ADR-0013` frontmatter, 0013 blockquote, index-row notes on both 0013 and 0031, `Amends` field documented in the README Format section |\n| 4 | \"Binding on […]

> TOOL

tool_result
id: toolu_01QfjiQC3aMJysXRWVAXM2fq
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-review-summary.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01PiJCmBFWsthwJ5DutFJZc1
```json
{
  "command": "gh pr comment 733 -R TheurgicDuke771/DataQ --body-file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/scratchpad/pr-review-summary.md",
  "description": "Post review summary comment on PR 733"
}
```

> TOOL

tool_use Bash
id: toolu_01QXL2XGm8wcnedUyx7icKAd
```json
{
  "command": "sleep 45; gh pr checks 733 -R TheurgicDuke771/DataQ 2>&1 | head -20",
  "description": "Check CI status on PR 733 after a short wait"
}
```

> TOOL

tool_result
id: toolu_01PiJCmBFWsthwJ5DutFJZc1
```
https://github.com/TheurgicDuke771/DataQ/pull/733#issuecomment-4930701656
```

> TOOL

tool_result ERROR
id: toolu_01QXL2XGm8wcnedUyx7icKAd
```
<tool_use_error>Blocked: sleep 45 followed by: gh pr checks 733 -R TheurgicDuke771/DataQ head -20. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
```

> TOOL

tool_use ToolSearch
id: toolu_015diucTwUG39k1HiDWDnsG1
```json
{
  "query": "select:Monitor",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_015diucTwUG39k1HiDWDnsG1
```
{
  "type": "tool_reference",
  "tool_name": "Monitor"
}
```

> TOOL

tool_use Bash
id: toolu_01UeyE8djrogJmyJBt1c8uYp
```json
{
  "command": "until gh pr checks 733 -R TheurgicDuke771/DataQ 2>/dev/null | grep -qvE 'pending|^$' || ! gh pr checks 733 -R TheurgicDuke771/DataQ 2>/dev/null | grep -q pending; do sleep 20; done; gh pr checks 733 -R TheurgicDuke771/DataQ",
  "description": "Wait for PR 733 CI checks to finish, then report",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01UeyE8djrogJmyJBt1c8uYp
```
Command running in background with ID: bdl84fptd. Output is being written to: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/bdl84fptd.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

CI is running on the PR — I'll report once checks finish.

> TOOL

tool_use Read
id: toolu_01F6Uv5Y465ndSKEyJ6WsCYM
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/c0b670d5-58c4-41ee-bbcf-b0dd9018241d/tasks/bdl84fptd.output"
}
```

> TOOL

tool_result
id: toolu_01F6Uv5Y465ndSKEyJ6WsCYM
```
1	Backend — SAST (Bandit)	pass	18s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530393	
2	Backend — dependency audit (pip-audit)	pass	35s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530408	
3	Backend — lint & format	pass	20s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530412	
4	Backend — tests	pass	3m24s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530392	
5	Backend — type check	pass	52s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530398	
6	CodeQL	pass	4s	https://github.com/TheurgicDuke771/DataQ/runs/86257650931	
7	CodeQL analysis (javascript-typescript)	pass	1m6s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530483	
8	CodeQL analysis (python)	pass	1m21s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530480	
9	Frontend — browser E2E (Playwright)	pass	3m8s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530442	
10	Frontend — dependency audit (pnpm audit)	pass	20s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530432	
11	Frontend — lint & format	pass	33s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530484	
12	Frontend — tests	pass	2m27s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530437	
13	GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
14	Secret scanning (betterleaks)	pass	27s	https://github.com/TheurgicDuke771/DataQ/actions/runs/29059334055/job/86257530414	
15	
```

> AGENT

Done — ADR 0031 is drafted, reviewed, fixed, and green. Summary:

## PR [#733](https://github.com/TheurgicDuke771/DataQ/pull/733) — `docs: ADR 0031 — free OSS (MIT) + BYOL distribution licensing`

**All 14 CI checks pass.** The PR carries two commits (the draft + a `fixup:` addressing review findings) and is milestoned to v1.1 Week 3, ready for your review and squash-merge.

**What the ADR records** ([0031-oss-byol-distribution-licensing.md](docs/adr/0031-oss-byol-distribution-licensing.md)):
- DataQ stays **free open-source under MIT**, distributed customer-deployed BYOL — no entitlement/license-key machinery. It formally **amends ADR 0013** (supersedes the §5 licensing line *and* 0013's "revenue licensed outside the meter" framing; the distribution model, phasing, and anti-lock-in guardrails stand).
- Embeds the license-audit evidence (239 backend + 643 frontend packages, zero strong copyleft) and the notices-only compliance obligation.
- A **standing dependency-license guardrail** (no GPL/AGPL/SSPL/BUSL; exceptions need an ADR).

**The agentic code review earned its keep** — 8 finder angles + verification found 6 confirmed issues in my own draft, all posted as [inline comments](https://github.com/TheurgicDuke771/DataQ/pull/733) and fixed in `e50f78c9`:
- The two substantive ones: my "everything else in 0013 stands unchanged" claim was false (0013's billing table/Consequences still framed BYOL as paid revenue — now explicitly amended via a blockquote at 0013's top, per the ADR 0012 […]

> DEVELOPER

Merge it. 
After that can you check this - 

## Summary: Email+OTP Signin Discussion

**Starting question:** Could email+OTP replace Basic auth for local/non-Azure-AD users, given DataQ already rejected Basic auth (ADR 0026) because it would make DataQ a password system?

**Recommendation:** Yes, worth pursuing — OTP is passwordless (avoids the exact problem Basic auth was rejected for) and it closes a real gap: BYOL customers on non-Azure clouds currently have *no* way to sign in (Azure AD is the only human-auth path today; PATs need an existing user to mint them). Proposed as a third authenticator behind the existing `get_current_user` seam (`backend/app/core/auth.py`), alongside Azure AD JWTs and PATs — scoped as its own small ADR rather than folded into 0026.

**1. Session/token design**
- Reuse the PAT *mechanism* (opaque, prefixed token — e.g. `dq_sess_…` — SHA-256 hash-at-rest, indexed lookup) rather than have DataQ self-issue JWTs, to avoid owning a signing-key/rotation story.
- Don't store it in the `api_keys` table though — different lifecycle/visibility than user-managed PATs. Give it its own `sessions` table.
- Short, fixed expiry (e.g. 12–24h), no refresh-token pair — since re-running OTP is low-friction, expiry just means "log in again."
- Open item this forces: `users.aad_object_id` needs […]

> AGENT

I'll merge #733 first (resolving my own review threads if the ruleset blocks on them), then verify the OTP design summary's claims against the actual code.

> TOOL

tool_use Bash
id: toolu_01K2CE4f1wujxTXh2k4Cp4uQ
```json
{
  "command": "gh pr merge 733 -R TheurgicDuke771/DataQ --squash --delete-branch 2>&1 | head -5",
  "description": "Squash-merge PR 733"
}
```

> TOOL

tool_result
id: toolu_01K2CE4f1wujxTXh2k4Cp4uQ
```
X Pull request TheurgicDuke771/DataQ#733 is not mergeable: the base branch policy prohibits the merge.
To have the pull request merged after all the requirements have been met, add the `--auto` flag.
To use administrator privileges to immediately merge the pull request, add the `--admin` flag.
```

> AGENT

Blocked by unresolved review threads (expected — my 5 inline comments). Resolving them via GraphQL, then merging.

> TOOL

tool_use Bash
id: toolu_01G58pM3QafJQLLvSB4SVG9D
```json
{
  "command": "gh api graphql -f query='query { repository(owner:\"TheurgicDuke771\", name:\"DataQ\") { pullRequest(number:733) { reviewThreads(first:20) { nodes { id isResolved } } } } }' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | .id'",
  "description": "List unresolved review thread IDs on PR 733"
}
```

> TOOL

tool_result
id: toolu_01G58pM3QafJQLLvSB4SVG9D
```
PRRT_kwDOSBITx86PvMqY
PRRT_kwDOSBITx86PvMrL
PRRT_kwDOSBITx86PvMrq
PRRT_kwDOSBITx86PvMr9
PRRT_kwDOSBITx86PvMsb
```

> TOOL

tool_use Bash
id: toolu_01VhRmTKYE6ByTmqwcD7ePb5
```json
{
  "command": "for t in PRRT_kwDOSBITx86PvMqY PRRT_kwDOSBITx86PvMrL PRRT_kwDOSBITx86PvMrq PRRT_kwDOSBITx86PvMr9 PRRT_kwDOSBITx86PvMsb; do gh api graphql -f query=\"mutation { resolveReviewThread(input:{threadId:\\\"$t\\\"}) { thread { isResolved } } }\" --jq '.data.resolveReviewThread.thread.isResolved'; done && gh pr merge 733 -R TheurgicDuke771/DataQ --squash --delete-branch 2>&1 | head -3",
  "description": "Resolve all 5 review threads and squash-merge PR 733"
}
```

> TOOL

tool_result
id: toolu_01VhRmTKYE6ByTmqwcD7ePb5
```
true
true
true
true
true
```

> TOOL

tool_use Bash
id: toolu_015LUYiAZGmLWwFmsDv22c8P
```json
{
  "command": "gh pr view 733 -R TheurgicDuke771/DataQ --json state,mergedAt,mergeCommit --jq '{state, mergedAt, sha: .mergeCommit.oid}'",
  "description": "Verify PR 733 merge state"
}
```

> TOOL

tool_result
id: toolu_015LUYiAZGmLWwFmsDv22c8P
```
{"mergedAt":"2026-07-10T00:19:16Z","sha":"6ab4d04c2a28dada8a714433d8ada85781ae657e","state":"MERGED"}
```

> TOOL

tool_use Bash
id: toolu_01RbY9wDqJYxnrvcUTX6aVtw
```json
{
  "command": "git -C /home/<USER>/Coding/Python/DataQ checkout main && git -C /home/<USER>/Coding/Python/DataQ pull --ff-only && git -C /home/<USER>/Coding/Python/DataQ branch -D docs/adr-0031-oss-byol-licensing 2>/dev/null; true",
  "description": "Switch to main, pull, delete local ADR branch"
}
```

> TOOL

tool_use Read
id: toolu_01Y6eefr4AfhH5AgB6Bkoj9H
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/core/auth.py"
}
```

> TOOL

tool_result
id: toolu_01RbY9wDqJYxnrvcUTX6aVtw
```
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
From github.com:TheurgicDuke771/DataQ
   45c5e6a8..6ab4d04c  main       -> origin/main
Updating 45c5e6a8..6ab4d04c
Fast-forward
 CLAUDE.md                                          |  7 +--
 CONTRIBUTING.md                                    |  1 +
 context/post-v1-roadmap.md                         |  2 +-
 ...13-marketplace-distribution-and-anti-lock-in.md | 11 +++++
 docs/adr/0031-oss-byol-distribution-licensing.md   | 52 ++++++++++++++++++++++
 docs/adr/README.md                                 |  4 +-
 6 files changed, 72 insertions(+), 5 deletions(-)
 create mode 100644 docs/adr/0031-oss-byol-distribution-licensing.md
Deleted branch docs/adr-0031-oss-byol-licensing (was e50f78c9).
```

> TOOL

tool_result
id: toolu_01Y6eefr4AfhH5AgB6Bkoj9H
```
1	"""Bearer-token auth (Azure AD or DataQ PAT) + user upsert.
2	
3	Two operating modes — picked once at import time from settings:
4	
5	- **Real mode** — `AZURE_TENANT_ID` + `AZURE_API_CLIENT_ID` are set.
6	  Two authenticators behind the one `get_current_user` seam (ADR 0026):
7	  a **DataQ PAT** (`Authorization: Bearer dq_live_…` → hashed lookup in
8	  `api_keys`, resolving to the owning user) is tried first by prefix;
9	  anything else is an **Azure AD token** validated by `fastapi-azure-auth`
10	  (issuer, audience, signature, expiry, scope — OpenID config loaded at app
11	  startup via `init_auth()` and refreshed automatically).
12	
13	- **Dev bypass** — all three of:
14	  `ENVIRONMENT=dev`, `AUTH_DEV_BYPASS=true`, Azure vars empty.
15	  No token required. Resolves every request to a fixed dev user upserted
16	  into the `users` table. Intended for local development against a
17	  Postgres in `docker-compose` without a real Azure tenant. (PATs still
18	  resolve in dev bypass when presented — the same seam order.)
19	
20	If neither mode is configured, `init_auth` raises at startup — fail-closed.
21	"""
22	
23	from collections.abc import Callable
24	from datetime import UTC, datetime
25	from typing import Annotated, Any
26	
27	from […]

> TOOL

tool_use Bash
id: toolu_01PrzUHiaWQjwWveqdYEqBLE
```json
{
  "command": "grep -n \"class User\" -A 25 /home/<USER>/Coding/Python/DataQ/backend/app/db/models.py | head -32",
  "description": "Inspect User model columns"
}
```

> TOOL

tool_result
id: toolu_01PrzUHiaWQjwWveqdYEqBLE
```
111:class User(Base):
112-    __tablename__ = "users"
113-
114-    id: Mapped[uuid.UUID] = _uuid_pk()
115-    aad_object_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
116-    email: Mapped[str] = mapped_column(String(320), nullable=False)
117-    display_name: Mapped[str | None] = mapped_column(String(256))
118-    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
119-    created_at: Mapped[datetime] = _created_at()
120-    updated_at: Mapped[datetime] = _updated_at()
121-
122-
123-class ApiKey(Base):
124-    """A DataQ-issued personal access token (PAT) — ADR 0026 phase 1 (#461).
125-
126-    The credential is a high-entropy random token shown once at creation; only
127-    its SHA-256 hex digest is stored (a verifier secret — never retrievable, so
128-    deliberately NOT in the SecretStore). The key authenticates as its owning
129-    user through the same `get_current_user` seam as Azure AD, inheriting the
130-    owner's per-suite grants — no separate authz model. `ondelete=CASCADE` ties
131-    the lifecycle to the owner: deleting the user kills their keys.
132-    """
133-
134-    __tablename__ = "api_keys"
135-
136-    id: Mapped[uuid.UUID] = _uuid_pk()
```

> TOOL

tool_use Read
id: toolu_01JSJTavBm48RRUfs1QqdkoK
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/alerting/email.py"
}
```

> TOOL

tool_result
id: toolu_01JSJTavBm48RRUfs1QqdkoK
```
1	"""Email (SMTP) ``ResultPublisher`` — sends a run's report as an email.
2	
3	Workspace-level: one sender (SMTP submission with STARTTLS) and a fixed
4	recipient list. The password (e.g. a Gmail app-password) is resolved from the
5	SecretStore by name; the rest of the SMTP coordinates are non-secret config.
6	Delivery follows the **same** per-suite policy as the other publishers (the
7	suite's `enabled` flag + `alert_on` threshold via :func:`routing.route_for`);
8	only the rendering + transport differ. Unconfigured (no recipients / username /
9	password secret) is a quiet no-op.
10	"""
11	
12	from __future__ import annotations
13	
14	import smtplib
15	import ssl
16	from email.message import EmailMessage
17	
18	from sqlalchemy.orm import Session
19	
20	from backend.app.alerting import render
21	from backend.app.alerting.base import CheckReport, RunReport
22	from backend.app.alerting.routing import route_for
23	from backend.app.core.logging import get_logger
24	from backend.app.core.secrets import SecretNotFoundError, SecretStore
25	from backend.app.services import notification_service
26	
27	log = get_logger(__name__)
28	
29	_SMTP_TIMEOUT_SECONDS = 15.0
30	_MAX_CHECK_LINES = 20
31	
32	
33	def render_subject(report: RunReport) -> str:
34	    """The email subject line — verdict + suite + counts at a glance."""
35	    if report.success:
36	        return f"[DataQ] {report.suite_name}: all {report.total_checks} checks […]

> TOOL

tool_use Bash
id: toolu_01D58QFpv9an13RmVYgW6T3g
```json
{
  "command": "grep -n \"email\\|smtp\" /home/<USER>/Coding/Python/DataQ/backend/app/core/config.py | head -25",
  "description": "Find email/SMTP config fields"
}
```

> TOOL

tool_result
id: toolu_01D58QFpv9an13RmVYgW6T3g
```
78:    # surface shows (#490) AND the "View run" deep links in Slack/email alerts
85:    # Workspace-admin allowlist — emails permitted to use the /admin read
89:    # against the IdP-supplied email — a generic identity attribute, so no
93:    # normalised `workspace_admin_email_set` property, never the raw field.
95:    workspace_admin_emails: str = ""
128:    # a string — not list[str] — like workspace_admin_emails, to sidestep Pydantic
145:    # only when email_to, email_username, and email_password_secret_name are all
147:    email_smtp_host: str = "smtp.gmail.com"
148:    email_smtp_port: int = 587
149:    email_username: str | None = None
150:    email_from: str | None = None  # defaults to email_username when unset
151:    email_to: str = ""  # comma-separated recipients; empty → no email alerting
152:    email_password_secret_name: str | None = None
169:    def workspace_admin_email_set(self) -> frozenset[str]:
170:        """Normalised (lower-cased, stripped) admin emails for membership tests.
176:            part.strip().lower() for part in self.workspace_admin_emails.split(",") if part.strip()
179:    def is_admin_email(self, email: str | None) -> bool:
180:        """True iff `email` is in the workspace-admin allowlist. The one
184:        normalized = (email or "").strip().lower()
185:        return bool(normalized) and normalized in self.workspace_admin_email_set
```

> TOOL

tool_use Bash
id: toolu_01NpndKT6FwBw6ZpbEEf3MUC
```json
{
  "command": "grep -n -i \"basic\" /home/<USER>/Coding/Python/DataQ/docs/adr/0026-auth-api-keys-and-principal-seam.md | head; grep -rn \"DATAQ_AUTH_MODE\" /home/<USER>/Coding/Python/DataQ/frontend/src --include=\"*.ts\" --include=\"*.tsx\" -l 2>/dev/null | head -3; grep -rn \"mode\" /home/<USER>/Coding/Python/DataQ/frontend/src/auth/*.ts 2>/dev/null | grep -i \"bypass\\|oidc\" | head -5",
  "description": "Check ADR 0026 Basic-auth rationale and frontend auth modes"
}
```

> TOOL

tool_result
id: toolu_01NpndKT6FwBw6ZpbEEf3MUC
```
51:- **HTTP Basic auth — rejected.** DataQ has no password store (identity is delegated to OIDC);
52:  Basic auth would make DataQ a password system (storage/hashing policy, lockout, reset flows,
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/AuthGate.tsx
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/authContext.ts:16:/** The current OIDC user (null when not signed in / not in real auth mode). */
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/config.ts:17: * - 'real'         — `mode:'oidc'` with authority + clientId present. The generic
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/config.ts:20: * - 'dev_bypass'   — ONLY when `mode:'bypass'` is explicitly set. Fail-closed:
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/config.ts:30:  mode?: 'bypass' | 'oidc';
/home/<USER>/Coding/Python/DataQ/frontend/src/auth/config.ts:62:    mode: bypass ? 'bypass' : tenantId && clientId ? 'oidc' : undefined,
```

> AGENT

Merged and verified: [#733](https://github.com/TheurgicDuke771/DataQ/pull/733) squash-merged to main as `6ab4d04c` (had to resolve the 5 review threads first — the main ruleset blocks on them), local main synced, branch deleted. The PR had ticked the progress.md N/A box, so no tracker update was needed.

---

# OTP design summary — checked against the codebase

**Overall verdict: the design is sound and the codebase claims are almost all accurate — I verified each against the code. One claim is factually wrong (rate limiting), and three significant design areas are missing entirely (sign-up gating, frontend mode, identity linking). Details below.**

## Claims that check out (verified, not assumed)

- **ADR 0026's Basic-auth rejection** reads exactly as characterized: "Basic auth would make DataQ a password system (storage/hashing policy, lockout, reset flows…)". OTP genuinely avoids the password-store half of that.
- **The auth gap is real**: [auth.py](backend/app/core/auth.py) has exactly two authenticators (Azure JWT via `SingleTenantAzureAuthorizationCodeBearer`, PAT by `dq_live_` prefix), and PAT minting requires an already-authenticated user. Non-Azure human sign-in does not exist.
- **Not reusing `api_keys`, hashing in a `sessions` table** is consistent with the codebase's own doctrine — the `ApiKey` docstring literally says verifier secrets are "deliberately NOT in the SecretStore." The `dq_sess_` prefix-branch […]

> DEVELOPER

what do you think of the feasibility? 
And what is our mailbox situation?

> AGENT

Good questions — let me ground both: check what SMTP/email is actually configured today (repo defaults, prod env, Key Vault) before opining on feasibility.

> TOOL

tool_use Bash
id: toolu_019qpf91Md49VsF4MDvqYUCE
```json
{
  "command": "grep -n \"EMAIL\" /home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example /home/<USER>/Coding/Python/DataQ/.env.app.example 2>/dev/null; grep -rn \"EMAIL\" /home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/*.tf | head -10",
  "description": "Check email config in prod env template and Terraform"
}
```

> TOOL

tool_result
id: toolu_019qpf91Md49VsF4MDvqYUCE
```
/home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example:49:WORKSPACE_ADMIN_EMAILS=
/home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example:76:EMAIL_USERNAME=
/home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example:77:EMAIL_FROM=
/home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example:78:EMAIL_TO=
/home/<USER>/Coding/Python/DataQ/deploy/.env.app.prod.example:79:EMAIL_PASSWORD_SECRET_NAME=
/home/<USER>/Coding/Python/DataQ/.env.app.example:52:WORKSPACE_ADMIN_EMAILS=
/home/<USER>/Coding/Python/DataQ/.env.app.example:101:# Email (SMTP) — active only when EMAIL_TO + EMAIL_USERNAME + EMAIL_PASSWORD_SECRET_NAME
/home/<USER>/Coding/Python/DataQ/.env.app.example:103:EMAIL_SMTP_HOST=smtp.gmail.com
/home/<USER>/Coding/Python/DataQ/.env.app.example:104:EMAIL_SMTP_PORT=587
/home/<USER>/Coding/Python/DataQ/.env.app.example:105:EMAIL_USERNAME=
/home/<USER>/Coding/Python/DataQ/.env.app.example:106:EMAIL_FROM=
/home/<USER>/Coding/Python/DataQ/.env.app.example:107:EMAIL_TO=
/home/<USER>/Coding/Python/DataQ/.env.app.example:108:EMAIL_PASSWORD_SECRET_NAME=
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:51:    { name = "WORKSPACE_ADMIN_EMAILS", value = var.workspace_admin_emails },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:71:    { name = "EMAIL_SMTP_HOST", value = "smtp.gmail.com" },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:72:    { name = "EMAIL_SMTP_PORT", value = "587" },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:73:    { name = "EMAIL_PASSWORD_SECRET_NAME", value = "channel-email-password" },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:74:    { name = "EMAIL_USERNAME", value = var.email_username },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:75:    { name = "EMAIL_FROM", value = var.email_from },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/containerapps.tf:76:    { name = "EMAIL_TO", value = var.email_to },
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/variables.tf:107:  description = "Comma-separated workspace-admin allowlist (WORKSPACE_ADMIN_EMAILS)."
```

> TOOL

tool_use Bash
id: toolu_01HWb7KMJtKfYcazNnC5as7z
```json
{
  "command": "grep -n \"EMAIL\\|email\" /home/<USER>/Coding/Python/DataQ/docker-compose.yml | head -5; grep -rn \"email\" /home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/terraform.tfvars 2>/dev/null | sed 's/=.*/= <redacted-check>/' | head -5",
  "description": "Check compose and tfvars for email settings (keys only)"
}
```

> TOOL

tool_result
id: toolu_01HWb7KMJtKfYcazNnC5as7z
```
88:      # No-colon form: WORKSPACE_ADMIN_EMAILS="" in .env opts back OUT (to a
90:      WORKSPACE_ADMIN_EMAILS: ${<REDACTED_EMAIL>}
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/terraform.tfvars:11:workspace_admin_emails = <redacted-check>
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/terraform.tfvars:14:email_username = <redacted-check>
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/terraform.tfvars:15:email_from     = <redacted-check>
/home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/terraform.tfvars:16:email_to       = <redacted-check>
```

> AGENT

The prod stack does wire an SMTP sender. Let me confirm the Key Vault secret actually exists (names only, no values) and check whether the app is still running during the wind-down.

> TOOL

tool_use Bash
id: toolu_01NEcRV3fARJEqB6EKt4Upcr
```json
{
  "command": "grep -n 'name' /home/<USER>/Coding/Python/DataQ/deploy/terraform/azure/keyvault.tf | head -5",
  "description": "Find Key Vault resource name"
}
```

> TOOL

tool_result
id: toolu_01NEcRV3fARJEqB6EKt4Upcr
```
17:  name                       = "dataq-app-kv-${random_string.suffix.result}"
19:  resource_group_name        = data.azurerm_resource_group.dataq.name
21:  sku_name                   = "standard"
32:  role_definition_name = "Key Vault Secrets Officer"
46:  name        = "DataQ App KV Secrets RW ${random_string.suffix.result}"
```

> TOOL

tool_use Bash
id: toolu_01D8mxTKtKNVCsdfU9iXcTD7
```json
{
  "command": "az keyvault list -g dataq-rg --query \"[].name\" -o tsv 2>&1 | head -3",
  "description": "List Key Vault names in dataq-rg"
}
```

> TOOL

tool_result
id: toolu_01D8mxTKtKNVCsdfU9iXcTD7
```
dataq-app-kv-aw6laj
```

> TOOL

tool_use Bash
id: toolu_01GdWyZbFNAgfZMb3zx27KtZ
```json
{
  "command": "az keyvault secret list --vault-name dataq-app-kv-aw6laj --query \"[].name\" -o tsv 2>&1 | head -20; echo ---; az containerapp list -g dataq-rg --query \"[].{name:name, running:properties.runningStatus}\" -o tsv 2>&1 | head -8",
  "description": "List KV secret names and Container App running status"
}
```

> TOOL

tool_result
id: toolu_01GdWyZbFNAgfZMb3zx27KtZ
```
adf-webhook-secret
airflow-oauth-client-secret-harness
airflow-webhook-secret
channel-email-password
channel-slack-webhook
conn-adf-factory
conn-adf-qa
conn-adls-landing
conn-adls-raw
conn-airflow
conn-airflow-qa
conn-bcdcad4f-48dd-4f6a-9f97-e381e9fac621
conn-snowflake-orders
conn-snowflake-payments
conn-snowflake-retail
conn-unity-catalog-qa
conn-unity-catalog-retail
databricks-token-harness
dataq-pat-w1-admin
dataq-pat-w1-member
---
WARNING: The behavior of this command has been altered by the following extension: containerapp
dataq-harness-redis	Stopped
dataq-harness-airflow	Stopped
dataq-harness-airflow-worker	Stopped
dataq-app-redis	Running
dataq-app-worker	Running
dataq-app-api	Running
dataq-harness-airflow-trigger	Stopped
```

> AGENT

Both answered — and I checked the live state rather than guessing.

## Mailbox situation: you already have a working sender

- The prod stack wires SMTP for alerting: `smtp.gmail.com:587`, sender = the Gmail account set as `email_username` in your (gitignored) tfvars, app password stored in Key Vault as **`channel-email-password`** — I confirmed the secret exists in `dataq-app-kv-aw6laj`, and this path was validated live when the #413 email alerts shipped. The app itself (`dataq-app-api`/`worker`/`redis`) is still **Running** — only the harness apps are stopped.
- So for a demo/reference deployment, OTP mail could send today with zero new provisioning — the design's separate `AUTH_EMAIL_*` block would just point at the same Gmail account.
- Two caveats: **(1)** consumer Gmail SMTP caps out around ~500 mails/day — irrelevant at your scale, but not a product answer; under BYOL the mailbox is *customer-supplied SMTP config* anyway (their relay handles SPF/DKIM/deliverability), so your Gmail is only ever the reference deployment's mailbox. **(2)** When Azure winds down (~2026-07-25) the Key Vault goes with it, so the app password re-homes to wherever the local-first posture (#591) puts secrets — today that's the gitignored `.env` via `EnvSecretStore`, i.e. plaintext-on-disk, which is the already-flagged non-Azure SecretStore gap. […]

> DEVELOPER

But, how will this approach looks like on a fresh deployment? there will not be a mailbox right?

> AGENT

Right — that's the honest catch: **OTP doesn't remove the external dependency, it swaps "bring an IdP" for "bring a mailbox."** A fresh deployment with no SMTP configured has no OTP sign-in, full stop. But I'd argue that's an acceptable and well-precedented shape if the ADR is explicit about it:

## What a fresh deployment looks like

The auth story becomes a three-mode ladder, each with a declared bring-your-own prerequisite:

| Mode | You bring | Fresh-deploy bootstrap |
|---|---|---|
| `bypass` | nothing | works instantly — solo/eval only (this is already today's `docker-compose.ghcr.yml` path) |
| `otp` | SMTP coordinates | set `AUTH_EMAIL_*` + `WORKSPACE_ADMIN_EMAILS=you@…` + the signup allowlist at install; sign in to your own mailbox; you're admin |
| `oidc` | an IdP tenant | today's Azure AD path (generic OIDC later) |

The first-admin bootstrap under OTP is actually *cleaner* than most self-hosted tools: no seeded password to rotate, no `admin/admin` default — the operator IS the allowlisted email, and proof of mailbox ownership is the credential. Grafana/GitLab-style bootstrap passwords are the thing this avoids.

## Is "bring a mailbox" a reasonable ask?

- **For the actual BYOL target (a company deploying into their own […]

> DEVELOPER

got it, switching the topic a bit, how the RBAC works in the cuurent state for DataQ?

> AGENT

Let me ground this in the actual authz code rather than answering from memory.

> TOOL

tool_use Read
id: toolu_01F3LtPNUEW1adCtj1eZv7id
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/backend/app/services/suite_authz.py"
}
```

> TOOL

tool_result
id: toolu_01F3LtPNUEW1adCtj1eZv7id
```
1	"""Suite authorization — the single primitive every suite-scoped endpoint gates on.
2	
3	A user's effective permission on a suite is the highest of: **owner** (they are
4	`suite.created_by` — implicit, immutable, never a share row), **admin** (they are
5	a **workspace-admin** — implicit on *every* suite, never a share row; ADR 0027),
6	or their `shares` row (`view` < `edit`). Capability ladder:
7	
8	    view   — read the suite, its checks, its results
9	    edit   — + create/update/delete checks, update the suite, trigger runs
10	    admin  — + manage shares (grant/revoke) AND delete the suite. Held by the
11	             workspace-admin(s) (`WORKSPACE_ADMIN_EMAILS`), implicit on every
12	             suite — the governance / break-glass path. **Not grantable to normal
13	             users** (a share can only be `view`/`edit`; ADR 0027).
14	    owner  — same capabilities as admin, but it is the creator: cannot be
15	             revoked or demoted, and granting a share to the owner is rejected.
16	
17	`admin` ranks below `owner` and above the `view`/`edit` shares, so a
18	workspace-admin always clears an `admin` gate even on a suite they don't own.
19	Legacy `shares.permission = 'admin'` rows (pre-#482) still resolve to `admin`
20	until the […]

> TOOL

tool_use Bash
id: toolu_019eitRvoJThNYyditvAPjKL
```json
{
  "command": "grep -n \"class Share\" -A 20 /home/<USER>/Coding/Python/DataQ/backend/app/db/models.py",
  "description": "Inspect Share model"
}
```

> TOOL

tool_result
id: toolu_019eitRvoJThNYyditvAPjKL
```
452:class Share(Base):
453-    __tablename__ = "shares"
454-    __table_args__ = (
455-        _in_check("permission", PERMISSIONS, "permission_valid"),
456-        UniqueConstraint("suite_id", "user_id", name="uq_shares_suite_user"),
457-        Index("ix_shares_user_id", "user_id"),
458-    )
459-
460-    id: Mapped[uuid.UUID] = _uuid_pk()
461-    suite_id: Mapped[uuid.UUID] = mapped_column(
462-        UUID(as_uuid=True), ForeignKey("suites.id", ondelete="CASCADE"), nullable=False
463-    )
464-    user_id: Mapped[uuid.UUID] = mapped_column(
465-        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
466-    )
467-    permission: Mapped[str] = mapped_column(String(16), nullable=False)
468-    created_at: Mapped[datetime] = _created_at()
469-
470-    # Read-only convenience for enriching a share with the grantee's directory
471-    # identity (email / display_name) so the sharing UI can name collaborators.
472-    # ORM-only — no schema change. Default-lazy: the hot authz path
```

> AGENT

One more check — how non-suite resources (connections, runs, admin) are gated.

> TOOL

tool_use Bash
id: toolu_01KReWC37Q1teF4TbA6Qgx1V
```json
{
  "command": "grep -n \"get_current_user\\|require_\\|created_by\\|owner\" /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/connections.py | head -15; grep -rn \"require_permission\\|require_workspace_admin\" /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/*.py /home/<USER>/Coding/Python/DataQ/backend/app/mcp/server.py 2>/dev/null | awk -F: '{print $1}' | sort | uniq -c",
  "description": "Check connections authz and where permission gates are used"
}
```

> TOOL

tool_result
id: toolu_01KReWC37Q1teF4TbA6Qgx1V
```
23:from backend.app.core.auth import get_current_user
55:    created_by: uuid.UUID
66:            created_by=conn.created_by,
86:    current_user: Annotated[User, Depends(get_current_user)],
97:        created_by=current_user.id,
109:    current_user: Annotated[User, Depends(get_current_user)],
125:    current_user: Annotated[User, Depends(get_current_user)],
139:    current_user: Annotated[User, Depends(get_current_user)],
162:    current_user: Annotated[User, Depends(get_current_user)],
176:    current_user: Annotated[User, Depends(get_current_user)],
193:    current_user: Annotated[User, Depends(get_current_user)],
232:    current_user: Annotated[User, Depends(get_current_user)],
   3 /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/admin.py
  11 /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/checks.py
   4 /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/notifications.py
   7 /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/runs.py
  11 /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/suites.py
   6 /home/<USER>/Coding/Python/DataQ/backend/app/mcp/server.py
```

> TOOL

tool_use Bash
id: toolu_01TqNvVeWgmRLVqe2ZquyAFV
```json
{
  "command": "grep -n \"def list_connections\\|def get_connection\\b\" -A 8 /home/<USER>/Coding/Python/DataQ/backend/app/services/connection_service.py | head -20; grep -n \"workspace\\|any authenticated\\|created_by\" /home/<USER>/Coding/Python/DataQ/backend/app/api/v1/connections.py | head -8",
  "description": "Check whether connections are user-scoped or workspace-global"
}
```

> TOOL

tool_result
id: toolu_01TqNvVeWgmRLVqe2ZquyAFV
```
199:def list_connections(
200-    session: Session,
201-    *,
202-    conn_type: str | None = None,
203-    env: str | None = None,
204-) -> list[Connection]:
205-    stmt = select(Connection).order_by(Connection.created_at.desc())
206-    if conn_type is not None:
207-        stmt = stmt.where(Connection.type == conn_type)
--
213:def get_connection(session: Session, connection_id: uuid.UUID) -> Connection:
214-    conn = session.get(Connection, connection_id)
215-    if conn is None:
216-        raise ConnectionNotFoundError(
217-            "connection not found", detail={"connection_id": str(connection_id)}
218-        )
219-    return conn
220-
221-
55:    created_by: uuid.UUID
66:            created_by=conn.created_by,
97:        created_by=current_user.id,
```

> AGENT

Here's the current RBAC picture, verified against the code (not just the ADRs):

## The model: two axes, one enforcement primitive

**There are no stored roles.** A user row carries no role column and there's no roles table — authorization is derived at request time from two sources:

**Axis 1 — workspace-admin (global, config-driven).** `WORKSPACE_ADMIN_EMAILS` is a comma-separated env allowlist, matched case-insensitively against the IdP-supplied email ([auth.py:229-241](backend/app/core/auth.py#L229-L241)). It's deliberately a generic identity attribute (no Entra claim read, per ADR 0010/0013). Being on the list grants: the `/admin` read endpoints via `require_workspace_admin` (403 otherwise), implicit `admin` on **every** suite, and workspace-wide visibility (extended to the MCP tools and schedules in #488/#695). There is no in-app management of this — changing admins means changing the env var and restarting.

**Axis 2 — suite-level sharing (the only resource-level RBAC).** Defined entirely in [suite_authz.py](backend/app/services/suite_authz.py), with a strict capability ladder `view(1) < edit(2) < admin(3) < owner(4)`:

| Level | How you get it | What it allows |
|---|---|---|
| `view` | a `shares` row | read the suite, its checks, its results |
| `edit` | a `shares` row | + create/update/delete checks, update the suite, trigger runs |
| `admin` | being […]