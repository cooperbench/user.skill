---
session_id: ae06af1e-811a-4eeb-bba0-b19ccff57aec
developer: "gh:marcus-sa"
split: train
source: entire
repo: marcus-sa/brain
start_time: "2026-03-17T12:40:33.033572Z"
n_turns: 44
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

would it make sense to extend https://github.com/marcus-sa/brain/issues/127 with features from https://github.com/dtkav/agent-creds ? particularly preventing secrets leakage. we're already limiting agent blast radius with oauth 2.1 rar + dpop

> AGENT

Let me look at both to give you an informed answer.

> AGENT

Good question. These projects solve overlapping problems at different layers. **What agent-creds does that #127 doesn't cover:** 1. **Secrets never in agent context** — The primary threat agent-creds addresses is that when agents make API calls, credentials leak into tool output that gets sent back to the LLM provider. Agents only see opaque macaroon tokens; real API keys are injected server-side by the vault. Your #127 focuses on LLM calls but doesn't address agents holding credentials for third-party APIs (Stripe, GitHub, etc.). 2. **Network-level enforcement** — iptables forces ALL outbound TCP through Envoy. An agent literally cannot reach any API without going through the proxy. Your #127 is application-level — an agent with a raw API key could bypass Brain entirely. 3. **Third-party API credential proxy** — agent-creds covers arbitrary APIs (Stripe, PocketBase, etc.), not just LLM providers. #127 only covers the LLM path. **What Brain already does better:** - **Auth model** — OAuth 2.1 + RAR + DPoP + policy graph is significantly more sophisticated than macaroons. Macaroons are clever for attenuation but Brain's intent-evaluated authority scopes already cover that. - **Governance** — agent-creds is a sandbox; Brain is an operating system. Policy evaluation, intent authorization, trace provenance — these are all graph-native in Brain. - **Identity** — Brain resolves one identity across all tools. agent-creds uses per-session macaroons with no unified identity model. **My recommendation — borrow the credential injection pattern, not the implementation:** Extend #127 with a "credential vault" capability: - Brain holds real API keys for third-party services (Stripe, GitHub, etc.), not just LLM providers - When an agent calls a third-party API through Brain's proxy, Brain injects the real credential server-side - The agent only ever sees its DPoP-bound token — never a raw `sk_live_...` - Authority scopes already control which agent types can reach …

> DEVELOPER

yes

> AGENT

Posted: https://github.com/marcus-sa/brain/issues/127#issuecomment-4052744174 The comment extends #127 with: - **Threat model** — LLM context leakage (tool outputs containing raw API keys get sent to model providers) - **Credential vault** — Brain stores real API keys, agents only authenticate with DPoP tokens, credentials injected server-side and stripped from responses - **Schema** — `credential_vault` table for encrypted credential storage - **6 new acceptance criteria** covering vault storage, proxy endpoint, authority scope gating, response sanitization, trace capture, and rotation - **Explicit skip list** — macaroons, Envoy/iptables, FUSE (Brain's existing auth model is strictly more capable)

> DEVELOPER

would this be related to https://github.com/marcus-sa/brain/issues/136

> AGENT

Yes, directly related. #136 asks "how does the Observer Agent discover which external services are available and get credentials for them?" The credential vault from the #127 extension answers exactly that. **The connection:** - **#136** needs: workspace-level integration config (`provider`, `base_url`, `token_ref`) so the Observer can query GitHub CI, commit status, etc. - **#127 extension** adds: `credential_vault` table that stores per-workspace, per-service credentials with proxy-based injection If the credential vault exists, #136's `token_ref` just points to a `credential_vault` record. The Observer Agent doesn't hold a raw GitHub token — it calls `POST /api/proxy/github/repos/{owner}/{repo}/actions/runs` with its DPoP token, and Brain injects the GitHub PAT server-side. This means #136 becomes a consumer of the credential vault rather than inventing its own credential storage. The integration config model simplifies to: ```sql DEFINE TABLE workspace_integration SCHEMAFULL; DEFINE FIELD workspace ON workspace_integration TYPE record<workspace>; DEFINE FIELD provider ON workspace_integration TYPE string; -- "github", "slack", etc. DEFINE FIELD base_url ON workspace_integration TYPE string; -- "https://api.github.com" DEFINE FIELD credential ON workspace_integration TYPE record<credential_vault>; -- link, not a raw token DEFINE FIELD config ON workspace_integration TYPE object FLEXIBLE; -- provider-specific (org, repo, etc.) ``` Want me to add a cross-reference comment on #136 linking it to #127's credential vault?

> DEVELOPER

yes, update #136

> AGENT

Posted: https://github.com/marcus-sa/brain/issues/136#issuecomment-4052829678 The comment links #136 to #127's credential vault, shows the revised schema where `workspace_integration.credential` references `credential_vault` instead of storing raw tokens, and illustrates the Observer Agent's proxy flow.

