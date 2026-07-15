> DEVELOPER

在 /user_4813494d/openbmb 项目中调研当前 Marlin NVFP4 kernel 的精度模式。背景：项目使用 SGLang fork + custom sgl-kernel 的 Marlin FP4 路径做 decode。我需要搞清楚：

1. **当前 Marlin 是 NVFP4 A16 还是 A8**？也就是 activation 是 fp16/bf16 还是 fp8/int8。重点查：
   - `demo-sala/sglang/python/sglang/srt/layers/quantization/` 下的 marlin / fp4 相关文件
   - `marlin_utils_fp4.py` 之类
   - `modelopt_quant.py` 里 hybrid Marlin 选择逻辑
   - sgl-kernel Marlin FP4 entry（gemm 函数签名 / dtype 参数）
   - `docs/gemm/marlin.md` 和 `docs/quant/` 里的相关结论
   
2. **是否存在 NVFP4 A8 Marlin kernel 的支持**？查 sgl-kernel 上游、CUTLASS、有没有 a8 variant 的入口或 todo 注释；docs/gemm 里有没有提到 a8 的讨论或 dead-end。

3. **当前 decode shape 下 Marlin 的实测速度** — 看 docs/gemm/sol_table.md / current.md / changelog.md，找最新的 Marlin 在小 M (decode) 的吞吐 vs roof。

请精读上述 docs 和关键代码文件后给我一个 300 字以内的总结：当前模式确认、a8 可行性、目前 marlin 瓶颈数字。不要列文件清单，给结论 + 关键引用（file:line）。

> AGENT

我来系统地调研这个 Marlin NVFP4 kernel 的精度模式问题。

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"*marlin*\" | grep -E \"\\.(py|md)$\" | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/bench_downproj_marlin_vs_cutlass.py
/user_4813494d/openbmb/bench/kernels/marlin_tile_sweep.py
/user_4813494d/openbmb/docs/gemm/marlin.md
/user_4813494d/openbmb/bench/kernels/marlin/bench_marlin_bandwidth.py
/user_4813494d/openbmb/bench/kernels/marlin/bench_marlin_graph_tiles.py
/user_4813494d/openbmb/bench/kernels/marlin/bench_marlin_reduce.py
/user_4813494d/openbmb/bench/kernels/marlin/bench_marlin_tune.py
/user_4813494d/openbmb/bench/kernels/marlin/bench_marlin_vs_cutlass.py
/user_4813494d/openbmb/docs/gemm/.ipynb_checkpoints/marlin-checkpoint.md
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/test/test_marlin_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp8.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/moe/fused_moe_triton/fused_marlin_moe.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/moe/moe_runner/marlin.py
```

> AGENT

现在查看关键文件：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py"
}
```

> TOOL

tool_result Read
```
1	# SPDX-License-Identifier: Apache-2.0
2	# Adapted from https://github.com/sgl-project/sglang/pull/19652
3	
4	"""NVFP4 Marlin fallback: run FP4-quantized models on non-Blackwell GPUs via Marlin kernel."""
5	
6	import logging
7	from typing import Optional
8	
9	import torch
10	
11	from sglang.srt.layers.quantization.marlin_utils import (
12	    USE_FP32_REDUCE_DEFAULT,
13	    marlin_make_workspace,
14	    marlin_permute_bias,
15	    marlin_permute_scales,
16	    should_use_atomic_add_reduce,
17	)
18	from sglang.srt.layers.quantization.utils import get_scalar_types
19	from sglang.srt.utils import get_device_capability, is_blackwell_supported, is_cuda
20	
21	_is_cuda = is_cuda()
22	if _is_cuda:
23	    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
24	
25	ScalarType, scalar_types = get_scalar_types()
26	
27	logger = logging.getLogger(__name__)
28	
29	# NVFP4 always uses group_size=16
30	FP4_MARLIN_GROUP_SIZE = 16
31	
32	
33	def is_fp4_marlin_supported() -> bool:
34	    """当前 GPU 是否支持 FP4 Marlin fallback (CUDA SM >= 75)。"""
35	    if not _is_cuda:
36	        return False
37	    if torch.version.hip is not None:
38	        return False
39	    major, minor = get_device_capability()
40	    if major is None or minor is None:
41	        return False
42	    return (major * 10 + minor) >= 75
43	
44	
45	def should_use_fp4_marlin_fallback() -> bool:
46	    """非 Blackwell（或强制）且 SM >= 75 时返回 True。"""
47	    import os
48	    force = os.environ.get("SGLANG_FORCE_NVFP4_MARLIN", "0") == "1"
49	    return (force or not is_blackwell_supported()) and is_fp4_marlin_supported()
50	
51	
52	def _nvfp4_compute_scale_factor(marlin_scales: torch.Tensor) -> float:
53	    """计算 power-of-2 rescale factor，使得所有非零 weight_scale * 2^7 >= 2。
54	
55	    防 dequant_fp8_scales<nv_bfloat162> BF16 widening underflow（vLLM PR #34577）：
56	    当 weight_scale * 2^7 < 2 时，S0E5M3 表示 MSB=0，BF16 widening 会被错误展开为 ~2^-112
57	    导致下游 dequant 退化。返回 sf >= 1.0 (Python float, power of 2)。
58	    """
59	    ws_float = marlin_scales.float() * (2**7)
60	    nonzero_mask = ws_float > 0
61	    if nonzero_mask.any():
62	        min_val = ws_float[nonzero_mask].min()
63	        if min_val < 2:
64	            sf = (2 / min_val).log2().ceil().exp2()
65	            assert (ws_float[nonzero_mask] * sf <= 448 * (2**7)).all(), (
66	                "NVFP4 scale dynamic range 太大，rescale 会溢出 E4M3 上限"
67	            )
68	            return sf.item()
69	    return 1.0
70	
71	
72	def nvfp4_marlin_process_scales(
73	    marlin_scales: torch.Tensor,
74	    scale_factor: Optional[float] = None,
75	) -> tuple[torch.Tensor, float]:
76	    """将 NVFP4 scales 从 FP8-S1E4M3 转换为 Marlin 所需的 FP8-S0E5M3 格式。
77	
78	    Args:
79	        marlin_scales: 已 marlin permute 的 weight scales。
80	        scale_factor: 可选 power-of-2 rescale factor。None 时自动计算，使得每个非零
81	            scale 满足 ``scale * 2^7 >= 2``（S0E5M3 MSB=1）。Caller 必须把
82	            ``global_scale`` 同步除以返回的 ``scale_factor`` 以保持数学等价。
83	
84	    Returns:
85	        (processed_scales, scale_factor)
86	    """
87	    marlin_scales = marlin_scales.to(torch.half)
88	
89	    if not (marlin_scales >= 0).all():
90	        logger.warning_once(
91	            "NVFP4 Marlin 要求 scales >= 0，但检测到负 scale，精度可能下降。"
92	        )
93	
94	    # 重排列：[0,1,2,3] -> [0,2,1,3]（每组4个，交换1和2）
95	    marlin_scales = marlin_scales.view(-1, 4)[:, [0, 2, 1, 3]].view(
96	        marlin_scales.size(0), -1
97	    )
98	
99	    # Rescale：把所有非零 scale 抬到 weight_scale * 2^7 >= 2，避免 BF16 widening underflow
100	    # （vLLM PR #34577：dequant_fp8_scales<nv_bfloat162> 的 5→8 bit exponent widening bug）
101	    if scale_factor is None:
102	        scale_factor = _nvfp4_compute_scale_factor(marlin_scales)
103	    if scale_factor > 1.0:
104	        marlin_scales = (marlin_scales.float() * scale_factor).to(torch.half)
105	
106	    # 转换 exponent bias：FP16 exponent bias=15，FP8-S0E5M3 bias=16，差值=1
107	    # 乘以 2^7 后以 int16 左移1位，再视作 float8_e4m3fn
108	    marlin_scales = (marlin_scales * (2**7)).view(torch.int16) << 1
109	    marlin_scales = marlin_scales.view(torch.float8_e4m3fn)
110	    marlin_scales = marlin_scales[:, 1::2].contiguous()
111	
112	    return marlin_scales, scale_factor
113	
114	
115	def nvfp4_marlin_process_global_scale(global_scale: torch.Tensor) -> torch.Tensor:
116	    """预调整 global scale 的 exponent bias 供 Marlin kernel 使用。"""
117	    assert global_scale.dtype in [torch.half, torch.bfloat16], (
118	        f"global_scale dtype 必须是 half 或 bfloat16，实际为 {global_scale.dtype}"
119	    )
120	    fp4_exponent = 2
121	    target_exponent = 5 if global_scale.dtype == torch.half else 8
122	    exponent_bias = 2 ** (target_exponent - 1) - 2 ** (fp4_exponent - 1)
123	    return global_scale * (2.0 ** (exponent_bias - 7))
124	
125	
126	def apply_fp4_marlin_linear(
127	    input: torch.Tensor,
128	    weight: torch.Tensor,
129	    weight_scale: torch.Tensor,
130	    weight_global_scale: Optional[torch.Tensor],
131	    workspace: torch.Tensor,
132	    size_n: int,
133	    size_k: int,
134	    bias: Optional[torch.Tensor] = None,
135	    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
136	) -> torch.Tensor:
137	    """通过 Marlin kernel 执行 FP4 量化 linear（非 Blackwell fallback）。"""
138	    reshaped_x = input.reshape(-1, input.shape[-1])
139	    out_shape = input.shape[:-1] + (size_n,)
140	
141	    use_atomic_add = should_use_atomic_add_reduce(
142	        m=reshaped_x.size(0),
143	        n=size_n,
144	        k=size_k,
145	        device=input.device,
146	        dtype=input.dtype,
147	    )
148	
149	    output = gptq_marlin_gemm(
150	        a=reshaped_x,
151	        c=None,
152	        b_q_weight=weight,
153	        b_scales=weight_scale,
154	        global_scale=weight_global_scale.reshape(-1),
155	        b_zeros=None,
156	        g_idx=None,
157	        perm=None,
158	        workspace=workspace,
159	        b_q_type=scalar_types.float4_e2m1f,
160	        size_m=reshaped_x.size(0),
161	        size_n=size_n,
162	        size_k=size_k,
163	        use_atomic_add=use_atomic_add,
164	        use_fp32_reduce=use_fp32_reduce,
165	    )
166	
167	    if bias is not None:
168	        output.add_(bias)
169	
170	    return output.reshape(out_shape)
171	
172	
173	def prepare_fp4_layer_for_marlin(
174	    layer: torch.nn.Module,
175	    weight_attr: str = "weight",
176	    weight_scale_attr: str = "weight_scale",
177	    weight_global_scale_attr: str = "weight_global_scale",
178	) -> None:
179	    """将 NVFP4 linear 层权重原地重打包为 Marlin 格式。"""
180	    logger.warning_once(
181	        "当前 GPU 不原生支持 FP4 计算，使用 Marlin kernel 做 FP4 weight-only 推理。"
182	    )
183	
184	    part_size_n = layer.output_size_per_partition
185	    part_size_k = layer.input_size_per_partition
186	    param_dtype = layer.params_dtype
187	
188	    weight = getattr(layer, weight_attr)
189	    assert weight.shape == (part_size_n, part_size_k // 2), (
190	        f"期望 {weight_attr} shape ({part_size_n}, {part_size_k // 2})，"
191	        f"实际 {weight.shape}"
192	    )
193	
194	    device = weight.device
195	    layer.marlin_workspace = marlin_make_workspace(device)
196	
197	    # 权重重打包：NVFP4 原始布局 → Marlin tile 布局
198	    perm = torch.empty(0, dtype=torch.int, device=device)
199	    qweight = weight.data.view(torch.int32).T.contiguous()
200	    del weight
201	    marlin_qweight = gptq_marlin_repack(
202	        b_q_weight=qweight,
203	        perm=perm,
204	        size_k=part_size_k,
205	        size_n=part_size_n,
206	        num_bits=4,
207	    )
208	    del qweight
209	    setattr(layer, weight_attr, torch.nn.Parameter(marlin_qweight, requires_grad=False))
210	
211	    # scale 转换：转置 → permute → FP8-S0E5M3
212	    weight_scale = getattr(layer, weight_scale_attr)
213	    weight_scale = weight_scale.data.T.contiguous().to(param_dtype)
214	    weight_scale = marlin_permute_scales(
215	        s=weight_scale,
216	        size_k=part_size_k,
217	        size_n=part_size_n,
218	        group_size=FP4_MARLIN_GROUP_SIZE,
219	    )
220	    weight_scale, scale_factor = nvfp4_marlin_process_scales(weight_scale)
221	    setattr(layer, weight_scale_attr, torch.nn.Parameter(weight_scale, requires_grad=False))
222	
223	    # global scale：调整 exponent bias，并补偿 process_scales 的 rescale
224	    weight_global_scale = getattr(layer, weight_global_scale_attr)
225	    weight_global_scale = weight_global_scale.to(param_dtype)
226	    weight_global_scale = nvfp4_marlin_process_global_scale(weight_global_scale)
227	    weight_global_scale = weight_global_scale / scale_factor
228	    setattr(layer, weight_global_scale_attr, torch.nn.Parameter(weight_global_scale, requires_grad=False))
229	
230	    # bias（如有）
231	    if hasattr(layer, "bias") and layer.bias is not None:
232	        assert layer.bias.shape == (part_size_n,)
233	        layer.bias = torch.nn.Parameter(marlin_permute_bias(layer.bias), requires_grad=False)
234	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils.py"
}
```

> TOOL

