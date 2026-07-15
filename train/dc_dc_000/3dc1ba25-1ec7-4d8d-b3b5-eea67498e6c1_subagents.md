> DEVELOPER

I'm planning a reusable prebuilt RunPod/VibeComfy validation environment to skip the slow ~46min uv sync + 21min VibeComfy install on every live test.

Survey these repos/dirs under `/Users/user_c042661f/Documents/reigh-workspace/`:

1. **reigh-worker/** — find the live-test harness/CLI that spins up a RunPod and runs VibeComfy workflows. I need to know:
   - The entry-point script(s), e.g. `live_test`, `vibecomfy_live_test`, etc.
   - Where it uses `runpod-lifecycle` to provision pods
   - Where it does `uv sync --extra cuda124` and the VibeComfy/ComfyUI/custom-node install (which scripts on the pod, which bootstrap code)
   - How it currently configures `disk_size_gb`, image, env, branch/ref selection
   - Model-cache/reconciliation logic and node-schema validation hooks

2. **vibecomfy/** — find:
   - The install/bootstrap path on a RunPod (which script installs ComfyUI + custom nodes)
   - The version-pinning / requirements files
   - The `ready_templates` dir layout briefly

3. **runpod-lifecycle/** — find the public API for creating/terminating pods and any existing snapshot/image/network-volume support.

4. **docs/** (only files directly tied to live-test or migration validation, e.g. `migration-vibecomfy*.md`, `sprint-12-route-inventory.md`) — quote any existing notes on env contracts or prebuilt environments. Skip everything else in docs/.

5. **Skills** — check `.claude/` or any agent-discovery file that documents how future agents should run live tests (CLAUDE.md, skill manifests). Just list paths and one-line purpose.

Report ~400 words. For each repo give: top-level layout (just relevant subpaths), the 3-6 key files with absolute paths and line numbers of the install/bootstrap commands, and any existing notion of caching/prebuilt images. Do NOT browse `.megaplan/` or unrelated docs. Stop once you have the touch points.

> AGENT

I'll survey these repos to understand the live-test harness and VibeComfy environment setup. Let me search systematically across the workspace.

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace -maxdepth 2 -type d | grep -E \"(reigh-worker|vibecomfy|runpod-lifecycle|docs|\\.claude)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/text-ip-adapter/docs
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/tasks
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/gpu_orchestrator
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.pytest_cache
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.uv-cache
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/config
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/orchestrator_common
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/tests
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.claude
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/docs
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.megaplan
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/scripts
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.desloppify
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/runpod_lifecycle
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.git
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/api_orchestrator
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/sql
/Users/user_c042661f/Documents/reigh-workspace/megaplan-fix/docs
/Users/user_c042661f/Documents/reigh-workspace/.claude
```

> AGENT

Let me refine the search to find reigh-worker, vibecomfy, and the runpod-lifecycle location:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/ | grep -E \"^d\" | awk '{print $NF}'"
}
```

> TOOL

tool_result Bash
```
This Bash command contains multiple operations. The following part requires approval: awk '{print $NF}'
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -d /Users/user_c042661f/Documents/reigh-workspace/*/ 2>/dev/null | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/Astrid/
/Users/user_c042661f/Documents/reigh-workspace/artagents-projects/
/Users/user_c042661f/Documents/reigh-workspace/astrid-projects/
/Users/user_c042661f/Documents/reigh-workspace/docs/
/Users/user_c042661f/Documents/reigh-workspace/megaplan-fix/
/Users/user_c042661f/Documents/reigh-workspace/outputs/
/Users/user_c042661f/Documents/reigh-workspace/packages/
/Users/user_c042661f/Documents/reigh-workspace/prompt-adapters/
/Users/user_c042661f/Documents/reigh-workspace/reigh-app-cloud-chain/
/Users/user_c042661f/Documents/reigh-workspace/reigh-app/
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/
/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/
/Users/user_c042661f/Documents/reigh-workspace/scripts/
/Users/user_c042661f/Documents/reigh-workspace/text-ip-adapter/
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy-backups/
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/
```

> AGENT

Good! Now let me search for live-test entry points in reigh-worker:

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/**/*live*test*"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/**/*.py"
}
```

> TOOL

tool_result Glob
```
reigh-worker/source/core/__init__.py
reigh-worker/source/core/constants.py
reigh-worker/source/media/__init__.py
reigh-worker/source/models/__init__.py
reigh-worker/source/models/comfy/__init__.py
reigh-worker/source/models/model_handlers/__init__.py
reigh-worker/source/task_handlers/__init__.py
reigh-worker/source/task_handlers/worker/__init__.py
reigh-worker/source/core/log/timing.py
reigh-worker/source/models/model_handlers/qwen_prompts.py
reigh-worker/source/models/wgp/__init__.py
reigh-worker/source/models/wgp/generators/__init__.py
reigh-worker/source/utils/prompt_utils.py
reigh-worker/tests/test_task_result_protocol.py
reigh-worker/tests/test_chatterbox_s3gen_direct_coverage.py
reigh-worker/tests/test_lora_formats_baseline.py
reigh-worker/tests/test_wan2gp_direct_coverage_remaining.py
reigh-worker/tests/test_param_precedence_contracts.py
reigh-worker/tests/test_plugin.py
reigh-worker/tests/test_wgp_output_contracts.py
reigh-worker/tests/test_output_paths_contracts.py
reigh-worker/tests/test_video_storage_upload_contracts.py
reigh-worker/tests/test_structure_treatment_contracts.py
reigh-worker/tests/test_travel_segment_types_contracts.py
reigh-worker/tests/test_log_context_scoping.py
reigh-worker/tests/test_clip_preprocessor.py
reigh-worker/tests/test_video_info_contracts.py
reigh-worker/tests/test_runtime_boundaries.py
reigh-worker/tests/test_remaining_module_coverage.py
reigh-worker/tests/test_split_helper_modules.py
reigh-worker/tests/test_task_metadata_split.py
reigh-worker/tests/test_structure_guidance_parsing_split.py
reigh-worker/tests/test_transition_prompt_templates.py
reigh-worker/tests/test_composite_result_split.py
reigh-worker/tests/test_queue_status_wait.py
reigh-worker/tests/test_task_dependencies_split_modules.py
reigh-worker/tests/test_structure_pipeline_contracts.py
reigh-worker/tests/test_wgp_params_overrides.py
reigh-worker/tests/test_failure_semantics_contracts.py
reigh-worker/tests/test_error_consistency_contracts.py
reigh-worker/tests/test_wan_orchestrator_collaborators.py
reigh-worker/source/task_handlers/join/__init__.py
reigh-worker/source/task_handlers/join/vace_quantization.py
reigh-worker/tests/test_task_polling_helpers.py
reigh-worker/tests/test_guide_video_request_api.py
reigh-worker/tests/test_travel_segment_queue_contracts.py
reigh-worker/tests/test_dispatch_payload_contracts.py
reigh-worker/tests/test_vace_frame_contracts.py
reigh-worker/tests/test_join_transition_contracts.py
reigh-worker/tests/test_travel_api_wrappers.py
reigh-worker/tests/test_critical_seams_contracts.py
reigh-worker/tests/test_debug_option_contracts.py
reigh-worker/tests/test_debug_diagnostics_and_uni3c.py
reigh-worker/tests/test_orchestrator_alias_resolution.py
reigh-worker/tests/test_output_paths_filename_policy.py
reigh-worker/tests/test_travel_payload_contracts.py
reigh-worker/tests/test_dispatch_contracts.py
reigh-worker/tests/test_travel_guide_module_alias.py
reigh-worker/tests/test_polling_policy.py
reigh-worker/tests/test_join_shared_idempotency_gating.py
reigh-worker/tests/test_wgp_bridge_contracts.py
reigh-worker/tests/test_queue_runtime_and_finalization_service.py
reigh-worker/tests/test_mask_generation_and_utils.py
reigh-worker/source/task_handlers/queue/__init__.py
reigh-worker/tests/test_db_runtime_error_contracts.py
reigh-worker/tests/test_uni3c_validation_contracts.py
reigh-worker/tests/test_task_registry_lazy_contracts.py
reigh-worker/tests/test_task_result_handler_contracts.py
reigh-worker/tests/test_root_shims_contracts.py
reigh-worker/tests/test_media_namespace_contracts.py
reigh-worker/tests/test_wgp_init_bootstrap_contracts.py
reigh-worker/tests/test_video_transform_api_contracts.py
reigh-worker/tests/test_runtime_model_patch_contracts.py
reigh-worker/tests/test_join_orchestrator_payload_contracts.py
reigh-worker/tests/test_video_api_facade_contracts.py
reigh-worker/tests/test_worker_postprocess_and_bootstrap_service_contracts.py
reigh-worker/tests/test_debug_helper_coverage.py
reigh-worker/tests/test_runtime_contracts_core_paths.py
reigh-worker/tests/test_task_status_return_contract.py
reigh-worker/tests/test_svi_preflight.py
reigh-worker/tests/test_debug_commands.py
reigh-worker/tests/test_task_dependencies_query_helpers.py
reigh-worker/tests/test_create_test_task_cli.py
reigh-worker/tests/test_transitive_direct_links_pass3.py
reigh-worker/tests/test_specialized_dispatch_contracts.py
reigh-worker/tests/test_runtime_registry_readonly_contracts.py
reigh-worker/tests/test_debug_split_module_coverage.py
reigh-worker/tests/test_edge_retry_contracts.py
reigh-worker/tests/test_high_import_facade_contracts.py
reigh-worker/tests/test_examples_cli.py
reigh-worker/tests/test_worker_auth_mode_contracts.py
reigh-worker/tests/test_worker_bootstrap_gate_contracts.py
reigh-worker/tests/test_video_brightness_contracts.py
reigh-worker/tests/test_edge_retry_helpers_contracts.py
reigh-worker/tests/test_video_brightness_module_contracts.py
reigh-worker/tests/test_debug_command_registry_contracts.py
reigh-worker/tests/test_task_dispatch_manifest_contracts.py
reigh-worker/tests/test_task_polling_contracts.py
reigh-worker/tests/test_task_polling_result_contracts.py
reigh-worker/debug/__init__.py
(Results are truncated. Consider using a more specific path or pattern.)
```

> AGENT

