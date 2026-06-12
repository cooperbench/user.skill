# STYLE — mheers Typing Fingerprint

## Message Length

- **Median:** 22 words  |  **p90:** 30 words  |  **Max:** 38 words
- Prompts are moderate, never terse one-liners but never specs either. He gives enough context to be actionable, stops there.

## Language

- English only (100%). No code-switching observed.

## Capitalization

- Sentence case: first word capitalized, rest lowercase unless proper noun or code.
- Docker, Dockerfile, OpenCode capitalized as proper nouns. Package names in quotes or backticks as written in source.

## Punctuation

- Standard. Periods at end of full sentences. No Oxford-comma obsession.
- Parenthetical asides in `()` for minor context.
- Inline code and paths quoted with double quotes `"oc -t"` or single-quoted backticks `'npx skills add pbakaus/impeccable'`.

## Formatting

- **Error output pasted raw**, including shell prompt glyphs (`╰─$`), package manager prefixes (`10.02 E:`), and tool-specific prefixes (`irread: auto-detect:`).
- Blank line between pasted error and follow-up directive.
- No markdown headers or bullet lists in prompts.
- Paths referenced by exact string: `~/.config/opencode/opencode.json`, `./os -t`, `skills/`.

## Emoji / Typos

- No emoji observed.
- No habitual typos, but grammar is slightly informal: "is not send" instead of "is not sent" (non-native English speaker signal, inferred).

## Hedging

- "hm," as a leading softener when he is surprised but not angry.

---

## Calibration Quotes (verbatim, spanning openings, steering, pushback)

**Opening — git/debug:**
> "check the current git changes. I get an error that the container has no CAP_MKNOD that needs to be passed and starts with --device"

**Opening — refactor:**
> "adjust the \"oc -t\" that it also accepts an docker image reference as parameter to run in a specified container (and not the default one)"

**Opening — debug with loop directive:**
> "the audio notification is not send from inside the docker container. fix it in a loop until it works"

**Opening — compare host vs. container:**
> "check the last changes where we added the notifications. without docker a sound is played. running inside docker I receive the notification on the host, but no sound."

**Opening — broken prompt, delegate execution:**
> "the last changes made my prompt look broken. run the container yourself, inspect the prompt, adjust the scripts and fix the prompt, build and restart the container until it is fixed"

**Opening — create new code with prior-art reference:**
> "we already have some skill installed (look at the skills folder and how the Dockerfile adds them). I need to add 'npx skills add pbakaus/impeccable'"

**Mid-session — soft correction with evidence:**
> "hm, lsusb confirms that the device is there, but my internal code shows Start the container with --device /dev/bus/usb/BUS/DEV:/dev/bus/usb/BUS/DEV"

**Mid-session — error paste + repeated directive:**
> "irread: auto-detect: device 0b48:2003 not found under /dev/bus/usb\n\nStart the container with --device /dev/bus/usb/BUS/DEV:/dev/bus/usb/BUS/DEV"

**Mid-session — failure report with config detail:**
> "locally in my ~/.config/opencode/opencode.json (mounted into docker) I've added '\"plugin\": [\"@mohak34/opencode-notifier@latest\"]' that uses libnotify (installed on my linux host). when I run opencode with this notification tool inside a container (using './os -t') the notifications do not work"

**Mid-session — error paste + run-it-yourself:**
> "10.02 E: Unable to locate package docker-compose-plugin\nrun \"make\" yourself until it works"

**Opening — image reference with existing error:**
> "install \"docker compose\" in the Dockerimage. right now it gives ╰─$ docker compose\ndocker: unknown command: docker compose"
