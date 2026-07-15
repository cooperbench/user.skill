> DEVELOPER

深入仔细阅读 谅解一下我们的工作和工作内容

> AGENT

我已经深入阅读了 `/user_4813494d/openbmb/` 工作区的 CLAUDE.md、AGENTS.md 和 docs/handover.md。以下是对你工作的理解： ## 项目定位 **SOAR 比赛工作区** — 优化 OpenBMB/MiniCPM-SALA 推理性能，最终在官方云环境打分。基座模型不可换，改动只能落在：量化、SGLang fork、推测解码 draft、kernel、平台部署脚本。 ## 模型架构要点 - 32 层混合：8 standard Attention（layer 0/9/16/17/22/29/30/31）+ 24 Lightning Attention (GLA) - `hidden=4096`, `intermediate=16384`, `nq/nkv=32/2`, `head_dim=128`，512K 上下文 - **生产默认 `--dense-as-sparse`**，所有 standard Attention 走 sparse 路径（compress_k → stage1 → stage2 top-K FA） ## 运行栈 - 硬件：RTX 6000D（sm_120 Blackwell, 84GB） - PyTorch 2.11.0+cu130 / CUDA 13.2 / cuDNN 9.21 / FlashInfer 0.6.8.post1[cu13] / Triton 3.6.0 - venv 预激活在 `/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env` ## 当前生产配置 - **量化**：NVFP4（GPTQ + FourOverSix，wikitext 90 样本，`MAX_SEQ_LENGTH=92160`） - **Decode**：Marlin 全 M（生产默认）；b12x 2-tier 已 lock-in 但默认关闭 - **推测解码**：EAGLE-3 chain verify，`spec_steps=5, topk=2, dtn=11`，dynamic NO_SPEC/D5/D7 切换 - **Draft**：`demo-sala/data/eagle_draft/`（来源 `draft_main` step 6250 / `v3mix_300k_s6250_ind672`） ## 三条主线 | 路径 | 用途 | |---|---| | `demo-sala/` | **正式提交包**（平台真正消费），≤2GB | | `probe-sala-s2/` | 反向 SSH 调试 sidecar（authorized_keys + dropbear/frpc） | | `eagle/` / `bench/` / `eval/` / `quant/` / `kernels/` | 研发、训练、bench、kernel 实验 | ## 关键红线（已记在脑里） - **始终简体中文回复** - **杀 sglang 只用** `bash bench/kill_sglang.sh`（禁 `pkill -f sglang`，会杀系统进程） - **始终 `uv pip install`**，永不 `pip install` - 替换 `.so` 必须先备份到 `outputs/so_backups/...` + 写 `docs/gemm/so-replacements.md` - SGLang 参数连字符风格（`--dense-as-sparse`） - 不用 argparse，脚本硬编码 - 性能改动先 profile 证明 >1.5× 收益再 e2e bench - DFlash / DDTree 是**探索路线，非生产**，提交包仍走 EAGLE-3 - 同时只能跑一个 GPU 任务 - Monitor 用 `grep -m1 PATTERN`，pattern […]

> AGENT

理解完毕，关键信息已存到 memory（5 个文件：项目、用户、中文反馈、运维规则、文档索引），下次 session 接续不用重读。 需要我现在动手做什么具体任务？比如： - 看 `docs/handover.md` 提到的某个接续点（prefill MLP epilogue / b12x 启用 / EAGLE 训练） - 跑 mini_bench 看当前性能 - 排查某个具体问题