> DEVELOPER

Lets check #286

> TOOL

tool_use Bash
id: toolu_01HfVqRPUXRyjSFcrXEvaqqE
```json
{
  "command": "gh issue view 286 --json number,title,state,labels,milestone,body,comments",
  "description": "View GitHub issue #286"
}
```

> TOOL

tool_result
id: toolu_01HfVqRPUXRyjSFcrXEvaqqE
```
{"body":"## Summary\n\nAdd native Apache Iceberg v2 and v3 table format support as a post-v1 datasource extension. Iceberg is increasingly the default open table format on Databricks (Unity Catalog), AWS (S3 Tables), and Azure (ADLS Gen2 with Polaris / Azure Managed Iceberg), making it a natural next step after the v1 flat-file and Unity Catalog paths.\n\n## Motivation\n\n- Unity Catalog (v1 datasource) now defaults to Iceberg v2 under the hood for managed tables — surfacing Iceberg natively lets DataQ profile and run checks directly against the table metadata and snapshot history rather than reading through a SQL Warehouse.\n- Iceberg v3 (encryption, row lineage, multi-arg transforms) is GA on some engines; users on the bleeding edge will expect it.\n- The `FlatFileCheckRunner` / `UnityCatalogCheckRunner` seams (CLAUDE.md §5 / ADR 0011) already read into a pandas DataFrame — an Iceberg reader (`pyiceberg`) slots in at the same boundary without touching the GX or severity layers.\n- Iceberg's snapshot / time-travel model opens a natural path for **freshness** and **schema-drift** monitor kinds (ADR 0012 reserved kinds) once those are implemented in v1.x.\n\n## Proposed scope\n\n- [ ] `IcebergConnectionAdapter` — catalog config (REST / Hive / Glue / Unity), warehouse path (S3 / ADLS), auth […]

> AGENT

This is the Iceberg spike (#286) — deferred to its own session per CLAUDE.md. Let me get grounded on the relevant seams and constraints before proposing how to run it.

> TOOL

tool_use Bash
id: toolu_01TYTafuL3G5y7qYsGsrQFJF
```json
{
  "command": "cat docs/adr/0015*.md 2>/dev/null | head -80; echo \"===ADR INDEX (0015)===\"; grep -i \"0015\\|iceberg\\|two-connection\\|comparison\" docs/adr/README.md",
  "description": "Read ADR 0015 and index entries"
}
```

> TOOL

tool_result
id: toolu_01TYTafuL3G5y7qYsGsrQFJF
```
(eval):1: no matches found: docs/adr/0015*.md
===ADR INDEX (0015)===
| [0014](0014-reconciliation-comparison-check-kind.md) | Cross-dataset reconciliation as a `comparison` check kind (reuse FastAPI_DataComparison engine) | Accepted |
| 0015 | Two-connection check model (source + target refs for `comparison` checks) | When reconciliation build starts (post-v1) |
```

> TOOL

tool_use Bash
id: toolu_01Tmb7kxCgV82e1k5vZF8hoo
```json
{
  "command": "ls backend/app/datasources/ && echo \"===\" && grep -rl \"CheckRunner\" backend/app/datasources/ | head",
  "description": "List datasource adapters/runners"
}
```

> TOOL

tool_result
id: toolu_01Tmb7kxCgV82e1k5vZF8hoo
```
__init__.py
__pycache__
adls.py
base.py
flatfile.py
gx_runner.py
monitors.py
registry.py
s3.py
snowflake.py
unity_catalog.py
===
backend/app/datasources/flatfile.py
backend/app/datasources/registry.py
backend/app/datasources/unity_catalog.py
backend/app/datasources/monitors.py
backend/app/datasources/adls.py
backend/app/datasources/snowflake.py
backend/app/datasources/s3.py
backend/app/datasources/base.py
backend/app/datasources/gx_runner.py
```

> TOOL

tool_use Bash
id: toolu_01FEAGqSm2wBhsikGC4iXxdw
```json
{
  "command": "grep -rn \"iceberg\\|Iceberg\\|pyiceberg\\|PyIceberg\" backend/ docs/ context/ 2>/dev/null | grep -vi \"test\" | head -30",
  "description": "Search for existing Iceberg references"
}
```

> TOOL

tool_result
id: toolu_01FEAGqSm2wBhsikGC4iXxdw
```
docs/progress.md:128:> (Iceberg v2 ADLS spike, pulled forward from the W7 stretch).
docs/progress.md:152:> **In-week follow-ups (2026-07-07):** #571 run-detail `checks_total` graft + semantics ([#699](https://github.com/TheurgicDuke771/DataQ/pull/699)) · #640 flaky `LiveRunProgress` terminal-state assertion ([#700](https://github.com/TheurgicDuke771/DataQ/pull/700)) · #643 `suite_policy_possibly_stale` event on repointing a policied target ([#701](https://github.com/TheurgicDuke771/DataQ/pull/701)) · #605 redaction-safe `runs.failure_reason` end-to-end ([#702](https://github.com/TheurgicDuke771/DataQ/pull/702), migration `c605d1e2f3a4`). **#286 (Iceberg v2/v3) deferred to its own focused session** — it needs a `pyiceberg` dependency eval + an ADR and touches the unsettled two-connection model (ADR 0015); still open on the W2 milestone.
docs/progress.md:278:| ⬜ | [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) Apache Iceberg v2/v3 table-format support (spike first) | Theme 2 |
context/post-v1-roadmap.md:112:| [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) | Apache Iceberg v2 / v3 table-format support |
context/post-v1-roadmap.md:346:| _(no issue yet)_ | **Trino adapter (+ Amazon Athena)** — the G-f multiplier: one SQLAlchemy dialect inherits the user's entire Trino/Starburst connector ecosystem (Hive, Iceberg, Cassandra, Mongo, Kafka-topics-as-tables — anything their cluster federates) with no per-store adapters on our side; **Athena** rides the same dialect family for serverless AWS. The cheapest answer to "4 datasources vs the 30–50 a category product ships". |
context/post-v1-roadmap.md:364:DQX v1.1 lane, ADR [0003](../docs/adr/0003-gx-only-for-v1.md)); **Delta / Iceberg table formats
context/post-v1-roadmap.md:365:on raw object storage** — Iceberg is already tracked as [#286](https://github.com/TheurgicDuke771/DataQ/issues/286)
```

> TOOL

tool_use Bash
id: toolu_01Liz2yJicwkauuM5RvrLc2q
```json
{
  "command": "ls ~/Coding/Python/DataQ-harness/ 2>/dev/null && echo \"===mockdata===\" && ls ~/Coding/Python/DataQ-harness/mockdata/ 2>/dev/null; echo \"===HARNESS_TODO iceberg===\"; grep -ni \"iceberg\" ~/Coding/Python/DataQ-harness/HARNESS_TODO.md 2>/dev/null | head",
  "description": "Inspect harness repo for iceberg tooling"
}
```

> TOOL

tool_result
id: toolu_01Liz2yJicwkauuM5RvrLc2q
```
DATABRICKS_MIGRATION_TODO.md
Dockerfile
README.md
airflow
airflow-metadata-backup.dump
databricks
dataq_setup
dbt
eventgrid_receiver
mockdata
scripts
secrets.sh
terraform
===mockdata===
README.md
__init__.py
__main__.py
__pycache__
config.py
dq_issues.py
emit.py
generate.py
increment.py
pools.py
requirements.txt
rng.py
state.py
storage.py
===HARNESS_TODO iceberg===
```

> AGENT

I've got the full picture on #286. Here's where it stands:

**What it is:** A spike (not the full build) to decide DataQ's Apache Iceberg read path. It's on the **v1.1 Week 2** milestone (due 2026-07-17), P3, and was deliberately deferred to its own session because it needs a `pyiceberg` dependency eval, a new ADR, and it brushes the unsettled two-connection model (ADR 0015 — which is still *unwritten*, status "when reconciliation build starts").

**The concrete spike shape** (from your 2026-07-05 comment) has 3 acceptance criteria:
1. Iceberg v2 table written to harness **ADLS** via PyIceberg (local, no new compute) → readable as a **Snowflake** iceberg table (external volume + object-store catalog) → **DataQ suite runs green** against it
2. **Databricks** read attempted; Free-Edition capability/limitation documented
3. v2-vs-v3 decision recorded; follow-up implementation issues filed

**The constraint that matters:** this is a *live-infra* spike, and both the Snowflake trial and Azure subscription wind down ~2026-07-25 (per your wind-down memory; harness compute is currently **stopped**). So the Snowflake/Databricks legs have a hard clock. The good news: the PyIceberg→ADLS write leg is "local, no new compute" and ADLS storage persists even with harness compute stopped — so the dependency eval and read-path decision […]

> TOOL

tool_use AskUserQuestion
id: toolu_01Dn1uF5amP6wGJa8AirpCa8
```json
{
  "questions": [
    {
      "question": "How far should this session take the #286 spike?",
      "header": "Spike scope",
      "multiSelect": false,
      "options": [
        {
          "label": "Full live spike",
          "description": "Do all 3 ACs: PyIceberg→ADLS write, stand up Snowflake external volume + iceberg table, run a DataQ suite green against it, attempt Databricks read, then ADR + follow-up issues. Uses the live Snowflake/Azure window (needs harness wake + credentials)."
        },
        {
          "label": "Local eval + decision + ADR",
          "description": "Do the parts with no live-infra dependency: pyiceberg dependency/CVE eval, PyIceberg→ADLS write proof, record the v2-vs-v3 + read-path decision, draft the ADR, and file follow-up implementation issues. Defer the Snowflake/Databricks read legs."
        },
        {
          "label": "Just plan it",
          "description": "Produce a written spike plan (steps, credentials needed, cost/time estimate, risk) and stop — no code or infra changes this session. You run it later."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01Dn1uF5amP6wGJa8AirpCa8
```
Your questions have been answered: "How far should this session take the #286 spike?"="If we read the Iceberg from snowflake iceberg table or Databricks Foreign catalog will it be any different from how we are reading snowflake or UC?". You can now continue with these answers in mind.
```

> AGENT

Excellent question — that's actually the crux of the whole spike, and it may collapse most of the scope. Let me verify against the actual runner code rather than assert it.

> TOOL

tool_use Read
id: toolu_01GdC9LGgkwmNc6JRFzvDdWp
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/backend/app/datasources/snowflake.py"
}
```

> TOOL

tool_result
id: toolu_01GdC9LGgkwmNc6JRFzvDdWp
```
1	"""Snowflake datasource adapter (GX Core 1.17).
2	
3	All Great-Expectations-specific machinery for Snowflake lives here, behind the
4	`CheckRunner` seam in ``base.py`` — per CLAUDE.md, the GX version-specific API
5	must not leak into the suite / check / result layer (GX v1 has drifted across
6	point releases).
7	
8	The full GX chain (``add_snowflake`` → ``add_table_asset`` →
9	``add_batch_definition_whole_table`` → ``ValidationDefinition.run``) connects to
10	Snowflake at asset-build time, so ``run_checks`` cannot run without a live
11	warehouse. Tests therefore exercise the GX-free parts directly — config
12	validation, connection-string building, the snake_case→GX-class translation,
13	and the GX-result→`CheckOutcome` mapping (fed a canned result) — and inject a
14	fake `CheckRunner` elsewhere. End-to-end validation against a real Snowflake DEV
15	warehouse is a tracked follow-up.
16	"""
17	
18	from __future__ import annotations
19	
20	import base64
21	import json
22	from typing import Any, Literal
23	from urllib.parse import quote_plus
24	
25	import great_expectations as gx
26	from cryptography.hazmat.primitives import serialization
27	from pydantic import BaseModel, ConfigDict, Field, model_validator
28	
29	from backend.app.core.secrets import SecretStore
30	from backend.app.datasources.base import CheckOutcome, CheckSpec, MonitorSpec, SuiteOutcome
31	
32	# GX-translation machinery is shared across runners (see `gx_runner`); […]

> TOOL

tool_use Read
id: toolu_01BcWLDnX9MjD2v4UX5DCsf2
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/backend/app/datasources/unity_catalog.py"
}
```

> TOOL

tool_result
id: toolu_01BcWLDnX9MjD2v4UX5DCsf2
```
1	"""Unity Catalog (Databricks) connection adapter.
2	
3	A datasource (CLAUDE.md §4): DQ checks run against Unity Catalog tables via a
4	Databricks SQL Warehouse. Week 2 ships only the `ConnectionAdapter` seam (config
5	validation + connectivity `test`).
6	
7	**Runner seam note:** the *check-run* path for UC must sit behind a
8	``UnityCatalogCheckRunner`` interface so v1.1 can swap GX for Databricks Labs DQX
9	on DLT/streaming (CLAUDE.md §5, ADR 0003). That runner is Week-3 work and is
10	deliberately **not** built here — this module is connection config + a
11	connectivity probe only.
12	
13	Auth is a **personal access token (PAT)** — the v1 default, held in the
14	SecretStore (no credential-less mode, so none of the ADLS/S3 ``secret_ref``
15	nullability deferral applies). ``test`` opens a SQL-Warehouse connection and runs
16	``SELECT 1`` — a green test means the workspace + warehouse are reachable and the
17	PAT authenticates. ``databricks-sql-connector`` is imported lazily (per
18	``core/secrets.py``); like the other adapters it runs live and fails-soft pending
19	real credentials.
20	"""
21	
22	from __future__ import annotations
23	
24	from typing import Any
25	from urllib.parse import quote_plus, urlparse
26	
27	import great_expectations […]

> AGENT

Verified against the runner code — here's the precise answer to your question, because it actually reframes the whole spike.

## Reading Iceberg *through an engine* = **zero new DataQ code**

Both existing runners talk **SQL to the engine**, never to the file format:

- **Snowflake** ([snowflake.py:214-218](backend/app/datasources/snowflake.py#L214-L218)): `add_table_asset(table_name=table, schema_name=schema)` → GX pushes SQL down to the warehouse. Snowflake resolves the identifier; whether it's a native FDN table or an Iceberg table created via `CATALOG_SOURCE=OBJECT_STORE` is **invisible** to the connector, the DSN, GX, and DataQ. It's just a table name. Same for `run_monitors` (scalar SQL, [:239-250](backend/app/datasources/snowflake.py#L239-L250)) and the profiler.
- **Unity Catalog** ([unity_catalog.py:151](backend/app/datasources/unity_catalog.py#L151)): `pd.read_sql_table(table, engine, schema=schema)` against the SQL Warehouse. A Databricks Foreign Catalog / UniForm-Iceberg table is addressed as `catalog.schema.table` — **identical** call.

So if the user registers their Iceberg table in Snowflake or Databricks, they just **point a suite target at it today**. No `IcebergConnectionAdapter`, no `IcebergCheckRunner`, no new ADR. It reuses the existing Snowflake/UC connection wholesale.

## What #286 is *actually* deciding

The only path that's **different** — and the only thing that justifies the new adapter+runner in the issue — is reading Iceberg **natively via `pyiceberg` directly from object storage (ADLS/S3), with no query engine in the […]

> TOOL

tool_use AskUserQuestion
id: toolu_015MVRGuQzXagC5FB453enU1
```json
{
  "questions": [
    {
      "question": "Given engine-level Iceberg is already free, what's the spike's target this session?",
      "header": "Path",
      "multiSelect": false,
      "options": [
        {
          "label": "Prove native pyiceberg path",
          "description": "Local pyiceberg dep/CVE eval + write a v2 table to ADLS + read it back to a DataFrame (the FlatFileCheckRunner shape) to confirm the native path is viable. This is the decision the whole issue hinges on; needs no query engine."
        },
        {
          "label": "Confirm engine path + document",
          "description": "Skip building native. Do a quick live confirm that a Snowflake iceberg table runs green under the existing runner (needs live SF window), then write the ADR concluding 'engine-level now, pyiceberg deferred' + file/close follow-ups."
        },
        {
          "label": "Both legs",
          "description": "Native pyiceberg viability proof AND the engine-level live confirm — the full AC set — then ADR + follow-up issues. Most complete, uses the live SF/Azure window."
        },
        {
          "label": "Just write the ADR + close",
          "description": "The finding above is conclusive enough: record it as the ADR (engine-level works today, native pyiceberg is the only new build and it's deferred), file follow-up implementation issues, and close the spike without running live infra."
        } […]

> TOOL

tool_result
id: toolu_015MVRGuQzXagC5FB453enU1
```
Your questions have been answered: "Given engine-level Iceberg is already free, what's the spike's target this session?"="for flat file we are currently reading parquet files, how will iceberg be different?". You can now continue with these answers in mind.
```

> AGENT

Right question again — let me read the flat-file runner so I answer precisely, because the difference is the whole reason Iceberg needs its own runner rather than reusing the parquet path.

> TOOL

tool_use Read
id: toolu_014fMtn1Mk6LGvuLqy6vmgv2
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/backend/app/datasources/flatfile.py"
}
```

> TOOL

tool_result
id: toolu_014fMtn1Mk6LGvuLqy6vmgv2
```
1	"""Flat-file (ADLS Gen2 / S3) IO + GX `CheckRunner`.
2	
3	Two responsibilities for the flat-file datasources, both behind the same
4	primitives the SQL adapters use (raw config dict + resolved secret, never the ORM
5	row — keeps `datasources/` decoupled from `db/`):
6	
7	* **IO** — `download_bytes` fetches an object/blob; `read_dataframe` parses it
8	  into pandas. Shared by the column profiler (service layer) and the runner.
9	* **Runner** — `FlatFileCheckRunner` runs GX expectations against the file by
10	  loading it into an in-memory pandas DataFrame and handing that to GX's pandas
11	  datasource, then mapping the result via the shared `gx_runner` machinery. The
12	  `CheckRunner` interface is table-shaped; for a flat-file datasource the
13	  ``table`` argument carries the **file path** and ``schema`` is unused.
14	
15	GX runs entirely in-process on the DataFrame, so — unlike the warehouse runners —
16	the run path is fully testable with a canned frame; only the network download is
17	the deferred-smoke seam.
18	"""
19	
20	from __future__ import annotations
21	
22	import io
23	import re
24	from dataclasses import dataclass
25	from datetime import UTC, datetime
26	from typing import Any […]

> AGENT

Yes — meaningfully different, and this is the part that determines whether native Iceberg is a real build or a trivial extension. It is **not** trivial.

## Flat-file today reads *one parquet file*

[flatfile.py:118](backend/app/datasources/flatfile.py#L118): `pd.read_parquet(raw)` on a **single downloaded blob**. The batch-resolution machinery ([:202-242](backend/app/datasources/flatfile.py#L202-L242)) even exists precisely to pick *one* file path (`orders_2026-06-01.parquet`) out of a prefix. The whole model is "one object → one DataFrame."

## An Iceberg table is a *table*, not a file

It's a directory tree: a metadata pointer (`metadata.json`) → manifest list → manifest files → **many** parquet data files across snapshots and partitions. You cannot `read_parquet` it. If you naively globbed and concatenated every `.parquet` under the prefix, you'd get **wrong answers** on all four of these:

| Iceberg mechanic | What breaks if you treat it as flat parquet |
|---|---|
| **Snapshots** | Old/expired snapshots' data files still sit in storage → you'd double-count stale rows. Only the current snapshot's manifest lists the *live* files. |
| **Delete files (v2)** | v2 positional/equality delete files logically remove rows. Raw parquet ignores them → you validate rows that no longer exist in the table. |
| **Schema evolution** | Iceberg reconciles schema by […]