Let me search for files with "live" or "test" in their names in the reigh-worker/tests directory and look for CLI entry points:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/reigh-worker -name \"*live*\" -o -name \"*cli*\" -o -name \"run*\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/run-docker-cuda-deb.sh
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/shared/cli_args.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/shared/api_cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/shared/deepy/cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/wan/modules/clip.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/TTS/index_tts2/cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/postprocessing/mmaudio/runner.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/scripts/run.bat
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/scripts/run.sh
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/__pycache__/runtime_paths.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/__pycache__/runtime_paths.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/__pycache__/runtime_paths.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/runtime_paths.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/entrypoints/__pycache__/run_worker.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/entrypoints/__pycache__/run_worker.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/entrypoints/__pycache__/run_worker.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/entrypoints/run_worker.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/wgp_ports/__pycache__/runtime_registry.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/wgp_ports/__pycache__/runtime_registry.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/wgp_ports/__pycache__/runtime_registry.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/runtime/wgp_ports/runtime_registry.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/utils/cli_error_boundary.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/utils/__pycache__/cli_error_boundary.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/utils/__pycache__/cli_error_boundary.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/utils/__pycache__/cli_error_boundary.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/models/wgp/__pycache__/runtime_services.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/models/wgp/runtime_services.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/clip_validator.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/__pycache__/clip_validator.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/__pycache__/clip_validator.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/__pycache__/clip_validator.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/__pycache__/clip_preprocessor.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/__pycache__/clip_preprocessor.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/join/clip_preprocessor.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_debug_cli_and_formatters.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_clip_preprocessor.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_travel_stitch_explicit_clips.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/runtime
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_examples_cli.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_clip_preprocessor.cpython-314-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_create_test_task_cli.cpython-314-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_examples_cli.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_debug_cli_and_formatters.cpython-310-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_debug_cli_and_formatters.cpython-314-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_travel_stitch_explicit_clips.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_travel_stitch_explicit_clips.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_create_test_task_cli.cpython-310-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_clip_preprocessor.cpython-310-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_examples_cli.cpython-310-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_debug_cli_and_formatters.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_debug_cli_and_formatters.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_travel_stitch_explicit_clips.cpython-314-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_travel_stitch_explicit_clips.cpython-310-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_clip_preprocessor.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_create_test_task_cli.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_create_test_task_cli.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_examples_cli.cpython-314-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/__pycache__/test_clip_preprocessor.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_examples_cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_create_test_task_cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/__pycache__/run_worker.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/supabase/.temp/cli-latest
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/examples/join_clips_example.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/examples/__pycache__/join_clips_example.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/run_worker_matrix.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/__pycache__/run_worker_matrix.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/__pycache__/db_client.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/db_client.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/runs
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/preview/run_preview.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/preview/__pycache__/run_preview.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/capability_contracts/live_matrix_manifest.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T053546Z/run_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T053530Z/run_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T053516Z/run_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T050302Z/runpod_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T050302Z/run_sprint35_vibecomfy_candidate.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/vibecomfy_candidate/20260506T050302Z/runpod_session.log
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043213Z/runpod_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043213Z/runpod_session.log
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043327Z/runpod_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043327Z/runpod_session.log
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T044342Z/run_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043642Z/runpod_metadata.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/artifacts/sprint35/wgp_reference/20260506T043642Z/runpod_session.log
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/golden/join_clips_segment__model-wan22_vace__guidance-vace__continuity-join_bridge__profile-default
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/__pycache__/runtime_metrics.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/__pycache__/runtime_metrics.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/fixtures/golden_seed_payloads/join_clips_segment__model-wan22_vace__guidance-vace__continuity-join_bridge__profile-default.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/dual_run_compare/runtime_metrics.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_213624/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_160109/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_211122/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_205717/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_123001/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_134841/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_060903/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_020849/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260301_015937/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_024017/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_011245/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_212027/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_205451/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_212620/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_050849/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_051213/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_112805/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_201941/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_043340/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_112542/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_012719/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_041351/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_034819/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_233631/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_044727/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_023151/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_113150/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_052739/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_160807/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_205135/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_002131/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_144653/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_214930/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_212808/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_160514/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_045433/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_113938/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_210214/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_011439/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_112217/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_172617/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_202831/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_054931/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_035225/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_054103/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_045338/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260301_033803/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_124556/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_062207/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260301_011538/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_161012/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_192229/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_020535/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_225524/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_053607/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_145414/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_122438/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_060645/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_151532/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_001552/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_033651/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_010849/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_055907/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260301_002802/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_230451/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260301_012409/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_051842/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_213244/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_061730/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_030516/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_214043/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_152733/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_120914/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_042011/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_201100/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_191935/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_210707/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_042106/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_153444/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_222053/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_060324/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_222712/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_184417/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260227_224229/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_211222/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_231222/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260228_040521/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.desloppify/subagents/runs/20260226_042734/run_summary.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/logs/refs/heads/runpod-lifecycle-migration
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/logs/refs/heads/live-test
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/logs/refs/remotes/origin/runpod-lifecycle-migration
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/logs/refs/remotes/origin/live-test
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/refs/heads/runpod-lifecycle-migration
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/refs/heads/live-test
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/refs/remotes/origin/runpod-lifecycle-migration
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.git/refs/remotes/origin/live-test
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/outputs/preview_join_output/join_clips_run_preview-join-run-0002
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/outputs/join_clips_segment
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/run_worker.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/client.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_system.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_system.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_workers.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_workers.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_workers.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/runtime_queries_system.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/client.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/client.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/client.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/cli.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/cli.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/__pycache__/cli.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/runtime_queries_system.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/cli.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/runtime_queries_workers.py
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/commands/__pycache__/runpod.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/commands/__pycache__/runpod.cpython-310.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/commands/__pycache__/runpod.cpython-314.pyc
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/debug/commands/runpod.py
```

> AGENT

Excellent! I found the live_test directory. Now let me search for vibecomfy bootstrap and runpod-lifecycle files:

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/**/*.py"
}
```

> TOOL

tool_result Glob
```
reigh-worker/scripts/live_test/logger.py
reigh-worker/scripts/live_test/safety_gate.py
reigh-worker/scripts/live_test/stage1_probe.py
reigh-worker/scripts/live_test/token_resolver.py
reigh-worker/scripts/live_test/git_ops.py
reigh-worker/scripts/live_test/task_spoofer.py
reigh-worker/scripts/live_test/heartbeat_waiter.py
reigh-worker/scripts/live_test/config.py
reigh-worker/scripts/live_test/completion_poller.py
reigh-worker/scripts/live_test/inspect.py
reigh-worker/scripts/live_test/main.py
reigh-worker/scripts/live_test/__init__.py
reigh-worker/scripts/live_test/db_client.py
reigh-worker/scripts/live_test/launch_command.py
reigh-worker/scripts/live_test/preflight.py
reigh-worker/scripts/live_test/smoke.py
reigh-worker/scripts/live_test/terminate_guard.py
reigh-worker/scripts/live_test/matrix.py
reigh-worker/scripts/live_test/ssh_bootstrap.py
reigh-worker/scripts/live_test/report.py
reigh-worker/scripts/live_test/variant_update.py
reigh-worker/scripts/live_test/variant_fresh.py
reigh-worker/scripts/live_test/tests/test_primitives.py
```

> AGENT

