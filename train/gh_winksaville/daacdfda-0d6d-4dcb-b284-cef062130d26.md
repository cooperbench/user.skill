> DEVELOPER

I'm getting this error:
error[E0308]: mismatched types
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/gix-object-0.58.0/src/parse.rs:72:5
    |
 71 | ) -> ModalResult<gix_actor::SignatureRef<'a>, E> {
    |      ------------------------------------------- expected `Result<SignatureRef<'a>, ErrMode<E>>` because of return type
 72 |     gix_actor::signature::decode(i)
    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Result<SignatureRef<'_>, ErrMode<E>>`, found `Result<SignatureRef<'_>, ErrMode<_>>`
    |
note: there are multiple different versions of crate `winnow` in the dependency graph
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/winnow-0.7.15/src/error.rs:104:1


compiling this code on another computer, compiles fine here?

> DEVELOPER

Actually I'm getting the same error when I run `cargo install --path .` but no error `cargo build --release`, weird

> AGENT

That's the classic `cargo install` lockfile gotcha: by default `cargo install` **ignores** your `Cargo.lock` and re-resolves from scratch, which is why it picks up a different (incompatible) winnow version than `cargo build --release` does. Your `Cargo.lock` pins one winnow version that satisfies all gix-* crates; the fresh resolution pulls in two and they collide inside `gix-object`.

Fix:

```
cargo install --path . --locked
```

`--locked` tells cargo to use the existing `Cargo.lock` exactly, matching what `cargo build` does. The "compiles fine on another computer" part is likely just timing — the other machine resolved before whichever upstream crate published the version that triggers the dual-winnow pull-in.

If you want this to be the default, you can also stick this in `.cargo/config.toml`:

```toml
[install]
# (no built-in "always locked" key yet — common workaround is a shell alias
# or just remembering --locked; cargo issue #7169 tracks this)
```

There's no clean config flag for it yet, so the alias / habit route is the practical answer. Want me to update `CLAUDE.md`'s pre-commit checklist (step 4 says `cargo install --path .`) to use `--locked`?

> DEVELOPER

I've never had to do that before, is this because in --locked there is only one version?

> AGENT

Right — `Cargo.lock` records the exact versions cargo resolved to at lock time, and at that moment a single winnow version satisfied everything in the gix-* family. With `--locked`, cargo replays those exact pins, so you get one winnow.

Without `--locked`, cargo re-resolves from scratch using the version *requirements* in each `Cargo.toml`. Since you last locked, some crate in the gix graph (or below it) has published a new compatible release whose winnow requirement no longer overlaps with what its sibling crates pin. Cargo's resolver is allowed to satisfy each independently, so you end up with two winnow versions in the graph — and `gix-object` and `gix-actor` get compiled against different ones, which is why their `ErrMode<E>` types don't match even though they look identical.

"Never had to before" just means you hadn't hit a window where an upstream publish broke the cross-crate winnow agreement. It's episodic — usually resolves itself in a day or two when the lagging crate publishes a matching update, but `--locked` sidesteps it entirely by reusing your known-good resolution.

> DEVELOPER

So a dependency is "locked" to the old version but we're pulling in the new version

> AGENT

Not quite — there's no "old vs new" tug-of-war. Both winnows in the broken build are typically recent; they're just *different* versions (e.g. `0.6.x` and `0.7.x`) that no single pin can satisfy.

The accurate framing:

- **With `--locked`**: cargo replays your `Cargo.lock`, which happens to contain *one* winnow that satisfied every crate's requirement at lock time. One winnow → types match → compiles.
- **Without `--locked`**: cargo re-resolves from scratch and is free to pick the newest semver-compatible version of *each* crate independently. After the latest round of upstream publishes, the gix-* family's winnow requirements no longer have a common solution, so the resolver picks two winnows (one per requirement bucket). `gix-object` and `gix-actor` end up compiled against different ones → type mismatch.

So your lockfile isn't holding anything "back" — it's holding a *coherent* resolution that the fresh resolve can no longer reproduce because the constraint graph has shifted underneath it.

> DEVELOPER

So I did a rustup, cargo clean ...:
wink@3900x 26-04-25T16:54:38.101Z:~
$ rustup update
info: syncing channel updates for stable-x86_64-unknown-linux-gnu
info: syncing channel updates for nightly-x86_64-unknown-linux-gnu
info: latest update on 2026-04-25 for version 1.97.0-nightly (7c61a357e 2026-04-24)
info: removing previous version of component rust-std for target x86_64-unknown-linux-musl
info: removing previous version of component rustc-dev
info: removing previous version of component rustfmt
info: removing previous version of component rust-std for target thumbv7em-none-eabihf
info: removing previous version of component llvm-tools
info: removing previous version of component rust-src
info: removing previous version of component rust-analysis
info: removing previous version of component cargo
info: removing previous version of component clippy
info: removing previous version of component rust-docs
info: removing previous version of component rust-std
info: removing previous version of component rustc
info: downloading 12 components
     rust-std installed                       37.25 MiB
    rustc-dev installed                      115.76 MiB
      rustfmt installed                        2.06 MiB
     rust-std installed                       12.39 MiB
   llvm-tools installed                       37.42 MiB
     rust-src installed                        3.85 MiB
rust-analysis installed                       15.83 KiB
        cargo installed                       10.65 MiB
       clippy installed                        4.59 MiB
    rust-docs installed                       22.45 MiB
     rust-std installed                       28.60 MiB
        rustc installed                       76.33 MiB                                                                                                                                    
  stable-x86_64-unknown-linux-gnu unchanged - rustc 1.95.0 (59807616e 2026-04-14)
   nightly-x86_64-unknown-linux-gnu updated - rustc 1.97.0-nightly (7c61a357e 2026-04-24) (from rustc 1.97.0-nightly (e22c616e4 2026-04-19))

info: checking for self-update (current version: 1.29.0)
info: cleaning up downloads & tmp directories
wink@3900x 26-04-25T16:55:07.585Z:~
$ rustup update
info: syncing channel updates for stable-x86_64-unknown-linux-gnu
info: syncing channel updates for nightly-x86_64-unknown-linux-gnu

   stable-x86_64-unknown-linux-gnu unchanged - rustc 1.95.0 (59807616e 2026-04-14)
  nightly-x86_64-unknown-linux-gnu unchanged - rustc 1.97.0-nightly (7c61a357e 2026-04-24)

info: checking for self-update (current version: 1.29.0)
info: cleaning up downloads & tmp directories
wink@3900x 26-04-25T16:55:10.412Z:~
$ cd data/prgs/rust/vc-x1
wink@3900x 26-04-25T17:37:21.539Z:~/data/prgs/rust/vc-x1 ((main))
$ cargo clean
     Removed 6835 files, 6.5GiB total
wink@3900x 26-04-25T17:37:27.895Z:~/data/prgs/rust/vc-x1 ((main))
$ cargo install --path .
  Installing vc-x1 v0.41.0-0 (/home/wink/data/prgs/rust/vc-x1)
    Updating crates.io index
     Locking 290 packages to latest Rust 1.95.0 compatible versions
      Adding generic-array v0.14.7 (available: v0.14.9)
   Compiling proc-macro2 v1.0.106
   Compiling unicode-ident v1.0.24
   Compiling quote v1.0.45

..
   Compiling gix-pathspec v0.16.1
   Compiling gix-shallow v0.10.0
error[E0308]: mismatched types
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/gix-object-0.58.0/src/parse.rs:72:5
    |
 71 | ) -> ModalResult<gix_actor::SignatureRef<'a>, E> {
    |      ------------------------------------------- expected `Result<SignatureRef<'a>, ErrMode<E>>` because of return type
 72 |     gix_actor::signature::decode(i)
    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Result<SignatureRef<'_>, ErrMode<E>>`, found `Result<SignatureRef<'_>, ErrMode<_>>`
    |
note: there are multiple different versions of crate `winnow` in the dependency graph
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/winnow-0.7.15/src/error.rs:104:1

..
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/winnow-0.7.15/src/error.rs:104:1
    |
104 | pub enum ErrMode<E> {
    | ^^^^^^^^^^^^^^^^^^^ this is the expected type
    |
   ::: /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/winnow-1.0.2/src/error.rs:65:1
    |
 65 | pub enum ErrMode<E> {
    | ------------------- this is the found type
    = help: you can use `cargo tree` to explore your dependency tree
note: associated function defined here
   --> /home/wink/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/gix-object-0.58.0/src/lib.rs:345:27
    |
345 |             pub(crate) fn with_err(err: winnow::error::ErrMode<ParseError>, _remaining: &[u8]) -> Self {
    |                           ^^^^^^^^ ---------------------------------------

For more information about this error, try `rustc --explain E0308`.
error: could not compile `gix-object` (lib) due to 3 previous errors
error: failed to compile `vc-x1 v0.41.0-0 (/home/wink/data/prgs/rust/vc-x1)`, intermediate artifacts can be found at `/home/wink/data/prgs/rust/vc-x1/target`.
To reuse those artifacts with a future compilation, set the environment variable `CARGO_BUILD_BUILD_DIR` to that path.
wink@3900x 26-04-25T17:37:41.990Z:~/data/prgs/rust/vc-x1 ((main))

And that mucked things up?

> AGENT

No, nothing was mucked up. `cargo clean` only removes build artifacts under `target/`; it doesn't touch `Cargo.lock`. And `rustup update` doesn't either.

The smoking gun is right in your output:

```
Locking 290 packages to latest Rust 1.95.0 compatible versions
  Adding generic-array v0.14.7 (available: v0.14.9)
