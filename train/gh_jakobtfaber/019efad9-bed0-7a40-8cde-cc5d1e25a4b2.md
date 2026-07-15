> SYSTEM

# AGENTS.md instructions for /private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire

<INSTRUCTIONS>
# Codex Configuration

## Learned User Preferences

- When the user asks about Codex, interpret that as Codex CLI/configuration specifically; do not answer from Cursor MCP or Cursor IDE state unless explicitly asked.
- For cross-agent plan review, use Codex with GPT-5.5 medium effort, Claude Code with Opus 4.8 xhigh effort, and Antigravity through the `agy` CLI when available.
- Be conservative about durable memory: capture recurring corrections and stable workspace facts only, not one-off runtime details or transient command output.
- For chezmoi-managed dotfiles, edit source under `~/Developer/repos/github.com/jakobtfaber/dotfiles/home/`; restore live drift (e.g. tool-injected shell hooks) with `chezmoi apply --force` on the target file, not direct edits to `~/.*`.
- When adding core Homebrew tooling, promote packages into `home/dot_Brewfile.tmpl` (e.g. `dotfiles local promote brew <pkg>`) instead of only running `brew install`.
- Maintain Mac-local agent and observability inventories in `~/Obsidian/LLMs/agents/registry/` (`Agent Registry`, `Agent Observability Registry`, inactive-tools log) alongside chezmoi/dotfiles memory—not only in `AGENTS.md`.
- Keep `wolfbook.mcpEnabled: false` in Cursor and VS Code so the Wolfbook extension does not rewrite Antigravity/Gemini MCP configs on disk.
- Orchestrate Claude Code from Cursor via `claude -p --resume` from the session's project cwd; do not run parallel iTerm sessions on the same Claude session ID.
- Trigger prompt-guided context compaction when the chat context window reaches ~40%.

## Learned Workspace Facts

- Dotfiles are chezmoi-managed from `~/Developer/repos/github.com/jakobtfaber/dotfiles/home/`; `~/.zshrc` maps to `dot_zshrc.tmpl`.
- Interactive agent work runs in Cursor; Claude Code shells use iTerm (`claude -p --resume` from project cwd). cmux was removed Jun 2026 (SwiftUI terminal-panel teardown crashes).
- Devin shell integration injects `MANAGED DEVIN BLOCK` (`devin shell init zsh`) into live `~/.zshrc`, re-wrapping sessions as `devin shell run zsh`; the chezmoi template has no Devin hooks — disable with `chezmoi apply --force ~/.zshrc`, restart terminals, and optionally `devin auth logout`.
- Codex MCP startup paths were migrated away from networked `npx`: Playwright uses `/opt/homebrew/bin/playwright-mcp`, Context7 uses `/opt/homebrew/bin/context7-mcp`, and Sourcegraph uses `SOURCEGRAPH_MCP_REMOTE_BIN=/opt/homebrew/bin/mcp-remote`.
- Maistro MCP is globally registered through `my-skillset` (`meta/mcps.json`) and projected by `mskill install`; Codex/Claude should reach it as `/Users/jakobfaber/.local/bin/mskill mcp maistro`. Do not hand-maintain separate Maistro MCP entries; change `~/Developer/my-skillset/meta/mcps.json`, run `bash meta/install-host.sh`, and verify with `codex mcp get maistro` / `mskill doctor`.
- The cross-agent runtime standard is project opt-in for `mise`; Conda-first repos keep Python owned by Conda, and agent automation should use explicit `mise exec -- ...` or clean `conda run -n ...` runners.
- Antigravity `agy` does not expose stable CLI model/effort flags here; model/effort is verified from Antigravity memory logs as runtime metadata such as `Model Selection ... Gemini 3.5 Flash (Medium)`.
- Runtime-standard validation artifacts live under `~/.codex/automations/runtime-standard/`; local fixtures are `~/Developer/projects/runtime-standard-pilot` and `~/Developer/projects/runtime-standard-conda-pilot`.
- Orphan prior-art-recon `claude -p` workers can persist as PPID 1 after the parent exits; kill manually if they linger.
- Gurobi 13.0.2 on jakob-mbp: native pkgs (`/Library/gurobi1302`, `/Library/gurobi_server1302`, `/usr/local/bin`); WLS license `~/gurobi.lic`; `GUROBI_HOME` in chezmoi `10-env.zsh`; Python via `pip install gurobipy==13.0.2` in `py312` (not conda package `gurobi`). After upgrading the macOS .pkg or pip `gurobipy`, re-verify with fresh `gurobi_cl --license` and a trivial `gurobipy` solve—the two paths update independently.
- HPCC MATLAB: on `hpcc`, MATLAB is module-provided, not on the default PATH. Use `module load matlab/r2026a`; then `matlab` resolves to `/software/Matlab/R2026a/bin/matlab`, `matlabroot` is `/resnick/software/Matlab/R2026a`, and verified version is `26.1.0.3251617 (R2026a) Update 2`. Run non-GUI checks with `matlab -batch "..."`. User MATLAB folder exists at `/home/jfaber/Documents/MATLAB`; `userpath` points there and `prefdir` is `/home/jfaber/.matlab/R2026a`.
- HPCC Mathematica/Wolfram: on `hpcc`, Mathematica is module-provided, not on the default PATH. Available modules verified: `mathematica/11.1`, `12.0`, `12.3`, `13.2`, `14.2`; prefer `module load mathematica/14.2`. Then `wolframscript` resolves to `/resnick/software9/external/Mathematica/14.2/bin/wolframscript`, `math` resolves to `/resnick/software9/external/Mathematica/14.2/bin/math`, `$InstallationDirectory` is `/resnick/software9/external/Mathematica/14.2`, verified `$Version` is `14.2.0 for Linux x86 (64-bit) (December 26, 2024)`, `$UserBaseDirectory` is `/home/jfaber/.Wolfram`, and `$BaseDirectory` is `/usr/share/Wolfram`. Run non-GUI checks with `wolframscript -code '...'` or `math -noprompt -run '...; Exit[]'`.
- HPCC Jupyter/JupyterLab: on `hpcc`, Jupyter is module-provided through Open OnDemand. Use `module load jupyter-ood/7.1.2`; then `jupyter` resolves to `/central/software9/external/jupyter-ood-03262024/bin/jupyter`. Verified stack includes JupyterLab `4.1.5`, Notebook `7.1.2`, IPython `8.22.2`, ipykernel `6.29.3`, jupyter_server `2.13.0`, and jupyter_core `5.7.2`.
- HPCC Julia: on `hpcc`, Julia is module-provided, not on the default PATH. Available modules verified: `julia/1.9.4`, `1.10.2`, `1.10.8`, `1.11.3`, `1.12.2`; prefer `module load julia/1.12.2`. Then `julia` resolves to `/central/software9/external/julia/1.12.2/bin/julia`; verified version is `julia version 1.12.2`.
- HPCC Octave: on `hpcc`, GNU Octave is available on the system PATH without loading a module. `octave` resolves to `/usr/bin/octave`; verified version is `GNU Octave, version 7.3.0`.
- Edison Scientific API: `EDISON_API_KEY` from keychain (`Agents/edison-api-key`); Python client `edison-client` in conda `py312`. PyPI watch: dotfiles workflow `edison-client-pypi-watch` (daily) commits `~/.local/share/edison-client-pypi-watch.json` when a new release ships; `com.jakob.dotfiles-autopull` (30m) runs `chezmoi apply` so onchange upgrades `edison-client` locally. Optional manual/PyPI poll: `edison-client-autoupdate` (24h throttle). Kosmos is web-only (not in API).
- Time Machine destination is external volume `MacBackupDrive` (Samsung T7 Shield); `AutoBackup` runs hourly while attached; redundant Shortcuts mount automation was removed—rely on Time Machine only.
- DSA-110 continuum imaging: active repo is `https://github.com/dsa110/dsa110-continuum`. Legacy `~/Developer/research/archive/dsa110-contimg` is deprecated/archival (read-only); port new work to `dsa110-continuum`, not the archive tree.
- `~/Developer/research/AGENTS.md` defines the two-tree rule: `research/` = owned active work (flat repos + archive); upstream clones → `~/Developer/reference/<domain>/`. `astrophysics/` is the unified radio workspace (merged from `radio-astronomy`); `blimpy`/`FRB` live in `reference/astrophysics/`.
- Orchestrator memory (Maistro) lives at `~/Developer/repos/github.com/jakobtfaber/maistro` (`jakobtfaber/maistro`, SQLite event log, RPC writer on :8787, `https://dashboard.jakobtfaber.com`); bearer token in keychain service `Agents`, account `orch-rpc-token`.
- Pulsar periodicity research: `~/Developer/repos/github.com/jakobtfaber/gridless-pulsar` (`jakobtfaber/gridless-pulsar`); GPU coherent folding is the north star; comb-ANM is a refinement tier only (FRB scope removed).

## Codex from Cursor agent Shell

Full runbook: **`~/Developer/reference/cursor-agent-shell-cli-insights.md`**.

When Cursor (or another IDE) runs **`codex exec`** via agent **Shell**, use **subscription auth only** (`codex login` / ChatGPT tokens). Do **not** set **`OPENAI_API_KEY`** for automation unless the workflow explicitly needs API billing.

Prefer **Cursor `Task`** for small in-IDE delegation. Use **`codex exec`** when you need the full CLI tool surface; diagnose the **child Shell process**, not the chat UI alone.

### Argv-vs-stdin rule

- **Prompt as argv ⇒ close stdin:** `codex exec "…" < /dev/null`.
- If **`codex doctor`** shows ChatGPT auth and the process prints **`Reading additional input from stdin...`**, debug **stdin** before auth, `--full-auto`, or API-key settings.

### Root cause (observed in Cursor agent Shell)

Cursor agent Shell **can** leave stdin open. When **`codex exec`** receives the prompt as an **argument**, it may wait indefinitely for additional stdin.

### Required

```bash
codex exec "Your task here" < /dev/null

codex exec -C /path/to/repo "Your task" < /dev/null

# Unattended — restricted actions may fail instead of prompting
codex exec -c 'approval_policy="never"' "Your task" < /dev/null
```

Smoke tests: **`gtimeout`** from **`brew install coreutils`**, or Homebrew **`timeout`** (`which timeout gtimeout`) — avoid multi-hour zombies.

### Sanity check

```bash
codex doctor   # expect stored auth mode chatgpt, stored API key false
```

### Do not

- Run **`codex exec "…"`** without **`< /dev/null`** from Cursor agent Shell when the prompt is argv.
- Background **`codex exec`** without a watchdog unless stdin is explicitly closed.
- Assume hangs mean broken login when the stdin message appears.

