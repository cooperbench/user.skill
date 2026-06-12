# PREFERENCES — mheers

## What He Corrects and Rejects

Pushback distribution: **correction 53.8%**, **failure_report 38.5%**, non-pushback 7.7%.

Almost every agent turn draws a response — he is an active corrector, not a passive acceptor.

**Corrections** happen when:
- The agent uses the wrong device path, package name, or capability flag.
- The agent makes a change that technically satisfies the request but breaks something else (broken shell prompt after notification changes).
- The agent does not look at existing code structure first (see: skills folder pattern in Dockerfile — he explicitly pointed this out).

**Failure reports** happen when:
- The package the agent specified does not exist (`docker-compose-plugin` not found).
- A runtime test fails: device not found at the expected path, no sound inside the container.
- He pastes the raw error from the terminal and expects the agent to continue from there.

## What Satisfies Him

Direct evidence of satisfaction is rare (only 7.7% non-pushback). He appears satisfied when the agent:
- Finds the correct flag or path on the first try without him having to spell it out.
- Successfully runs and verifies a build cycle autonomously.

## Workflow Habits

- **No planning phase.** Jumps straight to the task. No "let's think about the approach" prompts.
- **No test-driven development signals.** He validates by running the container and observing behavior.
- **Iterative until it works.** Expects the agent to loop on build/run/test autonomously—he delegates the retry loop explicitly.
- **Mounts host config into Docker** rather than baking credentials or config into the image.
- **Delegates runtime inspection to the agent** ("run the container yourself, inspect the prompt").
- **Does not ask for explanations** of what the agent did. He reads the output; he does not need it narrated.
- **References prior session context** ("check the last changes where we added the notifications") — assumes the agent has memory.

## Tool and Stack Preferences

- Docker / Docker Compose (v2 plugin, `docker compose` not `docker-compose`)
- Shell wrapper scripts (`oc`, `os`) around docker run
- OpenCode as the AI coding tool, configured via `~/.config/opencode/opencode.json`
- OpenCode plugins: `@mohak34/opencode-notifier@latest`, `pbakaus/impeccable`, `antfu/skills`
- libnotify (Linux desktop notifications)
- Audio playback (host-side sound, piped through container)
- USB device passthrough (`/dev/bus/usb/`, `CAP_MKNOD`)
- `make` as the build entry point
