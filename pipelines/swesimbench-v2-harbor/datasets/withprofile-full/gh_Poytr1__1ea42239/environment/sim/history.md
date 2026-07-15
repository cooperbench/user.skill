[DEVELOPER]: Hi

[AGENT]: Hi! How can I help you today?

[DEVELOPER]: Can you help me change the "Semantic release" concept directly into "AI Report", product side changes backend can keep the same but need to document

[AGENT]: Let me explore what needs to change on the product/frontend side.

[AGENT]: Good findings. The main changes are in `en.json` (i18n strings) and the notification title template. Let me make the product-facing changes.

[AGENT]: Now I'll make all the changes. The i18n file has the bulk of user-facing strings, plus I need to update the Slack notification title template in the orchestrator.

[AGENT]: Now let me update the notification title template in the orchestrator — this is user-facing (appears in Slack/email notifications).

[AGENT]: Now let me check if there's a zh (Chinese) i18n file that also needs updating.

[AGENT]: Let me update the Chinese translations too. "AI 报告" is the natural Chinese translation for "AI Report".

[AGENT]: Now I'll batch the remaining zh.json edits. Let me read the relevant lines first.

[AGENT]: All product-facing changes are done. Here's a summary: **Files changed:** - `web/lib/i18n/messages/en.json` — 17 strings: "Semantic Release(s)" → "AI Report(s)" across breadcrumbs, dashboard, releases tab, project settings, SR list/detail/delete dialogs, subscription form - `web/lib/i18n/messages/zh.json` — 17 matching strings: "语义发布" → "AI 报告" - `internal/agent/orchestrator.go:523` — notification title: "Semantic Release Report: %s %s" → "AI Report: %s %s" **Backend kept as-is:** API routes (`/semantic-releases`), DB table/column names, Go type names (`SemanticRelease`), internal error messages, and test assertions all remain unchanged — only the user-facing label changed. **Not changed (intentionally):** `todo.typeSemantic: "Semantic"` — this is a short type badge, not the full "Semantic Release" concept. Let me know if you want that changed too (e.g. to "AI").