tool_result Read
```
1	# SPDX-License-Identifier: Apache-2.0
2	# Adapted from https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/quantization/utils/marlin_utils.py
3	
4	from __future__ import annotations
5	
6	import logging
7	import os
8	from dataclasses import dataclass
9	from typing import TYPE_CHECKING, Any, Optional
10	
11	import numpy
12	import torch
13	
14	from sglang.srt.layers.parameter import (
15	    BasevLLMParameter,
16	    ChannelQuantScaleParameter,
17	    GroupQuantScaleParameter,
18	    PackedvLLMParameter,
19	)
20	from sglang.srt.layers.quantization.base_config import (
21	    LinearMethodBase,
22	    QuantizationConfig,
23	)
24	from sglang.srt.layers.quantization.utils import (
25	    get_scalar_types,
26	    pack_cols,
27	    unpack_cols,
28	)
29	from sglang.srt.utils import get_device_capability, is_cuda
30	from sglang.srt.utils.custom_op import register_custom_op
31	
32	if TYPE_CHECKING:
33	    from sglang.srt.layers.linear import LinearBase
34	    from sglang.srt.layers.moe.fused_moe_triton.layer import FusedMoE
35	
36	from sglang.srt.compilation.piecewise_context_manager import get_forward_context
37	
38	try:
39	    from vllm import _custom_ops as ops
40	except ImportError:
41	    ops = None
42	
43	
44	_is_cuda = is_cuda()
45	
46	if _is_cuda:
47	    from sgl_kernel import gptq_marlin_gemm
48	
49	logger = logging.getLogger(__name__)
50	
51	ScalarType, scalar_types = get_scalar_types()
52	
53	GPTQ_MARLIN_TILE = 16
54	GPTQ_MARLIN_MIN_THREAD_N = 64
55	GPTQ_MARLIN_MIN_THREAD_K = 128
56	GPTQ_MARLIN_MAX_PARALLEL = 16
57	
58	MARLIN_SUPPORTED_GROUP_SIZES = [-1, 32, 64, 128]
59	
60	# In case there is a performance issue with Marlin, the variable below can be
61	# changed to False, which allows Marlin to perform global reductions in fp16
62	# precision (instead of fp32), and therefore, save on some memory movements.
63	# Override via env: SGLANG_MARLIN_USE_FP32_REDUCE=0|1 (default 1 = upstream behavior).
64	USE_FP32_REDUCE_DEFAULT = (
65	    os.environ.get("SGLANG_MARLIN_USE_FP32_REDUCE", "1") not in ("0", "false", "False")
66	)
67	
68	
69	@dataclass
70	class MarlinLinearLayerConfig:
71	    full_weight_shape: tuple[int, int]  # [in, out]
72	    partition_weight_shape: tuple[int, int]
73	    weight_type: ScalarType
74	    act_type: torch.dtype
75	    group_size: int
76	    zero_points: bool
77	    has_g_idx: bool
78	
79	
80	# For binary size and compile time, we don't support the same types for with and
81	#  without runtime zero-point. We support common cases, i.e. AWQ and GPTQ.
82	#  TODO: we may want to move this into the C++ so its closer to the actual impl
83	def query_marlin_supported_quant_types(
84	    has_zp: Optional[bool] = None,
85	    include_fp_type: bool = True,
86	    device_capability: Optional[int] = None,
87	):
88	    if device_capability is None:
89	        major, minor = get_device_capability()
90	        capability = major * 10 + minor
91	        device_capability = -1 if capability is None else capability
92	
93	    if device_capability < 80:
94	        return []
95	
96	    # - has_zp is True: return quant_types that has zero points
97	    # - has_zp is False: return quant_types that has not zero points
98	    # - has_zp is None: both
99	    if has_zp is None:
100	        types0 = query_marlin_supported_quant_types(
101	            False, include_fp_type, device_capability
102	        )
103	        types1 = query_marlin_supported_quant_types(
104	            True, include_fp_type, device_capability
105	        )
106	        return types0 + types1
107	
108	    if has_zp:
109	        # AWQ style, unsigned + runtime zero-point
110	        return [scalar_types.uint4]
111	    else:
112	        # GPTQ style, unsigned + symmetric bias
113	        res = [scalar_types.uint4b8, scalar_types.uint8b128]
114	        if include_fp_type:
115	            res += [scalar_types.float8_e4m3fn, scalar_types.float4_e2m1f]
116	        return res
117	
118	
119	def _check_marlin_supported(
120	    quant_type: ScalarType,
121	    group_size: Optional[int],
122	    has_zp: bool,
123	    device_capability: Optional[int] = None,
124	) -> tuple[bool, Optional[str]]:
125	
126	    if device_capability is None:
127	        major, minor = get_device_capability()
128	        capability = major * 10 + minor
129	        device_capability = -1 if capability is None else capability
130	
131	    supported_types = query_marlin_supported_quant_types(
132	        has_zp, True, device_capability
133	    )
134	
135	    if quant_type not in supported_types:
136	        return (
137	            False,
138	            f"Marlin does not support weight_bits = {quant_type}. "
139	            f"Only types = {supported_types} "
140	            f"are supported (for group_size = {group_size}, "
141	            f"device_capability = {device_capability}, zp = {has_zp}).",
142	        )
143	    if group_size is None or group_size not in MARLIN_SUPPORTED_GROUP_SIZES:
144	        return (
145	            False,
146	            f"Marlin does not support group_size = {group_size}. "
147	            f"Only group_sizes = {MARLIN_SUPPORTED_GROUP_SIZES} "
148	            "are supported.",
149	        )
150	
151	    return True, None
152	
153	
154	def check_marlin_supported(
155	    quant_type: ScalarType,
156	    group_size: int,
157	    has_zp: bool = False,
158	    device_capability: Optional[int] = None,
159	) -> bool:
160	    cond, _ = _check_marlin_supported(quant_type, group_size, has_zp, device_capability)
161	    return cond
162	
163	
164	def verify_marlin_supported(
165	    quant_type: ScalarType, group_size: int, has_zp: bool = False
166	) -> None:
167	    cond, err_msg = _check_marlin_supported(quant_type, group_size, has_zp)
168	    if not cond:
169	        assert err_msg is not None
170	        raise ValueError(err_msg)
171	
172	
173	def verify_marlin_supports_shape(
174	    output_size_per_partition: int,
175	    input_size_per_partition: int,
176	    input_size: int,
177	    group_size: int,
178	) -> None:
179	
180	    # Validate output_size_per_partition
181	    if output_size_per_partition % GPTQ_MARLIN_MIN_THREAD_N != 0:
182	        raise ValueError(
183	            f"Weight output_size_per_partition = "
184	            f"{output_size_per_partition} is not divisible by "
185	            f" min_thread_n = {GPTQ_MARLIN_MIN_THREAD_N}. "
186	            "Consider reducing tensor_parallel_size or running "
187	            "with --quantization gptq."
188	        )
189	
190	    # Validate input_size_per_partition
191	    if input_size_per_partition % GPTQ_MARLIN_MIN_THREAD_K != 0:
192	        raise ValueError(
193	            f"Weight input_size_per_partition = "
194	            f"{input_size_per_partition} is not divisible "
195	            f"by min_thread_k = {GPTQ_MARLIN_MIN_THREAD_K}. "
196	            "Consider reducing tensor_parallel_size or running "
197	            "with --quantization gptq."
198	        )
199	
200	    if group_size < input_size and input_size_per_partition % group_size != 0:
201	        raise ValueError(
202	            f"Weight input_size_per_partition = {input_size_per_partition}"
203	            f" is not divisible by group_size = {group_size}. "
204	            "Consider reducing tensor_parallel_size or running "
205	            "with --quantization gptq."
206	        )
207	
208	
209	def check_marlin_supports_shape(
210	    output_size_per_partition: int,
211	    input_size_per_partition: int,
212	    input_size: int,
213	    group_size: int,
214	) -> tuple[bool, Optional[str]]:
215	    try:
216	        verify_marlin_supports_shape(
217	            output_size_per_partition, input_size_per_partition, input_size, group_size
218	        )
219	    except ValueError as e:
220	        return False, e.__str__()
221	    return True, None
222	
223	
224	def check_marlin_supports_layer(layer: LinearBase, group_size: int) -> bool:
225	    output_size_per_partition = (
226	        getattr(layer, "output_size_per_partition", None) or layer.output_size
227	    )
228	    input_size_per_partition = (
229	        getattr(layer, "input_size_per_partition", None) or layer.input_size
230	    )
231	
232	    return check_marlin_supports_shape(
233	        output_size_per_partition=output_size_per_partition,
234	        input_size_per_partition=input_size_per_partition,
235	        input_size=layer.input_size,
236	        group_size=group_size,
237	    )[0]
238	
239	
240	def check_moe_marlin_supports_layer(layer: FusedMoE, group_size: int) -> bool:
241	    hidden_size = layer.hidden_size
242	    intermediate_size_per_partition = layer.intermediate_size_per_partition
243	    # apply_router_weight_on_input is not supported for moe marlin
244	    supports_router_weight = not layer.moe_runner_config.apply_router_weight_on_input
245	    # moe marlin requires the activation to be silu
246	    supports_activation = layer.moe_runner_config.activation == "silu"
247	
248	    # gate-up: (n, k) = (intermediate_size_per_partition * 2, hidden_size)
249	    # down: (n, k) = (hidden_size, intermediate_size_per_partition)
250	    # moe marlin requires n % 128 == 0 and k % 64 == 0
251	    supports_shape = (
252	        hidden_size % 128 == 0
253	        and intermediate_size_per_partition % max(64, group_size) == 0
254	    )
255	    supports_group_size = group_size in [-1, 32, 64, 128]
256	    return (
257	        supports_shape
258	        and supports_group_size
259	        and supports_router_weight
260	        and supports_activation
261	    )
262	
263	
264	def marlin_make_workspace(
265	    device: torch.device, max_blocks_per_sm: int = 1
266	) -> torch.Tensor:
267	    # In the new marlin kernel, we use the num of threadblocks as workspace
268	    # size. The num of threadblocks is is sms_count * max_blocks_per_sm.
269	    sms = torch.cuda.get_device_properties(device).multi_processor_count
270	    return torch.zeros(
271	        sms * max_blocks_per_sm, dtype=torch.int, device=device, requires_grad=False
272	    )
273	
274	
275	def marlin_is_k_full(act_order: bool, is_row_parallel: bool) -> bool:
276	    return (not act_order) or (act_order and not is_row_parallel)
277	
278	
279	def marlin_repeat_scales_on_all_ranks(
280	    act_order: bool, group_size: int, is_row_parallel: bool
281	) -> bool:
282	    # Need to repeat scales on every rank if act_ordering or
283	    # channelwise and RowParallelLinear
284	    is_channelwise = group_size == -1
285	    return act_order or (is_channelwise and is_row_parallel)
286	
287	
288	def marlin_make_empty_g_idx(device: torch.device) -> torch.Tensor:
289	    return torch.nn.Parameter(
290	        torch.empty(0, dtype=torch.int, device=device), requires_grad=False
291	    )
292	
293	
294	def marlin_make_empty_zp(device: torch.device) -> torch.Tensor:
295	    return torch.nn.Parameter(
296	        torch.empty(0, dtype=torch.int, device=device), requires_grad=False
297	    )
298	
299	
300	def marlin_sort_g_idx(g_idx: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
301	    g_idx_sort_indices = torch.argsort(g_idx).to(torch.int)
302	    return g_idx[g_idx_sort_indices], g_idx_sort_indices
303	
304	
305	def get_scale_perms():
306	    scale_perm: list[int] = []
307	    for i in range(8):
308	        scale_perm.extend([i + 8 * j for j in range(8)])
309	    scale_perm_single: list[int] = []
310	    for i in range(4):
311	        scale_perm_single.extend([2 * i + j for j in [0, 1, 8, 9, 16, 17, 24, 25]])
312	    return scale_perm, scale_perm_single
313	
314	
315	def marlin_permute_scales(
316	    s: torch.Tensor, size_k: int, size_n: int, group_size: int
317	) -> torch.Tensor:
318	
319	    scale_perm, scale_perm_single = get_scale_perms()
320	    if group_size < size_k and group_size != -1:
321	        s = s.reshape((-1, len(scale_perm)))[:, scale_perm]
322	    else:
323	        s = s.reshape((-1, len(scale_perm_single)))[:, scale_perm_single]
324	    s = s.reshape((-1, size_n)).contiguous()
325	
326	    return s
327	
328	
329	def marlin_permute_bias(s: torch.Tensor) -> torch.Tensor:
330	    origin_shape = s.shape
331	    _, scale_perm_single = get_scale_perms()
332	    s = s.reshape((-1, len(scale_perm_single)))[:, scale_perm_single]
333	    return s.reshape(*origin_shape).contiguous()
334	
335	
336	def marlin_moe_permute_scales(
337	    s: torch.Tensor,
338	    size_k: int,
339	    size_n: int,
340	    group_size: int,
341	):
342	    num_experts = s.shape[0]
343	    output = torch.empty(
344	        (num_experts, s.shape[1], s.shape[2]),
345	        device=s.device,
346	        dtype=s.dtype,
347	    )
348	
349	    for e in range(num_experts):
350	        output[e] = marlin_permute_scales(s[e], size_k, size_n, group_size)
351	    return output
352	
353	
354	def marlin_zero_points(
355	    zp: torch.Tensor, size_k: int, size_n: int, num_bits: int
356	) -> torch.Tensor:
357	    # Permute zero-points in a similar way to scales, but do not use the
358	    # "single" permutation, since zero-points are applied on every MMA
359	    scale_perm, _ = get_scale_perms()
360	    zp = zp.reshape((-1, len(scale_perm)))[:, scale_perm]
361	
362	    # Interleave column dim (for the dequantize code) and pack it to int32
363	    if num_bits == 4:
364	        interleave = numpy.array([0, 2, 4, 6, 1, 3, 5, 7])
365	    elif num_bits == 8:
366	        interleave = numpy.array([0, 2, 1, 3])
367	    else:
368	        raise Exception("num_bits must be 4 or 8, got {}".format(num_bits))
369	
370	    zp = zp.reshape((-1, len(interleave)))[:, interleave].ravel()
371	    zp = zp.reshape((-1, size_n)).contiguous()
372	    zp = pack_cols(zp, num_bits, size_k, size_n)
373	
374	    return zp
375	
376	
377	def awq_to_marlin_zero_points(
378	    q_zp_packed: torch.Tensor, size_k: int, size_n: int, num_bits: int
379	) -> torch.Tensor:
380	    # AWQ zero-points are quantized and packed on the column dim.
381	    # In addition, the values are permuted based on dequantizer.
382	    # Here we undo both of these, and then apply marlin permutation
383	    # and pack it back.
384	    q_zp = unpack_cols(q_zp_packed, num_bits, size_k, size_n)
385	
386	    # Undo interleaving (use argsort(..) to get inverse perm)
387	    if num_bits == 4:
388	        undo_interleave = numpy.argsort(numpy.array([0, 2, 4, 6, 1, 3, 5, 7]))
389	    elif num_bits == 8:
390	        undo_interleave = numpy.argsort(numpy.array([0, 2, 1, 3]))
391	    else:
392	        raise Exception("num_bits must be 4 or 8, got {}".format(num_bits))
393	
394	    q_zp = q_zp.reshape((-1, len(undo_interleave)))[:, undo_interleave].ravel()
395	    q_zp = q_zp.reshape((-1, size_n)).contiguous()
396	
397	    marlin_zp = marlin_zero_points(q_zp, size_k, size_n, num_bits)
398	    return marlin_zp
399	
400	
401	def moe_awq_to_marlin_zero_points(
402	    q_zp_packed: torch.Tensor, size_k: int, size_n: int, num_bits: int
403	):
404	    num_experts = q_zp_packed.shape[0]
405	    output = torch.empty(
406	        (num_experts, q_zp_packed.shape[1], q_zp_packed.shape[2]),
407	        device=q_zp_packed.device,
408	        dtype=q_zp_packed.dtype,
409	    )
410	    for e in range(num_experts):
411	        output[e] = awq_to_marlin_zero_points(q_zp_packed[e], size_k, size_n, num_bits)
412	    return output
413	
414	
415	def maybe_warn_marlin_atomic_add(device, dtype):
416	    if torch.compiler.is_dynamo_compiling():
417	        return
418	    device_capability = torch.cuda.get_device_capability(device)
419	    if device_capability[0] < 9 and dtype == torch.bfloat16:
420	        logger.info_once(
421	            "You are running Marlin kernel with bf16 on GPUs before SM90. "
422	            "You can consider change to fp16 to achieve better performance "
423	            "if possible."
424	        )
425	
426	
427	def maybe_warn_marlin_atomic_add_env():
428	    if torch.compiler.is_dynamo_compiling():
429	        return
430	    # TODO(yiyun): Need to add sglang's MARLIN_USE_ATOMIC_ADD: bool = False
431	    if True:
432	        return
433	    # if envs.VLLM_MARLIN_USE_ATOMIC_ADD:
434	    #     return
435	    logger.info_once(
436	        "Marlin kernel can achieve better performance for small size_n "
437	        "with experimental use_atomic_add feature. "
438	        "You can consider set environment variable "
439	        "VLLM_MARLIN_USE_ATOMIC_ADD to 1 if possible."
440	    )
441	
442	
443	def should_use_atomic_add_reduce(
444	    m: int, n: int, k: int, device: torch.device, dtype: torch.dtype
445	) -> bool:
446	
447	    # the performance of atomicAdd is better than global reduce
448	    # only when m*n is small and k is large
449	    if n >= 2048 or k < 2048 or device.type != "cuda":
450	        return False
451	
452	    # disable atomicAdd reduce by default,
453	    # one can enable it with VLLM_MARLIN_USE_ATOMIC_ADD=1
454	    # TODO: Need to add sglang's MARLIN_USE_ATOMIC_ADD: bool = False
455	    if not True:
456	        maybe_warn_marlin_atomic_add_env()
457	        return False
458	
459	    # sm8x doesn't support atomicAdd + bfloat16 natively
460	    device_capability = torch.cuda.get_device_capability(device)
461	    if device_capability[0] < 9 and dtype == torch.bfloat16:
462	        maybe_warn_marlin_atomic_add(device, dtype)
463	        return False
464	
465	    return True
466	
467	
468	def apply_gptq_marlin_linear(
469	    input: torch.Tensor,
470	    weight: torch.Tensor,
471	    weight_scale: torch.Tensor,
472	    weight_zp: torch.Tensor,
473	    g_idx: torch.Tensor,
474	    g_idx_sort_indices: torch.Tensor,
475	    workspace: torch.Tensor,
476	    wtype: ScalarType,
477	    output_size_per_partition: int,
478	    input_size_per_partition: int,
479	    is_k_full: bool,
480	    bias: Optional[torch.Tensor] = None,
481	    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
482	) -> torch.Tensor:
483	    reshaped_x = input.reshape(-1, input.shape[-1])
484	    out_shape = input.shape[:-1] + (output_size_per_partition,)
485	
486	    use_atomic_add = should_use_atomic_add_reduce(
487	        m=reshaped_x.size(0),
488	        n=output_size_per_partition,
489	        k=reshaped_x.size(1),
490	        device=input.device,
491	        dtype=input.dtype,
492	    )
493	
494	    forward_context = get_forward_context()
495	    if forward_context is None:
496	        output = gptq_marlin_gemm(
497	            reshaped_x,
498	            None,
499	            weight,
500	            weight_scale,
501	            None,
502	            weight_zp,
503	            g_idx,
504	            g_idx_sort_indices,
505	            workspace,
506	            wtype,
507	            size_m=reshaped_x.shape[0],
508	            size_n=output_size_per_partition,
509	            size_k=input_size_per_partition,
510	            is_k_full=is_k_full,
511	            use_atomic_add=use_atomic_add,
512	            use_fp32_reduce=use_fp32_reduce,
513	            is_zp_float=False,
514	        )
515	    else:
516	        output = unified_apply_gptq_marlin_gemm_with_wtype(
517	            input=reshaped_x,
518	            weight=weight,
519	            weight_scale=weight_scale,
520	            weight_zp=weight_zp,
521	            g_idx=g_idx,
522	            g_idx_sort_indices=g_idx_sort_indices,
523	            workspace=workspace,
524	            wtype_id=wtype.id,
525	            output_size_per_partition=output_size_per_partition,
526	            input_size_per_partition=input_size_per_partition,
527	            is_k_full=is_k_full,
528	            use_atomic_add=use_atomic_add,
529	            use_fp32_reduce=use_fp32_reduce,
530	            is_zp_float=False,
531	        )
532	
533	    if bias is not None:
534	        output.add_(bias)  # In-place add
535	
536	    return output.reshape(out_shape)
537	
538	
539	def apply_awq_marlin_linear(
540	    input: torch.Tensor,
541	    weight: torch.Tensor,
542	    weight_scale: torch.Tensor,
543	    weight_zp: torch.Tensor,
544	    g_idx: torch.Tensor,
545	    g_idx_sort_indices: torch.Tensor,
546	    workspace: torch.Tensor,
547	    quant_type: ScalarType,
548	    output_size_per_partition: int,
549	    input_size_per_partition: int,
550	    bias: Optional[torch.Tensor] = None,
551	    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
552	) -> torch.Tensor:
553	    reshaped_x = input.reshape(-1, input.shape[-1])
554	    out_shape = input.shape[:-1] + (output_size_per_partition,)
555	
556	    use_atomic_add = should_use_atomic_add_reduce(
557	        m=reshaped_x.size(0),
558	        n=output_size_per_partition,
559	        k=reshaped_x.size(1),
560	        device=input.device,
561	        dtype=input.dtype,
562	    )
563	
564	    forward_context = get_forward_context()
565	    if forward_context is None:
566	        output = gptq_marlin_gemm(
567	            reshaped_x,
568	            None,
569	            weight,
570	            weight_scale,
571	            None,
572	            weight_zp,
573	            g_idx,
574	            g_idx_sort_indices,
575	            workspace,
576	            quant_type,
577	            size_m=reshaped_x.shape[0],
578	            size_n=output_size_per_partition,
579	            size_k=input_size_per_partition,
580	            use_atomic_add=use_atomic_add,
581	            use_fp32_reduce=use_fp32_reduce,
582	            is_zp_float=False,
583	        )
584	    else:
585	        output = unified_apply_gptq_marlin_gemm(
586	            input=reshaped_x,
587	            weight=weight,
588	            weight_scale=weight_scale,
589	            weight_zp=weight_zp,
590	            g_idx=g_idx,
591	            g_idx_sort_indices=g_idx_sort_indices,
592	            workspace=workspace,
593	            output_size_per_partition=output_size_per_partition,
594	            input_size_per_partition=input_size_per_partition,
595	            use_atomic_add=use_atomic_add,
596	            use_fp32_reduce=use_fp32_reduce,
597	            is_zp_float=False,
598	        )
599	
600	    if bias is not None:
601	        output.add_(bias)  # In-place add
602	
603	    return output.reshape(out_shape)
604	
605	
606	class MarlinConfig(QuantizationConfig):
607	    """Config class for Marlin.
608	
609	    Reference: https://github.com/IST-DASLab/marlin/tree/master
610	    """
611	
612	    def __init__(
613	        self,
614	        group_size: int,
615	        lm_head_quantized: bool,
616	    ) -> None:
617	        super().__init__()
618	
619	        # Group size for the quantization.
620	        self.group_size = group_size
621	        self.lm_head_quantized = lm_head_quantized
622	        if self.group_size != 128 and self.group_size != -1:
623	            raise ValueError(
624	                "Currently, only group size 128 and -1 (channelwise) "
625	                "is supported for Marlin, but got group_size of "
626	                f"{self.group_size}"
627	            )
628	
629	        # 4 Bits packed into 32 bit datatype.
630	        self.pack_factor = 32 // 4
631	
632	        # Tile size used by marlin kernels.
633	        self.tile_size = 16
634	
635	        # Min out_features dim
636	        self.min_n_threads = 64
637	
638	        # Min in_features dim
639	        self.min_k_threads = 128
640	
641	        # Max parallel problems to solve at once (improves large
642	        # batch performance)
643	        self.max_parallel = 16
644	
645	        # Permutation length used by the marlin kernels.
646	        self.perm_len = 1024
647	
648	    def __repr__(self) -> str:
649	        return (
650	            f"MarlinConfig(group_size={self.group_size}, "
651	            f"lm_head_quantized={self.lm_head_quantized})"
652	        )
653	
654	    @classmethod
655	    def get_name(cls) -> str:
656	        return "marlin"
657	
658	    @classmethod
659	    def get_supported_act_dtypes(cls) -> list[torch.dtype]:
660	        return [torch.half]
661	
662	    @classmethod
663	    # Need to figure it out
664	    def get_min_capability(cls) -> int:
665	        return 80
666	
667	    @classmethod
668	    def get_config_filenames(cls) -> list[str]:
669	        return ["quantize_config.json"]
670	
671	    @classmethod
672	    def from_config(cls, config: dict[str, Any]) -> "MarlinConfig":
673	        group_size = cls.get_from_keys(config, ["group_size"])
674	        lm_head_quantized = cls.get_from_keys_or(config, ["lm_head"], default=False)
675	        return cls(group_size, lm_head_quantized)
676	
677	    @classmethod
678	    def override_quantization_method(cls, hf_quant_cfg, user_quant) -> Optional[str]:
679	        # compat: autogptq >=0.8.0 use checkpoint_format: str
680	        # compat: autogptq <=0.7.1 is_marlin_format: bool
681	        is_marlin_format = hf_quant_cfg.get(
682	            "checkpoint_format"
683	        ) == "marlin" or hf_quant_cfg.get("is_marlin_format", False)
684	
685	        is_valid_user_quant = (
686	            user_quant is None or user_quant == "gptq" or user_quant == "marlin"
687	        )
688	
689	        if is_marlin_format and is_valid_user_quant:
690	            msg = "The model is serialized in {} format. Using {} kernel.".format(
691	                cls.get_name(), cls.get_name()
692	            )
693	            logger.info(msg)
694	            return cls.get_name()
695	
696	        return None
697	
698	    def get_quant_method(
699	        self, layer: torch.nn.Module, prefix: str
700	    ) -> Optional[MarlinLinearMethod]:
701	        from sglang.srt.layers.linear import LinearBase
702	        from sglang.srt.layers.vocab_parallel_embedding import ParallelLMHead
703	
704	        if isinstance(layer, LinearBase) or (
705	            isinstance(layer, ParallelLMHead) and self.lm_head_quantized
706	        ):
707	            return MarlinLinearMethod(self)
708	        return None
709	
710	
711	class MarlinLinearMethod(LinearMethodBase):
712	    """Linear method for Marlin.
713	
714	    Args:
715	        quant_config: The Marlin quantization config.
716	    """
717	
718	    def __init__(self, quant_config: MarlinConfig):
719	        self.quant_config = quant_config
720	
721	    def create_weights(
722	        self,
723	        layer: torch.nn.Module,
724	        input_size_per_partition: int,
725	        output_partition_sizes: list[int],
726	        input_size: int,
727	        output_size: int,
728	        params_dtype: torch.dtype,
729	        **extra_weight_attrs,
730	    ):
731	        del output_size  # Unused.
732	        weight_loader = extra_weight_attrs["weight_loader"]
733	
734	        if params_dtype != torch.float16:
735	            raise ValueError(
736	                f"The params dtype must be float16, but got {params_dtype}"
737	            )
738	
739	        # Validate output_size_per_partition
740	        output_size_per_partition = sum(output_partition_sizes)
741	        if output_size_per_partition % self.quant_config.min_n_threads != 0:
742	            raise ValueError(
743	                f"Weight output_size_per_partition = "
744	                f"{output_size_per_partition} is not divisible by "
745	                f"min_n_threads = {self.quant_config.min_n_threads}."
746	            )
747	        if output_size_per_partition % self.quant_config.pack_factor != 0:
748	            raise ValueError(
749	                f"Weight output_size_per_partition = "
750	                f"{output_size_per_partition} is not divisible by "
751	                f"pack_factor = {self.quant_config.pack_factor}."
752	            )
753	
754	        # Validate input_size_per_partition
755	        if input_size_per_partition % self.quant_config.min_k_threads != 0:
756	            raise ValueError(
757	                f"Weight input_size_per_partition = "
758	                f"{input_size_per_partition} is not divisible by "
759	                f"min_k_threads = {self.quant_config.min_k_threads}."
760	            )
761	        if (
762	            self.quant_config.group_size != -1
763	            and input_size_per_partition % self.quant_config.group_size != 0
764	        ):
765	            raise ValueError(
766	                f"Weight input_size_per_partition = "
767	                f"{input_size_per_partition} is not divisible by "
768	                f"group_size = {self.quant_config.group_size}."
769	            )
770	
771	        # Check that we have at least 4 tiles horizontally in the shard
772	        num_tiles_per_perm = self.quant_config.perm_len // (
773	            self.quant_config.tile_size**2
774	        )
775	        if output_size_per_partition % num_tiles_per_perm != 0:
776	            raise ValueError("Each permutation group must reside on the same gpu")
777	
778	        # Quantized 4Bit weights packed into Int32.
779	        qweight = PackedvLLMParameter(
780	            data=torch.empty(
781	                input_size_per_partition // self.quant_config.tile_size,
782	                output_size_per_partition
783	                * self.quant_config.tile_size
784	                // self.quant_config.pack_factor,
785	                device="cuda",
786	                dtype=torch.int32,
787	            ),
788	            input_dim=0,
789	            output_dim=1,
790	            packed_dim=1,
791	            packed_factor=self.quant_config.pack_factor,
792	            marlin_tile_size=self.quant_config.tile_size,
793	            weight_loader=weight_loader,
794	        )
795	
796	        # Determine if channelwise or not
797	        input_groups = (
798	            1
799	            if self.quant_config.group_size == -1
800	            else input_size_per_partition // self.quant_config.group_size
801	        )
802	
803	        weight_scale_args = {
804	            "data": torch.empty(
805	                input_groups,
806	                output_size_per_partition,
807	                device="cuda",
808	                dtype=params_dtype,
809	            ),
810	            "weight_loader": weight_loader,
811	        }
812	        if input_groups == 1:
813	            scales = ChannelQuantScaleParameter(output_dim=1, **weight_scale_args)
814	        else:
815	            scales = GroupQuantScaleParameter(
816	                output_dim=1, input_dim=0, **weight_scale_args
817	            )
818	
819	        # Allocate workspace (Used for internal locking mechanism)
820	        max_workspace_size = (
821	            output_size_per_partition // self.quant_config.min_n_threads
822	        ) * self.quant_config.max_parallel
823	
824	        workspace = BasevLLMParameter(
825	            data=torch.zeros(max_workspace_size, device="cuda", dtype=torch.int),
826	            weight_loader=weight_loader,
827	        )
828	
829	        layer.register_parameter("B", qweight)
830	        layer.register_parameter("s", scales)
831	        layer.register_parameter("workspace", workspace)
832	
833	    def process_weights_after_loading(self, layer: torch.nn.Module) -> None:
834	        # required by torch.compile
835	        layer.B = torch.nn.Parameter(layer.B.data, requires_grad=False)
836	        layer.s = torch.nn.Parameter(layer.s.data, requires_grad=False)
837	        layer.workspace = torch.nn.Parameter(layer.workspace.data, requires_grad=False)
838	
839	    def apply(
840	        self,
841	        layer: torch.nn.Module,
842	        x: torch.Tensor,
843	        bias: Optional[torch.Tensor] = None,
844	    ) -> torch.Tensor:
845	        qweight = layer.B
846	        scales = layer.s
847	        workspace = layer.workspace
848	
849	        x_2d = x.view(-1, x.shape[-1])
850	
851	        size_m = x_2d.shape[0]
852	        size_k = x_2d.shape[1]
853	        size_n = scales.shape[1]
854	
855	        output_2d = ops.marlin_gemm(
856	            x_2d, qweight, scales, workspace, size_m, size_n, size_k
857	        )
858	
859	        output = output_2d.view(x.shape[:-1] + (output_2d.shape[1],))
860	
861	        if bias is not None:
862	            output.add_(bias)  # In-place add
863	
864	        return output
865	
866	
867	def fake_unified_apply_gptq_marlin_gemm(
868	    input: torch.Tensor,
869	    weight: torch.Tensor,
870	    weight_scale: torch.Tensor,
871	    weight_zp: torch.Tensor,
872	    g_idx: torch.Tensor,
873	    g_idx_sort_indices: torch.Tensor,
874	    workspace: torch.Tensor,
875	    output_size_per_partition: int,
876	    input_size_per_partition: int,
877	    use_atomic_add: bool,
878	    use_fp32_reduce: bool,
879	    is_zp_float: bool,
880	) -> torch.Tensor:
881	    return input.new_empty(
882	        (input.shape[0], output_size_per_partition), dtype=input.dtype
883	    )
884	
885	
886	@register_custom_op(fake_impl=fake_unified_apply_gptq_marlin_gemm)
887	def unified_apply_gptq_marlin_gemm(
888	    input: torch.Tensor,
889	    weight: torch.Tensor,
890	    weight_scale: torch.Tensor,
891	    weight_zp: torch.Tensor,
892	    g_idx: torch.Tensor,
893	    g_idx_sort_indices: torch.Tensor,
894	    workspace: torch.Tensor,
895	    output_size_per_partition: int,
896	    input_size_per_partition: int,
897	    use_atomic_add: bool,
898	    use_fp32_reduce: bool,
899	    is_zp_float: bool,
900	) -> torch.Tensor:
901	    quant_config = get_forward_context().quant_config
902	    quant_type = quant_config.quant_type
903	    return gptq_marlin_gemm(
904	        input,
905	        None,
906	        weight,
907	        weight_scale,
908	        None,
909	        weight_zp,
910	        g_idx,
911	        g_idx_sort_indices,
912	        workspace,
913	        quant_type,
914	        size_m=input.shape[0],
915	        size_n=output_size_per_partition,
916	        size_k=input_size_per_partition,
917	        use_atomic_add=use_atomic_add,
918	        use_fp32_reduce=use_fp32_reduce,
919	        is_zp_float=is_zp_float,
920	    )
921	
922	
923	def fake_unified_apply_gptq_marlin_gemm_with_wtype(
924	    input: torch.Tensor,
925	    weight: torch.Tensor,
926	    weight_scale: torch.Tensor,
927	    weight_zp: torch.Tensor,
928	    g_idx: torch.Tensor,
929	    g_idx_sort_indices: torch.Tensor,
930	    workspace: torch.Tensor,
931	    wtype_id: int,
932	    output_size_per_partition: int,
933	    input_size_per_partition: int,
934	    is_k_full: bool,
935	    use_atomic_add: bool,
936	    use_fp32_reduce: bool,
937	    is_zp_float: bool,
938	) -> torch.Tensor:
939	    return input.new_empty(
940	        (input.shape[0], output_size_per_partition), dtype=input.dtype
941	    )
942	
943	
944	@register_custom_op(fake_impl=fake_unified_apply_gptq_marlin_gemm_with_wtype)
945	def unified_apply_gptq_marlin_gemm_with_wtype(
946	    input: torch.Tensor,
947	    weight: torch.Tensor,
948	    weight_scale: torch.Tensor,
949	    weight_zp: torch.Tensor,
950	    g_idx: torch.Tensor,
951	    g_idx_sort_indices: torch.Tensor,
952	    workspace: torch.Tensor,
953	    wtype_id: int,
954	    output_size_per_partition: int,
955	    input_size_per_partition: int,
956	    is_k_full: bool,
957	    use_atomic_add: bool,
958	    use_fp32_reduce: bool,
959	    is_zp_float: bool,
960	) -> torch.Tensor:
961	    # Reconstruct ScalarType from id
962	    wtype = None
963	    for attr_name in dir(scalar_types):
964	        if not attr_name.startswith("_"):
965	            st = getattr(scalar_types, attr_name)
966	            if hasattr(st, "id") and st.id == wtype_id:
967	                wtype = st
968	                break
969	    return gptq_marlin_gemm(
970	        input,
971	        None,
972	        weight,
973	        weight_scale,
974	        None,
975	        weight_zp,
976	        g_idx,
977	        g_idx_sort_indices,
978	        workspace,
979	        wtype,
980	        size_m=input.shape[0],
981	        size_n=output_size_per_partition,
982	        size_k=input_size_per_partition,
983	        is_k_full=is_k_full,
984	        use_atomic_add=use_atomic_add,
985	        use_fp32_reduce=use_fp32_reduce,
986	        is_zp_float=is_zp_float,
987	    )
988	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"modelopt_quant.py\" -o -name \"*hybrid*marlin*\" | head -10"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
```

