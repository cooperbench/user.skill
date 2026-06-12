---
name: error-paste-directive
description: When an agent's fix didn't work, paste the raw error output from the terminal, then on a new line restate the expected behavior or the exact flag/path needed — no explanation, no "you were wrong".
---

mheers reports failures by pasting the terminal error verbatim (including shell prompt glyphs, package manager error codes, or tool-specific prefixes), then following with the correct expected behavior or command. He does not narrate what he tried or why it failed — the error is the evidence.

**Pattern:**
```
<raw terminal error pasted verbatim>

<restatement of expected behavior OR the correct flag/path>
```

**Examples:**

> "irread: auto-detect: device 0b48:2003 not found under /dev/bus/usb\n\nStart the container with --device /dev/bus/usb/BUS/DEV:/dev/bus/usb/BUS/DEV"

> "10.02 E: Unable to locate package docker-compose-plugin\nrun \"make\" yourself until it works"

> "install \"docker compose\" in the Dockerimage. right now it gives ╰─$ docker compose\ndocker: unknown command: docker compose"

Note: when he pastes a longer error mid-session, he may add a sentence of context before it (e.g., "locally in my ~/.config/... I've added..."), but the error itself is always raw.
