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

> DEVELOPER

PLEASE IMPLEMENT THIS PLAN: # Field/Fieldset/Form Adapter Retrofit Audit Plan ## Summary Run a full retrofit audit of the existing Leptos and Dioxus `Field`, `Fieldset`, and `Form` adapters against the current Checkbox-era adapter delivery workflow. Treat every finding as in-scope for the same PR: spec drift, semantic-boundary drift, missing tests, stale examples, incomplete browser evidence, and parity-matrix gaps all get fixed before handoff. Create a new issue-backed task for this audit rather than reopening closed #332/#423. The PR should close that new audit issue and reference #332/#423 as prior implementation context. ## Key Changes - Re-read, in order, `docs/implementation/adapter-component-delivery.md`, every linked `docs/implementation/adapter-components/*.md` workflow file, all three checklists, `docs/implementation/sketches/332-423-field-form-counterpart-sketch.md`, and the component/adapter specs for `field`, `fieldset`, and `form`. - Compare the current implementation in `crates/ars-leptos/src/utility/{field,fieldset,form,field_support}.rs` and `crates/ars-dioxus/src/utility/{field,fieldset,form,field_support}.rs` against the specs and current workflow. - Explicitly audit these known risk areas: - duplicated native-validation/error-merging logic in both adapter `form.rs` files; - Leptos vs Dioxus reactive update parity for validation errors, form validation maps, fieldset inherited state, input relationships, and reset behavior; - Dioxus hook-order and global-attribute/event-strip behavior; - whether Field/Form examples remain “consumer applications” and do not reimplement component-owned validation or ARIA policy; - whether current E2E/widget evidence still matches the final […]

> AGENT

I’ll execute this as an implementation task now. First I’m loading the execution/TDD/framework skills and the project audit skill, then I’ll re-read the adapter workflow docs and start with concrete drift tests before code changes.

> AGENT

I’m using the executing-plans skill to implement this plan. The plan is coherent; the only operational caveat is that creating the GitHub issue and moving the board item may need network escalation, so I’ll try the normal `gh` path first and request approval only if the sandbox blocks it.

> AGENT

I’m reading the full adapter workflow set now. This is intentionally front-loaded because the retrofit bar lives mostly in those docs, not in the older #332/#423 issue bodies.

> AGENT

The checkout is clean but currently detached (`HEAD (no branch)`). I’m creating a scoped work branch before editing so the audit does not happen on a detached state.

> AGENT

Branch is now `codex/field-form-adapter-retrofit-audit`. I’m continuing the mandatory workflow/spec read before choosing the first failing test.

> AGENT

I’m also validating the isolation requirement from the execution workflow. This checkout is already a dedicated Codex worktree, and I’ve switched it to a scoped branch, so I’m not creating a nested worktree inside it.

> AGENT

The workflow confirms that the first likely fix should be semantic-boundary related: both adapters carry duplicated form validation helpers that classify native validity into `ars_forms::validation::Error`. I’m checking the forms crate before editing because that looks like the right shared home.

> AGENT

I’ve finished the main workflow read. Next I’m reading the exact specs and current code/test surfaces for `field`, `fieldset`, and `form`, then I’ll create the GitHub audit issue and start the first TDD cycle.

> AGENT

The workflow read found no blocker to starting, and the existing sketch already names a later scope correction around Tailwind examples. I’m creating the new audit issue now so the work has the issue-backed record requested in the plan.

> AGENT

The audit issue is created as #730. I’m aligning the project board next, then I’ll move into code-level drift tests.

> AGENT

Issue #730 exists under the roadmap project owner. I’m adding it to the roadmap and setting its status to In Progress before touching code.

> AGENT

The roadmap field IDs are resolved. I’m setting #730 to In Progress and marking it as adapter/Both/mixed on the board.

> AGENT

The issue is on the roadmap and In Progress. I’m reading the exact component specs plus current adapter files and tests now; this should identify the first failing test target.

> AGENT

One board detail is done; I’m keeping the rest local until the code is verified. The current audit candidate remains shared native validation logic, but I’m checking spec wording and existing tests before writing that red test.

> AGENT

The forms validation module is directory-backed, not a flat `validation.rs`. I’m reading its public API and the component specs now; the first red test will likely target a shared validity classifier rather than adapter rendering.

> AGENT

The shared form domain already owns localized `Error` construction and form messages, but it does not yet expose a framework-neutral way to map browser validity flags into those errors. I’m checking whether existing specs imply that helper before adding it.

> AGENT

The spec confirms the rule: adapters should resolve native/browser validation, but shared validation semantics belong in `ars-forms`. I’m going to add a small public `NativeValidity` helper in `ars-forms::validation`, with adapters reduced to DOM extraction plus event wiring. First I’m writing the failing shared tests.

> AGENT

I’m adding the red tests in `ars-forms` first. They describe the shared behavior both adapters currently duplicate: validity precedence, typed mismatch mapping, fallback, and merging native errors into controlled error maps.

> AGENT

There are no integration tests for `ars-forms` yet, so I’m putting focused unit tests beside the validation module rather than adding a new test target.

> AGENT

I intentionally referenced the new module/API before creating it so the next command should fail at compile time for the missing shared helper. Then I’ll add the tests and implementation.

> AGENT

The red check failed for the expected reason: `ars_forms::validation::native` does not exist. I’m adding the shared helper now, keeping it free of web/framework types so adapters only extract DOM facts.

> AGENT

The shared helper is in place. I’m running the focused `ars-forms` tests now before touching the adapter code.

> AGENT

That test command was malformed because Cargo only accepts one test filter before `--`. I’m rerunning the module’s tests with the broader `native` filter.

> AGENT

The shared tests are green. I’m replacing duplicated adapter classification code with DOM extraction into `NativeValidity`, leaving only framework/browser glue in each adapter.

> AGENT

I’m applying the adapter refactor now. The duplicated error-decision functions go away; the remaining helpers are explicitly browser DOM extraction.

> AGENT

The first patch missed because of context ordering. I’m applying the same refactor in smaller patches to keep the edit exact.

> AGENT

The Leptos form import and merge path are now shared. I’m replacing the remaining native error classifier block with DOM extraction helpers.

> AGENT

