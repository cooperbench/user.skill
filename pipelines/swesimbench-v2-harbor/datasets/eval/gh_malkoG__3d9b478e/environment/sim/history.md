[DEVELOPER]: Add bottom padding for each post/article detail enough

[AGENT]: Found it. The `LazyColumn` in `PostDetailContent` (line 455) has no bottom `contentPadding`, so the last reply gets obscured by the FAB and the system nav bar (Scaffold has `contentWindowInsets = WindowInsets(0)`). Let me add bottom padding accounting for both the FAB and the navigation bar inset.

[AGENT]: Now let me verify the edit compiles by checking for build tasks.

[AGENT]: Build passes (only pre-existing deprecation warnings). Added bottom `contentPadding` of `navigationBars` inset + 96.dp on the `LazyColumn` in `PostDetailScreen.kt:459`, so the last reply clears the FAB and system nav bar.

[AGENT]: No staged changes. Let me stage the modified file.

[AGENT]: Commit created: `8256344 Add bottom padding to post detail list`.

[AGENT]: PR created: https://github.com/hackers-pub/android/pull/129