# Persona: maoxiaoke

## Background (inferred)

Chinese developer, likely based in mainland China or Taiwan given WeChat presence, Gaegu/PingFang
font choices, and Chinese-language writing. Blogs in both Chinese and English. Maintains a
newsletter and a "digital garden." (inferred) Probably a frontend-leaning product engineer or
indie developer — the technical depth is solid (knows Tailwind internals, CSS specifics, rehype
plugins, MDX, pnpm lockfiles) but the work is almost entirely self-directed single-developer.

## Domains

- Personal website / blog development (primary)
- Typography and visual design
- AI/agent tooling (writes about it; has blog posts like "Advanced Guide to AI Programming" and "How to Build Agents")
- MCP / Claude ecosystem (has MCP server configured, writing posts about it)

## Role (inferred)

Likely indie developer / content creator / small-product maker. Sells products on Lemon Squeezy
(`anotherme.lemonsqueezy.com`). GitHub: `maoxiaoke`, WeChat: `nazha_m`, X/Twitter: `@xiaokedada`.

## Seniority signals

- Knows exact CSS properties and values (letter-spacing: 1px, outline-offset, text-decoration-thickness)
- Uses Tailwind class names directly ("USE TEXT-XL", "`font-moderat`", "`tracking-[1px]`")
- Understands browser font fallback cascade; specifies: Spectral → Ashbury → PingFang SC → Hiragino Sans GB → Microsoft YaHei
- Aware of Next.js hydration issues, pnpm lockfile mechanics
- Uses `rehype-slug`, `rehype-autolink-headings`, MDX custom components
- Knows what React component is rendered where by reading the component tree in Page Feedback
- (inferred) Mid-level to senior frontend skill; not a beginner but not an infra engineer

## Attitude toward the agent

**Skeptical and impatient.** Trusts the agent to execute, not to decide. Gives specific pixel
values and font names rather than letting the agent choose. Corrects immediately when the agent
over-explains, adds unsolicited flourishes, or misinterprets scope. The 73% correction rate and
frequent interruptions signal that the agent rarely gets it right in one shot. The user does not
praise the agent; satisfaction is expressed by silence or a single "oik"/"OK".

When the agent produces a long summary of changes, the user ignores it and sends the next
correction. When the agent explains its logic, the user ignores the explanation.

## Communication style summary

- Chinese when requesting nuanced design changes or iterating
- English ALL CAPS when the agent did something wrong or needs an urgent directive
- Terse English for git operations and one-off directives
- Never apologizes or softens requests
- Pastes build errors verbatim; pastes URLs verbatim; pastes exact error HTML when debugging
