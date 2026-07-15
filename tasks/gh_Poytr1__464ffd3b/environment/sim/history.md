[DEVELOPER]: In the todo page, for "Ackowledge/resolve" it should automatically ack and resolve all the historic releases, has it already been implemented?

[AGENT]: Let me check the current implementation of the acknowledge/resolve functionality in the todo page.

[AGENT]: Yes, it's already implemented. When you click **Acknowledge** on a pending todo, it passes `cascade=true`, which makes the backend automatically acknowledge all older pending todos for the same source/project. Similarly, **Resolve** from the acknowledged view cascades to all older pending and acknowledged todos. The only action that doesn't cascade is **Dismiss**, which explicitly sets `cascade=false` to only affect the single release.

[DEVELOPER]: But we found a bug that after acknowledging the latest, the older one still pops up why?

[AGENT]: Let me dig into the cascade logic to find the bug.

[AGENT]: Now let me check how todos are created — specifically whether new todos are created for releases that come in *after* the acknowledge action, which would bypass the cascade.

[AGENT]: I see the issue. Let me check if the `CreateReleaseTodo` respects previously acknowledged state — i.e., if you acknowledge the latest, and then a *re-notification* or retry creates a todo for an older release, does it skip it?

[AGENT]: Now let me check the cascade query more carefully. The issue is in the cascade condition — it uses `r2.created_at <= r1.created_at`. But what if the "older" release's `release_todos.release_id` is NULL (i.e., the todo is a semantic_release todo, not a release todo)? The `OR` branches are mutually exclusive based on which ID is set. Let me look at a different angle — what if the problem is that some todos have a `semantic_release_id` and others have a `release_id` for the same project?