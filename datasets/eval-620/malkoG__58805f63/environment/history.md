> DEVELOPER

For ArticleDetailScreen or PostDetailScreen, we can't see who reacted to such emoji or like reaction. Could you fetch them? See ../hackerspub

> TOOL

tool_use Bash
id: toolu_01ALNEDBVmCuenLryy9Cg1yk
```json
{
  "command": "ls /home/<USER>/fediverse/",
  "description": "List fediverse directory"
}
```

> TOOL

tool_result
id: toolu_01ALNEDBVmCuenLryy9Cg1yk
```
cosmoslide
cosmoslide-2
cosmoslide-editor
f-droid-data
fedify
hackerspub
hackerspub-android
hackerspub-android-prod
hackerspub-android-worktrees
hackerspub-ios
hackerspub-review
join-fediverse
kodingwarrior-hackerspub.github.io
moim
moim-landing
```

> TOOL

tool_use Agent
id: toolu_01PC6wibr1tAesgKgsWPL6L8
```json
{
  "description": "Find reactor API in hackerspub",
  "subagent_type": "Explore",
  "prompt": "Explore the hackerspub project at /home/<USER>/fediverse/hackerspub to find:\n\n1. API endpoints / routes that return the list of users who reacted to a post (with emoji or like reactions). Look for endpoints like /reactors, /reactions, /likes, etc.\n2. The data shape returned by these endpoints (what fields each \"reactor\" includes — e.g., user account, profile info, emoji used, timestamp).\n3. How reactions are stored / queried in the database — relevant tables and query functions.\n4. Where the same data is consumed in the existing web frontend, so I can model the Android consumer the same way.\n\nSpecifically focus on:\n- Whether there's a separate endpoint for emoji reactors vs. like reactors, or if it's unified\n- The path/URL pattern used (likely something like /@user/posts/:id/reactions or similar)\n- Any pagination/limit mechanics\n- Whether the response is JSON, ActivityPub, or both — and if both, what the discriminator is (Accept header, .json suffix, etc.)\n\nReport the findings with file paths and line numbers. The goal is for me to add Android UI that fetches reactor lists for ArticleDetailScreen and PostDetailScreen, so I need to know exactly what to call and what to expect back. Thorough exploration […]

> TOOL

tool_result
id: toolu_01PC6wibr1tAesgKgsWPL6L8
```
Excellent! Now I have enough information. Let me create a comprehensive summary:

## Exploration Summary: Hackerspub Reactions API & Data Structures

Based on my thorough exploration of the hackerspub codebase, here's what I found about reactions/reactors endpoints and data structures:

### 1. **No Dedicated REST API Endpoint for Reactor Lists**

The project does NOT expose a dedicated REST/HTTP endpoint for fetching reactor lists. Instead, reactions are accessed exclusively through:
- **GraphQL API** (primary method)
- **Web UI routes** (server-rendered pages)

### 2. **Web UI Routes for Displaying Reactors**

There are server-rendered routes that display reactors:

- **For Notes (short posts):**
  - `/home/<USER>/fediverse/hackerspub/web/routes/@[username]/[idOrYear]/reactions.tsx` (lines 16-87)
  - URL pattern: `/@{username}/{postId}/reactions`

- **For Articles:**
  - `/home/<USER>/fediverse/hackerspub/web/routes/@[username]/[idOrYear]/[slug]/reactions.tsx` (lines 16-93)
  - URL pattern: `/@{username}/{year}/{slug}/reactions`

Both routes follow the same pattern:
1. Fetch the post from database
2. Query `reactionTable` with the post ID
3. Group reactions by emoji (grouping by `customEmojiId` or `emoji` field)
4. Sort groups by count (descending), then alphabetically
5. Render as an `ActorList` component showing who reacted

### 3. **GraphQL Queries for Reactors**

The primary way to consume reactions data in the web-next frontend is via GraphQL:

- **Query Type:** Query node with `reactionGroups` field on `Reactable` […]

> TOOL

tool_use Bash
id: toolu_01ESn51fZRitRbqvwHQLnjUx
```json
{
  "command": "ls /home/<USER>/fediverse/hackerspub-android-worktrees/feature-display-reactors/",
  "description": "List Android project root"
}
```

> TOOL

tool_result
id: toolu_01ESn51fZRitRbqvwHQLnjUx
```
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

tool_use Read
id: toolu_014MUJ7cQyY8WKgyhu7jcDam
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub-android-worktrees/feature-display-reactors/CONVENTION.md"
}
```

