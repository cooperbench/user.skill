> DEVELOPER

I'm planning a Sprint 2 feature for the `megaplan` CLI at /Users/user_c042661f/Documents/megaplan/: a `megaplan bakeoff` subcommand that runs the same idea through N profiles concurrently in git worktrees, then compares and merges results. I need a thorough but focused map of the current codebase, NOT prior plan artifacts (ignore `.megaplan/` directories). Focus on source in `megaplan/` and relevant tests. Report (be concise, use file:line refs): 1. **CLI structure**: Where is the top-level argparse wired? How are subcommands registered? (Look at `megaplan/cli.py`, `megaplan/__main__.py`.) I need to know how to add a new `bakeoff` subcommand group with sub-subcommands like `bakeoff run`, `bakeoff status`, etc. 2. **`megaplan auto` driver**: Where does it live (probably `megaplan/auto.py`)? What's its entry point / signature? How does it know which plan dir to operate on — is it CWD-based, or explicit flag? What is the `DriverOutcome` type and where is `DriverOutcome.status` defined? List the status values. 3. **Plan state**: Where is `state.json` written and loaded? What's the structure (especially `state.json.config.project_dir` which the brief mentions contains absolute paths)? What directory does `.megaplan/plans/<plan-id>/` contain? 4. **Profiles**: How are named profiles defined (`megaplan/profiles/`)? What's the format of `standard.toml`? How are they loaded and how does `--profile` flag work currently? 5. **Plan directory discovery**: Grep for `rglob` and `.megaplan` to understand the "circular recursion" risk the brief mentions — how does megaplan currently find plan dirs? 6. **Step receipts (Sprint 1 prerequisite)**: Grep for "receipt" or "step_receipt" or similar. Does this concept exist in the codebase already? Is there a canonical prompt hash? A global audit log? The brief says these are a prerequisite — I need to know whether they're implemented or still pending, because bakeoff compare uses receipts as the primary metric source. 7. **Scope drift**: Grep for "scope_drift" or "scope drift" — is this a first-class metric already? 8. **Existing subprocess orchestration**: Does `megaplan` already shell out to itself or to other processes? Any use of `asyncio.create_subprocess_exec` or `subprocess.Popen`? The brief says "auto-driver already shells out per phase" — verify. 9. **Tests**: What's the test layout at `/Users/user_c042661f/Documents/megaplan/tests/`? How are CLI subcommands typically tested? 10. **Git worktree usage**: Any existing worktree code in the repo? 11. **Phase artifacts**: Where does each phase write its artifact (plan_v1.md, critique_v*.json, execution.json, review_output.json)? Just the directory layout, not the full contents. 12. **pyproject.toml**: What's the package name, Python version, current deps (especially asyncio-related, toml parsing)? Keep it tight — I need enough […]

> AGENT

I'll conduct a focused exploration of the megaplan codebase to answer your questions. Let me start with the overall structure and then drill into specifics.

> AGENT

Now let me explore the main entry points and structure:

> AGENT

Now let me search for auto.py, state.py, and profiles code:

> AGENT

Let me search for profiles:

> AGENT

Now let me search for key terms from the brief:

> AGENT

Let me check for rglob and circular recursion references:

> AGENT

Now let me check profiles and pyproject.toml:

> AGENT

Now let me look at tests and phase artifacts:

> AGENT

Let me check the loop worktree code and more on auto driver:

> AGENT

Let me search for more info on state.json structure and artifact directories:

> AGENT

Let me check the types to understand DriverOutcome and plan state:

> AGENT

Perfect! Now let me check for handlers and phase structure:

> AGENT

Now let me look for the prep and revise handlers and check build_auto_parser:

> AGENT

Now let me get a comprehensive look at the auto.py final parts and check for phase artifacts locations:

> AGENT

Perfect! Let me now look for receipt/step_receipt more carefully and get info on latest_*_path functions:

> AGENT