Now let me search for vibecomfy installation scripts and runpod-lifecycle:

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/**/*.sh"
}
```

> TOOL

tool_result Glob
```
vibecomfy/vendor/ComfyUI/.github/scripts/check-ai-co-authors.sh
vibecomfy/.venv/lib/python3.11/site-packages/tqdm/completion.sh
vibecomfy/out/runpod_artifacts/20260505T150006Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260505T151632Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260505T233347Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260506T175410Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260506T212136Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260507T020357Z/out/corpus_matrix/remote_run.sh
vibecomfy/out/runpod_artifacts/20260507T020859Z/out/corpus_matrix/remote_run.sh
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/**/*bootstrap* -o /Users/user_c042661f/Documents/reigh-workspace/vibecomfy/**/*install*"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/**/*.py"
}
```

> TOOL

tool_result Glob
```
vibecomfy/vibecomfy/nodes/__init__.py
vibecomfy/tests/test_scratchpad_loader.py
vibecomfy/vibecomfy/commands/logs.py
vibecomfy/vibecomfy/schema/cache.py
vibecomfy/vibecomfy/analysis/__init__.py
vibecomfy/tests/test_analysis.py
vibecomfy/vibecomfy/search/aliases.py
vibecomfy/vibecomfy/search/scorer.py
vibecomfy/tests/test_edge_primitives.py
vibecomfy/tests/test_controlnet_patch.py
vibecomfy/vibecomfy/cli.py
vibecomfy/vibecomfy/patches/types.py
vibecomfy/vibecomfy/patches/__init__.py
vibecomfy/vibecomfy/patches/resolution.py
vibecomfy/vibecomfy/patches/save_prefix.py
vibecomfy/vibecomfy/patches/seed.py
vibecomfy/vibecomfy/commands/index_files.py
vibecomfy/vibecomfy/search/__init__.py
vibecomfy/vibecomfy/commands/search.py
vibecomfy/vibecomfy/patches/builtins.py
vibecomfy/vibecomfy/patches/registry.py
vibecomfy/vibecomfy/patches/requirements.py
vibecomfy/vibecomfy/patches/controlnet.py
vibecomfy/vibecomfy/patches/gguf_unet.py
vibecomfy/vibecomfy/patches/ltx_lowvram.py
vibecomfy/vibecomfy/index_types.py
vibecomfy/vibecomfy/ingest/index.py
vibecomfy/vibecomfy/nodes/index.py
vibecomfy/vibecomfy/analysis/graph.py
vibecomfy/vibecomfy/search/index.py
vibecomfy/vibecomfy/runtime/client.py
vibecomfy/scripts/warm_session_smoke.py
vibecomfy/vibecomfy/commands/runtime.py
vibecomfy/out/runpod_artifacts/1777154866/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777154866/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777154866/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777154866/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777156171/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777156171/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777156171/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777157135/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777157135/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777157135/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777158263/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777158263/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777158263/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777158263/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777159483/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777166390/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_motion_track.scratchpad.py
vibecomfy/out/runpod_artifacts/1777166999/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_motion_track.scratchpad.py
vibecomfy/out/runpod_artifacts/1777170882/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_motion_track.scratchpad.py
vibecomfy/out/runpod_artifacts/1777170882/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_union_control.scratchpad.py
vibecomfy/out/runpod_artifacts/1777171710/out/corpus_matrix/logs/z_image.scratchpad.py
vibecomfy/out/runpod_artifacts/1777171710/out/corpus_matrix/logs/flux2_klein_4b_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777171710/out/corpus_matrix/logs/flux2_klein_9b_gguf_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777172662/out/corpus_matrix/logs/flux2_klein_4b_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777172662/out/corpus_matrix/logs/flux2_klein_4b_image_edit_distilled.scratchpad.py
vibecomfy/out/runpod_artifacts/1777173866/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777173866/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777173866/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777173866/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777175257/out/corpus_matrix/logs/z_image.scratchpad.py
vibecomfy/out/runpod_artifacts/1777175257/out/corpus_matrix/logs/flux2_klein_4b_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777175257/out/corpus_matrix/logs/flux2_klein_4b_image_edit_distilled.scratchpad.py
vibecomfy/out/runpod_artifacts/1777175257/out/corpus_matrix/logs/flux2_klein_9b_gguf_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777176644/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777176644/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777176644/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777180848/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777180848/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777180848/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777183379/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777183379/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777183379/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_flf2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777183379/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v_controlnet.scratchpad.py
vibecomfy/out/runpod_artifacts/1777183379/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777186120/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777186120/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777186120/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_flf2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777186120/out/corpus_matrix/logs/wanvideo_wrapper_22_5b_i2v_controlnet.scratchpad.py
vibecomfy/out/runpod_artifacts/1777186120/out/corpus_matrix/logs/wanvideo_wrapper_13b_control_lora.scratchpad.py
vibecomfy/out/runpod_artifacts/1777191469/out/corpus_matrix/logs/wanvideo_wrapper_21_14b_v2v_infinitetalk.scratchpad.py
vibecomfy/out/runpod_artifacts/1777195666/out/corpus_matrix/logs/ltx2_3_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777195666/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_motion_track.scratchpad.py
vibecomfy/out/runpod_artifacts/1777195666/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_union_control.scratchpad.py
vibecomfy/out/runpod_artifacts/1777204423/out/corpus_matrix/logs/ace_step_1_5_t2a_song.scratchpad.py
vibecomfy/out/runpod_artifacts/1777205920/out/corpus_matrix/logs/qwen_image_edit.scratchpad.py
vibecomfy/out/runpod_artifacts/1777205920/out/corpus_matrix/logs/z_image.scratchpad.py
vibecomfy/out/runpod_artifacts/1777205920/out/corpus_matrix/logs/flux2_klein_4b_t2i.scratchpad.py
vibecomfy/out/runpod_artifacts/1777205920/out/corpus_matrix/logs/flux2_klein_4b_image_edit_distilled.scratchpad.py
vibecomfy/out/runpod_artifacts/1777211608/out/corpus_matrix/logs/ltx2_3_t2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777211608/out/corpus_matrix/logs/ltx2_3_i2v.scratchpad.py
vibecomfy/out/runpod_artifacts/1777211608/out/corpus_matrix/logs/ltx2_3_lightricks_two_stage.scratchpad.py
vibecomfy/out/runpod_artifacts/1777211608/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_motion_track.scratchpad.py
vibecomfy/out/runpod_artifacts/1777211608/out/corpus_matrix/logs/ltx2_3_lightricks_iclora_union_control.scratchpad.py
vibecomfy/vibecomfy/fixtures.py
vibecomfy/tests/test_metadata_registration.py
vibecomfy/vibecomfy/commands/watchdog.py
vibecomfy/tests/test_fixtures.py
vibecomfy/tests/test_models_registry.py
(Results are truncated. Consider using a more specific path or pattern.)
```

> AGENT

Let me check the main entry points for live_test and look for bootstrap logic:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/main.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""CLI entrypoint for the live worker harness."""
2	
3	from __future__ import annotations
4	
5	import argparse
6	import sys
7	from datetime import datetime, timezone
8	
9	from scripts.live_test import config
10	from scripts.live_test.inspect import main as run_inspect
11	from scripts.live_test.variant_fresh import run as run_variant_fresh
12	from scripts.live_test.variant_update import run as run_variant_update
13	
14	
15	def build_parser() -> argparse.ArgumentParser:
16	    parser = argparse.ArgumentParser(description="Run the Reigh live worker harness.")
17	    parser.add_argument("--variant", choices=("fresh", "update"), required=True)
18	    parser.add_argument("--pod-id", help="Existing RunPod pod ID for update-mode takeover.")
19	    parser.add_argument(
20	        "--spawn-takeover",
21	        action="store_true",
22	        help="Spawn a fresh orchestrator-managed pod, then take it over with the local worker branch.",
23	    )
24	    termination_group = parser.add_mutually_exclusive_group()
25	    termination_group.add_argument("--no-terminate", dest="no_terminate", action="store_true")
26	    termination_group.add_argument("--terminate", dest="no_terminate", action="store_false")
27	    parser.set_defaults(no_terminate=None)
28	    parser.add_argument("--dry-run", action="store_true")
29	    parser.add_argument("--ref", default="main", help="Branch/ref to clone for Variant Fresh.")
30	    parser.add_argument(
31	        "--vibecomfy-ref",
32	        default="megaplan/production-parity-templates",
33	        help="VibeComfy branch/ref to clone for VibeComfy backend live tests.",
34	    )
35	    parser.add_argument("--wgp-profile", type=int, default=3)
36	    parser.add_argument(
37	        "--backend",
38	        choices=("wgp", "vibecomfy"),
39	        default="wgp",
40	        help="Worker backend to inject through REIGH_BACKEND.",
41	    )
42	    parser.add_argument(
43	        "--selector-namespace",
44	        default="production",
45	        help="Route selector namespace to inject into worker claim validation.",
46	    )
47	    parser.add_argument(
48	        "--selector-version",
49	        help="Optional route selector version to inject into worker claim validation.",
50	    )
51	    parser.add_argument(
52	        "--worker-contract-version",
53	        type=int,
54	        default=1,
55	        help="Worker route contract version to stamp into Reigh-shaped live-test tasks.",
56	    )
57	    parser.add_argument(
58	        "--worker-profile",
59	        default="default",
60	        help="Selected worker route profile to stamp into route-specific live-test tasks.",
61	    )
62	    parser.add_argument(
63	        "--case",
64	        action="append",
65	        default=[],
66	        help="Restrict the matrix to a case name. May be passed multiple times.",
67	    )
68	    parser.add_argument(
69	        "--task-type",
70	        action="append",
71	        default=[],
72	        help="Restrict the matrix to a task type. May be passed multiple times.",
73	    )
74	    parser.add_argument(
75	        "--route-key",
76	        action="append",
77	        default=[],
78	        help="Restrict the matrix to a route key. May be passed multiple times.",
79	    )
80	    parser.add_argument(
81	        "--wgp-rollback",
82	        action="store_true",
83	        help="Run the selected route/task cases in rollback mode by forcing REIGH_BACKEND=wgp.",
84	    )
85	    parser.add_argument(
86	        "--allow-fresh-heartbeat",
87	        action="store_true",
88	        help="Allow update-mode takeover of a pod that is already running this live-test worker.",
89	    )
90	    parser.add_argument("--timeout-image", type=int, default=config.TIMEOUT_IMAGE_SEC)
91	    parser.add_argument(
92	        "--timeout-travel-segment",
93	        type=int,
94	        default=config.TIMEOUT_INDIVIDUAL_TRAVEL_SEGMENT_SEC,
95	    )
96	    parser.add_argument(
97	        "--timeout-travel-orchestrator",
98	        type=int,
99	        default=config.TIMEOUT_TRAVEL_ORCHESTRATOR_SEC,
100	    )
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ssh_bootstrap.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""SSH-side worker bootstrap helpers shared by the live-test variants."""
2	
3	from __future__ import annotations
4	
5	import os
6	import shlex
7	from dataclasses import dataclass
8	import time
9	from typing import Literal
10	
11	import scripts.live_test as live_test_pkg
12	
13	
14	APT_INSTALL_PACKAGES = (
15	    "python3.10-venv",
16	    "python3.10-dev",
17	    "build-essential",
18	    "ffmpeg",
19	    "git",
20	    "curl",
21	    "wget",
22	)
23	PROCESS_SCAN_COMMAND = (
24	    r"ps -eo pid=,args= | awk '/run_worker[.]py|python[^ ]* .*worker[.]py|source[.]runtime[.]worker/ {print}'"
25	)
26	KILL_COMMAND = (
27	    "pkill -f 'run_worker[.]py'; "
28	    "pkill -f 'python worker[.]py'; "
29	    "pkill -f 'python[^ ]* .*worker[.]py'; "
30	    "pkill -f 'source[.]runtime[.]worker'; "
31	    "sleep 5; "
32	    "pkill -9 -f 'run_worker[.]py' || true; "
33	    "pkill -9 -f 'python worker[.]py' || true; "
34	    "pkill -9 -f 'python[^ ]* .*worker[.]py' || true; "
35	    "pkill -9 -f 'source[.]runtime[.]worker' || true; "
36	    "sleep 2"
37	)
38	
39	
40	@dataclass(frozen=True)
41	class WorkerProcessInfo:
42	    family: Literal["supervisor", "direct"]
43	    cmdline: list[str]
44	    pid: int
45	
46	
47	def _quote(value: str) -> str:
48	    return shlex.quote(str(value))
49	
50	
51	def _resolve_attention_profile(raw: str | None = None) -> str:
52	    value = (
53	        raw
54	        or os.environ.get("REIGH_VIBECOMFY_ATTENTION_PROFILE")
55	        or os.environ.get("VIBECOMFY_ATTENTION_PROFILE")
56	        or ""
57	    ).strip().lower()
58	    if value in {"", "default", "portable", "sdpa"}:
59	        return "portable"
60	    if value in {"optimized", "sage", "sageattn", "sageattention"}:
61	        return "sage"
62	    raise ValueError("VibeComfy attention profile must be 'portable' or 'sage'")
63	
64	
65	def _sageattention_install_block(python_path: str) -> str:
66	    py = _quote(python_path)
67	    return (
68	        "rm -rf /tmp/sageattention\n"
69	        "git clone --depth 1 https://github.com/thu-ml/SageAttention.git /tmp/sageattention\n"
70	        f"{py} -m pip install --no-build-isolation /tmp/sageattention\n"
71	        f"{py} - <<'PY'\n"
72	        "import sageattention\n"
73	        "if not callable(getattr(sageattention, 'sageattn', None)):\n"
74	        "    raise RuntimeError('sageattention import succeeded but sageattn is missing')\n"
75	        "print('sageattention verified')\n"
76	        "PY\n"
77	    )
78	
79	
80	def _execute(ssh, command: str, *, timeout: int = 600, check: bool = True) -> tuple[str, str]:
81	    exit_code, stdout, stderr = ssh.execute_command(command, timeout=timeout)
82	    if check and exit_code != 0:
83	        raise RuntimeError(
84	            f"Remote command failed with exit {exit_code}: {command}\nstdout:\n{stdout}\nstderr:\n{stderr}"
85	        )
86	    return stdout, stderr
87	
88	
89	def open_session(pod_id: str, api_key: str, *, ssh_wait_timeout: int = 300, poll_interval: int = 5):
90	    deadline = time.monotonic() + ssh_wait_timeout
91	    ssh_details = None
92	    last_status = None
93	    while time.monotonic() < deadline:
94	        ssh_details = live_test_pkg.get_pod_ssh_details(pod_id, api_key)
95	        if ssh_details and ssh_details.get("ip") and ssh_details.get("port"):
96	            break
97	        try:
98	            last_status = live_test_pkg.get_pod_status(pod_id, api_key)
99	        except Exception:
100	            last_status = None
101	        time.sleep(poll_interval)
102	    if not ssh_details or not ssh_details.get("ip") or not ssh_details.get("port"):
103	        status_hint = _format_pod_status_hint(last_status)
104	        raise RuntimeError(
105	            f"Could not resolve SSH details for pod {pod_id} within {ssh_wait_timeout}s{status_hint}"
106	        )
107	
108	    import os as _os
109	    private_key_path = _os.environ.get("REIGH_LIVE_TEST_SSH_KEY") or "~/.ssh/id_ed25519"
110	    ssh = live_test_pkg.SSHClient(
111	        hostname=str(ssh_details["ip"]),
112	        port=int(ssh_details["port"]),
113	        username="root",
114	        [REDACTED]("password"),
115	        private_key_path=private_key_path,
116	    )
117	    connect_deadline = time.monotonic() + ssh_wait_timeout
118	    last_err: Exception | None = None
119	    while time.monotonic() < connect_deadline:
120	        try:
121	            ssh.connect()
122	            return ssh
123	        except Exception as exc:
124	            last_err = exc
125	            try:
126	                last_status = live_test_pkg.get_pod_status(pod_id, api_key)
127	            except Exception:
128	                last_status = None
129	            time.sleep(poll_interval)
130	    status_hint = _format_pod_status_hint(last_status)
131	    raise RuntimeError(f"Could not SSH into pod {pod_id} within {ssh_wait_timeout}s{status_hint}: {last_err}")
132	
133	
134	def _format_pod_status_hint(status) -> str:
135	    if not isinstance(status, dict):
136	        return "; latest pod status unavailable"
137	    desired = status.get("desired_status") or status.get("desiredStatus") or "unknown"
138	    actual = status.get("actual_status") or status.get("actualStatus") or status.get("status") or "unknown"
139	    ip = status.get("ip") or "none"
140	    ports = status.get("ports")
141	    if isinstance(ports, list) and ports:
142	        rendered_ports = []
143	        for port in ports:
144	            if not isinstance(port, dict):
145	                continue
146	            private = port.get("privatePort") or port.get("private_port") or port.get("containerPort")
147	            public = port.get("publicPort") or port.get("public_port") or port.get("hostPort")
148	            if private and public:
149	                rendered_ports.append(f"{private}->{public}")
150	        ports_text = ",".join(rendered_ports) if rendered_ports else "unparseable"
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/variant_fresh.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	"""Variant A driver: launch a fresh pod and run the live-test matrix."""
2	
3	from __future__ import annotations
4	
5	import asyncio
6	from contextlib import contextmanager
7	import io
8	from datetime import datetime, timezone
9	from pathlib import Path
10	import re
11	import sys
12	import time
13	from typing import Any
14	
15	from scripts.live_test import config
16	from scripts.live_test.heartbeat_waiter import wait_until_ready
17	from scripts.live_test.launch_command import build_run_worker_command
18	from scripts.live_test.logger import get_logger
19	from scripts.live_test.matrix import build_matrix, poll_queued_matrix, queue_matrix, render_case_payload
20	from scripts.live_test.preflight import (
21	    assert_user_queue_clean,
22	    close_stale_live_test_tasks,
23	    ensure_live_test_route_selectors,
24	    ensure_user_cloud_generation_enabled,
25	    get_or_create_live_test_project,
26	)
27	from scripts.live_test.report import all_results_passed, write_report
28	from scripts.live_test.ssh_bootstrap import (
29	    clone_and_install_vibecomfy,
30	    clone_repo_into,
31	    export_env,
32	    fetch_worker_logs,
33	    launch_worker_detached,
34	    open_session,
35	    run_install,
36	)
37	from scripts.live_test.terminate_guard import guarded_terminate, prune_stale_live_test_pods
38	from scripts.live_test.token_resolver import resolve_token_to_user_id
39	
40	
41	FRESH_VARIANT = "fresh"
42	FRESH_WORKDIR = "/workspace/Reigh-Worker-LiveTest"
43	FRESH_REPO_URL = "https://github.com/banodoco/Reigh-Worker.git"
44	VIBECOMFY_WORKDIR = "/workspace/vibecomfy"
45	VIBECOMFY_REPO_URL = "https://github.com/peteromallet/VibeComfy.git"
46	VIBECOMFY_PYTHON = "python3.11"
47	VIBECOMFY_DEFAULT_CASE_ORDER = {
48	    "z_image_turbo": 0,
49	    "z_image_turbo_i2i": 1,
50	    "qwen_image_2512": 2,
51	    "qwen_image_edit": 3,
52	    "image_inpaint": 4,
53	    "annotated_image_edit": 5,
54	    "qwen_image_style": 6,
55	    "wan_2_2_t2i": 7,
56	    "wan_2_2_i2v": 8,
57	    "animate_character": 9,
58	    "image_upscale": 10,
59	    "video_enhance": 11,
60	    "flux_klein_edit": 12,
61	    "individual_travel_segment_wan22_vace": 13,
62	}
63	
64	log = get_logger(__name__)
65	
66	
67	_SENSITIVE_OUTPUT_PATTERNS = (
68	    re.compile(r"(?i)(['\"]?)(REIGH_ACCESS_TOKEN|SUPABASE_SERVICE_ROLE_KEY|RUNPOD_API_KEY|REIGH_LIVE_TEST_TOKEN)(['\"]?\s*[:=]\s*['\"]?)([^,'\"\s}]+)"),
69	    re.compile(r"(?i)(--reigh-access-token\s+)([^\s]+)"),
70	)
71	
72	
73	def _timestamp_label() -> str:
74	    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
75	
76	
77	def _build_matrix_cases(args) -> list:
78	    cases = build_matrix(
79	        anchor_image_a=args.anchor_image_a,
80	        anchor_image_b=args.anchor_image_b,
81	        timeout_image_sec=args.timeout_image,
82	        timeout_travel_segment_sec=args.timeout_travel_segment,
83	        timeout_travel_orchestrator_sec=args.timeout_travel_orchestrator,
84	        selected_backend=getattr(args, "backend", "wgp"),
85	        selector_namespace=getattr(args, "selector_namespace", "production"),
86	        selector_version=getattr(args, "selector_version", None),
87	        worker_contract_version=getattr(args, "worker_contract_version", 1),
88	        selected_profile=getattr(args, "worker_profile", "default"),
89	        case_names=getattr(args, "case", []),
90	        task_types=getattr(args, "task_type", []),
91	        route_keys=getattr(args, "route_key", []),
92	    )
93	    explicit_selection = bool(getattr(args, "case", []) or getattr(args, "task_type", []) or getattr(args, "route_key", []))
94	    if getattr(args, "backend", "wgp") == "vibecomfy" and not explicit_selection:
95	        filtered = [case for case in cases if case.support_state == "vibecomfy_supported"]
96	        return sorted(
97	            filtered,
98	            key=lambda case: VIBECOMFY_DEFAULT_CASE_ORDER.get(case.name, len(VIBECOMFY_DEFAULT_CASE_ORDER)),
99	        )
100	    return cases
101	
102	
103	def _build_worker_env(token: str, supabase_url: str, service_role_key: str, args=None) -> dict[str, str]:
104	    backend = getattr(args, "backend", "wgp")
105	    env = {
106	        "REIGH_ACCESS_TOKEN": token,
107	        "REIGH_BACKEND": backend,
108	        "REIGH_SELECTOR_NAMESPACE": getattr(args, "selector_namespace", "production"),
109	        "REIGH_WORKER_CONTRACT_VERSION": str(getattr(args, "worker_contract_version", 1)),
110	        "REIGH_WORKER_PROFILE": getattr(args, "worker_profile", "default"),
111	        "[REDACTED],
112	        "SUPABASE_URL": supabase_url,
113	        "WORKER_DB_CLIENT_AUTH_MODE": "service" if backend == "vibecomfy" else "worker",
114	        "REIGH_CLAIM_TELEMETRY": "1",
115	    }
116	    selector_version = getattr(args, "selector_version", None)
117	    if selector_version:
118	        env["REIGH_SELECTOR_VERSION"] = str(selector_version)
119	    if backend == "vibecomfy":
120	        attention_profile = "sage" if str(getattr(args, "worker_profile", "")).strip().lower() in {"sage", "optimized"} else "portable"
121	        env.update(
122	            {
123	                "VIBECOMFY_CWD": VIBECOMFY_WORKDIR,
124	                "VIBECOMFY_PATH": VIBECOMFY_WORKDIR,
125	                "VIBECOMFY_PYTHON": VIBECOMFY_PYTHON,
126	                "VIBECOMFY_ATTENTION_PROFILE": attention_profile,
127	                "REIGH_VIBECOMFY_ATTENTION_PROFILE": attention_profile,
128	            }
129	        )
130	    return env
131	
132	
133	def _runs_root() -> Path:
134	    return config.WORKER_ROOT / "scripts" / "live_test" / "runs"
135	
136	
137	def _redact_sensitive_text(text: str) -> str:
138	    redacted = text
139	    for pattern in _SENSITIVE_OUTPUT_PATTERNS:
140	        if pattern.pattern.startswith("(?i)(--reigh-access-token"):
141	            redacted = pattern.sub(r"\1<redacted>", redacted)
142	        else:
143	            redacted = pattern.sub(r"\1\2\3<redacted>", redacted)
144	    return redacted
145	
146	
147	@contextmanager
148	def _capture_and_redact_noisy_lifecycle_output():
149	    stdout = io.StringIO()
150	    stderr = io.StringIO()
151	    old_stdout = sys.stdout
152	    old_stderr = sys.stderr
153	    try:
154	        sys.stdout = stdout
155	        sys.stderr = stderr
156	        yield
157	    finally:
158	        sys.stdout = old_stdout
159	        sys.stderr = old_stderr
160	        captured_stdout = _redact_sensitive_text(stdout.getvalue()).strip()
161	        captured_stderr = _redact_sensitive_text(stderr.getvalue()).strip()
162	        if captured_stdout:
163	            log.info("captured runpod lifecycle stdout: %s", captured_stdout)
164	        if captured_stderr:
165	            log.warning("captured runpod lifecycle stderr: %s", captured_stderr)
166	
167	
168	def _resolve_runpod_gpu_type_id(api_key: str, requested_gpu_type: str) -> tuple[str, str]:
169	    from runpod_lifecycle.api import find_gpu_type
170	
171	    gpu = find_gpu_type(requested_gpu_type, api_key)
172	    if not gpu:
173	        raise RuntimeError(f"RunPod GPU type not found: {requested_gpu_type!r}")
174	
175	    gpu_type_id = str(gpu.get("id") or "").strip()
176	    gpu_display_name = str(gpu.get("displayName") or requested_gpu_type).strip()
177	    if not gpu_type_id:
178	        raise RuntimeError(f"RunPod GPU type {requested_gpu_type!r} resolved without an id")
179	
180	    log.info(
181	        "resolved RunPod GPU type",
182	        requested_gpu_type=requested_gpu_type,
183	        gpu_type_id=gpu_type_id,
184	        gpu_display_name=gpu_display_name,
185	    )
186	    return gpu_type_id, gpu_display_name
187	
188	
189	@contextmanager
190	def _phase(name: str, **fields):
191	    started_at = time.monotonic()
192	    log.info("live test phase started", phase=name, **fields)
193	    try:
194	        yield
195	    except Exception as exc:
196	        log.error(
197	            "live test phase failed",
198	            phase=name,
199	            elapsed_sec=round(time.monotonic() - started_at, 1),
200	            error_type=type(exc).__name__,
```

