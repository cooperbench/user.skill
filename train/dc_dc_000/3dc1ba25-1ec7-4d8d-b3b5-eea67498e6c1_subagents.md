> DEVELOPER

I'm planning a reusable prebuilt RunPod/VibeComfy validation environment to skip the slow ~46min uv sync + 21min VibeComfy install on every live test. Survey these repos/dirs under `/Users/user_c042661f/Documents/reigh-workspace/`: 1. **reigh-worker/** — find the live-test harness/CLI that spins up a RunPod and runs VibeComfy workflows. I need to know: - The entry-point script(s), e.g. `live_test`, `vibecomfy_live_test`, etc. - Where it uses `runpod-lifecycle` to provision pods - Where it does `uv sync --extra cuda124` and the VibeComfy/ComfyUI/custom-node install (which scripts on the pod, which bootstrap code) - How it currently configures `disk_size_gb`, image, env, branch/ref selection - Model-cache/reconciliation logic and node-schema validation hooks 2. **vibecomfy/** — find: - The install/bootstrap path on a RunPod (which script installs ComfyUI + custom nodes) - The version-pinning / requirements files - The `ready_templates` dir layout briefly 3. **runpod-lifecycle/** — find the public API for creating/terminating pods and any existing snapshot/image/network-volume support. 4. **docs/** (only files directly tied to live-test or migration validation, e.g. `migration-vibecomfy*.md`, `sprint-12-route-inventory.md`) — quote any existing notes on env contracts or prebuilt environments. Skip everything else in docs/. 5. **Skills** — check `.claude/` or any agent-discovery file that documents how future agents should run live tests (CLAUDE.md, skill manifests). Just list paths and one-line purpose. Report ~400 words. For each repo give: top-level layout (just relevant subpaths), the 3-6 key files with absolute paths and line numbers of the install/bootstrap commands, and any existing notion of caching/prebuilt images. Do NOT browse `.megaplan/` or unrelated docs. Stop once you have the touch points.

> AGENT

I'll survey these repos to understand the live-test harness and VibeComfy environment setup. Let me search systematically across the workspace.

> AGENT

Let me refine the search to find reigh-worker, vibecomfy, and the runpod-lifecycle location:

> AGENT

Good! Now let me search for live-test entry points in reigh-worker:

> AGENT

Let me search for files with "live" or "test" in their names in the reigh-worker/tests directory and look for CLI entry points:

> AGENT

Excellent! I found the live_test directory. Now let me search for vibecomfy bootstrap and runpod-lifecycle files:

> AGENT

Now let me search for vibecomfy installation scripts and runpod-lifecycle:

> AGENT

Let me check the main entry points for live_test and look for bootstrap logic:

> AGENT

Now let me search for the actual bootstrap functions in ssh_bootstrap.py:

> AGENT

Now let me check runpod-lifecycle and look for vibecomfy's setup:

> AGENT

Now let me check vibecomfy's structure and ready_templates:

> AGENT

Now let me check for docs related to live-test or prebuilt environments:

> AGENT

Now let me check for CLAUDE.md or agent discovery in .claude:

> AGENT

Let me check runpod-lifecycle for more specific API details:

> AGENT

Let me search for the launch function signature:

> AGENT

Now let me look at the variant_fresh.py to understand the flow of pod launching and environment configuration:

> AGENT

Perfect! Now let me check vibecomfy's pyproject.toml for requirements:

> AGENT

Excellent context. Now let me do a final check for custom_nodes.lock and prepare my findings:

> AGENT

