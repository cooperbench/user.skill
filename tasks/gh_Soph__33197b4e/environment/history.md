> DEVELOPER

Not primarily. The main cause is `--all-refs` itself, not the fact that you previously ran `--tags`.

What the earlier `--tags` run changed is the target state:
- after that run, the target was no longer “empty”
- so the later `--all-refs` run became a sync against an existing target

That can matter, but the important part is this:

- if `--all-refs` produces only branch/tag-style work, relay can still be used
- if `--all-refs` includes “other” refs or ref shapes the relay checks won’t handle, it falls back to materialized

So the difference is not simply:
- first `--tags`, then `--all-refs` => broken

It is more like:
- `--all-refs` exposed refs outside the normal heads/tags set
- on this repo/target state, that made incremental relay ineligible
- therefore the run used materialized push
- that is the HTTP target path currently failing

The earlier `--tags` run may have contributed indirectly by making the target non-empty, which can change planning, but it is not the root reason by itself.

Short version:
- `--tags` did not “poison” the target
- `--all-refs` triggered a different strategy because it covered a broader ref set

If you want, I can inspect the plan logic for this […]

> AGENT

Sure. Here's the same argument in plainer terms.

**The setup**

git-sync has two ways to push to a target:
- **relay** — incremental, cheap, but only works in certain conditions
- **materialized** — full rebuild, more expensive, used as a fallback

You ran two syncs in sequence:
1. one with `--tags`
2. one with `--all-refs`

The second one took the materialized path and hit a bug in materialized's HTTP code. The question was: did step 1 cause step 2 to fail?

**The claim**

No — step 2 would have taken the materialized path regardless, because of what `--all-refs` itself does, not because step 1 ran first.

**Why `--all-refs` is the real cause**

Relay can only handle "normal" refs — `refs/heads/*` and `refs/tags/*`. If a sync includes anything else (e.g. `refs/notes/*`, `refs/pull/*`, custom namespaces), the planner says "relay can't do this" and falls back to materialized.

`--tags` stays inside the safe set. `--all-refs` opens the door to everything, so if the source repo has any non-standard refs, relay is immediately disqualified.

**Why step 1 wasn't innocent either, but only marginally**

Before step 1, the target was empty. After step 1, the target had content. Planning logic can behave differently against an […]