```

That "Locking 290 packages to latest..." line is cargo announcing it just did a fresh resolution from scratch and ignored your `Cargo.lock` — exactly the default `cargo install` behavior I described. The `Adding ... (available: ...)` hint also tells you it's resolving fresh against current crates.io, not replaying the lockfile.

So you're seeing the same problem for the same reason. Try:

```
cargo install --path . --locked
```

That'll skip the fresh resolve, use the winnow that `Cargo.lock` has already pinned (which satisfies all the gix-* crates simultaneously), and the build should go through.

> DEVELOPER

That is weird that `cargo build --release` and I'm guessing `cargo test --release` would have passed but `cargo install --path .` installs something different, that feels broken and would imply `--locked` should be the default?

> AGENT

You're right, and it's a long-standing wart that the cargo team and the community have argued about for years. The behavior is intentional, but the rationale only really fits one case:

- `cargo install <name>` (from crates.io): the published crate may not even ship a `Cargo.lock` (libraries traditionally don't), so cargo re-resolves to get something current. Defensible.
- `cargo install --path .` / `--git ...`: a `Cargo.lock` *is* sitting right there next to the manifest, and it's the same resolution `cargo build` just used. Re-resolving here is the surprising case — it gives you a binary that wasn't built from the same dep graph as your tests passed against.

So your instinct is shared by a lot of people: build/test pass, `cargo install` produces something different, that's a real correctness gap. There have been multiple cargo issues and pre-RFC discussions about flipping the default (or at least making `--path` / `--git` respect the lockfile) — none have landed. The official guidance remains "use `--locked` if reproducibility matters", which is the workaround everyone settles on.

Practical options:

- Add `--locked` to step 4 of the pre-commit checklist in `CLAUDE.md` (`cargo install --path . --locked`). Cheap, fully fixes it for this project.
- Or a shell alias: `alias ci='cargo install --locked'`.

Want me to update the checklist?

> DEVELOPER

What about changing cargo.toml or rust-config.toml(?) neither I nor you should have to remember that

> AGENT

Fair — let me check what cargo actually supports for this rather than guess.

> AGENT

Checked the cargo docs to be sure — and the answer is annoyingly: **there is no config key** for this. `[install]` in `.cargo/config.toml` only controls the install *root directory*, not lockfile behavior. No env var either (no `CARGO_INSTALL_LOCKED` or similar). The cargo team has chosen to keep this CLI-only.

So the realistic "neither of us has to remember" options, ranked:

1. **Update `CLAUDE.md`'s pre-commit checklist** — change step 4 from `cargo install --path .` to `cargo install --path . --locked`. The bot reads CLAUDE.md every session, so it won't forget. This fixes it for *me* permanently.
2. **Shell alias for you** — `alias ci='cargo install --locked'` in your `~/.bashrc` or `~/.zshrc`. Fixes it for *you* permanently.
3. **Project-local cargo alias** — add to `.cargo/config.toml`:
   ```toml
   [alias]
   install-local = "install --path . --locked"
   ```
   Then `cargo install-local`. Discoverable in-repo, but you still have to remember the alias name, so it's weaker than (1)+(2).

I'd do (1) and (2) — they cover both of us with zero new vocabulary. Want me to make the CLAUDE.md edit?

> DEVELOPER

yes, but not yet I need to understand. So build, test always do an implied `--locked` but not install

> AGENT

Almost — one nuance. It's not quite "implied `--locked`":

- **`cargo build` / `cargo test` / `cargo run`**: read `Cargo.lock` if present and use those exact pins. They *will* update `Cargo.lock` if `Cargo.toml` changed (e.g., you bumped a version requirement) or if it's missing entries — but they won't gratuitously re-resolve to newer versions. So in practice, on a clean tree, they behave like `--locked`.
- **`--locked`**: stricter — *errors out* if cargo would need to modify `Cargo.lock` for any reason. It's "use the lockfile, and if you can't, fail."
- **`cargo install` (default)**: ignores `Cargo.lock` entirely and does a fresh resolve, picking the newest semver-compatible version of every dep. That's the "Locking 290 packages to latest..." line in your output.

So your mental model is right where it counts: build/test keep your resolved dep graph stable; install throws it away and resolves fresh. The asymmetry is the bug-feeling part.

> DEVELOPER

I added ci, but I hate that make the change to CLAUDE.md

> AGENT

Done. Step 4 now mandates `--locked` and explains *why* in two lines so a future reader (you or a fresh bot session) doesn't re-litigate the question.

> DEVELOPER

commit

> AGENT

Before I prep the commit, I want to check a couple of things — the current version state is mid-multi-step (0.41.0-0 is the planning marker for the `--scope` continuation work), and this CLAUDE.md change is unrelated to that. I should also look at notes/todo.md and notes/chores to slot this in correctly.

> AGENT

This change is small but unrelated to the in-progress 0.41.0 multi-step (`--scope` continuation). Three reasonable ways to slot it in — they have different history shapes:

- **(a) 0.41.0-1 as a sibling step in the in-progress multi-step.** Simple, but mixes an unrelated process tweak into the `--scope` story.
- **(b) Bump `Cargo.toml` to a separate single-step (e.g., `0.40.1`) before the 0.41.0 work continues.** Clean separation, but interleaves version numbers awkwardly (currently at 0.41.0-0).
- **(c) Defer the commit until after 0.41.0 ships, then make it 0.41.1.** Keeps the in-progress story unbroken; the change is small enough to wait.

I'd lean **(a)** for pragmatism — calling it `chore: require --locked in pre-commit checklist (0.41.0-1)` and noting in the chores file that it's an interlude unrelated to `--scope`. Which do you want?

> DEVELOPER

I agree (a)

> AGENT

Hit a snag: the existing 0.41.0 plan in `chores-06.md:1099-1124` already reserves `0.41.0-1` for `vc-x1 sync --scope=…`. Two ways to handle:

- **(a1) Take `-1` for CLAUDE.md**, renumber the rest of the plan (sync→`-2`, push→`-3`, finalize→`-4`). Update the plan in chores-06.md to reflect the interlude.
- **(a2) Slot CLAUDE.md as the *next free* number after the existing reserved ones** (e.g., `0.41.0-4`), keeping the planned sub-steps intact. But this means committing the CLAUDE.md change *out of natural order* — much later in the sequence than now.

I'd do **(a1)**: it preserves chronological order in git history and the plan rewrite is small. Also let me check how 0.40.0-N sub-steps documented themselves so I copy the right shape.

> AGENT

Going with (a1). Let me set up tasks and execute.

> AGENT

Now update the chores plan and add the 0.41.0-1 subsection.

> AGENT

Now add the `### 0.41.0-1` subsection. It should land inside the `## --scope continuation (0.41.0)` block, after the plan/notes content but before the `# References` section. Let me check the boundary.

