> DEVELOPER

请仔细阅读以下文件，提取所有关键修改内容和实现细节：

1. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
   - 重点：NVFP4_AWQ 命名处理、pre_quant_scale 的完整实现（from_config, create_weights, process_weights_after_loading, apply 四处）、ModelOptFp4Config 和 ModelOptFp4LinearMethod 的关键字段

2. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py
   - 重点：load_weights 里跳过未知 tensor 的修改

3. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py
   - 重点：infllm_v2 的导入方式（硬导入还是 try/except）、compressed_attention 函数的关键调用链

4. /root/shared-nvme/openbmb/demo-sala/prepare_env.sh 完整内容
5. /root/shared-nvme/openbmb/demo-sala/prepare_model.sh 完整内容
6. /root/shared-nvme/openbmb/demo-sala/preprocess_model.py 完整内容

对每个文件，请给出：
- 文件总行数
- 关键修改的具体代码片段（带行号）
- 是否有 TODO 或未完成的内容

请返回完整的代码片段，不要省略。

> AGENT

正在读取这些文件并整理关键信息。

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/prepare_env.sh",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/prepare_env.sh"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/prepare_model.sh",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/prepare_model.sh"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/preprocess_model.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/preprocess_model.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> AGENT

正在确认各文件行数并搜索所有 `TODO` 注释。

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "TODO|FIXME",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "TODO|FIXME",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "TODO|FIXME",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use run_terminal_command_v2
```json
{
  "command": "wc -l /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py /root/shared-nvme/openbmb/demo-sala/prepare_env.sh /root/shared-nvme/openbmb/demo-sala/prepare_model.sh /root/shared-nvme/openbmb/demo-sala/preprocess_model.py",
  "cwd": "",
  "options": {
    "timeout": 30000
  },
  "parsingResult": {
    "executableCommands": [
      {
        "name": "wc",
        "args": [
          {
            "type": "word",
            "value": "-l"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/prepare_env.sh"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/prepare_model.sh"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/demo-sala/preprocess_model.py"
          }
        ],
        "fullText": "wc -l /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py /root/shared-nvme/openbmb/demo-sala/prepare_env.sh /root/shared-nvme/openbmb/demo-sala/prepare_model.sh /root/shared-nvme/openbmb/demo-sala/preprocess_model.py"
      }
    ]
  },
  "commandDescription": "Count lines in requested files"
}
```

> TOOL

tool_result run_terminal_command_v2
```
null
```

> AGENT

以下为按文件整理的阅读结果（行数按编辑器/Read 工具末行计：`modelopt_quant.py` 1825 行，`minicpm.py` 676 行，`minicpm_sparse_utils.py` 1663 行，`prepare_env.sh` 10 行，`prepare_model.sh` 7 行，`preprocess_model.py` 45 行）。

---

## 1. `modelopt_quant.py`（1825 行）

### 关键修改与实现要点

**NVFP4_AWQ 等前缀归一化**：凡 `quant_algo` 以 `NVFP4` 开头（含 `NVFP4_AWQ`）一律视为 `NVFP4`，再参与后续校验与 `is_checkpoint_nvfp4_serialized`。

```999:1008:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
        # Normalize NVFP4 variants (e.g. NVFP4_AWQ) to "NVFP4"
        if quant_method.startswith("NVFP4"):
            quant_method = "NVFP4"
        if not quant_method in ["FP8", "NVFP4"]:
            raise ValueError(
                f"ModelOpt currently only supports: FP8, NVFP4"
                " quantizations in sglang. Please check the "
                "quantization config for your model's configuration."
            )
        is_checkpoint_nvfp4_serialized = "NVFP4" in quant_method
```

**`pre_quant_scale` — `from_config`**：从扁平 `config` 或嵌套 `config["quantization"]` 读 `pre_quant_scale` 真值，写入 `ModelOptFp4Config.has_pre_quant_scale`。

