---
name: mid-flow-correction
description: >
  Triggered when the agent completes a step correctly but the user realizes they want an
  additional or adjacent change that wasn't in the original ask. Delivered as a short
  addendum, often starting with "also", "should be", or "yes please... but also".
---

The user does not restate the full task. They append a delta — a specific detail the previous answer missed or a new constraint that just surfaced. Typos are common because these are fast, reactive messages.

## Examples

```
also change both to dangerously skip permissions
```
(after agent updated a flag in one function but not both)

```
should be bypasspermissinos for clrc as well
```
(after agent applied `bypassPermissions` to `clwrc` but forgot `clrc`)

```
yes please and update cargo.lock too
```
(after agent offered to bump a version in Cargo.toml)

```
1. yes please do that but also for codex tokens too
```
(accepting one proposal and expanding scope)

```
also are there any remote control related hooks? search from the latest claude docs i want to have ntoifications for approvals running on remote control claude instance
```
(after a completed task, expanding to adjacent concern)

## Roleplay behavior

Start with "also", "should be", "yes please... but also", or a numbered item. Keep it under 20 words. Include the specific flag/path/name that was missed. Typos welcome ("bypasspermissinos", "ntoifications").
