> DEVELOPER

how would you rate current code quality of the project?

> AGENT

I’ll do a quick structural pass first: project shape, dependencies, scripts, and a few representative modules/tests. Then I’ll rate it based on maintainability, correctness risk, testability, and operational readiness.

> AGENT

The repo is a pnpm monorepo with a sizable UI/audit artifact footprint under `tmp/`, but the working tree itself is clean. I’m narrowing now to source layout, scripts, tests, and representative implementation files instead of screenshot artifacts.

> AGENT

The scale is nontrivial: roughly 92k lines of Python backend code and 280k lines of TS/TSX, with hundreds of tests. A few very large files stand out immediately, so I’m checking whether the tooling and architecture rules offset that complexity.

> AGENT

The project has real guardrails: lockfiles, ruff/pytest coverage threshold, TS typecheck/build scripts, a package DAG check, and some custom ESLint. The offsetting concern is that several “core” files are thousands of lines long and appear to centralize schema, coercion, rendering, and command behavior.

> AGENT

One hygiene issue is already visible: generated/local artifacts such as `.coverage`, `.DS_Store`, and many `tmp/ux-*` screenshots are tracked. That may be intentional for evidence artifacts, but it blurs the repo boundary and makes signal-to-noise worse.

> AGENT

The quick gates are mixed but mostly healthy: the architecture check passed, and `uv run ruff` passes. The Makefile’s hardcoded `app/.venv/bin/ruff` target does not currently work in this checkout because that venv lacks `ruff`, although `uv run ruff` does resolve it.

> AGENT

A sampled backend route test passed its assertions, but because pytest applies project-wide coverage on every run, a narrow test command exits nonzero with 21% coverage. The frontend is worse at the moment: `@bim-ai/web` typecheck fails with real source errors, not just test-only noise.

> AGENT

I’d rate the current code quality around **6/10**.

The project has solid foundations: strict TypeScript config, ruff/pytest, Prettier, package architecture checks, many frontend tests, backend coverage enforcement, and a clear monorepo structure. I ran:

- `pnpm architecture` passed
- `pnpm format:check` passed
- `cd app && uv run ruff check bim_ai tests scripts` passed
- frontend tests passed: `669` files / `5462` tests
- sampled backend route assertions passed

The main reason I would not rate it higher is that **the frontend does not currently typecheck**. `pnpm --filter @bim-ai/web typecheck` fails with real source errors, for example nonexistent core exports in [terraceFromFloor.ts](/Users/jhoetter/repos/bim-ai/packages/web/src/plan/terraceFromFloor.ts:1), invalid `PlanTool` usage in [PlanCanvas.tsx](/Users/jhoetter/repos/bim-ai/packages/web/src/plan/PlanCanvas.tsx:5966), missing `onSemanticCommand` references in [InspectorContent.tsx](/Users/jhoetter/repos/bim-ai/packages/web/src/workspace/inspector/InspectorContent.tsx:1673), and stale discriminated-union handling around `family_extrusion`.

Biggest quality risks:

- Several files are far too large for easy maintenance: `PlanCanvas.tsx` ~9.4k lines, `Workspace.tsx` ~6.7k, `packages/core/src/index.ts` ~6k, backend registry ~5.9k.
- Type safety is eroding in pressure areas: many `as any` / `unknown` escape hatches, especially around rendering, inspectors, and command/coercion layers.
- Test signal is noisy: frontend tests pass while emitting repeated React warnings, invalid URL fetch errors, missing canvas APIs, duplicate key warnings, and setState-during-render warnings.
- Python tooling is inconsistent: Makefile targets call `app/.venv/bin/ruff`, but this […]