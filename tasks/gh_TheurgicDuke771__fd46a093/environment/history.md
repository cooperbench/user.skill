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

> DEVELOPER

do the local pyiceberg proof next + file follow-ups and close the spike out.

> TOOL

tool_use TodoWrite
id: toolu_01PBHNTKv6c78KqMfS1TpUmX
```json
{
  "query": "select:TodoWrite",
  "max_results": "1"
}
```

> TOOL

tool_result ERROR
id: toolu_01PBHNTKv6c78KqMfS1TpUmX
```
<tool_use_error>InputValidationError: TodoWrite failed due to the following issues:
The required parameter `todos` is missing
An unexpected parameter `query` was provided
An unexpected parameter `max_results` was provided

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:TodoWrite", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"todos":{"description":"The updated todo list","type":"array","items":{"type":"object","properties":{"content":{"type":"string","minLength":1},"status":{"type":"string","enum":["pending","in_progress","completed"]},"activeForm":{"type":"string","minLength":1}},"required":["content","status","activeForm"],"additionalProperties":false}}},"required":["todos"],"additionalProperties":false}</tool_use_error>
```

> AGENT

Let me skip formal todos and just work through it. First, check the GX pin and available env for the proof.

> TOOL

tool_use Bash
id: toolu_01Mp9RcP9c2BoaerTHGumWEM
```json
{
  "command": "grep -iE \"great.?expectations|pyiceberg|pyarrow|pandas\" backend/requirements.txt 2>/dev/null; echo \"=== conda envs ===\"; conda env list 2>/dev/null | grep -i dataq",
  "description": "Find GX/pyarrow pins and dataq conda env"
}
```

> TOOL

tool_result
id: toolu_01Mp9RcP9c2BoaerTHGumWEM
```
great-expectations==1.17.2
pyarrow==24.0.0                   # Parquet flat-file IO (read_parquet/profiler) — was a databricks-sql-connector transitive until its 4.x dropped it (#201)
=== conda envs ===
dataq                    /opt/homebrew/Caskroom/miniconda/base/envs/dataq
```

> AGENT

GX 1.17.2 + pyarrow 24 in the `dataq` env. I'll build an isolated venv for the proof so I don't touch the project env. First, check what `gx_runner` pulls in, so I can import it standalone in the proof:

> TOOL

tool_use Bash
id: toolu_0191udhP8Mni6sYPfUt6oRo6
```json
{
  "command": "sed -n '1,40p' backend/app/datasources/gx_runner.py | grep -nE \"^import|^from\"",
  "description": "Inspect gx_runner imports"
}
```

> TOOL

tool_result
id: toolu_0191udhP8Mni6sYPfUt6oRo6
```
16:from __future__ import annotations
18:from typing import Any
20:import great_expectations as gx
21:import great_expectations.expectations as gxe
23:from backend.app.datasources.base import CheckOutcome, CheckSpec, SuiteOutcome
```

> AGENT

`gx_runner` only needs GX + `base` (pydantic). Let me see `run_expectations`'s signature so the proof calls it exactly as the runners do:

> TOOL

tool_use Bash
id: toolu_013jVFhk15atDtxpbhMs6mNP
```json
{
  "command": "grep -nE \"def run_expectations|def to_suite_outcome\" backend/app/datasources/gx_runner.py; sed -n '/def run_expectations/,/-> SuiteOutcome:/p' backend/app/datasources/gx_runner.py | head -40",
  "description": "Show run_expectations signature"
}
```

> TOOL

tool_result
id: toolu_013jVFhk15atDtxpbhMs6mNP
```
116:def to_suite_outcome(gx_result: Any) -> SuiteOutcome:
170:def run_expectations(
def run_expectations(
    context: Any,
    *,
    batch_definition: Any,
    checks: list[CheckSpec],
    name: str,
    batch_parameters: dict[str, Any] | None = None,
    index_columns: list[str] | None = None,
) -> SuiteOutcome:
```

> AGENT

Noted the Deciders edit. Now the proof. Writing the script:

> TOOL

tool_use Write
id: toolu_01EJ7EMW7wRbUjDnorjmUr3L
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py",
  "content": "\"\"\"#286 spike proof — native pyiceberg read → DataQ's gx_runner, end to end.\n\nProves the ADR 0030 native path is viable *without any query engine or cloud*:\na real format-version-2 Iceberg table (local SQL catalog + filesystem warehouse),\nexercised through the mechanics a naive `read_parquet` would get WRONG —\n\n  * multiple snapshots (two appends → the scan must read only the current one),\n  * a row delete (the scan must not surface deleted rows),\n  * schema evolution (add a column → rows written before it read back as null,\n    reconciled by field-ID, not per-file physical schema),\n\nthen hands the pyiceberg `scan().to_pandas()` frame to the *actual repo code*\n`backend.app.datasources.gx_runner.run_expectations`, exactly as\n`FlatFileCheckRunner`/`UnityCatalogCheckRunner` do, and asserts a green suite.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport sys\nimport tempfile\nfrom pathlib import Path\n\nimport pyarrow as pa\nimport pyiceberg\nfrom pyiceberg.catalog.sql import SqlCatalog\nfrom pyiceberg.schema import Schema\nfrom pyiceberg.types import LongType, NestedField, StringType\n\n# Import the real DataQ integration point (repo on sys.path via PYTHONPATH).\nfrom backend.app.datasources.base import CheckSpec\nfrom backend.app.datasources.gx_runner import run_expectations\n\nimport great_expectations as gx\n\nprint(f\"pyiceberg      {pyiceberg.__version__}\")\nprint(f\"pyarrow        {pa.__version__}\")\nprint(f\"great_exp      {gx.__version__}\")\n\nwarehouse = Path(tempfile.mkdtemp(prefix=\"iceberg-proof-\"))\ncatalog = SqlCatalog(\n    \"proof\",\n    uri=f\"sqlite:///{warehouse}/catalog.db\",\n    warehouse=f\"file://{warehouse}\",\n)\ncatalog.create_namespace(\"retail\")\n\n# --- create a format-version 2 table ------------------------------------------\nschema = Schema(\n    NestedField(1, \"order_id\", LongType(), required=True),\n    NestedField(2, \"customer\", StringType(), required=False),\n)\ntable = catalog.create_table(\n    \"retail.orders\", schema=schema, properties={\"format-version\": \"2\"}\n)\nfmt_version = table.metadata.format_version\nprint(f\"\\ntable format-version = […]

> TOOL

tool_result
id: toolu_01EJ7EMW7wRbUjDnorjmUr3L
```
File created successfully at: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py (file state is current in your context — no need to Read it back)
```

> AGENT