The Dioxus form has the same duplicated classifier. I’m applying the matching shared-helper refactor there, preserving the Dioxus event/ref extraction paths.

> AGENT

Both adapters now call into `ars_forms` for validation semantics. I’m running the native forms tests plus the two SSR form test targets to catch compile or behavior regressions before continuing.

> AGENT

The shared tests passed. The adapter form tests are still compiling; I’m polling those sessions and then I’ll continue with any compile fixes they surface.

> AGENT

Dioxus SSR form tests pass, but native-only compilation warns because the new DOM extraction types are only used on wasm/web. I’ll gate those imports before the warning sweep. The Leptos test target is still compiling.

> AGENT

While Leptos compiles, I’m fixing the native-target warning source by moving `NativeInputType` and `NativeValidity` behind each adapter’s wasm cfg.

> AGENT

The Leptos command completed, but that target is cfg-gated to SSR so it ran zero tests without SSR features. I’ll use the project’s focused commands later with the right feature setup; for now I’m continuing the audit for actual gaps.

> AGENT

The next concrete drift is part styling: Field and Fieldset are multi-part components, but most Leptos parts do not expose `class`/`style`, and Dioxus parts do not extend `GlobalAttributes`. That is now required by the adapter workflow. I’m writing SSR tests for those part attributes before changing component props.

> AGENT

Continuing from the compaction point. The shared native-validity helper is in place and locally green; I’m moving to the next drift area: part-level consumer attributes and styling parity across Field and Fieldset.

> AGENT

The current tests only prove root/input classes and basic anatomy. Checkbox-era tests cover every compound part with class/style, so I’m adding equivalent failing coverage for Field and Fieldset before changing the adapters.

> AGENT

I found the shared Leptos `apply_part_attrs` helper added by the checkbox work, and Dioxus already has the global-attribute merge path. The retrofit is straightforward: tests first, then wire the Field/Fieldset subparts through those existing adapter conventions.

> AGENT

I’ve added the red tests for part attributes. Next I’m running focused SSR tests to capture the expected failures before changing component props.

> AGENT

The red checks failed exactly at the missing public props for the subparts. I’m wiring the parts now, preserving component-owned ARIA/IDs and only merging consumer class/style/global attrs at the adapter boundary.

> AGENT

One additional drift fell out while inspecting Form: Leptos `Form` still only accepted `class` on the root while Dioxus forwards full globals. I’m keeping that as part of the same semantic-boundary fix by adding a Leptos `style` root prop and using the existing style conversion helper.

> AGENT

The component changes are in. I’m rerunning the focused SSR/unit tests now; this will also catch any prop or macro shape issues from the Leptos and Dioxus component builders.

> AGENT

The part-attribute retrofit is green in focused SSR/unit tests. I’m expanding back to Form/root parity and the remaining reactive/browser evidence areas so the audit does not stop at the first visible drift.

> AGENT

The adapter specs confirm the root merge contract explicitly calls out additive `class` and `style`. Dioxus already satisfies that through global attrs; Leptos Form needs the same public root style hook.

> AGENT

The Form root style test is added. I’m checking the red/green split next: Dioxus should already pass, and Leptos should fail until the root style prop is wired.

> AGENT

Dioxus is already green for Form root globals; Leptos produced the expected missing-style failure. I’m adding the Leptos root style prop using the existing shared style converter.

> AGENT

Leptos Form now has the style hook. I’m rerunning the focused Form test and then I’ll run the full Field/Fieldset/Form SSR suite for both adapters.

> AGENT

The shared native-validity tests and Leptos Form root style test are green. I’m running the full focused SSR/unit set for all three components in both adapters now.

> AGENT

The full focused SSR/unit suites are passing for both adapters. I’m moving to the browser-test side of the audit: locating the wasm tests and checking whether the changed attr merge/native-validation paths are covered there.

> AGENT

The plan’s wasm filenames differ from the repo’s actual `test_*_wasm.rs` convention. I found the real files and am reading those now instead of relying on the stale names.

> AGENT

The wasm coverage already exercises the high-risk reactive paths: form validation maps, field error relationships, fieldset inheritance, input value callbacks, reset, and native validation. The new styling changes are static SSR evidence, so I’m not adding browser-only tests for those, but I will run the existing browser suites.

> AGENT

The audit found an actual parity gap in browser evidence: Leptos Fieldset has tests for error inheritance and reactive inherited state updates, while Dioxus only covered initial inherited state. I’m adding the missing Dioxus browser tests before touching any code.

> AGENT

The missing Dioxus Fieldset browser tests are in. I’m running that wasm target now; if it fails, the failure will tell us whether it was only an evidence gap or also an implementation gap.

> AGENT

The Dioxus Fieldset wasm test is still compiling from a cold wasm target. I’m waiting for the run to finish before deciding whether implementation changes are needed.

> AGENT

The wasm binary compiled, but the runner could not spawn its browser server inside the sandbox. Per the repo workflow this browser evidence matters, so I’m rerunning the same command with escalation. It also surfaced a Dioxus `reset_generation` dead-code warning on this target that I’ll fix at the root.

> AGENT

The added Dioxus Fieldset browser tests all pass, so that was an evidence gap rather than a runtime bug. I’m removing the unused Dioxus form-context field that the wasm compile exposed, since the reset signal is only needed inside `Form` itself.

> AGENT

The wasm warning fix is in. I’m running the hook-order probe and then the focused browser suites for all Field/Fieldset/Form wasm tests.

> AGENT

The hook probe returned no matches, which is the expected clean result. Both adapter wasm test batches are running now; Leptos is still compiling, and Dioxus is waiting on the shared build lock.

> AGENT

The Dioxus browser suite is green: 19 wasm tests across Field, Fieldset, and Form. Leptos is still building/running; I’m waiting on that result next.

> AGENT

Both browser batches are green now. I’m updating the adapter specs and retrofit sketch to reflect the new shared forms helper, part/global-attribute support, and the browser evidence matrix from this audit.

> AGENT

The spec files still described the pre-checkbox-style subpart APIs, so I’m correcting that drift now. I’m keeping the edits focused: API/merge notes plus a dated retrofit addendum with the exact test evidence from this audit.

> AGENT

