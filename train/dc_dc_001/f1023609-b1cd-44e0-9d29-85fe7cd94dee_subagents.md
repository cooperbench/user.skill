---
session_id: "f1023609-b1cd-44e0-9d29-85fe7cd94dee:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-23T16:37:07.988Z"
n_turns: 44
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Research how EAGLE-3 (the speculative decoding paper by the EAGLE team) selects which layers to use as auxiliary hidden states ("aux layers"). Context: EAGLE-3 uses hidden states from multiple intermediate layers of the target model as input to the draft model. The draft model concatenates these hidden states and projects them via an fc layer. The question is: how does the EAGLE-3 paper recommend choosing WHICH layers to use? Search for: 1. The EAGLE-3 paper (likely on arxiv, by authors associated with EAGLE/EAGLE-2 speculative decoding, possibly from Peking University or related groups) 2. Specifically look for their methodology on selecting auxiliary layers - do they use linear probes? Mutual information? Some other criterion? 3. How many aux layers do they recommend? Is there a scaling relationship? 4. Any ablation studies on layer selection Also check EAGLE-2 if EAGLE-3 doesn't have this detail - the aux layer concept may have been introduced earlier. Report findings concisely - the key method and any specific recommendations.

> AGENT

I'll research the EAGLE-3 paper and its methodology for selecting auxiliary layers.

> AGENT

Now let me get the full paper content, specifically focusing on the layer selection methodology.

> AGENT

Now let me look at the SpecForge training framework and the EAGLE-3 code to find the specific layer selection logic.

> AGENT

Let me now look at the actual EAGLE-3 paper more carefully, and also check the SpecForge codebase for the concrete layer indices used.

> AGENT

Excellent finding. Let me get one more piece -- the actual config.json from released EAGLE-3 models to see the concrete layer indices used.

> AGENT

Now let me check the official EAGLE-3 repository and the SafeAILab code for the exact layer selection logic.

> AGENT

Now let me also check the local project's eagle config for the actual layer indices used.

> AGENT

Now let me look at the docs in this project for more details about their specific layer selection rationale.

> AGENT

Found the key piece. Now let me look at the training-v2.md for the linear probe details.

> AGENT

I have comprehensive information now. Let me compile the findings. --- ## 研究结果：EAGLE-3 辅助层（aux layers）选择方法 ### 核心论文 **EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test** (arXiv:2503.01840, NeurIPS 2025)，作者 Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang（Peking University / Microsoft Research Asia）。 ### 层选择方法 **EAGLE-3 论文本身并没有提出一套系统化的层选择方法论。** 论文只描述了"从 target model 的 low、middle、high 三个层级提取 hidden states"，然后 concat 成 3k 维向量，经 FC 层压缩回 k 维。论文没有给出： - 具体的层索引选择算法（如 linear probe、mutual information 等） - 层数的消融实验（只做了"top-layer only vs 三层 fusion"的消融，没有比较不同层组合） - 选多少层的推荐（固定为 3 层） ### 消融实验 论文 Table 2 的消融只有两个维度： 1. EAGLE-2 baseline (top-layer only): speedup 3.16x, tau 4.05 2. + remove feature prediction constraint: speedup 3.82x, tau 5.37 3. + fused features (low/mid/high): speedup 4.40x, tau 6.13 **没有**不同层组合的消融。 ### 实际工程中的做法 从实际部署代码和模型配置来看： 1. **固定 3 层**：所有 EAGLE-3 部署都用 3 个 aux 层（early/middle/late triad） 2. **具体层索引因模型而异**，常见选法是大致均匀分布在模型深度上： - **NVIDIA gpt-oss-120b (36 layers)**：layers 2, 18, 33（约 ~5%, ~50%, ~92% depth） - **Nemotron-Cascade2 (52 layers)**：layers 2, 26, 48（约 ~4%, ~51%, ~94% depth） - **本项目 MiniCPM-SALA (32 layers)**：layers 1, 10, 22（约 ~3%, ~31%, ~69% depth） 3. **Linear probe 验证**：本项目 (`/user_4813494d/openbmb/docs/eagle/README.md` 第 25 行) 记载了使用 linear probe 验证层选择的做法： > "Aux layers：[1, 10, 22]，linear probe 验证最优（CE=6.51 vs 次优 6.57）" 即：对不同层组合训练 linear probe（线性分类器从 hidden states 预测 next token），用交叉熵作为指标，选 CE 最低的组合。 4. **NVIDIA 的经验法则**（来自 Nemotron 模型卡的注释）： - 避免 layer 0（embedding 层附近，hidden states 还只是原始 token embedding，缺乏上下文化） - 避免最后一层（与只用 top-layer 差异不大） - 中间层选在模型中部 5. **本项目的待做项**（`/user_4813494d/openbmb/docs/eagle/training-v2.md` 第 101 行）提到了替代方案： > "aux_layers [0,9,22] or [7,15,23,31]：当前 [1,10,22] 偏前，均匀分布（借 DFlash 思路）可能更好。需重采数据。" 这说明 4 层方案也在考虑中，且有"均匀分布更好"的直觉。 ### 总结 | 问题 | 答案 | |---|---| | 论文推荐的选层方法 | **无系统方法**。论文只说"low/mid/high"三层 fusion，没有给出选择算法 | | 工程实践中的做法 | **Linear probe**（测量各层 hidden state 对 next-token prediction 的 CE loss），或者简单的**等间距三分法**（~5%, ~50%, ~90% depth） | | 推荐层数 | **固定 3 层**（论文和所有开源实现一致） | | 层数消融 | **论文中没有**。社区有人尝试 4 层但尚无发表结果 | | 关键避坑 | 避免 layer 0（太浅，只是 raw embedding）；避免最后一层（退化为 top-layer only） |