The import warnings are expected (pyiceberg isn't installed yet). Now build the isolated venv and run the proof:

> TOOL

tool_use Bash
id: toolu_0168nMny78hzYLrmqkNA7Umt
```json
{
  "command": "cd /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad\npython3 -m venv iceberg-venv\n./iceberg-venv/bin/pip install --quiet --upgrade pip 2>&1 | tail -2\necho \"=== installing pyiceberg + GX pin (pip resolves pyarrow intersection) ===\"\n./iceberg-venv/bin/pip install \"pyiceberg[sql-sqlite,pyarrow]\" \"great-expectations==1.17.2\" pandas 2>&1 | tail -25",
  "description": "Create venv and install pyiceberg + GX",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_0168nMny78hzYLrmqkNA7Umt
```
=== installing pyiceberg + GX pin (pip resolves pyarrow intersection) ===
Using cached markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
Using cached mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Using cached markupsafe-3.0.3-cp313-cp313-macosx_11_0_arm64.whl (12 kB)
Downloading mistune-3.3.2-py3-none-any.whl (61 kB)
Downloading narwhals-2.23.0-py3-none-any.whl (458 kB)
Downloading numpy-2.5.1-cp313-cp313-macosx_14_0_arm64.whl (5.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/5.3 MB 101.0 MB/s  0:00:00
Using cached packaging-26.2-py3-none-any.whl (100 kB)
Using cached pyarrow-24.0.0-cp313-cp313-macosx_12_0_arm64.whl (35.0 MB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached referencing-0.37.0-py3-none-any.whl (26 kB)
Using cached rpds_py-2026.6.3-cp313-cp313-macosx_11_0_arm64.whl (338 kB)
Using cached ruamel_yaml-0.19.1-py3-none-any.whl (118 kB)
Downloading scipy-1.18.0-cp313-cp313-macosx_14_0_arm64.whl (20.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.4/20.4 MB 133.4 MB/s  0:00:00
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading tqdm-4.68.4-py3-none-any.whl (676 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 676.6/676.6 kB 34.8 MB/s  0:00:00
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading tzlocal-5.4.4-py3-none-any.whl (18 kB)
Using cached pycparser-3.0-py3-none-any.whl (48 kB)
Installing collected packages: pyroaring, zstandard, urllib3, tzlocal, typing-extensions, tqdm, tenacity, six, ruamel.yaml, rpds-py, pyparsing, pyiceberg-core, pygments, pycparser, pyarrow, packaging, numpy, narwhals, mmh3, mistune, mdurl, MarkupSafe, idna, fsspec, click, charset_normalizer, certifi, cachetools, attrs, annotated-types, typing-inspection, sqlalchemy, scipy, requests, referencing, python-dateutil, pydantic-core, marshmallow, markdown-it-py, jinja2, cffi, strictyaml, rich, pydantic, pandas, jsonschema-specifications, cryptography, pyiceberg, jsonschema, altair, great-expectations

Successfully installed MarkupSafe-3.0.3 altair-6.2.2 annotated-types-0.7.0 attrs-26.1.0 cachetools-6.2.6 certifi-2026.6.17 cffi-2.1.0 charset_normalizer-3.4.9 click-8.4.2 cryptography-49.0.0 fsspec-2026.6.0 great-expectations-1.17.2 idna-3.18 jinja2-3.1.6 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 markdown-it-py-4.2.0 marshmallow-3.26.2 mdurl-0.1.2 mistune-3.3.2 mmh3-5.2.1 narwhals-2.23.0 […]

> AGENT

pyiceberg **0.11.1** resolved cleanly alongside the repo's pinned **pyarrow 24.0.0** and **GX 1.17.2** — no version conflict (a key dependency-eval finding). Now run the proof:

> TOOL

tool_use Bash
id: toolu_01RFarmooavm9QymJsLGAqF9
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\nPYTHONPATH=/Users/arijit/Coding/Python/DataQ \\\n  /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/bin/python \\\n  /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py 2>&1 | grep -v \"WARNING\\|UserWarning\\|warnings.warn\"",
  "description": "Run the pyiceberg proof script"
}
```

> TOOL

tool_result
id: toolu_01RFarmooavm9QymJsLGAqF9
```
pyiceberg      0.11.1
pyarrow        24.0.0
great_exp      1.17.2

table format-version = 2
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ┃ Table field                  ┃ Dataframe field              ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ❌ │ 1: order_id: required long   │ 1: order_id: optional long   │
│ ✅ │ 2: customer: optional string │ 2: customer: optional string │
└────┴──────────────────────────────┴──────────────────────────────┘
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py", line 59, in <module>
    table.append(
    ~~~~~~~~~~~~^
        pa.table(
        ^^^^^^^^^
    ...<4 lines>...
        )
        ^
    )
    ^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/table/__init__.py", line 1427, in append
    tx.append(df=df, snapshot_properties=snapshot_properties, branch=branch)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/table/__init__.py", line 513, in append
    _check_pyarrow_schema_compatible(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self.table_metadata.schema(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        format_version=self.table_metadata.format_version,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/io/pyarrow.py", line 2749, in _check_pyarrow_schema_compatible
    _check_schema_compatible(requested_schema, provided_schema)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/schema.py", line 1714, in _check_schema_compatible
    pre_order_visit(requested_schema, _SchemaCompatibilityVisitor(provided_schema))
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniconda/base/envs/dataq/lib/python3.13/functools.py", line 934, in wrapper
    return dispatch(args[0].__class__)(*args, **kw)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/schema.py", line 945, in _
    return visitor.schema(obj, lambda: pre_order_visit(obj.as_struct(), visitor))
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/lib/python3.13/site-packages/pyiceberg/schema.py", line 1791, in schema
    raise ValueError(f"Mismatch in fields:\n{self.console.export_text()}")
ValueError: Mismatch in fields:
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ┃ Table field                  ┃ Dataframe field              ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ❌ │ 1: order_id: required long   │ 1: order_id: optional long   │
│ ✅ │ 2: customer: optional string │ 2: customer: optional string │
└────┴──────────────────────────────┴──────────────────────────────┘
```

> AGENT

`order_id` was declared `required` in Iceberg but pyarrow inferred it nullable — pyiceberg's schema check rejects the mismatch. I'll pin an explicit non-nullable pyarrow schema for the appends:

> TOOL

tool_use Edit
id: toolu_01LjVqHtDuteGEGib7kK45cr
```json
{
  "replace_all": false,
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py",
  "old_string": "fmt_version = table.metadata.format_version\nprint(f\"\\ntable format-version = {fmt_version}\")\nassert fmt_version == 2, f\"expected v2 table, got v{fmt_version}\"\n\n# --- snapshot 1: append 3 rows ------------------------------------------------\ntable.append(\n    pa.table(\n        {\"order_id\": pa.array([1, 2, 3], pa.int64()),\n         \"customer\": pa.array([\"ana\", \"ben\", \"cara\"], pa.string())}\n    )\n)\n# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)\ntable.append(\n    pa.table(\n        {\"order_id\": pa.array([4, 5], pa.int64()),\n         \"customer\": pa.array([\"dee\", \"eli\"], pa.string())}\n    )\n)",
  "new_string": "fmt_version = table.metadata.format_version\nprint(f\"\\ntable format-version = {fmt_version}\")\nassert fmt_version == 2, f\"expected v2 table, got v{fmt_version}\"\n\n# pyarrow schema matching the Iceberg one: order_id non-nullable (required).\npa_schema = pa.schema(\n    [pa.field(\"order_id\", pa.int64(), nullable=False),\n     pa.field(\"customer\", pa.string(), nullable=True)]\n)\n\n# --- snapshot 1: append 3 rows ------------------------------------------------\ntable.append(\n    pa.table(\n        {\"order_id\": [1, 2, 3], \"customer\": [\"ana\", \"ben\", \"cara\"]}, schema=pa_schema\n    )\n)\n# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)\ntable.append(\n    pa.table({\"order_id\": [4, 5], \"customer\": [\"dee\", \"eli\"]}, schema=pa_schema)\n)"
}
```

> TOOL

tool_result ERROR
id: toolu_01LjVqHtDuteGEGib7kK45cr
```
<tool_use_error>String to replace not found in file.
String: fmt_version = table.metadata.format_version
print(f"\ntable format-version = {fmt_version}")
assert fmt_version == 2, f"expected v2 table, got v{fmt_version}"

# --- snapshot 1: append 3 rows ------------------------------------------------
table.append(
    pa.table(
        {"order_id": pa.array([1, 2, 3], pa.int64()),
         "customer": pa.array(["ana", "ben", "cara"], pa.string())}
    )
)
# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)
table.append(
    pa.table(
        {"order_id": pa.array([4, 5], pa.int64()),
         "customer": pa.array(["dee", "eli"], pa.string())}
    )
)</tool_use_error>
```

> AGENT

The formatter reflowed the file. Let me read the affected region:

> TOOL

tool_use Read
id: toolu_01HfGoEPdgFQQnxT763VApwd
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py",
  "offset": 50,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01HfGoEPdgFQQnxT763VApwd
```
50	)
51	table = catalog.create_table(
52	    "retail.orders", schema=schema, properties={"format-version": "2"}
53	)
54	fmt_version = table.metadata.format_version
55	print(f"\ntable format-version = {fmt_version}")
56	assert fmt_version == 2, f"expected v2 table, got v{fmt_version}"
57	
58	# --- snapshot 1: append 3 rows ------------------------------------------------
59	table.append(
60	    pa.table(
61	        {
62	            "order_id": pa.array([1, 2, 3], pa.int64()),
63	            "customer": pa.array(["ana", "ben", "cara"], pa.string()),
64	        }
65	    )
66	)
67	# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)
68	table.append(
69	    pa.table(
70	        {
71	            "order_id": pa.array([4, 5], pa.int64()),
72	            "customer": pa.array(["dee", "eli"], pa.string()),
73	        }
74	    )
75	)
76	# --- snapshot 3: delete one row (a raw parquet read would still see order_id=2)
77	table.delete("order_id == 2")
78	# --- snapshot 4: evolve schema — add a column absent from earlier data files ---
79	with table.update_schema() as upd:
```

> TOOL

tool_use Edit
id: toolu_01BgeTUVgcUYY7XJipH5WwES
```json
{
  "replace_all": false,
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py",
  "old_string": "assert fmt_version == 2, f\"expected v2 table, got v{fmt_version}\"\n\n# --- snapshot 1: append 3 rows ------------------------------------------------\ntable.append(\n    pa.table(\n        {\n            \"order_id\": pa.array([1, 2, 3], pa.int64()),\n            \"customer\": pa.array([\"ana\", \"ben\", \"cara\"], pa.string()),\n        }\n    )\n)\n# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)\ntable.append(\n    pa.table(\n        {\n            \"order_id\": pa.array([4, 5], pa.int64()),\n            \"customer\": pa.array([\"dee\", \"eli\"], pa.string()),\n        }\n    )\n)",
  "new_string": "assert fmt_version == 2, f\"expected v2 table, got v{fmt_version}\"\n\n# pyarrow schema matching the Iceberg one: order_id non-nullable (required).\npa_schema = pa.schema(\n    [\n        pa.field(\"order_id\", pa.int64(), nullable=False),\n        pa.field(\"customer\", pa.string(), nullable=True),\n    ]\n)\n\n# --- snapshot 1: append 3 rows ------------------------------------------------\ntable.append(\n    pa.table(\n        {\"order_id\": [1, 2, 3], \"customer\": [\"ana\", \"ben\", \"cara\"]}, schema=pa_schema\n    )\n)\n# --- snapshot 2: append 2 more (a naive all-parquet glob would double-count s1)\ntable.append(\n    pa.table({\"order_id\": [4, 5], \"customer\": [\"dee\", \"eli\"]}, schema=pa_schema)\n)"
}
```

> TOOL

tool_result
id: toolu_01BgeTUVgcUYY7XJipH5WwES
```
The file /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01QQNZcZf31ypDCuVss7iL78
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\nPYTHONPATH=/Users/arijit/Coding/Python/DataQ \\\n  /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg-venv/bin/python \\\n  /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/scratchpad/iceberg_proof.py 2>&1 | grep -v \"WARNING\\|UserWarning\\|warnings.warn\\|MarshmallowWarning\\|return self.dispatch\"",
  "description": "Re-run the pyiceberg proof"
}
```

> TOOL

tool_result
id: toolu_01QQNZcZf31ypDCuVss7iL78
```
pyiceberg      0.11.1
pyarrow        24.0.0
great_exp      1.17.2

table format-version = 2
snapshots      = 3 (appends + delete)

scan().to_pandas() → 4 rows, order_id = [1, 3, 4, 5]
columns        = ['order_id', 'customer', 'channel']
✓ current snapshot only, delete applied, schema-by-id reconciled
Calculating Metrics:   0%|          | 0/23 [00:00<?, ?it/s]Calculating Metrics:   0%|          | 0/23 [00:00<?, ?it/s]Calculating Metrics:  17%|█▋        | 4/23 [00:00<00:00, 5277.51it/s]Calculating Metrics:  17%|█▋        | 4/23 [00:00<00:00, 4746.03it/s]Calculating Metrics:  26%|██▌       | 6/23 [00:00<00:00, 6718.05it/s]Calculating Metrics:  26%|██▌       | 6/23 [00:00<00:00, 6375.94it/s]Calculating Metrics:  43%|████▎     | 10/23 [00:00<00:00, 5602.12it/s]Calculating Metrics:  43%|████▎     | 10/23 [00:00<00:00, 5473.45it/s]Calculating Metrics: 100%|██████████| 23/23 [00:00<00:00, 6592.11it/s]Calculating Metrics: 100%|██████████| 23/23 [00:00<00:00, 6520.82it/s]Calculating Metrics: 100%|██████████| 23/23 [00:00<00:00, 6482.26it/s]Calculating Metrics: 100%|██████████| 23/23 [00:00<00:00, 6428.27it/s]

run_expectations → success=True, 3 checks
  ✓ expect_column_values_to_not_be_null
  ✓ expect_column_values_to_be_unique
  ✓ expect_column_values_to_be_in_set

✅ PROOF GREEN — native pyiceberg v2 read runs a DataQ suite end to end
```

> AGENT

Proof is **green**. It demonstrates exactly the three things a naive parquet read would get wrong: only the current snapshot (no double-count), the delete applied (`order_id=2` gone → `[1,3,4,5]`), and schema-by-ID reconciliation (added `channel` column reads null for pre-evolution rows) — then a green DataQ suite through the real `gx_runner`.

Now file the follow-ups and post findings. Let me check the milestone/label conventions:

> TOOL

tool_use Bash
id: toolu_01XfPt32bmbWdoViYPj298tH
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\necho \"=== open milestones ===\"; gh api repos/:owner/:repo/milestones --jq '.[] | \"\\(.number)\\t\\(.title)\"'\necho \"=== labels (subset) ===\"; gh label list 2>/dev/null | grep -iE \"enhancement|backlog|priority|datasource|tech\" | head",
  "description": "List milestones and labels"
}
```

> TOOL

tool_result
id: toolu_01XfPt32bmbWdoViYPj298tH
```
=== open milestones ===
4	v1.1 Backlog
11	v1.1 Week 2 — Portability: OTel logs, secrets lifecycle, dry-run depth
12	v1.1 Week 3 — Azure wind-down + local-first posture
13	v1.1 Week 4 — schema_drift monitor kind
14	v1.1 Week 5 — anomaly monitor kind + metric trends
15	v1.1 Week 6 — scale-aware execution + hardening + cycle close
16	v1.1 Week 7 — stretch (backlog burn-down)
=== labels (subset) ===
enhancement	New feature or request	#a2eeef
priority/P0	Urgent — blocks milestone or security	#b60205
priority/P1	High — do soon, milestone-adjacent	#d93f0b
priority/P2	Medium — important, not blocking	#fbca04
priority/P3	Low — polish / docs	#0e8a16
refactor	Code cleanup / dedup / tech-debt (no behavior change)	#c5def5
```

> AGENT

Milestone 4 (v1.1 Backlog) is the home for deferred follow-ups. Filing the native-build issue and a v3-revisit tracker:

> TOOL

tool_use Bash
id: toolu_01Yaaty6W8G5HpeQqNe6C3yu
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh issue create \\\n  --title \"Implement native Iceberg read: \\`IcebergCheckRunner\\` + self-contained \\`iceberg\\` connection (ADR 0030)\" \\\n  --milestone \"v1.1 Backlog\" \\\n  --label \"enhancement\" --label \"priority/P3\" \\\n  --body \"$(cat <<'EOF'\nBuild the native Apache Iceberg read path decided in **[ADR 0030](../blob/main/docs/adr/0030-iceberg-native-read-path.md)** and spiked in #286. Engine-level reads (Snowflake iceberg tables / Databricks foreign or UniForm catalog) already work with zero code under the existing `snowflake`/`unity_catalog` connections; this issue is the **native, no-query-engine** path.\n\n## Scope (v2 baseline)\n\n- [ ] Add `pyiceberg[pyarrow]` (+ the relevant catalog extra) to `backend/requirements.txt` with a pinned version and a CVE-surface check. **Spike-verified compatible:** `pyiceberg==0.11.1` resolves cleanly with the repo's pinned `pyarrow==24.0.0` and `great-expectations==1.17.2` (no pyarrow conflict) — #286.\n- [ ] `IcebergConnectionAdapter` (`backend/app/datasources/iceberg.py`) — **self-contained (Option A)**: catalog config (REST / SQL / Glue / Hive / Unity IRC) + warehouse/storage location + its **own** storage credential (single `secret_ref`). `validate_config` + a lightweight `test` (load catalog + `list_tables` or a metadata read).\n- [ ] `IcebergCheckRunner` — `catalog.load_table(...).scan().to_pandas()` → `gx_runner.run_expectations`, mirroring `UnityCatalogCheckRunner` (thin). The `table` arg carries `namespace.table`.\n- [ ] Register `iceberg` in `datasources/registry.py` (`_ADAPTERS` + `_RUNNER_BUILDERS`). No change to flat-file/SQL dispatch.\n- [ ] Column profiler dispatch for `iceberg` (reuse the `profile_dataframe` […]

> TOOL

tool_result
id: toolu_01Yaaty6W8G5HpeQqNe6C3yu
```
https://github.com/TheurgicDuke771/DataQ/issues/716
```

> TOOL

tool_use Bash
id: toolu_01Dh7Tz8oY7m7jrsjAKZXkM4
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh issue create \\\n  --title \"Revisit Iceberg v3 support (deletion vectors, row lineage) behind a capability gate — ADR 0030\" \\\n  --milestone \"v1.1 Backlog\" \\\n  --label \"enhancement\" --label \"priority/P3\" \\\n  --body \"$(cat <<'EOF'\nTracking issue from **[ADR 0030](../blob/main/docs/adr/0030-iceberg-native-read-path.md)** §2. The native Iceberg build (#716) ships **format-version 2** as the baseline. Iceberg **v3** — deletion vectors, row lineage, multi-arg/variant transforms — is deferred because engine support is uneven and `pyiceberg`'s v3 read path is still maturing.\n\n## When to pick this up\n\n- `pyiceberg` v3 read is GA/stable, **and**\n- the engines DataQ users actually read from (Snowflake, Databricks/UniForm, Spark) converge on v3.\n\nNote: Delta UniForm currently emits **v2** (`delta.enableIcebergCompatV2`) and is mutually exclusive with deletion vectors, so it stays in v2 territory regardless.\n\n## Scope when revisited\n\n- [ ] Gate v3-only features behind a capability flag on the `iceberg` connection (v2 remains the default/baseline).\n- [ ] Verify `pyiceberg` reads a v3 table with deletion vectors correctly into the DataFrame.\n- [ ] Docs: v2-vs-v3 capability matrix per engine.\n\nDepends on #716.\nEOF\n)\"",
  "description": "File Iceberg v3 revisit tracker"
}
```

> TOOL

tool_result
id: toolu_01Dh7Tz8oY7m7jrsjAKZXkM4
```
https://github.com/TheurgicDuke771/DataQ/issues/717
```

> AGENT

Now post the spike findings to #286 and close it:

> TOOL

tool_use Bash
id: toolu_01TAgxdCY1GYWne6442kcnbF
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh issue comment 286 --body \"$(cat <<'EOF'\n## Spike complete — decision recorded in ADR 0030, native read proven, closing\n\n### Outcome (both ACs met)\n\n**AC 1 — read path decided & recorded → [ADR 0030](../blob/main/docs/adr/0030-iceberg-native-read-path.md) (Accepted).** The spike answered two prior questions that collapse most of the scope:\n\n- **Engine-level read is free, zero-code.** `SnowflakeCheckRunner` (`add_table_asset` → SQL pushdown) and `UnityCatalogCheckRunner` (`read_sql_table` over the SQL Warehouse) talk SQL to the engine, never to the file format — so a Snowflake iceberg table or a Databricks foreign/UniForm catalog table is just another table under the existing `snowflake`/`unity_catalog` connection. **We deliberately did NOT stand up a Snowflake external volume / Databricks foreign catalog**: format-transparency is guaranteed by the code, so a live setup would only re-confirm it at real infra cost during the subscription wind-down. Zero decision value.\n- **An Iceberg table is not a parquet file** — it can't reuse `FlatFileCheckRunner` (which reads one object). The only genuinely new capability is a **native `pyiceberg` read directly from object storage, no query engine**: `catalog.load_table(...).scan().to_pandas()` → the existing `gx_runner`.\n- **v2 baseline, v3 deferred** (uneven engine support + maturing pyiceberg v3). **Connection model = Option A self-contained** (`iceberg` type owns […]

> TOOL

tool_result
id: toolu_01TAgxdCY1GYWne6442kcnbF
```
https://github.com/TheurgicDuke771/DataQ/issues/286#issuecomment-4911693071
✓ Closed issue TheurgicDuke771/DataQ#286 (Post-v1: Apache Iceberg v2 / v3 table format support)
```

> AGENT

Spike closed. Now update the progress tracker to reflect the closed spike + new ADR + follow-ups:

> TOOL

tool_use Bash
id: toolu_01ATAr8phXChUnzygJxnkvR5
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ; grep -n \"#286\\|Iceberg\" docs/progress.md",
  "description": "Find #286 references in progress.md"
}
```

> TOOL

tool_result
id: toolu_01ATAr8phXChUnzygJxnkvR5
```
27:| **Open issues** | **52** (W2 2026-07-07 — **W2 exit gate MET 14/14** + **4 in-week follow-ups cleared** (#571 [#699](https://github.com/TheurgicDuke771/DataQ/pull/699) run-detail checks_total graft, #640 [#700](https://github.com/TheurgicDuke771/DataQ/pull/700) flaky test, #643 [#701](https://github.com/TheurgicDuke771/DataQ/pull/701) stale-policy event, #605 [#702](https://github.com/TheurgicDuke771/DataQ/pull/702) redaction-safe run failure_reason); **#286 Iceberg deferred to its own session**. Earlier: **#488 closed via [#695](https://github.com/TheurgicDuke771/DataQ/pull/695)** — workspace-admin workspace-wide visibility threaded into the MCP list/aggregate tools + `schedule_service.list_schedules`/`/schedules` (ADR-0027 REST parity; admin+non-admin authz tests); **#584 closed** — MCP NL tool-selection spot-check passed against live `/mcp` (VS Code Copilot Agent mode + W1 PAT routed all 4 canonical queries correctly, no docstring misses); **#532 closed via [#697](https://github.com/TheurgicDuke771/DataQ/pull/697)** — dry-run preview extended to all datasources via the `build_check_runner` registry + server-side target resolution (2-reviewer agentic review, 500→502 regression + batch-UI gap fixed in-PR). Earlier, W2 2026-07-05 — **alerting batch**: #386 (dedup severity single-source) + #387 (suppression guard) + #388 (alert_on drift-guard) closed via [#656](https://github.com/TheurgicDuke771/DataQ/pull/656); #389 closed won't-fix (Slack/email publishers made the per-channel name correct); **#655 closed via [#657](https://github.com/TheurgicDuke771/DataQ/pull/657)** — one canonical `db.models.SEVERITY_RANK` + `FAILING_TIERS` + shared `worst_severity()` helper (converged the 3 rank maps + the builder/run_service worst-severity loops); **#416 closed via [#659](https://github.com/TheurgicDuke771/DataQ/pull/659)** — enriched Slack/email alerts (deep link + metadata + expected-vs-observed via a shared pure […]

> TOOL

tool_use Read
id: toolu_012sabyN2qduXaGAqd6sPDdy
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "offset": 274,
  "limit": 8
}
```

> TOOL

tool_result
id: toolu_012sabyN2qduXaGAqd6sPDdy
```
274	| ⬜ | [#433](https://github.com/TheurgicDuke771/DataQ/issues/433) Compliance G3: warehouse-tag PII classification (Snowflake source lapses W1 — UC tags remain) | Theme 4 |
275	| ⬜ | [#434](https://github.com/TheurgicDuke771/DataQ/issues/434) Compliance G4: region/residency assertion | Theme 4 |
276	| ⬜ | [#435](https://github.com/TheurgicDuke771/DataQ/issues/435) Compliance G5: encryption-at-rest in IaC + CMK (partially blocked post-#590 — no cloud IaC target) | Theme 4 |
277	| ⬜ | [#529](https://github.com/TheurgicDuke771/DataQ/issues/529) MCP tool expansion — tier-1 read-only set (week-sized) | Theme 13 |
278	| ⬜ | [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) Apache Iceberg v2/v3 table-format support (spike first) | Theme 2 |
279	| ⬜ | [#244](https://github.com/TheurgicDuke771/DataQ/issues/244) Suite-on-suite triggering | Theme 8 |
280	| ⬜ | [#466](https://github.com/TheurgicDuke771/DataQ/issues/466) Interactive datasource browsing (ADLS half blocked post-Azure; S3 + UC picker remain) | Theme 8 |
281	| ⬜ | [#505](https://github.com/TheurgicDuke771/DataQ/issues/505) AWS/GCP deploy IaC (blocked until a target cloud subscription exists) | Theme 14 |
```

> TOOL

tool_use Edit
id: toolu_0188yFu2yZNsLjx7ARgiiTh8
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "old_string": "| ⬜ | [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) Apache Iceberg v2/v3 table-format support (spike first) | Theme 2 |",
  "new_string": "| ✅ | [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) Apache Iceberg — **spike DONE 2026-07-07** (ADR [0030](adr/0030-iceberg-native-read-path.md): engine-level read is free/zero-code; native `pyiceberg` v2 read is the only new build, proven green end-to-end; self-contained `iceberg` connection). Native build → [#716](https://github.com/TheurgicDuke771/DataQ/issues/716), v3 revisit → [#717](https://github.com/TheurgicDuke771/DataQ/issues/717) | Theme 2 |"
}
```

> TOOL

tool_result
id: toolu_0188yFu2yZNsLjx7ARgiiTh8
```
The file /Users/arijit/Coding/Python/DataQ/docs/progress.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_018561mugzyjm9aWfPgxwXAr
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "old_string": "#605 [#702](https://github.com/TheurgicDuke771/DataQ/pull/702) redaction-safe run failure_reason); **#286 Iceberg deferred to its own session**.",
  "new_string": "#605 [#702](https://github.com/TheurgicDuke771/DataQ/pull/702) redaction-safe run failure_reason); **#286 Iceberg spike DONE 2026-07-07** (ADR 0030 — engine-level read free/zero-code, native `pyiceberg` v2 read proven green, self-contained `iceberg` connection; native build → #716, v3 revisit → #717)."
}
```

> TOOL

tool_result
id: toolu_018561mugzyjm9aWfPgxwXAr
```
The file /Users/arijit/Coding/Python/DataQ/docs/progress.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

The hook flags snapshot-count consistency. Let me get the real open-issue count and update the header note + count:

> TOOL

tool_use Bash
id: toolu_01VEYBoo3ZrE5nReAmjMenud
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ; gh issue list --state open --limit 500 --json number --jq 'length'",
  "description": "Count open issues"
}
```

> TOOL

tool_result
id: toolu_01VEYBoo3ZrE5nReAmjMenud
```
54
```

> TOOL

tool_use Edit
id: toolu_01FYEoj26uQ1AHi8jsCVj2AM
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "old_string": "| **Open issues** | **52** (W2 2026-07-07 — **W2 exit gate MET 14/14**",
  "new_string": "| **Open issues** | **54** (W2 2026-07-07 — **W2 exit gate MET 14/14**"
}
```

