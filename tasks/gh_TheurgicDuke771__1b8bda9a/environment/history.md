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

> DEVELOPER

Leave the Snowflake/UC part. 
Currently for parquet files we are adding ADLS/S3 as connection, how will it change if we add iceberg capability? and how the csv, parquet, and other flat file retrival will look like? will all the parquet be routed to iceberg engine?

> AGENT

Good — this is the connection-model question, which is the other half of the ADR. Let me ground it in how connections and runner dispatch actually work today.

> TOOL

tool_use Read
id: toolu_017jjaN1TVc3pip8wg8m4pz9
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/backend/app/datasources/registry.py"
}
```

> TOOL

tool_result
id: toolu_017jjaN1TVc3pip8wg8m4pz9
```
1	"""Connection-type → adapter + runner registry.
2	
3	The single place that maps a ``Connection.type`` to its `ConnectionAdapter`
4	(`get_connection_adapter`, all six types) and — for datasources only — to its
5	`CheckRunner` builder (`build_check_runner`). Service/worker code dispatches
6	through these and never branches on ``connection.type`` itself; adding a
7	datasource is an entry here plus the adapter/runner, nothing else.
8	"""
9	
10	from __future__ import annotations
11	
12	from typing import Any, Protocol
13	
14	from backend.app.core.secrets import SecretStore
15	from backend.app.datasources.adls import AdlsConnectionAdapter
16	from backend.app.datasources.base import CheckRunner, ConnectionAdapter
17	from backend.app.datasources.flatfile import build_flatfile_runner
18	from backend.app.datasources.s3 import S3ConnectionAdapter
19	from backend.app.datasources.snowflake import SnowflakeConnectionAdapter, build_snowflake_runner
20	from backend.app.datasources.unity_catalog import (
21	    UnityCatalogConnectionAdapter,
22	    build_unity_catalog_runner,
23	)
24	from backend.app.orchestration.adf import ADFConnectionAdapter
25	from backend.app.orchestration.airflow import AirflowConnectionAdapter
26	from backend.app.orchestration.dbt import DbtConnectionAdapter
27	
28	
29	class UnsupportedConnectionTypeError(ValueError):
30	    """Raised when no adapter is registered for a connection type."""
31	
32	
33	# Datasource and orchestration-provider connection types share this one registry
34	# (both implement the `ConnectionAdapter` seam); the run path keeps them apart —
35	# only datasources get a `CheckRunner`. ADF, Airflow, and dbt are orchestration
36	# providers, so their […]

> TOOL