```1020:1035:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
        # Detect AWQ pre_quant_scale from either nested or flat config
        has_pre_quant_scale = False
        quant_section = config.get("quantization", {})
        if isinstance(quant_section, dict) and quant_section.get("pre_quant_scale"):
            has_pre_quant_scale = True
        if config.get("pre_quant_scale"):
            has_pre_quant_scale = True

        return cls(
            is_checkpoint_nvfp4_serialized,
            kv_cache_quant_algo,
            group_size,
            exclude_modules,
            config.get("packed_modules_mapping"),
            has_pre_quant_scale,
        )
```

**`ModelOptFp4Config` 关键字段**（构造函数与 `get_quant_method` 绑定的 Linear/MoE 方法）：

```858:878:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
class ModelOptFp4Config(ModelOptQuantConfig):
    """Config class for FP4."""

    def __init__(
        self,
        is_checkpoint_nvfp4_serialized: bool = False,
        kv_cache_quant_algo: str = None,
        group_size: int = None,
        exclude_modules: List[str] = None,
        packed_modules_mapping: Optional[Dict[str, List[str]]] = None,
        has_pre_quant_scale: bool = False,
    ) -> None:
        super().__init__(kv_cache_quant_algo, exclude_modules, packed_modules_mapping)
        self.is_checkpoint_nvfp4_serialized = is_checkpoint_nvfp4_serialized
        self.has_pre_quant_scale = has_pre_quant_scale
        if is_checkpoint_nvfp4_serialized:
            logger.warning(
                "Detected nvfp4 checkpoint. Please note that the "
                "format is experimental and subject to change."
            )
        self.group_size = group_size
```

```1058:1064:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
    def get_quant_method(self, layer: torch.nn.Module, prefix: str):
        return self._get_quant_method(
            layer,
            prefix,
            Linear=ModelOptFp4LinearMethod,
            Moe=ModelOptNvFp4FusedMoEMethod,  # FlashInferFP4MoE needs the same quantization method but with compatible attribute handling
        )
```

**`pre_quant_scale` — `create_weights`**：在 NVFP4 序列化路径下，若 `has_pre_quant_scale` 为真，注册与当前分区 `input_size_per_partition` 同长度的 `pre_quant_scale`（初值全 1，`ModelWeightParameter`）。

```1159:1167:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
        # AWQ checkpoints may include per-channel pre_quant_scale for input smoothing.
        if self.quant_config.has_pre_quant_scale:
            pre_quant_scale = ModelWeightParameter(
                data=torch.ones(input_size_per_partition, dtype=torch.float32),
                input_dim=0,
                output_dim=None,
                weight_loader=weight_loader,
            )
            layer.register_parameter("pre_quant_scale", pre_quant_scale)
```

**`pre_quant_scale` — `process_weights_after_loading`**：加载后把 `pre_quant_scale` 放到 CUDA，并转为 `bfloat16`，便于前向中 `x * pre_quant_scale` 在 bf16 上完成。

```1175:1183:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
        # Finalize AWQ pre_quant_scale: move to CUDA and cast to bf16 so that
        # x * pre_quant_scale stays in bf16 without an extra .to() in apply().
        if hasattr(layer, "pre_quant_scale"):
            layer.pre_quant_scale = Parameter(
                layer.pre_quant_scale.data.to(
                    device="cuda", dtype=torch.bfloat16
                ),
                requires_grad=False,
            )
```

**`pre_quant_scale` — `apply`**：在 `fp4_quantize` 之前对激活乘以 `pre_quant_scale`（与注释一致：避免在 `apply` 里再做 `.to()`）。

```1246:1249:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
        # Quantize BF16 or FP16 to (FP4 and interleaved block scale)
        if hasattr(layer, "pre_quant_scale"):
            x = x * layer.pre_quant_scale
        x_fp4, x_scale_interleaved = fp4_quantize(x, layer.input_scale_inv)
```

