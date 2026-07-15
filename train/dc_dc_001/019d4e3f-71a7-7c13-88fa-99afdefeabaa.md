> DEVELOPER

理解一下这个比赛的数据 给我讲讲什么类型的数据 是在做什么 集合Skip to
content
Kaggle

Create
Home

Competitions

Datasets

Models

Benchmarks

Game Arena

Code

Discussions

Learn

More

Your Work


Viewed

NVIDIA Nemotron Model Reasoning Challenge


It seems the KV cache is not enabled during RL training


Train locally and get lower scores.


Inquiry regarding inference non-determinism and Open Progress Prize fairness


ACCIDENT @ CVPR


Edited

baseline-bird


LB 35.9 with Regex corrections (Public Model)


LB 35.9 Ensembling & Post Processing Baseline


baseline


Data Preprocessing


View Active Events

Search

NVIDIA · Featured Prediction Competition · 2 months to go
NVIDIA Nemotron Model Reasoning Challenge
Advance reasoning techniques using NVIDIA Nemotron open models on a novel benchmark


NVIDIA Nemotron Model Reasoning Challenge

Submit Prediction
Overview
Develop techniques that improve reasoning accuracy using NVIDIA Nemotron models.

Participants will experiment with prompting, data pipelines, and lightweight fine-tuning while evaluating their approaches on a new reasoning benchmark developed by NVIDIA Research.

Start

17 days ago
Close
2 months to go
Merger & Entry
Description
Reasoning benchmarks are a useful way to measure progress on structured tasks. When approaches and results are shared openly, the community can compare methods, reproduce improvements, and iterate more effectively.

Today, reasoning improvements are explored across many independent efforts - often using different datasets, prompts, and evaluation setups - making direct comparison difficult. A shared benchmark and common baseline model allow techniques to be tested and compared more consistently.

While language models perform strongly on many tasks, structured reasoning benchmarks remain an active area of research and optimization.

In this competition, participants will work from a shared Nemotron 3 Nano baseline and a novel reasoning benchmark developed by NVIDIA Research. Nemotron provides an open foundation for this challenge, including openly available models, datasets, and training recipes that participants can build on or adapt within their own workflows.

You may experiment with:

Prompting strategies
Data filtering and curation
Synthetic data generation
Reinforcement learning
Lightweight fine-tuning
Or other approaches of your choice
Participants may use any training framework, tooling, or workflow to produce their LoRA adapter. NVIDIA-provided recipes are optional starting points - competitors are free to use other ecosystems and libraries (e.g., Hugging Face, Unsloth, Axolotl, TRL, or similar tooling).

The only requirement is that the final submission produces a compatible LoRA adapter for the Nemotron-3-Nano-30B base model.

Multiple valid solution paths are expected. Clear documentation - including notebooks and write-ups - is encouraged (and required for prize eligibility) to support reproducibility and communal learning.

By bringing models, datasets, and evaluation into an open, shared environment, this challenge creates an opportunity for collaborative iteration - strengthening open reasoning workflows that others can study, reuse, and extend.

Evaluation
Submissions are evaluated based on their Accuracy in solving the provided tasks. The NVIDIA Nemotron-3-Nano-30B model is loaded with your LoRA adapter (which must include an adapter_config.json) using the vLLM inference engine. For each test case, the model is prompted to generate a response and instructed to place its final answer within a \boxed{} LaTeX command. The metric extracts the final answer from the generated text, prioritizing content within the boxed format while falling back to other heuristic patterns or the last numeric value found. A prediction is graded as correct if it matches the ground truth either exactly as a string or within a relative numerical tolerance of 
. The final score is the proportion of correctly answered questions.

You may view the implementation of the metric here: NVIDIA Nemotron Metric. It is being run with the following parameters:

Parameter	Value
max_lora_rank	32
max_tokens	7680
top_p	1.0
temperature	0.0
max_num_seqs	64
gpu_memory_utilization	0.85
max_model_len	8192
Submitting
You must submit a LoRA adapter of rank at most 32 for the NVIDIA Nemotron-3-Nano-30B model packaged into a submission.zip file. You may consider adapting the NVIDIA Nemotron Submission Demo to produce your submission.

Timeline
March 16, 2026 - Start Date.
April 9, 2026 - Midpoint Cut-off Date
June 8, 2026 - Entry Deadline. You must accept the competition rules before this date in order to compete.
June 8, 2026 - Team Merger Deadline. This is the last day participants may join or merge teams.
June 15, 2026 - Competition End Date & Final Submission Deadline.
All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary.