> TOOL

tool_result
id: toolu_01FYEoj26uQ1AHi8jsCVj2AM
```
The file /Users/arijit/Coding/Python/DataQ/docs/progress.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the W2 section header and the in-week follow-up note (lines 150/152):

> TOOL

tool_use Edit
id: toolu_01A47E4oxYN3jWayAQ92QwnR
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "old_string": "**exit gate MET (14/14 tracked)**; 4 of 5 in-week follow-ups cleared (#571/#640/#643/#605), #286 deferred",
  "new_string": "**exit gate MET (14/14 tracked)**; 4 of 5 in-week follow-ups cleared (#571/#640/#643/#605), #286 spike closed (ADR 0030)"
}
```

> TOOL

tool_result
id: toolu_01A47E4oxYN3jWayAQ92QwnR
```
The file /Users/arijit/Coding/Python/DataQ/docs/progress.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01583AaKAjYqYLGPYTwf6cpG
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/progress.md",
  "old_string": "**#286 (Iceberg v2/v3) deferred to its own focused session** — it needs a `pyiceberg` dependency eval + an ADR and touches the unsettled two-connection model (ADR 0015); still open on the W2 milestone.",
  "new_string": "**#286 (Iceberg v2/v3) spike DONE 2026-07-07** in its own focused session → **ADR [0030](adr/0030-iceberg-native-read-path.md)**: engine-level read (Snowflake/UC iceberg tables) is free & zero-code; the only new build is a native `pyiceberg` **v2** read (proven green end-to-end in an isolated venv — snapshot/delete/schema-evolution all correctly resolved; `pyiceberg==0.11.1` compat with the pinned pyarrow 24/GX 1.17.2), behind a **self-contained** `iceberg` connection (Option A; Option B two-connection ref deferred to ADR 0015). Native build → [#716](https://github.com/TheurgicDuke771/DataQ/issues/716), Iceberg-v3 revisit → [#717](https://github.com/TheurgicDuke771/DataQ/issues/717)."
}
```