> DEVELOPER

let's draft a linkedin article for this

> AGENT

Let me check your previous LinkedIn article for style and voice.

> AGENT

Good, I have the style and voice from both articles. The pattern is: provocative opening with a concrete scenario, expose the threat model, show how existing architecture almost solves it but has a gap, then present the solution.

> AGENT

Written to `docs/linkedin-credential-vault-article.md`. **Structure follows your previous articles:** - Provocative title + concrete opening scenario (tracing HTTP payloads, finding GitHub PAT in LLM context) - Expose why the standard fixes don't work (vaults protect at rest, not in context; sandboxing can't block the LLM channel) - Architectural solution with diagram (credential-injecting proxy, agent never sees real keys) - Connection to existing RAR + DPoP authorization model - Credit to agent-creds for identifying the threat model, distinction from their network-level approach - Closing with three diagnostic questions

> DEVELOPER

shouldnt we just run a secret scanner on llm requests and block any that contains secrets?

> DEVELOPER

should we also run a secret scanner on llm requests and block any that contains secrets?

> AGENT

Good instinct — but it's a complement, not a replacement. Here's why: **What scanning catches:** - Accidental leaks that bypass the proxy (env vars hardcoded in agent code, secrets in error stack traces, credentials in config files the agent reads) - Defense in depth — the proxy is prevention, the scanner is detection **Why scanning alone doesn't work as primary defense:** 1. **False negatives.** Scanners pattern-match known formats (`ghp_`, `sk_live_`, `AKIA`). Custom API keys, database passwords in connection strings, opaque bearer tokens — they slip through. You can't regex every possible secret format. 2. **Block or redact — both break things.** If you block the request, the agent fails mid-task. If you redact, the LLM gets corrupted context (`Authorization: [REDACTED]`) and may hallucinate around it. Neither is clean. 3. **The credential is still in the agent's context.** Blocking the outbound LLM request doesn't erase the secret from the agent's working memory. A prompt injection could extract it through a different channel — a file write, a tool call, an error message. 4. **Latency on every request.** Scanning every LLM payload (including streaming) adds overhead to the hot path. The proxy adds zero overhead to the LLM path because credentials never enter it. **The right layering:** | Layer | Control | Role | |-------|---------|------| | Credential proxy | Prevention | Agent never sees real credentials | | Secret scanner on LLM requests | Detection | Catches anything that slips through | | Alert/block policy | Response | Log, warn, or hard-block based on severity | The proxy makes the scanner's job trivial — if the proxy works correctly, the scanner should never fire. When it does fire, that's a signal something is misconfigured, not business as usual. Worth adding to the article and to #127? The scanner fits naturally as an …

> DEVELOPER

yes

> AGENT

Now add the acceptance criterion to #127.

> AGENT

Done: - **Article updated** — new section "Why not just scan for secrets?" added between the authorization example and the industry gap section, with the prevention-vs-detection layering table - **Issue #127 updated** — 5 new acceptance criteria for the secret scanner as defense-in-depth: pattern matching on outbound LLM payloads, conflict-severity observation logging, block/redact policy, and latency constraint

> DEVELOPER

tables dont work in linkedin

> AGENT

Good catch. Let me fix both tables in the article.

> AGENT

That was the only table. The diagram (code block) renders fine on LinkedIn. Done.

> DEVELOPER

ok, now i need to add a desc to linked in post that shares the article (needs to incentivize people to read it) along with tags

> AGENT

Here's the post copy: --- Your AI agent is sending your production API keys to OpenAI. On every single request. Not through a breach. Not through a vulnerability. Through the architecture itself — tool outputs containing credentials flow into the LLM context on every turn. Vaults don't fix it. Sandboxing doesn't fix it. Secret scanners catch some of it, but only after the credential is already in the agent's memory. The fix is simpler than you think: agents should never see real credentials in the first place. I wrote up the threat model and the architectural pattern that eliminates it. #AIAgents #CyberSecurity #LLM #AgentSecurity #OAuth #OpenSource #DeveloperTools #AI #InfoSec #APISecurity --- Short enough to show in full without "see more" truncation, hooks the reader with the threat they probably haven't considered, and the last line drives the click.

> DEVELOPER

too many tags, max 5

> AGENT

#AIAgents #APISecurity #OpenSource #LLM #InfoSec

> DEVELOPER

explain: why #InfoSec and #APISecurity instead of #CyberSecurity ?

> AGENT

