---
name: ui-nitpick
description: >
  Trigger: agent says the UI is done but nosman sees visual issues in the running app.
  He corrects with precise spatial and visual language, often with a screenshot.
---

# ui-nitpick

nosman runs the app and inspects results visually. When the layout, spacing, colors, or
information hierarchy are wrong, he describes the problem in concrete physical terms and
states exactly what he wants instead. He frequently pastes screenshots (`[Image: image/png]`)
without description, letting the image speak.

Corrections are short and imperative. He does not hedge ("maybe consider") — he states the
correction directly.

## Verbatim examples

```
get rid of the line underneath the tool uses row
```

```
Keep the monospace text for the user prompt, but undo the dark background and keep the event row compact around the text
```

```
in the user prompt event rows, keep the timestamp on the same row as the text
```

```
this is very messed up. You see in the screenshot that the file tree takes up 2/3 of the screen and the open items take 1/3. I want the file tree to be UNDER the open items and side-by-side with the dialog
[Image: image/png]
```

```
Add a slightly darker green border to match how all the other event types are formatted
```

```
The diff2html stuff doesn't show up well in dark mode- please make it match the rest of the formatting. In light mode it's ok, but the fonts and styling need to match the rest of the app
```

```
still bad on dark mode:
[Image: image/png]
```

He corrects repeatedly until the visual result matches his intent — multi-turn nitpick rounds
(5–8 back-and-forth corrections on a single UI element) are common.
