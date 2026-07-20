> SYSTEM

# AGENTS.md instructions for /home/<USER>/code/evorto

<INSTRUCTIONS>
# Repository Guidelines

## Context Discipline

- Keep repository knowledge in small, relevant files.
- Use this file as the map, not the full manual.
- Read the nearest applicable guidance before editing:
  - root product/system context
  - module-level `AGENTS.md`
  - local README files
- Update context files when reality changes, assumptions are invalidated, or new constraints are discovered.
- Prefer small, accurate updates over large stale manuals.

## Root Context Files

- `PRODUCT.md` - product goals, personas, core workflows, domain concepts, and product invariants.
- `ARCHITECTURE.md` - high-level system shape, architectural boundaries, and where to look first for common changes.
- `QUALITY.md` - behavior-focused verification guidance, Browser/Playwright expectations, and done criteria.

Keep these files concise. Put implementation-specific guidance in the nearest module-level `AGENTS.md` or README.

## Project Structure

- App code: `src/app/**`
- Server runtime and APIs: `src/server/**`
- Data layer: `src/db/**`
- Shared contracts/types/utilities: `src/shared/**` and `src/types/**`
- Unit tests: `*.spec.ts` in `src/**`
- Playwright tests: `tests/**`
- Legacy e2e reference: `e2e/**`
- Assets/public: `public/`
- Theming: `src/styles.scss` and `_theme-colors.scss`

Start with the nearest applicable module guidance:

- `src/app/AGENTS.md`
- `src/server/AGENTS.md`
- `src/db/AGENTS.md`
- `tests/AGENTS.md`

More specific guidance may exist deeper in […]

> DEVELOPER

Update our checkout to the latest from remote

> AGENT

I’ll first check the current branch and worktree state, then use the repo’s conservative update path so we don’t overwrite local work.

> TOOL

