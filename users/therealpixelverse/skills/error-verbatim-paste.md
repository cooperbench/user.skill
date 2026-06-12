---
name: error-verbatim-paste
description: "Trigger: something breaks in the browser console, ClickHouse, or GitHub CI. User pastes the raw error with one short line of intro or none. No diagnosis attempted."
---

When something breaks, this user pastes the full raw error text with minimal or zero framing. The intro line (if any) is a single short sentence naming the location. No attempt at root-cause analysis. No question mark. The error speaks for itself.

**ClickHouse error format**:
> "I am getting this in clickhouse: Error\nUnknown expression or function identifier `PROJECT_KEY_EXPR` in scope (SELECT if(count() > 0, any(if(git_remote != '', arrayElement(splitByChar('/', git_remote), -1)..."

> "I am getting this in clickhouse PROJECT_KEY_EXPR"
(even shorter when the error is known)

**React/browser console format**:
> "I am gettin gthis error when loading projects Uncaught ReferenceError: ChartLegend is not defined\n    at content (ProjectTrendChart.tsx:303:10)\n    at Object.react_stack_bottom_frame..."

> "Getting this when lopading dashboard [plugin:vite:react-babel] /Users/rafa/Obsession/rudel/apps/web/src/components/charts/DimensionAnalysisChart.tsx: Unexpected token (293:7)"

**GitHub CI format**:
> "Got this error in github Error:  command finished with error: command (/home/runner/_work/***/***/) /home/runner/.bun/bin/bun run lint exited (1)\n@***/web:check-types\n..."

**Screenshot + URL format** (when UI is empty or visually wrong):
> "dashboard still empty [Image #1] http://localhost:4011/dashboard?from=2026-02-26&to=2026-03-05"

**Do not**: add "I think the issue is..." or ask "can you fix this?". Just intro + paste.
