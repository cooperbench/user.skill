[DEVELOPER]: See ../hackerspub implementation, we already have articledetail query. in this case, we need to also render toc. Could you do it?

[AGENT]: Now let me verify specific files before designing the approach.

[AGENT]: Let me check how JSON is currently used in Apollo-generated code.

[AGENT]: JSON maps to `Any`. Now let me look at how PostDetail is fetched in the repository and ViewModel, to understand how to plumb the TOC data.

[AGENT]: Let me look at the outer PostDetail screen caller and the end of PostDetailContent to understand structure.

[AGENT]: Now I have a complete picture. Let me outline my plan before I start making changes. ## Plan **Data flow:** Fetch `toc` JSON via `... on Article { contents { toc } }` → parse in repository into `List<TocItem>` → surface on `PostDetailUiState`. **Scroll mechanism:** Split heading tags into their own `ContentBlock.Heading(level, id, html)` so each heading becomes its own composable. Attach a `Modifier.bringIntoViewRequester(...)` per heading. The TOC keeps a `Map<String, BringIntoViewRequester>` and calls `bringIntoView()` on click — this works through LazyColumn because BringIntoViewRequester traverses scroll parents. **UI:** Collapsible TOC section above the article body, recursive indentation. I'll implement each step, running a build at the end to verify. Starting with the GraphQL query.

[AGENT]: Let me clean up by merging into a single `... on Post` block.

[AGENT]: Now verify the GraphQL query compiles by running the apollo codegen.

[AGENT]: `toc` generated as `Any`, and `contents: List<Content>`. Now let me check the shape — the access path and `Content.language` / `Content.toc`.

[AGENT]: Now let me create the TocItem model and parser.

[AGENT]: Now add the JSON parser in the repository's mapper layer.

[AGENT]: Now let me update the repository to parse TOC and include it in PostDetailResult.

[AGENT]: Now add the `parseTocJson` helper at the bottom of the repository file.

[AGENT]: Now wire TOC through to the UI state.

[AGENT]: Now on to the HtmlContent and the TOC composable. Let me update HtmlContent to split headings out and expose anchor hooks.

[AGENT]: Now I'll add the Heading block type, split logic, and rendering. Let me make these additions.

[AGENT]: Now add the heading-splitting regex and a function that takes a Text block and splits out Heading blocks.

[AGENT]: Now add the heading-splitting function and wire it into `splitIntoBlocks`.

[AGENT]: Now render the `Heading` block. The rendering should be a Text with heading size, optionally wrapped with `bringIntoViewRequester`. I need to add a parameter to `HtmlContent` to accept a supplier of `BringIntoViewRequester` per anchor id.

[AGENT]: Now add the `Heading` block rendering case.

[AGENT]: Now update `blockSpacing` to give headings top spacing.

[AGENT]: Now the collapsible TOC composable + integration in PostDetailContent.

[AGENT]: Now let me create the `TocPanel` composable.

[AGENT]: Good. Now wire TocPanel into `PostDetailContent` and supply the heading-anchor map.

[AGENT]: Acknowledged — I'll add tests after finishing the integration. Continuing.

[AGENT]: Now add the anchor map and render TocPanel above the article body.

[AGENT]: Understood — I'll scope the heading split to only run when TOC anchors are in use (i.e. article detail). Let me gate the splitting.

[AGENT]: Now let me build to verify it all compiles.

[AGENT]: Build succeeds. All warnings are pre-existing. Now let me address the user's test request. Let me look at existing test structure.

[AGENT]: Now let me add tests for heading-splitting and TOC parsing. First the HtmlContent tests:

[AGENT]: Let me extract the TOC parser into its own testable file.

[AGENT]: Now remove the duplicate parser from the repository and use the new one.

[AGENT]: Now let's verify: existing `PostDetailContentTest` uses the old signature — it needs the new `toc` param. Let me check and fix.

[AGENT]: Now run the tests.

[AGENT]: All tests pass. Let me run the PostDetailContent test too to confirm the signature change didn't break anything.

[AGENT]: Let me run the full test suite to make sure nothing else regressed.

