[DEVELOPER]: When reply is done, 1. If timeline page, scroll to top and refresh 2. For post/article detail page, and succeeded optimistically append

[AGENT]: Fresh branch. Let me read the key files to understand the current reply flow.

[AGENT]: Starting implementation. Let me update the GraphQL mutation first.

[AGENT]: Now update the repository's createNote to map the full post.

[AGENT]: Now wire it into ComposeViewModel to emit on reply success.

[AGENT]: Now wire the signal into PostDetailViewModel.

[AGENT]: Clear locals on refresh so the server-authoritative replies list wins.

[AGENT]: Now update PostDetailScreen to render the local replies after the paged items.

[AGENT]: Update PostDetailContent signature and rendering.

[AGENT]: Let me check existing tests for PostDetailViewModel and ComposeViewModel to see if they'll break.

[AGENT]: Now update ComposeViewModelTest to include the new dependency.

[AGENT]: Now let's verify the build.

[AGENT]: Build passes. Now run the tests.

[AGENT]: Build passed (`:app:assembleDebug`) and tests passed (`:app:testDebugUnitTest`) including 3 new ones I added. **Summary of changes** - Timeline behavior unchanged: a successful compose already fires `TimelineRefreshTrigger` → paging-source invalidate + scroll-to-top. - New for post/article detail: - `CreateNote` mutation now returns `...PostFields`, so the client has a full `Post` for the new reply (actor, mentions, engagement, etc.). `HackersPubRepository.createNote` now maps via `PostFields.toPost()`. - New singleton `ReplyPostedSignal` (DI-scoped `SharedFlow<ReplyPostedEvent>`) at `app/src/main/java/pub/hackers/android/ui/screens/compose/ReplyPostedSignal.kt`. - `ComposeViewModel` emits `ReplyPostedEvent(replyTargetId, newPost)` on success when `replyToId != null`. - `PostDetailViewModel` collects the signal, filters by its own `postId`, appends to `locallyAddedReplies: StateFlow<List<Post>>`, and bumps `engagementStats.replies`. `refresh()` clears the local list so the server list wins. - `PostDetailScreen` renders `localReplies` in an additional `items(...)` block after the paged replies, keyed as `"local-${id}"` to avoid duplicate-key collisions with a future server-returned copy. - Updated `PostDetailViewModelTest` (new signal param + 3 tests) and `ComposeViewModelTest` (new signal param).