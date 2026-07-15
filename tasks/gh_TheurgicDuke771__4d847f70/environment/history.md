> DEVELOPER

Hey, can you update the @CLAUDE.md §6 to reflect this high level working agreement - One functionality per commit - test coverage for the functionality - docs updation [if required] - agentic code-review on each PR - fix isses in same PR - file issues if defered - full CI gate pass - squash merge to main.

> AGENT

Updated CLAUDE.md §6 with the sequenced working agreement: one functionality per commit → test coverage → docs update → agentic `/code-review` → fix in-PR → file issues if deferred → full CI gate → squash-merge. Note: I only touched CLAUDE.md as you asked — CONTRIBUTING.md's rule 1–4 still describes the older "manual test until Week 8" language, which is now stale (coverage gates are live) and doesn't mention `/code-review` or the file-if-deferred step. Want me to reconcile CONTRIBUTING.md too so the two don't drift?

> DEVELOPER

yes, reconcile @CONTRIBUTING.md

> AGENT

Now update the DoD checklist (rule 5) to reflect the full sequence including CI gate pass and squash-merge.

> AGENT

CONTRIBUTING.md §A now mirrors the same 8-step sequence as CLAUDE.md §6, with the coverage-gate language de-staled (it's live now, not a "Week 8" future state) and cross-links to rules 3/9/13–17 preserved so no numbering elsewhere breaks.