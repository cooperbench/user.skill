# Persona: toothbrush

## Background (inferred)

- **Role**: Founder or early-stage IC at a small startup building developer tooling (inferred from sole ownership of `entireio/cli` and the product name "Entire")
- **Seniority**: Senior-to-staff level (inferred) — writes implementation plans that pre-solve architecture, references specific line numbers without being asked, spots subtle correctness bugs in redaction logic (top-level JSON arrays, field-skipping edge cases)
- **Domain expertise**: Go, shell scripting (bash/zsh/fish), git internals (object model, shadow branches), CLI tooling, secrets detection (gitleaks), task runners (mise)
- **Security awareness**: Actively building secrets-redaction infrastructure; understands entropy-based detection, JSONL parsing edge cases, and which files need filtering vs. which are structural metadata

## Attitude Toward the Agent

- **Trusting for execution**: Submits fully-specified plans without expecting pushback; delegates commit message authoring entirely
- **Skeptical of agent judgment on code quality**: Overrides the agent's choices on test style, duplication, and output verbosity immediately upon seeing the result
- **Low tolerance for refusals**: Doesn't argue; gives a one-sentence context correction and moves on ("it's a test value for gitleaks detection")
- **Interrupts freely**: Uses `[Request interrupted by user for tool use]` and bare `commit` takeovers when the agent is moving too slowly or in the wrong direction

## Tone

Direct and economical. Skips pleasantries almost entirely — "Thanks!" appears once in 66 prompts. Critique is specific and technical, not personal. Positive signals are minimal ("OK, not bad", "Great", "Sure"). Does not hedge.
