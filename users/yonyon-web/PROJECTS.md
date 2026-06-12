# Projects — yonyon-web

## yonyon-web/sodateru-wiki ★ (dominant — 100% of sessions)

**What it is**: A wiki / article-creation support tool, internal project name `記事作成支援ツール4` (Article Creation Support Tool, version 4). "Sodateru" (育てる) means "to grow/nurture" — the tool is framed as helping users develop and manage structured wiki articles over time.

**Target users**: Non-engineers. The user explicitly designs the UI to avoid technical jargon (`エンジニア用語をUI上にできるだけ出さないようにしたい`).

**Tech stack**:
- Frontend: **Svelte** (`web-ui/src/lib/components/SpreadsheetTable.svelte` is the central UI component)
- Backend: **Node.js** (API routes, `+server.ts`, reset scripts)
- Storage: **Markdown files** under `wiki/` (one file per row, identified by UUID)
- Data: JSON files under `data/` (e.g., `data/tables.json`)
- Config: `CLAUDE.md` at project root

**Recurring themes in sessions**:
1. **Spreadsheet-like table UI**: editing rows, adding ghost rows, saving behavior, cell layout.
2. **Attribute system**: user-defined columns with types (text, number, select, image); adding description and example fields to attributes; attribute ordering.
3. **Image attributes**: uploading new images or selecting existing ones for attribute values.
4. **Data reset**: `reset.js` script to restore `data/` and `wiki/` to initial state.
5. **UX polish for non-engineers**: removing engineer-facing labels, fixing layout shift, taming input behavior.
6. **Identity / naming**: moved from `name`-based row identity to UUID-based, removing the `名前` column from the spreadsheet UI.

**Path pattern seen**: `/home/yonyon/dev/記事作成支援ツール4/`
