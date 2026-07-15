---
session_id: "kungfusaini/dotfiles|0a7565de-7500-4adc-b9e0-b313b9cbe819"
developer: "gh:kungfusaini"
split: train
source: crawl
repo: kungfusaini/dotfiles
start_time: "2026-05-09T18:52:01.882Z"
n_turns: 9
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

hey man so can we talk about something. Becasue me and my gf will be colaborating on projecg pyari, I want a shared notes vailt wheere we can write stuff like for exmaple our financial plan. I want evyething to be in markdown, backed up by git and also editable and brosable in a web viier. I don't care what bu what is the best way to do this?

> AGENT

Great question. Given your requirements (markdown files, git-backed, web viewer/editor, two users), here's what I'd recommend:

**Best fit: [Wiki.js](https://js.wiki)**
- Stores pages as `.md` files in a git repo natively (bidirectional sync)
- Clean web UI with markdown editor + live preview
- Multi-user auth (you + Ashlyn)
- Search, tagging, navigation all built in
- Docker one-liner to deploy on your VPS

**Runner-up: [Gollum](https://github.com/gollum/gollum)**
- The engine behind GitHub wikis
- Dead simple — a git repo literally IS the wiki
- Web UI for browsing/editing, every save is a git commit
- Lighter than Wiki.js but the UI is more bare-bones

**Honorable mention: [Silverbullet](https://silverbullet.md)**
- Feels like Obsidian in the browser
- Markdown files on disk, very hackable
- But git isn't built-in (you'd add a cron/hook) and it's more single-user oriented

My vote is **Wiki.js** — it hits every requirement natively without duct tape, the UI is polished enough that Ashlyn won't hate it, and you already have the VPS to host it on. Want me to set it up?

> DEVELOPER

That's a good idea, lets make a ticket in projec tpyari and assign it to me pleas

> AGENT

Let me check the Vikunja setup details first.

> AGENT

Now let me find how we interact with Vikunja — checking for API tools or scripts.

> AGENT

Now I can create the task. Project Pyari is id=5, and Sumeet is user_id=1 (Ashlyn is user_id=2).

> AGENT

Task created (id=75). Now let me assign it to you.

> AGENT

The assignee went through but it blanked the description. Let me fix that.

> AGENT

Done. Created task **#16 — "Set up Wiki.js shared notes vault"** in Project Pyari, assigned to you. You can see it at [task.argbox.net](https://task.argbox.net).

The description includes the requirements and step-by-step plan (Docker setup, git storage backend, user accounts, nginx proxy, SSL).
