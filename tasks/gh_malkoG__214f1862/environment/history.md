> DEVELOPER

For ArticleDetailScreen or PostDetailScreen, we can't see who reacted to such emoji or like reaction. Could you fetch them? See ../hackerspub

> AGENT

Let me peek at how the web frontend handles this — specifically what gesture opens the reactor list — so the Android behavior matches.

> AGENT

Good news — the GraphQL query for `PostDetail` already fetches `reactors(first: 20)` per group; the reactor data lands in the client but isn't rendered. So this is mostly a UI task, not a data-fetching one. Two facts that shape the UX: - There is no separate `ArticleDetailScreen` — articles render through `PostDetailScreen` (`app/src/main/java/pub/hackers/android/ui/screens/postdetail/PostDetailScreen.kt:719-765`). - Tapping a reaction pill currently *toggles* the viewer's own reaction. We need a different gesture to open a reactor list. **Recommendation:** add a `ReactorsSheet` modeled on the existing `SharesSheet`/`QuotesSheet`, opened by **long-press** on a reaction pill (preserves the familiar tap-to-toggle, matches Slack). Tradeoff: long-press isn't very discoverable, but changing tap-to-show-reactors would force users to dismiss a sheet just to add/remove a reaction. Alternative: tap → open sheet (with the toggle as a button inside the sheet). Closer to Discord, more discoverable, but more clicks for the common toggle case. Want me to go with long-press, or prefer the tap-opens-sheet variant?