> AGENT

Running the pre-commit checklist.

> AGENT

Install with `--locked` succeeded — no fresh resolve, no winnow conflict. Confirming with one quick retest of the new binary.

> AGENT

Pre-commit checklist green. fmt clean, clippy clean (`-D warnings`), 240 tests pass, `cargo install --path . --locked` works (no fresh resolve, version replaced). Here's the proposed message:

**Title** (50 chars):
```
chore: require --locked for cargo install (0.41.0-1)
```

**Body**:
```
Interlude in the 0.41.0 cycle, unrelated to --scope.

Hit a build break on cargo install --path . where
cargo build / cargo test passed cleanly: cargo install
re-resolves from scratch by default and pulled two
incompatible winnow versions into the gix-* graph.
Cargo has no stable config for default --locked, so
the discipline lives in the pre-commit checklist.

- Cargo.toml: bump to 0.41.0-1.
- CLAUDE.md: pre-commit step 4 requires --locked, with
  a two-line reason inline.
- notes/chores-06.md: 0.41.0-1 subsection + plan
  renumber (sync -2, push -3, finalize -4).
```

OK to run `vc-x1 push main` with this title/body?

> DEVELOPER

y

> DEVELOPER

Provide links to recent issues on cargo repo and discussions on rust community board

> AGENT

