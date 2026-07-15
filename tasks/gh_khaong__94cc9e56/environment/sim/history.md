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