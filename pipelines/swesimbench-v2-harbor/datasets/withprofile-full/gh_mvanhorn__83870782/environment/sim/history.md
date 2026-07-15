[DEVELOPER]: give me the description

[AGENT]: Let me get the PR description for the current branch.

[DEVELOPER]: I need the description of the test I have selected

[AGENT]: Let me find the version check test file on this branch.

[AGENT]: This file has the following tests: | Test | Description | |------|-------------| | **TestIsOutdated** | Table-driven test verifying version comparison logic — standard semver, v-prefix handling, pre-release versions, and git describe format (stripping suffixes like `-76-g230b49bf-dirty` before comparing). | | **TestCacheReadWrite** | Verifies version cache can be serialized to JSON, written to disk, and loaded back with matching timestamps. | | **TestEnsureGlobalConfigDir** | Tests that the global config directory is created with correct permissions (at least `0o700`). | | **TestFetchLatestVersion** | Uses an httptest server to verify the GitHub API call sends correct headers and parses the release tag. | | **TestFetchLatestVersionPrerelease** | Verifies that fetching a pre-release version returns an error. | | **TestFetchLatestVersionServerError** | Verifies that a 500 response from the API returns an error. | | **TestParseGitHubRelease** | Table-driven test for JSON parsing of GitHub release responses (valid, prerelease, empty tag, invalid JSON). | | **TestUpdateCommand** | Checks that `updateCommand()` returns one of the two valid install commands (brew or curl). | | **TestCheckAndNotify_SkipsDevVersion** | Verifies no output is printed when the current version is `"dev"`. | | **TestCheckAndNotify_SkipsEmptyVersion** | Verifies no output for an empty version string. | | **TestCheckAndNotify_SkipsWhenCacheIsFresh** | Verifies the check is skipped […]

[DEVELOPER]: {"1.0.0-dev-xxx", "1.0.1", false, ""},

[AGENT]: That's the test case at line 44 in `TestIsOutdated`: ```go {"v0.4.4-76-g230b49bf-dirty", "v0.4.5", false, "git describe build is not outdated"}, ``` Wait — you pasted `{"1.0.0-dev-xxx", "1.0.1", false, ""}` which isn't currently in the file. It looks like a test case you want to add. It's missing a `desc` string. What would you like the description to be? Something like `"dev build is not outdated"` or `"dev suffix is stripped before comparing"`?