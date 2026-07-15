[SYSTEM]: # AGENTS.md instructions for /Users/ericson/.codex/worktrees/55bb/ars-ui <INSTRUCTIONS> ## Approach - Read existing files before writing. Don't re-read unless changed. - Thorough in reasoning, concise in output. - Skip files over 100KB unless required. - No sycophantic openers or closing fluff. - No emojis or em-dashes. - Do not guess APIs, versions, flags, commit SHAs, or package names. Verify by reading code or docs before asserting. --- project-doc --- # ars-ui ## Project Overview Rust frontend component library using state machines, framework-agnostic core with Leptos/Dioxus adapters. ## Current Phase The repo is now in active implementation, not spec drafting only. Agents working on implementation should use the GitHub Project roadmap and issue backlog as the execution source of truth: - Use the GitHub Project `ars-ui implementation roadmap` to understand active epics, task breakdown, dependencies, status, and iteration planning. - Prefer picking a single issue-backed task that is unblocked, sized, and scoped for independent delivery. - Do not start work from an epic issue unless the user explicitly asks for planning or further decomposition. - Do not start a task that is blocked by unresolved GitHub issue dependencies. - Treat native GitHub issue dependencies as the blocker graph and the issue body acceptance […]

[DEVELOPER]: Recently we did several improvements on how we design and implement our adapter level components, the first one following those new improvements was the Checkbox one, for both adapters. Now I wanna do an audit of the other components that were already implemented. Starting with the field, fieldset and form components.

[AGENT]: I’ll ground this in the existing workflow and prior adapter work first, then turn it into an audit plan rather than changing files in Plan Mode. I’m using the repo-specific adapter context plus the Superpowers planning guidance because this is a workflow/spec audit, not a one-off code tweak.

[AGENT]: The memory index points to the original Field/Fieldset/Form adapter delivery and one review-found defect: form error counts accidentally included fieldset/container invalid states instead of only named native controls. I’m going to inspect the current adapter workflow docs and the shipped Field/Form code to make the audit plan line up with today’s contract.

[AGENT]: The current checkout is clean, so the plan does not need to account for local uncommitted changes. Next I’m reading the adapter delivery/audit guidance and a representative slice of the Field/Form implementation and tests to identify what the audit should verify against the newer Checkbox standard.

[AGENT]: The newer workflow adds several audit dimensions that probably were not present, or were lighter, when Field/Form first landed: durable browser evidence, explicit consumer-reality review, composition integration, semantic-boundary checks, styled-template boundary checks, and a final outcome matrix with no unknown/workaround rows. I’m checking whether the current Field/Form artifacts already have those pieces or just the older baseline.

[AGENT]: The existing sketch is unusually complete for that earlier work and already records the three-pass parity loop, but it also has an addendum that later narrowed the Tailwind examples back to a “low-level relationship showcase.” The audit should therefore test the current repo against the newest workflow, not simply assume the old sketch remains true.

[AGENT]: I see one concrete likely audit item already: both adapters still have duplicated native-validity extraction and form-error merging logic in `form.rs`. Under the newer semantic-boundary rule, the plan should explicitly classify that as either renderer glue or moveable shared logic before accepting it.

[AGENT]: Another likely audit target is parity between Leptos reactivity and Dioxus props: the Leptos adapter has explicit reactive attr handling for Field/Fieldset error visibility and input relationships, while Dioxus relies on derived attrs from the machine. The audit plan should include specific reactive-update tests rather than just static SSR checks.

[AGENT]: The test surface is broader than I expected: there are SSR tests, wasm browser tests, and E2E assertions for Field/Form, including the earlier error-count regression. I’m going to verify the original issue acceptance criteria and the current component/spec shape so the plan can distinguish “audit only” from “audit plus fix drift.”

[AGENT]: The original issues were narrow 3-point adapter tasks, but the repo’s current adapter workflow now defines a much larger “complete” bar. The key planning choice is whether this pass should be a strict retroactive upgrade to the Checkbox-era bar or a bounded risk audit that files/lands only actual defects and spec drift.

