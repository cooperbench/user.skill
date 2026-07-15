> DEVELOPER

[Image #1] have we done all these perfectly if perfect deploy to main

> AGENT

I'll investigate the current state of the code against each of these 5 Trello cards before claiming anything is done. Let me start by looking at what's changed and the relevant files.

> TOOL

tool_use Bash
id: toolu_01QAoBeg2jt8MaVo4AaHES3r
```json
{
  "command": "git status && echo \"---DIFF STAT---\" && git diff --stat",
  "description": "Show git status and diff stat"
}
```

> TOOL

tool_result
id: toolu_01QAoBeg2jt8MaVo4AaHES3r
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/app/consumer/page.tsx
	modified:   src/components/farmer/OrderCard.tsx

no changes added to commit (use "git add" and/or "git commit -a")
---DIFF STAT---
 src/app/consumer/page.tsx           | 169 +++++++++++++++++++++++++-----------
 src/components/farmer/OrderCard.tsx |  15 ++--
 2 files changed, 126 insertions(+), 58 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01ACg8xyA13ubNm5182rNssQ
```json
{
  "command": "ls src/app && echo \"---\" && ls src/components/farmer && echo \"---scripts---\" && ls scripts 2>/dev/null | head -50",
  "description": "List app structure"
}
```

> TOOL

tool_result
id: toolu_01ACg8xyA13ubNm5182rNssQ
```
admin
api
buyer-protection
consumer
error.tsx
farmer
favicon.ico
globals.css
layout.tsx
moderator
not-found.tsx
page.tsx
region
rider
---
DeclineSheets.tsx
FarmCover.tsx
OrderCard.tsx
OrderReportSheet.tsx
StickyBottomBar.tsx
TabSection.tsx
TopNav.tsx
TrustStrip.tsx
tabs
---scripts---
apply-pending-migrations.sql
audit-log-migration.sql
client-fixes-migration.sql
cod-toggle-migration.sql
complaints-self-service-migration.sql
consumer-auth-migration.sql
consumer-intents-migration.sql
consumer-suspend-migration.sql
decline-reason-migration.sql
delivery-feature-migration.sql
farm-address-migration.sql
farm-images-bucket.sql
farmer-buyer-count-function.sql
farmer-follows-migration.sql
farmer-soil-ph-migration.sql
farmers-moderator-registration.sql
feature-migration.sql
fulfillment-datetime-migration.sql
guest-checkout-migration.sql
harvest-as-product-migration.sql
harvests-migration.sql
idempotency-migration.sql
media-anon-write-policies.sql
moderator-agents-migration.sql
moderator-auth-migration.sql
moderator-features-migration.sql
moderator-prices-migration.sql
must-fix-migration.sql
order-acknowledge-migration.sql
order-audit-migration.sql
order-code-migration.sql
order-completion-migration.sql
orders-consumer-id-migration.sql
orders-delivery-city-migration.sql
otp-sessions-migration.sql
payment-proof-migration.sql
payment-qr-migration.sql
pickup-confirm-migration.sql
platform-fee-migration.sql
produce-availability-frequency-migration.sql
produce-category-photos-migration.sql
produce-harvest-shelf-migration.sql
produce-listings-delete-policy.sql
produce-listings-update-policy.sql
produce-period-refund-migration.sql
produce-quality-fields-migration.sql
produce-reviews-migration.sql
produce-status-farmer-takedown-migration.sql
razorpay-payment-migration.sql
refund-migration.sql
```

> AGENT

Let me look at the uncommitted diff and understand what's been changed so far.

> TOOL

tool_use Bash
id: toolu_013fsbMXX9a7XLKBLC8yKqD5
```json
{
  "command": "git diff src/app/consumer/page.tsx src/components/farmer/OrderCard.tsx",
  "description": "Show full uncommitted diff"
}
```

> TOOL

tool_result
id: toolu_013fsbMXX9a7XLKBLC8yKqD5
```
diff --git a/src/app/consumer/page.tsx b/src/app/consumer/page.tsx
index 38cabf9..48e70cb 100644
--- a/src/app/consumer/page.tsx
+++ b/src/app/consumer/page.tsx
@@ -68,6 +68,28 @@ type ProduceListing = {
   latest_shelf_life_days?: number | null
 }
 
+// One logged harvest of a produce (template). The main grid shows a separate
+// card per harvest — so 3 harvests of the same Banana are 3 cards, each with its
+// own pick date/time, shelf life and stock — while inheriting everything else
+// (photos, price, farmer, quality) from the produce_listing. Reads the
+// `harvests` table (scripts/harvests-migration.sql).
+type GridHarvest = {
+  id: string
+  harvested_at: string
+  shelf_life_days: number | null
+  stock_qty: number | null
+  unit: string | null
+}
+
+// A produce listing with its computed distance from the consumer.
+type WithDist = ProduceListing & { distKm: number | null; distApprox: boolean }
+
+// One grid tile. `harvest` present → a specific harvest of the produce (own
+// date/shelf/stock, links to the harvest page); absent → the produce template
+// (fallback when nothing has been logged). `sortAt` is the harvest date/time
+// used by the "Freshest first" sort; `key` is the React/cart key.
+type DisplayCard = { item: WithDist; harvest?: GridHarvest; key: string; sortAt: […]

> AGENT

The uncommitted diff implements Card #1 (separate card per harvest). Now let me verify each card carefully — starting with whether the supporting pieces for Card #1 actually exist (harvest page route, cart supporting `harvestId`).

> TOOL

tool_use Bash
id: toolu_01Vuibm8sivU3KchoVypC3Lb
```json
{
  "command": "echo \"=== harvest consumer route ===\" && ls -la src/app/consumer/harvest 2>/dev/null && ls -la src/app/consumer/harvest/*/ 2>/dev/null\necho \"=== cart context: harvestId support ===\" && grep -rn \"harvestId\\|harvestedAt\\|shelfLifeDays\" src/ --include=*.tsx --include=*.ts | grep -i cart\necho \"=== CartItem type def ===\"\ngrep -rln \"type CartItem\\|interface CartItem\\|listingId\" src/ --include=*.tsx --include=*.ts",
  "description": "Check harvest route and cart harvestId support"
}
```

> TOOL

tool_result
id: toolu_01Vuibm8sivU3KchoVypC3Lb
```
=== harvest consumer route ===
total 12
drwxr-xr-x 3 veerendra veerendra 4096 Jul  3 11:11 .
drwxr-xr-x 8 veerendra veerendra 4096 Jul  4 11:03 ..
drwxr-xr-x 2 veerendra veerendra 4096 Jul  3 11:11 [harvestId]
total 32
drwxr-xr-x 2 veerendra veerendra  4096 Jul  3 11:11 .
drwxr-xr-x 3 veerendra veerendra  4096 Jul  3 11:11 ..
-rw-r--r-- 1 veerendra veerendra 20532 Jul  3 11:11 page.tsx
=== cart context: harvestId support ===
src/components/consumer/Cart.tsx:64:  // stock — so the cart is keyed by harvestId, and two harvests of the same
src/components/consumer/Cart.tsx:67:  harvestId?: string
src/components/consumer/Cart.tsx:70:  harvestedAt?: string
src/components/consumer/Cart.tsx:71:  shelfLifeDays?: number
src/components/consumer/Cart.tsx:98:// separate lines. Legacy produce-card items (no harvestId) key by listingId.
src/components/consumer/Cart.tsx:99:export const cartKeyOf = (item: { listingId: string; harvestId?: string }): string =>
src/components/consumer/Cart.tsx:100:  item.harvestId ?? item.listingId
src/components/consumer/Cart.tsx:509:        items: group.map((it) => ({ listingId: it.listingId, harvestId: it.harvestId, qty: it.qty })),
=== CartItem type def ===
src/app/moderator/listings/[id]/edit/page.tsx
src/app/farmer/[slug]/page.tsx
src/lib/purchaseCounts.ts
src/app/consumer/page.tsx
src/app/consumer/produce/[id]/page.tsx
src/app/consumer/harvest/[harvestId]/page.tsx
src/app/moderator/listings/ListingForm.tsx
src/app/api/farmer/update-listing/route.ts
src/components/region/tabs/BrowseProduceTab.tsx
src/app/farmer/dashboard/page.tsx
src/app/api/produce-reviews/route.ts
src/components/consumer/ProduceReviewsModal.tsx
src/components/consumer/Cart.tsx
src/components/consumer/FreshHarvestsTable.tsx
src/app/api/orders/place/route.ts
src/components/farmer/tabs/ProduceTab.tsx
src/components/consumer/TodaysHarvest.tsx
```

> AGENT

Cart supports `harvestId` and there's a `/consumer/harvest/[harvestId]` route. Let me verify the cart keying is consistent with how `page.tsx` calls it, and check the harvest page.

> TOOL

tool_use Read
id: toolu_01EfELTms4sToUGot4v38TT8
```json
{
  "file_path": "/home/veerendra/farmer/yourfamilyfarmer/src/components/consumer/Cart.tsx",
  "offset": 55,
  "limit": 180
}
```

> TOOL

tool_result
id: toolu_01EfELTms4sToUGot4v38TT8
```
55	    script.onerror = () => resolve(false)
56	    document.body.appendChild(script)
57	  })
58	}
59	
60	export type CartItem = {
61	  listingId: string
62	  // The specific harvest this line is for. A produce (template) can have many
63	  // harvests (fresh vs pre-book), each its own sellable product with its own
64	  // stock — so the cart is keyed by harvestId, and two harvests of the same
65	  // listing are two separate lines. Legacy produce-card adds leave it unset and
66	  // fall back to keying by listingId.
67	  harvestId?: string
68	  // Harvest-specific display info, carried so the cart/checkout can show which
69	  // pick this is (e.g. "harvested 2 hours ago").
70	  harvestedAt?: string
71	  shelfLifeDays?: number
72	  qty: number
73	  name: string
74	  variety?: string
75	  emoji?: string
76	  pricePerKg?: number
77	  priceTier1Qty?: number
78	  priceTier1Price?: number
79	  priceTier2Qty?: number
80	  priceTier2Price?: number
81	  priceTier3Price?: number
82	  unit?: string
83	  stockQty?: number
84	  farmerId: string
85	  farmerName: string
86	  farmerPhone: string
87	  farmerVillage: string
88	  farmerSlug: string
89	  farmerPickupLocations?: string[]
90	  farmerPickupSlots?: PickupSchedule
91	  farmerUpiId?: string
92	  farmerQrCodeUrl?: string
93	}
94	
95	export type CartState = Record<string, CartItem>
96	
97 […]

