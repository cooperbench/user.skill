> DEVELOPER

Research how EAGLE-3 (the speculative decoding paper by the EAGLE team) selects which layers to use as auxiliary hidden states ("aux layers"). 

Context: EAGLE-3 uses hidden states from multiple intermediate layers of the target model as input to the draft model. The draft model concatenates these hidden states and projects them via an fc layer. The question is: how does the EAGLE-3 paper recommend choosing WHICH layers to use?

Search for:
1. The EAGLE-3 paper (likely on arxiv, by authors associated with EAGLE/EAGLE-2 speculative decoding, possibly from Peking University or related groups)
2. Specifically look for their methodology on selecting auxiliary layers - do they use linear probes? Mutual information? Some other criterion?
3. How many aux layers do they recommend? Is there a scaling relationship?
4. Any ablation studies on layer selection

Also check EAGLE-2 if EAGLE-3 doesn't have this detail - the aux layer concept may have been introduced earlier.

Report findings concisely - the key method and any specific recommendations.

> AGENT

I'll research the EAGLE-3 paper and its methodology for selecting auxiliary layers.

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "query": "EAGLE-3 speculative decoding auxiliary layers selection paper arxiv",
  "search_depth": "advanced",
  "max_results": 10
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: [PDF] arXiv:2503.01840v3 [cs.CL] 23 Apr 2025
URL: https://arxiv.org/pdf/2503.01840
Content: 6 Conclusion In this paper, we introduce EAGLE-3. Building upon EAGLE, EAGLE-3 incorporates two key im-provements. First, it removes the feature prediction constraint, instead directly predicting draft tokens through a Training-time test. Second, it replaces the use of the target model’s top-layer features with a fusion of the target model’s lower, middle, and upper-layer features to obtain richer informa-tion. With these improvements, EAGLE-3 contin-ues to benefit from the augmentation of training data, achieving a maximum speedup of 6.5x.
Acknowledgement We woud like to thank James Liu, Ke Bao, Yineng Zhang, Lianmin Zheng, Ying Sheng, and many oth-ers in the SGLang team for merging and evaluating EAGLE-3 in the SGLang environment. [...] To summarize, this paper introduces EAGLE-3, an enhanced version of EAGLE that achieves a significant speedup. EAGLE-3 is parallelized and fully compatible with the drafting tree tech-nique from EAGLE-2 (Li et al., 2024b). Our key contributions include: • A novel training-time test architecture for the draft model: We remove the feature pre-diction constraint and directly predict tokens while simulating multi-step generation during training. This direct token prediction provides complete flexibility in the draft model’s input. [...] MT-bench GSM8K Method Speedup τ Speedup τ EAGLE-2 3.16x 4.05 3.39x 4.24 + remove fea con 3.82x 5.37 3.77x 5.22 + fused features (ours) 4.40x 6.13 4.48x 6.23 4.3 EAGLE-3 in SGLang Speculative sampling algorithms like EAGLE-3 reduce memory accesses and lower latency dur-ing memory-bound decoding by leveraging redun-dant computational power. As batch sizes increase, this redundancy decreases, reducing the effective-ness of speculative sampling. Efficiency improve-ments are more challenging in highly optimized production-grade frameworks. The performance of EAGLE-3 for large batches on a single H100 GPU and LLaMA-Instruct 3.1 8B in the SGLang v0.4.4 environment (Zheng et al., 2024) was evaluated by the SGLang team, shown in Table 3. This part of the experiment did not use the tree structure,

Title: 1 Introduction
URL: https://arxiv.org/html/2601.11580v1
Content: For EAGLE/EAGLE3, PdraftP\_{\text{draft}} refers to the parameters used in speculative decoding. For the EAGLE models we used, PdraftP\_{\text{draft}} refers to the parameter size of the autoregressive head, which includes one decoding layer and one fully connected (FC) layer. They share the same embedding layer and language modeling (LM) head with the target model. For the EAGLE3 models we used, PdraftP\_{\text{draft}} refers to the parameter size of the entire EAGLE3 model. It includes one decoding layer, the multi-layer feature fusion FC layer, a final normalization layer and its own LM head. In addition, the model checkpoints include two 1-dimensional token-id remapping tables (t2d and d2t) that translate between the target model’s vocabulary and the draft LM head’s vocabulary; they [...] Speculative decoding (SD) has become a popular technique to accelerate Large Language Model (LLM) inference, yet its real-world effectiveness remains unclear as prior evaluations rely on research prototypes and unrealistically small batch sizes. We present, to our knowledge, the first systematic study of SD on a production-grade and widely deployed inference engine (vLLM), covering multiple SD variants (nn-gram, EAGLE/EAGLE-3, Draft-Model, Multi-Token Prediction) across diverse workloads, model scales, and batch sizes. We analyze key factors governing SD performance, and [...] |  |  |  |  |  |
 ---  --- 
| Dataset | Method | Mean | Median | Std |
| InstructCoder | nn-gram | 7.27 | 6.57 | 4.19 |
| InstructCoder | EAGLE | 4.24 | 4.21 | 1.07 |
| InstructCoder | EAGLE-3 | 4.18 | 4.06 | 0.99 |
| CNN/DailyMail | EAGLE-3 | 3.08 | 2.97 | 0.61 |
| CNN/DailyMail | EAGLE | 2.32 | 2.31 | 0.21 |
| CNN/DailyMail | nn-gram | 2.33 | 1.96 | 1.08 |
| ShareGPT | EAGLE-3 | 3.06 | 2.92 | 0.87 |
| ShareGPT | EAGLE | 2.82 | 2.68 | 0.80 |
| ShareGPT | nn-gram | 2.02 | 1.37 | 1.87 |
| GSM8K | EAGLE-3 | 3.02 | 2.92 | 0.47 |
| GSM8K | EAGLE | 2.56 | 2.51 | 0.25 |
| GSM8K | nn-gram | 1.41 | 1.28 | 0.45 |
| GPQA\_Main | nn-gram | 4.20 | 3.73 | 2.24 |
| GPQA\_Main | EAGLE-3 | 2.78 | 2.49 | 0.87 |
| AIME22-24 | nn-gram | 3.53 | 2.96 | 2.29 |
| AIME22-24 | EAGLE-3 | 2.62 | 2.50 | 0.54 |

Title: 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎: A Flexible and Efficient Open-Source Training ...
URL: https://arxiv.org/html/2603.18567v1
Content: Owing to its strong empirical performance, EAGLE-3 has become the de facto industrial standard for speculative decoding and is supported by

Title: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
URL: https://arxiv.org/html/2503.01840v1
Content: Speculative sampling algorithms like EAGLE-3 reduce memory accesses and lower latency during memory-bound decoding by leveraging redundant computational power. As batch sizes increase, this redundancy decreases, reducing the effectiveness of speculative sampling. We conducted a study on the impact of EAGLE-3 on throughput for large batch sizes based on vLLM, a widely used production-grade framework, and the results are shown in Table 3. EAGLE shows the maximum throughput improvement at a batch size of 24, while EAGLE-3 shows this at 56. This part of the experiment did not use the tree structure, and the maximum chain length was set to 2. The framework used is also different from the other sections of this paper and from the typical settings in the speculative sampling domain, so [...] The sequential nature of modern LLMs makes them expensive and slow, and speculative sampling has proven to be an effective solution to this problem. Methods like EAGLE perform autoregression at the feature level, reusing top-layer features from the target model to achieve better results than vanilla speculative sampling. A growing trend in the LLM community is scaling up training data to improve model intelligence without increasing inference costs. However, we observe that scaling up data provides limited improvements for EAGLE. We identify that this limitation arises from EAGLE’s feature prediction constraints. In this paper, we introduce EAGLE-3, which abandons feature prediction in favor of direct token prediction and replaces reliance on top-layer features with multi-layer feature [...] Appendix A.1 of Leviathan et al. (2023) proves that speculative sampling is consistent with the distribution of vanilla autoregressive decoding.

Title: [2401.15077] EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty
URL: https://arxiv.org/abs/2401.15077
Content: Cornell University
arxiv logo

Help | Advanced Search

arXiv logo
Cornell University Logo

## quick links

# Computer Science > Machine Learning

# Title:EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

|  |  |
 --- |
| Subjects: | Machine Learning (cs.LG); Computation and Language (cs.CL) |
| Cite as: | arXiv:2401.15077 [cs.LG] |
|  | (or  arXiv:2401.15077v3 [cs.LG] for this version) |
|  |  Focus to learn more  arXiv-issued DOI via DataCite |

## Submission history

## Access Paper:

### References & Citations

## BibTeX formatted citation

### Bookmark

BibSonomy logo
Reddit logo

# Bibliographic and Citation Tools

# Code, Data and Media Associated with this Article

# Demos

# Recommenders and Search Tools [...] # Demos

# Recommenders and Search Tools

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

arXiv Operational Status

Title: [2602.13836] Speculative Decoding with a Speculative Vocabulary
URL: https://arxiv.org/abs/2602.13836
Content: Cornell University
arxiv logo

Help | Advanced Search

arXiv logo
Cornell University Logo

## quick links

# Computer Science > Computation and Language

# Title:Speculative Decoding with a Speculative Vocabulary

|  |  |
 --- |
| Comments: | Under review |
| Subjects: | Computation and Language (cs.CL) |
| Cite as: | arXiv:2602.13836 [cs.CL] |
|  | (or  arXiv:2602.13836v1 [cs.CL] for this version) |
|  |  Focus to learn more  arXiv-issued DOI via DataCite |

## Submission history

## Access Paper:

### Current browse context:

### References & Citations

## BibTeX formatted citation

### Bookmark

BibSonomy
Reddit

# Bibliographic and Citation Tools

# Code, Data and Media Associated with this Article

# Demos

# Recommenders and Search Tools [...] # Demos

# Recommenders and Search Tools

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

arXiv Operational Status

Title: [2503.01840] EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
URL: https://arxiv.org/abs/2503.01840
Content: Cornell University
arxiv logo

Help | Advanced Search

arXiv logo
Cornell University Logo

## quick links

# Computer Science > Computation and Language

# Title:EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

|  |  |
 --- |
| Subjects: | Computation and Language (cs.CL) |
| Cite as: | arXiv:2503.01840 [cs.CL] |
|  | (or  arXiv:2503.01840v3 [cs.CL] for this version) |
|  |  Focus to learn more  arXiv-issued DOI via DataCite |

## Submission history

## Access Paper:

### References & Citations

## BibTeX formatted citation

### Bookmark

BibSonomy logo
Reddit logo

# Bibliographic and Citation Tools

# Code, Data and Media Associated with this Article

# Demos

# Recommenders and Search Tools [...] # Demos

# Recommenders and Search Tools

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

arXiv Operational Status

Title: ■("") Speculative Decoding via Hybrid Drafting and Rollback-Aware Branch Parallelism
URL: https://arxiv.org/html/2506.01979v1
Content: where we extract K𝐾Kitalic\_K hidden states ht−1subscriptℎ𝑡1{h}\_{t-1}italic\_h start\_POSTSUBSCRIPT italic\_t - 1 end\_POSTSUBSCRIPT from the target model’s last K𝐾Kitalic\_K layers and concatenate them with the new token embedding etsubscript𝑒𝑡e\_{t}italic\_e start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT to (ft−1,𝐞t)subscript𝑓𝑡1subscript𝐞𝑡({f}\_{t-1},\mathbf{e}\_{t})( italic\_f start\_POSTSUBSCRIPT italic\_t - 1 end\_POSTSUBSCRIPT , bold\_e start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT ). To capture richer context than single-layer approaches li2024eagle ; zhang2024adaeagle , our method uses multiple layers for better length prediction. The output stsubscript𝑠𝑡s\_{t}italic\_s start\_POSTSUBSCRIPT italic\_t end\_POSTSUBSCRIPT initiates a new hybrid drafting strategy [...] Speculative Decoding While SD has demonstrated significant acceleration and lossless generalization, increasing the acceptance rate of draft tokens by the target model remains a critical challenge. Existing approaches rely on draft model training-based cai2024medusa ; li2024eagle ; du2024glide  and training-free methods fu2024break ; chen2023accelerating ; zhao2024ouroboros ; liu2024parallel  to align the draft and target models. For instance, Medusa introduces auxiliary decoding heads to the target model cai2024medusa , while Eagle li2024eagle  and Glide du2024glide  reuse target model information to enhance token prediction accuracy. SpecInfer uses tree-based attention to efficiently verify multiple draft candidates in order to improve acceptance rates chen2023accelerating . On the [...] Speculative Decoding Speculative decoding accelerates autoregressive generation through parallel token verification. The draft model Mqsubscript𝑀𝑞\mathit{M}\_{q}italic\_M start\_POSTSUBSCRIPT italic\_q end\_POSTSUBSCRIPT proposes γ𝛾\gammaitalic\_γ candidate tokens 𝐗~1:γsubscript~𝐗:1𝛾\tilde{\mathbf{X}}\_{1:\gamma}over~ start\_ARG bold\_X end\_ARG start\_POSTSUBSCRIPT 1 : italic\_γ end\_POSTSUBSCRIPT with probabilities {q⁢(xi|𝐗1:i−1)}i=1γsuperscriptsubscript𝑞conditionalsubscript𝑥𝑖subscript𝐗:1𝑖1𝑖1𝛾\{q(x\_{i}|\mathbf{X}\_{1:i-1})\}\_{i=1}^{\gamma}{ italic\_q ( italic\_x start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT | bold\_X start\_POSTSUBSCRIPT 1 : italic\_i - 1 end\_POSTSUBSCRIPT ) } start\_POSTSUBSCRIPT italic\_i = 1 end\_POSTSUBSCRIPT start\_POSTSUPERSCRIPT italic\_γ

Title: How top AI labs optimize for fast inference with speculative decoding | Eyal Ben Barouch posted on the topic | LinkedIn
URL: https://www.linkedin.com/posts/eyal-ben-barouch-007-1a2b3c4d5_want-to-know-how-the-top-ai-labs-optimize-activity-7379484544653045761-_ouQ
Content: is the idea behind speculative decoding, a fast draft model predicts several tokens ahead, and a larger, target model verifies which token prefix it agrees with and discards the rest. In standard autoregressive generation, each token requires a full forward pass, making inference slow and expensive. Speculative decoding reduces this cost by letting the large model validate multiple tokens at once, leveraging GPU parallelism. One of the best current approaches for SD is EAGLE, which improves speculative decoding by predicting in the feature space rather than token space and pruning low-probability paths (EAGLE-1, EAGLE-2). The latest version, EAGLE-3, takes a different direction with direct token prediction and multi-layer feature fusion, achieving up to 5× faster inference while [...] 61   10 Comments

Like   Comment

Eyal Ben Barouch 

Head of Data & AI @ Tavily

 1mo 

 Report this comment

 - EAGLE and EAGLE-2: Lossless Inference Acceleration for LLMs - Hongyang Zhang  - Faster Inference of LLMs Seminar   - Official EAGLE github  - LLM-Inference-Bench: Inference Benchmarking of Large Language Models on AI Accelerators

Reply  3 Reactions   4 Reactions

Ron Beiden 

Data Scientist @ HP | M.Sc Data Science Student @ BGU

 1mo 

 Report this comment

Very interesting! Thanks for sharing 😁

Like Reply  1 Reaction   2 Reactions

Shai Nisan, Ph.D. 

Head of AI @ Copyleaks | NLP Expert

 1mo 

 Report this comment

Speculative decoding is great indeed. For most tasks it is the optimal combination of speed and accuracy

Like Reply  1 Reaction   2 Reactions

Tamir Katz [...] brackets differently in the (𝘢+𝘣)+𝘤 ≠ 𝘢+(𝘣+𝘤) example. 𝐓𝐡𝐞 𝐩𝐫𝐨𝐩𝐨𝐬𝐞𝐝 𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧? The solution proposed by Thinking Machines is to change the infrastructure to ensure that each batch that is loaded into the AI is consistently shaped. They call this batch-invariant kernels— meaning rewriting the core GPU operations from scratch so that calculations produce identical results regardless of how many users are being processed together. Unfortunately for us users, we can’t do much about it. Need to wait for e.g OpenAI, Anthropic, etc. to adopt these changes. Link to the paper in the comments. 👇

Title: Cross-Attention Speculative Decoding
URL: https://arxiv.org/html/2505.24544v3
Content: We present Budget EAGLE (Beagle), the first, to our knowledge, cross-attention-based Transformer decoder SD model that achieves performance on
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "query": "EAGLE-3 speculative decoding hidden states intermediate layers draft model 2024 2025",
  "search_depth": "advanced",
  "max_results": 10
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: Speculative Decoding in Practice: How EAGLE3 Makes LLMs Faster Without Changing Their Outputs
URL: https://huggingface.co/blog/lujangusface/tw-eagle3-gpu
Content: EAGLE3 (NeurIPS 2025) made a more fundamental change: tri-layer feature fusion. Instead of conditioning on only the final hidden state, EAGLE3 fuses representations from three points in the target model simultaneously:

   Early layers — encode syntax, morphology, and local token context
   Middle layers — encode semantic relationships and broader discourse structure
   Late layers — encode the output probability distribution directly [...] ##  conditions the draft head on the target's final hidden state — the output of the last transformer block before the language modeling head. Because the draft sees what the target was processing at its output layer, it can make predictions closely aligned with the target's distribution. EAGLE1 achieved 2.7–3.5× latency speedup on LLaMA-2-Chat 70B.

EAGLE2 (EMNLP 2024) added dynamic draft trees: instead of proposing a linear sequence of $k$k tokens, the draft explores branching token paths and retains only the most confident branches. The target verifies the entire tree in a single pass, improving acceptance rates further. [...] ```python
import requests

response = requests.post(
    "
    json={
        "model": "default",
        "messages": [{"role": "user", "content": "Explain speculative decoding in 3 sentences."}],
        "max_tokens": 256,
    }
)
print(response.json()["choices"]["message"]["content"])
```

  

## : github.com/tails-mpt/sglang
   SpecForge fork (GPU draft head training): github.com/tails-mpt/SpecForge
   SpecJAX (TPU draft head training): github.com/tails-mpt/SpecJAX
   EAGLE3 paper: arXiv:2503.01840
   Original speculative decoding: Leviathan et al., ICML 2023

  

## },
  year={2025}
}
```

## Models mentioned in this article 2

Title: From research to production: Accelerate OSS LLM with EAGLE-3 on Vertex - LMSYS Blog | LMSYS Org
URL: https://lmsys.org/blog/2025-12-01-eagle3-vertex/
Content: This is where EAGLE-3 (Extrapolative Attention Guided LEarning) comes in. EAGLE-3 is a more advanced approach. Instead of a whole separate model, it attaches an extremely lightweight 'draft head'—just 2-5% of the target model's size—directly to its internal layers. This head operates at both feature and token level, ingesting features from the target model's hidden states to extrapolate and predict a tree of future tokens.

The result? All the benefits of speculative decoding while eliminat[ing] the overhead of training and running a second model. [...] LMSYS

Contents

# From research to production: Accelerate OSS LLM with EAGLE-3 on Vertex

TL;DR: Speculative decoding boosts LLM inference, but traditional methods require a separate, inefficient draft model. Vertex AI utilizes EAGLE-3, adding a small draft head (2-5% of the target model) to internal layers, simplifying training and achieving ~2x-3x decoding speedup. This post outlines our pipeline for data cleaning, embeddings, training, and serving EAGLE-3 with SGLang on Vertex AI at scale.

Title: [PDF] arXiv:2503.01840v3 [cs.CL] 23 Apr 2025
URL: https://arxiv.org/pdf/2503.01840
Content: EAGLE leverages the top-layer features of the tar-get model as additional information and performs autoregression at the feature level, simplifying the drafting process. EAGLE performs autoregression at the feature level and then uses the LM head of the target model to obtain the draft token. Due to the sampling results at the token layer being hidden, feature-level autoregression introduces un-certainty. EAGLE addresses this issue by feeding the token sequence from the previous time step, i.e., the sampling results, into the draft model. Unlike the chain-like drafts of Vanilla speculative sam-pling, EAGLE generates multiple draft tokens at the same position, resulting in a tree-like draft. In the verification stage, EAGLE uses tree attention to parallelize the verification of the draft [...] draft model operates independently of the target model. Unlike the vanilla speculative sampling, EAGLE (Li et al., 2024c) reuses the top-layer fea-tures of the target model (the features before the LM head). It trains the draft model to autoregres-sively predict the next feature and then uses the target model’s LM head to obtain the draft token.
By leveraging the rich information from the target model, EAGLE achieves significantly better accel-eration compared to vanilla speculative sampling.
Subsequent methods such as HASS (Zhang et al., 2024) and Falcon (Gao et al., 2024) also adopt the approach of predicting the next feature using the current feature sequence. [...] EAGLE and speculative sampling methods such as Medusa (Cai et al., 2024) reuse the top-layer fea-tures of the target model, specifically the features immediately before the LM head. For an LM head with a full-rank weight matrix, the top-layer fea-tures corresponding to the logits of the next token are unique, ensuring that the information contained in these features aligns directly with the logits of the next token. However, predicting the next-next token based solely on top-layer features—which are inherently limited to the next token—poses a significant challenge. Fortunately, the training-time test technique described above enables the use of features from intermediate layers instead of relying solely on the top layer, as the feature prediction loss lfea has been removed during

Title: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
URL: https://arxiv.org/html/2503.01840v1
Content: Speculative sampling uses the target model for verification to ensure lossless acceleration. Early speculative decoding methods Stern et al. (2018); Sun et al. (2021) accelerated generation in greedy settings, while Leviathan et al. (2023); Chen et al. (2023) introduced speculative sampling to extend the draft verification framework to non-greedy generation. Many subsequent works have improved upon speculative sampling. EAGLE Li et al. (2024c), EAGLE-2 Li et al. (2024b), Medusa Cai et al. (2024), and Hydra Ankner et al. (2024) reused the features of the target model. HASS Zhang et al. (2024) simulates a multi-step draft process during training to mitigate the issues of training-inference inconsistency and error accumulation in EAGLE. [...] Speculative sampling methods can reduce LLM latency by partially parallelizing the generation process. These methods rapidly generate draft tokens and then verify them in parallel. This allows multiple tokens to be produced in a single forward pass, significantly reducing inference latency. In vanilla speculative sampling, the draft model is a separate, smaller LLM, typically a lower-parameter version from the same series as the target model. This draft model operates independently of the target model. Unlike the vanilla speculative sampling, EAGLE Li et al. (2024c) reuses the top-layer features of the target model (the features before the LM head). It trains the draft model to autoregressively predict the next feature and then uses the target model’s LM head to obtain the draft token. By [...] Unlike the chain-like drafts of Vanilla speculative sampling, EAGLE generates multiple draft tokens at the same position, resulting in a tree-like draft. In the verification stage, EAGLE uses tree attention to parallelize the verification of the draft tree. Interestingly, EAGLE inspired the multi-token prediction technique used in the pre-training of DeepSeek-v3 Liu et al. (2024a), which in turn inspired new architectural designs in EAGLE-3.

Title: EAGLE-3 Speculative Decoding: 2-6x Faster LLM Inference Guide | E2E Networks
URL: https://www.e2enetworks.com/blog/Accelerating_LLM_Inference_with_EAGLE
Content: Load tokenized conversations from the dataset cache
 Generate target model features: Query the SGLang server to get hidden states from multiple layers (low, middle, high) of the target model for the current batch
 Fuse multi-layer features: Concatenate features from the three layers and compress them through a learned projection layer
 Draft head forward pass with training-time test:
  + Native prediction (step 0): Use target model features to predict the next token
  + Simulated prediction (steps 1-6): Feed the draft head's own predictions back as input to simulate multi-step generation during inference
  + Generate predictions for all positions up to `--ttt-length` (default 7 steps ahead) [...] Offline training: You pre-generate all target model hidden states and save them to disk. Training reads from these saved states instead of querying a server. This is faster but requires significantly more disk space (potentially several terabytes for large datasets).

EAGLE-3 Online vs Offline Training Pipeline Training pipeline comparison: Online mode (top) runs the target model as an SGLang server that processes training data in real-time, extracts multi-layer features, and feeds them to the draft model for training. Offline mode (bottom) pre-computes all hidden states during an SGLang phase and stores them to disk, then loads these cached features during the SpecForge training phase, eliminating the need for a live target model server. (Source: LMSYS SpecForge Blog) [...] json

`{ "model_type": "llama", "hidden_size": 4096, "num_hidden_layers": 1, "num_attention_heads": 32, "num_key_value_heads": 8, "intermediate_size": 14336, "hidden_act": "silu", "vocab_size": 128256, "draft_vocab_size": 32000 }`

Important fields:

 `num_hidden_layers: 1`: The draft head is just one transformer decoder layer
 `hidden_size: 4096`: Must match the target model's hidden dimension
 `vocab_size: 128256`: Target model's full vocabulary size
 `draft_vocab_size: 32000`: Reduced vocabulary for the draft model (top-k most frequent tokens)

The draft head uses a reduced vocabulary to save memory and computation. During training, SpecForge builds a mapping from the target model's 128K vocabulary to the draft model's 32K vocabulary, keeping only the most frequently used tokens.

Title: 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎: A Flexible and Efficient Open-Source Training Framework for Speculative Decoding
URL: https://arxiv.org/html/2603.18567v1
Content: Sub-optimal Prefill Performance.
The training process of EAGLE3 can be naturally decomposed into two stages. In the first stage, the target model is executed over the entire input sequence to generate the corresponding hidden states. This is equivalent to the prefill phase in standard LLM inference, where the model processes the tokens in a fully autoregressive manner in parallel before decoding begins. [...] Stage 3: Feature-Level Extrapolation. Although Medusa eliminates the overhead of maintaining an independent draft model, its non-autoregressive MLP heads struggle to capture long-range dependencies. Li et al. (2024b) address this limitation with EAGLE, which shifts autoregression from token space to feature space under the feature-uncertainty hypothesis: hidden-state trajectories in high-dimensional feature space are smoother and more predictable than the discrete jumps between tokens (Li et al., 2024b; Du et al., 2024). EAGLE replaces the standalone draft model with a lightweight single-layer Transformer that autoregressively predicts future feature representations, which are then projected through a linear layer to obtain the token logits. This fully autoregressive yet efficient design [...] Early demonstrations of speculative decoding (Leviathan et al., 2022) showed speedups of up to 3.4× on large Transformer models such as T5-XXL (Raffel et al., 2020), while provably preserving output fidelity. Subsequent advances have further improved its efficiency and practicality. Notably, the EAGLE-3 algorithm (Li et al., 2025) introduces a draft model that operates at a hybrid feature level, substantially increasing token acceptance rates and achieving up to 4.79× speedup on LLaMA-3.3-70B without quality degradation. EAGLE-3 further incorporates dynamic tree-based generation and a Training-Time Test (TTT) procedure that better simulates multi-step decoding during draft training. Owing to its strong empirical performance, EAGLE-3 has become the de facto industrial standard for

Title: [PDF] EAGLE-3: Scaling up Inference Acceleration of Large Language ...
URL: https://openreview.net/pdf?id=4exx1hUffq
Content: 2.2 EAGLE and EAGLE-2 The draft model with limited capacity struggles to precisely approximate the large-scale target model. EAGLE leverages the top-layer features of the target model as additional information and performs autoregression at the feature level, simplifying the drafting process. EAGLE performs autoregression at the feature level and then uses the LM head of the target model to obtain the draft token. Due to the sampling results at the token layer being hidden, feature-level autoregression introduces uncertainty. EAGLE addresses this issue by feeding the token sequence from the previous time step, i.e., the sampling results, into the draft model. Unlike the chain-like drafts of Vanilla speculative sampling, EAGLE generates multiple draft tokens at the same position, resulting [...] Speculative sampling uses the target model for verification to ensure lossless acceleration. Early speculative decoding methods [36, 37] accelerated generation in greedy settings, while [10, 11] introduced speculative sampling to extend the draft verification framework to non-greedy generation. [...] EAGLE and speculative sampling methods such as Medusa  reuse the top-layer features of the target model, specifically the features immediately before the LM head. For an LM head with a full-rank weight matrix, the top-layer features corresponding to the logits of the next token are unique, ensuring that the information contained in these features aligns directly with the logits of the next token. However, predicting the next-next token based solely on top-layer features—which are inherently limited to the next token—poses a significant challenge. Fortunately, the training-time test technique described above enables the use of features from intermediate layers instead of relying solely on the top layer, as the feature prediction loss lfea has been removed during training.

Title: Faster LLM inference with Parallel Speculative Decoding in vLLM
URL: https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm/
Content: Step 1: Prefilling. The target model processes the prompt and generates a new token, as it would during normal inference. Along the way, P-EAGLE captures the model’s internal hidden states: `h_prompt` for each prompt position, and `h_context` for the newly generated token. These hidden states encode what the target model “knows” at each position and will guide the drafter’s predictions. This step is identical to autoregressive EAGLE.

Step 2: P-EAGLE Drafter. The drafter constructs inputs for each position in parallel. Each input consists of a token embedding concatenated with a hidden state. [...] Code

# Conclusion

P-EAGLE removes the sequential bottleneck from speculative decoding, delivering up to 1.69× speedup over vanilla EAGLE-3 on real workloads. By decoupling draft count from forward pass count, we can now explore larger drafting architectures, which can even enable increased acceptance rates compared to single-layer baselines. This implementation carefully handles the complexities of input preparation, attention metadata management, and KV cache slot mapping through hand-written fused kernels. While it requires specially trained models, the performance benefits make it a valuable addition to vLLM’s speculative decoding capabilities. [...] This logic would otherwise be many GPU ops (copy/scatter + insert + fill + mask + remap). Fusing it into one kernel reduces launch overhead and extra memory traffic, keeping the drafting setup cheap.

## Hidden State Management

For EAGLE-based methods that pass hidden states to the draft model, parallel drafting handles populating these fields separately. Since hidden states are significantly larger than the rest of the input batch, we split the work: the Triton kernel outputs a mapping, and a dedicated copy kernel broadcasts the learned hidden state placeholder into the mask token slots.

Title: Train with Eagle3 Speculative Decoding — NeMo-RL
URL: https://docs.nvidia.com/nemo/rl/nightly/guides/eagle3-speculative-decoding.html
Content: In words:

use the hidden state at position `t`

`t`

use the embedding of the token at position `t+1`

`t+1`

predict the teacher distribution for position `t+1`

`t+1`

After this alignment, the draft loss is:

Here `z_{policy,t}` and `z_{draft,t}` refer to the aligned tensors after rolling, truncation, and masking, not the raw unshifted outputs of the forward pass.

`z_{policy,t}`
`z_{draft,t}`

This has the same student gradient as forward KL from the policy distribution to the draft distribution, up to the teacher entropy constant. The total training objective is:

where `lambda` is `policy.draft.loss_weight`.

`lambda`
`policy.draft.loss_weight`

## Important Knobs#

`policy.draft.enabled`: attach and train the Eagle draft model

`policy.draft.enabled` [...] the `draft.` weights into the vLLM drafter

`draft.`

That keeps the rollout drafter aligned with the latest RL-updated policy instead of a stale checkpoint.

### Training Path#

During the policy forward pass, NeMo RL captures:

token input embeddings

a small set of intermediate hidden states from auxiliary policy layers

Those captured activations are the Eagle inputs. NeMo RL captures an early/middle/late-style set of policy layers for Eagle3, then the draft model predicts logits with its own draft LM head. That LM head is loaded from the draft checkpoint when `lm_head.weight` is present and otherwise initialized from the current policy output layer.

`lm_head.weight`

### Draft Loss and Time-Step Alignment# [...] ## Draft Checkpoint#

For the best results, start from an Eagle checkpoint that was already pretrained as a draft model, then use NeMo RL’s online draft loss to keep it aligned with the policy during RL. For training or adapting an Eagle checkpoint, see the Model Optimizer speculative decoding example.

NeMo RL now keeps a trainer-owned draft LM head. If the draft checkpoint contains
`lm_head.weight`, NeMo RL loads it into the draft model. If that weight is absent,
NeMo RL initializes the draft LM head from the current policy output layer instead.

`lm_head.weight`

## Enablement#

### Generation Only#

This enables Eagle3 in vLLM, but the trainer does not own or update the draft model.

### Online Draft Training#

Note

Title: Speculative Decoding in vLLM: Complete Guide to Faster LLM ...
URL: https://jarvislabs.ai/blog/speculative-decoding-vllm-faster-llm-inference
Content: image Source : Generated by nano banana pro

To understand why EAGLE-3 is the current state-of-the-art for speculative decoding, we must look at how the technique evolved:

 EAGLE-1 (The Original): This version introduced the idea of a single-layer draft head reusing the Target Model's top-layer features (the features right before the final output).

  + Limitation: It suffered from "feature uncertainty." It was trained on perfect "ground truth" data but had to generate based on its own noisy predictions during inference. This caused acceptance rates to drop quickly as it predicted further ahead.
 EAGLE-2 (Dynamic Trees): This iteration improved the inference strategy. It introduced dynamic draft trees that contextually adjusted the shape of the speculation tree. [...] ## EAGLE Technique

The EAGLE (Extrapolation Algorithm for Greater Language-Model Efficiency) family represents a paradigm shift in speculative decoding. While Draft Models require a completely separate LLM (creating memory and tokenizer headaches) and MLP Speculators use simple projections, EAGLE takes a "best of both worlds" approach.

It trains a lightweight draft head (typically just 1-2 transformer layers) that plugs directly into your Target Model. This head reuses the Target Model's internal feature maps to predict tokens, adding minimal parameter overhead (under 5% for 70B models) while delivering massive speedups.

### The Evolution: EAGLE 1, 2, and 3

image Source : Generated by nano banana pro [...] + Improvement: It became smarter about how to guess (pruning low-confidence branches early), but it still relied on the same fundamental feature extraction as EAGLE-1, limiting its maximum accuracy.
 EAGLE-3 (The Breakthrough): This version fundamentally changes how the draft head learns and what it sees.

  + Key Innovation 1 (Multi-Layer Fusion): Instead of just looking at the top layer, EAGLE-3 extracts and fuses features from the Low, Middle, and High layers of the Target Model. This provides a much richer context for prediction.
  + Key Innovation 2 (Training-Time Test): It solves the "Distribution Mismatch" problem by simulating the noisy inference process during the training phase itself.

### Training Strategy: The "Training-Time Test" (TTT)
```

> AGENT

Now let me get the full paper content, specifically focusing on the layer selection methodology.

> TOOL

tool_use mcp__tavily__tavily_extract
```json
{
  "urls": [
    "https://arxiv.org/html/2503.01840v1"
  ],
  "query": "auxiliary layer selection multi-layer feature fusion which layers linear probe ablation"
}
```

> TOOL

