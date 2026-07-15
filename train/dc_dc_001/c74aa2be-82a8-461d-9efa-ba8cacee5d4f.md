> DEVELOPER

请完整读取以下文件，返回全部内容（较长的文件可以返回关键部分，但请标明行号）：

1. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
   - 重点：ModelOptFp4Config.from_config 方法（pre_quant_scale 处理），create_weights，process_weights_after_loading，apply 方法
   - 返回这几个方法的完整代码
   
2. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py
   - 重点：load_weights 方法完整内容
   
3. /root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
   - 搜索并返回关于 has_sparse_attention, force_dense_minicpm, sparse_config, NVFP4 相关的所有代码段
   
4. /root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py 完整内容
   
5. /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/__init__.py 完整内容

6. 运行：ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so
   并运行：strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so | grep -E "sm_[0-9]+" | sort -u

注意：这是只读任务，不要修改任何文件。

> AGENT

正在读取这些文件并运行只读的 `ls` 与 `strings` 命令。

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

tool_use ripgrep_raw_search
```json
{
  "pattern": "def load_weights",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "has_sparse_attention|force_dense_minicpm|sparse_config|NVFP4|nvfp4",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "caseInsensitive": true
}
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py"
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
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/__init__.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/__init__.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use run_terminal_command_v2
```json
{
  "command": "ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so 2>&1; strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so 2>&1 | grep -E \"sm_[0-9]+\" | sort -u",
  "cwd": "",
  "options": {
    "timeout": 30000
  },
  "parsingResult": {
    "executableCommands": [
      {
        "name": "ls",
        "args": [
          {
            "type": "word",
            "value": "-la"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
          }
        ],
        "fullText": "ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
      },
      {
        "name": "strings",
        "args": [
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
          }
        ],
        "fullText": "strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
      },
      {
        "name": "grep",
        "args": [
          {
            "type": "word",
            "value": "-E"
          },
          {
            "type": "string",
            "value": "\"sm_[0-9]+\""
          }
        ],
        "fullText": "grep -E \"sm_[0-9]+\""
      },
      {
        "name": "sort",
        "args": [
          {
            "type": "word",
            "value": "-u"
          }
        ],
        "fullText": "sort -u"
      }
    ],
    "hasRedirects": true
  },
  "commandDescription": "List .so and extract sm_* arch strings"
}
```

> TOOL

tool_result run_terminal_command_v2
```
null
```

> AGENT

正在读取 `minicpm.py` 中的 `load_weights` 及 `model_config.py` 中 `sparse_config` 相关段落；因终端输出为空，正在验证 `.so` 是否存在。

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py",
  "offset": 590,
  "limit": 120,
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

tool_use ripgrep_raw_search
```json
{
  "pattern": "sparse",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use run_terminal_command_v2
```json
{
  "command": "ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so; strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so | grep -E \"sm_[0-9]+\" | sort -u",
  "cwd": "",
  "options": {
    "timeout": 30000
  },
  "parsingResult": {
    "executableCommands": [
      {
        "name": "ls",
        "args": [
          {
            "type": "word",
            "value": "-la"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
          }
        ],
        "fullText": "ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
      },
      {
        "name": "strings",
        "args": [
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
          }
        ],
        "fullText": "strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
      },
      {
        "name": "grep",
        "args": [
          {
            "type": "word",
            "value": "-E"
          },
          {
            "type": "string",
            "value": "\"sm_[0-9]+\""
          }
        ],
        "fullText": "grep -E \"sm_[0-9]+\""
      },
      {
        "name": "sort",
        "args": [
          {
            "type": "word",
            "value": "-u"
          }
        ],
        "fullText": "sort -u"
      }
    ]
  },
  "commandDescription": "Verify .so exists and list sm_* strings"
}
```

> TOOL

tool_result run_terminal_command_v2
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "sparse_config",
  "path": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "caseInsensitive": false
}
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "offset": 95,
  "limit": 200,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py"
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
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "offset": 660,
  "limit": 180,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py"
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
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "offset": 850,
  "limit": 80,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2",
  "globPattern": "C*.so"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py",
  "offset": 300,
  "limit": 35,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> AGENT

