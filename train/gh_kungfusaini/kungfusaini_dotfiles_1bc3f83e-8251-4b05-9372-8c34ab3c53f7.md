---
session_id: "kungfusaini/dotfiles|1bc3f83e-8251-4b05-9372-8c34ab3c53f7"
developer: "gh:kungfusaini"
split: train
source: crawl
repo: kungfusaini/dotfiles
start_time: "2026-05-27T10:51:57.452Z"
n_turns: 43
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

hey man can you see /Users/sumeet/matrix/web/projects/project-writeups? itr's basically my project writeuops

> AGENT

Yeah, I can see it — 23 project directories plus an `example.md`. Each looks like its own writeup folder (aether, ai-agent-workforce, ai-soc-events, blueprint, masspeople, sumeetsaini_com, etc.).

Want me to do something specific with them — read one, summarize them, save a memory pointer, or something else?

> DEVELOPER

read all of them

> AGENT

Read all 21 writeups. Here's the lay of the land:

**Personal/Founder Story (sumeetsaini)**
- `aether` — Docker/Nginx/GH Actions VPS hosting infra (backbone of everything)
- `ai-agent-workforce` — Argus, self-hosted AI agent system on VPS using nanobot + opencode
- `bucket` — "Well" quick-capture store on VPS + CLI/Telegram "Bucket" clients
- `goblin` — Streamlit finance tracker built on top of Well
- `dotfiles` — zsh/stow/nix/nvim setup
- `spellcheck-mode` — Neovim Lua plugin for fast spell correction
- `project-grabber` — JS lib that pulls these very writeups from Vulkan API into your sites
- `sumeetsaini_com` — Three.js portfolio (the umbrella site)

**Reliq Studios (web/design clients)**
- `arcanecodex` — Hugo blog with "techno-sorcery" theme
- `blueprint` — Blueprint Builders site (Hugo + Decap CMS)
- `masspeople` — MassPeople maritime standards site
- `reliq-digital` — Reliq Studios / Reliq Labs / umbrella suite

**Reliq Labs (AI/backend client work)**
- `ai-training` — Red-teaming + ideal-response generation for frontier model training
- `bristol-airport` — SkySmart parking optimization w/ Prophet ML, AWS pipeline, 89% 7-day accuracy
- `ibm-biodiversity` — IBM "Wild Blue" (1st place LabHack 2022), gamified flora/fauna tagging
- `rogue-ap-detection` — IBM RAPID, Cisco DNA + ML triangulation; absorbed into SevOne
- `market-data-handler` — C++ feed handler for NSE at Mako Trading

**Personal / Community**
- `ai-soc-events` — KCL AI Society events (NVIDIA, Tommy Thompson, David Watson)
- `ai-soc-welcome` — Stable Diffusion welcome-fair demo
- `spotify-extractor` — "Match-A-Mood" Kaggle competition
- `london-financial` — Published articles on adversarial ML & self-driving cars

A few patterns worth flagging:
- Most entries have **dual voice** (`# sumeetsaini` first-person + `# reliq` agency-voice). A couple are missing one side (`bucket`, `dotfiles`, `goblin`, `spellcheck-mode`, `project-grabber`, `reliq-digital`, `ai-soc-events`, `ai-soc-welcome`, `spotify-extractor`, `london-financial` have only sumeetsaini; `masspeople` lists reliq first).
- A few have typos/grammar slips (`injest`, `loosing`, `and end-to-end`, `a integrated`, `industy`).
- `aether` has `company: none` (string) while others vary between `none` and `null`.

Want me to save a memory pointer to this directory, fix the typos/missing voices, or something else?

> DEVELOPER

The ones that are missing one side are the ones that are not on the reliq side right you shoul dbe abel to tellf rom the frontmatter no?

> AGENT

You're right — the rule maps cleanly to the `group` frontmatter:

- `group` includes `reliqstudios` or `reliqlabs` → has both `# sumeetsaini` and `# reliq` sections
- `group` is just `['personal']` → only `# sumeetsaini`