**`ModelOptFp4LinearMethod` 其它要点**（与 checkpoint 结构对应）：`weight` 为 `uint8` 打包 FP4；`input_scale`、`weight_scale_2` 为 per-partition 标量参数；`weight_scale` 为按 `group_size` 分块的 FP8 block scale；`process_weights` 里合并标量、可选 TRTLLM shuffle、或对 `weight_scale` 做 pad/permute 得到 `weight_scale_interleaved`；`apply` 里用 `fp4_gemm`。**`get_min_capability`** 返回 `100`（Blackwell 相关）。完整 `from_config` 还包含 flat/nested 两种格式、`group_size` 提取、`kv_cache_quant_algo` 推导、`common_group_size` 等逻辑（约 930–1019 行），此处按你的四点已把 **NVFP4 归一化 + pre_quant 四处** 单独列全。

### TODO / 未完成标记

- L151：`MOE_NVFP4_DISPATCH` 默认策略，待 DeepEP PR 合并后再改默认。  
- L741：`ModelOpt FP8 MoE` 路由方式扩展。  
- L760：`FIXME` FlashInfer `trtllm_fp8_block_scale_moe` 忽略 `output` 参数。  
- L1261：`TODO([REDACTED])` FlashInfer 版本与默认 backend。  
- L1329：`TODO(ch-wan)` NVFP4 MoE `intermediate_size_per_partition` 赋值是否必需。

---

## 2. `minicpm.py`（676 行）

### `load_weights`：跳过未知 / 量化侧多出 tensor

在走完 `stacked_params_mapping` 与 `expert_params_mapping` 后，若参数名不在 `params_dict`（例如 checkpoint 含当前图未注册的量化权重名），**直接 `continue`**，避免 `KeyError`；同时保留对 `.bias` 的跳过。

```662:673:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py
                else:
                    # Skip loading extra bias for GPTQ models.
                    if name.endswith(".bias") and name not in params_dict:
                        continue
                    # Skip unknown quantization-related weights
                    if name not in params_dict:
                        continue
                    param = params_dict[name]
                    weight_loader = getattr(
                        param, "weight_loader", default_weight_loader
                    )
                    weight_loader(param, loaded_weight)
```

### TODO

- L474：`MiniCPMDecoderLayer._compute_topk` 的 prefill 路径——“完整 TopK 用 kernel”仍为 `pass`，注释写明待实现。

---

## 3. `minicpm_sparse_utils.py`（1663 行）

### `infllm_v2` 导入方式：**硬导入**（无 try/except）

_module 顶层直接：`from infllm_v2 import infllmv2_attn_stage1, max_pooling_1d_varlen`。未安装或导入失败会在 import 阶段抛错，而不是降级路径。

```25:26:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py
import triton
from infllm_v2 import infllmv2_attn_stage1, max_pooling_1d_varlen
```

### `compressed_attention` 主调用链（完整函数，无省略）

逻辑概要：`no_grad` → 按需沿 head 维 `repeat_interleave` 使 q/k head 比 ≥16 → 区分 prefill/decode；**decode 且 `split_stage1`** 时用 `torch.bmm`+`softmax`+reshape/sum 算 `score`；**否则**调用 **`infllmv2_attn_stage1(q,k,k2,...)`** 得 `score` → **`max_pooling_1d_varlen(...)`** 得 `block_score` → **`topk` + `sort`** → `int32` 的 `topk_idx`。