### Expectations

- **~60–90s** for trivial invokes on this machine (hooks/config) is a local baseline; runs should **complete**, not hang, when stdin is closed.

### Output channels

Treat `codex exec` stdout as an execution transcript, not as a reliable machine-readable final answer. Normal stdout may include banners, prompts, hook lifecycle messages, the final assistant message, and token usage.

Use the output channel that matches the task:

- **Human-readable delegation:** let stdout print normally when a person will read the transcript.
- **Machine-readable artifact:** use `-o FILE` / `--output-last-message FILE` for the final model message, and redirect stdout/stderr to logs.
- **Event/debug stream:** use `--json` only when you want JSONL execution events; do not treat it as a single final-answer JSON document.

Canonical structured-output pattern:

```bash
mkdir -p logs

codex exec \
  -m gpt-5.5 \
  --skip-git-repo-check \
  -o result.json \
  "$PROMPT" \
  > logs/codex.stdout.log \
  2> logs/codex.stderr.log \
  < /dev/null

python3 -m json.tool result.json >/dev/null
```

Do not parse normal `codex exec` stdout as JSON unless using `--json` and expecting JSONL events. Do not use `--ignore-user-config` for normal delegation; reserve it for debugging Codex itself because it changes the execution environment.

## Runtime Management

- Repositories are opt-in for `mise` through repo-local `mise.toml`; do not set global `mise` Python.
- Conda-first repositories own Python through Conda; do not add `python` to `mise.toml` there unless explicitly migrating away from Conda.
- Agent automation must use explicit runners: `mise exec -- ...` for mise-first repos, or a clean `conda run -n ...` wrapper for Conda-first repos.
- `direnv` is for interactive shell convenience only. Hooks, agents, and non-interactive scripts must not depend on `.envrc` being loaded.
- MCP binaries used at agent startup are Homebrew-managed system tools, not project runtimes. Do not reintroduce `npx` on Codex MCP startup paths.
- On this machine, inherited interactive PATH state can make bare `conda run -n py312 python` resolve base Anaconda Python. For agent-safe Conda checks, prefer:
  `env -i HOME="$HOME" PATH="/opt/anaconda3/bin:/opt/homebrew/bin:/usr/bin:/bin" /opt/anaconda3/bin/conda run -n py312 ...`

## Skills — GitHub Sync

Custom skills are version-controlled in the private `my-skillset` repository.

- **Canonical local clone:** `~/Developer/repos/github.com/jakobtfaber/my-skillset/`
- **Compatibility symlink:** `~/Developer/projects/my-skillset` → `~/Developer/repos/github.com/jakobtfaber/my-skillset`
- **Compatibility symlink:** `~/Developer/my-skillset` → `~/Developer/repos/github.com/jakobtfaber/my-skillset`
- **Claude symlink:** `~/.claude/my-skillset` → `~/Developer/repos/github.com/jakobtfaber/my-skillset`
- **Codex symlink:** `~/.codex/my-skillset` → `~/Developer/repos/github.com/jakobtfaber/my-skillset`
- **Codex active skills symlink:** `~/.codex/skills` → `~/.codex/skills-minimal`
- **Codex minimal skill set:** `~/.codex/skills-minimal` contains a curated mix of local skill folders and symlinks into `my-skillset`; do not repoint it to the full skill tree unless intentionally reversing prompt-bloat pruning.
- **Auto-pull agent:** `com.jakob.skills-autopull`

Do not use the retired `~/Developer/misc/claude-config` path for current skill sync.

## Persistent Agent Memory

Use `~/Developer/repos/github.com/jakobtfaber/dotfiles/memory/` as the manual intent/context memory layer. This is the canonical memory store and the only persistent agent-memory store managed by dotfiles.

- Manual memory notes: `~/Developer/repos/github.com/jakobtfaber/dotfiles/memory/`
- Memory index: `~/Developer/repos/github.com/jakobtfaber/dotfiles/memory/MEMORY.md`
- Runtime memory path: `~/.claude/projects/-Users-jakobfaber/memory/` symlinks to `~/Developer/repos/github.com/jakobtfaber/dotfiles/memory/`
- Daily auto-commit of the memory subtree: launchd job `com.jakobfaber.dotfiles-memory-snapshot` (S-009)

Codex may update its own managed store under `~/.codex/memories/`, but any durable memory-worthy fact, correction, preference, or workspace state written there must also be captured in `~/Developer/repos/github.com/jakobtfaber/dotfiles/memory/` by default. Treat Codex memory as a Codex-local copy/cache, not the only durable record.

Do not create ad-hoc memory directories under `~/.codex/` for persistent memory.
Do not inspect `~/.claude-mem/` for current memory health; that retired directory no longer exists.

## Task Status Semantics

Use strict closure semantics when tracking tasks, updating a temporary to-do list, or summarizing whether work is done.

- `completed`: no further action remains for that item.
- `blocked`: cannot proceed without user input or an external state change.
- `diagnosed`: root cause or next step is known, but the fix/work is not complete.
- `validated`: behavior was checked, but there may still be follow-up.
- `decision pending`: implementation or investigation is sufficient, but a product/UX/cleanup choice remains.

If the available task-tracking tool only supports `pending`, `in_progress`, and `completed`, do not mark blocked/diagnosed/decision-pending work as `completed`. Keep the item `pending`, or split it into a completed investigation item plus a separate pending follow-up with the explicit status in the task text.

## Proactive Stopping Points

When work changes runtime behavior, tool availability, config, MCP servers, daemons, launch agents, browser/app state, shell startup, or any long-lived process, do not stop at a generic note such as "restart required" or "you may need to restart." Before final response, proactively identify the concrete affected process, service, app, server, port, or session that needs reload/restart, inspect what is currently running when practical, and stop at the actionable question with named targets, for example: "Shall I restart `X` and `Y`?" If the restart/reload is reversible and already authorized by the user, perform it and verify the new behavior instead of asking. If it is disruptive, kills user state, or crosses a one-way/outward boundary, ask with the explicit target list and blast radius.

Before claiming completion after file edits, run `agent-closeout-check` or `mskill tool agent-closeout-check` for every repo touched when either condition applies: the repo is dirty, or touched paths could affect runtime behavior. Pass each repo with `--repo`; pass known changed runtime/config paths with `--touched`; pass `--packet <closeout.json>` once you have a dirty-state handoff and/or restart inventory. If the checker fails, do not replace it with a vague caveat. Either produce the required dirty-state handoff packet, perform and verify the required restart, or stop at the concrete next question emitted by the check.

## Dirty Git State

<important if="you see dirty files in a git repo, or a command reports modified, staged, untracked, deleted, renamed, or conflicted files">
Use the `dirty-git-state` skill from `my-skillset` before deciding whether to inspect, edit, clean, stage, commit, or ask the user.

When committing, commit validated, task-scoped changes once the work is complete.
For pre-existing changes, review all of them before committing. Only include them
once they are fully understood, are not transient real-time development state,
and are deemed worthy of commit. If ownership, intent, or readiness is ambiguous
after review, leave the ambiguous changes uncommitted and report the ambiguity.
</important>

<important if="you are asked to run a code review or delegate a task using Codex or Claude">
- For Codex reviews, run Codex non-interactively using:
  `codex exec -m gpt-5.5 -c model_reasoning_effort="medium" "..." < /dev/null`
  This uses gpt-5.5 with medium effort by default.
- For Claude reviews, run Claude non-interactively using:
  `claude --model claude-opus-4-8 --effort xhigh -p "..." < /dev/null`
  This uses Opus 4.8 with xhigh effort by default.
</important>

## Authentication & Verification Protocols

When verifying, investigating, or inspecting the health, connectivity, or authentication state of any service, tool, or API (e.g., Grov, Firecrawl, MCP, ACP, or coding harnesses):

1. **Do Not Blindly Trust CLI Self-Checkers (`doctor` / `status` outputs)**:
   Never take a diagnostic command (e.g., `doctor`, `status`, `healthcheck`) showing green checkmarks as absolute proof of live runtime operational health. These commands often only check if your local configuration files are structured correctly without testing active connection channels.
2. **Test Live Operational Handshakes**:
   Always execute a minor, non-destructive live operational command (e.g., running a Dry-Run, pulling a mock schema, or making a safe query) to force a true cryptographic handshake with the API endpoint.
3. **Inspect Backing Configs Directly**:
   Always locate and inspect the underlying configuration and credentials storage files (JSON, TOML, SQLite databases, or environment variables) directly. Check active token lifetimes, `expires_at` timestamps, scopes, and encryption validity against the current local system time (e.g., `credentials.json` expiration dates) to verify active session state.

<!-- opensrc:start -->
## opensrc — dependency source for deeper context

`opensrc` (CLI, installed globally) caches dependency **source code** at `~/.opensrc/` so agents can read a package's internal implementation, not just its public types/interface. Cached inventory: `~/.opensrc/sources.json`.

- **Fetch (cache only):** `opensrc fetch <pkg>` — cross-registry: `opensrc fetch pypi:<pkg> crates:<pkg> <owner>/<repo>`
- **Read (fetches on cache miss):** `rg "pattern" $(opensrc path <pkg>)` · `cat $(opensrc path <pkg>)/path/to/file` · `find $(opensrc path <pkg>) -name "*.ts"`

Use it when you need to understand *how* a dependency works internally (npm, PyPI, crates.io, or a GitHub repo), not just its surface API.
<!-- opensrc:end -->

@/Users/jakobfaber/.codex/RTK.md

--- project-doc ---

# AGENTS.md

Repo-level agent guidance for FLITS. Full project guide: `CLAUDE.md`.
Binding fit-validation contract: `.cursor/rules/AGENT_CONFIGURATION_FLITS.md`.

## Long-View Science Goals

The primary objective of the CHIME–DSA co-detection analysis and the FLITS pipeline is to reconstruct the complete line-of-sight dispersion measure (DM) and scattering budgets for the 12 co-detected bursts.

1. **Accurate Scattering Index (\(\alpha\)) Measurement:** Break the degeneracy between scattering time \(\tau\) and index \(\alpha\) by fitting CHIME (400–800 MHz) and DSA-110 (1.2–1.5 GHz) data simultaneously with a shared model, leveraging the \(\sim 1\) GHz frequency lever arm.
2. **Mitigating Profile Bias:** Detect hidden temporal sub-components (multi-pulse structures). Left unmodeled, secondary pulses bias \(\alpha\) high (e.g. \(\alpha \approx 3.3 \to 2.7\)). Fits must model sub-components to ensure physical honesty.
3. **Sightline Attribution:** Partition observed \(DM_{\text{obs}}\) and scattering \(\tau_{\text{obs}}\) to constrain host-galaxy, Milky Way, and intervening foreground contributions (probing the CGM/groups/clusters of 49 candidate intervening systems).


