> DEVELOPER

我们要在 SGLang fork 上实现"按 running batch size 动态切换推测解码模式"，需要你详细梳理代码：

**上下文**：
- 工作目录 `/user_4813494d/openbmb`，SGLang fork 在 `demo-sala/sglang/python/sglang/`
- 当前用 EAGLE-3 chain verify，启动脚本 `eval/start_eagle.sh`：`spec_steps=2, topk=2, dtn=5`
- 已落地 MARS verify（θ=0.85），改动在 `sgl-kernel/csrc/speculative/eagle_utils.cu` 和 `demo-sala/sglang/.../eagle_utils.py`
- `SGLANG_ENABLE_SPEC_V2=0` 当前关闭，使用 v1 路径（`eagle_worker.py`），v2 入口在 `eagle_worker_v2.py`

**目标方案**：
- bs > 32：整 batch 全部走 no-spec（关 EAGLE，普通 decode）
- 1 < bs ≤ 32：MARS tree，θ=0.85，topk=2，draft=2（dtn=5）
- bs = 1：MARS tree，θ=0.85，topk=2，draft=3（dtn=7）
- 关键约束：**全体样本切**，不是只对新样本。bs 增长穿过阈值时，正在运行的所有请求都要立即跟着切

**请回答以下问题**（按重要性排序，每个问题都要给具体文件+行号）：

1. **batch 调度入口**：scheduler 哪里决定一个 step 的 running batch（哪个文件、哪个函数）？running batch 的 size 在何处可读？例如 `scheduler.py` 的 event loop、`get_next_batch_to_run` 等。`spec v1` 和 `spec v2 overlap` 的入口有什么差别？

2. **EAGLE worker 入口**：`eagle_worker.py` 和 `eagle_worker_v2.py` 中 `forward_batch_generation` 或同类函数。draft → verify 的主循环是什么样？`spec_steps`、`topk`、`num_draft_tokens` 在哪里被消费？是 worker 初始化时就固定，还是每 step 可读？

3. **CUDA graph 与 spec 形状的绑定**：
   - draft model 的 graph capture 在哪里？是否对 `topk × spec_steps` 形状做了 capture？
   - target verify 的 graph 是否对 `dtn` 形状 capture？capture 的 batch size 列表是什么？
   - 如果运行时 dtn 在 5 ↔ 7 之间切换，graph 是否要重新 capture？SGLang 是否支持多 graph（按 dtn 分桶）？
   - `--cuda-graph-bs` 之类的参数怎么设置（看 `server_args.py`）？

4. **no-spec 切换可能性**：
   - 同一 worker 实例能否在 step-level 切换 "走 EAGLE" vs "走普通 decode"？看是否存在 fallback 路径（例如 spec 失败时回退）。
   - `forward_batch_generation` 是否 hard-coded 走 spec_info 路径？是否有 enable/disable spec 的开关？
   - 如果切到 no-spec，draft KV / verify state 怎么处理？是否需要 flush？

5. **dtn 动态调整**：
   - `speculative_num_steps` / `speculative_eagle_topk` / `speculative_num_draft_tokens` 在哪些数据结构中被持有？是 `ServerArgs` 一处常量，还是每个 batch 都重新读？
   - 如果不重启 server，是否能把 dtn 在 5 ↔ 7 之间切？draft tree 形状（mask、parent、position）怎么生成的？
   - 看一下 `eagle_utils.py` 里 build draft tree / decode_tree_mask 的逻辑

6. **现有钩子**：
   - `start_eagle.sh` 有 `EAGLE_FORCE_NO_ACCEPT` 环境变量，看它是怎么实现的（grep 一下），这是不是一个潜在的"批量绕过 spec"钩子？
   - `EAGLE_MARS_THETA` 怎么传到 verify kernel？是 step-level 读还是 worker init 时读？
   - 是否还有其他"per-step 动态参数"通道？

7. **scheduler 视角拿到 running bs**：
   - scheduler.py 的 event loop（v1 / v2 overlap 两条路径）在 forward 之前，是否已经把 running batch 准备好？bs 在哪个变量里？
   - 在 forward 之前能否调用 worker 上的"set spec mode"接口？

**输出格式**：
- 每个问题独立小节，给出关键代码段（带文件:行号）+ 简短结论
- 末尾给"切换可行性快评"，明确指出哪些可做、哪些是大坑（例如：CUDA graph 必须重 capture 是否成立？dtn 切换会不会破坏 draft 内部 buffer？spec → no-spec 转换时正在 verify 的请求怎么处理？）

不要给实现代码，只做调研。预算 thorough。

> AGENT

我来详细梳理 SGLang fork 中关于推测解码的代码架构。这是一个复杂的系统，我会按照问题顺序逐一深入调查。

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"scheduler.py\" -o -name \"eagle_worker.py\" -o -name \"eagle_worker_v2.py\" -o -name \"server_args.py\" | grep -E \"(sglang|demo)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/server_args.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/multimodal_gen/runtime/server_args.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/managers/scheduler.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/multimodal_gen/runtime/server_args.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/multimodal_gen/runtime/managers/scheduler.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/multimodal_gen/runtime/managers/scheduler.py
```

> AGENT

让我重点看 demo-sala 这条线，因为题目明确指向它：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# Copyright 2023-2024 SGLang Team
2	# Licensed under the Apache License, Version 2.0 (the "License");
3	# you may not use this file except in compliance with the License.
4	# You may obtain a copy of the License at
5	#
6	#     http://www.apache.org/licenses/LICENSE-2.0
7	#
8	# Unless required by applicable law or agreed to in writing, software
9	# distributed under the License is distributed on an "AS IS" BASIS,
10	# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
11	# See the License for the specific language governing permissions and
12	# limitations under the License.
13	# ==============================================================================
14	"""A scheduler that manages a tensor parallel GPU worker."""
15	
16	import faulthandler
17	import logging
18	import os
19	import signal
20	import sys
21	import time
22	from collections import deque
23	from concurrent import futures
24	from contextlib import nullcontext
25	from dataclasses import dataclass
26	from http import HTTPStatus
27	from typing import Any, Deque, Dict, List, Optional, Tuple, Union
28	
29	import psutil
30	import setproctitle
31	import torch
32	import torch.distributed
33	import zmq
34	from torch.cuda import Stream as CudaStream
35	from torch.cuda import StreamContext as CudaStreamContext
36	from torch.distributed import barrier
37	
38	from sglang.srt.configs.model_config import ModelConfig
39	from sglang.srt.constrained.base_grammar_backend import (
40	    INVALID_GRAMMAR_OBJ,
41	    create_grammar_backend,
42	)
43	from sglang.srt.disaggregation.decode import (
44	    DecodePreallocQueue,
45	    DecodeTransferQueue,
46	    SchedulerDisaggregationDecodeMixin,
47	)
48	from sglang.srt.disaggregation.decode_kvcache_offload_manager import (
49	    DecodeKVCacheOffloadManager,
50	)
51	from sglang.srt.disaggregation.encode_receiver import MMReceiver
52	from sglang.srt.disaggregation.prefill import (
53	    PrefillBootstrapQueue,
54	    SchedulerDisaggregationPrefillMixin,
55	)
56	from sglang.srt.disaggregation.utils import (
57	    DisaggregationMode,
58	    MetadataBuffers,
59	    ReqToMetadataIdxAllocator,
60	    TransferBackend,
61	    prepare_abort,
62	)
63	from sglang.srt.distributed import get_pp_group, get_world_group
64	from sglang.srt.dllm.config import DllmConfig
65	from sglang.srt.environ import envs
66	from sglang.srt.eplb.expert_distribution import get_global_expert_distribution_recorder
67	from sglang.srt.layers.dp_attention import compute_dp_attention_world_info
68	from sglang.srt.layers.moe import initialize_moe_config
69	from sglang.srt.layers.quantization.fp8_utils import initialize_fp8_gemm_config
70	from sglang.srt.managers.io_struct import (
71	    AbortReq,
72	    BaseBatchReq,
73	    BaseReq,
74	    BatchTokenizedEmbeddingReqInput,
75	    BatchTokenizedGenerateReqInput,
76	    CheckWeightsReqInput,
77	    ClearHiCacheReqInput,
78	    ClearHiCacheReqOutput,
79	    CloseSessionReqInput,
80	    ContinueGenerationReqInput,
81	    DestroyWeightsUpdateGroupReqInput,
82	    ExpertDistributionReq,
83	    ExpertDistributionReqOutput,
84	    ExpertDistributionReqType,
85	    FlushCacheReqInput,
86	    FlushCacheReqOutput,
87	    FreezeGCReq,
88	    GetInternalStateReq,
89	    GetInternalStateReqOutput,
90	    GetLoadReqInput,
91	    GetWeightsByNameReqInput,
92	    HealthCheckOutput,
93	    InitWeightsSendGroupForRemoteInstanceReqInput,
94	    InitWeightsSendGroupForRemoteInstanceReqOutput,
95	    InitWeightsUpdateGroupReqInput,
96	    LoadLoRAAdapterReqInput,
97	    LoadLoRAAdapterReqOutput,
98	    OpenSessionReqInput,
99	    OpenSessionReqOutput,
100	    PauseGenerationReqInput,

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

继续看 scheduler 的核心循环：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"event_loop\\|forward_batch_generation\\|get_next_batch_to_run\\|def step\\|running_batch_size\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -40"
}
```

> TOOL

tool_result Bash
```
1087:    def event_loop_normal(self):
1097:            batch = self.get_next_batch_to_run()
1114:    def event_loop_overlap(self):
1133:            batch = self.get_next_batch_to_run()
1797:    def get_next_batch_to_run(self) -> Optional[ScheduleBatch]:
2243:                        batch_result = self.model_worker.forward_batch_generation(
2247:                    # FIXME(lsyin): maybe move this to forward_batch_generation
2283:                    batch_result = self.model_worker.forward_batch_generation(
2338:        # unifying the forward_batch_generation interface (related to spec V2).
2970:                scheduler.event_loop_pdmux()
2972:                scheduler.event_loop_pp()
2974:                scheduler.event_loop_overlap()
2976:                scheduler.event_loop_normal()
2979:                scheduler.event_loop_pp_disagg_prefill()
2981:                scheduler.event_loop_overlap_disagg_prefill()
2983:                scheduler.event_loop_normal_disagg_prefill()
2987:                scheduler.event_loop_pp_disagg_decode()
2989:                scheduler.event_loop_overlap_disagg_decode()
2991:                scheduler.event_loop_normal_disagg_decode()
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py",
  "offset": 1087,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1087	    def event_loop_normal(self):
1088	        """A normal scheduler loop."""
1089	        while True:
1090	            # Receive requests
1091	            recv_reqs = self.recv_requests()
1092	            self.process_input_requests(recv_reqs)
1093	            if self._engine_paused:
1094	                continue
1095	
1096	            # Get the next batch to run
1097	            batch = self.get_next_batch_to_run()
1098	            self.cur_batch = batch
1099	
1100	            # Launch the current batch
1101	            if batch:
1102	                result = self.run_batch(batch)
1103	                self.process_batch_result(batch, result)
1104	            else:
1105	                # When the server is idle, do self-check and re-init some states
1106	                self.self_check_during_idle()
1107	
1108	            # Update last_batch
1109	            self.last_batch = batch
1110	            if envs.SGLANG_ENABLE_STRICT_MEM_CHECK_DURING_BUSY.get():
1111	                self.self_check_during_busy()
1112	
1113	    @DynamicGradMode()
1114	    def event_loop_overlap(self):
1115	        """A scheduler loop that overlaps the CPU processing and GPU computation."""
1116	        self.result_queue: Deque[
1117	            Tuple[ScheduleBatch, Union[GenerationBatchResult, EmbeddingBatchResult]]
1118	        ] = deque()
1119	
1120	        def pop_and_process():
1121	            # Process the results of the last batch
1122	            tmp_batch, tmp_result = self.result_queue.popleft()
1123	            self.process_batch_result(tmp_batch, tmp_result)
1124	
1125	        while True:
1126	            # Receive requests
1127	            recv_reqs = self.recv_requests()
1128	            self.process_input_requests(recv_reqs)
1129	            if self._engine_paused:
1130	                continue
1131	
1132	            # Get the next batch to run
1133	            batch = self.get_next_batch_to_run()
1134	            self.cur_batch = batch
1135	            disable_overlap_for_batch = self.is_disable_overlap_for_batch(batch)
1136	
1137	            # If we do not need to overlap the current batch with the last batch,
1138	            # we can process the last batch immediately.
1139	            if disable_overlap_for_batch:
1140	                pop_and_process()
1141	
1142	            # Launch the current batch
1143	            if batch:
1144	                batch_result = self.run_batch(batch)
1145	                self.result_queue.append((batch.copy(), batch_result))
1146	            else:
1147	                batch_result = None
1148	
1149	            # Process the last batch
1150	            if self.last_batch:
1151	                if not disable_overlap_for_batch:
1152	                    pop_and_process()
1153	            elif batch is None:
1154	                # When the server is idle, do self-check and re-init some states
1155	                self.self_check_during_idle()
1156	
1157	            # Run sample of the current batch
1158	            # It depends on the result of the last batch (e.g., grammar), so we run it after the last batch is processed.
1159	            if self.is_generation:
1160	                self.launch_batch_sample_if_needed(batch_result)
1161	
1162	            # Update last_batch
1163	            self.last_batch = batch
1164	            if envs.SGLANG_ENABLE_STRICT_MEM_CHECK_DURING_BUSY.get():
1165	                self.self_check_during_busy()
1166	
1167	    def is_disable_overlap_for_batch(self, batch: ScheduleBatch) -> bool:
1168	        # For two consecutive prefill batches, we disable overlap to improve the TTFT of the first batch.
1169	        # This might slightly hurt the throughput, so we use an environment variable to control it.
1170	        disable_overlap_for_batch = (
1171	            envs.SGLANG_DISABLE_CONSECUTIVE_PREFILL_OVERLAP.get()
1172	            and batch
1173	            and batch.forward_mode.is_extend()
1174	            and self.last_batch
1175	            and self.last_batch.forward_mode.is_extend()
1176	        )
1177	
1178	        # We do not support overlap + spec + grammar yet,
1179	        # so we need to turn off overlap for this batch.
1180	        # TODO(lsyin): support overlap + spec + grammar
1181	        need_grammar_sync = (
1182	            batch
1183	            and batch.is_spec_v2
1184	            and batch.has_grammar
1185	            and batch.forward_mode.is_decode()
1186	            and len(self.result_queue) > 0

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py",
  "offset": 1797,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1797	    def get_next_batch_to_run(self) -> Optional[ScheduleBatch]:
1798	        if self.dllm_config is not None:
1799	            if self.chunked_req is not None and self.chunked_req.finished():
1800	                self.chunked_req = None
1801	
1802	        # Merge the prefill batch into the running batch
1803	        chunked_req_to_exclude = set()
1804	        if self.chunked_req:
1805	            # Move the chunked request out of the batch so that we can merge
1806	            # only finished requests to running_batch.
1807	            chunked_req_to_exclude.add(self.chunked_req)
1808	            self.tree_cache.cache_unfinished_req(self.chunked_req, chunked=True)
1809	
1810	            # chunked request keeps its rid but will get a new req_pool_idx
1811	            if self.tp_worker.model_runner.mambaish_config is not None:
1812	                self.req_to_token_pool.free(
1813	                    self.chunked_req.req_pool_idx, free_mamba_cache=False
1814	                )
1815	            else:
1816	                self.req_to_token_pool.free(self.chunked_req.req_pool_idx)
1817	
1818	        if self.last_batch and self.last_batch.forward_mode.is_extend():
1819	            if self.last_batch.chunked_req is not None:
1820	                # In the context pipeline parallelism, after the last chunk, the current microbatch still track outdated chunked_req.
1821	                # We need to discard it.
1822	                chunked_req_to_exclude.add(self.last_batch.chunked_req)
1823	
1824	            # Filter batch
1825	            last_bs = self.last_batch.batch_size()
1826	            self.last_batch.filter_batch(
1827	                chunked_req_to_exclude=list(chunked_req_to_exclude)
1828	            )
1829	            if self.last_batch.batch_size() < last_bs:
1830	                self.running_batch.batch_is_full = False
1831	
1832	            # Merge the new batch into the running batch.
1833	            # For prefill-only batch, we can avoid going through decoding step.
1834	            if not self.last_batch.is_empty() and not self.last_batch.is_prefill_only:
1835	                if self.running_batch.is_empty():
1836	                    self.running_batch = self.last_batch
1837	                else:
1838	                    # Merge running_batch with prefill batch
1839	                    self.running_batch.merge_batch(self.last_batch)
1840	
1841	        new_batch = self.get_new_batch_prefill()
1842	
1843	        need_mlp_sync = self.require_mlp_sync
1844	        if need_mlp_sync and not self.spec_algorithm.is_none():
1845	            # NOTE: This branch makes sure prefill and decode batches will not be mixed when spec and dp-attn is enabled.
1846	            # Before merging the new batch into running batch:
1847	            # 1. All new batches are none -> need_mlp_sync remains true (sync is needed for decode batch).
1848	            # 2. All new batches are some (prefill / idle) -> we do not need prepare mlp sync one more time.
1849	            new_batch = self.maybe_prepare_mlp_sync_batch_and_log_stats(
1850	                new_batch, log_stats=False
1851	            )
1852	            need_mlp_sync = new_batch is None
1853	
1854	        if new_batch is not None:
1855	            # Run prefill first if possible
1856	            ret = new_batch
1857	        else:
1858	            # Run decode
1859	            if not self.running_batch.is_empty():
1860	                self.running_batch = self.update_running_batch(self.running_batch)
1861	                ret = self.running_batch if not self.running_batch.is_empty() else None
1862	            else:
1863	                ret = None
1864	
1865	        # Handle DP attention and log stats
1866	        ret = self.maybe_prepare_mlp_sync_batch_and_log_stats(
1867	            ret, need_sync=need_mlp_sync
1868	        )
1869	
1870	        if ret:
1871	            trace_event_batch("schedule", ret.reqs)
1872	
1873	        return ret
1874	
1875	    def get_num_allocatable_reqs(self, running_bs):
1876	        res = get_global_server_args().pp_max_micro_batch_size - running_bs

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看 run_batch 以及 forward_batch_generation：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def run_batch\\|forward_batch_generation\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -20"
}
```

> TOOL

tool_result Bash
```
2193:    def run_batch(
2243:                        batch_result = self.model_worker.forward_batch_generation(
2247:                    # FIXME(lsyin): maybe move this to forward_batch_generation
2283:                    batch_result = self.model_worker.forward_batch_generation(
2338:        # unifying the forward_batch_generation interface (related to spec V2).
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py",
  "offset": 2193,
  "limit": 120
}
```

> TOOL