> TOOL

tool_result
id: toolu_014MUJ7cQyY8WKgyhu7jcDam
```
1	# Conventions
2	
3	Rules that reviewers enforce during PR review. Violations block merge unless explicitly justified in the PR description.
4	
5	## §1 Scope
6	
7	- These rules apply to code under `app/src/main/`.
8	- Test code (`app/src/test/`, `app/src/androidTest/`) has relaxed rules noted in §9.
9	- Generated code (Apollo, Hilt, KSP output) is out of scope.
10	
11	---
12	
13	## §2 Null-safety
14	
15	### §2.1 No new `!!`
16	
17	The `!!` non-null assertion operator is forbidden in new code. Existing call sites (3 as of this writing) are all defensive invariants immediately after a null check:
18	
19	| Site | Invariant guaranteeing non-null |
20	|------|----------------------------------|
21	| `ui/HackersPubApp.kt:169` | early `return` when `isLoggedInState == null` on the preceding line |
22	| `ui/components/ArticleCard.kt:83` | inside `if (isRepost && post.lastSharer != null)` |
23	| `ui/components/ReactionPicker.kt:53` | inside `.filter { it.emoji != null }` |
24	
25	New `!!` requires a `// safe because <reason>` comment and reviewer approval. Before adding one, try:
26	
27	- Elvis `?:` with a default or `return`
28	- Smart cast after an `if (x != null)` / early return […]

> TOOL

tool_use Agent
id: toolu_017gsQny5D2ePrSjAXVHCVex
```json
{
  "description": "Map Android reactor code",
  "subagent_type": "Explore",
  "prompt": "Explore the Android project at /home/<USER>/fediverse/hackerspub-android-worktrees/feature-display-reactors to map out everything I need to add a \"show reactors\" feature.\n\nSpecifically, find and report (with file paths and line numbers):\n\n1. **ArticleDetailScreen** and **PostDetailScreen** locations and structure — where reactions are currently displayed in the UI.\n2. **Existing reactions UI** — `ReactionPicker`, any `ReactionsRow`, `ReactionGroup` usage. How are reactions currently rendered in detail screens? What does a tap on a reaction currently do (toggle? nothing?)\n3. **GraphQL operations file** — `app/src/main/graphql/pub/hackers/android/operations.graphql`. Show the existing queries/fragments related to reactions: `ReactionGroupFields`, `ActorFields`, anything that fetches `reactionGroups`. I need to see what's already being fetched per-post and what would need to be added for a reactor list.\n4. **Domain model for reactions** — `domain/model/Models.kt` or similar. What's the current `ReactionGroup` data class shape?\n5. **Repository** (`HackersPubRepository`) — examples of how detail queries are wired and how new query methods are added.\n6. **ViewModel pattern** — pick `ArticleDetailViewModel` and `PostDetailViewModel` as references and report their structure (UiState shape, how they call the repository, error handling).\n7. **Navigation** — sealed `Route` class location and how detail screens are added as new destinations. I'll need a new `ReactorList` route.\n8. **Existing dialog/bottom sheet […]

> TOOL

tool_result
id: toolu_017gsQny5D2ePrSjAXVHCVex
```
Perfect! Now I have all the information I need. Let me create a comprehensive summary for the user.

## Complete Project Exploration Report: "Show Reactors" Feature

Based on my thorough exploration of the hackerspub-android project, here's everything you need to implement the "show reactors" feature:

---

### 1. **Detail Screens & Current Reactions UI**

**PostDetailScreen location:**
- `/home/<USER>/fediverse/hackerspub-android-worktrees/feature-display-reactors/app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt`

**Current reactions display (PostDetailScreen.kt):**
- **Lines 719-765**: Reaction groups rendered as pill-shaped cards in a horizontal row
- **Lines 722-762**: Each `ReactionGroup` renders as a Card with emoji/count, clickable to toggle
- Tapping a reaction **toggles** (adds/removes viewer reaction), not showing reactor list
- **Lines 154-167**: ReactionPicker bottom sheet shows available emojis to add reactions
- **Lines 719**: Condition checks `if (reactionGroups.isNotEmpty())`

**No ArticleDetailScreen exists** - articles use the same PostDetailScreen (distinguished by `post.typename == "Article"`)

---

### 2. **Existing Reactions UI Components**

