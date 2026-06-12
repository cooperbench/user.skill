# Preferences: maoxiaoke

## What they correct (73% of pushbacks are corrections)

The user corrects constantly and specifically. Common correction triggers:

1. **Agent over-interprets scope**: Changes too many things at once, or changes something the user didn't ask about. User redirects with a terse re-statement of what they actually wanted.
2. **Wrong text copy**: "不是 SOME ARE , 是所有的在,或者说更多可以在 LEMON SQUEEZY 找到" — agent used partial language when user wanted inclusive language.
3. **Wrong element removed**: "NO, REMOVE THE AVATAR AND NAME, NOT THE THEME SWITCH + X" — agent removed the wrong elements.
4. **Agent explains too much**: Long agent summaries are ignored; user immediately sends the next correction. Never acknowledge or respond to agent explanations.
5. **Wrong font or wrong fallback**: User has strong font opinions and will immediately correct font stack ordering or wrong font choice.
6. **Wrong pixel value**: Will specify exact values ("字体大小是 18，请改成 16", "outline OFFSET 改成 0px") when agent guesses.
7. **Missed linked URL**: "https://anotherme.lemonsqueezy.com/" — drops the URL again when the agent missed making something a link.
8. **Wrong direction of change**: Will send "可以再宽一点" or "再小一些" as a nudge without explanation.

## What satisfies them

Rare. Signs of satisfaction:
- "oik" — minimal acceptance
- "OK" — same
- "GST" — possibly moving on ("git status"?)
- Silence / next unrelated request
- No correction of a change (very rare)

Non-pushback prompts (21% of turns) are mostly skill invocations, task notifications, and a few
"oik"/"OK" acks — not praise.

## Workflow habits

- **Visual-feedback-driven iteration**: Uses a Page Feedback MCP tool that captures live browser state with React component trees and sends structured feedback. This is the primary way design changes are requested.
- **No planning phase**: Jumps directly into specific changes. Does not ask for plans or explanations before requesting implementation.
- **Does not ask for tests**: Never mentions tests, TDD, or test coverage across all sessions.
- **No code review requests**: Doesn't ask the agent to explain architecture choices.
- **Interrupts rather than waits**: Frequently cancels agent actions mid-stream rather than letting them complete.
- **Iterates on aesthetics in many small passes**: Will revisit the same component (e.g., blockquote, sidenote, TOC sidebar) across multiple turns with incremental adjustments.
- **Git delegation**: Delegates commits and pushes to the agent via "COMMIT AND PUSH" or "NOW, COMMIT AND PUSH". Reports build errors back verbatim for the agent to fix.
- **Images for spec**: Attaches screenshots (`[Image: image/png]`) as design reference without description — expects the agent to interpret.

## Stack preferences visible in prompts

- **CSS/Tailwind**: Knows and specifies Tailwind class names directly. Uses exact pixel values in CSS when Tailwind utility doesn't exist.
- **Fonts**: Strong opinions. Specific fonts used: Gaegu (Google Fonts), Moderat, Spectral, Ashbury, PingFang SC, Hiragino Sans GB. Knows how browser font cascade works.
- **Animation**: Framer Motion (`<motion.article>`, `<MotionComponent>`). Invoked the `/interaction-design` skill for motion guidance.
- **MDX**: Uses custom MDX components (`<SideNote>`, `<Footnote>`, `<ConnectedSideNote>`). Extends them with `asChild` pattern.
- **Package manager**: pnpm. Aware of lockfile issues.
- **Next.js**: Pages router (not App Router). Aware of hydration errors.
- **Dark mode**: Explicitly preserves dark mode toggle when agent removes it.

## Pushback distribution

| Type | Rate |
|------|------|
| correction | 73% |
| non_pushback | 21% |
| failure_report | 4% |
| takeover | 1% |
| rejection | 1% |

The 1% takeover was "NOW, COMMIT AND PUSH" — user took over the git operation rather than
waiting. The 1% rejection was asking to delete the Nav on a post page to "see the effect" —
an exploratory trial rather than a firm decision.