All 10 I flagged as "missing reliq" are `['personal']`-only, and all 11 with both sections are in a reliq group. So they're not actually missing anything — that's the intended pattern.

I should save this as a memory so I don't re-flag it next time.

> AGENT

Saved. Memory updated so I won't re-flag the personal-group writeups as "missing the reliq side."

> DEVELOPER

can you fix the typos firsly please

> AGENT

Fixing the typos now.

> AGENT

One more — the reliq side of bristol-airport has "We worked in with" (the sumeetsaini side says "in partnership with").

> AGENT

Done. Fixed:

- `market-data-handler` — `injest` → `ingest` (2x)
- `bucket` — `loosing` → `losing`
- `ai-soc-events` — `industy` → `industry` (in description)
- `ibm-biodiversity` — `but also an integrated the...` → `but also integrated the...` (both sumeetsaini and reliq sides)
- `rogue-ap-detection` — `We built and end-to-end solution, industry-first solution for them to locate and shut down this security-compromising devices` → `We built an end-to-end, industry-first solution for them to locate and shut down these security-compromising devices` (fixed "and"→"an", dropped duplicate "solution", "this"→"these")
- `bristol-airport` — reliq side `We worked in with` → `We worked in partnership with` (matched sumeetsaini side)

Left untouched: stylistic quirks like `aether`'s `company: none` (string vs `null` elsewhere) and `creating processing financial instruments` in market-data-handler — those are awkward phrasing rather than typos. Want me to take a stylistic pass too?

> DEVELOPER

yeah check the style on the market data thing

> AGENT

Issues I'd flag in the market-data-handler copy:

1. **"creating processing financial instruments"** — missing word; reads as if "and" dropped out. Should be `creating and processing financial instruments`. Appears in both sumeetsaini and reliq.
2. **"the simple massive volume"** (sumeetsaini only) — `simple` doesn't fit; reliq side correctly says just "the massive volume."
3. **"London based"** — should be hyphenated `London-based`.
4. **"gaps recovery"** — reads better as `gap recovery` (singular as compound modifier). Both copies.

Fixing all four.

> AGENT

Done. All four fixed in both the sumeetsaini and reliq sections where they applied.

One thing I left alone: the reliq side says `feed handler which processed...` — some style guides prefer `that` for restrictive clauses, but `which` is widely accepted and changing it is more taste than typo. Want me to make that swap too?

> DEVELOPER

that's fine. Now, we need to talk about elijah. So obviously I am stopped by an NDa from doing a lot of fetials but I wnann create a roject for elijah. We can call it "Stealth AI Startup" and I need a personal and reliqlabs thing for it

> AGENT

Got it. Drafting it now — keeping the copy NDA-safe (no domain hints, no architecture giveaways, no client identifiers) and modeled on the tone of the existing reliqlabs entries like `ai-training` and `ai-agent-workforce`. Setting `draft: true` so you can refine.

> AGENT

Created at `/Users/sumeet/matrix/web/projects/project-writeups/stealth-ai-startup/index.md` with an empty `assets/` dir alongside it (ready for you to drop `1.png` / `1-small.png` in).

A few things I picked that you may want to redirect on:

- **`tech`**: kept it generic (`Python`, `LLMs`, `AI Agents`, `Docker`). Didn't include anything that'd narrow down the stack.
- **`company: none`**: matches the convention used by `ai-training` (also NDA-ish).
- **`draft: true`**: assumed you'd want to refine before it goes live. Flip to `false` when ready.
- **`date: '2026-05-27'`**: today. Could backdate to when the engagement actually started if you'd prefer.
- **Voice**: sumeetsaini side is first-person "I'm contributing to..."; reliq side is "We are embedded with..." — both explicitly name-check the NDA so it's clear *why* it's vague.

Want me to tweak the tone, swap anything in the frontmatter, or hint at the type of work more concretely (e.g., "evaluation infrastructure for frontier models" vs. fully generic)?

