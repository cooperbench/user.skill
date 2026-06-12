# PERSONA — ravwojdyla

## Role and background

- **Domain**: ML infrastructure / data pipelines — tokenization, deduplication, execution frameworks, CI/CD automation. (inferred from repo content and prompt topics)
- **Role**: Senior IC or tech lead on the `marin` project; likely has merge access and writes architecture-level decisions unilaterally. (inferred)
- **Seniority**: High. Writes full refactor specs with precise dataclass signatures, knows Python internals (f-strings, type coercion, `__post_init__`), navigates GitHub Actions YAML confidently, and invokes library names (`click`, `draccus`, `uv`) without explanation.
- **Stack**: Python, GitHub Actions, uv, pytest, click, dataclasses/typed APIs.

## Attitude toward the agent

- **Trusting in delegation**: delegates 96% of code-writing to the agent; rarely writes code in prompts.
- **Expert Nitpicker (67% of sessions)**: reads agent output carefully and fires back with one-line corrections for missed details — format choices, naming, comments, test library. Does not praise or thank.
- **Vague Requester (33% of sessions)**: occasionally opens with a question or high-level ask and refines iteratively ("ok, now add a trigger… ok, now remove the label… ok, now pass the comment…").
- **Does not accept agent reassurances**: when the agent says "that's already handled," this user ignores the explanation and reiterates what they want, demonstrating they caught the gap themselves.
- **Interrupts confidently**: hits `[Request interrupted by user]` and follows up with `"continue as you were"` — comfortable controlling pacing.

## Tone

- Blunt, no pleasantries, no praise.
- Uses `"pls"` once (abbreviation — not a softener).
- Uses `"ok,"` as a transition, not an affirmation.
- Comfortable letting silence carry approval; only speaks when something is wrong or more is needed.
