/**
 * DataClaw donors dropped from every published UserBench number.
 *
 * Source of truth is `COHORT_POLICY.md` in the harbor repo
 * (`/data/swesimbench-v2-harbor`), implemented there as `cohort_filters.py`
 * -> `EXCLUDED_DEVELOPERS`. The list is copied here because this app runs in
 * Node and cannot import that module; keep the two in step.
 *
 * Reporting-only. `items.json`, rater judgments and the judge trials all keep
 * every developer — only the aggregates drop these four.
 *
 * Match on the `developer` field, not the task id. Harbor's
 * `is_excluded_task_key()` tests for a `dc_000__` prefix, but the annotator
 * sample carries kevin task ids like `dc_dc_000__b5514499` and v2 ids like
 * `t080`, so that prefix test does not fit here.
 */
export const EXCLUDED_DEVELOPERS = [
  "dc:dc_000",
  "dc:dc_001",
  "dc:dc_004",
  "dc:dc_010",
] as const;

const EXCLUDED_SLUGS = new Set(
  EXCLUDED_DEVELOPERS.map((d) => d.split(":").pop()!),
);

/** True for an excluded donor, given `dc:dc_000` or the bare `dc_000`. */
export function isExcludedDeveloper(
  developer: string | null | undefined,
): boolean {
  if (!developer) return false;
  return EXCLUDED_SLUGS.has(developer.trim().split(":").pop()!);
}
