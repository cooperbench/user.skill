> DEVELOPER

Explore the megaplan codebase at /Users/user_c042661f/Documents/megaplan to gather information needed to plan a new model-profile feature. Report in under 500 words, focused on concrete file paths and line references. Specifically find: 1. **CLI surface** (`megaplan/cli.py`): - Which subcommand parsers currently add `--phase-model` and `--hermes` (expected: init, step, loop-init, loop-run, chain, tiebreaker). Report the exact function/block names and approximate line numbers. - Pattern used for adding arguments (shared helper? repeated code?). - Existing `config` subcommand structure if any (for `config profiles list/show`). 2. **DEFAULT_AGENT_ROUTING** in workers.py or elsewhere — list all the phase keys including tiebreaker sub-phases (tiebreaker_orchestrator, tiebreaker_challenger, tiebreaker_researcher, tiebreaker_synthesis). Confirm the canonical list. 3. **parse_agent_spec** — file path and how it parses "hermes:model/name" strings. 4. **load_config** — where it reads TOML/YAML config, what format, what keys. This is relevant because we need to understand the existing config pattern. 5. **state.py** — confirm structure of `state["config"]` and where it's populated at plan-init time. Look for functions that snapshot CLI args into config. 6. **Existing TOML/tomllib usage** — does the project already use tomllib or another parser? Check pyproject.toml / imports. 7. **Test layout** — where are tests? `tests/` directory? What test framework (pytest)? Report a pattern for a new test file. 8. **The hermes vendor plan dependency** — check if `megaplan/hermes_worker.py` or similar has recently been split or is in flux. Look at git log for any in-progress vendor work. Do NOT read anything under `.megaplan/` (prior plan artifacts). Focus on source, tests, pyproject.toml, and top-level README if needed for config locations. Do NOT go exploring ops/docs directories. Return paths with line numbers where possible.

> AGENT

I'll systematically explore the megaplan codebase to gather the information needed for the model-profile feature. Let me start with the core files.

> AGENT

Now let me look at the specific files mentioned in the requirements:

> AGENT

Now let me examine the types.py to find DEFAULT_AGENT_ROUTING and parse_agent_spec:

> AGENT

Now let me check the types.py file for DEFAULT_AGENT_ROUTING and parse_agent_spec:

> AGENT

Now let me check _core for load_config, save_config, and state-related functions:

> AGENT

Now let me check the state.py and look for how config is populated:

> AGENT

Now let me check handlers/init.py to see how config is populated at init time:

> AGENT

Now let me check the git log to see recent work on hermes_worker.py and check for test structure:

> AGENT

Now let me verify the tiebreaker orchestrator parser and check the chain.py for YAML usage:

> AGENT

Let me also check workers.py for parse_agent_spec usage and get the auto.py handler structure:

> AGENT

Let me get the key areas for resolve_agent_and_model function:

> AGENT

Perfect! Now let me compile the final report. I have enough information to provide a comprehensive analysis. ## Summary Report: Model-Profile Feature Exploration Based on systematic exploration of the megaplan codebase, here are the key findings organized by requirement: ### 1. **CLI Surface** (`megaplan/cli.py`) **Subcommands with `--phase-model` and `--hermes` arguments:** - **init** (line 869-872): `--hermes` with optional model, `--phase-model` with append action - **plan, prep, critique, revise, gate, finalize, execute, review** (lines 895-914): all have both flags - **loop-init** (lines 985-988): both flags present - **loop-run** (lines 1002-1005): both flags present - **tiebreaker-run** (lines 1039-1046): both flags present - **chain** (via `build_chain_parser` at line 1025): not visible in main cli.py but uses same pattern - **tiebreaker** (via `build_tiebreaker_parser` at line 1034): external builder **Pattern used:** Repeated code blocks—no shared helper. Each parser explicitly adds both arguments (lines 871-872, 898-901, 985-988, 1002-1005, 1045-1046). **Existing config structure:** `config show/set/reset` subcommand exists (lines 916-922). Currently supports `agents.<step>` config keys and direct settings. No `profiles` subcommand yet. ### 2. **DEFAULT_AGENT_ROUTING** (`megaplan/types.py`, lines 305-318) Complete routing table confirmed: ```python DEFAULT_AGENT_ROUTING = { "plan": "claude", "prep": "claude", "critique": "codex", "revise": "claude", "gate": "claude", "finalize": "claude", "execute": "codex", "loop_plan": "claude", "loop_execute": "codex", "review": "codex", "tiebreaker_researcher": "codex", "tiebreaker_challenger": "codex", } ``` No `tiebreaker_orchestrator` or `tiebreaker_synthesis` as phase keys; these are orchestration phases, not routing targets. ### 3. **parse_agent_spec** (`megaplan/types.py`, lines 321-326) Location: `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:321` Implementation: ```python def parse_agent_spec(spec: str) -> tuple[str, str | None]: """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None).""" if ":" in spec: agent, model = spec.split(":", 1) return agent, model return spec, None ``` **Usage in workers.py** (line 1633, 1646, 1651): Called to extract model from `--phase-model` and `--hermes` arguments. ### 4. **load_config** (`megaplan/_core/io.py`, lines 229-241) Location: `/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py:229` - Reads from `~/.config/megaplan/config.json` (XDG_CONFIG_HOME aware) - Format: JSON dict - Currently stores: `agents` (routing map) and various execution settings (`auto_approve`, `robustness`, worker timeouts, etc.) - Config is loaded at runtime and merged with `DEFAULTS` via `get_effective()` **save_config**: Line 244—writes same JSON format atomically. ### 5. **state.py** (`megaplan/_core/state.py`) **state["config"]** structure initialized at plan init (`megaplan/handlers/init.py:105-111`): ```python "config": { "project_dir": str(project_dir), "auto_approve": auto_approve, "robustness": robustness, "mode": mode, "agent": "hermes" if getattr(args, "hermes", None) is not None else "", } ``` Additional config keys added conditionally: - `output_path` (line 127, for doc/joke modes) - `primary_criterion` (line 129, for joke mode) - `from_doc` (line 131, for doc imports) **Note:** Currently only stores a simple boolean "agent" flag, not […]
