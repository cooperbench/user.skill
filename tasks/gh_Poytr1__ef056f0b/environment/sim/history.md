[DEVELOPER]: In the todo page, for "Ackowledge/resolve" it should automatically ack and resolve all the historic releases, has it already been implemented?

[AGENT]: Let me check the current implementation of the acknowledge/resolve functionality in the todo page.

[AGENT]: Yes, it's already implemented. When you click **Acknowledge** on a pending todo, it passes `cascade=true`, which makes the backend automatically acknowledge all older pending todos for the same source/project. Similarly, **Resolve** from the acknowledged view cascades to all older pending and acknowledged todos. The only action that doesn't cascade is **Dismiss**, which explicitly sets `cascade=false` to only affect the single release.