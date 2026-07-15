> SYSTEM

# AGENTS.md instructions for /Users/ericson/.codex/worktrees/55bb/ars-ui

<INSTRUCTIONS>
## Approach
- Read existing files before writing. Don't re-read unless changed.
- Thorough in reasoning, concise in output.
- Skip files over 100KB unless required.
- No sycophantic openers or closing fluff.
- No emojis or em-dashes.
- Do not guess APIs, versions, flags, commit SHAs, or package names. Verify by reading code or docs before asserting.

--- project-doc ---

# ars-ui

## Project Overview

Rust frontend component library using state machines, framework-agnostic core with Leptos/Dioxus adapters.

## Current Phase

The repo is now in active implementation, not spec drafting only.

Agents working on implementation should use the GitHub Project roadmap and issue backlog as the execution source of truth:

- Use the GitHub Project `ars-ui implementation roadmap` to understand active epics, task breakdown, dependencies, status, and iteration planning.
- Prefer picking a single issue-backed task that is unblocked, sized, and scoped for independent delivery.
- Do not start work from an epic issue unless the user explicitly asks for planning or further decomposition.
- Do not start a task that is blocked by unresolved GitHub issue dependencies.
- Treat native GitHub issue dependencies as the blocker graph and the issue body acceptance […]

> DEVELOPER

Recently we did several improvements on how we design and implement our adapter level components, the first one following those new improvements was the Checkbox one, for both adapters. Now I wanna do an audit of the other components that were already implemented. Starting with the field, fieldset and form components.

> AGENT

I’ll ground this in the existing workflow and prior adapter work first, then turn it into an audit plan rather than changing files in Plan Mode. I’m using the repo-specific adapter context plus the Superpowers planning guidance because this is a workflow/spec audit, not a one-off code tweak.

> TOOL