> TOOL

tool_result
id: toolu_01583AaKAjYqYLGPYTwf6cpG
```
The file /Users/arijit/Coding/Python/DataQ/docs/progress.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Let me check whether the cycle epic #597 tracks #286 in a checklist:

> TOOL

tool_use Bash
id: toolu_01AMg6gJFuXvVb5BfoPN96aS
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ; gh issue view 597 --json body --jq '.body' | grep -n \"286\" || echo \"no #286 reference in epic #597\"",
  "description": "Check epic #597 for #286 reference"
}
```

> TOOL

tool_result
id: toolu_01AMg6gJFuXvVb5BfoPN96aS
```
16:- [ ] #286 (Iceberg v2 ADLS spike — pulled forward from W7 stretch 2026-07-04)
78:- [ ] #286 (Iceberg table format)
```

> TOOL

tool_use Bash
id: toolu_01CW3qC3iWNRphrXoSnqVx3a
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\nbody=$(gh issue view 597 --json body --jq '.body')\nprintf '%s' \"$body\" \\\n  | sed 's/- \\[ \\] #286 (Iceberg v2 ADLS spike — pulled forward from W7 stretch 2026-07-04)/- [x] #286 (Iceberg v2 spike DONE 2026-07-07 — ADR 0030; native build #716, v3 #717)/' \\\n  | sed 's/- \\[ \\] #286 (Iceberg table format)/- [x] #286 (Iceberg spike DONE — ADR 0030; native build → #716)/' \\\n  | gh issue edit 597 --body-file -\necho \"epic updated\"; gh issue view 597 --json body --jq '.body' | grep -n \"286\"",
  "description": "Tick #286 in epic #597 checklist"
}
```

> TOOL

tool_result
id: toolu_01CW3qC3iWNRphrXoSnqVx3a
```
https://github.com/TheurgicDuke771/DataQ/issues/597
epic updated
16:- [x] #286 (Iceberg v2 spike DONE 2026-07-07 — ADR 0030; native build #716, v3 #717)
78:- [x] #286 (Iceberg spike DONE — ADR 0030; native build → #716)
```

> AGENT

Everything's done. Here's the close-out summary.

## #286 Iceberg spike — DONE, closed

**Local pyiceberg proof — green** (isolated scratchpad venv, no cloud, no query engine, project env untouched):
- Real **format-version 2** Iceberg table via a local SQL catalog + filesystem warehouse.
- Deliberately exercised the three things a naive parquet-glob gets **wrong** — pyiceberg handled all three: two appends → **current snapshot only** (no double-count); `DELETE order_id=2` → scan omits it (`[1,3,4,5]`); schema evolution (add `channel`) → **reconciled by field-ID**, null for pre-evolution rows.
- The resulting frame ran through the **real repo code** `gx_runner.run_expectations` (same shape as `FlatFileCheckRunner`/`UnityCatalogCheckRunner`) → **3/3 checks green**.
- **Dependency finding:** `pyiceberg==0.11.1` resolves cleanly with the repo's pinned `pyarrow==24.0.0` + `great-expectations==1.17.2` — no conflict.

**Follow-ups filed:**
- **[#716](https://github.com/TheurgicDuke771/DataQ/issues/716)** — implement native `IcebergCheckRunner` + self-contained `iceberg` connection (the deferred build), v1.1 Backlog.
- **[#717](https://github.com/TheurgicDuke771/DataQ/issues/717)** — revisit Iceberg v3 behind a capability gate, v1.1 Backlog.

**Closed:** [#286](https://github.com/TheurgicDuke771/DataQ/issues/286) with a full findings comment (decision, proof output, dep finding, Delta-UniForm note).

**Docs updated (unstaged):**
- [docs/adr/0030-iceberg-native-read-path.md](docs/adr/0030-iceberg-native-read-path.md) + index row in [docs/adr/README.md](docs/adr/README.md)
- [docs/progress.md](docs/progress.md) — snapshot count 52→54, W2 section, backlog row all reflect the closed spike
- Epic [#597](https://github.com/TheurgicDuke771/DataQ/issues/597) checklist ticked for #286

This is a docs-only […]

> DEVELOPER

when we are using `catalog.load_table(...).scan().to_pandas()` we are using pyarrow as engine, right?

> AGENT

Yes — for `.to_pandas()`, **PyArrow is the read/compute engine**. Worth being precise about the layering, because it also confirms the ADR's "no query engine" claim isn't contradicted:

## What each layer does in `load_table().scan().to_pandas()`

| Step | Who does it |
|---|---|
| `load_table()` | Catalog resolves the current **metadata.json** → table metadata |
| `.scan()` | pyiceberg **planning** — evaluates the snapshot's manifests to pick which data files + delete files to read, prunes by partition/row filter. Pure Python + the Rust `pyiceberg-core` for manifest/delete evaluation. **No data read yet.** |
| `.to_arrow()` | **PyArrow** reads the selected parquet data files (`pyarrow.dataset`), applies residual filters, applies positional/equality **deletes**, projects to the current schema → an Arrow table |
| `.to_pandas()` | `= to_arrow().to_pandas()` — Arrow→pandas is just a zero-ish-copy container conversion; pandas is **not** the engine |

So the actual columnar work — reading parquet, applying deletes, schema projection — is **PyArrow**. That's exactly why the proof installed `pyiceberg[pyarrow]` and why pyarrow-24 compatibility mattered.

## Important: PyArrow ≠ a "query engine" in the ADR's sense

The ADR's "no query engine in the loop" means no **remote warehouse service** (Snowflake / Databricks SQL Warehouse) resolving the table and running SQL. […]

> DEVELOPER

okay in #716 keep an option b/w .to_arrow_batch_reader() and .to_arrow() and mention not directly use scan().to_pandas [or is it nor correct approach?] 
Also move #716 to week 3.

> AGENT

Good refinement — and yes, it's the correct approach. Quick judgment before I make the edits:

**Is avoiding bare `scan().to_pandas()` correct? Yes, for two concrete reasons:**
1. **dtype fidelity.** `.to_pandas()` is a convenience shortcut for `.to_arrow().to_pandas()` with default (numpy) dtypes — which silently loses Arrow nullability/types. `FlatFileCheckRunner` deliberately reads parquet with `dtype_backend="pyarrow"` ([flatfile.py:118](backend/app/datasources/flatfile.py#L118)), so going through `.to_arrow()` explicitly and mapping to Arrow-backed pandas dtypes keeps Iceberg's GX behavior **consistent with the flat-file runner** (integer nullability, null handling).
2. **It's the materialization seam.** `.to_arrow()` (full) vs `.to_arrow_batch_reader()` (streamed) is exactly where you choose whole-table vs out-of-core.

**One caveat to bake in:** GX's expectation path needs the **whole** frame in memory (row-count/uniqueness are exact — can't stream), so for expectation checks the batch reader still ends up materializing everything; its real payoff is the **monitor path** (freshness/volume = scalar aggregates, streamable) and sampled profiling. I'll write it that way.

Let me update #716 and move it to Week 3:

> TOOL

tool_use Bash
id: toolu_01PfhcSVVj6ZimeFKbQ9fqrB
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh issue edit 716 --milestone \"v1.1 Week 3 — Azure wind-down + local-first posture\" --body \"$(cat <<'EOF'\nBuild the native Apache Iceberg read path decided in **[ADR 0030](../blob/main/docs/adr/0030-iceberg-native-read-path.md)** and spiked in #286. Engine-level reads (Snowflake iceberg tables / Databricks foreign or UniForm catalog) already work with zero code under the existing `snowflake`/`unity_catalog` connections; this issue is the **native, no-query-engine** path.\n\n## Scope (v2 baseline)\n\n- [ ] Add `pyiceberg[pyarrow]` (+ the relevant catalog extra) to `backend/requirements.txt` with a pinned version and a CVE-surface check. **Spike-verified compatible:** `pyiceberg==0.11.1` resolves cleanly with the repo's pinned `pyarrow==24.0.0` and `great-expectations==1.17.2` (no pyarrow conflict) — #286.\n- [ ] `IcebergConnectionAdapter` (`backend/app/datasources/iceberg.py`) — **self-contained (Option A)**: catalog config (REST / SQL / Glue / Hive / Unity IRC) + warehouse/storage location + its **own** storage credential (single `secret_ref`). `validate_config` + a lightweight `test` (load catalog + `list_tables` or a metadata read).\n- [ ] `IcebergCheckRunner` — `catalog.load_table(...).scan()` → DataFrame → `gx_runner.run_expectations`, mirroring `UnityCatalogCheckRunner` (thin). The `table` arg carries `namespace.table`. **Materialization — do NOT use the bare `scan().to_pandas()` shortcut** (see note below).\n- [ ] Register `iceberg` in `datasources/registry.py` (`_ADAPTERS` + `_RUNNER_BUILDERS`). No change to flat-file/SQL dispatch.\n- [ ] Column profiler dispatch for `iceberg` (reuse […]

> TOOL

tool_result
id: toolu_01PfhcSVVj6ZimeFKbQ9fqrB
```
https://github.com/TheurgicDuke771/DataQ/issues/716
--- verify ---
Implement native Iceberg read: `IcebergCheckRunner` + self-contained `iceberg` connection (ADR 0030)
→ v1.1 Week 3 — Azure wind-down + local-first posture
```

> AGENT

#716 updated and now on **v1.1 Week 3**. I left #717 (v3 revisit) in Backlog since it's a "when the ecosystem converges" tracker, not week-scheduled — say the word if you want it moved too.

One coherence fix: the ADR's Decision still illustrates the shape as `scan().to_pandas()`, which now contradicts #716's "never the bare `.to_pandas()`" guidance. Let me align the ADR so the two docs don't drift:

> TOOL

tool_use Read
id: toolu_0179BAtJthKb5gq7QQhgAwP2
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md",
  "offset": 20,
  "limit": 5
}
```

