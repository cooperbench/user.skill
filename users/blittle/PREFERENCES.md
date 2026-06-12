# PREFERENCES

## What he corrects (pushback distribution: correction 35.3%, failure_report 28.9%)

Most pushback is correction (35%) or failure report (29%). True rejections are rare (0.5%).

**Corrects on:**
- UX feel: scroll sensitivity, animation timing, tap zone sizes, footer visibility, overflow by pixels
- Behavior that doesn't match book-reading metaphor ("it should be like a book — flipping from the last page of chapter two should bring you to the first page of chapter 3")
- Layout issues noticed visually ("The homepage layout kinda sucks. Look at the screen shot...")
- Implementation direction he didn't want ("no ugh, you got rid of the stripe and paypal packages")
- Approaches that seem architecturally wrong ("Do we need to take a step back and reconsider how we are doing this?")
- Anything that breaks existing behavior while fixing something else

**Failure reports contain:**
- Exact error text from browser console or terminal
- Exact URL where error occurs
- localStorage JSON state at time of failure
- Steps to reproduce, including "hard refresh" vs "navigating normally"
- Diff between expected and observed behavior

## What satisfies him

- "That appeared to work." — his typical success acknowledgment, brief and factual
- "Okay!" — positive but rare
- Silence + "commit this" — the strongest positive signal; if he says commit right after a change, it worked
- No acknowledgment at all if the output matches his plan exactly

## Workflow habits

- **Plans first, then implement**: writes or co-writes a markdown plan doc, then sends "Implement the following plan:" — does not do exploratory/iterative implementation without a plan for complex features
- **Commits frequently**: separate "commit this" prompts throughout sessions, not at the end
- **Branch and push for PRs**: "create a branch, commit, and push the branch remotely", "Create a pull request with these changes"
- **No test-driven development**: has almost no tests and explicitly says "I don't see a huge amount of value in fine grain unit tests for it"
- **Interrupts freely**: uses `[Request interrupted by user]` mid-tool-use — does not wait for the agent to finish if something looks off
- **Writes plans to files**: "Write the plan to a file so we can track progress in case interrupted" — uses plan docs as checkpointing
- **Does not ask for explanations**: wants results; if he needs to understand something he asks a direct question ("Why does running claude in cursor not allow me to shift+enter...")
- **Changes direction mid-session**: pivots when the current approach isn't working or he gets a better idea (Mind Changer 45.5%)

## Tool/stack preferences

- **Vite** for bundling (no webpack)
- **pnpm** workspaces for monorepo
- **Preact** (not React) — signals for state, hooks for effects
- **TypeScript** — strict, tsup for builds
- **Cloudflare Pages Functions** over Vercel for server-side logic (explicitly chose Cloudflare)
- **Stripe** for payments (not PayPal alone)
- **GitHub Actions** for CI/CD
- **GitHub Pages** for static deployment
- No unit tests; open to e2e but prefers integration testing

## Things he explicitly dislikes

- "Page X of Y" indicator — removed it ("isn't great. Let's just remove it.")
- Scroll-to-change-pages gesture ("too sensitive")
- Animations that run before content is positioned correctly ("the animation on page load sucks")
- Click-to-change-pages on mobile ("On mobile, maybe we should remove the click to change pages")
- Agent summaries after completing a task (he just sends the next command)
- Clutter on marketing pages (moved TOC and offline sections to reader footer)
