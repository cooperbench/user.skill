> DEVELOPER

In each order store the platform fee that is collected and show it in the order. . first explain what you undertand

> AGENT

Let me look at how the platform fee currently works before explaining my understanding.

> AGENT

Here's what I found and what I understand from your request. ## Current state of the platform fee **Storage — already done.** Since the platform-fee feature shipped (commit 147649a), every order row already stores the collected fee: - `orders.platform_fee` column exists (from `platform-fee-migration.sql`, applied in Supabase). - At order placement (`src/app/api/orders/place/route.ts:302-310`), the moderator's current fee % is read from `platform_settings`, converted to rupees per item, and **stamped on each order row**. So even if the moderator later changes the %, each order permanently records the exact rupee amount that was charged. - Cancel/decline refund logic already uses this stored value (withhold vs. full refund). **Display — only partially done.** This is the actual gap: | Place | Shows platform fee today? | |---|---| | Consumer order **detail** page (`/consumer/orders/[id]`) | ✅ Yes — in the "Total paid" breakdown and in cancelled/withheld notices | | Consumer order **card** (orders list) | ❌ No — the field is fetched but never rendered | | Farmer order card (`/farmer/dashboard/orders`) | ❌ No — `platform_fee` is in the query and the type, but not rendered | | Moderator module | ❌ No order view references `platform_fee` at all | ## What I understand you […]