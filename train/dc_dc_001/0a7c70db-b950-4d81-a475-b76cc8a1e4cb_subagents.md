> DEVELOPER

请深入分析 /user_4813494d/openbmb/kernels/infllmv2_cuda_impl 目录下的所有代码，寻找潜在的性能优化点。 背景： - 这是 InfLLM-v2 稀疏注意力的 CUDA 实现，用于 MiniCPM-SALA 的长上下文推理 - 硬件：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM） - CUDA toolkit 13.2，PyTorch 2.11.0+cu130，FlashInfer 0.6.8.post1 - standard Attention 层超过 dense_len=8192 时走 InfLLM-v2 稀疏（compress_k → stage1 block_score → stage2 top-K sparse FA） 请完整阅读： 1. 所有 .cu / .cuh / .cpp / .py 文件 2. 任何 CMakeLists.txt 或 setup.py 3. 头文件和接口定义 分析维度： 1. **算法层面**：计算流程是否有冗余？block_score 计算、top-K 选取、sparse FA 是否可以 fuse？ 2. **内存访问**：global memory 访问模式是否 coalesced？有无不必要的 host↔device 拷贝？shared memory 利用率？ 3. **并行度**：grid/block 配置是否合理？有无序列化的 bottleneck（如 atomics、synchronization）？ 4. **sm_120 特性**：是否利用了 Blackwell 的 warp-group MMA、async copy、TMA？有无可以升级的旧接口？ 5. **Python 绑定层**：有无可以消除的 Python overhead 或 tensor 拷贝？ 6. **与 FlashInfer 的交互**：是否完全利用了 FlashInfer 的稀疏 attention API？有无绕路的地方？ 请给出： - 目录结构概览 - 每个优化点的：位置（文件:行号）、问题描述、预期收益（高/中/低） - 最值得动手的前 3 个优化点（按 ROI 排序） 请尽量详细，搜索范围要 very thorough。

> AGENT

我将首先探索目录结构，然后系统地阅读所有源文件。

> AGENT

现在让我并行读取所有关键源文件。我将从核心自定义 CUDA 文件和 Python 绑定开始。

> AGENT

现在我来阅读所有 Python 文件和 Flash Attention 的关键头文件。

> AGENT

现在让我阅读 Flash Attention 的关键头文件，以理解 blockmask 和内核的实现。

> AGENT

现在我来读取 flash 前向传播的内核头文件，以理解实际的注意力计算逻辑。

> AGENT

现在让我搜索 flash 前向传播内核中的关键模式，特别是 `blockmask` 的遍历和 MMA 操作。

> AGENT

让我更仔细地检查反向传播的 blockmask 转换以及 `cu_seqlens` 扩展循环。

> AGENT

现在让我再检查一件事—— `max_pooling_1d_varlen_kernel` 中线性搜索批次以及 `topk` kernel 配置。

> AGENT

让我检查一下 `num_k_heads` 是如何硬编码的，并验证 topk 内核的块维度问题。

> AGENT

现在我对整个代码库有了全面的了解。让我再检查一个方面——stage1 内核如何处理 `block_score` 计算。

> AGENT