> DEVELOPER

深入检查 EAGLE-3 draft model 在 sglang 推理中的加载与前向流程，找出**所有可能与训练不一致的 bias / 量化 / 参数加载问题**。这非常关键，关系到 draft model 是否真的能复现训练时的精度。 ## 训练侧（已确认事实） - 训练脚本：/user_4813494d/openbmb/eagle/train.py - 训练时 fc 是 `nn.Linear(AUX_DIM=hidden_size*3=12288, HIDDEN_SIZE=4096, bias=False)` bf16，不做 FP4 QAT - 其他线性层（q/k/v/o + gate/up/down + lm_head 等）走 FP4_QAT (STE fake-quant on fwd) - aux_hidden 在采集时是从 target 的 layer_ids=[4, 9, 24] 抽取，3 层 hidden 在 last-dim 上 concat → AUX_DIM=12288 - 训练 forward：fc(aux) → embed_tokens(input_ids) → concat → norm → 1 个 transformer layer → lm_head(over draft_vocab=32000) - aux_hidden 在数据集里以 NVFP4 存储 (group=16, bf16 scale)，加载时 decompress 回 bf16 - shifted alignment：input_ids[:, 1:], aux_hidden[:, :-1], target[:, 1:] ## 转换侧（v3 → sglang_model_v3/） - /user_4813494d/openbmb/eagle/convert_to_sglang.py，FC_BF16=True - model.fc.weight 直接 bf16，无 NVFP4 4 元组（weight, weight_scale, weight_scale_2, input_scale） - 其他线性层走 add_nvfp4_tensors（NVFP4 4 元组） - hf_quant_config.json exclude_modules=["model.fc"] - config.json: eagle_aux_hidden_state_layer_ids=[4,9,24], target_hidden_size=4096, hidden_size=4096, draft_vocab_size=32000 ## 部署侧（需要你审计） - 部署模型路径：/user_4813494d/openbmb/eagle/sglang_model_v3/ - sglang fork：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/ - draft 模型类：llama_eagle3.py（应该在 srt/models/ 下） - 量化加载：layers/quantization/modelopt_quant.py（NVFP4LinearMethod / UnquantizedLinearMethod / is_layer_excluded） ## 任务 请仔细检查并报告以下每一项是否一致： 1. **fc 层加载**：sglang 加载 model.fc.weight 时是否真的走 UnquantizedLinearMethod（不做 fp4 反量化）？exclude_modules regex 匹配 "model.fc" 时 prefix 实际是什么？是否会因 prefix 拼接导致漏匹配？ 2. **fc 层 bias**：训练时 nn.Linear(bias=False)，sglang ColumnParallelLinear 默认 bias 配置是什么？如果默认 bias=True 会怎样？safetensors 里没有 fc.bias，加载时是会报 missing key 还是初始化为 0 还是 NaN？ 3. **fc 输入维度**：训练是 fc(aux_hidden_concat[..., 12288])，AUX_DIM = target_hidden_size*3。sglang 的 fc in_features 怎么算的？是从 config.target_hidden_size*3 推的吗？config 是 4096，但 sglang 是否用了别的字段？ 4. **aux_hidden 抽取顺序**：训练时 aux 是 [layer4, layer9, layer24] 顺序 concat。sglang 推理侧从 target 抽取后 concat 顺序与训练一致吗？eagle_aux_hidden_state_layer_ids=[4,9,24] 是有序的还是会被排序？ 5. **aux_hidden dtype**：训练时 aux_hidden 在 fwd 时是 bf16 输入 fc。推理时 target 输出的 aux_hidden 是什么 dtype？有没有 fp16/bf16 不一致？ 6. **embed_tokens / lm_head**：draft 模型里 embed_tokens 形状 (vocab=73448, hidden=4096)，lm_head 形状 (draft_vocab=32000, hidden=4096)。训练时 lm_head 走 FP4_QAT；部署时是 NVFP4 的吗？vocab/draft_vocab 是否对齐？draft_vocab=32000 是 tokenizer 的子集还是 remap 的？是否有 d2t/t2d remap 表？ 7. **scale_emb=12**：config 里有 scale_emb=12（MiniCPM 的 embedding scale）。draft 推理时 embed_tokens 输出会乘 12 吗？训练时乘了吗？ 8. **tie_word_embeddings=false**：draft 的 lm_head 不与 embed_tokens 共享。训练时确实是独立的吗？ 9. **norm 层 (input_layernorm / post_attention_layernorm / norm)**：这些 RMSNorm 是不量化的吧？safetensors 里以 bf16 还是 float32 存？sglang 加载是否一致？训练时 dtype 是？ 10. **rotary embedding**：max_position_embeddings=524288。draft 的 RoPE base / scaling 与 target 是否一致？训练时 RoPE max_len 是多少？是否会有位置编码不一致？ 11. **transformer layer 内部**：draft 只有 1 个 layer。q/k/v/o + gate/up/down 都走 NVFP4。是否有训练 fwd 上做 QAT 但部署时 forward 路径不同（比如 input_scale 缺失/重新计算）的问题？ 12. **lm_head NVFP4 量化**：lm_head 是大矩阵 (32000, 4096)，训练 FP4_QAT，部署 NVFP4。weight_scale_2 / input_scale 是怎么算的？convert_to_sglang.py 的 add_nvfp4_tensors 用的是 ammo 还是手算？校准的 amax 来源？是否复用 target lm_head 的 input_scale？还是重新算？ 请把发现的每个 bias/不一致问题列出来，包括：可能的影响、确证/怀疑级别、复现方法。不要只看一个文件，要顺着实际加载链路读。可以用 grep 找 "fc"、"aux_hidden"、"eagle"、"draft_vocab"、"d2t"、"target_hidden_size"、"scale_emb" 等关键 symbol。 控制在 800 字以内，但发现的具体问题点要列清楚。