> AGENT

Card #1's cart/order plumbing already shipped in Phase 1. Now let me check the other cards. Let me find the "Fresh From Your Local Farmer" header (Card #2), the Log Harvest shelf life field (Card #3), and Harvest Date Time in Produce (Card #4).

> TOOL

tool_use Bash
id: toolu_019kViVCC4RUdEfUS4aGjeJD
```json
{
  "command": "echo \"=== Card 2: Fresh From Your Local Farmer ===\" && grep -rn \"Fresh From Your Local Farmer\\|Fresh from your\\|Local Farmer\" src/ --include=*.tsx -i\necho \"=== Card 3: Log Harvest form ===\" && grep -rln \"Log Harvest\\|logHarvest\\|shelf_life\" src/ --include=*.tsx | head\necho \"=== Card 4: Harvest Date Time in Produce/Edit form ===\" && grep -rln \"harvest_date\\|Harvest date\\|Harvest Date\" src/ --include=*.tsx | head",
  "description": "Locate code for cards 2, 3, 4"
}
```

> TOOL

tool_result
id: toolu_019kViVCC4RUdEfUS4aGjeJD
```
=== Card 2: Fresh From Your Local Farmer ===
src/app/consumer/page.tsx:1147:              {L("Let local farmers know what you need — they'll reach out when available.", 'స్థానిక రైతులకు మీకు ఏమి కావాలో తెలియజేయండి')}
src/app/consumer/intents/page.tsx:114:          {L('Crops you asked local farmers for', 'మీరు రైతులను అడిగిన పంటలు')}
src/components/consumer/GlobalNav.tsx:41:            <span className="text-white font-bold text-sm block truncate">{L('Fresh from your local farmer', 'మీ స్థానిక రైతు నుండి తాజా')}</span>
=== Card 3: Log Harvest form ===
src/app/moderator/listings/page.tsx
src/app/moderator/listings/ListingForm.tsx
src/components/consumer/FreshHarvestsTable.tsx
src/components/farmer/OrderCard.tsx
src/app/farmer/dashboard/orders/[id]/page.tsx
src/app/moderator/listings/[id]/edit/page.tsx
src/app/consumer/page.tsx
src/app/consumer/harvest/[harvestId]/page.tsx
src/app/farmer/dashboard/orders/page.tsx
src/app/consumer/produce/[id]/page.tsx
=== Card 4: Harvest Date Time in Produce/Edit form ===
src/app/consumer/produce/[id]/page.tsx
src/app/moderator/listings/page.tsx
src/app/moderator/listings/[id]/edit/page.tsx
src/app/consumer/page.tsx
src/app/moderator/listings/ListingForm.tsx
src/app/farmer/dashboard/page.tsx
```

