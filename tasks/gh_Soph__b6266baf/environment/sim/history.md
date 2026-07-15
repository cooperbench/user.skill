> DEVELOPER

can you take a look at: Here's the git-sync issue, structured to mirror the entiredb one. --- ## git-sync: batched bootstrap sends pack-less ref creates that some servers reject ### Symptom During a batched bootstrap, git-sync finalizes a "subsumed" branch by sending a **ref-create command with no packfile**. Against a receive-pack implementation that expects a pack for any non-delete command, this fails: ``` bootstrap execute: create subsumed branch ref for refs/heads/<branch>: report-status: unpack error: quarantine fanout: read packfile header: EOF ``` The bootstrap dies mid-run, leaving the target half-populated. First observed mirroring `github.com/JUMPTOON/app` → entiredb prod `aws-us-east-2`, 2026-06-15 07:36 (trace `433bad8f4ef654ac651f868ab3c2fa3e`): ~15 batch pushes succeeded, then the subsumed-ref create EOF'd. ### Root cause In the batched bootstrap, the subsumed-branch path issues a ref-only push: ```go // internal/strategy/bootstrap/bootstrap.go (subsumed branch finalize) cmds := []gitproto.PushCommand{{Name: ..., Old: ZeroHash, New: batch.Plan.SourceHash}} p.TargetPusher.PushCommands(ctx, cmds) // no pack ``` `PushCommands` → `sendReceivePack(ctx, conn, req, nil, …)` with `packData=nil`, so the request body is the command pkt-lines + flush and **nothing else** (`internal/gitproto/push.go:585`, body assembly at `push.go:293-296`). That's valid git when the objects already exist, but it relies on the server tolerating a pack-less create. entiredb (and likely others) treats every non-delete as "a pack will […]

> AGENT

I'll verify these claims against the actual git-sync codebase. Let me investigate the key files referenced.

> AGENT

I'll dispatch parallel exploration to verify each claim in the report against the real source.

> AGENT

I dug into the actual git-sync source. Your report holds up well — line numbers are accurate and the mechanism is correctly described. Here's the verification, with the one correction worth fixing before you file. ## Primary bug: pack-less subsumed-ref create — ✅ confirmed **`internal/strategy/bootstrap/bootstrap.go:323-337`** (the report didn't pin a line; here it is): ```go if batch.subsumed { cmds := []gitproto.PushCommand{{ Name: batch.Plan.TargetRef, Old: plumbing.ZeroHash, New: batch.Plan.SourceHash, }} if err := p.TargetPusher.PushCommands(ctx, cmds); err != nil { return result, fmt.Errorf("create subsumed branch ref for %s: %w", batch.Plan.TargetRef, err) } ``` The `subsumed` field (struct doc at lines 121-126) explicitly says it "skips the commit-graph fetch, the pack fetch, the temp ref, and the pack push — emitting only a single ref create command." That matches your error string exactly. **`internal/gitproto/push.go`** — your line cites verified: - `push.go:585` — `PushCommands` calls `sendReceivePack(ctx, conn, req, nil, …)` with `packData=nil`. ✅ - `push.go:293-296` — body assembly is `bytes.NewReader(header.Bytes())`, and the pack is appended *only* `if packData != nil`. So with nil it's command pkt-lines + flush, nothing else. ✅ **Empty-pack suggestion:** confirmed there is **no** empty-pack construction anywhere in git-sync today (only `packfile.NewEncoder` for non-empty packs in `PushObjects`). So your suggested fix is […]

> DEVELOPER

let's first fix the empty-pack

> AGENT

Let me read the relevant code before making changes.

> AGENT

Now let me check how the codebase handles pack encoding and hash format, to build a correct empty pack.

> AGENT

git-sync supports SHA-256, so a hardcoded SHA-1 empty pack would be wrong for SHA-256 targets. Let me check how go-git's encoder determines the hash format.

> AGENT

I now have everything I need. The fix: `PushCommands` should attach an empty packfile when the request contains any non-delete command (delete-only pushes must stay pack-less), and the empty pack's trailer must match the target's advertised object format (SHA-1 vs SHA-256). Let me make the edits.

> AGENT

Now the package-level `PushCommands` and the new `emptyPack` helper:

> AGENT

Now let me build and check existing tests in the gitproto package.

> AGENT

Build passes. Let me look at the existing push_test.go to match conventions for a test.

> AGENT

Let me check the test file's imports and the `connForServer` helper.

> AGENT

Now I'll add tests. Let me append them to push_test.go:

> AGENT

All four pass, including the canonical empty-pack golden hash. Let me run the full gitproto suite plus the strategy packages to confirm nothing regressed, and vet.

> AGENT

All green and vet is clean. Let me run the repo's lint task on the package if one exists.

> AGENT

Project lint (`mise run lint`) passed clean, but the bare run flagged a perfsprint nit on my golden-hash line. Let me use `hex.EncodeToString` to satisfy both.

> AGENT

