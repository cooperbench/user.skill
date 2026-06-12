# PREFERENCES — FSM1

## What Triggers Pushback (correction rate: 39.1%)

**Commit and branch naming precision:**
- Wrong branch names ("feat/phase-12-mfa" when the real name is `feat/phase-12-multi-factor`)
- Wrong conventional commit prefixes — `fix:` when `chore(ci):` is correct, generic `feat:` when `feat(api):` is needed
- Commits that cascade unnecessary version bumps
- Overly verbose PR changelogs

**Security invariants:**
- Storing any PII (email address) in localStorage — stops the agent immediately regardless of where in implementation
- Any deviation from encryption rules: no unencrypted keys to server, no plaintext private keys in storage
- Assumes these rules are always in scope; doesn't need to repeat them session to session

**Scope and branch targeting:**
- PRs branched from `main` when they should branch off a feature branch
- CI/Release Please configuration mistakes that break automated versioning
- Files or changes committed to the wrong component package

**Excessive output:**
- Over-explained changelogs or summaries
- Running the wrong slash command or misidentifying a command
- Proposing research phases when the direction is already clear

## What Satisfies FSM1

- Correct conventional commit format on the first try
- Agent that remembers branch topology without being reminded
- Security review that actually checks against stated invariants
- Research that answers exactly what was asked — no padding
- Execution without preamble: just do it, no "I'll now proceed to..."
- When the agent says "already on `feat/phase-12-multi-factor`" after being corrected once

## Workflow Habits

**Planning first:** Uses a full GSD (Get Shit Done) planning system with phases, milestones, roadmap, and STATE.md. Plans are written before coding. `/gsd:plan-phase`, `/gsd:quick`, `/gsd:fast` are the entry points.

**Commit cadence:** Atomic commits per logical change. Uses conventional commits strictly. PR per phase is the norm. Uses Release Please for automated versioning.

**Testing:** Runs e2e tests in headed mode locally for visual verification. CI must pass before merging. Mentions CI failures by linking to specific GitHub Actions run URLs. Does not ask for unit test coverage without reason.

**Does he want explanations or just results?** Results first, explanation only when directly asked ("can you give me the play-by-play?"). If the agent summarizes what it just did unprompted, FSM1 will not acknowledge it and just issue the next command.

**Research integration:** Will ask for research when genuinely uncertain ("could you do some research in to how it was implemented in tkey"). Expects the research output to be synthesized into a concrete recommendation, not just a list of findings.

**Tool/stack preferences:**
- pnpm workspaces
- Conventional commits + Release Please
- GitHub Actions for CI
- Render for staging/preview deployments
- ngrok for local tunnel exposure
- Cloudflare for DNS
- SendGrid for email
- Web3Auth Core Kit (prefers control over convenience)
- IPFS / Kubo for decentralized storage
- PostgreSQL + Redis on host (192.168.133.114 in local dev)

## Pushback Distribution

| Type | Rate |
|---|---|
| Non-pushback (accepts) | 52.5% |
| Correction | 39.1% |
| Failure report | 6.7% |
| Takeover (just does it himself) | 1.1% |
| Rejection | 0.6% |

Corrections are almost always about naming, scope, or security. Failure reports are CI/runtime issues passed back to the agent. Takeover is rare — happens when the agent is visibly stuck and FSM1 just issues the corrective command himself (e.g., `git switch main && git pull`).
