---
name: config-freeze-correction
description: >
  Trigger: agent changes a training/infrastructure parameter (TPU slice, sequence length,
  gradient checkpointing, cluster choice, batch size) without being explicitly told to.
  AlienKevin fires a pointed "why did we change X??" question, expects explanation + revert.
---

AlienKevin maintains precise mental models of the current training configuration. When the agent silently changes a hyperparameter or infrastructure choice, he catches it — even steps later — and calls it out with a why-question using double question marks for emphasis. He does not say "revert this"; he expects the agent to understand that the correction implies a revert.

**Verbatim examples:**

> `"why did we change the training configs and switch to v5p-64??"`

> `"why is npx still on node 18?"`

> `"I see, just keep waiting and monitoring. Don't mess with training config/TPU slice size."`

> `"Try 1. Never reduce sequence length and never touch gradient_checkpointing unless explicitly told to. Commit these 2 rules to project memory."`

After the why-question gets answered, he either accepts the explanation and moves on, or issues a terse directive to restore the original setting. He sometimes pairs the correction with a memory-commit command to prevent recurrence.
