> DEVELOPER

Hey, can you update the @CLAUDE.md  §6 to reflect this high level working agreement - 
One functionality per commit - test coverage for the functionality - docs updation [if required] - agentic code-review on each PR - fix isses in same PR - file issues if defered - full CI gate pass - squash merge to main.

> TOOL

tool_use Read
id: toolu_01CZynvMAiFFk93qvRbrqLjf
```json
{
  "file_path": "/home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
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
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "### Commit & change discipline\n- **One functionality per commit** (where possible).\n- **Manually test each committed change before starting the next functionality** (required until unit tests land in Week 8).\n- **Defects → GitHub issue, never silent fixes.** Use `gh issue create`. The fixing PR must include `Fixes #N`.\n- **From Week 8 onward, every new functionality ships with tests.**",
  "new_string": "### Commit & change discipline\nPer-functionality workflow, in order:\n1. **One functionality per commit** (where possible).\n2. **Test coverage for the functionality** (unit/integration as applicable — the ≥80% CI gate, live since Week 8, covers this).\n3. **Docs updated if required** (CLAUDE.md / ADR / CONTRIBUTING / user docs — whichever the change touches).\n4. **Agentic code-review on the PR** — spawn `/code-review` (never an inline self-review only).\n5. **Fix issues found in the same PR** where feasible.\n6. **File a GitHub issue for anything deferred** — never drop a finding silently. Use `gh issue create`; the fixing PR must include `Fixes #N`.\n7. **Full CI gate must pass** (lint/format/types/tests/security — see below).\n8. **Squash-merge to `main`.**"
}
```

> TOOL

tool_result
id: toolu_015qEjXVNc26TuZcxu6aMkpM
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Updated CLAUDE.md §6 with the sequenced working agreement: one functionality per commit → test coverage → docs update → agentic `/code-review` → fix in-PR → file issues if deferred → full CI gate → squash-merge.

Note: I only touched CLAUDE.md as you asked — CONTRIBUTING.md's rule 1–4 still describes the older "manual test until Week 8" language, which is now stale (coverage gates are live) and doesn't mention `/code-review` or the file-if-deferred step. Want me to reconcile CONTRIBUTING.md too so the two don't drift?

> DEVELOPER

yes, reconcile @CONTRIBUTING.md

> TOOL

tool_use Edit
id: toolu_01GNPDWg8XviDkReyLTMAULo
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
  "old_string": "1. **One functionality per commit** (where possible). Each commit must be independently reviewable; do not bundle two unrelated changes.\n2. **Manually test each committed change before starting the next functionality.** Required until the unit-test suite reaches 80% coverage (Week 8 gate). \"Tested\" means: the affected code path was exercised locally, not just that it compiled.\n3. **Defects → GitHub issue first, never silent fixes.** Use `gh issue create --title \"fix: <desc>\"`. The PR that fixes it must include `Fixes #N` in the title or body.\n4. **From Week 8 onward, every new functionality ships with unit tests.** Tests live next to the code they cover (`backend/tests/`, `frontend/tests/`).",
  "new_string": "1. **One functionality per commit** (where possible). Each commit must be independently reviewable; do not bundle two unrelated changes.\n\n   **1a. Every functionality change ships with test coverage** — unit/integration as applicable. Enforced by the ≥80% CI gate (rule 13/14) since the Week-8 flip (2026-07-03); this is no longer a \"from Week 8\" aspiration, it's live and blocking.\n   **1b. Update docs in the same PR if the change is user-facing or architectural** — CLAUDE.md, the relevant ADR, CONTRIBUTING.md, or user docs, whichever applies.\n   **1c. Every […]

> TOOL

tool_result
id: toolu_01GNPDWg8XviDkReyLTMAULo
```
The file /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the DoD checklist (rule 5) to reflect the full sequence including CI gate pass and squash-merge.

> TOOL

tool_use Edit
id: toolu_01X1YComK2YzK5ihyhjZ1tjQ
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
  "old_string": "5. **Definition of Done (DoD)** per task:\n   - Code merged to `main`\n   - Manually tested locally\n   - (From Week 8) unit tests written and passing\n   - Docs / ADR updated if the change is user-facing or architectural\n   - Linked GitHub issue closed if one exists",
  "new_string": "5. **Definition of Done (DoD)** per task, in order:\n   - One functionality per commit (rule 1)\n   - Unit/integration tests written and passing (rule 1a)\n   - Docs / ADR updated if the change is user-facing or architectural (rule 1b)\n   - Manually tested locally (rule 2)\n   - Agentic code review (`/code-review`) run on the PR; findings fixed in-PR or filed as issues (rule 1c)\n   - Linked GitHub issue closed if one exists (rule 3)\n   - Full CI gate green (rule 13–17)\n   - Squash-merged to `main` (rule 9)"
}
```

> TOOL

tool_result
id: toolu_01X1YComK2YzK5ihyhjZ1tjQ
```
The file /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

CONTRIBUTING.md §A now mirrors the same 8-step sequence as CLAUDE.md §6, with the coverage-gate language de-staled (it's live now, not a "Week 8" future state) and cross-links to rules 3/9/13–17 preserved so no numbering elsewhere breaks.

> DEVELOPER

One more thing - add the review findings as a PR comment.

> TOOL

tool_use Edit
id: toolu_019p5WoyvGGDWA3jKAJ9529A
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md",
  "old_string": "   **1c. Every PR gets an agentic code review before merge.** Spawn `/code-review` (never an inline self-review only). Fix what it finds in the same PR where feasible; anything genuinely deferred must be filed as a GitHub issue (rule 3) — never dropped silently.",
  "new_string": "   **1c. Every PR gets an agentic code review before merge.** Spawn `/code-review` (never an inline self-review only), and post its findings to the PR as inline comments (`/code-review --comment`). Fix what it finds in the same PR where feasible; anything genuinely deferred must be filed as a GitHub issue (rule 3) — never dropped silently."
}
```

> TOOL

tool_result
id: toolu_019p5WoyvGGDWA3jKAJ9529A
```
The file /home/<USER>/Coding/Python/DataQ/CONTRIBUTING.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01ARvD4ufQZGCwnhqWAi6PiP
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Coding/Python/DataQ/CLAUDE.md",
  "old_string": "4. **Agentic code-review on the PR** — spawn `/code-review` (never an inline self-review only).",
  "new_string": "4. **Agentic code-review on the PR** — spawn `/code-review` (never an inline self-review only) and post findings to the PR as inline comments (`/code-review --comment`)."
}
```

> TOOL

tool_result
id: toolu_01ARvD4ufQZGCwnhqWAi6PiP
```
The file /home/<USER>/Coding/Python/DataQ/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Both docs now specify posting `/code-review` findings to the PR via inline comments (`--comment` flag), keeping CLAUDE.md §6 and CONTRIBUTING.md rule 1c consistent.