> TOOL

tool_result
id: toolu_0179BAtJthKb5gq7QQhgAwP2
```
20	### 1. Add native Iceberg as a new datasource; keep engine-level reads as the free zero-code path
21	
22	- **Engine-level (Snowflake iceberg table / Databricks foreign or UniForm catalog) — supported now, no code.** Documented as the "already works" path; it costs the engine's warehouse compute and only exposes what the engine surfaces as SQL.
23	- **Native `pyiceberg` — the new build.** `IcebergCheckRunner` reads a table via `pyiceberg` (`catalog.load_table(...).scan().to_pandas()`) and hands the frame to `gx_runner.run_expectations` — thin, like `UnityCatalogCheckRunner`. Payoff over engine-level: **no warehouse compute**, and **direct access to snapshot + schema history** — the natural feed for the reserved `freshness` / `schema_drift` monitor kinds (ADR 0012).
24	
```

> TOOL

tool_use Edit
id: toolu_01288sUBC7nC3zxXRrUn75bX
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md",
  "old_string": "- **Native `pyiceberg` — the new build.** `IcebergCheckRunner` reads a table via `pyiceberg` (`catalog.load_table(...).scan().to_pandas()`) and hands the frame to `gx_runner.run_expectations` — thin, like `UnityCatalogCheckRunner`. Payoff over engine-level: **no warehouse compute**, and **direct access to snapshot + schema history** — the natural feed for the reserved `freshness` / `schema_drift` monitor kinds (ADR 0012).",
  "new_string": "- **Native `pyiceberg` — the new build.** `IcebergCheckRunner` reads a table via `pyiceberg` (`catalog.load_table(...).scan()`) and hands the frame to `gx_runner.run_expectations` — thin, like `UnityCatalogCheckRunner`. Materialize via `.to_arrow()` → Arrow-backed pandas (**not** the bare `.to_pandas()` shortcut, which drops to numpy dtypes — keep parity with `FlatFileCheckRunner`'s `dtype_backend=\"pyarrow\"`) for the exact-expectation path; use `.to_arrow_batch_reader()` for the streamable monitor/aggregate path. See #716 for the materialization detail. Payoff over engine-level: **no warehouse compute**, and **direct access to snapshot + schema history** — the natural feed for the reserved `freshness` / `schema_drift` monitor kinds (ADR 0012)."
}
```

> TOOL

tool_result
id: toolu_01288sUBC7nC3zxXRrUn75bX
```
The file /Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
id: toolu_01Mu6UbHLiB33WTdwuA9PEGN
```json
{
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md",
  "offset": 54,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01Mu6UbHLiB33WTdwuA9PEGN
```
54	- **Positive:** DataQ "supports Iceberg" *today* at the engine level with no code. The native path, when built, is a thin runner behind the proven seams (more evidence ADR 0011 holds) and unlocks no-warehouse reads plus the snapshot/schema-history feed for `freshness`/`schema_drift` (ADR 0012). Delta **UniForm** tables come along for free: they publish Iceberg v2 metadata over the same parquet files, readable via Unity Catalog's Iceberg REST Catalog — so the native `pyiceberg` path reaches Delta tables (read-only) without a Databricks warehouse. Caveats for UniForm: Iceberg **v2 only**, **no deletion vectors** (mutually exclusive with UniForm), and **async metadata lag** (the Iceberg snapshot trails the latest Delta commit — `converted_delta_version`/`converted_delta_timestamp` track how far).
55	- **Negative / cost:** the native build adds a `pyiceberg` runtime dependency (CVE-surface + version pin to evaluate before it enters `requirements.txt`), a new `IcebergConnectionAdapter` + `IcebergCheckRunner`, a spec-driven connection form (catalog type + warehouse URL + auth), and duplicated storage credentials vs. an existing ADLS/S3 connection (the Option A trade). Whole-snapshot `to_pandas()` is memory-bound like the flat-file/UC DataFrame paths — same scale ceiling (G-b scale-aware execution, post-v1).
56	- **Neutral / deferred:** the native runner is **not built this cycle**. This ADR […]