[AGENT]: I’ll plan this as a full retrofit audit: the implementer should compare Field/Fieldset/Form against the current adapter delivery workflow and land all drift, tests, sketch updates, examples, and validation fixes in one PR. I’m reading the planning skill now so the final plan is implementation-ready rather than just an audit outline.

[AGENT]: I have enough to finalize the implementation plan. I’ll keep it scoped to a full retrofit audit for Field, Fieldset, and Form, with the known risk areas called out so an implementer does not have to rediscover them.

[AGENT]: <proposed_plan> # Field/Fieldset/Form Adapter Retrofit Audit Plan ## Summary Run a full retrofit audit of the existing Leptos and Dioxus `Field`, `Fieldset`, and `Form` adapters against the current Checkbox-era adapter delivery workflow. Treat every finding as in-scope for the same PR: spec drift, semantic-boundary drift, missing tests, stale examples, incomplete browser evidence, and parity-matrix gaps all get fixed before handoff. Create a new issue-backed task for this audit rather than reopening closed #332/#423. The PR should close that new audit issue and reference #332/#423 as prior implementation context. ## Key Changes - Re-read, in order, `docs/implementation/adapter-component-delivery.md`, every linked `docs/implementation/adapter-components/*.md` workflow file, all three checklists, `docs/implementation/sketches/332-423-field-form-counterpart-sketch.md`, and the component/adapter specs for `field`, `fieldset`, and `form`. - Compare the current implementation in `crates/ars-leptos/src/utility/{field,fieldset,form,field_support}.rs` and `crates/ars-dioxus/src/utility/{field,fieldset,form,field_support}.rs` against the specs and current workflow. - Explicitly audit these known risk areas: - duplicated native-validation/error-merging logic in both adapter `form.rs` files; - Leptos vs Dioxus reactive update parity for validation errors, form validation maps, fieldset inherited state, input relationships, and reset behavior; - Dioxus hook-order and global-attribute/event-strip behavior; - whether Field/Form examples remain “consumer applications” and do not reimplement component-owned validation or ARIA policy; - whether current E2E/widget evidence still matches the final outcome matrix after […]

[DEVELOPER]: PLEASE IMPLEMENT THIS PLAN: # Field/Fieldset/Form Adapter Retrofit Audit Plan ## Summary Run a full retrofit audit of the existing Leptos and Dioxus `Field`, `Fieldset`, and `Form` adapters against the current Checkbox-era adapter delivery workflow. Treat every finding as in-scope for the same PR: spec drift, semantic-boundary drift, missing tests, stale examples, incomplete browser evidence, and parity-matrix gaps all get fixed before handoff. Create a new issue-backed task for this audit rather than reopening closed #332/#423. The PR should close that new audit issue and reference #332/#423 as prior implementation context. ## Key Changes - Re-read, in order, `docs/implementation/adapter-component-delivery.md`, every linked `docs/implementation/adapter-components/*.md` workflow file, all three checklists, `docs/implementation/sketches/332-423-field-form-counterpart-sketch.md`, and the component/adapter specs for `field`, `fieldset`, and `form`. - Compare the current implementation in `crates/ars-leptos/src/utility/{field,fieldset,form,field_support}.rs` and `crates/ars-dioxus/src/utility/{field,fieldset,form,field_support}.rs` against the specs and current workflow. - Explicitly audit these known risk areas: - duplicated native-validation/error-merging logic in both adapter `form.rs` files; - Leptos vs Dioxus reactive update parity for validation errors, form validation maps, fieldset inherited state, input relationships, and reset behavior; - Dioxus hook-order and global-attribute/event-strip behavior; - whether Field/Form examples remain “consumer applications” and do not reimplement component-owned validation or ARIA policy; - whether current E2E/widget evidence still matches the final […]

[AGENT]: I’ll execute this as an implementation task now. First I’m loading the execution/TDD/framework skills and the project audit skill, then I’ll re-read the adapter workflow docs and start with concrete drift tests before code changes.

[AGENT]: I’m using the executing-plans skill to implement this plan. The plan is coherent; the only operational caveat is that creating the GitHub issue and moving the board item may need network escalation, so I’ll try the normal `gh` path first and request approval only if the sandbox blocks it.

