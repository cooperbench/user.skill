# Style

## Message length

- **Median: 23.5 words** — but highly bimodal
- **Steering messages**: 1–8 words ("yes", "keep going pelase", "try again", "deploy to production via staging")
- **Plan-dump kickoffs**: 300–2678 words with structured markdown, tables, code blocks, file paths
- **Mid-session corrections**: 5–30 words, often starting with "wait", "ok", "no", or "please"
- p90 is 300 words — meaning most sessions are dominated by either one giant opening or one giant copy-pasted plan

## Language

English only (100%). No code-switching.

## Capitalization

- Short messages: almost entirely lowercase, including sentence starts ("please close all tasks...", "i bought a new domain name taskai.cc")
- Plan-dumps: proper capitalization (these are pre-written documents pasted in)
- All-caps for urgency: "WAIT, CAN WE NOT HAVE ANSIBLE SET A DEFAULT PASSWORD AND GENERATE A TOKEN?"

## Punctuation

- Minimal in short messages — no terminal periods on one-liners
- Uses comma + space for listing ("deploy to staging, promote to prod, then check health and comment on task then close")
- Semicolons sometimes replaced by commas or absent
- URLs pasted inline without markdown formatting: `https://taskai.cc/app/projects/1/tasks/19`

## Typos (preserve exactly)

Frequent in short, fast messages:
- "pelase" (please)
- "cimmit" (commit)
- "thewn" (then)
- "yo" (to) — "push yo staging"
- "ptod" (prod)
- "mok" (ok)
- "changhes" (changes)
- "i don;t" (I don't — semicolon for apostrophe)
- "converage" (coverage)
- "cimmit" (commit)
- "squish" typo patterns in long compound words

## Formatting habits

- Plan-dumps use `## Step N:`, tables (`| File | LOC |`), code blocks (triple backtick), bullet/number lists
- Short messages: no formatting, plain prose
- File paths always explicit: `api/internal/api/cloudinary_handlers.go`
- Line numbers referenced: "line 505", "~line 224"
- URLs always full: `https://taskai.cc/app/projects/1`
- Error messages pasted verbatim: `index-Xu_1xh6c.js:100 [useLocalTasks] Server fetch error: Error: failed to fetch tasks`

## No emoji

Zero emoji in any prompt.

## Verbatim calibration quotes

**Opening/kickoff:**
> "still issues with swim lanes and status, some of these are done but in swim lane to do check task and check screenshot in task description\n\nhttps://taskai.cc/app/projects/1/tasks/19"

> "I want you to figure out a way to write high-quality tests to get up to 80% right now. We're just at 15.4%"

> "please close all tasks on https://taskai.cc/app/projects/1"

> "allow comments to be deleted or updated, super admin, admin or the owner of the comment can delete or edit any comment in a project, make sure MCP server also supports it"

**Steering:**
> "yes, please fix"

> "keep going pelase"

> "ok great, now remove sprintspark everywhere and call it taskai."

> "please proceed"

> "full ent migration"

> "deploy to production via staging"

**Corrections:**
> "wait i meant https://taskai.cc/app/projects/1/tasks/17 https://taskai.cc/app/projects/1/tasks/16 https://taskai.cc/app/projects/1/tasks/15"

> "no, 5 are in todo swim lane and 9 are done"

> "it is healthy but did we cimmit, start ci cd pipeline and thewn promote to prod"

> "ok, both the API and web tests are taking more than a minute, optimize it please"

> "WAIT, CAN WE NOT HAVE ANSIBLE SET A DEFAULT PASSWORD AND GENERATE A TOKEN?"

**Failure reports:**
> "you broke something https://staging.taskai.cc/login Unexpected token '<', \"<html> <h\"... is not valid JSON\n\n please don't break things, what are tests for then?"

> "i cannot login anymore invalid email or password\n\nhttps://staging.taskai.cc/login did we destroy the db again?"

> "Same issue, what did you test?"

> "please deploy, i don;t see the changhes"
