> DEVELOPER

[Image #1] have we done all these

> AGENT

I'll investigate the working tree to see which of these "In Progress" cards have actually been implemented. Let me look at the modified files and check for each card.

> TOOL

tool_use Bash
id: toolu_016icp3hv3oXCi3CPymM7FA8
```json
{
  "command": "git status && echo \"=== DIFF STAT ===\" && git diff --stat",
  "description": "Show git status and diff stat"
}
```

> TOOL

tool_use Read
id: toolu_01Rv2YvYSjBsorhJRrJkDkTv
```json
{
  "file_path": "/home/<USER>/.claude/projects/-home-veerendra-farmer-yourfamilyfarmer/memory/project_trello_todo_batch_0708.md"
}
```

> TOOL

tool_result
id: toolu_01Rv2YvYSjBsorhJRrJkDkTv
```
1	---
2	name: project_trello_todo_batch_0708
3	description: "11-card To-Do Trello batch (2026-07-08): 6 fixes done in working tree, #1 multi-farmer single-pay needs decision, #3 already done by unpushed work"
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: ea96b6a4-23e5-4070-992c-cc6cce302765
8	---
9	
10	Working through the 11-card **To Do** Trello board on 2026-07-08. Status of the cards tackled (all changes in working tree, NOT committed/pushed yet — [[feedback_ask_before_push]]):
11	
12	**Done (built + `npm run build` passes):**
13	- **#2 Harvest clock "slightly wrong":** root cause was `relTime`/`harvestAgeDays` in `src/lib/harvest.ts` counting elapsed 24h chunks (`floor(ms/86400000)`) instead of calendar days — a pick on the 5th 4pm viewed on the 7th 10am (42h) showed "yesterday" not "2 days ago". Fixed to count calendar-day diffs via `startOfLocalDay`. Shared lib ⇒ auto-fixes consumer + moderator (parity free).
14	- **#5 Show pickup/delivery date in My Orders list:** added `fulfillment_date` to `/api/consumer/orders` select, to `ConsumerOrder` type, and a 📅 Pickup/Delivery line in `OrderCard.tsx`. Farmer list already had it; moderator has no My-Orders surface (no parity needed).
15	- **#6:** Cart.tsx reworded "The farmer needs this to confirm pickup time." → "Order status will be sent."
16	- **#7:** consumer […]

> TOOL

tool_result
id: toolu_016icp3hv3oXCi3CPymM7FA8
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/app/api/consumer/orders/route.ts
	modified:   src/app/api/moderator/listings/[id]/route.ts
	modified:   src/app/api/moderator/listings/route.ts
	modified:   src/app/api/orders/place/route.ts
	modified:   src/app/consumer/orders/[id]/page.tsx
	modified:   src/app/farmer/dashboard/orders/[id]/page.tsx
	modified:   src/app/moderator/listings/ListingForm.tsx
	modified:   src/app/moderator/listings/[id]/edit/page.tsx
	modified:   src/components/consumer/Cart.tsx
	modified:   src/components/consumer/OrderCard.tsx
	modified:   src/lib/harvest.ts

no changes added to commit (use "git add" and/or "git commit -a")
=== DIFF STAT ===
 src/app/api/consumer/orders/route.ts          |   2 +-
 src/app/api/moderator/listings/[id]/route.ts  |   9 +
 src/app/api/moderator/listings/route.ts       |   9 +
 src/app/api/orders/place/route.ts             |  67 +-
 src/app/consumer/orders/[id]/page.tsx         |   2 +-
 src/app/farmer/dashboard/orders/[id]/page.tsx |   2 +-
 src/app/moderator/listings/ListingForm.tsx    |  51 +-
 src/app/moderator/listings/[id]/edit/page.tsx |   3 +
 src/components/consumer/Cart.tsx              | 873 +++++++++++++++-----------
 src/components/consumer/OrderCard.tsx         |  17 +
 src/lib/harvest.ts                            |  41 +-
 11 files changed, 677 insertions(+), 399 deletions(-)
```

> TOOL

tool_use Read
id: toolu_01SARNgmALRCMGp7JaBFPyzS
```json
{
  "file_path": "/home/<USER>/.claude/projects/-home-veerendra-farmer-yourfamilyfarmer/memory/project_per_harvest_delivery.md"
}
```

> TOOL

tool_result
id: toolu_01SARNgmALRCMGp7JaBFPyzS
```
<system-reminder>This memory is 2 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
1	---
2	name: project_per_harvest_delivery
3	description: "Trello \"Handling 2 harvests within same checkout\" — per-harvest pickup/delivery choice at checkout"
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: 43520812-9571-4279-b6af-cdb69aa846d7
8	---
9	
10	Trello card "Handling 2 harvests within same checkout" — BUILT 2026-07-07, not yet committed/pushed.
11	
12	Each cart line now picks its own Pickup/Delivery (both buttons always shown; the option a produce doesn't offer is disabled). Removed the single global top-of-cart toggle and the old cart-wide "delivery conflict" error. Address + pickup-location entry moved to one consolidated "Delivery & pickup details" block at the very END (after amounts), with payment method + per-farmer place buttons below it (approved layout choice).
13	
14	Key: `delivery_type` was already stored PER order row, so mixed pickup+delivery within one farmer order needed NO schema change — only the cart UI and the place-order API payload.
15	
16	Files:
17	- `src/components/consumer/Cart.tsx`: `deliveryByItem` map keyed by `cartKeyOf`, `deliveryOf/canPickupItem/canDeliverItem` helpers, seed effect. Place buttons + […]

> AGENT

The memory covers most cards. Let me verify the actual diffs and check the cards not mentioned in memory (overall rating, shipped date/time, notifications).

> TOOL

tool_use Bash
id: toolu_0112ddFruUGmUGzAAm4ztpYL
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== consumer orders route (card: farmer price total / fulfillment date) ===\"\ngit diff src/app/api/consumer/orders/route.ts src/components/consumer/OrderCard.tsx src/app/consumer/orders/[id]/page.tsx src/app/farmer/dashboard/orders/[id]/page.tsx\necho \"=== harvest.ts (card 6) ===\"\ngit diff src/lib/harvest.ts",
  "description": "Diff small files to confirm cards"
}
```

> TOOL

tool_result
id: toolu_0112ddFruUGmUGzAAm4ztpYL
```
=== consumer orders route (card: farmer price total / fulfillment date) ===
diff --git a/src/app/api/consumer/orders/route.ts b/src/app/api/consumer/orders/route.ts
index f4385ad..6a9d567 100644
--- a/src/app/api/consumer/orders/route.ts
+++ b/src/app/api/consumer/orders/route.ts
@@ -17,7 +17,7 @@ export async function GET(req: NextRequest) {
   const { data: orders, error } = await supabase
     .from('orders')
     .select(
-      'id, order_code, produce_name, produce_listing_id, quantity, unit, total_price, platform_fee, pickup_location, status, payment_method, payment_status, refund_status, refund_id, refund_amount, refunded_at, decline_reason, payment_proof_path, created_at, farmer_id, delivery_type, delivery_status, delivery_address, delivery_landmark, delivery_pincode, delivery_alt_phone, delivery_boy_id, handover_otp, assigned_at, picked_up_at, out_for_delivery_at, delivered_at, shipped_at, collected_at, received_at, acknowledged_at',
+      'id, order_code, produce_name, produce_listing_id, quantity, unit, total_price, platform_fee, pickup_location, status, payment_method, payment_status, refund_status, refund_id, refund_amount, refunded_at, decline_reason, payment_proof_path, created_at, fulfillment_date, farmer_id, delivery_type, delivery_status, delivery_address, delivery_landmark, delivery_pincode, delivery_alt_phone, delivery_boy_id, handover_otp, assigned_at, picked_up_at, out_for_delivery_at, delivered_at, shipped_at, collected_at, received_at, acknowledged_at',
     )
     .eq('consumer_id', session.consumerId)
     .order('created_at', { ascending: false })
diff --git a/src/app/consumer/orders/[id]/page.tsx b/src/app/consumer/orders/[id]/page.tsx
index e769e0c..a80bee8 100644
--- a/src/app/consumer/orders/[id]/page.tsx
+++ b/src/app/consumer/orders/[id]/page.tsx
@@ -335,7 +335,7 @@ export default function OrderDetailsPage() {
                   full refund timeline lives in RefundPanel). */}
               <div className="pt-2 border-t border-gray-100 mt-1 space-y-1">
                 <div className="flex items-center justify-between text-xs">
-                  <span className="text-gray-500">{L('Item total', 'వస్తువుల ధర')}</span>
+                  <span className="text-gray-500">{L('Farmer Price', 'రైతు ధర')}</span>
                   <span className="font-semibold text-gray-900">₹{order.total_price ?? 0}</span>
                 </div>
                 <div className="flex items-center justify-between text-xs">
diff --git a/src/app/farmer/dashboard/orders/[id]/page.tsx b/src/app/farmer/dashboard/orders/[id]/page.tsx
index cff1543..82f83ad 100644
--- […]

> AGENT

Cards 1–7, 10, 11 are confirmed done in the diffs. Now let me check cards 8, 9, and 13, which aren't mentioned in memory.

> TOOL

tool_use Bash
id: toolu_01FMJ7iwgBZ2FZ8errGGVY4i
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== Card 9: Shipped date/time after Mark Shipped (farmer order view) ===\"\ngrep -rn \"On the way\\|Shipped\" src/app/farmer/dashboard/orders/[id]/page.tsx | head -20\necho\necho \"=== shipped_at usage in farmer order detail ===\"\ngrep -n \"shipped_at\" src/app/farmer/dashboard/orders/[id]/page.tsx\necho\necho \"=== Card 8: overall rating above Farmer Dashboard title ===\"\ngrep -rn \"overall rating\\|overallRating\\|averageRating\\|avg_rating\\|Dashboard\" src/app/farmer/dashboard/page.tsx | head -20",
  "description": "Check cards 8, 9 implementation"
}
```

> TOOL

tool_result
id: toolu_01FMJ7iwgBZ2FZ8errGGVY4i
```
=== Card 9: Shipped date/time after Mark Shipped (farmer order view) ===
src/app/farmer/dashboard/orders/[id]/page.tsx:143:  // reads "Picked up" rather than the courier/delivery wording "Shipped".
src/app/farmer/dashboard/orders/[id]/page.tsx:173:  // sides stay in sync: Order placed → (Payment received) → Approved → Shipped
src/app/farmer/dashboard/orders/[id]/page.tsx:175:  // is gone: every order now moves farmer-taps-Shipped → buyer-taps-Delivered,
src/app/farmer/dashboard/orders/[id]/page.tsx:190:          // still show "Shipped" before "Delivered".
src/app/farmer/dashboard/orders/[id]/page.tsx:193:            : [{ label: L('Shipped', 'షిప్ చేశారు'), at: order.shipped_at, done: !!order.shipped_at }]),

=== shipped_at usage in farmer order detail ===
58:  shipped_at: string | null
69:  'id, farmer_id, order_code, produce_name, quantity, unit, total_price, platform_fee, buyer_name, buyer_phone, pickup_location, status, payment_method, payment_status, utr_number, decline_reason, refund_status, refund_amount, refunded_at, created_at, confirmed_at, paid_at, delivery_type, delivery_status, delivery_boy_id, delivery_address, delivery_city, delivery_landmark, delivery_pincode, delivery_alt_phone, assigned_at, picked_up_at, out_for_delivery_at, delivered_at, collected_at, shipped_at, received_at, fulfillment_date, acknowledged_at, harvest_id, harvest:harvests(harvested_at, shelf_life_days)'
193:            : [{ label: L('Shipped', 'షిప్ చేశారు'), at: order.shipped_at, done: !!order.shipped_at }]),

=== Card 8: overall rating above Farmer Dashboard title ===
src/app/farmer/dashboard/page.tsx:86:type DashboardListing = {
src/app/farmer/dashboard/page.tsx:153:export default function FarmerDashboard() {
src/app/farmer/dashboard/page.tsx:159:  const [listings, setListings] = useState<DashboardListing[]>([])
src/app/farmer/dashboard/page.tsx:172:  const loadDashboard = useCallback(async () => {
src/app/farmer/dashboard/page.tsx:210:    setListings((listingsRes.data ?? []) as DashboardListing[])
src/app/farmer/dashboard/page.tsx:248:  useEffect(() => { loadDashboard() }, [loadDashboard])
src/app/farmer/dashboard/page.tsx:352:    const refetch = () => { if (document.visibilityState === 'visible') loadDashboard() }
src/app/farmer/dashboard/page.tsx:359: […]

> TOOL

tool_use Bash
id: toolu_01Mek8NUPVSPA3QPPi85LFMa
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== Farmer dashboard title area (lines 380-410) ===\"\nsed -n '380,410p' src/app/farmer/dashboard/page.tsx\necho\necho \"=== Does the stepper render the 'at' date? (order detail lines 195-260) ===\"\nsed -n '195,265p' src/app/farmer/dashboard/orders/[id]/page.tsx\necho\necho \"=== rating fields anywhere in dashboard ===\"\ngrep -rn \"rating\\|Rating\\|⭐\\|review\" src/app/farmer/dashboard/page.tsx",
  "description": "Inspect dashboard title and stepper rendering"
}
```

> TOOL

tool_result
id: toolu_01Mek8NUPVSPA3QPPi85LFMa
```
=== Farmer dashboard title area (lines 380-410) ===
  const activeListings = listings.filter((l) => l.status === 'available').length

  const profileComplete = isProfileComplete(farmer)
  const displayName = farmer!.name?.trim() || tx.welcome

  return (
    <main className="min-h-screen bg-gray-50 pb-16">
      {/* Header */}
      <div className="bg-green-900 px-4 pt-6 pb-10">
        <div className="flex justify-end mb-2">
          <LanguageToggle />
        </div>
        <div className="flex items-start justify-between">
          <div>
            <p className="text-green-400 text-xs font-semibold mb-0.5 uppercase tracking-wide">
              {tx.farmerDashboard}
            </p>
            <h1 className="text-white text-xl font-extrabold leading-tight">{displayName}</h1>
            <p className="text-green-300 text-sm mt-0.5">
              {profileComplete
                ? `${farmer!.village}, ${farmer!.district}`
                : tx.completeProfilePrompt}
            </p>
            <p className="text-green-500 text-xs mt-1">+91 {farmer!.phone}</p>
          </div>
          <div className="flex flex-col items-end gap-2 flex-shrink-0">
            {profileComplete ? (
              <Link
                href={`/farmer/${farmer!.slug}`}
                className="bg-white text-green-800 text-xs font-bold px-3 py-2 rounded-xl"
              >

=== Does the stepper render the 'at' date? (order detail lines 195-260) ===
        ]
      })()
    : []

  return (
    <main className="min-h-screen bg-gray-50 pb-16">
      <div className="bg-green-900 px-4 pt-6 pb-10">
        <Link href="/farmer/dashboard/orders" className="text-green-300 text-sm flex items-center gap-1 mb-4">
          ← {tx.back}
        </Link>
        <h1 className="text-white text-xl font-extrabold leading-tight">
          {L('Order details', 'ఆర్డర్ వివరాలు')}
        </h1>
        {order?.order_code && (
          <p className="text-green-300 text-sm mt-1 font-mono">{order.order_code}</p>
        )}
      </div>

      <div className="px-4 -mt-5 space-y-4 max-w-lg mx-auto">
        {loading ? (
          <div className="bg-white rounded-2xl border border-gray-100 p-6 text-center">
            <div className="w-9 h-9 border-4 border-green-700 border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="text-gray-500 text-sm mt-3">{tx.loadingLabel}</p>
          </div>
        ) : notFound || […]

> AGENT

Let me check how the stepper renders the timestamps (card 9) and confirm no overall-rating display exists above the dashboard title (card 8).

> TOOL

tool_use Bash
id: toolu_014aFvB4ESsNQwFT8ojmfwb8
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== stepper render (search .map over steps/timeline) ===\"\ngrep -n \"\\.map\\|steps\\|timeline\\|\\.at\\b\\|formatDateTime\\|toLocaleString\" src/app/farmer/dashboard/orders/[id]/page.tsx | head -30",
  "description": "Find stepper rendering"
}
```

> TOOL

tool_result
id: toolu_014aFvB4ESsNQwFT8ojmfwb8
```
=== stepper render (search .map over steps/timeline) ===
131:    iso ? new Date(iso).toLocaleString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : ''
258:                      <span className="font-normal text-green-700"> · {new Date(h.harvested_at).toLocaleString('en-IN', {
377:                  {milestones.map((m, idx) => (
387:                        {m.at && m.done && <p className="text-[10px] text-gray-400 mt-0.5">{fmt(m.at)}</p>}
```

> TOOL

tool_use Bash
id: toolu_01ABzW1tt1S5ABiGCBjVieWZ
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== 'On the way' text location ===\"\ngrep -rn \"On the way\\|Shipped -\\|Shipped—\\|Shipped ·\" src/ | head\necho\necho \"=== statusText for shipped in farmer order detail ===\"\nsed -n '95,145p' src/app/farmer/dashboard/orders/[id]/page.tsx",
  "description": "Find On the way text and shipped status"
}
```

> TOOL

tool_result
id: toolu_01ABzW1tt1S5ABiGCBjVieWZ
```
=== 'On the way' text location ===
src/app/consumer/orders/[id]/page.tsx:766:    { key: 'assigned', label: 'Rider assigned', sub: 'On the way to farmer', at: order.assigned_at },
src/app/consumer/orders/[id]/page.tsx:768:    { key: 'out_for_delivery', label: 'Out for delivery', sub: 'On the way to you', at: order.out_for_delivery_at },
src/components/consumer/OrderCard.tsx:176:    if (order.shipped_at) return L('On the way', 'దారిలో ఉంది')

