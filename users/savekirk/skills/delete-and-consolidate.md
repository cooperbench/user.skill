---
name: delete-and-consolidate
description: Directs the agent to remove a module, tree view, or file and consolidate its function elsewhere (usually into package.json manifest or existing VS Code commands). Trigger when the agent has created a custom abstraction that duplicates a native VS Code mechanism.
---

# Delete and Consolidate

savekirk pushes back hard on code the agent added that duplicates something the platform already provides. The correction pattern is:
1. Name what to remove ("Get rid of...", "do away with...", "remove")
2. State where the behavior should live instead (package.json `viewsWelcome`, existing vscode commands)
3. No preamble or softening

This reflects an architectural preference: declarative manifest config over imperative TypeScript where VS Code supports it.

**Verbatim examples**:

> "Use `viewsWelcome` in package.json for empty views and do away with src/components/emptyViews.ts"

> "Get rid of the Recovery tree view and any related codebase since the options are exposed as vscode commands that can be triggered by the user already."

> "Use the viewsWelcome for session and checkpoint in package.json based on the `EntireWorkspaceState` and get rid of the versions in src/components/checkpointTreeView.ts and src/components/activeSessionTreeView.ts"

The target file or class is always named explicitly. References to `package.json` as the correct home are common.