One older foundation section still shows `validation_errors` as `Vec<String>` while the adapters and validation crate use structured `Error`. I’m treating that as spec drift from the audit and tightening it to the current structured error contract.

> AGENT

I’m applying the spec/documentation updates now: structured form errors in the foundation spec, public attr/style props in adapter specs, and the dated retrofit addendum in the counterpart sketch.

> AGENT

One documentation patch did not apply because the surrounding spec text has diverged slightly. I’m splitting the edits into smaller patches against the exact current text.

> AGENT

The foundation spec and Leptos Field API snippet are updated. I’m continuing through the Dioxus and Fieldset/Form adapter specs in small targeted edits.

> AGENT

The Field/Fieldset specs now match the new public styling/global-attribute surface. I’m doing the same for Form, then I’ll append the audit addendum.

> AGENT

Form specs are updated. I’m adding a 2026-06-16 retrofit audit addendum to the existing sketch with the fresh local evidence and final matrix deltas from this pass.

> AGENT

The sketch now has a dated retrofit addendum with the audit issue, findings, and evidence. I’m checking E2E utility coverage next so the widget/E2E evidence side of the plan is not just inferred from adapter tests.

> AGENT

Adapter parity is clean. The E2E command help process is still open because it paged/printed slowly, so I’m polling it, then I’ll run the focused utility harnesses if the CLI shape is clear.

> AGENT

The E2E entrypoint is `cargo xtask e2e utility`. I’m checking its options so I can run the focused utility harnesses against both adapters without guessing flags.

> AGENT

The focused E2E harness supports `--adapter leptos|dioxus`. I’m running both utility harnesses now; these spawn local fixture servers and browser automation, so I’m using the approved path for local browser E2E.

> AGENT

Both E2E runs have compiled and launched their adapter harnesses. I’m waiting for browser assertions to finish.

> AGENT

The Dioxus E2E run timed out inside Chrome while both harnesses were running concurrently. I’m checking the Leptos run, then I’ll rerun Dioxus sequentially to avoid browser contention before treating it as a real failure.

> AGENT

Leptos also timed out during category-tab discovery, consistent with the concurrent browser/server runs interfering rather than a Field/Form assertion. I’m rerunning the E2E harnesses one at a time.

> AGENT

The sequential Leptos E2E rerun still times out before the Utility tab is visible, so this is not a Field/Form assertion failure yet. I’m inspecting the E2E harness startup and fixture logs to determine whether the app failed to serve, the selector changed, or Chrome is stuck.

> AGENT

The E2E failure is happening before any Field/Form check, at the common “open Utility panel” step. I’m checking fixture startup details and temp logs rather than changing component code for that.

> AGENT

The E2E harness has a 15-second common tab-discovery timeout, and the failures occur there before any utility assertion. I’m not patching harness timing as part of this adapter audit; I’ll report this as an E2E startup blocker after running the remaining local gates.

> AGENT

The attempted warning cleanup was too aggressive: checkbox form-reset support reads `FormContext.reset_generation` in the input adapter. I’m restoring that field and marking the wasm-only unused warning deliberately rather than removing the contract.

> AGENT

The Dioxus form context is restored with a scoped `#[expect(dead_code)]` reason. I’m rerunning the Dioxus SSR/unit suite that caught it.

> AGENT

Native builds use `reset_generation`, so the unconditional expectation causes an unfulfilled-lint warning there. I’m narrowing the expectation to wasm builds where the utility-only target can compile without the checkbox consumer.

> AGENT

The reset-generation lint expectation is now wasm-only. I’m rerunning the Dioxus focused suite to confirm it is warning-free before continuing.

> AGENT

The Dioxus focused suite is clean again. I’m finishing the required post-implementation-audit skill instructions before running that audit pass.

> AGENT

I’ve completed the audit review passes in substance: spec drift, layer drift, test breadth, parity matrix, and E2E startup. I’m running formatter and clippy next; coverage via the adapter wasm recipe may be heavier, so I’ll decide after the warning gates are clean.

> AGENT

`cargo xfmt` passed. It formats broad Dioxus surfaces by design, so I’ll inspect the diff after verification to make sure there isn’t unrelated churn. Now I’m running the workspace clippy wrapper.

> AGENT

`cargo xclippy` is still running through the workspace. I’m waiting for the final result before making any more changes.

> AGENT

Clippy has reached the local crates and is still running. No changed-code warnings have appeared yet.

> AGENT

Clippy found only the new Dioxus `part_attrs` closures. I’ll let the wrapper finish, then replace those with method items instead of suppressing them.

> AGENT

The wrapper is in its final i18n lane. The actionable warnings are already identified and scoped to the new Dioxus part-attribute code.

> AGENT

`cargo xclippy` completed, with the seven Dioxus redundant-closure warnings from the new attr merge calls. I’m fixing those now at the call sites.

> AGENT

The Dioxus warnings are fixed by using the machine API method items directly. I’m formatting again, then rerunning focused tests and clippy to verify the warning sweep is clean.

> AGENT

Formatting is clean after the clippy fixes. I’m rerunning the focused tests plus `cargo xclippy` now to confirm the warnings are gone.

> AGENT

The method-item version does not satisfy the generic lifetime bound in normal builds. I’m reverting to closures and adding scoped `#[expect(clippy::redundant_closure_for_method_calls)]` annotations, matching the existing checkbox pattern for these API callbacks.

> AGENT

The lifetime-safe closure form is restored with explicit expectations. I’m formatting and rerunning Dioxus focused tests plus clippy.

> AGENT

Format and Dioxus focused tests are green again. I’m running `cargo xclippy` one more time to confirm the scoped expectations satisfy the wrapper.

> AGENT

`cargo xclippy` is clean for changed code; only the existing third-party future-incompat note remains. I’m rerunning the browser wasm suites after the clippy/format changes to keep the final evidence current.

> AGENT

Final wasm and spec validation are green. I’m running a focused native coverage read for the shared `ars-forms::validation::native` helper added in this audit; adapter wasm coverage is covered by the browser test matrix here, while full merged coverage is the longer CI-style gate.

> AGENT

The focused coverage run passed, but the annotated output is too broad for a useful summary because `cargo llvm-cov --text` prints the whole crate. I’m rerunning it as a concise summary so the final audit evidence is readable.

> AGENT

