> DEVELOPER

/brainstorming how do we allow trails to support multiple (potentially stacked) PRs, and hence multiple branches?

> TOOL

<command-message>superpowers:brainstorming</command-message>
<command-name>/superpowers:brainstorming</command-name>
<command-args>how do we allow trails to support multiple (potentially stacked) PRs, and hence multiple branches?</command-args>

> AGENT

Good, I now have a thorough understanding of the current architecture. Let me summarize the relevant starting point:

**Current state:**
- A trail is 1:1 with a branch (`Branch` + `Base` fields)
- Trails track checkpoints made on that branch
- No parent-child trail relationships exist
- No PR integration yet
- Sessions are commit-scoped (shadow branches), not branch-scoped

**The gap:** Trails are currently single-branch, single-PR. No way to represent "feature X spans branches A→B→C stacked on each other."

---

Let me start with the first clarifying question:

**What's the primary user story driving this?** I can think of a few distinct scenarios:

1. **Stacked PRs for a large feature** — User breaks a big feature into PR1 (base changes), PR2 (depends on PR1), PR3 (depends on PR2). Each is a branch. They want a unified trail showing the full feature's progress across all three.

2. **Iterative PRs on the same trail** — User works on branch A, merges PR, then continues on branch B for follow-up work. Same logical trail, but branches change over time sequentially.

3. **Parallel PRs from one trail** — User discovers mid-feature that they need a refactor PR first, so they split work into two […]

> DEVELOPER

I think in an ideal world we would like to support all these different use cases, while maintaining the same "Intent" for the Trail

> AGENT

That makes sense — the Trail is the *intent* (the "what" and "why"), and branches/PRs are just *execution artifacts* that serve that intent. Sometimes one branch suffices, sometimes you need several.

**Next question:** How do you think about the relationship structure between a trail and its branches/PRs? Two main models:

**A) Flat list** — A trail has an ordered list of branch/PR references. The trail itself doesn't encode dependencies between them. It's just "these branches all serve this intent." Stacking is implicit (branch B is based on branch A, but the trail just knows about both).

**B) Tree/graph** — The trail explicitly models parent-child relationships between its branches. E.g., "PR2 depends on PR1, PR3 also depends on PR1." This is richer but more complex to manage — especially when rebasing stacks.

