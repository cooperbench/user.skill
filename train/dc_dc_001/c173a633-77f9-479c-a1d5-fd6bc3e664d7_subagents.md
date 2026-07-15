---
session_id: "c173a633-77f9-479c-a1d5-fd6bc3e664d7:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-27T21:12:44.363Z"
n_turns: 29
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

我们要在 SGLang fork 上实现"按 running batch size 动态切换推测解码模式"，需要你详细梳理代码： **上下文**： - 工作目录 `/user_4813494d/openbmb`，SGLang fork 在 `demo-sala/sglang/python/sglang/` - 当前用 EAGLE-3 chain verify，启动脚本 `eval/start_eagle.sh`：`spec_steps=2, topk=2, dtn=5` - 已落地 MARS verify（θ=0.85），改动在 `sgl-kernel/csrc/speculative/eagle_utils.cu` 和 `demo-sala/sglang/.../eagle_utils.py` - `SGLANG_ENABLE_SPEC_V2=0` 当前关闭，使用 v1 路径（`eagle_worker.py`），v2 入口在 `eagle_worker_v2.py` **目标方案**： - bs > 32：整 batch 全部走 no-spec（关 EAGLE，普通 decode） - 1 < bs ≤ 32：MARS tree，θ=0.85，topk=2，draft=2（dtn=5） - bs = 1：MARS tree，θ=0.85，topk=2，draft=3（dtn=7） - 关键约束：**全体样本切**，不是只对新样本。bs 增长穿过阈值时，正在运行的所有请求都要立即跟着切 **请回答以下问题**（按重要性排序，每个问题都要给具体文件+行号）： 1. **batch 调度入口**：scheduler 哪里决定一个 step 的 running batch（哪个文件、哪个函数）？running batch 的 size 在何处可读？例如 `scheduler.py` 的 event loop、`get_next_batch_to_run` 等。`spec v1` 和 `spec v2 overlap` 的入口有什么差别？ 2. **EAGLE worker 入口**：`eagle_worker.py` 和 `eagle_worker_v2.py` 中 `forward_batch_generation` 或同类函数。draft → verify 的主循环是什么样？`spec_steps`、`topk`、`num_draft_tokens` 在哪里被消费？是 worker 初始化时就固定，还是每 step 可读？ 3. **CUDA graph 与 spec 形状的绑定**： - draft model 的 graph capture 在哪里？是否对 `topk × spec_steps` 形状做了 capture？ - target verify 的 graph 是否对 `dtn` 形状 capture？capture 的 batch size 列表是什么？ - 如果运行时 dtn 在 5 ↔ 7 之间切换，graph 是否要重新 capture？SGLang 是否支持多 graph（按 dtn 分桶）？ - `--cuda-graph-bs` 之类的参数怎么设置（看 `server_args.py`）？ 4. **no-spec 切换可能性**： - 同一 worker 实例能否在 step-level 切换 "走 EAGLE" vs "走普通 decode"？看是否存在 fallback 路径（例如 spec 失败时回退）。 - `forward_batch_generation` 是否 hard-coded 走 spec_info 路径？是否有 enable/disable spec 的开关？ - 如果切到 no-spec，draft KV / verify state 怎么处理？是否需要 flush？ 5. **dtn 动态调整**： - `speculative_num_steps` / `speculative_eagle_topk` / `speculative_num_draft_tokens` 在哪些数据结构中被持有？是 `ServerArgs` 一处常量，还是每个 batch 都重新读？ - 如果不重启 server，是否能把 dtn 在 5 ↔ 7 之间切？draft tree 形状（mask、parent、position）怎么生成的？ - 看一下 `eagle_utils.py` 里 build draft tree / decode_tree_mask 的逻辑 6. **现有钩子**： - `start_eagle.sh` 有 `EAGLE_FORCE_NO_ACCEPT` 环境变量，看它是怎么实现的（grep 一下），这是不是一个潜在的"批量绕过 spec"钩子？ - `EAGLE_MARS_THETA` 怎么传到 verify kernel？是 step-level 读还是 worker init 时读？ - 是否还有其他"per-step 动态参数"通道？ 7. **scheduler 视角拿到 running bs**： - scheduler.py 的 event loop（v1 / v2 overlap 两条路径）在 forward 之前，是否已经把 running batch 准备好？bs 在哪个变量里？ - 在 forward 之前能否调用 worker 上的"set spec mode"接口？ **输出格式**： - 每个问题独立小节，给出关键代码段（带文件:行号）+ 简短结论 - 末尾给"切换可行性快评"，明确指出哪些可做、哪些是大坑（例如：CUDA graph 必须重 capture 是否成立？dtn 切换会不会破坏 draft 内部 buffer？spec → no-spec 转换时正在 verify 的请求怎么处理？） 不要给实现代码，只做调研。预算 thorough。