> AGENT

Now let me search for the actual bootstrap functions in ssh_bootstrap.py:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def clone_and_install_vibecomfy\\|def run_install\\|def clone_repo_into\\|def launch_worker\" /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ssh_bootstrap.py | head -20"
}
```

> TOOL

tool_result Bash
```
156:def clone_repo_into(ssh, workdir: str, repo_url: str, branch: str) -> None:
166:def run_install(ssh, workdir: str) -> None:
199:def clone_and_install_vibecomfy(
305:def launch_worker_detached(ssh, command_line: str) -> None:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ssh_bootstrap.py",
  "offset": 156,
  "limit": 250
}
```

> TOOL

tool_result Read
```
156	def clone_repo_into(ssh, workdir: str, repo_url: str, branch: str) -> None:
157	    parent = workdir.rsplit("/", 1)[0] or "/"
158	    command = (
159	        f"mkdir -p {_quote(parent)} && "
160	        f"rm -rf {_quote(workdir)} && "
161	        f"git clone --branch {_quote(branch)} --single-branch --recurse-submodules {_quote(repo_url)} {_quote(workdir)}"
162	    )
163	    _execute(ssh, command, timeout=1800)
164	
165	
166	def run_install(ssh, workdir: str) -> None:
167	    package_list = " ".join(APT_INSTALL_PACKAGES)
168	    command = (
169	        "bash -lc "
170	        + _quote(
171	            "set -euo pipefail\n"
172	            "apt-get update\n"
173	            f"apt-get install -y {package_list}\n"
174	            "if ! command -v uv >/dev/null 2>&1; then\n"
175	            "  curl -LsSf https://astral.sh/uv/install.sh | sh\n"
176	            "  export PATH=\"$HOME/.local/bin:$PATH\"\n"
177	            "fi\n"
178	            f"cd {shlex.quote(workdir)}\n"
179	            "export PATH=\"$HOME/.local/bin:$PATH\"\n"
180	            "export UV_PROJECT_ENVIRONMENT=/opt/reigh-worker-live-test-venv\n"
181	            # Network volume is MooseFS which doesn't support hardlinks; force copy.
182	            "export UV_LINK_MODE=copy\n"
183	            # --locked dropped: main has newer pyproject deps (runpod-lifecycle)
184	            # that the committed uv.lock doesn't yet include; let uv update lock in-place.
185	            "for attempt in 1 2 3; do\n"
186	            "  if uv sync --extra cuda124; then\n"
187	            "    break\n"
188	            "  fi\n"
189	            "  echo \"uv sync attempt $attempt failed; cleaning partial venv and retrying\"\n"
190	            "  rm -rf .venv \"$UV_PROJECT_ENVIRONMENT\"\n"
191	            "  sleep 5\n"
192	            "  if [ $attempt -eq 3 ]; then exit 1; fi\n"
193	            "done\n"
194	        )
195	    )
196	    _execute(ssh, command, timeout=3600)
197	
198	
199	def clone_and_install_vibecomfy(
200	    ssh,
201	    *,
202	    repo_url: str,
203	    branch: str,
204	    workdir: str = "/workspace/vibecomfy",
205	    python_path: str,
206	    attention_profile: str | None = None,
207	) -> None:
208	    parent = workdir.rsplit("/", 1)[0] or "/"
209	    resolved_attention_profile = _resolve_attention_profile(attention_profile)
210	    sageattention_install = _sageattention_install_block(python_path) if resolved_attention_profile == "sage" else ""
211	    command = (
212	        "bash -lc "
213	        + _quote(
214	            "set -euo pipefail\n"
215	            f"export VIBECOMFY_ATTENTION_PROFILE={_quote(resolved_attention_profile)}\n"
216	            f"mkdir -p {_quote(parent)}\n"
217	            f"rm -rf {_quote(workdir)}\n"
218	            f"git clone --branch {_quote(branch)} --single-branch {_quote(repo_url)} {_quote(workdir)}\n"
219	            f"git -C {_quote(workdir)} fetch origin {_quote(branch)}\n"
220	            f"git -C {_quote(workdir)} checkout {_quote(branch)}\n"
221	            f"git -C {_quote(workdir)} reset --hard FETCH_HEAD\n"
222	            f"git -C {_quote(workdir)} clean -ffd\n"
223	            f"echo \"VibeComfy checkout: $(git -C {_quote(workdir)} rev-parse --short HEAD)\"\n"
224	            f"{_quote(python_path)} -m pip install -e {_quote(workdir)}\n"
225	            f"{_quote(python_path)} -m pip install "
226	            "'comfyui@git+https://github.com/peteromallet/ComfyUI.git@fix/latentupscale-model-mmap-residency' "
227	            "'comfy-script[default]'\n"
228	            f"{sageattention_install}"
229	            f"cd {_quote(workdir)}\n"
230	            "test -f custom_nodes.lock\n"
231	            f"{_quote(python_path)} -m vibecomfy.cli nodes restore --lockfile custom_nodes.lock\n"
232	            f"test -f {_quote(workdir)}/template_index.json\n"
233	            f"test -f {_quote(workdir)}/workflow_corpus/manifests/coverage.json\n"
234	        )
235	    )
236	    _execute(ssh, command, timeout=3600)
237	
238	
239	def export_env(env: dict[str, str]) -> str:
240	    exports = dict(env)
241	    required = {
242	        "REIGH_ACCESS_TOKEN",
243	        "SUPABASE_SERVICE_ROLE_KEY",
244	        "SUPABASE_URL",
245	        "WORKER_DB_CLIENT_AUTH_MODE",
246	    }
247	    missing = sorted(name for name in required if not exports.get(name))
248	    if missing:
249	        raise ValueError(f"Missing required environment values for export_env: {', '.join(missing)}")
250	    if exports["WORKER_DB_CLIENT_AUTH_MODE"] not in {"worker", "service"}:
251	        raise ValueError("WORKER_DB_CLIENT_AUTH_MODE must be 'worker' or 'service' for live tests")
252	    return " && ".join(f"export {key}={_quote(value)}" for key, value in sorted(exports.items()))
253	
254	
255	def capture_current_worker_cmdline(ssh) -> WorkerProcessInfo | None:
256	    stdout, _ = _execute(ssh, PROCESS_SCAN_COMMAND, check=False)
257	    rows: list[tuple[int, list[str]]] = []
258	    for raw_line in stdout.splitlines():
259	        line = raw_line.strip()
260	        if not line:
261	            continue
262	        parts = line.split(None, 1)
263	        if len(parts) != 2:
264	            continue
265	        pid_str, args = parts
266	        try:
267	            pid = int(pid_str)
268	        except ValueError:
269	            continue
270	        rows.append((pid, shlex.split(args)))
271	
272	    supervisor_rows = [row for row in rows if any("run_worker.py" in arg for arg in row[1])]
273	    if supervisor_rows:
274	        pid, cmdline = supervisor_rows[0]
275	        return WorkerProcessInfo(family="supervisor", cmdline=cmdline, pid=pid)
276	
277	    direct_rows = [
278	        row
279	        for row in rows
280	        if any(arg == "worker.py" or arg.endswith("/worker.py") or "source.runtime.worker" in arg for arg in row[1])
281	    ]
282	    if direct_rows:
283	        pid, cmdline = direct_rows[0]
284	        return WorkerProcessInfo(family="direct", cmdline=cmdline, pid=pid)
285	
286	    return None
287	
288	
289	def kill_supervisor_and_worker(ssh) -> None:
290	    _execute(ssh, KILL_COMMAND, check=False, timeout=30)
291	    deadline = time.monotonic() + 20
292	    while time.monotonic() < deadline:
293	        stdout, _ = _execute(
294	            ssh,
295	            PROCESS_SCAN_COMMAND,
296	            check=False,
297	            timeout=30,
298	        )
299	        if not stdout.strip():
300	            return
301	        time.sleep(1)
302	    raise RuntimeError(f"Worker processes are still running after kill attempt:\n{stdout}")
303	
304	
305	def launch_worker_detached(ssh, command_line: str) -> None:
306	    # Wrap so bash exits immediately after backgrounding; avoid paramiko hanging
307	    # on stdout EOF when a nohup child inherits the ssh channel streams.
308	    wrapped = f"bash -c {shlex.quote(command_line + ' ; exit 0')} </dev/null >/dev/null 2>&1"
309	    client = ssh.client
310	    transport = client.get_transport()
311	    channel = transport.open_session()
312	    try:
313	        channel.set_combine_stderr(True)
314	        channel.exec_command(wrapped)
315	        deadline = time.monotonic() + 30
316	        while not channel.exit_status_ready() and time.monotonic() < deadline:
317	            time.sleep(0.2)
318	        if not channel.exit_status_ready():
319	            return  # detached; don't wait further
320	        exit_code = channel.recv_exit_status()
321	        if exit_code != 0:
322	            raise RuntimeError(f"Detached launch command exited with {exit_code}")
323	    finally:
324	        channel.close()
325	
326	
327	def fetch_worker_logs(ssh, workdir: str, lines: int = 300) -> str:
328	    startup_script = _quote(
329	        f"cd {workdir} && "
330	        f'{{ echo "=== startup.log ==="; tail -n {int(lines)} logs/startup.log 2>/dev/null || true; }}'
331	    )
332	    startup_stdout, _ = _execute(
333	        ssh,
334	        f"bash -lc {startup_script}",
335	        check=False,
336	        timeout=60,
337	    )
338	    worker_script = _quote(
339	        f"cd {workdir} && "
340	        f'{{ echo "=== worker.log ==="; tail -n {int(lines)} logs/worker.log 2>/dev/null || true; }}'
341	    )
342	    worker_stdout, _ = _execute(
343	        ssh,
344	        f"bash -lc {worker_script}",
345	        check=False,
346	        timeout=60,
347	    )
348	    return "\n".join(part.rstrip() for part in (startup_stdout, worker_stdout) if part.strip())
349	
350	
351	__all__ = [
352	    "APT_INSTALL_PACKAGES",
353	    "KILL_COMMAND",
354	    "PROCESS_SCAN_COMMAND",
355	    "WorkerProcessInfo",
356	    "capture_current_worker_cmdline",
357	    "clone_and_install_vibecomfy",
358	    "clone_repo_into",
359	    "export_env",
360	    "fetch_worker_logs",
361	    "kill_supervisor_and_worker",
362	    "launch_worker_detached",
363	    "open_session",
364	    "run_install",
365	]
366
```

> AGENT

Now let me check runpod-lifecycle and look for vibecomfy's setup:

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/**/*.py"
}
```

