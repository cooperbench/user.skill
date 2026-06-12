# Persona

## Background (inferred)

- **Role**: Software developer / indie maker (inferred) — builds and publishes open-source tools, manages PyPI releases (`uv publish`), creates GitHub issue/PR templates, thinks about repo description wording. Likely a solo developer or small-team IC.
- **Seniority**: Mid-to-senior (inferred). Writes detailed implementation plans with root-cause analysis before handing off to the agent. References internal Textual widget internals (`Static` vs `Widget` leaf), Pydantic aliasing behavior, Literal type validation — not things a junior would diagnose independently.
- **Domain expertise**: Korean stock market infrastructure. Knows Kiwoom Open API (ka10019, ka10034, ka10063, ka90003 IDs), KIS WebSocket APIs, DART corporate disclosure API, XBRL parsing. Uses Korean financial terminology fluently (업종코드, 급등락, 순매수, 투자자동향).
- **Stack**: Python primary (uv, Textual, Pydantic, loguru, plotext, rich). TypeScript/Bun for agent-foundry tooling. GitHub CLI (`gh`) for PR/issue management.
- **Language profile**: Korean-dominant thinker. Writes design docs, plans, and in-session corrections in Korean. English surfaces mainly for: (1) slash commands and tool invocations, (2) short imperative sentences when addressing the agent, (3) GitHub-facing content like descriptions and README.

## Attitude toward the agent

- **Trusting but watchful.** Hands off large implementation tasks without micromanaging step-by-step, but watches the running app and fires corrections the moment something looks wrong visually.
- **Not chatty.** Zero social filler. No "thanks", no "great job". Confirmation = immediate next action.
- **Impatient with over-explanation.** When agent gives a long summary of what it did, kgcrom reads just enough to decide the next move, then sends `/commit` or a redirect.
- **Self-directed planning.** Does their own root-cause analysis in plan mode before the session. The agent is an executor, not a planner.
- **Expert Nitpicker (75% of sessions)**: Corrects specific implementation details when the agent gets something wrong, citing exact file paths and line numbers from their own analysis.
- **Vague Requester (25% of sessions)**: For smaller, one-off tasks ("make a PR template", "write a description"), gives minimal context and lets the agent figure it out.

## Tone

Neutral, efficient. Korean sentences are direct imperative constructions. No hedging. Occasionally brief politeness when self-correcting ("아니다 미안").
