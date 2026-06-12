# Projects: ashish1099

## Obmondo/gfetch ★ dominant (100% of sessions)

**What it is**: A Go CLI tool that syncs git repositories to local paths. The Obmondo org uses
it for Puppet/OpenVox environment management, where each git branch or tag must live in its own
sanitized directory (hyphens/dots/slashes replaced with underscores).

**Tech stack**: Go, go-git library, YAML config (`pkg/config/`), GitHub Actions (inferred).

**Recurring themes across sessions**:

1. **OpenVox mode implementation** — Adding an `openvox: true` config flag that creates one git
   repo per branch/tag at `local_path/{sanitized_name}/` rather than a single repo with all
   refs. Multiple sessions build on this feature incrementally.

2. **Config struct evolution** — Extending `pkg/config/config.go` to preserve global defaults
   (`global.yaml`) through the load/marshal cycle so `gfetch cat` reflects them correctly.

3. **Ref/tag handling** — Fixing `checkoutRef()` in `pkg/sync/branch.go` to peel annotated
   tags to their target commit (go-git's `repo.TagObject()` → `tagObj.Commit()` pattern) since
   `wt.Reset` requires a commit hash, not a tag object hash.

4. **Name sanitization hardening** — Rewriting `SanitizeName` in `pkg/gsync/openvox.go` from
   a `strings.NewReplacer` (only `-` and `.`) to a `strings.Map` allowlist covering `/`, `@`,
   `~`, `^`, spaces, and anything else outside `[a-zA-Z0-9_]`.

5. **Documentation** — Updating `docs/configuration.md` when new config fields land.

**Key files referenced in prompts**:
- `pkg/config/config.go` — Config struct, `loadDir`, `loadFile`
- `pkg/gsync/openvox.go` — `SanitizeName`, OpenVox sync logic
- `pkg/gsync/openvox_test.go` — `TestSanitizeName`, `TestDetectCollisions`
- `pkg/sync/branch.go` — `checkoutRef`, `syncBranch`
- `syncer.go` — `SyncRepo`, `ensureCloned`, `syncRepoOpenVox`
- `docs/configuration.md` — user-facing docs

**Relationship to the project**: (inferred) maintainer or primary contributor at Obmondo;
designs features independently and uses Claude Code to execute pre-written plans.
