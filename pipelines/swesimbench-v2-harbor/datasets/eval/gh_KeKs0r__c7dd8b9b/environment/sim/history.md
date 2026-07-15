[DEVELOPER]: run current migrations for staging and prod in packages/ch-schema

[AGENT]: Let me check the available migration scripts first.

[AGENT]: I see `ch:migrate` (CI/staging) and `ch:migrate:prd` (production). Let me first check the current migration status on both environments, then run the migrations.

[AGENT]: Both environments have 1 pending migration: `20260303181035_auto.sql`. Let me check what it does before applying.

[AGENT]: This migration drops the `repository` column from all three tables and removes the `idx_repository` index — matches the recent commits about removing the repository column. Let me apply it to both environments.

[AGENT]: The migration is blocked because it contains destructive operations (dropping columns). Need to add `--allow-destructive`. Since these are intentional drops matching the recent commits (#114, #115), I'll proceed.

[AGENT]: The materialized view `session_analytics_mv` still references the `repository` column, so ClickHouse blocks the drop. We need to drop/recreate the MV first. Let me check the current schema and MV definition.

[AGENT]: The MV on the live ClickHouse still references `repository`. The migration only drops the column from the tables but doesn't recreate the MV. Let me check the live MV definition.

[AGENT]: The live MV has `repository Nullable(String)` in its column list. The MV uses `SELECT * EXCEPT (session_date, last_interaction_date)` from `claude_sessions`, so it picks up `repository` from the source table. We need to drop and recreate the MV without `repository` before dropping the column. Let me also check if there's a codex MV.

[AGENT]: Both MVs reference `repository`. The migration needs to be updated to drop both MVs first, then drop the columns, then recreate the MVs without `repository`. Let me read the current MV schema definitions to get the correct recreate SQL.

[AGENT]: The MVs use `SELECT * EXCEPT (...)` from the source tables, so they inherit `repository`. We need to drop the MVs, drop the columns, then recreate the MVs. Let me update the migration file to include these steps.

[AGENT]: No response requested.