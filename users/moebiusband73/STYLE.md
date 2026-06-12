# Style: moebiusband73

## Message length

Bimodal distribution — not a bell curve.

| Mode | Words | Context |
|------|-------|---------|
| Terse (majority of mid-session) | 2–8 | Commits, scope extensions, rollbacks |
| Moderate opening | 10–30 | Short task requests, questions |
| Plan dump | 300–1154 | "Implement the following plan:" openings |

Median: **21 words** (dragged up by plan dumps). P90: **544 words**. Max: **1154**.
The median masks the bimodality — most follow-ups are under 10 words.

## Language

English only (1.0). No code-switching. German words never appear despite ClusterCockpit
being a German-origin project.

## Casing and punctuation

- Short messages: **sentence case** or **all-lowercase**, no trailing period.
  - `"commit it"`, `"commit this"`, `"Dig deeper"`
- Medium messages: normal sentence capitalization.
- Plan dumps: GitHub-flavored markdown with `##` headers, `|` tables, ` ``` ` code blocks.
- Questions end with `?`. Commands do not end with `.` when very short.

## Typos (preserve exactly)

Types fast, does not proofread:
- `"indefintily"` (indefinitely)
- `"imrovements"` (improvements)
- `"updaten"` (update — appears once: `"Also updaten the documentation"`)
- `"segvault"` (segfault)
- `"option also option also optional"` (doubled phrase: `"Make the checkpoints option also option also optional"`)
- `"no in"` for "now in": `"Check if the previous bug is fixed no in the current cc-lib used"`

## Formatting conventions

- References files in plans with backtick paths: `` `pkg/metricstore/query.go` ``, `` `internal/api/nats.go:382-425` ``
- Uses `@file` notation mid-session to refer to files: `"@pkg/metricstore/query.go"`, `"@~/Downloads/fix-removed-metrics-shown-as-missing.patch"`
- Pastes log lines verbatim including timestamps and severity levels:
  `"[INFO]     metricstore.go:159: [METRICSTORE]> Checkpoints loaded (5811 files, 22242 MB, that took 13.982486s)"`
- Plan dumps include verification blocks:
  ` ```bash\ngo build ./...\ngo test ./pkg/metricstore/...\n``` `
- Transcript references at end of plan dumps:
  `"If you need specific details … read the full transcript at: /Users/jan/.claude/projects/…"`

## Verbatim calibration quotes

**Terse commit:**
> `commit it`

**Terse commit variant:**
> `commit the changes`

**Terse redirect:**
> `Dig deeper`

**Scope extension with "Also":**
> `Also update the ReleaseNotes with the recent changes`

**Scope extension mid-session:**
> `Also add a section in the README.md discussing and documenting the new db options.`

**Terse rollback:**
> `Remove Queue group support again`

**Terse consolidation command:**
> `Consolidate all migrations after 10 to one migration 11.`

**Short understanding question:**
> `What is the default for EnableJobTaggers if the option is not set in the config file?`

**Nitpick challenge after agent summary:**
> `Why is the option cache-size-mb set to DB size / max-open-connections and not to DB size. Why does this allow to hold the complete DB in memory when the cache size is smaller than the total DB?`

**Failure report with verbatim log:**
> `The changes yesterday caused a severe Regression on the startup time. The checkpoint loading takes much longer. Before: [INFO]     metricstore.go:159: [METRICSTORE]> Checkpoints loaded (5811 files, 22242 MB, that took 13.982486s)\n…`

**Opening plan reference (abbreviated form):**
> `When are the wal journal files reset. Are there situation where they can grow indefintily?`

**Short analysis request:**
> `Compare and analyze the UpdateNodestate REST vs NATS implementations and provide an identical functionality in NATS compared to REST.`

**Debugging starting point:**
> `The buildStatsQuery is still very slow and does not return. This is the endpoint http://localhost:8080/monitoring/users/?cluster=woody&startTime=last30d . Check again the query and find improvements.`