Prizes
To be eligible for any prize, teams must publish a public Kaggle notebook and solution write-up documenting the methods, datasets, and techniques used to produce the submission. Submissions without qualifying public documentation may be deemed ineligible for prizes.

Final Leaderboard Prizes

1st Place - $25,000 + 5 DGX Sparks
2nd Place - $15,000 + 2 DGX Sparks
3rd Place - $5,000 + 1 DGX Sparks
Note: A total of eight (8) NVIDIA DGX Spark systems (Approximate Retail Value: $4,699 per system) will be awarded based on final leaderboard placement. If any team has fewer eligible members than the number of DGX Spark systems allocated for that placement, or if any team member is ineligible to receive hardware due to export, shipping, or regional restrictions, any remaining units will cascade to the next highest-ranked teams on the final leaderboard until all eight (8) DGX Spark systems have been awarded.

Each eligible participant may receive no more than one (1) DGX Spark, and only officially registered team members are eligible to receive hardware prizes. NVIDIA reserves the right to verify team membership and eligibility prior to awarding hardware prizes.

Open Progress Prize (Mid-Competition Milestone)
Open Progress Prize: $5,000 + 1 DGX Sparks

Awarded to the team with the highest leaderboard score as of the Midpoint Cut-off Date: April 9, 2026.
Methodology submissions Cut-off Date: April 16, 2026.
Winners will be announced during Cloud NEXT (April 22-24, 2026)
If the top-ranked submission at the cutoff date does not meet these requirements, the prize will be awarded to the next highest eligible submission.

In the event of a tie, the prize will be awarded to the team whose qualifying submission was submitted earliest.

Each eligible participant may receive no more than one (1) DGX Spark.

Open Contribution Awards
The Open Contribution Awards recognize techniques that meaningfully advance reasoning performance using Nemotron models.

Three awards will be granted:

Best Data/Synthetic Data Method - 1 DGX Spark
Best RL Method - 1 DGX Spark
Best Fine-tuning Method - 1 DGX Spark
Participants must submit their entry for these awards through this form linking to their notebook and clearly identifying the category being entered.

Only submissions ranking within the top 10% of the final leaderboard will be considered for Open Contribution Awards.

Compute Powered by NVIDIA Blackwell on Google Cloud
We're excited to partner with Google Cloud to offer the G4 VMs powered by NVIDIA RTX PRO 6000 Blackwell Server Edition GPUs as the compute backbone for this challenge. G4 VMs are a strong fit for both fine‑tuning and high‑throughput inference with Nemotron models so you can iterate quickly on prompts, data pipelines, and tuning strategies while evaluating performance on real benchmarks.

NVIDIA RTX PRO 6000 Blackwell GPUs provide the performance and memory needed to serve open reasoning models efficiently at inference time, enabling responsive evaluation runs and rapid leaderboard iteration as you improve your Nemotron variants. Learn more about the underlying Google Cloud G4 VM and its capabilities here.

Citation
Jamil C Semaan, Jean-Francois Puget, Christof Henkel, Yi Dong, Addison Howard, Ashley Oldacre, Ryan Holbrook, Chris Alexiuk, and Rebecca Kao. NVIDIA Nemotron Model Reasoning Challenge. https://kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge, 2026. Kaggle.


Cite
Competition Host
NVIDIA

Prizes & Awards
$106,388

Awards Points & Medals

Participation
9,512 Entrants

1,701 Participants

1,504 Teams

10,009 Submissions

Tags
Reasoning
Deep Learning
Pre-Trained Model
Custom Metric
Table of Contents 比赛介绍 给我讲讲

> AGENT

需求是把这个比赛在做什么、数据属于什么类型、训练集/测试集大概长什么样讲清楚。我先核对官方页面和数据说明，再用直白的话整理成一份比赛介绍。

> AGENT

官方说明确认了：这是一个“让你改进 Nemotron 推理能力”的题，不是一般 tabular 预测。接着我看一下这个工作区里有没有比赛数据或说明文件，这样能把“数据长什么样”讲得更具体。

> AGENT

本地数据已经看到了：`train.csv` 有 `9500` 条，列是 `id / prompt / answer`；`test.csv` 只有 `id / prompt`，看起来是示例格式，不是完整评测集。下面我抽几类题目看内容分布，确认它到底是哪种“推理数据”。

> TOOL

