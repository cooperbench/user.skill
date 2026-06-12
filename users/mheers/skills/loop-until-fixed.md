---
name: loop-until-fixed
description: When the fix requires iterative build/run/test cycles, explicitly tell the agent to execute the loop autonomously and not stop until it works. Triggered when a Docker build or runtime validation is needed to confirm the fix.
---

mheers delegates the build-test retry loop to the agent rather than checking results himself each round. He frames this as an explicit instruction: the agent should run the relevant command (build, start container, run make) and keep iterating until the observed behavior is correct. He does not ask for a summary of attempts — he wants a working result.

**Trigger:** Agent has proposed a fix that requires a build or container restart to verify.

**Examples:**

> "the audio notification is not send from inside the docker container. fix it in a loop until it works"

> "the last changes made my prompt look broken. run the container yourself, inspect the prompt, adjust the scripts and fix the prompt, build and restart the container until it is fixed"

> "10.02 E: Unable to locate package docker-compose-plugin\nrun \"make\" yourself until it works"

**Signature phrases:** "fix it in a loop until it works", "run X yourself until it works", "build and restart the container until it is fixed"
