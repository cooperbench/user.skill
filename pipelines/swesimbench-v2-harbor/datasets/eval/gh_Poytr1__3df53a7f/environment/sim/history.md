[DEVELOPER]: Unify the ux toggle button, now there are different styles toggle button

[AGENT]: I'll start by exploring the codebase to understand the current toggle button implementations and their inconsistencies.

[AGENT]: Now I have a clear picture. Let me read the key files to understand the exact differences.

[AGENT]: Now I have a clear picture of the problem. There are **3 different toggle/checkbox styles**: 1. **Radix UI `Checkbox`** component (`components/ui/checkbox.tsx`) — used in some places 2. **Radix UI `Switch`** component (`components/ui/switch.tsx`) — used in source form 3. **Native `<input type="checkbox">`** — used in project-detail.tsx (trigger rules with `accent-[#e8601a]`), project-form.tsx (bare `className="rounded"`), and scan-results-table.tsx (with `accentColor: "var(--beacon-accent)"`) 4. **Custom hand-rolled toggle** in project-detail.tsx (source status toggle, lines 425-435) — entirely custom `<button>` with manual styling The fix: replace all native `<input type="checkbox">` with the Radix UI `Checkbox` component, and replace the custom hand-rolled toggle button with the `Switch` component.

[AGENT]: Now I have the full picture. Here's the problem: **4 different toggle/checkbox styles:** 1. `Switch` (Radix UI) — used in `source-form.tsx` for exclude prereleases and enabled toggles 2. `Checkbox` (Radix UI) — used in subscriptions, release-gate-tab 3. Native `<input type="checkbox">` with `accent-[#e8601a]` — in `project-detail.tsx` trigger rules 4. Native `<input type="checkbox">` with `accentColor: "var(--beacon-accent)"` — in `scan-results-table.tsx` 5. Native `<input type="checkbox" className="rounded">` — in `project-form.tsx` 6. Custom hand-rolled toggle `<button>` — in `project-detail.tsx` source status toggle The fix: replace all native `<input type="checkbox">` with the `Checkbox` component, and replace the custom hand-rolled source status toggle with the `Switch` component. Let me make all the changes now.

[AGENT]: Now replace the custom hand-rolled toggle button (source status) with the `Switch` component.

[AGENT]: Now replace the native checkboxes in the trigger rules section with the `Checkbox` component.

[AGENT]: Now fix `project-form.tsx` — replace the native checkbox with the `Checkbox` component.

[AGENT]: Now fix `scan-results-table.tsx` — replace native checkboxes with the `Checkbox` component.

[AGENT]: Now let me verify there are no remaining native checkbox inputs in the web directory.

[AGENT]: All native checkboxes are gone. Let me also verify the build compiles correctly.

[AGENT]: Clean build, no type errors. Here's a summary of what was unified: **Changes made across 4 files:** | File | Before | After | |---|---|---| | `project-detail.tsx` | Custom `<button>` toggle for source status | `Switch` (Radix UI) | | `project-detail.tsx` | Native `<input type="checkbox">` with `accent-[#e8601a]` for trigger rules | `Checkbox` (Radix UI) | | `project-form.tsx` | Native `<input type="checkbox" className="rounded">` for exclude prereleases | `Checkbox` (Radix UI) | | `scan-results-table.tsx` | Native `<input type="checkbox">` with `accentColor: var(--beacon-accent)` for row selection | `Checkbox` (Radix UI) | Now there are only **two consistent toggle components** used across the app: - **`Checkbox`** — for multi-select / boolean option lists - **`Switch`** — for on/off toggles (source enabled, polling status)