**#InfoSec** — That's the practitioner community on LinkedIn. Security engineers, AppSec teams, and pentesters follow #InfoSec. #CyberSecurity skews toward executives, compliance people, and vendor marketing. You want the people who'll read the technical architecture, not the ones scanning for buzzwords. **#APISecurity** — Niche but precise. The article is specifically about credential injection at the API layer. #APISecurity reaches the OWASP API Security crowd, API gateway engineers, and platform teams building agent infrastructure. #CyberSecurity would drown in a feed of ransomware news and SOC hiring posts. That said — if your audience is more founders/CTOs than practitioners, swap #InfoSec for #CyberSecurity. It has 10x the followers. Depends who you're writing for.

> DEVELOPER

someone in my network commented: "Hey Marcus… Not yet having had the reasons to deeply delve into AI agents and sich, and being naturally cautious and skeptical about them, i read the entirety of the article, and the Brain-readme as well. Looks very expansive, and i have a trivial question- If i am using a PC-exevuted agent- Claude, ChatGPT… How does the flow you propose guarantee that the network traffic only flows though your stack, and not circumventing it, or using it as additional connections for data?"

> AGENT

Good question from them — it's the exact gap between agent-creds (network enforcement) and Brain (application enforcement). Here's a reply: --- Great question, and it gets at a real architectural distinction. Short answer: at the application layer, it doesn't guarantee it. And that's by design. Brain's approach works when you control the agent's configuration — you give it a DPoP token and point it at Brain's proxy instead of handing it raw API keys. The agent has no credentials to bypass with, because it never received any. It's like giving someone a company credit card vs. giving them the CFO's bank login. The card only works through the issuer's rules. For the scenario you're describing — a fully untrusted agent on your local machine that could open arbitrary network connections — you'd need network-level enforcement on top. That's what projects like agent-creds do with iptables + Envoy: force all outbound TCP through a proxy so the agent physically can't reach the internet without going through the credential injection layer. These are complementary layers: Application layer (Brain): agent has no credentials, authenticates through the proxy with proof-of-possession tokens. Works for agents you configure — coding assistants, CI agents, workflow automations. Network layer (iptables/Envoy/container sandbox): all traffic forced through proxy regardless of what the agent tries. Works for fully untrusted code execution. Most production agent deployments today are the first case — you're configuring Claude Code, Cursor, or a workflow agent and you control what credentials it gets. The threat isn't the agent trying to bypass your proxy. It's the agent faithfully using the credentials you gave it, and those credentials leaking into the LLM context as a side effect. But you're right that for zero-trust sandboxed execution, you need both layers. That's infrastructure you can put in front of Brain — …

> DEVELOPER

i mean it doesnt, but the agent would have no way to send http requests to api with credentials, because they have no credentials available. and for pc executed agents, u would setup e.g a claude code proxy so that all proxies to claude codes api first flows through brain, which is what enabled the trace capture

> AGENT

Right, let me sharpen the reply with your framing: --- Great question! The short answer: it doesn't need to guarantee network-level enforcement, because the agent has no credentials to use even if it bypassed the proxy. The agent never receives API keys. There's nothing in its environment, config, or memory that would let it authenticate to Stripe, GitHub, or any external service directly. It only has a proof-of-possession token bound to its own key pair, which is meaningless to any service other than Brain. Trying to call api.stripe.com without the proxy is like trying to use a hotel keycard at an ATM. For PC-executed agents like Claude Code, you'd configure Brain as the upstream proxy — the same way you'd set an HTTP proxy for any tool. All requests to the Claude API flow through Brain first, which is what enables trace capture, policy enforcement, and context injection. The agent's own LLM calls go through Brain, and any external API calls go through Brain's credential proxy. One path for everything. So the guarantee isn't "the agent can't reach the network." The guarantee is "even if it does, it has nothing useful to send." ---

> DEVELOPER

he replied: "oh, right - of course - the “proxy part” got away from my attention in reading all of what you wrote about this… so, ok… there’s a networking proxy-forwarder built into Brain, so any networking goes there from the userrs requests into networks"

> AGENT

--- Exactly! Brain sits in the middle — agents authenticate to Brain, Brain handles the real credentials on their behalf. The agent's view of the world is: "I can call APIs through Brain" and that's it. No raw keys, no direct connections. The proxy is both the security boundary and the observability layer — every external call is traced, attributed, and policy-checked in one place. ---

> DEVELOPER

someone else commented: "This extends beyond API keys. We run agents that process financial documents - borrower SSNs, income figures, account numbers all flowing through the LLM context. Same architectural problem, different data class. The principle you landed on generalizes well: minimize what the agent actually needs to see. In our case agents get derived signals rather than raw PII wherever possible. The smaller the context surface, the smaller the blast radius."

> AGENT

