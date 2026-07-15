> DEVELOPER

write one or more linkedin articles about what we've been building the last 2 weeks

> AGENT

Let me gather context on what's been built recently.

> DEVELOPER

go through commits

> AGENT

Now I have full context — 50 commits across 5 major themes. Let me draft the articles.

> DEVELOPER

these articles do not encapsulate the specific features that have been built for the past week...

> AGENT

You're right, those were too abstract. Let me look at the actual features with dates so I can write about what was concretely built.

> AGENT

Good, now I have the full picture. Let me rewrite with concrete features. Here's what actually shipped in two weeks: **Week 1 (Mar 16-19):** shadcn/ui migration, LLM proxy + CLI setup, Pino→OTel, self-hosted deployment, intent LLM traces, real-time feed SSE + agent activator, orchestrator hardening, observation convergence **Week 2 (Mar 19-26):** BM25 replacing embeddings, MCP tool registry with credential brokerage + OAuth discovery + governance + UI, SandboxAgent runtime + intent-gated MCP governance Let me rewrite with specifics.

> DEVELOPER

what im interested in here is the agent activation + sandboxagent runtime orchestration (one article) then governance and mcp as a second - you can also use the github issues as references for articles to be written

> AGENT

Now I have the full picture with issues. Let me rewrite both articles.

> AGENT

Two articles written to `docs/linkedin/`: **Article 1: Agent Activation + Sandbox Orchestration** — covers the Agent Activator (LLM classification routing, loop dampening, governance audit trail), SandboxAgent runtime (adapter, event bridge, session store, lifecycle), and how they compose. References PRs #167 and #189, links to issues #180 (trigger subsystem), #186 (yield-and-resume), #187 (session persist driver). **Article 2: MCP Governance + Tool Registry** — covers the tool registry (discovery, credential brokerage with AES-256-GCM, tool grants), proxy-as-tool-layer architecture (inject/intercept/execute), intent-gated MCP governance (scope engine, four authorization paths, structured error responses, session-aware auth), and the management UI. References issues #178, #189, #182 (streaming interception), #181 (agents as tools), #186 (yield-and-resume). I also removed the two generic drafts from before. Want me to adjust tone, length, or focus on either article?

> DEVELOPER

for article 2, include the skills system we're gonna build: gh issue Skills: graph-native behavioral expertise layer #177

> AGENT

You're absolutely right — LinkedIn articles need to be for a general audience. No code, no PRs, no issue links. Let me rewrite both as proper thought leadership pieces.

> AGENT

Done. Both articles rewritten for a general LinkedIn audience: **Article 1** — "We Taught AI Agents to Wake Themselves Up": Agent Activator (event routing, LLM classification vs vector search, loop dampening), sandboxed agent runtime (provisioning, streaming, persistence, lifecycle), and how they compose into a closed loop. Teases time-based triggers, yield-and-resume, and cloud persistence. **Article 2** — "Your AI Agent Needs a GitHub Token. Who Decides If It Gets One?": Tool registry with credential brokerage, proxy-as-universal-tool-layer, intent-gated authorization (four outcome paths), and the Skills system (three competency layers, auto tool grants, LLM-driven requirement analysis, ecosystem import, Observer-driven evolution). No code, no file paths, no PRs, no issue links. Business language throughout.

> DEVELOPER

also please use business domain as examples. it's clearly stated in AGENTS.md: ## Communication - When making examples (in docs, research, discussions, commit messages), use real-world business domain examples (e.g. supply chain disruption, customer refund, compliance audit), not developer-centric examples (e.g. merge PR, deploy service, fix bug). Brain is a general-purpose coordination system, not a developer tool.

> AGENT

Good catch. Let me replace all the developer-centric examples with business domain ones.

> DEVELOPER

these are too enterprisey and specific

> AGENT

Got it — business domain but natural, not corporate jargon. Let me redo both.

> DEVELOPER

dont mention extensions as something that is IN progress, incorporate it as something that is already done

> AGENT

Now article 2.

> AGENT

Updated both articles. All examples are now business domain — customer refunds, pricing policy contradictions, vendor decisions, compliance reviews, customer escalations, CRM lookups. No code, no PRs, no developer tooling references.

> DEVELOPER

answer: would article 1 be better if it also included gh issue External event ingestion via webhooks #165 ?

> AGENT

Yes, it would strengthen the article significantly. Right now article 1 has a gap: it explains that agents activate when the graph changes, but it's vague about where those changes come from. The reader might assume it's only internal — agents triggering other agents. External event ingestion completes the story end-to-end: **the real world triggers agents**. A payment failure from Stripe becomes an observation in the graph, the Activator wakes the right agent, and the agent handles it. That's the full loop from external event to autonomous action — much more compelling than "graph changes activate agents" in the abstract. It also makes the business domain examples land harder. "A customer refund contradicts a pricing policy" is interesting. "A Stripe payment failure arrives via webhook, the Activator wakes the finance agent, and it investigates autonomously" is a concrete story readers can picture in their own operations. Want me to weave it in?

> DEVELOPER

yes

> AGENT

Done. Added a new "External Event Ingestion" section before "How It All Connects" — Stripe payment failures, PagerDuty alerts, CRM signals flowing in via webhooks, becoming observations in the graph, and feeding the Activator. The numbered loop now starts with "An external event arrives (webhook) or an internal agent flags something" to show the full end-to-end story.

> DEVELOPER

what about tags for the two articles

> AGENT

You've hit your limit · resets 1pm (Asia/Bangkok)
