---
name: distill-local-user
description: Distill a user folder (USER.md, PERSONA.md, STYLE.md, PREFERENCES.md, PROJECTS.md, skills/) from a LOCAL trajectory digest built by scripts/build_local_profile.py. Use for digests made from raw on-disk agent logs (Claude Code, Codex, OpenCode, ...), which contain only transcript-derived signal — no LLM-annotated intent/pushback/persona fields. Args: <digest.json path> <output folder>.
---

# Distill a user folder from a LOCAL trajectory digest

You are given a digest built from a developer's own local AI-coding session logs and
must produce a **user folder**: files that capture this developer so precisely that
their requests, corrections, and habits can be reproduced.

Arguments: `$1` = path to the digest JSON, `$2` = output folder `users/<slug>/`.

This is the local-only counterpart to `distill-user`. The crucial difference: the
digest is derived **purely from raw transcripts**. There are **no** annotation-derived
fields (no `intent_distribution`, `pushback_distribution`, `annotated_personas`, no
pre-paired pushback examples). Do not invent them and do not mention them. Infer
everything from the prompt text itself and — when present — from `agent_context`.

## Input shape

1. **Read the digest** at `$1`. It contains:
   - `stats`: quantitative fingerprint derived from the logs — `n_sessions_total`,
     `sources`/`agents` (which CLIs), `repos`, `date_range`, `n_prompts_total`,
     `prompt_words` (median/p90/max), `session_turns_median`.
   - `opening_prompts`: how the user starts sessions (each `{source, project, text}`).
   - `mid_session_prompts`: how they steer mid-session (each `{source, project, text}`).
   - `agent_context` (optional, present only when built with `--agent-context`): a
     sample of sessions, each `{source, project, turns}` where `turns` is an ordered
     list of `{role, text}` with `role` ∈ {`user`, `assistant`, `tool`}. `tool` turns
     are short summaries of what the agent ran (e.g. `Bash: git status`, `edit: src/x.py`).
     Use these to see **what the user's messages were reacting to** — what the agent
     said or did right before a correction, what the user delegates vs. inspects.

## Procedure

1. **Study the evidence before writing.** Identify what makes THIS user distinguishable:
   vocabulary, message length, language(s) and code-switching, casing/punctuation habits,
   typo patterns, politeness/bluntness, domain expertise, what they delegate vs. specify
   precisely, what triggers corrections, pacing (one-liners vs. specs), whether they paste
   errors verbatim, reference files by path, mention tests/commits/PRs.

2. **Use `agent_context` for the relational signal.** Corrections only make sense against
   what preceded them. When a user turn pushes back (`no`, `that's wrong`, `still broken`,
   a re-paste, a sharper tone), look at the prior `assistant`/`tool` turns to characterize
   *what kind of agent behavior* triggers it (a no-op edit, running too much, a wrong
   filter, an ugly plot, an unrequested action). Note what the agent typically runs
   (`tool` turns: which commands/files) and how much the user lets it do autonomously.

3. **Write the folder** (create `$2` and `$2/skills/`):
   - `USER.md` — entry point, < 60 lines. One-paragraph identity sketch; bullet list of the
     5–8 most distinguishing behaviors; pointer to the other files; the cardinal rule:
     *output what this user would literally type, never what a helpful assistant would type*.
   - `PERSONA.md` — background and expertise (inferred, marked as inference), domains, role,
     seniority signals, attitude toward the agent (trusting / skeptical / micromanaging), tone.
   - `STYLE.md` — the typing fingerprint: typical/median message length (use the numbers from
     `stats.prompt_words`), language(s) and code-switching, capitalization, punctuation, emoji,
     typos (preserve them!), formatting (backticks, `@file` paths, pasted logs). Include 8–15
     SHORT verbatim quotes from the digest as calibration, spanning openings, steering, and
     corrections.
   - `PREFERENCES.md` — what they correct or reject and what satisfies them (grounded in the
     prompt text and `agent_context`, NOT in any annotation rate), workflow habits (plan first?
     test-driven? commit cadence? run things themselves? incremental checkpointing?), and
     tool/stack preferences visible in prompts. If `agent_context` is present, ground the
     "what triggers correction" items in concrete agent-action→user-reaction pairs you observed.
   - `PROJECTS.md` — each repo from `stats.repos` with what the user does there (infer from
     prompts/context), tech stack, recurring themes. Mark the dominant repo.
   - `skills/<name>.md` — 2–5 recurring behaviors as skills, each with YAML frontmatter
     (`name`, `description` with a trigger condition) and a body describing the behavior with
     1–2 verbatim examples. Name them after THIS user's habits, not generic ones.
   - `stats.json` — copy the digest's `stats` object verbatim.

## Quality bar

- **Specificity over flattery.** "Experienced developer" is useless; "writes 40-word imperative
  openers full of `@file` refs, all lowercase, pastes full terminal prompts, stacks `!!!` when an
  output didn't change" is gold.
- **Quote real evidence.** Every claim about style should be backed by a verbatim quote present
  in the digest. Preserve typos, casing, and punctuation exactly.
- **Respect the numbers.** If `prompt_words.median` is 9, the folder must scream "terse"; if it's
  42 with a huge p90, capture the "short sessions, occasional giant spec-dump" rhythm.
- **Mark inference.** Anything not directly evidenced (job, seniority, employer) gets "(inferred)".
- **No fabricated annotations.** Never report an intent/pushback/persona distribution or a
  correction *rate* — the local digest has none. Describe behavior qualitatively from evidence.
- **Privacy.** Use only what is in the digest. Do not add real names/employers/locations beyond
  what the prompts themselves reveal.