Here are the relevant threads. The cargo-repo issues are the canonical bug-tracker discussions; the forum links are the design-debate / community-perspective side.

## cargo issues (rust-lang/cargo)

The two most directly relevant to our case:

- [#7169 — "`cargo install` apparently ignores `Cargo.lock` as opposed to `cargo build`"](https://github.com/rust-lang/cargo/issues/7169) — the canonical issue, exact phrasing of the surprise we hit. Open since 2019.
- [#9436 — "`cargo install` on local repo ignores Cargo.lock"](https://github.com/rust-lang/cargo/issues/9436) — narrower variant for the `--path .` case specifically.

Adjacent ones worth knowing about:

- [#14308 — "`cargo install --locked --path .` isn't locking unlike `cargo build --locked`"](https://github.com/rust-lang/cargo/issues/14308) — recent; even with `--locked` there are edge cases.
- [#9289 — "`cargo install --locked` is not really locked"](https://github.com/rust-lang/cargo/issues/9289) — staleness gotcha; `--locked` doesn't enforce that the lockfile is up-to-date with `Cargo.toml` for install.
- [#16649 — contradictory documentation for `cargo install --locked`](https://github.com/rust-lang/cargo/issues/16649) — docs themselves disagree on the behavior.
- [#9106 — warn when `--locked` is used but no `Cargo.lock` exists](https://github.com/rust-lang/cargo/issues/9106).
- [PR #14556 — "lockfile path implies `--locked` on cargo install"](https://github.com/rust-lang/cargo/pull/14556) — incremental fix in this area.

## Community discussion

- [internals.rust-lang.org — "`cargo install --locked` or not locked middle ground?"](https://internals.rust-lang.org/t/cargo-install-locked-or-not-locked-middle-ground/23893) — Jan 2026, the live design debate. Two camps: predictable-as-tested vs. up-to-date-with-security-fixes.
- [users.rust-lang.org — "Cargo install and lock file"](https://users.rust-lang.org/t/cargo-install-and-lock-file/4203) — older but the long-running version of the same complaint.
- [users.rust-lang.org — "`Cargo.{toml,lock}` equivalent for cargo install"](https://users.rust-lang.org/t/cargo-toml-lock-equivalent-for-cargo-install/108703) — people asking exactly what we asked: how to make this the default.

The takeaway from the internals thread is that the cargo team is aware and conflicted, not unaware — which is why it hasn't been flipped despite #7169 being open ~7 years.

Sources:
- [github.com/rust-lang/cargo/issues/7169](https://github.com/rust-lang/cargo/issues/7169)
- [github.com/rust-lang/cargo/issues/9436](https://github.com/rust-lang/cargo/issues/9436)
- [github.com/rust-lang/cargo/issues/14308](https://github.com/rust-lang/cargo/issues/14308)
- [github.com/rust-lang/cargo/issues/9289](https://github.com/rust-lang/cargo/issues/9289)
- [github.com/rust-lang/cargo/issues/16649](https://github.com/rust-lang/cargo/issues/16649)
- [github.com/rust-lang/cargo/issues/9106](https://github.com/rust-lang/cargo/issues/9106)
- [github.com/rust-lang/cargo/pull/14556](https://github.com/rust-lang/cargo/pull/14556)
- [internals.rust-lang.org — middle ground thread](https://internals.rust-lang.org/t/cargo-install-locked-or-not-locked-middle-ground/23893)
- [users.rust-lang.org — Cargo install and lock file](https://users.rust-lang.org/t/cargo-install-and-lock-file/4203)
- [users.rust-lang.org — Cargo.{toml,lock} equivalent](https://users.rust-lang.org/t/cargo-toml-lock-equivalent-for-cargo-install/108703)

> DEVELOPER

add that to a notes/carog-locked-issue.md and point to that file in chores

> AGENT

Note: I'm reading "carog" as "cargo" — typo in the filename. Will create `notes/cargo-locked-issue.md`.

Also flagging upfront: the 0.41.0-1 commit was just pushed and is now immutable. To slot the new file into that chore subsection cleanly, the natural pattern (per CLAUDE.md "Late changes after push") is to squash into `@-` with `--ignore-immutable` and re-push. I'll do the writes first, summarize, and wait for your approval before squashing.

> AGENT

Acknowledged — squash pre-authorized. I'll write, summarize, then squash.

> AGENT

Now point to it from the chores subsection.

> AGENT

Now run the pre-commit checklist (notes-only change, but still runs).

> AGENT

Pre-commit green. Summary of what's about to be squashed into `@-` (the 0.41.0-1 commit on main):

- `notes/cargo-locked-issue.md` (new) — full writeup with the build error, root-cause table, links to cargo #7169 / #9436 / #14308 / #9289 / #16649 / #9106 / PR #14556, and the internals.rust-lang.org middle-ground thread.
- `notes/chores-06.md` — 0.41.0-1 subsection now points at the new file; edits-list bullet added for it.

Squashing now.

> AGENT

Squash + push done. Per CLAUDE.md, clearing stale push state since this was an out-of-band mutation.

> AGENT

Done. The 0.41.0-1 commit on `main` now contains both the original `--locked` checklist change and the new `notes/cargo-locked-issue.md` background doc; bookmark moved to the rewritten commit, push state was already clean. Trailing `.claude` writes (this turn's session) will be picked up by the next `vc-x1 push`.