tool_use exec_command
```json
{
  "cmd": "pwd && rg --files -g '!*node_modules*' -g '!*.parquet' -g '!*.bin' -g '!*.pt' -g '!*.safetensors'",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"train|test|validation|dataset|competition|Nemotron|Kaggle\" -S .",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,8p' train.csv",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,8p' test.csv",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv\nfor fn in ['train.csv','test.csv']:\n    with open(fn,newline='') as f:\n        r=csv.reader(f)\n        header=next(r)\n        n=sum(1 for _ in r)\n    print(fn, 'rows=', n, 'cols=', header)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

这份训练集不是传统分类表格，而是一批“文字题目 + 标准答案”。我再把题型分组一下，避免只看前几条造成误判。

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, itertools, textwrap\nwith open('train.csv', newline='') as f:\n    r=csv.DictReader(f)\n    for i,row in zip(range(5), r):\n        print('ID', row['id'])\n        print(textwrap.shorten(row['prompt'].replace('\\n',' '), width=220, placeholder=' ...'))\n        print('ANSWER:', row['answer'][:120])\n        print('---')\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, random, textwrap\nrows=[]\nwith open('train.csv', newline='') as f:\n    r=list(csv.DictReader(f))\nfor idx in [100,500,1000,2500,5000,8000]:\n    row=r[idx]\n    print('ID', row['id'])\n    print(textwrap.shorten(row['prompt'].replace('\\n',' '), width=220, placeholder=' ...'))\n    print('ANSWER:', row['answer'][:120])\n    print('---')\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\npatterns=collections.Counter()\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        p=row['prompt']\n        if 'Alice\\'s Wonderland' in p or 'bit manipulation' in p:\n            patterns['bit transformation']+=1\n        elif 'logic puzzle' in p or 'truth-teller' in p or 'liar' in p:\n            patterns['logic puzzle']+=1\n        elif 'grid' in p or 'matrix' in p:\n            patterns['grid/matrix']+=1\n        elif 'equation' in p or 'solve for' in p:\n            patterns['equation/algebra']+=1\n        elif 'sequence' in p or 'next number' in p:\n            patterns['sequence']+=1\n        elif 'geometry' in p or 'triangle' in p:\n            patterns['geometry']+=1\n        else:\n            patterns['other']+=1\nprint(patterns.most_common(20))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

**比赛在做什么**

这不是一般的表格预测比赛，也不是让你直接交一列答案。  
它本质上是在比：谁能把 `NVIDIA Nemotron-3-Nano-30B` 这个基础模型，调得更会做“看例子找规律，再给出答案”的推理题。

官方要求是交一个 **LoRA adapter**。评测时，Kaggle 会把你的 LoRA 挂到固定的 Nemotron 基础模型上，让它逐题作答，再按正确率打分。官方说明在这里：[Kaggle 比赛页](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge)。

**数据是什么类型**

你这份本地数据不是传统机器学习那种“很多数值特征 + 一个标签”的数据。  
它是 **文本题目数据**：

- 训练集：[train.csv](/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge/train.csv)
- 测试样例：[test.csv](/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge/test.csv)

结构很简单：

| 文件 | 列 |
|---|---|
| `train.csv` | `id`, `prompt`, `answer` |
| `test.csv` | `id`, `prompt` |

本地看到的数量是：

| 文件 | 条数 |
|---|---|
| `train.csv` | 9500 |
| `test.csv` | 3 |

`prompt` 里已经包含了题目和若干示例，`answer` 是标准答案。  
也就是说，每一条数据本身就是一道完整的“根据示例归纳规则”的题。

**这批题在考什么**

这套训练集主要是 6 类“规则归纳题”，每类数量都差不多：

| 题型 | 数量 | 本质 |
|---|---:|---|
| 8-bit binary 变换 | 1602 | 看几个输入输出例子，推断位运算规则 |
| 重力常数变化 | 1597 | 从样例反推出新的 `g`，再算自由落体距离 |
| 单位转换 | 1594 | 从例子反推换算比例，再做新换算 |
| 文本加解密 | 1576 | 从密文和明文样例推断替换规则 |
| 数字转另一种记法 | 1576 | 目前看到本质上是 Roman numeral 一类的表示转换 |
| 式子/符号变换 | 1555 | 从若干式子结果中归纳隐藏规则 |

所以这批数据的共同点是：

- 都是 **合成的规则题**
- 重点不是常识知识
- 重点是 **从上下文示例里找规律**
- 输出通常很短，可能是数字、二进制串、单词短语、Roman numeral、符号串

**这类数据集在训练什么能力**

它要练的不是“背答案”，而是三件事：

- 看懂题面里的少量示例
- 找出隐藏规则
- 按要求稳定输出最终答案

所以这个比赛更像是在测模型的：

- 规则归纳能力
- 符号操作能力
- 短链条计算能力
- 输出格式稳定性

**集合怎么理解**

如果你说的“集合”是指数据切分，可以这样理解：

- `train.csv`：公开训练题，有标准答案，拿来做微调、数据清洗、合成新数据、RL、prompt 设计
- `test.csv`：你本地这份只有 3 条，更像格式示例或本地检查样本
- 真正排行榜分数：不是靠提交 `test.csv` 答案，而是提交 **LoRA adapter**，让官方拿隐藏题来跑

**一句话总结**

这比赛不是在做传统预测，而是在做一类“给你几个例子，你要学会背后的规则”的推理增强。  
数据本质上是 **文本形式的规则归纳题库**，目标是把 Nemotron 调得更擅长这类推理题，并且答得稳定、答得准。

如果你要，我可以继续把这 6 类题各自拆开，用具体例子告诉你：  
“题目长什么样、模型实际上要学会什么、哪些题最适合做合成数据或微调。”

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nc=collections.Counter()\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        first=row['prompt'].split('\\n',1)[0].strip()\n        c[first]+=1\nfor k,v in c.most_common(20):\n    print(v, '|', k)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, collections\nc=collections.Counter()\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        p=row['prompt']\n        # first sentence until period\n        sent=p.split('. ',1)[0].strip()\n        c[sent]+=1\nfor k,v in c.most_common(30):\n    print(v, '|', k)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nc=collections.Counter()\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        p=row['prompt']\n        m=re.match(r\"In Alice's Wonderland, ([^.]+)\\.\", p)\n        c[m.group(1) if m else 'OTHER'] += 1\nfor k,v in c.most_common(50):\n    print(v, '|', k)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 6000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv\nseen=set()\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        first=row['prompt'].split('\\n',1)[0].strip()\n        if first not in seen:\n            seen.add(first)\n            print('TYPE:', first)\n            print(row['prompt'][:1200])\n            print('ANSWER:', row['answer'])\n            print('='*80)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, statistics\nans_lens=[]\nprompt_lens=[]\nwith open('train.csv', newline='') as f:\n    for row in csv.DictReader(f):\n        ans_lens.append(len(row['answer']))\n        prompt_lens.append(len(row['prompt']))\nprint('prompt chars avg', round(statistics.mean(prompt_lens),1), 'median', statistics.median(prompt_lens), 'min', min(prompt_lens), 'max', max(prompt_lens))\nprint('answer chars avg', round(statistics.mean(ans_lens),1), 'median', statistics.median(ans_lens), 'min', min(ans_lens), 'max', max(ans_lens))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

深入仔细的理解比赛内容 讨论我们怎么合成数据 怎么验证数据合成 等等 怎么使用数据

> AGENT

完成标准先定清楚：

1. 讲清比赛真正优化的对象、限制条件、评分方式与隐藏风险。  
2. 把现有训练数据拆成可操作的题型与数据生成思路。  
3. 给出一套可执行的方案：怎么合成、怎么验收、怎么用这些数据训练与筛选模型。

> AGENT

我会并行看两件事：一边把训练集按题型和答案形式拆细，一边核对官方评测细节，这样后面讨论合成策略时不会偏题。

> TOOL

tool_use update_plan
```json
{
  "explanation": "先把比赛约束、数据结构、可行的数据合成与验证框架拆开分析，再整理成一套可执行方案。",
  "plan": [
    {
      "step": "检查本地数据分布与题型特征",
      "status": "in_progress"
    },
    {
      "step": "核对官方评测与提交约束",
      "status": "pending"
    },
    {
      "step": "整理数据合成、验证、使用策略",
      "status": "pending"
    }
  ]
}
```

> AGENT

一个关键问题需要先确认：每一题是在考“同一套固定规则”，还是“每题自带一套新的隐藏规则”。这会直接决定合成数据该怎么做。

> TOOL

tool_use spawn_agent
```json
{
  "agent_type": "explorer",
  "model": "gpt-5.4-mini",
  "reasoning_effort": "medium",
  "fork_context": true,
  "message": "你负责只做数据侧分析。阅读工作区中的 train.csv/test.csv，输出：1) 各题型数量；2) 每类题的输入结构、目标输出结构；3) 每类题最可能的底层规则；4) 对数据合成最有价值的观察。不要改文件，只给结论。"
}
```

> TOOL

tool_use spawn_agent
```json
{
  "agent_type": "explorer",
  "model": "gpt-5.4-mini",
  "reasoning_effort": "medium",
  "fork_context": true,
  "message": "你负责只做比赛规则与评测侧分析。基于用户给的比赛说明和必要的官方网页信息，整理：1) 提交物是什么；2) 评分怎么提取答案；3) 哪些训练策略与输出策略容易踩坑；4) 对数据合成与验证有什么直接约束。不要改文件，只给结论。"
}
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, collections, re, statistics\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# group by first line\nc=collections.Counter(r['prompt'].split('\\n',1)[0].strip() for r in rows)\nprint('TYPE COUNTS')\nfor k,v in c.items():\n    print(v, '|', k)\nprint('\\nANSWER SHAPES')\nsh=collections.Counter()\nfor r in rows:\n    a=r['answer']\n    if re.fullmatch(r'[01]{8}', a): sh['8-bit binary']+=1\n    elif re.fullmatch(r'[IVXLCDM]+', a): sh['roman numeral']+=1\n    elif re.fullmatch(r'-?\\d+(?:\\.\\d+)?', a): sh['number']+=1\n    elif re.fullmatch(r'[A-Za-z]+(?: [A-Za-z]+)*', a): sh['words']+=1\n    else: sh['symbols/mixed']+=1\nprint(sh)\nprint('\\nPROMPT LENGTH')\npl=[len(r['prompt']) for r in rows]\nprint(min(pl), statistics.median(pl), round(statistics.mean(pl),1), max(pl))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nexamples={}\nfor row in csv.DictReader(open('train.csv', newline='')):\n    key=row['prompt'].split('\\n',1)[0].strip()\n    if key not in examples:\n        examples[key]=row\nfor k,row in examples.items():\n    print('\\nTYPE:', k)\n    # extract example pairs count roughly\n    lines=row['prompt'].splitlines()\n    ex=[ln for ln in lines if '->' in ln or 'For t =' in ln or 'becomes' in ln or '=' in ln]\n    print('num clue lines:', len(ex))\n    print('sample answer:', row['answer'])\n    print('last line:', lines[-1])\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

