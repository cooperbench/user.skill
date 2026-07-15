> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace





        Idea:
Build a reusable prebuilt RunPod/VibeComfy validation environment for Reigh parity work. Context: we are validating Reigh worker VibeComfy parity with Wan2GP across all app capabilities. The current fresh RunPod live-test path spends ~46 minutes in reigh-worker uv sync --extra cuda124 and ~21 minutes installing VibeComfy/ComfyUI/custom nodes before it can run a single workflow. That makes workflow debugging slow, expensive, and noisy. We need a well-engineered solution, not a local hack. Research and implement the right abstraction across the workspace repos as needed (reigh-worker, vibecomfy, runpod-lifecycle, docs/skills). Desired outcome: a reusable validation environment path that can be launched for live tests without reinstalling the CUDA/PyTorch/ComfyUI/VibeComfy/custom-node stack each time, while staying branch-flexible enough to test arbitrary reigh-worker and vibecomfy refs. It should have explicit environment contracts, version metadata, dependency/model/cache preflight, and clear invalidation rules. It should not constrain workflow authoring to one approach or add brittle manual steps. It must improve observability: install/bootstrap phases should expose progress/logs and fail with actionable diagnostics. It must integrate cleanly with the existing live-test harness, RunPod lifecycle tools, workflow contracts, model reconciliation, node-schema validation, and documentation/skill guidance. Think through image vs network-volume cache vs warm persistent pod vs hybrid; pick the pragmatic path and implement it. Validation requirements: local tests for harness behavior, dry-run or unit coverage for selecting prebuilt environment, and at least one actual RunPod validation proving the new path reaches workflow execution materially faster than the cold fresh path and still terminates only pods it owns. Also document how future agents discover and use this path by default.

        Approved plan:

# Implementation Plan: Prebuilt RunPod/VibeComfy Validation Environment (rev 3 — fixups)

## Overview

This revision is a **surgical fixup pass against rev 2**, not another architectural pivot. The bundle-extract architecture (settled decision ARCH-001) is preserved: compressed `tar.zst` bundles live on the RunPod network volume; the consumer pod extracts the venv + vibecomfy install tree to **container-local disk** at boot. The 24 open significant flags from the rev 2 critique are all concrete file/line/decision issues that we correct in place.

**Key corrections folded into this revision:**

1. **Container-disk paths corrected** (correctness-1 / FLAG-009): replace invented `/workspace-local/*` with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` — consistent with the existing `/opt/reigh-worker-live-test-venv` convention. `/workspace` remains the network-volume mountpoint.
2. **ComfyUI bundle merged into venv bundle** (correctness-2): ComfyUI is pip-installed into the venv (`ssh_bootstrap.py:225-227`), so it lives inside `site-packages`. Only **two** bundles: `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The `extract_comfyui_bundle` phase is removed.
3. **`--python` in launch_command parameterized** (correctness-7 / FLAG-010 / all_locations-1): `build_run_worker_command` now takes `python_version` (default `3.10` for the fresh path, manifest-driven for prebuilt). `launch_command.py:43-44` is an enumerated touch point.
4. **HF cache env threaded into `_build_worker_env`** (FLAG-014 / scope-3): `HF_HOME`, `HF_HUB_CACHE`, and the ComfyUI models-path env are added to the worker-env dict that `export_env` serializes, so the worker subprocess inherits them — not just the SSH bootstrap shell.
5. **Region detection via `get_network_volumes()` `dataCenterId`** (correctness-3): `PREBUILT_VOLUME_CANDIDATES` is no longer derived from the legacy `RUNPOD_STORAGE_VOLUMES` name tuple. Instead the consumer enumerates `get_network_volumes(api_key)`, filters by the `reigh-livetest-prebuilt-{profile}-` prefix, and selects by `dataCenterId`.
6. **`find_gpu_type` region wording dropped** (correctness-4): the SDK has no region filter (`runpod-lifecycle/src/runpod_lifecycle/api.py:83-97`). The plan now states the actual mechanism — RunPod pod creation enforces region match implicitly through the attached volume's `dataCenterId`; we let pod-create fail loudly rather than pretending to constrain.
7. **`verify_extracted_env` reordered after syncs and made crash-resistant** (callers-2 / correctness-5): the probe phase runs **after** `sync_worker_ref` and `sync_vibecomfy_ref`, catches non-zero exit codes from each shell probe and translates them to diagnostic strings rather than letting them raise.
8. **Cross-repo import direction fixed** (correctness-6): the prune helper lives in `runpod-lifecycle/src/runpod_lifecycle/guard.py` as `prune_pods_by_prefix(prefixes, api_key, ...)`. `reigh-worker/scripts/live_test/terminate_guard.py` becomes a thin caller. There is no fallback branch — runpod-lifecycle never imports reigh-worker code.
9. **`_register_fresh_worker_record` rename committed** (scope-1 / callers-3): renamed to `register_worker_record(..., variant_label: str)` in `_shared.py`. `variant_fresh.py` passes `variant_label="fresh"`; `variant_prebuilt.py` passes `"prebuilt"`. Both call sites enumerated.
10. **variant_update coexistence guarded** (scope-2): if `variant_update.run` finds a prebuilt manifest at `/workspace/reigh-livetest-prebuilt/env.manifest.json` it refuses with an actionable error (`use --variant prebuilt or invalidate the prebuilt cache first`). This is a one-line check; no other changes to variant_update.
11. **`_FRESH_POD_NAME_RE` enumerated for all three prefixes** (all_locations-2): the regex becomes a tuple of three compiled patterns, each scoped to one prefix, all using the same timestamp suffix `%Y%m%dT%H%M%SZ` (the existing format from `_timestamp_label()`).
12. **`test_primitives.py` import-path updates enumerated** (all_locations-3): test imports of `_phase` / `_redact_sensitive_text` / `_capture_and_redact_noisy_lifecycle_output` get re-exports from `variant_fresh` so existing tests still resolve them. (`from scripts.live_test._shared import _phase as _phase` line added to `variant_fresh.py` keeps the old import path working.)
13. **`__all__` updated** (all_locations-4): `config.py:__all__` is extended to export `PREBUILT_VOLUME_CANDIDATES`, `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH`, `PREBUILT_RUNTIME_WORKER_PATH`, `PREBUILT_RUNTIME_VIBECOMFY_PATH`.
14. **Default `--variant` stays `fresh`** (issue_hints-2): the rev 2 plan flipped the default to `auto`; reverted here. `--variant auto` is opt-in. Future flip can be a separate migration with release-note coverage. Skill + docs still recommend `--variant auto`, which is the durable discovery story.
15. **Node-schema validation runs on every prebuilt run** (issue_hints-3): a cheap read-only `python -m vibecomfy.cli nodes verify --lockfile custom_nodes.lock` (or equivalent template_index sanity probe) runs in the bootstrap regardless of lockfile drift. Destructive `nodes restore` still gated on `custom_nodes_lock_hash` drift.
16. **Dry-run plan honors variant venv path** (callers-1): `_print_dry_run_plan` (or `variant_prebuilt._print_dry_run_plan`) takes `venv_path` and `python_version` from the contract so dry-run output for the prebuilt variant displays the correct paths.
17. **Model warming product call** (issue_hints-1 / FLAG-008): accept v1 first-run model cold-download as in-scope cost; the prebuilt env materially improves *deps* time (67 min → ~10 min) and **steady-state** model time (subsequent runs reuse `models/` via `HF_HOME`). A future `rl prebuilt warm-models <recipe>` verb is explicitly deferred to v2 and tracked as an open question, not a v1 requirement.

**Updated key-file touchpoints (additions over rev 2 enumerated):**

- `reigh-worker/scripts/live_test/launch_command.py:37, 43-44` (add `venv_path` and `python_version` kwargs)
- `runpod-lifecycle/src/runpod_lifecycle/guard.py` (new — houses `prune_pods_by_prefix`)
- `reigh-worker/scripts/live_test/variant_update.py` (add prebuilt-manifest-present guard only)
- `reigh-worker/scripts/live_test/_shared.py` (now also owns `register_worker_record`, re-exports preserved for test compat)
- `reigh-worker/scripts/live_test/config.py:__all__` (export new prebuilt constants)
- `reigh-worker/scripts/live_test/variant_fresh.py` (compatibility re-exports for `_phase`, `_redact_sensitive_text`, `_capture_and_redact_noisy_lifecycle_output`)

**Decisions explicitly settled (not re-litigated here):** ARCH-001 through ARCH-007 from the gate's settled-decisions list — bundle architecture, hard-fail invalidation triggers, pod-name prefixes, variant_update out of scope, build.lock concurrency, helper extraction before new variant, committed skill manifest as discovery surface.

---

## Phase 1: Foundation — Bundle Contract, Manifest, Atomic Layout

### Step 1: Define the bundle-based env contract (`runpod-lifecycle/src/runpod_lifecycle/prebuilt.py`)
**Scope:** Medium
1. **Create** the module with:
   - `@dataclass(frozen=True) PrebuiltEnvContract`: `volume_name`, `data_center_id`, `mount_path` (default `/workspace`), `cache_root` (default `{mount_path}/reigh-livetest-prebuilt`, **on volume**), `runtime_venv_path` (default `/opt/reigh-worker-live-test-venv`, **container disk** — matches existing convention), `runtime_worker_path` (default `/opt/reigh-livetest-prebuilt/worker`, **container disk**), `runtime_vibecomfy_path` (default `/opt/reigh-livetest-prebuilt/vibecomfy`, **container disk**), `models_path` (default `{cache_root}/models`, **stays on volume**), `attention_profile`, `comfyui_pin`, `python_version` (e.g. `3.10` or `3.11`), `bundle_format_version` (int).
   - `@dataclass(frozen=True) PrebuiltManifest`: `schema_version: int`, `bundle_format_version: int`, `built_at_utc: str`, `built_by: str`, `pyproject_hash: str`, `custom_nodes_lock_hash: str`, `comfyui_pin: str`, `attention_profile: str`, `python_version: str`, `cuda_extra: str` (literal `cuda124`), `vibecomfy_commit: str`, `reigh_worker_commit: str`, `uv_version: str`, `venv_bundle_sha256: str`, `vibecomfy_bundle_sha256: str`, `models_index_sha256: str`, `notes: str`. **(Note: no `comfyui_bundle_sha256` field — ComfyUI is in the venv.)**
   - `compute_pyproject_hash(text)`, `compute_lockfile_hash(text)` (SHA256 of canonicalized newline-normalized content).
   - `manifest_path(contract)` → `{cache_root}/env.manifest.json`.
   - `lock_path(contract)` → `{cache_root}/build.lock`.
   - `staging_path(contract)` → `{cache_root}/.staging-{uuid}`.
2. **Document** invalidation precedence:
   - **HARD-FAIL** (operator must rerun `rl prebuilt build`): `schema_version`, `bundle_format_version`, `python_version`, `cuda_extra` drift.
   - **Delta-sync**: `pyproject_hash`, `custom_nodes_lock_hash`, `comfyui_pin`, `vibecomfy_commit`, `reigh_worker_commit` drift.
   - **No-op**: all hashes match.
3. **Export** all symbols from `runpod_lifecycle/__init__.py`.

### Step 2: SSH-side helpers (`runpod-lifecycle/src/runpod_lifecycle/prebuilt.py`)
**Scope:** Small
1. **Add** `read_manifest(ssh, contract) -> PrebuiltManifest | None`.
2. **Add** `write_manifest(ssh, contract, manifest)` via heredoc + atomic `mv`.
3. **Add** `acquire_build_lock(ssh, contract, *, holder_id, ttl_sec=7200)` — O_EXCL lockfile with TTL takeover; returns release callback.
4. **Add** `verify_extracted_env(ssh, contract, manifest) -> list[str]` returning a list of partial-state issue strings (empty == healthy). Each probe runs via `_execute(ssh, cmd, check=False)` so non-zero exits **never raise inside the probe**; instead the probe captures stderr (first/last 50 lines) and emits a diagnostic string. Probes:
   - `(a)` `bash -c 'cd {runtime_worker_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} uv run --python {python_version} python -c "import torch; print(torch.version.cuda)"'` — issue if exit != 0 OR stdout != manifest.cuda_extra-derived expected (`12.4` for `cuda124`).
   - `(b)` `test -f {runtime_vibecomfy_path}/template_index.json && test -f {runtime_vibecomfy_path}/workflow_corpus/manifests/coverage.json`.
   - `(c)` `du -sb {runtime_venv_path}/lib | awk '{print $1}'` — issue if reported size is more than 20% smaller than manifest's recorded venv size (a marker we add to the manifest as `venv_size_bytes`).
   - `(d)` `bash -c 'cd {runtime_vibecomfy_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} python -m vibecomfy.cli nodes verify --lockfile custom_nodes.lock'` — **node-schema validation** (issue_hints-3). Issue on non-zero exit; diagnostic includes the literal `rl prebuilt build` and `rl prebuilt invalidate` commands.

### Step 3: Refactor install helpers into bundle-aware primitives (`reigh-worker/scripts/live_test/ssh_bootstrap.py`)
**Scope:** Medium
1. **Extract** `_uv_sync_shell(workdir, *, env_path, extras=("cuda124",), with_locked=False)`. `extras` is mandatory non-empty (raises `ValueError` otherwise). `run_install` wraps with the original args, preserving byte-identical output.
2. **Extract** `_vibecomfy_install_shell(workdir, *, python_path, attention_profile, run_nodes_restore=True)`. `clone_and_install_vibecomfy` wraps with the original args.
3. **Add** bundle helpers:
   - `bundle_venv(ssh, *, source_env_path, bundle_path)` — `tar --use-compress-program "zstd -1 --threads=0" -cf {staging} … && sha256sum && mv {staging} {bundle_path}`.
   - `bundle_install_tree(ssh, *, source_path, bundle_path)` — same.
   - `extract_bundle_to_container_disk(ssh, *, bundle_path, target_path, expected_sha256)` — `mkdir -p {target_path}`, verify sha, extract with `pv` for progress; on sha mismatch raise with first/last 50 lines of stderr.
   - `ensure_git_ref_synced(ssh, *, workdir, repo_url, ref, force_clone=False)` — non-`uv-sync` helper. On force_clone: full clone. Else: `git fetch && git checkout && git reset --hard FETCH_HEAD && git clean -ffd`.
4. **Re-implement** `run_install` and `clone_and_install_vibecomfy` as thin wrappers (no behavioral change for `variant_fresh.py` — verified by golden-string regression tests in Step 11).
5. **Decision**: `_vibecomfy_install_shell` accepts `run_nodes_restore=True|False`. Full-install wrappers pass `True`. Consumer passes `lock_hash_drifted`. The read-only **node-schema verify** is a separate cheap probe in Step 2.4(d) and runs **every time** regardless of restore.

### Step 4: Parameterize launch_command (`reigh-worker/scripts/live_test/launch_command.py`, `tests/test_primitives.py`)
**Scope:** Small (now addresses both venv_path and python_version)
1. **Change** `build_run_worker_command` signature to add two new keyword args: `venv_path: str = "/opt/reigh-worker-live-test-venv"` and `python_version: str = "3.10"`. Both keyword-only.
2. **Edit** `launch_command.py:37` to use `venv_path` in the `UV_PROJECT_ENVIRONMENT` export.
3. **Edit** `launch_command.py:43-44` (the `--python 3.10` literal) to use `python_version`.
4. **Update** `variant_fresh.py:457-464` and `variant_fresh.py:304-312` (the dry-run `_print_dry_run_plan` call) to **explicitly omit the kwargs** (keeps defaults; behavior unchanged).
5. **Add** a contract-aware path in `variant_prebuilt.py` that passes `venv_path=contract.runtime_venv_path` and `python_version=contract.python_version`. The corresponding `_print_dry_run_plan` in `variant_prebuilt.py` does the same.
6. **Update** `tests/test_primitives.py:870, 2317-2319, 2445`: change assertions to verify the **mechanism** (the function emits `UV_PROJECT_ENVIRONMENT="{venv_path}"` and `--python {python_version}` from the kwargs) rather than the literal string. Add new tests: `build_run_worker_command(venv_path="/custom", python_version="3.11")` emits both substitutions; defaults preserve the legacy strings.

### Step 5: Extract shared helpers + commit to rename (`reigh-worker/scripts/live_test/_shared.py`, `variant_fresh.py`)
**Scope:** Medium
1. **Create** `_shared.py` and move verbatim: `_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume` (new, accepting `candidate_names`, optional `data_center_filter`).
2. **Move + rename** `_register_fresh_worker_record` (`variant_fresh.py:262-299`) to `register_worker_record(db, pod_id, pod, args, *, variant_label: str)`. The function body uses `variant_label` in place of the literal `FRESH_VARIANT`. `variant_fresh.run` calls it with `variant_label="fresh"`; `variant_prebuilt.run` calls it with `variant_label="prebuilt"`. The `args.backend / args.worker_profile / args.selector_namespace / args.selector_version / args.worker_contract_version` reads are preserved — Step 9.3 confirms `variant_prebuilt` argparse inherits these flags from the shared parser.
3. **Update** `variant_fresh.py` to import from `_shared`. **Preserve backward-compatible names**: at the top of `variant_fresh.py`, re-export the moved symbols (`_phase = _shared._phase`, etc.) so any existing test that does `from scripts.live_test.variant_fresh import _phase` still resolves (addresses all_locations-3).

---

## Phase 2: Builder — Atomic Volume Provisioner with Lock + Multi-Region

### Step 6: Add `prebuilt` CLI verb (`runpod-lifecycle/src/runpod_lifecycle/cli.py`, `runpod-lifecycle/src/runpod_lifecycle/guard.py`)
**Scope:** Medium
1. **Read** `cli.py` to confirm subparser registration mechanism; register `prebuilt build|inspect|invalidate|list`.
2. **`prebuilt build` args:** `--volume-name` (required), `--data-center` (required), `--attention-profile {portable,sage}` (default portable), `--worker-ref` (default main), `--vibecomfy-ref` (default main), `--gpu-type` (default `NVIDIA GeForce RTX 4090`), `--container-disk-gb` (default 200; floor 100 — must be ≥ 100), `--volume-disk-gb` (default 500), `--python-version` (default `3.10`), `--dry-run`, `--force` (override lock).
3. **Builder flow phases** (each `_phase` wrapped, mirroring `variant_fresh.py:189-211`):
   - `provision_builder_pod`: pod prefix **`reigh-livetest-builder-`** + timestamp suffix `%Y%m%dT%H%M%SZ`.
   - `acquire_lock`.
   - `clone_repos`: clone reigh-worker → `/opt/build/reigh-worker`, vibecomfy → `/opt/build/vibecomfy` (container disk).
   - `install_worker`: `_uv_sync_shell(env_path="/opt/reigh-worker-live-test-venv", extras=("cuda124",))`.
   - `install_vibecomfy`: `_vibecomfy_install_shell(workdir=/opt/build/vibecomfy, run_nodes_restore=True)`.
   - `bundle_artifacts`: `bundle_venv` to `{cache_root}/venv.cuda124.tar.zst`, `bundle_install_tree` to `{cache_root}/vibecomfy.tar.zst`. **No `comfyui.tar.zst`** — ComfyUI lives inside the venv (correctness-2).
   - `seed_models_dir`: `mkdir -p {models_path}`, write empty `INDEX.json` if absent.
   - `write_manifest`.
   - `release_lock`.
   - `terminate_builder_pod`: `guarded_terminate(pod_id, api_key, no_terminate=False)`.
4. **New module `runpod-lifecycle/src/runpod_lifecycle/guard.py`** (addresses correctness-6 with the correct import direction):
   - `prune_pods_by_prefix(prefixes: tuple[str, ...], api_key: str, *, stale_age_sec: int = 6*60*60) -> StalePodCleanupResult` — same shape as the existing `prune_stale_live_test_pods`, but parametric on `prefixes`.
   - The accompanying compiled regex tuple: one `re.compile(rf"^{prefix}(\d{{8}})t(\d{{6}})z$")` per prefix.
   - `runpod-lifecycle` has **no dependency on `reigh-worker`** — this module is freestanding.
5. **`prebuilt inspect`**: provisions a small probe pod, attaches volume, runs `read_manifest`, prints; terminates. (Open question carried forward: whether to allow `--pod` to skip probe-pod provisioning. v1: provision-and-terminate; cost is negligible at minutes-per-call.)
6. **`prebuilt invalidate`**: `rm -rf {cache_root}/{venv.cuda124.tar.zst,vibecomfy.tar.zst,env.manifest.json}` (preserves `models/` and `build.lock`).
7. **`prebuilt list`**: enumerates `get_network_volumes(api_key)`, filters by name prefix `reigh-livetest-prebuilt-`, prints `{name, dataCenterId, size}` for each. No probe pod required (skips manifest content).

### Step 7: Multi-region volume convention (`runpod-lifecycle/src/runpod_lifecycle/prebuilt.py`, `reigh-worker/scripts/live_test/config.py`)
**Scope:** Small (corrected for correctness-3 / correctness-4)
1. **Volume naming convention**: `reigh-livetest-prebuilt-{profile}-{datacenterid-lowercased}`, where `{datacenterid-lowercased}` is RunPod's `dataCenterId` (e.g. `eu-no-1`, `eu-cz-1`, `eur-is-1`). Operator builds one per region they want covered. **Not derived from `RUNPOD_STORAGE_VOLUMES`** (which contains volume names like `Peter`, not regions).
2. **Consumer-side resolution** (`config.py`): no static `PREBUILT_VOLUME_CANDIDATES` tuple. Instead `_shared.select_network_volume` enumerates `get_network_volumes(api_key)`, filters by prefix `reigh-livetest-prebuilt-{profile}-`, returns `(volume_id, name, data_center_id)` for the **first match** (or all matches if caller wants priority). `config.py` exposes a single constant `PREBUILT_VOLUME_NAME_PREFIX = "reigh-livetest-prebuilt-"` and a helper `prebuilt_name_for_profile(profile: str, data_center_id: str) -> str`.
3. **GPU region pin**: `find_gpu_type` in `runpod-lifecycle/src/runpod_lifecycle/api.py:83-97` has **no region filter**. We don't pretend otherwise. Pod creation enforces region implicitly via the attached `network_volume_id`'s `dataCenterId`; if the resolved GPU is in a different region the RunPod API returns an error. We surface that error verbatim with hint text suggesting `rl prebuilt list` to pick a region.
4. **`__all__` update**: `config.py:173-203` adds `PREBUILT_VOLUME_NAME_PREFIX`, `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH`, `PREBUILT_RUNTIME_WORKER_PATH`, `PREBUILT_RUNTIME_VIBECOMFY_PATH`, `prebuilt_name_for_profile`.
5. **Document** in Step 13 docs: "volume is region-pinned by its `dataCenterId`; build at least one region; consumer auto-selects the first matching volume; if no matching GPU is available in that region, build another region's volume."

---

## Phase 3: Consumer — `variant_prebuilt.py` with Reordered Phases + Worker-Env Threading

### Step 8: New consumer variant (`reigh-worker/scripts/live_test/variant_prebuilt.py`)
**Scope:** Medium
1. **Create** the module importing from `_shared`. Skeleton: prepare_context → validate_cases → create_pod → SSH → bootstrap → launch_worker → matrix → report → guarded_terminate.
2. **Pod creation differences**:
   - Pod name prefix: `reigh-livetest-prebuilt-` + timestamp `%Y%m%dT%H%M%SZ`.
   - Volume selection: `select_network_volume(api_key, name_prefix="reigh-livetest-prebuilt-{profile}-")`. Returns first match with `(id, name, data_center_id)`. If no match → raise with the **exact** `rl prebuilt build --volume-name {recommended_name} --data-center {EU-NO-1} --attention-profile portable` command.
   - GPU region: no SDK-side filter (correctness-4). Pod-create is the gate; if RunPod refuses, surface the error with a hint to `rl prebuilt list`.
   - Container disk: floor 100 GB, default 200 GB. Reject `--container-disk-gb < 100`.
