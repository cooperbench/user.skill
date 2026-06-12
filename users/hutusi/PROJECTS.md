# Projects: hutusi

## hutusi/amytis ★ (dominant — 100% of sessions)

**What it is**: An open-source Next.js + Bun digital-garden/blog framework. It is a template/starter that other developers deploy as their own site. hutusi is the sole author building it as a public framework, not just a personal blog.

**Tech stack**:
- Next.js App Router with `output: export` (static site generation)
- Bun as package manager and runtime
- TypeScript throughout
- Tailwind CSS
- Vercel for the demo site (`amytis.vercel.app`)
- Nginx on a self-hosted Linux server (static export deployment)
- CodeRabbit for automated PR reviews
- Playwright for mobile compatibility tests

**Content model** (inferred from prompts):
- **Posts**: Long-form articles, live at configurable `/posts/[post]` or `/[series]/[post]`
- **Flows**: Daily journal entries (`content/flows/YYYY/MM/DD.md`), Obsidian daily notes analog
- **Notes**: Short notes (`content/notes/[slug].md`), Obsidian regular notes analog
- **Series**: Ordered collections of posts; supports sub-collections ("collection series")
- **Books**: Book chapter collections with their own URL structure
- **Static pages**: About, Archive, Tags, Links, Subscribe

**Features being built during the observed sessions** (March 2–11, 2026):
- Comments and share sections for Flow and Note pages
- Obsidian vault import script (`import-obsidian`)
- `create-amytis` CLI (npm package: `bunx create-amytis my-blog`)
- RSS/Atom feed improvements (configurable output, npm package, content type)
- i18n disable mode (single-language config)
- Image zoom feature
- Mobile responsive improvements (Samsung Galaxy S8+, iPhone SE, Huawei, Xiaomi, Oppo, Vivo)
- WebP image optimization for static export
- Collection series (Series containing other Series or posts)
- Post URL restructuring (`/posts/[post]` vs `/[series]/[post]`)
- Commentable flag per content type
- Custom footer links (ICP filing info, configurable sections)
- Tag case-insensitivity
- Nginx config (SSL, trailing slash, custom 404)
- Build-time error for series/config name collisions
- Deployment documentation and troubleshooting guide

**Recurring themes**:
- Mobile UI bugs discovered via Chrome DevTools on real device emulation
- Vercel vs. static-export parity gaps
- CodeRabbit review cycle after each PR
- Config ergonomics (how `site.config.ts` should look for single-language vs i18n sites)
- Commit discipline (scope of each commit, conventional commit messages)
