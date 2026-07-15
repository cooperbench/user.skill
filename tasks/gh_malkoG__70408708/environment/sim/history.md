> DEVELOPER

For ArticleDetailScreen or PostDetailScreen, we can't see who reacted to such emoji or like reaction. Could you fetch them? See ../hackerspub

> AGENT

Let me peek at how the web frontend handles this — specifically what gesture opens the reactor list — so the Android behavior matches.

> AGENT

Good news — the GraphQL query for `PostDetail` already fetches `reactors(first: 20)` per group; the reactor data lands in the client but isn't rendered. So this is mostly a UI task, not a data-fetching one. Two facts that shape the UX: - There is no separate `ArticleDetailScreen` — articles render through `PostDetailScreen` (`app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt:719-765`). - Tapping a reaction pill currently *toggles* the viewer's own reaction. We need a different gesture to open a reactor list. **Recommendation:** add a `ReactorsSheet` modeled on the existing `SharesSheet`/`QuotesSheet`, opened by **long-press** on a reaction pill (preserves the familiar tap-to-toggle, matches Slack). Tradeoff: long-press isn't very discoverable, but changing tap-to-show-reactors would force users to dismiss a sheet just to add/remove a reaction. Alternative: tap → open sheet (with the toggle as a button inside the sheet). Closer to Discord, more discoverable, but more clicks for the common toggle case. Want me to go with long-press, or prefer the tap-opens-sheet variant?

> DEVELOPER

Only for see who reactored. we can custom react with reaction button

> AGENT

Got it — pill tap opens the reactor list (read-only); reactions are added/removed via the reaction button. Let me start by reading the actual files I'll need to change.

> AGENT

Now wire up the sheet in PostDetailScreen. First, change the pill onClick to open the reactor sheet, then add the bottom sheet wrapper, then add the `ReactorsSheet` composable.

> AGENT

Now change the pill onClick from `onReactionClick(emoji)` (toggle) to opening the reactor sheet. I'll thread a new callback through `PostDetailContent`.

> AGENT

Now add the `ReactorsSheet` composable. I'll place it next to `SharesSheet`.

> AGENT

The test passes `onReactionClick = {}` — Kotlin allows empty lambdas to satisfy `(T) -> Unit`, so it still compiles unchanged. Let me verify everything by re-reading the touched sections:

> AGENT

Now let me run a build to make sure compilation is clean.

> AGENT

BUILD SUCCESSFUL — only pre-existing deprecation warnings, none from my changes. Let me also run the postdetail test to confirm I didn't break anything.

> AGENT

Tests pass.

> AGENT

Done. Tapping a reaction pill on a post or article now opens a bottom sheet listing the actors who reacted with that emoji (or custom emoji). The reactor data was already fetched by the existing `PostDetailQuery` (`reactors(first: 20)` per group) — this change just surfaces it in the UI. Changes: - `PostDetailViewModel.kt`: added `showReactorsSheet` / `selectedReactionGroup` state and `showReactorsSheet(group)` / `dismissReactorsSheet()` methods. - `PostDetailScreen.kt`: added a `ReactorsSheet` composable + `ModalBottomSheet` wrapper; changed the pill `onReactionClick` from `(String) -> Unit` (toggle) to `(ReactionGroup) -> Unit` (open sheet). Reactions are still added/removed via the dedicated reaction-picker button. - `strings.xml`: added `reactors`, `no_reactors`, `reactors_with_emoji`. Caveat: server returns up to 20 reactors per group with the current query — anything past 20 won't show until pagination is added (separate task).

> DEVELOPER

It also display when click on N reactions text

> AGENT

First, add the ViewModel method:

> AGENT

Now update the sheet wrapper to allow `selectedReactionGroup == null`, and pass `reactionGroups` for the all-reactors case:

> AGENT

Now update the `ReactorsSheet` composable to take a list of groups, and add a divider between sections when there are multiple:

> AGENT