以下为只读汇总。说明：`model_config.py` 里**没有名为 `sparse_config` 的标识符**；与稀疏相关的逻辑在 `has_sparse_attention`、`force_dense_minicpm`、`dual_chunk_attention_config` 与 `get_sparse_attention_config` 等处。工作区内对 `infllm_v2/C.cpython-310-x86_64-linux-gnu.so` 的 glob 未找到该文件；在此环境执行的 `ls`/`strings` 未产生可见输出（可能路径不存在或沙箱限制），请你本机再执行一次用户给出的两条命令确认。

---

## 1. `modelopt_quant.py` — `ModelOptFp4Config` / `ModelOptFp4LinearMethod` 相关方法

### `ModelOptFp4Config.from_config`（含 `pre_quant_scale`）

```930:1035:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> ModelOptFp4Config:
        # Handle two different config formats:
        # 1. hf_quant_config.json format: {"quantization": {"quant_algo": "NVFP4", ...}}
        # 2. config.json quantization_config format: {"quant_algo": "NVFP4", ...}
        # In future modelopt will deprecate hf_quant_config.json, and only keep config.json.
        # For legacy reasons, we keep hf_quant_config.json for now.

        # Initialize variables
        kv_cache_quant_algo = None
        group_size = None
        exclude_modules = []

        # Try flat format first (config.json quantization_config - preferred format)
        quant_method = config.get("quant_algo")
        if quant_method is not None:
            # Flat format (config.json quantization_config)
            # Note: FP4 models in config.json format may not have all the detailed fields
            # that are present in hf_quant_config.json, so we need to handle defaults
            kv_cache_quant_algo = config.get("kv_cache_quant_algo")
            if not kv_cache_quant_algo:
                # For config.json format, derive from kv_cache_scheme if available
                kv_cache_scheme = config.get("kv_cache_scheme")
                if isinstance(kv_cache_scheme, dict):
                    if (
                        kv_cache_scheme.get("type") == "float"
                        and kv_cache_scheme.get("num_bits") == 8
                    ):
                        kv_cache_quant_algo = "FP8"
                    else:
                        kv_cache_quant_algo = "auto"
                elif isinstance(kv_cache_scheme, str):
                    scheme_name = kv_cache_scheme.strip().upper()
                    if scheme_name in ("FP8", "FLOAT8"):
                        kv_cache_quant_algo = "FP8"
                    elif scheme_name in ("FP4", "FLOAT4", "NVFP4"):
                        kv_cache_quant_algo = "NVFP4"
                    else:
                        kv_cache_quant_algo = "auto"
                else:
                    kv_cache_quant_algo = "auto"

            group_size = config.get("group_size")
            # If group_size is not at top level, try to extract from config_groups
            if group_size is None:
                config_groups = config.get("config_groups", {})
                if config_groups:
                    # Get group_size from the first group's weights config
                    first_group = next(iter(config_groups.values()), {})
                    weights_config = first_group.get("weights", {})
                    group_size = weights_config.get("group_size")

            exclude_modules = config.get("ignore", [])
        else:
            # Fall back to nested format (hf_quant_config.json - legacy format)
            try:
                quant_config = cls.get_from_keys(config, ["quantization"])
                quant_method = quant_config["quant_algo"]
                kv_cache_quant_algo = quant_config.get("kv_cache_quant_algo")
                if not kv_cache_quant_algo:
                    kv_cache_quant_algo = "auto"
                group_size = ModelOptFp4Config.common_group_size(config)
                exclude_modules = quant_config.get("exclude_modules", [])
            except (ValueError, KeyError):
                raise ValueError(
                    "Cannot find 'quant_algo' in the model's quantization config. "
                    "Expected either flat format (config.json) or nested format (hf_quant_config.json)."
                )

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

        if group_size is None or exclude_modules is None:
            logger.warning(
                f"group_size: {group_size},"
                f"kv_cache_quant_algo: {kv_cache_quant_algo},"
                f"exclude_modules: {exclude_modules}"
            )
            raise ValueError(
                "NVFP4 quantization requires group_size and exclude_modules "
                "specified in the quantization config"
            )
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

### `ModelOptFp4LinearMethod.create_weights`

```1085:1167:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
    def create_weights(
        self,
        layer: torch.nn.Module,
        input_size_per_partition: int,
        output_partition_sizes: List[int],
        input_size: int,
        output_size: int,
        params_dtype: torch.dtype,
        **extra_weight_attrs,
    ):
        del input_size, output_size
        if not self.quant_config.is_checkpoint_nvfp4_serialized:
            raise ValueError(
                "NVFP4 quantization was selected, "
                " dynamic quantization is not supported."
            )

        output_size_per_partition = sum(output_partition_sizes)
        weight_loader = extra_weight_attrs.get("weight_loader")

        layer.logical_widths = output_partition_sizes

        layer.input_size_per_partition = input_size_per_partition
        layer.output_size_per_partition = output_size_per_partition
        if input_size_per_partition % 16 != 0:
            raise ValueError(
                "Unsupported model when in features size is " "not multiple of 16"
            )

        weight_dtype = (
            torch.float8_e4m3fn
            if self.quant_config.is_checkpoint_nvfp4_serialized
            else params_dtype
        )

        weight = ModelWeightParameter(
            data=torch.empty(
                # 2 fp4 data is packed in one uint8 in the input dimension
                output_size_per_partition,
                input_size_per_partition // 2,
                dtype=torch.uint8,
            ),
            input_dim=1,
            output_dim=0,
            weight_loader=weight_loader,
        )
        layer.register_parameter("weight", weight)

        input_scale = PerTensorScaleParameter(
            data=torch.empty(len(output_partition_sizes), dtype=torch.float32),
            weight_loader=weight_loader,
        )

        layer.register_parameter("input_scale", input_scale)

        weight_scale_2 = PerTensorScaleParameter(
            data=torch.empty(len(output_partition_sizes), dtype=torch.float32),
            weight_loader=weight_loader,
        )
        layer.register_parameter("weight_scale_2", weight_scale_2)

        weight_scale = ModelWeightParameter(
            data=torch.empty(
                output_size_per_partition,
                input_size_per_partition // self.quant_config.group_size,
                dtype=weight_dtype,
            ),
            input_dim=1,
            output_dim=0,
            weight_loader=weight_loader,
        )

        layer.register_parameter("weight_scale", weight_scale)

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

