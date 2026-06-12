---
name: log-paste-debug
description: >
  Trigger: a regression or production failure between sessions. User pastes raw log output
  verbatim — timestamps, severity, file:line, message — then says "Investigate the issue and
  fix it." or "Investigate the issue."
---

When something breaks in production or a regression appears after recent changes, the user
provides raw evidence rather than a description. The log paste includes:
- Systemd-style timestamps: `Mar 21 06:28:04 monitoring cc-backend[2671537]:`
- Or Go log format: `[INFO]     metricstore.go:159: [METRICSTORE]> ...`
- Actual numbers (file counts, MB, durations, row counts)
- Before/after comparison when it's a regression

The closing instruction is always short: `"Investigate the issue and fix it."` or
`"Investigate the issue:"` (with the log following the colon).

**Example — regression report:**
> `The changes yesterday caused a severe Regression on the startup time. The checkpoint loading takes much longer. Before: [INFO]     metricstore.go:159: [METRICSTORE]> Checkpoints loaded (5811 files, 22242 MB, that took 13.982486s)\n3/24/2026, 7:19:34 AMINFO… And after the changes: etricstore.go:159: [METRICSTORE]> Checkpoints loaded (5860 files, 21338 MB, that took 302.524814s)\n… Investigate the issue and fix it.`

**Example — production error:**
> `The cleanup archiving still does not work correctly. For some clusters the following log message occurs: Investigate the issue: Mar 21 06:28:04 monitoring cc-backend[2671537]: [ERROR]    /home/jan/cc-backend/pkg/metricstore/archive.go:69: [METRICSTORE]> archiving failed: writing parquet archive for cluster fritz: flushing parquet row group: the limit of 32767 row groups has been reached`

**Failure report without log** (agent did something, user sees nothing works):
> `The following error occurs in the Log view if enabling Auto Refresh. Investigate the issue and fix it.`
(No log pasted — agent must reproduce or find the error itself.)