> AGENT

继续查看关键文件：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	# Adapted from https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/quantization/modelopt.py
2	from __future__ import annotations
3	
4	import logging
5	from enum import IntEnum
6	from typing import TYPE_CHECKING, Any, Dict, List, Optional
7	
8	import torch
9	from torch.nn.parameter import Parameter
10	
11	from sglang.srt.distributed import get_tp_group
12	from sglang.srt.distributed.device_communicators.pynccl_allocator import (
13	    use_symmetric_memory,
14	)
15	from sglang.srt.environ import envs
16	from sglang.srt.layers.dp_attention import is_allocation_symmetric
17	from sglang.srt.layers.moe import (
18	    MoeRunner,
19	    MoeRunnerBackend,
20	    MoeRunnerConfig,
21	    get_moe_runner_backend,
22	)
23	from sglang.srt.layers.moe.cutlass_moe_params import CutlassMoEParams, CutlassMoEType
24	from sglang.srt.layers.moe.moe_runner.triton import TritonMoeQuantInfo
25	from sglang.srt.layers.moe.utils import should_use_flashinfer_cutlass_moe_fp4_allgather
26	from sglang.srt.layers.parameter import ModelWeightParameter, PerTensorScaleParameter
27	from sglang.srt.layers.quantization.base_config import (
28	    FusedMoEMethodBase,
29	    LinearMethodBase,
30	    QuantizationConfig,
31	    QuantizeMethodBase,
32	)
33	from sglang.srt.layers.quantization.fp8_kernel import scaled_fp8_quant
34	from sglang.srt.layers.quantization.fp8_utils import (
35	    apply_fp8_linear,
36	    cutlass_fp8_supported,
37	    is_blackwell_supported,
38	)
39	from sglang.srt.layers.quantization.kv_cache import BaseKVCacheMethod
40	from sglang.srt.layers.quantization.unquant import UnquantizedLinearMethod
41	from sglang.srt.layers.quantization.utils import (
42	    convert_to_channelwise,
43	    is_layer_skipped,
44	    per_tensor_dequantize,
45	    prepare_static_weights_for_trtllm_fp4_moe,
46	    requantize_with_max_scale,
47	    swizzle_blockscale,
48	)
49	from sglang.srt.layers.radix_attention import RadixAttention
50	from sglang.srt.utils.common import (
51	    get_bool_env_var,
52	    is_cuda,
53	    is_sm120_supported,
54	    next_power_of_2,
55	)
56	from sglang.srt.utils.custom_op import register_custom_op
57	from sglang.srt.utils.patch_torch import register_fake_if_exists
58	
59	if TYPE_CHECKING:
60	    from sglang.srt.batch_overlap.single_batch_overlap import DownGemmOverlapArgs
61	    from sglang.srt.layers.moe.fused_moe_triton.layer import FusedMoE
62	    from sglang.srt.layers.moe.token_dispatcher import (
63	        CombineInput,
64	        StandardDispatchOutput,
65	    )
66	
67	try:
68	    if is_sm120_supported():
69	        from flashinfer import fp4_quantize
70	    else:
71	        from sgl_kernel import scaled_fp4_quant as fp4_quantize
72	
73	except ImportError:
74	    fp4_quantize = None
75	
76	try:
77	    from flashinfer import mm_fp4 as flashinfer_fp4_gemm
78	    from flashinfer import reorder_rows_for_gated_act_gemm, shuffle_matrix_sf_a
79	
80	    enable_flashinfer_fp4_gemm = True
81	except ImportError:
82	    if is_cuda():
83	        from sgl_kernel import cutlass_scaled_fp4_mm as cutlass_fp4_gemm
84	    enable_flashinfer_fp4_gemm = False
85	    reorder_rows_for_gated_act_gemm = None
86	    shuffle_matrix_a = None
87	    shuffle_matrix_sf_a = None
88	
89	
90	def _load_fp4_autotune_cache() -> None:
91	    """Load offline-tuned mm_fp4 cutlass tactics into the flashinfer AutoTuner
92	    singleton. Non-fatal on failure — fallback tactic=-1 is always valid.
93	    """
94	    import os as _os_inner
95	    path = _os_inner.environ.get("SGLANG_FP4_TUNE_CACHE", "")
96	    if not path or not _os_inner.path.exists(path):
97	        return
98	    try:
99	        from flashinfer.autotuner import AutoTuner
100	        ok = AutoTuner.get().load_configs(path)
101	        logging.getLogger(__name__).info(
102	            f"[fp4-autotune] loaded cache ok={ok} path={path} "
103	            f"entries={len(AutoTuner.get()._file_configs)}"
104	        )
105	    except Exception as _e:
106	        logging.getLogger(__name__).warning(
107	            f"[fp4-autotune] failed to load {path}: {_e}"
108	        )
109	
110	
111	if enable_flashinfer_fp4_gemm:
112	    _load_fp4_autotune_cache()
113	
114	
115	try:
116	    from flashinfer.fused_moe import cutlass_fused_moe as flashinfer_cutlass_fused_moe
117	    from flashinfer.fused_moe.core import ActivationType
118	except ImportError:
119	    flashinfer_cutlass_fused_moe = None
120	
121	    # Define a minimal ActivationType enum if flashinfer is not available
122	    class ActivationType(IntEnum):
123	        Swiglu = 3
124	        Relu2 = 6
125	
126	
127	# Initialize logger for the module
128	logger = logging.getLogger(__name__)
129	
130	
131	def _sglang_fp4_gemm_fake(
132	    input: torch.Tensor,
133	    weight: torch.Tensor,
134	    input_sf: torch.Tensor,
135	    weight_sf: torch.Tensor,
136	    alpha: torch.Tensor,
137	    out_dtype: torch.dtype,
138	    out_features: int,
139	) -> torch.Tensor:
140	    M = input.shape[-2]
141	    N = int(out_features)
142	    return input.new_empty((M, N), dtype=out_dtype)
143	
144	
145	@register_custom_op(fake_impl=_sglang_fp4_gemm_fake)
146	def fp4_gemm(
147	    input: torch.Tensor,
148	    weight: torch.Tensor,
149	    input_sf: torch.Tensor,
150	    weight_sf: torch.Tensor,
151	    alpha: torch.Tensor,
152	    out_dtype: torch.dtype,
153	    out_features: int,
154	) -> torch.Tensor:
155	    backend = FLASHINFER_FP4_GEMM_BACKEND if FLASHINFER_FP4_GEMM_BACKEND else "cutlass"
156	    if enable_flashinfer_fp4_gemm:
157	        return flashinfer_fp4_gemm(
158	            input, weight, input_sf, weight_sf, alpha, out_dtype, backend=backend
159	        )
160	    else:
161	        return cutlass_fp4_gemm(input, weight, input_sf, weight_sf, alpha, out_dtype)
162	
163	
164	if is_cuda() and (not is_sm120_supported()) and (fp4_quantize is not None):
165	
166	    @register_fake_if_exists("sgl_kernel::scaled_fp4_quant")
167	    def _sgl_kernel_scaled_fp4_quant_fake(
168	        output, input, output_scale, input_global_scale
169	    ):
170	        return
171	
172	
173	CUTEDSL_MOE_SCALAR_INPUT_SCALE = get_bool_env_var(
174	    "SGLANG_CUTEDSL_MOE_SCALAR_INPUT_SCALE", "true"
175	)
176	
177	# TODO make it true by default when the DeepEP PR is merged
178	MOE_NVFP4_DISPATCH = envs.SGLANG_MOE_NVFP4_DISPATCH.get()
179	FLASHINFER_FP4_GEMM_BACKEND = envs.SGLANG_FLASHINFER_FP4_GEMM_BACKEND.get()
180	
181	# Hybrid Marlin decode threshold: M <= threshold uses Marlin FP4 GEMV,
182	# M > threshold uses CUTLASS NVFP4 W4A4. Set via env var, 0 = disabled.
183	import os as _os
184	_MARLIN_HYBRID_THRESHOLD = int(_os.environ.get("SGLANG_MARLIN_DECODE_THRESHOLD", "0"))
185	
186	# Per-shape MARLIN_DECODE_THRESHOLD overrides — outranks the global value when
187	# shape (output_size_per_partition, input_size_per_partition) matches.
188	# R3 partial rollback (2026-05-10): 所有 shape 阈值统一回 48，与 baseline 行为一致。
189	# 历史：R2 用 microbench (无 autotune) 数据定阈值 down=128/qkv=64/o=64/eagle=128，
190	# 旧版 quick_validate 测出 bs=8/16 -40% (实际是 cold path 测量噪声，升级 bench 后
191	# 实测 R2 中性，无收益无退化)。R3 撤回非 48 值，保留 dict + resolve 框架供 R4 用
192	# server-internal autotune 真实数据 + 带 batch warmup 的 bench 驱动。
193	# 详见 docs/gemm/changelog.md Round 1-4。
194	# Format: (output_size_per_partition, input_size_per_partition) -> threshold
195	_MARLIN_HYBRID_THRESHOLD_PER_SHAPE: dict[tuple[int, int], int] = {
196	    (32768, 4096):  48,    # gate_up_proj
197	    (4096,  16384): 48,    # down_proj      — R3: 与 baseline 等价
198	    (4608,  4096):  48,    # qkv_proj_std
199	    (4096,  4096):  48,    # o_proj_std
200	    (12288, 4096):  48,    # gla_qkv_proj

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/marlin.md"
}
```

> TOOL

tool_result Read
```
1	# Marlin / b12x 调优
2	
3	range：MiniCPM-SALA NVFP4 Marlin + b12x/CUTLASS 分流。性能口径：CUDA graph replay 内 kernel 时间。
4	
5	## 1. 当前部署
6	
7	| 组件 | 状态 |
8	|---|---|
9	| `common_ops.abi3.so` | `220c18cc` base + Marlin FP4 scale fix + R-blog-tile（不能用 `32d27c7`，EAGLE draft graph 卡 37%，§5） |
10	| `SGLANG_MARLIN_DECODE_THRESHOLD=48` | 生效，M ≤ 48 → Marlin |
11	| b12x 2-tier dispatch | **lock-in** (R-b12x, 2026-05-10)，默认 `SGLANG_ENABLE_B12X=1` |
12	| Draft model | 纯 Marlin (threshold=9999)，M=1-6 时 CUTLASS 比 Marlin 慢 3-8× |
13	
14	## 2. Dispatch
15	
16	| Backend | M | 路径 |
17	|---|---|---|
18	| Marlin W4A16 | 1-48 | bf16 act, CUDA core dequant + HMMA |
19	| b12x W4A4 (CuTe DSL) | 48 < M ≤ 512 | post-permute TMA-swizzled scale |
20	| CUTLASS NVFP4 (flashinfer) | M > 512 (override) | 6 shape override |
21	| b12x W4A4 | M > 512 非 override | bucket 1024/2048/4096/8192 |
22	
23	`process_weights_after_loading` 同时准备 CUTLASS + Marlin 格式，共存 ~4GB VRAM；`apply()` 按 M 分流，CUDA graph safe。
24	
25	## 3. Marlin FP4 关键 fix（R-marlin-fp4-fix）
26	
27	### 3.1 sgl-kernel C++ `dequant_fp8_scales<nv_bfloat162>` 缺陷（dequant.h:442）
28	
29	```cpp
30	constexpr int FP8_EXPONENT = 4, BF16_EXPONENT = 8;
31	constexpr int RIGHT_SHIFT = BF16_EXPONENT - FP8_EXPONENT;  // = 4
32	int Out1 = ((q & 0x80008000) >> 1) | ((q & 0x7F007F00) >> RIGHT_SHIFT);
33	```
34	
35	只做 right-shift 4，**未做 exponent rebias**（FP8 bias=15 vs BF16 bias=127）。与 vLLM PR #34577 BF16 widening underflow bug 形态一致：small global_scale → `2^-112` underflow。
36	
37	### 3.2 Python 端 rescale + clamp (R9 lock-in, commit 1183bae)
38	
39	`marlin_utils_fp4.py` 在 `nvfp4_marlin_process_global_scale` 加 rescale + clamp，防御 weight_scale max < 3.5 silent underflow。Python only，性能 ±0.4% 噪声层。**marlin_utils_fp4.py 实际代码注释引用本节作 fix 出处**——修改时同步更新。
40	
41	## 4. Marlin SASS 分析（gate_up M=1）
42	
43	```
44	HMMA:                              48 条
45	HFMA2+HADD2+HMUL2 (CUDA core FP):  532 条
46	LOP3+SHF+PRMT (dequant):           454 条
47	地址计算:                           536 条
48	```
49	
50	HMMA:HFMA2 = 1:11，张量核空转。瓶颈在 CUDA core dequant。**Marlin 在 sm_120 W4A16 M=1-8 decode 已近 Pareto 最优**，继续压 ROI <2%。
51	
52	## 5. `.so` 兼容性警告
53	
54	`32d27c7`（含 small-M atomic + shape-aware tile，~+3%）**导致 EAGLE-3 draft CUDA graph capture 挂死 37%**。生产必须 `220c18cc` 系。要恢复 Marlin 3% 必须 bisect small-M atomic vs shape-aware tile，找冲突点。
55	
56	## 6. 已落地 kernel-side 优化
57	
58	| Patch | 实测 |
59	|---|---|
60	| SimpleGLA direct-state decode (`e922b76`) | bs=1 2.33×, bs=8 3.39× |
61	| compress_k head-parallel rewrite | bs=1 k1 1.99×, k2 1.81× |
62	| Skip-fill compress_k -inf buffer (`5c83e4c`) | -0.103 ms/step |
63	| Decode pooling no-zero | S1 1.52× |
64	
65	## 7. 负结果（不重踩）
66	
67	- pipe_stages 4→6：e2e <0.5%
68	- `use_fp32_reduce=False`：M=4-8 退化 9-17%
69	- native FP4 MMA：PTX 要求 A+B 都 FP4
70	- tile/warp sweep：HMMA:HFMA2=1:11，换 tile 不改 HFMA2
71	- `--fuse-topk`：破坏 k1+k2 语义
72	- stage2 `disable_split_kv`：21→230 µs
73	
74	### 7.1 stage1 k1+k2 语义（必须保持）
75	
76	`infllmv2_attn_stage1(q, k=k1, v=k2)`：第一段用 k2 跑 coarse softmax 得 row max/sum，第二段用 k1 + `softmax_rescale_gt()` 写 score。**k1-only fused topk 是错的**——官方 score 不是 `softmax(q @ k1)`。
77	
78	## 8. 当前 decode 剩余热点（S8 trace）
79	
80	| class | calls/step | ms/step |
81	|---|---:|---:|
82	| Marlin | 160 | 4.9032 |
83	| attention split/paged-kv | 24 | 1.7541 |
84	| SimpleGLA direct | 24 | 0.4748 |
85	| BF16/CUTLASS GEMM | 1 | 0.4588 |
86	| compress_k | 16 | 0.4037 |
87	
88	下一轮高 ROI 不在 Marlin tile，而在 **k1+k2 语义保持的 stage1 fused topk**。
89	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

