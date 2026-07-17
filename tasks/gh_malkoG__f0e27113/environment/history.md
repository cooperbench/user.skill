> DEVELOPER

Add edit button for article detail page

> TOOL

tool_use Bash
id: toolu_01DAX4VHLpvR9X48QENKov4d
```json
{
  "command": "pwd && ls",
  "description": "Show working directory and contents"
}
```

> TOOL

tool_result
id: toolu_01DAX4VHLpvR9X48QENKov4d
```
/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality
app
docs
fastlane
gradle
metadata
build.gradle.kts
CONVENTION.md
gradle.properties
gradlew
gradlew.bat
LICENSE
README.md
settings.gradle.kts
```

> TOOL

tool_use Bash
id: toolu_01MANQmNhGhkWHbP65iF9vnD
```json
{
  "command": "git log --oneline -20",
  "description": "Recent git history"
}
```

> TOOL

tool_result
id: toolu_01MANQmNhGhkWHbP65iF9vnD
```
231c0a7 Merge pull request #130 from malkoG/fix/search-ux
ef85a5e Merge pull request #129 from malkoG/fix/bottom-padding-for-post-detail
e4d1ae0 pass locales to searchPost
ab72025 Show link preview on post detail
8256344 Add bottom padding to post detail list
9e129fb Merge pull request #128 from malkoG/feature/profile-edit
581ec91 Add EditProfileViewModel tests
aa97b0d fan out all search buckets on Enter so chip switches are instant
d3c9e83 Add Edit Profile entry point and navigation wiring
7f77c9b Wire avatar picker + data URL conversion
8ccf0fb add All chip that renders Actors and Posts sections
f3d24be Build EditProfileScreen UI for name, bio, links
ef8ba8e tighten vertical padding in search header
38e54f2 Add EditProfileViewModel
88c660a Add repository methods for editable account
19e7869 add People/Posts/Tags filter chips to search
4463b50 Add UpdateAccount mutation and EditAccount query
6b5808b reserve trailing slot in search bar to prevent height jump
70dff94 Merge pull request #127 from malkoG/feature/display-reactors
65e3b91 Display reactors in bottom sheet with emoji filter pills
```

> TOOL

tool_use Agent
id: toolu_01G4hhUHAxiA1dR7pMQUFpam
```json
{
  "description": "Explore article detail page structure",
  "subagent_type": "Explore",
  "prompt": "Explore this Android app codebase to find the article detail page/screen and understand how edit functionality is implemented for other entities.\n\nSpecifically:\n1. Find the article detail screen/composable. Articles are likely a type of post. Look in `app/src/main/java` for things like `ArticleDetail`, `ArticleDetailScreen`, or similar. Also find any `PostDetailScreen` to see the pattern.\n2. Find any existing \"edit\" button implementations on related screens (e.g., post detail, profile detail) — especially how they detect that the current user is the author, how the button is rendered, and how it navigates to the edit screen.\n3. Check if there's already an article edit screen (the branch name is `fix/article-edit-functionality` and recent commits added EditProfileScreen — so there may be an existing article edit screen already). If found, note its route/navigation.\n4. Report: (a) file path + line numbers for the ArticleDetailScreen (or equivalent), (b) how ownership is determined (viewer vs actor), (c) whether/where an Edit Article screen already exists, and (d) any existing edit button pattern to follow from profile or post detail.\n\nThorough level: medium. Report under 300 words with concrete file paths and line numbers."
}
```

> TOOL

