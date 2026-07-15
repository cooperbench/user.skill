> TOOL

tool_result
id: toolu_01KWYTv5H96mMdL5iNDPNYMH
```
sync: 2 repos, all bookmarks up-to-date
/home/wink/data/prgs/rust/vc-x1: @- (5e0f61e1e8ce) is not behind 'main' (01357c2bdec7); leaving @ in place
/home/wink/data/prgs/rust/vc-x1/.claude: jj new main
```

> AGENT

Work commit `0.68.0-1` (sync side) is complete:

- `src/sync.rs`: new `repo_bookmark` helper — returns `main` for the session repo (via the existing `is_session_repo` dispatch), the passed bookmark otherwise. Wired into all four per-repo bookmark uses: the tracking preflight (with an info line when the pin overrides a non-`main` bookmark), the `state::save` snapshot, `classify`, `act_on_state` (fast-forward/rebase target), and the `reposition_at` call. Module doc and `--bookmark` help text updated to say the flag is code-repo-only.
- `src/sync/integration_tests.rs`: new scenario 10 `sync_feature_bookmark_pins_session_to_main` — code repo on a pushed `feature` bookmark, session remote advances `main`; asserts the session repo fast-forwards `main`, repositions `@` onto it, and grows no `feature` bookmark, while the code repo syncs `feature`.

Cargo cycle clean (fmt, clippy `-D warnings`, 389+ tests pass, installed `0.68.0-1`), and a live `vc-x1 sync` on this workspace behaves as before.

Ready to commit — please review.