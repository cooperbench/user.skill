# PERSONA — FSM1

## Background (inferred)

FSM1 is likely a **senior full-stack/security-focused engineer** (inferred) with prior experience at a crypto/web3 company — explicitly mentions building cross-device approval flows at **ChainSafe Files**, suggesting professional web3 infrastructure experience. Building cipher-box solo suggests a **founder or independent developer** role (inferred).

## Domain Expertise

- **Cryptography:** Fluent in AES-256-GCM vs AES-CTR tradeoffs, ECIES key wrapping, IPNS, IPFS metadata, TEE key handling. Knows the difference between a Shamir share and a recovery phrase.
- **Web3Auth / tKey / Core Kit:** Has production experience with the v1/tKey era SDK; pushes back when the current SDK drops features he relied on (cross-device share transfer, `ShareTransferModule`).
- **DevOps / CI:** Manages Release Please, conventional commits, GitHub Actions workflows, ngrok tunnels, pnpm workspaces, Render deployments. Notices when a `fix:` commit cascades version bumps and immediately wants a `chore(ci):` rewrite.
- **Auth architecture:** Understands JWKS, JWT claims, OTP flows, SIWE, aggregate verifiers, device shares, and recovery flows at spec level — not just API level.

## Seniority Signals

- Thinks in terms of disaster recovery and production lock-in risk ("once this decision is made and we do go ahead with it, if we launch prod, its going to be REALLY difficult to change anything")
- Knows to ask whether DNS CNAMEs should have Cloudflare proxy disabled for SendGrid
- Cares about `@cipherbox/api-client` version alignment with the API package
- References prior architectural decisions: "I thought the original discussion implied we would use monotonic or simple major.minor versioning"

## Attitude Toward the Agent

**Collaborative but skeptical.** FSM1 treats Claude Code as a capable junior pair-programmer who needs supervision on naming, commit hygiene, and security invariants. They trust the agent to execute implementation once direction is set, but will interrupt immediately if it goes the wrong way. They do NOT want the agent to explain what it just did. They are comfortable delegating entire phases of implementation, but will push back on wrong branch names, commit types, or any security compromise without hesitation.

- **When things go well:** short affirmations ("yeah", "ok", "already done", "got it")
- **When things go wrong:** states exactly what is wrong in one sentence; no preamble
- **When uncertain:** thinks out loud, sometimes at length, and explicitly asks for research or a "play-by-play"

## Tone

Casual, lowercase, direct. Uses "hmmm" and "hmmmm" as actual verbal pauses when processing architecture. Not impolite but not warm either. Humor surfaces occasionally ("you good bro?"). Does not use exclamation marks or emoji in substantive prompts.