3. **Bootstrap phases** (each `_phase` wrapped, **reordered so verify runs after syncs** — addresses callers-2):
   - `attach_prebuilt_volume` — `mountpoint -q /workspace`.
   - `read_prebuilt_manifest` — `read_manifest`. If `None` → raise with the `rl prebuilt build` command.
   - `check_hard_fail_drift` — compare `schema_version`/`bundle_format_version`/`python_version`/`cuda_extra` only. If any drift → raise with the `rl prebuilt build` command; **never delta-sync** these.
   - `extract_venv_bundle` — extract `venv.cuda124.tar.zst` to `/opt/reigh-worker-live-test-venv` (container disk).
   - `extract_vibecomfy_bundle` — extract `vibecomfy.tar.zst` to `/opt/reigh-livetest-prebuilt/vibecomfy` (container disk). **No comfyui_bundle phase**.
   - `sync_worker_ref` — `ensure_git_ref_synced` for `/opt/reigh-livetest-prebuilt/worker` (we treat the bundle's worker tree as a starting point and check out `args.ref`). If `pyproject_hash` drifted: `_uv_sync_shell(env_path=runtime_venv_path, extras=("cuda124",))`. **`extras=("cuda124",)` is mandatory** (correctness-3).
   - `sync_vibecomfy_ref` — `ensure_git_ref_synced` for the vibecomfy tree to `args.vibecomfy_ref`. If `custom_nodes_lock_hash` drifted: `_vibecomfy_install_shell(..., run_nodes_restore=True)`. Else: `pip install -e .` only.
   - `verify_extracted_env` — runs `verify_extracted_env(ssh, contract, manifest)` from Step 2.4. Any returned issue raises with a numbered diagnostic + `rl prebuilt invalidate && rl prebuilt build` instruction. **Always includes the node-schema verify probe (Step 2.4d) regardless of lockfile drift** — addresses issue_hints-3.
   - `bind_models_dir` — compute `HF_HOME = {models_path}/huggingface`, `HF_HUB_CACHE = {models_path}/huggingface/hub`, and the ComfyUI models path env var (decided at implementation time after inspecting vibecomfy/ComfyUI's loader — write `extra_model_paths.yaml` at `{runtime_vibecomfy_path}/extra_model_paths.yaml` as a fallback). **Add these three values to `worker_env`** (the dict passed to `export_env` and used by `launch_worker_detached`) so the worker subprocess inherits them. This addresses FLAG-014 / scope-3.
   - `launch_worker` — `build_run_worker_command(workdir=runtime_worker_path, venv_path=contract.runtime_venv_path, python_version=contract.python_version, …)`.
4. **`_build_worker_env` change** (in `variant_prebuilt.py`): a thin wrapper around `_shared._build_worker_env_base` (which we keep in `_shared.py` or re-export from `variant_fresh.py`) that additionally inserts `HF_HOME`, `HF_HUB_CACHE`, and `COMFYUI_EXTRA_MODEL_PATHS` (or whichever env var the ComfyUI fork honors). The fresh variant's env-builder is unchanged.
5. **Manifest update after delta sync**: when `sync_worker_ref` or `sync_vibecomfy_ref` mutate the cache, the consumer **does not rewrite the manifest on the volume** by default (avoids cross-operator race). Optional `--update-manifest-on-sync` flag rewrites it under `acquire_build_lock`.
6. **Strict mode**: `--strict-prebuilt` aborts on any drift (including soft) without syncing.

### Step 9: CLI dispatch and auto-detect (`reigh-worker/scripts/live_test/main.py`, `config.py`)
**Scope:** Small (default stays `fresh` — addresses issue_hints-2)
1. **Dispatch**: add `prebuilt` and `auto` to the variant switch. Default **remains `fresh`** — no silent dispatch change.
2. **`--variant auto`** (opt-in): preflights `select_network_volume(name_prefix=PREBUILT_VOLUME_NAME_PREFIX)`. If a volume exists AND its manifest is readable → dispatch `prebuilt`. Else → dispatch `fresh` and emit a structured `prebuilt_unavailable` log line.
3. **Argparse additions on the shared parser**: `--prebuilt-volume-name`, `--strict-prebuilt`, `--allow-delta` (default true), `--update-manifest-on-sync`. The existing shared flags `--backend`, `--worker-profile`, `--selector-namespace`, `--selector-version`, `--worker-contract-version` continue to be parsed for all variants — explicitly confirmed via argparse subparser inheritance so `register_worker_record` finds them on the `args` namespace (addresses callers-3).
4. **Container-disk floor 100 GB** enforced for prebuilt variant; default 200 GB. `project_live_test_disk.md` constraint preserved.
5. **Skill and docs (Step 13) recommend** `--variant auto` as the default invocation for future agents; main.py argparse default is `fresh` for backward compatibility.

### Step 10: Pod-prefix and termination wiring (`reigh-worker/scripts/live_test/terminate_guard.py`)
**Scope:** Small (regex enumerated for all three prefixes — addresses all_locations-2)
1. **Replace** the single `LIVE_TEST_FRESH_POD_PREFIX` with a tuple `LIVE_TEST_POD_PREFIXES: tuple[str, ...] = ("reigh-live-test-fresh-", "reigh-livetest-prebuilt-", "reigh-livetest-builder-")`.
2. **Replace** `_FRESH_POD_NAME_RE` with `_LIVE_TEST_POD_NAME_RES: tuple[re.Pattern, ...] = tuple(re.compile(rf"^{re.escape(p)}(\d{{8}})t(\d{{6}})z$") for p in LIVE_TEST_POD_PREFIXES)` — one pattern per prefix, **all using the same timestamp suffix `%Y%m%dT%H%M%SZ`** (the existing format from `_timestamp_label()`). Step 6.3 explicitly states builder pods use the same suffix; Step 8.2 same for prebuilt pods.
3. **Update** `prune_stale_live_test_pods` to delegate to `runpod_lifecycle.guard.prune_pods_by_prefix(LIVE_TEST_POD_PREFIXES, api_key, …)`. Existing call sites unchanged. **Preserves `guarded_terminate` semantics** (single-pod action).

### Step 11: variant_update coexistence guard (`reigh-worker/scripts/live_test/variant_update.py`)
**Scope:** Small (addresses scope-2)
1. **Add** at the top of `variant_update.run` (before any `uv sync` issue): SSH `test -f /workspace/reigh-livetest-prebuilt/env.manifest.json`. If exit code 0 → raise `RuntimeError("Prebuilt cache present at /workspace/reigh-livetest-prebuilt; --variant update would mutate the cached venv at /opt/reigh-worker-live-test-venv. Use --variant prebuilt instead, or run `rl prebuilt invalidate --volume-name X` first.")`.
2. **No other changes** to `variant_update.py`. This is a single guard line, no scope creep. The variant_update success criterion stays: file unchanged except for this guard.

---

## Phase 4: Tests, Real Validation, Docs/Skills

### Step 12: Local tests (`runpod-lifecycle/tests/test_prebuilt.py`, `reigh-worker/scripts/live_test/tests/test_variant_prebuilt.py`, updates to `test_primitives.py`)
**Scope:** Medium
1. **Unit tests for `prebuilt.py`**: hash determinism; manifest round-trip; drift detection per field; `schema_version`/`bundle_format_version`/`python_version`/`cuda_extra` drift each return `hard_fail`; `pyproject_hash`/`custom_nodes_lock_hash`/`comfyui_pin`/`vibecomfy_commit`/`reigh_worker_commit` drift each return `delta_sync`; lockfile acquire/release + TTL takeover.
2. **Unit tests for `ssh_bootstrap.py` refactor**: `run_install` and `clone_and_install_vibecomfy` emit **byte-identical** commands (golden-string compare) vs the pre-refactor capture. `_uv_sync_shell(extras=())` raises `ValueError`. `ensure_git_ref_synced` emits the expected sequence **without any `uv sync`**.
3. **`launch_command.py` tests**: `build_run_worker_command()` defaults emit `UV_PROJECT_ENVIRONMENT="/opt/reigh-worker-live-test-venv"` and `--python 3.10` (existing behavior). `build_run_worker_command(venv_path="/x", python_version="3.11")` emits `UV_PROJECT_ENVIRONMENT="/x"` and `--python 3.11`. Update `test_primitives.py:870, 2317-2319, 2445` to match the mechanism-based assertions.
4. **Harness tests for `variant_prebuilt`** with fake SSH capturing commands:
   - manifest match → zero install commands issued; `verify_extracted_env` runs (after sync phases).
   - `pyproject_hash` drift → `_uv_sync_shell(extras=("cuda124",))` issued.
   - `custom_nodes_lock_hash` drift → destructive `nodes restore` issued.
   - `vibecomfy_commit` only drift → `git checkout` + `pip install -e` but NO `nodes restore`.
   - `python_version` drift → raises with `rl prebuilt build` text; no extract / sync attempted.
   - `schema_version` drift → raises with `rl prebuilt build` text; no extract / sync attempted.
   - missing manifest → raises with literal substring `rl prebuilt build --volume-name`.
   - **Phase order test**: in the success path, `verify_extracted_env` is invoked AFTER `sync_worker_ref` and `sync_vibecomfy_ref` (captured command order).
5. **Worker-env test**: `variant_prebuilt._build_worker_env(...)` returns a dict containing `HF_HOME`, `HF_HUB_CACHE`, and a ComfyUI models-path key — none of which appear in the fresh variant's env builder.
6. **variant_update guard test**: with a fake SSH that reports manifest present, `variant_update.run` raises with the literal substring `Prebuilt cache present` before any `uv sync` is issued.
7. **terminate_guard regex test**: each of the three prefixes matches a pod name like `reigh-livetest-prebuilt-20260513t120000z`, `reigh-livetest-builder-20260513t120000z`, `reigh-live-test-fresh-20260513t120000z`.
8. **Dry-run tests**: `--variant prebuilt --dry-run` and `--variant auto --dry-run` complete without RunPod credentials. `auto` falls back to fresh when `select_network_volume` returns `None`; picks prebuilt when a volume is returned. **Dry-run output for prebuilt variant shows `runtime_venv_path` and `python_version` from the contract, not the fresh defaults** (addresses callers-1).
9. **test import-path compat**: any existing `from scripts.live_test.variant_fresh import _phase` or similar still resolves via the re-exports in Step 5.3.

### Step 13: Real RunPod validation (operator)
**Scope:** Small
1. **Build**: `rl prebuilt build --volume-name reigh-livetest-prebuilt-portable-eu-no-1 --data-center EU-NO-1 --attention-profile portable --worker-ref main --vibecomfy-ref main --python-version 3.11`. Capture builder phase timings.
2. **Run consumer twice** (single small case `z_image_turbo`):
   - Run A (cold model cache): `python -m scripts.live_test --variant prebuilt --backend vibecomfy --case z_image_turbo`. Measure pod-create → `launch_worker` elapsed (excludes model download).
   - Run B (warm model cache, 5 min later): same command. Verifies HF cache reuse.
3. **Assert**: Run A bootstrap (pod-create → `launch_worker`) under **10 min** (vs ~67 min cold). Run B's workflow-execute phase shows no HF download log lines for the model weights used by `z_image_turbo`.
4. **Verify**: post-run RunPod listing shows only the consumer pod terminated; the builder pod is already gone; volume persists.
5. **Capture** under `reigh-worker/scripts/live_test/runs/{timestamp}/prebuilt-validation.md` with phase timings.

### Step 14: Documentation and skill discovery (`docs/migration-vibecomfy-live-validation.md`, `reigh-worker/.claude/skills/live-test/SKILL.md`, `vibecomfy/CLAUDE.md`)
**Scope:** Small
1. **`docs/migration-vibecomfy-live-validation.md`**: new section "Prebuilt validation environment" covering: bundle architecture (extract-to-container-disk), hard-fail vs delta-sync drift rules, region-pinned volume naming + auto-selection, model-cache layout + first-run cold-download caveat, partial-state diagnostics, concurrent-builder lock, variant_update coexistence guard, `--variant auto` opt-in.
2. **`reigh-worker/.claude/skills/live-test/SKILL.md`** (new committed file): names `--variant auto` as the recommended invocation; cross-references the doc above.
3. **`vibecomfy/CLAUDE.md`**: one-line pointer in the decision-shortcuts section.

---

## Execution Order

1. **Phase 1 first**: contract + manifest + helper extraction (Steps 1–5). `variant_fresh.py` remains observably unchanged — verified by golden-string tests in Step 12.2.
2. **Phase 2 second**: builder CLI + `runpod_lifecycle.guard` module (Steps 6–7). Builder is independently usable.
3. **Phase 3 third**: consumer variant + variant_update guard + terminate_guard regex (Steps 8–11).
4. **Phase 4 last**: tests in Step 12 are written alongside Phases 1–3 (test-driven where cheap); Step 13 real run after Step 12 passes; Step 14 docs at the end.

## Validation Order

1. **Cheap first**: unit tests for `prebuilt.py` and `ssh_bootstrap.py` golden-string regression (Steps 12.1–12.2).
2. **`launch_command.py` parameterization** + `test_primitives.py` fixture updates (Step 12.3).
3. **Dry-run**: `--variant prebuilt --dry-run` and `--variant auto --dry-run` (Step 12.8).
4. **Harness tests** (Step 12.4) — fake SSH, phase-order assertion, drift behavior.
5. **Real RunPod**: Step 13 — single case, two runs (bootstrap-time + model-cache-warm).
6. **Full matrix run** (operator, info-only).


        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-12T22:31:34Z",
  "hash": "sha256:af6309b0c0758b8899a06dac4a602c7555ca79808378b8a1f8ed1d1c8871346a",
  "changes_summary": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
  "flags_addressed": [
    {
      "id": "FLAG-008",
      "resolution": "addressed",
      "reason": "Product call recorded: v1 accepts first-run model cold-download as in-scope cost; the prebuilt env materially improves deps install (67min \u2192 ~10min) and steady-state model reuse via HF_HOME on the volume. `rl prebuilt warm-models <recipe>` is explicitly deferred to v2 and tracked in the questions field, not as a v1 requirement. Step 13.3 success criterion measures Run B (5 min later) for HF cache reuse, which is the actual reusable-cache claim."
    },
    {
      "id": "issue_hints-1",
      "resolution": "addressed",
      "reason": "Same product call as FLAG-008 \u2014 first-run cold download accepted as v1 scope; models_path + HF_HOME plumbing means subsequent runs reuse the cache. v2 will add explicit warming."
    },
    {
      "id": "issue_hints-2",
      "resolution": "addressed",
      "reason": "Step 9.1 reverts the rev 2 default flip \u2014 --variant default REMAINS `fresh`. --variant auto is opt-in. Skill (Step 14.2) and docs (Step 14.1) recommend the auto invocation. No silent dispatch change."
    },
    {
      "id": "issue_hints-3",
      "resolution": "addressed",
      "reason": "Step 2.4(d) and Step 8.3 verify_extracted_env phase always runs `vibecomfy.cli nodes verify --lockfile custom_nodes.lock` as a cheap read-only node-schema validation probe on every prebuilt run, regardless of lockfile drift. Destructive `nodes restore` remains gated on `custom_nodes_lock_hash` drift."
    },
    {
      "id": "correctness-1",
      "resolution": "addressed",
      "reason": "Step 1.1 default paths corrected: runtime_worker_path=/opt/reigh-livetest-prebuilt/worker, runtime_vibecomfy_path=/opt/reigh-livetest-prebuilt/vibecomfy. /workspace stays as the network-volume mountpoint per config.py:114. /opt/ is the established container-disk convention (existing /opt/reigh-worker-live-test-venv)."
    },
    {
      "id": "correctness-2",
      "resolution": "addressed",
      "reason": "Step 6.3 bundle_artifacts produces TWO bundles: venv.cuda124.tar.zst and vibecomfy.tar.zst. No comfyui.tar.zst. Step 8.3 has no extract_comfyui_bundle phase. ComfyUI is acknowledged as pip-installed inside the venv (ssh_bootstrap.py:225-227) and therefore covered by the venv bundle. Manifest schema (Step 1.1) has no comfyui_bundle_sha256 field."
    },
    {
      "id": "correctness-3",
      "resolution": "addressed",
      "reason": "Step 7 corrected: volume name suffix is `dataCenterId` (e.g. eu-no-1) from get_network_volumes(api_key), not a derivation from RUNPOD_STORAGE_VOLUMES (which contains volume NAMES like 'Peter'). Consumer enumerates volumes by prefix at runtime and selects by dataCenterId. config.py exposes PREBUILT_VOLUME_NAME_PREFIX and prebuilt_name_for_profile(profile, data_center_id) helper."
    },
    {
      "id": "correctness-4",
      "resolution": "addressed",
      "reason": "Step 7.3 and Step 8.2 explicitly state find_gpu_type has no region filter (per api.py:83-97). The plan no longer uses 'if possible' language. Pod-create with the attached volume's dataCenterId is the actual region enforcement mechanism; if the GPU is in a different region the RunPod API returns an error, which we surface verbatim with a `rl prebuilt list` hint."
    },
    {
      "id": "correctness-5",
      "resolution": "addressed",
      "reason": "Step 2.4 specifies every probe in verify_extracted_env runs via _execute(ssh, cmd, check=False) so non-zero exit codes NEVER raise inside the probe; instead the function captures stderr (first/last 50 lines) and emits a diagnostic string. The probe function returns a list[str] of issues, not a raised exception."
    },
    {
      "id": "correctness-6",
      "resolution": "addressed",
      "reason": "Step 6.4 creates new module runpod-lifecycle/src/runpod_lifecycle/guard.py with prune_pods_by_prefix(prefixes, api_key, ...). reigh-worker/scripts/live_test/terminate_guard.py imports this and delegates (Step 10.3). runpod-lifecycle has NO dependency on reigh-worker \u2014 the import direction is one-way (reigh-worker \u2192 runpod-lifecycle). No fallback branch."
    },
    {
      "id": "correctness-7",
      "resolution": "addressed",
      "reason": "Step 4.1 build_run_worker_command signature adds python_version: str = '3.10' kwarg; Step 4.3 edits launch_command.py:43-44 to use it. Step 8.3 launch_worker phase passes python_version=contract.python_version. Manifest's python_version field is now end-to-end enforced \u2014 the python_version hard-fail invalidation rule (Step 1.2) is meaningful because launch reads the same value."
    },
    {
      "id": "scope-1",
      "resolution": "addressed",
      "reason": "Step 5.2 explicitly renames _register_fresh_worker_record to register_worker_record(db, pod_id, pod, args, *, variant_label: str). variant_fresh passes variant_label='fresh'; variant_prebuilt passes 'prebuilt'. Both call sites enumerated. The function body uses variant_label in place of the literal FRESH_VARIANT."
    },
    {
      "id": "scope-2",
      "resolution": "addressed",
      "reason": "Step 11 adds a single-line guard at the top of variant_update.run: if /workspace/reigh-livetest-prebuilt/env.manifest.json exists, raise with the literal text 'Prebuilt cache present at /workspace/reigh-livetest-prebuilt; --variant update would mutate the cached venv at /opt/reigh-worker-live-test-venv. Use --variant prebuilt instead, or run `rl prebuilt invalidate --volume-name X` first.' No other variant_update changes. Step 12.6 has a test for this guard."
    },
    {
      "id": "scope-3",
      "resolution": "addressed",
      "reason": "Step 8.3 bind_models_dir phase now adds HF_HOME, HF_HUB_CACHE, and the ComfyUI models-path env to the worker_env dict (the same dict passed to export_env and consumed by launch_worker_detached). Step 8.4 documents the new _build_worker_env wrapper in variant_prebuilt.py. Step 12.5 has a test verifying these keys are present in the dict, not just exported in the SSH bootstrap shell."
    },
    {
      "id": "all_locations-1",
      "resolution": "addressed",
      "reason": "Overview enumerates `reigh-worker/scripts/live_test/launch_command.py:37, 43-44` as a touched location (both UV_PROJECT_ENVIRONMENT and --python literals). Step 4.3 explicitly edits line 43-44 to use the new python_version kwarg."
    },
    {
      "id": "all_locations-2",
      "resolution": "addressed",
      "reason": "Step 10.2 replaces the single _FRESH_POD_NAME_RE with a tuple of three compiled patterns, one per prefix, all using the shared timestamp suffix %Y%m%dT%H%M%SZ. Step 6.3 specifies builder pods use that suffix; Step 8.2 specifies prebuilt consumer pods use it. Step 12.7 has a regex test verifying each of the three prefixes matches a sample pod name."
    },
    {
      "id": "all_locations-3",
      "resolution": "addressed",
      "reason": "Step 5.3 adds backward-compatible re-exports at the top of variant_fresh.py: _phase = _shared._phase, _redact_sensitive_text = _shared._redact_sensitive_text, _capture_and_redact_noisy_lifecycle_output = _shared._capture_and_redact_noisy_lifecycle_output. Existing tests that import these from variant_fresh keep resolving. Step 12.9 tests that the old import paths still work."
    },
    {
      "id": "all_locations-4",
      "resolution": "addressed",
      "reason": "Step 7.4 explicitly updates config.py:__all__ (currently lines 173-203) to include PREBUILT_VOLUME_NAME_PREFIX, PREBUILT_CACHE_ROOT, PREBUILT_RUNTIME_VENV_PATH, PREBUILT_RUNTIME_WORKER_PATH, PREBUILT_RUNTIME_VIBECOMFY_PATH, and prebuilt_name_for_profile."
    },
    {
      "id": "callers-1",
      "resolution": "addressed",
      "reason": "Step 4.4 explicitly says variant_fresh.py:304-312 (the dry-run path) omits the new kwargs (keeps defaults). Step 4.5 says variant_prebuilt.py adds a corresponding _print_dry_run_plan that passes venv_path=contract.runtime_venv_path and python_version=contract.python_version. Dry-run output for the prebuilt variant therefore shows the prebuilt paths, not the fresh defaults. Step 12.8 tests this."
    },
    {
      "id": "callers-2",
      "resolution": "addressed",
      "reason": "Step 8.3 explicitly reorders the bootstrap phases so verify_extracted_env runs AFTER sync_worker_ref and sync_vibecomfy_ref, not before. Step 12.4 includes a phase-order assertion test capturing the command sequence."
    },
    {
      "id": "callers-3",
      "resolution": "addressed",
      "reason": "Step 9.3 explicitly confirms that the existing shared flags --backend, --worker-profile, --selector-namespace, --selector-version, --worker-contract-version continue to be parsed for ALL variants (including prebuilt) via shared argparse subparser inheritance. register_worker_record's args.backend / args.worker_profile / args.selector_namespace reads therefore work for the prebuilt variant with no flag-renaming."
    },
    {
      "id": "FLAG-009",
      "resolution": "addressed",
      "reason": "Same as correctness-1 \u2014 paths now /opt/reigh-livetest-prebuilt/{worker,vibecomfy} (container disk), consistent with existing /opt/reigh-worker-live-test-venv. /workspace stays the network volume mount."
    },
    {
      "id": "FLAG-010",
      "resolution": "addressed",
      "reason": "Same as correctness-7 \u2014 build_run_worker_command now takes python_version; launch_command.py:43-44 reads it; variant_prebuilt passes contract.python_version from the manifest. End-to-end python_version invariant is now enforceable."
    },
    {
      "id": "FLAG-014",
      "resolution": "addressed",
      "reason": "Same as scope-3 \u2014 HF_HOME, HF_HUB_CACHE, and the ComfyUI models path env var are now added to worker_env (the dict consumed by export_env and launch_worker_detached). The worker subprocess inherits them. Step 12.5 verifies via test."
    }
  ],
  "questions": [
    "Should `rl prebuilt warm-models <recipe>` ship in v1, or stay deferred to v2? Current plan defers; first-run model cold-download is accepted v1 scope. If v1 is preferred, scope grows by ~1 day to add a warm-models verb that pre-downloads HF weights for a named workflow subset.",
    "ComfyUI fork's models-path env var: the actual variable name (or whether extra_model_paths.yaml is the only way) needs a quick read of vibecomfy/ComfyUI's loader. Want me to confirm during implementation, or do you already know the right env var?",
    "Does the `vibecomfy.cli nodes verify` subcommand (used as the cheap node-schema validation probe in Step 2.4(d) and Step 8.3) already exist? If not, this plan adds a trivial read-only addition; if it does exist under a different name, we use that.",
    "Step 7.5 carries forward the rev 2 open question on whether `rl prebuilt inspect` should be allowed to reuse an existing consumer pod's SSH rather than provisioning a probe pod. v1 provisions-and-terminates for simplicity; let me know if you want the --pod escape hatch."
  ],
  "success_criteria": [
    {
      "criterion": "runpod_lifecycle/prebuilt.py exists exporting PrebuiltEnvContract, PrebuiltManifest (with schema_version, bundle_format_version, python_version, cuda_extra, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes fields; NO comfyui_bundle_sha256 field), compute_pyproject_hash, compute_lockfile_hash, read_manifest, write_manifest, acquire_build_lock, verify_extracted_env",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "runpod_lifecycle/guard.py exists exporting prune_pods_by_prefix(prefixes, api_key, ...); runpod-lifecycle has no import dependency on reigh-worker",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "ssh_bootstrap.run_install and clone_and_install_vibecomfy produce byte-identical shell commands (modulo whitespace normalization) compared to pre-refactor, verified by golden-string unit tests",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "build_run_worker_command accepts venv_path AND python_version keyword arguments; defaults are /opt/reigh-worker-live-test-venv and 3.10; passing alternative values emits the corresponding UV_PROJECT_ENVIRONMENT export and --python flag",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "test_primitives.py assertions at lines 870, 2317-2319, 2445 are updated to verify the parameterized venv_path / python_version mechanism (not just literals) and still pass",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "_shared.py exists with _phase, _capture_and_redact_noisy_lifecycle_output, _redact_sensitive_text, _runs_root, _timestamp_label, _resolve_runpod_gpu_type_id, select_network_volume, and register_worker_record(..., variant_label: str); variant_fresh.py imports from _shared AND retains backward-compatible re-exports for tests",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "register_worker_record (renamed from _register_fresh_worker_record) is called by variant_fresh with variant_label='fresh' and by variant_prebuilt with variant_label='prebuilt'; both pass args containing backend, worker_profile, selector_namespace, selector_version, worker_contract_version",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Unit tests cover: schema_version drift returns hard_fail, bundle_format_version drift returns hard_fail, python_version drift returns hard_fail, cuda_extra drift returns hard_fail; pyproject_hash / custom_nodes_lock_hash / comfyui_pin / vibecomfy_commit / reigh_worker_commit drift each return delta_sync; lockfile O_EXCL acquire/release + TTL takeover",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Harness tests for variant_prebuilt cover: manifest match \u2192 zero install commands; pyproject_hash drift \u2192 _uv_sync_shell(extras=(cuda124,)) issued; custom_nodes_lock_hash drift \u2192 nodes restore issued; vibecomfy_commit only drift \u2192 git checkout + pip install -e but NO nodes restore; python_version drift \u2192 RuntimeError with `rl prebuilt build` text and NO extract/sync; schema_version drift \u2192 RuntimeError with `rl prebuilt build` text and NO extract/sync; missing manifest \u2192 RuntimeError containing literal `rl prebuilt build --volume-name`",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Phase-order test: in the success path, verify_extracted_env is invoked AFTER sync_worker_ref and sync_vibecomfy_ref (captured command sequence assertion)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "_uv_sync_shell raises ValueError when extras is empty; default extras is (cuda124,)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "live_test --variant prebuilt --dry-run and --variant auto --dry-run run to completion without RunPod credentials; auto falls back to fresh when select_network_volume returns None and picks prebuilt when a volume is reported; dry-run output for variant_prebuilt shows runtime_venv_path and python_version from the contract, NOT the fresh defaults",
      "priority": "must",
      "requires": [
        "run_shell",
        "run_tests"
      ]
    },
    {
      "criterion": "rl prebuilt {build,inspect,invalidate,list} subcommands exist with argparse help text; build requires --data-center and --volume-name and accepts --python-version; invalidate preserves models/ tree and build.lock",
      "priority": "must",
      "requires": [
        "run_shell"
      ]
    },
    {
      "criterion": "terminate_guard exposes LIVE_TEST_POD_PREFIXES = ('reigh-live-test-fresh-', 'reigh-livetest-prebuilt-', 'reigh-livetest-builder-') and a tuple of three compiled regex patterns each matching {prefix}{timestamp} with the shared %Y%m%dT%H%M%SZ format; prune_stale_live_test_pods delegates to runpod_lifecycle.guard.prune_pods_by_prefix",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "variant_prebuilt consumer pod uses prefix reigh-livetest-prebuilt-; builder pod uses prefix reigh-livetest-builder-; both use the shared %Y%m%dT%H%M%SZ timestamp suffix",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "verify_extracted_env runs each probe with check=False, captures stderr, returns a list[str] of diagnostic strings (never raises from a probe); always includes the node-schema verify probe (vibecomfy.cli nodes verify) regardless of lockfile drift; consumer raises with rl prebuilt invalidate/build text when issues are non-empty",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "variant_prebuilt._build_worker_env returns a dict containing HF_HOME, HF_HUB_CACHE, and a ComfyUI models-path key (e.g. COMFYUI_EXTRA_MODEL_PATHS); these are present in the worker_env dict passed to export_env and inherited by the launched worker subprocess",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Container-disk floor: variant_prebuilt rejects --container-disk-gb < 100 and defaults to 200; rl prebuilt build defaults to 200 GB container disk and rejects values < 100",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Volume name derivation: prebuilt_name_for_profile(profile, data_center_id) returns the lowercased dataCenterId as the suffix (not derived from RUNPOD_STORAGE_VOLUMES name tuple); consumer enumerates get_network_volumes by prefix at runtime",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "config.py:__all__ exports PREBUILT_VOLUME_NAME_PREFIX, PREBUILT_CACHE_ROOT, PREBUILT_RUNTIME_VENV_PATH, PREBUILT_RUNTIME_WORKER_PATH, PREBUILT_RUNTIME_VIBECOMFY_PATH, prebuilt_name_for_profile",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "build.lock with O_EXCL and TTL takeover prevents concurrent corrupt builds; a second concurrent prebuilt build call fails with a recorded holder id and acquisition timestamp",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "variant_update.run raises RuntimeError with literal substring 'Prebuilt cache present' when the prebuilt manifest exists on the volume; this is the only change to variant_update.py and is tested with a fake SSH",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Backward-compatible re-exports: tests that import _phase / _redact_sensitive_text / _capture_and_redact_noisy_lifecycle_output from variant_fresh continue to resolve them",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "--variant argparse default REMAINS 'fresh' (NOT flipped to 'auto'); --variant auto is opt-in; auto path logs structured prebuilt_unavailable event when no volume is found",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Atomic rename via staging_path: a builder crash mid-bundle leaves the existing manifest + bundles untouched (verified by unit test simulating a crash before final mv)",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Phase-level structured logs emitted in the consumer: attach_prebuilt_volume, read_prebuilt_manifest, check_hard_fail_drift, extract_venv_bundle, extract_vibecomfy_bundle, sync_worker_ref, sync_vibecomfy_ref, verify_extracted_env, bind_models_dir, launch_worker (in that order)",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "docs/migration-vibecomfy-live-validation.md contains a Prebuilt validation environment section covering bundle architecture (extract-to-/opt/), hard-fail vs delta-sync rules, region-pinned volume naming + auto-selection by dataCenterId, model-cache layout with first-run cold-download caveat, partial-state diagnostics, concurrent-builder lock, variant_update coexistence guard, --variant auto opt-in",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "reigh-worker/.claude/skills/live-test/SKILL.md is committed and recommends --variant auto as the default invocation for future agents; vibecomfy/CLAUDE.md has a one-line pointer to the skill",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Existing variant_fresh and variant_update test suites still pass after the ssh_bootstrap, launch_command, and _shared refactors",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "One real RunPod live-test run on the prebuilt path reaches launch_worker in under 10 minutes from pod-create (vs ~67 min cold), captured in scripts/live_test/runs/{timestamp}/prebuilt-validation.md",
      "priority": "info",
      "requires": [
        "observe_runtime_logs",
        "verify_physical_device"
      ]
    },
    {
      "criterion": "A second RunPod run within 5 minutes of the first reuses the models/ cache (no HuggingFace download log lines for the workflow's model weights). Note: this depends on the first run having downloaded the relevant weights into models/; first-encounter cold downloads are accepted v1 scope.",
      "priority": "info",
      "requires": [
        "observe_runtime_logs",
        "verify_physical_device"
      ]
    },
    {
      "criterion": "Post-validation, RunPod pod list shows only the consumer prebuilt pod was terminated; the builder pod is already gone; the prebuilt volume persists",
      "priority": "info",
      "requires": [
        "observe_runtime_logs",
        "verify_physical_device"
      ]
    },
    {
      "criterion": "No new lint/type errors introduced in changed files",
      "priority": "should",
      "requires": [
        "run_linter"
      ]
    },
    {
      "criterion": "variant_update.py diff is limited to the new prebuilt-manifest coexistence guard (one or two new lines at the top of run() and any necessary import)",
      "priority": "should",
      "requires": [
        "parse_diff"
      ]
    }
  ],
  "assumptions": [
    "The runpod base pytorch image (config.py:91 = py3.11-cuda12.4.1) provides 200+ GB of container-local disk so the extracted venv (~15-25 GB) plus the two checkouts (~1 GB combined) fit comfortably under /opt/ alongside runtime outputs.",
    "MooseFS sequential read throughput is acceptable for streaming a multi-GB tar.zst from the volume to container disk. Validated empirically in Step 13; if intolerable we'd revisit on a follow-up, not in this plan.",
    "RunPod network volumes are region-pinned by `dataCenterId`. Multi-region rollout requires one build per region. v1 ships one region; auto-detect enumerates by prefix at runtime.",
    "variant_update.py stays untouched except for the new single-line coexistence guard (Step 11). No coupling to prebuilt beyond the guard.",
    "Concurrent builders are rare; one O_EXCL lockfile + TTL takeover suffices. No distributed coordination needed.",
    "Model warming is v2 scope. v1 first-run model cold-download is accepted; the materially-faster claim covers deps (67 min \u2192 ~10 min) and steady-state model reuse via HF_HOME. Future `rl prebuilt warm-models` will pre-populate weights.",
    "argparse default for --variant stays `fresh` (not flipped to `auto`). Skill + docs recommend `--variant auto` but no script behavior changes silently. A future default flip is a separate migration.",
    "The ComfyUI fork's models-path env var: best-effort detection at implementation time by reading vibecomfy's loader; fallback is writing extra_model_paths.yaml at runtime_vibecomfy_path. Either is sufficient.",
    "The cheap `vibecomfy.cli nodes verify` subcommand either already exists or is a trivial read-only addition; if it does not exist, the partial-state probe uses `test -f template_index.json` plus a lighter sanity check (template count > 0).",
    "Backward-compatible re-exports of moved symbols (Step 5.3) keep test imports stable; no test file paths need refactoring.",
    "The runpod-lifecycle CLI uses argparse subparsers (validated by reading cli.py in Step 6.1). If a different framework, Step 6.1 adapts.",
    "test_primitives.py line numbers cited (870, 2317-2319, 2445) may shift slightly between revisions; the literal `/opt/reigh-worker-live-test-venv` string is the marker."
  ],
  "delta_from_previous_percent": 84.59,
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 34,
    "items": [
      {
        "criterion": "runpod_lifecycle/prebuilt.py exists exporting PrebuiltEnvContract, PrebuiltManifest (with schema_version, bundle_format_version, python_version, cuda_extra, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes fields; NO comfyui_bundle_sha256 field), compute_pyproject_hash, compute_lockfile_hash, read_manifest, write_manifest, acquire_build_lock, verify_extracted_env",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "runpod_lifecycle/guard.py exists exporting prune_pods_by_prefix(prefixes, api_key, ...); runpod-lifecycle has no import dependency on reigh-worker",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "ssh_bootstrap.run_install and clone_and_install_vibecomfy produce byte-identical shell commands (modulo whitespace normalization) compared to pre-refactor, verified by golden-string unit tests",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "build_run_worker_command accepts venv_path AND python_version keyword arguments; defaults are /opt/reigh-worker-live-test-venv and 3.10; passing alternative values emits the corresponding UV_PROJECT_ENVIRONMENT export and --python flag",
        "priority": "must",
        "requires": [
          "run_tests",
          "read_files"
        ]
      },
      {
        "criterion": "test_primitives.py assertions at lines 870, 2317-2319, 2445 are updated to verify the parameterized venv_path / python_version mechanism (not just literals) and still pass",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "_shared.py exists with _phase, _capture_and_redact_noisy_lifecycle_output, _redact_sensitive_text, _runs_root, _timestamp_label, _resolve_runpod_gpu_type_id, select_network_volume, and register_worker_record(..., variant_label: str); variant_fresh.py imports from _shared AND retains backward-compatible re-exports for tests",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "register_worker_record (renamed from _register_fresh_worker_record) is called by variant_fresh with variant_label='fresh' and by variant_prebuilt with variant_label='prebuilt'; both pass args containing backend, worker_profile, selector_namespace, selector_version, worker_contract_version",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Unit tests cover: schema_version drift returns hard_fail, bundle_format_version drift returns hard_fail, python_version drift returns hard_fail, cuda_extra drift returns hard_fail; pyproject_hash / custom_nodes_lock_hash / comfyui_pin / vibecomfy_commit / reigh_worker_commit drift each return delta_sync; lockfile O_EXCL acquire/release + TTL takeover",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Harness tests for variant_prebuilt cover: manifest match \u2192 zero install commands; pyproject_hash drift \u2192 _uv_sync_shell(extras=(cuda124,)) issued; custom_nodes_lock_hash drift \u2192 nodes restore issued; vibecomfy_commit only drift \u2192 git checkout + pip install -e but NO nodes restore; python_version drift \u2192 RuntimeError with `rl prebuilt build` text and NO extract/sync; schema_version drift \u2192 RuntimeError with `rl prebuilt build` text and NO extract/sync; missing manifest \u2192 RuntimeError containing literal `rl prebuilt build --volume-name`",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Phase-order test: in the success path, verify_extracted_env is invoked AFTER sync_worker_ref and sync_vibecomfy_ref (captured command sequence assertion)",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "_uv_sync_shell raises ValueError when extras is empty; default extras is (cuda124,)",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "live_test --variant prebuilt --dry-run and --variant auto --dry-run run to completion without RunPod credentials; auto falls back to fresh when select_network_volume returns None and picks prebuilt when a volume is reported; dry-run output for variant_prebuilt shows runtime_venv_path and python_version from the contract, NOT the fresh defaults",
        "priority": "must",
        "requires": [
          "run_shell",
          "run_tests"
        ]
      },
      {
        "criterion": "rl prebuilt {build,inspect,invalidate,list} subcommands exist with argparse help text; build requires --data-center and --volume-name and accepts --python-version; invalidate preserves models/ tree and build.lock",
        "priority": "must",
        "requires": [
          "run_shell"
        ]
      },
      {
        "criterion": "terminate_guard exposes LIVE_TEST_POD_PREFIXES = ('reigh-live-test-fresh-', 'reigh-livetest-prebuilt-', 'reigh-livetest-builder-') and a tuple of three compiled regex patterns each matching {prefix}{timestamp} with the shared %Y%m%dT%H%M%SZ format; prune_stale_live_test_pods delegates to runpod_lifecycle.guard.prune_pods_by_prefix",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "variant_prebuilt consumer pod uses prefix reigh-livetest-prebuilt-; builder pod uses prefix reigh-livetest-builder-; both use the shared %Y%m%dT%H%M%SZ timestamp suffix",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "verify_extracted_env runs each probe with check=False, captures stderr, returns a list[str] of diagnostic strings (never raises from a probe); always includes the node-schema verify probe (vibecomfy.cli nodes verify) regardless of lockfile drift; consumer raises with rl prebuilt invalidate/build text when issues are non-empty",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "variant_prebuilt._build_worker_env returns a dict containing HF_HOME, HF_HUB_CACHE, and a ComfyUI models-path key (e.g. COMFYUI_EXTRA_MODEL_PATHS); these are present in the worker_env dict passed to export_env and inherited by the launched worker subprocess",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Container-disk floor: variant_prebuilt rejects --container-disk-gb < 100 and defaults to 200; rl prebuilt build defaults to 200 GB container disk and rejects values < 100",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Volume name derivation: prebuilt_name_for_profile(profile, data_center_id) returns the lowercased dataCenterId as the suffix (not derived from RUNPOD_STORAGE_VOLUMES name tuple); consumer enumerates get_network_volumes by prefix at runtime",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "config.py:__all__ exports PREBUILT_VOLUME_NAME_PREFIX, PREBUILT_CACHE_ROOT, PREBUILT_RUNTIME_VENV_PATH, PREBUILT_RUNTIME_WORKER_PATH, PREBUILT_RUNTIME_VIBECOMFY_PATH, prebuilt_name_for_profile",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "build.lock with O_EXCL and TTL takeover prevents concurrent corrupt builds; a second concurrent prebuilt build call fails with a recorded holder id and acquisition timestamp",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "variant_update.run raises RuntimeError with literal substring 'Prebuilt cache present' when the prebuilt manifest exists on the volume; this is the only change to variant_update.py and is tested with a fake SSH",
        "priority": "must",
        "requires": [
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Backward-compatible re-exports: tests that import _phase / _redact_sensitive_text / _capture_and_redact_noisy_lifecycle_output from variant_fresh continue to resolve them",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "--variant argparse default REMAINS 'fresh' (NOT flipped to 'auto'); --variant auto is opt-in; auto path logs structured prebuilt_unavailable event when no volume is found",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Atomic rename via staging_path: a builder crash mid-bundle leaves the existing manifest + bundles untouched (verified by unit test simulating a crash before final mv)",
        "priority": "should",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Phase-level structured logs emitted in the consumer: attach_prebuilt_volume, read_prebuilt_manifest, check_hard_fail_drift, extract_venv_bundle, extract_vibecomfy_bundle, sync_worker_ref, sync_vibecomfy_ref, verify_extracted_env, bind_models_dir, launch_worker (in that order)",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "docs/migration-vibecomfy-live-validation.md contains a Prebuilt validation environment section covering bundle architecture (extract-to-/opt/), hard-fail vs delta-sync rules, region-pinned volume naming + auto-selection by dataCenterId, model-cache layout with first-run cold-download caveat, partial-state diagnostics, concurrent-builder lock, variant_update coexistence guard, --variant auto opt-in",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "reigh-worker/.claude/skills/live-test/SKILL.md is committed and recommends --variant auto as the default invocation for future agents; vibecomfy/CLAUDE.md has a one-line pointer to the skill",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Existing variant_fresh and variant_update test suites still pass after the ssh_bootstrap, launch_command, and _shared refactors",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "One real RunPod live-test run on the prebuilt path reaches launch_worker in under 10 minutes from pod-create (vs ~67 min cold), captured in scripts/live_test/runs/{timestamp}/prebuilt-validation.md",
        "priority": "info",
        "requires": [
          "observe_runtime_logs",
          "verify_physical_device"
        ]
      },
      {
        "criterion": "A second RunPod run within 5 minutes of the first reuses the models/ cache (no HuggingFace download log lines for the workflow's model weights). Note: this depends on the first run having downloaded the relevant weights into models/; first-encounter cold downloads are accepted v1 scope.",
        "priority": "info",
        "requires": [
          "observe_runtime_logs",
          "verify_physical_device"
        ]
      },
      {
        "criterion": "Post-validation, RunPod pod list shows only the consumer prebuilt pod was terminated; the builder pod is already gone; the prebuilt volume persists",
        "priority": "info",
        "requires": [
          "observe_runtime_logs",
          "verify_physical_device"
        ]
      },
      {
        "criterion": "No new lint/type errors introduced in changed files",
        "priority": "should",
        "requires": [
          "run_linter"
        ]
      },
      {
        "criterion": "variant_update.py diff is limited to the new prebuilt-manifest coexistence guard (one or two new lines at the top of run() and any necessary import)",
        "priority": "should",
        "requires": [
          "parse_diff"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "FLAG-008",
      "concern": "Model-cache reuse (the largest cost driver after deps) is not part of the prebuilt contract. The manifest tracks .venv and custom_nodes but does not declare or invalidate the HuggingFace / model weight cache that downloads on first workflow execution. A prebuilt env that still cold-downloads 10-50GB of weights does not meet the materially faster bar for repeat workflow runs beyond the first.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "issue_hints-1",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Model warming is explicitly deferred to v2 (assumption #6). The idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50GB HF download. The success criterion for Run B model reuse depends on Run A having performed that download. Plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Model warming is explicitly deferred to v2 (assumption #6). The idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50GB HF download. The success criterion for Run B model reuse depends on Run A having performed that download. Plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "issue_hints-2",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (Step 2.4d, Step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. The plan does not enumerate adding it to the vibecomfy repo as a planned change. If it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. Open question #3 explicitly defers verifying its existence.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (Step 2.4d, Step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. The plan does not enumerate adding it to the vibecomfy repo as a planned change. If it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. Open question #3 explicitly defers verifying its existence.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "issue_hints-3",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Discovery-by-default: rev 2's silent dispatch flip was reverted (Step 9.1 keeps argparse default `fresh`). Skill + docs recommend `--variant auto`. Future agents reading docs will see the recommendation, but agents that invoke `--variant fresh` from existing scripts still pay the 67-min cost. This is the correct tradeoff for backward compat, but worth recording that 'used by default' is now a recommendation, not an enforced default.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Discovery-by-default: rev 2's silent dispatch flip was reverted (Step 9.1 keeps argparse default `fresh`). Skill + docs recommend `--variant auto`. Future agents reading docs will see the recommendation, but agents that invoke `--variant fresh` from existing scripts still pay the 67-min cost. This is the correct tradeoff for backward compat, but worth recording that 'used by default' is now a recommendation, not an enforced default.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-1",
      "concern": "Are the proposed changes technically correct?: Step 6.4 says 'New module runpod-lifecycle/src/runpod_lifecycle/guard.py'. That module ALREADY EXISTS (127 lines) and houses `PodGuard` (re-exported from __init__.py:15 as `PodGuard, install_signal_handlers`). The plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. As worded an executor could create a duplicate file or overwrite the existing PodGuard.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 6.4 says 'New module runpod-lifecycle/src/runpod_lifecycle/guard.py'. That module ALREADY EXISTS (127 lines) and houses `PodGuard` (re-exported from __init__.py:15 as `PodGuard, install_signal_handlers`). The plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. As worded an executor could create a duplicate file or overwrite the existing PodGuard.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-2",
      "concern": "Are the proposed changes technically correct?: Step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. But there is NO worker bundle: Step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. On first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. The plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. This works functionally (git clone is cheap) but the description is misleading.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. But there is NO worker bundle: Step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. On first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. The plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. This works functionally (git clone is cheap) but the description is misleading.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-3",
      "concern": "Are the proposed changes technically correct?: Step 4.1 keeps the default `python_version='3.10'` in `build_run_worker_command` for backward compat. The current `--python 3.10` in launch_command.py:43-44 works because `uv run --python 3.10` makes uv download/manage Python 3.10 itself (the runpod base image is py3.11). When the prebuilt path uses `python_version='3.11'` matching the base image, no uv-managed download is needed; when fresh continues with 3.10, uv-managed download is needed. The two paths diverge in interpreter source. Not new (existing behavior), but the plan does not call out that the prebuilt path is effectively a different interpreter than the fresh path.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 4.1 keeps the default `python_version='3.10'` in `build_run_worker_command` for backward compat. The current `--python 3.10` in launch_command.py:43-44 works because `uv run --python 3.10` makes uv download/manage Python 3.10 itself (the runpod base image is py3.11). When the prebuilt path uses `python_version='3.11'` matching the base image, no uv-managed download is needed; when fresh continues with 3.10, uv-managed download is needed. The two paths diverge in interpreter source. Not new (existing behavior), but the plan does not call out that the prebuilt path is effectively a different interpreter than the fresh path.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-4",
      "concern": "Are the proposed changes technically correct?: Step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. The extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. The plan does not specify clobber vs merge semantics. A baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. The extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. The plan does not specify clobber vs merge semantics. A baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-5",
      "concern": "Are the proposed changes technically correct?: Step 6.3 builder install_worker invokes `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`. The builder pod is provisioned with `--container-disk-gb=200`. The venv install plus comfyui pip install plus uv cache fits, but bundling adds another ~10-25GB temporary tar.zst at `{staging_path}` on the network volume before atomic mv to `{cache_root}`. Plan does not address whether the staging directory write to MooseFS during the multi-GB tar+zstd stream is performant enough that the builder doesn't time out. No timeout/throughput target is set.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 6.3 builder install_worker invokes `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`. The builder pod is provisioned with `--container-disk-gb=200`. The venv install plus comfyui pip install plus uv cache fits, but bundling adds another ~10-25GB temporary tar.zst at `{staging_path}` on the network volume before atomic mv to `{cache_root}`. Plan does not address whether the staging directory write to MooseFS during the multi-GB tar+zstd stream is performant enough that the builder doesn't time out. No timeout/throughput target is set.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-6",
      "concern": "Are the proposed changes technically correct?: Step 6.5 fallback for cross-repo imports: 'if runpod-lifecycle cannot import reigh-worker code, replicate the helper as runpod_lifecycle.guard.prune_pods_by_prefix(prefixes, ...) and have terminate_guard.py delegate to it'. runpod-lifecycle is a standalone package with no reigh-worker dependency \u2014 the import direction is reigh-worker \u2192 runpod-lifecycle, not the reverse. The replicate-helper fallback is the only correct option; the import-from-reigh-worker primary branch is wrong by repo structure.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. But variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). The spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. This is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. But variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). The spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. This is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 7.1 says builds are 'one per region they want covered' but offers no story for promoting a single-region build to multi-region. Operators in different regions must run the full ~67-min builder pipeline independently, with no shared state. Not a correctness issue but a notable operational ceiling \u2014 at 4 regions in RUNPOD_STORAGE_VOLUMES, that's 4\u00d7 builder cost on each schema_version / python_version / cuda_extra bump.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step 7.1 says builds are 'one per region they want covered' but offers no story for promoting a single-region build to multi-region. Operators in different regions must run the full ~67-min builder pipeline independently, with no shared state. Not a correctness issue but a notable operational ceiling \u2014 at 4 regions in RUNPOD_STORAGE_VOLUMES, that's 4\u00d7 builder cost on each schema_version / python_version / cuda_extra bump.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope-3",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: verify_extracted_env (Step 2.4) returns `list[str]`, but Step 8.3 says the consumer raises when issues are non-empty. Plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. The diagnostic UX matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, AND node-schema verify fail \u2014 operator should see all three reasons, not just one).",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "verify_extracted_env (Step 2.4) returns `list[str]`, but Step 8.3 says the consumer raises when issues are non-empty. Plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. The diagnostic UX matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, AND node-schema verify fail \u2014 operator should see all three reasons, not just one).",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "all_locations-1",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. Should be marked as 'extend existing'. The associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. Minor but enumerated.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. Should be marked as 'extend existing'. The associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. Minor but enumerated.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "all_locations-2",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. But `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is NOT in the Step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). The plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. Without that, variant_prebuilt's HF_HOME-extending wrapper has nothing to wrap.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. But `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is NOT in the Step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). The plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. Without that, variant_prebuilt's HF_HOME-extending wrapper has nothing to wrap.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "all_locations-3",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. The actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%Y%m%dT%H%M%SZ'` (uppercase T, Z), and existing _FRESH_POD_NAME_RE at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). The plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. The actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%Y%m%dT%H%M%SZ'` (uppercase T, Z), and existing _FRESH_POD_NAME_RE at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). The plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "all_locations-4",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in Step 7.2 actually lives where? Plan says config.py exposes the helper. That mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). Placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. Minor consistency concern.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in Step 7.2 actually lives where? Plan says config.py exposes the helper. That mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). Placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. Minor consistency concern.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "callers-1",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. Step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). The plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. If it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. Step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). The plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. If it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "callers-2",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `_uv_sync_shell` (new in Step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=False`). variant_update.py:69-79 has a separate `REMOTE_UV_SYNC` that uses `--locked`. Plan does not migrate variant_update's REMOTE_UV_SYNC to call `_uv_sync_shell(..., with_locked=True)` \u2014 variant_update stays untouched per assumption #4. So the new `with_locked` parameter has no caller. Minor but adds unused API surface.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Callers of `_uv_sync_shell` (new in Step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=False`). variant_update.py:69-79 has a separate `REMOTE_UV_SYNC` that uses `--locked`. Plan does not migrate variant_update's REMOTE_UV_SYNC to call `_uv_sync_shell(..., with_locked=True)` \u2014 variant_update stays untouched per assumption #4. So the new `with_locked` parameter has no caller. Minor but adds unused API surface.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "callers-3",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `extract_bundle_to_container_disk` (new in Step 3.3): only variant_prebuilt invokes it. The target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). Plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). Default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. Probably correct as-is for the ephemeral pod use case.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Callers of `extract_bundle_to_container_disk` (new in Step 3.3): only variant_prebuilt invokes it. The target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). Plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). Default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. Probably correct as-is for the ephemeral pod use case.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "correctness-7",
      "concern": "Are the proposed changes technically correct?: Step 4 parameterizes `build_run_worker_command` to take `venv_path`. The hardcoded `--python 3.10` at launch_command.py:43-44 is NOT parameterized. If the prebuilt manifest's python_version is 3.11 (the runpod base image at config.py:91 is `py3.11-cuda12.4.1`), the worker is launched with a 3.10 uv interpreter while the prebuilt venv was created for 3.11. This is the same class of mismatch the python_version invalidation rule is supposed to catch but does not, because launch_command never reads the manifest python_version.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "FLAG-018",
      "concern": "Step 6.4 says 'new module runpod-lifecycle/src/runpod_lifecycle/guard.py', but that file ALREADY EXISTS (127 lines) and exports `PodGuard` + `install_signal_handlers` (re-exported from __init__.py:15). The plan must EXTEND the existing module rather than create a new one; ambiguous wording could cause an executor to overwrite PodGuard.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "runpod-lifecycle/src/runpod_lifecycle/guard.py:1-127 already defines class PodGuard; runpod-lifecycle/src/runpod_lifecycle/__init__.py:15 re-exports `PodGuard, install_signal_handlers` from .guard.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ],
  "recommendation": "PROCEED",
  "rationale": "Iteration 3 with score trending down (34 \u2192 40 \u2192 35.5) and the remaining 22 significant flags are overwhelmingly minor enumeration/wording gaps and accepted product tradeoffs \u2014 not architectural defects. The plan's seven settled architectural decisions (ARCH-001 through ARCH-007) are stable across all iterations; 16 flags have now been resolved. The plan correctly addressed every concrete correctness defect from v2 (paths corrected to /opt/, comfyui bundle dropped, --python parameterized, HF_HOME threaded into _build_worker_env, region derivation from dataCenterId, find_gpu_type wording dropped, verify-after-sync order, crash-resistant probes, cross-repo import direction fixed, register_worker_record rename committed, variant_update guard added, regex tuple enumerated, default stays `fresh`). The remaining flags split into three categories: (a) wording risks that an executor reading existing files will naturally handle (FLAG-018/correctness-1 \"new module guard.py\" vs existing \u2014 the executor will read the file before editing and the plan's settled-decisions table now records \"extend, don't create\"); (b) cosmetic UX nits (scope-1 message wording, scope-3 multi-issue concatenation, all_locations-4 helper location); (c) accepted product tradeoffs the user has been told about via assumptions and open questions (model warming deferred to v2, discovery-by-default kept as docs recommendation, multi-region build cost ceiling, vibecomfy CLI subcommand existence). The iteration-pressure analysis shows reopened_count=0 across all 45 fuzzy groups \u2014 none of the concerns have been addressed and then re-raised. While five groups span \u22652 iterations with \u22652 member flags (the TIEBREAKER threshold), each is either a product decision the plan has explicitly recorded as accepted (FG-001 default flip, FG-008 model warming) or a persistent minor-nit class (FG-002 wording about worker bundle starting point, FG-003 multi-issue message join, FG-004 __all__ placement, FG-005 tar overwrite semantics) \u2014 not unresolvable architectural tensions requiring human arbitration. A fourth iteration would produce another ~20 fresh minor flags as critics find new corners; the marginal value of further revision is below the cost. Time to execute.",
  "signals_assessment": "Score 34 \u2192 40 \u2192 35.5 across three iterations with 91% / 85% plan deltas; trajectory is now downward and the remaining defects are mostly enumeration/wording. 16 flags resolved cumulatively (FLAG-001/002/003/004/005/006/007/009/010/011/012/013/014/015/016/017). All 45 fuzzy groups in iteration-pressure analysis show reopened_count=0 \u2014 no churn loop. Five groups span \u22652 iterations \u00d7 \u22652 flags, but each is either a recorded product tradeoff (model warming, default flip) or a minor-nit class, not an architectural deadlock. Preflight clean. Debt-overlap warns the `are-the-proposed-changes-technically-correct` subsystem is escalated (9 occurrences across 6 prior plans) but the remaining correctness-tier flags here are wording and enumeration rather than the typical defect class that drives that overlap.",
  "warnings": [
    "Before implementation: Read existing `runpod-lifecycle/src/runpod_lifecycle/guard.py` first; the plan's 'new module' wording is incorrect \u2014 extend the existing file by adding `prune_pods_by_prefix` and update `__init__.py:15` to re-export it. Do NOT overwrite PodGuard.",
    "When extracting helpers in Step 5: also move `_build_worker_env` into `_shared.py` as `_build_worker_env_base`. variant_prebuilt's HF_HOME wrapper depends on this.",
    "Verify the regex case convention by reading the existing `terminate_guard._FRESH_POD_NAME_RE` and `_timestamp_label` before writing the new pattern tuple. The plan's lowercase t/z form is plausible but unverified; match whatever the existing code does (case-fold input or uppercase pattern).",
    "Run `_finalize_args` (main.py:115-132) for the prebuilt variant too \u2014 currently it normalizes `selector_namespace` for vibecomfy; skipping it for prebuilt would diverge selector resolution between fresh and prebuilt.",
    "Specify clobber semantics for `extra_model_paths.yaml`: consumer overwrites any builder-baked file at `{runtime_vibecomfy_path}/extra_model_paths.yaml` on every prebuilt bootstrap (matches the ephemeral-pod use case).",
    "Concatenate ALL `verify_extracted_env` issues into the diagnostic raise (not just the first) so operators see every failing probe.",
    "When building the cheap node-schema verify probe: if `vibecomfy.cli nodes verify` does not exist, the implementer must either add it as a small read-only subcommand (and enumerate that as a touchpoint) or fall back to a `template_index.json` count + json-parse smoke. Do not silently no-op.",
    "Builder staging-stream throughput on MooseFS is the only unbenchmarked perf assumption. If Step 13 shows tar+zstd to volume exceeds ~10 min, raise the issue rather than burying it.",
    "Model warming is v2; first-encounter workflows still cold-download. The 'materially faster' claim covers deps (67min \u2192 ~10min) and steady-state reuse, not first-encounter. Make this caveat clear in the prebuilt-validation.md artifact.",
    "Default `--variant` is `fresh`; the skill recommends `--variant auto`. Existing CI/scripts that omit `--variant` continue to pay the 67-min cost until they opt in. Track explicit operator migration to `auto` as a follow-up.",
    "If iteration 4 of any future related plan reopens >2 of these accepted-tradeoff flags as real defects after implementation, escalate to a redesign rather than another revision."
  ],
  "settled_decisions": [
    {
      "id": "ARCH-001",
      "decision": "Compressed bundles on the network volume, extracted to container-local `/opt/` on pod start; `models/` tree mounted from the volume. Two bundles only: `venv.cuda124.tar.zst` (includes ComfyUI in site-packages) and `vibecomfy.tar.zst`.",
      "rationale": "Resolves MooseFS Python-import cost while preserving branch flexibility. Stable across iterations 2 and 3."
    },
    {
      "id": "ARCH-002",
      "decision": "Hard-fail invalidation triggers (mandatory `rl prebuilt build`): schema_version, bundle_format_version, python_version, cuda_extra. Delta-syncable: pyproject_hash, custom_nodes_lock_hash, comfyui_pin, vibecomfy_commit, reigh_worker_commit.",
      "rationale": "End-to-end enforced via parameterized `python_version` in `build_run_worker_command` (closes the launch_command.py:43-44 gap)."
    },
    {
      "id": "ARCH-003",
      "decision": "Pod-name prefixes: `reigh-livetest-prebuilt-` (consumer), `reigh-livetest-builder-` (builder), `reigh-live-test-fresh-` (existing fresh). All use the `%Y%m%dT%H%M%SZ` timestamp suffix. `LIVE_TEST_POD_PREFIXES` tuple drives prune coverage via `runpod_lifecycle.guard.prune_pods_by_prefix`.",
      "rationale": "Builder pods are reaped by the same mechanism; orphan risk closed."
    },
    {
      "id": "ARCH-004",
      "decision": "variant_update.py untouched except for a single guard line refusing when the prebuilt manifest exists at `/workspace/reigh-livetest-prebuilt/env.manifest.json`. variant_update does not adopt prebuilt.",
      "rationale": "Confirmed across iterations 1\u20133."
    },
    {
      "id": "ARCH-005",
      "decision": "Build concurrency via `build.lock` (O_EXCL + holder_id + TTL takeover) and atomic staging-rename for bundle/manifest writes. Manifest is rewritten only by the builder by default; consumer can optionally rewrite under the same lock via `--update-manifest-on-sync`.",
      "rationale": "Resolves scope-1 from iteration 1."
    },
    {
      "id": "ARCH-006",
      "decision": "Shared helpers extracted into `_shared.py` BEFORE writing `variant_prebuilt.py`. `_register_fresh_worker_record` renamed to `register_worker_record(..., variant_label: str)`. `_build_worker_env` ALSO extracted as `_build_worker_env_base` (covers all_locations-2 from v3). Backward-compatible re-exports preserved in `variant_fresh.py` for test stability.",
      "rationale": "Avoids 500-line clone; preserves test imports."
    },
    {
      "id": "ARCH-007",
      "decision": "Discovery surface is a committed `reigh-worker/.claude/skills/live-test/SKILL.md` plus docs/migration-vibecomfy-live-validation.md. Auto-memory is not the contract. argparse default for `--variant` stays `fresh`; skill recommends `--variant auto`.",
      "rationale": "Backward compat over silent default flip."
    },
    {
      "id": "ARCH-008",
      "decision": "`runpod-lifecycle/src/runpod_lifecycle/guard.py` is EXTENDED (not created). `prune_pods_by_prefix(prefixes, api_key, ...)` is added alongside existing `PodGuard`; `__init__.py:15` re-exports it. `reigh-worker/scripts/live_test/terminate_guard.py` delegates to it. Cross-repo import direction is one-way: reigh-worker \u2192 runpod-lifecycle.",
      "rationale": "Corrects v3's 'new module' wording; PodGuard is preserved."
    },
    {
      "id": "ARCH-009",
      "decision": "Volume region derived from `get_network_volumes(api_key)` `dataCenterId` (not from `RUNPOD_STORAGE_VOLUMES` name tuple). `find_gpu_type` has no region filter; pod-create enforces region via the attached volume's `dataCenterId`; if no GPU is available in that region the RunPod API error is surfaced verbatim with a `rl prebuilt list` hint.",
      "rationale": "Matches actual SDK capabilities (api.py:83-97)."
    },
    {
      "id": "ARCH-010",
      "decision": "Consumer bootstrap phase order: attach_prebuilt_volume \u2192 read_prebuilt_manifest \u2192 check_hard_fail_drift \u2192 extract_venv_bundle \u2192 extract_vibecomfy_bundle \u2192 sync_worker_ref \u2192 sync_vibecomfy_ref \u2192 verify_extracted_env \u2192 bind_models_dir \u2192 launch_worker. Verify runs AFTER syncs so partial-sync state is caught.",
      "rationale": "Resolves v2 callers-2."
    },
    {
      "id": "ARCH-011",
      "decision": "Worker subprocess inherits HF_HOME, HF_HUB_CACHE, and the ComfyUI models-path env via `_build_worker_env`'s prebuilt-aware wrapper. SSH bootstrap export alone is not sufficient; the dict consumed by `export_env(worker_env)` and `launch_worker_detached` must include them.",
      "rationale": "Resolves v2 FLAG-014/scope-3."
    },
    {
      "id": "ARCH-012",
      "decision": "Node-schema validation runs on every prebuilt bootstrap via `verify_extracted_env`, regardless of `custom_nodes_lock_hash` drift. Destructive `vibecomfy.cli nodes restore` remains gated on lockfile drift. If the cheap `nodes verify` subcommand does not exist in vibecomfy, the implementer adds it as a small read-only addition.",
      "rationale": "Covers schema-drift cases that don't touch the lockfile."
    },
    {
      "id": "ARCH-013",
      "decision": "Model warming is explicitly v2 scope. v1 accepts first-encounter cold-download; the 'materially faster' claim is bounded to deps install (67 min \u2192 ~10 min) plus steady-state model reuse via HF_HOME on the volume.",
      "rationale": "Recorded product call; tracked as v2 work via `rl prebuilt warm-models`."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Plan passed gate and preflight. Proceed to finalize. Verify unresolved flags against the plan and project code before accepting.",
  "robustness": "standard",
  "signals": {
    "iteration": 3,
    "idea": "Build a reusable prebuilt RunPod/VibeComfy validation environment for Reigh parity work. Context: we are validating Reigh worker VibeComfy parity with Wan2GP across all app capabilities. The current fresh RunPod live-test path spends ~46 minutes in reigh-worker uv sync --extra cuda124 and ~21 minutes installing VibeComfy/ComfyUI/custom nodes before it can run a single workflow. That makes workflow debugging slow, expensive, and noisy. We need a well-engineered solution, not a local hack. Research and implement the right abstraction across the workspace repos as needed (reigh-worker, vibecomfy, runpod-lifecycle, docs/skills). Desired outcome: a reusable validation environment path that can be launched for live tests without reinstalling the CUDA/PyTorch/ComfyUI/VibeComfy/custom-node stack each time, while staying branch-flexible enough to test arbitrary reigh-worker and vibecomfy refs. It should have explicit environment contracts, version metadata, dependency/model/cache preflight, and clear invalidation rules. It should not constrain workflow authoring to one approach or add brittle manual steps. It must improve observability: install/bootstrap phases should expose progress/logs and fail with actionable diagnostics. It must integrate cleanly with the existing live-test harness, RunPod lifecycle tools, workflow contracts, model reconciliation, node-schema validation, and documentation/skill guidance. Think through image vs network-volume cache vs warm persistent pod vs hybrid; pick the pragmatic path and implement it. Validation requirements: local tests for harness behavior, dry-run or unit coverage for selecting prebuilt environment, and at least one actual RunPod validation proving the new path reaches workflow execution materially faster than the cold fresh path and still terminates only pods it owns. Also document how future agents discover and use this path by default.",
    "significant_flags": 22,
    "unresolved_flags": [
      {
        "id": "FLAG-008",
        "concern": "Model-cache reuse (the largest cost driver after deps) is not part of the prebuilt contract. The manifest tracks .venv and custom_nodes but does not declare or invalidate the HuggingFace / model weight cache that downloads on first workflow execution. A prebuilt env that still cold-downloads 10-50GB of weights does not meet the materially faster bar for repeat workflow runs beyond the first.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Model warming is explicitly deferred to v2 (assumption #6). The idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50GB HF download. The success criterion for Run B model reuse depends on Run A having performed that download. Plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (Step 2.4d, Step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. The plan does not enumerate adding it to the vibecomfy repo as a planned change. If it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. Open question #3 explicitly defers verifying its existence.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-3",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Discovery-by-default: rev 2's silent dispatch flip was reverted (Step 9.1 keeps argparse default `fresh`). Skill + docs recommend `--variant auto`. Future agents reading docs will see the recommendation, but agents that invoke `--variant fresh` from existing scripts still pay the 67-min cost. This is the correct tradeoff for backward compat, but worth recording that 'used by default' is now a recommendation, not an enforced default.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-1",
        "concern": "Are the proposed changes technically correct?: Step 6.4 says 'New module runpod-lifecycle/src/runpod_lifecycle/guard.py'. That module ALREADY EXISTS (127 lines) and houses `PodGuard` (re-exported from __init__.py:15 as `PodGuard, install_signal_handlers`). The plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. As worded an executor could create a duplicate file or overwrite the existing PodGuard.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-2",
        "concern": "Are the proposed changes technically correct?: Step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. But there is NO worker bundle: Step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. On first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. The plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. This works functionally (git clone is cheap) but the description is misleading.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-3",
        "concern": "Are the proposed changes technically correct?: Step 4.1 keeps the default `python_version='3.10'` in `build_run_worker_command` for backward compat. The current `--python 3.10` in launch_command.py:43-44 works because `uv run --python 3.10` makes uv download/manage Python 3.10 itself (the runpod base image is py3.11). When the prebuilt path uses `python_version='3.11'` matching the base image, no uv-managed download is needed; when fresh continues with 3.10, uv-managed download is needed. The two paths diverge in interpreter source. Not new (existing behavior), but the plan does not call out that the prebuilt path is effectively a different interpreter than the fresh path.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-4",
        "concern": "Are the proposed changes technically correct?: Step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. The extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. The plan does not specify clobber vs merge semantics. A baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-5",
        "concern": "Are the proposed changes technically correct?: Step 6.3 builder install_worker invokes `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`. The builder pod is provisioned with `--container-disk-gb=200`. The venv install plus comfyui pip install plus uv cache fits, but bundling adds another ~10-25GB temporary tar.zst at `{staging_path}` on the network volume before atomic mv to `{cache_root}`. Plan does not address whether the staging directory write to MooseFS during the multi-GB tar+zstd stream is performant enough that the builder doesn't time out. No timeout/throughput target is set.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-6",
        "concern": "Are the proposed changes technically correct?: Step 6.5 fallback for cross-repo imports: 'if runpod-lifecycle cannot import reigh-worker code, replicate the helper as runpod_lifecycle.guard.prune_pods_by_prefix(prefixes, ...) and have terminate_guard.py delegate to it'. runpod-lifecycle is a standalone package with no reigh-worker dependency \u2014 the import direction is reigh-worker \u2192 runpod-lifecycle, not the reverse. The replicate-helper fallback is the only correct option; the import-from-reigh-worker primary branch is wrong by repo structure.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. But variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). The spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. This is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 7.1 says builds are 'one per region they want covered' but offers no story for promoting a single-region build to multi-region. Operators in different regions must run the full ~67-min builder pipeline independently, with no shared state. Not a correctness issue but a notable operational ceiling \u2014 at 4 regions in RUNPOD_STORAGE_VOLUMES, that's 4\u00d7 builder cost on each schema_version / python_version / cuda_extra bump.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-3",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: verify_extracted_env (Step 2.4) returns `list[str]`, but Step 8.3 says the consumer raises when issues are non-empty. Plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. The diagnostic UX matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, AND node-schema verify fail \u2014 operator should see all three reasons, not just one).",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations-1",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. Should be marked as 'extend existing'. The associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. Minor but enumerated.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations-2",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. But `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is NOT in the Step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). The plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. Without that, variant_prebuilt's HF_HOME-extending wrapper has nothing to wrap.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations-3",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. The actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%Y%m%dT%H%M%SZ'` (uppercase T, Z), and existing _FRESH_POD_NAME_RE at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). The plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations-4",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in Step 7.2 actually lives where? Plan says config.py exposes the helper. That mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). Placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. Minor consistency concern.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers-1",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. Step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). The plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. If it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers-2",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `_uv_sync_shell` (new in Step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=False`). variant_update.py:69-79 has a separate `REMOTE_UV_SYNC` that uses `--locked`. Plan does not migrate variant_update's REMOTE_UV_SYNC to call `_uv_sync_shell(..., with_locked=True)` \u2014 variant_update stays untouched per assumption #4. So the new `with_locked` parameter has no caller. Minor but adds unused API surface.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers-3",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `extract_bundle_to_container_disk` (new in Step 3.3): only variant_prebuilt invokes it. The target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). Plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). Default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. Probably correct as-is for the ephemeral pod use case.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-7",
        "concern": "Are the proposed changes technically correct?: Step 4 parameterizes `build_run_worker_command` to take `venv_path`. The hardcoded `--python 3.10` at launch_command.py:43-44 is NOT parameterized. If the prebuilt manifest's python_version is 3.11 (the runpod base image at config.py:91 is `py3.11-cuda12.4.1`), the worker is launched with a 3.10 uv interpreter while the prebuilt venv was created for 3.11. This is the same class of mismatch the python_version invalidation rule is supposed to catch but does not, because launch_command never reads the manifest python_version.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "FLAG-018",
        "concern": "Step 6.4 says 'new module runpod-lifecycle/src/runpod_lifecycle/guard.py', but that file ALREADY EXISTS (127 lines) and exports `PodGuard` + `install_signal_handlers` (re-exported from __init__.py:15). The plan must EXTEND the existing module rather than create a new one; ambiguous wording could cause an executor to overwrite PodGuard.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "MooseFS venv performance: hosting the full cuda124 .venv on the existing MooseFS network volume (the only acceptable host per assumption #1) will likely add per-invocation Python-import overhead that the plan never benchmarks. The existing code intentionally puts the venv on container-local disk and sets UV_LINK_MODE=copy precisely because MooseFS is slow for many small files. Plan should either include a steady-state startup benchmark in Step 11, allocate the venv to a non-MooseFS persistent volume, or document the import-cost tradeoff.",
        "resolution": "Pivoted the cache mechanism from \"venv on MooseFS network volume\" to \"compressed bundles on volume, extracted to container-local disk on pod start\" \u2014 this resolves the MooseFS-import-cost concern (FLAG-001/correctness-1) without giving up branch flexibility. Added explicit handling for every other significant flag: launch_command.py:37 is now an enumerated touch point and gets a parameterized venv_path (FLAG-002/correctness-2/all_locations-1); models/ tree on the volume + HF_HOME/ComfyUI env binding addresses model-cache reuse (FLAG-008/issue_hints-1); --extra cuda124 is mandatory and tested (correctness-3); python_version/schema_version/bundle_format_version/cuda_extra are explicit hard-fail invalidation triggers with a separate consumer code path (correctness-4/correctness-5); new pod prefixes for prebuilt + builder pods with terminate_guard broadened to a tuple (correctness-6/scope-2); build.lock with TTL takeover handles concurrent builders (scope-1); region-pinned volume naming with auto-selection across the existing RUNPOD_STORAGE_VOLUMES candidates (all_locations-2); new committed skill file at reigh-worker/.claude/skills/live-test/SKILL.md as the durable discovery surface, not auto-memory (all_locations-4); --variant auto becomes the new default, picking prebuilt when a volume exists and otherwise falling back to fresh, resolving discovery-vs-used-by-default (issue_hints-3); verify_extracted_env probe enumerates partial-state diagnostics (issue_hints-2); helpers extracted from variant_fresh.py into _shared.py before variant_prebuilt is written, not a clone (scope-3); container-disk floor of 100 GB enforced and 200 GB default preserved (callers-3); cli.py subparser registry enumerated as a touched file (all_locations-3); variant_update explicitly out of scope by decision (callers-1); ensure_vibecomfy_synced delta semantics for nodes restore are explicit and gated by lockfile hash drift (callers-2); builder pod cleanup wired through the same prune helper (scope-2). Helper extraction step added (Step 5) before the new variant to commit to reuse rather than aspire to it."
      },
      {
        "id": "FLAG-002",
        "concern": "launch_command.build_run_worker_command hardcodes UV_PROJECT_ENVIRONMENT=/opt/reigh-worker-live-test-venv at line 37; the prebuilt variant must parameterize this or workers will launch against a different venv than bootstrap synced.",
        "resolution": "Pivoted the cache mechanism from \"venv on MooseFS network volume\" to \"compressed bundles on volume, extracted to container-local disk on pod start\" \u2014 this resolves the MooseFS-import-cost concern (FLAG-001/correctness-1) without giving up branch flexibility. Added explicit handling for every other significant flag: launch_command.py:37 is now an enumerated touch point and gets a parameterized venv_path (FLAG-002/correctness-2/all_locations-1); models/ tree on the volume + HF_HOME/ComfyUI env binding addresses model-cache reuse (FLAG-008/issue_hints-1); --extra cuda124 is mandatory and tested (correctness-3); python_version/schema_version/bundle_format_version/cuda_extra are explicit hard-fail invalidation triggers with a separate consumer code path (correctness-4/correctness-5); new pod prefixes for prebuilt + builder pods with terminate_guard broadened to a tuple (correctness-6/scope-2); build.lock with TTL takeover handles concurrent builders (scope-1); region-pinned volume naming with auto-selection across the existing RUNPOD_STORAGE_VOLUMES candidates (all_locations-2); new committed skill file at reigh-worker/.claude/skills/live-test/SKILL.md as the durable discovery surface, not auto-memory (all_locations-4); --variant auto becomes the new default, picking prebuilt when a volume exists and otherwise falling back to fresh, resolving discovery-vs-used-by-default (issue_hints-3); verify_extracted_env probe enumerates partial-state diagnostics (issue_hints-2); helpers extracted from variant_fresh.py into _shared.py before variant_prebuilt is written, not a clone (scope-3); container-disk floor of 100 GB enforced and 200 GB default preserved (callers-3); cli.py subparser registry enumerated as a touched file (all_locations-3); variant_update explicitly out of scope by decision (callers-1); ensure_vibecomfy_synced delta semantics for nodes restore are explicit and gated by lockfile hash drift (callers-2); builder pod cleanup wired through the same prune helper (scope-2). Helper extraction step added (Step 5) before the new variant to commit to reuse rather than aspire to it."
      },
      {
        "id": "FLAG-003",
        "concern": "Schema-version mismatch handling not differentiated from other drift. Plan treats schema_version drift via the same delta-sync code path that handles pyproject_hash drift, but schema_version bumps mean on-disk layout is incompatible and only a full rebuild via rl prebuilt build can fix it.",
        "resolution": "Plan Step 1.2 and Step 7.2 invalidation rule says hard-rebuild when schema_version changes but consumer flow only allows delta-sync or abort, not a distinguished must-rebuild-via-builder path."
      },
      {
        "id": "FLAG-004",
        "concern": "Concurrent builder collisions are unguarded. Two simultaneous rl prebuilt build invocations against the same named volume corrupt the cache with no lockfile/sentinel.",
        "resolution": "Plan Step 5 no mention of write-locking the volume, atomic manifest rename, or in-progress marker in the manifest schema."
      },
      {
        "id": "FLAG-005",
        "concern": "Builder pod orphan risk: prebuilt builder creates a pod but is not integrated with prune_stale_live_test_pods (which keys on the reigh-live-test-fresh- prefix). Builder crash between pod-create and terminate leaves an orphan that no existing reaper picks up.",
        "resolution": "terminate_guard.py:14 (prefix constant); plan Step 5 introduces a separate runtime with no prefix declaration or reaper extension."
      },
      {
        "id": "FLAG-006",
        "concern": "Step 8.4 inverts the disk-size constraint. Moving content from ephemeral container disk to the network volume INCREASES persistent volume footprint, not decreases it. Plan should grow disk_size_gb / volume capacity, not shrink container disk in a way that conflates the two budgets.",
        "resolution": "Plan Step 8.4; project memory project_live_test_disk.md notes 50GB is already too small."
      },
      {
        "id": "FLAG-007",
        "concern": "Regional volume availability is unaddressed. RUNPOD_STORAGE_VOLUMES is a multi-region tuple precisely because RunPod volumes are region-pinned and GPU quota varies by region. Plan defaults to a single-name volume, which will fail pod-create whenever the GPU is allocated outside the volume region.",
        "resolution": "config.py:98 (RUNPOD_STORAGE_VOLUMES tuple); plan Step 1.1 single volume_name field with no regional alternates."
      },
      {
        "id": "FLAG-009",
        "concern": "Container-disk path convention: plan invents `/workspace-local/reigh-worker` and `/workspace-local/vibecomfy` as 'container disk via --container-disk mount', but no such path exists in the runpod base image or the codebase. /workspace is the network volume mount. Intent is almost certainly /opt/ (matching the existing /opt/reigh-worker-live-test-venv pattern); using /workspace-local invites a real bug where the path doesn't exist and bundle extraction fails. Plan must specify the actual container-disk paths consistent with the runpod image and existing code.",
        "resolution": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1)."
      },
      {
        "id": "FLAG-010",
        "concern": "launch_command.py:43-44 hardcodes `--python 3.10` for uv run; the prebuilt manifest's python_version field is meant to be a hard-fail invalidation trigger but the worker spawn command never reads it. A prebuilt venv built against the py3.11 runpod base image would be launched with --python 3.10, undermining the python_version invariant. The plan parameterizes venv_path but not python_version through build_run_worker_command.",
        "resolution": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1)."
      },
      {
        "id": "FLAG-011",
        "concern": "comfyui.tar.zst is a third bundle the plan creates, but ComfyUI is `pip install`'d into the venv (ssh_bootstrap.py:225-227) and lives in site-packages \u2014 there is no separate ComfyUI install tree to bundle distinct from the venv. extract_comfyui_bundle is either redundant work or based on a wrong model of where ComfyUI lives.",
        "resolution": "ssh_bootstrap.py:225-227 pip-installs comfyui as a regular package; Step 8.3 lists extract_comfyui_bundle as a distinct phase."
      },
      {
        "id": "FLAG-012",
        "concern": "Region-suffix derivation mismatches data: PREBUILT_VOLUME_CANDIDATES is built by lowercasing RUNPOD_STORAGE_VOLUMES entries, but the first entry 'Peter' is a volume name not a region. The naming convention conflates two semantic categories. Should derive region from each volume's dataCenterId via get_network_volumes, not from volume names.",
        "resolution": "config.py:98 storage_volumes tuple mixes 'Peter' (name) with 'EU-NO-1' (region); Step 7.2 mirrors the tuple as-is."
      },
      {
        "id": "FLAG-013",
        "concern": "find_gpu_type does not support region filtering. Step 8.2 says 'use the volume's dataCenterId to constrain find_gpu_type if possible'. The SDK function at runpod-lifecycle/src/runpod_lifecycle/api.py:83-97 only matches by displayName/id; there is no region filter to add without a separate API call. Plan should drop the optimistic language and state that GPU/region pairing is enforced solely by volume attachment.",
        "resolution": "api.py:83-97 find_gpu_type signature; Step 8.2 conditional 'if possible'."
      },
      {
        "id": "FLAG-014",
        "concern": "HF_HOME / HF_HUB_CACHE redirection in bind_models_dir only sets env in the SSH bootstrap session. The worker subprocess is launched via launch_worker_detached with explicit `export_env(worker_env)`. If HF_HOME is not added to `_build_worker_env`, the worker process never sees the model cache redirect and re-downloads weights despite the cached models/ tree.",
        "resolution": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1)."
      },
      {
        "id": "FLAG-015",
        "concern": "Step 8.3 orders verify_extracted_env BEFORE sync_worker_ref / sync_vibecomfy_ref. If the manifest's pyproject_hash drifts (acceptable delta-sync case), the venv contents change AFTER the probe. A partial-state failure introduced by a network drop mid-uv-sync goes undetected because the probe already ran. Probe should be re-run after any sync that mutates the venv.",
        "resolution": "Step 8.3 phase order; Step 2.4 verify_extracted_env returns a list of issues; partial-state diagnostic claim depends on the probe catching post-sync corruption."
      },
      {
        "id": "FLAG-016",
        "concern": "Auto-variant default change is a silent behavior change. Existing scripts that omit --variant get 'fresh' today; after the change they get 'auto' which can dispatch to 'prebuilt' against any matching volume the operator has on their RunPod account, even one built by a teammate with a different attention_profile. Plan should keep --variant fresh default or emit a one-time interactive warning, plus document the change in CHANGELOG / docs.",
        "resolution": "Step 9.5 changes argparse default to auto; assumption #7 declares non-breaking."
      },
      {
        "id": "FLAG-017",
        "concern": "Plan models the runpod-lifecycle CLI as needing to import reigh-worker's terminate_guard for prune behavior (Step 6.5). runpod-lifecycle is a standalone package and reigh-worker depends ON it, not the other way around. Only the replicate-helper fallback path (`runpod_lifecycle.guard.prune_pods_by_prefix`) is structurally correct. The conditional wording risks an implementer choosing the wrong branch.",
        "resolution": "Step 6.5 conditional 'if runpod-lifecycle cannot import reigh-worker code'; package dependency direction is unambiguous from runpod-lifecycle/__init__.py which has no reigh-worker imports."
      }
    ],
    "weighted_score": 35.5,
    "weighted_history": [
      34.0,
      40.0
    ],
    "plan_delta_from_previous": 84.59,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 3. Weighted score trajectory: 34.0 -> 40.0 -> 35.5. Plan deltas: 91.4%, 84.6%. Recurring critiques: 0. Resolved flags: 16. Open significant flags: 22.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [
    {
      "flag_id": "FLAG-008",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Already marked addressed in the gate signals. The prebuilt path covers deps and steady-state model reuse; v1 accepts first-encounter HF download as in-scope. Recorded as ARCH-013 settled decision."
    },
    {
      "flag_id": "issue_hints-1",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Same as FLAG-008. Model warming is a v2 product call; the v1 scope is reasonable and explicit in the plan's assumptions + open questions. Operator can run the same workflow twice if they need warm-cache validation today."
    },
    {
      "flag_id": "issue_hints-2",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "If `vibecomfy.cli nodes verify` does not exist, the implementer adds it as a small read-only addition during execution (enumerated in the warnings). The probe is genuinely cheap and the fallback (template_index.json count + json-parse) is well-specified. Not a planning gap a fourth revision would meaningfully improve."
    },
    {
      "flag_id": "issue_hints-3",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Backward-compat preservation deliberately wins over silent default flip; the rev 2 critique flagged the flip as a regression risk and rev 3 reverted it correctly. 'Discovery-by-default' via the committed skill is the right contract; existing scripts continue to work unchanged."
    },
    {
      "flag_id": "correctness-1",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "The plan's 'new module' wording is imprecise but ARCH-008 settled decision records the correct intent: extend the existing guard.py. Any competent implementer reads existing files before editing; the executor warning explicitly flags this."
    },
    {
      "flag_id": "correctness-2",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "The 'starting point' wording is misleading but functionally harmless: `ensure_git_ref_synced(force_clone=True)` on a missing dir does a full clone, which is fast. Documentation polish, not a defect."
    },
    {
      "flag_id": "correctness-3",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Fresh path uses uv-managed py3.10; prebuilt uses base-image py3.11. This divergence is intentional (matches the runpod base image to save uv-managed download time) and is encoded in the manifest's `python_version` field. The fresh path remains observably unchanged; that is the requirement."
    },
    {
      "flag_id": "correctness-4",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Consumer overwrites `extra_model_paths.yaml` on every bootstrap (ephemeral pod; deterministic state win). Builder-baked content is irrelevant because the consumer's bind_models_dir phase is authoritative. Specified in the warnings list."
    },
    {
      "flag_id": "correctness-5",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "MooseFS staging-stream throughput is the only unbenchmarked perf assumption; Step 13 validates it empirically. If it exceeds 10 min, the operator notices in the prebuilt-validation.md artifact and we revisit in a follow-up; not a v1 blocker."
    },
    {
      "flag_id": "correctness-6",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Already marked addressed in the gate signals. ARCH-008 settled decision records the correct one-way import direction."
    },
    {
      "flag_id": "scope-1",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "The guard message wording can be refined to mention --spawn-takeover during implementation; the guard logic itself is correct (blocks both modes). Cosmetic."
    },
    {
      "flag_id": "scope-2",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Multi-region build cost (4\u00d7 builder run per schema bump if all 4 regions covered) is a known operational ceiling; v2 will explore promotion via volume snapshots. Acceptable v1 limitation."
    },
    {
      "flag_id": "scope-3",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Implementer joins all `verify_extracted_env` issues with newlines into the raised RuntimeError message; specified in warnings. Cosmetic gap, not a defect."
    },
    {
      "flag_id": "all_locations-1",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Covered by ARCH-008 settled decision and the executor warnings. __init__.py:15 re-export of `prune_pods_by_prefix` is a one-line addition the implementer makes alongside extending guard.py."
    },
    {
      "flag_id": "all_locations-2",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "ARCH-006 settled decision now includes `_build_worker_env` in the extraction list as `_build_worker_env_base`. The warnings call this out explicitly so the implementer cannot miss it."
    },
    {
      "flag_id": "all_locations-3",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Regex case convention is a 30-second check during implementation (read `terminate_guard.py:16` and `_timestamp_label`; match whichever convention they use). Warnings flag this. Not worth another revision cycle."
    },
    {
      "flag_id": "all_locations-4",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Placing `prebuilt_name_for_profile` in config.py vs a new module is a cosmetic placement decision the implementer can resolve in 10 seconds. Not a planning gap."
    },
    {
      "flag_id": "callers-1",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "The fact that `_finalize_args` runs for prebuilt too is implicit in the shared dispatch architecture; an alert implementer wires it correctly. Warnings list calls this out to remove ambiguity. Existing test suite would catch divergence on first run."
    },
    {
      "flag_id": "callers-2",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Unused `with_locked` parameter is a few lines of API surface that costs nothing; intent is to keep variant_update behavior untouched (assumption #4) while making _uv_sync_shell future-proof. Trivially trimmable later."
    },
    {
      "flag_id": "callers-3",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Default `tar` overwrite behavior is correct for the ephemeral-pod use case (we want fresh state on extract). No --keep-newer-files needed."
    },
    {
      "flag_id": "correctness-7",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Already marked addressed in the gate signals. ARCH-002 settled decision records that build_run_worker_command now takes python_version and reads it from the manifest."
    },
    {
      "flag_id": "FLAG-018",
      "action": "accept_tradeoff",
      "evidence": "",
      "rationale": "Duplicate of correctness-1. ARCH-008 settled decision and the executor warnings make the correct intent (extend existing guard.py) unambiguous; PodGuard is preserved."
    }
  ],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Flag registry:
        [
  {
    "id": "FLAG-001",
    "concern": "MooseFS venv performance: hosting the full cuda124 .venv on the existing MooseFS network volume (the only acceptable host per assumption #1) will likely add per-invocation Python-import overhead that the plan never benchmarks. The existing code intentionally puts the venv on container-local disk and sets UV_LINK_MODE=copy precisely because MooseFS is slow for many small files. Plan should either include a steady-state startup benchmark in Step 11, allocate the venv to a non-MooseFS persistent volume, or document the import-cost tradeoff.",
    "evidence": "Pivoted the cache mechanism from \"venv on MooseFS network volume\" to \"compressed bundles on volume, extracted to container-local disk on pod start\" \u2014 this resolves the MooseFS-import-cost concern (FLAG-001/correctness-1) without giving up branch flexibility. Added explicit handling for every other significant flag: launch_command.py:37 is now an enumerated touch point and gets a parameterized venv_path (FLAG-002/correctness-2/all_locations-1); models/ tree on the volume + HF_HOME/ComfyUI env binding addresses model-cache reuse (FLAG-008/issue_hints-1); --extra cuda124 is mandatory and tested (correctness-3); python_version/schema_version/bundle_format_version/cuda_extra are explicit hard-fail invalidation triggers with a separate consumer code path (correctness-4/correctness-5); new pod prefixes for prebuilt + builder pods with terminate_guard broadened to a tuple (correctness-6/scope-2); build.lock with TTL takeover handles concurrent builders (scope-1); region-pinned volume naming with auto-selection across the existing RUNPOD_STORAGE_VOLUMES candidates (all_locations-2); new committed skill file at reigh-worker/.claude/skills/live-test/SKILL.md as the durable discovery surface, not auto-memory (all_locations-4); --variant auto becomes the new default, picking prebuilt when a volume exists and otherwise falling back to fresh, resolving discovery-vs-used-by-default (issue_hints-3); verify_extracted_env probe enumerates partial-state diagnostics (issue_hints-2); helpers extracted from variant_fresh.py into _shared.py before variant_prebuilt is written, not a clone (scope-3); container-disk floor of 100 GB enforced and 200 GB default preserved (callers-3); cli.py subparser registry enumerated as a touched file (all_locations-3); variant_update explicitly out of scope by decision (callers-1); ensure_vibecomfy_synced delta semantics for nodes restore are explicit and gated by lockfile hash drift (callers-2); builder pod cleanup wired through the same prune helper (scope-2). Helper extraction step added (Step 5) before the new variant to commit to reuse rather than aspire to it.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-002",
    "concern": "launch_command.build_run_worker_command hardcodes UV_PROJECT_ENVIRONMENT=/opt/reigh-worker-live-test-venv at line 37; the prebuilt variant must parameterize this or workers will launch against a different venv than bootstrap synced.",
    "evidence": "Pivoted the cache mechanism from \"venv on MooseFS network volume\" to \"compressed bundles on volume, extracted to container-local disk on pod start\" \u2014 this resolves the MooseFS-import-cost concern (FLAG-001/correctness-1) without giving up branch flexibility. Added explicit handling for every other significant flag: launch_command.py:37 is now an enumerated touch point and gets a parameterized venv_path (FLAG-002/correctness-2/all_locations-1); models/ tree on the volume + HF_HOME/ComfyUI env binding addresses model-cache reuse (FLAG-008/issue_hints-1); --extra cuda124 is mandatory and tested (correctness-3); python_version/schema_version/bundle_format_version/cuda_extra are explicit hard-fail invalidation triggers with a separate consumer code path (correctness-4/correctness-5); new pod prefixes for prebuilt + builder pods with terminate_guard broadened to a tuple (correctness-6/scope-2); build.lock with TTL takeover handles concurrent builders (scope-1); region-pinned volume naming with auto-selection across the existing RUNPOD_STORAGE_VOLUMES candidates (all_locations-2); new committed skill file at reigh-worker/.claude/skills/live-test/SKILL.md as the durable discovery surface, not auto-memory (all_locations-4); --variant auto becomes the new default, picking prebuilt when a volume exists and otherwise falling back to fresh, resolving discovery-vs-used-by-default (issue_hints-3); verify_extracted_env probe enumerates partial-state diagnostics (issue_hints-2); helpers extracted from variant_fresh.py into _shared.py before variant_prebuilt is written, not a clone (scope-3); container-disk floor of 100 GB enforced and 200 GB default preserved (callers-3); cli.py subparser registry enumerated as a touched file (all_locations-3); variant_update explicitly out of scope by decision (callers-1); ensure_vibecomfy_synced delta semantics for nodes restore are explicit and gated by lockfile hash drift (callers-2); builder pod cleanup wired through the same prune helper (scope-2). Helper extraction step added (Step 5) before the new variant to commit to reuse rather than aspire to it.",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-003",
    "concern": "Schema-version mismatch handling not differentiated from other drift. Plan treats schema_version drift via the same delta-sync code path that handles pyproject_hash drift, but schema_version bumps mean on-disk layout is incompatible and only a full rebuild via rl prebuilt build can fix it.",
    "evidence": "Plan Step 1.2 and Step 7.2 invalidation rule says hard-rebuild when schema_version changes but consumer flow only allows delta-sync or abort, not a distinguished must-rebuild-via-builder path.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-004",
    "concern": "Concurrent builder collisions are unguarded. Two simultaneous rl prebuilt build invocations against the same named volume corrupt the cache with no lockfile/sentinel.",
    "evidence": "Plan Step 5 no mention of write-locking the volume, atomic manifest rename, or in-progress marker in the manifest schema.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-005",
    "concern": "Builder pod orphan risk: prebuilt builder creates a pod but is not integrated with prune_stale_live_test_pods (which keys on the reigh-live-test-fresh- prefix). Builder crash between pod-create and terminate leaves an orphan that no existing reaper picks up.",
    "evidence": "terminate_guard.py:14 (prefix constant); plan Step 5 introduces a separate runtime with no prefix declaration or reaper extension.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-006",
    "concern": "Step 8.4 inverts the disk-size constraint. Moving content from ephemeral container disk to the network volume INCREASES persistent volume footprint, not decreases it. Plan should grow disk_size_gb / volume capacity, not shrink container disk in a way that conflates the two budgets.",
    "evidence": "Plan Step 8.4; project memory project_live_test_disk.md notes 50GB is already too small.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-007",
    "concern": "Regional volume availability is unaddressed. RUNPOD_STORAGE_VOLUMES is a multi-region tuple precisely because RunPod volumes are region-pinned and GPU quota varies by region. Plan defaults to a single-name volume, which will fail pod-create whenever the GPU is allocated outside the volume region.",
    "evidence": "config.py:98 (RUNPOD_STORAGE_VOLUMES tuple); plan Step 1.1 single volume_name field with no regional alternates.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-008",
    "concern": "Model-cache reuse (the largest cost driver after deps) is not part of the prebuilt contract. The manifest tracks .venv and custom_nodes but does not declare or invalidate the HuggingFace / model weight cache that downloads on first workflow execution. A prebuilt env that still cold-downloads 10-50GB of weights does not meet the materially faster bar for repeat workflow runs beyond the first.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 29: requires human verification (observe_runtime_logs, verify_physical_device).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 30: requires human verification (observe_runtime_logs, verify_physical_device).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-2",
    "concern": "Criterion 31: requires human verification (observe_runtime_logs, verify_physical_device).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "issue_hints-1",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Model warming is explicitly deferred to v2 (assumption #6). The idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50GB HF download. The success criterion for Run B model reuse depends on Run A having performed that download. Plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too.",
    "evidence": "Model warming is explicitly deferred to v2 (assumption #6). The idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50GB HF download. The success criterion for Run B model reuse depends on Run A having performed that download. Plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "issue_hints-2",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (Step 2.4d, Step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. The plan does not enumerate adding it to the vibecomfy repo as a planned change. If it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. Open question #3 explicitly defers verifying its existence.",
    "evidence": "Node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (Step 2.4d, Step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. The plan does not enumerate adding it to the vibecomfy repo as a planned change. If it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. Open question #3 explicitly defers verifying its existence.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "issue_hints-3",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Discovery-by-default: rev 2's silent dispatch flip was reverted (Step 9.1 keeps argparse default `fresh`). Skill + docs recommend `--variant auto`. Future agents reading docs will see the recommendation, but agents that invoke `--variant fresh` from existing scripts still pay the 67-min cost. This is the correct tradeoff for backward compat, but worth recording that 'used by default' is now a recommendation, not an enforced default.",
    "evidence": "Discovery-by-default: rev 2's silent dispatch flip was reverted (Step 9.1 keeps argparse default `fresh`). Skill + docs recommend `--variant auto`. Future agents reading docs will see the recommendation, but agents that invoke `--variant fresh` from existing scripts still pay the 67-min cost. This is the correct tradeoff for backward compat, but worth recording that 'used by default' is now a recommendation, not an enforced default.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-1",
    "concern": "Are the proposed changes technically correct?: Step 6.4 says 'New module runpod-lifecycle/src/runpod_lifecycle/guard.py'. That module ALREADY EXISTS (127 lines) and houses `PodGuard` (re-exported from __init__.py:15 as `PodGuard, install_signal_handlers`). The plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. As worded an executor could create a duplicate file or overwrite the existing PodGuard.",
    "evidence": "Step 6.4 says 'New module runpod-lifecycle/src/runpod_lifecycle/guard.py'. That module ALREADY EXISTS (127 lines) and houses `PodGuard` (re-exported from __init__.py:15 as `PodGuard, install_signal_handlers`). The plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. As worded an executor could create a duplicate file or overwrite the existing PodGuard.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-2",
    "concern": "Are the proposed changes technically correct?: Step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. But there is NO worker bundle: Step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. On first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. The plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. This works functionally (git clone is cheap) but the description is misleading.",
    "evidence": "Step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. But there is NO worker bundle: Step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. The builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. On first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. The plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. This works functionally (git clone is cheap) but the description is misleading.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-3",
    "concern": "Are the proposed changes technically correct?: Step 4.1 keeps the default `python_version='3.10'` in `build_run_worker_command` for backward compat. The current `--python 3.10` in launch_command.py:43-44 works because `uv run --python 3.10` makes uv download/manage Python 3.10 itself (the runpod base image is py3.11). When the prebuilt path uses `python_version='3.11'` matching the base image, no uv-managed download is needed; when fresh continues with 3.10, uv-managed download is needed. The two paths diverge in interpreter source. Not new (existing behavior), but the plan does not call out that the prebuilt path is effectively a different interpreter than the fresh path.",
    "evidence": "Step 4.1 keeps the default `python_version='3.10'` in `build_run_worker_command` for backward compat. The current `--python 3.10` in launch_command.py:43-44 works because `uv run --python 3.10` makes uv download/manage Python 3.10 itself (the runpod base image is py3.11). When the prebuilt path uses `python_version='3.11'` matching the base image, no uv-managed download is needed; when fresh continues with 3.10, uv-managed download is needed. The two paths diverge in interpreter source. Not new (existing behavior), but the plan does not call out that the prebuilt path is effectively a different interpreter than the fresh path.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-4",
    "concern": "Are the proposed changes technically correct?: Step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. The extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. The plan does not specify clobber vs merge semantics. A baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree.",
    "evidence": "Step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. The extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. The plan does not specify clobber vs merge semantics. A baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-5",
    "concern": "Are the proposed changes technically correct?: Step 6.3 builder install_worker invokes `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`. The builder pod is provisioned with `--container-disk-gb=200`. The venv install plus comfyui pip install plus uv cache fits, but bundling adds another ~10-25GB temporary tar.zst at `{staging_path}` on the network volume before atomic mv to `{cache_root}`. Plan does not address whether the staging directory write to MooseFS during the multi-GB tar+zstd stream is performant enough that the builder doesn't time out. No timeout/throughput target is set.",
    "evidence": "Step 6.3 builder install_worker invokes `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`. The builder pod is provisioned with `--container-disk-gb=200`. The venv install plus comfyui pip install plus uv cache fits, but bundling adds another ~10-25GB temporary tar.zst at `{staging_path}` on the network volume before atomic mv to `{cache_root}`. Plan does not address whether the staging directory write to MooseFS during the multi-GB tar+zstd stream is performant enough that the builder doesn't time out. No timeout/throughput target is set.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "correctness-6",
    "concern": "Are the proposed changes technically correct?: Step 6.5 fallback for cross-repo imports: 'if runpod-lifecycle cannot import reigh-worker code, replicate the helper as runpod_lifecycle.guard.prune_pods_by_prefix(prefixes, ...) and have terminate_guard.py delegate to it'. runpod-lifecycle is a standalone package with no reigh-worker dependency \u2014 the import direction is reigh-worker \u2192 runpod-lifecycle, not the reverse. The replicate-helper fallback is the only correct option; the import-from-reigh-worker primary branch is wrong by repo structure.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "scope-1",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. But variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). The spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. This is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id.",
    "evidence": "Step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. But variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). The spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. This is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "scope-2",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Step 7.1 says builds are 'one per region they want covered' but offers no story for promoting a single-region build to multi-region. Operators in different regions must run the full ~67-min builder pipeline independently, with no shared state. Not a correctness issue but a notable operational ceiling \u2014 at 4 regions in RUNPOD_STORAGE_VOLUMES, that's 4\u00d7 builder cost on each schema_version / python_version / cuda_extra bump.",
    "evidence": "Step 7.1 says builds are 'one per region they want covered' but offers no story for promoting a single-region build to multi-region. Operators in different regions must run the full ~67-min builder pipeline independently, with no shared state. Not a correctness issue but a notable operational ceiling \u2014 at 4 regions in RUNPOD_STORAGE_VOLUMES, that's 4\u00d7 builder cost on each schema_version / python_version / cuda_extra bump.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "scope-3",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: verify_extracted_env (Step 2.4) returns `list[str]`, but Step 8.3 says the consumer raises when issues are non-empty. Plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. The diagnostic UX matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, AND node-schema verify fail \u2014 operator should see all three reasons, not just one).",
    "evidence": "verify_extracted_env (Step 2.4) returns `list[str]`, but Step 8.3 says the consumer raises when issues are non-empty. Plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. The diagnostic UX matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, AND node-schema verify fail \u2014 operator should see all three reasons, not just one).",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "all_locations-1",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. Should be marked as 'extend existing'. The associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. Minor but enumerated.",
    "evidence": "Plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. Should be marked as 'extend existing'. The associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. Minor but enumerated.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "all_locations-2",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. But `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is NOT in the Step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). The plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. Without that, variant_prebuilt's HF_HOME-extending wrapper has nothing to wrap.",
    "evidence": "Step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. But `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is NOT in the Step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). The plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. Without that, variant_prebuilt's HF_HOME-extending wrapper has nothing to wrap.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "all_locations-3",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. The actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%Y%m%dT%H%M%SZ'` (uppercase T, Z), and existing _FRESH_POD_NAME_RE at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). The plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention.",
    "evidence": "Step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. The actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%Y%m%dT%H%M%SZ'` (uppercase T, Z), and existing _FRESH_POD_NAME_RE at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). The plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "all_locations-4",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in Step 7.2 actually lives where? Plan says config.py exposes the helper. That mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). Placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. Minor consistency concern.",
    "evidence": "Step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in Step 7.2 actually lives where? Plan says config.py exposes the helper. That mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). Placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. Minor consistency concern.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "callers-1",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. Step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). The plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. If it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh.",
    "evidence": "Step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. Step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). The plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. If it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "callers-2",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `_uv_sync_shell` (new in Step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=False`). variant_update.py:69-79 has a separate `REMOTE_UV_SYNC` that uses `--locked`. Plan does not migrate variant_update's REMOTE_UV_SYNC to call `_uv_sync_shell(..., with_locked=True)` \u2014 variant_update stays untouched per assumption #4. So the new `with_locked` parameter has no caller. Minor but adds unused API surface.",
    "evidence": "Callers of `_uv_sync_shell` (new in Step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=False`). variant_update.py:69-79 has a separate `REMOTE_UV_SYNC` that uses `--locked`. Plan does not migrate variant_update's REMOTE_UV_SYNC to call `_uv_sync_shell(..., with_locked=True)` \u2014 variant_update stays untouched per assumption #4. So the new `with_locked` parameter has no caller. Minor but adds unused API surface.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "callers-3",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Callers of `extract_bundle_to_container_disk` (new in Step 3.3): only variant_prebuilt invokes it. The target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). Plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). Default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. Probably correct as-is for the ephemeral pod use case.",
    "evidence": "Callers of `extract_bundle_to_container_disk` (new in Step 3.3): only variant_prebuilt invokes it. The target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). Plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). Default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. Probably correct as-is for the ephemeral pod use case.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "FLAG-009",
    "concern": "Container-disk path convention: plan invents `/workspace-local/reigh-worker` and `/workspace-local/vibecomfy` as 'container disk via --container-disk mount', but no such path exists in the runpod base image or the codebase. /workspace is the network volume mount. Intent is almost certainly /opt/ (matching the existing /opt/reigh-worker-live-test-venv pattern); using /workspace-local invites a real bug where the path doesn't exist and bundle extraction fails. Plan must specify the actual container-disk paths consistent with the runpod image and existing code.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-010",
    "concern": "launch_command.py:43-44 hardcodes `--python 3.10` for uv run; the prebuilt manifest's python_version field is meant to be a hard-fail invalidation trigger but the worker spawn command never reads it. A prebuilt venv built against the py3.11 runpod base image would be launched with --python 3.10, undermining the python_version invariant. The plan parameterizes venv_path but not python_version through build_run_worker_command.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-011",
    "concern": "comfyui.tar.zst is a third bundle the plan creates, but ComfyUI is `pip install`'d into the venv (ssh_bootstrap.py:225-227) and lives in site-packages \u2014 there is no separate ComfyUI install tree to bundle distinct from the venv. extract_comfyui_bundle is either redundant work or based on a wrong model of where ComfyUI lives.",
    "evidence": "ssh_bootstrap.py:225-227 pip-installs comfyui as a regular package; Step 8.3 lists extract_comfyui_bundle as a distinct phase.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-012",
    "concern": "Region-suffix derivation mismatches data: PREBUILT_VOLUME_CANDIDATES is built by lowercasing RUNPOD_STORAGE_VOLUMES entries, but the first entry 'Peter' is a volume name not a region. The naming convention conflates two semantic categories. Should derive region from each volume's dataCenterId via get_network_volumes, not from volume names.",
    "evidence": "config.py:98 storage_volumes tuple mixes 'Peter' (name) with 'EU-NO-1' (region); Step 7.2 mirrors the tuple as-is.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-013",
    "concern": "find_gpu_type does not support region filtering. Step 8.2 says 'use the volume's dataCenterId to constrain find_gpu_type if possible'. The SDK function at runpod-lifecycle/src/runpod_lifecycle/api.py:83-97 only matches by displayName/id; there is no region filter to add without a separate API call. Plan should drop the optimistic language and state that GPU/region pairing is enforced solely by volume attachment.",
    "evidence": "api.py:83-97 find_gpu_type signature; Step 8.2 conditional 'if possible'.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-014",
    "concern": "HF_HOME / HF_HUB_CACHE redirection in bind_models_dir only sets env in the SSH bootstrap session. The worker subprocess is launched via launch_worker_detached with explicit `export_env(worker_env)`. If HF_HOME is not added to `_build_worker_env`, the worker process never sees the model cache redirect and re-downloads weights despite the cached models/ tree.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "verified",
    "severity": "significant"
  },
  {
    "id": "FLAG-015",
    "concern": "Step 8.3 orders verify_extracted_env BEFORE sync_worker_ref / sync_vibecomfy_ref. If the manifest's pyproject_hash drifts (acceptable delta-sync case), the venv contents change AFTER the probe. A partial-state failure introduced by a network drop mid-uv-sync goes undetected because the probe already ran. Probe should be re-run after any sync that mutates the venv.",
    "evidence": "Step 8.3 phase order; Step 2.4 verify_extracted_env returns a list of issues; partial-state diagnostic claim depends on the probe catching post-sync corruption.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-016",
    "concern": "Auto-variant default change is a silent behavior change. Existing scripts that omit --variant get 'fresh' today; after the change they get 'auto' which can dispatch to 'prebuilt' against any matching volume the operator has on their RunPod account, even one built by a teammate with a different attention_profile. Plan should keep --variant fresh default or emit a one-time interactive warning, plus document the change in CHANGELOG / docs.",
    "evidence": "Step 9.5 changes argparse default to auto; assumption #7 declares non-breaking.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "FLAG-017",
    "concern": "Plan models the runpod-lifecycle CLI as needing to import reigh-worker's terminate_guard for prune behavior (Step 6.5). runpod-lifecycle is a standalone package and reigh-worker depends ON it, not the other way around. Only the replicate-helper fallback path (`runpod_lifecycle.guard.prune_pods_by_prefix`) is structurally correct. The conditional wording risks an implementer choosing the wrong branch.",
    "evidence": "Step 6.5 conditional 'if runpod-lifecycle cannot import reigh-worker code'; package dependency direction is unambiguous from runpod-lifecycle/__init__.py which has no reigh-worker imports.",
    "status": "verified",
    "severity": "minor"
  },
  {
    "id": "correctness-7",
    "concern": "Are the proposed changes technically correct?: Step 4 parameterizes `build_run_worker_command` to take `venv_path`. The hardcoded `--python 3.10` at launch_command.py:43-44 is NOT parameterized. If the prebuilt manifest's python_version is 3.11 (the runpod base image at config.py:91 is `py3.11-cuda12.4.1`), the worker is launched with a 3.10 uv interpreter while the prebuilt venv was created for 3.11. This is the same class of mismatch the python_version invalidation rule is supposed to catch but does not, because launch_command never reads the manifest python_version.",
    "evidence": "Surgical fixup pass over rev 2, NOT another pivot \u2014 bundle-extract architecture preserved. Fixed every open significant flag inline: (a) replaced invented `/workspace-local/*` paths with `/opt/reigh-livetest-prebuilt/{worker,vibecomfy}` consistent with the existing `/opt/...-venv` convention (correctness-1/FLAG-009); (b) dropped the phantom `comfyui.tar.zst` bundle since ComfyUI lives inside the venv site-packages (correctness-2); (c) parameterized `--python` in `build_run_worker_command` so manifest `python_version` flows end-to-end and the 3.10/3.11 mismatch is closed (correctness-7/FLAG-010/all_locations-1); (d) threaded `HF_HOME`/`HF_HUB_CACHE`/ComfyUI-models-path into `_build_worker_env` so the worker subprocess sees the model cache (FLAG-014/scope-3); (e) corrected `PREBUILT_VOLUME_CANDIDATES` derivation \u2014 region now comes from `dataCenterId` returned by `get_network_volumes`, not from the volume-name tuple `RUNPOD_STORAGE_VOLUMES` (correctness-3); (f) dropped the misleading \"if possible\" GPU region-filter wording \u2014 `find_gpu_type` has no region filter; pod-create is the gate (correctness-4); (g) reordered consumer phases so `verify_extracted_env` runs AFTER `sync_worker_ref`/`sync_vibecomfy_ref`, catching partial-sync state (callers-2); (h) made probes crash-resistant via `_execute(..., check=False)` + diagnostic strings instead of raising on non-zero exit (correctness-5); (i) corrected cross-repo import direction \u2014 `prune_pods_by_prefix` lives in new `runpod_lifecycle.guard`; `terminate_guard.py` delegates to it; runpod-lifecycle never imports reigh-worker (correctness-6); (j) committed the `_register_fresh_worker_record` \u2192 `register_worker_record(..., variant_label=...)` rename and confirmed shared argparse flags (`--backend`, `--worker-profile`, etc.) are inherited by the prebuilt variant (scope-1/callers-3); (k) added single-line variant_update coexistence guard that refuses when a prebuilt manifest is present (scope-2); (l) enumerated the three regex patterns in `terminate_guard.py` with the shared `%Y%m%dT%H%M%SZ` timestamp suffix (all_locations-2); (m) preserved test-import compatibility via re-exports of `_phase`/`_redact_sensitive_text`/`_capture_and_redact_noisy_lifecycle_output` from `variant_fresh.py` (all_locations-3); (n) updated `config.py:__all__` to export new prebuilt constants (all_locations-4); (o) reverted the rev 2 default-flip \u2014 `--variant fresh` remains the argparse default; `--variant auto` is opt-in and recommended via committed skill/docs (issue_hints-2); (p) added a cheap read-only `vibecomfy.cli nodes verify` probe that runs every prebuilt bootstrap, providing node-schema validation regardless of lockfile drift (issue_hints-3); (q) made the product call on model warming: accept first-run cold download as v1 scope; `rl prebuilt warm-models` deferred to v2 with explicit tracking (issue_hints-1/FLAG-008); (r) parameterized `_print_dry_run_plan` to honor the variant's venv_path and python_version (callers-1).",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "FLAG-018",
    "concern": "Step 6.4 says 'new module runpod-lifecycle/src/runpod_lifecycle/guard.py', but that file ALREADY EXISTS (127 lines) and exports `PodGuard` + `install_signal_handlers` (re-exported from __init__.py:15). The plan must EXTEND the existing module rather than create a new one; ambiguous wording could cause an executor to overwrite PodGuard.",
    "evidence": "runpod-lifecycle/src/runpod_lifecycle/guard.py:1-127 already defines class PodGuard; runpod-lifecycle/src/runpod_lifecycle/__init__.py:15 re-exports `PodGuard, install_signal_handlers` from .guard.",
    "status": "accepted_tradeoff",
    "severity": "significant"
  },
  {
    "id": "FLAG-019",
    "concern": "No worker source bundle: Step 6.3 bundles only venv.cuda124.tar.zst and vibecomfy.tar.zst. There is no worker source bundle, so Step 8.3 sync_worker_ref's 'treat the bundle's worker tree as a starting point' wording is incorrect \u2014 `ensure_git_ref_synced` must full-clone the worker repo on first run. Plan should either bundle the worker tree (cheap, ~MBs) or correct the wording so executors don't expect a non-existent dir.",
    "evidence": "Step 6.3 bundle_artifacts produces only the two named bundles; Step 8.3 phase reads 'bundle's worker tree as a starting point'.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-020",
    "concern": "Bind_models_dir clobber/merge semantics undefined. The extracted vibecomfy bundle may contain a builder-pod-local extra_model_paths.yaml whose paths point at non-existent dirs on the consumer pod. Plan does not specify whether the consumer overwrites or merges the file at runtime.",
    "evidence": "Step 8.3 bind_models_dir writes extra_model_paths.yaml at runtime_vibecomfy_path; no clobber/merge contract.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-021",
    "concern": "Node-schema verify probe depends on a vibecomfy.cli subcommand that may not exist. Assumption #9 acknowledges 'either already exists or is a trivial read-only addition'. Open question #3 explicitly defers verifying its existence. Plan should enumerate adding the subcommand to vibecomfy as a touched file or specify a hard fallback probe (template_index count + sanity), not both as a choice deferred to implementation time.",
    "evidence": "Step 2.4(d) requires `vibecomfy.cli nodes verify`; assumption #9; open question #3.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-022",
    "concern": "`_build_worker_env` extraction not enumerated. Step 8.4 says variant_prebuilt._build_worker_env wraps a `_shared._build_worker_env_base`, but Step 5.1's extraction list omits `_build_worker_env`. Without moving (or duplicating) the base function into _shared, variant_prebuilt cannot wrap it.",
    "evidence": "Step 5.1 extracted symbols list (no _build_worker_env); Step 8.4 implies _shared._build_worker_env_base exists; variant_fresh.py:103-130 currently holds the function.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-023",
    "concern": "_finalize_args (main.py:115-132) currently does variant-specific normalization (backend+namespace overrides). Plan does not specify whether `--variant prebuilt` triggers the same normalization path. Without explicit handling, prebuilt runs may use the literal `production` selector namespace where fresh would switch to a dated namespace.",
    "evidence": "reigh-worker/scripts/live_test/main.py:115-132 _finalize_args; Step 9.3 enumerates new flags but not _finalize_args branch for prebuilt.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-024",
    "concern": "Multi-region build cost is linear in regions with no sharing. Operators paying ~67 min \u00d7 N regions on each hard-fail invalidation (schema_version/bundle_format_version/python_version/cuda_extra). Acceptable for v1 but worth noting as a scaling constraint \u2014 a future improvement might ship pre-built tar.zst across regions via S3-style replication.",
    "evidence": "Step 7.1 'one per region they want covered'; assumption #3.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-025",
    "concern": "verify_extracted_env returns list[str] but consumer aggregation behavior is unspecified. If 3+ probes fail simultaneously (truncated venv \u2192 torch import fails + size deviation + node-schema fail), the operator should see all reasons in the diagnostic raise. Plan does not specify join-vs-first-only semantics.",
    "evidence": "Step 2.4 returns list of issues; Step 8.3 raises 'with a numbered diagnostic'.",
    "status": "open",
    "severity": "minor"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 11,
    "verified": []
  },
  {
    "iteration": 2,
    "flag_count": 12,
    "verified": [
      "FLAG-001",
      "FLAG-002",
      "FLAG-003",
      "FLAG-004",
      "FLAG-005",
      "FLAG-006",
      "FLAG-007"
    ]
  },
  {
    "iteration": 3,
    "flag_count": 11,
    "verified": [
      "FLAG-009",
      "FLAG-010",
      "FLAG-011",
      "FLAG-012",
      "FLAG-013",
      "FLAG-014",
      "FLAG-015",
      "FLAG-016",
      "FLAG-017"
    ]
  }
]

        Debt watch items (do not make these worse):
        [
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: for ordinary pairs, the new diagnosis is not well-supported by the repo. the current sync effect in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l62) already syncs `url` and `primaryvariantid`, and the regenerate path reads exactly `starturl`, `endurl`, `startgenid`, `endgenid`, `startvariantid`, and `endvariantid` from `segmentslotmode.pairdata` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/usevideoregeneratemode.ts#l438). adding `thumburl` and `generationid` to the sync does not, by itself, explain why an old image url is still being used for regular pairs. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the fix is incomplete for extra trailing slots. `handlepairclick` can populate `activepairdata` from `trailingpairdata` when `pairindex === pairdatabyindex.size` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotmode.ts#l121), but the proposed sync effect only reads `pairdatabyindex.get(segmentslotlightboxindex)`. for those trailing-slot cases `fresh` is `undefined`, so no image refresh happens. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the merge pseudocode does not actually sync 'all image fields' as claimed. it omits `id` and `position` from change detection, and when `fresh.startimage` or `fresh.endimage` becomes `null` it preserves the stale previous object instead of syncing that null state. as written, it also needs explicit null-guards around spreads of `prev.startimage` / `prev.endimage` to be safe in strict typescript. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the plan's claim that `worker_state.py:200-204` (the 30-minute startup safety net) catches abandoned pods that exited before patching is slightly imprecise. line 200-204 only runs when `in_startup_phase` is true, which requires `startup_phase` to be in `('deps_installing', 'deps_verified', 'worker_starting')` per line 161. a pod that exits before its first patch has `startup_phase = none`, so `in_startup_phase` is false and the code falls through to the normal timeout checks (active_stale / not_claiming) at line 207+, not the 30-minute startup cap. both paths eventually reap the worker, so the end result is the same, but the overview's reasoning (naming 200-204 specifically) is wrong. worth correcting so future readers don't mis-reason about the invariant. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: checked worker_state.py line 161 (`in_startup_phase = startup_phase in (...)`) against the plan's assumption that subsequent lenient writes are safe. if deps_installing succeeds but deps_verified silently fails, startup_phase stays at 'deps_installing' and the 30-minute cap from line 200-204 applies \u2014 even though the pod is actually progressing through `uv sync`. on a slow runpod image with cold wheel downloads, `uv sync --extra cuda124` plus wan2gp deps can take 20+ minutes. there's no concrete benchmark in the plan that says the 30-minute cap is safely above the expected sync time; if `uv sync` legitimately takes 25 minutes and the deps_verified patch fails on a transient network blip, the orchestrator will terminate a healthy pod. plan should either bump the cap or note that deps_verified swallowing is acceptable because the cap is generously above typical sync time. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the path-mapping defect from the previous iteration is fixed, but a different technical gap remains around `self_refiner`. repository search shows `shared.utils.self_refiner` is imported by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx_pipelines/distilled.py`, `ti2vid_one_stage.py`, `ti2vid_two_stages.py`, `wan2gp/models/ltx2/ltx_pipelines/utils/helpers.py`, and `wan2gp/models/wan/any2video.py`; the v4 plan still aligns `wan2gp/shared/utils/self_refiner.py` to upstream head without any concrete runtime step that exercises those code paths after the change, so the only repo-documented behavior check for that file is still missing from the executable body. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: the direct adapter still has a correctness risk around resolution parity. current vibecomfy ready templates hardcode image dimensions (`image/z_image` uses `emptysd3latentimage` 1024x1024 and `image/qwen_image_2512` uses 768x768), while `vibecomfy run` exposes no `--resolution` flag; the revised plan says a temporary scratchpad/input file may be generated only if supported, otherwise resolution is left out. that means a vibecomfy-supported direct route can silently ignore the worker's `resolution` param unless scratchpad resolution patching is made mandatory for supported direct routes or the support is explicitly limited to default-resolution smoke fixtures. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: route support states: the revised step 5 says to classify ltx control rows as vibecomfy_supported, wgp_only, vibecomfy_unsupported, new, or blocked, but the current worker routesupportstate enum at reigh-worker/source/task_handlers/tasks/template_routing.py:17-20 only supports wgp_only, vibecomfy_supported, and vibecomfy_unsupported. the plan needs to either extend the enum/report schema for new/blocked or keep new/blocked strictly as fixture disposition values mapped to an existing runtime support state. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: startup tests: step 11 still needs sharper wording for `vibecomfy_memory_profile`. the current startup template exports it only inside `if [ \"$reigh_backend\" = \"vibecomfy\" ] && [[ \"$reigh_worker_profile\" =~ ^[0-9]+$ ]]` at worker_startup.template.sh lines 28-30, while the revised plan says to assert it is exported consistently when proving both wgp and vibecomfy render from the same template. if implemented as an unconditional wgp+vibecomfy export assertion, the test would conflict with the current template's intentional conditional behavior. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: step 6.4 says 'new module runpod-lifecycle/src/runpod_lifecycle/guard.py'. that module already exists (127 lines) and houses `podguard` (re-exported from __init__.py:15 as `podguard, install_signal_handlers`). the plan must extend the existing module by adding `prune_pods_by_prefix`, not create a new one. as worded an executor could create a duplicate file or overwrite the existing podguard. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: step 8.3 sync_worker_ref operates on `/opt/reigh-livetest-prebuilt/worker` and `ensure_git_ref_synced` it to `args.ref`. but there is no worker bundle: step 6.3 produces only `venv.cuda124.tar.zst` and `vibecomfy.tar.zst`. the builder clones reigh-worker to `/opt/build/reigh-worker` and never bundles it. on first consumer run the worker dir does not exist at `/opt/reigh-livetest-prebuilt/worker`, so `ensure_git_ref_synced` must full-clone. the plan's wording 'we treat the bundle's worker tree as a starting point' is incorrect; there is no worker tree in the bundle. this works functionally (git clone is cheap) but the description is misleading. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: step 8.3 bind_models_dir writes `extra_model_paths.yaml` at `runtime_vibecomfy_path` on every consumer run. the extracted vibecomfy.tar.zst may already contain a different `extra_model_paths.yaml` from the builder's build environment. the plan does not specify clobber vs merge semantics. a baked-in path that points at builder-pod-local cache directories would conflict with the consumer's volume-hosted models/ tree. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: step 6.5 fallback for cross-repo imports: 'if runpod-lifecycle cannot import reigh-worker code, replicate the helper as runpod_lifecycle.guard.prune_pods_by_prefix(prefixes, ...) and have terminate_guard.py delegate to it'. runpod-lifecycle is a standalone package with no reigh-worker dependency \u2014 the import direction is reigh-worker \u2192 runpod-lifecycle, not the reverse. the replicate-helper fallback is the only correct option; the import-from-reigh-worker primary branch is wrong by repo structure. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: step 4 parameterizes `build_run_worker_command` to take `venv_path`. the hardcoded `--python 3.10` at launch_command.py:43-44 is not parameterized. if the prebuilt manifest's python_version is 3.11 (the runpod base image at config.py:91 is `py3.11-cuda12.4.1`), the worker is launched with a 3.10 uv interpreter while the prebuilt venv was created for 3.11. this is the same class of mismatch the python_version invalidation rule is supposed to catch but does not, because launch_command never reads the manifest python_version. (flagged 1 times across 1 plans)",
  "[DEBT] are-the-success-criteria-well-prioritized-and-verifiable: are the success criteria well-prioritized and verifiable?: the attached success criteria are stale and do not match the current plan body. they still require 'no `usestate` for `activepairdata`', '`setactivepairdata` fully removed', 'sync effect deleted', and '`onpairclick` simplified to `(pairindex: number) => void`', which are the opposite of the current targeted-sync plan. as presented, the criteria are not usable for review or execution. (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: getaudiodata in useeffect removes render-readiness signal (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: same as correctness-3 \u2014 preview/render parity risk (flagged 1 times across 1 plans)",
  "[DEBT] audio-loading: preview/render parity partially satisfied (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: overlapping clips use first-found, volume not scaled (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: same as audio-reactivity-1 \u2014 overlapping/volume-adjusted clips diverge from audible mix (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: textclip missing globalframeprovider (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: same as audio-reactivity-2 \u2014 textclipsequence missing provider (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: textclip effects surface not covered (flagged 1 times across 1 plans)",
  "[DEBT] audio-reactivity: continuous effects shared by visual and text clips (flagged 1 times across 1 plans)",
  "[DEBT] batch-generation-pipeline: enhancement in usegeneratebatch before generatevideo() could compute prompts against a stale pair snapshot if mutations are still in flight. (flagged 1 times across 1 plans)",
  "[DEBT] cas-intern-short-circuit: symlink short-circuit comparison may produce false negatives on macos-like layouts where project_dir contains symlinked segments (/var \u2192 /private/var) because resolve(strict=true) on the source returns canonical paths but project_dir / cas_dirname may be non-canonical. (flagged 1 times across 1 plans)",
  "[DEBT] completeness-model-cache: model-cache reuse is not part of the prebuilt contract for first-encounter workflows (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: cascade lookup only reads params->>'orchestrator_task_id_ref', missing shared reference paths and orchestrator-self detection. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: duplicate of correctness-2 + correctness-3: invalid sql syntax and narrow cascade lookup. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: shared orchestrator-reference helpers not referenced. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: orchestrator tasks that crash don't get orchestrator-self cascade. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-cascade-paths: hardcoded params->>'orchestrator_task_id_ref' misses other reference paths. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: crash requeue sql does not increment attempts, risking infinite requeue loop. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: duplicate of correctness-1: attempts never advance on crash requeue. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: missing attempts increment location in heartbeat sql. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-retry: step 6 under-scoped for real retry convergence and orchestrator-self handling. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-sql-syntax: bare select inside plpgsql is invalid \u2014 needs perform. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: no multi-crash convergence test exercising attempts 0\u21921\u21922\u21923. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: no validation that plpgsql body executes successfully. (flagged 1 times across 1 plans)",
  "[DEBT] crash-recovery-testing: criteria don't require proof of crash requeue convergence. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: 'no unsafe .maybesingle()' criterion requires judgment about column uniqueness. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: decision documentation location not specified. (flagged 1 times across 1 plans)",
  "[DEBT] criteria-verifiability: the must criterion requiring 5 task types to exist as active db rows is not verifiable from code diff alone \u2014 it requires a live db query. (flagged 1 times across 1 plans)",
  "[DEBT] db-fallback-testing: no new automated test for the db fallback dispatch path or dependant_on preservation for raw worker families. (flagged 1 times across 1 plans)",
  "[DEBT] dependency-resolution: dependency resolution: the plan does not lock down the active python-version matrix even though the repo currently splits between python 3.10 local installs and a python 3.11 runpod image. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: the package is internally inconsistent. the plan body says to keep `activepairdata` in `usestate` and make phase 2 optional, but the attached metadata and success criteria still describe the previous derive-via-`usememo` / remove-`setactivepairdata` / simplify-`onpairclick` plan. that means the approved-plan requirements are only partially coherent as presented. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: the linux distro note is documentation-only; the generated install command in step 7 still runs `apt-get install python3.10-venv python3.10-dev ffmpeg` without any pre-check that the package exists. users on ubuntu 24.04+ who ignore the doc and try to copy-paste the command will hit a confusing `e: unable to locate package python3.10-venv` from apt rather than a targeted error from commandutils.ts. a one-line detection pre-check (e.g., `apt-cache show python3.10-venv >/dev/null 2>&1 || { echo 'install deadsnakes ppa first \u2014 see readme'; exit 1; }`) would convert the silent failure into an actionable error, but the plan does not add this. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: checked the revised v4 body against `docs/wan2gp_fork_migration_plan.md` sprint 2. the repo plan doc still lists an \"ltx-2 `self_refiner` smoke against the pre-sprint behavioral baseline\" as a sprint 2 verification gate and repeats that smoke in the functionality-preservation checks, but the revised execution steps no longer schedule that smoke anywhere; it survives only as an info-level metadata criterion. because `wan2gp/shared/utils/self_refiner.py` remains an explicit sprint 2 deliverable, the revised plan still only partially carries forward the verification package described in the source migration plan. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: worker integration: the migration doc describes the per-call profile override gap as involving reigh-worker adapter handling of override_profile before constructing vibecomfy sessionconfig, but the plan limits sprint 1 per-run work to the vibecomfy cli/runtime. that may be acceptable for a vibecomfy-library mvp, but it does not fully exercise the production-facing per-task override semantics called out in the overall context. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: a residual issue-hint tension remains for resolution handling. the plan acknowledges current `vibecomfy run` lacks a resolution flag, but allows the adapter to leave resolution and other template-specific values unwired for sprint 2. because `z_image_turbo` and `qwen_image_2512` are marked vibecomfy-supported direct routes, this may not preserve the existing worker task-parameter contract for tasks that provide a non-default `resolution`. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: model warming is explicitly deferred to v2 (assumption #6). the idea text demands the new path 'reach workflow execution materially faster than the cold fresh path'. v1 meets this for deps (67 min \u2192 ~10 min) but a first-encounter workflow still incurs a 10-50gb hf download. the success criterion for run b model reuse depends on run a having performed that download. plan accepts this tradeoff openly via open question #1 \u2014 flagging because the idea's 'reusable validation environment' framing could be read as covering models too. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: node-schema validation (issue_hints-3) is wired via a `vibecomfy.cli nodes verify` probe (step 2.4d, step 8.3), but assumption #9 admits the subcommand 'either already exists or is a trivial read-only addition'. the plan does not enumerate adding it to the vibecomfy repo as a planned change. if it does not exist, the executor either silently no-ops the probe (false success) or adds a vibecomfy patch that is out of the stated touchpoints. open question #3 explicitly defers verifying its existence. (flagged 1 times across 1 plans)",
  "[DEBT] direct-route-parameter-parity: direct route parameter parity: vibecomfy-supported direct routes may ignore the worker `resolution` parameter. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: phase 1 still misses a real supporting-data location: `trailingpairdata` lives outside `pairdatabyindex` in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/usesegmentslotpresentationadapter.ts#l111), but the proposed sync logic only considers `pairdatabyindex`. if trailing slot regenerate is part of the bug surface, that location is not covered. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the non-swallowing helper `update_worker_phase_strict` is a new shell function, but phase 1 step 2 introduces it only as pseudo-code. there is no concrete note that the helper must handle supabase http non-2xx responses as failures (curl returns 0 even on http 4xx/5xx by default unless `-f` or `--fail-with-body` is used). if the implementer ports `update_worker_phase` verbatim with only `|| return 0` removed, a 500 from supabase would still report success because curl's exit code is 0. the plan should specify `curl --fail` or explicit http status code checking in the strict variant. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the supporting-infrastructure review still finds one missing check. in `docs/wan2gp_fork_migration_plan.md`, sprint 2's verification matrix and risk register both single out `self_refiner` as a distinct drift-upgrade surface with its own smoke and its own silent-behavior-change risk, but the revised v4 body updates the file without keeping that supporting verification step in the actual execution checklist. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: documentation/data gap: the sprint exit criteria require profiles 1 and 3 to have vram and wall-clock data, but the plan puts that only in metadata as an info-level criterion and does not schedule a concrete artifact location or command for recording the measurements. the implementation could satisfy all unit tests while still missing one of the explicit exit criteria. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: the supporting infrastructure for resolution is still incomplete if direct vibecomfy routes are considered production-supported. vibecomfy has a `vibecomfy.patches.resolution` helper and the cli can load scratchpad files with `allow_scratchpad=true`, but the plan does not require using that path; it permits leaving resolution out for sprint 2. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: checked vibecomfy profile wording against `vibecomfy/tests/test_ready_templates.py`. the revised plan says to add the production template to representative compile profile coverage 'alongside the existing dry-run id', but the dry-run id is not currently in `profile_smoke_template_ids`; only `video/wanvideo_wrapper_22_5b_i2v` and `video/wan_t2v` are. this is a small wording mismatch rather than a functional blocker because adding either the production id alone or both ids would still satisfy sprint 4. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: plan enumerates `runpod-lifecycle/src/runpod_lifecycle/guard.py` as a touched file but describes it as 'new'. should be marked as 'extend existing'. the associated `__init__.py:15` re-export line will need `prune_pods_by_prefix` added \u2014 not listed in the touchpoints. minor but enumerated. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: step 8.4 `variant_prebuilt._build_worker_env` wraps a `_shared._build_worker_env_base`. but `_build_worker_env` currently lives in `variant_fresh.py:103-130` and is not in the step 5.1 extraction list (`_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`, `select_network_volume`, `register_worker_record`). the plan implies but does not enumerate moving/refactoring `_build_worker_env` into `_shared.py` as a base helper. without that, variant_prebuilt's hf_home-extending wrapper has nothing to wrap. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: step 10.2 regex tuple uses `re.escape(prefix)` \u2014 fine \u2014 but the timestamp suffix `(\\d{{8}})t(\\d{{6}})z` is lowercase 't' and 'z'. the actual `_timestamp_label()` at variant_fresh.py:73-74 emits `'%y%m%dt%h%m%sz'` (uppercase t, z), and existing _fresh_pod_name_re at terminate_guard.py:16 uses lowercase t,z because the function does `.lower()` on the pod name before regex match (likely \u2014 need to verify). the plan's regex inline format is plausible but not verified against the existing pattern; if the existing regex assumes case-folded input, the tuple must follow the same convention. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: step 7.4 lists new `__all__` exports for config.py but the helper `prebuilt_name_for_profile(profile, data_center_id)` defined in step 7.2 actually lives where? plan says config.py exposes the helper. that mixes runtime logic (function definition) into config.py, which currently holds only constants + loader (`_load_runpod_defaults`, `load_fixture_json`). placing the helper there is fine but breaks the current naming convention where computed helpers live in their own modules. minor consistency concern. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: plan's vitest commands use the wrong config entry point. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: same as verification-3: wrong vitest config in validation commands. (flagged 1 times across 1 plans)",
  "[DEBT] edge-test-config: success criterion references wrong test command. (flagged 1 times across 1 plans)",
  "[DEBT] error-handling: db loader error handling convention mismatch (plan says log+null, existing loaders throw) (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-logging: generation.ts and handler.ts logging endpoints are not directly tested. (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: no end-to-end regression test for the full symptom chain (db error \u2192 tocompletionerror metadata \u2192 handler log). (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: handler.ts metadata surfacing criterion lacks a concrete automated verifier. (flagged 1 times across 1 plans)",
  "[DEBT] error-propagation-testing: main issue only partially validated without an integration test. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: the step 2 retry loop uses a naked `sleep 2` between attempts, which adds up to 6 seconds of latency on the happy path when the first patch eventually succeeds on attempt 2 or 3. for pods where supabase is reachable but slow during the initial moments of a cold runpod start, the retry logic is fine. however, if the first attempt fails with a tls handshake delay and the retry loop sleeps 2s per attempt regardless of whether curl itself has been blocking for tens of seconds, the total startup latency penalty could be substantial. this is a minor tuning concern, not a correctness issue. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: finding callers of the changed module shows that `shared.utils.self_refiner` is consumed by `wan2gp/wgp.py`, `wan2gp/models/ltx2/ltx2_handler.py`, multiple ltx2 pipeline modules, and `wan2gp/models/wan/any2video.py`. the revised validation steps still only drive the three bridge getters in `source/runtime/wgp_ports/vendor_imports.py`; none of the scheduled commands execute a real `self_refiner` caller, so the plan does not yet verify the main caller shapes for the other explicit sprint 2 file change. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked direct queue caller values in `db_task_to_generation_task()`: direct image tasks may carry `resolution`, `steps`/`num_inference_steps`, `seed`, and `override_profile`. the revised adapter plan covers seed, steps, and memory profile but not guaranteed resolution propagation, so it does not handle all relevant direct-route caller arguments for a supported vibecomfy direct route. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: step 5.2 `register_worker_record(..., variant_label: str)` reads `args.backend`, `args.worker_profile`, `args.selector_namespace`, `args.selector_version`, `args.worker_contract_version`. step 9.3 says the prebuilt variant inherits the shared parser. variant_fresh's `_finalize_args` at main.py:115-132 also performs variant-specific normalization (e.g. when `args.backend == 'vibecomfy' && args.selector_namespace == 'production'`, switches to `_live_test_selector_namespace()`). the plan does not enumerate whether `_finalize_args` runs for `--variant prebuilt` too. if it doesn't, prebuilt runs against production selector namespace by default \u2014 different behavior than fresh. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: callers of `_uv_sync_shell` (new in step 3.1): only `run_install` wraps it (`extras=('cuda124',)`, `with_locked=false`). variant_update.py:69-79 has a separate `remote_uv_sync` that uses `--locked`. plan does not migrate variant_update's remote_uv_sync to call `_uv_sync_shell(..., with_locked=true)` \u2014 variant_update stays untouched per assumption #4. so the new `with_locked` parameter has no caller. minor but adds unused api surface. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: callers of `extract_bundle_to_container_disk` (new in step 3.3): only variant_prebuilt invokes it. the target_path defaults to existing /opt/reigh-worker-live-test-venv (matches the bundled venv's original absolute path so internal symlinks remain valid). plan does not specify behavior if target_path is non-empty (e.g. operator re-extracts on the same pod after a prior consumer run). default tar behavior overwrites; if `--keep-newer-files` semantics are wanted to avoid clobbering operator-modified files, plan should call it out. probably correct as-is for the ephemeral pod use case. (flagged 1 times across 1 plans)",
  "[DEBT] gpu-branching-test-matrix: linux cuda128 path under-verified (flagged 1 times across 1 plans)",
  "[DEBT] gpu-branching-ui-surface: nvidia-50 option is exposed on linux in the ui but linux cuda128 smoke test is missing (flagged 1 times across 1 plans)",
  "[DEBT] hook-abstraction: usepairsettingshandler becomes trivial with single caller \u2014 keeping it is extra indirection. (flagged 1 times across 1 plans)",
  "[DEBT] hype-mirror-cas-coverage: hype-mirrored files whose parent step does not declare matching produces will not be cas-interned, even with the follow_symlinks=false edit. (flagged 1 times across 1 plans)",
  "[DEBT] is-the-change-in-the-right-place-and-would-it-break-any-callers: is the change in the right place, and would it break any callers?: the optional cleanup steps are not in the right place yet. `pairregionslayer` does not receive `pairdatabyindex` today; its props are only `images`, `imagepositionswithpending`, `pairinfowithpending`, and callback/display props in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/timeline/timelinecontainer/components/pairregionslayer.tsx#l20). so step 4's 'pass `pairdatabyindex.get(pairindex)` directly' would require new prop plumbing or a different seam. (flagged 1 times across 1 plans)",
  "[DEBT] is-the-scope-and-scale-of-the-change-appropriate: is the scope and scale of the change appropriate?: phase 2 is still under-specified for execution. step 4 says pairregionslayer should either pass `pairdatabyindex.get(pairindex)` directly or 'just pass the index + frame-only data', which are materially different designs. if phase 2 is kept in the plan, it needs a single concrete direction. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: the plan still lacks an explicit automated regression test for the reported bug. step 2 is manual ('check that `usevideoregeneratemode` now gets the fresh url'), but there is no concrete test that opens a segment slot, changes the primary variant data, and asserts that the regenerate path sees the fresh `url`, `generationid`, and `primaryvariantid`. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: the current `usesegmentslotmode` test remains only a smoke test in [/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts](/users/user_c042661f/documents/reigh-workspace/reigh-app/src/tools/travel-between-images/components/shotimageseditor/hooks/__tests__/usesegmentslotmode.test.ts), and the plan does not add behavior coverage for the new sync effect. (flagged 1 times across 1 plans)",
  "[DEBT] is-there-convincing-verification-for-the-change: is there convincing verification for the change?: no verification step covers the trailing-slot branch, even though the proposed phase 1 logic currently misses `trailingpairdata` refreshes. (flagged 1 times across 1 plans)",
  "[DEBT] legacy-data-backfill: the step 8 diagnostic query only detects cross-shot pair_shot_generation_id misassociations, not same-shot misassociations caused by timeline reordering within a shot. (flagged 1 times across 1 plans)",
  "[DEBT] lookup-consistency: other repo call sites use unordered .limit(1).maybesingle() and will remain inconsistent. (flagged 1 times across 1 plans)",
  "[DEBT] lookup-consistency: other call sites with same unsafe pattern not covered. (flagged 1 times across 1 plans)",
  "[DEBT] lora-management: lora tools simplified vs full ui parity (multi-stage metadata, private loras) (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-persistence: variant switches do not clear/restore inpaintprompt, so stale prompt state can leak across variants with no cached prompt. (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-persistence: removing prompt/numgenerations from the variant-keyed localstorage cache means all variants within a generation share the same prompt. this broadens existing debt-002 (variant prompt leakage). (flagged 1 times across 1 plans)",
  "[DEBT] media-lightbox-segment-slot: media lightbox / segment slot: the targeted sync rationale does not fully explain the reported stale-url bug for regular pairs, and the proposed effect still misses trailing-slot refreshes because those can come from `trailingpairdata` rather than `pairdatabyindex`. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: plan doesn't explicitly state onchange must also accept null, though step 3 depends on it. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: disputed v1 flag \u2014 original concern about bulkclippanel being unimplementable. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-nullable: onchange null filtering not explicitly addressed in plan. (flagged 1 times across 1 plans)",
  "[DEBT] number-input-testing: no planned tests for numberinput shared component or bulkclippanel nullable draft flow. (flagged 1 times across 1 plans)",
  "[DEBT] operational-ceiling: per-region builder cost is linear (4\u00d7 for 4 regions) (flagged 1 times across 1 plans)",
  "[DEBT] operator-discovery: --variant default stays fresh; auto is opt-in (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: pre-existing individual_travel_segment children won't drive orchestrator completion through segment_type_config after deploy. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: missing compatibility seam in orchestratorcore.ts:123-126 for old individual_travel_segment rows. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: mixed old/new data during rollout can leave old orchestrators without completion counting. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: no test or deployment guard for pre-existing individual_travel_segment children completing after worker change. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: plan overstates backward compatibility for existing data. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: missing rollout compatibility step for in-flight individual_travel_segment tasks. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: pre-deploy individual_travel_segment child completing post-rollout won't be treated as segment task by checkorchestratorcompletion. (flagged 1 times across 1 plans)",
  "[DEBT] orchestrator-completion-rollout: orchestrator.test.ts criterion too narrow to verify old individual_travel_segment compatibility. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: handleopenpairsettings(pairindex, pairframedata) path in timelinetrackprelude, segmentoutputstrip, and usesegmentoutputstrip not explicitly named. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: same as flag-002 \u2014 segmentoutputstrip and usesegmentoutputstrip still carry pairframedata. (flagged 1 times across 1 plans)",
  "[DEBT] pair-settings-plumbing: timelinetrackprelude and segmentoutputstrip still forward (pairindex, pairframedata). (flagged 1 times across 1 plans)",
  "[DEBT] performance: moosefs staging-stream throughput unbenchmarked (flagged 1 times across 1 plans)",
  "[DEBT] plan-scope: step 3 is larger than a light megaplan warrants. (flagged 1 times across 1 plans)",
  "[DEBT] planning-metadata: planning metadata: the attached metadata and success criteria still describe a different implementation than the current plan body, which risks sending execution and review down the wrong path. (flagged 1 times across 1 plans)",
  "[DEBT] planning-metadata: success criteria don't cover wave 4 scope (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: plan investigates a unique constraint on (parent_generation_id, child_order) which doesn't match repo semantics for position keys. (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: plan weights toward child_order rather than pair_shot_generation_id as the key that matters. (flagged 1 times across 1 plans)",
  "[DEBT] position-key-semantics: unique constraint on (parent_generation_id, child_order) not supported by repo semantics. (flagged 1 times across 1 plans)",
  "[DEBT] prompt-composition: the plan's step 1 signature includes textbeforeprompts/textafterprompts parameters that would be applied before enhancement, double-wrapping the prompt. (flagged 1 times across 1 plans)",
  "[DEBT] python-version: fresh path uses uv-managed py3.10 while prebuilt uses base-image py3.11 \u2014 different interpreter sources (flagged 1 times across 1 plans)",
  "[DEBT] ready-template-snapshots: step 4.2 drops markdownnote nodes but step 4.5 and the success criteria require class_type/widget parity with pre-refactor snapshots, which currently include markdownnote nodes. (flagged 1 times across 1 plans)",
  "[DEBT] ready-template-snapshots: same tension as issue_hints v2: drop-markdownnote vs. snapshot parity. (flagged 1 times across 1 plans)",
  "[DEBT] reigh-worker-orchestrator-dockerfile: step 7 \u00a73 claims `gpu_orchestrator/dockerfile` has wan2gp install steps; current main is generic and contains none. (flagged 1 times across 1 plans)",
  "[DEBT] reigh-worker-orchestrator-runpod-startup: `gpu_orchestrator/runpod/startup_script.py` embeds `headless-wan2gp` in `_workdir_discovery_snippet` and is not named explicitly in step 7 \u00a73's checklist. (flagged 1 times across 1 plans)",
  "[DEBT] route-support-states: route support states: new and blocked are added to the plan as worker support classifications but are not representable in the current routesupportstate enum. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the broader runtime surface after the v4 path fix. sprint 2 is still moving two behavior-sensitive seams rather than just the import-path contract: the `wan2gp/` mount path and the `self_refiner` runtime. step 6.2 covers only the three `vendor_imports` getters, while the 6-file travel suite and the bridge-contract tests do not mention `self_refiner`, so dropping the dedicated self-refiner smoke from the runnable steps leaves the broader downstream surface of that changed file under-covered. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: the supported direct-route scope is still broader than the adapter's guaranteed parameter surface. `db_task_to_generation_task()` currently carries direct task params such as `resolution`, `steps`, and `seed` into wgp generation, but the vibecomfy cli path only guarantees prompt, seed, steps, and memory profile; resolution remains optional/documentation-only in the plan. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: checked the revised child-route scope against `migration-thresholds.yaml`. the threshold corpus currently has wan/vace entries for `travel_segment__model-wan22_vace__...` and `join_clips_segment__model-wan22_vace__...`, but only an i2v entry for `individual_travel_segment`; the revised plan makes `individual_travel_segment` with vace model params a must-level worker fixture, which broadens the worker smoke scope beyond the currently tracked wan/vace threshold routes. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: step 11 variant_update coexistence guard refuses when `/workspace/reigh-livetest-prebuilt/env.manifest.json` exists. but variant_update has two modes: `--pod-id` (attaching to an existing pod) and `--spawn-takeover` (spawning a fresh orchestrator-managed pod). the spawn-takeover path would create a pod with the prebuilt volume attached and then immediately fail the guard, even though the operator just spawned it. this is correct behavior (we don't want update to mutate the prebuilt cache) but the operator-facing message should mention that --spawn-takeover is also blocked, not just --pod-id. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: verify_extracted_env (step 2.4) returns `list[str]`, but step 8.3 says the consumer raises when issues are non-empty. plan does not specify whether multiple issues are concatenated into one message or only the first surfaces. the diagnostic ux matters when 3+ probes all fail (e.g. truncated venv triggers torch import fail, size deviation, and node-schema verify fail \u2014 operator should see all three reasons, not just one). (flagged 1 times across 1 plans)",
  "[DEBT] self-refiner-verification: self-refiner verification: the revised plan still aligns `wan2gp/shared/utils/self_refiner.py` without scheduling the sprint 2 ltx-2 `self_refiner` smoke that `docs/wan2gp_fork_migration_plan.md` defines as the behavior-preservation check for that drift upgrade. (flagged 1 times across 1 plans)",
  "[DEBT] settings-defaults: workerrepopath default can go stale if user switches computertype before editing path (flagged 1 times across 1 plans)",
  "[DEBT] settings-resolution: settings cascade missing \u2014 shot-only read diverges from form's defaults\u2192user\u2192project\u2192shot merge (flagged 1 times across 1 plans)",
  "[DEBT] settings-resolution: settings cascade missing \u2014 shot-only read (flagged 1 times across 1 plans)",
  "[DEBT] shared-component-compatibility: numberinput changes affect callers outside video-editor (billing, travel-between-images, phaseconfigselectormodal). (flagged 1 times across 1 plans)",
  "[DEBT] shared-component-compatibility: shared ui component blast radius not audited in plan. (flagged 1 times across 1 plans)",
  "[DEBT] shot-linking-testing: no test covers the linkgenerationtoshot error/catch branches. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: plan doesn't explicitly name timeline/index.tsx and segmentslotcontracts.ts for updates. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: same as flag-001 \u2014 timeline/index.tsx and segmentslotcontracts.ts not in checklist. (flagged 1 times across 1 plans)",
  "[DEBT] signature-propagation: five supporting contract/plumbing sites not named in the checklist. (flagged 1 times across 1 plans)",
  "[DEBT] step-6-4-says-new-module-runpod-lifecycle-src-runpod-lifecycle-guard-py-but-that-file-already-exists-127-lines-and-exports-podguard-install-signal-handlers-re-exported-from-init-py: step 6.4 says 'new module runpod-lifecycle/src/runpod_lifecycle/guard.py', but that file already exists (127 lines) and exports `podguard` + `install_signal_handlers` (re-exported from __init__.py:15). the plan must extend the existing module rather than create a new one; ambiguous wording could cause an executor to overwrite podguard. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: step 3 cites wrong migration file (task_cost_configs instead of task_types) as evidence for db fallback path. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: step 3 should cite task_types source, not task_cost_configs. (flagged 1 times across 1 plans)",
  "[DEBT] ta[REDACTED_SK]: plan doesn't verify travel_segment and travel_stitch exist as active task_types rows using the correct table. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: current generation-child.test.ts is only a smoke test. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no plan to verify other lookup paths choose rows consistently. (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no new tests for db loader or travel param merge path (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: must-level criteria depend on manual testing rather than automated assertions (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: no new unit tests for wave 4 tools (flagged 1 times across 1 plans)",
  "[DEBT] test-coverage: must criteria backed by manual testing only (flagged 1 times across 1 plans)",
  "[DEBT] test-infrastructure: no test fixtures for resources table (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: plan keeps two hooks instead of a single coordinator (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: brief says single coordinator but plan keeps separate hooks (flagged 2 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: pendingopsref retained despite brief suggesting removal (flagged 1 times across 1 plans)",
  "[DEBT] timeline-drag-coordination: wrapper-bound listener mount wiring under-specified (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: read path still assembles config and registry from separate requests (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: poll sync verification not structurally changed (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend save helpers not wired to new rpc (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: read infrastructure not updated (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend tests not in validation list (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend callers not migrated (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: broader persistence-contract problem (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: backend split-save not addressed (flagged 1 times across 1 plans)",
  "[DEBT] timeline-persistence: split polling can combine config and registry from different snapshots (flagged 1 times across 1 plans)",
  "[DEBT] timeline-scaling: the plan only specifies a concrete fix for the default scale(1) case; explicit-scale tracks may still break blend-mode effects. (flagged 1 times across 1 plans)",
  "[DEBT] timeline-snap-threshold: threshold is generous (duration) rather than zoom-scaled (8px) (flagged 1 times across 1 plans)",
  "[DEBT] timeline-snap-threshold: computedropposition does not pass a zoom-scaled threshold override (flagged 1 times across 1 plans)",
  "[DEBT] travel-continuations: smooth continuations not threaded \u2014 agent tasks won't have continuation_config even when shot settings enable it (flagged 1 times across 1 plans)",
  "[DEBT] travel-continuations: continuation_config omitted from form parity (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-cleanup-scope: plan scope narrower than original user request (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-cleanup-scope: broader create-task contract problem left untouched (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-readers: phase 4 app-side reader audit incomplete (flagged 1 times across 1 plans)",
  "[DEBT] travel-payload-readers: phase 4 field inventory incomplete for app-side readers (flagged 1 times across 1 plans)",
  "[DEBT] travel-request-contract: image_variant_ids is in frontend request contract (flagged 1 times across 1 plans)",
  "[DEBT] travel-request-contract: image_variant_ids contract change (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: spawn_worker does not internally call start_worker_process; harness must call both explicitly (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: worker_id and runpod_id must be generated and threaded distinctly; plan currently uses pod_id as both (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-1 \u2014 spawn_worker two-step misstatement (flagged 2 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-2 \u2014 worker_id/runpod_id propagation across takeover and restore paths (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-1 + correctness-2 \u2014 missing create_worker_record glue and start_worker_process integration (flagged 1 times across 1 plans)",
  "[DEBT] variant-update-b-fresh-takeover: duplicate of correctness-2 \u2014 caller contract for spawn_worker requires worker_id, not pod_id (flagged 1 times across 1 plans)",
  "[DEBT] verification: no end-to-end render test for audio analysis timing (flagged 1 times across 1 plans)",
  "[DEBT] verification: no automated coverage for text clips or overlapping clips with audio effects (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: no automated test exercises the full segment-slot opening path after cleanup. (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: no automated coverage that clicking a pair opens the correct modal after cleanup. (flagged 1 times across 1 plans)",
  "[DEBT] verification-coverage: zero behavioral change criterion is not verifiable from tsc + existing tests alone. (flagged 1 times across 1 plans)",
  "[DEBT] verification-workflow: tsconfig.app.json excludes test files, so tsc won't catch test breakage. (flagged 1 times across 1 plans)",
  "[DEBT] worker-test-staleness: worker test in test_additional_coverage_modules.py:37 may assert stale payload structure (task_type vs family). (flagged 1 times across 1 plans)",
  "[DEBT] workspace-state: plan checkpoint says the repo was clean, but current worker files may already be modified. (flagged 1 times across 1 plans)",
  "[DEBT] workspace-state: `tests/test_vibecomfy_adapter.py` is both locally modified and in scope for planned edits. (flagged 1 times across 1 plans)"
]

        Requirements:
        - Produce structured JSON only.
        - `tasks` must be an ordered array of task objects. Every task object must include:
          - `id`: short stable task ID like `T1`
          - `description`: concrete work item
          - `depends_on`: array of earlier task IDs or `[]`
          - `status`: always `"pending"` at finalize time
          - `executor_notes`: always `""` at finalize time
          - `reviewer_verdict`: always `""` at finalize time
          - `kind`: indicating the type of work. One of:
            - `code`: writes or modifies source files (executor must produce `files_changed`).
            - `test`: writes or modifies test files, or runs the test suite (executor must produce `files_changed` in tests/ OR `commands_run` containing pytest/test invocations).
            - `audit`: read-only investigation — grep, code review, schema inspection (executor evidence is `executor_notes` describing findings; no `files_changed` expected).
            - `research`: external research or non-code investigation (executor evidence is `executor_notes`).
            - `docs`: writes documentation files (executor must produce `files_changed`).
            If unsure, default to `code`.
        - `watch_items` must be an array of strings covering runtime risks, critique concerns, and assumptions to keep visible during execution.
        - `sense_checks` must be an array with one verification question per task. Every sense-check object must include:
          - `id`: short stable ID like `SC1`
          - `task_id`: the related task ID
          - `question`: reviewer verification question
          - `verdict`: always `""` at finalize time
        - `user_actions` must be an array of human-only setup or operational actions. Use IDs `U1`, `U2`, ... and include `description` plus `phase` (`before_execute` or `after_execute`). Use optional `blocks_task_ids` when an action blocks specific tasks, optional `rationale` when useful, and `requires_human_only_reason` ONLY when the user_action is the sole coverage for a plan step.
- Include ONLY actions that require a human outside the executor's repo-editing work: env vars or secrets, infra access such as cloud accounts or VPN, DB migrations the human must trigger, manual UI/UX smoke tests, deploys, and out-of-band approvals.
- Anything that touches code in the repo MUST be a task, not a user_action. Reading docs, editing files, running tests, and writing migration SQL are tasks. Negative example: writing the migration SQL is a task, not a user_action.
- Positive examples: `U1: Set ANTHROPIC_API_KEY in .env (before_execute)`; `U2: Manually smoke test the production deploy in the browser (after_execute)`.
        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
        - `validation` must be an object that self-checks plan coverage:
          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_item_ids` (array of task IDs `T*` or user_action IDs `U*` that implement or cover it — a single plan step may map to multiple tasks and/or user_actions).
          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task or user_action AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
          - Example:
          ```json
          "validation": {
            "plan_steps_covered": [
              {"plan_step_summary": "Add retry logic to API client", "finalize_item_ids": ["T1", "T2"]},
              {"plan_step_summary": "Set required production secret", "finalize_item_ids": ["U1"]}
            ],
            "orphan_tasks": [],
            "completeness_notes": "All plan steps mapped to tasks.",
            "coverage_complete": true
          }
          ```
        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
        - - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.

> TOOL

tool_use StructuredOutput
```json
{
  "$schema": "{\"tasks\":[{\"id\":\"T1\",\"description\":\"Create `runpod-lifecycle/src/runpod_lifecycle/prebuilt.py` exporting PrebuiltEnvContract (frozen dataclass with volume_name, data_center_id, mount_path=/workspace, cache_root={mount_path}/reigh-livetest-prebuilt, runtime_venv_path=/opt/reigh-worker-live-test-venv, runtime_worker_path=/opt/reigh-livetest-prebuilt/worker, runtime_vibecomfy_path=/opt/reigh-livetest-prebuilt/vibecomfy, models_path={cache_root}/models, attention_profile, comfyui_pin, python_version, bundle_format_version) and PrebuiltManifest (schema_version, bundle_format_version, built_at_utc, built_by, pyproject_hash, custom_nodes_lock_hash, comfyui_pin, attention_profile, python_version, cuda_extra='cuda124', vibecomfy_commit, reigh_worker_commit, uv_version, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes, notes — NO comfyui_bundle_sha256 field). Add compute_pyproject_hash, compute_lockfile_hash (SHA256 of canonicalized newline-normalized content), manifest_path(contract), lock_path(contract), staging_path(contract). Document invalidation precedence in module docstring: HARD-FAIL (schema_version, bundle_format_version, python_version, cuda_extra) requires `rl prebuilt build`; delta-sync (pyproject_hash, custom_nodes_lock_hash, comfyui_pin, vibecomfy_commit, reigh_worker_commit); no-op when all hashes match. Export all symbols from `runpod_lifecycle/__init__.py`.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T2\",\"description\":\"Extend `runpod-lifecycle/src/runpod_lifecycle/prebuilt.py` with SSH-side helpers: read_manifest(ssh, contract) -> PrebuiltManifest|None; write_manifest(ssh, contract, manifest) via heredoc + atomic mv; acquire_build_lock(ssh, contract, *, holder_id, ttl_sec=7200) using O_EXCL lockfile with TTL takeover returning release callback; verify_extracted_env(ssh, contract, manifest) -> list[str] of diagnostic strings (never raises from probes — every probe uses _execute(check=False), captures stderr first/last 50 lines, and emits diagnostic on non-zero exit). Probes: (a) torch CUDA import probe `cd {runtime_worker_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} uv run --python {python_version} python -c 'import torch; print(torch.version.cuda)'` — diagnose if exit != 0 or stdout != expected `12.4` for cuda124; (b) test -f template_index.json and workflow_corpus/manifests/coverage.json; (c) du -sb {runtime_venv_path}/lib size vs manifest venv_size_bytes (issue if >20% smaller); (d) node-schema verify `cd {runtime_vibecomfy_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} python -m vibecomfy.cli nodes verify --lockfile custom_nodes.lock` — diagnostic must include literal `rl prebuilt build` and `rl prebuilt invalidate` strings.\",\"depends_on\":[\"T1\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T3\",\"description\":\"Refactor `reigh-worker/scripts/live_test/ssh_bootstrap.py` into bundle-aware primitives WITHOUT changing observable behavior of existing callers. Extract `_uv_sync_shell(workdir, *, env_path, extras=('cuda124',), with_locked=False)` — raises ValueError if extras is empty. Extract `_vibecomfy_install_shell(workdir, *, python_path, attention_profile, run_nodes_restore=True)`. Re-implement existing `run_install` and `clone_and_install_vibecomfy` as thin wrappers around these (must emit byte-identical shell commands — golden-string regression test will verify in T12). Add bundle helpers: `bundle_venv(ssh, *, source_env_path, bundle_path)` and `bundle_install_tree(ssh, *, source_path, bundle_path)` using `tar --use-compress-program 'zstd -1 --threads=0' -cf {staging} && sha256sum && mv {staging} {bundle_path}`; `extract_bundle_to_container_disk(ssh, *, bundle_path, target_path, expected_sha256)` with mkdir -p, sha verification, pv-streamed extract, raising with first/last 50 stderr lines on sha mismatch; `ensure_git_ref_synced(ssh, *, workdir, repo_url, ref, force_clone=False)` doing full clone on force_clone or `git fetch && git checkout && git reset --hard FETCH_HEAD && git clean -ffd` otherwise.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T4\",\"description\":\"Parameterize `reigh-worker/scripts/live_test/launch_command.py:build_run_worker_command` by adding two keyword-only kwargs: `venv_path: str = '/opt/reigh-worker-live-test-venv'` and `python_version: str = '3.10'`. Edit line 37 to use `venv_path` in the `UV_PROJECT_ENVIRONMENT` export. Edit lines 43-44 to substitute `python_version` into the `--python` flag (replacing hardcoded `3.10`). Defaults must preserve byte-identical existing behavior. Update `tests/test_primitives.py` lines 870, 2317-2319, 2445 assertions to verify the parameterized mechanism (function emits `UV_PROJECT_ENVIRONMENT=\\\"{venv_path}\\\"` and `--python {python_version}` substitutions) rather than literal strings. Add new test cases: `build_run_worker_command(venv_path='/custom', python_version='3.11')` emits both substitutions; defaults preserve legacy strings.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T5\",\"description\":\"Create `reigh-worker/scripts/live_test/_shared.py` and move VERBATIM from variant_fresh.py: `_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`. Also extract `_build_worker_env` to `_shared.py` as `_build_worker_env_base` (per warning all_locations-2 — variant_prebuilt's HF_HOME-extending wrapper needs this). Add new `select_network_volume(api_key, *, name_prefix, data_center_filter=None)` helper that enumerates `get_network_volumes(api_key)` and returns first match `(volume_id, name, data_center_id)` or None. Move + rename `_register_fresh_worker_record` (variant_fresh.py:262-299) to `register_worker_record(db, pod_id, pod, args, *, variant_label: str)` — body uses `variant_label` in place of the literal `FRESH_VARIANT`. Update `variant_fresh.py` to import from `_shared` and call register_worker_record with variant_label='fresh'. Preserve backward-compatible re-exports at top of variant_fresh.py: `_phase = _shared._phase`, `_redact_sensitive_text = _shared._redact_sensitive_text`, `_capture_and_redact_noisy_lifecycle_output = _shared._capture_and_redact_noisy_lifecycle_output` so existing test imports keep resolving.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T6\",\"description\":\"EXTEND existing `runpod-lifecycle/src/runpod_lifecycle/guard.py` (DO NOT overwrite the existing PodGuard class — read the file first to confirm current contents). Add `prune_pods_by_prefix(prefixes: tuple[str, ...], api_key: str, *, stale_age_sec: int = 6*60*60) -> StalePodCleanupResult` with the same return shape as existing `prune_stale_live_test_pods`, parametric on `prefixes`. Compile one regex per prefix: `re.compile(rf'^{re.escape(prefix)}(\\\\d{{8}})t(\\\\d{{6}})z$')` — first verify case convention by reading `terminate_guard._FRESH_POD_NAME_RE` and `_timestamp_label` in variant_fresh.py:73-74 to match whichever case the existing code uses (the timestamp format is `%Y%m%dT%H%M%SZ` but the existing regex may lowercase input). Update `runpod_lifecycle/__init__.py:15` to re-export `prune_pods_by_prefix` alongside the existing PodGuard exports. No reigh-worker import in this module — direction is reigh-worker → runpod-lifecycle one-way.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T7\",\"description\":\"Add `prebuilt` CLI verb to `runpod-lifecycle/src/runpod_lifecycle/cli.py` with `build|inspect|invalidate|list` subcommands (first read cli.py to confirm subparser registration mechanism). `prebuilt build` args: `--volume-name` (required), `--data-center` (required), `--attention-profile {portable,sage}` (default portable), `--worker-ref` (default main), `--vibecomfy-ref` (default main), `--gpu-type` (default 'NVIDIA GeForce RTX 4090'), `--container-disk-gb` (default 200, floor ≥100), `--volume-disk-gb` (default 500), `--python-version` (default 3.10), `--dry-run`, `--force`. Builder flow phases each wrapped in `_phase`: provision_builder_pod (prefix `reigh-livetest-builder-` + `%Y%m%dT%H%M%SZ` suffix); acquire_lock; clone_repos to /opt/build/{reigh-worker,vibecomfy}; install_worker via `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`; install_vibecomfy via `_vibecomfy_install_shell(workdir=/opt/build/vibecomfy, run_nodes_restore=True)`; bundle_artifacts producing ONLY `{cache_root}/venv.cuda124.tar.zst` and `{cache_root}/vibecomfy.tar.zst` (NO comfyui.tar.zst — ComfyUI lives in venv site-packages); seed_models_dir (mkdir -p {models_path}, write empty INDEX.json if absent); write_manifest; release_lock; terminate_builder_pod via `guarded_terminate(pod_id, api_key, no_terminate=False)`. `prebuilt inspect` provisions probe pod, attaches volume, reads manifest, terminates. `prebuilt invalidate` runs `rm -rf {cache_root}/{venv.cuda124.tar.zst,vibecomfy.tar.zst,env.manifest.json}` preserving models/ and build.lock. `prebuilt list` enumerates get_network_volumes, filters by prefix `reigh-livetest-prebuilt-`, prints {name, dataCenterId, size}.\",\"depends_on\":[\"T1\",\"T2\",\"T3\",\"T6\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T8\",\"description\":\"Update `reigh-worker/scripts/live_test/config.py` to add the multi-region volume convention. Add `PREBUILT_VOLUME_NAME_PREFIX = 'reigh-livetest-prebuilt-'` and `prebuilt_name_for_profile(profile: str, data_center_id: str) -> str` returning `f'{PREBUILT_VOLUME_NAME_PREFIX}{profile}-{data_center_id.lower()}'`. Add new constants: `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH = '/opt/reigh-worker-live-test-venv'`, `PREBUILT_RUNTIME_WORKER_PATH = '/opt/reigh-livetest-prebuilt/worker'`, `PREBUILT_RUNTIME_VIBECOMFY_PATH = '/opt/reigh-livetest-prebuilt/vibecomfy'`. Extend `config.py:__all__` (currently lines 173-203) to export: `PREBUILT_VOLUME_NAME_PREFIX`, `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH`, `PREBUILT_RUNTIME_WORKER_PATH`, `PREBUILT_RUNTIME_VIBECOMFY_PATH`, `prebuilt_name_for_profile`. Volume region comes from RunPod's `dataCenterId` (e.g. `eu-no-1`) at runtime via `select_network_volume` (added in T5) — NOT from `RUNPOD_STORAGE_VOLUMES` name tuple. `find_gpu_type` has no region filter; pod-create enforces region implicitly via attached volume's dataCenterId.\",\"depends_on\":[\"T5\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T9\",\"description\":\"Create `reigh-worker/scripts/live_test/variant_prebuilt.py` importing from `_shared`. Pod name prefix `reigh-livetest-prebuilt-` + `%Y%m%dT%H%M%SZ`. Volume selection via `select_network_volume(api_key, name_prefix=PREBUILT_VOLUME_NAME_PREFIX + f'{profile}-')` — if no match, raise with the EXACT `rl prebuilt build --volume-name {recommended_name} --data-center {dc} --attention-profile portable` command. Reject `--container-disk-gb < 100`, default 200. Bootstrap phases each wrapped in `_phase` IN THIS ORDER: attach_prebuilt_volume (mountpoint -q /workspace) → read_prebuilt_manifest (raise with `rl prebuilt build` text if None) → check_hard_fail_drift (compare ONLY schema_version/bundle_format_version/python_version/cuda_extra; on drift raise with `rl prebuilt build` text — NEVER delta-sync these) → extract_venv_bundle (to /opt/reigh-worker-live-test-venv) → extract_vibecomfy_bundle (to /opt/reigh-livetest-prebuilt/vibecomfy; NO comfyui_bundle phase) → sync_worker_ref (ensure_git_ref_synced for /opt/reigh-livetest-prebuilt/worker to args.ref using force_clone=True since worker is not in the bundle; if pyproject_hash drifted run `_uv_sync_shell(env_path=runtime_venv_path, extras=('cuda124',))`) → sync_vibecomfy_ref (ensure_git_ref_synced to args.vibecomfy_ref; if custom_nodes_lock_hash drifted run `_vibecomfy_install_shell(run_nodes_restore=True)` else `pip install -e .` only) → verify_extracted_env (calls T2's function AFTER syncs; joins ALL returned issues into a numbered diagnostic and raises with `rl prebuilt invalidate && rl prebuilt build` instructions — must always include node-schema verify probe regardless of drift) → bind_models_dir (compute HF_HOME={models_path}/huggingface, HF_HUB_CACHE={models_path}/huggingface/hub, ComfyUI models-path env; OVERWRITE `{runtime_vibecomfy_path}/extra_model_paths.yaml` on every bootstrap — clobber semantics, do not merge; add HF_HOME, HF_HUB_CACHE, and ComfyUI models-path key to the worker_env dict passed to export_env and launch_worker_detached) → launch_worker (call build_run_worker_command(workdir=runtime_worker_path, venv_path=contract.runtime_venv_path, python_version=contract.python_version, ...)). Implement `_build_worker_env` as wrapper around `_shared._build_worker_env_base` adding HF_HOME, HF_HUB_CACHE, and ComfyUI models-path env. Call `register_worker_record(..., variant_label='prebuilt')`. Add `_print_dry_run_plan` taking venv_path/python_version from contract so dry-run output shows the prebuilt paths, not fresh defaults. Add `--strict-prebuilt` (abort on any drift), `--allow-delta` (default true), `--update-manifest-on-sync` flags. Manifest is not rewritten on delta sync by default. Ensure `_finalize_args` (main.py:115-132) also runs for prebuilt variant to apply selector_namespace normalization (per warning callers-1).\",\"depends_on\":[\"T1\",\"T2\",\"T3\",\"T4\",\"T5\",\"T8\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T10\",\"description\":\"Update `reigh-worker/scripts/live_test/main.py` to add `prebuilt` and `auto` to the variant switch. Argparse default for `--variant` REMAINS `'fresh'` — DO NOT flip to auto. `--variant auto` (opt-in) preflights `select_network_volume(name_prefix=PREBUILT_VOLUME_NAME_PREFIX)`; if a volume exists AND manifest readable → dispatch prebuilt, else dispatch fresh and emit structured `prebuilt_unavailable` log line. Add to shared argparse parser (so existing `--backend`, `--worker-profile`, `--selector-namespace`, `--selector-version`, `--worker-contract-version` continue to be parsed for prebuilt): `--prebuilt-volume-name`, `--strict-prebuilt`, `--allow-delta` (default true), `--update-manifest-on-sync`. Confirm `_finalize_args` runs for all variants including prebuilt. Container-disk floor of 100 GB and default 200 GB enforced for prebuilt variant.\",\"depends_on\":[\"T9\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T11\",\"description\":\"Update `reigh-worker/scripts/live_test/terminate_guard.py` to replace the single `LIVE_TEST_FRESH_POD_PREFIX` with `LIVE_TEST_POD_PREFIXES: tuple[str, ...] = ('reigh-live-test-fresh-', 'reigh-livetest-prebuilt-', 'reigh-livetest-builder-')`. Replace `_FRESH_POD_NAME_RE` with `_LIVE_TEST_POD_NAME_RES: tuple[re.Pattern, ...] = tuple(re.compile(rf'^{re.escape(p)}(\\\\d{{8}})t(\\\\d{{6}})z$') for p in LIVE_TEST_POD_PREFIXES)` — VERIFY case convention by reading the existing pattern first; the timestamp format from `_timestamp_label` is `%Y%m%dT%H%M%SZ` but existing code may lowercase input before matching. All three patterns must use the same convention. Update `prune_stale_live_test_pods` to delegate to `runpod_lifecycle.guard.prune_pods_by_prefix(LIVE_TEST_POD_PREFIXES, api_key, ...)`. Preserve `guarded_terminate` semantics unchanged.\",\"depends_on\":[\"T6\"],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T12\",\"description\":\"Add ONE guard line at the top of `reigh-worker/scripts/live_test/variant_update.run` (before any uv sync issue): SSH `test -f /workspace/reigh-livetest-prebuilt/env.manifest.json`. If exit code 0 → raise `RuntimeError('Prebuilt cache present at /workspace/reigh-livetest-prebuilt; --variant update would mutate the cached venv at /opt/reigh-worker-live-test-venv. Use --variant prebuilt instead, or run `rl prebuilt invalidate --volume-name X` first. This applies to both --pod-id and --spawn-takeover modes.')`. No other changes to variant_update.py. Diff must be limited to this guard plus any necessary import.\",\"depends_on\":[],\"status\":\"pending\",\"kind\":\"code\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T13\",\"description\":\"Write unit tests `runpod-lifecycle/tests/test_prebuilt.py` covering: hash determinism (compute_pyproject_hash, compute_lockfile_hash); manifest round-trip; drift detection — schema_version/bundle_format_version/python_version/cuda_extra each return hard_fail; pyproject_hash/custom_nodes_lock_hash/comfyui_pin/vibecomfy_commit/reigh_worker_commit each return delta_sync; build.lock O_EXCL acquire/release + TTL takeover; concurrent acquire fails with recorded holder_id and timestamp; atomic-rename simulation — builder crash before final mv leaves existing manifest+bundles untouched.\",\"depends_on\":[\"T1\",\"T2\"],\"status\":\"pending\",\"kind\":\"test\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T14\",\"description\":\"Write ssh_bootstrap refactor regression tests in the existing reigh-worker test module: golden-string comparisons proving `run_install` and `clone_and_install_vibecomfy` produce byte-identical shell commands (modulo whitespace normalization) vs pre-refactor capture; `_uv_sync_shell(extras=())` raises ValueError; default extras is ('cuda124',); `ensure_git_ref_synced` emits the expected git fetch/checkout/reset/clean sequence WITHOUT any uv sync.\",\"depends_on\":[\"T3\"],\"status\":\"pending\",\"kind\":\"test\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T15\",\"description\":\"Write harness tests `reigh-worker/scripts/live_test/tests/test_variant_prebuilt.py` with fake SSH capturing commands. Cover: (a) manifest match → zero install commands issued, verify_extracted_env still runs after sync phases; (b) pyproject_hash drift → `_uv_sync_shell(extras=('cuda124',))` issued; (c) custom_nodes_lock_hash drift → destructive `nodes restore` issued; (d) vibecomfy_commit-only drift → git checkout + pip install -e but NO nodes restore; (e) python_version drift → raises with literal `rl prebuilt build` text, no extract/sync attempted; (f) schema_version drift → raises with `rl prebuilt build` text, no extract/sync attempted; (g) missing manifest → raises with literal substring `rl prebuilt build --volume-name`; (h) phase-order assertion — verify_extracted_env is invoked AFTER sync_worker_ref and sync_vibecomfy_ref by capturing command order; (i) worker-env test — `variant_prebuilt._build_worker_env` returns a dict containing HF_HOME, HF_HUB_CACHE, and ComfyUI models-path key (none of which appear in fresh variant's env); (j) variant_update guard test — fake SSH reports manifest present, variant_update.run raises with literal `Prebuilt cache present` before any uv sync; (k) terminate_guard regex test — each of three prefixes matches sample pod name like `reigh-livetest-prebuilt-20260513t120000z`, `reigh-livetest-builder-20260513t120000z`, `reigh-live-test-fresh-20260513t120000z` (match case to whichever convention T11 verified); (l) test that legacy imports `from scripts.live_test.variant_fresh import _phase` still resolve via re-exports.\",\"depends_on\":[\"T9\",\"T10\",\"T11\",\"T12\"],\"status\":\"pending\",\"kind\":\"test\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T16\",\"description\":\"Run dry-run smoke tests: `python -m scripts.live_test --variant prebuilt --dry-run --backend vibecomfy --case z_image_turbo` and `python -m scripts.live_test --variant auto --dry-run --backend vibecomfy --case z_image_turbo`. Both must complete without RunPod credentials. Assert: auto falls back to fresh when select_network_volume returns None and picks prebuilt when a volume is reported (use a fake/mocked select_network_volume or env var injection if needed). Assert dry-run output for the prebuilt variant displays `runtime_venv_path` and `python_version` from the contract, NOT the fresh defaults. Also smoke `rl prebuilt --help`, `rl prebuilt build --help`, `rl prebuilt inspect --help`, `rl prebuilt invalidate --help`, `rl prebuilt list --help` to confirm subcommands exist with help text and `build` requires `--data-center` and `--volume-name`.\",\"depends_on\":[\"T7\",\"T9\",\"T10\"],\"status\":\"pending\",\"kind\":\"test\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T17\",\"description\":\"Add the Prebuilt validation environment section to `docs/migration-vibecomfy-live-validation.md` covering: bundle architecture (extract-to-/opt/ on container disk, /workspace as network-volume mount); two bundles only (venv.cuda124.tar.zst includes ComfyUI in site-packages; vibecomfy.tar.zst); hard-fail vs delta-sync drift rules with explicit invalidation table; region-pinned volume naming (`reigh-livetest-prebuilt-{profile}-{datacenterid-lowercased}`) with auto-selection by dataCenterId via `select_network_volume`; model-cache layout (models/ on volume, HF_HOME/HF_HUB_CACHE redirection) with v1 first-run cold-download caveat; partial-state diagnostics (verify_extracted_env probes joined into a single error); concurrent-builder build.lock with TTL takeover; variant_update coexistence guard; `--variant auto` opt-in recommendation; explicit note that argparse default remains `fresh` and that future agents should pass `--variant auto`. Create new committed file `reigh-worker/.claude/skills/live-test/SKILL.md` naming `--variant auto` as the recommended invocation and cross-referencing the doc above. Add a one-line pointer in `vibecomfy/CLAUDE.md` decision-shortcuts section to the new skill.\",\"depends_on\":[\"T9\",\"T10\"],\"status\":\"pending\",\"kind\":\"docs\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null},{\"id\":\"T18\",\"description\":\"Run the full relevant local test suite to verify nothing regressed. Execute: (a) `pytest runpod-lifecycle/tests/test_prebuilt.py -v`; (b) the reigh-worker live_test tests including the new `test_variant_prebuilt.py`, the updated `test_primitives.py`, and existing variant_fresh + variant_update test suites — confirm all pass; (c) the dry-run smoke commands from T16; (d) a quick `python -c 'from scripts.live_test.variant_fresh import _phase, _redact_sensitive_text, _capture_and_redact_noisy_lifecycle_output'` to confirm backward-compat re-exports resolve. Also write a short throwaway script `/tmp/repro_prebuilt_dryrun.py` that imports variant_prebuilt, constructs a mock PrebuiltManifest with python_version='3.11', and asserts that `build_run_worker_command(venv_path='/opt/reigh-worker-live-test-venv', python_version='3.11')` emits `--python 3.11` in its shell command — run it to confirm the python_version end-to-end flow, then delete it. If any test fails, read the error, fix the code, and re-run until all green. Lint/typecheck changed files. Capture command output in executor_notes.\",\"depends_on\":[\"T1\",\"T2\",\"T3\",\"T4\",\"T5\",\"T6\",\"T7\",\"T8\",\"T9\",\"T10\",\"T11\",\"T12\",\"T13\",\"T14\",\"T15\",\"T16\",\"T17\"],\"status\":\"pending\",\"kind\":\"test\",\"executor_notes\":\"\",\"files_changed\":[],\"commands_run\":[],\"auto_attributed_files\":null,\"evidence_files\":[],\"reviewer_verdict\":\"\",\"stance\":null,\"stop_signal\":null}],\"watch_items\":[\"DO NOT overwrite existing `runpod-lifecycle/src/runpod_lifecycle/guard.py` — that file already exists (127 lines) and houses PodGuard + install_signal_handlers re-exported from __init__.py:15. Read the file first; extend it by adding prune_pods_by_prefix; update __init__.py:15 to also re-export prune_pods_by_prefix. Plan wording 'new module' is imprecise.\",\"Plan body says python_version default in build_run_worker_command is 3.10 (matches existing behavior). Fresh path uses uv-managed py3.10 download; prebuilt path uses base-image py3.11 (config.py:91 = py3.11-cuda12.4.1). This divergence is intentional and the manifest's python_version field enforces consistency for prebuilt — but DO NOT change the fresh default or you will silently break existing fresh runs.\",\"DO NOT bundle the worker tree — the bundle architecture is intentionally venv + vibecomfy only; worker is cloned fresh on each consumer run via `ensure_git_ref_synced(force_clone=True)` since it's branch-flexible by design. Plan's `treat the bundle's worker tree as a starting point` wording is misleading; on first run the dir does not exist and a full clone happens.\",\"verify_extracted_env probes MUST use _execute(check=False) so non-zero exit codes never raise inside the probe — capture stderr (first/last 50 lines) and emit diagnostic strings; consumer joins ALL returned issues (newline-separated, numbered) into the raised RuntimeError, NOT just the first one.\",\"The cheap `vibecomfy.cli nodes verify --lockfile custom_nodes.lock` subcommand may not exist yet in vibecomfy. If it does not exist when implementing T2, the implementer must either add it as a small read-only subcommand to vibecomfy (touch enumerate-add to vibecomfy repo) OR fall back to a lighter sanity probe like `test -f template_index.json` plus `python -c 'import json; assert len(json.load(open(\\\"template_index.json\\\"))) > 0'`. DO NOT silently no-op the probe.\",\"argparse `--variant` default MUST remain `fresh` — the rev 2 plan flipped to `auto` and that was reverted in rev 3. Skill + docs recommend `--variant auto` but no script behavior changes silently.\",\"`bind_models_dir` always OVERWRITES `{runtime_vibecomfy_path}/extra_model_paths.yaml` on every consumer bootstrap (clobber semantics — do not merge with builder-baked file).\",\"MooseFS staging-stream throughput during the multi-GB tar+zstd write to the network volume is the only unbenchmarked perf assumption. If T19's real RunPod run shows the bundle phase exceeds ~10 min, surface it in the prebuilt-validation.md artifact rather than burying it.\",\"Model warming is v2 scope. First-encounter workflows still cold-download HF weights (10-50GB). The `materially faster` claim is bounded to deps install (67min → ~10min) plus steady-state model reuse via HF_HOME on the volume — make this caveat explicit in T17's docs.\",\"Pod-name regex case convention: the timestamp format `%Y%m%dT%H%M%SZ` from `_timestamp_label` uses uppercase T/Z, but `terminate_guard._FRESH_POD_NAME_RE` may lowercase input before matching. Read the existing pattern in terminate_guard.py:16 BEFORE writing the new tuple in T11; match whichever convention the existing code uses for all three prefixes.\",\"`_finalize_args` (main.py:115-132) currently normalizes selector_namespace for vibecomfy+production. Confirm in T10 that it runs for `--variant prebuilt` too, or the prebuilt path will use a different selector namespace than fresh.\",\"cross-repo import direction is strictly one-way: reigh-worker → runpod-lifecycle. runpod-lifecycle has NO dependency on reigh-worker — `prune_pods_by_prefix` lives in `runpod_lifecycle.guard` and `terminate_guard.py` delegates to it. Do not introduce any reverse import.\",\"Builder pods use the SAME `%Y%m%dT%H%M%SZ` timestamp suffix as consumer pods so the terminate_guard regex tuple catches all three pod prefixes uniformly.\",\"variant_update.py diff is strictly limited to the new prebuilt-manifest coexistence guard line plus any necessary import. Do not refactor or migrate REMOTE_UV_SYNC to call `_uv_sync_shell(with_locked=True)` — variant_update stays untouched.\"],\"sense_checks\":[{\"id\":\"SC1\",\"task_id\":\"T1\",\"question\":\"Does PrebuiltManifest have exactly these fields and NO comfyui_bundle_sha256: schema_version, bundle_format_version, built_at_utc, built_by, pyproject_hash, custom_nodes_lock_hash, comfyui_pin, attention_profile, python_version, cuda_extra, vibecomfy_commit, reigh_worker_commit, uv_version, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes, notes?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC2\",\"task_id\":\"T2\",\"question\":\"Does verify_extracted_env use _execute(check=False) for every probe and return list[str] of issues without raising on non-zero exit? Does probe (d) always run regardless of lockfile drift?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC3\",\"task_id\":\"T3\",\"question\":\"Do run_install and clone_and_install_vibecomfy produce byte-identical shell commands vs pre-refactor (verified by golden-string test in T14)? Does _uv_sync_shell raise ValueError when extras is empty?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC4\",\"task_id\":\"T4\",\"question\":\"Does build_run_worker_command(venv_path='/x', python_version='3.11') emit UV_PROJECT_ENVIRONMENT=\\\"/x\\\" and --python 3.11, while defaults preserve /opt/reigh-worker-live-test-venv and 3.10? Are test_primitives.py:870, 2317-2319, 2445 updated to mechanism-based assertions?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC5\",\"task_id\":\"T5\",\"question\":\"Are _phase, _redact_sensitive_text, _capture_and_redact_noisy_lifecycle_output still importable from variant_fresh via re-exports? Is _build_worker_env extracted as _build_worker_env_base? Does register_worker_record take variant_label and accept args.backend/worker_profile/selector_namespace/selector_version/worker_contract_version?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC6\",\"task_id\":\"T6\",\"question\":\"Was the existing PodGuard class in guard.py preserved? Is prune_pods_by_prefix added alongside without overwriting? Does __init__.py:15 also re-export prune_pods_by_prefix? Is runpod-lifecycle free of any reigh-worker import?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC7\",\"task_id\":\"T7\",\"question\":\"Does `rl prebuilt build --help` require --data-center and --volume-name and accept --python-version? Does `rl prebuilt invalidate` preserve models/ and build.lock? Does bundle_artifacts produce ONLY venv.cuda124.tar.zst and vibecomfy.tar.zst (no comfyui.tar.zst)?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC8\",\"task_id\":\"T8\",\"question\":\"Does prebuilt_name_for_profile(profile, data_center_id) return the lowercased dataCenterId as suffix (not derived from RUNPOD_STORAGE_VOLUMES)? Are all five new constants + helper exported in config.py:__all__?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC9\",\"task_id\":\"T9\",\"question\":\"Does the consumer bootstrap order phases as: attach_prebuilt_volume → read_prebuilt_manifest → check_hard_fail_drift → extract_venv_bundle → extract_vibecomfy_bundle → sync_worker_ref → sync_vibecomfy_ref → verify_extracted_env → bind_models_dir → launch_worker? Does verify run AFTER syncs? Does bind_models_dir add HF_HOME, HF_HUB_CACHE, ComfyUI models-path key to the worker_env dict consumed by launch_worker_detached?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC10\",\"task_id\":\"T10\",\"question\":\"Does argparse `--variant` default still equal 'fresh' (NOT 'auto')? Does --variant auto preflight select_network_volume and dispatch fresh when None? Does container-disk floor reject <100 GB?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC11\",\"task_id\":\"T11\",\"question\":\"Does LIVE_TEST_POD_PREFIXES contain exactly the three prefixes? Do the three regex patterns use the same case convention as the existing _FRESH_POD_NAME_RE? Does prune_stale_live_test_pods delegate to runpod_lifecycle.guard.prune_pods_by_prefix?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC12\",\"task_id\":\"T12\",\"question\":\"Is variant_update.py's diff strictly limited to the new guard line (plus any necessary import)? Does the guard raise with literal substring 'Prebuilt cache present' when the prebuilt manifest exists?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC13\",\"task_id\":\"T13\",\"question\":\"Do unit tests cover schema_version/bundle_format_version/python_version/cuda_extra hard_fail and pyproject_hash/custom_nodes_lock_hash/comfyui_pin/vibecomfy_commit/reigh_worker_commit delta_sync? Does the build.lock test cover O_EXCL + TTL takeover + concurrent acquire failure? Does the atomic-rename test prove a mid-bundle crash leaves existing manifest+bundles untouched?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC14\",\"task_id\":\"T14\",\"question\":\"Do golden-string tests prove run_install and clone_and_install_vibecomfy emit byte-identical commands vs pre-refactor capture? Does _uv_sync_shell(extras=()) raise ValueError?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC15\",\"task_id\":\"T15\",\"question\":\"Do harness tests cover all 12 cases (a)–(l) including phase-order assertion, worker-env keys, variant_update guard, terminate_guard regex for all three prefixes, and legacy import re-exports?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC16\",\"task_id\":\"T16\",\"question\":\"Did --variant prebuilt --dry-run and --variant auto --dry-run complete without RunPod credentials? Did auto fall back to fresh when no volume? Did dry-run output for prebuilt show contract paths, not fresh defaults? Did all four rl prebuilt subcommands show help?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC17\",\"task_id\":\"T17\",\"question\":\"Does the doc section cover bundle architecture (extract-to-/opt/), hard-fail vs delta-sync rules, dataCenterId-based region selection, model-cache layout + first-run cold-download caveat, partial-state diagnostics, build.lock, variant_update guard, --variant auto opt-in? Is SKILL.md committed and recommending --variant auto? Is vibecomfy/CLAUDE.md updated with a pointer?\",\"executor_note\":\"\",\"verdict\":\"\"},{\"id\":\"SC18\",\"task_id\":\"T18\",\"question\":\"Did all tests pass (runpod-lifecycle/tests/test_prebuilt.py, the new test_variant_prebuilt.py, updated test_primitives.py, existing variant_fresh + variant_update tests)? Did the throwaway end-to-end python_version repro confirm --python 3.11 propagates? Were no new lint/type errors introduced?\",\"executor_note\":\"\",\"verdict\":\"\"}],\"user_actions\":[{\"id\":\"U1\",\"description\":\"Operator runs the real RunPod live-test validation: (1) `rl prebuilt build --volume-name reigh-livetest-prebuilt-portable-eu-no-1 --data-center EU-NO-1 --attention-profile portable --worker-ref main --vibecomfy-ref main --python-version 3.11` and capture builder phase timings; (2) Run A (cold model cache): `python -m scripts.live_test --variant prebuilt --backend vibecomfy --case z_image_turbo` — measure pod-create → launch_worker elapsed; (3) Run B (warm model cache, 5 min after Run A): same command — verify HF cache reuse (no HuggingFace download log lines for z_image_turbo's model weights); (4) assert Run A bootstrap under 10 min vs ~67 min cold; (5) verify post-run RunPod listing shows only the consumer pod terminated, builder pod is already gone, volume persists; (6) capture results under `reigh-worker/scripts/live_test/runs/{timestamp}/prebuilt-validation.md` with phase timings. Requires real RunPod API credentials and GPU quota in EU-NO-1.\",\"phase\":\"after_execute\",\"blocks_task_ids\":null,\"rationale\":\"Real RunPod validation is the only way to satisfy the `info` success criteria proving the prebuilt path reaches launch_worker materially faster and that pod ownership is correct. The harness cannot self-verify physical-device timings or runtime logs.\",\"requires_human_only_reason\":\"Requires real RunPod API credentials, billing-incurring GPU pod provisioning, and physical-device runtime log observation that the executor cannot perform autonomously.\"}],\"meta_commentary\":\"This is a multi-repo change across reigh-worker, runpod-lifecycle, vibecomfy, and docs. Execution order matters: do Phase 1 foundation (T1-T5) BEFORE the builder CLI (T6-T8) BEFORE the consumer variant (T9-T12) BEFORE tests (T13-T16) BEFORE docs (T17) BEFORE the final test run (T18). Within Phase 1 the tasks can run in parallel since they touch different files (T1, T3, T4, T5 have no inter-dependencies; T2 depends on T1; T8 depends on T5). The single highest-risk pitfall is overwriting the existing PodGuard in guard.py — read the file first. The second-highest is the python_version end-to-end flow: launch_command.py:43-44 must read python_version from the manifest via build_run_worker_command's new kwarg, or the hard-fail invalidation rule is meaningless. The third is forgetting to add HF_HOME/HF_HUB_CACHE/ComfyUI models-path to the worker_env dict (NOT just the SSH bootstrap export) — the worker subprocess inherits env from that dict via export_env(worker_env). When the vibecomfy.cli nodes verify subcommand doesn't exist, add it as a small read-only addition rather than silently no-op'ing the probe. variant_update.py changes are strictly limited to one guard line — do not scope-creep. The argparse default for --variant stays `fresh`; --variant auto is opt-in and recommended in docs/skill only. Real RunPod validation is gated on operator action U1 after T18 passes locally.\",\"validation\":{\"plan_steps_covered\":[{\"plan_step_summary\":\"Step 1: Define bundle-based env contract (PrebuiltEnvContract, PrebuiltManifest, hash helpers, paths)\",\"finalize_item_ids\":[\"T1\"]},{\"plan_step_summary\":\"Step 2: SSH-side helpers (read/write manifest, build_lock, verify_extracted_env with 4 probes)\",\"finalize_item_ids\":[\"T2\"]},{\"plan_step_summary\":\"Step 3: Refactor ssh_bootstrap helpers into bundle-aware primitives\",\"finalize_item_ids\":[\"T3\"]},{\"plan_step_summary\":\"Step 4: Parameterize launch_command with venv_path + python_version, update test_primitives.py\",\"finalize_item_ids\":[\"T4\"]},{\"plan_step_summary\":\"Step 5: Extract _shared.py helpers and rename register_worker_record\",\"finalize_item_ids\":[\"T5\"]},{\"plan_step_summary\":\"Step 6: Add `prebuilt` CLI verb and extend guard.py with prune_pods_by_prefix\",\"finalize_item_ids\":[\"T6\",\"T7\"]},{\"plan_step_summary\":\"Step 7: Multi-region volume convention via dataCenterId; config.py constants and __all__ update\",\"finalize_item_ids\":[\"T8\"]},{\"plan_step_summary\":\"Step 8: New consumer variant variant_prebuilt.py with reordered phases and HF env threading\",\"finalize_item_ids\":[\"T9\"]},{\"plan_step_summary\":\"Step 9: CLI dispatch and --variant auto opt-in (default stays fresh)\",\"finalize_item_ids\":[\"T10\"]},{\"plan_step_summary\":\"Step 10: Pod-prefix tuple and terminate_guard regex enumeration\",\"finalize_item_ids\":[\"T11\"]},{\"plan_step_summary\":\"Step 11: variant_update coexistence guard\",\"finalize_item_ids\":[\"T12\"]},{\"plan_step_summary\":\"Step 12: Local tests (unit + harness + dry-run + smoke)\",\"finalize_item_ids\":[\"T13\",\"T14\",\"T15\",\"T16\"]},{\"plan_step_summary\":\"Step 13: Real RunPod validation (operator action)\",\"finalize_item_ids\":[\"U1\"]},{\"plan_step_summary\":\"Step 14: Documentation and skill discovery\",\"finalize_item_ids\":[\"T17\"]},{\"plan_step_summary\":\"Final verification — run full test suite and confirm everything passes\",\"finalize_item_ids\":[\"T18\"]}],\"orphan_tasks\":[],\"completeness_notes\":\"All 14 plan steps mapped. Step 6 covers two distinct deliverables (guard.py extension + cli.py verb) which are split into T6 and T7 for clarity. Step 12 has multiple sub-deliverables split into T13 (prebuilt unit tests), T14 (ssh_bootstrap regression tests), T15 (variant_prebuilt harness tests), T16 (dry-run smoke + CLI help smoke). T18 adds the mandatory final test-run verification per harness requirements. U1 is the only user_action and covers Step 13's RunPod validation which requires credentials, billing, and physical-device observation.\",\"coverage_complete\":true},\"baseline_test_failures\":[],\"baseline_test_command\":null,\"baseline_test_note\":\"No baseline test run was performed prior to finalize. The executor should run the relevant existing test suites (runpod-lifecycle tests, reigh-worker live_test tests including test_primitives.py and the variant_fresh + variant_update suites) as part of T18 to confirm no pre-existing failures are misattributed to this change. Per the assumption in the plan, all existing variant_fresh and variant_update tests must continue passing after the refactors.\"}"
}
```

> TOOL

tool_result StructuredOutput
```
Output does not match required schema: root: must have required property 'tasks', root: must have required property 'watch_items', root: must have required property 'sense_checks', root: must have required property 'user_actions', root: must have required property 'meta_commentary', root: must have required property 'validation', root: must have required property 'baseline_test_failures', root: must have required property 'baseline_test_command', root: must have required property 'baseline_test_note', root: must NOT have additional properties
```

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Create `runpod-lifecycle/src/runpod_lifecycle/prebuilt.py` exporting PrebuiltEnvContract (frozen dataclass with volume_name, data_center_id, mount_path=/workspace, cache_root={mount_path}/reigh-livetest-prebuilt, runtime_venv_path=/opt/reigh-worker-live-test-venv, runtime_worker_path=/opt/reigh-livetest-prebuilt/worker, runtime_vibecomfy_path=/opt/reigh-livetest-prebuilt/vibecomfy, models_path={cache_root}/models, attention_profile, comfyui_pin, python_version, bundle_format_version) and PrebuiltManifest (schema_version, bundle_format_version, built_at_utc, built_by, pyproject_hash, custom_nodes_lock_hash, comfyui_pin, attention_profile, python_version, cuda_extra='cuda124', vibecomfy_commit, reigh_worker_commit, uv_version, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes, notes — NO comfyui_bundle_sha256 field). Add compute_pyproject_hash, compute_lockfile_hash (SHA256 of canonicalized newline-normalized content), manifest_path(contract), lock_path(contract), staging_path(contract). Document invalidation precedence in module docstring: HARD-FAIL (schema_version, bundle_format_version, python_version, cuda_extra) requires `rl prebuilt build`; delta-sync (pyproject_hash, custom_nodes_lock_hash, comfyui_pin, vibecomfy_commit, reigh_worker_commit); no-op when all hashes match. Export all symbols from `runpod_lifecycle/__init__.py`.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T2",
      "description": "Extend `runpod-lifecycle/src/runpod_lifecycle/prebuilt.py` with SSH-side helpers: read_manifest(ssh, contract) -> PrebuiltManifest|None; write_manifest(ssh, contract, manifest) via heredoc + atomic mv; acquire_build_lock(ssh, contract, *, holder_id, ttl_sec=7200) using O_EXCL lockfile with TTL takeover returning release callback; verify_extracted_env(ssh, contract, manifest) -> list[str] of diagnostic strings (never raises from probes — every probe uses _execute(check=False), captures stderr first/last 50 lines, and emits diagnostic on non-zero exit). Probes: (a) torch CUDA import probe `cd {runtime_worker_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} uv run --python {python_version} python -c 'import torch; print(torch.version.cuda)'` — diagnose if exit != 0 or stdout != expected `12.4` for cuda124; (b) test -f template_index.json and workflow_corpus/manifests/coverage.json; (c) du -sb {runtime_venv_path}/lib size vs manifest venv_size_bytes (issue if >20% smaller); (d) node-schema verify `cd {runtime_vibecomfy_path} && UV_PROJECT_ENVIRONMENT={runtime_venv_path} python -m vibecomfy.cli nodes verify --lockfile custom_nodes.lock` — diagnostic must include literal `rl prebuilt build` and `rl prebuilt invalidate` strings.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T3",
      "description": "Refactor `reigh-worker/scripts/live_test/ssh_bootstrap.py` into bundle-aware primitives WITHOUT changing observable behavior of existing callers. Extract `_uv_sync_shell(workdir, *, env_path, extras=('cuda124',), with_locked=False)` — raises ValueError if extras is empty. Extract `_vibecomfy_install_shell(workdir, *, python_path, attention_profile, run_nodes_restore=True)`. Re-implement existing `run_install` and `clone_and_install_vibecomfy` as thin wrappers around these (must emit byte-identical shell commands — golden-string regression test will verify in T14). Add bundle helpers: `bundle_venv(ssh, *, source_env_path, bundle_path)` and `bundle_install_tree(ssh, *, source_path, bundle_path)` using `tar --use-compress-program 'zstd -1 --threads=0' -cf {staging} && sha256sum && mv {staging} {bundle_path}`; `extract_bundle_to_container_disk(ssh, *, bundle_path, target_path, expected_sha256)` with mkdir -p, sha verification, pv-streamed extract, raising with first/last 50 stderr lines on sha mismatch; `ensure_git_ref_synced(ssh, *, workdir, repo_url, ref, force_clone=False)` doing full clone on force_clone or `git fetch && git checkout && git reset --hard FETCH_HEAD && git clean -ffd` otherwise.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T4",
      "description": "Parameterize `reigh-worker/scripts/live_test/launch_command.py:build_run_worker_command` by adding two keyword-only kwargs: `venv_path: str = '/opt/reigh-worker-live-test-venv'` and `python_version: str = '3.10'`. Edit line 37 to use `venv_path` in the `UV_PROJECT_ENVIRONMENT` export. Edit lines 43-44 to substitute `python_version` into the `--python` flag (replacing hardcoded `3.10`). Defaults must preserve byte-identical existing behavior. Update `tests/test_primitives.py` lines 870, 2317-2319, 2445 assertions to verify the parameterized mechanism (function emits `UV_PROJECT_ENVIRONMENT=\"{venv_path}\"` and `--python {python_version}` substitutions) rather than literal strings. Add new test cases: `build_run_worker_command(venv_path='/custom', python_version='3.11')` emits both substitutions; defaults preserve legacy strings.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T5",
      "description": "Create `reigh-worker/scripts/live_test/_shared.py` and move VERBATIM from variant_fresh.py: `_phase`, `_capture_and_redact_noisy_lifecycle_output`, `_redact_sensitive_text`, `_runs_root`, `_timestamp_label`, `_resolve_runpod_gpu_type_id`. Also extract `_build_worker_env` to `_shared.py` as `_build_worker_env_base` (per warning all_locations-2 — variant_prebuilt's HF_HOME-extending wrapper needs this). Add new `select_network_volume(api_key, *, name_prefix, data_center_filter=None)` helper that enumerates `get_network_volumes(api_key)` and returns first match `(volume_id, name, data_center_id)` or None. Move + rename `_register_fresh_worker_record` (variant_fresh.py:262-299) to `register_worker_record(db, pod_id, pod, args, *, variant_label: str)` — body uses `variant_label` in place of the literal `FRESH_VARIANT`. Update `variant_fresh.py` to import from `_shared` and call register_worker_record with variant_label='fresh'. Preserve backward-compatible re-exports at top of variant_fresh.py: `_phase = _shared._phase`, `_redact_sensitive_text = _shared._redact_sensitive_text`, `_capture_and_redact_noisy_lifecycle_output = _shared._capture_and_redact_noisy_lifecycle_output` so existing test imports keep resolving.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T6",
      "description": "EXTEND existing `runpod-lifecycle/src/runpod_lifecycle/guard.py` (DO NOT overwrite the existing PodGuard class — read the file first to confirm current contents). Add `prune_pods_by_prefix(prefixes: tuple[str, ...], api_key: str, *, stale_age_sec: int = 6*60*60) -> StalePodCleanupResult` with the same return shape as existing `prune_stale_live_test_pods`, parametric on `prefixes`. Compile one regex per prefix: `re.compile(rf'^{re.escape(prefix)}(\\d{{8}})t(\\d{{6}})z$')` — first verify case convention by reading `terminate_guard._FRESH_POD_NAME_RE` and `_timestamp_label` in variant_fresh.py:73-74 to match whichever case the existing code uses (the timestamp format is `%Y%m%dT%H%M%SZ` but the existing regex may lowercase input). Update `runpod_lifecycle/__init__.py:15` to re-export `prune_pods_by_prefix` alongside the existing PodGuard exports. No reigh-worker import in this module — direction is reigh-worker → runpod-lifecycle one-way.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T7",
      "description": "Add `prebuilt` CLI verb to `runpod-lifecycle/src/runpod_lifecycle/cli.py` with `build|inspect|invalidate|list` subcommands (first read cli.py to confirm subparser registration mechanism). `prebuilt build` args: `--volume-name` (required), `--data-center` (required), `--attention-profile {portable,sage}` (default portable), `--worker-ref` (default main), `--vibecomfy-ref` (default main), `--gpu-type` (default 'NVIDIA GeForce RTX 4090'), `--container-disk-gb` (default 200, floor ≥100), `--volume-disk-gb` (default 500), `--python-version` (default 3.10), `--dry-run`, `--force`. Builder flow phases each wrapped in `_phase`: provision_builder_pod (prefix `reigh-livetest-builder-` + `%Y%m%dT%H%M%SZ` suffix); acquire_lock; clone_repos to /opt/build/{reigh-worker,vibecomfy}; install_worker via `_uv_sync_shell(env_path='/opt/reigh-worker-live-test-venv', extras=('cuda124',))`; install_vibecomfy via `_vibecomfy_install_shell(workdir=/opt/build/vibecomfy, run_nodes_restore=True)`; bundle_artifacts producing ONLY `{cache_root}/venv.cuda124.tar.zst` and `{cache_root}/vibecomfy.tar.zst` (NO comfyui.tar.zst — ComfyUI lives in venv site-packages); seed_models_dir (mkdir -p {models_path}, write empty INDEX.json if absent); write_manifest; release_lock; terminate_builder_pod via `guarded_terminate(pod_id, api_key, no_terminate=False)`. `prebuilt inspect` provisions probe pod, attaches volume, reads manifest, terminates. `prebuilt invalidate` runs `rm -rf {cache_root}/{venv.cuda124.tar.zst,vibecomfy.tar.zst,env.manifest.json}` preserving models/ and build.lock. `prebuilt list` enumerates get_network_volumes, filters by prefix `reigh-livetest-prebuilt-`, prints {name, dataCenterId, size}.",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T6"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T8",
      "description": "Update `reigh-worker/scripts/live_test/config.py` to add the multi-region volume convention. Add `PREBUILT_VOLUME_NAME_PREFIX = 'reigh-livetest-prebuilt-'` and `prebuilt_name_for_profile(profile: str, data_center_id: str) -> str` returning `f'{PREBUILT_VOLUME_NAME_PREFIX}{profile}-{data_center_id.lower()}'`. Add new constants: `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH = '/opt/reigh-worker-live-test-venv'`, `PREBUILT_RUNTIME_WORKER_PATH = '/opt/reigh-livetest-prebuilt/worker'`, `PREBUILT_RUNTIME_VIBECOMFY_PATH = '/opt/reigh-livetest-prebuilt/vibecomfy'`. Extend `config.py:__all__` (currently lines 173-203) to export: `PREBUILT_VOLUME_NAME_PREFIX`, `PREBUILT_CACHE_ROOT`, `PREBUILT_RUNTIME_VENV_PATH`, `PREBUILT_RUNTIME_WORKER_PATH`, `PREBUILT_RUNTIME_VIBECOMFY_PATH`, `prebuilt_name_for_profile`. Volume region comes from RunPod's `dataCenterId` (e.g. `eu-no-1`) at runtime via `select_network_volume` (added in T5) — NOT from `RUNPOD_STORAGE_VOLUMES` name tuple. `find_gpu_type` has no region filter; pod-create enforces region implicitly via attached volume's dataCenterId.",
      "depends_on": [
        "T5"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T9",
      "description": "Create `reigh-worker/scripts/live_test/variant_prebuilt.py` importing from `_shared`. Pod name prefix `reigh-livetest-prebuilt-` + `%Y%m%dT%H%M%SZ`. Volume selection via `select_network_volume(api_key, name_prefix=PREBUILT_VOLUME_NAME_PREFIX + f'{profile}-')` — if no match, raise with the EXACT `rl prebuilt build --volume-name {recommended_name} --data-center {dc} --attention-profile portable` command. Reject `--container-disk-gb < 100`, default 200. Bootstrap phases each wrapped in `_phase` IN THIS ORDER: attach_prebuilt_volume (mountpoint -q /workspace) → read_prebuilt_manifest (raise with `rl prebuilt build` text if None) → check_hard_fail_drift (compare ONLY schema_version/bundle_format_version/python_version/cuda_extra; on drift raise with `rl prebuilt build` text — NEVER delta-sync these) → extract_venv_bundle (to /opt/reigh-worker-live-test-venv) → extract_vibecomfy_bundle (to /opt/reigh-livetest-prebuilt/vibecomfy; NO comfyui_bundle phase) → sync_worker_ref (ensure_git_ref_synced for /opt/reigh-livetest-prebuilt/worker to args.ref using force_clone=True since worker is not in the bundle; if pyproject_hash drifted run `_uv_sync_shell(env_path=runtime_venv_path, extras=('cuda124',))`) → sync_vibecomfy_ref (ensure_git_ref_synced to args.vibecomfy_ref; if custom_nodes_lock_hash drifted run `_vibecomfy_install_shell(run_nodes_restore=True)` else `pip install -e .` only) → verify_extracted_env (calls T2's function AFTER syncs; joins ALL returned issues into a numbered diagnostic and raises with `rl prebuilt invalidate && rl prebuilt build` instructions — must always include node-schema verify probe regardless of drift) → bind_models_dir (compute HF_HOME={models_path}/huggingface, HF_HUB_CACHE={models_path}/huggingface/hub, ComfyUI models-path env; OVERWRITE `{runtime_vibecomfy_path}/extra_model_paths.yaml` on every bootstrap — clobber semantics, do not merge; add HF_HOME, HF_HUB_CACHE, and ComfyUI models-path key to the worker_env dict passed to export_env and launch_worker_detached) → launch_worker (call build_run_worker_command(workdir=runtime_worker_path, venv_path=contract.runtime_venv_path, python_version=contract.python_version, ...)). Implement `_build_worker_env` as wrapper around `_shared._build_worker_env_base` adding HF_HOME, HF_HUB_CACHE, and ComfyUI models-path env. Call `register_worker_record(..., variant_label='prebuilt')`. Add `_print_dry_run_plan` taking venv_path/python_version from contract so dry-run output shows the prebuilt paths, not fresh defaults. Add `--strict-prebuilt` (abort on any drift), `--allow-delta` (default true), `--update-manifest-on-sync` flags. Manifest is not rewritten on delta sync by default. Ensure `_finalize_args` (main.py:115-132) also runs for prebuilt variant to apply selector_namespace normalization (per warning callers-1).",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T8"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T10",
      "description": "Update `reigh-worker/scripts/live_test/main.py` to add `prebuilt` and `auto` to the variant switch. Argparse default for `--variant` REMAINS `'fresh'` — DO NOT flip to auto. `--variant auto` (opt-in) preflights `select_network_volume(name_prefix=PREBUILT_VOLUME_NAME_PREFIX)`; if a volume exists AND manifest readable → dispatch prebuilt, else dispatch fresh and emit structured `prebuilt_unavailable` log line. Add to shared argparse parser (so existing `--backend`, `--worker-profile`, `--selector-namespace`, `--selector-version`, `--worker-contract-version` continue to be parsed for prebuilt): `--prebuilt-volume-name`, `--strict-prebuilt`, `--allow-delta` (default true), `--update-manifest-on-sync`. Confirm `_finalize_args` runs for all variants including prebuilt. Container-disk floor of 100 GB and default 200 GB enforced for prebuilt variant.",
      "depends_on": [
        "T9"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T11",
      "description": "Update `reigh-worker/scripts/live_test/terminate_guard.py` to replace the single `LIVE_TEST_FRESH_POD_PREFIX` with `LIVE_TEST_POD_PREFIXES: tuple[str, ...] = ('reigh-live-test-fresh-', 'reigh-livetest-prebuilt-', 'reigh-livetest-builder-')`. Replace `_FRESH_POD_NAME_RE` with `_LIVE_TEST_POD_NAME_RES: tuple[re.Pattern, ...] = tuple(re.compile(rf'^{re.escape(p)}(\\d{{8}})t(\\d{{6}})z$') for p in LIVE_TEST_POD_PREFIXES)` — VERIFY case convention by reading the existing pattern first; the timestamp format from `_timestamp_label` is `%Y%m%dT%H%M%SZ` but existing code may lowercase input before matching. All three patterns must use the same convention. Update `prune_stale_live_test_pods` to delegate to `runpod_lifecycle.guard.prune_pods_by_prefix(LIVE_TEST_POD_PREFIXES, api_key, ...)`. Preserve `guarded_terminate` semantics unchanged.",
      "depends_on": [
        "T6"
      ],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T12",
      "description": "Add ONE guard line at the top of `reigh-worker/scripts/live_test/variant_update.run` (before any uv sync issue): SSH `test -f /workspace/reigh-livetest-prebuilt/env.manifest.json`. If exit code 0 → raise `RuntimeError('Prebuilt cache present at /workspace/reigh-livetest-prebuilt; --variant update would mutate the cached venv at /opt/reigh-worker-live-test-venv. Use --variant prebuilt instead, or run `rl prebuilt invalidate --volume-name X` first. This applies to both --pod-id and --spawn-takeover modes.')`. No other changes to variant_update.py. Diff must be limited to this guard plus any necessary import.",
      "depends_on": [],
      "status": "pending",
      "kind": "code",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T13",
      "description": "Write unit tests `runpod-lifecycle/tests/test_prebuilt.py` covering: hash determinism (compute_pyproject_hash, compute_lockfile_hash); manifest round-trip; drift detection — schema_version/bundle_format_version/python_version/cuda_extra each return hard_fail; pyproject_hash/custom_nodes_lock_hash/comfyui_pin/vibecomfy_commit/reigh_worker_commit each return delta_sync; build.lock O_EXCL acquire/release + TTL takeover; concurrent acquire fails with recorded holder_id and timestamp; atomic-rename simulation — builder crash before final mv leaves existing manifest+bundles untouched.",
      "depends_on": [
        "T1",
        "T2"
      ],
      "status": "pending",
      "kind": "test",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T14",
      "description": "Write ssh_bootstrap refactor regression tests in the existing reigh-worker test module: golden-string comparisons proving `run_install` and `clone_and_install_vibecomfy` produce byte-identical shell commands (modulo whitespace normalization) vs pre-refactor capture; `_uv_sync_shell(extras=())` raises ValueError; default extras is ('cuda124',); `ensure_git_ref_synced` emits the expected git fetch/checkout/reset/clean sequence WITHOUT any uv sync.",
      "depends_on": [
        "T3"
      ],
      "status": "pending",
      "kind": "test",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T15",
      "description": "Write harness tests `reigh-worker/scripts/live_test/tests/test_variant_prebuilt.py` with fake SSH capturing commands. Cover: (a) manifest match → zero install commands issued, verify_extracted_env still runs after sync phases; (b) pyproject_hash drift → `_uv_sync_shell(extras=('cuda124',))` issued; (c) custom_nodes_lock_hash drift → destructive `nodes restore` issued; (d) vibecomfy_commit-only drift → git checkout + pip install -e but NO nodes restore; (e) python_version drift → raises with literal `rl prebuilt build` text, no extract/sync attempted; (f) schema_version drift → raises with `rl prebuilt build` text, no extract/sync attempted; (g) missing manifest → raises with literal substring `rl prebuilt build --volume-name`; (h) phase-order assertion — verify_extracted_env is invoked AFTER sync_worker_ref and sync_vibecomfy_ref by capturing command order; (i) worker-env test — `variant_prebuilt._build_worker_env` returns a dict containing HF_HOME, HF_HUB_CACHE, and ComfyUI models-path key (none of which appear in fresh variant's env); (j) variant_update guard test — fake SSH reports manifest present, variant_update.run raises with literal `Prebuilt cache present` before any uv sync; (k) terminate_guard regex test — each of three prefixes matches sample pod name like `reigh-livetest-prebuilt-20260513t120000z`, `reigh-livetest-builder-20260513t120000z`, `reigh-live-test-fresh-20260513t120000z` (match case to whichever convention T11 verified); (l) test that legacy imports `from scripts.live_test.variant_fresh import _phase` still resolve via re-exports.",
      "depends_on": [
        "T9",
        "T10",
        "T11",
        "T12"
      ],
      "status": "pending",
      "kind": "test",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T16",
      "description": "Run dry-run smoke tests: `python -m scripts.live_test --variant prebuilt --dry-run --backend vibecomfy --case z_image_turbo` and `python -m scripts.live_test --variant auto --dry-run --backend vibecomfy --case z_image_turbo`. Both must complete without RunPod credentials. Assert: auto falls back to fresh when select_network_volume returns None and picks prebuilt when a volume is reported (use a fake/mocked select_network_volume or env var injection if needed). Assert dry-run output for the prebuilt variant displays `runtime_venv_path` and `python_version` from the contract, NOT the fresh defaults. Also smoke `rl prebuilt --help`, `rl prebuilt build --help`, `rl prebuilt inspect --help`, `rl prebuilt invalidate --help`, `rl prebuilt list --help` to confirm subcommands exist with help text and `build` requires `--data-center` and `--volume-name`.",
      "depends_on": [
        "T7",
        "T9",
        "T10"
      ],
      "status": "pending",
      "kind": "test",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T17",
      "description": "Add the Prebuilt validation environment section to `docs/migration-vibecomfy-live-validation.md` covering: bundle architecture (extract-to-/opt/ on container disk, /workspace as network-volume mount); two bundles only (venv.cuda124.tar.zst includes ComfyUI in site-packages; vibecomfy.tar.zst); hard-fail vs delta-sync drift rules with explicit invalidation table; region-pinned volume naming (`reigh-livetest-prebuilt-{profile}-{datacenterid-lowercased}`) with auto-selection by dataCenterId via `select_network_volume`; model-cache layout (models/ on volume, HF_HOME/HF_HUB_CACHE redirection) with v1 first-run cold-download caveat; partial-state diagnostics (verify_extracted_env probes joined into a single error); concurrent-builder build.lock with TTL takeover; variant_update coexistence guard; `--variant auto` opt-in recommendation; explicit note that argparse default remains `fresh` and that future agents should pass `--variant auto`. Create new committed file `reigh-worker/.claude/skills/live-test/SKILL.md` naming `--variant auto` as the recommended invocation and cross-referencing the doc above. Add a one-line pointer in `vibecomfy/CLAUDE.md` decision-shortcuts section to the new skill.",
      "depends_on": [
        "T9",
        "T10"
      ],
      "status": "pending",
      "kind": "docs",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T18",
      "description": "Run the full relevant local test suite to verify nothing regressed. Execute: (a) `pytest runpod-lifecycle/tests/test_prebuilt.py -v`; (b) the reigh-worker live_test tests including the new `test_variant_prebuilt.py`, the updated `test_primitives.py`, and existing variant_fresh + variant_update test suites — confirm all pass; (c) the dry-run smoke commands from T16; (d) a quick `python -c 'from scripts.live_test.variant_fresh import _phase, _redact_sensitive_text, _capture_and_redact_noisy_lifecycle_output'` to confirm backward-compat re-exports resolve. Also write a short throwaway script `/tmp/repro_prebuilt_dryrun.py` that imports variant_prebuilt, constructs a mock PrebuiltManifest with python_version='3.11', and asserts that `build_run_worker_command(venv_path='/opt/reigh-worker-live-test-venv', python_version='3.11')` emits `--python 3.11` in its shell command — run it to confirm the python_version end-to-end flow, then delete it. If any test fails, read the error, fix the code, and re-run until all green. Lint/typecheck changed files. Capture command output in executor_notes.",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7",
        "T8",
        "T9",
        "T10",
        "T11",
        "T12",
        "T13",
        "T14",
        "T15",
        "T16",
        "T17"
      ],
      "status": "pending",
      "kind": "test",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    }
  ],
  "watch_items": [
    "DO NOT overwrite existing `runpod-lifecycle/src/runpod_lifecycle/guard.py` — that file already exists (127 lines) and houses PodGuard + install_signal_handlers re-exported from __init__.py:15. Read the file first; extend it by adding prune_pods_by_prefix; update __init__.py:15 to also re-export prune_pods_by_prefix. Plan wording 'new module' is imprecise.",
    "Plan body says python_version default in build_run_worker_command is 3.10 (matches existing behavior). Fresh path uses uv-managed py3.10 download; prebuilt path uses base-image py3.11 (config.py:91 = py3.11-cuda12.4.1). This divergence is intentional and the manifest's python_version field enforces consistency for prebuilt — but DO NOT change the fresh default or you will silently break existing fresh runs.",
    "DO NOT bundle the worker tree — the bundle architecture is intentionally venv + vibecomfy only; worker is cloned fresh on each consumer run via `ensure_git_ref_synced(force_clone=True)` since it's branch-flexible by design. Plan's `treat the bundle's worker tree as a starting point` wording is misleading; on first run the dir does not exist and a full clone happens.",
    "verify_extracted_env probes MUST use _execute(check=False) so non-zero exit codes never raise inside the probe — capture stderr (first/last 50 lines) and emit diagnostic strings; consumer joins ALL returned issues (newline-separated, numbered) into the raised RuntimeError, NOT just the first one.",
    "The cheap `vibecomfy.cli nodes verify --lockfile custom_nodes.lock` subcommand may not exist yet in vibecomfy. If it does not exist when implementing T2, the implementer must either add it as a small read-only subcommand to vibecomfy (touch enumerate-add to vibecomfy repo) OR fall back to a lighter sanity probe like `test -f template_index.json` plus `python -c 'import json; assert len(json.load(open(\"template_index.json\"))) > 0'`. DO NOT silently no-op the probe.",
    "argparse `--variant` default MUST remain `fresh` — the rev 2 plan flipped to `auto` and that was reverted in rev 3. Skill + docs recommend `--variant auto` but no script behavior changes silently.",
    "`bind_models_dir` always OVERWRITES `{runtime_vibecomfy_path}/extra_model_paths.yaml` on every consumer bootstrap (clobber semantics — do not merge with builder-baked file).",
    "MooseFS staging-stream throughput during the multi-GB tar+zstd write to the network volume is the only unbenchmarked perf assumption. If U1's real RunPod run shows the bundle phase exceeds ~10 min, surface it in the prebuilt-validation.md artifact rather than burying it.",
    "Model warming is v2 scope. First-encounter workflows still cold-download HF weights (10-50GB). The `materially faster` claim is bounded to deps install (67min → ~10min) plus steady-state model reuse via HF_HOME on the volume — make this caveat explicit in T17's docs.",
    "Pod-name regex case convention: the timestamp format `%Y%m%dT%H%M%SZ` from `_timestamp_label` uses uppercase T/Z, but `terminate_guard._FRESH_POD_NAME_RE` may lowercase input before matching. Read the existing pattern in terminate_guard.py:16 BEFORE writing the new tuple in T11; match whichever convention the existing code uses for all three prefixes.",
    "`_finalize_args` (main.py:115-132) currently normalizes selector_namespace for vibecomfy+production. Confirm in T10 that it runs for `--variant prebuilt` too, or the prebuilt path will use a different selector namespace than fresh.",
    "Cross-repo import direction is strictly one-way: reigh-worker → runpod-lifecycle. runpod-lifecycle has NO dependency on reigh-worker — `prune_pods_by_prefix` lives in `runpod_lifecycle.guard` and `terminate_guard.py` delegates to it. Do not introduce any reverse import.",
    "Builder pods use the SAME `%Y%m%dT%H%M%SZ` timestamp suffix as consumer pods so the terminate_guard regex tuple catches all three pod prefixes uniformly.",
    "variant_update.py diff is strictly limited to the new prebuilt-manifest coexistence guard line plus any necessary import. Do not refactor or migrate REMOTE_UV_SYNC to call `_uv_sync_shell(with_locked=True)` — variant_update stays untouched."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does PrebuiltManifest have exactly these fields and NO comfyui_bundle_sha256: schema_version, bundle_format_version, built_at_utc, built_by, pyproject_hash, custom_nodes_lock_hash, comfyui_pin, attention_profile, python_version, cuda_extra, vibecomfy_commit, reigh_worker_commit, uv_version, venv_bundle_sha256, vibecomfy_bundle_sha256, models_index_sha256, venv_size_bytes, notes?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does verify_extracted_env use _execute(check=False) for every probe and return list[str] of issues without raising on non-zero exit? Does probe (d) always run regardless of lockfile drift?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Do run_install and clone_and_install_vibecomfy produce byte-identical shell commands vs pre-refactor (verified by golden-string test in T14)? Does _uv_sync_shell raise ValueError when extras is empty?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does build_run_worker_command(venv_path='/x', python_version='3.11') emit UV_PROJECT_ENVIRONMENT=\"/x\" and --python 3.11, while defaults preserve /opt/reigh-worker-live-test-venv and 3.10? Are test_primitives.py:870, 2317-2319, 2445 updated to mechanism-based assertions?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Are _phase, _redact_sensitive_text, _capture_and_redact_noisy_lifecycle_output still importable from variant_fresh via re-exports? Is _build_worker_env extracted as _build_worker_env_base? Does register_worker_record take variant_label and accept args.backend/worker_profile/selector_namespace/selector_version/worker_contract_version?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Was the existing PodGuard class in guard.py preserved? Is prune_pods_by_prefix added alongside without overwriting? Does __init__.py:15 also re-export prune_pods_by_prefix? Is runpod-lifecycle free of any reigh-worker import?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does `rl prebuilt build --help` require --data-center and --volume-name and accept --python-version? Does `rl prebuilt invalidate` preserve models/ and build.lock? Does bundle_artifacts produce ONLY venv.cuda124.tar.zst and vibecomfy.tar.zst (no comfyui.tar.zst)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does prebuilt_name_for_profile(profile, data_center_id) return the lowercased dataCenterId as suffix (not derived from RUNPOD_STORAGE_VOLUMES)? Are all five new constants + helper exported in config.py:__all__?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does the consumer bootstrap order phases as: attach_prebuilt_volume → read_prebuilt_manifest → check_hard_fail_drift → extract_venv_bundle → extract_vibecomfy_bundle → sync_worker_ref → sync_vibecomfy_ref → verify_extracted_env → bind_models_dir → launch_worker? Does verify run AFTER syncs? Does bind_models_dir add HF_HOME, HF_HUB_CACHE, ComfyUI models-path key to the worker_env dict consumed by launch_worker_detached?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Does argparse `--variant` default still equal 'fresh' (NOT 'auto')? Does --variant auto preflight select_network_volume and dispatch fresh when None? Does container-disk floor reject <100 GB?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Does LIVE_TEST_POD_PREFIXES contain exactly the three prefixes? Do the three regex patterns use the same case convention as the existing _FRESH_POD_NAME_RE? Does prune_stale_live_test_pods delegate to runpod_lifecycle.guard.prune_pods_by_prefix?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC12",
      "task_id": "T12",
      "question": "Is variant_update.py's diff strictly limited to the new guard line (plus any necessary import)? Does the guard raise with literal substring 'Prebuilt cache present' when the prebuilt manifest exists?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "question": "Do unit tests cover schema_version/bundle_format_version/python_version/cuda_extra hard_fail and pyproject_hash/custom_nodes_lock_hash/comfyui_pin/vibecomfy_commit/reigh_worker_commit delta_sync? Does the build.lock test cover O_EXCL + TTL takeover + concurrent acquire failure? Does the atomic-rename test prove a mid-bundle crash leaves existing manifest+bundles untouched?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "question": "Do golden-string tests prove run_install and clone_and_install_vibecomfy emit byte-identical commands vs pre-refactor capture? Does _uv_sync_shell(extras=()) raise ValueError?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC15",
      "task_id": "T15",
      "question": "Do harness tests cover all 12 cases (a)–(l) including phase-order assertion, worker-env keys, variant_update guard, terminate_guard regex for all three prefixes, and legacy import re-exports?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC16",
      "task_id": "T16",
      "question": "Did --variant prebuilt --dry-run and --variant auto --dry-run complete without RunPod credentials? Did auto fall back to fresh when no volume? Did dry-run output for prebuilt show contract paths, not fresh defaults? Did all four rl prebuilt subcommands show help?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC17",
      "task_id": "T17",
      "question": "Does the doc section cover bundle architecture (extract-to-/opt/), hard-fail vs delta-sync rules, dataCenterId-based region selection, model-cache layout + first-run cold-download caveat, partial-state diagnostics, build.lock, variant_update guard, --variant auto opt-in? Is SKILL.md committed and recommending --variant auto? Is vibecomfy/CLAUDE.md updated with a pointer?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC18",
      "task_id": "T18",
      "question": "Did all tests pass (runpod-lifecycle/tests/test_prebuilt.py, the new test_variant_prebuilt.py, updated test_primitives.py, existing variant_fresh + variant_update tests)? Did the throwaway end-to-end python_version repro confirm --python 3.11 propagates? Were no new lint/type errors introduced?",
      "executor_note": "",
      "verdict": ""
    }
  ],
  "user_actions": [
    {
      "id": "U1",
      "description": "Operator runs the real RunPod live-test validation: (1) `rl prebuilt build --volume-name reigh-livetest-prebuilt-portable-eu-no-1 --data-center EU-NO-1 --attention-profile portable --worker-ref main --vibecomfy-ref main --python-version 3.11` and capture builder phase timings; (2) Run A (cold model cache): `python -m scripts.live_test --variant prebuilt --backend vibecomfy --case z_image_turbo` — measure pod-create → launch_worker elapsed; (3) Run B (warm model cache, 5 min after Run A): same command — verify HF cache reuse (no HuggingFace download log lines for z_image_turbo's model weights); (4) assert Run A bootstrap under 10 min vs ~67 min cold; (5) verify post-run RunPod listing shows only the consumer pod terminated, builder pod is already gone, volume persists; (6) capture results under `reigh-worker/scripts/live_test/runs/{timestamp}/prebuilt-validation.md` with phase timings. Requires real RunPod API credentials and GPU quota in EU-NO-1.",
      "phase": "after_execute",
      "blocks_task_ids": null,
      "rationale": "Real RunPod validation is the only way to satisfy the `info` success criteria proving the prebuilt path reaches launch_worker materially faster and that pod ownership is correct. The harness cannot self-verify physical-device timings or runtime logs.",
      "requires_human_only_reason": "Requires real RunPod API credentials, billing-incurring GPU pod provisioning, and physical-device runtime log observation that the executor cannot perform autonomously."
    }
  ],
  "meta_commentary": "This is a multi-repo change across reigh-worker, runpod-lifecycle, vibecomfy, and docs. Execution order matters: do Phase 1 foundation (T1-T5) BEFORE the builder CLI (T6-T8) BEFORE the consumer variant (T9-T12) BEFORE tests (T13-T16) BEFORE docs (T17) BEFORE the final test run (T18). Within Phase 1 the tasks can run in parallel since they touch different files (T1, T3, T4, T5 have no inter-dependencies; T2 depends on T1; T8 depends on T5). The single highest-risk pitfall is overwriting the existing PodGuard in guard.py — read the file first. The second-highest is the python_version end-to-end flow: launch_command.py:43-44 must read python_version from the manifest via build_run_worker_command's new kwarg, or the hard-fail invalidation rule is meaningless. The third is forgetting to add HF_HOME/HF_HUB_CACHE/ComfyUI models-path to the worker_env dict (NOT just the SSH bootstrap export) — the worker subprocess inherits env from that dict via export_env(worker_env). When the vibecomfy.cli nodes verify subcommand doesn't exist, add it as a small read-only addition rather than silently no-op'ing the probe. variant_update.py changes are strictly limited to one guard line — do not scope-creep. The argparse default for --variant stays `fresh`; --variant auto is opt-in and recommended in docs/skill only. Real RunPod validation is gated on operator action U1 after T18 passes locally.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Define bundle-based env contract (PrebuiltEnvContract, PrebuiltManifest, hash helpers, paths)",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: SSH-side helpers (read/write manifest, build_lock, verify_extracted_env with 4 probes)",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 3: Refactor ssh_bootstrap helpers into bundle-aware primitives",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 4: Parameterize launch_command with venv_path + python_version, update test_primitives.py",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 5: Extract _shared.py helpers and rename register_worker_record",
        "finalize_item_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 6: Add `prebuilt` CLI verb and extend guard.py with prune_pods_by_prefix",
        "finalize_item_ids": [
          "T6",
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 7: Multi-region volume convention via dataCenterId; config.py constants and __all__ update",
        "finalize_item_ids": [
          "T8"
        ]
      },
      {
        "plan_step_summary": "Step 8: New consumer variant variant_prebuilt.py with reordered phases and HF env threading",
        "finalize_item_ids": [
          "T9"
        ]
      },
      {
        "plan_step_summary": "Step 9: CLI dispatch and --variant auto opt-in (default stays fresh)",
        "finalize_item_ids": [
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 10: Pod-prefix tuple and terminate_guard regex enumeration",
        "finalize_item_ids": [
          "T11"
        ]
      },
      {
        "plan_step_summary": "Step 11: variant_update coexistence guard",
        "finalize_item_ids": [
          "T12"
        ]
      },
      {
        "plan_step_summary": "Step 12: Local tests (unit + harness + dry-run + smoke)",
        "finalize_item_ids": [
          "T13",
          "T14",
          "T15",
          "T16"
        ]
      },
      {
        "plan_step_summary": "Step 13: Real RunPod validation (operator action)",
        "finalize_item_ids": [
          "U1"
        ]
      },
      {
        "plan_step_summary": "Step 14: Documentation and skill discovery",
        "finalize_item_ids": [
          "T17"
        ]
      },
      {
        "plan_step_summary": "Final verification — run full test suite and confirm everything passes",
        "finalize_item_ids": [
          "T18"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All 14 plan steps mapped. Step 6 covers two distinct deliverables (guard.py extension + cli.py verb) which are split into T6 and T7 for clarity. Step 12 has multiple sub-deliverables split into T13 (prebuilt unit tests), T14 (ssh_bootstrap regression tests), T15 (variant_prebuilt harness tests), T16 (dry-run smoke + CLI help smoke). T18 adds the mandatory final test-run verification per harness requirements. U1 is the only user_action and covers Step 13's RunPod validation which requires credentials, billing, and physical-device observation.",
    "coverage_complete": true
  },
  "baseline_test_failures": [],
  "baseline_test_command": null,
  "baseline_test_note": "No baseline test run was performed prior to finalize. The executor should run the relevant existing test suites (runpod-lifecycle tests, reigh-worker live_test tests including test_primitives.py and the variant_fresh + variant_update suites) as part of T18 to confirm no pre-existing failures are misattributed to this change. Per the assumption in the plan, all existing variant_fresh and variant_update tests must continue passing after the refactors."
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Finalize document produced: 18 tasks (T1–T18) covering all 14 plan steps plus a mandatory final verification, 1 user_action (U1) for the real-RunPod validation, 18 sense checks, and 14 watch items capturing the highest-risk pitfalls (preserving existing PodGuard, python_version end-to-end flow, HF_HOME env threading into the worker subprocess dict, regex case convention, scope-limit on variant_update.py, etc.). All 14 plan steps map to tasks/user_actions with `coverage_complete: true`.
