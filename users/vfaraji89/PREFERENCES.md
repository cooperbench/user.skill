# Preferences — vfaraji89

## Pushback distribution

- **54.7% non-pushback** — accepts agent output without comment; often follows with "Tool loaded." (harness acknowledgment) or a simple "yes"
- **42.2% correction** — fires a new imperative that ignores agent's summary; does not explain what was wrong
- **2.3% failure report** — pastes raw error output (CI logs, BibTeX errors) verbatim, minimal annotation
- **0.8% rejection** — single-word dismissal: "disconnected", "no"

## What triggers correction

- Agent explains rather than doing ("Want me to bump all three?" → user wanted it done already)
- Agent produces a detailed summary when user wanted a next action taken
- Agent targets the wrong scope (paper when user said extension; website when user said extension)
- Agent misses something that was named in a prior turn ("appendix graf is not updated")
- Agent adds things without being asked (emoji, verbose docs, bold claims in Marketplace copy)
- Version numbers are inconsistent across files

## What satisfies

- Simple "yes" or "Tool loaded." — accepts output silently
- Follows up with the next task rather than acknowledging — agent got it right
- "vercel prod", "pushed now", "see on live marketplace" — signals user is happy and moving forward

## Workflow habits

- **No planning phase**: fires vague openers directly ("in tokalator we have some bugs-- detect first"), expects the agent to plan and execute
- **Sequencing with "first"**: uses "first" to set priority within a message without writing a numbered list
- **Simultaneous tracks**: extension bugs, website updates, and LaTeX paper can all be active in the same session; user switches without preamble
- **Git through agent**: commits, tags, and pushes delegated ("gitingnore paper files and push and commit"), but user also manually pushes sometimes ("pushed now")
- **Images over words**: attaches screenshots for design direction instead of describing
- **Interrupts mid-response**: does not wait for agent to finish wrong work; "[Request interrupted by user]" is common
- **Pastes large context**: drops entire LaTeX files or journal CfPs as context without explanation, then gives 5-word instruction
- **Versioning is meticulous**: tracks v3.1.2/3.1.3/3.1.4 across extension, website, changelog; corrects inconsistencies immediately

## Tool/stack preferences visible in prompts

- VS Code extension (TypeScript) — primary product
- Next.js for website
- LaTeX (Overleaf + GitHub sync) for paper
- Vercel for deployment (`vercel --prod`)
- GitHub Actions for CI/CD
- VSX (vsce) for Marketplace publishing
- Skills CLI (`npx skills add`) for skill distribution
- Recharts for data visualization
- Framer Motion for animations
- Claude Code as the AI coding assistant

## Explanation preferences

- Does NOT ask for explanations unprompted
- When understanding is needed: "why we skipped, what we missed, do we need any new packages?" — asks all sub-questions in one short burst
- Prefers results over step-by-step breakdowns; tables and bullet summaries in agent output are okay but not required
- "no details of formulas" — wants practical, not theoretical exposition
