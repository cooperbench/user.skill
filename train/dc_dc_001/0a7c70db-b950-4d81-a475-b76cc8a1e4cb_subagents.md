> DEVELOPER

请深入分析 /user_4813494d/openbmb/kernels/infllmv2_cuda_impl 目录下的所有代码，寻找潜在的性能优化点。

背景：
- 这是 InfLLM-v2 稀疏注意力的 CUDA 实现，用于 MiniCPM-SALA 的长上下文推理
- 硬件：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM）
- CUDA toolkit 13.2，PyTorch 2.11.0+cu130，FlashInfer 0.6.8.post1
- standard Attention 层超过 dense_len=8192 时走 InfLLM-v2 稀疏（compress_k → stage1 block_score → stage2 top-K sparse FA）

请完整阅读：
1. 所有 .cu / .cuh / .cpp / .py 文件
2. 任何 CMakeLists.txt 或 setup.py
3. 头文件和接口定义

分析维度：
1. **算法层面**：计算流程是否有冗余？block_score 计算、top-K 选取、sparse FA 是否可以 fuse？
2. **内存访问**：global memory 访问模式是否 coalesced？有无不必要的 host↔device 拷贝？shared memory 利用率？
3. **并行度**：grid/block 配置是否合理？有无序列化的 bottleneck（如 atomics、synchronization）？
4. **sm_120 特性**：是否利用了 Blackwell 的 warp-group MMA、async copy、TMA？有无可以升级的旧接口？
5. **Python 绑定层**：有无可以消除的 Python overhead 或 tensor 拷贝？
6. **与 FlashInfer 的交互**：是否完全利用了 FlashInfer 的稀疏 attention API？有无绕路的地方？

请给出：
- 目录结构概览
- 每个优化点的：位置（文件:行号）、问题描述、预期收益（高/中/低）
- 最值得动手的前 3 个优化点（按 ROI 排序）

请尽量详细，搜索范围要 very thorough。

> AGENT

我将首先探索目录结构，然后系统地阅读所有源文件。

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -type f | sort",
  "description": "List all files in the infllmv2_cuda_impl directory"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/.gitignore
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/.gitmodules
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/README.md
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/entry.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/alibi.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/block_info.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/dropout.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim128_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim128_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim128_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim128_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim160_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim160_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim160_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim160_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim192_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim192_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim192_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim192_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim224_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim224_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim256_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim256_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim256_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim256_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim32_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim32_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim32_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim32_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim64_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim64_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim64_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim64_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim96_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim96_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim96_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_hdim96_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_kernel.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_launch_template.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_bwd_preprocess_kernel.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/generate_kernels.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/hardware_info.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/mask.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/philox.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/philox_unpack.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/rotary.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/softmax.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/static_switch.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/utils.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/get_probs.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/trait.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/utils.cuh
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/__init__.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/blockmask_to_uint64.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/topk_to_uint64.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/uint64_to_bool.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/setup.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/stage1/basic_online_softmax.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/stage1/complse_online_softmax.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/stage1/naive_softmax.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_blockmask.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_cache_lens.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_flash_attn.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_infllmv2.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_kvcache_simple.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_pooling_comparison.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_pooling_varlen.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_stage1.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_stage1_causal.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_stage1_compressed_lse.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_stage1_cp_load.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_stage1_uncompressed_lse.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_topk_to_uint64.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_tp.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_tp_blockmasks.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/test_uint64_to_bool.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/topk_hit_stat.py
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/utils.py
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/",
  "description": "List directory contents with details"
}
```

> TOOL

tool_result Bash
```
total 44
drwxr-xr-x 5 user_4813494d user_4813494d   118 Mar 29 14:48 .
drwxr-xr-x 4 user_4813494d user_4813494d    63 Mar 31 15:21 ..
-rw-r--r-- 1 user_4813494d user_4813494d   294 Mar 29 14:48 .gitignore
-rw-r--r-- 1 user_4813494d user_4813494d    93 Mar 29 14:48 .gitmodules
-rw-r--r-- 1 user_4813494d user_4813494d  9341 Mar 29 14:48 README.md
drwxr-xr-x 3 user_4813494d user_4813494d  4096 Mar 29 14:48 csrc
drwxr-xr-x 2 user_4813494d user_4813494d   166 Mar 29 14:48 infllm_v2
-rw-r--r-- 1 user_4813494d user_4813494d 13666 Mar 29 14:48 setup.py
drwxr-xr-x 3 user_4813494d user_4813494d  4096 Mar 29 14:48 tests
```

> AGENT

现在让我并行读取所有关键源文件。我将从核心自定义 CUDA 文件和 Python 绑定开始。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/entry.cu"
}
```

> TOOL

tool_result Read
```
1	#include <torch/extension.h>
2	#include <ATen/ATen.h>
3	#include <c10/util/Optional.h>
4	#include <pybind11/pybind11.h>
5	#include "topk.cuh"
6	#include "get_probs.cuh"
7	#include "blockmask_to_uint64.cuh"
8	#include "topk_to_uint64.cuh"
9	#include "uint64_to_bool.cuh"
10	#include "max_pooling_1d.cuh"
11	#include <ATen/cuda/CUDAContext.h>
12	#include <c10/cuda/CUDAStream.h>
13	
14	// Forward declarations for Flash Attention functions
15	std::vector<at::Tensor> mha_fwd(at::Tensor &q, const at::Tensor &k, const at::Tensor &v, c10::optional<at::Tensor> &out_, c10::optional<at::Tensor> &alibi_slopes_, const float p_dropout, const float softmax_scale, bool is_causal, int window_size_left, int window_size_right, const float softcap, const bool return_softmax, c10::optional<at::Generator> gen_);
16	std::vector<at::Tensor> mha_varlen_fwd(at::Tensor &q, const at::Tensor &k, const at::Tensor &v, c10::optional<at::Tensor> &out_, const at::Tensor &cu_seqlens_q, const at::Tensor &cu_seqlens_k, c10::optional<at::Tensor> &seqused_k, c10::optional<const at::Tensor> &leftpad_k_, c10::optional<at::Tensor> &block_table_, c10::optional<at::Tensor> &alibi_slopes_, int max_seqlen_q, const int max_seqlen_k, const float p_dropout, const float softmax_scale, const bool zero_tensors, bool is_causal, int window_size_left, int window_size_right, const float softcap, const bool return_softmax, c10::optional<at::Generator> gen_, c10::optional<at::Tensor> &blockmask_);
17	std::vector<at::Tensor> mha_varlen_fwd_stage1(at::Tensor &q, const at::Tensor &k, const at::Tensor &v, c10::optional<at::Tensor> &out_, const at::Tensor &cu_seqlens_q, const at::Tensor &cu_seqlens_k, const at::Tensor &cu_seqlens_v, c10::optional<at::Tensor> &seqused_k, c10::optional<const at::Tensor> &leftpad_k_, c10::optional<at::Tensor> &block_table_, c10::optional<at::Tensor> &alibi_slopes_, int max_seqlen_q, const int max_seqlen_k, const float p_dropout, const float softmax_scale, const bool zero_tensors, bool is_causal, int window_size_left, int window_size_right, const float softcap, const bool return_softmax, c10::optional<at::Generator> gen_);
18	std::vector<at::Tensor> mha_bwd(const at::Tensor &dout, const at::Tensor &q, const at::Tensor &k, const at::Tensor &v, const at::Tensor &out, const at::Tensor &softmax_lse, c10::optional<at::Tensor> &dq_, c10::optional<at::Tensor> &dk_, c10::optional<at::Tensor> &dv_, c10::optional<at::Tensor> &alibi_slopes_, const float p_dropout, const float softmax_scale, const bool is_causal, int window_size_left, int window_size_right, const float softcap, const bool deterministic, c10::optional<at::Generator> gen_, c10::optional<at::Tensor> &rng_state);
19	std::vector<at::Tensor> mha_varlen_bwd(const at::Tensor &dout, const at::Tensor &q, const at::Tensor &k, const at::Tensor &v, const at::Tensor &out, const at::Tensor &softmax_lse, c10::optional<at::Tensor> &dq_, c10::optional<at::Tensor> &dk_, c10::optional<at::Tensor> &dv_, const at::Tensor &cu_seqlens_q, const at::Tensor &cu_seqlens_k, c10::optional<at::Tensor> &alibi_slopes_, const int max_seqlen_q, const int max_seqlen_k, const float p_dropout, const float softmax_scale, const bool zero_tensors, const bool is_causal, int window_size_left, int window_size_right, const float softcap, const bool deterministic, c10::optional<at::Tensor> &col_blockmask_, c10::optional<at::Generator> gen_, c10::optional<at::Tensor> &rng_state);
20	std::vector<at::Tensor> mha_fwd_kvcache(at::Tensor &q, const at::Tensor &kcache, const at::Tensor &vcache, c10::optional<const at::Tensor> &k_, c10::optional<const at::Tensor> &v_, c10::optional<const at::Tensor> &seqlens_k_, c10::optional<const at::Tensor> &rotary_cos_, c10::optional<const at::Tensor> &rotary_sin_, c10::optional<const at::Tensor> &cache_batch_idx_, c10::optional<const at::Tensor> &leftpad_k_, c10::optional<at::Tensor> &block_table_, c10::optional<at::Tensor> &alibi_slopes_, c10::optional<at::Tensor> &out_, const float softmax_scale, bool is_causal, int window_size_left, int window_size_right, const float softcap, bool is_rotary_interleaved, int num_splits, c10::optional<at::Tensor> &blockmask_);
21	
22	#define DTYPE_SWITCH(COND, ...)               \
23	    [&] {                                     \
24	        if (COND == 0) {                      \
25	            using elem_type = __half;         \
26	            return __VA_ARGS__();             \
27	        } else {                              \
28	            using elem_type = __nv_bfloat16;  \
29	            return __VA_ARGS__();             \
30	        }                                     \
31	    }()
32	
33	void topk(
34	    std::uintptr_t stream,
35	    int num_tokens, int dim, int top, int dtype,
36	    std::uintptr_t x,
37	    std::uintptr_t topk_val, std::uintptr_t topk_pos
38	) {
39	    DTYPE_SWITCH(dtype, [&] {
40	        topk_func<elem_type>(
41	            reinterpret_cast<cudaStream_t>(stream),
42	            num_tokens, dim, top, dtype,
43	            reinterpret_cast<elem_type*>(x),
44	            reinterpret_cast<elem_type*>(topk_val), reinterpret_cast<int*>(topk_pos)
45	        );
46	    });
47	}
48	
49	void get_probs(
50	    std::uintptr_t stream,
51	    int n, int dim, int dtype,
52	    std::uintptr_t attn_probs, std::uintptr_t lse, float scale
53	) {
54	    DTYPE_SWITCH(dtype, [&] {
55	        get_probs_func<elem_type>(
56	            reinterpret_cast<cudaStream_t>(stream),
57	            reinterpret_cast<elem_type*>(attn_probs), reinterpret_cast<float*>(lse), scale,
58	            n, dim
59	        );
60	    });
61	}
62	
63	void blockmask_to_uint64(
64	    std::uintptr_t stream,
65	    std::uintptr_t blockmask,
66	    std::uintptr_t result,
67	    int batch_size,
68	    int last_dim_size,
69	    int n_uint64_per_row
70	) {
71	    blockmask_to_uint64_func(
72	        reinterpret_cast<cudaStream_t>(stream),
73	        reinterpret_cast<const bool*>(blockmask),
74	        reinterpret_cast<uint64_t*>(result),
75	        batch_size,
76	        last_dim_size,
77	        n_uint64_per_row
78	    );
79	}
80	
81	void topk_to_uint64(
82	    std::uintptr_t stream,
83	    std::uintptr_t topk_idx,
84	    std::uintptr_t result,
85	    int batch_size,
86	    int k,
87	    int k_blocks,
88	    int n_uint64_per_row
89	) {
90	    topk_to_uint64_func(
91	        reinterpret_cast<cudaStream_t>(stream),
92	        reinterpret_cast<const int*>(topk_idx),
93	        reinterpret_cast<uint64_t*>(result),
94	        batch_size,
95	        k,
96	        k_blocks,
97	        n_uint64_per_row
98	    );
99	}
100	
101	void uint64_to_bool(
102	    std::uintptr_t stream,
103	    std::uintptr_t input,
104	    std::uintptr_t result,
105	    int batch_size,
106	    int last_dim_size,
107	    int n_uint64_per_row
108	) {
109	    uint64_to_bool_func(
110	        reinterpret_cast<cudaStream_t>(stream),
111	        reinterpret_cast<const uint64_t*>(input),
112	        reinterpret_cast<bool*>(result),
113	        batch_size,
114	        last_dim_size,
115	        n_uint64_per_row
116	    );
117	}
118	
119	void max_pooling_1d(
120	    std::uintptr_t stream,
121	    std::uintptr_t input,
122	    std::uintptr_t output,
123	    int dtype,
124	    int num_heads,
125	    int q_len,
126	    int k_len,
127	    int out_len,
128	    int cache_len,
129	    int kernel_size,
130	    int stride,
131	    int padding,
132	    int block_size,
133	    int local_blocks,
134	    int init_blocks
135	) {
136	    DTYPE_SWITCH(dtype, [&] {
137	        max_pooling_1d_func<elem_type>(
138	            reinterpret_cast<cudaStream_t>(stream),
139	            reinterpret_cast<const elem_type*>(input),
140	            reinterpret_cast<elem_type*>(output),
141	            num_heads,
142	            q_len,
143	            k_len,
144	            out_len,
145	            cache_len,
146	            kernel_size,
147	            stride,
148	            padding,
149	            block_size,
150	            local_blocks,
151	            init_blocks
152	        );
153	    });
154	}
155	
156	void max_pooling_1d_varlen(
157	    std::uintptr_t stream,
158	    std::uintptr_t input,
159	    std::uintptr_t output,
160	    std::uintptr_t cu_seqlens_q,
161	    std::uintptr_t cu_seqlens_k,
162	    std::uintptr_t cache_lens,
163	    int dtype,
164	    int batch_size,
165	    int num_heads,
166	    int max_seqlen_q,
167	    int max_seqlen_k,
168	    int out_len,
169	    int kernel_size,
170	    int stride,
171	    int padding,
172	    int block_size,
173	    int local_blocks,
174	    int init_blocks,
175	    int total_q
176	) {
177	    // WARNING: 为了适配 CUDA Graph，这里将 max_seqlen_k 设置为model_max_len / 16
178	    // 根据当前8B模型最长上下文为32k，设置为 32768 / 16 = 2048.
179	    // TODO: 优化此处的写法，根据实际最大序列长度动态赋值，以避免过多显存占用。
180	    // const int max_seqlen_k = 2048;
181	    
182	    DTYPE_SWITCH(dtype, [&] {
183	        max_pooling_1d_varlen_func<elem_type>(
184	            reinterpret_cast<cudaStream_t>(stream),
185	            reinterpret_cast<const elem_type*>(input),
186	            reinterpret_cast<elem_type*>(output),
187	            reinterpret_cast<const int*>(cu_seqlens_q),
188	            reinterpret_cast<const int*>(cu_seqlens_k),
189	            reinterpret_cast<const int*>(cache_lens),
190	            batch_size,
191	            num_heads,
192	            max_seqlen_q,
193	            max_seqlen_k,
194	            out_len,
195	            kernel_size,
196	            stride,
197	            padding,
198	            block_size,
199	            local_blocks,
200	            init_blocks,
201	            total_q
202	        );
203	    });
204	}
205	
206	
207	PYBIND11_MODULE(C, m) {
208	    m.doc() = "InfLLM V2 CUDA Implementation with FlashAttention";
209	    
210	    // Original functions
211	    m.def("topk", &topk, "Topk func");
212	    m.def("get_probs", &get_probs, "Get probs func");
213	    m.def("blockmask_to_uint64", &blockmask_to_uint64, "Convert boolean mask to uint64 representation");
214	    m.def("topk_to_uint64", &topk_to_uint64, "Convert topk indices directly to uint64 representation");
215	    m.def("uint64_to_bool", &uint64_to_bool, "Convert uint64 representation back to boolean mask");
216	    m.def("max_pooling_1d", &max_pooling_1d, "Max pooling 1d func");
217	    m.def("max_pooling_1d_varlen", &max_pooling_1d_varlen, "Max pooling 1d func for variable-length sequences");
218	    
219	    m.def("fwd", &mha_fwd, "Forward pass");
220	    m.def("varlen_fwd", &mha_varlen_fwd, "Forward pass (variable length)");
221	    m.def("varlen_fwd_stage1", &mha_varlen_fwd_stage1, "Forward pass (variable length) nsa stage 1");
222	    m.def("bwd", &mha_bwd, "Backward pass");
223	    m.def("varlen_bwd", &mha_varlen_bwd, "Backward pass (variable length)");
224	    m.def("fwd_kvcache", &mha_fwd_kvcache, "Forward pass, with KV-cache");
225	} 
226
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/get_probs.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	#include "trait.cuh"
5	
6	namespace {
7	template<typename T>
8	__global__ void get_probs_kernel(
9	    T* attn_probs, float* lse, float scale, int dim
10	) {
11	    int bid = blockIdx.x;
12	    int tid = threadIdx.x;
13	    float v = attn_probs[bid * dim + tid];
14	    attn_probs[bid * dim + tid] = exp(v * scale - lse[bid]);
15	}
16	}
17	
18	template<typename T>
19	void get_probs_func(
20	    cudaStream_t stream,
21	    T* attn_probs, float* lse, float scale,
22	    int n, int dim
23	) {
24	    get_probs_kernel<T><<<n, dim, 0, stream>>>(attn_probs, lse, scale, dim);
25	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	#include "trait.cuh"
5	namespace {
6	template<typename T, int N>
7	static __device__ inline void warpBitonicSort(T& v1, int& pos, bool asc) {
8	    int lane_id = threadIdx.x & (N - 1);
9	    #pragma unroll
10	    for (int k = 2; k <= N; k *= 2) {
11	        bool desc = ((lane_id & k) == 0) ^ asc;
12	        #pragma unroll
13	        for (int j = k / 2; j > 0; j /= 2) {
14	            T v2 = __shfl_xor_sync(0xFFFFFFFF, v1, j);
15	            int pos2 = __shfl_xor_sync(0xFFFFFFFF, pos, j);
16	            bool upper = (lane_id & j) != 0;
17	            if (desc ^ (v1 > v2 || (v1 == v2 && pos < pos2)) ^ upper) {
18	                v1 = v2;
19	                pos = pos2;
20	            }
21	        }
22	    }
23	}
24	template<typename T, int N>
25	static __device__ inline void warpBitonicMerge(T& v1, int& pos1, T& v2, int& pos2) {
26	    if (v1 < v2 || (v1 == v2 && pos1 > pos2)) {
27	        v1 = v2;
28	        pos1 = pos2;
29	    }
30	    int lane_id = threadIdx.x & (N - 1);
31	    // resort
32	    #pragma unroll
33	    for (int j = N / 2; j > 0; j /= 2) {
34	        v2 = __shfl_xor_sync(0xFFFFFFFF, v1, j);
35	        int pos2 = __shfl_xor_sync(0xFFFFFFFF, pos1, j);
36	        bool upper = (lane_id & j) != 0;
37	        if ((v1 < v2 || (v1 == v2 && pos1 > pos2)) ^ upper) {
38	            v1 = v2;
39	            pos1 = pos2;
40	        }
41	    }
42	}
43	template<typename T, int N>
44	static __device__ inline void blockBitonicReduce(T& v, int& pos) {
45	    __shared__ T shared_val[1024];
46	    __shared__ int shared_pos[1024];
47	    // block reduce
48	    shared_val[threadIdx.x] = v;
49	    shared_pos[threadIdx.x] = pos;
50	    // inter warp reduce
51	    #pragma unroll
52	    for (int i = 512; i >= 32; i >>= 1) {
53	        if (blockDim.x > i) {
54	            __syncthreads();
55	            if (threadIdx.x < i) {
56	                int idx_next = (i << 1) - threadIdx.x - 1;
57	                T nw_v = (idx_next < blockDim.x) ? shared_val[idx_next] : T(-TypeTraits<T>::inf());
58	                int nw_pos = (idx_next < blockDim.x) ? shared_pos[idx_next] : -1;
59	                warpBitonicMerge<T, N>(v, pos, nw_v, nw_pos); // merge and rebuild in desc order
60	                shared_val[threadIdx.x] = v;
61	                shared_pos[threadIdx.x] = pos;
62	            }
63	        }
64	    }
65	    // intra warp reduce
66	    if (threadIdx.x < 32) {
67	        warpBitonicSort<T, 32>(v, pos, false);
68	    }
69	}
70	template<typename T, int N>
71	static __global__ void kernel_bitonic_topk(
72	    int n, int top,
73	    T *inp,     // (batch, n)
74	    float *out,     // (batch, top)
75	    int *idx    // (batch, top)
76	) {
77	    int offset_inp = blockIdx.x * n;
78	    int offset_out = blockIdx.x * top;
79	    T local_v = threadIdx.x < n ? inp[offset_inp + threadIdx.x] : -TypeTraits<T>::inf();
80	    int local_pos = threadIdx.x;
81	    warpBitonicSort<T, N>(local_v, local_pos, false); // local sort in desc order
82	    for (int i = blockDim.x; i < n; i += blockDim.x) {
83	        T nw_v = (i + threadIdx.x) < n ? inp[offset_inp + i + threadIdx.x] : -TypeTraits<T>::inf();
84	        int nw_pos = i + threadIdx.x;
85	        // step.1: local sort
86	        warpBitonicSort<T, N>(nw_v, nw_pos, true); // local sort in asc order
87	        // step.2&3: merge and rebuild
88	        warpBitonicMerge<T, N>(local_v, local_pos, nw_v, nw_pos); // merge and rebuild in desc order
89	    }
90	    blockBitonicReduce<T, N>(local_v, local_pos);
91	    if (threadIdx.x < top) {
92	        out[offset_out + threadIdx.x] = local_v;
93	        idx[offset_out + threadIdx.x] = local_pos;
94	    }
95	}
96	// intra-block topk
97	// gridDim(batch, n / 1024, 1), threadDim(1024, 1, 1)
98	template<typename T, int N, bool ordered>
99	static __global__ void kernel_bitonic_topk_multiblock(
100	    int n,
101	    const T *inp,       // (batch, n)
102	    const int *idx_inp, // (batch, n)
103	    T *out,     // (batch, n / 1024 * N)
104	    int *idx    // (batch, n / 1024 * N)
105	) {
106	    int offset_col = blockIdx.y * blockDim.x + threadIdx.x;
107	    int offset_inp = blockIdx.x * n + offset_col;
108	    int offset_out = blockIdx.x * (gridDim.y * N) + blockIdx.y * N + threadIdx.x;
109	    T local_v = (offset_col < n) ? inp[offset_inp] : T(-TypeTraits<T>::inf());
110	    int local_pos = (idx_inp == nullptr) ? offset_col : idx_inp[offset_inp];
111	    if (!ordered) warpBitonicSort<T, N>(local_v, local_pos, false); // local sort in desc order
112	    blockBitonicReduce<T, N>(local_v, local_pos);
113	    if (threadIdx.x < N) {
114	        out[offset_out] = local_v;
115	        idx[offset_out] = local_pos;
116	    }
117	}
118	
119	#define TOPK_SIZE_DISPATCH(top, ...) \
120	    do { \
121	        const int &top_v = top; \
122	        if (top_v > 16) { \
123	            const int top_size = 32; \
124	            __VA_ARGS__ \
125	        } else if (top_v > 8) { \
126	            const int top_size = 16; \
127	            __VA_ARGS__ \
128	        } else if (top_v > 4) { \
129	            const int top_size = 8; \
130	            __VA_ARGS__ \
131	        } else if (top_v > 2) { \
132	            const int top_size = 4; \
133	            __VA_ARGS__ \
134	        } else if (top_v > 1) { \
135	            const int top_size = 2; \
136	            __VA_ARGS__ \
137	        } else { \
138	            const int top_size = 1; \
139	            __VA_ARGS__ \
140	        } \
141	    } while(0)
142	
143	template <typename T>
144	void bitonic_topk(
145	    const cudaStream_t stream,
146	    const int batch,
147	    const int n,
148	    const int top,
149	    const T* x, 
150	    T* out, 
151	    int* pos
152	) {
153	    TOPK_SIZE_DISPATCH(top, {
154	        dim3 blockDim(n, 1, 1);
155	        dim3 gridDim(batch, 1, 1);
156	        kernel_bitonic_topk_multiblock<T, top_size, false><<<gridDim, blockDim, 0, stream>>>(
157	            n,
158	            x,
159	            nullptr,
160	            out,
161	            pos
162	        );
163	    });
164	}
165	} // namespace
166	
167	template<typename T>
168	void topk_func(
169	    cudaStream_t stream,
170	    int num_tokens, int dim, int top, int dtype,
171	    T* x,
172	    T* topk_val, int* topk_pos
173	) {
174	    bitonic_topk<T>(
175	        stream,
176	        num_tokens,
177	        dim, top,
178	        x,
179	        topk_val, topk_pos
180	    );
181	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	#include "trait.cuh"
5	
6	#include <cuda_runtime.h>
7	#include <cuda_fp16.h>
8	#include <cuda_bf16.h>
9	
10	namespace {
11	template <typename T>
12	__global__ void max_pooling_1d_varlen_kernel(
13	    const T* input,  // [num_heads, total_q, max_k]
14	    T* output,       // [num_heads, total_q, out_len]
15	    const int* cu_seqlens_q,  // cumulative sequence lengths for queries
16	    const int* cu_seqlens_k,  // cumulative sequence lengths for keys
17	    const int* cache_lens,    // cache lengths for each batch [batch_size]
18	    int batch_size,
19	    int num_heads,
20	    int max_seqlen_q,
21	    int max_seqlen_k,
22	    int out_len,
23	    int kernel_size,
24	    int stride,
25	    int padding,
26	    int block_size,
27	    int local_blocks,
28	    int init_blocks
29	) {
30	    // Grid: (total_q, num_heads)
31	    // Block: (threads_per_block)
32	    
33	    int bidh = blockIdx.y;  // head index
34	    int bidq_global = blockIdx.x;  // global query index across all batches
35	    
36	    // Find which batch this query belongs to
37	    int batch_idx = 0;
38	    int q_start = 0;
39	    int q_end = 0;
40	    int k_start = 0;
41	    int k_end = 0;
42	    
43	    // Binary search to find batch index
44	    for (int b = 0; b < batch_size; b++) {
45	        q_start = cu_seqlens_q[b];
46	        q_end = cu_seqlens_q[b + 1];
47	        k_start = cu_seqlens_k[b];
48	        k_end = cu_seqlens_k[b + 1];
49	        
50	        if (bidq_global >= q_start && bidq_global < q_end) {
51	            batch_idx = b;
52	            break;
53	        }
54	    }
55	    
56	    // Local query index within the batch
57	    int bidq_local = bidq_global - q_start;
58	    int seqlen_q = q_end - q_start;
59	    int seqlen_k = k_end - k_start;
60	    
61	    // Skip if this thread is outside the sequence length
62	    if (bidq_local >= seqlen_q) return;
63	    
64	    // Calculate input and output pointers
65	    // Input is packed: [num_heads, total_q, max_k]
66	    // We need to access the k values for this specific query
67	    size_t total_q_all = cu_seqlens_q[batch_size]; 
68	    size_t in_offset = (size_t)bidh * total_q_all * (size_t)max_seqlen_k + (size_t)bidq_global * (size_t)max_seqlen_k;
69	    const T* in = input + in_offset;
70	    size_t out_offset = (size_t)bidh * total_q_all * (size_t)out_len + (size_t)bidq_global * (size_t)out_len;
71	    T* out = output + out_offset;
72	    
73	    // Calculate query block index for masking
74	    int cache_len = cache_lens[batch_idx];  // Get cache_len for this batch
75	    int off_bq = (bidq_local + cache_len) / block_size;
76	
77	    for (int k = threadIdx.x; k < out_len; k += blockDim.x) {
78	        // This is equivalent to `off_bk` in transform_score
79	        int off_bk = k;
80	        
81	        // Check causal + local window mask based on exact criteria from transform_score
82	        bool should_mask_inf = (off_bk < init_blocks) || ((off_bq >= off_bk) && (off_bq <= off_bk + local_blocks));
83	        
84	        if (should_mask_inf) {
85	            out[k] = TypeTraits<T>::inf();
86	        }
87	        else {
88	            // Compute max pooling for other areas
89	            int start = k * stride - padding;
90	            int end = start + kernel_size;
91	            start = max(start, 0);
92	            end = min(end, seqlen_k);  // Use actual sequence length for this batch
93	            
94	            T max_val = -TypeTraits<T>::inf();
95	            if (end > start) {
96	                max_val = in[start];
97	                for (int i = start + 1; i < end; i++) {
98	                    if (in[i] > max_val) {
99	                        max_val = in[i];
100	                    }
101	                }
102	            }
103	            out[k] = max_val;
104	        }
105	    }
106	}
107	
108	// Original kernel for backward compatibility
109	template <typename T>
110	__global__ void max_pooling_1d_kernel(
111	    const T* input,
112	    T* output,
113	    int num_heads,
114	    int q_len,
115	    int k_len,
116	    int out_len,
117	    int cache_len,
118	    int kernel_size,
119	    int stride,
120	    int padding,
121	    int block_size,
122	    int local_blocks,
123	    int init_blocks
124	) {
125	    int bidh = blockIdx.y;
126	    int bidq = blockIdx.x;
127	    const T* in = input + bidh * (q_len * k_len) + bidq * k_len;
128	    T* out = output + bidh * (q_len * out_len) + bidq * out_len;
129	    
130	    // Calculate query block index (equivalent to off_bq in transform_score)
131	    int off_bq = (bidq + cache_len) / block_size;
132	
133	    for (int k = threadIdx.x; k < out_len; k += blockDim.x) {
134	        // This is equivalent to `off_bk` in transform_score
135	        int off_bk = k;
136	        
137	        // Check causal + local window mask based on exact criteria from transform_score
138	        bool should_mask_inf = (off_bk < init_blocks) || ((off_bq >= off_bk) && (off_bq <= off_bk + local_blocks));
139	
140	        if (should_mask_inf) {
141	            out[k] = TypeTraits<T>::inf();
142	        }
143	
144	        else {
145	            // Compute max pooling for other areas
146	            int start = k * stride - padding;
147	            int end = start + kernel_size;
148	            start = max(start, 0);
149	            end = min(end, k_len);
150	            
151	            T max_val = -TypeTraits<T>::inf();
152	            if (end > start) {
153	                max_val = in[start];
154	                for (int i = start + 1; i < end; i++) {
155	                    if (in[i] > max_val) {
156	                        max_val = in[i];
157	                    }
158	                }
159	            }
160	            out[k] = max_val;
161	        }
162	    }
163	}
164	} // namespace
165	
166	// Variable-length sequence version
167	template <typename T>
168	void max_pooling_1d_varlen_func(
169	    cudaStream_t stream,
170	    const T* input,
171	    T* output,
172	    const int* cu_seqlens_q,
173	    const int* cu_seqlens_k,
174	    const int* cache_lens,
175	    int batch_size,
176	    int num_heads,
177	    int max_seqlen_q,
178	    int max_seqlen_k,
179	    int out_len,
180	    int kernel_size,
181	    int stride,
182	    int padding,
183	    int block_size,
184	    int local_blocks,
185	    int init_blocks,
186	    int total_q
187	) {
188	    const int threads_per_block = 256;
189	    
190	    // Total number of queries across all batches
191	    // int total_q;
192	    // cudaMemcpyAsync(&total_q, &cu_seqlens_q[batch_size], sizeof(int), 
193	    //                 cudaMemcpyDeviceToHost, stream);
194	    // cudaStreamSynchronize(stream);
195	    
196	    dim3 grid(total_q, num_heads);
197	    dim3 block(threads_per_block, 1);
198	    
199	    max_pooling_1d_varlen_kernel<<<grid, block, 0, stream>>>(
200	        input, output, cu_seqlens_q, cu_seqlens_k, cache_lens, batch_size, num_heads, 
201	        max_seqlen_q, max_seqlen_k, out_len, kernel_size, stride, padding, block_size, local_blocks, init_blocks
202	    );
203	}
204	
205	// Original fixed-length version for backward compatibility
206	template <typename T>
207	void max_pooling_1d_func(
208	    cudaStream_t stream,
209	    const T* input,
210	    T* output,
211	    int num_heads,
212	    int q_len,
213	    int k_len,
214	    int out_len,
215	    int cache_len,
216	    int kernel_size,
217	    int stride,
218	    int padding,
219	    int block_size,
220	    int local_blocks,
221	    int init_blocks
222	) {
223	    const int threads_per_block = 256;
224	    
225	    dim3 grid(q_len, num_heads);
226	    dim3 block(threads_per_block, 1);
227	    
228	    max_pooling_1d_kernel<<<grid, block, 0, stream>>>(
229	        input, output, num_heads, q_len, k_len, out_len, cache_len, kernel_size, stride, padding, block_size, local_blocks, init_blocks
230	    );
231	} 
232
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	
5	namespace {
6	/**
7	 * CUDA kernel to convert boolean mask to uint64 representation
8	 * Each thread processes one element in the output array
9	 */
10	__global__ void kernel_blockmask_to_uint64(
11	    const bool* blockmask,     // Input boolean mask
12	    uint64_t* result,          // Output uint64 array
13	    int batch_size,            // Total number of rows (flattened batch dimensions)
14	    int last_dim_size,         // Original last dimension size
15	    int n_uint64_per_row       // Number of uint64 needed per row
16	) {
17	    // Calculate global position
18	    int row = blockIdx.x * blockDim.x + threadIdx.x;
19	    int col = blockIdx.y;
20	    
21	    if (row >= batch_size || col >= n_uint64_per_row) return;
22	    
23	    // Calculate input and output offsets
24	    int out_idx = row * n_uint64_per_row + col;
25	    int in_idx_base = row * last_dim_size;
26	    
27	    // Calculate starting bit position for this uint64
28	    int bit_start = col * 64;
29	    
30	    // Initialize result
31	    uint64_t packed_value = 0;
32	    
33	    // Pack 64 bits (or fewer for the last uint64)
34	    for (int bit = 0; bit < 64; bit++) {
35	        int bit_pos = bit_start + bit;
36	        
37	        // Check if we're still within the valid range
38	        if (bit_pos < last_dim_size) {
39	            // Get the boolean value
40	            bool bit_value = blockmask[in_idx_base + bit_pos];
41	            
42	            // Set the corresponding bit in the result
43	            if (bit_value) {
44	                packed_value |= (1ULL << bit);
45	            }
46	        }
47	    }
48	    
49	    // Store the result
50	    result[out_idx] = packed_value;
51	}
52	} // namespace
53	
54	/**
55	 * Function to convert boolean mask to uint64 representation
56	 */
57	void blockmask_to_uint64_func(
58	    cudaStream_t stream,
59	    const bool* blockmask,        // Input boolean mask
60	    uint64_t* result,             // Output uint64 array
61	    int batch_size,               // Total number of rows (flattened batch dimensions)
62	    int last_dim_size,            // Original last dimension size
63	    int n_uint64_per_row          // Number of uint64 needed per row
64	) {
65	    const int threads_per_block = 256;
66	    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
67	    
68	    dim3 grid(blocks_per_row, n_uint64_per_row);
69	    dim3 block(threads_per_block, 1);
70	    
71	    kernel_blockmask_to_uint64<<<grid, block, 0, stream>>>(
72	        blockmask, result, batch_size, last_dim_size, n_uint64_per_row
73	    );
74	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	
5	namespace {
6	/**
7	 * CUDA kernel to convert topk indices directly to uint64 representation
8	 * Each thread processes one element in the output array
9	 */
10	__global__ void kernel_topk_to_uint64(
11	    const int* topk_idx,       // Input topk indices [num_heads, total_seqlen, k]
12	    uint64_t* result,          // Output uint64 array
13	    int batch_size,            // Total number of rows (flattened batch dimensions)
14	    int k,                     // Number of topk values per row
15	    int k_blocks,              // Number of key blocks
16	    int n_uint64_per_row       // Number of uint64 needed per row
17	) {
18	    // Calculate global position
19	    int row = blockIdx.x * blockDim.x + threadIdx.x;
20	    int col = blockIdx.y;
21	    
22	    if (row >= batch_size || col >= n_uint64_per_row) return;
23	    
24	    // Calculate output offset
25	    int out_idx = row * n_uint64_per_row + col;
26	    
27	    // Calculate starting bit position for this uint64
28	    int bit_start = col * 64;
29	    
30	    // Initialize result
31	    uint64_t packed_value = 0;
32	    
33	    // For each topk index in this row
34	    for (int i = 0; i < k; i++) {
35	        // Get the index value
36	        int idx_offset = row * k + i;
37	        int idx = topk_idx[idx_offset];
38	        
39	        // Skip if the index is -1 (invalid)
40	        if (idx == -1) continue;
41	        
42	        // Check if this idx falls within the current uint64 chunk
43	        if (idx >= bit_start && idx < bit_start + 64) {
44	            // Set the corresponding bit in the packed value
45	            int local_bit = idx - bit_start;
46	            packed_value |= (1ULL << local_bit);
47	        }
48	    }
49	    
50	    // Store the result
51	    result[out_idx] = packed_value;
52	}
53	} // namespace
54	
55	/**
56	 * Function to convert topk indices directly to uint64 representation
57	 */
58	void topk_to_uint64_func(
59	    cudaStream_t stream,
60	    const int* topk_idx,          // Input topk indices
61	    uint64_t* result,             // Output uint64 array
62	    int batch_size,               // Total number of rows (flattened batch dimensions)
63	    int k,                        // Number of topk values per row
64	    int k_blocks,                 // Number of key blocks
65	    int n_uint64_per_row          // Number of uint64 needed per row
66	) {
67	    const int threads_per_block = 256;
68	    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
69	    
70	    dim3 grid(blocks_per_row, n_uint64_per_row);
71	    dim3 block(threads_per_block, 1);
72	    
73	    kernel_topk_to_uint64<<<grid, block, 0, stream>>>(
74	        topk_idx, result, batch_size, k, k_blocks, n_uint64_per_row
75	    );
76	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include "utils.cuh"
4	
5	namespace {
6	/**
7	 * CUDA kernel to convert uint64 representation back to boolean mask
8	 * Each thread processes one element in the output array
9	 */
10	__global__ void kernel_uint64_to_bool(
11	    const uint64_t* input,     // Input uint64 array
12	    bool* result,              // Output boolean mask
13	    int batch_size,            // Total number of rows (flattened batch dimensions)
14	    int last_dim_size,         // Original last dimension size
15	    int n_uint64_per_row       // Number of uint64 needed per row
16	) {
17	    // Calculate global position
18	    int row = blockIdx.x * blockDim.x + threadIdx.x;
19	    int col = blockIdx.y;
20	    
21	    if (row >= batch_size || col >= last_dim_size) return;
22	    
23	    // Calculate which uint64 element contains this bit
24	    int uint64_idx = col / 64;
25	    
26	    // Calculate bit position within the uint64
27	    int bit_pos = col % 64;
28	    
29	    // Calculate input offset
30	    int in_idx = row * n_uint64_per_row + uint64_idx;
31	    
32	    // Calculate output offset
33	    int out_idx = row * last_dim_size + col;
34	    
35	    // Get the uint64 value
36	    uint64_t packed_value = input[in_idx];
37	    
38	    // Extract the bit and convert to boolean
39	    bool bit_value = (packed_value & (1ULL << bit_pos)) != 0;
40	    
41	    // Store the result
42	    result[out_idx] = bit_value;
43	}
44	} // namespace
45	
46	/**
47	 * Function to convert uint64 representation back to boolean mask
48	 */
49	void uint64_to_bool_func(
50	    cudaStream_t stream,
51	    const uint64_t* input,        // Input uint64 array
52	    bool* result,                 // Output boolean mask
53	    int batch_size,               // Total number of rows (flattened batch dimensions)
54	    int last_dim_size,            // Original last dimension size
55	    int n_uint64_per_row          // Number of uint64 needed per row
56	) {
57	    const int threads_per_block = 256;
58	    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
59	    
60	    dim3 grid(blocks_per_row, last_dim_size);
61	    dim3 block(threads_per_block, 1);
62	    
63	    kernel_uint64_to_bool<<<grid, block, 0, stream>>>(
64	        input, result, batch_size, last_dim_size, n_uint64_per_row
65	    );
66	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/trait.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cuda_runtime.h>
3	#include <cuda_fp16.h>
4	#include <cuda_bf16.h>
5	
6	template <typename T>
7	struct TypeTraits;
8	
9	template <>
10	struct TypeTraits<__half> {
11	    using half2 = __half2;
12	
13	    static __inline__ int type_code() {
14	        return 0;
15	    }
16	
17	    static __host__ __device__ __inline__ __half inf() { 
18	        return __float2half(INFINITY);
19	    }
20	};
21	
22	template <>
23	struct TypeTraits<__nv_bfloat16> {
24	    using half2 = __nv_bfloat162;
25	
26	    static __inline__ int type_code() {
27	        return 1;
28	    }
29	
30	    static __host__ __device__ __inline__ __nv_bfloat16 inf() { 
31	        return __float2bfloat16(INFINITY);
32	    }
33	};
34
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/utils.cuh"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	#include <cmath>
3	#include <cstdio>
4	#include <cstdlib>
5	#include <iostream>
6	#include <iomanip>
7	#include <cuda_runtime.h>
8	
9	#define CEIL_DIV(M, N) (((M) + (N) - 1) / (N))
10	#define ROUND_UP(M, N) (((M) + (N) - 1) / (N) * (N))
11	
12	#define cudaCheck(err) \
13	    if (err != cudaSuccess) { \
14	        std::cerr << "cuda error at " << __FILE__ << ":" << __LINE__ << std::endl; \
15	        std::cerr << cudaGetErrorString(err) << std::endl; \
16	        exit(EXIT_FAILURE); \
17	    }
18	
19	#define cublasCheck(err) \
20	    if (err != CUBLAS_STATUS_SUCCESS) { \
21	        std::cerr << "cuBLAS error at " << __FILE__ << ":" << __LINE__ << std::endl; \
22	        std::cerr << err << std::endl; \
23	        exit(EXIT_FAILURE); \
24	    }
25
```

> AGENT

现在我来阅读所有 Python 文件和 Flash Attention 的关键头文件。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/__init__.py"
}
```

> TOOL

tool_result Read
```
1	__version__ = "0.1.0"
2	
3	from .blockmask_to_uint64 import blockmask_to_uint64
4	from .topk_to_uint64 import topk_to_uint64
5	from .uint64_to_bool import uint64_to_bool
6	from .max_pooling_1d import max_pooling_1d, max_pooling_1d_varlen, max_pooling_1d_varlen_v2
7	from .infllmv2_sparse_attention import (
8	    infllmv2_attn_varlen_func,
9	    infllmv2_attn_stage1,
10	    infllmv2_attn_with_kvcache,
11	)
12
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py"
}
```

> TOOL

tool_result Read
```
1	# Copyright (c) 2023, Tri Dao.
2	
3	from typing import Optional, Sequence, Tuple, Union
4	
5	import torch
6	import torch.nn as nn
7	import os
8	
9	# Import from infllm_v2's C extension and local modules
10	from . import C as infllm_cuda
11	from .topk_to_uint64 import topk_to_uint64 as cuda_topk_to_uint64
12	from .uint64_to_bool import uint64_to_bool as cuda_uint64_to_bool
13	from .blockmask_to_uint64 import blockmask_to_uint64 as cuda_blockmask_to_uint64
14	
15	# isort: on
16	
17	def maybe_contiguous(x):
18	    return x.contiguous() if x is not None and x.stride(-1) != 1 else x
19	
20	
21	def round_multiple(x, m):
22	    return (x + m - 1) // m * m
23	
24	
25	# torch.compile() support is only enabled for pytorch >= 2.4
26	# The reason for this is that we are using the new custom_op and register_fake
27	# APIs, which support inplace modification of inputs in the function itself
28	if torch.__version__ >= "2.4.0":
29	    _torch_custom_op_wrapper = torch.library.custom_op
30	    _torch_register_fake_wrapper = torch.library.register_fake
31	else:
32	    def noop_custom_op_wrapper(name, fn=None, /, *, mutates_args, device_types=None, schema=None):
33	        def wrap(func):
34	            return func
35	        if fn is None:
36	            return wrap
37	        return fn
38	    def noop_register_fake_wrapper(op, fn=None, /, *, lib=None, _stacklevel=1):
39	        def wrap(func):
40	            return func
41	        if fn is None:
42	            return wrap
43	        return fn
44	    _torch_custom_op_wrapper = noop_custom_op_wrapper
45	    _torch_register_fake_wrapper = noop_register_fake_wrapper
46	
47	
48	@_torch_custom_op_wrapper("infllmv2_attn::_infllmv2_attn_varlen_forward", mutates_args=(), device_types="cuda")
49	def _infllmv2_attn_varlen_forward(
50	    q: torch.Tensor,
51	    k: torch.Tensor,
52	    v: torch.Tensor,
53	    cu_seqlens_q: torch.Tensor,
54	    cu_seqlens_k: torch.Tensor,
55	    max_seqlen_q: int,
56	    max_seqlen_k: int,
57	    dropout_p: float,
58	    softmax_scale: float,
59	    causal: bool,
60	    window_size_left: int = -1,
61	    window_size_right: int = -1,
62	    softcap: float = 0.0,
63	    alibi_slopes: Optional[torch.Tensor] = None,
64	    return_softmax: bool = False,
65	    block_table: Optional[torch.Tensor] = None,
66	    leftpad_k: Optional[torch.Tensor] = None,
67	    seqused_k: Optional[torch.Tensor] = None,
68	    topk_idx: Optional[torch.Tensor] = None,
69	
70	) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
71	    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
72	
73	    if topk_idx is not None:
74	        # Calculate group size (number of query heads per K/V head)
75	        nheads_q = q.shape[1]
76	        nheads_k = k.shape[1]
77	        group_size = nheads_q // nheads_k
78	        head_dim = q.shape[-1]
79	        
80	        # Optimize for MQA case (nheads_k == 1)
81	        if nheads_k == 1:
82	            # Direct reshape for MQA - no transpose needed
83	            q = q.reshape(-1, 1, head_dim).contiguous()
84	            cu_seqlens_q = cu_seqlens_q * nheads_q
85	            max_seqlen_q = max_seqlen_q * nheads_q
86	        else:
87	            # General case for GQA/MHA
88	            q = q.reshape(-1, nheads_k, group_size, head_dim).transpose(1, 2).reshape(-1, nheads_k, head_dim).contiguous()
89	            cu_seqlens_q = cu_seqlens_q * group_size
90	            max_seqlen_q = max_seqlen_q * group_size
91	        
92	        assert topk_idx.dtype == torch.int32
93	        fwd_blockmask_uint64, _ = cuda_topk_to_uint64(topk_idx, max_seqlen_k, 64) # N_BLOCK_DIM=64
94	    else:
95	        fwd_blockmask_uint64 = None
96	
97	    out, softmax_lse, S_dmask, rng_state = infllm_cuda.varlen_fwd(
98	        q,
99	        k,
100	        v,
101	        None,
102	        cu_seqlens_q,
103	        cu_seqlens_k,
104	        seqused_k,
105	        leftpad_k,
106	        block_table,
107	        alibi_slopes,
108	        max_seqlen_q,
109	        max_seqlen_k,
110	        dropout_p,
111	        softmax_scale,
112	        False,
113	        causal,
114	        window_size_left,
115	        window_size_right,
116	        softcap,
117	        return_softmax,
118	        None,
119	        fwd_blockmask_uint64,
120	    )
121	    # if out.isnan().any() or softmax_lse.isnan().any():
122	    #     breakpoint()
123	    if topk_idx is not None:
124	        # Reshape output back to original dimensions
125	        if nheads_k == 1:
126	            # Direct reshape for MQA - no transpose needed
127	            out = out.reshape(-1, nheads_q, head_dim).contiguous()
128	        else:
129	            # General case for GQA/MHA
130	            out = out.reshape(-1, group_size, nheads_k, head_dim).transpose(1, 2).reshape(-1, nheads_q, head_dim).contiguous()
131	    
132	    return out, softmax_lse, S_dmask, fwd_blockmask_uint64, rng_state
133	
134	
135	
136	_wrapped_infllmv2_attn_varlen_forward = _infllmv2_attn_varlen_forward
137	
138	
139	@_torch_custom_op_wrapper("infllmv2_attn::_infllmv2_attn_varlen_backward", mutates_args=("dq", "dk", "dv"), device_types="cuda")
140	def _infllmv2_attn_varlen_backward(
141	    dout: torch.Tensor,
142	    q: torch.Tensor,
143	    k: torch.Tensor,
144	    v: torch.Tensor,
145	    out: torch.Tensor,
146	    softmax_lse: torch.Tensor,
147	    dq: Optional[torch.Tensor],
148	    dk: Optional[torch.Tensor],
149	    dv: Optional[torch.Tensor],
150	    cu_seqlens_q: torch.Tensor,
151	    cu_seqlens_k: torch.Tensor,
152	    max_seqlen_q: int,
153	    max_seqlen_k: int,
154	    dropout_p: float,
155	    softmax_scale: float,
156	    causal: bool,
157	    window_size_left: int,
158	    window_size_right: int,
159	    softcap: float,
160	    alibi_slopes: Optional[torch.Tensor],
161	    deterministic: bool,
162	    bwd_blockmask_uint64 : Optional[torch.Tensor] = None,  # Use the uint64 matrix directly
163	    rng_state: Optional[torch.Tensor] = None,
164	) -> torch.Tensor:
165	    # dq, dk, dv are allocated by us so they should already be contiguous
166	    dout, q, k, v, out = [maybe_contiguous(x) for x in (dout, q, k, v, out)]
167	    # Calculate the ratio of q heads to k sequence
168	    group_size = q.shape[-2] // k.shape[-2]
169	    # Get original shapes and dimensions
170	    total_q, nheads_q, dim = q.shape
171	    nheads_k = k.shape[-2]
172	    
173	    # Optimize for MQA case (nheads_k == 1)
174	    if nheads_k == 1:
175	        # Direct reshape for MQA - no transpose needed
176	        q_final = q.reshape(total_q * nheads_q, 1, dim).contiguous()
177	        dout_final = dout.reshape(total_q * nheads_q, 1, dim).contiguous()
178	        out_final = out.reshape(total_q * nheads_q, 1, dim).contiguous()
179	    else:
180	        # Memory-efficient reshaping for GQA/MHA - break into steps with immediate cleanup
181	        q_final = q.reshape(total_q, nheads_k, group_size, dim)
182	        q_final = q_final.permute(0, 2, 1, 3)
183	        q_final = q_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
184	        
185	        dout_final = dout.reshape(total_q, nheads_k, group_size, dim)
186	        dout_final = dout_final.permute(0, 2, 1, 3)
187	        dout_final = dout_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
188	        
189	        out_final = out.reshape(total_q, nheads_k, group_size, dim)
190	        out_final = out_final.permute(0, 2, 1, 3)
191	        out_final = out_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
192	    # q = q.reshape(-1, 16, 2, head_dim).reshape(-1, 2, head_dim)
193	    # breakpoint()
194	    # with open("/user/luopeiyan/a/Block-Sparse-Attention/tests/after_q_output_flash_attn_varlen_forward.txt", "a+") as f:
195	    #     f.write(str(q) + "\n") 
196	    # Reduce memory by computing cu_seqlens_q_expanded in-place
197	    if nheads_k == 1:
198	        # For MQA, multiply by nheads_q
199	        cu_seqlens_q_expanded = torch.zeros(cu_seqlens_q.shape[0], device=cu_seqlens_q.device, dtype=cu_seqlens_q.dtype)
200	        for i in range(cu_seqlens_q.shape[0]-1):
201	            cu_seqlens_q_expanded[i+1] = (cu_seqlens_q[i+1] - cu_seqlens_q[i]) * nheads_q + cu_seqlens_q_expanded[i]
202	        max_seqlen_q_expanded = max_seqlen_q * nheads_q
203	    else:
204	        # For GQA/MHA, multiply by group_size
205	        cu_seqlens_q_expanded = torch.zeros(cu_seqlens_q.shape[0], device=cu_seqlens_q.device, dtype=cu_seqlens_q.dtype)
206	        for i in range(cu_seqlens_q.shape[0]-1):
207	            cu_seqlens_q_expanded[i+1] = (cu_seqlens_q[i+1] - cu_seqlens_q[i]) * group_size + cu_seqlens_q_expanded[i]
208	        max_seqlen_q_expanded = max_seqlen_q * group_size
209	    # Create dq_temp directly with correct shape
210	    dq_temp = torch.empty_like(q_final)
211	    
212	    (
213	        _,
214	        _,
215	        _,
216	        softmax_d,
217	    ) = infllm_cuda.varlen_bwd(
218	        dout_final,
219	        q_final,
220	        k,
221	        v,
222	        out_final,
223	        softmax_lse,
224	        dq_temp,
225	        dk,
226	        dv,
227	        cu_seqlens_q_expanded,
228	        cu_seqlens_k,
229	        alibi_slopes,
230	        max_seqlen_q_expanded,
231	        max_seqlen_k,
232	        dropout_p,
233	        softmax_scale,
234	        False,
235	        causal,
236	        window_size_left,
237	        window_size_right,
238	        softcap,
239	        deterministic,
240	        bwd_blockmask_uint64,
241	        None,
242	        rng_state,
243	    )
244	    # Free memory immediately after use
245	    dout_final = out_final = None
246	    torch.cuda.empty_cache()
247	    
248	    # Reshape dq_temp directly back to original shape
249	    if nheads_k == 1:
250	        # Direct reshape for MQA - no transpose needed
251	        dq_temp = dq_temp.reshape(total_q, nheads_q, dim)
252	    else:
253	        # General case for GQA/MHA
254	        dq_temp = dq_temp.reshape(total_q, group_size, nheads_k, dim)
255	        dq_temp = dq_temp.permute(0, 2, 1, 3)
256	        dq_temp = dq_temp.reshape(total_q, nheads_q, dim)
257	    
258	    # Use in-place copy instead of assignment
259	    dq.copy_(dq_temp)
260	    
261	    # Clean up remaining references
262	    q_final = dq_temp = None
263	    torch.cuda.empty_cache()
264	    return softmax_d
265	
266	
267	
268	
269	if torch.__version__ >= "2.4.0":
270	    _wrapped_infllmv2_attn_varlen_backward = torch.ops.infllmv2_attn._infllmv2_attn_varlen_backward
271	else:
272	    _wrapped_infllmv2_attn_varlen_backward = _infllmv2_attn_varlen_backward
273	
274	
275	class Infllmv2AttnVarlenFunc(torch.autograd.Function):
276	    @staticmethod
277	    def forward(
278	        ctx,
279	        q,
280	        k,
281	        v,
282	        cu_seqlens_q,
283	        cu_seqlens_k,
284	        max_seqlen_q,
285	        max_seqlen_k,
286	        dropout_p,
287	        softmax_scale,
288	        causal,
289	        window_size,
290	        softcap,
291	        alibi_slopes,
292	        deterministic,
293	        return_softmax,
294	        block_table,
295	        topk_idx,
296	    ):
297	        if softmax_scale is None:
298	            softmax_scale = q.shape[-1] ** (-0.5)
299	        head_size_og = q.size(2)
300	        if head_size_og % 8 != 0:
301	            q = torch.nn.functional.pad(q, [0, 8 - head_size_og % 8])
302	            k = torch.nn.functional.pad(k, [0, 8 - head_size_og % 8])
303	            v = torch.nn.functional.pad(v, [0, 8 - head_size_og % 8])
304	        out_padded, softmax_lse, S_dmask, fwd_blockmask_uint64, rng_state = _wrapped_infllmv2_attn_varlen_forward(
305	            q,
306	            k,
307	            v,
308	            cu_seqlens_q,
309	            cu_seqlens_k,
310	            max_seqlen_q,
311	            max_seqlen_k,
312	            dropout_p,
313	            softmax_scale,
314	            causal=causal,
315	            window_size_left=window_size[0],
316	            window_size_right=window_size[1],
317	            softcap=softcap,
318	            alibi_slopes=alibi_slopes,
319	            return_softmax=return_softmax and dropout_p > 0,
320	            block_table=block_table,
321	            topk_idx=topk_idx,
322	        )
323	        ctx.save_for_backward(
324	            q, k, v, out_padded, softmax_lse, cu_seqlens_q, cu_seqlens_k, fwd_blockmask_uint64, rng_state
325	        )
326	        ctx.dropout_p = dropout_p
327	        ctx.max_seqlen_q = max_seqlen_q
328	        ctx.max_seqlen_k = max_seqlen_k
329	        ctx.softmax_scale = softmax_scale
330	        ctx.causal = causal
331	        ctx.window_size = window_size
332	        ctx.softcap = softcap
333	        ctx.alibi_slopes = alibi_slopes
334	        ctx.deterministic = deterministic
335	        ctx.topk_idx = topk_idx
336	        out = out_padded[..., :head_size_og]
337	        return out if not return_softmax else (out, softmax_lse, S_dmask)
338	
339	    def backward(ctx, dout, *args):
340	        q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, fwd_blockmask_uint64, rng_state = ctx.saved_tensors
341	        dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
342	        bwd_blockmask_uint64 = None
343	        if fwd_blockmask_uint64 is not None:
344	            fwd_blockmask_bool = cuda_uint64_to_bool(fwd_blockmask_uint64, (ctx.max_seqlen_k + 64- 1) // 64) 
345	            # Ensure the tensor is contiguous in memory after transpose
346	            transposed_blockmask = fwd_blockmask_bool.transpose(1, 2).contiguous()
347	            # Synchronize CUDA stream before conversion
348	            torch.cuda.synchronize()
349	            # Convert to uint64
350	            bwd_blockmask_uint64, _ = cuda_blockmask_to_uint64(transposed_blockmask)
351	        
352	        head_size_og = dout.size(2)
353	        dout_padded = dout
354	        if head_size_og % 8 != 0:
355	            dout_padded = torch.nn.functional.pad(dout, [0, 8 - head_size_og % 8])
356	        _wrapped_infllmv2_attn_varlen_backward(
357	            dout_padded,
358	            q,
359	            k,
360	            v,
361	            out,
362	            softmax_lse,
363	            dq,
364	            dk,
365	            dv,
366	            cu_seqlens_q,
367	            cu_seqlens_k,
368	            ctx.max_seqlen_q,
369	            ctx.max_seqlen_k,
370	            ctx.dropout_p,
371	            ctx.softmax_scale,
372	            ctx.causal,
373	            ctx.window_size[0],
374	            ctx.window_size[1],
375	            ctx.softcap,
376	            ctx.alibi_slopes,
377	            ctx.deterministic,
378	            bwd_blockmask_uint64,  # Use the uint64 matrix directly
379	            rng_state=rng_state,
380	        )
381	        dq = dq[..., : dout.shape[-1]]  # We could have padded the head dimension
382	        dk = dk[..., : dout.shape[-1]]
383	        dv = dv[..., : dout.shape[-1]]
384	
385	        return dq, dk, dv, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
386	
387	
388	def infllmv2_attn_varlen_func(
389	    q,
390	    k,
391	    v,
392	    cu_seqlens_q,
393	    cu_seqlens_k,
394	    max_seqlen_q,
395	    max_seqlen_k,
396	    dropout_p=0.0,
397	    softmax_scale=None,
398	    causal=False,
399	    window_size=(-1, -1),  # -1 means infinite context window
400	    softcap=0.0, # 0.0 means deactivated
401	    alibi_slopes=None,
402	    deterministic=False,
403	    return_attn_probs=False,
404	    block_table=None,
405	    topk_idx=None,
406	):
407	    """dropout_p should be set to 0.0 during evaluation
408	    Supports multi-query and grouped-query attention (MQA/GQA) by passing in K, V with fewer heads
409	    than Q. Note that the number of heads in Q must be divisible by the number of heads in KV.
410	    For example, if Q has 6 heads and K, V have 2 heads, head 0, 1, 2 of Q will attention to head
411	    0 of K, V, and head 3, 4, 5 of Q will attention to head 1 of K, V.
412	
413	    If causal=True, the causal mask is aligned to the bottom right corner of the attention matrix.
414	    For example, if seqlen_q = 2 and seqlen_k = 5, the causal mask (1 = keep, 0 = masked out) is:
415	        1 1 1 1 0
416	        1 1 1 1 1
417	    If seqlen_q = 5 and seqlen_k = 2, the causal mask is:
418	        0 0
419	        0 0
420	        0 0
421	        1 0
422	        1 1
423	    If the row of the mask is all zero, the output will be zero.
424	
425	    If window_size != (-1, -1), implements sliding window local attention. Query at position i
426	    will only attend to keys between
427	    [i + seqlen_k - seqlen_q - window_size[0], i + seqlen_k - seqlen_q + window_size[1]] inclusive.
428	
429	    Arguments:
430	        q: (total_q, nheads, headdim), where total_q = total number of query tokens in the batch.
431	        k: (total_k, nheads_k, headdim), where total_k = total number of key tokens in the batch.
432	        v: (total_k, nheads_k, headdim), where total_k = total number of key tokens in the batch.
433	        cu_seqlens_q: (batch_size + 1,), dtype torch.int32. The cumulative sequence lengths
434	           of the sequences in the batch, used to index into q.
435	        cu_seqlens_k: (batch_size + 1,), dtype torch.int32. The cumulative sequence lengths
436	           of the sequences in the batch, used to index into kv.
437	        max_seqlen_q: int. Maximum query sequence length in the batch.
438	        max_seqlen_k: int. Maximum key sequence length in the batch.
439	        dropout_p: float. Dropout probability.
440	        softmax_scale: float. The scaling of QK^T before applying softmax.
441	            Default to 1 / sqrt(headdim).
442	        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
443	        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
444	        softcap: float. Anything > 0 activates softcapping attention.
445	        alibi_slopes: (nheads,) or (batch_size, nheads), fp32. A bias of
446	            (-alibi_slope * |i + seqlen_k - seqlen_q - j|)
447	            is added to the attention score of query i and key j.
448	        deterministic: bool. Whether to use the deterministic implementation of the backward pass,
449	            which is slightly slower and uses more memory. The forward pass is always deterministic.
450	        return_attn_probs: bool. Whether to return the attention probabilities. This option is for
451	           testing only. The returned probabilities are not guaranteed to be correct
452	           (they might not have the right scaling).
453	    Return:
454	        out: (total, nheads, headdim).
455	        softmax_lse [optional, if return_attn_probs=True]: (nheads, total_q_seqlen). The
456	            logsumexp of each row of the matrix QK^T * scaling (e.g., log of the softmax
457	            normalization factor).
458	        S_dmask [optional, if return_attn_probs=True]: (batch_size, nheads, seqlen, seqlen).
459	            The output of softmax (possibly with different scaling). It also encodes the dropout
460	            pattern (negative means that location was dropped, nonnegative means it was kept).
461	    """
462	    return Infllmv2AttnVarlenFunc.apply(
463	        q,
464	        k,
465	        v,
466	        cu_seqlens_q,
467	        cu_seqlens_k,
468	        max_seqlen_q,
469	        max_seqlen_k,
470	        dropout_p,
471	        softmax_scale,
472	        causal,
473	        window_size,
474	        softcap,
475	        alibi_slopes,
476	        deterministic,
477	        return_attn_probs,
478	        block_table,
479	        topk_idx,
480	    )
481	
482	
483	def infllmv2_attn_stage1(
484	    q,
485	    k,
486	    v,
487	    cu_seqlens_q,
488	    cu_seqlens_k,
489	    cu_seqlens_v,
490	    max_seqlen_q,
491	    max_seqlen_k,
492	    dropout_p=0.0,
493	    softmax_scale=None,
494	    causal=False,
495	    window_size=(-1, -1),  # -1 means infinite context window
496	    softcap=0.0, # 0.0 means deactivated
497	    alibi_slopes=None,
498	    deterministic=False,
499	    return_attn_probs=True,
500	    block_table=None,
501	):
502	    """
503	    Neighborhood Sparse Attention (NSA) Stage 1 with varlen support.
504	    
505	    This function performs the first stage of NSA, computing attention scores
506	    with a specific sparsity pattern where queries are grouped and only attend
507	    to a subset of keys.
508	    
509	    Arguments:
510	        q: (total_q, nheads, headdim), where total_q = total number of query tokens in the batch.
511	        k: (total_k, nheads_k, headdim), where total_k = total number of key tokens in the batch.
512	        v: (total_k, nheads_k, headdim), where total_k = total number of key tokens in the batch.
513	        cu_seqlens_q: (batch_size + 1,), dtype torch.int32. The cumulative sequence lengths
514	           of the sequences in the batch, used to index into q.
515	        cu_seqlens_k: (batch_size + 1,), dtype torch.int32. The cumulative sequence lengths
516	           of the sequences in the batch, used to index into k.
517	        cu_seqlens_v: (batch_size + 1,), dtype torch.int32. The cumulative sequence lengths
518	           of the sequences in the batch, used to index into v.
519	        max_seqlen_q: int. Maximum query sequence length in the batch.
520	        max_seqlen_k: int. Maximum key sequence length in the batch. 
521	            This is the k1_cache_len calculated based on the maximum context length, not based on the current k1 length.
522	        dropout_p: float. Dropout probability.
523	        softmax_scale: float. The scaling of QK^T before applying softmax.
524	            Default to 1 / sqrt(headdim).
525	        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
526	        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
527	        softcap: float. Anything > 0 activates softcapping attention.
528	        alibi_slopes: (nheads,) or (batch_size, nheads), fp32. A bias of
529	            (-alibi_slope * |i + seqlen_k - seqlen_q - j|)
530	            is added to the attention score of query i and key j.
531	        deterministic: bool. Whether to use the deterministic implementation.
532	        return_attn_probs: bool. Whether to return the attention probabilities.
533	        block_table: Optional block table for paged attention.
534	        nsa_group_size: int. Number of groups for neighborhood sparse attention.
535	        nsa_heads_per_group: int. Number of heads per group.
536	        
537	    Return:
538	        S_dmask: The attention scores/probabilities matrix with NSA sparsity pattern.
539	                 Shape: (num_heads_k, total_q, max_seqlen_k)
540	                 Note: max_seqlen_k is set to 2048 by default in the C++ implementation.
541	    """
542	    if softmax_scale is None:
543	        softmax_scale = q.shape[-1] ** (-0.5)
544	    
545	    # max_seqlen_k is set to 2048 by default in the C++ implementation
546	    # max_seqlen_k = 2048
547	    
548	    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
549	    
550	    # Get dimensions
551	    total_q, nheads, head_dim = q.shape
552	    # batch_size = cu_seqlens_q.numel() - 1
553	    nheads_k = k.shape[1]
554	    nheads_per_group = nheads // nheads_k
555	    
556	    # Reshape query for NSA pattern
557	    # From (total_q, nsa_group_size * nsa_heads_per_group, head_dim)
558	    # To (total_q * nsa_group_size, nsa_heads_per_group, head_dim)
559	    q = q.reshape(total_q, nheads_k, nheads_per_group, head_dim)
560	    q = q.transpose(1, 2).reshape(total_q * nheads_per_group, nheads_k, head_dim).contiguous()
561	    
562	    # Adjust cu_seqlens and max_seqlen for the reshaped query
563	    # cu_seqlens_q_adjusted = cu_seqlens_q * nheads_per_group
564	    # max_seqlen_q_adjusted = max_seqlen_q * nheads_per_group
565	
566	    # Call the underlying CUDA kernel
567	    result = infllm_cuda.varlen_fwd_stage1(
568	        q,
569	        k,
570	        v,
571	        None,
572	        cu_seqlens_q,
573	        cu_seqlens_k,
574	        cu_seqlens_v,
575	        None,
576	        None,
577	        block_table,
578	        alibi_slopes,
579	        max_seqlen_q,
580	        max_seqlen_k,
581	        dropout_p,
582	        softmax_scale,
583	        True,
584	        causal,
585	        window_size[0],
586	        window_size[1],
587	        softcap,
588	        True,
589	        None,
590	    )
591	    
592	    # S_dmask = result[0] if isinstance(result, list) else result
593	    # S_dmask = S_dmask[:,:, :max_seqlen_k]
594	    # S_dmask = torch.where(torch.isnan(S_dmask), 0, S_dmask)
595	    # if return_attn_probs and S_dmask is not None:
596	    #     # The kernel now returns shape (num_heads_k, total_q, max_seqlen_k)
597	    #     assert S_dmask.shape == (nheads_k, total_q, max_seqlen_k), \
598	    #         f"Expected shape ({nheads_k}, {total_q}, {max_seqlen_k}), got {S_dmask.shape}"
599	        # TODO causal masking with first block -inf
600	        # Apply causal masking if needed
601	        # if causal:
602	        #     # Calculate the stride for masking
603	        #     stride = nsa_heads_per_group * nsa_group_size
604	        #     mask_size = stride - 1
605	            
606	            # Apply masking based on the output shape
607	            # S_dmask shape is (num_heads_k, total_q, max_seqlen_k)
608	            # if S_dmask.shape[1] > mask_size:  # total_q dimension
609	            #     S_dmask[:, :mask_size, :] = float('-inf')
610	    
611	    return result[0]
612	
613	
614	def infllmv2_attn_with_kvcache(
615	    q,
616	    k_cache,
617	    v_cache,
618	    k=None,
619	    v=None,
620	    rotary_cos=None,
621	    rotary_sin=None,
622	    cache_seqlens: Optional[Union[(int, torch.Tensor)]] = None,
623	    cache_batch_idx: Optional[torch.Tensor] = None,
624	    cache_leftpad: Optional[torch.Tensor] = None,
625	    block_table: Optional[torch.Tensor] = None,
626	    softmax_scale=None,
627	    causal=False,
628	    window_size=(-1, -1),  # -1 means infinite context window
629	    softcap=0.0, # 0.0 means deactivated
630	    rotary_interleaved=True,
631	    alibi_slopes=None,
632	    num_splits=0,
633	    return_softmax_lse=False,
634	    topk_idx=None,
635	):
636	    """
637	    If k and v are not None, k_cache and v_cache will be updated *inplace* with the new values from
638	    k and v. This is useful for incremental decoding: you can pass in the cached keys/values from
639	    the previous step, and update them with the new keys/values from the current step, and do
640	    attention with the updated cache, all in 1 kernel.
641	
642	    If you pass in k / v, you must make sure that the cache is large enough to hold the new values.
643	    For example, the KV cache could be pre-allocated with the max sequence length, and you can use
644	    cache_seqlens to keep track of the current sequence lengths of each sequence in the batch.
645	
646	    Also apply rotary embedding if rotary_cos and rotary_sin are passed in. The key @k will be
647	    rotated by rotary_cos and rotary_sin at indices cache_seqlens, cache_seqlens + 1, etc.
648	    If causal or local (i.e., window_size != (-1, -1)), the query @q will be rotated by rotary_cos
649	    and rotary_sin at indices cache_seqlens, cache_seqlens + 1, etc.
650	    If not causal and not local, the query @q will be rotated by rotary_cos and rotary_sin at
651	    indices cache_seqlens only (i.e. we consider all tokens in @q to be at position cache_seqlens).
652	
653	    See tests/test_flash_attn.py::test_flash_attn_kvcache for examples of how to use this function.
654	
655	    Supports multi-query and grouped-query attention (MQA/GQA) by passing in KV with fewer heads
656	    than Q. Note that the number of heads in Q must be divisible by the number of heads in KV.
657	    For example, if Q has 6 heads and K, V have 2 heads, head 0, 1, 2 of Q will attention to head
658	    0 of K, V, and head 3, 4, 5 of Q will attention to head 1 of K, V.
659	
660	    If causal=True, the causal mask is aligned to the bottom right corner of the attention matrix.
661	    For example, if seqlen_q = 2 and seqlen_k = 5, the causal mask (1 = keep, 0 = masked out) is:
662	        1 1 1 1 0
663	        1 1 1 1 1
664	    If seqlen_q = 5 and seqlen_k = 2, the causal mask is:
665	        0 0
666	        0 0
667	        0 0
668	        1 0
669	        1 1
670	    If the row of the mask is all zero, the output will be zero.
671	
672	    If window_size != (-1, -1), implements sliding window local attention. Query at position i
673	    will only attend to keys between
674	    [i + seqlen_k - seqlen_q - window_size[0], i + seqlen_k - seqlen_q + window_size[1]] inclusive.
675	
676	    Note: Does not support backward pass.
677	
678	    Arguments:
679	        q: (batch_size, seqlen, nheads, headdim)
680	        k_cache: (batch_size_cache, seqlen_cache, nheads_k, headdim) if there's no block_table,
681	            or (num_blocks, page_block_size, nheads_k, headdim) if there's a block_table (i.e. paged KV cache)
682	            page_block_size must be a multiple of 256.
683	        v_cache: (batch_size_cache, seqlen_cache, nheads_k, headdim) if there's no block_table,
684	            or (num_blocks, page_block_size, nheads_k, headdim) if there's a block_table (i.e. paged KV cache)
685	        k [optional]: (batch_size, seqlen_new, nheads_k, headdim). If not None, we concatenate
686	            k with k_cache, starting at the indices specified by cache_seqlens.
687	        v [optional]: (batch_size, seqlen_new, nheads_k, headdim). Similar to k.
688	        rotary_cos [optional]: (seqlen_ro, rotary_dim / 2). If not None, we apply rotary embedding
689	            to k and q. Only applicable if k and v are passed in. rotary_dim must be divisible by 16.
690	        rotary_sin [optional]: (seqlen_ro, rotary_dim / 2). Similar to rotary_cos.
691	        cache_seqlens: int, or (batch_size,), dtype torch.int32. The sequence lengths of the
692	            KV cache.
693	        cache_batch_idx: (batch_size,), dtype torch.int32. The indices used to index into the KV cache.
694	            If None, we assume that the batch indices are [0, 1, 2, ..., batch_size - 1].
695	            If the indices are not distinct, and k and v are provided, the values updated in the cache
696	                 might come from any of the duplicate indices.
697	        cache_leftpad: (batch_size,), dtype torch.int32. The index that the KV cache starts. If None, assume 0.
698	        block_table [optional]: (batch_size, max_num_blocks_per_seq), dtype torch.int32.
699	        softmax_scale: float. The scaling of QK^T before applying softmax.
700	            Default to 1 / sqrt(headdim).
701	        causal: bool. Whether to apply causal attention mask (e.g., for auto-regressive modeling).
702	        window_size: (left, right). If not (-1, -1), implements sliding window local attention.
703	        softcap: float. Anything > 0 activates softcapping attention.
704	        rotary_interleaved: bool. Only applicable if rotary_cos and rotary_sin are passed in.
705	            If True, rotary embedding will combine dimensions 0 & 1, 2 & 3, etc. If False,
706	            rotary embedding will combine dimensions 0 & rotary_dim / 2, 1 & rotary_dim / 2 + 1
707	            (i.e. GPT-NeoX style).
708	        alibi_slopes: (nheads,) or (batch_size, nheads), fp32. A bias of
709	            (-alibi_slope * |i + seqlen_k - seqlen_q - j|)
710	            is added to the attention score of query i and key j.
711	        num_splits: int. If > 1, split the key/value into this many chunks along the sequence.
712	           If num_splits == 1, we don't split the key/value. If num_splits == 0, we use a heuristic
713	           to automatically determine the number of splits.
714	           Don't change this unless you know what you are doing.
715	        return_softmax_lse: bool. Whether to return the logsumexp of the attention scores.
716	
717	    Return:
718	        out: (batch_size, seqlen, nheads, headdim).
719	        softmax_lse [optional, if return_softmax_lse=True]: (batch_size, nheads, seqlen). The
720	            logsumexp of each row of the matrix QK^T * scaling (e.g., log of the softmax
721	            normalization factor).
722	    """
723	    assert k_cache.stride(-1) == 1, "k_cache must have contiguous last dimension"
724	    assert v_cache.stride(-1) == 1, "v_cache must have contiguous last dimension"
725	    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
726	    if softmax_scale is None:
727	        softmax_scale = q.shape[-1] ** (-0.5)
728	    if cache_seqlens is not None and isinstance(cache_seqlens, int):
729	        cache_seqlens = torch.full(
730	            (k_cache.shape[0],), cache_seqlens, dtype=torch.int32, device=k_cache.device
731	        )
732	        cache_seqlens = maybe_contiguous(cache_seqlens)
733	    cache_batch_idx = maybe_contiguous(cache_batch_idx)
734	    block_table = maybe_contiguous(block_table)
735	    if topk_idx is not None:
736	        assert topk_idx.dtype == torch.int32
737	        blockmask, _ = cuda_topk_to_uint64(topk_idx, k_cache.shape[1] if block_table is None else block_table.shape[1] * k_cache.shape[1], 64) # N_BLOCK_DIM=64
738	    else:
739	        blockmask = None
740	    out, softmax_lse = infllm_cuda.fwd_kvcache(
741	        q,
742	        k_cache,
743	        v_cache,
744	        k,
745	        v,
746	        cache_seqlens,
747	        rotary_cos,
748	        rotary_sin,
749	        cache_batch_idx,
750	        cache_leftpad,
751	        block_table,
752	        alibi_slopes,
753	        None,
754	        softmax_scale,
755	        causal,
756	        window_size[0],
757	        window_size[1],
758	        softcap,
759	        rotary_interleaved,
760	        num_splits,
761	        blockmask,
762	    )
763	    return (out, softmax_lse) if return_softmax_lse else out
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/blockmask_to_uint64.py"
}
```

> TOOL

tool_result Read
```
1	import torch
2	from typing import Tuple
3	from . import C
4	
5	def blockmask_to_uint64(blockmask: torch.Tensor) -> Tuple[torch.Tensor, int]:
6	    """
7	    Convert PyTorch boolean mask to uint64 representation using CUDA kernel
8	    
9	    Args:
10	        blockmask: Boolean PyTorch tensor
11	        
12	    Returns:
13	        Tuple of:
14	            uint64_arrays: Tensor with the same batch dimensions but last dim replaced with uint64 values
15	            last_dim_size: Original size of the last dimension
16	    """
17	    # Record original shape
18	    original_shape = blockmask.shape
19	    last_dim_size = original_shape[-1]
20	    
21	    # Compute how many uint64 values are needed per row
22	    n_uint64_per_row = (last_dim_size + 63) // 64
23	    
24	    # Flatten all batch dimensions
25	    flat_dims = torch.prod(torch.tensor(original_shape[:-1], dtype=torch.int64)).item()
26	    flat_blockmask = blockmask.reshape(flat_dims, last_dim_size)
27	    
28	    # Create output tensor
29	    output_shape = original_shape[:-1] + (n_uint64_per_row,)
30	    result = torch.zeros(output_shape, dtype=torch.int64, device=blockmask.device)
31	    flat_result = result.reshape(flat_dims, n_uint64_per_row)
32	    
33	    # Call CUDA kernel
34	    C.blockmask_to_uint64(
35	        torch.cuda.current_stream().cuda_stream,
36	        flat_blockmask.data_ptr(),
37	        flat_result.data_ptr(),
38	        flat_dims,
39	        last_dim_size,
40	        n_uint64_per_row
41	    )
42	    
43	    return result, last_dim_size
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py"
}
```

> TOOL

tool_result Read
```
1	import torch
2	
3	import warnings
4	from . import C
5	
6	def max_pooling_1d(
7	    input: torch.Tensor, # num_heads x q_len x k_len
8	    cache_len: int,
9	    local_blocks: int,
10	    init_blocks: int,
11	    block_size: int = 64,
12	    stride: int = 16,
13	) -> torch.Tensor:
14	    assert input.dtype == torch.float16 or input.dtype == torch.bfloat16
15	    input = input.contiguous()
16	    stride = block_size // stride
17	    kernel_size = stride + 1
18	    padding = 1
19	    num_heads = input.shape[0]
20	    q_len = input.shape[1]
21	    k_len = input.shape[2]
22	    total_len = q_len + cache_len
23	    out_len = (total_len + block_size - 1) // block_size
24	    output = torch.zeros(num_heads, q_len, out_len, device=input.device, dtype=input.dtype)
25	    with torch.cuda.device(input.device):
26	        stream = torch.cuda.current_stream().cuda_stream
27	        C.max_pooling_1d(
28	            stream,
29	            input.data_ptr(),
30	            output.data_ptr(),
31	            input.dtype == torch.bfloat16,
32	            num_heads,
33	            q_len,
34	            k_len,
35	            out_len,
36	            cache_len,
37	            kernel_size,
38	            stride,
39	            padding,
40	            block_size,
41	            local_blocks,
42	            init_blocks,
43	        )
44	    
45	    # Log device information before return
46	    # print(f"max_pooling_1d - input device: {input.device}, output device: {output.device}")
47	    
48	    return output
49	
50	
51	def max_pooling_1d_varlen(
52	    input: torch.Tensor, # num_heads x total_q x max_k
53	    cu_seqlens_q: torch.Tensor, # batch_size + 1
54	    cu_seqlens_k: torch.Tensor, # batch_size + 1
55	    cache_lens: torch.Tensor, # batch_size
56	    max_seqlen_q: int,
57	    max_context_len: int,
58	    local_blocks: int,
59	    init_blocks: int,
60	    block_size: int = 64,
61	    stride: int = 16,
62	    total_q: int = -1,
63	) -> torch.Tensor:
64	    """
65	    Variable-length version of max_pooling_1d that handles packed sequences.
66	    
67	    Args:
68	        input: Tensor of shape (num_heads, total_q, max_k) where:
69	               - total_q is sum of all query sequence lengths
70	               - max_k is the maximum key sequence length (padded)
71	        cu_seqlens_q: Cumulative sequence lengths for queries (batch_size + 1,)
72	        cu_seqlens_k: Cumulative sequence lengths for keys (batch_size + 1,)
73	        cache_lens: Cache lengths for each sequence in the batch (batch_size,)
74	        max_seqlen_q: Maximum query sequence length in the batch
75	        local_blocks: Number of local blocks for window attention
76	        init_blocks: Number of initial blocks to mask with inf
77	        block_size: Block size (default: 64)
78	        stride: Stride for pooling (default: 16)
79	    
80	    Returns:
81	        output: Tensor of shape (num_heads, total_q, out_len)
82	    """
83	    assert input.dtype == torch.float16 or input.dtype == torch.bfloat16
84	    assert cu_seqlens_q.dtype == torch.int32
85	    assert cu_seqlens_k.dtype == torch.int32
86	    assert cache_lens.dtype == torch.int32
87	    assert input.dim() == 3, f"Expected 3D input, got {input.dim()}D"
88	    
89	    input = input.contiguous()
90	    cu_seqlens_q = cu_seqlens_q.contiguous()
91	    cu_seqlens_k = cu_seqlens_k.contiguous()
92	    cache_lens = cache_lens.contiguous()
93	    
94	    # TODO: Based on the passed parameters in hf code, 
95	    # the stride passed in should be the stride used during compress k1. 
96	    # This differs from the kernel comment and requires subsequent verification.
97	    max_seqlen_k = max_context_len // stride
98	    out_len = (max_context_len + block_size - 1) // block_size
99	    
100	    stride = block_size // stride
101	    kernel_size = stride + 1
102	    padding = 1
103	    
104	    batch_size = cu_seqlens_q.shape[0] - 1
105	    num_heads = input.shape[0]
106	    total_q = input.shape[1]
107	    
108	    # Verify dimensions
109	    # assert cu_seqlens_q[-1].item() == total_q, f"total_q mismatch: {cu_seqlens_q[-1].item()} vs {total_q}"
110	    # assert cache_lens.shape[0] == batch_size, f"cache_lens batch size mismatch: {cache_lens.shape[0]} vs {batch_size}"
111	    
112	    # Calculate output length based on max sequence length and max cache length
113	    # max_cache_len = cache_lens.max().item()
114	    # total_len = max_seqlen_q + max_cache_len
115	    # out_len = (total_len + block_size - 1) // block_size
116	    
117	    # Read this static const variable from config.json in advance
118	    # max_context_len = 32768
119	    
120	    # WARNING: 为了适配 CUDA Graph，max_seqlen_k 已在 C 代码中硬编码为 2048
121	    # warnings.warn(
122	    #     "max_pooling_1d_varlen: max_seqlen_k is hardcoded to 2048 in C code to accommodate CUDA Graph. "
123	    #     "This may over-allocate memory. TODO: Dynamically set this according to real input requirements.",
124	    #     UserWarning
125	    # )
126	    
127	    # TODO: modify this to out.zeros_()
128	    output = torch.zeros(num_heads, total_q, out_len, device=input.device, dtype=input.dtype)
129	    with torch.cuda.device(input.device):
130	        stream = torch.cuda.current_stream(input.device).cuda_stream
131	        C.max_pooling_1d_varlen(
132	            stream,
133	            input.data_ptr(),
134	            output.data_ptr(),
135	            cu_seqlens_q.data_ptr(),
136	            cu_seqlens_k.data_ptr(),
137	            cache_lens.data_ptr(),
138	            input.dtype == torch.bfloat16,
139	            batch_size,
140	            num_heads,
141	            max_seqlen_q,
142	            max_seqlen_k,
143	            out_len,
144	            kernel_size,
145	            stride,
146	            padding,
147	            block_size,
148	            local_blocks,
149	            init_blocks,
150	            total_q,
151	        )
152	    
153	    # Log device information before return
154	    #print(f"max_pooling_1d_varlen - input device: {input.device}, output device: {output.device}")
155	    
156	    return output
157	
158	
159	def max_pooling_1d_varlen_v2(
160	    input: torch.Tensor, # num_heads x total_q x max_k
161	    cu_seqlens_q: torch.Tensor, # batch_size + 1
162	    cu_seqlens_k: torch.Tensor, # batch_size + 1
163	    cache_lens: torch.Tensor, # batch_size
164	    max_seqlen_q: int,
165	    local_blocks: int,
166	    init_blocks: int,
167	    block_size: int = 64,
168	    stride: int = 16,
169	    total_q: int = -1,
170	) -> torch.Tensor:
171	    """
172	    Variable-length version of max_pooling_1d that handles packed sequences.
173	    
174	    Args:
175	        input: Tensor of shape (num_heads, total_q, max_k) where:
176	               - total_q is sum of all query sequence lengths
177	               - max_k is the maximum key sequence length (padded)
178	        cu_seqlens_q: Cumulative sequence lengths for queries (batch_size + 1,)
179	        cu_seqlens_k: Cumulative sequence lengths for keys (batch_size + 1,)
180	        cache_lens: Cache lengths for each sequence in the batch (batch_size,)
181	        max_seqlen_q: Maximum query sequence length in the batch
182	        local_blocks: Number of local blocks for window attention
183	        init_blocks: Number of initial blocks to mask with inf
184	        block_size: Block size (default: 64)
185	        stride: Stride for pooling (default: 16)
186	    
187	    Returns:
188	        output: Tensor of shape (num_heads, total_q, out_len)
189	    """
190	    from . import _C
191	
192	    assert input.dtype == torch.float16 or input.dtype == torch.bfloat16
193	    assert cu_seqlens_q.dtype == torch.int32
194	    assert cu_seqlens_k.dtype == torch.int32
195	    assert cache_lens.dtype == torch.int32
196	    assert input.dim() == 3, f"Expected 3D input, got {input.dim()}D"
197	    
198	    input = input.contiguous()
199	    cu_seqlens_q = cu_seqlens_q.contiguous()
200	    cu_seqlens_k = cu_seqlens_k.contiguous()
201	    cache_lens = cache_lens.contiguous()
202	    
203	    stride = block_size // stride
204	    kernel_size = stride + 1
205	    padding = 1
206	    
207	    batch_size = cu_seqlens_q.shape[0] - 1
208	    num_heads = input.shape[0]
209	    total_q = input.shape[1]
210	    
211	    # Verify dimensions
212	    assert cu_seqlens_q[-1].item() == total_q, f"total_q mismatch: {cu_seqlens_q[-1].item()} vs {total_q}"
213	    assert cache_lens.shape[0] == batch_size, f"cache_lens batch size mismatch: {cache_lens.shape[0]} vs {batch_size}"
214	    
215	    # Calculate output length based on max sequence length and max cache length
216	    # max_cache_len = cache_lens.max().item()
217	    # total_len = max_seqlen_q + max_cache_len
218	    # out_len = (total_len + block_size - 1) // block_size
219	    
220	    # Read this static const variable from config.json in advance
221	    max_context_len = 32768
222	    out_len = (max_context_len + block_size - 1) // block_size
223	    
224	    # WARNING: 为了适配 CUDA Graph，max_seqlen_k 已在 C 代码中硬编码为 2048
225	    # warnings.warn(
226	    #     "max_pooling_1d_varlen: max_seqlen_k is hardcoded to 2048 in C code to accommodate CUDA Graph. "
227	    #     "This may over-allocate memory. TODO: Dynamically set this according to real input requirements.",
228	    #     UserWarning
229	    # )
230	    
231	    # TODO: modify this to out.zeros_()
232	    output = torch.zeros(num_heads, total_q, out_len, device=input.device, dtype=input.dtype)
233	    _C.max_pooling_1d_varlen_v2(
234	        input,
235	        output,
236	        cu_seqlens_q,
237	        cu_seqlens_k,
238	        cache_lens,
239	        input.dtype == torch.bfloat16,
240	        batch_size,
241	        num_heads,
242	        max_seqlen_q,
243	        out_len,
244	        kernel_size,
245	        stride,
246	        padding,
247	        block_size,
248	        local_blocks,
249	        init_blocks,
250	        total_q,
251	    )
252	        
253	    
254	    # Log device information before return
255	    #print(f"max_pooling_1d_varlen - input device: {input.device}, output device: {output.device}")
256	    
257	    return output
258	
259
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/topk_to_uint64.py"
}
```

> TOOL

tool_result Read
```
1	import torch
2	from typing import Tuple, Optional
3	from . import C
4	
5	def topk_to_uint64(topk_idx: torch.Tensor, max_seqlen_k: int, block_size: int, 
6	                   memory_buffer: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, int]:
7	    """
8	    Convert topk indices directly to uint64 representation without intermediate bool mask
9	    
10	    Args:
11	        topk_idx: Tensor of shape [batch, num_heads, total_seqlen, k] or [num_heads, total_seqlen, k]
12	                 containing block indices
13	        max_seqlen_k: Maximum sequence length for keys
14	        block_size: Size of each block
15	        memory_buffer: Optional pre-allocated buffer to reuse. If provided and has correct shape,
16	                      it will be used instead of allocating new memory.
17	        
18	    Returns:
19	        Tuple of:
20	            uint64_arrays: Tensor with the same batch dimensions but last dim replaced with uint64 values
21	            k_blocks: Number of key blocks
22	    """
23	    assert topk_idx.dtype == torch.int32
24	    # Calculate key blocks
25	    k_blocks = (max_seqlen_k + block_size - 1) // block_size  # Ceiling division
26	    
27	    # Record original shape
28	    original_shape = topk_idx.shape
29	    
30	    # Check if we have a batch dimension
31	    has_batch = len(original_shape) == 4
32	    
33	    if has_batch:
34	        batch_size, num_heads, total_seqlen, k = original_shape
35	    else:
36	        num_heads, total_seqlen, k = original_shape
37	        batch_size = 1
38	    
39	    # Compute how many uint64 values are needed per row
40	    n_uint64_per_row = (k_blocks + 63) // 64
41	    # Flatten batch dimensions
42	    if has_batch:
43	        flat_dims = batch_size * num_heads * total_seqlen
44	        
45	        # Create output tensor
46	        output_shape = (batch_size, num_heads, total_seqlen, n_uint64_per_row)
47	    else:
48	        flat_dims = num_heads * total_seqlen
49	        
50	        # Create output tensor
51	        output_shape = (num_heads, total_seqlen, n_uint64_per_row)
52	    
53	    # Check if we can reuse the provided memory buffer
54	    with torch.cuda.device(topk_idx.device):
55	        stream = torch.cuda.current_stream().cuda_stream
56	        result = torch.zeros(output_shape, dtype=torch.int64, device=topk_idx.device)
57	    
58	        # Call CUDA kernel
59	        C.topk_to_uint64(
60	            stream,
61	            topk_idx.data_ptr(),
62	            result.data_ptr(),
63	            flat_dims,
64	            k,
65	            k_blocks,
66	            n_uint64_per_row
67	        )
68	    
69	    # Log device information before return
70	    #print(f"topk_to_uint64 - input device: {topk_idx.device}, output device: {result.device}")
71	    
72	    return result, k_blocks
73	
74	
75	    """
76	    A class that manages memory buffer for topk_to_uint64 conversions.
77	    This can improve performance by reusing memory across multiple calls.
78	    """
79	    
80	    def __init__(self):
81	        self.memory_buffer = None
82	    
83	    def convert(self, topk_idx: torch.Tensor, max_seqlen_k: int, block_size: int) -> Tuple[torch.Tensor, int]:
84	        """
85	        Convert topk indices to uint64 representation, reusing memory buffer when possible.
86	        
87	        Args:
88	            topk_idx: Tensor of shape [batch, num_heads, total_seqlen, k] or [num_heads, total_seqlen, k]
89	                     containing block indices
90	            max_seqlen_k: Maximum sequence length for keys
91	            block_size: Size of each block
92	            
93	        Returns:
94	            Tuple of:
95	                uint64_arrays: Tensor with the same batch dimensions but last dim replaced with uint64 values
96	                k_blocks: Number of key blocks
97	        """
98	        result, k_blocks = topk_to_uint64(topk_idx, max_seqlen_k, block_size, self.memory_buffer)
99	        # Update our memory buffer reference for next time
100	        self.memory_buffer = result
101	        return result, k_blocks
102	    
103	    def clear_memory(self):
104	        """Clear the internal memory buffer"""
105	        self.memory_buffer = None
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/uint64_to_bool.py"
}
```

> TOOL

tool_result Read
```
1	import torch
2	from typing import Tuple
3	from . import C
4	
5	def uint64_to_bool(uint64_array: torch.Tensor, last_dim_size: int) -> torch.Tensor:
6	    """
7	    Convert uint64 representation back to PyTorch boolean mask using CUDA kernel
8	    
9	    Args:
10	        uint64_array: Tensor with uint64 values
11	        last_dim_size: Original size of the last dimension
12	        
13	    Returns:
14	        Boolean tensor with the same batch dimensions and last dimension of size last_dim_size
15	    """
16	    # Record original shape of uint64 array
17	    original_shape = uint64_array.shape
18	    n_uint64_per_row = original_shape[-1]
19	    
20	    # Flatten all batch dimensions
21	    flat_dims = torch.prod(torch.tensor(original_shape[:-1], dtype=torch.int64)).item()
22	    flat_uint64_array = uint64_array.reshape(flat_dims, n_uint64_per_row)
23	    
24	    # Create output tensor
25	    output_shape = original_shape[:-1] + (last_dim_size,)
26	    result = torch.zeros(output_shape, dtype=torch.bool, device=uint64_array.device)
27	    flat_result = result.reshape(flat_dims, last_dim_size)
28	    
29	    # Call CUDA kernel
30	    C.uint64_to_bool(
31	        torch.cuda.current_stream().cuda_stream,
32	        flat_uint64_array.data_ptr(),
33	        flat_result.data_ptr(),
34	        flat_dims,
35	        last_dim_size,
36	        n_uint64_per_row
37	    )
38	    
39	    return result
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/setup.py"
}
```

> TOOL

tool_result Read
```
1	import sys
2	import warnings
3	import os
4	import re
5	import ast
6	from pathlib import Path
7	from packaging.version import parse, Version
8	import platform
9	
10	from setuptools import setup, find_packages
11	import subprocess
12	
13	import torch
14	from torch.utils.cpp_extension import (
15	    BuildExtension,
16	    CppExtension,
17	    CUDAExtension,
18	    CUDA_HOME,
19	)
20	
21	# ninja build does not work unless include_dirs are abs path
22	this_dir = os.path.dirname(os.path.abspath(__file__))
23	
24	# FORCE_BUILD: Force a fresh build locally
25	# SKIP_CUDA_BUILD: Intended to allow CI to use a simple `python setup.py sdist` run to copy over raw files, without any cuda compilation
26	FORCE_BUILD = os.getenv("INFLLM_V2_FORCE_BUILD", "FALSE") == "TRUE"
27	SKIP_CUDA_BUILD = os.getenv("INFLLM_V2_SKIP_CUDA_BUILD", "FALSE") == "TRUE"
28	# For CI, we want the option to build with C++11 ABI since the nvcr images use C++11 ABI
29	FORCE_CXX11_ABI = os.getenv("INFLLM_V2_FORCE_CXX11_ABI", "FALSE") == "TRUE"
30	
31	def get_cuda_bare_metal_version(cuda_dir):
32	    raw_output = subprocess.check_output([cuda_dir + "/bin/nvcc", "-V"], universal_newlines=True)
33	    output = raw_output.split()
34	    release_idx = output.index("release") + 1
35	    bare_metal_version = parse(output[release_idx].split(",")[0])
36	
37	    return raw_output, bare_metal_version
38	
39	def check_if_cuda_home_none(global_option: str) -> None:
40	    if CUDA_HOME is not None:
41	        return
42	    # warn instead of error because user could be downloading prebuilt wheels, so nvcc won't be necessary.
43	    warnings.warn(
44	        f"{global_option} was requested, but nvcc was not found.  Are you sure your environment has nvcc available?  "
45	        "If you're installing within a container from https://hub.docker.com/r/pytorch/pytorch, "
46	        "only images whose names contain 'devel' will provide nvcc."
47	    )
48	
49	def append_nvcc_threads(nvcc_extra_args):
50	    # Increase thread count based on available CPU cores
51	    import multiprocessing
52	    num_threads = min(multiprocessing.cpu_count(), 8)  # Use up to 8 threads
53	    return nvcc_extra_args + ["--threads", str(num_threads)]
54	
55	class NinjaBuildExtension(BuildExtension):
56	    def __init__(self, *args, **kwargs) -> None:
57	        # do not override env MAX_JOBS if already exists
58	        if not os.environ.get("MAX_JOBS"):
59	            import psutil
60	
61	            # calculate the maximum allowed NUM_JOBS based on cores
62	            max_num_jobs_cores = max(1, os.cpu_count() // 2)
63	
64	            # calculate the maximum allowed NUM_JOBS based on free memory
65	            free_memory_gb = psutil.virtual_memory().available / (1024 ** 3)  # free memory in GB
66	            max_num_jobs_memory = int(free_memory_gb / 9)  # each JOB peak memory cost is ~8-9GB when threads = 4
67	
68	            # pick lower value of jobs based on cores vs memory metric to minimize oom and swap usage during compilation
69	            max_jobs = max(1, min(max_num_jobs_cores, max_num_jobs_memory))
70	            os.environ["MAX_JOBS"] = str(max_jobs)
71	
72	        super().__init__(*args, **kwargs)
73	
74	cmdclass = {}
75	ext_modules = []
76	
77	if not SKIP_CUDA_BUILD:
78	    print("\n\ntorch.__version__  = {}\n\n".format(torch.__version__))
79	    TORCH_MAJOR = int(torch.__version__.split(".")[0])
80	    TORCH_MINOR = int(torch.__version__.split(".")[1])
81	
82	    # Check, if ATen/CUDAGeneratorImpl.h is found, otherwise use ATen/cuda/CUDAGeneratorImpl.h
83	    # See https://github.com/pytorch/pytorch/pull/70650
84	    generator_flag = []
85	    torch_dir = torch.__path__[0]
86	    if os.path.exists(os.path.join(torch_dir, "include", "ATen", "CUDAGeneratorImpl.h")):
87	        generator_flag = ["-DOLD_GENERATOR_PATH"]
88	
89	    check_if_cuda_home_none("infllm_v2")
90	    # Check, if CUDA11 is installed for compute capability 8.0
91	    cc_flag = []
92	    if CUDA_HOME is not None:
93	        _, bare_metal_version = get_cuda_bare_metal_version(CUDA_HOME)
94	        if bare_metal_version < Version("11.6"):
95	            raise RuntimeError(
96	                "InfLLM V2 is only supported on CUDA 11.6 and above.  "
97	                "Note: make sure nvcc has a supported version by running nvcc -V."
98	            )
99	    
100	    # Auto-detect supported GPU archs based on CUDA toolkit version
101	    # 80: A100 (Ampere), 90: H100 (Hopper, CUDA 11.8+), 120: B100/B200 (Blackwell, CUDA 12.8+)
102	    supported_archs = ["80"]
103	    if CUDA_HOME is not None:
104	        if bare_metal_version >= Version("11.8"):
105	            supported_archs.append("90")
106	        if bare_metal_version >= Version("12.8"):
107	            supported_archs.append("120")
108	
109	    for arch in supported_archs:
110	        cc_flag.extend(["-gencode", f"arch=compute_{arch},code=sm_{arch}"])
111	
112	    # HACK: The compiler flag -D_GLIBCXX_USE_CXX11_ABI is set to be the same as
113	    # torch._C._GLIBCXX_USE_CXX11_ABI
114	    if FORCE_CXX11_ABI:
115	        torch._C._GLIBCXX_USE_CXX11_ABI = True
116	    
117	    # Flash Attention CUDA源文件列表 - 只编译 hdim128, bf16 版本
118	    flash_attn_sources = [
119	                # "csrc/flash_attn/src/flash_fwd_hdim32_fp16_sm80.cu",
120	                # "csrc/flash_attn/src/flash_fwd_hdim32_bf16_sm80.cu",
121	                # "csrc/flash_attn/src/flash_fwd_hdim64_fp16_sm80.cu",
122	                "csrc/flash_attn/src/flash_fwd_hdim64_bf16_sm80.cu",
123	                # "csrc/flash_attn/src/flash_fwd_hdim96_fp16_sm80.cu",
124	                # "csrc/flash_attn/src/flash_fwd_hdim96_bf16_sm80.cu",
125	                # "csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu",
126	                "csrc/flash_attn/src/flash_fwd_hdim128_bf16_sm80.cu",
127	                # "csrc/flash_attn/src/flash_fwd_hdim160_fp16_sm80.cu",
128	                # "csrc/flash_attn/src/flash_fwd_hdim160_bf16_sm80.cu",
129	                # "csrc/flash_attn/src/flash_fwd_hdim192_fp16_sm80.cu",
130	                # "csrc/flash_attn/src/flash_fwd_hdim192_bf16_sm80.cu",
131	                # "csrc/flash_attn/src/flash_fwd_hdim256_fp16_sm80.cu",
132	                # "csrc/flash_attn/src/flash_fwd_hdim256_bf16_sm80.cu",
133	                # "csrc/flash_attn/src/flash_fwd_hdim32_fp16_causal_sm80.cu",
134	                # "csrc/flash_attn/src/flash_fwd_hdim32_bf16_causal_sm80.cu",
135	                # "csrc/flash_attn/src/flash_fwd_hdim64_fp16_causal_sm80.cu",
136	                "csrc/flash_attn/src/flash_fwd_hdim64_bf16_causal_sm80.cu",
137	                # "csrc/flash_attn/src/flash_fwd_hdim96_fp16_causal_sm80.cu",
138	                # "csrc/flash_attn/src/flash_fwd_hdim96_bf16_causal_sm80.cu",
139	                # "csrc/flash_attn/src/flash_fwd_hdim128_fp16_causal_sm80.cu",
140	                "csrc/flash_attn/src/flash_fwd_hdim128_bf16_causal_sm80.cu",
141	                # "csrc/flash_attn/src/flash_fwd_hdim160_fp16_causal_sm80.cu",
142	                # "csrc/flash_attn/src/flash_fwd_hdim160_bf16_causal_sm80.cu",
143	                # "csrc/flash_attn/src/flash_fwd_hdim192_fp16_causal_sm80.cu",
144	                # "csrc/flash_attn/src/flash_fwd_hdim192_bf16_causal_sm80.cu",
145	                # "csrc/flash_attn/src/flash_fwd_hdim256_fp16_causal_sm80.cu",
146	                # "csrc/flash_attn/src/flash_fwd_hdim256_bf16_causal_sm80.cu",
147	                # "csrc/flash_attn/src/flash_bwd_hdim32_fp16_sm80.cu",
148	                # "csrc/flash_attn/src/flash_bwd_hdim32_bf16_sm80.cu",
149	                # "csrc/flash_attn/src/flash_bwd_hdim64_fp16_sm80.cu",
150	                "csrc/flash_attn/src/flash_bwd_hdim64_bf16_sm80.cu",
151	                # "csrc/flash_attn/src/flash_bwd_hdim96_fp16_sm80.cu",
152	                # "csrc/flash_attn/src/flash_bwd_hdim96_bf16_sm80.cu",
153	                # "csrc/flash_attn/src/flash_bwd_hdim128_fp16_sm80.cu",
154	                "csrc/flash_attn/src/flash_bwd_hdim128_bf16_sm80.cu",
155	                # "csrc/flash_attn/src/flash_bwd_hdim160_fp16_sm80.cu",
156	                # "csrc/flash_attn/src/flash_bwd_hdim160_bf16_sm80.cu",
157	                # "csrc/flash_attn/src/flash_bwd_hdim192_fp16_sm80.cu",
158	                # "csrc/flash_attn/src/flash_bwd_hdim192_bf16_sm80.cu",
159	                # "csrc/flash_attn/src/flash_bwd_hdim256_fp16_sm80.cu",
160	                # "csrc/flash_attn/src/flash_bwd_hdim256_bf16_sm80.cu",
161	                # "csrc/flash_attn/src/flash_bwd_hdim32_fp16_causal_sm80.cu",
162	                # "csrc/flash_attn/src/flash_bwd_hdim32_bf16_causal_sm80.cu",
163	                # "csrc/flash_attn/src/flash_bwd_hdim64_fp16_causal_sm80.cu",
164	                "csrc/flash_attn/src/flash_bwd_hdim64_bf16_causal_sm80.cu",
165	                # "csrc/flash_attn/src/flash_bwd_hdim96_fp16_causal_sm80.cu",
166	                # "csrc/flash_attn/src/flash_bwd_hdim96_bf16_causal_sm80.cu",
167	                # "csrc/flash_attn/src/flash_bwd_hdim128_fp16_causal_sm80.cu",
168	                "csrc/flash_attn/src/flash_bwd_hdim128_bf16_causal_sm80.cu",
169	                # "csrc/flash_attn/src/flash_bwd_hdim160_fp16_causal_sm80.cu",
170	                # "csrc/flash_attn/src/flash_bwd_hdim160_bf16_causal_sm80.cu",
171	                # "csrc/flash_attn/src/flash_bwd_hdim192_fp16_causal_sm80.cu",
172	                # "csrc/flash_attn/src/flash_bwd_hdim192_bf16_causal_sm80.cu",
173	                # "csrc/flash_attn/src/flash_bwd_hdim256_fp16_causal_sm80.cu",
174	                # "csrc/flash_attn/src/flash_bwd_hdim256_bf16_causal_sm80.cu",
175	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_sm80.cu",
176	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_sm80.cu",
177	                # "csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_sm80.cu",
178	                "csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_sm80.cu",
179	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_sm80.cu",
180	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_sm80.cu",
181	                # "csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_sm80.cu",
182	                "csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_sm80.cu",
183	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_sm80.cu",
184	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_sm80.cu",
185	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_sm80.cu",
186	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_sm80.cu",
187	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_sm80.cu",
188	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_sm80.cu",
189	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_causal_sm80.cu",
190	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_causal_sm80.cu",
191	                # "csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_causal_sm80.cu",
192	                "csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_causal_sm80.cu",
193	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_causal_sm80.cu",
194	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_causal_sm80.cu",
195	                # "csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_causal_sm80.cu",
196	                "csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_causal_sm80.cu",
197	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_causal_sm80.cu",
198	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_causal_sm80.cu",
199	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_causal_sm80.cu",
200	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_causal_sm80.cu",
201	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_causal_sm80.cu",
202	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_causal_sm80.cu",
203	    ]
204	    
205	    # 过滤掉不存在的文件
206	    existing_flash_attn_sources = []
207	    for source in flash_attn_sources:
208	        if os.path.exists(source):
209	            existing_flash_attn_sources.append(source)
210	    
211	    ext_modules.append(
212	        CUDAExtension(
213	            name="infllm_v2.C",
214	            sources=[
215	                "csrc/entry.cu",
216	                "csrc/flash_attn/flash_api.cpp",
217	            ] + existing_flash_attn_sources,
218	            extra_compile_args={
219	                "cxx": ["-O3", "-std=c++17"],
220	                "nvcc": append_nvcc_threads(
221	                    [
222	                        "-O3",
223	                        "-std=c++17",
224	                        "-U__CUDA_NO_HALF_OPERATORS__",
225	                        "-U__CUDA_NO_HALF_CONVERSIONS__",
226	                        "-U__CUDA_NO_HALF2_OPERATORS__",
227	                        "-U__CUDA_NO_BFLOAT16_CONVERSIONS__",
228	                        "--expt-relaxed-constexpr",
229	                        "--expt-extended-lambda",
230	                        "--use_fast_math",
231	                        # "--ptxas-options=-v",
232	                        # "--ptxas-options=-O2",
233	                        # "-lineinfo",
234	                        # "-DFLASHATTENTION_DISABLE_BACKWARD",
235	                        "-DFLASHATTENTION_DISABLE_DROPOUT",
236	                        "-DFLASHATTENTION_DISABLE_ALIBI",
237	                        "-DFLASHATTENTION_DISABLE_SOFTCAP",
238	                        "-DFLASHATTENTION_DISABLE_UNEVEN_K",
239	                        "-DFLASHATTENTION_DISABLE_LOCAL",
240	                    ]
241	                    + cc_flag
242	                ),
243	            },
244	            include_dirs=[
245	                Path(this_dir) / "csrc" / "flash_attn",
246	                Path(this_dir) / "csrc" / "flash_attn" / "src", 
247	                Path(this_dir) / "csrc" / "cutlass" / "include",
248	                # Path(this_dir) / "3rd" / "cutlass" / "include",
249	            ],
250	        )
251	    )
252	
253	setup(
254	    name='infllm_v2',
255	    version='0.0.0',
256	    author_email="[REDACTED]",
257	    description="infllm_v2 cuda implementation with flash attention and cutlass",
258	    packages=find_packages(),
259	    ext_modules=ext_modules,
260	    cmdclass={"build_ext": NinjaBuildExtension} if ext_modules else {},
261	    python_requires=">=3.7",
262	    install_requires=[
263	        "torch",
264	        "packaging",
265	        "psutil",
266	    ],
267	) 
268
```

> AGENT

现在让我阅读 Flash Attention 的关键头文件，以理解 blockmask 和内核的实现。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	// Include these 2 headers instead of torch/extension.h since we don't need all of the torch headers.
6	#include <torch/python.h>
7	#include <torch/nn/functional.h>
8	#include <c10/cuda/CUDAGuard.h>
9	#include <c10/cuda/CUDAStream.h>
10	#include <ATen/cuda/CUDAGeneratorImpl.h>  // For at::Generator and at::PhiloxCudaState
11	#include "philox_unpack.cuh"  // For at::cuda::philox::unpack
12	
13	#include <cutlass/numeric_types.h>
14	
15	#include "hardware_info.h"
16	#include "flash.h"
17	#include "static_switch.h"
18	
19	#define CHECK_DEVICE(x) TORCH_CHECK(x.is_cuda(), #x " must be on CUDA")
20	#define CHECK_SHAPE(x, ...) TORCH_CHECK(x.sizes() == torch::IntArrayRef({__VA_ARGS__}), #x " must have shape (" #__VA_ARGS__ ")")
21	#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
22	
23	
24	void set_params_fprop(Flash_fwd_params &params,
25	                      // sizes
26	                      const size_t b,
27	                      const size_t seqlen_q,
28	                      const size_t seqlen_k,
29	                      const size_t seqlen_q_rounded,
30	                      const size_t seqlen_k_rounded,
31	                      const size_t h,
32	                      const size_t h_k,
33	                      const size_t d,
34	                      const size_t d_rounded,
35	                      // device pointers
36	                      const at::Tensor q,
37	                      const at::Tensor k,
38	                      const at::Tensor v,
39	                      at::Tensor out,
40	                      void *cu_seqlens_q_d,
41	                      void *cu_seqlens_k_d,
42	                      void *seqused_k,
43	                      void *p_d,
44	                      void *softmax_lse_d,
45	                      float p_dropout,
46	                      float softmax_scale,
47	                      int window_size_left,
48	                      int window_size_right,
49	                      const float softcap,
50	                      bool seqlenq_ngroups_swapped=false,
51	                      const bool unpadded_lse=false) {
52	
53	    // Reset the parameters
54	    params = {};
55	
56	    params.is_bf16 = q.dtype() == torch::kBFloat16;
57	
58	    // Set the pointers and strides.
59	    params.q_ptr = q.data_ptr();
60	    params.k_ptr = k.data_ptr();
61	    params.v_ptr = v.data_ptr();
62	    // All stride are in elements, not bytes.
63	    params.q_row_stride = q.stride(-3);
64	    params.k_row_stride = k.stride(-3);
65	    params.v_row_stride = v.stride(-3);
66	    params.q_head_stride = q.stride(-2);
67	    params.k_head_stride = k.stride(-2);
68	    params.v_head_stride = v.stride(-2);
69	    params.o_ptr = out.data_ptr();
70	    params.o_row_stride = params.o_ptr ? out.stride(-3) : 0;
71	    params.o_head_stride = params.o_ptr ? out.stride(-2) : 0;
72	
73	    if (cu_seqlens_q_d == nullptr) {
74	        params.q_batch_stride = q.stride(0);
75	        params.k_batch_stride = k.stride(0);
76	        params.v_batch_stride = v.stride(0);
77	        params.o_batch_stride = params.o_ptr ? out.stride(0) : 0;
78	        if (seqlenq_ngroups_swapped) {
79	             params.q_batch_stride *= seqlen_q;
80	             params.o_batch_stride *= seqlen_q;
81	        }
82	    }
83	
84	    params.cu_seqlens_q = static_cast<int *>(cu_seqlens_q_d);
85	    params.cu_seqlens_k = static_cast<int *>(cu_seqlens_k_d);
86	    params.seqused_k = static_cast<int *>(seqused_k);
87	
88	    // P = softmax(QK^T)
89	    params.p_ptr = p_d;
90	
91	    // Softmax sum
92	    params.softmax_lse_ptr = softmax_lse_d;
93	
94	    // Set the dimensions.
95	    params.b = b;
96	    params.h = h;
97	    params.h_k = h_k;
98	    params.h_h_k_ratio = h / h_k;
99	    params.seqlen_q = seqlen_q;
100	    params.seqlen_k = seqlen_k;
101	    params.seqlen_q_rounded = seqlen_q_rounded;
102	    params.seqlen_k_rounded = seqlen_k_rounded;
103	    params.d = d;
104	    params.d_rounded = d_rounded;
105	
106	    // Set the different scale values.
107	    #ifdef FLASHATTENTION_DISABLE_SOFTCAP
108	        TORCH_CHECK(softcap <= 0.0, "This flash attention build does not support softcap.");
109	    #endif
110	    if (softcap > 0.0) {
111	        params.softcap = softmax_scale / softcap;
112	        params.scale_softmax = softcap;
113	        params.scale_softmax_log2 = softcap * M_LOG2E;
114	    } else{
115	        // Remove potential NaN
116	        params.softcap = 0.0;
117	        params.scale_softmax = softmax_scale;
118	        params.scale_softmax_log2 = softmax_scale * M_LOG2E;
119	    }
120	
121	    // Set this to probability of keeping an element to simplify things.
122	    params.p_dropout = 1.f - p_dropout;
123	    // Convert p from float to int so we don't have to convert the random uint to float to compare.
124	    // [Minor] We want to round down since when we do the comparison we use <= instead of <
125	    // params.p_dropout_in_uint = uint32_t(std::floor(params.p_dropout * 4294967295.0));
126	    // params.p_dropout_in_uint16_t = uint16_t(std::floor(params.p_dropout * 65535.0));
127	    params.p_dropout_in_uint8_t = uint8_t(std::floor(params.p_dropout * 255.0));
128	    params.rp_dropout = 1.f / params.p_dropout;
129	    params.scale_softmax_rp_dropout = params.rp_dropout * params.scale_softmax;
130	    TORCH_CHECK(p_dropout < 1.f);
131	    #ifdef FLASHATTENTION_DISABLE_DROPOUT
132	        TORCH_CHECK(p_dropout == 0.0f, "This flash attention build does not support dropout.");
133	    #endif
134	
135	    // Causal is the special case where window_size_right == 0 and window_size_left < 0.
136	    // Local is the more general case where window_size_right >= 0 or window_size_left >= 0.
137	    params.is_causal = window_size_left < 0 && window_size_right == 0;
138	
139	    if (window_size_left < 0 && window_size_right >= 0) { window_size_left = seqlen_k; }
140	    if (window_size_left >= 0 && window_size_right < 0) { window_size_right = seqlen_k; }
141	    params.window_size_left = window_size_left;
142	    params.window_size_right = window_size_right;
143	
144	    #ifdef FLASHATTENTION_DISABLE_LOCAL
145	        TORCH_CHECK(params.is_causal || (window_size_left < 0 && window_size_right < 0),
146	            "This flash attention build does not support local attention.");
147	    #endif
148	
149	    params.is_seqlens_k_cumulative = true;
150	
151	    #ifdef FLASHATTENTION_DISABLE_UNEVEN_K
152	        TORCH_CHECK(d == d_rounded, "This flash attention build does not support headdim not being a multiple of 32.");
153	    #endif
154	
155	    params.unpadded_lse = unpadded_lse;
156	    params.seqlenq_ngroups_swapped = seqlenq_ngroups_swapped;
157	}
158	
159	void set_params_dgrad(Flash_bwd_params &params,
160	                      // sizes
161	                      const size_t b,
162	                      const size_t seqlen_q,
163	                      const size_t seqlen_k,
164	                      const size_t seqlen_q_rounded,
165	                      const size_t seqlen_k_rounded,
166	                      const size_t h,
167	                      const size_t h_k,
168	                      const size_t d,
169	                      const size_t d_rounded,
170	                      // device pointers
171	                      const at::Tensor q,
172	                      const at::Tensor k,
173	                      const at::Tensor v,
174	                      const at::Tensor out,
175	                      const at::Tensor dout,
176	                      at::Tensor dq,
177	                      at::Tensor dk,
178	                      at::Tensor dv,
179	                      void *cu_seqlens_q_d,
180	                      void *cu_seqlens_k_d,
181	                      void *dq_accum_d,
182	                      void *dk_accum_d,
183	                      void *dv_accum_d,
184	                      void *softmax_lse_d,
185	                      void *dsoftmax_sum_d,
186	                      float p_dropout,
187	                      float softmax_scale,
188	                      int window_size_left,
189	                      int window_size_right,
190	                      const float softcap,
191	                      bool deterministic,
192	                      const bool unpadded_lse) {
193	
194	    set_params_fprop(params,
195	                     b, seqlen_q, seqlen_k, seqlen_q_rounded, seqlen_k_rounded, h, h_k, d, d_rounded,
196	                     q, k, v, out,
197	                     cu_seqlens_q_d,
198	                     cu_seqlens_k_d,
199	                     nullptr,
200	                     nullptr,
201	                     softmax_lse_d,
202	                     p_dropout,
203	                     softmax_scale,
204	                     window_size_left,
205	                     window_size_right,
206	                     softcap,
207	                     false, // seqlenq_ngroups_swapped
208	                     unpadded_lse);
209	
210	    // Set the pointers and strides.
211	    params.do_ptr = dout.data_ptr();
212	    params.do_row_stride = dout.stride(-3);
213	    params.do_head_stride = dout.stride(-2);
214	    params.dq_ptr = dq.data_ptr();
215	    params.dk_ptr = dk.data_ptr();
216	    params.dv_ptr = dv.data_ptr();
217	    params.dq_row_stride = dq.stride(-3);
218	    params.dk_row_stride = dk.stride(-3);
219	    params.dv_row_stride = dv.stride(-3);
220	    params.dq_head_stride = dq.stride(-2);
221	    params.dk_head_stride = dk.stride(-2);
222	    params.dv_head_stride = dv.stride(-2);
223	
224	    if (cu_seqlens_q_d == nullptr) {
225	        params.do_batch_stride = dout.stride(0);
226	        params.dq_batch_stride = dq.stride(0);
227	        params.dk_batch_stride = dk.stride(0);
228	        params.dv_batch_stride = dv.stride(0);
229	    }
230	
231	    params.dq_accum_ptr = dq_accum_d;
232	    params.dk_accum_ptr = dk_accum_d;
233	    params.dv_accum_ptr = dv_accum_d;
234	
235	    // Softmax sum
236	    params.dsoftmax_sum = dsoftmax_sum_d;
237	
238	    params.deterministic = deterministic;
239	}
240	
241	void run_mha_fwd(Flash_fwd_params &params, cudaStream_t stream, bool force_split_kernel=false) {
242	    FP16_SWITCH(!params.is_bf16, [&] {
243	        HEADDIM_SWITCH(params.d, [&] {
244	            BOOL_SWITCH(params.is_causal, Is_causal, [&] {
245	                if (params.num_splits <= 1 && !force_split_kernel) {  // If we don't set it num_splits == 0
246	                    run_mha_fwd_<elem_type, kHeadDim, Is_causal>(params, stream);
247	                } else {
248	                    run_mha_fwd_splitkv_dispatch<elem_type, kHeadDim, Is_causal>(params, stream);
249	                }
250	            });
251	        });
252	    });
253	}
254	
255	// Find the number of splits that maximizes the occupancy. For example, if we have
256	// batch * n_heads = 48 and we have 108 SMs, having 2 splits (efficiency = 0.89) is
257	// better than having 3 splits (efficiency = 0.67). However, we also don't want too many
258	// splits as that would incur more HBM reads/writes.
259	// So we find the best efficiency, then find the smallest number of splits that gets 85%
260	// of the best efficiency.
261	inline int num_splits_heuristic(int batch_nheads_mblocks, int num_SMs, int num_n_blocks, int max_splits) {
262	    // If we have enough to almost fill the SMs, then just use 1 split
263	    if (batch_nheads_mblocks >= 0.8f * num_SMs) { return 1; }
264	    max_splits = std::min({max_splits, num_SMs, num_n_blocks});
265	    float max_efficiency = 0.f;
266	    std::vector<float> efficiency;
267	    efficiency.reserve(max_splits);
268	    auto ceildiv = [](int a, int b) { return (a + b - 1) / b; };
269	    // Some splits are not eligible. For example, if we have 64 blocks and choose 11 splits,
270	    // we'll have 6 * 10 + 4 blocks. If we choose 12 splits, we'll have 6 * 11 + (-2) blocks
271	    // (i.e. it's 11 splits anyway).
272	    // So we check if the number of blocks per split is the same as the previous num_splits.
273	    auto is_split_eligible = [&ceildiv, &num_n_blocks](int num_splits) {
274	        return num_splits == 1 || ceildiv(num_n_blocks, num_splits) != ceildiv(num_n_blocks, num_splits - 1);
275	    };
276	    for (int num_splits = 1; num_splits <= max_splits; num_splits++) {
277	        if (!is_split_eligible(num_splits)) {
278	            efficiency.push_back(0.f);
279	        } else {
280	            float n_waves = float(batch_nheads_mblocks * num_splits) / num_SMs;
281	            float eff = n_waves / ceil(n_waves);
282	            // printf("num_splits = %d, eff = %f\n", num_splits, eff);
283	            if (eff > max_efficiency) { max_efficiency = eff; }
284	            efficiency.push_back(eff);
285	        }
286	    }
287	    for (int num_splits = 1; num_splits <= max_splits; num_splits++) {
288	        if (!is_split_eligible(num_splits)) { continue; }
289	        if (efficiency[num_splits - 1] >= 0.85 * max_efficiency) {
290	            // printf("num_splits chosen = %d\n", num_splits);
291	            return num_splits;
292	        }
293	    }
294	    return 1;
295	}
296	
297	std::tuple<at::Tensor, at::Tensor> set_params_splitkv(Flash_fwd_params &params, const int batch_size,
298	    const int num_heads, const int head_size, const int max_seqlen_k, const int max_seqlen_q,
299	    const int head_size_rounded, const float p_dropout,
300	    const int num_splits, const int num_sm, struct c10::TensorOptions opts) {
301	
302	    // This needs to match with run_mha_fwd_splitkv_dispatch
303	    const int block_n = head_size <= 64 ? 256 : (head_size <= 128 ? 128 : 64);
304	    const int num_n_blocks = (max_seqlen_k + block_n - 1) / block_n;
305	    // Technically kBlockM = 64 only for the splitKV kernels, not the standard kernel.
306	    // In any case we don't expect seqlen_q to be larger than 64 for inference.
307	    const int num_m_blocks = (max_seqlen_q + 64 - 1) / 64;
308	    params.num_splits = num_splits;
309	    at::Tensor softmax_lse_accum;
310	    at::Tensor out_accum;
311	
312	    if (p_dropout == 0.0f) {  // SplitKV is not implemented for dropout
313	        if (num_splits < 1) {
314	            // We multiply number of SMs by 2 to hard-code the fact that we're using 128 threads per block.
315	            params.num_splits = num_splits_heuristic(batch_size * num_heads * num_m_blocks, num_sm * 2, num_n_blocks, 128);
316	        }
317	        if (params.num_splits > 1) {
318	            softmax_lse_accum = torch::empty({params.num_splits, batch_size, num_heads, max_seqlen_q}, opts.dtype(at::kFloat));
319	            out_accum = torch::empty({params.num_splits, batch_size, num_heads, max_seqlen_q, head_size_rounded}, opts.dtype(at::kFloat));
320	            params.softmax_lseaccum_ptr = softmax_lse_accum.data_ptr();
321	            params.oaccum_ptr = out_accum.data_ptr();
322	        }
323	        TORCH_CHECK(params.num_splits <= 128, "num_splits > 128 not supported");
324	    }
325	
326	    return std::make_tuple(softmax_lse_accum, out_accum);
327	}
328	
329	void set_params_alibi(Flash_fwd_params &params, c10::optional<at::Tensor> &alibi_slopes_, int batch_size, int num_heads){
330	#ifdef FLASHATTENTION_DISABLE_ALIBI
331	    TORCH_CHECK(!alibi_slopes_.has_value(), "This flash attention build does not support alibi.");
332	    params.alibi_slopes_ptr = nullptr;
333	#else
334	    if (alibi_slopes_.has_value()) {
335	        auto alibi_slopes = alibi_slopes_.value();
336	        TORCH_CHECK(alibi_slopes.dtype() == torch::kFloat32, "ALiBi slopes must have dtype fp32");
337	        CHECK_DEVICE(alibi_slopes);
338	        TORCH_CHECK(alibi_slopes.stride(-1) == 1, "ALiBi slopes tensor must have contiguous last dimension");
339	        TORCH_CHECK(alibi_slopes.sizes() == torch::IntArrayRef({num_heads}) || alibi_slopes.sizes() == torch::IntArrayRef({batch_size, num_heads}));
340	        params.alibi_slopes_ptr = alibi_slopes.data_ptr();
341	        params.alibi_slopes_batch_stride = alibi_slopes.dim() == 2 ? alibi_slopes.stride(0) : 0;
342	    } else {
343	        params.alibi_slopes_ptr = nullptr;
344	    }
345	#endif
346	}
347	
348	std::vector<at::Tensor>
349	mha_fwd(at::Tensor &q,         // batch_size x seqlen_q x num_heads x round_multiple(head_size, 8)
350	        const at::Tensor &k,         // batch_size x seqlen_k x num_heads_k x round_multiple(head_size, 8)
351	        const at::Tensor &v,         // batch_size x seqlen_k x num_heads_k x round_multiple(head_size, 8)
352	        c10::optional<at::Tensor> &out_,             // batch_size x seqlen_q x num_heads x round_multiple(head_size, 8)
353	        c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
354	        const float p_dropout,
355	        const float softmax_scale,
356	        bool is_causal,
357	        int window_size_left,
358	        int window_size_right,
359	        const float softcap,
360	        const bool return_softmax,
361	        c10::optional<at::Generator> gen_) {
362	
363	    // Otherwise the kernel will be launched from cuda:0 device
364	    at::cuda::CUDAGuard device_guard{q.device()};
365	
366	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
367	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
368	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
369	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
370	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
371	    // We will support Turing in the near future
372	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
373	
374	    auto q_dtype = q.dtype();
375	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
376	                "FlashAttention only support fp16 and bf16 data type");
377	    if (q_dtype == torch::kBFloat16) {
378	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
379	    }
380	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
381	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
382	
383	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
384	
385	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
386	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
387	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
388	
389	    const auto sizes = q.sizes();
390	
391	    const int batch_size = sizes[0];
392	    int seqlen_q = sizes[1];
393	    int num_heads = sizes[2];
394	    const int head_size = sizes[3];
395	    const int seqlen_k = k.size(1);
396	    const int num_heads_k = k.size(2);
397	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
398	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
399	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
400	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
401	
402	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
403	
404	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
405	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
406	
407	    // causal=true is the same as causal=false in this case
408	    if (seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }
409	    if (is_causal) { window_size_right = 0; }
410	
411	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
412	    // H/t Daniel Haziza
413	    const int seqlenq_ngroups_swapped = seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
414	    const int ngroups = num_heads / num_heads_k;
415	    if (seqlenq_ngroups_swapped) {
416	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2);
417	        seqlen_q = ngroups;
418	        num_heads = num_heads_k;
419	    }
420	
421	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size);
422	    CHECK_SHAPE(k, batch_size, seqlen_k, num_heads_k, head_size);
423	    CHECK_SHAPE(v, batch_size, seqlen_k, num_heads_k, head_size);
424	
425	    at::Tensor out;
426	    if (out_.has_value()) {
427	        out = out_.value();
428	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
429	        CHECK_DEVICE(out);
430	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
431	        CHECK_SHAPE(out, batch_size, sizes[1], sizes[2], head_size);
432	        if (seqlenq_ngroups_swapped) {
433	            out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2);
434	        }
435	    } else {
436	        out = torch::empty_like(q);
437	    }
438	
439	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
440	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
441	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
442	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
443	
444	    auto opts = q.options();
445	
446	    auto softmax_lse = torch::empty({batch_size, num_heads, seqlen_q}, opts.dtype(at::kFloat));
447	    at::Tensor p;
448	    // Only return softmax if there's dropout to reduce compilation time
449	    if (return_softmax) {
450	        TORCH_CHECK(p_dropout > 0.0f, "return_softmax is only supported when p_dropout > 0.0");
451	        p = torch::empty({ batch_size, num_heads, seqlen_q_rounded, seqlen_k_rounded }, opts);
452	    }
453	    else {
454	        p = torch::empty({ 0 }, opts);
455	    }
456	
457	    Flash_fwd_params params;
458	    set_params_fprop(params,
459	                     batch_size,
460	                     seqlen_q, seqlen_k,
461	                     seqlen_q_rounded, seqlen_k_rounded,
462	                     num_heads, num_heads_k,
463	                     head_size, head_size_rounded,
464	                     q, k, v, out,
465	                     /*cu_seqlens_q_d=*/nullptr,
466	                     /*cu_seqlens_k_d=*/nullptr,
467	                     /*seqused_k=*/nullptr,
468	                     return_softmax ? p.data_ptr() : nullptr,
469	                     softmax_lse.data_ptr(),
470	                     p_dropout,
471	                     softmax_scale,
472	                     window_size_left,
473	                     window_size_right,
474	                     softcap
475	                     );
476	
477	    // Keep references to these tensors to extend their lifetime
478	    at::Tensor softmax_lse_accum, out_accum;
479	    std::tie(softmax_lse_accum, out_accum) = set_params_splitkv(
480	        params, batch_size, num_heads, head_size, seqlen_k, seqlen_q,
481	        head_size_rounded, p_dropout, /*num_splits*/ 0, get_num_sm(get_current_device()), opts);
482	
483	    // number of times random will be generated per thread, to offset philox counter in thc random
484	    // state
485	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
486	    int64_t counter_offset = params.b * params.h * 32;
487	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
488	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
489	    // Forward kernel will populate memory with the seed and offset.
490	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
491	
492	    if (p_dropout > 0.0)  {
493	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
494	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
495	        // See Note [Acquire lock when using random generators]
496	        std::lock_guard<std::mutex> lock(gen->mutex_);
497	        params.philox_args = gen->philox_cuda_state(counter_offset);
498	    }
499	
500	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
501	
502	    if (seqlen_k > 0) {
503	        auto stream = at::cuda::getCurrentCUDAStream().stream();
504	        run_mha_fwd(params, stream);
505	    } else {
506	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
507	        out.zero_();
508	        softmax_lse.fill_(std::numeric_limits<float>::infinity());
509	    }
510	
511	    if (seqlenq_ngroups_swapped) {
512	        out = out.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size});
513	        q = q.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size});
514	        softmax_lse = softmax_lse.reshape({batch_size, num_heads_k * seqlen_q, 1});
515	    }
516	    return {out, softmax_lse, p, rng_state};
517	}
518	
519	std::vector<at::Tensor>
520	mha_varlen_fwd(at::Tensor &q,  // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
521	               const at::Tensor &k,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
522	               const at::Tensor &v,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
523	               c10::optional<at::Tensor> &out_, // total_q x num_heads x head_size, total_k := \sum_{i=0}^{b} s_i
524	               const at::Tensor &cu_seqlens_q,  // b+1
525	               const at::Tensor &cu_seqlens_k,  // b+1
526	               c10::optional<at::Tensor> &seqused_k, // b. If given, only this many elements of each batch element's keys are used.
527	               c10::optional<const at::Tensor> &leftpad_k_, // batch_size
528	               c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
529	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
530	               int max_seqlen_q,
531	               const int max_seqlen_k,
532	               const float p_dropout,
533	               const float softmax_scale,
534	               const bool zero_tensors,
535	               bool is_causal,
536	               int window_size_left,
537	               int window_size_right,
538	               const float softcap,
539	               const bool return_softmax,
540	               c10::optional<at::Generator> gen_,
541	               c10::optional<at::Tensor> &blockmask_) {
542	
543	    // Otherwise the kernel will be launched from cuda:0 device
544	    at::cuda::CUDAGuard device_guard{q.device()};
545	
546	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
547	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
548	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
549	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
550	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
551	    // We will support Turing in the near future
552	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
553	
554	    auto q_dtype = q.dtype();
555	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
556	                "FlashAttention only support fp16 and bf16 data type");
557	    if (q_dtype == torch::kBFloat16) {
558	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
559	    }
560	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
561	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
562	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
563	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
564	
565	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
566	    CHECK_DEVICE(cu_seqlens_q);
567	    CHECK_DEVICE(cu_seqlens_k);
568	
569	    at::Tensor block_table;
570	    const bool paged_KV = block_table_.has_value();
571	    if (paged_KV) {
572	        block_table = block_table_.value();
573	        CHECK_DEVICE(block_table);
574	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
575	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
576	    }
577	
578	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
579	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
580	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
581	    CHECK_CONTIGUOUS(cu_seqlens_q);
582	    CHECK_CONTIGUOUS(cu_seqlens_k);
583	
584	    const auto sizes = q.sizes();
585	
586	    const int batch_size = cu_seqlens_q.numel() - 1;
587	    int num_heads = sizes[1];
588	    const int head_size = sizes[2];
589	    const int num_heads_k = paged_KV ? k.size(2) : k.size(1);
590	
591	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
592	
593	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
594	    const int num_blocks = !paged_KV ? 0 : k.size(0);
595	    const int page_block_size = !paged_KV ? 1 : k.size(1);
596	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
597	
598	    if (max_seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }  // causal=true is the same as causal=false in this case
599	    if (is_causal) { window_size_right = 0; }
600	
601	    void *cu_seqlens_q_d = cu_seqlens_q.data_ptr();
602	
603	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
604	    // H/t Daniel Haziza
605	    const int seqlenq_ngroups_swapped = max_seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
606	    const int ngroups = num_heads / num_heads_k;
607	    if (seqlenq_ngroups_swapped) {
608	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
609	        max_seqlen_q = ngroups;
610	        num_heads = num_heads_k;
611	        cu_seqlens_q_d = nullptr;
612	    }
613	
614	    const int total_q = q.sizes()[0];
615	
616	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
617	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
618	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
619	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
620	
621	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
622	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
623	
624	    CHECK_SHAPE(q, total_q, num_heads, head_size);
625	    if (!paged_KV) {
626	        const int total_k = k.size(0);
627	        CHECK_SHAPE(k, total_k, num_heads_k, head_size);
628	        CHECK_SHAPE(v, total_k, num_heads_k, head_size);
629	    } else {
630	        CHECK_SHAPE(k, num_blocks, page_block_size, num_heads_k, head_size);
631	        CHECK_SHAPE(v, num_blocks, page_block_size, num_heads_k, head_size);
632	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
633	    }
634	
635	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
636	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
637	    if (seqused_k.has_value()){
638	        auto seqused_k_ = seqused_k.value();
639	        TORCH_CHECK(seqused_k_.dtype() == torch::kInt32, "seqused_k must have dtype int32");
640	        TORCH_CHECK(seqused_k_.is_cuda(), "seqused_k must be on CUDA device");
641	        TORCH_CHECK(seqused_k_.is_contiguous(), "seqused_k must be contiguous");
642	        CHECK_SHAPE(seqused_k_, batch_size);
643	    }
644	
645	    at::Tensor out;
646	    if (out_.has_value()) {
647	        out = out_.value();
648	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
649	        CHECK_DEVICE(out);
650	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
651	        CHECK_SHAPE(out, sizes[0], sizes[1], head_size);
652	        if (seqlenq_ngroups_swapped) {
653	            out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
654	        }
655	    } else {
656	        out = torch::empty_like(q);
657	    }
658	
659	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
660	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
661	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
662	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
663	
664	    auto opts = q.options();
665	    auto softmax_lse = torch::empty({num_heads, total_q}, opts.dtype(at::kFloat));
666	    at::Tensor p;
667	    // Only return softmax if there's dropout to reduce compilation time
668	    if (return_softmax) {
669	        TORCH_CHECK(p_dropout > 0.0f, "return_softmax is only supported when p_dropout > 0.0");
670	        p = torch::empty({ batch_size, num_heads, seqlen_q_rounded, seqlen_k_rounded }, opts);
671	    }
672	    else {
673	        p = torch::empty({ 0 }, opts);
674	    }
675	
676	    if (zero_tensors) {
677	        out.zero_();
678	        softmax_lse.fill_(-std::numeric_limits<float>::infinity());
679	        if (return_softmax) {p.zero_();}
680	    }
681	
682	    Flash_fwd_params params;
683	    set_params_fprop(params,
684	                     batch_size,
685	                     max_seqlen_q, max_seqlen_k,
686	                     seqlen_q_rounded, seqlen_k_rounded,
687	                     num_heads, num_heads_k,
688	                     head_size, head_size_rounded,
689	                     q, k, v, out,
690	                     cu_seqlens_q_d,
691	                     cu_seqlens_k.data_ptr(),
692	                     seqused_k.has_value() ? seqused_k.value().data_ptr() : nullptr,
693	                     return_softmax ? p.data_ptr() : nullptr,
694	                     softmax_lse.data_ptr(),
695	                     p_dropout,
696	                     softmax_scale,
697	                     window_size_left,
698	                     window_size_right,
699	                     softcap,
700	                     seqlenq_ngroups_swapped,
701	                     /*unpadded_lse*/true);
702	    params.total_q = total_q;
703	
704	    if (blockmask_.has_value()) {
705	        params.blockmask = static_cast<uint64_t*>(blockmask_.value().data_ptr());
706	        params.m_block_dim = 16;
707	        params.n_block_dim = 64;
708	        params.num_k_heads = 2;
709	        params.num_blocks_m = (total_q + 16 - 1) / 16;
710	        params.num_blocks_n = (max_seqlen_k + 64 - 1) / 64;
711	    } else {
712	        params.blockmask = nullptr;
713	        params.m_block_dim = 1;
714	        params.n_block_dim = 1;
715	    }
716	
717	    if (paged_KV) {
718	        params.block_table = block_table.data_ptr<int>();
719	        params.block_table_batch_stride = block_table.stride(0);
720	        params.k_batch_stride = k.stride(0);
721	        params.v_batch_stride = v.stride(0);
722	    }
723	    params.page_block_size = page_block_size;
724	    // Keep references to these tensors to extend their lifetime
725	    at::Tensor softmax_lse_accum, out_accum;
726	    if (seqlenq_ngroups_swapped) {
727	        // Only apply split-k for decoding
728	        std::tie(softmax_lse_accum, out_accum) =
729	            set_params_splitkv(params, batch_size, num_heads, head_size,
730	                               max_seqlen_k, max_seqlen_q, head_size_rounded,
731	                               p_dropout, /*num_splits*/ 0, get_num_sm(get_current_device()), opts);
732	    }
733	
734	    if (leftpad_k_.has_value()) {
735	        auto leftpad_k = leftpad_k_.value();
736	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
737	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
738	        CHECK_DEVICE(leftpad_k);
739	        CHECK_CONTIGUOUS(leftpad_k);
740	        CHECK_SHAPE(leftpad_k, batch_size);
741	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
742	    }
743	
744	    // number of times random will be generated per thread, to offset philox counter in thc random
745	    // state
746	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
747	    int64_t counter_offset = params.b * params.h * 32;
748	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
749	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
750	    // Forward kernel will populate memory with the seed and offset.
751	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
752	
753	    if (p_dropout > 0.0)  {
754	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
755	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
756	        // See Note [Acquire lock when using random generators]
757	        std::lock_guard<std::mutex> lock(gen->mutex_);
758	        params.philox_args = gen->philox_cuda_state(counter_offset);
759	    }
760	
761	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
762	
763	    if (max_seqlen_k > 0) {
764	        auto stream = at::cuda::getCurrentCUDAStream().stream();
765	        params.num_splits = 1;
766	        run_mha_fwd(params, stream, paged_KV);
767	    } else {
768	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
769	        out.zero_();
770	        softmax_lse.fill_(std::numeric_limits<float>::infinity());
771	    }
772	
773	    if (seqlenq_ngroups_swapped) {
774	        int64_t size_before[] = {batch_size, max_seqlen_q, num_heads_k, head_size};
775	        int64_t size_after[] = {batch_size, num_heads_k * max_seqlen_q, head_size};
776	        out = out.reshape(size_before).transpose(1, 2).reshape(size_after);
777	        q = q.reshape(size_before).transpose(1, 2).reshape(size_after);
778	        softmax_lse = softmax_lse.reshape({num_heads * max_seqlen_q, batch_size});
779	    }
780	
781	    return {out, softmax_lse, p, rng_state};
782	}
783	
784	std::vector<at::Tensor>
785	mha_varlen_fwd_stage1(at::Tensor &q,  // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
786	               const at::Tensor &k,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
787	               const at::Tensor &v,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
788	               c10::optional<at::Tensor> &out_, // total_q x num_heads x head_size, total_k := \sum_{i=0}^{b} s_i
789	               const at::Tensor &cu_seqlens_q,  // b+1
790	               const at::Tensor &cu_seqlens_k,  // b+1
791	               const at::Tensor &cu_seqlens_v,  // b+1
792	               c10::optional<at::Tensor> &seqused_k, // b. If given, only this many elements of each batch element's keys are used.
793	               c10::optional<const at::Tensor> &leftpad_k_, // batch_size
794	               c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
795	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
796	               int max_seqlen_q,
797	               const int max_seqlen_k,
798	               const float p_dropout,
799	               const float softmax_scale,
800	               const bool zero_tensors,
801	               bool is_causal,
802	               int window_size_left,
803	               int window_size_right,
804	               const float softcap,
805	               const bool return_softmax,
806	               c10::optional<at::Generator> gen_) {
807	
808	    // Otherwise the kernel will be launched from cuda:0 device
809	    at::cuda::CUDAGuard device_guard{q.device()};
810	
811	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
812	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
813	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
814	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
815	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
816	    // We will support Turing in the near future
817	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
818	
819	    auto q_dtype = q.dtype();
820	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
821	                "FlashAttention only support fp16 and bf16 data type");
822	    if (q_dtype == torch::kBFloat16) {
823	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
824	    }
825	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
826	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
827	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
828	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
829	    TORCH_CHECK(cu_seqlens_v.dtype() == torch::kInt32, "cu_seqlens_v must have dtype int32");
830	
831	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
832	    CHECK_DEVICE(cu_seqlens_q);
833	    CHECK_DEVICE(cu_seqlens_k);
834	    CHECK_DEVICE(cu_seqlens_v);
835	
836	    at::Tensor block_table;
837	    const bool paged_KV = block_table_.has_value();
838	    if (paged_KV) {
839	        block_table = block_table_.value();
840	        CHECK_DEVICE(block_table);
841	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
842	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
843	    }
844	
845	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
846	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
847	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
848	    CHECK_CONTIGUOUS(cu_seqlens_q);
849	    CHECK_CONTIGUOUS(cu_seqlens_k);
850	    CHECK_CONTIGUOUS(cu_seqlens_v);
851	
852	    const auto sizes = q.sizes();
853	
854	    const int batch_size = cu_seqlens_q.numel() - 1;
855	    int num_heads = sizes[1];
856	    const int head_size = sizes[2];
857	    const int num_heads_k = paged_KV ? k.size(2) : k.size(1);
858	
859	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
860	
861	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
862	    const int num_blocks = !paged_KV ? 0 : k.size(0);
863	    const int page_block_size = !paged_KV ? 1 : k.size(1);
864	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
865	
866	    if (max_seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }  // causal=true is the same as causal=false in this case
867	    if (is_causal) { window_size_right = 0; }
868	
869	    void *cu_seqlens_q_d = cu_seqlens_q.data_ptr();
870	
871	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
872	    // H/t Daniel Haziza
873	    const int seqlenq_ngroups_swapped = max_seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
874	    const int ngroups = num_heads / num_heads_k;
875	    if (seqlenq_ngroups_swapped) {
876	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
877	        max_seqlen_q = ngroups;
878	        num_heads = num_heads_k;
879	        cu_seqlens_q_d = nullptr;
880	    }
881	
882	    const int total_q = q.sizes()[0];
883	
884	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
885	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
886	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
887	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
888	
889	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
890	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
891	
892	    CHECK_SHAPE(q, total_q, num_heads, head_size);
893	    if (!paged_KV) {
894	        const int total_k = k.size(0);
895	        CHECK_SHAPE(k, total_k, num_heads_k, head_size);
896	        // CHECK_SHAPE(v, total_k, num_heads_k, head_size);
897	    } else {
898	        CHECK_SHAPE(k, num_blocks, page_block_size, num_heads_k, head_size);
899	        // CHECK_SHAPE(v, num_blocks, page_block_size, num_heads_k, head_size);
900	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
901	    }
902	
903	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
904	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
905	    CHECK_SHAPE(cu_seqlens_v, batch_size + 1);
906	    if (seqused_k.has_value()){
907	        auto seqused_k_ = seqused_k.value();
908	        TORCH_CHECK(seqused_k_.dtype() == torch::kInt32, "seqused_k must have dtype int32");
909	        TORCH_CHECK(seqused_k_.is_cuda(), "seqused_k must be on CUDA device");
910	        TORCH_CHECK(seqused_k_.is_contiguous(), "seqused_k must be contiguous");
911	        CHECK_SHAPE(seqused_k_, batch_size);
912	    }
913	
914	
915	    auto opts = q.options();
916	    at::Tensor out;
917	    out = torch::empty({ 0 }, opts);
918	    // if (out_.has_value()) {
919	    //     out = out_.value();
920	    //     TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
921	    //     CHECK_DEVICE(out);
922	    //     TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
923	    //     CHECK_SHAPE(out, sizes[0], sizes[1], head_size);
924	    //     if (seqlenq_ngroups_swapped) {
925	    //         out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
926	    //     }
927	    // } else {
928	    //     out = torch::empty_like(q);
929	    // }
930	
931	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
932	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
933	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
934	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
935	
936	    // auto softmax_lse = torch::empty({num_heads, total_q}, opts.dtype(at::kFloat));
937	    at::Tensor p;
938	    // Only return softmax if there's dropout to reduce compilation time
939	    if (return_softmax) {
940	        // Return tensor with shape (num_heads_k, total_q, max_seqlen_k)
941	        p = torch::full({ num_heads_k, total_q / 16, seqlen_k_rounded }, 0, opts);
942	    }
943	    else {
944	        p = torch::empty({ 0 }, opts);
945	    }
946	
947	    if (zero_tensors) {
948	        // out.zero_();
949	        // softmax_lse.fill_(-std::numeric_limits<float>::infinity());
950	        if (return_softmax) {p.zero_();}
951	    }
952	
953	    Flash_fwd_params params;
954	    set_params_fprop(params,
955	                     batch_size,
956	                     max_seqlen_q, max_seqlen_k,
957	                     seqlen_q_rounded, seqlen_k_rounded,
958	                     num_heads, num_heads_k,
959	                     head_size, head_size_rounded,
960	                     q, k, v, out,
961	                     cu_seqlens_q_d,
962	                     cu_seqlens_k.data_ptr(),
963	                     seqused_k.has_value() ? seqused_k.value().data_ptr() : nullptr,
964	                     return_softmax ? p.data_ptr() : nullptr,
965	                     nullptr, //softmax_lse.data_ptr(),
966	                     p_dropout,
967	                     softmax_scale,
968	                     window_size_left,
969	                     window_size_right,
970	                     softcap,
971	                     seqlenq_ngroups_swapped,
972	                     /*unpadded_lse*/true);
973	
974	    params.cu_seqlens_v = static_cast<int *>(cu_seqlens_v.data_ptr());
975	    params.is_seqlens_v_cumulative = true;  // Treat cu_seqlens_v as cumulative sequence lengths
976	    // {
977	    //     // Copy cu_seqlens_v to CPU for printing
978	    //     at::Tensor cu_seqlens_v_cpu = cu_seqlens_v.to(torch::kCPU);
979	    //     const int* cu_seqlens_v_data = cu_seqlens_v_cpu.data_ptr<int>();
980	    //     printf("params.cu_seqlens_v: ");
981	    //     for (int i = 0; i < batch_size + 1; ++i) {
982	    //         printf("%d ", cu_seqlens_v_data[i]);
983	    //     }
984	    //     printf("\n");
985	    // }
986	    params.total_q = total_q;
987	
988	    params.m_block_dim = 16;
989	    params.n_block_dim = 1;
990	
991	    if (paged_KV) {
992	        params.block_table = block_table.data_ptr<int>();
993	        params.block_table_batch_stride = block_table.stride(0);
994	        params.k_batch_stride = k.stride(0);
995	        // params.v_batch_stride = v.stride(0);
996	    }
997	    params.page_block_size = page_block_size;
998	    // Keep references to these tensors to extend their lifetime
999	
1000	
1001	    if (leftpad_k_.has_value()) {
1002	        auto leftpad_k = leftpad_k_.value();
1003	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
1004	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
1005	        CHECK_DEVICE(leftpad_k);
1006	        CHECK_CONTIGUOUS(leftpad_k);
1007	        CHECK_SHAPE(leftpad_k, batch_size);
1008	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
1009	    }
1010	
1011	    // number of times random will be generated per thread, to offset philox counter in thc random
1012	    // state
1013	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1014	    int64_t counter_offset = params.b * params.h * 32;
1015	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
1016	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
1017	    // Forward kernel will populate memory with the seed and offset.
1018	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
1019	
1020	    if (p_dropout > 0.0)  {
1021	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1022	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
1023	        // See Note [Acquire lock when using random generators]
1024	        std::lock_guard<std::mutex> lock(gen->mutex_);
1025	        params.philox_args = gen->philox_cuda_state(counter_offset);
1026	    }
1027	
1028	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1029	
1030	    if (max_seqlen_k > 0) {
1031	        auto stream = at::cuda::getCurrentCUDAStream().stream();
1032	        params.num_splits = 1;
1033	        run_mha_fwd(params, stream, paged_KV || true);
1034	    } else {
1035	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
1036	        // out.zero_();
1037	        // softmax_lse.fill_(std::numeric_limits<float>::infinity());
1038	    }
1039	
1040	    if (seqlenq_ngroups_swapped) {
1041	        int64_t size_before[] = {batch_size, max_seqlen_q, num_heads_k, head_size};
1042	        int64_t size_after[] = {batch_size, num_heads_k * max_seqlen_q, head_size};
1043	        // out = out.reshape(size_before).transpose(1, 2).reshape(size_after);
1044	        q = q.reshape(size_before).transpose(1, 2).reshape(size_after);
1045	        // softmax_lse = softmax_lse.reshape({num_heads * max_seqlen_q, batch_size});
1046	    }
1047	
1048	    return {p};
1049	}
1050	
1051	void run_mha_bwd(Flash_bwd_params &params, cudaStream_t stream) {
1052	    FP16_SWITCH(!params.is_bf16, [&] {
1053	        HEADDIM_SWITCH(params.d, [&] {
1054	            BOOL_SWITCH(params.is_causal, Is_causal, [&] {
1055	                run_mha_bwd_<elem_type, kHeadDim, Is_causal>(params, stream);
1056	            });
1057	        });
1058	    });
1059	}
1060	
1061	std::vector<at::Tensor>
1062	mha_bwd(const at::Tensor &dout,  // batch_size x seqlen_q x num_heads, x multiple_of(head_size_og, 8)
1063	        const at::Tensor &q,   // batch_size x seqlen_q x num_heads x head_size
1064	        const at::Tensor &k,   // batch_size x seqlen_k x num_heads_k x head_size
1065	        const at::Tensor &v,   // batch_size x seqlen_k x num_heads_k x head_size
1066	        const at::Tensor &out,   // batch_size x seqlen_q x num_heads x head_size
1067	        const at::Tensor &softmax_lse,     // b x h x seqlen_q
1068	        c10::optional<at::Tensor> &dq_,   // batch_size x seqlen_q x num_heads x head_size
1069	        c10::optional<at::Tensor> &dk_,   // batch_size x seqlen_k x num_heads_k x head_size
1070	        c10::optional<at::Tensor> &dv_,   // batch_size x seqlen_k x num_heads_k x head_size
1071	        c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
1072	        const float p_dropout,         // probability to drop
1073	        const float softmax_scale,
1074	        const bool is_causal,
1075	        int window_size_left,
1076	        int window_size_right,
1077	        const float softcap,
1078	        const bool deterministic,
1079	        c10::optional<at::Generator> gen_,
1080	        c10::optional<at::Tensor> &rng_state) {
1081	
1082	    #ifdef FLASHATTENTION_DISABLE_BACKWARD
1083	        TORCH_CHECK(false, "This flash attention build does not support backward.");
1084	    #endif
1085	    if (is_causal) { window_size_right = 0; }
1086	
1087	    // Otherwise the kernel will be launched from cuda:0 device
1088	    at::cuda::CUDAGuard device_guard{q.device()};
1089	
1090	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1091	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1092	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1093	    bool is_sm80 = cc_major == 8 && cc_minor == 0;
1094	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1095	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1096	    // We will support Turing in the near future
1097	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1098	
1099	    bool is_dropout = p_dropout > 0.0;
1100	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1101	
1102	    auto q_dtype = q.dtype();
1103	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1104	                "FlashAttention only support fp16 and bf16 data type");
1105	    if (q_dtype == torch::kBFloat16) {
1106	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1107	    }
1108	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
1109	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
1110	    TORCH_CHECK(out.dtype() == q_dtype, "query and out must have the same dtype");
1111	    TORCH_CHECK(dout.dtype() == q_dtype, "query and dout must have the same dtype");
1112	
1113	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
1114	    CHECK_DEVICE(out); CHECK_DEVICE(dout); CHECK_DEVICE(softmax_lse);
1115	
1116	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1117	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1118	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1119	    TORCH_CHECK(out.stride(-1) == 1, "out tensor must have contiguous last dimension");
1120	    TORCH_CHECK(dout.stride(-1) == 1, "dout tensor must have contiguous last dimension");
1121	
1122	    const auto sizes = q.sizes();
1123	
1124	    const int batch_size = sizes[0];
1125	    const int seqlen_q = sizes[1];
1126	    const int num_heads = sizes[2];
1127	    const int head_size = sizes[3];
1128	    const int seqlen_k = k.size(1);
1129	    const int num_heads_k = k.size(2);
1130	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1131	    TORCH_CHECK(head_size % 8 == 0, "head_size should be a multiple of 8");
1132	    TORCH_CHECK(head_size <= 256, "FlashAttention backward only supports head dimension at most 256");
1133	    if (head_size > 192 && is_dropout) {
1134	        TORCH_CHECK(is_sm80 || is_sm90, "FlashAttention backward for head dim > 192 with dropout requires A100/A800 or H100/H800");
1135	    }
1136	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1137	
1138	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1139	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1140	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
1141	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
1142	
1143	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
1144	
1145	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
1146	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
1147	
1148	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size);
1149	    CHECK_SHAPE(k, batch_size, seqlen_k, num_heads_k, head_size);
1150	    CHECK_SHAPE(v, batch_size, seqlen_k, num_heads_k, head_size);
1151	    CHECK_SHAPE(out, batch_size, seqlen_q, num_heads, head_size);
1152	    CHECK_SHAPE(dout, batch_size, seqlen_q, num_heads, head_size);
1153	
1154	    at::Tensor dq, dk, dv;
1155	    if (dq_.has_value()) {
1156	        dq = dq_.value();
1157	        TORCH_CHECK(dq.dtype() == q_dtype, "dq must have the same dtype as q");
1158	        CHECK_DEVICE(dq);
1159	        TORCH_CHECK(dq.stride(-1) == 1, "dq must have contiguous last dimension");
1160	        CHECK_SHAPE(dq, batch_size, seqlen_q, num_heads, head_size);
1161	    } else {
1162	        dq = torch::empty_like(q);
1163	    }
1164	    if (dk_.has_value()) {
1165	        dk = dk_.value();
1166	        TORCH_CHECK(dk.dtype() == q_dtype, "dk must have the same dtype as q");
1167	        CHECK_DEVICE(dk);
1168	        TORCH_CHECK(dk.stride(-1) == 1, "dk must have contiguous last dimension");
1169	        CHECK_SHAPE(dk, batch_size, seqlen_k, num_heads_k, head_size);
1170	    } else {
1171	        dk = torch::empty_like(k);
1172	    }
1173	    if (dv_.has_value()) {
1174	        dv = dv_.value();
1175	        TORCH_CHECK(dv.dtype() == q_dtype, "dv must have the same dtype as q");
1176	        CHECK_DEVICE(dv);
1177	        TORCH_CHECK(dv.stride(-1) == 1, "dv must have contiguous last dimension");
1178	        CHECK_SHAPE(dv, batch_size, seqlen_k, num_heads_k, head_size);
1179	    } else {
1180	        dv = torch::empty_like(v);
1181	    }
1182	
1183	    // bool loop = seqlen_k > blocksize_c;
1184	    // TODO: change later, for now set to true for simplicity
1185	    bool loop = true;
1186	
1187	    auto opts = q.options();
1188	    auto softmax_d = torch::empty({batch_size, num_heads, seqlen_q_rounded}, opts.dtype(at::kFloat));
1189	    at::Tensor dq_accum;
1190	    at::Tensor dk_accum, dv_accum;
1191	    if (loop) {
1192	        if (!deterministic) {
1193	            dq_accum = torch::empty({batch_size, seqlen_q_rounded, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1194	        } else {
1195	            const int nsplits = (get_num_sm(get_current_device()) + batch_size * num_heads - 1) / (batch_size * num_heads);
1196	            dq_accum = torch::zeros({nsplits, batch_size, seqlen_q_rounded, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1197	        }
1198	        // dk_accum = torch::empty({batch_size, num_heads_k, seqlen_k_rounded, head_size_rounded}, opts.dtype(at::kFloat));
1199	        // dv_accum = torch::empty({batch_size, num_heads_k, seqlen_k_rounded, head_size_rounded}, opts.dtype(at::kFloat));
1200	    }
1201	
1202	    at::Tensor dk_expanded, dv_expanded;
1203	    if (num_heads_k != num_heads) {  // MQA / GQA
1204	        dk_expanded = torch::empty({batch_size, seqlen_k, num_heads, head_size}, opts);
1205	        dv_expanded = torch::empty({batch_size, seqlen_k, num_heads, head_size}, opts);
1206	    } else {
1207	        dk_expanded = dk;
1208	        dv_expanded = dv;
1209	    }
1210	
1211	    Flash_bwd_params params;
1212	
1213	    set_params_dgrad(params,
1214	                     batch_size,
1215	                     seqlen_q, seqlen_k,
1216	                     seqlen_q_rounded, seqlen_k_rounded,
1217	                     num_heads, num_heads_k,
1218	                     head_size, head_size_rounded,
1219	                     q, k, v, out,
1220	                     dout, dq, dk_expanded, dv_expanded,
1221	                     nullptr,
1222	                     nullptr,
1223	                     loop ? dq_accum.data_ptr() : nullptr,
1224	                     // loop ? dk_accum.data_ptr() : nullptr,
1225	                     // loop ? dv_accum.data_ptr() : nullptr,
1226	                     nullptr,
1227	                     nullptr,
1228	                     softmax_lse.data_ptr(),
1229	                     softmax_d.data_ptr(),
1230	                     p_dropout,
1231	                     softmax_scale,
1232	                     window_size_left,
1233	                     window_size_right,
1234	                     softcap,
1235	                     deterministic,
1236	                     /*unpadded_lse*/false);
1237	    params.dq_accum_split_stride = !deterministic ? 0 : dq_accum.stride(0);
1238	
1239	    auto launch = &run_mha_bwd;
1240	
1241	    auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1242	        gen_, at::cuda::detail::getDefaultCUDAGenerator());
1243	
1244	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1245	    int64_t counter_offset = params.b * params.h * 32;
1246	
1247	    if ( rng_state.has_value() ) {
1248	        params.rng_state = reinterpret_cast<uint64_t*>(rng_state.value().data_ptr());
1249	    } else if( is_dropout ) {
1250	        // See Note [Acquire lock when using random generators]
1251	        std::lock_guard<std::mutex> lock(gen->mutex_);
1252	        params.philox_args = gen->philox_cuda_state(counter_offset);
1253	        auto seeds = at::cuda::philox::unpack(params.philox_args);
1254	        params.rng_state[0] = std::get<0>(seeds);
1255	        params.rng_state[1] = std::get<1>(seeds);
1256	    }
1257	
1258	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1259	
1260	    if (seqlen_q > 0) {
1261	        launch(params, stream);
1262	    } else {
1263	        // If seqlen_q == 0, then we have an empty tensor. We need to set the output to 0.
1264	        dk_expanded.zero_();
1265	        dv_expanded.zero_();
1266	        softmax_d.zero_();
1267	    }
1268	
1269	    // For MQA/GQA we need to sum dK and dV across the groups
1270	    if (num_heads_k != num_heads) {
1271	        at::sum_out(dk, at::reshape(dk_expanded, {batch_size, seqlen_k, num_heads_k, num_heads / num_heads_k, head_size}), {3});
1272	        at::sum_out(dv, at::reshape(dv_expanded, {batch_size, seqlen_k, num_heads_k, num_heads / num_heads_k, head_size}), {3});
1273	    }
1274	
1275	    return { dq, dk, dv, softmax_d };
1276	}
1277	
1278	std::vector<at::Tensor>
1279	mha_varlen_bwd(const at::Tensor &dout,  // total_q x num_heads, x head_size
1280	               const at::Tensor &q,   // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
1281	               const at::Tensor &k,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1282	               const at::Tensor &v,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1283	               const at::Tensor &out,   // total_q x num_heads x head_size
1284	               const at::Tensor &softmax_lse,    // h x total_q, softmax logsumexp
1285	               c10::optional<at::Tensor> &dq_,   // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
1286	               c10::optional<at::Tensor> &dk_,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1287	               c10::optional<at::Tensor> &dv_,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1288	               const at::Tensor &cu_seqlens_q,  // b+1
1289	               const at::Tensor &cu_seqlens_k,  // b+1
1290	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
1291	               const int max_seqlen_q,
1292	               const int max_seqlen_k,          // max sequence length to choose the kernel
1293	               const float p_dropout,         // probability to drop
1294	               const float softmax_scale,
1295	               const bool zero_tensors,
1296	               const bool is_causal,
1297	               int window_size_left,
1298	               int window_size_right,
1299	               const float softcap,
1300	               const bool deterministic,
1301	               c10::optional<at::Tensor> &col_blockmask_, 
1302	               c10::optional<at::Generator> gen_,
1303	               c10::optional<at::Tensor> &rng_state) {
1304	
1305	    #ifdef FLASHATTENTION_DISABLE_BACKWARD
1306	        TORCH_CHECK(false, "This flash attention build does not support backward.");
1307	    #endif
1308	    if (is_causal) { window_size_right = 0; }
1309	
1310	    // Otherwise the kernel will be launched from cuda:0 device
1311	    at::cuda::CUDAGuard device_guard{q.device()};
1312	
1313	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1314	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1315	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1316	    bool is_sm80 = cc_major == 8 && cc_minor == 0;
1317	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1318	    const bool has_blockmask = col_blockmask_.has_value();
1319	    at::Tensor col_blockmask;
1320	    if (has_blockmask) {
1321	        col_blockmask = col_blockmask_.value();
1322	    }
1323	    if(has_blockmask){
1324	        TORCH_CHECK(col_blockmask.dtype() == torch::kInt64, "col_blockmask must have dtype int64");
1325	    }
1326	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1327	    // We will support Turing in the near future
1328	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1329	    bool is_dropout = p_dropout > 0.0;
1330	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1331	
1332	    auto q_dtype = q.dtype();
1333	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1334	                "FlashAttention only support fp16 and bf16 data type");
1335	    if (q_dtype == torch::kBFloat16) {
1336	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1337	    }
1338	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
1339	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
1340	    TORCH_CHECK(out.dtype() == q_dtype, "query and out must have the same dtype");
1341	    TORCH_CHECK(dout.dtype() == q_dtype, "query and dout must have the same dtype");
1342	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
1343	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
1344	
1345	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
1346	    CHECK_DEVICE(out); CHECK_DEVICE(dout); CHECK_DEVICE(softmax_lse);
1347	    CHECK_DEVICE(cu_seqlens_q); CHECK_DEVICE(cu_seqlens_k);
1348	    if(has_blockmask){
1349	        CHECK_DEVICE(col_blockmask);
1350	    }
1351	
1352	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1353	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1354	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1355	    TORCH_CHECK(out.stride(-1) == 1, "out tensor must have contiguous last dimension");
1356	    TORCH_CHECK(dout.stride(-1) == 1, "dout tensor must have contiguous last dimension");
1357	    CHECK_CONTIGUOUS(cu_seqlens_q);
1358	    CHECK_CONTIGUOUS(cu_seqlens_k);
1359	    
1360	
1361	    const auto sizes = q.sizes();
1362	
1363	    const int total_q = sizes[0];
1364	    const int batch_size = cu_seqlens_q.numel() - 1;
1365	    const int num_heads = sizes[1];
1366	    const int head_size = sizes[2];
1367	    const int total_k = k.size(0);
1368	    const int num_heads_k = k.size(1);
1369	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1370	    TORCH_CHECK(head_size % 8 == 0, "head_size should be a multiple of 8");
1371	    TORCH_CHECK(head_size <= 256, "FlashAttention backward only supports head dimension at most 256");
1372	    if (head_size > 192 && is_dropout) {
1373	        TORCH_CHECK(is_sm80 || is_sm90, "FlashAttention backward for head dim > 192 with dropout requires A100/A800 or H100/H800");
1374	    }
1375	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1376	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
1377	
1378	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1379	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1380	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
1381	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
1382	
1383	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
1384	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
1385	
1386	    CHECK_SHAPE(q, total_q, num_heads, head_size);
1387	    CHECK_SHAPE(k, total_k, num_heads_k, head_size);
1388	    CHECK_SHAPE(v, total_k, num_heads_k, head_size);
1389	    CHECK_SHAPE(out, total_q, num_heads, head_size);
1390	    CHECK_SHAPE(dout, total_q, num_heads, head_size);
1391	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
1392	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
1393	    if(has_blockmask){
1394	        CHECK_CONTIGUOUS(col_blockmask);
1395	        // Last dimension should now be the number of uint64s needed to represent the original blocks
1396	        int blocks_per_uint64 = 64;  // 64 bits per uint64
1397	        int m_blocks = total_q / 16;
1398	        int uint64_per_row = (m_blocks + blocks_per_uint64 - 1) / blocks_per_uint64;
1399	        CHECK_SHAPE(col_blockmask, num_heads_k, round_multiple(max_seqlen_k, 64) / 64, uint64_per_row);
1400	    }
1401	
1402	    at::Tensor dq, dk, dv;
1403	    if (dq_.has_value()) {
1404	        dq = dq_.value();
1405	        TORCH_CHECK(dq.dtype() == q_dtype, "dq must have the same dtype as q");
1406	        CHECK_DEVICE(dq);
1407	        TORCH_CHECK(dq.stride(-1) == 1, "dq must have contiguous last dimension");
1408	        CHECK_SHAPE(dq, total_q, num_heads, head_size);
1409	    } else {
1410	        dq = torch::empty_like(q);
1411	    }
1412	    if (dk_.has_value()) {
1413	        dk = dk_.value();
1414	        TORCH_CHECK(dk.dtype() == q_dtype, "dk must have the same dtype as q");
1415	        CHECK_DEVICE(dk);
1416	        TORCH_CHECK(dk.stride(-1) == 1, "dk must have contiguous last dimension");
1417	        CHECK_SHAPE(dk, total_k, num_heads_k, head_size);
1418	    } else {
1419	        dk = torch::empty_like(k);
1420	    }
1421	    if (dv_.has_value()) {
1422	        dv = dv_.value();
1423	        TORCH_CHECK(dv.dtype() == q_dtype, "dv must have the same dtype as q");
1424	        CHECK_DEVICE(dv);
1425	        TORCH_CHECK(dv.stride(-1) == 1, "dv must have contiguous last dimension");
1426	        CHECK_SHAPE(dv, total_k, num_heads_k, head_size);
1427	    } else {
1428	        dv = torch::empty_like(v);
1429	    }
1430	
1431	    // bool loop = max_seqlen_k > blocksize_c;
1432	    // TODO: change later, for now set to true for simplicity
1433	    bool loop = true;
1434	
1435	    auto opts = q.options();
1436	    auto softmax_d = torch::empty({num_heads, total_q + 128 * batch_size}, opts.dtype(at::kFloat));
1437	    at::Tensor dq_accum;
1438	    if (loop) {
1439	        // We don't want to allocate dq_accum of size (batch, seqlen_q_rounded, num_heads, head_size_rounded)
1440	        // because that would be too large if there is a very long sequence and the rest of the sequences are short.
1441	        // Instead, we allocate dq_accum of size (total_q + 128 * batch, num_heads, head_size_rounded).
1442	        // Note that 128 is the max block size on the seqlen_q dimension.
1443	        // For dQ, the i-th sequence is stored in indices from cu_seqlens[i] + 128 * i to
1444	        // cu_seqlens[i + 1] * 128 * i - 1. This ensures that the i-th sequence and (i + 1)-th sequence will
1445	        // be at least 128 apart. It's ok for us to do atomicAdds up to 128 rows beyond what we're normally
1446	        // allowed to do. So we won't have to do any bound checking, and performance should stay the same.
1447	        // Same holds for softmax_d, since LSE is stored in unpadded format.
1448	        if (!deterministic) {
1449	            dq_accum = torch::empty({total_q + 128 * batch_size, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1450	        } else {
1451	            const int nsplits = (get_num_sm(get_current_device()) + batch_size * num_heads - 1) / (batch_size * num_heads);
1452	            dq_accum = torch::zeros({nsplits, total_q + 128 * batch_size, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1453	        }
1454	    }
1455	
1456	    at::Tensor dk_expanded, dv_expanded;
1457	    if (num_heads_k != num_heads) {  // MQA / GQA
1458	        dk_expanded = torch::empty({total_k, num_heads, head_size}, opts);
1459	        dv_expanded = torch::empty({total_k, num_heads, head_size}, opts);
1460	    } else {
1461	        dk_expanded = dk;
1462	        dv_expanded = dv;
1463	    }
1464	
1465	    if( zero_tensors ) {
1466	        dq.zero_();
1467	        dk_expanded.zero_();
1468	        dv_expanded.zero_();
1469	        softmax_d.zero_();
1470	    }
1471	
1472	    Flash_bwd_params params;
1473	
1474	    set_params_dgrad(params,
1475	                     batch_size,
1476	                     max_seqlen_q, max_seqlen_k,
1477	                     seqlen_q_rounded, seqlen_k_rounded,
1478	                     num_heads, num_heads_k,
1479	                     head_size, head_size_rounded,
1480	                     q, k, v, out,
1481	                     dout, dq, dk_expanded, dv_expanded,
1482	                     cu_seqlens_q.data_ptr(),
1483	                     cu_seqlens_k.data_ptr(),
1484	                     loop ? dq_accum.data_ptr() : nullptr,
1485	                     nullptr,
1486	                     nullptr,
1487	                     softmax_lse.data_ptr(),
1488	                     softmax_d.data_ptr(),
1489	                     p_dropout,
1490	                     softmax_scale,
1491	                     window_size_left,
1492	                     window_size_right,
1493	                     softcap,
1494	                     deterministic,
1495	                     /*unpadded_lse*/true);
1496	    params.dq_accum_split_stride = !deterministic ? 0 : dq_accum.stride(0);
1497	    params.total_q = total_q;
1498	
1499	    if(has_blockmask){
1500	        params.blockmask = static_cast<uint64_t*>(col_blockmask.data_ptr());
1501	        params.m_block_dim = 16;
1502	        params.n_block_dim = 64;
1503	        params.num_blocks_m = total_q / 16;
1504	        params.num_blocks_n = round_multiple(max_seqlen_k, 64) / 64;
1505	        // params.block_window_size = block_window_size;
1506	    }
1507	    else {
1508	        params.blockmask = nullptr;
1509	    }
1510	    auto launch = &run_mha_bwd;
1511	
1512	    auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1513	        gen_, at::cuda::detail::getDefaultCUDAGenerator());
1514	
1515	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1516	    int64_t counter_offset = params.b * params.h * 32;
1517	
1518	    if ( rng_state.has_value() ) {
1519	        params.rng_state = reinterpret_cast<uint64_t*>(rng_state.value().data_ptr());
1520	    } else if( is_dropout ) {
1521	        // See Note [Acquire lock when using random generators]
1522	        std::lock_guard<std::mutex> lock(gen->mutex_);
1523	        params.philox_args = gen->philox_cuda_state(counter_offset);
1524	        auto seeds = at::cuda::philox::unpack(params.philox_args);
1525	        params.rng_state[0] = std::get<0>(seeds);
1526	        params.rng_state[1] = std::get<1>(seeds);
1527	    }
1528	
1529	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1530	
1531	    if (max_seqlen_q > 0) {
1532	        launch(params, stream);
1533	    } else {
1534	        // If seqlen_q == 0, then we have an empty tensor. We need to set the output to 0.
1535	        dk_expanded.zero_();
1536	        dv_expanded.zero_();
1537	        softmax_d.zero_();
1538	    }
1539	
1540	    // For MQA/GQA we need to sum dK and dV across the groups
1541	    if (num_heads_k != num_heads) {
1542	        at::sum_out(dk, at::reshape(dk_expanded, {total_k, num_heads_k, num_heads / num_heads_k, head_size}), {2});
1543	        at::sum_out(dv, at::reshape(dv_expanded, {total_k, num_heads_k, num_heads / num_heads_k, head_size}), {2});
1544	    }
1545	
1546	    return { dq, dk, dv, softmax_d };
1547	}
1548	
1549	std::vector<at::Tensor>
1550	mha_fwd_kvcache(at::Tensor &q,                 // batch_size x seqlen_q x num_heads x head_size
1551	                const at::Tensor &kcache,            // batch_size_c x seqlen_k x num_heads_k x head_size or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
1552	                const at::Tensor &vcache,            // batch_size_c x seqlen_k x num_heads_k x head_size or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
1553	                c10::optional<const at::Tensor> &k_, // batch_size x seqlen_knew x num_heads_k x head_size
1554	                c10::optional<const at::Tensor> &v_, // batch_size x seqlen_knew x num_heads_k x head_size
1555	                c10::optional<const at::Tensor> &seqlens_k_, // batch_size
1556	                c10::optional<const at::Tensor> &rotary_cos_, // seqlen_ro x (rotary_dim / 2)
1557	                c10::optional<const at::Tensor> &rotary_sin_, // seqlen_ro x (rotary_dim / 2)
1558	                c10::optional<const at::Tensor> &cache_batch_idx_, // indices to index into the KV cache
1559	                c10::optional<const at::Tensor> &leftpad_k_, // batch_size
1560	                c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
1561	                c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
1562	                c10::optional<at::Tensor> &out_,             // batch_size x seqlen_q x num_heads x head_size
1563	                const float softmax_scale,
1564	                bool is_causal,
1565	                int window_size_left,
1566	                int window_size_right,
1567	                const float softcap,
1568	                bool is_rotary_interleaved,   // if true, rotary combines indices 0 & 1, else indices 0 & rotary_dim / 2
1569	                int num_splits,
1570	                        c10::optional<at::Tensor> &blockmask_
1571	                ) {
1572	
1573	    // Otherwise the kernel will be launched from cuda:0 device
1574	    at::cuda::CUDAGuard device_guard{q.device()};
1575	
1576	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1577	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1578	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1579	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1580	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1581	    // We will support Turing in the near future
1582	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1583	
1584	    auto q_dtype = q.dtype();
1585	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1586	                "FlashAttention only support fp16 and bf16 data type");
1587	    if (q_dtype == torch::kBFloat16) {
1588	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1589	    }
1590	    TORCH_CHECK(kcache.dtype() == q_dtype, "query and key must have the same dtype");
1591	    TORCH_CHECK(vcache.dtype() == q_dtype, "query and value must have the same dtype");
1592	
1593	    CHECK_DEVICE(q); CHECK_DEVICE(kcache); CHECK_DEVICE(vcache);
1594	
1595	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1596	    TORCH_CHECK(kcache.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1597	    TORCH_CHECK(vcache.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1598	
1599	    at::Tensor block_table;
1600	    const bool paged_KV = block_table_.has_value();
1601	    if (paged_KV) {
1602	        TORCH_CHECK(!cache_batch_idx_.has_value(), "Paged KVcache does not support cache_batch_idx");
1603	        block_table = block_table_.value();
1604	        CHECK_DEVICE(block_table);
1605	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
1606	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
1607	    }
1608	
1609	    const auto sizes = q.sizes();
1610	
1611	    const int batch_size = sizes[0];
1612	    int seqlen_q = sizes[1];
1613	    int num_heads = sizes[2];
1614	    const int head_size_og = sizes[3];
1615	
1616	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
1617	    const int num_blocks = !paged_KV ? 0 : kcache.size(0);
1618	    const int page_block_size = !paged_KV ? 1 : kcache.size(1);
1619	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
1620	    const int seqlen_k = !paged_KV ? kcache.size(1) : max_num_blocks_per_seq * page_block_size;
1621	    const int num_heads_k = kcache.size(2);
1622	    const int batch_size_c = !paged_KV ? kcache.size(0) : batch_size;
1623	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1624	    TORCH_CHECK(head_size_og <= 256, "FlashAttention forward only supports head dimension at most 256");
1625	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1626	
1627	    // causal=true is the same as causal=false in this case
1628	    if (seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }
1629	    if (is_causal) { window_size_right = 0; }
1630	
1631	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
1632	    // H/t Daniel Haziza
1633	    const int seqlenq_ngroups_swapped = seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && head_size_og % 8 == 0 && !alibi_slopes_.has_value();
1634	    if (seqlenq_ngroups_swapped) {
1635	        const int ngroups = num_heads / num_heads_k;
1636	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size_og}).transpose(1, 2);
1637	        seqlen_q = ngroups;
1638	        num_heads = num_heads_k;
1639	    }
1640	
1641	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
1642	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
1643	
1644	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size_og);
1645	    if (!paged_KV) {
1646	        CHECK_SHAPE(kcache, batch_size_c, seqlen_k, num_heads_k, head_size_og);
1647	        CHECK_SHAPE(vcache, batch_size_c, seqlen_k, num_heads_k, head_size_og);
1648	    } else {
1649	        CHECK_SHAPE(kcache, num_blocks, page_block_size, num_heads_k, head_size_og);
1650	        CHECK_SHAPE(vcache, num_blocks, page_block_size, num_heads_k, head_size_og);
1651	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
1652	    }
1653	
1654	    at::Tensor q_padded, kcache_padded, vcache_padded;
1655	    if (head_size_og % 8 != 0) {
1656	        q_padded = torch::nn::functional::pad(q, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1657	        kcache_padded = torch::nn::functional::pad(kcache, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1658	        vcache_padded = torch::nn::functional::pad(vcache, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1659	    } else {
1660	        q_padded = q;
1661	        kcache_padded = kcache;
1662	        vcache_padded = vcache;
1663	    }
1664	
1665	    at::Tensor out;
1666	    if (out_.has_value()) {
1667	        out = out_.value();
1668	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
1669	        CHECK_DEVICE(out);
1670	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
1671	        CHECK_SHAPE(out, batch_size, seqlen_q, num_heads, head_size_og);
1672	        if (head_size_og % 8 != 0) { out = torch::empty_like(q_padded); }
1673	    } else {
1674	        out = torch::empty_like(q_padded);
1675	    }
1676	
1677	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1678	    const int head_size = round_multiple(head_size_og, 8);
1679	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1680	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
1681	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
1682	
1683	    auto opts = q.options();
1684	
1685	    auto softmax_lse = torch::empty({batch_size, num_heads, seqlen_q}, opts.dtype(at::kFloat));
1686	
1687	    Flash_fwd_params params;
1688	    set_params_fprop(params,
1689	                     batch_size,
1690	                     seqlen_q, seqlen_k,
1691	                     seqlen_q_rounded, seqlen_k_rounded,
1692	                     num_heads, num_heads_k,
1693	                     head_size, head_size_rounded,
1694	                     q_padded, kcache_padded, vcache_padded, out,
1695	                     /*cu_seqlens_q_d=*/nullptr,
1696	                     /*cu_seqlens_k_d=*/nullptr,
1697	                     /*seqused_k=*/nullptr,
1698	                     /*p_ptr=*/nullptr,
1699	                     softmax_lse.data_ptr(),
1700	                     /*p_dropout=*/0.f,
1701	                     softmax_scale,
1702	                     window_size_left,
1703	                     window_size_right,
1704	                     softcap
1705	                     );
1706	
1707	    if (blockmask_.has_value()) {
1708	        params.blockmask = static_cast<uint64_t*>(blockmask_.value().data_ptr());
1709	        params.m_block_dim = 16;
1710	        params.n_block_dim = 64;
1711	        params.num_k_heads = 2;
1712	        params.num_blocks_m = (seqlen_q + 16 - 1) / 16;
1713	        params.num_blocks_n = (seqlen_k + 64 - 1) / 64;
1714	    } else {
1715	        params.blockmask = nullptr;
1716	        params.m_block_dim = 1;
1717	        params.n_block_dim = 1;
1718	    }
1719	
1720	    at::Tensor k, v, k_padded, v_padded;
1721	    if (k_.has_value()) {
1722	        TORCH_CHECK(v_.has_value(), "If key is supplied, value must also be passed in");
1723	        TORCH_CHECK(seqlens_k_.has_value(), "If key is supplied, seqlens_k must also be passed in");
1724	        TORCH_CHECK(seqlen_q <= seqlen_k, "If key is supplied, it must have seqlen <= the seqlen of the KV cache");
1725	        k = k_.value();
1726	        v = v_.value();
1727	        TORCH_CHECK(k.dtype() == q_dtype, "Key must have the same dtype as query");
1728	        TORCH_CHECK(v.dtype() == q_dtype, "Value must have the same dtype as query");
1729	        CHECK_DEVICE(k); CHECK_DEVICE(v);
1730	        TORCH_CHECK(k.stride(-1) == 1, "Key tensor must have contiguous last dimension");
1731	        TORCH_CHECK(v.stride(-1) == 1, "Value tensor must have contiguous last dimension");
1732	        int seqlen_knew = k.size(1);
1733	        CHECK_SHAPE(k, batch_size, seqlen_knew, num_heads_k, head_size_og);
1734	        CHECK_SHAPE(v, batch_size, seqlen_knew, num_heads_k, head_size_og);
1735	        if (head_size_og % 8 != 0) {
1736	            k_padded = torch::nn::functional::pad(k, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1737	            v_padded = torch::nn::functional::pad(v, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1738	        } else {
1739	            k_padded = k;
1740	            v_padded = v;
1741	        }
1742	        params.seqlen_knew = seqlen_knew;
1743	        params.knew_ptr = k_padded.data_ptr();
1744	        params.vnew_ptr = v_padded.data_ptr();
1745	        // All stride are in elements, not bytes.
1746	        params.knew_batch_stride = k_padded.stride(0);
1747	        params.vnew_batch_stride = v_padded.stride(0);
1748	        params.knew_row_stride = k_padded.stride(-3);
1749	        params.vnew_row_stride = v_padded.stride(-3);
1750	        params.knew_head_stride = k_padded.stride(-2);
1751	        params.vnew_head_stride = v_padded.stride(-2);
1752	    }
1753	
1754	    if (seqlens_k_.has_value()) {
1755	        auto seqlens_k = seqlens_k_.value();
1756	        TORCH_CHECK(seqlens_k.dtype() == torch::kInt32, "seqlens_k must have dtype int32");
1757	        CHECK_DEVICE(seqlens_k);
1758	        CHECK_CONTIGUOUS(seqlens_k);
1759	        CHECK_SHAPE(seqlens_k, batch_size);
1760	        params.cu_seqlens_k = static_cast<int *>(seqlens_k.data_ptr());
1761	    }
1762	    params.is_seqlens_k_cumulative = !(seqlens_k_.has_value());
1763	    if (leftpad_k_.has_value()) {
1764	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
1765	        auto leftpad_k = leftpad_k_.value();
1766	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
1767	        CHECK_DEVICE(leftpad_k);
1768	        CHECK_CONTIGUOUS(leftpad_k);
1769	        CHECK_SHAPE(leftpad_k, batch_size);
1770	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
1771	    }
1772	
1773	    if (rotary_cos_.has_value()) {
1774	        TORCH_CHECK(k_.has_value(), "If rotary cos/sin are provided, new key / value to be appended to KV cache must also be provided");
1775	        auto rotary_cos = rotary_cos_.value();
1776	        CHECK_DEVICE(rotary_cos);
1777	        params.rotary_dim = rotary_cos.size(1) * 2;
1778	        TORCH_CHECK(params.rotary_dim <= head_size, "rotary_dim must be <= headdim");
1779	        TORCH_CHECK(params.rotary_dim % 16 == 0, "Only rotary dimensions divisible by 16 are currently supported");
1780	        const int seqlen_ro = rotary_cos.size(0);
1781	        TORCH_CHECK(seqlen_ro >= seqlen_k, "cos/sin seqlen must be at least the seqlen of KV cache");
1782	        CHECK_SHAPE(rotary_cos, seqlen_ro, params.rotary_dim / 2);
1783	        CHECK_CONTIGUOUS(rotary_cos);
1784	        TORCH_CHECK(rotary_cos.scalar_type() == q_dtype, "rotary_cos must have the same dtype as query");
1785	
1786	        TORCH_CHECK(rotary_sin_.has_value(), "If rotary cos is provided, rotary sin must also be provided");
1787	        auto rotary_sin = rotary_sin_.value();
1788	        CHECK_DEVICE(rotary_sin);
1789	        CHECK_SHAPE(rotary_sin, seqlen_ro, params.rotary_dim / 2);
1790	        CHECK_CONTIGUOUS(rotary_sin);
1791	        TORCH_CHECK(rotary_sin.scalar_type() == q_dtype, "rotary_cos must have the same dtype as query");
1792	        params.rotary_cos_ptr = rotary_cos.data_ptr();
1793	        params.rotary_sin_ptr = rotary_sin.data_ptr();
1794	        params.is_rotary_interleaved = is_rotary_interleaved;
1795	    } else {
1796	        params.rotary_dim = 0;
1797	    }
1798	
1799	    if (cache_batch_idx_.has_value()) {
1800	        auto cache_batch_idx = cache_batch_idx_.value();
1801	        CHECK_DEVICE(cache_batch_idx);
1802	        CHECK_CONTIGUOUS(cache_batch_idx);
1803	        TORCH_CHECK(cache_batch_idx.scalar_type() == torch::kInt32, "cache_batch_idx must have dtype int32");
1804	        params.cache_batch_idx = reinterpret_cast<int *>(cache_batch_idx.data_ptr());
1805	    }
1806	
1807	    // Keep references to these tensors to extend their lifetime
1808	    at::Tensor softmax_lse_accum, out_accum;
1809	    std::tie(softmax_lse_accum, out_accum) = set_params_splitkv(
1810	        params, batch_size, num_heads, head_size, seqlen_k, seqlen_q,
1811	        head_size_rounded, /*dropout*/ 0.f, num_splits, get_num_sm(get_current_device()), opts);
1812	
1813	    if (paged_KV) {
1814	        params.block_table = block_table.data_ptr<int>();
1815	        params.block_table_batch_stride = block_table.stride(0);
1816	    }
1817	    params.page_block_size = page_block_size;
1818	
1819	
1820	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1821	
1822	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1823	    // Only split kernel supports appending to KV cache, or indexing to the cache with cache_batch_idx,
1824	    // or paged KV cache
1825	    run_mha_fwd(params, stream, /*force_split_kernel=*/k_.has_value() || cache_batch_idx_.has_value() || paged_KV || true);
1826	
1827	    if (head_size_og % 8 != 0) {
1828	        out = out.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)});
1829	        if (out_.has_value()) { out_.value().copy_(out); }
1830	        if (k_.has_value()) {
1831	            // It's expensive to copy the KV cache here for the case where head size not divisible by 8,
1832	            // but we don't expect to get this case in practice. This is just so that the code works for that case.
1833	            kcache.copy_(kcache_padded.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)}));
1834	            vcache.copy_(vcache_padded.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)}));
1835	        }
1836	    }
1837	
1838	    if (seqlenq_ngroups_swapped) {
1839	        out = out.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size_og});
1840	        softmax_lse = softmax_lse.reshape({batch_size, num_heads_k * seqlen_q, 1});
1841	    }
1842	    return {out, softmax_lse};
1843	}
1844	
1845	
1846
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	
3	namespace flash {
4	
5	class fwdIterator{
6	    public:
7	    template<typename Params, typename BlockInfo>
8	    __device__ fwdIterator(const Params &params, const BlockInfo &binfo, const int kBlockM, const int kBlockN, const int batch_idx, const int head_idx, const int loop_step_idx, int n_block_min, int n_block_max) {//row first
9	        if (params.blockmask == nullptr) {
10	            blockmask_ptr = nullptr;
11	            return;
12	        }
13	        this->cache_seqlen_k = binfo.actual_seqlen_k - binfo.actual_seqlen_q / params.m_block_dim;
14	        this->max_block_idx = cute::ceil_div(binfo.actual_seqlen_k, params.n_block_dim);
15	        this->m_block_dim = params.m_block_dim;
16	        this->n_block_dim = params.n_block_dim;
17	        this->n_block_min = n_block_min;
18	        this->n_block_max = n_block_max;
19	        this->batch_idx = batch_idx;  // Store batch_idx for debugging
20	        this->head_idx = head_idx;
21	
22	        // Calculate the offset for the uint64 blockmask 
23	        const int num_blocks_m = params.num_blocks_m;
24	        const int num_blocks_n = params.num_blocks_n;
25	        const int uint64_per_row = (num_blocks_n + 64 - 1) / 64;
26	        const int row_offset = params.cu_seqlens_q != nullptr ? binfo.blockmask_q_offset(m_block_dim, batch_idx) : batch_idx * params.num_k_heads * params.num_blocks_m;
27	
28	        blockmask_ptr = params.blockmask + 
29	                        head_idx * params.num_blocks_m * uint64_per_row + 
30	                        row_offset * uint64_per_row +
31	                        loop_step_idx * uint64_per_row;
32	
33	        // printf("blockmask_ptr = %d\n", blockmask_ptr);
34	
35	        const int q_block_idx = loop_step_idx + cache_seqlen_k;
36	    }
37	
38	    __device__ int max_no_larger(int target) const {
39	        if (blockmask_ptr == nullptr){
40	            // printf("blockmask_ptr is nullptr\n");
41	            return target;
42	        }
43	        // printf("blockmask_ptr is NOT!!!! nullptr\n");
44	        if(max_block_idx == 0){
45	            return -1;
46	        };
47	        
48	        
49	        // 目标值不能超过最大块索引
50	        target = min(target, max_block_idx - 1);
51	        
52	        // 计算相对于当前q_bit_position的实际位置
53	        int target_bit_pos = target;
54	        
55	        // 确定此块在哪个uint64中
56	        int uint64_offset = target_bit_pos / 64;
57	        
58	        // 确定此块在uint64中的哪一位
59	        int bit_pos = target_bit_pos % 64;
60	        
61	        // 创建一个掩码，保留target及更低位的所有位
62	        uint64_t mask = bit_pos != 63 ? (1ULL << (bit_pos + 1)) - 1 : 0xFFFFFFFFFFFFFFFFULL;
63	        
64	        // 检查当前uint64中target及以下的位
65	        uint64_t value = blockmask_ptr[uint64_offset] & mask;
66	        
67	        // 如果当前uint64中有设置的位
68	        int result = -1;
69	        if (value != 0) {
70	            // 找到最高位的1（即不大于target的最大设置位）
71	            int highest_bit = 63 - __clzll(value);  // __clzll计算前导0的数量
72	            result = highest_bit + (uint64_offset * 64);
73	        } else {
74	            // 如果当前uint64中没有找到，检查更低的uint64块
75	            for (int i = uint64_offset - 1; i >= 0; i--) {
76	                value = blockmask_ptr[i];
77	                if (value != 0) {
78	                    // 找到最高位的1
79	                    int highest_bit = 63 - __clzll(value);
80	                    // 计算相对于q_bit_position的偏移
81	                    result = highest_bit + (i * 64);
82	                    break;
83	                }
84	            }
85	        }
86	
87	        
88	        // 没有找到设置位
89	        return result;
90	    }
91	
92	    uint64_t *blockmask_ptr;
93	    int row_offset; // 行偏移量
94	    int uint64_per_row;          // 每行使用的uint64数量
95	    int cache_seqlen_k;
96	    int max_block_idx;
97	    int m_block_dim, n_block_dim;
98	    int n_block_min, n_block_max;
99	    int batch_idx, head_idx;
100	};
101	
102	class bwdIterator{
103	    public:
104	    template<typename Params, typename BlockInfo>
105	    __device__ bwdIterator(const Params &params, const BlockInfo &binfo, const int kBlockM, const int kBlockN, const int batch_idx, const int head_idx, const int loop_step_idx, int m_block_min, int m_block_max) {
106	        if (params.blockmask == nullptr) {
107	            blockmask_ptr = nullptr;
108	            return;
109	        }
110	        this -> max_block_idx = cute::ceil_div(binfo.actual_seqlen_q, params.m_block_dim);
111	        this -> m_block_dim = params.m_block_dim;
112	        this -> n_block_dim = params.n_block_dim;
113	        this -> m_block_min = m_block_min;
114	        this -> m_block_max = m_block_max;
115	
116	        this -> loop_step_idx = loop_step_idx;
117	            
118	
119	        // 计算块的基本信息
120	        const int blocks_per_uint64 = 64;  // 每个uint64可以存储64个块信息
121	        
122	        // 原始行块的索引起始位置（考虑批次位置）
123	        const int q_block_offset = binfo.blockmask_q_offset(m_block_dim, batch_idx);
124	        
125	        // 计算q_block_offset在uint64表示中的位置
126	        const int q_uint64_idx = q_block_offset / blocks_per_uint64;  // 确定在第几个uint64
127	        const int q_bit_position = q_block_offset % blocks_per_uint64; // 确定在uint64中的第几位
128	        
129	        // 列块的索引（循环步进位置）
130	        const int k_block_idx = loop_step_idx;
131	        
132	        // 计算每行需要多少个uint64来表示
133	        const int num_blocks_m = params.num_blocks_m;
134	        const int uint64_per_row = (num_blocks_m + blocks_per_uint64 - 1) / blocks_per_uint64;
135	        
136	        // 确保这里用的是num_blocks_n而不是num_blocks_m，以匹配前向传播中的计算方式
137	        this->blockmask_ptr = params.blockmask + 
138	                            head_idx * params.num_blocks_n * uint64_per_row + 
139	                            k_block_idx * uint64_per_row +
140	                            q_uint64_idx;
141	        
142	        // 存储块在uint64中的位偏移
143	        this->q_bit_position = q_bit_position;
144	        
145	        // 存储每行使用的uint64数量，用于计算偏移
146	        this->uint64_per_row = uint64_per_row;
147	    };
148	
149	    __device__ int max_no_larger(int target) const {
150	        if (blockmask_ptr == nullptr) {
151	            return target;
152	        }
153	        if(max_block_idx == 0){
154	            return -1;
155	        };
156	        
157	        // 目标值不能超过最大块索引
158	        target = min(target, max_block_idx - 1);
159	        
160	        
161	        // 接下来检查blockmask
162	        const int blocks_per_uint64 = 64;
163	        int target_bit_pos = q_bit_position + target;
164	        
165	        // 确定此块在哪个uint64中
166	        int uint64_offset = target_bit_pos / blocks_per_uint64;
167	        
168	        // 确定此块在uint64中的哪一位
169	        int bit_pos = target_bit_pos % blocks_per_uint64;
170	        
171	        // 创建一个掩码，保留target及更低位的所有位
172	        uint64_t mask = (1ULL << (bit_pos + 1)) - 1;
173	        
174	        // 检查当前uint64中target及以下的位
175	        uint64_t value = blockmask_ptr[uint64_offset] & mask;
176	        int blockmask_result = -1;
177	        
178	        if (value != 0) {
179	            // 找到最高位的1（即不大于target的最大设置位）
180	            int highest_bit = 63 - __clzll(value);  // __clzll计算前导0的数量
181	            blockmask_result = highest_bit + (uint64_offset * blocks_per_uint64) - q_bit_position;
182	        } else {
183	            // 如果当前uint64中没有找到，检查更低的uint64块
184	            for (int i = uint64_offset - 1; i >= 0; i--) {
185	                value = blockmask_ptr[i];
186	                if (value != 0) {
187	                    // 找到最高位的1
188	                    int highest_bit = 63 - __clzll(value);
189	                    // 计算相对于q_bit_position的偏移
190	                    blockmask_result = highest_bit + (i * blocks_per_uint64) - q_bit_position;
191	                    break;
192	                }
193	            }
194	        }
195	
196	        // 返回blockmask结果
197	        return blockmask_result;
198	    };
199	
200	
201	    uint64_t *blockmask_ptr;
202	    int q_bit_position;
203	    int uint64_per_row;
204	    int max_block_idx;
205	    int m_block_dim, n_block_dim;
206	    int m_block_min, m_block_max;
207	    int batch_idx, head_idx;
208	    int loop_step_idx;
209	};
210	
211	}  // namespace flash
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include <cuda.h>
8	#include <vector>
9	
10	#include <ATen/cuda/CUDAGeneratorImpl.h> // For at::Generator and at::PhiloxCudaState
11	
12	constexpr int TOTAL_DIM = 0;
13	constexpr int H_DIM = 1;
14	constexpr int D_DIM = 2;
15	
16	////////////////////////////////////////////////////////////////////////////////////////////////////
17	
18	struct Qkv_params {
19	    using index_t = int64_t;
20	    // The QKV matrices.
21	    void *__restrict__ q_ptr;
22	    void *__restrict__ k_ptr;
23	    void *__restrict__ v_ptr;
24	
25	    // The stride between rows of the Q, K and V matrices.
26	    index_t q_batch_stride;
27	    index_t k_batch_stride;
28	    index_t v_batch_stride;
29	    index_t q_row_stride;
30	    index_t k_row_stride;
31	    index_t v_row_stride;
32	    index_t q_head_stride;
33	    index_t k_head_stride;
34	    index_t v_head_stride;
35	
36	    // The number of heads.
37	    int h, h_k;
38	    // In the case of multi-query and grouped-query attention (MQA/GQA), nheads_k could be
39	    // different from nheads (query).
40	    int h_h_k_ratio; // precompute h / h_k,
41	};
42	
43	////////////////////////////////////////////////////////////////////////////////////////////////////
44	
45	struct Flash_fwd_params : public Qkv_params {
46	
47	    // The O matrix (output).
48	    void * __restrict__ o_ptr;
49	    void * __restrict__ oaccum_ptr;
50	
51	    // The stride between rows of O.
52	    index_t o_batch_stride;
53	    index_t o_row_stride;
54	    index_t o_head_stride;
55	
56	    // The pointer to the P matrix.
57	    void * __restrict__ p_ptr;
58	
59	    // The pointer to the softmax sum.
60	    void * __restrict__ softmax_lse_ptr;
61	    void * __restrict__ softmax_lseaccum_ptr;
62	
63	    // The dimensions.
64	    int b, seqlen_q, seqlen_k, seqlen_v, seqlen_knew, seqlen_vnew, d, seqlen_q_rounded, seqlen_k_rounded, d_rounded, rotary_dim, total_q;
65	
66	    // The scaling factors for the kernel.
67	    float scale_softmax;
68	    float scale_softmax_log2;
69	
70	    // array of length b+1 holding starting offset of each sequence.
71	    int * __restrict__ cu_seqlens_q;
72	    int * __restrict__ cu_seqlens_k;
73	    int * __restrict__ cu_seqlens_v;
74	    int * __restrict__ leftpad_k;
75	    int * __restrict__ leftpad_v;
76	
77	    // If provided, the actual length of each k sequence.
78	    int * __restrict__ seqused_k;
79	    int * __restrict__ seqused_v;
80	    uint64_t *__restrict__ blockmask;
81	    int m_block_dim, n_block_dim, num_k_heads;
82	    int num_blocks_m, num_blocks_n;
83	
84	    // The K_new and V_new matrices.
85	    void * __restrict__ knew_ptr;
86	    void * __restrict__ vnew_ptr;
87	
88	    // The stride between rows of the Q, K and V matrices.
89	    index_t knew_batch_stride;
90	    index_t vnew_batch_stride;
91	    index_t knew_row_stride;
92	    index_t vnew_row_stride;
93	    index_t knew_head_stride;
94	    index_t vnew_head_stride;
95	
96	    // The cos and sin matrices for rotary embedding.
97	    void * __restrict__ rotary_cos_ptr;
98	    void * __restrict__ rotary_sin_ptr;
99	
100	    // The indices to index into the KV cache.
101	    int * __restrict__ cache_batch_idx;
102	
103	    // Paged KV cache
104	    int * __restrict__ block_table;
105	    index_t block_table_batch_stride;
106	    int page_block_size;
107	
108	    // The dropout probability (probability of keeping an activation).
109	    float p_dropout;
110	    // uint32_t p_dropout_in_uint;
111	    // uint16_t p_dropout_in_uint16_t;
112	    uint8_t p_dropout_in_uint8_t;
113	
114	    // Scale factor of 1 / (1 - p_dropout).
115	    float rp_dropout;
116	    float scale_softmax_rp_dropout;
117	
118	    // Local window size
119	    int window_size_left, window_size_right;
120	    float softcap;
121	
122	    // Random state.
123	    at::PhiloxCudaState philox_args;
124	
125	    // Pointer to the RNG seed (idx 0) and offset (idx 1).
126	    uint64_t * rng_state;
127	
128	    bool is_bf16;
129	    bool is_causal;
130	
131	    // If is_seqlens_k_cumulative, then seqlen_k is cu_seqlens_k[bidb + 1] - cu_seqlens_k[bidb].
132	    // Otherwise it's cu_seqlens_k[bidb], i.e., we use cu_seqlens_k to store the sequence lengths of K.
133	    bool is_seqlens_k_cumulative;
134	    
135	    // If is_seqlens_v_cumulative, then seqlen_v is cu_seqlens_v[bidb + 1] - cu_seqlens_v[bidb].
136	    // Otherwise it's cu_seqlens_v[bidb], i.e., we use cu_seqlens_v to store the sequence lengths of V.
137	    bool is_seqlens_v_cumulative;
138	
139	    bool is_rotary_interleaved;
140	
141	    int num_splits;  // For split-KV version
142	
143	    void * __restrict__ alibi_slopes_ptr;
144	    index_t alibi_slopes_batch_stride;
145	
146	    bool unpadded_lse;  // For varlen paths: LSE is in [nheads, total_seqlen_q] format instead of [b, nheads, seqlen_q].
147	    bool seqlenq_ngroups_swapped;  // q has been transposed from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d).
148	};
149	
150	////////////////////////////////////////////////////////////////////////////////////////////////////
151	
152	struct Flash_bwd_params : public Flash_fwd_params {
153	
154	    // The dO and dQKV matrices.
155	    void *__restrict__ do_ptr;
156	    void *__restrict__ dq_ptr;
157	    void *__restrict__ dk_ptr;
158	    void *__restrict__ dv_ptr;
159	
160	    // To accumulate dQ
161	    void *__restrict__ dq_accum_ptr;
162	    void *__restrict__ dk_accum_ptr;
163	    void *__restrict__ dv_accum_ptr;
164	
165	    // // To accumulate dK and dV in case we're splitting the bwd along seqlen_q
166	    // dimension void *__restrict__ dk_accum_ptr; void *__restrict__
167	    // dv_accum_ptr;
168	
169	    // The stride between rows of the dO, dQ, dK and dV matrices.
170	    // TD [2022-04-16]: We're using 32-bit indexing to save registers.
171	    // The code probably won't work for arrays larger than 2GB.
172	    index_t do_batch_stride;
173	    index_t do_row_stride;
174	    index_t do_head_stride;
175	    index_t dq_batch_stride;
176	    index_t dk_batch_stride;
177	    index_t dv_batch_stride;
178	    index_t dq_row_stride;
179	    index_t dk_row_stride;
180	    index_t dv_row_stride;
181	    index_t dq_head_stride;
182	    index_t dk_head_stride;
183	    index_t dv_head_stride;
184	
185	    // The pointer to the softmax d sum.
186	    void *__restrict__ dsoftmax_sum;
187	
188	    bool deterministic;
189	    index_t dq_accum_split_stride;
190	};
191	
192	////////////////////////////////////////////////////////////////////////////////////////////////////
193	
194	template<typename T, int Headdim, bool Is_causal> void run_mha_fwd_(Flash_fwd_params &params, cudaStream_t stream);
195	template<typename T, int Headdim, bool Is_causal> void run_mha_fwd_splitkv_dispatch(Flash_fwd_params &params, cudaStream_t stream);
196	
197	template<typename T, int Headdim, bool Is_causal> void run_mha_bwd_(Flash_bwd_params &params, cudaStream_t stream);
198
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h"
}
```

> TOOL

tool_result Read
```
File content (28105 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	#include <c10/cuda/CUDAException.h>  // For C10_CUDA_CHECK and C10_CUDA_KERNEL_LAUNCH_CHECK
7	
8	#include "static_switch.h"
9	#include "hardware_info.h"
10	#include "flash.h"
11	#include "flash_fwd_kernel.h"
12	
13	// Determine if the architecture supports FLASH and define a macro to handle parameter modifiers
14	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
15	#define ARCH_SUPPORTS_FLASH
16	#define KERNEL_PARAM_MODIFIER __grid_constant__
17	#else
18	#define KERNEL_PARAM_MODIFIER
19	#endif
20	
21	// Define a macro for unsupported architecture handling to centralize the error message
22	#define FLASH_UNSUPPORTED_ARCH printf("FATAL: FlashAttention requires building with sm version sm80-sm90, but was built for < 8.0!");
23	
24	// Use a macro to clean up kernel definitions
25	#define DEFINE_FLASH_FORWARD_KERNEL(kernelName, ...) \
26	template<typename Kernel_traits, __VA_ARGS__> \
27	__global__ void kernelName(KERNEL_PARAM_MODIFIER const Flash_fwd_params params)
28	
29	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_kernel, bool Is_dropout, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Return_softmax) {
30	    #if defined(ARCH_SUPPORTS_FLASH)
31	        static_assert(!(Is_causal && Is_local)); // Enforce constraints
32	        flash::compute_attn<Kernel_traits, Is_dropout, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Return_softmax>(params);
33	    #else
34	        FLASH_UNSUPPORTED_ARCH
35	    #endif
36	}
37	
38	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_kernel, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV) {
39	    #if defined(ARCH_SUPPORTS_FLASH)
40	        flash::compute_attn_splitkv<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params);
41	    #else
42	        FLASH_UNSUPPORTED_ARCH
43	    #endif
44	}
45	
46	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_stage1_kernel, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV) {
47	    #if defined(ARCH_SUPPORTS_FLASH)
48	        flash::compute_attn_splitkv_stage1<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params);
49	    #else
50	        FLASH_UNSUPPORTED_ARCH
51	    #endif
52	}
53	
54	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_combine_kernel, int kBlockM, int Log_max_splits, bool Is_even_K) {
55	    static_assert(Log_max_splits >= 1);
56	    flash::combine_attn_seqk_parallel<Kernel_traits, kBlockM, Log_max_splits, Is_even_K>(params);
57	}
58	
59	template<typename Kernel_traits, bool Is_dropout, bool Is_causal>
60	void run_flash_fwd(Flash_fwd_params &params, cudaStream_t stream) {
61	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
62	    // printf("smem_size = %d\n", smem_size);
63	
64	    // Work-around for gcc 7. It doesn't like nested BOOL_SWITCH.
65	    // https://github.com/kokkos/kokkos-kernels/issues/349
66	    // https://github.com/HazyResearch/flash-attention/issues/21
67	
68	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
69	    dim3 grid(num_m_block, params.b, params.h);
70	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
71	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
72	    // const bool return_softmax = params.p_ptr != nullptr;
73	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
74	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
75	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
76	            constexpr static bool Is_local = false; { // TODO remove debug info
77	                // BOOL_SWITCH(return_softmax, ReturnSoftmaxConst, [&] {
78	                constexpr static bool ReturnSoftmaxConst = false; { // TODO remove debug info
79	                    // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
80	                    constexpr static bool Has_alibi = false; { // TODO remove debug info
81	                        // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
82	                        constexpr static bool Is_softcap = false; {
83	                            // Will only return softmax if dropout, to reduce compilation time.
84	                            // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
85	                            // If return_softmax, set IsEvenMNConst to false to reduce number of templates
86	                            // If head dim > 128, set IsEvenMNConst to false to reduce number of templates
87	                            // If Is_local, set Is_causal to false
88	                            auto kernel = &flash_fwd_kernel<Kernel_traits, Is_dropout && !Is_softcap, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && IsEvenKConst && !Is_local && !ReturnSoftmaxConst && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, ReturnSoftmaxConst && Is_dropout && !Is_softcap>;
89	                            // auto kernel = &flash_fwd_kernel<Kernel_traits, false, Is_causal, false, false, true, true, false>;
90	                            // printf("IsEvenMNConst = %d, IsEvenKConst = %d, Is_local = %d, Is_causal = %d, ReturnSoftmaxConst = %d, Is_dropout = %d\n", int(IsEvenMNConst), int(IsEvenKConst), int(Is_local), int(Is_causal), int(ReturnSoftmaxConst), int(Is_dropout));
91	                            // auto kernel = &flash_fwd_kernel<Kernel_traits, false, Is_causal, false, true, true, false>;
92	                            if (smem_size >= 48 * 1024) {
93	                                C10_CUDA_CHECK(cudaFuncSetAttribute(
94	                                    kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
95	                            }
96	                            // int ctas_per_sm;
97	                            // cudaError status_ = cudaOccupancyMaxActiveBlocksPerMultiprocessor(
98	                            //     &ctas_per_sm, kernel, Kernel_traits::kNThreads, smem_size);
99	                            // printf("smem_size = %d, CTAs per SM = %d\n", int(smem_size), ctas_per_sm);
100	                            kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
101	                            C10_CUDA_KERNEL_LAUNCH_CHECK();
102	                        }
103	                    }
104	                }
105	            }
106	        });
107	    });
108	}
109	
110	template<typename Kernel_traits, bool Is_causal>
111	void run_flash_splitkv_fwd(Flash_fwd_params &params, cudaStream_t stream) {
112	    static_assert(!Kernel_traits::Is_Q_in_regs, "SplitKV implementation does not support Is_Q_in_regs");
113	    static_assert(!Kernel_traits::Share_Q_K_smem, "SplitKV implementation does not support Share_Q_K_smem");
114	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
115	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
116	    dim3 grid(num_m_block, params.num_splits > 1 ? params.num_splits : params.b, params.num_splits > 1 ? params.b * params.h : params.h);
117	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
118	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
119	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
120	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
121	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
122	            constexpr static bool Is_local = false; { // TODO remove debug info
123	                BOOL_SWITCH(params.num_splits > 1, Split, [&] {
124	                    BOOL_SWITCH(params.knew_ptr != nullptr, Append_KV, [&] {
125	                        // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
126	                        constexpr static bool Has_alibi = false; { // TODO remove debug info
127	                            // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
128	                            constexpr static bool Is_softcap = false; { // TODO remove debug info
129	                                // If Append_KV, then we must have seqlen_offsets, which means cu_seqlens_k != nullptr.
130	                                // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
131	                                // If Is_local, set Is_causal to false
132	                                auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && !Append_KV && IsEvenKConst && !Is_local && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, Split, Append_KV>;
133	                                // auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, false, true, Split, Append_KV>;
134	                                // auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, false, IsEvenKConst>;
135	                                if (smem_size >= 48 * 1024) {
136	                                    C10_CUDA_CHECK(cudaFuncSetAttribute(
137	                                        kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
138	                                }
139	                                kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
140	                                C10_CUDA_KERNEL_LAUNCH_CHECK();
141	                            }
142	                        }
143	                    });
144	                });
145	            }
146	        });
147	    });
148	    if (params.num_splits > 1) {
149	        // We want kBlockM to be as small as possible for more parallelism.
150	        // With 128 threads we can load 512 elements at a time, so if headdim is divisible by 128, kBlockM = 4.
151	        // If headdim is divisible by 64, then we set kBlockM = 8, etc.
152	        constexpr static int kBlockM = Kernel_traits::kHeadDim % 128 == 0 ? 4 : (Kernel_traits::kHeadDim % 64 == 0 ? 8 : 16);
153	        dim3 grid_combine((params.b * params.h * params.seqlen_q + kBlockM - 1) / kBlockM);
154	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
155	            if (params.num_splits <= 2) {
156	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 1, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
157	            } else if (params.num_splits <= 4) {
158	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 2, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
159	            } else if (params.num_splits <= 8) {
160	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 3, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
161	            } else if (params.num_splits <= 16) {
162	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 4, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
163	            } else if (params.num_splits <= 32) {
164	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 5, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
165	            } else if (params.num_splits <= 64) {
166	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 6, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
167	            } else if (params.num_splits <= 128) {
168	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 7, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
169	            }
170	            C10_CUDA_KERNEL_LAUNCH_CHECK();
171	        });
172	    }
173	}
174	
175	template<typename Kernel_traits, bool Is_causal>
176	void run_flash_splitkv_fwd_stage1(Flash_fwd_params &params, cudaStream_t stream) {
177	    static_assert(!Kernel_traits::Is_Q_in_regs, "SplitKV implementation does not support Is_Q_in_regs");
178	    static_assert(!Kernel_traits::Share_Q_K_smem, "SplitKV implementation does not support Share_Q_K_smem");
179	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
180	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
181	    dim3 grid(num_m_block, params.num_splits > 1 ? params.num_splits : params.b, params.num_splits > 1 ? params.b * params.h : params.h);
182	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
183	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
184	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
185	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
186	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
187	            constexpr static bool Is_local = false; { // TODO remove debug info
188	                // BOOL_SWITCH(params.num_splits > 1, Split, [&] {
189	                constexpr static bool Split = false; { // TODO remove debug info
190	                    // BOOL_SWITCH(params.knew_ptr != nullptr, Append_KV, [&] {
191	                    constexpr static bool Append_KV = false; { // TODO remove debug info
192	                        // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
193	                        constexpr static bool Has_alibi = false; { // TODO remove debug info
194	                            // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
195	                            constexpr static bool Is_softcap = false; { // TODO remove debug info
196	                                // If Append_KV, then we must have seqlen_offsets, which means cu_seqlens_k != nullptr.
197	                                // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
198	                                // If Is_local, set Is_causal to false
199	                                auto kernel = &flash_fwd_splitkv_stage1_kernel<Kernel_traits, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && !Append_KV && IsEvenKConst && !Is_local && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, Split, Append_KV>;
200	                                if (smem_size >= 48 * 1024) {
201	                                    C10_CUDA_CHECK(cudaFuncSetAttribute(
202	                                        kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
203	                                }
204	                                kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
205	                                C10_CUDA_KERNEL_LAUNCH_CHECK();
206	                            }
207	                        }
208	                    }
209	                }
210	            }
211	        });
212	    });
213	}
214	
215	template<typename T, int Headdim, bool Is_causal>
216	void run_mha_fwd_splitkv_dispatch(Flash_fwd_params &params, cudaStream_t stream) {
217	    if (params.blockmask == nullptr) {
218	        constexpr static int kBlockM = 64;  // Fixed for all head dimensions
219	        // TD [2023-08-28]: nvcc segfaults for headdim 96 with block size 64 x 256,
220	        // and for headdim 192 with block size 64 x 128.
221	        // Also for headdim 160 with block size 64 x 128 after the rotary addition.
222	        constexpr static int kBlockN = Headdim <= 64 ? 256 : (Headdim <= 128 ? 128 : 64);
223	        if (params.m_block_dim == 1) {
224	            run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 4, false, false, T>, Is_causal>(params, stream);
225	        } else {
226	            run_flash_splitkv_fwd_stage1<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_causal>(params, stream);
227	        }
228	    } else if (params.cu_seqlens_q != nullptr) {
229	        constexpr static int kBlockM = 16;
230	        constexpr static int kBlockN = 64;
231	        run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 1, false, false, T>, Is_causal>(params, stream);
232	    } else {
233	        constexpr static int kBlockM = 64;
234	        constexpr static int kBlockN = 64;
235	        run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 4, false, false, T>, Is_causal>(params, stream);
236	    }
237	}
238	
239	template<typename T, bool Is_causal>
240	void run_mha_fwd_hdim32(Flash_fwd_params &params, cudaStream_t stream) {
241	    constexpr static int Headdim = 32;
242	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
243	        run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
244	    });
245	}
246	
247	template<typename T, bool Is_causal>
248	void run_mha_fwd_hdim64(Flash_fwd_params &params, cudaStream_t stream) {
249	    constexpr static int Headdim = 64;
250	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
251	        if constexpr(!Is_dropout) {
252	            // Using 8 warps is 18% slower for seqlen=2k, 2 warps is 5% slower
253	            // Using block size (64 x 256) is 27% slower for seqlen=2k
254	            // Using block size (256 x 64) is 85% slower for seqlen=2k, because of register spilling
255	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
256	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
257	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
258	        } else {
259	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
260	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
261	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
262	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
263	        }
264	    });
265	}
266	
267	template<typename T, bool Is_causal>
268	void run_mha_fwd_hdim96(Flash_fwd_params &params, cudaStream_t stream) {
269	    constexpr static int Headdim = 96;
270	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
271	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
272	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
273	        // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
274	        if (is_sm8x) {
275	            if constexpr(!Is_causal) {
276	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
277	            } else {
278	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
279	            }
280	        } else {
281	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
282	        }
283	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
284	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
285	        // These two are always slower
286	        // run_flash_fwd<Flash_fwd_kernel_traits<96, 128, 128, 4, true, T>>(params, stream);
287	        // run_flash_fwd<Flash_fwd_kernel_traits<96, 64, 128, 4, true, T>>(params, stream);
288	    });
289	}
290	
291	template<typename T, bool Is_causal>
292	void run_mha_fwd_hdim128(Flash_fwd_params &params, cudaStream_t stream) {
293	    constexpr static int Headdim = 128;
294	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
295	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
296	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
297	        if constexpr(!Is_dropout) {
298	            // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
299	            // and 128 x 32 (48 KB smem) is the fastest for non-causal since we get 2 CTAs per SM.
300	            if (is_sm8x) {
301	                if constexpr(!Is_causal) {
302	                    run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
303	                } else {
304	                    run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
305	                }
306	            } else {
307	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
308	            }
309	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
310	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
311	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
312	            // Using 8 warps (128 x 128 and 256 x 64) is 28% slower for seqlen=2k
313	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
314	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
315	            // 1st ones are good for H100, A100
316	            // 2nd one is good for A6000 bc we get slightly better occupancy
317	        } else {
318	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
319	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
320	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
321	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
322	        }
323	    });
324	}
325	
326	template<typename T, bool Is_causal>
327	void run_mha_fwd_hdim160(Flash_fwd_params &params, cudaStream_t stream) {
328	    constexpr static int Headdim = 160;
329	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
330	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
331	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
332	        // For A100, H100, 128 x 32 is the fastest.
333	        // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
334	        // and 128 x 64 with 8 warps is the fastest for non-causal.
335	        if (is_sm8x) {
336	            if constexpr(!Is_causal) {
337	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
338	            } else {
339	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
340	            }
341	        } else {
342	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
343	        }
344	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, false, true, T>, Is_dropout, Is_causal>(params, stream);
345	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
346	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, T>>(params, stream);
347	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, T>>(params, stream);
348	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, T>>(params, stream);
349	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, T>>(params, stream);
350	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, T>>(params, stream);
351	    });
352	}
353	
354	template<typename T, bool Is_causal>
355	void run_mha_fwd_hdim192(Flash_fwd_params &params, cudaStream_t stream) {
356	    constexpr static int Headdim = 192;
357	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
358	        if constexpr(!Is_dropout) {
359	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
360	        } else {
361	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
362	        }
363	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
364	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
365	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, T>>(params, stream);
366	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, T>>(params, stream);
367	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, T>>(params, stream);
368	    });
369	}
370	
371	template<typename T, bool Is_causal>
372	void run_mha_fwd_hdim256(Flash_fwd_params &params, cudaStream_t stream) {
373	    constexpr static int Headdim = 256;
374	    int device;
375	    cudaGetDevice(&device);
376	    int max_smem_per_sm, max_smem_per_block;
377	    cudaError status_ = cudaDeviceGetAttribute(
378	        &max_smem_per_sm, cudaDevAttrMaxSharedMemoryPerMultiprocessor, device);
379	    status_ = cudaDeviceGetAttribute(
380	        &max_smem_per_block, cudaDevAttrMaxSharedMemoryPerBlockOptin, device);
381	    if (status_ != cudaSuccess) {
382	      C10_CUDA_CHECK(status_);
383	    }
384	    // printf("max_smem_per_sm = %d, max_smem_per_block = %d\n", max_smem_per_sm, max_smem_per_block);
385	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
386	        // For A100, we want to run with 128 x 64 (128KB smem).
387	        // For H100 we want to run with 64 x 64 (96KB smem) since then we can get 2 CTAs per SM.
388	        if (max_smem_per_block >= 2 * Headdim * (128 + 2 * 64) && max_smem_per_sm < 4 * Headdim * (64 + 2 * 64)) {
389	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
390	        } else {
391	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
392	        }
393	        // 64 KB
394	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
395	        // 96 KB
396	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
397	    });
398	}
399
```

> AGENT

现在我来读取 flash 前向传播的内核头文件，以理解实际的注意力计算逻辑。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 1
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include "philox_unpack.cuh" // For at::cuda::philox::unpack
8	
9	#include <cute/tensor.hpp>
10	
11	#include <cutlass/cutlass.h>
12	#include <cutlass/array.h>
13	#include <cutlass/numeric_types.h>
14	
15	#include "block_info.h"
16	#include "kernel_traits.h"
17	#include "utils.h"
18	#include "softmax.h"
19	#include "mask.h"
20	#include "dropout.h"
21	#include "rotary.h"
22	#include "flash_blockmask.h"
23	
24	namespace flash {
25	
26	using namespace cute;
27	
28	////////////////////////////////////////////////////////////////////////////////////////////////////
29	
30	__forceinline__ __device__ float minusinf_to_zero(float &input) {
31	    if (input == -INFINITY) {
32	        return 0;
33	    } else {
34	        return input;
35	    }
36	}
37	
38	template<int thr_offset, typename Engine0, typename Layout0, typename Operator>
39	__forceinline__ __device__  void thread_element_wise_reduce_(Tensor<Engine0, Layout0> &tensor, Operator &op) {
40	    static_assert(Layout0::rank == 2, "Only support 2D Tensor");
41	    #pragma unroll
42	    for (int mi = 0; mi < size<0>(tensor); mi++) {
43	        #pragma unroll
44	        for (int ni = 0; ni < size<1>(tensor); ni++) {
45	            tensor(mi, ni) = op(
46	                minusinf_to_zero(tensor(mi, ni)), 
47	                __shfl_xor_sync(uint32_t(-1), minusinf_to_zero(tensor(mi, ni)), thr_offset)
48	            );
49	        }
50	    }
51	}
52	
53	template <typename Element, typename E1, typename L1, typename E2, typename L2>
54	__forceinline__ __device__ void hdim16_reduce(
55	    Tensor<E1, L1> &acc_S, 
56	    Tensor<E2, L2> &g_Sh,
57	    const int col_idx_offset_,
58	    const int row_idx_offset_,
59	    const int warp_row_stride) {
60	
61	    // Reshape tensor_ from (MMA=4, MMA_M, MMA_N) (or (_2,_2),_2,_16) for D=32) to (nrow=(2, MMA_M), ncol=(2, MMA_N))
62	    auto tensor = make_tensor(acc_S.data(), flash::convert_layout_acc_rowcol(acc_S.layout()));
63	    const int warp_id = threadIdx.x / 32;
64	    const int lane_id = threadIdx.x % 32;
65	    // const int col_idx_offset = col_idx_offset_ + (lane_id % 4) * 2;
66	    // const int row_idx_offset = row_idx_offset_ + warp_id * 16 + lane_id / 4;
67	    const int col_idx_offset = 0 + (lane_id % 4) * 2;
68	    const int row_idx_offset = 0 + warp_id * 16 + lane_id / 4;
69	
70	    // step 1: 线程内部求和 (v0 + v2)
71	    using TensorT = decltype(make_tensor<float>(Shape< Int<size<0, 1>(tensor)>, Int<size<1>(tensor)> >{}));
72	    TensorT v02;
73	    clear(v02);
74	    #pragma unroll
75	    for (int mi = 0; mi < size<0, 1>(tensor); ++mi) {
76	        #pragma unroll
77	        for (int nj = 0; nj < size<1, 1>(tensor); ++nj) {
78	            #pragma unroll
79	            for (int j = 0; j < size<1, 0>(tensor); ++j) {
80	                const int col_idx_v02 = j * size<1, 1>(tensor) + nj;
81	                const float v0 = minusinf_to_zero(tensor(make_coord(0, mi), make_coord(j, nj)));
82	                const float v2 = minusinf_to_zero(tensor(make_coord(1, mi), make_coord(j, nj)));
83	                v02(mi, col_idx_v02) = v0 + v2;
84	            }
85	        }
86	    }
87	
88	    // step 2: warp 内部蝶形求和
89	    SumOp<float> sum_op;
90	    thread_element_wise_reduce_<16>(v02, sum_op);
91	    thread_element_wise_reduce_<8> (v02, sum_op);
92	    thread_element_wise_reduce_<4> (v02, sum_op);
93	
94	    // step 3: copy 到 global mem
95	    cutlass::NumericConverter<Element, float> converter;
96	    if (lane_id < 4) {
97	        #pragma unroll
98	        for (int mi = 0; mi < size<0, 1>(tensor); ++mi) {
99	            const int row_idx_base = row_idx_offset + mi * warp_row_stride;
100	            #pragma unroll
101	            for (int nj = 0; nj < size<1, 1>(tensor); ++nj) {
102	                const int col_idx_base = col_idx_offset + nj * 8;
103	                #pragma unroll
104	                for (int j = 0; j < size<1, 0>(tensor); ++j) {
105	                    const int col_idx = col_idx_base + j;
106	                    const int col_idx_v02 = j * size<1, 1>(tensor) + nj;
107	                    g_Sh(row_idx_base/16, col_idx) = converter(v02(mi, col_idx_v02)); // ignore /16 since it's too slow
108	                }
109	            }
110	        }
111	    }
112	}
113	
114	////////////////////////////////////////////////////////////////////////////////////////////////////
115	
116	template<typename ElementAccum, typename Params, int kBlockM, bool Is_even_MN>
117	__forceinline__ __device__ auto get_lse_tile(const Params &params, const int bidb, const int bidh, const int m_block, const BlockInfo</*Varlen=*/!Is_even_MN> &binfo) {
118	        // When params.unpadded_lse is false, LSE is written as (b, h, seqlen_q) - this is non-variable seqlen path.
119	        // Otherwise, when params.seqlenq_ngroups_swapped is true, it is written as (h, seqlen_q, b) to account for seqlen_q <-> h swapping trick.
120	        // Otherwise, it's written as (h, b, seqlen_q).
121	        const bool varlen_q = params.unpadded_lse && !params.seqlenq_ngroups_swapped;
122	        auto lse_offset = varlen_q ? binfo.q_offset(params.seqlen_q, 1, bidb) : 0;
123	        auto gmem_ptr_lse = make_gmem_ptr(reinterpret_cast<ElementAccum*>(params.softmax_lse_ptr) + lse_offset);
124	
125	        auto lse_shape = varlen_q ? make_shape(1, params.h, params.total_q) : make_shape(params.b, params.h, params.seqlen_q);
126	        auto lse_stride = params.seqlenq_ngroups_swapped ? make_stride(1, params.seqlen_q * params.b, params.b) : (
127	            params.unpadded_lse ? make_stride(params.h * params.total_q, params.total_q, 1) :  make_stride(params.h * params.seqlen_q, params.seqlen_q, 1)
128	            );
129	
130	        auto lse_layout = make_layout(lse_shape, lse_stride);
131	        Tensor mLSE = make_tensor(gmem_ptr_lse, lse_layout);
132	        auto mLSE_slice = varlen_q ? mLSE(0, bidh, _) : mLSE(bidb, bidh, _);
133	        return local_tile(mLSE_slice, Shape<Int<kBlockM>>{}, make_coord(m_block));
134	}
135	
136	
137	template<typename Kernel_traits, bool Is_dropout, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Return_softmax, typename Params>
138	inline __device__ void compute_attn_1rowblock(const Params &params, const int bidb, const int bidh, const int m_block) {
139	
140	    using Element = typename Kernel_traits::Element;
141	    using ElementAccum = typename Kernel_traits::ElementAccum;
142	    using index_t = typename Kernel_traits::index_t;
143	
144	    // Shared memory.
145	    extern __shared__ char smem_[];
146	
147	    // The thread index.
148	    const int tidx = threadIdx.x;
149	
150	    constexpr int kBlockM = Kernel_traits::kBlockM;
151	    constexpr int kBlockN = Kernel_traits::kBlockN;
152	    constexpr int kHeadDim = Kernel_traits::kHeadDim;
153	    constexpr int kNWarps = Kernel_traits::kNWarps;
154	
155	    auto seed_offset = at::cuda::philox::unpack(params.philox_args);
156	    flash::Dropout dropout(std::get<0>(seed_offset), std::get<1>(seed_offset), params.p_dropout_in_uint8_t,
157	                           bidb, bidh, tidx, params.h);
158	
159	    // Save seed and offset for backward, before any early exiting. Otherwise the 0-th thread block might
160	    // exit early and no one saves the rng states.
161	    if (Is_dropout && blockIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0 && tidx == 0) {
162	        params.rng_state[0] = std::get<0>(seed_offset);
163	        params.rng_state[1] = std::get<1>(seed_offset);
164	    }
165	
166	    const BlockInfo</*Varlen=*/!Is_even_MN> binfo(params, bidb);
167	    if (m_block * kBlockM >= binfo.actual_seqlen_q) return;
168	
169	    const int n_block_min = !Is_local ? 0 : std::max(0, (m_block * kBlockM + binfo.actual_seqlen_k - binfo.actual_seqlen_q - params.window_size_left) / kBlockN);
170	    int n_block_max = cute::ceil_div(binfo.actual_seqlen_k, kBlockN);
171	    if (Is_causal || Is_local) {
172	        n_block_max = std::min(n_block_max,
173	                               cute::ceil_div((m_block + 1) * kBlockM / params.m_block_dim + binfo.actual_seqlen_k - (binfo.actual_seqlen_q / params.m_block_dim) + params.window_size_right, kBlockN));
174	        // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) {
175	        //     printf("m_block = %d, n_block_max = %d\n", m_block, n_block_max);
176	        // }
177	    }
178	    // We exit early and write 0 to gO and gLSE. This also covers the case where actual_seqlen_k == 0.
179	    // Otherwise we might read OOB elements from gK and gV.
180	    if ((Is_causal || Is_local || !Is_even_MN) && n_block_max <= n_block_min) {
181	        Tensor mO = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.o_ptr)
182	                                              + binfo.q_offset(params.o_batch_stride, params.o_row_stride, bidb)),
183	                                make_shape(binfo.actual_seqlen_q, params.h, params.d),
184	                                make_stride(params.o_row_stride, params.o_head_stride, _1{}));
185	        Tensor gO = local_tile(mO(_, bidh, _), Shape<Int<kBlockM>, Int<kHeadDim>>{},
186	                              make_coord(m_block, 0));  // (kBlockM, kHeadDim)
187	
188	        Tensor gLSE = get_lse_tile<ElementAccum, Params, kBlockM, Is_even_MN>(params, bidb, bidh, m_block, binfo);
189	
190	        typename Kernel_traits::GmemTiledCopyO gmem_tiled_copy_O;
191	        auto gmem_thr_copy_O = gmem_tiled_copy_O.get_thread_slice(tidx);
192	        Tensor tOgO = gmem_thr_copy_O.partition_D(gO);
193	        Tensor tOrO = make_tensor<Element>(shape(tOgO));
194	        clear(tOrO);
195	        // Construct identity layout for sO
196	        Tensor cO = make_identity_tensor(make_shape(size<0>(gO), size<1>(gO)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
197	        // Repeat the partitioning with identity layouts
198	        Tensor tOcO = gmem_thr_copy_O.partition_D(cO);
199	        Tensor tOpO = make_tensor<bool>(make_shape(size<2>(tOgO)));
200	        if (!Is_even_K) {
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include "cute/tensor.hpp"
8	
9	#include "cutlass/cutlass.h"
10	#include "cutlass/layout/layout.h"
11	#include <cutlass/numeric_types.h>
12	
13	using namespace cute;
14	
15	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t>
16	struct Flash_kernel_traits {
17	
18	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
19	    using Element = elem_type;
20	    static constexpr bool Has_cp_async = true;
21	#else
22	    using Element = cutlass::half_t;
23	    static constexpr bool Has_cp_async = false;
24	#endif
25	
26	    using ElementAccum = float;
27	    using index_t = int64_t;
28	
29	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
30	    using MMA_Atom_Arch = std::conditional_t<
31	        std::is_same_v<elem_type, cutlass::half_t>,
32	        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,
33	        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>
34	    >;
35	#else
36	    using MMA_Atom_Arch = MMA_Atom<SM75_16x8x8_F32F16F16F32_TN>;
37	#endif
38	
39	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 750
40	    using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>;
41	    using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>;
42	#else
43	    using SmemCopyAtom = Copy_Atom<DefaultCopy, elem_type>;
44	    using SmemCopyAtomTransposed = Copy_Atom<DefaultCopy, elem_type>;
45	#endif
46	};
47	
48	// If Share_Q_K_smem is true, that forces Is_Q_in_regs to be true
49	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, bool Is_Q_in_regs_=false, bool Share_Q_K_smem_=false, typename elem_type=cutlass::half_t,
50	         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
51	struct Flash_fwd_kernel_traits : public Base {
52	    using Element = typename Base::Element;
53	    using ElementAccum = typename Base::ElementAccum;
54	    using index_t = typename Base::index_t;
55	    static constexpr bool Has_cp_async = Base::Has_cp_async;
56	    using SmemCopyAtom = typename Base::SmemCopyAtom;
57	    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;
58	
59	    static constexpr bool Share_Q_K_smem = Share_Q_K_smem_;
60	    static constexpr bool Is_Q_in_regs = Is_Q_in_regs_ || Share_Q_K_smem;
61	
62	    // The number of threads.
63	    static constexpr int kNWarps = kNWarps_;
64	    static constexpr int kNThreads = kNWarps * 32;
65	
66	    static constexpr int kBlockM = kBlockM_;
67	    static constexpr int kBlockN = kBlockN_;
68	    static constexpr int kHeadDim = kHeadDim_;
69	    static_assert(kHeadDim % 32 == 0);
70	    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
71	    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
72	    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;
73	
74	    using TiledMma = TiledMMA<
75	        typename Base::MMA_Atom_Arch,
76	        Layout<Shape<Int<kNWarps>,_1,_1>>,  // 4x1x1 or 8x1x1 thread group
77	        Tile<Int<16 * kNWarps>, _16, _16>>;
78	
79	    using SmemLayoutAtomQ = decltype(
80	        composition(Swizzle<kSwizzle, 3, 3>{},
81	                    // This has to be kBlockKSmem, using kHeadDim gives wrong results for d=128
82	                    Layout<Shape<_8, Int<kBlockKSmem>>,
83	                           Stride<Int<kBlockKSmem>, _1>>{}));
84	    using SmemLayoutQ = decltype(tile_to_shape(
85	        SmemLayoutAtomQ{},
86	        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
87	
88	    using SmemLayoutKV = decltype(tile_to_shape(
89	        SmemLayoutAtomQ{},
90	        Shape<Int<kBlockN>, Int<kHeadDim>>{}));
91	
92	    // https://github.com/ColfaxResearch/cutlass-kernels/blob/a222587e6d59b93ba704853d3946fb686d8b8892/src/fmha/fmha_forward.cu#L434
93	    using SmemLayoutVtransposed = decltype(
94	        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
95	    using SmemLayoutVtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutVtransposed{}));
96	
97	    using SmemLayoutAtomO = decltype(
98	        composition(Swizzle<kSwizzle, 3, 3>{},
99	                    Layout<Shape<Int<8>, Int<kBlockKSmem>>,
100	                           Stride<Int<kBlockKSmem>, _1>>{}));
101	    using SmemLayoutO = decltype(tile_to_shape(
102	        SmemLayoutAtomO{},
103	        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
104	    using SmemCopyAtomO = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>;
105	    using SmemCopyAtomOaccum = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>;
106	
107	    static constexpr int kSmemQSize = size(SmemLayoutQ{}) * sizeof(Element);
108	    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
109	    static constexpr int kSmemSize = Share_Q_K_smem ? std::max(kSmemQSize, kSmemKVSize) : kSmemQSize + kSmemKVSize;
110	
111	    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
112	    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
113	    // Using kBlockKSmem here is 6-10% faster than kBlockKGmem for d=128 because of bank conflicts.
114	    // For example, for d=128, smem is split into 2 "pages", each page takes care of columns
115	    // 0-63 and 64-127. If we have 16 threads per row for gmem read, when we write to smem,
116	    // thread 0 - 7 will write to the first page and thread 8 - 15 will write to the second page,
117	    // to the same banks.
118	    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
119	    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
120	    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
121	                                  Stride<Int<kGmemThreadsPerRow>, _1>>;
122	
123	    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
124	    // from the same address by the same threadblock. This is slightly faster.
125	    using Gmem_copy_struct = std::conditional_t<
126	        Has_cp_async,
127	        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
128	        AutoVectorizingCopyWithAssumedAlignment<128>
129	    >;
130	    using GmemTiledCopyQKV = decltype(
131	        make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{},
132	                        GmemLayoutAtom{},
133	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
134	    using GmemTiledCopyO = decltype(
135	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
136	                        GmemLayoutAtom{},
137	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per store
138	
139	    using GmemLayoutAtomOaccum = std::conditional_t<
140	        kBlockKSmem == 32,
141	        Layout<Shape <_16, _8>,  // Thread layout, 8 threads per row
142	               Stride< _8, _1>>,
143	        Layout<Shape <_8, _16>,  // Thread layout, 16 threads per row
144	               Stride< _16, _1>>
145	    >;
146	    using GmemTiledCopyOaccum = decltype(
147	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
148	                        GmemLayoutAtomOaccum{},
149	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
150	    using GmemLayoutAtomRotcossin = GmemLayoutAtom;
151	    using GmemTiledCopyRotcossin = decltype(
152	        make_tiled_copy(Copy_Atom<UniversalCopy<uint64_t>, Element>{},
153	                        GmemLayoutAtomRotcossin{},
154	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per load
155	    using GmemTiledCopyRotcossinCont = decltype(
156	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
157	                        GmemLayoutAtomRotcossin{},
158	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per load
159	};
160	
161	// Is_V_in_regs is an option to reduce smem usage, but will increase register pressue.
162	// No_double_buffer is another option to reduce smem usage, but will slow things down.
163	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_,
164	         int AtomLayoutMSdP_=1, int AtomLayoutNdKV=2, int AtomLayoutMdQ=2,
165	         bool Is_V_in_regs_=false, bool No_double_buffer_=false, typename elem_type=cutlass::half_t,
166	         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
167	struct Flash_bwd_kernel_traits : public Base {
168	    using Element = typename Base::Element;
169	    using ElementAccum = typename Base::ElementAccum;
170	    using index_t = typename Base::index_t;
171	    static constexpr bool Has_cp_async = Base::Has_cp_async;
172	    using SmemCopyAtom = typename Base::SmemCopyAtom;
173	    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;
174	
175	    static constexpr bool Is_V_in_regs = Is_V_in_regs_;
176	    static constexpr bool No_double_buffer = No_double_buffer_;
177	
178	    // The number of threads.
179	    static constexpr int kNWarps = kNWarps_;
180	    static constexpr int kNThreads = kNWarps * 32;
181	
182	    static constexpr int kBlockM = kBlockM_;
183	    static constexpr int kBlockN = kBlockN_;
184	    static constexpr int kHeadDim = kHeadDim_;
185	    static_assert(kHeadDim % 32 == 0);
186	    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
187	    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
188	    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;
189	
190	    static constexpr int AtomLayoutMSdP = AtomLayoutMSdP_;
191	    static_assert(kNWarps % AtomLayoutMSdP == 0);
192	    static_assert(kNWarps % AtomLayoutNdKV == 0);
193	    static_assert(kNWarps % AtomLayoutMdQ == 0);
194	
195	    using TiledMmaSdP = TiledMMA<
196	        typename Base::MMA_Atom_Arch,
197	        Layout<Shape<Int<AtomLayoutMSdP>, Int<kNWarps / AtomLayoutMSdP>, _1>>,
198	        Tile<Int<16 * AtomLayoutMSdP>, Int<16 * kNWarps / AtomLayoutMSdP>, _16>>;
199	
200	    using TiledMmadKV = TiledMMA<
201	        typename Base::MMA_Atom_Arch,
202	        Layout<Shape<Int<AtomLayoutNdKV>, Int<kNWarps / AtomLayoutNdKV>, _1>>,
203	        Tile<Int<16 * AtomLayoutNdKV>, Int<16 * kNWarps / AtomLayoutNdKV>, _16>>;
204	
205	    using TiledMmadQ = TiledMMA<
206	        typename Base::MMA_Atom_Arch,
207	        Layout<Shape<Int<AtomLayoutMdQ>, Int<kNWarps / AtomLayoutMdQ>, _1>>,  // 2x4x1 or 4x2x1 thread group
208	        Tile<Int<16 * AtomLayoutMdQ>, Int<16 * kNWarps / AtomLayoutMdQ>, _16>>;
209	
210	    using SmemLayoutAtomQdO = decltype(
211	        composition(Swizzle<kSwizzle, 3, 3>{},
212	                    Layout<Shape<_8, Int<kBlockKSmem>>,
213	                           Stride<Int<kBlockKSmem>, _1>>{}));
214	    using SmemLayoutQdO = decltype(tile_to_shape(
215	        SmemLayoutAtomQdO{},
216	        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
217	
218	    using SmemLayoutAtomKV = decltype(
219	        composition(Swizzle<kSwizzle, 3, 3>{},
220	                    Layout<Shape<Int<kBlockM / kNWarps>, Int<kBlockKSmem>>,
221	                           Stride<Int<kBlockKSmem>, _1>>{}));
222	    using SmemLayoutKV = decltype(tile_to_shape(
223	        // SmemLayoutAtomQdO{},
224	        SmemLayoutAtomKV{},
225	        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
226	
227	    using SmemLayoutKtransposed = decltype(
228	        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
229	    using SmemLayoutKtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutKtransposed{}));
230	
231	    // TODO: generalize to other values of kBlockN
232	    // TODO: what should be the Swizzle here? 3 is faster than 1, and 1 is faster than 2
233	    // static constexpr int kPBlockN = kBlockN;
234	    // Temporarily disabling this for hdim 256 on sm86 and sm89
235	    // static_assert(kBlockN >= 64);
236	    static_assert(kBlockN >= 32);
237	    // TD [2023-03-19]: Idk why kPBlockN = 16 and kSwizzlePdS=3 is the fastest.
238	    static constexpr int kPBlockN = kBlockN >= 64 ? 64 : 32;
239	    static_assert(kPBlockN == 16 || kPBlockN == 32 || kPBlockN == 64);
240	    // static constexpr int kSwizzlePdS = kPBlockN == 16 ? 1 : (kPBlockN == 32 ? 2 : 3);
241	    static constexpr int kSwizzlePdS = 3;
242	    using SmemLayoutAtomPdS = decltype(
243	        composition(Swizzle<kSwizzlePdS, 3, 3>{},
244	                    Layout<Shape<Int<kBlockM>, Int<kPBlockN>>,
245	                           Stride<Int<kPBlockN>, _1>>{}));
246	    using SmemLayoutPdS = decltype(tile_to_shape(
247	        SmemLayoutAtomPdS{},
248	        make_shape(Int<kBlockM>{}, Int<kBlockN>{})));
249	    using SmemLayoutPdStransposed = decltype(
250	        composition(SmemLayoutPdS{}, make_layout(Shape<Int<kBlockN>, Int<kBlockM>>{}, GenRowMajor{})));
251	    using SmemLayoutPdStransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutPdStransposed{}));
252	
253	    using SmemCopyAtomPdS = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
254	
255	    using SmemLayoutQdOtransposed = decltype(
256	        composition(SmemLayoutQdO{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockM>>{}, GenRowMajor{})));
257	    using SmemLayoutQdOtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutQdOtransposed{}));
258	
259	    using SmemLayoutAtomdKV = decltype(
260	        composition(Swizzle<kSwizzle, 3, 3>{},
261	                    Layout<Shape<_8, Int<kBlockKSmem>>,
262	                           Stride<Int<kBlockKSmem>, _1>>{}));
263	    using SmemLayoutdKV = decltype(tile_to_shape(
264	        SmemLayoutAtomdKV{},
265	        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
266	    using SmemCopyAtomdKV = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
267	
268	    using SmemLayoutAtomdQ = decltype(
269	        composition(Swizzle<kSwizzle, 3, 3>{},
270	                    Layout<Shape<_8, Int<kBlockKSmem>>,
271	                           Stride<Int<kBlockKSmem>, _1>>{}));
272	    using SmemLayoutdQ = decltype(tile_to_shape(
273	        SmemLayoutAtomdQ{},
274	        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
275	    using SmemCopyAtomdQ = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
276	
277	    // Double buffer for sQ
278	    static constexpr int kSmemQdOSize = size(SmemLayoutQdO{}) * (No_double_buffer ? 2 : 3) * sizeof(Element);
279	    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
280	    static constexpr int kSmemdSSize = size(SmemLayoutPdS{}) * sizeof(Element);
281	    static constexpr int kSmemPSize = size(SmemLayoutPdS{}) * sizeof(Element);
282	    static constexpr int kSmemdQSize = size(SmemLayoutdQ{}) * sizeof(Element);
283	    static constexpr int kSmemSize = kSmemQdOSize
284	        + (!Is_V_in_regs
285	           ? kSmemKVSize + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)
286	           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)));
287	    static constexpr int kSmemSize1colblock = kSmemQdOSize
288	        + (!Is_V_in_regs
289	           ? kSmemKVSize + kSmemdSSize + kSmemPSize
290	           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + kSmemPSize));
291	
292	    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
293	    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
294	    // Using kBlockKSmem instead of kHeadDim here to avoid bank conflicts, but doesn't seem
295	    // to affect speed in practice.
296	    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
297	    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
298	    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
299	                                  Stride<Int<kGmemThreadsPerRow>, _1>>;
300	
301	    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
302	    // from the same address by the same threadblock. This is slightly faster.
303	    using Gmem_copy_struct = std::conditional_t<
304	        Has_cp_async,
305	        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
306	        AutoVectorizingCopyWithAssumedAlignment<128>
307	    >;
308	    using GmemTiledCopyQKV = decltype(
309	        make_tiled_copy(Copy_Atom<Gmem_copy_struct, elem_type>{},
310	                        GmemLayoutAtom{},
311	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
312	    using GmemTiledCopydO = decltype(
313	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
314	                        GmemLayoutAtom{},
315	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
316	    using GmemTiledCopydKV = decltype(
317	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
318	                        GmemLayoutAtom{},
319	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
320	    using GmemTiledCopydQ = decltype(
321	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
322	                        GmemLayoutAtom{},
323	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
324	    // using GmemLayoutAtomdQaccum = std::conditional_t<
325	    //     kBlockKSmem == 32,
326	    //     Layout<Shape <_32, _8>,  // Thread layout, 8 threads per row
327	    //            Stride< _8, _1>>,
328	    //     Layout<Shape <_16, _16>,  // Thread layout, 16 threads per row
329	    //            Stride< _16, _1>>
330	    // >;
331	    using GmemLayoutAtomdQaccum = Layout<Shape<_16, _8>, Stride<_8, _1>>;
332	    using GmemTiledCopydQaccum = decltype(
333	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
334	                        GmemLayoutAtomdQaccum{},
335	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
336	
337	    using GmemTiledCopydQaccumAtomicAdd = decltype(
338	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
339	                        Layout<Shape <_8, _16>,  // Thread layout, 8 threads per row
340	                               Stride<_16, _1>>{},
341	                        Layout<Shape < _1, _1>>{}));  // Val layout, 1 val per store
342	
343	};
344	
345	////////////////////////////////////////////////////////////////////////////////////////////////////
346
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/block_info.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	namespace flash {
8	
9	////////////////////////////////////////////////////////////////////////////////////////////////////
10	
11	template<bool Varlen=true>
12	struct BlockInfo {
13	
14	    template<typename Params>
15	    __device__ BlockInfo(const Params &params, const int bidb)
16	        : sum_s_q(!Varlen || params.cu_seqlens_q == nullptr ? -1 : params.cu_seqlens_q[bidb])
17	        , sum_s_k(!Varlen || params.cu_seqlens_k == nullptr || !params.is_seqlens_k_cumulative ? -1 : params.cu_seqlens_k[bidb])
18	        , sum_s_v(!Varlen || params.cu_seqlens_v == nullptr || !params.is_seqlens_v_cumulative ? -1 : params.cu_seqlens_v[bidb])
19	        , actual_seqlen_q(!Varlen || params.cu_seqlens_q == nullptr ? params.seqlen_q : params.cu_seqlens_q[bidb + 1] - sum_s_q)
20	        // If is_seqlens_k_cumulative, then seqlen_k is cu_seqlens_k[bidb + 1] - cu_seqlens_k[bidb].
21	        // Otherwise it's cu_seqlens_k[bidb], i.e., we use cu_seqlens_k to store the sequence lengths of K.
22	        , leftpad_k(params.leftpad_k == nullptr ? 0 : params.leftpad_k[bidb])
23	        , seqlen_k_cache((!Varlen || params.cu_seqlens_k == nullptr ? params.seqlen_k : (params.is_seqlens_k_cumulative ? params.cu_seqlens_k[bidb + 1] - sum_s_k : params.cu_seqlens_k[bidb])) - leftpad_k)
24	        , actual_seqlen_k(params.seqused_k ? params.seqused_k[bidb] - leftpad_k : seqlen_k_cache + (params.knew_ptr == nullptr ? 0 : params.seqlen_knew))
25	        // If is_seqlens_v_cumulative, then seqlen_v is cu_seqlens_v[bidb + 1] - cu_seqlens_v[bidb].
26	        // Otherwise it's cu_seqlens_v[bidb], i.e., we use cu_seqlens_v to store the sequence lengths of V.
27	        , leftpad_v(params.leftpad_v == nullptr ? 0 : params.leftpad_v[bidb])
28	        , seqlen_v_cache((!Varlen || params.cu_seqlens_v == nullptr ? params.seqlen_v : (params.is_seqlens_v_cumulative ? params.cu_seqlens_v[bidb + 1] - sum_s_v : params.cu_seqlens_v[bidb])) - leftpad_v)
29	        , actual_seqlen_c(params.seqused_v ? params.seqused_v[bidb] - leftpad_v : seqlen_v_cache + (params.vnew_ptr == nullptr ? 0 : params.seqlen_vnew))
30	        {
31	        }
32	
33	    template <typename index_t>
34	    __forceinline__ __device__ index_t q_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
35	        return sum_s_q == -1 ? bidb * batch_stride : uint32_t(sum_s_q) * row_stride;
36	    }
37	
38	    template <typename index_t>
39	    __forceinline__ __device__ index_t k_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
40	        return sum_s_k == -1 ? bidb * batch_stride + leftpad_k * row_stride : uint32_t(sum_s_k + leftpad_k) * row_stride;
41	    }
42	
43	    template <typename index_t>
44	    __forceinline__ __device__ index_t v_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
45	        return sum_s_v == -1 ? bidb * batch_stride + leftpad_v * row_stride : uint32_t(sum_s_v + leftpad_v) * row_stride;
46	    }
47	
48	
49	    template <typename index_t>
50	    inline __device__ index_t blockmask_q_offset(const index_t m_block_dim, const int bidb) const {
51	        return sum_s_q == -1 ? bidb * (actual_seqlen_q / m_block_dim) : uint32_t(sum_s_q) / m_block_dim;
52	    }
53	
54	    const int sum_s_q;
55	    const int sum_s_k;
56	    const int sum_s_v;
57	    const int actual_seqlen_q;
58	    // We have to have seqlen_k_cache declared before actual_seqlen_k, otherwise actual_seqlen_k is set to 0.
59	    const int leftpad_k;
60	    const int seqlen_k_cache;
61	    const int actual_seqlen_k;
62	    // We have to have seqlen_v_cache declared before actual_seqlen_c, otherwise actual_seqlen_c is set to 0.
63	    const int leftpad_v;
64	    const int seqlen_v_cache;
65	    const int actual_seqlen_c;
66	};
67	
68	////////////////////////////////////////////////////////////////////////////////////////////////////
69	
70	}  // namespace flash
71
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/utils.h",
  "limit": 100,
  "offset": 1
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include <assert.h>
8	#include <stdint.h>
9	#include <stdlib.h>
10	
11	#include <cuda_fp16.h>
12	
13	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
14	#include <cuda_bf16.h>
15	#endif
16	
17	#include <cute/tensor.hpp>
18	
19	#include <cutlass/array.h>
20	#include <cutlass/cutlass.h>
21	#include <cutlass/numeric_conversion.h>
22	#include <cutlass/numeric_types.h>
23	
24	////////////////////////////////////////////////////////////////////////////////////////////////////
25	
26	namespace flash {
27	
28	////////////////////////////////////////////////////////////////////////////////////////////////////
29	
30	template<typename T>
31	__forceinline__ __device__ uint32_t relu2(const uint32_t x);
32	
33	template<>
34	__forceinline__ __device__ uint32_t relu2<cutlass::half_t>(const uint32_t x) {
35	    uint32_t res;
36	    const uint32_t zero = 0u;
37	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
38	    asm volatile("max.f16x2 %0, %1, %2;\n" : "=r"(res) : "r"(x), "r"(zero));
39	#else
40	    asm volatile( \
41	        "{\n" \
42	        "\t .reg .f16x2 sela;\n" \
43	        "\t set.gtu.u32.f16x2 sela, %1, %2;\n" \
44	        "\t and.b32 %0, sela, %1;\n" 
45	        "}\n" : "=r"(res) : "r"(x), "r"(zero));
46	#endif
47	    return res;
48	}
49	
50	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
51	template<>
52	__forceinline__ __device__ uint32_t relu2<cutlass::bfloat16_t>(const uint32_t x) {
53	    uint32_t res;
54	    const uint32_t zero = 0u;
55	    asm volatile("max.bf16x2 %0, %1, %2;\n" : "=r"(res) : "r"(x), "r"(zero));
56	    return res;
57	}
58	#endif
59	
60	////////////////////////////////////////////////////////////////////////////////////////////////////
61	
62	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
63	
64	template<typename T>
65	__forceinline__ __device__ uint32_t convert_relu2(const float2 x);
66	
67	template<>
68	__forceinline__ __device__ uint32_t convert_relu2<cutlass::half_t>(const float2 x) {
69	    uint32_t res;
70	    const uint32_t a = reinterpret_cast<const uint32_t&>(x.x);
71	    const uint32_t b = reinterpret_cast<const uint32_t&>(x.y);
72	    asm volatile("cvt.rn.relu.f16x2.f32 %0, %1, %2;\n" : "=r"(res) : "r"(b), "r"(a));
73	    return res;
74	}
75	
76	template<>
77	__forceinline__ __device__ uint32_t convert_relu2<cutlass::bfloat16_t>(const float2 x) {
78	    uint32_t res;
79	    const uint32_t a = reinterpret_cast<const uint32_t&>(x.x);
80	    const uint32_t b = reinterpret_cast<const uint32_t&>(x.y);
81	    asm volatile("cvt.rn.relu.bf16x2.f32 %0, %1, %2;\n" : "=r"(res) : "r"(b), "r"(a));
82	    return res;
83	}
84	
85	#endif
86	
87	////////////////////////////////////////////////////////////////////////////////////////////////////
88	
89	template<typename T>
90	struct MaxOp {
91	__device__ __forceinline__ T operator()(T const & x, T const & y) { return x > y ? x : y; }
92	};
93	
94	template <>
95	struct MaxOp<float> {
96	// This is slightly faster
97	__device__ __forceinline__ float operator()(float const &x, float const &y) { return max(x, y); }
98	};
99	
100	////////////////////////////////////////////////////////////////////////////////////////////////////
```

> AGENT

现在让我搜索 flash 前向传播内核中的关键模式，特别是 `blockmask` 的遍历和 MMA 操作。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"blockmask\\|fwdIterator\\|bwdIterator\\|max_no_larger\\|compute_attn_splitkv_stage1\\|compute_attn_splitkv\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h | head -60",
  "description": "Find blockmask iterator usage in flash_fwd_kernel.h"
}
```

> TOOL

tool_result Bash
```
22:#include "flash_blockmask.h"
376:    // Initialize blockmask iterator if blockmask is enabled
377:    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
378:    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
425:            next_block_idx = blockmask.max_no_larger(n_block-1);
484:        next_block_idx = blockmask.max_no_larger(n_block - 1);
949:    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
950:    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
1006:            next_block_idx = blockmask.max_no_larger(n_block-1);
1062:        next_block_idx = blockmask.max_no_larger(n_block - 1);
1440:    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max_c);
1441:    int next_block_idx = blockmask.max_no_larger(n_block_max_c-1);
1477:            next_block_idx = blockmask.max_no_larger(n_block-1);
1530:        next_block_idx = blockmask.max_no_larger(n_block - 1);
1590:    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
1592:    next_block_idx = blockmask.max_no_larger(n_block_max-1);
1625:            next_block_idx = blockmask.max_no_larger(n_block-1);
1687:        next_block_idx = blockmask.max_no_larger(n_block - 1);
1769:inline __device__ void compute_attn_splitkv(const Params &params) {
1781:inline __device__ void compute_attn_splitkv_stage1(const Params &params) {
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"SM80\\|SM90\\|SM120\\|cp_async\\|TMA\\|warp_group\\|wg_mma\\|cp.async.bulk\\|wgmma\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h 2>/dev/null | head -30",
  "description": "Search for arch-specific MMA and async copy usage"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:20:    static constexpr bool Has_cp_async = true;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:23:    static constexpr bool Has_cp_async = false;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:32:        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:33:        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:55:    static constexpr bool Has_cp_async = Base::Has_cp_async;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:126:        Has_cp_async,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:127:        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:171:    static constexpr bool Has_cp_async = Base::Has_cp_async;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:304:        Has_cp_async,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:305:        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:338:    if (Kernel_traits::Is_Q_in_regs) { cute::cp_async_fence(); }
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:345:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:357:    cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:362:        flash::cp_async_wait<1>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:397:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:409:        cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:430:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:437:            // This cp_async_fence needs to be in the if block, otherwise the synchronization
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:439:            cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:488:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:491:        cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:500:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:506:            // This cp_async_fence needs to be in the if block, otherwise the synchronization
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:508:            cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:935:    cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:937:    // flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:969:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:990:        cute::cp_async_fence();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:1011:        flash::cp_async_wait<0>();
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:1030:            // This cp_async_fence needs to be in the if block, otherwise the synchronization
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"torch.cuda.synchronize\\|\\.item()\\|\\.cpu()\\|\\.numpy()\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/",
  "description": "Search for host-device synchronization points in Python"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/blockmask_to_uint64.py:25:    flat_dims = torch.prod(torch.tensor(original_shape[:-1], dtype=torch.int64)).item()
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/uint64_to_bool.py:21:    flat_dims = torch.prod(torch.tensor(original_shape[:-1], dtype=torch.int64)).item()
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py:109:    # assert cu_seqlens_q[-1].item() == total_q, f"total_q mismatch: {cu_seqlens_q[-1].item()} vs {total_q}"
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py:113:    # max_cache_len = cache_lens.max().item()
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py:212:    assert cu_seqlens_q[-1].item() == total_q, f"total_q mismatch: {cu_seqlens_q[-1].item()} vs {total_q}"
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/max_pooling_1d.py:216:    # max_cache_len = cache_lens.max().item()
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:348:            torch.cuda.synchronize()
```

> AGENT

让我更仔细地检查反向传播的 blockmask 转换以及 `cu_seqlens` 扩展循环。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py",
  "limit": 80,
  "offset": 339
}
```

> TOOL

tool_result Read
```
339	    def backward(ctx, dout, *args):
340	        q, k, v, out, softmax_lse, cu_seqlens_q, cu_seqlens_k, fwd_blockmask_uint64, rng_state = ctx.saved_tensors
341	        dq, dk, dv = torch.empty_like(q), torch.empty_like(k), torch.empty_like(v)
342	        bwd_blockmask_uint64 = None
343	        if fwd_blockmask_uint64 is not None:
344	            fwd_blockmask_bool = cuda_uint64_to_bool(fwd_blockmask_uint64, (ctx.max_seqlen_k + 64- 1) // 64) 
345	            # Ensure the tensor is contiguous in memory after transpose
346	            transposed_blockmask = fwd_blockmask_bool.transpose(1, 2).contiguous()
347	            # Synchronize CUDA stream before conversion
348	            torch.cuda.synchronize()
349	            # Convert to uint64
350	            bwd_blockmask_uint64, _ = cuda_blockmask_to_uint64(transposed_blockmask)
351	        
352	        head_size_og = dout.size(2)
353	        dout_padded = dout
354	        if head_size_og % 8 != 0:
355	            dout_padded = torch.nn.functional.pad(dout, [0, 8 - head_size_og % 8])
356	        _wrapped_infllmv2_attn_varlen_backward(
357	            dout_padded,
358	            q,
359	            k,
360	            v,
361	            out,
362	            softmax_lse,
363	            dq,
364	            dk,
365	            dv,
366	            cu_seqlens_q,
367	            cu_seqlens_k,
368	            ctx.max_seqlen_q,
369	            ctx.max_seqlen_k,
370	            ctx.dropout_p,
371	            ctx.softmax_scale,
372	            ctx.causal,
373	            ctx.window_size[0],
374	            ctx.window_size[1],
375	            ctx.softcap,
376	            ctx.alibi_slopes,
377	            ctx.deterministic,
378	            bwd_blockmask_uint64,  # Use the uint64 matrix directly
379	            rng_state=rng_state,
380	        )
381	        dq = dq[..., : dout.shape[-1]]  # We could have padded the head dimension
382	        dk = dk[..., : dout.shape[-1]]
383	        dv = dv[..., : dout.shape[-1]]
384	
385	        return dq, dk, dv, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
386	
387	
388	def infllmv2_attn_varlen_func(
389	    q,
390	    k,
391	    v,
392	    cu_seqlens_q,
393	    cu_seqlens_k,
394	    max_seqlen_q,
395	    max_seqlen_k,
396	    dropout_p=0.0,
397	    softmax_scale=None,
398	    causal=False,
399	    window_size=(-1, -1),  # -1 means infinite context window
400	    softcap=0.0, # 0.0 means deactivated
401	    alibi_slopes=None,
402	    deterministic=False,
403	    return_attn_probs=False,
404	    block_table=None,
405	    topk_idx=None,
406	):
407	    """dropout_p should be set to 0.0 during evaluation
408	    Supports multi-query and grouped-query attention (MQA/GQA) by passing in K, V with fewer heads
409	    than Q. Note that the number of heads in Q must be divisible by the number of heads in KV.
410	    For example, if Q has 6 heads and K, V have 2 heads, head 0, 1, 2 of Q will attention to head
411	    0 of K, V, and head 3, 4, 5 of Q will attention to head 1 of K, V.
412	
413	    If causal=True, the causal mask is aligned to the bottom right corner of the attention matrix.
414	    For example, if seqlen_q = 2 and seqlen_k = 5, the causal mask (1 = keep, 0 = masked out) is:
415	        1 1 1 1 0
416	        1 1 1 1 1
417	    If seqlen_q = 5 and seqlen_k = 2, the causal mask is:
418	        0 0
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"empty_cache\\|contiguous\\|reshape\\|permute\\|transpose\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py",
  "description": "Find memory and tensor operation patterns"
}
```

> TOOL

tool_result Bash
```
17:def maybe_contiguous(x):
18:    return x.contiguous() if x is not None and x.stride(-1) != 1 else x
71:    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
82:            # Direct reshape for MQA - no transpose needed
83:            q = q.reshape(-1, 1, head_dim).contiguous()
88:            q = q.reshape(-1, nheads_k, group_size, head_dim).transpose(1, 2).reshape(-1, nheads_k, head_dim).contiguous()
126:            # Direct reshape for MQA - no transpose needed
127:            out = out.reshape(-1, nheads_q, head_dim).contiguous()
130:            out = out.reshape(-1, group_size, nheads_k, head_dim).transpose(1, 2).reshape(-1, nheads_q, head_dim).contiguous()
165:    # dq, dk, dv are allocated by us so they should already be contiguous
166:    dout, q, k, v, out = [maybe_contiguous(x) for x in (dout, q, k, v, out)]
175:        # Direct reshape for MQA - no transpose needed
176:        q_final = q.reshape(total_q * nheads_q, 1, dim).contiguous()
177:        dout_final = dout.reshape(total_q * nheads_q, 1, dim).contiguous()
178:        out_final = out.reshape(total_q * nheads_q, 1, dim).contiguous()
181:        q_final = q.reshape(total_q, nheads_k, group_size, dim)
182:        q_final = q_final.permute(0, 2, 1, 3)
183:        q_final = q_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
185:        dout_final = dout.reshape(total_q, nheads_k, group_size, dim)
186:        dout_final = dout_final.permute(0, 2, 1, 3)
187:        dout_final = dout_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
189:        out_final = out.reshape(total_q, nheads_k, group_size, dim)
190:        out_final = out_final.permute(0, 2, 1, 3)
191:        out_final = out_final.reshape(total_q * group_size, nheads_k, dim).contiguous()
192:    # q = q.reshape(-1, 16, 2, head_dim).reshape(-1, 2, head_dim)
246:    torch.cuda.empty_cache()
250:        # Direct reshape for MQA - no transpose needed
251:        dq_temp = dq_temp.reshape(total_q, nheads_q, dim)
254:        dq_temp = dq_temp.reshape(total_q, group_size, nheads_k, dim)
255:        dq_temp = dq_temp.permute(0, 2, 1, 3)
256:        dq_temp = dq_temp.reshape(total_q, nheads_q, dim)
263:    torch.cuda.empty_cache()
345:            # Ensure the tensor is contiguous in memory after transpose
346:            transposed_blockmask = fwd_blockmask_bool.transpose(1, 2).contiguous()
350:            bwd_blockmask_uint64, _ = cuda_blockmask_to_uint64(transposed_blockmask)
548:    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
559:    q = q.reshape(total_q, nheads_k, nheads_per_group, head_dim)
560:    q = q.transpose(1, 2).reshape(total_q * nheads_per_group, nheads_k, head_dim).contiguous()
562:    # Adjust cu_seqlens and max_seqlen for the reshaped query
723:    assert k_cache.stride(-1) == 1, "k_cache must have contiguous last dimension"
724:    assert v_cache.stride(-1) == 1, "v_cache must have contiguous last dimension"
725:    q, k, v = [maybe_contiguous(x) for x in (q, k, v)]
732:        cache_seqlens = maybe_contiguous(cache_seqlens)
733:    cache_batch_idx = maybe_contiguous(cache_batch_idx)
734:    block_table = maybe_contiguous(block_table)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"num_k_heads\\|m_block_dim\\|n_block_dim\\|num_blocks_m\\|num_blocks_n\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "description": "Find blockmask dimension parameters"
}
```

> TOOL

tool_result Bash
```
706:        params.m_block_dim = 16;
707:        params.n_block_dim = 64;
708:        params.num_k_heads = 2;
709:        params.num_blocks_m = (total_q + 16 - 1) / 16;
710:        params.num_blocks_n = (max_seqlen_k + 64 - 1) / 64;
713:        params.m_block_dim = 1;
714:        params.n_block_dim = 1;
988:    params.m_block_dim = 16;
989:    params.n_block_dim = 1;
1501:        params.m_block_dim = 16;
1502:        params.n_block_dim = 64;
1503:        params.num_blocks_m = total_q / 16;
1504:        params.num_blocks_n = round_multiple(max_seqlen_k, 64) / 64;
1709:        params.m_block_dim = 16;
1710:        params.n_block_dim = 64;
1711:        params.num_k_heads = 2;
1712:        params.num_blocks_m = (seqlen_q + 16 - 1) / 16;
1713:        params.num_blocks_n = (seqlen_k + 64 - 1) / 64;
1716:        params.m_block_dim = 1;
1717:        params.n_block_dim = 1;
```

> AGENT

现在让我再检查一件事—— `max_pooling_1d_varlen_kernel` 中线性搜索批次以及 `topk` kernel 配置。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"for.*batch\\|binary_search\\|linear search\\|cu_seqlens\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh",
  "description": "Check the batch search pattern in max_pooling"
}
```

> TOOL

tool_result Bash
```
15:    const int* cu_seqlens_q,  // cumulative sequence lengths for queries
16:    const int* cu_seqlens_k,  // cumulative sequence lengths for keys
17:    const int* cache_lens,    // cache lengths for each batch [batch_size]
44:    for (int b = 0; b < batch_size; b++) {
45:        q_start = cu_seqlens_q[b];
46:        q_end = cu_seqlens_q[b + 1];
47:        k_start = cu_seqlens_k[b];
48:        k_end = cu_seqlens_k[b + 1];
67:    size_t total_q_all = cu_seqlens_q[batch_size]; 
74:    int cache_len = cache_lens[batch_idx];  // Get cache_len for this batch
92:            end = min(end, seqlen_k);  // Use actual sequence length for this batch
172:    const int* cu_seqlens_q,
173:    const int* cu_seqlens_k,
192:    // cudaMemcpyAsync(&total_q, &cu_seqlens_q[batch_size], sizeof(int), 
200:        input, output, cu_seqlens_q, cu_seqlens_k, cache_lens, batch_size, num_heads,
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"dim3\\|blockDim\\|gridDim\\|threads_per_block\\|block_size\\|kNThreads\\|kNWarps\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/get_probs.cuh /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh",
  "description": "Check grid/block configurations across all kernels"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:18:    int row = blockIdx.x * blockDim.x + threadIdx.x;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:57:    const int threads_per_block = 256;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:58:    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:60:    dim3 grid(blocks_per_row, last_dim_size);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:61:    dim3 block(threads_per_block, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:18:    int row = blockIdx.x * blockDim.x + threadIdx.x;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:65:    const int threads_per_block = 256;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:66:    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:68:    dim3 grid(blocks_per_row, n_uint64_per_row);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:69:    dim3 block(threads_per_block, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:53:        if (blockDim.x > i) {
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:57:                T nw_v = (idx_next < blockDim.x) ? shared_val[idx_next] : T(-TypeTraits<T>::inf());
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:58:                int nw_pos = (idx_next < blockDim.x) ? shared_pos[idx_next] : -1;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:82:    for (int i = blockDim.x; i < n; i += blockDim.x) {
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:97:// gridDim(batch, n / 1024, 1), threadDim(1024, 1, 1)
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:106:    int offset_col = blockIdx.y * blockDim.x + threadIdx.x;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:108:    int offset_out = blockIdx.x * (gridDim.y * N) + blockIdx.y * N + threadIdx.x;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:154:        dim3 blockDim(n, 1, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:155:        dim3 gridDim(batch, 1, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:156:        kernel_bitonic_topk_multiblock<T, top_size, false><<<gridDim, blockDim, 0, stream>>>(
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:19:    int row = blockIdx.x * blockDim.x + threadIdx.x;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:67:    const int threads_per_block = 256;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:68:    const int blocks_per_row = (batch_size + threads_per_block - 1) / threads_per_block;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:70:    dim3 grid(blocks_per_row, n_uint64_per_row);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:71:    dim3 block(threads_per_block, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:26:    int block_size,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:31:    // Block: (threads_per_block)
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:75:    int off_bq = (bidq_local + cache_len) / block_size;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:77:    for (int k = threadIdx.x; k < out_len; k += blockDim.x) {
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:121:    int block_size,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:131:    int off_bq = (bidq + cache_len) / block_size;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:133:    for (int k = threadIdx.x; k < out_len; k += blockDim.x) {
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:183:    int block_size,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:188:    const int threads_per_block = 256;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:196:    dim3 grid(total_q, num_heads);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:197:    dim3 block(threads_per_block, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:201:        max_seqlen_q, max_seqlen_k, out_len, kernel_size, stride, padding, block_size, local_blocks, init_blocks
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:219:    int block_size,
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:223:    const int threads_per_block = 256;
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:225:    dim3 grid(q_len, num_heads);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:226:    dim3 block(threads_per_block, 1);
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:229:        input, output, num_heads, q_len, k_len, out_len, cache_len, kernel_size, stride, padding, block_size, local_blocks, init_blocks
```

> AGENT

让我检查一下 `num_k_heads` 是如何硬编码的，并验证 topk 内核的块维度问题。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"num_k_heads\\s*=\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "description": "Check hardcoded num_k_heads"
}
```

> TOOL

tool_result Bash
```
708:        params.num_k_heads = 2;
1711:        params.num_k_heads = 2;
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"n_block_dim\\s*=\\|m_block_dim\\s*=\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "description": "Check hardcoded block dimensions"
}
```

> TOOL

tool_result Bash
```
706:        params.m_block_dim = 16;
707:        params.n_block_dim = 64;
713:        params.m_block_dim = 1;
714:        params.n_block_dim = 1;
988:    params.m_block_dim = 16;
989:    params.n_block_dim = 1;
1501:        params.m_block_dim = 16;
1502:        params.n_block_dim = 64;
1709:        params.m_block_dim = 16;
1710:        params.n_block_dim = 64;
1716:        params.m_block_dim = 1;
1717:        params.n_block_dim = 1;
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 120,
  "offset": 370
}
```

> TOOL

tool_result Read
```
370	
371	    flash::Softmax<2 * size<1>(acc_o)> softmax;
372	
373	    const float alibi_slope = !Has_alibi || params.alibi_slopes_ptr == nullptr ? 0.0f : reinterpret_cast<float *>(params.alibi_slopes_ptr)[bidb * params.alibi_slopes_batch_stride + bidh] / params.scale_softmax;
374	    flash::Mask<Is_causal, Is_local, Has_alibi> mask(binfo.actual_seqlen_k, binfo.actual_seqlen_q, params.window_size_left, params.window_size_right, alibi_slope, params.m_block_dim);
375	
376	    // Initialize blockmask iterator if blockmask is enabled
377	    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
378	    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
379	    int leap = 0;
380	
381	    // For performance reason, we separate out two kinds of iterations:
382	    // those that need masking on S, and those that don't.
383	    // We need masking on S for the very last block when K and V has length not multiple of kBlockN.
384	    // We also need masking on S if it's causal, for the last ceil_div(kBlockM, kBlockN) blocks.
385	    // We will have at least 1 "masking" iteration.
386	
387	    // If not even_N, then seqlen_k might end in the middle of a block. In that case we need to
388	    // mask 2 blocks (e.g. when kBlockM == kBlockN), not just 1.
389	    constexpr int n_masking_steps = (!Is_causal && !Is_local)
390	        ? 1
391	        : ((Is_even_MN && Is_causal) ? cute::ceil_div(kBlockM, kBlockN) : cute::ceil_div(kBlockM, kBlockN) + 1);
392	    #pragma unroll
393	    for (int masking_step = 0; masking_step < n_masking_steps; ++masking_step, --n_block) {
394	        const bool skip = (n_block != next_block_idx);
395	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
396	        clear(acc_s);
397	        flash::cp_async_wait<0>();
398	        __syncthreads();
399	
400	        // Advance gV
401	        if (masking_step > 0) {
402	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV(_, _, _, n_block), tVsV, tKVcKV, tKVpKV);
403	        } else {
404	            // Clear the smem tiles to account for predicated off loads
405	            flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/true>(
406	                gmem_tiled_copy_QKV, tVgV(_, _, _, n_block), tVsV, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN
407	            );
408	        }
409	        cute::cp_async_fence();
410	
411	        if (!skip) {
412	            flash::gemm</*A_in_regs=*/Kernel_traits::Is_Q_in_regs>(
413	                acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
414	                smem_thr_copy_Q, smem_thr_copy_K
415	            );
416	            // if (cute::thread0()) { print(acc_s); }
417	            if constexpr (Is_softcap){
418	                flash::apply_softcap(acc_s, params.softcap);
419	            }
420	
421	            mask.template apply_mask<Is_causal, Is_even_MN>(
422	                acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
423	            );
424	
425	            next_block_idx = blockmask.max_no_larger(n_block-1);
426	        } else {
427	            mask.all_mask(acc_s);
428	        }
429	
430	        flash::cp_async_wait<0>();
431	        __syncthreads();
432	        
433	        leap = (masking_step + 1 == n_masking_steps) ? n_block - next_block_idx : 1;
434	        
435	        if (n_block > n_block_min && next_block_idx != -1) {
436	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK(_, _, _, n_block - leap), tKsK, tKVcKV, tKVpKV);
437	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
438	            // isn't right and we get race conditions.
439	            cute::cp_async_fence();
440	        }
441	
442	        // TODO: when we have key_padding_mask we'll need to Check_inf
443	        masking_step == 0
444	            ? softmax.template softmax_rescale_o</*Is_first=*/true,  /*Check_inf=*/Is_causal || Is_local>(acc_s, acc_o, params.scale_softmax_log2)
445	            : softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_causal || Is_local>(acc_s, acc_o, params.scale_softmax_log2);
446	
447	        if (!skip) {
448	            // Convert acc_s from fp32 to fp16/bf16
449	            Tensor rP = flash::convert_type<Element>(acc_s);
450	            int block_row_idx = m_block * (kBlockM / 16) + tidx / 32;
451	            int block_col_idx = n_block * (kBlockN / 32);
452	            if (Return_softmax) {
453	                Tensor rP_drop = make_fragment_like(rP);
454	                cute::copy(rP, rP_drop);
455	                dropout.template apply_dropout</*encode_dropout_in_sign_bit=*/true>(
456	                    rP_drop, block_row_idx, block_col_idx, kNWarps
457	                );
458	                cute::copy(rP_drop, tSgS);
459	                tSgS.data() = tSgS.data() + (-kBlockN);
460	            }
461	            if (Is_dropout) {
462	                dropout.apply_dropout(rP, block_row_idx, block_col_idx, kNWarps);
463	            }
464	
465	            // Reshape rP from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
466	            // if using m16n8k16 or (4, MMA_M, MMA_N) if using m16n8k8.
467	            Tensor tOrP = make_tensor(rP.data(), flash::convert_layout_acc_Aregs<Kernel_traits::TiledMma>(rP.layout()));
468	            // if (cute::thread0()) { print(tOrP); }
469	            flash::gemm_rs(acc_o, tOrP, tOrVt, tOsVt, tiled_mma, smem_tiled_copy_V, smem_thr_copy_V);
470	            // if (cute::thread0()) { print(scores); }
471	        }
472	
473	        // This check is at the end of the loop since we always have at least 1 iteration
474	        if (n_masking_steps > 1 && n_block <= n_block_min) {
475	            --n_block;
476	            break;
477	        }
478	    }
479	
480	    leap = n_block - next_block_idx + 1;
481	
482	    // These are the iterations where we don't need masking on S
483	    for (n_block = next_block_idx; n_block != -1 && n_block >= n_block_min; n_block = next_block_idx) {
484	        next_block_idx = blockmask.max_no_larger(n_block - 1);
485	        
486	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
487	        clear(acc_s);
488	        flash::cp_async_wait<0>();
489	        __syncthreads();
```

> AGENT

现在我对整个代码库有了全面的了解。让我再检查一个方面——stage1 内核如何处理 `block_score` 计算。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 80,
  "offset": 1769
}
```

> TOOL

tool_result Read
```
1769	inline __device__ void compute_attn_splitkv(const Params &params) {
1770	    const int m_block = blockIdx.x;
1771	    // The block index for the batch.
1772	    const int bidb = Split ? blockIdx.z / params.h : blockIdx.y;
1773	    // The block index for the head.
1774	    const int bidh = Split ? blockIdx.z - bidb * params.h : blockIdx.z;
1775	    const int n_split_idx = Split ? blockIdx.y : 0;
1776	    const int num_n_splits = Split ? gridDim.y : 1;
1777	    flash::compute_attn_1rowblock_splitkv<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params, bidb, bidh, m_block, n_split_idx, num_n_splits);
1778	}
1779	
1780	template<typename Kernel_traits, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV, typename Params>
1781	inline __device__ void compute_attn_splitkv_stage1(const Params &params) {
1782	    const int m_block = blockIdx.x;
1783	    // The block index for the batch.
1784	    const int bidb = Split ? blockIdx.z / params.h : blockIdx.y;
1785	    // The block index for the head.
1786	    const int bidh = Split ? blockIdx.z - bidb * params.h : blockIdx.z;
1787	    const int n_split_idx = Split ? blockIdx.y : 0;
1788	    const int num_n_splits = Split ? gridDim.y : 1;
1789	    flash::compute_attn_1rowblock_splitkv_stage1<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params, bidb, bidh, m_block, n_split_idx, num_n_splits);
1790	}
1791	
1792	////////////////////////////////////////////////////////////////////////////////////////////////////
1793	
1794	template<typename Kernel_traits, int kBlockM, int Log_max_splits, bool Is_even_K, typename Params>
1795	inline __device__ void combine_attn_seqk_parallel(const Params &params) {
1796	    using Element = typename Kernel_traits::Element;
1797	    using ElementAccum = typename Kernel_traits::ElementAccum;
1798	    using index_t = typename Kernel_traits::index_t;
1799	    constexpr int kMaxSplits = 1 << Log_max_splits;
1800	    constexpr int kHeadDim = Kernel_traits::kHeadDim;
1801	    constexpr int kNThreads = 128;
1802	
1803	    static_assert(kMaxSplits <= 128, "kMaxSplits must be <= 128");
1804	    static_assert(kBlockM == 4 || kBlockM == 8 || kBlockM == 16 || kBlockM == 32, "kBlockM must be 4, 8, 16 or 32");
1805	
1806	    // Shared memory.
1807	    // kBlockM + 1 instead of kBlockM to reduce bank conflicts.
1808	    __shared__ ElementAccum sLSE[kMaxSplits][kBlockM + 1];
1809	
1810	    // The thread and block index.
1811	    const int tidx = threadIdx.x;
1812	    const int bidx = blockIdx.x;
1813	
1814	    const index_t lse_size = params.b * params.h * params.seqlen_q;
1815	
1816	    const index_t row_offset_lse = bidx * kBlockM;
1817	    Tensor gLSEaccum = make_tensor(make_gmem_ptr(reinterpret_cast<ElementAccum *>(params.softmax_lseaccum_ptr) + row_offset_lse),
1818	                                   Shape<Int<kMaxSplits>, Int<kBlockM>>{},
1819	                                   make_stride(lse_size, _1{}));
1820	
1821	    // LSE format is different depending on params.unpadded_lse and params.seqlenq_ngroups_swapped, see comment in get_lse_tile.
1822	    // This tensor's layout maps row_offset_lse to {bidb, bidh, q_offset}.
1823	    Tensor gLSE = make_tensor(make_gmem_ptr(reinterpret_cast<ElementAccum *>(params.softmax_lse_ptr) + row_offset_lse),
1824	                              Shape<Int<kBlockM>>{}, Stride<_1>{});
1825	
1826	    // This layout maps row_offset_lse to {bidh, q_offset, bidb} or {bidh, bidb, q_offset}.
1827	    Layout flat_layout = make_layout(lse_size);
1828	    Layout orig_layout = make_layout(make_shape(params.seqlen_q, params.h, params.b));
1829	    auto transposed_stride = params.seqlenq_ngroups_swapped ? make_stride(params.b, params.seqlen_q * params.b, 1) : make_stride(1, params.seqlen_q * params.b, params.seqlen_q);
1830	    Layout remapped_layout = make_layout(make_shape(params.seqlen_q, params.h, params.b), transposed_stride);
1831	    Layout final_layout = cute::composition(remapped_layout, cute::composition(orig_layout, flat_layout));
1832	
1833	    Tensor gLSE_unpadded = make_tensor(make_gmem_ptr(reinterpret_cast<ElementAccum *>(params.softmax_lse_ptr)), final_layout);
1834	
1835	    constexpr int kNLsePerThread = (kMaxSplits * kBlockM + kNThreads - 1) / kNThreads;
1836	
1837	    // Read the LSE values from gmem and store them in shared memory, then transpose them.
1838	    constexpr int kRowsPerLoadLSE = kNThreads / kBlockM;
1839	    #pragma unroll
1840	    for (int l = 0; l < kNLsePerThread; ++l) {
1841	        const int row = l * kRowsPerLoadLSE + tidx / kBlockM;
1842	        const int col = tidx % kBlockM;
1843	        ElementAccum lse = (row < params.num_splits && col < lse_size - bidx * kBlockM) ? gLSEaccum(row, col) : -INFINITY;
1844	        if (row < kMaxSplits) { sLSE[row][col] = lse; }
1845	        // if (bidx == 0 && tidx < 32) { printf("tidx = %d, row = %d, col = %d, lse = %f\n", tidx, row, col, lse); }
1846	    }
1847	    // if (bidx == 1 && tidx < 32) { printf("tidx = %d, row_offset_lse = %d, lse = %f\n", tidx, row_offset_lse, lse_accum(0)); }
1848	    __syncthreads();
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 120,
  "offset": 920
}
```

> TOOL

tool_result Read
```
920	                tQgQ, tQsQ, tRgCos, tRgSin, tQcQ, binfo.actual_seqlen_q - m_block * kBlockM,
921	                0, params.d, params.rotary_dim
922	            );
923	        } else {
924	            flash::copy_rotary_contiguous<Is_even_K>(
925	                tQgQ, tQsQ, tRgCosCont, tRgSinCont, tQcQ, binfo.actual_seqlen_q - m_block * kBlockM,
926	                0, params.d, params.rotary_dim
927	            );
928	        }
929	    }
930	
931	    int n_block = n_block_max - 1;
932	    // We don't need to clear the sK smem tiles since we'll mask out the scores anyway.
933	    flash::copy<Is_even_MN, Is_even_K>(gmem_tiled_copy_QKV, tKgK, tKsK, tKVcKV, tKVpKV,
934	                                       binfo.actual_seqlen_k - n_block * kBlockN);
935	    cute::cp_async_fence();
936	
937	    // flash::cp_async_wait<0>();
938	    // __syncthreads();
939	    // if (tidx == 0 && blockIdx.y == 0 && blockIdx.z == 0) { print(tKsK); }
940	    // __syncthreads();
941	
942	    clear(acc_o);
943	
944	    flash::Softmax<2 * size<1>(acc_o)> softmax;
945	
946	    const float alibi_slope = !Has_alibi ? 0.0f : reinterpret_cast<float *>(params.alibi_slopes_ptr)[bidb * params.alibi_slopes_batch_stride + bidh] / params.scale_softmax;
947	    flash::Mask<Is_causal, Is_local, Has_alibi> mask(binfo.actual_seqlen_k, binfo.actual_seqlen_q, params.window_size_left, params.window_size_right, alibi_slope, params.m_block_dim);
948	
949	    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
950	    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
951	    int leap = 0;
952	
953	    // For performance reason, we separate out two kinds of iterations:
954	    // those that need masking on S, and those that don't.
955	    // We need masking on S for the very last block when K and V has length not multiple of kBlockN.
956	    // We also need masking on S if it's causal, for the last ceil_div(kBlockM, kBlockN) blocks.
957	    // We will have at least 1 "masking" iteration.
958	
959	    // If not even_N, then seqlen_k might end in the middle of a block. In that case we need to
960	    // mask 2 blocks (e.g. when kBlockM == kBlockN), not just 1.
961	    constexpr int n_masking_steps = (!Is_causal && !Is_local)
962	        ? 1
963	        : ((Is_even_MN && Is_causal) ? cute::ceil_div(kBlockM, kBlockN) : cute::ceil_div(kBlockM, kBlockN) + 1);
964	    #pragma unroll
965	    for (int masking_step = 0; masking_step < n_masking_steps; ++masking_step, --n_block) {
966	        const bool skip = (n_block != next_block_idx);
967	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
968	        clear(acc_s);
969	        flash::cp_async_wait<0>();
970	        __syncthreads();
971	
972	        // Advance gV
973	        if (masking_step > 0) {
974	            if (block_table == nullptr) {
975	                tVgV.data() = tVgV.data() + (-int(kBlockN * params.v_row_stride));
976	            } else {
977	                const int block_table_idx_cur = (n_block + 1) * kBlockN / params.page_block_size;
978	                const int block_table_offset_cur = (n_block + 1) * kBlockN - block_table_idx_cur * params.page_block_size;
979	                const int block_table_idx_next = n_block * kBlockN / params.page_block_size;
980	                const int block_table_offset_next = n_block * kBlockN - block_table_idx_next * params.page_block_size;
981	                tVgV.data() = tVgV.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.v_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.v_row_stride;
982	            }
983	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV, tVsV, tKVcKV, tKVpKV);
984	        } else {
985	            // Clear the smem tiles to account for predicated off loads
986	            flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/true>(
987	                gmem_tiled_copy_QKV, tVgV, tVsV, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN
988	            );
989	        }
990	        cute::cp_async_fence();
991	
992	        if (!skip) {
993	            flash::gemm(
994	                acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
995	                smem_thr_copy_Q, smem_thr_copy_K
996	            );
997	            // if (cute::thread0()) { print(acc_s); }
998	            if constexpr (Is_softcap){
999	                flash::apply_softcap(acc_s, params.softcap);
1000	            }
1001	
1002	            mask.template apply_mask<Is_causal, Is_even_MN>(
1003	                acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
1004	            );
1005	
1006	            next_block_idx = blockmask.max_no_larger(n_block-1);
1007	        } else {
1008	            mask.all_mask(acc_s);
1009	        }
1010	
1011	        flash::cp_async_wait<0>();
1012	        __syncthreads();
1013	        // if (tidx == 0 && blockIdx.y == 0 && blockIdx.z == 0) { print(tVsV); }
1014	        // __syncthreads();
1015	
1016	        leap = (masking_step + 1 == n_masking_steps) ? n_block - next_block_idx : 1;
1017	
1018	        if (n_block > n_block_min && next_block_idx != -1) {
1019	            // Advance gK
1020	            if (block_table == nullptr) {
1021	                tKgK.data() = tKgK.data() + (-int(kBlockN * leap * params.k_row_stride));
1022	            } else {
1023	                const int block_table_idx_cur = n_block * kBlockN / params.page_block_size;
1024	                const int block_table_offset_cur = n_block * kBlockN - block_table_idx_cur * params.page_block_size;
1025	                const int block_table_idx_next = (n_block - leap) * kBlockN / params.page_block_size;
1026	                const int block_table_offset_next =(n_block - leap) * kBlockN - block_table_idx_next * params.page_block_size;
1027	                tKgK.data() = tKgK.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.k_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.k_row_stride;
1028	            }
1029	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK, tKsK, tKVcKV, tKVpKV);
1030	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
1031	            // isn't right and we get race conditions.
1032	            cute::cp_async_fence();
1033	        }
1034	
1035	        // We have key_padding_mask so we'll need to Check_inf
1036	        masking_step == 0
1037	            ? softmax.template softmax_rescale_o</*Is_first=*/true,  /*Check_inf=*/Is_causal || Is_local || !Is_even_MN>(acc_s, acc_o, params.scale_softmax_log2)
1038	            : softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_causal || Is_local || !Is_even_MN>(acc_s, acc_o, params.scale_softmax_log2);
1039	        // if (cute::thread0()) { print(scores_max); print(scores_sum); print(scores); }
```

> AGENT

我现在对代码库有了全面的了解。下面我将整理详细的分析报告。

---

## 目录结构概览

```
infllmv2_cuda_impl/
  csrc/
    entry.cu                       -- pybind11 入口，所有 kernel 的 C++ 绑定
    get_probs.cuh                  -- softmax 概率恢复 kernel
    topk.cuh                       -- bitonic top-k kernel
    max_pooling_1d.cuh             -- max pooling 1D（含 varlen 版本）
    blockmask_to_uint64.cuh        -- bool mask -> uint64 打包
    topk_to_uint64.cuh             -- top-k index -> uint64 打包
    uint64_to_bool.cuh             -- uint64 -> bool 解包
    trait.cuh                      -- half/bf16 类型 trait
    utils.cuh                      -- 宏定义和 CUDA 检查
    flash_attn/
      flash_api.cpp                -- FlashAttention C++ 入口（varlen_fwd, varlen_fwd_stage1, varlen_bwd, fwd_kvcache）
      src/
        flash.h                    -- 参数结构体（Flash_fwd_params / Flash_bwd_params）
        flash_fwd_kernel.h         -- forward kernel 实现（compute_attn_1rowblock, splitkv, stage1）
        flash_fwd_launch_template.h-- kernel launch 模板和 hdim dispatch
        flash_blockmask.h          -- fwdIterator / bwdIterator（uint64 blockmask 遍历器）
        block_info.h               -- BlockInfo（varlen 偏移计算）
        kernel_traits.h            -- CUTLASS kernel traits（MMA atom, smem layout, copy atom）
        softmax.h / mask.h / ...   -- 辅助头文件
        flash_fwd_hdim*_sm80.cu    -- 各 headdim 的编译单元
  infllm_v2/
    __init__.py                    -- Python 包入口
    infllmv2_sparse_attention.py   -- 主 Python 接口（forward/backward Function, stage1, kvcache）
    topk_to_uint64.py              -- topk_to_uint64 Python 封装
    blockmask_to_uint64.py         -- blockmask_to_uint64 Python 封装
    uint64_to_bool.py              -- uint64_to_bool Python 封装
    max_pooling_1d.py              -- max_pooling_1d Python 封装
  setup.py                         -- 构建脚本
```

---

## 详细优化点分析

### 1. 算法层面

**优化点 1.1: backward 路径中 uint64 blockmask 的冗余转换链**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:343-350`
- 描述: 反向传播中，将 `fwd_blockmask_uint64` 先解包成 bool (`cuda_uint64_to_bool`)，转置后再重新打包成 uint64 (`cuda_blockmask_to_uint64`)。这条路径是: `uint64 -> bool -> transpose -> bool -> uint64`，中间产生了两个大 tensor（bool mask 很大，每个 block 1 byte），且有一次 `.contiguous()` 拷贝和一次 `torch.cuda.synchronize()`。实际上可以直接在 GPU 上对 uint64 做转置，或者在 kernel 中直接做 column-oriented 读取。
- 预期收益: **高**。这个同步点在每次反向传播中都会触发，bool mask 的大小是 uint64 mask 的 ~8x。消除同步和两步 kernel 可节省数毫秒。

**优化点 1.2: topk_to_uint64 + varlen_fwd 两步可 fuse**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:93` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh`
- 描述: 当前流程是 `topk_indices -> topk_to_uint64 kernel -> uint64 blockmask -> varlen_fwd kernel`。topk_to_uint64 生成的 uint64 blockmask 被写入 global memory，然后立刻被 varlen_fwd 读取。可以将 topk_to_uint64 的逻辑内联到 varlen_fwd kernel 的 prologue 中，在 shared memory 中直接构建 blockmask 行，避免一次 global memory round-trip。
- 预期收益: **中**。取决于 topk 的 K 值大小；若 K 较小（如 16-32），uint64 mask 行只有几个 uint64，shared memory 完全放得下。

**优化点 1.3: stage1 (block_score) 输出的 max_pooling + topk 可部分 fuse**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh`
- 描述: 当前 stage1 输出 attention scores 后，需要 max_pooling_1d 做下采样，然后 topk 选取。max_pooling_1d 的输出是 topk 的输入。两者可以 fuse 为一个 kernel：在 max_pooling 输出每个位置时，同时维护一个 warp-level top-k 结构，避免将完整下采样结果写回 global memory。
- 预期收益: **中**。取决于 block 数量（out_len），通常为 128-512，一个 warp 内做 bitonic top-k 开销不大。

**优化点 1.4: get_probs kernel 可内联到 stage1 输出**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/get_probs.cuh:7-15`
- 描述: `get_probs_kernel` 做的是 `exp(v * scale - lse[bid])`，这是一个 element-wise 操作。如果这个操作只在 stage1 的输出上使用（将 score 转为概率），可以直接在 stage1 kernel 的 epilogue 中完成，而不是单独发射一个 kernel。
- 预期收益: **低到中**。单个 elementwise kernel 开销本身不大，但减少一次 kernel launch 和 global memory 读写仍有帮助。

### 2. 内存访问

**优化点 2.1: max_pooling_1d_varlen_kernel 线性搜索 batch**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:44-54`
- 描述: 每个 thread 做 `for (int b = 0; b < batch_size; b++)` 线性搜索 `cu_seqlens_q` 来确定自己属于哪个 batch。这是 O(batch_size) 的全局内存读取，且完全不 coalesced（每个 thread 读取不同位置）。应该用二分搜索代替线性搜索，或者用辅助数组做 O(1) 查找。
- 预期收益: **高**。batch_size 较大时（如 32+），所有 thread 都在重复读取 cu_seqlens 数组，导致大量非合并访存。

**优化点 2.2: topk kernel (bitonic_topk) blockDim = n，当 n 很大时可能超限**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh:153-156`
- 描述: `dim3 blockDim(n, 1, 1)`，如果 `n`（block_score 的维度）超过 1024，单个 block 的 thread 数超限。代码中虽有 `kernel_bitonic_topk_multiblock`，但 `bitonic_topk` 函数只调用了 multiblock 版本。实际上在 `topk_func` 中，`dim3 blockDim(n, 1, 1)` 的 n 如果超过 1024，CUDA launch 会失败。需确认调用路径是否保证 n <= 1024；否则存在潜在 bug。
- 预期收益: **中**（正确性 + 性能）。

**优化点 2.3: blockmask_to_uint64 / topk_to_uint64 的 low warp 利用率**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/blockmask_to_uint64.cuh:65-69` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh:67-71`
- 描述: Grid 为 `(blocks_per_row, n_uint64_per_row)`，block 为 `(256, 1)`。当 `batch_size * n_uint64_per_row` 较小时（例如 batch=1, n_uint64=4），只有 4 个 block，严重浪费 GPU。应该将 row 和 col 维度合并到一个 1D grid，让每个 thread 处理多个元素。
- 预期收益: **低到中**。在小 batch decode 场景下，这些 kernel 本身很快；但在 prefill 阶段 batch 较大时可能有影响。

**优化点 2.4: uint64_to_bool kernel 每个 thread 只写 1 bit，大量 waste**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/uint64_to_bool.cuh:10-43`
- 描述: Grid 为 `(blocks_per_row, last_dim_size)`，每个 thread 只读取 1 个 uint64 中的 1 个 bit 然后写 1 个 bool。一个 uint64 有 64 bit，但 64 个 thread 分别读同一个 uint64。大量重复的全局内存读取。可以让每个 thread 读 1 个 uint64 并写 64 个 bool，或者完全消除这个 kernel（见优化点 1.1）。
- 预期收益: **中**。只在 backward 中使用，且如果 1.1 被修复，此 kernel 可被完全消除。

**优化点 2.5: max_pooling_1d kernel 的 input 访问模式**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:77-103`
- 描述: 内层循环 `for (int k = threadIdx.x; k < out_len; k += blockDim.x)` 中，每个 thread 读 `input` 的一个 stride 窗口做 max pooling。Input 的最后一维是 `max_k`（可能是 2048），而 `kernel_size` 通常只有 4-5，但 thread 需要读非连续的多个窗口。当 `stride` 较小时，相邻 thread 读的内存区域高度重叠，却没有利用 shared memory 做 cache。
- 预期收益: **低到中**。max_pooling 本身计算量小，通常不是瓶颈。

### 3. 并行度

**优化点 3.1: fwdIterator::max_no_larger 中串行扫描 uint64**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h:74-85`
- 描述: 当当前 uint64 块没有 bit 时，`max_no_larger` 做 `for (int i = uint64_offset - 1; i >= 0; i--)` 线性扫描前面的 uint64 块。如果 sparsity 很高（大部分 block 被跳过），这个扫描最多遍历 `n_uint64_per_row` 个全局内存位置。在稀疏场景下（这正是此 kernel 的目标场景），此循环可能成为 hotspot。
- 预期收益: **中**。在极端稀疏情况下（topk=8, n_blocks=512），每次 `max_no_larger` 调用可能读 8+ 个 uint64。但 `__clzll` 优化已经做了单 uint64 内的快速查找，多 uint64 的扫描确实无法避免。可以考虑预计算每个 uint64 行的 "前缀最大 block_idx" 辅助数组。

**优化点 3.2: backward 中 cu_seqlens_q_expanded 的 Python for 循环**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:197-208`
- 描述: `cu_seqlens_q_expanded` 的构建是在 Python 中用 for 循环逐元素计算的。这个循环应该在 GPU 上用一个小 kernel 完成，或者用 `cu_seqlens_q * group_size` 向量化（但这不正确因为 cu_seqlens 是 cumulative）。当前实现每步都有 Python 开销和 CUDA kernel launch。
- 预期收益: **中**。虽然循环长度通常等于 batch_size（如 1-32），但每次 backward 都执行且涉及 GPU tensor 操作。

**优化点 3.3: backward 中两次 torch.cuda.empty_cache()**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:246, 263`
- 描述: `torch.cuda.empty_cache()` 会触发 CUDA 内存分配器的全量回收，这是一个非常昂贵的操作（可能耗时数十毫秒），且在训练循环中完全不应使用。这两行代码的意图是释放中间 tensor 的显存，但 Python 引用计数已经足够。`empty_cache()` 只在推理中偶尔使用来减少碎片。
- 预期收益: **高**。`empty_cache()` 可能每次调用耗时 5-50ms，在训练中完全不需要。

### 4. sm_120 (Blackwell) 特性

**优化点 4.1: MMA Atom 仍使用 SM80 指令，未利用 Blackwell warp-group MMA**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:30-33`
- 描述: `MMA_Atom_Arch` 使用 `SM80_16x8x16_F32F16F16F32_TN` 或 `SM80_16x8x16_F32BF16BF16F32_TN`。Blackwell (sm_120) 引入了 `wgmma`（warp-group MMA），一个 warp group（4 个 warp）可以在一条指令中完成 256x128x64 的矩阵乘法，吞吐量远超 SM80 的 mma.sync。cuBLAS 和 CUTLASS 3.x 已经支持 sm_120 的 wgmma。当前代码完全没有 Blackwell 优化路径。
- 预期收益: **高**。Blackwell 的 wgmma 在 FP16/BF16 上吞吐量约为 SM80 mma.sync 的 4-8 倍。对于 attention 这种计算密集型 kernel，这是最大的单点优化。

**优化点 4.2: cp_async 仅使用 SM80 CP_ASYNC，未使用 TMA (Tensor Memory Accelerator)**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:126-127`
- 描述: `Gmem_copy_struct` 使用 `SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>`。Blackwell 引入了 TMA，可以从 global memory 直接将多维 tensor tile 加载到 shared memory，不需要 warp 级编程。TMA 可以大幅减少地址计算和加载指令的开销。CUTLASS 3.x 的 CollectiveBuilder 已经支持 TMA。
- 预期收益: **高**。TMA 可以减少 30-50% 的 global memory load 指令数，且与 wgmma 的 async 特性配合更好。

**优化点 4.3: setup.py 编译目标最高仅 sm_90**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/setup.py:102-107`
- 描述: 虽然 setup.py 有 sm_120 的 gencode 逻辑，但 FlashAttention 的编译单元文件名全部是 `*_sm80.cu`。即使加了 `-gencode arch=compute_120`，kernel traits 中的 `__CUDA_ARCH__ >= 800` 判断也不会激活任何 sm_120 专属路径。内核本身需要添加 `__CUDA_ARCH__ >= 120` 分支来使用 wgmma 和 TMA。
- 预期收益: **高**（与 4.1/4.2 相同，是实现前提）。

**优化点 4.4: Shared memory 大小未利用 Blackwell 的 228KB/shared memory**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h:107-109`
- 描述: Blackwell SM 每个 SM 有 228KB shared memory（vs A100 的 164KB）。当前 kernel 的 shared memory 使用量（`kSmemSize`）是按 SM80/90 设计的，没有利用更大的 shared memory 来增加 tile size（例如 kBlockM 从 16 增到 32 或 64）。
- 预期收益: **中**。更大的 tile 可以减少 global memory 访问次数，但需要配合 wgmma 才能充分发挥。

### 5. Python 绑定层

**优化点 5.1: torch.cuda.synchronize() 在 backward 中**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:348`
- 描述: `torch.cuda.synchronize()` 等待整个 GPU 空闲，这在训练中是灾难性的。它打断了 CUDA 流水线，使 GPU 在等待期间完全闲置。这是为 blockmask 转换添加的，但完全可以通过消除 1.1 中的冗余转换链来移除。
- 预期收益: **高**。与优化点 1.1 一起修复。

**优化点 5.2: blockmask_to_uint64.py 和 uint64_to_bool.py 中的 .item() 调用**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/blockmask_to_uint64.py:25` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/uint64_to_bool.py:21`
- 描述: `torch.prod(torch.tensor(original_shape[:-1], dtype=torch.int64)).item()` 在 CPU 上创建 tensor 然后用 `.item()` 取值。这涉及 CPU tensor 创建和同步。可以用 Python 的 `math.prod()` 直接在 CPU 上计算。
- 预期收益: **低**。开销很小，但每帧都会触发。

**优化点 5.3: infllmv2_attn_varlen_forward 中 GQA reshape 多次 contiguous()**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:88`
- 描述: `q.reshape(-1, nheads_k, group_size, head_dim).transpose(1, 2).reshape(-1, nheads_k, head_dim).contiguous()` 会触发一次数据拷贝（因为 transpose 后 reshape 不连续）。在 backward 中同样的操作做了 3 次（q, dout, out 各一次）。可以考虑用 `permute + reshape` 或直接在 C++ kernel 中用 stride 处理，避免多次内存拷贝。
- 预期收益: **中**。每次 contiguous() 都是一次完整的 tensor 拷贝，在 prefill 阶段 tensor 较大时影响明显。

**优化点 5.4: infllmv2_attn_varlen_forward 输出再做一次 contiguous()**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:127-130`
- 描述: forward 输出的 reshape + contiguous 又做了一次拷贝。如果下游能接受非连续 tensor，可以省略。
- 预期收益: **低到中**。

### 6. 与 FlashInfer 的交互

**优化点 6.1: 未使用 FlashInfer 的稀疏 attention API**

- 位置: 整个 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py`
- 描述: FlashInfer 0.6.x 提供了原生的 sparse attention 接口（`flashinfer.sparse`），支持 block-sparse mask 和 variable-length 序列。当前实现完全绕过了 FlashInfer，使用自定义的 FlashAttention-v2 fork（带 blockmask 支持）。FlashInfer 的稀疏 attention 可能在 Blackwell 上有更好的优化，且与 vLLM 等框架的集成更顺畅。
- 预期收益: **中**。取决于 FlashInfer 稀疏 API 的成熟度和性能。当前自定义 FA2 fork 的优势是 blockmask 遍历器与 kernel 紧密集成。

**优化点 6.2: stage1 使用自定义 FlashAttention fork 而非 FlashInfer 的 batch attention**

- 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:567-590`
- 描述: `infllmv2_attn_stage1` 调用 `infllm_cuda.varlen_fwd_stage1`，这是一个特殊的 FlashAttention 变体，输出 attention score（而非通常的 O = softmax(QK^T)V）。FlashInfer 的 batch prefill attention 也可以输出 score，但当前未使用。
- 预期收益: **低**。stage1 的特殊之处在于 kBlockM=16, n_block_dim=1 的配置，这是为 NSA pattern 优化的。FlashInfer 不一定有此配置。

---

## 最值得动手的前 3 个优化点（按 ROI 排序）

### 第 1 名: 消除 backward 中 blockmask 转换链 + synchronize + empty_cache

- 涉及位置:
  - `infllmv2_sparse_attention.py:343-350`（uint64->bool->transpose->uint64 转换链）
  - `infllmv2_sparse_attention.py:348`（`torch.cuda.synchronize()`）
  - `infllmv2_sparse_attention.py:246,263`（`torch.cuda.empty_cache()`）
- ROI 理由: 这 3 个问题高度关联，修复方向明确。`synchronize()` 在每次 backward 中引入完整的 GPU pipeline stall，`empty_cache()` 触发 CUDA allocator 的全量回收，两者合计可能占 backward 耗时的 20-40%。修复方案：写一个 CUDA kernel 直接对 uint64 blockmask 做转置（行优先 <-> 列优先的 bit 重排），或修改 bwdIterator 使其能直接读取行优先格式的 uint64 mask，从而完全跳过 bool 中间态。工作量中等（一个 ~50 行的 kernel + Python 层修改），收益极高。

### 第 2 名: 为 sm_120 (Blackwell) 添加 wgmma + TMA kernel 路径

- 涉及位置:
  - `kernel_traits.h:30-33`（MMA Atom 使用 SM80）
  - `kernel_traits.h:126-127`（cp_async 使用 SM80）
  - `setup.py:102-107`（编译目标仅 sm_80）
  - `flash_fwd_launch_template.h`（缺少 sm_120 dispatch）
- ROI 理由: RTX 6000D (sm_120) 的 wgmma 吞吐量是 SM80 mma.sync 的数倍。当前代码在 Blackwell 上以兼容模式运行，浪费了大量算力。实现方案：在 `kernel_traits.h` 中添加 `__CUDA_ARCH__ >= 120` 分支，使用 `SM120_64x128x32_F32BF16BF16_AssumeM16` 等 wgmma atom，用 TMA 替代 cp_async 做 Q/K/V 加载。工作量较大（需要新增 sm_120 编译单元和 kernel traits），但收益是架构级的。作为第一步，可以先只为 hdim128_bf16（最常用的配置）添加 sm_120 路径。

### 第 3 名: max_pooling_1d_varlen_kernel 中用二分搜索替代线性搜索 batch

- 涉及位置:
  - `max_pooling_1d.cuh:44-54`（`for (int b = 0; b < batch_size; b++)` 线性扫描）
- ROI 理由: 这是一个 O(batch_size) 的 global memory 读取循环，每个 thread 独立执行，完全无法合并。在 batch_size=32 时，每个 thread 最多读 32 个 int（128 bytes），且重复度极高。改为二分搜索只需读 log2(batch_size) 个 int。工作量极小（修改 10 行代码），收益随 batch_size 线性增长。在 prefill 场景（batch_size 较大）中尤其明显。

---

## 补充说明

1. **num_k_heads=2 硬编码**: `flash_api.cpp:708` 和 `flash_api.cpp:1711` 将 `params.num_k_heads` 硬编码为 2。如果模型架构改变 KV head 数量，此处会出错。应该从输入 tensor 的 shape 动态推导。

2. **stage1 中 n_block_dim=1**: `flash_api.cpp:989` 设置 `params.n_block_dim = 1`，这意味着 stage1 的 blockmask 遍历器每个 N-block 只有 1 个 token，与 stage2 的 `n_block_dim=64` 不同。这是 NSA 的设计选择（每个压缩 token 独立评分），但确认其正确性很重要。

3. **flash_fwd_launch_template.h 中多个 constexpr static bool 硬编码为 false**: 行 76-79 将 `Is_local`、`ReturnSoftmaxConst`、`Has_alibi`、`Is_softcap` 全部设为 `false`。这是与 setup.py 中 `-DFLASHATTENTION_DISABLE_*` 宏对应的，减少了编译时间，但也意味着这些功能不可用。若未来需要 local attention 或 softcap，需重新启用。

> DEVELOPER

请深入阅读 /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/ 下的所有代码，目标是搞清楚"为 sm_120 (Blackwell) 添加 wgmma + TMA 路径"需要做什么、能怎么做。

硬件背景：
- NVIDIA RTX 6000D，sm_120 (Blackwell)，84 GB VRAM
- CUDA toolkit 13.2，CUTLASS 已可用
- 当前 MMA Atom 是 SM80_16x8x16_F32F16F16F32_TN（mma.sync），未用 wgmma
- 当前数据加载是 SM80_CP_ASYNC_CACHEGLOBAL（cp.async），未用 TMA

请完整阅读以下文件（全文，不要截断）：
1. csrc/flash_attn/src/kernel_traits.h
2. csrc/flash_attn/src/flash_fwd_launch_template.h
3. csrc/flash_attn/src/flash_fwd_kernel.h
4. csrc/flash_attn/src/flash_blockmask.h
5. csrc/flash_attn/src/flash.h
6. csrc/flash_attn/src/block_info.h
7. csrc/flash_attn/flash_api.cpp（重点看 varlen_fwd, varlen_fwd_stage1, fwd_kvcache 的 dispatch 逻辑）
8. csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu（了解现有编译单元结构）
9. setup.py（了解编译命令和 gencode 配置）
10. 任何 flash_fwd_hdim*_sm*.cu 文件

分析以下问题并给出详细结论：

**A. 现有架构摘要**
- `Flash_fwd_kernel_traits` 的完整模板参数和 MMA/Copy atom 选择逻辑
- `run_flash_fwd` 在 `flash_fwd_launch_template.h` 中的 kernel launch 流程（smem size、grid、block）
- `compute_attn_1rowblock` 的主循环结构（Q/K/V load → MMA → softmax → output，关键的流水线 stage 数）
- `flash_blockmask.h` 中 fwdIterator 的接口和遍历逻辑

**B. 迁移到 wgmma + TMA 的技术要点**
- CUTLASS 3.x 中 sm_120 对应的 wgmma MMA Atom 名称（如 SM90_64x64x16_F32F16F16F32_SS 等，但这是 sm_90；sm_120/Blackwell 的对应 atom 是什么）
- CUTLASS 3.x 中 TMA copy atom（SM90_TMA_LOAD / SM120_TMA_LOAD）的接口差异
- 现有代码用了哪个版本的 CUTLASS（查 setup.py 的 include path 或 CMakeLists）
- 如果现有 CUTLASS 版本不支持 sm_120，替代方案是什么

**C. 工程量评估**
- 需要修改哪些文件，每个文件大概改动量
- 最小可行路径（只改 hdim128 + bf16 + sm_120）需要新增多少代码
- 有哪些不可绕过的技术障碍（如 CUTLASS 版本限制、API 不兼容等）

**D. 可行性判断**
- Flash Attention 3（FA3）已经实现了 sm_90 的 wgmma + TMA。FA3 的源码结构是否可以直接参考或 fork？
- 是否有更简单的替代方案，比如：直接调用 FlashInfer（已支持 sm_120）的 kernel，而不是修改这个自定义 FA fork？

请给出所有文件的关键代码片段（函数签名、模板参数、关键循环），以支撑你的结论。搜索深度：very thorough。

> AGENT

我将首先阅读所有指定的文件，以彻底理解代码库。让我开始并行阅读这些文件。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include "cute/tensor.hpp"
8	
9	#include "cutlass/cutlass.h"
10	#include "cutlass/layout/layout.h"
11	#include <cutlass/numeric_types.h>
12	
13	using namespace cute;
14	
15	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t>
16	struct Flash_kernel_traits {
17	
18	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
19	    using Element = elem_type;
20	    static constexpr bool Has_cp_async = true;
21	#else
22	    using Element = cutlass::half_t;
23	    static constexpr bool Has_cp_async = false;
24	#endif
25	
26	    using ElementAccum = float;
27	    using index_t = int64_t;
28	
29	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
30	    using MMA_Atom_Arch = std::conditional_t<
31	        std::is_same_v<elem_type, cutlass::half_t>,
32	        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,
33	        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>
34	    >;
35	#else
36	    using MMA_Atom_Arch = MMA_Atom<SM75_16x8x8_F32F16F16F32_TN>;
37	#endif
38	
39	#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 750
40	    using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>;
41	    using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>;
42	#else
43	    using SmemCopyAtom = Copy_Atom<DefaultCopy, elem_type>;
44	    using SmemCopyAtomTransposed = Copy_Atom<DefaultCopy, elem_type>;
45	#endif
46	};
47	
48	// If Share_Q_K_smem is true, that forces Is_Q_in_regs to be true
49	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, bool Is_Q_in_regs_=false, bool Share_Q_K_smem_=false, typename elem_type=cutlass::half_t,
50	         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
51	struct Flash_fwd_kernel_traits : public Base {
52	    using Element = typename Base::Element;
53	    using ElementAccum = typename Base::ElementAccum;
54	    using index_t = typename Base::index_t;
55	    static constexpr bool Has_cp_async = Base::Has_cp_async;
56	    using SmemCopyAtom = typename Base::SmemCopyAtom;
57	    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;
58	
59	    static constexpr bool Share_Q_K_smem = Share_Q_K_smem_;
60	    static constexpr bool Is_Q_in_regs = Is_Q_in_regs_ || Share_Q_K_smem;
61	
62	    // The number of threads.
63	    static constexpr int kNWarps = kNWarps_;
64	    static constexpr int kNThreads = kNWarps * 32;
65	
66	    static constexpr int kBlockM = kBlockM_;
67	    static constexpr int kBlockN = kBlockN_;
68	    static constexpr int kHeadDim = kHeadDim_;
69	    static_assert(kHeadDim % 32 == 0);
70	    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
71	    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
72	    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;
73	
74	    using TiledMma = TiledMMA<
75	        typename Base::MMA_Atom_Arch,
76	        Layout<Shape<Int<kNWarps>,_1,_1>>,  // 4x1x1 or 8x1x1 thread group
77	        Tile<Int<16 * kNWarps>, _16, _16>>;
78	
79	    using SmemLayoutAtomQ = decltype(
80	        composition(Swizzle<kSwizzle, 3, 3>{},
81	                    // This has to be kBlockKSmem, using kHeadDim gives wrong results for d=128
82	                    Layout<Shape<_8, Int<kBlockKSmem>>,
83	                           Stride<Int<kBlockKSmem>, _1>>{}));
84	    using SmemLayoutQ = decltype(tile_to_shape(
85	        SmemLayoutAtomQ{},
86	        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
87	
88	    using SmemLayoutKV = decltype(tile_to_shape(
89	        SmemLayoutAtomQ{},
90	        Shape<Int<kBlockN>, Int<kHeadDim>>{}));
91	
92	    // https://github.com/ColfaxResearch/cutlass-kernels/blob/a222587e6d59b93ba704853d3946fb686d8b8892/src/fmha/fmha_forward.cu#L434
93	    using SmemLayoutVtransposed = decltype(
94	        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
95	    using SmemLayoutVtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutVtransposed{}));
96	
97	    using SmemLayoutAtomO = decltype(
98	        composition(Swizzle<kSwizzle, 3, 3>{},
99	                    Layout<Shape<Int<8>, Int<kBlockKSmem>>,
100	                           Stride<Int<kBlockKSmem>, _1>>{}));
101	    using SmemLayoutO = decltype(tile_to_shape(
102	        SmemLayoutAtomO{},
103	        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
104	    using SmemCopyAtomO = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>;
105	    using SmemCopyAtomOaccum = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>;
106	
107	    static constexpr int kSmemQSize = size(SmemLayoutQ{}) * sizeof(Element);
108	    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
109	    static constexpr int kSmemSize = Share_Q_K_smem ? std::max(kSmemQSize, kSmemKVSize) : kSmemQSize + kSmemKVSize;
110	
111	    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
112	    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
113	    // Using kBlockKSmem here is 6-10% faster than kBlockKGmem for d=128 because of bank conflicts.
114	    // For example, for d=128, smem is split into 2 "pages", each page takes care of columns
115	    // 0-63 and 64-127. If we have 16 threads per row for gmem read, when we write to smem,
116	    // thread 0 - 7 will write to the first page and thread 8 - 15 will write to the second page,
117	    // to the same banks.
118	    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
119	    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
120	    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
121	                                  Stride<Int<kGmemThreadsPerRow>, _1>>;
122	
123	    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
124	    // from the same address by the same threadblock. This is slightly faster.
125	    using Gmem_copy_struct = std::conditional_t<
126	        Has_cp_async,
127	        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
128	        AutoVectorizingCopyWithAssumedAlignment<128>
129	    >;
130	    using GmemTiledCopyQKV = decltype(
131	        make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{},
132	                        GmemLayoutAtom{},
133	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
134	    using GmemTiledCopyO = decltype(
135	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
136	                        GmemLayoutAtom{},
137	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per store
138	
139	    using GmemLayoutAtomOaccum = std::conditional_t<
140	        kBlockKSmem == 32,
141	        Layout<Shape <_16, _8>,  // Thread layout, 8 threads per row
142	               Stride< _8, _1>>,
143	        Layout<Shape <_8, _16>,  // Thread layout, 16 threads per row
144	               Stride< _16, _1>>
145	    >;
146	    using GmemTiledCopyOaccum = decltype(
147	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
148	                        GmemLayoutAtomOaccum{},
149	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
150	    using GmemLayoutAtomRotcossin = GmemLayoutAtom;
151	    using GmemTiledCopyRotcossin = decltype(
152	        make_tiled_copy(Copy_Atom<UniversalCopy<uint64_t>, Element>{},
153	                        GmemLayoutAtomRotcossin{},
154	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per load
155	    using GmemTiledCopyRotcossinCont = decltype(
156	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
157	                        GmemLayoutAtomRotcossin{},
158	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per load
159	};
160	
161	// Is_V_in_regs is an option to reduce smem usage, but will increase register pressue.
162	// No_double_buffer is another option to reduce smem usage, but will slow things down.
163	template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_,
164	         int AtomLayoutMSdP_=1, int AtomLayoutNdKV=2, int AtomLayoutMdQ=2,
165	         bool Is_V_in_regs_=false, bool No_double_buffer_=false, typename elem_type=cutlass::half_t,
166	         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
167	struct Flash_bwd_kernel_traits : public Base {
168	    using Element = typename Base::Element;
169	    using ElementAccum = typename Base::ElementAccum;
170	    using index_t = typename Base::index_t;
171	    static constexpr bool Has_cp_async = Base::Has_cp_async;
172	    using SmemCopyAtom = typename Base::SmemCopyAtom;
173	    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;
174	
175	    static constexpr bool Is_V_in_regs = Is_V_in_regs_;
176	    static constexpr bool No_double_buffer = No_double_buffer_;
177	
178	    // The number of threads.
179	    static constexpr int kNWarps = kNWarps_;
180	    static constexpr int kNThreads = kNWarps * 32;
181	
182	    static constexpr int kBlockM = kBlockM_;
183	    static constexpr int kBlockN = kBlockN_;
184	    static constexpr int kHeadDim = kHeadDim_;
185	    static_assert(kHeadDim % 32 == 0);
186	    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
187	    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
188	    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;
189	
190	    static constexpr int AtomLayoutMSdP = AtomLayoutMSdP_;
191	    static_assert(kNWarps % AtomLayoutMSdP == 0);
192	    static_assert(kNWarps % AtomLayoutNdKV == 0);
193	    static_assert(kNWarps % AtomLayoutMdQ == 0);
194	
195	    using TiledMmaSdP = TiledMMA<
196	        typename Base::MMA_Atom_Arch,
197	        Layout<Shape<Int<AtomLayoutMSdP>, Int<kNWarps / AtomLayoutMSdP>, _1>>,
198	        Tile<Int<16 * AtomLayoutMSdP>, Int<16 * kNWarps / AtomLayoutMSdP>, _16>>;
199	
200	    using TiledMmadKV = TiledMMA<
201	        typename Base::MMA_Atom_Arch,
202	        Layout<Shape<Int<AtomLayoutNdKV>, Int<kNWarps / AtomLayoutNdKV>, _1>>,
203	        Tile<Int<16 * AtomLayoutNdKV>, Int<16 * kNWarps / AtomLayoutNdKV>, _16>>;
204	
205	    using TiledMmadQ = TiledMMA<
206	        typename Base::MMA_Atom_Arch,
207	        Layout<Shape<Int<AtomLayoutMdQ>, Int<kNWarps / AtomLayoutMdQ>, _1>>,  // 2x4x1 or 4x2x1 thread group
208	        Tile<Int<16 * AtomLayoutMdQ>, Int<16 * kNWarps / AtomLayoutMdQ>, _16>>;
209	
210	    using SmemLayoutAtomQdO = decltype(
211	        composition(Swizzle<kSwizzle, 3, 3>{},
212	                    Layout<Shape<_8, Int<kBlockKSmem>>,
213	                           Stride<Int<kBlockKSmem>, _1>>{}));
214	    using SmemLayoutQdO = decltype(tile_to_shape(
215	        SmemLayoutAtomQdO{},
216	        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
217	
218	    using SmemLayoutAtomKV = decltype(
219	        composition(Swizzle<kSwizzle, 3, 3>{},
220	                    Layout<Shape<Int<kBlockM / kNWarps>, Int<kBlockKSmem>>,
221	                           Stride<Int<kBlockKSmem>, _1>>{}));
222	    using SmemLayoutKV = decltype(tile_to_shape(
223	        // SmemLayoutAtomQdO{},
224	        SmemLayoutAtomKV{},
225	        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
226	
227	    using SmemLayoutKtransposed = decltype(
228	        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
229	    using SmemLayoutKtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutKtransposed{}));
230	
231	    // TODO: generalize to other values of kBlockN
232	    // TODO: what should be the Swizzle here? 3 is faster than 1, and 1 is faster than 2
233	    // static constexpr int kPBlockN = kBlockN;
234	    // Temporarily disabling this for hdim 256 on sm86 and sm89
235	    // static_assert(kBlockN >= 64);
236	    static_assert(kBlockN >= 32);
237	    // TD [2023-03-19]: Idk why kPBlockN = 16 and kSwizzlePdS=3 is the fastest.
238	    static constexpr int kPBlockN = kBlockN >= 64 ? 64 : 32;
239	    static_assert(kPBlockN == 16 || kPBlockN == 32 || kPBlockN == 64);
240	    // static constexpr int kSwizzlePdS = kPBlockN == 16 ? 1 : (kPBlockN == 32 ? 2 : 3);
241	    static constexpr int kSwizzlePdS = 3;
242	    using SmemLayoutAtomPdS = decltype(
243	        composition(Swizzle<kSwizzlePdS, 3, 3>{},
244	                    Layout<Shape<Int<kBlockM>, Int<kPBlockN>>,
245	                           Stride<Int<kPBlockN>, _1>>{}));
246	    using SmemLayoutPdS = decltype(tile_to_shape(
247	        SmemLayoutAtomPdS{},
248	        make_shape(Int<kBlockM>{}, Int<kBlockN>{})));
249	    using SmemLayoutPdStransposed = decltype(
250	        composition(SmemLayoutPdS{}, make_layout(Shape<Int<kBlockN>, Int<kBlockM>>{}, GenRowMajor{})));
251	    using SmemLayoutPdStransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutPdStransposed{}));
252	
253	    using SmemCopyAtomPdS = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
254	
255	    using SmemLayoutQdOtransposed = decltype(
256	        composition(SmemLayoutQdO{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockM>>{}, GenRowMajor{})));
257	    using SmemLayoutQdOtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutQdOtransposed{}));
258	
259	    using SmemLayoutAtomdKV = decltype(
260	        composition(Swizzle<kSwizzle, 3, 3>{},
261	                    Layout<Shape<_8, Int<kBlockKSmem>>,
262	                           Stride<Int<kBlockKSmem>, _1>>{}));
263	    using SmemLayoutdKV = decltype(tile_to_shape(
264	        SmemLayoutAtomdKV{},
265	        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
266	    using SmemCopyAtomdKV = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
267	
268	    using SmemLayoutAtomdQ = decltype(
269	        composition(Swizzle<kSwizzle, 3, 3>{},
270	                    Layout<Shape<_8, Int<kBlockKSmem>>,
271	                           Stride<Int<kBlockKSmem>, _1>>{}));
272	    using SmemLayoutdQ = decltype(tile_to_shape(
273	        SmemLayoutAtomdQ{},
274	        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
275	    using SmemCopyAtomdQ = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;
276	
277	    // Double buffer for sQ
278	    static constexpr int kSmemQdOSize = size(SmemLayoutQdO{}) * (No_double_buffer ? 2 : 3) * sizeof(Element);
279	    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
280	    static constexpr int kSmemdSSize = size(SmemLayoutPdS{}) * sizeof(Element);
281	    static constexpr int kSmemPSize = size(SmemLayoutPdS{}) * sizeof(Element);
282	    static constexpr int kSmemdQSize = size(SmemLayoutdQ{}) * sizeof(Element);
283	    static constexpr int kSmemSize = kSmemQdOSize
284	        + (!Is_V_in_regs
285	           ? kSmemKVSize + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)
286	           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)));
287	    static constexpr int kSmemSize1colblock = kSmemQdOSize
288	        + (!Is_V_in_regs
289	           ? kSmemKVSize + kSmemdSSize + kSmemPSize
290	           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + kSmemPSize));
291	
292	    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
293	    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
294	    // Using kBlockKSmem instead of kHeadDim here to avoid bank conflicts, but doesn't seem
295	    // to affect speed in practice.
296	    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
297	    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
298	    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
299	                                  Stride<Int<kGmemThreadsPerRow>, _1>>;
300	
301	    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
302	    // from the same address by the same threadblock. This is slightly faster.
303	    using Gmem_copy_struct = std::conditional_t<
304	        Has_cp_async,
305	        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
306	        AutoVectorizingCopyWithAssumedAlignment<128>
307	    >;
308	    using GmemTiledCopyQKV = decltype(
309	        make_tiled_copy(Copy_Atom<Gmem_copy_struct, elem_type>{},
310	                        GmemLayoutAtom{},
311	                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
312	    using GmemTiledCopydO = decltype(
313	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
314	                        GmemLayoutAtom{},
315	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
316	    using GmemTiledCopydKV = decltype(
317	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
318	                        GmemLayoutAtom{},
319	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
320	    using GmemTiledCopydQ = decltype(
321	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
322	                        GmemLayoutAtom{},
323	                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
324	    // using GmemLayoutAtomdQaccum = std::conditional_t<
325	    //     kBlockKSmem == 32,
326	    //     Layout<Shape <_32, _8>,  // Thread layout, 8 threads per row
327	    //            Stride< _8, _1>>,
328	    //     Layout<Shape <_16, _16>,  // Thread layout, 16 threads per row
329	    //            Stride< _16, _1>>
330	    // >;
331	    using GmemLayoutAtomdQaccum = Layout<Shape<_16, _8>, Stride<_8, _1>>;
332	    using GmemTiledCopydQaccum = decltype(
333	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
334	                        GmemLayoutAtomdQaccum{},
335	                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
336	
337	    using GmemTiledCopydQaccumAtomicAdd = decltype(
338	        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
339	                        Layout<Shape <_8, _16>,  // Thread layout, 8 threads per row
340	                               Stride<_16, _1>>{},
341	                        Layout<Shape < _1, _1>>{}));  // Val layout, 1 val per store
342	
343	};
344	
345	////////////////////////////////////////////////////////////////////////////////////////////////////
346
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	#include <c10/cuda/CUDAException.h>  // For C10_CUDA_CHECK and C10_CUDA_KERNEL_LAUNCH_CHECK
7	
8	#include "static_switch.h"
9	#include "hardware_info.h"
10	#include "flash.h"
11	#include "flash_fwd_kernel.h"
12	
13	// Determine if the architecture supports FLASH and define a macro to handle parameter modifiers
14	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
15	#define ARCH_SUPPORTS_FLASH
16	#define KERNEL_PARAM_MODIFIER __grid_constant__
17	#else
18	#define KERNEL_PARAM_MODIFIER
19	#endif
20	
21	// Define a macro for unsupported architecture handling to centralize the error message
22	#define FLASH_UNSUPPORTED_ARCH printf("FATAL: FlashAttention requires building with sm version sm80-sm90, but was built for < 8.0!");
23	
24	// Use a macro to clean up kernel definitions
25	#define DEFINE_FLASH_FORWARD_KERNEL(kernelName, ...) \
26	template<typename Kernel_traits, __VA_ARGS__> \
27	__global__ void kernelName(KERNEL_PARAM_MODIFIER const Flash_fwd_params params)
28	
29	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_kernel, bool Is_dropout, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Return_softmax) {
30	    #if defined(ARCH_SUPPORTS_FLASH)
31	        static_assert(!(Is_causal && Is_local)); // Enforce constraints
32	        flash::compute_attn<Kernel_traits, Is_dropout, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Return_softmax>(params);
33	    #else
34	        FLASH_UNSUPPORTED_ARCH
35	    #endif
36	}
37	
38	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_kernel, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV) {
39	    #if defined(ARCH_SUPPORTS_FLASH)
40	        flash::compute_attn_splitkv<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params);
41	    #else
42	        FLASH_UNSUPPORTED_ARCH
43	    #endif
44	}
45	
46	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_stage1_kernel, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV) {
47	    #if defined(ARCH_SUPPORTS_FLASH)
48	        flash::compute_attn_splitkv_stage1<Kernel_traits, Is_causal, Is_local, Has_alibi, Is_even_MN, Is_even_K, Is_softcap, Split, Append_KV>(params);
49	    #else
50	        FLASH_UNSUPPORTED_ARCH
51	    #endif
52	}
53	
54	DEFINE_FLASH_FORWARD_KERNEL(flash_fwd_splitkv_combine_kernel, int kBlockM, int Log_max_splits, bool Is_even_K) {
55	    static_assert(Log_max_splits >= 1);
56	    flash::combine_attn_seqk_parallel<Kernel_traits, kBlockM, Log_max_splits, Is_even_K>(params);
57	}
58	
59	template<typename Kernel_traits, bool Is_dropout, bool Is_causal>
60	void run_flash_fwd(Flash_fwd_params &params, cudaStream_t stream) {
61	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
62	    // printf("smem_size = %d\n", smem_size);
63	
64	    // Work-around for gcc 7. It doesn't like nested BOOL_SWITCH.
65	    // https://github.com/kokkos/kokkos-kernels/issues/349
66	    // https://github.com/HazyResearch/flash-attention/issues/21
67	
68	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
69	    dim3 grid(num_m_block, params.b, params.h);
70	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
71	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
72	    // const bool return_softmax = params.p_ptr != nullptr;
73	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
74	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
75	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
76	            constexpr static bool Is_local = false; { // TODO remove debug info
77	                // BOOL_SWITCH(return_softmax, ReturnSoftmaxConst, [&] {
78	                constexpr static bool ReturnSoftmaxConst = false; { // TODO remove debug info
79	                    // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
80	                    constexpr static bool Has_alibi = false; { // TODO remove debug info
81	                        // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
82	                        constexpr static bool Is_softcap = false; {
83	                            // Will only return softmax if dropout, to reduce compilation time.
84	                            // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
85	                            // If return_softmax, set IsEvenMNConst to false to reduce number of templates
86	                            // If head dim > 128, set IsEvenMNConst to false to reduce number of templates
87	                            // If Is_local, set Is_causal to false
88	                            auto kernel = &flash_fwd_kernel<Kernel_traits, Is_dropout && !Is_softcap, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && IsEvenKConst && !Is_local && !ReturnSoftmaxConst && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, ReturnSoftmaxConst && Is_dropout && !Is_softcap>;
89	                            // auto kernel = &flash_fwd_kernel<Kernel_traits, false, Is_causal, false, false, true, true, false>;
90	                            // printf("IsEvenMNConst = %d, IsEvenKConst = %d, Is_local = %d, Is_causal = %d, ReturnSoftmaxConst = %d, Is_dropout = %d\n", int(IsEvenMNConst), int(IsEvenKConst), int(Is_local), int(Is_causal), int(ReturnSoftmaxConst), int(Is_dropout));
91	                            // auto kernel = &flash_fwd_kernel<Kernel_traits, false, Is_causal, false, true, true, false>;
92	                            if (smem_size >= 48 * 1024) {
93	                                C10_CUDA_CHECK(cudaFuncSetAttribute(
94	                                    kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
95	                            }
96	                            // int ctas_per_sm;
97	                            // cudaError status_ = cudaOccupancyMaxActiveBlocksPerMultiprocessor(
98	                            //     &ctas_per_sm, kernel, Kernel_traits::kNThreads, smem_size);
99	                            // printf("smem_size = %d, CTAs per SM = %d\n", int(smem_size), ctas_per_sm);
100	                            kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
101	                            C10_CUDA_KERNEL_LAUNCH_CHECK();
102	                        }
103	                    }
104	                }
105	            }
106	        });
107	    });
108	}
109	
110	template<typename Kernel_traits, bool Is_causal>
111	void run_flash_splitkv_fwd(Flash_fwd_params &params, cudaStream_t stream) {
112	    static_assert(!Kernel_traits::Is_Q_in_regs, "SplitKV implementation does not support Is_Q_in_regs");
113	    static_assert(!Kernel_traits::Share_Q_K_smem, "SplitKV implementation does not support Share_Q_K_smem");
114	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
115	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
116	    dim3 grid(num_m_block, params.num_splits > 1 ? params.num_splits : params.b, params.num_splits > 1 ? params.b * params.h : params.h);
117	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
118	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
119	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
120	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
121	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
122	            constexpr static bool Is_local = false; { // TODO remove debug info
123	                BOOL_SWITCH(params.num_splits > 1, Split, [&] {
124	                    BOOL_SWITCH(params.knew_ptr != nullptr, Append_KV, [&] {
125	                        // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
126	                        constexpr static bool Has_alibi = false; { // TODO remove debug info
127	                            // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
128	                            constexpr static bool Is_softcap = false; { // TODO remove debug info
129	                                // If Append_KV, then we must have seqlen_offsets, which means cu_seqlens_k != nullptr.
130	                                // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
131	                                // If Is_local, set Is_causal to false
132	                                auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && !Append_KV && IsEvenKConst && !Is_local && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, Split, Append_KV>;
133	                                // auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, false, true, Split, Append_KV>;
134	                                // auto kernel = &flash_fwd_splitkv_kernel<Kernel_traits, Is_causal, false, IsEvenKConst>;
135	                                if (smem_size >= 48 * 1024) {
136	                                    C10_CUDA_CHECK(cudaFuncSetAttribute(
137	                                        kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
138	                                }
139	                                kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
140	                                C10_CUDA_KERNEL_LAUNCH_CHECK();
141	                            }
142	                        }
143	                    });
144	                });
145	            }
146	        });
147	    });
148	    if (params.num_splits > 1) {
149	        // We want kBlockM to be as small as possible for more parallelism.
150	        // With 128 threads we can load 512 elements at a time, so if headdim is divisible by 128, kBlockM = 4.
151	        // If headdim is divisible by 64, then we set kBlockM = 8, etc.
152	        constexpr static int kBlockM = Kernel_traits::kHeadDim % 128 == 0 ? 4 : (Kernel_traits::kHeadDim % 64 == 0 ? 8 : 16);
153	        dim3 grid_combine((params.b * params.h * params.seqlen_q + kBlockM - 1) / kBlockM);
154	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
155	            if (params.num_splits <= 2) {
156	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 1, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
157	            } else if (params.num_splits <= 4) {
158	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 2, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
159	            } else if (params.num_splits <= 8) {
160	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 3, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
161	            } else if (params.num_splits <= 16) {
162	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 4, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
163	            } else if (params.num_splits <= 32) {
164	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 5, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
165	            } else if (params.num_splits <= 64) {
166	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 6, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
167	            } else if (params.num_splits <= 128) {
168	                flash_fwd_splitkv_combine_kernel<Kernel_traits, kBlockM, 7, IsEvenKConst><<<grid_combine, Kernel_traits::kNThreads, 0, stream>>>(params);
169	            }
170	            C10_CUDA_KERNEL_LAUNCH_CHECK();
171	        });
172	    }
173	}
174	
175	template<typename Kernel_traits, bool Is_causal>
176	void run_flash_splitkv_fwd_stage1(Flash_fwd_params &params, cudaStream_t stream) {
177	    static_assert(!Kernel_traits::Is_Q_in_regs, "SplitKV implementation does not support Is_Q_in_regs");
178	    static_assert(!Kernel_traits::Share_Q_K_smem, "SplitKV implementation does not support Share_Q_K_smem");
179	    constexpr size_t smem_size = Kernel_traits::kSmemSize;
180	    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
181	    dim3 grid(num_m_block, params.num_splits > 1 ? params.num_splits : params.b, params.num_splits > 1 ? params.b * params.h : params.h);
182	    const bool is_even_MN = params.cu_seqlens_q == nullptr && params.cu_seqlens_k == nullptr && params.seqlen_k % Kernel_traits::kBlockN == 0 && params.seqlen_q % Kernel_traits::kBlockM == 0;
183	    const bool is_even_K = params.d == Kernel_traits::kHeadDim;
184	    BOOL_SWITCH(is_even_MN, IsEvenMNConst, [&] {
185	        EVENK_SWITCH(is_even_K, IsEvenKConst, [&] {
186	            // LOCAL_SWITCH((params.window_size_left >= 0 || params.window_size_right >= 0) && !Is_causal, Is_local, [&] {
187	            constexpr static bool Is_local = false; { // TODO remove debug info
188	                // BOOL_SWITCH(params.num_splits > 1, Split, [&] {
189	                constexpr static bool Split = false; { // TODO remove debug info
190	                    // BOOL_SWITCH(params.knew_ptr != nullptr, Append_KV, [&] {
191	                    constexpr static bool Append_KV = false; { // TODO remove debug info
192	                        // ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
193	                        constexpr static bool Has_alibi = false; { // TODO remove debug info
194	                            // SOFTCAP_SWITCH(params.softcap > 0.0, Is_softcap, [&] {
195	                            constexpr static bool Is_softcap = false; { // TODO remove debug info
196	                                // If Append_KV, then we must have seqlen_offsets, which means cu_seqlens_k != nullptr.
197	                                // If not IsEvenKConst, we also set IsEvenMNConst to false to reduce number of templates.
198	                                // If Is_local, set Is_causal to false
199	                                auto kernel = &flash_fwd_splitkv_stage1_kernel<Kernel_traits, Is_causal, Is_local && !Is_causal, Has_alibi, IsEvenMNConst && !Append_KV && IsEvenKConst && !Is_local && Kernel_traits::kHeadDim <= 128, IsEvenKConst, Is_softcap, Split, Append_KV>;
200	                                if (smem_size >= 48 * 1024) {
201	                                    C10_CUDA_CHECK(cudaFuncSetAttribute(
202	                                        kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
203	                                }
204	                                kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
205	                                C10_CUDA_KERNEL_LAUNCH_CHECK();
206	                            }
207	                        }
208	                    }
209	                }
210	            }
211	        });
212	    });
213	}
214	
215	template<typename T, int Headdim, bool Is_causal>
216	void run_mha_fwd_splitkv_dispatch(Flash_fwd_params &params, cudaStream_t stream) {
217	    if (params.blockmask == nullptr) {
218	        constexpr static int kBlockM = 64;  // Fixed for all head dimensions
219	        // TD [2023-08-28]: nvcc segfaults for headdim 96 with block size 64 x 256,
220	        // and for headdim 192 with block size 64 x 128.
221	        // Also for headdim 160 with block size 64 x 128 after the rotary addition.
222	        constexpr static int kBlockN = Headdim <= 64 ? 256 : (Headdim <= 128 ? 128 : 64);
223	        if (params.m_block_dim == 1) {
224	            run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 4, false, false, T>, Is_causal>(params, stream);
225	        } else {
226	            run_flash_splitkv_fwd_stage1<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_causal>(params, stream);
227	        }
228	    } else if (params.cu_seqlens_q != nullptr) {
229	        constexpr static int kBlockM = 16;
230	        constexpr static int kBlockN = 64;
231	        run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 1, false, false, T>, Is_causal>(params, stream);
232	    } else {
233	        constexpr static int kBlockM = 64;
234	        constexpr static int kBlockN = 64;
235	        run_flash_splitkv_fwd<Flash_fwd_kernel_traits<Headdim, kBlockM, kBlockN, 4, false, false, T>, Is_causal>(params, stream);
236	    }
237	}
238	
239	template<typename T, bool Is_causal>
240	void run_mha_fwd_hdim32(Flash_fwd_params &params, cudaStream_t stream) {
241	    constexpr static int Headdim = 32;
242	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
243	        run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
244	    });
245	}
246	
247	template<typename T, bool Is_causal>
248	void run_mha_fwd_hdim64(Flash_fwd_params &params, cudaStream_t stream) {
249	    constexpr static int Headdim = 64;
250	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
251	        if constexpr(!Is_dropout) {
252	            // Using 8 warps is 18% slower for seqlen=2k, 2 warps is 5% slower
253	            // Using block size (64 x 256) is 27% slower for seqlen=2k
254	            // Using block size (256 x 64) is 85% slower for seqlen=2k, because of register spilling
255	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
256	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
257	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
258	        } else {
259	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
260	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
261	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
262	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
263	        }
264	    });
265	}
266	
267	template<typename T, bool Is_causal>
268	void run_mha_fwd_hdim96(Flash_fwd_params &params, cudaStream_t stream) {
269	    constexpr static int Headdim = 96;
270	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
271	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
272	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
273	        // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
274	        if (is_sm8x) {
275	            if constexpr(!Is_causal) {
276	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
277	            } else {
278	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
279	            }
280	        } else {
281	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
282	        }
283	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
284	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
285	        // These two are always slower
286	        // run_flash_fwd<Flash_fwd_kernel_traits<96, 128, 128, 4, true, T>>(params, stream);
287	        // run_flash_fwd<Flash_fwd_kernel_traits<96, 64, 128, 4, true, T>>(params, stream);
288	    });
289	}
290	
291	template<typename T, bool Is_causal>
292	void run_mha_fwd_hdim128(Flash_fwd_params &params, cudaStream_t stream) {
293	    constexpr static int Headdim = 128;
294	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
295	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
296	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
297	        if constexpr(!Is_dropout) {
298	            // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
299	            // and 128 x 32 (48 KB smem) is the fastest for non-causal since we get 2 CTAs per SM.
300	            if (is_sm8x) {
301	                if constexpr(!Is_causal) {
302	                    run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
303	                } else {
304	                    run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
305	                }
306	            } else {
307	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
308	            }
309	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
310	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
311	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
312	            // Using 8 warps (128 x 128 and 256 x 64) is 28% slower for seqlen=2k
313	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
314	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
315	            // 1st ones are good for H100, A100
316	            // 2nd one is good for A6000 bc we get slightly better occupancy
317	        } else {
318	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 16, 64, 1, false, false, T>, Is_dropout, Is_causal>(params, stream);
319	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
320	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, true, false, T>, Is_dropout, Is_causal>(params, stream);
321	            // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, true, true, T>, Is_dropout, Is_causal>(params, stream);
322	        }
323	    });
324	}
325	
326	template<typename T, bool Is_causal>
327	void run_mha_fwd_hdim160(Flash_fwd_params &params, cudaStream_t stream) {
328	    constexpr static int Headdim = 160;
329	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
330	    bool is_sm8x = cc_major == 8 && cc_minor > 0;
331	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
332	        // For A100, H100, 128 x 32 is the fastest.
333	        // For sm86 or sm89, 64 x 64 is the fastest for causal (because it's square),
334	        // and 128 x 64 with 8 warps is the fastest for non-causal.
335	        if (is_sm8x) {
336	            if constexpr(!Is_causal) {
337	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
338	            } else {
339	                run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
340	            }
341	        } else {
342	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
343	        }
344	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 4, false, true, T>, Is_dropout, Is_causal>(params, stream);
345	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
346	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, T>>(params, stream);
347	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, T>>(params, stream);
348	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, T>>(params, stream);
349	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, T>>(params, stream);
350	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, T>>(params, stream);
351	    });
352	}
353	
354	template<typename T, bool Is_causal>
355	void run_mha_fwd_hdim192(Flash_fwd_params &params, cudaStream_t stream) {
356	    constexpr static int Headdim = 192;
357	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
358	        if constexpr(!Is_dropout) {
359	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
360	        } else {
361	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
362	        }
363	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
364	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
365	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 4, false, T>>(params, stream);
366	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 128, 4, false, T>>(params, stream);
367	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 128, 8, false, T>>(params, stream);
368	    });
369	}
370	
371	template<typename T, bool Is_causal>
372	void run_mha_fwd_hdim256(Flash_fwd_params &params, cudaStream_t stream) {
373	    constexpr static int Headdim = 256;
374	    int device;
375	    cudaGetDevice(&device);
376	    int max_smem_per_sm, max_smem_per_block;
377	    cudaError status_ = cudaDeviceGetAttribute(
378	        &max_smem_per_sm, cudaDevAttrMaxSharedMemoryPerMultiprocessor, device);
379	    status_ = cudaDeviceGetAttribute(
380	        &max_smem_per_block, cudaDevAttrMaxSharedMemoryPerBlockOptin, device);
381	    if (status_ != cudaSuccess) {
382	      C10_CUDA_CHECK(status_);
383	    }
384	    // printf("max_smem_per_sm = %d, max_smem_per_block = %d\n", max_smem_per_sm, max_smem_per_block);
385	    DROPOUT_SWITCH(params.p_dropout < 1.f, Is_dropout, [&] {
386	        // For A100, we want to run with 128 x 64 (128KB smem).
387	        // For H100 we want to run with 64 x 64 (96KB smem) since then we can get 2 CTAs per SM.
388	        if (max_smem_per_block >= 2 * Headdim * (128 + 2 * 64) && max_smem_per_sm < 4 * Headdim * (64 + 2 * 64)) {
389	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 64, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
390	        } else {
391	            run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 64, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
392	        }
393	        // 64 KB
394	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 64, 32, 4, false, false, T>, Is_dropout, Is_causal>(params, stream);
395	        // 96 KB
396	        // run_flash_fwd<Flash_fwd_kernel_traits<Headdim, 128, 32, 8, false, false, T>, Is_dropout, Is_causal>(params, stream);
397	    });
398	}
399
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h"
}
```

> TOOL

tool_result Read
```
File content (28105 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h"
}
```

> TOOL

tool_result Read
```
1	#pragma once
2	
3	namespace flash {
4	
5	class fwdIterator{
6	    public:
7	    template<typename Params, typename BlockInfo>
8	    __device__ fwdIterator(const Params &params, const BlockInfo &binfo, const int kBlockM, const int kBlockN, const int batch_idx, const int head_idx, const int loop_step_idx, int n_block_min, int n_block_max) {//row first
9	        if (params.blockmask == nullptr) {
10	            blockmask_ptr = nullptr;
11	            return;
12	        }
13	        this->cache_seqlen_k = binfo.actual_seqlen_k - binfo.actual_seqlen_q / params.m_block_dim;
14	        this->max_block_idx = cute::ceil_div(binfo.actual_seqlen_k, params.n_block_dim);
15	        this->m_block_dim = params.m_block_dim;
16	        this->n_block_dim = params.n_block_dim;
17	        this->n_block_min = n_block_min;
18	        this->n_block_max = n_block_max;
19	        this->batch_idx = batch_idx;  // Store batch_idx for debugging
20	        this->head_idx = head_idx;
21	
22	        // Calculate the offset for the uint64 blockmask 
23	        const int num_blocks_m = params.num_blocks_m;
24	        const int num_blocks_n = params.num_blocks_n;
25	        const int uint64_per_row = (num_blocks_n + 64 - 1) / 64;
26	        const int row_offset = params.cu_seqlens_q != nullptr ? binfo.blockmask_q_offset(m_block_dim, batch_idx) : batch_idx * params.num_k_heads * params.num_blocks_m;
27	
28	        blockmask_ptr = params.blockmask + 
29	                        head_idx * params.num_blocks_m * uint64_per_row + 
30	                        row_offset * uint64_per_row +
31	                        loop_step_idx * uint64_per_row;
32	
33	        // printf("blockmask_ptr = %d\n", blockmask_ptr);
34	
35	        const int q_block_idx = loop_step_idx + cache_seqlen_k;
36	    }
37	
38	    __device__ int max_no_larger(int target) const {
39	        if (blockmask_ptr == nullptr){
40	            // printf("blockmask_ptr is nullptr\n");
41	            return target;
42	        }
43	        // printf("blockmask_ptr is NOT!!!! nullptr\n");
44	        if(max_block_idx == 0){
45	            return -1;
46	        };
47	        
48	        
49	        // 目标值不能超过最大块索引
50	        target = min(target, max_block_idx - 1);
51	        
52	        // 计算相对于当前q_bit_position的实际位置
53	        int target_bit_pos = target;
54	        
55	        // 确定此块在哪个uint64中
56	        int uint64_offset = target_bit_pos / 64;
57	        
58	        // 确定此块在uint64中的哪一位
59	        int bit_pos = target_bit_pos % 64;
60	        
61	        // 创建一个掩码，保留target及更低位的所有位
62	        uint64_t mask = bit_pos != 63 ? (1ULL << (bit_pos + 1)) - 1 : 0xFFFFFFFFFFFFFFFFULL;
63	        
64	        // 检查当前uint64中target及以下的位
65	        uint64_t value = blockmask_ptr[uint64_offset] & mask;
66	        
67	        // 如果当前uint64中有设置的位
68	        int result = -1;
69	        if (value != 0) {
70	            // 找到最高位的1（即不大于target的最大设置位）
71	            int highest_bit = 63 - __clzll(value);  // __clzll计算前导0的数量
72	            result = highest_bit + (uint64_offset * 64);
73	        } else {
74	            // 如果当前uint64中没有找到，检查更低的uint64块
75	            for (int i = uint64_offset - 1; i >= 0; i--) {
76	                value = blockmask_ptr[i];
77	                if (value != 0) {
78	                    // 找到最高位的1
79	                    int highest_bit = 63 - __clzll(value);
80	                    // 计算相对于q_bit_position的偏移
81	                    result = highest_bit + (i * 64);
82	                    break;
83	                }
84	            }
85	        }
86	
87	        
88	        // 没有找到设置位
89	        return result;
90	    }
91	
92	    uint64_t *blockmask_ptr;
93	    int row_offset; // 行偏移量
94	    int uint64_per_row;          // 每行使用的uint64数量
95	    int cache_seqlen_k;
96	    int max_block_idx;
97	    int m_block_dim, n_block_dim;
98	    int n_block_min, n_block_max;
99	    int batch_idx, head_idx;
100	};
101	
102	class bwdIterator{
103	    public:
104	    template<typename Params, typename BlockInfo>
105	    __device__ bwdIterator(const Params &params, const BlockInfo &binfo, const int kBlockM, const int kBlockN, const int batch_idx, const int head_idx, const int loop_step_idx, int m_block_min, int m_block_max) {
106	        if (params.blockmask == nullptr) {
107	            blockmask_ptr = nullptr;
108	            return;
109	        }
110	        this -> max_block_idx = cute::ceil_div(binfo.actual_seqlen_q, params.m_block_dim);
111	        this -> m_block_dim = params.m_block_dim;
112	        this -> n_block_dim = params.n_block_dim;
113	        this -> m_block_min = m_block_min;
114	        this -> m_block_max = m_block_max;
115	
116	        this -> loop_step_idx = loop_step_idx;
117	            
118	
119	        // 计算块的基本信息
120	        const int blocks_per_uint64 = 64;  // 每个uint64可以存储64个块信息
121	        
122	        // 原始行块的索引起始位置（考虑批次位置）
123	        const int q_block_offset = binfo.blockmask_q_offset(m_block_dim, batch_idx);
124	        
125	        // 计算q_block_offset在uint64表示中的位置
126	        const int q_uint64_idx = q_block_offset / blocks_per_uint64;  // 确定在第几个uint64
127	        const int q_bit_position = q_block_offset % blocks_per_uint64; // 确定在uint64中的第几位
128	        
129	        // 列块的索引（循环步进位置）
130	        const int k_block_idx = loop_step_idx;
131	        
132	        // 计算每行需要多少个uint64来表示
133	        const int num_blocks_m = params.num_blocks_m;
134	        const int uint64_per_row = (num_blocks_m + blocks_per_uint64 - 1) / blocks_per_uint64;
135	        
136	        // 确保这里用的是num_blocks_n而不是num_blocks_m，以匹配前向传播中的计算方式
137	        this->blockmask_ptr = params.blockmask + 
138	                            head_idx * params.num_blocks_n * uint64_per_row + 
139	                            k_block_idx * uint64_per_row +
140	                            q_uint64_idx;
141	        
142	        // 存储块在uint64中的位偏移
143	        this->q_bit_position = q_bit_position;
144	        
145	        // 存储每行使用的uint64数量，用于计算偏移
146	        this->uint64_per_row = uint64_per_row;
147	    };
148	
149	    __device__ int max_no_larger(int target) const {
150	        if (blockmask_ptr == nullptr) {
151	            return target;
152	        }
153	        if(max_block_idx == 0){
154	            return -1;
155	        };
156	        
157	        // 目标值不能超过最大块索引
158	        target = min(target, max_block_idx - 1);
159	        
160	        
161	        // 接下来检查blockmask
162	        const int blocks_per_uint64 = 64;
163	        int target_bit_pos = q_bit_position + target;
164	        
165	        // 确定此块在哪个uint64中
166	        int uint64_offset = target_bit_pos / blocks_per_uint64;
167	        
168	        // 确定此块在uint64中的哪一位
169	        int bit_pos = target_bit_pos % blocks_per_uint64;
170	        
171	        // 创建一个掩码，保留target及更低位的所有位
172	        uint64_t mask = (1ULL << (bit_pos + 1)) - 1;
173	        
174	        // 检查当前uint64中target及以下的位
175	        uint64_t value = blockmask_ptr[uint64_offset] & mask;
176	        int blockmask_result = -1;
177	        
178	        if (value != 0) {
179	            // 找到最高位的1（即不大于target的最大设置位）
180	            int highest_bit = 63 - __clzll(value);  // __clzll计算前导0的数量
181	            blockmask_result = highest_bit + (uint64_offset * blocks_per_uint64) - q_bit_position;
182	        } else {
183	            // 如果当前uint64中没有找到，检查更低的uint64块
184	            for (int i = uint64_offset - 1; i >= 0; i--) {
185	                value = blockmask_ptr[i];
186	                if (value != 0) {
187	                    // 找到最高位的1
188	                    int highest_bit = 63 - __clzll(value);
189	                    // 计算相对于q_bit_position的偏移
190	                    blockmask_result = highest_bit + (i * blocks_per_uint64) - q_bit_position;
191	                    break;
192	                }
193	            }
194	        }
195	
196	        // 返回blockmask结果
197	        return blockmask_result;
198	    };
199	
200	
201	    uint64_t *blockmask_ptr;
202	    int q_bit_position;
203	    int uint64_per_row;
204	    int max_block_idx;
205	    int m_block_dim, n_block_dim;
206	    int m_block_min, m_block_max;
207	    int batch_idx, head_idx;
208	    int loop_step_idx;
209	};
210	
211	}  // namespace flash
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include <cuda.h>
8	#include <vector>
9	
10	#include <ATen/cuda/CUDAGeneratorImpl.h> // For at::Generator and at::PhiloxCudaState
11	
12	constexpr int TOTAL_DIM = 0;
13	constexpr int H_DIM = 1;
14	constexpr int D_DIM = 2;
15	
16	////////////////////////////////////////////////////////////////////////////////////////////////////
17	
18	struct Qkv_params {
19	    using index_t = int64_t;
20	    // The QKV matrices.
21	    void *__restrict__ q_ptr;
22	    void *__restrict__ k_ptr;
23	    void *__restrict__ v_ptr;
24	
25	    // The stride between rows of the Q, K and V matrices.
26	    index_t q_batch_stride;
27	    index_t k_batch_stride;
28	    index_t v_batch_stride;
29	    index_t q_row_stride;
30	    index_t k_row_stride;
31	    index_t v_row_stride;
32	    index_t q_head_stride;
33	    index_t k_head_stride;
34	    index_t v_head_stride;
35	
36	    // The number of heads.
37	    int h, h_k;
38	    // In the case of multi-query and grouped-query attention (MQA/GQA), nheads_k could be
39	    // different from nheads (query).
40	    int h_h_k_ratio; // precompute h / h_k,
41	};
42	
43	////////////////////////////////////////////////////////////////////////////////////////////////////
44	
45	struct Flash_fwd_params : public Qkv_params {
46	
47	    // The O matrix (output).
48	    void * __restrict__ o_ptr;
49	    void * __restrict__ oaccum_ptr;
50	
51	    // The stride between rows of O.
52	    index_t o_batch_stride;
53	    index_t o_row_stride;
54	    index_t o_head_stride;
55	
56	    // The pointer to the P matrix.
57	    void * __restrict__ p_ptr;
58	
59	    // The pointer to the softmax sum.
60	    void * __restrict__ softmax_lse_ptr;
61	    void * __restrict__ softmax_lseaccum_ptr;
62	
63	    // The dimensions.
64	    int b, seqlen_q, seqlen_k, seqlen_v, seqlen_knew, seqlen_vnew, d, seqlen_q_rounded, seqlen_k_rounded, d_rounded, rotary_dim, total_q;
65	
66	    // The scaling factors for the kernel.
67	    float scale_softmax;
68	    float scale_softmax_log2;
69	
70	    // array of length b+1 holding starting offset of each sequence.
71	    int * __restrict__ cu_seqlens_q;
72	    int * __restrict__ cu_seqlens_k;
73	    int * __restrict__ cu_seqlens_v;
74	    int * __restrict__ leftpad_k;
75	    int * __restrict__ leftpad_v;
76	
77	    // If provided, the actual length of each k sequence.
78	    int * __restrict__ seqused_k;
79	    int * __restrict__ seqused_v;
80	    uint64_t *__restrict__ blockmask;
81	    int m_block_dim, n_block_dim, num_k_heads;
82	    int num_blocks_m, num_blocks_n;
83	
84	    // The K_new and V_new matrices.
85	    void * __restrict__ knew_ptr;
86	    void * __restrict__ vnew_ptr;
87	
88	    // The stride between rows of the Q, K and V matrices.
89	    index_t knew_batch_stride;
90	    index_t vnew_batch_stride;
91	    index_t knew_row_stride;
92	    index_t vnew_row_stride;
93	    index_t knew_head_stride;
94	    index_t vnew_head_stride;
95	
96	    // The cos and sin matrices for rotary embedding.
97	    void * __restrict__ rotary_cos_ptr;
98	    void * __restrict__ rotary_sin_ptr;
99	
100	    // The indices to index into the KV cache.
101	    int * __restrict__ cache_batch_idx;
102	
103	    // Paged KV cache
104	    int * __restrict__ block_table;
105	    index_t block_table_batch_stride;
106	    int page_block_size;
107	
108	    // The dropout probability (probability of keeping an activation).
109	    float p_dropout;
110	    // uint32_t p_dropout_in_uint;
111	    // uint16_t p_dropout_in_uint16_t;
112	    uint8_t p_dropout_in_uint8_t;
113	
114	    // Scale factor of 1 / (1 - p_dropout).
115	    float rp_dropout;
116	    float scale_softmax_rp_dropout;
117	
118	    // Local window size
119	    int window_size_left, window_size_right;
120	    float softcap;
121	
122	    // Random state.
123	    at::PhiloxCudaState philox_args;
124	
125	    // Pointer to the RNG seed (idx 0) and offset (idx 1).
126	    uint64_t * rng_state;
127	
128	    bool is_bf16;
129	    bool is_causal;
130	
131	    // If is_seqlens_k_cumulative, then seqlen_k is cu_seqlens_k[bidb + 1] - cu_seqlens_k[bidb].
132	    // Otherwise it's cu_seqlens_k[bidb], i.e., we use cu_seqlens_k to store the sequence lengths of K.
133	    bool is_seqlens_k_cumulative;
134	    
135	    // If is_seqlens_v_cumulative, then seqlen_v is cu_seqlens_v[bidb + 1] - cu_seqlens_v[bidb].
136	    // Otherwise it's cu_seqlens_v[bidb], i.e., we use cu_seqlens_v to store the sequence lengths of V.
137	    bool is_seqlens_v_cumulative;
138	
139	    bool is_rotary_interleaved;
140	
141	    int num_splits;  // For split-KV version
142	
143	    void * __restrict__ alibi_slopes_ptr;
144	    index_t alibi_slopes_batch_stride;
145	
146	    bool unpadded_lse;  // For varlen paths: LSE is in [nheads, total_seqlen_q] format instead of [b, nheads, seqlen_q].
147	    bool seqlenq_ngroups_swapped;  // q has been transposed from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d).
148	};
149	
150	////////////////////////////////////////////////////////////////////////////////////////////////////
151	
152	struct Flash_bwd_params : public Flash_fwd_params {
153	
154	    // The dO and dQKV matrices.
155	    void *__restrict__ do_ptr;
156	    void *__restrict__ dq_ptr;
157	    void *__restrict__ dk_ptr;
158	    void *__restrict__ dv_ptr;
159	
160	    // To accumulate dQ
161	    void *__restrict__ dq_accum_ptr;
162	    void *__restrict__ dk_accum_ptr;
163	    void *__restrict__ dv_accum_ptr;
164	
165	    // // To accumulate dK and dV in case we're splitting the bwd along seqlen_q
166	    // dimension void *__restrict__ dk_accum_ptr; void *__restrict__
167	    // dv_accum_ptr;
168	
169	    // The stride between rows of the dO, dQ, dK and dV matrices.
170	    // TD [2022-04-16]: We're using 32-bit indexing to save registers.
171	    // The code probably won't work for arrays larger than 2GB.
172	    index_t do_batch_stride;
173	    index_t do_row_stride;
174	    index_t do_head_stride;
175	    index_t dq_batch_stride;
176	    index_t dk_batch_stride;
177	    index_t dv_batch_stride;
178	    index_t dq_row_stride;
179	    index_t dk_row_stride;
180	    index_t dv_row_stride;
181	    index_t dq_head_stride;
182	    index_t dk_head_stride;
183	    index_t dv_head_stride;
184	
185	    // The pointer to the softmax d sum.
186	    void *__restrict__ dsoftmax_sum;
187	
188	    bool deterministic;
189	    index_t dq_accum_split_stride;
190	};
191	
192	////////////////////////////////////////////////////////////////////////////////////////////////////
193	
194	template<typename T, int Headdim, bool Is_causal> void run_mha_fwd_(Flash_fwd_params &params, cudaStream_t stream);
195	template<typename T, int Headdim, bool Is_causal> void run_mha_fwd_splitkv_dispatch(Flash_fwd_params &params, cudaStream_t stream);
196	
197	template<typename T, int Headdim, bool Is_causal> void run_mha_bwd_(Flash_bwd_params &params, cudaStream_t stream);
198
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/block_info.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	namespace flash {
8	
9	////////////////////////////////////////////////////////////////////////////////////////////////////
10	
11	template<bool Varlen=true>
12	struct BlockInfo {
13	
14	    template<typename Params>
15	    __device__ BlockInfo(const Params &params, const int bidb)
16	        : sum_s_q(!Varlen || params.cu_seqlens_q == nullptr ? -1 : params.cu_seqlens_q[bidb])
17	        , sum_s_k(!Varlen || params.cu_seqlens_k == nullptr || !params.is_seqlens_k_cumulative ? -1 : params.cu_seqlens_k[bidb])
18	        , sum_s_v(!Varlen || params.cu_seqlens_v == nullptr || !params.is_seqlens_v_cumulative ? -1 : params.cu_seqlens_v[bidb])
19	        , actual_seqlen_q(!Varlen || params.cu_seqlens_q == nullptr ? params.seqlen_q : params.cu_seqlens_q[bidb + 1] - sum_s_q)
20	        // If is_seqlens_k_cumulative, then seqlen_k is cu_seqlens_k[bidb + 1] - cu_seqlens_k[bidb].
21	        // Otherwise it's cu_seqlens_k[bidb], i.e., we use cu_seqlens_k to store the sequence lengths of K.
22	        , leftpad_k(params.leftpad_k == nullptr ? 0 : params.leftpad_k[bidb])
23	        , seqlen_k_cache((!Varlen || params.cu_seqlens_k == nullptr ? params.seqlen_k : (params.is_seqlens_k_cumulative ? params.cu_seqlens_k[bidb + 1] - sum_s_k : params.cu_seqlens_k[bidb])) - leftpad_k)
24	        , actual_seqlen_k(params.seqused_k ? params.seqused_k[bidb] - leftpad_k : seqlen_k_cache + (params.knew_ptr == nullptr ? 0 : params.seqlen_knew))
25	        // If is_seqlens_v_cumulative, then seqlen_v is cu_seqlens_v[bidb + 1] - cu_seqlens_v[bidb].
26	        // Otherwise it's cu_seqlens_v[bidb], i.e., we use cu_seqlens_v to store the sequence lengths of V.
27	        , leftpad_v(params.leftpad_v == nullptr ? 0 : params.leftpad_v[bidb])
28	        , seqlen_v_cache((!Varlen || params.cu_seqlens_v == nullptr ? params.seqlen_v : (params.is_seqlens_v_cumulative ? params.cu_seqlens_v[bidb + 1] - sum_s_v : params.cu_seqlens_v[bidb])) - leftpad_v)
29	        , actual_seqlen_c(params.seqused_v ? params.seqused_v[bidb] - leftpad_v : seqlen_v_cache + (params.vnew_ptr == nullptr ? 0 : params.seqlen_vnew))
30	        {
31	        }
32	
33	    template <typename index_t>
34	    __forceinline__ __device__ index_t q_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
35	        return sum_s_q == -1 ? bidb * batch_stride : uint32_t(sum_s_q) * row_stride;
36	    }
37	
38	    template <typename index_t>
39	    __forceinline__ __device__ index_t k_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
40	        return sum_s_k == -1 ? bidb * batch_stride + leftpad_k * row_stride : uint32_t(sum_s_k + leftpad_k) * row_stride;
41	    }
42	
43	    template <typename index_t>
44	    __forceinline__ __device__ index_t v_offset(const index_t batch_stride, const index_t row_stride, const int bidb) const {
45	        return sum_s_v == -1 ? bidb * batch_stride + leftpad_v * row_stride : uint32_t(sum_s_v + leftpad_v) * row_stride;
46	    }
47	
48	
49	    template <typename index_t>
50	    inline __device__ index_t blockmask_q_offset(const index_t m_block_dim, const int bidb) const {
51	        return sum_s_q == -1 ? bidb * (actual_seqlen_q / m_block_dim) : uint32_t(sum_s_q) / m_block_dim;
52	    }
53	
54	    const int sum_s_q;
55	    const int sum_s_k;
56	    const int sum_s_v;
57	    const int actual_seqlen_q;
58	    // We have to have seqlen_k_cache declared before actual_seqlen_k, otherwise actual_seqlen_k is set to 0.
59	    const int leftpad_k;
60	    const int seqlen_k_cache;
61	    const int actual_seqlen_k;
62	    // We have to have seqlen_v_cache declared before actual_seqlen_c, otherwise actual_seqlen_c is set to 0.
63	    const int leftpad_v;
64	    const int seqlen_v_cache;
65	    const int actual_seqlen_c;
66	};
67	
68	////////////////////////////////////////////////////////////////////////////////////////////////////
69	
70	}  // namespace flash
71
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	// Include these 2 headers instead of torch/extension.h since we don't need all of the torch headers.
6	#include <torch/python.h>
7	#include <torch/nn/functional.h>
8	#include <c10/cuda/CUDAGuard.h>
9	#include <c10/cuda/CUDAStream.h>
10	#include <ATen/cuda/CUDAGeneratorImpl.h>  // For at::Generator and at::PhiloxCudaState
11	#include "philox_unpack.cuh"  // For at::cuda::philox::unpack
12	
13	#include <cutlass/numeric_types.h>
14	
15	#include "hardware_info.h"
16	#include "flash.h"
17	#include "static_switch.h"
18	
19	#define CHECK_DEVICE(x) TORCH_CHECK(x.is_cuda(), #x " must be on CUDA")
20	#define CHECK_SHAPE(x, ...) TORCH_CHECK(x.sizes() == torch::IntArrayRef({__VA_ARGS__}), #x " must have shape (" #__VA_ARGS__ ")")
21	#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
22	
23	
24	void set_params_fprop(Flash_fwd_params &params,
25	                      // sizes
26	                      const size_t b,
27	                      const size_t seqlen_q,
28	                      const size_t seqlen_k,
29	                      const size_t seqlen_q_rounded,
30	                      const size_t seqlen_k_rounded,
31	                      const size_t h,
32	                      const size_t h_k,
33	                      const size_t d,
34	                      const size_t d_rounded,
35	                      // device pointers
36	                      const at::Tensor q,
37	                      const at::Tensor k,
38	                      const at::Tensor v,
39	                      at::Tensor out,
40	                      void *cu_seqlens_q_d,
41	                      void *cu_seqlens_k_d,
42	                      void *seqused_k,
43	                      void *p_d,
44	                      void *softmax_lse_d,
45	                      float p_dropout,
46	                      float softmax_scale,
47	                      int window_size_left,
48	                      int window_size_right,
49	                      const float softcap,
50	                      bool seqlenq_ngroups_swapped=false,
51	                      const bool unpadded_lse=false) {
52	
53	    // Reset the parameters
54	    params = {};
55	
56	    params.is_bf16 = q.dtype() == torch::kBFloat16;
57	
58	    // Set the pointers and strides.
59	    params.q_ptr = q.data_ptr();
60	    params.k_ptr = k.data_ptr();
61	    params.v_ptr = v.data_ptr();
62	    // All stride are in elements, not bytes.
63	    params.q_row_stride = q.stride(-3);
64	    params.k_row_stride = k.stride(-3);
65	    params.v_row_stride = v.stride(-3);
66	    params.q_head_stride = q.stride(-2);
67	    params.k_head_stride = k.stride(-2);
68	    params.v_head_stride = v.stride(-2);
69	    params.o_ptr = out.data_ptr();
70	    params.o_row_stride = params.o_ptr ? out.stride(-3) : 0;
71	    params.o_head_stride = params.o_ptr ? out.stride(-2) : 0;
72	
73	    if (cu_seqlens_q_d == nullptr) {
74	        params.q_batch_stride = q.stride(0);
75	        params.k_batch_stride = k.stride(0);
76	        params.v_batch_stride = v.stride(0);
77	        params.o_batch_stride = params.o_ptr ? out.stride(0) : 0;
78	        if (seqlenq_ngroups_swapped) {
79	             params.q_batch_stride *= seqlen_q;
80	             params.o_batch_stride *= seqlen_q;
81	        }
82	    }
83	
84	    params.cu_seqlens_q = static_cast<int *>(cu_seqlens_q_d);
85	    params.cu_seqlens_k = static_cast<int *>(cu_seqlens_k_d);
86	    params.seqused_k = static_cast<int *>(seqused_k);
87	
88	    // P = softmax(QK^T)
89	    params.p_ptr = p_d;
90	
91	    // Softmax sum
92	    params.softmax_lse_ptr = softmax_lse_d;
93	
94	    // Set the dimensions.
95	    params.b = b;
96	    params.h = h;
97	    params.h_k = h_k;
98	    params.h_h_k_ratio = h / h_k;
99	    params.seqlen_q = seqlen_q;
100	    params.seqlen_k = seqlen_k;
101	    params.seqlen_q_rounded = seqlen_q_rounded;
102	    params.seqlen_k_rounded = seqlen_k_rounded;
103	    params.d = d;
104	    params.d_rounded = d_rounded;
105	
106	    // Set the different scale values.
107	    #ifdef FLASHATTENTION_DISABLE_SOFTCAP
108	        TORCH_CHECK(softcap <= 0.0, "This flash attention build does not support softcap.");
109	    #endif
110	    if (softcap > 0.0) {
111	        params.softcap = softmax_scale / softcap;
112	        params.scale_softmax = softcap;
113	        params.scale_softmax_log2 = softcap * M_LOG2E;
114	    } else{
115	        // Remove potential NaN
116	        params.softcap = 0.0;
117	        params.scale_softmax = softmax_scale;
118	        params.scale_softmax_log2 = softmax_scale * M_LOG2E;
119	    }
120	
121	    // Set this to probability of keeping an element to simplify things.
122	    params.p_dropout = 1.f - p_dropout;
123	    // Convert p from float to int so we don't have to convert the random uint to float to compare.
124	    // [Minor] We want to round down since when we do the comparison we use <= instead of <
125	    // params.p_dropout_in_uint = uint32_t(std::floor(params.p_dropout * 4294967295.0));
126	    // params.p_dropout_in_uint16_t = uint16_t(std::floor(params.p_dropout * 65535.0));
127	    params.p_dropout_in_uint8_t = uint8_t(std::floor(params.p_dropout * 255.0));
128	    params.rp_dropout = 1.f / params.p_dropout;
129	    params.scale_softmax_rp_dropout = params.rp_dropout * params.scale_softmax;
130	    TORCH_CHECK(p_dropout < 1.f);
131	    #ifdef FLASHATTENTION_DISABLE_DROPOUT
132	        TORCH_CHECK(p_dropout == 0.0f, "This flash attention build does not support dropout.");
133	    #endif
134	
135	    // Causal is the special case where window_size_right == 0 and window_size_left < 0.
136	    // Local is the more general case where window_size_right >= 0 or window_size_left >= 0.
137	    params.is_causal = window_size_left < 0 && window_size_right == 0;
138	
139	    if (window_size_left < 0 && window_size_right >= 0) { window_size_left = seqlen_k; }
140	    if (window_size_left >= 0 && window_size_right < 0) { window_size_right = seqlen_k; }
141	    params.window_size_left = window_size_left;
142	    params.window_size_right = window_size_right;
143	
144	    #ifdef FLASHATTENTION_DISABLE_LOCAL
145	        TORCH_CHECK(params.is_causal || (window_size_left < 0 && window_size_right < 0),
146	            "This flash attention build does not support local attention.");
147	    #endif
148	
149	    params.is_seqlens_k_cumulative = true;
150	
151	    #ifdef FLASHATTENTION_DISABLE_UNEVEN_K
152	        TORCH_CHECK(d == d_rounded, "This flash attention build does not support headdim not being a multiple of 32.");
153	    #endif
154	
155	    params.unpadded_lse = unpadded_lse;
156	    params.seqlenq_ngroups_swapped = seqlenq_ngroups_swapped;
157	}
158	
159	void set_params_dgrad(Flash_bwd_params &params,
160	                      // sizes
161	                      const size_t b,
162	                      const size_t seqlen_q,
163	                      const size_t seqlen_k,
164	                      const size_t seqlen_q_rounded,
165	                      const size_t seqlen_k_rounded,
166	                      const size_t h,
167	                      const size_t h_k,
168	                      const size_t d,
169	                      const size_t d_rounded,
170	                      // device pointers
171	                      const at::Tensor q,
172	                      const at::Tensor k,
173	                      const at::Tensor v,
174	                      const at::Tensor out,
175	                      const at::Tensor dout,
176	                      at::Tensor dq,
177	                      at::Tensor dk,
178	                      at::Tensor dv,
179	                      void *cu_seqlens_q_d,
180	                      void *cu_seqlens_k_d,
181	                      void *dq_accum_d,
182	                      void *dk_accum_d,
183	                      void *dv_accum_d,
184	                      void *softmax_lse_d,
185	                      void *dsoftmax_sum_d,
186	                      float p_dropout,
187	                      float softmax_scale,
188	                      int window_size_left,
189	                      int window_size_right,
190	                      const float softcap,
191	                      bool deterministic,
192	                      const bool unpadded_lse) {
193	
194	    set_params_fprop(params,
195	                     b, seqlen_q, seqlen_k, seqlen_q_rounded, seqlen_k_rounded, h, h_k, d, d_rounded,
196	                     q, k, v, out,
197	                     cu_seqlens_q_d,
198	                     cu_seqlens_k_d,
199	                     nullptr,
200	                     nullptr,
201	                     softmax_lse_d,
202	                     p_dropout,
203	                     softmax_scale,
204	                     window_size_left,
205	                     window_size_right,
206	                     softcap,
207	                     false, // seqlenq_ngroups_swapped
208	                     unpadded_lse);
209	
210	    // Set the pointers and strides.
211	    params.do_ptr = dout.data_ptr();
212	    params.do_row_stride = dout.stride(-3);
213	    params.do_head_stride = dout.stride(-2);
214	    params.dq_ptr = dq.data_ptr();
215	    params.dk_ptr = dk.data_ptr();
216	    params.dv_ptr = dv.data_ptr();
217	    params.dq_row_stride = dq.stride(-3);
218	    params.dk_row_stride = dk.stride(-3);
219	    params.dv_row_stride = dv.stride(-3);
220	    params.dq_head_stride = dq.stride(-2);
221	    params.dk_head_stride = dk.stride(-2);
222	    params.dv_head_stride = dv.stride(-2);
223	
224	    if (cu_seqlens_q_d == nullptr) {
225	        params.do_batch_stride = dout.stride(0);
226	        params.dq_batch_stride = dq.stride(0);
227	        params.dk_batch_stride = dk.stride(0);
228	        params.dv_batch_stride = dv.stride(0);
229	    }
230	
231	    params.dq_accum_ptr = dq_accum_d;
232	    params.dk_accum_ptr = dk_accum_d;
233	    params.dv_accum_ptr = dv_accum_d;
234	
235	    // Softmax sum
236	    params.dsoftmax_sum = dsoftmax_sum_d;
237	
238	    params.deterministic = deterministic;
239	}
240	
241	void run_mha_fwd(Flash_fwd_params &params, cudaStream_t stream, bool force_split_kernel=false) {
242	    FP16_SWITCH(!params.is_bf16, [&] {
243	        HEADDIM_SWITCH(params.d, [&] {
244	            BOOL_SWITCH(params.is_causal, Is_causal, [&] {
245	                if (params.num_splits <= 1 && !force_split_kernel) {  // If we don't set it num_splits == 0
246	                    run_mha_fwd_<elem_type, kHeadDim, Is_causal>(params, stream);
247	                } else {
248	                    run_mha_fwd_splitkv_dispatch<elem_type, kHeadDim, Is_causal>(params, stream);
249	                }
250	            });
251	        });
252	    });
253	}
254	
255	// Find the number of splits that maximizes the occupancy. For example, if we have
256	// batch * n_heads = 48 and we have 108 SMs, having 2 splits (efficiency = 0.89) is
257	// better than having 3 splits (efficiency = 0.67). However, we also don't want too many
258	// splits as that would incur more HBM reads/writes.
259	// So we find the best efficiency, then find the smallest number of splits that gets 85%
260	// of the best efficiency.
261	inline int num_splits_heuristic(int batch_nheads_mblocks, int num_SMs, int num_n_blocks, int max_splits) {
262	    // If we have enough to almost fill the SMs, then just use 1 split
263	    if (batch_nheads_mblocks >= 0.8f * num_SMs) { return 1; }
264	    max_splits = std::min({max_splits, num_SMs, num_n_blocks});
265	    float max_efficiency = 0.f;
266	    std::vector<float> efficiency;
267	    efficiency.reserve(max_splits);
268	    auto ceildiv = [](int a, int b) { return (a + b - 1) / b; };
269	    // Some splits are not eligible. For example, if we have 64 blocks and choose 11 splits,
270	    // we'll have 6 * 10 + 4 blocks. If we choose 12 splits, we'll have 6 * 11 + (-2) blocks
271	    // (i.e. it's 11 splits anyway).
272	    // So we check if the number of blocks per split is the same as the previous num_splits.
273	    auto is_split_eligible = [&ceildiv, &num_n_blocks](int num_splits) {
274	        return num_splits == 1 || ceildiv(num_n_blocks, num_splits) != ceildiv(num_n_blocks, num_splits - 1);
275	    };
276	    for (int num_splits = 1; num_splits <= max_splits; num_splits++) {
277	        if (!is_split_eligible(num_splits)) {
278	            efficiency.push_back(0.f);
279	        } else {
280	            float n_waves = float(batch_nheads_mblocks * num_splits) / num_SMs;
281	            float eff = n_waves / ceil(n_waves);
282	            // printf("num_splits = %d, eff = %f\n", num_splits, eff);
283	            if (eff > max_efficiency) { max_efficiency = eff; }
284	            efficiency.push_back(eff);
285	        }
286	    }
287	    for (int num_splits = 1; num_splits <= max_splits; num_splits++) {
288	        if (!is_split_eligible(num_splits)) { continue; }
289	        if (efficiency[num_splits - 1] >= 0.85 * max_efficiency) {
290	            // printf("num_splits chosen = %d\n", num_splits);
291	            return num_splits;
292	        }
293	    }
294	    return 1;
295	}
296	
297	std::tuple<at::Tensor, at::Tensor> set_params_splitkv(Flash_fwd_params &params, const int batch_size,
298	    const int num_heads, const int head_size, const int max_seqlen_k, const int max_seqlen_q,
299	    const int head_size_rounded, const float p_dropout,
300	    const int num_splits, const int num_sm, struct c10::TensorOptions opts) {
301	
302	    // This needs to match with run_mha_fwd_splitkv_dispatch
303	    const int block_n = head_size <= 64 ? 256 : (head_size <= 128 ? 128 : 64);
304	    const int num_n_blocks = (max_seqlen_k + block_n - 1) / block_n;
305	    // Technically kBlockM = 64 only for the splitKV kernels, not the standard kernel.
306	    // In any case we don't expect seqlen_q to be larger than 64 for inference.
307	    const int num_m_blocks = (max_seqlen_q + 64 - 1) / 64;
308	    params.num_splits = num_splits;
309	    at::Tensor softmax_lse_accum;
310	    at::Tensor out_accum;
311	
312	    if (p_dropout == 0.0f) {  // SplitKV is not implemented for dropout
313	        if (num_splits < 1) {
314	            // We multiply number of SMs by 2 to hard-code the fact that we're using 128 threads per block.
315	            params.num_splits = num_splits_heuristic(batch_size * num_heads * num_m_blocks, num_sm * 2, num_n_blocks, 128);
316	        }
317	        if (params.num_splits > 1) {
318	            softmax_lse_accum = torch::empty({params.num_splits, batch_size, num_heads, max_seqlen_q}, opts.dtype(at::kFloat));
319	            out_accum = torch::empty({params.num_splits, batch_size, num_heads, max_seqlen_q, head_size_rounded}, opts.dtype(at::kFloat));
320	            params.softmax_lseaccum_ptr = softmax_lse_accum.data_ptr();
321	            params.oaccum_ptr = out_accum.data_ptr();
322	        }
323	        TORCH_CHECK(params.num_splits <= 128, "num_splits > 128 not supported");
324	    }
325	
326	    return std::make_tuple(softmax_lse_accum, out_accum);
327	}
328	
329	void set_params_alibi(Flash_fwd_params &params, c10::optional<at::Tensor> &alibi_slopes_, int batch_size, int num_heads){
330	#ifdef FLASHATTENTION_DISABLE_ALIBI
331	    TORCH_CHECK(!alibi_slopes_.has_value(), "This flash attention build does not support alibi.");
332	    params.alibi_slopes_ptr = nullptr;
333	#else
334	    if (alibi_slopes_.has_value()) {
335	        auto alibi_slopes = alibi_slopes_.value();
336	        TORCH_CHECK(alibi_slopes.dtype() == torch::kFloat32, "ALiBi slopes must have dtype fp32");
337	        CHECK_DEVICE(alibi_slopes);
338	        TORCH_CHECK(alibi_slopes.stride(-1) == 1, "ALiBi slopes tensor must have contiguous last dimension");
339	        TORCH_CHECK(alibi_slopes.sizes() == torch::IntArrayRef({num_heads}) || alibi_slopes.sizes() == torch::IntArrayRef({batch_size, num_heads}));
340	        params.alibi_slopes_ptr = alibi_slopes.data_ptr();
341	        params.alibi_slopes_batch_stride = alibi_slopes.dim() == 2 ? alibi_slopes.stride(0) : 0;
342	    } else {
343	        params.alibi_slopes_ptr = nullptr;
344	    }
345	#endif
346	}
347	
348	std::vector<at::Tensor>
349	mha_fwd(at::Tensor &q,         // batch_size x seqlen_q x num_heads x round_multiple(head_size, 8)
350	        const at::Tensor &k,         // batch_size x seqlen_k x num_heads_k x round_multiple(head_size, 8)
351	        const at::Tensor &v,         // batch_size x seqlen_k x num_heads_k x round_multiple(head_size, 8)
352	        c10::optional<at::Tensor> &out_,             // batch_size x seqlen_q x num_heads x round_multiple(head_size, 8)
353	        c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
354	        const float p_dropout,
355	        const float softmax_scale,
356	        bool is_causal,
357	        int window_size_left,
358	        int window_size_right,
359	        const float softcap,
360	        const bool return_softmax,
361	        c10::optional<at::Generator> gen_) {
362	
363	    // Otherwise the kernel will be launched from cuda:0 device
364	    at::cuda::CUDAGuard device_guard{q.device()};
365	
366	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
367	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
368	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
369	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
370	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
371	    // We will support Turing in the near future
372	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
373	
374	    auto q_dtype = q.dtype();
375	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
376	                "FlashAttention only support fp16 and bf16 data type");
377	    if (q_dtype == torch::kBFloat16) {
378	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
379	    }
380	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
381	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
382	
383	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
384	
385	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
386	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
387	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
388	
389	    const auto sizes = q.sizes();
390	
391	    const int batch_size = sizes[0];
392	    int seqlen_q = sizes[1];
393	    int num_heads = sizes[2];
394	    const int head_size = sizes[3];
395	    const int seqlen_k = k.size(1);
396	    const int num_heads_k = k.size(2);
397	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
398	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
399	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
400	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
401	
402	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
403	
404	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
405	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
406	
407	    // causal=true is the same as causal=false in this case
408	    if (seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }
409	    if (is_causal) { window_size_right = 0; }
410	
411	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
412	    // H/t Daniel Haziza
413	    const int seqlenq_ngroups_swapped = seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
414	    const int ngroups = num_heads / num_heads_k;
415	    if (seqlenq_ngroups_swapped) {
416	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2);
417	        seqlen_q = ngroups;
418	        num_heads = num_heads_k;
419	    }
420	
421	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size);
422	    CHECK_SHAPE(k, batch_size, seqlen_k, num_heads_k, head_size);
423	    CHECK_SHAPE(v, batch_size, seqlen_k, num_heads_k, head_size);
424	
425	    at::Tensor out;
426	    if (out_.has_value()) {
427	        out = out_.value();
428	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
429	        CHECK_DEVICE(out);
430	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
431	        CHECK_SHAPE(out, batch_size, sizes[1], sizes[2], head_size);
432	        if (seqlenq_ngroups_swapped) {
433	            out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2);
434	        }
435	    } else {
436	        out = torch::empty_like(q);
437	    }
438	
439	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
440	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
441	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
442	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
443	
444	    auto opts = q.options();
445	
446	    auto softmax_lse = torch::empty({batch_size, num_heads, seqlen_q}, opts.dtype(at::kFloat));
447	    at::Tensor p;
448	    // Only return softmax if there's dropout to reduce compilation time
449	    if (return_softmax) {
450	        TORCH_CHECK(p_dropout > 0.0f, "return_softmax is only supported when p_dropout > 0.0");
451	        p = torch::empty({ batch_size, num_heads, seqlen_q_rounded, seqlen_k_rounded }, opts);
452	    }
453	    else {
454	        p = torch::empty({ 0 }, opts);
455	    }
456	
457	    Flash_fwd_params params;
458	    set_params_fprop(params,
459	                     batch_size,
460	                     seqlen_q, seqlen_k,
461	                     seqlen_q_rounded, seqlen_k_rounded,
462	                     num_heads, num_heads_k,
463	                     head_size, head_size_rounded,
464	                     q, k, v, out,
465	                     /*cu_seqlens_q_d=*/nullptr,
466	                     /*cu_seqlens_k_d=*/nullptr,
467	                     /*seqused_k=*/nullptr,
468	                     return_softmax ? p.data_ptr() : nullptr,
469	                     softmax_lse.data_ptr(),
470	                     p_dropout,
471	                     softmax_scale,
472	                     window_size_left,
473	                     window_size_right,
474	                     softcap
475	                     );
476	
477	    // Keep references to these tensors to extend their lifetime
478	    at::Tensor softmax_lse_accum, out_accum;
479	    std::tie(softmax_lse_accum, out_accum) = set_params_splitkv(
480	        params, batch_size, num_heads, head_size, seqlen_k, seqlen_q,
481	        head_size_rounded, p_dropout, /*num_splits*/ 0, get_num_sm(get_current_device()), opts);
482	
483	    // number of times random will be generated per thread, to offset philox counter in thc random
484	    // state
485	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
486	    int64_t counter_offset = params.b * params.h * 32;
487	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
488	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
489	    // Forward kernel will populate memory with the seed and offset.
490	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
491	
492	    if (p_dropout > 0.0)  {
493	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
494	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
495	        // See Note [Acquire lock when using random generators]
496	        std::lock_guard<std::mutex> lock(gen->mutex_);
497	        params.philox_args = gen->philox_cuda_state(counter_offset);
498	    }
499	
500	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
501	
502	    if (seqlen_k > 0) {
503	        auto stream = at::cuda::getCurrentCUDAStream().stream();
504	        run_mha_fwd(params, stream);
505	    } else {
506	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
507	        out.zero_();
508	        softmax_lse.fill_(std::numeric_limits<float>::infinity());
509	    }
510	
511	    if (seqlenq_ngroups_swapped) {
512	        out = out.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size});
513	        q = q.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size});
514	        softmax_lse = softmax_lse.reshape({batch_size, num_heads_k * seqlen_q, 1});
515	    }
516	    return {out, softmax_lse, p, rng_state};
517	}
518	
519	std::vector<at::Tensor>
520	mha_varlen_fwd(at::Tensor &q,  // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
521	               const at::Tensor &k,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
522	               const at::Tensor &v,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
523	               c10::optional<at::Tensor> &out_, // total_q x num_heads x head_size, total_k := \sum_{i=0}^{b} s_i
524	               const at::Tensor &cu_seqlens_q,  // b+1
525	               const at::Tensor &cu_seqlens_k,  // b+1
526	               c10::optional<at::Tensor> &seqused_k, // b. If given, only this many elements of each batch element's keys are used.
527	               c10::optional<const at::Tensor> &leftpad_k_, // batch_size
528	               c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
529	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
530	               int max_seqlen_q,
531	               const int max_seqlen_k,
532	               const float p_dropout,
533	               const float softmax_scale,
534	               const bool zero_tensors,
535	               bool is_causal,
536	               int window_size_left,
537	               int window_size_right,
538	               const float softcap,
539	               const bool return_softmax,
540	               c10::optional<at::Generator> gen_,
541	               c10::optional<at::Tensor> &blockmask_) {
542	
543	    // Otherwise the kernel will be launched from cuda:0 device
544	    at::cuda::CUDAGuard device_guard{q.device()};
545	
546	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
547	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
548	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
549	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
550	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
551	    // We will support Turing in the near future
552	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
553	
554	    auto q_dtype = q.dtype();
555	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
556	                "FlashAttention only support fp16 and bf16 data type");
557	    if (q_dtype == torch::kBFloat16) {
558	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
559	    }
560	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
561	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
562	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
563	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
564	
565	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
566	    CHECK_DEVICE(cu_seqlens_q);
567	    CHECK_DEVICE(cu_seqlens_k);
568	
569	    at::Tensor block_table;
570	    const bool paged_KV = block_table_.has_value();
571	    if (paged_KV) {
572	        block_table = block_table_.value();
573	        CHECK_DEVICE(block_table);
574	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
575	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
576	    }
577	
578	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
579	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
580	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
581	    CHECK_CONTIGUOUS(cu_seqlens_q);
582	    CHECK_CONTIGUOUS(cu_seqlens_k);
583	
584	    const auto sizes = q.sizes();
585	
586	    const int batch_size = cu_seqlens_q.numel() - 1;
587	    int num_heads = sizes[1];
588	    const int head_size = sizes[2];
589	    const int num_heads_k = paged_KV ? k.size(2) : k.size(1);
590	
591	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
592	
593	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
594	    const int num_blocks = !paged_KV ? 0 : k.size(0);
595	    const int page_block_size = !paged_KV ? 1 : k.size(1);
596	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
597	
598	    if (max_seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }  // causal=true is the same as causal=false in this case
599	    if (is_causal) { window_size_right = 0; }
600	
601	    void *cu_seqlens_q_d = cu_seqlens_q.data_ptr();
602	
603	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
604	    // H/t Daniel Haziza
605	    const int seqlenq_ngroups_swapped = max_seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
606	    const int ngroups = num_heads / num_heads_k;
607	    if (seqlenq_ngroups_swapped) {
608	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
609	        max_seqlen_q = ngroups;
610	        num_heads = num_heads_k;
611	        cu_seqlens_q_d = nullptr;
612	    }
613	
614	    const int total_q = q.sizes()[0];
615	
616	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
617	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
618	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
619	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
620	
621	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
622	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
623	
624	    CHECK_SHAPE(q, total_q, num_heads, head_size);
625	    if (!paged_KV) {
626	        const int total_k = k.size(0);
627	        CHECK_SHAPE(k, total_k, num_heads_k, head_size);
628	        CHECK_SHAPE(v, total_k, num_heads_k, head_size);
629	    } else {
630	        CHECK_SHAPE(k, num_blocks, page_block_size, num_heads_k, head_size);
631	        CHECK_SHAPE(v, num_blocks, page_block_size, num_heads_k, head_size);
632	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
633	    }
634	
635	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
636	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
637	    if (seqused_k.has_value()){
638	        auto seqused_k_ = seqused_k.value();
639	        TORCH_CHECK(seqused_k_.dtype() == torch::kInt32, "seqused_k must have dtype int32");
640	        TORCH_CHECK(seqused_k_.is_cuda(), "seqused_k must be on CUDA device");
641	        TORCH_CHECK(seqused_k_.is_contiguous(), "seqused_k must be contiguous");
642	        CHECK_SHAPE(seqused_k_, batch_size);
643	    }
644	
645	    at::Tensor out;
646	    if (out_.has_value()) {
647	        out = out_.value();
648	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
649	        CHECK_DEVICE(out);
650	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
651	        CHECK_SHAPE(out, sizes[0], sizes[1], head_size);
652	        if (seqlenq_ngroups_swapped) {
653	            out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
654	        }
655	    } else {
656	        out = torch::empty_like(q);
657	    }
658	
659	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
660	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
661	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
662	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
663	
664	    auto opts = q.options();
665	    auto softmax_lse = torch::empty({num_heads, total_q}, opts.dtype(at::kFloat));
666	    at::Tensor p;
667	    // Only return softmax if there's dropout to reduce compilation time
668	    if (return_softmax) {
669	        TORCH_CHECK(p_dropout > 0.0f, "return_softmax is only supported when p_dropout > 0.0");
670	        p = torch::empty({ batch_size, num_heads, seqlen_q_rounded, seqlen_k_rounded }, opts);
671	    }
672	    else {
673	        p = torch::empty({ 0 }, opts);
674	    }
675	
676	    if (zero_tensors) {
677	        out.zero_();
678	        softmax_lse.fill_(-std::numeric_limits<float>::infinity());
679	        if (return_softmax) {p.zero_();}
680	    }
681	
682	    Flash_fwd_params params;
683	    set_params_fprop(params,
684	                     batch_size,
685	                     max_seqlen_q, max_seqlen_k,
686	                     seqlen_q_rounded, seqlen_k_rounded,
687	                     num_heads, num_heads_k,
688	                     head_size, head_size_rounded,
689	                     q, k, v, out,
690	                     cu_seqlens_q_d,
691	                     cu_seqlens_k.data_ptr(),
692	                     seqused_k.has_value() ? seqused_k.value().data_ptr() : nullptr,
693	                     return_softmax ? p.data_ptr() : nullptr,
694	                     softmax_lse.data_ptr(),
695	                     p_dropout,
696	                     softmax_scale,
697	                     window_size_left,
698	                     window_size_right,
699	                     softcap,
700	                     seqlenq_ngroups_swapped,
701	                     /*unpadded_lse*/true);
702	    params.total_q = total_q;
703	
704	    if (blockmask_.has_value()) {
705	        params.blockmask = static_cast<uint64_t*>(blockmask_.value().data_ptr());
706	        params.m_block_dim = 16;
707	        params.n_block_dim = 64;
708	        params.num_k_heads = 2;
709	        params.num_blocks_m = (total_q + 16 - 1) / 16;
710	        params.num_blocks_n = (max_seqlen_k + 64 - 1) / 64;
711	    } else {
712	        params.blockmask = nullptr;
713	        params.m_block_dim = 1;
714	        params.n_block_dim = 1;
715	    }
716	
717	    if (paged_KV) {
718	        params.block_table = block_table.data_ptr<int>();
719	        params.block_table_batch_stride = block_table.stride(0);
720	        params.k_batch_stride = k.stride(0);
721	        params.v_batch_stride = v.stride(0);
722	    }
723	    params.page_block_size = page_block_size;
724	    // Keep references to these tensors to extend their lifetime
725	    at::Tensor softmax_lse_accum, out_accum;
726	    if (seqlenq_ngroups_swapped) {
727	        // Only apply split-k for decoding
728	        std::tie(softmax_lse_accum, out_accum) =
729	            set_params_splitkv(params, batch_size, num_heads, head_size,
730	                               max_seqlen_k, max_seqlen_q, head_size_rounded,
731	                               p_dropout, /*num_splits*/ 0, get_num_sm(get_current_device()), opts);
732	    }
733	
734	    if (leftpad_k_.has_value()) {
735	        auto leftpad_k = leftpad_k_.value();
736	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
737	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
738	        CHECK_DEVICE(leftpad_k);
739	        CHECK_CONTIGUOUS(leftpad_k);
740	        CHECK_SHAPE(leftpad_k, batch_size);
741	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
742	    }
743	
744	    // number of times random will be generated per thread, to offset philox counter in thc random
745	    // state
746	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
747	    int64_t counter_offset = params.b * params.h * 32;
748	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
749	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
750	    // Forward kernel will populate memory with the seed and offset.
751	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
752	
753	    if (p_dropout > 0.0)  {
754	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
755	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
756	        // See Note [Acquire lock when using random generators]
757	        std::lock_guard<std::mutex> lock(gen->mutex_);
758	        params.philox_args = gen->philox_cuda_state(counter_offset);
759	    }
760	
761	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
762	
763	    if (max_seqlen_k > 0) {
764	        auto stream = at::cuda::getCurrentCUDAStream().stream();
765	        params.num_splits = 1;
766	        run_mha_fwd(params, stream, paged_KV);
767	    } else {
768	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
769	        out.zero_();
770	        softmax_lse.fill_(std::numeric_limits<float>::infinity());
771	    }
772	
773	    if (seqlenq_ngroups_swapped) {
774	        int64_t size_before[] = {batch_size, max_seqlen_q, num_heads_k, head_size};
775	        int64_t size_after[] = {batch_size, num_heads_k * max_seqlen_q, head_size};
776	        out = out.reshape(size_before).transpose(1, 2).reshape(size_after);
777	        q = q.reshape(size_before).transpose(1, 2).reshape(size_after);
778	        softmax_lse = softmax_lse.reshape({num_heads * max_seqlen_q, batch_size});
779	    }
780	
781	    return {out, softmax_lse, p, rng_state};
782	}
783	
784	std::vector<at::Tensor>
785	mha_varlen_fwd_stage1(at::Tensor &q,  // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
786	               const at::Tensor &k,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
787	               const at::Tensor &v,  // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
788	               c10::optional<at::Tensor> &out_, // total_q x num_heads x head_size, total_k := \sum_{i=0}^{b} s_i
789	               const at::Tensor &cu_seqlens_q,  // b+1
790	               const at::Tensor &cu_seqlens_k,  // b+1
791	               const at::Tensor &cu_seqlens_v,  // b+1
792	               c10::optional<at::Tensor> &seqused_k, // b. If given, only this many elements of each batch element's keys are used.
793	               c10::optional<const at::Tensor> &leftpad_k_, // batch_size
794	               c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
795	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
796	               int max_seqlen_q,
797	               const int max_seqlen_k,
798	               const float p_dropout,
799	               const float softmax_scale,
800	               const bool zero_tensors,
801	               bool is_causal,
802	               int window_size_left,
803	               int window_size_right,
804	               const float softcap,
805	               const bool return_softmax,
806	               c10::optional<at::Generator> gen_) {
807	
808	    // Otherwise the kernel will be launched from cuda:0 device
809	    at::cuda::CUDAGuard device_guard{q.device()};
810	
811	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
812	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
813	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
814	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
815	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
816	    // We will support Turing in the near future
817	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
818	
819	    auto q_dtype = q.dtype();
820	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
821	                "FlashAttention only support fp16 and bf16 data type");
822	    if (q_dtype == torch::kBFloat16) {
823	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
824	    }
825	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
826	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
827	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
828	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
829	    TORCH_CHECK(cu_seqlens_v.dtype() == torch::kInt32, "cu_seqlens_v must have dtype int32");
830	
831	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
832	    CHECK_DEVICE(cu_seqlens_q);
833	    CHECK_DEVICE(cu_seqlens_k);
834	    CHECK_DEVICE(cu_seqlens_v);
835	
836	    at::Tensor block_table;
837	    const bool paged_KV = block_table_.has_value();
838	    if (paged_KV) {
839	        block_table = block_table_.value();
840	        CHECK_DEVICE(block_table);
841	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
842	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
843	    }
844	
845	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
846	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
847	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
848	    CHECK_CONTIGUOUS(cu_seqlens_q);
849	    CHECK_CONTIGUOUS(cu_seqlens_k);
850	    CHECK_CONTIGUOUS(cu_seqlens_v);
851	
852	    const auto sizes = q.sizes();
853	
854	    const int batch_size = cu_seqlens_q.numel() - 1;
855	    int num_heads = sizes[1];
856	    const int head_size = sizes[2];
857	    const int num_heads_k = paged_KV ? k.size(2) : k.size(1);
858	
859	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
860	
861	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
862	    const int num_blocks = !paged_KV ? 0 : k.size(0);
863	    const int page_block_size = !paged_KV ? 1 : k.size(1);
864	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
865	
866	    if (max_seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }  // causal=true is the same as causal=false in this case
867	    if (is_causal) { window_size_right = 0; }
868	
869	    void *cu_seqlens_q_d = cu_seqlens_q.data_ptr();
870	
871	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
872	    // H/t Daniel Haziza
873	    const int seqlenq_ngroups_swapped = max_seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && p_dropout == 0.f && head_size % 8 == 0 && !alibi_slopes_.has_value();
874	    const int ngroups = num_heads / num_heads_k;
875	    if (seqlenq_ngroups_swapped) {
876	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
877	        max_seqlen_q = ngroups;
878	        num_heads = num_heads_k;
879	        cu_seqlens_q_d = nullptr;
880	    }
881	
882	    const int total_q = q.sizes()[0];
883	
884	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
885	    TORCH_CHECK(head_size <= 256, "FlashAttention forward only supports head dimension at most 256");
886	    TORCH_CHECK(head_size % 8 == 0, "query, key, value, and out_ must have a head_size that is a multiple of 8");
887	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
888	
889	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
890	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
891	
892	    CHECK_SHAPE(q, total_q, num_heads, head_size);
893	    if (!paged_KV) {
894	        const int total_k = k.size(0);
895	        CHECK_SHAPE(k, total_k, num_heads_k, head_size);
896	        // CHECK_SHAPE(v, total_k, num_heads_k, head_size);
897	    } else {
898	        CHECK_SHAPE(k, num_blocks, page_block_size, num_heads_k, head_size);
899	        // CHECK_SHAPE(v, num_blocks, page_block_size, num_heads_k, head_size);
900	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
901	    }
902	
903	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
904	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
905	    CHECK_SHAPE(cu_seqlens_v, batch_size + 1);
906	    if (seqused_k.has_value()){
907	        auto seqused_k_ = seqused_k.value();
908	        TORCH_CHECK(seqused_k_.dtype() == torch::kInt32, "seqused_k must have dtype int32");
909	        TORCH_CHECK(seqused_k_.is_cuda(), "seqused_k must be on CUDA device");
910	        TORCH_CHECK(seqused_k_.is_contiguous(), "seqused_k must be contiguous");
911	        CHECK_SHAPE(seqused_k_, batch_size);
912	    }
913	
914	
915	    auto opts = q.options();
916	    at::Tensor out;
917	    out = torch::empty({ 0 }, opts);
918	    // if (out_.has_value()) {
919	    //     out = out_.value();
920	    //     TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
921	    //     CHECK_DEVICE(out);
922	    //     TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
923	    //     CHECK_SHAPE(out, sizes[0], sizes[1], head_size);
924	    //     if (seqlenq_ngroups_swapped) {
925	    //         out = out.reshape({batch_size, num_heads_k, ngroups, head_size}).transpose(1, 2).reshape({batch_size * ngroups, num_heads_k, head_size});
926	    //     }
927	    // } else {
928	    //     out = torch::empty_like(q);
929	    // }
930	
931	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
932	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
933	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
934	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
935	
936	    // auto softmax_lse = torch::empty({num_heads, total_q}, opts.dtype(at::kFloat));
937	    at::Tensor p;
938	    // Only return softmax if there's dropout to reduce compilation time
939	    if (return_softmax) {
940	        // Return tensor with shape (num_heads_k, total_q, max_seqlen_k)
941	        p = torch::full({ num_heads_k, total_q / 16, seqlen_k_rounded }, 0, opts);
942	    }
943	    else {
944	        p = torch::empty({ 0 }, opts);
945	    }
946	
947	    if (zero_tensors) {
948	        // out.zero_();
949	        // softmax_lse.fill_(-std::numeric_limits<float>::infinity());
950	        if (return_softmax) {p.zero_();}
951	    }
952	
953	    Flash_fwd_params params;
954	    set_params_fprop(params,
955	                     batch_size,
956	                     max_seqlen_q, max_seqlen_k,
957	                     seqlen_q_rounded, seqlen_k_rounded,
958	                     num_heads, num_heads_k,
959	                     head_size, head_size_rounded,
960	                     q, k, v, out,
961	                     cu_seqlens_q_d,
962	                     cu_seqlens_k.data_ptr(),
963	                     seqused_k.has_value() ? seqused_k.value().data_ptr() : nullptr,
964	                     return_softmax ? p.data_ptr() : nullptr,
965	                     nullptr, //softmax_lse.data_ptr(),
966	                     p_dropout,
967	                     softmax_scale,
968	                     window_size_left,
969	                     window_size_right,
970	                     softcap,
971	                     seqlenq_ngroups_swapped,
972	                     /*unpadded_lse*/true);
973	
974	    params.cu_seqlens_v = static_cast<int *>(cu_seqlens_v.data_ptr());
975	    params.is_seqlens_v_cumulative = true;  // Treat cu_seqlens_v as cumulative sequence lengths
976	    // {
977	    //     // Copy cu_seqlens_v to CPU for printing
978	    //     at::Tensor cu_seqlens_v_cpu = cu_seqlens_v.to(torch::kCPU);
979	    //     const int* cu_seqlens_v_data = cu_seqlens_v_cpu.data_ptr<int>();
980	    //     printf("params.cu_seqlens_v: ");
981	    //     for (int i = 0; i < batch_size + 1; ++i) {
982	    //         printf("%d ", cu_seqlens_v_data[i]);
983	    //     }
984	    //     printf("\n");
985	    // }
986	    params.total_q = total_q;
987	
988	    params.m_block_dim = 16;
989	    params.n_block_dim = 1;
990	
991	    if (paged_KV) {
992	        params.block_table = block_table.data_ptr<int>();
993	        params.block_table_batch_stride = block_table.stride(0);
994	        params.k_batch_stride = k.stride(0);
995	        // params.v_batch_stride = v.stride(0);
996	    }
997	    params.page_block_size = page_block_size;
998	    // Keep references to these tensors to extend their lifetime
999	
1000	
1001	    if (leftpad_k_.has_value()) {
1002	        auto leftpad_k = leftpad_k_.value();
1003	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
1004	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
1005	        CHECK_DEVICE(leftpad_k);
1006	        CHECK_CONTIGUOUS(leftpad_k);
1007	        CHECK_SHAPE(leftpad_k, batch_size);
1008	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
1009	    }
1010	
1011	    // number of times random will be generated per thread, to offset philox counter in thc random
1012	    // state
1013	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1014	    int64_t counter_offset = params.b * params.h * 32;
1015	    auto options = torch::TensorOptions().dtype(torch::kFloat32).device(torch::kCUDA);
1016	    auto rng_state = torch::empty({2}, options.dtype(torch::kInt64));
1017	    // Forward kernel will populate memory with the seed and offset.
1018	    params.rng_state = reinterpret_cast<uint64_t*>(rng_state.data_ptr());
1019	
1020	    if (p_dropout > 0.0)  {
1021	        auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1022	            gen_, at::cuda::detail::getDefaultCUDAGenerator());
1023	        // See Note [Acquire lock when using random generators]
1024	        std::lock_guard<std::mutex> lock(gen->mutex_);
1025	        params.philox_args = gen->philox_cuda_state(counter_offset);
1026	    }
1027	
1028	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1029	
1030	    if (max_seqlen_k > 0) {
1031	        auto stream = at::cuda::getCurrentCUDAStream().stream();
1032	        params.num_splits = 1;
1033	        run_mha_fwd(params, stream, paged_KV || true);
1034	    } else {
1035	        // If seqlen_k == 0, then we have an empty tensor. We need to set the output to 0.
1036	        // out.zero_();
1037	        // softmax_lse.fill_(std::numeric_limits<float>::infinity());
1038	    }
1039	
1040	    if (seqlenq_ngroups_swapped) {
1041	        int64_t size_before[] = {batch_size, max_seqlen_q, num_heads_k, head_size};
1042	        int64_t size_after[] = {batch_size, num_heads_k * max_seqlen_q, head_size};
1043	        // out = out.reshape(size_before).transpose(1, 2).reshape(size_after);
1044	        q = q.reshape(size_before).transpose(1, 2).reshape(size_after);
1045	        // softmax_lse = softmax_lse.reshape({num_heads * max_seqlen_q, batch_size});
1046	    }
1047	
1048	    return {p};
1049	}
1050	
1051	void run_mha_bwd(Flash_bwd_params &params, cudaStream_t stream) {
1052	    FP16_SWITCH(!params.is_bf16, [&] {
1053	        HEADDIM_SWITCH(params.d, [&] {
1054	            BOOL_SWITCH(params.is_causal, Is_causal, [&] {
1055	                run_mha_bwd_<elem_type, kHeadDim, Is_causal>(params, stream);
1056	            });
1057	        });
1058	    });
1059	}
1060	
1061	std::vector<at::Tensor>
1062	mha_bwd(const at::Tensor &dout,  // batch_size x seqlen_q x num_heads, x multiple_of(head_size_og, 8)
1063	        const at::Tensor &q,   // batch_size x seqlen_q x num_heads x head_size
1064	        const at::Tensor &k,   // batch_size x seqlen_k x num_heads_k x head_size
1065	        const at::Tensor &v,   // batch_size x seqlen_k x num_heads_k x head_size
1066	        const at::Tensor &out,   // batch_size x seqlen_q x num_heads x head_size
1067	        const at::Tensor &softmax_lse,     // b x h x seqlen_q
1068	        c10::optional<at::Tensor> &dq_,   // batch_size x seqlen_q x num_heads x head_size
1069	        c10::optional<at::Tensor> &dk_,   // batch_size x seqlen_k x num_heads_k x head_size
1070	        c10::optional<at::Tensor> &dv_,   // batch_size x seqlen_k x num_heads_k x head_size
1071	        c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
1072	        const float p_dropout,         // probability to drop
1073	        const float softmax_scale,
1074	        const bool is_causal,
1075	        int window_size_left,
1076	        int window_size_right,
1077	        const float softcap,
1078	        const bool deterministic,
1079	        c10::optional<at::Generator> gen_,
1080	        c10::optional<at::Tensor> &rng_state) {
1081	
1082	    #ifdef FLASHATTENTION_DISABLE_BACKWARD
1083	        TORCH_CHECK(false, "This flash attention build does not support backward.");
1084	    #endif
1085	    if (is_causal) { window_size_right = 0; }
1086	
1087	    // Otherwise the kernel will be launched from cuda:0 device
1088	    at::cuda::CUDAGuard device_guard{q.device()};
1089	
1090	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1091	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1092	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1093	    bool is_sm80 = cc_major == 8 && cc_minor == 0;
1094	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1095	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1096	    // We will support Turing in the near future
1097	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1098	
1099	    bool is_dropout = p_dropout > 0.0;
1100	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1101	
1102	    auto q_dtype = q.dtype();
1103	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1104	                "FlashAttention only support fp16 and bf16 data type");
1105	    if (q_dtype == torch::kBFloat16) {
1106	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1107	    }
1108	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
1109	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
1110	    TORCH_CHECK(out.dtype() == q_dtype, "query and out must have the same dtype");
1111	    TORCH_CHECK(dout.dtype() == q_dtype, "query and dout must have the same dtype");
1112	
1113	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
1114	    CHECK_DEVICE(out); CHECK_DEVICE(dout); CHECK_DEVICE(softmax_lse);
1115	
1116	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1117	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1118	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1119	    TORCH_CHECK(out.stride(-1) == 1, "out tensor must have contiguous last dimension");
1120	    TORCH_CHECK(dout.stride(-1) == 1, "dout tensor must have contiguous last dimension");
1121	
1122	    const auto sizes = q.sizes();
1123	
1124	    const int batch_size = sizes[0];
1125	    const int seqlen_q = sizes[1];
1126	    const int num_heads = sizes[2];
1127	    const int head_size = sizes[3];
1128	    const int seqlen_k = k.size(1);
1129	    const int num_heads_k = k.size(2);
1130	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1131	    TORCH_CHECK(head_size % 8 == 0, "head_size should be a multiple of 8");
1132	    TORCH_CHECK(head_size <= 256, "FlashAttention backward only supports head dimension at most 256");
1133	    if (head_size > 192 && is_dropout) {
1134	        TORCH_CHECK(is_sm80 || is_sm90, "FlashAttention backward for head dim > 192 with dropout requires A100/A800 or H100/H800");
1135	    }
1136	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1137	
1138	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1139	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1140	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
1141	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
1142	
1143	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
1144	
1145	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
1146	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
1147	
1148	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size);
1149	    CHECK_SHAPE(k, batch_size, seqlen_k, num_heads_k, head_size);
1150	    CHECK_SHAPE(v, batch_size, seqlen_k, num_heads_k, head_size);
1151	    CHECK_SHAPE(out, batch_size, seqlen_q, num_heads, head_size);
1152	    CHECK_SHAPE(dout, batch_size, seqlen_q, num_heads, head_size);
1153	
1154	    at::Tensor dq, dk, dv;
1155	    if (dq_.has_value()) {
1156	        dq = dq_.value();
1157	        TORCH_CHECK(dq.dtype() == q_dtype, "dq must have the same dtype as q");
1158	        CHECK_DEVICE(dq);
1159	        TORCH_CHECK(dq.stride(-1) == 1, "dq must have contiguous last dimension");
1160	        CHECK_SHAPE(dq, batch_size, seqlen_q, num_heads, head_size);
1161	    } else {
1162	        dq = torch::empty_like(q);
1163	    }
1164	    if (dk_.has_value()) {
1165	        dk = dk_.value();
1166	        TORCH_CHECK(dk.dtype() == q_dtype, "dk must have the same dtype as q");
1167	        CHECK_DEVICE(dk);
1168	        TORCH_CHECK(dk.stride(-1) == 1, "dk must have contiguous last dimension");
1169	        CHECK_SHAPE(dk, batch_size, seqlen_k, num_heads_k, head_size);
1170	    } else {
1171	        dk = torch::empty_like(k);
1172	    }
1173	    if (dv_.has_value()) {
1174	        dv = dv_.value();
1175	        TORCH_CHECK(dv.dtype() == q_dtype, "dv must have the same dtype as q");
1176	        CHECK_DEVICE(dv);
1177	        TORCH_CHECK(dv.stride(-1) == 1, "dv must have contiguous last dimension");
1178	        CHECK_SHAPE(dv, batch_size, seqlen_k, num_heads_k, head_size);
1179	    } else {
1180	        dv = torch::empty_like(v);
1181	    }
1182	
1183	    // bool loop = seqlen_k > blocksize_c;
1184	    // TODO: change later, for now set to true for simplicity
1185	    bool loop = true;
1186	
1187	    auto opts = q.options();
1188	    auto softmax_d = torch::empty({batch_size, num_heads, seqlen_q_rounded}, opts.dtype(at::kFloat));
1189	    at::Tensor dq_accum;
1190	    at::Tensor dk_accum, dv_accum;
1191	    if (loop) {
1192	        if (!deterministic) {
1193	            dq_accum = torch::empty({batch_size, seqlen_q_rounded, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1194	        } else {
1195	            const int nsplits = (get_num_sm(get_current_device()) + batch_size * num_heads - 1) / (batch_size * num_heads);
1196	            dq_accum = torch::zeros({nsplits, batch_size, seqlen_q_rounded, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1197	        }
1198	        // dk_accum = torch::empty({batch_size, num_heads_k, seqlen_k_rounded, head_size_rounded}, opts.dtype(at::kFloat));
1199	        // dv_accum = torch::empty({batch_size, num_heads_k, seqlen_k_rounded, head_size_rounded}, opts.dtype(at::kFloat));
1200	    }
1201	
1202	    at::Tensor dk_expanded, dv_expanded;
1203	    if (num_heads_k != num_heads) {  // MQA / GQA
1204	        dk_expanded = torch::empty({batch_size, seqlen_k, num_heads, head_size}, opts);
1205	        dv_expanded = torch::empty({batch_size, seqlen_k, num_heads, head_size}, opts);
1206	    } else {
1207	        dk_expanded = dk;
1208	        dv_expanded = dv;
1209	    }
1210	
1211	    Flash_bwd_params params;
1212	
1213	    set_params_dgrad(params,
1214	                     batch_size,
1215	                     seqlen_q, seqlen_k,
1216	                     seqlen_q_rounded, seqlen_k_rounded,
1217	                     num_heads, num_heads_k,
1218	                     head_size, head_size_rounded,
1219	                     q, k, v, out,
1220	                     dout, dq, dk_expanded, dv_expanded,
1221	                     nullptr,
1222	                     nullptr,
1223	                     loop ? dq_accum.data_ptr() : nullptr,
1224	                     // loop ? dk_accum.data_ptr() : nullptr,
1225	                     // loop ? dv_accum.data_ptr() : nullptr,
1226	                     nullptr,
1227	                     nullptr,
1228	                     softmax_lse.data_ptr(),
1229	                     softmax_d.data_ptr(),
1230	                     p_dropout,
1231	                     softmax_scale,
1232	                     window_size_left,
1233	                     window_size_right,
1234	                     softcap,
1235	                     deterministic,
1236	                     /*unpadded_lse*/false);
1237	    params.dq_accum_split_stride = !deterministic ? 0 : dq_accum.stride(0);
1238	
1239	    auto launch = &run_mha_bwd;
1240	
1241	    auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1242	        gen_, at::cuda::detail::getDefaultCUDAGenerator());
1243	
1244	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1245	    int64_t counter_offset = params.b * params.h * 32;
1246	
1247	    if ( rng_state.has_value() ) {
1248	        params.rng_state = reinterpret_cast<uint64_t*>(rng_state.value().data_ptr());
1249	    } else if( is_dropout ) {
1250	        // See Note [Acquire lock when using random generators]
1251	        std::lock_guard<std::mutex> lock(gen->mutex_);
1252	        params.philox_args = gen->philox_cuda_state(counter_offset);
1253	        auto seeds = at::cuda::philox::unpack(params.philox_args);
1254	        params.rng_state[0] = std::get<0>(seeds);
1255	        params.rng_state[1] = std::get<1>(seeds);
1256	    }
1257	
1258	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1259	
1260	    if (seqlen_q > 0) {
1261	        launch(params, stream);
1262	    } else {
1263	        // If seqlen_q == 0, then we have an empty tensor. We need to set the output to 0.
1264	        dk_expanded.zero_();
1265	        dv_expanded.zero_();
1266	        softmax_d.zero_();
1267	    }
1268	
1269	    // For MQA/GQA we need to sum dK and dV across the groups
1270	    if (num_heads_k != num_heads) {
1271	        at::sum_out(dk, at::reshape(dk_expanded, {batch_size, seqlen_k, num_heads_k, num_heads / num_heads_k, head_size}), {3});
1272	        at::sum_out(dv, at::reshape(dv_expanded, {batch_size, seqlen_k, num_heads_k, num_heads / num_heads_k, head_size}), {3});
1273	    }
1274	
1275	    return { dq, dk, dv, softmax_d };
1276	}
1277	
1278	std::vector<at::Tensor>
1279	mha_varlen_bwd(const at::Tensor &dout,  // total_q x num_heads, x head_size
1280	               const at::Tensor &q,   // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
1281	               const at::Tensor &k,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1282	               const at::Tensor &v,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1283	               const at::Tensor &out,   // total_q x num_heads x head_size
1284	               const at::Tensor &softmax_lse,    // h x total_q, softmax logsumexp
1285	               c10::optional<at::Tensor> &dq_,   // total_q x num_heads x head_size, total_q := \sum_{i=0}^{b} s_i
1286	               c10::optional<at::Tensor> &dk_,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1287	               c10::optional<at::Tensor> &dv_,   // total_k x num_heads_k x head_size, total_k := \sum_{i=0}^{b} s_i
1288	               const at::Tensor &cu_seqlens_q,  // b+1
1289	               const at::Tensor &cu_seqlens_k,  // b+1
1290	               c10::optional<at::Tensor> &alibi_slopes_, // num_heads or b x num_heads
1291	               const int max_seqlen_q,
1292	               const int max_seqlen_k,          // max sequence length to choose the kernel
1293	               const float p_dropout,         // probability to drop
1294	               const float softmax_scale,
1295	               const bool zero_tensors,
1296	               const bool is_causal,
1297	               int window_size_left,
1298	               int window_size_right,
1299	               const float softcap,
1300	               const bool deterministic,
1301	               c10::optional<at::Tensor> &col_blockmask_, 
1302	               c10::optional<at::Generator> gen_,
1303	               c10::optional<at::Tensor> &rng_state) {
1304	
1305	    #ifdef FLASHATTENTION_DISABLE_BACKWARD
1306	        TORCH_CHECK(false, "This flash attention build does not support backward.");
1307	    #endif
1308	    if (is_causal) { window_size_right = 0; }
1309	
1310	    // Otherwise the kernel will be launched from cuda:0 device
1311	    at::cuda::CUDAGuard device_guard{q.device()};
1312	
1313	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1314	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1315	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1316	    bool is_sm80 = cc_major == 8 && cc_minor == 0;
1317	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1318	    const bool has_blockmask = col_blockmask_.has_value();
1319	    at::Tensor col_blockmask;
1320	    if (has_blockmask) {
1321	        col_blockmask = col_blockmask_.value();
1322	    }
1323	    if(has_blockmask){
1324	        TORCH_CHECK(col_blockmask.dtype() == torch::kInt64, "col_blockmask must have dtype int64");
1325	    }
1326	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1327	    // We will support Turing in the near future
1328	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1329	    bool is_dropout = p_dropout > 0.0;
1330	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1331	
1332	    auto q_dtype = q.dtype();
1333	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1334	                "FlashAttention only support fp16 and bf16 data type");
1335	    if (q_dtype == torch::kBFloat16) {
1336	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1337	    }
1338	    TORCH_CHECK(k.dtype() == q_dtype, "query and key must have the same dtype");
1339	    TORCH_CHECK(v.dtype() == q_dtype, "query and value must have the same dtype");
1340	    TORCH_CHECK(out.dtype() == q_dtype, "query and out must have the same dtype");
1341	    TORCH_CHECK(dout.dtype() == q_dtype, "query and dout must have the same dtype");
1342	    TORCH_CHECK(cu_seqlens_q.dtype() == torch::kInt32, "cu_seqlens_q must have dtype int32");
1343	    TORCH_CHECK(cu_seqlens_k.dtype() == torch::kInt32, "cu_seqlens_k must have dtype int32");
1344	
1345	    CHECK_DEVICE(q); CHECK_DEVICE(k); CHECK_DEVICE(v);
1346	    CHECK_DEVICE(out); CHECK_DEVICE(dout); CHECK_DEVICE(softmax_lse);
1347	    CHECK_DEVICE(cu_seqlens_q); CHECK_DEVICE(cu_seqlens_k);
1348	    if(has_blockmask){
1349	        CHECK_DEVICE(col_blockmask);
1350	    }
1351	
1352	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1353	    TORCH_CHECK(k.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1354	    TORCH_CHECK(v.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1355	    TORCH_CHECK(out.stride(-1) == 1, "out tensor must have contiguous last dimension");
1356	    TORCH_CHECK(dout.stride(-1) == 1, "dout tensor must have contiguous last dimension");
1357	    CHECK_CONTIGUOUS(cu_seqlens_q);
1358	    CHECK_CONTIGUOUS(cu_seqlens_k);
1359	    
1360	
1361	    const auto sizes = q.sizes();
1362	
1363	    const int total_q = sizes[0];
1364	    const int batch_size = cu_seqlens_q.numel() - 1;
1365	    const int num_heads = sizes[1];
1366	    const int head_size = sizes[2];
1367	    const int total_k = k.size(0);
1368	    const int num_heads_k = k.size(1);
1369	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1370	    TORCH_CHECK(head_size % 8 == 0, "head_size should be a multiple of 8");
1371	    TORCH_CHECK(head_size <= 256, "FlashAttention backward only supports head dimension at most 256");
1372	    if (head_size > 192 && is_dropout) {
1373	        TORCH_CHECK(is_sm80 || is_sm90, "FlashAttention backward for head dim > 192 with dropout requires A100/A800 or H100/H800");
1374	    }
1375	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1376	    if (softcap > 0.f) { TORCH_CHECK(p_dropout == 0.f, "Softcapping does not support dropout for now"); }
1377	
1378	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1379	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1380	    const int seqlen_q_rounded = round_multiple(max_seqlen_q, 128);
1381	    const int seqlen_k_rounded = round_multiple(max_seqlen_k, 128);
1382	
1383	    if (window_size_left >= max_seqlen_k) { window_size_left = -1; }
1384	    if (window_size_right >= max_seqlen_k) { window_size_right = -1; }
1385	
1386	    CHECK_SHAPE(q, total_q, num_heads, head_size);
1387	    CHECK_SHAPE(k, total_k, num_heads_k, head_size);
1388	    CHECK_SHAPE(v, total_k, num_heads_k, head_size);
1389	    CHECK_SHAPE(out, total_q, num_heads, head_size);
1390	    CHECK_SHAPE(dout, total_q, num_heads, head_size);
1391	    CHECK_SHAPE(cu_seqlens_q, batch_size + 1);
1392	    CHECK_SHAPE(cu_seqlens_k, batch_size + 1);
1393	    if(has_blockmask){
1394	        CHECK_CONTIGUOUS(col_blockmask);
1395	        // Last dimension should now be the number of uint64s needed to represent the original blocks
1396	        int blocks_per_uint64 = 64;  // 64 bits per uint64
1397	        int m_blocks = total_q / 16;
1398	        int uint64_per_row = (m_blocks + blocks_per_uint64 - 1) / blocks_per_uint64;
1399	        CHECK_SHAPE(col_blockmask, num_heads_k, round_multiple(max_seqlen_k, 64) / 64, uint64_per_row);
1400	    }
1401	
1402	    at::Tensor dq, dk, dv;
1403	    if (dq_.has_value()) {
1404	        dq = dq_.value();
1405	        TORCH_CHECK(dq.dtype() == q_dtype, "dq must have the same dtype as q");
1406	        CHECK_DEVICE(dq);
1407	        TORCH_CHECK(dq.stride(-1) == 1, "dq must have contiguous last dimension");
1408	        CHECK_SHAPE(dq, total_q, num_heads, head_size);
1409	    } else {
1410	        dq = torch::empty_like(q);
1411	    }
1412	    if (dk_.has_value()) {
1413	        dk = dk_.value();
1414	        TORCH_CHECK(dk.dtype() == q_dtype, "dk must have the same dtype as q");
1415	        CHECK_DEVICE(dk);
1416	        TORCH_CHECK(dk.stride(-1) == 1, "dk must have contiguous last dimension");
1417	        CHECK_SHAPE(dk, total_k, num_heads_k, head_size);
1418	    } else {
1419	        dk = torch::empty_like(k);
1420	    }
1421	    if (dv_.has_value()) {
1422	        dv = dv_.value();
1423	        TORCH_CHECK(dv.dtype() == q_dtype, "dv must have the same dtype as q");
1424	        CHECK_DEVICE(dv);
1425	        TORCH_CHECK(dv.stride(-1) == 1, "dv must have contiguous last dimension");
1426	        CHECK_SHAPE(dv, total_k, num_heads_k, head_size);
1427	    } else {
1428	        dv = torch::empty_like(v);
1429	    }
1430	
1431	    // bool loop = max_seqlen_k > blocksize_c;
1432	    // TODO: change later, for now set to true for simplicity
1433	    bool loop = true;
1434	
1435	    auto opts = q.options();
1436	    auto softmax_d = torch::empty({num_heads, total_q + 128 * batch_size}, opts.dtype(at::kFloat));
1437	    at::Tensor dq_accum;
1438	    if (loop) {
1439	        // We don't want to allocate dq_accum of size (batch, seqlen_q_rounded, num_heads, head_size_rounded)
1440	        // because that would be too large if there is a very long sequence and the rest of the sequences are short.
1441	        // Instead, we allocate dq_accum of size (total_q + 128 * batch, num_heads, head_size_rounded).
1442	        // Note that 128 is the max block size on the seqlen_q dimension.
1443	        // For dQ, the i-th sequence is stored in indices from cu_seqlens[i] + 128 * i to
1444	        // cu_seqlens[i + 1] * 128 * i - 1. This ensures that the i-th sequence and (i + 1)-th sequence will
1445	        // be at least 128 apart. It's ok for us to do atomicAdds up to 128 rows beyond what we're normally
1446	        // allowed to do. So we won't have to do any bound checking, and performance should stay the same.
1447	        // Same holds for softmax_d, since LSE is stored in unpadded format.
1448	        if (!deterministic) {
1449	            dq_accum = torch::empty({total_q + 128 * batch_size, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1450	        } else {
1451	            const int nsplits = (get_num_sm(get_current_device()) + batch_size * num_heads - 1) / (batch_size * num_heads);
1452	            dq_accum = torch::zeros({nsplits, total_q + 128 * batch_size, num_heads, head_size_rounded}, opts.dtype(at::kFloat));
1453	        }
1454	    }
1455	
1456	    at::Tensor dk_expanded, dv_expanded;
1457	    if (num_heads_k != num_heads) {  // MQA / GQA
1458	        dk_expanded = torch::empty({total_k, num_heads, head_size}, opts);
1459	        dv_expanded = torch::empty({total_k, num_heads, head_size}, opts);
1460	    } else {
1461	        dk_expanded = dk;
1462	        dv_expanded = dv;
1463	    }
1464	
1465	    if( zero_tensors ) {
1466	        dq.zero_();
1467	        dk_expanded.zero_();
1468	        dv_expanded.zero_();
1469	        softmax_d.zero_();
1470	    }
1471	
1472	    Flash_bwd_params params;
1473	
1474	    set_params_dgrad(params,
1475	                     batch_size,
1476	                     max_seqlen_q, max_seqlen_k,
1477	                     seqlen_q_rounded, seqlen_k_rounded,
1478	                     num_heads, num_heads_k,
1479	                     head_size, head_size_rounded,
1480	                     q, k, v, out,
1481	                     dout, dq, dk_expanded, dv_expanded,
1482	                     cu_seqlens_q.data_ptr(),
1483	                     cu_seqlens_k.data_ptr(),
1484	                     loop ? dq_accum.data_ptr() : nullptr,
1485	                     nullptr,
1486	                     nullptr,
1487	                     softmax_lse.data_ptr(),
1488	                     softmax_d.data_ptr(),
1489	                     p_dropout,
1490	                     softmax_scale,
1491	                     window_size_left,
1492	                     window_size_right,
1493	                     softcap,
1494	                     deterministic,
1495	                     /*unpadded_lse*/true);
1496	    params.dq_accum_split_stride = !deterministic ? 0 : dq_accum.stride(0);
1497	    params.total_q = total_q;
1498	
1499	    if(has_blockmask){
1500	        params.blockmask = static_cast<uint64_t*>(col_blockmask.data_ptr());
1501	        params.m_block_dim = 16;
1502	        params.n_block_dim = 64;
1503	        params.num_blocks_m = total_q / 16;
1504	        params.num_blocks_n = round_multiple(max_seqlen_k, 64) / 64;
1505	        // params.block_window_size = block_window_size;
1506	    }
1507	    else {
1508	        params.blockmask = nullptr;
1509	    }
1510	    auto launch = &run_mha_bwd;
1511	
1512	    auto gen = at::get_generator_or_default<at::CUDAGeneratorImpl>(
1513	        gen_, at::cuda::detail::getDefaultCUDAGenerator());
1514	
1515	    // We use a custom RNG that increases the offset by batch_size * nheads * 32.
1516	    int64_t counter_offset = params.b * params.h * 32;
1517	
1518	    if ( rng_state.has_value() ) {
1519	        params.rng_state = reinterpret_cast<uint64_t*>(rng_state.value().data_ptr());
1520	    } else if( is_dropout ) {
1521	        // See Note [Acquire lock when using random generators]
1522	        std::lock_guard<std::mutex> lock(gen->mutex_);
1523	        params.philox_args = gen->philox_cuda_state(counter_offset);
1524	        auto seeds = at::cuda::philox::unpack(params.philox_args);
1525	        params.rng_state[0] = std::get<0>(seeds);
1526	        params.rng_state[1] = std::get<1>(seeds);
1527	    }
1528	
1529	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1530	
1531	    if (max_seqlen_q > 0) {
1532	        launch(params, stream);
1533	    } else {
1534	        // If seqlen_q == 0, then we have an empty tensor. We need to set the output to 0.
1535	        dk_expanded.zero_();
1536	        dv_expanded.zero_();
1537	        softmax_d.zero_();
1538	    }
1539	
1540	    // For MQA/GQA we need to sum dK and dV across the groups
1541	    if (num_heads_k != num_heads) {
1542	        at::sum_out(dk, at::reshape(dk_expanded, {total_k, num_heads_k, num_heads / num_heads_k, head_size}), {2});
1543	        at::sum_out(dv, at::reshape(dv_expanded, {total_k, num_heads_k, num_heads / num_heads_k, head_size}), {2});
1544	    }
1545	
1546	    return { dq, dk, dv, softmax_d };
1547	}
1548	
1549	std::vector<at::Tensor>
1550	mha_fwd_kvcache(at::Tensor &q,                 // batch_size x seqlen_q x num_heads x head_size
1551	                const at::Tensor &kcache,            // batch_size_c x seqlen_k x num_heads_k x head_size or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
1552	                const at::Tensor &vcache,            // batch_size_c x seqlen_k x num_heads_k x head_size or num_blocks x page_block_size x num_heads_k x head_size if there's a block_table.
1553	                c10::optional<const at::Tensor> &k_, // batch_size x seqlen_knew x num_heads_k x head_size
1554	                c10::optional<const at::Tensor> &v_, // batch_size x seqlen_knew x num_heads_k x head_size
1555	                c10::optional<const at::Tensor> &seqlens_k_, // batch_size
1556	                c10::optional<const at::Tensor> &rotary_cos_, // seqlen_ro x (rotary_dim / 2)
1557	                c10::optional<const at::Tensor> &rotary_sin_, // seqlen_ro x (rotary_dim / 2)
1558	                c10::optional<const at::Tensor> &cache_batch_idx_, // indices to index into the KV cache
1559	                c10::optional<const at::Tensor> &leftpad_k_, // batch_size
1560	                c10::optional<at::Tensor> &block_table_, // batch_size x max_num_blocks_per_seq
1561	                c10::optional<at::Tensor> &alibi_slopes_, // num_heads or batch_size x num_heads
1562	                c10::optional<at::Tensor> &out_,             // batch_size x seqlen_q x num_heads x head_size
1563	                const float softmax_scale,
1564	                bool is_causal,
1565	                int window_size_left,
1566	                int window_size_right,
1567	                const float softcap,
1568	                bool is_rotary_interleaved,   // if true, rotary combines indices 0 & 1, else indices 0 & rotary_dim / 2
1569	                int num_splits,
1570	                        c10::optional<at::Tensor> &blockmask_
1571	                ) {
1572	
1573	    // Otherwise the kernel will be launched from cuda:0 device
1574	    at::cuda::CUDAGuard device_guard{q.device()};
1575	
1576	    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
1577	    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
1578	    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
1579	    bool is_sm90 = cc_major == 9 && cc_minor == 0;
1580	    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
1581	    // We will support Turing in the near future
1582	    // TORCH_CHECK(is_sm90 || is_sm8x || is_sm75, "FlashAttention only supports Turing GPUs or newer.");
1583	
1584	    auto q_dtype = q.dtype();
1585	    TORCH_CHECK(q_dtype == torch::kFloat16 || q_dtype == torch::kBFloat16,
1586	                "FlashAttention only support fp16 and bf16 data type");
1587	    if (q_dtype == torch::kBFloat16) {
1588	        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
1589	    }
1590	    TORCH_CHECK(kcache.dtype() == q_dtype, "query and key must have the same dtype");
1591	    TORCH_CHECK(vcache.dtype() == q_dtype, "query and value must have the same dtype");
1592	
1593	    CHECK_DEVICE(q); CHECK_DEVICE(kcache); CHECK_DEVICE(vcache);
1594	
1595	    TORCH_CHECK(q.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1596	    TORCH_CHECK(kcache.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1597	    TORCH_CHECK(vcache.stride(-1) == 1, "Input tensor must have contiguous last dimension");
1598	
1599	    at::Tensor block_table;
1600	    const bool paged_KV = block_table_.has_value();
1601	    if (paged_KV) {
1602	        TORCH_CHECK(!cache_batch_idx_.has_value(), "Paged KVcache does not support cache_batch_idx");
1603	        block_table = block_table_.value();
1604	        CHECK_DEVICE(block_table);
1605	        TORCH_CHECK(block_table.dtype() == torch::kInt32, "block_table must have dtype torch.int32");
1606	        TORCH_CHECK(block_table.stride(-1) == 1, "block_table must have contiguous last dimension");
1607	    }
1608	
1609	    const auto sizes = q.sizes();
1610	
1611	    const int batch_size = sizes[0];
1612	    int seqlen_q = sizes[1];
1613	    int num_heads = sizes[2];
1614	    const int head_size_og = sizes[3];
1615	
1616	    const int max_num_blocks_per_seq = !paged_KV ? 0 : block_table.size(1);
1617	    const int num_blocks = !paged_KV ? 0 : kcache.size(0);
1618	    const int page_block_size = !paged_KV ? 1 : kcache.size(1);
1619	    TORCH_CHECK(!paged_KV || page_block_size % 256 == 0, "Paged KV cache block size must be divisible by 256");
1620	    const int seqlen_k = !paged_KV ? kcache.size(1) : max_num_blocks_per_seq * page_block_size;
1621	    const int num_heads_k = kcache.size(2);
1622	    const int batch_size_c = !paged_KV ? kcache.size(0) : batch_size;
1623	    TORCH_CHECK(batch_size > 0, "batch size must be positive");
1624	    TORCH_CHECK(head_size_og <= 256, "FlashAttention forward only supports head dimension at most 256");
1625	    TORCH_CHECK(num_heads % num_heads_k == 0, "Number of heads in key/value must divide number of heads in query");
1626	
1627	    // causal=true is the same as causal=false in this case
1628	    if (seqlen_q == 1 && !alibi_slopes_.has_value()) { is_causal = false; }
1629	    if (is_causal) { window_size_right = 0; }
1630	
1631	    // Faster to transpose q from (b, 1, (nheads_kv ngroups), d) to (b, ngroups, nheads_kv, d) in this case
1632	    // H/t Daniel Haziza
1633	    const int seqlenq_ngroups_swapped = seqlen_q == 1 && num_heads > num_heads_k && window_size_left < 0 && window_size_right < 0 && head_size_og % 8 == 0 && !alibi_slopes_.has_value();
1634	    if (seqlenq_ngroups_swapped) {
1635	        const int ngroups = num_heads / num_heads_k;
1636	        q = q.reshape({batch_size, num_heads_k, ngroups, head_size_og}).transpose(1, 2);
1637	        seqlen_q = ngroups;
1638	        num_heads = num_heads_k;
1639	    }
1640	
1641	    if (window_size_left >= seqlen_k) { window_size_left = -1; }
1642	    if (window_size_right >= seqlen_k) { window_size_right = -1; }
1643	
1644	    CHECK_SHAPE(q, batch_size, seqlen_q, num_heads, head_size_og);
1645	    if (!paged_KV) {
1646	        CHECK_SHAPE(kcache, batch_size_c, seqlen_k, num_heads_k, head_size_og);
1647	        CHECK_SHAPE(vcache, batch_size_c, seqlen_k, num_heads_k, head_size_og);
1648	    } else {
1649	        CHECK_SHAPE(kcache, num_blocks, page_block_size, num_heads_k, head_size_og);
1650	        CHECK_SHAPE(vcache, num_blocks, page_block_size, num_heads_k, head_size_og);
1651	        CHECK_SHAPE(block_table, batch_size, max_num_blocks_per_seq);
1652	    }
1653	
1654	    at::Tensor q_padded, kcache_padded, vcache_padded;
1655	    if (head_size_og % 8 != 0) {
1656	        q_padded = torch::nn::functional::pad(q, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1657	        kcache_padded = torch::nn::functional::pad(kcache, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1658	        vcache_padded = torch::nn::functional::pad(vcache, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1659	    } else {
1660	        q_padded = q;
1661	        kcache_padded = kcache;
1662	        vcache_padded = vcache;
1663	    }
1664	
1665	    at::Tensor out;
1666	    if (out_.has_value()) {
1667	        out = out_.value();
1668	        TORCH_CHECK(out.dtype() == q_dtype, "Output must have the same dtype as inputs");
1669	        CHECK_DEVICE(out);
1670	        TORCH_CHECK(out.stride(-1) == 1, "Output tensor must have contiguous last dimension");
1671	        CHECK_SHAPE(out, batch_size, seqlen_q, num_heads, head_size_og);
1672	        if (head_size_og % 8 != 0) { out = torch::empty_like(q_padded); }
1673	    } else {
1674	        out = torch::empty_like(q_padded);
1675	    }
1676	
1677	    auto round_multiple = [](int x, int m) { return (x + m - 1) / m * m; };
1678	    const int head_size = round_multiple(head_size_og, 8);
1679	    const int head_size_rounded = head_size <= 192 ? round_multiple(head_size, 32) : 256;
1680	    const int seqlen_q_rounded = round_multiple(seqlen_q, 128);
1681	    const int seqlen_k_rounded = round_multiple(seqlen_k, 128);
1682	
1683	    auto opts = q.options();
1684	
1685	    auto softmax_lse = torch::empty({batch_size, num_heads, seqlen_q}, opts.dtype(at::kFloat));
1686	
1687	    Flash_fwd_params params;
1688	    set_params_fprop(params,
1689	                     batch_size,
1690	                     seqlen_q, seqlen_k,
1691	                     seqlen_q_rounded, seqlen_k_rounded,
1692	                     num_heads, num_heads_k,
1693	                     head_size, head_size_rounded,
1694	                     q_padded, kcache_padded, vcache_padded, out,
1695	                     /*cu_seqlens_q_d=*/nullptr,
1696	                     /*cu_seqlens_k_d=*/nullptr,
1697	                     /*seqused_k=*/nullptr,
1698	                     /*p_ptr=*/nullptr,
1699	                     softmax_lse.data_ptr(),
1700	                     /*p_dropout=*/0.f,
1701	                     softmax_scale,
1702	                     window_size_left,
1703	                     window_size_right,
1704	                     softcap
1705	                     );
1706	
1707	    if (blockmask_.has_value()) {
1708	        params.blockmask = static_cast<uint64_t*>(blockmask_.value().data_ptr());
1709	        params.m_block_dim = 16;
1710	        params.n_block_dim = 64;
1711	        params.num_k_heads = 2;
1712	        params.num_blocks_m = (seqlen_q + 16 - 1) / 16;
1713	        params.num_blocks_n = (seqlen_k + 64 - 1) / 64;
1714	    } else {
1715	        params.blockmask = nullptr;
1716	        params.m_block_dim = 1;
1717	        params.n_block_dim = 1;
1718	    }
1719	
1720	    at::Tensor k, v, k_padded, v_padded;
1721	    if (k_.has_value()) {
1722	        TORCH_CHECK(v_.has_value(), "If key is supplied, value must also be passed in");
1723	        TORCH_CHECK(seqlens_k_.has_value(), "If key is supplied, seqlens_k must also be passed in");
1724	        TORCH_CHECK(seqlen_q <= seqlen_k, "If key is supplied, it must have seqlen <= the seqlen of the KV cache");
1725	        k = k_.value();
1726	        v = v_.value();
1727	        TORCH_CHECK(k.dtype() == q_dtype, "Key must have the same dtype as query");
1728	        TORCH_CHECK(v.dtype() == q_dtype, "Value must have the same dtype as query");
1729	        CHECK_DEVICE(k); CHECK_DEVICE(v);
1730	        TORCH_CHECK(k.stride(-1) == 1, "Key tensor must have contiguous last dimension");
1731	        TORCH_CHECK(v.stride(-1) == 1, "Value tensor must have contiguous last dimension");
1732	        int seqlen_knew = k.size(1);
1733	        CHECK_SHAPE(k, batch_size, seqlen_knew, num_heads_k, head_size_og);
1734	        CHECK_SHAPE(v, batch_size, seqlen_knew, num_heads_k, head_size_og);
1735	        if (head_size_og % 8 != 0) {
1736	            k_padded = torch::nn::functional::pad(k, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1737	            v_padded = torch::nn::functional::pad(v, torch::nn::functional::PadFuncOptions({0, 8 - head_size_og % 8}));
1738	        } else {
1739	            k_padded = k;
1740	            v_padded = v;
1741	        }
1742	        params.seqlen_knew = seqlen_knew;
1743	        params.knew_ptr = k_padded.data_ptr();
1744	        params.vnew_ptr = v_padded.data_ptr();
1745	        // All stride are in elements, not bytes.
1746	        params.knew_batch_stride = k_padded.stride(0);
1747	        params.vnew_batch_stride = v_padded.stride(0);
1748	        params.knew_row_stride = k_padded.stride(-3);
1749	        params.vnew_row_stride = v_padded.stride(-3);
1750	        params.knew_head_stride = k_padded.stride(-2);
1751	        params.vnew_head_stride = v_padded.stride(-2);
1752	    }
1753	
1754	    if (seqlens_k_.has_value()) {
1755	        auto seqlens_k = seqlens_k_.value();
1756	        TORCH_CHECK(seqlens_k.dtype() == torch::kInt32, "seqlens_k must have dtype int32");
1757	        CHECK_DEVICE(seqlens_k);
1758	        CHECK_CONTIGUOUS(seqlens_k);
1759	        CHECK_SHAPE(seqlens_k, batch_size);
1760	        params.cu_seqlens_k = static_cast<int *>(seqlens_k.data_ptr());
1761	    }
1762	    params.is_seqlens_k_cumulative = !(seqlens_k_.has_value());
1763	    if (leftpad_k_.has_value()) {
1764	        TORCH_CHECK(!paged_KV, "We don't support Paged KV and leftpad_k running at the same time yet");
1765	        auto leftpad_k = leftpad_k_.value();
1766	        TORCH_CHECK(leftpad_k.dtype() == torch::kInt32, "leftpad_k must have dtype int32");
1767	        CHECK_DEVICE(leftpad_k);
1768	        CHECK_CONTIGUOUS(leftpad_k);
1769	        CHECK_SHAPE(leftpad_k, batch_size);
1770	        params.leftpad_k = static_cast<int *>(leftpad_k.data_ptr());
1771	    }
1772	
1773	    if (rotary_cos_.has_value()) {
1774	        TORCH_CHECK(k_.has_value(), "If rotary cos/sin are provided, new key / value to be appended to KV cache must also be provided");
1775	        auto rotary_cos = rotary_cos_.value();
1776	        CHECK_DEVICE(rotary_cos);
1777	        params.rotary_dim = rotary_cos.size(1) * 2;
1778	        TORCH_CHECK(params.rotary_dim <= head_size, "rotary_dim must be <= headdim");
1779	        TORCH_CHECK(params.rotary_dim % 16 == 0, "Only rotary dimensions divisible by 16 are currently supported");
1780	        const int seqlen_ro = rotary_cos.size(0);
1781	        TORCH_CHECK(seqlen_ro >= seqlen_k, "cos/sin seqlen must be at least the seqlen of KV cache");
1782	        CHECK_SHAPE(rotary_cos, seqlen_ro, params.rotary_dim / 2);
1783	        CHECK_CONTIGUOUS(rotary_cos);
1784	        TORCH_CHECK(rotary_cos.scalar_type() == q_dtype, "rotary_cos must have the same dtype as query");
1785	
1786	        TORCH_CHECK(rotary_sin_.has_value(), "If rotary cos is provided, rotary sin must also be provided");
1787	        auto rotary_sin = rotary_sin_.value();
1788	        CHECK_DEVICE(rotary_sin);
1789	        CHECK_SHAPE(rotary_sin, seqlen_ro, params.rotary_dim / 2);
1790	        CHECK_CONTIGUOUS(rotary_sin);
1791	        TORCH_CHECK(rotary_sin.scalar_type() == q_dtype, "rotary_cos must have the same dtype as query");
1792	        params.rotary_cos_ptr = rotary_cos.data_ptr();
1793	        params.rotary_sin_ptr = rotary_sin.data_ptr();
1794	        params.is_rotary_interleaved = is_rotary_interleaved;
1795	    } else {
1796	        params.rotary_dim = 0;
1797	    }
1798	
1799	    if (cache_batch_idx_.has_value()) {
1800	        auto cache_batch_idx = cache_batch_idx_.value();
1801	        CHECK_DEVICE(cache_batch_idx);
1802	        CHECK_CONTIGUOUS(cache_batch_idx);
1803	        TORCH_CHECK(cache_batch_idx.scalar_type() == torch::kInt32, "cache_batch_idx must have dtype int32");
1804	        params.cache_batch_idx = reinterpret_cast<int *>(cache_batch_idx.data_ptr());
1805	    }
1806	
1807	    // Keep references to these tensors to extend their lifetime
1808	    at::Tensor softmax_lse_accum, out_accum;
1809	    std::tie(softmax_lse_accum, out_accum) = set_params_splitkv(
1810	        params, batch_size, num_heads, head_size, seqlen_k, seqlen_q,
1811	        head_size_rounded, /*dropout*/ 0.f, num_splits, get_num_sm(get_current_device()), opts);
1812	
1813	    if (paged_KV) {
1814	        params.block_table = block_table.data_ptr<int>();
1815	        params.block_table_batch_stride = block_table.stride(0);
1816	    }
1817	    params.page_block_size = page_block_size;
1818	
1819	
1820	    set_params_alibi(params, alibi_slopes_, batch_size, num_heads);
1821	
1822	    auto stream = at::cuda::getCurrentCUDAStream().stream();
1823	    // Only split kernel supports appending to KV cache, or indexing to the cache with cache_batch_idx,
1824	    // or paged KV cache
1825	    run_mha_fwd(params, stream, /*force_split_kernel=*/k_.has_value() || cache_batch_idx_.has_value() || paged_KV || true);
1826	
1827	    if (head_size_og % 8 != 0) {
1828	        out = out.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)});
1829	        if (out_.has_value()) { out_.value().copy_(out); }
1830	        if (k_.has_value()) {
1831	            // It's expensive to copy the KV cache here for the case where head size not divisible by 8,
1832	            // but we don't expect to get this case in practice. This is just so that the code works for that case.
1833	            kcache.copy_(kcache_padded.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)}));
1834	            vcache.copy_(vcache_padded.index({"...", torch::indexing::Slice(torch::indexing::None, head_size_og)}));
1835	        }
1836	    }
1837	
1838	    if (seqlenq_ngroups_swapped) {
1839	        out = out.transpose(1, 2).reshape({batch_size, 1, num_heads_k * seqlen_q, head_size_og});
1840	        softmax_lse = softmax_lse.reshape({batch_size, num_heads_k * seqlen_q, 1});
1841	    }
1842	    return {out, softmax_lse};
1843	}
1844	
1845	
1846
```

> AGENT

现在让我分部分读取 `flash_fwd_kernel.h` 文件，并找到 `.cu` 文件和 `setup.py`。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 1
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include "philox_unpack.cuh" // For at::cuda::philox::unpack
8	
9	#include <cute/tensor.hpp>
10	
11	#include <cutlass/cutlass.h>
12	#include <cutlass/array.h>
13	#include <cutlass/numeric_types.h>
14	
15	#include "block_info.h"
16	#include "kernel_traits.h"
17	#include "utils.h"
18	#include "softmax.h"
19	#include "mask.h"
20	#include "dropout.h"
21	#include "rotary.h"
22	#include "flash_blockmask.h"
23	
24	namespace flash {
25	
26	using namespace cute;
27	
28	////////////////////////////////////////////////////////////////////////////////////////////////////
29	
30	__forceinline__ __device__ float minusinf_to_zero(float &input) {
31	    if (input == -INFINITY) {
32	        return 0;
33	    } else {
34	        return input;
35	    }
36	}
37	
38	template<int thr_offset, typename Engine0, typename Layout0, typename Operator>
39	__forceinline__ __device__  void thread_element_wise_reduce_(Tensor<Engine0, Layout0> &tensor, Operator &op) {
40	    static_assert(Layout0::rank == 2, "Only support 2D Tensor");
41	    #pragma unroll
42	    for (int mi = 0; mi < size<0>(tensor); mi++) {
43	        #pragma unroll
44	        for (int ni = 0; ni < size<1>(tensor); ni++) {
45	            tensor(mi, ni) = op(
46	                minusinf_to_zero(tensor(mi, ni)), 
47	                __shfl_xor_sync(uint32_t(-1), minusinf_to_zero(tensor(mi, ni)), thr_offset)
48	            );
49	        }
50	    }
51	}
52	
53	template <typename Element, typename E1, typename L1, typename E2, typename L2>
54	__forceinline__ __device__ void hdim16_reduce(
55	    Tensor<E1, L1> &acc_S, 
56	    Tensor<E2, L2> &g_Sh,
57	    const int col_idx_offset_,
58	    const int row_idx_offset_,
59	    const int warp_row_stride) {
60	
61	    // Reshape tensor_ from (MMA=4, MMA_M, MMA_N) (or (_2,_2),_2,_16) for D=32) to (nrow=(2, MMA_M), ncol=(2, MMA_N))
62	    auto tensor = make_tensor(acc_S.data(), flash::convert_layout_acc_rowcol(acc_S.layout()));
63	    const int warp_id = threadIdx.x / 32;
64	    const int lane_id = threadIdx.x % 32;
65	    // const int col_idx_offset = col_idx_offset_ + (lane_id % 4) * 2;
66	    // const int row_idx_offset = row_idx_offset_ + warp_id * 16 + lane_id / 4;
67	    const int col_idx_offset = 0 + (lane_id % 4) * 2;
68	    const int row_idx_offset = 0 + warp_id * 16 + lane_id / 4;
69	
70	    // step 1: 线程内部求和 (v0 + v2)
71	    using TensorT = decltype(make_tensor<float>(Shape< Int<size<0, 1>(tensor)>, Int<size<1>(tensor)> >{}));
72	    TensorT v02;
73	    clear(v02);
74	    #pragma unroll
75	    for (int mi = 0; mi < size<0, 1>(tensor); ++mi) {
76	        #pragma unroll
77	        for (int nj = 0; nj < size<1, 1>(tensor); ++nj) {
78	            #pragma unroll
79	            for (int j = 0; j < size<1, 0>(tensor); ++j) {
80	                const int col_idx_v02 = j * size<1, 1>(tensor) + nj;
81	                const float v0 = minusinf_to_zero(tensor(make_coord(0, mi), make_coord(j, nj)));
82	                const float v2 = minusinf_to_zero(tensor(make_coord(1, mi), make_coord(j, nj)));
83	                v02(mi, col_idx_v02) = v0 + v2;
84	            }
85	        }
86	    }
87	
88	    // step 2: warp 内部蝶形求和
89	    SumOp<float> sum_op;
90	    thread_element_wise_reduce_<16>(v02, sum_op);
91	    thread_element_wise_reduce_<8> (v02, sum_op);
92	    thread_element_wise_reduce_<4> (v02, sum_op);
93	
94	    // step 3: copy 到 global mem
95	    cutlass::NumericConverter<Element, float> converter;
96	    if (lane_id < 4) {
97	        #pragma unroll
98	        for (int mi = 0; mi < size<0, 1>(tensor); ++mi) {
99	            const int row_idx_base = row_idx_offset + mi * warp_row_stride;
100	            #pragma unroll
101	            for (int nj = 0; nj < size<1, 1>(tensor); ++nj) {
102	                const int col_idx_base = col_idx_offset + nj * 8;
103	                #pragma unroll
104	                for (int j = 0; j < size<1, 0>(tensor); ++j) {
105	                    const int col_idx = col_idx_base + j;
106	                    const int col_idx_v02 = j * size<1, 1>(tensor) + nj;
107	                    g_Sh(row_idx_base/16, col_idx) = converter(v02(mi, col_idx_v02)); // ignore /16 since it's too slow
108	                }
109	            }
110	        }
111	    }
112	}
113	
114	////////////////////////////////////////////////////////////////////////////////////////////////////
115	
116	template<typename ElementAccum, typename Params, int kBlockM, bool Is_even_MN>
117	__forceinline__ __device__ auto get_lse_tile(const Params &params, const int bidb, const int bidh, const int m_block, const BlockInfo</*Varlen=*/!Is_even_MN> &binfo) {
118	        // When params.unpadded_lse is false, LSE is written as (b, h, seqlen_q) - this is non-variable seqlen path.
119	        // Otherwise, when params.seqlenq_ngroups_swapped is true, it is written as (h, seqlen_q, b) to account for seqlen_q <-> h swapping trick.
120	        // Otherwise, it's written as (h, b, seqlen_q).
121	        const bool varlen_q = params.unpadded_lse && !params.seqlenq_ngroups_swapped;
122	        auto lse_offset = varlen_q ? binfo.q_offset(params.seqlen_q, 1, bidb) : 0;
123	        auto gmem_ptr_lse = make_gmem_ptr(reinterpret_cast<ElementAccum*>(params.softmax_lse_ptr) + lse_offset);
124	
125	        auto lse_shape = varlen_q ? make_shape(1, params.h, params.total_q) : make_shape(params.b, params.h, params.seqlen_q);
126	        auto lse_stride = params.seqlenq_ngroups_swapped ? make_stride(1, params.seqlen_q * params.b, params.b) : (
127	            params.unpadded_lse ? make_stride(params.h * params.total_q, params.total_q, 1) :  make_stride(params.h * params.seqlen_q, params.seqlen_q, 1)
128	            );
129	
130	        auto lse_layout = make_layout(lse_shape, lse_stride);
131	        Tensor mLSE = make_tensor(gmem_ptr_lse, lse_layout);
132	        auto mLSE_slice = varlen_q ? mLSE(0, bidh, _) : mLSE(bidb, bidh, _);
133	        return local_tile(mLSE_slice, Shape<Int<kBlockM>>{}, make_coord(m_block));
134	}
135	
136	
137	template<typename Kernel_traits, bool Is_dropout, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Return_softmax, typename Params>
138	inline __device__ void compute_attn_1rowblock(const Params &params, const int bidb, const int bidh, const int m_block) {
139	
140	    using Element = typename Kernel_traits::Element;
141	    using ElementAccum = typename Kernel_traits::ElementAccum;
142	    using index_t = typename Kernel_traits::index_t;
143	
144	    // Shared memory.
145	    extern __shared__ char smem_[];
146	
147	    // The thread index.
148	    const int tidx = threadIdx.x;
149	
150	    constexpr int kBlockM = Kernel_traits::kBlockM;
151	    constexpr int kBlockN = Kernel_traits::kBlockN;
152	    constexpr int kHeadDim = Kernel_traits::kHeadDim;
153	    constexpr int kNWarps = Kernel_traits::kNWarps;
154	
155	    auto seed_offset = at::cuda::philox::unpack(params.philox_args);
156	    flash::Dropout dropout(std::get<0>(seed_offset), std::get<1>(seed_offset), params.p_dropout_in_uint8_t,
157	                           bidb, bidh, tidx, params.h);
158	
159	    // Save seed and offset for backward, before any early exiting. Otherwise the 0-th thread block might
160	    // exit early and no one saves the rng states.
161	    if (Is_dropout && blockIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0 && tidx == 0) {
162	        params.rng_state[0] = std::get<0>(seed_offset);
163	        params.rng_state[1] = std::get<1>(seed_offset);
164	    }
165	
166	    const BlockInfo</*Varlen=*/!Is_even_MN> binfo(params, bidb);
167	    if (m_block * kBlockM >= binfo.actual_seqlen_q) return;
168	
169	    const int n_block_min = !Is_local ? 0 : std::max(0, (m_block * kBlockM + binfo.actual_seqlen_k - binfo.actual_seqlen_q - params.window_size_left) / kBlockN);
170	    int n_block_max = cute::ceil_div(binfo.actual_seqlen_k, kBlockN);
171	    if (Is_causal || Is_local) {
172	        n_block_max = std::min(n_block_max,
173	                               cute::ceil_div((m_block + 1) * kBlockM / params.m_block_dim + binfo.actual_seqlen_k - (binfo.actual_seqlen_q / params.m_block_dim) + params.window_size_right, kBlockN));
174	        // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) {
175	        //     printf("m_block = %d, n_block_max = %d\n", m_block, n_block_max);
176	        // }
177	    }
178	    // We exit early and write 0 to gO and gLSE. This also covers the case where actual_seqlen_k == 0.
179	    // Otherwise we might read OOB elements from gK and gV.
180	    if ((Is_causal || Is_local || !Is_even_MN) && n_block_max <= n_block_min) {
181	        Tensor mO = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.o_ptr)
182	                                              + binfo.q_offset(params.o_batch_stride, params.o_row_stride, bidb)),
183	                                make_shape(binfo.actual_seqlen_q, params.h, params.d),
184	                                make_stride(params.o_row_stride, params.o_head_stride, _1{}));
185	        Tensor gO = local_tile(mO(_, bidh, _), Shape<Int<kBlockM>, Int<kHeadDim>>{},
186	                              make_coord(m_block, 0));  // (kBlockM, kHeadDim)
187	
188	        Tensor gLSE = get_lse_tile<ElementAccum, Params, kBlockM, Is_even_MN>(params, bidb, bidh, m_block, binfo);
189	
190	        typename Kernel_traits::GmemTiledCopyO gmem_tiled_copy_O;
191	        auto gmem_thr_copy_O = gmem_tiled_copy_O.get_thread_slice(tidx);
192	        Tensor tOgO = gmem_thr_copy_O.partition_D(gO);
193	        Tensor tOrO = make_tensor<Element>(shape(tOgO));
194	        clear(tOrO);
195	        // Construct identity layout for sO
196	        Tensor cO = make_identity_tensor(make_shape(size<0>(gO), size<1>(gO)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
197	        // Repeat the partitioning with identity layouts
198	        Tensor tOcO = gmem_thr_copy_O.partition_D(cO);
199	        Tensor tOpO = make_tensor<bool>(make_shape(size<2>(tOgO)));
200	        if (!Is_even_K) {
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 200
}
```

> TOOL

tool_result Read
```
200	        if (!Is_even_K) {
201	            #pragma unroll
202	            for (int k = 0; k < size(tOpO); ++k) { tOpO(k) = get<1>(tOcO(0, 0, k)) < params.d; }
203	        }
204	        // Clear_OOB_K must be false since we don't want to write zeros to gmem
205	        flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/false, /*Clear_OOB_K=*/false>(
206	            gmem_tiled_copy_O, tOrO, tOgO, tOcO, tOpO, binfo.actual_seqlen_q - m_block * kBlockM
207	        );
208	        #pragma unroll
209	        for (int m = 0; m < size<1>(tOgO); ++m) {
210	            const int row = get<0>(tOcO(0, m, 0));
211	            if (row < binfo.actual_seqlen_q - m_block * kBlockM && get<1>(tOcO(0, m, 0)) == 0) { gLSE(row) = INFINITY; }
212	        }
213	        return;
214	    }
215	    // if (tidx == 0) { printf("m_block = %d, n_block_min = %d, n_block_max = %d\n", m_block, n_block_min, n_block_max); }
216	
217	    // We iterate over the blocks in reverse order. This is because the last block is the only one
218	    // that needs masking when we read K and V from global memory. Moreover, iterating in reverse
219	    // might save us 1 register (we just need n_block instead of both n_block and n_block_max).
220	
221	    const index_t row_offset_p = ((bidb * params.h + bidh) * params.seqlen_q_rounded
222	        + m_block * kBlockM) * params.seqlen_k_rounded + (n_block_max - 1) * kBlockN;
223	
224	    Tensor mQ = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.q_ptr)
225	                                          + binfo.q_offset(params.q_batch_stride, params.q_row_stride, bidb)),
226	                            make_shape(binfo.actual_seqlen_q, params.h, params.d),
227	                            make_stride(params.q_row_stride, params.q_head_stride, _1{}));
228	    Tensor gQ = local_tile(mQ(_, bidh, _), Shape<Int<kBlockM>, Int<kHeadDim>>{},
229	                           make_coord(m_block, 0));  // (kBlockM, kHeadDim)
230	    Tensor mK = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.k_ptr)
231	                                          + binfo.k_offset(params.k_batch_stride, params.k_row_stride, bidb)),
232	                            make_shape(binfo.actual_seqlen_k, params.h_k, params.d),
233	                            make_stride(params.k_row_stride, params.k_head_stride, _1{}));
234	    Tensor gK = local_tile(mK(_, bidh / params.h_h_k_ratio, _), Shape<Int<kBlockN>, Int<kHeadDim>>{},
235	                           make_coord(_, 0));  // (kBlockN, kHeadDim, nblocksN)
236	    Tensor mV = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.v_ptr)
237	                                          + binfo.k_offset(params.v_batch_stride, params.v_row_stride, bidb)),
238	                            make_shape(binfo.actual_seqlen_k, params.h_k, params.d),
239	                            make_stride(params.v_row_stride, params.v_head_stride, _1{}));
240	    Tensor gV = local_tile(mV(_, bidh / params.h_h_k_ratio, _), Shape<Int<kBlockN>, Int<kHeadDim>>{},
241	                           make_coord(_, 0));  // (kBlockN, kHeadDim, nblocksN)
242	    Tensor gP = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.p_ptr) + row_offset_p),
243	                            Shape<Int<kBlockM>, Int<kBlockN>>{},
244	                            make_stride(params.seqlen_k_rounded, _1{}));
245	
246	    Tensor sQ = make_tensor(make_smem_ptr(reinterpret_cast<Element *>(smem_)),
247	                            typename Kernel_traits::SmemLayoutQ{});
248	    // Careful we're using the same smem for sQ and sK | sV if Share_Q_K_smem;
249	    Tensor sK = make_tensor(sQ.data() + (Kernel_traits::Share_Q_K_smem ? 0 : size(sQ)),
250	                            typename Kernel_traits::SmemLayoutKV{});
251	    Tensor sV = make_tensor(sK.data() + size(sK), typename Kernel_traits::SmemLayoutKV{});
252	    Tensor sVt = make_tensor(sV.data(), typename Kernel_traits::SmemLayoutVtransposed{});
253	    Tensor sVtNoSwizzle = make_tensor(sV.data().get(), typename Kernel_traits::SmemLayoutVtransposedNoSwizzle{});
254	
255	    typename Kernel_traits::GmemTiledCopyQKV gmem_tiled_copy_QKV;
256	    auto gmem_thr_copy_QKV = gmem_tiled_copy_QKV.get_thread_slice(tidx);
257	
258	    Tensor tQgQ = gmem_thr_copy_QKV.partition_S(gQ);
259	    Tensor tQsQ = gmem_thr_copy_QKV.partition_D(sQ);
260	    Tensor tKgK = gmem_thr_copy_QKV.partition_S(gK);  // (KCPY, KCPY_N, KCPY_K, nblocksN)
261	    Tensor tKsK = gmem_thr_copy_QKV.partition_D(sK);
262	    Tensor tVgV = gmem_thr_copy_QKV.partition_S(gV);  // (VCPY, VCPY_N, VCPY_K, nblocksN)
263	    Tensor tVsV = gmem_thr_copy_QKV.partition_D(sV);
264	
265	    typename Kernel_traits::TiledMma tiled_mma;
266	    auto thr_mma = tiled_mma.get_thread_slice(tidx);
267	    Tensor tSrQ  = thr_mma.partition_fragment_A(sQ);                           // (MMA,MMA_M,MMA_K)
268	    Tensor tSrK  = thr_mma.partition_fragment_B(sK);                           // (MMA,MMA_N,MMA_K)
269	    Tensor tOrVt  = thr_mma.partition_fragment_B(sVtNoSwizzle);                // (MMA, MMA_K,MMA_N)
270	
271	    Tensor tSgS  = thr_mma.partition_C(gP);
272	
273	    Tensor acc_o = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kHeadDim>>{});  // MMA, MMA_M, MMA_K
274	
275	    //
276	    // Copy Atom retiling
277	    //
278	
279	    auto smem_tiled_copy_Q = make_tiled_copy_A(typename Kernel_traits::SmemCopyAtom{}, tiled_mma);
280	    auto smem_thr_copy_Q = smem_tiled_copy_Q.get_thread_slice(tidx);
281	    // if (cute::thread0()) {smem_thr_copy_Q.print_all();}
282	    Tensor tSsQ = smem_thr_copy_Q.partition_S(sQ);
283	    // if (cute::thread0()) {print(tSsQ.layout()); printf("\n");}
284	
285	    auto smem_tiled_copy_K = make_tiled_copy_B(typename Kernel_traits::SmemCopyAtom{}, tiled_mma);
286	    auto smem_thr_copy_K = smem_tiled_copy_K.get_thread_slice(tidx);
287	    Tensor tSsK = smem_thr_copy_K.partition_S(sK);
288	
289	    auto smem_tiled_copy_V = make_tiled_copy_B(typename Kernel_traits::SmemCopyAtomTransposed{}, tiled_mma);
290	    auto smem_thr_copy_V = smem_tiled_copy_V.get_thread_slice(tidx);
291	    Tensor tOsVt = smem_thr_copy_V.partition_S(sVt);
292	
293	    //
294	    // PREDICATES
295	    //
296	
297	    // // Allocate predicate tensors for m and n
298	    // Tensor tQpQ = make_tensor<bool>(make_shape(size<1>(tQsQ), size<2>(tQsQ)), Stride<_1,_0>{});
299	    // Tensor tKVpKV = make_tensor<bool>(make_shape(size<1>(tKsK), size<2>(tKsK)), Stride<_1,_0>{});
300	
301	    // Construct identity layout for sQ and sK
302	    Tensor cQ = make_identity_tensor(make_shape(size<0>(sQ), size<1>(sQ)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
303	    Tensor cKV = make_identity_tensor(make_shape(size<0>(sK), size<1>(sK)));    // (BLK_N,BLK_K) -> (blk_n,blk_k)
304	    // Tensor tScQ = thr_mma.partition_A(cQ);                           // (MMA,MMA_M,MMA_K)
305	    // if (cute::thread0()) {
306	    //     print(tScQ.layout()); printf("\n");
307	    //     for (int i = 0; i < size(tScQ); ++i) {
308	    //         printf("%d ", get<0>(tScQ(i)));
309	    //     }
310	    //     printf("\n");
311	    //     for (int i = 0; i < size(tScQ); ++i) {
312	    //         printf("%d ", get<1>(tScQ(i)));
313	    //     }
314	    //     printf("\n");
315	    // }
316	
317	    // Repeat the partitioning with identity layouts
318	    Tensor tQcQ = gmem_thr_copy_QKV.partition_S(cQ);       // (ACPY,ACPY_M,ACPY_K) -> (blk_m,blk_k)
319	    Tensor tKVcKV = gmem_thr_copy_QKV.partition_S(cKV);   // (BCPY,BCPY_N,BCPY_K) -> (blk_n,blk_k)
320	
321	    // Allocate predicate tensors for k
322	    Tensor tQpQ = make_tensor<bool>(make_shape(size<2>(tQsQ)));
323	    Tensor tKVpKV = make_tensor<bool>(make_shape(size<2>(tKsK)));
324	
325	    // Set predicates for k bounds
326	    if (!Is_even_K) {
327	        #pragma unroll
328	        for (int k = 0; k < size(tQpQ); ++k) { tQpQ(k) = get<1>(tQcQ(0, 0, k)) < params.d; }
329	        #pragma unroll
330	        for (int k = 0; k < size(tKVpKV); ++k) { tKVpKV(k) = get<1>(tKVcKV(0, 0, k)) < params.d; }
331	    }
332	
333	    // Prologue
334	
335	    // We don't need to clear the sQ smem tiles since we'll only write out the valid outputs
336	    flash::copy<Is_even_MN, Is_even_K>(gmem_tiled_copy_QKV, tQgQ, tQsQ, tQcQ, tQpQ,
337	                                       binfo.actual_seqlen_q - m_block * kBlockM);
338	    if (Kernel_traits::Is_Q_in_regs) { cute::cp_async_fence(); }
339	
340	    // // if (cute::thread(1, 0)) { print(tQsQ); }
341	    // // Tensor sQNoSwizzle = make_tensor(make_smem_ptr(reinterpret_cast<Element *>(smem_)), typename Kernel_traits::SmemLayoutQNoSwizzle{});
342	    // // if (cute::thread0()) { print(sQNoSwizzle); }
343	
344	    if (Kernel_traits::Share_Q_K_smem) {
345	        flash::cp_async_wait<0>();
346	        __syncthreads();
347	        Tensor tSrQ_copy_view = smem_thr_copy_Q.retile_D(tSrQ);
348	        CUTE_STATIC_ASSERT_V(size<1>(tSsQ) == size<1>(tSrQ_copy_view));            // M
349	        cute::copy(smem_tiled_copy_Q, tSsQ, tSrQ_copy_view);
350	        __syncthreads();
351	    }
352	
353	    int n_block = n_block_max - 1;
354	    // We don't need to clear the sK smem tiles since we'll mask out the scores anyway.
355	    flash::copy<Is_even_MN, Is_even_K>(gmem_tiled_copy_QKV, tKgK(_, _, _, n_block), tKsK, tKVcKV, tKVpKV,
356	                                       binfo.actual_seqlen_k - n_block * kBlockN);
357	    cute::cp_async_fence();
358	    // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z < 2) { print(tKgK); }
359	    // __syncthreads();
360	
361	    if (Kernel_traits::Is_Q_in_regs && !Kernel_traits::Share_Q_K_smem) {
362	        flash::cp_async_wait<1>();
363	        __syncthreads();
364	        Tensor tSrQ_copy_view = smem_thr_copy_Q.retile_D(tSrQ);
365	        CUTE_STATIC_ASSERT_V(size<1>(tSsQ) == size<1>(tSrQ_copy_view));            // M
366	        cute::copy(smem_tiled_copy_Q, tSsQ, tSrQ_copy_view);
367	    }
368	
369	    clear(acc_o);
370	
371	    flash::Softmax<2 * size<1>(acc_o)> softmax;
372	
373	    const float alibi_slope = !Has_alibi || params.alibi_slopes_ptr == nullptr ? 0.0f : reinterpret_cast<float *>(params.alibi_slopes_ptr)[bidb * params.alibi_slopes_batch_stride + bidh] / params.scale_softmax;
374	    flash::Mask<Is_causal, Is_local, Has_alibi> mask(binfo.actual_seqlen_k, binfo.actual_seqlen_q, params.window_size_left, params.window_size_right, alibi_slope, params.m_block_dim);
375	
376	    // Initialize blockmask iterator if blockmask is enabled
377	    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
378	    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
379	    int leap = 0;
380	
381	    // For performance reason, we separate out two kinds of iterations:
382	    // those that need masking on S, and those that don't.
383	    // We need masking on S for the very last block when K and V has length not multiple of kBlockN.
384	    // We also need masking on S if it's causal, for the last ceil_div(kBlockM, kBlockN) blocks.
385	    // We will have at least 1 "masking" iteration.
386	
387	    // If not even_N, then seqlen_k might end in the middle of a block. In that case we need to
388	    // mask 2 blocks (e.g. when kBlockM == kBlockN), not just 1.
389	    constexpr int n_masking_steps = (!Is_causal && !Is_local)
390	        ? 1
391	        : ((Is_even_MN && Is_causal) ? cute::ceil_div(kBlockM, kBlockN) : cute::ceil_div(kBlockM, kBlockN) + 1);
392	    #pragma unroll
393	    for (int masking_step = 0; masking_step < n_masking_steps; ++masking_step, --n_block) {
394	        const bool skip = (n_block != next_block_idx);
395	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
396	        clear(acc_s);
397	        flash::cp_async_wait<0>();
398	        __syncthreads();
399
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 400
}
```

> TOOL

tool_result Read
```
400	        // Advance gV
401	        if (masking_step > 0) {
402	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV(_, _, _, n_block), tVsV, tKVcKV, tKVpKV);
403	        } else {
404	            // Clear the smem tiles to account for predicated off loads
405	            flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/true>(
406	                gmem_tiled_copy_QKV, tVgV(_, _, _, n_block), tVsV, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN
407	            );
408	        }
409	        cute::cp_async_fence();
410	
411	        if (!skip) {
412	            flash::gemm</*A_in_regs=*/Kernel_traits::Is_Q_in_regs>(
413	                acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
414	                smem_thr_copy_Q, smem_thr_copy_K
415	            );
416	            // if (cute::thread0()) { print(acc_s); }
417	            if constexpr (Is_softcap){
418	                flash::apply_softcap(acc_s, params.softcap);
419	            }
420	
421	            mask.template apply_mask<Is_causal, Is_even_MN>(
422	                acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
423	            );
424	
425	            next_block_idx = blockmask.max_no_larger(n_block-1);
426	        } else {
427	            mask.all_mask(acc_s);
428	        }
429	
430	        flash::cp_async_wait<0>();
431	        __syncthreads();
432	        
433	        leap = (masking_step + 1 == n_masking_steps) ? n_block - next_block_idx : 1;
434	        
435	        if (n_block > n_block_min && next_block_idx != -1) {
436	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK(_, _, _, n_block - leap), tKsK, tKVcKV, tKVpKV);
437	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
438	            // isn't right and we get race conditions.
439	            cute::cp_async_fence();
440	        }
441	
442	        // TODO: when we have key_padding_mask we'll need to Check_inf
443	        masking_step == 0
444	            ? softmax.template softmax_rescale_o</*Is_first=*/true,  /*Check_inf=*/Is_causal || Is_local>(acc_s, acc_o, params.scale_softmax_log2)
445	            : softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_causal || Is_local>(acc_s, acc_o, params.scale_softmax_log2);
446	
447	        if (!skip) {
448	            // Convert acc_s from fp32 to fp16/bf16
449	            Tensor rP = flash::convert_type<Element>(acc_s);
450	            int block_row_idx = m_block * (kBlockM / 16) + tidx / 32;
451	            int block_col_idx = n_block * (kBlockN / 32);
452	            if (Return_softmax) {
453	                Tensor rP_drop = make_fragment_like(rP);
454	                cute::copy(rP, rP_drop);
455	                dropout.template apply_dropout</*encode_dropout_in_sign_bit=*/true>(
456	                    rP_drop, block_row_idx, block_col_idx, kNWarps
457	                );
458	                cute::copy(rP_drop, tSgS);
459	                tSgS.data() = tSgS.data() + (-kBlockN);
460	            }
461	            if (Is_dropout) {
462	                dropout.apply_dropout(rP, block_row_idx, block_col_idx, kNWarps);
463	            }
464	
465	            // Reshape rP from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
466	            // if using m16n8k16 or (4, MMA_M, MMA_N) if using m16n8k8.
467	            Tensor tOrP = make_tensor(rP.data(), flash::convert_layout_acc_Aregs<Kernel_traits::TiledMma>(rP.layout()));
468	            // if (cute::thread0()) { print(tOrP); }
469	            flash::gemm_rs(acc_o, tOrP, tOrVt, tOsVt, tiled_mma, smem_tiled_copy_V, smem_thr_copy_V);
470	            // if (cute::thread0()) { print(scores); }
471	        }
472	
473	        // This check is at the end of the loop since we always have at least 1 iteration
474	        if (n_masking_steps > 1 && n_block <= n_block_min) {
475	            --n_block;
476	            break;
477	        }
478	    }
479	
480	    leap = n_block - next_block_idx + 1;
481	
482	    // These are the iterations where we don't need masking on S
483	    for (n_block = next_block_idx; n_block != -1 && n_block >= n_block_min; n_block = next_block_idx) {
484	        next_block_idx = blockmask.max_no_larger(n_block - 1);
485	        
486	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
487	        clear(acc_s);
488	        flash::cp_async_wait<0>();
489	        __syncthreads();
490	        flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV(_, _, _, n_block), tVsV, tKVcKV, tKVpKV);
491	        cute::cp_async_fence();
492	        flash::gemm</*A_in_regs=*/Kernel_traits::Is_Q_in_regs>(
493	            acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
494	            smem_thr_copy_Q, smem_thr_copy_K
495	        );
496	        if constexpr (Is_softcap){
497	            flash::apply_softcap(acc_s, params.softcap);
498	        }
499	
500	        flash::cp_async_wait<0>();
501	        __syncthreads();
502	        
503	        leap = n_block - next_block_idx;
504	        if (next_block_idx != -1) {
505	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK(_, _, _, n_block - leap), tKsK, tKVcKV, tKVpKV);
506	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
507	            // isn't right and we get race conditions.
508	            cute::cp_async_fence();
509	        }
510	
511	        mask.template apply_mask</*Causal_mask=*/false>(
512	            acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
513	        );
514	
515	        softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_local>(acc_s, acc_o, params.scale_softmax_log2);
516	
517	        Tensor rP = flash::convert_type<Element>(acc_s);
518	        int block_row_idx = m_block * (kBlockM / 16) + tidx / 32;
519	        int block_col_idx = n_block * (kBlockN / 32);
520	        if (Return_softmax) {
521	            Tensor rP_drop = make_fragment_like(rP);
522	            cute::copy(rP, rP_drop);
523	            dropout.template apply_dropout</*encode_dropout_in_sign_bit=*/true>(
524	                rP_drop, block_row_idx, block_col_idx, kNWarps
525	            );
526	            cute::copy(rP_drop, tSgS);
527	            tSgS.data() = tSgS.data() + (-kBlockN);
528	        }
529	        if (Is_dropout) {
530	            dropout.apply_dropout(rP, block_row_idx, block_col_idx, kNWarps);
531	        }
532	
533	        // Reshape rP from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
534	        // if using m16n8k16 or (4, MMA_M, MMA_N) if using m16n8k8.
535	        Tensor tOrP = make_tensor(rP.data(), flash::convert_layout_acc_Aregs<Kernel_traits::TiledMma>(rP.layout()));
536	        flash::gemm_rs(acc_o, tOrP, tOrVt, tOsVt, tiled_mma, smem_tiled_copy_V, smem_thr_copy_V);
537	    }
538	
539	    // Epilogue
540	
541	    Tensor lse = softmax.template normalize_softmax_lse<Is_dropout>(acc_o, params.scale_softmax, params.rp_dropout);
542	
543	    // Convert acc_o from fp32 to fp16/bf16
544	    Tensor rO = flash::convert_type<Element>(acc_o);
545	    Tensor sO = make_tensor(sQ.data(), typename Kernel_traits::SmemLayoutO{});    // (SMEM_M,SMEM_N)
546	    // Partition sO to match the accumulator partitioning
547	    auto smem_tiled_copy_O = make_tiled_copy_C(typename Kernel_traits::SmemCopyAtomO{}, tiled_mma);
548	    auto smem_thr_copy_O = smem_tiled_copy_O.get_thread_slice(tidx);
549	    Tensor taccOrO = smem_thr_copy_O.retile_S(rO);        // ((Atom,AtomNum), MMA_M, MMA_N)
550	    Tensor taccOsO = smem_thr_copy_O.partition_D(sO);     // ((Atom,AtomNum),PIPE_M,PIPE_N)
551	
552	    // sO has the same size as sQ, so we don't need to sync here.
553	    if (Kernel_traits::Share_Q_K_smem) { __syncthreads(); }
554	
555	    cute::copy(smem_tiled_copy_O, taccOrO, taccOsO);
556	
557	    Tensor mO = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.o_ptr)
558	                                          + binfo.q_offset(params.o_batch_stride, params.o_row_stride, bidb)),
559	                            make_shape(binfo.actual_seqlen_q, params.h, params.d),
560	                            make_stride(params.o_row_stride, params.o_head_stride, _1{}));
561	    Tensor gO = local_tile(mO(_, bidh, _), Shape<Int<kBlockM>, Int<kHeadDim>>{},
562	                           make_coord(m_block, 0));  // (kBlockM, kHeadDim)
563	    Tensor gLSE = get_lse_tile<ElementAccum, Params, kBlockM, Is_even_MN>(params, bidb, bidh, m_block, binfo);
564	
565	    typename Kernel_traits::GmemTiledCopyO gmem_tiled_copy_O;
566	    auto gmem_thr_copy_O = gmem_tiled_copy_O.get_thread_slice(tidx);
567	    Tensor tOsO = gmem_thr_copy_O.partition_S(sO);        // ((Atom,AtomNum),ATOM_M,ATOM_N)
568	    Tensor tOgO = gmem_thr_copy_O.partition_D(gO);
569	
570	    __syncthreads();
571	
572	    Tensor tOrO = make_tensor<Element>(shape(tOgO));
573	    cute::copy(gmem_tiled_copy_O, tOsO, tOrO);
574	
575	    Tensor caccO = make_identity_tensor(Shape<Int<kBlockM>, Int<kHeadDim>>{});    // (BLK_M,BLK_K) -> (blk_m,blk_k)
576	    Tensor taccOcO = thr_mma.partition_C(caccO);                           // (MMA,MMA_M,MMA_K)
577	    static_assert(decltype(size<0>(taccOcO))::value == 4);
578	    // Convert to ((2, 2), MMA_M, MMA_K) then take only the row indices.
579	    Tensor taccOcO_row = logical_divide(taccOcO, Shape<_2>{})(make_coord(0, _), _, 0);
580	    CUTE_STATIC_ASSERT_V(size(lse) == size(taccOcO_row));                     // MMA_M
581	    if (get<1>(taccOcO_row(0)) == 0) {
582	        #pragma unroll
583	        for (int mi = 0; mi < size(lse); ++mi) {
584	            const int row = get<0>(taccOcO_row(mi));
585	            if (row < binfo.actual_seqlen_q - m_block * kBlockM) { gLSE(row) = lse(mi); }
586	        }
587	    }
588	
589	    // Construct identity layout for sO
590	    Tensor cO = make_identity_tensor(make_shape(size<0>(sO), size<1>(sO)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
591	    // Repeat the partitioning with identity layouts
592	    Tensor tOcO = gmem_thr_copy_O.partition_D(cO);                           // (ACPY,ACPY_M,ACPY_K) -> (blk_m,blk_k)
593	    Tensor tOpO = make_tensor<bool>(make_shape(size<2>(tOgO)));
594	    if (!Is_even_K) {
595	        #pragma unroll
596	        for (int k = 0; k < size(tOpO); ++k) { tOpO(k) = get<1>(tOcO(0, 0, k)) < params.d; }
597	    }
598	    // Clear_OOB_K must be false since we don't want to write zeros to gmem
599	    flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/false, /*Clear_OOB_K=*/false>(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 600
}
```

> TOOL

tool_result Read
```
600	        gmem_tiled_copy_O, tOrO, tOgO, tOcO, tOpO, binfo.actual_seqlen_q - m_block * kBlockM
601	    );
602	}
603	
604	////////////////////////////////////////////////////////////////////////////////////////////////////
605	
606	template<typename Kernel_traits, bool Is_causal, bool Is_local, bool Has_alibi, bool Is_even_MN, bool Is_even_K, bool Is_softcap, bool Split, bool Append_KV, typename Params>
607	inline __device__ void compute_attn_1rowblock_splitkv(const Params &params, const int bidb, const int bidh, const int m_block, const int n_split_idx, const int num_n_splits) {
608	
609	    using Element = typename Kernel_traits::Element;
610	    using ElementAccum = typename Kernel_traits::ElementAccum;
611	    using index_t = typename Kernel_traits::index_t;
612	
613	    // Shared memory.
614	    extern __shared__ char smem_[];
615	
616	    // The thread index.
617	    const int tidx = threadIdx.x;
618	
619	    constexpr int kBlockM = Kernel_traits::kBlockM;
620	    constexpr int kBlockN = Kernel_traits::kBlockN;
621	    constexpr int kHeadDim = Kernel_traits::kHeadDim;
622	    constexpr int kNWarps = Kernel_traits::kNWarps;
623	
624	    using GmemTiledCopyO = std::conditional_t<
625	        !Split,
626	        typename Kernel_traits::GmemTiledCopyO,
627	        typename Kernel_traits::GmemTiledCopyOaccum
628	    >;
629	    using ElementO = std::conditional_t<!Split, Element, ElementAccum>;
630	
631	    const BlockInfo</*Varlen=*/!Is_even_MN> binfo(params, bidb);
632	    // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) { printf("Is_even_MN = %d, is_cumulativ = %d, seqlen_k_cache = %d, actual_seqlen_k = %d\n", Is_even_MN, params.is_seqlens_k_cumulative, binfo.seqlen_k_cache, binfo.actual_seqlen_k); }
633	    // if (threadIdx.x == 0 && blockIdx.y == 1 && blockIdx.z == 0) { printf("params.knew_ptr = %p, seqlen_k_cache + seqlen_knew = %d\n", params.knew_ptr, binfo.seqlen_k_cache + (params.knew_ptr == nullptr ? 0 : params.seqlen_knew)); }
634	    if (m_block * kBlockM >= binfo.actual_seqlen_q) return;
635	
636	    const int n_blocks_per_split = ((params.seqlen_k + kBlockN - 1) / kBlockN + num_n_splits - 1) / num_n_splits;
637	    const int n_block_min = !Is_local
638	        ? n_split_idx * n_blocks_per_split
639	        : std::max(n_split_idx * n_blocks_per_split, (m_block * kBlockM + binfo.actual_seqlen_k - binfo.actual_seqlen_q - params.window_size_left) / kBlockN);
640	    int n_block_max = std::min(cute::ceil_div(binfo.actual_seqlen_k, kBlockN), (n_split_idx + 1) * n_blocks_per_split);
641	    if (Is_causal || Is_local) {
642	        n_block_max = std::min(n_block_max,
643	                               cute::ceil_div((m_block + 1) * kBlockM / params.m_block_dim + binfo.actual_seqlen_k - (binfo.actual_seqlen_q / params.m_block_dim) + params.window_size_right, kBlockN));
644	    }
645	    if (n_block_min >= n_block_max) {  // This also covers the case where n_block_max <= 0
646	        // We exit early and write 0 to gOaccum and -inf to gLSEaccum.
647	        // Otherwise we might read OOB elements from gK and gV,
648	        // or get wrong results when we combine gOaccum from different blocks.
649	        const index_t row_offset_o = binfo.q_offset(params.o_batch_stride, params.o_row_stride, bidb)
650	            + m_block * kBlockM * params.o_row_stride + bidh * params.o_head_stride;
651	        const index_t row_offset_oaccum = (((n_split_idx * params.b + bidb) * params.h + bidh) * params.seqlen_q
652	            + m_block * kBlockM) * params.d_rounded;
653	        const index_t row_offset_lseaccum = ((n_split_idx * params.b + bidb) * params.h + bidh) * params.seqlen_q + m_block * kBlockM;
654	        Tensor gOaccum = make_tensor(make_gmem_ptr(reinterpret_cast<ElementO *>(Split ? params.oaccum_ptr : params.o_ptr) + (Split ? row_offset_oaccum : row_offset_o)),
655	                                      Shape<Int<kBlockM>, Int<kHeadDim>>{},
656	                                     make_stride(Split ? kHeadDim : params.o_row_stride, _1{}));
657	        Tensor gLSEaccum = make_tensor(make_gmem_ptr(reinterpret_cast<ElementAccum *>(Split ? params.softmax_lseaccum_ptr : params.softmax_lse_ptr) + row_offset_lseaccum),
658	                                      Shape<Int<kBlockM>>{}, Stride<_1>{});
659	
660	        GmemTiledCopyO gmem_tiled_copy_Oaccum;
661	        auto gmem_thr_copy_Oaccum = gmem_tiled_copy_Oaccum.get_thread_slice(tidx);
662	        Tensor tOgOaccum = gmem_thr_copy_Oaccum.partition_D(gOaccum);
663	        Tensor tOrOaccum = make_tensor<ElementO>(shape(tOgOaccum));
664	        clear(tOrOaccum);
665	        // Construct identity layout for sO
666	        Tensor cO = make_identity_tensor(make_shape(size<0>(gOaccum), size<1>(gOaccum)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
667	        // Repeat the partitioning with identity layouts
668	        Tensor tOcO = gmem_thr_copy_Oaccum.partition_D(cO);
669	        Tensor tOpO = make_tensor<bool>(make_shape(size<2>(tOgOaccum)));
670	        if (!Is_even_K) {
671	            #pragma unroll
672	            for (int k = 0; k < size(tOpO); ++k) { tOpO(k) = get<1>(tOcO(0, 0, k)) < params.d; }
673	        }
674	        // Clear_OOB_K must be false since we don't want to write zeros to gmem
675	        flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/false, /*Clear_OOB_K=*/false>(
676	            gmem_tiled_copy_Oaccum, tOrOaccum, tOgOaccum, tOcO, tOpO, binfo.actual_seqlen_q - m_block * kBlockM
677	        );
678	        #pragma unroll
679	        for (int m = 0; m < size<1>(tOgOaccum); ++m) {
680	            const int row = get<0>(tOcO(0, m, 0));
681	            if (row < binfo.actual_seqlen_q - m_block * kBlockM && get<1>(tOcO(0, m, 0)) == 0) { gLSEaccum(row) = Split ? -INFINITY : INFINITY; }
682	        }
683	        return;
684	    }
685	
686	    // We iterate over the blocks in reverse order. This is because the last block is the only one
687	    // that needs masking when we read K and V from global memory. Moreover, iterating in reverse
688	    // might save us 1 register (we just need n_block instead of both n_block and n_block_max).
689	
690	    // We move K and V to the last block.
691	    const int bidb_cache = params.cache_batch_idx == nullptr ? bidb : params.cache_batch_idx[bidb];
692	    const int *block_table = params.block_table == nullptr ? nullptr : params.block_table + bidb * params.block_table_batch_stride;
693	    const int block_table_idx = block_table == nullptr ? 0 : (n_block_max - 1) * kBlockN / params.page_block_size;
694	    const int block_table_offset = block_table == nullptr ? 0 : (n_block_max - 1) * kBlockN - block_table_idx * params.page_block_size;
695	    const index_t row_offset_k = block_table == nullptr
696	        ? binfo.k_offset(params.k_batch_stride, params.k_row_stride, bidb_cache)
697	          + (n_block_max - 1) * kBlockN * params.k_row_stride + (bidh / params.h_h_k_ratio) * params.k_head_stride
698	        : block_table[block_table_idx] * params.k_batch_stride + block_table_offset * params.k_row_stride + (bidh / params.h_h_k_ratio) * params.k_head_stride;
699	    const index_t row_offset_v = block_table == nullptr
700	        ? binfo.k_offset(params.v_batch_stride, params.v_row_stride, bidb_cache)
701	          + (n_block_max - 1) * kBlockN * params.v_row_stride + (bidh / params.h_h_k_ratio) * params.v_head_stride
702	        : block_table[block_table_idx] * params.v_batch_stride + block_table_offset * params.v_row_stride + (bidh / params.h_h_k_ratio) * params.v_head_stride;
703	
704	    Tensor mQ = make_tensor(make_gmem_ptr(reinterpret_cast<Element*>(params.q_ptr) + binfo.q_offset(params.q_batch_stride, params.q_row_stride, bidb)),
705	                            make_shape(binfo.actual_seqlen_q, params.h, params.d),
706	                            make_stride(params.q_row_stride, params.q_head_stride, _1{}));
707	    Tensor gQ = local_tile(mQ(_, bidh, _), Shape<Int<kBlockM>, Int<kHeadDim>>{},
708	                           make_coord(m_block, 0));  // (kBlockM, kHeadDim)
709	    Tensor gK = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.k_ptr) + row_offset_k),
710	                            Shape<Int<kBlockN>, Int<kHeadDim>>{},
711	                            make_stride(params.k_row_stride, _1{}));
712	    // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) { printf("k_ptr = %p, row_offset_k = %d, gK_ptr = %p\n", params.k_ptr, row_offset_k, gK.data()); }
713	    Tensor gV = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.v_ptr) + row_offset_v),
714	                            Shape<Int<kBlockN>, Int<kHeadDim>>{},
715	                            make_stride(params.v_row_stride, _1{}));
716	
717	    Tensor sQ = make_tensor(make_smem_ptr(reinterpret_cast<Element *>(smem_)),
718	                            typename Kernel_traits::SmemLayoutQ{});
719	    Tensor sK = make_tensor(sQ.data() + size(sQ), typename Kernel_traits::SmemLayoutKV{});
720	    Tensor sV = make_tensor(sK.data() + size(sK), typename Kernel_traits::SmemLayoutKV{});
721	    Tensor sVt = make_tensor(sV.data(), typename Kernel_traits::SmemLayoutVtransposed{});
722	    Tensor sVtNoSwizzle = make_tensor(sV.data().get(), typename Kernel_traits::SmemLayoutVtransposedNoSwizzle{});
723	
724	    typename Kernel_traits::GmemTiledCopyQKV gmem_tiled_copy_QKV;
725	    auto gmem_thr_copy_QKV = gmem_tiled_copy_QKV.get_thread_slice(tidx);
726	
727	    Tensor tQgQ = gmem_thr_copy_QKV.partition_S(gQ);
728	    Tensor tQsQ = gmem_thr_copy_QKV.partition_D(sQ);
729	    Tensor tKgK = gmem_thr_copy_QKV.partition_S(gK);  // (KCPY, KCPY_N, KCPY_K)
730	    Tensor tKsK = gmem_thr_copy_QKV.partition_D(sK);
731	    Tensor tVgV = gmem_thr_copy_QKV.partition_S(gV);  // (VCPY, VCPY_N, VCPY_K)
732	    Tensor tVsV = gmem_thr_copy_QKV.partition_D(sV);
733	
734	    typename Kernel_traits::TiledMma tiled_mma;
735	    auto thr_mma = tiled_mma.get_thread_slice(tidx);
736	    Tensor tSrQ  = thr_mma.partition_fragment_A(sQ);                           // (MMA,MMA_M,MMA_K)
737	    Tensor tSrK  = thr_mma.partition_fragment_B(sK);                           // (MMA,MMA_N,MMA_K)
738	    Tensor tOrVt  = thr_mma.partition_fragment_B(sVtNoSwizzle);                // (MMA, MMA_K,MMA_N)
739	
740	    Tensor acc_o = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kHeadDim>>{});  // MMA, MMA_M, MMA_K
741	
742	    //
743	    // Copy Atom retiling
744	    //
745	
746	    auto smem_tiled_copy_Q = make_tiled_copy_A(typename Kernel_traits::SmemCopyAtom{}, tiled_mma);
747	    auto smem_thr_copy_Q = smem_tiled_copy_Q.get_thread_slice(tidx);
748	    Tensor tSsQ = smem_thr_copy_Q.partition_S(sQ);
749	
750	    auto smem_tiled_copy_K = make_tiled_copy_B(typename Kernel_traits::SmemCopyAtom{}, tiled_mma);
751	    auto smem_thr_copy_K = smem_tiled_copy_K.get_thread_slice(tidx);
752	    Tensor tSsK = smem_thr_copy_K.partition_S(sK);
753	
754	    auto smem_tiled_copy_V = make_tiled_copy_B(typename Kernel_traits::SmemCopyAtomTransposed{}, tiled_mma);
755	    auto smem_thr_copy_V = smem_tiled_copy_V.get_thread_slice(tidx);
756	    Tensor tOsVt = smem_thr_copy_V.partition_S(sVt);
757	
758	    // PREDICATES
759	    //
760	
761	    // // Allocate predicate tensors for m and n
762	    // Tensor tQpQ = make_tensor<bool>(make_shape(size<1>(tQsQ), size<2>(tQsQ)), Stride<_1,_0>{});
763	    // Tensor tKVpKV = make_tensor<bool>(make_shape(size<1>(tKsK), size<2>(tKsK)), Stride<_1,_0>{});
764	
765	    // Construct identity layout for sQ and sK
766	    Tensor cQ = make_identity_tensor(make_shape(size<0>(sQ), size<1>(sQ)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
767	    Tensor cKV = make_identity_tensor(make_shape(size<0>(sK), size<1>(sK)));    // (BLK_N,BLK_K) -> (blk_n,blk_k)
768	
769	    // Repeat the partitioning with identity layouts
770	    Tensor tQcQ = gmem_thr_copy_QKV.partition_S(cQ);       // (ACPY,ACPY_M,ACPY_K) -> (blk_m,blk_k)
771	    Tensor tKVcKV = gmem_thr_copy_QKV.partition_S(cKV);   // (BCPY,BCPY_N,BCPY_K) -> (blk_n,blk_k)
772	
773	    // Allocate predicate tensors for k
774	    Tensor tQpQ = make_tensor<bool>(make_shape(size<2>(tQsQ)));
775	    Tensor tKVpKV = make_tensor<bool>(make_shape(size<2>(tKsK)));
776	
777	    // Set predicates for k bounds
778	    if (!Is_even_K) {
779	        #pragma unroll
780	        for (int k = 0; k < size(tQpQ); ++k) { tQpQ(k) = get<1>(tQcQ(0, 0, k)) < params.d; }
781	        #pragma unroll
782	        for (int k = 0; k < size(tKVpKV); ++k) { tKVpKV(k) = get<1>(tKVcKV(0, 0, k)) < params.d; }
783	    }
784	
785	    // Prologue
786	
787	    // Copy from Knew to K, optionally apply rotary embedding.
788	    typename Kernel_traits::GmemTiledCopyRotcossin gmem_tiled_copy_rotary;
789	    auto gmem_thr_copy_rotary = gmem_tiled_copy_rotary.get_thread_slice(tidx);
790	    typename Kernel_traits::GmemTiledCopyRotcossinCont gmem_tiled_copy_rotary_cont;
791	    auto gmem_thr_copy_rotary_cont = gmem_tiled_copy_rotary_cont.get_thread_slice(tidx);
792	    if constexpr (Append_KV) {
793	        // Even if we have MQA / GQA, all threadblocks responsible for the same KV head are writing to
794	        // gmem. Technically it's a race condition, but they all write the same content anyway, and it's safe.
795	        // We want to do this so that all threadblocks can proceed right after they finish writing the KV cache.
796	        const index_t row_offset_cossin = ((n_block_max - 1) * kBlockN + (params.leftpad_k == nullptr ? 0 : params.leftpad_k[bidb])) * (params.rotary_dim / 2);
797	        Tensor gCos = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_cos_ptr) + row_offset_cossin),
798	                                  Shape<Int<kBlockN>, Int<kHeadDim / 2>>{},
799	                                  make_stride(params.rotary_dim / 2, _1{}));
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 800
}
```

> TOOL

tool_result Read
```
800	        Tensor gSin = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_sin_ptr) + row_offset_cossin),
801	                                  Shape<Int<kBlockN>, Int<kHeadDim / 2>>{},
802	                                  make_stride(params.rotary_dim / 2, _1{}));
803	        Tensor gCosCont = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_cos_ptr) + row_offset_cossin),
804	                                      Shape<Int<kBlockN>, Int<kHeadDim>>{},
805	                                      make_stride(params.rotary_dim / 2, _1{}));
806	        Tensor gSinCont = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_sin_ptr) + row_offset_cossin),
807	                                      Shape<Int<kBlockN>, Int<kHeadDim>>{},
808	                                      make_stride(params.rotary_dim / 2, _1{}));
809	        Tensor tRgCos = gmem_thr_copy_rotary.partition_S(gCos);
810	        Tensor tRgSin = gmem_thr_copy_rotary.partition_S(gSin);
811	        Tensor tRgCosCont = gmem_thr_copy_rotary_cont.partition_S(gCosCont);
812	        Tensor tRgSinCont = gmem_thr_copy_rotary_cont.partition_S(gSinCont);
813	        // if (cute::thread(0, 0)) { printf("rotary_cos_ptr = %p, gCos.data() = %p, tRgCos.data() = %p, rotary_dim = %d\n", params.rotary_cos_ptr, gCos.data(), tRgCos.data(), params.rotary_dim); }
814	        // if (cute::thread(8, 0)) { print_tensor(gCos); }
815	        // if (cute::thread(0, 0)) { print_tensor(tRgCos); }
816	
817	        // const index_t row_offset_knew = binfo.k_offset(params.knew_batch_stride, params.knew_row_stride, bidb)
818	        const index_t row_offset_knew = bidb * params.knew_batch_stride
819	            + ((n_block_max - 1) * kBlockN) * params.knew_row_stride + (bidh / params.h_h_k_ratio) * params.knew_head_stride;
820	        // const index_t row_offset_vnew = binfo.k_offset(params.vnew_batch_stride, params.vnew_row_stride, bidb)
821	        const index_t row_offset_vnew = bidb * params.vnew_batch_stride
822	            + ((n_block_max - 1) * kBlockN) * params.vnew_row_stride + (bidh / params.h_h_k_ratio) * params.vnew_head_stride;
823	        // Subtract seqlen_k_cache * row stride so that conceptually gK and gKnew "line up". When we access them,
824	        // e.g. if gK has 128 rows and gKnew has 64 rows, we access gK[:128] and gKNew[128:128 + 64].
825	        // This maps to accessing the first 64 rows of knew_ptr.
826	        Tensor gKnew = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.knew_ptr)
827	                                                + row_offset_knew - binfo.seqlen_k_cache * params.knew_row_stride),
828	                                  Shape<Int<kBlockN>, Int<kHeadDim>>{},
829	                                  make_stride(params.knew_row_stride, _1{}));
830	        // if (threadIdx.x == 0 && blockIdx.y == 0 && blockIdx.z == 0) { printf("knew_ptr = %p, row_offset_knew = %d, gKnew_ptr = %p\n", params.knew_ptr, row_offset_knew, gKnew.data()); }
831	        Tensor gVnew = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.vnew_ptr)
832	                                                + row_offset_vnew - binfo.seqlen_k_cache * params.vnew_row_stride),
833	                                  Shape<Int<kBlockN>, Int<kHeadDim>>{},
834	                                  make_stride(params.vnew_row_stride, _1{}));
835	        Tensor tKgKnew = gmem_thr_copy_QKV.partition_S(gKnew);  // (KCPY, KCPY_N, KCPY_K)
836	        Tensor tVgVnew = gmem_thr_copy_QKV.partition_S(gVnew);  // (VCPY, VCPY_N, VCPY_K)
837	
838	        const int n_block_copy_min = std::max(n_block_min, binfo.seqlen_k_cache / kBlockN);
839	        auto tKgK_data = tKgK.data();
840	        auto tVgV_data = tVgV.data();
841	        for (int n_block = n_block_max - 1; n_block >= n_block_copy_min; n_block--) {
842	            flash::copy_w_min_idx<Is_even_K>(
843	                tVgVnew, tVgV, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN, binfo.seqlen_k_cache - n_block * kBlockN
844	            );
845	            tVgVnew.data() = tVgVnew.data() + (-int(kBlockN * params.vnew_row_stride));
846	            if (params.rotary_dim == 0) {
847	                flash::copy_w_min_idx<Is_even_K>(
848	                    tKgKnew, tKgK, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN, binfo.seqlen_k_cache - n_block * kBlockN
849	                );
850	            } else {
851	                if (params.is_rotary_interleaved) {
852	                    // Don't clear OOB_K because we're writing to global memory
853	                    flash::copy_rotary_interleaved<Is_even_K, /*Clear_OOB_K=*/false>(
854	                        tKgKnew, tKgK, tRgCos, tRgSin, tKVcKV, binfo.actual_seqlen_k - n_block * kBlockN,
855	                        binfo.seqlen_k_cache - n_block * kBlockN, params.d, params.rotary_dim
856	                    );
857	                    tRgCos.data() = tRgCos.data() + (-int(kBlockN * params.rotary_dim / 2));
858	                    tRgSin.data() = tRgSin.data() + (-int(kBlockN * params.rotary_dim / 2));
859	                } else {
860	                    // Don't clear OOB_K because we're writing to global memory
861	                    flash::copy_rotary_contiguous<Is_even_K, /*Clear_OOB_K=*/false>(
862	                        tKgKnew, tKgK, tRgCosCont, tRgSinCont, tKVcKV, binfo.actual_seqlen_k - n_block * kBlockN,
863	                        binfo.seqlen_k_cache - n_block * kBlockN, params.d, params.rotary_dim
864	                    );
865	                    tRgCosCont.data() = tRgCosCont.data() + (-int(kBlockN * params.rotary_dim / 2));
866	                    tRgSinCont.data() = tRgSinCont.data() + (-int(kBlockN * params.rotary_dim / 2));
867	
868	                }
869	            }
870	            tKgKnew.data() = tKgKnew.data() + (-int(kBlockN * params.knew_row_stride));
871	            if (block_table == nullptr) {
872	                tVgV.data() = tVgV.data() + (-int(kBlockN * params.v_row_stride));
873	                tKgK.data() = tKgK.data() + (-int(kBlockN * params.k_row_stride));
874	            } else {
875	                if (n_block > n_block_copy_min) {
876	                    const int block_table_idx_cur = n_block * kBlockN / params.page_block_size;
877	                    const int block_table_offset_cur = n_block * kBlockN - block_table_idx_cur * params.page_block_size;
878	                    const int block_table_idx_next = (n_block - 1) * kBlockN / params.page_block_size;
879	                    const int block_table_offset_next = (n_block - 1) * kBlockN - block_table_idx_next * params.page_block_size;
880	                    const int table_diff = block_table[block_table_idx_next] - block_table[block_table_idx_cur];
881	                    const int offset_diff = block_table_offset_next - block_table_offset_cur;
882	                    tVgV.data() = tVgV.data() + table_diff * params.v_batch_stride + offset_diff * params.v_row_stride;
883	                    tKgK.data() = tKgK.data() + table_diff * params.k_batch_stride + offset_diff * params.k_row_stride;
884	                }
885	            }
886	        }
887	        // Need this before we can read in K again, so that we'll see the updated K values.
888	        __syncthreads();
889	        tKgK.data() = tKgK_data;
890	        tVgV.data() = tVgV_data;
891	    }
892	
893	    // Read Q from gmem to smem, optionally apply rotary embedding.
894	    if (!Append_KV || params.rotary_dim == 0) {
895	        // We don't need to clear the sQ smem tiles since we'll only write out the valid outputs
896	        flash::copy<Is_even_MN, Is_even_K>(gmem_tiled_copy_QKV, tQgQ, tQsQ, tQcQ, tQpQ,
897	                                           binfo.actual_seqlen_q - m_block * kBlockM);
898	    } else {
899	        const index_t row_offset_cossin = (binfo.seqlen_k_cache + (params.leftpad_k == nullptr ? 0 : params.leftpad_k[bidb]) + (Is_causal || Is_local ? m_block * kBlockM : 0)) * (params.rotary_dim / 2);
900	        // If not causal, all the queries get the same the cos/sin, taken at location seqlen_k_cache.
901	        // We do this by setting the row stride of gCos / gSin to 0.
902	        Tensor gCos = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_cos_ptr) + row_offset_cossin),
903	                                  Shape<Int<kBlockM>, Int<kHeadDim / 2>>{},
904	                                  make_stride(Is_causal || Is_local ? params.rotary_dim / 2 : 0, _1{}));
905	        Tensor gSin = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_sin_ptr) + row_offset_cossin),
906	                                  Shape<Int<kBlockM>, Int<kHeadDim / 2>>{},
907	                                  make_stride(Is_causal || Is_local ? params.rotary_dim / 2 : 0, _1{}));
908	        Tensor gCosCont = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_cos_ptr) + row_offset_cossin),
909	                                  Shape<Int<kBlockM>, Int<kHeadDim>>{},
910	                                  make_stride(Is_causal || Is_local ? params.rotary_dim / 2 : 0, _1{}));
911	        Tensor gSinCont = make_tensor(make_gmem_ptr(reinterpret_cast<Element *>(params.rotary_sin_ptr) + row_offset_cossin),
912	                                  Shape<Int<kBlockM>, Int<kHeadDim>>{},
913	                                  make_stride(Is_causal || Is_local ? params.rotary_dim / 2 : 0, _1{}));
914	        Tensor tRgCos = gmem_thr_copy_rotary.partition_S(gCos);
915	        Tensor tRgSin = gmem_thr_copy_rotary.partition_S(gSin);
916	        Tensor tRgCosCont = gmem_thr_copy_rotary_cont.partition_S(gCosCont);
917	        Tensor tRgSinCont = gmem_thr_copy_rotary_cont.partition_S(gSinCont);
918	        if (params.is_rotary_interleaved) {
919	            flash::copy_rotary_interleaved<Is_even_K>(
920	                tQgQ, tQsQ, tRgCos, tRgSin, tQcQ, binfo.actual_seqlen_q - m_block * kBlockM,
921	                0, params.d, params.rotary_dim
922	            );
923	        } else {
924	            flash::copy_rotary_contiguous<Is_even_K>(
925	                tQgQ, tQsQ, tRgCosCont, tRgSinCont, tQcQ, binfo.actual_seqlen_q - m_block * kBlockM,
926	                0, params.d, params.rotary_dim
927	            );
928	        }
929	    }
930	
931	    int n_block = n_block_max - 1;
932	    // We don't need to clear the sK smem tiles since we'll mask out the scores anyway.
933	    flash::copy<Is_even_MN, Is_even_K>(gmem_tiled_copy_QKV, tKgK, tKsK, tKVcKV, tKVpKV,
934	                                       binfo.actual_seqlen_k - n_block * kBlockN);
935	    cute::cp_async_fence();
936	
937	    // flash::cp_async_wait<0>();
938	    // __syncthreads();
939	    // if (tidx == 0 && blockIdx.y == 0 && blockIdx.z == 0) { print(tKsK); }
940	    // __syncthreads();
941	
942	    clear(acc_o);
943	
944	    flash::Softmax<2 * size<1>(acc_o)> softmax;
945	
946	    const float alibi_slope = !Has_alibi ? 0.0f : reinterpret_cast<float *>(params.alibi_slopes_ptr)[bidb * params.alibi_slopes_batch_stride + bidh] / params.scale_softmax;
947	    flash::Mask<Is_causal, Is_local, Has_alibi> mask(binfo.actual_seqlen_k, binfo.actual_seqlen_q, params.window_size_left, params.window_size_right, alibi_slope, params.m_block_dim);
948	
949	    fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
950	    int next_block_idx = blockmask.max_no_larger(n_block_max-1);
951	    int leap = 0;
952	
953	    // For performance reason, we separate out two kinds of iterations:
954	    // those that need masking on S, and those that don't.
955	    // We need masking on S for the very last block when K and V has length not multiple of kBlockN.
956	    // We also need masking on S if it's causal, for the last ceil_div(kBlockM, kBlockN) blocks.
957	    // We will have at least 1 "masking" iteration.
958	
959	    // If not even_N, then seqlen_k might end in the middle of a block. In that case we need to
960	    // mask 2 blocks (e.g. when kBlockM == kBlockN), not just 1.
961	    constexpr int n_masking_steps = (!Is_causal && !Is_local)
962	        ? 1
963	        : ((Is_even_MN && Is_causal) ? cute::ceil_div(kBlockM, kBlockN) : cute::ceil_div(kBlockM, kBlockN) + 1);
964	    #pragma unroll
965	    for (int masking_step = 0; masking_step < n_masking_steps; ++masking_step, --n_block) {
966	        const bool skip = (n_block != next_block_idx);
967	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
968	        clear(acc_s);
969	        flash::cp_async_wait<0>();
970	        __syncthreads();
971	
972	        // Advance gV
973	        if (masking_step > 0) {
974	            if (block_table == nullptr) {
975	                tVgV.data() = tVgV.data() + (-int(kBlockN * params.v_row_stride));
976	            } else {
977	                const int block_table_idx_cur = (n_block + 1) * kBlockN / params.page_block_size;
978	                const int block_table_offset_cur = (n_block + 1) * kBlockN - block_table_idx_cur * params.page_block_size;
979	                const int block_table_idx_next = n_block * kBlockN / params.page_block_size;
980	                const int block_table_offset_next = n_block * kBlockN - block_table_idx_next * params.page_block_size;
981	                tVgV.data() = tVgV.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.v_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.v_row_stride;
982	            }
983	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV, tVsV, tKVcKV, tKVpKV);
984	        } else {
985	            // Clear the smem tiles to account for predicated off loads
986	            flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/true>(
987	                gmem_tiled_copy_QKV, tVgV, tVsV, tKVcKV, tKVpKV, binfo.actual_seqlen_k - n_block * kBlockN
988	            );
989	        }
990	        cute::cp_async_fence();
991	
992	        if (!skip) {
993	            flash::gemm(
994	                acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
995	                smem_thr_copy_Q, smem_thr_copy_K
996	            );
997	            // if (cute::thread0()) { print(acc_s); }
998	            if constexpr (Is_softcap){
999	                flash::apply_softcap(acc_s, params.softcap);
```

> AGENT

现在让我阅读剩余的内核文件并找到 `.cu` 文件。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h",
  "limit": 200,
  "offset": 1000
}
```

> TOOL

tool_result Read
```
1000	            }
1001	
1002	            mask.template apply_mask<Is_causal, Is_even_MN>(
1003	                acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
1004	            );
1005	
1006	            next_block_idx = blockmask.max_no_larger(n_block-1);
1007	        } else {
1008	            mask.all_mask(acc_s);
1009	        }
1010	
1011	        flash::cp_async_wait<0>();
1012	        __syncthreads();
1013	        // if (tidx == 0 && blockIdx.y == 0 && blockIdx.z == 0) { print(tVsV); }
1014	        // __syncthreads();
1015	
1016	        leap = (masking_step + 1 == n_masking_steps) ? n_block - next_block_idx : 1;
1017	
1018	        if (n_block > n_block_min && next_block_idx != -1) {
1019	            // Advance gK
1020	            if (block_table == nullptr) {
1021	                tKgK.data() = tKgK.data() + (-int(kBlockN * leap * params.k_row_stride));
1022	            } else {
1023	                const int block_table_idx_cur = n_block * kBlockN / params.page_block_size;
1024	                const int block_table_offset_cur = n_block * kBlockN - block_table_idx_cur * params.page_block_size;
1025	                const int block_table_idx_next = (n_block - leap) * kBlockN / params.page_block_size;
1026	                const int block_table_offset_next =(n_block - leap) * kBlockN - block_table_idx_next * params.page_block_size;
1027	                tKgK.data() = tKgK.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.k_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.k_row_stride;
1028	            }
1029	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK, tKsK, tKVcKV, tKVpKV);
1030	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
1031	            // isn't right and we get race conditions.
1032	            cute::cp_async_fence();
1033	        }
1034	
1035	        // We have key_padding_mask so we'll need to Check_inf
1036	        masking_step == 0
1037	            ? softmax.template softmax_rescale_o</*Is_first=*/true,  /*Check_inf=*/Is_causal || Is_local || !Is_even_MN>(acc_s, acc_o, params.scale_softmax_log2)
1038	            : softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_causal || Is_local || !Is_even_MN>(acc_s, acc_o, params.scale_softmax_log2);
1039	        // if (cute::thread0()) { print(scores_max); print(scores_sum); print(scores); }
1040	
1041	        if (!skip) {
1042	            // Convert acc_s from fp32 to fp16/bf16
1043	            Tensor rP = flash::convert_type<Element>(acc_s);
1044	            // Reshape rP from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
1045	            // if using m16n8k16 or (4, MMA_M, MMA_N) if using m16n8k8.
1046	            Tensor tOrP = make_tensor(rP.data(), flash::convert_layout_acc_Aregs<Kernel_traits::TiledMma>(rP.layout()));
1047	
1048	            flash::gemm_rs(acc_o, tOrP, tOrVt, tOsVt, tiled_mma, smem_tiled_copy_V, smem_thr_copy_V);
1049	        }
1050	
1051	        // This check is at the end of the loop since we always have at least 1 iteration
1052	        if (n_masking_steps > 1 && n_block <= n_block_min) {
1053	            --n_block;
1054	            break;
1055	        }
1056	    }
1057	
1058	    leap = n_block - next_block_idx + 1;
1059	
1060	    // These are the iterations where we don't need masking on S
1061	    for (n_block = next_block_idx; n_block != -1 && n_block >= n_block_min; n_block = next_block_idx) {
1062	        next_block_idx = blockmask.max_no_larger(n_block - 1);
1063	
1064	        Tensor acc_s = partition_fragment_C(tiled_mma, Shape<Int<kBlockM>, Int<kBlockN>>{});  // (MMA=4, MMA_M, MMA_N)
1065	        clear(acc_s);
1066	        flash::cp_async_wait<0>();
1067	        __syncthreads();
1068	        // Advance gV
1069	        if (block_table == nullptr) {
1070	            tVgV.data() = tVgV.data() + (-int(kBlockN * leap * params.v_row_stride));
1071	        } else {
1072	            const int block_table_idx_cur = (n_block + leap) * kBlockN / params.page_block_size;
1073	            const int block_table_offset_cur = (n_block + leap) * kBlockN - block_table_idx_cur * params.page_block_size;
1074	            const int block_table_idx_next = n_block * kBlockN / params.page_block_size;
1075	            const int block_table_offset_next = n_block * kBlockN - block_table_idx_next * params.page_block_size;
1076	            tVgV.data() = tVgV.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.v_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.v_row_stride;
1077	        }
1078	        flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tVgV, tVsV, tKVcKV, tKVpKV);
1079	        cute::cp_async_fence();
1080	
1081	        flash::gemm(
1082	            acc_s, tSrQ, tSrK, tSsQ, tSsK, tiled_mma, smem_tiled_copy_Q, smem_tiled_copy_K,
1083	            smem_thr_copy_Q, smem_thr_copy_K
1084	        );
1085	        if constexpr (Is_softcap){
1086	            flash::apply_softcap(acc_s, params.softcap);
1087	        }
1088	
1089	        flash::cp_async_wait<0>();
1090	        __syncthreads();
1091	
1092	        leap = n_block - next_block_idx;        
1093	        if (next_block_idx != -1) {
1094	            // Advance gK
1095	            if (block_table == nullptr) {
1096	                tKgK.data() = tKgK.data() + (-int(kBlockN * leap * params.k_row_stride));
1097	            } else {
1098	                const int block_table_idx_cur = n_block * kBlockN / params.page_block_size;
1099	                const int block_table_offset_cur = n_block * kBlockN - block_table_idx_cur * params.page_block_size;
1100	                const int block_table_idx_next = (n_block - leap) * kBlockN / params.page_block_size;
1101	                const int block_table_offset_next = (n_block - leap) * kBlockN - block_table_idx_next * params.page_block_size;
1102	                tKgK.data() = tKgK.data() + (block_table[block_table_idx_next] - block_table[block_table_idx_cur]) * params.k_batch_stride + (block_table_offset_next - block_table_offset_cur) * params.k_row_stride;
1103	            }
1104	            flash::copy</*Is_even_MN=*/true, Is_even_K>(gmem_tiled_copy_QKV, tKgK, tKsK, tKVcKV, tKVpKV);
1105	            // This cp_async_fence needs to be in the if block, otherwise the synchronization
1106	            // isn't right and we get race conditions.
1107	            cute::cp_async_fence();
1108	        }
1109	
1110	        mask.template apply_mask</*Causal_mask=*/false>(
1111	            acc_s, n_block * kBlockN, m_block * kBlockM + (tidx / 32) * 16 + (tidx % 32) / 4, kNWarps * 16
1112	        );
1113	        softmax.template softmax_rescale_o</*Is_first=*/false, /*Check_inf=*/Is_local>(acc_s, acc_o, params.scale_softmax_log2);
1114	
1115	        Tensor rP = flash::convert_type<Element>(acc_s);
1116	        // Reshape rP from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
1117	        // if using m16n8k16 or (4, MMA_M, MMA_N) if using m16n8k8.
1118	        Tensor tOrP = make_tensor(rP.data(), flash::convert_layout_acc_Aregs<Kernel_traits::TiledMma>(rP.layout()));
1119	
1120	        flash::gemm_rs(acc_o, tOrP, tOrVt, tOsVt, tiled_mma, smem_tiled_copy_V, smem_thr_copy_V);
1121	    }
1122	
1123	    // Epilogue
1124	
1125	    Tensor lse = softmax.template normalize_softmax_lse</*Is_dropout=*/false, Split>(acc_o, params.scale_softmax);
1126	    // if (cute::thread0()) { print(lse); }
1127	
1128	    Tensor sOaccum = make_tensor(make_smem_ptr(reinterpret_cast<ElementO *>(smem_)), typename Kernel_traits::SmemLayoutO{}); // (SMEM_M,SMEM_N)
1129	    // Partition sO to match the accumulator partitioning
1130	    using SmemTiledCopyO = std::conditional_t<
1131	        !Split,
1132	        typename Kernel_traits::SmemCopyAtomO,
1133	        typename Kernel_traits::SmemCopyAtomOaccum
1134	    >;
1135	    auto smem_tiled_copy_Oaccum = make_tiled_copy_C(SmemTiledCopyO{}, tiled_mma);
1136	    auto smem_thr_copy_Oaccum = smem_tiled_copy_Oaccum.get_thread_slice(tidx);
1137	    Tensor rO = flash::convert_type<ElementO>(acc_o);
1138	    Tensor taccOrOaccum = smem_thr_copy_Oaccum.retile_S(rO);        // ((Atom,AtomNum), MMA_M, MMA_N)
1139	    Tensor taccOsOaccum = smem_thr_copy_Oaccum.partition_D(sOaccum);     // ((Atom,AtomNum),PIPE_M,PIPE_N)
1140	
1141	    // sOaccum is larger than sQ, so we need to syncthreads here
1142	    // TODO: allocate enough smem for sOaccum
1143	    if constexpr (Split) { __syncthreads(); }
1144	
1145	    cute::copy(smem_tiled_copy_Oaccum, taccOrOaccum, taccOsOaccum);
1146	
1147	    const index_t row_offset_o = binfo.q_offset(params.o_batch_stride, params.o_row_stride, bidb)
1148	        + m_block * kBlockM * params.o_row_stride + bidh * params.o_head_stride;
1149	    const index_t row_offset_oaccum = (((n_split_idx * params.b + bidb) * params.h + bidh) * params.seqlen_q
1150	                                         + m_block * kBlockM) * params.d_rounded;
1151	    const index_t row_offset_lseaccum = (Split || !params.unpadded_lse ?
1152	            ((n_split_idx * params.b + bidb) * params.h + bidh) * params.seqlen_q : bidh * params.total_q + binfo.q_offset(params.seqlen_q, 1, bidb)
1153	        ) + m_block * kBlockM;
1154	
1155	    Tensor gOaccum = make_tensor(make_gmem_ptr(reinterpret_cast<ElementO *>(Split ? params.oaccum_ptr : params.o_ptr) + (Split ? row_offset_oaccum : row_offset_o)),
1156	                                 Shape<Int<kBlockM>, Int<kHeadDim>>{},
1157	                                 make_stride(Split ? kHeadDim : params.o_row_stride, _1{}));
1158	    Tensor gLSEaccum = make_tensor(make_gmem_ptr(reinterpret_cast<ElementAccum *>(Split ? params.softmax_lseaccum_ptr : params.softmax_lse_ptr) + row_offset_lseaccum),
1159	                                   Shape<Int<kBlockM>>{}, Stride<_1>{});
1160	    // if (tidx == 0) { printf("row_offset_o = %d, bidh = %d, gOaccum = %p\n", row_offset_o, bidh, gOaccum.data()); }
1161	
1162	    GmemTiledCopyO gmem_tiled_copy_Oaccum;
1163	    auto gmem_thr_copy_Oaccum = gmem_tiled_copy_Oaccum.get_thread_slice(tidx);
1164	    Tensor tOsOaccum = gmem_thr_copy_Oaccum.partition_S(sOaccum);        // ((Atom,AtomNum),ATOM_M,ATOM_N)
1165	    Tensor tOgOaccum = gmem_thr_copy_Oaccum.partition_D(gOaccum);
1166	
1167	    __syncthreads();
1168	
1169	    Tensor tOrOaccum = make_tensor<ElementO>(shape(tOgOaccum));
1170	    cute::copy(gmem_tiled_copy_Oaccum, tOsOaccum, tOrOaccum);
1171	
1172	    Tensor caccO = make_identity_tensor(Shape<Int<kBlockM>, Int<kHeadDim>>{});    // (BLK_M,BLK_K) -> (blk_m,blk_k)
1173	    Tensor taccOcO = thr_mma.partition_C(caccO);                           // (MMA,MMA_M,MMA_K)
1174	    static_assert(decltype(size<0>(taccOcO))::value == 4);
1175	    // Convert to ((2, 2), MMA_M, MMA_K) then take only the row indices.
1176	    Tensor taccOcO_row = logical_divide(taccOcO, Shape<_2>{})(make_coord(0, _), _, 0);
1177	    CUTE_STATIC_ASSERT_V(size(lse) == size(taccOcO_row));                     // MMA_M
1178	    if (get<1>(taccOcO_row(0)) == 0) {
1179	        #pragma unroll
1180	        for (int mi = 0; mi < size(lse); ++mi) {
1181	            const int row = get<0>(taccOcO_row(mi));
1182	            if (row < binfo.actual_seqlen_q - m_block * kBlockM) { gLSEaccum(row) = lse(mi); }
1183	        }
1184	    }
1185	
1186	    // Construct identity layout for sO
1187	    Tensor cO = make_identity_tensor(make_shape(size<0>(sOaccum), size<1>(sOaccum)));    // (BLK_M,BLK_K) -> (blk_m,blk_k)
1188	    // Repeat the partitioning with identity layouts
1189	    Tensor tOcO = gmem_thr_copy_Oaccum.partition_D(cO);                           // (ACPY,ACPY_M,ACPY_K) -> (blk_m,blk_k)
1190	    Tensor tOpO = make_tensor<bool>(make_shape(size<2>(tOgOaccum)));
1191	    if (!Is_even_K) {
1192	        #pragma unroll
1193	        for (int k = 0; k < size(tOpO); ++k) { tOpO(k) = get<1>(tOcO(0, 0, k)) < params.d; }
1194	    }
1195	    // Clear_OOB_K must be false since we don't want to write zeros to gmem
1196	    flash::copy<Is_even_MN, Is_even_K, /*Clear_OOB_MN=*/false, /*Clear_OOB_K=*/false>(
1197	        gmem_tiled_copy_Oaccum, tOrOaccum, tOgOaccum, tOcO, tOpO, binfo.actual_seqlen_q - m_block * kBlockM
1198	    );
1199	}
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn -name \"flash_fwd_hdim*_sm*.cu\" -o -name \"flash_fwd_*.cu\" | sort",
  "description": "Find all flash_fwd .cu files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim160_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim192_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim224_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim256_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim32_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim64_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim96_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim224_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_causal_sm80.cu
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_sm80.cu
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name \"setup.py\" -path \"*/infllmv2*\" | head -5",
  "description": "Find setup.py"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/setup.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu"
}
```

> TOOL

tool_result Read
```
1	// Copyright (c) 2024, Tri Dao.
2	// Splitting the different head dimensions to different files to speed up compilation.
3	// This file is auto-generated. See "generate_kernels.py"
4	
5	#include "flash_fwd_launch_template.h"
6	
7	template<>
8	void run_mha_fwd_<cutlass::half_t, 128, false>(Flash_fwd_params &params, cudaStream_t stream) {
9	    run_mha_fwd_hdim128<cutlass::half_t, false>(params, stream);
10	}
11
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/setup.py"
}
```

> TOOL

tool_result Read
```
1	import sys
2	import warnings
3	import os
4	import re
5	import ast
6	from pathlib import Path
7	from packaging.version import parse, Version
8	import platform
9	
10	from setuptools import setup, find_packages
11	import subprocess
12	
13	import torch
14	from torch.utils.cpp_extension import (
15	    BuildExtension,
16	    CppExtension,
17	    CUDAExtension,
18	    CUDA_HOME,
19	)
20	
21	# ninja build does not work unless include_dirs are abs path
22	this_dir = os.path.dirname(os.path.abspath(__file__))
23	
24	# FORCE_BUILD: Force a fresh build locally
25	# SKIP_CUDA_BUILD: Intended to allow CI to use a simple `python setup.py sdist` run to copy over raw files, without any cuda compilation
26	FORCE_BUILD = os.getenv("INFLLM_V2_FORCE_BUILD", "FALSE") == "TRUE"
27	SKIP_CUDA_BUILD = os.getenv("INFLLM_V2_SKIP_CUDA_BUILD", "FALSE") == "TRUE"
28	# For CI, we want the option to build with C++11 ABI since the nvcr images use C++11 ABI
29	FORCE_CXX11_ABI = os.getenv("INFLLM_V2_FORCE_CXX11_ABI", "FALSE") == "TRUE"
30	
31	def get_cuda_bare_metal_version(cuda_dir):
32	    raw_output = subprocess.check_output([cuda_dir + "/bin/nvcc", "-V"], universal_newlines=True)
33	    output = raw_output.split()
34	    release_idx = output.index("release") + 1
35	    bare_metal_version = parse(output[release_idx].split(",")[0])
36	
37	    return raw_output, bare_metal_version
38	
39	def check_if_cuda_home_none(global_option: str) -> None:
40	    if CUDA_HOME is not None:
41	        return
42	    # warn instead of error because user could be downloading prebuilt wheels, so nvcc won't be necessary.
43	    warnings.warn(
44	        f"{global_option} was requested, but nvcc was not found.  Are you sure your environment has nvcc available?  "
45	        "If you're installing within a container from https://hub.docker.com/r/pytorch/pytorch, "
46	        "only images whose names contain 'devel' will provide nvcc."
47	    )
48	
49	def append_nvcc_threads(nvcc_extra_args):
50	    # Increase thread count based on available CPU cores
51	    import multiprocessing
52	    num_threads = min(multiprocessing.cpu_count(), 8)  # Use up to 8 threads
53	    return nvcc_extra_args + ["--threads", str(num_threads)]
54	
55	class NinjaBuildExtension(BuildExtension):
56	    def __init__(self, *args, **kwargs) -> None:
57	        # do not override env MAX_JOBS if already exists
58	        if not os.environ.get("MAX_JOBS"):
59	            import psutil
60	
61	            # calculate the maximum allowed NUM_JOBS based on cores
62	            max_num_jobs_cores = max(1, os.cpu_count() // 2)
63	
64	            # calculate the maximum allowed NUM_JOBS based on free memory
65	            free_memory_gb = psutil.virtual_memory().available / (1024 ** 3)  # free memory in GB
66	            max_num_jobs_memory = int(free_memory_gb / 9)  # each JOB peak memory cost is ~8-9GB when threads = 4
67	
68	            # pick lower value of jobs based on cores vs memory metric to minimize oom and swap usage during compilation
69	            max_jobs = max(1, min(max_num_jobs_cores, max_num_jobs_memory))
70	            os.environ["MAX_JOBS"] = str(max_jobs)
71	
72	        super().__init__(*args, **kwargs)
73	
74	cmdclass = {}
75	ext_modules = []
76	
77	if not SKIP_CUDA_BUILD:
78	    print("\n\ntorch.__version__  = {}\n\n".format(torch.__version__))
79	    TORCH_MAJOR = int(torch.__version__.split(".")[0])
80	    TORCH_MINOR = int(torch.__version__.split(".")[1])
81	
82	    # Check, if ATen/CUDAGeneratorImpl.h is found, otherwise use ATen/cuda/CUDAGeneratorImpl.h
83	    # See https://github.com/pytorch/pytorch/pull/70650
84	    generator_flag = []
85	    torch_dir = torch.__path__[0]
86	    if os.path.exists(os.path.join(torch_dir, "include", "ATen", "CUDAGeneratorImpl.h")):
87	        generator_flag = ["-DOLD_GENERATOR_PATH"]
88	
89	    check_if_cuda_home_none("infllm_v2")
90	    # Check, if CUDA11 is installed for compute capability 8.0
91	    cc_flag = []
92	    if CUDA_HOME is not None:
93	        _, bare_metal_version = get_cuda_bare_metal_version(CUDA_HOME)
94	        if bare_metal_version < Version("11.6"):
95	            raise RuntimeError(
96	                "InfLLM V2 is only supported on CUDA 11.6 and above.  "
97	                "Note: make sure nvcc has a supported version by running nvcc -V."
98	            )
99	    
100	    # Auto-detect supported GPU archs based on CUDA toolkit version
101	    # 80: A100 (Ampere), 90: H100 (Hopper, CUDA 11.8+), 120: B100/B200 (Blackwell, CUDA 12.8+)
102	    supported_archs = ["80"]
103	    if CUDA_HOME is not None:
104	        if bare_metal_version >= Version("11.8"):
105	            supported_archs.append("90")
106	        if bare_metal_version >= Version("12.8"):
107	            supported_archs.append("120")
108	
109	    for arch in supported_archs:
110	        cc_flag.extend(["-gencode", f"arch=compute_{arch},code=sm_{arch}"])
111	
112	    # HACK: The compiler flag -D_GLIBCXX_USE_CXX11_ABI is set to be the same as
113	    # torch._C._GLIBCXX_USE_CXX11_ABI
114	    if FORCE_CXX11_ABI:
115	        torch._C._GLIBCXX_USE_CXX11_ABI = True
116	    
117	    # Flash Attention CUDA源文件列表 - 只编译 hdim128, bf16 版本
118	    flash_attn_sources = [
119	                # "csrc/flash_attn/src/flash_fwd_hdim32_fp16_sm80.cu",
120	                # "csrc/flash_attn/src/flash_fwd_hdim32_bf16_sm80.cu",
121	                # "csrc/flash_attn/src/flash_fwd_hdim64_fp16_sm80.cu",
122	                "csrc/flash_attn/src/flash_fwd_hdim64_bf16_sm80.cu",
123	                # "csrc/flash_attn/src/flash_fwd_hdim96_fp16_sm80.cu",
124	                # "csrc/flash_attn/src/flash_fwd_hdim96_bf16_sm80.cu",
125	                # "csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu",
126	                "csrc/flash_attn/src/flash_fwd_hdim128_bf16_sm80.cu",
127	                # "csrc/flash_attn/src/flash_fwd_hdim160_fp16_sm80.cu",
128	                # "csrc/flash_attn/src/flash_fwd_hdim160_bf16_sm80.cu",
129	                # "csrc/flash_attn/src/flash_fwd_hdim192_fp16_sm80.cu",
130	                # "csrc/flash_attn/src/flash_fwd_hdim192_bf16_sm80.cu",
131	                # "csrc/flash_attn/src/flash_fwd_hdim256_fp16_sm80.cu",
132	                # "csrc/flash_attn/src/flash_fwd_hdim256_bf16_sm80.cu",
133	                # "csrc/flash_attn/src/flash_fwd_hdim32_fp16_causal_sm80.cu",
134	                # "csrc/flash_attn/src/flash_fwd_hdim32_bf16_causal_sm80.cu",
135	                # "csrc/flash_attn/src/flash_fwd_hdim64_fp16_causal_sm80.cu",
136	                "csrc/flash_attn/src/flash_fwd_hdim64_bf16_causal_sm80.cu",
137	                # "csrc/flash_attn/src/flash_fwd_hdim96_fp16_causal_sm80.cu",
138	                # "csrc/flash_attn/src/flash_fwd_hdim96_bf16_causal_sm80.cu",
139	                # "csrc/flash_attn/src/flash_fwd_hdim128_fp16_causal_sm80.cu",
140	                "csrc/flash_attn/src/flash_fwd_hdim128_bf16_causal_sm80.cu",
141	                # "csrc/flash_attn/src/flash_fwd_hdim160_fp16_causal_sm80.cu",
142	                # "csrc/flash_attn/src/flash_fwd_hdim160_bf16_causal_sm80.cu",
143	                # "csrc/flash_attn/src/flash_fwd_hdim192_fp16_causal_sm80.cu",
144	                # "csrc/flash_attn/src/flash_fwd_hdim192_bf16_causal_sm80.cu",
145	                # "csrc/flash_attn/src/flash_fwd_hdim256_fp16_causal_sm80.cu",
146	                # "csrc/flash_attn/src/flash_fwd_hdim256_bf16_causal_sm80.cu",
147	                # "csrc/flash_attn/src/flash_bwd_hdim32_fp16_sm80.cu",
148	                # "csrc/flash_attn/src/flash_bwd_hdim32_bf16_sm80.cu",
149	                # "csrc/flash_attn/src/flash_bwd_hdim64_fp16_sm80.cu",
150	                "csrc/flash_attn/src/flash_bwd_hdim64_bf16_sm80.cu",
151	                # "csrc/flash_attn/src/flash_bwd_hdim96_fp16_sm80.cu",
152	                # "csrc/flash_attn/src/flash_bwd_hdim96_bf16_sm80.cu",
153	                # "csrc/flash_attn/src/flash_bwd_hdim128_fp16_sm80.cu",
154	                "csrc/flash_attn/src/flash_bwd_hdim128_bf16_sm80.cu",
155	                # "csrc/flash_attn/src/flash_bwd_hdim160_fp16_sm80.cu",
156	                # "csrc/flash_attn/src/flash_bwd_hdim160_bf16_sm80.cu",
157	                # "csrc/flash_attn/src/flash_bwd_hdim192_fp16_sm80.cu",
158	                # "csrc/flash_attn/src/flash_bwd_hdim192_bf16_sm80.cu",
159	                # "csrc/flash_attn/src/flash_bwd_hdim256_fp16_sm80.cu",
160	                # "csrc/flash_attn/src/flash_bwd_hdim256_bf16_sm80.cu",
161	                # "csrc/flash_attn/src/flash_bwd_hdim32_fp16_causal_sm80.cu",
162	                # "csrc/flash_attn/src/flash_bwd_hdim32_bf16_causal_sm80.cu",
163	                # "csrc/flash_attn/src/flash_bwd_hdim64_fp16_causal_sm80.cu",
164	                "csrc/flash_attn/src/flash_bwd_hdim64_bf16_causal_sm80.cu",
165	                # "csrc/flash_attn/src/flash_bwd_hdim96_fp16_causal_sm80.cu",
166	                # "csrc/flash_attn/src/flash_bwd_hdim96_bf16_causal_sm80.cu",
167	                # "csrc/flash_attn/src/flash_bwd_hdim128_fp16_causal_sm80.cu",
168	                "csrc/flash_attn/src/flash_bwd_hdim128_bf16_causal_sm80.cu",
169	                # "csrc/flash_attn/src/flash_bwd_hdim160_fp16_causal_sm80.cu",
170	                # "csrc/flash_attn/src/flash_bwd_hdim160_bf16_causal_sm80.cu",
171	                # "csrc/flash_attn/src/flash_bwd_hdim192_fp16_causal_sm80.cu",
172	                # "csrc/flash_attn/src/flash_bwd_hdim192_bf16_causal_sm80.cu",
173	                # "csrc/flash_attn/src/flash_bwd_hdim256_fp16_causal_sm80.cu",
174	                # "csrc/flash_attn/src/flash_bwd_hdim256_bf16_causal_sm80.cu",
175	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_sm80.cu",
176	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_sm80.cu",
177	                # "csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_sm80.cu",
178	                "csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_sm80.cu",
179	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_sm80.cu",
180	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_sm80.cu",
181	                # "csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_sm80.cu",
182	                "csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_sm80.cu",
183	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_sm80.cu",
184	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_sm80.cu",
185	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_sm80.cu",
186	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_sm80.cu",
187	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_sm80.cu",
188	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_sm80.cu",
189	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_fp16_causal_sm80.cu",
190	                # "csrc/flash_attn/src/flash_fwd_split_hdim32_bf16_causal_sm80.cu",
191	                # "csrc/flash_attn/src/flash_fwd_split_hdim64_fp16_causal_sm80.cu",
192	                "csrc/flash_attn/src/flash_fwd_split_hdim64_bf16_causal_sm80.cu",
193	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_fp16_causal_sm80.cu",
194	                # "csrc/flash_attn/src/flash_fwd_split_hdim96_bf16_causal_sm80.cu",
195	                # "csrc/flash_attn/src/flash_fwd_split_hdim128_fp16_causal_sm80.cu",
196	                "csrc/flash_attn/src/flash_fwd_split_hdim128_bf16_causal_sm80.cu",
197	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_fp16_causal_sm80.cu",
198	                # "csrc/flash_attn/src/flash_fwd_split_hdim160_bf16_causal_sm80.cu",
199	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_fp16_causal_sm80.cu",
200	                # "csrc/flash_attn/src/flash_fwd_split_hdim192_bf16_causal_sm80.cu",
201	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_fp16_causal_sm80.cu",
202	                # "csrc/flash_attn/src/flash_fwd_split_hdim256_bf16_causal_sm80.cu",
203	    ]
204	    
205	    # 过滤掉不存在的文件
206	    existing_flash_attn_sources = []
207	    for source in flash_attn_sources:
208	        if os.path.exists(source):
209	            existing_flash_attn_sources.append(source)
210	    
211	    ext_modules.append(
212	        CUDAExtension(
213	            name="infllm_v2.C",
214	            sources=[
215	                "csrc/entry.cu",
216	                "csrc/flash_attn/flash_api.cpp",
217	            ] + existing_flash_attn_sources,
218	            extra_compile_args={
219	                "cxx": ["-O3", "-std=c++17"],
220	                "nvcc": append_nvcc_threads(
221	                    [
222	                        "-O3",
223	                        "-std=c++17",
224	                        "-U__CUDA_NO_HALF_OPERATORS__",
225	                        "-U__CUDA_NO_HALF_CONVERSIONS__",
226	                        "-U__CUDA_NO_HALF2_OPERATORS__",
227	                        "-U__CUDA_NO_BFLOAT16_CONVERSIONS__",
228	                        "--expt-relaxed-constexpr",
229	                        "--expt-extended-lambda",
230	                        "--use_fast_math",
231	                        # "--ptxas-options=-v",
232	                        # "--ptxas-options=-O2",
233	                        # "-lineinfo",
234	                        # "-DFLASHATTENTION_DISABLE_BACKWARD",
235	                        "-DFLASHATTENTION_DISABLE_DROPOUT",
236	                        "-DFLASHATTENTION_DISABLE_ALIBI",
237	                        "-DFLASHATTENTION_DISABLE_SOFTCAP",
238	                        "-DFLASHATTENTION_DISABLE_UNEVEN_K",
239	                        "-DFLASHATTENTION_DISABLE_LOCAL",
240	                    ]
241	                    + cc_flag
242	                ),
243	            },
244	            include_dirs=[
245	                Path(this_dir) / "csrc" / "flash_attn",
246	                Path(this_dir) / "csrc" / "flash_attn" / "src", 
247	                Path(this_dir) / "csrc" / "cutlass" / "include",
248	                # Path(this_dir) / "3rd" / "cutlass" / "include",
249	            ],
250	        )
251	    )
252	
253	setup(
254	    name='infllm_v2',
255	    version='0.0.0',
256	    author_email="[REDACTED]",
257	    description="infllm_v2 cuda implementation with flash attention and cutlass",
258	    packages=find_packages(),
259	    ext_modules=ext_modules,
260	    cmdclass={"build_ext": NinjaBuildExtension} if ext_modules else {},
261	    python_requires=">=3.7",
262	    install_requires=[
263	        "torch",
264	        "packaging",
265	        "psutil",
266	    ],
267	) 
268
```

> AGENT

现在让我检查 CUTLASS 版本并查看可用的 SM120 相关定义。

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass/include/ | head -30",
  "description": "List CUTLASS include directory"
}
```

> TOOL

tool_result Bash
```
ls: cannot access '/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass/include/': No such file or directory
```

> TOOL

tool_use Bash
```json
{
  "command": "head -5 /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass/include/cutlass/version.h 2>/dev/null || echo \"no version.h\"",
  "description": "Check CUTLASS version"
}
```

> TOOL

tool_result Bash
```
no version.h
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16_F32F16F16F32\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass/include/ --include=\"*.hpp\" --include=\"*.h\" -l 2>/dev/null | head -5",
  "description": "Find wgmma MMA atom definitions"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass -maxdepth 1 -type d 2>/dev/null; find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name \"cutlass\" -type d 2>/dev/null | head -5",
  "description": "Find CUTLASS directory"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name \"arch\" -path \"*/cutlass/*\" -type d 2>/dev/null | head -5",
  "description": "Find CUTLASS arch directory"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name \"cutlass\" -type d 2>/dev/null; find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name \"cute\" -type d 2>/dev/null | head -5",
  "description": "Find CUTLASS/CuTe directories"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -maxdepth 4 -type d | head -30",
  "description": "List directory structure"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/tests/stage1
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"import cutlass; print(cutlass.__path__)\" 2>/dev/null; find /usr -name \"cutlass\" -path \"*/include/*\" -type d 2>/dev/null | head -5; find /usr/local -name \"cutlass\" -type d 2>/dev/null | head -5",
  "description": "Find system CUTLASS installation"
}
```

> TOOL

tool_result Bash
```
[[REDACTED]]
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"import torch; print(torch.__version__); print(torch.utils.cmake_prefix_path)\" 2>/dev/null",
  "description": "Get torch version and cmake path"
}
```

> TOOL

tool_result Bash
```
2.11.0+cu130
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/torch/share/cmake
```

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages -name \"cutlass\" -type d -maxdepth 5 2>/dev/null | head -5",
  "description": "Find cutlass in python packages"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/deep_gemm/include/cutlass
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/nvidia_cutlass_dsl/python_packages/cutlass
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/tilelang/3rdparty/cutlass
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/tilelang/3rdparty/cutlass/include/cutlass
```

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env -path \"*/cutlass/include/cutlass/arch\" -type d 2>/dev/null | head -5",
  "description": "Find CUTLASS arch include dir"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/tilelang/3rdparty/cutlass/include/cutlass/arch
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM120\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch/ --include=\"*.h\" -l 2>/dev/null | head -5",
  "description": "Search for SM120 in flashinfer's CUTLASS"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch/grid_dependency_control.h
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch/config.h
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch/reg_reconfig.h
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/ --include=\"*.h\" -l 2>/dev/null | head -5",
  "description": "Search for wgmma MMA atoms in flashinfer's CUTLASS"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "nvcc --version 2>/dev/null; echo \"---\"; ls /usr/local/cuda/include/cutlass/arch/ 2>/dev/null | head -10",
  "description": "Check nvcc version and system CUTLASS"
}
```

> TOOL

tool_result Bash
```
---
```

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include -name \"mma_sm90*\" -o -name \"mma_sm120*\" 2>/dev/null | head -10",
  "description": "Find MMA atom definitions for SM90/120"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120_sparse.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_desc.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma_ext.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma_sparse.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma_sparse_ext.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cutlass/arch/mma_sm90.h
```

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch -name \"*.hpp\" 2>/dev/null | head -20",
  "description": "List CuTe arch files"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/cluster_sm100.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/cluster_sm90.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/config.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm100.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm100_tma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm50.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm75.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm80.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm90.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm90_desc.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/copy_sm90_tma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_desc.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120_sparse.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm61.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm70.hpp
```

> AGENT

太棒了！让我阅读关键文件——SM120 MMA 定义和 SM100/SM120 的 TMA/COPY 定义。

> TOOL

tool_use Read
```json
{
  "file_path": "/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	/***************************************************************************************************
2	 * Copyright (c) 2025 - 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
3	 * SPDX-License-Identifier: BSD-3-Clause
4	 *
5	 * Redistribution and use in source and binary forms, with or without
6	 * modification, are permitted provided that the following conditions are met:
7	 *
8	 * 1. Redistributions of source code must retain the above copyright notice, this
9	 * list of conditions and the following disclaimer.
10	 *
11	 * 2. Redistributions in binary form must reproduce the above copyright notice,
12	 * this list of conditions and the following disclaimer in the documentation
13	 * and/or other materials provided with the distribution.
14	 *
15	 * 3. Neither the name of the copyright holder nor the names of its
16	 * contributors may be used to endorse or promote products derived from
17	 * this software without specific prior written permission.
18	 *
19	 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
20	 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
21	 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
22	 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
23	 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
24	 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
25	 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
26	 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
27	 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
28	 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
29	 *
30	 **************************************************************************************************/
31	
32	
33	#pragma once
34	
35	#include <cute/arch/config.hpp>
36	#include <cute/arch/mma.hpp>
37	#include <cute/numeric/numeric_types.hpp> // cute::float_e4m3_t, etc
38	#include <cutlass/detail/dependent_false.hpp>
39	
40	namespace cute {
41	
42	////////////////////////////////////////////////////////////////////////////////////////////////////
43	
44	template <class a_type, class b_type, class c_type>
45	struct SM120_16x8x32_TN
46	{
47	  static_assert(cutlass::detail::dependent_false<a_type>, "No MMA matches SM120_16x8x32_TN for given data types.");
48	};
49	
50	
51	////////////////////////////////////////////////////////////////////////////////////////////////////
52	
53	// MMA 16x8x32 TN E2M1 x E2M1
54	template <>
55	struct SM120_16x8x32_TN<float_e2m1_t, float_e2m1_t, float>
56	{
57	  using DRegisters = float[4];
58	  using ARegisters = uint32_t[4];
59	  using BRegisters = uint32_t[2];
60	  using CRegisters = float[4];
61	
62	  CUTE_HOST_DEVICE static void
63	  fma(float         & d0, float         & d1, float         & d2, float         & d3,
64	      uint32_t const& a0, uint32_t const& a1, uint32_t const& a2, uint32_t const& a3,
65	      uint32_t const& b0, uint32_t const& b1,
66	      float const   & c0, float const   & c1, float const   & c2, float const   & c3)
67	  {
68	#if defined(CUTE_ARCH_F8F6F4_MMA_ENABLED)
69	    asm volatile(
70	      "mma.sync.aligned.kind::f8f6f4.m16n8k32.row.col.f32.e2m1.e2m1.f32 "
71	      "{%0,  %1,  %2,  %3},"
72	      "{%4,  %5,  %6,  %7},"
73	      "{%8,  %9},"
74	      "{%10, %11, %12, %13};\n"
75	      : "=f"(d0), "=f"(d1), "=f"(d2), "=f"(d3)
76	      :  "r"(a0),  "r"(a1),  "r"(a2),  "r"(a3),
77	         "r"(b0),  "r"(b1),
78	         "f"(c0),  "f"(c1),  "f"(c2),  "f"(c3));
79	#else
80	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM120_16x8x32_TN without CUTE_ARCH_F8F6F4_MMA_ENABLED");
81	#endif
82	  }
83	};
84	
85	////////////////////////////////////////////////////////////////////////////////////////////////////
86	
87	// MMA 16x8x32 TN E2M1 x E3M2
88	template <>
89	struct SM120_16x8x32_TN<float_e2m1_t, float_e3m2_t, float>
90	{
91	  using DRegisters = float[4];
92	  using ARegisters = uint32_t[4];
93	  using BRegisters = uint32_t[2];
94	  using CRegisters = float[4];
95	
96	  CUTE_HOST_DEVICE static void
97	  fma(float         & d0, float         & d1, float         & d2, float         & d3,
98	      uint32_t const& a0, uint32_t const& a1, uint32_t const& a2, uint32_t const& a3,
99	      uint32_t const& b0, uint32_t const& b1,
100	      float const   & c0, float const   & c1, float const   & c2, float const   & c3)
101	  {
102	#if defined(CUTE_ARCH_F8F6F4_MMA_ENABLED)
103	    asm volatile(
104	      "mma.sync.aligned.kind::f8f6f4.m16n8k32.row.col.f32.e2m1.e3m2.f32 "
105	      "{%0,  %1,  %2,  %3},"
106	      "{%4,  %5,  %6,  %7},"
107	      "{%8,  %9},"
108	      "{%10, %11, %12, %13};\n"
109	      : "=f"(d0), "=f"(d1), "=f"(d2), "=f"(d3)
110	      :  "r"(a0),  "r"(a1),  "r"(a2),  "r"(a3),
111	         "r"(b0),  "r"(b1),
112	         "f"(c0),  "f"(c1),  "f"(c2),  "f"(c3));
113	#else
114	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM120_16x8x32_TN without CUTE_ARCH_F8F6F4_MMA_ENABLED");
115	#endif
116	  }
117	};
118	
119	////////////////////////////////////////////////////////////////////////////////////////////////////
120	
121	// MMA 16x8x32 TN E2M1 x E2M3
122	template <>
123	struct SM120_16x8x32_TN<float_e2m1_t, float_e2m3_t, float>
124	{
125	  using DRegisters = float[4];
126	  using ARegisters = uint32_t[4];
127	  using BRegisters = uint32_t[2];
128	  using CRegisters = float[4];
129	
130	  CUTE_HOST_DEVICE static void
131	  fma(float         & d0, float         & d1, float         & d2, float         & d3,
132	      uint32_t const& a0, uint32_t const& a1, uint32_t const& a2, uint32_t const& a3,
133	      uint32_t const& b0, uint32_t const& b1,
134	      float const   & c0, float const   & c1, float const   & c2, float const   & c3)
135	  {
136	#if defined(CUTE_ARCH_F8F6F4_MMA_ENABLED)
137	    asm volatile(
138	      "mma.sync.aligned.kind::f8f6f4.m16n8k32.row.col.f32.e2m1.e2m3.f32 "
139	      "{%0,  %1,  %2,  %3},"
140	      "{%4,  %5,  %6,  %7},"
141	      "{%8,  %9},"
142	      "{%10, %11, %12, %13};\n"
143	      : "=f"(d0), "=f"(d1), "=f"(d2), "=f"(d3)
144	      :  "r"(a0),  "r"(a1),  "r"(a2),  "r"(a3),
145	         "r"(b0),  "r"(b1),
146	         "f"(c0),  "f"(c1),  "f"(c2),  "f"(c3));
147	#else
148	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM120_16x8x32_TN without CUTE_ARCH_F8F6F4_MMA_ENABLED");
149	#endif
150	  }
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM120_64x64x16\\|SM120_.*_F32F16F16F32\\|SM120_.*wgmma\\|wgmma_mma_async\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp | head -30",
  "description": "Find SM120 MMA atom names"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16_F32F16F16F32\\|SM90_.*wgmma\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma.hpp | head -20",
  "description": "Find SM90 wgmma MMA atom names"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16\\|SM90_.*_F32F16F16F32\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm90_gmma.hpp | head -20",
  "description": "Find SM90 wgmma MMA atom names for FP16"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"wgmma_mma_async\\|SM90_.*F16.*F32\\|SM120_.*F16.*F32\\|UMMA\\|umma\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp | head -20",
  "description": "Search SM120 MMA for FP16/wgmma"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp",
  "description": "Count lines in SM120 MMA file"
}
```

> TOOL

tool_result Bash
```
3278 /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp
```

> TOOL

tool_use Bash
```json
{
  "command": "grep \"^struct SM120_\\|^struct SM90_\\|wgmma\\|WGMMA\\|UMMA\\|umma\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm120.hpp | head -40",
  "description": "List SM120 MMA struct names and wgmma/UMMA references"
}
```

> TOOL

tool_result Bash
```
struct SM120_16x8x32_TN
struct SM120_16x8x32_TN<float_e2m1_t, float_e2m1_t, float>
struct SM120_16x8x32_TN<float_e2m1_t, float_e3m2_t, float>
struct SM120_16x8x32_TN<float_e2m1_t, float_e2m3_t, float>
struct SM120_16x8x32_TN<float_e2m1_t, float_e4m3_t, float>
struct SM120_16x8x32_TN<float_e2m1_t, float_e5m2_t, float>
struct SM120_16x8x32_TN<float_e3m2_t, float_e2m1_t, float>
struct SM120_16x8x32_TN<float_e3m2_t, float_e3m2_t, float>
struct SM120_16x8x32_TN<float_e3m2_t, float_e2m3_t, float>
struct SM120_16x8x32_TN<float_e3m2_t, float_e4m3_t, float>
struct SM120_16x8x32_TN<float_e3m2_t, float_e5m2_t, float>
struct SM120_16x8x32_TN<float_e2m3_t, float_e2m1_t, float>
struct SM120_16x8x32_TN<float_e2m3_t, float_e3m2_t, float>
struct SM120_16x8x32_TN<float_e2m3_t, float_e2m3_t, float>
struct SM120_16x8x32_TN<float_e2m3_t, float_e4m3_t, float>
struct SM120_16x8x32_TN<float_e2m3_t, float_e5m2_t, float>
struct SM120_16x8x32_TN<float_e4m3_t, float_e2m1_t, float>
struct SM120_16x8x32_TN<float_e4m3_t, float_e3m2_t, float>
struct SM120_16x8x32_TN<float_e4m3_t, float_e2m3_t, float>
struct SM120_16x8x32_TN<float_e4m3_t, float_e4m3_t, float>
struct SM120_16x8x32_TN<float_e4m3_t, float_e5m2_t, float>
struct SM120_16x8x32_TN<float_e5m2_t, float_e2m1_t, float>
struct SM120_16x8x32_TN<float_e5m2_t, float_e3m2_t, float>
struct SM120_16x8x32_TN<float_e5m2_t, float_e2m3_t, float>
struct SM120_16x8x32_TN<float_e5m2_t, float_e4m3_t, float>
struct SM120_16x8x32_TN<float_e5m2_t, float_e5m2_t, float>
struct SM120_16x8x32_TN<float_e2m1_t, float_e2m1_t, half_t>
struct SM120_16x8x32_TN<float_e2m1_t, float_e3m2_t, half_t>
struct SM120_16x8x32_TN<float_e2m1_t, float_e2m3_t, half_t>
struct SM120_16x8x32_TN<float_e2m1_t, float_e4m3_t, half_t>
struct SM120_16x8x32_TN<float_e2m1_t, float_e5m2_t, half_t>
struct SM120_16x8x32_TN<float_e3m2_t, float_e2m1_t, half_t>
struct SM120_16x8x32_TN<float_e3m2_t, float_e3m2_t, half_t>
struct SM120_16x8x32_TN<float_e3m2_t, float_e2m3_t, half_t>
struct SM120_16x8x32_TN<float_e3m2_t, float_e4m3_t, half_t>
struct SM120_16x8x32_TN<float_e3m2_t, float_e5m2_t, half_t>
struct SM120_16x8x32_TN<float_e2m3_t, float_e2m1_t, half_t>
struct SM120_16x8x32_TN<float_e2m3_t, float_e3m2_t, half_t>
struct SM120_16x8x32_TN<float_e2m3_t, float_e2m3_t, half_t>
struct SM120_16x8x32_TN<float_e2m3_t, float_e4m3_t, half_t>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep \"^struct SM100_\\|^struct SM120_\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -40",
  "description": "List SM100 UMMA struct names"
}
```

> TOOL

tool_result Bash
```
struct SM100_MMA_TF32_SS
struct SM100_MMA_F16BF16_SS
struct SM100_MMA_TF32_TS
struct SM100_MMA_F16BF16_TS
struct SM100_MMA_TF32_TS_INTERLEAVED_CF32CTF32CTF32CF32_TN
struct SM100_MMA_TF32_SS_SCALED
struct SM100_MMA_F16BF16_SS_SCALED
struct SM100_MMA_TF32_TS_SCALED
struct SM100_MMA_F16BF16_TS_SCALED
struct SM100_MMA_TF32_SS_SPARSE
struct SM100_MMA_F16BF16_SS_SPARSE
struct SM100_MMA_TF32_2x1SM_SS
struct SM100_MMA_F16BF16_2x1SM_SS
struct SM100_MMA_TF32_2x1SM_TS
struct SM100_MMA_F16BF16_2x1SM_TS
struct SM100_MMA_TF32_2x1SM_TS_INTERLEAVED_CF32CTF32CTF32CF32_TN
struct SM100_MMA_TF32_2x1SM_SS_SCALED
struct SM100_MMA_F16BF16_2x1SM_SS_SCALED
struct SM100_MMA_TF32_2x1SM_TS_SCALED
struct SM100_MMA_F16BF16_2x1SM_TS_SCALED
struct SM100_MMA_TF32_2x1SM_SS_SPARSE
struct SM100_MMA_F16BF16_2x1SM_SS_SPARSE
struct SM100_MMA_S8_SS
struct SM100_MMA_S8_TS
struct SM100_MMA_S8_SS_SPARSE
struct SM100_MMA_S8_2x1SM_SS
struct SM100_MMA_S8_2x1SM_TS
struct SM100_MMA_S8_2x1SM_SS_SPARSE
struct SM100_MMA_F8F6F4_SS
struct SM100_MMA_MXF8F6F4_SS
struct SM100_MMA_F8F6F4_TS
struct SM100_MMA_F8F6F4_2x1SM_TS
struct SM100_MMA_F8F6F4_SS_SPARSE
struct SM100_MMA_MXF8F6F4_SS_SPARSE
struct SM100_MMA_F8F6F4_2x1SM_SS
struct SM100_MMA_MXF8F6F4_2x1SM_SS_SPARSE
struct SM100_MMA_MXF8F6F4_2x1SM_SS
struct SM100_MMA_F8F6F4_2x1SM_SS_SPARSE
struct SM100_MMA_MXF4_SS
struct SM100_MMA_MXF4NVF4_SS_SPARSE
```

> AGENT

这非常具有启发性。让我再检查几项关键内容。

> TOOL

tool_use Bash
```json
{
  "command": "grep \"SM100_MMA_F16BF16_SS\\b\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -10",
  "description": "Find SM100 F16/BF16 UMMA atom definition"
}
```

> TOOL

tool_result Bash
```
struct SM100_MMA_F16BF16_SS
    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_SS without CUTE_ARCH_MMA_SM100A_ENABLED");
    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_SS without CUTE_ARCH_TCGEN05_F16BF16_MMA_SCALED_ENABLED");
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -A5 \"struct SM100_MMA_F16BF16_SS<\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -30",
  "description": "Find SM100 UMMA F16/BF16 SS definition"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom -name \"*.hpp\" 2>/dev/null | head -20",
  "description": "List CuTe atom files"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_atom.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm100.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm100_im2col.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm100_tma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm50.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm75.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm80.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_im2col.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma_swizzle.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_atom.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm100.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm120.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm120_sparse.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm61.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm70.hpp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm75.hpp
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM120_TMA\\|SM100_TMA\\|TMA_LOAD\\|tma_load\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_atom.hpp | head -20",
  "description": "Find TMA copy atom names"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep \"SM90_TMA_LOAD\\|SM100_TMA\\|SM120_TMA\\|SM90_TMA_STORE\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_atom.hpp | head -20",
  "description": "Find TMA copy atom definitions"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_TMA\\|SM100_TMA\\|SM120_TMA\\|TMA_LOAD\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp | head -10",
  "description": "Find TMA trait definitions"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:// Utility for unpacking TMA_LOAD arguments into a CopyOp
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:struct TMA_LOAD_Unpack
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:    static_assert(is_smem<TD>::value, "SM90_TMA_LOAD requires the destination be shared memory.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:///////////////////////////// TMA_LOAD ///////////////////////////////////////
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:struct SM90_TMA_LOAD_OP : SM90_TMA_LOAD {};
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:// The non-executable SM90_TMA_LOAD with tma_desc and no tma_mbar
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:struct Copy_Traits<SM90_TMA_LOAD, NumBitsPerTMA, AuxParams_>
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:  // SM90_TMA_LOAD arguments
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:  // Construct an executable SM90_TMA_LOAD with tma_mbar
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm90_tma.hpp:  Copy_Traits<SM90_TMA_LOAD_OP, NumBitsPerTMA>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep \"SM100_TMA\\|SM120_TMA\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/copy_traits_sm100_tma.hpp | head -10",
  "description": "Find SM100/SM120 TMA copy trait definitions"
}
```

> TOOL

tool_result Bash
```
struct SM100_TMA_2SM_LOAD_OP : SM100_TMA_2SM_LOAD {};
// The non-executable SM100_TMA_2SM_LOAD with tma_desc and no tma_mbar
struct Copy_Traits<SM100_TMA_2SM_LOAD, NumBitsPerTMA, AuxParams_>
  // SM100_TMA_2SM_LOAD arguments
  // Construct an executable SM100_TMA_2SM_LOAD with tma_mbar
  Copy_Traits<SM100_TMA_2SM_LOAD_OP, NumBitsPerTMA>
  // Construct an executable SM100_TMA_2SM_LOAD with tma_mbar (temp. overloaded for grouped gemm/ptr array gemm)
  Copy_Traits<SM100_TMA_2SM_LOAD_OP, NumBitsPerTMA>
  // Don't try to execute a copy with SM100_TMA_2SM_LOAD before calling .with()
// The executable SM100_TMA_2SM_LOAD with tma_desc and tma_mbar
```

> AGENT

现在让我检查 Flash Attention 3 (FA3) 源码结构，并查看 FlashInfer 如何处理 SM120。

> TOOL

tool_use Bash
```json
{
  "command": "find /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer -name \"*.cu\" -path \"*attention*\" 2>/dev/null | head -10",
  "description": "Find FlashInfer attention kernels"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/batch_attention.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/batch_attention_jit_binding.cu
```

> TOOL

tool_use Bash
```json
{
  "command": "pip show flashinfer 2>/dev/null | head -10",
  "description": "Check FlashInfer version"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"sm_120\\|sm120\\|SM120\\|blackwell\\|Blackwell\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/ --include=\"*.py\" -l 2>/dev/null | head -5",
  "description": "Find FlashInfer SM120 support"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/compilation_context.py
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/aot.py
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/gdn_prefill.py
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/fp4_quantization.py
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/gdn_decode.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"sm120\\|SM120\\|sm_120\\|blackwell\\|120\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/compilation_context.py | head -10",
  "description": "Check FlashInfer SM120 support in compilation"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/compilation_context.py:        SM 12.x -> 'f' suffix with minor version preserved (e.g. compute_120f for SM120, compute_121a for SM121).
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/compilation_context.py:        Each SM 12.x variant gets its own cubin to avoid running SM120 code on SM121 (DGX Spark) which
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"wgmma\\|WGMMA\\|SM90_64x64\\|TMA_LOAD\\|cp_async_bulk\" /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/ --include=\"*.h\" --include=\"*.cu\" -l 2>/dev/null",
  "description": "Check if current codebase has any wgmma/TMA references"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> AGENT

现在，我将查看 FA3 源代码的可用性，并检查现有代码库中的 `generate_kernels.py` 和 `utils.h`。

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"generate_kernels.py\" 2>/dev/null | head -3",
  "description": "Find generate_kernels.py"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/generate_kernels.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src -name \"utils.h\" -o -name \"softmax.h\" -o -name \"mask.h\" -o -name \"dropout.h\" -o -name \"rotary.h\" -o -name \"static_switch.h\" -o -name \"hardware_info.h\" | sort",
  "description": "List utility headers"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/dropout.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/hardware_info.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/mask.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/rotary.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/softmax.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/static_switch.h
/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/utils.h
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/utils.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2023, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include <assert.h>
8	#include <stdint.h>
9	#include <stdlib.h>
10	
11	#include <cuda_fp16.h>
12	
13	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
14	#include <cuda_bf16.h>
15	#endif
16	
17	#include <cute/tensor.hpp>
18	
19	#include <cutlass/array.h>
20	#include <cutlass/cutlass.h>
21	#include <cutlass/numeric_conversion.h>
22	#include <cutlass/numeric_types.h>
23	
24	////////////////////////////////////////////////////////////////////////////////////////////////////
25	
26	namespace flash {
27	
28	////////////////////////////////////////////////////////////////////////////////////////////////////
29	
30	template<typename T>
31	__forceinline__ __device__ uint32_t relu2(const uint32_t x);
32	
33	template<>
34	__forceinline__ __device__ uint32_t relu2<cutlass::half_t>(const uint32_t x) {
35	    uint32_t res;
36	    const uint32_t zero = 0u;
37	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
38	    asm volatile("max.f16x2 %0, %1, %2;\n" : "=r"(res) : "r"(x), "r"(zero));
39	#else
40	    asm volatile( \
41	        "{\n" \
42	        "\t .reg .f16x2 sela;\n" \
43	        "\t set.gtu.u32.f16x2 sela, %1, %2;\n" \
44	        "\t and.b32 %0, sela, %1;\n" 
45	        "}\n" : "=r"(res) : "r"(x), "r"(zero));
46	#endif
47	    return res;
48	}
49	
50	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
51	template<>
52	__forceinline__ __device__ uint32_t relu2<cutlass::bfloat16_t>(const uint32_t x) {
53	    uint32_t res;
54	    const uint32_t zero = 0u;
55	    asm volatile("max.bf16x2 %0, %1, %2;\n" : "=r"(res) : "r"(x), "r"(zero));
56	    return res;
57	}
58	#endif
59	
60	////////////////////////////////////////////////////////////////////////////////////////////////////
61	
62	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
63	
64	template<typename T>
65	__forceinline__ __device__ uint32_t convert_relu2(const float2 x);
66	
67	template<>
68	__forceinline__ __device__ uint32_t convert_relu2<cutlass::half_t>(const float2 x) {
69	    uint32_t res;
70	    const uint32_t a = reinterpret_cast<const uint32_t&>(x.x);
71	    const uint32_t b = reinterpret_cast<const uint32_t&>(x.y);
72	    asm volatile("cvt.rn.relu.f16x2.f32 %0, %1, %2;\n" : "=r"(res) : "r"(b), "r"(a));
73	    return res;
74	}
75	
76	template<>
77	__forceinline__ __device__ uint32_t convert_relu2<cutlass::bfloat16_t>(const float2 x) {
78	    uint32_t res;
79	    const uint32_t a = reinterpret_cast<const uint32_t&>(x.x);
80	    const uint32_t b = reinterpret_cast<const uint32_t&>(x.y);
81	    asm volatile("cvt.rn.relu.bf16x2.f32 %0, %1, %2;\n" : "=r"(res) : "r"(b), "r"(a));
82	    return res;
83	}
84	
85	#endif
86	
87	////////////////////////////////////////////////////////////////////////////////////////////////////
88	
89	template<typename T>
90	struct MaxOp {
91	__device__ __forceinline__ T operator()(T const & x, T const & y) { return x > y ? x : y; }
92	};
93	
94	template <>
95	struct MaxOp<float> {
96	// This is slightly faster
97	__device__ __forceinline__ float operator()(float const &x, float const &y) { return max(x, y); }
98	};
99	
100	////////////////////////////////////////////////////////////////////////////////////////////////////
101	
102	template<typename T>
103	struct SumOp {
104	__device__ __forceinline__ T operator()(T const & x, T const & y) { return x + y; }
105	};
106	
107	////////////////////////////////////////////////////////////////////////////////////////////////////
108	
109	template<int THREADS>
110	struct Allreduce {
111	    static_assert(THREADS == 32 || THREADS == 16 || THREADS == 8 || THREADS == 4);
112	    template<typename T, typename Operator>
113	    static __device__ __forceinline__ T run(T x, Operator &op) {
114	        constexpr int OFFSET = THREADS / 2;
115	        x = op(x, __shfl_xor_sync(uint32_t(-1), x, OFFSET));
116	        return Allreduce<OFFSET>::run(x, op);
117	    }
118	};
119	
120	////////////////////////////////////////////////////////////////////////////////////////////////////
121	
122	template<>
123	struct Allreduce<2> {
124	template<typename T, typename Operator> 
125	static __device__ __forceinline__ T run(T x, Operator &op) {
126	    x = op(x, __shfl_xor_sync(uint32_t(-1), x, 1));
127	    return x;
128	}
129	};
130	
131	////////////////////////////////////////////////////////////////////////////////////////////////////
132	
133	template<bool A_in_regs=false, bool B_in_regs=false, typename Tensor0, typename Tensor1,
134	         typename Tensor2, typename Tensor3, typename Tensor4,
135	         typename TiledMma, typename TiledCopyA, typename TiledCopyB,
136	         typename ThrCopyA, typename ThrCopyB>
137	__forceinline__ __device__ void gemm(Tensor0 &acc, Tensor1 &tCrA, Tensor2 &tCrB, Tensor3 const& tCsA,
138	                            Tensor4 const& tCsB, TiledMma tiled_mma,
139	                            TiledCopyA smem_tiled_copy_A, TiledCopyB smem_tiled_copy_B,
140	                            ThrCopyA smem_thr_copy_A, ThrCopyB smem_thr_copy_B) {
141	    CUTE_STATIC_ASSERT_V(size<1>(tCrA) == size<1>(acc));                     // MMA_M
142	    CUTE_STATIC_ASSERT_V(size<1>(tCrB) == size<2>(acc));                     // MMA_N
143	    CUTE_STATIC_ASSERT_V(size<2>(tCrA) == size<2>(tCrB));                     // MMA_K
144	    Tensor tCrA_copy_view = smem_thr_copy_A.retile_D(tCrA);
145	    CUTE_STATIC_ASSERT_V(size<1>(tCsA) == size<1>(tCrA_copy_view));            // M
146	    Tensor tCrB_copy_view = smem_thr_copy_B.retile_D(tCrB);
147	    CUTE_STATIC_ASSERT_V(size<1>(tCsB) == size<1>(tCrB_copy_view));            // N
148	    if (!A_in_regs) { cute::copy(smem_tiled_copy_A, tCsA(_, _, _0{}), tCrA_copy_view(_, _, _0{})); }
149	    if (!B_in_regs) { cute::copy(smem_tiled_copy_B, tCsB(_, _, _0{}), tCrB_copy_view(_, _, _0{})); }
150	    #pragma unroll
151	    for (int i = 0; i < size<2>(tCrA); ++i) {
152	        if (i < size<2>(tCrA) - 1) {
153	            if (!A_in_regs) { cute::copy(smem_tiled_copy_A, tCsA(_, _, i + 1), tCrA_copy_view(_, _, i + 1)); }
154	            if (!B_in_regs) { cute::copy(smem_tiled_copy_B, tCsB(_, _, i + 1), tCrB_copy_view(_, _, i + 1)); }
155	        }
156	        cute::gemm(tiled_mma, tCrA(_, _, i), tCrB(_, _, i), acc);
157	    }
158	}
159	
160	////////////////////////////////////////////////////////////////////////////////////////////////////
161	
162	template<typename Tensor0, typename Tensor1, typename Tensor2, typename Tensor3,
163	         typename TiledMma, typename TiledCopy, typename ThrCopy>
164	__forceinline__ __device__ void gemm_rs(Tensor0 &acc, Tensor1 &tCrA, Tensor2 &tCrB, Tensor3 const& tCsB,
165	                               TiledMma tiled_mma, TiledCopy smem_tiled_copy_B,
166	                               ThrCopy smem_thr_copy_B) {
167	    CUTE_STATIC_ASSERT_V(size<1>(tCrA) == size<1>(acc));                     // MMA_M
168	    CUTE_STATIC_ASSERT_V(size<1>(tCrB) == size<2>(acc));                     // MMA_N
169	    CUTE_STATIC_ASSERT_V(size<2>(tCrA) == size<2>(tCrB));                     // MMA_K
170	    Tensor tCrB_copy_view = smem_thr_copy_B.retile_D(tCrB);
171	    CUTE_STATIC_ASSERT_V(size<1>(tCsB) == size<1>(tCrB_copy_view));            // N
172	    cute::copy(smem_tiled_copy_B, tCsB(_, _, _0{}), tCrB_copy_view(_, _, _0{}));
173	    #pragma unroll
174	    for (int i = 0; i < size<2>(tCrA); ++i) {
175	        if (i < size<2>(tCrA) - 1) {
176	            cute::copy(smem_tiled_copy_B, tCsB(_, _, i + 1), tCrB_copy_view(_, _, i + 1));
177	        }
178	        cute::gemm(tiled_mma, tCrA(_, _, i), tCrB(_, _, i), acc);
179	    }
180	}
181	
182	////////////////////////////////////////////////////////////////////////////////////////////////////
183	
184	// Convert acc_layout from (MMA=4, MMA_M, MMA_N) to (nrow=(2, MMA_M), ncol=(2, MMA_N))
185	template<typename Layout>
186	__forceinline__ __device__ auto convert_layout_acc_rowcol(Layout acc_layout) {
187	    static_assert(decltype(size<0>(acc_layout))::value == 4);
188	    static_assert(decltype(rank(acc_layout))::value == 3);
189	    auto l = logical_divide(acc_layout, Shape<_2>{});  // ((2, 2), MMA_M, MMA_N)
190	    return make_layout(make_layout(get<0, 1>(l), get<1>(l)), make_layout(get<0, 0>(l), get<2>(l)));
191	};
192	
193	////////////////////////////////////////////////////////////////////////////////////////////////////
194	
195	// Convert acc_layout from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
196	// if using m16n8k16, or to (4, MMA_M, MMA_N) if using m16n8k8.
197	template<typename MMA_traits, typename Layout>
198	__forceinline__ __device__ auto convert_layout_acc_Aregs(Layout acc_layout) {
199	    using X = Underscore;
200	    static_assert(decltype(size<0>(acc_layout))::value == 4);
201	    static_assert(decltype(rank(acc_layout))::value == 3);
202	    constexpr int mma_shape_K = get<2>(typename MMA_traits::Shape_MNK{});
203	    static_assert(mma_shape_K == 8 || mma_shape_K == 16);
204	    if constexpr (mma_shape_K == 8) {
205	        return acc_layout;
206	    } else {
207	        auto l = logical_divide(acc_layout, Shape<X, X, _2>{});  // (4, MMA_M, (2, MMA_N / 2)))
208	        return make_layout(make_layout(get<0>(l), get<2, 0>(l)), get<1>(l), get<2, 1>(l));
209	    }
210	};
211	
212	////////////////////////////////////////////////////////////////////////////////////////////////////
213	
214	// Convert acc_layout from (MMA=4, MMA_M, MMA_N) to ((4, 2), MMA_M, MMA_N / 2)
215	template<typename Layout>
216	__forceinline__ __device__ auto convert_layout_acc_dropout(Layout acc_layout) {
217	    using X = Underscore;
218	    static_assert(decltype(size<0>(acc_layout))::value == 4);
219	    static_assert(decltype(rank(acc_layout))::value == 3);
220	    auto l = logical_divide(acc_layout, Shape<X, X, _2>{});  // (4, MMA_M, (2, MMA_N / 2)))
221	    return make_layout(make_layout(get<0>(l), get<2, 0>(l)), get<1>(l), get<2, 1>(l));
222	};
223	
224	////////////////////////////////////////////////////////////////////////////////////////////////////
225	
226	template <typename To_type, typename Engine, typename Layout>
227	__forceinline__ __device__ auto convert_type(Tensor<Engine, Layout> const &tensor) {
228	    using From_type = typename Engine::value_type;
229	    constexpr int numel = decltype(size(tensor))::value;
230	    cutlass::NumericArrayConverter<To_type, From_type, numel> convert_op;
231	    // HACK: this requires tensor to be "contiguous"
232	    auto frag = convert_op(*reinterpret_cast<const cutlass::Array<From_type, numel> *>(tensor.data()));
233	    return make_tensor(make_rmem_ptr<To_type>(&frag), tensor.layout());
234	}
235	
236	////////////////////////////////////////////////////////////////////////////////////////////////////
237	
238	template <typename Engine, typename Layout>
239	__forceinline__ __device__ void relu_(Tensor<Engine, Layout> &tensor) {
240	    constexpr int numel = decltype(size(tensor))::value;
241	    static_assert(numel % 2 == 0);
242	    using value_t = typename Engine::value_type;
243	    // HACK: this requires tensor to be "contiguous"
244	    Tensor tensor_uint32 = recast<uint32_t>(tensor);
245	    #pragma unroll
246	    for (int i = 0; i < size(tensor_uint32); ++i) {
247	        tensor_uint32(i) = relu2<value_t>(tensor_uint32(i));
248	    }
249	}
250	
251	////////////////////////////////////////////////////////////////////////////////////////////////////
252	
253	// On SM80 and above, we can fuse fp32 -> fp16/bf16 conversion and relu into 1 instruction
254	template <typename To_type, typename Engine, typename Layout>
255	__forceinline__ __device__ auto convert_type_relu(Tensor<Engine, Layout> const &tensor) {
256	    using From_type = typename Engine::value_type;
257	    static_assert(std::is_same_v<To_type, cutlass::half_t> || std::is_same_v<To_type, cutlass::bfloat16_t>);
258	    static_assert(std::is_same_v<float, From_type>);
259	    constexpr int numel = decltype(size(tensor))::value;
260	    static_assert(numel % 2 == 0);
261	#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
262	    // HACK: this requires tensor to be "contiguous"
263	    Tensor tensor_float2 = recast<float2>(tensor);
264	    Tensor out_uint32 = make_tensor<uint32_t>(tensor_float2.layout());
265	    #pragma unroll
266	    for (int i = 0; i < size(out_uint32); ++i) {
267	        out_uint32(i) = convert_relu2<To_type>(tensor_float2(i));
268	    }
269	    Tensor out = make_tensor(make_rmem_ptr<To_type>(out_uint32.data()), tensor.layout());
270	#else
271	    Tensor out = flash::convert_type<To_type>(tensor);
272	    flash::relu_(out);
273	#endif
274	    return out;
275	}
276	
277	////////////////////////////////////////////////////////////////////////////////////////////////////
278	
279	// Blocks until all but N previous cp.async.commit_group operations have committed.
280	// This differs from cute::cp_async_wait in that when N = 0 we don't call cp.async.wait_all
281	// (which is equivalent to commit_group then wait_group 0).
282	// Instead we just call cp.async.wait_group 0, which is slightly faster.
283	// https://github.com/NVIDIA/cutlass/blob/master/include/cute/arch/copy_sm80.hpp#L113
284	template <int N>
285	CUTE_HOST_DEVICE
286	void cp_async_wait() {
287	#if defined(CUTE_ARCH_CP_ASYNC_SM80_ENABLED)
288	    asm volatile("cp.async.wait_group %0;\n" :: "n"(N));
289	#endif
290	}
291	
292	////////////////////////////////////////////////////////////////////////////////////////////////////
293	
294	template <bool Is_even_MN=true, bool Is_even_K=true, bool Clear_OOB_MN=false, bool Clear_OOB_K=true,
295	          typename TiledCopy, typename Engine0, typename Layout0, typename Engine1, typename Layout1,
296	          typename Engine2, typename Layout2, typename Engine3, typename Layout3>
297	__forceinline__ __device__ void copy(TiledCopy tiled_copy, Tensor<Engine0, Layout0> const &S,
298	                            Tensor<Engine1, Layout1> &D, Tensor<Engine2, Layout2> const &identity_MN,
299	                            Tensor<Engine3, Layout3> const &predicate_K, const int max_MN=0) {
300	    CUTE_STATIC_ASSERT_V(rank(S) == Int<3>{});
301	    CUTE_STATIC_ASSERT_V(rank(D) == Int<3>{});
302	    CUTE_STATIC_ASSERT_V(size<0>(S) == size<0>(D));                     // MMA
303	    CUTE_STATIC_ASSERT_V(size<1>(S) == size<1>(D));                     // MMA_M
304	    CUTE_STATIC_ASSERT_V(size<2>(S) == size<2>(D));                     // MMA_K
305	    // There's no case where !Clear_OOB_K && Clear_OOB_MN
306	    static_assert(!(Clear_OOB_MN && !Clear_OOB_K));
307	    #pragma unroll
308	    for (int m = 0; m < size<1>(S); ++m) {
309	        if (Is_even_MN || get<0>(identity_MN(0, m, 0)) < max_MN) {
310	            #pragma unroll
311	            for (int k = 0; k < size<2>(S); ++k) {
312	                if (Is_even_K || predicate_K(k)) {
313	                    cute::copy(tiled_copy, S(_, m, k), D(_, m, k));
314	                } else if (Clear_OOB_K) {
315	                    cute::clear(D(_, m, k));
316	                }
317	            }
318	        } else if (Clear_OOB_MN) {
319	            cute::clear(D(_, m, _));
320	        }
321	    }
322	    // TD [2023-04-13]: Strange that the code below can cause race condition.
323	    // I think it's because the copies are under an if statement.
324	    // if (Is_even_K) {
325	    //     #pragma unroll
326	    //     for (int m = 0; m < size<1>(S); ++m) {
327	    //         if (Is_even_MN || get<0>(identity_MN(0, m, 0)) < max_MN) {
328	    //             copy(tiled_copy, S(_, m, _), D(_, m, _));
329	    //         } else if (Clear_OOB_MN) {
330	    //             clear(D(_, m, _));
331	    //         }
332	    //     }
333	    // } else {  // It's slightly faster in this case if iterate over K first
334	    //     #pragma unroll
335	    //     for (int k = 0; k < size<2>(S); ++k) {
336	    //         if (predicate_K(k)) {
337	    //             #pragma unroll
338	    //             for (int m = 0; m < size<1>(S); ++m) {
339	    //                 if (Is_even_MN || get<0>(identity_MN(0, m, 0)) < max_MN) {
340	    //                     copy(tiled_copy, S(_, m, k), D(_, m, k));
341	    //                 } else if (Clear_OOB_MN) {
342	    //                     clear(D(_, m, k));
343	    //                 }
344	    //             }
345	    //         } else if (Clear_OOB_K) {  // There's no case where !Clear_OOB_K && Clear_OOB_MN
346	    //             if (Clear_OOB_MN || Is_even_MN) {
347	    //                 clear(D(_, _, k));
348	    //             } else {
349	    //                 #pragma unroll
350	    //                 for (int m = 0; m < size<1>(S); ++m) {
351	    //                     if (!(Is_even_MN || get<0>(identity_MN(0, m, 0)) < max_MN)) {
352	    //                         clear(D(_, m, k));
353	    //                     }
354	    //                 }
355	    //             }
356	    //         }
357	    //     }
358	    // }
359	}
360	
361	////////////////////////////////////////////////////////////////////////////////////////////////////
362	
363	template <bool Is_even_K=true,
364	          typename Engine0, typename Layout0, typename Engine1, typename Layout1,
365	          typename Engine2, typename Layout2, typename Engine3, typename Layout3>
366	__forceinline__ __device__ void copy_w_min_idx(Tensor<Engine0, Layout0> const &S,
367	                                      Tensor<Engine1, Layout1> &D, Tensor<Engine2, Layout2> const &identity_MN,
368	                                      Tensor<Engine3, Layout3> const &predicate_K,
369	                                      const int max_MN=0, const int min_MN=0) {
370	    CUTE_STATIC_ASSERT_V(rank(S) == Int<3>{});
371	    CUTE_STATIC_ASSERT_V(rank(D) == Int<3>{});
372	    CUTE_STATIC_ASSERT_V(size<0>(S) == size<0>(D));                     // MMA
373	    CUTE_STATIC_ASSERT_V(size<1>(S) == size<1>(D));                     // MMA_M
374	    CUTE_STATIC_ASSERT_V(size<2>(S) == size<2>(D));                     // MMA_K
375	    // if (threadIdx.x == 0 && blockIdx.z == 0) { printf("blockIdx.y = %d, max_MN = %d, min_MN = %d\n", blockIdx.y, max_MN, min_MN); }
376	    #pragma unroll
377	    for (int m = 0; m < size<1>(S); ++m) {
378	        // if (threadIdx.x == 0 && blockIdx.z == 0) { printf("blockIdx.y = %d, m = %d\n", blockIdx.y, get<0>(identity_MN(0, m, 0))); }
379	        if (get<0>(identity_MN(0, m, 0)) >= min_MN && get<0>(identity_MN(0, m, 0)) < max_MN) {
380	            // if (threadIdx.x == 0 && blockIdx.z == 0) { printf("Inner loop, blockIdx.y = %d, m = %d\n", blockIdx.y, get<0>(identity_MN(0, m, 0))); }
381	            #pragma unroll
382	            for (int k = 0; k < size<2>(S); ++k) {
383	                if (Is_even_K || predicate_K(k)) {
384	                    cute::copy(S(_, m, k), D(_, m, k));
385	                }
386	            }
387	        }
388	    }
389	}
390	
391	////////////////////////////////////////////////////////////////////////////////////////////////////
392	
393	template <typename Engine, typename Layout>
394	__forceinline__ __device__ void apply_softcap(Tensor<Engine, Layout> &tensor, const float softcap){
395	    #pragma unroll
396	    for (int i = 0; i < size(tensor); ++i) {
397	        tensor(i) = cutlass::fast_tanh(tensor(i) * softcap);
398	    }
399	}
400	
401	template <typename Engine0, typename Layout0, typename Engine1, typename Layout1>
402	__forceinline__ __device__ void calculate_dtanh(Tensor<Engine0, Layout0> &src_tensor, Tensor<Engine1, Layout1> &dst_tensor, const float softcap){
403	    #pragma unroll
404	    for (int i = 0; i < size(src_tensor); ++i) {
405	        dst_tensor(i) = (1.f - (src_tensor(i) * src_tensor(i))) * softcap;
406	    }
407	}
408	
409	////////////////////////////////////////////////////////////////////////////////////////////////////
410	
411	}  // namespace flash
412
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/hardware_info.h"
}
```

> TOOL

tool_result Read
```
1	/******************************************************************************
2	 * Copyright (c) 2024, Tri Dao.
3	 ******************************************************************************/
4	
5	#pragma once
6	
7	#include <tuple>
8	
9	#if !defined(__CUDACC_RTC__)
10	#include "cuda_runtime.h"
11	#endif
12	
13	#define CHECK_CUDA(call)                                                       \
14	  do {                                                                         \
15	    cudaError_t status_ = call;                                                \
16	    if (status_ != cudaSuccess) {                                              \
17	      fprintf(stderr, "CUDA error (%s:%d): %s\n", __FILE__, __LINE__,          \
18	              cudaGetErrorString(status_));                                    \
19	      exit(1);                                                                 \
20	    }                                                                          \
21	  } while (0)
22	
23	
24	inline int get_current_device() {
25	    int device;
26	    CHECK_CUDA(cudaGetDevice(&device));
27	    return device;
28	}
29	
30	inline std::tuple<int, int> get_compute_capability(int device) {
31	    int capability_major, capability_minor;
32	    CHECK_CUDA(cudaDeviceGetAttribute(&capability_major, cudaDevAttrComputeCapabilityMajor, device));
33	    CHECK_CUDA(cudaDeviceGetAttribute(&capability_minor, cudaDevAttrComputeCapabilityMinor, device));
34	    return {capability_major, capability_minor};
35	}
36	
37	inline int get_num_sm(int device) {
38	    int multiprocessor_count;
39	    CHECK_CUDA(cudaDeviceGetAttribute(&multiprocessor_count, cudaDevAttrMultiProcessorCount, device));
40	    return multiprocessor_count;
41	}
42
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/generate_kernels.py"
}
```

> TOOL

tool_result Read
```
1	# Copied from Driss Guessous's PR in PyTorch: https://github.com/pytorch/pytorch/pull/105602
2	
3	# This file is run to generate the kernel instantiations for the flash_attn kernels
4	# They are written to several files in order to speed up compilation
5	
6	import argparse
7	import itertools
8	from dataclasses import dataclass
9	from pathlib import Path
10	from typing import List, Optional
11	
12	DTYPE_MAP = {
13	    "fp16": "cutlass::half_t",
14	    "bf16": "cutlass::bfloat16_t",
15	}
16	
17	SM = [80]  # Sm80 kernels support up to
18	HEAD_DIMENSIONS = [32, 64, 96, 128, 160, 192, 256]
19	IS_CAUSAL = ["false", "true"]
20	KERNEL_IMPL_TEMPLATE_FWD = """#include "flash_fwd_launch_template.h"
21	
22	template<>
23	void run_mha_fwd_<{DTYPE}, {HEAD_DIM}, {IS_CAUSAL}>(Flash_fwd_params &params, cudaStream_t stream) {{
24	    run_mha_fwd_hdim{HEAD_DIM}<{DTYPE}, {IS_CAUSAL}>(params, stream);
25	}}
26	"""
27	
28	KERNEL_IMPL_TEMPLATE_FWD_SPLIT = """#include "flash_fwd_launch_template.h"
29	
30	template void run_mha_fwd_splitkv_dispatch<{DTYPE}, {HEAD_DIM}, {IS_CAUSAL}>(Flash_fwd_params &params, cudaStream_t stream);
31	"""
32	
33	KERNEL_IMPL_TEMPLATE_BWD = """#include "flash_bwd_launch_template.h"
34	
35	template<>
36	void run_mha_bwd_<{DTYPE}, {HEAD_DIM}, {IS_CAUSAL}>(Flash_bwd_params &params, cudaStream_t stream) {{
37	    run_mha_bwd_hdim{HEAD_DIM}<{DTYPE}, {IS_CAUSAL}>(params, stream);
38	}}
39	"""
40	
41	
42	@dataclass
43	class Kernel:
44	    sm: int
45	    dtype: str
46	    head_dim: int
47	    is_causal: bool
48	    direction: str
49	
50	    @property
51	    def template(self) -> str:
52	        if self.direction == "fwd":
53	            return KERNEL_IMPL_TEMPLATE_FWD.format(
54	                DTYPE=DTYPE_MAP[self.dtype], HEAD_DIM=self.head_dim, IS_CAUSAL=self.is_causal
55	            )
56	        elif self.direction == "bwd":
57	            return KERNEL_IMPL_TEMPLATE_BWD.format(
58	                DTYPE=DTYPE_MAP[self.dtype], HEAD_DIM=self.head_dim, IS_CAUSAL=self.is_causal
59	            )
60	        else:
61	            return KERNEL_IMPL_TEMPLATE_FWD_SPLIT.format(
62	                DTYPE=DTYPE_MAP[self.dtype], HEAD_DIM=self.head_dim, IS_CAUSAL=self.is_causal
63	            )
64	
65	    @property
66	    def filename(self) -> str:
67	        return f"flash_{self.direction}_hdim{self.head_dim}_{self.dtype}_{'causal_' if self.is_causal == 'true' else ''}sm{self.sm}.cu"
68	
69	
70	def get_all_kernels() -> List[Kernel]:
71	    for direction in ["fwd", "fwd_split", "bwd"]:
72	        for dtype, head_dim, is_causal, sm in itertools.product(DTYPE_MAP.keys(), HEAD_DIMENSIONS, IS_CAUSAL, SM):
73	            yield Kernel(sm=sm, dtype=dtype, head_dim=head_dim, is_causal=is_causal, direction=direction)
74	
75	
76	def write_kernel(kernel: Kernel, autogen_dir: Path) -> None:
77	    prelude = """// Copyright (c) 2024, Tri Dao.
78	// Splitting the different head dimensions to different files to speed up compilation.
79	// This file is auto-generated. See "generate_kernels.py"\n
80	"""
81	    (autogen_dir / kernel.filename).write_text(prelude + kernel.template)
82	
83	
84	def main(output_dir: Optional[str]) -> None:
85	    if output_dir is None:
86	        output_dir = Path(__file__).parent
87	    else:
88	        output_dir = Path(output_dir)
89	
90	    for kernel in get_all_kernels():
91	        write_kernel(kernel, output_dir)
92	
93	
94	if __name__ == "__main__":
95	    parser = argparse.ArgumentParser(
96	        prog="generate_kernels",
97	        description="Generate the flash_attention kernels template instantiations",
98	    )
99	    # Set an optional output directory
100	    parser.add_argument(
101	        "-o",
102	        "--output_dir",
103	        required=False,
104	        help="Where to generate the kernels "
105	        " will default to the current directory ",
106	    )
107	    args = parser.parse_args()
108	    main(args.output_dir)
109
```

> AGENT

现在，我将阅读 SM100 UMMA 文件，以了解 Blackwell 对 FP16/BF16 的 MMA 指令。

> TOOL

tool_use Bash
```json
{
  "command": "grep -A20 \"struct SM100_MMA_F16BF16_SS<half_t\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -40",
  "description": "Find SM100 UMMA F16/BF16 SS definition for half_t"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep \"^struct SM100_MMA_F16BF16_SS<\\|^struct SM100_MMA_F16BF16_TS<\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -10",
  "description": "List SM100 UMMA F16/BF16 template specializations"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"SM100_MMA_F16BF16\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp | head -20",
  "description": "Find SM100_MMA_F16BF16 line numbers"
}
```

> TOOL

tool_result Bash
```
86:struct SM100_MMA_F16BF16_SS
88:  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16 M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
90:                "SM100_MMA_F16BF16 N-mode size should be a multiple of 8 between 8 and 256.");
118:    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_SS without CUTE_ARCH_MMA_SM100A_ENABLED");
171:struct SM100_MMA_F16BF16_TS
173:  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16 M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
176:                "SM100_MMA_F16BF16 N-mode size should be a multiple of 8 between 8 and 256 for M=64,\
178:  static_assert(a_major == UMMA::Major::K, "SM100_MMA_F16BF16 A from TMEM can't be transposed");
206:    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_TS without CUTE_ARCH_MMA_SM100A_ENABLED");
299:struct SM100_MMA_F16BF16_SS_SCALED
301:  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16_SS_SCALED M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
303:                "SM100_MMA_F16BF16_SS_SCALED N-mode size should be a multiple of 8 between 8 and 256.");
332:    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_SS without CUTE_ARCH_TCGEN05_F16BF16_MMA_SCALED_ENABLED");
386:struct SM100_MMA_F16BF16_TS_SCALED
388:  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16_TS_SCALED M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
391:                "SM100_MMA_F16BF16_TS_SCALED N-mode size should be a multiple of 8 between 8 and 256 for M=64,\
393:  static_assert(a_major == UMMA::Major::K, "SM100_MMA_F16BF16_TS_SCALED A from TMEM can't be transposed");
422:    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_TS_SCALED without CUTE_ARCH_TCGEN05_F16BF16_MMA_SCALED_ENABLED");
471:struct SM100_MMA_F16BF16_SS_SPARSE
473:  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16_SS_SPARSE M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
```

> TOOL

tool_use Read
```json
{
  "file_path": "/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/arch/mma_sm100_umma.hpp",
  "limit": 120,
  "offset": 70
}
```

> TOOL

tool_result Read
```
70	        "setp.ne.b32 p, %4, 0;\n\t"
71	        "tcgen05.mma.cta_group::1.kind::tf32 [%0], %1, %2, %3, {%5, %6, %7, %8}, p; \n\t"
72	        "}\n"
73	        :
74	        : "r"(tmem_c), "l"(desc_a), "l"(desc_b), "r"(uint32_t(idescE>>32)), "r"(scaleC),
75	          "r"(mask[0]), "r"(mask[1]), "r"(mask[2]), "r"(mask[3]));
76	    }
77	#else
78	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_TF32_SS without CUTE_ARCH_TCGEN05_TF32_MMA_ENABLED");
79	#endif
80	  }
81	};
82	
83	template <class a_type, class b_type, class c_type,
84	          int M, int N, UMMA::Major a_major, UMMA::Major b_major,
85	          UMMA::ScaleIn a_neg = UMMA::ScaleIn::One, UMMA::ScaleIn b_neg = UMMA::ScaleIn::One>
86	struct SM100_MMA_F16BF16_SS
87	{
88	  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16 M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
89	  static_assert((N % 8 == 0)  && (8 <= N)  && (N <= 256),
90	                "SM100_MMA_F16BF16 N-mode size should be a multiple of 8 between 8 and 256.");
91	
92	  using DRegisters = void;
93	  using ARegisters = uint64_t[1];
94	  using BRegisters = uint64_t[1];
95	  using CRegisters = uint32_t[1];
96	
97	  CUTE_HOST_DEVICE static void
98	  fma(uint64_t const& desc_a,
99	      uint64_t const& desc_b,
100	      uint32_t const& tmem_c,
101	      uint32_t const& scaleC,
102	      uint64_t const& idescE)
103	  {
104	#if defined(CUTE_ARCH_TCGEN05_F16F32_MMA_ENABLED)
105	    if (cute::elect_one_sync()) {
106	      uint32_t mask[4] = {0, 0, 0, 0};
107	      asm volatile(
108	        "{\n\t"
109	        ".reg .pred p;\n\t"
110	        "setp.ne.b32 p, %4, 0;\n\t"
111	        "tcgen05.mma.cta_group::1.kind::f16 [%0], %1, %2, %3, {%5, %6, %7, %8}, p; \n\t"
112	        "}\n"
113	        :
114	        : "r"(tmem_c), "l"(desc_a), "l"(desc_b), "r"(uint32_t(idescE>>32)), "r"(scaleC),
115	          "r"(mask[0]), "r"(mask[1]), "r"(mask[2]), "r"(mask[3]));
116	    }
117	#else
118	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_F16BF16_SS without CUTE_ARCH_MMA_SM100A_ENABLED");
119	#endif
120	  }
121	};
122	
123	template <class a_type, class b_type, class c_type,
124	          int M, int N, UMMA::Major a_major, UMMA::Major b_major,
125	          UMMA::ScaleIn a_neg = UMMA::ScaleIn::One, UMMA::ScaleIn b_neg = UMMA::ScaleIn::One,
126	          UMMA::Saturate c_sat = UMMA::Saturate::False>
127	struct SM100_MMA_TF32_TS
128	{
129	  static_assert(M == 64 || M == 128, "SM100_MMA_TF32 M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
130	  static_assert((M == 64  && (N % 8 == 0)  && (8 <= N)  && (N <= 256)) ||
131	                (M == 128 && (N % 16 == 0) && (16 <= N) && (N <= 256)),
132	                "SM100_MMA_TF32 N-mode size should be a multiple of 8 between 8 and 256 for M=64,\
133	                 or a multiple of 16 between 16 and 256 for M=128.");
134	  static_assert(a_major == UMMA::Major::K, "SM100_MMA_TF32 A from TMEM can't be transposed");
135	
136	  using DRegisters = void;
137	  using ARegisters = uint32_t[1];
138	  using BRegisters = uint64_t[1];
139	  using CRegisters = uint32_t[1];
140	
141	  CUTE_HOST_DEVICE static void
142	  fma(uint32_t const& tmem_a,
143	      uint64_t const& desc_b,
144	      uint32_t const& tmem_c,
145	      uint32_t const& scaleC,
146	      uint64_t const& idescE)
147	  {
148	#if defined(CUTE_ARCH_TCGEN05_TF32_MMA_ENABLED)
149	    uint32_t mask[4] = {0, 0, 0, 0};
150	    if (cute::elect_one_sync()) {
151	      asm volatile(
152	        "{\n\t"
153	        ".reg .pred p;\n\t"
154	        "setp.ne.b32 p, %4, 0;\n\t"
155	        "tcgen05.mma.cta_group::1.kind::tf32 [%0], [%1], %2, %3, {%5, %6, %7, %8}, p; \n\t"
156	        "}\n"
157	        :
158	        : "r"(tmem_c), "r"(tmem_a), "l"(desc_b), "r"(uint32_t(idescE>>32)), "r"(scaleC),
159	          "r"(mask[0]), "r"(mask[1]), "r"(mask[2]), "r"(mask[3]));
160	    }
161	#else
162	    CUTE_INVALID_CONTROL_PATH("Attempting to use SM100_MMA_TF32_TS without CUTE_ARCH_TCGEN05_TF32_MMA_ENABLED");
163	#endif
164	  }
165	};
166	
167	template <class a_type, class b_type, class c_type,
168	          int M, int N, UMMA::Major a_major, UMMA::Major b_major,
169	          UMMA::ScaleIn a_neg = UMMA::ScaleIn::One, UMMA::ScaleIn b_neg = UMMA::ScaleIn::One,
170	          UMMA::Saturate c_sat = UMMA::Saturate::False>
171	struct SM100_MMA_F16BF16_TS
172	{
173	  static_assert(M == 64 || M == 128, "SM100_MMA_F16BF16 M-mode size should be 64 or 128 for 1 CTA cluster MMA.");
174	  static_assert((M == 64  && (N % 8 == 0)  && (8 <= N)  && (N <= 256)) ||
175	                (M == 128 && (N % 16 == 0) && (16 <= N) && (N <= 256)),
176	                "SM100_MMA_F16BF16 N-mode size should be a multiple of 8 between 8 and 256 for M=64,\
177	                 or a multiple of 16 between 16 and 256 for M=128.");
178	  static_assert(a_major == UMMA::Major::K, "SM100_MMA_F16BF16 A from TMEM can't be transposed");
179	
180	  using DRegisters = void;
181	  using ARegisters = uint32_t[1];
182	  using BRegisters = uint64_t[1];
183	  using CRegisters = uint32_t[1];
184	
185	  CUTE_HOST_DEVICE static void
186	  fma(uint32_t const& tmem_a,
187	      uint64_t const& desc_b,
188	      uint32_t const& tmem_c,
189	      uint32_t const& scaleC,
```

> AGENT

现在我来检查 SM120 MMA traits，以理解 CuTe 如何封装 SM120 MMA atoms。

> TOOL

tool_use Bash
```json
{
  "command": "cat /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm120.hpp",
  "description": "Read SM120 MMA traits"
}
```

> TOOL

tool_result Bash
```
/***************************************************************************************************
 * Copyright (c) 2025 - 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **************************************************************************************************/

#pragma once

#include <cute/arch/mma_sm120.hpp>
#include <cute/atom/mma_traits.hpp>
#include <cute/atom/mma_traits_sm80.hpp>
#include <cute/layout.hpp>
#include <cute/numeric/numeric_types.hpp>

namespace cute
{

namespace SM120::BLOCKSCALED {

template <class MMAOp,
          class TD, class DLayout,
          class TA, class ALayout,
          class TB, class BLayout,
          class TC, class CLayout>
CUTE_HOST_DEVICE constexpr void
mma_unpack(MMA_Traits<MMAOp>   const& traits,
           Tensor<TD, DLayout>      & D,
           Tensor<TA, ALayout> const& A_zipped,
           Tensor<TB, BLayout> const& B_zipped,
           Tensor<TC, CLayout> const& C)
{
  static_assert(is_rmem<TD>::value, "Expected registers in MMA_Atom::call");
  static_assert(is_rmem<TA>::value, "Expected registers in MMA_Atom::call");
  static_assert(is_rmem<TB>::value, "Expected registers in MMA_Atom::call");
  static_assert(is_rmem<TC>::value, "Expected registers in MMA_Atom::call");

  // Register value types from the MMA_Operation register arrays
  using          RegTypeD = typename remove_extent<typename MMAOp::DRegisters>::type;
  using          RegTypeA = typename remove_extent<typename MMAOp::ARegisters>::type;
  using          RegTypeB = typename remove_extent<typename MMAOp::BRegisters>::type;
  using          RegTypeC = typename remove_extent<typename MMAOp::CRegisters>::type;
  using        RegTypeSFA = typename remove_extent<typename MMAOp::SFARegisters>::type;
  using        RegTypeSFB = typename remove_extent<typename MMAOp::SFBRegisters>::type;

  constexpr int   RegNumD = extent<typename MMAOp::DRegisters>::value;
  constexpr int   RegNumA = extent<typename MMAOp::ARegisters>::value;
  constexpr int   RegNumB = extent<typename MMAOp::BRegisters>::value;
  constexpr int   RegNumC = extent<typename MMAOp::CRegisters>::value;
  constexpr int RegNumSFA = extent<typename MMAOp::SFARegisters>::value;
  constexpr int RegNumSFB = extent<typename MMAOp::SFBRegisters>::value;

  auto  [A, SFA] = unzip_tensor(A_zipped);
  auto  [B, SFB] = unzip_tensor(B_zipped);
  
  using Shape_MNK = typename MMA_Traits<MMAOp>::Shape_MNK;
  constexpr int SFVecSize = MMA_Traits<MMAOp>::SFVecSize;
  
  // Assert logical size
  CUTE_STATIC_ASSERT_V(size(SFA) == size<2>(Shape_MNK{}));
  CUTE_STATIC_ASSERT_V(size(SFB) == size<2>(Shape_MNK{})); 

  // Assert physical size
  CUTE_STATIC_ASSERT(decltype(cosize(layout(SFA))){} == size<2>(Shape_MNK{}) / SFVecSize); 
  CUTE_STATIC_ASSERT(decltype(cosize(layout(SFB))){} == size<2>(Shape_MNK{}) / SFVecSize); 

  Tensor rA = recast<RegTypeA>(A);
  Tensor rB = recast<RegTypeB>(B);
  CUTE_STATIC_ASSERT_V(size(rA) == Int<RegNumA>{});
  CUTE_STATIC_ASSERT_V(size(rB) == Int<RegNumB>{});

  Tensor rD = recast<RegTypeD>(D);
  Tensor rC = recast<RegTypeC>(C);
  CUTE_STATIC_ASSERT_V(size(rD) == Int<RegNumD>{});
  CUTE_STATIC_ASSERT_V(size(rC) == Int<RegNumC>{});

  Tensor rSFA = recast<RegTypeSFA>(filter_zeros(SFA));
  Tensor rSFB = recast<RegTypeSFB>(filter_zeros(SFB));

  CUTE_STATIC_ASSERT_V(size(rSFA) == Int<RegNumSFA>{});
  CUTE_STATIC_ASSERT_V(size(rSFB) == Int<RegNumSFB>{});

  detail::explode(MMAOp::fma,
            rD,   make_int_sequence<RegNumD>{},
            rA,   make_int_sequence<RegNumA>{},
            rB,   make_int_sequence<RegNumB>{},
            rC,   make_int_sequence<RegNumC>{},
            rSFA, make_int_sequence<RegNumSFA>{},
            rSFB, make_int_sequence<RegNumSFB>{});
}
} // namespace SM120::BLOCKSCALED

////////////////////////////////////////////////////////////////////////////////////////////////////

// MMA F8F6F4 16x8x32 TN
template <class a_type, class b_type, class c_type>
struct MMA_Traits<SM120_16x8x32_TN<a_type, b_type, c_type>>
     : MMA_Traits<SM80_16x8x32_S32S8S8S32_TN>
{
  // The MMA accepts 8-bit inputs regardless of the types for A and B
  using ValTypeA = uint8_t;
  using ValTypeB = uint8_t;

  using ValTypeD = c_type;
  using ValTypeC = c_type;
};

////////////////////////////////////////////////////////////////////////////////////////////////////

// MMA MXF8F6F4 16x8x64 TN
template <class a_type, class b_type, class c_type, class sf_type, int VS>
struct MMA_Traits<SM120::BLOCKSCALED::SM120_16x8x64_TN_VS<a_type, b_type, c_type, sf_type, VS>>
{
  // The MMA accepts 4-bit inputs regardless of the types for A and B
  using ValTypeA = uint4_t;
  using ValTypeB = uint4_t;

  using ValTypeD = c_type;
  using ValTypeC = c_type;

  using ValTypeSF = sf_type;
  constexpr static int SFVecSize = VS;

  using Shape_MNK = Shape<_16,_8,_64>;
  using ThrID     = Layout<_32>;

  // (T32,V32) -> (M16,K64)
  using ALayout   = Layout<Shape <Shape <  _4,_8>,Shape < _8,_2,  _2>>,
                           Stride<Stride<_128,_1>,Stride<_16,_8,_512>>>;
  // (T32,V16) -> (M16,K64)
  using BLayout   = Layout<Shape <Shape < _4,_8>,Shape <_8,  _2>>,
                           Stride<Stride<_64,_1>,Stride<_8,_256>>>;
  // (T32,V64) -> (M16,K64)
  using SFALayout = Layout<Shape <Shape <_2,_2,_8>,_64>,  // Effectively 16 threads due to the 2:0 mode
                           Stride<Stride<_8,_0,_1>,_16>>;
  // (T32,V64) -> (N8,K64)
  using SFBLayout = Layout<Shape <Shape <_4,_8>,_64>,     // Effectively 8 threads due to the 4:0 mode
                           Stride<Stride<_0,_1>, _8>>;
  // (T32,V4)  -> (M16,N8)
  using CLayout   = SM80_16x8_Row;
};

////////////////////////////////////////////////////////////////////////////////////////////////////

// MMA MXF8F6F4 16x8x32 TN
template <class a_type, class b_type, class c_type, class sf_type, int VS>
struct MMA_Traits<SM120::BLOCKSCALED::SM120_16x8x32_TN_VS<a_type, b_type, c_type, sf_type, VS>>
{
  using UnderlyingTraits = MMA_Traits<SM120_16x8x32_TN<a_type, b_type, c_type>>;

  // The MMA accepts 8-bit inputs regardless of the types for A and B
  using ValTypeA = typename UnderlyingTraits::ValTypeA;
  using ValTypeB = typename UnderlyingTraits::ValTypeB;

  using ValTypeD = typename UnderlyingTraits::ValTypeD;
  using ValTypeC = typename UnderlyingTraits::ValTypeC;

  using Shape_MNK = typename UnderlyingTraits::Shape_MNK;
  using ThrID     = typename UnderlyingTraits::ThrID;

  using ALayout   = typename UnderlyingTraits::ALayout;
  using BLayout   = typename UnderlyingTraits::BLayout;
  using CLayout   = typename UnderlyingTraits::CLayout;

  // Scaling factor
  using ValTypeSF = sf_type;
  constexpr static int SFVecSize = VS;

  // (T32,V32) -> (M16,K32)
  using SFALayout = Layout<Shape <Shape <_2,_2,_8>,_32>,  // Effectively 16 threads due to the 2:0 mode
                           Stride<Stride<_8,_0,_1>,_16>>;
  // (T32,V32) -> (N8,K32)
  using SFBLayout = Layout<Shape <Shape <_4,_8>,_32>,     // Effectively 8 threads due to the 4:0 mode
                           Stride<Stride<_0,_1>, _8>>;
};

// Transform if needed
template<class MMA_Op, class Tensor>
CUTLASS_DEVICE void
fp4_shift_A(MMA_Op const& op, Tensor&& tensor) {
}
template<class MMA_Op, class Tensor>
CUTLASS_DEVICE void
fp4_shift_B(MMA_Op const& op, Tensor&& tensor) {
}

// For SM120 MMA F8F6F4 input fp4, the operand A/B are load from ld.matrix. 
// ld.matrix b4x16_p64 places FP4 data at the first four bits in each
// eight-bit container, whereas MMA F8F6F4 expects the four-bit data to be in 
// the middle of the eight-bit container. Thus, e2m1 operands being fed
// to MMA F8F6F4 must be shifted left by two bits.
// 0b0000ABCD --> 0b00ABCD00
// NOTE: Same transformation is NOT needed for FP6 and FP8.
template<class AType, class BType, class... MMAArgs, class Tensor>
CUTLASS_DEVICE void
fp4_shift_A(SM120_16x8x32_TN<AType, BType, MMAArgs ...> const&, Tensor&& tensor) {
  using RegisterTypeA = typename remove_extent<typename
                        SM120_16x8x32_TN<AType, BType, MMAArgs ...>::ARegisters>::type;
  if constexpr (cute::is_same_v<AType, cutlass::float_e2m1_t>) {
    cute::transform(recast<RegisterTypeA>(tensor), [](RegisterTypeA& v){ return v << 2; });
  }
}
template<class AType, class BType, class... MMAArgs, class Tensor>
CUTLASS_DEVICE void
fp4_shift_B(SM120_16x8x32_TN<AType, BType, MMAArgs ...> const&, Tensor&& tensor) {
  using RegisterTypeB = typename remove_extent<typename
                        SM120_16x8x32_TN<AType, BType, MMAArgs ...>::BRegisters>::type;
  if constexpr (cute::is_same_v<BType, cutlass::float_e2m1_t>) {
    cute::transform(recast<RegisterTypeB>(tensor), [](RegisterTypeB& v){ return v << 2; });
  }
}

namespace SM120::BLOCKSCALED {

// Template function with scale factor needs to enmuerate types one by one, as template 
// arguments contatins two variadic lists, which cannot be deduced in one shot.
template<class AType, class BType, class CType, class SFType, int VS, class Tensor>
CUTLASS_DEVICE void
fp4_shift_A(SM120::BLOCKSCALED::SM120_16x8x32_TN_VS<AType, BType, CType, SFType, VS> const&, Tensor&& tensor) {
  using RegisterTypeA = typename remove_extent<typename
                        SM120::BLOCKSCALED::SM120_16x8x32_TN_VS<AType, BType, CType, SFType, VS>::ARegisters>::type;
  if constexpr (cute::is_same_v<AType, cutlass::float_e2m1_t>) {
    cute::transform(recast<RegisterTypeA>(tensor), [](RegisterTypeA& v){ return v << 2; });
  }
}
template<class AType, class BType, class CType, class SFType, int VS, class Tensor>
CUTLASS_DEVICE void
fp4_shift_B(SM120::BLOCKSCALED::SM120_16x8x32_TN_VS<AType, BType, CType, SFType, VS> const&, Tensor&& tensor) {
  using RegisterTypeB = typename remove_extent<typename
                        SM120::BLOCKSCALED::SM120_16x8x32_TN_VS<AType, BType, CType, SFType, VS>::BRegisters>::type;
  if constexpr (cute::is_same_v<BType, cutlass::float_e2m1_t>) {
    cute::transform(recast<RegisterTypeB>(tensor), [](RegisterTypeB& v){ return v << 2; });
  }
}

}

} // end namespace cute
```

> AGENT

现在，让我检查一下 SM100 MMA traits，以便理解 UMMA 是如何封装的。

> TOOL

tool_use Bash
```json
{
  "command": "head -100 /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm100.hpp",
  "description": "Read SM100 MMA traits header"
}
```

> TOOL

tool_result Bash
```
/***************************************************************************************************
 * Copyright (c) 2022 - 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **************************************************************************************************/

#pragma once

#include <cute/config.hpp>
#include <cute/pointer_sparse.hpp>
#include <cute/tensor_impl.hpp>
#include <cute/arch/mma_sm100.hpp>
#include <cute/arch/mma_sm100_desc.hpp>
#include <cute/arch/mma_sm100_umma.hpp>
#include <cute/arch/tmem_allocator_sm100.hpp>         // cute::TMEM::

#include <cute/atom/mma_traits.hpp>
#include <cute/atom/mma_traits_sm90_gmma.hpp>         // cute::GMMA::
#include <cute/atom/mma_traits_sm90_gmma_sparse.hpp>  // cute::GMMA::
#include <cute/atom/copy_traits_sm100.hpp>            // UTCCP smem desc

#include <cute/numeric/numeric_types.hpp>

// Check that aggregate initialization in .with() initializes all fields
#if defined(__GNUG__)
#pragma GCC diagnostic warning "-Wmissing-field-initializers"
#pragma GCC diagnostic error "-Wmissing-field-initializers"
#endif

namespace cute {

namespace UMMA {

//////////////////////////////////////////////////
// Common layouts for UMMA Shared Memory //
//////////////////////////////////////////////////

using cute::GMMA::Layout_MN_INTER_Atom;
using cute::GMMA::Layout_MN_SW32_Atom;
using cute::GMMA::Layout_MN_SW64_Atom;
using cute::GMMA::Layout_MN_SW128_Atom;
using cute::GMMA::Layout_K_INTER_Atom;
using cute::GMMA::Layout_K_SW32_Atom;
using cute::GMMA::Layout_K_SW64_Atom;
using cute::GMMA::Layout_K_SW128_Atom;

using Layout_MN_SW128_32B_Atom_Bits = ComposedLayout<Swizzle<2,5,2>, smem_ptr_flag, Layout<Shape< _1024,_4>,Stride<_1, _1024>>>;

template <class Type>
using Layout_MN_SW128_32B_Atom = decltype(upcast<sizeof_bits<Type>::value>(Layout_MN_SW128_32B_Atom_Bits{}));

//////////////////////////////////////////////////
// Common layouts for Sparse UMMA Shared Memory //
//////////////////////////////////////////////////

using cute::GMMA::Layout_MN_INTER_SpAtom;
using cute::GMMA::Layout_MN_SW32_SpAtom;
using cute::GMMA::Layout_MN_SW64_SpAtom;
using cute::GMMA::Layout_MN_SW128_SpAtom;
using cute::GMMA::Layout_K_INTER_SpAtom;
using cute::GMMA::Layout_K_SW32_SpAtom;
using cute::GMMA::Layout_K_SW64_SpAtom;
using cute::GMMA::Layout_K_SW128_SpAtom;

template <class Type, int S>
using Layout_MN_SW128_32B_SpAtom = ComposedLayout<Swizzle<2,5,2>, smem_sparse_ptr_flag_bits<S,sizeof_bits_v<Type>>,
                                                  decltype(blocked_product(Layout<Shape<_1,Int<S>>>{}, Layout_MN_SW128_32B_Atom<Type>{}.layout_b()))>;

// With UMMA::Major param
template <class Type, int S, UMMA::Major tnsp>
using Layout_INTER_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
                                                 Layout_MN_INTER_SpAtom<Type,S>,
                                                 Layout_K_INTER_SpAtom<Type,S>>::type;
template <class Type, int S, UMMA::Major tnsp>
using Layout_SW32_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"SM100_MMA_F16BF16\\|TmemAllocator\\|UMMA\\|tcgen05\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm100.hpp | head -20",
  "description": "Find SM100 UMMA MMA trait key lines"
}
```

> TOOL

tool_result Bash
```
57:namespace UMMA {
60:// Common layouts for UMMA Shared Memory //
78:// Common layouts for Sparse UMMA Shared Memory //
94:// With UMMA::Major param
95:template <class Type, int S, UMMA::Major tnsp>
96:using Layout_INTER_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
99:template <class Type, int S, UMMA::Major tnsp>
100:using Layout_SW32_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
103:template <class Type, int S, UMMA::Major tnsp>
104:using Layout_SW64_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
107:template <class Type, int S, UMMA::Major tnsp>
108:using Layout_SW128_SpAtom = typename conditional<tnsp == UMMA::Major::MN,
156:    static_assert(M==5,   "Only 16B and 32B Atoms are supported for UMMA. Unsupported layout swizzle.");
162:// Construction method for UMMA Descriptors
179:*   m  : integer in [1,16] corresponding to UMMA shape
180:*   k  : integer in [1,32] corresponding to UMMA shape
184:* See UMMA::Layout_MN_XXX_Atom<value_type> for building canonical UmmaDescriptor Major-MN layouts.
199:* See UMMA::Layout_K_XXX_Atom<value_type> for building canonical UmmaDescriptor Major-K layouts.
204:template <UMMA::Major MajorMode, class TEngine, class TLayout>
209:  static_assert(is_smem<TEngine>::value, "UMMA Descriptors can only be constructed on smem.");
```

> AGENT

现在让我检查 FA3 源代码，以参考 sm90 的 wgmma 实现。

> TOOL

tool_use Bash
```json
{
  "command": "find / -name \"flash_fwd_kernel.h\" -path \"*flash-attention*\" -o -name \"flash_fwd_kernel.h\" -path \"*flash_attention*\" -o -name \"flash_fwd_kernel.h\" -path \"*fa3*\" 2>/dev/null | head -5",
  "description": "Find FA3 source files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/deps/repo-flash-attention/csrc/flash_attn/src/flash_fwd_kernel.h
```

> TOOL

tool_use Bash
```json
{
  "command": "pip show flash-attn 2>/dev/null | head -5; pip show flash-attn-3 2>/dev/null | head -5",
  "description": "Check installed FA3"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/deps/repo-flash-attention/csrc/flash_attn/src/ | head -30",
  "description": "List FA3 source directory"
}
```

> TOOL

tool_result Bash
```
alibi.h
block_info.h
dropout.h
flash.h
flash_bwd_hdim128_bf16_causal_sm80.cu
flash_bwd_hdim128_bf16_sm80.cu
flash_bwd_hdim128_fp16_causal_sm80.cu
flash_bwd_hdim128_fp16_sm80.cu
flash_bwd_hdim192_bf16_causal_sm80.cu
flash_bwd_hdim192_bf16_sm80.cu
flash_bwd_hdim192_fp16_causal_sm80.cu
flash_bwd_hdim192_fp16_sm80.cu
flash_bwd_hdim256_bf16_causal_sm80.cu
flash_bwd_hdim256_bf16_sm80.cu
flash_bwd_hdim256_fp16_causal_sm80.cu
flash_bwd_hdim256_fp16_sm80.cu
flash_bwd_hdim32_bf16_causal_sm80.cu
flash_bwd_hdim32_bf16_sm80.cu
flash_bwd_hdim32_fp16_causal_sm80.cu
flash_bwd_hdim32_fp16_sm80.cu
flash_bwd_hdim64_bf16_causal_sm80.cu
flash_bwd_hdim64_bf16_sm80.cu
flash_bwd_hdim64_fp16_causal_sm80.cu
flash_bwd_hdim64_fp16_sm80.cu
flash_bwd_hdim96_bf16_causal_sm80.cu
flash_bwd_hdim96_bf16_sm80.cu
flash_bwd_hdim96_fp16_causal_sm80.cu
flash_bwd_hdim96_fp16_sm80.cu
flash_bwd_kernel.h
flash_bwd_launch_template.h
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -l \"wgmma\\|WGMMA\\|SM90_64x64\\|TMA_LOAD\\|tma_load\" /user_4813494d/deps/repo-flash-attention/csrc/flash_attn/src/*.h 2>/dev/null | head -10",
  "description": "Find FA3 files with wgmma/TMA"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> AGENT

这是 FA2，不是 FA3。让我在线查找 FA3。

> TOOL

tool_use Bash
```json
{
  "command": "find / -name \"flash3*\" -path \"*/flash*\" -type d 2>/dev/null | head -5; find / -name \"flash_attn_3*\" -path \"*/site*\" -type d 2>/dev/null | head -5",
  "description": "Find FA3 installation"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16\\|wgmma\\|WGMMA\" /user_4813494d/deps/repo-flash-attention/csrc/flash_attn/src/kernel_traits.h 2>/dev/null | head -10",
  "description": "Check if FA2 repo has wgmma"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> AGENT

让我简要查阅 FA3 的 GitHub 仓库，以理解其结构，并检查 FlashInfer 对 SM120 的支持。

> TOOL

tool_use mcp__exa__web_search_exa
```json
{
  "numResults": 5,
  "query": "Flash Attention 3 FA3 wgmma TMA sm90 kernel_traits.h source code github tri dao"
}
```

> TOOL

tool_result mcp__exa__web_search_exa
```
Title: csrc/flash_attn/src/kernel_traits.h at main · Dao-AILab/flash-attention
URL: https://github.com/Dao-AILab/flash-attention/blob/main/csrc/flash_attn/src/kernel_traits.h
Published: N/A
Author: N/A
Highlights:
# File: Dao-AILab/flash-attention/csrc/flash_attn/src/kernel_traits.h
[...]
Q_K_smem;
[...]
iledMma = TiledMMA<
        typename Base::MMA_
[...]
KSmem>, _1>>{}));
    using SmemLayoutQ = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockM>, Int<kHeadDim>>{}));

    using SmemLayoutKV = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockN>, Int<kHeadDim>>{}));

    // https://github.com/ColfaxResearch/cutlass-kernels/blob/a222587e6d59b93ba704853d3946fb686d8b8892/src/fmha/fmha_forward.cu#L434
    using SmemLayoutVtransposed = decltype(
        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
    using SmemLayoutVtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutVtransposed{}));

    using SmemLayoutAtomO = decltype(
        composition(Swizzle<kSwizzle,
[...]
3, 3>{},
                    Layout<Shape<Int<8>, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutO = decltype(tile_to_shape(
        SmemLayoutAtomO{},
        Shape<Int<
[...]
BlockM>, Int<kHeadDim>>{}));
    using SmemCopyAtomO = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>;
    using SmemCopyAtomOaccum = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>;

    static constexpr int kSmemQSize = size(SmemLayoutQ{}) * sizeof(Element);
    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
    static constexpr int kSmemSize = Share_Q_K_smem ? std::max(kSmemQSize, kSmemKVSize) : kSmemQSize + kSmemKVSize;

    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
    // Using kBlockKSmem here is 6-10% faster than kBlockKGmem for d=128 because of bank conflicts.
    // For example, for d=1
[...]
split into 2 "pages", each
[...]
em,
    // thread

---

Title: csrc/flash_attn/src/flash_fwd_launch_template.h at 3387de49 · Dao-AILab/flash-attention
URL: https://github.com/Dao-AILab/flash-attention/blob/3387de49/csrc/flash_attn/src/flash_fwd_launch_template.h
Published: N/A
Author: N/A
Highlights:
typename Kernel_traits, bool Is_dropout, bool Is_causal>
[...]
void run_flash_fwd(Flash_fwd_params &params, cudaStream_t stream) {
    constexpr size_t smem_size = Kernel_traits::kSmemSize;
    // printf("smem_size = %d\n", smem_size);

    // Work-around for gcc 7. It doesn't like nested BOOL_SWITCH.
    // https://github.com/kokkos/kokkos-kernels/issues/349
    // https://github.com/HazyResearch/flash-attention/issues/21
[...]
const int num_m_block = (params.
[...]
len_q + Kernel_traits::kBlockM -
[...]
1) / Kernel_traits::kBlockM;
[...]
dim3 grid(num_m_block, params.b, params.h);
    const
[...]
= params.
[...]
_seqlens_q ==
[...]
&& params.cu_seqlens_k == nullptr && params.
[...]
len_k %
[...]
_traits::k
[...]
== 0 && params.
[...]
len_q % Kernel_traits::kBlockM ==
[...]
const bool
[...]
= params.d == Kernel_traits::kHeadDim;
[...]
_right >= 0) && !Is_causal, Is_local, [&] {
                BOOL_SWITCH(
[...]
_softmax, ReturnSoftmaxConst, [&]
[...]
ALIBI_SWITCH(params.alibi_slopes_ptr != nullptr, Has_alibi, [&] {
                        SOFTCAP
[...]
(params.softcap > 0.0, Is_softcap
[...]
// If
[...]
KConst, we
[...]
// If
[...]
// If head dim >
[...]
128, set IsEvenMNConst to false to reduce number of templates
                            // If
[...]
local, set Is_causal to false
                            auto kernel = &
[...]
_fwd_kernel<Kernel_traits, Is_dropout &&
[...]
Is_softcap
[...]
Is_causal, Is_local && !Is_causal
[...]
Has_al
[...]
Is_local
[...]
Has_alibi
[...]
Const && Kernel_traits::kHeadDim <=
[...]
128, IsEvenKConst && !ReturnSoftmaxConst && !Has_alibi, Is_softcap, ReturnSoftmaxConst && Is_dropout &&
[...]
Is_softcap
[...]
// auto kernel = &
[...]
_fwd
[...]
kernel<Kernel_traits, false, Is_causal, false, false, true, true,
[...]
>;
                            // printf("IsEvenMNConst = %d, IsEvenKConst = %d
[...]
Is_local = %d, Is_causal = %
[...]
IsEvenMNConst

---

Title: flash-attn/flash_bwd_kernel_sm90.h · kernels-community/flash-attn3 at bc10fdce7000c4e39e9c2d2aec60d10a45b45a77
URL: https://huggingface.co/kernels-community/flash-attn3/blob/bc10fdce7000c4e39e9c2d2aec60d10a45b45a77/flash-attn/flash_bwd_kernel_sm90.h
Published: N/A
Author: N/A
Highlights:
flash-attn/flash_bwd_kernel_sm90.h · kernels-community/flash-attn3 at bc10fdce7000c4e39e9c2d2aec60d10a45b45a77
[...]
|
| #include |
| #include |
| #include |
| #include |
| #include |
| #include "cutlass/pipeline/pipeline.hpp" |
| #include "utils.h" |
[...]
| namespace flash { |
| using namespace cute; |
| template |
| class FlashAttnBwdSm90 { |
| public: |
[...]
Mainloop derived types |
[...]
| using CollectiveMainloop = CollectiveMainloop_; |
| using TileShape_MNK = typename CollectiveMainloop::TileShape_MNK; |
| using TiledMmaSdP = typename CollectiveMainloop::TiledMmaSdP; |
| using TiledMmadKV = typename CollectiveMainloop::TiledMmadKV; |
| using ArchTag = typename CollectiveMainloop::ArchTag; |
| using ClusterShape = typename CollectiveMainloop::ClusterShape; |
| using MainloopArguments = typename CollectiveMainloop::Arguments; |
| using MainloopParams = typename CollectiveMainloop::Params; |
| static constexpr bool dKV_swapAB = CollectiveMainloop::dKV_swapAB; |
[...]
smem_buf
[...]
(&shared_
[...]
| // Initialize matmul objects. |
| TiledMmadKV tiled_mma_dKV; |
| PipelineState smem_pipe_read; |
| PipelineState_dO smem_pipe_read_do; |
| mainloop.mma_init(); |
| scheduler.init_consumer(); |
[...]
| // dK and dV output accumulator. |
| Tensor tdKrdK = partition_fragment_C(tiled_mma_dKV, select (TileShape_MNK{})); |
| Tensor tdVrdV = partition_fragment_C(tiled_mma_dKV, select (TileShape_MNK{})); |
[...]
| bool tile_valid = mainloop.mma( |
| params.mainloop, pipeline_q, pipeline_do, smem_pipe_read, smem_pipe_read_do, |
| tdKrdK, tdVrdV, threadIdx.x - NumCopyThreads, work_idx, block_coord, shared_storage); |
[...]
| if (tile_valid) { |
| epilogue.store(params.epilogue, tdKrdK, tdVrdV, shared_storage, tiled_mma_dKV, |
| threadIdx.x - NumCopyThreads, block_coord); |
| } else { |
|
[...]
ilogue.store_zero(params.
[...]
ilogue, threadIdx
[...]
x - NumCopyThreads, block_coord); |

---

Title: tridao/flash-attention-wheels
URL: https://github.com/tridao/flash-attention-wheels
Published: 2023-08-03T08:10:07.000Z
Author: N/A
Highlights:
# Repository: tridao/flash-attention-wheels
[...]
# FlashAttention
[...]
This repository provides the official implementation of FlashAttention and
FlashAttention-2 from the
following papers.
[...]
**FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness** 
Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré 
Paper: https://arxiv.org/abs/2205.14135 
IEEE Spectrum article about our submission to the MLPerf 2.0 benchmark using FlashAttention.
FlashAttention
[...]
**FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning** 
Tri Dao

Paper: https://tridao.me/publications/flash2/flash2.pdf
[...]
Interface: `src/flash_attention_interface.py`
[...]
## Upgrading from FlashAttention (1.x) to FlashAttention-2
[...]
## Full model code and training script
[...]
## Triton implementation of FlashAttention
[...]
Phil Tillet (OpenAI) has an experimental implementation of FlashAttention in Triton:
https://github.com/openai/triton/blob/master/python/tutorials/06-fused-attention.py
[...]
We also have an experimental implementation in Triton that support attention
bias (e.g. ALiBi):
[...]
https://github.com/Dao-AILab/flash-attention/blob/main/flash_attn/flash_attn_triton.py
[...]
```
@inproceedings{dao2022flashattention,
  title={Flash{A}ttention: Fast and Memory-Efficient Exact Attention with {IO}-Awareness},
  author={Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
  booktitle={Advances in Neural Information Processing Systems},
  year={2022}
}
[...]
@article{dao2023flashattention2,
  title={Flash{A}ttention-2: Faster Attention with Better Parallelism and Work Partitioning,
  author={Dao, Tri},
  year={2023}
}

---

Title: [Sm90] Add script to search fwd bwd configs · 5c7c494 · Dao-AILab/flash-attention
URL: https://github.com/Dao-AILab/flash-attention/commit/5c7c4947d5c339993b4058fdae51d788f2416242
Published: 2026-03-15T13:52:03.000Z
Author: tridao
Highlights:
## [Sm90] Add script to search fwd bwd configs
[...]
(head_dim, head_dim_v, causal, local
[...]
"""Return BwdConfig for SM90
[...]
Configs based on C++ FA3 hopper/flash_bwd_launch_template.h
[...]
### flash_attn/cute/sm90_config_search.py
[...]
+"""Search feasible SM90 backward configs for given (head_dim, head_dim_v).
+
+Each config specifies tile sizes, swap modes, atom layouts, and staging.
+Constraints: GMMA M-dim divisible by 64, register budget, smem budget (224 KB).
+
+Usage:
+    python flash_attn/cute/bwd_config_search.py --headdim 128
+    python flash_attn/cute/bwd_config_search.py --headdim 192-128
+"""
+
+
[...]
mma(M, N, num_wg, atom_layout_m, swap_AB):
[...]
Check MMA feasibility
[...]
per WG, or None if infeasible.
[...]
M-dim is always 64
[...]
Swap exchanges (M, N) and atom layout
[...]
+    Requires: eff_m divisible by (atom_layout_m * 64), eff_n by atom_layout_n.
[...]
+    """
[...]
+    if swap_AB:
+        M, N = N, M
[...]
+        atom_layout_m = num_wg // atom_layout_m
[...]
+    atom_layout_n
[...]
num_wg //
[...]
_layout_m
[...]
+    if M % (atom_layout_m * 64) != 0 or
[...]
atom_layout_n
[...]
+def _check_config(
+    hdim,
+    hdimv,
+    tile_m,
+    tile_n,
+    num_wg,
+    SdP_swapAB,
+    dKV_swapAB,
+    dQ_swapAB,
+    AtomLayoutMSdP,
+    AtomLayoutNdKV,
+    AtomLayoutMdQ,
+):
+    """Check a single config. Returns dict if feasible, None otherwise."""
+    reg_limit = REG_LIMITS[num_wg]
[...]
MMA feasibility: SdP, dK, dV, dQ
[...]
+    regs_SdP
[...]
_check_mma(tile_m, tile_n, num_wg, AtomLayoutMSdP, SdP_swapAB
[...]
+    regs_dK
[...]
_check_mma(tile_n, hdim, num
[...]
wg, AtomLayoutNdKV, dKV_swapAB)
[...]
+    regs_dV = _check_mma(tile_n, hdimv, num_wg, AtomLayoutNdKV, dKV_swapAB
[...]
_mma(tile_m, hdim, num
[...]
wg, AtomLayoutMdQ, dQ_swapAB
[...]
regs_dK, regs_dV, regs
[...]
2) + TMA load
[...]
head_dim,
+    head_dim_v=None
[...]
tile_m_choices=(64,
[...]
tile_n_choices
[...]
hdimv
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"sm120\\|sm_120\\|SM120\\|120\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/ --include=\"*.cu\" --include=\"*.cuh\" -l 2>/dev/null | head -10",
  "description": "Find FlashInfer SM120 kernel files"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/fmha_v2_run.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/group_gemm_mxfp4_groupwise_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/gemm_groupwise_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/fp4_gemm_cutlass_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/group_gemm_nvfp4_groupwise_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/gemm_sm120_binding.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/group_gemm_fp8_groupwise_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/group_gemm_sm120_binding.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/mxfp8_gemm_cutlass_sm120.cu
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/csrc/trtllm_fmha_v2_binding.cu
```

> AGENT

现在我来检查 FA3 的源代码结构，并查看 SM90 wgmma 内核的结构。

> TOOL

tool_use mcp__exa__web_fetch_exa
```json
{
  "maxCharacters": 5000,
  "urls": [
    "https://github.com/Dao-AILab/flash-attention/tree/main/csrc/flash_attn/src"
  ]
}
```

> TOOL

tool_result mcp__exa__web_fetch_exa
```
Error fetching URL(s): https://github.com/Dao-AILab/flash-attention/tree/main/csrc/flash_attn/src: CRAWL_NOT_FOUND
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"SM90_64x64x16\\|SM90_128x.*x16_F16\\|SM90_.*wgmma\\|SM90_GMMA\\|GMMA_\" /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp 2>/dev/null | head -15",
  "description": "Find SM90 GMMA MMA trait names"
}
```

> TOOL

tool_result Bash
```
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:                         "Not a canonical GMMA_MN Layout: Expected K-size 256/sizeof_bits<T> for dense or (128|512)/sizeof_bits<T> for sparse.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    CUTE_STATIC_ASSERT_V(congruent(canonical_layout, Shape<Shape<_1,_1>,Shape<_1,_1>>{}), "Not a canonical GMMA_MN Layout: Expected profile failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    static_assert(stride_00 == expected_stride_00, "Not a canonical GMMA_MN Layout: Expected stride failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    static_assert(stride_10 == expected_stride_10, "Not a canonical GMMA_MN Layout: Expected stride failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:                         "Not a canonical GMMA_K Layout: Expected MN-size multiple of 8.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:                         "Not a canonical GMMA_K Layout: Expected K-size 2 for dense or 4 for sparse (in units of uint128_t).");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    CUTE_STATIC_ASSERT_V(congruent(canonical_layout, Shape<Shape<_1,_1>,Shape<_1,_1>>{}), "Not a canonical GMMA_K Layout: Expected profile failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    static_assert(stride_00 == expected_stride_00, "Not a canonical GMMA_K Layout: Expected stride failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:    static_assert(stride_10 == expected_stride_10, "Not a canonical GMMA_K Layout: Expected stride failure.");
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:using SM90_64x64x16_F16F16F16_SS = SM90::GMMA::MMA_64x64x16_F16F16F16_SS<tnspA, tnspB, scaleA, scaleB>;
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:struct MMA_Traits<SM90_64x64x16_F16F16F16_SS<tnspA, tnspB, scaleA, scaleB>>
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:using SM90_64x64x16_F16F16F16_RS = SM90::GMMA::MMA_64x64x16_F16F16F16_RS<tnspA, tnspB, scaleA, scaleB>;
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:struct MMA_Traits<SM90_64x64x16_F16F16F16_RS<tnspA, tnspB, scaleA, scaleB>>
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:using SM90_64x64x16_F32F16F16_SS = SM90::GMMA::MMA_64x64x16_F32F16F16_SS<tnspA, tnspB, scaleA, scaleB>;
/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/include/cute/atom/mma_traits_sm90_gmma.hpp:struct MMA_Traits<SM90_64x64x16_F32F16F16_SS<tnspA, tnspB, scaleA, scaleB>>
```

> AGENT

现在我有了足够的信息来提供一个全面的分析。让我再核对一件事——FA3 (sm90) 分支的结构。

> TOOL

tool_use mcp__exa__web_fetch_exa
```json
{
  "maxCharacters": 4000,
  "urls": [
    "https://github.com/Dao-AILab/flash-attention/blob/main/csrc/flash_attn/src/kernel_traits.h"
  ]
}
```

> TOOL

tool_result mcp__exa__web_fetch_exa
```
# csrc/flash_attn/src/kernel_traits.h at main · Dao-AILab/flash-attention
URL: https://github.com/Dao-AILab/flash-attention/blob/main/csrc/flash_attn/src/kernel_traits.h

# File: Dao-AILab/flash-attention/csrc/flash_attn/src/kernel_traits.h

- Repository: Dao-AILab/flash-attention | Fast and memory-efficient exact attention | 23K stars | Python
- Branch: main

```h
/******************************************************************************
 * Copyright (c) 2024, Tri Dao.
 ******************************************************************************/

#pragma once

#include "cute/tensor.hpp"

#include "cutlass/cutlass.h"
#include "cutlass/layout/layout.h"
#include <cutlass/numeric_types.h>

using namespace cute;

template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t>
struct Flash_kernel_traits {

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
    using Element = elem_type;
    static constexpr bool Has_cp_async = true;
#else
    using Element = cutlass::half_t;
    static constexpr bool Has_cp_async = false;
#endif

    using ElementAccum = float;
    using index_t = int64_t;

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
    using MMA_Atom_Arch = std::conditional_t<
        std::is_same_v<elem_type, cutlass::half_t>,
        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,
        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>
    >;
#else
    using MMA_Atom_Arch = MMA_Atom<SM75_16x8x8_F32F16F16F32_TN>;
#endif

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 750
    using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>;
    using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>;
#else
    using SmemCopyAtom = Copy_Atom<DefaultCopy, elem_type>;
    using SmemCopyAtomTransposed = Copy_Atom<DefaultCopy, elem_type>;
#endif
};

// If Share_Q_K_smem is true, that forces Is_Q_in_regs to be true
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, bool Is_Q_in_regs_=false, bool Share_Q_K_smem_=false, typename elem_type=cutlass::half_t,
         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
struct Flash_fwd_kernel_traits : public Base {
    using Element = typename Base::Element;
    using ElementAccum = typename Base::ElementAccum;
    using index_t = typename Base::index_t;
    static constexpr bool Has_cp_async = Base::Has_cp_async;
    using SmemCopyAtom = typename Base::SmemCopyAtom;
    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;

    static constexpr bool Share_Q_K_smem = Share_Q_K_smem_;
    static constexpr bool Is_Q_in_regs = Is_Q_in_regs_ || Share_Q_K_smem;

    // The number of threads.
    static constexpr int kNWarps = kNWarps_;
    static constexpr int kNThreads = kNWarps * 32;

    static constexpr int kBlockM = kBlockM_;
    static constexpr int kBlockN = kBlockN_;
    static constexpr int kHeadDim = kHeadDim_;
    static_assert(kHeadDim % 32 == 0);
    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;

    using TiledMma = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<kNWarps>,_1,_1>>,  // 4x1x1 or 8x1x1 thread group
        Tile<Int<16 * kNWarps>, _16, _16>>;

    using SmemLayoutAtomQ = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    // This has to be kBlockKSmem, using kHeadDim gives wrong results for d=128
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutQ = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockM>, Int<kHeadDim>>{}));

    using SmemLayoutKV = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockN>, Int<kHeadDim>>{}));

    // https://github.com/ColfaxResearch/cutlass-kernels/blob/a222587e6d59b93ba704853d3946fb686d8b8892/src/fmha/fmha_forward.cu#L434
    using SmemLayoutVtransposed = decltype(
        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
    using SmemLayoutVtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutVtransposed{}));

    using SmemLayoutAtomO = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<Int<8>, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutO = decltype(tile_to_shape(
        SmemLayoutAtomO{},
        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
    using SmemCopyAtomO = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>;
    using SmemCopyAtomOaccum = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>;

    static constexpr int kSmemQSize = size(SmemLayoutQ{}) * sizeof(Element);
    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
    static constexpr int kSmemSize = Share_Q_K_smem ? std::max(kSmemQSize, kSmemKVSize) : kSmemQSize + kSmemKVSize;

    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
    // Using kBlockKSmem here is 6-10% faster than kBlockKGmem for d=128 because of bank conflicts.
    // For example, for d=128, smem is split into 2 "pages", each page takes care of columns
    // 0-63 and 64-127. If we have 16 threads per row for gmem read, when we write to smem,
    // thread 0 - 7 will write to the first page and thread 8 - 15 will write to the second page,
    // to the same banks.
    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
                                  Stride<Int<kGmemThreadsPerRow>, _1>>;

    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
    // from the same address by the same threadblock. This is slightly faster.
    using Gmem_copy_struct = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
        AutoVectorizingCopyWithAssumedAlignment<128>
    >;
    using GmemTiledCopyQKV = decltype(
        make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
    using GmemTiledCopyO = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per store

    using GmemLayoutAtomOaccum = std::conditional_t<
        kBlockKSmem == 32,
        Layout<Shape <_16, _8>,  // Thread layout, 8 threads per row
               Stride< _8, _1>>,
        Layout<Shape <_8, _16>,  // Thread layout, 16 threads per row
               Stride< _16, _1>>
    >;
    using GmemTiledCopyOaccum = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
                        GmemLayoutAtomOaccum{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
    using GmemLayoutAtomRotcossin = GmemLayoutAtom;
    using GmemTiledCopyRotcossin = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint64_t>, Element>{},
                        GmemLayoutAtomRotcossin{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per load
    using GmemTiledCopyRotcossinCont = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, Element>{},
                        GmemLayoutAtomRotcossin{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per load
};

// Is_V_in_regs is an option to reduce smem usage, but will increase register pressue.
// No_double_buffer is another option to reduce smem usage, but will slow things down.
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_,
         int AtomLayoutMSdP_=1, int AtomLayoutNdKV=2, int AtomLayoutMdQ=2,
         bool Is_V_in_regs_=false, bool No_double_buffer_=false, typename elem_type=cutlass::half_t,
         typename Base=Flash_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
struct Flash_bwd_kernel_traits : public Base {
    using Element = typename Base::Element;
    using ElementAccum = typename Base::ElementAccum;
    using index_t = typename Base::index_t;
    static constexpr bool Has_cp_async = Base::Has_cp_async;
    using SmemCopyAtom = typename Base::SmemCopyAtom;
    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;

    static constexpr bool Is_V_in_regs = Is_V_in_regs_;
    static constexpr bool No_double_buffer = No_double_buffer_;

    // The number of threads.
    static constexpr int kNWarps = kNWarps_;
    static constexpr int kNThreads = kNWarps * 32;

    static constexpr int kBlockM = kBlockM_;
    static constexpr int kBlockN = kBlockN_;
    static constexpr int kHeadDim = kHeadDim_;
    static_assert(kHeadDim % 32 == 0);
    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;

    static constexpr int AtomLayoutMSdP = AtomLayoutMSdP_;
    static_assert(kNWarps % AtomLayoutMSdP == 0);
    static_assert(kNWarps % AtomLayoutNdKV == 0);
    static_assert(kNWarps % AtomLayoutMdQ == 0);

    using TiledMmaSdP = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutMSdP>, Int<kNWarps / AtomLayoutMSdP>, _1>>,
        Tile<Int<16 * AtomLayoutMSdP>, Int<16 * kNWarps / AtomLayoutMSdP>, _16>>;

    using TiledMmadKV = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutNdKV>, Int<kNWarps / AtomLayoutNdKV>, _1>>,
        Tile<Int<16 * AtomLayoutNdKV>, Int<16 * kNWarps / AtomLayoutNdKV>, _16>>;

    using TiledMmadQ = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutMdQ>, Int<kNWarps / AtomLayoutMdQ>, _1>>,  // 2x4x1 or 4x2x1 thread group
        Tile<Int<16 * AtomLayoutMdQ>, Int<16 * kNWarps / AtomLayoutMdQ>, _16>>;

    using SmemLayoutAtomQdO = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutQdO = decltype(tile_to_shape(
        SmemLayoutAtomQdO{},
        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));

    using SmemLayoutAtomKV = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<Int<kBlockM / kNWarps>, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutKV = decltype(tile_to_shape(
        // SmemLayoutAtomQdO{},
        SmemLayoutAtomKV{},
        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));

    using SmemLayoutKtransposed = decltype(
        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
    using SmemLayoutKtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutKtransposed{}));

    // TODO: generalize to other values of kBlockN
    // TODO: what should be the Swizzle here? 3 is faster than 1, and 1 is faster than 2
    // static constexpr int kPBlockN = kBlockN;
    // Temporarily disabling this for hdim 256 on sm86 and sm89
    // static_assert(kBlockN >= 64);
    static_assert(kBlockN >= 32);
    // TD [2023-03-19]: Idk why kPBlockN = 16 and kSwizzlePdS=3 is the fastest.
    static constexpr int kPBlockN = kBlockN >= 64 ? 64 : 32;
    static_assert(kPBlockN == 16 || kPBlockN == 32 || kPBlockN == 64);
    // static constexpr int kSwizzlePdS = kPBlockN == 16 ? 1 : (kPBlockN == 32 ? 2 : 3);
    static constexpr int kSwizzlePdS = 3;
    using SmemLayoutAtomPdS = decltype(
        composition(Swizzle<kSwizzlePdS, 3, 3>{},
                    Layout<Shape<Int<kBlockM>, Int<kPBlockN>>,
                           Stride<Int<kPBlockN>, _1>>{}));
    using SmemLayoutPdS = decltype(tile_to_shape(
        SmemLayoutAtomPdS{},
        make_shape(Int<kBlockM>{}, Int<kBlockN>{})));
    using SmemLayoutPdStransposed = decltype(
        composition(SmemLayoutPdS{}, make_layout(Shape<Int<kBlockN>, Int<kBlockM>>{}, GenRowMajor{})));
    using SmemLayoutPdStransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutPdStransposed{}));

    using SmemCopyAtomPdS = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;

    using SmemLayoutQdOtransposed = decltype(
        composition(SmemLayoutQdO{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockM>>{}, GenRowMajor{})));
    using SmemLayoutQdOtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutQdOtransposed{}));

    using SmemLayoutAtomdKV = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutdKV = decltype(tile_to_shape(
        SmemLayoutAtomdKV{},
        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
    using SmemCopyAtomdKV = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;

    using SmemLayoutAtomdQ = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutdQ = decltype(tile_to_shape(
        SmemLayoutAtomdQ{},
        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
    using SmemCopyAtomdQ = Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>;

    // Double buffer for sQ
    static constexpr int kSmemQdOSize = size(SmemLayoutQdO{}) * (No_double_buffer ? 2 : 3) * sizeof(Element);
    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
    static constexpr int kSmemdSSize = size(SmemLayoutPdS{}) * sizeof(Element);
    static constexpr int kSmemPSize = size(SmemLayoutPdS{}) * sizeof(Element);
    static constexpr int kSmemdQSize = size(SmemLayoutdQ{}) * sizeof(Element);
    static constexpr int kSmemSize = kSmemQdOSize
        + (!Is_V_in_regs
           ? kSmemKVSize + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)
           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)));
    static constexpr int kSmemSize1colblock = kSmemQdOSize
        + (!Is_V_in_regs
           ? kSmemKVSize + kSmemdSSize + kSmemPSize
           : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + kSmemPSize));

    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
    // Using kBlockKSmem instead of kHeadDim here to avoid bank conflicts, but doesn't seem
    // to affect speed in practice.
    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
                                  Stride<Int<kGmemThreadsPerRow>, _1>>;

    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
    // from the same address by the same threadblock. This is slightly faster.
    using Gmem_copy_struct = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
        AutoVectorizingCopyWithAssumedAlignment<128>
    >;
    using GmemTiledCopyQKV = decltype(
        make_tiled_copy(Copy_Atom<Gmem_copy_struct, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
    using GmemTiledCopydO = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
    using GmemTiledCopydKV = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
    using GmemTiledCopydQ = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
    using GmemLayoutAtomdQaccum = std::conditional_t<
        kBlockKSmem == 32,
        Layout<Shape <_32, _8>,  // Thread layout, 8 threads per row
               Stride< _8, _1>>,
        Layout<Shape <_16, _16>,  // Thread layout, 16 threads per row
               Stride< _16, _1>>
    >;
    using GmemTiledCopydQaccum = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
                        GmemLayoutAtomdQaccum{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store

    using GmemTiledCopydQaccumAtomicAdd = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopyWithAssumedAlignment<128>, ElementAccum>{},
                        Layout<Shape <_8, _32>,  // Thread layout, 8 threads per row
                               Stride<_32, _1>>{},
                        Layout<Shape < _1, _1>>{}));  // Val layout, 1 val per store

};

////////////////////////////////////////////////////////////////////////////////////////////////////

```
```

> AGENT

现在我对代码库有了全面的了解。请允许我整理这份全面的分析报告。

---

# 综合分析：为 SM_120 (Blackwell) 添加 WGMMA + TMA 路径

## A. 现有架构摘要

### A.1 Flash_fwd_kernel_traits 的完整模板参数和 MMA/Copy atom 选择逻辑

**文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h`

**基础特征 (Flash_kernel_traits)**：
```cpp
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t>
struct Flash_kernel_traits {
    // MMA Atom 选择：SM80 mma.sync（16x8x16）
    using MMA_Atom_Arch = std::conditional_t<
        std::is_same_v<elem_type, cutlass::half_t>,
        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,   // FP16
        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>   // BF16
    >;
    // Smem Copy Atom：LDSM (SM75+)
    using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>;
    using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>;
};
```

**前向特征 (Flash_fwd_kernel_traits)**：
```cpp
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_,
         bool Is_Q_in_regs_=false, bool Share_Q_K_smem_=false,
         typename elem_type=cutlass::half_t, typename Base=...>
struct Flash_fwd_kernel_traits : public Base {
    // TiledMma：基于 mma.sync 的 1D-warp-vote layout
    using TiledMma = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<kNWarps>,_1,_1>>,
        Tile<Int<16 * kNWarps>, _16, _16>>;

    // Gmem Copy：SM80 cp.async (16-byte 搬运)
    using Gmem_copy_struct = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,   // <-- cp.async
        AutoVectorizingCopyWithAssumedAlignment<128>
    >;
    using GmemTiledCopyQKV = decltype(
        make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{},
                        GmemLayoutAtom{}, Layout<Shape<_1, _8>>{}));
};
```

**关键设计约束**：
- 当前 block 配置：`kBlockM=16, kBlockN=64, kNWarps=1`（来自 `run_mha_fwd_hdim128`）
- 这是因为该代码库面向的是解码场景（`seqlen_q=1`，GQA 交换后变成 `kBlockM=16`）
- 单 warp 设计，MMA 的 M 维度 = `16 * kNWarps = 16`，与 `kBlockM` 一致
- `kBlockKSmem = 64`，`kSwizzle = 3`

### A.2 run_flash_fwd 的 kernel launch 流程

**文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h`

```cpp
template<typename Kernel_traits, bool Is_dropout, bool Is_causal>
void run_flash_fwd(Flash_fwd_params &params, cudaStream_t stream) {
    constexpr size_t smem_size = Kernel_traits::kSmemSize;
    // smem_size = kSmemQSize + kSmemKVSize (不共享时)
    //           = 16*128*2 + 64*128*2*2 = 4KB + 32KB = 36KB (hdim128 bf16)
    
    const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM;
    dim3 grid(num_m_block, params.b, params.h);
    
    if (smem_size >= 48 * 1024) {
        C10_CUDA_CHECK(cudaFuncSetAttribute(
            kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size));
    }
    kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params);
    // kNThreads = 32 (1 warp)
}
```

**Grid**：`(num_m_blocks, batch_size, num_heads)` -- 每个 (batch, head) 串行处理其 M blocks

### A.3 compute_attn_1rowblock 的主循环结构

**文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h`

**核心循环是单 stage 的软件流水线**：
```
1. Load Q from gmem -> smem (cp.async)
2. Load K[n_block_max-1] from gmem -> smem (cp.async fence)
3. If Is_Q_in_regs: wait cp_async<1>, copy Q smem -> regs
4. Clear acc_o
5. [Masking loop] for masking_step in 0..n_masking_steps:
     a. cp_async_wait<0>(); __syncthreads()
     b. Load V[n_block] gmem -> smem (cp.async fence)
     c. MMA: Q * K -> acc_s (gemm with smem->reg copy + mma.sync)
     d. Apply mask
     e. Softmax rescale
     f. Convert acc_s to fp16 -> rP
     g. MMA: rP * V -> acc_o (gemm_rs)
     h. Prefetch K[n_block - leap] (cp.async fence)
6. [Inner loop] for n_block = next_block_idx down to n_block_min:
     Same as 5 but without masking
7. Epilogue: normalize, convert, write O to gmem
```

**Pipeline 特征**：
- 仅 1 stage 深度（load next K while computing current K*Q）
- V 的 load 和当前 QK 的 MMA 有重叠
- 没有多缓冲（double buffering），这是 SM80 的简单流水线
- 使用 `cp_async_wait<0>()`（等待全部完成），而非 `wait_group<1>`（SM90 pipeline 模式）

### A.4 fwdIterator 的接口和遍历逻辑

**文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h`

```cpp
class fwdIterator {
    uint64_t *blockmask_ptr;  // 压缩的 bitmap (每 bit 代表一个 K block)
    int m_block_dim, n_block_dim;  // 16, 64
    int cache_seqlen_k;  // actual_seqlen_k - actual_seqlen_q / m_block_dim
    int max_block_idx;   // ceil_div(actual_seqlen_k, n_block_dim)

    // 核心方法：找 <= target 的最大已设置 bit
    __device__ int max_no_larger(int target) const;
};
```

在 kernel 中的使用：
```cpp
fwdIterator blockmask(params, binfo, kBlockM, kBlockN, bidb, bidh, m_block, n_block_min, n_block_max);
int next_block_idx = blockmask.max_no_larger(n_block_max-1);
// 主循环中：
for (n_block = next_block_idx; ...; n_block = next_block_idx) {
    next_block_idx = blockmask.max_no_larger(n_block - 1);
    // leap = n_block - next_block_idx (跳过的 block 数)
}
```

这使得 kernel 可以跳过被 blockmask 掉的 K/V blocks，避免无效计算。

---

## B. 迁移到 WGMMA + TMA 的技术要点

### B.1 SM120 (Blackwell) 的 MMA Atom -- 关键发现

**SM120 没有原生的 FP16/BF16 WGMMA！** 这是一个关键发现。

在 FlashInfer 自带的 CUTLASS 3.x 中（位于 `/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/flashinfer/data/cutlass/`）：

- `cute/arch/mma_sm120.hpp` 定义了 `SM120_16x8x32_TN` 系列，但仅支持 **FP8/F6/F4** 数据类型（e2m1, e3m2, e4m3, e5m2）。这些是 `mma.sync` 指令（`kind::f8f6f4`），不是 WGMMA。

- SM120 的 UMMA（相当于 SM90 的 WGMMA）被定义在 `cute/arch/mma_sm100_umma.hpp` 中，名为 `SM100_MMA_F16BF16_SS` / `SM100_MMA_F16BF16_TS`。这是 `tcgen05.mma` 指令。

**SM100/SM120 UMMA 的核心特征**：
```cpp
struct SM100_MMA_F16BF16_SS<a_type, b_type, c_type, M, N, a_major, b_major> {
    // M = 64 or 128, N = 8..256 (multiple of 8)
    using ARegisters = uint64_t[1];  // TMA descriptor, 不是寄存器！
    using BRegisters = uint64_t[1];  // TMA descriptor
    using CRegisters = uint32_t[1];  // TMEM pointer
    
    fma(uint64_t desc_a, uint64_t desc_b, uint32_t tmem_c, uint32_t scaleC, uint64_t idescE);
    // asm: "tcgen05.mma.cta_group::1.kind::f16 [%0], %1, %2, %3, ..."
};
```

**与 SM90 WGMMA 的根本区别**：
| 特征 | SM90 WGMMA | SM100/SM120 UMMA |
|------|-----------|------------------|
| 指令 | `wgmma.mma_async` | `tcgen05.mma` |
| MMA Atom | `SM90_64x64x16_F32F16F16F32_SS` | `SM100_MMA_F16BF16_SS` |
| A 操作数来源 | smem (直接) | smem via **TMA descriptor** |
| B 操作数来源 | smem (直接) | smem via **TMA descriptor** |
| C 操作数位置 | 寄存器 | **TMEM** (Tensor Memory) |
| 最小 M 维度 | 64 | 64 |
| 执行方式 | warp-group (4 warps) | CTA-level (`elect_one_sync`) |
| 需要集群 | 否 (1 CTA) | 否 (1 CTA) |

### B.2 TMA Copy Atom 的接口差异

SM90 TMA：
```cpp
SM90_TMA_LOAD  -> Copy_Traits<SM90_TMA_LOAD, NumBitsPerTMA>
    // 需要 tma_desc + tma_mbar
SM90_TMA_STORE -> 类似
```

SM100 TMA：
```cpp
SM100_TMA_2SM_LOAD -> Copy_Traits<SM100_TMA_2SM_LOAD, NumBitsPerTMA>
    // 支持 2-SM 协同加载
```

SM120 的 TMA 接口复用 SM100 的 TMA 描述符格式。TMA 描述符在 host 端通过 `cute::create_tma_descriptor` 构造。

### B.3 现有 CUTLASS 版本

**setup.py** 中的 include path：
```python
include_dirs=[
    Path(this_dir) / "csrc" / "flash_attn",
    Path(this_dir) / "csrc" / "flash_attn" / "src",
    Path(this_dir) / "csrc" / "cutlass" / "include",  # <-- 但此目录不存在！
]
```

实际 CUTLASS 来源：通过 PyTorch 2.11.0+cu130 的 `torch.utils.cpp_extension` 自动引入的系统 CUTLASS。FlashInfer 自带的 CUTLASS 有 SM120 支持，但当前代码库没有引用它。

**CUTLASS 版本判断**：FlashInfer 的 CUTLASS 包含 `cute/arch/mma_sm120.hpp`（Copyright 2025-2026 NVIDIA），说明这是 CUTLASS 3.8+，支持 SM120。但当前项目的 `csrc/cutlass/` 目录为空。

### B.4 如果 CUTLASS 不支持 SM120 的替代方案

当前环境已有 FlashInfer 的 CUTLASS（支持 SM120），可以：
1. 将 FlashInfer 的 CUTLASS include path 添加到 setup.py
2. 或者安装 CUTLASS 3.8+ 到 `csrc/cutlass/include/`

---

## C. 工程量评估

### C.1 需要修改的文件

| 文件 | 改动量 | 改动内容 |
|------|--------|----------|
| `kernel_traits.h` | **~300 行新增** | 新增 `Flash_fwd_kernel_traits_sm120` 特化，使用 UMMA + TMA descriptor layout，TMEM 管理，完全不同的 smem layout |
| `flash_fwd_kernel.h` | **~500 行新增** | 新增 `compute_attn_1rowblock_sm120`，重写主循环以使用 UMMA pipeline + TMA load + TMEM accumulator + pipeline 同步 |
| `flash_fwd_launch_template.h` | **~50 行修改** | 添加 sm120 的 dispatch 逻辑 |
| `flash.h` | **~10 行** | 添加 TMA descriptor 相关参数到 Flash_fwd_params |
| `flash_api.cpp` | **~50 行修改** | 在 dispatch 中添加 sm120 分支，构造 TMA descriptor |
| `generate_kernels.py` | **~10 行** | 添加 SM=120 |
| `setup.py` | **~5 行** | 添加 sm_120 gencode，更新 CUTLASS include path |
| 新增 `.cu` 文件 | **4 个** | `flash_fwd_hdim128_bf16_sm120.cu` 等 |

### C.2 最小可行路径（hdim128 + bf16 + sm120）的新增代码量

**至少 800-1000 行新 kernel 代码**，原因如下：

1. **UMMA 的编程模型与 mma.sync 完全不同**：
   - A/B 操作数不再从 smem 直读，而是通过 TMA descriptor
   - C 操作数在 TMEM 而非寄存器
   - 需要 `elect_one_sync()` 而非 warp-level 操作
   - 需要 `TMEM::Allocator` 管理 TMEM

2. **Smem layout 必须满足 TMA descriptor 的对齐和 swizzle 要求**：
   - 当前 `SmemLayoutAtomQ` 使用 `Swizzle<3,3,3>` + 8x64
   - UMMA 要求 `UMMA::Layout_K_SW128_Atom` 或 `UMMA::Layout_MN_INTER_Atom` 等特定布局

3. **Pipeline 机制完全不同**：
   - SM90+ 使用 `cutlass::Pipeline`（Producer-Consumer 模式）
   - 需要 TMA barrier (`tma_load_barrier`)，不能用简单的 `cp_async_fence/wait`

4. **kBlockM = 16 不可行**：UMMA 的最小 M 维度是 64。这意味着：
   - 必须改用 `kBlockM = 64, kNWarps = 4`（4 个 warp 组成一个 warp-group）
   - 或者 `kBlockM = 128`，这改变了整个 kernel 的调度语义
   - 这对解码场景（seqlen_q=1）意味着一个 CTA 处理 64 个 query token，而原来只处理 16 个

### C.3 不可绕过的技术障碍

1.  **CUTLASS 版本**：当前项目的 `csrc/cutlass/` 为空目录，实际使用的 CUTLASS 可能不包含 SM120 支持。需要升级 CUTLASS 到 3.8+ 或引入 FlashInfer 的 CUTLASS。

2.  **UMMA M 维度约束**：最小 M=64，与当前解码配置 `kBlockM=16` 不兼容。这意味着：
    - 对于 prefill（seqlen_q 较大），可以使用 `kBlockM=128, kNWarps=8`
    - 对于 decode（seqlen_q=1），UMMA 反而可能不如 mma.sync 高效，因为浪费了计算资源

3.  **TMEM 管理**：UMMA 的 accumulator 在 TMEM 中，需要 `cute::TMEM::Allocator` 预分配和释放。这改变了 softmax 的实现方式（需要从 TMEM 读出 softmax 分数）。

4.  **TMA descriptor 构造**：需要在 host 端为 Q/K/V 创建 TMA descriptor，这要求输入张量满足 TMA 的对齐要求（至少 16B 对齐，某些 layout 需要 128B 对齐）。

5.  **Paged KV cache 兼容性**：当前代码支持 paged KV cache（block_table），但 TMA descriptor 假设连续内存。Paged KV cache 需要间接寻址，与 TMA 不兼容。SplitKV 路径可能需要保留 cp.async。

6.  **Blockmask 迭代器**：当前 `fwdIterator` 的 `max_no_larger` 按顺序遍历 block，而 TMA 可以一次加载一个 tile，不影响。但 UMMA 的最小 M=64 可能导致 blockmask 的粒度不匹配。

---

## D. 可行性判断

### D.1 FA3 的源码结构参考

FA3（flash-attention main 分支的 SM90 路径）已经实现了 wgmma + TMA。其结构是：

- 使用 CUTLASS 3.x 的 `CollectiveMainloop` 模式，而非当前代码的手写循环
- 使用 `cutlass::Pipeline` 进行 Producer-Consumer 同步
- 使用 `SM90_64x64x16_F32F16F16F32_SS` 作为 MMA Atom
- 使用 `SM90_TMA_LOAD` 进行 Q/K/V 加载
- 有独立的 SM90 kernel 文件：`flash_fwd_kernel_sm90.h`

**但是**：FA3 的 SM90 代码是 wgmma（warp-group MMA），而 SM120 使用 UMMA（CTA-level MMA with TMEM）。两者的编程模型差异很大：

| | FA3 SM90 | SM120 |
|--|---------|-------|
| MMA 指令 | `wgmma.mma_async` | `tcgen05.mma` |
| Accumulator | 寄存器 | TMEM |
| A/B 来源 | smem (swizzled) | smem via TMA desc |
| 同步 | warp-group level | CTA level |
| Pipeline | cute::gemm + manual | cutlass::Pipeline |

**FA3 的代码不能直接 fork**，但可以作为架构参考（尤其是 pipeline 结构、split-KV、epilogue）。

### D.2 替代方案：直接调用 FlashInfer

**FlashInfer 已经支持 SM120**（其 CUTLASS 包含 SM120 MMA traits，且其编译上下文已处理 `compute_120f` 等 arch）。

**替代方案评估**：

1.  **直接替换为 FlashInfer 的 attention kernel**：
    - 优点：零开发成本，FlashInfer 已有 SM120 优化
    - 缺点：需要改造上层调用接口（`Flash_fwd_params` -> FlashInfer 的参数结构），且 FlashInfer 的 blockmask 机制可能不同

2.  **混合方案**：
    - SM120 decode 路径：保留 mma.sync + cp.async（因为 kBlockM=16 不满足 UMMA 最小 M=64 的约束，UMMA 在 decode 场景反而低效）
    - SM120 prefill 路径：使用 FlashInfer 或新写 UMMA kernel
    - 关键观察：**当前的 kBlockM=16, kNWarps=1 配置是为了 decode 优化的，而 UMMA 的最小 M=64 决定了它在 decode 场景没有优势**

3.  **最务实的建议**：
    - 对于 decode（`seqlen_q=1`，swap 后 `kBlockM=16`）：**继续使用 mma.sync + cp.async**。SM120 完全兼容 SM80 的 mma.sync 指令，编译为 sm_120 时可以正常运行。
    - 对于 prefill（`seqlen_q` 较大）：**集成 FlashInfer 的 SM120 prefill kernel**
    - 只有在 prefill 成为瓶颈且需要极致性能时，才值得为 SM120 写自定义 UMMA kernel

### 总结

| 方案 | 开发量 | 风险 | 性能收益 |
|------|--------|------|----------|
| 什么都不做（sm_80 代码在 sm_120 上跑） | 0 | 低（兼容） | 基线（mma.sync 性能） |
| 为 SM120 添加 UMMA+TMA prefill kernel | 1000+ 行 | 高 | prefill 30-50% 提升 |
| 集成 FlashInfer 的 SM120 kernel | 200-300 行接口适配 | 中 | 取决于 FlashInfer 优化程度 |
| 完整重写 decode+prefill | 2000+ 行 | 很高 | decode 几乎无收益 |

**结论**：对于 decode 场景（kBlockM=16），SM120 的 UMMA 不可用（最小 M=64），mma.sync 已是最优选择。建议先在 setup.py 中添加 `sm_120` gencode 让现有代码在 Blackwell 上原生运行，然后评估是否需要为 prefill 路径集成 FlashInfer 的 SM120 kernel。