### `ModelOptFp4LinearMethod.process_weights_after_loading`

```1169:1233:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
    def process_weights_after_loading(self, layer: torch.nn.Module) -> None:
        input_scale_2 = layer.input_scale.max().to(torch.float32)
        weight_scale_2 = layer.weight_scale_2.max().to(torch.float32)
        layer.input_scale = Parameter(input_scale_2, requires_grad=False)
        layer.weight_scale_2 = Parameter(weight_scale_2, requires_grad=False)

        # Finalize AWQ pre_quant_scale: move to CUDA and cast to bf16 so that
        # x * pre_quant_scale stays in bf16 without an extra .to() in apply().
        if hasattr(layer, "pre_quant_scale"):
            layer.pre_quant_scale = Parameter(
                layer.pre_quant_scale.data.to(
                    device="cuda", dtype=torch.bfloat16
                ),
                requires_grad=False,
            )
        layer.alpha = Parameter(
            layer.input_scale * layer.weight_scale_2, requires_grad=False
        )
        layer.input_scale_inv = Parameter(
            (1 / input_scale_2).to(torch.float32), requires_grad=False
        )
        if FLASHINFER_FP4_GEMM_BACKEND == "trtllm":
            # FlashInfer TRTLLM FP4 GEMM requires a different weight layout.
            # FlashInfer provides nvfp4_quantize to quantize + shuffle the
            # layout but we use our own quantization so we have to call
            # shuffles ourselves.
            from flashinfer import shuffle_matrix_a, shuffle_matrix_sf_a

            weight = layer.weight
            scale = layer.weight_scale
            epilogue_tile_m = 128
            weight = shuffle_matrix_a(weight.view(torch.uint8), epilogue_tile_m)
            scale = (
                shuffle_matrix_sf_a(scale.view(torch.uint8), epilogue_tile_m)
                .reshape(scale.shape)
                .view(torch.float8_e4m3fn)
            )

            layer.weight_scale_interleaved = Parameter(scale, requires_grad=False)
            layer.weight = Parameter(weight, requires_grad=False)
            return
        # Pad and blockwise interleave weight_scale
        scales = layer.weight_scale
        scale_ndim = scales.ndim
        if scale_ndim == 2:
            scales = scales.unsqueeze(0)
        assert scales.ndim == 3
        B, M, K = scales.shape
        round_up_multiple = lambda x, m: (x + m - 1) // m * m
        M_padded = round_up_multiple(M, 128)
        K_padded = round_up_multiple(K, 4)
        padded_scales = torch.zeros((B, M_padded, K_padded), dtype=scales.dtype)
        padded_scales[:B, :M, :K] = scales
        batches, rows, cols = padded_scales.shape
        assert rows % 128 == 0
        assert cols % 4 == 0
        padded_scales = padded_scales.reshape(batches, rows // 128, 4, 32, cols // 4, 4)
        padded_scales = padded_scales.permute((0, 1, 4, 3, 2, 5))
        padded_scales = padded_scales.contiguous().cuda()
        padded_scales = (
            padded_scales.reshape(M_padded, K_padded)
            if scale_ndim == 2
            else padded_scales.reshape(B, M_padded, K_padded)
        )
        layer.weight_scale_interleaved = Parameter(padded_scales, requires_grad=False)
```