> TOOL

tool_result Glob
```
runpod-lifecycle/tests/__init__.py
runpod-lifecycle/src/runpod_lifecycle/errors.py
runpod-lifecycle/src/runpod_lifecycle/events.py
runpod-lifecycle/tests/conftest.py
runpod-lifecycle/src/runpod_lifecycle/storage.py
runpod-lifecycle/tests/test_storage.py
runpod-lifecycle/tests/test_terminate.py
runpod-lifecycle/src/runpod_lifecycle/discovery.py
runpod-lifecycle/tests/test_discovery.py
runpod-lifecycle/smoke_live.py
runpod-lifecycle/tests/test_ssh_details.py
runpod-lifecycle/src/runpod_lifecycle/ssh.py
runpod-lifecycle/src/runpod_lifecycle/guard.py
runpod-lifecycle/src/runpod_lifecycle/shipping.py
runpod-lifecycle/src/runpod_lifecycle/pod.py
runpod-lifecycle/tests/test_shipping.py
runpod-lifecycle/tests/test_guard.py
runpod-lifecycle/tests/test_pod.py
runpod-lifecycle/tests/test_live_pod.py
runpod-lifecycle/src/runpod_lifecycle/api.py
runpod-lifecycle/tests/test_api.py
runpod-lifecycle/src/runpod_lifecycle/probe.py
runpod-lifecycle/src/runpod_lifecycle/lifecycle.py
runpod-lifecycle/src/runpod_lifecycle/__init__.py
runpod-lifecycle/tests/test_launch.py
runpod-lifecycle/src/runpod_lifecycle/cli.py
runpod-lifecycle/src/runpod_lifecycle/config.py
runpod-lifecycle/tests/test_config.py
runpod-lifecycle/tests/test_probe.py
runpod-lifecycle/tests/test_cli.py
runpod-lifecycle/src/runpod_lifecycle/runner.py
runpod-lifecycle/tests/test_runner.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/__init__.py"
}
```

> TOOL

tool_result Read
```
1	"""Async RunPod lifecycle primitives for launching pods, waiting for readiness, executing SSH commands, and terminating machines through a small typed public API. Also provides account-wide discovery (list_pods, find_orphans) and a `runpod-lifecycle` CLI."""
2	
3	from .config import RunPodConfig
4	from .discovery import (
5	    PodSummary,
6	    cost_summary,
7	    find_orphans,
8	    find_pods,
9	    get_pod,
10	    list_pods,
11	    terminate,
12	)
13	from .errors import LaunchFailure, NotReadyTimeout, RunPodError, SSHError, TerminateError
14	from .events import EventHooks, PodEvent, PodState
15	from .guard import PodGuard, install_signal_handlers
16	from .api import create_network_volume
17	from .lifecycle import find_gpu_type, get_network_volumes, launch
18	from .pod import Pod
19	from .probe import probe
20	from .runner import ShipAndRunResult, ship_and_run, ship_and_run_detached
21	from .shipping import (
22	    UploadHeartbeat,
23	    _build_upload_tarball,
24	    _preflight_upload_disk,
25	    _upload_remote_script,
26	    download_artifact_archive,
27	    should_skip,
28	    upload_dir,
29	)
30	
31	__all__ = [
32	    "RunPodConfig",
33	    "Pod",
34	    "PodState",
35	    "PodEvent",
36	    "EventHooks",
37	    "PodGuard",
38	    "UploadHeartbeat",
39	    "ShipAndRunResult",
40	    "ship_and_run",
41	    "ship_and_run_detached",
42	    "launch",
43	    "probe",
44	    "find_gpu_type",
45	    "get_network_volumes",
46	    "create_network_volume",
47	    "list_pods",
48	    "find_pods",
49	    "find_orphans",
50	    "get_pod",
51	    "terminate",
52	    "cost_summary",
53	    "PodSummary",
54	    "install_signal_handlers",
55	    "should_skip",
56	    "upload_dir",
57	    "_build_upload_tarball",
58	    "_preflight_upload_disk",
59	    "_upload_remote_script",
60	    "download_artifact_archive",
61	    "RunPodError",
62	    "LaunchFailure",
63	    "NotReadyTimeout",
64	    "SSHError",
65	    "TerminateError",
66	]
67
```

> AGENT