tool_result
id: toolu_01G4hhUHAxiA1dR7pMQUFpam
```
Perfect! Now I have all the key information. Let me compile the findings:

## Exploration Results

Based on my analysis of the Android app codebase, here are the findings:

### 1. **Article Detail Screen**
Articles are shown via the **PostDetailScreen** (not a separate ArticleDetailScreen). The screen detects articles by checking `post.typename == "Article"` (line 562, PostDetailScreen.kt).

**File**: `/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt`

**Line numbers**:
- Lines 299-300: Title displays "Article" vs "Post"
- Lines 562-575: Article-specific rendering (larger title, divider)
- Lines 677-691: "Read on Web" button for articles

### 2. **Ownership Determination (canDelete Pattern)**
Ownership is determined by comparing the viewer's handle with the post actor's handle:

**File**: `/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailViewModel.kt`

**Lines 82-85** (and 114-116 on refresh):
```kotlin
val viewerHandle = sessionManager.userHandle.first()
val canDelete = viewerHandle != null &&
    result.post.actor.handle.equals(viewerHandle, ignoreCase = true) &&
    result.post.sharedPost == null
```

The deletion is hidden in a **MoreVert menu** (lines 309-323, PostDetailScreen.kt), shown only if `canDelete` is true.

### 3. **EditArticleScreen Status**
**No ArticleEditScreen exists yet**. Only `EditProfileScreen` exists. The ComposeArticleScreen is used for creating new articles and loading drafts via `draftId` parameter, but there's no dedicated edit-article screen for editing published articles.

**File**: `/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/compose/ComposeArticleScreen.kt` (lines 64-69 show draft loading but no published article […]

> TOOL

tool_use Bash
id: toolu_01RfrzX6zipTEYsHCxCZYgQK
```json
{
  "command": "git status && git log --oneline main..HEAD",
  "description": "Check branch state vs main"
}
```

> TOOL

tool_result
id: toolu_01RfrzX6zipTEYsHCxCZYgQK
```
On branch fix/article-edit-functionality
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/settings.local.json

nothing added to commit but untracked files present (use "git add" to track)
```

> TOOL

tool_use Read
id: toolu_01A3vs1BswpBR7ULWJY7QUQ9
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt",
  "offset": 280,
  "limit": 350
}
```

> TOOL

tool_result
id: toolu_01A3vs1BswpBR7ULWJY7QUQ9
```
280	    }
281	
282	    if (uiState.deleteError != null) {
283	        AlertDialog(
284	            onDismissRequest = { viewModel.dismissDeleteError() },
285	            title = { Text(stringResource(R.string.action_error)) },
286	            text = { Text(uiState.deleteError ?: "") },
287	            confirmButton = {
288	                TextButton(onClick = { viewModel.dismissDeleteError() }) {
289	                    Text(stringResource(R.string.ok))
290	                }
291	            }
292	        )
293	    }
294	
295	    Scaffold(
296	        contentWindowInsets = WindowInsets(0),
297	        topBar = {
298	            LargeTitleHeader(
299	                title = if (uiState.post?.typename == "Article") stringResource(R.string.article) else "Post",
300	                leadingContent = {
301	                    IconButton(onClick = onNavigateBack) {
302	                        Icon(
303	                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
304	                            contentDescription = "Back",
305	                            tint = colors.accent
306	                        )
307	                    }
308	                },
309	                trailingContent = if (uiState.canDelete) {
310	                    {
311	                        PostDetailActionMenu(
312	                            isDeleting = uiState.isDeleting,
313	                            onDelete = {
314	                                if (confirmBeforeDelete) {
315	                                    showDeleteConfirmation = true
316	                                } else {
317	                                    viewModel.deletePost()
318	                                }
319	                            }
320	                        )
321	                    }
322	                } else null
323	            )
324	        },
325	        floatingActionButton = {
326	            if (uiState.post != null && isLoggedIn) {
327	                FloatingActionButton(
328	                    onClick = { onReplyClick(postId) },
329	                    containerColor = colors.composeAccent,
330	                    contentColor = colors.composeOnAccent
331	                ) {
332	                    Icon(
333	                        imageVector = Icons.AutoMirrored.Filled.Reply,
334	                        contentDescription = stringResource(R.string.reply)
335	                    )
336 […]

> TOOL

tool_use Read
id: toolu_01YFSuNhT3EBrfJ51rkbxfP8
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt",
  "offset": 1,
  "limit": 280
}
```