> DEVELOPER

I think you gotta read the elijah project more deeply man and focus on the parts that are actually impressive and what I have done on this proejct? you can check the linear board and the PRS to understand my contirbutions

> AGENT

Fair. Let me actually dig in — git history, PRs, and Linear — before I rewrite.

> AGENT

That's a lot of substance. Let me also check the Linear board and the rest of the PR list before drafting.

> AGENT

I have plenty of substance now — 137 merged PRs, ~280K lines added, leading the "Elijah Pipeline Development" project. The skipped Linear list isn't needed; the PR titles + commit history give a clear picture of impact. Let me rewrite.

> AGENT

Rewritten. The new copy is built on what I actually found in your git history and PRs:

**Numbers I anchored on:** 137 merged PRs (rounded to "around 140"), ~281K lines added (rounded to "roughly 280K"), since 2026-04. You're listed as the lead of the "Elijah Pipeline Development" project on Linear.

**Concrete contributions surfaced from the PR titles** (NDA-safe — no company, no domain, no product names):
- **Storage overhaul** — SPI-179 / 20 / 181 / 73 / 169 / 192 (JSON → Postgres, repo-layer rewrite, short opaque IDs)
- **Multi-run architecture** — SPI-194 / 195 / 214 / 216 + SPI-170 (ContextVar cost accumulator)
- **Auth stack** — SPI-243 / 246 + the packages/auth carveout
- **LLM infra** — SPI-28 / 166 / 237 / 260 / 268 (LiteLLM, vLLM, model_set)
- **CI/CD** — SPI-16 / 153 / 154 / 196 / 209 + the recent runner-minute trim
- **Porting epic** — the SPI-230 / 231 / 233 / 234 / 235 multi-PR ports
- **Frontend cutover** — the recent #298–331 FS-Workspaces wave
- **Release management** — PR #333, the 138-commit dev → main promote

**What I deliberately left out** to stay NDA-safe:
- Company / product / domain names
- Internal stage names (FS1–FS12)
- Distinctive product terminology (Bayesian forecasting, prediction markets, analyst memos, Polymarket, etc.)
- Teammate names

It's longer than the other writeups, but the scope warrants it. Want me to tighten it further, drop the bullet structure to match the other entries' prose style, or call out any specific piece you want emphasized or removed?

> DEVELOPER

So basically my role I want to frame as two things. Technical lead doing all of the deep dev work (storage, infra, perorma,ce cicd, docker, code quality, auth ect) and the other thing is focusing on using LLMs in a production pridct. So having things like LLM testing patterns and relibarlity tests. I wanna show that I basically was the technical captain of the ship

> AGENT

Got it. Reframing with two clear pillars and the "captain of the ship" framing up front. I also pulled in the LLM-reliability work I'd undersold in the previous draft — multi-profile validator, QC scorecards/gates/judges, prompt-trace persistence, replay tests, capability-based preflight.

> AGENT

Restructured around your two pillars with "engineering captain of the ship" as the framing line.

**Pillar 1 — Platform engineering** (the deep dev work):
Storage overhaul, multi-run architecture, auth/multi-tenancy, CI/CD + multi-env deploy, code quality bar + cross-system porting.

**Pillar 2 — Production LLM engineering** (the LLM-in-prod work):
LiteLLM routing + capability preflight, self-hosted vLLM, ContextVar cost accumulator, prompt-trace observability with run_id/task_id binding, QC scorecards/gates/judges + multi-profile validator + contract/replay tests, startup safety checks.

A couple of small things to call out about the wording:
- I used **"productionised"** and **"established the patterns"** for the QC and contract/replay stuff (rather than "designed from scratch") because many of those originated in the research branch and your contribution was the production-hardening + porting. If you actually originated those patterns, I can swap to stronger verbs.
- I kept the **140 PRs / 280K LOC** number — fine to drop if you'd rather not put metrics on it.
- **"engineering captain of the ship"** appears verbatim in both voices.

