# Persona: AlienKevin

## Role and Seniority (inferred)

ML researcher/engineer (inferred) at a lab working on frontier agentic AI. Works in the `marin-community/marin` framework which is an open research infrastructure project. Likely a senior IC or research engineer (inferred) given the depth of systems knowledge: configures Levanter SFT hyperparameters from first principles, spots XLA compiler bugs, reasons about TPU chip counts and HBM, and tracks paper-reported benchmarks to ±2.2%.

GitHub username is a public identifier; no other PII inferred.

## Domain Expertise

- **TPU cluster operations**: v5p-32/64/256, v4-512 slices; knows scheduling behavior, preemption, and coscheduling constraints on Iris cluster vs. Ray
- **Levanter/JAX training**: `SimpleSFTConfig`, `max_grad_norm`, gradient checkpointing, YaRN RoPE scaling, HF export pipelines, checkpoint resumption via content-addressed GCS paths
- **Distributed training failure modes**: XLA compiler crashes at unusual tensor shapes, gradient offloading tradeoffs, sequence length vs. OOM
- **Eval infrastructure**: TerminalBench 2.0, TB-Lite, SWE-bench; Harbor eval runner; Daytona sandbox concurrency limits; sharded eval trials
- **Agentic SFT**: Reproducing OpenThoughts-Agent SFT pipeline; comparing LlamaFactory vs. Levanter preprocessing (think-token normalization, `prep_for_thinking.py`, `ReasoningTemplate`)
- **HuggingFace ecosystem**: Model cards, dataset hubs, snapshot_download, checkpoint formats

## Attitude Toward the Agent

**Trusting but strict**. Delegates freely — the agent does all the running, submitting, monitoring, and GitHub commenting. But AlienKevin holds precise mental models of what should be happening and immediately flags divergences. He does not micromanage step-by-step; he sets objectives and constraints, then checks in periodically. When the agent violates a constraint (changes config, uses wrong cluster, runs two jobs simultaneously), correction is swift and pointed: "why did we change the training configs and switch to v5p-64??"

He is the annotated persona "Expert Nitpicker" 60% of the time — catching wrong details ("why do I still see '131K v2' in #3896?"), wrong numbers ("why is npx still on node 18?"), and logical inconsistencies ("the x/25s don't sum up to 14"). He is "Vague Requester" 27% of the time — sending short, context-light messages that rely on shared session state ("start an Iris dashboard for me", "got it, stop v3 then").

## Tone

Collegial and direct. No please/thank you. Uses "awesome" approvingly. Asks follow-up questions with "why did…" when confused. Rarely praises verbosely. Can be blunt: "I see, just keep waiting and monitoring. Don't mess with training config/TPU slice size."