tool_result mcp__tavily__tavily_extract
```
Detailed Results:

Title: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
URL: https://arxiv.org/html/2503.01840v1
Content: undefined
Raw Content: reliance on top-layer features with multi-layer feature fusion via a technique named training-time test. These improvements significantly enhance performance and enable the draft model to fully benefit from scaling up training data. Our experiments include both chat models and reasoning models, evaluated on five tasks. The results show that EAGLE-3 achieves a speedup ratio up to 6.5x, with about 1.4x improvement over EAGLE-2. The code is available at . [...] Refer to caption

### 4.2 Ablation Study

The improvements of EAGLE-3 mainly come from two aspects: first, the removal of the feature regression constraint, and second, the improvement from reusing only the top-layer features to reusing a mix of low, middle, and high-level features. We conducted an ablation study on MT-bench with LLaMA-Instruct 3.1 8B as the target model. The results, shown in Table 2, indicate that both improvements in EAGLE-3 significantly enhance the acceptance length and speedup ratio, demonstrating the rationality of the EAGLE-3 design. [...] subscript𝑔1subscript𝑔2⋯subscript𝑔𝑖subscript𝑎𝑖1⋯subscript𝑎𝑖𝑛g\_{1},g\_{2},\cdots,g\_{i},{a}\_{i+1},\cdots,{a}\_{i+n}italic\_g start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT , italic\_g start\_POSTSUBSCRIPT 2 end\_POSTSUBSCRIPT , ⋯ , italic\_g start\_POSTSUBSCRIPT italic\_i end\_POSTSUBSCRIPT , italic\_a start\_POSTSUBSCRIPT italic\_i + 1 end\_POSTSUBSCRIPT , ⋯ , italic\_a start\_POSTSUBSCRIPT italic\_i + italic\_n end\_POSTSUBSCRIPT, where g𝑔gitalic\_g is the fused feature from the target model.
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "EAGLE-3 arxiv 2503.01840 layer selection linear probe auxiliary hidden states which layers low middle high ablation",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: [PDF] arXiv:2503.01840v3 [cs.CL] 23 Apr 2025
URL: https://arxiv.org/pdf/2503.01840
Content: from reusing only the top-layer features to reusing a mix of low, middle, and high-level features. We conducted an ablation study on MT-bench with LLaMA-Instruct 3.1 8B as the target model. The results, shown in Table 2, indicate that both im-provements in EAGLE-3 significantly enhance the acceptance length and speedup ratio, demonstrat-ing the rationality of the EAGLE-3 design.
Table 2: Ablation study results with LLaMA-Instruct 3.1 8B as the target model. “Remove fea con” refers to the first improvement of EAGLE-3, which removes the feature prediction constraint. “Fused features” refers to the second improvement of EAGLE-3, where low, middle, and high-level feature fusion replaces the use of top-layer features. [...] 3.1 Inference Pipeline Consistent with other speculative sampling meth-ods, EAGLE-3 alternates between the drafting and verification stages. The difference between EAGLE-3 and EAGLE lies in the drafting stage, which we introduce with an example, as shown in Figure 5. Consider the prefix “How can”. Dur-ing the prefill phase or the previous verification stage, the target model performs a forward pass to generate the next token, “I”. We record the low, middle, and high-level feature sequences from the target model’s forward pass, denoted as l, m, and h, respectively. We concatenate the k-dimensional vectors l, m, and h to form a 3k-dimensional vector, then pass it through a fully connected (FC) layer to reduce it to k-dimensions, obtaining a feature g that integrates information from [...] 6 Conclusion In this paper, we introduce EAGLE-3. Building upon EAGLE, EAGLE-3 incorporates two key im-provements. First, it removes the feature prediction constraint, instead directly predicting draft tokens through a Training-time test. Second, it replaces the use of the target model’s top-layer features with a fusion of the target model’s lower, middle, and upper-layer features to obtain richer informa-tion. With these improvements, EAGLE-3 contin-ues to benefit from the augmentation of training data, achieving a maximum speedup of 6.5x.
Acknowledgement We woud like to thank James Liu, Ke Bao, Yineng Zhang, Lianmin Zheng, Ying Sheng, and many oth-ers in the SGLang team for merging and evaluating EAGLE-3 in the SGLang environment.

Title: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
URL: https://arxiv.org/html/2503.01840v1
Content: We record the low, middle, and high-level feature sequences from the target model’s forward pass, denoted as l𝑙litalic\_l, m𝑚mitalic\_m, and hℎhitalic\_h, respectively. We concatenate the k𝑘kitalic\_k-dimensional vectors l𝑙litalic\_l, m𝑚mitalic\_m, and hℎhitalic\_h to form a 3⁢k3𝑘3k3 italic\_k-dimensional vector, then pass it through a fully connected (FC) layer to reduce it to k𝑘kitalic\_k-dimensions, obtaining a feature g𝑔gitalic\_g that integrates information from different layers.
Here, k𝑘kitalic\_k refers to the hidden size of the target model. [...] Refer to caption

### 4.2 Ablation Study

The improvements of EAGLE-3 mainly come from two aspects: first, the removal of the feature regression constraint, and second, the improvement from reusing only the top-layer features to reusing a mix of low, middle, and high-level features. We conducted an ablation study on MT-bench with LLaMA-Instruct 3.1 8B as the target model. The results, shown in Table 2, indicate that both improvements in EAGLE-3 significantly enhance the acceptance length and speedup ratio, demonstrating the rationality of the EAGLE-3 design. [...] To summarize, this paper introduces EAGLE-3, an enhanced version of EAGLE that achieves a significant speedup. EAGLE-3 is parallelized and fully compatible with the drafting tree technique from EAGLE-2 Li et al. (2024b). Our key contributions include:

A novel training-time test architecture for the draft model: We remove the feature prediction constraint and directly predict tokens while simulating multi-step generation during training. This direct token prediction provides complete flexibility in the draft model’s input. Instead of reusing only the top-layer features, we integrate and leverage low-, mid-, and high-level features from the target model, capturing rich semantic information from different layers.

Title: Speculative Decoding in Practice: How EAGLE3 Makes LLMs Faster ...
URL: https://huggingface.co/blog/lujangusface/tw-eagle3-gpu
Content: EAGLE3 (NeurIPS 2025) made a more fundamental change: tri-layer feature fusion. Instead of conditioning on only the final hidden state, EAGLE3 fuses representations from three points in the target model simultaneously:

   Early layers — encode syntax, morphology, and local token context
   Middle layers — encode semantic relationships and broader discourse structure
   Late layers — encode the output probability distribution directly [...] By fusing all three, the draft head sees why the target would produce a particular token at every level of abstraction — not just the output distribution, but the full semantic reasoning context. EAGLE3 also switches from feature-level prediction to direct token prediction, removing a scaling ceiling that had limited EAGLE1 and EAGLE2 as training data increased.

Image 13: 04-eagle3-architecture

The EAGLE3 paper reports 4.1–6.5× speedup at temperature 0 on academic benchmarks (Vicuna 13B, Llama-3.1-8B, Llama-3.3-70B).

EAGLE3 requires training a custom draft head per target model. Off-the-shelf draft heads exist for a handful of mainstream models. For anything outside that set — especially models with MoE layers, custom attention variants, or quantized formats — you train from scratch. [...] ##  conditions the draft head on the target's final hidden state — the output of the last transformer block before the language modeling head. Because the draft sees what the target was processing at its output layer, it can make predictions closely aligned with the target's distribution. EAGLE1 achieved 2.7–3.5× latency speedup on LLaMA-2-Chat 70B.

EAGLE2 (EMNLP 2024) added dynamic draft trees: instead of proposing a linear sequence of $k$k tokens, the draft explores branching token paths and retains only the most confident branches. The target verifies the entire tree in a single pass, improving acceptance rates further.

Title: EAGLE-3: Accelerating LLM Inference
URL: https://www.emergentmind.com/topics/eagle-3
Content: Multi-layer feature fusion avoids the narrow top-layer constraints of prior EAGLE versions by collecting features from multiple transformer layers (e.g., low-, mid-, and high-level). These are fused via concatenation and a learned linear projection: gt​=Wfuse​[ft(1)​;…;ft(L)​]∈Rk The training-time test enables the draft model to simulate multi-step autoregressive generation during training, attending to its own previous predictions through custom causal masks. At each simulated position, the model restricts attention to the correct causal prefix, thereby learning to handle its own outputs as inputs—a crucial requirement for robust drafting at inference.

## 3. Draft Model Architecture and Pipeline Design [...] 1. The target model p pre-fills the prefix T1:t​, exposing low-, mid-, and high-level features (lt​,mt​,ht​).
2. These features are fused into gt​=Wfuse​[lt​;mt​;ht​].
3. The draft model receives as input the tuple {g1:t​,at+1:t+j−1​} and processes it with a single-layer Transformer decoder (consisting of self-attention and feed-forward modules).
4. The output vector at+j​ is projected by the target model’s LM head to yield the draft token distribution q(⋅). The draft token t^t+j​ is sampled from this distribution.
5. This draft/verify loop is repeated for up to k tokens, after which all are verified by the target LLM in parallel. [...] ## 3. Draft Model Architecture and Pipeline Design

EAGLE-3 integrates multi-layer feature fusion and direct token prediction within a streamlined draft model architecture. The inference pipeline operates as follows:

Title: EAGLE-3: Scaling up Inference Acceleration of Large ...
URL: https://arxiv.org/abs/2503.01840
Content: Cornell University
arxiv logo

Help | Advanced Search

arXiv logo
Cornell University Logo

## quick links

# Computer Science > Computation and Language

# Title:EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

|  |  |
 --- |
| Subjects: | Computation and Language (cs.CL) |
| Cite as: | arXiv:2503.01840 [cs.CL] |
|  | (or  arXiv:2503.01840v3 [cs.CL] for this version) |
|  |  Focus to learn more  arXiv-issued DOI via DataCite |

## Submission history

## Access Paper:

### References & Citations

## BibTeX formatted citation

### Bookmark

BibSonomy logo
Reddit logo

# Bibliographic and Citation Tools

# Code, Data and Media Associated with this Article

# Demos

# Recommenders and Search Tools [...] # Demos

# Recommenders and Search Tools

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

arXiv Operational Status

Title: Paper page - EAGLE-3: Scaling up Inference Acceleration of Large Language Models via
  Training-Time Test
URL: https://huggingface.co/papers/2503.01840
Content: ### Community

This paper introduces EAGLE-3, the latest version in the family of EAGLE with SOTA performance in speculative decoding.

This is an automated message from the Librarian Bot. I found the following papers similar to this paper.

The following papers were recommended by the Semantic Scholar API

Please give a thumbs up to this comment if you found it helpful!

If you want recommendations for any Paper on Hugging Face checkout this Space

You can directly ask Librarian Bot for paper recommendations by tagging it in a comment: `@librarian-bot  recommend`

`@librarian-bot  recommend`

· Sign up or log in to comment

Get this paper in your agent:

`hf papers read 2503.01840`
`curl -LsSf  | bash`

## Models citing this paper 65

#### RedHatAI/gemma-4-31B-it-speculator.eagle3 [...] top-layer features with multi-layer feature fusion via a technique named
training-time test. These improvements significantly enhance performance and
enable the draft model to fully benefit from scaling up training data. Our
experiments include both chat models and reasoning models, evaluated on five
tasks. The results show that EAGLE-3 achieves a speedup ratio up to 6.5x, with
about 1.4x improvement over EAGLE-2. The code is available at [...] Hugging Face's logo

# EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

## Abstract

EAGLE-3 improves speculative sampling in large language models by replacing feature prediction with direct token prediction and using multi-layer feature fusion, leading to better performance and greater benefit from increased training data.

Title: SafeAILab/EAGLE: Official Implementation of EAGLE-1 ... - GitHub
URL: https://github.com/SafeAILab/EAGLE
Content: , Tianle Cai, Hao Zhang, Ziteng Sun, and others.

## About

Official Implementation of EAGLE-1 (ICML'24), EAGLE-2 (EMNLP'24), and EAGLE-3 (NeurIPS'25).

arxiv.org/pdf/2503.01840

### Topics

large-language-modelsllm-inferencespeculative-decoding

### Resources

Readme

### License

View license

### Uh oh!

There was an error while loading. Please reload this page.

Activity

Custom properties

### Stars

2.3k stars

### Watchers

31 watching

### Forks

268 forks

Report repository

## Releases

No releases published

## Packages 0

### Uh oh!

There was an error while loading. Please reload this page.

### Uh oh!

There was an error while loading. Please reload this page.

## Contributors

    
    
    

### Uh oh!

There was an error while loading. Please reload this page. [...] EAGLE-2 is: 
       4x faster than vanilla decoding (13B).
       1.4x faster than EAGLE-1 (13B).

EAGLE-3 removes the feature prediction constraint in EAGLE and simulates this process during training using training-time testing. Considering that top-layer features are limited to next-token prediction, EAGLE-3 replaces them with a fusion of low-, mid-, and high-level semantic features. EAGLE-3 further improves generation speed while ensuring lossless performance.

   EAGLE-3 is: 
       5.6 faster than vanilla decoding (13B).
       1.8x faster than EAGLE-1 (13B).

Image 7: demogif

_Inference is conducted on 2x RTX 3090 GPUs at fp16 precision using the Vicuna 13B model._

## Support

. [...] # GitHub - SafeAILab/EAGLE: Official Implementation of EAGLE-1 (ICML'24), EAGLE-2 (EMNLP'24), and EAGLE-3 (NeurIPS'25). · GitHub

Skip to content
## Navigation Menu

Toggle navigation

 | Paper (EAGLE-2) | Paper (EAGLE-3) | Blog |

Image 2: VersionImage 3: LicenseImage 4: MaintenanceImage 5: Contributions welcome

Image 6: benchmark

EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency) is a new baseline for fast decoding of Large Language Models (LLMs) with provable performance maintenance. This approach involves extrapolating the second-top-layer contextual feature vectors of LLMs, enabling a significant boost in generation efficiency.

Title: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test | OpenReview
URL: https://openreview.net/forum?id=4exx1hUffq
Content: Supplementary Material:  zip

Primary Area: Deep learning (e.g., architectures, generative models, optimization for deep networks, foundation models, LLMs)

Submission Number: 13079

Loading

OpenReview is a long-term project to advance science through improved peer review with legal nonprofit status. We gratefully acknowledge the support of the OpenReview Sponsors. © 2026 OpenReview [...] Abstract: The sequential nature of modern LLMs makes them expensive and slow, and speculative sam- pling has proven to be an effective solution to this problem. Methods like EAGLE perform autoregression at the feature level, reusing top- layer features from the target model to achieve better results than vanilla speculative sampling. A growing trend in the LLM community is scaling up training data to improve model intelligence without increasing inference costs. However, we observe that scaling up data provides limited improvements for EAGLE. We identify that this limitation arises from EAGLE’s feature prediction constraints. In this paper, we introduce EAGLE-3, which abandons feature prediction in favor of direct token prediction and replaces reliance on top-layer features with [...] prediction and replaces reliance on top-layer features with multi-layer feature fusion via a technique named training-time test. These improvements significantly enhance performance and enable the draft model to fully benefit from scaling up training data. Our experiments include both chat models and reasoning models, evaluated on five tasks. The results show that EAGLE-3 achieves a speedup ratio up to 6.5x, with about 1.4x improvement over EAGLE-2. In the SGLang framework, EAGLE- 3 achieves a 1.38x throughput improvement at a batch size of 64.

Title: NeurIPS Poster EAGLE-3: Scaling up Inference Acceleration of ...
URL: https://neurips.cc/virtual/2025/poster/119930
Content: ### Video

Chat is not available.

Successful Page Load

| NeurIPS uses cookies for essential functions only. We do not sell your personal information. Our Privacy Policy » |  | [...] reliance on top-layer features with multi-layer feature fusion via a technique named training-time test. These improvements significantly enhance performance and enable the draft model to fully benefit from scaling up training data. Our experiments include both chat models and reasoning models, evaluated on five tasks. The results show that EAGLE-3 achieves a speedup ratio up to 6.5x, with about 1.4x improvement over EAGLE-2. In the SGLang framework, EAGLE- 3 achieves a 1.38x throughput improvement at a batch size of 64. [...] Skip to yearly menu bar

## Main Navigation

conference_logo

 NeurIPS 
  + Code of Ethics  

  + Code of Conduct  

  + Create Profile  

  + Journal To Conference Track  

  + Diversity & Inclusion  

  + Proceedings  

  + Future Meetings  

  + Press  

  + Exhibitor Information  

  + Contact NeurIPS  

  + Help/FAQ  

  + Privacy Policy  

  + Downloads
 My Stuff

 Login

Poster  Wed, Dec 3, 2025 • 11:00 AM – 2:00 PM PST

# EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

Yuhui Li · Fangyun Wei · Chao Zhang · Hongyang Zhang

Project Page    [Slides]     [Poster]     [OpenReview]

### Abstract

Title: From research to production: Accelerate OSS LLM with EAGLE-3 on ...
URL: https://lmsys.org/blog/2025-12-01-eagle3-vertex/
Content: This is where EAGLE-3 (Extrapolative Attention Guided LEarning) comes in. EAGLE-3 is a more advanced approach. Instead of a whole separate model, it attaches an extremely lightweight 'draft head'—just 2-5% of the target model's size—directly to its internal layers. This head operates at both feature and token level, ingesting features from the target model's hidden states to extrapolate and predict a tree of future tokens.

The result? All the benefits of speculative decoding while eliminat[ing] the overhead of training and running a second model. [...] ## Acknowledgements

We would like to express our sincere gratitude to the SGLang team—specifically Ying Sheng, Lianmin Zheng, Yineng Zhang, Xinyuan Tong, Liangsheng Yin as well as SGLang/SpecForge team —specifically Shenggui Li, Yikai Zhu—for their invaluable support throughout this project. Their generous assistance and deep technical insights were instrumental to the success of this project. [...] ## Challenge #1: Preparing the data

The EAGLE-3 head needs to be trained. The obvious first step is to grab a generic public available dataset. Most of these datasets present challenges, including:

Using this data as-is is not an option.

### Lesson 1: Build a Synthetic Data Generation Pipeline
```

> AGENT

Now let me look at the SpecForge training framework and the EAGLE-3 code to find the specific layer selection logic.

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "SpecForge EAGLE-3 training \"aux_hidden_state_layers\" layer index selection low middle high feature fusion configuration",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: EAGLE-3 Speculative Decoding: 2-6x Faster LLM Inference Guide
URL: https://www.e2enetworks.com/blog/Accelerating_LLM_Inference_with_EAGLE
Content: EAGLE-3's solution: Multi-layer fusion

The information needed to predict multiple steps ahead exists in the model, but it's distributed across different layers. EAGLE-3 extracts features from three levels: low, middle, and high. Each level of the model captures different aspects of the input, and combining them gives the draft head richer information for multi-step prediction.

EAGLE-3 Multi-Layer Feature Fusion Architecture Training architecture: The target model generates embeddings and hidden states at low, mid, and high layers. These features are concatenated and passed through an FC layer to produce fused hidden states, which feed into the draft model's decoder layer for plogp loss calculation. (Source: LMSYS SpecForge Blog) [...] Load tokenized conversations from the dataset cache
 Generate target model features: Query the SGLang server to get hidden states from multiple layers (low, middle, high) of the target model for the current batch
 Fuse multi-layer features: Concatenate features from the three layers and compress them through a learned projection layer
 Draft head forward pass with training-time test:
  + Native prediction (step 0): Use target model features to predict the next token
  + Simulated prediction (steps 1-6): Feed the draft head's own predictions back as input to simulate multi-step generation during inference
  + Generate predictions for all positions up to `--ttt-length` (default 7 steps ahead) [...] EAGLE-3 Inference Pipeline Complete inference workflow: The target model processes input tokens through multiple decoder layers. For each prompt position, features from low/mid/high layers are extracted, fused, and fed to the draft model's decoder. The draft model then generates a tree of candidate tokens (shown as nodes ①②③), which are verified by the target model's LM head in parallel. (Source: LMSYS SpecForge Blog)

When you generate text with the prompt "How can", the target model runs a forward pass and produces features at each layer. EAGLE-3 grabs features from all three levels, fuses them, and creates a unified representation that's useful for predicting not just "I" but also what comes after it.

## The Draft Head Architecture

Title: 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎: A Flexible and Efficient Open-Source Training Framework for Speculative Decoding
URL: https://arxiv.org/html/2603.18567v1
Content: 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎\mathtt{SpecForge} is our attempt to fill these gaps by advancing the practical development of speculative decoding in both research and industry. It is a unified, production-oriented framework for training draft models for speculative decoding, offering native support for advanced algorithms such as EAGLE-3, including the complex Training-Time Test (TTT) procedure with tree attention masks and recursive scheduling. With 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎\mathtt{SpecForge}, practitioners can easily train state-of-the-art draft models through simple configuration rather than custom engineering. [...] 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎\mathtt{SpecForge} further optimizes the Training-Time Test (TTT) procedure in EAGLE-3 by introducing memory- and compute-efficient attention implementations tailored to its autoregressive multi-step structure. It leverages the sparsity pattern in tree attention to reduce the computation time and memory peak, and optimizes the loss computation via customized in-place operations. Together, these optimizations significantly lower memory consumption and wall-clock time, enabling stable and scalable EAGLE-3 training at long context lengths. [...] training for Qwen3-235B-A22B. In addition, we release 𝚂𝚙𝚎𝚌𝙱𝚞𝚗𝚍𝚕𝚎\mathtt{SpecBundle}, a suite of production-grade EAGLE-3 draft models trained with 𝚂𝚙𝚎𝚌𝙵𝚘𝚛𝚐𝚎\mathtt{SpecForge} for mainstream open-source LLMs. Through

Title: Speculative Decoding in Practice: How EAGLE3 Makes LLMs Faster ...
URL: https://huggingface.co/blog/lujangusface/tw-eagle3-gpu
Content: EAGLE3 (NeurIPS 2025) made a more fundamental change: tri-layer feature fusion. Instead of conditioning on only the final hidden state, EAGLE3 fuses representations from three points in the target model simultaneously:

   Early layers — encode syntax, morphology, and local token context
   Middle layers — encode semantic relationships and broader discourse structure
   Late layers — encode the output probability distribution directly [...] By fusing all three, the draft head sees why the target would produce a particular token at every level of abstraction — not just the output distribution, but the full semantic reasoning context. EAGLE3 also switches from feature-level prediction to direct token prediction, removing a scaling ceiling that had limited EAGLE1 and EAGLE2 as training data increased.

Image 13: 04-eagle3-architecture

The EAGLE3 paper reports 4.1–6.5× speedup at temperature 0 on academic benchmarks (Vicuna 13B, Llama-3.1-8B, Llama-3.3-70B).

EAGLE3 requires training a custom draft head per target model. Off-the-shelf draft heads exist for a handful of mainstream models. For anything outside that set — especially models with MoE layers, custom attention variants, or quantized formats — you train from scratch. [...] ```python
import requests

response = requests.post(
    "
    json={
        "model": "default",
        "messages": [{"role": "user", "content": "Explain speculative decoding in 3 sentences."}],
        "max_tokens": 256,
    }
)
print(response.json()["choices"]["message"]["content"])
```

  

## : github.com/tails-mpt/sglang
   SpecForge fork (GPU draft head training): github.com/tails-mpt/SpecForge
   SpecJAX (TPU draft head training): github.com/tails-mpt/SpecJAX
   EAGLE3 paper: arXiv:2503.01840
   Original speculative decoding: Leviathan et al., ICML 2023

  