> TOOL

tool_use Edit
id: toolu_014Ej1LUf6Y5aK4DTnxH2VSZ
```json
{
  "replace_all": false,
  "file_path": "/Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md",
  "old_string": "Whole-snapshot `to_pandas()` is memory-bound like the flat-file/UC DataFrame paths — same scale ceiling (G-b scale-aware execution, post-v1).",
  "new_string": "The exact-expectation path materializes the whole snapshot (via `.to_arrow()`), memory-bound like the flat-file/UC DataFrame paths — same scale ceiling (G-b scale-aware execution, post-v1); `.to_arrow_batch_reader()` is the streaming escape hatch for the monitor/aggregate path (#716)."
}
```

> TOOL

tool_result
id: toolu_014Ej1LUf6Y5aK4DTnxH2VSZ
```
The file /Users/arijit/Coding/Python/DataQ/docs/adr/0030-iceberg-native-read-path.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done. Summary of this round:

- **#716** — added a **Read-materialization note** and updated the runner checklist item. It now specifies:
  - **`.to_arrow()` → Arrow-backed pandas** (matching `FlatFileCheckRunner`'s `dtype_backend="pyarrow"`) for the **expectation-check** path — GX needs the full frame, so it materializes the whole table.
  - **`.to_arrow_batch_reader()`** for the streamable **monitor/aggregate** path (freshness/volume scalars) and sampled profiling — the memory escape hatch for G-b.
  - **Never the bare `scan().to_pandas()`** convenience call (drops Arrow dtypes, hides the materialization seam).
  - Moved to **v1.1 Week 3**.
- **ADR 0030** — aligned the Decision bullet and the memory-ceiling consequence with that same guidance, so the ADR and #716 don't drift.
- **#717** (v3 revisit) — left in Backlog as a convergence tracker (not moved).

Your call on whether it's actually *incorrect* to use `.to_pandas()`: it's not *wrong*, it just works — but it's the inferior default (numpy dtypes, no batch seam), so treating it as "don't use directly" is the right engineering call, exactly as you framed it.

Docs still unstaged (ADR 0030 + README index + progress.md). Want me to branch and commit the doc set now, or leave it for review?

> DEVELOPER

branch, commit and merge the doc set

> TOOL

tool_use Bash
id: toolu_01FetEYsoRgqBC5wRLAx7rFn
```json
{
  "command": "git status --short && echo \"=== branch ===\" && git branch --show-current",
  "description": "Check git status and current branch"
}
```

> TOOL

tool_result
id: toolu_01FetEYsoRgqBC5wRLAx7rFn
```
 M docs/adr/README.md
 M docs/progress.md
