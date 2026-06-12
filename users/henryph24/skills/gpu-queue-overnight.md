---
name: gpu-queue-overnight
description: >
  Trigger: user mentions available GPU hours (overnight, "8 hours", "2 weeks", "GPUs ready"),
  asks to plan experiments to fill that time, or asks to monitor running experiments at the
  RACE VM. Fires on "monitor experiments", "queue them so GPUs get used", "we have roughly N
  hours", or any reference to the RACE VM GPU state.
---

# gpu-queue-overnight

henryph24 treats the RACE VM GPU as a continuous resource that should never sit idle while he
sleeps or steps away. He plans experiment batches specifically to fill the available GPU window,
asks for monitoring loops at 15-30 minute intervals, and checks whether the GPU is fully packed
or has headroom for more work.

## Pattern — queuing

Short message, collaborative framing, time constraint stated:

> `let plan out some new algorithms or architectural tweak  that may potentially help here and queue them so that GPUs get used until I wake up (the deadline given)`

> `we have roughly 8 hours overnight, can we add more experiments that may meaningfully improve our papers`

> `given this new, better estimation, let's plan more expermients and queued at the race vm so that it run continously in next 8 hours from NOW()`

> `we have the RACE VM with ready GPU (recall from memory)`

## Pattern — monitoring

Often fires as a `/loop` command with "15 minutes" or "30 minutes" interval:

> `/loop monitor experimetns at RACE VM and GPU utilisation --15 minutes`

Or as a bare command:

> `monitor experiments at RACE VM and GPU utilisation`

> `Let's do progress check for the currently running at vm`

> `ETA for the still running experiments`

## Pattern — capacity check after monitor report

He checks whether GPU has headroom and immediately asks to fill it:

> `but GPU is fully packed ?` (after seeing "100% util")

> `in the meantime cna we design more experiments and load them to the GPU`

> `we have the full nights of 8 hours, let design all experiments that will solidify our contributions even further, new algorithm that are likely helpful, and queued that after GPU is ready`

## Typos specific to this behavior

- "experimetns" (experiments) — very consistent
- "continously" (continuously)
- "expermients" (experiments)
