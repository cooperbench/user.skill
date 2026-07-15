> DEVELOPER

[Image #1] need small add to cart symbol in right side of the product

> AGENT

I'll find the harvest table component that renders these "Fresh Harvests" and "Upcoming Harvests" cards.

> AGENT

Let me understand how the cart / add-to-cart works elsewhere in the app so I mirror the existing pattern.

> AGENT

Let me see how add-to-cart is wired on the consumer browse list, so the harvest table can mirror it.

> AGENT

A click-time fetch is cleaner than guessing a nested embed name. Let me check `requireAuth`.

> AGENT

Now I have everything. Let me implement the add-to-cart icon in the harvest tables.

> AGENT

Now add the add-to-cart handler after `listingOf`:

> AGENT

Now replace the chevron cell with a small add-to-cart button:

> AGENT

Now let me verify it compiles/typechecks:

> AGENT

Let me mirror the established pattern of gating on auth *before* fetching, so logged-out users get the login prompt immediately without two wasted queries:

> AGENT

Now fix the closing braces (removed the outer `requireAuth(() => {` wrapper around addItem):

> AGENT

Clean. Let me run lint on the file to catch anything:

> AGENT

Done. I added a small add-to-cart button on the right of each row in both the **Fresh Harvests** and **Upcoming Harvests** tables (they share the `HarvestTable` component). What it does: - Replaced the decorative `›` chevron with a compact cart icon button (32px, green pill). - Tapping it adds that harvest's listing straight to the cart without leaving the page. Since the table only holds the listing id/name, the handler fetches the full listing + its farmer on tap and builds the same cart-item shape the browse cards use (`Cart.tsx` `addItem`), including price tiers, stock cap, and farmer pickup info. - It's gated behind consumer login via `requireAuth` (matches the existing browse-card flow), and `stopPropagation` keeps the row's tap-to-open-details behavior intact. - Visual states: cart icon → `…` while fetching → green ✓ once the item is in the cart. The existing `CartFab` picks up the count automatically. Notes: - This is a consumer-facing feature, so the farmer↔moderator parity rule doesn't apply here. - I left the `TodaysHarvest.tsx` feed untouched since your screenshot is the two side-by-side tables. Let me know if you want the same cart icon on that feed too. I haven't committed — want me to commit […]