tool_use exec_command
id: call_OKDbHoR43zRWAtvVy7VkHJYh
```json
{
  "cmd": "sed -n '1,220p' /Users/ericson/.claude/skills/using-superpowers/SKILL.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_z75OoBt6kFvGfTubc1Xswer7
```json
{
  "cmd": "sed -n '1,220p' /Users/ericson/.claude/skills/brainstorming/SKILL.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_21OFGYjPk8ROEViYF7POw1Ru
```json
{
  "cmd": "rg -n \"Field|Fieldset|Form|field|fieldset|form|adapter-component|issue-332|issue-423\" /Users/ericson/.codex/memories/MEMORY.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_OKDbHoR43zRWAtvVy7VkHJYh
```
Chunk ID: 34db9b
Wall time: 0.3138 seconds
Process exited with code 0
Original token count: 1356
Output:
---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Superpowers skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Superpowers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md, GEMINI.md, or AGENTS.md says "don't use TDD" and a skill says "always use TDD," follow the user's instructions. The user is in control.

## How to Access […]

> TOOL

tool_result
id: call_z75OoBt6kFvGfTubc1Xswer7
```
Chunk ID: dc3d4a
Wall time: 0.3080 seconds
Process exited with code 0
Original token count: 2659
Output:
---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get […]

> TOOL

tool_result
id: call_21OFGYjPk8ROEViYF7POw1Ru
```
Chunk ID: f9116b
Wall time: 0.0502 seconds
Process exited with code 0
Original token count: 1366
Output:
14:- ars-ui, checkbox, leptos, dioxus, adapter delivery, issue-320, issue-431, merge_dioxus_attrs, hidden input, form reset, cargo xtask spec info checkbox, as_child, @codex review
16:## Task 2: Implement Field, Fieldset, and Form adapter work for Leptos (#332) and Dioxus (#423), with review-fix follow-through
20:- rollout_summaries/REDACTED.md (cwd=/Users/ericson/.codex/worktrees/3efe/ars-ui, rollout_path=/Users/ericson/.codex/sessions/2026/06/04/rollout-2026-06-04T14-33-56-019e93b2-e997-7881-b092-7b1fb63bf491.jsonl, updated_at=2026-06-07T02:45:47+00:00, thread_id=019e93b2-e997-7881-b092-7b1fb63bf491, combined cross-adapter delivery, focused wasm validation, review-thread cleanup, and Coverage still pending at stop time)
24:- ars-ui, leptos, dioxus, adapter delivery, field, fieldset, form, issue-332, issue-423, wasm-bindgen-test-runner, browser tests, ButtonAsChild, raw oninput, status-region, review threads, @codex review
30:- issue bodies that call for parity, SSR/hydration stability, form integration, and named tests should push the default toward broad adapter completeness instead of a partial component shell [Task 1][Task 2]
35:- the fastest orientation loop for this task family was: read the live GitHub issues, run `cargo xtask spec info <component>`, `cargo xtask spec component-deps <component> --adapter <adapter>`, and `cargo xtask spec issue-deps --adapter <adapter> --component <component> --dry-run`, then read `docs/implementation/adapter-components/`, `docs/implementation/adapter-contract.md`, and the relevant component/adapter specs before editing [Task 1][Task 2]
37:- for Field in this rollout, `cargo xtask spec component-deps field --adapter […]

> AGENT

The memory index points to the original Field/Fieldset/Form adapter delivery and one review-found defect: form error counts accidentally included fieldset/container invalid states instead of only named native controls. I’m going to inspect the current adapter workflow docs and the shipped Field/Form code to make the audit plan line up with today’s contract.

> TOOL

tool_use exec_command
id: call_ykYIan7XCd7GLczGz1KvSb0U
```json
{
  "cmd": "sed -n '1,260p' /Users/ericson/.codex/memories/rollout_summaries/REDACTED.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_JVLwFaOV6OnoWwMPEh9jagp7
```json
{
  "cmd": "wc -l docs/implementation/adapter-component-delivery.md .agents/skills/post-implementation-audit/SKILL.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_OqENtHQ1mWDrwnkDdS6S0CoH
```json
{
  "cmd": "rg --files crates/ars-leptos crates/ars-dioxus crates/ars-e2e examples spec docs/implementation | rg '(field|fieldset|form|adapter-component|adapter-components)'",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_5lTldMkefSspLFF4ebVnMcTS
```json
{
  "cmd": "git status --short",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_ykYIan7XCd7GLczGz1KvSb0U
```
Chunk ID: d5c8f6
Wall time: 0.4361 seconds
Process exited with code 0
Original token count: 783
Output:
thread_id: 019e93b2-e997-7881-b092-7b1fb63bf491
updated_at: 2026-06-07T02:45:47+00:00
rollout_path: /Users/ericson/.codex/sessions/2026/06/04/rollout-2026-06-04T14-33-56-019e93b2-e997-7881-b092-7b1fb63bf491.jsonl
cwd: /Users/ericson/.codex/worktrees/3efe/ars-ui
git_branch: codex/issue-332-423-field-form-adapters

# Implemented Leptos and Dioxus Field/Fieldset/Form adapter work for issues #332 and #423, then fixed review regressions and pushed a follow-up commit.

Rollout context: the user asked to "Implement tasks #332 and #423" in `/Users/ericson/.codex/worktrees/3efe/ars-ui`. The work was framed as adapter-level component delivery, so the agent read the live GitHub issues, the adapter workflow docs, the Leptos/Dioxus framework skills, the adapter contract docs, and the component specs before editing. The two issues were closely related: #332 covered the Leptos adapter for Field/Fieldset/Form; #423 covered the Dioxus adapter for the same component family. Dependency checks confirmed both were unblocked and matched the issue bodies.

## Task 1: Leptos + Dioxus Field/Fieldset/Form adapter implementation and follow-up fixes

Outcome: partial

Preference signals:
- The user asked for both issue numbers in one request: "Implement tasks #332 and #423" -> the rollout treated the two adapters as a single coordinated delivery rather than separate threads.
- The user did not ask for design discussion or incremental approval before implementation -> the agent proceeded […]

> TOOL

tool_result
id: call_JVLwFaOV6OnoWwMPEh9jagp7
```
Chunk ID: 0d33b7
Wall time: 0.4482 seconds
Process exited with code 0
Original token count: 34
Output:
     172 docs/implementation/adapter-component-delivery.md
     468 .agents/skills/post-implementation-audit/SKILL.md
     640 total

```

> TOOL

tool_result
id: call_OqENtHQ1mWDrwnkDdS6S0CoH
```
Chunk ID: 6355ee
Wall time: 0.4504 seconds
Process exited with code 0
Original token count: 900
Output:
docs/implementation/adapter-component-delivery.md
docs/implementation/adapter-components/02-adapter-api-and-wiring.md
docs/implementation/adapter-components/06-widgets-examples.md
docs/implementation/adapter-components/12-parity-audit-loop.md
docs/implementation/adapter-components/04-adapter-tests.md
docs/implementation/adapter-components/10-reference-exploration-sketch.md
docs/implementation/adapter-component-dependency-inventory.md
docs/implementation/adapter-components/11-i18n-and-a11y-support.md
docs/implementation/adapter-components/checkbox-usage.md
docs/implementation/adapter-components/05-e2e-fixtures-and-harnesses.md
docs/implementation/adapter-components/01-before-you-code.md
docs/implementation/adapter-components/README.md
docs/implementation/adapter-components/03-framework-rules.md
docs/implementation/adapter-components/08-validation-and-pr-closeout.md
docs/implementation/adapter-components/09-browser-parity-harness.md
docs/implementation/adapter-components/13-composition-integration.md
docs/implementation/adapter-components/07-parity-review.md
docs/implementation/adapter-component-dependencies.md
docs/implementation/sketches/332-423-field-form-counterpart-sketch.md
spec/testing/11-form-validation.md
docs/implementation/adapter-components/templates/reference-exploration-sketch.md
docs/implementation/adapter-components/checklists/widgets-visual-review.md
docs/implementation/adapter-components/checklists/e2e-feature-matrix.md
docs/implementation/adapter-components/checklists/component-delivery.md
crates/ars-leptos/src/utility/form.rs
crates/ars-leptos/src/utility/fieldset.rs
crates/ars-leptos/src/utility/field.rs
crates/ars-leptos/src/utility/field_support.rs
crates/ars-dioxus/src/utility/form.rs
crates/ars-dioxus/src/utility/fieldset.rs
crates/ars-dioxus/src/utility/field.rs
crates/ars-dioxus/src/utility/field_support.rs
crates/ars-dioxus/src/platform.rs
spec/components/utility/form-submit.md
spec/components/utility/field.md
spec/components/utility/fieldset.md
spec/components/utility/form.md
crates/ars-e2e/src/utility/field_form.rs
spec/foundation/12-adapter-component-spec-template.md
spec/foundation/07-forms.md
spec/dioxus-components/utility/field.md
spec/dioxus-components/utility/fieldset.md
spec/dioxus-components/utility/form.md
spec/leptos-components/utility/field.md
spec/leptos-components/utility/fieldset.md
spec/leptos-components/utility/form.md
crates/ars-leptos/tests/form.rs
crates/ars-leptos/tests/fieldset.rs
crates/ars-leptos/tests/test_field_wasm.rs
crates/ars-leptos/tests/field.rs
crates/ars-leptos/tests/test_form_wasm.rs
spec/leptos-components/specialized/color-field.md
crates/ars-dioxus/tests/form.rs
crates/ars-dioxus/tests/fieldset.rs
crates/ars-dioxus/tests/test_field_wasm.rs
crates/ars-dioxus/tests/field.rs
crates/ars-dioxus/tests/test_form_wasm.rs
crates/ars-leptos/tests/test_fieldset_wasm.rs
spec/leptos-components/input/text-field.md
crates/ars-dioxus/tests/test_fieldset_wasm.rs
crates/ars-dioxus/tests/desktop_platform.rs
spec/leptos-components/date-time/date-range-field.md
spec/leptos-components/date-time/date-field.md
spec/leptos-components/date-time/time-field.md
spec/components/date-time/date-range-field.md
spec/components/date-time/date-field.md
spec/components/date-time/time-field.md
spec/dioxus-components/date-time/date-range-field.md
spec/dioxus-components/date-time/date-field.md
spec/dioxus-components/date-time/time-field.md
spec/components/specialized/color-field.md
spec/dioxus-components/input/text-field.md
spec/dioxus-components/specialized/color-field.md
spec/components/input/text-field.md

```

> TOOL

tool_result
id: call_5lTldMkefSspLFF4ebVnMcTS
```
Chunk ID: 283e5b
Wall time: 0.3539 seconds
Process exited with code 0
Original token count: 0
Output:

```

> AGENT

The current checkout is clean, so the plan does not need to account for local uncommitted changes. Next I’m reading the adapter delivery/audit guidance and a representative slice of the Field/Form implementation and tests to identify what the audit should verify against the newer Checkbox standard.

> TOOL

tool_use exec_command
id: call_0GynVkNrKLcddoyDSpj27JpF
```json
{
  "cmd": "sed -n '1,220p' docs/implementation/adapter-component-delivery.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_CSONRcqalo00vLK9bNZs51ws
```json
{
  "cmd": "sed -n '1,260p' .agents/skills/post-implementation-audit/SKILL.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_3e3rUBmlgCXEIPeS1jEAjo8y
```json
{
  "cmd": "sed -n '1,220p' docs/implementation/adapter-components/README.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_9SIxjeeqJ38Ins6Cbw6wQMfG
```json
{
  "cmd": "sed -n '1,240p' docs/implementation/adapter-components/checklists/component-delivery.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_0GynVkNrKLcddoyDSpj27JpF
```
Chunk ID: 737458
Wall time: 0.4560 seconds
Process exited with code 0
Original token count: 2441
Output:
# Adapter Component Delivery Workflow

This file is the mandatory entry point for adapter-level component work.

Use this workflow for any issue that adds or materially changes a component in
`crates/ars-leptos` or `crates/ars-dioxus`.

The detailed workflow is split across:

- [adapter-components/README.md](adapter-components/README.md)
- [adapter-components/01-before-you-code.md](adapter-components/01-before-you-code.md)
- [adapter-components/10-reference-exploration-sketch.md](adapter-components/10-reference-exploration-sketch.md)
- [adapter-components/07-parity-review.md](adapter-components/07-parity-review.md)
- [adapter-components/11-i18n-and-a11y-support.md](adapter-components/11-i18n-and-a11y-support.md)
- [adapter-components/02-adapter-api-and-wiring.md](adapter-components/02-adapter-api-and-wiring.md)
- [adapter-components/03-framework-rules.md](adapter-components/03-framework-rules.md)
- [adapter-components/04-adapter-tests.md](adapter-components/04-adapter-tests.md)
- [adapter-components/13-composition-integration.md](adapter-components/13-composition-integration.md)
- [adapter-components/05-e2e-fixtures-and-harnesses.md](adapter-components/05-e2e-fixtures-and-harnesses.md)
- [adapter-components/06-widgets-examples.md](adapter-components/06-widgets-examples.md)
- [adapter-components/09-browser-parity-harness.md](adapter-components/09-browser-parity-harness.md)
- [adapter-components/12-parity-audit-loop.md](adapter-components/12-parity-audit-loop.md)
- [adapter-components/08-validation-and-pr-closeout.md](adapter-components/08-validation-and-pr-closeout.md)
- [adapter-components/checklists/component-delivery.md](adapter-components/checklists/component-delivery.md)
- [adapter-components/checklists/e2e-feature-matrix.md](adapter-components/checklists/e2e-feature-matrix.md)
- [adapter-components/checklists/widgets-visual-review.md](adapter-components/checklists/widgets-visual-review.md)

## Mandatory Reading Rule

Before planning or implementing an adapter-level component task, fully read:

1. this entry-point file;
2. every workflow file listed above;
3. the checklists listed above.

The checklist files are reminders, not substitutes for the workflow files. Do
not start from a checklist alone.

## Why This Is Split

Adapter delivery spans several distinct concerns:

- issue/spec dependency checks;
- counterpart-driven UX design;
- durable reference-exploration sketches written from live browser evidence;
- full i18n and accessibility contract mapping for every user-facing state;
- adapter API shape and wiring;
- framework-specific Leptos and Dioxus rules;
- adapter SSR/unit tests plus focused wasm browser […]

> TOOL

tool_result
id: call_CSONRcqalo00vLK9bNZs51ws
```
Chunk ID: 281128
Wall time: 0.3240 seconds
Process exited with code 0
Original token count: 6631
Output:
---
name: post-implementation-audit
description: MANDATORY after every implementation task — runs three sequential audits on the new code (spec/impl drift, iterative "anything missing?", test coverage) and lands every finding in the same PR before the user-review step. Invoke as soon as an implementation task's named tests pass, OR when any of these phrases appears: "ready to present", "implementation is complete", "named tests pass", "before opening the PR", "ready for review". Skipping this audit leaves spec drift, untested defensive code, missing conventions, and silent contract violations in the merged PR.
---

# Post-implementation audit

This skill is the bridge between _"the named tests pass"_ and _"the user reviews the diff"_. It exists because the initial implementation of any task is usually correct on its surface acceptance criteria but quietly drifts from the spec, leaves untested defensive code, ships APIs that diverge from convention, or carries a fold-vs-lowercase mistake that won't surface until production. Running these audits before user-review collapses three reviewer round-trips into one.

The skill is mandatory per CLAUDE.md "Development Workflow" step 7 — run it after implementing any […]

> TOOL

tool_result
id: call_3e3rUBmlgCXEIPeS1jEAjo8y
```
Chunk ID: 86dd3b
Wall time: 0.3276 seconds
Process exited with code 0
Original token count: 1070
Output:
# Adapter Component Delivery

This directory is the end-to-end workflow for implementing adapter-level
components in `crates/ars-leptos` and `crates/ars-dioxus`.

The old monolithic workflow now lives as this doc set so agents can read the
full contract in a stable order and then return to the specific layer they are
editing.

## Mandatory Reading Order

Before planning or implementing any adapter-level component task, read every
file below:

1. [01-before-you-code.md](01-before-you-code.md)
2. [10-reference-exploration-sketch.md](10-reference-exploration-sketch.md)
3. [07-parity-review.md](07-parity-review.md)
4. [11-i18n-and-a11y-support.md](11-i18n-and-a11y-support.md)
5. [02-adapter-api-and-wiring.md](02-adapter-api-and-wiring.md)
6. [03-framework-rules.md](03-framework-rules.md)
7. [04-adapter-tests.md](04-adapter-tests.md)
8. [13-composition-integration.md](13-composition-integration.md)
9. [05-e2e-fixtures-and-harnesses.md](05-e2e-fixtures-and-harnesses.md)
10. [06-widgets-examples.md](06-widgets-examples.md)
11. [09-browser-parity-harness.md](09-browser-parity-harness.md)
12. [12-parity-audit-loop.md](12-parity-audit-loop.md)
13. [08-validation-and-pr-closeout.md](08-validation-and-pr-closeout.md)

Then keep the checklists open while implementing:

- [checklists/component-delivery.md](checklists/component-delivery.md)
- [checklists/e2e-feature-matrix.md](checklists/e2e-feature-matrix.md)
- [checklists/widgets-visual-review.md](checklists/widgets-visual-review.md)

Component-specific usage notes live beside this workflow when an adapter
component has composition behavior worth preserving. For Checkbox, read
[checkbox-usage.md](checkbox-usage.md) before changing standalone, `Form`, or
`Fieldset` behavior.

The checklist files are reminders, not substitutes for the workflow files.

## Non-Negotiable Contract

An adapter component task is complete only when the same PR includes:

- adapter crate code, module wiring, feature wiring, and symmetric prelude
  exports for unstyled primitives;
- styled component source-template crate code and […]

> TOOL

tool_result
id: call_9SIxjeeqJ38Ins6Cbw6wQMfG
```
Chunk ID: 797b73
Wall time: 0.0475 seconds
Process exited with code 0
Original token count: 2778
Output:
# Adapter Component Delivery Checklist

Use this checklist while implementing. It is not a substitute for reading the
workflow docs.

## Before Code

- [ ] Assigned issue read.
- [ ] Issue moved to In Progress.
- [ ] Dependency checks run for Leptos and Dioxus.
- [ ] Agnostic and adapter specs read.
- [ ] Adapter foundation specs read.
- [ ] `adapter-contract.md` read.
- [ ] `examples/widgets-ownership.md` read.
- [ ] Component-specific usage docs read or created when the component has standalone/composed behavior.
- [ ] Framework skills loaded when touching Leptos/Dioxus.
- [ ] `playwright-cli` skill loaded for reference exploration.
- [ ] Reference implementation tried with `playwright-cli`, not only read.
- [ ] Implementation sketch created under `docs/implementation/sketches/`.
- [ ] Sketch records reference artifact paths and explored states.
- [ ] Sketch maps every reference outcome to ars-ui contract surfaces.
- [ ] Sketch records API/contract stance for every reference outcome, without treating React/TypeScript API shape as required parity.
- [ ] Sketch maps every user-facing string to an i18n source or […]

> AGENT

The newer workflow adds several audit dimensions that probably were not present, or were lighter, when Field/Form first landed: durable browser evidence, explicit consumer-reality review, composition integration, semantic-boundary checks, styled-template boundary checks, and a final outcome matrix with no unknown/workaround rows. I’m checking whether the current Field/Form artifacts already have those pieces or just the older baseline.

> TOOL

tool_use exec_command
id: call_tR4IkQZWWqpeCLjlm3wbV9EJ
```json
{
  "cmd": "sed -n '1,260p' docs/implementation/sketches/332-423-field-form-counterpart-sketch.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_2ZplPuDbL2TpYN3XGIROal2i
```json
{
  "cmd": "sed -n '1,260p' crates/ars-leptos/src/utility/field.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_HvT8WjCxSSerg06jIyfxiyrs
```json
{
  "cmd": "sed -n '1,260p' crates/ars-dioxus/src/utility/field.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_BuRgxN2HpPNSWaOjp9dD5Wny
```json
{
  "cmd": "sed -n '1,260p' crates/ars-e2e/src/utility/field_form.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_tR4IkQZWWqpeCLjlm3wbV9EJ
```
Chunk ID: 81934d
Wall time: 0.3359 seconds
Process exited with code 0
Original token count: 9468
Output:
# Field/Form Adapter Reference Exploration Sketch

## Task

- Issues: #332, #423
- Component: Field, Fieldset, Form
- Category: utility
- Adapters in scope: Leptos, Dioxus
- Specs read: `spec/leptos-components/utility/field.md`, `spec/dioxus-components/utility/field.md`, `spec/leptos-components/utility/form.md`, `spec/dioxus-components/utility/form.md`, `spec/components/utility/field.md`, `spec/components/utility/fieldset.md`, `spec/components/utility/form.md`
- Date: 2026-06-04

## Reference Sources

- Primary counterpart: React Aria Form
- Primary URL: <https://react-aria.adobe.com/Form>
- Fallback counterparts inspected: NotApplicable
- Reason for fallback or N/A: React Aria has the component and is the primary adapter reference.

## Playwright Exploration Commands

```bash
playwright-cli -s=reference open https://react-aria.adobe.com/Form
playwright-cli -s=reference snapshot --filename=.playwright-cli/reference-form-initial.yml
playwright-cli -s=reference click e275
playwright-cli -s=reference snapshot --filename=.playwright-cli/reference-form-empty-submit.yml
playwright-cli -s=reference screenshot --filename=/tmp/reference-form-empty-submit.png
playwright-cli -s=reference run-code "async page => { /* inspect email validity states */ }"
playwright-cli -s=reference run-code "async page => { /* inspect reset behavior */ }"
playwright-cli -s=reference run-code "async page => { /* inventory all React Aria Form examples */ }"
```

## Reference Evidence

| State or outcome               | Command or action                                                              | Artifact                                                                                  | Notes                                                                                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Page baseline                  | `snapshot --filename=.playwright-cli/reference-form-initial.yml`               | `.playwright-cli/reference-form-initial.yml`                                              | Shows five […]

> TOOL

tool_result
id: call_2ZplPuDbL2TpYN3XGIROal2i
```
Chunk ID: 8786f5
Wall time: 0.3361 seconds
Process exited with code 0
Original token count: 1710
Output:
//! Leptos Field adapter.

use ars_components::utility::field;
pub use ars_components::utility::field::{InputType, Part, Props};
use ars_core::{AriaAttr, AttrMap, AttrValue, Direction, HtmlAttr};
use ars_forms::validation::Error;
use leptos::{children::TypedChildren, context::Provider, either::Either, prelude::*};

use crate::{attr_map_to_leptos_inline_attrs, callbacks, use_id, use_machine_with_reactive_props};

#[derive(Clone, Copy)]
struct FieldContext {
    machine: crate::UseMachineReturn<field::Machine>,
}

fn field_context() -> FieldContext {
    use_context::<FieldContext>().expect("Field subcomponents must be rendered inside <Field/>")
}

/// Leptos Field root component.
#[component]
#[expect(
    clippy::needless_pass_by_value,
    reason = "Leptos component props are owned builder inputs; borrowing the Oco class prop avoids allocating with Oco::into_owned just to satisfy Clippy."
)]
pub fn Field<T: 'static>(
    /// Optional component instance ID.
    #[prop(optional, into)]
    id: Option<Oco<'static, str>>,

    /// Whether the field is required.
    #[prop(optional, into)]
    required: Signal<bool>,

    /// Whether the field is disabled.
    #[prop(optional, into)]
    disabled: Signal<bool>,

    /// Whether the field is read-only.
    #[prop(optional, into)]
    readonly: Signal<bool>,

    /// Whether the field is invalid.
    #[prop(optional, into)]
    invalid: Signal<bool>,

    /// Field name used to consume matching form-level validation errors.
    #[prop(optional, into)]
    name: Option<Oco<'static, str>>,

    /// Field-level validation errors.
    #[prop(optional, into)]
    errors: Signal<Vec<Error>>,

    /// Optional text direction override.
    #[prop(optional)]
    dir: Option<Direction>,

    /// Consumer class tokens appended to the root.
    #[prop(optional, into)]
    class: Option<TextProp>,

    /// […]

> TOOL

tool_result
id: call_HvT8WjCxSSerg06jIyfxiyrs
```
Chunk ID: 202b3f
Wall time: 0.3346 seconds
Process exited with code 0
Original token count: 1720
Output:
//! Dioxus Field adapter.

use ars_components::utility::field;
pub use ars_components::utility::field::{InputType, Part, Props};
use ars_core::{AriaAttr, AttrMap, Direction, HtmlAttr};
use ars_forms::validation::Error;
use dioxus::prelude::*;

use crate::{
    attr_map_to_dioxus_inline_attrs, callbacks, merge_dioxus_attrs, use_machine, use_stable_id,
};

#[derive(Clone, Copy)]
struct FieldContext {
    machine: crate::UseMachineReturn<field::Machine>,
}

fn field_context() -> FieldContext {
    try_use_context::<FieldContext>().expect("Field subcomponents must be rendered inside <Field/>")
}

/// Props for the Dioxus [`Field`] component.
#[derive(Props, Clone, PartialEq, Debug)]
pub struct FieldProps {
    /// Optional component instance ID.
    #[props(optional, into)]
    pub id: Option<String>,

    /// Whether the field is required.
    #[props(default = false)]
    pub required: bool,

    /// Whether the field is disabled.
    #[props(default = false)]
    pub disabled: bool,

    /// Whether the field is read-only.
    #[props(default = false)]
    pub readonly: bool,

    /// Whether the field is invalid.
    #[props(default = false)]
    pub invalid: bool,

    /// Field name used to consume matching form-level validation errors.
    #[props(optional, into)]
    pub name: Option<String>,

    /// Field-level validation errors.
    #[props(default)]
    pub errors: Vec<Error>,

    /// Optional text direction override.
    #[props(optional)]
    pub dir: Option<Direction>,

    /// Global HTML attributes forwarded onto the root.
    #[props(extends = GlobalAttributes)]
    pub attrs: Vec<Attribute>,

    /// Field anatomy children.
    pub children: Element,
}

/// Dioxus Field […]

> TOOL

tool_result
id: call_BuRgxN2HpPNSWaOjp9dD5Wny
```
Chunk ID: 25bb44
Wall time: 0.0490 seconds
Process exited with code 0
Original token count: 1709
Output:
//! Browser E2E harness for Field, Fieldset, and Form utility adapters.

use std::time::{Duration, Instant};

use thirtyfour::prelude::*;
use tokio::time;

pub use crate::fixtures::Adapter;
use crate::{
    Error,
    axe::run_axe,
    utility::{assert_attr, assert_bool_attr, element_by_id, open_utility_panel},
};

/// Runs Field, Fieldset, and Form browser assertions inside the Utility fixture panel.
///
/// # Errors
///
/// Returns an error when `WebDriver` cannot find fixture nodes or an assertion fails.
pub async fn run_field_form_flow(
    driver: &WebDriver,
    url: &str,
    adapter: Adapter,
) -> Result<(), Error> {
    open_utility_panel(driver, url).await?;

    let prefix = id_prefix(adapter);

    let form = element_by_id(driver, &format!("{prefix}-account-form")).await?;

    assert_attr(&form, "data-ars-scope", "form").await?;
    assert_attr(&form, "data-ars-part", "root").await?;
    assert_attr(&form, "data-ars-state", "idle").await?;
    assert_attr(&form, "action", "/account").await?;
    assert_bool_attr(&form, "novalidate").await?;

    let fieldset = element_by_id(driver, &format!("{prefix}-account-fieldset")).await?;

    assert_attr(&fieldset, "data-ars-scope", "fieldset").await?;
    assert_attr(&fieldset, "data-ars-part", "root").await?;
    assert_bool_attr(&fieldset, "disabled").await?;

    assert_invalid_email_field(
        driver,
        prefix,
        "required",
        "email-required",
        "Email is required.",
        true,
        None,
    )
    .await?;

    assert_invalid_email_field(
        driver,
        prefix,
        "missing-at",
        "email-missing-at",
        "Include an @ in the email address.",
        false,
        Some("admin"),
    )
    .await?;

    assert_invalid_email_field(
        driver,
        prefix,
        "incomplete-domain",
        "email-incomplete-domain",
        "Enter a domain after @.",
        false,
        Some("admin@"),
    )
    .await?;

    assert_valid_email_field(driver, prefix).await?;

    let status = form
        .find(By::Css("[data-ars-part='status-region']"))
        .await?;

    assert_attr(&status, "role", "status").await?;
    assert_attr(&status, "aria-live", "polite").await?;
    assert_attr(&status, "aria-atomic", "true").await?;
    assert_text(&status, "Ready", "form status").await?;
    assert_status_is_not_field_error(&status).await?; […]

> AGENT

The existing sketch is unusually complete for that earlier work and already records the three-pass parity loop, but it also has an addendum that later narrowed the Tailwind examples back to a “low-level relationship showcase.” The audit should therefore test the current repo against the newest workflow, not simply assume the old sketch remains true.

> TOOL

tool_use exec_command
id: call_KEm3P37qk0L15ZQfADucBViL
```json
{
  "cmd": "sed -n '220,520p' crates/ars-leptos/src/utility/field.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_nqkOtNlQy74l0ppIDV4Q2kvz
```json
{
  "cmd": "sed -n '220,520p' crates/ars-dioxus/src/utility/field.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_biq4X8iDgYNV2GU1CXbgjYz0
```json
{
  "cmd": "sed -n '1,300p' crates/ars-leptos/src/utility/form.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_hRIfA0eUXwJw6tYlNpJ2Tdb9
```json
{
  "cmd": "sed -n '1,340p' crates/ars-dioxus/src/utility/form.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_KEm3P37qk0L15ZQfADucBViL
```
Chunk ID: 1eab93
Wall time: 0.4333 seconds
Process exited with code 0
Original token count: 1102
Output:
    children: TypedChildren<T>,
) -> impl IntoView
where
    View<T>: IntoView,
{
    let machine = field_context().machine;

    machine.send.run(field::Event::SetHasDescription(true));

    on_cleanup(move || machine.send.run(field::Event::SetHasDescription(false)));

    let attrs =
        machine.with_api_snapshot(|api| attr_map_to_leptos_inline_attrs(api.description_attrs()));

    view! { <div {..attrs}>{children.into_inner()()}</div> }
}

/// Leptos Field error message part.
#[component]
pub fn ErrorMessage<T>(
    /// Error message content.
    children: TypedChildren<T>,
) -> impl IntoView
where
    View<T>: IntoView,
{
    let machine = field_context().machine;

    let hidden = machine.derive(|api| api.error_message_attrs().contains(&HtmlAttr::Hidden));

    let attrs = machine.with_api_snapshot(|api| {
        let mut attrs = api.error_message_attrs();

        attrs.set(
            HtmlAttr::Hidden,
            AttrValue::reactive_bool(move || hidden.get()),
        );

        attr_map_to_leptos_inline_attrs(attrs)
    });

    view! { <div {..attrs}>{children.into_inner()()}</div> }
}

#[expect(
    clippy::redundant_closure_for_method_calls,
    reason = "Api method references are not general enough for part attr callbacks."
)]
fn add_dynamic_input_attrs(attrs: &mut AttrMap, machine: crate::UseMachineReturn<field::Machine>) {
    let described_by = machine.attr_optional_string_memo(
        |api| api.input_attrs(),
        HtmlAttr::Aria(AriaAttr::DescribedBy),
    );
    let aria_invalid =
        machine.attr_presence_memo(|api| api.input_attrs(), HtmlAttr::Aria(AriaAttr::Invalid));
    let error_message = machine.attr_optional_string_memo(
        |api| api.input_attrs(),
        HtmlAttr::Aria(AriaAttr::ErrorMessage),
    );
    let aria_required =
        machine.attr_presence_memo(|api| api.input_attrs(), HtmlAttr::Aria(AriaAttr::Required));
    let aria_disabled =
        machine.attr_presence_memo(|api| api.input_attrs(), HtmlAttr::Aria(AriaAttr::Disabled));
    let aria_readonly =
        machine.attr_presence_memo(|api| api.input_attrs(), HtmlAttr::Aria(AriaAttr::ReadOnly));

    attrs
        .set(
            HtmlAttr::Aria(AriaAttr::DescribedBy),
            AttrValue::reactive_optional(move || described_by.get()),
        )
        .set(
            HtmlAttr::Aria(AriaAttr::Invalid),
            AttrValue::reactive_bool(move || aria_invalid.get()),
        )
        .set(
            HtmlAttr::Aria(AriaAttr::ErrorMessage),
            AttrValue::reactive_optional(move || error_message.get()),
        )
        .set(
            HtmlAttr::Aria(AriaAttr::Required),
            AttrValue::reactive_bool(move || aria_required.get()),
        )
        .set(
            HtmlAttr::Required,
            AttrValue::reactive_bool(move || aria_required.get()), […]

> TOOL

tool_result
id: call_nqkOtNlQy74l0ppIDV4Q2kvz
```
Chunk ID: 042fa5
Wall time: 0.4182 seconds
Process exited with code 0
Original token count: 370
Output:
    });

    let attrs = field_context()
        .machine
        .derive(|api| attr_map_to_dioxus_inline_attrs(api.description_attrs()))();

    rsx! {
        div { ..attrs,{props.children} }
    }
}

/// Props for the Dioxus [`ErrorMessage`] component.
#[derive(Props, Clone, PartialEq, Debug)]
pub struct ErrorMessageProps {
    /// Error message content.
    pub children: Element,
}

/// Dioxus Field error message part.
#[component]
pub fn ErrorMessage(props: ErrorMessageProps) -> Element {
    let attrs = field_context()
        .machine
        .derive(|api| attr_map_to_dioxus_inline_attrs(api.error_message_attrs()))();

    rsx! {
        div { ..attrs,{props.children} }
    }
}

fn apply_input_attrs(
    attrs: &mut AttrMap,
    r#type: Option<InputType>,
    name: Option<String>,
    placeholder: Option<String>,
) {
    if let Some(input_type) = r#type {
        attrs.set(HtmlAttr::Type, input_type.as_str());
    }

    if let Some(name) = name {
        attrs.set(HtmlAttr::Name, name);
    }

    if let Some(placeholder) = placeholder {
        attrs.set(HtmlAttr::Placeholder, placeholder);
    }

    if attrs.contains(&HtmlAttr::Aria(AriaAttr::Disabled)) {
        attrs.set_bool(HtmlAttr::Disabled, true);
    }

    if attrs.contains(&HtmlAttr::Aria(AriaAttr::Required)) {
        attrs.set_bool(HtmlAttr::Required, true);
    }

    if attrs.contains(&HtmlAttr::Aria(AriaAttr::ReadOnly)) {
        attrs.set_bool(HtmlAttr::ReadOnly, true);
    }
}

```

> TOOL

tool_result
id: call_biq4X8iDgYNV2GU1CXbgjYz0
```
Chunk ID: 7c0062
Wall time: 0.4211 seconds
Process exited with code 0
Original token count: 2411
Output:
//! Leptos Form adapter.

use std::collections::BTreeMap;

use ars_components::utility::form;
pub use ars_components::utility::form::{Part, Props, ValidationBehavior};
use ars_core::{AriaAttr, AttrMap, AttrValue, HtmlAttr};
use ars_forms::validation::Error;
use leptos::{children::TypedChildren, context::Provider, html, prelude::*};
#[cfg(target_arch = "wasm32")]
use leptos::{
    wasm_bindgen::{JsCast as _, JsValue},
    web_sys,
};

use crate::{
    attr_map_to_leptos_inline_attrs, callbacks, use_id, use_machine_with_reactive_props,
    use_messages_and_locale,
};

#[derive(Clone, Copy)]
pub(crate) struct FormContext {
    pub(crate) machine: crate::UseMachineReturn<form::Machine>,
}

/// Leptos Form root component.
#[component]
pub fn Form<T: 'static>(
    /// Optional component instance ID.
    #[prop(optional, into)]
    id: Option<Oco<'static, str>>,

    /// URL the browser submits the form to.
    #[prop(optional, into)]
    action: Option<Oco<'static, str>>,

    /// Optional explicit form role.
    #[prop(optional, into)]
    role: Option<Oco<'static, str>>,

    /// Validation display behavior.
    #[prop(optional, into)]
    validation_behavior: Signal<ValidationBehavior>,

    /// Validation errors keyed by field name.
    #[prop(optional, into)]
    validation_errors: Signal<BTreeMap<String, Vec<Error>>>,

    /// Controlled status text shown in the form live region.
    #[prop(optional, into)]
    status_message: Signal<Option<String>>,

    /// Consumer class tokens appended to the form.
    #[prop(optional, into)]
    class: Option<TextProp>,

    /// Fires when the form submit event runs.
    #[prop(optional, into)]
    on_submit: Option<Callback<()>>,

    /// Fires when the form reset event runs.
    #[prop(optional, into)]
    on_reset: Option<Callback<()>>,

    /// Form content.
    children: TypedChildren<T>,
) -> impl IntoView
where
    View<T>: IntoView, […]

> TOOL

tool_result
id: call_hRIfA0eUXwJw6tYlNpJ2Tdb9
```
Chunk ID: 1f1e81
Wall time: 0.0338 seconds
Process exited with code 0
Original token count: 2757
Output:
//! Dioxus Form adapter.

use std::{collections::BTreeMap, rc::Rc};

use ars_components::utility::form;
pub use ars_components::utility::form::{Part, Props, ValidationBehavior};
use ars_forms::validation::Error;
use dioxus::{events::MountedData, prelude::*};
#[cfg(all(feature = "web", target_arch = "wasm32"))]
use web_sys::wasm_bindgen::{JsCast as _, JsValue};

use crate::{
    attr_map_to_dioxus_inline_attrs, callbacks, merge_dioxus_attrs, use_machine,
    use_messages_and_locale, use_stable_id,
};

#[derive(Clone, Copy)]
pub(crate) struct FormContext {
    pub(crate) machine: crate::UseMachineReturn<form::Machine>,
    pub(crate) reset_generation: Signal<u64>,
}

/// Props for the Dioxus [`Form`] component.
#[derive(Props, Clone, PartialEq, Debug)]
pub struct FormProps {
    /// Optional component instance ID.
    #[props(optional, into)]
    pub id: Option<String>,

    /// URL the browser submits the form to.
    #[props(optional, into)]
    pub action: Option<String>,

    /// Optional explicit form role.
    #[props(optional, into)]
    pub role: Option<String>,

    /// Validation display behavior.
    #[props(optional)]
    pub validation_behavior: Option<ValidationBehavior>,

    /// Validation errors keyed by field name.
    #[props(default, into)]
    pub validation_errors: BTreeMap<String, Vec<Error>>,

    /// Controlled status text shown in the form live region.
    #[props(optional, into)]
    pub status_message: Option<String>,

    /// Fires when the form submit event runs.
    #[props(optional, into)]
    pub on_submit: Option<EventHandler>,

    /// Fires when the form reset event runs.
    #[props(optional, into)]
    pub on_reset: Option<EventHandler>,

    /// Global HTML attributes forwarded onto the form.
    #[props(extends = GlobalAttributes)]
    pub attrs: Vec<Attribute>,

    /// Form content. […]

> AGENT

I see one concrete likely audit item already: both adapters still have duplicated native-validity extraction and form-error merging logic in `form.rs`. Under the newer semantic-boundary rule, the plan should explicitly classify that as either renderer glue or moveable shared logic before accepting it.

> TOOL

tool_use exec_command
id: call_UUtBUO1CYKc7mM6AL6nWW9HP
```json
{
  "cmd": "sed -n '300,680p' crates/ars-leptos/src/utility/form.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_m4YWNSfc7JW2g6VcxSuJ9njo
```json
{
  "cmd": "sed -n '340,760p' crates/ars-dioxus/src/utility/form.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_8OmBNwjZBxi0Xof3NMVjeruK
```json
{
  "cmd": "sed -n '1,260p' crates/ars-leptos/src/utility/fieldset.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_vR6MkWXacda7C9Vw8QglD6mW
```json
{
  "cmd": "sed -n '1,300p' crates/ars-dioxus/src/utility/fieldset.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_UUtBUO1CYKc7mM6AL6nWW9HP
```
Chunk ID: 6eba0d
Wall time: 0.3206 seconds
Process exited with code 0
Original token count: 1644
Output:
        let _ = messages;
        let _ = locale;
        BTreeMap::new()
    }
}

#[cfg(target_arch = "wasm32")]
fn native_validation_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Error {
    if validity_flag(element, "valueMissing") {
        return Error::required(messages, locale);
    }

    for error in [
        build_type_mismatch_error(element, messages, locale),
        build_pattern_mismatch_error(element, messages, locale),
        build_length_error(element, messages, locale),
        build_range_error(element, messages, locale),
        build_step_error(element, messages, locale),
    ] {
        if let Some(error) = error {
            return error;
        }
    }

    Error::custom("native", (messages.pattern_error)(locale))
}

#[cfg(target_arch = "wasm32")]
fn build_type_mismatch_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    if !validity_flag(element, "typeMismatch") {
        return None;
    }

    Some(match element.get_attribute("type").as_deref() {
        Some("email") => Error::email(messages, locale),
        Some("url") => Error::url(messages, locale),
        _ => Error::custom("native", (messages.pattern_error)(locale)),
    })
}

#[cfg(target_arch = "wasm32")]
fn build_pattern_mismatch_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    validity_flag(element, "patternMismatch")
        .then(|| element.get_attribute("pattern"))
        .flatten()
        .map(|pattern| Error::pattern(pattern, messages, locale))
}

#[cfg(target_arch = "wasm32")]
fn build_length_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    if validity_flag(element, "tooShort")
        && let Some(min_length) = build_parsed_attr::<usize>(element, "minlength")
    {
        return Some(Error::min_length(min_length, messages, locale));
    }

    if validity_flag(element, "tooLong")
        && let Some(max_length) = build_parsed_attr::<usize>(element, "maxlength")
    {
        return Some(Error::max_length(max_length, messages, locale));
    }

    None
} […]

