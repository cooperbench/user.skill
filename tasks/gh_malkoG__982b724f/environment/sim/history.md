> DEVELOPER

We have two weblinks. article/post for article, @actor/year/slug should be redirected to ArticleDetailScreen. for post, @actor/uuid should be redirected to PostDetailScreen. For detail, see ../hackerspub

> AGENT

Let me explore both the hackerspub project and the Android app to understand the URL patterns and current navigation setup.

> AGENT

Now let me look at the key files I need to modify.

> AGENT

Let me check how the API handles article lookups and how PostDetail loads content.

> AGENT

Let me read the PostDetailViewModel and GraphQL schema for the specific queries.

> AGENT

Let me check the GraphQL schema for the article lookup queries.

> AGENT

Let me check the PostDetailScreen composable signature and how it receives data.

> AGENT

Let me check the mapper functions and the full repository.

> AGENT

Now I have a clear picture. Here's my plan: **Goal**: Route article URLs (`/@actor/year/slug`) to the detail screen, and also handle post URLs (`/@actor/uuid`) that already work. **Approach**: 1. Add a lightweight `PostByUrl` GraphQL query (just needs to return the relay ID) 2. Add a "URL resolver" route that resolves the URL → relay ID, then redirects to the existing PostDetailScreen 3. Update `HackersPubUrlRouter` to recognize article URLs 4. Wire up the new route in `HackersPubApp` This avoids modifying the PostDetailViewModel at all. Let me implement it.

> AGENT

**Step 1**: Add the `PostByUrl` GraphQL query. It only needs to return the relay `id` so the existing PostDetail flow can take over.

> AGENT

**Step 2**: Add `resolvePostIdByUrl()` to the repository.

> AGENT

Now add the import for `PostByUrlQuery`.

> AGENT

**Step 3**: Update `HackersPubUrlRouter` to recognize article URLs (`/@handle/year/slug`).

> AGENT

Now add the article URL matching pattern. Article URLs have 3 segments: `@handle`, year (4-digit number), slug. This must be checked **before** the UUID pattern for posts (2 segments).

> AGENT

Now add the article pattern matching case. It needs to come before the UUID-based note detail check:

> AGENT

Now update `toNavRoute()` to handle the new `ArticleDetail` route:

> AGENT

**Step 4**: Add `DetailScreen.PostByUrl` route and resolver composable. First, add the route definition:

> AGENT

Now add the resolver composable in the NavHost. Let me find a good place to add it - right after the PostDetail composable:

> AGENT

Now I'll add the `PostByUrl` resolver composable right after the `PostDetail` composable. I need to create a small resolver screen. Let me add it as inline composable first:

> AGENT

Now I need to create the `PostByUrlResolverScreen` composable. Let me create it as a separate file:

> AGENT

Now create the ViewModel for the resolver:

> AGENT

Now add the import for the resolver screen in `HackersPubApp.kt`:

> AGENT

**Step 5**: Let me verify the files look correct, then build.

> AGENT

Good. Now let me build to check compilation:

> AGENT

Need to handle the new `ArticleDetail` case in `MainActivity.kt`.

> AGENT

Build succeeds.

> AGENT

All done. Here's a summary of the changes: ### Files modified: 1. **`operations.graphql`** - Added `PostByUrl` query that resolves a URL to a relay ID 2. **`HackersPubRepository.kt`** - Added `resolvePostIdByUrl()` method + import 3. **`HackersPubUrlRouter.kt`** - Added `ArticleDetail(url)` route variant and `/@handle/year/slug` pattern matching (4-digit year regex) 4. **`HackersPubApp.kt`** - Added `DetailScreen.PostByUrl` route definition and the resolver composable in the NavHost 5. **`MainActivity.kt`** - Added `ArticleDetail` to the exhaustive `when` expression ### Files created: 6. **`PostByUrlResolverScreen.kt`** - Loading screen that resolves a URL to a relay ID, then redirects to PostDetailScreen 7. **`PostByUrlResolverViewModel.kt`** - ViewModel that calls `resolvePostIdByUrl` ### How it works: - **Article URL** (`https://hackers.pub/@alice/2025/my-article`) → `HackersPubUrlRouter` recognizes the `/@handle/year/slug` pattern → routes to `PostByUrl` resolver → calls `postByUrl` GraphQL query → gets relay ID → navigates to `PostDetailScreen` - **Post URL** (`https://hackers.pub/@alice/uuid`) → works as before via `NoteDetail` route → `PostDetailScreen` - Both deep links from outside the app and in-app link clicks (via `InAppBrowserUriHandler`) are handled

> TOOL

<bash-input>git switch -c fix/post-url-resolution</bash-input>

> TOOL

<bash-stdout>Switched to a new branch 'fix/post-url-resolution'</bash-stdout><bash-stderr></bash-stderr>