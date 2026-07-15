> DEVELOPER

when and why did we set a hard refresh interval on zwave locks? I thought we had decided before that we always get events with User Code CC with the only potential gap being an external program but we shouldn't worry about that. User Credential CC has notifications too, so what changed?

> AGENT

Please run /login · API Error: 401 Invalid authentication credentials

> DEVELOPER

when and why did we set a hard refresh interval on zwave locks? I thought we had decided before that we always get events with User Code CC with the only potential gap being an external program but we shouldn't worry about that. User Credential CC has notifications too, so what changed?

> AGENT

I'll investigate the history of the refresh interval on Z-Wave locks. Let me look at the code and its git history.

> AGENT

Let me read the relevant code with the docstrings explaining the rationale, and find where the periodic interval is set.

> AGENT

There's a reference to an "hourly hard-refresh backstop." Let me find where that interval is actually scheduled.

> AGENT

Found it. The Z-Wave hard refresh is set in `zwave_js.py`. Let me read the rationale and then check git history for when/why it was introduced.

> AGENT

Now let me trace the git history to find when and why this was introduced.

> AGENT

PR #1227 introduced it. Let me check whether the old (pre-#1227) Z-Wave provider had any such interval, and read the base-class framing to understand the "what changed."

> AGENT

The mechanism is older than #1227 — it dates to PR #693 "Add push-based coordinator updates with drift detection." Let me check what the pre-#1227 Z-Wave provider actually set as its interval, and read the #693 framing.

> AGENT

Pre-#1227, the Z-Wave provider didn't override `hard_refresh_interval` at all — so it inherited the base default. Let me confirm what that default was at the time.

> AGENT

I have the timeline. Let me pull the PR #1227 rationale and see what `entire` offers for extra context.

> AGENT

The PR body line 13 is the smoking gun. Let me try `entire explain` on that commit as you suggested, to see if it surfaces the original session reasoning.

> AGENT

Here's the full picture, traced through git history and the PR #1227 description. ## When The hourly interval on Z-Wave locks was added in **PR #1227** (`feat(zwave_js): migrate to unified access_control credential API`, commit `4f1e4946`). That's the credential-management refactor branch. The *mechanism* is much older — `hard_refresh_interval` + the coordinator's drift timer goes back to PR #693 ("Add push-based coordinator updates with drift detection"). But the base-class default is `None` (disabled), and **pre-#1227 the Z-Wave provider never overrode it**. So legacy User Code CC locks had *no* hourly hard refresh. Your recollection is correct: you trusted the events, treated external programming as the only gap, and didn't worry about it. #1227 is where `zwave_js.py` first added: ```python @property def hard_refresh_interval(self) -> timedelta | None: return timedelta(hours=1) ``` ## Why — what actually changed It wasn't that notifications got less reliable. **The push source changed.** From the PR #1227 body (line 13): > **Push** moves from User Code CC value events to the access-control credential node events (`credential added` / `modified` / `deleted`); lock/unlock **operation** notifications still drive the code-slot events. A 1-hour `hard_refresh_interval` backstops missed events. Old path: you read User Code CC **value-updated events** — the event *is* the […]

> DEVELOPER

so the only point her eis to get a readable code? We can't even guarantee we will get a readable code if the lock masks it, so why not just fall back into that path when that happens?

> AGENT

Good challenge — let me not hand-wave this. The question is really: *what does the hourly poll uniquely catch that an on-demand fallback can't?* Let me trace what the refresh actually reconciles and whether a value-less event already triggers an on-demand read.

> AGENT

Let me check one more thing that decides whether "stranded unreadable" is even a real problem worth backstopping: how the sync predicate treats `observed=unreadable` vs `desired=known`.

> AGENT

This is a genuinely sharp catch, and tracing it through the code, you're largely right. Let me lay out what the hourly poll *actually* does versus what the docstring claims. ## The readability justification is weak — you've identified that correctly Two things confirm your instinct: **1. The value-less-event case is already handled inline, with no re-read.** `_on_credential_changed` (zwave_js.py:586) reads `args.data` straight from the event and pushes `_pin_state(args.data)`. If the value is absent/masked it pushes `unreadable` — it does *not* trigger an on-demand refresh. So a refresh isn't even the fallback for "event arrived without a value." And as you say, on a masking lock a re-read returns masked anyway, so there's nothing to recover. **2. An "unreadable" slot isn't actually stranded in any harmful way** — *if we set it*. `calculate_in_sync` (sync.py:427): ```python if not credential.is_readable: return slot_state.pin_state == self._last_set_pin ``` An unreadable slot whose `_last_set_pin` matches the configured PIN is **in sync**. No rewrite, no churn. So the "stranded as unreadable" scare in the docstring only bites a slot we *didn't* set (or one where `_last_set_pin` was lost, e.g. across restart) — and the hourly refresh can't un-mask it anyway. So: for masking locks, the hourly poll buys […]

> DEVELOPER

lets drop the refresh. The important thing is that nothign has changed that changes what that drift captures after adding U3C support