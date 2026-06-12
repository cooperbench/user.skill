# PROJECTS — FSM1

## FSM1/cipher-box ★ (dominant — 100% of sessions)

**What it is:** A privacy-first encrypted file vault. Users encrypt files client-side (AES-256-GCM) before uploading to IPFS. Keys are managed via Web3Auth Core Kit (MPC-based key derivation). The server never sees plaintext content or unencrypted keys.

**Tech stack:**
- Frontend: React/TypeScript, pnpm workspace monorepo
- Backend (API): Go or Node.js (inferred from JWT/JWKS usage and pnpm api:generate)
- Auth: Web3Auth Core Kit (MPC), custom JWKS endpoint, OTP email login, SIWE (Sign-In with Ethereum)
- Storage: IPFS via Kubo node (host: 192.168.133.114:5001)
- Database: PostgreSQL + Redis (host: 192.168.133.114)
- Email: SendGrid integration (in progress at time of sessions)
- Desktop: Electron app (inferred from "desktop apps" versioning discussion)
- CI: GitHub Actions, Release Please for automated versioning, Render for deployments
- Package: `@cipherbox/api-client` published separately; version must match API version

**Recurring themes:**

1. **MFA / Key stability (Phase 12):** The dominant ongoing work. Implementing multi-factor authentication with Web3Auth Core Kit (formerly PnP Modal → Core Kit migration). Architectural debate about SIWE for wallet users, aggregate verifiers, cross-device approval flows, Shamir secret sharing, key recovery disaster scenarios.

2. **CI / Release Please plumbing:** Significant effort keeping the automated versioning pipeline working. Common issues: wrong commit prefixes triggering cascade version bumps, `fix:` vs `chore(ci):` collisions, Release Please branch commit strategies, post-release target job failures.

3. **GSD planning system:** The codebase has a full `.planning/` directory with phases, milestones, roadmap, STATE.md, quick tasks. FSM1 uses slash commands (`/gsd:*`) to orchestrate agent work.

4. **Security reviews:** Custom `/security:review` command runs against PRs. Invariants enforced: no private keys in localStorage/sessionStorage, no logging of sensitive keys, always ECIES for key wrapping, always AES-256-GCM for content, server never has plaintext.

5. **AES-CTR streaming encryption:** Planned for v1.1 (M2). Deferred but on roadmap. FSM1 asked whether it was implemented; it was not; he wants it added to M2 as a phase.

6. **Sidebar / UI consistency:** Periodic quick tasks for UI polish — icon consistency (custom SVG vs icon library), matrix background effect visibility.

**Phase context (at time of sessions):**
- M1: Shipped (2026-02-11), 72 plans across 17 phases
- M2: Active, targeting Production v1.0 (Phases 11–17 + decimal insertions)
- Phase 12 (Multi-Factor Authentication): Key focus area; multiple sessions
- Phases 38, 39: Had PRs but no summary stubs; FSM1 provided PR links to create them

**Versioning philosophy:**
- API package: semver (Release Please managed)
- `@cipherbox/api-client`: version must match API version exactly
- Web/Desktop apps: FSM1 initially wanted monotonic/major.minor versioning ("semver doesn't make much sense for these sorts of apps") but accepted semver for now