### `ModelOptFp4LinearMethod.apply`

```1235:1277:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
    def apply(
        self,
        layer: torch.nn.Module,
        x: torch.Tensor,
        bias: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        output_dtype = x.dtype
        x_m, _ = x.shape
        w_n, _ = layer.weight.shape
        output_shape = [x_m, w_n]

        # Quantize BF16 or FP16 to (FP4 and interleaved block scale)
        if hasattr(layer, "pre_quant_scale"):
            x = x * layer.pre_quant_scale
        x_fp4, x_scale_interleaved = fp4_quantize(x, layer.input_scale_inv)

        assert x_fp4.dtype == torch.uint8
        assert layer.weight.dtype == torch.uint8
        assert layer.weight_scale_interleaved.dtype == torch.float8_e4m3fn
        assert layer.alpha.dtype == torch.float32

        w = layer.weight
        w_scale_interleaved = layer.weight_scale_interleaved
        if enable_flashinfer_fp4_gemm:
            w = layer.weight.T
            w_scale_interleaved = layer.weight_scale_interleaved.T
        # TODO([REDACTED])
        # Remove the default after flashinfer bumped to 0.5.1
        backend = (
            FLASHINFER_FP4_GEMM_BACKEND if FLASHINFER_FP4_GEMM_BACKEND else "cutlass"
        )
        out = fp4_gemm(
            x_fp4,
            w,
            x_scale_interleaved,
            w_scale_interleaved,
            layer.alpha,
            output_dtype,
            w_n,
        )
        if bias is not None:
            out = out + bias
        return out.view(*output_shape)
```

---

## 2. `minicpm.py` — `load_weights` 全文