## Review guidelines

Used by Codex automatic code review (and any agent reviewing a PR). Flag only
real P0/P1 issues; skip style that ruff already enforces. Ignore base64 image
payloads embedded in `docs/*.html`.

- **Physics kernel ownership.** `scattering/scat_analysis/burstfit.py` is the
  canonical kernel; `flits/` wraps it. Model-physics changes belong in
  `burstfit.py` — flag edits that fork physics into the wrapper.
- **Fit validation is mandatory.** Flag any change that could rationalize a
  failing/marginal fit into a pass, drop a validation level (Level-1 gates,
  chi2_red / R2, physics `tau*dnu` in [0.1, 2.0], alpha bounds), or bypass the
  diagnostic-figure review gate. A numeric PASS without figure review is not a pass.
- **Physics sanity.** Enforce bounds `0.0001 < tau < 100 ms` and
  `1.5 < alpha < 6.0`; check units and the frequency-ascending load assumption.
- **Lazy-minimalist (ponytail).** Flag unnecessary abstractions, dead code,
  speculative config, and parallel near-duplicate modules. Prefer the shortest
  correct diff — but never trade scientific rigor or a validation level for brevity.

</INSTRUCTIONS>
<environment_context>
  <cwd>/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire</cwd>
  <shell>zsh</shell>
  <current_date>2026-06-24</current_date>
  <timezone>America/Los_Angeles</timezone>
  <filesystem><workspace_roots><root>/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire</root></workspace_roots><permission_profile type="managed"><file_system type="restricted"><entry access="read"><special>:root</special></entry></file_system></permission_profile></filesystem>
</environment_context>

> DEVELOPER

You are reviewing a single-commit feature branch in a FLITS (FRB scattering/scintillation) repo.

CONTEXT: PRs #54 (pipeline wiring) and #55 (ACF revalidation: compare_lorentzian_components) are now MERGED to origin/main. This branch feat/scint-multicomponent-select is rebased to a CLEAN single commit on top of current origin/main. Its full diff is below.

The change wires revalidation.compare_lorentzian_components (BIC ΔBIC>6 AND nested F-test, p<0.05) into scintillation/scint_analysis/analysis.py::analyze_scintillation_from_acfs so the pipeline auto-selects the statistically-justified Lorentzian component count per sub-band, aggregates by plurality, and when >1 extracts each component (ordered by ascending Δν) into the existing per-component power-law path. Replaces a dead 2c/3c-in-name heuristic. Gated on a Lorentzian-family best model; gauss/power/lor_gen stay single-component.

The full committed diff:
---8<---
commit 662ba4cb6a884c0a426602b5404100a6044aecee
Author: Jakob Faber <jfaber@caltech.edu>
Date:   Wed Jun 24 11:10:27 2026 -0700

    feat(scint): pipeline auto-selects Lorentzian component count (BIC+F-test)
    
    Wires compare_lorentzian_components into analyze_scintillation_from_acfs: for a
    Lorentzian-family best model, determine the statistically-justified component
    count per sub-band (BIC ΔBIC>6 AND nested F-test) and aggregate by plurality;
    when >1, extract each component (ordered by ascending Δν = same screen across
    sub-bands) into the existing per-component power-law path. Replaces the dead
    2c/3c-in-name heuristic. Reports n_components + per-sub-band counts in
    final_results. Gauss/power/lor_gen stay single-component.
    
    Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_01Nkd8kUhDoc6ZZnviUsvVon

diff --git a/scintillation/scint_analysis/analysis.py b/scintillation/scint_analysis/analysis.py
index 00e969ab..31434156 100644
--- a/scintillation/scint_analysis/analysis.py
+++ b/scintillation/scint_analysis/analysis.py
@@ -1298,6 +1298,77 @@ def _select_overall_best_model(all_subband_fits):
     return best_model
 
 