[AGENT]: I’m reading the full adapter workflow set now. This is intentionally front-loaded because the retrofit bar lives mostly in those docs, not in the older #332/#423 issue bodies.

[AGENT]: The checkout is clean but currently detached (`HEAD (no branch)`). I’m creating a scoped work branch before editing so the audit does not happen on a detached state.

[AGENT]: Branch is now `codex/field-form-adapter-retrofit-audit`. I’m continuing the mandatory workflow/spec read before choosing the first failing test.

[AGENT]: I’m also validating the isolation requirement from the execution workflow. This checkout is already a dedicated Codex worktree, and I’ve switched it to a scoped branch, so I’m not creating a nested worktree inside it.

[AGENT]: The workflow confirms that the first likely fix should be semantic-boundary related: both adapters carry duplicated form validation helpers that classify native validity into `ars_forms::validation::Error`. I’m checking the forms crate before editing because that looks like the right shared home.

[AGENT]: I’ve finished the main workflow read. Next I’m reading the exact specs and current code/test surfaces for `field`, `fieldset`, and `form`, then I’ll create the GitHub audit issue and start the first TDD cycle.

[AGENT]: The workflow read found no blocker to starting, and the existing sketch already names a later scope correction around Tailwind examples. I’m creating the new audit issue now so the work has the issue-backed record requested in the plan.

[AGENT]: The audit issue is created as #730. I’m aligning the project board next, then I’ll move into code-level drift tests.

[AGENT]: Issue #730 exists under the roadmap project owner. I’m adding it to the roadmap and setting its status to In Progress before touching code.

[AGENT]: The roadmap field IDs are resolved. I’m setting #730 to In Progress and marking it as adapter/Both/mixed on the board.

[AGENT]: The issue is on the roadmap and In Progress. I’m reading the exact component specs plus current adapter files and tests now; this should identify the first failing test target.

[AGENT]: One board detail is done; I’m keeping the rest local until the code is verified. The current audit candidate remains shared native validation logic, but I’m checking spec wording and existing tests before writing that red test.

[AGENT]: The forms validation module is directory-backed, not a flat `validation.rs`. I’m reading its public API and the component specs now; the first red test will likely target a shared validity classifier rather than adapter rendering.

[AGENT]: The shared form domain already owns localized `Error` construction and form messages, but it does not yet expose a framework-neutral way to map browser validity flags into those errors. I’m checking whether existing specs imply that helper before adding it.

[AGENT]: The spec confirms the rule: adapters should resolve native/browser validation, but shared validation semantics belong in `ars-forms`. I’m going to add a small public `NativeValidity` helper in `ars-forms::validation`, with adapters reduced to DOM extraction plus event wiring. First I’m writing the failing shared tests.

[AGENT]: I’m adding the red tests in `ars-forms` first. They describe the shared behavior both adapters currently duplicate: validity precedence, typed mismatch mapping, fallback, and merging native errors into controlled error maps.

[AGENT]: There are no integration tests for `ars-forms` yet, so I’m putting focused unit tests beside the validation module rather than adding a new test target.

[AGENT]: I intentionally referenced the new module/API before creating it so the next command should fail at compile time for the missing shared helper. Then I’ll add the tests and implementation.

[AGENT]: The red check failed for the expected reason: `ars_forms::validation::native` does not exist. I’m adding the shared helper now, keeping it free of web/framework types so adapters only extract DOM facts.

[AGENT]: The shared helper is in place. I’m running the focused `ars-forms` tests now before touching the adapter code.

[AGENT]: That test command was malformed because Cargo only accepts one test filter before `--`. I’m rerunning the module’s tests with the broader `native` filter.

[AGENT]: The shared tests are green. I’m replacing duplicated adapter classification code with DOM extraction into `NativeValidity`, leaving only framework/browser glue in each adapter.

[AGENT]: I’m applying the adapter refactor now. The duplicated error-decision functions go away; the remaining helpers are explicitly browser DOM extraction.