我在补一层更细的结构判断：哪些题型是“固定规则反复出题”，哪些是“每题随机抽一套规则”。这会影响我们该用模板扩增，还是要自己造新的隐藏规则。

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, collections\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# duplicate full prompts?\nprompts=[r['prompt'] for r in rows]\nprint('duplicate prompts', len(prompts)-len(set(prompts)))\n# duplicate answers only not meaningful, but per type maybe answer diversity\nbytype=collections.defaultdict(list)\nfor r in rows:\n    t=r['prompt'].split('\\n',1)[0]\n    bytype[t].append(r['answer'])\nfor t,ans in bytype.items():\n    print('\\n',t[:60])\n    print('rows', len(ans), 'unique answers', len(set(ans)))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# compare prompt skeletons within type\nfor t in list({r['prompt'].split('\\n',1)[0] for r in rows}):\n    sample=[r for r in rows if r['prompt'].split('\\n',1)[0]==t][:3]\n    print('\\nTYPE:', t)\n    for i,r in enumerate(sample,1):\n        lines=r['prompt'].splitlines()\n        print('sample',i,'last line:',lines[-1])\n        print('example block hashlike:', hash('\\n'.join(lines[2:-1])))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# inspect numeric precision by type\nfor t in sorted({r['prompt'].split('\\n',1)[0] for r in rows}):\n    vals=[r['answer'] for r in rows if r['prompt'].split('\\n',1)[0]==t]\n    dec=sum(1 for v in vals if '.' in v)\n    print(t[:70], 'decimal', dec, 'integer', len(vals)-dec)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