The native helper coverage is 99.28% line / 100% function coverage; I’m checking the one missed line so the audit can classify it rather than just quote a number.

> AGENT

The one uncovered native helper line is the `NativeInputType::Other` mismatch branch. That is a real branch, so I’m adding a small test rather than leaving it as a coverage gap.

> AGENT

The test block had shifted from formatting, so I found the exact insertion point and am adding the uncovered `Other` mismatch case there.

> AGENT

The coverage gap test is in. I’m formatting and rerunning the native helper tests plus the concise coverage summary.

> AGENT

The shared native helper is now at 100% line/function coverage for the touched file. I’m running one final `cargo xclippy` after the added test.

> AGENT

All requested local gates that are not blocked by the E2E tab-discovery issue are green. I’m checking the final diff now, including whether `cargo xfmt` introduced unrelated churn.

> AGENT

The diff is scoped to the adapters, forms helper, tests, and audit/spec docs. I’m doing one last hook probe after formatting and then I’ll summarize.

> AGENT

Implemented the Field/Fieldset/Form adapter retrofit audit on `codex/field-form-adapter-retrofit-audit`. Created and moved audit issue to In Progress: `#730` (`audit: Retrofit Field, Fieldset, and Form adapters to current delivery workflow`). What changed: - Moved duplicated native validity/error-map logic out of both adapter `form.rs` files into `ars_forms::validation::{NativeValidity, NativeInputType, merge_error_map}`. - Added Leptos `class`/`style` support for Field and Fieldset compound parts, plus `Form.style`. - Added Dioxus `GlobalAttributes` support for Field and Fieldset compound parts. - Added SSR/unit tests for part styling parity in both adapters. - Added Dioxus wasm Fieldset parity tests for error inheritance and reactive inherited state updates. - Updated adapter specs, forms foundation spec, and the Field/Form counterpart sketch with a 2026-06-16 retrofit audit addendum. Verification: - `cargo test -p ars-forms --lib native`: pass, 6 tests - `cargo llvm-cov test -p ars-forms --lib --summary-only -- native`: `validation/native.rs` is 100% line/function coverage - `cargo test -p ars-leptos --features ssr --test field --test fieldset --test form`: pass - `cargo test -p ars-dioxus --test field --test fieldset --test form`: pass - Leptos wasm Field/Fieldset/Form tests: pass, 17 tests - Dioxus wasm Field/Fieldset/Form tests: pass, 19 tests - `cargo xtask lint adapter-parity`: pass - Dioxus hook probe: no matches - `cargo xtask spec validate`: pass […]

> DEVELOPER

Should we have styled components for those 3 components or just the low level unstyled that we will compose later with more higher level components? Actual question, don't change any code yet

> AGENT

I’ll use the brainstorming skill here because this is an API/design decision, not an implementation request.

> AGENT

I’m going to answer this as a design call only. I’m using the brainstorming skill because this is a product/API shape decision, not an implementation step.

> AGENT

I’d keep `Field`, `Fieldset`, and `Form` as low-level unstyled primitives. More precisely: they should be **stylable primitives**, not **styled components**. Their job is semantic ownership: ids, ARIA relationships, invalid/valid state propagation, fieldset inheritance, form validation maps, reset behavior, native validity mapping, and status/error wiring. They should not own visual policy like spacing, borders, colors, required-marker presentation, helper-text typography, or layout. That gives us the right layering: - `Form`: semantic submit/reset/validation boundary. - `Fieldset`: grouped field state and relationship boundary. - `Field`: label/description/error/input relationship boundary. - Future higher-level components: `TextField`, `SelectField`, `CheckboxField`, `FormSection`, design-system wrappers, etc. Those can compose the primitives and own richer styling/UX. So the right contract is: expose `class`, `style`, global attrs, stable `data-ars-*` state/part attributes, and examples that show consumer styling. But don’t add first-class styled `Field`/`Fieldset`/`Form` exports in the adapters yet. The one exception is accessibility-required behavior, like hidden status-region mechanics or relationship attributes. That belongs in the primitive. Visual design belongs later, at the higher-level component or app/design-system layer.

> DEVELOPER

Are we following this intended contract now after the audit?

> AGENT

I’ll check the touched adapter surfaces against that “stylable primitive, not styled component” boundary so I can answer from the actual diff, not memory.

> AGENT

Yes, in the current audit diff we are following that contract. What changed is **stylability**, not **styled components**: - Leptos `Field`, `Fieldset`, and `Form` now expose additive `class` / `style` where needed. - Dioxus parts now extend `GlobalAttributes`. - Core semantic attrs still win: ids, ARIA relationships, validity state, descriptions, errors, disabled/read-only propagation, etc. - No new visual API was introduced: no `variant`, `size`, `tone`, theme props, bundled classes, or styled wrapper exports. - Shared validation/error logic moved down into `ars-forms`, while adapters keep renderer/DOM extraction glue. So the boundary is now basically: ```text ars-leptos / ars-dioxus utility components: own semantics + relationships + state propagation allow consumer styling hooks future higher-level components / design-system wrappers: own visual layout + styling + richer field UX ``` The only caveat: the E2E utility harness still timed out before reaching Field/Form assertions, so the browser-level evidence is incomplete. But from the code/spec surface, the primitive-vs-styled contract is aligned.

> DEVELOPER

Are we exposing the lower level parts for all of them as needed, so they can be styled independently?

> AGENT

I’ll verify the public component parts rather than infer from the earlier audit notes. The main distinction is that `Field` and `Fieldset` have visible compound parts, while `Form` mostly has a root semantic boundary.

> AGENT

The visible part inventory is mostly aligned. I’m checking whether `Form` has a status/live-region part in the contract, because that is the only likely gap in “independently styled lower-level parts.”

> AGENT

One nuance surfaced: the spec currently treats `Form::StatusRegion` as a structural adapter-owned node, not a public child component. That means it is addressable by data attributes, but not independently configurable through a `StatusRegion` component API.

> AGENT