> AGENT

I'll conduct a thorough audit of the EAGLE-3 draft model's loading and forward flow in sglang to identify bias/quantization/parameter loading inconsistencies. Let me start by exploring the codebase systematically.

> AGENT

Let me search for the key files mentioned in the audit.

> AGENT

Now let me check the sglang model loading side:

> AGENT

Now let me check the quantization loading code:

> AGENT

Let me continue reading the quantization file and check the exclude_modules logic:

> AGENT

Now let me check the ColumnParallelLinear bias default and the training script:

> AGENT

Now let me check the training script and the hf_quant_config.json:

> AGENT

Now let me check the config and verify scale_emb handling:

> AGENT

Now let me check the aux_hidden extraction and how it's used:

> AGENT

Now let me check how lm_head is loaded and if it goes through NVFP4:

> AGENT

Let me check the fc layer loading behavior more carefully:

> AGENT

Now check the key part - how bias is handled in training vs deployment:

> AGENT

Let me check if there's missing key handling in weight loading:

> AGENT

Now let me check the eagle_worker to understand how aux_hidden is extracted during inference:

> AGENT

Let me check eagle_info to see how aux_hidden is extracted from layer outputs:

> AGENT

Let me search for where hidden_states is extracted from layer_ids:

> AGENT

Let me search in the model runner or forward batch to see how aux_hidden concatenation happens:

> AGENT

Critical! Let me verify how the hidden states are concatenated:

> AGENT

Now let me check how the aux_hidden_states list is then processed in forward_batch:

> AGENT

Let me search for where logits_output is created in forward:

> AGENT

Found it! Let me check line 538:

> AGENT

Perfect! Now let me check if the concatenation order preserves the order of layer_ids. Let me also check for potential issues with dtype:

> AGENT

Now let me check what dtype the aux_hidden comes in:

> AGENT

Now let me check the fc layer in llama_eagle3 to verify bias handling:

> AGENT

Good! Now let me check safetensors to see what's actually in there:

> AGENT

Perfect! Now let me check if there are issues with the fc layer in exclude_modules matching:

> AGENT

Excellent! Now let me verify the fc layer will not have bias loaded and check the actual layer instantiation:

> AGENT

Now let me check one more critical issue - whether the ColumnParallelLinear actually creates a bias even when bias=False:

> AGENT

Perfect! Now let me verify the scale_emb is actually applied in forward:

> AGENT

Perfect! Now let me do a final check on the lm_head to see if it will load correctly:

> AGENT

Excellent! Now let me compile my findings. Let me search for the actual issue with the comment in llama_eagle3.py about lm_head:

> AGENT