tool_result Read
```
2193	    def run_batch(
2194	        self,
2195	        batch: ScheduleBatch,
2196	        pp_proxy_tensors: Optional[PPProxyTensors] = None,
2197	    ) -> Union[GenerationBatchResult, EmbeddingBatchResult]:
2198	        """Run a batch."""
2199	        self.forward_ct += 1
2200	
2201	        # Whether to run the profiler
2202	        self._profile_batch_predicate(batch)
2203	        if self.forward_sleep_time is not None:
2204	            logger.info(f"Scheduler.run_batch sleep {self.forward_sleep_time}s")
2205	            time.sleep(self.forward_sleep_time)
2206	
2207	        # Capture prefill start time for EXTEND mode
2208	        if batch.forward_mode == ForwardMode.EXTEND:
2209	            current_time = time.perf_counter()
2210	            for req in batch.reqs:
2211	                req.time_stats.prefill_start_time_host = current_time
2212	
2213	        # Place holder handling for pd-disagg decode event loop
2214	        if batch.forward_mode.is_prebuilt():
2215	            return self._run_batch_prebuilt(batch)
2216	
2217	        # Run forward
2218	        if self.is_generation:
2219	            if self.spec_algorithm.is_none() or self.enable_overlap:
2220	                # In most cases, we use the model worker batch to run the forward.
2221	                worker_batch_or_batch = batch.get_model_worker_batch()
2222	            else:
2223	                # In speculative decoding v1 (non-overlap) case, we use the batch directly.
2224	                # TODO(lsyin): delete this branch after unifying the abstraction.
2225	                worker_batch_or_batch = batch
2226	
2227	            if self.enable_overlap:
2228	                model_worker_batch = worker_batch_or_batch
2229	                self.record_batch_in_overlap(model_worker_batch)
2230	
2231	                # Sampling info will be modified during forward, so we store a copy.
2232	                model_worker_batch.sampling_info = (
2233	                    model_worker_batch.sampling_info.copy_for_forward()
2234	                )
2235	
2236	                bs = len(model_worker_batch.seq_lens)
2237	                future_indices = self.future_map.alloc_future_indices(bs)
2238	
2239	                with self.forward_stream_ctx:
2240	                    self.forward_stream.wait_stream(self.default_stream)
2241	                    self.future_map.resolve_future(model_worker_batch)
2242	                    with self.record_forward_metrics(batch):
2243	                        batch_result = self.model_worker.forward_batch_generation(
2244	                            model_worker_batch
2245	                            # here pp is not compatible with overlap
2246	                        )
2247	                    # FIXME(lsyin): maybe move this to forward_batch_generation
2248	                    batch_result.copy_done = self.device_module.Event()
2249	                    if batch_result.delay_sample_func is None:
2250	                        self.future_map.store_to_map(future_indices, batch_result)
2251	                        batch_result.copy_to_cpu(return_logprob=batch.return_logprob)
2252	                    else:
2253	                        batch_result.future_indices = future_indices
2254	
2255	                # FIXME(lsyin): move this assignment elsewhere
2256	                future_indices_or_next_token_ids = -future_indices.indices
2257	
2258	                if batch.is_spec_v2:
2259	                    # FIXME(lsyin): tmp code for spec v2
2260	                    # We only keep future indices for next draft input
2261	
2262	                    batch.spec_info = batch_result.next_draft_input
2263	                    batch.spec_info.future_indices = future_indices
2264	
2265	                    # batch.spec_info = EagleDraftInput(
2266	                    #     future_indices=future_indices,
2267	                    #     verify_done=batch_result.next_draft_input.verify_done,
2268	                    # )
2269	
2270	                    # The future value, usually for next batch preparation
2271	                    # Current implementation strictly synchronizes the seq_lens
2272	                    batch.seq_lens = batch_result.next_draft_input.new_seq_lens
2273	            elif self.enable_pdmux and batch.forward_mode.is_split_prefill():
2274	                batch_result = self.tp_worker.forward_batch_split_prefill(batch)
2275	                future_indices_or_next_token_ids = batch_result.next_token_ids
2276	            else:
2277	                kwargs = (
2278	                    {"pp_proxy_tensors": pp_proxy_tensors}
2279	                    if self.spec_algorithm.is_none()
2280	                    else {}
2281	                )
2282	                with self.record_forward_metrics(batch):
2283	                    batch_result = self.model_worker.forward_batch_generation(
2284	                        worker_batch_or_batch, **kwargs
2285	                    )
2286	                future_indices_or_next_token_ids = batch_result.next_token_ids
2287	                self.update_cache_from_scheduler(batch, batch_result)
2288	
2289	            # NOTE: future_indices_or_next_token_ids is used in ScheduleBatch,
2290	            #       which can probably be replaced by future_indices later [TODO(lsyin)].
2291	            #       we shall still keep the original outputs, e.g. next_token_ids
2292	            #       in the GenerationBatchOutput for processing after copy_done.
2293	            batch.output_ids = future_indices_or_next_token_ids
2294	
2295	            # These 2 values are needed for processing the output, but the values can be
2296	            # modified by overlap schedule. So we have to copy them here so that
2297	            # we can use the correct values in output processing.
2298	            if batch.return_logprob:
2299	                batch_result.extend_input_len_per_req = [
2300	                    req.extend_input_len for req in batch.reqs
2301	                ]
2302	                batch_result.extend_logprob_start_len_per_req = [
2303	                    req.extend_logprob_start_len for req in batch.reqs
2304	                ]
2305	            else:
2306	                batch_result.extend_input_len_per_req = None
2307	                batch_result.extend_logprob_start_len_per_req = None
2308	
2309	            ret = batch_result
2310	        else:  # embedding or reward model
2311	            model_worker_batch = batch.get_model_worker_batch()
2312	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看 ScheduleBatch 中的 batch_size() 方法和 running_batch 如何被持有：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"self.running_batch\\|class ScheduleBatch\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -30"
}
```

> TOOL

tool_result Bash
```
740:        self.running_batch: ScheduleBatch = ScheduleBatch(reqs=[], batch_is_full=False)
1330:                or not self.running_batch.is_empty()
1830:                self.running_batch.batch_is_full = False
1835:                if self.running_batch.is_empty():
1836:                    self.running_batch = self.last_batch
1839:                    self.running_batch.merge_batch(self.last_batch)
1859:            if not self.running_batch.is_empty():
1860:                self.running_batch = self.update_running_batch(self.running_batch)
1861:                ret = self.running_batch if not self.running_batch.is_empty() else None
1900:            self.running_batch.batch_is_full = False
1903:            self.running_batch.batch_is_full or len(self.waiting_queue) == 0
1907:        running_bs = len(self.running_batch.reqs)
1918:            self.running_batch.batch_is_full = True
1946:            self.running_batch,
1961:            lora_set = set([req.lora_id for req in self.running_batch.reqs])
1982:            running_bs = len(self.running_batch.reqs)
1984:                self.running_batch.batch_is_full = True
1989:                    self.running_batch.batch_is_full = True
1991:            if self.running_batch.batch_is_full:
2014:                        self.running_batch.batch_is_full = len(
2016:                        ) > 0 or (not self.running_batch.is_empty())
2018:                        self.running_batch.batch_is_full = True
2051:                running_bs=len(self.running_batch.reqs),
2087:            and not self.running_batch.is_empty()
2088:            and not (new_batch.return_logprob or self.running_batch.return_logprob)
2091:            self.running_batch.filter_batch(v1_spec_info_filtered=True)
2092:            if not self.running_batch.is_empty():
2093:                self.running_batch.prepare_for_decode()
2094:                new_batch.mix_with_running(self.running_batch)
2095:                new_batch.decoding_reqs = self.running_batch.reqs
```

> AGENT