目前可以确认两件很重要的事：  
一，这不是“固定答案库”，而是每题都有自己的一套例子；二，至少数值类题目明显是按参数随机生成的。接着我把文字题的词表和规则随机性也补上。

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, math, statistics\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# unit conversion ratio inference\nratios=[]\nerrs=[]\nfor r in rows:\n    p=r['prompt']\n    if 'secret unit conversion' not in p: continue\n    pairs=re.findall(r'([0-9]+(?:\\.[0-9]+)?) m becomes ([0-9]+(?:\\.[0-9]+)?)', p)\n    rs=[round(float(b)/float(a),6) for a,b in pairs]\n    ratios.append(statistics.mean(rs))\n    errs.append(max(rs)-min(rs))\nprint('unit conversion max within-row ratio spread', max(errs))\nprint('sample ratios', [round(x,4) for x in ratios[:10]])\nprint('unique rounded ratios', len(set(round(x,2) for x in ratios)))\n# gravity g inference\nGs=[]; Gerr=[]\nfor r in rows:\n    p=r['prompt']\n    if 'gravitational constant' not in p: continue\n    pairs=re.findall(r'For t = ([0-9]+(?:\\.[0-9]+)?)s, distance = ([0-9]+(?:\\.[0-9]+)?) m', p)\n    gs=[round(2*float(d)/(float(t)**2),6) for t,d in pairs]\n    Gs.append(statistics.mean(gs))\n    Gerr.append(max(gs)-min(gs))\nprint('gravity max within-row g spread', max(Gerr))\nprint('sample g', [round(x,3) for x in Gs[:10]])\nprint('unique rounded g', len(set(round(x,2) for x in Gs)))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re\nrows=list(csv.DictReader(open('train.csv', newline='')))\nnums=[]\nfor r in rows:\n    if 'different numeral system' not in r['prompt']: continue\n    m=re.search(r'Now, write the number ([0-9]+) in the Wonderland numeral system\\.', r['prompt'])\n    if m: nums.append(int(m.group(1)))\nprint('roman targets min/max', min(nums), max(nums))\nprint('unique targets', len(set(nums)))\nprint('first 30 sorted unique', sorted(set(nums))[:30])\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nrows=list(csv.DictReader(open('train.csv', newline='')))\n# equation task target shapes\nc=collections.Counter()\nfor r in rows:\n    if 'transformation rules is applied to equations' not in r['prompt']: continue\n    target=r['prompt'].split('Now, determine the result for: ',1)[1].strip()\n    if re.fullmatch(r'[0-9]+[+\\-*/<>][0-9]+', target): c['numeric expr']+=1\n    elif re.fullmatch(r'[\\\\`\\'\"!@#$%^&*()\\[\\]{}<>/?|+=_\\-]+', target): c['symbol expr']+=1\n    else: c['mixed expr']+=1\nprint(c)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

