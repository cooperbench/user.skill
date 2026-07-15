> DEVELOPER

Can you do a diff between this branch and main? I specifically want a PR description that includes specifics about what was modified. I also want to understand how the training code relates to the d2l_train code we already had.

> TOOL

tool_use Bash
id: toolu_01FZdy88cWwcLWXSsUBhAZzi
```json
{
  "command": "git log main..HEAD --oneline",
  "description": "List commits on branch since main"
}
```

> TOOL

tool_result
id: toolu_01FZdy88cWwcLWXSsUBhAZzi
```
223b5e4 docs: training upgrade usage guide and README refresh
4bbd8cf feat(hpo): training-hyperparameter HPO study with Hyperband
49a1a8a feat(training): diff-aware loss collator and trainer subclass
56958af feat(training): train.sh unified wrapper + trainer_cli
1651a96 feat(training): mined-pairs → SFT chat converter
32dc16f feat(training): MLflow tracking in QLoRA trainer
```

> TOOL

tool_use Bash
id: toolu_01Pr9v2XmcnxEkFEauKqmpTq
```json
{
  "command": "git diff main..HEAD --stat",
  "description": "Show diff stats vs main"
}
```

> TOOL

tool_result
id: toolu_01Pr9v2XmcnxEkFEauKqmpTq
```
docs/plans/training_upgrade.md                     | 224 +++++++++
 libs/model-training/README.md                      |  33 ++
 libs/model-training/src/model_training/d2l_data.py | 139 +++++-
 .../model-training/src/model_training/diff_loss.py | 230 +++++++++
 libs/model-training/src/model_training/trainer.py  | 468 +++++++++++++++++-
 .../src/model_training/trainer_cli.py              | 227 +++++++++
 libs/model-training/tests/test_diff_loss.py        | 141 ++++++
 libs/model-training/tests/test_lora_overrides.py   | 150 ++++++
 libs/model-training/tests/test_pairs_to_chat.py    | 158 +++++++
 libs/model-training/tests/test_trainer_cli.py      | 214 +++++++++
 libs/model-training/tests/test_trainer_mlflow.py   | 107 +++++
 scripts/optimization/run_training_hpo.py           | 521 +++++++++++++++++++++
 scripts/optimization/tests/__init__.py             |   0
 scripts/optimization/tests/test_training_hpo.py    | 193 ++++++++
 scripts/train.sh                                   |  56 +++
 15 files changed, 2834 insertions(+), 27 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01NwibDgNNbFqMLq5xBQPawo
```json
{
  "command": "git show --stat 32dc16f 1651a96 56958af 49a1a8a 4bbd8cf 223b5e4",
  "description": "Show stats for each commit"
}
```

> TOOL

tool_result
id: toolu_01NwibDgNNbFqMLq5xBQPawo
```
commit 32dc16f431070cbe94535ef7a911116089b309d3
Author: Noah Dolev <noah@elixirtrials.com>
Date:   Tue Apr 21 15:20:54 2026 +0000

    feat(training): MLflow tracking in QLoRA trainer
    
    Add MLflow helpers to trainer.py mirroring the pattern in d2l_train.py so
    QLoRA runs produce the same tracking surface as the distillation pipeline.
    Helpers are gated by RUNE_DISABLE_MLFLOW=1 and by mlflow ImportError, so
    CPU-only environments and tests continue to work unchanged.
    
    - _setup_mlflow_trainer: configure tracking URI + experiment (env fallback)
    - _mlflow_log_params / _mlflow_log_artifact: silent no-ops on failure
    - _mlflow_log_output_artifacts: logs adapter safetensors + config.json
    - _mlflow_run context manager: start/end run, logs params, guards finally
    - train_qlora / train_and_register: new mlflow_experiment and
      mlflow_tracking_uri kwargs; SFTConfig.report_to toggles to "mlflow"
      when enabled so per-step loss streams natively via TRL.
    
    Tests: libs/model-training/tests/test_trainer_mlflow.py covers the
    RUNE_DISABLE_MLFLOW path, the ImportError path, the log-helper no-op
    path, and the new kwargs surface on both public functions.
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

 libs/model-training/src/model_training/trainer.py | 142 +++++++++++++++++++++-
 libs/model-training/tests/test_trainer_mlflow.py  | 107 ++++++++++++++++
 2 files changed, 244 insertions(+), 5 deletions(-)

