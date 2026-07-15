> DEVELOPER

[Image #1]

> AGENT

I'll investigate how the consumer browse-harvests page renders harvests, since the card says 3 harvests for Banana show as only one card.

> AGENT

These two components already render one card per harvest. The complaint is about the main "browse" grid. Let me find where consumers browse the full produce/harvest list.

> AGENT

The main grid (`ConsumerPage`) renders one `ProduceCard` per **produce listing**, not per harvest — that's the Phase 2 gap. Let me examine the API and data model before deciding the approach.

> AGENT

Now let me look at the harvest detail page and the harvests schema to understand per-harvest fields.

> AGENT

I now fully understand the architecture. The main grid renders **one card per produce listing**; harvest-as-product (Phase 1) already exists for detail pages, cart, and the Fresh/Upcoming tables — but the main browse grid was the deferred Phase 2. This Trello card asks to expand the main grid so each harvest is its own card. Let me implement it. First the type and state:

> AGENT

Now the `displayItems` rework to expand each listing into per-harvest cards:

> AGENT

Now I need to declare the `WithDist` and `DisplayCard` types at module scope (I removed the inline `WithDist`):

> AGENT

Now update the render loop to pass `harvest` and use the card structure:

> AGENT

Now the `ProduceCard` component itself — make it harvest-aware. First the signature and derived values:

> AGENT

Now the `addItem` call and `handleInc`:

> AGENT

Now the clock display block and the decrement button (both still reference `item.latest_harvested_at` / `item.id`):

> AGENT

Let me verify no stale references remain and typecheck:

> AGENT

Typecheck is clean. Let me run a production build to be sure it compiles:

> AGENT

Build succeeds. Let me quickly verify the region discovery page doesn't share the same one-card-per-produce grid that would need the same treatment:

> AGENT

The region page is the P2 discovery page (produce counts, not the buyable card grid) — out of scope for this card, which targets the main `/consumer` browse grid. The fix is complete and builds clean. Let me update the memory to record Phase 2 shipped:

> AGENT

Done. Here's what I found and changed. ## The problem The Trello card (in **Testing Failed**) reported: *"I added 3 Harvests for Banana but I can see only one card in the consumer browse harvests place."* Root cause: the harvest-as-product model shipped in Phase 1 (detail pages, cart lines, the Fresh/Upcoming tables) — but the **main `/consumer` browse grid** was the explicitly deferred Phase 2. It still rendered **one `ProduceCard` per produce listing**, keeping only the *latest* harvest per produce for the clock. So 3 Banana harvests collapsed into 1 card. ## The fix — `src/app/consumer/page.tsx` 1. **Fetch all harvests, not just latest** — `fetchData` now builds `harvestsByListing: Record<listingId, GridHarvest[]>` (id, date, shelf life, stock, unit) over a 14-day window that also includes future pre-books. 2. **Expand into per-harvest cards** — `displayItems` now returns `DisplayCard[]`: a produce with logged harvests becomes **one card per harvest**; a produce with none falls back to a single template card. Farmer/distance filters and the fresh/rating/purchases sorts all still apply (each card sorts by its own harvest date). 3. **Made `ProduceCard` harvest-aware** — an optional `harvest` prop makes the card link to `/consumer/harvest/[id]`, key the cart on the harvest id, show that harvest's own stock/clock/freshness, […]