+def _determine_n_components(acf_results, max_components=3):
+    """Burst-level Lorentzian component count from the BIC + nested-F-test selector
+    (``revalidation.compare_lorentzian_components``) run on each sub-band ACF and
+    aggregated by plurality (ties → fewer components, the conservative default).
+
+    The pipeline feeds its OWN ACFs (``calculate_acf``) to the selector, so this does
+    not compromise the cross-check independence of the revalidation ACF estimator —
+    only the model-selection statistic is shared. Returns ``(n_components, per_subband)``.
+    """
+    from .revalidation import compare_lorentzian_components
+
+    per = []
+    for i in range(len(acf_results["subband_acfs"])):
+        lags = np.asarray(acf_results["subband_lags_mhz"][i], dtype=float)
+        acf = np.asarray(acf_results["subband_acfs"][i], dtype=float)
+        try:
+            per.append(compare_lorentzian_components(lags, acf, max_components=max_components))
+        except Exception as e:  # a single bad sub-band must not sink the burst
+            log.debug(f"component-count selector failed on sub-band {i}: {e}")
+            per.append({"n_preferred": 1})
+    if not per:
+        return 1, per
+    votes = {}
+    for v in per:
+        k = int(v.get("n_preferred", 1))
+        votes[k] = votes.get(k, 0) + 1
+    top = max(votes.values())
+    return min(k for k, c in votes.items() if c == top), per  # plurality, ties → fewer
+
+
+def _extract_multi_component(per_subband, num_comps, n_subbands):
+    """params_per_comp from each sub-band's N-Lorentzian fit (the selector's ``fits``
+    entry for n=num_comps). Components are ordered by ascending Δν so component k is
+    the same screen across sub-bands (the per-component power-law then tracks one
+    screen). Sub-bands whose N-fit failed or whose k-th component is non-physical get
+    a ``{}`` placeholder, which the downstream consumer skips."""
+    params_per_comp = [[] for _ in range(num_comps)]
+    for i in range(n_subbands):
+        verdict = per_subband[i] if per_subband and i < len(per_subband) else None
+        fit_n = (
+            next(
+                (
+                    f
+                    for f in verdict.get("fits", [])
+                    if f.get("n") == num_comps and f.get("success")
+                ),
+                None,
+            )
+            if verdict
+            else None
+        )
+        comps = sorted(fit_n["components"], key=lambda c: c["dnu_mhz"]) if fit_n else []
+        gof = {"bic": fit_n["bic"], "redchi": fit_n["redchi"]} if fit_n else {}
+        for c in range(num_comps):
+            cc = comps[c] if c < len(comps) else None
+            if cc and np.isfinite(cc["dnu_mhz"]) and cc["dnu_mhz"] > 0:
+                params_per_comp[c].append(
+                    {
+                        "bw": cc["dnu_mhz"],
+                        "mod": cc["m"],
+                        "bw_err": cc.get("dnu_err", np.nan),
+                        "mod_err": cc.get("m_err", np.nan),
+                        "finite_err": np.nan,
+                        "gof": gof,
+                    }
+                )
+            else:
+                params_per_comp[c].append({})
+    return params_per_comp
+
+
 def analyze_scintillation_from_acfs(acf_results, config):
     """
     Main analysis orchestrator. Fits multiple ACF models, selects the best one,
@@ -1354,11 +1425,13 @@ def analyze_scintillation_from_acfs(acf_results, config):
         # If no model is forced, use the automatic selection.
         best_model_name = auto_best_model
 
-    # Logic for determining the number of components was not robust.
-    if "3c" in best_model_name:
-        num_comps = 3
-    elif "2c" in best_model_name or "unresolved" in best_model_name:
-        num_comps = 2
+    # Determine the statistically-justified number of Lorentzian components via the
+    # BIC + nested-F-test selector (aggregated across sub-bands). Only Lorentzian-
+    # family bursts are eligible; gauss/power/lor_gen stay single-component. This
+    # replaces a dead "2c"/"3c"-in-name heuristic that no model ever emitted.
+    n_comp_detail = None
+    if best_model_name.endswith("lor"):
+        num_comps, n_comp_detail = _determine_n_components(acf_results, max_components=3)
     else:
         num_comps = 1
 
@@ -1441,7 +1514,19 @@ def analyze_scintillation_from_acfs(acf_results, config):
         for comp_list in params_per_comp[1:]:
             comp_list.append({})
 
+    # When the selector found >1 Lorentzian component, replace the single-component
+    # extraction above with per-component measurements from each sub-band's
+    # N-Lorentzian fit (component identity fixed by ascending Δν).
+    if num_comps > 1:
+        params_per_comp = _extract_multi_component(n_comp_detail, num_comps, len(all_fits))
+
     final_results = {"best_model": best_model_name, "components": {}}
+    final_results["n_components"] = num_comps
+    if n_comp_detail is not None:
+        final_results["component_selection"] = {
+            "n_per_subband": [int(v.get("n_preferred", 1)) for v in n_comp_detail],
+            "criterion": n_comp_detail[0].get("criterion") if n_comp_detail else None,
+        }
     all_powerlaw_fits = {}
 
     for i, params_list in enumerate(params_per_comp):
diff --git a/scintillation/scint_analysis/revalidation.py b/scintillation/scint_analysis/revalidation.py
index 9d245518..8be5d92e 100644
--- a/scintillation/scint_analysis/revalidation.py
+++ b/scintillation/scint_analysis/revalidation.py
@@ -268,6 +268,12 @@ def _n_lorentzian_model(n):
     return model
 
 
+def _param_stderr(param):
+    """lmfit parameter 1σ stderr as a float, or nan when unavailable."""
+    e = param.stderr
+    return float(e) if e is not None else float("nan")
+
+
 def compare_lorentzian_components(
     lags, acf, max_components=3, acf_err=None, delta_bic_strong=6.0, p_thresh=0.05
 ):
@@ -354,11 +360,18 @@ def compare_lorentzian_components(
         except Exception:
             fits.append({"n": n, "success": False, "bic": np.inf, "chi2": np.inf})
             continue
+
         comps = sorted(
             (
-                (abs(res_n.params[f"l{i}_gamma"].value), abs(res_n.params[f"l{i}_m"].value))
+                {
+                    "dnu_mhz": abs(res_n.params[f"l{i}_gamma"].value),
+                    "m": abs(res_n.params[f"l{i}_m"].value),
+                    "dnu_err": _param_stderr(res_n.params[f"l{i}_gamma"]),
+                    "m_err": _param_stderr(res_n.params[f"l{i}_m"]),
+                }
                 for i in range(n)
             ),
+            key=lambda c: c["dnu_mhz"],
             reverse=True,
         )
         fits.append(
@@ -371,7 +384,7 @@ def compare_lorentzian_components(
                 "redchi": float(res_n.redchi),
                 "n_params": int(res_n.nvarys),
                 "ndata": int(res_n.ndata),
-                "components": [{"dnu_mhz": g, "m": m} for g, m in comps],
+                "components": comps,
             }
         )
 
diff --git a/scintillation/scint_analysis/tests/test_multicomponent_select.py b/scintillation/scint_analysis/tests/test_multicomponent_select.py
new file mode 100644
index 00000000..12065a99
--- /dev/null
+++ b/scintillation/scint_analysis/tests/test_multicomponent_select.py
@@ -0,0 +1,118 @@
+"""Pipeline wiring: analyze_scintillation_from_acfs determines and uses the
+statistically-justified number of Lorentzian components (BIC + nested F-test, via
+revalidation.compare_lorentzian_components), instead of the dead "2c"/"3c"-in-name
+heuristic that no model ever emitted.
+
+Driven on synthetic acf_results (raw burst spectra are gitignored, DATA_SOURCES.md):
+a known one- vs two-component ACF in every sub-band must come back as
+n_components 1 vs 2, with the two screens recovered as component_1 (narrow) and
+component_2 (wide).
+"""
+
+from __future__ import annotations
+
+import sys
+from pathlib import Path
+
+_test_dir = Path(__file__).parent
+sys.path.insert(0, str(_test_dir.parent.parent.parent))  # FLITS root
+sys.path.insert(0, str(_test_dir.parent.parent))  # scintillation dir
+
+import numpy as np
+
+from scint_analysis.analysis import (
+    _determine_n_components,
+    analyze_scintillation_from_acfs,
+    lorentzian_component,
+)
+
+_CFG = {
+    "analysis": {
+        "fitting": {
+            "fit_lagrange_mhz": 2.0,
+            "reference_frequency_mhz": 600.0,
+            "force_model": "fit_lor",  # deterministic Lorentzian gate
+        }
+    }
+}
+
+
+def _acf_results(component_sets, dch=0.01, nch=256, noise=2e-3, seed=0):
+    """acf_results dict (no noise template/self-noise -> single-prefix model labels)
+    whose every sub-band ACF is the sum of the given (gamma, m) Lorentzians."""
+    rng = np.random.default_rng(seed)
+    pos = np.arange(1, nch + 1) * dch
+    lags = np.concatenate((-pos[::-1], [0.0], pos))
+    out = {
+        "subband_acfs": [],
+        "subband_lags_mhz": [],
+        "subband_center_freqs_mhz": [],
+        "subband_channel_widths_mhz": [],
+        "subband_num_channels": [],
+        "noise_template": None,
+        "sigma_self_mhz": None,
+    }
+    freqs = np.linspace(450.0, 750.0, len(component_sets))
+    for f, comps in zip(freqs, component_sets, strict=True):
+        acf = np.zeros(lags.size)
+        for g, m in comps:
+            acf = acf + lorentzian_component(lags, g, m)
+        acf = acf + rng.normal(0, noise, lags.size)
+        out["subband_acfs"].append(acf)
+        out["subband_lags_mhz"].append(lags)
+        out["subband_center_freqs_mhz"].append(float(f))
+        out["subband_channel_widths_mhz"].append(dch)
+        out["subband_num_channels"].append(nch)
+    return out
+
+
+def test_determine_n_components_counts():
+    assert _determine_n_components(_acf_results([[(0.1, 0.8)]] * 4))[0] == 1
+    assert _determine_n_components(_acf_results([[(0.04, 0.6), (0.6, 0.6)]] * 4))[0] == 2
+
+
+def test_two_components_wired_into_output():
+    fr, _fits, _pl = analyze_scintillation_from_acfs(
+        _acf_results([[(0.04, 0.6), (0.6, 0.6)]] * 4), _CFG
+    )
+    assert fr["n_components"] == 2
+    assert set(fr["components"]) == {"component_1", "component_2"}
+    assert fr["component_selection"]["n_per_subband"] == [2, 2, 2, 2]
+    # component_1 = narrow (≈0.04), component_2 = wide (≈0.6), recovered at ref freq.
+    assert abs(fr["components"]["component_1"]["bw_at_ref_mhz"] - 0.04) < 0.02
+    assert abs(fr["components"]["component_2"]["bw_at_ref_mhz"] - 0.6) < 0.15
+    for name in ("component_1", "component_2"):
+        assert len(fr["components"][name]["subband_measurements"]) == 4
+
+
+def test_single_component_unchanged():
+    fr, _fits, _pl = analyze_scintillation_from_acfs(_acf_results([[(0.1, 0.8)]] * 4), _CFG)
+    assert fr["n_components"] == 1
+    assert list(fr["components"]) == ["scint_scale"]
+
+
+def test_non_lorentzian_best_model_stays_single():
+    """The component-count search is gated on a Lorentzian best model; force a
+    power-law and the burst must stay single-component (no spurious multi-fit)."""
+    cfg = {
+        "analysis": {
+            "fitting": {
+                "fit_lagrange_mhz": 2.0,
+                "reference_frequency_mhz": 600.0,
+                "force_model": "fit_power",
+            }
+        }
+    }
+    fr, _fits, _pl = analyze_scintillation_from_acfs(
+        _acf_results([[(0.04, 0.6), (0.6, 0.6)]] * 4), cfg
+    )
+    assert fr["n_components"] == 1
+    assert "component_selection" not in fr  # determination not run for non-Lorentzian
+
+
+if __name__ == "__main__":
+    test_determine_n_components_counts()
+    test_two_components_wired_into_output()
+    test_single_component_unchanged()
+    test_non_lorentzian_best_model_stays_single()
+    print("ok")
---8<---

Tests: 4 new + 94 scint suite pass; mutation-checked (forcing wrong count makes the new tests fail, confirming teeth). ruff: zero NEW errors from this diff (pre-existing scintillation noise only). revalidation.py ruff-clean.

Give me TWO things, concisely:
1. CORRECTNESS REVIEW of this wiring. Focus on: (a) does plurality-vote aggregation across sub-bands make physical sense, or should it be stricter/looser? (b) is ordering components by ascending Δν a sound "same screen across sub-bands" assumption? (c) any bug, edge case (empty sub-bands, all-fail, single sub-band), or silent-wrong risk in _determine_n_components / _extract_multi_component? (d) is gating on best_model_name.endswith("lor") correct given the model registry? Rate P1 (must-fix) / P2 (should-fix) / P3 (nit). If none, say "no P1/P2".
2. LANDING VERDICT: given #54/#55 are merged and this is a clean single commit on origin/main, is opening a PR for this branch the right move? Any reason to hold, restructure, or squash differently? One line.

> AGENT

I’m using the `review` skill because this is explicitly a branch/diff review. I’ll keep this to the two requested outputs and avoid widening beyond the provided commit.

> TOOL

tool_use shell_command
id: call_tPEj5wlSY1CWX2DF5dQDHKfM
```json
{
  "command": "sed -n '1,220p' /Users/jakobfaber/.agents/skills/review/SKILL.md",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_tPEj5wlSY1CWX2DF5dQDHKfM
```
Exit code: 0
Wall time: 3.9 seconds
Output:
---
name: review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent for both.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3.
- The brief: "Report — per file/hunk where relevant — every place the diff violates a documented standard. Cite the standard (file + the rule). Distinguish hard violations from judgement calls. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

```

> AGENT

I’m checking only the parts that can affect the verdict: the model-name registry, the preexisting component-output path, and the selector return shape. That’s enough to avoid reviewing from commit text alone.

> TOOL

tool_use shell_command
id: call_qRhYR7NVWted8KkA2Urgo7Vw
```json
{
  "command": "rg -n \"fit_lor|lor_gen|fit_power|fit_gauss|all_subband_fits|best_model_name|def fit_|model\" scintillation/scint_analysis/analysis.py | head -n 160",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_MAV7qGDAsFgAGqUlq9KdmvXf
```json
{
  "command": "sed -n '1240,1585p' scintillation/scint_analysis/analysis.py",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_V0A4egxiZpFJLzNDnzSDblaD
```json
{
  "command": "sed -n '250,430p' scintillation/scint_analysis/revalidation.py",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_fTIHcPLkwUq3wcFOGEAvcEHT
```json
{
  "command": "rg -n \"component|scint_scale|params_per_comp|subband_measurements|bw_at_ref\" scintillation/scint_analysis/analysis.py | tail -n 120",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_EB2U1oADJoaxqr9pz17XwBTm
```json
{
  "command": "rg -n \"FLITS|scint|revalidation|component|Lorentzian|fit validation\" /Users/jakobfaber/.codex/memories/MEMORY.md | head -n 80",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_qRhYR7NVWted8KkA2Urgo7Vw
```
Command blocked by PreToolUse hook: rtk-codex-guard: shell command should use RTK compact output.

Suggested command:
rtk grep -n "fit_lor|lor_gen|fit_power|fit_gauss|all_subband_fits|best_model_name|def fit_|model" scintillation/scint_analysis/analysis.py | head -n 160

To bypass for this command, prefix it with: RTK_DISABLED=1. Command: rg -n "fit_lor|lor_gen|fit_power|fit_gauss|all_subband_fits|best_model_name|def fit_|model" scintillation/scint_analysis/analysis.py | head -n 160
```

> TOOL

tool_result
id: call_MAV7qGDAsFgAGqUlq9KdmvXf
```
Exit code: 0
Wall time: 3.2 seconds
Output:
            "or one measurement may be affected by systematics."
        )
    else:  # C_implied >= C_hi
        result["consistent"] = False
        result["interpretation"] = (
            f"Inconsistent: C = {C_implied:.2f} > {C_hi:.2f} (τ·Δν > 2.0). "
            "May indicate multiple scattering screens, anisotropic scattering, "
            "or measurement systematics."
        )

    return result


def _select_overall_best_model(all_subband_fits):
    """
    Determines the best overall model by summing the BIC across all sub-bands
    for each model type and selecting the one with the lowest total BIC.

    Keep the pretty log ordering (optional):
    ----------------------------------------

    for model_name in sorted(model_bics):
    bic_entry = model_bics[model_name]
    if bic_entry['count'] > 0:
        avg_bic = bic_entry['total_bic'] / bic_entry['count']
        log.info(f"{model_name:>20s}:  Total BIC = {avg_bic:7.1f}  "
                 f"(from {bic_entry['count']:2d} fits)")
    """
    # Use a dictionary to store total BICs and fit counts for each model
    model_bics = defaultdict(lambda: {"total_bic": 0.0, "count": 0})

    for fits in all_subband_fits:
        for model_name, fit_result in fits.items():
            if fit_result and fit_result.success:
                model_bics[model_name]["total_bic"] += fit_result.bic
                model_bics[model_name]["count"] += 1

    log.info("--- Model Comparison (Lowest Total BIC is Best) ---")

    best_model = None
    min_bic = float("inf")

    for model_name, results in model_bics.items():
        if results["count"] > 0:
            log.info(
                f"Model '{model_name}': Total BIC = {results['total_bic']:.2f} (from {results['count']} fits)"
            )
            if results["total_bic"] < min_bic:
                min_bic = results["total_bic"]
                best_model = model_name
        else:
            log.info(f"Model '{model_name}': No successful fits.")

    if best_model is None:
        log.warning("No successful fits for any model. Defaulting to 'lorentzian_component'.")
        return "lorentzian_component"

    log.info(f"==> Best overall model selected: {best_model}")
    return best_model


def _determine_n_components(acf_results, max_components=3):
    """Burst-level Lorentzian component count from the BIC + nested-F-test selector
    (``revalidation.compare_lorentzian_components``) run on each sub-band ACF and
    aggregated by plurality (ties → fewer components, the conservative default).

    The pipeline feeds its OWN ACFs (``calculate_acf``) to the selector, so this does
    not compromise the cross-check independence of the revalidation ACF estimator —
    only the model-selection statistic is shared. Returns ``(n_components, per_subband)``.
    """
    from .revalidation import compare_lorentzian_components

    per = []
    for i in range(len(acf_results["subband_acfs"])):
        lags = np.asarray(acf_results["subband_lags_mhz"][i], dtype=float)
        acf = np.asarray(acf_results["subband_acfs"][i], dtype=float)
        try:
            per.append(compare_lorentzian_components(lags, acf, max_components=max_components))
        except Exception as e:  # a single bad sub-band must not sink the burst
            log.debug(f"component-count selector failed on sub-band {i}: {e}")
            per.append({"n_preferred": 1})
    if not per:
        return 1, per
    votes = {}
    for v in per:
        k = int(v.get("n_preferred", 1))
        votes[k] = votes.get(k, 0) + 1
    top = max(votes.values())
    return min(k for k, c in votes.items() if c == top), per  # plurality, ties → fewer


def _extract_multi_component(per_subband, num_comps, n_subbands):
    """params_per_comp from each sub-band's N-Lorentzian fit (the selector's ``fits``
    entry for n=num_comps). Components are ordered by ascending Δν so component k is
    the same screen across sub-bands (the per-component power-law then tracks one
    screen). Sub-bands whose N-fit failed or whose k-th component is non-physical get
    a ``{}`` placeholder, which the downstream consumer skips."""
    params_per_comp = [[] for _ in range(num_comps)]
    for i in range(n_subbands):
        verdict = per_subband[i] if per_subband and i < len(per_subband) else None
        fit_n = (
            next(
                (
                    f
                    for f in verdict.get("fits", [])
                    if f.get("n") == num_comps and f.get("success")
                ),
                None,
            )
            if verdict
            else None
        )
        comps = sorted(fit_n["components"], key=lambda c: c["dnu_mhz"]) if fit_n else []
        gof = {"bic": fit_n["bic"], "redchi": fit_n["redchi"]} if fit_n else {}
        for c in range(num_comps):
            cc = comps[c] if c < len(comps) else None
            if cc and np.isfinite(cc["dnu_mhz"]) and cc["dnu_mhz"] > 0:
                params_per_comp[c].append(
                    {
                        "bw": cc["dnu_mhz"],
                        "mod": cc["m"],
                        "bw_err": cc.get("dnu_err", np.nan),
                        "mod_err": cc.get("m_err", np.nan),
                        "finite_err": np.nan,
                        "gof": gof,
                    }
                )
            else:
                params_per_comp[c].append({})
    return params_per_comp


def analyze_scintillation_from_acfs(acf_results, config):
    """
    Main analysis orchestrator. Fits multiple ACF models, selects the best one,
    and derives scintillation parameters, including goodness-of-fit checks.
    """
    fit_config = config.get("analysis", {}).get("fitting", {})
    fit_lagrange_mhz = fit_config.get("fit_lagrange_mhz", 45.0)
    ref_freq = fit_config.get("reference_frequency_mhz", 600.0)

    log.info("Fitting all ACF models to all sub-band ACFs...")
    all_fits = []
    noise_templates = acf_results.get("noise_template", None)
    sigma_self_mhz = acf_results.get("sigma_self_mhz", None)
    for i in tqdm(range(len(acf_results["subband_acfs"])), desc="Fitting Sub-band ACFs"):
        acf_data = acf_results["subband_acfs"][i]
        lags = acf_results["subband_lags_mhz"][i]
        sub_freq = acf_results["subband_center_freqs_mhz"][i]
        sub_bandwidth = (
            acf_results["subband_num_channels"][i] * acf_results["subband_channel_widths_mhz"][i]
        )
        current_fit_lagrange = min(fit_lagrange_mhz, sub_bandwidth / 2.0)
        tpl = noise_templates[i] if noise_templates else None
        fit_result = _fit_acf_models(
            ACF(acf_data, lags),
            current_fit_lagrange,
            sub_freq=sub_freq,
            sigma_self_mhz=sigma_self_mhz,
            noise_template=tpl,
            config=config,
        )
        all_fits.append(fit_result)

    # 1. Get the automatically selected best model via BIC as a default.
    auto_best_model = _select_overall_best_model(all_fits)

    # 2. Check the config for a user-forced model.
    forced_model = fit_config.get("force_model")

    if forced_model:
        # Check if the forced model is a valid option
        valid_models = all_fits[0].keys() if all_fits else []
        if forced_model in valid_models:
            log.warning(
                f"OVERRIDE: User has forced the model to '{forced_model}'. Bypassing BIC selection."
            )
            best_model_name = forced_model
        else:
            log.error(
                f"Invalid model '{forced_model}' specified in config. Falling back to automatic BIC selection."
            )
            log.info(f"Valid model names are: {list(valid_models)}")
            best_model_name = auto_best_model
    else:
        # If no model is forced, use the automatic selection.
        best_model_name = auto_best_model

    # Determine the statistically-justified number of Lorentzian components via the
    # BIC + nested-F-test selector (aggregated across sub-bands). Only Lorentzian-
    # family bursts are eligible; gauss/power/lor_gen stay single-component. This
    # replaces a dead "2c"/"3c"-in-name heuristic that no model ever emitted.
    n_comp_detail = None
    if best_model_name.endswith("lor"):
        num_comps, n_comp_detail = _determine_n_components(acf_results, max_components=3)
    else:
        num_comps = 1

    params_per_comp = [[] for _ in range(num_comps)]

    for i, fits in enumerate(all_fits):
        fit_obj = fits.get(best_model_name)

        if not (fit_obj and fit_obj.success):
            for comp_list in params_per_comp:
                comp_list.append({})
            continue

        p = fit_obj.params
        sub_bw = (
            acf_results["subband_num_channels"][i] * acf_results["subband_channel_widths_mhz"][i]
        )
        gof_metrics = {"bic": fit_obj.bic, "redchi": fit_obj.redchi}

        def get_bw_params(param_name, is_gauss):
            val = p[param_name].value
            err = p[param_name].stderr if p[param_name].stderr is not None else np.nan
            if is_gauss:
                hwhm_factor = np.sqrt(2 * np.log(2))
                return val * hwhm_factor, err * hwhm_factor
            return val, err

        def get_mod_err(param_name):
            param = p.get(param_name)
            return param.stderr if param is not None and param.stderr is not None else np.nan

        # Handle different model types
        if "power" in best_model_name:
            # Power-law model: C(Δν) = c · |Δν|^n
            # No direct "bandwidth" - use characteristic scale at 1 MHz
            prefix = "p_"
            c_val = p[f"{prefix}c"].value
            c_err = p[f"{prefix}c"].stderr if p[f"{prefix}c"].stderr is not None else np.nan
            n_val = p[f"{prefix}n"].value
            n_err = p[f"{prefix}n"].stderr if p[f"{prefix}n"].stderr is not None else np.nan

            # For power-law, store c and n instead of bandwidth and modulation
            # Use c as proxy for "bandwidth scale" and set modulation to NaN
            bw, bw_err = c_val, c_err
            mod, mod_err = np.nan, np.nan  # Power-law has no modulation index

        elif "lor_gen" in best_model_name or "gen" in best_model_name:
            # Generalized Lorentzian: has gamma, alpha, m
            prefix = "lg_"
            bw, bw_err = get_bw_params(f"{prefix}gamma", False)
            mod = p[f"{prefix}m"].value
            mod_err = get_mod_err(f"{prefix}m")

        else:
            # Standard Lorentzian or Gaussian
            is_gauss = "gauss" in best_model_name
            prefix = "g_" if is_gauss else "l_"
            p_root = "sigma" if is_gauss else "gamma"
            bw, bw_err = get_bw_params(f"{prefix}{p_root}", is_gauss)
            mod = p[f"{prefix}m"].value
            mod_err = get_mod_err(f"{prefix}m")

        # Append this sub-band's measurement as the dict contract the power-law
        # consumer below expects (keys bw/mod/bw_err/mod_err/finite_err/gof).
        # _fit_acf_models only yields single-component models, so the measured
        # bandwidth lands in component 0; any extra components (never hit on this
        # path) get {} to keep per-sub-band index alignment with the fail branch.
        measurement = {
            "bw": bw,
            "mod": mod,
            "bw_err": bw_err,
            "mod_err": mod_err,
            # finite-scintle error is already folded into bw_err via the weighted
            # ACF fit (calculate_acf builds it into acf_err); keep nan here so the
            # consumer's quadrature sum does not double-count it.
            "finite_err": np.nan,
            "gof": gof_metrics,
        }
        params_per_comp[0].append(measurement)
        for comp_list in params_per_comp[1:]:
            comp_list.append({})

    # When the selector found >1 Lorentzian component, replace the single-component
    # extraction above with per-component measurements from each sub-band's
    # N-Lorentzian fit (component identity fixed by ascending Δν).
    if num_comps > 1:
        params_per_comp = _extract_multi_component(n_comp_detail, num_comps, len(all_fits))

    final_results = {"best_model": best_model_name, "components": {}}
    final_results["n_components"] = num_comps
    if n_comp_detail is not None:
        final_results["component_selection"] = {
            "n_per_subband": [int(v.get("n_preferred", 1)) for v in n_comp_detail],
            "criterion": n_comp_detail[0].get("criterion") if n_comp_detail else None,
        }
    all_powerlaw_fits = {}

    for i, params_list in enumerate(params_per_comp):
        name = f"component_{i + 1}" if num_comps > 1 else "scint_scale"
        measurements = [p for p in params_list if "bw" in p]

        # Check for non-positive values before taking log
        if not all(p.get("bw", -1) > 0 for p in measurements):
            log.warning(f"Skipping power-law fit for {name}: contains non-positive bandwidths.")
            final_results["components"][name] = {
                "power_law_fit_report": "Fit failed: Non-positive BWs"
            }
            continue

        freqs = np.array(
            [
                acf_results["subband_center_freqs_mhz"][j]
                for j, p in enumerate(params_list)
                if "bw" in p
            ]
        )
        bws = np.array([p.get("bw") for p in measurements])
        bw_errs = np.array([p.get("bw_err") for p in measurements])
        finite_errs = np.array([p.get("finite_err") for p in measurements])
        total_errs = np.sqrt(np.nan_to_num(bw_errs) ** 2 + np.nan_to_num(finite_errs) ** 2)

        # Log-transform the data and errors
        log_freqs = np.log10(freqs)
        log_bws = np.log10(bws)
        # Error propagation: err(log10(y)) = err(y) / (y * ln(10))
        log_bw_errs = total_errs / (bws * np.log(10))

        # Fall back to unweighted ODR when uncertainties are missing or zero
        # (np.nan_to_num converts NaN→0, giving spurious infinite weight).
        use_weights = bool(np.all(np.isfinite(log_bw_errs)) and np.all(log_bw_errs > 0))

        # Define a linear model: f(x) = slope*x + intercept
        linear_model = ModelODR(lambda B, x: B[0] * x + B[1])
        data = RealData(log_freqs, log_bws, sy=log_bw_errs if use_weights else None)

        # Initial guess: slope (alpha) = 4, intercept can be 0
        odr = ODR(data, linear_model, beta0=[4.0, 0.0])
        out = odr.run()

        # Extract results. B[0] is the slope alpha, B[1] is log10(c)
        alpha_fit, log_c_fit = out.beta
        alpha_err, log_c_err = out.sd_beta
        c_fit = 10**log_c_fit

        # Propagate error for bandwidth at reference frequency
        log_ref_freq = np.log10(ref_freq)
        log_b_ref = alpha_fit * log_ref_freq + log_c_fit
        b_ref = 10**log_b_ref

        # Gradient for error propagation in log space
        grad = np.array([log_ref_freq, 1.0])

```

> TOOL

tool_result
id: call_V0A4egxiZpFJLzNDnzSDblaD
```
Exit code: 0
Wall time: 3.2 seconds
Output:
        "m_total": float(np.sqrt(m_wide**2 + m_narrow**2)),
        "center_omitted": True,
    }


def _lor(x, gamma, m):
    """Bare Lorentzian component m²/(1+(x/γ)²); the composite below adds one shared C."""
    return m**2 / (1 + (x / gamma) ** 2)


def _n_lorentzian_model(n):
    """lmfit composite of ``n`` Lorentzians (prefixes l0_, l1_, …) + one shared constant.
    For n=1 this is identical to ``_lorentz_w_c``."""
    from lmfit.models import ConstantModel

    model = ConstantModel(prefix="c_")
    for i in range(n):
        model = model + Model(_lor, prefix=f"l{i}_")
    return model


def _param_stderr(param):
    """lmfit parameter 1σ stderr as a float, or nan when unavailable."""
    e = param.stderr
    return float(e) if e is not None else float("nan")


def compare_lorentzian_components(
    lags, acf, max_components=3, acf_err=None, delta_bic_strong=6.0, p_thresh=0.05
):
    """Decide how many Lorentzian components an ACF statistically supports.

    Fits 1..``max_components`` Lorentzians (+ a shared constant) to the SAME ACF and
    compares neighbouring models two independent ways, which must BOTH agree before a
    component is added:

      - **BIC** — the criterion the pipeline's ``_select_overall_best_model`` already
        uses. Prefer n over n−1 only if ΔBIC = BIC_{n−1} − BIC_n exceeds
        ``delta_bic_strong`` (≈6 ⇒ "strong" on the Kass & Raftery 1995 scale).
      - **nested extra-sum-of-squares F-test** — the (n−1)-component model is nested in
        the n-component one (set the extra m→0), so the two added parameters must cut
        the residual sum of squares significantly (p < ``p_thresh``).

    Requiring both guards against BIC alone accepting a degenerate extra component
    (γ_i≈γ_j or m≈0) that does not actually reduce χ². Caveat: adding a component puts
    the null (m=0) on the parameter-space boundary with γ unidentified there, so the
    F-test p-value is only approximate / mildly anti-conservative (Protassov et al.
    2002, ApJ 571, 545). That is why BIC is the primary, more defensible criterion and
    the F-test is the corroborating second vote, not the sole arbiter.

    Parameters
    ----------
    lags, acf : array
        ACF and its lags (MHz). Use the mean-normalized, lag-0-excluded ACF from
        ``_mean_normalized_acf`` for a Nimmo/Pleunis-consistent comparison. A symmetric
        (±lag) input is reduced to its positive side internally (the ACF is even), so
        the reported ``ndata`` and the BIC/F-test reflect independent points, not the
        mirrored count.
    acf_err : array, optional
        Per-lag ACF uncertainty; when given the fits are χ²-weighted (1/err) so the BIC
        and χ² are on a true-χ² scale (the F-test ratio is valid either way).

    Returns
    -------
    dict
        ``n_preferred`` plus, per n, BIC/AIC/redchi/χ²/n_params/components, and the
        ``delta_bic`` and ``f_test`` p-value for each n vs n−1.
    """
    from scipy.stats import f as f_dist

    lags = np.asarray(lags, dtype=float)
    acf = np.asarray(acf, dtype=float)
    err = np.asarray(acf_err, dtype=float) if acf_err is not None else None
    # The ACF is even, so a symmetric ±lag input duplicates every independent point;
    # counting both sides would inflate ndata and over-state BIC/F-test significance
    # (the penalty term and F dof both scale with ndata). Fit one side (positive lags,
    # lag 0 excluded) — the Lorentzian model is symmetric so the fit is identical but
    # ndata is the true independent-point count.
    side = lags > 0
    if side.sum() >= 3:
        lags, acf = lags[side], acf[side]
        if err is not None:
            err = err[side]
    order = np.argsort(lags)
    lags, acf = lags[order], acf[order]
    if err is not None:
        err = err[order]
    span = float(np.nanmax(lags))
    uniq = np.unique(lags)
    fine = float(np.nanmin(np.diff(uniq))) if uniq.size > 1 else span / 10.0
    peak = float(np.nanmax(acf))
    weights = (1.0 / err) if err is not None else None

    fits = []
    for n in range(1, max_components + 1):
        model = _n_lorentzian_model(n)
        params = model.make_params()
        params["c_c"].set(value=0.0)
        # seed γ_i geometrically across [≈few channels, ≈half-span] so the components
        # start on distinct scales; m_i split from the ACF peak.
        gammas = (
            np.geomspace(max(fine * 2.0, span / 50.0), 0.5 * span, n)
            if n > 1
            else np.array([0.2 * span])
        )
        for i in range(n):
            params[f"l{i}_gamma"].set(value=float(gammas[i]), min=fine / 10.0)
            params[f"l{i}_m"].set(value=float(np.sqrt(max(peak, 1e-3) / n)), min=0.0)
        try:
            res_n = model.fit(acf, params, x=lags, weights=weights)
        except Exception:
            fits.append({"n": n, "success": False, "bic": np.inf, "chi2": np.inf})
            continue

        comps = sorted(
            (
                {
                    "dnu_mhz": abs(res_n.params[f"l{i}_gamma"].value),
                    "m": abs(res_n.params[f"l{i}_m"].value),
                    "dnu_err": _param_stderr(res_n.params[f"l{i}_gamma"]),
                    "m_err": _param_stderr(res_n.params[f"l{i}_m"]),
                }
                for i in range(n)
            ),
            key=lambda c: c["dnu_mhz"],
            reverse=True,
        )
        fits.append(
            {
                "n": n,
                "success": bool(res_n.success),
                "bic": float(res_n.bic),
                "aic": float(res_n.aic),
                "chi2": float(res_n.chisqr),
                "redchi": float(res_n.redchi),
                "n_params": int(res_n.nvarys),
                "ndata": int(res_n.ndata),
                "components": comps,
            }
        )

    # Walk up from 1: accept n only if BIC strongly improves AND the nested F-test is
    # significant; stop at the first n that is not justified (do not skip a level).
    delta_bic = {}
    f_test = {}
    n_pref = 1
    for n in range(2, max_components + 1):
        prev, cur = fits[n - 2], fits[n - 1]
        if not (prev.get("success") and cur.get("success")):
            break
        d_bic = prev["bic"] - cur["bic"]  # > 0 ⇒ n is the better model
        delta_bic[n] = float(d_bic)
        dof_num = cur["n_params"] - prev["n_params"]
        dof_den = cur["ndata"] - cur["n_params"]
        if dof_num > 0 and dof_den > 0 and cur["chi2"] > 0 and prev["chi2"] > cur["chi2"]:
            f_stat = ((prev["chi2"] - cur["chi2"]) / dof_num) / (cur["chi2"] / dof_den)
            p = float(f_dist.sf(f_stat, dof_num, dof_den))
        else:
            p = 1.0
        f_test[n] = p
        if n_pref == n - 1 and d_bic > delta_bic_strong and p < p_thresh:
            n_pref = n
        else:
            break

    return {
        "n_preferred": n_pref,
        "fits": fits,
        "delta_bic": delta_bic,
        "f_test": f_test,
        "criterion": (
            f"BIC ΔBIC>{delta_bic_strong} (Kass-Raftery 'strong') AND nested "
            f"F-test p<{p_thresh}; both required to add a component"
        ),
    }


def compare_components_from_spectrum(
    spec,
    channel_width_mhz,
    max_components=3,

```

> TOOL

tool_result
id: call_fTIHcPLkwUq3wcFOGEAvcEHT
```
Command blocked by PreToolUse hook: rtk-codex-guard: shell command should use RTK compact output.

Suggested command:
rtk grep -n "component|scint_scale|params_per_comp|subband_measurements|bw_at_ref" scintillation/scint_analysis/analysis.py | tail -n 120

To bypass for this command, prefix it with: RTK_DISABLED=1. Command: rg -n "component|scint_scale|params_per_comp|subband_measurements|bw_at_ref" scintillation/scint_analysis/analysis.py | tail -n 120
```

> TOOL

tool_result
id: call_EB2U1oADJoaxqr9pz17XwBTm
```
Command blocked by PreToolUse hook: rtk-codex-guard: shell command should use RTK compact output.

Suggested command:
rtk grep -n "FLITS|scint|revalidation|component|Lorentzian|fit validation" /Users/jakobfaber/.codex/memories/MEMORY.md | head -n 80

To bypass for this command, prefix it with: RTK_DISABLED=1. Command: rg -n "FLITS|scint|revalidation|component|Lorentzian|fit validation" /Users/jakobfaber/.codex/memories/MEMORY.md | head -n 80
```

> AGENT

The checked code confirms the new helpers are present on the branch. I’m doing one narrower pass for the model keys and the downstream component contract, since those are the places a silent mismatch would show up.

> TOOL

tool_use shell_command
id: call_W4DIxiThaVlgsAXkDn0ACEUR
```json
{
  "command": "rtk grep -n \"fit_lor|lor_gen|fit_power|fit_gauss|fit_.*lor|best_model_name|models_to_fit|fit_results\" scintillation/scint_analysis/analysis.py | head -n 180",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_0L86GK5nnzdVYyMrJyNQGO7H
```json
{
  "command": "sed -n '1585,1685p' scintillation/scint_analysis/analysis.py",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_XfXapF4R18c3Y7vKpJYfhyqo
```json
{
  "command": "rtk grep -n \"FLITS|scint|revalidation|component|Lorentzian|fit validation\" /Users/jakobfaber/.codex/memories/MEMORY.md | head -n 80",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_W4DIxiThaVlgsAXkDn0ACEUR
```
Exit code: 0
Wall time: 3 seconds
Output:
19 matches in 1 files:

scintillation/scint_analysis/analysis.py:132:"lor_gen",
scintillation/scint_analysis/analysis.py:135:merge(dict(lg_gamma=0.05, lg_alpha=5 / 3, lg_m=0.8), tag="lor_gen"),
scintillation/scint_analysis/analysis.py:670:fit_results: dict[str, lmfit.ModelResult | None] = {}
scintillation/scint_analysis/analysis.py:736:fit_results[label] = model.fit(
scintillation/scint_analysis/analysis.py:741:fit_results[label] = None
scintillation/scint_analysis/analysis.py:743:return fit_results
scintillation/scint_analysis/analysis.py:1417:best_model_name = forced_model
scintillation/scint_analysis/analysis.py:1423:best_model_name = auto_best_model
scintillation/scint_analysis/analysis.py:1426:best_model_name = auto_best_model
scintillation/scint_analysis/analysis.py:1430:# family bursts are eligible; gauss/power/lor_gen stay single-component. This
scintillation/scint_analysis/analysis.py:1433:if best_model_name.endswith("lor"):
scintillation/scint_analysis/analysis.py:1441:fit_obj = fits.get(best_model_name)
scintillation/scint_analysis/analysis.py:1467:if "power" in best_model_name:
scintillation/scint_analysis/analysis.py:1481:elif "lor_gen" in best_model_name or "gen" in best_model_name:
scintillation/scint_analysis/analysis.py:1490:is_gauss = "gauss" in best_model_name
scintillation/scint_analysis/analysis.py:1523:final_results = {"best_model": best_model_name, "components": {}}
scintillation/scint_analysis/analysis.py:1732:model_to_fit = fit_config.get("intra_pulse_fit_model", "lorentzian_component")
scintillation/scint_analysis/analysis.py:1787:fit_results = _fit_acf_models(
scintillation/scint_analysis/analysis.py:1795:fit_obj = fit_results.get(model_to_fit)

```

> TOOL

tool_result
id: call_0L86GK5nnzdVYyMrJyNQGO7H
```
Exit code: 0
Wall time: 3 seconds
Output:
        grad = np.array([log_ref_freq, 1.0])
        var_log_b_ref = grad @ out.cov_beta @ grad
        # Convert error from log-space back to linear space
        b_ref_err = b_ref * np.sqrt(var_log_b_ref) * np.log(10)

        all_powerlaw_fits[name] = out

        # ================================================================= #
        # Use the fitted alpha and its error to suggest a
        # physical scenario based on the findings from Pradeep et al. (2025)
        # and Nimmo et al. (2025).

        # Interpret the scaling index based on physical expectations
        interpretation = _interpret_scaling_index(alpha_fit, alpha_err)

        subband_measurements = []
        for j, p_dict in enumerate(measurements):
            measurement = {
                "freq_mhz": freqs[j],
                "bw": p_dict.get("bw"),
                "mod": p_dict.get("mod"),
                "bw_err": p_dict.get("bw_err"),
                "mod_err": p_dict.get("mod_err"),
                "finite_err": p_dict.get("finite_err"),
                "gof": p_dict.get("gof", {}),
            }
            subband_measurements.append(measurement)

        final_results["components"][name] = {
            "power_law_fit_report": [c_fit, alpha_fit],  # Store linear-space c and slope alpha
            "scaling_index": alpha_fit,
            "scaling_index_err": alpha_err,
            "bw_at_ref_mhz": b_ref,
            "bw_at_ref_mhz_err": b_ref_err,
            "subband_measurements": subband_measurements,
            "scaling_interpretation": interpretation,
        }

    return final_results, all_fits, all_powerlaw_fits


def attach_scintillation_interpretation(final_results, config):
    """Attach two-screen interpretation to each component of an
    ``analyze_scintillation_from_acfs`` result, in place.

    Per-measurement inputs come from the component itself: m = median of the
    per-subband modulation indices (m = sqrt(ACF peak); frequency-independent),
    Δν_dc = the power-law decorrelation bandwidth at the reference frequency
    (its HWHM). The external science inputs come from an optional
    ``config['source']`` block:
      - ``tau_d_ms``           -> τ_s = C/(2π Δν_dc) consistency check
      - ``d_source_screen_pc`` -> emission-region size (Nimmo et al. 2025 Eqs 21-23)
      - ``distance_mpc``       -> two-screen coherence constraint (needs a 2nd scale)

    Each interpretation attaches ONLY when its required science input is present,
    so on configs that don't carry a ``source`` block the call is a clean no-op
    (Decision 3 of plan-incomplete-work-closeout). ``modulation`` always attaches
    because m is intrinsic to the fit. Follows Nimmo et al. 2025 (arXiv:2406.11053).
    """
    if not isinstance(final_results, dict):
        return final_results

    def _pos(x):  # a usable physical input: present, finite, strictly positive
        try:
            return x is not None and np.isfinite(float(x)) and float(x) > 0
        except (TypeError, ValueError):
            return False

    src = config.get("source", {}) if isinstance(config, dict) else {}
    ref_freq = (
        config.get("analysis", {}).get("fitting", {}).get("reference_frequency_mhz", 600.0)
        if isinstance(config, dict)
        else 600.0
    )
    if not _pos(ref_freq):
        ref_freq = 600.0
    tau_d_ms = src.get("tau_d_ms")
    d_screen_pc = src.get("d_source_screen_pc")
    d_source_mpc = src.get("distance_mpc")

    for comp in final_results.get("components", {}).values():
        meas = comp.get("subband_measurements") if isinstance(comp, dict) else None
        if not meas:  # failed/empty component -> leave untouched
            continue
        mods = np.array([sm.get("mod", np.nan) for sm in meas], dtype=float)
        mod_errs = np.array([sm.get("mod_err", np.nan) for sm in meas], dtype=float)
        m = float(np.nanmedian(mods)) if np.isfinite(mods).any() else np.nan
        m_err = float(np.nanmedian(mod_errs)) if np.isfinite(mod_errs).any() else 0.0
        dnu = comp.get("bw_at_ref_mhz", np.nan)
        dnu_err = comp.get("bw_at_ref_mhz_err", 0.0) or 0.0

        comp["modulation"] = interpret_modulation_index(m, m_err)
        if _pos(tau_d_ms) and _pos(dnu):
            comp["consistency"] = scattering_scintillation_consistency(
                float(tau_d_ms), float(dnu), delta_nu_err_mhz=float(dnu_err)
            )
        if _pos(d_screen_pc) and _pos(dnu) and _pos(m):
            comp["emission_size"] = estimate_emission_region_size(
                m,
                float(dnu),
                float(d_screen_pc),

```

> TOOL

tool_result
id: call_XfXapF4R18c3Y7vKpJYfhyqo
```
Exit code: 0
Wall time: 3 seconds
Output:
69 matches in 1 files:

/Users/jakobfaber/.codex/memories/MEMORY.md:1:# Task Group: /Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa110...
/Users/jakobfaber/.codex/memories/MEMORY.md:3:scope: use when work is happening in the user's FLITS fork and touches CANFAR...
/Users/jakobfaber/.codex/memories/MEMORY.md:4:applies_to: cwd=/Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa1...
/Users/jakobfaber/.codex/memories/MEMORY.md:10:- rollout_summaries/2026-06-19T16-46-02-fWzE-dsa_canfar_path_fix_and_push.md ...
/Users/jakobfaber/.codex/memories/MEMORY.md:20:- extensions/chronicle/resources/2026-06-22T20-40-00-LeQd-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:21:- extensions/chronicle/resources/2026-06-22T20-11-00-aIMp-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:25:- docs/codetection-science-plan.md, CONTEXT.md, docs/adr/0001-two-band-levera...
/Users/jakobfaber/.codex/memories/MEMORY.md:27:## Task 3: Add `consistency_table(...)`, verify the multi-screen signal, and ...
/Users/jakobfaber/.codex/memories/MEMORY.md:31:- extensions/chronicle/resources/2026-06-22T22-09-00-yQgr-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:35:- scintillation/scint_analysis/consistency.py, consistency_table, band_consis...
/Users/jakobfaber/.codex/memories/MEMORY.md:41:- extensions/chronicle/resources/2026-06-22T23-49-00-gBoS-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:42:- extensions/chronicle/resources/2026-06-23T01-44-00-eADA-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:48:## Task 5: Run FLITS tests from a clean Conda environment, push fork `main`, ...
/Users/jakobfaber/.codex/memories/MEMORY.md:52:- extensions/chronicle/resources/2026-06-23T01-44-00-eADA-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:56:- conda run -n flits pytest -m "not slow", ModuleNotFoundError: No module nam...
/Users/jakobfaber/.codex/memories/MEMORY.md:62:- extensions/chronicle/resources/2026-06-23T04-03-00-SJjn-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:72:- extensions/chronicle/resources/2026-06-23T00-32-00-CbTO-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:73:- extensions/chronicle/resources/2026-06-23T00-10-00-FHwB-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:83:- extensions/chronicle/resources/2026-06-23T00-38-00-wvtD-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:84:- extensions/chronicle/resources/2026-06-23T00-37-00-AhTm-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:90:## Task 9: Reproduce the FLITS scattering-refit chain with real local data, p...
/Users/jakobfaber/.codex/memories/MEMORY.md:94:- extensions/chronicle/resources/2026-06-23T00-10-00-FHwB-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:95:- extensions/chronicle/resources/2026-06-23T00-06-00-Hvgz-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:96:- extensions/chronicle/resources/2026-06-23T05-03-00-AKGw-10min-memory-summar...
/Users/jakobfaber/.codex/memories/MEMORY.md:100:- gain_ladder.py, gain_ladder.npz, multiscale_fit.py, joint_json, freya_joint...
[+44 more]

```

> AGENT

So far I see no sign that the new path forks the canonical physics kernel; this is scintillation model-selection wiring. One possible issue remains: the exact suffix gate depends on the generated model labels, so I’m verifying those labels directly.

> TOOL

tool_use shell_command
id: call_x32zMqkIV6ZOUb5bOHGQ48VG
```json
{
  "command": "sed -n '90,160p' scintillation/scint_analysis/analysis.py",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_hJqMulfhTrPBVOce43CNtQ4J
```json
{
  "command": "sed -n '620,755p' scintillation/scint_analysis/analysis.py",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_y6MBHRyTFxo35wyNXQ3H9WsZ
```json
{
  "command": "nl -ba /Users/jakobfaber/.codex/memories/MEMORY.md | sed -n '1,7p'",
  "workdir": "/private/tmp/claude-501/-Users-jakobfaber-Developer-repos-github-com-jakobtfaber-dsa110-FLITS/370d2d4d-f54b-47a1-9bac-3d06ba51d427/scratchpad/wt-wire",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_x32zMqkIV6ZOUb5bOHGQ48VG
```
Exit code: 0
Wall time: 3 seconds
Output:
    )
    return sn, p


def _baseline_registry(cfg_init: dict | None = None):
    """Return a list describing **all** baseline scattering models.

    Parameters
    ----------
    cfg_init : dict | None
        Overrides for the initial‑guess dictionaries below, typically taken
        from YAML → ``analysis → fitting → init_guess``.
    """

    if cfg_init is None:
        cfg_init = {}

    def merge(seed: dict, tag: str):
        """Override hard‑coded seed with YAML values for the given *tag*."""
        merged = seed.copy()
        merged.update(cfg_init.get(tag, {}))
        return merged

    return [
        # ------------------------------------------------------------------
        #  SINGLE‑COMPONENT MODELS
        # ------------------------------------------------------------------
        (
            "lor",
            lorentzian_component,
            "l_",
            merge(dict(l_gamma=0.05, l_m=0.8), tag="lor"),
            lambda p: (p["l_gamma"].set(min=1e-6), p["l_m"].set(min=0)),
        ),
        (
            "gauss",
            gaussian_component,
            "g_",
            merge(dict(g_sigma=0.05, g_m=0.8), tag="gauss"),
            lambda p: (p["g_sigma"].set(min=1e-6), p["g_m"].set(min=0)),
        ),
        (
            "lor_gen",
            lorentzian_generalised,
            "lg_",
            merge(dict(lg_gamma=0.05, lg_alpha=5 / 3, lg_m=0.8), tag="lor_gen"),
            lambda p: (
                p["lg_gamma"].set(min=1e-6),
                p["lg_alpha"].set(min=0.1, max=4.0),
                p["lg_m"].set(min=0),
            ),
        ),
        (
            "power",
            power_law_model,
            "p_",
            merge(dict(p_c=0.01, p_n=-2.0), tag="power"),
            lambda p: p["p_c"].set(min=1e-6),
        ),
    ]


# ----------------------------------------------
# --- Core Calculation and Fitting Functions ---
# ----------------------------------------------

if _NUMBA:

    @nb.njit(cache=True)
    def _acf_with_errs(x, lags, denom):
        nlag = lags.size

```

> TOOL

tool_result
id: call_hJqMulfhTrPBVOce43CNtQ4J
```
Exit code: 0
Wall time: 3 seconds
Output:
                spec_len=len(acf_obj.acf),
                channel_width_mhz=chan_width,
                mask_hash=real_mask_hash,
            )
            if mean_noise_acf is not None:
                # normalise so fitted 'amp' really is the radiometer m-value
                centre = len(mean_noise_acf) // 2
                if mean_noise_acf[centre] != 0:
                    mean_noise_acf /= mean_noise_acf[centre]

        # Store results
        results["noise_template"].append(mean_noise_acf)
        results["subband_acfs"].append(acf_obj.acf)
        results["subband_lags_mhz"].append(acf_obj.lags)
        results["subband_acfs_err"].append(acf_obj.err)
        results["subband_center_freqs_mhz"].append(float(np.mean(sub_freqs)))
        results["subband_channel_widths_mhz"].append(chan_width)
        results["subband_num_channels"].append(sub_spec.count())

        start_idx = end_idx  # next sub‑band
        log.debug(f"Cache now holds {len(_noise_acf_cache)} noise ACF template(s)")

    return results


def _make_noise_model(template, lags):
    """Return (Model, Parameters) with one free amp parameter."""
    shape = template / template[len(template) // 2]  # unity at Δν=0
    f = interp1d(lags, shape, kind="linear", bounds_error=False, fill_value=0.0)

    def noise_tpl(x, amp):
        return amp * f(x)

    nmod = Model(noise_tpl, prefix="n_")
    p = nmod.make_params(amp=0.2, min=0, max=2.0)  # free amplitude
    return nmod, p


def _fit_acf_models(
    acf_object,
    fit_lagrange_mhz: float,
    *,
    sub_freq: float,  # <-- Parameter added
    sigma_self_mhz: float | None = None,
    noise_template: np.ndarray | None = None,
    config=None,
):
    """
    Fit every scattering candidate to one ACF.
    """
    fit_results: dict[str, lmfit.ModelResult | None] = {}

    # --- data slice & weights ---
    m = (np.abs(acf_object.lags) <= fit_lagrange_mhz) & (acf_object.lags != 0)
    x, y = acf_object.lags[m], acf_object.acf[m]
    w = None if acf_object.err is None else 1.0 / np.maximum(acf_object.err[m], 1e-9)

    # --- optional components ---
    has_sn = sigma_self_mhz is not None
    has_tpl = noise_template is not None

    if has_sn:
        sn_model, sn_params = _self_noise_model(sigma_self_mhz)
    if has_tpl:
        tpl_model, tpl_params = _make_noise_model(noise_template, acf_object.lags)

    # --- iterate over baseline registry ---
    init_cfg = config.get("analysis", {}).get("fitting", {}).get("init_guess", {})
    # Note: The `_baseline_registry` needs to be called with the raw `init_cfg`
    for key, mfn, prefix, seed, hook in _baseline_registry(init_cfg):
        # Check if there is a frequency-evolving guess configuration for this model key
        if key in init_cfg and "components" in init_cfg[key]:
            adv_cfg = init_cfg[key]
            ref_freq = adv_cfg["reference_frequency_mhz"]
            p0_dict = adv_cfg.get("constants", {}).copy()

            for i, comp_cfg in enumerate(adv_cfg["components"]):
                comp_idx = i + 1
                alpha = comp_cfg["gamma_scaling_index"]
                gamma_ref = comp_cfg["gamma_guess"]
                scaled_gamma = gamma_ref * (sub_freq / ref_freq) ** alpha
                p0_dict[f"{prefix}gamma{comp_idx}"] = scaled_gamma
                p0_dict[f"{prefix}m{comp_idx}"] = comp_cfg["m_guess"]

        else:
            # Fallback to the old method (static guesses from YAML or defaults)
            merged_seed = seed.copy()
            if key in init_cfg:
                merged_seed.update(init_cfg.get(key, {}))
            p0_dict = merged_seed

        # Build the baseline model and its parameters from our calculated p0_dict
        base_model = Model(mfn, prefix=prefix)
        base_params = base_model.make_params(**p0_dict)
        if hook:
            hook(base_params)

        # Decide which composite we will fit, using the correctly generated base_params
        if has_sn and has_tpl:
            model = sn_model + tpl_model + base_model
            params = sn_params.copy() + tpl_params.copy() + base_params.copy()

        elif has_sn:
            model = sn_model + base_model
            params = sn_params.copy() + base_params.copy()

        elif has_tpl:
            model = tpl_model + base_model
            params = tpl_params.copy() + base_params.copy()

        else:
            model, params = base_model, base_params.copy()

        # Run the fit
        label = f"fit_{'sn_tpl_' if has_sn and has_tpl else 'sn_' if has_sn else 'tpl_' if has_tpl else ''}{key}"
        try:
            fit_results[label] = model.fit(
                y, params, x=x, weights=w, method="nelder", max_nfev=4000
            )
        except Exception as e:
            log.debug(f"{label} failed ({e})")
            fit_results[label] = None

    return fit_results


def _interpret_scaling_index(alpha: float, alpha_err: float) -> str:
    """Interpret the frequency scaling index based on physical expectations.

    Based on theoretical predictions from Bhat et al. (2004) and Nimmo et al. (2025):
    - α ≈ 4.0-4.4: Kolmogorov turbulence (diffractive scintillation)
    - α ≈ 3.9: Global average with inner scale effects (Bhat et al. 2004)
    - α ≈ 3.0: Emission region partially resolved by screen (Nimmo et al. 2025)
    - α ≈ 2.0: Refractive scintillation
    - α ≈ 1.0: Two screens resolving each other (Nimmo et al. 2025)
    - α ≈ 0: No frequency dependence (intrinsic structure or instrumental)

```

> TOOL

tool_result
id: call_y6MBHRyTFxo35wyNXQ3H9WsZ
```
Exit code: 0
Wall time: 3 seconds
Output:
     1	# Task Group: /Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa110-FLITS / CHIME-DSA archive validation, scattering-scintillation checks, and calibration/planning lanes
     2	
     3	scope: use when work is happening in the user's FLITS fork and touches CANFAR/CADC reachability, CHIME/DSA data provenance, two-screen/scintillation planning, fork-vs-HPCC state, or calibration-gated burst-energy outputs under a dirty multi-lane worktree
     4	applies_to: cwd=/Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa110-FLITS, /home/jfaber/flits/dsa110-FLITS, and temporary `/tmp` archive-localization helpers; reuse_rule=safe for this fork + HPCC mirror workflow while CANFAR/VOSpace, `data-manifest.csv`, `scintillation/scint_analysis/`, and calibration seams in `telescopes.yaml` remain the relevant surfaces; treat exact branch names, cert state, test counts, and current dirty-path inventory as time specific
     5	
     6	## Task 1: Fix DSA CANFAR data paths in YAMLs and the manifest, then push the validated branch, success
     7	

```
