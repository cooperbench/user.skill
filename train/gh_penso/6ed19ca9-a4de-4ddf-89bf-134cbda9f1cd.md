---
session_id: 6ed19ca9-a4de-4ddf-89bf-134cbda9f1cd
developer: "gh:penso"
split: train
source: swechat
repo: "?"
start_time: "2026-04-16T19:54:25.700067Z"
n_turns: 20
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Looking at https://github.com/moltis-org/moltis/issues/739 would it make sense to have a "brain" option next to the provider/llm in the web-ui, enabled when the model has a thinking mode (low/medium/high etc)? How many models do we support which have thinking mode, with different thinking mode?

> AGENT

Great, now I have the full picture. Here's my analysis:

## Issue #739: Configuring Reasoning Effort for OpenRouter

The user wants to set reasoning effort for OpenRouter models — either globally or per-model. Currently, reasoning effort is only applied for **native** providers (Anthropic, OpenAI) but not for BYOM (bring-your-own-model) providers like OpenRouter.

## Current State of Thinking Mode Support

The codebase already has solid reasoning infrastructure:

**`ReasoningEffort` enum** (`crates/config/src/schema.rs`): `Low`, `Medium`, `High`

**Models with thinking support** (detected via `supports_reasoning_for_model()` in `model_capabilities.rs`):

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude Opus 4.5+, Sonnet 4.5+, Opus 4.6+, Sonnet 4.6+, 3.7 Sonnet |
| **OpenAI** | o1, o1-mini, o3, o3-mini, o4, o4-mini, GPT-5.x |
| **Google** | Gemini 2.5+, 3.x Flash/Pro |
| **DeepSeek** | R1 / deepseek-reasoner |
| **xAI** | Grok 3+, Grok 4 series |

**Existing mechanisms:**
- Model ID suffix: `claude-opus-4-5@reasoning-high` — auto-generates 3 variants per reasoning-capable model
- Agent presets: `reasoning_effort = "high"` in TOML config
- Web UI already renders reasoning output in collapsible `<details>` disclosures

## Would a "Brain" Toggle in the Web UI Make Sense?

**Yes, absolutely.** Here's why:

1. **The backend is ready** — `ReasoningEffort` enum, `with_reasoning_effort()` on providers, and `ModelCapabilities.reasoning` flag all exist. The web UI just doesn't expose a control for it yet.

2. **The `@reasoning-*` suffix approach is awkward for users** — it triples the model list (every reasoning-capable model gets 3 extra entries). A toggle next to the model selector would be much cleaner.

3. **It solves #739 naturally** — OpenRouter proxies models from multiple providers. If the UI lets users pick reasoning effort for any model flagged as reasoning-capable, it works regardless of whether the backend is native Anthropic or OpenRouter-proxied Claude.

4. **Implementation path is clear:**
   - The `/api/gon` endpoint already sends `ModelCapabilities` (including `reasoning: bool`) to the frontend
   - When a reasoning-capable model is selected, show a brain icon / toggle with Low/Medium/High options
   - Send the chosen effort as part of the chat request (could be a simple query param or body field)
   - Backend already knows how to apply it via `with_reasoning_effort()`

5. **Different providers use different mechanisms** but that's already abstracted — Anthropic uses `budget_tokens`, OpenAI uses `reasoning_effort` string, and the provider layer handles the translation.

**The main gap for #739 specifically** is that OpenRouter (and other OpenAI-compatible providers) need to actually pass the reasoning parameters through. The `apply_reasoning_effort_chat()` / `apply_reasoning_effort_responses()` methods on the OpenAI provider would need to be used by OpenRouter's provider implementation too, since OpenRouter supports the `reasoning_effort` field for compatible models.

**Suggested approach:** A small brain icon next to the model selector that, when the selected model has `reasoning: true`, expands to show Low/Medium/High buttons (similar to selection cards already used elsewhere). This would be cleaner than the current suffix-based model variants and would address #739 for all BYOM providers at once.

> DEVELOPER

ok proceed

> AGENT

Here's a summary of all changes:

## Changes Summary