比赛的骨架已经比较清楚了，我在等两份并行分析收尾：一份专门盯数据结构，一份专门盯评测与提交约束。拿到后我会把“怎么造数据、怎么验数据、怎么用数据”连成一套。

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\nsrc=collections.Counter(); tgt=collections.Counter(); lens=collections.Counter()\nfor r in csv.DictReader(open('train.csv', newline='')):\n    p=r['prompt']\n    if 'secret encryption rules' not in p: continue\n    for enc,dec in re.findall(r'([a-z ]+) -> ([a-z ]+)', p):\n        for w in enc.split(): src[w]+=1\n        for w in dec.split(): tgt[w]+=1\n        lens[(len(enc.split()), len(dec.split()))]+=1\n    for w in r['answer'].split(): tgt[w]+=1\nprint('target vocab size', len(tgt))\nprint('most common target words', tgt.most_common(40))\nprint('source vocab size', len(src))\nprint('word-count mapping shapes', lens.most_common(10))\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections, string\n# collect all chars from equation task answers/targets\nchars=collections.Counter()\nfor r in csv.DictReader(open('train.csv', newline='')):\n    if 'transformation rules is applied to equations' not in r['prompt']: continue\n    target=r['prompt'].split('Now, determine the result for: ',1)[1]\n    ans=r['answer']\n    chars.update(target)\n    chars.update(ans)\nprint(chars)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 3000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python - <<'PY'\nimport csv, re, collections\n# inspect number of examples per prompt for each type\nbytype=collections.defaultdict(collections.Counter)\nfor r in csv.DictReader(open('train.csv', newline='')):\n    p=r['prompt']\n    t=p.split('\\n',1)[0]\n    if 'bit manipulation' in p:\n        n=len(re.findall(r'([01]{8}) -> ([01]{8})', p))\n    elif 'secret encryption rules' in p:\n        n=len(re.findall(r'([a-z ]+) -> ([a-z ]+)', p))\n    elif 'different numeral system' in p:\n        n=len(re.findall(r'([0-9]+) -> ([IVXLCDM]+)', p))\n    elif 'unit conversion' in p:\n        n=len(re.findall(r'([0-9]+(?:\\.[0-9]+)?) m becomes ([0-9]+(?:\\.[0-9]+)?)', p))\n    elif 'gravitational constant' in p:\n        n=len(re.findall(r'For t = ([0-9]+(?:\\.[0-9]+)?)s, distance = ([0-9]+(?:\\.[0-9]+)?) m', p))\n    else:\n        n=len(re.findall(r'^.+ = .+$', p, re.M)) - 1\n    bytype[t][n]+=1\nfor t,c in bytype.items():\n    print('\\nTYPE', t[:60])\n    print(c)\nPY",
  "workdir": "/Users/user_0a329be7/Downloads/nvidia-nemotron-model-reasoning-challenge",
  "yield_time_ms": 1000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use wait_agent
```json
{
  "targets": [
    "019d4e42-933d-7b30-9056-80ac3b8fbe2a",
    "019d4e42-9364-7910-9e0d-05df8a7ef87a"
  ],
  "timeout_ms": 30000
}
```

> AGENT

**结论**