commit 1651a96fe7d1fc5a9be5c90b62cd1cab26faaa98
Author: Noah Dolev <noah@elixirtrials.com>
Date:   Tue Apr 21 15:27:54 2026 +0000

    feat(training): mined-pairs → SFT chat converter
    
    Add pairs_to_chat_messages() in d2l_data.py and wire a dataset_path branch
    into train_qlora / train_and_register so QLoRA can train directly […]

> AGENT

Now let me check how `d2l_train` relates to the new `trainer` code.

> TOOL

tool_use Bash
id: toolu_013c5DjTRE4CpRosRzYCW2z1
```json
{
  "command": "ls libs/model-training/src/model_training/",
  "description": "List model-training source"
}
```

> TOOL

tool_result
id: toolu_013c5DjTRE4CpRosRzYCW2z1
```
__init__.py  1.8K
config.py  2.8K
d2l_config.py  9.2K
d2l_data.py  31.4K
d2l_diff.py  3.6K
d2l_lora.py  7.7K
d2l_mining.py  10.3K
d2l_prep.py  3.4K
d2l_probe.py  9.0K
d2l_train.py  27.1K
diff_loss.py  8.8K
github_client.py  5.4K
hypernetwork.py  15.3K
merging.py  5.3K
model_configs.py  6.5K
peft_utils.py  2.1K
py.typed  0B
sakana_d2l.py  26.3K
trainer.py  30.4K
trainer_cli.py  6.9K
trajectory.py  4.0K

21 files, 0 dirs (20 .py, 1 .typed)
```

> TOOL

tool_use Bash
id: toolu_01Rph755tZhhZwvLbbpKqoFG
```json
{
  "command": "git show main:libs/model-training/src/model_training/trainer.py | head -50",
  "description": "Check base trainer.py on main"
}
```

> TOOL

tool_result
id: toolu_01Rph755tZhhZwvLbbpKqoFG
```
"""QLoRA training orchestrator.

All GPU-dependent imports (datasets, transformers, trl, torch) are deferred
inside function bodies to ensure CPU-only importability (INFRA-05).

Module-level imports: stdlib only.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict


class _ResolvedParams(TypedDict):
    """Resolved training parameters after merging registry defaults."""

    base_model_id: str | None
    warm_start: str | None
    rank: int
    alpha: int
    epochs: int
    grad_accum: int
    lr_sched: str
    attn_impl: str | None


def _resolve_training_params(
    *,
    model_config_name: str | None,
    base_model_id: str | None,
    warm_start_adapter_id: str | None,
    rank: int | None,
    alpha: int | None,
    epochs: int | None,
    gradient_accumulation_steps: int | None,
    lr_scheduler_type: str | None,
) -> _ResolvedParams:
    """Resolve training parameters from registry defaults and explicit overrides.

    Args:
        model_config_name: Registry lookup key (e.g. "qwen3.5-9b").
        base_model_id: Explicit model ID override.
        warm_start_adapter_id: Explicit warm-start adapter override.
        rank: Explicit LoRA rank override.
        alpha: Explicit LoRA alpha override.
        epochs: Explicit epochs override.
```

> TOOL

tool_use Bash
id: toolu_0158fquRdr5MC7aMM6JknQ55
```json
{
  "command": "git show main:libs/model-training/src/model_training/trainer.py | wc -l\ngit show HEAD:libs/model-training/src/model_training/trainer.py | wc -l\ngit show HEAD:libs/model-training/src/model_training/d2l_train.py | wc -l",
  "description": "Compare file sizes"
}
```

> TOOL

tool_result
id: toolu_0158fquRdr5MC7aMM6JknQ55
```
     398
     814
     752
```

> TOOL

