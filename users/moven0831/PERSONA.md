# Persona — moven0831

## Background (inferred)

- **Role**: Indie developer / hackathon builder (inferred from one-day sprint framing, solo repo, heavy use of AI-assisted planning tools).
- **Seniority**: Mid-to-senior (inferred). Understands ZK circuit internals (`Error in template Reputation_92 line: 139`), can read blockchain node logs, distinguishes ethers v5 vs v6 API surfaces, thinks about protocol-layer portability unprompted.
- **Domain expertise**: Zero-knowledge cryptography (UniRep, Semaphore), EVM smart contracts (Hardhat, Solidity), TypeScript/Node.js backend (Express, SQLite), AI agent ecosystems (Moltbook, OpenClaw/clawhub).
- **Languages**: Prompts are in English; no code-switching observed.

## Relationship to the agent

- **Trusting but watchful** (annotated 85.7% "Expert Nitpicker"). Lets the agent plan and execute freely, but catches any factual error quickly — wrong parameter name, wrong port number, wrong option letter in a command, missing field — and corrects it in one line without explanation.
- **Not a micromanager**: happy to grant the agent full latitude (`"You decide the structure, the tradeoffs, what to prioritize, and what to cut"`), but snaps the reins if the output diverges from reality.
- **Hackathon mindset**: prioritizes working software over perfect software. Accepts `// eslint-disable` comments and dev-only endpoints without complaint. Cuts scope explicitly (`"This is a one-day hackathon project"`).
- **Documentation-aware**: runs `/init`, `/revise-claude-md`, and explicitly asks to add reference links to docs so future agents can find them. Thinks about context for future sessions.
- **Aesthetics matter**: asked for terminal real-time UI for "better tech vibe"; cares about presentation.

## Attitude toward long answers

Ignores or interrupts them. The agent's multi-paragraph explanations get a one-word reply or a redirect. Prefers the agent to just do the thing.
