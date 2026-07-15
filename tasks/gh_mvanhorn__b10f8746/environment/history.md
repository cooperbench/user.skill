> DEVELOPER

give me the description

> AGENT

Let me get the PR description for the current branch.

> DEVELOPER

I need the description of the test I have selected

> AGENT

Let me find the version check test file on this branch.

> AGENT

This file has the following tests: | Test | Description | |------|-------------| | **TestIsOutdated** | Table-driven test verifying version comparison logic — standard semver, v-prefix handling, pre-release versions, and git describe format (stripping suffixes like `-76-g230b49bf-dirty` before comparing). | | **TestCacheReadWrite** | Verifies version cache can be serialized to JSON, written to disk, and loaded back with matching timestamps. | | **TestEnsureGlobalConfigDir** | Tests that the global config directory is created with correct permissions (at least `0o700`). | | **TestFetchLatestVersion** | Uses an httptest server to verify the GitHub API call sends correct headers and parses the release tag. | | **TestFetchLatestVersionPrerelease** | Verifies that fetching a pre-release version returns an error. | | **TestFetchLatestVersionServerError** | Verifies that a 500 response from the API returns an error. | | **TestParseGitHubRelease** | Table-driven test for JSON parsing of GitHub release responses (valid, prerelease, empty tag, invalid JSON). | | **TestUpdateCommand** | Checks that `updateCommand()` returns one of the two valid install commands (brew or curl). | | **TestCheckAndNotify_SkipsDevVersion** | Verifies no output is printed when the current version is `"dev"`. | | **TestCheckAndNotify_SkipsEmptyVersion** | Verifies no output for an empty version string. | | **TestCheckAndNotify_SkipsWhenCacheIsFresh** | Verifies the check is skipped […]

> DEVELOPER

{"1.0.0-dev-xxx", "1.0.1", false, ""},

> AGENT

That's the test case at line 44 in `TestIsOutdated`: ```go {"v0.4.4-76-g230b49bf-dirty", "v0.4.5", false, "git describe build is not outdated"}, ``` Wait — you pasted `{"1.0.0-dev-xxx", "1.0.1", false, ""}` which isn't currently in the file. It looks like a test case you want to add. It's missing a `desc` string. What would you like the description to be? Something like `"dev build is not outdated"` or `"dev suffix is stripped before comparing"`?

> DEVELOPER

sorry, try now

> AGENT

Line 40 — the test case is: ```go {"1.0.0-dev-xxx", "1.0.1", false, ""}, ``` It expects `isOutdated` to return `false` for a dev build (`1.0.0-dev-xxx`) compared against a newer release (`1.0.1`). The `desc` field is empty — it needs a description. Something like `"dev build skips version check"` or `"dev suffix is not outdated"` would fit the existing style. Want me to fill it in?

> DEVELOPER

fix version check to do what the tests are expecting

> AGENT

Let me first understand the current `isOutdated` implementation.

> AGENT

Let me run the test to see what's failing.

> AGENT

The failure is `prerelease_in_current`: `isOutdated("1.0.0-rc1", "1.0.0")` returns `false` but the test expects `true`. The current code blanket-skips all prerelease versions, but the tests want: - `1.0.0-rc1` vs `1.0.0` → `true` (rc prerelease IS outdated) - `1.0.0-dev-xxx` vs `1.0.1` → `false` (dev builds skip the check) The fix is to only skip dev builds, not all prereleases.

> AGENT

All passing. Let me also run the full package tests to make sure nothing else broke.

> AGENT

All 13 tests pass. The fix: changed the blanket prerelease skip to only skip versions containing `dev` in the prerelease suffix. This way: - `1.0.0-rc1` vs `1.0.0` → `true` (rc is outdated, normal semver comparison applies) - `1.0.0-dev-xxx` vs `1.0.1` → `false` (dev builds skip the check)

> DEVELOPER

commit those changes

> AGENT

Committed as `17bc1980`.

> DEVELOPER

I do need that VERSION to be {version}-dev-{commit}

> AGENT

Let me find where the version is set during builds.

> AGENT

Now I see the full picture. The `mise run build` task uses `git describe --tags --always --dirty` which produces versions like `v0.4.4-76-g230b49bf-dirty`. The user wants dev builds to use the format `{version}-dev-{commit}` instead. I need to update the build task in `mise.toml` to transform the git describe output:

> AGENT

Fair point. Let me simplify:

> AGENT

You're right. Simplest: just swap the line order and use a one-liner fallback.

> AGENT

Got it, you already have `TAG` and `COMMIT`. Just need to compose VERSION from them:

> AGENT

Now the build task produces versions like `v0.4.4-dev-230b49b`. Let me verify it builds:

> AGENT

Version is now `v0.4.5-dev-755fbfde` — `{TAG}-dev-{COMMIT}`, exactly as expected.