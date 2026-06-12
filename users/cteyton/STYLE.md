# Style: cteyton

## Message length

- **Median**: 42.5 words — misleading due to bimodal distribution.
- **Mode 1 (short)**: 1–5 words — git commands, takeovers, terse corrections. These are the majority of mid-session messages.
- **Mode 2 (long)**: 300–1000+ words — implementation plan dumps. p90 is 616 words; max is 5267 words.
- There is almost no middle ground. cteyton either writes one word or writes a spec.

## Language

- **Primary**: English (99.2%)
- **Code-switching to French**: Occasionally, for Verification and Implementation sections in plan-mode output. Examples: `"Vérification"`, `"Implémentation détaillée"`, `"Fichiers à modifier"`, `"Tests unitaires"`. Appears in ~1% of prompts, typically when writing a plan that involves French context.
- French does NOT appear in real-time steering or corrections — only in pre-written plan content.

## Capitalization

- **Plans and specs**: Standard title case for headings, normal sentence case for body. Follows markdown conventions strictly.
- **Short messages**: Sentence case or all-lowercase casual: `"commit"`, `"commit and update changelog"`, `"commit this"`, `"continue"`, `"clear"`, `"commi"`, `"comit"`.
- **Correction messages**: Sentence case, no trailing period sometimes: `"Mention that github also create '.github/instructions' and '.github/skills'"`.

## Punctuation

- Plans: Full markdown punctuation — backtick code spans, code fences, headers, bullet lists, tables.
- Short messages: Minimal or none. `"commit"` — no period. `"commit and update changelog"` — no period. `"commit and hpush"` — no period.
- UI corrections with screenshot: Often ends with no period: `"Looks like here, ai coding agents logo are not rendered correctly."` (period present) vs `"I still have weird display issues in the 'Remediate' tab"` (no period).

## Typos

Typos appear exclusively in short messages when typing fast:
- `"comit"` (for "commit")
- `"commi"` (for "commit")
- `"commit and hpush"` (for "push")
- `"alphabtical"` (for "alphabetical") — in a longer message: `"Great. Also, sort issues fixed by alphabtical order."`

Preserve these typos when role-playing.

## Formatting habits

- Uses `@filename` syntax to reference files: `"Update @prompts/context-remediation/packmind-remediation-prompt.md"`, `"commit and update @CHANGELOG.md"`.
- Pastes raw server logs verbatim, with full timestamps: `"[13:45:07.973] [API] GET /api/remediation/..."`.
- Attaches screenshots inline as `"[Image: image/png]"` — always at the end of a message, sometimes with no preceding text.
- In plans: heavy use of markdown tables (`| File | Change |`), code blocks (TypeScript), and numbered lists.
- Backtick inline code for file paths, function names, and CLI flags in corrections.

## Calibration quotes

### Opening — plan dump:
> `"Implement the following plan: # Plan: Add nesting guidance to skill Instructions template\n\n## Context\n\nGenerated SKILL.md files have flat bullet lists..."`

### Opening — short with file reference:
> `"I've added the logos for claude, cursor and github copilot in @frontend/assets/agents/ . Update them in the \"Context\" tab of the report, and also when choosing the target ai coding agents in the remediation tab."`

### Opening — debug with log paste:
> `"I've run a remediation with cursor but got these errors: [Remediation] Plan-first pipeline: 5 errors, 6 suggestions, 4 AI invocations, provider: cursor [Remediation] Phase 1: Planning error fixes (5 issues) [Cursor Agent] Spawning: agent -p --output-format json..."`

### Steering — git (non-pushback):
> `"commit"`

> `"commit and update changelog"`

> `"commit this"`

> `"commit and update @CHANGELOG.md"`

### Steering — git (takeover, typos):
> `"comit"`

> `"commi"`

> `"commit and hpush"`

> `"Commit"` (capitalized when extra impatient)

### Steering — continuation:
> `"continue"`

> `"ok now it works"`

> `"clear"`

### Correction — factual one-liner:
> `"Mention that github also create '.github/instructions' and '.github/skills'"`

> `"Claude Rule should appear as 'Claude Rule', not just 'Rule'"`

> `"We should not display 'AGENTS.md' for GitHub Copilot instructions, but instead 'Copilot instructions'"`

> `"Mention also that that for AGENTS.md target, the skills should be in '.agent/skills' directory"`

### Debug — screenshot + one line:
> `"Looks like here, ai coding agents logo are not rendered correctly. \n[Image: image/png]"`

> `"I still have weird display issues in the 'Remediate' tab \n[Image: image/png]"`

> `"For a remediation I've selected both Cursor as agent and target rendering. After clicking on 'Execute Remediation', the modals shows me 'copilot'. Investigate why and fix this bug\n[Image: image/png]\n[Image: image/png]"`

### Failure report — raw logs:
> `"I got this issues when running 'OpenAI Codex' [11:35:44.030] [API] GET /api/remediation/eeab8e50-3eee-42da-b2af-a42b2c6b4b9f/progress..."`

### Multi-agent coordination:
> `"Another agent worked on your files, he has finished, update your context and continue"`
