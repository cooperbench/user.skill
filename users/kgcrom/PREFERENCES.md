# Preferences

## Pushback distribution

| Type | Rate | What it looks like |
|------|------|-------------------|
| non_pushback | 71% | Accepts and fires `/commit` or next task |
| correction | 16% | Short Korean sentence pointing at the specific wrong element |
| failure_report | 7% | Korean sentence + screenshot, asking agent to diagnose |
| takeover | 5% | Skips agent's response entirely; sends commit skill spec |
| rejection | 1% | Blunt one-liner ("방금 커밋도 reset해줘") |

## What triggers corrections

- Agent delivers a feature but misses a visual/UX behavior (e.g., active menu highlight not working after screen switch).
- Agent uses wrong language (Korean when English was wanted, or vice versa).
- Agent's commit body message doesn't match the desired format/content.
- Agent skips part of the requested output (e.g., missing eval file in a create-issue task).

## What triggers failure reports

- App renders incorrectly (visual artifact, blank panel, "Loading..." stuck). Always accompanied by a screenshot.
- API returns empty data after a fix that only partially worked ("코스피, 코스닥은 잘 된것 같은데 여전히 업종 리스트 조회는안되고 있어").

## What satisfies kgcrom

- Implementation matches the plan spec exactly — no divergence.
- App runs (`uv run cluefin-desk`) and looks correct on screen.
- Commit message follows the custom format (type in English, Korean summary/body, imperative concise verb forms like "추가", "수정", not "추가하도록 함").

## Workflow habits

- **Plan-first, always**: Does root-cause analysis and writes a full Korean spec before entering the session. Hands spec to agent as the opening message.
- **Commit after every meaningful unit**: Does not batch changes into one commit. Commits frequently, sometimes adjusting commit message or resetting if the body is wrong.
- **No explanation requests**: Rarely asks "why" or "how does this work." When they do ("pypi publish 하려면 어떻게 해야돼?"), it's a one-liner.
- **Issue tracking**: References GitHub issue numbers in commit args (`#19 issue number`, `#19 issue progress`).
- **PR creation**: Writes PRs in Korean with English conventional commit type prefix. Uses `gh pr create`.
- **Verification by running the app**: Always verifies by running `uv run cluefin-desk`, not by reading code or running tests.
- **Interrupts freely**: Uses `[Request interrupted by user for tool use]` when the agent is mid-action and something else is needed.

## Tool/stack preferences

- **Python + uv**: Package manager of choice; uses `uv run`, `uv build`, `uv publish`.
- **Textual**: TUI framework for cluefin-desk. Knows widget internals (Static vs Widget, reactive, recompose).
- **GitHub CLI (`gh`)**: For all GitHub operations — PRs, issues, repo description.
- **Bun/TypeScript**: For agent-foundry CLI tooling (`bun run validate`, `bun test`, `bun run check`).
- **loguru**: Logging library in Python projects.
- **plotext + rich**: Chart rendering and ANSI-to-Rich conversion.
- **Kiwoom/KIS API**: Korean brokerage APIs; uses numeric API IDs (ka10019, ka10063, etc.).
- **DART API + XBRL**: Korean corporate disclosure and financial statement parsing.
- **Pydantic**: Data validation in API response models; aware of aliasing behavior.
- **Literal types**: Uses them for strict API parameter validation.