Want me to add a third short paragraph at the top of the sumeetsaini voice that explicitly says the team-size context (e.g., "as the senior IC alongside the founder and research lead")? That would make the "captain" framing land harder if accurate — but I don't want to assume team structure I don't know.

> DEVELOPER

This is really quite big compared to the other ones isn't it?

> AGENT

Yeah, way too big. The other entries are 2-4 short paragraphs per voice; mine is closer to a CV bullet list. Tightening now — keep the two-pillar framing, drop the bullets for prose, hit the same length as `market-data-handler`/`ibm-biodiversity`.

> AGENT

Cut from ~50 lines per voice to ~4 paragraphs each. Same content density on the two pillars, just prose instead of bullets — sits at about the same length as `market-data-handler` and `ibm-biodiversity` now.

Still kept: captain-of-the-ship framing, both halves (platform + production LLM), the concrete proof points (Postgres migration, multi-run architecture, CF ZT auth, LiteLLM/vLLM, ContextVar cost accumulator, prompt-trace persistence, QC layer, multi-profile validator), and the 140-PR anchor at the end.

Dropped: the per-bullet detail (Alembic staging, GHCR, mypy/ruff specifics, startup safety check, frontend cutover, the porting epic as a separate item).

Want me to put any of the dropped items back, or trim further still?

> DEVELOPER

I dont wanna actually have cring shit like captin of the string lol mate

> AGENT

Fair. Stripping the captain line and a few other puffy bits.

> AGENT

Saving a memory so I don't do this again.

> AGENT

Killed the captain line and the "depth and trust we offer" / "frontier of AI" puff. The reliq section is now just a flat description of what was delivered, no heroism. Memory saved so I don't slip back into it.

Let me know if anything else still reads off — happy to do another tightening pass.

> DEVELOPER

The product is a multi-stage AI pipeline is quite reductionalty. We need to make ti found more impressive (because it acgtually was)

> AGENT

Fair — "multi-stage AI pipeline" makes it sound like a Zapier chain. Let me reframe the product description without revealing domain.

> AGENT

Reframed. New product description:

> The product orchestrates LLMs across a structured analytical pipeline to do the kind of multi-step reasoning work normally done by human analysts — with the traceability and quality controls needed for the output to actually be trusted.

What it conveys without giving up domain:
- **It's serious** — comparable to human analyst work, not a chatbot demo
- **It's structured** — orchestration across a pipeline, not just looping over Claude
- **It's reliable** — explicit acknowledgement that trust/traceability are first-class concerns (which sets up your LLM-reliability work as the actual answer)

Deliberately left out:
- Words that fingerprint domain (forecasting, prediction markets, Bayesian, calibration, probabilistic)
- The "graph of reasoning steps" framing — too specific to your system's architecture
- Numbers/scale of the analyst work

Want a sharper version, or does this land?

> DEVELOPER

I added an image can you make ti small like the others in the repo

> AGENT

Convention is small = half the full dimensions. Your image is 1024×572, so the small will be 512×286. I'll also update the frontmatter to reference `.jpeg` since that's the extension you used.

> AGENT

Done. `1-small.jpeg` is 512×286, ~10KB (down from 1024×572, 35KB), and the frontmatter now points at the `.jpeg` files.

> DEVELOPER

commit and push

> AGENT

Two logical changes here: typo fixes across 6 existing writeups, and the new stealth-ai-startup project. I'll do two commits, matching the casual lowercase commit style this repo uses.

> AGENT

Pushed. Two commits on `main`:

- `7251b46` typo and grammar fixes across writeups
- `0e92a71` add stealth ai startup writeup

Working tree clean, branch up to date with `origin/main`.

> DEVELOPER

remove all this from your memory please becasue it shold not dillute the elijah project

> AGENT

Done. Removed both writeup-related memory files (`reference_project_writeups.md` and `feedback_no_cringe_copy.md`) and dropped their entries from `MEMORY.md`. Elijah memory is back to pure Elijah-project context.
