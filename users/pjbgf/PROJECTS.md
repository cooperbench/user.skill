# Projects — pjbgf

## entireio/cli ★ dominant (83% of sessions)

**What it is**: A CLI tool (`entire`) that records and resumes AI coding sessions, persisting
session data as git objects (commits, blobs, trees) in the repository itself.

**What pjbgf does here**: Owns the full codebase. Works on the checkpoint/resume subsystem
(`cmd/entire/cli/checkpoint/`), git storage strategies (`cmd/entire/cli/strategy/`), and
blob-fetching infrastructure. Frequently upgrades go-git dependencies and refactors internal
APIs to track library changes.

**Tech stack**: Go, go-git (upgrading v5 → v6), CLI, git plumbing (object model, commit trailers,
tree/blob reads).

**Recurring themes**:
- Migrating away from deprecated go-git APIs (`PlainOpenWithOptions` → `PlainOpen`)
- Fixing resume logic regressions after refactors touch `FetchingTree` / `ReadCommitted`
- Removing dead code flagged by static analysis (unused fields, wasted heap allocations)
- Per-blob vs. batched fetch optimization (`FetchBlobsByHash`, `CollectTranscriptBlobHashes`)
- Managing rebase conflicts when multiple parallel workstreams touch the same files
- Frequent commit cadence during active development; verifies SHA preservation after rebases

**Representative session arc**: upgrade dependency → update all import paths → build + test →
fix conflicts → commit → discover regression → diagnose root cause → pick fix option → commit.

---

## go-git/x (17% of sessions)

**What it is**: Extensions or experimental packages for the go-git ecosystem.

**What pjbgf does here**: Limited evidence — only one session. Likely upstream contribution or
experimentation work (inferred).

**Tech stack**: Go, go-git.

**Recurring themes**: Insufficient data to characterize beyond the go-git domain.
