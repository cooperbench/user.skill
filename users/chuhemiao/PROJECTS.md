# Projects: chuhemiao

## chuhemiao/portfolio ★ (dominant — 100% of sessions)

Personal portfolio site built with Next.js + MDX, deployed on Vercel. The user's primary coding surface across all 22 sessions. Acts simultaneously as a blog, investment portfolio display, research map, and personal "digital garden".

**Tech stack:** Next.js, MDX, pnpm, Tailwind CSS, Vercel, GitHub Actions  
**Recurring themes:**

### Pages built / maintained
- `/blog` — MDX posts organized by category (research, story, thoughts, tech)
- `/fund` — Investment portfolio page inspired by Paradigm's layout; shows crypto + stocks organized by category with card grid
- `/research` — Crypto project research map with logos and type filters (60+ projects)
- `/stack` — Tech stack showcase
- `/thoughts` — Micro-blog fed by Telegram channel sync via GitHub Actions
- `/fear` (external link) — Fear Dashboard at `watch.kkdemian.com`

### Integrations built
- **Telegram → GitHub Actions sync**: Script that pulls messages from `@kkdemian2050` Telegram channel and commits them to `content/thoughts.json` daily
- **Mermaid rendering in MDX**: Custom rehype plugin + client component
- **Research page logo system**: Uses CoinGecko and CoinMarketCap CDN URLs keyed by ticker; falls back to colored initials

### Content domains the user writes about
- Crypto market analysis (ALT/BTC oscillator theory, DeFi protocols, exchange comparisons)
- Investment portfolio (BTC, ETH, Hyperliquid, Aave, US tech stocks: NVDA, MSFT, PLTR)
- Crypto legends / stories (e.g., Satoshi Nakamoto)
- AI / LLM context and memory research
- Japanese language learning (lingoi app — separate project, appears once in a prompt)

### Recurring pain points
- Vercel build failures that don't reproduce locally
- Data sync scripts overwriting instead of merging
- Logo display (broken images, wrong CDN URLs)
- Lazy loading and page performance as content grows
- GitHub Actions permission errors (bot pushing to protected repo)

## Side projects (mentioned but not in this repo)

- **Stablecoin Flow & Supply Dashboard** — `usdc.kkdemian.com` (separate deployment)
- **Fear Dashboard** — `watch.kkdemian.com` (crypto market regime classification)
- **lingoi** — Japanese vocabulary learning app (JLPT-focused, Next.js + Prisma + Stripe; mentioned once in a spec dump)