?? docs/adr/0030-iceberg-native-read-path.md
=== branch ===
main
```

> AGENT

Clean three-file doc set. Branching, committing, and pushing:

> TOOL

tool_use Bash
id: toolu_019FTZT3jigHQyXJUTwfdBUm
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngit checkout -b docs/adr-0030-iceberg-spike\ngit add docs/adr/0030-iceberg-native-read-path.md docs/adr/README.md docs/progress.md\ngit commit -m \"$(cat <<'EOF'\ndocs: ADR 0030 — Iceberg spike outcome (native pyiceberg v2 read path)\n\nClose the #286 Iceberg spike. Records the decision: engine-level reads\n(Snowflake iceberg tables / Databricks foreign or UniForm catalog) are free\nand zero-code; the only new build is a native pyiceberg v2 read behind a thin\nIcebergCheckRunner (scan → Arrow-backed DataFrame → gx_runner), fronted by a\nself-contained `iceberg` connection type (Option A — own catalog + storage\ncredential; Option B two-connection ref deferred to ADR 0015). v2 baseline,\nv3 deferred. Native path proven green end-to-end in the spike (snapshot,\ndelete, and schema-evolution all correctly resolved; pyiceberg 0.11.1 compat\nwith pinned pyarrow 24 / GX 1.17.2). Also reads Delta UniForm (read-only).\n\nNative build tracked in #716 (v1.1 Week 3), Iceberg v3 revisit in #717.\n\n- add docs/adr/0030-iceberg-native-read-path.md + index row\n- progress.md: #286 spike closed, snapshot count 52→54, W2 section\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nEOF\n)\"\ngit push -u origin docs/adr-0030-iceberg-spike 2>&1 | tail -5",
  "description": "Create branch, commit doc set, push"
}
```

> TOOL

tool_result
id: toolu_019FTZT3jigHQyXJUTwfdBUm
```
Switched to a new branch 'docs/adr-0030-iceberg-spike'
[docs/adr-0030-iceberg-spike 22f95708] docs: ADR 0030 — Iceberg spike outcome (native pyiceberg v2 read path)
 3 files changed, 75 insertions(+), 4 deletions(-)
 create mode 100644 docs/adr/0030-iceberg-native-read-path.md
remote:      https://github.com/TheurgicDuke771/DataQ/pull/new/docs/adr-0030-iceberg-spike        
remote: 
To github.com:TheurgicDuke771/DataQ.git
 * [new branch]        docs/adr-0030-iceberg-spike -> docs/adr-0030-iceberg-spike
branch 'docs/adr-0030-iceberg-spike' set up to track 'origin/docs/adr-0030-iceberg-spike'.
```

> AGENT

Pushed clean. Now open the PR (with milestone per repo convention) and squash-merge:

> TOOL

tool_use Bash
id: toolu_0124efeMxqm3yBHxLnUdU39D
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh pr create --title \"docs: ADR 0030 — Iceberg spike outcome (native pyiceberg v2 read path)\" \\\n  --milestone \"v1.1 Week 2 — Portability: OTel logs, secrets lifecycle, dry-run depth\" \\\n  --body \"$(cat <<'EOF'\nCloses the #286 Apache Iceberg spike (docs-only — no code touched).\n\n## What's here\n\n- **ADR [0030](../blob/docs/adr-0030-iceberg-spike/docs/adr/0030-iceberg-native-read-path.md)** (Accepted; native impl deferred) + index row. Records:\n  - **Engine-level read is free, zero-code** — Snowflake iceberg tables / Databricks foreign or UniForm catalog are just tables under the existing `snowflake`/`unity_catalog` connections (SQL runners are format-transparent). We deliberately did **not** stand up an external volume / foreign catalog — zero decision value at real infra cost during wind-down.\n  - **Native `pyiceberg` v2 read** is the only new build: thin `IcebergCheckRunner` (`scan()` → Arrow-backed DataFrame → `gx_runner`), materialized via `.to_arrow()` for expectations and `.to_arrow_batch_reader()` for monitors (never bare `.to_pandas()`).\n  - **Self-contained `iceberg` connection (Option A)** — own catalog + storage credential; independent lifecycle, cascade-safe. Option B (two-connection ref) deferred to ADR 0015.\n  - **v2 baseline, v3 deferred.** Reads Delta **UniForm** too (read-only, v2, async lag).\n- **progress.md** — #286 spike marked done, snapshot count 52→54, W2 section + backlog row updated.\n\n## Spike evidence\n\nNative v2 read proven green […]

