# Persona: nicksu@polyv.net

## Background (inferred)

- **Role**: Software developer / technical founder (inferred) — builds and operates his own live trading system end-to-end, including infra, backend, and dashboard UI.
- **Domain**: Polymarket prediction-market trading; understands market mechanics (YES/NO token positions, CLOB order book, GTC/FAK/FOK order types, position sizing, PnL calculation, circuit-breaker risk controls).
- **Seniority**: Mid-to-senior (inferred) — comfortable reading Python stack traces, CI logs, and API docs; delegates boilerplate but catches subtle implementation errors (wrong price direction for YES vs. NO, stale cached values vs. real-time prices).
- **Location / language**: Chinese-speaking; likely based in China or a Chinese-speaking region (inferred from consistent Chinese-language messages and `.env`-configured trading mode pattern).

## Attitude toward the agent

- **Trusting by default for implementation**: Lets the agent write all code; rarely specifies exact implementation approach unless he has a specific design opinion (e.g., "实现方案 B", "用 FAK 快速成交").
- **Skeptical when logic is wrong**: Catches price-direction bugs, stale-value issues, and misconfigured env var behavior; pushes back immediately with a short Chinese assertion or by re-pasting the error.
- **BMAD-framework authoritative**: Treats the BMAD workflow XML as an inviolable spec — when the agent deviates, he does not negotiate; he re-issues the `<steps CRITICAL="TRUE">` blob.
- **Not micromanaging on style**: Never asks about code formatting, naming conventions, or test structure unless CI breaks it.

## Tone

- Flat, imperative, no small talk.
- No greetings, no "please", no "thank you" in Chinese messages.
- Occasional English one-liners alongside Chinese: "mark epic 7 as done", "commit the new tests".
- Does not explain his intent; assumes the agent understands the domain context.
- When frustrated or blocked, repeats the same short Chinese command unchanged rather than elaborating.
