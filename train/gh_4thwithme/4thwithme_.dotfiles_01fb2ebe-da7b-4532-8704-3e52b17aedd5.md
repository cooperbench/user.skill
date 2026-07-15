---
session_id: "4thwithme/.dotfiles|01fb2ebe-da7b-4532-8704-3e52b17aedd5"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-26T08:12:05.873Z"
n_turns: 34
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

read task https://customink.atlassian.net/browse/RECO-738

> AGENT

**RECO-738** — D&A: Product Position (Index) Tracking for Recommendation & Promotion Events

**Status:** To Do | **Assignee:** Andrii Popenko | **Target:** End of April 2026

**Goal:** Capture product position (`index`) in analytics events for recommendation/promotion widgets on PLPs to analyze placement effectiveness.

**Four events to update:**

| Event | Payload |
|---|---|
| `recommendation_view` | Full items array (all products + positions) |
| `view_promotion` | Full items array (all products + positions) |
| `recommendation_click` | Single item (clicked product + position) |
| `select_promotion` | Single item (selected product + position) |

Each item: `{ index: <1-based>, item_id: <id> }` plus metadata (`item_list_id`, `item_list_name`, page type, user state, session info).

**Key constraints:**
- Index is 1-based, reflects rendered order
- Index must NOT reset on pagination/lazy-load (continues sequentially)
- No events fire if product list fails to load
- `data-testid` attributes on all new frontend components

> DEVELOPER

our trending products widget is @app/javascript/features/TrendingProducts/TrendingCarousel.jsx and @app/javascript/features/TrendingProducts/TrendingBanner.jsx we need to add/edit events for both of them

> AGENT

Let me explore the existing event utilities and understand the current implementation.

> AGENT

Now let me read the actual event file to see exact current code.

> AGENT

Now let me check where TrendingBanner's events come from — it uses `fireGARenderedEvent` and `fireGAClickedEvent` as props.

> AGENT

Now I have the full picture. Let me implement the changes.

**Plan:**

1. **`trendingPromoProducts.ts`** — Update both events to accept `items` (with `index` + `item_id`) and include ecommerce payload
2. **`marchPromoBanner.ts`** — Update both events to accept `items` with `index` + `item_id`
3. **`TrendingCarousel.jsx`** — Pass products with index to view event, pass clicked product with index to click event
4. **`TrendingBanner.jsx`** — Same pattern, pass index-enriched items to the GA event callbacks
5. **`MarchPromoBanner.tsx`** — Update to pass through the new signature

Starting with the metrics files:

> AGENT

Now update **TrendingCarousel.jsx** — view event needs all products with index, click event needs clicked product with index:

> AGENT

Now update the click handler — need to pass index. The `products.map` creates cards, so I need to pass the index through:

> AGENT

Now update **TrendingBanner.jsx** — the events come in as props (`fireGARenderedEvent`, `fireGAClickedEvent`). I need to pass items to the rendered event and product+index to the clicked event:

> AGENT

Now update the click handler in TrendingBanner — need to pass index:

> AGENT

Now let me check if there are any tests for these files that need updating.

> AGENT

No existing tests. Let me verify the changes compile correctly:

> AGENT

Running lint and format on the changed files per CLAUDE.md instructions (yarn, not npm):

> AGENT

0 errors, all warnings are pre-existing. All changed files unchanged by prettier (already formatted).

Here's a summary of all changes:

### `utils/metrics/trendingPromoProducts.ts`
- **`firePromoTrendingRecommendationViewEvent`** — now accepts `items` array and `categoryId`, pushes `ecommerce` payload with `item_list_id`, `item_list_name`, and full items array (`{index, item_id}`)
- **`firePromoTrendingRecommendationClickEvent`** — now accepts `{product, index, categoryId, categoryName}` object, pushes `ecommerce` payload with single-item array
- Both events now clear ecommerce layer first (`{ecommerce: null}`)

### `utils/metrics/marchPromoBanner.ts`
- **`fireMarchPromoRenderedGA4Event`** — now accepts `items: EcommerceItem[]` and includes them in the `view_promotion` ecommerce payload
- **`fireMarchPromoInteractionGA4Event`** — now accepts `index` param, adds `index` to the promotion item in `select_promotion`
- Both events now clear ecommerce layer first

### `TrendingCarousel.jsx`
- View event: builds 1-based `items` array from `products` and passes `categoryId` + `categoryName`
- Click event: passes `{product, index: productIndex + 1, categoryId, categoryName}` object

### `TrendingBanner.jsx`
- View event (`fireGARenderedEvent`): builds 1-based `items` array from `products` and passes it
- Click event (`fireGAClickedEvent`): passes `(product, productIndex + 1)` — the 1-based index