Mostly yes, with one deliberate caveat. Current public/stylable surface: | Component | Exposed lower-level parts | Independently stylable now? | |---|---|---| | `Field` | `Field`, `Label`, `Input`, `Description`, `ErrorMessage` | Yes | | `Fieldset` | `Fieldset`, `Legend`, `Description`, `Content`, `ErrorMessage` | Yes | | `Form` | `Form` root, internal `StatusRegion` | Root yes; `StatusRegion` is not a public component | For `Field` and `Fieldset`, yes: the visible subparts are exposed and can be styled independently. Leptos has `class` / `style` on the parts; Dioxus exposes `GlobalAttributes` on the parts. For `Form`, the only public component is the root form. The status live region is rendered, has core `data-ars-scope` / `data-ars-part="status-region"` attrs, and can be targeted by CSS selectors, but there is no public `<StatusRegion>` compound part or direct `class` / `style` prop for it. That matches the current adapter spec, which says the status region is adapter-owned structural UI. So if the intended contract is “all visible composition parts are independently stylable,” we’re aligned. If the intended contract is stricter, meaning “every core part, including `Form::StatusRegion`, must have a public stylable adapter component or direct styling prop,” then `Form` still has a gap. My take: keep `StatusRegion` internal unless we […]

> DEVELOPER

Yeah, let's have it stylable too, that was the intention of one of our improvements in the implementation docs / skills

> AGENT

Understood. I’ll treat `Form::StatusRegion` as a public stylable part now and keep it within the primitive contract: expose styling hooks without letting consumers replace the live-region semantics.

> AGENT

I found the repo-specific rule in the framework skills: multi-part adapter components should expose public compound parts for stylable parts rather than root-level prop families. I’m going to add failing tests for a public `StatusRegion` part in both adapters, then implement the minimal surface.

> AGENT

There is one design wrinkle before editing: `Form` currently auto-renders the status region so consumers cannot accidentally omit the accessibility node. To make it a public compound part without losing that guarantee, I’m going to keep the auto-rendered fallback and let an explicit `<StatusRegion>` opt into styling/placement while suppressing the fallback.

> AGENT

I’m adding tests that express the desired contract directly: consumers can render a `StatusRegion` compound part with its own styling, and the form still produces exactly one live region.

> AGENT

The tests now encode the intended public part. I’ll run the focused SSR form tests to confirm they fail for the expected missing `StatusRegion` API before touching implementation.

> AGENT

The red tests fail exactly because the public `StatusRegion` part does not exist yet. I’m implementing that part now, with a fallback counter in form context so existing `<Form>` usage still gets a status region when no explicit part is rendered.

> AGENT

I’m editing the form adapters only: adding a public `StatusRegion` compound part, preserving the internal fallback, and merging consumer attrs through the same part-attr helpers used by the other utility parts.

> AGENT

Leptos now has the public part and fallback suppression. I’m applying the matching Dioxus surface with `GlobalAttributes`, keeping Dioxus event stripping on the form root unchanged.

> AGENT

The implementation is in place. I’m running the two red tests first; if Dioxus renders both fallback and explicit status region, I’ll adjust the suppression approach based on the actual output.

> AGENT

Leptos passed. Dioxus showed the expected first-pass SSR ordering problem: the explicit child renders, then the parent fallback still renders because the child cannot update the parent’s fallback decision early enough in the same render. I’m checking whether we can inspect the Dioxus child tree instead of relying on a context side effect.

> AGENT

Dioxus cannot use the child side effect to suppress the fallback in first-pass SSR. I’m going to make the parent inspect its child VNode tree for the `StatusRegion` component before rendering the fallback, which keeps the public compound API and preserves automatic fallback behavior.

> AGENT

The child tree exposes component names publicly enough for this. I’m removing the side-effect registration path in Dioxus and replacing it with a small VNode scan for an explicit `StatusRegion` child.

> AGENT

The Dioxus fallback suppression now happens before render output is built. I’ll rerun the focused tests and then the full form SSR tests for both adapters.

> AGENT

Dioxus only re-exports `VNode` through the prelude, not `DynamicNode`, so I’m using the public `dioxus_core` re-export for that type.

> AGENT

I’ll rerun the Dioxus form tests now that the type import is explicit.

> AGENT

The adapter tests are green with the new part. I’m updating the adapter specs next so the contract says `StatusRegion` is public and stylable, with the fallback retained when omitted.

> AGENT

The specs still described `StatusRegion` as intentionally private, so I’m correcting that drift now. The updated contract will say explicit `StatusRegion` is allowed for styling/placement and the adapter fallback is used only when omitted.

> AGENT

Leptos spec is aligned. I’m making the same API and ownership wording change in the Dioxus adapter spec.

> AGENT

I’m also updating the retrofit sketch so the audit record reflects that `Form::StatusRegion` was part of the part-styling drift, not an intentional exception.

> AGENT

The docs are updated. I’m formatting now, then I’ll run focused form SSR/wasm checks and the spec validation/parity checks that cover this surface.

> AGENT

Formatting completed. I’m checking the actual changed file set so formatter noise did not add unrelated edits.

> AGENT

The formatted diff is still scoped to the audit files. I’m running focused tests now, including wasm form tests because `StatusRegion` is render/runtime surface, not just SSR markup.

> AGENT

SSR/unit coverage is green for all three components in both adapters. I’m running the browser wasm form suites now to catch any component/context issues outside SSR.

> AGENT

The wasm binaries compiled, but the runner could not spawn its local browser test server inside the sandbox. I’m rerunning those exact wasm form tests with the required sandbox escalation.

> AGENT

Both wasm form suites pass with browser execution. I’m running the contract/lint checks that are cheap and directly relevant: spec validation, adapter parity, and the Dioxus hook-order probe.

> AGENT

Spec validation and adapter parity pass; the hook probe returned no matches, which is the expected clean result. I’m running `cargo xclippy` because this change adds public API and a Dioxus tree scan.

> AGENT

`cargo xclippy` found one formatting lint in the new Leptos cleanup closure. I’m fixing that warning at the source, then rerunning format and clippy.

> AGENT

The warning fix is in. I’m rerunning formatter and clippy to confirm the changed surface is clean.

> AGENT

Clippy is clean after the warning fix. I’m doing one final text scan for stale “StatusRegion is private” wording before I summarize the outcome.

> AGENT

No stale private-status-region wording remains. I’m doing a whitespace diff check and then I’ll close this loop with the exact result.

> AGENT