```610:673:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py
    def load_weights(self, weights: Iterable[Tuple[str, torch.Tensor]]):
        stacked_params_mapping = [
            # (param_name, shard_name, shard_id)
            ("qkv_proj", "q_proj", "q"),
            ("qkv_proj", "k_proj", "k"),
            ("qkv_proj", "v_proj", "v"),
            ("gate_up_proj", "gate_proj", 0),
            ("gate_up_proj", "up_proj", 1),
        ]
        expert_params_mapping = [
            # (param_name, weight_name, expert_id)
            (
                "ws" if weight_name in ["w1", "w3"] else "w2s",
                f"experts.{expert_id}.{weight_name}.weight",
                expert_id,
            )
            for expert_id in range(self.num_experts)
            for weight_name in ["w1", "w2", "w3"]
        ]
        params_dict = dict(self.named_parameters())
        for name, loaded_weight in weights:
            if "rotary_emb.inv_freq" in name:
                continue
            if "rotary_emb.cos_cached" in name or "rotary_emb.sin_cached" in name:
                # Models trained using ColossalAI may include these tensors in
                # the checkpoint. Skip them.
                continue
            if self.config.tie_word_embeddings and "lm_head.weight" in name:
                continue

            for param_name, weight_name, shard_id in stacked_params_mapping:
                if weight_name not in name:
                    continue
                name = name.replace(weight_name, param_name)
                # Skip loading extra bias for GPTQ models.
                if name.endswith(".bias") and name not in params_dict:
                    continue
                param = params_dict[name]
                weight_loader = param.weight_loader
                weight_loader(param, loaded_weight, shard_id)
                break
            else:
                for param_name, weight_name, expert_id in expert_params_mapping:
                    if weight_name not in name:
                        continue
                    name = name.replace(weight_name, param_name)
                    param = params_dict[name]
                    weight_loader = param.weight_loader
                    weight_loader(
                        param, loaded_weight, weight_name, expert_id=expert_id
                    )
                    break
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

---

## 3. `model_config.py` — 稀疏 / NVFP4 相关片段

**`force_dense_minicpm` 构造与传入**

```107:158:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
        force_dense_minicpm: bool = False,
    ) -> None:
        # Parse args
        self.model_path = model_path
        ...
        self.force_dense_minicpm = force_dense_minicpm
```

```316:317:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
            force_dense_minicpm=server_args.force_dense_minicpm,
            **kwargs,
```

**`has_sparse_attention` 与各 sparse_* 属性（从 `hf_config` 读取；`force_dense_minicpm` 时关掉稀疏层 id）**

```235:283:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
    @property
    def has_sparse_attention(self):
        """Check if model has sparse attention (accesses hf_config.has_sparse_attention)."""
        return getattr(self.hf_config, "has_sparse_attention", False) if not self.force_dense_minicpm else False

    @property
    def has_lightning_layers(self):
        """Check if model has lightning layers (accesses hf_config.has_lightning_layers)."""
        return getattr(self.hf_config, "has_lightning_layers", False)

    @property
    def sparse_layer_ids(self):
        """Get layer IDs with sparse attention (accesses hf_config.sparse_layer_ids)."""
        return getattr(self.hf_config, "sparse_layer_ids", []) if not self.force_dense_minicpm else []

    @property
    def lightning_layer_ids(self):
        """Get layer IDs with lightning attention (accesses hf_config.lightning_layer_ids)."""
        return getattr(self.hf_config, "lightning_layer_ids", [])

    @property
    def sparse_block_size(self):
        """Get sparse block size (accesses hf_config.sparse_block_size)."""
        return getattr(self.hf_config, "sparse_block_size", 32)

    @property
    def sparse_kernel_size(self):
        """Get sparse kernel size (accesses hf_config.sparse_kernel_size)."""
        return getattr(self.hf_config, "sparse_kernel_size", 32)

    @property
    def sparse_kernel_stride(self):
        """Get sparse kernel stride (accesses hf_config.sparse_kernel_stride)."""
        return getattr(self.hf_config, "sparse_kernel_stride", 16)

    @property
    def sparse_topk(self):
        """Get sparse topk value (accesses hf_config.sparse_topk)."""
        return getattr(self.hf_config, "sparse_topk", 8)

    @property
    def sparse_window_size(self):
        """Get sparse window size (accesses hf_config.sparse_window_size)."""
        return getattr(self.hf_config, "sparse_window_size", 64)

    @property
    def sparse_dense_len(self):
        """Get sparse dense length (accesses hf_config.sparse_dense_len)."""
        return getattr(self.hf_config, "sparse_dense_len", 512)
```

**双块注意力：合并外部 `sparse_attention_config`（无 `sparse_config` 字段名）**

```879:894:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
    def _verify_dual_chunk_attention_config(self) -> None:
        if hasattr(self.hf_config, "dual_chunk_attention_config"):
            # Try loading the sparse attention config
            sparse_attn_config = get_sparse_attention_config(self.model_path)
            if not sparse_attn_config:
                return
            self.hf_config.dual_chunk_attention_config["sparse_attention_config"] = (
                sparse_attn_config
            )
            if (
                "sparse_attention_enabled"
                not in self.hf_config.dual_chunk_attention_config
            ):
                self.hf_config.dual_chunk_attention_config[
                    "sparse_attention_enabled"
                ] = True