> AGENT

我来详细梳理 SGLang fork 中关于推测解码的代码架构。这是一个复杂的系统，我会按照问题顺序逐一深入调查。

> AGENT

让我重点看 demo-sala 这条线，因为题目明确指向它：

> AGENT

继续看 scheduler 的核心循环：

> AGENT

现在看 run_batch 以及 forward_batch_generation：

> AGENT

现在看 ScheduleBatch 中的 batch_size() 方法和 running_batch 如何被持有：

> AGENT

找 ScheduleBatch 定义：

> AGENT

现在看 eagle_worker.py 和 v2 的详情：

> AGENT

现在看 eagle_worker_v2：

> AGENT

现在看 spec_info 和 eagle_utils：

> AGENT

现在查看 CUDA graph 的初始化和 dtn 的使用：

> AGENT

现在看 server_args.py 中 spec 相关参数的定义：

> AGENT

现在查找 EAGLE_MARS_THETA 和 EAGLE_FORCE_NO_ACCEPT：

> AGENT

现在查看 start_eagle.sh 的参数：

> AGENT

现在查看 verify 流程相关的内核代码：

> AGENT

题目中提到内核代码在 `sgl-kernel/csrc/speculative/eagle_utils.cu`，但实际上看起来 sgl-kernel 是作为依赖导入的。让我看看 eagle_worker 中的 verify 流程：

> AGENT

现在看看 spec_info 的 verify 和 prepare_for_verify 方法：

> AGENT

现在查看 scheduler 中如何拿到 running batch 的 size 和是否可能在 forward 之前做某种开关：

> AGENT

现在检查是否有 fallback 或者禁用 spec 的路径：

> AGENT

现在看看 spec_info 中是否能动态调整参数或者有 disable 的方式：

> AGENT

现在查看 eagle_worker_v2 和 overlap 路径的差别：

> AGENT

现在查看如何在 eagle_worker.py 中传递和使用 dtn：

> AGENT

现在检查 CUDA graph 与 dtn 的关系：

> AGENT

现在查看 CUDA graph runner 的实现细节：

> AGENT

现在查看 target worker 的 forward_batch_generation 是否有 no-spec 的路径：

> AGENT

现在整理关键信息。让我再看一下 running_batch 何时被更新和它在多个地方的可见性：

> AGENT

现在让我检查 spec_info 中是否有 per-step 动态读取参数的机制：

> AGENT

完美。现在我有足够的信息来生成报告。让我最后检查一个关键细节——是否有任何已有的 per-batch 或 per-request 的 spec 参数覆盖机制：

> AGENT

