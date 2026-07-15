> DEVELOPER

Fix a bug where nested-scrolling is not available in bottomsheet

> AGENT

I see the setup. The TOC work is on `feature/article-detail-toc` (9 commits ahead of main), but the current branch `fix/article-toc-scrolling` sits at main with no TOC code. To fix the bottom-sheet scrolling, I need the TOC sheet code present. The TOC bottom sheet is here: ```kotlin if (showTocSheet && tocAvailable) { ModalBottomSheet(...) { Column( modifier = Modifier .navigationBarsPadding() .padding(horizontal = 16.dp, vertical = 12.dp) ) { Text(...) TocList(items = uiState.toc, ...) } } } ``` The `Column` holding `TocList` has no `verticalScroll` — long TOCs get clipped and can't be scrolled, which matches "nested-scrolling not available in bottom sheet." Before I proceed, how would you like me to base this fix? Options: 1. Rebase `fix/article-toc-scrolling` onto `feature/article-detail-toc` (fix sits on top of the TOC PR) 2. Wait until `feature/article-detail-toc` merges to main, then fix from main 3. Merge `feature/article-detail-toc` into this branch Option 1 is cleanest if the TOC PR is still open. Which do you want?