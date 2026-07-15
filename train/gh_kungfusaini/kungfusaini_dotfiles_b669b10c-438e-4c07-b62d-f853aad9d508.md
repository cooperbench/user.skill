> DEVELOPER

I have a video call tomorrow with a potential investor — a former Google Head of Fintech UK who now runs a UK VC firm. The call is an intro conversation. My co-founder will demo the product and explain the methodology and Bayesian forecasting approach. My role on the call is specifically to answer questions about infrastructure, architecture, security, devops, and production engineering.
This is not a technical due diligence call. It's an intro. The investor needs to feel confident enough in the engineering that he can introduce us to senior technical people in his network — including potentially Google — without embarrassment. He won't see the code. He just needs to hear answers that sound credible coming from someone who's spent decades around serious enterprise technology.
Please analyse the entire codebase and prepare me to answer questions confidently across all of the following areas. For each, give me a concise factual summary of what's actually in the codebase, specific component or file references where useful, and a one or two sentence answer I could give verbally.
1. Architecture overview
One paragraph plain English summary of the overall system. Five main components and what each does. How they connect. Suitable for a 30 second verbal description.
2. Production readiness
Database — what's used, schema management, migrations. Object storage for artifacts — what's stored where and why. Queue worker — how async jobs are handled. API layer — what framework, what endpoints exist. Frontend — how it's served.
3. Code quality and testing
How many tests exist, what they cover. Whether tests pass cleanly. CI/CD status. Code organisation and separation of concerns. Logging approach.
4. Security posture
How secrets are managed currently. API authentication — what mechanism, how it's enforced. Any known security gaps. The LiteLLM security context specifically — is it used in library mode or proxy mode, how do credentials flow through it, what's the attack surface, any current CVE considerations.
5. Scalability and concurrency
What happens when many questions run simultaneously. How the queue worker handles backpressure. LLM provider resilience via LiteLLM or similar — multi-provider failover, rate limit handling, what happens when a provider has downtime. Cost management across providers.
6. Observability
Logging structure and where logs go. How we'd know if something is broken in production. Tracing across distributed worker jobs. Run state and artifact lineage.
7. Data engineering
How sources are deduplicated. PDF processing pipeline. Document storage and review registry. How a forecast can be traced back to its source evidence — auditability and provenance.
8. Cost structure
Per-question cost rough estimate — LLM tokens plus retrieval API costs. How cost scales with volume. Whether provider routing helps cost optimisation.
9. Reproducibility and deployment
Docker setup — how complete it is. Whether a new technical team could spin up the stack independently from documentation alone. Environment-based configuration.
10. Failure handling
What happens mid-pipeline if something fails. Retry logic. Idempotency. Whether a half-completed run can resume cleanly. Data corruption risks.
11. Privacy and data residency
Where data is stored. Whether the system could be deployed in a customer's own cloud. UK GDPR considerations. How sensitive enterprise data would be handled in a hedge fund or government context.
12. Versioning and reproducibility of forecasts
Whether a forecast made today can be reproduced six months later with the same inputs. Important for audit trails.
13. Integration potential
Could this be embedded into an existing platform via API. How hard that would actually be. What integration would require from an acquirer.
14. IP and dependencies
Confirm clean IP chain — all code written by the team, no third party contributors with claims. List the main open source dependencies and their licences. Flag anything with copyleft or commercial restriction concerns.
15. Technical debt and honest weaknesses
What would I fix first with a properly resourced team. Where are the rough edges. Senior people respect honest answers about weaknesses over false claims of perfection.
16. Defensibility
Why can't a large company just build this themselves with GPT-4 in three months. What's actually hard about the system. Where is the real engineering moat — domain packs, retrieval pipeline, evidence extraction, inference graph.
17. The team contribution question
One concise sentence I can use to describe what I specifically built — the production infrastructure, retrieval pipeline, API layer, persistence, queue worker, web interface, devops. Distinct from my co-founder's contribution to the Bayesian methodology and product vision.
18. The Pip-forwards-this test
Three or four genuinely impressive things about the technical infrastructure that the investor could mention to a senior Google contact without embarrassment — things that show this is real engineering, not a prototype.
Format the output as a structured document I can read in 30 minutes tonight and use as a reference during the call tomorrow. Be specific to this codebase. Don't give generic answers. If something I should know is missing or weak, flag it honestly so I'm not caught off guard.

> AGENT

I'll analyze the codebase across all the areas you need. Let me dispatch parallel exploration agents to cover the breadth, then synthesize into a briefing document.

> AGENT

Now I have the lay of the land. Let me dispatch parallel deep-dive agents.

> AGENT

I have comprehensive findings from all five analysis agents. Let me synthesize them into the briefing document.

> AGENT

Done. The briefing is at `/Users/sumeet/INVESTOR_BRIEFING.md` — outside the repo so it won't get accidentally committed.

It covers all 18 sections you asked for, each grounded in specific file paths and line numbers from the actual codebase. A few things worth flagging that you'll want to be ready for tomorrow:

**Honest weaknesses you should pre-empt rather than wait to be asked about:**
1. **PyMuPDF is AGPL-3.0** — used as a PDF fallback. Needs license-or-remove decision before any binary distribution. Lead with this if licensing comes up.
2. **S3/MinIO artifact store is interface-only** — env vars exist, implementation is local disk. MinIO was removed in SPI-37.
3. **Worker concurrency is single-job-per-replica** with sequential per-question execution. Scale horizontally; per-question parallelism is a config flag, not implemented yet.
4. **mypy in soft mode**, `pytest` ignores frontend by default — senior reviewers will spot both.
5. **Prompts live on disk in git, not in DB.** Old-run reproducibility relies on git checkout, not pure DB replay.

**Strongest things to drop unprompted** (full quotes in section 18):
- Every LLM call traced with template SHA, rendered-prompt SHA, model requested vs effective, tokens, USD — all in Postgres.
- LiteLLM in **proxy mode**, provider keys never touch app code or DB.
- Real Bayesian factor inference (`core/research_driver/bn_inference.py`), not LLM-as-judge.
- FS10 validation harness with queryable prompt-edit audit trail against resolved historical questions.

Read time is roughly 25–30 minutes. The cheat-sheet table at the bottom is for quick on-call lookup.
