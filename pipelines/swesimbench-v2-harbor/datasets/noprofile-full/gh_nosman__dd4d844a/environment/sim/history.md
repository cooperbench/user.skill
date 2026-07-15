[DEVELOPER]: Let's clean up the gossamer init flow. I think the push-to-remote false default setting should be set to true. The happy path should just be to have the checkpoint branch in the same repo as the code. The wizard can let them change it tho.

[AGENT]: Let me read the init command to understand the current flow.

[AGENT]: The fix is on line 114. Currently `ask_yn("Auto-push sessions on git push", false)` defaults to no-push, so `skip_push` ends up `true` and `--skip-push-sessions` gets passed. Flipping the default to `true` makes push-to-same-repo the happy path.

[AGENT]: Now rebuild and install:

[AGENT]: Done. The wizard now defaults "Auto-push sessions on git push?" to **yes** (`[Y/n]`), so pressing Enter skips the `--skip-push-sessions` flag and sessions land on the checkpoint branch in the same repo. Users can still opt out by typing `n`.