Now let me check vibecomfy's structure and ready_templates:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/vibecomfy -name \"ready_templates\" -o -name \"*bootstrap*\" -o -name \"pyproject.toml\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/ready_templates
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/pyproject.toml
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/vibecomfy_extras/ready_templates
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/vibecomfy/search/bootstrap.py
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/vibecomfy/search/__pycache__/bootstrap.cpython-312.pyc
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/vibecomfy/search/__pycache__/bootstrap.cpython-311.pyc
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/vendor/ComfyUI/pyproject.toml
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/vibecomfy/ready_templates/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 40
drwxr-xr-x  10 user_c042661f  staff    320 May  7 04:10 .
drwxr-xr-x  39 user_c042661f  staff   1248 May 11 14:30 ..
-rw-r--r--@  1 user_c042661f  staff  10244 May  9 03:41 .DS_Store
-rw-r--r--   1 user_c042661f  staff   2405 May  9 01:04 README.md
-rw-r--r--   1 user_c042661f  staff   3481 Apr 28 04:33 VALIDATION.md
drwxr-xr-x@  7 user_c042661f  staff    224 May  5 17:13 audio
drwxr-xr-x   8 user_c042661f  staff    256 May  5 17:13 edit
drwxr-xr-x  10 user_c042661f  staff    320 May  8 10:25 image
drwxr-xr-x   4 user_c042661f  staff    128 May  5 17:26 smoke
drwxr-xr-x  47 user_c042661f  staff   1504 May 11 14:30 video
```

> AGENT

Now let me check for docs related to live-test or prebuilt environments:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/docs -type f -name \"*live*\" -o -name \"*migration*\" -o -name \"*vibecomfy*\" 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/docs/megaplan-vibecomfy-chain
/Users/user_c042661f/Documents/reigh-workspace/docs/megaplan-vibecomfy-chain/sprint-11a-vibecomfy-endpoint-inventory.md
/Users/user_c042661f/Documents/reigh-workspace/docs/megaplan-vibecomfy-chain/ideas/sprint-01-vibecomfy-memory-profile-mvp.md
/Users/user_c042661f/Documents/reigh-workspace/docs/megaplan-vibecomfy-chain/sprint-11a-live-proof-attempts.md
/Users/user_c042661f/Documents/reigh-workspace/docs/structure_detail/deployment_and_migration_guide.md
/Users/user_c042661f/Documents/reigh-workspace/docs/vibecomfy-post-chain-validation-20260507.md
/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy.md
/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy-live-validation.md
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy-live-validation.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# Live Validation Plan: reigh-worker Dual Backend VibeComfy Migration
2	
3	> **Draft status:** Sister plan for `migration-vibecomfy.md`, authored 2026-05-05.
4	
5	This document defines how to test the addition of VibeComfy as a peer execution backend alongside Wan2GP, live and end-to-end on real RunPod GPUs. It complements `migration-vibecomfy.md`: that document owns the migration design; this document owns the validation harness, acceptance gates, and evidence package required before canary and dual-executor steady state.
6	
7	## Threshold and Route Version 0B (2026-05-05)
8	
9	The executable threshold and route source of truth for Sprint 0B and later dual-run, dry-run, and canary consumers is `reigh-worker/scripts/dual_run_compare/migration-thresholds.yaml` (`version: 0B-2026-05-05`, `schema_version: 1`). The YAML exposes row-granular `metric_keys`, metric `defaults`, and `routes`. Later scripts must load this YAML through `python -m scripts.dual_run_compare.check_thresholds --strict` and the `Thresholds` API rather than copying values from this document or `migration-vibecomfy.md`.
10	
11	Metric rows in version `0B-2026-05-05`:
12	
13	- `image_phash_normalized_hamming`
14	- `image_ssim`
15	- `image_pixel_dimensions`
16	- `image_format_container`
17	- `video_frame_count`
18	- `video_phash_mean`
19	- `video_phash_p95`
20	- `video_duration_ms`
21	- `video_fps`
22	- `video_audio_duration_ms`
23	- `latency_p95_wall_clock_ratio`
24	- `vram_peak_ratio`
25	- `error_oom_count`
26	- `canary_output_divergence_rate`
27	
28	Route [REDACTED] is defined in `reigh-worker/scripts/dual_run_compare/route_keys.py`. Cohort A/B direct product routes use direct route keys; Cohort B edit variants add dimensions when variant dimensions are present; Cohort E route keys are dimensional and include task type, model family, guidance kind, continuity case, and profile.
29	
30	Golden corpus and fixture layout:
31	
32	- `reigh-worker/scripts/dual_run_compare/golden/<route_key>/manifest.json`
33	- `reigh-worker/scripts/dual_run_compare/fixtures/golden_seed_payloads/`
34	- `reigh-worker/scripts/dual_run_compare/fixtures/non_rayworker/`
35	
36	WGP repeatability evidence for this version is committed at:
37	
38	- `reigh-worker/scripts/dual_run_compare/reports/wgp-self-repeat-0b-2026-05-05-deferral.json`
39	- `reigh-worker/scripts/dual_run_compare/reports/wgp-self-repeat-0b-2026-05-05-deferral.md`
40	
41	Status summary: all 14 route keys in the YAML and report are currently marked `deferred_pending_sprint_0c_disk`. The report records the attempted WGP-vs-WGP command shape for every required route, but it contains no paired WGP metric observations. This is not a RunPod-access failure: the agent separately verified live RunPod lifecycle on 2026-05-05 with pod `f9s5vqk15gux9d` through launch, SSH readiness, GPU visibility, storage health, pod listing, termination, and post-terminate absence. After user correction, WGP is treated as the trusted control; paired WGP self-repeatability should run only when a later sprint needs fresh measured drift to promote route statuses.
42	
43	## Execution Primitive
44	
45	The migration execution unit is a VibeComfy Python ready template under `vibecomfy/ready_templates/**/*.py`.
46	
47	Raw Comfy JSON can remain as import/source material under `workflow_corpus/`, and tiny JSON fixtures may remain for parser or runtime unit tests, but live migration validation must not treat JSON fixture execution as the standard path. A RunPod validation row should execute a Python ready template by ready-template id or path, for example:
48	
49	```bash
50	python3 -m vibecomfy.cli run smoke/empty_image_red --ready --runtime embedded --backend graphbuilder
51	python3 -m vibecomfy.cli run image/qwen_image_2512 --ready --runtime embedded --backend graphbuilder
52	```
53	
54	Each production row must report the ready-template id, Python source path, `READY_REQUIREMENTS`, staged model URLs/paths, VibeComfy run id, Comfy prompt id, outputs, and artifact paths. If a validation command runs a raw JSON workflow directly, it is only a low-level runtime smoke and cannot satisfy a migration gate.
55	
56	## Goals
57	
58	- Prove each production-used task type can run through the VibeComfy backend on real RunPod hardware.
59	- Reuse VibeComfy's existing cloud/RunPod mode for template and workflow execution validation instead of duplicating pod lifecycle code in `reigh-worker`.
60	- Preserve `reigh-worker` live-test coverage for Supabase queue behavior, task claiming, completion, generation linking, output shape, logs, and rollback.
61	- Add semantic media grading through Astrid `builtin.understand` so live tests check whether outputs are coherent and intent-preserving, not only whether files exist.
62	- Produce a durable evidence bundle per run: task payload, backend, template id, RunPod pod id, worker id, output paths, timings, failure class, media descriptions, rubric scores, and final gate decision.
63	
64	## Non-Goals
65	
66	- No replacement of VibeComfy's existing RunPod/cloud scripts.
67	- No new production queue schema.
68	- No requirement that automated visual grading be the only approval signal. It is a promotion gate and triage aid; final canary still requires human review of sampled outputs.
69	- No migration coverage for task types classified as UNUSED in `migration-vibecomfy.md` §0A.
70	- No Wan2GP retirement validation. WGP remains the control backend and a supported rollback executor.
71	
72	## Existing Surfaces To Reuse
73	
74	### VibeComfy Cloud / RunPod Mode
75	
76	VibeComfy already has the primary cloud validation machinery:
77	
78	- `vibecomfy/scripts/runpod_runner.py`
79	  - `PodGuard` launches and terminates RunPod pods with a max-runtime watchdog.
80	  - `run_pod()` uploads the local VibeComfy checkout, runs a remote script, prints pod id and SSH details, and terminates in `finally`.
81	  - `run_pod_detached()` runs long matrix jobs, polls `results.tsv` / media / logs, downloads `out/corpus_matrix`, `output`, and `out/runs` artifacts, then terminates in `finally`.
82	- `vibecomfy/scripts/runpod_validate.py`
83	  - Cheap live smoke: install VibeComfy, install HiddenSwitch ComfyUI and ComfyScript, run tests, run runtime smoke, then execute the minimal Python ready template `ready_templates/smoke/empty_image_red.py`.
84	- `vibecomfy/scripts/runpod_model_matrix.py`
85	  - Proper model-backed matrix: baseline `comfyui run-workflow`, convert to VibeComfy scratchpad, run via embedded Comfy, record output counts and timings.
86	- `vibecomfy/scripts/runpod_corpus_matrix.py`
87	  - Corpus-scale remote matrix with detached polling and artifact download.
88	- `vibecomfy/vibecomfy/commands/runpod.py`
89	  - CLI forwarding for `vibecomfy runpod list/status/terminate/gpu-types/corpus-matrix`.
90	- `vibecomfy/tests/smoke/test_*runpod*.py`
91	  - Opt-in pytest markers `runpod` and `runpod_full` for real GPU smoke and matrix coverage.
92	
93	This should be the foundation for template execution, model staging, custom-node installation, artifact capture, and pod lifecycle safety.
94	
95	### reigh-worker Live Harness
96	
97	`reigh-worker` already has a queue-realistic harness:
98	
99	- `reigh-worker/scripts/live_test/main.py`
100	  - CLI entrypoint with `fresh` and `update` variants, WGP profile argument, task timeouts, and anchor image overrides.
```

> AGENT

Now let me check for CLAUDE.md or agent discovery in .claude:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace -maxdepth 2 -name \"CLAUDE.md\" -o -name \".claude\" -type d"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker-orchestrator/.claude
/Users/user_c042661f/Documents/reigh-workspace/.claude
/Users/user_c042661f/Documents/reigh-workspace/reigh-app-cloud-chain/CLAUDE.md
/Users/user_c042661f/Documents/reigh-workspace/reigh-app/.claude
/Users/user_c042661f/Documents/reigh-workspace/reigh-app/CLAUDE.md
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/.claude
/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/CLAUDE.md
/Users/user_c042661f/Documents/reigh-workspace/Astrid/.claude
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.claude
/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/.claude
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.claude/CLAUDE.md"
}
```

> TOOL

tool_result Read
```
File does not exist. Note: your current working directory is /Users/user_c042661f/Documents/reigh-workspace.
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.claude/ 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
total 8
drwxr-xr-x   4 user_c042661f  staff   128 Apr 23 22:09 .
drwxr-xr-x  48 user_c042661f  staff  1536 May 11 14:31 ..
-rw-r--r--   1 user_c042661f  staff  1243 Mar 16 14:23 settings.local.json
drwxr-xr-x   3 user_c042661f  staff    96 Feb 11 19:40 skills
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/.claude -type f -name \"*.md\" 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/.claude/skills/megaplan.md
```

> AGENT

Let me check runpod-lifecycle for more specific API details:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/lifecycle.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""Launch orchestration for RunPod pods with RAM-tier and storage fallback."""
2	
3	from __future__ import annotations
4	
5	import asyncio
6	import logging
7	import os
8	import time
9	from typing import Any
10	
11	from .api import create_pod, find_gpu_type, get_network_volumes
12	from .config import RunPodConfig
13	from .errors import LaunchFailure
14	from .events import EventHooks, PodState, _emit_error, _emit_state
15	from .pod import Pod
16	from .storage import check_and_expand_storage, get_storage_volume_id
17	
18	logger = logging.getLogger("runpod_lifecycle.lifecycle")
19	
20	
21	def _resolve_public_key_string(config: RunPodConfig) -> str | None:
22	    if config.ssh_public_key:
23	        return config.ssh_public_key
24	
25	    if config.ssh_public_key_path:
26	        expanded_path = os.path.expanduser(config.ssh_public_key_path)
27	        try:
28	            return open(expanded_path, "r", encoding="utf-8").read().strip()
29	        except OSError as exc:
30	            logger.warning("Could not read SSH public key from %s: %s", expanded_path, exc)
31	
32	    logger.warning("No SSH public key configured; pod access may require password auth")
33	    return None
34	
35	
36	def _build_ram_tiers(config: RunPodConfig) -> list[int]:
37	    if not config.ram_tiers_enabled:
38	        return [config.min_memory_gb]
39	
40	    ram_tiers = [tier for tier in config.ram_tiers if tier >= config.min_memory_gb]
41	    return ram_tiers or [config.min_memory_gb]
42	
43	
44	async def _resolve_storage_targets(config: RunPodConfig) -> list[tuple[str | None, str | None]]:
45	    raw_targets: list[str] = []
46	    for storage_name in [config.storage_name, *config.storage_volumes]:
47	        if storage_name and storage_name not in raw_targets:
48	            raw_targets.append(storage_name)
49	
50	    if not raw_targets:
51	        return [(None, None)]
52	
53	    resolved_targets: list[tuple[str | None, str | None]] = []
54	    for storage_name in raw_targets:
55	        volume_id = await asyncio.to_thread(get_storage_volume_id, config.api_key, storage_name)
56	        if volume_id:
57	            resolved_targets.append((storage_name, volume_id))
58	        else:
59	            logger.warning("Storage '%s' not found, skipping", storage_name)
60	
61	    return resolved_targets
62	
63	
64	class _GpuCandidateFailure(Exception):
65	    """Internal: signals one candidate GPU exhausted its RAM x storage matrix."""
66	
67	    def __init__(
68	        self,
69	        gpu_type: str,
70	        reason: str,
71	        attempted_pairs: list[dict[str, Any]],
72	        last_error: Exception | None,
73	    ) -> None:
74	        super().__init__(reason)
75	        self.gpu_type = gpu_type
76	        self.reason = reason
77	        self.attempted_pairs = attempted_pairs
78	        self.last_error = last_error
79	
80	
81	async def _try_launch_one_gpu(
82	    config: RunPodConfig,
83	    gpu_type: str,
84	    *,
85	    pod_name: str,
86	    hooks: EventHooks,
87	    public_key_string: str | None,
88	    ram_tiers: list[int],
89	    storage_targets: list[tuple[str | None, str | None]],
90	    expanded_storage_ids: set[str],
91	) -> Pod:
92	    """Resolve a single GPU type and walk the RAM-tier x storage matrix.
93	
94	    Returns a launched Pod on success, otherwise raises ``_GpuCandidateFailure``
95	    summarising the per-pair errors for this candidate.
96	    """
97	    gpu_info = await asyncio.to_thread(find_gpu_type, gpu_type, config.api_key)
98	    if not gpu_info:
99	        raise _GpuCandidateFailure(
100	            gpu_type=gpu_type,
```