[AGENT]: All tests pass. Let me give a final summary. ## Summary Added TOC support for article detail, matching the web implementation. **Data:** - `operations.graphql:377` — added `... on Article { contents { language, toc } }` to PostDetail. - `domain/model/Models.kt:247` — new `TocItem(id, level, title, children)`; `PostDetailResult` gains `toc`. - `domain/model/TocParser.kt` — new recursive parser from Apollo's JSON `Any` → `List<TocItem>`. - `HackersPubRepository.kt:228` — pulls `onArticle.contents.first().toc` and parses it. - `PostDetailViewModel.kt` — `toc` on `PostDetailUiState`, surfaced from load + refresh. **UI:** - `HtmlContent.kt` — new `ContentBlock.Heading(level, anchorId, innerHtml)`. `splitIntoBlocks(splitHeadings = true)` now extracts `<h1-6>` into separate blocks with their `id=` attribute. Each heading gets `Modifier.bringIntoViewRequester` when an anchor is supplied. Splitting is opt-in so notes/replies are unchanged. - `components/TocPanel.kt` — collapsible list mirroring web layout; taps call `BringIntoViewRequester.bringIntoView()` to scroll to heading. - `PostDetailScreen.kt` — TOC rendered only when `isArticle && toc.isNotEmpty() && !showTranslated`; anchors passed to `HtmlContent` only for articles. **Tests:** - `TocParserTest.kt` — 8 cases (null/empty/flat/nested/missing-fields/numeric-variants/missing-children). - `HtmlContentKtTest.kt` — 5 new cases covering opt-out default, extraction with id, missing id, multiple headings, heading + code block interaction. - `PostDetailContentTest.kt` — updated call site with `toc = emptyList()`. All unit tests pass. Build compiles clean.

[AGENT]: Now launch the three review agents in parallel.

[AGENT]: Aggregating findings. Applying the following fixes: 1. Use existing `parseAttributes` helper instead of new `ID_ATTR_REGEX` (reuse) 2. Delete unreachable empty-Text fallback in Heading rendering (quality) 3. Drop unused `language` field from GraphQL query (efficiency) 4. `remember` the heading TextStyle per (bodyStyle, level) (efficiency) 5. `remember` `items.minOf` in TocPanel (efficiency) 6. `remember` the `anchorRequester` lambda (efficiency) 7. Add a depth guard to `parseTocJson` (quality) Skipping: TocEntry/RenderListBlock generic refactor (too invasive for the win), `parseTocJson` merging with `toJsonValue` (opposite direction), and switching the anchor map to `mutableStateMapOf` (plain map is intentional — we don't want heading registration to trigger TocPanel recompositions). **Fix 1: Use `parseAttributes` for heading id extraction.**

[AGENT]: **Fix 2 + 4: Delete unreachable fallback and `remember` the heading style.**

[AGENT]: **Fix 3: Drop unused `language` from the GraphQL query.**

[AGENT]: **Fix 5: `remember` `items.minOf` in TocPanel.**

[AGENT]: **Fix 6: `remember` the anchorRequester lambda.**

[AGENT]: **Fix 7: Add depth guard to parseTocJson.**

[AGENT]: Now verify with build + tests.

[AGENT]: All tests pass. ## Summary of fixes **Applied:** - `HtmlContent.kt` — removed duplicate `ID_ATTR_REGEX`; reused existing `parseAttributes()` to extract heading `id`. Wrapped heading `TextStyle.copy(...)` in `remember(bodyStyle, block.level)`. Deleted unreachable empty-Text fallback branch. - `TocPanel.kt` — hoisted `items.minOf { it.level }` into a `remember(items)` block. - `PostDetailScreen.kt` — stabilized the `anchorRequester` lambda via `remember(post.id)` and dropped the extra wrapping lambda at the HtmlContent call site. - `operations.graphql` — dropped unused `language` field from `contents`. - `TocParser.kt` — added `MAX_TOC_DEPTH = 16` recursion guard. **Skipped (deliberately):** - Extracting a generic recursive list renderer shared between `TocEntry` and `RenderListBlock` — the two have meaningfully different layouts (indent vs marker + hanging indent) and the abstraction would cost more than it saves. - Unifying `parseTocJson` with `toJsonValue/toJsonString` — they traverse in opposite directions (decode vs encode), not true duplicates. - Switching the anchor map to `mutableStateMapOf` — plain `mutableMapOf` is intentional; observing it would trigger unnecessary recompositions when headings register themselves. Build clean, tests green.