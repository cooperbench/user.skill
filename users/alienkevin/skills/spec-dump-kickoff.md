---
name: spec-dump-kickoff
description: >
  Trigger: AlienKevin is starting a complex multi-step experiment. He opens with a
  200–586-word message containing numbered steps, GCS paths, GitHub URLs, code sketches,
  and explicit verification criteria.
---

When AlienKevin has a complex experiment to run, he front-loads everything in a single dense opening message. These messages include: GitHub issue URLs for context, HuggingFace model/dataset paths, step-by-step instructions with numbering, code sketches in fenced blocks, parallel vs. sequential ordering instructions, verification thresholds (e.g., "within +/-3%"), and GitHub issue titles to create.

**Structure pattern:**
1. Brief context sentence or "Follow [issue URL]"
2. Step-by-step numbered list with sub-bullets
3. Code snippet(s) for key operations
4. Parallelism instruction ("in parallel set up SFT and start the SFT")
5. Verification gate ("confirm within +/-3% before proceeding")
6. GitHub tracking instruction ("Log progress via github comments")

**Verbatim example (truncated):**
> `"Follow https://github.com/marin-community/marin/issues/3490 ... to reproduce 2 OpenThoughts-Agent SFTs. At 32k context length laion/exp_tas_optimal_combined_traces. At 131k context length, REDACTED. Start with the 32k SFT. First find the SFT model at https://huggingface.co/... (double check this for me please). Then, reproduce OT-A's reported 23.8% on TB-Lite and 12.6% on TB2 using their released SFT weights. After making sure we can reproduced within +/-3% for TB-Lite, in parallel set up SFT closely following the model card and start the SFT. ... Log progress via github comments like #3490 to keep all everybody in the loop in a new GitHub issue titled \"[Agentic SFT] Reproduce OT-Agent's best 32K context length SFT\"."`

Note typos like "we can reproduced" and "keep all everybody in the loop" are preserved naturally. These dumps are pasted from his planning notes, not typed fresh.
