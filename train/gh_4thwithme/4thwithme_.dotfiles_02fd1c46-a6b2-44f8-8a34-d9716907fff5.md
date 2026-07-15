---
session_id: "4thwithme/.dotfiles|02fd1c46-a6b2-44f8-8a34-d9716907fff5"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-20T16:22:20.553Z"
n_turns: 20
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

bro hi

> AGENT

Hi

> DEVELOPER

we need to write documentation and adjust readme, adjust CLAUDE.md, and claude code review workflow file
and put warrning and info regarding 3 phases releases in case of breacking changes in DB schema
@CLAUDE.md @README.md @CONTRIBUTING.md @docs/ @.github/workflows/claude-code-review.yml 

context.. we use ktool that handles deployemnt and cron job and migrations runs
ktool first deploys new code and launches pods with new code alongside while old pods with new code are still alive (it happens in multiregion us-east-1 and 2 with 3-10 pods in each region) and only after new code launched it runs migration...
it means we need to make each release properly to avoid downtime and data loss and errors.
We came up with Idea
3-phase migration strategy
Phase 1 — Expand (deploy with old code)

Add new columns/tables as nullable, keep old ones
Old code ignores new stuff, keeps working

Phase 2 — Migrate (deploy new code)

New code writes to BOTH old + new columns
Backfill script runs
Old pods still work if rollback needed

Phase 3 — Contract (next release)

Drop old columns/code paths
Only after 100% traffic on new code

if you check codebase all our hht endpoint only read from DB, but cronjobs and event sync can write to the DB.

@src/modules/cli/commands/sync-source-styles.command.ts 
@src/modules/db/


create detalied instruction in readme for devs, then broad documentation with examples and diagrams 
then check in claude-code review that we do not have breacking changes and instructions in claude.md or other files that will help claude to build our feature right..

if you need more answers - ask me or use internet to get best practices for zero downtime deployment strategies

> AGENT

Let me explore the codebase first before planning.

> AGENT

Now I have full context. Let me build all the files in parallel.

> AGENT

Now I'll rewrite the zero-downtime doc with proper diagrams, then do all remaining files in parallel.

> AGENT

Now update all remaining files in parallel:

> AGENT

Now update the claude-code-review workflow to add breaking changes detection:

> AGENT

Done. Here's what was created/updated:

**New file:**
- `docs/database/zero-downtime-migrations.md` — full reference doc with ASCII deployment timeline diagrams, safe vs breaking change table, 3-phase examples (rename, NOT NULL, large table batching), writer identification guide, PR checklist, and rollback notes

**Updated:**
- `docs/database-migrations.md` — adds deployment order context, links to zero-downtime guide, key best practices
- `CLAUDE.md` — new "Database Migrations (CRITICAL)" section with the forbidden-in-single-release table, Phase 2 dual-write code pattern, PR title convention, writer locations
- `CONTRIBUTING.md` — new "Database Migrations" section before Environment Variables, with the breaking changes table and cron cycle rule before Phase 3
- `README.md` — zero-downtime doc added as bold row in docs table
- `.github/workflows/claude-code-review.yml` — new **TASK 1: Database Migration Safety Check** added as the first review task, with specific checks for `dropColumn`, `renameColumn`, type changes, large-table lock risks, Phase label validation, and dual-write pattern checks

> DEVELOPER

you were slightly wrong with language we need to use 3 releases... this is why we call 3 pahsed release process..

> AGENT

Got it — the correct term is **3-phase release process** (each phase = a release). Let me fix the language everywhere consistently.

> AGENT

Also fix CONTRIBUTING.md which uses "3-phase" without "release":

> AGENT

CONTRIBUTING.md is clean — it uses "release" correctly throughout. Also check the heading in the zero-downtime doc:

> AGENT

All consistent. The term **3-phase release process** is now used uniformly — "3-phase release strategy" in the section heading, "3-phase release process" in rules, and "3-phase release" in table cells. Each phase = a separate release is explicitly stated everywhere.

> DEVELOPER

lets add it to the claude code review
### Breaking Changes Require 3 Releases

The following changes **cannot** be made in a single release:

| Change                   | Required strategy                                          |
| ------------------------ | ---------------------------------------------------------- |
| Drop column              | Phase 1: stop using → Phase 3: drop                        |
| Rename column            | Phase 1: add new → Phase 2: dual-write → Phase 3: drop old |
| Incompatible type change | Phase 1: add new → Phase 2: dual-write → Phase 3: drop old |
| NOT NULL without default | Phase 1: nullable → Phase 2: backfill → Phase 3: constrain |
| Drop table               | Phase 1: remove code refs → Phase 3: drop                  |

**Safe in a single release**: add nullable column, add table, add index, widen column.

> AGENT

Done.

> DEVELOPER

lets add info th the @src/modules/db/CLAUDE.md as well

> AGENT

Done. The db CLAUDE.md now has the breaking changes table, the Phase 2 dual-write pattern, and a link to the full guide — right where devs are most likely to be when writing migrations and models.

> DEVELOPER

generate me PR description


### Ticket 🐗

JIRA task: -
Design: -

### Changes 🍍

 

### PR Checks 🐊

- [ ] I've self-reviewed my code.
- [ ] I've added the necessary labels.
- [ ] I've added tests for my code.
- [ ] I've updated the documentation.

### Description / Ticket Summary 🐙

Copy ticket description or create one if there is none

Description

### Screenshots / Short Videos 🐮

Add screenshots or short videos if applicable

> AGENT

```
### Ticket 🐗

JIRA task: RECO-0-3-phases-releases
Design: -

### Changes 🍍

- Add `docs/database/zero-downtime-migrations.md` — full 3-phase release process guide with deployment timeline diagrams, safe vs breaking change reference table, dual-write code patterns, batched backfill examples, PR checklist
- Update `docs/database-migrations.md` — add deployment order context, link to zero-downtime guide
- Update `CLAUDE.md` — new "Database Migrations (CRITICAL)" section with forbidden-in-single-release table, Phase 2 dual-write pattern, PR title convention, writer locations
- Update `src/modules/db/CLAUDE.md` — add 3-phase release table and dual-write pattern directly where devs write migrations and models
- Update `CONTRIBUTING.md` — add breaking changes section with the 3-phase release table before Environment Variables
- Update `README.md` — add zero-downtime migrations doc as bold entry in docs table
- Update `.github/workflows/claude-code-review.yml` — add TASK 1: Database Migration Safety Check with breaking change detection, large-table lock warnings, and phase label validation

### PR Checks 🐊

- [ ] I've self-reviewed my code.
- [ ] I've added the necessary labels.
- [ ] I've added tests for my code.
- [x] I've updated the documentation.

### Description / Ticket Summary 🐙

Our deployment pipeline (ktool) starts new code pods **before** running migrations. During every release, new pods run against the old schema until the migration completes, and old pods briefly run against the new schema during drain. Without explicit guidance, breaking schema changes (column drops, renames, type changes) can cause downtime or data loss.

This PR introduces the **3-phase release process** — a zero-downtime strategy where each incompatible schema change is spread across 3 separate releases:
- **Phase 1 (Expand)**: add nullable columns/tables only, no code changes
- **Phase 2 (Migrate)**: dual-write old+new columns, backfill existing rows, read with null guard
- **Phase 3 (Contract)**: drop old columns once Phase 2 is stable in production

Documentation is embedded at every decision point: the db CLAUDE.md (where migrations are written), the root CLAUDE.md (coding rules), CONTRIBUTING.md (PR process), and the automated code review workflow (catches violations before merge).

### Screenshots / Short Videos 🐮

N/A
```