Perfect! Now I have all the information I need. Let me compile the audit report. ## 深度审计报告：EAGLE-3 Draft Model 加载与前向不一致问题 ### 关键发现：**大多数配置一致，但有3个明确问题和3个高风险潜在问题** --- ### ✅ **确认无误的项（1, 2, 3, 5, 7, 8, 9, 10）** | 项 | 状态 | 证据 | |----|------|------| | **1. fc 层加载** | ✅ 正确 | exclude_modules regex "model.fc" 精确匹配；is_layer_excluded() 会拦截所有 model.fc.* 前缀 → UnquantizedLinearMethod 加载无量化 | | **2. fc 层 bias** | ✅ 正确 | config 无 "bias" 字段 → getattr(config, 'bias', False)=False；safetensors 无 fc.bias；ColumnParallelLinear 行361 register_parameter("bias", None) | | **3. fc 输入维度** | ✅ 正确 | config.target_hidden_size=4096，fc_in = 4096*3=12288；llama_eagle3.py L138 显式 self.hidden_size_in * 3 | | **5. aux_hidden dtype** | ✅ 安全 | target 是 bfloat16 模型；aux_hidden 从 layer output 抽取保持原 dtype；fc forward 接收 bf16 输入 | | **7. scale_emb=12** | ✅ 应用 | llama_eagle3.py L161 embeds = self.embed_tokens(input_ids) * self.scale_emb；训练脚本 L318 也设 self.scale_emb = SCALE_EMB=12 | | **8. tie_word_embeddings=false** | ✅ 一致 | config tie_word_embeddings=false；lm_head 独立 (32000, 4096)，不与 embed_tokens 共享 | | **9. norm 层** | ✅ 一致 | RMSNorm 权重以 bf16 保存在 safetensors；无 scale/zero_point；部署加载无量化 | | **10. RoPE** | ✅ 无不一致 | max_position_embeddings=524288；base=10000；部署继承 target 的 RoPE（llama_eagle3 无自定义） | --- ### ⚠️ **发现的问题** #### **问题 1：aux_hidden 抽取顺序可能 off-by-one** - **现象**：训练数据采集时 aux 来自 layer_ids=[4, 9, 24]；部署 eagle_aux_hidden_state_layer_ids=[4,9,24] 传给 set_eagle3_layers_to_capture() - **关键发现**：llama.py L779 **对 layer_ids 做了 +1 转换**： ```python self.model.layers_to_capture = [val + 1 for val in layer_ids] # [4,9,24] → [5,10,25] ``` **注释说明**："in sglang, for the ith layer, it takes the output of the (i-1)th layer as aux hidden state" - **不一致**：这个 +1 **改变了抽取的实际层**。如果训练数据真的是从 layer 4/9/24 抽取，而部署从 5/10/25 抽取，则特征分布完全不同 - **可能的影响**：aux_hidden 与训练不匹配 → fc 输入分布变化 → 精度下降 - **复现方法**：对比训练数据里 layer 4/9/24 hidden state 与部署实际抽取的 5/10/25 - **怀疑级别**：**高度怀疑** — 注释明确说有偏移，但无人验证训练数据采集时是否也做了相同偏移 #### **问题 2：aux_hidden 列表顺序与 layers_to_capture 无序** - **现象**：logits_processor.py L538 `torch.cat(aux_hidden_states, dim=-1)` 拼接列表 - **风险**：llama.py L371 `if i in self.layers_to_capture: aux_hidden_states.append(...)` — 列表顺序取决于层遍历顺序 - 若 layers_to_capture=[5,10,25]，则层遍历 [5,10,25] 顺序追加 ✅ - 但若遍历中 layers_to_capture 被排序或打乱，顺序变化 - **训练端对比**：train.py 中 concat 的是 `[layer4, layer9, layer24]` 的 3 个 hidden（cat 在 last-dim） - **可能的影响**：若 concat 顺序不同（如 [5,10,25] vs [4,9,24] 后续加 +1），logits_processor 拼接顺序不对 → fc 权重对应关系混乱 - **复现方法**：打印 aux_hidden_states 列表长度与顺序，验证 dim=-1 拼接后形状是否 [bs, seq, 12288] - **怀疑级别**：**中等** — Python list 保持 append 顺序，but 需验证 layers_to_capture 是否被排序 #### **问题 3：lm_head 未走 NVFP4，但训练时用 FP4_QAT_LINEAR** - **现象**：convert_to_sglang.py L211 将 lm_head 存为 **BF16**（注释 L208-210）；safetensors 中 lm_head.weight 无 weight_scale/weight_scale_2 - **训练端**：train.py L321 `self.lm_head = FP4QATLinear(...)` — 在训练时走 **FP4 fake-quant** (STE) - **不一致**： - 训练：lm_head 权重在 FP4 grid（经过 _fp4_round） - 部署：lm_head 权重以 BF16 存储，无 NVFP4 4-tuple（weight_scale, weight_scale_2, input_scale） - […]
