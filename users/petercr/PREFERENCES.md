# Preferences — petercr

## Pushback distribution

| Type | Rate |
|------|------|
| Non-pushback (accepted) | 55.8% |
| Correction | 26.9% |
| Failure report | 11.5% |
| Rejection | 5.8% |

More than 4 in 10 prompts are some form of pushback — petercr is an active corrector, not a passive approver.

## What triggers correction

- **Incomplete scope:** agent finishes part of the task and declares done, but missed related files or refs. Response: adds the missed item in one clause. Example: "also change the web-app-manifest files and refs in the webmanifest"
- **Wrong element targeted:** agent changed the right type of thing but on the wrong component. Response: "umm that was the shader, not the main background image! we need to address that"
- **Agent asks instead of infers:** when agent asks a clarifying question, petercr supplies the missing info tersely. Example: agent asked "What's the filename?", petercr replied: `"apps/frontend/public/favicon-dark.png"`
- **CSS/layout mismatches:** sizes, proportions, or relationships are off from what the design specifies. Response: states what the correct relationship should be. Example: "we need to adjust the headerPill size to be less than the formCard size. like we did with the rest of the headers"
- **Stale mental model:** petercr points to what they already fixed as context. Example: "ref in this file but i fixed it: /home/peterc/ccw/apps/frontend/src/lib/seo.ts"

## What triggers failure reports

- Code compiles/runs but visual result is wrong: "good news the shader runs, but a couple of things: 1. ..."
- Changes don't seem to apply in browser: "already running, port 3000. check with chrome mcp, seems like code changes didn't have much effect"
- Still broken after agent claimed it was fixed: "opened incog window, still doesn't reload favicon"
- Raw console error pasted verbatim with minimal intro

## What triggers rejection (hard stop)

- Visual result is too extreme or wrong direction: "no it's too wild let's undo those last changes. fallback to when the shader had no image"
- Debugging rabbit hole grows unproductive: "ok enough of this. just put it back how you found it with the package.json. before we started trying to match the versions"

## What satisfies

- "yes it works now. good job."
- "great looks good."
- "good 2 go now"
- Followed immediately by a commit/PR request — satisfaction flows directly into git ceremony

## Workflow habits

- **Plan first on big tasks:** opens with "let's make a plan to do it" for new issues; uses ultraplan for complex implementations
- **Not test-driven:** no mention of writing or running tests; test failures in CI are ignored ("pre-existing environment issue")
- **Commit cadence:** commits at the end of every session or logical unit of work, always into a named feature branch, then makes a PR
- **Visual verification via Chrome MCP:** prefers browser-level confirmation over code review; delegates the checking to Claude ("check Yourself with Chrome MCP")
- **Design via Penpot MCP:** references design frames by name, delegates pixel lookup to Claude ("use the penpot mcp server to view the Desktop page. you can view the frame Intro to see the max widths")
- **Git stash/branch management:** comfortable with stash, branch switches, and pulling — gives these as direct imperative instructions
- **No explanations requested:** doesn't ask Claude to explain what it did; just moves on to next task
- **Results over process:** cares that it looks right in the browser, not that the code is elegant

## Stack preferences visible in prompts

- TanStack Router/Start (routes as `/contact`, `/` landing)
- Vanilla Extract (component names like `headerPill`, `formCard`, `shaderContainer`)
- React with hooks
- TypeScript (`.tsx` files referenced)
- Penpot for design
- Chrome MCP for browser verification
- Sanity CMS (referenced in OG image context)
- GitHub PRs for code review/merge
