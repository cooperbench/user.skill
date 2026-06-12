---
name: nitpick-redirect
description: How squishykid catches something the agent missed or got structurally wrong — asks a pointed question or makes an observation, then follows with a correction command. Trigger when the agent has just declared success but missed a file, left duplicate code, or made a visibility/naming mistake.
---

squishykid does not acknowledge the agent's summary. Instead they immediately flag the oversight with a short observation or rhetorical question, then issue the fix command. The pattern is:

1. Agent delivers output (summary ignored)
2. squishykid names what was missed, often phrasing it as a question or a soft "perhaps"
3. If the question is answered affirmatively, squishykid issues the removal/fix command

**Example — missed file:**
> `can you check hooks_geminicli_handers.go. perhaps this needs a change too`

**Example — wrong visibility:**
> `why is HookManager and DetectHookManagers exported (capitalized)?`
*(agent explains → squishykid follows with:)*
> `let make HookManager and DetectHookManagers local (not captialised)`

**Example — duplicate helper:**
> `initGitRepo duplicates the existing initHooksTestRepo helper in hooks_test.go (both run git init, t.Chdir, and clear the RepoRoot cache). Reusing the shared helper would reduce duplication and keep repo setup logic consistent across tests.`

**Example — duplicate logic:**
> `cmdPrefix selection logic is duplicated here and in hooks.go (both branch on isLocalDev() to pick either entire or go run ...). Consider extracting a small helper (e.g. hookCmdPrefix() / commandPrefix()) to avoid future drift where hook contents and warning instructions could disagree.`

Note: when the nitpick is a code block or reference data (e.g. a config file pattern list), squishykid pastes it raw with no framing text.