好的，现在查看 sgl-kernel 的具体 gemm 函数签名和 FP8 支持情况：

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"*.md\" -path \"*/docs/gemm/*\" | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/docs/gemm/so-replacements.md
/user_4813494d/openbmb/docs/gemm/marlin.md
/user_4813494d/openbmb/docs/gemm/kernels-sm120.md
/user_4813494d/openbmb/docs/gemm/README.md
/user_4813494d/openbmb/docs/gemm/current.md
/user_4813494d/openbmb/docs/gemm/roadmap.md
/user_4813494d/openbmb/docs/gemm/methodology.md
/user_4813494d/openbmb/docs/gemm/dead-ends.md
/user_4813494d/openbmb/docs/gemm/charter.md
/user_4813494d/openbmb/docs/gemm/hardware.md
/user_4813494d/openbmb/docs/gemm/sol_table.md
/user_4813494d/openbmb/docs/gemm/changelog.md
/user_4813494d/openbmb/docs/gemm/todo.md
/user_4813494d/openbmb/docs/gemm/sop.md
/user_4813494d/openbmb/docs/gemm/evt_fusion_design.md
/user_4813494d/openbmb/docs/gemm/bottleneck_cards/01_o_proj_std_M48.md
/user_4813494d/openbmb/docs/gemm/bottleneck_cards/02_down_proj_M128.md
/user_4813494d/openbmb/docs/gemm/.ipynb_checkpoints/changelog-checkpoint.md
/user_4813494d/openbmb/docs/gemm/.ipynb_checkpoints/todo-checkpoint.md
/user_4813494d/openbmb/docs/gemm/.ipynb_checkpoints/dead-ends-checkpoint.md
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/current.md"
}
```

> TOOL

tool_result Read
```
1	# sm_120 GEMM 当前事实
2	
3	事实来源：`cuobjdump` on `demo-sala/common_ops.abi3.so`（2026-05-11）+ sgl-kernel `CMakeLists.txt:50` + git diff 实测。瞬时 bench 数字重测跑 `bench/quick_validate.sh`。
4	
5	## 0. HEAD 概要
6	
7	- **HEAD**：`demosala-rollback`，post R-blog-tile lock-in (2026-05-11)
8	- **量化**：NVFP4 (GPTQ + FourOverSix，loguniform128 校准，48K 上下文)
9	- **Dispatch**：Marlin (M ≤ 48) / b12x W4A4 (48 < M ≤ 512 或 ∉ override) / flashinfer mm_fp4 (M > 512 ∈ override)
10	- **EAGLE-3**：chain verify，`spec_steps=3, topk=2, dtn=7`，dynamic spec (NO_SPEC/D5/D7)
11	- **Draft model**：`eagle/models/v2mix_20k_s3500_ood757/`（NVFP4 QAT，纯 Marlin path，`SGLANG_MARLIN_DECODE_THRESHOLD=9999`）
12	
13	## 1. 当前 `.so` 速查
14	
15	| 字段 | 值 |
16	|---|---|
17	| 部署 | `demo-sala/common_ops.abi3.so` → `${VENV_SP}/sgl_kernel/sm100/common_ops.abi3.so` (`prepare_env.sh` G1) |
18	| 加载 | `sgl_kernel/load_utils.py:60-65`：sm_120 落 `ops_subdir="sm100"`（共用目录非 sm100 cubin） |
19	| 编译目标 | **sm_120a** 74 cubins，无 PTX 兜底 |
20	| 编译开关 | `-gencode=arch=compute_120a,code=sm_120a` + `-DENABLE_NVFP4=1` + `--compress-mode=size` |
21	| sgl-kernel | 0.3.20，内嵌 CUTLASS **4.2.0**（commit `57e3cfb`） |
22	| FlashInfer | 0.6.8.post1，内嵌 CUTLASS 4.4.2 |
23	| 大小 / md5 / sha256 | 25 121 160 B / `dc3ab83e2061…` / `5ea432cf56db…` |
24	| 来源 | `220c18cc + Marlin FP4 scale fix + R-blog-tile` (2026-05-11) |
25	| 备份 | `outputs/so_backups/20260511-044425__pre_rblogtile_lockin/` |
26	
27	## 2. sm_120 NVFP4 GEMM Kernel 资源
28	
29	资源约束：max warps/SM=48（2026-05-10 实测）、max blocks/SM=24、Register file/SM=256 KB、SMEM/SM=100 KB。
30	
31	**REG=168 是 NVFP4 GEMM 物理下限**：warp tile 64×64 fp32 accum = 128 reg/thread；+frag double buffer +scale +addr ≈ 168。要降必须缩 warp tile → 复用减半 → 得不偿失（[methodology.md §11](methodology.md) + [dead-ends.md §B](dead-ends.md)）。`setmaxnreg` 不改 occupancy。
32	
33	`.so` 内 sm_120 dense NVFP4 实例：Cooperative `KernelTmaWarpSpecializedCooperativeBlockScaledSm120` × 4（REG=168，SHARED=1024，dense 主用） + PingpongBlockScaled Array × 1（grouped MoE，不用）。Tile shapes `<256,128,128>` / `<128,128,128>`；MMA atom `SM120_16x8x64_TN_VSI`（e2m1×e2m1→f32，ue4m3 scale）。
34	
35	**关键事实**：sm_120 NVFP4 BlockScaled **物理上无独立 PingPong dense kernel**，任何 "切 PingPong" 立刻拒（[dead-ends.md §B](dead-ends.md#b)）。
36	
37	**Marlin kernel REG 100-127**（19×100 + 27×122-127）—— 比 NVFP4 dense 168 低，是 Marlin 在 small M 优于 CUTLASS 的硬件依据。
38	
39	**死代码**：`Sm100*` (tcgen05/UMMA) 52 + `Sm90*` (WGMMA) 111 = 163 个被实例化但 sm_120 调用即崩。潜在 .so 体积优化（与性能无关）。
40	
41	## 3. sgl-kernel Marlin FP4 路径
42	
43	- **Python**：`marlin_utils_fp4.py` 与上游 PR #19652 cosmetic 差异；R9 已加 rescale + clamp（[marlin.md §3.2](marlin.md)）
44	- **C++ (dequant.h:442)**：只 right-shift 4，**未做 exponent rebias** → vLLM PR #34577 BF16 widening underflow 同形态（[marlin.md §3.1](marlin.md)），生产 underflow 未实测确认
45	- **marlin_template.h.rej**：sgl-kernel 已有自家维护的 NVFP4 1-byte FP8 scale 特殊路径，与上游"删特殊路径"冲突
46	
47	## 4. CUTLASS 4.2.0 → 4.4.2 实际 diff
48	
49	git diff `57e3cfb`..`v4.4.2`：`sm120_blockscaled_mma_tma.hpp` 2 行 `alignas(16)` smem_SFA/B；`sm120_blockscaled_mma_array_tma.hpp` 2 行（同上）；`sm120_gemm_tma_warpspecialized_cooperative_asymmetric_dma.hpp` 0 行；`dispatch_policy.hpp` +140 全 SM100 InterleavedComplexTF32 / PlanarComplex（与 sm_120 无关）。
50	
51	CHANGELOG "Fix memory fence clc scheduler Blackwell SM120 pingpong" 在 sm120 文件看不到 diff；生产走 dense Cooperative 非 Pingpong。**升 4.4.2 对 sm_120 dense GEMM 几乎无影响**。唯一稳定收益：`alignas(16)` SMEM scale fix，可 cherry-pick 不需全升。
52	
53	## 5. 待验证 / 已废弃
54	
55	待验证：`dequant_fp8_scales<nv_bfloat162>` 小 global_scale underflow 实证；`cvt.rn.bf16x2.e4m3x2` issue rate vs 6 ALU；sm_120 BlockScaled K_BLOCK_MAX + NamedBarrier cycle。
56	
57	已 resolved：max warps/SM=48；`.so` spill 1128 LDL/STL avg 17/kernel ~0.5% cycle 不致命（[changelog.md R1.3](changelog.md)）。
58	
59	已废弃：~~PingPong dense BlockScaled~~ / ~~借 RTX PRO 6000 ncu~~（[dead-ends.md §B/C](dead-ends.md)）。
60	
61	## 6. 关键文件路径
62	
63	```
64	demo-sala/common_ops.abi3.so
65	demo-sala/sglang/python/sglang/srt/layers/quantization/{marlin_utils_fp4.py, b12x_fp4.py}
66	opt/.../sgl-kernel/csrc/gemm/marlin/{marlin_template.h, dequant.h:442}  # FP8→BF16 widening
67	opt/.../sgl-kernel/csrc/gemm/nvfp4_scaled_mm_kernels.cu
68	```
69	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/dead-ends.md"
}
```

> TOOL

tool_result Read
```
1	# sm_120 + NVFP4 + 容器云 GEMM 调优死路 catalog
2	
3	每条标"死因 + 实证来源 + 看到这个想法立刻拒"的硬规则。看到任何报告/PR/讨论提议下面任一方向，**直接拒绝**，不要再调研、不要"再试一次"。
4	
5	---
6	
7	## A. 硬件物理不存在（永远不可能）
8	
9	sm_120 上以下方向物理无：
10	
11	- FA4 / `tcgen05` 系列（无 TMEM）
12	- WGMMA (`wgmma.mma_async`)（不在 WGMMA target）
13	- Cluster ≥ 2 / Distributed Shared Memory（cluster 锁 1×1×1）
14	- TMA multicast / gather4（无 cluster）
15	- FP16/BF16 sparse 2:4 tensor core（consumer 无 sparse TC）
16	
17	参考：Blackwell tuning guide、PTX ISA 9.x、CUTLASS sm120 codepath、FlashInfer issue #3170。
18	
19	---
20	
21	## B. 配置层错误方向（被实证推翻）
22	
23	- ~~"PingPong dense NVFP4 path"~~ — sm_120 NVFP4 BlockScaled 只走 cooperative；PingPong 与 Cooperative 是同一个 kernel
24	- ~~"setmaxnreg 改 occupancy"~~ — 只在 producer/consumer 内重分布，CTA 总池 launch 时静态
25	- ~~"REG=168 可降到 120"~~ — Warp tile 64×64 fp32 accum 已 128 reg；168 是物理下限
26	- ~~"占用越高越好"~~ — Volkov 证伪；occupancy 是手段不是目标
27	- ~~"sm_120 max warps/SM = 48"~~ — 与多源 64 矛盾；只影响 occupancy% 数字
28	- ~~"升 CUTLASS 4.2.0 → 4.4.2 拿 sm_120 dense GEMM 大收益"~~ — sm120 collective 仅 18 行 + SM100 无关代码；仅 alignas(16) cherry-pick 有意义（修 N<128 broadcast silent corrupt）
29	- ~~"借卡 ncu profile"~~ — 容器云不允许
30	- ~~"vLLM PR #34577 是 kernel BF16 widening"~~ — 实为 Python 端 `_nvfp4_compute_scale_factor` power-of-2 rescale + `<2→0` clamp；缺 → weight_scale max<3.5 silent underflow `2^-112`
31	
32	---
33	
34	## C. 工具层永久不可用（容器云 + sm_120 SKU 锁）
35	
36	`ncu` HW counter、CUPTI Range Profiler、CUPTI PC Sampling/SASS、GPUscout、Zymtrace 全部 SKU/PerfWorks 锁；`nvidia-smi --lock-gpu-clocks` / `--power-limit` 无 user_4813494d；MaxAs/TuringAs/sass-king 不支持 Blackwell SASS；DeepGEMM sm_120 不支持（issue #236）。底层调优只能 cuobjdump SASS + nsys timeline + ncu_occupancy Python API + 自写 microbench。
37	
38	---
39	
40	## D. 库 / 框架层死路
41	
42	- TensorRT-LLM `mm_fp4` trtllm backend（sm_120 capability check 死，FI issue #2577）
43	- cuBLASLt 默认 sm_120 dispatcher（Cloudrift 实证 60% 选错 kernel）
44	- IST-DASLab/marlin 上游冻结，sm_120 改进在 vllm-project/vllm 的 marlin fork
45	- FlashInfer `mm_fp4(backend="cute-dsl")` sm_120 不支持
46	- `--fuse-topk`（属于 sparse attention 不是 GEMM）
47	- native FP4 MMA / QuTLASS W4A4 替换 W4A16（mma.kind=mxf4nvf4 要求 A+B 都 FP4）
48	
49	---
50	
51	## E. 量化方向死路
52	
53	- trtllm_fmha_v2_prefill 直调（speedup 来自跳过 garbage 行，accuracy 无法在比赛 eval 闭环）
54	- BLASST skip-softmax on sm_120（任何非零阈值 NaN/Inf，上游 bug）
55	- `BatchPrefill backend="trtllm-gen"` wrapper（sm_120 抛 Unsupported）
56	- KV cache 重组为交错格式（现有布局已交错）
57	- SageAttention3（Python ≥ 3.13 硬要求；无 varlen/paged KV API）
58	- FA3 / FA4（无 TMEM）
59	
60	---
61	
62	## F. 测量层反模式（看到这种"实证"立刻拒）
63	
64	**调研期反模式**：
65	- 不画 roofline 直接动手
66	- 没有 reference baseline
67	- 一次改多个变量
68	- 只看 wall-clock 不看 kernel-level metric
69	- 照抄别人 commit hash + 数字（不同硬件不可迁移）
70	- 优化非 critical path（Amdahl 反例）
71	
72	**测量期反模式（容器云特有）**：
73	- 单次跑就报数字
74	- 用 wall-time 比指令数变化（先看 SASS diff）
75	- 没排除冷启动 / JIT
76	- 邻居偷 HBM/PCIe（时段性方差爆炸不识别）
77	- DVFS sticky（长 kernel 后接短 kernel → 测降频频率）
78	- 测量本身扰动测量（每 kernel 插 event/sync 破坏 overlap）
79	- launch overhead 主导（< 10 μs kernel 30% 是 launch）
80	- 跨容器 runner 切换（baseline 和 candidate 在不同节点）
81	- 报数不报分布（只 mean 不 CI / IQR）
82	- A/B sequential 而非 interleaved（DVFS sticky 污染）
83	
84	**架构层反模式**：
85	- 占用越高越好（Volkov 证伪）
86	- autotune 当万能药（search space 错就放大错误）
87	- 混淆 numerical regression 与 perf regression
88	- tunable 范围过大但 budget 不够（noise > 候选差异）
89	
90	---
91	
92	## G. 失败模式 catalog（已踩坑/确认）
93	
94	- **Marlin `32d27c7`** small-M atomic + shape-aware tile 与 EAGLE draft cuda graph 不兼容（draft graph capture 37% 卡死）→ 必须 `220c18cc`；atomic clear scratch 必须在 cuda graph 外。
95	- **sgl-kernel cutlass_scaled_fp4_mm scale `/2` bug** → NVFP4 cos_sim=0.77；`220c18cc` base 已修；任何 .so 替换必须先验证 cos_sim。
96	- **dequant_fp8_scales silent underflow `2^-112`**（weight_scale max < 3.5 silent garbage，wall-time 不变）→ backport vLLM PR #34577 等价 Python rescale + clamp。
97	- **CUTLASS 4.2.0 sm120 BlockScaled mma SMEM scale 缺 `alignas(16)`** → N<128 broadcast silent corruption → cherry-pick 4.4.0 fix。
98	- **b12x backend 必须喂 `weight_scale_interleaved`**（不是 `padded_scales`）否则模型答非所问 → 复用 `layer.weight_scale_interleaved`。
99	- **容器云 DVFS sticky** → A/B 必须 interleaved，每边 N=50，同步 DCGM 丢低频样本。
100	- **nvcc plain C `(q&MASK)|((q&X)>>N)` 拆 LOP3+SHF+PRMT** → 显式 `lop3.b32` inline asm 或 `cvt.rn.bf16x2.e4m3x2`。
101	
102	---
103	
104	## H. 看到立刻拒的"伪实证"标志
105	
106	PR/调研出现下列**任一**直接拒绝：引用别人 commit/数字未在我们卡跑；单次 wall-time 无 trial/分布；A/B 在不同容器；提案切到 §A 物理不存在的 kernel；借卡/换硬件；升级 CUTLASS 全栈（实证 0 差异）；没回答"影响哪个物理常数/traffic/latency"；没回答"属于 5 正交模块（Mainloop/Epilogue/TileScheduler/Pipeline/Numerics）的哪一个"；没回答"何时停"（charter SOL% / 3 轮 <1% / 破坏正交）。
107	
108	---
109	
110	## I. 演化判定（何时进入下一代 kernel）
111	
112	**判定准则**：上一版瓶颈模型是否仍成立——**不是 speedup 数字**（FA v1→v4 / CUTLASS 4.x / Marlin→Machete 三证据）。SOAR 当前：Marlin (M≤48 W4A16) + CUTLASS NVFP4 (M>48 W4A4) + flashinfer mm_fp4 autotune cache。切下一代触发：sm_120 NVFP4 BlockScaled mainloop SOL>90% / 新硬件路径解锁 / 上游算法替代。**不切的标志**：5% speedup、跟随某 commit、autotune 多 1 tile、cherry-pick alignas — 都是同代精修。
113	
114	---
115	
116	## J. R5b — A/B/A bench config 不等于 production config
117	
118	**陷阱**：dispatch tuning 在某 config +13-15%，切到 production -1.9%~-19%。
119	
120	**根因**：(1) `eval/start_eagle.sh` 有 uncommitted `--kv-cache-dtype fp8_e5m2` → `disable_cuda_graph=True` → eager → Marlin 占便宜 (2) autotune cache 在 cuda graph 下才发挥作用 (3) cache version mismatch silently 退化 (4) microbench → e2e 非单调。
121	
122	**SOP**：bench 前 `git status` 检查启动脚本；A/B/A lock production config（BF16 KV + cuda graph + autotune cache）；autotune version warning 是阻塞信号；覆盖 cuda graph 边界（M<32 / 40-200 / ≥256）。
123	
124	**弃用**：per-(shape,M) Marlin override @ M∈{56,112}；无 autotune microbench 推 dispatch 阈值。
125	
126	---
127	
128	## K. R6 — Autotune cache 元数据 strip 强制加载（无收益）
129	
130	**陷阱**：强制加载 mismatch cache 拿回 autotune 增益。**实测**：A/B/A 三 run 漂移 ≤ 0.5%。**根因**：69 entry key 单 bucket 覆盖 M∈[1,2048]，spec verify M∈{11,28,56,84,112,168} 选的 tile 与 default heuristic 几乎相同。strip 绕过 mismatch ≠ 覆盖关心的 M。**正路**：production server 内 `with autotune(True)` 对真实 M 跑 fresh autotune。
131	
132	---
133	
134	## L. R8 — 移除 bs=24 from autotune sweep 不能恢复 bs=24 退化
135	
136	**陷阱**：R7 bs=24 (M=168) -0.75% 唯一退化，从 sweep 移除走 default heuristic。**实测**：B+B' bs=24 ≈ 1998-2002 < 0.1% 变化，完全不回 default baseline (2013)。**未确认真因**：cuda graph capture bs=24 graph 与邻居 autotune'd graph 共享 scratch/plan/workspace。**沉淀**：bs=24 -0.75% 是已知 trade-off，net 正向；ROI 低（生产 < 5%）不追。
137	
138	---
139	
140	## M. b12x backend (target-only enable) — ~~精度损失放弃~~ **已平反**（2026-05-10 R-b12x）
141	
142	> 原 dead-end，2026-05-10 R-b12x 实证撤销，保留作历史记录。
143	
144	历史（2026-04，已撤销，commit 5c8b107）：以"精度损失 / accept-rate 长尾退化"为由回滚 B12X dispatch。
145	
146	重新调查（2026-05-10）按 SOP 补 numerics + e2e A/B：
147	- numerics：4 shapes × 9 M = 36 组合 vs flashinfer cutlass **全部 max_diff=0 / cos_sim=1.0 / argmax 100%**（bit-exact）
148	- e2e：Decode single **+28.5%** (146→188 tok/s)；bs=8/12/16/24 +6-12%；bs=4 (M=28) -6%
149	
150	现结论：`SGLANG_ENABLE_B12X=1` 新默认。历史"精度损失"应理解为原作者 reference 错误，或 accept-rate 退化是 EAGLE 随机性。R9 lock-in (1183bae) scale rescale 封堵了 BF16 widening underflow 路径。**教训**：看起来像精度问题也可能是测量噪声/reference 错误，永远先 microbench 比对再下 dead-end。
151	
152	---
153	
154	## N. R10/R11 — sgl-kernel CUTLASS 4.2.0 → 4.4.x cherry-pick 对生产 NVFP4 dense GEMM 无效（2026-05-10）
155	
156	**陷阱**：todo Tier 2.1/2.2/1.2 基于"sgl-kernel CUTLASS 4.2.0 落后，cherry-pick 拿 1-3%"。
157	
158	**实证驳斥**：(1) production NVFP4 dense GEMM 走 flashinfer 不走 sgl-kernel — `modelopt_quant.py:77` 优先 `flashinfer.mm_fp4`，sgl-kernel `cutlass_scaled_fp4_mm` 仅 ImportError fallback；当前 flashinfer 正常 → sgl-kernel CUTLASS NVFP4 = 死代码。(2) flashinfer 0.6.8.post1 bundled CUTLASS 已 4.4.2，`sm120_blockscaled_mma_tma.hpp:259-260` 已含 `alignas(16)`。
159	
160	**结论**：R10 alignas / R11 SF SmemCopyAtom uint32 = 完全/基本死路；R14 CUTLASS 4.5.0 升级 + 新 tile 必须改 flashinfer bundled CUTLASS + JIT cache 协议；R12 见 §S 进一步否决；R13 EVT 必须 fork flashinfer mm_fp4。R15 dequant_fp8_scales PTX 2026-05-10 否决 — `dequant.h:442-455` 非标准 bit-shuffle（sign bit15→14，整体 `>>4` 无 bias），与 `cvt.rn.bf16x2.e4m3x2` 不等价，替换要重打包权重。
161	
162	**沉淀**：所有"sgl-kernel CUTLASS pin 4.2.0 落后"ROI 估计先 verify (a) flashinfer 是否已含 (b) sgl-kernel 是否 hot path — 两者都 yes 才有意义。
163	
164	---
165	
166	## O. R-b12x-bucket64 — `_M_BUCKETS` 加 64：bench@isolated 通过但 production e2e 退化（2026-05-10）
167	
168	**假设**：M∈{49,64,80,96} microbench b12x (64,64,F)/(64,128,T) 比 bucket=96 现 tile 快 14-44%。
169	
170	**测量层 PASS**：quick_validate bs=8 +1.98% 可复现。**production e2e FAIL**：full eval ori_acc 80.33→79.27% (-1.06pp)，duration 1303→1416s (+8.7%)，长尾 mcq 单 batch ~4min。
171	
172	**根因**：quick_validate 稳态短输出 = 单 bucket；EAGLE-3 accept_rate≈0.34 → M 在 48/64/96 边界横跳 → kernel cache thrashing。**fallback path bug**：未给 down 加 explicit bucket=64 entry，`_M_BUCKETS` 含 64 后 down 走 `_resolve_tile` fallback `reversed(_M_BUCKETS)` 选 bucket=8192 tile 编 M_bucket=64 kernel 加剧 thrashing。
173	
174	**SOP**：`_M_BUCKETS` 改动必须 full eval gate；所有 6 production shapes 覆盖测量；新 bucket 必须 audit fallback semantics 或全 shape 显式 entry。
175	
176	**弃用**：部分 shape 加 entry；quick_validate-only lock-in；bench@isolated 推 production。
177	
178	---
179	
180	## P. R-b12x-prefill — 提升 `SGLANG_B12X_MAX_M` 512→8192 让 b12x 接管 prefill（2026-05-11）
181	
182	**假设**：M=8192 prefill 占 cutlass 95%+；microbench b12x 在 M∈{1024,2048,4096,8192} 普遍 +2%~78%（std_o M=2048 1.78×）。
183	
184	**Patch**（已回滚）：`SGLANG_B12X_MAX_M=8192` + prune `TUNED_CUTLASS_OVERRIDE`。dispatch verified：std_o/down/gla_qkv M=8192 → b12x。
185	
186	**mini_bench e2e — NET REGRESSION**：S1 129→**155s (+19.9%)**、S8 227→214s (-6%)、Smax 414→**431s (+4.1%)**。
187	
188	**原假设推翻**："Python dispatch 50-200µs/call" — `measure_dispatch_overhead.py` 实测 wrapper overhead < 5µs/call。**真因未定位**，候选（未验证）：(1) production memory pressure cache-thrash b12x SF tensor (2) `torch.empty((M,N))` 每 call alloc 32MB vs flashinfer 内部 pool (3) CUDA stream/sync 冲突 (4) 微基随机权重与生产 SF pattern 互动差异。
189	
190	**§P 真因排查 Phase B（2026-05-11 12:30，`bench/b12x/diag_p_sustained.py`）**：5 prefill shapes × M=8192 × `{hot, cold-L2}` × `{b12x, cutlass}` 各 200 iters × 5 outer trials。**HOT** = 同一 weight 复用；**COLD-L2** = 32 个 weight 轮询模拟 32 层。
191	
192	| shape | b12x HOT | b12x COLD | cut HOT | cut COLD | HOT b/c | COLD b/c | L2 pen b | L2 pen c |
193	|---|---:|---:|---:|---:|---:|---:|---:|---:|
194	| std_o     | 0.505m | 0.505m | 0.533m | 0.531m | **1.056×** | 1.051× | +0.0% | -0.4% |
195	| std_qkv   | 0.572m | 0.572m | 0.571m | 0.570m | 0.999× | 0.997× | +0.0% | -0.2% |
196	| gla_qkv   | 1.501m | 1.501m | 1.516m | 1.515m | 1.010× | 1.009× | -0.0% | -0.1% |
197	| gate_up   | 3.969m | 3.968m | 3.956m | 3.956m | **0.997×** | 0.997× | -0.0% | +0.0% |
198	| down      | 2.016m | 2.017m | 2.096m | 2.098m | 1.040× | 1.040× | +0.0% | +0.1% |
199	
200	**关键发现**：
201	1. **L2 weight thrash 候选根因 (1) 推翻**：HOT 与 COLD-L2 两模式全部 5 shape 差 < 0.5%，证 32 层轮询 weight 与同一 weight 200 iters 等价 — L2 不是 b12x/cutlass 性能差源；
202	2. **§P 前提"microbench 78% 全胜"在 M=8192 不成立**：M=8192 b12x 平均仅 +1.4%（−0.3%~+5.6%），**两个最大 shape（gate_up、std_qkv）b12x 实际等于或慢于 cutlass**；78% 速胜是 M=2048（std_o）值，不能外推到 M=8192；
203	3. **gate_up 是 prefill 最大算力消耗 shape**（3.96ms vs std_o 0.51ms，**比重 ≈ 50%**），b12x 在此 shape 上不胜，所以 prefill 整体期望收益 ≤ 1%；
204	4. **§P e2e -25s 与 microbench 无矛盾**：算式 `δ_kernel × 24576_calls ≈ 0` 给不出 25s，需另查 host-side（dispatch/quantize/sync/alloc 非 GEMM 部分的微差）。
205	
206	**重写候选根因**：(1) L2 thrash **REFUTED**；(2) alloc **REFUTED** (§T)；(3) stream/dispatch 已知 <5µs（§P 原始）；剩余 = host-side per-call 微差累积（CPU 端 dispatch / fp4_quantize 路径 / `out.view(...)` reshape）需 per-call 微基准对照测量，但 ROI ≤ 1% e2e（因 microbench 已显示 GPU-side 无攻击面）。
207	
208	**弃用补充**：
209	- 任何"M=8192 b12x microbench 速胜"假设（实测均值 +1.4%，**且两个主算力 shape 不胜**）；
210	- 任何"L2 weight thrash 是 §P 根因"假设；
211	- 用 M=2048 microbench 数据外推 M=8192 e2e 行为。
212	
213	**artifacts**：
214	- `bench/b12x/diag_p_sustained.py`（保留，作为 sustained-throughput 对照工具）
215	- `bench/b12x/diag_p_sustained.json`
216	
217	**SOP**：mini_bench **S1+S8+Smax 三档全部 ≥ baseline** 才进 quick_validate（S8 单档赢不算）；microbench 只能"排除"不能"确认"；攻击 prefill M=8192 必须改 flashinfer csrc 或自写 fused kernel。
218	
219	**弃用**：bump `SGLANG_B12X_MAX_M > 512`；"microbench 1.78× → 生产 1.78×"；Python dispatch C++ 化（overhead <5µs）。
220	
221	---
222	
223	## Q. R-blog-tile-v2 — 加 Marlin LB idx3 = `{tk=64, tn=128, t=256}` 配置无效（kernel 越界写）（2026-05-11）
224	
225	**假设**：idx1 NUM_THREADS 128→256 变体在 issue rate / warp scheduling 角度优。
226	
227	**Patch**（已回滚）：`gptq_marlin.cu` 加 `{64,128,256}` + N=12288 段 `order[3]=3`。
228	
229	**microbench 假胜 + CUDA illegal memory access cascade**：gate_up/down M=32 idx3 vs default **-14~-16%**（phantom）。`down_proj M=48 idx3` 30 trials σ=0.63 无异常 — 看起来真胜。但下次 launch (`qkv_proj_std M=1`) 立即 `CUDA error: illegal memory access`，**整个 CUDA context 污染**。
230	
231	**根因**：idx3 `(THREAD_N_BLOCKS=8, THREAD_K_BLOCKS=4, NUM_THREADS=256)` **不是 valid Marlin 配置**。Marlin 内部 (warps×N×K) 不变式可能假设 NUM_THREADS=128，模板实例化编译期合法但 runtime 写出 buffer。"巨胜"是 kernel 做了错误 work，CUDA error 是 async illegal 在 next launch 同步报出。
232	
233	**关键教训**：**microbench timing 通过 ≠ kernel 正确**。新 tile 必须 (1) 数值 vs upstream-validated bit-exact (2) 后续 launch 无 illegal access (3) 多 shape cross-test 无污染。
234	
235	**SOP**：新 Marlin tile 候选必须从 upstream vLLM marlin commit history 抓；microbench 加 sentinel check（每 trial 后跑独立 `torch.zeros` 哨兵）；timing >10% kernel-level 增益必须警惕。
236	
237	**弃用**：Marlin LB idx3 `(8,4,256)`；microbench σ 小=正确；ad-hoc `(N,K,NUM_THREADS)` 组合。
238	
239	---
240	
241	## R. R-blog-tile-v3 — SB 路径 (N,K)-aware tile reorder：单点信号，ROI 不实施（2026-05-11）
242	
243	**假设**：R-blog-tile 已覆盖 LB 路径，SB 路径（thread_m_blocks=1, M≤16）仍 default。
244	
245	**实测**：18 SB 点唯一显著 o_proj_std (N=4096,K=4096) M=16 idx2 **-9.19%**（21.09→19.15 µs）。其它 default idx0 已最优或 ≤ 2% 噪声。
246	
247	**为什么不实施**：信号面太窄（1 shape × 1 M = EAGLE-3 bs=2 D=7）；ROI 上限 1.8%/下限 0.6%；**§6.2 停手信号 #1 已触发**（近 3 轮 R-marlin-fp32reduce/R-b12x-bucket64/R-blog-tile-v2 全 REJECTED）；R-XX-v2 系列模式重复：微基窄信号难 e2e 兑现。
248	
249	**2026-05-11 12:30 σ-check 二次确认（R-marlin-sb-tile 重启分析）**：sweep `outputs/quick_validate/rblogtile_20260511-074040.json` 里 gate_up_proj (N=32768) SB M=1/8/16 idx0 vs default 看似 -2.4/-1.9/-0.9%。用 σ = sqrt(σ_def² + σ_idx0²) 算 9 cells（6 SHAPES × M ∈ {1,8,16} 中 N=4096/4608/32768 9 cell）：
250	
251	| n_σ 区间 | cells |
252	|---|---:|
253	| \|n_σ\| ≤ 0.5 | **9/9** 全是 NOISE |
254	| 最大 \|n_σ\| | 0.5（gate_up_proj M=1 -0.5σ） |
255	
256	**SB 9 cells 全部统计上等价 default**。看 -2.4% 兴奋时，σ_def=1.48 µs / σ_idx0=0.57 µs → 综合 1.58 µs，Δ=-0.83 µs → -0.5σ 纯噪声。R-blog-tile original comment "small_batch 在所有 N 上 default 都最优" 在 σ 检验下成立。
257	
258	**反模式补充**：本次重启分析犯了 SOP §F 反模式 "看 Δ% 就开干而不 σ-check"。**任何 GEMM tile/dispatch sweep 立项前必须 σ-check**（不只是 σ 显示但要 \|n_σ\| > 2 才算信号）。本次 R-marlin-sb-tile 静态阶段证伪，无 patch、无 rebuild、无 backup 需要。
259	
260	**复活条件**（强化）：production dispatch SB M=16 占比 ≥ 20%（当前 attribution_prod 显示 SB 总 wall < 5%）；§6.2 reset；找到 upstream-validated SB (N,K)-aware reorder；OR 增 sweep N_samples 把 σ 降到 0.2 µs 重测有无 >2σ 信号。
261	
262	---
263	
264	## S. R12 显式 KernelSchedule（PINGPONG/COOPERATIVE/WARPSPECIALIZED）在 sm_120 NVFP4 BlockScaled 上无搜索空间（2026-05-11）
265	
266	**假设**：flashinfer `getConfigs()` 6 tactic 全 `MainloopScheduleType::AUTO`，显式指定拿 1-3%。
267	
268	**实证否决**：
269	1. `cutlass_gemm_configs.h:159-184` `MainloopScheduleType` 注释明确 Hopper-only — non-Hopper 落到 "legacy"
270	2. flashinfer csrc 已 hardcoded `KernelTmaWarpSpecializedCooperative`（`fp4_gemm_template_sm120.h:261`），不经 user 枚举
271	3. **cubin 验证**：AOT 6 kernel 全部 `KernelTmaWarpSpecializedCooperativeBlockScaledSm120<Li3EEE>`，无 PingPong
272	4. sm_120 BlockScaled CollectiveMainloop 模板特化只覆盖 Cooperative
273	
274	与 §A 不同：sm_120 物理可跑 Cooperative，但 BlockScaled PingPong/2SM-coop **CUTLASS 没 specialization**（需 sm_100 `KernelTmaWarpSpecialized2SmNvf4Sm100`）。
275	
276	**结论**：R12 = **0 收益 dead-end**。**弃用**：显式 MainloopScheduleType / EpilogueScheduleType；"AUTO 可能选错"假设。
277	
278	### S.1 R12-replacement candidate — 加新 CUTLASS tile shape
279	
280	`fp4_gemm_cutlass_sm120.jinja:23` 是 jinja 模板，(cta_m,cta_n,cta_k) 可填；`CutlassTileConfigSM120` 已声明 7 valid tile，flashinfer 只用 3 个；4 unused tile 在 SM120_16x8x64_TN_VS atom 下倍数/对齐通过。
281	
282	**为什么不实施（与 §R 同模式）**：ROI 上限边际（R-prefill-prewarm 实测 6-tactic 全 ≤ 3% margin → 新 tile 预期 e2e ≤ 1-2%）；**§6.2 停手信号 #1 已触发**（近 4 轮无突破）；Build cost 极高（JIT rebuild 4 tile × 2 dtype × 2 scheduler = 3-8h；AOT 替换协议未跑通；autotune cache schema 升级）；K=64 stage carveout 未验证（SF block 16 + K=64 = 4 SF chunks 可能 < sm_120 min K-tile）。
283	
284	**复活条件**：§6.2 reset；JIT rebuild 协议跑通；找到 ≥ 5% e2e ROI 上限的具体 hot shape gap。
285	
286	---
287	
288	## T. R-b12x-buffer-reuse — b12x output tensor 复用 pool：alloc overhead 实证 < 1µs/call 无攻击面（2026-05-11）
289	
290	**假设**：`b12x_fp4.py:489` 每 call `torch.empty((M, N))` per-call alloc 是 §P R-b12x-prefill 退化的候选根因 (2)。bump `MAX_M=8192` 后 prefill M=2048-8192 输出 32-64MB，每 call alloc 可能 > 100µs；引入 (M_bucket, N, dtype, device) keyed pool 复用可消除该 overhead。
291	
292	**Patch**（已回滚 `git checkout --`）：`b12x_fp4.py` 加 `_OUTPUT_BUFFER_POOL` + `_get_output_buffer()`，env `SGLANG_B12X_BUFFER_REUSE` opt-in；cuda graph capture 内自动 fallback `torch.empty`（让 graph 接管 lifetime）；同 (M_bucket, N) 串行复用，slice 出精确 (M, N) view。
293	
294	**Microbench A/B**（`bench/b12x/measure_alloc_overhead.py`，REUSE=0 vs REUSE=1，200 iters/case）：
295	
296	| case (N, K, M) | alloc_us | reuse_us | delta_us | delta% |
297	|---|---:|---:|---:|---:|
298	| std_o M=96 (4096, 4096, 96)     | 12.32 | 19.48 | -7.16 | -58% ⚠ 首 case 噪声 |
299	| std_qkv M=96 (4608, 4096, 96)   | 22.60 | 19.18 | +3.42 | +15% 单 case 离群 |
300	| down M=128 (4096, 16384, 128)   | 38.97 | 38.91 | +0.06 | +0.16% |
301	| gla_qkv M=128 (12288, 4096, 128)| 30.79 | 30.74 | +0.05 | +0.16% |
302	| eagle_fc M=128 (4096, 12288, 128)| 28.75 | 28.71 | +0.04 | +0.14% |
303	| std_o M=512 (4096, 4096, 512)   | 37.92 | 37.66 | +0.25 | +0.67% |
304	| **down M=8192 (4096, 16384, 8192) 输出 64MB** | **2018.83** | **2019.51** | **-0.68** | **-0.03%** |
305	
306	**核心证据**：down M=8192 (out 64 MB) 复用节省 **−0.68µs（−0.03%）** —— PyTorch CachingAllocator cached hit 路径对 64 MB 块开销已 ≤ 1µs；远小于 kernel wall 2 ms。decode 路径 5 case 全部 delta_us < +0.3µs（噪声），无 reuse 价值。
307	
308	**§P 候选根因 (2) 推翻**：§P R-b12x-prefill mini_bench S1 退化 +25s（129→155）单靠 alloc 不可能解释——最坏情况几百 b12x calls × 1µs = 几 ms 数量级，与 25s 退化差 4 个量级。**§P 真因仍未定位**，剩余候选：cache thrash / stream-sync / SF pattern 与 production 权重互动（**不**是 alloc）。
309	
310	**为什么不进 e2e gate**：microbench 已证 ROI = 0；mini_bench 三档不可能显示正向收益（patch 只 reorder host-side 路径，不动 GPU kernel）；按 SOP §0 "每改动必须 attribute SOL gap 缩小"——本 patch 无可 attribute gap，不应消耗 e2e gate budget。**直接 ROLLBACK，不进 D.3-D.5**。
311	
312	**SOP 教训**：
313	1. **wrapper-level host overhead 优化必须先 microbench 量化 baseline overhead**——`measure_dispatch_overhead.py` 已证 wrapper Python overhead < 5µs（§P 已知），alloc 是其子项更小，本应直接得出"无攻击面"结论而非动手实施 patch。
314	2. **PyTorch CachingAllocator cached hit ≤ 1µs/call**（即使 64 MB 块）是已知性质，应作为常数表 §G 补充——任何"减少 alloc"假设都先按此 quick-reject。
315	3. **§P 真因排查应按物理量级匹配**：25s 退化必然对应每 decode iter 数百 µs 级 stable overhead 或 cache thrashing，alloc <1µs/call × 数百 call/iter = 几 ms × 数千 iter = 几 s 数量级不够。
316	
317	**弃用**：
318	- 任何"b12x wrapper torch.empty alloc 是 hot overhead"假设
319	- 任何不先 microbench host overhead 量级就动手的 wrapper-level reuse patch
320	- 把"PyTorch alloc"作为 GEMM dispatch 路径退化候选根因（不再列入 §P 剩余候选）
321	
322	**复活条件**：
323	- 测得 production trace 中 `cudaMalloc`/`cudaFreeAsync` 占比 ≥ 1% wall（当前未测）
324	- 或 §P 真因被定位为 alloc 类（基于物理量级不太可能）
325	- 或迁移到 non-CachingAllocator 路径（如 cuda graph 外的 trtllm pool / 自管 arena）
326	
327	**artifacts**：
328	- `bench/b12x/measure_alloc_overhead.py`（保留，作为 alloc baseline reference 工具）
329	- `outputs/alloc_overhead_dead-end_breuse_20260511_111846.log`
330	- 回滚 commit：`git checkout -- demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`
331	
332	---
333	
334	## U. R-b12x-kernel-internal — b12x sm_120 kernel 内部 `ab_stage` cap=4 已是经验最优（2026-05-11）
335	
336	**假设**：`Sm120BlockScaledDenseGemmKernel._compute_stages` 末尾 `ab_stage = max(1, min(ab_stage, 4))` 是 b12x 从上游 CUTLASS sm_100 reference 移植时加的人为 cap。上游 flashinfer sm_100 reference (`flashinfer/gemm/kernels/dense_blockscaled_gemm_sm100.py:1811`) 无此 cap，纯按 SMEM/occupancy 自动计算。预期解除 cap 后 mainloop pipeline 加深 → TMA load 与 MMA 计算更好 overlap → kernel 提速 5-15%。
337	
338	**SMEM 量化**（sm_120 SMEM=101376 bytes, `mbar_helpers=1024`, `epi_stage=1`, occupancy=1）：
339	
340	| tile (M,N,K) | A bytes/stage | B bytes/stage | epi bytes | ab_stage 自然解 | cap=4 解 | cap=8 解 | 多用 SMEM (KB) |
341	|---|---:|---:|---:|---:|---:|---:|---:|
342	| (64,  64,128) | 4096 | 4096 |  8192 | ~8.9 → 8 | 4 | 8 | +40 |
343	| (64, 128,128) | 4096 | 8192 | 16384 | ~5.8 → 5 | 4 | 5 | +14 |
344	| (128,128,128) | 8192 | 8192 | 32768 | ~3.6 → 3 | 3 (SMEM bound) | 3 | 0 |
345	
346	**实证否决**（`bench/b12x/diag_ab_stage_cap.py`，5 prefill shapes × M=8192 × 200 iters × 3 trials）：
347	
348	| shape | tile | ab_stage 4→8 | ms default | ms cap=8 | Δ% | n_σ |
349	|---|---|---:|---:|---:|---:|---:|
350	| std_o   | (64,64)  | 4→**8** | 0.5054 | 0.5052 | **+0.04%** | -1.4 |
351	| std_qkv | (64,64)  | 4→**8** | 0.5716 | 0.5715 | **+0.00%** | -0.04 |
352	| gla_qkv | (64,128) | 4→**5** | 1.5018 | 1.5015 | **+0.02%** | -0.3 |
353	| gate_up | (64,128) | 4→**5** | 3.9756 | 3.9724 | **+0.08%** | -1.7 |
354	| down    | (64,64)  | 4→**8** | 2.0188 | 2.0159 | **+0.14%** | -3.0 |
355	
356	**关键结论**：
357	1. **最大 Δ = +0.14%（down，8 stages 实际生效）**，3σ statistically significant 但**绝对数值 = 3 µs / 2018 µs**，工程上 ROI = 0。
358	2. **std_o / std_qkv / gate_up Δ ≤ 0.1% 全噪声层** — 4 stages 已饱和 TMA→MMA pipeline；多 stage 只占用 SMEM 不加速。
359	3. **bit-exact 确认**（`bench/b12x/diag_ab_stage_cap_correct.py`，valid SF + valid weights）：max_abs_diff = 0.0；sentinel zeros 检查通过 — **无 §Q 类越界写风险**。
360	
361	**为什么 4 stages 已饱和**：sm_120 GeForce 在 NVFP4 BlockScaled 上 TMA-load → SMEM → MMA 的 issue rate 在 ~4-stage depth 已经能 hide HBM latency。增加到 8 stage 只是 SMEM 多占，pipeline barriers 多，consumer 仍在等 producer issue 同样的 K-tile work — 没有额外 overlap 机会。这与上游 sm_100 SMEM 远大（228KB）、stage 可上到 7-8 不同：**sm_120 是 GeForce SKU，SMEM 小，cap=4 已是上限-下限均衡点**。
362	
363	**SOP §A 6 问验证**：
364	- (1) GEMM kernel internal — 命中
365	- (2) 影响 mainloop pipeline depth → TMA/MMA overlap
366	- (3) 一阶（直接改 kernel SMEM 分配）
367	- (4) **假设 5-15% 提速 — 实证 +0.14% 上限，10× 量级低估**
368	- (5) attribute 到任何 sol_table gap：5 shapes 现 TF/s = 541-554（sm_120 NVFP4 peak ~1000 TF/s → SOL ~54%），有 gap 但本路径不能砍
369	- (6) 验证：correctness pass / 性能 < 1% → 不进 e2e gate
370	
371	**弃用**：
372	- "lift kernel SMEM/stage cap 必然提速" 假设；
373	- "上游 sm_100 reference 不加 cap → sm_120 也该解 cap" 反推；
374	- 任何"b12x mainloop pipeline depth 不够"假设（4 stages 在 sm_120 GeForce 上充足）。
375	
376	**复活条件**：
377	- 迁到 SMEM 更大的 SKU（sm_120 Pro Plus 等，若存在）；
378	- 找到新的硬件级低效证据（ncu mainloop_pipeline_stalled_cycles > 30%）— 当前未测；
379	- 改 kernel 引入新的 fusion（例如 EVT 加 SiLU），改变 SMEM 预算结构。
380	
381	**occupancy=1 派生候选**（`self.occupancy = 1` hardcoded line 114）：bump occupancy=2 也无攻击面。理由：occupancy=2 时 SMEM/2 = ~50KB/CTA，ab_stage 退到 3（更浅 pipeline），同时 reg 压力翻倍（288 thread/CTA × 2 = 576 thread/SM，每 thread reg 上限从 227 降到 113，b12x kernel 实测 reg 用量约 96-120 — 边界风险高）。**预期收益 ≤ ab_stage 实验的 +0.14%，风险高于收益**，未实施。
382	
383	**artifacts**：
384	- `bench/b12x/diag_ab_stage_cap.py`（保留，作为 b12x kernel internal 验证工具）
385	- `bench/b12x/diag_ab_stage_cap_correct.py`（valid-SF bit-exact 校验）
386	- `bench/b12x/diag_ab_stage_cap.json`
387	- 无 patch、无 rebuild、无 .so 替换需要（试探用独立 cache 路径 `/tmp/cute_dsl_cache_diag_stagecap`）
388	
389	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 sol_table 和 gptq_marlin_gemm 的函数签名：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/sol_table.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# Stage 2 — SOL 表（54 个 (shape, M) 物理下限）
2	
3	按 [methodology.md](methodology.md) §3 cost model + [hardware.md](hardware.md) §1 实测常数算出。**这是攻击优先级的物理依据——不知道距离物理上限多远就不知道何时停**。
4	
5	---
6	
7	## 0. 算法
8	
9	```
10	AI = FLOPs / Bytes_moved_from_DRAM
11	T_compute_LB = FLOPs / peak_FLOPS_dtype
12	T_mem_LB    = Bytes_traffic / BW_HBM
13	T_kernel_LB = max(T_compute_LB, T_mem_LB)
14	SOL%        = T_kernel_LB / T_measured  (>80% = 够好)
15	```
16	
17	## 1. 硬件常数（来自 [hardware.md](hardware.md)）
18	
19	| 常数 | 值 | 出处 |
20	|---|---|---|
21	| N_SM | 156 | `p.multi_processor_count` |
22	| f_clk | 2.43 GHz | `nvidia-smi clocks.max.graphics` |
23	| Peak NVFP4 unscaled | 1467 TFLOPS | [kernels-sm120.md §2](kernels-sm120.md) `pure_mma_peak` |
24	| Peak NVFP4 **scaled** | **489 TFLOPS** | unscaled / 3（block-scaled mma ISA 硬开销）|
25	| BW_HBM 实测 SOL | **1.4 TB/s**（保守 SOL） | 理论 1.5 × 90%（GDDR7 448-bit @ 12481 MHz）|
26	| W_BYTES_PER_ELEM | 0.5625 byte | NVFP4: 0.5 byte FP4 + 1 byte e4m3 / 16 elem |
27	| A_BYTES_PER_ELEM | 2.0 byte | bf16 activation |
28	| C_BYTES_PER_ELEM | 2.0 byte | bf16 output |
29	
30	> 本表用 BW_HBM=1.4 TB/s（保守 SOL）。保守版 T_mem_LB 偏大，意味着实测 SOL% 看起来更高——避免"乐观估算 SOL 永远达不到"反模式。
31	> **SOL > 100% (❄)** 解释：cost model 简化无 reuse 系数，weight stationary + L2 命中能让 wall-time < T_mem_LB。详见 [methodology.md §3.0bis](methodology.md)。
32	
33	## 2. SOL 表（54 行）
34	
35	| shape | N | K | M | regime | AI | bound | T_compute_LB µs | T_mem_LB µs | T_kernel_LB µs | target SOL% |
36	|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|
37	| **gate_up_proj** | 32768 | 4096 | 1 | M=1 (decode) | 3.6 | mem | 0.55 | 53.98 | **53.98** | 80% |
38	| gate_up_proj | 32768 | 4096 | 8 | small batch | 28.2 | mem | 4.39 | 54.35 | 54.35 | 75% |
39	| gate_up_proj | 32768 | 4096 | 16 | small batch | 56.0 | mem | 8.78 | 54.77 | 54.77 | 75% |
40	| gate_up_proj | 32768 | 4096 | 32 | small batch | 110.3 | mem | 17.57 | 55.61 | 55.61 | 75% |
41	| gate_up_proj | 32768 | 4096 | 48 | small batch | 163.0 | mem | 26.35 | 56.45 | 56.45 | 75% |
42	| gate_up_proj | 32768 | 4096 | 128 | transition | 404.5 | **compute** | 70.27 | 60.67 | 70.27 | 75% |
43	| gate_up_proj | 32768 | 4096 | 256 | transition | 728.2 | compute | 140.53 | 67.41 | 140.53 | 75% |
44	| gate_up_proj | 32768 | 4096 | 2048 | prefill | 2427.3 | compute | 1124.25 | 161.78 | 1124.25 | 80% |
45	| gate_up_proj | 32768 | 4096 | 8192 | prefill | 3236.3 | compute | 4496.98 | 485.34 | **4496.98** | 80% |
46	| **down_proj** | 4096 | 16384 | 1 | M=1 (decode) | 3.6 | mem | 0.27 | 26.99 | **26.99** | 80% |
47	| down_proj | 4096 | 16384 | 8 | small batch | 28.2 | mem | 2.20 | 27.20 | 27.20 | 75% |
48	| down_proj | 4096 | 16384 | 16 | small batch | 55.9 | mem | 4.39 | 27.43 | 27.43 | 75% |
49	| down_proj | 4096 | 16384 | 32 | small batch | 110.0 | mem | 8.78 | 27.90 | 27.90 | 75% |
50	| down_proj | 4096 | 16384 | 48 | small batch | 162.2 | mem | 13.17 | 28.37 | 28.37 | 75% |
51	| down_proj | 4096 | 16384 | 128 | transition | 399.6 | compute | 35.13 | 30.71 | 35.13 | 75% |
52	| down_proj | 4096 | 16384 | 256 | transition | 712.3 | compute | 70.27 | 34.45 | 70.27 | 75% |
53	| down_proj | 4096 | 16384 | 2048 | prefill | 2259.9 | compute | 562.12 | 86.88 | 562.12 | 80% |
54	| down_proj | 4096 | 16384 | 8192 | prefill | 2945.4 | compute | 2248.49 | 266.64 | 2248.49 | 80% |
55	| **qkv_proj_std** | 4608 | 4096 | 1 | M=1 (decode) | 3.5 | mem | 0.08 | 7.60 | **7.60** | 80% |
56	| qkv_proj_std | 4608 | 4096 | 8 | small batch | 28.1 | mem | 0.62 | 7.68 | 7.68 | 75% |
57	| qkv_proj_std | 4608 | 4096 | 16 | small batch | 55.4 | mem | 1.24 | 7.78 | 7.78 | 75% |
58	| qkv_proj_std | 4608 | 4096 | 32 | small batch | 108.1 | mem | 2.47 | 7.98 | 7.98 | 75% |
59	| qkv_proj_std | 4608 | 4096 | 48 | small batch | 158.2 | mem | 3.71 | 8.18 | 8.18 | 75% |
60	| qkv_proj_std | 4608 | 4096 | 128 | transition | 376.2 | compute | 9.88 | 9.18 | 9.88 | 75% |
61	| qkv_proj_std | 4608 | 4096 | 256 | transition | 641.1 | compute | 19.76 | 10.77 | 19.76 | 75% |
62	| qkv_proj_std | 4608 | 4096 | 2048 | prefill | 1670.9 | compute | 158.10 | 33.05 | 158.10 | 80% |
63	| qkv_proj_std | 4608 | 4096 | 8192 | prefill | 2018.2 | compute | 632.39 | 109.45 | 632.39 | 80% |
64	| **o_proj_std** | 4096 | 4096 | 1 | M=1 (decode) | 3.5 | mem | 0.07 | 6.75 | **6.75** | 80% |
65	| o_proj_std | 4096 | 4096 | 8 | small batch | 28.1 | mem | 0.55 | 6.83 | 6.83 | 75% |
66	| o_proj_std | 4096 | 4096 | 16 | small batch | 55.4 | mem | 1.10 | 6.93 | 6.93 | 75% |
67	| o_proj_std | 4096 | 4096 | 32 | small batch | 107.8 | mem | 2.20 | 7.12 | 7.12 | 75% |
68	| o_proj_std | 4096 | 4096 | 48 | small batch | 157.5 | mem | 3.29 | 7.30 | 7.30 | 75% |
69	| o_proj_std | 4096 | 4096 | 128 | transition | 372.4 | compute | 8.78 | 8.24 | 8.78 | 75% |
70	| o_proj_std | 4096 | 4096 | 256 | transition | 630.2 | compute | 17.57 | 9.74 | 17.57 | 75% |
71	| o_proj_std | 4096 | 4096 | 2048 | prefill | 1598.4 | compute | 140.53 | 30.71 | 140.53 | 80% |
72	| o_proj_std | 4096 | 4096 | 8192 | prefill | 1913.5 | compute | 562.12 | 102.61 | 562.12 | 80% |
73	| **gla_qkv_proj** | 12288 | 4096 | 1 | M=1 (decode) | 3.6 | mem | 0.21 | 20.25 | **20.25** | 80% |
74	| gla_qkv_proj | 12288 | 4096 | 8 | small batch | 28.2 | mem | 1.65 | 20.41 | 20.41 | 75% |
75	| gla_qkv_proj | 12288 | 4096 | 16 | small batch | 55.9 | mem | 3.29 | 20.60 | 20.60 | 75% |
76	| gla_qkv_proj | 12288 | 4096 | 32 | small batch | 109.7 | mem | 6.59 | 20.97 | 20.97 | 75% |
77	| gla_qkv_proj | 12288 | 4096 | 48 | small batch | 161.7 | mem | 9.88 | 21.35 | 21.35 | 75% |
78	| gla_qkv_proj | 12288 | 4096 | 128 | transition | 396.4 | compute | 26.35 | 23.22 | 26.35 | 75% |
79	| gla_qkv_proj | 12288 | 4096 | 256 | transition | 702.2 | compute | 52.70 | 26.21 | 52.70 | 75% |
80	| gla_qkv_proj | 12288 | 4096 | 2048 | prefill | 2160.5 | compute | 421.59 | 68.16 | 421.59 | 80% |
81	| gla_qkv_proj | 12288 | 4096 | 8192 | prefill | 2778.9 | compute | 1686.37 | 211.96 | 1686.37 | 80% |
82	| **eagle_fc** | 4096 | 12288 | 1 | M=1 (decode) | 3.6 | mem | 0.21 | 20.25 | **20.25** | 80% |
83	| eagle_fc | 4096 | 12288 | 8 | small batch | 28.2 | mem | 1.65 | 20.41 | 20.41 | 75% |
84	| eagle_fc | 4096 | 12288 | 16 | small batch | 55.9 | mem | 3.29 | 20.60 | 20.60 | 75% |
85	| eagle_fc | 4096 | 12288 | 32 | small batch | 109.7 | mem | 6.59 | 20.97 | 20.97 | 75% |
86	| eagle_fc | 4096 | 12288 | 48 | small batch | 161.7 | mem | 9.88 | 21.35 | 21.35 | 75% |
87	| eagle_fc | 4096 | 12288 | 128 | transition | 396.4 | compute | 26.35 | 23.22 | 26.35 | 75% |
88	| eagle_fc | 4096 | 12288 | 256 | transition | 702.2 | compute | 52.70 | 26.21 | 52.70 | 75% |
89	| eagle_fc | 4096 | 12288 | 2048 | prefill | 2160.5 | compute | 421.59 | 68.16 | 421.59 | 80% |
90	| eagle_fc | 4096 | 12288 | 8192 | prefill | 2778.9 | compute | 1686.37 | 211.96 | 1686.37 | 80% |
91	
92	## 3. 关键观察
93	
94	**regime 边界**：6 形状均在 **M=128 附近** 从 mem-bound 反转到 compute-bound（AI 跨过 machine balance ≈ 349 ops/byte）。M ≤ 64 全 mem-bound，M ≥ 128 全 compute-bound。
95	
96	**`SGLANG_MARLIN_DECODE_THRESHOLD=48` 物理依据**：M ≤ 48 weight-bound，Marlin 设计目标；M > 48 进入 transition / compute，CUTLASS NVFP4 占优。这是 regime 边界，不是经验值（具体 per-shape Marlin 阈值见 [kernels-sm120.md §7.4](kernels-sm120.md)）。
97	
98	---
99	
100	## 4. Stage 3 baseline 实测（2026-05-09，详见 `outputs/baseline/latest/baseline.md`）

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"gptq_marlin_gemm\" /user_4813494d/openbmb/demo-sala --include=\"*.py\" | head -5"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/bench_downproj_marlin_vs_cutlass.py:    marlin path  = bf16 input → gptq_marlin_gemm (W4A16)      → bf16 output
/user_4813494d/openbmb/demo-sala/verify_env.py:    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp8.py:    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp8.py:    output = gptq_marlin_gemm(
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py:    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
```

> AGENT

最后检查 marlin_utils_fp8 和查看 gptq_marlin_gemm 的具体参数：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp8.py"
}
```

> TOOL

tool_result Read
```
1	# SPDX-License-Identifier: Apache-2.0
2	
3	import logging
4	from typing import Optional
5	
6	import torch
7	
8	from sglang.srt.layers.quantization.marlin_utils import (
9	    USE_FP32_REDUCE_DEFAULT,
10	    marlin_make_workspace,
11	    marlin_permute_bias,
12	    marlin_permute_scales,
13	    should_use_atomic_add_reduce,
14	)
15	from sglang.srt.layers.quantization.utils import get_scalar_types
16	from sglang.srt.utils import is_cuda
17	
18	_is_cuda = is_cuda()
19	if _is_cuda:
20	    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
21	
22	ScalarType, scalar_types = get_scalar_types()
23	
24	logger = logging.getLogger(__name__)
25	
26	
27	def fp8_fused_exponent_bias_into_scales(scales):
28	    fp8_exponent = 4
29	    if scales.dtype == torch.half:
30	        target_exponent = 5
31	    elif scales.dtype == torch.bfloat16:
32	        target_exponent = 8
33	    # exponent_bias_fp16 = 2 ** 4 - 2 ** 3 = 8
34	    # exponent_bias_bf16 = 2 ** 7 - 2 ** 3 = 120
35	    exponent_bias = 2 ** (target_exponent - 1) - 2 ** (fp8_exponent - 1)
36	    s = torch.ones_like(scales) * 2
37	    s = s**exponent_bias
38	    return scales * s
39	
40	
41	def apply_fp8_marlin_linear(
42	    input: torch.Tensor,
43	    weight: torch.Tensor,
44	    weight_scale: torch.Tensor,
45	    workspace: torch.Tensor,
46	    size_n: int,
47	    size_k: int,
48	    bias: Optional[torch.Tensor],
49	    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
50	) -> torch.Tensor:
51	    # For GPUs that lack FP8 hardware support, we can leverage the
52	    # Marlin kernel for fast weight-only FP8 quantization
53	
54	    reshaped_x = input.reshape(-1, input.shape[-1])
55	    out_shape = input.shape[:-1] + (size_n,)
56	
57	    use_atomic_add = should_use_atomic_add_reduce(
58	        m=reshaped_x.size(0), n=size_n, k=size_k, device=input.device, dtype=input.dtype
59	    )
60	
61	    output = gptq_marlin_gemm(
62	        a=reshaped_x,
63	        c=None,
64	        b_q_weight=weight,
65	        b_scales=weight_scale,
66	        global_scale=None,
67	        b_zeros=None,
68	        g_idx=None,
69	        perm=None,
70	        workspace=workspace,
71	        b_q_type=scalar_types.float8_e4m3fn,
72	        size_m=reshaped_x.size(0),
73	        size_n=size_n,
74	        size_k=size_k,
75	        use_atomic_add=use_atomic_add,
76	        use_fp32_reduce=use_fp32_reduce,
77	    )
78	
79	    if bias is not None:
80	        output.add_(bias)
81	
82	    return output.reshape(out_shape)
83	
84	
85	def prepare_fp8_layer_for_marlin(
86	    layer: torch.nn.Module, size_k_first: bool = True
87	) -> None:
88	    logger.warning_once(
89	        "Your GPU does not have native support for FP8 computation but "
90	        "FP8 quantization is being used. Weight-only FP8 compression will "
91	        "be used leveraging the Marlin kernel. This may degrade "
92	        "performance for compute-heavy workloads."
93	    )
94	
95	    part_size_n = layer.output_size_per_partition
96	    part_size_k = layer.input_size_per_partition
97	    weight_block_size = getattr(layer, "weight_block_size", None)
98	
99	    if size_k_first:
100	        assert layer.weight.shape == (part_size_k, part_size_n)
101	    else:
102	        assert layer.weight.shape == (part_size_n, part_size_k)
103	
104	    device = layer.weight.device
105	
106	    # WORKSPACE
107	    layer.workspace = marlin_make_workspace(device)
108	
109	    # WEIGHT
110	    # Repack weights to marlin format
111	    perm = torch.empty(0, dtype=torch.int, device=device)
112	    qweight = pack_fp8_to_int32(layer.weight, size_k_first)
113	    if not size_k_first:
114	        qweight = qweight.T.contiguous()
115	
116	    marlin_qweight = gptq_marlin_repack(
117	        b_q_weight=qweight,
118	        perm=perm,
119	        size_k=part_size_k,
120	        size_n=part_size_n,
121	        num_bits=8,
122	    )
123	    layer.weight = torch.nn.Parameter(marlin_qweight, requires_grad=False)
124	
125	    # WEIGHT SCALES
126	    # Permute scales
127	    if "weight_scale" in dir(layer):
128	        scales = layer.weight_scale.to(layer.orig_dtype)
129	    elif "weight_scale_inv" in dir(layer):
130	        scales = layer.weight_scale_inv.to(layer.orig_dtype)
131	        del layer.weight_scale_inv
132	
133	    group_size = -1 if weight_block_size is None else weight_block_size[1]
134	
135	    # marlin kernel only support channel-wise and group-wise quantization
136	    # we need to convert the scales
137	    if weight_block_size is None:
138	        if scales.nelement() == 1:
139	            # tensor-wise quantization -> channel-wise quantization
140	            # (1, 1) =>(repeat)=> (1, size_n)
141	            scales = scales.view(1, 1).repeat_interleave(part_size_n, 1)
142	        elif scales.nelement() > 1 and scales.nelement() != part_size_n:
143	            assert part_size_n % scales.nelement() == 0
144	            s_size = scales.nelement()
145	            # tensor-wise quantization (for gate-up proj)
146	            #     -> channel-wise quantization
147	            # (1, s_size) =>(repeat)=> (1, size_n)
148	            scales = scales.view(1, s_size)
149	            scales = scales.repeat_interleave(part_size_n // s_size, 1)
150	        else:
151	            # channel-wise quantization
152	            # (1, size_n)
153	            scales = scales.view(1, part_size_n)
154	    else:
155	        # block-wise quantization -> group-wise quantization
156	        # (size_k // block_size[1], ceil(size_n / block_size[0]))
157	        #  =>(repeat)=> (size_k // block_size[1], size_n)
158	        if not size_k_first:
159	            scales = scales.T.contiguous()
160	        block_n = weight_block_size[0]
161	        scales = scales.repeat_interleave(block_n, 1)
162	        # size_n may not divisible by block_size[0]
163	        scales = scales[:, :part_size_n]
164	
165	    marlin_scales = marlin_permute_scales(
166	        s=scales, size_k=part_size_k, size_n=part_size_n, group_size=group_size
167	    )
168	    marlin_scales = fp8_fused_exponent_bias_into_scales(marlin_scales)
169	    layer.weight_scale = torch.nn.Parameter(marlin_scales, requires_grad=False)
170	
171	    if hasattr(layer, "bias") and layer.bias is not None:
172	        assert layer.bias.shape == (part_size_n,)
173	        bias = marlin_permute_bias(layer.bias)
174	        layer.bias = torch.nn.Parameter(bias, requires_grad=False)
175	
176	
177	def prepare_moe_fp8_layer_for_marlin(
178	    layer: torch.nn.Module, size_k_first: bool = True
179	) -> None:
180	    logger.warning_once(
181	        "Your GPU does not have native support for FP8 computation but "
182	        "FP8 quantization is being used. Weight-only FP8 compression will "
183	        "be used leveraging the Marlin kernel. This may degrade "
184	        "performance for compute-heavy workloads."
185	    )
186	
187	    e = layer.num_experts
188	    k = layer.hidden_size
189	    n = layer.intermediate_size_per_partition
190	    weight_block_size = getattr(layer, "weight_block_size", None)
191	
192	    # WORKSPACE
193	    device = layer.w13_weight.device
194	    layer.workspace = marlin_make_workspace(device, 4)
195	    perm = torch.empty(0, dtype=torch.int, device=device)
196	
197	    # WEIGHT
198	    # Repack weights to marlin format
199	    for name in ["w13_weight", "w2_weight"]:
200	        weight = getattr(layer, name)
201	        tensor_list = []
202	        if "w13" in name:
203	            size_n, size_k = n * 2, k
204	        else:
205	            size_n, size_k = k, n
206	
207	        if size_k_first:
208	            assert weight.shape == (e, size_k, size_n)
209	        else:
210	            assert weight.shape == (e, size_n, size_k)
211	
212	        for i in range(e):
213	            qweight = pack_fp8_to_int32(weight[i], size_k_first)
214	            if not size_k_first:
215	                qweight = qweight.T.contiguous()
216	
217	            marlin_qweight = gptq_marlin_repack(
218	                b_q_weight=qweight, perm=perm, size_k=size_k, size_n=size_n, num_bits=8
219	            )
220	            tensor_list.append(marlin_qweight)
221	
222	        weight = torch.cat([x.unsqueeze(0) for x in tensor_list], 0)
223	        weight = torch.nn.Parameter(weight, requires_grad=False)
224	
225	        setattr(layer, name, weight)
226	
227	    # WEIGHT SCALES
228	    # Permute scales
229	    group_size = -1 if weight_block_size is None else weight_block_size[1]
230	
231	    for name in ["w13", "w2"]:
232	        if name + "_weight_scale" in dir(layer):
233	            new_name = name + "_weight_scale"
234	            scales = getattr(layer, new_name).to(layer.orig_dtype)
235	            delattr(layer, new_name)
236	        elif name + "_weight_scale_inv" in dir(layer):
237	            new_name = name + "_weight_scale_inv"
238	            scales = getattr(layer, new_name).to(layer.orig_dtype)
239	            delattr(layer, new_name)
240	
241	        tensor_list = []
242	        if "w13" in name:
243	            size_n, size_k = n * 2, k
244	        else:
245	            size_n, size_k = k, n
246	
247	        # marlin kernel only support channel-wise and group-wise quantization
248	        # we need to convert the scales
249	        if weight_block_size is None:
250	            if scales.nelement() == e:
251	                # tensor-wise quantization -> channel-wise quantization
252	                # (e, 1, 1) =>(repeat)=> (e, 1, size_n)
253	                scales = scales.view(e, 1, 1).repeat_interleave(size_n, 2)
254	            elif scales.nelement() > e and scales.nelement() != e * size_n:
255	                assert (e * size_n) % scales.nelement() == 0
256	                s_size = scales.nelement() // e
257	                # tensor-wise quantization (for gate-up proj)
258	                #     -> channel-wise quantization
259	                # (e, 1, s_size) =>(repeat)=> (e, 1, size_n)
260	                scales = scales.view(e, 1, s_size)
261	                scales = scales.repeat_interleave(size_n // s_size, 2)
262	            else:
263	                # channel-wise quantization
264	                # (e, 1, size_n)
265	                scales = scales.view(e, 1, size_n)
266	        else:
267	            # block-wise quantization -> group-wise quantization
268	            # (e, size_k // block_size[1], ceil(size_n / block_size[0]))
269	            #  =>(repeat)=> (e, size_k // block_size[1], size_n)
270	            if not size_k_first:
271	                scales = scales.permute(0, 2, 1)
272	            block_n = weight_block_size[0]
273	            scales = scales.repeat_interleave(block_n, 2)
274	            # size_n may not divisible by block_size[0]
275	            scales = scales[..., :size_n].contiguous()
276	
277	        for i in range(e):
278	            marlin_scales = marlin_permute_scales(
279	                s=scales[i], size_k=size_k, size_n=size_n, group_size=group_size
280	            )
281	            tensor_list.append(marlin_scales)
282	
283	        scales = torch.cat([x.unsqueeze(0) for x in tensor_list], 0)
284	        scales = fp8_fused_exponent_bias_into_scales(scales)
285	        scales = torch.nn.Parameter(scales, requires_grad=False)
286	
287	        setattr(layer, name + "_weight_scale", scales)
288	
289	    # BIAS
290	    # Permute bias
291	    for name in ["w13_bias", "w2_bias"]:
292	        if not hasattr(layer, name):
293	            continue
294	        bias = getattr(layer, name).to(layer.orig_dtype)
295	
296	        tensor_list = []
297	        for i in range(e):
298	            expert_bias = bias[i]
299	
300	            tensor_list.append(marlin_permute_bias(expert_bias))
301	
302	        bias = torch.cat([x.unsqueeze(0) for x in tensor_list], 0)
303	        bias = torch.nn.Parameter(bias, requires_grad=False)
304	        setattr(layer, name, bias)
305	
306	
307	def pack_fp8_to_int32(
308	    fp8_tensor: torch.Tensor, size_k_first: bool = True
309	) -> torch.Tensor:
310	    """
311	    Repack FP8 weights to gptq format (packed int32 elements)
312	    """
313	    assert fp8_tensor.dtype == torch.float8_e4m3fn
314	    assert fp8_tensor.ndim == 2
315	
316	    fp8_tensor = fp8_tensor.T if size_k_first else fp8_tensor
317	    fp8_tensor = fp8_tensor.contiguous()
318	    # fp8_tensor is contiguous and have shape (N, K) now
319	    # with `.view(torch.int32)`, it become (N, K // 4)
320	    int32_tensor = fp8_tensor.view(torch.int32)
321	    return int32_tensor.T.contiguous() if size_k_first else int32_tensor
322	
323	
324	def marlin_quant_fp8_torch(weight, group_size):
325	    size_n, size_k = weight.shape
326	    device = weight.device
327	
328	    if group_size != -1:
329	        scales = weight.view(size_n, -1, group_size).abs().max(-1)[0] / 448
330	        repeated_scales = scales.repeat_interleave(group_size, 1)
331	        fp8_weight = (weight / repeated_scales).to(torch.float8_e4m3fn)
332	        weight_ref = fp8_weight.to(weight.dtype) * repeated_scales
333	    else:
334	        scales = weight.view(size_n, 1, group_size).abs().max(-1)[0] / 448
335	        repeated_scales = scales.repeat_interleave(size_k, 1)
336	        fp8_weight = (weight / repeated_scales).to(torch.float8_e4m3fn)
337	        weight_ref = fp8_weight.to(weight.dtype) * repeated_scales
338	
339	    packed_weight = pack_fp8_to_int32(fp8_weight, False).T.contiguous()
340	    marlin_qweight = gptq_marlin_repack(
341	        b_q_weight=packed_weight,
342	        perm=torch.empty(0, dtype=torch.int, device=device),
343	        size_k=size_k,
344	        size_n=size_n,
345	        num_bits=8,
346	    )
347	
348	    marlin_scales = marlin_permute_scales(
349	        s=scales.T, size_k=size_k, size_n=size_n, group_size=group_size
350	    )
351	
352	    marlin_scales = fp8_fused_exponent_bias_into_scales(marlin_scales)
353	
354	    return weight_ref.T, marlin_qweight, marlin_scales
355	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 30 \"def apply_fp4_marlin_linear\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py | head -40"
}
```

> TOOL

tool_result Bash
```
def apply_fp4_marlin_linear(
    input: torch.Tensor,
    weight: torch.Tensor,
    weight_scale: torch.Tensor,
    weight_global_scale: Optional[torch.Tensor],
    workspace: torch.Tensor,
    size_n: int,
    size_k: int,
    bias: Optional[torch.Tensor] = None,
    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
) -> torch.Tensor:
    """通过 Marlin kernel 执行 FP4 量化 linear（非 Blackwell fallback）。"""
    reshaped_x = input.reshape(-1, input.shape[-1])
    out_shape = input.shape[:-1] + (size_n,)

    use_atomic_add = should_use_atomic_add_reduce(
        m=reshaped_x.size(0),
        n=size_n,
        k=size_k,
        device=input.device,
        dtype=input.dtype,
    )

    output = gptq_marlin_gemm(
        a=reshaped_x,
        c=None,
        b_q_weight=weight,
        b_scales=weight_scale,
        global_scale=weight_global_scale.reshape(-1),
        b_zeros=None,
        g_idx=None,
```

> AGENT

完美！现在我有了全面的信息。让我生成总结。

## 总结

**当前 Marlin NVFP4 精度模式确认：**

1. **NVFP4 是 A16 模式（fp16/bf16 activation）**，不是 A8。
   - `marlin_utils_fp4.py:149-165` 中 `gptq_marlin_gemm()` 调用：activation 是 `reshaped_x`（input tensor，dtype 为 bf16），weight 是 `scalar_types.float4_e2m1f`，output 也是 bf16——典型 W4A16 架构。
   - Weight scales 在 FP8-S0E5M3 格式（`nvfp4_marlin_process_scales` 第 109 行），global_scale 在 bf16/fp16（第 226 行）。

2. **不存在 NVFP4 A8 Marlin kernel 支持**。
   - `dead-ends.md §E` 明确列举"native FP4 MMA / QuTLASS W4A4 替换"为 dead-end：`mma.kind=mxf4nvf4` 要求 A+B 都必须是 FP4，硬件限制。
   - `marlin_utils_fp4.py` 唯一路径就是 W4A16；配对的 `b12x_fp4.py` 是 W4A4（CUTLASS），M>48 才走。
   - sgl-kernel 上游无 A8 变体；vLLM marlin fork 也是 W4A16 设计。

3. **当前 decode 瓶颈数字**（M≤48 Marlin 路径）：
   - `sol_table.md` §2：gate_up M=1 理论下界 53.98µs，down_proj M=1 理论下界 26.99µs（mem-bound，AI≈3.6）。
   - `marlin.md §8`：S8 baseline 中 Marlin 总耗时 4.9ms/step（160 calls），平均 ~30.6µs/call — **接近 sol_table 理论下界**，已近 Pareto 最优。
   - 瓶颈在 CUDA core dequant（SASS 分析 HMMA:HFMA2=1:11，张量核空转），ROI<2%（`marlin.md §4`）。

**A8 可行性评估**：硬件 ISA 级不支持（PTX FP4 MMA 要求双侧 FP4），无路径。W4A16 已因 dequant 成为硬制约，提升空间属于内核级微优化而非量化精度档位调整。

---

**关键引用**：
- 架构确认：`marlin_utils_fp4.py:149-165`（W4A16 GEMM 签名）
- A8 dead-end：`dead-ends.md:47`（native FP4 MMA 无法用）
- decode 数字：`sol_table.md:37-50`（M≤48 理论下界）、`marlin.md:82-84`（S8 实测 4.9ms）
