# Style — squishykid

## Typing fingerprint

- **Median prompt:** 7 words. 90th percentile: 33 words. Max: 646 (spec dump).
- **Casing:** all lowercase, always. Even proper nouns in casual messages ("lets remove HookSuport.GetSupportedHooks", "let move HookNames()").
- **Punctuation:** omitted on short messages. No period at the end of commands. Question marks used normally. Apostrophes often dropped ("lets", "ive", "dont").
- **Emoji:** never.
- **Formatting:** pastes code, file paths, and issue/PR numbers inline without backticks in casual messages. Uses markdown code blocks only inside spec-dump plans (which are fully formatted).
- **Typos:** frequent and uncorrected. Never sends a second message to fix them.
  - "intiializesession" (initializeSession)
  - "repositiory" (repository)
  - "captialised" (capitalised)
  - "HookSuport" (HookSupport)
  - "efthook" (Lefthook — drops the L)
  - "let make" (let's make)

## Language

English only (100%). No code-switching.

## Calibration quotes

**Opening a session (terse):**
> `commit the changes and make a pr`

> `fix the tests please`

> `is Agent.GetHookConfigPath used anywhere?`

**Starting mid-session git work:**
> `commit this on a feature branch. use prefix 'rwr/' for the branch name`

> `commit and create a pr referencing #279 and #293`

> `git push`

**Steering / redirecting:**
> `rather than modifying intiializesession for manual_commit_session.go and auto_commit.go, could we call 'IsEmptyRepository' inside common.go:OpenRepository()?`

> `can you check hooks_geminicli_handers.go. perhaps this needs a change too`

> `move to another branch before committing`

**Nitpick corrections:**
> `initGitRepo duplicates the existing initHooksTestRepo helper in hooks_test.go (both run git init, t.Chdir, and clear the RepoRoot cache). Reusing the shared helper would reduce duplication and keep repo setup logic consistent across tests.`

> `cmdPrefix selection logic is duplicated here and in hooks.go (both branch on isLocalDev() to pick either entire or go run ...). Consider extracting a small helper (e.g. hookCmdPrefix() / commandPrefix()) to avoid future drift where hook contents and warning instructions could disagree.`

**Short removal commands:**
> `lets remove it`

> `lets remove HookSuport.GetSupportedHooks`

> `lets remove Agent.SupportsHooks`

**Pasting reference data as a correction:**
> `Lefthook looks for a configuration file using the pattern {.,}lefthook.{yml,yaml,json,toml} DeepWiki. So all valid main config files are:`
> *(followed by raw list, no framing)*

**After branch mishap:**
> `ive just moved to another branch, can you apply those changes again please?`