[AGENT]: The first patch missed because of context ordering. I’m applying the same refactor in smaller patches to keep the edit exact.

[AGENT]: The Leptos form import and merge path are now shared. I’m replacing the remaining native error classifier block with DOM extraction helpers.

[AGENT]: The Dioxus form has the same duplicated classifier. I’m applying the matching shared-helper refactor there, preserving the Dioxus event/ref extraction paths.

[AGENT]: Both adapters now call into `ars_forms` for validation semantics. I’m running the native forms tests plus the two SSR form test targets to catch compile or behavior regressions before continuing.

[AGENT]: The shared tests passed. The adapter form tests are still compiling; I’m polling those sessions and then I’ll continue with any compile fixes they surface.

[AGENT]: Dioxus SSR form tests pass, but native-only compilation warns because the new DOM extraction types are only used on wasm/web. I’ll gate those imports before the warning sweep. The Leptos test target is still compiling.

[AGENT]: While Leptos compiles, I’m fixing the native-target warning source by moving `NativeInputType` and `NativeValidity` behind each adapter’s wasm cfg.

[AGENT]: The Leptos command completed, but that target is cfg-gated to SSR so it ran zero tests without SSR features. I’ll use the project’s focused commands later with the right feature setup; for now I’m continuing the audit for actual gaps.

[AGENT]: The next concrete drift is part styling: Field and Fieldset are multi-part components, but most Leptos parts do not expose `class`/`style`, and Dioxus parts do not extend `GlobalAttributes`. That is now required by the adapter workflow. I’m writing SSR tests for those part attributes before changing component props.

[AGENT]: Continuing from the compaction point. The shared native-validity helper is in place and locally green; I’m moving to the next drift area: part-level consumer attributes and styling parity across Field and Fieldset.

[AGENT]: The current tests only prove root/input classes and basic anatomy. Checkbox-era tests cover every compound part with class/style, so I’m adding equivalent failing coverage for Field and Fieldset before changing the adapters.

[AGENT]: I found the shared Leptos `apply_part_attrs` helper added by the checkbox work, and Dioxus already has the global-attribute merge path. The retrofit is straightforward: tests first, then wire the Field/Fieldset subparts through those existing adapter conventions.

[AGENT]: I’ve added the red tests for part attributes. Next I’m running focused SSR tests to capture the expected failures before changing component props.

[AGENT]: The red checks failed exactly at the missing public props for the subparts. I’m wiring the parts now, preserving component-owned ARIA/IDs and only merging consumer class/style/global attrs at the adapter boundary.

[AGENT]: One additional drift fell out while inspecting Form: Leptos `Form` still only accepted `class` on the root while Dioxus forwards full globals. I’m keeping that as part of the same semantic-boundary fix by adding a Leptos `style` root prop and using the existing style conversion helper.

[AGENT]: The component changes are in. I’m rerunning the focused SSR/unit tests now; this will also catch any prop or macro shape issues from the Leptos and Dioxus component builders.

[AGENT]: The part-attribute retrofit is green in focused SSR/unit tests. I’m expanding back to Form/root parity and the remaining reactive/browser evidence areas so the audit does not stop at the first visible drift.

[AGENT]: The adapter specs confirm the root merge contract explicitly calls out additive `class` and `style`. Dioxus already satisfies that through global attrs; Leptos Form needs the same public root style hook.

[AGENT]: The Form root style test is added. I’m checking the red/green split next: Dioxus should already pass, and Leptos should fail until the root style prop is wired.

[AGENT]: Dioxus is already green for Form root globals; Leptos produced the expected missing-style failure. I’m adding the Leptos root style prop using the existing shared style converter.

[AGENT]: Leptos Form now has the style hook. I’m rerunning the focused Form test and then I’ll run the full Field/Fieldset/Form SSR suite for both adapters.

[AGENT]: The shared native-validity tests and Leptos Form root style test are green. I’m running the full focused SSR/unit set for all three components in both adapters now.

[AGENT]: The full focused SSR/unit suites are passing for both adapters. I’m moving to the browser-test side of the audit: locating the wasm tests and checking whether the changed attr merge/native-validation paths are covered there.

