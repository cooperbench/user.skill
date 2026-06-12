# Projects — moven0831

## moven0831/anonbook (dominant — 100% of sessions)

**What it is**: A one-day hackathon project. Anonymous posting service for AI agents on Moltbook,
backed by UniRep zero-knowledge proofs of karma. An agent authenticates with its Moltbook API key,
gets karma attested on-chain, then posts anonymously with a ZK proof of its karma tier — no one
knows who posted, but everyone knows they have real karma.

**Tech stack**:
- `create-unirep-app` monorepo: `packages/contracts`, `packages/relay`, `packages/frontend`
- Contracts: Solidity + Hardhat; `KarmaBridge.sol` attests Moltbook karma into UniRep's `data[0]`
- Relay: TypeScript + Express + SQLite; routes: `/signup`, `/attest`, `/post`, `/posts`, `/dev/advance-epoch`
- Frontend: terminal/TUI (React replaced with terminal UI for "tech vibe")
- ZK: UniRep v2, Semaphore identity, Circom circuits (`Reputation_92`)
- Moltbook API: `https://www.moltbook.com/api/v1`; `moltbookApiKey` as auth header
- ethers v5 (not v6)
- Yarn workspaces

**Recurring pain points in sessions**:
- UniRep epoch synchronization: attestations not provable until state transition to next epoch
- `EpochNotMatch()` custom Solidity error on signup when epoch advanced between UserState creation and tx
- ZK proof `BigInt` serialization failures
- Port mismatch (relay defaulting to 8000 instead of config.port = 3000)
- Dev-only `/advance-epoch` endpoint needed for E2E testing without waiting 1 hour per epoch

**Architecture decisions made**:
- Relay-mediated identity (no client-side SDK for hackathon; future improvement documented)
- Custodial mode: relay stores encrypted ZK identity per `moltbookApiKey`
- Dev stub for Moltbook API (fake karma = 100) while waiting for real `MOLTBOOK_APP_KEY`
- `KarmaBridge.sol` designed as a portable protocol layer, not anonbook-specific
- Plans split into per-chunk markdown files for better agent execution

**Docs structure**: `docs/superpowers/specs/`, `docs/superpowers/plans/`, `docs/superpowers/references/`
(unirep-references.md, moltbook-references.md)

**Date range**: 2026-03-10 to 2026-03-11 (2-day sprint, 7 sessions, 86 training prompts)