```398:543:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py
def compressed_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    k2: torch.Tensor,
    kernel_size: int,
    kernel_stride: int,
    block_size: int,
    topk: int,
    cu_seqlens_q: torch.Tensor,
    cu_seqlens_k: torch.Tensor,
    cu_seqlens_k2: torch.Tensor,
    max_seqlen_q: int,
    # max_seqlen_k: int,
    max_context_len: int,
    sm_scale: Optional[float] = None,
    init_blocks: int = 1,
    local_blocks: int = 2,
    cache_lens: Optional[torch.Tensor] = None,
    total_q: int = -1,
    cu_seqlens_q_adjusted: Optional[torch.Tensor] = None,
    max_seqlen_q_adjusted: Optional[int] = None,
    split_stage1: bool = False,
) -> torch.Tensor:
    """Compressed attention computation for sparse attention.

    Computes attention scores between query and compressed keys (k and k2),
    then performs max pooling and selects top-k blocks.

    Args:
        q: Query tensor, shape (total_q_len, num_heads, head_dim)
        k: Compressed key tensor k1, shape (total_k_len, num_heads, head_dim)
        k2: Compressed key tensor k2, shape (total_k_len, num_heads, head_dim)
        kernel_size: Size of compression kernel
        kernel_stride: Stride of compression kernel
        block_size: Size of attention blocks
        topk: Number of top blocks to select
        cu_seqlens_q: Cumulative sequence lengths for query, shape (batch_size + 1)
        cu_seqlens_k: Cumulative sequence lengths for k, shape (batch_size + 1)
        cu_seqlens_k2: Cumulative sequence lengths for k2, shape (batch_size + 1)
        max_seqlen_q: Maximum sequence length in query
        max_seqlen_k: Maximum sequence length in key
        sm_scale: Softmax scaling factor (unused, kept for compatibility)
        init_blocks: Number of initial blocks to always attend to
        local_blocks: Number of local blocks to consider
        cache_lens: Cache lengths for each batch (optional)
        total_q: Total number of queries (used for pooling)
        cu_seqlens_q_adjusted: Adjusted cumulative sequence lengths for query (for stage1 optimization)
        max_seqlen_q_adjusted: Adjusted maximum sequence length for query (for stage1 optimization)

    Returns:
        Top-k block indices, shape (num_heads, total_q_len, topk)
    """
    with torch.no_grad():
        batch_size = cu_seqlens_q.shape[0] - 1

        current_ratio = q.shape[-2] // k.shape[-2]
        required_ratio = 16
        if current_ratio < required_ratio:
            repeat_times = required_ratio // current_ratio
            q = q.repeat_interleave(repeat_times, dim=-2)

        is_prefilling = max_seqlen_q > 1

        # Stage1 optimization: q_idx computation is no longer needed
        if is_prefilling:
            if cache_lens is None:
                cache_lens = torch.zeros(batch_size, dtype=torch.int32, device=q.device)
        #     q_idx = torch.cat(
        #         [
        #             (
        #                 torch.arange(
        #                     cu_seqlens_q[i + 1] - cu_seqlens_q[i], device=q.device
        #                 )
        #                 + cache_lens[i]
        #             )
        #             // block_size
        #             for i in range(batch_size)
        #         ],
        #         dim=0,
        #     )
        # else:
        #     q_idx = cache_lens // block_size


        # split-stage1 -> bmm+softmax+reduce_sum
        if not is_prefilling and split_stage1:
            batch_size = q.shape[0]
            k1_len = k.shape[0]
            q_head = q.shape[1]
            kv_head = k.shape[1]
            group_size = q_head // kv_head
            head_dim = k.shape[2]
            q_reshape = (
                q.reshape(batch_size, 1, q_head, head_dim)
                    .transpose(1, 2)
                    .reshape(batch_size, kv_head, group_size, head_dim)
                    .transpose(0, 1)
                    .reshape(-1, group_size, head_dim)
            )
            k_reshape = (
                k.reshape(batch_size, k1_len // batch_size, kv_head, head_dim)
                .transpose(1, 2)
                .transpose(-2, -1)
                .transpose(0, 1)
                .reshape(-1, head_dim, k1_len // batch_size)
            )
    
            scale = 1.0 / math.sqrt(head_dim)
            score = torch.bmm(q_reshape, k_reshape).mul_(scale)
            torch.nan_to_num(score, nan=float("-inf"), posinf=float("-inf"), out=score)
            torch.softmax(score, dim=-1, out=score)
            score = score.reshape(kv_head, batch_size, group_size, k1_len // batch_size).sum(dim=2)
        else:  
            score = infllmv2_attn_stage1(
                q.contiguous(),
                k.contiguous(),
                k2.contiguous(),
                cu_seqlens_q=cu_seqlens_q_adjusted,
                cu_seqlens_k=cu_seqlens_k,
                cu_seqlens_v=cu_seqlens_k2,
                max_seqlen_q=max_seqlen_q_adjusted,
                max_seqlen_k=max_context_len // kernel_stride,
                causal=is_prefilling
            )

        block_score = max_pooling_1d_varlen(
            score.contiguous(),
            cu_seqlens_q,
            cu_seqlens_k,
            cache_lens,
            max_seqlen_q,
            # max_seqlen_k,
            max_context_len,
            local_blocks=local_blocks,
            init_blocks=init_blocks,
            block_size=block_size,
            stride=kernel_stride,
            total_q=total_q,
        )

        topk_idx = block_score.topk(topk, dim=-1).indices.sort(-1).values
        # Stage1 optimization: skip q_idx filtering
        # topk_idx[topk_idx > q_idx[None, :, None]] = -1
        topk_idx = topk_idx.to(torch.int32)

    return topk_idx
```

