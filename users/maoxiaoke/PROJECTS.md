# Projects: maoxiaoke

## maoxiaoke/nazha ★ (dominant — 100% of sessions)

**What it is**: Personal blog and portfolio website. Named "nazha" (哪吒, a Chinese mythological figure). The user's primary creative and professional presence.

**What the user does here**: Frontend refinement. Almost no greenfield features — the sessions are dominated by typography adjustments, layout tweaks, custom MDX component creation, and interaction polish. The blog publishes AI/agent-focused content in Chinese and English.

**Tech stack**:
- Next.js (Pages Router, not App Router) — hydration errors visible in sessions
- React with Framer Motion for animations
- Tailwind CSS for styling
- MDX for blog content with custom components
- pnpm for package management
- Rehype plugins: `rehype-slug`, `rehype-autolink-headings`
- Google Fonts (Gaegu) + custom font files (Moderat, Ashbury, Spectral)
- Dark mode support with ThemeSwitch component
- MCP server configured locally (Claude Code integration)

**Custom components built in sessions**:
- `TableOfContents` — fixed left sidebar with scroll spy, active heading highlighting
- `SideNote` — marginal annotations with connecting line to annotated text, `asChild` variant
- `Footnote` / `ConnectedSideNote` — footnote references with sidenote popup and hover box outline
- Syntax-highlighted code blocks with copy button
- Post list with hover dim effect (non-hovered posts fade to gray)

**Recurring themes**:
- Typography: obsessive tuning of font stacks, letter-spacing, font sizes, and fallback ordering
- Dark mode consistency
- Blog post features: TOC, sidenotes, footnotes, blockquote styling, code blocks
- Interaction design: entrance animations, hover states, transition timing
- Mobile responsiveness (raised as correction, not planned upfront)
- Accessibility (uses `/rams` skill for design reviews)

**Content published on the blog**:
- "Advanced Guide to AI Programming"
- "How to Build Agents" (with Claude Agent SDK focus)
- "What is MCP and How to Use"
- "How to Make HTTP Requests Based on the Onion Model"

**External integrations**:
- X/Twitter: `@xiaokedada`
- WeChat: `nazha_m`
- Lemon Squeezy: `anotherme.lemonsqueezy.com` (sells products)
- RSS feed
- Newsletter

**Date range of sessions**: 2026-02-19 to 2026-02-23 (4-day burst)