找 ScheduleBatch 定义：

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala -name \"*.py\" -exec grep -l \"class ScheduleBatch\" {} \\;"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/disaggregation/decode_schedule_batch_mixin.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def batch_size\\|class ScheduleBatch\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py | head -20"
}
```

> TOOL

tool_result Bash
```
1170:class ScheduleBatch(ScheduleBatchDisaggregationDecodeMixin):
1371:    def batch_size(self):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py",
  "offset": 1371,
  "limit": 10
}
```

> TOOL

tool_result Read
```
1371	    def batch_size(self):
1372	        return len(self.reqs)
1373	
1374	    def is_empty(self):
1375	        return len(self.reqs) == 0
1376	
1377	    def is_dllm(self):
1378	        return self.dllm_config is not None
1379	
1380	    def prepare_encoder_info_extend(self, input_ids: List[int], seq_lens: List[int]):

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看 eagle_worker.py 和 v2 的详情：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	import logging
2	import time
3	from copy import copy
4	from typing import List, Optional, Tuple
5	
6	import torch
7	
8	from sglang.srt.distributed import get_tp_group
9	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
10	    EAGLEDraftNpuGraphRunner,
11	)
12	from sglang.srt.layers.dp_attention import get_attention_tp_group
13	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
14	from sglang.srt.layers.moe.utils import (
15	    speculative_moe_a2a_backend_context,
16	    speculative_moe_backend_context,
17	)
18	from sglang.srt.layers.utils.logprob import add_output_logprobs_for_spec_v1
19	from sglang.srt.managers.io_struct import UpdateWeightsFromTensorReqInput
20	from sglang.srt.managers.schedule_batch import ScheduleBatch
21	from sglang.srt.managers.scheduler import GenerationBatchResult
22	from sglang.srt.managers.tp_worker import TpModelWorker
23	from sglang.srt.mem_cache.chunk_cache import SWAChunkCache
24	from sglang.srt.mem_cache.common import (
25	    alloc_paged_token_slots_extend,
26	    alloc_token_slots,
27	    get_last_loc,
28	)
29	from sglang.srt.model_executor.forward_batch_info import (
30	    CaptureHiddenMode,
31	    ForwardBatch,
32	    ForwardMode,
33	)
34	from sglang.srt.server_args import ServerArgs
35	from sglang.srt.speculative.draft_utils import DraftBackendFactory
36	from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
37	    EAGLEDraftCudaGraphRunner,
38	)
39	from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
40	    EAGLEDraftExtendCudaGraphRunner,
41	)
42	from sglang.srt.speculative.eagle_info import (
43	    _EAGLE_TRACE_PATH,
44	    _eagle_trace_emit,
45	    EagleDraftInput,
46	    EagleVerifyInput,
47	    EagleVerifyOutput,
48	)
49	from sglang.srt.speculative.eagle_utils import (
50	    build_tree_kernel_efficient,
51	    organize_draft_results,
52	)
53	from sglang.srt.speculative.spec_info import SpeculativeAlgorithm
54	from sglang.srt.speculative.spec_utils import (
55	    assign_draft_cache_locs,
56	    detect_nan,
57	    draft_tp_context,
58	    fast_topk,
59	    generate_token_bitmask,
60	    get_last_loc_large_page_size_large_top_k,
61	    load_token_map,
62	    select_top_k_tokens,
63	)
64	from sglang.srt.sampling.sampling_batch_info import SamplingBatchInfo
65	from sglang.srt.utils import (
66	    MultiprocessingSerializer,
67	    empty_context,
68	    get_available_gpu_memory,
69	    is_cuda,
70	    is_npu,
71	    next_power_of_2,
72	)
73	from sglang.srt.utils.patch_torch import monkey_patch_torch_reductions
74	
75	_is_npu = is_npu()
76	
77	if is_cuda():
78	    from sgl_kernel import segment_packbits  # noqa: F401
79	
80	logger = logging.getLogger(__name__)
81	
82	
83	def _detect_draft_model_quantization(
84	    draft_model_path: Optional[str],
85	    default_quant: Optional[str],
86	) -> Optional[str]:
87	    """Return the quantization scheme to use for the EAGLE-3 draft model.
88	
89	    Detection order:
90	    1. hf_quant_config.json: {"quantization": {"quant_algo": "NVFP4", ...}}
91	       — written by convert_to_sglang.py; presence means pre-quantized NVFP4.
92	    2. config.json quantization_config.quant_algo = "NVFP4" (legacy flat format).
93	    3. config.json quantization_config.quant_type in ("nvfp4", "modelopt_fp4")
94	       (original format before fix).
95	
96	    Returns "modelopt_fp4" if NVFP4 detected, else None (BF16 legacy mode).
97	    """
98	    if draft_model_path is None:
99	        return None
100	    import json, os
101	
102	    # ── 1. hf_quant_config.json (primary, written by convert_to_sglang.py) ──
103	    hf_quant_path = os.path.join(draft_model_path, "hf_quant_config.json")
104	    if os.path.exists(hf_quant_path):
105	        try:
106	            with open(hf_quant_path) as f:
107	                hf_cfg = json.load(f)
108	            quant_algo = hf_cfg.get("quantization", {}).get("quant_algo", "").upper()
109	            if "NVFP4" in quant_algo or "FP4" in quant_algo:
110	                logger.info(
111	                    "Draft model at %s has hf_quant_config.json with %s — "
112	                    "enabling modelopt_fp4 (Marlin W4A16)",
113	                    draft_model_path, quant_algo,
114	                )
115	                return "modelopt_fp4"
116	        except Exception:
117	            pass
118	
119	    # ── 2/3. config.json quantization_config (fallback) ────────────────────
120	    config_path = os.path.join(draft_model_path, "config.json")
121	    if not os.path.exists(config_path):
122	        return None
123	    try:
124	        with open(config_path) as f:
125	            cfg = json.load(f)
126	        qcfg = cfg.get("quantization_config", {})
127	        quant_algo = qcfg.get("quant_algo", "").upper()
128	        quant_type = qcfg.get("quant_type", "").lower()
129	        if "NVFP4" in quant_algo or "FP4" in quant_algo or quant_type in ("nvfp4", "modelopt_fp4"):
130	            logger.info(
131	                "Draft model at %s has NVFP4 in config.json — enabling modelopt_fp4",
132	                draft_model_path,
133	            )
134	            return "modelopt_fp4"
135	    except Exception:
136	        pass
137	    return None
138	
139	
140	class EAGLEWorker(TpModelWorker):
141	
142	    def __init__(
143	        self,
144	        server_args: ServerArgs,
145	        gpu_id: int,
146	        tp_rank: int,
147	        dp_rank: Optional[int],
148	        moe_ep_rank: int,
149	        nccl_port: int,
150	        target_worker: TpModelWorker,

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def forward_batch_generation\\|def __init__\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -30"
}
```

> TOOL

tool_result Bash
```
142:    def __init__(
351:    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 142,
  "limit": 200
}
```

> TOOL

tool_result Read
```
142	    def __init__(
143	        self,
144	        server_args: ServerArgs,
145	        gpu_id: int,
146	        tp_rank: int,
147	        dp_rank: Optional[int],
148	        moe_ep_rank: int,
149	        nccl_port: int,
150	        target_worker: TpModelWorker,
151	    ):
152	        # Parse arguments
153	        self.server_args = server_args
154	        self.topk = server_args.speculative_eagle_topk
155	        self.speculative_num_steps = server_args.speculative_num_steps
156	        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
157	        self.enable_nan_detection = server_args.enable_nan_detection
158	        self.gpu_id = gpu_id
159	        self.device = server_args.device
160	        self.target_worker = target_worker
161	        self.page_size = server_args.page_size
162	        self.speculative_algorithm = SpeculativeAlgorithm.from_string(
163	            server_args.speculative_algorithm
164	        )
165	
166	        # Override the context length of the draft model to be the same as the target model.
167	        server_args.context_length = target_worker.model_runner.model_config.context_len
168	
169	        # Do not capture cuda graph in `super().__init__()`
170	        # It will be captured later.
171	        backup_disable_cuda_graph = server_args.disable_cuda_graph
172	        server_args.disable_cuda_graph = True
173	        # Determine draft model quantization.
174	        # If the draft model's config.json has quantization_config.quant_type="nvfp4",
175	        # it was trained with FP4_QAT and packed in NVFP4 format — keep modelopt_fp4.
176	        # Otherwise use None (BF16 mode, legacy behaviour).
177	        backup_draft_quant = server_args.speculative_draft_model_quantization
178	        draft_model_path = server_args.speculative_draft_model_path
179	        draft_quant = _detect_draft_model_quantization(draft_model_path, backup_draft_quant)
180	        server_args.speculative_draft_model_quantization = draft_quant
181	        # Draft model (Llama architecture) should use standard flashinfer, not minicpm_flashinfer
182	        backup_draft_attn = server_args.speculative_draft_attention_backend
183	        if (
184	            server_args.attention_backend == "minicpm_flashinfer"
185	            and backup_draft_attn in (None, "minicpm_flashinfer")
186	        ):
187	            server_args.speculative_draft_attention_backend = "flashinfer"
188	        # Share the allocator with a target worker.
189	        # Draft and target worker own their own KV cache pools.
190	        self.req_to_token_pool, self.token_to_kv_pool_allocator = (
191	            target_worker.get_memory_pool()
192	        )
193	
194	        # Load hot token ids
195	        if self.speculative_algorithm.is_eagle3():
196	            if server_args.speculative_token_map is not None:
197	                logger.warning(
198	                    "Speculative token map specified, but EAGLE3 models already have this. Ignoring the specified token map."
199	                )
200	            self.hot_token_id = None
201	        elif server_args.speculative_token_map is not None:
202	            self.hot_token_id = load_token_map(server_args.speculative_token_map)
203	            server_args.json_model_override_args = (
204	                f'{{"hot_vocab_size": {len(self.hot_token_id)}}}'
205	            )
206	        else:
207	            self.hot_token_id = None
208	
209	        # Init draft worker
210	        if server_args.enable_dp_attention and self.speculative_algorithm.is_eagle3():
211	            ctx = draft_tp_context(get_attention_tp_group())
212	        else:
213	            ctx = empty_context()
214	        with (
215	            ctx
216	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
217	            super().__init__(
218	                server_args=server_args,
219	                gpu_id=gpu_id,
220	                tp_rank=tp_rank,
221	                pp_rank=0,  # FIXME
222	                dp_rank=dp_rank,
223	                moe_ep_rank=moe_ep_rank,
224	                nccl_port=nccl_port,
225	                is_draft_worker=True,
226	                req_to_token_pool=self.req_to_token_pool,
227	                token_to_kv_pool_allocator=self.token_to_kv_pool_allocator,
228	            )
229	
230	        embed, head = self.target_worker.model_runner.model.get_embed_and_head()
231	
232	        if self.speculative_algorithm.is_eagle3():
233	            # most cases EAGLE3 models don't share lm_head
234	            # but some models (e.g. nvidia/gpt-oss-120b-Eagle3) shares
235	            if (
236	                hasattr(self.draft_model_runner.model, "load_lm_head_from_target")
237	                and self.draft_model_runner.model.load_lm_head_from_target
238	            ):
239	                self.draft_model_runner.model.set_embed_and_head(embed, head)
240	            else:
241	                self.draft_model_runner.model.set_embed(embed)
242	
243	            # grab hot token ids
244	            if self.draft_model_runner.model.hot_token_id is not None:
245	                self.hot_token_id = self.draft_model_runner.model.hot_token_id.to(
246	                    embed.device
247	                )
248	
249	        else:
250	            if self.hot_token_id is not None:
251	                head = head.clone()
252	                self.hot_token_id = self.hot_token_id.to(head.device)
253	                head.data = head.data[self.hot_token_id]
254	
255	            # Share the embedding and lm_head
256	            self.draft_model_runner.model.set_embed_and_head(embed, head)
257	
258	        # Init attention backend and cuda graphs
259	        self.draft_model_runner.server_args.disable_cuda_graph = (
260	            backup_disable_cuda_graph
261	        )
262	        self.draft_tp_context = (
263	            draft_tp_context if server_args.enable_dp_attention else empty_context
264	        )
265	        self.eagle_use_aux_hidden_state = False
266	        if self.speculative_algorithm.is_eagle3():
267	            self.eagle_use_aux_hidden_state = True
268	            eagle_config = getattr(
269	                self.draft_model_runner.model_config.hf_config, "eagle_config", {}
270	            )
271	            self.eagle_use_aux_hidden_state = eagle_config.get(
272	                "use_aux_hidden_state", True
273	            )
274	        with self.draft_tp_context(
275	            self.draft_model_runner.tp_group
276	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
277	            self.init_attention_backend()
278	            self.init_cuda_graphs()
279	
280	        # Some dummy tensors
281	        self.num_new_pages_per_topk = torch.empty(
282	            (), dtype=torch.int64, device=self.device
283	        )
284	        self.extend_lens = torch.empty((), dtype=torch.int64, device=self.device)
285	
286	    def init_attention_backend(self):
287	        # Create multi-step attn backends and cuda graph runners
288	        draft_backend_factory = DraftBackendFactory(
289	            self.server_args,
290	            self.draft_model_runner,
291	            self.topk,
292	            self.speculative_num_steps,
293	        )
294	
295	        # Initialize decode attention backend
296	        self.draft_attn_backend = draft_backend_factory.create_decode_backend()
297	
298	        # Initialize draft extend attention backend (respects speculative_attention_mode setting)
299	        self.draft_extend_attn_backend = (
300	            draft_backend_factory.create_draft_extend_backend()
301	        )
302	
303	        self.draft_model_runner.draft_attn_backend = self.draft_attn_backend
304	
305	    def init_cuda_graphs(self):
306	        """Capture cuda graphs."""
307	        self.cuda_graph_runner = None
308	        self.cuda_graph_runner_for_draft_extend = None
309	
310	        if self.server_args.disable_cuda_graph:
311	            return
312	
313	        Device2DraftCudaGraphRunner = {
314	            "npu": EAGLEDraftNpuGraphRunner,
315	            "cuda": EAGLEDraftCudaGraphRunner,
316	        }
317	        # Capture draft
318	        if self.speculative_num_steps > 1:
319	            tic = time.perf_counter()
320	            before_mem = get_available_gpu_memory(self.device, self.gpu_id)
321	            logger.info(
322	                f"Capture draft cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
323	            )
324	            self.cuda_graph_runner = Device2DraftCudaGraphRunner[
325	                self.target_worker.device
326	            ](self)
327	            after_mem = get_available_gpu_memory(self.device, self.gpu_id)
328	            logger.info(
329	                f"Capture draft cuda graph end. Time elapsed: {time.perf_counter() - tic:.2f} s. mem usage={(before_mem - after_mem):.2f} GB. avail mem={after_mem:.2f} GB."
330	            )
331	
332	        # Capture extend
333	        if self.draft_extend_attn_backend and not _is_npu:
334	            tic = time.perf_counter()
335	            before_mem = get_available_gpu_memory(self.device, self.gpu_id)
336	            logger.info(
337	                f"Capture draft extend cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
338	            )
339	            self.cuda_graph_runner_for_draft_extend = EAGLEDraftExtendCudaGraphRunner(
340	                self
341	            )

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 351,
  "limit": 200
}
```

> TOOL

tool_result Read
```
351	    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
352	        """Run speculative decoding forward.
353	
354	        NOTE: Many states of batch is modified as you go through. It is not guaranteed that
355	        the final output batch have the same state as the input.
356	
357	        Args:
358	            batch: The batch to run forward. The state of the batch is modified as it runs.
359	        Returns:
360	            A tuple of the final logit output of the target model, next tokens accepted,
361	            the batch id (used for overlap schedule), and number of accepted tokens.
362	        """
363	        if batch.forward_mode.is_extend() or batch.is_extend_in_batch:
364	            logits_output, next_token_ids, seq_lens_cpu = self.forward_target_extend(
365	                batch
366	            )
367	            with self.draft_tp_context(
368	                self.draft_model_runner.tp_group
369	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
370	                self.forward_draft_extend(
371	                    batch, logits_output.hidden_states, next_token_ids, seq_lens_cpu
372	                )
373	            return GenerationBatchResult(
374	                logits_output=logits_output,
375	                next_token_ids=next_token_ids,
376	                num_accepted_tokens=0,
377	                can_run_cuda_graph=False,
378	            )
379	        else:
380	            with self.draft_tp_context(
381	                self.draft_model_runner.tp_group
382	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
383	                spec_info = self.draft(batch)
384	            logits_output, verify_output, model_worker_batch, can_run_cuda_graph = (
385	                self.verify(batch, spec_info)
386	            )
387	
388	            with self.draft_tp_context(
389	                self.draft_model_runner.tp_group
390	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
391	                # NOTE: We should use `check_forward_draft_extend_after_decode`
392	                # when DP attention is enabled, but it is slow. Skip it for now.
393	                if (
394	                    self.server_args.enable_dp_attention
395	                    or batch.spec_info.verified_id.shape[0] > 0
396	                ):
397	                    # decode is not finished
398	                    self.forward_draft_extend_after_decode(batch)
399	
400	            return GenerationBatchResult(
401	                logits_output=logits_output,
402	                next_token_ids=verify_output.verified_id,
403	                num_accepted_tokens=sum(verify_output.accept_length_per_req_cpu),
404	                accept_length_per_req_cpu=verify_output.accept_length_per_req_cpu,
405	                can_run_cuda_graph=can_run_cuda_graph,
406	            )
407	
408	    def check_forward_draft_extend_after_decode(self, batch: ScheduleBatch):
409	        local_need_forward = batch.spec_info.verified_id.shape[0] > 0
410	        if not self.server_args.enable_dp_attention:
411	            return local_need_forward
412	
413	        global_need_forward = torch.tensor(
414	            [
415	                (local_need_forward),
416	            ],
417	            dtype=torch.int64,
418	        )
419	        torch.distributed.all_reduce(
420	            global_need_forward, group=get_tp_group().cpu_group
421	        )
422	        global_need_forward_cnt = global_need_forward[0].item()
423	        need_forward = global_need_forward_cnt > 0
424	        return need_forward
425	
426	    def forward_target_extend(
427	        self, batch: ScheduleBatch
428	    ) -> Tuple[LogitsProcessorOutput, torch.Tensor, int, Optional[torch.Tensor]]:
429	        """Run the target extend.
430	
431	        Args:
432	            batch: The batch to run. States could be modified.
433	
434	        Returns:
435	            logits_output: The output of logits. It will contain the full hidden states.
436	            next_token_ids: Next token ids generated.
437	        """
438	        # Forward with the target model and get hidden states.
439	        # We need the full hidden states to prefill the KV cache of the draft model.
440	        model_worker_batch = batch.get_model_worker_batch()
441	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.FULL
442	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
443	        logits_output, next_token_ids = (
444	            batch_result.logits_output,
445	            batch_result.next_token_ids,
446	        )
447	        return (
448	            logits_output,
449	            next_token_ids,
450	            model_worker_batch.seq_lens_cpu,
451	        )
452	
453	    def _draft_preprocess_decode(self, batch: ScheduleBatch):
454	        if isinstance(batch.tree_cache, SWAChunkCache):
455	            for req in batch.reqs:
456	                batch.tree_cache.evict_swa(req, req.seqlen - 1)
457	
458	        # Parse args
459	        num_seqs = batch.batch_size()
460	        spec_info = batch.spec_info
461	
462	        # Accumulate penalty
463	        if batch.sampling_info.penalizer_orchestrator.is_required:
464	            # This is a relaxed version of penalties for speculative decoding.
465	            batch.sampling_info.penalizer_orchestrator.cumulate_output_tokens(
466	                spec_info.verified_id.to(torch.int64)
467	            )
468	
469	        # Allocate cache locations
470	        # Layout of the out_cache_loc
471	        # [       topk 0         ] [       topk 1         ]
472	        # [iter=0, iter=1, iter=2] [iter=0, iter=1, iter=2]
473	        if self.page_size == 1:
474	            # TODO: We only need self.speculative_num_steps - 1 * topk cache loc
475	            out_cache_loc, token_to_kv_pool_state_backup = alloc_token_slots(
476	                batch.tree_cache,
477	                num_seqs * self.speculative_num_steps * self.topk,
478	                backup_state=True,
479	            )
480	        else:
481	            if self.topk == 1:
482	                prefix_lens, seq_lens, last_loc = get_last_loc_large_page_size_top_k_1(
483	                    batch.req_to_token_pool.req_to_token,
484	                    batch.req_pool_indices,
485	                    batch.seq_lens,
486	                    self.speculative_num_steps,
487	                )
488	                prefix_lens_cpu = batch.seq_lens_cpu
489	                seq_lens_cpu = batch.seq_lens_cpu + self.speculative_num_steps
490	                extend_num_tokens = num_seqs * self.speculative_num_steps
491	            else:
492	                # In this case, the last partial page needs to be duplicated.
493	                # KV cache layout in batch.req_to_token_pool.req_to_token:
494	                #
495	                # | -------- | -- xxxx .. | -- xxxx .. | -- xxxx .. |
496	                #    prefix     top-k = 0    tok-k = 1    top-k = 2
497	                #
498	                #  "-" means prefix tokens
499	                #  "x" means speculative draft tokens
500	                #  "." means padded tokens
501	
502	                (
503	                    prefix_lens,
504	                    seq_lens,
505	                    last_loc,
506	                    self.num_new_pages_per_topk,
507	                    self.extend_lens,
508	                    last_page_lens,
509	                ) = get_last_loc_large_page_size_large_top_k(
510	                    batch.req_to_token_pool.req_to_token,
511	                    batch.req_pool_indices,
512	                    batch.seq_lens,
513	                    self.speculative_num_steps,
514	                    self.topk,
515	                    self.page_size,
516	                )
517	                prefix_lens_cpu = batch.seq_lens_cpu
518	                last_page_lens_cpu = prefix_lens_cpu % self.page_size
519	                num_new_pages_per_topk = (
520	                    last_page_lens_cpu + self.speculative_num_steps + self.page_size - 1
521	                ) // self.page_size
522	                seq_lens_cpu = (
523	                    prefix_lens_cpu // self.page_size * self.page_size
524	                    + num_new_pages_per_topk * (self.page_size * self.topk)
525	                )
526	                extend_num_tokens = torch.sum((seq_lens_cpu - prefix_lens_cpu)).item()
527	
528	            out_cache_loc, token_to_kv_pool_state_backup = (
529	                alloc_paged_token_slots_extend(
530	                    batch.tree_cache,
531	                    prefix_lens,
532	                    prefix_lens_cpu,
533	                    seq_lens,
534	                    seq_lens_cpu,
535	                    last_loc,
536	                    extend_num_tokens,
537	                    backup_state=True,
538	                )
539	            )
540	
541	        if self.page_size > 1 and self.topk > 1:
542	            last_page_lens_cumsum = torch.cumsum(last_page_lens, dim=0)
543	            duplicate_cache_len = torch.sum(last_page_lens_cpu).item() * (self.topk - 1)
544	            target_cache_loc = torch.zeros(
545	                duplicate_cache_len, dtype=torch.int32, device=self.device
546	            )
547	            source_cache_loc = torch.zeros(
548	                duplicate_cache_len, dtype=torch.int32, device=self.device
549	            )
550	        else:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看 eagle_worker_v2：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	import contextlib
2	import logging
3	import time
4	from typing import List, Optional, Tuple
5	
6	import torch
7	
8	from sglang.srt.environ import envs
9	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_extend_npu_graph_runner import (
10	    EAGLEDraftExtendNpuGraphRunner,
11	)
12	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
13	    EAGLEDraftNpuGraphRunner,
14	)
15	from sglang.srt.layers.attention.triton_backend import TritonMultiStepDraftBackend
16	from sglang.srt.layers.moe.utils import (
17	    speculative_moe_a2a_backend_context,
18	    speculative_moe_backend_context,
19	)
20	from sglang.srt.managers.io_struct import UpdateWeightsFromTensorReqInput
21	from sglang.srt.managers.schedule_batch import ModelWorkerBatch
22	from sglang.srt.managers.scheduler import GenerationBatchResult
23	from sglang.srt.managers.tp_worker import TpModelWorker
24	from sglang.srt.model_executor.forward_batch_info import CaptureHiddenMode, ForwardBatch
25	from sglang.srt.server_args import ServerArgs
26	from sglang.srt.speculative.base_spec_worker import BaseDraftWorker, BaseSpecWorker
27	from sglang.srt.speculative.draft_utils import DraftBackendFactory
28	from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
29	    EAGLEDraftCudaGraphRunner,
30	)
31	from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
32	    EAGLEDraftExtendCudaGraphRunner,
33	)
34	from sglang.srt.speculative.eagle_info import EagleDraftInput, EagleVerifyInput
35	from sglang.srt.speculative.eagle_info_v2 import (
36	    assign_extend_cache_locs,
37	    fill_accepted_out_cache_loc,
38	    fill_new_verified_id,
39	)
40	from sglang.srt.speculative.eagle_utils import TreeMaskMode, build_tree_kernel_efficient
41	from sglang.srt.speculative.spec_info import SpeculativeAlgorithm
42	from sglang.srt.speculative.spec_utils import (
43	    detect_nan,
44	    draft_tp_context,
45	    generate_token_bitmask,
46	    load_token_map,
47	    select_top_k_tokens,
48	)
49	from sglang.srt.utils.common import (
50	    MultiprocessingSerializer,
51	    empty_context,
52	    fast_topk,
53	    get_available_gpu_memory,
54	    is_cuda,
55	    is_npu,
56	    next_power_of_2,
57	)
58	from sglang.srt.utils.patch_torch import monkey_patch_torch_reductions
59	
60	_is_npu = is_npu()
61	_is_cuda = is_cuda()
62	
63	logger = logging.getLogger(__name__)
64	
65	
66	def _get_plan_stream(
67	    device: str,
68	) -> Tuple[any, contextlib.AbstractContextManager]:
69	    if envs.SGLANG_ENABLE_OVERLAP_PLAN_STREAM.get():
70	        plan_stream = torch.get_device_module(device).Stream()
71	        plan_stream_ctx = torch.get_device_module(device).stream(plan_stream)
72	        return plan_stream, plan_stream_ctx
73	    else:
74	        return None, contextlib.nullcontext()
75	
76	
77	class EagleDraftWorker(BaseDraftWorker):
78	    def __init__(
79	        self,
80	        server_args: ServerArgs,
81	        gpu_id: int,
82	        tp_rank: int,
83	        dp_rank: int,
84	        moe_ep_rank: int,
85	        nccl_port: int,
86	        target_worker: TpModelWorker,
87	    ):
88	        # copy args
89	        self.server_args = server_args
90	        self.gpu_id = gpu_id
91	        self.tp_rank = tp_rank
92	        self.dp_rank = dp_rank
93	        self.moe_ep_rank = moe_ep_rank
94	        self.nccl_port = nccl_port
95	        self.target_worker = target_worker
96	
97	        # Args for easy access
98	        self.device = server_args.device
99	        self.topk = server_args.speculative_eagle_topk
100	        self.speculative_num_steps = server_args.speculative_num_steps

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def forward\\|class EagleDraftWorker\\|SGLANG_ENABLE_SPEC_V2\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py | head -40"
}
```

> TOOL

tool_result Bash
```
77:class EagleDraftWorker(BaseDraftWorker):
616:    def forward_batch_generation(self, model_worker_batch: ModelWorkerBatch):
```

> AGENT

现在看 spec_info 和 eagle_utils：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"speculative_num_steps\\|speculative_eagle_topk\\|speculative_num_draft_tokens\\|EAGLE_MARS_THETA\\|EAGLE_FORCE_NO_ACCEPT\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py | head -40"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	import math
2	from enum import IntEnum
3	from typing import List, Optional
4	
5	import torch
6	
7	from sglang.srt.utils import is_cuda, is_hip, is_npu
8	
9	_is_cuda = is_cuda()
10	_is_hip = is_hip()
11	_is_npu = is_npu()
12	
13	if _is_cuda or _is_hip:
14	    from sgl_kernel import (
15	        build_tree_kernel_efficient as sgl_build_tree_kernel_efficient,
16	    )
17	
18	
19	def organize_draft_results(
20	    score_list: List[torch.Tensor],
21	    token_list: List[torch.Tensor],
22	    parents_list: List[torch.Tensor],
23	    num_draft_token: int,
24	):
25	    score_list = torch.cat(score_list, dim=1).flatten(1)
26	    ss_token_list = torch.cat(token_list, dim=1)
27	    top_scores = torch.topk(score_list, num_draft_token - 1, dim=-1)
28	    top_scores_index = top_scores.indices
29	    top_scores_index = torch.sort(top_scores_index).values
30	    draft_tokens = torch.gather(ss_token_list, index=top_scores_index, dim=1)
31	
32	    if len(parents_list) > 1:
33	        parent_list = torch.cat(parents_list[:-1], dim=1)
34	    else:
35	        batch_size = parents_list[0].shape[0]
36	        parent_list = torch.empty(batch_size, 0, device=parents_list[0].device)
37	
38	    return parent_list, top_scores_index, draft_tokens
39	
40	
41	class TreeMaskMode(IntEnum):
42	    FULL_MASK = 0
43	    QLEN_ONLY = 1
44	    QLEN_ONLY_BITPACKING = 2
45	
46	
47	def build_tree_kernel_efficient(
48	    verified_id: torch.Tensor,
49	    parent_list: List[torch.Tensor],
50	    top_scores_index: torch.Tensor,
51	    draft_tokens: torch.Tensor,
52	    seq_lens: torch.Tensor,
53	    seq_lens_sum: int,
54	    topk: int,
55	    spec_steps: int,
56	    num_verify_tokens: int,
57	    tree_mask_mode: TreeMaskMode = TreeMaskMode.FULL_MASK,
58	    tree_mask_buf: Optional[torch.Tensor] = None,
59	    position_buf: Optional[torch.Tensor] = None,
60	):
61	    draft_tokens = torch.cat((verified_id.unsqueeze(1), draft_tokens), dim=1).flatten()
62	
63	    # seq_lens_sum == sum(seq_lens); seq_lens: sequence length without draft tokens
64	    bs = seq_lens.numel()
65	    device = seq_lens.device
66	    # e.g. for bs=1, tree_mask: num_draft_token, seq_lens_sum + num_draft_token (flattened)
67	    # where each row indicates the attending pattern of each draft token
68	    # if use_partial_packed_tree_mask is True, tree_mask: num_draft_token (flattened, packed)
69	    if tree_mask_buf is not None:
70	        tree_mask = tree_mask_buf
71	        if tree_mask_mode == TreeMaskMode.QLEN_ONLY:
72	            tree_mask.fill_(True)
73	        elif tree_mask_mode == TreeMaskMode.QLEN_ONLY_BITPACKING:
74	            tree_mask.fill_(0)
75	        elif tree_mask_mode == TreeMaskMode.FULL_MASK:
76	            tree_mask.fill_(True)
77	        else:
78	            raise NotImplementedError(f"Invalid tree mask: {tree_mask_mode=}")
79	    elif tree_mask_mode == TreeMaskMode.QLEN_ONLY:
80	        tree_mask = torch.full(
81	            (num_verify_tokens * bs * num_verify_tokens,),
82	            True,
83	            dtype=torch.bool,
84	            device=device,
85	        )
86	    elif tree_mask_mode == TreeMaskMode.QLEN_ONLY_BITPACKING:
87	        packed_dtypes = [torch.uint8, torch.uint16, torch.uint32]
88	        packed_dtype_idx = int(math.ceil(math.log2((num_verify_tokens + 7) // 8)))
89	        tree_mask = torch.zeros(
90	            (num_verify_tokens * bs,),
91	            dtype=packed_dtypes[packed_dtype_idx],
92	            device=device,
93	        )
94	    elif tree_mask_mode == TreeMaskMode.FULL_MASK:
95	        tree_mask = torch.full(
96	            (
97	                seq_lens_sum * num_verify_tokens
98	                + num_verify_tokens * num_verify_tokens * bs,
99	            ),
100	            True,
101	            device=device,
102	        )
103	    else:
104	        raise NotImplementedError(f"Invalid tree mask: {tree_mask_mode=}")
105	
106	    # TODO: make them torch.empty and fuse them into `sgl_build_tree_kernel`
107	    retrive_buf = torch.full(
108	        (3, bs, num_verify_tokens), -1, device=device, dtype=torch.long
109	    )
110	    retrive_index, retrive_next_token, retrive_next_sibling = retrive_buf
111	    # position: where each token belongs to
112	    # e.g. if depth of each draft token is [0, 1, 1, 2] and the prompt length is 7
113	    # then, positions = [7, 8, 8, 9]
114	    if position_buf is not None:
115	        positions = position_buf
116	    else:
117	        positions = torch.empty(
118	            (bs * num_verify_tokens,), device=device, dtype=torch.long
119	        )
120	
121	    if _is_npu:
122	        torch.ops.npu.build_tree_kernel_efficient(
123	            parent_list.to(dtype=torch.int64),
124	            top_scores_index,
125	            seq_lens,
126	            tree_mask,
127	            positions,
128	            retrive_index,
129	            retrive_next_token,
130	            retrive_next_sibling,
131	            topk,
132	            spec_steps,
133	            num_verify_tokens,
134	            tree_mask_mode,
135	        )
136	    else:
137	        sgl_build_tree_kernel_efficient(
138	            parent_list,
139	            top_scores_index,
140	            seq_lens,
141	            tree_mask,
142	            positions,
143	            retrive_index,
144	            retrive_next_token,
145	            retrive_next_sibling,
146	            topk,
147	            spec_steps,
148	            num_verify_tokens,
149	            tree_mask_mode,
150	        )

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 CUDA graph 的初始化和 dtn 的使用：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"num_verify_tokens\\|num_draft_tokens\\|dtn\\|decode_tree_mask\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -50"
}
```

> TOOL

tool_result Bash
```
156:        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
647:                self.speculative_num_draft_tokens,
666:            self.speculative_num_draft_tokens,
710:            draft_token_num=self.server_args.speculative_num_draft_tokens,
783:            score_list, token_list, parents_list, self.speculative_num_draft_tokens
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 640,
  "limit": 100
}
```

> TOOL