[AGENT]: The plan’s wasm filenames differ from the repo’s actual `test_*_wasm.rs` convention. I found the real files and am reading those now instead of relying on the stale names.

[AGENT]: The wasm coverage already exercises the high-risk reactive paths: form validation maps, field error relationships, fieldset inheritance, input value callbacks, reset, and native validation. The new styling changes are static SSR evidence, so I’m not adding browser-only tests for those, but I will run the existing browser suites.

[AGENT]: The audit found an actual parity gap in browser evidence: Leptos Fieldset has tests for error inheritance and reactive inherited state updates, while Dioxus only covered initial inherited state. I’m adding the missing Dioxus browser tests before touching any code.

[AGENT]: The missing Dioxus Fieldset browser tests are in. I’m running that wasm target now; if it fails, the failure will tell us whether it was only an evidence gap or also an implementation gap.

[AGENT]: The Dioxus Fieldset wasm test is still compiling from a cold wasm target. I’m waiting for the run to finish before deciding whether implementation changes are needed.

[AGENT]: The wasm binary compiled, but the runner could not spawn its browser server inside the sandbox. Per the repo workflow this browser evidence matters, so I’m rerunning the same command with escalation. It also surfaced a Dioxus `reset_generation` dead-code warning on this target that I’ll fix at the root.

[AGENT]: The added Dioxus Fieldset browser tests all pass, so that was an evidence gap rather than a runtime bug. I’m removing the unused Dioxus form-context field that the wasm compile exposed, since the reset signal is only needed inside `Form` itself.

[AGENT]: The wasm warning fix is in. I’m running the hook-order probe and then the focused browser suites for all Field/Fieldset/Form wasm tests.

[AGENT]: The hook probe returned no matches, which is the expected clean result. Both adapter wasm test batches are running now; Leptos is still compiling, and Dioxus is waiting on the shared build lock.

[AGENT]: The Dioxus browser suite is green: 19 wasm tests across Field, Fieldset, and Form. Leptos is still building/running; I’m waiting on that result next.

[AGENT]: Both browser batches are green now. I’m updating the adapter specs and retrofit sketch to reflect the new shared forms helper, part/global-attribute support, and the browser evidence matrix from this audit.

[AGENT]: The spec files still described the pre-checkbox-style subpart APIs, so I’m correcting that drift now. I’m keeping the edits focused: API/merge notes plus a dated retrofit addendum with the exact test evidence from this audit.

[AGENT]: One older foundation section still shows `validation_errors` as `Vec<String>` while the adapters and validation crate use structured `Error`. I’m treating that as spec drift from the audit and tightening it to the current structured error contract.

[AGENT]: I’m applying the spec/documentation updates now: structured form errors in the foundation spec, public attr/style props in adapter specs, and the dated retrofit addendum in the counterpart sketch.

[AGENT]: One documentation patch did not apply because the surrounding spec text has diverged slightly. I’m splitting the edits into smaller patches against the exact current text.

[AGENT]: The foundation spec and Leptos Field API snippet are updated. I’m continuing through the Dioxus and Fieldset/Form adapter specs in small targeted edits.

[AGENT]: The Field/Fieldset specs now match the new public styling/global-attribute surface. I’m doing the same for Form, then I’ll append the audit addendum.

[AGENT]: Form specs are updated. I’m adding a 2026-06-16 retrofit audit addendum to the existing sketch with the fresh local evidence and final matrix deltas from this pass.

[AGENT]: The sketch now has a dated retrofit addendum with the audit issue, findings, and evidence. I’m checking E2E utility coverage next so the widget/E2E evidence side of the plan is not just inferred from adapter tests.

[AGENT]: Adapter parity is clean. The E2E command help process is still open because it paged/printed slowly, so I’m polling it, then I’ll run the focused utility harnesses if the CLI shape is clear.

[AGENT]: The E2E entrypoint is `cargo xtask e2e utility`. I’m checking its options so I can run the focused utility harnesses against both adapters without guessing flags.