The linter already auto-fixed the line to `hex.EncodeToString`. I added the `hex` import — let me verify there's no duplicate or now-unused `fmt`, then re-run tests and lint.

> AGENT

Lint clean, all tests pass. Here's a summary of the empty-pack fix. ## What changed **`internal/gitproto/push.go`** — the package-level `PushCommands` now attaches a valid empty packfile whenever the request contains a non-delete command: ```go req, _, hasUpdates, err := buildUpdateRequest(adv, commands, verbose) if err != nil { return err } var packData io.Reader if hasUpdates { packData = bytes.NewReader(emptyPack(adv)) } return sendReceivePack(ctx, conn, req, packData, verbose, onRejection) ``` Plus a new helper: ```go func emptyPack(adv *packp.AdvRefs) []byte { header := []byte{'P', 'A', 'C', 'K', 0, 0, 0, 2, 0, 0, 0, 0} algo := crypto.SHA1 if vals := adv.Capabilities.Get(capability.ObjectFormat); len(vals) > 0 && vals[0] == "sha256" { algo = crypto.SHA256 } h := hash.New(algo) _, _ = h.Write(header) return h.Sum(header) } ``` This fixes the subsumed-branch finalize path (`bootstrap.go:324` and `:643`) and any other create/update routed through `PushCommands` — the request body now ends with a 12-byte header + checksum trailer instead of nothing, so a receive-pack that unconditionally reads a pack header (like entiredb) no longer EOFs. ## Two correctness details I made sure of - **Delete-only pushes stay pack-less.** `PushCommands` is also used for temp-ref deletes (`bootstrap.go:375/649`, `replicate.go:78`). Gating on `hasUpdates` means deletes still send no pack, as […]

> AGENT

I'll gather the diff first, then launch the four cleanup agents in parallel.

> AGENT

The changes are uncommitted in the working tree. Let me capture the full diff.

> AGENT

Now I'll launch the four cleanup review agents in parallel.

> AGENT

All four agents reported. Let me dedup and decide: **Converging, high-value fixes:** - **Precompute the two empty packs** (efficiency #1/#2/#3 + simplification #3): the result has exactly two possible values, so build them once at package load instead of hashing on every call. This *also* eliminates the subtle `h.Sum(header)` append-in-place idiom and the per-call allocation. - **Deduplicate the 12-byte header literal** (reuse #1): share one `emptyPackHeader` var between production and the test (same package). - **Extract the test body-capture boilerplate** (simplification #1): the two new tests are near-identical server+channel+select copy-paste. **Skipping (with notes):** - *Generalize the rule into `sendReceivePack`* (altitude #1): the altitude agent itself graded the current placement correct. `sendReceivePack` doesn't have `adv` (no object-format), and `PushObjects` always encodes a real pack via the go-git encoder, so it isn't actually exposed. Moving the rule would mean reworking a shared chokepoint's signature — scope creep for no current benefit. - *Extract a `PreferredObjectFormat` accessor* (altitude #2): single caller; adding it now is speculative generality (YAGNI). Worth revisiting if a second caller appears. - *`var packData` conditional* (simplification #2): agent confirmed already minimal. Let me apply the fixes.

> AGENT

Now the test file: remove the duplicated `emptyPackHeader` var (now lives in push.go), and extract the body-capture boilerplate.

> AGENT

Now rewrite the two tests to use the helpers:

> AGENT

Now build, test, and lint.

> AGENT

Build, tests, and lint all clean. Let me show the final state of the production helper for the record.

> AGENT

Done. `/simplify` complete — build, full `internal/gitproto` suite, and `mise run lint` all pass. ## Fixed 1. **Precomputed the two empty packs** (`push.go`) — the empty-pack bytes depend only on the hash algorithm, so there are exactly two possible outputs. They're now built once at package load (`emptyPackSHA1`, `emptyPackSHA256`) via a small `buildEmptyPack(algo)` helper, and `emptyPack(adv)` just selects between them after the capability check. Removes the per-call hash + allocation in bootstrap's per-branch/per-checkpoint loops, and confines the subtle `Sum`/append construction to one clearly-named builder that uses the unambiguous `append(slices.Clone(header), h.Sum(nil)...)` form. 2. **Deduplicated the 12-byte header literal** (reuse) — `emptyPackHeader` now lives once in `push.go` and is shared by both production and the test (same package), replacing the copy that was in `push_test.go`. 3. **Extracted the test boilerplate** (simplification) — added `captureReceivePackBody(t)` and `awaitBody(t, bodies)` helpers, collapsing the two near-identical ~30-line server/channel/select blocks in the new tests down to a few lines each. ## Skipped (with reasons) - **Generalizing the rule into `sendReceivePack`** (altitude) — the altitude agent itself graded the current placement correct. `sendReceivePack` lacks `adv`/object-format, and `PushObjects` always encodes a real pack through the go-git encoder so it isn't exposed; moving the rule would rework a shared chokepoint's […]