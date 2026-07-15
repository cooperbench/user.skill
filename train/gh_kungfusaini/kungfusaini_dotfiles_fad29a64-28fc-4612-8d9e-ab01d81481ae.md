---
session_id: "kungfusaini/dotfiles|fad29a64-28fc-4612-8d9e-ab01d81481ae"
developer: "gh:kungfusaini"
split: train
source: crawl
repo: kungfusaini/dotfiles
start_time: "2026-05-27T17:44:58.698Z"
n_turns: 6
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

analyse this paper. what's it about and any cool insight? https://arxiv.org/abs/2605.22391

> AGENT

**Epicure: Food Ingredient Embeddings**

The paper builds vector embeddings for ~1,790 canonical ingredients by combining two very different signals: how ingredients *co-occur in recipes* and how they *share chemical flavor compounds*.

**What they did**
- Pooled 4.14M recipes across 11 sources / 7 languages, normalizing messy ingredient strings into a canonical vocabulary.
- Trained three Metapath2Vec variants on a heterogeneous graph (ingredients ↔ recipes ↔ compounds). Same architecture and hyperparams — the only difference is the random-walk schema:
  - **Cooc** — pure recipe co-occurrence
  - **Chem** — pure shared-compound walks (from FlavorDB)
  - **Core** — a tunable blend

**Cool insights**
- Holding everything fixed except the walk schema is a clean ablation: it isolates *what kind of similarity* the embedding encodes (cultural/contextual vs. molecular) rather than confounding it with model choice.
- The Core mixing ratio is basically a dial between "what cooks actually combine" and "what chemistry says should pair" — useful for testing the famous *food pairing hypothesis* (shared-compound ingredients taste better together), which is known to hold in Western cuisines but break down in East Asian ones.
- Multilingual normalization to 1,790 canonical ingredients is the unglamorous but load-bearing part — without it the co-occurrence graph is dominated by spelling/locale noise rather than real culinary signal.
- It's an unusually nice example of fusing a behavioral graph (recipes) with a physical-science graph (flavor chemistry) under one embedding space, so downstream tasks (substitution, pairing, cross-cuisine transfer) can pick which axis they want.

> DEVELOPER

okay but could this be used by my ai chef or no?

> AGENT

Short answer: **yes, but probably as a retrieval/grounding layer, not as the brain.**

Where it helps:
- **Substitutions** — "out of shallots, what's closest?" Nearest-neighbor lookup in Cooc gives culinarily plausible swaps; Chem gives flavor-chemistry swaps. Way more reliable than asking an LLM cold.
- **Pairing suggestions** — given a partial ingredient list, rank candidates by embedding similarity to seed a "what goes with this?" feature.
- **Cuisine steering** — the Cooc↔Chem dial is literally a knob for "traditional pairing" vs "experimental/molecular" recipes.
- **Cheap structured grounding** — 1,790 ingredients is tiny; you can stuff top-k neighbors into the LLM prompt as context and dramatically cut hallucinated combos.

Where it won't help:
- No quantities, techniques, timing, or instructions — it's *just* ingredient vectors.
- Vocabulary is fixed at 1,790 canonical items. Anything niche (yuzu kosho, specific chili varietals, brand-name products) probably isn't in there or got collapsed.
- No dietary/allergen/nutrition info baked in — you'd bolt that on separately.

**Practical shape:** LLM does planning + prose, Epicure does ingredient-space math. The LLM proposes, you re-rank or constrain with embeddings before generating the final recipe. If you want, tell me what your AI chef currently does and I'll be more specific about where to wedge it in.

> DEVELOPER

my ai chef takes a photo of my fridge and suggests recipes. It also looks at my diet and makes me meal plans

> AGENT

Honest take: **Epicure is a poor fit for your use case.** Here's why:

**The mismatch**
- Your bottleneck isn't "what ingredients pair well" — it's *vision* (what's actually in the fridge) and *constraints* (your diet, macros, calories, what you ate yesterday). Epicure has nothing to say about either.
- 1,790 canonical ingredients is too coarse for fridge reality. "Greek yogurt vs. skyr vs. labneh," "cilantro vs. parsley," "chicken thigh vs. breast" — these matter for recipes but probably collapse or go missing.
- Meal planning is dominated by nutrition, variety-over-time, prep effort, and leftovers. Embeddings don't encode any of that.

**Where it could still earn its keep — narrow uses**
1. **Substitution fallback.** Vision sees "shallot" but you have red onion — nearest neighbor in Cooc gives a defensible swap without bothering the LLM.
2. **"What's missing?" nudges.** Given detected fridge contents, suggest the 2–3 ingredients that would unlock the most recipes (ingredients with high co-occurrence to what you already have). Good for shopping-list features.
3. **Variety in meal plans.** Penalize back-to-back meals whose ingredient centroids are too close in embedding space — cheap way to avoid "chicken + rice" five days running.

**What I'd actually invest in instead**
- Better vision → ingredient list (this is your real moat).
- A nutrition DB join (USDA FoodData Central) — does the heavy lifting for diet/meal plans.
- A recipe corpus with instructions + macros, retrieved by what's in the fridge.

Epicure is a nice "version 1.3" polish feature. It's not what makes or breaks an AI chef.
