---
session_id: f3ec64bf-e3c2-493c-baa2-daff53277df0
developer: "gh:marcus-sa"
split: train
source: swechat
repo: "?"
start_time: "2026-03-25T08:48:04.997551Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

What is the difference between a mutex and a semaphore?

> AGENT

**Mutex** — exclusive lock. One thread owns it at a time. Only the owner can unlock it. Used to protect a single shared resource.

**Semaphore** — a counter. Allows up to N concurrent accessors. Any thread can signal (increment) it. Used to limit concurrency (e.g., connection pool of 5).

Key differences:

| | Mutex | Semaphore |
|---|---|---|
| Count | 1 (binary) | N (configurable) |
| Ownership | Yes — only holder unlocks | No — any thread can signal |
| Purpose | Mutual exclusion | Rate-limiting concurrency |
| Analogy | Bathroom key (one person) | Parking lot with N spots |

A binary semaphore (N=1) looks similar to a mutex but lacks ownership semantics — any thread can release it, which makes it unsuitable for protecting critical sections where you need guarantee that only the lock holder can unlock.