> TOOL

tool_result
id: call_m4YWNSfc7JW2g6VcxSuJ9njo
```
Chunk ID: 5621d2
Wall time: 0.3202 seconds
Process exited with code 0
Original token count: 1517
Output:
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    if validity_flag(element, "tooShort")
        && let Some(min_length) = build_parsed_attr::<usize>(element, "minlength")
    {
        return Some(Error::min_length(min_length, messages, locale));
    }

    if validity_flag(element, "tooLong")
        && let Some(max_length) = build_parsed_attr::<usize>(element, "maxlength")
    {
        return Some(Error::max_length(max_length, messages, locale));
    }

    None
}

#[cfg(all(feature = "web", target_arch = "wasm32"))]
fn build_range_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    if validity_flag(element, "rangeUnderflow")
        && let Some(min) = build_parsed_attr::<f64>(element, "min")
    {
        return Some(Error::min(min, messages, locale));
    }

    if validity_flag(element, "rangeOverflow")
        && let Some(max) = build_parsed_attr::<f64>(element, "max")
    {
        return Some(Error::max(max, messages, locale));
    }

    None
}

#[cfg(all(feature = "web", target_arch = "wasm32"))]
fn build_step_error(
    element: &web_sys::Element,
    messages: &ars_forms::form::Messages,
    locale: &ars_i18n::Locale,
) -> Option<Error> {
    if !validity_flag(element, "stepMismatch") {
        return None;
    }

    build_parsed_attr::<f64>(element, "step").map(|step| Error::step(step, messages, locale))
}

#[cfg(all(feature = "web", target_arch = "wasm32"))]
fn build_parsed_attr<T: std::str::FromStr>(element: &web_sys::Element, attr: &str) -> Option<T> {
    element
        .get_attribute(attr)
        .and_then(|value| value.parse::<T>().ok())
}

#[cfg(all(feature = "web", target_arch = "wasm32"))]
fn validity_flag(element: &web_sys::Element, flag: &str) -> bool {
    js_sys::Reflect::get(element.as_ref(), &JsValue::from_str("validity"))
        .ok()
        .and_then(|validity| js_sys::Reflect::get(&validity, &JsValue::from_str(flag)).ok())
        .and_then(|flag| flag.as_bool())
        .unwrap_or(false)
}

#[expect(
    clippy::missing_const_for_fn,
    reason = "The wasm implementation reflects on the live submit event's submitter property."
)] […]

> TOOL

tool_result
id: call_8OmBNwjZBxi0Xof3NMVjeruK
```
Chunk ID: 78764d
Wall time: 0.1648 seconds
Process exited with code 0
Original token count: 1495
Output:
//! Leptos Fieldset adapter.