### New files (2)
- **`crates/web/src/assets/js/reasoning-toggle.js`** — Self-contained reasoning toggle module with bind/unbind lifecycle, dropdown rendering, and session restore helper
- **`crates/web/ui/e2e/specs/reasoning-toggle.spec.js`** — 7 E2E tests covering visibility, dropdown options, effort selection, model ID suffix, variant filtering, and auto-reset

### Modified files (7)

**`stores/model-store.js`** — Added:
- `reasoningEffort` signal (persisted to localStorage)
- `supportsReasoning` computed (derives from selected model)
- `effectiveModelId` computed (appends `@reasoning-*` suffix when active)
- `parseReasoningSuffix()` / `isReasoningVariant()` helpers
- `setReasoningEffort()` method
- On fetch, strips reasoning suffix from saved model ID and restores effort

**`models.js`** — Filters out `@reasoning-*` virtual variants from the model dropdown (1 line)

**`page-chat.js`** — Added:
- Reasoning combo HTML in toolbar (between model and node combos)
- `bindReasoningToggle()` in init, `unbindReasoningToggle()` in teardown
- `applySelectedModelToChatParams()` now uses `modelStore.effectiveModelId` instead of `S.selectedModelId`

**`sessions.js`** — `restoreSessionState()` now calls `restoreReasoningFromModelId()` to strip `@reasoning-*` suffix from stored model IDs and restore the toggle state

**Locale files** (en/fr/zh) — Added `reasoningTooltip`, `reasoningOff/Low/Medium/High` strings

### Zero backend changes
The feature leverages the existing `@reasoning-*` model ID suffix system — the backend already resolves these to the correct provider with reasoning effort applied.

> DEVELOPER

commit push and create a PR

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/750

> DEVELOPER

The thinking select could use a brain icon instead of the current sparkles. And thinking model could have a distinctive thing in the model listing, so we know thinking will be available.

> AGENT

Pushed. The PR at https://github.com/moltis-org/moltis/pull/750 now has 3 commits:

1. **feat(web): add reasoning effort toggle to chat toolbar** — the core feature
2. **feat(web): use brain icon for reasoning toggle and mark capable models** — brain icon + reasoning indicator in model list
3. **fix(web): match reasoning dropdown font size with model dropdown** — font size consistency fix

> DEVELOPER

The thinking select is very very wide with short text inside, any way to shrink its width a bit?

> AGENT

Pushed. The reasoning combo button now uses `width: auto` with `justify-content: flex-start` instead of stretching to `max-width: 220px`, so it'll shrink to fit its short label.

> DEVELOPER

still very wide.
[Image: image/png]

> DEVELOPER

[Image: source: /var/folders/0h/dmk6d6mj52s98cq24w9_n4d00000gn/T/TemporaryItems/NSIRD_screencaptureui_TKNA0z/Screenshot 2026-04-16 at 20.46.22.png]

> AGENT

Pushed. The dropdown now uses `width: auto; min-width: 100px` instead of the hardcoded `280px`, so it'll size to fit "Off/Low/Medium/High" snugly.

> DEVELOPER

nothing changed
[Image: image/png]

> DEVELOPER

[Image: source: /var/folders/0h/dmk6d6mj52s98cq24w9_n4d00000gn/T/TemporaryItems/NSIRD_screencaptureui_LMsrSb/Screenshot 2026-04-16 at 20.47.58.png]

> AGENT

The fix is now in `layout.css` too (the file that's actually loaded in dev mode). The dropdown should now shrink to fit "Off/Low/Medium/High" instead of being 280px wide.

> DEVELOPER

commit and push

> AGENT

Clean working tree, all 5 commits pushed and up to date with `origin/literate-coral`.

> DEVELOPER

Fix and solve PR comments

> AGENT

All 4 PR comments fixed and pushed:

1. **P1 — Stale reasoning effort**: `restoreReasoningFromModelId` now calls `setReasoningEffort(parsed.effort)` unconditionally, so switching to a session without `@reasoning-*` clears the previous effort
2. **P2 — i18n not wired**: Imported `t` from `i18n.js`, replaced hardcoded labels with `t("chat:reasoningOff")` etc.
3. **P2 — French untranslated**: Changed to Désactivé/Faible/Moyen/Élevé
4. **P2 — Duplicated constant**: Exported `REASONING_SEP` from `model-store.js`, imported in `models.js`