> TOOL

tool_result
id: toolu_0124efeMxqm3yBHxLnUdU39D
```
https://github.com/TheurgicDuke771/DataQ/pull/718
```

> AGENT

PR [#718](https://github.com/TheurgicDuke771/DataQ/pull/718) created. Enabling squash auto-merge (main requires CI green) and deleting the branch on merge:

> TOOL

tool_use Bash
id: toolu_0175uctZDfmpJNmEHk77jBaS
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh pr merge 718 --squash --auto --delete-branch 2>&1 | tail -3\necho \"=== checks ===\"; sleep 5; gh pr checks 718 2>&1 | head -20",
  "description": "Enable squash auto-merge and show checks"
}
```

> TOOL

tool_result
id: toolu_0175uctZDfmpJNmEHk77jBaS
```
=== checks ===
Backend — dependency audit (pip-audit)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923854	
Backend — lint & format	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923863	
Backend — tests	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923867	
Backend — type check	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923833	
CodeQL analysis (javascript-typescript)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923923	
CodeQL analysis (python)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923843	
Frontend — browser E2E (Playwright)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923845	
Frontend — lint & format	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923850	
Frontend — tests	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923841	
Secret scanning (betterleaks)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923851	
Backend — SAST (Bandit)	pass	13s	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923844	
Frontend — dependency audit (pnpm audit)	pending	0	https://github.com/TheurgicDuke771/DataQ/actions/runs/28920975000/job/85797923837	
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com
```

> AGENT

Auto-merge is enabled; CI is running (Bandit + GitGuardian already green, the rest pending). It'll squash-merge automatically once the required checks pass. The hook's "PR merged" note is premature — it fired on the merge *command*, but `--auto` queues the merge behind CI rather than merging immediately. Let me confirm the queue state:

> TOOL

tool_use Bash
id: toolu_01QMr6v9wN93WMqzugJqTYyB
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngh pr view 718 --json state,autoMergeRequest,mergeStateStatus --jq '{state, autoMerge: (.autoMergeRequest.mergeMethod // \"OFF\"), mergeState: .mergeStateStatus}'",
  "description": "Confirm auto-merge queue state"
}
```

> TOOL

tool_result
id: toolu_01QMr6v9wN93WMqzugJqTYyB
```
{"autoMerge":"SQUASH","mergeState":"BLOCKED","state":"OPEN"}
```

> AGENT

Auto-merge (SQUASH) is correctly queued — `BLOCKED` just means it's waiting on the required checks, which is expected for a fresh PR. It'll merge itself on green. Let me watch it to completion rather than leave it hanging:

> TOOL

tool_use Bash
id: toolu_01LnQUncBYCRHunbnR3RRHB2
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\nfor i in $(seq 1 24); do\n  state=$(gh pr view 718 --json state --jq '.state')\n  if [ \"$state\" != \"OPEN\" ]; then echo \"PR 718 state=$state after ~$((i*30))s\"; break; fi\n  sleep 30\ndone\necho \"=== final ===\"\ngh pr view 718 --json state,mergedAt,mergeCommit --jq '{state, mergedAt, mergeCommit: .mergeCommit.oid}'\necho \"=== any failed checks ===\"; gh pr checks 718 2>/dev/null | grep -iE \"fail|cancel\" || echo \"none failed\"",
  "description": "Poll until PR 718 merges or fails",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01LnQUncBYCRHunbnR3RRHB2
```
Command running in background with ID: bkbsarx4b. Output is being written to: /private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/tasks/bkbsarx4b.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

I've queued a background watcher on the PR. Here's where things stand:

**Done:**
- Branch `docs/adr-0030-iceberg-spike` created, doc set committed (ADR 0030 + README index + progress.md), pushed.
- PR [#718](https://github.com/TheurgicDuke771/DataQ/pull/718) opened (on the v1.1 Week 2 milestone).
- **Squash auto-merge enabled** with branch auto-delete — it will merge the moment required CI goes green (Bandit + GitGuardian already passed; backend/frontend lint+tests, E2E, CodeQL, secret-scan, dep-audits still running).

The background watcher polls until it merges (or flags any failed check), and I'll report back when it lands. No action needed from you — it's a docs-only change, so I expect a clean green merge. If any check fails I'll surface it and fix rather than leave it stuck.

> TOOL

tool_use Read
id: toolu_01R3si2W3ex5v5oanuoeRePw
```json
{
  "file_path": "/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/8bb76f13-05da-451c-ab08-dc5056bf7a39/tasks/bkbsarx4b.output"
}
```

> TOOL

tool_result
id: toolu_01R3si2W3ex5v5oanuoeRePw
```
1	PR 718 state=MERGED after ~180s
2	=== final ===
3	{"mergeCommit":"2483ec17fc0edc9b6015aa6be21a18674406aed7","mergedAt":"2026-07-08T05:59:41Z","state":"MERGED"}
4	=== any failed checks ===
5	none failed
6	
```

> AGENT

Merged cleanly — no failed checks. Let me sync local `main` and confirm the branch is gone:

> TOOL

tool_use Bash
id: toolu_016Z7b9ehEvdskWGxEFHnaNx
```json
{
  "command": "cd /Users/arijit/Coding/Python/DataQ\ngit checkout main -q && git pull --ff-only -q 2>&1 | tail -2\necho \"=== on main, recent ===\"; git log --oneline -3\necho \"=== local branch cleanup ===\"; git branch -d docs/adr-0030-iceberg-spike 2>&1 || echo \"(already gone)\"",
  "description": "Sync local main and clean up branch"
}
```

> TOOL

tool_result
id: toolu_016Z7b9ehEvdskWGxEFHnaNx
```
=== on main, recent ===
2483ec17 docs: ADR 0030 — Iceberg spike outcome (native pyiceberg v2 read path) (#718)
634dba33 test(frontend): de-flake SchedulesPanel delete-confirm (AntD modal motion race, #714) (#715)
83031b01 docs(site): fill remaining gaps — tutorial, security, REST API, deployment, troubleshooting, changelog (#713)
=== local branch cleanup ===
warning: deleting branch 'docs/adr-0030-iceberg-spike' that has been merged to
         'refs/remotes/origin/docs/adr-0030-iceberg-spike', but not yet merged to HEAD
Deleted branch docs/adr-0030-iceberg-spike (was 22f95708).
```

> AGENT

✅ **Merged and cleaned up.** Squash-commit `2483ec17` is on `main`, local synced, feature branch deleted (both remote via `--delete-branch` and local).

## #286 Iceberg spike — fully closed out

| Item | State |
|---|---|
| **ADR 0030** | On `main` — decision recorded (engine-level free/zero-code · native `pyiceberg` v2 the only new build · self-contained `iceberg` connection Option A · v2 baseline / v3 deferred · reads Delta UniForm) |
| **Native pyiceberg proof** | Green end-to-end — snapshot/delete/schema-evolution correctly resolved → 3/3 GX checks via real `gx_runner`; `pyiceberg 0.11.1` ✓ pyarrow 24 / GX 1.17.2 |
| **#286** | Closed (findings comment posted) |
| **#716** | Filed — native runner + `iceberg` connection, with the `.to_arrow()` / `.to_arrow_batch_reader()` materialization guidance → **v1.1 Week 3** |
| **#717** | Filed — Iceberg v3 revisit → Backlog |
| **Epic #597** | Checklist ticked for #286 |
| **PR #718** | Squash-merged, CI all green, branch deleted |

The only remaining Iceberg work is now the deferred build in #716 (Week 3) and the v3 tracker in #717 — nothing outstanding from this session.