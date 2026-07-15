> DEVELOPER

jHey, bro. I just copy pasted new skill to the repository. Can you please check is it valid skill data structure or not really? Because I see rules directory. I'm not sure it is like cool.

> AGENT

Structure is valid. The skill is already loaded — it appears in the available skills list as `react-best-practices`.

Key files:
- `SKILL.md` — proper frontmatter (`name`, `description`, `license`, `metadata`) ✓
- `metadata.json` — supplementary metadata ✓
- `rules/` — individual rule files referenced from `SKILL.md` ✓
- `AGENTS.md` — compiled full guide ✓

The `rules/` directory is intentional. `SKILL.md` tells the agent to read individual files from `rules/` for detailed examples. This is a valid multi-file skill pattern.

> DEVELOPER

ok

> AGENT

👍

> DEVELOPER

vale

> AGENT

<br>

> DEVELOPER

nu idi nahuy

> AGENT

😄

> DEVELOPER

do you understand what does idid nuhuy mean>?

> AGENT

Yes. Russian profanity. "Go f*** yourself" roughly.

> DEVELOPER

it was joke bro

> AGENT

I know, no worries.

> DEVELOPER

using /react-best-practices and /frontend-design do code review for https://github.com/customink/pigment/pull/1094
context we are migrating existing component from the repo to the design library

> AGENT

Now let me read the core implementation files:

> AGENT

I've read through the full PR diff. Here's the review:

---

## Code Review: PR #1094 — TrendingProductsCarousel Migration

Context: new `@customink/pigment-extensions/reco` package, no existing consumers, risk is low. Review focuses on correctness, React patterns, and API design.

---

### 🔴 HIGH

**1. Wrong ARIA role on Popover (`Popover.tsx:2543`)**
```tsx
<span ref={panelRef} role="dialog" aria-hidden={!visible} ...>
```
`role="dialog"` implies a modal with focus trap and requires `aria-labelledby`/`aria-label`. A hover/focus-triggered pricing panel is a `role="tooltip"`. The trigger should have `aria-describedby={panelId}`. As-is, screen readers announce this incorrectly and it fails WCAG.

**2. Side effect during render breaks React Strict Mode (`decorator.tsx:35-36`)**
```tsx
const originalFetchRef = React.useRef(window.fetch);
window.fetch = async (...) => { ... }; // ← happens during render
```
In React Strict Mode (dev), components render twice. On second render, `originalFetchRef.current` is already the patched fetch, so cleanup restores the patched version. The mock leaks. This should be in a `useLayoutEffect` with the patching logic, using a flag to guard against double invocation.

**3. `ref` not forwarded in loading state (`ProductsCarouselWidget.tsx:3639`)**
```tsx
if (isLoading) return <LoadingSkeleton count={Math.floor(perView)} gap={spacing} />;
```
`ref` is never passed to `LoadingSkeleton`, so `ref.current` is `null` during loading. If a consumer passes a ref expecting to track the widget root (e.g. for an IntersectionObserver), it silently fails. Either forward the ref to `LoadingSkeleton` or wrap both branches in the same root div.

---

### 🟡 MEDIUM

**4. Inline lambdas in `.map()` (`ProductsCarouselWidget.tsx:3666–3670`)**
```tsx
// eslint-disable-next-line react/jsx-no-bind
onClick={() => onCardClicked?.(product, index)}
// eslint-disable-next-line react/jsx-no-bind
renderPriceDetails={renderPriceDetails ? () => renderPriceDetails(product) : undefined}
```
Two new function instances are created per product per render. The ESLint disables acknowledge this is known but leave it unfixed. With 10+ cards in the carousel, this is 20+ new allocations every render. Extract via `useCallback` or lift into a `ProductCard` wrapper component that takes `product` as prop and closes over it stably.

**5. `arrowPath` defined inside render (`Carousel.tsx:2147`)**
```tsx
const arrowPath = 'M8.29289 5.70711C7.90237...';
```
New string allocation on every render. Hoist to module level.

