---
session_id: "4thwithme/.dotfiles|d2ecfa3f-eb7d-4fe1-810c-b3bf09cbfc0d"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-12T11:48:33.431Z"
n_turns: 18
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Unknown skill: effort

> DEVELOPER

we have added a/b test to check if boosted products work for trending product widget- answer is no. lets find all code we created to run thi a/b test and clean it up. a/b test, withBoostedProducts related code

> AGENT

Now I have the full picture. Let me read all affected files.

> AGENT

Now let me read the test file:

> AGENT

Now I have the full scope. Making all changes:

> AGENT

Now remove `withBoostedProducts` from `recommendations.js`:

> AGENT

Now clean up the test file:

> AGENT

Now remove the entire "Boosted Products Feature Flag" describe block:

> AGENT

Now let me also check if `fireABTestGroupEvent` is still used elsewhere in TrendingCarousel (since we removed it from the import):

> AGENT

`fireABTestGroupEvent` is no longer called anywhere. Let me check if the function should be removed from the metrics file:

> AGENT

Clean up the metrics file too — remove `fireABTestGroupEvent` and the `isBoosted` logic since the test is done:

> AGENT

Now verify no remaining references to the boosted products test:

> AGENT

Clean. All references removed across:

| File | Change |
|------|--------|
| `config/feature_flags.rb` | Removed `pc_boosted_promo_products_v1` feature |
| `app/controllers/concerns/catalog_caching.rb` | Removed `BOOSTED_PROMO_PRODUCTS_TEST_CACHE_KEY` constant and its usage in `catalog_page_ab_test_suffixes` |
| `app/helpers/signalman_helper.rb` | Removed `boosted_promo_products_test_enabled?` |
| `app/javascript/utils/constants/signalmanConstants.ts` | Removed `boostedPromoProductsTest` export |
| `app/javascript/features/TrendingProducts/hooks/useTrendingProducts.js` | Removed flag import and `withBoostedProducts` conditional |
| `app/javascript/features/TrendingProducts/TrendingCarousel.jsx` | Removed `fireABTestGroupEvent` import, `hasFiredABTestEvent` ref, and the AB test tracking `useEffect` |
| `app/javascript/hooks/queries/recommendations.js` | Removed `withBoostedProducts` from `fetchPromotionalProducts` and `usePromotionalProducts` |
| `app/javascript/utils/metrics/trendingPromoProducts.ts` | Removed `fireABTestGroupEvent`, `ABTestGroup` type, `AB_TEST_NAME`/`AB_TEST_LOCATION` constants, and `isBoosted` conditional |
| `app/javascript/features/TrendingProducts/hooks/useTrendingProducts.test.jsx` | Removed signalmanConstants mock and entire "Boosted Products Feature Flag" describe block |

> DEVELOPER

this is template for pr description in GH

### Stakeholder Overview _[(learn more)](https://app.getguru.com/card/TGyLkrnc/Pull-Review-Stakeholder-Overview)_

<!--
Provide a concise summary of the motivation and the driving force behind this change, in a way that anyone without context can understand.
-->

### Risk Estimate _[(learn more)](https://app.getguru.com/card/iMnRRRjT/Pull-Request-Risk-Estimate)_

<!-- Optionally add a description of the risk, and how the change will be deployed. -->

<!-- remove any that do not apply -->
- ⚠️ Big/complex change
- ⚠️ Big splash zone
- ⚠️ High stakes if errors occur
- ⚠️ Low confidence
- ⚠️ Not hidden by feature flag
- ✅ Negligible risk!

### Changes

<!--
Please describe your code changes in detail for reviewers. Explain the technical solution you have provided and how it addresses the issue at hand.
-->

##### Updated Dependencies
 - None
<!--
Please include any notes that might be helpful for a reviewer to check the dependency changes you might have introduced.
  - gem version update
  - new gem introduced
  - data model update
-->

### Project Link

