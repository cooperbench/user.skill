> DEVELOPER

理解一下这个比赛的数据 给我讲讲什么类型的数据 是在做什么 集合Skip to content Kaggle Create Home Competitions Datasets Models Benchmarks Game Arena Code Discussions Learn More Your Work Viewed NVIDIA Nemotron Model Reasoning Challenge It seems the KV cache is not enabled during RL training Train locally and get lower scores. Inquiry regarding inference non-determinism and Open Progress Prize fairness ACCIDENT @ CVPR Edited baseline-bird LB 35.9 with Regex corrections (Public Model) LB 35.9 Ensembling & Post Processing Baseline baseline Data Preprocessing View Active Events Search NVIDIA · Featured Prediction Competition · 2 months to go NVIDIA Nemotron Model Reasoning Challenge Advance reasoning techniques using NVIDIA Nemotron open models on a novel benchmark NVIDIA Nemotron Model Reasoning Challenge Submit Prediction Overview Develop techniques that improve reasoning accuracy using NVIDIA Nemotron models. Participants will experiment with prompting, data pipelines, and lightweight fine-tuning while evaluating their approaches on a new reasoning benchmark developed by NVIDIA Research. Start 17 days ago Close 2 months to go Merger & Entry Description Reasoning benchmarks are a useful way to measure progress on structured tasks. When approaches and results are shared openly, the community can compare methods, reproduce improvements, and iterate more effectively. Today, reasoning improvements are explored across many independent efforts - often using different datasets, prompts, and evaluation setups - making direct comparison difficult. A shared benchmark and common baseline model allow techniques to be tested and compared more consistently. While language models perform strongly on many tasks, structured reasoning benchmarks remain an active area of research and optimization. In this competition, participants will work from a shared Nemotron 3 Nano baseline and a novel reasoning benchmark developed by NVIDIA Research. Nemotron provides an open foundation for this challenge, including openly available models, datasets, and training recipes that participants can build on or adapt within their own workflows. You may experiment with: Prompting strategies Data filtering and curation Synthetic data generation Reinforcement learning Lightweight fine-tuning Or other approaches of your choice Participants may use any training framework, tooling, or workflow to produce their LoRA adapter. NVIDIA-provided recipes are optional starting points - competitors are free to use other ecosystems and libraries (e.g., Hugging Face, Unsloth, Axolotl, TRL, or similar tooling). The only requirement is that the final submission produces a compatible LoRA adapter for the Nemotron-3-Nano-30B base model. Multiple valid solution paths are expected. Clear documentation - including notebooks and write-ups - is encouraged (and required for prize eligibility) to support […]

> AGENT

需求是把这个比赛在做什么、数据属于什么类型、训练集/测试集大概长什么样讲清楚。我先核对官方页面和数据说明，再用直白的话整理成一份比赛介绍。

> AGENT

官方说明确认了：这是一个“让你改进 Nemotron 推理能力”的题，不是一般 tabular 预测。接着我看一下这个工作区里有没有比赛数据或说明文件，这样能把“数据长什么样”讲得更具体。

> AGENT

本地数据已经看到了：`train.csv` 有 `9500` 条，列是 `id / prompt / answer`；`test.csv` 只有 `id / prompt`，看起来是示例格式，不是完整评测集。下面我抽几类题目看内容分布，确认它到底是哪种“推理数据”。

> AGENT

这份训练集不是传统分类表格，而是一批“文字题目 + 标准答案”。我再把题型分组一下，避免只看前几条造成误判。

> AGENT