> TOOL

tool_result
id: toolu_01YFSuNhT3EBrfJ51rkbxfP8
```
1	package pub.hackers.android.ui.screens.postdetail
2	
3	import android.annotation.SuppressLint
4	import android.content.Intent
5	import android.text.Html
6	import android.webkit.WebView
7	import androidx.compose.foundation.clickable
8	import androidx.compose.foundation.horizontalScroll
9	import androidx.compose.foundation.verticalScroll
10	import androidx.compose.foundation.layout.Arrangement
11	import androidx.compose.foundation.layout.Box
12	import androidx.compose.foundation.layout.Column
13	import androidx.compose.foundation.layout.PaddingValues
14	import androidx.compose.foundation.layout.Row
15	import androidx.compose.foundation.layout.Spacer
16	import androidx.compose.foundation.layout.WindowInsets
17	import androidx.compose.foundation.layout.asPaddingValues
18	import androidx.compose.foundation.layout.fillMaxHeight
19	import androidx.compose.foundation.layout.fillMaxSize
20	import androidx.compose.foundation.layout.fillMaxWidth
21	import androidx.compose.foundation.layout.height
22	import androidx.compose.foundation.layout.navigationBars
23	import androidx.compose.foundation.layout.padding
24	import androidx.compose.foundation.layout.size
25	import androidx.compose.foundation.layout.width
26	import androidx.compose.foundation.lazy.LazyColumn
27	import androidx.compose.foundation.rememberScrollState
28	import androidx.compose.foundation.shape.CircleShape
29	import androidx.compose.foundation.shape.RoundedCornerShape
30	import androidx.compose.material.icons.Icons
31	import androidx.compose.material.icons.automirrored.filled.ArrowBack
32	import androidx.compose.material.icons.automirrored.filled.Reply
33	import androidx.compose.material.icons.automirrored.outlined.OpenInNew
34	import androidx.compose.material.icons.filled.Delete
35	import androidx.compose.material.icons.filled.MoreVert
36	import androidx.compose.material.icons.filled.Public
37	import androidx.compose.material.icons.filled.Repeat
38	import androidx.compose.material.icons.outlined.AddReaction
39	import androidx.compose.material.icons.outlined.FormatQuote
40	import androidx.compose.material.icons.outlined.Group
41	import androidx.compose.material.icons.outlined.Lock
42	import androidx.compose.material.icons.outlined.Share
43	import androidx.compose.material3.AlertDialog
44	import androidx.compose.material3.Card
45	import androidx.compose.material3.CardDefaults
46	import androidx.compose.material3.CircularProgressIndicator
47	import androidx.compose.material3.DropdownMenu
48	import androidx.compose.material3.DropdownMenuItem
49	import androidx.compose.material3.ExperimentalMaterial3Api
50	import androidx.compose.material3.FloatingActionButton
51	import androidx.compose.material3.HorizontalDivider
52	import androidx.compose.material3.Icon
53	import androidx.compose.material3.IconButton
54	import androidx.compose.material3.LinearProgressIndicator
55	import androidx.compose.material3.MaterialTheme
56	import androidx.compose.material3.ModalBottomSheet
57	import androidx.compose.material3.OutlinedButton
58	import androidx.compose.material3.Scaffold
59	import androidx.compose.material3.Text
60	import androidx.compose.material3.TextButton
61	import androidx.compose.material3.pulltorefresh.PullToRefreshBox
62	import androidx.compose.material3.rememberModalBottomSheetState
63	import androidx.compose.runtime.Composable
64	import androidx.compose.runtime.LaunchedEffect
65	import androidx.compose.runtime.collectAsState
66	import androidx.compose.runtime.getValue […]

> TOOL

tool_use Read
id: toolu_01DVkAugVepsxuXyBgsxCTdb
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailViewModel.kt"
}
```

