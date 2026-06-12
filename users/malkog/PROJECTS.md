# PROJECTS

## hackers-pub/android ★ dominant repo (100% of sessions)

**What it is:** The official Android client for Hackers' Pub — a Fediverse/ActivityPub social network focused on software developers. Written in Kotlin with Jetpack Compose.

**What malkoG does here:**
- Drives feature parity from scratch against the iOS reference app (`../hackerspub-ios`)
- UI redesign: replacing default Material UI with a custom design system (custom `AppColors`, `AppTypography`, `AppShapes`, `LargeTitleHeader`)
- Content rendering: HTML post content with syntax-highlighted code blocks (Shiki-parsed server HTML), markdown list/heading support
- Release management: signed APK builds, Fastlane metadata, F-Droid submission, Google Play dual distribution
- Git workflow: PR-per-feature against `hackers-pub/android:main` upstream

**Tech stack:**
- Kotlin / Jetpack Compose
- Gradle with Kotlin DSL (`app/build.gradle.kts`)
- Custom theme tokens: `LocalAppColors`, `LocalAppTypography`, `LocalAppShapes`
- NeoUtils/Highlight (initially evaluated, then replaced by server-side Shiki parsing)
- UnifiedPush + embedded FCM distributor for push notifications
- Fastlane for store metadata
- GitHub Actions / PKCS12 keystore for signed releases

**Recurring themes:**
- "See ../hackerspub-ios" — iOS app is the canonical design reference for every screen
- "See ../hackerspub/web-next" — web app referenced for HTML rendering and styling details
- Screen-by-screen restyle: Timeline, Explore, Notifications, Search, Profile, Post Detail, Compose, Settings, Sign-In
- Bug fixes in rendering: mention highlighting, code block syntax, bullet list line breaks, click navigation, reaction sheet
- Release pipeline: version bumps, tags, F-Droid metadata setup

**Fork/upstream relationship:**
- malkoG works on a personal fork (`malkoG/hackerspub-android`)
- PRs target `hackers-pub/android:main` upstream
- Pulls upstream changes with `git pull upstream main` + rebase