tool_result Read
```
640	                forward_batch
641	            )
642	
643	        if batch.forward_mode.is_idle():
644	            return EagleVerifyInput.create_idle_input(
645	                self.topk,
646	                self.speculative_num_steps,
647	                self.speculative_num_draft_tokens,
648	            )
649	
650	        (
651	            tree_mask,
652	            position,
653	            retrive_index,
654	            retrive_next_token,
655	            retrive_next_sibling,
656	            draft_tokens,
657	        ) = build_tree_kernel_efficient(
658	            spec_info.verified_id,
659	            parent_list,
660	            top_scores_index,
661	            draft_tokens,
662	            batch.seq_lens,
663	            batch.seq_lens_sum,
664	            self.topk,
665	            self.speculative_num_steps,
666	            self.speculative_num_draft_tokens,
667	        )
668	
669	        if _EAGLE_TRACE_PATH:
670	            try:
671	                _tr_draft = draft_tokens.view(len(batch.reqs), -1).cpu().tolist()
672	                _tr_pos = position.view(len(batch.reqs), -1).cpu().tolist()
673	                _tr_parent = parent_list.cpu().tolist()
674	                _tr_top_idx = top_scores_index.cpu().tolist()
675	                _tr_ri = retrive_index.cpu().tolist()
676	                _tr_rnt = retrive_next_token.cpu().tolist()
677	                _tr_rns = retrive_next_sibling.cpu().tolist()
678	                _tr_vid = spec_info.verified_id.cpu().tolist()
679	                _tr_sl = batch.seq_lens_cpu.tolist()
680	                for _i, _req in enumerate(batch.reqs):
681	                    _eagle_trace_emit(
682	                        {
683	                            "kind": "tree",
684	                            "rid": str(_req.rid)[:12],
685	                            "step": int(_req.spec_verify_ct),
686	                            "sl": int(_tr_sl[_i]),
687	                            "vid": int(_tr_vid[_i]),
688	                            "parents": _tr_parent[_i],
689	                            "top_idx": _tr_top_idx[_i],
690	                            "draft": _tr_draft[_i],
691	                            "pos": _tr_pos[_i],
692	                            "ri": _tr_ri[_i],
693	                            "rnt": _tr_rnt[_i],
694	                            "rns": _tr_rns[_i],
695	                        }
696	                    )
697	            except Exception as _e:
698	                logger.warning(f"eagle tree trace emit failed: {_e}")
699	
700	        return EagleVerifyInput(
701	            draft_token=draft_tokens,
702	            custom_mask=tree_mask,
703	            positions=position,
704	            retrive_index=retrive_index,
705	            [REDACTED],
706	            retrive_next_sibling=retrive_next_sibling,
707	            retrive_cum_len=None,
708	            spec_steps=self.speculative_num_steps,
709	            topk=self.topk,
710	            draft_token_num=self.server_args.speculative_num_draft_tokens,
711	            capture_hidden_mode=CaptureHiddenMode.FULL,
712	            seq_lens_sum=forward_batch.seq_lens_sum,
713	            seq_lens_cpu=forward_batch.seq_lens_cpu,
714	        )
715	
716	    def draft_forward(self, forward_batch: ForwardBatch):
717	        # Parse args
718	        spec_info = forward_batch.spec_info
719	        assert isinstance(spec_info, EagleDraftInput)
720	        out_cache_loc = forward_batch.out_cache_loc
721	        topk_p, topk_index, hidden_states = (
722	            spec_info.topk_p,
723	            spec_info.topk_index,
724	            spec_info.hidden_states,
725	        )
726	        if self.hot_token_id is not None:
727	            topk_index = self.hot_token_id[topk_index]
728	        # TODO: We only need self.speculative_num_steps - 1 cache loc
729	        out_cache_loc = out_cache_loc.reshape(
730	            forward_batch.batch_size, self.topk, self.speculative_num_steps
731	        )
732	        out_cache_loc = out_cache_loc.permute((2, 0, 1)).reshape(
733	            self.speculative_num_steps, -1
734	        )
735	
736	        # Return values
737	        score_list: List[torch.Tensor] = []
738	        token_list: List[torch.Tensor] = []
739	        parents_list: List[torch.Tensor] = []

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看 server_args.py 中 spec 相关参数的定义：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"speculative_num_steps\\|speculative_eagle_topk\\|speculative_num_draft_tokens\\|cuda.*graph.*bs\\|cuda_graph_batch_size\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py | head -50"
}
```

> TOOL

tool_result Bash
```
423:    speculative_num_steps: Optional[int] = None
424:    speculative_eagle_topk: Optional[int] = None
425:    speculative_num_draft_tokens: Optional[int] = None
529:    cuda_graph_max_bs: Optional[int] = None
530:    cuda_graph_bs: Optional[List[int]] = None
849:        chunked_prefill_size, cuda_graph_max_bs, and mem_fraction_static.
852:        - Set chunked_prefill_size and cuda_graph_max_bs based on the GPU memory capacity.
854:          chunked_prefill_size and a larger cuda_graph_max_bs to fully utilize the GPU.
855:        - Then set mem_fraction_static based on chunked_prefill_size and cuda_graph_max_bs.
864:          The cuda graph memory is proportional to the cuda_graph_max_bs.
865:          We use reserved_mem = chunked_prefill_size * 1.5 + cuda_graph_max_bs * 2 to estimate the size of activations and cuda graph buffers in GB.
873:                # (chunked_prefill_size 2k, cuda_graph_max_bs 8)
876:                if self.cuda_graph_max_bs is None:
877:                    self.cuda_graph_max_bs = 8
880:                # (chunked_prefill_size 2k, cuda_graph_max_bs 24 if tp < 4 else 80)
883:                if self.cuda_graph_max_bs is None:
884:                    # Based on detailed statistics, when serving TP1/TP2 models on lower-end GPUs with HBM < 35GB, you can either disable cuda graph or set `cuda_graph_max_bs` to a very small value to reduce the memory overhead of creating cuda graphs, with almost no impact on performance.
885:                    # However, when serving models with TP4 or TP8, we need to enable cuda graph to maintain high performance. In this case, we can set `cuda_graph_max_bs` to 80 (half of the default value 160) to reduce the memory overhead of creating cuda graphs. Looking at the logs
888:                        self.cuda_graph_max_bs = 24
890:                        self.cuda_graph_max_bs = 80
893:                # (chunked_prefill_size 4k, cuda_graph_max_bs 32 if tp < 4 else 160)
896:                if self.cuda_graph_max_bs is None:
898:                        self.cuda_graph_max_bs = 32
900:                        self.cuda_graph_max_bs = 160
903:                # (chunked_prefill_size 8k, cuda_graph_max_bs 256 if tp < 4 else 512)
906:                if self.cuda_graph_max_bs is None:
908:                        self.cuda_graph_max_bs = 256
910:                        self.cuda_graph_max_bs = 512
913:                # (chunked_prefill_size 8k, cuda_graph_max_bs 256 if tp < 4 else 512)
916:                if self.cuda_graph_max_bs is None:
918:                        self.cuda_graph_max_bs = 256
920:                        self.cuda_graph_max_bs = 512
923:                # (chunked_prefill_size 16k, cuda_graph_max_bs 512)
926:                if self.cuda_graph_max_bs is None:
927:                    self.cuda_graph_max_bs = 512
932:            if self.cuda_graph_max_bs is None:
933:                self.cuda_graph_max_bs = 160
936:        if self.cuda_graph_bs is None:
937:            self.cuda_graph_bs = self._generate_cuda_graph_batch_sizes()
939:            self.cuda_graph_max_bs = max(self.cuda_graph_bs)
961:            reserved_mem += self.cuda_graph_max_bs * 2
967:                reserved_mem += self.cuda_graph_max_bs * self.dp_size * 3
969:                # DP attention uses much more memory for large cuda graph max bs,
972:                if self.cuda_graph_max_bs > 300:
973:                    reserved_mem += self.cuda_graph_max_bs * self.dp_size * 1.5
1002:    def _generate_cuda_graph_batch_sizes(self):
1004:        Generate the list of batch sizes for CUDA graph capture based on cuda_graph_max_bs.
1009:            capture_bs = list(range(1, self.cuda_graph_max_bs + 1))
1016:                + list(range(512, self.cuda_graph_max_bs + 1, 32))
1025:                + list(range(272, self.cuda_graph_max_bs + 1, 16))
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py",
  "offset": 423,
  "limit": 30
}
```

> TOOL

tool_result Read
```
423	    speculative_num_steps: Optional[int] = None
424	    speculative_eagle_topk: Optional[int] = None
425	    speculative_num_draft_tokens: Optional[int] = None
426	    speculative_accept_threshold_single: float = 1.0
427	    speculative_accept_threshold_acc: float = 1.0
428	    speculative_token_map: Optional[str] = None
429	    speculative_attention_mode: str = "prefill"
430	    speculative_draft_attention_backend: Optional[str] = None
431	    speculative_moe_runner_backend: Optional[str] = None
432	    speculative_moe_a2a_backend: Optional[str] = None
433	    speculative_draft_model_quantization: Optional[str] = None
434	
435	    # Speculative decoding (ngram)
436	    speculative_ngram_min_match_window_size: int = 1
437	    speculative_ngram_max_match_window_size: int = 12
438	    speculative_ngram_min_bfs_breadth: int = 1
439	    speculative_ngram_max_bfs_breadth: int = 10
440	    speculative_ngram_match_type: Literal["BFS", "PROB"] = "BFS"
441	    speculative_ngram_branch_length: int = 18
442	    speculative_ngram_capacity: int = 10 * 1000 * 1000
443	    enable_multi_layer_eagle: bool = False
444	
445	    # Expert parallelism
446	    ep_size: int = 1
447	    moe_a2a_backend: Literal["none", "deepep", "mooncake", "ascend_fuseep"] = "none"
448	    moe_runner_backend: str = "auto"
449	    flashinfer_mxfp4_moe_precision: Literal["default", "bf16"] = "default"
450	    enable_flashinfer_allreduce_fusion: bool = False
451	    deepep_mode: Literal["auto", "normal", "low_latency"] = "auto"
452	    ep_num_redundant_experts: int = 0

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查找 EAGLE_MARS_THETA 和 EAGLE_FORCE_NO_ACCEPT：

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"EAGLE_MARS_THETA\\|EAGLE_FORCE_NO_ACCEPT\\|MARS_THETA\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/ | head -40"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:24:_FORCE_NO_ACCEPT = os.environ.get("EAGLE_FORCE_NO_ACCEPT", "0") == "1"
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:26:_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:344:            # Enabled when EAGLE_MARS_THETA >= 0; default disabled (-1.0) keeps standard SD.
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:345:            mars_theta = float(_MARS_THETA)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	import json
2	import logging
3	import os
4	import threading
5	from copy import copy
6	from dataclasses import dataclass
7	from typing import ClassVar, List, Optional, Tuple
8	
9	import torch
10	import torch.nn.functional as F
11	
12	
13	_EAGLE_TRACE_PATH = os.environ.get("EAGLE_TRACE_FILE")
14	_EAGLE_TRACE_FD = None
15	_EAGLE_TRACE_LOCK = threading.Lock()
16	
17	# Collapse instrumentation: per-rid consecutive al==0 counter. When a request
18	# stays in al==0 for >= EAGLE_COLLAPSE_LOG_K consecutive verify steps, log a
19	# warning. Pure visibility — does NOT alter spec behavior. Use to monitor
20	# collapse frequency on production traffic. Default K=10 so noise stays low.
21	_COLLAPSE_COUNTERS: dict = {}
22	_COLLAPSE_LOG_K = int(os.environ.get("EAGLE_COLLAPSE_LOG_K", "10"))
23	_COLLAPSE_LOG_LOCK = threading.Lock()
24	_FORCE_NO_ACCEPT = os.environ.get("EAGLE_FORCE_NO_ACCEPT", "0") == "1"
25	# MARS verify (arXiv:2601.15498): theta < 0 disables, default. Recommended 0.9.
26	_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))
27	
28	
29	def _eagle_trace_emit(rec: dict):
30	    global _EAGLE_TRACE_FD
31	    if not _EAGLE_TRACE_PATH:
32	        return
33	    with _EAGLE_TRACE_LOCK:
34	        if _EAGLE_TRACE_FD is None:
35	            _EAGLE_TRACE_FD = open(_EAGLE_TRACE_PATH, "a", buffering=1 << 20)
36	        _EAGLE_TRACE_FD.write(json.dumps(rec, separators=(",", ":")) + "\n")
37	        _EAGLE_TRACE_FD.flush()
38	
39	from sglang.srt.constrained.base_grammar_backend import BaseGrammarObject
40	from sglang.srt.environ import envs
41	from sglang.srt.layers.attention.utils import create_flashinfer_kv_indices_triton
42	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
43	from sglang.srt.layers.sampler import apply_custom_logit_processor
44	from sglang.srt.managers.overlap_utils import FutureIndices
45	from sglang.srt.managers.schedule_batch import FINISH_MATCHED_TOKEN, ScheduleBatch
46	from sglang.srt.mem_cache.allocator import BaseTokenToKVPoolAllocator
47	from sglang.srt.mem_cache.common import (
48	    alloc_paged_token_slots_extend,
49	    alloc_token_slots,
50	    get_last_loc,
51	)
52	from sglang.srt.model_executor.forward_batch_info import CaptureHiddenMode
53	from sglang.srt.server_args import get_global_server_args
54	from sglang.srt.speculative.eagle_info_v2 import (
55	    EagleDraftInputV2Mixin,
56	    EagleVerifyInputV2Mixin,
57	)
58	from sglang.srt.speculative.eagle_utils import verify_tree_greedy_func
59	from sglang.srt.speculative.spec_info import SpecInput, SpecInputType
60	from sglang.srt.speculative.spec_utils import (
61	    SIMULATE_ACC_LEN,
62	    TREE_SPEC_KERNEL_AVAILABLE,
63	    align_evict_mask_to_page_size,
64	    assign_req_to_token_pool_func,
65	    create_accept_length_filter,
66	    create_extend_after_decode_spec_info,
67	    filter_finished_cache_loc_kernel,
68	    generate_simulated_accept_index,
69	    get_src_tgt_cache_loc,
70	    get_target_cache_loc,
71	)
72	from sglang.srt.utils import is_cuda, next_power_of_2
73	
74	if is_cuda():
75	    from sgl_kernel import (
76	        top_k_renorm_prob,
77	        top_p_renorm_prob,
78	        tree_speculative_sampling_target_only,
79	    )
80	
81	logger = logging.getLogger(__name__)
82	
83	
84	@dataclass
85	class EagleVerifyInput(SpecInput, EagleVerifyInputV2Mixin):
86	    draft_token: torch.Tensor
87	    custom_mask: torch.Tensor
88	    positions: torch.Tensor
89	    retrive_index: torch.Tensor
90	    retrive_next_token: torch.Tensor
91	    retrive_next_sibling: torch.Tensor
92	    retrive_cum_len: torch.Tensor
93	    spec_steps: int
94	    topk: int
95	    draft_token_num: int
96	    capture_hidden_mode: CaptureHiddenMode
97	    seq_lens_sum: int
98	    seq_lens_cpu: torch.Tensor
99	    grammar: BaseGrammarObject = None
100	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 340,
  "limit": 100
}
```

> TOOL

tool_result Read
```
340	        if is_all_greedy or not TREE_SPEC_KERNEL_AVAILABLE:
341	          with torch.profiler.record_function("verify_tree_greedy"):
342	            # MARS (Margin-Aware Speculative verification, arXiv:2601.15498):
343	            # accept draft if it == argmax (top-1) OR (it == top-2 AND z2/z1 > theta).
344	            # Enabled when EAGLE_MARS_THETA >= 0; default disabled (-1.0) keeps standard SD.
345	            mars_theta = float(_MARS_THETA)
346	            if mars_theta >= 0.0:
347	                top2 = torch.topk(logits_output.next_token_logits, 2, dim=-1)
348	                target_predict = top2.indices[..., 0].reshape(bs, self.draft_token_num)
349	                top2_token = top2.indices[..., 1].reshape(bs, self.draft_token_num).contiguous()
350	                z1 = top2.values[..., 0]
351	                z2 = top2.values[..., 1]
352	                # ratio = z2/z1 only when z1 > 0; else -1.0 (never triggers MARS)
353	                ratio = torch.where(z1 > 0, z2 / z1, torch.full_like(z2, -1.0))
354	                top2_ratio = ratio.reshape(bs, self.draft_token_num).contiguous().float()
355	            else:
356	                target_predict = torch.argmax(logits_output.next_token_logits, dim=-1)
357	                target_predict = target_predict.reshape(bs, self.draft_token_num)
358	                top2_token = None
359	                top2_ratio = None
360	
361	            predict, accept_index, accept_length = verify_tree_greedy_func(
362	                predicts=predict,  # mutable
363	                accept_index=accept_index,  # mutable
364	                accept_token_num=accept_length,  # mutable
365	                candidates=candidates,
366	                retrive_index=self.retrive_index,
367	                [REDACTED],
368	                retrive_next_sibling=self.retrive_next_sibling,
369	                target_predict=target_predict,
370	                topk=self.topk,
371	                top2_token=top2_token,
372	                top2_ratio=top2_ratio,
373	                mars_theta=mars_theta,
374	            )
375	
376	        else:
377	            # apply temperature and get target probs
378	            expanded_temperature = torch.repeat_interleave(
379	                sampling_info.temperatures, self.draft_token_num, dim=0
380	            )  # (bs * draft_token_num, 1)
381	
382	            target_probs = F.softmax(
383	                logits_output.next_token_logits / expanded_temperature, dim=-1
384	            )  # (bs * draft_token_num, vocab_size)
385	            target_probs = top_k_renorm_prob(
386	                target_probs,
387	                torch.repeat_interleave(
388	                    sampling_info.top_ks, self.draft_token_num, dim=0
389	                ),
390	            )  # (bs * draft_token_num, vocab_size)
391	            if not torch.all(sampling_info.top_ps == 1.0):
392	                target_probs = top_p_renorm_prob(
393	                    target_probs,
394	                    torch.repeat_interleave(
395	                        sampling_info.top_ps, self.draft_token_num, dim=0
396	                    ),
397	                )
398	            target_probs = target_probs.reshape(bs, self.draft_token_num, -1)
399	
400	            draft_probs = torch.zeros(
401	                target_probs.shape, dtype=torch.float32, device=batch.device
402	            )
403	
404	            # coins for rejection sampling
405	            coins = torch.rand_like(
406	                candidates, dtype=torch.float32, device=batch.device
407	            )
408	            # coins for final sampling
409	            coins_for_final_sampling = torch.rand(
410	                (bs,), dtype=torch.float32, device=batch.device
411	            )
412	            tree_speculative_sampling_target_only(
413	                predicts=predict,  # mutable
414	                accept_index=accept_index,  # mutable
415	                accept_token_num=accept_length,  # mutable
416	                candidates=candidates,
417	                retrive_index=self.retrive_index,
418	                [REDACTED],
419	                retrive_next_sibling=self.retrive_next_sibling,
420	                uniform_samples=coins,
421	                uniform_samples_for_final_sampling=coins_for_final_sampling,
422	                target_probs=target_probs,
423	                draft_probs=draft_probs,
424	                threshold_single=get_global_server_args().speculative_accept_threshold_single,
425	                threshold_acc=get_global_server_args().speculative_accept_threshold_acc,
426	                deterministic=True,
427	            )
428	
429	        if SIMULATE_ACC_LEN > 0.0:
430	            # Do simulation
431	            accept_index = generate_simulated_accept_index(
432	                accept_index=accept_index,
433	                predict=predict,  # mutable
434	                accept_length=accept_length,  # mutable
435	                bs=bs,
436	                spec_steps=self.spec_steps,
437	            )
438	
439	        if _FORCE_NO_ACCEPT:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 438,
  "limit": 30
}
```

> TOOL

