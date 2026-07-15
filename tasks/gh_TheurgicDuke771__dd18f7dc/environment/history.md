> DEVELOPER

Hey, can you update the @CLAUDE.md  §6 to reflect this high level working agreement - 
One functionality per commit - test coverage for the functionality - docs updation [if required] - agentic code-review on each PR - fix isses in same PR - file issues if defered - full CI gate pass - squash merge to main.

> TOOL

tool_use Read
id: toolu_01CZynvMAiFFk93qvRbrqLjf
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/CONTRIBUTING.md",
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01CZynvMAiFFk93qvRbrqLjf
```
1	# Contributing to DataQ
2	
3	> Working agreements for everyone (human and AI) writing code in this repo. These rules are locked in Week 1 and override any "speed > quality" temptation. If a week's exit gate conflicts with them, **the rules win**.
4	
5	---
6	
7	## A. Commit & change discipline
8	
9	1. **One functionality per commit** (where possible). Each commit must be independently reviewable; do not bundle two unrelated changes.
10	2. **Manually test each committed change before starting the next functionality.** Required until the unit-test suite reaches 80% coverage (Week 8 gate). "Tested" means: the affected code path was exercised locally, not just that it compiled.
11	3. **Defects → GitHub issue first, never silent fixes.** Use `gh issue create --title "fix: <desc>"`. The PR that fixes it must include `Fixes #N` in the title or body.
12	4. **From Week 8 onward, every new functionality ships with unit tests.** Tests live next to the code they cover (`backend/tests/`, `frontend/tests/`).
13	
14	   **4a. Test for failure modes, not just the happy path.** Lesson from the column-profiler bugs ([#145](https://github.com/TheurgicDuke771/DataQ/issues/145)/[#147](https://github.com/TheurgicDuke771/DataQ/issues/147)): the profiler sat at ~94% line coverage and still `500`d […]

> TOOL

tool_use Edit
id: toolu_015qEjXVNc26TuZcxu6aMkpM
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "### Commit & change discipline\n- **One functionality per commit** (where possible).\n- **Manually test each committed change before starting the next functionality** (required until unit tests land in Week 8).\n- **Defects → GitHub issue, never silent fixes.** Use `gh issue create`. The fixing PR must include `Fixes #N`.\n- **From Week 8 onward, every new functionality ships with tests.**",
  "new_string": "### Commit & change discipline\nPer-functionality workflow, in order:\n1. **One functionality per commit** (where possible).\n2. **Test coverage for the functionality** (unit/integration as applicable — the ≥80% CI gate, live since Week 8, covers this).\n3. **Docs updated if required** (CLAUDE.md / ADR / CONTRIBUTING / user docs — whichever the change touches).\n4. **Agentic code-review on the PR** — spawn `/code-review` (never an inline self-review only).\n5. **Fix issues found in the same PR** where feasible.\n6. **File a GitHub issue for anything deferred** — never drop a finding silently. Use `gh issue create`; the fixing PR must include `Fixes #N`.\n7. **Full CI gate must pass** (lint/format/types/tests/security — see below).\n8. **Squash-merge to `main`.**"
}
```

> TOOL

tool_result
id: toolu_015qEjXVNc26TuZcxu6aMkpM
```
The file /Users/arijit/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Updated CLAUDE.md §6 with the sequenced working agreement: one functionality per commit → test coverage → docs update → agentic `/code-review` → fix in-PR → file issues if deferred → full CI gate → squash-merge.

Note: I only touched CLAUDE.md as you asked — CONTRIBUTING.md's rule 1–4 still describes the older "manual test until Week 8" language, which is now stale (coverage gates are live) and doesn't mention `/code-review` or the file-if-deferred step. Want me to reconcile CONTRIBUTING.md too so the two don't drift?