> AGENT

Let me search for the launch function signature:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^async def launch\\|^def launch\" /Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/lifecycle.py | head -5"
}
```

> TOOL

tool_result Bash
```
205:async def launch(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/lifecycle.py",
  "offset": 205,
  "limit": 80
}
```

> TOOL

tool_result Read
```
205	async def launch(
206	    config: RunPodConfig,
207	    *,
208	    name: str | None = None,
209	    hooks: EventHooks | None = None,
210	) -> Pod:
211	    hooks = hooks or EventHooks()
212	    pod_name = name or f"{config.name_prefix}-{int(time.time())}"
213	
214	    candidates = config.gpu_type_candidates
215	    if not candidates:
216	        error = LaunchFailure("No GPU types configured for launch")
217	        await _emit_error(hooks, error, {"name": pod_name})
218	        raise error
219	
220	    await _emit_state(hooks, None, PodState.PROVISIONING, {"name": pod_name})
221	
222	    public_key_string = _resolve_public_key_string(config)
223	    ram_tiers = _build_ram_tiers(config)
224	    storage_targets = await _resolve_storage_targets(config)
225	
226	    input_storages = [value for value in [config.storage_name, *config.storage_volumes] if value]
227	    if input_storages and not storage_targets:
228	        error = LaunchFailure(
229	            f"Configured storage volumes could not be resolved: {', '.join(input_storages)}"
230	        )
231	        await _emit_error(
232	            hooks,
233	            error,
234	            {"storages": input_storages, "name": pod_name},
235	        )
236	        raise error
237	
238	    expanded_storage_ids: set[str] = set()
239	    candidate_failures: list[_GpuCandidateFailure] = []
240	
241	    for gpu_type in candidates:
242	        await _emit_state(
243	            hooks,
244	            None,
245	            PodState.PROVISIONING,
246	            {"name": pod_name, "gpu_type": gpu_type},
247	        )
248	        try:
249	            return await _try_launch_one_gpu(
250	                config,
251	                gpu_type,
252	                pod_name=pod_name,
253	                hooks=hooks,
254	                public_key_string=public_key_string,
255	                ram_tiers=ram_tiers,
256	                storage_targets=storage_targets,
257	                expanded_storage_ids=expanded_storage_ids,
258	            )
259	        except _GpuCandidateFailure as failure:
260	            candidate_failures.append(failure)
261	            continue
262	
263	    reasons = "; ".join(failure.reason for failure in candidate_failures) or "no attempts made"
264	    aggregated_pairs = [pair for failure in candidate_failures for pair in failure.attempted_pairs]
265	    last_underlying = next(
266	        (failure.last_error for failure in reversed(candidate_failures) if failure.last_error),
267	        None,
268	    )
269	
270	    error = LaunchFailure(
271	        f"Failed to launch pod across GPU candidates {list(candidates)}: {reasons}"
272	    )
273	    await _emit_error(
274	        hooks,
275	        error,
276	        {
277	            "name": pod_name,
278	            "gpu_candidates": list(candidates),
279	            "ram_tiers": ram_tiers,
280	            "attempted_pairs": aggregated_pairs,
281	            "candidate_reasons": [failure.reason for failure in candidate_failures],
282	            "last_error": str(last_underlying) if last_underlying else None,
283	        },
284	    )
```

> AGENT

Now let me look at the variant_fresh.py to understand the flow of pod launching and environment configuration:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"disk_size\\|image\\|template\\|snapshot\" /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/variant_fresh.py | head -20"
}
```

> TOOL

tool_result Bash
```
48:    "z_image_turbo": 0,
49:    "z_image_turbo_i2i": 1,
50:    "qwen_image_2512": 2,
51:    "qwen_image_edit": 3,
52:    "image_inpaint": 4,
53:    "annotated_image_edit": 5,
54:    "qwen_image_style": 6,
58:    "image_upscale": 10,
79:        anchor_image_a=args.anchor_image_a,
80:        anchor_image_b=args.anchor_image_b,
81:        timeout_image_sec=args.timeout_image,
236:                "selected_template_id": case.selected_template_id,
412:            image=config.RUNPOD_WORKER_IMAGE,
418:                    image_name=config.RUNPOD_WORKER_IMAGE,
426:                    template_id=config.RUNPOD_TEMPLATE_ID,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/config.py"
}
```

> TOOL

tool_result Read
```
1	"""Configuration and static references for the live-test harness."""
2	
3	from __future__ import annotations
4	
5	import os
6	from dataclasses import dataclass
7	from pathlib import Path
8	from typing import Any
9	
10	import scripts.live_test as live_test_pkg
11	from scripts.live_test import ORCHESTRATOR_ROOT, WORKER_ROOT, ensure_orchestrator_imports
12	
13	ensure_orchestrator_imports()
14	
15	
16	def _load_env_file(path: Path) -> None:
17	    if not path.exists():
18	        return
19	    for raw_line in path.read_text(encoding="utf-8").splitlines():
20	        line = raw_line.strip()
21	        if not line or line.startswith("#") or "=" not in line:
22	            continue
23	        key, value = line.split("=", 1)
24	        key = key.strip()
25	        value = value.strip()
26	        if value and value[0] == value[-1] and value[0] in {'"', "'"}:
27	            value = value[1:-1]
28	        os.environ.setdefault(key, value)
29	
30	
31	_load_env_file(WORKER_ROOT / ".env")
32	
33	
34	def get_env(name: str, default: str | None = None) -> str | None:
35	    value = os.environ.get(name)
36	    if value is None:
37	        return default
38	    value = value.strip()
39	    return value or default
40	
41	
42	def require_env(name: str) -> str:
43	    value = get_env(name)
44	    if value is None:
45	        raise ValueError(f"Missing required environment variable: {name}")
46	    return value
47	
48	
49	@dataclass(frozen=True)
50	class RunpodDefaults:
51	    gpu_type: str
52	    worker_image: str
53	    template_id: str
54	    volume_mount_path: str
55	    disk_size_gb: int
56	    container_disk_gb: int
57	    min_vcpu_count: int
58	    min_memory_gb: int
59	    storage_volumes: tuple[str, ...]
60	    ram_tiers: tuple[int, ...]
61	
62	
63	@dataclass(frozen=True)
64	class LiveTestEnv:
65	    reigh_live_test_token: str | None
66	    runpod_api_key: str | None
67	    supabase_url: str | None
68	    supabase_service_role_key: str | None
69	
70	
71	def _load_runpod_defaults() -> RunpodDefaults:
72	    try:
73	        from runpod_lifecycle import RunPodConfig
74	
75	        cfg = RunPodConfig.from_env()
76	        return RunpodDefaults(
77	            gpu_type=cfg.gpu_type,
78	            worker_image=cfg.worker_image,
79	            template_id=cfg.template_id,
80	            volume_mount_path=cfg.volume_mount_path,
81	            disk_size_gb=cfg.disk_size_gb,
82	            container_disk_gb=cfg.container_disk_gb,
83	            min_vcpu_count=cfg.min_vcpu_count,
84	            min_memory_gb=cfg.min_memory_gb,
85	            storage_volumes=tuple(cfg.storage_volumes) or (cfg.storage_name,) if cfg.storage_name else tuple(cfg.storage_volumes),
86	            ram_tiers=tuple(cfg.ram_tiers),
87	        )
88	    except Exception:
89	        return RunpodDefaults(
90	            gpu_type="NVIDIA GeForce RTX 4090",
91	            worker_image="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04",
92	            template_id="runpod-torch-v240",
93	            volume_mount_path="/workspace",
94	            disk_size_gb=50,
95	            container_disk_gb=50,
96	            min_vcpu_count=8,
97	            min_memory_gb=32,
98	            storage_volumes=("Peter", "EU-NO-1", "EU-CZ-1", "EUR-IS-1"),
99	            ram_tiers=(72, 60, 48, 32, 16),
100	        )
101	
102	
103	ENV = LiveTestEnv(
104	    reigh_live_test_token=get_env("REIGH_LIVE_TEST_TOKEN"),
105	    runpod_api_key=get_env("RUNPOD_API_KEY"),
106	    supabase_url=get_env("SUPABASE_URL"),
107	    supabase_service_role_key=get_env("SUPABASE_SERVICE_ROLE_KEY"),
108	)
109	
110	RUNPOD = _load_runpod_defaults()
111	RUNPOD_GPU_TYPE = RUNPOD.gpu_type
112	RUNPOD_WORKER_IMAGE = RUNPOD.worker_image
113	RUNPOD_TEMPLATE_ID = RUNPOD.template_id
114	RUNPOD_VOLUME_MOUNT_PATH = RUNPOD.volume_mount_path
115	LIVE_TEST_CONTAINER_DISK_GB = int(get_env("REIGH_LIVE_TEST_CONTAINER_DISK_GB", "200") or 200)
116	LIVE_TEST_DISK_SIZE_GB = int(get_env("REIGH_LIVE_TEST_DISK_SIZE_GB", "200") or 200)
117	RUNPOD_DISK_SIZE_GB = RUNPOD.disk_size_gb
118	RUNPOD_CONTAINER_DISK_GB = RUNPOD.container_disk_gb
119	RUNPOD_MIN_VCPU_COUNT = RUNPOD.min_vcpu_count
120	RUNPOD_MIN_MEMORY_GB = RUNPOD.min_memory_gb
121	RUNPOD_STORAGE_VOLUMES = RUNPOD.storage_volumes
122	RUNPOD_RAM_TIERS = RUNPOD.ram_tiers
123	
124	TIMEOUT_IMAGE_SEC = 900
125	TIMEOUT_INDIVIDUAL_TRAVEL_SEGMENT_SEC = 1500
126	TIMEOUT_TRAVEL_ORCHESTRATOR_SEC = 2400
127	
128	LTX_MODEL_ID = "ltx2_22B_distilled_1_1"
129	
130	ANCHOR_IMAGE_A_URL = (
131	    "https://[REDACTED]/storage/v1/object/public/image_uploads/"
132	    [REDACTED]
133	)
134	ANCHOR_IMAGE_B_URL = (
135	    "https://[REDACTED]/storage/v1/object/public/image_uploads/"
136	    "8a9fdac5-ed89-482c-aeca-c3dd7922d53c/e2699835-35d2-4547-85f5-d59219341e4d-"
137	    "u1_3c8779e7-54b4-436c-bfce-9eee8872e370.jpeg"
138	)
139	
140	FIXTURES: dict[str, Path] = {
141	    "qwen_image_basic": WORKER_ROOT
142	    / [REDACTED],
143	    "qwen_image_edit_basic": WORKER_ROOT
144	    / [REDACTED],
145	    "z_image_turbo_i2i_basic": WORKER_ROOT
146	    / [REDACTED],
147	    "qwen_image_style_db_task": WORKER_ROOT
148	    / [REDACTED],
149	    "wan22_i2v_individual_segment": WORKER_ROOT
150	    / [REDACTED],
151	}
152	
153	
154	def load_fixture_json(case_name: str) -> dict[str, Any]:
155	    fixture_path = FIXTURES[case_name]
156	    import json
157	
158	    return json.loads(fixture_path.read_text(encoding="utf-8"))
159	
160	
161	def __getattr__(name: str):
162	    if name in {
163	        "DatabaseClient",
164	        "RunpodLifecycleMixin",
165	        "SSHClient",
166	        "get_pod_ssh_details",
167	        "terminate_pod",
168	    }:
169	        return getattr(live_test_pkg, name)
170	    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
171	
172	
173	__all__ = [
174	    "ANCHOR_IMAGE_A_URL",
175	    "ANCHOR_IMAGE_B_URL",
176	    "DatabaseClient",
177	    "ENV",
178	    "FIXTURES",
179	    "LTX_MODEL_ID",
180	    "ORCHESTRATOR_ROOT",
181	    "RunpodLifecycleMixin",
182	    "RUNPOD",
183	    "RUNPOD_CONTAINER_DISK_GB",
184	    "RUNPOD_DISK_SIZE_GB",
185	    "RUNPOD_GPU_TYPE",
186	    "RUNPOD_MIN_MEMORY_GB",
187	    "RUNPOD_MIN_VCPU_COUNT",
188	    "RUNPOD_RAM_TIERS",
189	    "RUNPOD_STORAGE_VOLUMES",
190	    "RUNPOD_TEMPLATE_ID",
191	    "RUNPOD_VOLUME_MOUNT_PATH",
192	    "RUNPOD_WORKER_IMAGE",
193	    "SSHClient",
194	    "TIMEOUT_IMAGE_SEC",
195	    "TIMEOUT_INDIVIDUAL_TRAVEL_SEGMENT_SEC",
196	    "TIMEOUT_TRAVEL_ORCHESTRATOR_SEC",
197	    "WORKER_ROOT",
198	    "get_env",
199	    "get_pod_ssh_details",
200	    "load_fixture_json",
201	    "require_env",
202	    "terminate_pod",
203	]
204
```

