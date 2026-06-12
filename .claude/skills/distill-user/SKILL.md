---
name: distill-user
description: Distill a SWE-chat user's trajectory digest into a role-playable user folder (USER.md, PERSONA.md, STYLE.md, PREFERENCES.md, PROJECTS.md, skills/). Use when asked to distill, extract, or build a user folder/persona from a digest JSON. Args: <digest.json path> <output folder>.
---

# Distill a user folder from a trajectory digest

You are given a digest of a real developer's AI-coding sessions (from the SWE-chat dataset) and
must produce a **user folder**: files that let another agent role-play this developer so
faithfully that its messages are hard to distinguish from the real user's.

Arguments: `$1` = path to `data/digests/<slug>.json`, `$2` = output folder `users/<slug>/`.

## Procedure

1. **Read the digest** at `$1`. It contains:
   - `stats`: quantitative fingerprint (repos, languages, intent/pushback distributions, prompt lengths)
   - `opening_prompts`: how the user starts sessions (their task requests)
   - `mid_session_prompts`: how they steer mid-session
   - `pushback_examples`: agent output that triggered correction/rejection, with the user's reply

2. **Study the evidence before writing.** Identify what makes THIS user distinguishable from a
   generic developer: vocabulary, message length, language(s) and code-switching, casing and
   punctuation habits, typo patterns, politeness/bluntness, domain expertise, what they delegate
   vs. specify precisely, what triggers their pushback, pacing (one-liners vs. specs), whether
   they paste errors verbatim, reference files by path, mention tests/commits/PRs.

3. **Write the folder** (create `$2` and `$2/skills/`):

   - `USER.md` — entry point, < 60 lines. One-paragraph identity sketch; bullet list of the 5–8
     most distinguishing behaviors; instructions to consult the other files; the cardinal rule:
     *output what this user would literally type, never what a helpful assistant would type*.
   - `PERSONA.md` — background and expertise (inferred, marked as inference), domains, role
     (founder/IC/researcher…), seniority signals, attitude toward the agent (trusting/skeptical/
     micromanaging), tone.
   - `STYLE.md` — the typing fingerprint: typical/median message length (give numbers from
     stats), language(s) with code-switching rules, capitalization, punctuation, emoji, typos
     (preserve them!), formatting (backticks, paths, pasted logs). Include 8–15 SHORT verbatim
     quotes from the digest as calibration examples spanning openings, steering, and pushback.
   - `PREFERENCES.md` — what they correct or reject (with the pushback distribution), what
     satisfies them, workflow habits (planning first? test-driven? commit cadence? do they ask
     for explanations or just results?), tool/stack preferences visible in prompts.
   - `PROJECTS.md` — each repo from `stats.repos` with what the user does there (infer from
     prompts), tech stack, recurring themes. Mark the dominant repo.
   - `skills/<name>.md` — 2–5 recurring behaviors as skills, each with YAML frontmatter
     (`name`, `description` with a trigger condition) and a body describing the behavior with
     1–2 verbatim examples. Examples: `terse-redirect.md` (how they cut off a rambling agent),
     `error-paste-debug.md` (how they report failures), `spec-dump-kickoff.md` (how they open
     big tasks). Name them after THIS user's habits, not generic ones.
   - `stats.json` — copy the digest's `stats` object verbatim.

## Quality bar

- **Specificity over flattery.** "Experienced TypeScript developer" is useless; "writes 5–15 word
  imperative messages, all lowercase, Spanish when frustrated, pastes stack traces with no
  commentary" is gold.
- **Quote real evidence.** Every claim about style should be backed by a verbatim quote somewhere
  in the folder. Preserve typos, casing, and punctuation in quotes exactly.
- **Respect the numbers.** If median prompt length is 9 words, the folder must scream "terse".
  If 40% of prompts are `debug` intent, debugging behavior dominates.
- **Mark inference.** Anything not directly evidenced (job, seniority) gets "(inferred)".
- **No PII beyond the dataset.** Use only what is in the digest; the user_id is a public GitHub
  username. Do not speculate about real names, employers, or locations.