tool_use Read
id: toolu_01LXp5TZGDkomSeX6qufGzst
```json
{
  "file_path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/d2l_train.py",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01LXp5TZGDkomSeX6qufGzst
```
1	"""KL-divergence context distillation training loop for Qwen3-Coder-Next.
2	
3	Assembles all Phase 25-28 components (config, data pipeline, activation
4	extraction, weight transfer, functional LoRA injection) into a complete
5	distillation training script.
6	
7	Three execution modes:
8	- dry-run: loads real base model + hypernet, validates tensor shapes, exits
9	- smoke-test: 5 training steps, verifies finite loss and decreasing trend
10	- full: trains from JSONL dataset with tiered checkpointing and MLflow tracking
11	
12	All heavy GPU imports (torch, transformers, peft) are deferred to function
13	bodies per INFRA-05 project convention.
14	
15	Usage:
16	    uv run python -m model_training.d2l_train --dry-run
17	    uv run python -m model_training.d2l_train --smoke-test
18	    uv run python -m model_training.d2l_train --dataset path/to/train.jsonl
19	"""
20	
21	from __future__ import annotations
22	
23	import logging
24	import os
25	from pathlib import Path
26	from typing import Any
27	
28	from pydantic import BaseModel, Field, field_validator
29	
30	logger = logging.getLogger(__name__)
31	
32	__all__ = ["train_d2l_qwen3", "D2LTrainConfig"]
33	
34	
35	def _require_probe_cache(model_name: str) -> None:
36	    """Raise RuntimeError if probe cache is absent for *model_name*.
37	
38	    Called before build_qwen3_hypernet_config so training never proceeds with
39	    placeholder feature_sizes that […]

> TOOL

tool_use Bash
id: toolu_01XDr5uDXLRVD2rkCRwVnBZd
```json
{
  "command": "grep -n \"def \" libs/model-training/src/model_training/d2l_train.py | head -30",
  "description": "List functions in d2l_train"
}
```

> TOOL

tool_result
id: toolu_01XDr5uDXLRVD2rkCRwVnBZd
```
12 matches in 1F:

[file] libs/.../model_training/d2l_train.py (12):
    35: def _require_probe_cache(model_name: str) -> None:
   110: def model_post_init(self, __context: Any) -> None:
   120: def _validate_lr(cls, v: float) -> float:
   128: def _validate_alpha(cls, v: float) -> float:
   136: def _validate_temperature(cls, v: float) -> float:
   144: def _validate_num_steps(cls, v: int) -> int:
   151: def _compute_kl_ce_loss(
   225: def _training_step(
   300: def _save_checkpoint(
   354: def _setup_mlflow(config: D2LTrainConfig) -> None:
   375: def _dry_run_validate_shapes(config: D2LTrainConfig) -> dict[str, Any]:
   486: def train_d2l_qwen3(config: D2LTrainConfig) -> dict[str, Any]:  # noqa: C901
```

> TOOL

tool_use Grep
id: toolu_016yS7G5MeU5bZm1dWyTb1Mx
```json
{
  "pattern": "def |^class \">\n<parameter name=\"path\">/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/trainer.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_016yS7G5MeU5bZm1dWyTb1Mx
```
No matches found
```

> TOOL

tool_use Grep
id: toolu_01M7tA72FnNhpuwB83PRvkXV
```json
{
  "pattern": "^def |^class |^    def ",
  "path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/trainer.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01M7tA72FnNhpuwB83PRvkXV
```
23:def _setup_mlflow_trainer(
51:def _mlflow_log_params(params: dict[str, Any]) -> None:
61:def _mlflow_log_artifact(path: str) -> None:
71:def _mlflow_log_output_artifacts(output_dir: str) -> None:
82:def _mlflow_run(
103:class _ResolvedParams(TypedDict):
116:def _resolve_training_params(
179:def _override_lora_alpha(
220:def _override_lora_dropout(
257:def _validate_data_source(
280:def _build_training_dataset(
324:def _construct_sft_trainer(
375:def train_qlora(
657:def train_and_register(
```

> TOOL

tool_use Read
id: toolu_01B6N8Yy6AqVJKfF2uCrTyh2
```json
{
  "file_path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/trainer.py",
  "offset": 375,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01B6N8Yy6AqVJKfF2uCrTyh2
```
375	def train_qlora(
376	    session_id: str | None,
377	    adapter_id: str,
378	    output_dir: str,
379	    *,
380	    base_model_id: str | None = None,
381	    task_type: str = "code-gen",
382	    rank: int | None = None,
383	    alpha: int | None = None,
384	    epochs: int | None = None,
385	    learning_rate: float = 2e-4,
386	    model_config_name: str | None = None,
387	    warm_start_adapter_id: str | None = None,
388	    gradient_accumulation_steps: int | None = None,
389	    lr_scheduler_type: str | None = None,
390	    mlflow_experiment: str = "rune-qlora",
391	    mlflow_tracking_uri: str | None = None,
392	    dataset_path: str | None = None,
393	    encoding_mode: str = "multi_turn",
394	    diff_aware_loss: bool = False,
395	    diff_changed_weight: float = 1.0,
396	    diff_unchanged_weight: float = 0.3,
397	    override_lora_alpha: int | None = None,
398	    override_lora_dropout: float | None = None,
399	) -> str:
400	    """Train a QLoRA adapter from a recorded coding trajectory.
401	
402	    Orchestrates the full training pipeline: load trajectory, format as SFT
403	    messages, build dataset, load model with NF4 quantization, train with SFT,
404	    and save the adapter to output_dir.
405	
406	    When model_config_name is provided, training defaults (rank, alpha, LR
407	    schedule, gradient accumulation, attention […]

> TOOL

tool_use Bash
id: toolu_0193pKCPbbQfAcq9Ugx18Lx8
```json
{
  "command": "git show main:libs/model-training/src/model_training/trainer.py | grep -n \"def train_qlora\\|def train_and_register\\|^def \\|^class \"",
  "description": "Check public API of main trainer"
}
```

> TOOL

tool_result
id: toolu_0193pKCPbbQfAcq9Ugx18Lx8
```
18:class _ResolvedParams(TypedDict):
31:def _resolve_training_params(
94:def train_qlora(
275:def train_and_register(
```

> TOOL

tool_use Bash
id: toolu_01J8muJ4sMmwqu96ioaxCFEV
```json
{
  "command": "git show main:libs/model-training/src/model_training/trainer.py | sed -n '94,130p'",
  "description": "Show old train_qlora signature"
}
```

> TOOL

tool_result
id: toolu_01J8muJ4sMmwqu96ioaxCFEV
```
def train_qlora(
    session_id: str,
    adapter_id: str,
    output_dir: str,
    *,
    base_model_id: str | None = None,
    task_type: str = "code-gen",
    rank: int | None = None,
    alpha: int | None = None,
    epochs: int | None = None,
    learning_rate: float = 2e-4,
    model_config_name: str | None = None,
    warm_start_adapter_id: str | None = None,
    gradient_accumulation_steps: int | None = None,
    lr_scheduler_type: str | None = None,
) -> str:
    """Train a QLoRA adapter from a recorded coding trajectory.

    Orchestrates the full training pipeline: load trajectory, format as SFT
    messages, build dataset, load model with NF4 quantization, train with SFT,
    and save the adapter to output_dir.

    When model_config_name is provided, training defaults (rank, alpha, LR
    schedule, gradient accumulation, attention implementation) are loaded from
    the model registry. When the registry config specifies a warm_start_adapter_id,
    the pre-trained adapter is loaded via PeftModel.from_pretrained and training
    continues from those weights instead of initializing fresh LoRA matrices.

    All GPU imports are deferred to this function body; the module is safe to
    import in CPU-only environments.

    Args:
        session_id: Trajectory session ID to train from.
        adapter_id: Unique identifier for the resulting adapter.
        output_dir: Directory to save the trained adapter weights.
        base_model_id: HuggingFace model ID. Overrides […]

> TOOL

tool_use Read
id: toolu_01FMdenPkBHYJqwVHymzRu1T
```json
{
  "file_path": "/Users/noahdolevelixir/Code/rune/docs/plans/training_upgrade.md",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01FMdenPkBHYJqwVHymzRu1T
```
1	# Training Infrastructure Upgrade
2	
3	Comprehensive overhaul of Rune's QLoRA fine-tuning pipeline to support
4	optimal DeltaCoder warm-start training on mined GitHub trajectories,
5	with MLflow tracking, a one-command CLI wrapper, diff-aware loss
6	weighting, and a training-hyperparameter HPO study.
7	
8	## Motivation
9	
10	The existing `trainer.py` fine-tuning path had three gaps relative to the
11	goal (fine-tune the pre-warmed DeltaCoder adapter on mined trajectories
12	optimally, so the resulting LoRA can train a Doc-to-LoRA hypernetwork):
13	
14	1. **No MLflow** — experiments were untracked. Only `d2l_train.py`
15	   (the KL-divergence distillation path) had MLflow wiring.
16	2. **Only trajectory JSONs were accepted** — mined pairs from
17	   `scripts/mine_github.py --batch` use an activation/teacher split
18	   that `format_for_sft` can't consume.
19	3. **HPO optimized inference, not training** — the existing Optuna study
20	   in `scripts/optimization/run_optimization.py` tunes scaling, prompt
21	   style, and sampling temperature, not learning rate / rank / alpha.
22	
23	The upgrade closes all three gaps and adds a diff-aware loss variant so
24	HPO can A/B the collator against vanilla SFT.
25	
26	## Usage
27	
28	### One-command training
29	
30	```bash
31	# Mined-pair training (DeltaCoder warm-start on Qwen3.5-9B […]

> TOOL

tool_use Bash
id: toolu_01Wqj6DGdjKuB3izuAYxGpSD
```json
{
  "command": "git show main:libs/model-training/src/model_training/d2l_data.py | grep -n \"^def \\|^class \\|^__all__\"",
  "description": "List d2l_data public API on main"
}
```

> TOOL

tool_result
id: toolu_01Wqj6DGdjKuB3izuAYxGpSD
```
22:__all__ = [
256:def save_jsonl(records: list[dict[str, Any]], path: str | Path) -> None:
270:def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
287:def format_for_distillation(trajectory: dict[str, Any]) -> list[dict[str, str]]:
344:def normalize_mined_trajectory(mined: dict[str, Any]) -> dict[str, Any]:
424:def generate_needle_dataset(n: int = 20) -> list[dict[str, str]]:
471:def generate_trajectory_dataset(
524:def augment_trajectories(
629:def split_by_task_id(
658:def _group_steps_into_blocks(
679:def _make_pair_record(
701:def normalize_mined_pairs(
```

> TOOL

tool_use Grep
id: toolu_01Jjk1nhF1rTExXEjniGAqzV
```json
{
  "pattern": "^def |^class |^__all__",
  "path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/d2l_data.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01Jjk1nhF1rTExXEjniGAqzV
```
26:__all__ = [
261:def save_jsonl(records: list[dict[str, Any]], path: str | Path) -> None:
275:def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
292:def format_for_distillation(trajectory: dict[str, Any]) -> list[dict[str, str]]:
349:def normalize_mined_trajectory(mined: dict[str, Any]) -> dict[str, Any]:
429:def generate_needle_dataset(n: int = 20) -> list[dict[str, str]]:
476:def generate_trajectory_dataset(
529:def augment_trajectories(
634:def split_by_task_id(
663:def _group_steps_into_blocks(
684:def _make_pair_record(
706:def normalize_mined_pairs(
792:def _extract_revision(activation_text: str, teacher_text: str) -> str:
813:def _pairs_to_single_turn(
833:def _group_pairs_by_task(
852:def pairs_to_chat_messages(
```

> TOOL

tool_use Read
id: toolu_016tm3UZNFpZmoGeFQf2hsxR
```json
{
  "file_path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/d2l_data.py",
  "offset": 852,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_016tm3UZNFpZmoGeFQf2hsxR
```
852	def pairs_to_chat_messages(
853	    pairs: list[dict[str, Any]],
854	    *,
855	    mode: Literal["multi_turn", "single_turn"] = "multi_turn",
856	    system_prompt: str = SYSTEM_PROMPT,
857	) -> list[list[dict[str, str]]]:
858	    """Convert mined pair records into SFT chat conversations.
859	
860	    ``multi_turn`` (preferred when pairs share a ``source_task_id``): emits
861	    one conversation per task grouping — ``[system, user_1, assistant_1,
862	    user_2, assistant_2, ...]`` — where each (user, assistant) pair is one
863	    review→revision cycle. This preserves the attempt-error-correction
864	    structure so the adapter can encode the trajectory rather than only the
865	    final code.
866	
867	    ``single_turn``: emits one conversation per pair (no clustering). Useful
868	    when ``metadata.source_task_id`` is missing or the caller prefers flat
869	    examples. Each conversation is ``[system, user, assistant]``.
870	
871	    Pairs are grouped in the order they appear in the input; within a group,
872	    pairs are sorted by ``metadata.step_index`` to preserve chronological
873	    order of review cycles. Empty input returns ``[]``.
874	
875	    Args:
876	        pairs: List of pair records as emitted by ``normalize_mined_pairs``.
877	            Each record must have ``activation_text`` and ``teacher_text``.
878	            ``metadata.source_task_id`` and ``metadata.step_index`` are used
879	            for grouping/ordering when present; fall back to ``task_id``.
880	        mode: ``"multi_turn"`` clusters pairs by task_id; ``"single_turn"`` […]

> TOOL

tool_use Bash
id: toolu_01SgWKKf1yevT1TVKbAtvosV
```json
{
  "command": "grep -n \"pairs_to_chat_messages\\|normalize_mined_pairs\\|format_for_distillation\" libs/model-training/src/model_training/d2l_train.py scripts/mine_github.py 2>/dev/null | head -20",
  "description": "Check usage of key data functions"
}
```

> TOOL

tool_result
id: toolu_01SgWKKf1yevT1TVKbAtvosV
```
0 matches for 'pairs_to_chat_messages\|normalize_mined_pairs\|format_for_distillation'
```

> TOOL

tool_use Grep
id: toolu_01F8JTjRreE3BmLV5NUKMtTN
```json
{
  "pattern": "pairs_to_chat_messages|normalize_mined_pairs|format_for_distillation",
  "path": "/Users/noahdolevelixir/Code/rune",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01F8JTjRreE3BmLV5NUKMtTN
```
Found 8 files
libs/model-training/tests/test_pairs_to_chat.py
libs/model-training/src/model_training/trainer.py
libs/model-training/src/model_training/d2l_data.py
docs/plans/training_upgrade.md
libs/model-training/src/model_training/__init__.py
scripts/mine_github.py
libs/model-training/tests/test_d2l_data.py
libs/model-training/src/model_training/d2l_prep.py
```

> TOOL

tool_use Grep
id: toolu_01Y2ACNXfnvnwxTx5uVCvnUu
```json
{
  "pattern": "format_for_distillation|normalize_mined_pairs",
  "path": "/Users/noahdolevelixir/Code/rune/libs/model-training/src/model_training/d2l_prep.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01Y2ACNXfnvnwxTx5uVCvnUu
```
4:format_for_distillation on each trajectory and persisting the resulting
18:from model_training.d2l_data import format_for_distillation, save_jsonl
53:    Reads each input file, calls format_for_distillation on every trajectory,
57:    format_for_distillation and produce zero records — they do not raise.
74:            records = format_for_distillation(traj)
```

> AGENT

I have everything I need. Let me write up the PR description and the relationship analysis.

## Branch vs `main`: 6 commits, 15 files, +2,834 / −27

### Suggested PR title
`feat(training): QLoRA upgrade — MLflow, mined-pair SFT, train.sh, diff-aware loss, training HPO`

### Suggested PR description

```markdown
## Summary

Overhauls the QLoRA training path (`libs/model-training/src/model_training/trainer.py`) so the DeltaCoder warm-start adapter can be optimally fine-tuned on mined GitHub trajectories, with experiment tracking, a one-command wrapper, a diff-weighted loss variant, and a training-side HPO study. Closes three gaps vs. `main`:

1. `trainer.py` had no MLflow — only `d2l_train.py` did.
2. `trainer.py` accepted only recorded trajectory sessions — not the JSONL emitted by `scripts/mine_github.py --batch`.
3. The existing Optuna study (`run_optimization.py`) tunes *inference* knobs (scaling, prompt style, temperature), not training knobs (lr, alpha, dropout, schedule).

## What changed, by commit

### `32dc16f` — MLflow tracking in QLoRA trainer
`libs/model-training/src/model_training/trainer.py`
- `_setup_mlflow_trainer`, `_mlflow_log_params`, `_mlflow_log_artifact`, `_mlflow_log_output_artifacts`, `_mlflow_run` context manager.
- New `mlflow_experiment` and `mlflow_tracking_uri` kwargs on `train_qlora` / `train_and_register`.
- `SFTConfig.report_to = "mlflow"` when enabled, so per-step loss streams natively via TRL.
- Gated by `RUNE_DISABLE_MLFLOW=1` and by `mlflow` ImportError — CPU-only/CI paths unchanged.
- Tests: `tests/test_trainer_mlflow.py` (disable env var, ImportError, log no-ops, kwargs […]