> DEVELOPER

i'm reviewing the prs open in this repo specifically the stacks from pr 22 up to 28 lets review the handoff process and its verdicts as that's the focus explain to me the handoff API with an example of how to use it and give me human friendly version of the happy path and failure mode tests that have been written

> AGENT

I'll dig into the handoff process across PRs 22-28. Let me start by looking at the open PRs and finding the handoff code.

> AGENT

The stack is linear: `main → #22 → #23 → #24 → #25 → #26 → #27 → #28`. The focus (handoff + verdicts) lives in `drain_cycle/handoff.py` and `tests/test_handoff.py`. Let me read the cumulative tip (PR #28 / branch `ABA-393`).

> AGENT

Now let me see how the orchestrator consumes these verdicts and lands them in the run log (PR #22–24), plus the KR2 schema check (PR #23).

> AGENT

I have the core picture. Let me confirm who actually writes the file and check the verdict shapes used downstream.

> AGENT

I've got the full picture across the stack. Here's the review of the handoff process and its verdicts. ## What the handoff is `.drain-handoff.json` is the **exit record a stack-mode worker leaves behind** for the orchestrator to read after the worker finishes an issue. It's the one file the supervisor reads to answer three questions on every exit path (Done, halted, or errored): 1. Did the worker actually submit PRs? (`pr_urls`) 2. How did the work self-assess? (`outcome_verdict`, `prep_verdict`) — schema v2 3. If it didn't reach Done, what verdicts did it manage to record before stopping? The module is `drain_cycle/handoff.py`. Note a division of labour: the **`/shape:pr-finishing` skill writes the JSON** (it owns `gt`/`gh` and the file); the Python `write()` is the canonical serializer/test helper. The **orchestrator only reads** — it's the sole reader of `pr_urls`. ## The API Three functions and two dataclasses: ```python @dataclass(frozen=True) class PullRequest: title: str url: str @dataclass(frozen=True) class HandoffData: pr_urls: tuple[PullRequest, ...] outcome_verdict: dict | None = None # the outcome verifier's self-assessment prep_verdict: dict | None = None # the PR-prep routing decision write(worktree: Path, data: HandoffData) -> None read(worktree: Path) -> HandoffData | None # strict: gated on valid pr_urls read_partial(worktree: […]

> DEVELOPER

before we do that, are there are any failure modes that should be added?

> AGENT

Good question to ask before adding more. I went back through `read`/`read_partial` branch by branch and compared against the suite. There are a few genuine gaps — and two of them aren't just "missing test," they're **unspecified behaviour that smells like a latent bug**. ### Worth adding — and possibly a bug **1. Empty `title` is silently accepted (asymmetric with `url`)** The validity check is: ```python if not isinstance(title, str) or not isinstance(url, str) or not url: ``` Note `not url` rejects an empty URL, but there's **no `not title`** — so `{"title": "", "url": ".../pull/1"}` passes and produces a `PullRequest(title="", ...)`. There's no test either way, so it's unclear if that's intentional (title is informational, url is the signal) or an oversight. Either add a test pinning "empty title is OK" or add `not title` to reject it. Right now the behaviour is accidental. **2. A verdict that's a dict but missing `"result"` passes the gate** `_parse_dict` only checks `isinstance(raw, dict)` — it doesn't look inside. But the orchestrator's `_set_verdict_span_attrs` does `outcome.outcome_verdict["result"]` (subscript, line ~220), which **`KeyError`s** on a result-less verdict. (The recovery path uses `.get("result")` and is safe — so it's inconsistent.) `handoff.read` happily lets `{"outcome_verdict": {"foo": 1}}` […]

> DEVELOPER

add that as a comment against the PR first, i want to walk through it all and then do one sweep

> AGENT

Let me confirm which PR owns the handoff module and the `read_partial`/verdict code so the comment lands on the right one.

> AGENT

All of it landed in one commit on PR #22 (`ABA-373-handoff-schema`). Posting the comment there.

> AGENT

Posted to PR #22: https://github.com/ababushkin/drain-cycle/pull/22#issuecomment-4725232550 It covers all six failure modes plus the skip list, ordered for triage: - **#1 / #2** — flagged as contract decisions, not just coverage (empty-title asymmetry; verdict-missing-`result` passing the gate but crashing `_set_verdict_span_attrs`). - **#3** — `read_partial` with `"pr_urls": []` present (the real halt file). - **#4–6** — symmetry + all-or-nothing semantics. Whenever you've walked through it and ruled on #1/#2, I'll do the one sweep — and I can fold in the finishing-recovery test walkthrough at the same time if you want it on the same pass.