Perfect! Now I have enough information to compile the comprehensive survey. Let me generate the report. --- ## Summary: Reusable PrebuiltRunPod/VibeComfy Validation Environment Survey **Workspace:** `/Users/user_c042661f/Documents/reigh-workspace` ### 1. **reigh-worker/** — Live-Test Harness **Top-level paths:** - Entry point: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/main.py` (lines 1–100) - SSH bootstrap & pod lifecycle: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ssh_bootstrap.py` (lines 1–366) - Config & RunPod defaults: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/config.py` (lines 1–203) - Variant-fresh (pod provisioning): `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/variant_fresh.py` (lines 1–250+) **Key bootstrap commands:** 1. **uv sync + install** (`ssh_bootstrap.py:166–196`): APT packages, uv installation, `uv sync --extra cuda124` with retry logic, hardlink-disabled copy mode for MooseFS network volumes. 2. **VibeComfy checkout + install** (`ssh_bootstrap.py:199–236`): Clone VibeComfy branch, `pip install -e`, install HiddenSwitch ComfyUI fork + ComfyScript, run `vibecomfy.cli nodes restore --lockfile custom_nodes.lock`, validate template_index.json & coverage.json. 3. **SageAttention optional install** (`ssh_bootstrap.py:65–77`): Conditional based on `VIBECOMFY_ATTENTION_PROFILE`; clones & installs from `thu-ml/SageAttention`. **RunPod config:** - GPU type resolution (`variant_fresh.py:168–186`): Calls `runpod_lifecycle.api.find_gpu_type(requested_gpu_type, api_key)` - Image, disk, memory (`config.py:89–100`): Defaults to `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`, 50 GB container + 200 GB live-test overrides, storage volumes fallback chain (Peter → EU-NO-1 → EU-CZ-1 → EUR-IS-1), RAM tiers (72–16 GB) - VibeComfy env injection (`variant_fresh.py:103–130`): `REIGH_BACKEND`, `VIBECOMFY_PATH`, `VIBECOMFY_ATTENTION_PROFILE`, `REIGH_SELECTOR_NAMESPACE`, worker profile **No prebuilt image/snapshot concept yet:** All live tests start from base image + 46min uv sync + 21min VibeComfy install. --- ### 2. **vibecomfy/** — VibeComfy Install & Templates **Top-level paths:** - Ready templates root: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/ready_templates/` (subdirs: smoke, image, video, edit, audio) - Bootstrap script (VibeComfy): Handled entirely by `reigh-worker/scripts/live_test/ssh_bootstrap.py:199–236` on the pod. - Custom nodes lock: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/custom_nodes.lock` (pins KJNodes, QwenTTS, WanVideoWrapper, etc.) - Project config: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/pyproject.toml` (lines 1–50) **Template index:** `template_index.json` (generated by `refresh_template_index`) + manifest: `vibecomfy/workflow_corpus/manifests/coverage.json` **No RunPod prebuilt setup:** VibeComfy has scripts `runpod_validate.py`, `runpod_model_matrix.py`, `runpod_corpus_matrix.py` for independent GPU runs; these are *separate* from reigh-worker live-test harness. --- ### 3. **runpod-lifecycle/** — Pod Provisioning API **Top-level paths:** - Main API: `/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/__init__.py` (lines 1–66) - Lifecycle orchestration: `/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/lifecycle.py` (lines 205–284, async launch signature) **Public API surface:** - `launch(config: RunPodConfig, *, name, hooks)` — Returns `Pod` object (async) - `find_gpu_type(gpu_type_str, api_key)` — Resolves GPU by name string - `get_network_volumes(api_key)` — Lists available storage - `create_network_volume(...)` — Creates persistent volume - No built-in snapshot/image creation; all pods spawn from base image + SSH bootstrap upload **Config fields:** `gpu_type_candidates` (list), `min_memory_gb`, `disk_size_gb`, `container_disk_gb`, `volume_mount_path`, `storage_name` + `storage_volumes` (fallback chain), `ram_tiers` (tuple for fallback), `ssh_public_key_path`, `worker_image`, `template_id` --- ### 4. **docs/** — Migration & Validation **Live-test & prebuilt relevant docs:** - `/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy-live-validation.md` (lines 1–100+): Defines execution primitives (Python […]