**比赛在做什么** 这不是一般的表格预测比赛，也不是让你直接交一列答案。 它本质上是在比：谁能把 `NVIDIA Nemotron-3-Nano-30B` 这个基础模型，调得更会做“看例子找规律，再给出答案”的推理题。 官方要求是交一个 **LoRA adapter**。评测时，Kaggle 会把你的 LoRA 挂到固定的 Nemotron 基础模型上，让它逐题作答，再按正确率打分。官方说明在这里：[Kaggle 比赛页](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge)。 **数据是什么类型** 你这份本地数据不是传统机器学习那种“很多数值特征 + 一个标签”的数据。 它是 **文本题目数据**： - 训练集：[train.csv](/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge/train.csv) - 测试样例：[test.csv](/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge/test.csv) 结构很简单： | 文件 | 列 | |---|---| | `train.csv` | `id`, `prompt`, `answer` | | `test.csv` | `id`, `prompt` | 本地看到的数量是： | 文件 | 条数 | |---|---| | `train.csv` | 9500 | | `test.csv` | 3 | `prompt` 里已经包含了题目和若干示例，`answer` 是标准答案。 也就是说，每一条数据本身就是一道完整的“根据示例归纳规则”的题。 **这批题在考什么** 这套训练集主要是 6 类“规则归纳题”，每类数量都差不多： | 题型 | 数量 | 本质 | |---|---:|---| | 8-bit binary 变换 | 1602 | 看几个输入输出例子，推断位运算规则 | | 重力常数变化 | 1597 | 从样例反推出新的 `g`，再算自由落体距离 | | 单位转换 | 1594 | 从例子反推换算比例，再做新换算 | | 文本加解密 | 1576 | 从密文和明文样例推断替换规则 | | 数字转另一种记法 | 1576 | 目前看到本质上是 Roman numeral 一类的表示转换 | | 式子/符号变换 | 1555 | 从若干式子结果中归纳隐藏规则 | 所以这批数据的共同点是： - 都是 **合成的规则题** - 重点不是常识知识 - 重点是 **从上下文示例里找规律** - 输出通常很短，可能是数字、二进制串、单词短语、Roman numeral、符号串 **这类数据集在训练什么能力** 它要练的不是“背答案”，而是三件事： - 看懂题面里的少量示例 - 找出隐藏规则 - 按要求稳定输出最终答案 所以这个比赛更像是在测模型的： - 规则归纳能力 - 符号操作能力 - 短链条计算能力 - 输出格式稳定性 **集合怎么理解** 如果你说的“集合”是指数据切分，可以这样理解： - `train.csv`：公开训练题，有标准答案，拿来做微调、数据清洗、合成新数据、RL、prompt 设计 - `test.csv`：你本地这份只有 3 条，更像格式示例或本地检查样本 - 真正排行榜分数：不是靠提交 `test.csv` 答案，而是提交 **LoRA adapter**，让官方拿隐藏题来跑 **一句话总结** 这比赛不是在做传统预测，而是在做一类“给你几个例子，你要学会背后的规则”的推理增强。 数据本质上是 **文本形式的规则归纳题库**，目标是把 Nemotron 调得更擅长这类推理题，并且答得稳定、答得准。 如果你要，我可以继续把这 6 类题各自拆开，用具体例子告诉你： “题目长什么样、模型实际上要学会什么、哪些题最适合做合成数据或微调。”

> DEVELOPER

深入仔细的理解比赛内容 讨论我们怎么合成数据 怎么验证数据合成 等等 怎么使用数据

> AGENT

完成标准先定清楚： 1. 讲清比赛真正优化的对象、限制条件、评分方式与隐藏风险。 2. 把现有训练数据拆成可操作的题型与数据生成思路。 3. 给出一套可执行的方案：怎么合成、怎么验收、怎么用这些数据训练与筛选模型。

> AGENT

我会并行看两件事：一边把训练集按题型和答案形式拆细，一边核对官方评测细节，这样后面讨论合成策略时不会偏题。

> AGENT

一个关键问题需要先确认：每一题是在考“同一套固定规则”，还是“每题自带一套新的隐藏规则”。这会直接决定合成数据该怎么做。

> AGENT

我在补一层更细的结构判断：哪些题型是“固定规则反复出题”，哪些是“每题随机抽一套规则”。这会影响我们该用模板扩增，还是要自己造新的隐藏规则。

> AGENT

目前可以确认两件很重要的事： 一，这不是“固定答案库”，而是每题都有自己的一套例子；二，至少数值类题目明显是按参数随机生成的。接着我把文字题的词表和规则随机性也补上。

> AGENT

比赛的骨架已经比较清楚了，我在等两份并行分析收尾：一份专门盯数据结构，一份专门盯评测与提交约束。拿到后我会把“怎么造数据、怎么验数据、怎么用数据”连成一套。

> AGENT