Now thread an `onReactionsClick` callback through `PostDetailContent` and make the "N reactions" text clickable:

> AGENT

Wire the callback at the call site:

> AGENT

Now I need to add the new required parameter to the existing test:

> AGENT

Tests pass.

> AGENT

Done. The "N reactions" engagement text is now styled like Shares/Quotes (accent color, clickable) and opens the same `ReactorsSheet` — but in "all groups" mode, showing each emoji header followed by its reactors, separated by dividers. Tapping an individual reaction pill still opens the sheet scoped to that one emoji.

> DEVELOPER

But, its not scrollable inside

> AGENT

I need `verticalScroll` import — let me check if it's already imported:

> AGENT

`rememberScrollState` is imported but `verticalScroll` is not. Adding it:

> AGENT

Done. Added `verticalScroll(rememberScrollState())` to the `ReactorsSheet` outer Column so long lists (multiple emoji groups, each with up to 20 reactors) scroll inside the bottom sheet. Note: `SharesSheet` and `QuotesSheet` have the same non-scrolling pattern — same fix would apply there if they exhibit the issue, but I left them alone since you mentioned reactors specifically.

> DEVELOPER

For readability, Adding pill filter would be help. So that, first reaction is the applied filter. We can choice only one

> AGENT

Update the wrapper to always pass full `reactionGroups` plus an `initialIndex`:

> AGENT

Now refactor `ReactorsSheet` to add the filter pill row + single-selection state:

> AGENT

Build clean (only pre-existing deprecation warning).

> AGENT

Done. The reactor sheet now has a horizontally-scrollable row of selectable emoji pills at the top (single-selection). The selected pill highlights in the accent color and only that group's reactors render below. Initial selection: - Opened from "N reactions" → first group is selected. - Opened from a specific reaction pill → that pill's index is selected.

> DEVELOPER

Wait where is the avatar url?

> AGENT

The avatar URL is wired through the existing data path — let me trace it for you: | Step | Location | What it does | |------|----------|--------------| | 1. GraphQL fragment | `operations.graphql:1-6` | `fragment ActorFields { id name handle avatarUrl }` | | 2. PostDetail query | `operations.graphql:392-397` | `reactors(first: 20) { edges { node { ...ActorFields } } }` | | 3. Repository mapping | `HackersPubRepository.kt:223-224` | `it.node.actorFields.toActor()` | | 4. `toActor()` | `HackersPubRepository.kt:1401` | `avatarUrl = avatarUrl.toString()` | | 5. Domain model | `Models.kt:179` | `Actor.avatarUrl: String` | | 6. UI | `PostDetailScreen.kt:974` | `AsyncImage(model = actor.avatarUrl, ...)` | So the avatar **is** being fetched and rendered — the call site is identical to `SharesSheet` at line 1049 which works. Are you not seeing avatars on screen? If so — is it: - A specific post (federated remote actor whose avatar URL is broken)? - All reactors on every post? - Only after switching between filter pills? Or did you mean "where in the code is it" — in which case the table above answers that.

> DEVELOPER

Actor's avatar i mean

> AGENT

It's there — `PostDetailScreen.kt:974`: ```kotlin AsyncImage( model = actor.avatarUrl, contentDescription = null, modifier = Modifier.size(40.dp).clip(CircleShape), contentScale = ContentScale.Crop ) ``` This is identical to the working `SharesSheet` at line 1048. The data path is `Edge.node.actorFields.avatarUrl` (URL scalar) → `toActor()` does `avatarUrl = avatarUrl.toString()` → `Actor.avatarUrl: String` → `AsyncImage` above. If avatars aren't rendering on your device, can you confirm: 1. Do avatars show in the **Shares** bottom sheet (same code path) on the same post? 2. Are the rows just blank circles, or are the rows themselves not appearing? That'll tell me whether it's a Coil/network issue or a data issue (empty reactors list because the post hasn't been loaded fresh from `PostDetailQuery`).