[AGENT]: The focused E2E harness supports `--adapter leptos|dioxus`. I’m running both utility harnesses now; these spawn local fixture servers and browser automation, so I’m using the approved path for local browser E2E.

[AGENT]: Both E2E runs have compiled and launched their adapter harnesses. I’m waiting for browser assertions to finish.

[AGENT]: The Dioxus E2E run timed out inside Chrome while both harnesses were running concurrently. I’m checking the Leptos run, then I’ll rerun Dioxus sequentially to avoid browser contention before treating it as a real failure.

[AGENT]: Leptos also timed out during category-tab discovery, consistent with the concurrent browser/server runs interfering rather than a Field/Form assertion. I’m rerunning the E2E harnesses one at a time.

[AGENT]: The sequential Leptos E2E rerun still times out before the Utility tab is visible, so this is not a Field/Form assertion failure yet. I’m inspecting the E2E harness startup and fixture logs to determine whether the app failed to serve, the selector changed, or Chrome is stuck.

[AGENT]: The E2E failure is happening before any Field/Form check, at the common “open Utility panel” step. I’m checking fixture startup details and temp logs rather than changing component code for that.

[AGENT]: The E2E harness has a 15-second common tab-discovery timeout, and the failures occur there before any utility assertion. I’m not patching harness timing as part of this adapter audit; I’ll report this as an E2E startup blocker after running the remaining local gates.

[AGENT]: The attempted warning cleanup was too aggressive: checkbox form-reset support reads `FormContext.reset_generation` in the input adapter. I’m restoring that field and marking the wasm-only unused warning deliberately rather than removing the contract.

[AGENT]: The Dioxus form context is restored with a scoped `#[expect(dead_code)]` reason. I’m rerunning the Dioxus SSR/unit suite that caught it.

[AGENT]: Native builds use `reset_generation`, so the unconditional expectation causes an unfulfilled-lint warning there. I’m narrowing the expectation to wasm builds where the utility-only target can compile without the checkbox consumer.

[AGENT]: The reset-generation lint expectation is now wasm-only. I’m rerunning the Dioxus focused suite to confirm it is warning-free before continuing.

[AGENT]: The Dioxus focused suite is clean again. I’m finishing the required post-implementation-audit skill instructions before running that audit pass.

[AGENT]: I’ve completed the audit review passes in substance: spec drift, layer drift, test breadth, parity matrix, and E2E startup. I’m running formatter and clippy next; coverage via the adapter wasm recipe may be heavier, so I’ll decide after the warning gates are clean.

[AGENT]: `cargo xfmt` passed. It formats broad Dioxus surfaces by design, so I’ll inspect the diff after verification to make sure there isn’t unrelated churn. Now I’m running the workspace clippy wrapper.

[AGENT]: `cargo xclippy` is still running through the workspace. I’m waiting for the final result before making any more changes.

[AGENT]: Clippy has reached the local crates and is still running. No changed-code warnings have appeared yet.

[AGENT]: Clippy found only the new Dioxus `part_attrs` closures. I’ll let the wrapper finish, then replace those with method items instead of suppressing them.

[AGENT]: The wrapper is in its final i18n lane. The actionable warnings are already identified and scoped to the new Dioxus part-attribute code.

[AGENT]: `cargo xclippy` completed, with the seven Dioxus redundant-closure warnings from the new attr merge calls. I’m fixing those now at the call sites.

[AGENT]: The Dioxus warnings are fixed by using the machine API method items directly. I’m formatting again, then rerunning focused tests and clippy to verify the warning sweep is clean.

[AGENT]: Formatting is clean after the clippy fixes. I’m rerunning the focused tests plus `cargo xclippy` now to confirm the warnings are gone.

[AGENT]: The method-item version does not satisfy the generic lifetime bound in normal builds. I’m reverting to closures and adding scoped `#[expect(clippy::redundant_closure_for_method_calls)]` annotations, matching the existing checkbox pattern for these API callbacks.

[AGENT]: The lifetime-safe closure form is restored with explicit expectations. I’m formatting and rerunning Dioxus focused tests plus clippy.