我现在对代码库有了全面的了解。下面我将整理详细的分析报告。 --- ## 目录结构概览 ``` infllmv2_cuda_impl/ csrc/ entry.cu -- pybind11 入口，所有 kernel 的 C++ 绑定 get_probs.cuh -- softmax 概率恢复 kernel topk.cuh -- bitonic top-k kernel max_pooling_1d.cuh -- max pooling 1D（含 varlen 版本） blockmask_to_uint64.cuh -- bool mask -> uint64 打包 topk_to_uint64.cuh -- top-k index -> uint64 打包 uint64_to_bool.cuh -- uint64 -> bool 解包 trait.cuh -- half/bf16 类型 trait utils.cuh -- 宏定义和 CUDA 检查 flash_attn/ flash_api.cpp -- FlashAttention C++ 入口（varlen_fwd, varlen_fwd_stage1, varlen_bwd, fwd_kvcache） src/ flash.h -- 参数结构体（Flash_fwd_params / Flash_bwd_params） flash_fwd_kernel.h -- forward kernel 实现（compute_attn_1rowblock, splitkv, stage1） flash_fwd_launch_template.h-- kernel launch 模板和 hdim dispatch flash_blockmask.h -- fwdIterator / bwdIterator（uint64 blockmask 遍历器） block_info.h -- BlockInfo（varlen 偏移计算） kernel_traits.h -- CUTLASS kernel traits（MMA atom, smem layout, copy atom） softmax.h / mask.h / ... -- 辅助头文件 flash_fwd_hdim*_sm80.cu -- 各 headdim 的编译单元 infllm_v2/ __init__.py -- Python 包入口 infllmv2_sparse_attention.py -- 主 Python 接口（forward/backward Function, stage1, kvcache） topk_to_uint64.py -- topk_to_uint64 Python 封装 blockmask_to_uint64.py -- blockmask_to_uint64 Python 封装 uint64_to_bool.py -- uint64_to_bool Python 封装 max_pooling_1d.py -- max_pooling_1d Python 封装 setup.py -- 构建脚本 ``` --- ## 详细优化点分析 ### 1. 算法层面 **优化点 1.1: backward 路径中 uint64 blockmask 的冗余转换链** - 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:343-350` - 描述: 反向传播中，将 `fwd_blockmask_uint64` 先解包成 bool (`cuda_uint64_to_bool`)，转置后再重新打包成 uint64 (`cuda_blockmask_to_uint64`)。这条路径是: `uint64 -> bool -> transpose -> bool -> uint64`，中间产生了两个大 tensor（bool mask 很大，每个 block 1 byte），且有一次 `.contiguous()` 拷贝和一次 `torch.cuda.synchronize()`。实际上可以直接在 GPU 上对 uint64 做转置，或者在 kernel 中直接做 column-oriented 读取。 - 预期收益: **高**。这个同步点在每次反向传播中都会触发，bool mask 的大小是 uint64 mask 的 ~8x。消除同步和两步 kernel 可节省数毫秒。 **优化点 1.2: topk_to_uint64 + varlen_fwd 两步可 fuse** - 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py:93` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk_to_uint64.cuh` - 描述: 当前流程是 `topk_indices -> topk_to_uint64 kernel -> uint64 blockmask -> varlen_fwd kernel`。topk_to_uint64 生成的 uint64 blockmask 被写入 global memory，然后立刻被 varlen_fwd 读取。可以将 topk_to_uint64 的逻辑内联到 varlen_fwd kernel 的 prologue 中，在 shared memory 中直接构建 blockmask 行，避免一次 global memory round-trip。 - 预期收益: **中**。取决于 topk 的 K 值大小；若 K 较小（如 16-32），uint64 mask 行只有几个 uint64，shared memory 完全放得下。 **优化点 1.3: stage1 (block_score) 输出的 max_pooling + topk 可部分 fuse** - 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh` 和 `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/topk.cuh` - 描述: 当前 stage1 输出 attention scores 后，需要 max_pooling_1d 做下采样，然后 topk 选取。max_pooling_1d 的输出是 topk 的输入。两者可以 fuse 为一个 kernel：在 max_pooling 输出每个位置时，同时维护一个 warp-level top-k 结构，避免将完整下采样结果写回 global memory。 - 预期收益: **中**。取决于 block 数量（out_len），通常为 128-512，一个 warp 内做 bitonic top-k 开销不大。 **优化点 1.4: get_probs kernel 可内联到 stage1 输出** - 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/get_probs.cuh:7-15` - 描述: `get_probs_kernel` 做的是 `exp(v * scale - lse[bid])`，这是一个 element-wise 操作。如果这个操作只在 stage1 的输出上使用（将 score 转为概率），可以直接在 stage1 kernel 的 epilogue 中完成，而不是单独发射一个 kernel。 - 预期收益: **低到中**。单个 elementwise kernel 开销本身不大，但减少一次 kernel launch 和 global memory 读写仍有帮助。 ### 2. 内存访问 **优化点 2.1: max_pooling_1d_varlen_kernel 线性搜索 batch** - 位置: `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/max_pooling_1d.cuh:44-54` - 描述: 每个 thread 做 `for (int b = 0; […]

> DEVELOPER

