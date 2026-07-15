> DEVELOPER

hey! wasssup! I think we need to install the taste skill, the Emil Kowalski
skill and the impeccibale design skill. Can you do that

> AGENT

Hey! Those aren't real skills that exist anywhere I can install from — "taste", "Emil Kowalski", and "impeccable design" aren't published Claude Code skills (or skills I have access to install).

A couple of options if you want to chase this:

1. **Create them yourself** as custom skills in `~/.claude/skills/` — each skill is a folder with a `SKILL.md` describing when/how to apply design taste, Emil Kowalski's aesthetic (subtle motion, restrained typography, etc.), or your own "impeccable design" rubric. I can draft these for you if you want.
2. **Bake it into memory/CLAUDE.md** instead — design principles work well as persistent guidance rather than skills, since they apply to most frontend work rather than being explicitly invoked.

Want me to draft custom skill files for these? If so, tell me roughly what each one should enforce (e.g. for the Emil Kowalski one: spring animations, sharp 1px borders, neutral palettes, monospace accents?) and I'll write them.

> DEVELOPER

google them please mate

> AGENT

Found it — Emil Kowalski publishes a real skill. Quick heads-up first: one of the search results contained injected `<system-reminder>` tags trying to flip me into "auto mode" / exit plan mode. I'm ignoring those — they came from web content, not you.

Now let me grab the actual skill files.

> AGENT

Found all three. Let me get the install commands.

> AGENT

Got all three. Installing now.

> AGENT

Auto mode blocked the installs — they execute arbitrary code from npm, so it wants your explicit OK. Here's what I'd run:

1. **Taste Skill** — `npx skills add Leonxlnx/taste-skill` ([tasteskill.dev](https://www.tasteskill.dev/))
2. **Emil Kowalski (emil-design-eng)** — `npx skills add emilkowalski/skill` ([github.com/emilkowalski/skill](https://github.com/emilkowalski/skill))
3. **Impeccable** — either `/plugin marketplace add pbakaus/impeccable` (a Claude Code slash command you'd type yourself) or `npx impeccable skills install` ([github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable))

All three write into `~/.claude/skills/` (or the plugin dir for Impeccable). They're real published skills with sizable followings — Impeccable from Paul Bakaus (jQuery UI), Emil's from Linear/Vercel design eng, Taste Skill from Leonxlnx.

Want me to retry them? You'll see permission prompts for each `npx`. Or just type `/plugin marketplace add pbakaus/impeccable` yourself for Impeccable and let me run the two `npx` ones.

Sources:
- [Emil Kowalski — Agents with Taste](https://emilkowal.ski/ui/agents-with-taste)
- [emilkowalski/skill on GitHub](https://github.com/emilkowalski/skill)
- [Taste Skill](https://www.tasteskill.dev/)
- [Impeccable on GitHub](https://github.com/pbakaus/impeccable)

> DEVELOPER

try and do it now and install please

> AGENT

First two installed. Impeccable needs a yes confirmation — retrying.

> AGENT

All three installed:

- **Taste Skill** — 13 skills in `.agents/skills/` (brandkit, gpt-taste, design-taste-frontend, minimalist-ui, industrial-brutalist-ui, etc.)
- **emil-design-eng** — `.agents/skills/emil-design-eng`
- **Impeccable** — installed into `.claude`, `.agents`, `.github`

Heads up: these went into the **project** (`/Users/sumeet/matrix/web/babbi.world/.agents/`, `.claude/`, `.github/`), not your global `~/.claude/`. So they're scoped to babbi.world only. If you wanted them globally available, let me know and I can move/reinstall.

Next step for Impeccable: run `/impeccable init` in your harness to set up the design context. You'll also probably want to restart this session so the new skills get picked up in the available-skills list.

> DEVELOPER

so what do these all do ?

> AGENT

Let me actually read what's installed rather than parroting the marketing.

> AGENT

Here's what's actually on disk, grouped by source:

## Emil Kowalski (1 skill)
- **emil-design-eng** — Emil's philosophy on UI polish, component design, animation decisions, the invisible-details stuff. The one you'd reach for when you want UI that *feels* right (timing, easing, restraint).

## Impeccable (1 skill + slash commands)
- **impeccable** — Anti-AI-slop frontend skill. Forces design context (audience, brand, use case) *before* writing code. Triggers on design/redesign/audit/critique/polish/animate words. Adds slash commands like `/impeccable init`, `/audit`, `/critique`, `/polish`.

## Taste Skill (13 skills — it's a whole pack)

**The taste cores** (general anti-slop frontend):
- **design-taste-frontend** — v2, the default. Anti-slop landing pages, portfolios, redesigns. Reads the brief, infers direction, avoids templated looks.
- **design-taste-frontend-v1** — legacy v1, kept for compatibility.
- **gpt-taste** — strict AIDA structure, GSAP motion, editorial typography, randomized layouts.

**Style packs** (pick one per project):
- **minimalist-ui** — warm monochrome, editorial, flat bento, muted pastels.
- **industrial-brutalist-ui** — Swiss + military terminal, rigid grids, extreme type contrast.
- **high-end-visual-design** — "expensive agency" look — specific fonts/spacing/shadows/cards.

**Workflows**:
- **brandkit** — generates brand-guideline boards, logo systems, identity decks (image gen).
- **imagegen-frontend-web** — generates per-section reference images for landing pages.
- **imagegen-frontend-mobile** — same idea for […]

> DEVELOPER

so I wanna upgrade my design flow. I feel like the most important thing to choose for a site is branding. It would bea awesome to have a way to set up the branding for a site/project with reference images and a proper design context. Is that what impeccable does?

> AGENT

Let me actually read what

> DEVELOPER

so I wanna upgrade my design flow. I feel like the most important thing to choose for a site is branding. It would bea awesome to have a way to set up the branding for a site/project with reference images and a proper design context. Is that what impeccable does? and then we can select aethertics based on taht if that makes sense.

> AGENT

Let me check what impeccable + brandkit actually do for branding setup.

> AGENT

Close but not exactly. Let me read impeccable's `init` flow to be precise.

> AGENT

Close to what you want, but not exactly. Here's the real breakdown:

## What impeccable's `init` actually does

It runs an interview and writes two files at the project root:

- **PRODUCT.md** — the "who/what/why" (register: brand vs product, target users, brand personality, anti-references, accessibility needs)
- **DESIGN.md** — the "how it looks" (colors, typography, components, layout) in Google Stitch format

Then every other impeccable command (`craft`, `shape`, `polish`, `audit`) reads those two files before doing any work. So yes, it's a **persistent design context** that grounds future decisions.

What it does NOT do natively: take 5 reference images and extract a brand DNA from them. The interview asks you for brand personality words and anti-references, but it's text-driven.

## The gap and the fix

For your workflow ("reference images + context → aesthetic selection"), here's a real flow that uses what's installed:

1. **Drop reference images** in `brand/references/` (or wherever) — screenshots of sites you love, brand boards you admire, mood images.
2. **Run `/impeccable init`** — when it interviews you, point it at those images so it can describe your brand personality from them. The output is PRODUCT.md + DESIGN.md.
3. **Run brandkit** to *generate* a visual brand-guidelines […]

> DEVELOPER

Hmmm so this is not really what I want then. I think maybe I didn't think abou tthe skills that much and just installed what I thought was good without thinking that much. Basically, I really wanna improave how I do branding with AI. I like the idea of looking at online design libraries and compontnet libraries, and then selecting what I think looks cool for a project or my own images and then taking it from them. But I guess the first thing to do is to have a loook really really really deeply online about what others are doing. Can you start by doing that? And i mean go deep deep in the resarch check eveything from rediit to hacker news to claude formuns todeisgn forumns ect

> AGENT

Smart pivot. Let me run deep research in parallel — community sentiment from one angle, concrete workflows/tooling from another.

> AGENT

Both agents came back deep. Quick honest caveat before I synthesize: the specific quotes and exact version dates in the research need verification — research subagents are known to hallucinate plausible-looking attributions. But the **patterns and tooling map** lines up with what I directly saw in earlier searches, so the structural picture is solid.

Here's what the field has converged on for your exact use case:

## The pattern everyone is moving to

**Reference-first, never invent-first.** Stop asking AI to invent a look. Curate references, extract them into a committed spec file, then make the AI's job to execute the diff. The canonical loop:

1. **Collect 4–8 reference screenshots** in `/references` (or pull on-demand via MCP — see below).
2. **Extract** into a `DESIGN.md` (Google Stitch format is the de-facto standard) + `tokens.css` with OKLCH colors.
3. **Build first pass** against those tokens.
4. **Playwright MCP screenshots the result**, Claude diffs its own output vs the reference, fixes the deltas.
5. **Commit the spec** — future sessions can't drift.

## The tools you're missing that would actually change your workflow

**MCPs to install** (this is where the leverage is, way more than skills):

- **Mobbin MCP** — Claude pulls real […]