[AGENT]: Format and Dioxus focused tests are green again. I’m running `cargo xclippy` one more time to confirm the scoped expectations satisfy the wrapper.

[AGENT]: `cargo xclippy` is clean for changed code; only the existing third-party future-incompat note remains. I’m rerunning the browser wasm suites after the clippy/format changes to keep the final evidence current.

[AGENT]: Final wasm and spec validation are green. I’m running a focused native coverage read for the shared `ars-forms::validation::native` helper added in this audit; adapter wasm coverage is covered by the browser test matrix here, while full merged coverage is the longer CI-style gate.

[AGENT]: The focused coverage run passed, but the annotated output is too broad for a useful summary because `cargo llvm-cov --text` prints the whole crate. I’m rerunning it as a concise summary so the final audit evidence is readable.

[AGENT]: The native helper coverage is 99.28% line / 100% function coverage; I’m checking the one missed line so the audit can classify it rather than just quote a number.

[AGENT]: The one uncovered native helper line is the `NativeInputType::Other` mismatch branch. That is a real branch, so I’m adding a small test rather than leaving it as a coverage gap.

[AGENT]: The test block had shifted from formatting, so I found the exact insertion point and am adding the uncovered `Other` mismatch case there.

[AGENT]: The coverage gap test is in. I’m formatting and rerunning the native helper tests plus the concise coverage summary.

[AGENT]: The shared native helper is now at 100% line/function coverage for the touched file. I’m running one final `cargo xclippy` after the added test.

[AGENT]: All requested local gates that are not blocked by the E2E tab-discovery issue are green. I’m checking the final diff now, including whether `cargo xfmt` introduced unrelated churn.

[AGENT]: The diff is scoped to the adapters, forms helper, tests, and audit/spec docs. I’m doing one last hook probe after formatting and then I’ll summarize.

[AGENT]: Implemented the Field/Fieldset/Form adapter retrofit audit on `codex/field-form-adapter-retrofit-audit`. Created and moved audit issue to In Progress: `#730` (`audit: Retrofit Field, Fieldset, and Form adapters to current delivery workflow`). What changed: - Moved duplicated native validity/error-map logic out of both adapter `form.rs` files into `ars_forms::validation::{NativeValidity, NativeInputType, merge_error_map}`. - Added Leptos `class`/`style` support for Field and Fieldset compound parts, plus `Form.style`. - Added Dioxus `GlobalAttributes` support for Field and Fieldset compound parts. - Added SSR/unit tests for part styling parity in both adapters. - Added Dioxus wasm Fieldset parity tests for error inheritance and reactive inherited state updates. - Updated adapter specs, forms foundation spec, and the Field/Form counterpart sketch with a 2026-06-16 retrofit audit addendum. Verification: - `cargo test -p ars-forms --lib native`: pass, 6 tests - `cargo llvm-cov test -p ars-forms --lib --summary-only -- native`: `validation/native.rs` is 100% line/function coverage - `cargo test -p ars-leptos --features ssr --test field --test fieldset --test form`: pass - `cargo test -p ars-dioxus --test field --test fieldset --test form`: pass - Leptos wasm Field/Fieldset/Form tests: pass, 17 tests - Dioxus wasm Field/Fieldset/Form tests: pass, 19 tests - `cargo xtask lint adapter-parity`: pass - Dioxus hook probe: no matches - `cargo xtask spec validate`: pass […]

[DEVELOPER]: Should we have styled components for those 3 components or just the low level unstyled that we will compose later with more higher level components? Actual question, don't change any code yet

[AGENT]: I’ll use the brainstorming skill here because this is an API/design decision, not an implementation request.

[AGENT]: I’m going to answer this as a design call only. I’m using the brainstorming skill because this is a product/API shape decision, not an implementation step.