use ars_components::utility::fieldset;
pub use ars_components::utility::fieldset::{Part, Props};
use ars_core::Direction;
use ars_forms::validation::Error;
use leptos::{children::TypedChildren, context::Provider, prelude::*};

use crate::{attr_map_to_leptos_inline_attrs, use_id, use_machine_with_reactive_props};

#[derive(Clone, Copy)]
struct FieldsetContext {
    machine: crate::UseMachineReturn<fieldset::Machine>,
}

#[derive(Clone, Copy)]
pub(crate) struct InheritedFieldsetContext {
    pub(crate) disabled: Signal<bool>,
    pub(crate) invalid: Signal<bool>,
    pub(crate) readonly: Signal<bool>,
}

fn fieldset_context() -> FieldsetContext {
    use_context::<FieldsetContext>()
        .expect("Fieldset subcomponents must be rendered inside <Fieldset/>")
}

/// Leptos Fieldset root component.
#[component]
pub fn Fieldset<T: 'static>(
    /// Optional component instance ID.
    #[prop(optional, into)]
    id: Option<Oco<'static, str>>,

    /// Whether every descendant form control is disabled.
    #[prop(optional, into)]
    disabled: Signal<bool>,

    /// Whether the fieldset is invalid.
    #[prop(optional, into)]
    invalid: Signal<bool>,

    /// Whether the fieldset is read-only.
    #[prop(optional, into)]
    readonly: Signal<bool>,

    /// Fieldset-level validation errors.
    #[prop(optional, into)]
    errors: Signal<Vec<Error>>,

    /// Optional text direction override.
    #[prop(optional)]
    dir: Option<Direction>,

    /// Consumer class tokens appended to the fieldset.
    #[prop(optional, into)]
    class: Option<TextProp>,

    /// Fieldset anatomy children.
    children: TypedChildren<T>,
) -> impl IntoView
where
    View<T>: IntoView,
{
    let id = id.map_or_else(|| use_id("fieldset"), Oco::into_owned);

    let mut props = Props::new().id(&id);

    if let Some(dir) = dir {
        props = props.dir(dir);
    }

    let machine = use_machine_with_reactive_props::<fieldset::Machine>(fieldset_props_signal( […]

> TOOL

tool_result
id: call_vR6MkWXacda7C9Vw8QglD6mW
```
Chunk ID: c0be44
Wall time: 0.0331 seconds
Process exited with code 0
Original token count: 1320
Output:
//! Dioxus Fieldset adapter.

use ars_components::utility::fieldset;
pub use ars_components::utility::fieldset::{Part, Props};
use ars_core::{Direction, HtmlAttr};
use ars_forms::validation::Error;
use dioxus::prelude::*;

use crate::{attr_map_to_dioxus_inline_attrs, merge_dioxus_attrs, use_machine, use_stable_id};

#[derive(Clone, Copy)]
struct FieldsetContext {
    machine: crate::UseMachineReturn<fieldset::Machine>,
}

#[derive(Clone, Copy)]
pub(crate) struct InheritedFieldsetContext {
    pub(crate) disabled: Memo<bool>,
    pub(crate) invalid: Memo<bool>,
    pub(crate) readonly: Memo<bool>,
}

fn fieldset_context() -> FieldsetContext {
    try_use_context::<FieldsetContext>()
        .expect("Fieldset subcomponents must be rendered inside <Fieldset/>")
}

/// Props for the Dioxus [`Fieldset`] component.
#[derive(Props, Clone, PartialEq, Debug)]
pub struct FieldsetProps {
    /// Optional component instance ID.
    #[props(optional, into)]
    pub id: Option<String>,

    /// Whether every descendant form control is disabled.
    #[props(default = false)]
    pub disabled: bool,

    /// Whether the fieldset is invalid.
    #[props(default = false)]
    pub invalid: bool,

    /// Whether the fieldset is read-only.
    #[props(default = false)]
    pub readonly: bool,

    /// Fieldset-level validation errors.
    #[props(default)]
    pub errors: Vec<Error>,

    /// Optional text direction override.
    #[props(optional)]
    pub dir: Option<Direction>,

    /// Global HTML attributes forwarded onto the fieldset.
    #[props(extends = GlobalAttributes)]
    pub attrs: Vec<Attribute>,

    /// Fieldset anatomy children.
    pub children: Element,
}

/// Dioxus Fieldset root component.
#[expect(
    clippy::redundant_closure_for_method_calls,
    reason = "fieldset::Api method items are not lifetime-general enough for […]

> AGENT

Another likely audit target is parity between Leptos reactivity and Dioxus props: the Leptos adapter has explicit reactive attr handling for Field/Fieldset error visibility and input relationships, while Dioxus relies on derived attrs from the machine. The audit plan should include specific reactive-update tests rather than just static SSR checks.

> TOOL

tool_use exec_command
id: call_Gb4QYfSnd3wk8vMWosgNgMGV
```json
{
  "cmd": "sed -n '1,240p' crates/ars-leptos/src/utility/field_support.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_lTsiHdknQKcJKFaEubQLwfZs
```json
{
  "cmd": "sed -n '1,260p' crates/ars-dioxus/src/utility/field_support.rs",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_6qXXnJ5cigcoje4Qt1Ng32q3
```json
{
  "cmd": "rg -n \"Field|Fieldset|Form|field|fieldset|form|validation_errors|on_value_input|reset|required|readonly|disabled|aria-errormessage|status\" crates/ars-leptos/tests crates/ars-dioxus/tests | head -n 240",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_VTmZEThEuVOrcuZuVfiQ6OR5
```json
{
  "cmd": "rg -n \"field_form|Field|Fieldset|Form|validation|email|required|status|field-error|native\" examples crates/ars-e2e/fixtures | head -n 240",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_Gb4QYfSnd3wk8vMWosgNgMGV
```
Chunk ID: 9584be
Wall time: 0.1970 seconds
Process exited with code 0
Original token count: 543
Output:
//! Shared Leptos form-field context support for adapter controls.

use ars_forms::validation::Error;
use leptos::prelude::*;

/// Merged field state inherited from explicit props, Form, and Fieldset.
#[derive(Clone, Copy)]
pub(crate) struct FieldSupport {
    pub(crate) disabled: Signal<bool>,
    pub(crate) invalid: Signal<bool>,
    pub(crate) readonly: Signal<bool>,
    pub(crate) errors: Signal<Vec<Error>>,
}

pub(crate) fn use_field_support(
    disabled: Signal<bool>,
    invalid: Signal<bool>,
    readonly: Signal<bool>,
    errors: Signal<Vec<Error>>,
    name: Option<Oco<'static, str>>,
) -> FieldSupport {
    let form_context = use_context::<super::form::FormContext>();
    let fieldset_context = use_context::<super::fieldset::InheritedFieldsetContext>();

    let merged_errors = Signal::derive(move || {
        merged_validation_errors(errors.get(), name.as_deref(), form_context)
    });

    FieldSupport {
        disabled: Signal::derive(move || {
            disabled.get() || fieldset_context.is_some_and(|ctx| ctx.disabled.get())
        }),
        invalid: Signal::derive(move || {
            invalid.get()
                || fieldset_context.is_some_and(|ctx| ctx.invalid.get())
                || !merged_errors.get().is_empty()
        }),
        readonly: Signal::derive(move || {
            readonly.get() || fieldset_context.is_some_and(|ctx| ctx.readonly.get())
        }),
        errors: merged_errors,
    }
}

fn merged_validation_errors(
    mut errors: Vec<Error>,
    name: Option<&str>,
    form_context: Option<super::form::FormContext>,
) -> Vec<Error> {
    if let Some(name) = name
        && let Some(form_context) = form_context
    {
        let _ = form_context.machine.context_version.get();

        if let Some(form_errors) = form_context
            .machine
            .service
            .read_value()
            .context()
            .validation_errors
            .get(name)
            && !form_errors.is_empty()
        {
            errors.reserve(form_errors.len());
            for error in form_errors {
                errors.push(error.clone());
            }
        }
    }

    errors
}

```

> TOOL

tool_result
id: call_lTsiHdknQKcJKFaEubQLwfZs
```
Chunk ID: 4b3e88
Wall time: 0.2091 seconds
Process exited with code 0
Original token count: 464
Output:
//! Shared Dioxus form-field context support for adapter controls.

use ars_forms::validation::Error;
use dioxus::prelude::*;

/// Merged field state inherited from explicit props, Form, and Fieldset.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct FieldSupport {
    pub(crate) disabled: bool,
    pub(crate) invalid: bool,
    pub(crate) readonly: bool,
    pub(crate) errors: Vec<Error>,
}

pub(crate) fn use_field_support(
    disabled: bool,
    invalid: bool,
    readonly: bool,
    errors: Vec<Error>,
    name: Option<&str>,
) -> FieldSupport {
    let form_context = try_use_context::<super::form::FormContext>();
    let fieldset_context = try_use_context::<super::fieldset::InheritedFieldsetContext>();

    let errors = merged_validation_errors(errors, name, form_context);

    FieldSupport {
        disabled: disabled || fieldset_context.is_some_and(|ctx| (ctx.disabled)()),
        invalid: invalid
            || fieldset_context.is_some_and(|ctx| (ctx.invalid)())
            || !errors.is_empty(),
        readonly: readonly || fieldset_context.is_some_and(|ctx| (ctx.readonly)()),
        errors,
    }
}

fn merged_validation_errors(
    mut errors: Vec<Error>,
    name: Option<&str>,
    form_context: Option<super::form::FormContext>,
) -> Vec<Error> {
    if let Some(name) = name
        && let Some(form_context) = form_context
    {
        let _ = &*form_context.machine.context_version.read();

        if let Some(form_errors) = form_context
            .machine
            .service
            .peek()
            .context()
            .validation_errors
            .get(name)
            && !form_errors.is_empty()
        {
            errors.reserve(form_errors.len());
            form_errors
                .iter()
                .for_each(|error| errors.push(error.clone()));
        }
    }

    errors
}

```

> TOOL

tool_result
id: call_6qXXnJ5cigcoje4Qt1Ng32q3
```
Chunk ID: cf4b97
Wall time: 0.2134 seconds
Process exited with code 0
Original token count: 5323
Output:
crates/ars-leptos/tests/button.rs:74:        html.contains(r#"aria-disabled="true""#),
crates/ars-leptos/tests/button.rs:75:        "missing loading-disabled state: {html}"
crates/ars-leptos/tests/button.rs:82:        html.contains(r#"role="status""#),
crates/ars-leptos/tests/button.rs:83:        "missing status role: {html}"
crates/ars-leptos/tests/button.rs:100:fn button_renders_disabled_and_form_override_attrs() {
crates/ars-leptos/tests/button.rs:106:            disabled=true
crates/ars-leptos/tests/button.rs:108:            form="account-form"
crates/ars-leptos/tests/button.rs:111:            form_action=action
crates/ars-leptos/tests/button.rs:112:            form_method=button::FormMethod::Post
crates/ars-leptos/tests/button.rs:113:            form_enc_type=button::FormEncType::MultipartFormData
crates/ars-leptos/tests/button.rs:114:            form_target=button::FormTarget::Self_
crates/ars-leptos/tests/button.rs:115:            form_no_validate=true
crates/ars-leptos/tests/button.rs:123:        r#" disabled"#,
crates/ars-leptos/tests/button.rs:124:        r#"aria-disabled="true""#,
crates/ars-leptos/tests/button.rs:125:        r#"data-ars-disabled"#,
crates/ars-leptos/tests/button.rs:127:        r#"form="account-form""#,
crates/ars-leptos/tests/button.rs:130:        r#"formaction="/submit""#,
crates/ars-leptos/tests/button.rs:131:        r#"formmethod="post""#,
crates/ars-leptos/tests/button.rs:132:        r#"formenctype="multipart/form-data""#,
crates/ars-leptos/tests/button.rs:133:        r#"formtarget="_self""#,
crates/ars-leptos/tests/button.rs:134:        r#"formnovalidate"#,
crates/ars-leptos/tests/button.rs:172:            form="ergonomic-form"
crates/ars-leptos/tests/button.rs:175:            form_action=action
crates/ars-leptos/tests/button.rs:188:        r#"form="ergonomic-form""#,
crates/ars-leptos/tests/button.rs:191:        r#"formaction="/submit""#,
crates/ars-leptos/tests/button.rs:240:        <ButtonAsChild id="docs-link" disabled=true>
crates/ars-leptos/tests/button.rs:248:        r#"form="external-form""#,
crates/ars-leptos/tests/button.rs:251:        r#"formaction="/submit""#,
crates/ars-leptos/tests/button.rs:252:        r#"formmethod="post""#,
crates/ars-leptos/tests/button.rs:253:        r#"formenctype="application/x-www-form-urlencoded""#,
crates/ars-leptos/tests/button.rs:254:        r#"formtarget="_self""#,
crates/ars-leptos/tests/button.rs:255:        r#"formnovalidate"#,
crates/ars-leptos/tests/button.rs:256:        " disabled",
crates/ars-dioxus/tests/button.rs:74:        r#"aria-disabled="true""#,
crates/ars-dioxus/tests/button.rs:76:        r#"role="status""#,
crates/ars-dioxus/tests/button.rs:86:fn button_renders_disabled_and_form_override_attrs() {
crates/ars-dioxus/tests/button.rs:91:                disabled: true,
crates/ars-dioxus/tests/button.rs:93:                form: "account-form",
crates/ars-dioxus/tests/button.rs:96:                form_action: "/submit",
crates/ars-dioxus/tests/button.rs:97:                form_method: button::FormMethod::Post,
crates/ars-dioxus/tests/button.rs:98:                form_enc_type: button::FormEncType::MultipartFormData,
crates/ars-dioxus/tests/button.rs:99:                form_target: button::FormTarget::Self_,
crates/ars-dioxus/tests/button.rs:100:                form_no_validate: true,
crates/ars-dioxus/tests/button.rs:109:        r#"disabled"#,
crates/ars-dioxus/tests/button.rs:110:        r#"aria-disabled="true""#,
crates/ars-dioxus/tests/button.rs:111:        r#"data-ars-disabled"#,
crates/ars-dioxus/tests/button.rs:113:        r#"form="account-form""#,
crates/ars-dioxus/tests/button.rs:116:        r#"formaction="/submit""#,
crates/ars-dioxus/tests/button.rs:117:        r#"formmethod="post""#,
crates/ars-dioxus/tests/button.rs:118:        r#"formenctype="multipart/form-data""#,
crates/ars-dioxus/tests/button.rs:119:        r#"formtarget="_self""#,
crates/ars-dioxus/tests/button.rs:120:        r#"formnovalidate"#,
crates/ars-dioxus/tests/button.rs:159:                form: "ergonomic-form",
crates/ars-dioxus/tests/button.rs:162:                form_action: "/submit",
crates/ars-dioxus/tests/button.rs:176:        r#"form="ergonomic-form""#,
crates/ars-dioxus/tests/button.rs:179:        r#"formaction="/submit""#,
crates/ars-dioxus/tests/button.rs:249:        r#"form="external-form""#,
crates/ars-dioxus/tests/button.rs:252:        r#"formaction="/submit""#,
crates/ars-dioxus/tests/button.rs:253:        r#"formmethod="post""#,
crates/ars-dioxus/tests/button.rs:254:        r#"formenctype="application/x-www-form-urlencoded""#,
crates/ars-dioxus/tests/button.rs:255:        r#"formtarget="_self""#,
crates/ars-dioxus/tests/button.rs:256:        r#"formnovalidate"#,
crates/ars-leptos/tests/form.rs:1://! SSR tests for the Leptos Form adapter.
crates/ars-leptos/tests/form.rs:7:use ars_components::utility::form;
crates/ars-leptos/tests/form.rs:8:use ars_forms::validation::Error;
crates/ars-leptos/tests/form.rs:10:    field::{ErrorMessage, Field, Input, Label},
crates/ars-leptos/tests/form.rs:11:    form::Form,
crates/ars-leptos/tests/form.rs:25:fn form_renders_root_and_status_region() {
crates/ars-leptos/tests/form.rs:28:            <Form
crates/ars-leptos/tests/form.rs:29:                id="account-form"
crates/ars-leptos/tests/form.rs:32:                validation_behavior=form::ValidationBehavior::Aria
crates/ars-leptos/tests/form.rs:33:                validation_errors=BTreeMap::from([
crates/ars-leptos/tests/form.rs:36:                status_message="Ready"
crates/ars-leptos/tests/form.rs:37:                class="account-form" […]

> TOOL

tool_result
id: call_VTmZEThEuVOrcuZuVfiQ6OR5
```
Chunk ID: 483e4f
Wall time: 0.0683 seconds
Process exited with code 0
Original token count: 6630
Output:
examples/widgets-ownership.md:17:not implement component-owned validation, ARIA relationships, keyboard or focus
examples/widgets-leptos-tailwind/src/categories/input.rs:8:    FormStatusEmpty,
examples/widgets-leptos-tailwind/src/categories/input.rs:16:    #[translate(en_US = "Forms", pt_BR = "Formulários")]
examples/widgets-leptos-tailwind/src/categories/input.rs:17:    Forms,
examples/widgets-leptos-tailwind/src/categories/input.rs:80:        en_US = "Select the required value before submitting.",
examples/widgets-leptos-tailwind/src/categories/input.rs:97:    #[translate(en_US = "Form reset.", pt_BR = "Formulário redefinido.")]
examples/widgets-leptos-tailwind/src/categories/input.rs:98:    FormReset,
examples/widgets-leptos-tailwind/src/categories/input.rs:106:    let (form_required, set_form_required) = signal(State::Checked);
examples/widgets-leptos-tailwind/src/categories/input.rs:108:    let (form_status, set_form_status) = signal(InputText::FormStatusEmpty);
examples/widgets-leptos-tailwind/src/categories/input.rs:109:    let form_status_text = t(form_status);
examples/widgets-leptos-tailwind/src/categories/input.rs:110:    let required_invalid = Signal::derive(move || {
examples/widgets-leptos-tailwind/src/categories/input.rs:111:        form_submit_attempted.get() && form_required.get() != State::Checked
examples/widgets-leptos-tailwind/src/categories/input.rs:139:                    <Checkbox id="checkbox-required" required=true>
examples/widgets-leptos-tailwind/src/categories/input.rs:174:                <Form
examples/widgets-leptos-tailwind/src/categories/input.rs:179:                        set_form_status
examples/widgets-leptos-tailwind/src/categories/input.rs:181:                                if form_required.get() != State::Checked {
examples/widgets-leptos-tailwind/src/categories/input.rs:192:                        set_form_required.set(State::Checked);
examples/widgets-leptos-tailwind/src/categories/input.rs:194:                        set_form_status.set(InputText::FormReset);
examples/widgets-leptos-tailwind/src/categories/input.rs:197:                    <h3>{t(InputText::Forms)}</h3>
examples/widgets-leptos-tailwind/src/categories/input.rs:210:                        checked=form_required
examples/widgets-leptos-tailwind/src/categories/input.rs:212:                        invalid=required_invalid
examples/widgets-leptos-tailwind/src/categories/input.rs:216:                                    required_invalid.get()
examples/widgets-leptos-tailwind/src/categories/input.rs:220:                        on_checked_change=move |next| set_form_required.set(next)
examples/widgets-leptos-tailwind/src/categories/input.rs:232:                    <p>{form_status_text}</p>
examples/widgets-leptos-tailwind/src/categories/input.rs:233:                </Form>
examples/widgets-leptos-css/src/categories/input.rs:8:    FormStatusEmpty,
examples/widgets-leptos-css/src/categories/input.rs:16:    #[translate(en_US = "Forms", pt_BR = "Formulários")]
examples/widgets-leptos-css/src/categories/input.rs:17:    Forms,
examples/widgets-leptos-css/src/categories/input.rs:80:        en_US = "Select the required value before submitting.",
examples/widgets-leptos-css/src/categories/input.rs:97:    #[translate(en_US = "Form reset.", pt_BR = "Formulário redefinido.")]
examples/widgets-leptos-css/src/categories/input.rs:98:    FormReset,
examples/widgets-leptos-css/src/categories/input.rs:106:    let (form_required, set_form_required) = signal(State::Checked);
examples/widgets-leptos-css/src/categories/input.rs:108:    let (form_status, set_form_status) = signal(InputText::FormStatusEmpty);
examples/widgets-leptos-css/src/categories/input.rs:109:    let form_status_text = t(form_status);
examples/widgets-leptos-css/src/categories/input.rs:110:    let required_invalid =
examples/widgets-leptos-css/src/categories/input.rs:111:        move || form_submit_attempted.get() && form_required.get() != State::Checked;
examples/widgets-leptos-css/src/categories/input.rs:139:                    <Checkbox id="checkbox-required" required=true>
examples/widgets-leptos-css/src/categories/input.rs:174:                <Form
examples/widgets-leptos-css/src/categories/input.rs:179:                        set_form_status
examples/widgets-leptos-css/src/categories/input.rs:181:                                if form_required.get() != State::Checked {
examples/widgets-leptos-css/src/categories/input.rs:192: […]

> AGENT

The test surface is broader than I expected: there are SSR tests, wasm browser tests, and E2E assertions for Field/Form, including the earlier error-count regression. I’m going to verify the original issue acceptance criteria and the current component/spec shape so the plan can distinguish “audit only” from “audit plus fix drift.”

> TOOL

tool_use exec_command
id: call_B6IPoDg2M0TioLhbkEuAt9c3
```json
{
  "cmd": "gh issue view 332 --json number,title,state,body,labels,url",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_v8K8KKfKuA9u5PO5Y9PniOf0
```json
{
  "cmd": "gh issue view 423 --json number,title,state,body,labels,url",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_N9hYRgKWeZVyolCZj6L3nbL6
```json
{
  "cmd": "cargo xtask spec info field",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 30000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_npurCrJeBC1OdPhWSw5kh8ik
```json
{
  "cmd": "cargo xtask spec info fieldset",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 30000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_GotyAulqsR5ikIgc6K0e6R5k
```json
{
  "cmd": "cargo xtask spec info form",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 30000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_B6IPoDg2M0TioLhbkEuAt9c3
```
Chunk ID: 3b65ae
Wall time: 0.9626 seconds
Process exited with code 0
Original token count: 520
Output:
{"body":"**Epic: #303 (Leptos utility adapter components)**\n\n## Goal\n\nImplement the Leptos adapter for Field, Fieldset, and Form: reactive component shell(s) wiring the agnostic core machine to Leptos props, children, context, event mapping, and SSR.\n\n## Out of scope\n\nOther framework adapters (Dioxus).\n\n## Spec refs\n\n- `spec/leptos-components/utility/field.md`\n- `spec/leptos-components/utility/fieldset.md`\n- `spec/leptos-components/utility/form.md`\n- `spec/foundation/08-adapter-leptos.md`\n\n## Depends on\n\n- #206 (Field, Fieldset, and Form agnostic core)\n- #190 (ArsProvider context and reactive props)\n- #191 (Leptos adapter utilities)\n\n## Layer\n\nAdapter\n\n## Framework\n\nLeptos\n\n## Test tier\n\nAdapter\n\n## Fibonacci points\n\n3\n\n## Tests to add first\n\n- Adapter component renders with correct ARIA attributes from core ConnectApi.\n- Prop sync: controlled Signal props update machine state reactively.\n- SSR hydration stability: server and client markup match.\n- Axe-core audit: rendered component output passes in the adapter harness using the component root `data-ars-scope` selector.\n\n## Acceptance criteria\n\n- Leptos `#[component]` matches the public API in the adapter spec.\n- Part mapping, attr merge, and event mapping match adapter spec.\n- SSR produces hydration-stable markup.\n- All public types documented per workspace `missing_docs` lint.\n- All named tests pass with zero warnings.\n\n- Adapter tests use the framework-specific test harness entrypoints and shared `ars-test-harness` helpers where applicable, rather than bespoke DOM test setup.\n\n## Spec impact\n\nNo […]

> TOOL

tool_result
id: call_v8K8KKfKuA9u5PO5Y9PniOf0
```
Chunk ID: a525ee
Wall time: 0.7753 seconds
Process exited with code 0
Original token count: 520
Output:
{"body":"**Epic: #407 (Dioxus utility adapter components)**\n\n## Goal\n\nImplement the Dioxus adapter for Field, Fieldset, and Form: reactive component shell(s) wiring the agnostic core machine to Dioxus props, children, context, event mapping, and SSR.\n\n## Out of scope\n\nOther framework adapters (Leptos).\n\n## Spec refs\n\n- `spec/dioxus-components/utility/field.md`\n- `spec/dioxus-components/utility/fieldset.md`\n- `spec/dioxus-components/utility/form.md`\n- `spec/foundation/09-adapter-dioxus.md`\n\n## Depends on\n\n- #206 (Field, Fieldset, and Form agnostic core)\n- #193 (ArsProvider context and reactive props)\n- #194 (Dioxus adapter utilities)\n\n## Layer\n\nAdapter\n\n## Framework\n\nDioxus\n\n## Test tier\n\nAdapter\n\n## Fibonacci points\n\n3\n\n## Tests to add first\n\n- Adapter component renders with correct ARIA attributes from core ConnectApi.\n- Prop sync: controlled Signal props update machine state reactively.\n- SSR hydration stability: server and client markup match.\n- Axe-core audit: rendered component output passes in the adapter harness using the component root `data-ars-scope` selector.\n\n## Acceptance criteria\n\n- Dioxus `#[component]` matches the public API in the adapter spec.\n- Part mapping, attr merge, and event mapping match adapter spec.\n- SSR produces hydration-stable markup.\n- All public types documented per workspace `missing_docs` lint.\n- All named tests pass with zero warnings.\n\n- Adapter tests use the framework-specific test harness entrypoints and shared `ars-test-harness` helpers where applicable, rather than bespoke DOM test setup.\n\n## Spec impact\n\nNo […]

> TOOL

tool_result
id: call_N9hYRgKWeZVyolCZj6L3nbL6
```
Chunk ID: 1a80cd
Wall time: 21.9043 seconds
Process exited with code 0
Original token count: 885
Output:
    Updating crates.io index
    Blocking waiting for file lock on package cache
     Locking 826 packages to latest Rust 1.90 compatible versions
      Adding generic-array v0.14.7 (available: v0.14.9)
      Adding matchit v0.8.4 (available: v0.8.6)
      Adding toml v0.8.2 (available: v0.8.23)
      Adding toml_datetime v0.6.3 (available: v0.6.11)
      Adding toml_edit v0.20.2 (available: v0.20.7)
      Adding webkit2gtk v2.0.1 (available: v2.0.2)
      Adding webkit2gtk-sys v2.0.1 (available: v2.0.2)
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on shared package cache
   Compiling unicode-ident v1.0.24
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.45
   Compiling serde_core v1.0.228
   Compiling memchr v2.8.2
   Compiling pin-project-lite v0.2.17
   Compiling strsim v0.11.1
   Compiling zmij v1.0.21
   Compiling autocfg v1.5.1
   Compiling futures-sink v0.3.32
   Compiling futures-core v0.3.32
   Compiling itoa v1.0.18
   Compiling ident_case v1.0.1
   Compiling serde v1.0.228
   Compiling slab v0.4.12
   Compiling futures-task v0.3.32
   Compiling futures-io v0.3.32
   Compiling ref-cast v1.0.25
   Compiling serde_json v1.0.150
   Compiling futures-channel v0.3.32
   Compiling utf8parse v0.2.2
   Compiling anstyle-parse v1.0.0
   Compiling colorchoice v1.0.5
   Compiling num-traits v0.2.19
   Compiling anstyle-query v1.1.5
   Compiling bytes v1.11.1
   Compiling thiserror v2.0.18
   Compiling anstyle v1.0.14
   Compiling once_cell v1.21.4
   Compiling is_terminal_polyfill v1.70.2
   Compiling anstream v1.0.0
   Compiling tracing-core v0.1.36
   Compiling aho-corasick v1.1.4 […]

> TOOL

tool_result
id: call_npurCrJeBC1OdPhWSw5kh8ik
```
Chunk ID: 652715
Wall time: 21.6362 seconds
Process exited with code 0
Original token count: 178
Output:
    Blocking waiting for file lock on package cache
    Updating crates.io index
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on build directory
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 20.73s
     Running `target/debug/xtask spec info fieldset`
component: fieldset
path: components/utility/fieldset.md
category: utility
foundation_deps: [architecture, accessibility, forms]
shared_deps: []
related: [field, form]
component_deps: []
leptos_adapter: leptos-components/utility/fieldset.md
dioxus_adapter: dioxus-components/utility/fieldset.md

```

> TOOL

tool_result
id: call_GotyAulqsR5ikIgc6K0e6R5k
```
Chunk ID: a24e59
Wall time: 21.4691 seconds
Process exited with code 0
Original token count: 192
Output:
    Blocking waiting for file lock on package cache
    Updating crates.io index
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on package cache
    Blocking waiting for file lock on shared package cache
    Blocking waiting for file lock on build directory
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 20.73s
     Running `target/debug/xtask spec info form`
component: form
path: components/utility/form.md
category: utility
foundation_deps: [architecture, accessibility, forms]
shared_deps: []
related: [field, fieldset, form-submit]
component_deps: []
leptos_adapter: leptos-components/utility/form.md
dioxus_adapter: dioxus-components/utility/form.md

```

> AGENT

The original issues were narrow 3-point adapter tasks, but the repo’s current adapter workflow now defines a much larger “complete” bar. The key planning choice is whether this pass should be a strict retroactive upgrade to the Checkbox-era bar or a bounded risk audit that files/lands only actual defects and spec drift.

> TOOL

tool_use request_user_input
id: call_omGRBMpjrlX3VmRHRkpguGRJ
```json
{
  "questions": [
    {
      "id": "audit_depth",
      "header": "Depth",
      "question": "How strict should this Field/Fieldset/Form audit be against the new Checkbox-era adapter workflow?",
      "options": [
        {
          "label": "Retrofit fully (Recommended)",
          "description": "Treat the current workflow as the bar and plan to fix every drift found in the same PR."
        },
        {
          "label": "Defect-focused",
          "description": "Audit the new workflow surfaces, but only plan fixes for concrete user-visible/spec/test defects."
        },
        {
          "label": "Report only",
          "description": "Produce a written audit with findings and recommendations, without planning code changes yet."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: call_omGRBMpjrlX3VmRHRkpguGRJ
```
{"answers":{"audit_depth":{"answers":["Retrofit fully (Recommended)"]}}}
```

> AGENT

I’ll plan this as a full retrofit audit: the implementer should compare Field/Fieldset/Form against the current adapter delivery workflow and land all drift, tests, sketch updates, examples, and validation fixes in one PR. I’m reading the planning skill now so the final plan is implementation-ready rather than just an audit outline.

> TOOL

tool_use exec_command
id: call_WSXEKeVxu89PCL30VchTusij
```json
{
  "cmd": "sed -n '1,260p' /Users/ericson/.claude/skills/writing-plans/SKILL.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_result
id: call_WSXEKeVxu89PCL30VchTusij
```
Chunk ID: e7b7ef
Wall time: 0.0412 seconds
Process exited with code 0
Original token count: 1512
Output:
---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should […]

> AGENT

I have enough to finalize the implementation plan. I’ll keep it scoped to a full retrofit audit for Field, Fieldset, and Form, with the known risk areas called out so an implementer does not have to rediscover them.

> TOOL

tool_use exec_command
id: call_Q4VrxvpCwkPCQMmVS1BHRbVo
```json
{
  "cmd": "nl -ba /Users/ericson/.codex/memories/MEMORY.md | sed -n '16,24p;35,38p;53,53p'",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 6000
}
```

> TOOL

tool_use exec_command
id: call_jmMMfdW6a25scnE8O0Dd6CW9
```json
{
  "cmd": "nl -ba /Users/ericson/.codex/memories/rollout_summaries/REDACTED.md | sed -n '1,26p;49,74p;99,148p'",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_Q4VrxvpCwkPCQMmVS1BHRbVo
```
Chunk ID: 7ac27f
Wall time: 0.1652 seconds
Process exited with code 0
Original token count: 659
Output:
    16	## Task 2: Implement Field, Fieldset, and Form adapter work for Leptos (#332) and Dioxus (#423), with review-fix follow-through
    17	
    18	### rollout_summary_files
    19	
    20	- rollout_summaries/REDACTED.md (cwd=/Users/ericson/.codex/worktrees/3efe/ars-ui, rollout_path=/Users/ericson/.codex/sessions/2026/06/04/rollout-2026-06-04T14-33-56-019e93b2-e997-7881-b092-7b1fb63bf491.jsonl, updated_at=2026-06-07T02:45:47+00:00, thread_id=019e93b2-e997-7881-b092-7b1fb63bf491, combined cross-adapter delivery, focused wasm validation, review-thread cleanup, and Coverage still pending at stop time)
    21	
    22	### keywords
    23	
    24	- ars-ui, leptos, dioxus, adapter delivery, field, fieldset, form, issue-332, issue-423, wasm-bindgen-test-runner, browser tests, ButtonAsChild, raw oninput, status-region, review threads, @codex review
    35	- the fastest orientation loop for this task family was: read the live GitHub issues, run `cargo xtask spec info <component>`, `cargo xtask spec component-deps <component> --adapter <adapter>`, and `cargo xtask spec issue-deps --adapter <adapter> --component <component> --dry-run`, then read `docs/implementation/adapter-components/`, `docs/implementation/adapter-contract.md`, and the relevant component/adapter specs before editing [Task 1][Task 2]
    36	- for Checkbox, `cargo xtask spec info checkbox` mapped directly to `spec/components/input/checkbox.md`, `spec/leptos-components/input/checkbox.md`, and `spec/dioxus-components/input/checkbox.md`; `component-deps` returned none, while `issue-deps` matched the issue-body blocked-by graphs `[190,191,229]` for Leptos and `[193,194,229]` for Dioxus [Task 1]
    37	- for Field in this rollout, `cargo xtask spec component-deps field --adapter leptos|dioxus` returned `component_deps: […]

> TOOL

tool_result
id: call_jmMMfdW6a25scnE8O0Dd6CW9
```
Chunk ID: 03258a
Wall time: 0.0382 seconds
Process exited with code 0
Original token count: 695
Output:
     1	thread_id: 019e93b2-e997-7881-b092-7b1fb63bf491
     2	updated_at: 2026-06-07T02:45:47+00:00
     3	rollout_path: /Users/ericson/.codex/sessions/2026/06/04/rollout-2026-06-04T14-33-56-019e93b2-e997-7881-b092-7b1fb63bf491.jsonl
     4	cwd: /Users/ericson/.codex/worktrees/3efe/ars-ui
     5	git_branch: codex/issue-332-423-field-form-adapters
     6	
     7	# Implemented Leptos and Dioxus Field/Fieldset/Form adapter work for issues #332 and #423, then fixed review regressions and pushed a follow-up commit.
     8	
     9	Rollout context: the user asked to "Implement tasks #332 and #423" in `/Users/ericson/.codex/worktrees/3efe/ars-ui`. The work was framed as adapter-level component delivery, so the agent read the live GitHub issues, the adapter workflow docs, the Leptos/Dioxus framework skills, the adapter contract docs, and the component specs before editing. The two issues were closely related: #332 covered the Leptos adapter for Field/Fieldset/Form; #423 covered the Dioxus adapter for the same component family. Dependency checks confirmed both were unblocked and matched the issue bodies.
    10	
    11	## Task 1: Leptos + Dioxus Field/Fieldset/Form adapter implementation and follow-up fixes
    12	
    13	Outcome: partial
    14	
    15	Preference signals:
    16	- The user asked for both issue numbers in one request: "Implement tasks #332 and #423" -> the rollout treated the two adapters as a single coordinated delivery rather than separate threads.
    17	- […]

> TOOL

tool_use exec_command
id: call_8w8aRsjFButFgxJbAc2ckbV8
```json
{
  "cmd": "wc -l /Users/ericson/.codex/memories/rollout_summaries/REDACTED.md",
  "workdir": "/Users/ericson/.codex/worktrees/55bb/ars-ui",
  "yield_time_ms": 10000,
  "max_output_tokens": 2000
}
```

> TOOL

tool_result
id: call_8w8aRsjFButFgxJbAc2ckbV8
```
Chunk ID: 06edf9
Wall time: 0.0609 seconds
Process exited with code 0
Original token count: 34
Output:
      30 /Users/ericson/.codex/memories/rollout_summaries/REDACTED.md

```

> AGENT

<proposed_plan>
# Field/Fieldset/Form Adapter Retrofit Audit Plan

## Summary
Run a full retrofit audit of the existing Leptos and Dioxus `Field`, `Fieldset`, and `Form` adapters against the current Checkbox-era adapter delivery workflow. Treat every finding as in-scope for the same PR: spec drift, semantic-boundary drift, missing tests, stale examples, incomplete browser evidence, and parity-matrix gaps all get fixed before handoff.

Create a new issue-backed task for this audit rather than reopening closed #332/#423. The PR should close that new audit issue and reference #332/#423 as prior implementation context.

## Key Changes
- Re-read, in order, `docs/implementation/adapter-component-delivery.md`, every linked `docs/implementation/adapter-components/*.md` workflow file, all three checklists, `docs/implementation/sketches/332-423-field-form-counterpart-sketch.md`, and the component/adapter specs for `field`, `fieldset`, and `form`.
- Compare the current implementation in `crates/ars-leptos/src/utility/{field,fieldset,form,field_support}.rs` and `crates/ars-dioxus/src/utility/{field,fieldset,form,field_support}.rs` against the specs and current workflow.
- Explicitly audit these known risk areas:
  - duplicated native-validation/error-merging logic in both adapter `form.rs` files;
  - Leptos vs Dioxus reactive update parity for validation errors, form validation maps, fieldset inherited state, input relationships, and reset behavior;
  - Dioxus hook-order and global-attribute/event-strip behavior;
  - whether Field/Form examples remain “consumer applications” and do not reimplement component-owned validation or ARIA policy;
  - whether current E2E/widget evidence still matches the final outcome matrix after […]