tool_result Read
```
438	
439	        if _FORCE_NO_ACCEPT:
440	            # Profile hack: force all draft tokens rejected. Keep user_4813494d only.
441	            accept_index[:, 1:] = -1
442	            accept_length.zero_()
443	
444	        if _EAGLE_TRACE_PATH:
445	            try:
446	                dtn = self.draft_token_num
447	                _tr_logits_v = logits_output.next_token_logits.view(bs, dtn, -1).float()
448	                _tr_top2_v, _tr_top2_i = torch.topk(_tr_logits_v, 2, dim=-1)
449	                _tr_top2_v_cpu = _tr_top2_v.cpu().tolist()
450	                _tr_top2_i_cpu = _tr_top2_i.cpu().tolist()
451	                _tr_draft = self.draft_token.view(bs, dtn).cpu().tolist()
452	                _tr_accept_idx = accept_index.cpu().tolist()
453	                _tr_accept_len = accept_length.cpu().tolist()
454	                _tr_predict = predict.cpu().tolist()
455	                _tr_hs = logits_output.hidden_states.view(bs, dtn, -1).float()
456	                _tr_hs_norm = _tr_hs.norm(dim=-1).cpu().tolist()
457	                _tr_hs_sample = _tr_hs[:, :, :3].cpu().tolist()
458	                _tr_sl = batch.seq_lens_cpu.tolist()
459	                _tr_pos = self.positions.view(bs, dtn).cpu().tolist()
460	                _tr_ri = self.retrive_index.cpu().tolist()
461	                _tr_rnt = self.retrive_next_token.cpu().tolist()
462	                _tr_rns = self.retrive_next_sibling.cpu().tolist()
463	                for _i, _req in enumerate(batch.reqs):
464	                    _eagle_trace_emit({
465	                        "rid": str(_req.rid)[:12],
466	                        "kind": "verify",
467	                        "step": int(_req.spec_verify_ct),

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 start_eagle.sh 的参数：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eval/start_eagle.sh"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env bash
2	set -euo pipefail
3	
4	cd /user_4813494d/openbmb
5	
6	# Ensure the project venv is active (scripts must not depend on caller's shell).
7	SALA_VENV="/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env"
8	if [[ "${VIRTUAL_ENV:-}" != "${SALA_VENV}" || "$(command -v python3)" != "${SALA_VENV}/bin/python3" ]]; then
9	    # shellcheck disable=SC1091
10	    source "${SALA_VENV}/bin/activate"
11	fi
12	
13	# EAGLE-3 speculative decoding server (current production config)
14	# - spec_steps=2, topk=1, dtn=3  (chain verify, break-even accept_len ~1.15)
15	# - target: NVFP4 (GPTQ + FourOverSix), hybrid Marlin/CUTLASS decode @ threshold=48
16	# - draft:  v2 FP4_QAT, pure Marlin W4A16
17	#
18	# Env overrides:
19	#   EAGLE_SPEC_STEPS, EAGLE_TOPK, EAGLE_TARGET_MODEL, EAGLE_DRAFT_MODEL
20	#   SGLANG_MINICPM_PLAN_CACHE=0 to disable long-prompt prefill plan reuse
21	#   SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=1 to restore old decode replay fills
22	#   SGLANG_SIMPLE_GLA_DIRECT_DECODE=0 to disable the direct-state decode kernel
23	
24	SPEC_STEPS="${EAGLE_SPEC_STEPS:-2}"
25	TOPK="${EAGLE_TOPK:-2}"
26	# dtn = 1 + topk * spec_steps (tree nodes)
27	DTN=$((1 + TOPK * SPEC_STEPS))
28	TARGET_MODEL="${EAGLE_TARGET_MODEL:-/user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4}"
29	DRAFT_MODEL="${EAGLE_DRAFT_MODEL:-/user_4813494d/openbmb/demo-sala/data/eagle_draft}"
30	RANDOM_SEED_ARGS=()
31	if [[ -n "${SGLANG_RANDOM_SEED:-}" ]]; then
32	    RANDOM_SEED_ARGS=(--random-seed "${SGLANG_RANDOM_SEED}")
33	fi
34	
35	EAGLE_FORCE_NO_ACCEPT="${EAGLE_FORCE_NO_ACCEPT:-0}" \
36	EAGLE_TRACE_FILE="${EAGLE_TRACE_FILE:-}" \
37	SGLANG_MINICPM_PLAN_CACHE="${SGLANG_MINICPM_PLAN_CACHE:-1}" \
38	SGLANG_MINICPM_FILL_COMPRESS_BUFFERS="${SGLANG_MINICPM_FILL_COMPRESS_BUFFERS:-0}" \
39	SGLANG_SIMPLE_GLA_DIRECT_DECODE="${SGLANG_SIMPLE_GLA_DIRECT_DECODE:-1}" \
40	SGLANG_SIMPLE_GLA_DECODE_WARPS="${SGLANG_SIMPLE_GLA_DECODE_WARPS:-4}" \
41	SGLANG_FP4_TUNE_CACHE="${SGLANG_FP4_TUNE_CACHE:-/user_4813494d/openbmb/demo-sala/assets/mm_fp4_tune_sm120.json}" \
42	SGLANG_MARLIN_DECODE_THRESHOLD="${SGLANG_MARLIN_DECODE_THRESHOLD:-48}" \
43	CUTE_DSL_ARCH="${CUTE_DSL_ARCH:-sm_120a}" \
44	CUTE_DSL_CACHE_DIR="${CUTE_DSL_CACHE_DIR:-/user_4813494d/openbmb/bench/b12x/cache/cute_dsl}" \
45	SGLANG_ENABLE_B12X="${SGLANG_ENABLE_B12X:-0}" \
46	SGLANG_B12X_DISPATCH_PROFILE="${SGLANG_B12X_DISPATCH_PROFILE:-tuned}" \
47	SGLANG_B12X_PRECOMPILE="${SGLANG_B12X_PRECOMPILE:-1}" \
48	SGLANG_B12X_PRECOMPILE_PROFILE="${SGLANG_B12X_PRECOMPILE_PROFILE:-nospec-mini}" \
49	SGLANG_ENABLE_SPEC_V2=0 \
50	EAGLE_MARS_THETA=0.85 \
51	python3 -m sglang.launch_server \
52	    --model-path "${TARGET_MODEL}" \
53	    --trust-remote-code --port 30000 \
54	    --mem-fraction-static 0.75 \
55	    --max-running-requests 64 \
56	    --attention-backend minicpm_flashinfer \
57	    --chunked-prefill-size 8192 --disable-radix-cache \
58	    --skip-server-warmup \
59	    --dense-as-sparse \
60	    --quantization modelopt_fp4 \
61	    --speculative-algorithm EAGLE3 \
62	    --speculative-num-steps "${SPEC_STEPS}" \
63	    --speculative-eagle-topk "${TOPK}" \
64	    --speculative-num-draft-tokens "${DTN}" \
65	    --speculative-draft-attention-backend flashinfer \
66	    --speculative-draft-model-path "${DRAFT_MODEL}" \
67	    "${RANDOM_SEED_ARGS[@]}"
68	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 verify 流程相关的内核代码：

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -path \"*/sgl-kernel/csrc/speculative/*.cu\" -o -path \"*/sgl-kernel/csrc/speculative/*.h\" | head -10"
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
  "command": "find /user_4813494d/openbmb -type f -name \"eagle_utils.cu\" | head -5"
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
  "command": "find /user_4813494d/openbmb -type d -name \"sgl-kernel\" | head -3"
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
  "command": "find /user_4813494d/openbmb -name \"*eagle*\" -type f | grep -E \"\\.(cu|cpp|h)$\" | head -10"
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
  "command": "ls -la /user_4813494d/openbmb/"
}
```

> TOOL

tool_result Bash
```
total 1215884
drwxr-xr-x 22 user_4813494d user_4813494d      4096 Apr 27 20:46 .
drwx------  1 user_4813494d user_4813494d      4096 Apr 27 21:13 ..
drwxr-xr-x  2 user_4813494d user_4813494d        54 Apr 27 15:47 .claude
drwxr-xr-x 11 user_4813494d user_4813494d      4096 Apr 27 21:13 .git
-rw-r-----  1 user_4813494d user_4813494d        81 Apr 23 13:09 .gitattributes
-rw-r--r--  1 user_4813494d user_4813494d      1796 Apr 26 07:13 .gitignore
drwxr-xr-x  2 user_4813494d user_4813494d       167 Apr 15 10:20 .ipynb_checkpoints
drwxr-xr-x  3 user_4813494d user_4813494d        90 Apr 19 13:28 .pytest_cache
drwxr-xr-x  3 user_4813494d user_4813494d        75 Apr 18 05:26 .ruff_cache
-rw-r--r--  1 user_4813494d user_4813494d     10950 Apr 26 07:23 AGENTS.md
-rw-r--r--  1 user_4813494d user_4813494d      8279 Apr 26 17:30 CLAUDE.md
-rwxr-xr-x  1 user_4813494d user_4813494d  16342389 Mar 29 14:48 bcecmd
drwxr-xr-x 13 user_4813494d user_4813494d      4096 Apr 27 14:51 bench
drwxr-xr-x  9 user_4813494d user_4813494d      4096 Apr 27 20:16 demo-sala
-rw-r--r--  1 user_4813494d user_4813494d 409505489 Apr 27 18:17 demo-sala-20260427.tar.gz
-rw-r--r--  1 user_4813494d user_4813494d 409506292 Apr 27 20:16 demo-sala-20260428.tar.gz
drwxr-xr-x  4 user_4813494d user_4813494d        74 Apr 26 16:53 demo-sala.from_tar.20260426_082915
-rw-r--r--  1 user_4813494d user_4813494d 409503177 Apr 26 22:24 demo-sala.tar.gz
drwxr-xr-x  4 user_4813494d user_4813494d      4096 Apr 27 21:03 docs
drwxr-xr-x 11 user_4813494d user_4813494d      4096 Apr 26 07:23 eagle
-rw-r--r--  1 user_4813494d user_4813494d     21854 Apr 19 05:05 eagle3_runtime_investigation.md
drwxr-xr-x  5 user_4813494d user_4813494d      4096 Apr 27 20:32 eval
drwxr-xr-x  4 user_4813494d user_4813494d        63 Mar 31 15:21 kernels
drwxr-xr-x  5 user_4813494d user_4813494d      4096 Apr 19 05:05 medusa
drwxr-xr-x 11 user_4813494d user_4813494d      4096 Apr 26 12:49 outputs
drwxr-xr-x  2 user_4813494d user_4813494d       118 Apr 12 07:43 probe-env-diff
drwxr-xr-x 10 user_4813494d user_4813494d      4096 Apr 27 20:23 probe-sala
drwxr-xr-x  2 user_4813494d user_4813494d       100 Apr 12 07:36 probe-so-test
drwxr-xr-x  4 user_4813494d user_4813494d      4096 Apr 17 02:44 quant
-rw-r--r--  1 user_4813494d user_4813494d     40441 Apr 27 20:31 sgl_kernel_py_snapshot.tar.gz
-rw-r--r--  1 user_4813494d user_4813494d     24243 Apr 27 20:36 sglang_0427_24_custom.jsonl
-rw-r--r--  1 user_4813494d user_4813494d     24247 Apr 27 20:46 sglang_0427_64_custom.jsonl
drwxr-xr-x  3 user_4813494d user_4813494d      4096 Apr 20 06:48 tests
drwxr-xr-x  4 user_4813494d user_4813494d       184 Apr 20 09:50 toolkit
```

> AGENT

