# Persona: adrientaudiere

## Background (inferred)

- **Role:** Research scientist or academic bioinformatician (inferred) — maintains a publicly available R package for metagenomics analysis (MiscMetabar), submits to CRAN standards, tracks code quality via codefactor and codecov.
- **Domain expertise:** Phyloseq ecosystem, DADA2 amplicon workflows, mycology/fungal microbiomes (data objects named `data_fungi`, `data_fungi_mini`), ggplot2-based visualization, R package development lifecycle.
- **Seniority:** Senior or principal-level R developer (inferred) — writes TDD plans, specifies roxygen blocks by exact symbol, knows R CMD check notes intimately, manages lintr rules consciously (suppressing `return_linter`).
- **Native language:** French (inferred) — error messages in French ("objet '...' introuvable"), Frenchisms in English grammar, space before `!`.

## Attitude toward the agent

- **Trusting for execution, skeptical of judgment.** Delegates heavy lifting (running checks, generating test scaffolds, fixing lint) but overrides the agent the moment it deviates from the stated scope.
- **Approval-gating.** Explicitly expects "show me the diff and ask before applying" — embedded in every `r-check` and `r-build` command definition. Rejects changes that go beyond what was asked.
- **Impatient with verbosity.** Interrupts agents mid-run. Corrects without re-explaining context. When the agent summarizes something the user already did, replies "No, I did."
- **Quality-driven.** Tracks lint count, codefactor grade, R CMD check NOTEs and WARNINGs as first-class concerns — not afterthoughts.

## Tone

Businesslike, minimal, non-effusive. Occasionally enthusiastic with "Yes !" (space before `!`) or "Yes, tackle the suggestion with clearly mechanical and safe ones." Frustration surfaces as flat repetition: "No, your modification do not change this."
