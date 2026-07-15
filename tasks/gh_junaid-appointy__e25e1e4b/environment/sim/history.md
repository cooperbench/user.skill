> DEVELOPER

in the auxilio-extension lets give people ability to edit the details of guests like their name and phone when invites are already sent and the event is opened second time for updates , corrections and all, also, can we keep it clean looking, like do not show the details of the user until its needed to edit, like the input boxes being open by default makes each card take a lot of space.

> AGENT

I'll start by exploring the auxilio-extension folder to understand the current structure and how guest cards are rendered.

> AGENT

The patch already flows to the engine via `DRAFT_PATCH`. Let me check the types and engine client, and whether the engine accepts edits to already-sent guests.

> AGENT

The patch flows to the engine's `PATCH /draft`. Let me verify the engine accepts name/phone edits for already-sent guests, since that's the behavioral assumption.

> AGENT

The engine's `patchDraft` applies name/phone to any guest regardless of status — no `sent` gating. So editing sent guests already works server-side; this is purely a frontend change in `RosterRow.tsx`. Let me check the CSS and available design components.

> AGENT

Let me check the Button and TextField components for available variants/sizes.

> AGENT

Now I have everything I need. Let me rewrite `RosterRow.tsx` to collapse the edit form behind an affordance and allow editing already-sent guests.

> AGENT

Now the body — replace the always-open form with a collapsed summary + expand-on-demand form:

> AGENT

Now add the CSS for the collapsed summary, edit affordance, and Done button. Let me add it right after the existing `.guest__hint` / keyframes block:

> AGENT

Now bump the extension version (CLAUDE.md requires it on every shipped change) and type-check.

> AGENT

Type-check passes. Let me verify the final RosterRow reads cleanly:

> AGENT

Done. Here's what changed and why. ## What I changed **`features/visit/RosterRow.tsx`** — the per-guest card: - **Sent guests are now editable.** The gate went from `editable = guest.include && !sent` to `editable = guest.include && !cancelled`. When a host reopens an event for corrections, they can fix a name or phone on a guest whose pass already went out. - **Details are collapsed by default.** Instead of always-open input boxes, each editable card shows a compact one-line summary: the phone (if set) plus a small inline **"Edit details"** / **"Add phone"** affordance (Lucide `Pencil`). The name/email already live in the head, so a card is now ~one line tall until you choose to open it. - **Expand on demand.** Clicking the affordance reveals the same name + phone fields, with a **"Done"** button (Lucide `Check`) to collapse again. Edits still persist on blur exactly as before — Done just folds the card back up. - **Honest feedback for sent guests:** when editing an already-sent guest, a muted line reads *"Re-send to update the pass that's already been issued."* — because corrections only reach the issued pass via the existing **"Review & update passes"** flow. **`design/global.css`** — added `.guest__summary`, `.guest__phone`, `.guest__edit`, […]