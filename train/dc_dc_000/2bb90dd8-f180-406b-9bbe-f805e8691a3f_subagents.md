> DEVELOPER

I need you to explore the reigh-worker repo at /Users/user_c042661f/Documents/reigh-workspace/reigh-worker for Sprint 3 of the Wan2GP fork migration. I need concrete findings — file paths, line numbers, current content — to write an implementation plan. Please gather the following information: 1. **Wan2GP submodule state**: Is `Wan2GP/` a git submodule now? Check `.gitmodules` and `git submodule status` from the repo root. What commit is it pinned to? What does the `banodoco/Wan2GP` fork look like — is there a `reigh-sprint-2` branch? What about `reigh-sprint-3`? Run `cd Wan2GP && git log --oneline -10 && git status && git branch -a` to understand. 2. **models/ltx2/ hot zone current state**: List the files in `Wan2GP/models/ltx2/` (just the directory, not deep recursive). Of those 22 files mentioned as differing, what's the drift right now vs. upstream? Focus on: - `Wan2GP/models/ltx2/ltx_core/tools.py` — read lines 50-100 to confirm the `clear_conditioning` function is present, and capture its exact content (byte-level) so we know the baseline to compare against. - Does `Wan2GP/defaults/ltx2_22B_distilled_1_1.json` exist yet? If not, what other `ltx2_*.json` defaults exist for comparison? 3. **IC-LoRA override code**: Read `source/core/params/travel_guidance.py` to understand: - The `_IC_LORA_BY_MODE` registry (around line 32-37 per the plan) — what modes does it currently have, what are the paths/names/strengths? - The `get_ic_lora_entry()` function around line 310-314 and its cameraman override branch - `_IC_LORA_UNION_CONTROL` constant — what's its value? - `TravelGuidanceConfig` dataclass — what fields does it have (kind, mode, etc.)? Is `strength` a field? 4. **Task registry dedup**: Read `source/task_handlers/tasks/task_registry.py` lines 940-990 to understand the dedup logic that compares basenames. Capture how the auto-inject drives the dedup — function name, what keys it expects in the segment_loras list items, etc. 5. **Existing test patterns**: Look at `tests/test_travel_guidance_config.py` (first 80 lines or so, plus check for fixtures) so we know what existing helpers/imports are used. Also check `tests/` directory for any `conftest.py` and list all existing test files. 6. **clear_conditioning fixture**: Is there already a saved latent fixture anywhere? Search for `.pt`, `.npy`, `.safetensors` files under `tests/` and `fixtures/`. Also search for `clear_conditioning` references in `tests/` and `scripts/`. 7. **scripts/live_test/**: What's in this untracked directory (from `git status`)? It appeared in Sprint 2 — is there a smoke test setup there we should reuse? 8. **Sprint 2 smoke venv reference**: Search the docs or prior plan outputs for `/tmp/sprint2-smoke-venv` references — is there a script that builds that venv? Also check `.megaplan/` for any Sprint 2 outputs that […]

> AGENT

I'll systematically explore the repo to gather these Sprint 3 baseline findings. Let me start with parallel searches.

> AGENT

Now let me check the git submodule state and other foundational information:

> AGENT

Good, `.gitmodules` shows it's a submodule on `reigh-sprint-2` branch. Let me check the Wan2GP state directly:

> AGENT

Let me check these files without changing directory:

> AGENT

Let me continue with file exploration while keeping the focus on reading the main repo files:

> AGENT

Now let me read more of the travel_guidance file to get the complete picture of the get_ic_lora_entry and TravelGuidanceConfig:

> AGENT

Now let me check the test files and fixtures:

> AGENT

Let me search for fixture data and clear_conditioning references:

> AGENT

Let me check the scripts/live_test directory and conftest:

> AGENT

Now let me search for .megaplan and any Sprint 2 venv references:

> AGENT

Good! Let me check the Wan2GP tools.py file and the megaplan directory:

> AGENT

Let me check the megaplan/plans directory and search for any ltx2_*.json defaults:

> AGENT

Now let me check the Sprint 2 plan outputs and look at the files more closely:

> AGENT

Perfect! Now let me read the rest of the migration plan to understand the context for Sprint 3:

> AGENT

Excellent! Now let me verify the exact content of the clear_conditioning function and check one more key registry detail:

> AGENT

Perfect! Now let me create a concise final report with all the key findings: ## Sprint 3 Baseline Findings Report ### 1. Wan2GP Submodule State **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.gitmodules` - Wan2GP IS a git submodule (lines 1-4) - Branch pinned to: `reigh-sprint-2` - URL: `https://github.com/banodoco/Wan2GP.git` - Directory: `Wan2GP/` at repo root **Status:** Git submodule is already configured from Sprint 2. Awaiting branch creation for `reigh-sprint-3` on the banodoco fork. ### 2. Models/ltx2 Hot Zone — Current Baseline **File Structure:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/` exists with subdirectories: - `configs/` (ltx2_22b_config.json, ltx2_19b_config.json, ltx2_rgb_factors.json) - `ltx_core/` (contains tools.py) - `ltx_pipelines/` (contains utils/ subdirectory) - Total tools.py file: 188 lines **clear_conditioning Function:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/ltx_core/tools.py:66-79` ```python def clear_conditioning(self, latent_state: LatentState) -> LatentState: """ Clear the conditioning from the latent state. This method removes extra tokens from the end of the latent. Therefore, conditioning items should add extra tokens ONLY to the end of the latent. """ latent_state = latent_state.clone() num_tokens = self.patchifier.get_token_count(self.target_shape) latent = latent_state.latent[:, :num_tokens] clean_latent = latent_state.clean_latent[:, :num_tokens] denoise_mask = torch.ones_like(latent_state.denoise_mask)[:, :num_tokens] positions = latent_state.positions[:, :, :num_tokens] return LatentState(latent=latent, denoise_mask=denoise_mask, positions=positions, clean_latent=clean_latent) ``` **Defaults:** `ltx2_22B_distilled.json` exists at `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled.json`. **Missing:** `ltx2_22B_distilled_1_1.json` (planned addition per Sprint 3 spec, not yet present). ### 3. IC-LoRA Registry & Override Code **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py` **Registry Location (lines 29-37):** ```python _IC_LORA_UNION_CONTROL = "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors" _IC_LORA_BY_MODE: dict[str, tuple[str, str | None]] = { "cameraman": ( [REDACTED], "https://huggingface.co/Cseti/LTX2.3-22B_IC-LoRA-Cameraman_v1/resolve/main/LTX2.3-22B_IC-LoRA-Cameraman_v1_10500.safetensors", ), } ``` **get_ic_lora_entry() Method (lines 305-325):** - Returns `None` if `needs_ic_lora()` is False - For cameraman: uses URL from `_IC_LORA_BY_MODE` with strength - For pose/depth/canny: falls back to `_IC_LORA_UNION_CONTROL` (filename only, no URL) - Strength is pulled from `control_strength` (hybrid) or `strength` (ltx_control) - Returns dict with keys: `path`, `strength`, `name` **TravelGuidanceConfig Dataclass (lines 122-151):** - `kind` field (Literal, default "none") - `strength` field (float, default 0.0) — YES, exists at line 130 - `mode` field (str, default "") - `control_strength` field (float, default 1.0) - All control modes: `{"pose", "depth", "canny", "video", "cameraman"}` (line 27) ### 4. Task Registry Dedup Logic **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/tasks/task_registry.py:940-990` **IC LoRA Auto-Inject + Dedup Flow (lines 955-970):** - Triggers when `structure.structure_config` is `TravelGuidanceConfig` instance - Calls `structure.structure_config.get_ic_lora_entry()` (line 958) - Dedup compares `os.path.basename(existing.get("path", ""))` against `ic_basename` (lines 962-968) - If match found: updates `strength` in-place and sets `found = True` - If no match: appends `ic_entry` to `segment_loras` list - Each dict item in `segment_loras` expects keys: `"path"` and `"strength"` ### 5. Existing Test Patterns **File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_travel_guidance_config.py:1-80` **Imports & Fixtures:** - Line 1: `import pytest` […]