My instinct is that **A (flat list)** is the right starting point. The git branch topology already encodes dependencies (what's based on what), and duplicating that in trail metadata creates a synchronization problem. The trail just needs to know "these are my branches" and can derive the rest from git.

Do you agree with flat list, or do you see value in explicitly modeling the dependency graph?

> DEVELOPER

yeah I think the flat list is fine for now. branch-PRs are natural units, though the PR part could in theory get discarded for a replacement?

> AGENT

Right — so the branch is the durable identifier, and the PR is an optional, replaceable attachment on it. You might close PR #42, rebase, and open PR #43 on the same branch. Or have a branch with no PR yet.

**Next question:** What should a branch entry in a trail look like conceptually? Something like:

```
BranchEntry {
  Branch:    "alex/auth-refactor"
  Base:      "main"              // what it's stacked on
  PR:        #42                 // optional, replaceable
  Status:    "open"              // branch-level status
  AddedAt:   timestamp
}
```

And a few sub-questions packed into one (since they're tightly related):

1. **Is `Base` per-branch or per-trail?** Currently trails have a single `Base`. With stacking, each branch could have a different base (PR2's base is PR1's branch, not `main`). Should `Base` move to the branch entry?

2. **When a branch is the "current" trail branch** (the one the user is actively working on), should that be explicit? Or just inferred from which git branch is checked out?

3. **Should there be a "primary" branch?** E.g., the first branch created is the main line of work, and others are supporting. Or are all branches equal peers?

> DEVELOPER

1. remember also that branch refs themselves are not durable (and may not be available in the local repo)...so we may need to record more than that. To answer your question though I think the base needs to be per-branch/PR to support stacking.

at least one branch/PR presumably comes from main...but as rebases happen the specific merge-base is mutable as well 😅

2. it can just be inferred? are you asking when a branch should be added to a Trail? Let's keep it explicit for now, I don't know if there are any hooks available on the git branch command to track it!

3. let's keep it flat and simple for now

> AGENT

Great point about durability. Branch names are ephemeral — they get deleted after merge, renamed, or might only exist on the remote. So we need the branch entry to be self-describing enough to survive that.

**Next question:** What should make a branch entry identifiable if the branch name itself isn't durable? I'm thinking something like:

```
BranchEntry {
  ID:          "uuid"              // stable internal identifier
  Name:        "alex/auth-refactor" // label, may go stale
  Base:        "main"              // what it targets (also a label)
  PR:          #42                 // optional, replaceable, but arguably the most durable external ref
  Checkpoints: [...]              // checkpoint refs made on this branch
}
```

The `ID` is what we use internally to link things. The `Name` and `Base` are informational labels that may drift. The `PR` number is ironically the most durable external identifier (GitHub PRs persist even after branch deletion).

Does that feel right? And a related question — **should the existing single-branch trail fields (`Branch`, `Base`) migrate into this new structure**, or do you want to keep backward compatibility where a trail with one branch still looks like today's format?

> DEVELOPER

Base: main@{sha}? what's the 'git native' way to express this?

Let's run with this for now

> AGENT

Good question. Git doesn't have a single native syntax for "branch + pinned commit." The idiomatic way is two separate fields:

- **Branch name** — the human-readable ref (`main`, `alex/auth-refactor`)
- **Commit SHA** — the immutable anchor (what `main` pointed to at time of recording, or the fork point)

So the base would be:

```
BaseBranch: "main"       // where it targets
BaseCommit: "abc1234..." // fork point / merge-base at time of recording
```

The branch name gives intent, the SHA gives precision. Rebases update the SHA.

---

**Next question:** How should users interact with multi-branch trails? I'm imagining something like:

```bash
# Create trail (same as today, first branch implicit from current)
entire trail create "Add auth system"

# Explicitly add another branch to the trail
entire trail branch add alex/auth-api --base alex/auth-refactor

# Replace a PR reference
entire trail branch set-pr alex/auth-api 43

# List branches in a trail
entire trail show
```

Two things I want to confirm:

1. **Is the current branch auto-added on `trail create`?** (Seems natural — you create a trail while on a branch.)

2. **Should `entire trail branch add` require being on that branch, or accept a branch name argument?** The user might […]

> DEVELOPER

1. the ux is a bit clunky, we currently 'auto-generate' a branch name but you can go back and edit it
2. perhaps `entire trail branch add` adds this branch? I don't know how to avoid adding branches into multiple trails by accident though 😅 (maybe doesn't matter for now). We should also have a version where we can pass the branch.

> AGENT

Makes sense. And yeah, a warning if a branch is already in another trail is probably sufficient — no need to hard-block.

I think I have enough context to propose approaches. Let me lay them out.

---

## Three Approaches

### Approach A: Evolve TrailMetadata in-place (Recommended)

Add `Branches []BranchEntry` to `TrailMetadata`, migrate existing `Branch`/`Base` into the first entry. Checkpoints move from trail-level (`checkpoints.json`) to per-branch-entry.

```
TrailMetadata {
  TrailID, Title, Body, Status, ...
  Branches: []BranchEntry          // replaces Branch + Base
}

BranchEntry {
  ID:          "uuid"
  Name:        "alex/auth-refactor"
  BaseBranch:  "main"
  BaseCommit:  "abc1234..."        // fork point, updated on rebase
  PR:          *PRRef              // optional {Number, URL, Status}
  Checkpoints: []CheckpointRef
  AddedAt:     timestamp
}
```

Storage stays the same (single `metadata.json` per trail). `FindByBranch` scans all trails' branch entries — fine at our scale.

**Pros:** Simple, single file per trail, easy migration, minimal new plumbing.
**Cons:** `FindByBranch` is O(trails × branches) — acceptable for now.

### Approach B: Separate branch index file

Keep `metadata.json` lean. Add `branches.json` to each trail's tree with the branch entries. Plus a global `branch-index.json` mapping branch names → trail IDs for fast lookup.

**Pros:** Fast O(1) branch lookup, cleaner separation.
**Cons:** Two files to keep in sync, index can […]

> DEVELOPER

I wonder if there is parallel development going on - would we start running into file concurrency issues?

> AGENT

Sharp instinct — yes, this is a real concern. The trail data lives on `entire/trails/v1` (an orphan branch), and writes are: read tip → build new tree → commit → update ref. Two concurrent processes hitting the same trail could race:

1. Session A reads metadata (branches: [X])
2. Session B reads metadata (branches: [X])
3. Session A writes (branches: [X, Y])
4. Session B writes (branches: [X, Z]) — **clobbers Y**

**How bad is it in practice with Approach A?**

The risky operations are:
- **Adding a branch to a trail** — explicit user action, unlikely to race
- **Appending a checkpoint** — happens on commit, could race if two worktrees commit simultaneously on branches belonging to the same trail
- **Updating PR reference** — explicit user action, unlikely to race

So checkpoint appending is the main risk. And with multi-branch trails, you're *more likely* to have concurrent sessions on different branches of the same trail — that's the whole point.

**Mitigation options (cheapest to most complex):**

1. **Optimistic concurrency via `git update-ref --stdin`** — use compare-and-swap on the ref. If the ref moved since we read it, re-read and retry. Narrow retry loop, no locks. This is git-native. […]

> DEVELOPER

tell me more about git update-ref?

> AGENT

So the current write path is: read ref → build tree → commit → `SetReference` (unconditional). Classic read-modify-write with no CAS.

Here's the summary for you:

**Current situation:** Every ref update in the codebase (`entire/trails/v1`, `entire/checkpoints/v1`, shadow branches) uses unconditional `SetReference`. This means concurrent writes can silently clobber each other. It works today because:
- Single session per worktree is the common case
- Trail writes are infrequent (user-initiated)
- Checkpoint writes are per-commit (narrow window)

**With multi-branch trails, the risk increases** because two worktrees working on different branches of the same trail would both write to `entire/trails/v1` (appending checkpoints to the same trail).

**The fix is straightforward:** go-git has `CheckAndSetReference(new, old)` which does exactly CAS. The write path becomes:

```go
// Instead of:
repo.Storer.SetReference(newRef)

// Use:
err := repo.Storer.CheckAndSetReference(newRef, oldRef)
if errors.Is(err, storage.ErrReferenceHasChanged) {
    // Re-read, re-apply, retry
}
```

This is a self-contained improvement we can make independently — it benefits the existing checkpoint/trail code too, not just multi-branch.

**My recommendation:** Add CAS as a foundational improvement early in the implementation plan, then build multi-branch trails on top of it. It's a small change with broad benefit.

Want to continue refining the design, or do you have more […]

> DEVELOPER

essentially doing a `git commit` on the trails file?

> AGENT

Yes, exactly — it's already doing that. Every trail write creates a git commit on `entire/trails/v1`. The flow is:

1. Read current tip of `entire/trails/v1` → get commit `abc123` + its tree
2. Modify the tree (splice in updated trail files)
3. Create new commit `def456` with parent `abc123`
4. Point `entire/trails/v1` → `def456`

Step 4 is where the race lives. Today it's an unconditional "set ref to `def456`". With CAS it becomes "set ref to `def456` **only if it still points to `abc123`**." If someone snuck in a commit between steps 1 and 4, the ref now points to `xyz789` instead, the CAS fails, and we retry from step 1.

It's the same semantics as `git commit` on a regular branch — git won't let two people commit to the same branch tip simultaneously. We're just replicating that safety for our plumbing-level ref updates in go-git, since `SetReference` bypasses it.

Shall we move on to the rest of the design? I think the major open questions are:

1. **Migration** — how do existing single-branch trails get upgraded to the new schema?
2. **CLI commands** — the `entire trail branch add/set-pr/list` surface area
3. **Hook integration** — how post-commit finds […]

> DEVELOPER

so what you're saying is that we don't need to split the file as git will help us 'lock' on simultaneous changes?

> AGENT

Right — git's ref semantics give us the lock for free. Since every trail write is a commit on `entire/trails/v1`, and CAS ensures only one writer wins the ref update, we don't need to split files to avoid conflicts. The "conflict" happens at the ref level, not the file level.

**But there's a nuance:** CAS tells us *someone else wrote*, but it doesn't help us *merge* the changes. With a single `metadata.json` per trail, the retry loop is:

1. Re-read the whole file
2. Re-apply our change (e.g., append our checkpoint to the branch entry)
3. Re-commit and CAS again

This works cleanly because our writes are typically **append-only** (adding a checkpoint ref) or **field updates** (setting a PR number). Re-reading and re-applying is trivial — there's no merge conflict to resolve.

If we had a scenario where two writers were *modifying the same field* (e.g., both trying to set the trail status simultaneously), last-writer-wins after retry is fine. That's a human-initiated action and shouldn't race.

So yes — **single `metadata.json` per trail + CAS retry is sufficient.** No need for file splitting, subdirectories, or separate indexes. Git does the heavy lifting.

Shall we move on to the design? I […]

> DEVELOPER

ok

> AGENT

## Section 1: Data Model

### Trail Metadata (revised)

```go
type Metadata struct {
    TrailID   ID        `json:"trail_id"`
    Title     string    `json:"title"`
    Body      string    `json:"body"`
    Status    Status    `json:"status"`
    Type      Type      `json:"type,omitempty"`
    Priority  Priority  `json:"priority,omitempty"`
    Author    string    `json:"author,omitempty"`
    Reviewers []Reviewer `json:"reviewers,omitempty"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`

    // REMOVED: Branch, Base (moved into BranchEntry)
    // NEW:
    Branches  []BranchEntry `json:"branches"`
}
```

### BranchEntry (new)

```go
type BranchEntry struct {
    ID         string    `json:"id"`           // stable UUID
    Name       string    `json:"name"`         // branch name (informational, may go stale)
    BaseBranch string    `json:"base_branch"`  // target branch name (e.g., "main")
    BaseCommit string    `json:"base_commit"`  // fork point SHA (updated on rebase)
    PR         *PRRef    `json:"pr,omitempty"` // optional, replaceable
    AddedAt    time.Time `json:"added_at"`
}
```

### PRRef (new)

```go
type PRRef struct {
    Number int    `json:"number"`
    URL    string `json:"url,omitempty"`
    Status string `json:"status,omitempty"` // open, merged, closed
}
```

### Checkpoints stay per-trail, gain a BranchID field

```go
type CheckpointRef struct {
    CheckpointID string    `json:"checkpoint_id"`
    CommitSHA    string    `json:"commit_sha"`
    Summary      string    `json:"summary,omitempty"`
    CreatedAt    time.Time `json:"created_at"`
    // NEW:
    BranchID     string    `json:"branch_id,omitempty"` // links to BranchEntry.ID
}
```

This keeps `checkpoints.json` as a single flat file (easy to read the full trail history) while still allowing filtering by branch. The `BranchID` is optional for backward compat — […]

> DEVELOPER

while we're here....
Trail
+-- intent (typed reference — see below)
+-- checkpoints[] (linked checkpoints — the spine of the trail)
+--   summary (one per checkpoint, exists today in CLI)
+--   sessions[] (contributing agent sessions, reachable via checkpoint)
+-- amendments[] (spec changes with reasoning)
+-- summary (aggregated trail-level summary, rolled up from checkpoint summaries)
+-- report (aggregated verification report)
+-- ship reference (PR URL, merge commit — set at ship time)
```

### Intent reference (typed)

The intent reference should be typed rather than a bare string, so tooling can
resolve and display it appropriately. _(h/t evisdren)_

```go
type Intent struct {
    Kind    string `json:"kind"`              // file, url, issue, inline
    Value   string `json:"value"`             // path, URL, issue ID, inline text
    Content string `json:"content,omitempty"` // resolved intent text (cached)
}
```

This supports the full spectrum: formal spec file, Linear issue, URL, or inline
one-liner. `Content` is optional — populated at trail creation or on first resolve
to avoid repeated lookups.


this is some thinking from elsewhere, we need to align both of these models...

the elsewhere version didn't really consider branches or PRs, which I think is important now that we're seeing the rubber hit the road

> AGENT

Great — let me align these. The elsewhere model is richer and more intentional. The key question is where branches fit in.

Here's my attempt at merging:

```
Trail
+-- intent          (typed reference — file, url, issue, inline)
+-- branches[]      (NEW — execution artifacts serving the intent)
+--   name, base_branch, base_commit
+--   pr             (optional, replaceable)
+-- checkpoints[]   (the spine — exists today)
+--   summary
+--   branch_id      (NEW — which branch this checkpoint belongs to)
+--   sessions[]     (contributing agent sessions)
+-- amendments[]    (spec changes with reasoning)
+-- summary         (aggregated trail-level summary)
+-- report          (aggregated verification report)
+-- ship_reference  (trail-level — final merge to main?)
```

The **tensions** I see:

1. **Ship reference vs. per-branch PRs** — The elsewhere model has a single ship reference (PR URL + merge commit). But with multi-branch, each branch has its own PR that gets merged. Is the trail-level `ship_reference` the *last* PR (the one that lands on main)? Or do we drop it and derive "shipped" from "all branch PRs merged"?

2. **Intent replaces Title/Body** — The elsewhere model's `Intent` is strictly better than bare `Title`/`Body`. But do we keep `Title` as a human-friendly label alongside `Intent`? E.g., Intent points to a Linear issue, Title […]

> DEVELOPER

1. we don't need to keep anything at top level
2. I think having the title as a separate field is fine
3. amendments might live under Intent?

> AGENT

Clean. Revised model:

```
Trail
+-- title            (human-friendly label for display)
+-- intent           (typed reference — the "what and why")
+--   kind, value, content
+--   amendments[]   (spec changes with reasoning — lives under intent)
+-- branches[]       (execution artifacts — the "how")
+--   id, name, base_branch, base_commit
+--   pr             (optional, replaceable — number, url, status)
+-- checkpoints[]    (the spine — the "when")
+--   checkpoint_id, commit_sha, summary
+--   branch_id      (links to branch entry)
+--   sessions[]
+-- summary          (aggregated trail-level summary)
+-- report           (aggregated verification report)
```

"Shipped" is derived: all branch PRs have `status: "merged"`. No redundant top-level field.

---

## Section 2: Storage Layout

Currently each trail is stored on `entire/trails/v1` as:

```
<trail-id[:2]>/<trail-id[2:]>/
├── metadata.json
├── discussion.json
└── checkpoints.json
```

I'd propose keeping this structure. The three files map naturally:

- **`metadata.json`** — title, intent (with amendments), branches[], summary, report, status
- **`checkpoints.json`** — checkpoint refs with branch_id (unchanged file, new field)
- **`discussion.json`** — unchanged

The alternative would be splitting branches or checkpoints into separate files, but as we discussed, CAS retry handles concurrency and the data volume per trail is small.

Does this storage layout look right, or do you want to restructure the files?

> DEVELOPER

shipped == status: "merged" or discarded (whatever that looks like)

discussion - separate file but....part of the Trail model at top level?

the multi-PRs have a bit of an impact on the verification report...

> AGENT

Good catches, let me address each:

**Shipped** — right, a branch's terminal states are `merged` or `discarded` (closed without merge, abandoned, superseded). Trail is "shipped" when all branches have reached a terminal state and at least one was merged. Something like:

```go
type BranchStatus string
const (
    BranchOpen      BranchStatus = "open"
    BranchMerged    BranchStatus = "merged"
    BranchDiscarded BranchStatus = "discarded"
)
```

**Discussion** — yes, I'd put it in the conceptual model at top level:

```
Trail
+-- title
+-- intent
+--   amendments[]
+-- branches[]
+-- checkpoints[]
+-- discussion[]     ← top-level concept
+-- summary
+-- report
```

Stored in a separate file for practical reasons (discussions grow independently and can get large), but logically it's a first-class part of the trail.

**Verification report + multi-PR** — this is the interesting one. A few options:

1. **Per-branch reports** — each branch/PR gets its own verification report. Trail-level report aggregates them.
2. **Trail-level only** — single report that covers the whole intent, re-run after each branch lands.
3. **Incremental** — report tracks which branches it has verified, flags unverified ones.

My instinct is **(1)** — per-branch reports that roll up. Each PR is a reviewable/shippable unit with its own test results, and the […]

> DEVELOPER

today it is a PR scoped bunch of github checks, pr-review activity and an "approval". I'm imagining a future where that also potentially extends to canary or post-release metrics, which makes it a bit tricky in terms of timeline

but we need to be able to support a flow that has progressive release with potential rollback, and the trail isn't 'done' until we achieve full rollout I think (which is part of the verification in this case)

> AGENT

That extends the trail lifecycle significantly. The trail isn't just a code artifact — it tracks the full intent lifecycle from idea to verified-in-production:

```
intent → branches/PRs → merge → canary → progressive rollout → full deployment
                                    ↑ rollback possible at any stage
```

I think this means the verification report needs to be a **timeline of verification events** rather than a point-in-time snapshot:

```
Trail
+-- report
+--   events[]
+--     kind: "pr_checks" | "review_approval" | "canary" | "rollout_stage" | "rollback" | "full_rollout"
+--     branch_id (optional — PR checks are per-branch, canary might be trail-level)
+--     status: "pass" | "fail" | "pending"
+--     timestamp
+--     details
```

And trail status extends to cover the deployment lifecycle:

```
draft → open → in_progress → in_review → merged → deploying → deployed
                                                      ↑
                                                  rolled_back
```

**But** — I think we should be careful about designing the deployment verification piece in detail right now. The code-side model (intent, branches, checkpoints, PR-scoped verification) is concrete and buildable. The deployment-side is still forming.

**My suggestion:** Design the report as an extensible event log (so new event kinds can be added later), but only implement PR-scoped verification events now. The structure accommodates canary/rollout later without […]

> DEVELOPER

yes, the post-deployment stuff is just another type of 'verification'

things like security/perf review are also verification types I think

> AGENT

Exactly. Verification is a unified concept with many kinds — all the same shape, just different scopes and triggers:

| Kind | Scope | Trigger |
|------|-------|---------|
| PR checks (CI) | per-branch | automated |
| Code review / approval | per-branch | human |
| Security review | per-branch or per-trail | human |
| Performance review | per-branch or per-trail | human/automated |
| Canary | per-trail | automated |
| Rollout stage | per-trail | automated |
| Post-deploy monitoring | per-trail | automated |

The model handles all of these uniformly. Let me consolidate the full data model and move on.

---

## Consolidated Data Model (revised)

```
Trail
+-- title              (human-friendly label)
+-- status             (draft → open → in_progress → in_review → merged → deploying → deployed | rolled_back)
+-- intent
+--   kind             (file, url, issue, inline)
+--   value            (path, URL, issue ID, inline text)
+--   content          (resolved/cached text)
+--   amendments[]
+--     description
+--     reasoning
+--     timestamp
+-- branches[]
+--   id               (stable UUID)
+--   name             (branch ref, informational)
+--   base_branch      (target branch name)
+--   base_commit      (fork point SHA)
+--   status           (open, merged, discarded)
+--   pr               (optional, replaceable: number, url)
+-- checkpoints[]      (the spine)
+-- […]

> DEVELOPER

do we need to have the status delineation between in_review -> merged -> deploying -> deployed -> done?

a progressive rollout strategy could be modelled as either the tail of the review process or a 'validating' stage? Do we need to know the underlying mechanics of it?

> AGENT

You're right — the verification event log already captures the mechanics. The trail status shouldn't duplicate that. It should reflect the *intent lifecycle*, not the deployment pipeline.

Simpler:

```
draft → active → validating → done
                     ↓
                  abandoned
```

- **draft** — intent defined, work hasn't started
- **active** — branches exist, work in progress
- **validating** — PRs up for review, canary running, rollout in progress — all "is this good?" activity
- **done** — intent fully realized and verified
- **abandoned** — intent dropped

Whether you're waiting on a code review or at 50% canary rollout, the trail is "validating." The verification event log tells you *what kind* of validation and *where* in the process. The trail status just says "we think we're done, checking."

This also avoids the problem of status transitions being tightly coupled to a specific deployment model — not every trail goes through canary/rollout.

Does this feel right?

> DEVELOPER

the only reason I'd keep something in there is if there needs to be a specific trigger for human action, i.e. the "Trail Review".

That said it that activity could happen at various points in the process and is perhaps a different type of Verification in itself...

> AGENT

Yeah — a "Trail Review" is a verification event, not a status. It could happen at different points:

- Before any PRs are merged (design review)
- After first PR lands but before the rest (checkpoint review)
- After all code lands but before rollout (final review)

If it's a status, you're forced into one spot in the lifecycle. If it's a verification event, it can happen whenever it's needed — and the trail just stays `validating`.

The trigger for human action could come from the verification log itself: "all automated checks passed, no `trail_review` event yet → surface a prompt to the user." That's a policy decision on top of the data, not baked into the state machine.

So I'd keep the simple statuses:

```
draft → active → validating → done | abandoned
```

And model trail review as:

```
verification event:
  kind: "trail_review"
  status: "requested" | "approved" | "changes_requested"
  branch_id: optional (could be trail-wide or per-branch)
```

---

Ready to move on to migration and CLI commands?

> DEVELOPER

good point, the design review is pretty critical. So yeah, it's a specific verification event, but we'd just need to work out how to signal it.

re: migration let's not worry about it, we don't need to bring prior trails up to date in this scheme

> AGENT

Makes sense — the signaling question (how to prompt a human for trail review at the right time) is an important UX problem, but it's separate from the data model. We can solve it later with rules/policies on top of the verification event log.

And agreed on migration — clean break. Old trails stay as-is, new trails use the new schema.

---

## Section 3: CLI Commands

Building on the existing `entire trail` command surface:

**Trail creation (modified):**
```bash
entire trail create "Add auth system"              # title, current branch auto-added
entire trail create "Add auth system" --intent-file docs/spec.md
entire trail create "Add auth system" --intent-issue LIN-123
entire trail create "Add auth system" --intent "inline description"
```

**Branch management (new):**
```bash
entire trail branch add                            # add current branch to active trail
entire trail branch add feature/auth-api           # add named branch
entire trail branch add --base feature/auth-core   # explicit base (stacking)
entire trail branch set-pr 43                      # set/replace PR on current branch
entire trail branch set-pr 43 --branch feature/x   # set PR on named branch
entire trail branch discard                        # mark current branch as discarded
```

**Viewing (modified):**
```bash
entire trail show                                  # full trail view including all branches
entire trail […]

> DEVELOPER

do we take a leave out of the nvm book? our current console has the 'trail context' loaded?

we could potentially switch when we move into different worktrees....

> AGENT

That's a great mental model. An "active trail" context, like `nvm use` or `rbenv local`:

```bash
entire trail create "Add auth system"    # creates trail AND activates it
entire trail use <id>                    # switch active trail

# all subsequent commands operate on the active trail implicitly
entire trail branch add
entire trail branch set-pr 43
entire trail show
```

And the worktree angle is clever — each worktree is already branch-scoped, so:

- Enter worktree for `feature/auth-api` → active trail auto-resolves to whichever trail has that branch
- No explicit `trail use` needed if the mapping is unambiguous
- If ambiguous (branch in multiple trails, which we warned about earlier), fall back to explicit selection

**Storage for the active trail context:**
- Per-worktree: something like `.git/entire-trail-context` (or inside `.git/entire-sessions/`)
- Set explicitly on `trail create` / `trail use`
- Auto-resolved from branch→trail lookup as a fallback

So the resolution order would be:
1. Explicit `--trail <id>` flag (always wins)
2. Stored context (from `trail create` or `trail use`)
3. Branch lookup (current branch found in exactly one trail)
4. Error: "multiple trails match, use `entire trail use`"

This also answers question #2 — `trail create` both creates the trail and […]

> DEVELOPER

.git is a pointer in worktrees, not a folder?

> AGENT

Right — in a linked worktree, `.git` is a file containing `gitdir: /path/to/main/.git/worktrees/<name>/`, not a directory.

Two relevant paths:
- **`git rev-parse --git-dir`** → worktree-specific: `/main/.git/worktrees/<name>/` 
- **`git rev-parse --git-common-dir`** → shared: `/main/.git/`

Session state already lives in the common dir (`.git/entire-sessions/`). But trail context is per-worktree, so options:

1. **Worktree-specific git dir** — `<git-dir>/entire-trail-context` (e.g., `/main/.git/worktrees/auth/entire-trail-context`). Git-native, invisible to the working tree.

2. **`.entire/` in the working directory** — already exists per worktree, already gitignored. Simplest to find.

3. **Common dir, keyed by worktree ID** — like sessions do today, but with worktree scoping.

I'd lean toward **(2)** — `.entire/trail-context.json` in the working directory. It's where all other Entire local state lives, it's already gitignored, and it works identically in both main worktrees and linked worktrees without resolving git dir paths.

Does that work?

> DEVELOPER

we just need to be able to handle this when switching branches within a worktree :|

> AGENT

Yeah, that's the problem with stored context — it goes stale on `git checkout`. And there's no reliable hook for branch switches.

Maybe we don't store context at all. Just derive it:

1. **`--trail <id>` flag** — explicit, always wins
2. **Branch→trail lookup** — current branch found in exactly one trail
3. **No match** → prompt/error

The "cost" is a branch→trail scan on every command, but we said that's fine at our scale. And it's always correct — no stale state to worry about.

The one gap: you're on a new branch that hasn't been added to any trail yet. But that's actually the right moment to be explicit — you're either:
- `entire trail create` (new trail, branch auto-added)
- `entire trail branch add` (needs to know which trail → `--trail <id>` or interactive picker if few trails are active)

Once the branch is in a trail, all subsequent commands auto-resolve.

This is simpler, stateless, and branch-switch-proof. The tradeoff is that `entire trail branch add` on a fresh branch needs trail disambiguation, but that's a one-time action per branch.

Does stateless lookup feel sufficient, or do you think there are commands where it falls short?

> DEVELOPER

stateless lookup is the safest for now

> AGENT

Agreed. Let me move on.

---

## Section 4: Hook Integration

This is where the rubber meets the road — how the existing post-commit hook finds the right trail and branch entry to append a checkpoint.

**Current flow** (from `manual_commit_hooks.go`):
1. Post-commit fires
2. Get current branch name
3. `store.FindByBranch(branchName)` → finds the trail
4. Append checkpoint to trail's checkpoints list

**New flow:**
1. Post-commit fires
2. Get current branch name
3. `store.FindByBranch(branchName)` → returns `(trail, branchEntry)` instead of just `trail`
4. Append checkpoint with `branch_id: branchEntry.ID` to trail's checkpoints list

The change is minimal — `FindByBranch` already exists, it just needs to:
- Scan all trails' `Branches[]` instead of matching a single `Branch` field
- Return the matched `BranchEntry` alongside the trail
- Warn (log) if a branch appears in multiple trails

**CAS retry wraps the write:**
```
loop:
  read trail tip → get tree
  find trail, modify checkpoints
  commit new tree
  CheckAndSetReference(new, old)
  if conflict → retry from read
```

**What about branches not in any trail?** Same as today — checkpoint is still saved on the shadow branch and condensed to `entire/checkpoints/v1`. It just doesn't get linked to a trail. The trail linkage is optional/additive.

---

Does […]

> DEVELOPER

yep

> AGENT

Plan complete and saved to `docs/plans/2026-03-07-trails-multi-branch-plan.md`.

**Summary: 11 tasks covering:**
1. New types (`Intent`, `BranchEntry`, `VerificationEvent`, new `Status` constants)
2. Updated `Metadata` struct with `Branches[]` and backward-compat legacy fields
3. `verification.json` storage in trail store
4. Multi-branch `FindByBranch` with legacy fallback
5. `BranchID` on `CheckpointRef` + hook integration
6. CAS retry with `CheckAndSetReference` for concurrent-safe writes
7. `entire trail branch add` command
8. `entire trail branch set-pr` and `discard` commands
9. Updated `trail create` for `Branches[]` and `Intent`
10. Updated `trail show` for multi-branch display
11. Full integration test pass

**Two execution options:**

**1. Subagent-Driven (this session)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** — Open new session with executing-plans, batch execution with checkpoints

Which approach?

> DEVELOPER

1

> AGENT

Understood, I'll wait for you to adjust the sandbox settings.

> DEVELOPER

continue

> AGENT

All done. Here's a summary of what was built:

**10 commits implementing multi-branch trail support:**

1. **New types** — `Intent`, `Amendment`, `BranchEntry`, `BranchStatus`, `PRRef`, `VerificationEvent`; simplified status lifecycle (`draft → active → validating → done | abandoned`)
2. **Updated Metadata** — added `Branches[]`, `Intent`, `Summary` fields with backward-compat legacy `Branch`/`Base`; added `FindBranch()` and `ActiveBranchName()` methods
3. **verification.json** — 4th file in trail store for verification event log
4. **Multi-branch FindByBranch** — scans `Branches[]` arrays, returns matched `*BranchEntry`, legacy fallback
5. **BranchID on checkpoints** — checkpoints now tagged with which branch they came from via post-commit hook
6. **CAS retry** — `CheckAndSetReference` with retry loop for concurrent-safe trail writes
7. **`trail branch add`** — add current or named branch to a trail with `--base` for stacking
8. **`trail branch set-pr` / `discard`** — set PR number, mark branch as discarded
9. **Updated `trail create`** — populates `Branches[]`, supports `--intent`/`--intent-file`/`--intent-issue` flags
10. **Updated display** — `trail show` renders branches with status markers and PR refs; `trail list` uses `ActiveBranchName()`

**Verification:** `mise run fmt` + `mise run lint` clean, all unit tests pass, integration tests pass, all 43 E2E canary tests pass.

Would you like me to proceed with finishing the branch (PR, […]

> DEVELOPER

what sort of test coverage do we have on the new stuff?

> AGENT

Here's what we have:

**New tests added (11 tests):**

| Test | What it covers |
|---|---|
| `TestBranchStatus_IsValid` | BranchStatus type validation |
| `TestStatus_OldStatusesInvalid` | Old status constants rejected |
| `TestMetadata_FindBranch` | FindBranch method on Metadata |
| `TestMetadata_ActiveBranchName` | Legacy fallback + new Branches[] |
| `TestStore_WriteAndReadVerification` | verification.json roundtrip |
| `TestStore_ReadVerificationBackwardCompat` | Old trails without verification.json |
| `TestStore_UpdatePreservesVerification` | Update doesn't lose verification data |
| `TestStore_FindByBranch_MultiBranch` | FindByBranch scanning Branches[] |
| `TestStore_FindByBranch_LegacyFallback` | FindByBranch with old single-branch trails |
| `TestStore_AddCheckpointWithBranchID` | BranchID persists on checkpoint refs |
| `TestStore_SequentialAddCheckpoints` | CAS retry path (sequential writes) |

**What's NOT tested:**

- **CLI commands** (`trail branch add`, `set-pr`, `discard`) — no unit tests. These are wired to cobra commands that call `strategy.OpenRepository`, `GetCurrentBranch`, etc. which makes them hard to unit test without integration test infrastructure.
- **CAS retry under actual contention** — we test sequential (non-conflicting) writes but not true concurrent races. Hard to test deterministically.
- **Intent from flags** in `trail create` — no test for `--intent-file` reading file content, `--intent-issue`, `--intent` flag handling.
- **Display output** of `printTrailDetails` — no test for the multi-branch rendering.
- **`trail list` with `ActiveBranchName()`** […]