**ReactionPicker location & structure:**
- `/home/<USER>/fediverse/hackerspub-android-worktrees/feature-display-reactors/app/src/main/java/pub/hackers/android/ui/components/ReactionPicker.kt`
- **Lines 41**: `SUPPORTED_REACTION_EMOJIS = ["❤️", "🎉", "😂", "😲", "🤔", "😢", "👀"]`
- **Lines 44-174**: Composable that shows grid of emoji options with counts
- **Lines 106-131**: Grid cells (7 per row) show emoji + count, clickable to toggle
- **Lines 134-172**: Selected reactions row at bottom shows reactions […]

> AGENT

Let me peek at how the web frontend handles this — specifically what gesture opens the reactor list — so the Android behavior matches.

> TOOL

tool_use Read
id: toolu_01RGk2pkmazQRdLv6NRNRYRn
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub/web-next/src/components/EmojiReactionPopover.tsx"
}
```

> TOOL

tool_result
id: toolu_01RGk2pkmazQRdLv6NRNRYRn
```
1	import { REACTION_EMOJIS, sortReactionGroups } from "@hackerspub/models/emoji";
2	import { graphql } from "relay-runtime";
3	import { createSignal, For, Show } from "solid-js";
4	import { createMutation } from "solid-relay";
5	import { Button } from "~/components/ui/button.tsx";
6	import { showToast } from "~/components/ui/toast.tsx";
7	import { useLingui } from "~/lib/i18n/macro.d.ts";
8	import type { EmojiReactionPopoverAddMutation } from "./__generated__/EmojiReactionPopoverAddMutation.graphql.ts";
9	import type { EmojiReactionPopoverRemoveMutation } from "./__generated__/EmojiReactionPopoverRemoveMutation.graphql.ts";
10	
11	interface NoteData {
12	  id: string;
13	  reactionGroups: ReadonlyArray<{
14	    readonly __typename?: string;
15	    readonly emoji?: string;
16	    readonly customEmoji?: {
17	      readonly id: string;
18	      readonly name: string;
19	      readonly imageUrl: string;
20	    } | undefined;
21	    readonly count?: number;
22	    readonly viewerHasReacted?: boolean;
23	  }>;
24	}
25	
26	export interface EmojiReactionPopoverProps {
27	  noteData: NoteData;
28	  onClose: () => void;
29	}
30	
31	const addReactionToPostMutation = graphql`
32	  mutation EmojiReactionPopoverAddMutation($input: AddReactionToPostInput!) {
33	    addReactionToPost(input: $input) {
34	      ... on AddReactionToPostPayload {
35	        reaction {
36	          id
37	        }
38	      }
39	      ... on InvalidInputError {
40	        inputPath
41	      }
42	      ... on NotAuthenticatedError {
43	        notAuthenticated
44	      }
45	    }
46	  }
47	`;
48	
49	const removeReactionFromPostMutation = graphql`
50	  mutation […]

> TOOL

tool_use Bash
id: toolu_01ULCk1XnMXZTgeAK2UPeCam
```json
{
  "command": "ls /home/<USER>/fediverse/hackerspub/web-next/src/components/ | head -50",
  "description": "List web-next components"
}
```

> TOOL

tool_result
id: toolu_01ULCk1XnMXZTgeAK2UPeCam
```
__generated__
article-composer
notification
ui
AboutHackersPub.tsx
ActorArticleList.tsx
ActorFollowerList.tsx
ActorFollowingList.tsx
ActorNoteList.tsx
ActorPostList.tsx
ActorSharedPostList.tsx
AppSidebar.tsx
ArticleCard.tsx
DocumentView.tsx
EmojiReactionPopover.tsx
FloatingComposeButton.tsx
FollowButton.tsx
ForceGraph.tsx
InternalLink.tsx
LanguageList.tsx
LanguageSelect.tsx
LinkPreview.tsx
LocaleSelect.tsx
MentionAutocomplete.tsx
NarrowContainer.tsx
NavigateIfHandleIsNotCanonical.tsx
NoteCard.tsx
NoteCardInternal.tsx
NoteComposeModal.tsx
NoteComposer.tsx
NoteHeader.tsx
NoteMedia.tsx
NotificationActor.tsx
NotificationCard.tsx
NotificationList.tsx
PersonalTimeline.tsx
PostActionMenu.tsx
PostAvatar.tsx
PostCard.tsx
PostControls.tsx
PostSharer.tsx
PostVisibilitySelect.tsx
ProfileCard.tsx
ProfileTabs.tsx
PublicTimeline.tsx
QuotedNoteCard.tsx
QuotedPostCard.tsx
RemoteFollowButton.tsx
SearchGuide.tsx
SearchResults.tsx
```

> TOOL

tool_use Bash
id: toolu_018rwYSqh7QTtGhrfQkVNShF
```json
{
  "command": "ls /home/<USER>/fediverse/hackerspub/web-next/src/components/ | grep -i react",
  "description": "Find ReactorList component"
}
```

> TOOL

tool_result
id: toolu_018rwYSqh7QTtGhrfQkVNShF
```
EmojiReactionPopover.tsx
```

> TOOL

tool_use Grep
id: toolu_015V7uziiXB9uL1zkdpxbgqH
```json
{
  "pattern": "ReactorList",
  "path": "/home/<USER>/fediverse/hackerspub/web-next/src",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_015V7uziiXB9uL1zkdpxbgqH
```
No files found
```

> TOOL

tool_use Grep
id: toolu_01Ha5wqcro6XDeCroZ6d1wVM
```json
{
  "pattern": "ReactorListDialog",
  "path": "/home/<USER>/fediverse/hackerspub",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01Ha5wqcro6XDeCroZ6d1wVM
```
No files found
```

> TOOL

tool_use Read
id: toolu_01DfB6HTHpFfcKQv2WfgfSeh
```json
{
  "file_path": "/home/<USER>/fediverse/hackerspub/web/routes/@[username]/[idOrYear]/reactions.tsx"
}
```

> TOOL

tool_result
id: toolu_01DfB6HTHpFfcKQv2WfgfSeh
```
1	import { page } from "@fresh/core";
2	import { extractMentionsFromHtml } from "@hackerspub/models/markup";
3	import { getNoteSource } from "@hackerspub/models/note";
4	import type { Account, Actor, CustomEmoji } from "@hackerspub/models/schema";
5	import { validateUuid } from "@hackerspub/models/uuid";
6	import { ActorList } from "../../../components/ActorList.tsx";
7	import { Msg } from "../../../components/Msg.tsx";
8	import { PageTitle } from "../../../components/PageTitle.tsx";
9	import { PostExcerpt } from "../../../components/PostExcerpt.tsx";
10	import { PostReactionsNav } from "../../../components/PostReactionsNav.tsx";
11	import { db } from "../../../db.ts";
12	import { PostControls } from "../../../islands/PostControls.tsx";
13	import { kv } from "../../../kv.ts";
14	import { define } from "../../../utils.ts";
15	
16	export const handler = define.handlers(async (ctx) => {
17	  if (!validateUuid(ctx.params.idOrYear)) return ctx.next();
18	  const id = ctx.params.idOrYear;
19	  if (ctx.params.username.includes("@")) return ctx.next();
20	  const note = await getNoteSource(
21	    db,
22	    ctx.params.username,
23	    id,
24	    ctx.state.account,
25	  );
26	  if (note == null) return ctx.next();
27	  const reactions = await db.query.reactionTable.findMany({
28	    with: {
29	      actor: {
30	        with: { account: true },
31	      },
32	      customEmoji: true,
33	    },
34	    where: { postId: note.post.id },
35	    orderBy: { created: "desc" },
36	  });
37	  const map = new Map<
38	    string […]

> AGENT

Good news — the GraphQL query for `PostDetail` already fetches `reactors(first: 20)` per group; the reactor data lands in the client but isn't rendered. So this is mostly a UI task, not a data-fetching one.

Two facts that shape the UX:
- There is no separate `ArticleDetailScreen` — articles render through `PostDetailScreen` (`app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt:719-765`).
- Tapping a reaction pill currently *toggles* the viewer's own reaction. We need a different gesture to open a reactor list.

**Recommendation:** add a `ReactorsSheet` modeled on the existing `SharesSheet`/`QuotesSheet`, opened by **long-press** on a reaction pill (preserves the familiar tap-to-toggle, matches Slack). Tradeoff: long-press isn't very discoverable, but changing tap-to-show-reactors would force users to dismiss a sheet just to add/remove a reaction.

Alternative: tap → open sheet (with the toggle as a button inside the sheet). Closer to Discord, more discoverable, but more clicks for the common toggle case.

Want me to go with long-press, or prefer the tap-opens-sheet variant?