**结论** 这个比赛的核心不是让模型记住题库，而是让它更擅长一件事： **看几条例子，推断这道题自己的隐藏规则，再给出一个很短的最终答案。** 所以数据工作的重点不是“多造题”，而是三件事： 1. 新题真的在训练这种能力。 2. 新题的答案一定正确，而且题目本身可解。 3. 验证方式能排除“看起来进步，其实只是记住套路”的假提升。 --- **比赛内容** 提交的不是答案表，而是一个挂在固定基础模型上的 LoRA。 评测时，官方会用你的 LoRA 去跑隐藏题，按正确率计分。答案会从模型生成的文字里抽取，优先看 `\boxed{}`，所以不仅要会做题，还要稳定把最终答案交对格式。 这点很重要，因为这类比赛常见的失分有两种： - 题会做，但最后答案格式不稳 - 本地验证很好，真正隐藏题不涨 --- **这份训练集到底是什么** 本地训练集 `train.csv` 有 `9500` 题，分成 6 类，数量几乎平均： | 类别 | 数量 | 本质 | |---|---:|---| | bit 变换 | 1602 | 看若干组 8-bit 输入输出，猜位运算规则 | | gravity | 1597 | 从例子反推出当前题目的重力常数，再算距离 | | unit conversion | 1594 | 从例子反推出换算比例 | | text cipher | 1576 | 从密文/明文例子推断解码规则 | | numeral system | 1576 | 数字改写成另一种表示法，当前公开集基本是 Roman numeral | | equation/symbol transformation | 1555 | 从少量示例中猜字符串变换规则 | 验证结果： - 没有重复 `prompt` - 每题都自带示例，不是空手解题 - `bit` 题一般给 7 到 10 个示例 - 其他题大多给 3 到 5 个示例 - 答案都很短：数字、二进制串、短词组、Roman numeral、符号串 这说明它不是知识问答，而是**规则归纳题**。 --- **最关键的判断** 不是所有题型都值得同样投入。 | 题型 | 合成价值 | 原因 | |---|---|---| | `gravity` | 高 | 规则明确，答案可直接算，最容易做干净 | | `unit` | 高 | 同上，容易做边界题 | | `numeral` | 中 | 很规整，容易做，但上限有限 | | `bit` | 高 | 很适合程序生成，但必须控制规则空间 | | `text` | 中高 | 能做，但很容易造出看似合理、实际无效的题 | | `equation` | 中 | 最容易做偏，建议最后处理 | **推荐顺序** 1. 先做 `gravity / unit / numeral` 2. 再做 `bit` 3. 最后做 `text / equation` 推荐原因：前四类最容易保证题真、答案真、难度可控；后两类最容易把模型教偏。 --- **怎么合成数据** 只有 3 条路： | 方案 | 做法 | 优点 | 缺点 | 建议 | |---|---|---|---|---| | A | 程序直接出题和算答案 | 最干净、最好验证 | 前期要设计规则 | 推荐主线 | | B | 让大模型仿写题目 | 快 | 最容易出错题、脏题 | 不推荐主线 | | C | 规则由程序保证，题面再润色 | 兼顾正确性和外观 | 稍复杂 | 可作为辅助 | **推荐：A 为主，C 为辅。** 这个比赛最怕的是“题面看着像，但底层训练的不是同一种能力”。 --- **每类题怎么造才有效** **1. gravity** 做法： - 每题随机一个 `g` - 给 3 到 5 个 `(t, d)` 示例 - 再问一个新的 `t` - 统一保留两位小数 重点不是多，而是补这些情况： - `t` 很接近 - 只有少量示例 - 刚好卡在四舍五入边界 **2. unit** 本地数据看起来基本是每题一个比例 `y = kx`。 做法： - 比例范围贴近原始训练集 - 再少量做轻微扩展 - 重点补接近边界和容易舍入出错的样本 **3. numeral** 这类最容易做对，但收益未必最大。 建议： - 保留和原始范围一致的一批 - 少量往更大范围扩 - 主要拿来练稳定输出，不要押太重 **4. bit** 这里最重要的不是数量，是规则设计。 建议先限定一个干净的小规则库，例如： - rotate - shift - xor 固定掩码 - bit reverse - 邻位组合 - 少量简单组合 必须加一道检查： **当前给出的示例，是否足以唯一锁定正确规则。** 否则会出现一种坏题：题目自己就不够信息量，模型答错不代表能力差。 **5. text** 不要让模型自由编。 推荐只做可逆、可验证的生成方式，例如： - 词表映射 - 固定替换表 - 受控的字符位移 - 受控的词级变换 必须满足： - 编码和解码可完全还原 - 目标句里的每个词都能从示例推出 - 不能靠英文词频去猜 **6. equation** 这类建议拆开，不要混着造： - 数字式变换 - 符号串变换 宁可少做几种，也不要做成很多互相没有共同规律的怪题。 --- **怎么验证合成数据** 这里比“会不会生成”更重要。 验证至少要分 4 层。 **1. 规则正确** 每题都要能程序复算： - 每个示例都符合规则 - 最终答案符合规则 - 小数处理一致 - text 可逆 - bit 不歧义 **2. 分布接近比赛** 至少对齐这些统计： - 六大类比例 - 每题示例数 - 数值范围 - 小数位数 - 文本长度 - 答案长度 - bit 和 equation 的复杂度 如果差太远，题再多也可能无效。 **3. 验证集切法正确** 最容易犯的错是随机切分。 这样同一种底层规则可能同时出现在训练和验证里，分数会虚高。 更好的切法是： - 按规则家族切 - 按生成参数切 - 按模板切 - 按词表或操作符切 目标是让验证集里保留一部分“没见过的规则实例”。 **4. 增益是否稳定** 判断一批合成数据有没有价值，不看一次分数，要看： - 原始验证集是否涨 […]
