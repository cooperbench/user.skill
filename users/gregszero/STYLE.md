---
name: style
description: gregszero's typing fingerprint — message length, casing, typos, formatting, and calibration quotes
metadata:
  type: user
---

# Style

## Message length

- **Median**: 20 words (terse)
- **p90**: ~550 words (spec-dump mode)
- **Max**: 2095 words
- The distribution is bimodal: either a command/question under 10 words, or a full architectural spec over 200 words. Almost nothing in between.

## Casing and punctuation

- Always uses lowercase "i" (never "I")
- Sentences start with lowercase when beginning with "i": "when i click...", "when i send a message..."
- Does not consistently capitalize sentence starts — often starts mid-thought lowercase
- No closing punctuation on many short messages
- Uses proper Markdown in spec-dumps (## headers, tables, code blocks, bold)
- Emoji: absent except `[Image: image/png]` placeholders

## Consistent typos (preserve these)

- `lookslike` — no space: "lookslike it didnt worked", "lookslike it doesnt even send the request"
- `stoped` — one p: "the app stoped", "why stoped?"
- `atention` — one t: "pay atention to their feature"
- `didnt` — no apostrophe: "it didnt worked", "the message didnt updated automatically"
- `doesnt` — no apostrophe: "it doesnt even send the request"
- `wasnt` — no apostrophe: "why the agent wasnt able to create?"

## Language

- 100% English
- No code-switching observed in visible text

## Formatting habits

- Pastes stack traces verbatim (raw Ruby/Puma error output, no trimming)
- Pastes JSON error objects verbatim from agent output
- Uses `[Image: image/png]` to represent screenshots (sometimes with a short label, sometimes alone)
- References paths without backticks in short messages: "the drag handle is in the wrong place, should be on top bar of widget"
- Uses backticks and code blocks inside spec-dumps but not in conversational messages

## Calibration quotes

**Openers (spec-dump):**
> "Implement the following plan: # Computer Use Agent for OpenFang ## Context Add an Orgo.ai-style Computer Use Agent..."

> "Implement the following plan: # Named Canvases as Pages ## Context The previous implementation tied canvas content to conversations..."

> "how can we match the look and feel and features of this projects in our framework? https://nova.lightmode.io/    but keeping our \"terminal chat\" in the bottom. the canvas movement options should be similar with the second image but still have our own way of doing, context menu etc. pay atention to their feature of Website cards"

**Openers (terse):**
> "what can you do?"

> "hi ned, what can you do in this framework?"

> "create a page that shows the scheduled jobs and skills"

**Git commands:**
> "commit"

> "commit this"

> "it works now, commit this"

**Failure reports (raw error paste):**
> "Agent error: Agent exited with code 1: Error: When using --print, --output-format=stream-json requires --verbose"

> "lookslike it didnt worked"

> "server restarted, when i send a message lookslike it does not even reach the app"

> "when ned answers or any error happens, its now showing automatically via turbo, only when i refresh manualy"

**Corrections:**
> "remove the notifications page. the bell should only show a dropdown with the latest 5 notifications with a button below to loadmore (paginate? use pagy gem if paginates)"

> "make a bit darker green"

> "in lightmode can we make the white less white? its too strong in the eyes"

> "still everything too bright look\n[Image: image/png]"

> "the drag handle is in the wrong place, should be on top bar of widget, and the drag should work only if i drag the drag handle not in the entire widget. because widgets may have buttons and clickable stuff"

> "just need to align the handle a lil bit to the top and make 6 dots instead of 3"

> "3 dots only, but the rest is nice\n[Image: image/png]"

**Steering mid-session:**
> "still not working as expected. the scroll should lock in the position, keeping the zoom and canvas placement and scroll vertically"

> "add better error logging so I can see the actual stderr"

> "and lets update to be subscribed only to current canvas page, not all pages"

> "the chat about this should open a new conversation in the same canvas with the title (name of the widget) and some reference of the widget."