请深入阅读 /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/ 下的所有代码，目标是搞清楚"为 sm_120 (Blackwell) 添加 wgmma + TMA 路径"需要做什么、能怎么做。 硬件背景： - NVIDIA RTX 6000D，sm_120 (Blackwell)，84 GB VRAM - CUDA toolkit 13.2，CUTLASS 已可用 - 当前 MMA Atom 是 SM80_16x8x16_F32F16F16F32_TN（mma.sync），未用 wgmma - 当前数据加载是 SM80_CP_ASYNC_CACHEGLOBAL（cp.async），未用 TMA 请完整阅读以下文件（全文，不要截断）： 1. csrc/flash_attn/src/kernel_traits.h 2. csrc/flash_attn/src/flash_fwd_launch_template.h 3. csrc/flash_attn/src/flash_fwd_kernel.h 4. csrc/flash_attn/src/flash_blockmask.h 5. csrc/flash_attn/src/flash.h 6. csrc/flash_attn/src/block_info.h 7. csrc/flash_attn/flash_api.cpp（重点看 varlen_fwd, varlen_fwd_stage1, fwd_kvcache 的 dispatch 逻辑） 8. csrc/flash_attn/src/flash_fwd_hdim128_fp16_sm80.cu（了解现有编译单元结构） 9. setup.py（了解编译命令和 gencode 配置） 10. 任何 flash_fwd_hdim*_sm*.cu 文件 分析以下问题并给出详细结论： **A. 现有架构摘要** - `Flash_fwd_kernel_traits` 的完整模板参数和 MMA/Copy atom 选择逻辑 - `run_flash_fwd` 在 `flash_fwd_launch_template.h` 中的 kernel launch 流程（smem size、grid、block） - `compute_attn_1rowblock` 的主循环结构（Q/K/V load → MMA → softmax → output，关键的流水线 stage 数） - `flash_blockmask.h` 中 fwdIterator 的接口和遍历逻辑 **B. 迁移到 wgmma + TMA 的技术要点** - CUTLASS 3.x 中 sm_120 对应的 wgmma MMA Atom 名称（如 SM90_64x64x16_F32F16F16F32_SS 等，但这是 sm_90；sm_120/Blackwell 的对应 atom 是什么） - CUTLASS 3.x 中 TMA copy atom（SM90_TMA_LOAD / SM120_TMA_LOAD）的接口差异 - 现有代码用了哪个版本的 CUTLASS（查 setup.py 的 include path 或 CMakeLists） - 如果现有 CUTLASS 版本不支持 sm_120，替代方案是什么 **C. 工程量评估** - 需要修改哪些文件，每个文件大概改动量 - 最小可行路径（只改 hdim128 + bf16 + sm_120）需要新增多少代码 - 有哪些不可绕过的技术障碍（如 CUTLASS 版本限制、API 不兼容等） **D. 可行性判断** - Flash Attention 3（FA3）已经实现了 sm_90 的 wgmma + TMA。FA3 的源码结构是否可以直接参考或 fork？ - 是否有更简单的替代方案，比如：直接调用 FlashInfer（已支持 sm_120）的 kernel，而不是修改这个自定义 FA fork？ 请给出所有文件的关键代码片段（函数签名、模板参数、关键循环），以支撑你的结论。搜索深度：very thorough。

> AGENT

我将首先阅读所有指定的文件，以彻底理解代码库。让我开始并行阅读这些文件。

> AGENT

现在让我分部分读取 `flash_fwd_kernel.h` 文件，并找到 `.cu` 文件和 `setup.py`。

> AGENT

现在让我阅读剩余的内核文件并找到 `.cu` 文件。

> AGENT

现在让我检查 CUTLASS 版本并查看可用的 SM120 相关定义。

> AGENT

太棒了！让我阅读关键文件——SM120 MMA 定义和 SM100/SM120 的 TMA/COPY 定义。

> AGENT

这非常具有启发性。让我再检查几项关键内容。

> AGENT

现在让我检查 Flash Attention 3 (FA3) 源码结构，并查看 FlashInfer 如何处理 SM120。

> AGENT

现在，我将查看 FA3 源代码的可用性，并检查现有代码库中的 `generate_kernels.py` 和 `utils.h`。

> AGENT

现在，我将阅读 SM100 UMMA 文件，以了解 Blackwell 对 FP16/BF16 的 MMA 指令。

> AGENT

现在我来检查 SM120 MMA traits，以理解 CuTe 如何封装 SM120 MMA atoms。

> AGENT

现在，让我检查一下 SM100 MMA traits，以便理解 UMMA 是如何封装的。

> AGENT

现在让我检查 FA3 源代码，以参考 sm90 的 wgmma 实现。

> AGENT

这是 FA2，不是 FA3。让我在线查找 FA3。

> AGENT

让我简要查阅 FA3 的 GitHub 仓库，以理解其结构，并检查 FlashInfer 对 SM120 的支持。

> AGENT

现在我来检查 FA3 的源代码结构，并查看 SM90 wgmma 内核的结构。

> AGENT

现在我有了足够的信息来提供一个全面的分析。让我再核对一件事——FA3 (sm90) 分支的结构。