tool_use exec_command
id: call_d9CAIMgs7o1sN249SKzTCHWV
```json
{
  "cmd": "rg -n \"update-evorto-branch|latest changes|git fetch|FETCH_HEAD\" /home/<USER>/.codex/memories/MEMORY.md",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_kr0pl2m2Nm8eat9FGMhPWG8f
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_DhC1cUEb285lqgmYc0iUaEqB
```json
{
  "cmd": "ls skills/update-evorto-branch && sed -n '1,220p' skills/update-evorto-branch/SKILL.md",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_d9CAIMgs7o1sN249SKzTCHWV
```
Chunk ID: 4d4869
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 207
Output:
246:- bun outdated --json, angular-22, typescript-6, node-24.15.0, @types/pg, TS7016, git rebase --onto FETCH_HEAD, codex/pr62-split-06-browser-transport-blocker, PR 76, chore: refresh dependencies and vendored sources
269:- For stacked PRs, check `git rev-parse`/`merge-base` before rebasing; when the base has advanced, `git rebase --onto FETCH_HEAD <old-base-commit>` is the safe shape for replaying only the dependency-refresh commit onto the fetched PR62 tip. [Task 1]
277:- Symptom: rebasing onto the refreshed PR62 base replays the old base commit and creates conflicts. Cause: a broad/plain rebase targeted the wrong commit range. Fix: abort and rebase only the dependency-refresh commit with `git rebase --onto FETCH_HEAD <old-base-commit>`. [Task 1]
417:- Related skill: skills/update-evorto-branch/SKILL.md [Task 3]

```

> TOOL

tool_result
id: call_kr0pl2m2Nm8eat9FGMhPWG8f
```
Chunk ID: 5f5b73
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 9
Output:
## main...origin/main [behind 1]

```

> TOOL

tool_result
id: call_DhC1cUEb285lqgmYc0iUaEqB
```
Chunk ID: cf806e
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 15
Output:
ls: skills/update-evorto-branch: No such file or directory

```

> AGENT

The checkout is on `main`, clean, and behind `origin/main` by one commit. The memory pointer mentions a sync skill, but that local skill path is not present in this checkout, so I’m falling back to direct Git verification and a fast-forward update.

> TOOL

tool_use exec_command
id: call_EgS7jof3aXcrvh8xmzdufVNp
```json
{
  "cmd": "sed -n '408,422p' /home/<USER>/.codex/memories/MEMORY.md",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_use exec_command
id: call_ypFx3y4BobmgkgcLelr1evsE
```json
{
  "cmd": "git fetch --no-tags origin main",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_WCRGQMiVSkNpsC9gvwNAZAce
```json
{
  "cmd": "find /home/<USER>/code/evorto -path '*/update-evorto-branch/SKILL.md' -print",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result
id: call_EgS7jof3aXcrvh8xmzdufVNp
```
Chunk ID: 37d65c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 689
Output:
- In `evorto`, the relevant Neon project came from `.env.dev.local` and the API key from `.env`; the validated project id in this rollout was `polished-frost-79768881`. [Task 1]
- Branch deletion worked for both `ready` and `archived` branches, and verification should end with `total=1` and only `main` remaining. [Task 1]
- The branch explosion mechanism in this repo is tied to Neon Local, not manual branch naming: `docker-compose.yml`, `helpers/testing/runtime-environment.ts`, `.github/workflows/e2e-baseline.yml`, and `helpers/README.md` all point to a stack that mounts `.neon_local` metadata and uses `PARENT_BRANCH_ID`-driven ephemeral branches. [Task 2]
- Neon operations history is the useful source of truth for branch creation vs deletion patterns; in the validated slice, `create_branch=7` aligned with deleted branch ids and many `delete_timeline` events. [Task 2]
- After deleting stale Neon branches, restart any local containers still pointing at those branches; the local `db` container became unhealthy after its branch `br-damp-base-a9iezwjr` was removed. [Task 2]
- The mitigation that was pushed adds `helpers/testing/set-neon-local-branch-expiration.ts`, which waits for `.neon_local/.branches` metadata, skips when `BRANCH_ID` is already set or `DELETE_BRANCH=false`, and PATCHes `expires_at` on the generated branch. [Task 3]
- […]

> TOOL

tool_result
id: call_ypFx3y4BobmgkgcLelr1evsE
```
Chunk ID: 4c1982
Wall time: 0.4039 seconds
Process exited with code 0
Original token count: 24
Output:
From https://github.com/evorto-app/app
 * branch                    main       -> FETCH_HEAD

```

> TOOL

tool_result
id: call_WCRGQMiVSkNpsC9gvwNAZAce
```
Chunk ID: cd3845
Wall time: 1.0017 seconds
Process running with session ID 19043
Original token count: 0
Output:

```

> AGENT

The fetch succeeded and confirmed remote `main` is the target. I’m checking whether this can be fast-forwarded cleanly, then I’ll apply it.

> TOOL

tool_use write_stdin
id: call_W5BCfHqPEBPXzrdLc38EhXxb
```json
{
  "session_id": 19043,
  "chars": "",
  "yield_time_ms": 5000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_use exec_command
id: call_TMZleWAZ1cZAvVwV6geIq5cr
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_NHTrzhsuHSM3uMQzuvamAlcz
```json
{
  "cmd": "git rev-parse HEAD FETCH_HEAD && git merge-base --is-ancestor HEAD FETCH_HEAD; printf 'ancestor=%s\\n' \"$?\"",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_gt9B1s86r0XIE5ffIwiT2YP5
```json
{
  "cmd": "git log --oneline --decorate --max-count=5 HEAD..FETCH_HEAD",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result
id: call_W5BCfHqPEBPXzrdLc38EhXxb
```
Chunk ID: ecb887
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 0
Output:

```

> TOOL

tool_result
id: call_TMZleWAZ1cZAvVwV6geIq5cr
```
Chunk ID: 79bf0e
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 9
Output:
## main...origin/main [behind 1]

```

> TOOL

tool_result
id: call_NHTrzhsuHSM3uMQzuvamAlcz
```
Chunk ID: d4823b
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 24
Output:
0b113419b8dd44f3603f2ffcb352cf51a3fe5312
d1662b419c42a1d7ff55954f1ab8ca19bc5ae6ad
ancestor=0

```

> TOOL

tool_result
id: call_gt9B1s86r0XIE5ffIwiT2YP5
```
Chunk ID: b419e6
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 24
Output:
d1662b419c4 (origin/main, origin/HEAD) test: harden launch-critical Playwright coverage (#82)

```

> AGENT

`HEAD` is an ancestor of the fetched remote commit, so this is a clean fast-forward. I’m updating `main` now and then I’ll confirm the branch is current.

> TOOL

tool_use exec_command
id: call_KJSyNRF8HvOaZRn4YcNGgGpw
```json
{
  "cmd": "git merge --ff-only FETCH_HEAD",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
}
```

> TOOL

tool_result
id: call_KJSyNRF8HvOaZRn4YcNGgGpw
```
Chunk ID: 60aceb
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 308
Output:
Updating 0b113419b8d..d1662b419c4
Fast-forward
 .../members-hub/members-hub.component.spec.ts      | 122 ++++++++++++
 .../members-hub/members-hub.component.ts           |  22 ++-
 src/server/config/test-runtime-config.ts           |  10 +-
 src/server/effect/rpc/handlers/admin.handlers.ts   |   6 +-
 .../finance/receipt-review-reimbursement.doc.ts    | 205 ++++++++++++++++++++-
 tests/docs/templates/templates.doc.ts              |  90 +++++++++
 tests/docs/users/create-account.doc.ts             |  56 ++++--
 tests/specs/events/events.test.ts                  |   6 +-
 tests/specs/finance/receipts-flows.spec.ts         | 190 +++++++++++--------
 tests/specs/finance/stripe-webhook-replay.spec.ts  |  10 +-
 .../tax-rates/admin-import-tax-rates.spec.ts       |   2 +-
 tests/specs/permissions/matrix.spec.ts             |   2 +-
 tests/specs/permissions/override.test.ts           |  78 +++++++-
 tests/specs/profile/create-account.spec.ts         |  48 +++--
 tests/specs/scanning/scanner.test.ts               |   4 +-
 tests/test-inventory.md                            |   5 +
 16 files changed, 708 insertions(+), 148 deletions(-)
 create mode 100644 src/app/internal-pages/members-hub/members-hub.component.spec.ts

```

> AGENT

The fast-forward completed. I’m doing one final status check and recording the resulting commit so you have the exact state.

> TOOL

tool_use exec_command
id: call_YzGZk5X6v80eDvJTn2fWMgWK
```json
{
  "cmd": "git status --short --branch",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_use exec_command
id: call_rYJKKDFZPEJ3T2yDPU80sskI
```json
{
  "cmd": "git rev-parse --short HEAD && git log -1 --oneline --decorate",
  "workdir": "/home/<USER>/code/evorto",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result
id: call_YzGZk5X6v80eDvJTn2fWMgWK
```
Chunk ID: 332e27
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 6
Output:
## main...origin/main

```

> TOOL

tool_result
id: call_rYJKKDFZPEJ3T2yDPU80sskI
```
Chunk ID: 3e592f
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 30
Output:
d1662b419c4
d1662b419c4 (HEAD -> main, origin/main, origin/HEAD) test: harden launch-critical Playwright coverage (#82)

```

> AGENT

Updated `/home/<USER>/code/evorto` to the latest remote `main`.

Current state:
- Branch: `main`
- Status: clean and aligned with `origin/main`
- HEAD: `d1662b419c4 test: harden launch-critical Playwright coverage (#82)`

No tests were run because this was a fast-forward-only checkout update with no local edits.

<oai-mem-citation>
<citation_entries>
MEMORY.md:417-417|note=[checked repo sync guidance pointer]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>