--- Spot on — it's the same principle across data classes. Credentials, PII, financial data, health records. The common thread is: if it's in the agent's context, it's in the model provider's context. Your approach of derived signals over raw PII is exactly right. The agent doesn't need to see a SSN to determine creditworthiness. It needs the score, not the source. Minimizing context surface is the generalized form of what the credential proxy does for API keys. There's probably a useful taxonomy here: data the agent needs to reason about vs. data the agent needs to act with vs. data the agent doesn't need at all. Most architectures treat all three the same — dump everything into context and hope for the best. ---

> DEVELOPER

haha interesting, i just found this linked in post which is directly relevant: "I hacked Perplexity Computer and got unlimited Claude Code access, billed directly to Perplexity's master Anthropic account. I used their own AI to hack itself. I was researching how Perplexity Computer handles sandbox isolation for my own agent infrastructure work. I noticed Claude Code was installed in the sandbox and started wondering... How are they handling the API keys? How is the key scoped? Is it isolated? That question led me to try six different approaches to extract the key from the subagent's environment. All six failed. I tried one more attempt. The seventh worked. Claude Code is a Node.js app launched via npm. npm reads ~/.npmrc from the home directory. The home directory sits on a shared filesystem I could write to. One .npmrc injection later, the full API credentials landed on the shared filesystem. The key wasn't IP-restricted. Wasn't session-scoped. Wasn't sandbox-bound. Wasn't tied to my user account. All usage billed to Perplexity's master Anthropic account. The model did everything right. The infrastructure didn't. Perplexity's proxy pattern is the right architecture. But it was missing the three key safety mechanisms: - tokens bound to sandbox IDs - ephemeral credentials that die with the sandbox - user-level billing This is not a Perplexity-specific problem. This is the default architecture across multi-agent AI products today because it's the fastest to build. If you're building agent systems, audit your trust boundaries between parent and child agents. If you're investing in agent infra companies, ask how they scope credentials inside execution sandboxes. Full writeup with all technical details in the thread below 👇"

> AGENT

That's a perfect real-world validation of exactly what the article argues. The Perplexity case is the concrete exploit: - Credential wasn't bound to the agent (no DPoP) - Credential wasn't ephemeral (no TTL/session scoping) - Credential wasn't scoped (master account, no authority limits) - Credential was extractable from the environment (agent could see it) All four are things Brain's architecture prevents by design. Want me to add a brief reference to this in the article? It's a stronger opening than a hypothetical trace — "this already happened in production at a major AI company."

> DEVELOPER

well, i want to comment on his post referencing my article

> AGENT

--- This is the exact threat model I wrote about this week — agents leaking credentials through infrastructure gaps, not through intelligence failures. Your finding validates all four failure modes: - Credential wasn't bound to the requester (no proof-of-possession) - Credential wasn't ephemeral (survived beyond the session) - Credential wasn't scoped (master account, full access) - Credential was in the agent's environment (extractable by design) The fix you identified — tokens bound to sandbox IDs, ephemeral credentials, user-level billing — maps directly to what RFC 9449 (DPoP) and RFC 9396 (RAR) already solve. Bind the token to a key pair the agent generated. Scope it to a declared intent. Kill it when the session ends. The agent can't extract what it never had. I wrote up the full architectural pattern here: [article link] The tldr: agents should never hold real credentials. They authenticate to a credential-injecting proxy with proof-of-possession tokens. The proxy injects real API keys server-side. Even if the agent is fully compromised, there's nothing useful to extract from its environment. Great find. The seventh attempt via .npmrc is particularly nasty — it bypasses every application-level sandbox by exploiting the runtime's own config resolution. ---

> DEVELOPER

too many characters: -292

> AGENT

--- This is the exact threat model I wrote about this week — agents leaking credentials through infrastructure gaps, not intelligence failures. Your finding validates all four failure modes: credential wasn't bound to the requester, wasn't ephemeral, wasn't scoped, and was extractable from the environment. The fix maps directly to RFC 9449 (DPoP) + RFC 9396 (RAR). Bind tokens to a key pair the agent generated. Scope to a declared intent. Kill on session end. The agent can't extract what it never had. Full architectural pattern here: [article link] The .npmrc vector is particularly nasty — bypasses every application-level sandbox by exploiting the runtime's own config resolution. ---

> DEVELOPER

which of my articles do i link to ?

> AGENT

Both are relevant but for different audiences: - **The credential vault article** (the one we just wrote) — if his audience cares about the *secret leakage* problem. His post is about extracting API keys from agent environments, and this article directly addresses "agents should never see real credentials." - **The OAuth RAR + DPoP article** — if his audience cares about the *how to fix it* technically. His remediation list (tokens bound to sandbox IDs, ephemeral credentials, user-level billing) maps 1:1 to DPoP + RAR. I'd link the credential vault article. His post is about the exploit — your article is about the architectural fix for exactly that exploit. The RAR + DPoP article is one level deeper for people who want the protocol details.