=== statusText for shipped in farmer order detail ===
      .maybeSingle()
      .then(async ({ data }) => {
        if (cancelled) return
        if (!data) { setNotFound(true); setLoading(false); return }
        // Best-effort reschedule reason: the column may not exist until its
        // migration is applied, so fetch it separately and ignore failure.
        const { data: rs } = await supabase
          .from('orders')
          .select('reschedule_reason')
          .eq('id', id)
          .maybeSingle()
        if (cancelled) return
        setOrder({ ...(data as Order), reschedule_reason: (rs as { reschedule_reason?: string | null } | null)?.reschedule_reason ?? null })
        setLoading(false)
      })
    return () => { cancelled = true }
  }, [id, router])

  // Pull the assigned rider's contact for home deliveries (mirrors the card).
  useEffect(() => {
    const riderId = order?.delivery_boy_id ?? null
    if (!riderId) { setRider(null); return }
    let cancelled = false
    supabase
      .from('delivery_boys')
      .select('name, phone')
      .eq('id', riderId)
      .maybeSingle()
      .then(({ data }) => {
        if (cancelled || !data) return
        setRider({ name: data.name ?? […]

> AGENT

Let me verify card 10 (combined multi-farmer pay) is in the Cart diff and check card 13 (notifications).

> TOOL

tool_use Bash
id: toolu_01FX9d91UT5jcfNeWvnGD2dQ
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== Card 10: combined multi-farmer razorpay ===\"\ngit diff src/components/consumer/Cart.tsx | grep -n \"handleRazorpayOrderAll\\|Order & Pay\\|combined\\|multi-farmer\\|multiFarmer\" | head\necho\necho \"=== Card 13: notifications on farmer dashboard ===\"\ngrep -rln \"Notification\\|notification\\|web-push\\|onesignal\\|firebase\\|FCM\\|push\" src/app/farmer/ 2>/dev/null | head\necho \"--- any notifications table/lib ---\"\ngrep -rln \"notification\" src/lib src/app/api 2>/dev/null | head",
  "description": "Verify card 10 and check notifications"
}
```

> TOOL

tool_result
id: toolu_01FX9d91UT5jcfNeWvnGD2dQ
```
=== Card 10: combined multi-farmer razorpay ===
160:+  // orders, then collect ONE payment for the combined total into the platform's
162:+  // multi-farmer cart pays once — pickup is still chosen per farmer above, and
164:+  const handleRazorpayOrderAll = async () => {
915:-                                : `💳 Order & Pay ₹${(() => {
947:+                  platform, which then settles each farmer), so a multi-farmer
953:+                  // combined pay button.
965:+                      onClick={() => requireAuth(() => (single ? handleRazorpayOrderFarmer(farmerGroups[0]) : handleRazorpayOrderAll()))}
973:+                      {payingOnline != null ? 'Opening payment...' : `💳 Order & Pay ₹${cartSubtotal + cartFee}`}

=== Card 13: notifications on farmer dashboard ===
src/app/farmer/dashboard/orders/page.tsx
src/app/farmer/dashboard/page.tsx
--- any notifications table/lib ---
```

> TOOL

tool_use Bash
id: toolu_01UANS2RBmRTPUGkTzqTNpUB
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\ngrep -n \"otification\" src/app/farmer/dashboard/orders/page.tsx src/app/farmer/dashboard/page.tsx",
  "description": "Check what notification refs exist"
}
```

> TOOL

tool_result
id: toolu_01UANS2RBmRTPUGkTzqTNpUB
```
src/app/farmer/dashboard/page.tsx:259:  // Fires a browser notification when:
src/app/farmer/dashboard/page.tsx:265:    const fireNotification = (title: string, body: string) => {
src/app/farmer/dashboard/page.tsx:267:      if (!('Notification' in window)) return
src/app/farmer/dashboard/page.tsx:268:      if (Notification.permission !== 'granted') return
src/app/farmer/dashboard/page.tsx:270:        new Notification(title, { body, icon: '/icon-192.png', tag: 'yff-order' })
src/app/farmer/dashboard/page.tsx:286:          fireNotification(
src/app/farmer/dashboard/page.tsx:309:              fireNotification(
src/app/farmer/dashboard/page.tsx:326:            fireNotification(
src/app/farmer/dashboard/page.tsx:331:          // Fire notification when buyer claims payment (covers initial pay AND retry)
src/app/farmer/dashboard/page.tsx:336:            fireNotification(
src/app/farmer/dashboard/page.tsx:435:        {/* Notification permission banner — shown only if browser supports it
src/app/farmer/dashboard/page.tsx:438:        <NotificationPermissionBanner />
src/app/farmer/dashboard/page.tsx:645:/* ─── Notification permission banner ───────────────────────── */
src/app/farmer/dashboard/page.tsx:646:function NotificationPermissionBanner() {
src/app/farmer/dashboard/page.tsx:652:    if (typeof window === 'undefined' || !('Notification' in window)) {
src/app/farmer/dashboard/page.tsx:656:    setPerm(Notification.permission as 'default' | 'granted' | 'denied')
src/app/farmer/dashboard/page.tsx:661:    if (typeof window === 'undefined' || !('Notification' in window)) return
src/app/farmer/dashboard/page.tsx:662:    const result = await Notification.requestPermission()
src/app/farmer/dashboard/page.tsx:665:      try { new Notification('YourFamilyFarmer', { body: 'You will be alerted on every new order.' }) } catch {}
src/app/farmer/dashboard/page.tsx:683:            {L('Notifications blocked', 'నోటిఫికేషన్‌లు బ్లాక్')}
src/app/farmer/dashboard/page.tsx:686:            Enable notifications in your browser settings to get alerted on new orders.
src/app/farmer/dashboard/page.tsx:702:          Allow notifications to be alerted the moment a buyer places an order.
```

> AGENT

Let me quickly check card 9 — the farmer's order *summary/list* view, where "Shipped - On the way" would appear without a date.

> TOOL

tool_use Bash
id: toolu_01BBvo8GVvSaegwnZ3gpM1dW
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\ngrep -n \"shipped\\|Shipped\\|On the way\\|fulfillment_date\\|toLocaleString\\|statusText\" src/app/farmer/dashboard/orders/page.tsx | head -30",
  "description": "Check farmer order list for shipped date"
}
```

> TOOL

tool_result
id: toolu_01BBvo8GVvSaegwnZ3gpM1dW
```
13:type StatusFilter = 'all' | 'pending' | 'approved' | 'shipped' | 'completed' | 'declined' | 'cancelled'
16:// An order the farmer can still act on (approve/decline, mark picked-up/shipped,
30:  // approved: resolved (collected / received / delivered) → completed; shipped
31:  // (farmer marked it shipped, buyer hasn't confirmed yet) → shipped; otherwise
34:  if (o.shipped_at) return 'shipped'
61:    if (s && ['pending', 'approved', 'shipped', 'completed', 'declined', 'cancelled'].includes(s)) {
82:      .select('id, farmer_id, order_code, produce_listing_id, harvest_id, harvest:harvests(harvested_at, shelf_life_days), produce_name, quantity, unit, total_price, delivery_fee, platform_fee, buyer_name, buyer_phone, pickup_location, status, payment_method, payment_status, utr_number, decline_reason, refund_status, refund_amount, refunded_at, delivery_type, delivery_status, delivery_boy_id, collected_at, shipped_at, received_at, fulfillment_date, created_at, acknowledged_at')
142:      ? { ...o, fulfillment_date: value, ...(reason ? { reschedule_reason: reason } : {}) }
145:    await supabase.from('orders').update({ fulfillment_date: value }).eq('id', orderId)
167:      .update({ status: 'approved', fulfillment_date: date, confirmed_at: new Date().toISOString() })
178:      prev.map((o) => (o.id === orderId ? { ...o, status: 'approved', fulfillment_date: date } : o)),
183:  // Courier / farmer-driven home delivery: the farmer marks it Shipped (trust-
184:  // based dispatch, no code). Stamps shipped_at; the order stays active until the
186:  const handleMarkShipped = async (orderId: string) => {
194:      if (!res.ok) { alert(json.error || L('Could not mark […]

> AGENT

I've now traced every card. Here's the status of all 13 "In Progress" cards.

## Done (9 cards in the current working tree, not yet pushed)

| # | Card | Where |
|---|------|-------|
| 1 | Consumer order detail → "Item total" renamed **Farmer Price** | `consumer/orders/[id]/page.tsx` ✅ |
| 2 | Cart reword → **"Order status will be sent"** | `Cart.tsx` ✅ |
| 3 | **Pickup/Delivery date** shown in My Orders list | `OrderCard.tsx` + `consumer/orders/route.ts` (`fulfillment_date`) ✅ |
| 4 | Moderator **Edit Listing synced** with farmer (delivery method was missing) | `ListingForm.tsx`, edit page, POST + PUT routes ✅ |
| 5 | Remove **"Self pickup from farm"** under Your Cart title | string already gone via per-harvest work ✅ |
| 6 | **Harvest clock** "yesterday" bug (calendar-day fix) | `lib/harvest.ts` ✅ |
| 7 | Farmer order detail → "Item total" renamed **Your Price** | `farmer/dashboard/orders/[id]/page.tsx` ✅ |
| 10 | **2 orders from different farmers** in one checkout | `Cart.tsx` `handleRazorpayOrderAll` — single combined pay ✅ |
| 11 | **2 harvests in same checkout** (per-line pickup/delivery) | `Cart.tsx` + `orders/place/route.ts` ✅ |

## Already present in committed code (2 cards)

- […]

> DEVELOPER

do 8

> TOOL

tool_use Read
id: toolu_012Avpgxbe4dDPUahW6Eavad
```json
{
  "__unparsedToolInput": {
    "raw": "{\"file_path\": \"/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx\", \"offset\": 370, \"limit\": 60}}",
    "len": 119
  }
}
```

> TOOL

tool_result ERROR
id: toolu_012Avpgxbe4dDPUahW6Eavad
```
<tool_use_error>InputValidationError: Read was called with input that could not be parsed as JSON.
You sent (first 119 of 119 bytes): {"file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx", "offset": 370, "limit": 60}}
Common causes: unescaped backslashes in file paths (use / or \\), unescaped control characters, or truncated output. Retry with valid JSON.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_016zXLC7x4BWHL6GKKzmd3TJ
```json
{
  "__unparsedToolInput": {
    "raw": "{\"file_path\": \"/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx\", \"offset\": 370, 60, \"limit\": 60}",
    "len": 122
  }
}
```

> TOOL

tool_result ERROR
id: toolu_016zXLC7x4BWHL6GKKzmd3TJ
```
<tool_use_error>InputValidationError: Read was called with input that could not be parsed as JSON.
You sent (first 122 of 122 bytes): {"file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx", "offset": 370, 60, "limit": 60}
Common causes: unescaped backslashes in file paths (use / or \\), unescaped control characters, or truncated output. Retry with valid JSON.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_01MY1ry5PPcbse9P4CfYdvZe
```json
{
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx",
  "offset": 375,
  "limit": 45
}
```

> TOOL

tool_result
id: toolu_01MY1ry5PPcbse9P4CfYdvZe
```
375	  // The list now also holds approved-but-unresolved orders; the stat card should
376	  // still reflect only the orders that genuinely need a response.
377	  const pendingCount = pendingOrders.filter((o) => o.status === 'pending').length
378	  // Active = visible-to-buyers listings, derived so the count stays in sync when
379	  // the farmer suspends/resumes from the inline produce list below.
380	  const activeListings = listings.filter((l) => l.status === 'available').length
381	
382	  const profileComplete = isProfileComplete(farmer)
383	  const displayName = farmer!.name?.trim() || tx.welcome
384	
385	  return (
386	    <main className="min-h-screen bg-gray-50 pb-16">
387	      {/* Header */}
388	      <div className="bg-green-900 px-4 pt-6 pb-10">
389	        <div className="flex justify-end mb-2">
390	          <LanguageToggle />
391	        </div>
392	        <div className="flex items-start justify-between">
393	          <div>
394	            <p className="text-green-400 text-xs font-semibold mb-0.5 uppercase tracking-wide">
395	              {tx.farmerDashboard}
396	            </p>
397	            <h1 className="text-white text-xl font-extrabold leading-tight">{displayName}</h1>
398	            <p className="text-green-300 text-sm mt-0.5">
399	              {profileComplete
400	                ? `${farmer!.village}, ${farmer!.district}`
401	                : tx.completeProfilePrompt}
402	            </p>
403	            <p className="text-green-500 text-xs mt-1">+91 {farmer!.phone}</p>
404	          </div>
405	          <div className="flex flex-col items-end gap-2 flex-shrink-0">
406	            {profileComplete ? (
407	              <Link
408	                href={`/farmer/${farmer!.slug}`}
409	                className="bg-white text-green-800 text-xs font-bold px-3 py-2 rounded-xl"
410	              >
411	                {tx.viewProfile} ↗
412	              </Link>
413	            ) : (
414	              <span className="bg-amber-400 […]

> TOOL

tool_use Bash
id: toolu_01FkX9gbii7VLFwZCLxFGTUR
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== how tx / L are set in FarmerDashboard component ===\"\nsed -n '153,172p' src/app/farmer/dashboard/page.tsx\necho \"=== does 'reviews' exist in tx dict? ===\"\ngrep -n \"reviews\\|review\\b\\|farmerDashboard:\" src/app/farmer/dashboard/page.tsx | head\necho \"=== L helper definition / useLang ===\"\ngrep -n \"useLang\\|const L =\\|const { t\\|const tx =\\|function useT\\|reviews:\" src/app/farmer/dashboard/page.tsx | head",
  "description": "Determine translation helpers in scope"
}
```

> TOOL

tool_result
id: toolu_01FkX9gbii7VLFwZCLxFGTUR
```
=== how tx / L are set in FarmerDashboard component ===
export default function FarmerDashboard() {
  const router = useRouter()
  const { tx, L } = useLang()
  const [farmer, setFarmer] = useState<Farmer | null>(null)
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)
  const [listings, setListings] = useState<DashboardListing[]>([])
  const [pendingOrders, setPendingOrders] = useState<Order[]>([])
  const [todayCount, setTodayCount] = useState(0)
  const [approvedCount, setApprovedCount] = useState(0)
  const [totalRevenue, setTotalRevenue] = useState(0)
  const [supplyDemand, setSupplyDemand] = useState<CropBalance[]>([])
  const [monthlyRevenue, setMonthlyRevenue] = useState(0)
  const [monthlyOrderCount, setMonthlyOrderCount] = useState(0)
  const [weeklyEarnings, setWeeklyEarnings] = useState<number[]>([0, 0, 0, 0])
  const [showForm, setShowForm] = useState(false)
  const [showProfileEdit, setShowProfileEdit] = useState(false)
  const [showListings, setShowListings] = useState(false)

  const loadDashboard = useCallback(async () => {
=== does 'reviews' exist in tx dict? ===
765:  const [coverPreview, setCoverPreview] = useState('')
770:  const [avatarPreview, setAvatarPreview] = useState('')
775:  const [certPreview, setCertPreview] = useState('')
781:  const [qrPreview, setQrPreview] = useState('')
837:    setPreview: (s: string) => void,
838:    currentPreview: string,
845:    if (currentPreview) URL.revokeObjectURL(currentPreview)
848:    setPreview(URL.createObjectURL(compressed))
1216:              preview={coverPreview}
1218:              onPick={(e) => handlePickFile(e, setCoverFile, setCoverPreview, coverPreview)}
=== L helper definition / useLang ===
8:import { useLang } from '@/lib/LanguageContext'
155:  const { tx, L } = useLang()
647:  const { L } […]

> AGENT

`L` is available in the component. Now let me add the aggregate computation and the rating display above the title.

> TOOL

tool_use Edit
id: toolu_015RiSnXUZV9vHBAYmgnqM3T
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx",
  "old_string": "  const activeListings = listings.filter((l) => l.status === 'available').length\n\n  const profileComplete = isProfileComplete(farmer)",
  "new_string": "  const activeListings = listings.filter((l) => l.status === 'available').length\n\n  // Overall rating across ALL of this farmer's harvests — a review-count-weighted\n  // mean (a harvest with more reviews pulls proportionally harder) so it matches\n  // the single number a buyer would infer from the whole catalogue. Only harvests\n  // that actually carry reviews contribute; with none, we hide the badge rather\n  // than show a misleading 0.0.\n  const ratedListings = listings.filter((l) => (l.review_count ?? 0) > 0 && l.rating_avg != null)\n  const totalReviews = ratedListings.reduce((sum, l) => sum + (l.review_count ?? 0), 0)\n  const overallRating =\n    totalReviews > 0\n      ? ratedListings.reduce((sum, l) => sum + (l.rating_avg ?? 0) * (l.review_count ?? 0), 0) / totalReviews\n      : null\n\n  const profileComplete = isProfileComplete(farmer)"
}
```

> TOOL

tool_result
id: toolu_015RiSnXUZV9vHBAYmgnqM3T
```
The file /home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01RMt6sR4wGNZRmohL5muc1X
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx",
  "old_string": "          <div>\n            <p className=\"text-green-400 text-xs font-semibold mb-0.5 uppercase tracking-wide\">\n              {tx.farmerDashboard}\n            </p>",
  "new_string": "          <div>\n            {/* Overall rating across all harvests, sits above the dashboard title. */}\n            {overallRating != null && (\n              <div className=\"flex items-center gap-1 mb-1\">\n                <span className=\"text-amber-400 text-sm leading-none\">★</span>\n                <span className=\"text-white text-sm font-bold leading-none\">{overallRating.toFixed(1)}</span>\n                <span className=\"text-green-400 text-[11px] leading-none\">\n                  ({totalReviews}{' '}\n                  {totalReviews === 1 ? L('review', 'సమీక్ష') : L('reviews', 'సమీక్షలు')})\n                </span>\n              </div>\n            )}\n            <p className=\"text-green-400 text-xs font-semibold mb-0.5 uppercase tracking-wide\">\n              {tx.farmerDashboard}\n            </p>"
}
```

> TOOL

tool_result
id: toolu_01RMt6sR4wGNZRmohL5muc1X
```
The file /home/<USER>/farmer/yourfamilyfarmer/src/app/farmer/dashboard/page.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now, per the farmer↔moderator parity rule, let me check whether the moderator module has an equivalent farmer-dashboard/overview surface to mirror this into.

> TOOL

tool_use Bash
id: toolu_01UzWpVDms5iU5FimSnbysD2
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== moderator pages ===\"\nfind src/app/moderator -name \"page.tsx\" | head -40\necho\necho \"=== moderator farmer-detail or dashboard-like views + rating usage ===\"\ngrep -rln \"rating_avg\\|review_count\\|farmerDashboard\\|Farmer Dashboard\" src/app/moderator 2>/dev/null",
  "description": "Survey moderator module for parity target"
}
```

> TOOL

tool_result
id: toolu_01UzWpVDms5iU5FimSnbysD2
```
=== moderator pages ===
src/app/moderator/page.tsx
src/app/moderator/listings/page.tsx
src/app/moderator/register-farmer/page.tsx
src/app/moderator/escalations/page.tsx
src/app/moderator/my-farmers/page.tsx
src/app/moderator/login/page.tsx
src/app/moderator/farmers/page.tsx
src/app/moderator/consumers/page.tsx
src/app/moderator/agents/page.tsx
src/app/moderator/audit/page.tsx
src/app/moderator/prices/page.tsx
src/app/moderator/farmers/new/page.tsx
src/app/moderator/reports/page.tsx
src/app/moderator/supply/page.tsx
src/app/moderator/listings/new/page.tsx
src/app/moderator/farmers/[id]/edit/page.tsx
src/app/moderator/listings/[id]/edit/page.tsx

=== moderator farmer-detail or dashboard-like views + rating usage ===
src/app/moderator/listings/page.tsx
```

> TOOL

tool_use Bash
id: toolu_0195LKH4tdq8pHwYBwaVPAfY
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== how moderator listings page uses rating ===\"\ngrep -n \"rating_avg\\|review_count\\|★\\|rating\" src/app/moderator/listings/page.tsx | head\necho\necho \"=== moderator farmers page: does it list farmers / show per-farmer info? ===\"\ngrep -n \"rating\\|farmer\\|Farmer\\|<h1\\|title\" src/app/moderator/farmers/page.tsx | head -25",
  "description": "Inspect moderator listings and farmers pages"
}
```

> TOOL

tool_result
id: toolu_0195LKH4tdq8pHwYBwaVPAfY
```
=== how moderator listings page uses rating ===
24:  rating_avg: number | null
25:  review_count: number | null
60:  const [sortBy, setSortBy] = useState<'fresh' | 'rating' | 'purchases'>('fresh')
84:  // Apply method + farmer filters, then sort by harvest date / rating / purchases.
94:      if (sortBy === 'rating') {
95:        return (b.rating_avg ?? 0) - (a.rating_avg ?? 0) || (b.review_count ?? 0) - (a.review_count ?? 0)
166:          onChange={(e) => setSortBy(e.target.value as 'fresh' | 'rating' | 'purchases')}
170:          <option value="rating">⭐ Rating</option>
238:                {l.rating_avg != null && (l.review_count ?? 0) > 0 && (
239:                  <span>Rating: <b>{l.rating_avg.toFixed(1)}★</b> ({l.review_count})</span>

=== moderator farmers page: does it list farmers / show per-farmer info? ===
7:type Farmer = {
25:export default function ModeratorFarmersPage() {
28:  const [farmers, setFarmers] = useState<Farmer[]>([])
34:    const r = await fetch('/api/moderator/farmers', { credentials: 'same-origin' }).catch(() => null)
38:    if (!r.ok) { setError(json?.error ?? 'Could not load farmers.'); return }
39:    setFarmers((json.farmers ?? []) as Farmer[])
44:  const toggleActive = async (f: Farmer) => {
47:    const r = await fetch(`/api/moderator/farmers/${f.id}`, {
55:    setFarmers((list) => list.map((x) => (x.id === f.id ? { ...x, active: !x.active } : x)))
66:  const activeCount = farmers.filter((f) => f.active).length
69:    <ModeratorShell […]

> AGENT

The moderator module has no per-farmer dashboard equivalent (its listings page already shows per-harvest ratings, and the farmers page is a management list, not a dashboard) — so there's no natural parity target for an "above the dashboard title" aggregate. I'll keep the change to the farmer dashboard. Let me verify it builds.

> TOOL

tool_use Bash
id: toolu_01JAAhUhwu44ZiaQW4CTQuow
```json
{
  "command": "npm run build 2>&1 | tail -25",
  "description": "Production build to verify change compiles"
}
```

> TOOL

tool_result
id: toolu_01JAAhUhwu44ZiaQW4CTQuow
```
├ ○ /moderator/consumers
├ ○ /moderator/escalations
├ ○ /moderator/farmers
├ ƒ /moderator/farmers/[id]/edit
├ ○ /moderator/farmers/new
├ ○ /moderator/listings
├ ƒ /moderator/listings/[id]/edit
├ ○ /moderator/listings/new
├ ○ /moderator/login
├ ○ /moderator/my-farmers
├ ○ /moderator/prices
├ ○ /moderator/register-farmer
├ ○ /moderator/reports
├ ○ /moderator/supply
├ ƒ /region/[slug]
├ ○ /rider
├ ○ /rider/complaints
├ ○ /rider/dashboard
├ ○ /rider/login
└ ○ /rider/signup


○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

> TOOL

tool_use Bash
id: toolu_014Gi58mp2Ke8arHmGvo6WXa
```json
{
  "command": "npm run build 2>&1 | grep -iE \"error|failed|✓ Compiled|Compiled successfully\" | head",
  "description": "Check build status line"
}
```

> TOOL

tool_result
id: toolu_014Gi58mp2Ke8arHmGvo6WXa
```
✓ Compiled successfully in 8.5s
```

> AGENT

Build passes. Card #8 is done.

## What I did

Added the farmer's **overall rating** above the "Farmer Dashboard" title in `src/app/farmer/dashboard/page.tsx`:

- **Computed** a review-count-weighted mean across all the farmer's harvests (`rating_avg` × `review_count`, summed and divided by total reviews) — data already loaded, no extra query. Harvests with no reviews are excluded, and if there are none the badge is hidden rather than showing a misleading `0.0`.
- **Rendered** `★ 4.6 (23 reviews)` above the title, bilingual (review/reviews singular-plural handled via `L()`).

## Parity note (#12 rule)

No moderator change: the moderator module has no per-farmer dashboard clone. Its listings page already shows per-harvest ratings, and the farmers page is a management list, not a dashboard — so there's no "above the dashboard title" surface to mirror. If you'd like, I could instead add an overall-rating column to the moderator **farmers** list, but that's beyond this card.

## Verified
- `npm run build` → **Compiled successfully**.
- Left untested: the exact number depends on live Supabase `rating_avg`/`review_count` values — worth a glance on a farmer account that has reviews.

This is uncommitted, along with the rest of the batch. Want me to commit everything (I'll hold off on […]

> DEVELOPER

commit and push to main

> AGENT

User explicitly authorized the push. Let me review the full scope, commit, and push.

> TOOL

tool_use Bash
id: toolu_01LUATX3kC4HMGKSRtEWsyx6
```json
{
  "command": "git status --short",
  "description": "Confirm files to commit"
}
```

> TOOL

tool_result
id: toolu_01LUATX3kC4HMGKSRtEWsyx6
```
 M src/app/api/consumer/orders/route.ts
 M src/app/api/moderator/listings/[id]/route.ts
 M src/app/api/moderator/listings/route.ts
 M src/app/api/orders/place/route.ts
 M src/app/consumer/orders/[id]/page.tsx
 M src/app/farmer/dashboard/orders/[id]/page.tsx
 M src/app/farmer/dashboard/page.tsx
 M src/app/moderator/listings/ListingForm.tsx
 M src/app/moderator/listings/[id]/edit/page.tsx
 M src/components/consumer/Cart.tsx
 M src/components/consumer/OrderCard.tsx
 M src/lib/harvest.ts
```

> TOOL

tool_use Bash
id: toolu_01TeVtRRYVXHqn82VtpJNjbH
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\ngit add -A\ngit commit -q -F - <<'EOF'\nfeat(trello): In-Progress batch — labels, harvest clock, moderator sync, combined pay, farmer rating\n\n- consumer order detail \"Item total\" → \"Farmer Price\"; farmer order detail → \"Your Price\"\n- cart WhatsApp hint reworded to \"Order status will be sent\"\n- My Orders list shows scheduled pickup/delivery date (fulfillment_date)\n- moderator Edit Listing now carries delivery_mode/charge/radius (parity with farmer form + POST/PUT)\n- harvest clock counts calendar days, not 24h chunks (no more \"yesterday\" for a 2-day-old pick)\n- checkout: per-line pickup/delivery + single combined Razorpay pay across multiple farmers\n- farmer dashboard shows review-count-weighted overall rating above the title\n\nCo-Authored-By: Claude Opus 4.8 <<REDACTED_EMAIL>>\nEOF\ngit log --oneline -1",
  "description": "Stage and commit the batch"
}
```

> TOOL

tool_result
id: toolu_01TeVtRRYVXHqn82VtpJNjbH
```
683403f feat(trello): In-Progress batch — labels, harvest clock, moderator sync, combined pay, farmer rating
```

> TOOL

tool_use Bash
id: toolu_012cssTzDTks2NpcyHBzUFfg
```json
{
  "command": "git push origin main 2>&1 | tail -8",
  "description": "Push to origin main"
}
```

> TOOL

tool_result
id: toolu_012cssTzDTks2NpcyHBzUFfg
```
[entire] Pushing entire/checkpoints/v1 to origin........ done
To github.com:singampalliveerendra/your_family_farmer.git
   27a6cd5..683403f  main -> main
```

> AGENT

Committed and pushed to `main`.

- **Commit:** `683403f` — the full In-Progress batch (11 files)
- **Pushed:** `27a6cd5..683403f  main -> main`
- Vercel deploys from `main`, so this will auto-deploy.

Let me update memory to reflect that this batch is now shipped.

> TOOL

tool_use Edit
id: toolu_01Ty3oJYviMS3bWXNKZXS2Cy
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/.claude/projects/-home-veerendra-farmer-yourfamilyfarmer/memory/project_trello_todo_batch_0708.md",
  "old_string": "Working through the 11-card **To Do** Trello board on 2026-07-08. Status of the cards tackled (all changes in working tree, NOT committed/pushed yet — [[feedback_ask_before_push]]):",
  "new_string": "**SHIPPED to main 2026-07-09 (683403f, pushed).** Also added the In-Progress card #8 in this commit: farmer dashboard now shows a review-count-weighted overall rating (⭐ + count) above the \"Farmer Dashboard\" title (`farmer/dashboard/page.tsx`). No moderator parity — moderator has no per-farmer dashboard clone (its listings page already shows per-harvest ratings). Still open from that board: #12 \"new environment for real farmers\" (infra, needs Vercel/Supabase decision), #13 \"test notifications\" (feature already built, just needs live QA).\n\n---\nWorking through the 11-card **To Do** Trello board on 2026-07-08. Status of the cards tackled (all changes in working tree, NOT committed/pushed yet — [[feedback_ask_before_push]]):"
}
```

> TOOL

tool_result
id: toolu_01Ty3oJYviMS3bWXNKZXS2Cy
```
The file /home/<USER>/.claude/projects/-home-veerendra-farmer-yourfamilyfarmer/memory/project_trello_todo_batch_0708.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done. Summary:

- **Card #8 built** — overall (review-count-weighted) rating shown above the Farmer Dashboard title; build passes.
- **Committed** as `683403f` and **pushed to `main`** (`27a6cd5..683403f`), which triggers the Vercel deploy.
- **Memory updated** to mark the batch shipped.

Remaining from that board: **#12** (new test environment — needs your Vercel/Supabase decision) and **#13** (notifications feature already exists; just needs live QA).

> DEVELOPER

whats the main motto of this application that we are building

> AGENT

Based on the project context (`CLAUDE.md`), the core motto/mission of **YourFamilyFarmer** is:

> **Connecting natural farmers directly to buyers in Andhra Pradesh — no middlemen, no app download, no barriers.**

The guiding principles that flow from that:

- **Farmer-first, direct-to-buyer** — natural/organic farmers get a direct line to consumers, keeping more value with the grower (hence the "Farmer Price" vs "Your Price" framing you just shipped).
- **Radically accessible** — a mobile-first PWA with *no app download required*, built to load under 3 seconds on slow Android 4G connections common in rural AP.
- **Freshness & trust as the USP** — the "harvest-as-product" model (today's harvest feed, harvest clock, shelf-life, ratings) is all about proving *how fresh* and *how trusted* each pick is.
- **Lean MVP** — no payments-heavy complexity, no native app, English-only, mobile min-width 390px.

In one line: **a natural farmer's family, connected to yours — fresh harvests direct from the farm, on any phone.**

> DEVELOPER

and also project description

> AGENT

## YourFamilyFarmer — Project Description

**What it is**
A mobile-first Progressive Web App (PWA) that connects natural/organic farmers in Andhra Pradesh directly to buyers — cutting out middlemen. It runs in the browser with no app download, and is engineered for the slow Android 4G connections common in rural AP (target: page load under 3 seconds).

**Who it's for**
- **Farmers** — list their harvests, manage orders, set prices, track earnings, get notified on new orders.
- **Consumers** — browse today's fresh harvests, order with pickup or home delivery, pay online (Razorpay) or COD, track and rate orders.
- **Moderators** — onboard/manage farmers, manage listings, oversee supply/demand, handle escalations (mirrors farmer features for parity).
- **Delivery riders** — a rider module for home deliveries.

**Core concept — "harvest as product"**
Instead of generic produce listings, the app centers on the *harvest*: each card shows when it was picked (a "harvest clock"), shelf life, freshness, and ratings — making freshness and trust the product's selling point.

**Tech stack**
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- Supabase (PostgreSQL + Storage)
- Vercel hosting (auto-deploys from `main`)
- Razorpay for payments; Twilio WhatsApp API planned for onboarding/notifications

**MVP scope […]

> DEVELOPER

[Image #2] can you add this as fevicon

> AGENT

I'll set up this logo as the favicon. First let me find the image file and understand the current favicon/icon setup.

> TOOL

tool_use Bash
id: toolu_01P9Khr6RNKb5g1WkJ5P5JYG
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== image cache file ===\"\nls -la /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png\nfile /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png\necho\necho \"=== current favicon / icon files ===\"\nls -la public/ | grep -iE \"icon|favicon|apple|logo\" \nls -la src/app/ | grep -iE \"icon|favicon\"\necho\necho \"=== manifest / metadata references ===\"\ngrep -rn \"favicon\\|icon-192\\|icon-512\\|apple-touch\\|manifest\\|icons\" src/app/layout.tsx public/manifest.json public/manifest.webmanifest 2>/dev/null | head -30",
  "description": "Locate image and current favicon setup"
}
```

> TOOL

tool_result
id: toolu_01P9Khr6RNKb5g1WkJ5P5JYG
```
=== image cache file ===
-rw------- 1 veerendra veerendra 1528097 Jul  9 15:37 /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png
/home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png: PNG image data, 1254 x 1254, 8-bit/color RGBA, non-interlaced

=== current favicon / icon files ===
-rw-r--r--  1 veerendra veerendra 25931 Apr 16 10:13 favicon.ico

=== manifest / metadata references ===
```

> TOOL

tool_use Bash
id: toolu_01XbKY6WsTnnLLAXz2WuRWF8
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== all icon-ish files in public and app ===\"\nfind public src/app -maxdepth 2 -iregex \".*\\(icon\\|favicon\\|apple\\|logo\\|manifest\\|png\\).*\" 2>/dev/null\necho\necho \"=== layout.tsx metadata/icons ===\"\ngrep -rn \"icon\\|Icon\\|favicon\\|manifest\\|metadata\\|apple\\|<link\" src/app/layout.tsx | head -30\necho\necho \"=== manifest referenced anywhere ===\"\ngrep -rln \"manifest\\|icon-192\\|icon-512\\|apple-touch\" src/ public/ 2>/dev/null | head",
  "description": "Find all icon files and manifest references"
}
```

> TOOL

tool_result
id: toolu_01XbKY6WsTnnLLAXz2WuRWF8
```
=== all icon-ish files in public and app ===
src/app/favicon.ico

=== layout.tsx metadata/icons ===
src/app/layout.tsx:7:export const metadata: Metadata = {

=== manifest referenced anywhere ===
src/app/farmer/dashboard/page.tsx
```

> TOOL

tool_use Read
id: toolu_01K5TzBzkfxbttxPneEWKXAP
```json
{
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/src/app/layout.tsx"
}
```

> TOOL

tool_result
id: toolu_01K5TzBzkfxbttxPneEWKXAP
```
1	import type { Metadata, Viewport } from "next";
2	import "./globals.css";
3	import { LanguageProvider } from "@/lib/LanguageContext";
4	import { ConsumerAuthProvider } from "@/lib/ConsumerAuthContext";
5	import SplashScreen from "@/components/SplashScreen";
6	
7	export const metadata: Metadata = {
8	  title: "Go Grameen — Your Family Farmer",
9	  description: "Buy natural harvests directly from farmers in Andhra Pradesh. No middlemen.",
10	};
11	
12	export const viewport: Viewport = {
13	  width: 'device-width',
14	  initialScale: 1,
15	  maximumScale: 1,
16	  userScalable: false,
17	};
18	
19	export default function RootLayout({
20	  children,
21	}: Readonly<{
22	  children: React.ReactNode;
23	}>) {
24	  return (
25	    <html lang="en" className="h-full">
26	      <body className="min-h-full bg-gray-50 antialiased">
27	        {/* Runs before first paint: if the splash already played this session,
28	            mark <html> so CSS hides the overlay instantly (no green flash on
29	            navigations). On the very first open it just records the flag and
30	            lets the overlay paint — which covers the page and kills the
31	            consumer-page flash. */}
32	        <script
33	          dangerouslySetInnerHTML={{
34	            __html: `try{if(sessionStorage.getItem('splash_shown')==='true'){document.documentElement.classList.add('splash-skip')}else{sessionStorage.setItem('splash_shown','true')}}catch(e){}`,
35	          }}
36	        />
37	        <SplashScreen />
38	        <LanguageProvider>
39	          <ConsumerAuthProvider>{children}</ConsumerAuthProvider>
40	        </LanguageProvider>
41	      </body>
42	    </html>
43	  );
44 […]

> AGENT

The app uses Next.js App Router's `src/app/favicon.ico` convention. I also noticed the farmer dashboard's notifications reference `/icon-192.png`. Let me check the tooling available to convert the image and see the full picture.

> TOOL

tool_use Bash
id: toolu_01BHq1prKko92qxxZJwigtqb
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\necho \"=== public dir contents ===\"\nls -la public/\necho \"=== does /icon-192.png exist (referenced by notifications)? ===\"\nls -la public/icon-192.png 2>&1\necho \"=== image tooling ===\"\nwhich convert magick 2>/dev/null; convert --version 2>/dev/null | head -1 || echo \"no imagemagick\"\nnode -e \"console.log('sharp?', require.resolve('sharp'))\" 2>/dev/null || echo \"no sharp in node_modules\"\necho \"=== both favicons ===\"\nls -la src/app/favicon.ico public/favicon.ico 2>&1",
  "description": "Check public dir, icon refs, and image tooling"
}
```

> TOOL

tool_result ERROR
id: toolu_01BHq1prKko92qxxZJwigtqb
```
Exit code 2
=== public dir contents ===
total 28
drwxr-xr-x  2 veerendra veerendra 4096 Jul  2 12:18 .
drwxr-xr-x 13 veerendra veerendra 4096 Jul  8 13:18 ..
-rw-r--r--  1 veerendra veerendra  391 Apr 16 10:13 file.svg
-rw-r--r--  1 veerendra veerendra 1035 Apr 16 10:13 globe.svg
-rw-r--r--  1 veerendra veerendra 1375 Apr 16 10:13 next.svg
-rw-r--r--  1 veerendra veerendra  128 Apr 16 10:13 vercel.svg
-rw-r--r--  1 veerendra veerendra  385 Apr 16 10:13 window.svg
=== does /icon-192.png exist (referenced by notifications)? ===
ls: cannot access 'public/icon-192.png': No such file or directory
=== image tooling ===
sharp? /home/<USER>/farmer/yourfamilyfarmer/node_modules/sharp/lib/index.js
=== both favicons ===
ls: cannot access 'public/favicon.ico': No such file or directory
-rw-r--r-- 1 veerendra veerendra 25931 Apr 16 10:13 src/app/favicon.ico
```

> AGENT

`sharp` is available. I'll generate a proper set of icons from the logo: the Next.js App Router `icon.png`/`apple-icon.png`, a real multi-size `favicon.ico`, and the `icon-192.png`/`icon-512.png` that the notification code references but which are currently missing (a latent 404). Let me write a generation script.

> TOOL

tool_use Write
id: toolu_01MdJrJR1ZcJU4g42NmKmjvo
```json
{
  "file_path": "/tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js",
  "content": "const sharp = require('sharp')\nconst fs = require('fs')\nconst path = require('path')\n\nconst SRC = process.argv[2]\nconst ROOT = process.argv[3]\n\n// Build an ICO that embeds PNG-encoded entries (supported by all modern\n// browsers). Header + one 16-byte directory entry per size, then the PNGs.\nfunction buildIco(pngs) {\n  const count = pngs.length\n  const header = Buffer.alloc(6)\n  header.writeUInt16LE(0, 0)      // reserved\n  header.writeUInt16LE(1, 2)      // type = icon\n  header.writeUInt16LE(count, 4)  // image count\n\n  const dir = Buffer.alloc(16 * count)\n  let offset = 6 + 16 * count\n  pngs.forEach((p, i) => {\n    const b = 16 * i\n    dir.writeUInt8(p.size >= 256 ? 0 : p.size, b + 0) // width (0 => 256)\n    dir.writeUInt8(p.size >= 256 ? 0 : p.size, b + 1) // height\n    dir.writeUInt8(0, b + 2)   // palette\n    dir.writeUInt8(0, b + 3)   // reserved\n    dir.writeUInt16LE(1, b + 4)  // color planes\n    dir.writeUInt16LE(32, b + 6) // bits per pixel\n    dir.writeUInt32LE(p.data.length, b + 8)  // size in bytes\n    dir.writeUInt32LE(offset, b + 12)        // offset\n    offset += p.data.length\n  })\n  return Buffer.concat([header, dir, ...pngs.map((p) => p.data)])\n}\n\nasync function png(size) {\n  return sharp(SRC).resize(size, size, { fit: 'cover' }).png().toBuffer()\n}\n\n;(async () => {\n  // App Router auto-icons (Next injects the <link> tags for these).\n  await […]

> TOOL

tool_result
id: toolu_01MdJrJR1ZcJU4g42NmKmjvo
```
File created successfully at: /tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01P4N1jrFXY4Qed493shqNUe
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nnode /tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js \\\n  /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png \\\n  /home/<USER>/farmer/yourfamilyfarmer\necho \"=== results ===\"\nls -la src/app/icon.png src/app/apple-icon.png src/app/favicon.ico public/icon-192.png public/icon-512.png\necho \"=== verify favicon.ico is valid ICO ===\"\nfile src/app/favicon.ico",
  "description": "Generate icons from logo"
}
```

> TOOL

tool_result
id: toolu_01P4N1jrFXY4Qed493shqNUe
```
node:internal/modules/cjs/loader:1210
  throw err;
  ^

Error: Cannot find module 'sharp'
Require stack:
- /tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js
    at Module._resolveFilename (node:internal/modules/cjs/loader:1207:15)
    at Module._load (node:internal/modules/cjs/loader:1038:27)
    at Module.require (node:internal/modules/cjs/loader:1289:19)
    at require (node:internal/modules/helpers:182:18)
    at Object.<anonymous> (/tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js:1:15)
    at Module._compile (node:internal/modules/cjs/loader:1521:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1623:10)
    at Module.load (node:internal/modules/cjs/loader:1266:32)
    at Module._load (node:internal/modules/cjs/loader:1091:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:164:12) {
  code: 'MODULE_NOT_FOUND',
  requireStack: [
    '/tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js'
  ]
}

Node.js v20.20.2
=== results ===
ls: cannot access 'src/app/icon.png': No such file or directory
ls: cannot access 'src/app/apple-icon.png': No such file or directory
ls: cannot access 'public/icon-192.png': No such file or directory
ls: cannot access 'public/icon-512.png': No such file or directory
-rw-r--r-- 1 veerendra veerendra 25931 Apr 16 10:13 src/app/favicon.ico
=== verify favicon.ico is valid ICO ===
src/app/favicon.ico: MS Windows icon resource - 4 icons, 16x16, 32 bits/pixel, 32x32, 32 bits/pixel
```

> AGENT

The script runs from the scratchpad, so it can't resolve `sharp` from the project's `node_modules`. Let me run it from the project directory instead.

> TOOL

tool_use Bash
id: toolu_01Pj3MhM8AQXrdM4TMjmsz2n
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\ncp /tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/gen-icons.js ./gen-icons.tmp.js\nnode ./gen-icons.tmp.js \\\n  /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/2.png \\\n  /home/<USER>/farmer/yourfamilyfarmer\nrm -f ./gen-icons.tmp.js\necho \"=== results ===\"\nls -la src/app/icon.png src/app/apple-icon.png src/app/favicon.ico public/icon-192.png public/icon-512.png\nfile src/app/favicon.ico src/app/icon.png",
  "description": "Run icon generation from project dir"
}
```

> TOOL

tool_result
id: toolu_01Pj3MhM8AQXrdM4TMjmsz2n
```
generated: src/app/icon.png, src/app/apple-icon.png, src/app/favicon.ico, public/icon-192.png, public/icon-512.png
=== results ===
-rw-r--r-- 1 veerendra veerendra  44421 Jul  9 15:39 public/icon-192.png
-rw-r--r-- 1 veerendra veerendra 281418 Jul  9 15:39 public/icon-512.png
-rw-r--r-- 1 veerendra veerendra  39660 Jul  9 15:39 src/app/apple-icon.png
-rw-r--r-- 1 veerendra veerendra   6390 Jul  9 15:39 src/app/favicon.ico
-rw-r--r-- 1 veerendra veerendra 281418 Jul  9 15:39 src/app/icon.png
src/app/favicon.ico: MS Windows icon resource - 3 icons, 16x16 with PNG image data, 16 x 16, 8-bit/color RGBA, non-interlaced, 32 bits/pixel, 32x32 with PNG image data, 32 x 32, 8-bit/color RGBA, non-interlaced, 32 bits/pixel
src/app/icon.png:    PNG image data, 512 x 512, 8-bit/color RGBA, non-interlaced
```

> AGENT

All icons generated. Let me visually verify the generated favicon and confirm the build picks them up.

> TOOL

tool_use Read
id: toolu_019iUM7hUmTjKt5vKQ25KHSV
```json
{
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/public/icon-192.png"
}
```

> TOOL

tool_result
id: toolu_019iUM7hUmTjKt5vKQ25KHSV
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/png"
  }
}
```

> AGENT

The logo rendered correctly. Now let me build to confirm Next.js picks up the App Router icons without errors.

> TOOL

tool_use Bash
id: toolu_01G7rEYModLCzTSzbSdPqp5t
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nnpm run build 2>&1 | grep -iE \"error|failed|Compiled successfully|/icon|favicon\" | head",
  "description": "Build to confirm icons compile"
}
```

> TOOL

tool_result
id: toolu_01G7rEYModLCzTSzbSdPqp5t
```
✓ Compiled successfully in 8.9s
├ ○ /icon.png
```

> AGENT

Build passes and Next.js registered `/icon.png` (it auto-injects the `<link rel="icon">` tags for `icon.png`, `apple-icon.png`, and `favicon.ico`). 

Let me stage, commit, and push (you authorized pushing to main earlier for this session; I'll continue that).

> TOOL

tool_use Bash
id: toolu_01WiBJK7gUGELv7ftShZCK4a
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\ngit add -A\ngit status --short\ngit commit -q -F - <<'EOF'\nfeat(branding): set Go Grameen logo as favicon + app/PWA icons\n\n- replace favicon.ico with the natural-farmer logo (16/32/48 multi-size ICO)\n- add App Router icon.png (512) + apple-icon.png (180) so Next injects the tags\n- add public/icon-192.png & icon-512.png — the farmer-dashboard notification\n  icon ('/icon-192.png') referenced these but they were missing (404 until now)\n\nCo-Authored-By: Claude Opus 4.8 <<REDACTED_EMAIL>>\nEOF\ngit push origin main 2>&1 | tail -4",
  "description": "Commit and push icon changes"
}
```

> TOOL

tool_result
id: toolu_01WiBJK7gUGELv7ftShZCK4a
```
A  public/icon-192.png
A  public/icon-512.png
A  src/app/apple-icon.png
M  src/app/favicon.ico
A  src/app/icon.png
[entire] Pushing entire/checkpoints/v1 to origin....... done
To github.com:singampalliveerendra/your_family_farmer.git
   683403f..f26b578  main -> main
```

> AGENT

Done — the logo is now the favicon and app icon set, committed and pushed.

## What was added
- **`src/app/favicon.ico`** — replaced with the logo (multi-size 16/32/48 ICO for browser tabs).
- **`src/app/icon.png`** (512×512) & **`src/app/apple-icon.png`** (180×180) — Next.js App Router auto-injects `<link rel="icon">` / apple-touch tags for these, so modern browsers and iOS home-screen use the high-res logo.
- **`public/icon-192.png`** & **`public/icon-512.png`** — these double as the PWA/notification icons. The farmer dashboard's notification code already pointed at `/icon-192.png`, but the file didn't exist (a silent 404) — now it resolves to your logo.

## Shipped
- Commit `f26b578`, pushed `683403f..f26b578 main -> main` → Vercel will auto-deploy.

Note: browsers cache favicons aggressively, so you may need a hard refresh (or a cache-busted tab) to see the new icon locally after the deploy lands.

> DEVELOPER

its showing but not visible need another logo [Image #3] use this

> AGENT

Good call — the previous logo was too fine-detailed to read at favicon size. This one has bolder shapes. Let me check its dimensions and background first so it frames well when squared.

> TOOL

tool_use Bash
id: toolu_01C3WvBjXfoa5vjKSHPLk6GF
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nfile /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/3.png\nnode -e \"const sharp=require('sharp');sharp('/home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/3.png').metadata().then(m=>console.log(JSON.stringify({width:m.width,height:m.height,hasAlpha:m.hasAlpha,channels:m.channels})))\"",
  "description": "Inspect new logo dimensions and alpha"
}
```

> TOOL

tool_result
id: toolu_01C3WvBjXfoa5vjKSHPLk6GF
```
/home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/3.png: PNG image data, 570 x 411, 8-bit/color RGBA, non-interlaced
{"width":570,"height":411,"hasAlpha":true,"channels":4}
```

> AGENT

It's landscape (570×411) with whitespace top/bottom, so I'll trim the whitespace and center it on a square white canvas — that keeps the whole logo visible and as large as possible at tab size.

> TOOL

tool_use Write
id: toolu_01ApXKj5nGNiwSKdQkxezjYZ
```json
{
  "file_path": "/home/<USER>/farmer/yourfamilyfarmer/gen-icons.tmp.js",
  "content": "const sharp = require('sharp')\nconst fs = require('fs')\nconst path = require('path')\n\nconst SRC = process.argv[2]\nconst ROOT = process.argv[3]\n\nfunction buildIco(pngs) {\n  const count = pngs.length\n  const header = Buffer.alloc(6)\n  header.writeUInt16LE(0, 0)\n  header.writeUInt16LE(1, 2)\n  header.writeUInt16LE(count, 4)\n  const dir = Buffer.alloc(16 * count)\n  let offset = 6 + 16 * count\n  pngs.forEach((p, i) => {\n    const b = 16 * i\n    dir.writeUInt8(p.size >= 256 ? 0 : p.size, b + 0)\n    dir.writeUInt8(p.size >= 256 ? 0 : p.size, b + 1)\n    dir.writeUInt8(0, b + 2)\n    dir.writeUInt8(0, b + 3)\n    dir.writeUInt16LE(1, b + 4)\n    dir.writeUInt16LE(32, b + 6)\n    dir.writeUInt32LE(p.data.length, b + 8)\n    dir.writeUInt32LE(offset, b + 12)\n    offset += p.data.length\n  })\n  return Buffer.concat([header, dir, ...pngs.map((p) => p.data)])\n}\n\n// Flatten onto white, trim surrounding white, then center on a square white\n// canvas with a little breathing room — keeps the whole (landscape) logo\n// visible and as large as possible at small favicon sizes.\nasync function squared() {\n  const trimmed = await sharp(SRC)\n    .flatten({ background: '#ffffff' })\n    .trim({ background: '#ffffff', threshold: 12 })\n    .toBuffer()\n  const meta = await sharp(trimmed).metadata()\n  const side = Math.max(meta.width, meta.height)\n  const pad = Math.round(side * 0.08)\n  const canvas = side + pad * 2\n  return sharp({\n    create: { […]

> TOOL

tool_result
id: toolu_01ApXKj5nGNiwSKdQkxezjYZ
```
File created successfully at: /home/<USER>/farmer/yourfamilyfarmer/gen-icons.tmp.js (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01JJHw4FaxMkTERVwRWn6kyB
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nnode ./gen-icons.tmp.js \\\n  /home/<USER>/.claude/image-cache/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/3.png \\\n  /home/<USER>/farmer/yourfamilyfarmer\nrm -f ./gen-icons.tmp.js\nfile src/app/favicon.ico\nls -la src/app/icon.png public/icon-192.png",
  "description": "Regenerate icons from new logo"
}
```

> TOOL

tool_result
id: toolu_01JJHw4FaxMkTERVwRWn6kyB
```
regenerated all icons from new logo
src/app/favicon.ico: MS Windows icon resource - 3 icons, 16x16 with PNG image data, 16 x 16, 8-bit/color RGBA, non-interlaced, 32 bits/pixel, 32x32 with PNG image data, 32 x 32, 8-bit/color RGBA, non-interlaced, 32 bits/pixel
-rw-r--r-- 1 veerendra veerendra  24100 Jul  9 15:43 public/icon-192.png
-rw-r--r-- 1 veerendra veerendra 147370 Jul  9 15:43 src/app/icon.png
```

> AGENT

Let me visually verify the new icon at small size (this is what matters for the tab).

> TOOL

tool_use Bash
id: toolu_01TgWCaaUt2oDfDJHcyQ5yQN
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nnode -e \"const sharp=require('sharp');sharp('src/app/icon.png').resize(48,48).png().toFile('/tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/fav48.png').then(()=>console.log('ok'))\"",
  "description": "Render 48px preview of favicon"
}
```

> TOOL

tool_result
id: toolu_01TgWCaaUt2oDfDJHcyQ5yQN
```
ok
```

> TOOL

tool_use Read
id: toolu_01Aex7sTP39sNY4MZ28NS48H
```json
{
  "file_path": "/tmp/claude-1000/-home-veerendra-farmer-yourfamilyfarmer/ddfe77aa-4aaf-4dba-bff9-1f01a3a7a0c0/scratchpad/fav48.png"
}
```

> TOOL

tool_result
id: toolu_01Aex7sTP39sNY4MZ28NS48H
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/png"
  }
}
```

> AGENT

At 48px the farmer, sun, and fields read clearly — much bolder than the previous detailed one. Let me build, commit, and push.

> TOOL

tool_use Bash
id: toolu_01UeiMioXAGxyZoREYdsrJXg
```json
{
  "command": "cd /home/<USER>/farmer/yourfamilyfarmer\nnpm run build 2>&1 | grep -iE \"error|failed|Compiled successfully\" | head\ngit add -A\ngit commit -q -F - <<'EOF'\nfeat(branding): swap favicon/app icons to bolder farmer-sun-fields logo\n\nPrevious logo was too fine-detailed to read at tab size. Regenerate the full\nicon set (favicon.ico 16/32/48, icon.png 512, apple-icon 180, PWA 192/512)\nfrom the higher-contrast logo, trimmed and centered on a white square.\n\nCo-Authored-By: Claude Opus 4.8 <<REDACTED_EMAIL>>\nEOF\ngit push origin main 2>&1 | tail -3",
  "description": "Build, commit and push new icons"
}
```

> TOOL

tool_result
id: toolu_01UeiMioXAGxyZoREYdsrJXg
```
✓ Compiled successfully in 11.2s
[entire] Pushing entire/checkpoints/v1 to origin....... done
To github.com:singampalliveerendra/your_family_farmer.git
   f26b578..b214698  main -> main
```

> AGENT

Done — swapped to the bolder logo and pushed.

## What changed
Regenerated the full icon set from the new higher-contrast logo (farmer + sun + fields), trimmed of whitespace and centered on a white square so it's readable at tab size:
- `src/app/favicon.ico` (16/32/48)
- `src/app/icon.png` (512) + `src/app/apple-icon.png` (180)
- `public/icon-192.png` + `public/icon-512.png` (PWA/notifications)

## Shipped
- Build passed, commit `b214698`, pushed `f26b578..b214698 main -> main` → Vercel auto-deploys.

Verified the 48px render — the farmer, sun, and green fields are clearly distinguishable now, unlike the previous fine-lined version.

One thing to note: browsers cache favicons hard. After the deploy lands, do a hard refresh (Ctrl+Shift+R) or open the site in a fresh tab — if it still looks stale, visit `/favicon.ico` directly once to force the update.