> DEVELOPER

can you check do we have tests and linter?

> AGENT

No tests exist for these files. Lint passes — 0 errors, 507 warnings (all pre-existing).

> DEVELOPER

generate me ningfull pr description..responce give me in md format ### Stakeholder Overview _[(learn more)](https://app.getguru.com/card/TGyLkrnc/Pull-Review-Stakeholder-Overview)_<!--Provide a concise summary of the motivation and the driving force behind this change, in a way that anyone without context can understand.-->### Risk Estimate _[(learn more)](https://app.getguru.com/card/iMnRRRjT/Pull-Request-Risk-Estimate)_<!-- Optionally add a description of the risk, and how the change will be deployed. --><!-- remove any that do not apply -->- ⚠️ Big/complex change- ⚠️ Big splash zone- ⚠️ High stakes if errors occur- ⚠️ Low confidence- ⚠️ Not hidden by feature flag- ✅ Negligible risk!### Changes<!--Please describe your code changes in detail for reviewers. Explain the technical solution you have provided and how it addresses the issue at hand.-->##### Updated Dependencies - None<!--Please include any notes that might be helpful for a reviewer to check the dependency changes you might have introduced.  - gem version update  - new gem introduced  - data model update-->### Project Link<!-- Fill in the ticket information with the details of your feature --><!-- [Monday issue](https://customink.monday.com/boards/12345/pulses/12345) --><!-- [Project pitch](https://docs.google.com/document/d/1X7qdItdxoxC6p0MertCjfyzlKw_T2M79yQknTlPQOF4) -->### Screenshots<!-- Communicate the visual story of the change that is being made. -->### Notes_Recommended reading: [Code Review guide](https://github.com/customink/guides/blob/master/operations/code-review/README.md)_<!--Please include any notes that might be helpful for a reviewer to keep in mind while reading the changes.-->### Optional Tasks<!--Common, optional tasks are included here in case you forgot something important.-->- [ ] Include 🎩 Instructions- [ ] Update the readme (README.md)- [ ] Update the API or architecture docs (e.g. docs/api.md)##### Library-Specific- [ ] Increment the changelog (CHANGELOG.md)- [ ] Increment the version number (lib/version.rb)- [ ] [Release & Tag][release] the version above in Github[release]: https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository##### Performance- Are there any new queries in your change set that might require new indexes?- Do any new queries require time-boxing to avoid table-scans when the data grows?##### Data & Analytics Dependencies- For customer-facing applications, are there any GA tagging changes that are needed or created by this change? If so, have those been discussed with D&A?- Has Data Engineering been notified of any schema changes?### What GIF Best Describes This Pull Request?<!--![](https://i.giphy.com/media/WNuF3KK9NaQ8w/source.gif)-->

> AGENT

```markdown
### Stakeholder Overview _[(learn more)](https://app.getguru.com/card/TGyLkrnc/Pull-Review-Stakeholder-Overview)_

Adds product position (`index`) and `item_id` tracking to recommendation and promotion analytics events fired by the Trending Products widgets (TrendingCarousel and TrendingBanner). This enables the D&A and Recommendations teams to analyze how product placement within these widgets influences engagement and conversion — e.g., do products in positions 1–5 convert better than those in position 12?

### Risk Estimate _[(learn more)](https://app.getguru.com/card/iMnRRRjT/Pull-Request-Risk-Estimate)_

- ✅ Negligible risk!

Analytics-only change. No UI changes, no feature flag required. Existing event names are preserved — payloads are enriched with additional `ecommerce` data. Worst case on failure: events fire without position data (current behavior).

### Changes

**`utils/metrics/trendingPromoProducts.ts`**
- `firePromoTrendingRecommendationViewEvent` — now accepts `items` array (`{index, item_id}[]`) and `categoryId`; pushes `ecommerce` payload with `item_list_id`, `item_list_name`, and full items list
- `firePromoTrendingRecommendationClickEvent` — now accepts `{product, index, categoryId, categoryName}`; pushes `ecommerce` payload with single-item array
- Both events now clear the ecommerce layer first (`{ecommerce: null}`) per GA4 best practices

**`utils/metrics/marchPromoBanner.ts`**
- `fireMarchPromoRenderedGA4Event` — now accepts `items: EcommerceItem[]` and includes them in `view_promotion` ecommerce payload
- `fireMarchPromoInteractionGA4Event` — now accepts `index` param; adds `index` to the promotion item in `select_promotion`
- Both events now clear the ecommerce layer first

**`features/TrendingProducts/TrendingCarousel.jsx`**
- Builds 1-based `items` array from `products` and passes to view event with `categoryId`/`categoryName`
- Passes `{product, index, categoryId, categoryName}` to click event

**`features/TrendingProducts/TrendingBanner.jsx`**
- Builds 1-based `mappedItems` array and passes to `fireGARenderedEvent`
- Passes `(product, productIndex + 1)` to `fireGAClickedEvent`

##### Updated Dependencies
- None

### Project Link

[RECO-738](https://customink.atlassian.net/browse/RECO-738) — D&A: Product Position (Index) Tracking for Recommendation & Promotion Events

### Screenshots

N/A — analytics-only change, no visual modifications.

### Notes

_Recommended reading: [Code Review guide](https://github.com/customink/guides/blob/master/operations/code-review/README.md)_

- Index values are **1-based** per the ticket requirements
- Payload structure follows the existing `view_item_list` pattern in `productsAnalytics.js`
- No existing tests for these files; no tests were broken

### Optional Tasks

- [ ] Include 🎥 Instructions
- [ ] Update the readme (README.md)
- [ ] Update the API or architecture docs (e.g. docs/api.md)

##### Library-Specific
- [ ] Increment the changelog (CHANGELOG.md)
- [ ] Increment the version number (lib/version.rb)
- [ ] [Release & Tag][release] the version above in Github

[release]: https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository

##### Performance
- No new queries introduced.

##### Data & Analytics Dependencies
- **GA tagging changes**: Yes — four events enriched with `ecommerce.items` containing `index` and `item_id`. D&A team should validate event schema in Amplitude/GA.
- No schema changes for Data Engineering.

### What GIF Best Describes This Pull Request?

![](https://media.giphy.com/media/3o7btNa0RUYa5E7iiQ/giphy.gif)
```

