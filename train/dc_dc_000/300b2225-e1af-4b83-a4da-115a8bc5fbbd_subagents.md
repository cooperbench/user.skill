---
session_id: "300b2225-e1af-4b83-a4da-115a8bc5fbbd:subagents"
developer: "dc:dc_000"
split: train
source: dataclaw
repo: peteromallet/my-dataclaw-data
start_time: "2026-04-15T10:42:15.238Z"
n_turns: 25
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Explore the megaplan project at /Users/user_c042661f/Documents/megaplan. I need to understand: 1. Overall file structure (ls the top-level and key subdirectories) 2. How CLI commands are registered in megaplan/cli.py — look for argparse subparser patterns 3. How handlers.py dispatches commands — look for handle_* functions 4. How workers are dispatched — find run_codex_step and run_claude_step, understand their signatures 5. How SessionDB works 6. The existing prompt files in megaplan/prompts/ 7. The existing JSON schemas in schemas/ 8. The types defined in megaplan/types.py 9. How existing phases (plan, critique, execute) wire their workers 10. Current version in pyproject.toml Thoroughness: very thorough. Report file paths and line numbers for all key integration points.

> AGENT

I'll conduct a thorough exploration of the megaplan project. Let me start by examining the overall structure and then dive into the specific areas you've requested.

> AGENT

Now let me explore the megaplan directory structure and key files:

> AGENT

Let me continue exploring the subdirectories:

> AGENT

Now let me read the key files to understand the architecture:

> AGENT

Now let me examine the CLI file to understand command registration:

> AGENT

Let me continue reading the CLI file to find the argparse setup:

> AGENT

Now let me examine the handlers file:

> AGENT

Let me search for handle_* function definitions:

> AGENT

Now let me examine the workers file to find run_codex_step and run_claude_step:

> AGENT

Excellent! Now let me read the worker functions:

> AGENT

Now let me look at the state.py to understand SessionDB:

> AGENT

Now let me check the prompt files and then schemas:

> AGENT

Now let me examine schemas.py:

> AGENT

Let me get a sample JSON schema:

> AGENT

Now let me check how phases wire their workers. Let me look at one of the existing phase handler implementations:

> AGENT

Now let me look at the _run_worker function to see how it dispatches:

> AGENT

Now let me check the run_step_with_worker function:

> AGENT

Now let me look at a few more schema examples and understand existing phases better:

> AGENT

Let me check the workflow/state file to understand how phases transition:

> AGENT

Perfect! Now let me look at one more example handler to see the pattern, and examine the critique phase which seems more complex:

> AGENT

Now let me look at the io.py to see database operations:

> AGENT

Now let me check the init file to see what's exported from _core:

> AGENT

Perfect! Now let me compile all this into a comprehensive report. Let me also check one more execution schema to be thorough:

> AGENT

Perfect! Now I have all the information I need. Let me compile a comprehensive report. ## Megaplan Project Architecture — Comprehensive Exploration Report ### 1. OVERALL FILE STRUCTURE **Top-level directories:** ``` /Users/user_c042661f/Documents/megaplan/ ├── megaplan/ # Main package (v0.16.0) ├── tests/ # Test suite ├── .megaplan/ # Runtime state directory ├── .git/ # Git repository ├── pyproject.toml # Package metadata ├── README.md, CHANGELOG.md # Documentation └── Various idea/planning docs ``` **megaplan/ subdirectories:** ``` megaplan/ ├── __init__.py # Package initialization ├── __main__.py # CLI entry ├── cli.py # Command-line interface (43KB) ├── handlers.py # Phase handlers (85KB) — core orchestration ├── workers.py # Worker dispatch (60KB) — Claude/Codex/Hermes runners ├── types.py # Type definitions & constants ├── schemas.py # JSON schema definitions ├── prompts/ # Prompt templates for each phase │ ├── __init__.py # Prompt dispatch tables │ ├── _shared.py │ ├── planning.py │ ├── critique.py │ ├── execute.py │ ├── finalize.py │ ├── gate.py │ └── review.py ├── _core/ # Core infrastructure │ ├── __init__.py # Re-exports all core APIs │ ├── state.py # Plan state, locks, history, sessions │ ├── io.py # Atomic I/O, config, paths │ ├── workflow.py # State machine & transitions │ ├── registries.py # Flag & debt registries │ └── phase_runtime.py # Timeout policy ├── execution.py # Execution orchestration ├── evaluation.py # Gate logic & validation ├── handlers*.py # Various domain handlers ├── parallel_*.py # Parallel phases └── other modules ``` --- ### 2. CLI COMMAND REGISTRATION (megaplan/cli.py) **Command registration pattern: argparse subparsers** **File:** `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py` **Function:** `build_parser()` — lines 802–952 - Creates root `ArgumentParser` with `add_subparsers(dest="command", required=True)` at line 804 - Registers all commands as subparsers **Command categories:** | Command | Lines | Subcommand Args | |---------|-------|-----------------| | `setup` | 806–809 | `--local`, `--target-dir`, `--force` | | `init` | 811–820 | `--project-dir` (req), `--name`, `--auto-approve`, `--robustness`, `--hermes`, `--phase-model` | | `list` | 822–832 | `--all`, `--no-tree`, `--include-done`, `--status`, `--summary` | | `status/audit/progress/watch` | 834–836 | `--plan` | | **Phase steps** (plan, prep, critique, revise, gate, finalize, execute, review) | 838–854 | `--plan`, `--agent`, `--hermes`, `--phase-model`, `--fresh`, `--persist`, `--ephemeral`; execute also has `--confirm-destructive`, `--user-approved`, `--batch` | | `config` | 856–862 | Sub-actions: show, set, reset | | `step` | 864–879 | Sub-actions: add, remove, move | | `override` | 881–886 | Actions: abort, force-proceed, add-note, replan, set-robustness | | `debt` | 888–902 | Sub-actions: list, add, resolve | | `loop-*` (loop-init, loop-run, loop-status, loop-pause) | 904–944 | […]
