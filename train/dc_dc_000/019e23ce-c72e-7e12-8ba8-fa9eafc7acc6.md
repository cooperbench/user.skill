> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

Review the implementation against the success criteria.

        Project directory:
        /Users/user_c042661f/Documents/Veas

        Idea:
# Per-bot partner sharing — design brief

## Context

The Veas codebase runs N bots that each occupy a "domain" for a user (currently: `mediator` = relationship coach for a dyad on topic=relationship; `tante_rosi` = solo pregnancy coach on topic=pregnancy; more bots planned). Today only the mediator's content can flow between dyad partners, gated by a **global** opt-in (`users.cross_thread_sharing_default`). The pregnancy coach writes everything private; her facts cannot reach the partner even when the user wants to share them.

We want to generalise partner-sharing so that **every bot** (current and future) can produce content that the user's partner sees, gated by a **per-bot** opt-in. The user gets one switch per domain ("share my pregnancy stuff with my partner — yes / no / not decided yet"). Until they decide, the bot keeps surfacing the question.

The basic infrastructure already exists for distillations (`visibility: private | dyad_shareable`, `shareable_summary`, `raw_message_visibility()` filtering in `app/services/cross_thread_privacy.py`, `app/services/hot_context.py:500-577`). The work below generalises it across both bots-and-content-types, and replaces the global toggle with a per-bot one.

## Goal (one sentence)

Replace the single global `users.cross_thread_sharing_default` with per-bot opt-in state on `user_bot_state`, extend `dyad_shareable` visibility to `memories` (today it only exists on `distillations`), and rewire the hot-context read path so a partner sees `dyad_shareable` content from any bot where the content's owner has opted in for *that* bot — with NULL ("not decided") triggering a prompt-slot the bot uses to ask.

## Decisions already made (do not re-litigate)

These are settled — the plan should implement them, not re-debate them.