题目中提到内核代码在 `sgl-kernel/csrc/speculative/eagle_utils.cu`，但实际上看起来 sgl-kernel 是作为依赖导入的。让我看看 eagle_worker 中的 verify 流程：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def verify\\|def forward_target\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -30"
}
```

> TOOL

tool_result Bash
```
426:    def forward_target_extend(
792:    def verify(self, batch: ScheduleBatch, spec_info: EagleVerifyInput):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 792,
  "limit": 150
}
```

> TOOL

tool_result Read
```
792	    def verify(self, batch: ScheduleBatch, spec_info: EagleVerifyInput):
793	        seq_lens_pre_verify = batch.seq_lens.clone()
794	        seq_lens_pre_verify_cpu = batch.seq_lens_cpu.clone()
795	
796	        # Free the draft model's KV cache slots BEFORE prepare_for_verify overwrites batch.out_cache_loc.
797	        # The draft phase allocated (num_seqs * steps * topk) tokens in _draft_preprocess_decode,
798	        # which are no longer needed once draft_forward completes. If we don't free them here,
799	        # they become orphaned when prepare_for_verify allocates new slots for verification.
800	        if batch.out_cache_loc is not None and not batch.forward_mode.is_idle():
801	            batch.tree_cache.token_to_kv_pool_allocator.free(batch.out_cache_loc)
802	
803	        spec_info.prepare_for_verify(batch, self.page_size)
804	        spec_info.num_tokens_per_batch = self.speculative_num_steps + 1
805	        batch.return_hidden_states = False
806	        batch.forward_mode = (
807	            ForwardMode.TARGET_VERIFY
808	            if not batch.forward_mode.is_idle()
809	            else ForwardMode.IDLE
810	        )
811	        batch.spec_info = spec_info
812	
813	        model_worker_batch = batch.get_model_worker_batch(
814	            seq_lens_cpu_cache=spec_info.seq_lens_cpu
815	        )
816	        assert model_worker_batch.capture_hidden_mode == spec_info.capture_hidden_mode
817	
818	        if batch.has_grammar:
819	            retrieve_next_token_cpu = spec_info.retrive_next_token.cpu()
820	            retrieve_next_sibling_cpu = spec_info.retrive_next_sibling.cpu()
821	            draft_tokens_cpu = spec_info.draft_token.view(
822	                spec_info.retrive_next_token.shape
823	            ).cpu()
824	
825	        # Forward
826	        batch_result = self.target_worker.forward_batch_generation(
827	            model_worker_batch, is_verify=True
828	        )
829	        logits_output, can_run_cuda_graph = (
830	            batch_result.logits_output,
831	            batch_result.can_run_cuda_graph,
832	        )
833	
834	        vocab_mask = None
835	        if batch.has_grammar:
836	            # Generate the logit mask for structured output.
837	            # Overlap the CPU operations for bitmask generation with the forward pass.
838	            vocab_mask = generate_token_bitmask(
839	                batch.reqs,
840	                spec_info,
841	                retrieve_next_token_cpu,
842	                retrieve_next_sibling_cpu,
843	                draft_tokens_cpu,
844	                batch.sampling_info.vocab_size,
845	            )
846	
847	            if vocab_mask is not None:
848	                assert spec_info.grammar is not None
849	                vocab_mask = vocab_mask.to(spec_info.retrive_next_token.device)
850	                # NOTE (sk): otherwise, this vocab mask will be the one from the previous extend stage
851	                # and will be applied to produce wrong results
852	                batch.sampling_info.vocab_mask = None
853	
854	        if self.enable_nan_detection:
855	            detect_nan(logits_output)
856	
857	        spec_info.hidden_states = logits_output.hidden_states
858	        res: EagleVerifyOutput = spec_info.verify(
859	            batch,
860	            logits_output,
861	            self.token_to_kv_pool_allocator,
862	            self.page_size,
863	            vocab_mask,
864	        )
865	
866	        # Post process based on verified outputs.
867	        # Pick indices that we care (accepted)
868	        logits_output.next_token_logits = logits_output.next_token_logits[
869	            res.accepted_indices
870	        ]
871	        logits_output.hidden_states = logits_output.hidden_states[res.accepted_indices]
872	
873	        if (
874	            self.target_worker.model_runner.mambaish_config is not None
875	        ):
876	            self._mamba_verify_update(
877	                batch, res, logits_output, spec_info, seq_lens_pre_verify
878	            )
879	
880	        # Allocate sparse k1/k2 slots for MiniCPM-SALA (InfLLM-v2 sparse attention)
881	        self._alloc_sparse_for_new_positions(batch, seq_lens_pre_verify_cpu)
882	
883	        if batch.return_logprob:
884	            add_output_logprobs_for_spec_v1(batch, res, logits_output)
885	
886	        # Prepare the batch for the next draft forwards.
887	        batch.forward_mode = (
888	            ForwardMode.DECODE if not batch.forward_mode.is_idle() else ForwardMode.IDLE
889	        )
890	        batch.spec_info = res.draft_input
891	
892	        return logits_output, res, model_worker_batch, can_run_cuda_graph
893	
894	    def _mamba_verify_update(
895	        self,
896	        batch: ScheduleBatch,
897	        res: EagleVerifyOutput,
898	        logits_output: LogitsProcessorOutput,
899	        spec_info: EagleVerifyInput,
900	        seq_lens_pre_verify: torch.Tensor,
901	    ):
902	        accepted_length = (
903	            torch.tensor(
904	                res.accept_length_per_req_cpu,
905	                device=logits_output.hidden_states.device,
906	                dtype=torch.int64,
907	            )
908	            + 1
909	        )
910	        cumulative_accepted_lengths = torch.cumsum(accepted_length, dim=0)
911	        # prepend 0 to the cumulative_accepted_lengths
912	        accepted_indices_start = torch.cat(
913	            [
914	                torch.zeros(
915	                    1,
916	                    dtype=cumulative_accepted_lengths.dtype,
917	                    device=cumulative_accepted_lengths.device,
918	                ),
919	                cumulative_accepted_lengths[:-1],
920	            ]
921	        )
922	        accepted_indices_offset = torch.arange(
923	            0,
924	            len(batch.seq_lens) * batch.spec_info.draft_token_num,
925	            step=batch.spec_info.draft_token_num,
926	            dtype=accepted_indices_start.dtype,
927	            device=accepted_indices_start.device,
928	        )
929	
930	        # If topk > 1, we need to use retrieve_next_token and retrieve_next_sibling to handle the eagle tree custom attention mask
931	        # res.accepted_indices.shape[0] > 0 skips DP attn idle batch
932	        if spec_info.topk > 1 and res.accepted_indices.shape[0] > 0:
933	            # accepted_indices=[0,2,3,4,5,7,9,10,11], accepted_length=[4, 3, 2], cumulative_accepted_lengths=[4, 7, 9]
934	            # first_token_indices_per_req=prepend(0, accepted_indices[cumulative_accepted_lengths[:-1]]) = [0, 5, 10]
935	            # last_token_indices_per_req=accepted_indices[cumulative_accepted_lengths - 1] = [4, 9, 11] (last token ID of each req)
936	            # max_relative_indices_per_req = [4,4,1]; those are the per-req spec-decoding step offsets that contain the correct mamba caches
937	            # first_token_indices_per_req = res.accepted_indices[accepted_indices_start]
938	            accepted_steps = (
939	                res.accepted_indices[cumulative_accepted_lengths - 1]
940	                - accepted_indices_offset
941	            )

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在看看 spec_info 的 verify 和 prepare_for_verify 方法：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def prepare_for_verify\\|def verify\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py | head -30"
}
```

> TOOL

tool_result Bash
```
134:    def prepare_for_verify(self, batch: ScheduleBatch, page_size: int):
246:    def verify(
1110:    def prepare_for_verify(self, batch: ScheduleBatch):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 134,
  "limit": 120
}
```

> TOOL

tool_result Read
```
134	    def prepare_for_verify(self, batch: ScheduleBatch, page_size: int):
135	
136	        if batch.forward_mode.is_idle():
137	            return
138	
139	        batch.input_ids = self.draft_token
140	
141	        if page_size == 1:
142	            batch.out_cache_loc = alloc_token_slots(
143	                batch.tree_cache,
144	                len(batch.input_ids),
145	            )
146	            end_offset = batch.seq_lens + self.draft_token_num
147	        else:
148	            prefix_lens = batch.seq_lens
149	            prefix_lens_cpu = batch.seq_lens_cpu
150	            end_offset = prefix_lens + self.draft_token_num
151	            end_offset_cpu = prefix_lens_cpu + self.draft_token_num
152	            last_loc = get_last_loc(
153	                batch.req_to_token_pool.req_to_token,
154	                batch.req_pool_indices,
155	                prefix_lens,
156	            )
157	            batch.out_cache_loc = alloc_paged_token_slots_extend(
158	                batch.tree_cache,
159	                prefix_lens,
160	                prefix_lens_cpu,
161	                end_offset,
162	                end_offset_cpu,
163	                last_loc,
164	                len(batch.input_ids),
165	            )
166	            self.last_loc = last_loc
167	
168	        bs = batch.batch_size()
169	        assign_req_to_token_pool_func(
170	            batch.req_pool_indices,
171	            batch.req_to_token_pool.req_to_token,
172	            batch.seq_lens,
173	            end_offset,
174	            batch.out_cache_loc,
175	            bs,
176	        )
177	
178	        if get_global_server_args().enable_mamba_extra_buffer():
179	            batch.mamba_track_indices = torch.tensor(
180	                [
181	                    req.mamba_ping_pong_track_buffer[req.mamba_next_track_idx]
182	                    for req in batch.reqs
183	                ],
184	                dtype=torch.int64,
185	                device=batch.device,
186	            )
187	
188	    def generate_attn_arg_prefill(
189	        self,
190	        req_pool_indices: torch.Tensor,
191	        paged_kernel_lens: torch.Tensor,
192	        paged_kernel_lens_sum: int,
193	        req_to_token: torch.Tensor,
194	    ):
195	        device = req_pool_indices.device
196	        batch_size = len(req_pool_indices)
197	        qo_indptr = torch.arange(
198	            0,
199	            (1 + batch_size) * self.draft_token_num,
200	            step=self.draft_token_num,
201	            dtype=torch.int32,
202	            device=device,
203	        )
204	        cum_kv_seq_len = torch.zeros(
205	            (batch_size + 1,), dtype=torch.int32, device=device
206	        )
207	
208	        paged_kernel_lens = paged_kernel_lens + self.draft_token_num
209	        cum_kv_seq_len[1:] = torch.cumsum(paged_kernel_lens, dim=0)
210	
211	        kv_indices = torch.empty(
212	            paged_kernel_lens_sum + self.draft_token_num * batch_size,
213	            dtype=torch.int32,
214	            device=device,
215	        )
216	        create_flashinfer_kv_indices_triton[(batch_size,)](
217	            req_to_token,
218	            req_pool_indices,
219	            paged_kernel_lens,
220	            cum_kv_seq_len,
221	            None,
222	            kv_indices,
223	            req_to_token.size(1),
224	        )
225	        mask_numel = (
226	            paged_kernel_lens_sum * self.draft_token_num
227	            + (self.draft_token_num**2) * batch_size
228	        )
229	        if self.custom_mask.numel() < mask_numel:
230	            # FIXME(attn): temporary fix for custom mask padding with cuda graph
231	            self.custom_mask = torch.cat(
232	                [
233	                    self.custom_mask,
234	                    torch.full(
235	                        (mask_numel - self.custom_mask.numel(),),
236	                        True,
237	                        dtype=torch.bool,
238	                        device=device,
239	                    ),
240	                ],
241	                dim=0,
242	            )
243	
244	        return kv_indices, cum_kv_seq_len, qo_indptr, self.custom_mask
245	
246	    def verify(
247	        self,
248	        batch: ScheduleBatch,
249	        logits_output: LogitsProcessorOutput,
250	        token_to_kv_pool_allocator: BaseTokenToKVPoolAllocator,
251	        page_size: int,
252	        vocab_mask: Optional[torch.Tensor] = None,  # For grammar
253	    ) -> torch.Tensor:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 scheduler 中如何拿到 running batch 的 size 和是否可能在 forward 之前做某种开关：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py",
  "offset": 2216,
  "limit": 100
}
```

> TOOL

tool_result Read
```
2216	
2217	        # Run forward
2218	        if self.is_generation:
2219	            if self.spec_algorithm.is_none() or self.enable_overlap:
2220	                # In most cases, we use the model worker batch to run the forward.
2221	                worker_batch_or_batch = batch.get_model_worker_batch()
2222	            else:
2223	                # In speculative decoding v1 (non-overlap) case, we use the batch directly.
2224	                # TODO(lsyin): delete this branch after unifying the abstraction.
2225	                worker_batch_or_batch = batch
2226	
2227	            if self.enable_overlap:
2228	                model_worker_batch = worker_batch_or_batch
2229	                self.record_batch_in_overlap(model_worker_batch)
2230	
2231	                # Sampling info will be modified during forward, so we store a copy.
2232	                model_worker_batch.sampling_info = (
2233	                    model_worker_batch.sampling_info.copy_for_forward()
2234	                )
2235	
2236	                bs = len(model_worker_batch.seq_lens)
2237	                future_indices = self.future_map.alloc_future_indices(bs)
2238	
2239	                with self.forward_stream_ctx:
2240	                    self.forward_stream.wait_stream(self.default_stream)
2241	                    self.future_map.resolve_future(model_worker_batch)
2242	                    with self.record_forward_metrics(batch):
2243	                        batch_result = self.model_worker.forward_batch_generation(
2244	                            model_worker_batch
2245	                            # here pp is not compatible with overlap
2246	                        )
2247	                    # FIXME(lsyin): maybe move this to forward_batch_generation
2248	                    batch_result.copy_done = self.device_module.Event()
2249	                    if batch_result.delay_sample_func is None:
2250	                        self.future_map.store_to_map(future_indices, batch_result)
2251	                        batch_result.copy_to_cpu(return_logprob=batch.return_logprob)
2252	                    else:
2253	                        batch_result.future_indices = future_indices
2254	
2255	                # FIXME(lsyin): move this assignment elsewhere
2256	                future_indices_or_next_token_ids = -future_indices.indices
2257	
2258	                if batch.is_spec_v2:
2259	                    # FIXME(lsyin): tmp code for spec v2
2260	                    # We only keep future indices for next draft input
2261	
2262	                    batch.spec_info = batch_result.next_draft_input
2263	                    batch.spec_info.future_indices = future_indices
2264	
2265	                    # batch.spec_info = EagleDraftInput(
2266	                    #     future_indices=future_indices,
2267	                    #     verify_done=batch_result.next_draft_input.verify_done,
2268	                    # )
2269	
2270	                    # The future value, usually for next batch preparation
2271	                    # Current implementation strictly synchronizes the seq_lens
2272	                    batch.seq_lens = batch_result.next_draft_input.new_seq_lens
2273	            elif self.enable_pdmux and batch.forward_mode.is_split_prefill():
2274	                batch_result = self.tp_worker.forward_batch_split_prefill(batch)
2275	                future_indices_or_next_token_ids = batch_result.next_token_ids
2276	            else:
2277	                kwargs = (
2278	                    {"pp_proxy_tensors": pp_proxy_tensors}
2279	                    if self.spec_algorithm.is_none()
2280	                    else {}
2281	                )
2282	                with self.record_forward_metrics(batch):
2283	                    batch_result = self.model_worker.forward_batch_generation(
2284	                        worker_batch_or_batch, **kwargs
2285	                    )
2286	                future_indices_or_next_token_ids = batch_result.next_token_ids
2287	                self.update_cache_from_scheduler(batch, batch_result)
2288	
2289	            # NOTE: future_indices_or_next_token_ids is used in ScheduleBatch,
2290	            #       which can probably be replaced by future_indices later [TODO(lsyin)].
2291	            #       we shall still keep the original outputs, e.g. next_token_ids
2292	            #       in the GenerationBatchOutput for processing after copy_done.
2293	            batch.output_ids = future_indices_or_next_token_ids
2294	
2295	            # These 2 values are needed for processing the output, but the values can be
2296	            # modified by overlap schedule. So we have to copy them here so that
2297	            # we can use the correct values in output processing.
2298	            if batch.return_logprob:
2299	                batch_result.extend_input_len_per_req = [
2300	                    req.extend_input_len for req in batch.reqs
2301	                ]
2302	                batch_result.extend_logprob_start_len_per_req = [
2303	                    req.extend_logprob_start_len for req in batch.reqs
2304	                ]
2305	            else:
2306	                batch_result.extend_input_len_per_req = None
2307	                batch_result.extend_logprob_start_len_per_req = None
2308	
2309	            ret = batch_result
2310	        else:  # embedding or reward model
2311	            model_worker_batch = batch.get_model_worker_batch()
2312	
2313	            if self.enable_overlap:
2314	                self.record_batch_in_overlap(model_worker_batch)
2315	                with self.forward_stream_ctx:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在检查是否有 fallback 或者禁用 spec 的路径：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"spec_algorithm.is_none\\|enable_overlap\\|forward_batch_generation\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -50"
}
```

> TOOL

tool_result Bash
```
285:        self.enable_overlap = not server_args.disable_overlap_schedule
506:            if self.enable_overlap:
536:                enable_overlap=self.enable_overlap
550:        if self.spec_algorithm.is_none():
724:            if self.spec_algorithm.is_none()
868:        elif self.spec_algorithm.supports_spec_v2() and self.enable_overlap:
1007:        if not self.enable_overlap:
1844:        if need_mlp_sync and not self.spec_algorithm.is_none():
2071:            self.enable_overlap,
2219:            if self.spec_algorithm.is_none() or self.enable_overlap:
2227:            if self.enable_overlap:
2243:                        batch_result = self.model_worker.forward_batch_generation(
2247:                    # FIXME(lsyin): maybe move this to forward_batch_generation
2279:                    if self.spec_algorithm.is_none()
2283:                    batch_result = self.model_worker.forward_batch_generation(
2313:            if self.enable_overlap:
2338:        # unifying the forward_batch_generation interface (related to spec V2).
2464:            and (not self.enable_overlap or len(self.result_queue) == 0)
2520:        if not self.spec_algorithm.is_none() and self.spec_total_num_forward_ct > 0:
2559:            if not self.spec_algorithm.is_none() and self.spec_total_num_forward_ct > 0:
2686:        if self.enable_overlap and self.last_batch:
2973:            elif scheduler.enable_overlap:
2980:            elif scheduler.enable_overlap:
2988:            elif scheduler.enable_overlap:
```

> AGENT

现在看看 spec_info 中是否能动态调整参数或者有 disable 的方式：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class SpeculativeAlgorithm\\|is_none\\|supports_spec\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_info.py | head -40"
}
```

> TOOL

tool_result Bash
```
14:class SpeculativeAlgorithm(Enum):
33:    def is_none(self) -> bool:
52:    def supports_spec_v2(self) -> bool:
58:        if self.is_none():
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_info.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	from abc import ABC, abstractmethod
4	from enum import Enum, IntEnum, auto
5	from typing import TYPE_CHECKING, List, Optional, Tuple, Type, Union
6	
7	if TYPE_CHECKING:
8	    from sglang.srt.managers.schedule_batch import ModelWorkerBatch
9	    from sglang.srt.managers.tp_worker import TpModelWorker
10	    from sglang.srt.speculative.base_spec_worker import BaseSpecWorker
11	    from sglang.srt.speculative.ngram_worker import NGRAMWorker
12	
13	
14	class SpeculativeAlgorithm(Enum):
15	    """Enumeration of speculative decoding algorithms."""
16	
17	    EAGLE = auto()
18	    EAGLE3 = auto()
19	    STANDALONE = auto()
20	    NGRAM = auto()
21	    MEDUSA = auto()
22	    NONE = auto()
23	
24	    @classmethod
25	    def from_string(cls, name: Optional[str]) -> SpeculativeAlgorithm:
26	        if name is None:
27	            return cls.NONE
28	        try:
29	            return cls[name.upper()]
30	        except KeyError:
31	            raise ValueError(f"Unknown speculative algorithm name: {name}")
32	
33	    def is_none(self) -> bool:
34	        return self == SpeculativeAlgorithm.NONE
35	
36	    def is_medusa(self) -> bool:
37	        return self == SpeculativeAlgorithm.MEDUSA
38	
39	    def is_eagle(self) -> bool:
40	        # NOTE: EAGLE3 is a variant of EAGLE
41	        return self == SpeculativeAlgorithm.EAGLE or self == SpeculativeAlgorithm.EAGLE3
42	
43	    def is_eagle3(self) -> bool:
44	        return self == SpeculativeAlgorithm.EAGLE3
45	
46	    def is_standalone(self) -> bool:
47	        return self == SpeculativeAlgorithm.STANDALONE
48	
49	    def is_ngram(self) -> bool:
50	        return self == SpeculativeAlgorithm.NGRAM
51	
52	    def supports_spec_v2(self) -> bool:
53	        return self.is_eagle() or self.is_standalone()
54	
55	    def create_worker(
56	        self, enable_overlap: bool = False
57	    ) -> Optional[Union[Type[BaseSpecWorker], Type[TpModelWorker], Type[NGRAMWorker]]]:
58	        if self.is_none():
59	            return None
60	
61	        if self.is_eagle():
62	            if enable_overlap:
63	                from sglang.srt.speculative.eagle_worker_v2 import EAGLEWorkerV2
64	
65	                return EAGLEWorkerV2
66	
67	            from sglang.srt.speculative.eagle_worker import EAGLEWorker
68	
69	            return EAGLEWorker
70	        elif self.is_standalone():
71	            if enable_overlap:
72	                from sglang.srt.speculative.standalone_worker_v2 import (
73	                    StandaloneWorkerV2,
74	                )
75	
76	                return StandaloneWorkerV2
77	
78	            from sglang.srt.speculative.standalone_worker import StandaloneWorker
79	
80	            return StandaloneWorker
81	        elif self.is_medusa():
82	            if enable_overlap:
83	                raise ValueError(
84	                    f"Speculative algorithm {self.name} does not support overlap worker creation."
85	                )
86	
87	            from sglang.srt.speculative.medusa_worker import MedusaWorker
88	
89	            return MedusaWorker
90	        elif self.is_ngram():
91	            if enable_overlap:
92	                raise ValueError(
93	                    f"Speculative algorithm {self.name} does not support overlap worker creation."
94	                )
95	
96	            from sglang.srt.speculative.ngram_worker import NGRAMWorker
97	
98	            return NGRAMWorker
99	
100	        raise ValueError("Unreachable code path in create_worker.")

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 eagle_worker_v2 和 overlap 路径的差别：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py",
  "offset": 616,
  "limit": 100
}
```

> TOOL

tool_result Read
```
616	    def forward_batch_generation(self, model_worker_batch: ModelWorkerBatch):
617	        if (
618	            model_worker_batch.forward_mode.is_extend()
619	            or model_worker_batch.is_extend_in_batch
620	        ):
621	            # Target prefill
622	            model_worker_batch.capture_hidden_mode = CaptureHiddenMode.FULL
623	            batch_output = self.target_worker.forward_batch_generation(
624	                model_worker_batch
625	            )
626	
627	            # Draft prefill
628	            model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
629	            with speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
630	                batch_output.next_draft_input = (
631	                    self.draft_worker._draft_extend_for_prefill(
632	                        model_worker_batch,
633	                        batch_output.logits_output.hidden_states,
634	                        batch_output.next_token_ids,
635	                    )
636	                )
637	                return batch_output
638	        else:
639	            if model_worker_batch.spec_info is None:
640	                model_worker_batch.spec_info = EagleDraftInput.create_idle_input(
641	                    device=self.device,
642	                    hidden_size=self.target_worker.model_config.hidden_size,
643	                    dtype=self.target_worker.model_config.dtype,
644	                    topk=self.topk,
645	                    capture_hidden_mode=CaptureHiddenMode.LAST,
646	                )
647	            with speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
648	                verify_input: EagleVerifyInput = self.draft_worker.draft(
649	                    model_worker_batch
650	                )
651	            assert verify_input.is_verify_input()
652	            model_worker_batch.spec_info = verify_input
653	            batch_output = self.verify(model_worker_batch)
654	            with speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
655	                self.draft_worker._draft_extend_for_decode(
656	                    model_worker_batch, batch_output
657	                )
658	            return batch_output
659	
660	    def verify(self, batch: ModelWorkerBatch):
661	        # Since batch.seq_lens is allocated in another stream, we need
662	        # record_stream() to prevent pytorch gc and reuse the gpu memory
663	        # while forward_stream is still running.
664	        batch.seq_lens.record_stream(
665	            torch.get_device_module(self.device).current_stream()
666	        )
667	
668	        # Parse args
669	        verify_input: EagleVerifyInput = batch.spec_info
670	        verify_input.num_tokens_per_batch = self.speculative_num_steps + 1
671	        bs = len(batch.seq_lens)
672	
673	        # Batch 1: Target verify
674	        # Prepare for target verify in a separate stream
675	        with self.plan_stream_ctx:
676	            verify_forward_batch, can_run_cuda_graph = (
677	                verify_input.prepare_for_v2_verify(
678	                    self.req_to_token_pool,
679	                    batch,
680	                    self.target_worker,
681	                )
682	            )
683	
684	        # Correct some buffers due to the overlap plan
685	        if self.plan_stream:
686	            torch.get_device_module(self.device).current_stream().wait_stream(
687	                self.plan_stream
688	            )
689	
690	            # Some values such as custom_mask and position depend on the output of draft,
691	            # so the previous plan step used the wrong values. Here, we need to run the related
692	            # computation again to update them to the correct values.
693	            self.target_worker.model_runner.attn_backend.update_verify_buffers_to_fill_after_draft(
694	                verify_input,
695	                (
696	                    self.target_worker.model_runner.graph_runner.bs
697	                    if can_run_cuda_graph
698	                    else None
699	                ),
700	            )
701	
702	        # Prepare grammar data on CPU if needed
703	        if batch.has_grammar:
704	            retrieve_next_token_cpu = verify_input.retrive_next_token.cpu()
705	            retrieve_next_sibling_cpu = verify_input.retrive_next_sibling.cpu()
706	            draft_tokens_cpu = verify_input.draft_token.view(
707	                verify_input.retrive_next_token.shape
708	            ).cpu()
709	
710	        # Run target verify batch in the main compute stream (GPU compute)
711	        forward_batch_output = self.target_worker.forward_batch_generation(
712	            model_worker_batch=None,
713	            forward_batch=verify_forward_batch,
714	            is_verify=True,
715	            skip_attn_backend_init=True,

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看如何在 eagle_worker.py 中传递和使用 dtn：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"speculative_num_draft_tokens\\|num_draft_token\\|dtn\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -60"
}
```

> TOOL

tool_result Bash
```
156:        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
647:                self.speculative_num_draft_tokens,
666:            self.speculative_num_draft_tokens,
710:            draft_token_num=self.server_args.speculative_num_draft_tokens,
783:            score_list, token_list, parents_list, self.speculative_num_draft_tokens
```

> AGENT

现在检查 CUDA graph 与 dtn 的关系：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"cuda_graph\\|graph_runner\\|num_verify_tokens\\|capture.*graph\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -80"
}
```

> TOOL

tool_result Bash
```
9:from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
36:from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
39:from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
169:        # Do not capture cuda graph in `super().__init__()`
171:        backup_disable_cuda_graph = server_args.disable_cuda_graph
172:        server_args.disable_cuda_graph = True
259:        self.draft_model_runner.server_args.disable_cuda_graph = (
260:            backup_disable_cuda_graph
278:            self.init_cuda_graphs()
305:    def init_cuda_graphs(self):
307:        self.cuda_graph_runner = None
308:        self.cuda_graph_runner_for_draft_extend = None
310:        if self.server_args.disable_cuda_graph:
324:            self.cuda_graph_runner = Device2DraftCudaGraphRunner[
339:            self.cuda_graph_runner_for_draft_extend = EAGLEDraftExtendCudaGraphRunner(
377:                can_run_cuda_graph=False,
384:            logits_output, verify_output, model_worker_batch, can_run_cuda_graph = (
405:                can_run_cuda_graph=can_run_cuda_graph,
623:        can_cuda_graph = self.cuda_graph_runner and self.cuda_graph_runner.can_run(
626:        if can_cuda_graph:
627:            parent_list, top_scores_index, draft_tokens = self.cuda_graph_runner.replay(
631:            forward_batch.can_run_dp_cuda_graph = False
829:        logits_output, can_run_cuda_graph = (
831:            batch_result.can_run_cuda_graph,
892:        return logits_output, res, model_worker_batch, can_run_cuda_graph
1157:        can_cuda_graph = (
1158:            self.cuda_graph_runner_for_draft_extend
1159:            and self.cuda_graph_runner_for_draft_extend.can_run(forward_batch)
1161:        if can_cuda_graph:
1162:            logits_output = self.cuda_graph_runner_for_draft_extend.replay(
1171:            forward_batch.can_run_dp_cuda_graph = False
```

> AGENT

现在查看 CUDA graph runner 的实现细节：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class.*CudaGraphRunner\\|def __init__\\|def can_run\\|def replay\\|def capture\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py | head -60"
}
```

> TOOL

tool_result Bash
```
37:class EAGLEDraftCudaGraphRunner:
38:    def __init__(self, eagle_worker: EAGLEWorker):
139:    def can_run(self, forward_batch: ForwardBatch):
178:    def capture(self):
181:    def capture_one_batch_size(
319:    def replay(self, forward_batch: ForwardBatch):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py",
  "offset": 37,
  "limit": 150
}
```

> TOOL

tool_result Read
```
37	class EAGLEDraftCudaGraphRunner:
38	    def __init__(self, eagle_worker: EAGLEWorker):
39	        # Parse args
40	        self.eagle_worker = eagle_worker
41	        if not hasattr(eagle_worker, "model_runner"):
42	            # V2: EagleDraftWorker
43	            self.model_runner = model_runner = eagle_worker.draft_runner
44	        else:
45	            self.model_runner = model_runner = eagle_worker.model_runner
46	        self.graphs = {}
47	        self.output_buffers = {}
48	        self.enable_torch_compile = model_runner.server_args.enable_torch_compile
49	        self.disable_padding = model_runner.server_args.disable_cuda_graph_padding
50	        self.require_gathered_buffer = require_gathered_buffer(model_runner.server_args)
51	        self.require_mlp_tp_gather = require_mlp_tp_gather(model_runner.server_args)
52	        self.require_mlp_sync = require_mlp_sync(model_runner.server_args)
53	        self.require_attn_tp_gather = require_attn_tp_gather(model_runner.server_args)
54	        self.tp_size = self.model_runner.tp_size
55	        self.dp_size = self.model_runner.dp_size
56	        self.speculative_num_steps = model_runner.server_args.speculative_num_steps
57	        self.topk = model_runner.server_args.speculative_eagle_topk
58	        self.enable_profile_cuda_graph = (
59	            model_runner.server_args.enable_profile_cuda_graph
60	        )
61	        self.enable_pdmux = False
62	        self.deepep_adapter = DeepEPCudaGraphRunnerAdapter()
63	
64	        # Batch sizes to capture
65	        self.capture_bs, self.compile_bs = get_batch_sizes_to_capture(model_runner)
66	
67	        # Attention backend
68	        self.num_tokens_per_bs = self.topk
69	        self.max_bs = max(self.capture_bs)
70	        self.max_num_token = self.max_bs * self.num_tokens_per_bs
71	
72	        self.model_runner.draft_attn_backend.init_cuda_graph_state(
73	            self.max_bs, self.max_num_token
74	        )
75	        self.seq_len_fill_value = self.model_runner.draft_attn_backend.attn_backends[
76	            0
77	        ].get_cuda_graph_seq_len_fill_value()
78	        self.seq_lens_cpu = torch.full(
79	            (self.max_bs,), self.seq_len_fill_value, dtype=torch.int32
80	        )
81	        self.extend_seq_lens_cpu = [self.seq_len_fill_value] * self.max_bs
82	
83	        if self.enable_torch_compile:
84	            set_torch_compile_config()
85	
86	        # Graph inputs
87	        with torch.device(model_runner.device):
88	            self.input_ids = torch.zeros((self.max_num_token,), dtype=torch.int64)
89	            self.req_pool_indices = torch.zeros((self.max_bs,), dtype=torch.int32)
90	            self.out_cache_loc = torch.zeros(
91	                (self.max_num_token * self.speculative_num_steps,),
92	                dtype=self._cache_loc_dtype(),
93	            )
94	            self.positions = torch.zeros((self.max_num_token,), dtype=torch.int64)
95	            self.mrope_positions = torch.zeros(
96	                (3, self.max_num_token), dtype=torch.int64
97	            )
98	            self.seq_lens = torch.full(
99	                (self.max_bs,), self.seq_len_fill_value, dtype=torch.int32
100	            )
101	            self.extend_seq_lens = torch.ones((self.max_bs,), dtype=torch.int32)
102	            self.topk_p = torch.zeros((self.max_bs, self.topk), dtype=torch.float32)
103	            self.topk_index = torch.zeros((self.max_bs, self.topk), dtype=torch.int64)
104	            self.hidden_states = torch.zeros(
105	                (self.max_bs, self.model_runner.model_config.hidden_size),
106	                dtype=self.model_runner.dtype,
107	            )
108	
109	            if self.require_gathered_buffer:
110	                if self.require_mlp_tp_gather:
111	                    self.global_num_tokens_gpu = torch.zeros(
112	                        (self.dp_size,), dtype=torch.int32
113	                    )
114	                    self.global_num_tokens_for_logprob_gpu = torch.zeros(
115	                        (self.dp_size,), dtype=torch.int32
116	                    )
117	                else:
118	                    assert self.require_attn_tp_gather
119	                    self.global_num_tokens_gpu = torch.zeros((1,), dtype=torch.int32)
120	                    self.global_num_tokens_for_logprob_gpu = torch.zeros(
121	                        (1,), dtype=torch.int32
122	                    )
123	            else:
124	                self.global_num_tokens_gpu = None
125	                self.global_num_tokens_for_logprob_gpu = None
126	
127	        # Capture
128	        try:
129	            with model_capture_mode():
130	                self.capture()
131	        except RuntimeError as e:
132	            raise Exception(
133	                f"Capture cuda graph failed: {e}\n{CUDA_GRAPH_CAPTURE_FAILED_MSG}"
134	            )
135	
136	    def _cache_loc_dtype(self):
137	        return torch.int64
138	
139	    def can_run(self, forward_batch: ForwardBatch):
140	        if self.require_mlp_tp_gather:
141	            cuda_graph_bs = (
142	                max(forward_batch.global_num_tokens_cpu) // self.num_tokens_per_bs
143	                if self.model_runner.spec_algorithm.is_eagle()
144	                or self.model_runner.spec_algorithm.is_standalone()
145	                else max(forward_batch.global_num_tokens_cpu)
146	            )
147	        else:
148	            cuda_graph_bs = forward_batch.batch_size
149	
150	        is_bs_supported = (
151	            cuda_graph_bs in self.graphs
152	            if self.disable_padding
153	            else cuda_graph_bs <= self.max_bs
154	        )
155	
156	        if self.require_mlp_sync:
157	            is_bs_supported = is_bs_supported and forward_batch.can_run_dp_cuda_graph
158	
159	        return is_bs_supported
160	
161	    def _create_graph(self):
162	        return torch.cuda.CUDAGraph()
163	
164	    def _capture_init(self, run_once_fn):
165	        for _ in range(2):
166	            torch.cuda.synchronize()
167	            self.model_runner.tp_group.barrier()
168	            run_once_fn()
169	
170	    def _capture_graph(self, graph, pool, stream, run_once_fn):
171	        with torch.cuda.graph(graph, pool=pool, stream=stream):
172	            out = run_once_fn()
173	        return out
174	
175	    def _replay(self, forward_batch: ForwardBatch):
176	        self.graphs[self.bs].replay()
177	
178	    def capture(self):
179	        CudaGraphRunner.capture(self)
180	
181	    def capture_one_batch_size(
182	        self, num_seqs: int, forward: Callable, stream_idx: int = 0
183	    ):
184	        graph = self._create_graph()
185	        stream = self.stream
186	        num_tokens = num_seqs * self.num_tokens_per_bs

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在查看 target worker 的 forward_batch_generation 是否有 no-spec 的路径：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def forward_batch_generation\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/tp_worker.py 2>/dev/null | head -10"
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
  "command": "find /user_4813494d/openbmb/demo-sala -name \"tp_worker.py\" -exec grep -l \"forward_batch_generation\" {} \\;"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/tp_worker.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def forward_batch_generation\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/tp_worker.py"
}
```

> TOOL

tool_result Bash
```
60:    def forward_batch_generation(self, forward_batch: ForwardBatch):
423:    def forward_batch_generation(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/tp_worker.py",
  "offset": 423,
  "limit": 100
}
```

> TOOL

tool_result Read
```
423	    def forward_batch_generation(
424	        self,
425	        model_worker_batch: ModelWorkerBatch,
426	        forward_batch: Optional[ForwardBatch] = None,
427	        pp_proxy_tensors: Optional[PPProxyTensors] = None,
428	        is_verify: bool = False,
429	        skip_attn_backend_init=False,
430	    ) -> GenerationBatchResult:
431	        # FIXME(lsyin): maybe remove skip_attn_backend_init in forward_batch_generation,
432	        #               which requires preparing replay to always be in this function
433	
434	        # Get forward batch from model worker batch
435	        if model_worker_batch is not None:
436	            # update the consumer index of hicache to the running batch
437	            self.set_hicache_consumer(model_worker_batch.hicache_consumer_index)
438	
439	            forward_batch = ForwardBatch.init_new(model_worker_batch, self.model_runner)
440	        else:
441	            # FIXME(lsyin): unify the interface of forward_batch
442	            assert forward_batch is not None
443	
444	        if self.is_dllm():
445	            return self._forward_batch_generation_dllm(forward_batch)
446	
447	        if self.pp_group.is_last_rank:
448	            out = self.model_runner.forward(
449	                forward_batch,
450	                pp_proxy_tensors=pp_proxy_tensors,
451	                skip_attn_backend_init=skip_attn_backend_init,
452	            )
453	            logits_output, can_run_cuda_graph = out.logits_output, out.can_run_graph
454	            batch_result = GenerationBatchResult(
455	                logits_output=logits_output,
456	                can_run_cuda_graph=can_run_cuda_graph,
457	                expert_distribution_metrics=out.expert_distribution_metrics,
458	            )
459	
460	            if is_verify:
461	                # Skip sampling and return logits for target forward
462	                return batch_result
463	
464	            if (
465	                self.enable_overlap
466	                and not self.enable_spec
467	                and model_worker_batch.sampling_info.grammars is not None
468	            ):
469	
470	                def sample_batch_func():
471	                    batch_result.next_token_ids = self.model_runner.sample(
472	                        logits_output, forward_batch
473	                    )
474	                    return batch_result
475	
476	                batch_result.delay_sample_func = sample_batch_func
477	                return batch_result
478	
479	            if not model_worker_batch.is_prefill_only:
480	                # For normal requests, sample the next token ids.
481	                batch_result.next_token_ids = self.model_runner.sample(
482	                    logits_output, forward_batch
483	                )
484	            else:
485	                # For prefill-only requests, create dummy token IDs on CPU
486	                # The size should match the batch size (number of sequences), not total tokens
487	                batch_result.next_token_ids = torch.zeros(
488	                    len(model_worker_batch.seq_lens),
489	                    dtype=torch.long,
490	                    device=model_worker_batch.input_ids.device,
491	                )
492	                if (
493	                    model_worker_batch.return_logprob
494	                    and logits_output.next_token_logits is not None
495	                ):
496	                    # NOTE: Compute logprobs without full sampling
497	                    self.model_runner.compute_logprobs_only(
498	                        logits_output, model_worker_batch
499	                    )
500	
501	            return batch_result
502	        else:
503	            out = self.model_runner.forward(
504	                forward_batch,
505	                pp_proxy_tensors=pp_proxy_tensors,
506	                skip_attn_backend_init=skip_attn_backend_init,
507	            )
508	            pp_proxy_tensors, can_run_cuda_graph = out.logits_output, out.can_run_graph
509	            return GenerationBatchResult(
510	                pp_hidden_states_proxy_tensors=pp_proxy_tensors,
511	                can_run_cuda_graph=can_run_cuda_graph,
512	                expert_distribution_metrics=out.expert_distribution_metrics,
513	            )
514	
515	    def forward_batch_split_prefill(self, batch: ScheduleBatch):
516	        if batch.split_index == 0:
517	            model_worker_batch = batch.get_model_worker_batch()
518	            forward_batch = ForwardBatch.init_new(model_worker_batch, self.model_runner)
519	            batch.split_forward_batch = forward_batch
520	            batch.seq_lens_cpu_cache = model_worker_batch.seq_lens_cpu
521	        else:
522	            model_worker_batch = batch.get_model_worker_batch(batch.seq_lens_cpu_cache)

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

现在整理关键信息。让我再看一下 running_batch 何时被更新和它在多个地方的可见性：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"running_batch.batch_size()\\|len(self.running_batch.reqs)\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -20"
}
```

> TOOL

tool_result Bash
```
1907:        running_bs = len(self.running_batch.reqs)
1982:            running_bs = len(self.running_batch.reqs)
2051:                running_bs=len(self.running_batch.reqs),
2502:                f"#running-req: {len(self.running_batch.reqs)}"
2706:            if len(self.running_batch.reqs) != 0:
```

> AGENT

现在让我检查 spec_info 中是否有 per-step 动态读取参数的机制：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"spec_steps\\|topk\\|draft_token_num\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py | head -100"
}
```

> TOOL

tool_result Bash
```
93:    spec_steps: int
94:    topk: int
95:    draft_token_num: int
108:        return self.draft_token_num, self.draft_token_num
111:    def create_idle_input(cls, topk: int, spec_steps: int, num_verify_tokens: int):
126:            topk=topk,
127:            draft_token_num=num_verify_tokens,
128:            spec_steps=spec_steps,
146:            end_offset = batch.seq_lens + self.draft_token_num
150:            end_offset = prefix_lens + self.draft_token_num
151:            end_offset_cpu = prefix_lens_cpu + self.draft_token_num
199:            (1 + batch_size) * self.draft_token_num,
200:            step=self.draft_token_num,
208:        paged_kernel_lens = paged_kernel_lens + self.draft_token_num
212:            paged_kernel_lens_sum + self.draft_token_num * batch_size,
226:            paged_kernel_lens_sum * self.draft_token_num
227:            + (self.draft_token_num**2) * batch_size
270:                    topk=self.topk,
277:                    (0, self.spec_steps + 1),
285:        candidates = self.draft_token.reshape(bs, self.draft_token_num)
292:            (bs, self.spec_steps + 1), -1, dtype=torch.int32, device=batch.device
306:                num_tokens_in_batch=self.draft_token_num,
322:                torch.repeat_interleave(linear_penalty, self.draft_token_num, dim=0)
347:                top2 = torch.topk(logits_output.next_token_logits, 2, dim=-1)
348:                target_predict = top2.indices[..., 0].reshape(bs, self.draft_token_num)
349:                top2_token = top2.indices[..., 1].reshape(bs, self.draft_token_num).contiguous()
354:                top2_ratio = ratio.reshape(bs, self.draft_token_num).contiguous().float()
357:                target_predict = target_predict.reshape(bs, self.draft_token_num)
370:                topk=self.topk,
379:                sampling_info.temperatures, self.draft_token_num, dim=0
380:            )  # (bs * draft_token_num, 1)
384:            )  # (bs * draft_token_num, vocab_size)
388:                    sampling_info.top_ks, self.draft_token_num, dim=0
390:            )  # (bs * draft_token_num, vocab_size)
395:                        sampling_info.top_ps, self.draft_token_num, dim=0
398:            target_probs = target_probs.reshape(bs, self.draft_token_num, -1)
436:                spec_steps=self.spec_steps,
446:                dtn = self.draft_token_num
448:                _tr_top2_v, _tr_top2_i = torch.topk(_tr_logits_v, 2, dim=-1)
469:                        "topk": int(self.topk),
470:                        "spec_steps": int(self.spec_steps),
584:            if self.topk == 1:
590:                    self.draft_token_num,
591:                    next_power_of_2(self.draft_token_num),
605:                    self.draft_token_num,
629:                    self.draft_token_num,
630:                    next_power_of_2(self.draft_token_num),
645:                if page_size == 1 or self.topk == 1:
679:            if page_size == 1 or self.topk == 1:
699:                if page_size == 1 or self.topk == 1:
719:                        next_power_of_2(self.draft_token_num),
741:                    topk=self.topk,
760:    # shape: (b, topk)
761:    topk_p: torch.Tensor = None
762:    topk_index: torch.Tensor = None
822:        topk: int,
828:            topk_p=torch.empty((0, topk), device=device, dtype=torch.float32),
829:            topk_index=torch.empty((0, topk), device=device, dtype=torch.int64),
997:        if self.topk_p is None:
1016:            error_msg = f"length of new_indices: {len(new_indices)} != length of topk_p: {len(self.topk_p)}, this should not happen"
1017:            if len(new_indices) != len(self.topk_p):
1023:            self.topk_p = self.topk_p[: len(new_indices)]
1024:            self.topk_index = self.topk_index[: len(new_indices)]
1029:            self.topk_p = self.topk_p[new_indices]
1030:            self.topk_index = self.topk_index[new_indices]
1047:            self.topk_p = spec_info.topk_p
1048:            self.topk_index = spec_info.topk_index
1056:        self.topk_p = torch.cat([self.topk_p, spec_info.topk_p])
1057:        self.topk_index = torch.cat([self.topk_index, spec_info.topk_index])
1082:    draft_token: torch.Tensor  # (bs * draft_token_num,) flattened input_ids
1083:    positions: torch.Tensor  # (bs * draft_token_num,) position ids
1084:    draft_token_num: int  # K+1 (verified + K drafts)
1085:    topk: int = 1  # always 1 for flat Medusa (no tree)
1097:        return self.draft_token_num, self.draft_token_num
1100:    def create_idle_input(cls, draft_token_num: int):
1104:            draft_token_num=draft_token_num,
1118:        # Allocate KV cache slots for all draft_token_num tokens per request
1122:        end_offset = batch.seq_lens + self.draft_token_num
```

> AGENT

完美。现在我有足够的信息来生成报告。让我最后检查一个关键细节——是否有任何已有的 per-batch 或 per-request 的 spec 参数覆盖机制：

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"per_req\\|override\\|dynamic.*spec\\|batch.*spec.*config\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -30"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:203:            server_args.json_model_override_args = (
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:403:                num_accepted_tokens=sum(verify_output.accept_length_per_req_cpu),
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:404:                accept_length_per_req_cpu=verify_output.accept_length_per_req_cpu,
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:904:                res.accept_length_per_req_cpu,
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:934:            # first_token_indices_per_req=prepend(0, accepted_indices[cumulative_accepted_lengths[:-1]]) = [0, 5, 10]
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:935:            # last_token_indices_per_req=accepted_indices[cumulative_accepted_lengths - 1] = [4, 9, 11] (last token ID of each req)
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:936:            # max_relative_indices_per_req = [4,4,1]; those are the per-req spec-decoding step offsets that contain the correct mamba caches
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:937:            # first_token_indices_per_req = res.accepted_indices[accepted_indices_start]
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class.*Req\\|class Request\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/io_struct.py | head -30"
}
```

> TOOL

tool_result Bash
```
44:class BaseReq(ABC):
58:class BaseBatchReq(ABC):
69:class RequestTimingMetricsMixin:
166:class GenerateReqInput(BaseReq, APIServingTimingMixin):
684:class TokenizedGenerateReqInput(BaseReq):
760:class BatchTokenizedGenerateReqInput(BaseBatchReq):
775:class EmbeddingReqInput(BaseReq, APIServingTimingMixin):
902:class TokenizedEmbeddingReqInput(BaseReq):
922:class BatchTokenizedEmbeddingReqInput(BaseBatchReq):
998:class BatchMultimodalDecodeReq(BaseBatchReq):
1086:class BatchMultimodalOutput(BaseBatchReq):
1111:class BatchEmbeddingOutput(BaseBatchReq, RequestTimingMetricsMixin):
1128:class ClearHiCacheReqInput(BaseReq):
1133:class ClearHiCacheReqOutput(BaseReq):
1138:class FlushCacheReqInput(BaseReq):
1143:class FlushCacheReqOutput(BaseReq):
1148:class PauseGenerationReqInput(BaseReq):
1178:class ContinueGenerationReqInput(BaseReq):
1183:class UpdateWeightFromDiskReqInput(BaseReq):
1207:class UpdateWeightFromDiskReqOutput(BaseReq):
1215:class UpdateWeightsFromDistributedReqInput(BaseReq):
1232:class UpdateWeightsFromDistributedReqOutput(BaseReq):
1238:class UpdateWeightsFromTensorReqInput(BaseReq):
1257:class UpdateWeightsFromTensorReqOutput(BaseReq):
1263:class InitWeightsSendGroupForRemoteInstanceReqInput(BaseReq):
1281:class UpdateWeightsFromIPCReqInput(BaseReq):
1291:class UpdateWeightsFromIPCReqOutput(BaseReq):
1297:class InitWeightsSendGroupForRemoteInstanceReqOutput(BaseReq):
1303:class SendWeightsToRemoteInstanceReqInput(BaseReq):
1313:class SendWeightsToRemoteInstanceReqOutput(BaseReq):
```

> AGENT

现在我有足够信息了。让我整理完整的分析报告：

---

## 详细代码梳理：SGLang EAGLE-3 推测解码动态 BS 切换方案

### 问题 1：Batch 调度入口

**Scheduler 决定 running batch 的关键位置：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py`
  - **行 1097**：`event_loop_normal()` 调用 `batch = self.get_next_batch_to_run()` 获取当前 step 的 batch
  - **行 1133**：`event_loop_overlap()` 同样调用上述函数
  - **行 1797-1873**：`get_next_batch_to_run()` 核心函数，负责返回下一个要执行的 ScheduleBatch 对象

**Running batch 的 size 可读位置：**

- **行 1907, 1982, 2051, 2502, 2706**：均使用 `len(self.running_batch.reqs)` 获取当前 running batch 大小
- **行 740**：`self.running_batch` 初始化为 `ScheduleBatch(reqs=[], batch_is_full=False)`，是 scheduler 的成员变量
- **行 2236**：在 `enable_overlap` 模式下，`bs = len(model_worker_batch.seq_lens)` 也能获取 BS

**spec v1 vs spec v2 overlap 入口差别：**

- **行 2219-2225**：判断逻辑——
  - `spec_algorithm.is_none() or enable_overlap` 时：使用 `batch.get_model_worker_batch()`（v2 overlap 路径）
  - 否则：直接传递 `batch` 本身（v1 非 overlap 路径）
- **行 2258-2272**：若 `batch.is_spec_v2`，则进入 overlap 特殊处理，包括 `batch.spec_info = batch_result.next_draft_input`

**结论**：
- Running batch size 在 scheduler event loop 的 `get_next_batch_to_run()` 之后、`run_batch()` 之前可读
- 调用者需要通过 `len(self.running_batch.reqs)` 或 `batch.batch_size()` 获取
- 两条路径的分歧点在 `enable_overlap` 标志（由 `server_args.disable_overlap_schedule` 控制）

---

### 问题 2：EAGLE Worker 入口与 draft→verify 主循环

**EAGLEWorker v1 的核心入口：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`
  - **行 351-406**：`forward_batch_generation(batch: ScheduleBatch) -> GenerationBatchResult` 主函数
    - **行 363-378**：若为 `EXTEND` 模式，走 prefill 路径
    - **行 380-406**：否则走 decode 主循环：`draft(batch)` → `verify(batch, spec_info)` → 返回结果

**Draft→Verify 主循环结构：**

```
forward_batch_generation(batch)
  ├─ 若 batch.forward_mode.is_extend(): forward_target_extend + forward_draft_extend
  └─ 否则（DECODE）:
      ├─ spec_info = draft(batch)         [行 383]
      ├─ logits_output, verify_output, ... = verify(batch, spec_info)  [行 384-385]
      └─ 若需要，forward_draft_extend_after_decode(batch)  [行 398]
```

**spec_steps、topk、num_draft_tokens 的消费位置：**

- **行 154-156**：在 `__init__` 时从 `server_args` 读取并存储为 self 属性：
  ```python
  self.topk = server_args.speculative_eagle_topk
  self.speculative_num_steps = server_args.speculative_num_steps
  self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
  ```
- **行 647, 666**：在 `draft()` 函数中调用 `build_tree_kernel_efficient()` 时使用
- **行 710**：在 `EagleVerifyInput` 创建时传入 `draft_token_num=self.server_args.speculative_num_draft_tokens`
- **行 783**：在 `organize_draft_results()` 中被消费用于重组 token

**关键发现**：这些参数在 **worker init 时一次性读取**，之后每个 step 都使用同一份值。**不存在 step-level 的动态读取机制**。

**EAGLEWorkerV2（overlap 模式）的差别：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py`
  - **行 616-658**：`forward_batch_generation(model_worker_batch)` 主函数
    - 分为 EXTEND 和 DECODE 两路
    - DECODE 路径：`draft(model_worker_batch)` → `verify(model_worker_batch)` → `_draft_extend_for_decode()`
    - 使用 `ModelWorkerBatch` 而非 `ScheduleBatch`

---

### 问题 3：CUDA Graph 与 Spec 形状绑定

**Draft model CUDA graph capture：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`
  - **行 305-341**：`init_cuda_graphs()` 函数，调用 `EAGLEDraftCudaGraphRunner` 进行 capture
  - **行 318**：仅在 `self.speculative_num_steps > 1` 时才 capture draft graph
  
- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py`
  - **行 37-134**：`EAGLEDraftCudaGraphRunner.__init__()` 中进行 graph capture
  - **行 56-57**：存储 `self.speculative_num_steps` 和 `self.topk`
  - **行 65-74**：
    ```python
    self.capture_bs, self.compile_bs = get_batch_sizes_to_capture(model_runner)
    self.num_tokens_per_bs = self.topk          # 关键！
    self.max_bs = max(self.capture_bs)
    self.max_num_token = self.max_bs * self.num_tokens_per_bs  # max_bs × topk
    ```
  - **行 86-101**：分配 graph 输入 buffers，大小为：
    - `out_cache_loc`：`(max_num_token * speculative_num_steps,)` 【与 spec_steps 相关】
    - `input_ids`：`(max_num_token,)` = `(max_bs * topk,)`
    - `seq_lens`, `topk_p`, `topk_index` 等

**Target model verify graph：**

- Target model 的 graph 是在 target worker 侧 capture，不是在 EAGLE worker 侧
- Verify 不捕获独立的 cuda graph，而是依赖 target worker 自身的 graph capture（按照普通 decode batch size 捕获）

**Graph 与 dtn 形状的关键绑定：**

- **`dtn` 影响的是 verify kernel 的输入形状**，而不是 draft graph：
  - Verify 的输入是 `spec_info.draft_token`，形状为 `(batch_size × dtn,)` 展平
  - 这在 `prepare_for_verify()` 时动态分配 cache（行 142-176）
  
- **Draft graph 只与 `topk × spec_steps` 有关**：
  - Draft 从 `topk_p` 和 `topk_index` 读取 top-k 候选
  - 输出大小固定为 `batch_size × topk × spec_steps` 的 draft tokens
  - Graph buffer 大小 = `max_bs × topk × speculative_num_steps`

**Capture batch size 列表：**

- **行 65**：`self.capture_bs = get_batch_sizes_to_capture(model_runner)`
- 这来自 `server_args.cuda_graph_bs`（行 936-939 in server_args.py）
- 默认生成的列表包含 1 到 `cuda_graph_max_bs` 的多个 bucket

**如果 dtn 在 5 ↔ 7 之间切换：**

- **Draft graph 不需要重新 capture**（dtn 不影响 draft graph，只影响 verify 输入）
- **但 verify kernel 的执行会改变**：从 `bs × 5` 个 draft token 变成 `bs × 7` 个
- **关键问题**：verify 使用的 tree mask、positions 等是在 `prepare_for_verify()` 中动态重新计算的（行 134），所以理论上支持。但 **custom_mask buffer 的大小是预分配的**（行 229-242），如果 dtn 变化导致 mask 需要更大，会触发 re-alloc

**SGLang 是否支持多 graph 按 dtn 分桶：**

- **当前：不支持**
- Graph 对 dtn 并无约束，因为 dtn 只影响 verify 的输入准备，不影响 draft graph

**Cuda-graph-bs 参数设置：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py`
  - **行 529-530**：
    ```python
    cuda_graph_max_bs: Optional[int] = None
    cuda_graph_bs: Optional[List[int]] = None
    ```
  - **行 936-939**：如果未指定 `cuda_graph_bs`，则调用 `_generate_cuda_graph_batch_sizes()` 自动生成
  - **行 1002-1025**：生成逻辑，根据 `cuda_graph_max_bs` 和硬件配置生成 bucket

---

### 问题 4：No-spec 切换可能性

**同一 worker 实例能否 step-level 切换 EAGLE vs 普通 decode：**

- **答案：目前不支持**
- `EAGLEWorker.forward_batch_generation()` 是 hard-coded 的 spec 流程，无条件分支到 draft/verify
- 没有 fallback 路径可以在 spec 失败时回退到普通 decode

**forward_batch_generation 是否有 enable/disable spec 的开关：**

- **行 351-406**：函数签名只有 `batch: ScheduleBatch`，不接受 spec enable/disable 参数
- 执行 path 由 `batch.forward_mode` 决定（EXTEND/DECODE/IDLE），但不涉及 spec on/off

**spec_info 的 verified_id / verified_token 的生命周期：**

- **初始化**：在 `draft()` 中从 spec_info（来自上一步 verify 输出）读取（行 658）
- **修改**：在 `organize_draft_results()` 中更新（行 783）
- **消费**：在 build_tree_kernel_efficient() 中使用（行 657）

**如果切到 no-spec，draft KV / verify state 的处理：**

- 无法通过同一 worker instance 切换，必须走完整的 forward_batch_generation 流程
- 若要支持，需要在 scheduler 层实现"跳过 EAGLE worker，直接调用 target_worker"的逻辑
- 当前代码路径（行 2283-2285）中，spec v1 时直接调用 `self.model_worker.forward_batch_generation()`，可以绕过 eagle_worker
- **但问题**：running_batch 中的 req.spec_info 等状态已经被污染，无法直接回到无 spec 状态

**现有 fallback 机制检查：**

- **行 439-442**（tp_worker.py）：`is_verify=True` 时会跳过 sampling，但不涉及 spec on/off

---

### 问题 5：Dtn 动态调整

**speculative_num_draft_tokens 的持有位置：**

- **ServerArgs（唯一全局常量）**：
  - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py` 行 425
  - 在启动时通过 `--speculative-num-draft-tokens` 参数设置，之后不变
  
- **EAGLEWorker 实例**：
  - `eagle_worker.py` 行 156：`self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens`
  - 存储在 worker 实例上，作为初始化时的常数

- **EagleVerifyInput（每 step 携带）**：
  - `eagle_info.py` 行 95：`draft_token_num: int` 字段
  - 在每个 verify step 都会被读取，但值来自 eagle_worker 的 self 属性（行 710）

**不重启 server 能否切换 dtn：**

- **答案：不能**
- dtn 在初始化时固定，每个 batch 都硬编码使用该值
- 要改变 dtn，必须重启 server，重新初始化 EAGLEWorker

**Draft tree 形状生成逻辑（mask、parent、position）：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py`
  - **行 47-150**：`build_tree_kernel_efficient()` 函数
  - **输入**：`verified_id`, `parent_list`, `top_scores_index`, `draft_tokens`, `topk`, `spec_steps`, `num_verify_tokens`
  - **处理**：调用 sgl_kernel 侧的 CUDA kernel
  - **输出**：`tree_mask`, `position`, `retrive_index`, `retrive_next_token`, `retrive_next_sibling`

- **关键发现**：所有这些都在 **runtime 动态计算**（不是预先 capture 的常数）
  - `num_verify_tokens` = `num_draft_tokens`，来自参数
  - tree mask 大小：取决于 `topk`, `spec_steps`, `num_verify_tokens` 的组合

**如果要在运行时改变 dtn：**

- 理论上可行：只需修改 eagle_worker 的 self.speculative_num_draft_tokens，下一个 step 会用新值
- **但实际困难**：
  1. 没有接口来动态修改 worker 的参数
  2. 需要确保所有正在运行的 requests 同时切换（否则混合不同 dtn 的 batch）
  3. Verify kernel 的 buffer 需要重新分配

---

### 问题 6：现有钩子与环境变量

**EAGLE_FORCE_NO_ACCEPT 的实现：**

- **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py`
  - **行 24**：`_FORCE_NO_ACCEPT = os.environ.get("EAGLE_FORCE_NO_ACCEPT", "0") == "1"`
  - **行 439-442**：若 `_FORCE_NO_ACCEPT` 为真，强制设置 `accept_index[:, 1:] = -1` 和 `accept_length.zero_()`
  
- **效果**：虽然仍然执行 draft 和 verify，但 **所有 draft token 都被 reject**，只接受 user_4813494d token（原始预测）
- **不是完整的 no-spec**，而是"假 spec"（spec 流程运行，但结果被丢弃）

**EAGLE_MARS_THETA 的传递路径：**

- **环境变量读取**：
  - **行 26**：`_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))`
  
- **Verify 中的消费**：
  - **行 345-374**：在 `EagleVerifyInput.verify()` 中，读取全局 `_MARS_THETA` 并计算 top-2 ratio
  
- **Step-level 读取**：
  - 每次 verify 都读取全局变量，所以理论上可以动态改变（但需要改动 environ，且需要重新启动 kernel）

**其他 per-step 动态参数通道：**

- **Sampling info**：`batch.sampling_info` 可以 per-request 定制，但与 spec 参数无关
- **Grammar**：`batch.has_grammar` 和 vocab_mask 可以动态变化，但独立于 spec 配置
- **没有通用的"spec mode config"结构体** 用于 per-batch 或 per-step 定制

---

### 问题 7：Scheduler 视角拿到 running bs

**Event loop 中 running batch 何时准备好：**

- **行 1097/1133**：`batch = self.get_next_batch_to_run()` 返回后，`running_batch` 已完全构建
- **行 2051**：在 `run_batch()` 中可以直接读取 `len(self.running_batch.reqs)`

**V1 非 overlap 路径：**

```
get_next_batch_to_run()
  ├─ 行 1841: new_batch = self.get_new_batch_prefill()
  ├─ 行 1859-1861: 若无 new_batch，则返回 self.running_batch
  └─ 返回 ret（可能是 new_batch 或 running_batch）

run_batch(batch)
  ├─ 行 2225: worker_batch_or_batch = batch  （直接用 ScheduleBatch）
  └─ 行 2283: self.model_worker.forward_batch_generation(worker_batch_or_batch)
```

**V2 overlap 路径：**

```
get_next_batch_to_run()
  └─ 返回 batch（ScheduleBatch）

run_batch(batch)
  ├─ 行 2221: worker_batch_or_batch = batch.get_model_worker_batch()  （转换为 ModelWorkerBatch）
  ├─ 行 2236: bs = len(model_worker_batch.seq_lens)  （在这里可读）
  └─ 行 2243: self.model_worker.forward_batch_generation(model_worker_batch)
```

**在 forward 之前能否调用 worker 上的"set spec mode"接口：**

- **答案：当前不存在这样的接口**
- Forward 之前只有 batch 构建逻辑，没有 worker 配置修改步骤
- 要实现此功能，需要新增接口，例如：`eagle_worker.set_spec_config(dtn=5, topk=2, spec_steps=2)`

**Running batch size 在 event loop 中的可见性：**

```
event_loop_normal():
  ├─ 行 1097: batch = self.get_next_batch_to_run()
  │   └─ 此时 self.running_batch 已更新（内部逻辑）
  ├─ 行 1098: self.cur_batch = batch
  ├─ 行 2236 (run_batch): bs = batch.batch_size()  ← 可直接读
  └─ 或 len(batch.reqs)
```

---

## 切换可行性快评

### 关键技术障碍

| 挑战 | 当前状态 | 难度 |
|------|--------|------|
| **Batch size 感知** | Scheduler 内可读 `len(self.running_batch.reqs)` | ✅ 容易 |
| **Step-level 参数切换** | 无机制，所有参数在 init 时固定 | ❌ 中等 |
| **Spec mode 动态启/禁** | No-spec 无专用路径，只有 FORCE_NO_ACCEPT 钩子 | ❌ 困难 |
| **CUDA graph 重 capture** | Graph 绑定 `max_bs × topk × spec_steps`；若 dtn 变化需重分配 buffers | ⚠️ 中等 |
| **Tree mask/positions 动态调整** | 每 step 都重新计算，与 dtn 无硬绑定 | ✅ 已支持 |
| **Draft KV cache 状态** | 与 dtn 强相关，切换时需要 flush 或重新分配 | ❌ 困难 |
| **正在运行的请求原子性** | 无法保证"全体 requests 同时切换" | ❌ 困难 |

### 分阶段实现可行性评估

#### 阶段 1：添加"按 BS 切换"的钩子（实现度：40%）

**可做性：中等难度**

```python
# 在 scheduler.run_batch() 中（行 2193-2309）：
running_bs = batch.batch_size()
if running_bs > 32:
    # 禁用 EAGLE，走普通 decode
    spec_config = {"enable": False}
elif running_bs > 1:
    # MARS tree，dtn=5
    spec_config = {"dtn": 5, "topk": 2, "spec_steps": 2, "theta": 0.85}
else:
    # BS=1，dtn=7
    spec_config = {"dtn": 7, "topk": 2, "spec_steps": 3, "theta": 0.85}

# 问题：如何传递 spec_config 到 eagle_worker？
```

**需要修改的地方：**
1. 新增 scheduler → worker 的参数传递通道
2. EAGLEWorker 需要支持 per-call 的 spec_config 参数
3. 每个 batch 都需要检查 BS 并决定是否使用 spec

**风险：**
- 样本混合：同一个 batch 中部分请求用 spec，部分不用 → 复杂的状态管理

#### 阶段 2：实现"全体样本原子切换"（实现度：20%）

**可做性：困难**

```python
# 候选方案：
# 1. Scheduler 维护一个"全局 spec 配置"状态机
# 2. 当 BS 穿过阈值时，设置一个"待切换"标记
# 3. 等待所有当前 requests 完成 verify，再切换 config
# 4. 新的 requests 用新 config

# 问题：
# - 需要追踪每个 request 的生命周期（何时 verify 完成）
# - 需要对 running_batch 中的所有 requests 做"检查点"
# - Spec v2 overlap 模式中，draft 和 verify 异步，增加复杂性
```

**需要修改的地方：**
1. Scheduler 新增"spec mode 状态机"
2. Request 类新增"spec config version"字段
3. 在 process_batch_result() 中检测配置版本变化
4. 必要时 flush draft KV cache

#### 阶段 3：Draft KV cache 状态管理（实现度：10%）

**可做性：非常困难**

**核心问题：**

当 dtn 从 5 → 7 时：
- Draft model 的 KV cache 从 `bs × 5 × spec_steps` 变成 `bs × 7 × spec_steps`
- 已分配的 cache slot 无法"扩展"（paged cache 中的 page 链已确定）
- 需要重新分配整个 draft KV cache 池

**解决方案需要：**
1. 追踪每个 request 的 draft KV cache 位置
2. 当配置改变时，重新分配并拷贝 KV
3. 确保 draft_pool 中有足够空间（可能需要 evict 其他 request）

**风险：**
- 内存碎片化
- 性能抖动（重分配期间的延迟）

#### 阶段 4：No-spec fallback（实现度：5%）

**可做性：极其困难**

**当前架构的根本限制：**

1. `EAGLEWorker` 继承自 `TpModelWorker`，hard-coded 覆盖 `forward_batch_generation()`
2. Scheduler 调用 `self.model_worker.forward_batch_generation()`，无法中途切换到"原始 target_worker"
3. Running batch 中的 requests 已经进入 spec 流程，有 `spec_info` 状态

**可能的实现方式：**

```python
# 在 scheduler 层增加 override：
if should_disable_spec():
    # 绕过 EAGLE worker，直接调用 target_worker
    batch_result = self.target_worker.forward_batch_generation(batch.get_model_worker_batch())
else:
    batch_result = self.model_worker.forward_batch_generation(...)  # EAGLE worker
```

**需要处理：**
1. Requests 的 `spec_info` 需要重置或忽略
2. Draft KV cache slots 需要释放
3. Scheduler 需要知道两个 worker 实例（target 和 spec）

---

## 最终建议

### 推荐方案：三层递进式实现

**第一层（低风险，短期可交付）：**
1. 在 scheduler 中添加 BS 阈值检测逻辑
2. 使用现有的 `EAGLE_FORCE_NO_ACCEPT` 钩子实现"伪 no-spec"
   - 样本仍走 draft/verify 流程，但 draft tokens 全部被 reject
   - 性能接近 no-spec，但无需改动核心流程
3. 环境变量动态控制：`EAGLE_FORCE_NO_ACCEPT=1` 当 BS > 32

**第二层（中期目标）：**
1. 新增 scheduler → worker 的"per-batch spec config"传递机制
2. 修改 `EAGLEWorker.forward_batch_generation()` 接受可选的 spec_config 参数
3. 支持 dtn 和 theta 的 per-batch 变化（但仍是全 batch 一致）
4. 使用预分配的多大小 draft KV cache 池（按 dtn=5, dtn=7 分类）

**第三层（长期架构演进）：**
1. 设计"Spec Config State Machine"，支持配置平滑过渡
2. 实现 per-request 的 spec 配置跟踪（而非 per-batch）
3. 支持真正的 spec → no-spec fallback（需要重构 Worker 接口）

### 立即可做的验证步骤

1. **测试 EAGLE_FORCE_NO_ACCEPT** 的实际性能影响（vs 真正的 no-spec）
2. **在 scheduler.run_batch() 之前插入 BS 检查**，打印 BS 变化趋势
3. **评估 draft KV cache 内存成本**（dtn=5 vs dtn=7 的差异）
4. **Profiling draft model 的时间成本**（在不同 dtn/topk 下的性能）

这样可以量化收益与成本，为后续深度改造提供数据支持。