**6. `widgetRef` is an inner element, not the root (`ProductsCarouselWidget.tsx:3616–3646`)**
```tsx
const widgetRef = useRef<HTMLDivElement>(null); // inner div
// ...
<div ref={ref} className={rootClass} style={style}>   // outer — consumer's ref
  <div ref={widgetRef}>                               // inner — IntersectionObserver target
```
The `onWidgetViewed` effect observes `widgetRef` (inner div, excludes the margin from `.root`). The `IntersectionObserver` threshold `0.1` may fire before the card row is visible due to the `margin: 2.5rem 0` on the outer div. Attach the observer to `ref` (outer) or the outer div directly.

**7. Hardcoded `width: 332px` (`ProductCardPriceDetailsContent.module.css:2727`)**
```css
.root {
  width: 332px;
}
```
Magic pixel value in a design library component. Should be a CSS custom property (`--price-details-popover-width`) or at minimum a comment citing the Figma source (`/* Figma: Pricing Popover / Width */`). The value 332 is currently untracked.

---

### 🔵 LOW

**8. `imageSrcSet` never populated by mapper (`mapper.ts:4214`)**
`TrendingProduct.imageSrcSet` exists on the type but `ApiRecoProduct` has no corresponding field, so it's always `undefined` after mapping. Either remove the field from the type or add `image_src_set?: string` to `ApiRecoProduct`. Storybook uses `imageSrcSet` from `MOCK_PRODUCTS` populated manually, masking this gap.

**9. Duplicate `@keyframes shimmer` definitions**
`LoadingSkeleton.module.css:2193` and `ProductCardPriceDetailsContent.module.css:2717` both define `@keyframes shimmer` with slightly different directions (`-200% → 200%` vs `200% → -200%`). CSS Modules scope the names, so they don't conflict, but if the animation direction is intentionally different, it should be documented. If unintentional, extract to a shared `shimmer.module.css`.

**10. PR title typo**
"Reco 730 trendng products migration" → missing `i` in "trending".

---

### ✅ What's solid

- Clean Atoms/Molecules/Widget separation with correct public API boundary (atoms not exported)
- `forwardRef` + `displayName` on every component — good
- Render prop pattern for `renderFavoriteButton` / `renderPriceDetails` decouples catalog-specific state correctly
- Lazy mount pattern in `Popover` (`mounted` state + `createPortal`) — correct
- `useBreakpoint` correctly computes from `window.innerWidth` in the handler, not from the MQ result — avoids the skip-breakpoint edge case
- `hasFiredViewEvent` ref prevents double-firing `onWidgetViewed` — correct
- Test coverage is thorough and uses real mock data

> DEVELOPER

using /react-best-practices and /frontend-design do code review for https://github.com/customink/next-frontend/pull/807/
context we are migrating existing component from the repo to the other repo

> AGENT

Now I have the full diff. Here's the review:

---

## Code Review: PR #807 — RECO-740 Related Products Restoration

Three areas of change: keen-slider migration, tab indicator, and server caching. Overall clean migration, a few issues worth fixing.

---

### 🔴 HIGH

**1. `showArrows` logic regression (`carousel-cards-view.tsx:531`)**
```tsx
const showArrows = loaded && children.length > 1;
```
Old logic was `total > SLIDES_PER_VIEW` (> 4). New logic shows arrows for any carousel with ≥ 2 items. On desktop with `perView: 4`, a 2-item or 3-item carousel shows arrows but clicking them produces no visible change (all items already fit). This is a confusing UX regression. Should be gated by breakpoint-aware perView. Simplest approach:
```tsx
const showArrows = loaded && children.length > 4; // conservative: matches desktop perView
```
Or make it responsive by reading the slider's current `options.slides.perView`.

**2. `loop: true` with few items (`carousel-cards-view.tsx:436`)**
keen-slider with `loop: true` and fewer slides than `perView` produces visual glitches (slides stretch or duplicate). At `perView: 4` on desktop with 2 items, this is broken. Should disable loop when `children.length ≤ perView`:
```tsx
loop: children.length > 4,
```
Related to issue #1 — fixing both together with a responsive perView check is ideal.