```

**NVFP4 / modelopt_fp4**

```686:725:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
    def _parse_modelopt_quant_config(self, quant_config_dict: dict) -> Optional[dict]:
        """Parse ModelOpt quantization config and return the appropriate quant_method."""
        json_quant_configs = quant_config_dict["quantization"]
        quant_algo = json_quant_configs.get("quant_algo", None)

        if quant_algo == "MIXED_PRECISION":
            return {"quant_method": "w4afp8"}
        elif quant_algo and ("FP4" in quant_algo or "NVFP4" in quant_algo):
            return {"quant_method": "modelopt_fp4"}
        elif quant_algo and "FP8" in quant_algo:
            return {"quant_method": "modelopt_fp8"}
        else:
            return None
    ...
    def _get_modelopt_quant_type(self) -> str:
        """Extract ModelOpt quantization type from unified quantization flag."""
        if self.quantization == "modelopt_fp8":
            return "fp8"
        elif self.quantization == "modelopt_fp4":
            return "nvfp4"
```

```762:804:/root/shared-nvme/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py
        rocm_supported_quantization = [
            ...
            "petit_nvfp4",
            ...
        ]
        optimized_quantization_methods = [
            ...
            "modelopt_fp4",
            ...
            "petit_nvfp4",
            ...
        ]
        compatible_quantization_methods = {
            "modelopt_fp8": ["modelopt"],
            "modelopt_fp4": ["modelopt"],
            "petit_nvfp4": ["modelopt"],
            ...
        }
```

文件第 34 行有 `from ... get_sparse_attention_config` 的 import，与上面 `_verify_dual_chunk_attention_config` 一致。

---

## 4. `setup.py` 全文（267 行）

已在工具读取中完整取得；若你需要整文件粘贴，该路径为 `/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py`，结构与要点如下：

- `INFLLM_V2_FORCE_BUILD` / `SKIP_CUDA_BUILD` / `FORCE_CXX11_ABI`（约 24–29 行）
- `get_cuda_bare_metal_version`、`NinjaBuildExtension`（约 31–72 行）
- CUDA 架构：`supported_archs` 默认 `["80"]`，CUDA ≥11.8 加 `90`，≥12.8 加 `120`；`-gencode arch=compute_X,code=sm_X`（约 100–110 行）
- `CUDAExtension(name="infllm_v2.C", ...)` 与 flash_attn 源列表（约 117–251 行）
- `setup(...)`（253–267 行）

完整逐行内容与上文工具输出一致，篇幅较长此处不重复排版；你可直接打开该文件核对。

---

## 5. `infllm_v2/__init__.py` 全文

```1:12:/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/__init__.py
__version__ = "0.1.0"

from .blockmask_to_uint64 import blockmask_to_uint64
from .topk_to_uint64 import topk_to_uint64
from .uint64_to_bool import uint64_to_bool
from .max_pooling_1d import max_pooling_1d, max_pooling_1d_varlen, max_pooling_1d_varlen_v2
from .infllmv2_sparse_attention import (
    infllmv2_attn_varlen_func,
    infllmv2_attn_stage1,
    infllmv2_attn_with_kvcache,
)
```

---

## 6. `ls` / `strings` 关于 `.so`

- 在当前工作区对 `infllm_v2/C*.so` 的搜索 **未找到** 扩展名为 `.so` 的文件；因此此处无法给出真实的 `ls -la` 或 `strings ... | grep sm_` 结果。
- 已执行的命令在环境中 **没有打印出任何行**（可能对应文件不存在或执行环境未挂载该产物）。

请你在有该 `.so` 的机器上运行：

```bash
ls -la /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so
strings /root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so | grep -E "sm_[0-9]+" | sort -u
```

从 `setup.py` 可知编译时会根据 CUDA 版本加入 **`sm_80`、`sm_90`、`sm_120`**（在 nvcc 满足版本条件时）；`strings` 是否出现这些子串还取决于二进制是否内嵌了相关字面量。