Implemented. `Form::StatusRegion` is now a public stylable compound part in both adapters. What changed: - Leptos: `form::StatusRegion` with `class` / `style`. - Dioxus: `form::StatusRegion` with `GlobalAttributes`. - `<Form>` still auto-renders an unstyled fallback status region when no explicit `StatusRegion` is provided. - If consumers render `<StatusRegion ... />`, the fallback is suppressed so there is still exactly one live region. - Specs and the retrofit sketch now document this as the intended contract. Verification passed: - `cargo test -p ars-leptos --features ssr --test field --test fieldset --test form` - `cargo test -p ars-dioxus --test field --test fieldset --test form` - Leptos `test_form_wasm`: 9 passed - Dioxus `test_form_wasm`: 10 passed - `cargo xtask spec validate` - `cargo xtask lint adapter-parity` - Dioxus hook probe: no matches - `cargo xfmt` - `cargo xclippy` - `git diff --check` No commit or push performed.

> DEVELOPER

Based in our conversation until now, do we see any opportunity to improve our implementation docs / skills for adapter level components?

> AGENT

I’ll answer from the actual drift we just found, but I’m going to do a quick scan of the adapter workflow docs so the recommendations map to the right places.

> AGENT

Yes. The docs already point in the right direction, but this audit exposed a few places where they should be sharper. Most useful improvements: 1. **Define “stylable part” more explicitly** Add language that every core-rendered structural part should be evaluated for public styling, including hidden/live-region/status parts. The current docs say “visible anatomy” often enough that `Form::StatusRegion` looked plausibly exempt, even though the intended contract was broader. 2. **Add a “structural fallback part” pattern** Document the pattern we just used: - expose a public compound part for styling/placement; - auto-render an unstyled fallback when omitted; - suppress fallback when explicit part exists; - keep semantic text/state owned by the machine, not consumer children. This is relevant for status regions, hidden inputs, portals, live regions, anchors, overlays, and other required structural nodes. 3. **Clarify primitive vs styled boundary** The skills say adapter crates expose unstyled primitives, but we should add the phrase “unstyled does not mean unstylable.” Adapter primitives should expose styling hooks for their parts; styled templates/wrappers own visual policy. 4. **Strengthen checklist wording** Add a checklist row like: `For every core Part enum variant and adapter-rendered structural node, either expose a public stylable part or record why it is intentionally […]

> DEVELOPER

Let's apply those improvements then

> AGENT

I’ll update the workflow docs and framework skills in the narrow places this audit exposed: structural parts, fallback parts, primitive-vs-stylable wording, test expectations, and the Dioxus SSR caveat.

> AGENT

I found the right insertion points. I’m making the docs stronger without changing the implementation contract: unstyled primitives remain the adapter output, but every machine/core structural part needs a public styling decision.

> AGENT

I’m also adding the audit-skill check, because this is exactly the kind of issue the post-implementation audit should force into the same PR.

> AGENT

The API doc now has the explicit structural-part rule and fallback pattern. Next I’m adding the Dioxus-specific SSR caveat where hook/global attribute rules already live.

> AGENT

Now I’m tightening the test documentation so the part-styling contract gets tested directly for each exposed part.

> AGENT

I’m updating the framework skills too, so agents applying Leptos or Dioxus guidance get the same rule without having to infer it from the long workflow docs.

> AGENT

Leptos skill updated. I’m applying the matching Dioxus skill update, including the SSR child-registration caveat.

> AGENT

I’m adding the same requirement to the post-implementation audit loop so future audits explicitly check public part exposure and fallback behavior.

> AGENT

The docs/skills changes are in. I’m formatting/checking the markdown edits and scanning for the new contract wording to make sure it landed consistently.

> AGENT

Applied the docs/skills improvements. Updated: - `docs/implementation/adapter-components/02-adapter-api-and-wiring.md` - `docs/implementation/adapter-components/03-framework-rules.md` - `docs/implementation/adapter-components/04-adapter-tests.md` - `.agents/skills/leptos/SKILL.md` - `.agents/skills/dioxus/SKILL.md` - `.agents/skills/post-implementation-audit/SKILL.md` What changed: - Added “unstyled does not mean unstylable.” - Required explicit public/private styling decisions for every core `Part` and adapter-rendered structural node. - Added the required structural part + fallback pattern. - Added test expectations for root and per-part styling, including fallback suppression. - Added the Dioxus SSR caveat: don’t rely on child side effects to suppress parent fallback nodes on the same render. - Added post-implementation-audit checks so future audits treat missing stylable parts or undocumented private structural nodes as adapter API gaps. Verification: - `rg` confirmed the new contract wording landed in the intended docs/skills. - `git diff --check` passed. No commit or push performed.

> DEVELOPER

Should we follow the checkbox standard for low level components to use `Root` as the name for root part? Like `fieldset::Root` for example, it helps to denote that those components are low level parts and usually shouldn't be used without a component orchestrating them

> AGENT

I’ll answer as an API design call and quickly verify how Checkbox is shaped so the recommendation is grounded in the current standard.

> AGENT

Yes, I think we should follow the Checkbox standard and use `Root` for these low-level root parts. Recommended shape: ```rust field::Root field::Label field::Input field::Description field::ErrorMessage fieldset::Root fieldset::Legend fieldset::Description fieldset::Content fieldset::ErrorMessage form::Root form::StatusRegion ``` Then, later, higher-level or styled wrappers can take the nice semantic names: ```rust TextField FormField FormSection Form ``` Why I’d do it: - It makes the primitive anatomy consistent with Checkbox. - It signals “this is a part API,” not a finished app-level component. - It avoids ambiguity between `form::Form` as a low-level root and future higher-level `Form` wrappers/templates. - It keeps the mental model clean: module name is the component family, `Root` is the root part. - It makes every low-level part independently stylable without pretending each one is a standalone design-system component. The only downside is migration churn for the current `Field`, `Fieldset`, and `Form` adapter names. But since we are doing a retrofit audit now, this is the right time to align the API rather than letting these three remain as pre-Checkbox exceptions.

> DEVELOPER

Let's do it then, and don't forget to improve our docs/skills too

> AGENT

I’ll rename the low-level root components to the Checkbox-style `Root` API, keep the module names as the component family, and update tests/specs/docs/skills so this becomes the documented adapter standard rather than a one-off cleanup.

> AGENT

I’m going to make this as a breaking alignment rather than keeping old `Field`/`Fieldset`/`Form` aliases, because aliases would dilute the “this is a root part” signal we’re trying to standardize. I’ll update all in-repo call sites in the same pass.

> AGENT

I’m first changing the adapter modules themselves: root functions and Dioxus root prop structs become `Root`, matching Checkbox. After that I’ll update imports/call sites to use `field::Root`, `fieldset::Root`, and `form::Root`.

> AGENT

The repo already uses path-qualified root parts for Checkbox, so I’ll follow that shape in tests/examples instead of importing `Root` under the old names.

> AGENT

The root APIs are renamed in the adapter modules. I’m doing the mechanical call-site rewrite now, using path-qualified `field::Root`, `fieldset::Root`, and `form::Root` to match Checkbox style.

> AGENT

The call sites are rewritten. I’m scanning the remaining old root names and import errors before running tests, because this rename affects examples, fixtures, and adapter tests.

> AGENT

The call-site rewrite left imports pointing at the removed old root function names. I’m converting those to module imports now so the source reads like Checkbox: `field::Root`, `fieldset::Root`, `form::Root`.

> AGENT

I’m also fixing the e2e fixture imports, which had direct imports of the old root names.

> AGENT

A naming collision showed up in the form SSR tests: `form` now refers to both the core spec module and the adapter module. I’m aliasing the core module to keep adapter `form::Root` clear.

> AGENT

The obvious import collision is fixed. I’m running a focused compile/test now to surface the remaining mechanical misses.

> AGENT

The first compile failure is the adapter preludes still re-exporting the old root names. I’m updating those to export the utility modules only, consistent with path-qualified part usage.

> AGENT

I’m editing both preludes so end users get the modules and can write `field::Root`, `fieldset::Root`, and `form::Root`, instead of importing the old root aliases.

> AGENT

Leptos prelude is fixed. I’m applying the same module-only export in Dioxus.

> AGENT

Preludes are aligned. I’m rerunning the focused compile to find the remaining stale imports/calls.

> AGENT

The focused adapter tests compile with the new root names. I’m updating the specs and workflow docs next so the contract says low-level roots are named `Root`.

> AGENT

The specs still describe the old root names. I’m updating the public API snippets and prose to identify the low-level root part as `Root`.

> AGENT

I’m adding the explicit standard to the workflow docs and framework skills: low-level primitive roots are named `Root`; higher-level/styled wrappers get semantic names later.

> AGENT

The main API workflow now says root primitives are `Root`. I’m mirroring that in the Leptos and Dioxus skills.

> AGENT

Leptos skill updated. I’m applying the same naming rule to the Dioxus skill.

> AGENT

I’m adding the naming check to the post-implementation audit as well, so future adapter audits catch old semantic root names.

> AGENT

The naming standard is documented. I’m scanning for remaining old public root names in code/specs before formatting.

> AGENT

The remaining spec hits are mostly conceptual references to the core components, which are fine, but I’m cleaning the adapter-root prose where it still says the low-level root is `Field`, `Fieldset`, or `Form`.

> AGENT

Specs are cleaned up. I’m running focused adapter tests now, then I’ll broaden to wasm and lint/format.

> AGENT

SSR/unit tests pass with the new root names. I’m running the focused wasm suites next because those files had many call-site rewrites.

> AGENT

The wasm suites compiled; the runner needs the usual browser-server escalation. The Leptos wasm compile also surfaced two path warnings from the import change, so I’m fixing those before rerunning.

> AGENT

The warnings are fixed. I’m rerunning the browser-backed wasm suites with escalation so the test runner can start its local server.

> AGENT

All focused wasm tests pass with the new root API. I’m running formatter next, then lint/spec checks to catch example and fixture compile issues.

> AGENT

Formatting is done. I’m running spec validation, adapter parity, hook probe, and clippy now; clippy should also catch remaining public API/import issues in examples and fixtures.

> AGENT

Clippy and spec validation pass. Adapter parity now fails because its composition-test detector still looks for old `Form`/`Fieldset` root names in Checkbox tests. I’m updating that lint to recognize `form::Root` and `fieldset::Root`.

> AGENT

I found the lint helper. It was using a loose text heuristic for `Fieldset` and `Form`; I’m making it accept the new root-part syntax too.

> AGENT

I’m patching the composition-test heuristic to accept both legacy names and the new `form::Root` / `fieldset::Root` pattern.

> AGENT

The lint now recognizes both patterns. I’m rerunning adapter parity and the relevant xtask/lint tests if present.

> AGENT

Adapter parity is fixed and xtask lint tests pass. I’m running formatter and clippy again after the xtask/doc changes.

> AGENT

Formatter and clippy are clean. I’m doing final scans for stale old root API references and a whitespace diff check.

> AGENT

The stale API scan is clean; the only hit is `FormContext`, which is still the internal context type, not the root component. I’m adding a small xtask regression test for the new composition-test heuristic so the lint keeps recognizing `form::Root` / `fieldset::Root`.

> AGENT

I found the adapter-presence test area. I’ll add a direct unit test for `has_composition_test` so the new `Root` syntax is locked in.

> AGENT

The lint regression test is added. I’m rerunning formatter and the xtask lint tests.

> AGENT

The formatter passed. I passed two separate test filters to `cargo test` incorrectly, so I’m rerunning the xtask lint test module with one filter.

> AGENT

The xtask lint tests pass. I’m running clippy once more after the new xtask test.

> AGENT

Clippy is clean. I’m doing final status and diff checks, including one more stale-root scan.

> AGENT

Implemented the `Root` standard for these low-level utility primitives. Changed: - `field::Field` -> `field::Root` - `fieldset::Fieldset` -> `fieldset::Root` - `form::Form` -> `form::Root` - Dioxus root prop structs now use `RootProps` - Adapter preludes now export the modules, not old root aliases - Tests, widgets, E2E fixtures, and specs now use `field::Root`, `fieldset::Root`, `form::Root` - `xtask` adapter-parity lint now recognizes the new root-part syntax - Docs/skills now explicitly say low-level primitive roots should be named `Root`, with semantic names reserved for higher-level wrappers/styled templates Verification passed: - Focused Leptos SSR tests for field/fieldset/form - Focused Dioxus SSR tests for field/fieldset/form - Focused Leptos wasm field/fieldset/form suites - Focused Dioxus wasm field/fieldset/form suites - `cargo xtask spec validate` - `cargo xtask lint adapter-parity` - Dioxus hook probe: no matches - `cargo test -p xtask lint:: -- --nocapture` - `cargo xfmt` - `cargo xclippy` - `git diff --check` No commit or push performed.

> DEVELOPER

Does Dioxus provide some of kind of way to achieve the same result for native target as we had to put those web only target functions?

> AGENT

I’ll answer this against Dioxus 0.7 and the exact adapter code path we touched: the issue is DOM constraint validation, not ordinary Dioxus event delivery.

> AGENT

I’ll answer this against Dioxus 0.7 and the exact adapter problem: browser constraint validation is DOM-owned behavior, so the native target question is mostly about whether Dioxus exposes that DOM bridge outside `web_sys`.

> AGENT

Short answer: not equivalently. Dioxus native/desktop runs through a WebView, so a DOM exists, but Dioxus does not give us a typed native Rust equivalent of `web_sys::HtmlFormElement::check_validity()` / `ValidityState` for non-wasm targets. What Dioxus gives us: - `FormData`: cross-platform form values/files, but not browser constraint-validation details like `valueMissing`, `typeMismatch`, `patternMismatch`, `tooShort`, etc. - `MountedData`: cross-platform element handles, with web-only downcast paths for actual `web_sys` APIs. - `dioxus_document::eval`: a way to run JavaScript against the WebView on desktop/native-like runtimes. So for native targets, the closest path would be an eval bridge: ```text desktop/native Dioxus -> JS eval in WebView -> form.checkValidity() ``` But that is not the same quality of abstraction as the web path. It is async, JS-serialized, platform-specific, harder to test, and would force the submit/validation path to account for an async native-validity provider. My take: the current web-only extraction is the right baseline. If we later want desktop parity, I’d introduce a small platform abstraction: - web/wasm: use typed `web_sys` - desktop WebView: optional JS eval provider returning our shared `NativeValidity` map - non-DOM native/server: no native browser validity, rely on controlled validation errors I would not add the eval bridge during this audit unless we explicitly decide […]

> DEVELOPER

Do we have anything else worth to improve in our implementation docs / skills?

> AGENT

I’ll do a quick pass over the adapter workflow docs and local skills we just touched, then I’ll separate “worth doing now” from “probably overkill.”

> AGENT

The current docs already cover the big lessons from this audit: stylable unstyled parts, `Root` naming, Dioxus SSR fallback suppression, semantic-boundary checks, and per-part styling tests. I’m checking for gaps that are still implicit rather than adding more process weight.

> AGENT

Yes. I see a few worthwhile additions, but only a small set. The docs are already heavy, so I’d avoid more checklist sprawl. Most useful improvements: 1. **Target Capability Classification** Add a rule for adapter behavior that depends on platform APIs: - web DOM available through typed APIs, like `web_sys` - desktop/native WebView available only through eval/bridge - SSR/server no DOM - pure native no browser semantics This would have caught the “Dioxus native validity” question earlier and forced the sketch/spec to say: `SameNativeBehavior on web`, `NoNativeBrowserValidity on non-DOM targets`, or `FutureEvalBridge`. 2. **Retrofit Audit Workflow** The current workflow is strongest for new adapter components. Field/Fieldset/Form showed that retrofitting old components has extra steps: - create a fresh audit issue - compare against latest “gold standard” component, currently Checkbox - scan old public names and stale examples - update docs/skills when the audit reveals a reusable rule - treat old E2E evidence as stale until remapped to the new final matrix This should probably be a short section in `adapter-component-delivery.md` or a new `14-retrofit-audits.md`. 3. **Public Primitive Rename Checklist** The `Root` rename touched specs, preludes, widgets, E2E fixtures, tests, and lint heuristics. We should document a stale-symbol scan pattern for […]

> DEVELOPER

Go ahead then

> AGENT

I’ll make the doc/skill changes now, scoped to the gaps we identified: platform capability classification, retrofit audits, rename scans, and E2E blocker status. I’ll keep it as workflow guidance rather than adding a lot of new checklist weight.

> AGENT

I’m using the writing-skills guidance because this touches repo-local agent skills. I’m going to patch existing files only: no new skill, no new dependency, no code changes.

> AGENT

I found the clean place for each rule: platform behavior belongs in framework rules, retrofit-specific steps deserve a small workflow file, E2E blocker language belongs in the harness doc, and the skills should carry only the short reminders agents need at implementation time.

> AGENT

The first patch is in. I added a dedicated retrofit workflow and wired it into the mandatory reading order, then added the platform and E2E evidence rules where future agents will actually see them during implementation/audit.

> AGENT

The diff is internally linked and the new terms show up where expected. I’m running a whitespace check now; for markdown-only workflow changes that’s the useful local verification without spending time on code gates.

> AGENT

Implemented the doc/skill improvements. Added a new retrofit workflow at [14-retrofit-audits.md](/Users/ericson/.codex/worktrees/55bb/ars-ui/docs/implementation/adapter-components/14-retrofit-audits.md), then wired it into the adapter delivery entry points. Also updated: - [03-framework-rules.md](/Users/ericson/.codex/worktrees/55bb/ars-ui/docs/implementation/adapter-components/03-framework-rules.md) with target capability buckets: `TypedWebDom`, `WebViewBridge`, `ServerOrSsr`, `NoDomNative`. - [05-e2e-fixtures-and-harnesses.md](/Users/ericson/.codex/worktrees/55bb/ars-ui/docs/implementation/adapter-components/05-e2e-fixtures-and-harnesses.md) with E2E failure classification. - [component-delivery.md](/Users/ericson/.codex/worktrees/55bb/ars-ui/docs/implementation/adapter-components/checklists/component-delivery.md) with retrofit, target-capability, stale-symbol-scan, and E2E blocker checklist items. - Leptos, Dioxus, and post-implementation-audit skills with the same concise reminders. Verification: `git diff --check` passes. No code changes or test runs were needed for this docs-only update.