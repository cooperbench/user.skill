> DEVELOPER

[Image #1]Change "Harvested On" to "Harvest Date Time" in the Harvest Detail screen for Consumer.

> AGENT

Both consumer pages use the same label. Let me update them.

> AGENT

Done. Changed the label from **"Harvested on"** to **"Harvest Date Time"** in both consumer detail screens: - `src/app/consumer/harvest/[harvestId]/page.tsx:382` - `src/app/consumer/produce/[id]/page.tsx:407` (this is the one in your screenshot — the produce detail page with the bulk pricing and Add to cart) I updated both since they share the exact same label. The Telugu translation was also updated to `కోత తేదీ సమయం`. The value formatting (e.g. "5 Jul 2026, 04:05 pm") is unchanged.