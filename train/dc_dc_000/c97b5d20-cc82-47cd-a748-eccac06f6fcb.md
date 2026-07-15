> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only. Review the execution critically against user intent and observable success criteria. Project directory: /Users/user_c042661f/Documents/megaplan Idea: Vendor hermes-agent into the megaplan repo as a subpackage called `agent` using git subtree (preserving history). Job A scope: (1) map reachable-module surface from megaplan's hermes_worker integration; (2) git-subtree vendor /Users/user_c042661f/Documents/hermes-agent/ at megaplan/agent/ preserving history; (3) rewire megaplan/hermes_worker.py to import from in-tree megaplan.agent package; (4) remove check_hermes_available() gating; (5) delete obvious dead weight (evals/, landingpage/, website/, demo/, assets/, node_modules/, package.json, package-lock.json, tinker-atropos/, honcho_integration/, mini-swe-agent/, gateway/, cron/, hermes_cli/, cli.py, auto_improve/, batch_runner.py, rl_cli.py, datagen-config-examples/, root *.json benchmark artifacts, RELEASE_v*.md, setup-hermes.sh, cli-config.yaml.example); (6) verify megaplan still imports and hermes_worker resolves. Out of scope (Job B later): skills/, tools/ filtering, acp_adapter, acp_registry, environments/. Approved plan: # Implementation Plan: Vendor hermes-agent as `megaplan/agent/` subpackage (Job A) ## Overview Vendor `hermes-agent` into `megaplan` at `megaplan/agent/` via `git subtree` (history preserved). Integrate via a `sys.path` prepend shim in `megaplan/agent/__init__.py` so hermes's original top-level imports resolve without rewriting any vendored file. **Iter-6 refinement: DRY the shim+error-conversion via one helper.** Prior iterations tracked execution sites by name and kept missing one (iter-5 said three; the repo has four: `megaplan/hermes_worker.py:290 run_hermes_step`, `megaplan/review/parallel.py:80 _run_check`, `megaplan/review/parallel.py:209 _run_criteria_verdict`, `megaplan/parallel_critique.py:51 _run_check`). Fix: introduce one helper `_import_hermes_runtime()` in `megaplan/hermes_worker.py` that (a) triggers the shim, (b) imports `AIAgent` and `SessionDB`, (c) converts `ImportError` into `CliError("agent_deps_missing", ...)`. All four execution sites call the helper. The AST gate becomes a positive structural check: "zero `from run_agent import` / `from hermes_state import` statements anywhere in `megaplan/**/*.py` outside `megaplan/agent/` AND outside `_import_hermes_runtime` itself." A future 5th site that forgets the helper is caught by the gate; a correct 5th site that uses the helper passes without modification. **Settled decisions (locked; not revisited):** - `vendoring-strategy-shim`: sys.path shim in `megaplan/agent/__init__.py`. - `shim-trigger-placement-rule`: shim activated only through `_import_hermes_runtime()`; availability helpers use filesystem checks. - `availability-helpers-filesystem-check`: `_is_agent_available("hermes")` and `detect_available_agents()` use `(Path(__file__).resolve()... / "agent" / "run_agent.py").is_file()`. - `hermes-cli-retained`: keep vendored in Job A. - `agent-optional-extra`: `[project.optional-dependencies] agent = [...]`. - `key-pool-sibling-fallback-removed`: drop `../hermes-agent/auto_improve/api_keys.json`. - `preserve-sys-modules-test-fakes`: keep `sys.modules["run_agent"]/["hermes_state"]` test fakes unchanged. - `callers-agent-deps-missing-try-except`: every hermes import site routes through a single error-converting helper. […]

> AGENT

I'll review this execution carefully. Let me start by investigating the actual state of the code versus the claims.

> AGENT

Good — the subtree merge IS a real merge (two parents) with hermes-agent history preserved. Now let me verify the critical implementation pieces.

> AGENT

Helper function is correct. Now let me verify all four execution sites use it:

> AGENT

All 4 execution sites correctly route through the helper. Let me verify remaining critical items in parallel.

> AGENT

Source verification is complete. The subtree merge is a real two-parent merge commit with hermes-agent history reachable. All helper/shim/availability code matches the plan exactly. Let me finalize the review.

> AGENT

Confirmed — `236bf4d2` is a real merge commit with two parents (megaplan's `650677b3` + hermes-agent's `980e6b1c`), meaning `git subtree add` was run **without** `--squash` and history is preserved. The executor's T1/T2 happened in a prior commit session; the current session did T4/T5/T6/T8.

> AGENT

Review complete. Verdict: **approved**. Key findings: - **Subtree history IS preserved.** Commit `236bf4d2` is a true merge with two parents (`650677b3` main + `980e6b1c` hermes-agent tip); `git log 980e6b1c` shows hermes history reachable. The executor's T2 "skipped" status was misleading — the subtree add landed in a prior session's commit, not this session's pass. - **All helper/shim/availability code matches the plan exactly.** `_import_hermes_runtime()` at `hermes_worker.py:23-36`, all four execution-site rewires, filesystem-only availability helpers, and `check_hermes_available` deletion all verified via source inspection. - **Dead-weight cleanup complete.** The massive diff (412K lines, 2014 files) reflects the intended T6 deletions of `auto_improve/`, `evals/`, `website/`, etc. — not noise. - **Two MUST criteria deferred to human:** CLI `agent_deps_missing` smoke and fresh-venv hermetic probe. Both were legitimately blocked (user forbade CLI invocation; sandbox lacks `hatchling`) — source-level verification passes for both. - **Full test suite green** under Python 3.11 (790 passed, 2 skipped). All 14 verified flag IDs resolved. No rework items. The accepted-tradeoff about `ast.Import` vs `ast.ImportFrom` AST-gate coverage is documented as a 3-line follow-up and non-blocking since Steps 5.3/5.4 removed the only two bare-import sites that prompted the concern.
