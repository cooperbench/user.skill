> SYSTEM

# AGENTS.md instructions for /Users/ericson/.codex/worktrees/55bb/ars-ui <INSTRUCTIONS> ## Approach - Read existing files before writing. Don't re-read unless changed. - Thorough in reasoning, concise in output. - Skip files over 100KB unless required. - No sycophantic openers or closing fluff. - No emojis or em-dashes. - Do not guess APIs, versions, flags, commit SHAs, or package names. Verify by reading code or docs before asserting. --- project-doc --- # ars-ui ## Project Overview Rust frontend component library using state machines, framework-agnostic core with Leptos/Dioxus adapters. ## Current Phase The repo is now in active implementation, not spec drafting only. Agents working on implementation should use the GitHub Project roadmap and issue backlog as the execution source of truth: - Use the GitHub Project `ars-ui implementation roadmap` to understand active epics, task breakdown, dependencies, status, and iteration planning. - Prefer picking a single issue-backed task that is unblocked, sized, and scoped for independent delivery. - Do not start work from an epic issue unless the user explicitly asks for planning or further decomposition. - Do not start a task that is blocked by unresolved GitHub issue dependencies. - Treat native GitHub issue dependencies as the blocker graph and the issue body acceptance […]

> DEVELOPER

Recently we did several improvements on how we design and implement our adapter level components, the first one following those new improvements was the Checkbox one, for both adapters. Now I wanna do an audit of the other components that were already implemented. Starting with the field, fieldset and form components.

> AGENT

I’ll ground this in the existing workflow and prior adapter work first, then turn it into an audit plan rather than changing files in Plan Mode. I’m using the repo-specific adapter context plus the Superpowers planning guidance because this is a workflow/spec audit, not a one-off code tweak.

> AGENT

The memory index points to the original Field/Fieldset/Form adapter delivery and one review-found defect: form error counts accidentally included fieldset/container invalid states instead of only named native controls. I’m going to inspect the current adapter workflow docs and the shipped Field/Form code to make the audit plan line up with today’s contract.

> AGENT

The current checkout is clean, so the plan does not need to account for local uncommitted changes. Next I’m reading the adapter delivery/audit guidance and a representative slice of the Field/Form implementation and tests to identify what the audit should verify against the newer Checkbox standard.

> AGENT

The newer workflow adds several audit dimensions that probably were not present, or were lighter, when Field/Form first landed: durable browser evidence, explicit consumer-reality review, composition integration, semantic-boundary checks, styled-template boundary checks, and a final outcome matrix with no unknown/workaround rows. I’m checking whether the current Field/Form artifacts already have those pieces or just the older baseline.

> AGENT

The existing sketch is unusually complete for that earlier work and already records the three-pass parity loop, but it also has an addendum that later narrowed the Tailwind examples back to a “low-level relationship showcase.” The audit should therefore test the current repo against the newest workflow, not simply assume the old sketch remains true.

> AGENT

I see one concrete likely audit item already: both adapters still have duplicated native-validity extraction and form-error merging logic in `form.rs`. Under the newer semantic-boundary rule, the plan should explicitly classify that as either renderer glue or moveable shared logic before accepting it.

> AGENT

Another likely audit target is parity between Leptos reactivity and Dioxus props: the Leptos adapter has explicit reactive attr handling for Field/Fieldset error visibility and input relationships, while Dioxus relies on derived attrs from the machine. The audit plan should include specific reactive-update tests rather than just static SSR checks.

> AGENT

The test surface is broader than I expected: there are SSR tests, wasm browser tests, and E2E assertions for Field/Form, including the earlier error-count regression. I’m going to verify the original issue acceptance criteria and the current component/spec shape so the plan can distinguish “audit only” from “audit plus fix drift.”

> AGENT

The original issues were narrow 3-point adapter tasks, but the repo’s current adapter workflow now defines a much larger “complete” bar. The key planning choice is whether this pass should be a strict retroactive upgrade to the Checkbox-era bar or a bounded risk audit that files/lands only actual defects and spec drift.

> AGENT

I’ll plan this as a full retrofit audit: the implementer should compare Field/Fieldset/Form against the current adapter delivery workflow and land all drift, tests, sketch updates, examples, and validation fixes in one PR. I’m reading the planning skill now so the final plan is implementation-ready rather than just an audit outline.

> AGENT

I have enough to finalize the implementation plan. I’ll keep it scoped to a full retrofit audit for Field, Fieldset, and Form, with the known risk areas called out so an implementer does not have to rediscover them.

> AGENT

<proposed_plan> # Field/Fieldset/Form Adapter Retrofit Audit Plan ## Summary Run a full retrofit audit of the existing Leptos and Dioxus `Field`, `Fieldset`, and `Form` adapters against the current Checkbox-era adapter delivery workflow. Treat every finding as in-scope for the same PR: spec drift, semantic-boundary drift, missing tests, stale examples, incomplete browser evidence, and parity-matrix gaps all get fixed before handoff. Create a new issue-backed task for this audit rather than reopening closed #332/#423. The PR should close that new audit issue and reference #332/#423 as prior implementation context. ## Key Changes - Re-read, in order, `docs/implementation/adapter-component-delivery.md`, every linked `docs/implementation/adapter-components/*.md` workflow file, all three checklists, `docs/implementation/sketches/332-423-field-form-counterpart-sketch.md`, and the component/adapter specs for `field`, `fieldset`, and `form`. - Compare the current implementation in `crates/ars-leptos/src/utility/{field,fieldset,form,field_support}.rs` and `crates/ars-dioxus/src/utility/{field,fieldset,form,field_support}.rs` against the specs and current workflow. - Explicitly audit these known risk areas: - duplicated native-validation/error-merging logic in both adapter `form.rs` files; - Leptos vs Dioxus reactive update parity for validation errors, form validation maps, fieldset inherited state, input relationships, and reset behavior; - Dioxus hook-order and global-attribute/event-strip behavior; - whether Field/Form examples remain “consumer applications” and do not reimplement component-owned validation or ARIA policy; - whether current E2E/widget evidence still matches the final outcome matrix after […]