tool_use Read
id: toolu_013XLqttm2ZZUQ7upCb8degA
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/backend/app/datasources/base.py"
}
```

> TOOL

tool_result
id: toolu_013XLqttm2ZZUQ7upCb8degA
```
1	"""Datasource adapter seam.
2	
3	Every datasource (Snowflake now; ADLS / S3 / Unity Catalog later) executes DQ
4	checks behind one ``CheckRunner`` interface that speaks GX-agnostic DTOs. The
5	GX-specific machinery lives entirely inside each adapter, so the run-service and
6	its tests depend only on the types here — never on Great Expectations internals.
7	This is also the seam that lets v1.1 swap GX for DQX on Unity Catalog (CLAUDE.md
8	§5) without rippling into the suite / check / result layer.
9	
10	`CheckSpec` goes in (a check pulled from the DB); `CheckOutcome` comes out, one
11	per check, shaped to map cleanly onto the `results` table columns. Adapters
12	translate GX results into these DTOs; tests provide a fake `CheckRunner` and
13	never touch a live datasource.
14	"""
15	
16	from __future__ import annotations
17	
18	from dataclasses import dataclass
19	from typing import Any, Protocol, runtime_checkable
20	
21	from pydantic import BaseModel
22	
23	
24	@dataclass(frozen=True)
25	class CheckSpec:
26	    """One expectation to evaluate, sourced from a `checks` row.
27	
28	    `expectation_type` is the GX snake_case name (e.g.
29	    ``expect_column_values_to_not_be_null``); `kwargs` are its parameters
30	    (e.g. ``{"column": "id"}``). […]

> AGENT

Grounded in the dispatch code now. Here's exactly how it changes — and the key answer up front: **no, parquet does not get rerouted to Iceberg.** Routing is by `connection.type`, decided when the connection is created, not by file extension.

## How runner selection works today

[registry.py:135-144](backend/app/datasources/registry.py#L135-L144) dispatches purely on `conn_type`:

```
connection.type ──► build_check_runner ──►  snowflake     → SnowflakeCheckRunner   (SQL pushdown)
                                            adls_gen2 / s3 → FlatFileCheckRunner    (one object → DataFrame)
                                            unity_catalog  → UnityCatalogCheckRunner (SQL Warehouse)
```

Within flat-file, csv-vs-parquet is chosen by the **path extension** ([format_from_path](backend/app/datasources/flatfile.py#L50-L57)): `.csv`→`read_csv`, `.parquet`/`.pq`→`read_parquet`, anything else → `ValueError`. One object in, one DataFrame out.

## Adding Iceberg = a new connection *type*, parallel to the others

Iceberg becomes its own registry entry — exactly how `unity_catalog` is a distinct type even though it also sits on cloud storage underneath. Nothing about `adls_gen2`/`s3` changes:

```
connection.type ──► ...
                    adls_gen2 / s3 → FlatFileCheckRunner   ← UNCHANGED (csv + parquet objects)
                    iceberg        → IcebergCheckRunner     ← NEW (pyiceberg catalog scan → DataFrame)
```

So concretely:

- **csv / parquet retrieval: identical to today.** An `adls_gen2` or `s3` connection with a target path `orders_2026-06-01.parquet` still goes single-object → `read_parquet`. No change, no rerouting.
- **A plain `.parquet` object is never treated […]

> DEVELOPER

Yes write an ADR, mention why we choose iceberg v2, why we are not checking Snoflake Iceberg tables or Databricks foreign catalog. And for Iceberg connection lets go with option A. [example scenario - there might be a situation where user added an ADLS path which has both flat file and iceberg tables, but later user choose to delete the flat file connection and only going to be use the ADLS for iceberg table going forward. In that case, it would be a cleaner approach and we also have a cascade delete on the foreign key. So that scenario might be also in play]. 
One question will pyiceberg be able to read delta-uniform?

> AGENT

Let me answer the Delta-UniForm question, and read the ADR conventions so the new one matches the repo.

> TOOL

tool_use Bash
id: toolu_016JHUcYsocHmEoG4a7acoNV
```json
{
  "command": "ls docs/adr/ && echo \"=== README tail ===\" && tail -40 docs/adr/README.md",
  "description": "List ADRs and view index format"
}
```

> TOOL

tool_result
id: toolu_016JHUcYsocHmEoG4a7acoNV
```
0001-trunk-based-branching.md
0002-conventional-commits.md
0003-gx-only-for-v1.md
0004-orchestration-abstraction.md
0005-severity-tier-weights.md
0006-adf-webhook-authentication.md
0007-airflow-callback-model.md
0008-mcp-server.md
0009-flat-monorepo-layout.md
0010-provider-agnostic-infrastructure-seams.md
0011-extensibility-seams-for-deferred-integrations.md
0012-monitor-kind-seam.md
0013-marketplace-distribution-and-anti-lock-in.md
0014-reconciliation-comparison-check-kind.md
0016-severity-derivation-semantics.md
0017-python-313-runtime-upgrade.md
0018-results-surface-and-grafana-deferral.md
0019-custom-sql-check-kind.md
0020-history-and-audit-strategy.md
0021-demo-test-data-environment-strategy.md
0022-week6-prototype-adoption-and-chart-library.md
0023-container-image-registry-ghcr.md
0024-app-deployment-infrastructure.md
0025-production-image-pip-slim.md
0026-auth-api-keys-and-principal-seam.md
0027-suite-permission-model-workspace-admin.md
0028-cloud-neutral-image-runtime-config-generic-oidc.md
0029-dbt-orchestration-provider.md
README.md
=== README tail ===
```

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-trunk-based-branching.md) | Trunk-based branching with squash-merge into `main` | Accepted |
| [0002](0002-conventional-commits.md) | Conventional commits for PR titles and commit messages | Accepted |
| [0003](0003-gx-only-for-v1.md) | GX-only for v1; DQX deferred to v1.1 for DLT/streaming | Accepted |
| [0004](0004-orchestration-abstraction.md) | Unified `OrchestrationProvider` abstraction for ADF and Airflow | Accepted |
| [0005](0005-severity-tier-weights.md) | Severity tier weights (warn / fail / critical → health score) | Accepted |
| [0006](0006-adf-webhook-authentication.md) | ADF webhook authentication (shared secret in URL + hard-cutover rotation) | Accepted |
| [0007](0007-airflow-callback-model.md) | Airflow callback model (HMAC-signed webhook + polling fallback) | Accepted |
| [0008](0008-mcp-server.md) | FastMCP server at `/mcp` — Azure AD token validated (same token as REST); all 8 exposed as tools; thin wrappers reusing the service layer + per-suite authz; fail-closed without auth | Accepted |
| [0009](0009-flat-monorepo-layout.md) | Repo layout — flat monorepo (`backend/` + `frontend/`) | Accepted |
| […]

> TOOL

tool_use Read
id: toolu_01PCQaYSv1EvieNrAswqQ2Fh
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0029-dbt-orchestration-provider.md"
}
```

> TOOL

tool_result
id: toolu_01PCQaYSv1EvieNrAswqQ2Fh
```
1	# ADR 0029 — dbt as a third OrchestrationProvider (artifact-poll + HMAC webhook)
2	
3	- **Status:** Accepted
4	- **Date:** 2026-07-05
5	- **Deciders:** solo-dev
6	- **Related:** [0004](0004-orchestration-abstraction.md) (orchestration seam), [0007](0007-airflow-callback-model.md) (the sibling callback model this mirrors), [0011](0011-extensibility-seams-for-deferred-integrations.md) (second-impl-deferred seams), [0010](0010-provider-agnostic-infrastructure-seams.md)/[0013](0013-marketplace-distribution-and-anti-lock-in.md) (anti-lock-in). Issue #611 (split from #609).
7	
8	## Context
9	
10	ADR 0004 established one `OrchestrationProvider` seam with ADF as the reference impl and Airflow as the second. dbt is a **third** orchestration layer — a genuine second-generation test of the seam (not dbt clubbed under the already-proven Airflow provider). The harness dbt project (#609) produces the runs to observe.
11	
12	The problem: **dbt Core has no runs API.** dbt Cloud's free tier has no API/scheduler; dbt-on-Snowflake observes via Snowflake (dies with the trial); Databricks dbt tasks observe via the Jobs API. Binding to any of those couples DataQ to a host. What *every* dbt deployment produces, wherever it runs, is **artifacts** (`run_results.json`, `manifest.json`) and the ability to run a command after a build. So the provider must bind to that universal surface — neutrality by construction (ADR 0010/0013).
13	
14	## Decision
15	
16	Add a `dbt` provider that […]

> AGENT

I have the ADR conventions. Let me verify the Delta-UniForm specifics against current docs before baking them into a durable ADR.

> TOOL

tool_use ToolSearch
id: toolu_018Dh3LoChxTMAsueFnDoxBC
```json
{
  "query": "select:mcp__claude_ai_Microsoft_Learn__microsoft_docs_search",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_018Dh3LoChxTMAsueFnDoxBC
```
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Microsoft_Learn__microsoft_docs_search"
}
```

> TOOL

tool_use mcp__claude_ai_Microsoft_Learn__microsoft_docs_search
id: toolu_01H8m6MncgygtewXUVBXBXVg
```json
{
  "query": "Delta Lake UniForm Iceberg read Unity Catalog Iceberg REST catalog external clients"
}
```

> TOOL

tool_result
id: toolu_01H8m6MncgygtewXUVBXBXVg
```
{"results":[{"title":"Read Delta Lake tables with Iceberg clients using UniForm","content":"# Read Delta Lake tables with Iceberg clients using UniForm\nAvailable in Databricks Runtime 14.3 LTS and above, Iceberg reads allow you to configure Delta Lake tables to automatically generate Iceberg metadata, enabling Iceberg clients to read Delta Lake data without rewriting files.\nYou can configure an external connection to have Unity Catalog act as an Iceberg catalog. See [Access Azure Databricks tables from Apache Iceberg clients](https://learn.microsoft.com/azure/databricks/external-access/iceberg).\n## How Iceberg reads work\nBoth Delta Lake and Apache Iceberg consist of Parquet data files and a metadata layer. Enabling Iceberg reads configures your Delta Lake tables to automatically generate Iceberg metadata asynchronously, without rewriting data, enabling Iceberg clients to read them. A single copy of the data files supports multiple formats.\nWhen using Iceberg reads, consider the following:\n1. Delta Lake tables with Iceberg reads enabled use Zstandard instead of Snappy as the compression codec for underlying Parquet data files.\n2. Iceberg metadata generation runs asynchronously on the compute used to write data to Delta Lake tables, which might increase the driver resource usage.\nFor documentation about the legacy UniForm `IcebergCompatV1` table feature, see [Legacy UniForm IcebergCompatV1](https://learn.microsoft.com/azure/databricks/archive/legacy/uniform).\n## Requirements\nTo enable Iceberg reads, the following requirements must be met:\n1. […]

> AGENT

Confirmed against Databricks docs — I'll answer the UniForm question, then write the ADR.

**Delta UniForm + pyiceberg — yes, read-only, via the Iceberg REST catalog.** When you enable "Iceberg reads" (UniForm) on a Delta table, Databricks *asynchronously generates Iceberg metadata over the same parquet data files* (no data rewrite). An Iceberg client reads it through Unity Catalog's **Iceberg REST Catalog (IRC)**, which the docs list as giving "read-only access to Delta Lake tables with Apache Iceberg reads enabled (UniForm)." Since pyiceberg ships a `RestCatalog`, **pyiceberg can read Delta UniForm tables** — which is a nice bonus: the same native path reaches Delta tables, not just Iceberg-native ones, without a Databricks warehouse running. Three caveats worth recording:
- **It's Iceberg v2** (`delta.enableIcebergCompatV2`) — reinforces our v2 baseline.
- **Async metadata lag** — the Iceberg snapshot trails the latest Delta commit (`converted_delta_version`/`converted_delta_timestamp` track how far); you may read a slightly stale snapshot.
- **No deletion vectors** — UniForm and Delta deletion vectors are mutually exclusive, so this stays inside clean v2 territory.

Now the ADR:

> TOOL

tool_use Write
id: toolu_01UJWYv7BttUu3MUP5F9Bgav
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md",
  "content": "# ADR 0030 — Apache Iceberg support: native `pyiceberg` read (v2) behind a self-contained `iceberg` datasource\n\n- **Status:** Accepted (spike decision, 2026-07-07; native impl deferred — see Consequences)\n- **Date:** 2026-07-07\n- **Deciders:** solo-dev\n- **Related:** [0003](0003-gx-only-for-v1.md) (GX-only; DQX swap seam), [0011](0011-extensibility-seams-for-deferred-integrations.md) (second-impl-deferred seams — `CheckRunner`/`ConnectionAdapter`), [0012](0012-monitor-kind-seam.md) (freshness/schema-drift monitor kinds this feeds), [0010](0010-provider-agnostic-infrastructure-seams.md)/[0013](0013-marketplace-distribution-and-anti-lock-in.md) (anti-lock-in), [0015](README.md) (pending two-connection model — the Option B evolution). Issue [#286](https://github.com/TheurgicDuke771/DataQ/issues/286).\n\n## Context\n\nApache Iceberg is increasingly the default open table format on Databricks (Unity Catalog managed tables), Snowflake, and object storage (S3 Tables / ADLS + Polaris). #286 asks whether DataQ should read Iceberg tables natively. The spike (this session) answered two prior questions first, because they collapse most of the scope:\n\n1. **Does reading Iceberg through a query engine need new DataQ code?** No. `SnowflakeCheckRunner` (`add_table_asset` → SQL pushdown, `backend/app/datasources/snowflake.py`) and `UnityCatalogCheckRunner` (`pd.read_sql_table` over the SQL Warehouse, `backend/app/datasources/unity_catalog.py`) talk **SQL to the engine, never to the file format**. Whether an identifier resolves to a native FDN/Delta table or an Iceberg table (`CREATE ICEBERG TABLE … CATALOG_SOURCE=OBJECT_STORE`, or a Databricks foreign/UniForm table) is transparent to the connector, GX, and DataQ. A user can point a suite at an engine-registered Iceberg table **today, with […]

> TOOL

tool_result
id: toolu_01UJWYv7BttUu3MUP5F9Bgav
```
File created successfully at: /Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md (file state is current in your context — no need to Read it back)
```

> AGENT

Now the index entry:

> TOOL

tool_use Edit
id: toolu_01Tvw7pQheTe2Dhva6Shjsij
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "| [0029](0029-dbt-orchestration-provider.md) | dbt as a **third** `OrchestrationProvider` (mirrors the Airflow callback model 0007) — HMAC webhook + artifacts poll of `run_results.json` (adls/s3/file); binds to dbt's universal surface (no host API); job-level grain; migration widens the connection-type/provider/dedup value-sets (#611) | Accepted |\n\n## Pending (to be written in their respective weeks)",
  "new_string": "| [0029](0029-dbt-orchestration-provider.md) | dbt as a **third** `OrchestrationProvider` (mirrors the Airflow callback model 0007) — HMAC webhook + artifacts poll of `run_results.json` (adls/s3/file); binds to dbt's universal surface (no host API); job-level grain; migration widens the connection-type/provider/dedup value-sets (#611) | Accepted |\n| [0030](0030-iceberg-native-read-path.md) | Apache Iceberg — engine-level read (Snowflake/UC iceberg tables) is free, zero-code; the only new build is a **native `pyiceberg` read** (v2 baseline, v3 deferred) behind a thin `IcebergCheckRunner` (scan → DataFrame → `gx_runner`); new **self-contained** `iceberg` connection type (Option A: own catalog + storage credential — independent lifecycle, cascade-safe), Option B two-connection ref deferred to 0015; native impl deferred (#286) | Accepted (spike; native impl deferred) |\n\n## Pending (to be written in their respective weeks)"
}
```

> TOOL

tool_result ERROR
id: toolu_01Tvw7pQheTe2Dhva6Shjsij
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_013J19WeFS4Q8bT6cFHp6CTh
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/README.md",
  "offset": 40
}
```

> TOOL

tool_result
id: toolu_013J19WeFS4Q8bT6cFHp6CTh
```
40	
41	| # | Title | Status |
42	|---|---|---|
43	| [0001](0001-trunk-based-branching.md) | Trunk-based branching with squash-merge into `main` | Accepted |
44	| [0002](0002-conventional-commits.md) | Conventional commits for PR titles and commit messages | Accepted |
45	| [0003](0003-gx-only-for-v1.md) | GX-only for v1; DQX deferred to v1.1 for DLT/streaming | Accepted |
46	| [0004](0004-orchestration-abstraction.md) | Unified `OrchestrationProvider` abstraction for ADF and Airflow | Accepted |
47	| [0005](0005-severity-tier-weights.md) | Severity tier weights (warn / fail / critical → health score) | Accepted |
48	| [0006](0006-adf-webhook-authentication.md) | ADF webhook authentication (shared secret in URL + hard-cutover rotation) | Accepted |
49	| [0007](0007-airflow-callback-model.md) | Airflow callback model (HMAC-signed webhook + polling fallback) | Accepted |
50	| [0008](0008-mcp-server.md) | FastMCP server at `/mcp` — Azure AD token validated (same token as REST); all 8 exposed as tools; thin wrappers reusing the service layer + per-suite authz; fail-closed without auth | Accepted |
51	| [0009](0009-flat-monorepo-layout.md) | Repo layout — flat monorepo (`backend/` + `frontend/`) | Accepted |
52	| [0010](0010-provider-agnostic-infrastructure-seams.md) | Provider-agnostic infrastructure seams (Azure is the default, not the architecture) | Accepted |
53	| [0011](0011-extensibility-seams-for-deferred-integrations.md) | Extensibility seams for deferred […]

> TOOL

tool_use Edit
id: toolu_011Yv3gBdQX5YJC1v6eg3C6M
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/README.md",
  "old_string": "| [0029](0029-dbt-orchestration-provider.md) | dbt as a **third** `OrchestrationProvider` (mirrors the Airflow callback model 0007) — HMAC webhook + artifacts poll of `run_results.json` (adls/s3/file); binds to dbt's universal surface (no host API); job-level grain; migration widens the connection-type/provider/dedup value-sets (#611) | Accepted |\n\n## Pending (to be written in their respective weeks)",
  "new_string": "| [0029](0029-dbt-orchestration-provider.md) | dbt as a **third** `OrchestrationProvider` (mirrors the Airflow callback model 0007) — HMAC webhook + artifacts poll of `run_results.json` (adls/s3/file); binds to dbt's universal surface (no host API); job-level grain; migration widens the connection-type/provider/dedup value-sets (#611) | Accepted |\n| [0030](0030-iceberg-native-read-path.md) | Apache Iceberg — engine-level read (Snowflake/UC iceberg tables) is free & zero-code; the only new build is a **native `pyiceberg` read** (v2 baseline, v3 deferred) behind a thin `IcebergCheckRunner` (scan → DataFrame → `gx_runner`); new **self-contained** `iceberg` connection type (Option A: own catalog + storage credential — independent lifecycle, cascade-safe), Option B two-connection ref deferred to 0015; reads Delta UniForm too; native impl deferred (#286) | Accepted (spike; native impl deferred) |\n\n## Pending (to be written in their respective weeks)"
}
```

> TOOL

tool_result
id: toolu_011Yv3gBdQX5YJC1v6eg3C6M
```
The file /Users/arijit/Coding/Python/DataQ/docs/adr/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done. Here's what landed:

**[docs/adr/0030-iceberg-native-read-path.md](docs/adr/0030-iceberg-native-read-path.md)** — new ADR, plus the index row in [docs/adr/README.md](docs/adr/README.md). It records everything you asked for:

- **Why v2, not v3** — v2 is GA and read everywhere (Snowflake GA, Spark/Databricks, `pyiceberg` mature, Delta UniForm emits v2); v3's deletion-vectors/row-lineage are new and unevenly supported, so v3 goes behind a capability gate later.
- **Why we're not testing Snowflake iceberg tables / Databricks foreign catalog** — the SQL runners are format-transparent *by construction* (proven from `add_table_asset`/`read_sql_table` pushing SQL down, not by experiment); standing up an external volume / foreign catalog would only re-confirm what the code guarantees, at real live-infra cost during the wind-down. Engine-level read is documented as the free, zero-code, supported-today path.
- **Native `pyiceberg` is the only real new build** — thin `IcebergCheckRunner` (scan → DataFrame → `gx_runner`), and *why* an Iceberg table can't reuse the flat-file parquet read (snapshots / v2 deletes / schema-by-ID).
- **Option A (self-contained `iceberg` connection)** — with your independent-lifecycle scenario written into the rationale: register an ADLS path for flat files + Iceberg, later delete the flat-file connection and keep the storage for Iceberg only → clean because the `iceberg` connection owns its own credential and the cascade-delete […]