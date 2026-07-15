> DEVELOPER

OK bro we have list of small tasks you need to fix them all use this session as orchestrator, and spawn sub-session for each task.
Do it 1 by 1. TAsk by task.
use /fix-eslint-workflow skill for it... you need to run eslint checks only for the file described in the each task and fix warnings.
1 task -> then check elsint warnings in the file from the task -> fix them -> fix calls to the fixed functions in other files if needed -> commit changes with proper message -> push to GH -> create PR with proper description. Then move to the next task. Do it for all tasks in the list. Here is the list of tasks:
  https://customink.atlassian.net/browse/RECO-678                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-679                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-680
  https://customink.atlassian.net/browse/RECO-681 
  https://customink.atlassian.net/browse/RECO-682                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-683                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-684                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-685

> AGENT

Got all tasks. Summary:

| Task | File | Violations |
|------|------|------------|
| RECO-678 | `src/scripts/load-testing/artillery-data-generator.ts` | 6x require-object-params |
| RECO-679 | `src/scripts/mms-to-algolia-update.script.ts` | 2x require-object-params |
| RECO-680 | `src/scripts/product-parity-report.script.ts` | 3x require-object-params |
| RECO-681 | `src/unit-tests/decorators/log-execution.decorator.unit-spec.ts` | 1x no-unnecessary-condition |
| RECO-682 | `src/utils/array.util.ts` | 1x require-object-params |
| RECO-683 | `src/utils/check-internal-access.util.ts` | 1x require-object-params |
| RECO-684 | `src/utils/color-match.util.ts` | 4x require-object-params |
| RECO-685 | `src/utils/concurrency-pool.util.ts` | 2x require-object-params + 1x no-unnecessary-condition |

Starting RECO-678 now (already on that branch).

> AGENT

RECO-678 done. PR: https://github.com/customink/recommendations-service/pull/510

Now RECO-679:

> AGENT

Type-check clean — diagnostics were stale. Moving to RECO-680.

> AGENT

The agent missed call site updates again. Fixing directly.

> AGENT

No type errors. Diagnostics are stale (editor cache). Moving to RECO-681.

> AGENT

RECO-681 done. PR: https://github.com/customink/recommendations-service/pull/514

Now RECO-682:

> AGENT

RECO-682 — already fixed in prior PR. Moving to RECO-683:

> AGENT

RECO-683 — already fixed. Skipping PR. Moving to RECO-684:

> AGENT

Stale diagnostics again — type-check is clean. Moving to RECO-685 (last task):

> AGENT

All 8 tasks done. Summary:

| Task | File | PR |
|------|------|----|
| RECO-678 | `artillery-data-generator.ts` | [#510](https://github.com/customink/recommendations-service/pull/510) |
| RECO-679 | `mms-to-algolia-update.script.ts` | [#512](https://github.com/customink/recommendations-service/pull/512) |
| RECO-680 | `product-parity-report.script.ts` | [#513](https://github.com/customink/recommendations-service/pull/513) |
| RECO-681 | `log-execution.decorator.unit-spec.ts` | [#514](https://github.com/customink/recommendations-service/pull/514) |
| RECO-682 | `array.util.ts` | [#515](https://github.com/customink/recommendations-service/pull/515) — already fixed |
| RECO-683 | `check-internal-access.util.ts` | skipped — already fixed |
| RECO-684 | `color-match-worker.service.ts` | [#516](https://github.com/customink/recommendations-service/pull/516) |
| RECO-685 | `concurrency-pool.util.ts` | [#517](https://github.com/customink/recommendations-service/pull/517) |

> AGENT

These are background commit tasks from the subagents — all completed with exit code 0. No action needed.
