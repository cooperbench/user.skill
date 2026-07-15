> DEVELOPER

why i see this shet??

  ~/Documents/repo/recommendations-service   main *18 !4 ❯ npm run test:coverage                                                                                                                         17:26:22

> recommendations-service@0.0.1 test:coverage
> npm run code-quality-check && npm run test:unit:coverage && npm run test:e2e:coverage


> recommendations-service@0.0.1 code-quality-check
> npm run lint && npm run format && npm run type-check


> recommendations-service@0.0.1 lint
> eslint "{src,apps,libs,test}/**/*.ts"


/Users/4thwithme/Documents/repo/recommendations-service/src/modules/cli/commands/forecast-trending-products.command.ts
  332:5  error  Expected the Promise rejection reason to be an Error  @typescript-eslint/prefer-promise-reject-errors

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/category-correlations/models/category-correlation.model.ts
  64:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/condensed-features/models/condensed-feature.model.ts
   94:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  172:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  195:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  222:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  290:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/default-unit-prices/models/default-unit-price.model.ts
   80:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  111:21  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  158:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  217:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  323:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  455:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/forecasted-trending-products/models/forecasted-trending-products.model.ts
  345:30  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  402:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  445:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  482:28  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/product-annual-sales/models/product-annual-sales.model.ts
   46:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
   98:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  147:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/root-categories-correlations/models/root-category-correlation.model.ts
  55:29  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/style-alternatives/models/style-alternative.model.ts
   73:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
   94:22  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  202:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/style-colors/models/style-color.model.ts
   72:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
   99:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  128:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  157:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  211:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  312:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  442:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/styles-hash/models/styles-hash.model.ts
   73:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
   97:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  124:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  169:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/db/styles/models/style.model.ts
  458:38  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments
  579:38  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

/Users/4thwithme/Documents/repo/recommendations-service/src/modules/rest/frequently-bought-together/frequently-bought-together.controller.ts
   39:3   warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unnecessary-condition')
   41:11  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
   41:14  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
   41:42  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
   42:18  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
   42:21  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
   69:3   warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unnecessary-condition')
   71:11  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
   71:14  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
   71:42  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
   72:18  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
   72:21  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
  101:3   warning  Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-unnecessary-condition')
  103:11  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
  103:14  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
  103:42  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition
  104:18  warning  Unnecessary conditional, expected left-hand side of `??` operator to be possibly null or undefined              @typescript-eslint/no-unnecessary-condition
  104:21  warning  Unnecessary optional chain on a non-nullish value                                                               @typescript-eslint/no-unnecessary-condition

/Users/4thwithme/Documents/repo/recommendations-service/src/unit-tests/bigquery.service.unit-spec.ts
  115:27  error  This value can be trivially inferred for this type parameter, so it can be omitted  @typescript-eslint/no-unnecessary-type-arguments

✖ 56 problems (38 errors, 18 warnings)
  37 errors and 3 warnings potentially fixable with the `--fix` option.

for context i updated macos recently to the last vesrsion

> AGENT

The macOS update itself didn't cause this — these are real ESLint errors already in the codebase. More likely culprit: the update triggered a Node.js/npm version change, which may have caused `npm install` to pull updated `@typescript-eslint` packages with stricter rules now enabled.

Check what changed:

> AGENT

There's the cause. `@typescript-eslint` bumped `8.56.0 → 8.58.0` when npm ran (triggered by macOS update). New version catches more violations.

The errors are real — need fixing. Most are auto-fixable. Want me to fix them all?

> DEVELOPER

yep

> AGENT

Auto-fix resolved the `no-unnecessary-type-arguments` errors. 3 remaining issues to fix manually. Reading the files.

> AGENT

Let me check the response DTOs to understand property types.

> AGENT

Now I know what to fix:
- `frequently-bought-together.controller.ts`: Properties are non-optional in DTOs → remove `?.` and `??` guards
- `forecast-trending-products.command.ts:332`: Wrap `error` with instanceof guard
- `bigquery.service.unit-spec.ts:8`: Remove unused `StyleCopurchaseRow` import

> AGENT

Now verify:

> AGENT

All clean. Lint, format, and type-check all pass.

> DEVELOPER

Summary of all failing tests
 FAIL  src/unit-tests/algolia.service.unit-spec.ts (6.865 s)
  ● AlgoliaService › getRelatedProductIds › should handle ObjectID does not exist error without rollbar error

    expect(jest.fn()).not.toHaveBeenCalled()

    Expected number of calls: 0
    Received number of calls: 1

    1: {"context": {"className": "AlgoliaService", "error": {"message": "Failed to fetch related product IDs for productId 123", "name": "Error", "stack": "Error: Failed to fetch related product IDs for productId 123
        at AlgoliaService.getRelatedProductIds (/Users/4thwithme/Documents/repo/recommendations-service/src/modules/algolia/algolia.service.ts:343:10)
        at processTicksAndRejections (node:internal/process/task_queues:103:5)
        at AlgoliaService.descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/src/decorators/log-execution.decorator.ts:97:20)
        at Object.<anonymous> (/Users/4thwithme/Documents/repo/recommendations-service/src/unit-tests/algolia.service.unit-spec.ts:628:4)"}, "errorMessage": "Failed to fetch related product IDs for productId 123", "errorStack": "Error: Failed to fetch related product IDs for productId 123
        at AlgoliaService.getRelatedProductIds (/Users/4thwithme/Documents/repo/recommendations-service/src/modules/algolia/algolia.service.ts:343:10)
        at processTicksAndRejections (node:internal/process/task_queues:103:5)
        at AlgoliaService.descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/src/decorators/log-execution.decorator.ts:97:20)
        at Object.<anonymous> (/Users/4thwithme/Documents/repo/recommendations-service/src/unit-tests/algolia.service.unit-spec.ts:628:4)", "executionTimeMs": 0.15212499999961437, "methodName": "getRelatedProductIds", "success": false, "timestamp": "2026-04-06T16:03:01.694Z"}, "err": "Method AlgoliaService.getRelatedProductIds failed."}

      633 |
      634 |                     expect(errorSpy).toHaveBeenCalled();
    > 635 |                     expect(mockBufferedRollbar.error).not.toHaveBeenCalled();
          |                                                           ^
      636 |             });
      637 |
      638 |             it('should handle other errors with rollbar error', async () => {

      at Object.<anonymous> (src/unit-tests/algolia.service.unit-spec.ts:635:42)


Test Suites: 1 failed, 36 passed, 37 total
Tests:       1 failed, 1026 passed, 1027 total

> AGENT

The newly added `@LogExecution` on `getRelatedProductIds` has `logErrToRollbar: true` by default — but the catch block already handles rollbar manually (skipping it for `ObjectID does not exist`). The decorator fires rollbar unconditionally, breaking the test.

Fix: add `logErrToRollbar: false` to that decorator.

> AGENT

Fixed. All 36 tests pass.

> DEVELOPER

hey bro run npm run test:coverage and fix tests until it passes