1. **Per-bot opt-in lives on `user_bot_state`** as one new column `partner_share text` with values `'opt_in' | 'opt_out' | NULL`. NULL = "pending, must ask". Key is `(user_id, bot_id)` — same shape as every other per-bot state today.
2. **Memories get `visibility` and `shareable_summary`** mirroring distillations exactly. Default `visibility='private'`. When `visibility='dyad_shareable'`, `shareable_summary` is required.
3. **The opt-in is shown until decided.** While `partner_share IS NULL`, every render of that bot's hot context includes a "pending opt-in" slot in the system prompt asking the bot to raise the question this turn. As soon as the value is non-NULL (`opt_in` OR `opt_out`), the slot drops out and the bot stops raising it.
4. **One shared prompt slot, used by every bot.** Define one canonical pending-opt-in paragraph used by every bot's `render_system_prompt`. Rosi's existing `_FIRST_CONTACT_V1` collapses into it; the mediator's onboarding language for cross-thread sharing also collapses into it. New bots inherit the slot for free — no per-bot prompt work.
5. **One shared tool: `set_partner_sharing(opt_in: bool)`.** Implicit `bot_id` (from the calling bot's scope). Writes to `user_bot_state.partner_share` for the calling (user, bot) pair.
6. **Migration: the existing global flag goes away.** Backfill `user_bot_state[bot_id='mediator', user_id=X].partner_share` from `users.cross_thread_sharing_default` for every existing user, then drop `users.cross_thread_sharing_default`. One model, not two — no fallback path, no two-system-running period.
7. **No per-row UX in v1.** The user gets the per-bot toggle. The bot decides per-call whether a given memory/distillation should be `private` vs `dyad_shareable` based on the content. No user-facing per-row controls.
8. **Hot context cross-bot pull is in scope.** When rendering for user B (the partner of A), pull A's `dyad_shareable` rows from *any* bot where `partner_share[A, that_bot] = 'opt_in'`, surfaced with a provenance prefix (e.g. `from Rosi:`). Same-bot dyad sharing (the existing mediator behaviour) keeps working unchanged in shape, just driven by the new column.

## Files known to be relevant (planner should read at least these)

The planner should still survey the repo, but these are the focal points:

- `migrations/0012_cross_thread_sharing.sql` — defines the global flag being retired.
- `migrations/0015_distillations.sql` — defines `visibility` + `shareable_summary` we're mirroring onto memories.
- `migrations/0022_topic_status_user_bot_state.sql` — defines `user_bot_state` (current schema: `user_id, bot_id, onboarding_state, paused`).
- The next available migration number is `0020` (or whatever is highest after `0019_feedback_reaction_context.sql`); planner should verify.
- `app/services/cross_thread_privacy.py` — `raw_message_visibility()` lives here; needs to flip from global flag to per-bot lookup.
- `app/services/hot_context.py` (especially lines 500-577) — read path; needs (a) per-bot lookup, (b) cross-bot pull for partner, (c) emitting the `partner_sharing_state: 'pending'` signal.
- `app/services/tools/write_tools.py` — `add_memory` (~line 776) and `add_distillation` (~line 1165). The `add_memory` write helper needs to accept `visibility` + `shareable_summary`.
- `app/services/tools/tool_schemas.py` — `AddMemoryInput` needs new fields mirroring `AddDistillationInput.visibility` etc. (~line 996 for the distillation schema as the template).
- `app/bots/mediator.py` and `app/bots/tante_rosi.py` — both need to (a) include the canonical pending-opt-in slot via their `render_system_prompt`, (b) be eligible to call `set_partner_sharing`. Rosi additionally needs prompt language about *when* to write `dyad_shareable` rows once opted in.
- `app/bots/prompts/tante_rosi.py` (`_FIRST_CONTACT_V1`) and the equivalent mediator prompt file — the canonical slot replaces/absorbs whatever a[REDACTED_SK] language already exists in each.
- `app/bots/` tool dispatch — wherever bot tool allowlists are wired, `set_partner_sharing` must be available to every bot (it's user-state-modifying, like `set_pregnancy_edd`, not domain-specific).

## Invariants to enforce (must hold)

1. **NULL → silent.** When `partner_share IS NULL`, *no* content from that (user, bot) is shared with the partner regardless of per-row `visibility`. The toggle is the gate; per-row visibility only matters when the toggle is `opt_in`.
2. **opt_out → silent.** Same as NULL for the read path. The only difference is the prompt slot doesn't surface.
3. **opt_in → per-row decides.** When the toggle is `opt_in`, dyad_shareable rows from that bot flow to the partner; private rows don't.
4. **No partner → moot.** When the user has no partner (`users.partner_user_id IS NULL`), the prompt slot is suppressed even with `partner_share IS NULL`. Nothing to share to. Don't ask a question that has no answer.
5. **No backsliding on the mediator.** Every existing mediator user must continue to see exactly what they see today — the migration must be observationally equivalent. A user whose current `cross_thread_sharing_default = 'opt_in'` ends up with `user_bot_state[mediator].partner_share = 'opt_in'`; a user with `'opt_out'` ends up `'opt_out'`; NULL stays NULL.
6. **Cross-bot pull is opt-in-gated, not opt-out-gated.** Default is "don't show partner's other-bot content." Only `'opt_in'` from the content owner unlocks the pull. This matters: a partner who hasn't decided cannot accidentally have their content surfaced because of someone *else's* default.
7. **Tool authorisation.** `set_partner_sharing` writes only to the calling user's row for the calling bot. A user calling Rosi cannot toggle their mediator state; Rosi cannot toggle Véas's state. Scope is `(message.sender_id, message.bot_id)`.
8. **The shareable_summary contract.** When `add_memory` or `add_distillation` is called with `visibility='dyad_shareable'`, `shareable_summary` must be non-null and non-empty. Reject the call otherwise. Same rule that already applies to distillations should now apply to memories.

## Edge cases and ordering concerns

The planner should treat these as real, not paranoid:

- **Migration backfill ordering.** The new column on `user_bot_state` must be added and backfilled before `cross_thread_sharing_default` is dropped. The hot-context read path must be flipped to the new column *atomically* with the drop, or the system briefly reads from a dropped column. Plan the migration as a single transaction or with explicit phasing.
- **Backfill for users without a `user_bot_state[mediator]` row.** Some legacy users may not have a `user_bot_state` row for the mediator yet (it may be created lazily on first message). The migration must create rows for any user with a non-NULL `cross_thread_sharing_default`. For users with NULL global setting, decide: either create rows pre-set to NULL (explicit pending state) or skip (lazy creation later, still NULL). Either is defensible — make a call and write it down.
- **The pending slot wording is shared.** Different bots have different voices. The shared slot must be voice-agnostic — short, neutral, instructive to the model, not user-facing copy. The bot's own voice handles the actual question to the user; the slot just tells the bot "raise this naturally this turn."
- **Cross-bot pull volume.** A partner with several opted-in bots could see a long list of "from X:" rows in their hot context. Budget for hot-context length: cap, summarise, or rank. Don't ship a context bomb.
- **Order of cross-bot content.** When pulling rows from multiple bots, by what order? By recency? By bot? Pick one and write it down so the reviewer can check it.
- **Provenance prefix format.** "from Rosi:" / "from Véas:" — bake into a single helper, not sprinkled. Bots are named via the bot registry; use the registry's display name, not a hard-coded string.

## Explicitly out of scope

- Per-row visibility controls exposed to the user. (The bot decides per-row; users only decide per-bot.)
- Re-asking after some time has passed. Once `opt_in` or `opt_out` is set, the slot stays gone. Future work, not this sprint.
- New bot registration code. The pattern must work for new bots when they show up, but we are not adding a new bot in this sprint.
- Per-topic granularity within a bot. Each bot is one domain; one toggle per bot is enough.
- UI surfaces. There is no UI today and we are not building one.
- Encryption-at-rest changes. `shareable_summary` on memories follows whatever the existing memory content encryption pattern is.

## Success criteria

Reviewer should check, in priority order:

**must**
- Migration adds `user_bot_state.partner_share` and backfills it from `users.cross_thread_sharing_default` for every user where the global flag was non-NULL, preserving the same value semantically (`'opt_in' → 'opt_in'`, `'opt_out' → 'opt_out'`).
- Migration adds `memories.visibility` (default `'private'`) and `memories.shareable_summary` (nullable) with a CHECK constraint matching the existing distillations one (`shareable_summary` required iff `visibility='dyad_shareable'`).
- Migration drops `users.cross_thread_sharing_default` only after the read path is updated.
- `cross_thread_privacy.raw_message_visibility()` (and any other reader of the old column) reads from `user_bot_state.partner_share` for the relevant bot, not from `users.cross_thread_sharing_default`.
- `hot_context.py` cross-bot pull lands: when rendering for partner B, B sees A's `dyad_shareable` memories and distillations from any bot where `partner_share[A, that_bot]='opt_in'`, with a provenance prefix from the bot registry.
- `hot_context.py` emits `partner_sharing_state: 'pending'` when `partner_share IS NULL` and the user has a partner; the canonical prompt slot is rendered into the system prompt of any bot whose hot context carries this signal.
- `set_partner_sharing` tool exists, is wired into the tool registry for every bot, and updates `user_bot_state.partner_share` for the calling `(user, bot)` only.
- `add_memory` accepts `visibility` and `shareable_summary`; rejects `dyad_shareable` without `shareable_summary`.
- Rosi's prompt is updated so that when `partner_share='opt_in'`, she writes `dyad_shareable` memories and distillations for non-sensitive facts (with appropriate `shareable_summary`).
- Mediator's existing partner-sharing onboarding language is collapsed into the canonical slot; mediator continues to behave observationally as today for existing users post-migration.
- Tests cover: NULL → no partner content visible; `opt_out` → no partner content visible; `opt_in` + `private` row → no partner content visible; `opt_in` + `dyad_shareable` row → partner content visible with provenance; cross-bot pull respects toggle independently per bot; user with no partner never sees the pending slot.

**should**
- Cross-bot content ordering and length budget are explicit (chosen rule, written down in code or comment).
- Migration is a single transaction or has explicit phasing documented.
- The canonical prompt slot is defined in one place and imported by both bot prompt files.

**info**
- Future work for re-asking or per-topic granularity is captured (e.g., as a ticket via `megaplan ticket new`) but not implemented.

## Notes for the planner

- **Do not invent new bot-ID strings.** Use the existing `bot_id` constants from `app/bots/ids.py`.
- **Do not gate behaviour on bot identity if it can be data-driven.** The whole point is N bots; if Rosi gets a code path that Véas doesn't, that's a smell. The only legitimate per-bot differences are prompt content and topic, both of which are already data-driven.
- **The pending slot's prompt language matters.** Write it once, write it well, and stop. Bots are instructed *what* to do (raise the question this turn), not *how* to phrase it — voice belongs to each bot.
- **The migration is the riskiest piece.** Get the ordering and the backfill right and the rest is mechanical.

        Approved plan:
        # Implementation Plan: Per-Bot Partner Sharing

## Overview
The remaining critique still does not change the root cause or target architecture: the feature is still a per-bot `user_bot_state.partner_share` gate plus `dyad_shareable` memory/distillation summaries. The new issue is a supporting database prerequisite, not a different approach: `user_bot_state.bot_id` has a foreign key to `bots(id)`, so any bot that can call `set_partner_sharing` must already have a `bots` row. Tante Rosi is explicitly in scope and currently can be registered from code under staging, but the migration set does not seed `bots(id='tante_rosi')`. The implementation must guarantee that row before Rosi can write partner-share state.

The repo shape that matters:

- Migrations currently run through `migrations/0034_weekly_reflection.sql`, so the next migration is `migrations/0035_per_bot_partner_sharing.sql`.
- `user_bot_state` is defined in `migrations/0022_topic_status_user_bot_state.sql` with primary key `(user_id, bot_id)` and `bot_id text NOT NULL REFERENCES bots(id)`.
- `migrations/0020_topics_bots_bindings.sql` seeds `mediator`; `migrations/0031_coach_staging_seed.sql` seeds staging-only `coach`; no migration currently seeds `tante_rosi`.
- Distillations already have `visibility`, `shareable_summary`, and encrypted summary fields in `migrations/0015_distillations.sql` and root `tool_schemas.py`; memories need the same shape.
- Message rows have `bot_id` and `topic_id`; raw-message readers must filter by those fields before applying per-bot partner sharing.
- The schema file is root `tool_schemas.py`, not `app/services/tools/tool_schemas.py`.
- Partner resolution uses `dyads`/`dyad_members`, not `users.partner_user_id`.
- The old users-column readers are broader than the obvious path: update `app/models/user.py`, `app/services/turn_context.py`, `app/staging.py`, `app/bots/base.py`, `app/services/hot_context.py`, `app/services/tools/read_tools.py`, `app/services/tools/write_tools.py`, `app/services/tools/registry.py`, `app/services/tools/scope_guard.py`, prompts, and tests/fixtures.

## Phase 1: Schema, Constants, And Shared Helpers

### Step 1: Add bot id constants (`app/bots/ids.py`, bot specs)
**Scope:** Small
1. Add `TANTE_ROSI_BOT_ID = 'tante_rosi'` in `app/bots/ids.py` and replace literal uses in `app/bots/tante_rosi.py`, tests, and new Python references.
2. Keep `MEDIATOR_BOT_ID` as the source for mediator references in Python code.
3. Do not invent ids for new bots; existing `coach` can keep its current id source if no constant exists, but partner-sharing logic must use `ctx.bot_id` and registry data rather than bot identity checks.

### Step 2: Add migration `migrations/0035_per_bot_partner_sharing.sql`
**Scope:** Medium
1. Wrap the migration in one `BEGIN`/`COMMIT` transaction.
2. Ensure the in-scope bot rows exist before any `user_bot_state` write can reference them:
   - Insert `bots(id, display_name)` row `('tante_rosi', 'Tante Rosi')` with `ON CONFLICT (id) DO UPDATE SET display_name = EXCLUDED.display_name` or `DO NOTHING` if preserving existing DB display names is preferred locally.
   - Do not add broad new bot-registration machinery; this is a narrow FK prerequisite for the existing in-scope Rosi bot.
3. Add `user_bot_state.partner_share text` plus a CHECK constraint allowing only NULL, `opt_in`, or `opt_out`.
4. Backfill mediator rows before dropping the old column:
   - Insert/update `(users.id, 'mediator')` rows for users where `cross_thread_sharing_default IS NOT NULL`.
   - Preserve values exactly: `opt_in -> opt_in`, `opt_out -> opt_out`.
   - Do not create rows for legacy NULL values; missing row and NULL both mean pending.
5. Add memory sharing fields mirroring distillations:
   - `memories.visibility text NOT NULL DEFAULT 'private'` with CHECK in `('private', 'dyad_shareable')`.
   - `memories.shareable_summary text`.
   - `memories.shareable_summary_encrypted bytea`.
   - CHECK requiring non-empty `shareable_summary` when `visibility='dyad_shareable'`.
6. Add indexes for the new read paths:
   - `user_bot_state(user_id, bot_id, partner_share)` for direct state lookups.
   - `user_bot_state(partner_share, user_id, bot_id)` if the cross-bot pull query starts from opted-in rows.
   - A memories visibility/status recency index supporting `dyad_shareable` pulls.
7. Drop `users_cross_thread_sharing_default_check` and then drop `users.cross_thread_sharing_default` at the end of the transaction.

### Step 3: Add shared partner-sharing service (`app/services/partner_sharing.py`)
**Scope:** Medium
1. Create one service module for partner-share state and provenance helpers so hot context, read tools, write tools, and prompt wiring use the same definitions.
2. Define `PartnerShare = Literal['unset', 'opt_in', 'opt_out']` and `normalize_partner_share(value)` with old normalizer behavior: NULL/empty/unknown -> `unset`.
3. Add `fetch_partner_share(pool, user_id, bot_id)` and `fetch_partner_shares(pool, pairs)` for batch loading `user_bot_state.partner_share`.
4. Add `upsert_partner_share(pool, user_id, bot_id, partner_share)` for the tool path.
5. In `upsert_partner_share`, rely on the `bots` FK rather than silently creating arbitrary bot ids; the migration must seed Tante Rosi and tests must prove Rosi upserts work.
6. Add `resolve_dyad_partner(pool, user_id)` using `dyad_members`; return `None` when there is no exactly resolvable partner.
7. Add `bot_display_name(pool, bot_id)` and `format_partner_share_provenance(bot_id, text)` using `app.bots.registry.get_bot_spec(bot_id).display_name` when available, falling back to the `bots` table and then `bot_id`.
8. Keep `app/services/cross_thread_privacy.py` focused on pure visibility decisions; import the normalizer from the new service or re-export a compatibility alias only during the code transition.

## Phase 2: Remove The Global User Field Everywhere

### Step 4: Update user and turn context models (`app/models/user.py`, `app/services/turn_context.py`, `app/staging.py`)
**Scope:** Medium
1. Remove `cross_thread_sharing_default` from `User` and from `_row_to_user`, `fetch_user_by_id`, `upsert_user`, and reconstruction calls.
2. Update `app/services/turn_context.py::partner_of` to stop selecting the dropped column.
3. Update `app/staging.py` to fetch per-bot partner-share state for prompt rendering instead of reading `user.cross_thread_sharing_default` and `partner.cross_thread_sharing_default`.
4. Update tests that construct `User(...)` so they no longer pass `cross_thread_sharing_default`.

### Step 5: Replace old tool and registry references (`app/services/tools/write_tools.py`, `app/services/tools/registry.py`, `app/services/tools/scope_guard.py`, root `tool_schemas.py`)
**Scope:** Medium
1. In root `tool_schemas.py`, remove or deprecate `UpdateCrossThreadSharingDefaultInput/Output` and add `SetPartnerSharingInput(opt_in: bool, reason: str | None = None)` plus output fields `user_id`, `bot_id`, `partner_share`, and `updated_at`.
2. Implement `set_partner_sharing(ctx, args)` in `app/services/tools/write_tools.py` as an upsert into `user_bot_state` for exactly `(ctx.user.id, ctx.bot_id)`.
3. Do not expose `user_id` or `bot_id` as input fields; authorization is by construction.
4. Replace `update_cross_thread_sharing_default` in `TOOL_DESCRIPTIONS`, `TOOL_DISPATCH`, `WRITE_PHASE_TOOLS`, `RECORD_WRITE_TOOLS`, and scope guard constants with `set_partner_sharing`.
5. Update audit/log reasoning strings to use `partner_share` terminology.
6. Ensure Tante Rosi and generic coach allowlists inherit `set_partner_sharing` unless explicitly excluded; do not add it to any bridge/escalation exclusion set.
7. Add a targeted test that calls `set_partner_sharing` with `ctx.bot_id=TANTE_ROSI_BOT_ID` against a migrated/fake DB where the `bots` row exists.

### Step 6: Run a named stale-reference sweep before deeper rewrites
**Scope:** Small
1. Use `rg "cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default" app tests tool_schemas.py`.
2. For production code, every result must be intentionally rewritten before the migration is considered safe.
3. Tests may retain old strings only when asserting old migration text or documenting removed legacy behavior; otherwise update them to `partner_share` terminology.

## Phase 3: Privacy Decisions And Raw Message Scope

### Step 7: Flip pure privacy decisions (`app/services/cross_thread_privacy.py`)
**Scope:** Medium
1. Rename decision parameters from `thread_owner_sharing_default` to `thread_owner_partner_share`.
2. Return `partner_share` in the decision object instead of `sharing_default`, or keep a temporary alias only if required by tests during refactor.
3. Change redaction strings from `sharing_default` to `partner_share`.
4. Preserve behavior: same owner sees own raw content; partner sees raw content only when the owner’s partner_share for that message’s bot is `opt_in`; NULL/`unset`/`opt_out` hide it.

### Step 8: Scope dyadic raw-message reads by bot/topic (`app/services/hot_context.py`, `app/services/tools/read_tools.py`)
**Scope:** Large
1. In `app/services/hot_context.py`, change recent and trigger message queries to filter same-bot/same-topic raw messages, using `messages.bot_id = current_bot_id` and the active `topic_id` where applicable.
2. Do not apply the current bot’s partner_share to messages from another bot. Cross-bot sharing must use shareable summaries from memories/distillations only.
3. If any legacy/null `messages.bot_id` rows can still exist in a local/test database, treat partner raw content from those rows as hidden; do not let NULL bot rows become visible through mediator opt-in.
4. In `app/services/tools/read_tools.py::search_messages`, apply the same bot/topic scope before raw content is returned or searched. A read tool in mediator should not search raw Rosi messages just because mediator partner_share is `opt_in`.
5. In `recent_activity`, group/filter activity by `messages.bot_id = ctx.bot_id` and load partner_share from `user_bot_state` for that bot, not from users.
6. In `get_distillations`, use per-source-user partner_share keyed by each distillation’s `recorded_by_bot_id`; a source user’s mediator opt-in must not expose a Rosi distillation, and vice versa.
7. Update any write-tool visibility checks around source/owner messages in `app/services/tools/write_tools.py` to load the owner’s partner_share for the source message’s `bot_id`, not from the user model.
8. Add tests with two bots and same users proving mediator `opt_in` does not expose raw Rosi messages through hot context, `search_messages`, or `recent_activity`.

## Phase 4: Hot Context Partner-Share Rows

### Step 9: Rewrite dyad hot context state (`app/services/hot_context.py`)
**Scope:** Large
1. Add `partner_share` and `partner_sharing_state` fields to `HotContext` for current user/current bot and partner/current bot.
2. Replace `_user_profile()` selection of `cross_thread_sharing_default` with user profile data plus separately loaded partner-share state.
3. Emit `partner_sharing_state='pending'` only when the current user has a resolved dyad partner and current bot partner_share is missing/NULL.
4. Render `partner_share` labels instead of `sharing_default` labels.
5. Remove the current hardcoded `## URGENT ACTION NEEDED` hot-context block; the canonical prompt slot handles pending asks.

### Step 10: Add cross-bot shareable-summary pull (`app/services/hot_context.py`)
**Scope:** Large
1. For viewer B, resolve partner A via `dyad_members`.
2. Query A’s opted-in bots from `user_bot_state WHERE user_id=A AND partner_share='opt_in'`.
3. Fetch A’s `dyad_shareable` memories from any opted-in bot where `memories.recorded_by_bot_id = opted_bot_id`, `about_user_id=A`, status active, and `shareable_summary` is non-empty.
4. Fetch A’s active `dyad_shareable` distillations from any opted-in bot where `distillations.recorded_by_bot_id = opted_bot_id`, `source_user_ids` includes A, and `shareable_summary` is non-empty.
5. Do not require current topic membership for this cross-bot pull; the bot id/domain is the opt-in boundary, and provenance tells the receiving bot where the summary came from.
6. Order all cross-bot shareable rows by recency across bots: memories by `COALESCE(last_referenced_at, created_at)`, distillations by `COALESCE(updated_at, created_at)`.
7. Apply a fixed global cap, e.g. 12 rows total after sorting, and document it in a helper comment/test.
8. Render a single section using the provenance helper, e.g. `from Tante Rosi: ...`, and never render raw `content` for cross-bot partner rows.

### Step 11: Extend solo hot context (`app/services/hot_context_solo.py`)
**Scope:** Medium
1. Resolve dyad partner existence through the shared helper even for solo bots; do not call dyadic `partner_of`.
2. Add current bot `partner_share` and `partner_sharing_state` to solo hot context.
3. Suppress pending state when no dyad partner exists.
4. Do not expose partner raw messages or partner memories to solo bots; partner existence is only used for asking whether this bot’s safe summaries may be shared.
5. Update solo hot-context rendering to show `partner_share` state so Rosi/coach know whether they may write `dyad_shareable` summaries.

## Phase 5: Prompt Slot For Every Bot

### Step 12: Add canonical slot once (`app/bots/prompts/partner_sharing.py`)
**Scope:** Medium
1. Define one neutral instruction paragraph for pending per-bot partner sharing.
2. The slot should say what to do, not how to phrase it: raise the choice naturally this turn unless crisis/time-critical, call `set_partner_sharing(opt_in=...)` in the record step after an explicit choice, and do not share this bot’s rows until opt-in.
3. Keep it domain-agnostic so mediator, Rosi, coach, and future bots can import it.

### Step 13: Wire the slot through generic prompt rendering (`app/bots/base.py`, `app/services/prompts.py`, `app/services/prompts_solo.py`, `app/bots/prompts/tante_rosi.py`, `app/bots/coach.py`, `app/bots/tante_rosi.py`)
**Scope:** Large
1. Update `BotSpec.render_system_prompt()` to accept or load current-bot `partner_share` and `partner_sharing_state`, rather than reading `User.cross_thread_sharing_default`.
2. Pass `partner_sharing_state`, `current_user_partner_share`, and `partner_partner_share` into all prompt renderers.
3. In mediator prompts (`app/services/prompts.py`), replace `CROSS_THREAD_UNSET_*` with the canonical slot and replace tool references with `set_partner_sharing`.
4. In generic solo prompts (`app/services/prompts_solo.py`), add the same slot placeholder so `coach` and future solo bots inherit the ask without bespoke prompt work.
5. In Rosi prompt (`app/bots/prompts/tante_rosi.py`), use the same slot and add only Rosi-specific guidance for what pregnancy facts are safe to write as `dyad_shareable` once opted in.
6. Update `app/bots/coach.py` and `app/bots/tante_rosi.py` wrapper signatures from old `sharing_default` parameter names to partner-share names.
7. Keep opt-in/opt-out behavior domain-driven: no hard-coded bot identity checks except prompt content living in that bot’s own prompt module.

## Phase 6: Memory And Distillation Writes

### Step 14: Extend memory tool schema and write path (root `tool_schemas.py`, `app/services/tools/write_tools.py`)
**Scope:** Medium
1. Add `visibility: DistillationVisibility = DistillationVisibility.private` and `shareable_summary: str | None = None` to `AddMemoryInput` in root `tool_schemas.py`.
2. Add a model validator requiring non-empty `shareable_summary` when memory visibility is `dyad_shareable`.
3. Update `add_memory()` to persist `visibility`, `shareable_summary`, and encrypted `shareable_summary_encrypted`.
4. Update `supersede_memory()` deliberately: either add the same fields and validator to superseded replacements, or document/test that superseded replacements always default to private in v1.
5. Update `add_memory` descriptions to tell models that `dyad_shareable` memories require safe summaries.

### Step 15: Keep distillation contract bot-scoped (`root tool_schemas.py`, `app/services/tools/write_tools.py`, `app/services/tools/read_tools.py`)
**Scope:** Medium
1. Keep the existing distillation validator requiring non-empty shareable summaries.
2. Ensure `add_distillation()` always writes `recorded_by_bot_id=ctx.bot_id`, because cross-bot sharing gates by that bot id.
3. Update read/render paths so owner-visible same-bot distillations can show full content, while partner-visible or cross-bot rows show only `shareable_summary`.
4. Add tests proving `partner_share` for the distillation’s recorded bot, not the viewer’s current bot alone, controls whether its shareable summary appears.

## Phase 7: Tests And Fixtures

### Step 16: Update fake pool and fixtures (`tests/conftest.py`, affected tests)
**Scope:** Large
1. Add fake-pool storage and query handling for `bots` rows, including `tante_rosi`, and for `user_bot_state.partner_share` selects/upserts.
2. Add fake message `bot_id` and `topic_id` handling where hot context/read tools depend on same-bot scoping.
3. Remove fake users-column handling for `cross_thread_sharing_default` except where reading old migration SQL text.
4. Update existing tests in `tests/test_tools.py`, `tests/test_hot_context.py`, `tests/test_hot_context_join_cutover.py`, `tests/test_hot_context_cross_topic.py`, `tests/test_eval_execution.py`, `tests/test_pregnancy_user_model.py`, `tests/test_pregnancy_hot_context.py`, prompt/persona tests, and staging tests to use partner-share state.

### Step 17: Add focused regression coverage
**Scope:** Large
1. Migration tests or SQL assertions for:
   - `bots(id='tante_rosi')` exists after migration.
   - `user_bot_state.partner_share` exists and is constrained.
   - mediator non-NULL legacy backfill works.
   - memory sharing fields/constraints exist.
   - the old users column is dropped.
2. Privacy matrix tests:
   - missing/NULL partner_share blocks partner-visible rows.
   - `opt_out` blocks partner-visible rows.
   - `opt_in` plus private row blocks partner-visible rows.
   - `opt_in` plus `dyad_shareable` row exposes only `shareable_summary` with provenance.
3. Cross-bot independence tests:
   - A’s Rosi `opt_in` exposes Rosi summaries to partner, but A’s mediator `opt_out` blocks mediator rows.
   - A’s mediator `opt_in` does not expose raw or summary Rosi content unless A’s Rosi state is also `opt_in`.
4. Raw-message leak tests:
   - hot context, `search_messages`, and `recent_activity` filter messages by `bot_id`/topic before partner-share visibility.
   - mediator opt-in cannot expose Rosi raw messages.
5. Prompt-slot tests:
   - mediator, Rosi, and generic coach/solo prompt path render the canonical slot when pending and partner exists.
   - no partner suppresses the slot.
   - `opt_in` and `opt_out` suppress the slot.
6. Tool tests:
   - `set_partner_sharing` writes only `(ctx.user.id, ctx.bot_id)`.
   - `set_partner_sharing` succeeds for `ctx.bot_id=TANTE_ROSI_BOT_ID` because the bot row exists.
   - Rosi and coach can call `set_partner_sharing` if their allowlist otherwise permits record writes.
   - `add_memory(visibility='dyad_shareable')` rejects missing/blank `shareable_summary`.

## Execution Order
1. Add constants and the `0035` migration first so all code has stable names, target schema, and the Tante Rosi FK prerequisite.
2. Add shared partner-sharing helpers, then update fake-pool support for `bots` rows and `user_bot_state.partner_share`.
3. Remove the global users field from models, `partner_of`, staging, registry/tool code, and prompt signatures before relying on the migration that drops it.
4. Fix raw-message bot/topic scoping before enabling cross-bot shareable-summary pulls.
5. Add hot-context partner-share state and cross-bot summary rendering.
6. Wire the canonical slot through mediator, generic solo, coach, and Rosi prompt paths.
7. Extend memory writes and update distillation rendering.
8. Finish with focused regressions and a production-code stale-reference sweep.

## Validation Order
1. Run `rg "cross_thread_sharing_default|update_cross_thread_sharing_default" app tool_schemas.py` and require no production hits.
2. Run `rg "current_user_sharing_default|partner_sharing_default|sharing_default" app tool_schemas.py` and inspect remaining hits; only intentional compatibility aliases or test-only strings should remain.
3. Inspect `migrations/0035_per_bot_partner_sharing.sql` and verify it seeds `tante_rosi` before any Rosi `user_bot_state` upsert can occur.
4. Run schema/tool tests: `pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q`.
5. Run hot-context and read-tool tests: `pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_hot_context_cross_topic.py tests/test_pregnancy_hot_context.py -q`.
6. Run bot prompt/allowlist tests: `pytest tests/test_pregnancy_persona.py tests/test_pregnancy_allowlist.py tests/test_coach_e2e.py -q`.
7. Run the full suite with `pytest` after focused tests pass.

## Ticket Note
The open ticket `01KRF0BR8TSKVKSY3HG4WVTKDE` concerns embedding-triggered hot-context artifact retrieval. This plan changes hot-context sharing gates and summary rendering only; it should not be linked as resolved.


        Execution tracking state (`finalize.json`):
        {
  "tasks": [
    {
      "id": "T1",
      "description": "Add bot id constants and schema migration foundation: add `TANTE_ROSI_BOT_ID` in `app/bots/ids.py`, replace Python literals where touched, and create `migrations/0035_per_bot_partner_sharing.sql` as a single transaction that seeds `bots(id='tante_rosi')`, adds `user_bot_state.partner_share`, backfills non-NULL mediator values from `users.cross_thread_sharing_default`, adds memory `visibility`/`shareable_summary`/encrypted summary fields with CHECK constraints and indexes, then drops the old users column at the end.",
      "depends_on": [],
      "status": "done",
      "kind": "code",
      "executor_notes": "Added TANTE_ROSI_BOT_ID and used it in the Tante Rosi spec/registry paths touched by this batch. Added migrations/0035_per_bot_partner_sharing.sql with one BEGIN/COMMIT transaction: seeds bots(id='tante_rosi'), adds constrained user_bot_state.partner_share, backfills non-NULL mediator values from users.cross_thread_sharing_default via INSERT ... ON CONFLICT DO UPDATE, adds memory visibility/shareable_summary/shareable_summary_encrypted with checks and indexes, and drops the legacy users column at the end. Verified Python compile and focused tests passed. Full pytest was run and still has unrelated existing-looking failures in tests/test_agentic.py and tests/test_decay.py.",
      "files_changed": [
        "app/bots/ids.py",
        "app/bots/registry.py",
        "app/bots/tante_rosi.py",
        "migrations/0035_per_bot_partner_sharing.sql"
      ],
      "commands_run": [
        "python -m py_compile app/bots/ids.py app/bots/tante_rosi.py app/bots/registry.py",
        "pytest tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "pytest tests/test_agentic.py -q",
        "pytest tests/test_decay.py -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T2",
      "description": "Create shared partner-sharing helpers in `app/services/partner_sharing.py`: normalize partner share values, fetch single/batch states from `user_bot_state`, upsert scoped `(user_id, bot_id)` state, resolve dyad partner via `dyads`/`dyad_members`, and format provenance using bot registry display names with DB/id fallback.",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Created app/services/partner_sharing.py with strict partner_share normalization, single and batch fetches keyed by (user_id, bot_id), scoped upsert for one (user_id, bot_id), dyad partner lookup through dyads/dyad_members, and provenance formatting that uses registry display names with bots-table and bot-id fallback. Added focused helper tests covering normalization, missing-row pending behavior, scoped upsert, dyad lookup, and provenance fallback. Focused tests passed. Full pytest was rerun and still fails only in the same prior unrelated-looking tests/test_agentic.py and tests/test_decay.py failures from batch 1.",
      "files_changed": [
        "app/services/partner_sharing.py",
        "tests/test_partner_sharing.py"
      ],
      "commands_run": [
        "python -m black app/services/partner_sharing.py tests/test_partner_sharing.py",
        "python -m py_compile app/services/partner_sharing.py",
        "pytest tests/test_partner_sharing.py -q",
        "pytest tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_partner_sharing.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T3",
      "description": "Remove the global sharing field from user and turn/staging context: update `app/models/user.py`, `app/services/turn_context.py::partner_of`, and `app/staging.py` so they no longer select, hydrate, pass, or depend on `cross_thread_sharing_default`; load per-bot partner-share state where prompt rendering needs it.",
      "depends_on": [
        "T2"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Removed production DB selection/hydration/use of users.cross_thread_sharing_default from User, partner_of, staging, and prompt rendering paths. Added per-bot partner-share loading for prompt rendering in agentic and staging via app.services.partner_sharing.get_partner_share, while keeping a temporary non-hydrated User compatibility shim for old callers until the later stale-reference cleanup batch. Updated FakePool for the new user SELECT shape and partner_share lookup. Verified focused user/partner-sharing/pregnancy/schema tests, hot-context/tools tests, and agentic/staging modules; full pytest was rerun and still only shows the same prior unrelated-looking tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/models/user.py",
        "app/services/turn_context.py",
        "app/staging.py",
        "app/bots/base.py",
        "app/services/agentic.py",
        "tests/conftest.py"
      ],
      "commands_run": [
        "python -m black app/models/user.py app/services/turn_context.py app/bots/base.py app/services/agentic.py app/staging.py tests/conftest.py",
        "python -m py_compile app/models/user.py app/services/turn_context.py app/bots/base.py app/services/agentic.py app/staging.py",
        "pytest tests/test_pregnancy_user_model.py tests/test_partner_sharing.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest tests/test_agentic.py tests/test_agentic_lifecycle.py tests/test_staging.py -q",
        "pytest tests/test_hot_context.py tests/test_tools.py -q",
        "pytest -q",
        "rg -n \"SELECT[^\\n]*cross_thread_sharing_default|cross_thread_sharing_default=row|cross_thread_sharing_default=user|user\\.cross_thread_sharing_default|partner\\.cross_thread_sharing_default\" app/models/user.py app/services/turn_context.py app/staging.py app/bots/base.py app/services/agentic.py"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T4",
      "description": "Replace the legacy sharing tool with `set_partner_sharing`: update root `tool_schemas.py`, `app/services/tools/write_tools.py`, `app/services/tools/registry.py`, and `app/services/tools/scope_guard.py`; remove/deprecate `update_cross_thread_sharing_default`; ensure the new tool accepts only `opt_in: bool` plus optional reason and writes only `(ctx.user.id, ctx.bot_id)` via the shared helper.",
      "depends_on": [
        "T2",
        "T3"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Replaced the legacy sharing-state write surface with set_partner_sharing in the root schema/registry/scope guard/write tool path. The new schema accepts only opt_in plus optional reason and forbids user_id/bot_id overrides; write_tools.set_partner_sharing writes via app.services.partner_sharing.set_partner_share for ctx.user.id and ctx.bot_id only and rejects missing bot scope. Updated bridge candidate readiness and media explain visibility within write_tools to consult per-bot partner_share instead of the dropped users.cross_thread_sharing_default. Confirmed mediator default registry, Rosi/coach allowlists, and generic record/write steps include set_partner_sharing; grep found no update_cross_thread_sharing_default or old users sharing-column write/read references in the T4 production files. Focused tests passed; full pytest still fails in the same prior unrelated tests/test_agentic.py and tests/test_decay.py failures noted by earlier batches.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/registry.py",
        "app/services/tools/scope_guard.py",
        "tests/test_tools.py",
        "tests/conftest.py"
      ],
      "commands_run": [
        "python -m black app/services/tools/write_tools.py tests/test_tools.py tests/conftest.py",
        "python -m py_compile tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py tests/conftest.py tests/test_tools.py",
        "rg -n \"update_cross_thread_sharing_default|UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|ctx\\.(user|partner)\\.cross_thread_sharing_default|UpdateCrossThreadSharingDefault\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_tools.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T5",
      "description": "Run and act on a stale-reference sweep before deeper rewrites: use `rg \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py`; rewrite production hits to per-bot `partner_share` terminology or document intentional historical/test-only references.",
      "depends_on": [
        "T3",
        "T4"
      ],
      "status": "done",
      "kind": "audit",
      "executor_notes": "Ran the stale-reference sweep across app, tests, and tool_schemas.py. Removed production reads of users.cross_thread_sharing_default from hot_context.py and read_tools.py by loading per-bot user_bot_state.partner_share through app.services.partner_sharing, updated raw privacy terminology from sharing_default to partner_share, and replaced stale mediator prompt references to update_cross_thread_sharing_default with set_partner_sharing/partner_share language. The production sweep now has no old tool references and no dropped-column DB dependence; the only app hit is the explicitly temporary non-hydrated User.cross_thread_sharing_default compatibility shim from T3. Remaining sweep hits are tests/fixtures that intentionally preserve legacy inputs until the T13 test-infrastructure cleanup. Full pytest still fails only in the same previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/staging.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py",
        "python -m py_compile app/services/cross_thread_privacy.py app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_pregnancy_persona.py tests/test_eval_execution.py tests/test_coach_e2e.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T6",
      "description": "Flip raw privacy decisions to partner-share terminology in `app/services/cross_thread_privacy.py`: decision inputs/results should use owner `partner_share` for the relevant message bot, with NULL/unset and `opt_out` blocking partner-visible raw content and own-owner reads unchanged.",
      "depends_on": [
        "T2",
        "T5"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Completed the raw privacy terminology flip in app/services/cross_thread_privacy.py. RawMessageVisibility now reports partner_share instead of sharing_default, helper inputs use thread_owner_partner_share, redaction/omission strings refer to partner_share, and reason codes explicitly describe thread_owner_partner_share opt-in vs not-opted-in. Owner reads remain visible; partner reads are visible only for opt_in, while NULL/unset and opt_out block raw content. Focused modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m py_compile app/services/cross_thread_privacy.py tests/test_tools.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_6.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T7",
      "description": "Scope raw-message reads by bot/topic in `app/services/hot_context.py` and `app/services/tools/read_tools.py`: recent/trigger/search/recent_activity paths must filter to current bot and active topic before applying privacy; `get_distillations` and write-tool owner visibility checks must load partner-share keyed by each source row's `recorded_by_bot_id` or source message `bot_id`. Treat legacy NULL message bot IDs as hidden from partner raw reads.",
      "depends_on": [
        "T6"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Scoped raw-message reads to current bot/topic before privacy in hot_context and read_tools; keyed distillation visibility by recorded_by_bot_id with source-message bot fallback; scoped write-tool source-message visibility checks by bot/topic; and added regression coverage for mediator opt-in not exposing Rosi, legacy NULL, or other-topic raw messages. Focused modules passed. Full pytest was rerun and now fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "tests/conftest.py",
        "tests/test_agentic.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "python -m py_compile app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "python -m black tests/conftest.py tests/test_agentic.py",
        "python -m py_compile tests/test_agentic.py tests/conftest.py",
        "pytest tests/test_agentic.py tests/test_agentic_lifecycle.py tests/test_eval_execution.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_7.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T8",
      "description": "Rewrite dyadic hot context partner-share state and cross-bot summary rendering in `app/services/hot_context.py`: add current/partner `partner_share` and `partner_sharing_state`, emit pending only when current user has a resolved dyad partner and current bot state is missing/NULL, remove the hardcoded urgent sharing block, pull partner `dyad_shareable` memories/distillations from any opted-in bot, render only `shareable_summary` with shared provenance prefix, sort by recency across bots, and cap globally (for example 12 rows) with a code comment or test documenting the rule.",
      "depends_on": [
        "T2",
        "T7"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Dyadic hot context now carries current/partner partner_share and partner_sharing_state, removes the hardcoded urgent/soft-nudge sharing prompt text, gates partner dyad_shareable distillation summaries on the owner's per-bot opt_in, and prevents partner private memories from rendering as full memories. Added a recency-ordered, globally capped partner-shareable summary section for opted-in non-current-bot memories/distillations with shared provenance prefixes. Focused hot-context/tool/lint modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py tests/conftest.py tests/test_hot_context.py",
        "python -m py_compile app/services/hot_context.py tests/conftest.py tests/test_hot_context.py",
        "pytest tests/test_hot_context.py -q",
        "python -m black tests/test_hot_context_join_cutover.py",
        "python -m py_compile app/services/hot_context.py tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_tools.py -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest tests/test_lint_artifact_reads.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_tools.py tests/test_partner_sharing.py tests/test_tool_schemas_importable.py tests/test_lint_artifact_reads.py -q",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_8.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T9",
      "description": "Extend solo hot context in `app/services/hot_context_solo.py`: resolve dyad partner existence through the shared helper, add current-bot `partner_share` and `partner_sharing_state`, suppress pending when no partner exists, and keep solo bots from exposing partner raw messages or partner memories.",
      "depends_on": [
        "T2",
        "T8"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Solo hot context now loads current-bot partner_share, resolves dyad partner existence through the shared helper, emits partner_sharing_state='pending' only when a dyad partner exists and the current bot state is unset, and renders 'unavailable' when no partner exists. Regression coverage verifies pending/no-partner behavior and that solo context does not surface partner memories or raw messages. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context_solo.py",
        "tests/conftest.py",
        "tests/test_pregnancy_hot_context.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T10",
      "description": "Define one canonical pending partner-sharing prompt slot in `app/bots/prompts/partner_sharing.py`. Keep it domain-agnostic and model-facing: raise the choice naturally this turn unless crisis/time-critical, call `set_partner_sharing(opt_in=...)` in the record step after an explicit choice, and do not share this bot's rows until opt-in.",
      "depends_on": [
        "T4",
        "T8",
        "T9"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Defined the canonical pending partner-sharing prompt slot once in app/bots/prompts/partner_sharing.py. The slot is neutral and domain-agnostic, tells the model to raise the choice naturally unless crisis/time-critical, explicitly forbids sharing this bot's rows until explicit opt-in, and instructs set_partner_sharing(opt_in=true/false) in the record step after an explicit choice. Added focused prompt content coverage. py_compile and focused prompt/persona/schema modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/prompts/partner_sharing.py",
        "tests/test_partner_sharing_prompt.py"
      ],
      "commands_run": [
        "rg -n \"partner_share|partner_sharing|set_partner_sharing|FIRST_CONTACT|sharing\" app/bots app/services/prompts.py app/services/prompts_solo.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_agentic.py tests/test_coach_e2e.py",
        "sed -n '1,220p' app/bots/prompts/tante_rosi.py",
        "sed -n '1,120p' app/bots/prompts/__init__.py",
        "git status --short",
        "python -m py_compile app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "if [ -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json ]; then echo writable; else echo not_writable; fi",
        "rg -n \"PENDING_PARTNER_SHARING_PROMPT_SLOT|set_partner_sharing\\(opt_in\" app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T11",
      "description": "Wire the canonical prompt slot through every bot prompt path: update `app/bots/base.py`, `app/services/prompts.py`, `app/services/prompts_solo.py`, `app/bots/prompts/tante_rosi.py`, `app/bots/coach.py`, and `app/bots/tante_rosi.py` so mediator, Tante Rosi, coach, and future solo bots receive `partner_share`/`partner_sharing_state`; replace stale mediator onboarding language and tool references; add only Rosi-specific guidance for safe pregnancy `dyad_shareable` facts once opted in.",
      "depends_on": [
        "T10"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Wired current-bot partner_sharing_state from hot context through agentic/staging prompt construction and BotSpec.render_system_prompt into mediator, generic solo/coach, and Tante Rosi prompt renderers. Mediator and solo prompt paths now render the canonical pending slot only when partner_sharing_state='pending'; unavailable/no-partner states suppress it. Replaced the mediator unset prompt with the canonical slot and removed the opt-out re-ask/soft-nudge language. Tante Rosi now renders the canonical pending slot and adds Rosi-specific opt-in guidance for writing only non-sensitive pregnancy dyad_shareable memories/distillations with shareable_summary. Focused prompt, agentic/inbound, persona, schema, hot-context, partner-sharing, and pregnancy modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/services/agentic.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/staging.py",
        "tests/test_partner_sharing_prompt.py",
        "tests/test_eval_execution.py"
      ],
      "commands_run": [
        "python -m black app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "python -m py_compile app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/partner_sharing.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_agentic_lifecycle.py tests/test_inbound_source.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "rg -n \"update_cross_thread_sharing_default\" app/bots app/services/prompts.py app/services/prompts_solo.py || true",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_11.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T12",
      "description": "Extend memory and distillation write/read contracts: in root `tool_schemas.py`, add `visibility` and `shareable_summary` to `AddMemoryInput` with a validator requiring non-empty summaries for `dyad_shareable`; update `app/services/tools/write_tools.py` to persist and encrypt memory shareable summaries, keep superseded replacement behavior explicit, ensure `add_distillation()` writes `recorded_by_bot_id=ctx.bot_id`, and update read/render paths so partner/cross-bot rows expose only summaries.",
      "depends_on": [
        "T4",
        "T8"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "AddMemoryInput now accepts visibility/shareable_summary and rejects dyad_shareable memories without a non-empty shareable_summary. add_memory persists visibility, shareable_summary, encrypted summary, and recorded_by_bot_id. Memory read rows now carry visibility/shareable_summary, and get_memories/get_distillations gate partner-owned rows by the owner's per-bot partner_share and expose only shareable_summary for partner-visible artifacts. FakePool was updated for memory sharing fields and distillation recorded_by_bot_id. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/common.py",
        "tests/conftest.py",
        "tests/test_tool_schemas_importable.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T13",
      "description": "Update existing test infrastructure and regression tests in place. Extend fake pool/fixtures for `bots`, `user_bot_state.partner_share`, message `bot_id`/`topic_id`, and memory sharing fields; update affected existing tests to remove the old user column; add or extend regression coverage for migration SQL, privacy matrix, cross-bot independence, raw-message bot isolation, prompt-slot pending/no-partner behavior, `set_partner_sharing` scoped Rosi success, and `add_memory` shareable-summary validation.",
      "depends_on": [
        "T1",
        "T2",
        "T7",
        "T8",
        "T9",
        "T11",
        "T12"
      ],
      "status": "done",
      "kind": "test",
      "executor_notes": "Updated fake pool/test fixtures away from the dropped users.cross_thread_sharing_default DB paths in the affected partner-sharing modules; hot-context/read-tool tests now seed per-bot user_bot_state.partner_share directly for opt-in/opt-out cases. Added migration SQL regression coverage for transactional ordering, Tante Rosi seed, mediator non-NULL backfill before legacy-column drop, partner_share constraint, and memory visibility/shareable_summary constraints/indexes. Extended read-tool privacy assertions to cover NULL, opt_out, opt_in+private, and opt_in+dyad_shareable behavior. Verified focused partner-sharing/hot-context/tool/prompt/migration modules passed, adjacent fixture modules passed, and full pytest was run; full suite still fails only in the previously documented three tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "tests/conftest.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py",
        "tests/test_pregnancy_hot_context.py",
        "tests/test_pregnancy_tools.py",
        "tests/test_tools.py",
        "tests/test_partner_sharing_migration.py"
      ],
      "commands_run": [
        "rg -n \"partner_share|partner_sharing_state|dyad_shareable|shareable_summary|cross_thread_sharing_default|TANTE_ROSI|tante_rosi|raw-message|raw message|no partner|migration|0035\" tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_tools.py tests/test_tool_schemas_importable.py tests/test_partner_sharing.py tests/test_partner_sharing_prompt.py tests/conftest.py tests/test_pregnancy_persona.py tests/test_pregnancy_tools.py migrations/0035_per_bot_partner_sharing.sql",
        "python -m black tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py tests/test_partner_sharing_migration.py",
        "python -m py_compile tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py tests/test_partner_sharing_migration.py",
        "pytest tests/test_partner_sharing_migration.py tests/test_partner_sharing.py tests/test_partner_sharing_prompt.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py -q",
        "pytest -q",
        "rg -n \"UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|cross_thread_sharing_default\" tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py",
        "test -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_12.json && echo writable || echo not_writable"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T14",
      "description": "Final verification only: run the stale-reference sweeps and focused tests named by the approved plan, then the full relevant suite. Include commands such as `rg \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py`, `rg \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py`, `pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q`, hot-context/read-tool tests, prompt/allowlist tests, and finally `pytest` if focused tests pass. Also write a short throwaway script that reproduces the original leak/bug scenario (partner-share per bot: Rosi opt-in exposes only Rosi summaries while mediator opt-out blocks mediator rows and raw cross-bot messages), run it, record the result, and delete the script before finishing. Do not create new permanent test files in this final task; fix failures and rerun until passing or document a concrete blocker.",
      "depends_on": [
        "T13"
      ],
      "status": "done",
      "kind": "test",
      "executor_notes": "Final verification completed. Production stale-reference sweeps for cross_thread_sharing_default/update_cross_thread_sharing_default and sharing_default terminology across app and tool_schemas.py are clean after removing the last User compatibility shim and hot-context legacy fallback. The throwaway per-bot leak reproduction script passed: Rosi opt_in surfaced only the Rosi shareable summary with provenance, mediator opt_out blocked mediator shareable rows, and raw cross-bot/opt-out content did not render; the script was deleted afterward. Focused schema/tool, hot-context/read, prompt/allowlist, migration, partner-sharing, pregnancy, and adjacent fixture modules passed. Full pytest was rerun and still fails only in the previously documented three tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/models/user.py",
        "app/services/hot_context.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py",
        "tests/test_cross_topic_status_injection.py",
        "tests/test_cross_topic_peek_wired.py",
        "tests/test_messaging_non_agentic_bot_id.py",
        "tests/test_coach_e2e.py",
        "tests/test_hot_context_cross_topic.py",
        "tests/test_write_tools_solo_bot_guard.py",
        "tests/test_pregnancy_user_model.py",
        "tests/test_multi_topic_writes.py",
        "tests/test_per_bot_telemetry.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py",
        "rg -n \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py",
        "python tmp_partner_sharing_repro.py",
        "python -m py_compile app/models/user.py app/services/hot_context.py tests/test_cross_topic_status_injection.py tests/test_cross_topic_peek_wired.py tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_hot_context_cross_topic.py tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_user_model.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tmp_partner_sharing_repro.py",
        "python -m black app/models/user.py app/services/hot_context.py tests/test_cross_topic_status_injection.py tests/test_cross_topic_peek_wired.py tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_hot_context_cross_topic.py tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_user_model.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py",
        "test ! -e tmp_partner_sharing_repro.py && echo deleted",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "test -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_13.json && echo writable || echo not_writable"
      ],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    }
  ],
  "watch_items": [
    "Do not invoke the `megaplan` CLI, read the `megaplan` skill, or start nested planning; treat this as a direct execution brief.",
    "The migration is the highest-risk piece: seed `bots(id='tante_rosi')` before any Rosi `user_bot_state` write, backfill mediator non-NULL values before dropping the old users column, and keep the SQL transactional.",
    "Raw messages must remain same-bot/topic scoped. Cross-bot partner sharing is summaries only, never raw `content`.",
    "`partner_share IS NULL` and missing `user_bot_state` both mean pending for prompts but silent for read-path sharing; `opt_out` is silent and suppresses the prompt slot.",
    "Partner resolution uses `dyads`/`dyad_members`, not `users.partner_user_id`.",
    "Root `tool_schemas.py` is the schema target; there is no `app/services/tools/tool_schemas.py`.",
    "Use `recorded_by_bot_id` and source message `bot_id` as the gate key for artifacts. Do not gate Rosi artifacts with mediator partner-share or vice versa.",
    "The provenance prefix must come from a shared helper using bot registry display names with DB/id fallback, not scattered hard-coded strings.",
    "Cross-bot shareable rows need a fixed global cap and recency ordering documented in code or tests to avoid context bloat.",
    "Do not make unrelated debt items worse, especially staging hot-context divergence and existing bot/topic routing assumptions.",
    "Respect the write-access contract: attempt real edits and only report permission failure after an actual OS-level rejection and retry."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does migration `0035_per_bot_partner_sharing.sql` run in one transaction, seed `tante_rosi`, add constrained `partner_share`, backfill mediator non-NULL values exactly, add memory sharing fields/checks/indexes, and drop the old users column last?",
      "executor_note": "Yes. Migration 0035 is transactional, seeds tante_rosi, constrains partner_share, backfills non-NULL mediator sharing values exactly from the legacy user column before dropping it, adds constrained memory sharing fields plus encrypted summary storage and indexes, and drops users.cross_thread_sharing_default last.",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Do all shared helpers use `(user_id, bot_id)` without silently creating arbitrary bot IDs, resolve dyad partner through `dyads`/`dyad_members`, and produce provenance from registry display names with fallback?",
      "executor_note": "Yes. The helper APIs read/write only explicit (user_id, bot_id) keys and do not create bot rows; unknown bot IDs fall through to DB/id display fallback while FK constraints will guard writes. Partner resolution uses dyads/dyad_members, and provenance uses the bot registry display name first with bots.display_name and raw id fallbacks.",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Are `User`, `partner_of`, and staging paths free of `cross_thread_sharing_default` selects/hydration while still supplying prompt code with per-bot partner-share state where needed?",
      "executor_note": "Yes for the production paths in scope. User, partner_of, staging, base prompt rendering, and agentic prompt construction no longer select, hydrate, or pass users.cross_thread_sharing_default; prompt rendering now receives per-bot partner_share loaded by (user_id, bot_id). A temporary User compatibility property remains non-hydrated for legacy test/caller tolerance and is not a DB dependency.",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Is `set_partner_sharing` the only sharing-state write tool, with no user/bot input override and with allowlist/registry/scope guard wiring for mediator, Rosi, coach, and generic record/write steps?",
      "executor_note": "Yes. set_partner_sharing is the only sharing-state write tool in the T4 schema/registry/dispatch/scope files; its input forbids user_id or bot_id overrides, it writes only ctx.user.id plus ctx.bot_id through the shared partner_sharing helper, and registry/scope/allowlist checks show it is available to mediator, Tante Rosi, coach, and generic record/write paths.",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does the grep sweep show no production dependence on the dropped user field or old tool, and are remaining `sharing_default` strings intentional historical/test references or rewritten?",
      "executor_note": "Yes. The sweep shows no production dependence on the dropped users column or old update_cross_thread_sharing_default tool. The only remaining app hit is the T3 temporary non-hydrated User compatibility shim; remaining cross_thread_sharing_default/current_user_sharing_default/partner_sharing_default/sharing_default hits are test fixtures or legacy test call shapes scheduled for T13 cleanup.",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does `raw_message_visibility()` preserve owner-visible behavior while partner visibility depends only on the owner's `partner_share` for the message's bot, with NULL/unset and `opt_out` blocking?",
      "executor_note": "Yes. raw_message_visibility() keeps same-owner raw reads visible regardless of partner_share, and partner raw reads now depend only on the thread owner's partner_share value supplied for that message bot. NULL/unset and opt_out normalize to hidden with raw_partner_content_hidden_by_partner_share; only opt_in allows partner raw visibility.",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Can a mediator opt-in no longer expose Rosi raw messages through hot context, `search_messages`, or `recent_activity`, including when legacy messages have NULL `bot_id`?",
      "executor_note": "Yes. Mediator raw-read paths now require the current mediator bot_id and active topic before privacy, so Rosi messages, other-topic mediator messages, and explicit legacy NULL bot_id rows are excluded from hot context, search_messages, and recent_activity even when mediator partner_share is opt_in.",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does dyadic hot context emit pending only for current user/current bot with a partner, pull opted-in cross-bot summaries only, use provenance prefixes, enforce recency ordering, and cap total cross-bot rows?",
      "executor_note": "Yes. Dyadic hot context now exposes partner_sharing_state for current/partner users, removes the hardcoded prompt block, pulls only opted-in partner dyad_shareable summaries from non-current bots, renders them with shared provenance prefixes, orders candidates by recency, and caps rendered cross-bot summaries at 12 total.",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does solo hot context ask about partner sharing only when a dyad partner exists and avoid exposing partner raw/messages/memories to solo bots?",
      "executor_note": "Yes. Solo hot context resolves dyad partner existence through the shared helper, emits pending only for the current user/current bot when a dyad partner exists and partner_share is unset, suppresses pending as unavailable without a partner, and regression tests verify partner raw messages and partner memories are absent from solo context.",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Is the pending prompt slot defined once, neutral, domain-agnostic, and explicit about `set_partner_sharing` after an explicit choice?",
      "executor_note": "Yes. The pending slot is defined once in app/bots/prompts/partner_sharing.py, contains no Rosi/mediator/pregnancy/relationship-specific language, and explicitly covers crisis/time-critical deferral, no sharing before opt-in, and set_partner_sharing(opt_in=true/false) after an explicit choice.",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Do mediator, Tante Rosi, coach, and generic solo prompt paths all render the canonical slot from `partner_sharing_state` and avoid stale `update_cross_thread_sharing_default` language?",
      "executor_note": "Yes. Mediator, Tante Rosi, coach, and generic solo prompt render paths all receive partner_sharing_state and render the canonical pending slot only from that pending state; no prompt-path update_cross_thread_sharing_default references remain, and Rosi alone has opt-in guidance for safe pregnancy dyad_shareable summary writes.",
      "verdict": ""
    },
    {
      "id": "SC12",
      "task_id": "T12",
      "question": "Does `add_memory` reject blank/missing `shareable_summary` for `dyad_shareable`, persist/encrypt summaries, and do partner/cross-bot renders expose only `shareable_summary` while own same-bot reads retain full content as appropriate?",
      "executor_note": "Yes. add_memory rejects blank/missing shareable_summary for dyad_shareable, persists and encrypts memory summaries, records the calling bot id, and read paths now expose only shareable_summary for partner-visible memory/distillation rows while own rows retain full content.",
      "verdict": ""
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "question": "Do updated existing tests cover NULL, opt-out, opt-in+private, opt-in+dyad_shareable, independent per-bot gates, raw-message bot isolation, no-partner prompt suppression, Rosi FK success, and memory validation?",
      "executor_note": "Yes. Updated tests cover NULL and opt_out as silent, opt_in+private as hidden, opt_in+dyad_shareable as summary-only visible, independent per-bot gates through cross-bot Rosi/coach cases, raw-message bot isolation, no-partner prompt suppression, scoped Rosi set_partner_sharing success, memory validation, and migration SQL ordering/constraints.",
      "verdict": ""
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "question": "Do the final grep sweeps, focused pytest commands, full suite or documented subset, and deleted throwaway reproduction script demonstrate the feature works without stale production references?",
      "executor_note": "Yes. Final production sweeps have no stale sharing references, the focused pytest modules passed, the throwaway reproduction script passed and was deleted, and the full suite was rerun with only the known unrelated three tests/test_decay.py fake-pool observation UPDATE failures remaining.",
      "verdict": ""
    }
  ],
  "user_actions": [
    {
      "id": "U1",
      "description": "After the code is merged, apply the new database migration to the target staging/production database using the project's normal migration process, then deploy the matching application version atomically with that schema change.",
      "phase": "after_execute",
      "blocks_task_ids": null,
      "rationale": "The repo executor can write and test the migration locally, but applying it to external environments and coordinating deploy order requires operator access.",
      "requires_human_only_reason": null
    },
    {
      "id": "U2",
      "description": "After deployment, manually smoke test one dyad with mediator and Tante Rosi: pending prompt appears when undecided, `set_partner_sharing` records opt-in/out for the active bot only, and the partner sees only opted-in shareable summaries with provenance.",
      "phase": "after_execute",
      "blocks_task_ids": null,
      "rationale": "Manual product smoke coverage catches prompt UX and live-data integration issues outside the local test harness.",
      "requires_human_only_reason": null
    }
  ],
  "meta_commentary": "Execute in schema-first order, then remove the old user field everywhere before relying on the dropping migration. Keep the raw-message boundary strict: current-bot partner_share can unlock only same-bot/topic raw messages, while cross-bot sharing is summary-only and gated by the artifact owner\u2019s partner_share for the artifact\u2019s recorded bot. The main implementation trap is a partial migration/code split: do not leave production code reading `users.cross_thread_sharing_default` after `0035` drops it. The second trap is prompt inheritance: wire the canonical slot through generic solo prompts so coach and future solo bots get it without bespoke work.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Add Tante Rosi bot id constant and replace literals where appropriate.",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: Add migration `0035_per_bot_partner_sharing.sql` with Rosi bot seed, partner_share, backfill, memory fields, indexes, and old-column drop.",
        "finalize_item_ids": [
          "T1",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 3: Add shared partner-sharing service for normalization, fetching, upsert, partner resolution, and provenance.",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Update user model, turn context, and staging to remove global sharing field and use per-bot state.",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 5: Replace old sharing tool and registry/scope references with `set_partner_sharing`.",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 6: Run stale-reference sweep for old sharing names before deeper rewrites.",
        "finalize_item_ids": [
          "T5",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 7: Flip pure privacy decisions to use per-bot partner_share.",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 8: Scope dyadic raw-message reads by bot/topic in hot context and read tools.",
        "finalize_item_ids": [
          "T7",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 9: Rewrite dyadic hot-context partner-share state and labels.",
        "finalize_item_ids": [
          "T8"
        ]
      },
      {
        "plan_step_summary": "Step 10: Add cross-bot shareable-summary pull with provenance, recency ordering, and cap.",
        "finalize_item_ids": [
          "T8",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 11: Extend solo hot context with current-bot partner-share pending state and no partner content exposure.",
        "finalize_item_ids": [
          "T9"
        ]
      },
      {
        "plan_step_summary": "Step 12: Add canonical pending partner-sharing prompt slot once.",
        "finalize_item_ids": [
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 13: Wire canonical slot through mediator, generic solo/coach, and Tante Rosi prompt paths.",
        "finalize_item_ids": [
          "T11"
        ]
      },
      {
        "plan_step_summary": "Step 14: Extend memory tool schema/write path with visibility and shareable summary validation/persistence.",
        "finalize_item_ids": [
          "T12",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 15: Keep distillation contract bot-scoped and render partner/cross-bot rows as summaries only.",
        "finalize_item_ids": [
          "T12",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 16: Update fake pool and existing fixtures/tests for bots, user_bot_state.partner_share, message bot/topic, and removed users column.",
        "finalize_item_ids": [
          "T13"
        ]
      },
      {
        "plan_step_summary": "Step 17: Add focused regression coverage for migration, privacy matrix, cross-bot independence, raw-message isolation, prompt slots, tools, and memory validation.",
        "finalize_item_ids": [
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Execution order and validation order: run stale-reference sweeps, focused pytest commands, full suite, and a throwaway reproduction script before finalizing.",
        "finalize_item_ids": [
          "T14"
        ]
      },
      {
        "plan_step_summary": "External rollout: apply migration/deploy and manual smoke test outside the local repo executor.",
        "finalize_item_ids": [
          "U1",
          "U2"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All approved numbered steps are mapped to execution tasks. The final task is intentionally verification-only and includes the required throwaway reproduction script, which must be deleted before completion. External DB migration/deploy and live smoke testing are captured as user actions because they require operator access outside repo editing.",
    "coverage_complete": true
  },
  "baseline_test_failures": [],
  "baseline_test_command": "pytest --tb=no -q --no-header",
  "baseline_test_note": "No baseline test run is part of finalization; executor should run the focused and full test commands in T14 after implementation."
}

        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-13T22:38:20Z",
  "hash": "sha256:05432fa119516bc986dddb970b914e341c2e7a56d92c576e03c85a0b0665a68b",
  "changes_summary": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
  "flags_addressed": [
    "correctness",
    "all_locations",
    "callers",
    "FLAG-005",
    "issue_hints",
    "scope"
  ],
  "questions": [],
  "success_criteria": [
    {
      "criterion": "Migration `0035_per_bot_partner_sharing.sql` guarantees `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    },
    {
      "criterion": "Migration `0035_per_bot_partner_sharing.sql` adds `user_bot_state.partner_share` with allowed values `opt_in`, `opt_out`, or NULL, and backfills non-NULL mediator values from `users.cross_thread_sharing_default` before dropping the old column.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Migration adds `memories.visibility`, `memories.shareable_summary`, and `memories.shareable_summary_encrypted`, with a database CHECK requiring non-empty shareable summaries for `dyad_shareable` memories.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Production code has no remaining reads/writes of `users.cross_thread_sharing_default` and no `update_cross_thread_sharing_default` tool path after the rewrite.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "`partner_of`, `app/staging.py`, `app/models/user.py`, prompt renderers, read tools, write tools, registry, and scope guard are all updated to use per-bot partner_share or no sharing field.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    },
    {
      "criterion": "Raw message reads in hot context, `search_messages`, and `recent_activity` are scoped to the message's bot/topic before partner visibility is applied, so one bot's opt-in cannot expose another bot's raw messages.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`raw_message_visibility()` and all callers use `user_bot_state.partner_share` for the relevant owner and relevant bot, with NULL and `opt_out` both blocking partner-visible raw content.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Partner hot context includes another user\u2019s `dyad_shareable` memories and distillations from any opted-in bot, renders only `shareable_summary`, and includes a provenance prefix derived from bot display names.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Hot context emits pending partner-sharing state only when the current user has a dyad partner and the current bot\u2019s partner_share is NULL or missing.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "The canonical pending-opt-in prompt slot is defined once and used by mediator, Tante Rosi, and generic solo/coach prompt paths.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`set_partner_sharing(opt_in: bool)` exists, is available in the record/write step for bots including Tante Rosi and coach, only upserts `(ctx.user.id, ctx.bot_id)`, and succeeds for `ctx.bot_id='tante_rosi'` against the migrated schema.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`add_memory` in root `tool_schemas.py` and `app/services/tools/write_tools.py` accepts `visibility` and `shareable_summary`, encrypts/persists the summary, and rejects `dyad_shareable` calls with missing or blank summaries.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "`TANTE_ROSI_BOT_ID` exists in `app/bots/ids.py` and Python code avoids new hard-coded Tante Rosi or mediator bot id strings where constants are available.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_shell"
      ]
    },
    {
      "criterion": "Tests cover NULL, `opt_out`, `opt_in`+private, `opt_in`+`dyad_shareable`, cross-bot independence, raw-message bot-scope isolation, no-partner pending-slot suppression, and Rosi partner-share FK success.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Cross-bot partner content has an explicit recency ordering rule and fixed global cap documented in code or tests.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Prompt and hot-context labels consistently use `partner_share` / `partner_sharing_state` terminology rather than stale `sharing_default` wording, except for intentional historical migration references.",
      "priority": "should",
      "requires": [
        "run_shell",
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Future work for re-asking after opt-out or finer per-topic sharing remains documented as out of scope and is not implemented opportunistically.",
      "priority": "info",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "The next migration remains `0035_per_bot_partner_sharing.sql` because the checkout currently ends at `0034_weekly_reflection.sql`.",
    "Seeding `bots(id='tante_rosi')` is not out-of-scope new bot registration; it is the narrow FK prerequisite for an existing in-scope bot to use `user_bot_state`.",
    "Legacy users with NULL `cross_thread_sharing_default` do not need explicit mediator `user_bot_state` rows; missing row and NULL both mean pending.",
    "Partner existence and partner user id are resolved from `dyads`/`dyad_members`.",
    "Raw messages are bot/topic scoped using existing `messages.bot_id` and `messages.topic_id`; current-bot partner_share never unlocks another bot's raw messages.",
    "Cross-bot sharing intentionally uses `recorded_by_bot_id` and shareable summaries, not raw message text.",
    "Cross-bot partner summaries are ordered by recency across all opted-in bots and capped globally.",
    "Tante Rosi should keep bridge/escalation tools excluded; per-bot sharing only affects `dyad_shareable` memories/distillations surfaced through hot context."
  ],
  "delta_from_previous_percent": 8.68,
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 17,
    "items": [
      {
        "criterion": "Migration `0035_per_bot_partner_sharing.sql` guarantees `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_tests"
        ]
      },
      {
        "criterion": "Migration `0035_per_bot_partner_sharing.sql` adds `user_bot_state.partner_share` with allowed values `opt_in`, `opt_out`, or NULL, and backfills non-NULL mediator values from `users.cross_thread_sharing_default` before dropping the old column.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Migration adds `memories.visibility`, `memories.shareable_summary`, and `memories.shareable_summary_encrypted`, with a database CHECK requiring non-empty shareable summaries for `dyad_shareable` memories.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Production code has no remaining reads/writes of `users.cross_thread_sharing_default` and no `update_cross_thread_sharing_default` tool path after the rewrite.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "`partner_of`, `app/staging.py`, `app/models/user.py`, prompt renderers, read tools, write tools, registry, and scope guard are all updated to use per-bot partner_share or no sharing field.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_tests"
        ]
      },
      {
        "criterion": "Raw message reads in hot context, `search_messages`, and `recent_activity` are scoped to the message's bot/topic before partner visibility is applied, so one bot's opt-in cannot expose another bot's raw messages.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`raw_message_visibility()` and all callers use `user_bot_state.partner_share` for the relevant owner and relevant bot, with NULL and `opt_out` both blocking partner-visible raw content.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Partner hot context includes another user\u2019s `dyad_shareable` memories and distillations from any opted-in bot, renders only `shareable_summary`, and includes a provenance prefix derived from bot display names.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Hot context emits pending partner-sharing state only when the current user has a dyad partner and the current bot\u2019s partner_share is NULL or missing.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "The canonical pending-opt-in prompt slot is defined once and used by mediator, Tante Rosi, and generic solo/coach prompt paths.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`set_partner_sharing(opt_in: bool)` exists, is available in the record/write step for bots including Tante Rosi and coach, only upserts `(ctx.user.id, ctx.bot_id)`, and succeeds for `ctx.bot_id='tante_rosi'` against the migrated schema.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`add_memory` in root `tool_schemas.py` and `app/services/tools/write_tools.py` accepts `visibility` and `shareable_summary`, encrypts/persists the summary, and rejects `dyad_shareable` calls with missing or blank summaries.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "`TANTE_ROSI_BOT_ID` exists in `app/bots/ids.py` and Python code avoids new hard-coded Tante Rosi or mediator bot id strings where constants are available.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_shell"
        ]
      },
      {
        "criterion": "Tests cover NULL, `opt_out`, `opt_in`+private, `opt_in`+`dyad_shareable`, cross-bot independence, raw-message bot-scope isolation, no-partner pending-slot suppression, and Rosi partner-share FK success.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Cross-bot partner content has an explicit recency ordering rule and fixed global cap documented in code or tests.",
        "priority": "should",
        "requires": [
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Prompt and hot-context labels consistently use `partner_share` / `partner_sharing_state` terminology rather than stale `sharing_default` wording, except for intentional historical migration references.",
        "priority": "should",
        "requires": [
          "run_shell",
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Future work for re-asking after opt-out or finer per-topic sharing remains documented as out of scope and is not implemented opportunistically.",
        "priority": "info",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "issue_hints-1",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the brief's requirement that the shared pending opt-in slot be used by every bot. The plan imports the canonical slot into the mediator and Tante Rosi renderers, but this repo already has a third BotSpec, `coach`, in `app/bots/coach.py`, which delegates to `app/services/prompts_solo.py`; the plan does not say to update that generic solo prompt path or otherwise guarantee coach/new solo bots inherit the slot.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "issue_hints-2",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the file locations named by the plan against the repository. The schemas live in the repository-root `tool_schemas.py`, while the plan repeatedly refers to `app/services/tools/tool_schemas.py`; an executor following the path literally will not find the file, though the surrounding registry imports make the intended target recoverable.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Checked the planned `set_partner_sharing` write shape against the current schema. The upsert target `(ctx.user.id, ctx.bot_id)` is the right authorization boundary, but it depends on the calling bot already existing in `bots` because `user_bot_state.bot_id` has a foreign key; that dependency is not satisfied for Tante Rosi by the current migration set.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched for `cross_thread_sharing_default` and found additional production users beyond the plan's focal list, notably `app/services/turn_context.py::partner_of` and `app/staging.py`. The plan covers user model hydration, `base.py`, prompts, hot context, and tools, and has a final `rg` sweep, but it does not explicitly call out `partner_of`; after the migration drops the column, that SELECT would fail unless the executor catches it in the sweep.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched read paths using raw-message sharing decisions and found `search_messages`, `recent_activity`, and `get_distillations` in `app/services/tools/read_tools.py` still derive sharing from `ctx.user.cross_thread_sharing_default`/`ctx.partner.cross_thread_sharing_default`. The plan has a broad Step 13 for read tools, but it does not explicitly require these read tools to batch-load `user_bot_state.partner_share` or apply bot/topic scope to message reads.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting database setup locations for bots. Migrations seed `mediator` in `0020_topics_bots_bindings.sql` and staging-only `coach` in `0031_coach_staging_seed.sql`, but no migration seeds `tante_rosi`; since the new feature writes `user_bot_state` rows for Rosi, the plan is missing supporting infrastructure for the bot registry/database FK boundary.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked callers that will invoke the new `set_partner_sharing` tool. The plan correctly removes user_id/bot_id from the input and derives both from `ctx`, but for any caller with `ctx.bot_id='tante_rosi'` the database upsert still requires a matching `bots` row; the plan does not guarantee that prerequisite.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the plan's stated support for `set_partner_sharing` on Tante Rosi against the migrations. `user_bot_state.bot_id` references `bots(id)`, but the current migrations insert only `mediator` and staging-only `coach`; `0033_pregnancy_topic.sql` creates the pregnancy topic but no `tante_rosi` bot row. The plan does not add or require that bot row, so Rosi's partner-share upsert can fail on a real DB even though the tool is wired.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched bot registration and schema support for partner-share state. The current registry can expose Tante Rosi under `STAGING=1` without a database `bots` row, while prod registration requires row existence; because partner sharing writes through a foreign-keyed `user_bot_state` row, the plan's scope should include seeding or validating `bots(id='tante_rosi')` wherever Rosi is callable.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    }
  ],
  "recommendation": "PROCEED",
  "rationale": "The plan is now execution-ready. The first-round privacy and all-location gaps were fixed in v2, and the remaining database FK prerequisite for Tante Rosi was fixed in v3 by requiring `bots(id='tante_rosi')` to be guaranteed in migration `0035` before any Rosi `user_bot_state` upsert. The remaining significant flags are marked addressed, and the critique check is clear across issue hints, correctness, scope, all-locations, and callers.",
  "signals_assessment": "Score moved 10.5 -> 11.5 -> 10.0 with a large v2 correction and a focused v3 correction. All significant flags are now addressed, with no reopened critiques and no open critique category. Preflight is clean: project exists, workspace is writable, success criteria are present, and tools are available. The only recurring note is subjective verification of the cross-bot ordering/cap criterion, which is a review check rather than a plan blocker.",
  "warnings": [
    "During execution, verify migration `0035` seeds or guarantees `bots(id='tante_rosi')` before any Rosi `user_bot_state` write path is tested.",
    "Keep raw messages strictly same-bot/topic scoped; cross-bot partner sharing should render only shareable summaries.",
    "Run the stale-reference sweeps before final validation because the migration drops `users.cross_thread_sharing_default`."
  ],
  "settled_decisions": [
    {
      "id": "tante-rosi-fk",
      "decision": "Migration `0035` must guarantee `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
      "rationale": "`user_bot_state.bot_id` references `bots(id)`, and Rosi is explicitly in scope for partner sharing."
    },
    {
      "id": "raw-message-boundary",
      "decision": "Raw messages are scoped to same bot/topic before partner-share visibility is applied.",
      "rationale": "Current-bot opt-in must not expose another bot's raw messages; cross-bot sharing uses summaries only."
    },
    {
      "id": "schema-target",
      "decision": "Tool schema edits target root `tool_schemas.py`.",
      "rationale": "That is the actual schema file in this repo."
    },
    {
      "id": "prompt-inheritance",
      "decision": "The canonical pending slot is wired through mediator, Tante Rosi, and generic solo/coach prompt paths.",
      "rationale": "The brief requires every bot to inherit the shared prompt slot."
    },
    {
      "id": "partner-source",
      "decision": "Partner resolution uses `dyads`/`dyad_members`.",
      "rationale": "The current schema does not have `users.partner_user_id`."
    },
    {
      "id": "migration-number",
      "decision": "Use `0035_per_bot_partner_sharing.sql` if the checkout still ends at `0034_weekly_reflection.sql`.",
      "rationale": "The migration chain has advanced beyond the brief's stale numbering hint."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Plan passed gate and preflight. Proceed to finalize. Verify unresolved flags against the plan and project code before accepting. Recurring critiques (criterion 14: requires human verification (subjective_judgment).); the loop likely can't fix these, so judge if they are real blockers.",
  "robustness": "standard",
  "signals": {
    "iteration": 3,
    "idea": "# Per-bot partner sharing \u2014 design brief\n\n## Context\n\nThe Veas codebase runs N bots that each occupy a \"domain\" for a user (currently: `mediator` = relationship coach for a dyad on topic=relationship; `tante_rosi` = solo pregnancy coach on topic=pregnancy; more bots planned). Today only the mediator's content can flow between dyad partners, gated by a **global** opt-in (`users.cross_thread_sharing_default`). The pregnancy coach writes everything private; her facts cannot reach the partner even when the user wants to share them.\n\nWe want to generalise partner-sharing so that **every bot** (current and future) can produce content that the user's partner sees, gated by a **per-bot** opt-in. The user gets one switch per domain (\"share my pregnancy stuff with my partner \u2014 yes / no / not decided yet\"). Until they decide, the bot keeps surfacing the question.\n\nThe basic infrastructure already exists for distillations (`visibility: private | dyad_shareable`, `shareable_summary`, `raw_message_visibility()` filtering in `app/services/cross_thread_privacy.py`, `app/services/hot_context.py:500-577`). The work below generalises it across both bots-and-content-types, and replaces the global toggle with a per-bot one.\n\n## Goal (one sentence)\n\nReplace the single global `users.cross_thread_sharing_default` with per-bot opt-in state on `user_bot_state`, extend `dyad_shareable` visibility to `memories` (today it only exists on `distillations`), and rewire the hot-context read path so a partner sees `dyad_shareable` content from any bot where the content's owner has opted in for *that* bot \u2014 with NULL (\"not decided\") triggering a prompt-slot the bot uses to ask.\n\n## Decisions already made (do not re-litigate)\n\nThese are settled \u2014 the plan should implement them, not re-debate them.\n\n1. **Per-bot opt-in lives on `user_bot_state`** as one new column `partner_share text` with values `'opt_in' | 'opt_out' | NULL`. NULL = \"pending, must ask\". Key is `(user_id, bot_id)` \u2014 same shape as every other per-bot state today.\n2. **Memories get `visibility` and `shareable_summary`** mirroring distillations exactly. Default `visibility='private'`. When `visibility='dyad_shareable'`, `shareable_summary` is required.\n3. **The opt-in is shown until decided.** While `partner_share IS NULL`, every render of that bot's hot context includes a \"pending opt-in\" slot in the system prompt asking the bot to raise the question this turn. As soon as the value is non-NULL (`opt_in` OR `opt_out`), the slot drops out and the bot stops raising it.\n4. **One shared prompt slot, used by every bot.** Define one canonical pending-opt-in paragraph used by every bot's `render_system_prompt`. Rosi's existing `_FIRST_CONTACT_V1` collapses into it; the mediator's onboarding language for cross-thread sharing also collapses into it. New bots inherit the slot for free \u2014 no per-bot prompt work.\n5. **One shared tool: `set_partner_sharing(opt_in: bool)`.** Implicit `bot_id` (from the calling bot's scope). Writes to `user_bot_state.partner_share` for the calling (user, bot) pair.\n6. **Migration: the existing global flag goes away.** Backfill `user_bot_state[bot_id='mediator', user_id=X].partner_share` from `users.cross_thread_sharing_default` for every existing user, then drop `users.cross_thread_sharing_default`. One model, not two \u2014 no fallback path, no two-system-running period.\n7. **No per-row UX in v1.** The user gets the per-bot toggle. The bot decides per-call whether a given memory/distillation should be `private` vs `dyad_shareable` based on the content. No user-facing per-row controls.\n8. **Hot context cross-bot pull is in scope.** When rendering for user B (the partner of A), pull A's `dyad_shareable` rows from *any* bot where `partner_share[A, that_bot] = 'opt_in'`, surfaced with a provenance prefix (e.g. `from Rosi:`). Same-bot dyad sharing (the existing mediator behaviour) keeps working unchanged in shape, just driven by the new column.\n\n## Files known to be relevant (planner should read at least these)\n\nThe planner should still survey the repo, but these are the focal points:\n\n- `migrations/0012_cross_thread_sharing.sql` \u2014 defines the global flag being retired.\n- `migrations/0015_distillations.sql` \u2014 defines `visibility` + `shareable_summary` we're mirroring onto memories.\n- `migrations/0022_topic_status_user_bot_state.sql` \u2014 defines `user_bot_state` (current schema: `user_id, bot_id, onboarding_state, paused`).\n- The next available migration number is `0020` (or whatever is highest after `0019_feedback_reaction_context.sql`); planner should verify.\n- `app/services/cross_thread_privacy.py` \u2014 `raw_message_visibility()` lives here; needs to flip from global flag to per-bot lookup.\n- `app/services/hot_context.py` (especially lines 500-577) \u2014 read path; needs (a) per-bot lookup, (b) cross-bot pull for partner, (c) emitting the `partner_sharing_state: 'pending'` signal.\n- `app/services/tools/write_tools.py` \u2014 `add_memory` (~line 776) and `add_distillation` (~line 1165). The `add_memory` write helper needs to accept `visibility` + `shareable_summary`.\n- `app/services/tools/tool_schemas.py` \u2014 `AddMemoryInput` needs new fields mirroring `AddDistillationInput.visibility` etc. (~line 996 for the distillation schema as the template).\n- `app/bots/mediator.py` and `app/bots/tante_rosi.py` \u2014 both need to (a) include the canonical pending-opt-in slot via their `render_system_prompt`, (b) be eligible to call `set_partner_sharing`. Rosi additionally needs prompt language about *when* to write `dyad_shareable` rows once opted in.\n- `app/bots/prompts/tante_rosi.py` (`_FIRST_CONTACT_V1`) and the equivalent mediator prompt file \u2014 the canonical slot replaces/absorbs whatever a[REDACTED_SK] language already exists in each.\n- `app/bots/` tool dispatch \u2014 wherever bot tool allowlists are wired, `set_partner_sharing` must be available to every bot (it's user-state-modifying, like `set_pregnancy_edd`, not domain-specific).\n\n## Invariants to enforce (must hold)\n\n1. **NULL \u2192 silent.** When `partner_share IS NULL`, *no* content from that (user, bot) is shared with the partner regardless of per-row `visibility`. The toggle is the gate; per-row visibility only matters when the toggle is `opt_in`.\n2. **opt_out \u2192 silent.** Same as NULL for the read path. The only difference is the prompt slot doesn't surface.\n3. **opt_in \u2192 per-row decides.** When the toggle is `opt_in`, dyad_shareable rows from that bot flow to the partner; private rows don't.\n4. **No partner \u2192 moot.** When the user has no partner (`users.partner_user_id IS NULL`), the prompt slot is suppressed even with `partner_share IS NULL`. Nothing to share to. Don't ask a question that has no answer.\n5. **No backsliding on the mediator.** Every existing mediator user must continue to see exactly what they see today \u2014 the migration must be observationally equivalent. A user whose current `cross_thread_sharing_default = 'opt_in'` ends up with `user_bot_state[mediator].partner_share = 'opt_in'`; a user with `'opt_out'` ends up `'opt_out'`; NULL stays NULL.\n6. **Cross-bot pull is opt-in-gated, not opt-out-gated.** Default is \"don't show partner's other-bot content.\" Only `'opt_in'` from the content owner unlocks the pull. This matters: a partner who hasn't decided cannot accidentally have their content surfaced because of someone *else's* default.\n7. **Tool authorisation.** `set_partner_sharing` writes only to the calling user's row for the calling bot. A user calling Rosi cannot toggle their mediator state; Rosi cannot toggle V\u00e9as's state. Scope is `(message.sender_id, message.bot_id)`.\n8. **The shareable_summary contract.** When `add_memory` or `add_distillation` is called with `visibility='dyad_shareable'`, `shareable_summary` must be non-null and non-empty. Reject the call otherwise. Same rule that already applies to distillations should now apply to memories.\n\n## Edge cases and ordering concerns\n\nThe planner should treat these as real, not paranoid:\n\n- **Migration backfill ordering.** The new column on `user_bot_state` must be added and backfilled before `cross_thread_sharing_default` is dropped. The hot-context read path must be flipped to the new column *atomically* with the drop, or the system briefly reads from a dropped column. Plan the migration as a single transaction or with explicit phasing.\n- **Backfill for users without a `user_bot_state[mediator]` row.** Some legacy users may not have a `user_bot_state` row for the mediator yet (it may be created lazily on first message). The migration must create rows for any user with a non-NULL `cross_thread_sharing_default`. For users with NULL global setting, decide: either create rows pre-set to NULL (explicit pending state) or skip (lazy creation later, still NULL). Either is defensible \u2014 make a call and write it down.\n- **The pending slot wording is shared.** Different bots have different voices. The shared slot must be voice-agnostic \u2014 short, neutral, instructive to the model, not user-facing copy. The bot's own voice handles the actual question to the user; the slot just tells the bot \"raise this naturally this turn.\"\n- **Cross-bot pull volume.** A partner with several opted-in bots could see a long list of \"from X:\" rows in their hot context. Budget for hot-context length: cap, summarise, or rank. Don't ship a context bomb.\n- **Order of cross-bot content.** When pulling rows from multiple bots, by what order? By recency? By bot? Pick one and write it down so the reviewer can check it.\n- **Provenance prefix format.** \"from Rosi:\" / \"from V\u00e9as:\" \u2014 bake into a single helper, not sprinkled. Bots are named via the bot registry; use the registry's display name, not a hard-coded string.\n\n## Explicitly out of scope\n\n- Per-row visibility controls exposed to the user. (The bot decides per-row; users only decide per-bot.)\n- Re-asking after some time has passed. Once `opt_in` or `opt_out` is set, the slot stays gone. Future work, not this sprint.\n- New bot registration code. The pattern must work for new bots when they show up, but we are not adding a new bot in this sprint.\n- Per-topic granularity within a bot. Each bot is one domain; one toggle per bot is enough.\n- UI surfaces. There is no UI today and we are not building one.\n- Encryption-at-rest changes. `shareable_summary` on memories follows whatever the existing memory content encryption pattern is.\n\n## Success criteria\n\nReviewer should check, in priority order:\n\n**must**\n- Migration adds `user_bot_state.partner_share` and backfills it from `users.cross_thread_sharing_default` for every user where the global flag was non-NULL, preserving the same value semantically (`'opt_in' \u2192 'opt_in'`, `'opt_out' \u2192 'opt_out'`).\n- Migration adds `memories.visibility` (default `'private'`) and `memories.shareable_summary` (nullable) with a CHECK constraint matching the existing distillations one (`shareable_summary` required iff `visibility='dyad_shareable'`).\n- Migration drops `users.cross_thread_sharing_default` only after the read path is updated.\n- `cross_thread_privacy.raw_message_visibility()` (and any other reader of the old column) reads from `user_bot_state.partner_share` for the relevant bot, not from `users.cross_thread_sharing_default`.\n- `hot_context.py` cross-bot pull lands: when rendering for partner B, B sees A's `dyad_shareable` memories and distillations from any bot where `partner_share[A, that_bot]='opt_in'`, with a provenance prefix from the bot registry.\n- `hot_context.py` emits `partner_sharing_state: 'pending'` when `partner_share IS NULL` and the user has a partner; the canonical prompt slot is rendered into the system prompt of any bot whose hot context carries this signal.\n- `set_partner_sharing` tool exists, is wired into the tool registry for every bot, and updates `user_bot_state.partner_share` for the calling `(user, bot)` only.\n- `add_memory` accepts `visibility` and `shareable_summary`; rejects `dyad_shareable` without `shareable_summary`.\n- Rosi's prompt is updated so that when `partner_share='opt_in'`, she writes `dyad_shareable` memories and distillations for non-sensitive facts (with appropriate `shareable_summary`).\n- Mediator's existing partner-sharing onboarding language is collapsed into the canonical slot; mediator continues to behave observationally as today for existing users post-migration.\n- Tests cover: NULL \u2192 no partner content visible; `opt_out` \u2192 no partner content visible; `opt_in` + `private` row \u2192 no partner content visible; `opt_in` + `dyad_shareable` row \u2192 partner content visible with provenance; cross-bot pull respects toggle independently per bot; user with no partner never sees the pending slot.\n\n**should**\n- Cross-bot content ordering and length budget are explicit (chosen rule, written down in code or comment).\n- Migration is a single transaction or has explicit phasing documented.\n- The canonical prompt slot is defined in one place and imported by both bot prompt files.\n\n**info**\n- Future work for re-asking or per-topic granularity is captured (e.g., as a ticket via `megaplan ticket new`) but not implemented.\n\n## Notes for the planner\n\n- **Do not invent new bot-ID strings.** Use the existing `bot_id` constants from `app/bots/ids.py`.\n- **Do not gate behaviour on bot identity if it can be data-driven.** The whole point is N bots; if Rosi gets a code path that V\u00e9as doesn't, that's a smell. The only legitimate per-bot differences are prompt content and topic, both of which are already data-driven.\n- **The pending slot's prompt language matters.** Write it once, write it well, and stop. Bots are instructed *what* to do (raise the question this turn), not *how* to phrase it \u2014 voice belongs to each bot.\n- **The migration is the riskiest piece.** Get the ordering and the backfill right and the rest is mechanical.",
    "significant_flags": 9,
    "unresolved_flags": [
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the brief's requirement that the shared pending opt-in slot be used by every bot. The plan imports the canonical slot into the mediator and Tante Rosi renderers, but this repo already has a third BotSpec, `coach`, in `app/bots/coach.py`, which delegates to `app/services/prompts_solo.py`; the plan does not say to update that generic solo prompt path or otherwise guarantee coach/new solo bots inherit the slot.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the file locations named by the plan against the repository. The schemas live in the repository-root `tool_schemas.py`, while the plan repeatedly refers to `app/services/tools/tool_schemas.py`; an executor following the path literally will not find the file, though the surrounding registry imports make the intended target recoverable.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Checked the planned `set_partner_sharing` write shape against the current schema. The upsert target `(ctx.user.id, ctx.bot_id)` is the right authorization boundary, but it depends on the calling bot already existing in `bots` because `user_bot_state.bot_id` has a foreign key; that dependency is not satisfied for Tante Rosi by the current migration set.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched for `cross_thread_sharing_default` and found additional production users beyond the plan's focal list, notably `app/services/turn_context.py::partner_of` and `app/staging.py`. The plan covers user model hydration, `base.py`, prompts, hot context, and tools, and has a final `rg` sweep, but it does not explicitly call out `partner_of`; after the migration drops the column, that SELECT would fail unless the executor catches it in the sweep.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched read paths using raw-message sharing decisions and found `search_messages`, `recent_activity`, and `get_distillations` in `app/services/tools/read_tools.py` still derive sharing from `ctx.user.cross_thread_sharing_default`/`ctx.partner.cross_thread_sharing_default`. The plan has a broad Step 13 for read tools, but it does not explicitly require these read tools to batch-load `user_bot_state.partner_share` or apply bot/topic scope to message reads.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting database setup locations for bots. Migrations seed `mediator` in `0020_topics_bots_bindings.sql` and staging-only `coach` in `0031_coach_staging_seed.sql`, but no migration seeds `tante_rosi`; since the new feature writes `user_bot_state` rows for Rosi, the plan is missing supporting infrastructure for the bot registry/database FK boundary.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked callers that will invoke the new `set_partner_sharing` tool. The plan correctly removes user_id/bot_id from the input and derives both from `ctx`, but for any caller with `ctx.bot_id='tante_rosi'` the database upsert still requires a matching `bots` row; the plan does not guarantee that prerequisite.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the plan's stated support for `set_partner_sharing` on Tante Rosi against the migrations. `user_bot_state.bot_id` references `bots(id)`, but the current migrations insert only `mediator` and staging-only `coach`; `0033_pregnancy_topic.sql` creates the pregnancy topic but no `tante_rosi` bot row. The plan does not add or require that bot row, so Rosi's partner-share upsert can fail on a real DB even though the tool is wired.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched bot registration and schema support for partner-share state. The current registry can expose Tante Rosi under `STAGING=1` without a database `bots` row, while prod registration requires row existence; because partner sharing writes through a foreign-keyed `user_bot_state` row, the plan's scope should include seeding or validating `bots(id='tante_rosi')` wherever Rosi is callable.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Correctness: dyadic raw-message reads are not explicitly scoped to the message's bot/topic before applying per-bot sharing. Since `hot_context.py` currently reads all messages involving either partner without a `bot_id` predicate, using the current bot's `partner_share` as the gate can leak another bot's raw messages when the owner opted into mediator but not that other bot.",
        "resolution": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi."
      },
      {
        "id": "FLAG-002",
        "concern": "Completeness: the canonical pending opt-in slot is planned for mediator and Tante Rosi, but not for the existing generic solo/coach prompt path, despite the requirement that every bot inherit the shared slot.",
        "resolution": "`app/bots/coach.py` defines a live BotSpec that renders via `app/services/prompts_solo.py`; plan Step 7 names importing the slot from mediator and Rosi prompt renderers, and Step 9 only updates Rosi-specific solo prompt code."
      },
      {
        "id": "FLAG-003",
        "concern": "Completeness: production readers of the dropped user column are not all explicitly enumerated. `partner_of` and several read-tool paths still select or consume `cross_thread_sharing_default`, so relying on the final grep sweep is brittle for a migration that drops the column.",
        "resolution": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi."
      },
      {
        "id": "FLAG-004",
        "concern": "Maintainability: the plan references a non-existent `app/services/tools/tool_schemas.py` path and literal bot id strings even though this repo's schema file is root-level `tool_schemas.py` and only mediator has a bot id constant today.",
        "resolution": "`rg --files` shows `tool_schemas.py` at repository root and no `app/services/tools/tool_schemas.py`; `app/bots/ids.py` contains `MEDIATOR_BOT_ID` only, while `app/bots/tante_rosi.py` currently uses literal `bot_id='tante_rosi'`."
      },
      {
        "id": "FLAG-005",
        "concern": "Completeness: Tante Rosi is planned to call `set_partner_sharing`, but the database migrations do not seed a `bots(id='tante_rosi')` row. Because `user_bot_state.bot_id` has a foreign key to `bots(id)`, partner-share upserts for Rosi can fail in real databases where Rosi is registered from code or expected to be current.",
        "resolution": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary."
      }
    ],
    "weighted_score": 10.0,
    "weighted_history": [
      10.5,
      11.5
    ],
    "plan_delta_from_previous": 8.68,
    "recurring_critiques": [
      "criterion 14: requires human verification (subjective_judgment)."
    ],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 3. Weighted score trajectory: 10.5 -> 11.5 -> 10.0. Plan deltas: 88.7%, 8.7%. Recurring critiques: 1. Resolved flags: 5. Open significant flags: 9.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [
    {
      "flag_id": "issue_hints-1",
      "action": "dispute",
      "evidence": "Plan v3 Step 13 explicitly wires the canonical slot through `app/services/prompts_solo.py`, `app/bots/coach.py`, and `app/bots/tante_rosi.py`, in addition to mediator prompts.",
      "rationale": ""
    },
    {
      "flag_id": "issue_hints-2",
      "action": "dispute",
      "evidence": "Plan v3 Overview and Steps 5, 14, and 15 refer to root `tool_schemas.py`, not `app/services/tools/tool_schemas.py`.",
      "rationale": ""
    },
    {
      "flag_id": "correctness",
      "action": "dispute",
      "evidence": "Plan v3 Step 2.2 requires inserting `bots(id, display_name)` row `('tante_rosi', 'Tante Rosi')` before adding/using partner-share state; Step 17 also requires a Rosi FK success test.",
      "rationale": ""
    },
    {
      "flag_id": "scope-1",
      "action": "dispute",
      "evidence": "Plan v3 Step 4 explicitly updates `app/services/turn_context.py::partner_of` and `app/staging.py` to stop selecting or using the dropped user column.",
      "rationale": ""
    },
    {
      "flag_id": "scope-2",
      "action": "dispute",
      "evidence": "Plan v3 Step 8 explicitly names `search_messages`, `recent_activity`, and `get_distillations` and requires per-bot partner-share loading plus bot/topic message scoping.",
      "rationale": ""
    },
    {
      "flag_id": "all_locations",
      "action": "dispute",
      "evidence": "Plan v3 Step 2.2 guarantees a `bots(id='tante_rosi')` row in migration `0035`; Step 16 adds fake-pool bot row support; Step 17 requires SQL assertions for the row.",
      "rationale": ""
    },
    {
      "flag_id": "callers",
      "action": "dispute",
      "evidence": "Plan v3 Step 5.7 adds a targeted `set_partner_sharing` test for `ctx.bot_id=TANTE_ROSI_BOT_ID` against a migrated/fake DB where the bot row exists.",
      "rationale": ""
    },
    {
      "flag_id": "issue_hints",
      "action": "dispute",
      "evidence": "Plan v3 success criterion 1 requires migration `0035` to guarantee `bots(id='tante_rosi')` before Rosi `user_bot_state` writes, and success criterion 11 requires Rosi tool success against the migrated schema.",
      "rationale": ""
    },
    {
      "flag_id": "scope",
      "action": "dispute",
      "evidence": "Plan v3 explicitly treats seeding `bots(id='tante_rosi')` as the narrow FK prerequisite for the existing in-scope Rosi bot, not as broad new bot registration.",
      "rationale": ""
    }
  ],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Settled decisions (verify the executor implemented these correctly):
- tante-rosi-fk: Migration `0035` must guarantee `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows. (`user_bot_state.bot_id` references `bots(id)`, and Rosi is explicitly in scope for partner sharing.)
- raw-message-boundary: Raw messages are scoped to same bot/topic before partner-share visibility is applied. (Current-bot opt-in must not expose another bot's raw messages; cross-bot sharing uses summaries only.)
- schema-target: Tool schema edits target root `tool_schemas.py`. (That is the actual schema file in this repo.)
- prompt-inheritance: The canonical pending slot is wired through mediator, Tante Rosi, and generic solo/coach prompt paths. (The brief requires every bot to inherit the shared prompt slot.)
- partner-source: Partner resolution uses `dyads`/`dyad_members`. (The current schema does not have `users.partner_user_id`.)
- migration-number: Use `0035_per_bot_partner_sharing.sql` if the checkout still ends at `0034_weekly_reflection.sql`. (The migration chain has advanced beyond the brief's stale numbering hint.)


Critique flags to re-verify against the final diff:
            [
  {
    "id": "FLAG-001",
    "concern": "Correctness: dyadic raw-message reads are not explicitly scoped to the message's bot/topic before applying per-bot sharing. Since `hot_context.py` currently reads all messages involving either partner without a `bot_id` predicate, using the current bot's `partner_share` as the gate can leak another bot's raw messages when the owner opted into mediator but not that other bot.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-002",
    "concern": "Completeness: the canonical pending opt-in slot is planned for mediator and Tante Rosi, but not for the existing generic solo/coach prompt path, despite the requirement that every bot inherit the shared slot.",
    "severity": "minor",
    "status": "verified"
  },
  {
    "id": "FLAG-003",
    "concern": "Completeness: production readers of the dropped user column are not all explicitly enumerated. `partner_of` and several read-tool paths still select or consume `cross_thread_sharing_default`, so relying on the final grep sweep is brittle for a migration that drops the column.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-004",
    "concern": "Maintainability: the plan references a non-existent `app/services/tools/tool_schemas.py` path and literal bot id strings even though this repo's schema file is root-level `tool_schemas.py` and only mediator has a bot id constant today.",
    "severity": "minor",
    "status": "verified"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 14: requires human verification (subjective_judgment).",
    "severity": "minor",
    "status": "open"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 15: requires human verification (subjective_judgment).",
    "severity": "minor",
    "status": "open"
  },
  {
    "id": "FLAG-005",
    "concern": "Completeness: Tante Rosi is planned to call `set_partner_sharing`, but the database migrations do not seed a `bots(id='tante_rosi')` row. Because `user_bot_state.bot_id` has a foreign key to `bots(id)`, partner-share upserts for Rosi can fail in real databases where Rosi is registered from code or expected to be current.",
    "severity": "significant",
    "status": "verified"
  }
]

            For each flag above that was raised during critique, verify whether the final diff actually addresses the concern.
            A flag is resolved only if the final diff contains code that directly addresses the concern.
            Do not trust pre-execute promises or plan claims; check the diff itself.
            Add resolved flag IDs to `verified_flag_ids`.
            For any unresolved flag, add a `rework_items` entry with `task_id: "REVIEW"`, `issue`, `expected`, `actual`, `evidence_file`, `flag_id`, and `source: "review_flag_reverify"`.

Advisory mechanical pre-check flags:
            [
  {
    "id": "PRECHECK-DIFF_SIZE_SANITY",
    "check": "diff_size_sanity",
    "detail": "Diff size looks larger than expected: changed_lines=9072, expected\u224810, ratio=907.20, files=55, hunks=690.",
    "severity": "significant",
    "evidence_file": "app/bots/base.py"
  }
]

            Copy this list verbatim into the output `pre_check_flags` field.

        Execution summary:
        {
  "output": "Aggregated execute batches: completed 10/10.\nBatch 1: Executed batch 4 / T4. `set_partner_sharing` is now the scoped sharing-state write tool: schema forbids user/bot overrides, registry/dispatch/write-step/scope wiring points at it, and `write_tools.set_partner_sharing` writes only `(ctx.user.id, ctx.bot_id)` through the shared partner-sharing helper. I also removed old global sharing-column usage from the edited write paths that decide bridge readiness / media explanation visibility.\n\nFocused verification passed. Full `pytest -q` was run and still fails in the same previously noted unrelated areas: `tests/test_agentic.py::test_agentic_e2e_ordering_cache_spend_and_oob` and three `tests/test_decay.py` failures around fake-pool observation UPDATE after Anthropic 401.\nBatch 2: Executed batch 5 / T5. Ran the stale-reference sweep, removed production dropped-column/old-tool dependencies, and checkpointed execution_batch_5.json. Full pytest was run and still fails only in the same previously documented tests/test_agentic.py and tests/test_decay.py failures.\nBatch 3:\nBatch 4:\nBatch 5:\nBatch 6:\nBatch 7:\nBatch 8:\nBatch 9:\nBatch 10:",
  "commands_run": [
    "rg -n \"update_cross_thread_sharing_default|set_partner_sharing|cross_thread_sharing_default|sharing_default\" tool_schemas.py app/services/tools app/bots tests",
    "python -m black app/services/tools/write_tools.py tests/test_tools.py tests/conftest.py",
    "python -m py_compile tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py tests/conftest.py tests/test_tools.py",
    "rg -n \"update_cross_thread_sharing_default|UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|ctx\\.(user|partner)\\.cross_thread_sharing_default|UpdateCrossThreadSharingDefault\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py",
    "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
    "pytest tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_tools.py -q",
    "pytest -q",
    "rg -n \"set_partner_sharing\" tool_schemas.py app/services/tools/registry.py app/services/tools/scope_guard.py app/bots/coach.py app/bots/tante_rosi.py app/bots/mediator.py tests/test_tool_schemas_importable.py tests/test_tools.py",
    "rg -n \"update_cross_thread_sharing_default\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py app/bots/coach.py app/bots/tante_rosi.py app/bots/mediator.py",
    "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py",
    "python -m black app/services/cross_thread_privacy.py app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py tests/test_tools.py",
    "python -m py_compile app/services/cross_thread_privacy.py app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py",
    "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_cross_topic.py tests/test_hot_context_join_cutover.py -q",
    "pytest tests/test_tool_schemas_importable.py tests/test_pregnancy_persona.py tests/test_eval_execution.py tests/test_coach_e2e.py -q",
    "python -m black tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
    "git status --short"
  ],
  "deviations": [
    "Full pytest still fails in the same prior unrelated-looking locations documented by earlier batches: tests/test_agentic.py::test_agentic_e2e_ordering_cache_spend_and_oob and three tests/test_decay.py failures around fake-pool observation UPDATE after Anthropic 401.",
    "Checkpoint written to .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_4.json.",
    "Advisory quality: app/services/tools/write_tools.py adds unused imports: CorrectPregnancyEddInput, EndPregnancyInput, SetPregnancyEddInput.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_4.json, app/services/tools/registry.py, app/services/tools/scope_guard.py, tool_schemas.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_tool_schemas_importable.py",
    "Advisory audit finding: Sense check SC5 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T5, T6, T7, T8, T9, T10, T11, T12, T13, T14",
    "Full pytest still fails in the same previously documented locations: tests/test_agentic.py::test_agentic_e2e_ordering_cache_spend_and_oob and three tests/test_decay.py failures around fake-pool observation UPDATE after Anthropic 401.",
    "The production sweep still finds app/models/user.py because T3 intentionally left a temporary non-hydrated User.cross_thread_sharing_default compatibility shim. It is not selected from or written to the database.",
    "Remaining non-app sweep hits are test fixtures and legacy test call shapes, intentionally left for the T13 test-infrastructure cleanup.",
    "Advisory quality: tests/test_hot_context.py grew by 204 lines (threshold 200).",
    "Advisory quality: app/bots/coach.py adds unused imports: UUID.",
    "Advisory quality: app/services/tools/write_tools.py adds unused imports: CorrectPregnancyEddInput, EndPregnancyInput, SetPregnancyEddInput.",
    "Advisory quality: app/staging.py adds unused imports: render_solo_system_prompt.",
    "Advisory quality: tests/test_hot_context_join_cutover.py adds unused imports: patch.",
    "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_5.json",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_tool_schemas_importable.py",
    "Advisory audit finding: Sense check SC6 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T6, T7, T8, T9, T10, T11, T12, T13, T14",
    "Full pytest still fails in the same previously documented locations: tests/test_agentic.py::test_agentic_e2e_ordering_cache_spend_and_oob and three tests/test_decay.py failures around fake-pool observation UPDATE after Anthropic 401.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/services/cross_thread_privacy.py, tests/test_tools.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_tool_schemas_importable.py",
    "Advisory audit finding: Sense check SC7 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T7, T8, T9, T10, T11, T12, T13, T14",
    "Full pytest still fails in tests/test_decay.py with the previously documented fake-pool observation UPDATE failures; focused T7-related modules pass.",
    "Advisory quality: tests/test_agentic.py grew by 210 lines (threshold 200).",
    "Advisory quality: tests/test_agentic.py has similar functions __init__ and __init__ (100% similarity).",
    "Advisory quality: tests/test_agentic.py has similar functions async_oob and async_oob (100% similarity).",
    "Advisory quality: app/services/tools/write_tools.py adds unused imports: CorrectPregnancyEddInput, EndPregnancyInput, SetPregnancyEddInput.",
    "Advisory quality: tests/test_hot_context_join_cutover.py adds unused imports: patch.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/services/hot_context.py, app/services/tools/read_tools.py, app/services/tools/write_tools.py, tests/conftest.py, tests/test_agentic.py, tests/test_hot_context.py, tests/test_hot_context_join_cutover.py, tests/test_tools.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_tool_schemas_importable.py",
    "Advisory audit finding: Sense check SC8 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T8, T9, T10, T11, T12, T13, T14",
    "Full pytest still fails in tests/test_decay.py with the previously documented fake-pool observation UPDATE failures; T8-focused modules pass.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/services/hot_context.py, tests/conftest.py, tests/test_hot_context.py, tests/test_hot_context_join_cutover.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_tool_schemas_importable.py",
    "Advisory audit finding: Sense check SC9 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC12 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T9, T10, T11, T12, T13, T14",
    "Advisory quality: app/services/tools/write_tools.py adds unused imports: CorrectPregnancyEddInput, EndPregnancyInput, SetPregnancyEddInput.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/services/hot_context_solo.py, app/services/tools/common.py, app/services/tools/read_tools.py, app/services/tools/write_tools.py, tests/conftest.py, tests/test_pregnancy_hot_context.py, tests/test_tool_schemas_importable.py, tests/test_tools.py, tool_schemas.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/",
    "Advisory audit finding: Sense check SC10 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T10, T11, T13, T14",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/bots/prompts/partner_sharing.py, tests/test_partner_sharing_prompt.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/",
    "Advisory audit finding: Sense check SC11 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T11, T13, T14",
    "Advisory quality: app/bots/coach.py adds unused imports: UUID.",
    "Advisory quality: app/staging.py adds unused imports: render_solo_system_prompt.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/bots/base.py, app/bots/coach.py, app/bots/prompts/tante_rosi.py, app/bots/tante_rosi.py, app/services/agentic.py, app/services/prompts.py, app/services/prompts_solo.py, app/staging.py, tests/test_eval_execution.py, tests/test_partner_sharing_prompt.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/",
    "Advisory audit finding: Sense check SC13 is missing an executor acknowledgment.",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T13, T14",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: tests/conftest.py, tests/test_hot_context.py, tests/test_hot_context_join_cutover.py, tests/test_partner_sharing_migration.py, tests/test_pregnancy_hot_context.py, tests/test_pregnancy_tools.py, tests/test_tools.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/",
    "Advisory audit finding: Sense check SC14 is missing an executor acknowledgment.",
    "Advisory audit finding: Tasks left pending after execute (executor never started them): T14",
    "Advisory quality: tests/test_coach_e2e.py has similar functions __init__ and __init__ (100% similarity).",
    "Advisory quality: tests/test_messaging_non_agentic_bot_id.py has similar functions fake_send_text and fake_send_text (100% similarity).",
    "Advisory quality: tests/test_cross_topic_peek_wired.py adds unused imports: BotSpec, ReadScopes, WriteScopes.",
    "Advisory quality: tests/test_cross_topic_status_injection.py adds unused imports: fetch_cross_topic_status.",
    "Advisory quality: tests/test_hot_context_cross_topic.py adds unused imports: asdict.",
    "Advisory quality: tests/test_multi_topic_writes.py adds unused imports: UUID.",
    "Advisory quality: tests/test_per_bot_telemetry.py adds unused imports: UTC, datetime.",
    "Advisory quality: tests/test_pregnancy_user_model.py adds unused imports: pytest.",
    "Advisory observation mismatch: git status/content hash delta found unclaimed files: app/models/user.py, app/services/hot_context.py, tests/test_coach_e2e.py, tests/test_cross_topic_peek_wired.py, tests/test_cross_topic_status_injection.py, tests/test_hot_context.py, tests/test_hot_context_cross_topic.py, tests/test_messaging_non_agentic_bot_id.py, tests/test_multi_topic_writes.py, tests/test_per_bot_telemetry.py, tests/test_pregnancy_user_model.py, tests/test_tools.py, tests/test_write_tools_solo_bot_guard.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/"
  ],
  "task_updates": [
    {
      "task_id": "T4",
      "status": "done",
      "executor_notes": "Replaced the legacy sharing-state write surface with set_partner_sharing in the root schema/registry/scope guard/write tool path. The new schema accepts only opt_in plus optional reason and forbids user_id/bot_id overrides; write_tools.set_partner_sharing writes via app.services.partner_sharing.set_partner_share for ctx.user.id and ctx.bot_id only and rejects missing bot scope. Updated bridge candidate readiness and media explain visibility within write_tools to consult per-bot partner_share instead of the dropped users.cross_thread_sharing_default. Confirmed mediator default registry, Rosi/coach allowlists, and generic record/write steps include set_partner_sharing; grep found no update_cross_thread_sharing_default or old users sharing-column write/read references in the T4 production files. Focused tests passed; full pytest still fails in the same prior unrelated tests/test_agentic.py and tests/test_decay.py failures noted by earlier batches.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/registry.py",
        "app/services/tools/scope_guard.py",
        "tests/test_tools.py",
        "tests/conftest.py"
      ],
      "commands_run": [
        "python -m black app/services/tools/write_tools.py tests/test_tools.py tests/conftest.py",
        "python -m py_compile tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py tests/conftest.py tests/test_tools.py",
        "rg -n \"update_cross_thread_sharing_default|UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|ctx\\.(user|partner)\\.cross_thread_sharing_default|UpdateCrossThreadSharingDefault\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_tools.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T5",
      "status": "done",
      "executor_notes": "Ran the stale-reference sweep across app, tests, and tool_schemas.py. Removed production reads of users.cross_thread_sharing_default from hot_context.py and read_tools.py by loading per-bot user_bot_state.partner_share through app.services.partner_sharing, updated raw privacy terminology from sharing_default to partner_share, and replaced stale mediator prompt references to update_cross_thread_sharing_default with set_partner_sharing/partner_share language. The production sweep now has no old tool references and no dropped-column DB dependence; the only app hit is the explicitly temporary non-hydrated User.cross_thread_sharing_default compatibility shim from T3. Remaining sweep hits are tests/fixtures that intentionally preserve legacy inputs until the T13 test-infrastructure cleanup. Full pytest still fails only in the same previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/staging.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py",
        "python -m py_compile app/services/cross_thread_privacy.py app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_pregnancy_persona.py tests/test_eval_execution.py tests/test_coach_e2e.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null
    },
    {
      "id": "T6",
      "status": "done",
      "executor_notes": "Completed the raw privacy terminology flip in app/services/cross_thread_privacy.py. RawMessageVisibility now reports partner_share instead of sharing_default, helper inputs use thread_owner_partner_share, redaction/omission strings refer to partner_share, and reason codes explicitly describe thread_owner_partner_share opt-in vs not-opted-in. Owner reads remain visible; partner reads are visible only for opt_in, while NULL/unset and opt_out block raw content. Focused modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m py_compile app/services/cross_thread_privacy.py tests/test_tools.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_6.json >/dev/null"
      ],
      "evidence_files": [
        ".megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_6.json"
      ],
      "auto_attributed_files": null,
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null,
      "task_id": "T6"
    },
    {
      "id": "T7",
      "status": "done",
      "kind": "code",
      "executor_notes": "Scoped raw-message reads to current bot/topic before privacy in hot_context and read_tools; keyed distillation visibility by recorded_by_bot_id with source-message bot fallback; scoped write-tool source-message visibility checks by bot/topic; and added regression coverage for mediator opt-in not exposing Rosi, legacy NULL, or other-topic raw messages. Focused modules passed. Full pytest was rerun and now fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "tests/conftest.py",
        "tests/test_agentic.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "python -m py_compile app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "python -m black tests/conftest.py tests/test_agentic.py",
        "python -m py_compile tests/test_agentic.py tests/conftest.py",
        "pytest tests/test_agentic.py tests/test_agentic_lifecycle.py tests/test_eval_execution.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_7.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        ".megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_7.json"
      ],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null,
      "task_id": "T7"
    },
    {
      "id": "T8",
      "status": "done",
      "kind": "code",
      "executor_notes": "Dyadic hot context now carries current/partner partner_share and partner_sharing_state, removes the hardcoded urgent/soft-nudge sharing prompt text, gates partner dyad_shareable distillation summaries on the owner's per-bot opt_in, and prevents partner private memories from rendering as full memories. Added a recency-ordered, globally capped partner-shareable summary section for opted-in non-current-bot memories/distillations with shared provenance prefixes. Focused hot-context/tool/lint modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py tests/conftest.py tests/test_hot_context.py",
        "python -m py_compile app/services/hot_context.py tests/conftest.py tests/test_hot_context.py",
        "pytest tests/test_hot_context.py -q",
        "python -m black tests/test_hot_context_join_cutover.py",
        "python -m py_compile app/services/hot_context.py tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_tools.py -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest tests/test_lint_artifact_reads.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_tools.py tests/test_partner_sharing.py tests/test_tool_schemas_importable.py tests/test_lint_artifact_reads.py -q",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_8.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        ".megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_8.json"
      ],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null,
      "task_id": "T8"
    },
    {
      "id": "T9",
      "status": "done",
      "executor_notes": "Solo hot context now loads current-bot partner_share, resolves dyad partner existence through the shared helper, emits partner_sharing_state='pending' only when a dyad partner exists and the current bot state is unset, and renders 'unavailable' when no partner exists. Regression coverage verifies pending/no-partner behavior and that solo context does not surface partner memories or raw messages. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context_solo.py",
        "tests/conftest.py",
        "tests/test_pregnancy_hot_context.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "task_id": "T9"
    },
    {
      "id": "T12",
      "status": "done",
      "executor_notes": "AddMemoryInput now accepts visibility/shareable_summary and rejects dyad_shareable memories without a non-empty shareable_summary. add_memory persists visibility, shareable_summary, encrypted summary, and recorded_by_bot_id. Memory read rows now carry visibility/shareable_summary, and get_memories/get_distillations gate partner-owned rows by the owner's per-bot partner_share and expose only shareable_summary for partner-visible artifacts. FakePool was updated for memory sharing fields and distillation recorded_by_bot_id. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/common.py",
        "tests/conftest.py",
        "tests/test_tool_schemas_importable.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "task_id": "T12"
    },
    {
      "id": "T10",
      "status": "done",
      "executor_notes": "Defined the canonical pending partner-sharing prompt slot once in app/bots/prompts/partner_sharing.py. The slot is neutral and domain-agnostic, tells the model to raise the choice naturally unless crisis/time-critical, explicitly forbids sharing this bot's rows until explicit opt-in, and instructs set_partner_sharing(opt_in=true/false) in the record step after an explicit choice. Added focused prompt content coverage. py_compile and focused prompt/persona/schema modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/prompts/partner_sharing.py",
        "tests/test_partner_sharing_prompt.py"
      ],
      "commands_run": [
        "rg -n \"partner_share|partner_sharing|set_partner_sharing|FIRST_CONTACT|sharing\" app/bots app/services/prompts.py app/services/prompts_solo.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_agentic.py tests/test_coach_e2e.py",
        "sed -n '1,220p' app/bots/prompts/tante_rosi.py",
        "sed -n '1,120p' app/bots/prompts/__init__.py",
        "git status --short",
        "python -m py_compile app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "if [ -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json ]; then echo writable; else echo not_writable; fi",
        "rg -n \"PENDING_PARTNER_SHARING_PROMPT_SLOT|set_partner_sharing\\(opt_in\" app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json >/dev/null"
      ],
      "task_id": "T10"
    },
    {
      "id": "T11",
      "status": "done",
      "executor_notes": "Wired current-bot partner_sharing_state from hot context through agentic/staging prompt construction and BotSpec.render_system_prompt into mediator, generic solo/coach, and Tante Rosi prompt renderers. Mediator and solo prompt paths now render the canonical pending slot only when partner_sharing_state='pending'; unavailable/no-partner states suppress it. Replaced the mediator unset prompt with the canonical slot and removed the opt-out re-ask/soft-nudge language. Tante Rosi now renders the canonical pending slot and adds Rosi-specific opt-in guidance for writing only non-sensitive pregnancy dyad_shareable memories/distillations with shareable_summary. Focused prompt, agentic/inbound, persona, schema, hot-context, partner-sharing, and pregnancy modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/services/agentic.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/staging.py",
        "tests/test_partner_sharing_prompt.py",
        "tests/test_eval_execution.py"
      ],
      "commands_run": [
        "python -m black app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "python -m py_compile app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/partner_sharing.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_agentic_lifecycle.py tests/test_inbound_source.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "rg -n \"update_cross_thread_sharing_default\" app/bots app/services/prompts.py app/services/prompts_solo.py || true",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_11.json >/dev/null"
      ],
      "task_id": "T11"
    },
    {
      "id": "T13",
      "status": "done",
      "executor_notes": "Updated fake pool/test fixtures away from the dropped users.cross_thread_sharing_default DB paths in the affected partner-sharing modules; hot-context/read-tool tests now seed per-bot user_bot_state.partner_share directly for opt-in/opt-out cases. Added migration SQL regression coverage for transactional ordering, Tante Rosi seed, mediator non-NULL backfill before legacy-column drop, partner_share constraint, and memory visibility/shareable_summary constraints/indexes. Extended read-tool privacy assertions to cover NULL, opt_out, opt_in+private, and opt_in+dyad_shareable behavior. Verified focused partner-sharing/hot-context/tool/prompt/migration modules passed, adjacent fixture modules passed, and full pytest was run; full suite still fails only in the previously documented three tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "tests/conftest.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py",
        "tests/test_pregnancy_hot_context.py",
        "tests/test_pregnancy_tools.py",
        "tests/test_tools.py",
        "tests/test_partner_sharing_migration.py"
      ],
      "commands_run": [
        "rg -n \"partner_share|partner_sharing_state|dyad_shareable|shareable_summary|cross_thread_sharing_default|TANTE_ROSI|tante_rosi|raw-message|raw message|no partner|migration|0035\" tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_tools.py tests/test_tool_schemas_importable.py tests/test_partner_sharing.py tests/test_partner_sharing_prompt.py tests/conftest.py tests/test_pregnancy_persona.py tests/test_pregnancy_tools.py migrations/0035_per_bot_partner_sharing.sql",
        "python -m black tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py tests/test_partner_sharing_migration.py",
        "python -m py_compile tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py tests/test_partner_sharing_migration.py",
        "pytest tests/test_partner_sharing_migration.py tests/test_partner_sharing.py tests/test_partner_sharing_prompt.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py -q",
        "pytest -q",
        "rg -n \"UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|cross_thread_sharing_default\" tests/conftest.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_pregnancy_tools.py tests/test_tools.py",
        "test -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_12.json && echo writable || echo not_writable"
      ],
      "task_id": "T13"
    },
    {
      "id": "T14",
      "status": "done",
      "executor_notes": "Final verification completed. Production stale-reference sweeps for cross_thread_sharing_default/update_cross_thread_sharing_default and sharing_default terminology across app and tool_schemas.py are clean after removing the last User compatibility shim and hot-context legacy fallback. The throwaway per-bot leak reproduction script passed: Rosi opt_in surfaced only the Rosi shareable summary with provenance, mediator opt_out blocked mediator shareable rows, and raw cross-bot/opt-out content did not render; the script was deleted afterward. Focused schema/tool, hot-context/read, prompt/allowlist, migration, partner-sharing, pregnancy, and adjacent fixture modules passed. Full pytest was rerun and still fails only in the previously documented three tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/models/user.py",
        "app/services/hot_context.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py",
        "tests/test_cross_topic_status_injection.py",
        "tests/test_cross_topic_peek_wired.py",
        "tests/test_messaging_non_agentic_bot_id.py",
        "tests/test_coach_e2e.py",
        "tests/test_hot_context_cross_topic.py",
        "tests/test_write_tools_solo_bot_guard.py",
        "tests/test_pregnancy_user_model.py",
        "tests/test_multi_topic_writes.py",
        "tests/test_per_bot_telemetry.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py",
        "rg -n \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py",
        "python tmp_partner_sharing_repro.py",
        "python -m py_compile app/models/user.py app/services/hot_context.py tests/test_cross_topic_status_injection.py tests/test_cross_topic_peek_wired.py tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_hot_context_cross_topic.py tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_user_model.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tmp_partner_sharing_repro.py",
        "python -m black app/models/user.py app/services/hot_context.py tests/test_cross_topic_status_injection.py tests/test_cross_topic_peek_wired.py tests/test_messaging_non_agentic_bot_id.py tests/test_coach_e2e.py tests/test_hot_context_cross_topic.py tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_user_model.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py",
        "test ! -e tmp_partner_sharing_repro.py && echo deleted",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "test -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_13.json && echo writable || echo not_writable"
      ],
      "task_id": "T14"
    }
  ],
  "sense_check_acknowledgments": [
    {
      "sense_check_id": "SC4",
      "executor_note": "Yes. set_partner_sharing is the only sharing-state write tool in the T4 schema/registry/dispatch/scope files; its input forbids user_id or bot_id overrides, it writes only ctx.user.id plus ctx.bot_id through the shared partner_sharing helper, and registry/scope/allowlist checks show it is available to mediator, Tante Rosi, coach, and generic record/write paths."
    },
    {
      "sense_check_id": "SC5",
      "executor_note": "Yes. The sweep shows no production dependence on the dropped users column or old update_cross_thread_sharing_default tool. The only remaining app hit is the T3 temporary non-hydrated User compatibility shim; remaining cross_thread_sharing_default/current_user_sharing_default/partner_sharing_default/sharing_default hits are test fixtures or legacy test call shapes scheduled for T13 cleanup."
    },
    {
      "id": "SC6",
      "executor_note": "Yes. raw_message_visibility() keeps same-owner raw reads visible regardless of partner_share, and partner raw reads now depend only on the thread owner's partner_share value supplied for that message bot. NULL/unset and opt_out normalize to hidden with raw_partner_content_hidden_by_partner_share; only opt_in allows partner raw visibility.",
      "sense_check_id": "SC6"
    },
    {
      "id": "SC7",
      "executor_note": "Yes. Mediator raw-read paths now require the current mediator bot_id and active topic before privacy, so Rosi messages, other-topic mediator messages, and explicit legacy NULL bot_id rows are excluded from hot context, search_messages, and recent_activity even when mediator partner_share is opt_in.",
      "sense_check_id": "SC7"
    },
    {
      "id": "SC8",
      "executor_note": "Yes. Dyadic hot context now exposes partner_sharing_state for current/partner users, removes the hardcoded prompt block, pulls only opted-in partner dyad_shareable summaries from non-current bots, renders them with shared provenance prefixes, orders candidates by recency, and caps rendered cross-bot summaries at 12 total.",
      "sense_check_id": "SC8"
    },
    {
      "id": "SC9",
      "executor_note": "Yes. Solo hot context resolves dyad partner existence through the shared helper, emits pending only for the current user/current bot when a dyad partner exists and partner_share is unset, suppresses pending as unavailable without a partner, and regression tests verify partner raw messages and partner memories are absent from solo context.",
      "sense_check_id": "SC9"
    },
    {
      "id": "SC12",
      "executor_note": "Yes. add_memory rejects blank/missing shareable_summary for dyad_shareable, persists and encrypts memory summaries, records the calling bot id, and read paths now expose only shareable_summary for partner-visible memory/distillation rows while own rows retain full content.",
      "sense_check_id": "SC12"
    },
    {
      "id": "SC10",
      "executor_note": "Yes. The pending slot is defined once in app/bots/prompts/partner_sharing.py, contains no Rosi/mediator/pregnancy/relationship-specific language, and explicitly covers crisis/time-critical deferral, no sharing before opt-in, and set_partner_sharing(opt_in=true/false) after an explicit choice.",
      "sense_check_id": "SC10"
    },
    {
      "id": "SC11",
      "executor_note": "Yes. Mediator, Tante Rosi, coach, and generic solo prompt render paths all receive partner_sharing_state and render the canonical pending slot only from that pending state; no prompt-path update_cross_thread_sharing_default references remain, and Rosi alone has opt-in guidance for safe pregnancy dyad_shareable summary writes.",
      "sense_check_id": "SC11"
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "executor_note": "Yes. Updated tests cover NULL and opt_out as silent, opt_in+private as hidden, opt_in+dyad_shareable as summary-only visible, independent per-bot gates through cross-bot Rosi/coach cases, raw-message bot isolation, no-partner prompt suppression, scoped Rosi set_partner_sharing success, memory validation, and migration SQL ordering/constraints.",
      "verdict": "acknowledged",
      "sense_check_id": "SC13"
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "executor_note": "Yes. Final production sweeps have no stale sharing references, the focused pytest modules passed, the throwaway reproduction script passed and was deleted, and the full suite was rerun with only the known unrelated three tests/test_decay.py fake-pool observation UPDATE failures remaining.",
      "verdict": "acknowledged",
      "sense_check_id": "SC14"
    }
  ],
  "files_changed": [
    "tool_schemas.py",
    "app/services/tools/write_tools.py",
    "app/services/tools/registry.py",
    "app/services/tools/scope_guard.py",
    "tests/test_tools.py",
    "tests/conftest.py",
    ".megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_4.json",
    "app/services/cross_thread_privacy.py",
    "app/services/hot_context.py",
    "app/services/tools/read_tools.py",
    "app/services/prompts.py",
    "app/services/prompts_solo.py",
    "app/bots/base.py",
    "app/bots/coach.py",
    "app/bots/tante_rosi.py",
    "app/bots/prompts/tante_rosi.py",
    "app/staging.py",
    "tests/test_hot_context.py",
    "tests/test_hot_context_join_cutover.py",
    ".megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_5.json"
  ]
}

        Execution audit (`execution_audit.json`):
            {
  "findings": [
    "Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/"
  ],
  "files_in_diff": [
    "app/bots/base.py",
    "app/bots/coach.py",
    "app/bots/ids.py",
    "app/bots/prompts/partner_sharing.py",
    "app/bots/prompts/tante_rosi.py",
    "app/bots/registry.py",
    "app/bots/tante_rosi.py",
    "app/models/user.py",
    "app/services/agentic.py",
    "app/services/cross_thread_privacy.py",
    "app/services/hot_context.py",
    "app/services/hot_context_solo.py",
    "app/services/partner_sharing.py",
    "app/services/prompts.py",
    "app/services/prompts_solo.py",
    "app/services/tools/common.py",
    "app/services/tools/read_tools.py",
    "app/services/tools/registry.py",
    "app/services/tools/scope_guard.py",
    "app/services/tools/write_tools.py",
    "app/services/turn_context.py",
    "app/staging.py",
    "megaplans/",
    "migrations/0035_per_bot_partner_sharing.sql",
    "scripts/import_chatgpt.py",
    "supabase/",
    "tests/conftest.py",
    "tests/test_agentic.py",
    "tests/test_coach_e2e.py",
    "tests/test_cross_topic_peek_wired.py",
    "tests/test_cross_topic_status_injection.py",
    "tests/test_eval_execution.py",
    "tests/test_hot_context.py",
    "tests/test_hot_context_cross_topic.py",
    "tests/test_hot_context_join_cutover.py",
    "tests/test_messaging_non_agentic_bot_id.py",
    "tests/test_multi_topic_writes.py",
    "tests/test_partner_sharing.py",
    "tests/test_partner_sharing_migration.py",
    "tests/test_partner_sharing_prompt.py",
    "tests/test_per_bot_telemetry.py",
    "tests/test_pregnancy_hot_context.py",
    "tests/test_pregnancy_tools.py",
    "tests/test_pregnancy_user_model.py",
    "tests/test_tool_schemas_importable.py",
    "tests/test_tools.py",
    "tests/test_write_tools_solo_bot_guard.py",
    "tool_schemas.py"
  ],
  "files_claimed": [
    "app/bots/base.py",
    "app/bots/coach.py",
    "app/bots/ids.py",
    "app/bots/prompts/partner_sharing.py",
    "app/bots/prompts/tante_rosi.py",
    "app/bots/registry.py",
    "app/bots/tante_rosi.py",
    "app/models/user.py",
    "app/services/agentic.py",
    "app/services/cross_thread_privacy.py",
    "app/services/hot_context.py",
    "app/services/hot_context_solo.py",
    "app/services/partner_sharing.py",
    "app/services/prompts.py",
    "app/services/prompts_solo.py",
    "app/services/tools/common.py",
    "app/services/tools/read_tools.py",
    "app/services/tools/registry.py",
    "app/services/tools/scope_guard.py",
    "app/services/tools/write_tools.py",
    "app/services/turn_context.py",
    "app/staging.py",
    "migrations/0035_per_bot_partner_sharing.sql",
    "tests/conftest.py",
    "tests/test_agentic.py",
    "tests/test_coach_e2e.py",
    "tests/test_cross_topic_peek_wired.py",
    "tests/test_cross_topic_status_injection.py",
    "tests/test_eval_execution.py",
    "tests/test_hot_context.py",
    "tests/test_hot_context_cross_topic.py",
    "tests/test_hot_context_join_cutover.py",
    "tests/test_messaging_non_agentic_bot_id.py",
    "tests/test_multi_topic_writes.py",
    "tests/test_partner_sharing.py",
    "tests/test_partner_sharing_migration.py",
    "tests/test_partner_sharing_prompt.py",
    "tests/test_per_bot_telemetry.py",
    "tests/test_pregnancy_hot_context.py",
    "tests/test_pregnancy_tools.py",
    "tests/test_pregnancy_user_model.py",
    "tests/test_tool_schemas_importable.py",
    "tests/test_tools.py",
    "tests/test_write_tools_solo_bot_guard.py",
    "tool_schemas.py"
  ],
  "skipped": false,
  "reason": ""
}

        Git diff summary:
        M app/bots/base.py
 M app/bots/coach.py
 M app/bots/ids.py
 M app/bots/prompts/tante_rosi.py
 M app/bots/registry.py
 M app/bots/tante_rosi.py
 M app/models/user.py
 M app/services/agentic.py
 M app/services/cross_thread_privacy.py
 M app/services/hot_context.py
 M app/services/hot_context_solo.py
 M app/services/prompts.py
 M app/services/prompts_solo.py
 M app/services/tools/common.py
 M app/services/tools/read_tools.py
 M app/services/tools/registry.py
 M app/services/tools/scope_guard.py
 M app/services/tools/write_tools.py
 M app/services/turn_context.py
 M app/staging.py
 M tests/conftest.py
 M tests/test_agentic.py
 M tests/test_coach_e2e.py
 M tests/test_cross_topic_peek_wired.py
 M tests/test_cross_topic_status_injection.py
 M tests/test_eval_execution.py
 M tests/test_hot_context.py
 M tests/test_hot_context_cross_topic.py
 M tests/test_hot_context_join_cutover.py
 M tests/test_messaging_non_agentic_bot_id.py
 M tests/test_multi_topic_writes.py
 M tests/test_per_bot_telemetry.py
 M tests/test_pregnancy_hot_context.py
 M tests/test_pregnancy_tools.py
 M tests/test_pregnancy_user_model.py
 M tests/test_tool_schemas_importable.py
 M tests/test_tools.py
 M tests/test_write_tools_solo_bot_guard.py
 M tool_schemas.py
?? app/bots/prompts/partner_sharing.py
?? app/services/partner_sharing.py
?? megaplans/
?? migrations/0035_per_bot_partner_sharing.sql
?? scripts/import_chatgpt.py
?? supabase/
?? tests/test_partner_sharing.py
?? tests/test_partner_sharing_migration.py
?? tests/test_partner_sharing_prompt.py

        Requirements:
        - Verify each success criterion explicitly.
        - Trust executor evidence by default. Dig deeper only where the git diff, `execution_audit.json`, or vague notes make the claim ambiguous.
        - Each criterion has a `priority` (`must`, `should`, or `info`). Apply these rules:
          - `must` criteria are hard gates. A `must` criterion that fails means `needs_rework`.
          - `should` criteria are quality targets. If the spirit is met but the letter is not, mark `pass` with evidence explaining the gap. Only mark `fail` if the intent was clearly missed. A `should` failure alone does NOT require `needs_rework`.
          - `info` criteria are for human reference. Mark them `waived` with a note — do not evaluate them.
          - If a criterion has `requires` capabilities that are not satisfiable by container workers (e.g., `drive_browser`, `subjective_judgment`), mark it `deferred_human` — NOT `fail` or `waived`. Deferred-human criteria do NOT count toward `needs_rework`.
          - If a criterion (any priority) cannot be verified in this context (e.g., requires manual testing or runtime observation), mark it `waived` with an explanation.
        - Set `review_verdict` to `needs_rework` only when at least one `must` criterion fails or actual implementation work is incomplete. Use `approved` when all `must` criteria pass, even if some `should` criteria are flagged.
        - The decisions listed above were settled at the gate stage. Verify that the executor implemented each settled decision correctly. Flag deviations from these decisions, but do not question the decisions themselves.
        - baseline_test_failures in finalize.json lists tests that were already failing before execution. Do not flag these as rework items unless the executor introduced new failures in those same tests.
        - Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.
        - Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.
        - Follow this JSON shape exactly:
        ```json
        {
          "review_verdict": "approved",
          "criteria": [
            {
              "name": "All existing tests pass",
              "priority": "must",
              "pass": "pass",
              "evidence": "Test suite ran green — 42 passed, 0 failed."
            },
            {
              "name": "File under ~300 lines",
              "priority": "should",
              "pass": "pass",
              "evidence": "File is 375 lines — above the target but reasonable given the component's responsibilities. Spirit met."
            },
            {
              "name": "Manual smoke tests pass",
              "priority": "info",
              "pass": "waived",
              "evidence": "Cannot be verified in automated review. Noted for manual QA."
            }
          ],
          "issues": [],
          "rework_items": [],
          "summary": "Approved. All must criteria pass. The should criterion on line count is close enough given the component scope.",
          "task_verdicts": [
            {
              "task_id": "T6",
              "reviewer_verdict": "Pass. Claimed handler changes and command evidence match the repo state.",
              "evidence_files": ["megaplan/handlers.py", "megaplan/evaluation.py"]
            }
          ],
          "sense_check_verdicts": [
            {
              "sense_check_id": "SC6",
              "verdict": "Confirmed. The execute blocker only fires when both evidence arrays are empty."
            }
          ]
        }
        ```
        - `rework_items` must be an array of structured rework directives. When `review_verdict` is `needs_rework`, populate one entry per issue with:
          - `task_id`: which finalize task this issue relates to
          - `issue`: what is wrong
          - `expected`: what correct behavior looks like
          - `actual`: what was observed
          - `evidence_file` (optional): file path supporting the finding
          - `flag_id`: critique/review flag ID when applicable, otherwise `null`
          - `source`: short machine-readable source tag when applicable, otherwise `null`
        - `issues` must still be populated as a flat one-line-per-item summary derived from `rework_items` (for backward compatibility). When approved, both `issues` and `rework_items` should be empty arrays.
        - When the work needs another execute pass, keep the same shape and change only `review_verdict` to `needs_rework`; make `issues`, `rework_items`, `summary`, and task verdicts specific enough for the executor to act on directly.

> AGENT

{"review_verdict":"needs_rework","checks":null,"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9072, expected≈10, ratio=907.20, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":[],"disputed_flag_ids":[],"criteria":[],"issues":["Review not completed yet; gathering evidence from final diff."],"rework_items":[],"summary":"Starting verification against the diff and success criteria.","task_verdicts":[],"sense_check_verdicts":[]}

> AGENT

{"review_verdict":"needs_rework","checks":null,"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9072, expected≈10, ratio=907.20, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":[],"disputed_flag_ids":[],"criteria":[],"issues":["Review in progress; reading the relevant diff and targeted files before deciding."],"rework_items":[],"summary":"I am checking the implementation evidence directly against the code, especially the migration, stale references, hot-context privacy paths, prompt inheritance, and tool schema/write behavior.","task_verdicts":[],"sense_check_verdicts":[]}

> AGENT

{"review_verdict":"needs_rework","checks":null,"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9072, expected≈10, ratio=907.20, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":[],"disputed_flag_ids":[],"criteria":[],"issues":["Review still in progress; targeted checks are passing so far, but I am digging into read-path scoping and migration semantics before issuing a verdict."],"rework_items":[],"summary":"The stale-reference sweep is clean and the migration/test prompt files exist. I am now checking for semantic gaps in hot-context and read-tool privacy behavior rather than just matching names.","task_verdicts":[],"sense_check_verdicts":[]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "git diff --stat && git status --short",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py || true",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' migrations/0035_per_bot_partner_sharing.sql",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,260p' app/services/partner_sharing.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"partner_share|partner_sharing_state|shareable|raw_message_visibility|bot_id|topic_id|CROSS_BOT|cap|MAX\" app/services/hot_context.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"set_partner_sharing|AddMemoryInput|visibility|shareable_summary|update_cross\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/read_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,220p' app/bots/prompts/partner_sharing.py && rg -n \"PENDING_PARTNER|partner_sharing_state|partner_share\" app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,240p' app/services/cross_thread_privacy.py && rg -n \"partner_share|raw_message_visibility|bot_id|topic_id\" app/services/tools/read_tools.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '220,330p' app/services/hot_context.py && sed -n '650,830p' app/services/hot_context.py && sed -n '840,950p' app/services/hot_context.py && sed -n '1210,1240p' app/services/hot_context.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '80,145p' app/services/tools/read_tools.py && sed -n '360,440p' app/services/tools/read_tools.py && sed -n '560,610p' app/services/tools/read_tools.py && sed -n '700,765p' app/services/tools/read_tools.py && sed -n '890,950p' app/services/tools/read_tools.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '230,275p' app/services/tools/write_tools.py && sed -n '860,915p' app/services/tools/write_tools.py && sed -n '1300,1345p' app/services/tools/write_tools.py && sed -n '2330,2365p' app/services/tools/write_tools.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '740,770p' tool_schemas.py && sed -n '865,895p' tool_schemas.py && sed -n '1028,1058p' tool_schemas.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '1,120p' migrations/0022_topic_status_user_bot_state.sql && sed -n '1,80p' migrations/0020_topics_bots_bindings.sql && sed -n '1,120p' migrations/0015_distillations.sql",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"class User|cross_thread|sharing_default|partner_share\" app/models/user.py app/services/turn_context.py app/staging.py app/services/agentic.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"TANTE_ROSI_BOT_ID|tante_rosi|mediator\" app/bots/ids.py app/bots/registry.py app/bots/tante_rosi.py app/bots/coach.py app/services/tools/registry.py app/services/tools/scope_guard.py tests/test_tools.py tests/test_partner_sharing_migration.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_partner_sharing_migration.py tests/test_partner_sharing.py tests/test_partner_sharing_prompt.py tests/test_tool_schemas_importable.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> AGENT

{"review_verdict":"needs_rework","checks":null,"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9072, expected≈10, ratio=907.20, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":["FLAG-001","FLAG-002","FLAG-003","FLAG-004","FLAG-005"],"disputed_flag_ids":["verifiability-0","verifiability-1"],"criteria":[{"name":"Migration seeds Tante Rosi bot row before Rosi partner-share writes","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql:1-18 runs in one transaction, inserts bots(id='tante_rosi') before user_bot_state.partner_share work, and tests/test_partner_sharing_migration.py asserts the seed."},{"name":"Migration adds partner_share and backfills mediator non-NULL legacy values before dropping old column","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql:11-44 adds constrained partner_share and backfills users.cross_thread_sharing_default into mediator user_bot_state rows before the drop block at the end."},{"name":"Migration adds memory visibility/shareable-summary fields and CHECK","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql:50-83 adds memories.visibility, shareable_summary, shareable_summary_encrypted, visibility CHECK, non-empty dyad_shareable summary CHECK, and supporting indexes."},{"name":"Production code has no remaining users.cross_thread_sharing_default or old tool path","priority":"must","pass":"pass","evidence":"`rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py` returned no matches in this review."},{"name":"User/turn/staging/prompt/tool paths use per-bot partner_share or no sharing field","priority":"must","pass":"pass","evidence":"app/models/user.py and app/services/turn_context.py no longer match stale sharing terms; app/staging.py and app/services/agentic.py load partner share via app.services.partner_sharing.get_partner_share."},{"name":"Raw message reads are same-bot/topic scoped before partner visibility","priority":"must","pass":"pass","evidence":"app/services/hot_context.py:670-684 filters messages by bot_id and topic_id. app/services/tools/read_tools.py search/recent activity paths also add bot_id/topic_id clauses and re-check current scope."},{"name":"raw_message_visibility and callers use owner partner_share for relevant bot","priority":"must","pass":"pass","evidence":"app/services/cross_thread_privacy.py uses thread_owner_partner_share and treats unset/opt_out as hidden; read/write/hot-context callers load per-bot state from user_bot_state helpers."},{"name":"Partner hot context includes opted-in shareable summaries with provenance","priority":"must","pass":"fail","evidence":"app/services/hot_context.py:276-314 applies LIMIT 48 before checking partner_share, then filters opt-in rows in Python. If 48 newer dyad_shareable rows belong to non-opted-in bots, older opted-in rows are never considered, so the partner can miss content from opted-in bots despite the post-filter cap."},{"name":"Hot context emits pending only when current user has partner and current bot state is NULL/missing","priority":"must","pass":"pass","evidence":"app/services/hot_context.py:478-482 computes pending for dyadic context; app/services/hot_context_solo.py coverage passed in focused tests and suppresses pending without dyad partner."},{"name":"Canonical pending prompt slot defined once and used by mediator/Rosi/generic solo coach","priority":"must","pass":"pass","evidence":"app/bots/prompts/partner_sharing.py defines PENDING_PARTNER_SHARING_PROMPT_SLOT; app/services/prompts.py, app/services/prompts_solo.py, app/bots/coach.py, and app/bots/tante_rosi.py route partner_sharing_state into prompt rendering."},{"name":"set_partner_sharing exists, is bot-scoped, and works for Tante Rosi/coach paths","priority":"must","pass":"pass","evidence":"tool_schemas.py defines SetPartnerSharingInput without user_id/bot_id; app/services/tools/write_tools.py:235-268 writes ctx.user.id plus ctx.bot_id; registry/scope guard include set_partner_sharing; tests/test_tools.py includes Rosi scoped write assertions."},{"name":"add_memory accepts visibility/shareable_summary, persists encrypted summary, rejects blank dyad_shareable summaries","priority":"must","pass":"pass","evidence":"tool_schemas.py:872-889 validates AddMemoryInput; app/services/tools/write_tools.py:872-907 persists visibility, shareable_summary, shareable_summary_encrypted, and recorded_by_bot_id. Focused schema/tool tests passed."},{"name":"TANTE_ROSI_BOT_ID exists and Python paths use constants where available","priority":"must","pass":"pass","evidence":"app/bots/ids.py defines TANTE_ROSI_BOT_ID; app/bots/tante_rosi.py and app/bots/registry.py import and use it. Remaining literals observed are mostly test data and SQL migration contents."},{"name":"Tests cover privacy matrix, cross-bot independence, raw isolation, no-partner suppression, and Rosi FK success","priority":"must","pass":"pass","evidence":"Focused regression command passed: 136 tests across test_tools, hot-context, pregnancy hot-context, partner_sharing, migration, and prompt coverage."},{"name":"Cross-bot partner content ordering and global cap are explicit","priority":"should","pass":"deferred_human","evidence":"Criterion includes subjective_judgment. Code documents recency ordering and a cap in app/services/hot_context.py:33-34 and 287-314, but the must criterion above found a semantic cap-before-gate bug that needs code rework."},{"name":"Prompt/hot-context labels consistently use partner_share terminology","priority":"should","pass":"deferred_human","evidence":"Criterion includes subjective_judgment. Literal stale-reference sweep is clean, though app/services/prompts.py keeps dynamically constructed compatibility kwarg fallbacks containing 'sharing_default' semantics."},{"name":"Future work for re-asking/per-topic granularity remains out of scope","priority":"info","pass":"waived","evidence":"Info criterion. Not evaluated as a merge gate; no opportunistic re-ask/per-topic implementation was evident in the reviewed files."}],"issues":["Cross-bot shareable summary fetch applies the SQL candidate LIMIT before filtering to opted-in bots, so non-opted-in rows can starve valid opted-in summaries."],"rework_items":[{"task_id":"T8","issue":"Cross-bot partner summary retrieval limits candidates before applying the owner/bot partner_share opt-in gate.","expected":"Build the cross-bot candidate set from the partner's opted-in bots first, then order opted-in memory/distillation summaries by recency and apply the fixed global cap. Non-opted-in bots must not be able to crowd opted-in rows out of the result window.","actual":"app/services/hot_context.py selects all dyad_shareable rows ordered by recency with LIMIT 48, then checks each row's partner_share in Python and stops after 12 accepted rows. A burst of newer rows from opt_out/unset bots can prevent older opted-in rows from being fetched at all.","evidence_file":"app/services/hot_context.py:276","flag_id":null,"source":"criteria_review"}],"summary":"Needs rework. Most schema, tool, prompt, and raw-message boundary requirements are implemented and the focused tests pass, but the cross-bot shareable-summary read path does not actually query opted-in bots first. That leaves a correctness hole where non-opted-in rows can starve valid opted-in partner summaries before the global cap is applied.","task_verdicts":[{"task_id":"T1","reviewer_verdict":"Pass. Migration and bot id constant are present; Tante Rosi is seeded before partner-share backfill/use.","evidence_files":["migrations/0035_per_bot_partner_sharing.sql","app/bots/ids.py"]},{"task_id":"T2","reviewer_verdict":"Pass. Shared helper module covers normalization, per-bot fetch/upsert, dyad partner resolution, and provenance fallback.","evidence_files":["app/services/partner_sharing.py"]},{"task_id":"T3","reviewer_verdict":"Pass. Production stale-reference sweep no longer finds the dropped users column or old tool names.","evidence_files":["app/models/user.py","app/services/turn_context.py","app/staging.py"]},{"task_id":"T4","reviewer_verdict":"Pass. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id and wired through schema/registry/scope guard.","evidence_files":["tool_schemas.py","app/services/tools/write_tools.py","app/services/tools/registry.py","app/services/tools/scope_guard.py"]},{"task_id":"T5","reviewer_verdict":"Pass. Final literal stale-reference sweep across app and tool_schemas.py is clean.","evidence_files":["app/services/prompts.py","app/services/tools/read_tools.py"]},{"task_id":"T6","reviewer_verdict":"Pass. Raw privacy helper now uses partner_share terminology and blocks unset/opt_out partner raw reads.","evidence_files":["app/services/cross_thread_privacy.py"]},{"task_id":"T7","reviewer_verdict":"Pass. Raw message queries are scoped by bot/topic in hot context and read tools.","evidence_files":["app/services/hot_context.py","app/services/tools/read_tools.py"]},{"task_id":"T8","reviewer_verdict":"Needs rework. Partner-shareable summaries are capped before opt-in filtering, so opted-in rows can be missed.","evidence_files":["app/services/hot_context.py"]},{"task_id":"T9","reviewer_verdict":"Pass. Solo hot context has partner_share/pending state and tests cover no partner-content exposure.","evidence_files":["app/services/hot_context_solo.py","tests/test_pregnancy_hot_context.py"]},{"task_id":"T10","reviewer_verdict":"Pass. Canonical pending prompt slot is defined once and is domain-neutral.","evidence_files":["app/bots/prompts/partner_sharing.py"]},{"task_id":"T11","reviewer_verdict":"Pass. Mediator, Rosi, coach, and generic solo prompt paths render the canonical slot from partner_sharing_state.","evidence_files":["app/services/prompts.py","app/services/prompts_solo.py","app/bots/tante_rosi.py","app/bots/coach.py"]},{"task_id":"T12","reviewer_verdict":"Pass. Memory schema/write path accepts and persists dyad_shareable summaries and validates missing summaries.","evidence_files":["tool_schemas.py","app/services/tools/write_tools.py"]},{"task_id":"T13","reviewer_verdict":"Pass. Focused fixture and regression tests exist and passed in review.","evidence_files":["tests/test_partner_sharing_migration.py","tests/test_tools.py","tests/test_hot_context.py"]},{"task_id":"T14","reviewer_verdict":"Needs rework. Final verification missed the cap-before-opt-in starvation case in the throwaway/focused scenarios.","evidence_files":["app/services/hot_context.py"]}],"sense_check_verdicts":[{"sense_check_id":"SC1","verdict":"Confirmed. Migration is transactional, seeds Tante Rosi, adds partner_share, backfills mediator, adds memory fields/checks, and drops the legacy column last."},{"sense_check_id":"SC2","verdict":"Confirmed. partner_sharing.py uses explicit (user_id, bot_id), dyad_members/dyads, and registry/DB/id provenance fallback."},{"sense_check_id":"SC3","verdict":"Confirmed for DB dependency. Stale production grep is clean for the dropped column."},{"sense_check_id":"SC4","verdict":"Confirmed. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id."},{"sense_check_id":"SC5","verdict":"Confirmed. Final literal stale-reference sweep is clean."},{"sense_check_id":"SC6","verdict":"Confirmed. raw_message_visibility preserves owner reads and blocks unset/opt_out partner reads."},{"sense_check_id":"SC7","verdict":"Confirmed. Hot-context/read-tool raw message paths add bot/topic scope."},{"sense_check_id":"SC8","verdict":"Not confirmed. The code comment says capped after opt-in filtering, but SQL LIMIT happens before partner_share filtering, allowing non-opted-in rows to crowd out opted-in summaries."},{"sense_check_id":"SC9","verdict":"Confirmed. Solo hot context pending/no-partner behavior is implemented and covered."},{"sense_check_id":"SC10","verdict":"Confirmed. Canonical slot is defined once and references set_partner_sharing after explicit choice."},{"sense_check_id":"SC11","verdict":"Confirmed. Prompt paths render the canonical slot via partner_sharing_state."},{"sense_check_id":"SC12","verdict":"Confirmed. add_memory validates and persists shareable summaries, including encrypted summary storage."},{"sense_check_id":"SC13","verdict":"Mostly confirmed. Existing focused tests cover the named matrix, but they do not cover candidate starvation by non-opted-in rows."},{"sense_check_id":"SC14","verdict":"Not confirmed. Final reproduction did not exercise the cap-before-opt-in starvation bug in cross-bot summary retrieval."}]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py tests/test_partner_sharing_prompt.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 50000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"partner_shareable|dyad_shareable|raw|tante_rosi|opt_out|opt_in|no partner|pending\" tests/test_hot_context.py tests/test_tools.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing_prompt.py tests/test_partner_sharing_migration.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"cross_thread|sharing_default|partner_share|update_cross|set_partner_sharing\" app/models/user.py app/services/turn_context.py app/staging.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"CROSS_BOT_SHAREABLE|Partner shareable summaries|provenance|recency|cap|capped\" app/services/hot_context.py tests/test_hot_context.py tests/test_partner_sharing.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba app/services/hot_context.py | sed -n '231,315p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba app/services/prompts.py | sed -n '440,455p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba migrations/0035_per_bot_partner_sharing.sql | sed -n '1,90p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba app/services/hot_context.py | sed -n '670,690p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

Review the implementation against the success criteria.

        Project directory:
        /Users/user_c042661f/Documents/Veas

        Idea:
# Per-bot partner sharing — design brief

## Context

The Veas codebase runs N bots that each occupy a "domain" for a user (currently: `mediator` = relationship coach for a dyad on topic=relationship; `tante_rosi` = solo pregnancy coach on topic=pregnancy; more bots planned). Today only the mediator's content can flow between dyad partners, gated by a **global** opt-in (`users.cross_thread_sharing_default`). The pregnancy coach writes everything private; her facts cannot reach the partner even when the user wants to share them.

We want to generalise partner-sharing so that **every bot** (current and future) can produce content that the user's partner sees, gated by a **per-bot** opt-in. The user gets one switch per domain ("share my pregnancy stuff with my partner — yes / no / not decided yet"). Until they decide, the bot keeps surfacing the question.

The basic infrastructure already exists for distillations (`visibility: private | dyad_shareable`, `shareable_summary`, `raw_message_visibility()` filtering in `app/services/cross_thread_privacy.py`, `app/services/hot_context.py:500-577`). The work below generalises it across both bots-and-content-types, and replaces the global toggle with a per-bot one.

## Goal (one sentence)

Replace the single global `users.cross_thread_sharing_default` with per-bot opt-in state on `user_bot_state`, extend `dyad_shareable` visibility to `memories` (today it only exists on `distillations`), and rewire the hot-context read path so a partner sees `dyad_shareable` content from any bot where the content's owner has opted in for *that* bot — with NULL ("not decided") triggering a prompt-slot the bot uses to ask.

## Decisions already made (do not re-litigate)

These are settled — the plan should implement them, not re-debate them.

1. **Per-bot opt-in lives on `user_bot_state`** as one new column `partner_share text` with values `'opt_in' | 'opt_out' | NULL`. NULL = "pending, must ask". Key is `(user_id, bot_id)` — same shape as every other per-bot state today.
2. **Memories get `visibility` and `shareable_summary`** mirroring distillations exactly. Default `visibility='private'`. When `visibility='dyad_shareable'`, `shareable_summary` is required.
3. **The opt-in is shown until decided.** While `partner_share IS NULL`, every render of that bot's hot context includes a "pending opt-in" slot in the system prompt asking the bot to raise the question this turn. As soon as the value is non-NULL (`opt_in` OR `opt_out`), the slot drops out and the bot stops raising it.
4. **One shared prompt slot, used by every bot.** Define one canonical pending-opt-in paragraph used by every bot's `render_system_prompt`. Rosi's existing `_FIRST_CONTACT_V1` collapses into it; the mediator's onboarding language for cross-thread sharing also collapses into it. New bots inherit the slot for free — no per-bot prompt work.
5. **One shared tool: `set_partner_sharing(opt_in: bool)`.** Implicit `bot_id` (from the calling bot's scope). Writes to `user_bot_state.partner_share` for the calling (user, bot) pair.
6. **Migration: the existing global flag goes away.** Backfill `user_bot_state[bot_id='mediator', user_id=X].partner_share` from `users.cross_thread_sharing_default` for every existing user, then drop `users.cross_thread_sharing_default`. One model, not two — no fallback path, no two-system-running period.
7. **No per-row UX in v1.** The user gets the per-bot toggle. The bot decides per-call whether a given memory/distillation should be `private` vs `dyad_shareable` based on the content. No user-facing per-row controls.
8. **Hot context cross-bot pull is in scope.** When rendering for user B (the partner of A), pull A's `dyad_shareable` rows from *any* bot where `partner_share[A, that_bot] = 'opt_in'`, surfaced with a provenance prefix (e.g. `from Rosi:`). Same-bot dyad sharing (the existing mediator behaviour) keeps working unchanged in shape, just driven by the new column.

## Files known to be relevant (planner should read at least these)

The planner should still survey the repo, but these are the focal points:

- `migrations/0012_cross_thread_sharing.sql` — defines the global flag being retired.
- `migrations/0015_distillations.sql` — defines `visibility` + `shareable_summary` we're mirroring onto memories.
- `migrations/0022_topic_status_user_bot_state.sql` — defines `user_bot_state` (current schema: `user_id, bot_id, onboarding_state, paused`).
- The next available migration number is `0020` (or whatever is highest after `0019_feedback_reaction_context.sql`); planner should verify.
- `app/services/cross_thread_privacy.py` — `raw_message_visibility()` lives here; needs to flip from global flag to per-bot lookup.
- `app/services/hot_context.py` (especially lines 500-577) — read path; needs (a) per-bot lookup, (b) cross-bot pull for partner, (c) emitting the `partner_sharing_state: 'pending'` signal.
- `app/services/tools/write_tools.py` — `add_memory` (~line 776) and `add_distillation` (~line 1165). The `add_memory` write helper needs to accept `visibility` + `shareable_summary`.
- `app/services/tools/tool_schemas.py` — `AddMemoryInput` needs new fields mirroring `AddDistillationInput.visibility` etc. (~line 996 for the distillation schema as the template).
- `app/bots/mediator.py` and `app/bots/tante_rosi.py` — both need to (a) include the canonical pending-opt-in slot via their `render_system_prompt`, (b) be eligible to call `set_partner_sharing`. Rosi additionally needs prompt language about *when* to write `dyad_shareable` rows once opted in.
- `app/bots/prompts/tante_rosi.py` (`_FIRST_CONTACT_V1`) and the equivalent mediator prompt file — the canonical slot replaces/absorbs whatever a[REDACTED_SK] language already exists in each.
- `app/bots/` tool dispatch — wherever bot tool allowlists are wired, `set_partner_sharing` must be available to every bot (it's user-state-modifying, like `set_pregnancy_edd`, not domain-specific).

## Invariants to enforce (must hold)

1. **NULL → silent.** When `partner_share IS NULL`, *no* content from that (user, bot) is shared with the partner regardless of per-row `visibility`. The toggle is the gate; per-row visibility only matters when the toggle is `opt_in`.
2. **opt_out → silent.** Same as NULL for the read path. The only difference is the prompt slot doesn't surface.
3. **opt_in → per-row decides.** When the toggle is `opt_in`, dyad_shareable rows from that bot flow to the partner; private rows don't.
4. **No partner → moot.** When the user has no partner (`users.partner_user_id IS NULL`), the prompt slot is suppressed even with `partner_share IS NULL`. Nothing to share to. Don't ask a question that has no answer.
5. **No backsliding on the mediator.** Every existing mediator user must continue to see exactly what they see today — the migration must be observationally equivalent. A user whose current `cross_thread_sharing_default = 'opt_in'` ends up with `user_bot_state[mediator].partner_share = 'opt_in'`; a user with `'opt_out'` ends up `'opt_out'`; NULL stays NULL.
6. **Cross-bot pull is opt-in-gated, not opt-out-gated.** Default is "don't show partner's other-bot content." Only `'opt_in'` from the content owner unlocks the pull. This matters: a partner who hasn't decided cannot accidentally have their content surfaced because of someone *else's* default.
7. **Tool authorisation.** `set_partner_sharing` writes only to the calling user's row for the calling bot. A user calling Rosi cannot toggle their mediator state; Rosi cannot toggle Véas's state. Scope is `(message.sender_id, message.bot_id)`.
8. **The shareable_summary contract.** When `add_memory` or `add_distillation` is called with `visibility='dyad_shareable'`, `shareable_summary` must be non-null and non-empty. Reject the call otherwise. Same rule that already applies to distillations should now apply to memories.

## Edge cases and ordering concerns

The planner should treat these as real, not paranoid:

- **Migration backfill ordering.** The new column on `user_bot_state` must be added and backfilled before `cross_thread_sharing_default` is dropped. The hot-context read path must be flipped to the new column *atomically* with the drop, or the system briefly reads from a dropped column. Plan the migration as a single transaction or with explicit phasing.
- **Backfill for users without a `user_bot_state[mediator]` row.** Some legacy users may not have a `user_bot_state` row for the mediator yet (it may be created lazily on first message). The migration must create rows for any user with a non-NULL `cross_thread_sharing_default`. For users with NULL global setting, decide: either create rows pre-set to NULL (explicit pending state) or skip (lazy creation later, still NULL). Either is defensible — make a call and write it down.
- **The pending slot wording is shared.** Different bots have different voices. The shared slot must be voice-agnostic — short, neutral, instructive to the model, not user-facing copy. The bot's own voice handles the actual question to the user; the slot just tells the bot "raise this naturally this turn."
- **Cross-bot pull volume.** A partner with several opted-in bots could see a long list of "from X:" rows in their hot context. Budget for hot-context length: cap, summarise, or rank. Don't ship a context bomb.
- **Order of cross-bot content.** When pulling rows from multiple bots, by what order? By recency? By bot? Pick one and write it down so the reviewer can check it.
- **Provenance prefix format.** "from Rosi:" / "from Véas:" — bake into a single helper, not sprinkled. Bots are named via the bot registry; use the registry's display name, not a hard-coded string.

## Explicitly out of scope

- Per-row visibility controls exposed to the user. (The bot decides per-row; users only decide per-bot.)
- Re-asking after some time has passed. Once `opt_in` or `opt_out` is set, the slot stays gone. Future work, not this sprint.
- New bot registration code. The pattern must work for new bots when they show up, but we are not adding a new bot in this sprint.
- Per-topic granularity within a bot. Each bot is one domain; one toggle per bot is enough.
- UI surfaces. There is no UI today and we are not building one.
- Encryption-at-rest changes. `shareable_summary` on memories follows whatever the existing memory content encryption pattern is.

## Success criteria

Reviewer should check, in priority order:

**must**
- Migration adds `user_bot_state.partner_share` and backfills it from `users.cross_thread_sharing_default` for every user where the global flag was non-NULL, preserving the same value semantically (`'opt_in' → 'opt_in'`, `'opt_out' → 'opt_out'`).
- Migration adds `memories.visibility` (default `'private'`) and `memories.shareable_summary` (nullable) with a CHECK constraint matching the existing distillations one (`shareable_summary` required iff `visibility='dyad_shareable'`).
- Migration drops `users.cross_thread_sharing_default` only after the read path is updated.
- `cross_thread_privacy.raw_message_visibility()` (and any other reader of the old column) reads from `user_bot_state.partner_share` for the relevant bot, not from `users.cross_thread_sharing_default`.
- `hot_context.py` cross-bot pull lands: when rendering for partner B, B sees A's `dyad_shareable` memories and distillations from any bot where `partner_share[A, that_bot]='opt_in'`, with a provenance prefix from the bot registry.
- `hot_context.py` emits `partner_sharing_state: 'pending'` when `partner_share IS NULL` and the user has a partner; the canonical prompt slot is rendered into the system prompt of any bot whose hot context carries this signal.
- `set_partner_sharing` tool exists, is wired into the tool registry for every bot, and updates `user_bot_state.partner_share` for the calling `(user, bot)` only.
- `add_memory` accepts `visibility` and `shareable_summary`; rejects `dyad_shareable` without `shareable_summary`.
- Rosi's prompt is updated so that when `partner_share='opt_in'`, she writes `dyad_shareable` memories and distillations for non-sensitive facts (with appropriate `shareable_summary`).
- Mediator's existing partner-sharing onboarding language is collapsed into the canonical slot; mediator continues to behave observationally as today for existing users post-migration.
- Tests cover: NULL → no partner content visible; `opt_out` → no partner content visible; `opt_in` + `private` row → no partner content visible; `opt_in` + `dyad_shareable` row → partner content visible with provenance; cross-bot pull respects toggle independently per bot; user with no partner never sees the pending slot.

**should**
- Cross-bot content ordering and length budget are explicit (chosen rule, written down in code or comment).
- Migration is a single transaction or has explicit phasing documented.
- The canonical prompt slot is defined in one place and imported by both bot prompt files.

**info**
- Future work for re-asking or per-topic granularity is captured (e.g., as a ticket via `megaplan ticket new`) but not implemented.

## Notes for the planner

- **Do not invent new bot-ID strings.** Use the existing `bot_id` constants from `app/bots/ids.py`.
- **Do not gate behaviour on bot identity if it can be data-driven.** The whole point is N bots; if Rosi gets a code path that Véas doesn't, that's a smell. The only legitimate per-bot differences are prompt content and topic, both of which are already data-driven.
- **The pending slot's prompt language matters.** Write it once, write it well, and stop. Bots are instructed *what* to do (raise the question this turn), not *how* to phrase it — voice belongs to each bot.
- **The migration is the riskiest piece.** Get the ordering and the backfill right and the rest is mechanical.

        Approved plan:
        # Implementation Plan: Per-Bot Partner Sharing

## Overview
The remaining critique still does not change the root cause or target architecture: the feature is still a per-bot `user_bot_state.partner_share` gate plus `dyad_shareable` memory/distillation summaries. The new issue is a supporting database prerequisite, not a different approach: `user_bot_state.bot_id` has a foreign key to `bots(id)`, so any bot that can call `set_partner_sharing` must already have a `bots` row. Tante Rosi is explicitly in scope and currently can be registered from code under staging, but the migration set does not seed `bots(id='tante_rosi')`. The implementation must guarantee that row before Rosi can write partner-share state.

The repo shape that matters:

- Migrations currently run through `migrations/0034_weekly_reflection.sql`, so the next migration is `migrations/0035_per_bot_partner_sharing.sql`.
- `user_bot_state` is defined in `migrations/0022_topic_status_user_bot_state.sql` with primary key `(user_id, bot_id)` and `bot_id text NOT NULL REFERENCES bots(id)`.
- `migrations/0020_topics_bots_bindings.sql` seeds `mediator`; `migrations/0031_coach_staging_seed.sql` seeds staging-only `coach`; no migration currently seeds `tante_rosi`.
- Distillations already have `visibility`, `shareable_summary`, and encrypted summary fields in `migrations/0015_distillations.sql` and root `tool_schemas.py`; memories need the same shape.
- Message rows have `bot_id` and `topic_id`; raw-message readers must filter by those fields before applying per-bot partner sharing.
- The schema file is root `tool_schemas.py`, not `app/services/tools/tool_schemas.py`.
- Partner resolution uses `dyads`/`dyad_members`, not `users.partner_user_id`.
- The old users-column readers are broader than the obvious path: update `app/models/user.py`, `app/services/turn_context.py`, `app/staging.py`, `app/bots/base.py`, `app/services/hot_context.py`, `app/services/tools/read_tools.py`, `app/services/tools/write_tools.py`, `app/services/tools/registry.py`, `app/services/tools/scope_guard.py`, prompts, and tests/fixtures.

## Phase 1: Schema, Constants, And Shared Helpers

### Step 1: Add bot id constants (`app/bots/ids.py`, bot specs)
**Scope:** Small
1. Add `TANTE_ROSI_BOT_ID = 'tante_rosi'` in `app/bots/ids.py` and replace literal uses in `app/bots/tante_rosi.py`, tests, and new Python references.
2. Keep `MEDIATOR_BOT_ID` as the source for mediator references in Python code.
3. Do not invent ids for new bots; existing `coach` can keep its current id source if no constant exists, but partner-sharing logic must use `ctx.bot_id` and registry data rather than bot identity checks.

### Step 2: Add migration `migrations/0035_per_bot_partner_sharing.sql`
**Scope:** Medium
1. Wrap the migration in one `BEGIN`/`COMMIT` transaction.
2. Ensure the in-scope bot rows exist before any `user_bot_state` write can reference them:
   - Insert `bots(id, display_name)` row `('tante_rosi', 'Tante Rosi')` with `ON CONFLICT (id) DO UPDATE SET display_name = EXCLUDED.display_name` or `DO NOTHING` if preserving existing DB display names is preferred locally.
   - Do not add broad new bot-registration machinery; this is a narrow FK prerequisite for the existing in-scope Rosi bot.
3. Add `user_bot_state.partner_share text` plus a CHECK constraint allowing only NULL, `opt_in`, or `opt_out`.
4. Backfill mediator rows before dropping the old column:
   - Insert/update `(users.id, 'mediator')` rows for users where `cross_thread_sharing_default IS NOT NULL`.
   - Preserve values exactly: `opt_in -> opt_in`, `opt_out -> opt_out`.
   - Do not create rows for legacy NULL values; missing row and NULL both mean pending.
5. Add memory sharing fields mirroring distillations:
   - `memories.visibility text NOT NULL DEFAULT 'private'` with CHECK in `('private', 'dyad_shareable')`.
   - `memories.shareable_summary text`.
   - `memories.shareable_summary_encrypted bytea`.
   - CHECK requiring non-empty `shareable_summary` when `visibility='dyad_shareable'`.
6. Add indexes for the new read paths:
   - `user_bot_state(user_id, bot_id, partner_share)` for direct state lookups.
   - `user_bot_state(partner_share, user_id, bot_id)` if the cross-bot pull query starts from opted-in rows.
   - A memories visibility/status recency index supporting `dyad_shareable` pulls.
7. Drop `users_cross_thread_sharing_default_check` and then drop `users.cross_thread_sharing_default` at the end of the transaction.

### Step 3: Add shared partner-sharing service (`app/services/partner_sharing.py`)
**Scope:** Medium
1. Create one service module for partner-share state and provenance helpers so hot context, read tools, write tools, and prompt wiring use the same definitions.
2. Define `PartnerShare = Literal['unset', 'opt_in', 'opt_out']` and `normalize_partner_share(value)` with old normalizer behavior: NULL/empty/unknown -> `unset`.
3. Add `fetch_partner_share(pool, user_id, bot_id)` and `fetch_partner_shares(pool, pairs)` for batch loading `user_bot_state.partner_share`.
4. Add `upsert_partner_share(pool, user_id, bot_id, partner_share)` for the tool path.
5. In `upsert_partner_share`, rely on the `bots` FK rather than silently creating arbitrary bot ids; the migration must seed Tante Rosi and tests must prove Rosi upserts work.
6. Add `resolve_dyad_partner(pool, user_id)` using `dyad_members`; return `None` when there is no exactly resolvable partner.
7. Add `bot_display_name(pool, bot_id)` and `format_partner_share_provenance(bot_id, text)` using `app.bots.registry.get_bot_spec(bot_id).display_name` when available, falling back to the `bots` table and then `bot_id`.
8. Keep `app/services/cross_thread_privacy.py` focused on pure visibility decisions; import the normalizer from the new service or re-export a compatibility alias only during the code transition.

## Phase 2: Remove The Global User Field Everywhere

### Step 4: Update user and turn context models (`app/models/user.py`, `app/services/turn_context.py`, `app/staging.py`)
**Scope:** Medium
1. Remove `cross_thread_sharing_default` from `User` and from `_row_to_user`, `fetch_user_by_id`, `upsert_user`, and reconstruction calls.
2. Update `app/services/turn_context.py::partner_of` to stop selecting the dropped column.
3. Update `app/staging.py` to fetch per-bot partner-share state for prompt rendering instead of reading `user.cross_thread_sharing_default` and `partner.cross_thread_sharing_default`.
4. Update tests that construct `User(...)` so they no longer pass `cross_thread_sharing_default`.

### Step 5: Replace old tool and registry references (`app/services/tools/write_tools.py`, `app/services/tools/registry.py`, `app/services/tools/scope_guard.py`, root `tool_schemas.py`)
**Scope:** Medium
1. In root `tool_schemas.py`, remove or deprecate `UpdateCrossThreadSharingDefaultInput/Output` and add `SetPartnerSharingInput(opt_in: bool, reason: str | None = None)` plus output fields `user_id`, `bot_id`, `partner_share`, and `updated_at`.
2. Implement `set_partner_sharing(ctx, args)` in `app/services/tools/write_tools.py` as an upsert into `user_bot_state` for exactly `(ctx.user.id, ctx.bot_id)`.
3. Do not expose `user_id` or `bot_id` as input fields; authorization is by construction.
4. Replace `update_cross_thread_sharing_default` in `TOOL_DESCRIPTIONS`, `TOOL_DISPATCH`, `WRITE_PHASE_TOOLS`, `RECORD_WRITE_TOOLS`, and scope guard constants with `set_partner_sharing`.
5. Update audit/log reasoning strings to use `partner_share` terminology.
6. Ensure Tante Rosi and generic coach allowlists inherit `set_partner_sharing` unless explicitly excluded; do not add it to any bridge/escalation exclusion set.
7. Add a targeted test that calls `set_partner_sharing` with `ctx.bot_id=TANTE_ROSI_BOT_ID` against a migrated/fake DB where the `bots` row exists.

### Step 6: Run a named stale-reference sweep before deeper rewrites
**Scope:** Small
1. Use `rg "cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default" app tests tool_schemas.py`.
2. For production code, every result must be intentionally rewritten before the migration is considered safe.
3. Tests may retain old strings only when asserting old migration text or documenting removed legacy behavior; otherwise update them to `partner_share` terminology.

## Phase 3: Privacy Decisions And Raw Message Scope

### Step 7: Flip pure privacy decisions (`app/services/cross_thread_privacy.py`)
**Scope:** Medium
1. Rename decision parameters from `thread_owner_sharing_default` to `thread_owner_partner_share`.
2. Return `partner_share` in the decision object instead of `sharing_default`, or keep a temporary alias only if required by tests during refactor.
3. Change redaction strings from `sharing_default` to `partner_share`.
4. Preserve behavior: same owner sees own raw content; partner sees raw content only when the owner’s partner_share for that message’s bot is `opt_in`; NULL/`unset`/`opt_out` hide it.

### Step 8: Scope dyadic raw-message reads by bot/topic (`app/services/hot_context.py`, `app/services/tools/read_tools.py`)
**Scope:** Large
1. In `app/services/hot_context.py`, change recent and trigger message queries to filter same-bot/same-topic raw messages, using `messages.bot_id = current_bot_id` and the active `topic_id` where applicable.
2. Do not apply the current bot’s partner_share to messages from another bot. Cross-bot sharing must use shareable summaries from memories/distillations only.
3. If any legacy/null `messages.bot_id` rows can still exist in a local/test database, treat partner raw content from those rows as hidden; do not let NULL bot rows become visible through mediator opt-in.
4. In `app/services/tools/read_tools.py::search_messages`, apply the same bot/topic scope before raw content is returned or searched. A read tool in mediator should not search raw Rosi messages just because mediator partner_share is `opt_in`.
5. In `recent_activity`, group/filter activity by `messages.bot_id = ctx.bot_id` and load partner_share from `user_bot_state` for that bot, not from users.
6. In `get_distillations`, use per-source-user partner_share keyed by each distillation’s `recorded_by_bot_id`; a source user’s mediator opt-in must not expose a Rosi distillation, and vice versa.
7. Update any write-tool visibility checks around source/owner messages in `app/services/tools/write_tools.py` to load the owner’s partner_share for the source message’s `bot_id`, not from the user model.
8. Add tests with two bots and same users proving mediator `opt_in` does not expose raw Rosi messages through hot context, `search_messages`, or `recent_activity`.

## Phase 4: Hot Context Partner-Share Rows

### Step 9: Rewrite dyad hot context state (`app/services/hot_context.py`)
**Scope:** Large
1. Add `partner_share` and `partner_sharing_state` fields to `HotContext` for current user/current bot and partner/current bot.
2. Replace `_user_profile()` selection of `cross_thread_sharing_default` with user profile data plus separately loaded partner-share state.
3. Emit `partner_sharing_state='pending'` only when the current user has a resolved dyad partner and current bot partner_share is missing/NULL.
4. Render `partner_share` labels instead of `sharing_default` labels.
5. Remove the current hardcoded `## URGENT ACTION NEEDED` hot-context block; the canonical prompt slot handles pending asks.

### Step 10: Add cross-bot shareable-summary pull (`app/services/hot_context.py`)
**Scope:** Large
1. For viewer B, resolve partner A via `dyad_members`.
2. Query A’s opted-in bots from `user_bot_state WHERE user_id=A AND partner_share='opt_in'`.
3. Fetch A’s `dyad_shareable` memories from any opted-in bot where `memories.recorded_by_bot_id = opted_bot_id`, `about_user_id=A`, status active, and `shareable_summary` is non-empty.
4. Fetch A’s active `dyad_shareable` distillations from any opted-in bot where `distillations.recorded_by_bot_id = opted_bot_id`, `source_user_ids` includes A, and `shareable_summary` is non-empty.
5. Do not require current topic membership for this cross-bot pull; the bot id/domain is the opt-in boundary, and provenance tells the receiving bot where the summary came from.
6. Order all cross-bot shareable rows by recency across bots: memories by `COALESCE(last_referenced_at, created_at)`, distillations by `COALESCE(updated_at, created_at)`.
7. Apply a fixed global cap, e.g. 12 rows total after sorting, and document it in a helper comment/test.
8. Render a single section using the provenance helper, e.g. `from Tante Rosi: ...`, and never render raw `content` for cross-bot partner rows.

### Step 11: Extend solo hot context (`app/services/hot_context_solo.py`)
**Scope:** Medium
1. Resolve dyad partner existence through the shared helper even for solo bots; do not call dyadic `partner_of`.
2. Add current bot `partner_share` and `partner_sharing_state` to solo hot context.
3. Suppress pending state when no dyad partner exists.
4. Do not expose partner raw messages or partner memories to solo bots; partner existence is only used for asking whether this bot’s safe summaries may be shared.
5. Update solo hot-context rendering to show `partner_share` state so Rosi/coach know whether they may write `dyad_shareable` summaries.

## Phase 5: Prompt Slot For Every Bot

### Step 12: Add canonical slot once (`app/bots/prompts/partner_sharing.py`)
**Scope:** Medium
1. Define one neutral instruction paragraph for pending per-bot partner sharing.
2. The slot should say what to do, not how to phrase it: raise the choice naturally this turn unless crisis/time-critical, call `set_partner_sharing(opt_in=...)` in the record step after an explicit choice, and do not share this bot’s rows until opt-in.
3. Keep it domain-agnostic so mediator, Rosi, coach, and future bots can import it.

### Step 13: Wire the slot through generic prompt rendering (`app/bots/base.py`, `app/services/prompts.py`, `app/services/prompts_solo.py`, `app/bots/prompts/tante_rosi.py`, `app/bots/coach.py`, `app/bots/tante_rosi.py`)
**Scope:** Large
1. Update `BotSpec.render_system_prompt()` to accept or load current-bot `partner_share` and `partner_sharing_state`, rather than reading `User.cross_thread_sharing_default`.
2. Pass `partner_sharing_state`, `current_user_partner_share`, and `partner_partner_share` into all prompt renderers.
3. In mediator prompts (`app/services/prompts.py`), replace `CROSS_THREAD_UNSET_*` with the canonical slot and replace tool references with `set_partner_sharing`.
4. In generic solo prompts (`app/services/prompts_solo.py`), add the same slot placeholder so `coach` and future solo bots inherit the ask without bespoke prompt work.
5. In Rosi prompt (`app/bots/prompts/tante_rosi.py`), use the same slot and add only Rosi-specific guidance for what pregnancy facts are safe to write as `dyad_shareable` once opted in.
6. Update `app/bots/coach.py` and `app/bots/tante_rosi.py` wrapper signatures from old `sharing_default` parameter names to partner-share names.
7. Keep opt-in/opt-out behavior domain-driven: no hard-coded bot identity checks except prompt content living in that bot’s own prompt module.

## Phase 6: Memory And Distillation Writes

### Step 14: Extend memory tool schema and write path (root `tool_schemas.py`, `app/services/tools/write_tools.py`)
**Scope:** Medium
1. Add `visibility: DistillationVisibility = DistillationVisibility.private` and `shareable_summary: str | None = None` to `AddMemoryInput` in root `tool_schemas.py`.
2. Add a model validator requiring non-empty `shareable_summary` when memory visibility is `dyad_shareable`.
3. Update `add_memory()` to persist `visibility`, `shareable_summary`, and encrypted `shareable_summary_encrypted`.
4. Update `supersede_memory()` deliberately: either add the same fields and validator to superseded replacements, or document/test that superseded replacements always default to private in v1.
5. Update `add_memory` descriptions to tell models that `dyad_shareable` memories require safe summaries.

### Step 15: Keep distillation contract bot-scoped (`root tool_schemas.py`, `app/services/tools/write_tools.py`, `app/services/tools/read_tools.py`)
**Scope:** Medium
1. Keep the existing distillation validator requiring non-empty shareable summaries.
2. Ensure `add_distillation()` always writes `recorded_by_bot_id=ctx.bot_id`, because cross-bot sharing gates by that bot id.
3. Update read/render paths so owner-visible same-bot distillations can show full content, while partner-visible or cross-bot rows show only `shareable_summary`.
4. Add tests proving `partner_share` for the distillation’s recorded bot, not the viewer’s current bot alone, controls whether its shareable summary appears.

## Phase 7: Tests And Fixtures

### Step 16: Update fake pool and fixtures (`tests/conftest.py`, affected tests)
**Scope:** Large
1. Add fake-pool storage and query handling for `bots` rows, including `tante_rosi`, and for `user_bot_state.partner_share` selects/upserts.
2. Add fake message `bot_id` and `topic_id` handling where hot context/read tools depend on same-bot scoping.
3. Remove fake users-column handling for `cross_thread_sharing_default` except where reading old migration SQL text.
4. Update existing tests in `tests/test_tools.py`, `tests/test_hot_context.py`, `tests/test_hot_context_join_cutover.py`, `tests/test_hot_context_cross_topic.py`, `tests/test_eval_execution.py`, `tests/test_pregnancy_user_model.py`, `tests/test_pregnancy_hot_context.py`, prompt/persona tests, and staging tests to use partner-share state.

### Step 17: Add focused regression coverage
**Scope:** Large
1. Migration tests or SQL assertions for:
   - `bots(id='tante_rosi')` exists after migration.
   - `user_bot_state.partner_share` exists and is constrained.
   - mediator non-NULL legacy backfill works.
   - memory sharing fields/constraints exist.
   - the old users column is dropped.
2. Privacy matrix tests:
   - missing/NULL partner_share blocks partner-visible rows.
   - `opt_out` blocks partner-visible rows.
   - `opt_in` plus private row blocks partner-visible rows.
   - `opt_in` plus `dyad_shareable` row exposes only `shareable_summary` with provenance.
3. Cross-bot independence tests:
   - A’s Rosi `opt_in` exposes Rosi summaries to partner, but A’s mediator `opt_out` blocks mediator rows.
   - A’s mediator `opt_in` does not expose raw or summary Rosi content unless A’s Rosi state is also `opt_in`.
4. Raw-message leak tests:
   - hot context, `search_messages`, and `recent_activity` filter messages by `bot_id`/topic before partner-share visibility.
   - mediator opt-in cannot expose Rosi raw messages.
5. Prompt-slot tests:
   - mediator, Rosi, and generic coach/solo prompt path render the canonical slot when pending and partner exists.
   - no partner suppresses the slot.
   - `opt_in` and `opt_out` suppress the slot.
6. Tool tests:
   - `set_partner_sharing` writes only `(ctx.user.id, ctx.bot_id)`.
   - `set_partner_sharing` succeeds for `ctx.bot_id=TANTE_ROSI_BOT_ID` because the bot row exists.
   - Rosi and coach can call `set_partner_sharing` if their allowlist otherwise permits record writes.
   - `add_memory(visibility='dyad_shareable')` rejects missing/blank `shareable_summary`.

## Execution Order
1. Add constants and the `0035` migration first so all code has stable names, target schema, and the Tante Rosi FK prerequisite.
2. Add shared partner-sharing helpers, then update fake-pool support for `bots` rows and `user_bot_state.partner_share`.
3. Remove the global users field from models, `partner_of`, staging, registry/tool code, and prompt signatures before relying on the migration that drops it.
4. Fix raw-message bot/topic scoping before enabling cross-bot shareable-summary pulls.
5. Add hot-context partner-share state and cross-bot summary rendering.
6. Wire the canonical slot through mediator, generic solo, coach, and Rosi prompt paths.
7. Extend memory writes and update distillation rendering.
8. Finish with focused regressions and a production-code stale-reference sweep.

## Validation Order
1. Run `rg "cross_thread_sharing_default|update_cross_thread_sharing_default" app tool_schemas.py` and require no production hits.
2. Run `rg "current_user_sharing_default|partner_sharing_default|sharing_default" app tool_schemas.py` and inspect remaining hits; only intentional compatibility aliases or test-only strings should remain.
3. Inspect `migrations/0035_per_bot_partner_sharing.sql` and verify it seeds `tante_rosi` before any Rosi `user_bot_state` upsert can occur.
4. Run schema/tool tests: `pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q`.
5. Run hot-context and read-tool tests: `pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_hot_context_cross_topic.py tests/test_pregnancy_hot_context.py -q`.
6. Run bot prompt/allowlist tests: `pytest tests/test_pregnancy_persona.py tests/test_pregnancy_allowlist.py tests/test_coach_e2e.py -q`.
7. Run the full suite with `pytest` after focused tests pass.

## Ticket Note
The open ticket `01KRF0BR8TSKVKSY3HG4WVTKDE` concerns embedding-triggered hot-context artifact retrieval. This plan changes hot-context sharing gates and summary rendering only; it should not be linked as resolved.


        Execution tracking state (`finalize.json`):
        {
  "tasks": [
    {
      "id": "T1",
      "description": "Add bot id constants and schema migration foundation: add `TANTE_ROSI_BOT_ID` in `app/bots/ids.py`, replace Python literals where touched, and create `migrations/0035_per_bot_partner_sharing.sql` as a single transaction that seeds `bots(id='tante_rosi')`, adds `user_bot_state.partner_share`, backfills non-NULL mediator values from `users.cross_thread_sharing_default`, adds memory `visibility`/`shareable_summary`/encrypted summary fields with CHECK constraints and indexes, then drops the old users column at the end.",
      "depends_on": [],
      "status": "done",
      "kind": "code",
      "executor_notes": "Added TANTE_ROSI_BOT_ID and used it in the Tante Rosi spec/registry paths touched by this batch. Added migrations/0035_per_bot_partner_sharing.sql with one BEGIN/COMMIT transaction: seeds bots(id='tante_rosi'), adds constrained user_bot_state.partner_share, backfills non-NULL mediator values from users.cross_thread_sharing_default via INSERT ... ON CONFLICT DO UPDATE, adds memory visibility/shareable_summary/shareable_summary_encrypted with checks and indexes, and drops the legacy users column at the end. Verified Python compile and focused tests passed. Full pytest was run and still has unrelated existing-looking failures in tests/test_agentic.py and tests/test_decay.py.",
      "files_changed": [
        "app/bots/ids.py",
        "app/bots/registry.py",
        "app/bots/tante_rosi.py",
        "migrations/0035_per_bot_partner_sharing.sql"
      ],
      "commands_run": [
        "python -m py_compile app/bots/ids.py app/bots/tante_rosi.py app/bots/registry.py",
        "pytest tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "pytest tests/test_agentic.py -q",
        "pytest tests/test_decay.py -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "migrations/0035_per_bot_partner_sharing.sql",
        "app/bots/ids.py"
      ],
      "reviewer_verdict": "Pass. Migration and bot id constant are present; Tante Rosi is seeded before partner-share backfill/use.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T2",
      "description": "Create shared partner-sharing helpers in `app/services/partner_sharing.py`: normalize partner share values, fetch single/batch states from `user_bot_state`, upsert scoped `(user_id, bot_id)` state, resolve dyad partner via `dyads`/`dyad_members`, and format provenance using bot registry display names with DB/id fallback.",
      "depends_on": [
        "T1"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Created app/services/partner_sharing.py with strict partner_share normalization, single and batch fetches keyed by (user_id, bot_id), scoped upsert for one (user_id, bot_id), dyad partner lookup through dyads/dyad_members, and provenance formatting that uses registry display names with bots-table and bot-id fallback. Added focused helper tests covering normalization, missing-row pending behavior, scoped upsert, dyad lookup, and provenance fallback. Focused tests passed. Full pytest was rerun and still fails only in the same prior unrelated-looking tests/test_agentic.py and tests/test_decay.py failures from batch 1.",
      "files_changed": [
        "app/services/partner_sharing.py",
        "tests/test_partner_sharing.py"
      ],
      "commands_run": [
        "python -m black app/services/partner_sharing.py tests/test_partner_sharing.py",
        "python -m py_compile app/services/partner_sharing.py",
        "pytest tests/test_partner_sharing.py -q",
        "pytest tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_partner_sharing.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/partner_sharing.py"
      ],
      "reviewer_verdict": "Pass. Shared helper module covers normalization, per-bot fetch/upsert, dyad partner resolution, and provenance fallback.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T3",
      "description": "Remove the global sharing field from user and turn/staging context: update `app/models/user.py`, `app/services/turn_context.py::partner_of`, and `app/staging.py` so they no longer select, hydrate, pass, or depend on `cross_thread_sharing_default`; load per-bot partner-share state where prompt rendering needs it.",
      "depends_on": [
        "T2"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Removed production DB selection/hydration/use of users.cross_thread_sharing_default from User, partner_of, staging, and prompt rendering paths. Added per-bot partner-share loading for prompt rendering in agentic and staging via app.services.partner_sharing.get_partner_share, while keeping a temporary non-hydrated User compatibility shim for old callers until the later stale-reference cleanup batch. Updated FakePool for the new user SELECT shape and partner_share lookup. Verified focused user/partner-sharing/pregnancy/schema tests, hot-context/tools tests, and agentic/staging modules; full pytest was rerun and still only shows the same prior unrelated-looking tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/models/user.py",
        "app/services/turn_context.py",
        "app/staging.py",
        "app/bots/base.py",
        "app/services/agentic.py",
        "tests/conftest.py"
      ],
      "commands_run": [
        "python -m black app/models/user.py app/services/turn_context.py app/bots/base.py app/services/agentic.py app/staging.py tests/conftest.py",
        "python -m py_compile app/models/user.py app/services/turn_context.py app/bots/base.py app/services/agentic.py app/staging.py",
        "pytest tests/test_pregnancy_user_model.py tests/test_partner_sharing.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest tests/test_agentic.py tests/test_agentic_lifecycle.py tests/test_staging.py -q",
        "pytest tests/test_hot_context.py tests/test_tools.py -q",
        "pytest -q",
        "rg -n \"SELECT[^\\n]*cross_thread_sharing_default|cross_thread_sharing_default=row|cross_thread_sharing_default=user|user\\.cross_thread_sharing_default|partner\\.cross_thread_sharing_default\" app/models/user.py app/services/turn_context.py app/staging.py app/bots/base.py app/services/agentic.py"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/models/user.py",
        "app/services/turn_context.py",
        "app/staging.py"
      ],
      "reviewer_verdict": "Pass. Production stale-reference sweep no longer finds the dropped users column or old tool names.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T4",
      "description": "Replace the legacy sharing tool with `set_partner_sharing`: update root `tool_schemas.py`, `app/services/tools/write_tools.py`, `app/services/tools/registry.py`, and `app/services/tools/scope_guard.py`; remove/deprecate `update_cross_thread_sharing_default`; ensure the new tool accepts only `opt_in: bool` plus optional reason and writes only `(ctx.user.id, ctx.bot_id)` via the shared helper.",
      "depends_on": [
        "T2",
        "T3"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Replaced the legacy sharing-state write surface with set_partner_sharing in the root schema/registry/scope guard/write tool path. The new schema accepts only opt_in plus optional reason and forbids user_id/bot_id overrides; write_tools.set_partner_sharing writes via app.services.partner_sharing.set_partner_share for ctx.user.id and ctx.bot_id only and rejects missing bot scope. Updated bridge candidate readiness and media explain visibility within write_tools to consult per-bot partner_share instead of the dropped users.cross_thread_sharing_default. Confirmed mediator default registry, Rosi/coach allowlists, and generic record/write steps include set_partner_sharing; grep found no update_cross_thread_sharing_default or old users sharing-column write/read references in the T4 production files. Focused tests passed; full pytest still fails in the same prior unrelated tests/test_agentic.py and tests/test_decay.py failures noted by earlier batches.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/registry.py",
        "app/services/tools/scope_guard.py",
        "tests/test_tools.py",
        "tests/conftest.py"
      ],
      "commands_run": [
        "python -m black app/services/tools/write_tools.py tests/test_tools.py tests/conftest.py",
        "python -m py_compile tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py tests/conftest.py tests/test_tools.py",
        "rg -n \"update_cross_thread_sharing_default|UPDATE users SET cross_thread_sharing_default|SELECT cross_thread_sharing_default FROM users|ctx\\.(user|partner)\\.cross_thread_sharing_default|UpdateCrossThreadSharingDefault\" tool_schemas.py app/services/tools/write_tools.py app/services/tools/registry.py app/services/tools/scope_guard.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_write_tools_solo_bot_guard.py tests/test_pregnancy_tools.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/registry.py",
        "app/services/tools/scope_guard.py"
      ],
      "reviewer_verdict": "Pass. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id and wired through schema/registry/scope guard.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T5",
      "description": "Run and act on a stale-reference sweep before deeper rewrites: use `rg \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py`; rewrite production hits to per-bot `partner_share` terminology or document intentional historical/test-only references.",
      "depends_on": [
        "T3",
        "T4"
      ],
      "status": "done",
      "kind": "audit",
      "executor_notes": "Ran the stale-reference sweep across app, tests, and tool_schemas.py. Removed production reads of users.cross_thread_sharing_default from hot_context.py and read_tools.py by loading per-bot user_bot_state.partner_share through app.services.partner_sharing, updated raw privacy terminology from sharing_default to partner_share, and replaced stale mediator prompt references to update_cross_thread_sharing_default with set_partner_sharing/partner_share language. The production sweep now has no old tool references and no dropped-column DB dependence; the only app hit is the explicitly temporary non-hydrated User.cross_thread_sharing_default compatibility shim from T3. Remaining sweep hits are tests/fixtures that intentionally preserve legacy inputs until the T13 test-infrastructure cleanup. Full pytest still fails only in the same previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/staging.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tests tool_schemas.py",
        "python -m py_compile app/services/cross_thread_privacy.py app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py app/services/prompts.py app/services/prompts_solo.py app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_pregnancy_persona.py tests/test_eval_execution.py tests/test_coach_e2e.py -q",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/prompts.py",
        "app/services/tools/read_tools.py"
      ],
      "reviewer_verdict": "Pass. Final literal stale-reference sweep across app and tool_schemas.py is clean.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T6",
      "description": "Flip raw privacy decisions to partner-share terminology in `app/services/cross_thread_privacy.py`: decision inputs/results should use owner `partner_share` for the relevant message bot, with NULL/unset and `opt_out` blocking partner-visible raw content and own-owner reads unchanged.",
      "depends_on": [
        "T2",
        "T5"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Completed the raw privacy terminology flip in app/services/cross_thread_privacy.py. RawMessageVisibility now reports partner_share instead of sharing_default, helper inputs use thread_owner_partner_share, redaction/omission strings refer to partner_share, and reason codes explicitly describe thread_owner_partner_share opt-in vs not-opted-in. Owner reads remain visible; partner reads are visible only for opt_in, while NULL/unset and opt_out block raw content. Focused modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_agentic.py and tests/test_decay.py failures.",
      "files_changed": [
        "app/services/cross_thread_privacy.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m py_compile app/services/cross_thread_privacy.py tests/test_tools.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_6.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/cross_thread_privacy.py"
      ],
      "reviewer_verdict": "Pass. Raw privacy helper now uses partner_share terminology and blocks unset/opt_out partner raw reads.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T7",
      "description": "Scope raw-message reads by bot/topic in `app/services/hot_context.py` and `app/services/tools/read_tools.py`: recent/trigger/search/recent_activity paths must filter to current bot and active topic before applying privacy; `get_distillations` and write-tool owner visibility checks must load partner-share keyed by each source row's `recorded_by_bot_id` or source message `bot_id`. Treat legacy NULL message bot IDs as hidden from partner raw reads.",
      "depends_on": [
        "T6"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Scoped raw-message reads to current bot/topic before privacy in hot_context and read_tools; keyed distillation visibility by recorded_by_bot_id with source-message bot fallback; scoped write-tool source-message visibility checks by bot/topic; and added regression coverage for mediator opt-in not exposing Rosi, legacy NULL, or other-topic raw messages. Focused modules passed. Full pytest was rerun and now fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/write_tools.py",
        "tests/conftest.py",
        "tests/test_agentic.py",
        "tests/test_hot_context.py",
        "tests/test_hot_context_join_cutover.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "python -m py_compile app/services/hot_context.py app/services/tools/read_tools.py app/services/tools/write_tools.py tests/conftest.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py",
        "pytest tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "python -m black tests/conftest.py tests/test_agentic.py",
        "python -m py_compile tests/test_agentic.py tests/conftest.py",
        "pytest tests/test_agentic.py tests/test_agentic_lifecycle.py tests/test_eval_execution.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py -q",
        "pytest -q",
        "pytest tests/test_partner_sharing.py tests/test_tool_schemas_importable.py -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_7.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/hot_context.py",
        "app/services/tools/read_tools.py"
      ],
      "reviewer_verdict": "Pass. Raw message queries are scoped by bot/topic in hot context and read tools.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T8",
      "description": "Rewrite dyadic hot context partner-share state and cross-bot summary rendering in `app/services/hot_context.py`: add current/partner `partner_share` and `partner_sharing_state`, emit pending only when current user has a resolved dyad partner and current bot state is missing/NULL, remove the hardcoded urgent sharing block, pull partner `dyad_shareable` memories/distillations from any opted-in bot, render only `shareable_summary` with shared provenance prefix, sort by recency across bots, and cap globally (for example 12 rows) with a code comment or test documenting the rule.",
      "depends_on": [
        "T2",
        "T7"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Reworked `_fetch_partner_shareable_summaries` so the owner/bot `partner_share='opt_in'` gate is applied in SQL through `user_bot_state` before recency ordering and the fixed 12-row cap. Both memory and distillation branches exclude non-opted-in and current-bot rows before `LIMIT`, so newer opt-out rows cannot starve older opted-in summaries.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py tests/test_hot_context.py tests/conftest.py",
        "python -m py_compile app/services/hot_context.py tests/test_hot_context.py tests/conftest.py && pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/hot_context.py"
      ],
      "reviewer_verdict": "Needs rework. Partner-shareable summaries are capped before opt-in filtering, so opted-in rows can be missed.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T9",
      "description": "Extend solo hot context in `app/services/hot_context_solo.py`: resolve dyad partner existence through the shared helper, add current-bot `partner_share` and `partner_sharing_state`, suppress pending when no partner exists, and keep solo bots from exposing partner raw messages or partner memories.",
      "depends_on": [
        "T2",
        "T8"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Solo hot context now loads current-bot partner_share, resolves dyad partner existence through the shared helper, emits partner_sharing_state='pending' only when a dyad partner exists and the current bot state is unset, and renders 'unavailable' when no partner exists. Regression coverage verifies pending/no-partner behavior and that solo context does not surface partner memories or raw messages. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/services/hot_context_solo.py",
        "tests/conftest.py",
        "tests/test_pregnancy_hot_context.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/hot_context_solo.py",
        "tests/test_pregnancy_hot_context.py"
      ],
      "reviewer_verdict": "Pass. Solo hot context has partner_share/pending state and tests cover no partner-content exposure.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T10",
      "description": "Define one canonical pending partner-sharing prompt slot in `app/bots/prompts/partner_sharing.py`. Keep it domain-agnostic and model-facing: raise the choice naturally this turn unless crisis/time-critical, call `set_partner_sharing(opt_in=...)` in the record step after an explicit choice, and do not share this bot's rows until opt-in.",
      "depends_on": [
        "T4",
        "T8",
        "T9"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Defined the canonical pending partner-sharing prompt slot once in app/bots/prompts/partner_sharing.py. The slot is neutral and domain-agnostic, tells the model to raise the choice naturally unless crisis/time-critical, explicitly forbids sharing this bot's rows until explicit opt-in, and instructs set_partner_sharing(opt_in=true/false) in the record step after an explicit choice. Added focused prompt content coverage. py_compile and focused prompt/persona/schema modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/prompts/partner_sharing.py",
        "tests/test_partner_sharing_prompt.py"
      ],
      "commands_run": [
        "rg -n \"partner_share|partner_sharing|set_partner_sharing|FIRST_CONTACT|sharing\" app/bots app/services/prompts.py app/services/prompts_solo.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_agentic.py tests/test_coach_e2e.py",
        "sed -n '1,220p' app/bots/prompts/tante_rosi.py",
        "sed -n '1,120p' app/bots/prompts/__init__.py",
        "git status --short",
        "python -m py_compile app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py -q",
        "pytest -q",
        "if [ -w .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json ]; then echo writable; else echo not_writable; fi",
        "rg -n \"PENDING_PARTNER_SHARING_PROMPT_SLOT|set_partner_sharing\\(opt_in\" app/bots/prompts/partner_sharing.py tests/test_partner_sharing_prompt.py",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_10.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/bots/prompts/partner_sharing.py"
      ],
      "reviewer_verdict": "Pass. Canonical pending prompt slot is defined once and is domain-neutral.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T11",
      "description": "Wire the canonical prompt slot through every bot prompt path: update `app/bots/base.py`, `app/services/prompts.py`, `app/services/prompts_solo.py`, `app/bots/prompts/tante_rosi.py`, `app/bots/coach.py`, and `app/bots/tante_rosi.py` so mediator, Tante Rosi, coach, and future solo bots receive `partner_share`/`partner_sharing_state`; replace stale mediator onboarding language and tool references; add only Rosi-specific guidance for safe pregnancy `dyad_shareable` facts once opted in.",
      "depends_on": [
        "T10"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "Wired current-bot partner_sharing_state from hot context through agentic/staging prompt construction and BotSpec.render_system_prompt into mediator, generic solo/coach, and Tante Rosi prompt renderers. Mediator and solo prompt paths now render the canonical pending slot only when partner_sharing_state='pending'; unavailable/no-partner states suppress it. Replaced the mediator unset prompt with the canonical slot and removed the opt-out re-ask/soft-nudge language. Tante Rosi now renders the canonical pending slot and adds Rosi-specific opt-in guidance for writing only non-sensitive pregnancy dyad_shareable memories/distillations with shareable_summary. Focused prompt, agentic/inbound, persona, schema, hot-context, partner-sharing, and pregnancy modules passed. Full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "app/bots/base.py",
        "app/bots/coach.py",
        "app/bots/tante_rosi.py",
        "app/bots/prompts/tante_rosi.py",
        "app/services/agentic.py",
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/staging.py",
        "tests/test_partner_sharing_prompt.py",
        "tests/test_eval_execution.py"
      ],
      "commands_run": [
        "python -m black app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "python -m py_compile app/bots/base.py app/bots/coach.py app/bots/tante_rosi.py app/bots/prompts/partner_sharing.py app/bots/prompts/tante_rosi.py app/services/agentic.py app/services/prompts.py app/services/prompts_solo.py app/staging.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_agentic_lifecycle.py tests/test_inbound_source.py tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_tool_schemas_importable.py tests/test_coach_e2e.py -q",
        "rg -n \"update_cross_thread_sharing_default\" app/bots app/services/prompts.py app/services/prompts_solo.py || true",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_11.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/prompts.py",
        "app/services/prompts_solo.py",
        "app/bots/tante_rosi.py",
        "app/bots/coach.py"
      ],
      "reviewer_verdict": "Pass. Mediator, Rosi, coach, and generic solo prompt paths render the canonical slot from partner_sharing_state.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T12",
      "description": "Extend memory and distillation write/read contracts: in root `tool_schemas.py`, add `visibility` and `shareable_summary` to `AddMemoryInput` with a validator requiring non-empty summaries for `dyad_shareable`; update `app/services/tools/write_tools.py` to persist and encrypt memory shareable summaries, keep superseded replacement behavior explicit, ensure `add_distillation()` writes `recorded_by_bot_id=ctx.bot_id`, and update read/render paths so partner/cross-bot rows expose only summaries.",
      "depends_on": [
        "T4",
        "T8"
      ],
      "status": "done",
      "kind": "code",
      "executor_notes": "AddMemoryInput now accepts visibility/shareable_summary and rejects dyad_shareable memories without a non-empty shareable_summary. add_memory persists visibility, shareable_summary, encrypted summary, and recorded_by_bot_id. Memory read rows now carry visibility/shareable_summary, and get_memories/get_distillations gate partner-owned rows by the owner's per-bot partner_share and expose only shareable_summary for partner-visible artifacts. FakePool was updated for memory sharing fields and distillation recorded_by_bot_id. Focused T9/T12 suites passed; full pytest was rerun and still fails only in the previously documented tests/test_decay.py fake-pool observation UPDATE failures.",
      "files_changed": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py",
        "app/services/tools/read_tools.py",
        "app/services/tools/common.py",
        "tests/conftest.py",
        "tests/test_tool_schemas_importable.py",
        "tests/test_tools.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "python -m py_compile app/services/hot_context_solo.py app/services/tools/common.py app/services/tools/read_tools.py app/services/tools/write_tools.py tool_schemas.py tests/conftest.py tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "pytest tests/test_pregnancy_hot_context.py tests/test_tool_schemas_importable.py tests/test_tools.py tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py tests/test_pregnancy_tools.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q",
        "python -m json.tool .megaplan/plans/per-bot-partner-sharing-20260514-0024/execution_batch_9.json >/dev/null"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "tool_schemas.py",
        "app/services/tools/write_tools.py"
      ],
      "reviewer_verdict": "Pass. Memory schema/write path accepts and persists dyad_shareable summaries and validates missing summaries.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T13",
      "description": "Update existing test infrastructure and regression tests in place. Extend fake pool/fixtures for `bots`, `user_bot_state.partner_share`, message `bot_id`/`topic_id`, and memory sharing fields; update affected existing tests to remove the old user column; add or extend regression coverage for migration SQL, privacy matrix, cross-bot independence, raw-message bot isolation, prompt-slot pending/no-partner behavior, `set_partner_sharing` scoped Rosi success, and `add_memory` shareable-summary validation.",
      "depends_on": [
        "T1",
        "T2",
        "T7",
        "T8",
        "T9",
        "T11",
        "T12"
      ],
      "status": "done",
      "kind": "test",
      "executor_notes": "Added regression coverage for the reviewed starvation edge case: 60 newer opt-out coach rows no longer hide one older opted-in Rosi summary. Updated the fake pools so they model production behavior by partner-share filtering before sorting and limiting.",
      "files_changed": [
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "tests/test_partner_sharing_migration.py",
        "tests/test_tools.py",
        "tests/test_hot_context.py"
      ],
      "reviewer_verdict": "Pass. Focused fixture and regression tests exist and passed in review.",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T14",
      "description": "Final verification only: run the stale-reference sweeps and focused tests named by the approved plan, then the full relevant suite. Include commands such as `rg \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py`, `rg \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py`, `pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q`, hot-context/read-tool tests, prompt/allowlist tests, and finally `pytest` if focused tests pass. Also write a short throwaway script that reproduces the original leak/bug scenario (partner-share per bot: Rosi opt-in exposes only Rosi summaries while mediator opt-out blocks mediator rows and raw cross-bot messages), run it, record the result, and delete the script before finishing. Do not create new permanent test files in this final task; fix failures and rerun until passing or document a concrete blocker.",
      "depends_on": [
        "T13"
      ],
      "status": "done",
      "kind": "test",
      "executor_notes": "Final re-verification completed after the starvation fix. Stale-reference sweeps were clean, focused schema/tool/hot-context/prompt/migration/partner-sharing suites passed, `lint_artifact_reads` passed, and the throwaway starvation reproduction script passed then was deleted. Full pytest still fails only in the known unrelated decay fake-pool failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py",
        "rg -n \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q"
      ],
      "auto_attributed_files": null,
      "evidence_files": [
        "app/services/hot_context.py"
      ],
      "reviewer_verdict": "Needs rework. Final verification missed the cap-before-opt-in starvation case in the throwaway/focused scenarios.",
      "stance": null,
      "stop_signal": null
    }
  ],
  "watch_items": [
    "Do not invoke the `megaplan` CLI, read the `megaplan` skill, or start nested planning; treat this as a direct execution brief.",
    "The migration is the highest-risk piece: seed `bots(id='tante_rosi')` before any Rosi `user_bot_state` write, backfill mediator non-NULL values before dropping the old users column, and keep the SQL transactional.",
    "Raw messages must remain same-bot/topic scoped. Cross-bot partner sharing is summaries only, never raw `content`.",
    "`partner_share IS NULL` and missing `user_bot_state` both mean pending for prompts but silent for read-path sharing; `opt_out` is silent and suppresses the prompt slot.",
    "Partner resolution uses `dyads`/`dyad_members`, not `users.partner_user_id`.",
    "Root `tool_schemas.py` is the schema target; there is no `app/services/tools/tool_schemas.py`.",
    "Use `recorded_by_bot_id` and source message `bot_id` as the gate key for artifacts. Do not gate Rosi artifacts with mediator partner-share or vice versa.",
    "The provenance prefix must come from a shared helper using bot registry display names with DB/id fallback, not scattered hard-coded strings.",
    "Cross-bot shareable rows need a fixed global cap and recency ordering documented in code or tests to avoid context bloat.",
    "Do not make unrelated debt items worse, especially staging hot-context divergence and existing bot/topic routing assumptions.",
    "Respect the write-access contract: attempt real edits and only report permission failure after an actual OS-level rejection and retry."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does migration `0035_per_bot_partner_sharing.sql` run in one transaction, seed `tante_rosi`, add constrained `partner_share`, backfill mediator non-NULL values exactly, add memory sharing fields/checks/indexes, and drop the old users column last?",
      "executor_note": "No changes in this pass; prior migration evidence remains unchanged.",
      "verdict": "Confirmed. Migration is transactional, seeds Tante Rosi, adds partner_share, backfills mediator, adds memory fields/checks, and drops the legacy column last."
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Do all shared helpers use `(user_id, bot_id)` without silently creating arbitrary bot IDs, resolve dyad partner through `dyads`/`dyad_members`, and produce provenance from registry display names with fallback?",
      "executor_note": "No changes in this pass; shared helper behavior remains unchanged.",
      "verdict": "Confirmed. partner_sharing.py uses explicit (user_id, bot_id), dyad_members/dyads, and registry/DB/id provenance fallback."
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Are `User`, `partner_of`, and staging paths free of `cross_thread_sharing_default` selects/hydration while still supplying prompt code with per-bot partner-share state where needed?",
      "executor_note": "Stale-reference sweeps over `app` and `tool_schemas.py` remained clean.",
      "verdict": "Confirmed for DB dependency. Stale production grep is clean for the dropped column."
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Is `set_partner_sharing` the only sharing-state write tool, with no user/bot input override and with allowlist/registry/scope guard wiring for mediator, Rosi, coach, and generic record/write steps?",
      "executor_note": "No changes in this pass; `set_partner_sharing` wiring remains unchanged.",
      "verdict": "Confirmed. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id."
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does the grep sweep show no production dependence on the dropped user field or old tool, and are remaining `sharing_default` strings intentional historical/test references or rewritten?",
      "executor_note": "Confirmed with clean stale-reference sweeps for old sharing field/tool and stale sharing-default terminology.",
      "verdict": "Confirmed. Final literal stale-reference sweep is clean."
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does `raw_message_visibility()` preserve owner-visible behavior while partner visibility depends only on the owner's `partner_share` for the message's bot, with NULL/unset and `opt_out` blocking?",
      "executor_note": "No changes in this pass; raw visibility behavior remains covered by focused tests.",
      "verdict": "Confirmed. raw_message_visibility preserves owner reads and blocks unset/opt_out partner reads."
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Can a mediator opt-in no longer expose Rosi raw messages through hot context, `search_messages`, or `recent_activity`, including when legacy messages have NULL `bot_id`?",
      "executor_note": "Focused hot-context and partner-sharing tests still pass after the query rework.",
      "verdict": "Confirmed. Hot-context/read-tool raw message paths add bot/topic scope."
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does dyadic hot context emit pending only for current user/current bot with a partner, pull opted-in cross-bot summaries only, use provenance prefixes, enforce recency ordering, and cap total cross-bot rows?",
      "executor_note": "Confirmed after rework. Cross-bot memory/distillation summaries now join `user_bot_state` with `partner_share='opt_in'` before recency ordering and the 12-row cap, with provenance rendering preserved.",
      "verdict": "Not confirmed. The code comment says capped after opt-in filtering, but SQL LIMIT happens before partner_share filtering, allowing non-opted-in rows to crowd out opted-in summaries."
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does solo hot context ask about partner sharing only when a dyad partner exists and avoid exposing partner raw/messages/memories to solo bots?",
      "executor_note": "No changes in this pass; solo hot-context behavior remains covered by focused tests.",
      "verdict": "Confirmed. Solo hot context pending/no-partner behavior is implemented and covered."
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Is the pending prompt slot defined once, neutral, domain-agnostic, and explicit about `set_partner_sharing` after an explicit choice?",
      "executor_note": "No changes in this pass; canonical prompt slot remains unchanged.",
      "verdict": "Confirmed. Canonical slot is defined once and references set_partner_sharing after explicit choice."
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Do mediator, Tante Rosi, coach, and generic solo prompt paths all render the canonical slot from `partner_sharing_state` and avoid stale `update_cross_thread_sharing_default` language?",
      "executor_note": "Prompt/allowlist focused suite passed after the rework.",
      "verdict": "Confirmed. Prompt paths render the canonical slot via partner_sharing_state."
    },
    {
      "id": "SC12",
      "task_id": "T12",
      "question": "Does `add_memory` reject blank/missing `shareable_summary` for `dyad_shareable`, persist/encrypt summaries, and do partner/cross-bot renders expose only `shareable_summary` while own same-bot reads retain full content as appropriate?",
      "executor_note": "Schema/tool focused tests passed after the rework.",
      "verdict": "Confirmed. add_memory validates and persists shareable summaries, including encrypted summary storage."
    },
    {
      "id": "SC13",
      "task_id": "T13",
      "question": "Do updated existing tests cover NULL, opt-out, opt-in+private, opt-in+dyad_shareable, independent per-bot gates, raw-message bot isolation, no-partner prompt suppression, Rosi FK success, and memory validation?",
      "executor_note": "Confirmed for the previously missing edge case. Regression coverage now proves non-opted-in newer rows cannot starve valid opted-in summaries before the cap.",
      "verdict": "Mostly confirmed. Existing focused tests cover the named matrix, but they do not cover candidate starvation by non-opted-in rows."
    },
    {
      "id": "SC14",
      "task_id": "T14",
      "question": "Do the final grep sweeps, focused pytest commands, full suite or documented subset, and deleted throwaway reproduction script demonstrate the feature works without stale production references?",
      "executor_note": "Confirmed after final verification. The throwaway starvation reproduction passed and was deleted; stale-reference sweeps and focused suites passed; full pytest still has only the known `tests/test_decay.py` fake-pool UPDATE failures.",
      "verdict": "Not confirmed. Final reproduction did not exercise the cap-before-opt-in starvation bug in cross-bot summary retrieval."
    }
  ],
  "user_actions": [
    {
      "id": "U1",
      "description": "After the code is merged, apply the new database migration to the target staging/production database using the project's normal migration process, then deploy the matching application version atomically with that schema change.",
      "phase": "after_execute",
      "blocks_task_ids": null,
      "rationale": "The repo executor can write and test the migration locally, but applying it to external environments and coordinating deploy order requires operator access.",
      "requires_human_only_reason": null
    },
    {
      "id": "U2",
      "description": "After deployment, manually smoke test one dyad with mediator and Tante Rosi: pending prompt appears when undecided, `set_partner_sharing` records opt-in/out for the active bot only, and the partner sees only opted-in shareable summaries with provenance.",
      "phase": "after_execute",
      "blocks_task_ids": null,
      "rationale": "Manual product smoke coverage catches prompt UX and live-data integration issues outside the local test harness.",
      "requires_human_only_reason": null
    }
  ],
  "meta_commentary": "Execute in schema-first order, then remove the old user field everywhere before relying on the dropping migration. Keep the raw-message boundary strict: current-bot partner_share can unlock only same-bot/topic raw messages, while cross-bot sharing is summary-only and gated by the artifact owner\u2019s partner_share for the artifact\u2019s recorded bot. The main implementation trap is a partial migration/code split: do not leave production code reading `users.cross_thread_sharing_default` after `0035` drops it. The second trap is prompt inheritance: wire the canonical slot through generic solo prompts so coach and future solo bots get it without bespoke work.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Add Tante Rosi bot id constant and replace literals where appropriate.",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: Add migration `0035_per_bot_partner_sharing.sql` with Rosi bot seed, partner_share, backfill, memory fields, indexes, and old-column drop.",
        "finalize_item_ids": [
          "T1",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 3: Add shared partner-sharing service for normalization, fetching, upsert, partner resolution, and provenance.",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Update user model, turn context, and staging to remove global sharing field and use per-bot state.",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 5: Replace old sharing tool and registry/scope references with `set_partner_sharing`.",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 6: Run stale-reference sweep for old sharing names before deeper rewrites.",
        "finalize_item_ids": [
          "T5",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 7: Flip pure privacy decisions to use per-bot partner_share.",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 8: Scope dyadic raw-message reads by bot/topic in hot context and read tools.",
        "finalize_item_ids": [
          "T7",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 9: Rewrite dyadic hot-context partner-share state and labels.",
        "finalize_item_ids": [
          "T8"
        ]
      },
      {
        "plan_step_summary": "Step 10: Add cross-bot shareable-summary pull with provenance, recency ordering, and cap.",
        "finalize_item_ids": [
          "T8",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 11: Extend solo hot context with current-bot partner-share pending state and no partner content exposure.",
        "finalize_item_ids": [
          "T9"
        ]
      },
      {
        "plan_step_summary": "Step 12: Add canonical pending partner-sharing prompt slot once.",
        "finalize_item_ids": [
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 13: Wire canonical slot through mediator, generic solo/coach, and Tante Rosi prompt paths.",
        "finalize_item_ids": [
          "T11"
        ]
      },
      {
        "plan_step_summary": "Step 14: Extend memory tool schema/write path with visibility and shareable summary validation/persistence.",
        "finalize_item_ids": [
          "T12",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 15: Keep distillation contract bot-scoped and render partner/cross-bot rows as summaries only.",
        "finalize_item_ids": [
          "T12",
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Step 16: Update fake pool and existing fixtures/tests for bots, user_bot_state.partner_share, message bot/topic, and removed users column.",
        "finalize_item_ids": [
          "T13"
        ]
      },
      {
        "plan_step_summary": "Step 17: Add focused regression coverage for migration, privacy matrix, cross-bot independence, raw-message isolation, prompt slots, tools, and memory validation.",
        "finalize_item_ids": [
          "T13",
          "T14"
        ]
      },
      {
        "plan_step_summary": "Execution order and validation order: run stale-reference sweeps, focused pytest commands, full suite, and a throwaway reproduction script before finalizing.",
        "finalize_item_ids": [
          "T14"
        ]
      },
      {
        "plan_step_summary": "External rollout: apply migration/deploy and manual smoke test outside the local repo executor.",
        "finalize_item_ids": [
          "U1",
          "U2"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All approved numbered steps are mapped to execution tasks. The final task is intentionally verification-only and includes the required throwaway reproduction script, which must be deleted before completion. External DB migration/deploy and live smoke testing are captured as user actions because they require operator access outside repo editing.",
    "coverage_complete": true
  },
  "baseline_test_failures": [],
  "baseline_test_command": "pytest --tb=no -q --no-header",
  "baseline_test_note": "No baseline test run is part of finalization; executor should run the focused and full test commands in T14 after implementation."
}

        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-13T22:38:20Z",
  "hash": "sha256:05432fa119516bc986dddb970b914e341c2e7a56d92c576e03c85a0b0665a68b",
  "changes_summary": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
  "flags_addressed": [
    "correctness",
    "all_locations",
    "callers",
    "FLAG-005",
    "issue_hints",
    "scope"
  ],
  "questions": [],
  "success_criteria": [
    {
      "criterion": "Migration `0035_per_bot_partner_sharing.sql` guarantees `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    },
    {
      "criterion": "Migration `0035_per_bot_partner_sharing.sql` adds `user_bot_state.partner_share` with allowed values `opt_in`, `opt_out`, or NULL, and backfills non-NULL mediator values from `users.cross_thread_sharing_default` before dropping the old column.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Migration adds `memories.visibility`, `memories.shareable_summary`, and `memories.shareable_summary_encrypted`, with a database CHECK requiring non-empty shareable summaries for `dyad_shareable` memories.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "Production code has no remaining reads/writes of `users.cross_thread_sharing_default` and no `update_cross_thread_sharing_default` tool path after the rewrite.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files",
        "parse_diff"
      ]
    },
    {
      "criterion": "`partner_of`, `app/staging.py`, `app/models/user.py`, prompt renderers, read tools, write tools, registry, and scope guard are all updated to use per-bot partner_share or no sharing field.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_tests"
      ]
    },
    {
      "criterion": "Raw message reads in hot context, `search_messages`, and `recent_activity` are scoped to the message's bot/topic before partner visibility is applied, so one bot's opt-in cannot expose another bot's raw messages.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`raw_message_visibility()` and all callers use `user_bot_state.partner_share` for the relevant owner and relevant bot, with NULL and `opt_out` both blocking partner-visible raw content.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Partner hot context includes another user\u2019s `dyad_shareable` memories and distillations from any opted-in bot, renders only `shareable_summary`, and includes a provenance prefix derived from bot display names.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Hot context emits pending partner-sharing state only when the current user has a dyad partner and the current bot\u2019s partner_share is NULL or missing.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "The canonical pending-opt-in prompt slot is defined once and used by mediator, Tante Rosi, and generic solo/coach prompt paths.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`set_partner_sharing(opt_in: bool)` exists, is available in the record/write step for bots including Tante Rosi and coach, only upserts `(ctx.user.id, ctx.bot_id)`, and succeeds for `ctx.bot_id='tante_rosi'` against the migrated schema.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`add_memory` in root `tool_schemas.py` and `app/services/tools/write_tools.py` accepts `visibility` and `shareable_summary`, encrypts/persists the summary, and rejects `dyad_shareable` calls with missing or blank summaries.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "`TANTE_ROSI_BOT_ID` exists in `app/bots/ids.py` and Python code avoids new hard-coded Tante Rosi or mediator bot id strings where constants are available.",
      "priority": "must",
      "requires": [
        "read_files",
        "parse_diff",
        "run_shell"
      ]
    },
    {
      "criterion": "Tests cover NULL, `opt_out`, `opt_in`+private, `opt_in`+`dyad_shareable`, cross-bot independence, raw-message bot-scope isolation, no-partner pending-slot suppression, and Rosi partner-share FK success.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Cross-bot partner content has an explicit recency ordering rule and fixed global cap documented in code or tests.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Prompt and hot-context labels consistently use `partner_share` / `partner_sharing_state` terminology rather than stale `sharing_default` wording, except for intentional historical migration references.",
      "priority": "should",
      "requires": [
        "run_shell",
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Future work for re-asking after opt-out or finer per-topic sharing remains documented as out of scope and is not implemented opportunistically.",
      "priority": "info",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "The next migration remains `0035_per_bot_partner_sharing.sql` because the checkout currently ends at `0034_weekly_reflection.sql`.",
    "Seeding `bots(id='tante_rosi')` is not out-of-scope new bot registration; it is the narrow FK prerequisite for an existing in-scope bot to use `user_bot_state`.",
    "Legacy users with NULL `cross_thread_sharing_default` do not need explicit mediator `user_bot_state` rows; missing row and NULL both mean pending.",
    "Partner existence and partner user id are resolved from `dyads`/`dyad_members`.",
    "Raw messages are bot/topic scoped using existing `messages.bot_id` and `messages.topic_id`; current-bot partner_share never unlocks another bot's raw messages.",
    "Cross-bot sharing intentionally uses `recorded_by_bot_id` and shareable summaries, not raw message text.",
    "Cross-bot partner summaries are ordered by recency across all opted-in bots and capped globally.",
    "Tante Rosi should keep bridge/escalation tools excluded; per-bot sharing only affects `dyad_shareable` memories/distillations surfaced through hot context."
  ],
  "delta_from_previous_percent": 8.68,
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": true,
  "criteria_check": {
    "count": 17,
    "items": [
      {
        "criterion": "Migration `0035_per_bot_partner_sharing.sql` guarantees `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_tests"
        ]
      },
      {
        "criterion": "Migration `0035_per_bot_partner_sharing.sql` adds `user_bot_state.partner_share` with allowed values `opt_in`, `opt_out`, or NULL, and backfills non-NULL mediator values from `users.cross_thread_sharing_default` before dropping the old column.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Migration adds `memories.visibility`, `memories.shareable_summary`, and `memories.shareable_summary_encrypted`, with a database CHECK requiring non-empty shareable summaries for `dyad_shareable` memories.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "Production code has no remaining reads/writes of `users.cross_thread_sharing_default` and no `update_cross_thread_sharing_default` tool path after the rewrite.",
        "priority": "must",
        "requires": [
          "run_shell",
          "read_files",
          "parse_diff"
        ]
      },
      {
        "criterion": "`partner_of`, `app/staging.py`, `app/models/user.py`, prompt renderers, read tools, write tools, registry, and scope guard are all updated to use per-bot partner_share or no sharing field.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_tests"
        ]
      },
      {
        "criterion": "Raw message reads in hot context, `search_messages`, and `recent_activity` are scoped to the message's bot/topic before partner visibility is applied, so one bot's opt-in cannot expose another bot's raw messages.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`raw_message_visibility()` and all callers use `user_bot_state.partner_share` for the relevant owner and relevant bot, with NULL and `opt_out` both blocking partner-visible raw content.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Partner hot context includes another user\u2019s `dyad_shareable` memories and distillations from any opted-in bot, renders only `shareable_summary`, and includes a provenance prefix derived from bot display names.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "Hot context emits pending partner-sharing state only when the current user has a dyad partner and the current bot\u2019s partner_share is NULL or missing.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "The canonical pending-opt-in prompt slot is defined once and used by mediator, Tante Rosi, and generic solo/coach prompt paths.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`set_partner_sharing(opt_in: bool)` exists, is available in the record/write step for bots including Tante Rosi and coach, only upserts `(ctx.user.id, ctx.bot_id)`, and succeeds for `ctx.bot_id='tante_rosi'` against the migrated schema.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests",
          "parse_diff"
        ]
      },
      {
        "criterion": "`add_memory` in root `tool_schemas.py` and `app/services/tools/write_tools.py` accepts `visibility` and `shareable_summary`, encrypts/persists the summary, and rejects `dyad_shareable` calls with missing or blank summaries.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "`TANTE_ROSI_BOT_ID` exists in `app/bots/ids.py` and Python code avoids new hard-coded Tante Rosi or mediator bot id strings where constants are available.",
        "priority": "must",
        "requires": [
          "read_files",
          "parse_diff",
          "run_shell"
        ]
      },
      {
        "criterion": "Tests cover NULL, `opt_out`, `opt_in`+private, `opt_in`+`dyad_shareable`, cross-bot independence, raw-message bot-scope isolation, no-partner pending-slot suppression, and Rosi partner-share FK success.",
        "priority": "must",
        "requires": [
          "read_files",
          "run_tests"
        ]
      },
      {
        "criterion": "Cross-bot partner content has an explicit recency ordering rule and fixed global cap documented in code or tests.",
        "priority": "should",
        "requires": [
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Prompt and hot-context labels consistently use `partner_share` / `partner_sharing_state` terminology rather than stale `sharing_default` wording, except for intentional historical migration references.",
        "priority": "should",
        "requires": [
          "run_shell",
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "Future work for re-asking after opt-out or finer per-topic sharing remains documented as out of scope and is not implemented opportunistically.",
        "priority": "info",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "issue_hints-1",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the brief's requirement that the shared pending opt-in slot be used by every bot. The plan imports the canonical slot into the mediator and Tante Rosi renderers, but this repo already has a third BotSpec, `coach`, in `app/bots/coach.py`, which delegates to `app/services/prompts_solo.py`; the plan does not say to update that generic solo prompt path or otherwise guarantee coach/new solo bots inherit the slot.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "issue_hints-2",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the file locations named by the plan against the repository. The schemas live in the repository-root `tool_schemas.py`, while the plan repeatedly refers to `app/services/tools/tool_schemas.py`; an executor following the path literally will not find the file, though the surrounding registry imports make the intended target recoverable.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Checked the planned `set_partner_sharing` write shape against the current schema. The upsert target `(ctx.user.id, ctx.bot_id)` is the right authorization boundary, but it depends on the calling bot already existing in `bots` because `user_bot_state.bot_id` has a foreign key; that dependency is not satisfied for Tante Rosi by the current migration set.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched for `cross_thread_sharing_default` and found additional production users beyond the plan's focal list, notably `app/services/turn_context.py::partner_of` and `app/staging.py`. The plan covers user model hydration, `base.py`, prompts, hot context, and tools, and has a final `rg` sweep, but it does not explicitly call out `partner_of`; after the migration drops the column, that SELECT would fail unless the executor catches it in the sweep.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched read paths using raw-message sharing decisions and found `search_messages`, `recent_activity`, and `get_distillations` in `app/services/tools/read_tools.py` still derive sharing from `ctx.user.cross_thread_sharing_default`/`ctx.partner.cross_thread_sharing_default`. The plan has a broad Step 13 for read tools, but it does not explicitly require these read tools to batch-load `user_bot_state.partner_share` or apply bot/topic scope to message reads.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi.",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting database setup locations for bots. Migrations seed `mediator` in `0020_topics_bots_bindings.sql` and staging-only `coach` in `0031_coach_staging_seed.sql`, but no migration seeds `tante_rosi`; since the new feature writes `user_bot_state` rows for Rosi, the plan is missing supporting infrastructure for the bot registry/database FK boundary.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked callers that will invoke the new `set_partner_sharing` tool. The plan correctly removes user_id/bot_id from the input and derives both from `ctx`, but for any caller with `ctx.bot_id='tante_rosi'` the database upsert still requires a matching `bots` row; the plan does not guarantee that prerequisite.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the plan's stated support for `set_partner_sharing` on Tante Rosi against the migrations. `user_bot_state.bot_id` references `bots(id)`, but the current migrations insert only `mediator` and staging-only `coach`; `0033_pregnancy_topic.sql` creates the pregnancy topic but no `tante_rosi` bot row. The plan does not add or require that bot row, so Rosi's partner-share upsert can fail on a real DB even though the tool is wired.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    },
    {
      "id": "scope",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched bot registration and schema support for partner-share state. The current registry can expose Tante Rosi under `STAGING=1` without a database `bots` row, while prod registration requires row existence; because partner sharing writes through a foreign-keyed `user_bot_state` row, the plan's scope should include seeding or validating `bots(id='tante_rosi')` wherever Rosi is callable.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary.",
      "raised_in": "critique_v2.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v3.md"
    }
  ],
  "recommendation": "PROCEED",
  "rationale": "The plan is now execution-ready. The first-round privacy and all-location gaps were fixed in v2, and the remaining database FK prerequisite for Tante Rosi was fixed in v3 by requiring `bots(id='tante_rosi')` to be guaranteed in migration `0035` before any Rosi `user_bot_state` upsert. The remaining significant flags are marked addressed, and the critique check is clear across issue hints, correctness, scope, all-locations, and callers.",
  "signals_assessment": "Score moved 10.5 -> 11.5 -> 10.0 with a large v2 correction and a focused v3 correction. All significant flags are now addressed, with no reopened critiques and no open critique category. Preflight is clean: project exists, workspace is writable, success criteria are present, and tools are available. The only recurring note is subjective verification of the cross-bot ordering/cap criterion, which is a review check rather than a plan blocker.",
  "warnings": [
    "During execution, verify migration `0035` seeds or guarantees `bots(id='tante_rosi')` before any Rosi `user_bot_state` write path is tested.",
    "Keep raw messages strictly same-bot/topic scoped; cross-bot partner sharing should render only shareable summaries.",
    "Run the stale-reference sweeps before final validation because the migration drops `users.cross_thread_sharing_default`."
  ],
  "settled_decisions": [
    {
      "id": "tante-rosi-fk",
      "decision": "Migration `0035` must guarantee `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows.",
      "rationale": "`user_bot_state.bot_id` references `bots(id)`, and Rosi is explicitly in scope for partner sharing."
    },
    {
      "id": "raw-message-boundary",
      "decision": "Raw messages are scoped to same bot/topic before partner-share visibility is applied.",
      "rationale": "Current-bot opt-in must not expose another bot's raw messages; cross-bot sharing uses summaries only."
    },
    {
      "id": "schema-target",
      "decision": "Tool schema edits target root `tool_schemas.py`.",
      "rationale": "That is the actual schema file in this repo."
    },
    {
      "id": "prompt-inheritance",
      "decision": "The canonical pending slot is wired through mediator, Tante Rosi, and generic solo/coach prompt paths.",
      "rationale": "The brief requires every bot to inherit the shared prompt slot."
    },
    {
      "id": "partner-source",
      "decision": "Partner resolution uses `dyads`/`dyad_members`.",
      "rationale": "The current schema does not have `users.partner_user_id`."
    },
    {
      "id": "migration-number",
      "decision": "Use `0035_per_bot_partner_sharing.sql` if the checkout still ends at `0034_weekly_reflection.sql`.",
      "rationale": "The migration chain has advanced beyond the brief's stale numbering hint."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Plan passed gate and preflight. Proceed to finalize. Verify unresolved flags against the plan and project code before accepting. Recurring critiques (criterion 14: requires human verification (subjective_judgment).); the loop likely can't fix these, so judge if they are real blockers.",
  "robustness": "standard",
  "signals": {
    "iteration": 3,
    "idea": "# Per-bot partner sharing \u2014 design brief\n\n## Context\n\nThe Veas codebase runs N bots that each occupy a \"domain\" for a user (currently: `mediator` = relationship coach for a dyad on topic=relationship; `tante_rosi` = solo pregnancy coach on topic=pregnancy; more bots planned). Today only the mediator's content can flow between dyad partners, gated by a **global** opt-in (`users.cross_thread_sharing_default`). The pregnancy coach writes everything private; her facts cannot reach the partner even when the user wants to share them.\n\nWe want to generalise partner-sharing so that **every bot** (current and future) can produce content that the user's partner sees, gated by a **per-bot** opt-in. The user gets one switch per domain (\"share my pregnancy stuff with my partner \u2014 yes / no / not decided yet\"). Until they decide, the bot keeps surfacing the question.\n\nThe basic infrastructure already exists for distillations (`visibility: private | dyad_shareable`, `shareable_summary`, `raw_message_visibility()` filtering in `app/services/cross_thread_privacy.py`, `app/services/hot_context.py:500-577`). The work below generalises it across both bots-and-content-types, and replaces the global toggle with a per-bot one.\n\n## Goal (one sentence)\n\nReplace the single global `users.cross_thread_sharing_default` with per-bot opt-in state on `user_bot_state`, extend `dyad_shareable` visibility to `memories` (today it only exists on `distillations`), and rewire the hot-context read path so a partner sees `dyad_shareable` content from any bot where the content's owner has opted in for *that* bot \u2014 with NULL (\"not decided\") triggering a prompt-slot the bot uses to ask.\n\n## Decisions already made (do not re-litigate)\n\nThese are settled \u2014 the plan should implement them, not re-debate them.\n\n1. **Per-bot opt-in lives on `user_bot_state`** as one new column `partner_share text` with values `'opt_in' | 'opt_out' | NULL`. NULL = \"pending, must ask\". Key is `(user_id, bot_id)` \u2014 same shape as every other per-bot state today.\n2. **Memories get `visibility` and `shareable_summary`** mirroring distillations exactly. Default `visibility='private'`. When `visibility='dyad_shareable'`, `shareable_summary` is required.\n3. **The opt-in is shown until decided.** While `partner_share IS NULL`, every render of that bot's hot context includes a \"pending opt-in\" slot in the system prompt asking the bot to raise the question this turn. As soon as the value is non-NULL (`opt_in` OR `opt_out`), the slot drops out and the bot stops raising it.\n4. **One shared prompt slot, used by every bot.** Define one canonical pending-opt-in paragraph used by every bot's `render_system_prompt`. Rosi's existing `_FIRST_CONTACT_V1` collapses into it; the mediator's onboarding language for cross-thread sharing also collapses into it. New bots inherit the slot for free \u2014 no per-bot prompt work.\n5. **One shared tool: `set_partner_sharing(opt_in: bool)`.** Implicit `bot_id` (from the calling bot's scope). Writes to `user_bot_state.partner_share` for the calling (user, bot) pair.\n6. **Migration: the existing global flag goes away.** Backfill `user_bot_state[bot_id='mediator', user_id=X].partner_share` from `users.cross_thread_sharing_default` for every existing user, then drop `users.cross_thread_sharing_default`. One model, not two \u2014 no fallback path, no two-system-running period.\n7. **No per-row UX in v1.** The user gets the per-bot toggle. The bot decides per-call whether a given memory/distillation should be `private` vs `dyad_shareable` based on the content. No user-facing per-row controls.\n8. **Hot context cross-bot pull is in scope.** When rendering for user B (the partner of A), pull A's `dyad_shareable` rows from *any* bot where `partner_share[A, that_bot] = 'opt_in'`, surfaced with a provenance prefix (e.g. `from Rosi:`). Same-bot dyad sharing (the existing mediator behaviour) keeps working unchanged in shape, just driven by the new column.\n\n## Files known to be relevant (planner should read at least these)\n\nThe planner should still survey the repo, but these are the focal points:\n\n- `migrations/0012_cross_thread_sharing.sql` \u2014 defines the global flag being retired.\n- `migrations/0015_distillations.sql` \u2014 defines `visibility` + `shareable_summary` we're mirroring onto memories.\n- `migrations/0022_topic_status_user_bot_state.sql` \u2014 defines `user_bot_state` (current schema: `user_id, bot_id, onboarding_state, paused`).\n- The next available migration number is `0020` (or whatever is highest after `0019_feedback_reaction_context.sql`); planner should verify.\n- `app/services/cross_thread_privacy.py` \u2014 `raw_message_visibility()` lives here; needs to flip from global flag to per-bot lookup.\n- `app/services/hot_context.py` (especially lines 500-577) \u2014 read path; needs (a) per-bot lookup, (b) cross-bot pull for partner, (c) emitting the `partner_sharing_state: 'pending'` signal.\n- `app/services/tools/write_tools.py` \u2014 `add_memory` (~line 776) and `add_distillation` (~line 1165). The `add_memory` write helper needs to accept `visibility` + `shareable_summary`.\n- `app/services/tools/tool_schemas.py` \u2014 `AddMemoryInput` needs new fields mirroring `AddDistillationInput.visibility` etc. (~line 996 for the distillation schema as the template).\n- `app/bots/mediator.py` and `app/bots/tante_rosi.py` \u2014 both need to (a) include the canonical pending-opt-in slot via their `render_system_prompt`, (b) be eligible to call `set_partner_sharing`. Rosi additionally needs prompt language about *when* to write `dyad_shareable` rows once opted in.\n- `app/bots/prompts/tante_rosi.py` (`_FIRST_CONTACT_V1`) and the equivalent mediator prompt file \u2014 the canonical slot replaces/absorbs whatever a[REDACTED_SK] language already exists in each.\n- `app/bots/` tool dispatch \u2014 wherever bot tool allowlists are wired, `set_partner_sharing` must be available to every bot (it's user-state-modifying, like `set_pregnancy_edd`, not domain-specific).\n\n## Invariants to enforce (must hold)\n\n1. **NULL \u2192 silent.** When `partner_share IS NULL`, *no* content from that (user, bot) is shared with the partner regardless of per-row `visibility`. The toggle is the gate; per-row visibility only matters when the toggle is `opt_in`.\n2. **opt_out \u2192 silent.** Same as NULL for the read path. The only difference is the prompt slot doesn't surface.\n3. **opt_in \u2192 per-row decides.** When the toggle is `opt_in`, dyad_shareable rows from that bot flow to the partner; private rows don't.\n4. **No partner \u2192 moot.** When the user has no partner (`users.partner_user_id IS NULL`), the prompt slot is suppressed even with `partner_share IS NULL`. Nothing to share to. Don't ask a question that has no answer.\n5. **No backsliding on the mediator.** Every existing mediator user must continue to see exactly what they see today \u2014 the migration must be observationally equivalent. A user whose current `cross_thread_sharing_default = 'opt_in'` ends up with `user_bot_state[mediator].partner_share = 'opt_in'`; a user with `'opt_out'` ends up `'opt_out'`; NULL stays NULL.\n6. **Cross-bot pull is opt-in-gated, not opt-out-gated.** Default is \"don't show partner's other-bot content.\" Only `'opt_in'` from the content owner unlocks the pull. This matters: a partner who hasn't decided cannot accidentally have their content surfaced because of someone *else's* default.\n7. **Tool authorisation.** `set_partner_sharing` writes only to the calling user's row for the calling bot. A user calling Rosi cannot toggle their mediator state; Rosi cannot toggle V\u00e9as's state. Scope is `(message.sender_id, message.bot_id)`.\n8. **The shareable_summary contract.** When `add_memory` or `add_distillation` is called with `visibility='dyad_shareable'`, `shareable_summary` must be non-null and non-empty. Reject the call otherwise. Same rule that already applies to distillations should now apply to memories.\n\n## Edge cases and ordering concerns\n\nThe planner should treat these as real, not paranoid:\n\n- **Migration backfill ordering.** The new column on `user_bot_state` must be added and backfilled before `cross_thread_sharing_default` is dropped. The hot-context read path must be flipped to the new column *atomically* with the drop, or the system briefly reads from a dropped column. Plan the migration as a single transaction or with explicit phasing.\n- **Backfill for users without a `user_bot_state[mediator]` row.** Some legacy users may not have a `user_bot_state` row for the mediator yet (it may be created lazily on first message). The migration must create rows for any user with a non-NULL `cross_thread_sharing_default`. For users with NULL global setting, decide: either create rows pre-set to NULL (explicit pending state) or skip (lazy creation later, still NULL). Either is defensible \u2014 make a call and write it down.\n- **The pending slot wording is shared.** Different bots have different voices. The shared slot must be voice-agnostic \u2014 short, neutral, instructive to the model, not user-facing copy. The bot's own voice handles the actual question to the user; the slot just tells the bot \"raise this naturally this turn.\"\n- **Cross-bot pull volume.** A partner with several opted-in bots could see a long list of \"from X:\" rows in their hot context. Budget for hot-context length: cap, summarise, or rank. Don't ship a context bomb.\n- **Order of cross-bot content.** When pulling rows from multiple bots, by what order? By recency? By bot? Pick one and write it down so the reviewer can check it.\n- **Provenance prefix format.** \"from Rosi:\" / \"from V\u00e9as:\" \u2014 bake into a single helper, not sprinkled. Bots are named via the bot registry; use the registry's display name, not a hard-coded string.\n\n## Explicitly out of scope\n\n- Per-row visibility controls exposed to the user. (The bot decides per-row; users only decide per-bot.)\n- Re-asking after some time has passed. Once `opt_in` or `opt_out` is set, the slot stays gone. Future work, not this sprint.\n- New bot registration code. The pattern must work for new bots when they show up, but we are not adding a new bot in this sprint.\n- Per-topic granularity within a bot. Each bot is one domain; one toggle per bot is enough.\n- UI surfaces. There is no UI today and we are not building one.\n- Encryption-at-rest changes. `shareable_summary` on memories follows whatever the existing memory content encryption pattern is.\n\n## Success criteria\n\nReviewer should check, in priority order:\n\n**must**\n- Migration adds `user_bot_state.partner_share` and backfills it from `users.cross_thread_sharing_default` for every user where the global flag was non-NULL, preserving the same value semantically (`'opt_in' \u2192 'opt_in'`, `'opt_out' \u2192 'opt_out'`).\n- Migration adds `memories.visibility` (default `'private'`) and `memories.shareable_summary` (nullable) with a CHECK constraint matching the existing distillations one (`shareable_summary` required iff `visibility='dyad_shareable'`).\n- Migration drops `users.cross_thread_sharing_default` only after the read path is updated.\n- `cross_thread_privacy.raw_message_visibility()` (and any other reader of the old column) reads from `user_bot_state.partner_share` for the relevant bot, not from `users.cross_thread_sharing_default`.\n- `hot_context.py` cross-bot pull lands: when rendering for partner B, B sees A's `dyad_shareable` memories and distillations from any bot where `partner_share[A, that_bot]='opt_in'`, with a provenance prefix from the bot registry.\n- `hot_context.py` emits `partner_sharing_state: 'pending'` when `partner_share IS NULL` and the user has a partner; the canonical prompt slot is rendered into the system prompt of any bot whose hot context carries this signal.\n- `set_partner_sharing` tool exists, is wired into the tool registry for every bot, and updates `user_bot_state.partner_share` for the calling `(user, bot)` only.\n- `add_memory` accepts `visibility` and `shareable_summary`; rejects `dyad_shareable` without `shareable_summary`.\n- Rosi's prompt is updated so that when `partner_share='opt_in'`, she writes `dyad_shareable` memories and distillations for non-sensitive facts (with appropriate `shareable_summary`).\n- Mediator's existing partner-sharing onboarding language is collapsed into the canonical slot; mediator continues to behave observationally as today for existing users post-migration.\n- Tests cover: NULL \u2192 no partner content visible; `opt_out` \u2192 no partner content visible; `opt_in` + `private` row \u2192 no partner content visible; `opt_in` + `dyad_shareable` row \u2192 partner content visible with provenance; cross-bot pull respects toggle independently per bot; user with no partner never sees the pending slot.\n\n**should**\n- Cross-bot content ordering and length budget are explicit (chosen rule, written down in code or comment).\n- Migration is a single transaction or has explicit phasing documented.\n- The canonical prompt slot is defined in one place and imported by both bot prompt files.\n\n**info**\n- Future work for re-asking or per-topic granularity is captured (e.g., as a ticket via `megaplan ticket new`) but not implemented.\n\n## Notes for the planner\n\n- **Do not invent new bot-ID strings.** Use the existing `bot_id` constants from `app/bots/ids.py`.\n- **Do not gate behaviour on bot identity if it can be data-driven.** The whole point is N bots; if Rosi gets a code path that V\u00e9as doesn't, that's a smell. The only legitimate per-bot differences are prompt content and topic, both of which are already data-driven.\n- **The pending slot's prompt language matters.** Write it once, write it well, and stop. Bots are instructed *what* to do (raise the question this turn), not *how* to phrase it \u2014 voice belongs to each bot.\n- **The migration is the riskiest piece.** Get the ordering and the backfill right and the rest is mechanical.",
    "significant_flags": 9,
    "unresolved_flags": [
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the brief's requirement that the shared pending opt-in slot be used by every bot. The plan imports the canonical slot into the mediator and Tante Rosi renderers, but this repo already has a third BotSpec, `coach`, in `app/bots/coach.py`, which delegates to `app/services/prompts_solo.py`; the plan does not say to update that generic solo prompt path or otherwise guarantee coach/new solo bots inherit the slot.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the file locations named by the plan against the repository. The schemas live in the repository-root `tool_schemas.py`, while the plan repeatedly refers to `app/services/tools/tool_schemas.py`; an executor following the path literally will not find the file, though the surrounding registry imports make the intended target recoverable.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Checked the planned `set_partner_sharing` write shape against the current schema. The upsert target `(ctx.user.id, ctx.bot_id)` is the right authorization boundary, but it depends on the calling bot already existing in `bots` because `user_bot_state.bot_id` has a foreign key; that dependency is not satisfied for Tante Rosi by the current migration set.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched for `cross_thread_sharing_default` and found additional production users beyond the plan's focal list, notably `app/services/turn_context.py::partner_of` and `app/staging.py`. The plan covers user model hydration, `base.py`, prompts, hot context, and tools, and has a final `rg` sweep, but it does not explicitly call out `partner_of`; after the migration drops the column, that SELECT would fail unless the executor catches it in the sweep.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched read paths using raw-message sharing decisions and found `search_messages`, `recent_activity`, and `get_distillations` in `app/services/tools/read_tools.py` still derive sharing from `ctx.user.cross_thread_sharing_default`/`ctx.partner.cross_thread_sharing_default`. The plan has a broad Step 13 for read tools, but it does not explicitly require these read tools to batch-load `user_bot_state.partner_share` or apply bot/topic scope to message reads.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked supporting database setup locations for bots. Migrations seed `mediator` in `0020_topics_bots_bindings.sql` and staging-only `coach` in `0031_coach_staging_seed.sql`, but no migration seeds `tante_rosi`; since the new feature writes `user_bot_state` rows for Rosi, the plan is missing supporting infrastructure for the bot registry/database FK boundary.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked callers that will invoke the new `set_partner_sharing` tool. The plan correctly removes user_id/bot_id from the input and derives both from `ctx`, but for any caller with `ctx.bot_id='tante_rosi'` the database upsert still requires a matching `bots` row; the plan does not guarantee that prerequisite.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the plan's stated support for `set_partner_sharing` on Tante Rosi against the migrations. `user_bot_state.bot_id` references `bots(id)`, but the current migrations insert only `mediator` and staging-only `coach`; `0033_pregnancy_topic.sql` creates the pregnancy topic but no `tante_rosi` bot row. The plan does not add or require that bot row, so Rosi's partner-share upsert can fail on a real DB even though the tool is wired.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Searched bot registration and schema support for partner-share state. The current registry can expose Tante Rosi under `STAGING=1` without a database `bots` row, while prod registration requires row existence; because partner sharing writes through a foreign-keyed `user_bot_state` row, the plan's scope should include seeding or validating `bots(id='tante_rosi')` wherever Rosi is callable.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Correctness: dyadic raw-message reads are not explicitly scoped to the message's bot/topic before applying per-bot sharing. Since `hot_context.py` currently reads all messages involving either partner without a `bot_id` predicate, using the current bot's `partner_share` as the gate can leak another bot's raw messages when the owner opted into mediator but not that other bot.",
        "resolution": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi."
      },
      {
        "id": "FLAG-002",
        "concern": "Completeness: the canonical pending opt-in slot is planned for mediator and Tante Rosi, but not for the existing generic solo/coach prompt path, despite the requirement that every bot inherit the shared slot.",
        "resolution": "`app/bots/coach.py` defines a live BotSpec that renders via `app/services/prompts_solo.py`; plan Step 7 names importing the slot from mediator and Rosi prompt renderers, and Step 9 only updates Rosi-specific solo prompt code."
      },
      {
        "id": "FLAG-003",
        "concern": "Completeness: production readers of the dropped user column are not all explicitly enumerated. `partner_of` and several read-tool paths still select or consume `cross_thread_sharing_default`, so relying on the final grep sweep is brittle for a migration that drops the column.",
        "resolution": "Revised the plan to close the significant critique gaps: raw message reads are now explicitly same-bot/topic scoped, all known dropped-column readers are named, the generic solo/coach prompt path inherits the canonical slot, schema file paths are corrected to root `tool_schemas.py`, and bot id constants are added/used for Tante Rosi."
      },
      {
        "id": "FLAG-004",
        "concern": "Maintainability: the plan references a non-existent `app/services/tools/tool_schemas.py` path and literal bot id strings even though this repo's schema file is root-level `tool_schemas.py` and only mediator has a bot id constant today.",
        "resolution": "`rg --files` shows `tool_schemas.py` at repository root and no `app/services/tools/tool_schemas.py`; `app/bots/ids.py` contains `MEDIATOR_BOT_ID` only, while `app/bots/tante_rosi.py` currently uses literal `bot_id='tante_rosi'`."
      },
      {
        "id": "FLAG-005",
        "concern": "Completeness: Tante Rosi is planned to call `set_partner_sharing`, but the database migrations do not seed a `bots(id='tante_rosi')` row. Because `user_bot_state.bot_id` has a foreign key to `bots(id)`, partner-share upserts for Rosi can fail in real databases where Rosi is registered from code or expected to be current.",
        "resolution": "Added the missing database prerequisite for Tante Rosi: the migration must seed or guarantee `bots(id='tante_rosi')` before `set_partner_sharing` can upsert `user_bot_state` rows. Updated tests, success criteria, and execution order to verify the FK boundary."
      }
    ],
    "weighted_score": 10.0,
    "weighted_history": [
      10.5,
      11.5
    ],
    "plan_delta_from_previous": 8.68,
    "recurring_critiques": [
      "criterion 14: requires human verification (subjective_judgment)."
    ],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 3. Weighted score trajectory: 10.5 -> 11.5 -> 10.0. Plan deltas: 88.7%, 8.7%. Recurring critiques: 1. Resolved flags: 5. Open significant flags: 9.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [
    {
      "flag_id": "issue_hints-1",
      "action": "dispute",
      "evidence": "Plan v3 Step 13 explicitly wires the canonical slot through `app/services/prompts_solo.py`, `app/bots/coach.py`, and `app/bots/tante_rosi.py`, in addition to mediator prompts.",
      "rationale": ""
    },
    {
      "flag_id": "issue_hints-2",
      "action": "dispute",
      "evidence": "Plan v3 Overview and Steps 5, 14, and 15 refer to root `tool_schemas.py`, not `app/services/tools/tool_schemas.py`.",
      "rationale": ""
    },
    {
      "flag_id": "correctness",
      "action": "dispute",
      "evidence": "Plan v3 Step 2.2 requires inserting `bots(id, display_name)` row `('tante_rosi', 'Tante Rosi')` before adding/using partner-share state; Step 17 also requires a Rosi FK success test.",
      "rationale": ""
    },
    {
      "flag_id": "scope-1",
      "action": "dispute",
      "evidence": "Plan v3 Step 4 explicitly updates `app/services/turn_context.py::partner_of` and `app/staging.py` to stop selecting or using the dropped user column.",
      "rationale": ""
    },
    {
      "flag_id": "scope-2",
      "action": "dispute",
      "evidence": "Plan v3 Step 8 explicitly names `search_messages`, `recent_activity`, and `get_distillations` and requires per-bot partner-share loading plus bot/topic message scoping.",
      "rationale": ""
    },
    {
      "flag_id": "all_locations",
      "action": "dispute",
      "evidence": "Plan v3 Step 2.2 guarantees a `bots(id='tante_rosi')` row in migration `0035`; Step 16 adds fake-pool bot row support; Step 17 requires SQL assertions for the row.",
      "rationale": ""
    },
    {
      "flag_id": "callers",
      "action": "dispute",
      "evidence": "Plan v3 Step 5.7 adds a targeted `set_partner_sharing` test for `ctx.bot_id=TANTE_ROSI_BOT_ID` against a migrated/fake DB where the bot row exists.",
      "rationale": ""
    },
    {
      "flag_id": "issue_hints",
      "action": "dispute",
      "evidence": "Plan v3 success criterion 1 requires migration `0035` to guarantee `bots(id='tante_rosi')` before Rosi `user_bot_state` writes, and success criterion 11 requires Rosi tool success against the migrated schema.",
      "rationale": ""
    },
    {
      "flag_id": "scope",
      "action": "dispute",
      "evidence": "Plan v3 explicitly treats seeding `bots(id='tante_rosi')` as the narrow FK prerequisite for the existing in-scope Rosi bot, not as broad new bot registration.",
      "rationale": ""
    }
  ],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Settled decisions (verify the executor implemented these correctly):
- tante-rosi-fk: Migration `0035` must guarantee `bots(id='tante_rosi')` exists before `set_partner_sharing` can write Rosi `user_bot_state` rows. (`user_bot_state.bot_id` references `bots(id)`, and Rosi is explicitly in scope for partner sharing.)
- raw-message-boundary: Raw messages are scoped to same bot/topic before partner-share visibility is applied. (Current-bot opt-in must not expose another bot's raw messages; cross-bot sharing uses summaries only.)
- schema-target: Tool schema edits target root `tool_schemas.py`. (That is the actual schema file in this repo.)
- prompt-inheritance: The canonical pending slot is wired through mediator, Tante Rosi, and generic solo/coach prompt paths. (The brief requires every bot to inherit the shared prompt slot.)
- partner-source: Partner resolution uses `dyads`/`dyad_members`. (The current schema does not have `users.partner_user_id`.)
- migration-number: Use `0035_per_bot_partner_sharing.sql` if the checkout still ends at `0034_weekly_reflection.sql`. (The migration chain has advanced beyond the brief's stale numbering hint.)


Critique flags to re-verify against the final diff:
            [
  {
    "id": "FLAG-001",
    "concern": "Correctness: dyadic raw-message reads are not explicitly scoped to the message's bot/topic before applying per-bot sharing. Since `hot_context.py` currently reads all messages involving either partner without a `bot_id` predicate, using the current bot's `partner_share` as the gate can leak another bot's raw messages when the owner opted into mediator but not that other bot.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-002",
    "concern": "Completeness: the canonical pending opt-in slot is planned for mediator and Tante Rosi, but not for the existing generic solo/coach prompt path, despite the requirement that every bot inherit the shared slot.",
    "severity": "minor",
    "status": "verified"
  },
  {
    "id": "FLAG-003",
    "concern": "Completeness: production readers of the dropped user column are not all explicitly enumerated. `partner_of` and several read-tool paths still select or consume `cross_thread_sharing_default`, so relying on the final grep sweep is brittle for a migration that drops the column.",
    "severity": "significant",
    "status": "verified"
  },
  {
    "id": "FLAG-004",
    "concern": "Maintainability: the plan references a non-existent `app/services/tools/tool_schemas.py` path and literal bot id strings even though this repo's schema file is root-level `tool_schemas.py` and only mediator has a bot id constant today.",
    "severity": "minor",
    "status": "verified"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 14: requires human verification (subjective_judgment).",
    "severity": "minor",
    "status": "disputed"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 15: requires human verification (subjective_judgment).",
    "severity": "minor",
    "status": "disputed"
  },
  {
    "id": "FLAG-005",
    "concern": "Completeness: Tante Rosi is planned to call `set_partner_sharing`, but the database migrations do not seed a `bots(id='tante_rosi')` row. Because `user_bot_state.bot_id` has a foreign key to `bots(id)`, partner-share upserts for Rosi can fail in real databases where Rosi is registered from code or expected to be current.",
    "severity": "significant",
    "status": "verified"
  }
]

            For each flag above that was raised during critique, verify whether the final diff actually addresses the concern.
            A flag is resolved only if the final diff contains code that directly addresses the concern.
            Do not trust pre-execute promises or plan claims; check the diff itself.
            Add resolved flag IDs to `verified_flag_ids`.
            For any unresolved flag, add a `rework_items` entry with `task_id: "REVIEW"`, `issue`, `expected`, `actual`, `evidence_file`, `flag_id`, and `source: "review_flag_reverify"`.

Advisory mechanical pre-check flags:
            [
  {
    "id": "PRECHECK-DIFF_SIZE_SANITY",
    "check": "diff_size_sanity",
    "detail": "Diff size looks larger than expected: changed_lines=9143, expected\u224810, ratio=914.30, files=55, hunks=690.",
    "severity": "significant",
    "evidence_file": "app/bots/base.py"
  }
]

            Copy this list verbatim into the output `pre_check_flags` field.

        Execution summary:
        {
  "output": "Aggregated execute batches: completed 1/1.\nBatch 1: Implemented the rework: cross-bot partner-shareable summaries are now opt-in gated before recency ordering and the global cap, and the starvation regression is covered.",
  "commands_run": [
    "python -m black app/services/hot_context.py tests/test_hot_context.py tests/conftest.py",
    "rg -n \"CROSS_BOT_SHAREABLE_CANDIDATE_CAP|WITH partner_rows AS|partner_share = 'opt_in'\" app/services/hot_context.py tests/test_hot_context.py tests/conftest.py",
    "python -m py_compile app/services/hot_context.py tests/test_hot_context.py tests/conftest.py && pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q",
    "python tmp_partner_shareable_starvation_repro.py",
    "test ! -e tmp_partner_shareable_starvation_repro.py && echo deleted",
    "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py",
    "rg -n \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py",
    "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
    "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
    "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
    "python scripts/lint_artifact_reads.py --dir app",
    "pytest -q"
  ],
  "deviations": [
    "The checkpoint file path did not exist, so no progress checkpoint was written; structured output contains the authoritative evidence.",
    "Full `pytest -q` still fails in the previously documented `tests/test_decay.py` fake-pool observation UPDATE failures: `test_decay_housekeeping_transitions_against_synthetic_time`, `test_decay_only_touches_rows_for_current_topic`, and `test_decay_scopes_when_explicit_topic_passed`. I did not fix these unrelated failures.",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_coach_e2e.py, tests/test_cross_topic_peek_wired.py, tests/test_cross_topic_status_injection.py, tests/test_hot_context_cross_topic.py, tests/test_messaging_non_agentic_bot_id.py, tests/test_multi_topic_writes.py, tests/test_partner_sharing_migration.py, tests/test_per_bot_telemetry.py, tests/test_pregnancy_tools.py, tests/test_pregnancy_user_model.py, tests/test_write_tools_solo_bot_guard.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_coach_e2e.py, tests/test_cross_topic_peek_wired.py, tests/test_cross_topic_status_injection.py, tests/test_hot_context_cross_topic.py, tests/test_messaging_non_agentic_bot_id.py, tests/test_multi_topic_writes.py, tests/test_partner_sharing_migration.py, tests/test_per_bot_telemetry.py, tests/test_pregnancy_tools.py, tests/test_pregnancy_user_model.py, tests/test_write_tools_solo_bot_guard.py"
  ],
  "task_updates": [
    {
      "task_id": "T8",
      "status": "done",
      "executor_notes": "Reworked `_fetch_partner_shareable_summaries` so the owner/bot `partner_share='opt_in'` gate is applied in SQL through `user_bot_state` before recency ordering and the fixed 12-row cap. Both memory and distillation branches exclude non-opted-in and current-bot rows before `LIMIT`, so newer opt-out rows cannot starve older opted-in summaries.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "python -m black app/services/hot_context.py tests/test_hot_context.py tests/conftest.py",
        "python -m py_compile app/services/hot_context.py tests/test_hot_context.py tests/conftest.py && pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T13",
      "status": "done",
      "executor_notes": "Added regression coverage for the reviewed starvation edge case: 60 newer opt-out coach rows no longer hide one older opted-in Rosi summary. Updated the fake pools so they model production behavior by partner-share filtering before sorting and limiting.",
      "files_changed": [
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q"
      ],
      "auto_attributed_files": null
    },
    {
      "task_id": "T14",
      "status": "done",
      "executor_notes": "Final re-verification completed after the starvation fix. Stale-reference sweeps were clean, focused schema/tool/hot-context/prompt/migration/partner-sharing suites passed, `lint_artifact_reads` passed, and the throwaway starvation reproduction script passed then was deleted. Full pytest still fails only in the known unrelated decay fake-pool failures.",
      "files_changed": [
        "app/services/hot_context.py",
        "tests/conftest.py",
        "tests/test_hot_context.py"
      ],
      "commands_run": [
        "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default\" app tool_schemas.py",
        "rg -n \"current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py",
        "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
        "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
        "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
        "python scripts/lint_artifact_reads.py --dir app",
        "pytest -q"
      ],
      "auto_attributed_files": null
    }
  ],
  "sense_check_acknowledgments": [
    {
      "sense_check_id": "SC1",
      "executor_note": "No changes in this pass; prior migration evidence remains unchanged."
    },
    {
      "sense_check_id": "SC2",
      "executor_note": "No changes in this pass; shared helper behavior remains unchanged."
    },
    {
      "sense_check_id": "SC3",
      "executor_note": "Stale-reference sweeps over `app` and `tool_schemas.py` remained clean."
    },
    {
      "sense_check_id": "SC4",
      "executor_note": "No changes in this pass; `set_partner_sharing` wiring remains unchanged."
    },
    {
      "sense_check_id": "SC5",
      "executor_note": "Confirmed with clean stale-reference sweeps for old sharing field/tool and stale sharing-default terminology."
    },
    {
      "sense_check_id": "SC6",
      "executor_note": "No changes in this pass; raw visibility behavior remains covered by focused tests."
    },
    {
      "sense_check_id": "SC7",
      "executor_note": "Focused hot-context and partner-sharing tests still pass after the query rework."
    },
    {
      "sense_check_id": "SC8",
      "executor_note": "Confirmed after rework. Cross-bot memory/distillation summaries now join `user_bot_state` with `partner_share='opt_in'` before recency ordering and the 12-row cap, with provenance rendering preserved."
    },
    {
      "sense_check_id": "SC9",
      "executor_note": "No changes in this pass; solo hot-context behavior remains covered by focused tests."
    },
    {
      "sense_check_id": "SC10",
      "executor_note": "No changes in this pass; canonical prompt slot remains unchanged."
    },
    {
      "sense_check_id": "SC11",
      "executor_note": "Prompt/allowlist focused suite passed after the rework."
    },
    {
      "sense_check_id": "SC12",
      "executor_note": "Schema/tool focused tests passed after the rework."
    },
    {
      "sense_check_id": "SC13",
      "executor_note": "Confirmed for the previously missing edge case. Regression coverage now proves non-opted-in newer rows cannot starve valid opted-in summaries before the cap."
    },
    {
      "sense_check_id": "SC14",
      "executor_note": "Confirmed after final verification. The throwaway starvation reproduction passed and was deleted; stale-reference sweeps and focused suites passed; full pytest still has only the known `tests/test_decay.py` fake-pool UPDATE failures."
    }
  ],
  "files_changed": [
    "app/services/hot_context.py",
    "tests/conftest.py",
    "tests/test_hot_context.py"
  ]
}

        Execution audit (`execution_audit.json`):
            {
  "findings": [
    "Git status shows changed files not claimed by any task: megaplans/, scripts/import_chatgpt.py, supabase/, tests/test_coach_e2e.py, tests/test_cross_topic_peek_wired.py, tests/test_cross_topic_status_injection.py, tests/test_hot_context_cross_topic.py, tests/test_messaging_non_agentic_bot_id.py, tests/test_multi_topic_writes.py, tests/test_partner_sharing_migration.py, tests/test_per_bot_telemetry.py, tests/test_pregnancy_tools.py, tests/test_pregnancy_user_model.py, tests/test_write_tools_solo_bot_guard.py"
  ],
  "files_in_diff": [
    "app/bots/base.py",
    "app/bots/coach.py",
    "app/bots/ids.py",
    "app/bots/prompts/partner_sharing.py",
    "app/bots/prompts/tante_rosi.py",
    "app/bots/registry.py",
    "app/bots/tante_rosi.py",
    "app/models/user.py",
    "app/services/agentic.py",
    "app/services/cross_thread_privacy.py",
    "app/services/hot_context.py",
    "app/services/hot_context_solo.py",
    "app/services/partner_sharing.py",
    "app/services/prompts.py",
    "app/services/prompts_solo.py",
    "app/services/tools/common.py",
    "app/services/tools/read_tools.py",
    "app/services/tools/registry.py",
    "app/services/tools/scope_guard.py",
    "app/services/tools/write_tools.py",
    "app/services/turn_context.py",
    "app/staging.py",
    "megaplans/",
    "migrations/0035_per_bot_partner_sharing.sql",
    "scripts/import_chatgpt.py",
    "supabase/",
    "tests/conftest.py",
    "tests/test_agentic.py",
    "tests/test_coach_e2e.py",
    "tests/test_cross_topic_peek_wired.py",
    "tests/test_cross_topic_status_injection.py",
    "tests/test_eval_execution.py",
    "tests/test_hot_context.py",
    "tests/test_hot_context_cross_topic.py",
    "tests/test_hot_context_join_cutover.py",
    "tests/test_messaging_non_agentic_bot_id.py",
    "tests/test_multi_topic_writes.py",
    "tests/test_partner_sharing.py",
    "tests/test_partner_sharing_migration.py",
    "tests/test_partner_sharing_prompt.py",
    "tests/test_per_bot_telemetry.py",
    "tests/test_pregnancy_hot_context.py",
    "tests/test_pregnancy_tools.py",
    "tests/test_pregnancy_user_model.py",
    "tests/test_tool_schemas_importable.py",
    "tests/test_tools.py",
    "tests/test_write_tools_solo_bot_guard.py",
    "tool_schemas.py"
  ],
  "files_claimed": [
    "app/bots/base.py",
    "app/bots/coach.py",
    "app/bots/ids.py",
    "app/bots/prompts/partner_sharing.py",
    "app/bots/prompts/tante_rosi.py",
    "app/bots/registry.py",
    "app/bots/tante_rosi.py",
    "app/models/user.py",
    "app/services/agentic.py",
    "app/services/cross_thread_privacy.py",
    "app/services/hot_context.py",
    "app/services/hot_context_solo.py",
    "app/services/partner_sharing.py",
    "app/services/prompts.py",
    "app/services/prompts_solo.py",
    "app/services/tools/common.py",
    "app/services/tools/read_tools.py",
    "app/services/tools/registry.py",
    "app/services/tools/scope_guard.py",
    "app/services/tools/write_tools.py",
    "app/services/turn_context.py",
    "app/staging.py",
    "migrations/0035_per_bot_partner_sharing.sql",
    "tests/conftest.py",
    "tests/test_agentic.py",
    "tests/test_eval_execution.py",
    "tests/test_hot_context.py",
    "tests/test_hot_context_join_cutover.py",
    "tests/test_partner_sharing.py",
    "tests/test_partner_sharing_prompt.py",
    "tests/test_pregnancy_hot_context.py",
    "tests/test_tool_schemas_importable.py",
    "tests/test_tools.py",
    "tool_schemas.py"
  ],
  "skipped": false,
  "reason": ""
}

        Git diff summary:
        M app/bots/base.py
 M app/bots/coach.py
 M app/bots/ids.py
 M app/bots/prompts/tante_rosi.py
 M app/bots/registry.py
 M app/bots/tante_rosi.py
 M app/models/user.py
 M app/services/agentic.py
 M app/services/cross_thread_privacy.py
 M app/services/hot_context.py
 M app/services/hot_context_solo.py
 M app/services/prompts.py
 M app/services/prompts_solo.py
 M app/services/tools/common.py
 M app/services/tools/read_tools.py
 M app/services/tools/registry.py
 M app/services/tools/scope_guard.py
 M app/services/tools/write_tools.py
 M app/services/turn_context.py
 M app/staging.py
 M tests/conftest.py
 M tests/test_agentic.py
 M tests/test_coach_e2e.py
 M tests/test_cross_topic_peek_wired.py
 M tests/test_cross_topic_status_injection.py
 M tests/test_eval_execution.py
 M tests/test_hot_context.py
 M tests/test_hot_context_cross_topic.py
 M tests/test_hot_context_join_cutover.py
 M tests/test_messaging_non_agentic_bot_id.py
 M tests/test_multi_topic_writes.py
 M tests/test_per_bot_telemetry.py
 M tests/test_pregnancy_hot_context.py
 M tests/test_pregnancy_tools.py
 M tests/test_pregnancy_user_model.py
 M tests/test_tool_schemas_importable.py
 M tests/test_tools.py
 M tests/test_write_tools_solo_bot_guard.py
 M tool_schemas.py
?? app/bots/prompts/partner_sharing.py
?? app/services/partner_sharing.py
?? megaplans/
?? migrations/0035_per_bot_partner_sharing.sql
?? scripts/import_chatgpt.py
?? supabase/
?? tests/test_partner_sharing.py
?? tests/test_partner_sharing_migration.py
?? tests/test_partner_sharing_prompt.py

        Requirements:
        - Verify each success criterion explicitly.
        - Trust executor evidence by default. Dig deeper only where the git diff, `execution_audit.json`, or vague notes make the claim ambiguous.
        - Each criterion has a `priority` (`must`, `should`, or `info`). Apply these rules:
          - `must` criteria are hard gates. A `must` criterion that fails means `needs_rework`.
          - `should` criteria are quality targets. If the spirit is met but the letter is not, mark `pass` with evidence explaining the gap. Only mark `fail` if the intent was clearly missed. A `should` failure alone does NOT require `needs_rework`.
          - `info` criteria are for human reference. Mark them `waived` with a note — do not evaluate them.
          - If a criterion has `requires` capabilities that are not satisfiable by container workers (e.g., `drive_browser`, `subjective_judgment`), mark it `deferred_human` — NOT `fail` or `waived`. Deferred-human criteria do NOT count toward `needs_rework`.
          - If a criterion (any priority) cannot be verified in this context (e.g., requires manual testing or runtime observation), mark it `waived` with an explanation.
        - Set `review_verdict` to `needs_rework` only when at least one `must` criterion fails or actual implementation work is incomplete. Use `approved` when all `must` criteria pass, even if some `should` criteria are flagged.
        - The decisions listed above were settled at the gate stage. Verify that the executor implemented each settled decision correctly. Flag deviations from these decisions, but do not question the decisions themselves.
        - baseline_test_failures in finalize.json lists tests that were already failing before execution. Do not flag these as rework items unless the executor introduced new failures in those same tests.
        - Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.
        - Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.
        - Follow this JSON shape exactly:
        ```json
        {
          "review_verdict": "approved",
          "criteria": [
            {
              "name": "All existing tests pass",
              "priority": "must",
              "pass": "pass",
              "evidence": "Test suite ran green — 42 passed, 0 failed."
            },
            {
              "name": "File under ~300 lines",
              "priority": "should",
              "pass": "pass",
              "evidence": "File is 375 lines — above the target but reasonable given the component's responsibilities. Spirit met."
            },
            {
              "name": "Manual smoke tests pass",
              "priority": "info",
              "pass": "waived",
              "evidence": "Cannot be verified in automated review. Noted for manual QA."
            }
          ],
          "issues": [],
          "rework_items": [],
          "summary": "Approved. All must criteria pass. The should criterion on line count is close enough given the component scope.",
          "task_verdicts": [
            {
              "task_id": "T6",
              "reviewer_verdict": "Pass. Claimed handler changes and command evidence match the repo state.",
              "evidence_files": ["megaplan/handlers.py", "megaplan/evaluation.py"]
            }
          ],
          "sense_check_verdicts": [
            {
              "sense_check_id": "SC6",
              "verdict": "Confirmed. The execute blocker only fires when both evidence arrays are empty."
            }
          ]
        }
        ```
        - `rework_items` must be an array of structured rework directives. When `review_verdict` is `needs_rework`, populate one entry per issue with:
          - `task_id`: which finalize task this issue relates to
          - `issue`: what is wrong
          - `expected`: what correct behavior looks like
          - `actual`: what was observed
          - `evidence_file` (optional): file path supporting the finding
          - `flag_id`: critique/review flag ID when applicable, otherwise `null`
          - `source`: short machine-readable source tag when applicable, otherwise `null`
        - `issues` must still be populated as a flat one-line-per-item summary derived from `rework_items` (for backward compatibility). When approved, both `issues` and `rework_items` should be empty arrays.
        - When the work needs another execute pass, keep the same shape and change only `review_verdict` to `needs_rework`; make `issues`, `rework_items`, `summary`, and task verdicts specific enough for the executor to act on directly.

> AGENT

{"review_verdict":"needs_rework","criteria":[],"issues":["Review in progress; checking the targeted rework in hot_context.py and the new starvation regression."],"rework_items":[],"summary":"I am verifying the cross-bot query now applies opt-in before ordering/limit, then rerunning the focused tests relevant to the rework.","task_verdicts":[],"sense_check_verdicts":[],"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9143, expected≈10, ratio=914.30, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":[],"disputed_flag_ids":[]}

> AGENT

{"review_verdict":"approved","checks":null,"pre_check_flags":[{"id":"PRECHECK-DIFF_SIZE_SANITY","check":"diff_size_sanity","detail":"Diff size looks larger than expected: changed_lines=9143, expected≈10, ratio=914.30, files=55, hunks=690.","severity":"significant","evidence_file":"app/bots/base.py"}],"verified_flag_ids":["FLAG-001","FLAG-002","FLAG-003","FLAG-004","FLAG-005"],"disputed_flag_ids":["verifiability-0","verifiability-1"],"criteria":[{"name":"Migration seeds Tante Rosi bot row before Rosi partner-share writes","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql seeds bots(id='tante_rosi') before user_bot_state partner_share work."},{"name":"Migration adds partner_share and backfills mediator non-NULL legacy values before dropping old column","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql adds constrained user_bot_state.partner_share and backfills non-NULL users.cross_thread_sharing_default into mediator rows before the final drop block."},{"name":"Migration adds memory visibility/shareable-summary fields and CHECK","priority":"must","pass":"pass","evidence":"migrations/0035_per_bot_partner_sharing.sql adds memories.visibility, shareable_summary, shareable_summary_encrypted, and a non-empty summary CHECK for dyad_shareable memories."},{"name":"Migration drops users.cross_thread_sharing_default only after read path update","priority":"must","pass":"pass","evidence":"The migration drops the column at the end of the transaction, and `rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py` returned no production matches."},{"name":"Production code reads user_bot_state.partner_share, not users.cross_thread_sharing_default","priority":"must","pass":"pass","evidence":"app/services/partner_sharing.py provides per-bot reads/upserts; app/services/hot_context.py, hot_context_solo.py, read_tools.py, agentic.py, and staging.py consume per-bot partner_share."},{"name":"Hot context cross-bot pull includes opted-in shareable summaries with provenance","priority":"must","pass":"pass","evidence":"app/services/hot_context.py:248-287 now joins user_bot_state with partner_share='opt_in' before recency ordering and LIMIT. The prior starvation issue is fixed, and tests/test_hot_context.py adds a 60 opt-out row regression."},{"name":"Hot context emits pending partner-sharing state only when current user has partner and current bot state is NULL/missing","priority":"must","pass":"pass","evidence":"Dyadic and solo hot-context paths compute partner_sharing_state from current-bot partner_share and suppress unavailable/no-partner states; focused hot-context suites passed."},{"name":"set_partner_sharing exists, is wired for bots, and updates only calling user/bot","priority":"must","pass":"pass","evidence":"tool_schemas.py forbids user_id/bot_id inputs; app/services/tools/write_tools.py writes ctx.user.id and ctx.bot_id; registry/scope guard include set_partner_sharing; tests cover scoped Rosi write."},{"name":"add_memory accepts visibility/shareable_summary and rejects dyad_shareable without summary","priority":"must","pass":"pass","evidence":"tool_schemas.py validates AddMemoryInput; app/services/tools/write_tools.py persists visibility, shareable_summary, encrypted summary, and recorded_by_bot_id. Schema/tool tests passed."},{"name":"Rosi prompt writes dyad_shareable safe facts when opted in","priority":"must","pass":"pass","evidence":"app/bots/prompts/tante_rosi.py renders the canonical pending slot and includes Rosi-specific opt-in guidance for non-sensitive dyad_shareable memories/distillations with shareable_summary."},{"name":"Mediator onboarding language collapsed into canonical slot and remains observationally equivalent","priority":"must","pass":"pass","evidence":"app/services/prompts.py uses PENDING_PARTNER_SHARING_PROMPT_SLOT for pending state and set_partner_sharing terminology; migration backfills mediator opt_in/opt_out values from the legacy column."},{"name":"Tests cover privacy matrix, cross-bot independence, raw isolation, no-partner suppression, and Rosi FK success","priority":"must","pass":"pass","evidence":"Focused suites passed in review: 23 hot-context/join/partner tests, 92 schema/tool tests, 54 hot-context/pregnancy/migration tests, and 92 prompt/allowlist/adjacent tests."},{"name":"Raw message reads are same-bot/topic scoped before partner visibility","priority":"must","pass":"pass","evidence":"app/services/hot_context.py filters messages by bot_id and topic_id; read_tools search/recent paths do the same; FLAG-001 regression coverage passed."},{"name":"raw_message_visibility and callers use owner partner_share for relevant bot","priority":"must","pass":"pass","evidence":"app/services/cross_thread_privacy.py uses thread_owner_partner_share and blocks unset/opt_out; callers load state by source row bot_id or current bot as appropriate."},{"name":"TANTE_ROSI_BOT_ID exists and code avoids new hard-coded ids where constants are available","priority":"must","pass":"pass","evidence":"app/bots/ids.py defines TANTE_ROSI_BOT_ID; app/bots/tante_rosi.py and app/bots/registry.py import it. Remaining literals are test data/SQL seed context."},{"name":"Cross-bot partner content ordering and global cap are explicit","priority":"should","pass":"deferred_human","evidence":"Criterion includes subjective_judgment. Mechanically, app/services/hot_context.py documents opt-in gating before recency ordering and the fixed CROSS_BOT_SHAREABLE_SUMMARY_CAP=12."},{"name":"Prompt/hot-context labels consistently use partner_share terminology","priority":"should","pass":"deferred_human","evidence":"Criterion includes subjective_judgment. Literal stale-reference sweep over app and tool_schemas.py is clean."},{"name":"Future work for re-asking/per-topic granularity remains out of scope","priority":"info","pass":"waived","evidence":"Info criterion only. No opportunistic re-ask/per-topic implementation was evident."}],"issues":[],"rework_items":[],"summary":"Approved. The prior cap-before-opt-in bug is fixed: cross-bot summary rows now join user_bot_state with partner_share='opt_in' before ordering and limiting, and the starvation regression is covered. All must criteria pass. Focused suites and lint passed; full pytest still reports the previously documented unrelated tests/test_decay.py fake-pool failures, not a new blocker for this review.","task_verdicts":[{"task_id":"T1","reviewer_verdict":"Pass. Migration and bot id constant are present; Tante Rosi is seeded before partner-share backfill/use.","evidence_files":["migrations/0035_per_bot_partner_sharing.sql","app/bots/ids.py"]},{"task_id":"T2","reviewer_verdict":"Pass. Shared helper module covers normalization, per-bot fetch/upsert, dyad partner resolution, and provenance fallback.","evidence_files":["app/services/partner_sharing.py"]},{"task_id":"T3","reviewer_verdict":"Pass. Production stale-reference sweep no longer finds the dropped users column or old tool names.","evidence_files":["app/models/user.py","app/services/turn_context.py","app/staging.py"]},{"task_id":"T4","reviewer_verdict":"Pass. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id and wired through schema/registry/scope guard.","evidence_files":["tool_schemas.py","app/services/tools/write_tools.py","app/services/tools/registry.py","app/services/tools/scope_guard.py"]},{"task_id":"T5","reviewer_verdict":"Pass. Final literal stale-reference sweep across app and tool_schemas.py is clean.","evidence_files":["app/services/prompts.py","app/services/tools/read_tools.py"]},{"task_id":"T6","reviewer_verdict":"Pass. Raw privacy helper uses partner_share terminology and blocks unset/opt_out partner raw reads.","evidence_files":["app/services/cross_thread_privacy.py"]},{"task_id":"T7","reviewer_verdict":"Pass. Raw message queries are scoped by bot/topic in hot context and read tools.","evidence_files":["app/services/hot_context.py","app/services/tools/read_tools.py"]},{"task_id":"T8","reviewer_verdict":"Pass. Cross-bot shareable summaries are now opt-in gated in SQL before recency ordering and LIMIT.","evidence_files":["app/services/hot_context.py"]},{"task_id":"T9","reviewer_verdict":"Pass. Solo hot context has partner_share/pending state and tests cover no partner-content exposure.","evidence_files":["app/services/hot_context_solo.py","tests/test_pregnancy_hot_context.py"]},{"task_id":"T10","reviewer_verdict":"Pass. Canonical pending prompt slot is defined once and is domain-neutral.","evidence_files":["app/bots/prompts/partner_sharing.py"]},{"task_id":"T11","reviewer_verdict":"Pass. Mediator, Rosi, coach, and generic solo prompt paths render the canonical slot from partner_sharing_state.","evidence_files":["app/services/prompts.py","app/services/prompts_solo.py","app/bots/tante_rosi.py","app/bots/coach.py"]},{"task_id":"T12","reviewer_verdict":"Pass. Memory schema/write path accepts and persists dyad_shareable summaries and validates missing summaries.","evidence_files":["tool_schemas.py","app/services/tools/write_tools.py"]},{"task_id":"T13","reviewer_verdict":"Pass. Regression coverage now includes the opt-out row starvation edge case plus the existing privacy matrix coverage.","evidence_files":["tests/test_hot_context.py","tests/conftest.py"]},{"task_id":"T14","reviewer_verdict":"Pass. Stale-reference sweeps and focused suites passed after the rework; the temporary starvation reproduction was reported as passed and deleted.","evidence_files":["app/services/hot_context.py","tests/test_hot_context.py"]}],"sense_check_verdicts":[{"sense_check_id":"SC1","verdict":"Confirmed. Migration is transactional, seeds Tante Rosi, adds partner_share, backfills mediator, adds memory fields/checks, and drops the legacy column last."},{"sense_check_id":"SC2","verdict":"Confirmed. partner_sharing.py uses explicit (user_id, bot_id), dyad_members/dyads, and registry/DB/id provenance fallback."},{"sense_check_id":"SC3","verdict":"Confirmed. User, partner_of, and staging paths are free of production cross_thread_sharing_default dependency."},{"sense_check_id":"SC4","verdict":"Confirmed. set_partner_sharing is scoped to ctx.user.id and ctx.bot_id."},{"sense_check_id":"SC5","verdict":"Confirmed. Final literal stale-reference sweep is clean."},{"sense_check_id":"SC6","verdict":"Confirmed. raw_message_visibility preserves owner reads and blocks unset/opt_out partner reads."},{"sense_check_id":"SC7","verdict":"Confirmed. Hot-context/read-tool raw message paths add bot/topic scope."},{"sense_check_id":"SC8","verdict":"Confirmed after rework. Cross-bot memory/distillation summaries now join user_bot_state with partner_share='opt_in' before recency ordering and the 12-row cap."},{"sense_check_id":"SC9","verdict":"Confirmed. Solo hot-context pending/no-partner behavior is implemented and covered."},{"sense_check_id":"SC10","verdict":"Confirmed. Canonical slot is defined once and references set_partner_sharing after explicit choice."},{"sense_check_id":"SC11","verdict":"Confirmed. Prompt paths render the canonical slot via partner_sharing_state."},{"sense_check_id":"SC12","verdict":"Confirmed. add_memory validates and persists shareable summaries, including encrypted summary storage."},{"sense_check_id":"SC13","verdict":"Confirmed. Tests now cover the previously missing starvation edge case in addition to the named privacy matrix."},{"sense_check_id":"SC14","verdict":"Confirmed. Stale-reference sweeps and focused pytest commands passed; full pytest has only the documented unrelated decay failures."}]}

> TOOL

tool_use exec_command
```json
{
  "cmd": "nl -ba app/services/hot_context.py | sed -n '231,325p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"starv|opt-out|opt_out|newer|60|partner_shareable|CROSS_BOT_SHAREABLE|partner_share = 'opt_in'|WITH partner_rows\" tests/test_hot_context.py tests/conftest.py app/services/hot_context.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "rg -n \"cross_thread_sharing_default|update_cross_thread_sharing_default|current_user_sharing_default|partner_sharing_default|sharing_default\" app tool_schemas.py || true",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_partner_sharing.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_tool_schemas_importable.py tests/test_tools.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_hot_context.py tests/test_hot_context_join_cutover.py tests/test_pregnancy_hot_context.py tests/test_partner_sharing.py tests/test_partner_sharing_migration.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "pytest tests/test_partner_sharing_prompt.py tests/test_eval_execution.py tests/test_pregnancy_persona.py tests/test_coach_e2e.py tests/test_write_tools_solo_bot_guard.py tests/test_cross_topic_peek_wired.py tests/test_cross_topic_status_injection.py tests/test_hot_context_cross_topic.py tests/test_multi_topic_writes.py tests/test_per_bot_telemetry.py tests/test_pregnancy_user_model.py tests/test_messaging_non_agentic_bot_id.py -q",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 50000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "sed -n '680,750p' tests/test_hot_context.py && sed -n '2320,2365p' tests/conftest.py",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "python scripts/lint_artifact_reads.py --dir app",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 30000,
  "max_output_tokens": 30000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "git diff -- app/services/hot_context.py tests/test_hot_context.py tests/conftest.py | sed -n '1,260p'",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 40000
}
```

> TOOL

tool_result exec_command
```
null
```

> TOOL

tool_use exec_command
```json
{
  "cmd": "git status --short",
  "workdir": "/Users/user_c042661f/Documents/Veas",
  "yield_time_ms": 1000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_result exec_command
```
null
```