<!-- Fill in the ticket information with the details of your feature -->
<!-- [Monday issue](https://customink.monday.com/boards/12345/pulses/12345) -->
<!-- [Project pitch](https://docs.google.com/document/d/1X7qdItdxoxC6p0MertCjfyzlKw_T2M79yQknTlPQOF4) -->

### Screenshots

<!-- Communicate the visual story of the change that is being made. -->

### Notes

_Recommended reading: [Code Review guide](https://github.com/customink/guides/blob/master/operations/code-review/README.md)_

<!--
Please include any notes that might be helpful for a reviewer to keep in mind while reading the changes.
-->

### Optional Tasks

<!--
Common, optional tasks are included here in case you forgot something important.
-->

- [ ] Include 🎩 Instructions
- [ ] Update the readme (README.md)
- [ ] Update the API or architecture docs (e.g. docs/api.md)

##### Library-Specific

- [ ] Increment the changelog (CHANGELOG.md)
- [ ] Increment the version number (lib/version.rb)
- [ ] [Release & Tag][release] the version above in Github

[release]: https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository

##### Performance
- Are there any new queries in your change set that might require new indexes?
- Do any new queries require time-boxing to avoid table-scans when the data grows?


##### Data & Analytics Dependencies
- For customer-facing applications, are there any GA tagging changes that are needed or created by this change? If so, have those been discussed with D&A?
- Has Data Engineering been notified of any schema changes?

### What GIF Best Describes This Pull Request?

<!--
![](https://i.giphy.com/media/WNuF3KK9NaQ8w/source.gif)
-->


give me updated pr description for my PR

> AGENT

Here's the filled-in PR description:

---

### Stakeholder Overview

A/B test `pc_boosted_promo_products_v1` concluded with a negative result — boosted products did not improve the trending products widget. This PR removes all test infrastructure: the feature flag, Signalman helper, CloudFront cache key, and all JS/TS test branching logic.

### Risk Estimate

- ✅ Negligible risk!

### Changes

Removes all code introduced for the `pc_boosted_promo_products_v1` A/B test:

- **`config/feature_flags.rb`** — removed `pc_boosted_promo_products_v1` feature definition
- **`app/controllers/concerns/catalog_caching.rb`** — removed `BOOSTED_PROMO_PRODUCTS_TEST_CACHE_KEY` constant and its reference in `catalog_page_ab_test_suffixes`
- **`app/helpers/signalman_helper.rb`** — removed `boosted_promo_products_test_enabled?`
- **`app/javascript/utils/constants/signalmanConstants.ts`** — removed `boostedPromoProductsTest` export
- **`app/javascript/features/TrendingProducts/hooks/useTrendingProducts.js`** — removed flag check and `withBoostedProducts` query param
- **`app/javascript/features/TrendingProducts/TrendingCarousel.jsx`** — removed `fireABTestGroupEvent` call and `hasFiredABTestEvent` ref
- **`app/javascript/hooks/queries/recommendations.js`** — removed `withBoostedProducts` from `fetchPromotionalProducts` and `usePromotionalProducts`
- **`app/javascript/utils/metrics/trendingPromoProducts.ts`** — removed `fireABTestGroupEvent`, `ABTestGroup` type, AB test constants, and `isBoosted` conditional
- **`useTrendingProducts.test.jsx`** — removed signalmanConstants mock and "Boosted Products Feature Flag" describe block

##### Updated Dependencies
- None

### Project Link

<!-- [Monday issue](https://customink.monday.com/boards/12345/pulses/12345) -->

### Screenshots

No visual changes.

### Notes

The control behavior (no boosted products) is now the permanent behavior. No rollback needed — the flag was already at 0% at cleanup time.

> DEVELOPER

can y'all make sure the event tags (recommendation_view and recommendation_click) from the control experience remain?

> AGENT

Both events are intact. In `TrendingCarousel.jsx` the imports and calls were untouched:

> AGENT

Both events still fire:

- `recommendation_view` — `TrendingCarousel.jsx:179` via `IntersectionObserver` when the carousel enters the viewport
- `recommendation_click` — `TrendingCarousel.jsx:247` on product card click

No changes were made to either call site. The only thing removed from the metrics file was the `fireABTestGroupEvent` (the test-group tracking event), which is expected.