> AGENT

Perfect! Now let me check vibecomfy's pyproject.toml for requirements:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/pyproject.toml",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	[build-system]
2	requires = ["hatchling>=1.20"]
3	build-backend = "hatchling.build"
4	
5	[project]
6	name = "vibecomfy"
7	version = "0.1.0"
8	description = "Python scratchpads for discovering, editing, validating, and running ComfyUI workflows."
9	readme = "README.md"
10	requires-python = ">=3.11"
11	dependencies = [
12	  "huggingface_hub[hf_xet]>=0.32.0",
13	  "httpx>=0.25",
14	  "pyyaml>=6",
15	  "websockets>=12",
16	]
17	
18	[project.optional-dependencies]
19	dev = [
20	  "pytest>=7",
21	  "pytest-asyncio>=0.23",
22	]
23	runpod-local = [
24	  "python-dotenv>=1.0",
25	  "runpod-lifecycle @ git+https://github.com/banodoco/runpod-lifecycle.git@v0.1.1",
26	]
27	runpod-launch = [
28	  "python-dotenv>=1.0",
29	  "runpod-lifecycle @ git+https://github.com/banodoco/runpod-lifecycle.git@v0.1.1",
30	]
31	
32	[project.scripts]
33	vibecomfy = "vibecomfy.cli:main"
34	
35	[project.entry-points."vibecomfy.plugins"]
36	# my_plugin = "my_pkg:register"
37	
38	[tool.hatch.build.targets.wheel]
39	packages = ["vibecomfy"]
40	
41	[tool.pytest.ini_options]
42	asyncio_mode = "auto"
43	testpaths = ["tests"]
44	addopts = "-m 'not gpu'"
45	markers = [
46	  "gpu: marks tests that provision live GPU resources",
47	  "runpod: opt-in smoke tests that provision real RunPod GPU pods (requires --runpod and RUNPOD_API_KEY).",
48	  "runpod_full: opt-in production-resolution matrix tests; multi-pod, ~$5-10 per run (requires --runpod-full and RUNPOD_API_KEY).",
49	]
50	
51	[tool.hatch.metadata]
52	allow-direct-references = true
53
```

> AGENT

Excellent context. Now let me do a final check for custom_nodes.lock and prepare my findings:

> TOOL

tool_use Bash
```json
{
  "command": "head -30 /Users/user_c042661f/Documents/reigh-workspace/vibecomfy/custom_nodes.lock"
}
```

> TOOL

tool_result Bash
```
ComfyUI-KJNodes b7646ad70a7daa7aeb919ca542274758d26ba2df https://github.com/kijai/ComfyUI-KJNodes.git
ComfyUI-QwenTTS d8122a8ba835b65fd65c113d2b273b1ad1579293 https://github.com/1038lab/ComfyUI-QwenTTS.git
ComfyUI-WanVideoWrapper df8f3e49daaad117cf3090cc916c83f3d001494c https://github.com/kijai/ComfyUI-WanVideoWrapper.git
```

> AGENT

Perfect! Now I have enough information to compile the comprehensive survey. Let me generate the report.

---

## Summary: Reusable PrebuiltRunPod/VibeComfy Validation Environment Survey

**Workspace:** `/Users/user_c042661f/Documents/reigh-workspace`

### 1. **reigh-worker/** — Live-Test Harness

**Top-level paths:**
- Entry point: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/main.py` (lines 1–100)
- SSH bootstrap & pod lifecycle: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ssh_bootstrap.py` (lines 1–366)
- Config & RunPod defaults: `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/config.py` (lines 1–203)
- Variant-fresh (pod provisioning): `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/variant_fresh.py` (lines 1–250+)

**Key bootstrap commands:**
1. **uv sync + install** (`ssh_bootstrap.py:166–196`): APT packages, uv installation, `uv sync --extra cuda124` with retry logic, hardlink-disabled copy mode for MooseFS network volumes.
2. **VibeComfy checkout + install** (`ssh_bootstrap.py:199–236`): Clone VibeComfy branch, `pip install -e`, install HiddenSwitch ComfyUI fork + ComfyScript, run `vibecomfy.cli nodes restore --lockfile custom_nodes.lock`, validate template_index.json & coverage.json.
3. **SageAttention optional install** (`ssh_bootstrap.py:65–77`): Conditional based on `VIBECOMFY_ATTENTION_PROFILE`; clones & installs from `thu-ml/SageAttention`.

**RunPod config:**
- GPU type resolution (`variant_fresh.py:168–186`): Calls `runpod_lifecycle.api.find_gpu_type(requested_gpu_type, api_key)`
- Image, disk, memory (`config.py:89–100`): Defaults to `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`, 50 GB container + 200 GB live-test overrides, storage volumes fallback chain (Peter → EU-NO-1 → EU-CZ-1 → EUR-IS-1), RAM tiers (72–16 GB)
- VibeComfy env injection (`variant_fresh.py:103–130`): `REIGH_BACKEND`, `VIBECOMFY_PATH`, `VIBECOMFY_ATTENTION_PROFILE`, `REIGH_SELECTOR_NAMESPACE`, worker profile

**No prebuilt image/snapshot concept yet:** All live tests start from base image + 46min uv sync + 21min VibeComfy install.

---

### 2. **vibecomfy/** — VibeComfy Install & Templates

**Top-level paths:**
- Ready templates root: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/ready_templates/` (subdirs: smoke, image, video, edit, audio)
- Bootstrap script (VibeComfy): Handled entirely by `reigh-worker/scripts/live_test/ssh_bootstrap.py:199–236` on the pod.
- Custom nodes lock: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/custom_nodes.lock` (pins KJNodes, QwenTTS, WanVideoWrapper, etc.)
- Project config: `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/pyproject.toml` (lines 1–50)

**Template index:** `template_index.json` (generated by `refresh_template_index`) + manifest: `vibecomfy/workflow_corpus/manifests/coverage.json`

**No RunPod prebuilt setup:** VibeComfy has scripts `runpod_validate.py`, `runpod_model_matrix.py`, `runpod_corpus_matrix.py` for independent GPU runs; these are *separate* from reigh-worker live-test harness.

---

### 3. **runpod-lifecycle/** — Pod Provisioning API

**Top-level paths:**
- Main API: `/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/__init__.py` (lines 1–66)
- Lifecycle orchestration: `/Users/user_c042661f/Documents/reigh-workspace/runpod-lifecycle/src/runpod_lifecycle/lifecycle.py` (lines 205–284, async launch signature)

**Public API surface:**
- `launch(config: RunPodConfig, *, name, hooks)` — Returns `Pod` object (async)
- `find_gpu_type(gpu_type_str, api_key)` — Resolves GPU by name string
- `get_network_volumes(api_key)` — Lists available storage
- `create_network_volume(...)` — Creates persistent volume
- No built-in snapshot/image creation; all pods spawn from base image + SSH bootstrap upload

**Config fields:** `gpu_type_candidates` (list), `min_memory_gb`, `disk_size_gb`, `container_disk_gb`, `volume_mount_path`, `storage_name` + `storage_volumes` (fallback chain), `ram_tiers` (tuple for fallback), `ssh_public_key_path`, `worker_image`, `template_id`

---

### 4. **docs/** — Migration & Validation

**Live-test & prebuilt relevant docs:**
- `/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy-live-validation.md` (lines 1–100+): Defines execution primitives (Python ready templates, not raw JSON); mentions VibeComfy's `runpod_runner.py` for pod lifecycle; notes existing surfaces to reuse (PodGuard, artifact download).
- `/Users/user_c042661f/Documents/reigh-workspace/docs/migration-vibecomfy.md`: Parent design document (threshold YAML, route canonicalization, WGP repeatability evidence).

**Key note:** No existing notion of *prebuilt pod snapshots* or *cached venv images*. Migration design assumes ephemeral pods + fresh installs.

---

### 5. **.claude/** — Agent Skill Discovery

- `/Users/user_c042661f/Documents/reigh-workspace/.claude/skills/megaplan.md`: Agent manifest (generic megaplan skill)
- `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.claude/settings.local.json`: Local worker harness config (settings only, no CLAUDE.md agent instructions)
- `/Users/user_c042661f/Documents/reigh-workspace/vibecomfy/CLAUDE.md` (18KB): Comprehensive agent guide for VibeComfy (five flows, CLI, testing, repo rules, vocabulary, decision shortcuts)

---

### **Opportunity for Prebuilt Image**

The 67-minute overhead (46min uv sync + 21min VibeComfy install) can be eliminated by:

1. **Custom RunPod image** (Dockerfile): Base `runpod/pytorch:2.4.0...` → add uv, git, ffmpeg → `uv sync --extra cuda124` → `pip install -e vibecomfy` → `vibecomfy.cli nodes restore` → commit/push to docker registry.
2. **RunPod snapshot:** If using `runpod-lifecycle`'s storage + pod template features, pre-stage the venv on a network volume (MooseFS) as a tar.gz, then unpack on startup (~3min vs 67min).
3. **Custom network volume:** Pre-populate `VIBECOMFY_PATH` on a persistent storage volume; mount read-only or copy-on-write on each pod spawn.

None of these exist yet; current live-test assumes full bootstrap each run.