> TOOL

tool_result
id: toolu_01DVkAugVepsxuXyBgsxCTdb
```
1	package pub.hackers.android.ui.screens.postdetail
2	
3	import androidx.lifecycle.SavedStateHandle
4	import androidx.lifecycle.ViewModel
5	import androidx.lifecycle.viewModelScope
6	import androidx.paging.PagingData
7	import androidx.paging.cachedIn
8	import dagger.hilt.android.lifecycle.HiltViewModel
9	import kotlinx.coroutines.flow.Flow
10	import kotlinx.coroutines.flow.MutableStateFlow
11	import kotlinx.coroutines.flow.StateFlow
12	import kotlinx.coroutines.flow.asStateFlow
13	import kotlinx.coroutines.flow.first
14	import kotlinx.coroutines.flow.update
15	import kotlinx.coroutines.launch
16	import pub.hackers.android.data.local.PreferencesManager
17	import pub.hackers.android.data.local.SessionManager
18	import pub.hackers.android.data.paging.cursorPager
19	import pub.hackers.android.data.paging.distinctByEffectiveId
20	import pub.hackers.android.data.paging.postRepliesPage
21	import pub.hackers.android.data.repository.HackersPubRepository
22	import pub.hackers.android.domain.model.Actor
23	import pub.hackers.android.domain.model.Post
24	import pub.hackers.android.domain.model.ReactionGroup
25	import javax.inject.Inject
26	
27	data class PostDetailUiState(
28	    val post: Post? = null,
29	    val reactionGroups: List<ReactionGroup> = emptyList(),
30	    val isLoading: Boolean = false,
31	    val isRefreshing: Boolean = false,
32	    val error: String? = null,
33	    val canDelete: Boolean = false,
34	    val isDeleting: Boolean = false,
35	    val deleteError: String? = null,
36	    val isDeleted: Boolean = false,
37	    val isReacting: Boolean = false,
38	    val showReactionPicker: Boolean = false,
39	    val showSharesSheet: Boolean = false,
40	    val shareActors: List<Actor> = emptyList(),
41	    val isLoadingShares: Boolean = false,
42	    val showQuotesSheet: Boolean = false,
43	    val quotePosts: List<Post> = emptyList(),
44	    val isLoadingQuotes: Boolean = false,
45	    val showReactorsSheet: Boolean = false,
46	    val selectedReactionGroup: ReactionGroup? = null,
47	)
48	
49 […]

> TOOL

tool_use Bash
id: toolu_01TqyRbBJE94uFGjcWV7o8Nx
```json
{
  "command": "grep -n \"Article\\|compose\" /home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/HackersPubApp.kt | head -80",
  "description": "Find article routes in app nav"
}
```

> TOOL

tool_result
id: toolu_01TqyRbBJE94uFGjcWV7o8Nx
```
grep: /home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/HackersPubApp.kt: No such file or directory
```

> TOOL

tool_use Glob
id: toolu_01DV7LyxtYi8sKyAV3Sczjwc
```json
{
  "pattern": "**/HackersPubApp.kt"
}
```

> TOOL

tool_result
id: toolu_01DV7LyxtYi8sKyAV3Sczjwc
```
app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt
```

> TOOL

tool_use Grep
id: toolu_013US9Wv5QtUQaHuR4LdnRNT
```json
{
  "pattern": "Article|ComposeArticle|EditArticle|edit-article|compose-article|DetailScreen\\.\" ",
  "path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_013US9Wv5QtUQaHuR4LdnRNT
```
44:import pub.hackers.android.ui.screens.compose.ComposeArticleScreen
140:    data object ComposeArticle : DetailScreen("compose-article?draftId={draftId}") {
142:            return if (draftId != null) "compose-article?draftId=$draftId" else "compose-article"
356:                    onComposeArticleClick = {
357:                        navController.navigate(DetailScreen.ComposeArticle.createRoute())
359:                    onComposeArticleLongClick = {
609:                route = DetailScreen.ComposeArticle.route,
619:                ComposeArticleScreen(
640:                        navController.navigate(DetailScreen.ComposeArticle.createRoute(draftId))
```

> TOOL

tool_use Read
id: toolu_01RgP5RA2ycwWUP4g82PyjcS
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt",
  "offset": 130,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01RgP5RA2ycwWUP4g82PyjcS
```
130	    data object Profile : DetailScreen("profile/{handle}") {
131	        fun createRoute(handle: String) = "profile/$handle"
132	    }
133	    data object PostByUrl : DetailScreen("post-by-url?url={url}") {
134	        fun createRoute(url: String): String {
135	            val encoded = android.net.Uri.encode(url)
136	            return "post-by-url?url=$encoded"
137	        }
138	    }
139	    data object RecommendedActors : DetailScreen("recommended-actors")
140	    data object ComposeArticle : DetailScreen("compose-article?draftId={draftId}") {
141	        fun createRoute(draftId: String? = null): String {
142	            return if (draftId != null) "compose-article?draftId=$draftId" else "compose-article"
143	        }
144	    }
145	    data object Drafts : DetailScreen("drafts")
146	    data object EditProfile : DetailScreen("edit-profile")
147	    data object WebView : DetailScreen("webview?url={url}") {
148	        fun createRoute(url: String): String {
149	            val encoded = android.net.Uri.encode(url)
150	            return "webview?url=$encoded"
151	        }
152	    }
153	}
154	
155	@Composable
156	fun HackersPubApp(
157	    deepLinkData: pub.hackers.android.DeepLinkData? = null,
158	    navigationIntent: pub.hackers.android.NavigationIntent? = null,
159	    onDeepLinkConsumed: () -> Unit = {},
160	    onNavigationIntentConsumed: () -> Unit = {},
161	    viewModel: AppViewModel = hiltViewModel()
162	) {
163	    val navController = rememberNavController()
164	    val isLoggedInState by viewModel.isLoggedIn.collectAsState(initial = null as Boolean?)
165	
166	    val fontSizePercent by viewModel.preferencesManager.fontSizePercent.collectAsState(initial = 100)
167	    val hasUnread by viewModel.hasUnread.collectAsState()
168	
169	    // Wait for auth state to resolve from DataStore before rendering navigation.
170	    // This prevents […]

> TOOL

tool_use Read
id: toolu_01F1Kt6uUPagq33JW67QL4sy
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt",
  "offset": 600,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01F1Kt6uUPagq33JW67QL4sy
```
600	                        navController.previousBackStackEntry
601	                            ?.savedStateHandle
602	                            ?.set(PROFILE_REFRESH_KEY, true)
603	                        navController.popBackStack()
604	                    }
605	                )
606	            }
607	
608	            composable(
609	                route = DetailScreen.ComposeArticle.route,
610	                arguments = listOf(
611	                    navArgument("draftId") {
612	                        type = NavType.StringType
613	                        nullable = true
614	                        defaultValue = null
615	                    }
616	                )
617	            ) { backStackEntry ->
618	                val draftId = backStackEntry.arguments?.getString("draftId")
619	                ComposeArticleScreen(
620	                    draftId = draftId,
621	                    onSaveSuccess = {
622	                        navController.popBackStack()
623	                    },
624	                    onPublishSuccess = { articleId ->
625	                        navController.popBackStack()
626	                        navController.navigate(DetailScreen.PostDetail.createRoute(articleId))
627	                    },
628	                    onNavigateBack = {
629	                        navController.popBackStack()
630	                    }
631	                )
632	            }
633	
634	            composable(DetailScreen.Drafts.route) {
635	                DraftsScreen(
636	                    onNavigateBack = {
637	                        navController.popBackStack()
638	                    },
639	                    onDraftClick = { draftId ->
640	                        navController.navigate(DetailScreen.ComposeArticle.createRoute(draftId))
641	                    }
642	                )
643	            }
644	
645	            composable(DetailScreen.RecommendedActors.route) {
646	                RecommendedActorsScreen(
647	                    onNavigateBack = {
648	                        navController.popBackStack()
649	                    },
650	                    onProfileClick = { handle ->
651	                        navController.navigate(DetailScreen.Profile.createRoute(handle))
652	                    }
653	                )
654	            }
655	
656	            composable(
657	                route = DetailScreen.WebView.route,
658	                arguments = listOf(
659	                    navArgument("url") { type = NavType.StringType }
660	                )
661	            ) { backStackEntry ->
662	                val url = backStackEntry.arguments?.getString("url") ?: return@composable
663	                WebViewScreen(
664	                    url = url,
665	                    onNavigateBack = {
666	                        navController.popBackStack()
667	                    }
668 […]

> TOOL

tool_use Grep
id: toolu_01Phu2J86qhfzSaWBFawbybw
```json
{
  "pattern": "PostDetail|PostDetailScreen\" ",
  "path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01Phu2J86qhfzSaWBFawbybw
```
50:import pub.hackers.android.ui.screens.postdetail.PostDetailScreen
127:    data object PostDetail : DetailScreen("post/{postId}") {
339:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId))
368:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId))
379:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId))
411:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId))
514:                route = DetailScreen.PostDetail.route,
518:                PostDetailScreen(
533:                        navController.navigate(DetailScreen.PostDetail.createRoute(id))
549:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId)) {
577:                        navController.navigate(DetailScreen.PostDetail.createRoute(postId))
626:                        navController.navigate(DetailScreen.PostDetail.createRoute(articleId))
```

> TOOL

tool_use Read
id: toolu_0168uxT4neV7GRUnEwBDQ7uB
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/HackersPubApp.kt",
  "offset": 510,
  "limit": 70
}
```

> TOOL

tool_result
id: toolu_0168uxT4neV7GRUnEwBDQ7uB
```
510	                )
511	            }
512	
513	            composable(
514	                route = DetailScreen.PostDetail.route,
515	                arguments = listOf(navArgument("postId") { type = NavType.StringType })
516	            ) { backStackEntry ->
517	                val postId = backStackEntry.arguments?.getString("postId") ?: return@composable
518	                PostDetailScreen(
519	                    postId = postId,
520	                    onNavigateBack = {
521	                        navController.popBackStack()
522	                    },
523	                    onProfileClick = { handle ->
524	                        navController.navigate(DetailScreen.Profile.createRoute(handle))
525	                    },
526	                    onReplyClick = { id ->
527	                        navController.navigate(DetailScreen.Compose.createRoute(replyTo = id))
528	                    },
529	                    onQuoteClick = { id ->
530	                        navController.navigate(DetailScreen.Compose.createRoute(quoteOf = id))
531	                    },
532	                    onPostClick = { id ->
533	                        navController.navigate(DetailScreen.PostDetail.createRoute(id))
534	                    },
535	                    isLoggedIn = isLoggedIn
536	                )
537	            }
538	
539	            composable(
540	                route = DetailScreen.PostByUrl.route,
541	                arguments = listOf(
542	                    navArgument("url") { type = NavType.StringType }
543	                )
544	            ) { backStackEntry ->
545	                val url = backStackEntry.arguments?.getString("url") ?: return@composable
546	                PostByUrlResolverScreen(
547	                    url = url,
548	                    onResolved = { postId ->
549	                        navController.navigate(DetailScreen.PostDetail.createRoute(postId)) {
550	                            popUpTo(DetailScreen.PostByUrl.route) { inclusive = true }
551	                        }
552	                    },
553	                    onNavigateBack = {
554	                        navController.popBackStack()
555	                    }
556	                )
557	            }
558	
559	            composable(
560	                route = DetailScreen.Profile.route,
561	                arguments = listOf(navArgument("handle") { type = NavType.StringType })
562	            ) { backStackEntry ->
563	                val handle = backStackEntry.arguments?.getString("handle") ?: return@composable […]

> TOOL

tool_use Grep
id: toolu_01Awsnstey8LUUQyLuktgpMg
```json
{
  "pattern": "editArticle|updateArticle|editPost|updatePost|UpdateArticle|UpdatePost",
  "path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01Awsnstey8LUUQyLuktgpMg
```
No files found
```

> TOOL

tool_use Read
id: toolu_01MfzHbLZ8bMcCpMjhxGnZdd
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/compose/ComposeArticleScreen.kt",
  "offset": 1,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_01MfzHbLZ8bMcCpMjhxGnZdd
```
1	package pub.hackers.android.ui.screens.compose
2	
3	import androidx.compose.animation.AnimatedVisibility
4	import androidx.compose.animation.expandVertically
5	import androidx.compose.animation.shrinkVertically
6	import androidx.compose.foundation.BorderStroke
7	import androidx.compose.foundation.clickable
8	import androidx.compose.foundation.interaction.MutableInteractionSource
9	import androidx.compose.foundation.layout.Arrangement
10	import androidx.compose.foundation.layout.Box
11	import androidx.compose.foundation.layout.Column
12	import androidx.compose.foundation.layout.Row
13	import androidx.compose.foundation.layout.Spacer
14	import androidx.compose.foundation.layout.WindowInsets
15	import androidx.compose.foundation.layout.fillMaxSize
16	import androidx.compose.foundation.layout.fillMaxWidth
17	import androidx.compose.foundation.layout.height
18	import androidx.compose.foundation.layout.imePadding
19	import androidx.compose.foundation.layout.padding
20	import androidx.compose.foundation.layout.width
21	import androidx.compose.foundation.rememberScrollState
22	import androidx.compose.foundation.shape.RoundedCornerShape
23	import androidx.compose.foundation.text.BasicTextField
24	import androidx.compose.foundation.verticalScroll
25	import androidx.compose.material.icons.Icons
26	import androidx.compose.material.icons.filled.Close
27	import androidx.compose.material3.Button
28	import androidx.compose.material3.ButtonDefaults
29	import androidx.compose.material3.Checkbox
30	import androidx.compose.material3.CheckboxDefaults
31	import androidx.compose.material3.HorizontalDivider
32	import androidx.compose.material3.Icon
33	import androidx.compose.material3.IconButton
34	import androidx.compose.material3.OutlinedButton
35	import androidx.compose.material3.OutlinedTextField
36	import androidx.compose.material3.OutlinedTextFieldDefaults
37	import androidx.compose.material3.Scaffold
38	import androidx.compose.material3.SnackbarHost
39	import androidx.compose.material3.SnackbarHostState
40	import androidx.compose.material3.Surface
41	import androidx.compose.material3.Text
42	import androidx.compose.runtime.Composable
43	import androidx.compose.runtime.LaunchedEffect
44	import androidx.compose.runtime.collectAsState
45	import androidx.compose.runtime.getValue
46	import androidx.compose.runtime.remember
47	import androidx.compose.ui.Alignment
48	import androidx.compose.ui.Modifier
49	import androidx.compose.ui.draw.alpha
50	import androidx.compose.ui.focus.FocusRequester
51	import androidx.compose.ui.focus.focusRequester
52	import androidx.compose.ui.graphics.Color
53	import androidx.compose.ui.graphics.SolidColor
54	import androidx.compose.ui.platform.LocalSoftwareKeyboardController
55	import androidx.compose.ui.res.stringResource
56	import androidx.compose.ui.unit.dp
57	import androidx.hilt.navigation.compose.hiltViewModel
58	import pub.hackers.android.R
59	import pub.hackers.android.ui.theme.AppShapes
60	import pub.hackers.android.ui.theme.LocalAppColors
61	import pub.hackers.android.ui.theme.LocalAppTypography
62	
63	@Composable
64	fun ComposeArticleScreen(
65	    draftId: String? = null,
66	    onSaveSuccess: () -> […]

> TOOL

tool_use Read
id: toolu_01X4b4fMFS6BtbrPfTvhnGra
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/fix-article-edit-functionality/app/src/main/java/pub/hackers/android/ui/screens/compose/ComposeArticleViewModel.kt"
}
```

> TOOL

tool_result
id: toolu_01X4b4fMFS6BtbrPfTvhnGra
```
1	package pub.hackers.android.ui.screens.compose
2	
3	import android.content.Context
4	import android.os.Build
5	import android.view.textclassifier.TextClassificationManager
6	import android.view.textclassifier.TextLanguage
7	import androidx.lifecycle.ViewModel
8	import androidx.lifecycle.viewModelScope
9	import dagger.hilt.android.lifecycle.HiltViewModel
10	import dagger.hilt.android.qualifiers.ApplicationContext
11	import kotlinx.coroutines.flow.MutableStateFlow
12	import kotlinx.coroutines.flow.StateFlow
13	import kotlinx.coroutines.flow.asStateFlow
14	import kotlinx.coroutines.flow.update
15	import kotlinx.coroutines.launch
16	import pub.hackers.android.data.repository.HackersPubRepository
17	import javax.inject.Inject
18	
19	data class ComposeArticleUiState(
20	    val title: String = "",
21	    val content: String = "",
22	    val tags: String = "",
23	    val draftId: String? = null,
24	    val isSaving: Boolean = false,
25	    val isSaved: Boolean = false,
26	    val slug: String = "",
27	    val language: String = java.util.Locale.getDefault().language,
28	    val allowLlmTranslation: Boolean = true,
29	    val showPublishFields: Boolean = false,
30	    val isPublishing: Boolean = false,
31	    val isPublished: Boolean = false,
32	    val publishedArticleId: String? = null,
33	    val publishedArticleUrl: String? = null,
34	    val error: String? = null
35	)
36	
37	@HiltViewModel
38	class ComposeArticleViewModel @Inject constructor(
39	    private val repository: HackersPubRepository,
40	    @ApplicationContext private val context: Context
41	) : ViewModel() {
42	
43	    private val _uiState = MutableStateFlow(ComposeArticleUiState())
44	    val uiState: StateFlow<ComposeArticleUiState> = _uiState.asStateFlow()
45	
46	    fun loadDraft(draftId: String) {
47	        viewModelScope.launch {
48	            repository.getArticleDraft(draftId)
49	                .onSuccess […]

> AGENT

I've explored the code. Here's what I found:

- Article detail uses `PostDetailScreen` (it's a `Post` with `typename == "Article"`). `canDelete` already detects ownership via `viewerHandle` vs `actor.handle` in `PostDetailViewModel.kt:82-85`.
- The existing topBar action is a `MoreVert` dropdown menu (`PostDetailScreen.kt:309-323`, `405-446`) with only a Delete item.
- There is **no** edit-article screen or repository mutation yet. `ComposeArticleScreen` loads `draftId` but not a published article.

Before I code: what should the edit button actually do? Two reasonable paths:

1. **Add button + full edit flow** — extend the compose flow to load a published article and wire an `updateArticle` mutation. A single larger change.
2. **Add button + navigate to Compose with articleId** — still needs the compose-side wiring to do anything useful, so essentially the same work.

Given the memory note that fine-grained commits must each stay functional, I don't want to land a button that no-ops. Want me to do the full flow (button + load published article in ComposeArticle + publish-as-edit mutation), or should I scope this PR to just UI wiring and leave the mutation for a follow-up?