> AGENT

Let me look at the GlobalNav header (Card #2) and find where "Log Harvest" form lives with shelf life (Card #3).

> TOOL

tool_use Read
id: toolu_012HZy77gSFFEPceHibqXApu
```json
{
  "file_path": "/home/veerendra/farmer/yourfamilyfarmer/src/components/consumer/GlobalNav.tsx"
}
```

> TOOL

tool_result
id: toolu_012HZy77gSFFEPceHibqXApu
```
1	'use client'
2	
3	import Link from 'next/link'
4	import { useEffect, useRef, useState } from 'react'
5	import { useLang } from '@/lib/LanguageContext'
6	import LanguageToggle from '@/components/LanguageToggle'
7	import { useConsumerAuth } from '@/lib/ConsumerAuthContext'
8	
9	type ActiveTab = 'consumer' | 'farmer' | 'delivery' | 'moderator'
10	
11	// Optional location control shown in the top bar (right side, beside the
12	// greeting). Only the consumer browse page passes it; other pages omit it.
13	type LocationControl = { name: string; onClick: () => void }
14	
15	export default function GlobalNav({
16	  activeTab = 'consumer',
17	  location,
18	}: {
19	  activeTab?: ActiveTab
20	  location?: LocationControl
21	}) {
22	  const { tx, L } = useLang()
23	  const { state, consumer, openAuth, logout, suspendedReason, dismissSuspension } = useConsumerAuth()
24	
25	  const tabs = [
26	    { key: 'consumer' as const, href: '/consumer', label: tx.consumerNav },
27	    { key: 'farmer' as const, href: '/farmer/dashboard', label: tx.farmerNav },
28	    { key: 'delivery' as const, href: '/rider', label: tx.deliveryNav },
29	    { key: 'moderator' as const, href: '#', label: tx.moderatorNav, disabled: true },
30	  ]
31	
32	  return (
33	    <nav className="sticky top-0 […]

> AGENT

The header title exists in GlobalNav. Let me check the actual "Log Harvest" form and the produce Edit form to assess cards 3 & 4, and understand where "Log Harvest" is triggered from.

> TOOL

tool_use Bash
id: toolu_01DEu3dAuH1ZRMcKRavLi3q5
```json
{
  "command": "cd /home/veerendra/farmer/yourfamilyfarmer\necho \"=== files with 'Log Harvest' UI text ===\"\ngrep -rn \"Log Harvest\\|Log harvest\\|Add Harvest\\|Log a harvest\" src/ --include=*.tsx | grep -iv \"harvestlog\" | head -30",
  "description": "Find Log Harvest UI"
}
```

> TOOL

tool_result
id: toolu_01DEu3dAuH1ZRMcKRavLi3q5
```
=== files with 'Log Harvest' UI text ===
```

> TOOL

tool_use Bash
id: toolu_01Ngbon63VrrqCD6wK7grNVc
```json
{
  "command": "cd /home/veerendra/farmer/yourfamilyfarmer\ngrep -rln \"harvest\" src/app/farmer --include=*.tsx\necho \"=== HarvestLog / harvest components ===\"\nls src/components/farmer/tabs/ 2>/dev/null\ngrep -rln \"shelf_life_days\\|shelf life\\|Shelf life\\|Shelf Life\" src/app/farmer src/components/farmer src/app/moderator --include=*.tsx",
  "description": "Find harvest logging + shelf life in farmer/moderator"
}
```

> TOOL

tool_result
id: toolu_01Ngbon63VrrqCD6wK7grNVc
```
src/app/farmer/signup/page.tsx
src/app/farmer/dashboard/orders/[id]/page.tsx
src/app/farmer/login/page.tsx
src/app/farmer/dashboard/page.tsx
src/app/farmer/dashboard/orders/page.tsx
=== HarvestLog / harvest components ===
FarmMediaTab.tsx
ProduceTab.tsx
QualityTab.tsx
ReviewsTab.tsx
StoryTab.tsx
src/app/farmer/dashboard/orders/page.tsx
src/app/farmer/dashboard/orders/[id]/page.tsx
src/app/farmer/dashboard/page.tsx
src/app/moderator/listings/[id]/edit/page.tsx
src/app/moderator/listings/ListingForm.tsx
src/app/moderator/listings/page.tsx
src/components/farmer/tabs/ProduceTab.tsx
src/components/farmer/OrderCard.tsx
```

> TOOL

tool_use Bash
id: toolu_01F3iCBS3tE4Axj7jocbLAUh
```json
{
  "command": "cd /home/veerendra/farmer/yourfamilyfarmer\ngrep -n \"harvest\\|shelf\\|Shelf\\|Harvest\" src/app/farmer/dashboard/page.tsx | head -60",
  "description": "Find harvest/shelf in farmer dashboard"
}
```

> TOOL

tool_result
id: toolu_01F3iCBS3tE4Axj7jocbLAUh
```
14:import { harvestClock, freshnessLabel, type Harvest } from '@/lib/harvest'
74:  harvest_frequency: string | null
75:  harvest_frequency_count: number | null
76:  harvest_date: string | null
77:  shelf_life_days: number | null
1154:              {L('Set your farm location so nearby buyers discover your harvests first.', 'దగ్గరలో ఉన్న కొనుగోలుదారులు మీ కోతలను ముందుగా కనుగొంటారు.')}
1278:              {L('Where should the delivery rider come to collect the harvest? Include door number, street and landmark.', 'డెలివరీ రైడర్ ఎక్కడకు వచ్చి కోత తీసుకోవాలి? డోర్ నంబర్, వీధి, ల్యాండ్‌మార్క్ ఇవ్వండి.')}
1692:  // Availability range + harvesting frequency inputs were removed from the form
1693:  // (superseded by the harvests model). We still read any existing values so a
1697:  const [harvestFreq] = useState(editData?.harvest_frequency ?? '')
1698:  const [harvestFreqCount] = useState(
1699:    editData?.harvest_frequency_count != null ? String(editData.harvest_frequency_count) : '',
1701:  // Harvest date & time for this listing (stored as a full timestamp so the
1704:  const [harvestDate, setHarvestDate] = useState(() => {
1705:    if (!editData?.harvest_date) return ''
1706:    const d = new Date(editData.harvest_date)
1711:  // Shelf life (days) — how long this harvest stays fresh.
1712:  const [shelfLifeDays, setShelfLifeDays] = useState(
1713:    editData?.shelf_life_days != null ? String(editData.shelf_life_days) : '',
1834:    name: name || 'Harvest name',
1849:    // Harvest date/time and […]

> AGENT

Let me read the HarvestManager (the "Log Harvest" panel) and the produce Edit form's harvest date/shelf fields.

> TOOL

tool_use Read
id: toolu_01YN9DL9WacdkpbV1LzXYyxz
```json
{
  "file_path": "/home/veerendra/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx",
  "offset": 2119,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01YN9DL9WacdkpbV1LzXYyxz
```
2119	        {/* Availability range + harvesting frequency removed — the harvests
2120	            model (per-pick date/time + shelf life) supersedes them. */}
2121	
2122	        {/* Harvest date & time + shelf life (required) for this listing */}
2123	        <div className="space-y-2">
2124	          <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
2125	            {L('Harvest date & time', 'కోత తేదీ & సమయం')} <span className="text-red-500">*</span>
2126	          </label>
2127	          <input
2128	            type="datetime-local"
2129	            required
2130	            value={harvestDate}
2131	            onChange={(e) => setHarvestDate(e.target.value)}
2132	            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:border-green-500 focus:outline-none"
2133	          />
2134	        </div>
2135	        <div className="space-y-2">
2136	          <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
2137	            {L('Shelf life (days)', 'తాజా (రోజులు)')} <span className="text-red-500">*</span>
2138	          </label>
2139	          <input
2140	            type="number"
2141	            inputMode="numeric"
2142	            min={1}
2143	            required
2144	            placeholder={L('e.g. 5', 'ఉదా. 5')}
2145	            value={shelfLifeDays}
2146	            onChange={(e) => setShelfLifeDays(e.target.value)}
2147	            className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:border-green-500 focus:outline-none"
2148	          />
2149	        </div>
2150	
2151	        {/* Harvest timings — log/edit individual harvests (each a sellable pick
2152	            with its own date, shelf life and qty). Only when editing an existing
2153	            produce, since a harvest needs a saved produce to attach to. */}
2154	        {isEdit && editData && (
2155	          <HarvestManager listingId={editData.id} farmerId={farmerId} unit={unit} />
2156	        )}
2157	
2158 […]

> TOOL

tool_use Read
id: toolu_018Ck6xMJTq1X8io1uAWo5xK
```json
{
  "file_path": "/home/veerendra/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx",
  "offset": 2792,
  "limit": 220
}
```

> TOOL

tool_result
id: toolu_018Ck6xMJTq1X8io1uAWo5xK
```
2792	/* ─── Harvest timings manager (lives inside the produce Edit form) ─────
2793	   A produce_listing is the template; logging a harvest records one actual pick
2794	   (date+time, shelf life, qty-for-sale) into the `harvests` table — each pick is
2795	   its own sellable product powering the consumer "Today's Harvest" feed and the
2796	   "Harvested 2h ago" clock. This whole panel used to be a separate button on the
2797	   produce card; it now lives inside Edit. */
2798	function HarvestManager({ listingId, farmerId, unit }: { listingId: string; farmerId: string; unit?: string | null }) {
2799	  const { L } = useLang()
2800	  const nowLocal = () => {
2801	    const d = new Date()
2802	    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
2803	    return d.toISOString().slice(0, 16) // yyyy-MM-ddThh:mm for datetime-local
2804	  }
2805	  // datetime-local wants yyyy-MM-ddThh:mm in LOCAL time; convert a stored UTC
2806	  // ISO string back to that shape for the edit inputs.
2807	  const toLocalInput = (iso: string) => {
2808	    const d = new Date(iso)
2809	    if (isNaN(d.getTime())) return ''
2810	    d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
2811	    return d.toISOString().slice(0, 16)
2812	  }
2813	  const [harvestedAt, setHarvestedAt] = useState(nowLocal())
2814	  const [shelfLife, setShelfLife] = useState('')
2815	  const […]

> AGENT

I now have a clear picture. Let me quickly confirm the moderator side (parity) has the same harvest-date/shelf fields, so my assessment of remaining work is complete.

> TOOL

tool_use Bash
id: toolu_019523Vk7dwxEL9eusWq4qS3
```json
{
  "command": "cd /home/veerendra/farmer/yourfamilyfarmer\necho \"=== moderator ListingForm: harvest date/shelf fields ===\"\ngrep -n \"Harvest date\\|harvest_date\\|harvestDate\\|Shelf life\\|shelfLife\\|shelf_life\" src/app/moderator/listings/ListingForm.tsx | head\necho \"=== moderator: does it have a HarvestManager equivalent? ===\"\ngrep -n \"HarvestManager\\|Harvest timings\\|from('harvests')\\|Log harvest\\|Save harvest\" src/app/moderator/listings/ListingForm.tsx | head",
  "description": "Check moderator parity for harvest fields"
}
```

> TOOL

tool_result
id: toolu_019523Vk7dwxEL9eusWq4qS3
```
=== moderator ListingForm: harvest date/shelf fields ===
27:  harvest_date: string
28:  shelf_life_days: string
45:  stock_qty: '', description: '', brix: '', harvest_date: '', shelf_life_days: '',
152:    // Harvest date/time and shelf life are mandatory — they drive the buyer's
154:    if (!form.harvest_date) { setError('Harvest date & time is required.'); return }
155:    const shelfNum = parseInt(form.shelf_life_days, 10)
156:    if (!form.shelf_life_days || !Number.isFinite(shelfNum) || shelfNum <= 0) {
157:      setError('Shelf life (days) is required.'); return
295:        <Field label="Harvest date & time *">
296:          <input value={form.harvest_date} onChange={set('harvest_date')} type="datetime-local" required className={inputCls} />
=== moderator: does it have a HarvestManager equivalent? ===
```

> AGENT

I've verified all 5 cards against the actual code. Here's the honest status — **they are not all done, so I have not deployed.**

## Card-by-card

**① Separate card per Harvest in Produce — ✅ Done (but uncommitted)**
This is the only one that's actually built. It's the uncommitted diff in `src/app/consumer/page.tsx`: the grid expands each produce into one card per logged harvest (own date/shelf/stock), links to `/consumer/harvest/[id]`, and keys the cart by `harvestId`. Cart + harvest route + order plumbing already shipped in Phase 1, so this hangs together. Not committed yet.

**② "Fresh from your local farmer" title hidden — ⚠️ Likely NOT fixed**
The title still lives in `GlobalNav.tsx:41` inside a `min-w-0 ... truncate` block. On the consumer browse page the right side of the top bar carries the location chip + login/menu + language toggle, which squeezes that block — so on a 390px screen it can truncate to nothing, which matches the "totally hidden" complaint. Nothing in the current diff addresses this. Needs a layout fix (and a visual check to confirm).

**③ Remove Shelf life from Log Harvest — ❌ NOT done**
The Log Harvest panel (`HarvestManager`, `dashboard/page.tsx:2923-2932`, and again in edit mode `2974-2980`) […]