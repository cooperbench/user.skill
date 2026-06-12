# Preferences — yorrick

## Pushback distribution

- **Non-pushback**: 59.5% — accepts without comment more than half the time
- **Correction**: 34.2% — redirects when tool, scope, or approach is wrong
- **Failure report**: 6.3% — pastes test/command output verbatim expecting silent fix

## What triggers corrections

1. **Wrong tool for the job**: Agent reaches for a shell script instead of a slash command. "are you going to use /dev-loop:workflow?" / "I don't wanna run the dev loop script, I wanna run the workflow."
2. **Scope too narrow**: Agent declares "done" without doing the adjacent required thing. Corrects with short additive messages: "oh also…", "(and add that…)", "add it to CLAUDE.md".
3. **Overgeneralizing a scoped instruction**: "always use opus + max effort for brainstorming, not for everything!" — agent applied max effort everywhere after a scoped instruction.
4. **Missing quality gates**: Agent skips lint/format/typecheck or docs update. CLAUDE.md must encode these as mandatory.
5. **Partial execution**: "I don't want you to run review only. I want you to run everything."
6. **Planning instead of doing**: "Did you create a plan or what? I would like to actually implement this using the /dev-loop:dev-loop."
7. **Wrong packaging decision**: agent suggests standalone repo when plugin constraints make that impractical.

## What satisfies him

- Agent runs the correct slash command without being told twice.
- Minimal output — he doesn't want summaries of what was done, prefers silence or brief status.
- Quality gates run and pass automatically (he set them up in CLAUDE.md; agent should just do it).
- Short yes/no questions when the agent genuinely needs a choice; he picks a letter.
- PR created, merged with minimal ceremony.

## Workflow norms

- **Brainstorm first**: uses `/brainstorming` (Opus + max effort) to write a plan/spec before implementing.
- **Execute with /workflow**: all implementation goes through `/dev-loop:dev-loop` or `/workflow`, not raw scripts.
- **Quality loop**: after each meaningful change — `/simplify` + `/code-review:code-review` + `/security-review` (depending on complexity).
- **Commit cadence**: commits frequently and explicitly — often says "commit and push" as its own message.
- **GH issues for everything**: any improvement or TODO discovered mid-session → "open an issue in GH".
- **No planning docs in conversation**: plan lives in a GH issue or a `/docs/plans/` file, not in chat.
- **Headless execution**: favors `--skip-permissions` and headless agent runs; uses `<task-notification>` output files to read background results.

## Tool/stack preferences

- **Python**: uv, pyproject.toml, pytest. Python 3.14 (early adopter).
- **CI/quality**: ruff (lint), black or ruff-format, mypy/pyright, pytest.
- **Orchestration**: lightweight Python `StateGraph` engine (homegrown), not LangGraph. Nodes call Claude, Codex CLI, or Gemini CLI as subprocesses.
- **Diagrams**: Mermaid in markdown / `--diagram` flag on workflow scripts. Wants diagrams rendered inside Claude Code via browser.
- **Model policy**: Claude nodes by default; Codex/Gemini only if detected as available or repo instructions say so. Brainstorming always uses Opus + max effort; implementation uses Sonnet.
- **No explanations**: does not want the agent to narrate what it did. Just do it.
