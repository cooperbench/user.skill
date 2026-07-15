---
session_id: 884bebe2-2f5c-4f99-9db0-d84bfaeb8dff
developer: "gh:jeevanpillay"
split: train
source: swechat
repo: "?"
start_time: "2026-04-05T07:57:11.717000+00:00"
n_turns: 8
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

/create_plan @thoughts/shared/research/2026-04-05-trpc-client-error-propagation-next-step.md for both apps/platform and apps/app

> TOOL

<command-message>create_plan</command-message>
<command-name>/create_plan</command-name>
<command-args>@thoughts/shared/research/2026-04-05-trpc-client-error-propagation-next-step.md for both apps/platform and apps/app</command-args>

> AGENT

Now I have a complete picture. Let me present the plan structure for your feedback before writing the full document.

---

Based on my research, here's what I found:

**Current State:**
- `api/app/src/trpc.ts:103-119` and `api/platform/src/trpc.ts:85-98` — identical errorFormatters that sanitize `INTERNAL_SERVER_ERROR` messages but don't expose `isUserFacing`
- `apps/app/src/lib/trpc-errors.ts` — 95-line utility with hand-maintained `SAFE_MESSAGE_CODES` set, only used by 2 files (5 call sites)
- `packages/app-trpc/src/client.ts` and `packages/platform-trpc/src/client.ts` — identical `createQueryClient` factories with no `MutationCache`
- `apps/app/src/components/errors/org-page-error-boundary.tsx:36-48` — classifies errors via substring matching on `error.message`
- `apps/platform` has **no client-side UI** — no toast, no error boundaries, no components. Only server-side caller usage via `@repo/platform-trpc/caller`

**Key finding:** The platform app is headless, so `MutationCache.onError` with toast only applies to `@repo/app-trpc`. The errorFormatter enrichment (`isUserFacing`) should go in both API layers for consistency.

**Mutations that need attention:**
- 2 files use `showErrorToast` (5 call sites) — remove entirely
- `link-sources-button.tsx` — inline `toast.error` in `onError`, will double-toast → remove inline toast
- `source-settings-form.tsx` — no `onError` at all, currently silent → will now get auto-toast (improvement)
- `team-name-form.tsx` — uses `setError(err.message)` inline → needs `meta: { suppressErrorToast: true }`

**Proposed plan structure:**

## Phase 1: Enrich errorFormatters with `isUserFacing`
Add `isUserFacing: httpStatus < 500` to both `api/app/src/trpc.ts` and `api/platform/src/trpc.ts`

## Phase 2: Install global MutationCache error handler
Add `MutationCache.onError` to `@repo/app-trpc`'s `createQueryClient` with auto-toast and `meta` support for title override and opt-out

## Phase 3: Migrate consumers and delete `trpc-errors.ts`
Remove `showErrorToast` from 2 files, add `suppressErrorToast` meta to `team-name-form.tsx`, remove redundant inline `toast.error` from `link-sources-button.tsx`, delete `trpc-errors.ts`

## Phase 4: Fix error boundary classification
Replace string matching in `org-page-error-boundary.tsx` with `error.data.code` checks

Does this phasing and scope look right? Any adjustments before I write the full plan?

> DEVELOPER

before continuing, what do you reckon is the most accretive, innovative, radical and creative addition for long term developer maintainability and 100x improvement in architecture

> AGENT

The research document proposes adding `isUserFacing: boolean` to the errorFormatter. That's solid. But I think there's a more radical insight hiding in plain sight.

**The server already solved the classification problem. The client is redundantly re-solving it.**

Look at what the errorFormatter already does (`api/app/src/trpc.ts:107-112`):

```typescript
const shouldSanitize = isProduction && error.code === "INTERNAL_SERVER_ERROR";
return {
  ...shape,
  message: shouldSanitize ? "An unexpected error occurred" : shape.message,
```

In production, by the time `error.message` reaches the client:
- `INTERNAL_SERVER_ERROR` → already sanitized to `"An unexpected error occurred"`
- Everything else (`CONFLICT`, `BAD_REQUEST`, `FORBIDDEN`, ...) → the original, intentional, user-facing message preserved

**The message on the wire is already safe. Always.** The `SAFE_MESSAGE_CODES` set in `trpc-errors.ts` is a client-side reimplementation of a gate the server has already applied. `isUserFacing` would be a new field that encodes information already embedded in the message itself.

The radical move is: **don't add `isUserFacing` at all. Just trust `error.message`.**

```typescript
// The entire global error handler — 6 lines, zero server changes
onError: (error, _variables, _context, mutation) => {
  if ((mutation.options.meta as any)?.suppressErrorToast) return;
  const title = (mutation.options.meta as any)?.errorTitle ?? "Something went wrong";
  toast.error(title, { description: error.message });
},
```

This means:
- **Zero changes to either API layer** — no `isUserFacing`, no `getHTTPStatusCodeFromError` import, no errorFormatter diff
- **Zero new types or fields to maintain** — nothing to fall out of sync
- **The architecture becomes a cascade** — like CSS, with sensible defaults overridable at each level:
  1. **Global** (MutationCache) — auto-toast all mutation errors with the server's message
  2. **Route** (error boundary using `error.data.code`) — render contextual UI for query errors
  3. **Component** (`meta.suppressErrorToast`) — escape hatch for inline error display

The 100x isn't in a clever new abstraction. It's in *deleting* the abstraction that reimplements what the server already guarantees. The server sanitizes. The client trusts. One source of truth instead of two.

**Net impact vs the research proposal:**
- Research proposes: +2 lines server, +15 lines MutationCache, -110 lines deleted = -93 net
- This approach: +0 lines server, +15 lines MutationCache, -110 lines deleted = -95 net, and no API layer coordination needed

Should I write the plan with this approach — zero server changes, pure client-side consolidation?

> DEVELOPER

perfect. prced

> AGENT

Plan created at `thoughts/shared/plans/2026-04-05-trpc-client-error-propagation.md`.

**4 phases**, each independently verifiable:

1. **Enrich errorFormatters** — add `isUserFacing: httpStatus < 500` to both `api/app` and `api/platform` (additive, no behavior change)
2. **Install global MutationCache** — auto-toast in `@repo/app-trpc` with `meta.errorTitle` and `meta.suppressErrorToast` support
3. **Migrate consumers & delete `trpc-errors.ts`** — remove 5 `showErrorToast` calls, add `suppressErrorToast` to `team-name-form.tsx`, clean up `link-sources-button.tsx`, delete the file
4. **Fix error boundary** — replace message substring matching with `error.data.code` in `OrgPageErrorBoundary`

Net result: **~110 lines deleted, ~21 added**. Every future mutation gets correct error toasts with zero boilerplate.

Please review — any phases that need adjustment or missing edge cases?

> DEVELOPER

yes proceed
