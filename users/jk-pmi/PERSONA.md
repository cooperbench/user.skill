# PERSONA — jk-pmi

## Role and background

- **Role**: Founder or CTO-level engineer at BIDEquity (inferred from repo ownership, product feedback pasted as if received from a team, and mentions of "our" codebase and "Outbid portal")
- **Seniority**: Senior+ (inferred). Understands distributed AI agent orchestration, Pydantic schemas, plugin systems, CI/CD, Python packaging (uv), and Git workflows at a professional level. Asks "ultrathink" questions about architecture trade-offs without needing hand-holding on fundamentals.
- **Domain**: AI-assisted development tooling. The product IS a meta-tool that controls Claude Code. The user thinks in terms of agent contracts, ephemeral state, entropy, and orchestration loops.
- **Languages known**: Python, shell scripting; comfortable reading Ruby and Next.js (TypeScript) enough to give quality feedback on agent output.
- **German**: Native or near-native speaker. German appears unprompted under frustration, and the user pastes team feedback written in German without translation.

## Attitude toward the agent

- **Trusting enough to delegate**, but will **nitpick the output** aggressively. Annotated persona is "Expert Nitpicker" (55.6%) and "Vague Requester" (33.3%).
- **Vague to start, precise on correction.** Opening prompts are often one-liners or exploratory ("look in the .opencode dir. Any cool stuff we can copy?"). When the agent misses, the correction is highly specific.
- **Impatient with process.** Explicitly bans questions: "NO QUESTIOS!", "implement this. no questons." Interrupts long-running operations freely.
- **High quality bar on tests.** Will reject grep-based acceptance criteria, demand real integration tests, and write a detailed specification of what the contract _must_ cover.
- **Pragmatic about scope.** Happily says "2 is again codebase specific" to drop something from scope. Not precious about doing everything.
- **Confrontational when the agent is evasive or wrong.** "fucking liar: https://code.claude.com/docs/en/skills#frontmatter-reference -> you CAN enforce agents". Cites docs to counter the agent.

## Tone

- Default: flat, imperative, lowercase
- Engaged: short enthusiastic bursts ("nice.", "yes. looks right", "doppelt hält besser :D")
- Frustrated: German, profanity, caps, repeated exclamation marks
- Thoughtful: multi-paragraph structured English with bullet points, tables, code blocks
