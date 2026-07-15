> DEVELOPER

hey it seems like the tooltip is not  working well for the nodes hovering but it workd sfor the edges can you invesitgate. for nodes it just has placehomlser values

> AGENT

I found the bug. In `frontend/explorer_export.js`, the node hover tooltip in the exported HTML reads `n.baseline_p` and `n.posterior_p` straight off the Cytoscape `data` object — but `buildElements()` in `explorer_graph.js` (lines 584-603) only stores those fields nested under `data.raw`. So `n.baseline_p` / `n.posterior_p` are always `undefined`, the details line stays empty, and the tooltip only shows the (often truncated) `shortLabel` + `type` — i.e. the "placeholder" you're seeing.

By contrast, the edge weights in the driver/indicator tables use plain HTML `title=` on `<td>` cells (lines 123, 173) — that's why edge-related hovers look fine.

Two handlers are affected:
- `explorer_export.js:469-481` (single-question export)
- `explorer_export.js:857-871` (question-set export — also references `n.questionId`, which is at `n.raw.data.question_id`)

Want me to fix both handlers to read from `n.raw` (e.g. `n.raw?.baseline_p`, `n.raw?.posterior_p`, `n.raw?.label`, `n.raw?.data?.question_id`)? Or would you prefer I push the prior/posterior fields up onto the Cytoscape `data` object in `buildElements()` so both the live graph and the export see them uniformly?

> DEVELOPER

what is better practice.

> AGENT

Promoting the fields onto `data` in `buildElements()` is the better practice, for three reasons:

1. **`data` is Cytoscape's public surface.** Styles, selectors, `cy.json()` serialization, and any downstream consumer (live tooltip, export, future features) all read from `data`. `raw` is an escape hatch for "give me the whole record"; it shouldn't be the primary read path for common fields like prior/posterior.

2. **Decouples view from backend schema.** If the backend renames `baseline_p` → `prior_p`, you change one place (`buildElements`) instead of every consumer that drills into `raw.baseline_p`.

3. **Avoids shipping the full raw payload in exports.** Right now `raw: n` is serialized into the exported HTML via `cy.json().elements`. That's bloat and potentially leaks fields the export didn't intend to expose (provenance, internal flags, etc.). With a proper view-model on `data`, you can drop `raw` from the export snapshot.

Concrete shape — add `baseline_p`, `posterior_p`, and `questionId` to the node `data` block in `buildElements()` (explorer_graph.js:586-602), then the export tooltips work without changes. Optional follow-up: strip `raw` from elements before serializing in `exportQuestionHTML`/`exportQuestionSetHTML`.

Want me to make that change?

> DEVELOPER

yeah go fo ri t

> AGENT

Now let me strip `raw` from the elements before serializing into the export blobs, so we don't ship the full backend payload.

> AGENT

Now add the `stripRawFromElements` helper near the top of the file.

> AGENT

Done. Summary of changes:

- **`frontend/explorer_graph.js:597-602`** — Promoted `baseline_p`, `posterior_p`, and `questionId` onto the Cytoscape node `data` object in `buildElements()`. These are now the view-model fields any consumer (live graph, export, future features) reads from.
- **`frontend/explorer_export.js`** — Added a small `stripRawFromElements()` helper that removes the `raw` backend payload from node/edge data before serializing into the exported HTML, applied at both `buildExportHTML` (single question) and `buildQuestionSetExportHTML` (question set). The existing tooltip handlers (`n.baseline_p`, `n.posterior_p`, `n.questionId`) now resolve correctly because those fields live on `data`.

The live graph keeps `raw` for click-to-inspect; only the export drops it. Smoke-test by opening a question, exporting the HTML, and hovering a driver/indicator node — you should now see `Prior: X% · Posterior: Y%` (and the question id in question-set exports).

> DEVELOPER

can you put it up on the wireframe for me to test

> AGENT

A couple of things to sort before I can put it in front of you:

1. **Worktree isolation.** I made the edits in this worktree (`velvet-sprouting-creek`), not the main repo. Any dev server running against the main checkout won't see the changes.
2. **No running stack here.** Docker daemon isn't running locally and I don't see a dev server on port 8000.

How do you normally test? A couple of options:

- **Local Docker dev**: I can start the daemon (if you confirm) and run `docker compose -f compose.dev.yml up` against this worktree, then you hit `http://localhost:8000/`.
- **Local Python only**: Run the API directly via `uv run uvicorn services.api.app:create_app --factory --reload --port 8000` — assumes a Postgres is reachable.
- **Betty**: Push a branch and pull it on Betty, then reload your browser there.
- **Just open the worktree's HTML files in a browser**: won't work — they need the API for question data.

Which do you want? If you want local Docker, I'll need you to start Docker Desktop first (I can't launch the macOS app).

> DEVELOPER

just make a PR it's fine mate

> AGENT

Changes preserved cleanly in `frontend/legacy/`. Running pre-push checks now.

> AGENT

Hold on — let me stop the test run and check.

> AGENT

Yes — and that's a problem. On `dev`, the frontend was reorganised (PR #300): `frontend/` now has `analyst/`, `bet-pricer/`, `tuning/`, and the old explorer code moved to `frontend/legacy/`. My worktree branch was based on an older revision where the files still lived at `frontend/explorer_*.js`, so when I rebased onto dev the rename auto-merged my edits into `legacy/`.

Let me find where the explorer/tooltip lives in the new layout.

> AGENT

Found the real bug. In `frontend/analyst/index.html:3063-3065`, the node hover handler does:

```js
const raw = ensureNodeInfo(event.target.data("raw")) || event.target.data();
```

But `ensureNodeInfo()` (line 1609) returns `rawNode.data.node_info` — the side-panel info block, *not* the raw node. So `nodeHoverHtml(raw)` then reads `raw.baseline_p`, `raw.posterior_p`, `raw.type`, `raw.label`, `raw.evidence_ids` off the empty `node_info` object — hence the placeholder values. The edge handler on line 3068 doesn't wrap with `ensureNodeInfo`, so edges show correctly.

Let me revert the legacy edits, fix the real file, and reset the branch.

> AGENT

Clean. Now apply the real fix.

> AGENT

Done — and apologies for the legacy detour. The real fix is one line in `frontend/analyst/index.html`: the node hover handler was wrapping the raw node in `ensureNodeInfo()` (which returns the side-panel `node_info` block, not the raw node), so `nodeHoverHtml()` was reading `baseline_p` / `posterior_p` / `type` / `label` off the wrong object. Edges worked because the edge handler didn't apply the same wrapper.

Draft PR: https://github.com/elijahintelligence/elijah/pull/329 — targets `dev`, `@kungfusaini` tagged, ready for you to smoke-test by hovering a driver/indicator node.

> TOOL

<bash-input>pwd</bash-input>

> TOOL

<bash-stdout>/Users/sumeet/matrix/elijah/.claude/worktrees/velvet-sprouting-creek</bash-stdout><bash-stderr></bash-stderr>