> AGENT

现在我对代码库有了全面的了解。请允许我整理这份全面的分析报告。 --- # 综合分析：为 SM_120 (Blackwell) 添加 WGMMA + TMA 路径 ## A. 现有架构摘要 ### A.1 Flash_fwd_kernel_traits 的完整模板参数和 MMA/Copy atom 选择逻辑 **文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/kernel_traits.h` **基础特征 (Flash_kernel_traits)**： ```cpp template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t> struct Flash_kernel_traits { // MMA Atom 选择：SM80 mma.sync（16x8x16） using MMA_Atom_Arch = std::conditional_t< std::is_same_v<elem_type, cutlass::half_t>, MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>, // FP16 MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN> // BF16 >; // Smem Copy Atom：LDSM (SM75+) using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>; using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>; }; ``` **前向特征 (Flash_fwd_kernel_traits)**： ```cpp template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, bool Is_Q_in_regs_=false, bool Share_Q_K_smem_=false, typename elem_type=cutlass::half_t, typename Base=...> struct Flash_fwd_kernel_traits : public Base { // TiledMma：基于 mma.sync 的 1D-warp-vote layout using TiledMma = TiledMMA< typename Base::MMA_Atom_Arch, Layout<Shape<Int<kNWarps>,_1,_1>>, Tile<Int<16 * kNWarps>, _16, _16>>; // Gmem Copy：SM80 cp.async (16-byte 搬运) using Gmem_copy_struct = std::conditional_t< Has_cp_async, SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>, // <-- cp.async AutoVectorizingCopyWithAssumedAlignment<128> >; using GmemTiledCopyQKV = decltype( make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{}, GmemLayoutAtom{}, Layout<Shape<_1, _8>>{})); }; ``` **关键设计约束**： - 当前 block 配置：`kBlockM=16, kBlockN=64, kNWarps=1`（来自 `run_mha_fwd_hdim128`） - 这是因为该代码库面向的是解码场景（`seqlen_q=1`，GQA 交换后变成 `kBlockM=16`） - 单 warp 设计，MMA 的 M 维度 = `16 * kNWarps = 16`，与 `kBlockM` 一致 - `kBlockKSmem = 64`，`kSwizzle = 3` ### A.2 run_flash_fwd 的 kernel launch 流程 **文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h` ```cpp template<typename Kernel_traits, bool Is_dropout, bool Is_causal> void run_flash_fwd(Flash_fwd_params &params, cudaStream_t stream) { constexpr size_t smem_size = Kernel_traits::kSmemSize; // smem_size = kSmemQSize + kSmemKVSize (不共享时) // = 16*128*2 + 64*128*2*2 = 4KB + 32KB = 36KB (hdim128 bf16) const int num_m_block = (params.seqlen_q + Kernel_traits::kBlockM - 1) / Kernel_traits::kBlockM; dim3 grid(num_m_block, params.b, params.h); if (smem_size >= 48 * 1024) { C10_CUDA_CHECK(cudaFuncSetAttribute( kernel, cudaFuncAttributeMaxDynamicSharedMemorySize, smem_size)); } kernel<<<grid, Kernel_traits::kNThreads, smem_size, stream>>>(params); // kNThreads = 32 (1 warp) } ``` **Grid**：`(num_m_blocks, batch_size, num_heads)` -- 每个 (batch, head) 串行处理其 M blocks ### A.3 compute_attn_1rowblock 的主循环结构 **文件**：`/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h` **核心循环是单 stage 的软件流水线**： ``` 1. Load Q from gmem -> smem (cp.async) 2. Load K[n_block_max-1] from gmem -> smem (cp.async fence) 3. If Is_Q_in_regs: wait cp_async<1>, copy Q smem -> regs 4. Clear acc_o 5. [Masking loop] for masking_step in 0..n_masking_steps: a. cp_async_wait<0>(); __syncthreads() b. Load V[n_block] gmem -> smem (cp.async fence) c. MMA: Q * K -> acc_s (gemm with smem->reg copy + mma.sync) d. Apply mask e. Softmax rescale f. Convert acc_s to fp16 -> rP g. MMA: rP * V -> acc_o (gemm_rs) h. Prefetch K[n_block - leap] (cp.async fence) 6. [Inner loop] for n_block = next_block_idx down to n_block_min: Same as 5 but without masking 7. Epilogue: normalize, convert, write O to gmem ``` **Pipeline 特征**： - 仅 1 […]