Now let me do a final check on the directory layout by looking at an example plan directory:

> AGENT

Perfect! Now let me check for receipts more comprehensively:

> AGENT

So receipts don't exist yet. Now let me check the loop engine for worktree code:

> AGENT

Perfect! Now let me verify some final details about DriverOutcome status values:

> AGENT

Perfect! Now let me verify one more detail about the additional status values I saw:

> AGENT

Excellent! Now I have a comprehensive map. Let me create the final report: --- ## Megaplan Codebase Map for Sprint 2 (`bakeoff` Feature) ### 1. **CLI Structure & Subcommand Registration** **Entry points:** - `/Users/user_c042661f/Documents/megaplan/megaplan/__main__.py:3` — imports `main()` from CLI - `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:1193-1276` — `main()` function: dispatcher for all CLI commands - `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:864-1108` — `build_parser()` constructs argparse tree **How subcommands are registered:** - Parser uses `subparsers.add_parser(name)` pattern (e.g., cli.py:868 for "setup", cli.py:873 for "init") - Dynamic subcommand builders called in `main()` (e.g., auto.py:484-560 via `build_auto_parser`, chain.py via `build_chain_parser`) - Handler dispatch via dict: `cli.py:1111-1136` COMMAND_HANDLERS maps command name to handler function - Example handler signature: `handle_init(root: Path, args: argparse.Namespace) -> StepResponse` (cli.py:1112) **To add `bakeoff` subcommand group:** - Create `build_bakeoff_parser(subparsers)` function in a new `megaplan/bakeoff.py` module - Add sub-subcommands: `bakeoff run`, `bakeoff status`, `bakeoff compare`, `bakeoff merge` (using nested `add_subparsers`) - Call from `cli.py:main()` around line 1076-1080 (after auto/chain imports) - Add handlers dict entries in COMMAND_HANDLERS --- ### 2. **Auto Driver (`megaplan auto`)** **Location & entry point:** - `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py` — entire driver implementation - `build_auto_parser()` — line 484-560 (parser definition) - `run_auto(root, args)` — line 561-590 (CLI handler) - `drive(plan, *, cwd=None, ...)` — line 177-481 (core loop, CWD-based discovery) **How it discovers plan dir:** - `_resolve_plan_dir(plan, cwd)` — line 139-152: walks up parents from `cwd` looking for `.megaplan/plans/<plan>`, matches `megaplan status` logic - Returns `None` if not found (safe fallback for optional features) **Entry point signature:** ```python def drive(plan: str, *, cwd: Path | None = None, stall_threshold=5, max_iterations=200, ...) -> DriverOutcome ``` **DriverOutcome type & status values:** - Defined at `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py:50-74` as `@dataclass` - `status` field can be: `"done"` | `"stalled"` | `"escalated"` | `"failed"` | `"aborted"` | `"cap"` | `"blocked"` | `"awaiting_human"` | `"tiebreaker_pending"` | `"tiebreaker_ready"` (see lines 246-289 for terminal state handling) - Exit codes: 0 (done/aborted), 2 (stalled), 3 (escalated), 4 (cap), 5 (blocked), 1 (other failures) — line 575-590 **Subprocess orchestration:** - `_run_megaplan(args, cwd, timeout)` — line 77-109: uses `subprocess.run([sys.executable, "-m", "megaplan", *args], ...)` - Each phase runs as fresh subprocess to avoid state leakage (line 86-87 comment) - Timeout handling: returns exit code 124 on timeout, captures stdout/stderr (line 95-109) --- ### 3. **Plan State & Configuration** **State file location & structure:** - **Path:** `.megaplan/plans/<plan-id>/state.json` - **Type:** `PlanState` TypedDict defined at `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:134-148` - **Key fields:** - `config: PlanConfig` (line 140) contains: - `project_dir: str` (absolute path to workspace) — types.py:37 - `auto_approve: bool` - […]