[AGENT]: I’d keep `Field`, `Fieldset`, and `Form` as low-level unstyled primitives. More precisely: they should be **stylable primitives**, not **styled components**. Their job is semantic ownership: ids, ARIA relationships, invalid/valid state propagation, fieldset inheritance, form validation maps, reset behavior, native validity mapping, and status/error wiring. They should not own visual policy like spacing, borders, colors, required-marker presentation, helper-text typography, or layout. That gives us the right layering: - `Form`: semantic submit/reset/validation boundary. - `Fieldset`: grouped field state and relationship boundary. - `Field`: label/description/error/input relationship boundary. - Future higher-level components: `TextField`, `SelectField`, `CheckboxField`, `FormSection`, design-system wrappers, etc. Those can compose the primitives and own richer styling/UX. So the right contract is: expose `class`, `style`, global attrs, stable `data-ars-*` state/part attributes, and examples that show consumer styling. But don’t add first-class styled `Field`/`Fieldset`/`Form` exports in the adapters yet. The one exception is accessibility-required behavior, like hidden status-region mechanics or relationship attributes. That belongs in the primitive. Visual design belongs later, at the higher-level component or app/design-system layer.

[DEVELOPER]: Are we following this intended contract now after the audit?

[AGENT]: I’ll check the touched adapter surfaces against that “stylable primitive, not styled component” boundary so I can answer from the actual diff, not memory.

[AGENT]: Yes, in the current audit diff we are following that contract. What changed is **stylability**, not **styled components**: - Leptos `Field`, `Fieldset`, and `Form` now expose additive `class` / `style` where needed. - Dioxus parts now extend `GlobalAttributes`. - Core semantic attrs still win: ids, ARIA relationships, validity state, descriptions, errors, disabled/read-only propagation, etc. - No new visual API was introduced: no `variant`, `size`, `tone`, theme props, bundled classes, or styled wrapper exports. - Shared validation/error logic moved down into `ars-forms`, while adapters keep renderer/DOM extraction glue. So the boundary is now basically: ```text ars-leptos / ars-dioxus utility components: own semantics + relationships + state propagation allow consumer styling hooks future higher-level components / design-system wrappers: own visual layout + styling + richer field UX ``` The only caveat: the E2E utility harness still timed out before reaching Field/Form assertions, so the browser-level evidence is incomplete. But from the code/spec surface, the primitive-vs-styled contract is aligned.

[DEVELOPER]: Are we exposing the lower level parts for all of them as needed, so they can be styled independently?

[AGENT]: I’ll verify the public component parts rather than infer from the earlier audit notes. The main distinction is that `Field` and `Fieldset` have visible compound parts, while `Form` mostly has a root semantic boundary.

[AGENT]: The visible part inventory is mostly aligned. I’m checking whether `Form` has a status/live-region part in the contract, because that is the only likely gap in “independently styled lower-level parts.”

[AGENT]: One nuance surfaced: the spec currently treats `Form::StatusRegion` as a structural adapter-owned node, not a public child component. That means it is addressable by data attributes, but not independently configurable through a `StatusRegion` component API.

[AGENT]: Mostly yes, with one deliberate caveat. Current public/stylable surface: | Component | Exposed lower-level parts | Independently stylable now? | |---|---|---| | `Field` | `Field`, `Label`, `Input`, `Description`, `ErrorMessage` | Yes | | `Fieldset` | `Fieldset`, `Legend`, `Description`, `Content`, `ErrorMessage` | Yes | | `Form` | `Form` root, internal `StatusRegion` | Root yes; `StatusRegion` is not a public component | For `Field` and `Fieldset`, yes: the visible subparts are exposed and can be styled independently. Leptos has `class` / `style` on the parts; Dioxus exposes `GlobalAttributes` on the parts. For `Form`, the only public component is the root form. The status live region is rendered, has core `data-ars-scope` / `data-ars-part="status-region"` attrs, and can be targeted by CSS selectors, but there is no public `<StatusRegion>` compound part or direct `class` / `style` prop for it. That matches the current adapter spec, which says the status region is adapter-owned structural UI. So if the intended contract is “all visible composition parts are independently stylable,” we’re aligned. If the intended contract is stricter, meaning “every core part, including `Form::StatusRegion`, must have a public stylable adapter component or direct styling prop,” then `Form` still has a gap. My take: keep `StatusRegion` internal unless we […]