**上游与 `compressed_attention` 的关系**：同文件中 `get_compress_k_v2` / `allocate_and_compress_keys` 等通过 Triton kernel 从 KV cache 生成压缩的 `k1/k2`；`compressed_attention` 消费这些压缩 K 与 Q，完成 stage1 分数与 top-k 块索引（调用方可与 flash attention 路径衔接）。

### TODO

- L155：`get_compress_k_v2` 内注释 `# TODO in summary, the arguments needed are:`，后面是参数清单说明性 TODO，非实现缺口标题。

---

## 4. `prepare_env.sh`（10 行，全文）

```1:10:/root/shared-nvme/openbmb/demo-sala/prepare_env.sh
#!/usr/bin/env bash

echo "[prepare_env] start $(date '+%F %T')"

uv pip install --no-deps -e ./sglang/python

export SGLANG_SERVER_ARGS="${SGLANG_SERVER_ARGS:-} --log-level info"

echo "[prepare_env] done"
```

**TODO**：无。

---

## 5. `prepare_model.sh`（7 行，全文）

```1:7:/root/shared-nvme/openbmb/demo-sala/prepare_model.sh
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "${SCRIPT_DIR}/preprocess_model.py" "$@"
```

**TODO**：无。

---

## 6. `preprocess_model.py`（45 行，全文）

```1:45:/root/shared-nvme/openbmb/demo-sala/preprocess_model.py
"""
Simple model copy for MiniCPM-SALA submission demo.

Usage:
    python preprocess_model.py --input /path/to/model --output /path/to/output
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    src = Path(args.input).resolve()
    dst = Path(args.output).resolve()

    if not src.is_dir():
        raise FileNotFoundError(f"Input model dir not found: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    count = 0
    for f in sorted(src.iterdir()):
        if f.name.startswith("."):
            continue
        target = dst / f.name
        if not target.exists():
            if f.is_dir():
                shutil.copytree(f, target)
            else:
                shutil.copy2(f, target)
            count += 1

    print(f"[preprocess] done — copied {count} files from {src} to {dst}")


if __name__ == "__main__":
    main()
```

**TODO**：无。说明：已存在目标路径下的同名条目会跳过，只做“增量拷贝”，非强制镜像整个目录。

---

### 小结表

| 文件 | 行数 | TODO/FIXME |
|------|------|------------|
| `modelopt_quant.py` | 1825 | 多处（MOE、FlashInfer、NVFP4 MoE 等） |
| `minicpm.py` | 676 | prefill TopK 未实现 |
| `minicpm_sparse_utils.py` | 1663 | `get_compress_k_v2` 内注释型 TODO |
| `prepare_env.sh` | 10 | 无 |
| `prepare_model.sh` | 7 | 无 |
| `preprocess_model.py` | 45 | 无 |

若你需要把 `ModelOptFp4Config.from_config` 整段（930–1035）也以“无删节”形式贴出，可以说一下我按同一格式补上（当前回复已按你列的四点把 `pre_quant_scale` 与 `NVFP4_AWQ` 相关行完整给出）。