## },
  year={2025}
}
```

## Models mentioned in this article 2

Title: SpecForge: Accelerating Speculative Decoding Training for SGLang
URL: https://lmsys.org/blog/2025-07-25-spec-forge/
Content: intro.svg

intro.svg

#### Training-time Test Support

This high performance is largely driven by Eagle's novel Training-Time Test (TTT) architecture, which makes the draft model robust by simulating multi-step generation. Despite its power, TTT is notoriously difficult to implement due to its use of specialized attention masks and recursive data loops. SpecForge simplifies this complexity by providing built-in TTT support, referencing the official Eagle3 implementation to ensure correctness and optimal performance.

### Two Training Modes: Online and Offline

SpecForge simplifies hidden state collection by offering two versatile modes for training: Online and Offline. This two-mode design ensures flexibility across workflows, regardless of your model sizes or hardware limitations. [...] To bridge the gap between research and deployment, we built SpecForge—a purpose-built ecosystem for training draft models that integrate natively with SGLang. As soon as training completes, models are ready for inference out of the box—no further adaptation needed. Meanwhile, training effective draft models for today’s frontier LLMs—such as Llama 4, DeepSeek, and other Mixture-of-Experts (MoE) models—requires infrastructure that can handle their complexity and scale. SpecForge is purpose-built from the ground up to meet these demands, bridging the gap between cutting-edge research and real-world deployment.

Key Capabilities of SpecForge:

## Key Features of SpecForge

### Eagle3 Integration [...] LMSYS

Contents

# SpecForge: Accelerating Speculative Decoding Training for SGLang

Speculative decoding is a powerful technique for accelerating Large Language Model (LLM) inference. In this blog post, we are excited to announce the open-sourcing of SpecForge, our new training framework for Eagle3-based speculative decoding. SpecForge is designed for ease of use and is tightly integrated with the SGLang inference engine, enabling a seamless transition from training to deployment.

## Why a New Speculative Decoding Training Framework

Title: GitHub - sgl-project/SpecForge: Train speculative decoding models effortlessly and port them smoothly to SGLang serving.
URL: https://github.com/sgl-project/SpecForge
Content: | .gitignore | .gitignore | Qwen2.5-VL-7B egale3 train (  support qwen2_5_vl online  delete nohup  add qwen2.5-vl eagle model  add todo  clean dev code  support batch and fix position_ids bug  add eval wandb metrics  fix eval bug  fix eval dataloader bug  add comment  merge main  rename vlm online eagle3 model name  clean code  fix ttt input embeds bug Co-authored-by: Yingyi Huang <[REDACTED]>  fix eval metrics bug  merge qwen-vl draft model to llama3 Co-authored-by: Yingyi Huang <[REDACTED]>  fix qwen vl train shell  add timeout config Co-authored-by: Yingyi Huang <[REDACTED]>  qwenvl draft input without image embedding Co-authored-by: Yingyi Huang <[REDACTED]>  qwenvl draft input without image embedding Co-authored-by: [...] ## Repository files navigation

   README
   MIT license

Image 2: logo
Image 3: documentationImage 4: SpecBundleImage 5: DeepWiki

Image 6: github badgeImage 7: slack badgeImage 8: license

## 📍 Overview

 and SpecForge v0.2. Check out our blog at LMSYS.org
   [2025-12] 🔔 Released the roadmap for 2026 Q1.
   [2025-08] 🔔 SpecForge is listed as a flagship project in LMSYS. Congratulations to the SpecForge team!
   [2025-08] 🔥 SpecForge powered the Eagle3 draft model for GPT-OSS. Check out the blog at LMSYS.org
   [2025-07] 🔥 SpecForge is released together with Llama4-Eagle3 checkpoints. Check out our blog at LMSYS.org

## ✨ Acknowledgements

[](

Image 9: acknowledgements [...] ## 📃 Citation

[](

undefinedbibtex
@misc{specforge2025,
  title={SpecForge: Train speculative decoding models effortlessly},
  author={Shenggui Li, Yikai Zhu, Chao Wang, Fan Yin, Shuai Shi, Yubo Wang, Yi Zhang, Yingyi Huang, Haoshuai Zheng, Yineng Zhang},
  year={2025},
  publisher={GitHub},
  howpublished={\url{
}
undefined

## About

Train speculative decoding models effortlessly and port them smoothly to SGLang serving.

docs.sglang.ai/SpecForge/

### Topics

trainingeaglepytorchllmfsdpsglangeagle3

### Resources

Readme

### License

MIT license

### Uh oh!

There was an error while loading. Please reload this page.

Activity

Custom properties

### Stars

768 stars

### Watchers

7 watching

### Forks

201 forks

Report repository

## Releases

No releases published

## Packages 0

Title: [PDF] NOT-A-BANDIT: PROVABLY NO-REGRET DRAFTER SE
URL: https://openreview.net/pdf/a706fa14bedcfc5d571ddeeba9b5d91e6f805c75.pdf
Content: 2.3 EAGLE AND DRAFT TREE The EAGLE family is the most widely deployed speculative decoding models (Li et al., 2024a;b; 2025b). EAGLE-3 introduced multi-layer feature fusion with a training-time test mechanism. EAGLE-2 expands the draft tree with high-confidence tokens and prunes low-probability branches, improving efficiency by increasing the likelihood that more tokens are accepted per cycle. Specifically, instead of sampling from q1:K recursively like a language model, it generates a deterministic (1) draft-tree with Depth K and branching factor L. From the user_4813494d node (x≤t), EAGLE model q generates L children as possible choice of xt+1. These are chosen to be the tokens with L largest probabilities according to q1(·|x≤t). Then from each child, another L descendants (subsequent tokens) [...] 4.2 CURATING DIVERSE DRAFTERS FOR LARGE-SCALE EVALUATION To thoroughly evaluate the effectiveness of our framework at scale, we build 21 drafters upon the official EAGLE-3 models (Li et al., 2025b; Tengyunw, 2025; Contributors, 2025) and finetune them on seven open-sourced datasets spanning multiple domains: Python (jtatman, 2025), Math (Toshniwal et al., 2024), Biology (Wesney, 2025), Chemistry (mlfoundations dev, 2025), MedicalQA (Chen et al., 2024), CNN DM (Nallapati et al., 2016) and SQL (Meyer et al., 2024). The statistics of the resulting Llama and Qwen drafters are summarized in Table 1, 6 and 7. We observe that finetuning the generic EAGLE on a specific domain can greatly enhance its in-domain ability. We use SpecForge (Li et al., 2025a) as the training pipeline. In the meantime, [...] URL 
Taehyeon Kim, Hojung Jung, and Se-Young Yun. A unified framework for speculative decoding with multiple drafters as a bandit. 2024.
Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via speculative decoding. In International Conference on Machine Learning, pp. 19274–19286. PMLR, 2023.
Shenggui Li, Yikai Zhu, Chao Wang, Fan Yin, Shuai Shi, Yubo Wang, Yi Zhang, Yingyi Huang, Haoshuai Zheng, and Yineng Zhang. Specforge: Train speculative decoding models effortlessly.
 2025a. GitHub repository.
Yuhui Li, Fangyun Wei, Chao Zhang, and Hongyang Zhang. EAGLE: Speculative sampling requires rethinking feature uncertainty. In International Conference on Machine Learning, 2024a.

Title: How to train custom EAGLE-3 heads for speculative decoding
URL: https://www.baseten.co/blog/how-to-train-custom-eagle-3-heads-for-speculative-decoding/
Content: Recommended: 7–9

Setting this too low can cause the head to be brittle at inference time when it encounters its own (imperfect) draft tokens as input.

### Number of draft tokens

The number of tokens the head proposes during inference before the target model verifies. More draft tokens means more potential speedup per step, but also a higher chance of a mismatch (and wasted compute on incorrect predictions).

Recommended: 3–4 at inference time

Going higher (e.g., 8) rarely helps because prediction accuracy drops off and verification cost grows.

### Learning rate (LR)

Scaling the learning rate with model size is important. Larger models have more parameters and are more sensitive to large gradient updates, so they need smaller learning rates to train stably. [...] ## Conclusion

Training custom EAGLE-3 heads is a high-leverage optimization for any team serving LLMs in latency-sensitive settings. The process is straightforward: prepare a representative dataset with regenerated outputs, configure a handful of hyperparameters, and train a lightweight head. But getting the data distribution right, matching chat templates, and tuning TTT-length make the difference between a head that provides meaningful speedup and one that doesn't. [...] ## What is EAGLE-3?

EAGLE-3 is a speculative decoding method for autoregressive LLM inference. The core idea is that you attach a small, lightweight "draft head" to your target model that predicts multiple future tokens at once. The target model then verifies those predictions in a single forward pass. When the draft head is accurate, you skip multiple decoding steps, which dramatically reduces end-to-end latency.

eagle

While EAGLE papers report up to 4–6x speedups in benchmarks, some of that gain comes from differences in serving frameworks rather than the draft head alone. In production, we typically observe 1.5–2.5x latency improvements attributable to the EAGLE head itself.

A few key properties make EAGLE-3 practical:

Title: Adding New Speculative Decoding Algorithms - Speculators Docs
URL: https://docs.vllm.ai/projects/speculators/en/latest/algorithms/add_new_algorithms/
Content: ## Step-by-Step Guide

### 1. Create Algorithm Module

Create a self-contained directory for your algorithm under `src/speculators/models`. See `src/speculators/models/eagle3` as an example. This keeps algorithm logic isolated and maintainable. Each algorithm owns its configuration, model definition, and any custom components. Example file structure:

```
src/speculators/models |-> eagle3 |-> ... |-> new_algorithm  |-> __init__.py  |-> core.py  |-> config.py 
```

### 2. Implement Configuration Class

Define how your algorithm is configured. The config stores hyperparameters, architectural choices, and other settings. It's serialized when saving models and deserialized when loading them. In `config.py`, create a configuration class with the `@register` decorator, for example: [...] ### 5. Add CLI Arguments (Optional)

Add algorithm-specific command-line arguments to the training script. If your algorithm has unique hyperparameters (like Eagle3's `--ttt-steps` or a custom `--block-size`), users need a way to configure them from the command line. These arguments are passed to your `from_training_args()` method. Only add arguments if your algorithm needs parameters beyond the common ones (verifier path, number of layers, etc.).

Reference: See `scripts/train.py`

### 6. Train Your Model

The training script should automatically works with your new algorithm: [...] In `__init__.py`, export your config and model classes.

```
from speculators.models.eagle3.config import Eagle3SpeculatorConfig from  speculators.models.eagle3.config  import Eagle3SpeculatorConfigfrom speculators.models.eagle3.core import Eagle3DraftModel from  speculators.models.eagle3.core  import Eagle3DraftModel  __all__ = [ __all__ =[ "Eagle3DraftModel", "Eagle3DraftModel", "Eagle3SpeculatorConfig", "Eagle3SpeculatorConfig",] ]
```

Reference: See `src/speculators/models/eagle3/__init__.py`

### 5. Add CLI Arguments (Optional)

Title: Train with Eagle3 Speculative Decoding — NeMo-RL
URL: https://docs.nvidia.com/nemo/rl/nightly/guides/eagle3-speculative-decoding.html
Content: the `draft.` weights into the vLLM drafter

`draft.`

That keeps the rollout drafter aligned with the latest RL-updated policy instead of a stale checkpoint.

### Training Path#

During the policy forward pass, NeMo RL captures:

token input embeddings

a small set of intermediate hidden states from auxiliary policy layers

Those captured activations are the Eagle inputs. NeMo RL captures an early/middle/late-style set of policy layers for Eagle3, then the draft model predicts logits with its own draft LM head. That LM head is loaded from the draft checkpoint when `lm_head.weight` is present and otherwise initialized from the current policy output layer.

`lm_head.weight`

### Draft Loss and Time-Step Alignment# [...] `policy.draft.enabled`

`policy.draft.model_name`: checkpoint used to initialize the draft model

`policy.draft.model_name`

`policy.draft.loss_weight`: weight on the auxiliary draft loss

`policy.draft.loss_weight`

`policy.generation.vllm_kwargs.speculative_config.model`: draft checkpoint used by the vLLM drafter

`policy.generation.vllm_kwargs.speculative_config.model`

`policy.generation.vllm_kwargs.speculative_config.draft_tensor_parallel_size`: tensor parallelism used by the drafter inside vLLM

`policy.generation.vllm_kwargs.speculative_config.draft_tensor_parallel_size`

`policy.generation.vllm_kwargs.speculative_config.num_speculative_tokens`: number of speculative tokens proposed by vLLM

`policy.generation.vllm_kwargs.speculative_config.num_speculative_tokens`

## Notes# [...] `nemo_rl`
`nemo_rl.evals`
`nemo_rl.evals.eval`
`nemo_rl.evals.answer_parsing`
`nemo_rl.utils`
`nemo_rl.utils.nvml`
`nemo_rl.utils.config`
`nemo_rl.utils.packed_tensor`
`nemo_rl.utils.native_checkpoint`
`nemo_rl.utils.flops_formulas`
`nemo_rl.utils.flops_tracker`
`nemo_rl.utils.nsys`
`nemo_rl.utils.timer`
`nemo_rl.utils.memory_tracker`
`nemo_rl.utils.venvs`
`nemo_rl.utils.checkpoint`
`nemo_rl.utils.prefetch_venvs`
`nemo_rl.utils.logger`
`nemo_rl.algorithms`
`nemo_rl.algorithms.loss`
`nemo_rl.algorithms.distillation`
`nemo_rl.algorithms.utils`
`nemo_rl.algorithms.logits_sampling_utils`
`nemo_rl.algorithms.reward_functions`
`nemo_rl.algorithms.async_utils`
`nemo_rl.algorithms.grpo`
`nemo_rl.algorithms.advantage_estimator`
`nemo_rl.algorithms.rm`
`nemo_rl.algorithms.dpo`

Title: Speculative Decoding - vLLM
URL: https://docs.vllm.ai/en/latest/features/speculative_decoding/
Content: configs 
        + AXK1
        + afmoe
        + arctic
        + bagel
        + chatglm
        + cheers
        + colmodernvbert
        + colpali
        + colqwen3
        + deepseek\_vl2
        + dotsocr
        + eagle
        + extract\_hidden\_states
        + falcon
        + fireredlid
        + flex\_olmo
        + funaudiochat
        + hunyuan\_vl
        + hyperclovax
        + isaac
        + jais
        + kimi\_k25
        + kimi\_linear
        + kimi\_vl
        + lfm2\_moe
        + medusa
        + midashenglm
        + mistral
        + mlp\_speculator
        + moonvit
        + nemotron
        + nemotron\_h
        + olmo\_hybrid
        + ovis
        + parakeet
        + qwen3\_5
        + qwen3\_5\_moe
        + qwen3\_asr
        + qwen3\_next [...] spec\_decode 
        + dflash
        + draft\_model
        + eagle
        + extract\_hidden\_states
        + medusa
        + metadata
        + metrics
        + ngram\_proposer
        + ngram\_proposer\_gpu
        + suffix\_decoding
        + utils
       structured\_output

          structured\_output 
        + backend\_guidance
        + backend\_lm\_format\_enforcer
        + backend\_outlines
        + backend\_types
        + backend\_xgrammar
        + request
        + utils
       worker [...] | Method | Low QPS (latency focused) | High QPS (throughput focused) | Notes |
 ---  --- |
| EAGLE | High gain | Medium to high gain | Strong general-purpose model-based method. |
| MTP | High gain | Medium to high gain | Best when the target model has native MTP support. |
| Draft model | High gain | Medium gain | Needs a separate draft model. |
| Parallel Draft Model | High gain | Medium to high gain | Low draft model latency. |
| MLP speculator | Medium to high gain | Medium gain | Good when compatible MLP speculators are available. |
| N-gram | Low to medium gain | Medium gain | Lightweight and easy to enable. |
| Suffix decoding | Low to medium gain | Medium gain | No extra draft model; dynamic speculation depth. |
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "EAGLE-3 \"layer 0\" \"layer 16\" \"layer 31\" OR \"layer 15\" OR \"layer 10\" OR \"layer 20\" auxiliary hidden state layers selection llama",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: deepseek_eagle3 - vLLM
URL: https://docs.vllm.ai/en/v0.18.2/api/vllm/model_executor/models/deepseek_eagle3/
Content: quant_config = get_draft_quant_config(vllm_config)   self.hidden_size = config.hidden_size self. hidden_size = config. hidden_size rope_scaling = getattr(config, "rope_scaling", None) rope_scaling = getattr(config, "rope_scaling", None) max_position_embeddings = getattr(config, "max_position_embeddings", 8192) max_position_embeddings = getattr(config, "max_position_embeddings", 8192)   self.layer_idx = layer_idx self. layer_idx = layer_idx   # MLA attention parameters # MLA attention parameters qk_nope_head_dim = getattr(config, "qk_nope_head_dim", 0) qk_nope_head_dim = getattr(config, "qk_nope_head_dim", 0) qk_rope_head_dim = getattr(config, "qk_rope_head_dim", 0) qk_rope_head_dim = getattr(config, "qk_rope_head_dim", 0) v_head_dim = getattr(config, "v_head_dim", 0) v_head_dim = [...] hidden_states = self.hidden_norm(hidden_states) hidden_states = self. hidden_norm(hidden_states) return hidden_states, residual return hidden_states, residual   def forward( def  forward( self, self, positions: torch.Tensor, positions: torch. Tensor, embeds: torch.Tensor, embeds: torch. Tensor, hidden_states: torch.Tensor, hidden_states: torch. Tensor, residual: torch.Tensor | None, residual: torch. Tensor | None, ) -> tuple[torch.Tensor, torch.Tensor]: ) -> tuple[torch. Tensor, torch. Tensor]: if self.layer_idx == 0: if self. layer_idx == 0: # First layer: concatenate embeds with hidden_states # First layer: concatenate embeds with hidden_states embeds = self.input_layernorm(embeds) embeds = self. input_layernorm(embeds) hidden_states, residual = [...] torch. Tensor:  # Combine multiple auxiliary hidden states returned by Eagle3 # Combine multiple auxiliary hidden states returned by Eagle3 return self.model.fc(hidden_states) return self. model. fc(hidden_states)   def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]): def  load_weights(self, weights: Iterable[tuple[str, torch. Tensor]]): model_weights = {} model_weights ={} includes_draft_id_mapping = False includes_draft_id_mapping = False includes_embed_tokens = False includes_embed_tokens = False   for name, loaded_weight in weights: for name, loaded_weight in weights: if "t2d" in name: if "t2d" in name:  continue continue if "d2t" in name: if "d2t" in name: name = name.replace("d2t", "draft_id_to_target_id") name = name. replace("d2t", "draft_id_to_target_id")

Title: EAGLE-3 Speculative Decoding: 2-6x Faster LLM Inference Guide
URL: https://www.e2enetworks.com/blog/Accelerating_LLM_Inference_with_EAGLE
Content: EAGLE-3 closes this gap by simulating the actual generation process during training. Some positions see fused features from the target model, while others see the draft model's own outputs fed back in. This mixed regime matches what happens at inference. In the paper's MT-bench experiments, this lets EAGLE-3 keep a high, almost flat acceptance rate of around 70-80% across positions, whereas EAGLE's acceptance rate drops noticeably as more draft tokens appear in the context.

Now, let's dive into each layer of Eagle-3.

## Multi-Layer Feature Fusion

The problem with top-layer-only approaches [...] Here's how the fusion works. For example, for a model like Llama-3.1-8B with hidden dimension 4096, each level produces a 4096-dimensional vector. EAGLE-3 concatenates these three vectors into a 12,288-dimensional vector, then compresses it back down to 4096 dimensions through a fully connected layer. This compression step learns which features from each level matter most for predicting multiple tokens ahead. [...] Load tokenized conversations from the dataset cache
 Generate target model features: Query the SGLang server to get hidden states from multiple layers (low, middle, high) of the target model for the current batch
 Fuse multi-layer features: Concatenate features from the three layers and compress them through a learned projection layer
 Draft head forward pass with training-time test:
  + Native prediction (step 0): Use target model features to predict the next token
  + Simulated prediction (steps 1-6): Feed the draft head's own predictions back as input to simulate multi-step generation during inference
  + Generate predictions for all positions up to `--ttt-length` (default 7 steps ahead)

Title: From research to production: Accelerate OSS LLM with EAGLE-3 on ...
URL: https://lmsys.org/blog/2025-12-01-eagle3-vertex/
Content: This is where EAGLE-3 (Extrapolative Attention Guided LEarning) comes in. EAGLE-3 is a more advanced approach. Instead of a whole separate model, it attaches an extremely lightweight 'draft head'—just 2-5% of the target model's size—directly to its internal layers. This head operates at both feature and token level, ingesting features from the target model's hidden states to extrapolate and predict a tree of future tokens.

The result? All the benefits of speculative decoding while eliminat[ing] the overhead of training and running a second model. [...] EAGLE-3's approach is far more efficient than the complex, resource-intensive task of training and maintaining a separate, multi-billion parameter draft model. You train only a lightweight 'draft head'—just 2% to 5% of the target model size—that is added as part to your existing model. This simpler, efficient training process delivers a significant 2x-3x decoding performance gain for models like Llama 70B (depending on the workload types, e.g. multi-turn, code, long context and more).

But moving even this streamlined EAGLE-3 approach from a paper to a scaled, production-ready cloud service is a real engineering journey. This post shares our technical pipeline, key challenges, and the hard-won lessons we learned along the way.

## Challenge #1: Preparing the data [...] ## Benchmark Results

After this journey, was it worth it? Absolutely.

We benchmarked our trained EAGLE-3 head against the non-speculative baseline using SGLang with Llama 4 Scout 17B Instruct. Our benchmarks show a 2x-3x speedup in decoding latency and significant throughput gains depending on the workload types.

See the full details and benchmark it yourself using our comprehensive notebook.

### Metric 1: Median Time Per Output Token (TPOT)

This chart shows the better latency performance of EAGLE-3. The Time Per Output Token (TPOT) chart shows EAGLE-3-accelerated model (green line) consistently achieves a lower (faster) latency than the baseline (blue line) across all tested concurrency levels.

### Metric 2: Output Throughput

Title: Google Released Gemma-4 Four Days Ago. We Already Made It 1.72× Faster.
URL: https://huggingface.co/blog/lujangusface/tw-eagle3-gemma4
Content: ## Why Gemma-4 Is Different

Most EAGLE3 work targets standard dense transformers (Llama, Qwen) or MoE models (GLM-4.7-Flash, MiniMax). Gemma-4-31B is neither — it's a hybrid-attention dense model with two fundamentally different layer types:

This means the KV cache cannot be a uniform tensor. Each layer type has different shapes, different head counts, and different memory requirements. Every inference engine that serves Gemma-4 must maintain two separate memory pools — and when EAGLE3's tree verification starts rapidly allocating and freeing cache entries across both pools simultaneously, things break in ways nobody anticipated.

03-architecture

03-architecture [...] ### Always train with the backend you'll serve with

EAGLE3 draft heads learn from the target model's hidden state distributions at specific layers. If you train with one backend (e.g., HuggingFace Transformers) and serve with another (e.g., SGLang), those hidden states can diverge significantly — we measured up to 32% difference at the layer closest to the output. The result: a draft that looks great during training (acc\_0 = 0.85–0.87) but achieves only ~13% acceptance at inference time. Retraining with `--target-model-backend sglang` fixed it immediately (acc\_0 = 0.75–0.82, real-world acceptance matching expectations). This applies to any EAGLE3 deployment, not just Gemma-4.

`--target-model-backend sglang`

### Three bugs in the serving stack [...] 01-decoding-comparison

01-decoding-comparison

EAGLE3 (NeurIPS 2025) trains a specialized draft head that conditions on the target model's own internal representations from three points — early, middle, and late layers — rather than being an independent smaller model. This makes the draft much better at predicting what the target would say. The draft head is tiny (~277 MB) and co-deploys on the same GPU.

For a deeper dive on how speculative decoding works, the accept/reject rule, and the math behind the speedup curve, see our previous post on EAGLE3 for GLM-4.7-Flash.

## Results

We are releasing thoughtworks/Gemma-4-31B-Eagle3 — to our knowledge, the first publicly available EAGLE3 draft head for the Gemma-4 architecture.

Title: yuhuili/EAGLE-LLaMA3-Instruct-8B · Hugging Face
URL: https://huggingface.co/yuhuili/EAGLE-LLaMA3-Instruct-8B
Content: EAGLE-3 removes the feature prediction constraint in EAGLE and simulates this process during training using training-time testing. Considering that top-layer features are limited to next-token prediction, EAGLE-3 replaces them with a fusion of low-, mid-, and high-level semantic features.
EAGLE-3 further improves generation speed while ensuring lossless performance.

demogif

demogif

Inference is conducted on 2x RTX 3090 GPUs at fp16 precision using the Vicuna 13B model.

## Support

EAGLE has been merged in the following mainstream LLM serving frameworks (listed in alphabetical order).

## Reference

For technical details and full experimental results, please check the paper of EAGLE, the paper of EAGLE-2, and the paper of EAGLE-3. [...] Hugging Face's logo

# yuhuili / EAGLE-LLaMA3-Instruct-8B like 5

EAGLE

EAGLE

# EAGLE

| EAGLE |
EAGLE-2 |
EAGLE-3 |
Blog |

Version
License
Maintenance
Contributions welcome

Version
License
Maintenance
Contributions welcome

## 

benchmark

benchmark

EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency) is a new baseline for fast decoding of Large Language Models (LLMs) with provable performance maintenance. This approach involves extrapolating the second-top-layer contextual feature vectors of LLMs, enabling a significant boost in generation efficiency.

EAGLE-2 uses the confidence scores from the draft model to approximate acceptance rates, dynamically adjusting the draft tree structure, which further enhances performance. [...] `@inproceedings{li2024eagle,
author = {Yuhui Li and Fangyun Wei and Chao Zhang and Hongyang Zhang},
title = {{EAGLE}: Speculative Sampling Requires Rethinking Feature Uncertainty},
booktitle = {International Conference on Machine Learning},
year = {2024}
}
@inproceedings{li2024eagle2,
author = {Yuhui Li and Fangyun Wei and Chao Zhang and Hongyang Zhang},
title = {{EAGLE-2}: Faster Inference of Language Models with Dynamic Draft Trees},
booktitle = {Empirical Methods in Natural Language Processing},
year = {2024}
}
@inproceedings{li2025eagle3,
author = {Yuhui Li and Fangyun Wei and Chao Zhang and Hongyang Zhang},
title = {{EAGLE-3}: Scaling up Inference Acceleration of Large Language Models via Training-Time Test},
booktitle = {Annual Conference on Neural Information Processing Systems},

Title: Deep Dive into LlaMA 3 by Hand ✍️ | Towards Data Science
URL: https://towardsdatascience.com/deep-dive-into-llama-3-by-hand-%EF%B8%8F-6c6b23dc92b2/
Content: ###  Vocabulary-size and Attention Layers

Next up is the Transformer class which defines the vocabulary size and the number of layers. Once again the vocabulary size here refers to the set of words (and tokens) that the model can recognize and process. Attention layers here refer to the transformer block (the combination of the attention and feed-forward layers) used in the model.

Based on these numbers, LlaMA 3 has a vocabulary size of 128K which is quite large. Additionally, it has 32 copies of the transformer block.

###  Feature-dimension and Attention-Heads [...] The original source code where these numbers are stated can be found here.

Keeping these values in mind, the next steps illustrate how each of them play their part in the model. They are listed in their order of appearance in the source-code.

###  The context-window

While instantiating the LlaMa class, the variable \_max\_seqlen defines the context-window. There are other parameters in the class but this one serves our purpose in relation to the transformer model. The \_max\_seqlen here is 8K which implies the attention head is able to scan 8K tokens at one go.

###  Vocabulary-size and Attention Layers [...] ###  Multiple-layers of the Transformer block

LlaMA 3 combines 32 of these above transformer blocks with the output of one passing down into the next block until the last one is reached.

###  Let’s put it all together

Once we have set all the above pieces in motion, it is time to put it all together and see how they produce the LlaMA effect.

So, what is happening here?

Step 1 : First we have our input matrix, which is the size of 8K (context-window) x 128K (vocabulary-size). This matrix undergoes the process of embedding which takes this high-dimensional matrix into a lower dimension.

Title: Train with Eagle3 Speculative Decoding — NeMo-RL
URL: https://docs.nvidia.com/nemo/rl/nightly/guides/eagle3-speculative-decoding.html
Content: the `draft.` weights into the vLLM drafter

`draft.`

That keeps the rollout drafter aligned with the latest RL-updated policy instead of a stale checkpoint.

### Training Path#

During the policy forward pass, NeMo RL captures:

token input embeddings

a small set of intermediate hidden states from auxiliary policy layers

Those captured activations are the Eagle inputs. NeMo RL captures an early/middle/late-style set of policy layers for Eagle3, then the draft model predicts logits with its own draft LM head. That LM head is loaded from the draft checkpoint when `lm_head.weight` is present and otherwise initialized from the current policy output layer.

`lm_head.weight`

### Draft Loss and Time-Step Alignment# [...] `policy.draft.enabled`

`policy.draft.model_name`: checkpoint used to initialize the draft model

`policy.draft.model_name`

`policy.draft.loss_weight`: weight on the auxiliary draft loss

`policy.draft.loss_weight`

`policy.generation.vllm_kwargs.speculative_config.model`: draft checkpoint used by the vLLM drafter

`policy.generation.vllm_kwargs.speculative_config.model`

`policy.generation.vllm_kwargs.speculative_config.draft_tensor_parallel_size`: tensor parallelism used by the drafter inside vLLM

`policy.generation.vllm_kwargs.speculative_config.draft_tensor_parallel_size`

`policy.generation.vllm_kwargs.speculative_config.num_speculative_tokens`: number of speculative tokens proposed by vLLM

`policy.generation.vllm_kwargs.speculative_config.num_speculative_tokens`

## Notes# [...] `lm_head.weight`

### Draft Loss and Time-Step Alignment#

The draft loss compares draft logits against detached policy logits, but only after aligning both sides to the same next-token event.

Suppose the policy input sequence is:

The policy forward pass produces hidden states and logits at those positions:

For Eagle training, NeMo RL does not compare raw `p0, p1, p2, p3` directly to the raw draft output. Instead it shifts the draft inputs and teacher outputs so draft position `t` predicts the teacher distribution for position `t+1`.

`p0, p1, p2, p3`
`t`
`t+1`

First, it rolls the captured input embeddings left by one token:

Then it rolls the detached teacher logits left by one position:

So the aligned draft-training pairs become:

In words:

use the hidden state at position `t`

Title: Understand How Llama3.1 Works — A Deep Dive Into the Model Flow | by Xiaojian Yu | Medium
URL: https://medium.com/@yuxiaojian/understand-how-llama3-1-works-a-deep-dive-into-the-model-flow-b149aba04bed
Content: LlamaForCausalLM(  (model): LlamaModel(    (embed_tokens): Embedding(128256, 4096)    (layers): ModuleList(      (0-31): 32 x LlamaDecoderLayer(        (self_attn): LlamaSdpaAttention(          (q_proj): Linear4bit(in_features=4096, out_features=4096, bias=False)          (k_proj): Linear4bit(in_features=4096, out_features=1024, bias=False)          (v_proj): Linear4bit(in_features=4096, out_features=1024, bias=False)          (o_proj): Linear4bit(in_features=4096, out_features=4096, bias=False)          (rotary_emb): LlamaRotaryEmbedding()        )        (mlp): LlamaMLP(          (gate_proj): Linear4bit(in_features=4096, out_features=14336, bias=False)          (up_proj): Linear4bit(in_features=4096, out_features=14336, bias=False)          (down_proj): Linear4bit(in_features=14336, [...] # Process through each layer of the modelfor layer_idx, layer in enumerate(base_model_bnb_4b.model.layers):    print(f"Processing layer {layer_idx}")        # 1. Input LayerNorm    normalized_hidden_states = layer.input_layernorm(hidden_states)        # 2. Self-attention mechanism    # 2.1 Query, Key, Value projections    query_states = layer.self_attn.q_proj(normalized_hidden_states)    key_states = layer.self_attn.k_proj(normalized_hidden_states)    value_states = layer.self_attn.v_proj(normalized_hidden_states)        # 2.2 Reshape and transpose Q, K, V    # (batch_size, seq_length, num_heads, head_dim) -> (batch_size, num_heads, seq_length, head_dim)    query_states = query_states.view(batch_size, seq_length, layer.self_attn.num_heads, layer.self_attn.head_dim).transpose(1, 2) [...] # Final LayerNorm
# Normalize the hidden states from the last layer
# Language Model Head
# Project the normalized hidden states to the vocabulary space
# Get the logits for the last token
# We're only interested in predicting the next token, so we take the last position 1
# Note: The following line is commented out as we're using a more sophisticated sampling method
# next_token = torch.argmax(last_token_logits, dim=-1)
# Step 7: Apply temperature
# Temperature adjusts the randomness of predictions. Lower values make the model more confident.0.1
# Step 8: Apply top-p (nucleus) sampling
# This method truncates the least likely tokens whose cumulative probability exceeds (1 - top_p)0.9
# Sort logits in descending order True
# Calculate cumulative probabilities 1 1

Title: I've been looking into using the last hidden layer of an off-the-shelf LLM to he... | Hacker News
URL: https://news.ycombinator.com/item?id=42380033
Content: information (the distribution over the next token is just a projection from the embedding space). E.g. it would be useless for any classification task. | | | |  |  | danielmarkbruce on Dec 12, 2024  | user_4813494d | parent | next (javascript:void(0))   Various models in production are doing exactly that - training a layer which takes the vector out of the last hidden layer, for classification, in place of the language head. I even have one in production right now doing regression using the output of the last hidden layer.... In the case of llama 3 its 4096 \ 16 bit = 8192 bytes of information...that's like 8192 characters of ascii. More than enough for most classification tasks... and if you jsut spend any time thinking about encoding the logits for a vocab of 128k... you'll come to the [...] parent | next (javascript:void(0))   The last hidden layer outputs a vector which is then used to predict the probabilities of every token in the vocabulary, by a single layer (and, in practice now in llama models, this layer is the transpose of the embedding layer). That vector has a lot of information in it, it's not a debatable thing.  As noted above in parens, look at the llama 3.x models. The space is already shared in some sense. It's called "tied embedding". | | | |  |  | versteegen on Dec 12, 2024  | user_4813494d | parent | next (javascript:void(0))   > That vector has a lot of information in it, it's not a debatable thing. Encoding the next token is the minimum possible amount of information it might contain; that's not much information (the distribution over the next token is just a

Title: Hidden Layers: Decoded (Meta's Llama 3.2, OpenAI, Microsoft, Nobel Prize Reactions, GraphRAG & more)
URL: https://www.youtube.com/watch?v=HBXWkl4KSKs
Content: what I found there were so many of those they were like on the origin of probably 10,000 you know very fine grain topics I think well I need a higher level hierarchy to understand so there's a great website called papers with code that I know we we track all the time has papers but it also has methods and data sets and um basically I said there I think they like 17 or 18 sort of top level ml categories and so initially I tried to get the LM to say show to paper which of these categories is this about and they would just absolutely huc Nate and not picking different categories they make up stuff outside that list I would ask so nicely I asked so nicely please why only with one of these from this list I said nope we wouldn't do it so finally I just gave up and I went back and I think I [...] ### Transcript: [...] PhD in physics looking at uh you know dynamical systems nonlinear system chaotic systems so this paper um is really ambitious because they're trying to see if they can uh understand in a deep way how intelligence emerges so what they did was they they um used uh cellular automa um and just in case somebody's listening to this they don't know what that is um they use what are called ECA Elementary cellular automatas very basic they're two-dimensional grids each um you can think of almost like a like a chess board and each square has a binary State it's either off it's or its on and you start with some random State and there are rules based upon uh the states next to you to how you change your state whether you would you know turn off or on it's like the game of life right it's like game of
```

> AGENT

Let me now look at the actual EAGLE-3 paper more carefully, and also check the SpecForge codebase for the concrete layer indices used.

> TOOL

tool_use mcp__tavily__tavily_extract
```json
{
  "query": "auxiliary hidden state layers selection methodology which specific layer indices low middle high",
  "urls": [
    "https://arxiv.org/pdf/2503.01840"
  ]
}
```

> TOOL

tool_result mcp__tavily__tavily_extract
```
Detailed Results:

Title: [PDF] arXiv:2503.01840v3 [cs.CL] 23 Apr 2025
URL: https://arxiv.org/pdf/2503.01840
Content: undefined
Raw Content: How can LM Head I Target Model 𝑙how 𝑙can Decoder Layers Embedding 𝑚how 𝑚can Decoder Layers ℎhow ℎcan Decoder Layers Decoder Layers ℎhow ℎcan Concat 𝑚how 𝑚can 𝑙how 𝑙can FC Layer 𝑔how 𝑔can I Decoder Layer FC Layer can 𝑔can 𝑔how 𝑒can 𝑒I 𝑎I LM Head I can do do 𝑔can 𝑔how 𝑒can 𝑒I 𝑎I 𝑒do Decoder Layer FC Layer 𝑎do LM Head it I do 𝑔can 𝑔how 𝑒can 𝑒I 𝑎I 𝑒do it 𝑎do 𝑒it ...
① ② ③ can 𝑎can 𝑎I 𝑎can Figure 5: Diagram of the EAGLE-3 inference pipeline, illustrating the three steps of the draft model. l, m, and h represent the low, middle, and high-level features of the target model, respectively. e denotes the embedding.
3 EAGLE-3 In this section, we provide a detailed description of the implementation of EAGLE-3. [...] 3.1 Inference Pipeline Consistent with other speculative sampling meth-ods, EAGLE-3 alternates between the drafting and verification stages. The difference between EAGLE-3 and EAGLE lies in the drafting stage, which we introduce with an example, as shown in Figure 5. Consider the prefix “How can”. Dur-ing the prefill phase or the previous verification stage, the target model performs a forward pass to generate the next token, “I”. We record the low, middle, and high-level feature sequences from the target model’s forward pass, denoted as l, m, and h, respectively. We concatenate the k-dimensional vectors l, m, and h to form a 3k-dimensional vector, then pass it through a fully connected (FC) layer to reduce it to k-dimensions, obtaining a feature g that integrates information from [...] Instead of reusing only the top-layer features, we integrate and leverage low-, mid-, and high-level features from the target model, capturing rich semantic information from different lay-1 2 4 8 0.72 0.74 0.76 0.78 0.80 0-EAGLE EAGLE without fea pred EAGLE-3 1 2 4 8 0.2 0.3 0.4 0.5 0.6 0.7 0.8 1-EAGLE EAGLE without fea pred EAGLE-3 Figure 4: Comparison of acceptance rates across differ-ent methods, with the x-axis representing the data scale relative to ShareGPT.
ers.
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "SpecForge EAGLE-3 \"aux_hidden_state_layers\" OR \"hidden_state_layers\" OR \"feature_layers\" config.json layer indices",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: nvidia/gpt-oss-120b-Eagle3-long-context · Clarification on the layer hidden state source
URL: https://huggingface.co/nvidia/gpt-oss-120b-Eagle3/discussions/1
Content: Hugging Face's logo

# nvidia / gpt-oss-120b-Eagle3-long-context like 65 Follow NVIDIA 55.4k

## Clarification on the layer hidden state source

Eagle 3 default layer indices for this model would be 2,18,33  
The config specified 1, 17, 32  
Want to clarify, using layer indexing from 0 to 35 for this model, is it using input hidden states to layer 1,17,32 or output from layer 1,17,32?

That’s just the different notation of the layers. In SGLang the input hidden\_states of the layers (2,18,33) are used, while in TRTLLM we use the output hidden\_states of layers (1,17,32). Essentially they are the same

Got it, the hitrate seems to drop a lot with multi-gpu + trt-llm, any clue?

· Sign up or log in to comment

Title: README.md · chankhavu/Nemotron-Cascade2-30B-A3B-Eagle3-Long-Context at e9c70c41a1125f01e0b2083f7430098d89c8217b
URL: https://huggingface.co/chankhavu/c2.eagle3-test/blob/e9c70c41a1125f01e0b2083f7430098d89c8217b/README.md
Content: `sliding_window: 4096`

HF transformers (raw, no engine): the verifier exposes its
layers as `model.backbone.layers[0..51]`, where `layers[i]` is the
i-th character of `hybrid_override_pattern`. This is the canonical
reference. The training pipeline in this fork (SpecForge with the
NemotronH backend patch) reads from these indices via the
`aux_hidden_state_layers` config field on the draft.

`model.backbone.layers[0..51]`
`layers[i]`
`hybrid_override_pattern`
`aux_hidden_state_layers` [...] `target_hidden_state_indices: [2, 26, 48]`
`config.json`
`model.backbone.layers`

SGLang: SGLang's NemotronH implementation also uses 0-indexed
contiguous layer counting that matches HF, but as of late 2025 it
does NOT yet support sliding-window attention on Eagle3 drafts
(this draft has `sliding_window: 4096` in its config). Once SGLang
ships sw support, the layer indices should map cleanly. Until
then, prefer vLLM for serving this draft.

`sliding_window: 4096` [...] `[5, 12, 19, 26, 33, 42]`

### Engine-portability warning

Different inference engines may number layers differently because
of how they fuse, group, or skip blocks. Before serving this draft on
a new engine, verify that the engine's "layer i" corresponds to the
same character in the hybrid pattern as HF transformers does.

vLLM (0.19+): uses the full 52-layer ModuleList in its
NemotronH model implementation, 0-indexed contiguous, matches HF
transformers. The `target_hidden_state_indices: [2, 26, 48]` in
this draft's `config.json` is read directly by vLLM's Eagle3
speculative decoder and passed to the verifier as raw indices into
`model.backbone.layers`. Tested working on vLLM 0.19 with the
in-flight L=32k iteration.

Title: [Bug]: Inconsistent PP layer indexing in EAGLE model code · Issue #36151 · vllm-project/vllm · GitHub
URL: https://github.com/vllm-project/vllm/issues/36151
Content: `aux_hidden_states = []
for idx, layer in enumerate(
islice(self.layers, self.start_layer, self.end_layer)
):
if idx in self.aux_hidden_state_layers:
aux_hidden_states.append(hidden_states + residual)
hidden_states, residual = layer(positions, hidden_states, residual)`

This is not compatible with PP, because the `enumerate` is on the outside, so it will start from zero even when the layer indices start from `self.start_layer`. Valid solutions are to have the islice on the outside since `islice(enumerate(self.layers), self.start_layer, self.end_layer)` will pick up the right indices by slicing, or instead to provide a start index to the enumerate call directly as in `enumerate(islice(...), start=self.start_layer)`. Both are valid, but I think the former is a bit cleaner. [...] `enumerate`
`self.start_layer`
`islice(enumerate(self.layers), self.start_layer, self.end_layer)`
`enumerate(islice(...), start=self.start_layer)`

#36063 runs into this issue during a refactor of the EAGLE code, but I think it should be a follow-up work so that we can minimize the potential impact of the sweeping refactor, and have the PP fix more easily compatible with a rollback in case of unexpected side-effects.

### Before submitting a new issue...

## Metadata

## Metadata

### Assignees

### Labels

### Type

### Projects

### Milestone

### Relationships

### Development

## Issue actions

## Footer

### Footer navigation [...] ## Navigation Menu

# Search code, repositories, users, issues, pull requests...

# Provide feedback

We read every piece of feedback, and take your input very seriously.

# Saved searches

## Use saved searches to filter your results more quickly

To see all available qualifiers, see our documentation.

### Uh oh!

There was an error while loading. Please reload this page.

There was an error while loading. Please reload this page.

# [Bug]: Inconsistent PP layer indexing in EAGLE model code #36151

@benchislett

## Description

@benchislett

### Your current environment

Latest main

### 🐛 Describe the bug

For many EAGLE implementations, the layer iteration pattern is the following:

Title: SpecForge: Accelerating Speculative Decoding Training for SGLang
URL: https://lmsys.org/blog/2025-07-25-spec-forge/
Content: intro.svg

intro.svg

#### Training-time Test Support

This high performance is largely driven by Eagle's novel Training-Time Test (TTT) architecture, which makes the draft model robust by simulating multi-step generation. Despite its power, TTT is notoriously difficult to implement due to its use of specialized attention masks and recursive data loops. SpecForge simplifies this complexity by providing built-in TTT support, referencing the official Eagle3 implementation to ensure correctness and optimal performance.

### Two Training Modes: Online and Offline

SpecForge simplifies hidden state collection by offering two versatile modes for training: Online and Offline. This two-mode design ensures flexibility across workflows, regardless of your model sizes or hardware limitations. [...] To bridge the gap between research and deployment, we built SpecForge—a purpose-built ecosystem for training draft models that integrate natively with SGLang. As soon as training completes, models are ready for inference out of the box—no further adaptation needed. Meanwhile, training effective draft models for today’s frontier LLMs—such as Llama 4, DeepSeek, and other Mixture-of-Experts (MoE) models—requires infrastructure that can handle their complexity and scale. SpecForge is purpose-built from the ground up to meet these demands, bridging the gap between cutting-edge research and real-world deployment.

Key Capabilities of SpecForge:

## Key Features of SpecForge

### Eagle3 Integration [...] ## Key Features of SpecForge

### Eagle3 Integration

Eagle is a state-of-the-art method for speculative decoding designed to accelerate large language model inference. It achieves this by training a specialized, lightweight draft model to accurately predict the token distributions of a larger target model, leading to high acceptance rates and significant performance improvements.

intro.svg

intro.svg

#### Training-time Test Support

Title: SpecForge: Accelerating Speculative Decoding Training for SGLang - LMSYS Blog | LMSYS Org
URL: https://www.lmsys.org/blog/2025-07-25-spec-forge/
Content: To bridge the gap between research and deployment, we built SpecForge—a purpose-built ecosystem for training draft models that integrate natively with SGLang. As soon as training completes, models are ready for inference out of the box—no further adaptation needed. Meanwhile, training effective draft models for today’s frontier LLMs—such as Llama 4, DeepSeek, and other Mixture-of-Experts (MoE) models—requires infrastructure that can handle their complexity and scale. SpecForge is purpose-built from the ground up to meet these demands, bridging the gap between cutting-edge research and real-world deployment.

Key Capabilities of SpecForge:

## Key Features of SpecForge

### Eagle3 Integration [...] intro.svg

intro.svg

#### Training-time Test Support

This high performance is largely driven by Eagle's novel Training-Time Test (TTT) architecture, which makes the draft model robust by simulating multi-step generation. Despite its power, TTT is notoriously difficult to implement due to its use of specialized attention masks and recursive data loops. SpecForge simplifies this complexity by providing built-in TTT support, referencing the official Eagle3 implementation to ensure correctness and optimal performance.

### Two Training Modes: Online and Offline

SpecForge simplifies hidden state collection by offering two versatile modes for training: Online and Offline. This two-mode design ensures flexibility across workflows, regardless of your model sizes or hardware limitations. [...] ## Key Features of SpecForge

### Eagle3 Integration

Eagle is a state-of-the-art method for speculative decoding designed to accelerate large language model inference. It achieves this by training a specialized, lightweight draft model to accurately predict the token distributions of a larger target model, leading to high acceptance rates and significant performance improvements.

intro.svg

intro.svg

#### Training-time Test Support

Title: SpecForge: A Flexible and Efficient Open-Source Training Framework for Speculative Decoding | Takara TLDR
URL: https://tldr.takara.ai/p/2603.18567
Content: Large language models incur high inference latency due to sequential autoregressive decoding. Speculative decoding alleviates this bottleneck by using a lightweight draft model to propose multiple tokens for batched verification.   
  
However, its adoption has been limited by the lack of high-quality draft models and scalable training infrastructure. We introduce SpecForge, an open-source, production-oriented framework for training speculative decoding models with full support for EAGLE-3. [...] SpecForge incorporates target-draft decoupling, hybrid parallelism, optimized training kernels, and integration with production-grade inference engines, enabling up to 9.9x faster EAGLE-3 training for Qwen3-235B-A22B. In addition, we release SpecBundle, a suite of production-grade EAGLE-3 draft models trained with SpecForge for mainstream open-source LLMs.   
  
Through a systematic study of speculative decoding training recipes, SpecBundle addresses the scarcity of high-quality drafts in the community, and our draft models achieve up to 4.48x end-to-end inference speedup on SGLang, establishing SpecForge as a practical foundation for real-world speculative decoding deployment. [...] ## Resources

View on Hugging FaceRead PDFArXiv

### Stay in the loop

Every AI paper that matters, free in your inbox daily.

Home

### Pages

 About
 Search
 Favourites

### Tools

 MCP
 RSS
 llms.txt
 Sitemap

### Details

 © 2026takara.ai Ltd
 Content is sourced from third-party publications.

Title: SpecForge: Training speculative decoding models with SGLang — Tutorials for AI developers 8.0
URL: https://rocm.docs.amd.com/projects/ai-developer-hub/en/v8.0/notebooks/pretrain/SpecForge_SGlang.html
Content: SpecForge is a framework for training speculative decoding models so you can smoothly port them over to the SGLang serving framework to speed up your inference. It offers two methods of training the draft model: online and offline training. Online training freezes the target model and training draft model at same time, which generates auxiliary hidden states on the fly and needs multiple GPUs to achieve better performance. Offline training generates and saves the hidden states using the target model first and then trains the draft model in a separate process. Offline training requires as little as one GPU because it only needs to accommodate the draft model, but it needs a huge amount of disk space. For example, the UltraChat and ShareGPT datasets would need 12TB of storage. Due to the [...] `/path/to/SpecForge_Project`

Note: This command mounts the current directory to the `/SpecForge` directory in the container. Ensure the notebook file is either copied to this directory before running the Docker command or uploaded into the Jupyter Notebook environment after it starts. Save the token or URL provided in the terminal output to access the notebook from your web browser. You can download this notebook from the AI Developer Hub GitHub repository.

`/SpecForge`

### Step 2: Install and launch Jupyter#

Inside the Docker container, install Jupyter using the following command:

Start the Jupyter server: [...] ### Hardware#

AMD Instinct GPUs: This tutorial was tested on an AMD Instinct MI300X GPU node with eight GPUs. Ensure you are using a node with eight AMD Instinct GPUs or compatible hardware with ROCm support and that your system meets the official requirements.

### Software#

ROCm 6.3+: This tutorial requires ROCm 6.3 or later. Install and verify ROCm by following the ROCm install guide. After installation, confirm your setup using the `rocm-smi` command. AMD also provides prebuilt ROCm Docker images, for example, ROCm PyTorch, ROCm Ubuntu 22.04, and ROCm Ubuntu 24.04. You can use these prebuilt Docker images to reduce the effort of setting up a ROCm environment.

`rocm-smi`

Title: SpecForge/README.md at main · sgl-project/SpecForge · GitHub
URL: https://github.com/sgl-project/SpecForge/blob/main/README.md
Content: ## ✨ Acknowledgements

acknowledgements

acknowledgements

We would like to express our sincere gratitude to the official EAGLE team, especially Hongyang Zhang and Yuhui Li, for their invaluable contributions and support. Our thanks also go to the NVIDIA team—particularly Avery H and Izzy Putterman—and to the Google team, especially Ying Wang, for their insightful discussions and generous assistance throughout the project.

We are especially grateful to Meituan for their strong backing and meaningful contributions, which played a vital role in driving this project forward. [...] github badge
slack badge
license

## 📍 Overview

SpecForge is an ecosystem project developed by the SGLang team. It is a framework for training speculative decoding models so that you can smoothly port them over to the SGLang serving framework to speed up your inference.

We have seen many open-source projects for speculative decoding, but most of them are not well-maintained or not directly compatible with SGLang. We prepared this project because we wish that the open-source community can enjoy a speculative decoding framework that is

Check out our documentation to get started.

## 🚀 Accelerate with SpecBundle [...] This project has also been inspired by many outstanding open-source projects from the LLM community, including EAGLE, BaldEagle, and TensorRT-Model-Optimizer and others. Their contributions and shared knowledge have greatly benefited our work.

## 💡 Special Thanks to Voltage Park

Title: sgl-project/SpecForge: Train speculative decoding models ... - GitHub
URL: https://github.com/sgl-project/SpecForge
Content: ## Repository files navigation

   README
   MIT license

Image 2: logo
Image 3: documentationImage 4: SpecBundleImage 5: DeepWiki

Image 6: github badgeImage 7: slack badgeImage 8: license

## 📍 Overview

 and SpecForge v0.2. Check out our blog at LMSYS.org
   [2025-12] 🔔 Released the roadmap for 2026 Q1.
   [2025-08] 🔔 SpecForge is listed as a flagship project in LMSYS. Congratulations to the SpecForge team!
   [2025-08] 🔥 SpecForge powered the Eagle3 draft model for GPT-OSS. Check out the blog at LMSYS.org
   [2025-07] 🔥 SpecForge is released together with Llama4-Eagle3 checkpoints. Check out our blog at LMSYS.org

## ✨ Acknowledgements

[](

Image 9: acknowledgements [...] | .gitignore | .gitignore | Qwen2.5-VL-7B egale3 train (  support qwen2_5_vl online  delete nohup  add qwen2.5-vl eagle model  add todo  clean dev code  support batch and fix position_ids bug  add eval wandb metrics  fix eval bug  fix eval dataloader bug  add comment  merge main  rename vlm online eagle3 model name  clean code  fix ttt input embeds bug Co-authored-by: Yingyi Huang <[REDACTED]>  fix eval metrics bug  merge qwen-vl draft model to llama3 Co-authored-by: Yingyi Huang <[REDACTED]>  fix qwen vl train shell  add timeout config Co-authored-by: Yingyi Huang <[REDACTED]>  qwenvl draft input without image embedding Co-authored-by: Yingyi Huang <[REDACTED]>  qwenvl draft input without image embedding Co-authored-by: [...] #95)  init  upd with sglang container  remove uv install") | Aug 1, 2025 |
| .github | .github | fixed script of clearing GPU processes (  fixed script of clearing GPU processes  polish")#512)  fixed script of clearing GPU processes  polish") | Mar 24, 2026 |
| assets | assets | added specforge docs (")#199)") | Sep 1, 2025 |
| benchmarks | benchmarks | add offline eval args check and benchmark | Jan 23, 2026 |
| configs | configs | Merge branch 'main' into tool-use | Mar 24, 2026 |
| datasets | datasets | support download allava4v dataset ( polish code polsh code")#409) polish code polsh code") | Jan 12, 2026 |

Title: Update README.md · lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge at 63ebaa6
URL: https://huggingface.co/lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge/commit/63ebaa6585f96b89685adad8fdfa0da53be6a8fd
Content: Hugging Face's logo

# lmsys / SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge like 0 Follow Large Model Systems Organization 889

# Update README.md

|  |  |
 --- |
|  | @@ -24,13 +24,16 @@ This checkpoint was trained by the [\\SpecForge\\]( |
| 24 | You can use this checkpoint with the command below. |
| 25 |  |
| 26 | ```bash |
|  |  |
|  |  |
| 27 | python3 -m sglang.launch\_server \ |
| 28 | --model meta-llama/Llama-3.3-70B-Instruct \ |
| 29 | --speculative-algorithm EAGLE3 \ |
| 30 | --speculative-draft-model-path lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge \ |
| 31 | --speculative-num-steps 3 \ |
| 32 | --speculative-eagle-topk 1 \ |
| 33 | -  --speculative-num-draft-tokens 4 |
|  |  |
| 34 | ``` |
| 35 |  |
| 36 | # Performance | [...] |  |  |
 --- |
|  |  |
| 24 | You can use this checkpoint with the command below. |
| 25 |  |
| 26 | ```bash |
| 27 | + export SGLANG\_ALLOW\_OVERWRITE\_LONGER\_CONTEXT\_LEN=1 |
| 28 | + |
| 29 | python3 -m sglang.launch\_server \ |
| 30 | --model meta-llama/Llama-3.3-70B-Instruct \ |
| 31 | --speculative-algorithm EAGLE3 \ |
| 32 | --speculative-draft-model-path lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge \ |
| 33 | --speculative-num-steps 3 \ |
| 34 | --speculative-eagle-topk 1 \ |
| 35 | +  --speculative-num-draft-tokens 4 \ |
| 36 | +  --tp 4 |
| 37 | ``` |
| 38 |  |
| 39 | # Performance |
```

> AGENT

Excellent finding. Let me get one more piece -- the actual config.json from released EAGLE-3 models to see the concrete layer indices used.

> TOOL

tool_use mcp__tavily__tavily_extract
```json
{
  "query": "config.json aux_hidden_state_layers target_hidden_state_indices layer indices",
  "urls": [
    "https://huggingface.co/yuhuili/EAGLE3-LLaMA3-Instruct-8B/blob/main/config.json",
    "https://huggingface.co/lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge/blob/main/config.json"
  ]
}
```

> TOOL

tool_result mcp__tavily__tavily_extract
```
Detailed Results:

Title: config.json · lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge at main
URL: https://huggingface.co/lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge/blob/main/config.json
Content: undefined
Raw Content: ![Hugging Face's logo](/front/assets/huggingface_logo-noborder.svg)

# [lmsys](/lmsys) / [SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge](/lmsys/SGLang-EAGLE3-Llama-3.3-70B-Instruct-SpecForge) like 0 Follow Large Model Systems Organization 889

![](https://cdn-avatars.huggingface.co/v1/production/uploads/62d35f3ceaf3858ce253ab7a/uZ2jFNAjXfdBo6c6Yojmg.jpeg)
![](https://cdn-avatars.huggingface.co/v1/production/uploads/62d35f3ceaf3858ce253ab7a/uZ2jFNAjXfdBo6c6Yojmg.jpeg)
![frankleeeee's picture](/avatars/9acb77f982d7d369bc8ac22d669152f3.svg)

|  |  |
| --- | --- |
|  | { |
|  | "architectures": [ |
|  | "LlamaForCausalLMEagle3" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "draft\_vocab\_size": 32000, |
|  | "dtype": "bfloat16", |
|  | "eos\_token\_id": [ |
|  | 128001, |
|  | 128008, |
|  | 128009 |
|  | ], |
|  | "head\_dim": 128, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 8192, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 28672, |
|  | "max\_position\_embeddings": 4096, |
|  | "mlp\_bias": false, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 64, |
|  | "num\_hidden\_layers": 1, |
|  | "num\_key\_value\_heads": 8, |
|  | "pad\_token\_id": 0, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": { |
|  | "factor": 8.0, |
|  | "high\_freq\_factor": 4.0, |
|  | "low\_freq\_factor": 1.0, |
|  | "original\_max\_position\_embeddings": 4096, |
|  | "rope\_type": "llama3" |
|  | }, |
|  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "transformers\_version": "4.57.1", |
|  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  |
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "EAGLE-3 config.json \"aux_hidden_state_layers\" site:huggingface.co llama layer indices",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: https://huggingface.co/chankhavu/c2.eagle3-test/re...
URL: https://huggingface.co/chankhavu/c2.eagle3-test/resolve/73214303c16a8520c1dd628e8998d59f1429676a/README.md?download=true
Content: `aux\_hidden\_state\_layers` config field on the draft.
\ \\TensorRT-LLM / others\\: NOT tested. If you port to one of these,
cross-check by running a single forward pass on a fixed input and
comparing the hidden state dump at indices 2/26/48 against vLLM's
dump for the same input. The hidden states should be bit-equivalent
(or near-equivalent up to dtype) at the same indices if the
numbering convention matches.
### Why these specific indices
These three positions follow NVIDIA's gpt-oss-120b long-context Eagle3
recipe (early/mid/late triad). The choice of 2 / 26 / 48 as opposed to
e.g. 0 / 26 / 51 was made to:
\ \\Avoid layer 0\\ (the embedding-adjacent layer), where hidden
states are still mostly raw token embeddings without much
contextualization. [...] `intermediate\_size=8064` (~3x hidden), `head\_dim=128`,
`num\_attention\_heads=32`, `num\_key\_value\_heads=2` (GQA),
`sliding\_window=4096` (band causal), `max\_position\_embeddings=262144`
(matches verifier so vLLM does not clamp serving max\_model\_len),
`vocab\_size=131072`, `draft\_vocab\_size=32000`.
\ \\Aux hidden state layers\\ captured from verifier: layers
\\2 / 26 / 48\\ (~4% / 51% / 94% depth). See "Layer indexing" section
below for the exact mapping and the engine-portability caveat.
Layout follows NVIDIA's gpt-oss-120b long-context Eagle3 reference.
## Layer indexing -- which verifier layers feed the Eagle3 draft
Eagle3 draft heads consume hidden states from THREE specific layers
of the verifier (early / middle / late) and learn to map them into [...] in-flight L=32k iteration.
\ \\SGLang\\: SGLang's NemotronH implementation also uses 0-indexed
contiguous layer counting that matches HF, but as of late 2025 it
does NOT yet support sliding-window attention on Eagle3 drafts
(this draft has `sliding\_window: 4096` in its config). Once SGLang
ships sw support, the layer indices should map cleanly. \\Until
then, prefer vLLM for serving this draft.\\
\ \\HF transformers\\ (raw, no engine): the verifier exposes its
layers as `model.backbone.layers[0..51]`, where `layers[i]` is the
i-th character of `hybrid\_override\_pattern`. This is the canonical
reference. The training pipeline in this fork (SpecForge with the
NemotronH backend patch) reads from these indices via the
`aux\_hidden\_state\_layers` config field on the draft.

Title: stage2 checkpoint from epoch_1_step_8000 · chankhavu/Nemotron-Cascade2-30B-A3B-Eagle3-Long-Context at e9c70c4
URL: https://huggingface.co/chankhavu/c2.eagle3-test/commit/e9c70c41a1125f01e0b2083f7430098d89c8217b
Content: | 113 | +  layers as `model.backbone.layers[0..51]`, where `layers[i]` is the |
| 114 | +  i-th character of `hybrid\_override\_pattern`. This is the canonical |
| 115 | +  reference. The training pipeline in this fork (SpecForge with the |
| 116 | +  NemotronH backend patch) reads from these indices via the |
| 117 | +  `aux\_hidden\_state\_layers` config field on the draft. |
| 118 | + |
| 119 | + \ \\TensorRT-LLM / others\\: NOT tested. If you port to one of these, |
| 120 | +  cross-check by running a single forward pass on a fixed input and |
| 121 | +  comparing the hidden state dump at indices 2/26/48 against vLLM's |
| 122 | +  dump for the same input. The hidden states should be bit-equivalent |
| 123 | +  (or near-equivalent up to dtype) at the same indices if the | [...] | 88 | + Layer 26 is the central one. |
| 89 | + |
| 90 | + ### Engine-portability warning |
| 91 | + |
| 92 | + \\Different inference engines may number layers differently\\ because |
| 93 | + of how they fuse, group, or skip blocks. Before serving this draft on |
| 94 | + a new engine, verify that the engine's "layer i" corresponds to the |
| 95 | + same character in the hybrid pattern as HF transformers does. |
| 96 | + |
| 97 | + \ \\vLLM\\ (0.19+): uses the full 52-layer ModuleList in its |
| 98 | +  NemotronH model implementation, 0-indexed contiguous, \\matches HF |
| 99 | +  transformers\\. The `target\_hidden\_state\_indices: [2, 26, 48]` in |
| 100 | +  this draft's `config.json` is read directly by vLLM's Eagle3 | [...] | 43 | +  below for the exact mapping and the engine-portability caveat. |
| 44 | Layout follows NVIDIA's gpt-oss-120b long-context Eagle3 reference. |
| 45 | + |
| 46 | + ## Layer indexing -- which verifier layers feed the Eagle3 draft |
| 47 | + |
| 48 | + Eagle3 draft heads consume hidden states from THREE specific layers |
| 49 | + of the verifier (early / middle / late) and learn to map them into |
| 50 | + the draft's prediction. The choice of which 3 layers matters: too |
| 51 | + early and the draft has no semantics; too late and it's just |
| 52 | + predicting from the verifier's own next-token distribution. |
| 53 | + |
| 54 | + This draft is trained against verifier layers \\2 / 26 / 48\\ out of |
| 55 | + the verifier's 52 hybrid layers. \\The indexing convention is |

Title: README.md · chankhavu/Nemotron-Cascade2-30B-A3B-Eagle3-Long-Context at e9c70c41a1125f01e0b2083f7430098d89c8217b
URL: https://huggingface.co/chankhavu/c2.eagle3-test/blob/e9c70c41a1125f01e0b2083f7430098d89c8217b/README.md
Content: `target_hidden_state_indices: [2, 26, 48]`
`config.json`
`model.backbone.layers`

SGLang: SGLang's NemotronH implementation also uses 0-indexed
contiguous layer counting that matches HF, but as of late 2025 it
does NOT yet support sliding-window attention on Eagle3 drafts
(this draft has `sliding_window: 4096` in its config). Once SGLang
ships sw support, the layer indices should map cleanly. Until
then, prefer vLLM for serving this draft.

`sliding_window: 4096` [...] `[5, 12, 19, 26, 33, 42]`

### Engine-portability warning

Different inference engines may number layers differently because
of how they fuse, group, or skip blocks. Before serving this draft on
a new engine, verify that the engine's "layer i" corresponds to the
same character in the hybrid pattern as HF transformers does.

vLLM (0.19+): uses the full 52-layer ModuleList in its
NemotronH model implementation, 0-indexed contiguous, matches HF
transformers. The `target_hidden_state_indices: [2, 26, 48]` in
this draft's `config.json` is read directly by vLLM's Eagle3
speculative decoder and passed to the verifier as raw indices into
`model.backbone.layers`. Tested working on vLLM 0.19 with the
in-flight L=32k iteration. [...] `nvidia/Nemotron-Cascade-2-30B-A3B`

## TL;DR

`nvidia/Nemotron-Cascade-2-30B-A3B`
`hybrid_override_pattern`
`hidden_size=2688`
`intermediate_size=8064`
`head_dim=128`
`num_attention_heads=32`
`num_key_value_heads=2`
`sliding_window=4096`
`max_position_embeddings=262144`
`vocab_size=131072`
`draft_vocab_size=32000`

## Layer indexing -- which verifier layers feed the Eagle3 draft

Eagle3 draft heads consume hidden states from THREE specific layers
of the verifier (early / middle / late) and learn to map them into
the draft's prediction. The choice of which 3 layers matters: too
early and the draft has no semantics; too late and it's just
predicting from the verifier's own next-token distribution.

Title: config.json · unsloth/llama-3-8b-Instruct at main
URL: https://huggingface.co/unsloth/llama-3-8b-Instruct/blob/main/config.json
Content: |  |  |
 --- |
|  | { |
|  | "\_name\_or\_path": "unsloth/llama-3-8b-Instruct", |
|  | "architectures": [ |
|  | "LlamaForCausalLM" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "eos\_token\_id": 128009, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 4096, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 14336, |
|  | "max\_position\_embeddings": 8192, |
|  | "mlp\_bias": false, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 32, |
|  | "num\_hidden\_layers": 32, |
|  | "num\_key\_value\_heads": 8, |
|  | "pad\_token\_id": 128255, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": null, |
|  | "rope\_theta": 500000.0, | [...] |  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "torch\_dtype": "bfloat16", |
|  | "transformers\_version": "4.44.2", |
|  | "unsloth\_version": "2024.9", |
|  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  | [...] Hugging Face's logo

# unsloth / llama-3-8b-Instruct like 67 Follow Unsloth AI 19.8k

danielhanchen's picture

Title: config.json · NousResearch/Meta-Llama-3-8B-Instruct at main
URL: https://huggingface.co/NousResearch/Meta-Llama-3-8B-Instruct/blob/main/config.json
Content: |  |  |
 --- |
|  | { |
|  | "architectures": [ |
|  | "LlamaForCausalLM" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "eos\_token\_id": 128009, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 4096, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 14336, |
|  | "max\_position\_embeddings": 8192, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 32, |
|  | "num\_hidden\_layers": 32, |
|  | "num\_key\_value\_heads": 8, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": null, |
|  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "torch\_dtype": "bfloat16", |
|  | "transformers\_version": "4.40.0.dev0", |
|  | "use\_cache": true, | [...] |  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  | [...] Hugging Face's logo

# NousResearch / Meta-Llama-3-8B-Instruct like 105 Follow NousResearch 3.47k

teknium's picture

Title: config.json · NousResearch/Meta-Llama-3-70B-Instruct at 7e1b5532f5f974e32703e6fb284cd0e06563ccbb
URL: https://huggingface.co/NousResearch/Meta-Llama-3-70B-Instruct/blob/7e1b5532f5f974e32703e6fb284cd0e06563ccbb/config.json
Content: |  |  |
 --- |
|  | { |
|  | "architectures": [ |
|  | "LlamaForCausalLM" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "eos\_token\_id": 128001, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 8192, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 28672, |
|  | "max\_position\_embeddings": 8192, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 64, |
|  | "num\_hidden\_layers": 80, |
|  | "num\_key\_value\_heads": 8, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": null, |
|  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "torch\_dtype": "bfloat16", |
|  | "transformers\_version": "4.40.0.dev0", |
|  | "use\_cache": true, | [...] |  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  | [...] Hugging Face's logo

# NousResearch / Meta-Llama-3-70B-Instruct like 21 Follow NousResearch 3.47k

emozilla's picture

Title: config.json · NousResearch/Meta-Llama-3-8B-Instruct at 4c78467aced3bc0088de25626bacf4f690ef4f9d
URL: https://huggingface.co/NousResearch/Meta-Llama-3-8B-Instruct/blob/4c78467aced3bc0088de25626bacf4f690ef4f9d/config.json
Content: |  |  |
 --- |
|  | { |
|  | "architectures": [ |
|  | "LlamaForCausalLM" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "eos\_token\_id": 128001, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 4096, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 14336, |
|  | "max\_position\_embeddings": 8192, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 32, |
|  | "num\_hidden\_layers": 32, |
|  | "num\_key\_value\_heads": 8, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": null, |
|  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "torch\_dtype": "bfloat16", |
|  | "transformers\_version": "4.40.0.dev0", |
|  | "use\_cache": true, | [...] |  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  | [...] Hugging Face's logo

# NousResearch / Meta-Llama-3-8B-Instruct like 105 Follow NousResearch 3.47k

emozilla's picture

Title: resid_post_layer_15/trainer_1/config.json · andyrdt/saes-llama-3.1-8b-instruct at main
URL: https://huggingface.co/andyrdt/saes-llama-3.1-8b-instruct/blame/main/resid_post_layer_15/trainer_1/config.json
Content: | ``` 1be1212                                                                 ``` | ``` 1 ```  ``` 2 ```  ``` 3 ```  ``` 4 ```  ``` 5 ```  ``` 6 ```  ``` 7 ```  ``` 8 ```  ``` 9 ```  ``` 10 ```  ``` 11 ```  ``` 12 ```  ``` 13 ```  ``` 14 ```  ``` 15 ```  ``` 16 ```  ``` 17 ```  ``` 18 ```  ``` 19 ```  ``` 20 ```  ``` 21 ```  ``` 22 ```  ``` 23 ```  ``` 24 ```  ``` 25 ```  ``` 26 ```  ``` 27 ```  ``` 28 ```  ``` 29 ```  ``` 30 ```  ``` 31 ```  ``` 32 ```  ``` 33 ``` | ``` {     "trainer": {         "trainer_class": "BatchTopKTrainer",         "dict_class": "BatchTopKSAE",         "lr": 0.0001,         "steps": 244140,         "auxk_alpha": 0.03125,         "warmup_steps": 1000,         "decay_start": 195312,         "threshold_beta": 0.999,         "threshold_start_step": 1000, [...] 0.999,         "threshold_start_step": 1000,         "top_k_aux": 2048,         "seed": 0,         "activation_dim": 4096,         "dict_size": 131072,         "k": 64,         "device": "cuda",         "layer": 15,         "lm_name": "meta-llama/Llama-3.1-8B-Instruct",         "wandb_name": [REDACTED],         "submodule_name": "resid_post_layer_15"     },     "buffer": {         "d_submodule": 4096,         "io": "out",         "n_ctxs": 244,         "ctx_len": 1024,         "refresh_batch_size": 16,         "out_batch_size": 2048,         "device": "cuda",         "internal_device": "cuda"     } } ``` | [...] |  |  |  |
 ---

Title: config.json · NousResearch/Meta-Llama-3-8B at 2970722000dbfaac732cb8bed6138155785fd52c
URL: https://huggingface.co/NousResearch/Meta-Llama-3-8B/blob/2970722000dbfaac732cb8bed6138155785fd52c/config.json
Content: |  |  |
 --- |
|  | { |
|  | "architectures": [ |
|  | "LlamaForCausalLM" |
|  | ], |
|  | "attention\_bias": false, |
|  | "attention\_dropout": 0.0, |
|  | "bos\_token\_id": 128000, |
|  | "eos\_token\_id": 128001, |
|  | "hidden\_act": "silu", |
|  | "hidden\_size": 4096, |
|  | "initializer\_range": 0.02, |
|  | "intermediate\_size": 14336, |
|  | "max\_position\_embeddings": 8192, |
|  | "model\_type": "llama", |
|  | "num\_attention\_heads": 32, |
|  | "num\_hidden\_layers": 32, |
|  | "num\_key\_value\_heads": 8, |
|  | "pretraining\_tp": 1, |
|  | "rms\_norm\_eps": 1e-05, |
|  | "rope\_scaling": null, |
|  | "rope\_theta": 500000.0, |
|  | "tie\_word\_embeddings": false, |
|  | "torch\_dtype": "bfloat16", |
|  | "transformers\_version": "4.40.0.dev0", |
|  | "use\_cache": true, | [...] |  | "use\_cache": true, |
|  | "vocab\_size": 128256 |
|  | } |
|  |  | [...] Hugging Face's logo

# NousResearch / Meta-Llama-3-8B like 102 Follow NousResearch 3.47k

emozilla's picture

Title: config.json · NousResearch/Meta-Llama-3-70B at main
URL: https://huggingface.co/NousResearch/Meta-Llama-3-70B/blob/main/config.json
Content: historyblamecontributedelete

Safe

 654 Bytes

{
"architectures":[
"LlamaForCausalLM"
],
"attention_bias":false,
"attention_dropout":0.0,
"bos_token_id":128000,
"eos_token_id":128001,
"hidden_act":"silu",
"hidden_size":8192,
"initializer_range":0.02,
"intermediate_size":28672,
"max_position_embeddings":8192,
"model_type":"llama",
"num_attention_heads":64,
"num_hidden_layers":80,
"num_key_value_heads":8,
"pretraining_tp":1,
"rms_norm_eps":1e-05,
"rope_scaling":null,
"rope_theta":500000.0,
"tie_word_embeddings":false,
"torch_dtype":"bfloat16",
"transformers_version":"4.40.0.dev0",
"use_cache":true,
"vocab_size":128256
}

Wrap lines [...] # config.json · NousResearch/Meta-Llama-3-70B at main

Image 1: Hugging Face's logoHugging Face

   Models
   Datasets
   Spaces
   Buckets new
   Docs
   Enterprise
   Pricing
    
   
  

   Log In
   Sign Up

# Image 2

NousResearch

/

Meta-Llama-3-70B

like 11

Follow

Image 3NousResearch 3.44k

Text GenerationTransformersSafetensorsPyTorchEnglishllamafacebookmetallama-3text-generation-inference

License:llama3

Model cardFiles Files and versions xetCommunity

 Deploy

 Use this model

 main

Meta-Llama-3-70B/config.json

Image 4: emozilla's picture

emozilla

Upload folder using huggingface_hub

cff227fverified about 2 years ago

raw

Copy download link

historyblamecontributedelete

Safe

 654 Bytes
```

> AGENT

Now let me check the official EAGLE-3 repository and the SafeAILab code for the exact layer selection logic.

> TOOL

tool_use mcp__tavily__tavily_extract
```json
{
  "query": "aux_hidden_state_layers layer selection low middle high feature layer indices eagle3",
  "urls": [
    "https://github.com/SafeAILab/EAGLE/blob/main/eagle/model/configs/eagle3.py",
    "https://github.com/sgl-project/SpecForge/blob/main/configs/eagle3"
  ]
}
```

> TOOL

tool_result mcp__tavily__tavily_extract
```
Detailed Results:
```

> TOOL

tool_use mcp__tavily__tavily_search
```json
{
  "max_results": 10,
  "query": "SafeAILab EAGLE github eagle3 \"low_layer\" OR \"mid_layer\" OR \"high_layer\" OR \"aux_hidden\" layer selection code implementation",
  "search_depth": "advanced"
}
```

> TOOL

tool_result mcp__tavily__tavily_search
```
Detailed Results:

Title: SafeAILab/EAGLE: Official Implementation of EAGLE-1 ... - GitHub
URL: https://github.com/SafeAILab/EAGLE
Content: EAGLE-2 is: 
       4x faster than vanilla decoding (13B).
       1.4x faster than EAGLE-1 (13B).

EAGLE-3 removes the feature prediction constraint in EAGLE and simulates this process during training using training-time testing. Considering that top-layer features are limited to next-token prediction, EAGLE-3 replaces them with a fusion of low-, mid-, and high-level semantic features. EAGLE-3 further improves generation speed while ensuring lossless performance.

   EAGLE-3 is: 
       5.6 faster than vanilla decoding (13B).
       1.8x faster than EAGLE-1 (13B).

Image 7: demogif

_Inference is conducted on 2x RTX 3090 GPUs at fp16 precision using the Vicuna 13B model._

## Support

. [...] # GitHub - SafeAILab/EAGLE: Official Implementation of EAGLE-1 (ICML'24), EAGLE-2 (EMNLP'24), and EAGLE-3 (NeurIPS'25). · GitHub

Skip to content
## Navigation Menu

Toggle navigation

 | Paper (EAGLE-2) | Paper (EAGLE-3) | Blog |

Image 2: VersionImage 3: LicenseImage 4: MaintenanceImage 5: Contributions welcome

Image 6: benchmark

EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency) is a new baseline for fast decoding of Large Language Models (LLMs) with provable performance maintenance. This approach involves extrapolating the second-top-layer contextual feature vectors of LLMs, enabling a significant boost in generation efficiency. [...] EAGLE is: 
       certified by the third-party evaluation as the fastest speculative method so far.
       achieving 2x speedup on gpt-fast.
       3x faster than vanilla decoding (13B).
       2x faster than Lookahead (13B).
       1.6x faster than Medusa (13B).
       provably maintaining the consistency with vanilla decoding in the distribution of generated texts.
       trainable (within 1-2 days) and testable on 8x RTX 3090 GPUs. So even the GPU poor can afford it.
       combinable with other parallelled techniques such as vLLM, DeepSpeed, Mamba, FlashAttention, quantization, and hardware optimization.

EAGLE-2 uses the confidence scores from the draft model to approximate acceptance rates, dynamically adjusting the draft tree structure, which further enhances performance.

Title: [PDF] EAGLE-3: Scaling up Inference Acceleration of Large Language ...
URL: https://openreview.net/pdf?id=4exx1hUffq
Content: This paper introduces EAGLE-3, an enhanced version of EAGLE that achieves a significant speedup: • A training-time test architecture for the draft model: We remove the feature prediction constraint and directly predict tokens while simulating multi-step generation during training.
This direct token prediction provides complete flexibility in the draft model’s input. Instead of reusing only the top-layer features, we integrate and leverage low-, mid-, and high-level features from the target model, capturing rich semantic information from different layers. [...] There are several key differences between HASS  and EAGLE-3. First, HASS drafts using only top-layer features, whereas EAGLE-3 integrates low-, mid-, and high-level features. Second, HASS retains the token loss ltoken, while EAGLE-3 removes it to improve model capacity. Third, unlike HASS, EAGLE-3 exhibits a clear scaling law trend. Finally, EAGLE-3 significantly outperforms HASS, as demonstrated in Figure 1 and Table 1. [...] 9 6 Conclusion In this paper, we introduce EAGLE-3. Building upon EAGLE, EAGLE-3 incorporates two key improvements. First, it removes the feature prediction constraint, instead directly predicting draft tokens through a Training-time test. Second, it replaces the use of the target model’s top-layer features with a fusion of the target model’s lower, middle, and upper-layer features to obtain richer information. With these improvements, EAGLE-3 continues to benefit from the augmentation of training data, achieving a maximum speedup of 6.5x.

Title: How to train eagle3 with the new loss? · Issue #194 · SafeAILab/EAGLE · GitHub
URL: https://github.com/SafeAILab/EAGLE/issues/194
Content: ### Labels

### Type

### Projects

### Milestone

### Relationships

### Development

## Issue actions

## Footer

### Footer navigation [...] ## Navigation Menu

# Search code, repositories, users, issues, pull requests...

# Provide feedback

We read every piece of feedback, and take your input very seriously.

# Saved searches

## Use saved searches to filter your results more quickly

To see all available qualifiers, see our documentation.

# How to train eagle3 with the new loss? #194

@carlbunny

## Description

@carlbunny

Hello Eagle team,

I am checking the new EAGLE3 PR) and can't locate the loss function change. Not sure how to train the model using EAGLE3 that 1) removes the feature prediction 2) compare multiple output tokens.  
The loss function in eagle/train/main are still the plss + vloss of the next token.

Thank you!

## Metadata

## Metadata

### Assignees

### Labels

### Type

### Projects

### Milestone

Title: Summary: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test - Wentao's Blog
URL: https://wentao.site/eagle_v3_summary/
Content: Posts Categories About

Home

PostsCategoriesAbout

## Contents

# Summary: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

yewentao avataryewentao  included in  category Paper\_summary

365 words   2 minutes

Contents

## 0. Materials

 Paper
 Github

## 1. What is the paper about?

 Proposes EAGLE‑3, an inference‑acceleration method that extends speculative decoding for LLM decoding.
 Replaces feature‑vector prediction with direct token prediction and introduces a training‑time test (TTT) loop to train the draft model on its own noisy outputs.
 Fuses low, mid, and high‑level hidden states from the target model, instead of relying solely on top‑layer features.

## 2. What is new compared to prior work? [...] | Home

Summary: DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model Summary: MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models [...] Speed‑up & acceptance length measured against vanilla decoding, spec‑sampling, PLD, Hydra, Medusa, HASS, EAGLE, and EAGLE‑2. EAGLE‑3 tops all with 3‑6.5 × gains.
 Throughput +38 % at batch 64 in SGLang on H100; EAGLE‑2 regresses beyond batch 24.
 Throughput still ≥ 1.4 × at batch 24 in vLLM on RTX 3090, while EAGLE‑2 turns negative earlier.
 Acceptance rates and speed‑ups grow nearly linearly with training‑data scale (1 ×→8 × ShareGPT), validating scaling law.

## 4. What are the shortcomings/limitations of this paper?

Title: eagle - vLLM
URL: https://docs.vllm.ai/en/latest/api/vllm/v1/spec_decode/eagle/
Content: self.kv_cache_gid: int = -1 self. kv_cache_gid: int = - 1 self.eagle3_use_aux_hidden_state: bool = ( self. eagle3_use_aux_hidden_state: bool =( self._get_eagle3_use_aux_hidden_state_from_config() self. _get_eagle3_use_aux_hidden_state_from_config() ) )   self.compilation_config = self.vllm_config.compilation_config self. compilation_config = self. vllm_config. compilation_config   # Cudagraph dispatcher for PIECEWISE-only dispatching in eagle. # Cudagraph dispatcher for PIECEWISE-only dispatching in eagle. # Keys are initialized later via initialize_cudagraph_keys() called from # Keys are initialized later via initialize_cudagraph_keys() called from # gpu_model_runner._check_and_update_cudagraph_mode after # gpu_model_runner._check_and_update_cudagraph_mode after # [...] sampling_metadata: SamplingMetadata, sampling_metadata: SamplingMetadata, mm_embed_inputs: tuple[list[torch.Tensor], torch.Tensor] | None = None, mm_embed_inputs: tuple[list[torch. Tensor], torch. Tensor] | None = None, num_rejected_tokens_gpu: torch.Tensor | None = None, num_rejected_tokens_gpu: torch. Tensor | None = None, slot_mappings: dict[str, torch.Tensor] slot_mappings: dict[str, torch. Tensor] | list[dict[str, torch.Tensor]] | list[dict[str, torch. Tensor]] | None = None, | None = None, ) -> torch.Tensor: ) -> torch. Tensor: batch_size = common_attn_metadata.batch_size() batch_size = common_attn_metadata. batch_size()   if self.method in ("eagle3", "dflash"): if self. method in("eagle3", "dflash"): assert isinstance( assert isinstance( self.model, self. model, ( ( [...] positions = positions self.positions[:num_tokens] = positions self. positions[: num_tokens] = positions   def _get_slot_mapping( def  _get_slot_mapping( self, self, num_tokens: int, num_tokens: int, slot_mapping: torch.Tensor | None = None, slot_mapping: torch. Tensor | None = None, ) -> dict[str, torch.Tensor]: ) -> dict[str, torch. Tensor]: """Return slot_mapping dict for EAGLE layers.  """Return slot_mapping dict for EAGLE layers.   If slot_mapping is provided, copies it into the buffer first.  If slot_mapping is provided, copies it into the buffer first.  """  """ if slot_mapping is not None: if slot_mapping is not None: num_actual = slot_mapping.shape num_actual = slot_mapping. shape self._slot_mapping_buffer[:num_actual].copy_(slot_mapping) self. _slot_mapping_buffer[: num_actual].

Title: [Usage]: Qwen + Eagle3 supported in PyTorch backend yet? · Issue #7038 · NVIDIA/TensorRT-LLM · GitHub
URL: https://github.com/NVIDIA/TensorRT-LLM/issues/7038
Content: "eagle_module.layers.0.mlp.gate_proj.weight_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.mlp.up_proj.input_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.mlp.up_proj.weight": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.mlp.up_proj.weight_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.post_attention_layernorm.weight": "model-00008-of-00008.safetensors",
"eagle_module.layers.0.self_attn.k_proj.bias": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.k_proj.input_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.k_proj.weight": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.k_proj.weight_scale": "model-00007-of-00008.safetensors", [...] "eagle_module.layers.0.self_attn.o_proj.input_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.o_proj.weight": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.o_proj.weight_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.q_proj.bias": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.q_proj.input_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.q_proj.weight": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.q_proj.weight_scale": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.v_proj.bias": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.v_proj.input_scale": "model-00007-of-00008.safetensors", [...] "eagle_module.layers.0.self_attn.v_proj.weight": "model-00007-of-00008.safetensors",
"eagle_module.layers.0.self_attn.v_proj.weight_scale": "model-00007-of-00008.safetensors",
"eagle_module.norm.weight": "model-00008-of-00008.safetensors",`

Title: NeurIPS Poster EAGLE-3: Scaling up Inference Acceleration of ...
URL: https://neurips.cc/virtual/2025/poster/119930
Content: reliance on top-layer features with multi-layer feature fusion via a technique named training-time test. These improvements significantly enhance performance and enable the draft model to fully benefit from scaling up training data. Our experiments include both chat models and reasoning models, evaluated on five tasks. The results show that EAGLE-3 achieves a speedup ratio up to 6.5x, with about 1.4x improvement over EAGLE-2. In the SGLang framework, EAGLE- 3 achieves a 1.38x throughput improvement at a batch size of 64. [...] The sequential nature of modern LLMs makes them expensive and slow, and speculative sam- pling has proven to be an effective solution to this problem. Methods like EAGLE perform autoregression at the feature level, reusing top- layer features from the target model to achieve better results than vanilla speculative sampling. A growing trend in the LLM community is scaling up training data to improve model intelligence without increasing inference costs. However, we observe that scaling up data provides limited improvements for EAGLE. We identify that this limitation arises from EAGLE’s feature prediction constraints. In this paper, we introduce EAGLE-3, which abandons feature prediction in favor of direct token prediction and replaces reliance on top-layer features with multi-layer feature [...] Skip to yearly menu bar

## Main Navigation

conference_logo

 NeurIPS 
  + Code of Ethics  

  + Code of Conduct  

  + Create Profile  

  + Journal To Conference Track  

  + Diversity & Inclusion  

  + Proceedings  

  + Future Meetings  

  + Press  

  + Exhibitor Information  

  + Contact NeurIPS  

  + Help/FAQ  

  + Privacy Policy  

  + Downloads
 My Stuff

 Login

Poster  Wed, Dec 3, 2025 • 11:00 AM – 2:00 PM PST

# EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

Yuhui Li · Fangyun Wei · Chao Zhang · Hongyang Zhang

Project Page    [Slides]     [Poster]     [OpenReview]

### Abstract

Title: [PDF] EAGLE-2: Faster Inference of Language Models with Dynamic Draft ...
URL: https://aclanthology.org/anthology-files/pdf/emnlp/2024.emnlp-main.422.pdf
Content: top 2 nodes with the highest value from the current layer (orange blocks) as inputs to the draft model and connect the generated tokens (green blocks) to the draft tree. In the rerank phase, we select the top 8 nodes with the highest value from all nodes (blue blocks), flatten them into a 1-dimensional sequence to form the final draft. We then construct the attention mask according to the tree structure, ensuring each token can only see its ancestor nodes. [...] 2.2 EAGLE EAGLE (Li et al., 2024b) is an improvement over speculative sampling. At the submission of this work, EAGLE ranks first in the Spec-Bench (Xia et al., 2024), a comprehensive benchmark designed for assessing speculative decoding methods across diverse scenarios. [...] Neeraj Varshney, Agneet Chatterjee, Mihir Parmar, and Chitta Baral. 2023. Accelerating llm inference by enabling intermediate layer decoding. arXiv preprint arXiv:2310.18581.
Heming Xia, Zhe Yang, Qingxiu Dong, Peiyi Wang, Yongqi Li, Tao Ge, Tianyu Liu, Wenjie Li, and Zhi-fang Sui. 2024. Unlocking efficiency in large lan-guage model inference: A comprehensive survey of speculative decoding. Preprint, arXiv:2401.07851.
Nan Yang, Tao Ge, Liang Wang, Binxing Jiao, Daxin Jiang, Linjun Yang, Rangan Majumder, and Furu Wei. 2023a. Inference with reference: Lossless ac-celeration of large language models. arXiv preprint arXiv:2304.04487.
Seongjun Yang, Gibbeum Lee, Jaewoong Cho, Dim-itris Papailiopoulos, and Kangwook Lee. 2023b.

Title: Train - Speculators Docs
URL: https://docs.vllm.ai/projects/speculators/en/latest/examples/data_generation_and_training/
Content: eagle 
        + speculators.convert.eagle.eagle3\_converter
        + speculators.convert.eagle.eagle3\_legacy\_model
        + speculators.convert.eagle.eagle\_converter
        + speculators.convert.eagle.eagle\_legacy\_model
        + speculators.convert.eagle.utils
    - data generation

         data generation 
       speculators.data\_generation.config\_generator
       speculators.data\_generation.configs
       speculators.data\_generation.custom\_worker
       speculators.data\_generation.logging\_utils
       speculators.data\_generation.preprocessing
       speculators.data\_generation.vllm\_client
       speculators.data\_generation.vllm\_hidden\_states\_generator
    - models [...] models 
       speculators.models.attention
       speculators.models.base\_components
       dflash

           dflash 
        + speculators.models.dflash.attention
        + speculators.models.dflash.config
        + speculators.models.dflash.core
        + speculators.models.dflash.metrics
        + speculators.models.dflash.model\_definitions
        + speculators.models.dflash.utils
       eagle3

           eagle3 
        + speculators.models.eagle3.attention
        + speculators.models.eagle3.config
        + speculators.models.eagle3.core
        + speculators.models.eagle3.data
        + speculators.models.eagle3.model\_definitions
    - proposals

         proposals 
       speculators.proposals.base
       speculators.proposals.greedy
    - train [...] ## Vocab Mapping

Build `d2t` and `t2d` files from the token frequency distribution file. `scripts/build_vocab_mapping.py` is the main entrypoint for this step.

Once completed, the following files will be generated from this step on disk:

1. `d2t.npy`
2. `t2d.npy`

## Training

Train an Eagle3 draft model or `speculator`. Currently, training is supported for:

1. Single-Layer and Multi-Layer Draft Models for Non-MoE models
2. Single-Layer and Multi-Layer Draft Models of certain Non-Vision MoEs

For a full list of models with support, see: 

`scripts/train.py` provides the main entry point for training Eagle3 models with support for single and multi GPU training using FSDP.

# Examples

Title: [Bug] Qwen3-VL-30B-A3B (MoE) fails to start with speculative decoding: missing get_embed_and_head() / set_eagle3_layers_to_capture() in Qwen3VLMoeForConditionalGeneration (sglang v0.5.7) · Issue #17935 · sgl-project/sglang · GitHub
URL: https://github.com/sgl-project/sglang/issues/17935
Content: Draft model: `SpecForge_qwen3-vl-model_eagle3`

`SpecForge_qwen3-vl-model_eagle3`

Two platforms reproduced:

dtype: `bfloat16`

`bfloat16`

Context length: `4096`

`4096`

Note: `export SGLANG_DISABLE_CUDNN_CHECK=1` on Jetson

`export SGLANG_DISABLE_CUDNN_CHECK=1`

## Problem Summary

When enabling speculative decoding with Qwen3-VL-30B-A3B (MoE), the server fails to start due to missing methods on the target model wrapper class `Qwen3VLMoeForConditionalGeneration`:

`Qwen3VLMoeForConditionalGeneration`

With `--speculative-algorithm EAGLE`, SGLang crashes in `EAGLEWorker` because the target model has no `get_embed_and_head()`.

`--speculative-algorithm EAGLE`
`EAGLEWorker`
`get_embed_and_head()` [...] Draft model: `SpecForge_qwen3-vl-model_eagle3`

`SpecForge_qwen3-vl-model_eagle3`

Two platforms reproduced:

dtype: `bfloat16`

`bfloat16`

Context length: `4096`

`4096`

Note: `export SGLANG_DISABLE_CUDNN_CHECK=1` on Jetson

`export SGLANG_DISABLE_CUDNN_CHECK=1`

## Metadata

## Metadata

### Assignees

### Labels

### Type

### Projects

### Milestone

### Relationships

### Development

## Issue actions

## Footer

### Footer navigation [...] ### B) x86\_64 (sglang 0.5.7), EAGLE

Command:

Error (same user_4813494d cause):

`AttributeError: 'Qwen3VLMoeForConditionalGeneration' object has no attribute 'get_embed_and_head'`

### C) x86\_64 (sglang 0.5.7), EAGLE3

Command:

Error (key part):

`AttributeError: 'Qwen3VLMoeForConditionalGeneration' object has no attribute 'set_eagle3_layers_to_capture'
File .../sglang/srt/model_executor/cuda_graph_runner.py", line 353, in __init__
self.model_runner.model.set_eagle3_layers_to_capture()`

## Expected Behavior

Server should start successfully with speculative decoding enabled (EAGLE / EAGLE3), or at least provide a clear message that Qwen3-VL MoE is not supported by EAGLE/EAGLE3 yet.

## Additional Context / Suspected Cause
```

> AGENT

Now let me also check the local project's eagle config for the actual layer indices used.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/eagle -name \"config.json\" -type f 2>/dev/null | head -5",
  "description": "Find EAGLE config files in the project"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/sglang_model/config.json
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/eagle -name \"*.py\" -type f 2>/dev/null | head -20",
  "description": "Find Python files in eagle directory"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/collect_data.py
/user_4813494d/openbmb/eagle/train.py
/user_4813494d/openbmb/eagle/build_prompts.py
/user_4813494d/openbmb/eagle/convert_to_sglang.py
/user_4813494d/openbmb/eagle/bench_draft_kernel.py
/user_4813494d/openbmb/eagle/bench_real_fp4.py
/user_4813494d/openbmb/eagle/eval_ood_accept.py
/user_4813494d/openbmb/eagle/test_offline_pred.py
/user_4813494d/openbmb/eagle/verify_sglang_draft.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/sglang_model/config.json"
}
```

> TOOL

tool_result Read
```
1	{
2	  "architectures": [
3	    "LlamaForCausalLMEagle3"
4	  ],
5	  "model_type": "llama",
6	  "hidden_size": 4096,
7	  "intermediate_size": 16384,
8	  "num_hidden_layers": 1,
9	  "num_attention_heads": 32,
10	  "num_key_value_heads": 2,
11	  "head_dim": 128,
12	  "hidden_act": "silu",
13	  "max_position_embeddings": 524288,
14	  "rms_norm_eps": 1e-06,
15	  "vocab_size": 73448,
16	  "draft_vocab_size": 32000,
17	  "target_hidden_size": 4096,
18	  "scale_emb": 12,
19	  "tie_word_embeddings": false,
20	  "torch_dtype": "bfloat16",
21	  "eagle_config": {
22	    "use_aux_hidden_state": true,
23	    "eagle_aux_hidden_state_layer_ids": [
24	      1,
25	      10,
26	      22
27	    ]
28	  }
29	}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/train.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train EAGLE-3 draft model for MiniCPM-SALA speculative decoding.
4	
5	Architecture: fc(12288→4096) + 1 decoder layer (TTT 7-step) + norm + lm_head
6	Loss: plogp = -sum(target_p * log(draft_p)), weighted by 0.8^step
7	
8	Data: .pt files with {token_ids, aux_hidden, top_logit_values, top_logit_indices}
9	      aux_hidden = cat(layer1, layer10, layer22) of shape (seq_len, 12288)
10	
11	Run from repo user_4813494d:
12	    python3 eagle/train.py
13	"""
14	
15	import math
16	import os
17	import random
18	import time
19	from pathlib import Path
20	
21	import torch
22	import torch.nn as nn
23	import torch.nn.functional as F
24	from safetensors import safe_open
25	from tqdm import tqdm
26	
27	# ── Config ──────────────────────────────────────────────────────────────
28	DATA_DIR = Path("eagle/data/train")
29	VAL_OOD_DIR = Path("eagle/data/val_ood")  # bench speed responses — OOD distribution
30	OUTPUT_DIR = Path("eagle/weights")
31	MODEL_PATH = [REDACTED]
32	BF16_MODEL_PATH = [REDACTED]  # BF16 weights for MLP init
33	RESUME_CKPT = None  # 从头训（v2 数据分布变大，init_mlp_from_target 做 warm-start）
34	
35	# FP4 STE-QAT: train with FP4-quantized forward pass so weights are FP4-native
36	# at the end of training (no post-training quantization needed).
37	FP4_QAT = True
38	FP4_GROUP_SIZE = 16  # NVFP4 group size (16 weights share one FP8 scale)
39	TARGET_INIT_LAYER = 16  # target model layer to copy MLP/o_proj weights from
40	
41	HIDDEN_SIZE = 4096
42	AUX_DIM = HIDDEN_SIZE * 3  # 12288
43	VOCAB_SIZE = 73448
44	DRAFT_VOCAB_SIZE = 32000
45	SCALE_EMB = 12
46	SCALE_WIDTH = HIDDEN_SIZE / 256  # 16
47	NUM_HEADS = 32
48	NUM_KV_HEADS = 2
49	HEAD_DIM = 128
50	INTERMEDIATE_SIZE = 16384
51	RMS_NORM_EPS = 1e-6
52	
53	TTT_STEPS = 3  # 3-step TTT for regularization; spec_steps=1 推理只用 step 0, 多步为 robustness
54	LOSS_DECAY = 0.8
55	SEQ_LEN = 2048
56	BATCH_SIZE = 8
57	GRAD_ACCUM = 1  # effective batch = 8
58	LR = 3e-4
59	WARMUP_STEPS = 1500
60	WEIGHT_DECAY = 0.01
61	BETAS = (0.9, 0.95)
62	MAX_GRAD_NORM = 1.0
63	EPOCHS = 10
64	EVAL_EVERY_EPOCH = 1
65	EARLY_STOP_PATIENCE = 3  # stop training if OOD acc does not improve for N epochs
66	GRAD_CHECKPOINT = False  # 关：有充足显存（BS=4 peak 28.6 GB / 85 GB），换 bwd -35%
67	SEED = 42
68	MIN_TOKENS = 128  # skip files shorter than this
69	
70	DEVICE = "cuda"
71	DTYPE = torch.bfloat16
72	
73	# ── FP4 STE-QAT primitives ───────────────────────────────────────────────
74	# FP4 E2M1 positive values and their rounding boundaries
75	_FP4_POS = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0])
76	_FP4_BOUNDS = torch.tensor([0.25, 0.75, 1.25, 1.75, 2.5, 3.5, 5.0])
77	
78	
79	def _fp4_round(x: torch.Tensor) -> torch.Tensor:
80	    """Round each element to the nearest FP4 E2M1 representable value.
81	    Input: any float tensor (already in [-6, 6] range preferred).
82	    Output: same dtype, values in {0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}.
83	    """
84	    pos = _FP4_POS.to(device=x.device, dtype=x.dtype)
85	    bounds = _FP4_BOUNDS.to(device=x.device, dtype=x.dtype)
86	    sign = x.sign()
87	    idx = torch.bucketize(x.abs().clamp(max=6.0), bounds)
88	    return sign * pos[idx]
89	
90	
91	class _FP4QuantSTE(torch.autograd.Function):
92	    """Fake-quantize weight to FP4 E2M1 in forward; straight-through in backward.
93	
94	    Per-group-of-16 scaling: scale = max(|w_group|) / 6.0
95	    This matches NVFP4 group_size=16 used by the Marlin kernel.
96	    """
97	    @staticmethod
98	    def forward(ctx, weight: torch.Tensor) -> torch.Tensor:
99	        N, K = weight.shape
100	        w = weight.float()
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/collect_data.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""EAGLE-3 collect: read prebuilt prompts → send to server → move .pt files.
3	
4	Prereq:
5	  1. python3 eagle/build_prompts.py  (generates /tmp/eagle3_prompts.jsonl)
6	  2. Start sglang server with EAGLE3 collection env:
7	       EAGLE3_COLLECT_DIR=/tmp/eagle3_collect \
8	       EAGLE3_MAX_TOKENS=2048 \
9	       EAGLE3_TOP_K=128 \
10	       SGLANG_MARLIN_DECODE_THRESHOLD=48 \
11	       python3 -m sglang.launch_server \
12	           --model-path /user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4 \
13	           --trust-remote-code --port 30000 \
14	           --mem-fraction-static 0.75 --max-running-requests 64 \
15	           --attention-backend minicpm_flashinfer \
16	           --quantization modelopt_fp4 --dense-as-sparse \
17	           --skip-server-warmup
18	
19	Run (this script, after server is up):
20	  python3 eagle/collect_data.py          # train
21	  python3 eagle/collect_data.py --val-ood # val_ood (needs EAGLE3_MAX_TOKENS=0 server)
22	"""
23	import argparse
24	import asyncio
25	import json
26	import shutil
27	import sys
28	import time
29	from collections import defaultdict
30	from pathlib import Path
31	
32	import aiohttp
33	from tqdm import tqdm
34	
35	REPO_user_4813494d = Path(__file__).resolve().parent.parent
36	PROMPTS_PATH = Path("/tmp/eagle3_prompts.jsonl")
37	COLLECT_DIR = Path("/tmp/eagle3_collect")
38	OUT_TRAIN = REPO_user_4813494d / "eagle" / "data" / "train"
39	OUT_VAL = REPO_user_4813494d / "eagle" / "data" / "val"
40	OUT_VAL_OOD = REPO_user_4813494d / "eagle" / "data" / "val_ood"
41	API_BASE = "http://127.0.0.1:30000"
42	CONCURRENCY = 32
43	VAL_FRACTION = 0.02  # 2% of train samples → val (stratified)
44	# val_ood only — "用 bench 评 bench" 已明示允许（比赛提交也是测 bench）。严禁作为 train 源。
45	BENCH_DATA = REPO_user_4813494d / "bench" / "latest_data" / "speed_bench_cunlimited.jsonl"
46	VAL_OOD_COLLECT_DIR = Path("/tmp/eagle3_val_collect")
47	
48	
49	async def check_server_ready(session):
50	    try:
51	        async with session.get(f"{API_BASE}/v1/models") as resp:
52	            return resp.status == 200
53	    except Exception:
54	        return False
55	
56	
57	async def collect(prompts, collect_dir, output_dir, concurrency=CONCURRENCY):
58	    """Send each prompt as max_tokens=1, hook saves .pt in collect_dir, move to output_dir."""
59	    output_dir.mkdir(parents=True, exist_ok=True)
60	    collect_dir.mkdir(parents=True, exist_ok=True)
61	
62	    # Clean stale collect files only (keep output if resuming)
63	    for f in collect_dir.glob("*.pt"):
64	        f.unlink()
65	    existing = sorted(output_dir.glob("*.pt"))
66	    start_idx = len(existing)
67	    if start_idx > 0:
68	        print(f"Resuming from index {start_idx} ({start_idx} already in {output_dir})")
69	        prompts = prompts[start_idx:]
70	
71	    success = 0
72	    fail = 0
73	    async with aiohttp.ClientSession() as session:
74	        if not await check_server_ready(session):
75	            print(f"[ERROR] Server not ready at {API_BASE}. Start sglang server first.")
76	            sys.exit(1)
77	
78	        sem = asyncio.Semaphore(concurrency)
79	        batch_size = concurrency
80	        pbar = tqdm(total=len(prompts), desc=f"collect → {output_dir.name}", unit="seq")
```

> AGENT

Now let me look at the docs in this project for more details about their specific layer selection rationale.

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding
2	
3	## 1. 当前状态
4	
5	- **生产配置**：`spec_steps=2, topk=1, dtn=3`（chain verify）
6	- **Draft model**：`eagle/sglang_model/`（v2，415 MB safetensors），纯 Marlin W4A16 推理
7	- **Target model**：`/user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4`
8	- **相关文档**：
9	  - `spec v2 + overlap` 适配记录 → [spec-v2.md](spec-v2.md)
10	  - 训练改进细节 → [training-v2.md](training-v2.md)
11	  - 下一代候选 → [dflash.md](dflash.md)
12	
13	## 2. 架构
14	
15	```
16	Eagle3Model (~437M trainable):
17	  fc:        Linear(12288 → 4096)           # 融合 3 层 aux hidden
18	  midlayer:  Eagle3DecoderLayer             # 完整 decoder layer
19	    self_attn: Eagle3Attention (GQA 32h/2kv) # Q/K input = cat(normed_embed, normed_hidden)
20	    mlp: SwiGLU (4096 → 16384 → 4096)
21	  embed_tokens: Embedding(73448, 4096) [FROZEN]
22	  lm_head:      Linear(4096 → 32000)        # 32K draft 词表 (覆盖率 99.23%)
23	```
24	
25	- **Aux layers**：[1, 10, 22]，linear probe 验证最优（CE=6.51 vs 次优 6.57）
26	- **词表**：32K 子集，`d2t` 映射 draft→full vocab
27	- **Draft 推理**：~0.50 ms/step（Marlin FP4）
28	
29	## 3. 训练关键点
30	
31	### Shifted Alignment（关键对齐）
32	
33	推理时输入 `(x_{t+1}, aux[t])` → 预测 `x_{t+2}`。训练必须匹配：
34	
35	```python
36	input_ids   = token_ids[:, 1:]       # x_1..x_{S-1}
37	aux_shifted = aux_hidden[:, :-1, :]  # aux_0..aux_{S-2}
38	target      = target_logits[:, 1:]
39	```
40	
41	修复前 OOD accept rate = 8.2%，修复后 epoch 1 即达 35.5%。
42	
43	### RoPE 对齐
44	
45	训练原本无 RoPE 但推理有 → 离线 eval 虚高。已修：`_build_rope_cache(theta=10000.0)` + `apply_rotary_pos_emb`。
46	
47	### FP4_QAT (STE fake-quantize)
48	
49	训练时 forward 用 BF16，每步 `optimizer.step()` 后 project 到 FP4 grid。MLP/fc 从 NVFP4 目标模型 dequantized 权重初始化。推理时直接用 Marlin W4A16。
50	
51	## 4. SGLang 适配（4 个关键修复）
52	
53	提交 `8bc05a3`：
54	
55	1. **GLA state rollback**：用 `mambaish_config`（含 `minicpm_hybrid_config`）统一判断
56	2. **Sparse k1/k2 slot 分配**：新增 `_alloc_sparse_for_new_positions()`，verify 后手动分配
57	3. **Draft model 配置隔离**：量化置 None + attention backend 从 minicpm_flashinfer → flashinfer
58	4. **KV cache slot 释放时序**：verify() 开头释放 draft slots，避免孤儿
59	
60	## 5. Fused NVFP4 Scale Loader 修复
61	
62	`QKVParallelLinear.weight_loader_v2()` 加载 fused per-tensor scale 只写 `shard_id=0`，剩余 slot 为 `torch.empty` 垃圾 → `max()` 吸收 → scale 损坏 → qkv 输出 Inf → 全链 NaN → accept_len ≈ 1.03。
63	
64	**修复**：`load_fused_per_tensor_weight()` 标量广播到所有 shard。6 种配置 (flashinfer/triton × CUDA graph on/off × 新旧 ckpt) 全部零 NaN。
65	
66	## 6. Fused GLA Kernel
67	
68	**原始路径**：24 层 GLA × dtn 步 = 72 次 kernel launch。  
69	**优化**：24 层 × 1 次 launch，处理 T=dtn 并导出全部中间 state → **7.63× 加速**（microbench, 5.51 → 0.72 ms），cos_sim = 1.0。
70	
71	### intermediate_ssm 直写
72	
73	原 `ht_buf(N*H,T,K,V) → permute → intermediate_ssm.copy`（1848 call × 21us = 39.5 ms）。Triton kernel 直写 `intermediate_ssm[cache_idx,:B,:dtn]` → 0.4 ms（-99%）。cos = 1.000000, max_abs = 4.5e-8。
74	
75	## 7. GLA Tree Verify — tree-aware dtn5 verify ✅ 已落地
76	
77	### 背景
78	
79	GLA 递推 `h_t = exp(-γ)*h_{t-1} + k_t*v_t^T`。topk>1 时 flat verify `[user_4813494d, c1, c2]` 导致 c2 继承 c1 state（应从 user_4813494d 分叉）。
80	
81	### Plan A（per-branch 扁平）❌ 回滚
82	
83	重排 `[user_4813494d, c1, c2]` → `[user_4813494d, c1, user_4813494d, c2]` 做 2 个 varlen seq。离线数值正确（cos 0.996→0.9999999）。但 FP32 4D `index_select` 引入 205 ms/cycle 热点，吞掉全部收益，净 ROI 负。
84	
85	### tree-aware dtn5 verify（commit `1a16b26`）✅
86	
87	`hybrid_linear_attn_backend.py` + `eagle_worker.py` + `eagle_info.py` 联合改造，支持 tree 结构的 sibling 隔离。已落地稳定，`tests/test_simple_gla_tree_verify.py` 回归通过。
88	
89	## 8. Break-even 分析
90	
91	| 配置 | draft (ms) | verify (ms) | break-even accept_len |
92	|---|---|---|---|
93	| Medusa K=1 (truncated) | 0.39 | 6.5 | — (baseline) |
94	| EAGLE-3 s=2, k=1, dtn=3 | ~1.0 | ~5.5 | **~1.15** |
95	
96	当前 accept_len >> break-even，EAGLE-3 稳赢。
97	
98	## 9. spec_steps>1 链式 vs 树形（已决策）
99	
100	**spec_steps>1 chain 已终结**：draft forward 线性成本 ×N（每步 ~0.5 ms） + accept_len plateau → 净负。
```

> AGENT

Found the key piece. Now let me look at the training-v2.md for the linear probe details.

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training-v2.md",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 v2 训练改进记录
2	
3	2026-04-18 重新训练 draft model 的改进总集。旧 v1 配方（SkyPile/code_search_net/wikitext + SEQ_LEN 截断 + TTT 多步 eval）与线上分布严重 mismatch，v2 针对数据分布、管线效率、eval 方法论做了全面重构。
4	
5	## 1. 数据集重构
6	
7	**动机**：旧训练分布（SkyPile 中文 web + code_search_net + wikitext）与线上 bench 严重 mismatch。线上 83% 是中文长 CoT 推理，旧训练集 0% 含 `<think>` 风格。
8	
9	**v2 配比**（20,000 样本 × 2048 tok，真实代码 token ≈ 0.6%）：
10	
11	| 数据源 | 占比 | block 切法 |
12	|---|---|---|
13	| Chinese-DeepSeek-R1-Distill-110k | 60% | 按 `repo_name` 分组拼接 |
14	| stem_zh_instruction | 22% | 按学科分组 |
15	| OpenCodeReasoning (Python 全量) | 11.5% | 按 `source` 分组 |
16	| codeforces-cots py_decontam | 5.5% | 长样本直接切 |
17	| dolphin-r1 reasoning-deepseek | 1% | 长样本直接切 |
18	
19	剔除：NuminaMath（cn_k12 text 实际为英文）。
20	
21	## 2. 采集管线
22	
23	| 文件 | 作用 |
24	|---|---|
25	| `eagle/build_prompts.py` | 读 5 个数据源 → 切 2048-tok block → `/tmp/eagle3_prompts.jsonl` |
26	| `eagle/collect_data.py` | 并发发 `/v1/completions max_tokens=1` → hook 写 `.pt` |
27	| `demo-sala/.../minicpm.py:94` | `_EAGLE3_TOP_K = int(env('EAGLE3_TOP_K', '256'))`，从 256 改 128 |
28	
29	**陷阱 1：chunked prefill 切分 hook**。server 默认 `chunked-prefill-size=8192`，batch 32 × 2048 = 65k tok 被切 8 chunk。hook 对每个 chunk 写一次 .pt → 一条 prompt 产生多个残片，呈 full 2048 + medium (1024-2047) + tiny (<256) 三档分布。**修法**：采集用 `--chunked-prefill-size 131072` 或 65536。v2 采集未加，事后按长度 > 1024 过滤保留 19601 条。
30	
31	**陷阱 2：val_ood `EAGLE3_MAX_TOKENS=0` 导致 OOM**。server 需降 `--mem-fraction-static 0.70 --max-running-requests 4` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
32	
33	**陷阱 3：过滤 `completion_tokens >= 2000` 错误**。bench 本身就是生产分布，不该按长度过滤。改 `> 0` 拿全 64 条。
34	
35	## 3. 训练管线优化（-39% wall clock）
36	
37	Profile 定位（离线 microbench）：
38	
39	| 项 | baseline | 优化后 | 说明 |
40	|---|---|---|---|
41	| `GRAD_CHECKPOINT` | True | **False** | bwd 286→185 ms（-35%），peak mem 11→28 GB（84 GB 余量充足） |
42	| `BATCH_SIZE` / `GRAD_ACCUM` | 2 / 4 | **8 / 1** | effective batch 保持 8 |
43	| data loading | sync | **AsyncPrefetcher** | disk I/O 完全被 GPU 覆盖，77→21 ms |
44	| **per_sample** | **279 ms** | **169 ms** | **-39%** |
45	
46	`AsyncPrefetcher` 类在 `eagle/train.py`：后台线程 + pin_memory + `non_blocking` transfer，queue_size=2。
47	
48	Forward 内部分解（BS=4 per_sample 184ms）：
49	
50	| op | 占比 | 说明 |
51	|---|---|---|
52	| midlayer (attn + MLP) | **63%** | FP4_QAT fake-quant 固有 cost，继续优化需改 `_FP4QuantSTE` |
53	| lm_head (4096→32000) | 27% | |
54	| loss + target_p | 8% | |
55	| fc / embed / mask | 2% | |
56	
57	**Profile 数据**（BS=4 grad_ckpt=False，稳态）：
58	
59	```
60	fwd= 280ms  bwd= 381ms  mem=28.6GB  per_sample=170.1ms
61	```
62	
63	BS=12 测试（peak_mem 71.6 GB，边缘 OOM + disk-bound stalls 让 per_sample 回升到 185ms），不采用。
64	
65	## 4. 对齐官方 EAGLE（超参修正）
66	
67	| 参数 | 前 | 后 | 理由 |
68	|---|---|---|---|
69	| `MAX_GRAD_NORM` | 5.0 | **1.0** | 官方默认，防 grad 爆 |
70	| `WARMUP_STEPS` | 500 | **1500** | 总 step 数 6%（前 2% 过激） |
71	| `TTT_STEPS` | 3 | 3（未改） | 推理 spec_steps=2 只用 step 0-1；step 2 做正则 |
72	
73	## 5. eval_ood 修复
74	
75	**原问题**：旧 `eval_ood` 做 step 0..2 完整 TTT + SEQ_LEN 截断 + 逐 step 加权 acc。Step 1/2 在长序列上因 RoPE 外推坍塌（>2048 tok 时 step1 acc 18%）。
76	
77	**v2 改为 step-0 only + 全长**（`eagle/train.py:eval_ood`）：
78	
79	- 只测 step 0（user_4813494d token 预测），这是线上实际用的能力
80	- 全长 val_ood，不截断到 SEQ_LEN
81	
82	**v2 新坑**：RoPE cache = `SEQ_LEN * TTT_STEPS + 8192 + 64 = 14400`，val_ood 最长 30991 tok → 越界 `vectorized_gather_kernel`。**修法**：eval_ood 内按 `rope_max` 截断样本。
83	
84	**检查点提前保存**：ckpt 从 eval_ood 之后移到之前，eval 崩不再丢整 epoch。
85	
86	旧 `weighted_acc`（truncated 2048, TTT=3）= 0.5255 → 新 step-0 acc（full length）= 0.6607。对齐线上真实使用方式。
87	
88	## 6. vocab 覆盖（32k 维持最优）
89	
90	| K | train cov | val_ood target cov | masked |
91	|---|---|---|---|
92	| 8000 | 93.94% | 91.69% | 8.31% |
93	| 16000 | 98.07% | 96.48% | 3.52% |
94	| **32000** | **99.75%** | **99.23%** | **0.77%** |
95	
96	K=16000 masked 4.6×，accept_len 上限损失不划算。
97	
98	## 7. 未做（留给下轮）
99	
100	- **response-only loss mask**：需要 `build_prompts.py` 记录 assistant 段 token 边界。当前多数数据源无结构化分隔（只 `codeforces` 有明确 messages user/assistant）。
101	- **aux_layers [0,9,22] or [7,15,23,31]**：当前 [1,10,22] 偏前，均匀分布（借 DFlash 思路）可能更好。需重采数据。
102	- **fp8 aux_hidden 压缩**：存储 / IO 省 2×，精度待验证。
103	- **torch.compile**：midlayer 63% 占比，compile 可能省 15-20%。
104	
105	## 8. 训练重要文件
106	
107	- `eagle/train.py` — 主训练（含 AsyncPrefetcher、FP4_QAT、TTT loop）
108	- `eagle/build_prompts.py` — 数据切块
109	- `eagle/collect_data.py` — 并发 server 请求采集
110	- `eagle/convert_to_sglang.py` — ckpt → `eagle/sglang_model/` 格式
111	- `eagle/sglang_model/` — 当前部署 draft（v2，415MB safetensors）
112	- `demo-sala/sglang/python/sglang/srt/models/minicpm.py:90-161` — EAGLE3_COLLECT hook
113
```

> AGENT

I have comprehensive information now. Let me compile the findings.

---

## 研究结果：EAGLE-3 辅助层（aux layers）选择方法

### 核心论文

**EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test** (arXiv:2503.01840, NeurIPS 2025)，作者 Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang（Peking University / Microsoft Research Asia）。

### 层选择方法

**EAGLE-3 论文本身并没有提出一套系统化的层选择方法论。** 论文只描述了"从 target model 的 low、middle、high 三个层级提取 hidden states"，然后 concat 成 3k 维向量，经 FC 层压缩回 k 维。论文没有给出：
- 具体的层索引选择算法（如 linear probe、mutual information 等）
- 层数的消融实验（只做了"top-layer only vs 三层 fusion"的消融，没有比较不同层组合）
- 选多少层的推荐（固定为 3 层）

### 消融实验

论文 Table 2 的消融只有两个维度：
1. EAGLE-2 baseline (top-layer only): speedup 3.16x, tau 4.05
2. + remove feature prediction constraint: speedup 3.82x, tau 5.37
3. + fused features (low/mid/high): speedup 4.40x, tau 6.13

**没有**不同层组合的消融。

### 实际工程中的做法

从实际部署代码和模型配置来看：

1. **固定 3 层**：所有 EAGLE-3 部署都用 3 个 aux 层（early/middle/late triad）

2. **具体层索引因模型而异**，常见选法是大致均匀分布在模型深度上：
   - **NVIDIA gpt-oss-120b (36 layers)**：layers 2, 18, 33（约 ~5%, ~50%, ~92% depth）
   - **Nemotron-Cascade2 (52 layers)**：layers 2, 26, 48（约 ~4%, ~51%, ~94% depth）
   - **本项目 MiniCPM-SALA (32 layers)**：layers 1, 10, 22（约 ~3%, ~31%, ~69% depth）

3. **Linear probe 验证**：本项目 (`/user_4813494d/openbmb/docs/eagle/README.md` 第 25 行) 记载了使用 linear probe 验证层选择的做法：
   > "Aux layers：[1, 10, 22]，linear probe 验证最优（CE=6.51 vs 次优 6.57）"

   即：对不同层组合训练 linear probe（线性分类器从 hidden states 预测 next token），用交叉熵作为指标，选 CE 最低的组合。

4. **NVIDIA 的经验法则**（来自 Nemotron 模型卡的注释）：
   - 避免 layer 0（embedding 层附近，hidden states 还只是原始 token embedding，缺乏上下文化）
   - 避免最后一层（与只用 top-layer 差异不大）
   - 中间层选在模型中部

5. **本项目的待做项**（`/user_4813494d/openbmb/docs/eagle/training-v2.md` 第 101 行）提到了替代方案：
   > "aux_layers [0,9,22] or [7,15,23,31]：当前 [1,10,22] 偏前，均匀分布（借 DFlash 思路）可能更好。需重采数据。"

   这说明 4 层方案也在考虑中，且有"均匀分布更好"的直觉。

### 总结

| 问题 | 答案 |
|---|---|
| 论文推荐的选层方法 | **无系统方法**。论文只说"low/mid/high"三层 fusion，没有给出选择算法 |
| 工程实践中的做法 | **Linear probe**（测量各层 hidden state 对 next-token prediction 的 CE loss），或者简单的**等间距三分法**（~5%, ~50%, ~90% depth） |
| 推荐层数 | **固定 3 层**（论文和所有开源实现一致） |
| 层数消融 | **论文中没有**。社区有人尝试 4 层但尚无发表结果 |
| 关键避坑 | 避免 layer 0（太浅，只是 raw embedding）；避免最后一层（退化为 top-layer only） |

> DEVELOPER

深入检查 EAGLE-3 draft model 在 sglang 推理中的加载与前向流程，找出**所有可能与训练不一致的 bias / 量化 / 参数加载问题**。这非常关键，关系到 draft model 是否真的能复现训练时的精度。

## 训练侧（已确认事实）
- 训练脚本：/user_4813494d/openbmb/eagle/train.py
- 训练时 fc 是 `nn.Linear(AUX_DIM=hidden_size*3=12288, HIDDEN_SIZE=4096, bias=False)` bf16，不做 FP4 QAT
- 其他线性层（q/k/v/o + gate/up/down + lm_head 等）走 FP4_QAT (STE fake-quant on fwd)
- aux_hidden 在采集时是从 target 的 layer_ids=[4, 9, 24] 抽取，3 层 hidden 在 last-dim 上 concat → AUX_DIM=12288
- 训练 forward：fc(aux) → embed_tokens(input_ids) → concat → norm → 1 个 transformer layer → lm_head(over draft_vocab=32000)
- aux_hidden 在数据集里以 NVFP4 存储 (group=16, bf16 scale)，加载时 decompress 回 bf16
- shifted alignment：input_ids[:, 1:], aux_hidden[:, :-1], target[:, 1:]

## 转换侧（v3 → sglang_model_v3/）
- /user_4813494d/openbmb/eagle/convert_to_sglang.py，FC_BF16=True
- model.fc.weight 直接 bf16，无 NVFP4 4 元组（weight, weight_scale, weight_scale_2, input_scale）
- 其他线性层走 add_nvfp4_tensors（NVFP4 4 元组）
- hf_quant_config.json exclude_modules=["model.fc"]
- config.json: eagle_aux_hidden_state_layer_ids=[4,9,24], target_hidden_size=4096, hidden_size=4096, draft_vocab_size=32000

## 部署侧（需要你审计）
- 部署模型路径：/user_4813494d/openbmb/eagle/sglang_model_v3/
- sglang fork：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/
- draft 模型类：llama_eagle3.py（应该在 srt/models/ 下）
- 量化加载：layers/quantization/modelopt_quant.py（NVFP4LinearMethod / UnquantizedLinearMethod / is_layer_excluded）

## 任务
请仔细检查并报告以下每一项是否一致：

1. **fc 层加载**：sglang 加载 model.fc.weight 时是否真的走 UnquantizedLinearMethod（不做 fp4 反量化）？exclude_modules regex 匹配 "model.fc" 时 prefix 实际是什么？是否会因 prefix 拼接导致漏匹配？

2. **fc 层 bias**：训练时 nn.Linear(bias=False)，sglang ColumnParallelLinear 默认 bias 配置是什么？如果默认 bias=True 会怎样？safetensors 里没有 fc.bias，加载时是会报 missing key 还是初始化为 0 还是 NaN？

3. **fc 输入维度**：训练是 fc(aux_hidden_concat[..., 12288])，AUX_DIM = target_hidden_size*3。sglang 的 fc in_features 怎么算的？是从 config.target_hidden_size*3 推的吗？config 是 4096，但 sglang 是否用了别的字段？

4. **aux_hidden 抽取顺序**：训练时 aux 是 [layer4, layer9, layer24] 顺序 concat。sglang 推理侧从 target 抽取后 concat 顺序与训练一致吗？eagle_aux_hidden_state_layer_ids=[4,9,24] 是有序的还是会被排序？

5. **aux_hidden dtype**：训练时 aux_hidden 在 fwd 时是 bf16 输入 fc。推理时 target 输出的 aux_hidden 是什么 dtype？有没有 fp16/bf16 不一致？

6. **embed_tokens / lm_head**：draft 模型里 embed_tokens 形状 (vocab=73448, hidden=4096)，lm_head 形状 (draft_vocab=32000, hidden=4096)。训练时 lm_head 走 FP4_QAT；部署时是 NVFP4 的吗？vocab/draft_vocab 是否对齐？draft_vocab=32000 是 tokenizer 的子集还是 remap 的？是否有 d2t/t2d remap 表？

7. **scale_emb=12**：config 里有 scale_emb=12（MiniCPM 的 embedding scale）。draft 推理时 embed_tokens 输出会乘 12 吗？训练时乘了吗？

8. **tie_word_embeddings=false**：draft 的 lm_head 不与 embed_tokens 共享。训练时确实是独立的吗？

9. **norm 层 (input_layernorm / post_attention_layernorm / norm)**：这些 RMSNorm 是不量化的吧？safetensors 里以 bf16 还是 float32 存？sglang 加载是否一致？训练时 dtype 是？

10. **rotary embedding**：max_position_embeddings=524288。draft 的 RoPE base / scaling 与 target 是否一致？训练时 RoPE max_len 是多少？是否会有位置编码不一致？

11. **transformer layer 内部**：draft 只有 1 个 layer。q/k/v/o + gate/up/down 都走 NVFP4。是否有训练 fwd 上做 QAT 但部署时 forward 路径不同（比如 input_scale 缺失/重新计算）的问题？

12. **lm_head NVFP4 量化**：lm_head 是大矩阵 (32000, 4096)，训练 FP4_QAT，部署 NVFP4。weight_scale_2 / input_scale 是怎么算的？convert_to_sglang.py 的 add_nvfp4_tensors 用的是 ammo 还是手算？校准的 amax 来源？是否复用 target lm_head 的 input_scale？还是重新算？

请把发现的每个 bias/不一致问题列出来，包括：可能的影响、确证/怀疑级别、复现方法。不要只看一个文件，要顺着实际加载链路读。可以用 grep 找 "fc"、"aux_hidden"、"eagle"、"draft_vocab"、"d2t"、"target_hidden_size"、"scale_emb" 等关键 symbol。

控制在 800 字以内，但发现的具体问题点要列清楚。

> AGENT

I'll conduct a thorough audit of the EAGLE-3 draft model's loading and forward flow in sglang to identify bias/quantization/parameter loading inconsistencies. Let me start by exploring the codebase systematically.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"*eagle*\" -type f | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle3_runtime_investigation.md
/user_4813494d/openbmb/eval/start_eagle.sh
/user_4813494d/openbmb/bench/results/fused_gla_eagle3.md
/user_4813494d/openbmb/bench/b12x/bench_eagle_fc.py
/user_4813494d/openbmb/tests/test_eagle_fused_scale_loader.py
/user_4813494d/openbmb/tests/test_eagle_batch_alignment.py
/user_4813494d/openbmb/tests/test_eagle_draft_extend_graph_padding.py
/user_4813494d/openbmb/.ipynb_checkpoints/eagle3_runtime_investigation-checkpoint.md
/user_4813494d/openbmb/eval/.ipynb_checkpoints/start_eagle-checkpoint.sh
/user_4813494d/openbmb/bench/b12x/results/b12x_eagle_fc.json
/user_4813494d/openbmb/tests/__pycache__/test_eagle_fused_scale_loader.cpython-310.pyc
/user_4813494d/openbmb/tests/__pycache__/test_eagle_batch_alignment.cpython-310.pyc
/user_4813494d/openbmb/tests/__pycache__/test_eagle_batch_alignment.cpython-310-pytest-9.0.3.pyc
/user_4813494d/openbmb/tests/__pycache__/test_eagle_replay_padding.cpython-310-pytest-9.0.3.pyc
/user_4813494d/openbmb/tests/__pycache__/test_eagle_replay_padding.cpython-310.pyc
/user_4813494d/openbmb/tests/__pycache__/test_eagle_draft_extend_graph_padding.cpython-310-pytest-9.0.3.pyc
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_utils.py
```

> AGENT

Let me search for the key files mentioned in the audit.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -path \"*llama_eagle3.py\" -o -path \"*convert_to_sglang.py\" -o -path \"*modelopt_quant.py\" | grep -v __pycache__"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/convert_to_sglang.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/llama_eagle3.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/convert_to_sglang.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Convert EAGLE-3 training checkpoint to sglang-compatible format.
4	
5	When FP4_QAT=True (default), packs BF16 master weights into NVFP4 format
6	(weight_packed uint8 + weight_scale fp8 + weight_scale_2 f32) so the
7	sglang model can be loaded with quantization="modelopt_fp4" and Marlin
8	W4A16 dispatch.  No post-training optimization — weights trained with
9	FP4QATLinear are already on the FP4 grid.
10	
11	Produces a directory with:
12	  - config.json (LlamaConfig-compatible, quantization_config set for NVFP4)
13	  - model.safetensors (weights: NVFP4 for linear layers, BF16 for norms)
14	
15	Usage:
16	    python3 eagle/convert_to_sglang.py
17	"""
18	
19	import json
20	import os
21	from pathlib import Path
22	
23	import torch
24	from safetensors.torch import save_file
25	
26	
27	CKPT_PATH = Path("eagle/weights/v3/epoch_2.pt")
28	OUTPUT_DIR = Path("eagle/sglang_model_v3")
29	# v3: fc stays bf16 (not NVFP4). sglang loads it via UnquantizedLinearMethod
30	# triggered by exclude_modules=["model.fc"] in hf_quant_config.json.
31	FC_BF16 = True
32	TARGET_MODEL = [REDACTED]
33	
34	# Set True when the checkpoint was trained with FP4_QAT=True in train.py.
35	# Weights are already FP4-grid-aligned; packing is lossless format conversion.
36	FP4_QAT_CKPT = True
37	
38	# Architecture constants (must match train.py)
39	HIDDEN_SIZE = 4096
40	AUX_DIM = HIDDEN_SIZE * 3  # 12288
41	VOCAB_SIZE = 73448
42	DRAFT_VOCAB_SIZE = 32000
43	NUM_HEADS = 32
44	NUM_KV_HEADS = 2
45	HEAD_DIM = 128
46	INTERMEDIATE_SIZE = 16384
47	RMS_NORM_EPS = 1e-6
48	FP4_GROUP_SIZE = 16
49	
50	
51	# ── NVFP4 packing ────────────────────────────────────────────────────────
52	
53	# FP4 E2M1 values and rounding boundaries
54	_FP4_POS = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0])
55	_FP4_BOUNDS = torch.tensor([0.25, 0.75, 1.25, 1.75, 2.5, 3.5, 5.0])
56	
57	
58	def _fp4_round(x: torch.Tensor) -> torch.Tensor:
59	    """Round to nearest FP4 E2M1 value (float output)."""
60	    pos = _FP4_POS.to(device=x.device, dtype=x.dtype)
61	    bounds = _FP4_BOUNDS.to(device=x.device, dtype=x.dtype)
62	    sign = x.sign()
63	    idx = torch.bucketize(x.abs().clamp(max=6.0), bounds)
64	    return sign * pos[idx]
65	
66	
67	def _float_to_fp4_nibble(x: torch.Tensor) -> torch.Tensor:
68	    """Map FP4 float values to 4-bit nibble indices (0-15).
69	
70	    Encoding (FP4 E2M1):
71	      0→0, 1→0.5, 2→1.0, 3→1.5, 4→2.0, 5→3.0, 6→4.0, 7→6.0
72	      8→-0, 9→-0.5, 10→-1.0, ..., 15→-6.0
73	    """
74	    bounds = _FP4_BOUNDS.to(device=x.device, dtype=x.dtype)
75	    sign = (x < 0).to(torch.uint8)
76	    idx = torch.bucketize(x.abs().clamp(max=6.0), bounds).to(torch.uint8)
77	    return idx | (sign << 3)  # 0-7 positive, 8-15 negative
78	
79	
80	def pack_nvfp4(weight: torch.Tensor, group_size: int = FP4_GROUP_SIZE):
81	    """Pack a BF16 weight matrix into NVFP4 format.
82	
83	    Args:
84	        weight: (N, K) BF16 tensor (N = out_features, K = in_features)
85	        group_size: elements per FP8 scale group (must be 16 for NVFP4)
86	
87	    Returns:
88	        weight_packed:  (N, K//2) uint8    — two FP4 nibbles per byte
89	        weight_scale:   (N, K//group_size) float8_e4m3fn  — per-group FP8 scale
90	        weight_scale_2: scalar float32     — global scale for the FP8 scales
91	    """
92	    assert weight.ndim == 2, f"Expected 2D weight, got {weight.ndim}D"
93	    N, K = weight.shape
94	    assert K % group_size == 0, f"K={K} must be divisible by group_size={group_size}"
95	
96	    w = weight.float().cpu()
97	    # Reshape into groups: (N, K/G, G)
98	    w_g = w.reshape(N, K // group_size, group_size)
99	
100	    # Per-group scale = max(|w|) / 6.0  (FP4 max magnitude = 6.0)
101	    per_group_scale = w_g.abs().amax(dim=-1).clamp(min=1e-8) / 6.0  # (N, K/G)
102	
103	    # Global FP32 scale: normalise per-group scales to fit in fp8_e4m3fn range
104	    fp8_max = 448.0  # float8_e4m3fn max
105	    global_scale_val = float(per_group_scale.amax().clamp(min=1e-8).item() / fp8_max)
106	
107	    # Encode per-group scales as FP8 (round-trip to get exact values used)
108	    scales_f32 = (per_group_scale / global_scale_val).clamp(-fp8_max, fp8_max)
109	    weight_scale_fp8 = scales_f32.to(torch.float8_e4m3fn)  # (N, K/G)
110	
111	    # Actual per-group scale after FP8 rounding
112	    actual_scale = weight_scale_fp8.float() * global_scale_val  # (N, K/G)
113	    actual_scale_exp = actual_scale.unsqueeze(-1).expand(-1, -1, group_size)  # (N, K/G, G)
114	
115	    # Scale weights, round to FP4 grid
116	    w_scaled = (w_g / actual_scale_exp).clamp(-6.0, 6.0)
117	    w_fp4 = _fp4_round(w_scaled.reshape(N, K))  # (N, K) float, values ∈ FP4 grid
118	
119	    # Encode each value as a 4-bit nibble index
120	    nibbles = _float_to_fp4_nibble(w_fp4)  # (N, K) uint8, range 0-15
121	
122	    # Pack: even column → low nibble, odd column → high nibble
123	    even = nibbles[:, 0::2]        # (N, K//2)
124	    odd  = nibbles[:, 1::2]        # (N, K//2)
125	    weight_packed = (even | (odd << 4)).to(torch.uint8)  # (N, K//2)
126	
127	    weight_scale_2 = torch.tensor(global_scale_val, dtype=torch.float32)
128	
129	    return weight_packed, weight_scale_fp8, weight_scale_2
130	
131	
132	def add_nvfp4_tensors(tensors: dict, sglang_key: str, weight_bf16: torch.Tensor) -> None:
133	    """Pack weight and add the three NVFP4 tensors to the output dict."""
134	    packed, scale, scale2 = pack_nvfp4(weight_bf16)
135	    tensors[f"{sglang_key}.weight"]       = packed
136	    tensors[f"{sglang_key}.weight_scale"] = scale
137	    tensors[f"{sglang_key}.weight_scale_2"] = scale2
138	    # input_scale is used by CUTLASS W4A4; not needed for Marlin W4A16
139	    # but add a dummy so the loader doesn't warn
140	    tensors[f"{sglang_key}.input_scale"] = torch.tensor(1.0, dtype=torch.float32)
141	
142	
143	# ── Conversion ────────────────────────────────────────────────────────────
144	
145	def convert():
146	    print(f"Loading checkpoint: {CKPT_PATH}")
147	    ckpt = torch.load(CKPT_PATH, weights_only=True)
148	    state = ckpt["model_state_dict"]
149	
150	    print(f"Checkpoint epoch: {ckpt['epoch']}, acc0: {ckpt.get('avg_acc0', 'N/A')}")
151	    print(f"FP4_QAT_CKPT={FP4_QAT_CKPT}")
152	
153	    # Load vocab mapping
154	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
155	    d2t = vocab_cache["d2t"]  # (32000,) — target vocab ids
156	
157	    # d2t diff format (sglang convention: stored = d2t - arange(draft_vocab))
158	    d2t_diff = d2t - torch.arange(DRAFT_VOCAB_SIZE)
159	
160	    # Helper: retrieve weight from state dict
161	    def get(key):
162	        w = state[key]
163	        return w.to(torch.bfloat16)
164	
165	    tensors = {}
166	
167	    if FP4_QAT_CKPT:
168	        # ── NVFP4 layers ──────────────────────────────────────────────────
169	        print("Packing linear layers as NVFP4 ...")
170	
171	        # fc: (HIDDEN_SIZE, AUX_DIM) = (4096, 12288)
172	        # v3: fc stays bf16 — sglang's exclude_modules + UnquantizedLinearMethod
173	        # path loads bare model.fc.weight (no NVFP4 4-tuple).
174	        if FC_BF16:
175	            tensors["model.fc.weight"] = get("fc.weight")
176	        else:
177	            add_nvfp4_tensors(tensors, "model.fc", get("fc.weight"))
178	
179	        # qkv: pre-merge q/k/v in BF16 then pack as a single NVFP4 tensor.
180	        # This ensures one consistent global scale covers all three projections.
181	        # Names like "qkv_proj.weight" do NOT match stacked_params_mapping
182	        # (.q_proj / .k_proj / .v_proj with leading dot), so they go through
183	        # the else (direct-load) branch in load_weights without any shard logic.
184	        qkv_merged = torch.cat([
185	            get("midlayer.self_attn.q_proj.weight"),
186	            get("midlayer.self_attn.k_proj.weight"),
187	            get("midlayer.self_attn.v_proj.weight"),
188	        ], dim=0)
189	        add_nvfp4_tensors(tensors, "model.midlayer.self_attn.qkv_proj", qkv_merged)
190	        del qkv_merged
191	
192	        add_nvfp4_tensors(tensors, "model.midlayer.self_attn.o_proj",
193	                          get("midlayer.self_attn.o_proj.weight"))
194	
195	        # MLP: pre-merge gate/up for the same reason.
196	        # "gate_up_proj.weight" does NOT contain ".gate_proj" or ".up_proj"
197	        # with a leading dot so it also bypasses stacked_params_mapping.
198	        gate_up_merged = torch.cat([
199	            get("midlayer.mlp.gate_proj.weight"),
200	            get("midlayer.mlp.up_proj.weight"),
201	        ], dim=0)
202	        add_nvfp4_tensors(tensors, "model.midlayer.mlp.gate_up_proj", gate_up_merged)
203	        del gate_up_merged
204	
205	        add_nvfp4_tensors(tensors, "model.midlayer.mlp.down_proj",
206	                          get("midlayer.mlp.down_proj.weight"))
207	
208	        # lm_head: ParallelLMHead inherits VocabParallelEmbedding which stores
209	        # BF16 weights — it does NOT get quantized even with quant_config.
210	        # Save as BF16 to match the parameter shape (draft_vocab_size, hidden_size).
211	        tensors["lm_head.weight"] = get("lm_head.weight")
212	
213	    else:
214	        # ── BF16 layers (legacy path) ──────────────────────────────────
215	        key_mapping = {
216	            "fc.weight":                              "model.fc.weight",
217	            "midlayer.self_attn.q_proj.weight":       "model.midlayer.self_attn.q_proj.weight",
218	            "midlayer.self_attn.k_proj.weight":       "model.midlayer.self_attn.k_proj.weight",
219	            "midlayer.self_attn.v_proj.weight":       "model.midlayer.self_attn.v_proj.weight",
220	            "midlayer.self_attn.o_proj.weight":       "model.midlayer.self_attn.o_proj.weight",
221	            "midlayer.mlp.gate_proj.weight":          "model.midlayer.mlp.gate_proj.weight",
222	            "midlayer.mlp.up_proj.weight":            "model.midlayer.mlp.up_proj.weight",
223	            "midlayer.mlp.down_proj.weight":          "model.midlayer.mlp.down_proj.weight",
224	            "norm.weight":                            "model.norm.weight",
225	            "lm_head.weight":                         "lm_head.weight",
226	        }
227	        for train_key, sglang_key in key_mapping.items():
228	            if train_key in state:
229	                tensors[sglang_key] = state[train_key].to(torch.bfloat16)
230	            else:
231	                print(f"  WARNING: missing key {train_key}")
232	
233	    # ── Norm weights (always BF16) ─────────────────────────────────────
234	    tensors["model.midlayer.input_layernorm.weight"]        = get("midlayer.input_emb_norm.weight")
235	    tensors["model.midlayer.hidden_norm.weight"]            = get("midlayer.hidden_norm.weight")
236	    tensors["model.midlayer.post_attention_layernorm.weight"] = get("midlayer.post_attention_layernorm.weight")
237	    tensors["model.norm.weight"]                            = get("norm.weight")
238	
239	    # ── d2t vocab mapping ──────────────────────────────────────────────
240	    tensors["d2t"] = d2t_diff
241	
242	    # ── embed_tokens: SKIPPED ──────────────────────────────────────────
243	    # SGLang's eagle_worker calls set_embed() to copy embed_tokens from the
244	    # target model at runtime, so we don't need to include the 573 MB weight
245	    # in the safetensors file. This saves ~573 MB in the submission package.
246	
247	    # ── Save safetensors ───────────────────────────────────────────────
248	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
249	    save_file(tensors, OUTPUT_DIR / "model.safetensors")
250	    print(f"Saved {len(tensors)} tensors to {OUTPUT_DIR / 'model.safetensors'}")
251	
252	    # ── config.json ───────────────────────────────────────────────────
253	    config = {
254	        "architectures": ["LlamaForCausalLMEagle3"],
255	        "model_type": "llama",
256	        "hidden_size": HIDDEN_SIZE,
257	        "intermediate_size": INTERMEDIATE_SIZE,
258	        "num_hidden_layers": 1,
259	        "num_attention_heads": NUM_HEADS,
260	        "num_key_value_heads": NUM_KV_HEADS,
261	        "head_dim": HEAD_DIM,
262	        "hidden_act": "silu",
263	        "max_position_embeddings": 524288,
264	        "rms_norm_eps": RMS_NORM_EPS,
265	        "vocab_size": VOCAB_SIZE,
266	        "draft_vocab_size": DRAFT_VOCAB_SIZE,
267	        "target_hidden_size": HIDDEN_SIZE,
268	        "scale_emb": 12,
269	        "tie_word_embeddings": False,
270	        "torch_dtype": "bfloat16",
271	        "eagle_config": {
272	            "use_aux_hidden_state": True,
273	            "eagle_aux_hidden_state_layer_ids": [4, 9, 24],
274	        },
275	    }
276	    # NOTE: Do NOT add quantization_config to config.json.
277	    # HuggingFace transformers does not recognize "modelopt" as a quant_method,
278	    # which causes ModelOptModelLoader to crash.  Quantization is detected via
279	    # hf_quant_config.json (written below) which SGLang checks via has_hf_quant_config().
280	
281	    with open(OUTPUT_DIR / "config.json", "w") as f:
282	        json.dump(config, f, indent=2)
283	    print("Saved config.json")
284	
285	    # ── hf_quant_config.json — tells SGLang this is pre-quantized ─────
286	    # SGLang's ModelOptModelLoader checks for this file via _is_already_quantized().
287	    # If present, it skips the re-quantization path (HuggingFace from_pretrained)
288	    # and goes directly to DefaultModelLoader.load_model() → model.load_weights().
289	    if FP4_QAT_CKPT:
290	        hf_quant_cfg = {
291	            "producer": {"name": "eagle3-fp4-qat", "version": "1.0"},
292	            "quantization": {
293	                "quant_algo": "NVFP4",
294	                "kv_cache_quant_algo": None,
295	                "group_size": FP4_GROUP_SIZE,
296	                "has_zero_point": False,
297	                "pre_quant_scale": False,
298	                # v3: fc kept bf16. ColumnParallelLinear sees prefix "model.fc"
299	                # and is_layer_excluded() returns True → UnquantizedLinearMethod.
300	                "exclude_modules": ["model.fc"] if FC_BF16 else [],
301	            },
302	        }
303	        with open(OUTPUT_DIR / "hf_quant_config.json", "w") as f:
304	            json.dump(hf_quant_cfg, f, indent=2)
305	        print("Saved hf_quant_config.json")
306	
307	    # ── Copy tokenizer files ──────────────────────────────────────────
308	    for fname in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
309	                  "tokenizer.model", "added_tokens.json"]:
310	        src = os.path.join(TARGET_MODEL, fname)
311	        if os.path.exists(src):
312	            import shutil
313	            shutil.copy2(src, OUTPUT_DIR / fname)
314	            print(f"Copied {fname}")
315	
316	    # ── Summary ───────────────────────────────────────────────────────
317	    print(f"\nOutput directory: {OUTPUT_DIR}")
318	    for fp in sorted(OUTPUT_DIR.iterdir()):
319	        sz = fp.stat().st_size
320	        print(f"  {fp.name}: {sz/1024/1024:.1f} MB" if sz > 1024*1024 else f"  {fp.name}: {sz/1024:.1f} KB")
321	
322	    print(f"\nConversion complete! epoch={ckpt['epoch']}, acc0={ckpt.get('avg_acc0','N/A')}")
323	    mode = "NVFP4 (Marlin W4A16)" if FP4_QAT_CKPT else "BF16"
324	    print(f"Weight format: {mode}")
325	    print(f"To use: --speculative-draft-model-path {OUTPUT_DIR.resolve()}")
326	
327	
328	if __name__ == "__main__":
329	    convert()
330	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the sglang model loading side:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py"
}
```

> TOOL

tool_result Read
```
1	"""
2	Copyright 2023-2024 SGLang Team
3	Licensed under the Apache License, Version 2.0 (the "License");
4	you may not use this file except in compliance with the License.
5	You may obtain a copy of the License at
6	
7	    http://www.apache.org/licenses/LICENSE-2.0
8	
9	Unless required by applicable law or agreed to in writing, software
10	distributed under the License is distributed on an "AS IS" BASIS,
11	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
12	See the License for the specific language governing permissions and
13	limitations under the License.
14	"""
15	
16	from sglang.srt.utils import add_prefix
17	
18	# Adapted from
19	# https://github.com/SafeAILab/EAGLE/blob/main/eagle/model/cnets.py
20	"""Inference-only LLaMA-EAGLE model compatible with HuggingFace weights."""
21	
22	import copy
23	from typing import Iterable, Optional, Tuple
24	
25	import torch
26	from torch import nn
27	from transformers import LlamaConfig
28	
29	from sglang.srt.distributed import get_pp_group
30	from sglang.srt.layers.layernorm import RMSNorm
31	from sglang.srt.layers.linear import ColumnParallelLinear, QKVParallelLinear
32	from sglang.srt.layers.logits_processor import LogitsProcessor
33	from sglang.srt.layers.quantization.base_config import QuantizationConfig
34	from sglang.srt.layers.vocab_parallel_embedding import (
35	    ParallelLMHead,
36	    VocabParallelEmbedding,
37	)
38	from sglang.srt.model_executor.forward_batch_info import ForwardBatch, PPProxyTensors
39	from sglang.srt.model_loader.weight_utils import default_weight_loader
40	from sglang.srt.models.llama import LlamaDecoderLayer, LlamaForCausalLM, LlamaMLP
41	
42	
43	class LlamaDecoderLayer(LlamaDecoderLayer):
44	    def __init__(
45	        self,
46	        config: LlamaConfig,
47	        layer_id: int = 0,
48	        quant_config: Optional[QuantizationConfig] = None,
49	        prefix: str = "",
50	    ) -> None:
51	        super().__init__(config, layer_id, quant_config, prefix)
52	
53	        # override qkv
54	        self.self_attn.qkv_proj = QKVParallelLinear(
55	            2 * self.hidden_size,
56	            self.self_attn.head_dim,
57	            self.self_attn.total_num_heads,
58	            self.self_attn.total_num_kv_heads,
59	            bias=False,
60	            quant_config=quant_config,
61	            prefix=add_prefix("qkv_proj", prefix),
62	        )
63	
64	        if config.model_type == "llama4_text":
65	            inter_size = config.intermediate_size_mlp
66	        else:
67	            inter_size = config.intermediate_size
68	
69	        self.mlp = LlamaMLP(
70	            config.hidden_size, inter_size, config.hidden_act, quant_config, prefix
71	        )
72	
73	        self.hidden_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
74	
75	    def forward(
76	        self,
77	        positions: torch.Tensor,
78	        embeds: torch.Tensor,
79	        hidden_states: torch.Tensor,
80	        forward_batch: ForwardBatch,
81	        residual: Optional[torch.Tensor],
82	    ) -> Tuple[torch.Tensor, torch.Tensor]:
83	
84	        residual = hidden_states
85	        embeds = self.input_layernorm(embeds)
86	        hidden_states = self.hidden_norm(hidden_states)
87	
88	        hidden_states = torch.cat([embeds, hidden_states], dim=-1)
89	        # Self Attention
90	        hidden_states = self.self_attn(
91	            positions=positions,
92	            hidden_states=hidden_states,
93	            forward_batch=forward_batch,
94	        )
95	
96	        hidden_states, residual = self.post_attention_layernorm(hidden_states, residual)
97	
98	        # Fully Connected
99	        hidden_states = self.mlp(hidden_states)
100	
101	        return hidden_states, residual
102	
103	
104	class LlamaModel(nn.Module):
105	    def __init__(
106	        self,
107	        config: LlamaConfig,
108	        quant_config: Optional[QuantizationConfig] = None,
109	        prefix: str = "",
110	    ) -> None:
111	        super().__init__()
112	        self.config = config
113	
114	        self.is_mrope_enabled = (
115	            hasattr(config, "rope_scaling")
116	            and config.rope_scaling is not None
117	            and "mrope_section" in config.rope_scaling
118	        )
119	        # fix rope_scaling for qwen2.5-vl
120	        if self.is_mrope_enabled:
121	            config.rope_scaling["rope_type"] = "default"
122	
123	        self.vocab_size = config.vocab_size
124	        self.embed_tokens = VocabParallelEmbedding(
125	            config.vocab_size,
126	            config.hidden_size,
127	            prefix=add_prefix("embed_tokens", prefix),
128	        )
129	
130	        if hasattr(config, "target_hidden_size"):
131	            self.hidden_size_in = config.target_hidden_size
132	        else:
133	            self.hidden_size_in = config.hidden_size
134	
135	        # Use ColumnParallelLinear (supports quant_config) instead of plain Linear
136	        # so NVFP4 / Marlin quantization applies to fc as well.
137	        self.fc = ColumnParallelLinear(
138	            self.hidden_size_in * 3,
139	            config.hidden_size,
140	            bias=getattr(config, "bias", False),
141	            quant_config=quant_config,
142	            prefix=add_prefix("fc", prefix),
143	        )
144	
145	        self.midlayer = LlamaDecoderLayer(config, 0, quant_config, prefix)
146	
147	        self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
148	
149	        # MiniCPM-style scale_emb (default 1.0 for standard Llama)
150	        self.scale_emb = getattr(config, "scale_emb", 1.0)
151	
152	    def forward(
153	        self,
154	        input_ids: torch.Tensor,
155	        positions: torch.Tensor,
156	        forward_batch: ForwardBatch,
157	        input_embeds: torch.Tensor = None,
158	        pp_proxy_tensors: Optional[PPProxyTensors] = None,
159	    ) -> torch.Tensor:
160	        if input_embeds is None:
161	            embeds = self.embed_tokens(input_ids) * self.scale_emb
162	        else:
163	            embeds = input_embeds
164	
165	        if self.is_mrope_enabled:
166	            positions = forward_batch.mrope_positions
167	
168	        hidden_states = forward_batch.spec_info.hidden_states
169	        if hidden_states.shape[-1] != embeds.shape[-1]:
170	            # ColumnParallelLinear returns (output, bias) tuple
171	            hidden_states, _ = self.fc(hidden_states)
172	
173	        # idle batch
174	        if hidden_states.shape[0] == 0:
175	            return hidden_states, [hidden_states]
176	
177	        residual = None
178	        hidden_states, residual = self.midlayer(
179	            positions,
180	            embeds,
181	            hidden_states,
182	            forward_batch,
183	            residual,
184	        )
185	
186	        hidden_states_to_logits, hidden_states_to_aux = self.norm(
187	            hidden_states, residual
188	        )
189	
190	        # For draft decode, we capture the hidden state before norm
191	        return hidden_states_to_logits, [hidden_states_to_aux]
192	
193	
194	class LlamaForCausalLMEagle3(LlamaForCausalLM):
195	    def __init__(
196	        self,
197	        config: LlamaConfig,
198	        quant_config: Optional[QuantizationConfig] = None,
199	        prefix: str = "",
200	    ) -> None:
201	        nn.Module.__init__(self)
202	        self.config = config
203	        self.quant_config = quant_config
204	        self.pp_group = get_pp_group()
205	
206	        if self.config.num_hidden_layers != 1:
207	            raise ValueError("EAGLE3 currently only supports 1 layer")
208	
209	        self.model = LlamaModel(
210	            config, quant_config=quant_config, prefix=add_prefix("model", prefix)
211	        )
212	        # Llama 3.2 1B Instruct set tie_word_embeddings to True
213	        # Llama 3.1 8B Instruct set tie_word_embeddings to False
214	        self.load_lm_head_from_target = False
215	        if self.config.tie_word_embeddings:
216	            self.lm_head = self.model.embed_tokens
217	        else:
218	            if config.draft_vocab_size is None:
219	                self.load_lm_head_from_target = True
220	                config.draft_vocab_size = config.vocab_size
221	            self.lm_head = ParallelLMHead(
222	                config.draft_vocab_size,
223	                config.hidden_size,
224	                quant_config=quant_config,
225	                prefix=add_prefix("lm_head", prefix),
226	            )
227	
228	        config_ = copy.deepcopy(config)
229	        config_.vocab_size = (
230	            config_.draft_vocab_size
231	        )  # draft logits processor has it's own vocab size
232	        self.logits_processor = LogitsProcessor(config_)
233	
234	        self.capture_aux_hidden_states = True
235	        self.hot_token_id = None
236	
237	    def load_weights(self, weights: Iterable[Tuple[str, torch.Tensor]]) -> None:
238	        params_dict = dict(self.named_parameters())
239	        # Define the parameter mapping for stacked parameters
240	        stacked_params_mapping = [
241	            # (param_name, shard_name, shard_id)
242	            (".qkv_proj", ".q_proj", "q"),
243	            (".qkv_proj", ".k_proj", "k"),
244	            (".qkv_proj", ".v_proj", "v"),
245	            (".gate_up_proj", ".gate_proj", 0),
246	            (".gate_up_proj", ".up_proj", 1),
247	        ]
248	
249	        for name, loaded_weight in weights:
250	            if "d2t" in name:
251	                # d2t stores diffs between draft id and target id
252	                self.hot_token_id = loaded_weight + torch.arange(loaded_weight.shape[0])
253	                continue
254	
255	            if "t2d" in name:
256	                continue
257	
258	            _nvfp4_suffixes = (".weight_scale", ".weight_scale_2", ".input_scale")
259	            for param_name, weight_name, shard_id in stacked_params_mapping:
260	                if weight_name not in name:
261	                    continue
262	                # NVFP4 auxiliary tensors share the base name (e.g. q_proj.weight_scale)
263	                # but must NOT go through the shard weight_loader — fall through to direct load
264	                if any(name.endswith(sfx) for sfx in _nvfp4_suffixes):
265	                    break
266	                name = name.replace(weight_name, param_name)
267	                param_name = f"model.{name}" if name not in params_dict else name
268	                if param_name in params_dict:
269	                    param = params_dict[param_name]
270	                    weight_loader = getattr(
271	                        param, "weight_loader", default_weight_loader
272	                    )
273	                    weight_loader(param, loaded_weight, shard_id)
274	                break
275	            else:
276	                # Handle regular parameters
277	                param_name = name if name in params_dict else f"model.{name}"
278	                if param_name in params_dict:
279	                    param = params_dict[param_name]
280	                    weight_loader = getattr(
281	                        param, "weight_loader", default_weight_loader
282	                    )
283	                    weight_loader(param, loaded_weight)
284	
285	    def get_hot_token_id(self):
286	        return self.hot_token_id
287	
288	
289	EntryClass = [LlamaForCausalLMEagle3]
290	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the quantization loading code:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 300
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
103	            f"entries={len(AutoTuner.get().profiling_cache)}"
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
114	# b12x backend (sm_120a block-scaled MMA, 3-tier Marlin/b12x/CUTLASS dispatch).
115	# Bench-validated 2026-04-22 (bench/b12x/bench_full_matrix.json): decode GEMM
116	# kernel time saved up to 4.7× vs CUTLASS at M=16..256. Bit-identical vs CUTLASS
117	# (bench/b12x/test_correctness.py: 69/69 cos_sim=1.0). See docs/kernels-sm120.md §7.4.
118	#
119	# Gated on env CUTE_DSL_ARCH=sm_120a + nvidia-cutlass-dsl install + opt-in
120	# SGLANG_ENABLE_B12X=1. If any prerequisite missing, dispatch falls back to
121	# today's Marlin(≤48)/CUTLASS two-tier path.
122	import os as _os_b12x  # noqa: E402
123	_B12X_OPTIN = _os_b12x.environ.get("SGLANG_ENABLE_B12X", "0") == "1"
124	if _B12X_OPTIN:
125	    try:
126	        from sglang.srt.layers.quantization.b12x_fp4 import (
127	            b12x_available as _b12x_available,
128	            b12x_gemm_fp4 as _b12x_gemm_fp4,
129	            MARLIN_UPPER as _B12X_MARLIN_UPPER,
130	            CUTLASS_OVERRIDE as _B12X_CUTLASS_OVERRIDE,
131	            _bucket_m as _b12x_bucket_m,
132	        )
133	        _HAS_B12X = _b12x_available()
134	    except Exception as _e:
135	        logging.getLogger(__name__).warning(f"[b12x] dispatch disabled: {_e}")
136	        _HAS_B12X = False
137	        _B12X_MARLIN_UPPER = {}
138	        _B12X_CUTLASS_OVERRIDE = frozenset()
139	else:
140	    _HAS_B12X = False
141	    _B12X_MARLIN_UPPER = {}
142	    _B12X_CUTLASS_OVERRIDE = frozenset()
143	
144	try:
145	    from flashinfer.fused_moe import cutlass_fused_moe as flashinfer_cutlass_fused_moe
146	    from flashinfer.fused_moe.core import ActivationType
147	except ImportError:
148	    flashinfer_cutlass_fused_moe = None
149	
150	    # Define a minimal ActivationType enum if flashinfer is not available
151	    class ActivationType(IntEnum):
152	        Swiglu = 3
153	        Relu2 = 6
154	
155	
156	# Initialize logger for the module
157	logger = logging.getLogger(__name__)
158	
159	
160	def _sglang_fp4_gemm_fake(
161	    input: torch.Tensor,
162	    weight: torch.Tensor,
163	    input_sf: torch.Tensor,
164	    weight_sf: torch.Tensor,
165	    alpha: torch.Tensor,
166	    out_dtype: torch.dtype,
167	    out_features: int,
168	) -> torch.Tensor:
169	    M = input.shape[-2]
170	    N = int(out_features)
171	    return input.new_empty((M, N), dtype=out_dtype)
172	
173	
174	@register_custom_op(fake_impl=_sglang_fp4_gemm_fake)
175	def fp4_gemm(
176	    input: torch.Tensor,
177	    weight: torch.Tensor,
178	    input_sf: torch.Tensor,
179	    weight_sf: torch.Tensor,
180	    alpha: torch.Tensor,
181	    out_dtype: torch.dtype,
182	    out_features: int,
183	) -> torch.Tensor:
184	    backend = FLASHINFER_FP4_GEMM_BACKEND if FLASHINFER_FP4_GEMM_BACKEND else "cutlass"
185	    if enable_flashinfer_fp4_gemm:
186	        return flashinfer_fp4_gemm(
187	            input, weight, input_sf, weight_sf, alpha, out_dtype, backend=backend
188	        )
189	    else:
190	        return cutlass_fp4_gemm(input, weight, input_sf, weight_sf, alpha, out_dtype)
191	
192	
193	if is_cuda() and (not is_sm120_supported()) and (fp4_quantize is not None):
194	
195	    @register_fake_if_exists("sgl_kernel::scaled_fp4_quant")
196	    def _sgl_kernel_scaled_fp4_quant_fake(
197	        output, input, output_scale, input_global_scale
198	    ):
199	        return
200	
201	
202	CUTEDSL_MOE_SCALAR_INPUT_SCALE = get_bool_env_var(
203	    "SGLANG_CUTEDSL_MOE_SCALAR_INPUT_SCALE", "true"
204	)
205	
206	# TODO make it true by default when the DeepEP PR is merged
207	MOE_NVFP4_DISPATCH = envs.SGLANG_MOE_NVFP4_DISPATCH.get()
208	FLASHINFER_FP4_GEMM_BACKEND = envs.SGLANG_FLASHINFER_FP4_GEMM_BACKEND.get()
209	
210	# Hybrid Marlin decode threshold: M <= threshold uses Marlin FP4 GEMV,
211	# M > threshold uses CUTLASS NVFP4 W4A4. Set via env var, 0 = disabled.
212	# Per-shape override: gate_up_proj (fused, N=32768) crosses over earlier than
213	# other projections per offline bench (Marlin 94us vs CUTLASS 77us at M=48).
214	import os as _os
215	_MARLIN_HYBRID_THRESHOLD = int(_os.environ.get("SGLANG_MARLIN_DECODE_THRESHOLD", "0"))
216	_MARLIN_THRESHOLD_GATE_UP = int(_os.environ.get("SGLANG_MARLIN_THRESHOLD_GATE_UP", "24"))
217	
218	
219	def _resolve_marlin_threshold(part_size_n: int, part_size_k: int) -> int:
220	    """Return per-layer Marlin threshold based on output shape.
221	
222	    gate_up_proj fused has output N=2*intermediate_size. For MiniCPM-SALA this
223	    is 32768. At M=48 Marlin loses to CUTLASS by ~17us/call on this shape.
224	    Lower threshold to 24 (next CUDA graph bucket below crossover).
225	    """
226	    if _MARLIN_HYBRID_THRESHOLD <= 0:
227	        return 0
228	    if part_size_n == 32768 and part_size_k == 4096:
229	        return _MARLIN_THRESHOLD_GATE_UP
230	    return _MARLIN_HYBRID_THRESHOLD
231	
232	# Supported activation schemes for the current configuration
233	ACTIVATION_SCHEMES = ["static"]
234	
235	ACT_STR_TO_TYPE_MAP = {
236	    "silu": ActivationType.Swiglu,  # This is the default
237	    "relu2": ActivationType.Relu2,
238	}
239	
240	
241	class ModelOptQuantConfig(QuantizationConfig):
242	    def __init__(
243	        self,
244	        kv_cache_quant_algo: Optional[str],
245	        exclude_modules: Optional[List[str]],
246	        packed_modules_mapping: Optional[Dict[str, List[str]]],
247	    ):
248	        super().__init__()
249	        self.packed_modules_mapping = packed_modules_mapping
250	        self.exclude_modules = exclude_modules or []
251	        self.kv_cache_quant_algo = kv_cache_quant_algo
252	
253	    def _get_quant_method(
254	        self,
255	        layer: torch.nn.Module,
256	        prefix: str,
257	        *,
258	        Linear: type[LinearMethodBase],
259	        Moe: type[FusedMoEMethodBase],
260	    ) -> Optional[QuantizeMethodBase]:
261	        from sglang.srt.layers.linear import LinearBase
262	        from sglang.srt.layers.moe.fused_moe_triton import FusedMoE
263	
264	        if isinstance(layer, LinearBase):
265	            if is_layer_skipped(
266	                prefix, self.exclude_modules, self.packed_modules_mapping
267	            ) or self.is_layer_excluded(prefix):
268	                return UnquantizedLinearMethod()
269	            return Linear(self)
270	        elif self.kv_cache_quant_algo and isinstance(layer, RadixAttention):
271	            return ModelOptFp8KVCacheMethod(self)
272	        elif isinstance(layer, FusedMoE):
273	            return Moe(self)
274	        return None
275	
276	    @classmethod
277	    def get_config_filenames(cls) -> List[str]:
278	        return ["hf_quant_config.json"]
279	
280	    def get_scaled_act_names(self) -> List[str]:
281	        return []
282	
283	
284	class ModelOptFp8Config(ModelOptQuantConfig):
285	    """Configuration for ModelOpt FP8 quantization, including serialization and compatibility checks."""
286	
287	    def __init__(
288	        self,
289	        is_checkpoint_fp8_serialized: bool = False,
290	        kv_cache_quant_method: Optional[str] = None,
291	        exclude_modules: Optional[List[str]] = None,
292	        packed_modules_mapping: Optional[Dict[str, List[str]]] = None,
293	    ) -> None:
294	        """
295	        Args:
296	            is_checkpoint_fp8_serialized (bool): Indicates if the checkpoint uses serialized FP8 format.
297	        """
298	        super().__init__(kv_cache_quant_method, exclude_modules, packed_modules_mapping)
299	        self.is_checkpoint_fp8_serialized = is_checkpoint_fp8_serialized
300	        if is_checkpoint_fp8_serialized:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Let me continue reading the quantization file and check the exclude_modules logic:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"is_layer_excluded\\|is_layer_skipped\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py | head -20"
}
```

> TOOL

tool_result Bash
```
43:    is_layer_skipped,
265:            if is_layer_skipped(
267:            ) or self.is_layer_excluded(prefix):
379:    def is_layer_excluded(self, prefix: str) -> bool:
1115:    def is_layer_excluded(self, prefix: str):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "offset": 375,
  "limit": 30
}
```

> TOOL

tool_result Read
```
375	            exclude_modules=exclude_modules,
376	            packed_modules_mapping=config.get("packed_modules_mapping"),
377	        )
378	
379	    def is_layer_excluded(self, prefix: str) -> bool:
380	        if len(self.exclude_modules) == 0:
381	            return False
382	        return any(
383	            module in prefix
384	            or (
385	                prefix.startswith("language_model.")
386	                and module in prefix.removeprefix("language_model.")
387	            )
388	            for module in self.exclude_modules
389	        )
390	
391	    def get_quant_method(
392	        self, layer: torch.nn.Module, prefix: str
393	    ) -> Optional[QuantizeMethodBase]:
394	        return self._get_quant_method(
395	            layer, prefix, Linear=ModelOptFp8LinearMethod, Moe=ModelOptFp8MoEMethod
396	        )
397	
398	
399	class ModelOptFp8LinearMethod(LinearMethodBase):
400	    """Linear method for ModelOpt static FP8 quantization.
401	
402	    Supports loading FP8 checkpoints with static weight and activation scales.
403	    Future support may include dynamic scales.
404	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the ColumnParallelLinear bias default and the training script:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class ColumnParallelLinear\\|def __init__\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/linear.py | head -30"
}
```

> TOOL

tool_result Bash
```
147:    def __init__(
189:    def __init__(
270:class ColumnParallelLinear(LinearBase):
294:    def __init__(
486:    def __init__(
801:    def __init__(
1245:    def __init__(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/linear.py",
  "offset": 294,
  "limit": 50
}
```

> TOOL

tool_result Read
```
294	    def __init__(
295	        self,
296	        input_size: int,
297	        output_size: int,
298	        bias: bool = True,
299	        gather_output: bool = False,
300	        skip_bias_add: bool = False,
301	        params_dtype: Optional[torch.dtype] = None,
302	        quant_config: Optional[QuantizationConfig] = None,
303	        output_sizes: Optional[List[int]] = None,
304	        prefix: str = "",
305	        tp_rank: Optional[int] = None,
306	        tp_size: Optional[int] = None,
307	        use_presharded_weights: bool = False,
308	        skip_block_quant_check: bool = False,
309	    ):
310	        super().__init__(
311	            input_size, output_size, skip_bias_add, params_dtype, quant_config, prefix
312	        )
313	
314	        self.gather_output = gather_output
315	        self.use_presharded_weights = use_presharded_weights
316	
317	        # Divide the weight matrix along the last dimension.
318	        if tp_rank is None:
319	            tp_rank = get_tensor_model_parallel_rank()
320	        if tp_size is None:
321	            tp_size = get_tensor_model_parallel_world_size()
322	        self.tp_rank, self.tp_size = tp_rank, tp_size
323	        assert self.quant_method is not None
324	        self.output_size_per_partition = divide(self.output_size, tp_size)
325	        self.output_partition_sizes = [self.output_size_per_partition]
326	        # If QKV or MergedColumn, use output size of each partition.
327	        if hasattr(self, "output_sizes"):
328	            self.output_partition_sizes = [
329	                divide(output_size, tp_size) for output_size in self.output_sizes
330	            ]
331	
332	        if output_sizes is None:
333	            output_sizes = [output_size]
334	
335	        self.quant_method.create_weights(
336	            layer=self,
337	            input_size_per_partition=self.input_size,
338	            output_partition_sizes=self.output_partition_sizes,
339	            input_size=self.input_size,
340	            output_size=self.output_size,
341	            params_dtype=self.params_dtype,
342	            skip_block_quant_check=skip_block_quant_check,
343	            weight_loader=(

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the training script and the hf_quant_config.json:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/train.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train EAGLE-3 draft model for MiniCPM-SALA speculative decoding.
4	
5	Architecture: fc(12288→4096) + 1 decoder layer (TTT 7-step) + norm + lm_head
6	Loss: plogp = -sum(target_p * log(draft_p)), weighted by 0.8^step
7	
8	Data: .pt files with {token_ids, aux_hidden, top_logit_values, top_logit_indices}
9	      aux_hidden = cat(layer1, layer10, layer22) of shape (seq_len, 12288)
10	
11	Run from repo user_4813494d:
12	    python3 eagle/train.py
13	"""
14	
15	import math
16	import os
17	import random
18	import time
19	from pathlib import Path
20	
21	import torch
22	import torch.nn as nn
23	import torch.nn.functional as F
24	from safetensors import safe_open
25	from tqdm import tqdm
26	
27	# ── Config ──────────────────────────────────────────────────────────────
28	DATA_DIR = Path("eagle/data/train")
29	VAL_IND_DIR = Path("eagle/data/val_ind")  # held-out slice of training distribution — monitor only
30	VAL_OOD_DIR = Path("eagle/data/val_ood")  # bench speed responses — OOD, drives ckpt selection
31	OUTPUT_DIR = Path("eagle/weights/v3")  # isolated from v2 best.pt + train_v2.log
32	MODEL_PATH = [REDACTED]
33	BF16_MODEL_PATH = [REDACTED]  # BF16 weights for MLP init
34	RESUME_CKPT = None  # 从头训（v2 数据分布变大，init_mlp_from_target 做 warm-start）
35	
36	# FP4 STE-QAT: train with FP4-quantized forward pass so weights are FP4-native
37	# at the end of training (no post-training quantization needed).
38	FP4_QAT = True
39	FP4_GROUP_SIZE = 16  # NVFP4 group size (16 weights share one FP8 scale)
40	TARGET_INIT_LAYER = 16  # target model layer to copy MLP/o_proj weights from
41	
42	HIDDEN_SIZE = 4096
43	AUX_DIM = HIDDEN_SIZE * 3  # 12288
44	VOCAB_SIZE = 73448
45	DRAFT_VOCAB_SIZE = 32000
46	SCALE_EMB = 12
47	SCALE_WIDTH = HIDDEN_SIZE / 256  # 16
48	NUM_HEADS = 32
49	NUM_KV_HEADS = 2
50	HEAD_DIM = 128
51	INTERMEDIATE_SIZE = 16384
52	RMS_NORM_EPS = 1e-6
53	
54	TTT_STEPS = 5  # v3: predict 5 steps; step 0 used for ckpt selection, 1..4 printed only
55	LOSS_DECAY = 0.8
56	SEQ_LEN = 2048
57	BATCH_SIZE = 6
58	GRAD_ACCUM = 2  # effective batch = 12 (v3: bigger than v2's 8, stabler grad on 60K)
59	LR = 3e-4
60	WARMUP_STEPS = 900  # v3: 6% of total_steps=14875 (matches v2 ratio)
61	WEIGHT_DECAY = 0.01
62	BETAS = (0.9, 0.95)
63	MAX_GRAD_NORM = 1.0
64	EPOCHS = 3  # v3: large data → small epoch; EARLY_STOP_PATIENCE disabled
65	EVAL_EVERY_EPOCH = 1
66	EARLY_STOP_PATIENCE = 99  # effectively disabled (EPOCHS=3 never triggers)
67	GRAD_CHECKPOINT = False  # 关：有充足显存（BS=4 peak 28.6 GB / 85 GB），换 bwd -35%
68	SEED = 42
69	MIN_TOKENS = 128  # skip files shorter than this
70	
71	DEVICE = "cuda"
72	DTYPE = torch.bfloat16
73	
74	# ── FP4 STE-QAT primitives ───────────────────────────────────────────────
75	# FP4 E2M1 positive values and their rounding boundaries
76	_FP4_POS = torch.tensor([0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0])
77	_FP4_BOUNDS = torch.tensor([0.25, 0.75, 1.25, 1.75, 2.5, 3.5, 5.0])
78	
79	
80	def _fp4_round(x: torch.Tensor) -> torch.Tensor:
81	    """Round each element to the nearest FP4 E2M1 representable value.
82	    Input: any float tensor (already in [-6, 6] range preferred).
83	    Output: same dtype, values in {0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}.
84	    """
85	    pos = _FP4_POS.to(device=x.device, dtype=x.dtype)
86	    bounds = _FP4_BOUNDS.to(device=x.device, dtype=x.dtype)
87	    sign = x.sign()
88	    idx = torch.bucketize(x.abs().clamp(max=6.0), bounds)
89	    return sign * pos[idx]
90	
91	
92	class _FP4QuantSTE(torch.autograd.Function):
93	    """Fake-quantize weight to FP4 E2M1 in forward; straight-through in backward.
94	
95	    Per-group-of-16 scaling: scale = max(|w_group|) / 6.0
96	    This matches NVFP4 group_size=16 used by the Marlin kernel.
97	    """
98	    @staticmethod
99	    def forward(ctx, weight: torch.Tensor) -> torch.Tensor:
100	        N, K = weight.shape
101	        w = weight.float()
102	        # Reshape into groups of FP4_GROUP_SIZE along K dimension
103	        w_g = w.reshape(N, K // FP4_GROUP_SIZE, FP4_GROUP_SIZE)
104	        # Per-group scale: max(|w|) / 6.0 (FP4 max magnitude is 6.0)
105	        scale = w_g.abs().amax(dim=-1, keepdim=True).clamp(min=1e-8) / 6.0
106	        # Quantize: scale → round to nearest FP4 → dequantize
107	        w_q = _fp4_round(w_g / scale) * scale
108	        return w_q.reshape(N, K).to(weight.dtype)
109	
110	    @staticmethod
111	    def backward(ctx, grad: torch.Tensor) -> torch.Tensor:
112	        return grad  # STE: pass gradient through unchanged
113	
114	
115	class FP4QATLinear(nn.Linear):
116	    """nn.Linear with FP4 fake-quantization on weights during training.
117	
118	    In training: forward uses FP4-rounded weights (STE for backward).
119	    In eval: forward uses raw weights (which are already FP4-grid-aligned
120	    after training, so final RTN export has near-zero error).
121	    Only applies when FP4_QAT=True; if False behaves as plain nn.Linear.
122	    """
123	    def forward(self, x: torch.Tensor) -> torch.Tensor:
124	        w = _FP4QuantSTE.apply(self.weight) if (self.training and FP4_QAT) else self.weight
125	        return F.linear(x, w, self.bias)
126	
127	
128	# ── RMSNorm ─────────────────────────────────────────────────────────────
129	class RMSNorm(nn.Module):
130	    def __init__(self, dim, eps=1e-6):
131	        super().__init__()
132	        self.weight = nn.Parameter(torch.ones(dim))
133	        self.eps = eps
134	
135	    def forward(self, x):
136	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
137	        return (x * norm).to(x.dtype) * self.weight
138	
139	
140	# ── RoPE helpers ────────────────────────────────────────────────────────
141	ROPE_THETA = 10000.0  # MiniCPM-SALA config.rope_theta
142	
143	def _build_rope_cache(head_dim, max_seq=SEQ_LEN * TTT_STEPS + 8192 + 64, theta=ROPE_THETA):
144	    inv_freq = 1.0 / (theta ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim))
145	    t = torch.arange(max_seq, dtype=torch.float32)
146	    freqs = torch.outer(t, inv_freq)  # (max_seq, head_dim/2)
147	    return torch.cos(freqs), torch.sin(freqs)  # each (max_seq, head_dim/2)
148	
149	def _apply_rotary_pos_emb(x, cos, sin, position_ids):
150	    """Apply neox-style RoPE to x: (B, num_heads, S, head_dim)."""
151	    # cos/sin: (max_seq, head_dim/2), position_ids: (B, S)
152	    cos_pos = cos[position_ids].unsqueeze(1)  # (B, 1, S, head_dim/2)
153	    sin_pos = sin[position_ids].unsqueeze(1)  # (B, 1, S, head_dim/2)
154	    x1 = x[..., :x.shape[-1] // 2]
155	    x2 = x[..., x.shape[-1] // 2:]
156	    return torch.cat([x1 * cos_pos - x2 * sin_pos,
157	                      x2 * cos_pos + x1 * sin_pos], dim=-1)
158	
159	
160	# ── Attention (list-based cache, matching official EAGLE-3 cnets.py L227-314) ──
161	class Eagle3Attention(nn.Module):
162	    """EAGLE-3 attention with list-based KV cache across TTT steps and RoPE."""
163	    def __init__(self):
164	        super().__init__()
165	        self.num_heads = NUM_HEADS
166	        self.num_kv_heads = NUM_KV_HEADS
167	        self.head_dim = HEAD_DIM
168	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
169	
170	        qkv_in = HIDDEN_SIZE * 2  # cat(embed, hidden)
171	        self.q_proj = FP4QATLinear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
172	        self.k_proj = FP4QATLinear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
173	        self.v_proj = FP4QATLinear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
174	        self.o_proj = FP4QATLinear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
175	
176	        # RoPE cache (precomputed cos/sin, moved to device on first forward)
177	        cos, sin = _build_rope_cache(HEAD_DIM)
178	        self.register_buffer("rope_cos", cos, persistent=False)
179	        self.register_buffer("rope_sin", sin, persistent=False)
180	
181	    def forward(self, hidden_cat, cache_k_list, cache_v_list, causal_mask=None, position_ids=None):
182	        """
183	        hidden_cat: (B, S, 2*H)
184	        cache_k_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
185	        cache_v_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
186	        causal_mask: (1, 1, S, S)
187	        position_ids: (B, S) — positions for RoPE; offset by cache length for multi-step
188	        Returns: output (B, S, H), new_cache_k_list, new_cache_v_list
189	        """
190	        B, S, _ = hidden_cat.shape
191	
192	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
193	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
194	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
195	
196	        # Apply RoPE to Q and K
197	        if position_ids is None:
198	            position_ids = torch.arange(S, device=hidden_cat.device).unsqueeze(0).expand(B, -1)
199	        q = _apply_rotary_pos_emb(q, self.rope_cos, self.rope_sin, position_ids)
200	        k = _apply_rotary_pos_emb(k, self.rope_cos, self.rope_sin, position_ids)

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the config and verify scale_emb handling:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/sglang_model_v3"
}
```

> TOOL

tool_result Read
```
EISDIR: illegal operation on a directory, read '/user_4813494d/openbmb/eagle/sglang_model_v3'
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/openbmb/eagle/sglang_model_v3/config.json"
}
```

> TOOL

tool_result Bash
```
{
  "architectures": [
    "LlamaForCausalLMEagle3"
  ],
  "model_type": "llama",
  "hidden_size": 4096,
  "intermediate_size": 16384,
  "num_hidden_layers": 1,
  "num_attention_heads": 32,
  "num_key_value_heads": 2,
  "head_dim": 128,
  "hidden_act": "silu",
  "max_position_embeddings": 524288,
  "rms_norm_eps": 1e-06,
  "vocab_size": 73448,
  "draft_vocab_size": 32000,
  "target_hidden_size": 4096,
  "scale_emb": 12,
  "tie_word_embeddings": false,
  "torch_dtype": "bfloat16",
  "eagle_config": {
    "use_aux_hidden_state": true,
    "eagle_aux_hidden_state_layer_ids": [
      4,
      9,
      24
    ]
  }
}
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/openbmb/eagle/sglang_model_v3/hf_quant_config.json"
}
```

> TOOL

tool_result Bash
```
{
  "producer": {
    "name": "eagle3-fp4-qat",
    "version": "1.0"
  },
  "quantization": {
    "quant_algo": "NVFP4",
    "kv_cache_quant_algo": null,
    "group_size": 16,
    "has_zero_point": false,
    "pre_quant_scale": false,
    "exclude_modules": [
      "model.fc"
    ]
  }
}
```

> AGENT

Now let me check the aux_hidden extraction and how it's used:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"aux_hidden\\|hidden_states\\|spec_info\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py"
}
```

> TOOL

tool_result Bash
```
79:        hidden_states: torch.Tensor,
84:        residual = hidden_states
86:        hidden_states = self.hidden_norm(hidden_states)
88:        hidden_states = torch.cat([embeds, hidden_states], dim=-1)
90:        hidden_states = self.self_attn(
92:            hidden_states=hidden_states,
96:        hidden_states, residual = self.post_attention_layernorm(hidden_states, residual)
99:        hidden_states = self.mlp(hidden_states)
101:        return hidden_states, residual
168:        hidden_states = forward_batch.spec_info.hidden_states
169:        if hidden_states.shape[-1] != embeds.shape[-1]:
171:            hidden_states, _ = self.fc(hidden_states)
174:        if hidden_states.shape[0] == 0:
175:            return hidden_states, [hidden_states]
178:        hidden_states, residual = self.midlayer(
181:            hidden_states,
186:        hidden_states_to_logits, hidden_states_to_aux = self.norm(
187:            hidden_states, residual
191:        return hidden_states_to_logits, [hidden_states_to_aux]
234:        self.capture_aux_hidden_states = True
```

> AGENT

Now let me check how lm_head is loaded and if it goes through NVFP4:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"lm_head\\|ParallelLMHead\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py"
}
```

> TOOL

tool_result Bash
```
35:    ParallelLMHead,
214:        self.load_lm_head_from_target = False
216:            self.lm_head = self.model.embed_tokens
219:                self.load_lm_head_from_target = True
221:            self.lm_head = ParallelLMHead(
225:                prefix=add_prefix("lm_head", prefix),
```

> AGENT

Let me check the fc layer loading behavior more carefully:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"model.fc\\|fc_out_features\\|hidden_size_in\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py"
}
```

> TOOL

tool_result Bash
```
131:            self.hidden_size_in = config.target_hidden_size
133:            self.hidden_size_in = config.hidden_size
138:            self.hidden_size_in * 3,
```

> AGENT

Now check the key part - how bias is handled in training vs deployment:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/train.py",
  "offset": 250,
  "limit": 100
}
```

> TOOL

tool_result Read
```
250	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
251	        return self.o_proj(attn_output), local_cache_k, local_cache_v
252	
253	
254	# ── MLP ──────────────────────────────────────────────────────────────────
255	class Eagle3MLP(nn.Module):
256	    def __init__(self):
257	        super().__init__()
258	        self.gate_proj = FP4QATLinear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
259	        self.up_proj = FP4QATLinear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
260	        self.down_proj = FP4QATLinear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
261	
262	    def forward(self, x):
263	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
264	
265	
266	# ── Decoder Layer ────────────────────────────────────────────────────────
267	class Eagle3DecoderLayer(nn.Module):
268	    def __init__(self):
269	        super().__init__()
270	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
271	        self.input_emb_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
272	        self.self_attn = Eagle3Attention()
273	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
274	        self.mlp = Eagle3MLP()
275	
276	    def forward(self, input_emb, hidden_states, cache_k_list=None, cache_v_list=None, causal_mask=None, position_ids=None):
277	        """
278	        input_emb: (B, S, H) - embedded tokens
279	        hidden_states: (B, S, H) - running hidden from fc or prior step
280	        cache_k_list, cache_v_list: list of tensors from prior TTT steps
281	        position_ids: (B, S) — positions for RoPE
282	        Returns: new_hidden (B, S, H), cache_k_list, cache_v_list
283	        """
284	        residual = hidden_states
285	
286	        normed_emb = self.input_emb_norm(input_emb)
287	        normed_hidden = self.hidden_norm(hidden_states)
288	        hidden_cat = torch.cat([normed_emb, normed_hidden], dim=-1)
289	
290	        attn_out, cache_k_list, cache_v_list = self.self_attn(hidden_cat, cache_k_list, cache_v_list, causal_mask, position_ids)
291	        hidden_states = residual + attn_out
292	
293	        residual = hidden_states
294	        hidden_states = self.post_attention_layernorm(hidden_states)
295	        hidden_states = self.mlp(hidden_states)
296	        hidden_states = residual + hidden_states
297	
298	        return hidden_states, cache_k_list, cache_v_list
299	
300	
301	# ── EAGLE-3 Draft Model ─────────────────────────────────────────────────
302	class Eagle3Model(nn.Module):
303	    def __init__(self, embed_weight, lm_head_weight):
304	        """
305	        embed_weight: (vocab_size, hidden_size) from target model
306	        lm_head_weight: (vocab_size, hidden_size) from target model
307	        """
308	        super().__init__()
309	        # v3: fc stays bf16 (no FP4 QAT) — aux_hidden is already NVFP4-stored,
310	        # fp4-quantizing fc on top would double-quantize the adapter.
311	        # deploy side (convert_to_sglang.py) also keeps fc bf16.
312	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
313	        self.midlayer = Eagle3DecoderLayer()
314	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
315	
316	        # Frozen embedding from target (with scale_emb)
317	        self.embed_tokens = nn.Embedding.from_pretrained(embed_weight, freeze=True)
318	        self.scale_emb = SCALE_EMB
319	
320	        # lm_head initialized from target (subset rows set in _init_lm_head)
321	        self.lm_head = FP4QATLinear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
322	        self._full_lm_head_weight = lm_head_weight  # kept for init after vocab mapping
323	
324	        # d2t / t2d / draft_idx_map mappings (set later via build_vocab_mapping)
325	        self.register_buffer("d2t", torch.zeros(DRAFT_VOCAB_SIZE, dtype=torch.long))
326	        self.register_buffer("t2d", torch.zeros(VOCAB_SIZE, dtype=torch.bool))
327	        self.register_buffer("draft_idx_map", torch.zeros(VOCAB_SIZE, dtype=torch.long))
328	
329	        self.ttt_steps = TTT_STEPS
330	        self.loss_decay = LOSS_DECAY
331	
332	    def build_vocab_mapping(self, data_dir):
333	        """Build draft vocabulary from training data token frequency."""
334	        cache_path = data_dir.parent / "vocab_cache.pt"
335	        if cache_path.exists():
336	            cache = torch.load(cache_path, weights_only=True)
337	            self.d2t.copy_(cache["d2t"])
338	            self.t2d.copy_(cache["t2d"])
339	            print(f"Loaded vocab mapping from {cache_path}")
340	        else:
341	            print("Building draft vocabulary from training data...")
342	            from collections import Counter
343	            counter = Counter()
344	            pt_files = sorted(data_dir.glob("*.pt"))
345	            for f in tqdm(pt_files, desc="scanning vocab"):
346	                d = torch.load(f, weights_only=True)
347	                ids = d["token_ids"].numpy()
348	                for tok in ids:
349	                    counter[int(tok)] += 1

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Let me check if there's missing key handling in weight loading:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"missing_keys\\|unexpected_keys\\|strict\\|load_state_dict\" /user_4813494d/openbmb/eagle/train.py | head -20"
}
```

> TOOL

tool_result Bash
```
852:        model.load_state_dict(raw_state, strict=False)
```

> AGENT

Now let me check the eagle_worker to understand how aux_hidden is extracted during inference:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"*eagle*worker*\" -o -name \"*eagle*info*\" | grep -v __pycache__ | grep sglang"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_info.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/test/speculative/test_eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/test/speculative/test_eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"eagle_aux_hidden_state_layer_ids\\|hidden_states\\|aux_hidden\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -30"
}
```

> TOOL

tool_result Bash
```
265:        self.eagle_use_aux_hidden_state = False
267:            self.eagle_use_aux_hidden_state = True
271:            self.eagle_use_aux_hidden_state = eagle_config.get(
272:                "use_aux_hidden_state", True
371:                    batch, logits_output.hidden_states, next_token_ids, seq_lens_cpu
593:        batch.return_hidden_states = False
622:        batch.return_hidden_states = False
734:        topk_p, topk_index, hidden_states = (
737:            spec_info.hidden_states,
757:            input_ids, hidden_states, scores, tree_info = select_top_k_tokens(
758:                i, topk_p, topk_index, hidden_states, scores, self.topk
781:            spec_info.hidden_states = hidden_states
793:            hidden_states = logits_output.hidden_states
822:        batch.return_hidden_states = False
878:        spec_info.hidden_states = logits_output.hidden_states
895:        logits_output.hidden_states = logits_output.hidden_states[res.accepted_indices]
932:                device=logits_output.hidden_states.device,
1118:        hidden_states: torch.Tensor,
1126:            hidden_states: Hidden states from the target model forward
1130:            hidden_states=hidden_states,
1135:        batch.return_hidden_states = False
1165:                and self.eagle_use_aux_hidden_state
1209:        batch.return_hidden_states = False
1233:            forward_batch.spec_info.hidden_states = logits_output.hidden_states
1267:        draft_input.hidden_states = logits_output.hidden_states
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1100,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1100	            torch.cuda.nvtx.range_push("asp_k2_alloc")
1101	            k2_loc_all = alloc_token_slots(batch.tree_cache, total_k2).to(torch.int32)
1102	            torch.cuda.nvtx.range_pop()
1103	            torch.cuda.nvtx.range_push("asp_k2_writes")
1104	            pt = 0
1105	            for i in range(bs):
1106	                cnt = k2_count[i]
1107	                if cnt > 0:
1108	                    rtp.write_sparse_k2(
1109	                        (batch.req_pool_indices[i], slice(k2_first[i], k2_first[i] + cnt)),
1110	                        k2_loc_all[pt : pt + cnt],
1111	                    )
1112	                    pt += cnt
1113	            torch.cuda.nvtx.range_pop()
1114	
1115	    def forward_draft_extend(
1116	        self,
1117	        batch: ScheduleBatch,
1118	        hidden_states: torch.Tensor,
1119	        next_token_ids: torch.Tensor,
1120	        seq_lens_cpu: Optional[torch.Tensor],
1121	    ):
1122	        """Run draft model extend. This API modifies the states of the batch.
1123	
1124	        Args:
1125	            batch: The batch to run.
1126	            hidden_states: Hidden states from the target model forward
1127	            next_token_ids: Next token ids generated from the target forward.
1128	        """
1129	        batch.spec_info = EagleDraftInput(
1130	            hidden_states=hidden_states,
1131	            verified_id=next_token_ids,
1132	            num_tokens_per_batch=1,
1133	            num_tokens_for_logprob_per_batch=1,
1134	        )
1135	        batch.return_hidden_states = False
1136	        batch.spec_info.prepare_for_extend(batch)
1137	        batch.spec_info.capture_hidden_mode = CaptureHiddenMode.LAST
1138	        model_worker_batch = batch.get_model_worker_batch(
1139	            seq_lens_cpu_cache=seq_lens_cpu
1140	        )
1141	        forward_batch = ForwardBatch.init_new(
1142	            model_worker_batch, self.draft_model_runner
1143	        )
1144	        forward_batch.return_logprob = False
1145	        logits_output = self.draft_model_runner.forward(forward_batch).logits_output
1146	        if self.enable_nan_detection:
1147	            detect_nan(logits_output)
1148	        assert isinstance(forward_batch.spec_info, EagleDraftInput)
1149	        assert forward_batch.spec_info is batch.spec_info
1150	        self.capture_for_decode(logits_output, forward_batch.spec_info)
1151	
1152	    def forward_draft_extend_after_decode(self, batch: ScheduleBatch):
1153	        assert isinstance(batch.spec_info, EagleDraftInput)
1154	        original_batch = batch
1155	        input_is_idle = batch.forward_mode.is_idle()
1156	        using_temp_batch = False
1157	
1158	        if not input_is_idle and batch.spec_info.verified_id.numel() == 0:
1159	            batch = batch.copy()
1160	            using_temp_batch = True
1161	            batch.prepare_for_idle()
1162	            hidden_size = (
1163	                self.model_config.hidden_size * 3
1164	                if self.speculative_algorithm.is_eagle3()
1165	                and self.eagle_use_aux_hidden_state
1166	                else self.model_config.hidden_size
1167	            )
1168	            batch.spec_info = EagleDraftInput.create_idle_input(
1169	                device=self.device,
1170	                hidden_size=hidden_size,
1171	                dtype=self.model_config.dtype,
1172	                topk=self.topk,
1173	                capture_hidden_mode=CaptureHiddenMode.LAST,
1174	            )
1175	        elif (
1176	            not input_is_idle
1177	            and batch.spec_info.request_keep_indices is not None
1178	            and len(batch.spec_info.request_keep_indices) != len(batch.reqs)
1179	        ):
1180	            batch = copy(batch)
1181	            using_temp_batch = True
1182	            batch.spec_info = copy(batch.spec_info)
1183	            batch.spec_info.accept_length = batch.spec_info.accept_length.clone()
1184	            batch.spec_info.align_batch_for_draft_extend(batch)
1185	            batch.sampling_info = SamplingBatchInfo.from_schedule_batch(
1186	                batch, batch.model_config.vocab_size
1187	            )
1188	
1189	        if not using_temp_batch:
1190	            # Backup fields that will be modified in-place
1191	            seq_lens_backup = batch.seq_lens.clone()
1192	            seq_lens_cpu_backup = batch.seq_lens_cpu.clone()
1193	            req_pool_indices_backup = batch.req_pool_indices
1194	            accept_length_backup = batch.spec_info.accept_length
1195	            return_logprob_backup = batch.return_logprob
1196	
1197	        batch.spec_info.num_tokens_per_batch = self.speculative_num_steps + 1
1198	        batch.spec_info.num_tokens_for_logprob_per_batch = 1
1199	        batch.spec_info.prepare_extend_after_decode(
1200	            batch,
1201	            self.speculative_num_steps,
1202	        )
1203	        batch.forward_mode = (
1204	            ForwardMode.DRAFT_EXTEND
1205	            if not batch.forward_mode.is_idle()
1206	            else ForwardMode.IDLE
1207	        )
1208	
1209	        batch.return_hidden_states = False
1210	        model_worker_batch = batch.get_model_worker_batch()
1211	        assert model_worker_batch.capture_hidden_mode == CaptureHiddenMode.LAST
1212	        forward_batch = ForwardBatch.init_new(
1213	            model_worker_batch, self.draft_model_runner
1214	        )
1215	        if forward_batch.seq_lens_cpu is not None:
1216	            forward_batch.seq_lens_sum = forward_batch.seq_lens_cpu.sum().item()
1217	        else:
1218	            forward_batch.seq_lens_sum = batch.seq_lens.sum().item()
1219	
1220	        # Run
1221	        can_cuda_graph = (
1222	            self.cuda_graph_runner_for_draft_extend
1223	            and self.cuda_graph_runner_for_draft_extend.can_run(forward_batch)
1224	        )
1225	        if can_cuda_graph:
1226	            logits_output = self.cuda_graph_runner_for_draft_extend.replay(
1227	                forward_batch
1228	            )
1229	            forward_batch.spec_info.topk_p, forward_batch.spec_info.topk_index = (
1230	                logits_output.topk_p,
1231	                logits_output.topk_index,
1232	            )
1233	            forward_batch.spec_info.hidden_states = logits_output.hidden_states
1234	        else:
1235	            forward_batch.can_run_dp_cuda_graph = False
1236	            if not forward_batch.forward_mode.is_idle():
1237	                self.draft_model_runner.attn_backend.init_forward_metadata(
1238	                    forward_batch
1239	                )
1240	            logits_output = self.draft_model_runner.forward(
1241	                forward_batch, skip_attn_backend_init=True
1242	            ).logits_output
1243	            self.capture_for_decode(logits_output, forward_batch.spec_info)
1244	
1245	        if self.enable_nan_detection:
1246	            detect_nan(logits_output)
1247	
1248	        if using_temp_batch:
1249	            original_batch.spec_info = batch.spec_info

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Let me check eagle_info to see how aux_hidden is extracted from layer outputs:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"eagle_aux_hidden_state_layer_ids\\|concat\\|cat\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py | head -20"
}
```

> TOOL

tool_result Bash
```
35:from sglang.srt.mem_cache.allocator import BaseTokenToKVPoolAllocator
220:            self.custom_mask = torch.cat(
239:        token_to_kv_pool_allocator: BaseTokenToKVPoolAllocator,
326:                "Falling back to greedy verification."
531:            token_to_kv_pool_allocator.free(batch.out_cache_loc[evict_mask])
534:                req.kv_allocated_len = req.kv_committed_len
545:                token_to_kv_pool_allocator.free(batch.out_cache_loc[evict_mask])
548:                    req.kv_allocated_len = req.kv_committed_len
587:                token_to_kv_pool_allocator.free(to_free_slots)
590:                batch.token_to_kv_pool_allocator.get_kvcache().move_kv_cache(
647:                unfinished_accept_index = torch.cat(unfinished_accept_index)
767:            batch.input_ids[pt : pt + extend_len] = torch.cat(
996:                indices=torch.cat(
1010:        self.hidden_states = torch.cat(
1013:        self.verified_id = torch.cat([self.verified_id, spec_info.verified_id], axis=0)
1014:        self.topk_p = torch.cat([self.topk_p, spec_info.topk_p])
1015:        self.topk_index = torch.cat([self.topk_index, spec_info.topk_index])
1036:    Unlike EAGLE's tree-based verification, Medusa uses flat (sequential)
1069:        """Set up batch for TARGET_VERIFY: allocate cache slots, set positions."""
1076:        # Allocate KV cache slots for all draft_token_num tokens per request
```

> AGENT

Let me search for where hidden_states is extracted from layer_ids:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"layer_ids\\|hidden_states\\[\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py | head -40"
}
```

> TOOL

tool_result Bash
```
616:                hidden_states=batch.spec_info.hidden_states[accept_index],
678:                    hidden_states=batch.spec_info.hidden_states[
983:            self.hidden_states = self.hidden_states[: len(new_indices)]
989:            self.hidden_states = self.hidden_states[new_indices]
```

> AGENT

Let me search in the model runner or forward batch to see how aux_hidden concatenation happens:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang -name \"*.py\" -exec grep -l \"eagle_aux_hidden_state_layer_ids\" {} \\;"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/cuda_graph_runner.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"eagle_aux_hidden_state_layer_ids\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py -A 10 -B 5"
}
```

> TOOL

tool_result Bash
```
333-                    draft_model_config.hf_config, "eagle_config", None
334-                )
335-                self.eagle_use_aux_hidden_state = eagle_config.get(
336-                    "use_aux_hidden_state", True
337-                )
338:                self.eagle_aux_hidden_state_layer_ids = eagle_config[
339:                    "eagle_aux_hidden_state_layer_ids"
340-                ]
341-            except:
342-                # if there is no aux layer, set to None
343:                self.eagle_aux_hidden_state_layer_ids = None
344-
345-        # Apply the rank zero filter to logger
346-        if server_args.show_time_cost:
347-            enable_show_time_cost()
348-
349-        # Model-specific adjustment
350-        self.model_specific_adjustment()
351-
352-        # Set the global server_args in the scheduler process
353-        set_global_server_args_for_scheduler(server_args)
--
577-        if server_args.forward_hooks:
578-            register_forward_hooks(self.model, server_args.forward_hooks)
579-
580-        if self.eagle_use_aux_hidden_state:
581-            self.model.set_eagle3_layers_to_capture(
582:                self.eagle_aux_hidden_state_layer_ids
583-            )
584-
585-        # Initialize piecewise CUDA graph
586-        self.init_piecewise_cuda_graphs()
587-
588-    def init_routed_experts_capturer(self):
589-        if not self.server_args.disable_shared_experts_fusion and hasattr(
590-            self.model, "num_fused_shared_experts"
591-        ):
592-            num_fused_shared_experts = self.model.num_fused_shared_experts
--
1745-        if self.server_args.enable_torch_compile:
1746-            set_torch_compile_config()
1747-
1748-        if self.eagle_use_aux_hidden_state:
1749-            self.model.set_eagle3_layers_to_capture(
1750:                self.eagle_aux_hidden_state_layer_ids
1751-            )
1752-
1753-        require_mlp_tp_gather_ = require_mlp_tp_gather(self.server_args)
1754-        if require_gathered_buffer(self.server_args):
1755-            assert require_mlp_tp_gather_ or require_attn_tp_gather(self.server_args)
1756-
1757-        buffers: GraphInputBuffers = GraphInputBuffers.create(
1758-            device=self.device,
1759-            max_bs=batch_size,
1760-            max_num_token=num_tokens,
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"set_eagle3_layers_to_capture\\|capture_eagle3_hidden_states\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt -r | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py:581:            self.model.set_eagle3_layers_to_capture(
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py:1749:            self.model.set_eagle3_layers_to_capture(
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/cuda_graph_runner.py:371:            self.model_runner.model.set_eagle3_layers_to_capture(
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/apertus.py:670:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/deepseek_v2.py:3741:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/gpt_oss.py:1094:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/glm4_moe.py:1256:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen2_5_vl.py:868:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/mllama4.py:953:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/mllama4.py:954:        if hasattr(self.language_model, "set_eagle3_layers_to_capture"):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/mllama4.py:955:            self.language_model.set_eagle3_layers_to_capture(layer_ids)
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/longcat_flash.py:1044:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py:767:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/minimax_m2.py:955:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[list[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/mimo_v2_flash.py:672:    def set_eagle3_layers_to_capture(self, layers_to_capture: List[int]):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen2_moe.py:596:    def set_eagle3_layers_to_capture(self, layers_to_capture: List[int]):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen2_moe.py:873:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen2_moe.py:880:            self.model.set_eagle3_layers_to_capture(
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen2_moe.py:888:            self.model.set_eagle3_layers_to_capture([val + 1 for val in layer_ids])
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/qwen3.py:576:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py",
  "offset": 767,
  "limit": 100
}
```

> TOOL

tool_result Read
```
767	    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
768	        if not self.pp_group.is_last_rank:
769	            return
770	
771	        if layer_ids is None:
772	            self.capture_aux_hidden_states = True
773	            num_layers = self.config.num_hidden_layers
774	            self.model.layers_to_capture = [2, num_layers // 2, num_layers - 3]
775	        else:
776	            self.capture_aux_hidden_states = True
777	            # we plus 1 here because in sglang, for the ith layer, it takes the output
778	            # of the (i-1)th layer as aux hidden state
779	            self.model.layers_to_capture = [val + 1 for val in layer_ids]
780	
781	
782	class Phi3ForCausalLM(LlamaForCausalLM):
783	    pass
784	
785	
786	class InternLM3ForCausalLM(LlamaForCausalLM):
787	    pass
788	
789	
790	EntryClass = [LlamaForCausalLM, Phi3ForCausalLM, InternLM3ForCausalLM]
791	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Critical! Let me verify how the hidden states are concatenated:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"layers_to_capture\\|capture_eagle3\\|concat.*hidden\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py | head -30"
}
```

> TOOL

tool_result Bash
```
346:        self.layers_to_capture = []
371:            if i in self.layers_to_capture:
767:    def set_eagle3_layers_to_capture(self, layer_ids: Optional[List[int]] = None):
774:            self.model.layers_to_capture = [2, num_layers // 2, num_layers - 3]
779:            self.model.layers_to_capture = [val + 1 for val in layer_ids]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py",
  "offset": "\\1",
  "limit": 100
}
```

> TOOL

tool_result Read
```
<tool_use_error>InputValidationError: Read failed due to the following issue:
The parameter `offset` type is expected as `number` but provided as `string`</tool_use_error>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py",
  "offset": 340,
  "limit": 80
}
```

> TOOL

tool_result Read
```
340	        )
341	
342	        if self.pp_group.is_last_rank:
343	            self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
344	        else:
345	            self.norm = PPMissingLayer(return_tuple=True)
346	        self.layers_to_capture = []
347	
348	    def forward(
349	        self,
350	        input_ids: torch.Tensor,
351	        positions: torch.Tensor,
352	        forward_batch: ForwardBatch,
353	        input_embeds: torch.Tensor = None,
354	        pp_proxy_tensors: Optional[PPProxyTensors] = None,
355	    ) -> Union[torch.Tensor, Tuple[torch.Tensor, List[torch.Tensor]], PPProxyTensors]:
356	        if self.pp_group.is_first_rank:
357	            if input_embeds is None:
358	                hidden_states = self.embed_tokens(input_ids)
359	            else:
360	                hidden_states = input_embeds
361	            residual = None
362	        else:
363	            assert pp_proxy_tensors is not None
364	            # FIXME(@ying): reduce the number of proxy tensors by not fusing layer norms
365	            hidden_states = pp_proxy_tensors["hidden_states"]
366	            residual = pp_proxy_tensors["residual"]
367	            deferred_norm = None
368	
369	        aux_hidden_states = []
370	        for i in range(self.start_layer, self.end_layer):
371	            if i in self.layers_to_capture:
372	                aux_hidden_states.append(hidden_states + residual)
373	            layer = self.layers[i]
374	            hidden_states, residual = layer(
375	                positions,
376	                hidden_states,
377	                forward_batch,
378	                residual,
379	            )
380	
381	        if not self.pp_group.is_last_rank:
382	            return PPProxyTensors(
383	                {
384	                    "hidden_states": hidden_states,
385	                    "residual": residual,
386	                }
387	            )
388	        else:
389	            hidden_states, _ = self.norm(hidden_states, residual)
390	
391	        if len(aux_hidden_states) == 0:
392	            return hidden_states
393	
394	        return hidden_states, aux_hidden_states
395	
396	    # If this function is called, it should always initialize KV cache scale
397	    # factors (or else raise an exception). Thus, handled exceptions should
398	    # make sure to leave KV cache scale factors in a known good (dummy) state
399	    def load_kv_cache_scales(self, quantization_param_path: str) -> None:
400	        tp_size = get_tensor_model_parallel_world_size()
401	        tp_rank = get_tensor_model_parallel_rank()
402	        for layer_idx, scaling_factor in kv_cache_scales_loader(
403	            quantization_param_path,
404	            tp_rank,
405	            tp_size,
406	            self.config.num_hidden_layers,
407	            self.config.__class__.model_type,
408	        ):
409	            if not isinstance(self.layers[layer_idx], nn.Identity):
410	                layer_self_attn = self.layers[layer_idx].self_attn
411	
412	            if hasattr(layer_self_attn.attn, "k_scale"):
413	                layer_self_attn.attn.k_scale = scaling_factor
414	                layer_self_attn.attn.v_scale = scaling_factor
415	            else:
416	                raise RuntimeError(
417	                    "Self attention has no KV cache scaling " "factor attribute!"
418	                )
419	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check how the aux_hidden_states list is then processed in forward_batch:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"aux_hidden_states\\|logits_output\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/forward_batch_info.py | head -30"
}
```

> TOOL

tool_result Bash
```
1028:    def post_forward_mlp_sync_batch(self, logits_output: LogitsProcessorOutput):
1042:                logits_output.next_token_logits = logits_output.next_token_logits[
1045:                logits_output.hidden_states = logits_output.hidden_states[:num_tokens]
1048:                logits_output.next_token_logits = logits_output.next_token_logits[
1051:                logits_output.hidden_states = logits_output.hidden_states[:num_tokens]
1054:                logits_output.next_token_logits = logits_output.next_token_logits[:bs]
1055:                logits_output.hidden_states = logits_output.hidden_states[:bs]
1058:                logits_output.next_token_logits = logits_output.next_token_logits[:bs]
1059:                logits_output.hidden_states = logits_output.hidden_states[:bs]
1061:                logits_output.next_token_logits = logits_output.next_token_logits[:bs]
1062:                logits_output.hidden_states = logits_output.hidden_states[:bs]
1070:            logits_output.next_token_logits = logits_output.next_token_logits[:bs]
1071:            if logits_output.hidden_states is not None:
1072:                logits_output.hidden_states = logits_output.hidden_states[:bs]
1075:            logits_output.next_token_logits = logits_output.next_token_logits[
1078:            if logits_output.hidden_states is not None:
1079:                logits_output.hidden_states = logits_output.hidden_states[:num_tokens]
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def .*logits_output\\|hidden_states\\s*=\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py | grep -A 5 -B 5 \"aux\\|eagle\\|concat\" | head -50"
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
  "command": "grep -n \"hidden_states.*concat\\|torch.cat.*hidden\\|torch.cat.*aux\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py"
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
  "command": "grep -n \"aux_hidden\\|eagle.*hidden\\|hidden_states.*cat\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py | head -30"
}
```

> TOOL

tool_result Bash
```
319:        self.eagle_use_aux_hidden_state = False
328:            self.eagle_use_aux_hidden_state = True
335:                self.eagle_use_aux_hidden_state = eagle_config.get(
336:                    "use_aux_hidden_state", True
338:                self.eagle_aux_hidden_state_layer_ids = eagle_config[
339:                    "eagle_aux_hidden_state_layer_ids"
343:                self.eagle_aux_hidden_state_layer_ids = None
580:        if self.eagle_use_aux_hidden_state:
582:                self.eagle_aux_hidden_state_layer_ids
1748:        if self.eagle_use_aux_hidden_state:
1750:                self.eagle_aux_hidden_state_layer_ids
```

> AGENT

Let me search for where logits_output is created in forward:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class.*LogitsProcessorOutput\\|hidden_states =\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/logits_processor.py | head -30"
}
```

> TOOL

tool_result Bash
```
66:class LogitsProcessorOutput:
538:                    aux_hidden_states = torch.cat(aux_hidden_states, dim=-1)
860:            hidden_states, local_hidden_states = (
```

> AGENT

Found it! Let me check line 538:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/logits_processor.py",
  "offset": 530,
  "limit": 50
}
```

> TOOL

tool_result Read
```
530	            else None
531	        )
532	
533	        hidden_states_to_store: Optional[torch.Tensor] = None
534	        hidden_states_to_store_before_norm: Optional[torch.Tensor] = None
535	        if logits_metadata.capture_hidden_mode.need_capture():
536	            if logits_metadata.capture_hidden_mode.is_full():
537	                if aux_hidden_states is not None:
538	                    aux_hidden_states = torch.cat(aux_hidden_states, dim=-1)
539	                    hidden_states_to_store = aux_hidden_states
540	                else:
541	                    hidden_states_to_store = hidden_states
542	                hidden_states_to_store_before_norm = hidden_states_before_norm
543	            elif logits_metadata.capture_hidden_mode.is_last():
544	                # Get the last token hidden states. If sample_indices is None,
545	                # pruned states only contain the last tokens already.
546	                if aux_hidden_states is not None:
547	                    aux_pruned_states = torch.cat(aux_pruned_states, dim=-1)
548	                    hidden_states_to_store = (
549	                        aux_pruned_states[sample_indices]
550	                        if sample_indices is not None
551	                        else aux_pruned_states
552	                    )
553	                else:
554	                    hidden_states_to_store = (
555	                        pruned_states[sample_indices]
556	                        if sample_indices is not None
557	                        else pruned_states
558	                    )
559	                    if hidden_states_before_norm is not None:
560	                        hidden_states_to_store_before_norm = (
561	                            pruned_states_before_norm[sample_indices]
562	                            if sample_indices is not None
563	                            else pruned_states_before_norm
564	                        )
565	            else:
566	                assert False, "Should never reach"
567	
568	        del hidden_states
569	
570	        if hidden_states_to_store_before_norm is not None:
571	            # NOTE: when hidden_states_before_norm is provided, we always
572	            # prefer to return it.
573	            hidden_states_to_store = hidden_states_to_store_before_norm
574	
575	        if not logits_metadata.extend_return_logprob:
576	            # Compute logits for both input and sampled tokens.
577	            logits = self._get_logits(pruned_states, lm_head, logits_metadata)
578	            sampled_logits = (
579	                logits[sample_indices] if sample_indices is not None else logits

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me check if the concatenation order preserves the order of layer_ids. Let me also check for potential issues with dtype:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/logits_processor.py",
  "offset": 480,
  "limit": 60
}
```

> TOOL

tool_result Read
```
480	                    logits_metadata.extend_logprob_start_lens_cpu,
481	                    logits_metadata.extend_seq_lens_cpu,
482	                )
483	            ):
484	                # It can happen in chunked prefill. We still need to sample 1 token,
485	                # But we don't want to include it in input logprob.
486	                if extend_len == extend_logprob_start_len:
487	                    start_len = extend_logprob_start_len - 1
488	                else:
489	                    start_len = extend_logprob_start_len
490	
491	                # We always need at least 1 token to sample because that's required
492	                # by a caller.
493	                assert extend_len > start_len
494	                pruned_states_list.append(
495	                    hidden_states[pt + start_len : pt + extend_len]
496	                )
497	                if hidden_states_before_norm is not None:
498	                    pruned_states_before_norm_list.append(
499	                        hidden_states_before_norm[pt + start_len : pt + extend_len]
500	                    )
501	                # Map each token to its sequence index, for chunked computation
502	                # of input logprobs
503	                token_to_seq_idx.extend([idx] * (extend_len - start_len))
504	                pt += extend_len
505	                sample_index_pt += extend_len - start_len
506	                sample_indices.append(sample_index_pt)
507	                input_logprob_indices.extend(
508	                    [
509	                        input_logprob_indices_pt + i
510	                        for i in range(extend_len - extend_logprob_start_len)
511	                    ]
512	                )
513	                input_logprob_indices_pt += extend_len - start_len
514	
515	            # Set the last token of the last sequence
516	            token_to_seq_idx.append(len(logits_metadata.extend_seq_lens_cpu) - 1)
517	            pruned_states = torch.cat(pruned_states_list)
518	            if hidden_states_before_norm is not None:
519	                pruned_states_before_norm = torch.cat(pruned_states_before_norm_list)
520	            sample_indices = torch.tensor(
521	                sample_indices, device=pruned_states.device, dtype=torch.int64
522	            )
523	            input_logprob_indices = torch.tensor(
524	                input_logprob_indices, device=pruned_states.device, dtype=torch.int64
525	            )
526	
527	        full_logits = (
528	            self._get_logits(hidden_states, lm_head, logits_metadata)
529	            if self.return_full_logits
530	            else None
531	        )
532	
533	        hidden_states_to_store: Optional[torch.Tensor] = None
534	        hidden_states_to_store_before_norm: Optional[torch.Tensor] = None
535	        if logits_metadata.capture_hidden_mode.need_capture():
536	            if logits_metadata.capture_hidden_mode.is_full():
537	                if aux_hidden_states is not None:
538	                    aux_hidden_states = torch.cat(aux_hidden_states, dim=-1)
539	                    hidden_states_to_store = aux_hidden_states

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check what dtype the aux_hidden comes in:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/logits_processor.py",
  "offset": 420,
  "limit": 70
}
```

> TOOL

tool_result Read
```
420	        elif (
421	            logits_metadata.forward_mode.is_extend()
422	            and not logits_metadata.extend_return_logprob
423	        ):
424	            # Prefill without input logprobs.
425	            if logits_metadata.padded_static_len < 0:
426	                last_index = torch.cumsum(logits_metadata.extend_seq_lens, dim=0) - 1
427	            else:
428	                # If padding_static length is 5 and extended_seq_lens is [2, 3],
429	                # then our batch looks like [t00, t01, p, p, p, t10, t11, t12, p, p]
430	                # and this retrieves t01 and t12, which are the valid last tokens
431	                idx = torch.arange(
432	                    len(logits_metadata.extend_seq_lens),
433	                    device=logits_metadata.extend_seq_lens.device,
434	                )
435	                last_index = (
436	                    idx * logits_metadata.padded_static_len
437	                    + logits_metadata.extend_seq_lens
438	                    - 1
439	                )
440	            pruned_states = hidden_states[last_index]
441	            if hidden_states_before_norm is not None:
442	                pruned_states_before_norm = hidden_states_before_norm[last_index]
443	            if aux_hidden_states is not None:
444	                aux_pruned_states = [hidden[last_index] for hidden in aux_hidden_states]
445	            sample_indices = None
446	            input_logprob_indices = None
447	        else:
448	            # Prefill with input logprobs.
449	            # Find 4 different indices.
450	            # 1. pruned_states: hidden states that we want logprobs from.
451	            # 2. sample_indices: Indices that have sampled tokens.
452	            # 3. input_logprob_indices: Indices that have input logprob tokens.
453	            # 4. token_to_seq_idx: map each token to its sequence index
454	            #
455	            # Example
456	            # -------
457	            # Suppose a batch (flattened by sequence):
458	            # [t00, t01, t02, t03, t10, t11, t12, t13, t14, t20, t21, t22, t23, t24, t25]
459	            # extend_seq_lens_cpu           = [4, 5, 6]
460	            # extend_logprob_start_lens_cpu = [0, 5, 3]
461	            #
462	            # Then, the indices are:
463	            # pruned_states         -> [t00, t01, t02, t03, t14, t23, t24, t25]
464	            # sample_indices        -> [3, 4, 7]
465	            # input_logprob_indices -> [0, 1, 2, 3, 5, 6, 7]
466	            # token_to_seq_idx      -> [0, 0, 0, 0, 1, 2, 2, 2]
467	            #
468	            # If chunk is enabled and chunk_size = 3, the chunks will be computed in a chunked manner:
469	            # [t00, t01, t02], [t03, t14, t23], [t24, t25]
470	
471	            sample_index_pt = -1
472	            sample_indices = []
473	            input_logprob_indices_pt = 0
474	            input_logprob_indices = []
475	            pt, pruned_states_list, pruned_states_before_norm_list = 0, [], []
476	            token_to_seq_idx = []
477	
478	            for idx, (extend_logprob_start_len, extend_len) in enumerate(
479	                zip(
480	                    logits_metadata.extend_logprob_start_lens_cpu,
481	                    logits_metadata.extend_seq_lens_cpu,
482	                )
483	            ):
484	                # It can happen in chunked prefill. We still need to sample 1 token,
485	                # But we don't want to include it in input logprob.
486	                if extend_len == extend_logprob_start_len:
487	                    start_len = extend_logprob_start_len - 1
488	                else:
489	                    start_len = extend_logprob_start_len

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the fc layer in llama_eagle3 to verify bias handling:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py",
  "offset": 135,
  "limit": 15
}
```

> TOOL

tool_result Read
```
135	        # Use ColumnParallelLinear (supports quant_config) instead of plain Linear
136	        # so NVFP4 / Marlin quantization applies to fc as well.
137	        self.fc = ColumnParallelLinear(
138	            self.hidden_size_in * 3,
139	            config.hidden_size,
140	            bias=getattr(config, "bias", False),
141	            quant_config=quant_config,
142	            prefix=add_prefix("fc", prefix),
143	        )
144	
145	        self.midlayer = LlamaDecoderLayer(config, 0, quant_config, prefix)
146	
147	        self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
148	
149	        # MiniCPM-style scale_emb (default 1.0 for standard Llama)

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Good! Now let me check safetensors to see what's actually in there:

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"from safetensors.torch import safe_open; f = safe_open('/user_4813494d/openbmb/eagle/sglang_model_v3/model.safetensors', framework='pt', device='cpu'); print('Keys:', sorted(f.keys()))\" 2>/dev/null | head -50"
}
```

> TOOL

tool_result Bash
```
Keys: ['d2t', 'lm_head.weight', 'model.fc.weight', 'model.midlayer.hidden_norm.weight', 'model.midlayer.input_layernorm.weight', 'model.midlayer.mlp.down_proj.input_scale', 'model.midlayer.mlp.down_proj.weight', 'model.midlayer.mlp.down_proj.weight_scale', 'model.midlayer.mlp.down_proj.weight_scale_2', 'model.midlayer.mlp.gate_up_proj.input_scale', 'model.midlayer.mlp.gate_up_proj.weight', 'model.midlayer.mlp.gate_up_proj.weight_scale', 'model.midlayer.mlp.gate_up_proj.weight_scale_2', 'model.midlayer.post_attention_layernorm.weight', 'model.midlayer.self_attn.o_proj.input_scale', 'model.midlayer.self_attn.o_proj.weight', 'model.midlayer.self_attn.o_proj.weight_scale', 'model.midlayer.self_attn.o_proj.weight_scale_2', 'model.midlayer.self_attn.qkv_proj.input_scale', 'model.midlayer.self_attn.qkv_proj.weight', 'model.midlayer.self_attn.qkv_proj.weight_scale', 'model.midlayer.self_attn.qkv_proj.weight_scale_2', 'model.norm.weight']
```

> AGENT

Perfect! Now let me check if there are issues with the fc layer in exclude_modules matching:

> TOOL

tool_use Bash
```json
{
  "command": "python3 << 'EOF'\n# Test the is_layer_excluded logic from modelopt_quant.py\nexclude_modules = [\"model.fc\"]\n\ndef is_layer_excluded(prefix: str) -> bool:\n    if len(exclude_modules) == 0:\n        return False\n    return any(\n        module in prefix\n        or (\n            prefix.startswith(\"language_model.\")\n            and module in prefix.removeprefix(\"language_model.\")\n        )\n        for module in exclude_modules\n    )\n\n# Test with actual draft model prefixes\ntest_prefixes = [\n    \"model.fc\",\n    \"model.fc.weight\",\n    \"model.fc.weight_scale\",\n    \"model.fc.input_scale\",\n]\n\nfor prefix in test_prefixes:\n    result = is_layer_excluded(prefix)\n    print(f\"is_layer_excluded('{prefix}') = {result}\")\nEOF\n"
}
```

> TOOL

tool_result Bash
```
is_layer_excluded('model.fc') = True
is_layer_excluded('model.fc.weight') = True
is_layer_excluded('model.fc.weight_scale') = True
is_layer_excluded('model.fc.input_scale') = True
```

> AGENT

Excellent! Now let me verify the fc layer will not have bias loaded and check the actual layer instantiation:

> TOOL

tool_use Bash
```json
{
  "command": "python3 << 'EOF'\nimport json\n\n# Load config\nwith open('/user_4813494d/openbmb/eagle/sglang_model_v3/config.json') as f:\n    config = json.load(f)\n\n# Check if bias is defined in config\nhas_bias_key = \"bias\" in config\nbias_value = config.get(\"bias\", \"NOT SET (defaults to False)\")\n\nprint(f\"Config has 'bias' key: {has_bias_key}\")\nprint(f\"bias value: {bias_value}\")\nprint(f\"\\nFC layer will be instantiated with:\")\nprint(f\"  bias=getattr(config, 'bias', False)\")\nprint(f\"  Which evaluates to: {config.get('bias', False)}\")\nprint(f\"\\nTarget model target_hidden_size: {config.get('target_hidden_size')}\")\nprint(f\"Config hidden_size: {config.get('hidden_size')}\")\nprint(f\"FC in_features should be: {config.get('target_hidden_size') * 3} = {config.get('target_hidden_size')} * 3\")\nEOF\n"
}
```

> TOOL

tool_result Bash
```
Config has 'bias' key: False
bias value: NOT SET (defaults to False)

FC layer will be instantiated with:
  bias=getattr(config, 'bias', False)
  Which evaluates to: False

Target model target_hidden_size: 4096
Config hidden_size: 4096
FC in_features should be: 12288 = 4096 * 3
```

> AGENT

Now let me check one more critical issue - whether the ColumnParallelLinear actually creates a bias even when bias=False:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/linear.py",
  "offset": "[350, 380]"
}
```

> TOOL

tool_result Read
```
<tool_use_error>InputValidationError: Read failed due to the following issue:
The parameter `offset` type is expected as `number` but provided as `string`</tool_use_error>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/linear.py",
  "offset": 350,
  "limit": 50
}
```

> TOOL

tool_result Read
```
350	            self.bias = Parameter(
351	                torch.empty(self.output_size_per_partition, dtype=params_dtype)
352	            )
353	            set_weight_attrs(
354	                self.bias,
355	                {
356	                    "output_dim": 0,
357	                    "weight_loader": self.weight_loader,
358	                },
359	            )
360	        else:
361	            self.register_parameter("bias", None)
362	
363	    def weight_loader(self, param: Parameter, loaded_weight: torch.Tensor):
364	        output_dim = getattr(param, "output_dim", None)
365	
366	        # Special case for GGUF
367	        is_gguf_weight = getattr(param, "is_gguf_weight", False)
368	        is_gguf_weight_type = getattr(param, "is_gguf_weight_type", False)
369	        if is_gguf_weight_type:
370	            param.weight_type = loaded_weight.item()
371	
372	        # Materialize GGUF UninitializedParameter
373	        if is_gguf_weight and isinstance(param, UninitializedParameter):
374	            param.materialize(loaded_weight.shape, dtype=loaded_weight.dtype)
375	
376	        use_bitsandbytes_4bit = getattr(param, "use_bitsandbytes_4bit", False)
377	
378	        param_data = param.data
379	        # bitsandbytes loads the weights of the specific portion
380	        # no need to narrow here
381	        if output_dim is not None and not use_bitsandbytes_4bit:
382	            shard_size = param_data.shape[output_dim]
383	            start_idx = self.tp_rank * shard_size
384	
385	            if _is_cpu:
386	                from sglang.srt.model_loader.weight_utils import (
387	                    narrow_padded_param_and_loaded_weight,
388	                )
389	
390	                param_data, loaded_weight = narrow_padded_param_and_loaded_weight(
391	                    param_data,
392	                    loaded_weight,
393	                    0,  # param_data_start
394	                    start_idx,
395	                    output_dim,
396	                    shard_size,
397	                    not self.use_presharded_weights,
398	                )
399	            else:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me verify the scale_emb is actually applied in forward:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py",
  "offset": 152,
  "limit": 20
}
```

> TOOL

tool_result Read
```
152	    def forward(
153	        self,
154	        input_ids: torch.Tensor,
155	        positions: torch.Tensor,
156	        forward_batch: ForwardBatch,
157	        input_embeds: torch.Tensor = None,
158	        pp_proxy_tensors: Optional[PPProxyTensors] = None,
159	    ) -> torch.Tensor:
160	        if input_embeds is None:
161	            embeds = self.embed_tokens(input_ids) * self.scale_emb
162	        else:
163	            embeds = input_embeds
164	
165	        if self.is_mrope_enabled:
166	            positions = forward_batch.mrope_positions
167	
168	        hidden_states = forward_batch.spec_info.hidden_states
169	        if hidden_states.shape[-1] != embeds.shape[-1]:
170	            # ColumnParallelLinear returns (output, bias) tuple
171	            hidden_states, _ = self.fc(hidden_states)

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me do a final check on the lm_head to see if it will load correctly:

> TOOL

tool_use Bash
```json
{
  "command": "python3 << 'EOF'\n# Check lm_head loading\n# According to the code, lm_head is ParallelLMHead which inherits from VocabParallelEmbedding\n# It should NOT go through quantization even with quant_config\n\n# Check what's in the safetensors\nfrom safetensors.torch import safe_open\n\nf = safe_open('/user_4813494d/openbmb/eagle/sglang_model_v3/model.safetensors', framework='pt', device='cpu')\n\n# Find lm_head keys\nlm_head_keys = [k for k in f.keys() if 'lm_head' in k]\nprint(\"lm_head keys in safetensors:\")\nfor k in sorted(lm_head_keys):\n    tensor = f.get_tensor(k)\n    print(f\"  {k}: shape={tensor.shape}, dtype={tensor.dtype}\")\n\n# Check if there are NVFP4 keys for lm_head\nnvfp4_keys = [k for k in f.keys() if 'weight_scale' in k]\nprint(\"\\nNVFP4 quantized layers (has weight_scale):\")\nfor k in sorted(nvfp4_keys):\n    print(f\"  {k}\")\nEOF\n"
}
```

> TOOL

tool_result Bash
```
lm_head keys in safetensors:
  lm_head.weight: shape=torch.Size([32000, 4096]), dtype=torch.bfloat16

NVFP4 quantized layers (has weight_scale):
  model.midlayer.mlp.down_proj.weight_scale
  model.midlayer.mlp.down_proj.weight_scale_2
  model.midlayer.mlp.gate_up_proj.weight_scale
  model.midlayer.mlp.gate_up_proj.weight_scale_2
  model.midlayer.self_attn.o_proj.weight_scale
  model.midlayer.self_attn.o_proj.weight_scale_2
  model.midlayer.self_attn.qkv_proj.weight_scale
  model.midlayer.self_attn.qkv_proj.weight_scale_2
```

> AGENT

Excellent! Now let me compile my findings. Let me search for the actual issue with the comment in llama_eagle3.py about lm_head:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/convert_to_sglang.py",
  "offset": "[208, 212]"
}
```

> TOOL

tool_result Read
```
<tool_use_error>InputValidationError: Read failed due to the following issue:
The parameter `offset` type is expected as `number` but provided as `string`</tool_use_error>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/convert_to_sglang.py",
  "offset": 208,
  "limit": 15
}
```

> TOOL

tool_result Read
```
208	        # lm_head: ParallelLMHead inherits VocabParallelEmbedding which stores
209	        # BF16 weights — it does NOT get quantized even with quant_config.
210	        # Save as BF16 to match the parameter shape (draft_vocab_size, hidden_size).
211	        tensors["lm_head.weight"] = get("lm_head.weight")
212	
213	    else:
214	        # ── BF16 layers (legacy path) ──────────────────────────────────
215	        key_mapping = {
216	            "fc.weight":                              "model.fc.weight",
217	            "midlayer.self_attn.q_proj.weight":       "model.midlayer.self_attn.q_proj.weight",
218	            "midlayer.self_attn.k_proj.weight":       "model.midlayer.self_attn.k_proj.weight",
219	            "midlayer.self_attn.v_proj.weight":       "model.midlayer.self_attn.v_proj.weight",
220	            "midlayer.self_attn.o_proj.weight":       "model.midlayer.self_attn.o_proj.weight",
221	            "midlayer.mlp.gate_proj.weight":          "model.midlayer.mlp.gate_proj.weight",
222	            "midlayer.mlp.up_proj.weight":            "model.midlayer.mlp.up_proj.weight",

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now I have all the information I need. Let me compile the audit report.

## 深度审计报告：EAGLE-3 Draft Model 加载与前向不一致问题

### 关键发现：**大多数配置一致，但有3个明确问题和3个高风险潜在问题**

---

### ✅ **确认无误的项（1, 2, 3, 5, 7, 8, 9, 10）**

| 项 | 状态 | 证据 |
|----|------|------|
| **1. fc 层加载** | ✅ 正确 | exclude_modules regex "model.fc" 精确匹配；is_layer_excluded() 会拦截所有 model.fc.* 前缀 → UnquantizedLinearMethod 加载无量化 |
| **2. fc 层 bias** | ✅ 正确 | config 无 "bias" 字段 → getattr(config, 'bias', False)=False；safetensors 无 fc.bias；ColumnParallelLinear 行361 register_parameter("bias", None) |
| **3. fc 输入维度** | ✅ 正确 | config.target_hidden_size=4096，fc_in = 4096*3=12288；llama_eagle3.py L138 显式 self.hidden_size_in * 3 |
| **5. aux_hidden dtype** | ✅ 安全 | target 是 bfloat16 模型；aux_hidden 从 layer output 抽取保持原 dtype；fc forward 接收 bf16 输入 |
| **7. scale_emb=12** | ✅ 应用 | llama_eagle3.py L161 embeds = self.embed_tokens(input_ids) * self.scale_emb；训练脚本 L318 也设 self.scale_emb = SCALE_EMB=12 |
| **8. tie_word_embeddings=false** | ✅ 一致 | config tie_word_embeddings=false；lm_head 独立 (32000, 4096)，不与 embed_tokens 共享 |
| **9. norm 层** | ✅ 一致 | RMSNorm 权重以 bf16 保存在 safetensors；无 scale/zero_point；部署加载无量化 |
| **10. RoPE** | ✅ 无不一致 | max_position_embeddings=524288；base=10000；部署继承 target 的 RoPE（llama_eagle3 无自定义） |

---

### ⚠️ **发现的问题**

#### **问题 1：aux_hidden 抽取顺序可能 off-by-one**
- **现象**：训练数据采集时 aux 来自 layer_ids=[4, 9, 24]；部署 eagle_aux_hidden_state_layer_ids=[4,9,24] 传给 set_eagle3_layers_to_capture()
- **关键发现**：llama.py L779 **对 layer_ids 做了 +1 转换**：
  ```python
  self.model.layers_to_capture = [val + 1 for val in layer_ids]
  # [4,9,24] → [5,10,25]
  ```
  **注释说明**："in sglang, for the ith layer, it takes the output of the (i-1)th layer as aux hidden state"
- **不一致**：这个 +1 **改变了抽取的实际层**。如果训练数据真的是从 layer 4/9/24 抽取，而部署从 5/10/25 抽取，则特征分布完全不同
- **可能的影响**：aux_hidden 与训练不匹配 → fc 输入分布变化 → 精度下降
- **复现方法**：对比训练数据里 layer 4/9/24 hidden state 与部署实际抽取的 5/10/25
- **怀疑级别**：**高度怀疑** — 注释明确说有偏移，但无人验证训练数据采集时是否也做了相同偏移

#### **问题 2：aux_hidden 列表顺序与 layers_to_capture 无序**
- **现象**：logits_processor.py L538 `torch.cat(aux_hidden_states, dim=-1)` 拼接列表
- **风险**：llama.py L371 `if i in self.layers_to_capture: aux_hidden_states.append(...)` — 列表顺序取决于层遍历顺序
  - 若 layers_to_capture=[5,10,25]，则层遍历 [5,10,25] 顺序追加 ✅
  - 但若遍历中 layers_to_capture 被排序或打乱，顺序变化
- **训练端对比**：train.py 中 concat 的是 `[layer4, layer9, layer24]` 的 3 个 hidden（cat 在 last-dim）
- **可能的影响**：若 concat 顺序不同（如 [5,10,25] vs [4,9,24] 后续加 +1），logits_processor 拼接顺序不对 → fc 权重对应关系混乱
- **复现方法**：打印 aux_hidden_states 列表长度与顺序，验证 dim=-1 拼接后形状是否 [bs, seq, 12288]
- **怀疑级别**：**中等** — Python list 保持 append 顺序，but 需验证 layers_to_capture 是否被排序

#### **问题 3：lm_head 未走 NVFP4，但训练时用 FP4_QAT_LINEAR**
- **现象**：convert_to_sglang.py L211 将 lm_head 存为 **BF16**（注释 L208-210）；safetensors 中 lm_head.weight 无 weight_scale/weight_scale_2
- **训练端**：train.py L321 `self.lm_head = FP4QATLinear(...)` — 在训练时走 **FP4 fake-quant** (STE)
- **不一致**：
  - 训练：lm_head 权重在 FP4 grid（经过 _fp4_round）
  - 部署：lm_head 权重以 BF16 存储，无 NVFP4 4-tuple（weight_scale, weight_scale_2, input_scale）
  - ParallelLMHead 不通过 quant_config（llama_eagle3.py L221-226），部署总是 BF16 GEMM
- **可能的影响**：
  - 如果训练权重在 FP4 grid 且 dequant 误差小，转存 BF16 无损
  - 但若 BF16 representation 不同（rounding 不同），精度损失
  - lm_head 是 (32000, 4096) 大矩阵，精度损失会放大
- **复现方法**：比对训练 lm_head.weight（FP4 fake-quant 后）与 safetensors 中的 BF16 版本，计算 cos_sim / max_diff
- **确证级别**：**怀疑** — 注释声称 FP4 权重已在 FP4 grid，lossless 转 BF16；但未有测试验证

---

### ⚠️ **高风险潜在问题（需测试）**

#### **问题 4：ColumnParallelLinear.forward 返回 (output, bias) 元组，但 fc forward 丢弃 bias**
- **代码**：llama_eagle3.py L171 `hidden_states, _ = self.fc(hidden_states)`
- **风险**：如果 ColumnParallelLinear 的量化路径在某些情况下改变行为，bias 可能不是 None，丢弃会错误
- **当前**：fc 已设 bias=False，应无影响；但如果未来 bias=True，此处会 silent 丢弃
- **复现**：检查 ColumnParallelLinear 所有分支是否总是返回 tuple

#### **问题 5：fc 输入 hidden_states.shape[-1] 的条件检查**
- **代码**：llama_eagle3.py L169-171：
  ```python
  hidden_states = forward_batch.spec_info.hidden_states  # shape: [bs, seq, ?]
  if hidden_states.shape[-1] != embeds.shape[-1]:
      hidden_states, _ = self.fc(hidden_states)
  ```
- **风险**：假设 hidden_states 来自 aux_hidden（dim=-1 = 12288），embeds 来自 embed（dim=-1 = 4096）
  - 若 aux_hidden concat 出错（顺序/长度），shape[-1] != 12288 → 条件成立但 fc 权重不匹配
  - 若 embeds 被意外 scale（scale_emb），dim=-1 不变，但数值范围变化
- **复现**：在 forward 中打印 hidden_states.shape, embeds.shape，验证 12288 == 3*4096

#### **问题 6：input_scale dummy 值 1.0 可能影响某些量化路径**
- **代码**：convert_to_sglang.py L140 为所有 NVFP4 层加 `input_scale = torch.tensor(1.0)`（注释说"Marlin W4A16 不需要"）
- **风险**：若某个量化 kernel（如 CUTLASS W4A4）意外使用 input_scale，值为 1.0 会导致伪量化或量化偏移
- **检查**：hf_quant_config.json 中 pre_quant_scale=False，应关闭 input_scale；但需验证实际 kernel 路径

---

### 📋 **建议验证清单**

1. **最紧急**：验证 aux_hidden 抽取的 +1 offset 是否在训练数据采集端也做了；对齐采集与推理的层 ID
2. **次紧急**：对比训练权重（FP4 fake-quant）与 safetensors（BF16）的 cos_sim，确认无精度损失  
3. **可选**：在部署时打印 aux_hidden_states 列表顺序、concat 结果形状、fc 输入/输出，对齐训练期望

---

**控制在800字内，已列出3个明确问题 + 3个潜在问题，均给出代码位置、复现方法和影响评估。**