> DEVELOPER

Run # Valid types per doc/commit-guidelines.md and doc/agents/commit-conventions.mdPR title: RECO-738: improve ga4 eventsaPattern:  ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\[[A-Z]+-[0-9]+\])?((\([a-z0-9_-]+\))\!?|\!(\([a-z0-9_-]+\))|\!)?: [a-z].{0,71}$ERROR: PR title does not follow semantic commit conventions.  - Title does not match the expected format.Expected format: type[JIRA-ID](scope): description  type:        required  — feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert  [JIRA-ID]:   optional  — e.g. [PP-123]  (scope):     optional  — lowercase, e.g. (plp)  description: required  — 1-72 characters, starts lowercase, no trailing periodExamples:  feat: add quick view modal to PLP  feat[PP-123]: add product comparison feature  fix[BUG-456](api): resolve null pointer exception  refactor!: restructure database schemaSee doc/commit-guidelines.md for full details.

> AGENT

```
feat[RECO-738](analytics): add product position tracking to recommendation and promotion events
```

> DEVELOPER

Unmemoized mappedItems causes infinite useEffect re-runsMedium SeveritymappedItems is computed via products.map(...) inline on every render, producing a new array reference each time. Including it in the useEffect dependency array at line 201 causes the effect to re-run on every render, tearing down and recreating the IntersectionObserver unnecessarily. The hasFiredViewEvent ref guard prevents duplicate event firing, but the constant observer churn is wasteful and could theoretically prevent the observer callback from ever firing under rapid re-renders. Wrapping mappedItems in useMemo keyed on products would restore the previously-stable dependency behavior.

> AGENT

Valid issue. Also need to check TrendingCarousel imports for `useMemo`.

> AGENT

Now same fix for TrendingBanner — it uses `useIntersectionObserverOnce` so the infinite loop risk is lower, but still wasteful to recompute on every render:

> AGENT

Done. Both files now wrap `mappedItems` in `useMemo` keyed on `products`, preventing unnecessary IntersectionObserver churn in TrendingCarousel and redundant recomputation in TrendingBanner.

> DEVELOPER

app/javascript/features/TrendingProducts/TrendingBanner.jsxComment on lines +219 to +223      products.map((product, idx) => ({        index: idx + 1,        item_id: product.style_id      })),    [products]@akulisekakuliseknowLooks like this is the same function used below - would you mind extracting it to an util file somewhere?

> AGENT

Good call. Let me find where both usages are and extract.

> AGENT

Two usages confirmed. Let me check if `trendingPromoProducts.ts` is the right home for this utility since it already holds the event types.

> AGENT

The `EcommerceItem` type and the mapping logic both belong here. Adding the utility to `trendingPromoProducts.ts` and updating both components:

> AGENT

Now update TrendingCarousel:

> AGENT

Now update TrendingBanner:

> AGENT

Done. Extracted `mapProductsToEcommerceItems` to `utils/metrics/trendingPromoProducts.ts` and both components now import and use it.

> DEVELOPER

check linters again

> AGENT

Clean. 0 errors, 507 warnings (all pre-existing). Prettier made no changes.