---

### 🟡 MEDIUM

**3. `initialDataUpdatedAt: Date.now()` on every render (`use-related-styles.ts:195`, same pattern in 3 hooks)**
```tsx
initialDataUpdatedAt: options.initialData ? Date.now() : undefined,
```
This is called during render, so `Date.now()` is captured at render time — which is correct. But if the parent component re-renders after mount (e.g. color changes), `options.initialData` will still be set from the server prefetch, `Date.now()` will be the time of the re-render, and TQ will think the server data is fresh again, suppressing the color-change refetch for 5 minutes.

Color changes should trigger fresh fetches. The fix: pass `initialDataUpdatedAt` as a stable value (e.g. from server response or a ref set on first render only), or clear `initialData` after first hydration.

**4. `ResizeObserver` recreated on every `activeTab`/`tabs` change (`tabs.tsx:706`)**
```tsx
useEffect(() => {
  ...
  const observer = new ResizeObserver(measure);
  observer.observe(tabList);
  return () => observer.disconnect();
}, [activeTab, tabs]);
```
The `ResizeObserver` is destroyed and recreated every time the active tab changes. The observer only needs to be created once (watching the container). Measure should run on `activeTab` change separately:
```tsx
// One effect for the observer (runs once)
useEffect(() => {
  const observer = new ResizeObserver(measure);
  observer.observe(tabList);
  return () => observer.disconnect();
}, []); // eslint-disable-line

// Separate effect to re-measure on tab change
useEffect(() => { measure(); }, [activeTab]);
```
`measure` should be extracted via `useCallback`.

---

### 🔵 LOW

**5. `cacheTag` inconsistency between `getRelatedStyles` and `getRecommendedStyles` (`server.ts:799` vs `821`)**
```tsx
cacheTag(`related-styles-${styleId}-${colorId}`);   // includes colorId
cacheTag(`recommended-styles-${styleId}`);           // omits colorId
```
Probably intentional (recommendations are style-level, not color-level), but it's worth a comment to avoid someone "fixing" it later.

**6. `RelatedProductsClient` wrapper may be unnecessary (`related-products-client.tsx`)**
```tsx
export default function RelatedProductsClient({ initialData }): React.JSX.Element {
  return <RelatedProducts initialData={initialData} />;
}
```
`RelatedProductsServer` could import and use `dynamic(() => import("./related-products"), { ssr: false })` directly without the thin wrapper file. The wrapper exists to hold `"use client"` boundary — but `dynamic` with `ssr: false` already prevents server execution. If this mirrors the `CustomerPhotosServer` pattern intentionally, fine — just noting it adds an indirection layer that could be collapsed.

**7. `carousel-cards-view.tsx` - `key={i}` for slides**
```tsx
{children.map((child, i) => (
  <div key={i} className="keen-slider__slide">
```
Index keys are fine here since children are positional and don't reorder. Not a bug, just noting it's intentional.

---

### ✅ What's solid

- `Promise.all` for parallel server fetching (`server-parallel-fetching` ✓)
- `"use cache: remote"` + `cacheLife("hours")` is the right Next.js 15 pattern
- `isFetched → isSuccess` change with explanatory comment is correct and well-documented
- `Suspense` fallback to `<Loader />` during server async operations is correct
- Removing clone-based infinite loop and all the `requestAnimationFrame` hack — clean simplification
- `memo` on `Tabs` still intact
- Removing `Box` from MUI and replacing with plain `div` is correct for the extensions pattern
- `RelatedProducts` fallback: `{relatedProductsSlot || <RelatedProducts />}` is clean

> DEVELOPER

can you drop a comment in the PR plese? from my name with you as co-authored?

> AGENT

What's your GitHub username?

> DEVELOPER

4thwithme

> AGENT

Done. Comment posted: https://github.com/customink/next-frontend/pull/807#issuecomment-4117954289

> DEVELOPER

claude select random person from the list

> AGENT

**Kostantyn Orlov**
