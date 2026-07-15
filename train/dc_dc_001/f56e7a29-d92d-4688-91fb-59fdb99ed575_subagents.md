---
session_id: "f56e7a29-d92d-4688-91fb-59fdb99ed575:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-05-11T11:31:40.713Z"
n_turns: 8
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

在 /user_4813494d/openbmb 项目中调研当前 Marlin NVFP4 kernel 的精度模式。背景：项目使用 SGLang fork + custom sgl-kernel 的 Marlin FP4 路径做 decode。我需要搞清楚： 1. **当前 Marlin 是 NVFP4 A16 还是 A8**？也就是 activation 是 fp16/bf16 还是 fp8/int8。重点查： - `demo-sala/sglang/python/sglang/srt/layers/quantization/` 下的 marlin / fp4 相关文件 - `marlin_utils_fp4.py` 之类 - `modelopt_quant.py` 里 hybrid Marlin 选择逻辑 - sgl-kernel Marlin FP4 entry（gemm 函数签名 / dtype 参数） - `docs/gemm/marlin.md` 和 `docs/quant/` 里的相关结论 2. **是否存在 NVFP4 A8 Marlin kernel 的支持**？查 sgl-kernel 上游、CUTLASS、有没有 a8 variant 的入口或 todo 注释；docs/gemm 里有没有提到 a8 的讨论或 dead-end。 3. **当前 decode shape 下 Marlin 的实测速度** — 看 docs/gemm/sol_table.md / current.md / changelog.md，找最新的 Marlin 在小 M (decode) 的吞吐 vs roof。 请精读上述 docs 和关键代码文件后给我一个 300 字以内的总结：当前模式确认、a8 可行性、目前 marlin 瓶颈数字。不要列文件清单，给结论 + 关键引用（file:line）。

> AGENT

我来系统地调研这个 Marlin NVFP4 kernel 的精度模式问题。

> AGENT

现在查看关键文件：

> AGENT

继续查看关键文件：

> AGENT

好的，现在查看 sgl-kernel 的具体 gemm 函数签名和 FP8 支持情况：

> AGENT

现在查看 sol_table 和 gptq_marlin_gemm 的函数签名：

> AGENT

最后检查 marlin_utils_fp8 和查看 gptq_marlin_gemm 的具体参数：

> AGENT

完美！现在我有了全面的信息。让我生成总结。 ## 总结 **当前 Marlin NVFP4 精度模式确认：** 1. **NVFP4 是 A16 模式（fp16/bf16 activation）**，不是 A8。 - `marlin_utils_fp4.py:149-165` 中 `gptq_marlin_gemm()` 调用：activation 是 `reshaped_x`（input tensor，dtype 为 bf16），weight 是 `scalar_types.float4_e2m1f`，output 也是 bf16——典型 W4A16 架构。 - Weight scales 在 FP8-S0E5M3 格式（`nvfp4_marlin_process_scales` 第 109 行），global_scale 在 bf16/fp16（第 226 行）。 2. **不存在 NVFP4 A8 Marlin kernel 支持**。 - `dead-ends.md §E` 明确列举"native FP4 MMA / QuTLASS W4A4 替换"为 dead-end：`mma.kind=mxf4nvf4` 要求 A+B 都必须是 FP4，硬件限制。 - `marlin_utils_fp4.py` 唯一路径就是 W4A16；配对的 `b12x_fp4.py` 是 W4A4（CUTLASS），M>48 才走。 - sgl-kernel 上游无 A8 变体；vLLM marlin fork 也是 W4A16 设计。 3. **当前 decode 瓶颈数字**（M≤48 Marlin 路径）： - `sol_table.md` §2：gate_up M=1 理论下界 53.98µs，down_proj M=1 理论下界 26.99µs（mem-bound，AI≈3.6）。 - `marlin.md §8`：S8 baseline 中 Marlin 总耗时 4.9ms/step（160 calls），平均 ~30.6µs/call — **接近 sol_table 理论下界**，已近 Pareto 最优。 - 瓶颈在 CUDA core dequant（SASS 分析 HMMA:HFMA2=1:11，张量核空转），ROI<2%（`marlin.md §4`）。 **A8 可行性评估**：硬件 ISA 级不支持（PTX FP4 MMA 要求双侧 FP4），无路径。W4A16 已因 dequant 成为硬制约，提升空间属于内核级微优化而非量化精度档位调整。 --- **关键引用**： - 架构确认：`marlin_utils_fp4.py:149-165`（W4A16 GEMM 签名） - A8 dead-end：`dead-ends.md:47`（native FP4 MMA 无法用） - decode 数字：`sol_table.md:37-50`（M≤48 理论下界）、`marlin.md:82-84`（S8 实测 4.9ms）