现在我有足够信息了。让我整理完整的分析报告： --- ## 详细代码梳理：SGLang EAGLE-3 推测解码动态 BS 切换方案 ### 问题 1：Batch 调度入口 **Scheduler 决定 running batch 的关键位置：** - **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py` - **行 1097**：`event_loop_normal()` 调用 `batch = self.get_next_batch_to_run()` 获取当前 step 的 batch - **行 1133**：`event_loop_overlap()` 同样调用上述函数 - **行 1797-1873**：`get_next_batch_to_run()` 核心函数，负责返回下一个要执行的 ScheduleBatch 对象 **Running batch 的 size 可读位置：** - **行 1907, 1982, 2051, 2502, 2706**：均使用 `len(self.running_batch.reqs)` 获取当前 running batch 大小 - **行 740**：`self.running_batch` 初始化为 `ScheduleBatch(reqs=[], batch_is_full=False)`，是 scheduler 的成员变量 - **行 2236**：在 `enable_overlap` 模式下，`bs = len(model_worker_batch.seq_lens)` 也能获取 BS **spec v1 vs spec v2 overlap 入口差别：** - **行 2219-2225**：判断逻辑—— - `spec_algorithm.is_none() or enable_overlap` 时：使用 `batch.get_model_worker_batch()`（v2 overlap 路径） - 否则：直接传递 `batch` 本身（v1 非 overlap 路径） - **行 2258-2272**：若 `batch.is_spec_v2`，则进入 overlap 特殊处理，包括 `batch.spec_info = batch_result.next_draft_input` **结论**： - Running batch size 在 scheduler event loop 的 `get_next_batch_to_run()` 之后、`run_batch()` 之前可读 - 调用者需要通过 `len(self.running_batch.reqs)` 或 `batch.batch_size()` 获取 - 两条路径的分歧点在 `enable_overlap` 标志（由 `server_args.disable_overlap_schedule` 控制） --- ### 问题 2：EAGLE Worker 入口与 draft→verify 主循环 **EAGLEWorker v1 的核心入口：** - **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` - **行 351-406**：`forward_batch_generation(batch: ScheduleBatch) -> GenerationBatchResult` 主函数 - **行 363-378**：若为 `EXTEND` 模式，走 prefill 路径 - **行 380-406**：否则走 decode 主循环：`draft(batch)` → `verify(batch, spec_info)` → 返回结果 **Draft→Verify 主循环结构：** ``` forward_batch_generation(batch) ├─ 若 batch.forward_mode.is_extend(): forward_target_extend + forward_draft_extend └─ 否则（DECODE）: ├─ spec_info = draft(batch) [行 383] ├─ logits_output, verify_output, ... = verify(batch, spec_info) [行 384-385] └─ 若需要，forward_draft_extend_after_decode(batch) [行 398] ``` **spec_steps、topk、num_draft_tokens 的消费位置：** - **行 154-156**：在 `__init__` 时从 `server_args` 读取并存储为 self 属性： ```python self.topk = server_args.speculative_eagle_topk self.speculative_num_steps = server_args.speculative_num_steps self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens ``` - **行 647, 666**：在 `draft()` 函数中调用 `build_tree_kernel_efficient()` 时使用 - **行 710**：在 `EagleVerifyInput` 创建时传入 `draft_token_num=self.server_args.speculative_num_draft_tokens` - **行 783**：在 `organize_draft_results()` 中被消费用于重组 token **关键发现**：这些参数在 **worker init 时一次性读取**，之后每个 step 都使用同一份值。**不存在 step-level 的动态读取机制**。 **EAGLEWorkerV2（overlap 模式）的差别：** - **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py` - **行 616-658**：`forward_batch_generation(model_worker_batch)` 主函数 - 分为 EXTEND 和 DECODE 两路 - DECODE 路径：`draft(model_worker_batch)` → `verify(model_worker_batch)` → `_draft_extend_for_decode()` - 使用 `ModelWorkerBatch` 而非 `ScheduleBatch` --- ### 问题 3：CUDA Graph 与 Spec 形状绑定 **Draft model CUDA graph capture：** - **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` - **行 305-341**：`init_cuda_graphs()` 函数，调用 `EAGLEDraftCudaGraphRunner` 进行 capture - **行 318**：仅在 `self.speculative_num_steps > 1` 时才 capture draft graph - **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py` - **行 37-134**：`EAGLEDraftCudaGraphRunner.__init__()` 中进行 graph capture - **行 56-57**：存储 `self.speculative_num_steps` 和 `self.topk` - **行 65-74**： ```python self.capture_bs, self.compile_bs = get_batch_sizes_to_capture(model_runner) self.num_tokens_per_bs = self.topk # 关键！ self.max_bs = max(self.capture_bs) self.max_num_token = self.max_bs * self.num_tokens_per_bs # max_bs × topk ``` - **行 86-101**：分配 graph 输入 buffers，大小为： - `out_cache_loc`：`(max_num_token * speculative_num_steps,)` 【与 spec_steps 相关】 - `input_ids`：`(max_num_token,)` = `(max_bs * topk,)` - `seq_lens`, `topk_p`, `topk_index` 等 **Target model verify graph：** - Target model 的 graph 是在 target worker 侧 capture，不是在 EAGLE worker 侧 - Verify 不捕获独立的 cuda graph，而是依赖 target worker 自身的 graph […]