这个比赛的核心不是让模型记住题库，而是让它更擅长一件事：  
**看几条例子，推断这道题自己的隐藏规则，再给出一个很短的最终答案。**

所以数据工作的重点不是“多造题”，而是三件事：

1. 新题真的在训练这种能力。  
2. 新题的答案一定正确，而且题目本身可解。  
3. 验证方式能排除“看起来进步，其实只是记住套路”的假提升。

---

**比赛内容**

提交的不是答案表，而是一个挂在固定基础模型上的 LoRA。  
评测时，官方会用你的 LoRA 去跑隐藏题，按正确率计分。答案会从模型生成的文字里抽取，优先看 `\boxed{}`，所以不仅要会做题，还要稳定把最终答案交对格式。

这点很重要，因为这类比赛常见的失分有两种：

- 题会做，但最后答案格式不稳
- 本地验证很好，真正隐藏题不涨

---

**这份训练集到底是什么**

本地训练集 `train.csv` 有 `9500` 题，分成 6 类，数量几乎平均：

| 类别 | 数量 | 本质 |
|---|---:|---|
| bit 变换 | 1602 | 看若干组 8-bit 输入输出，猜位运算规则 |
| gravity | 1597 | 从例子反推出当前题目的重力常数，再算距离 |
| unit conversion | 1594 | 从例子反推出换算比例 |
| text cipher | 1576 | 从密文/明文例子推断解码规则 |
| numeral system | 1576 | 数字改写成另一种表示法，当前公开集基本是 Roman numeral |
| equation/symbol transformation | 1555 | 从少量示例中猜字符串变换规则 |

验证结果：

- 没有重复 `prompt`
- 每题都自带示例，不是空手解题
- `bit` 题一般给 7 到 10 个示例
- 其他题大多给 3 到 5 个示例
- 答案都很短：数字、二进制串、短词组、Roman numeral、符号串

这说明它不是知识问答，而是**规则归纳题**。

---

**最关键的判断**

不是所有题型都值得同样投入。

| 题型 | 合成价值 | 原因 |
|---|---|---|
| `gravity` | 高 | 规则明确，答案可直接算，最容易做干净 |
| `unit` | 高 | 同上，容易做边界题 |
| `numeral` | 中 | 很规整，容易做，但上限有限 |
| `bit` | 高 | 很适合程序生成，但必须控制规则空间 |
| `text` | 中高 | 能做，但很容易造出看似合理、实际无效的题 |
| `equation` | 中 | 最容易做偏，建议最后处理 |

**推荐顺序**

1. 先做 `gravity / unit / numeral`
2. 再做 `bit`
3. 最后做 `text / equation`

推荐原因：前四类最容易保证题真、答案真、难度可控；后两类最容易把模型教偏。

---

**怎么合成数据**

只有 3 条路：

| 方案 | 做法 | 优点 | 缺点 | 建议 |
|---|---|---|---|---|
| A | 程序直接出题和算答案 | 最干净、最好验证 | 前期要设计规则 | 推荐主线 |
| B | 让大模型仿写题目 | 快 | 最容易出错题、脏题 | 不推荐主线 |
| C | 规则由程序保证，题面再润色 | 兼顾正确性和外观 | 稍复杂 | 可作为辅助 |

**推荐：A 为主，C 为辅。**

这个比赛最怕的是“题面看着像，但底层训练的不是同一种能力”。

---

**每类题怎么造才有效**

**1. gravity**

做法：

- 每题随机一个 `g`
- 给 3 到 5 个 `(t, d)` 示例
- 再问一个新的 `t`
- 统一保留两位小数

重点不是多，而是补这些情况：

- `t` 很接近
- 只有少量示例
- 刚好卡在四舍五入边界

**2. unit**

本地数据看起来基本是每题一个比例 `y = kx`。  
做法：

- 比例范围贴近原始训练集
- 再少量做轻微扩展
- 重点补接近边界和容易舍入出错的样本

**3. numeral**

这类最容易做对，但收益未必最大。  
建议：

- 保留和原始范围一致的一批
- 少量往更大范围扩
- 主要拿来练稳定输出，不要押太重

**4. bit**

这里最重要的不是数量，是规则设计。  
建议先限定一个干净的小规则库，例如：

- rotate
- shift
- xor 固定掩码
- bit reverse
- 邻位组合
- 少量简单组合

必须加一道检查：  
**当前给出的示例，是否足以唯一锁定正确规则。**

否则会出现一种坏题：题目自己就不够信息量，模型答错不代表能力差。

**5. text**

不要让模型自由编。  
推荐只做可逆、可验证的生成方式，例如：

