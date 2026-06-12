# Style: armelhbobdad

## Message length

- **Median**: 21 words (stats). Majority of turns are 1–30 words.
- **p90**: 306 words — triggered by pasting plans, terminal output, or structured specs.
- **Max**: 3,004 words — full implementation plans pasted verbatim.
- Bimodal: either a single token or a wall of structured markdown.

## Language and code-switching

- English throughout; no French words in prompts.
- French-influenced English spelling — consistent, not random:
  - "complexe" (not "complex")
  - "recommandation" (not "recommendation")
  - "valide" (not "valid")
  - "usefull" (not "useful")
  - "compisitions" (not "compositions")
  - "extrated" (not "extracted")
  - "specfic" (not "specific")
  - "avaible" (not "available")
  - "yoursefl" (not "yourself")
  - "seciton" (not "section")
  - "ect..." (not "etc.")

## Capitalization and punctuation

- Sentence case for full sentences; often skips terminal period on short prompts.
- ALL CAPS for critical override commands only.
- No emoji in normal turns; occasional excitement in party-mode follow-ups.
- Uses markdown formatting in longer prompts: `##`, `###`, tables, code blocks.
- Backtick wraps: tool names (`skill-forge`, `npx bmad-module-skill-forge`), file paths
  (`` `README.md` ``), code snippets, terminal commands.

## File and path references

- `@path/` or `@filename.md` syntax — always, never just a bare name.
- Examples: `@src/`, `@docs/`, `@README.md`, `@website/src/content/docs`, `@package.json`

## Terminal output pasting

Pastes verbatim, including banners, prompts, and error traces. No trimming.
Example: pastes the full `armel@dzeta:~/Projects/demo/fast$` session.

## Calibration quotes

**Opening — debug with file ref:**
> "the mermaid diagram from @docs/architecture.md is not rendered in the astro @website/ . Please use https://github.com/joesaby/astro-mermaid to fix"

**Opening — question with file refs:**
> "is it important to add `nodeJs` as a prerequisite accross all docs ( @README.md , @docs/ @_bmad-output/planning-artifacts/medium-article-skf.md )? It is need to run npx command where is needed."

**Short correction:**
> "commit the previous work first then implement the simplest high-value option (click-to-expand)"

**Factual correction:**
> "you said \"Skill Forge (SKF) — Part of the BMad Method ecosystem.\" from the @README.md . It is not the case for the moment."

**ALL CAPS critical override:**
> "IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL {project-root}/_bmad/bmb/workflows/module/workflow-edit-module.md, READ its entire contents and follow its directions exactly!"

**Terse confirm:**
> "yes"

**Terse git:**
> "commit"

**Single-letter shortcut:**
> "E"

**Error report with terminal output:**
> "Are you sure it works? I just tried it here but look at the `fast` repo: armel@dzeta:~/Projects/demo/fast$ node /home/armel/Projects/OSS/bmad-module-skill-forge/tools/skf-npx-wrapper.js install ..."

**Failure report — light mode not tested:**
> "you did not test it in light mode"

**Pivot correction:**
> "Actually, we use `qmd` for deep tier."

**Pre-push review:**
> "Deep review the changes from the last 7 commits for any breaking changes, or missing impact and ect..."

**Party-mode pivot:**
> "Let's go to the party mode for multiple point of views."

**Hard rejection:**
> "drop"
