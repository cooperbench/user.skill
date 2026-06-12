# PREFERENCES.md — ujuc

## Pushback distribution

- **non_pushback**: 60.9% — majority of agent output is accepted and he continues
- **correction**: 37.4% — very high correction rate; he is precise about what was wrong
- **takeover**: 0.9% — rare; bypasses agent to do the thing himself (e.g., "커밋해줘" mid-output)
- **rejection**: 0.9% — extremely rare; only "다시 작업해줘" (do it again) observed

## What triggers correction

1. **Agent adds unrequested content**: Verbose "Insight" sections, completion summaries with checkmarks, architectural rationale he didn't ask for. He responds by pasting his actual design principles to overwrite the agent's approach.
2. **Wrong CLAUDE.md philosophy applied**: If the agent includes style rules, linter-level content, or speculative items in CLAUDE.md, he pastes the LLM context principle or his validation checklist.
3. **Document not matching his spec exactly**: Missing or wrong YAML fields, wrong section ordering, wrong placeholder syntax (`[...]` vs `<...>`), content expanded beyond the source.
4. **Wrong layer in document hierarchy**: CLAUDE.md referencing contributing-docs/ directly, AGENTS.md containing Claude-only content, nested CLAUDE.md repeating parent content.
5. **Language policy violation**: English where Korean was requested, or vice versa.
6. **Incomplete task**: Agent stops after one subtask when he expected the whole suite; he pastes the next document to process without comment.

## What satisfies him

- Clean execution of his plan with no additions
- Correct YAML frontmatter with all required fields
- Commit messages in Korean Conventional Commits format
- Short, fact-based completion acknowledgment (not a verbose summary)
- Agent catches a spec issue and asks how to resolve (rare but accepted)

## Workflow habits

- **Plan-first**: Always enters a session with a complete implementation plan from Claude Code's plan mode. Never asks for brainstorming or alternatives mid-session.
- **Pipeline session**: A session is often a multi-document processing run — he pastes each document as the correction/next prompt, and expects the agent to process it sequentially.
- **Commits as checkpoints**: Commits after each logical unit of work (not at end of session). Commit scope is always named explicitly.
- **No test requests**: Only 1.7% test intent. He doesn't ask the agent to write tests; his projects are configuration/documentation.
- **Frequent interruption**: Regularly uses keyboard interrupt (`[Request interrupted by user for tool use]`) when agent tool calls are unnecessary, then continues with a follow-up prompt.
- **Asks clarifying questions in Korean**: Short Korean questions for design decisions ("이거는 새로운 SKILL을 만드는게 좋을까?") before deciding himself.

## Tool/stack preferences visible in prompts

- **Claude Code** exclusively (all 16 sessions)
- **Korean Conventional Commits**: `<type>(<scope>): <한국어 주제 동사형으로 끝남>`
- **CalVer versioning**: `YYYY.MM.Patch` for all documentation
- **YAML frontmatter** for all markdown docs (name, description, version, tags, context, metadata — all required)
- **`git mv`** for moves (history preservation)
- **File references**: `@filename.md` in Claude Code, absolute paths in plans
- **Zsh/macOS tooling**: zimfw, starship, fzf, zoxide, mise
- **No CI/CD**: Configuration repos; pre-commit hooks for markdown linting only