- 词表映射
- 固定替换表
- 受控的字符位移
- 受控的词级变换

必须满足：

- 编码和解码可完全还原
- 目标句里的每个词都能从示例推出
- 不能靠英文词频去猜

**6. equation**

这类建议拆开，不要混着造：

- 数字式变换
- 符号串变换

宁可少做几种，也不要做成很多互相没有共同规律的怪题。

---

**怎么验证合成数据**

这里比“会不会生成”更重要。  
验证至少要分 4 层。

**1. 规则正确**

每题都要能程序复算：

- 每个示例都符合规则
- 最终答案符合规则
- 小数处理一致
- text 可逆
- bit 不歧义

**2. 分布接近比赛**

至少对齐这些统计：

- 六大类比例
- 每题示例数
- 数值范围
- 小数位数
- 文本长度
- 答案长度
- bit 和 equation 的复杂度

如果差太远，题再多也可能无效。

**3. 验证集切法正确**

最容易犯的错是随机切分。  
这样同一种底层规则可能同时出现在训练和验证里，分数会虚高。

更好的切法是：

- 按规则家族切
- 按生成参数切
- 按模板切
- 按词表或操作符切

目标是让验证集里保留一部分“没见过的规则实例”。

**4. 增益是否稳定**

判断一批合成数据有没有价值，不看一次分数，要看：

- 原始验证集是否涨
- 哪些题型涨
- 多次训练是否都稳定

只涨一次，不算数。

---

**怎么使用这些数据**

不建议一锅炖。  
建议分 3 层。

**第一层：先把原始数据用透**

先做这几件事：

- 分题型评估
- 找最弱的类
- 单独检查最终答案格式稳定性

很多时候，这一步的收益比盲目扩数据更大。

**第二层：加入可验证的合成数据**

优先加入：

- `gravity`
- `unit`
- `numeral`
- 少量高质量 `bit`

原则：

- 原始数据始终是主体
- 合成数据是补充
- 不让合成量远大于原始量

否则模型会学你生成器的习惯，而不是比赛分布。

**第三层：只留下真正有用的合成集**

每一批新增数据都做小规模对比。  
只保留三类：

- 能提高总分
- 能明显补强某一弱项
- 不拖累其他题型

没稳定收益，直接删。

---

**推荐方案**

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| 只用公开训练集 | 简单、干净 | 上限低 | 不推荐 |
| 大量通用合成题一起混 | 数据量大 | 很容易造偏 | 不推荐 |
| 按题型分开生成、分开验证、再按比例混合 | 最稳、最贴比赛目标 | 设计更费心 | 推荐 |

---

**最该防的坑**

1. 用随机切分验证集，误判效果。  
2. 合成很多题，但底层规则其实很单一。  
3. 让大模型自由造题，把错题也混进训练。  
4. 合成数据太多，盖过原始分布。  
5. 只看总分，不看分题型结果。  
6. 忽略最终答案格式，导致会做题却丢分。

---

**验证结果**

已确认的事实：

- `train.csv` 共 `9500` 题
- 6 类题型分布均衡
- 没有重复 `prompt`
- `numeral` 题目标数字范围是 `1` 到 `100`
- `unit` 和 `gravity` 的答案基本都是两位小数
- `bit` 答案固定为 8 位二进制串
- `test.csv` 只有 3 条，更像格式样例，不是正式评测集

---

**推荐起手顺序**

1. 先把 6 类题拆开做验证集，避免随机切分。  
2. 第一批只合成 `gravity / unit / numeral`。  
3. 第二批补 `bit`，前提是加入“题目是否唯一可解”的检查。  
4. `text / equation` 放后面，只保留完全可验证的版本。  
5. 每批新增数据都做小规模对比，没稳定提升就删。

如果要继续，最有价值的下一步是：  
**直接把这 6 类题写成一份可执行的数据生成蓝图，包含每类的生成规则、验收标准、使用顺序。**

> TOOL

tool_use wait_agent
```json
{
  "targets": [
    "019d4e42-933d-7b30-9056-80ac3b8fbe2a",
    "019d4e42-9364-7910-9e0d-05df8a7ef87a"
  ],
  "timeout_ms": 30000
}
```

> TOOL

tool_use wait_agent
```json
{
  "targets": [
    "019d4e42-933d-7b30-9056-80ac3b8fbe2a",
    "019d4e42-9364-7910-9e0d-05df8a7ef87a"
  ],
  "timeout_ms": 60000
}
```

> TOOL

tool_use wait_agent
```json
{
  "targets": [
    "019d4e42-933d-7b30-9056-80ac3b8fbe2a"
  ],
  "timeout_ms": 30000
}
```
