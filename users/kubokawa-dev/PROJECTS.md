---
# kubokawa-dev — Projects
---

## kubokawa-dev/million-pocket-orchestra ★ (dominant — 100% of sessions)

**What it is**: A Numbers4 lottery prediction and tracking web application. Numbers4 is a Japanese government lottery where players pick a 4-digit number (0000–9999); wins pay out for exact match (straight), any order (box), or partial matches (set, mini). The user wants to use ML to maximize their own winning probability.

**What the user does here**:
- Requests new prediction models (LightGBM, ml_neighborhood, lgbm_box, cold_revival, box_model) and keeps pushing to improve their accuracy
- Asks for new GitHub Actions jobs to run daily predictions on a schedule (1:00 AM, every 20 minutes)
- Reports CI failures by pasting GitHub Actions logs verbatim
- Requests mobile UI improvements (responsive tables → card layouts, font modernization)
- Requests SEO improvements ("アラブの石油王に見てもらえるぐらいのSEO対策")
- Pushes to Supabase via PostgREST UPSERT from CI scripts

**Tech Stack**:
- **Backend / ML**: Python 3.11, LightGBM, custom statistical models, GitHub Actions, Supabase/PostgreSQL (via PostgREST), pnpm
- **Frontend**: Next.js 16.2.1 (Turbopack), TypeScript, React, Tailwind CSS (inferred from card/responsive changes)
- **CI/CD**: GitHub Actions with scheduled daily runs and manual dispatch with model selection
- **Local dev**: pnpm/turbo monorepo at `/home/kbkkbk/Develop/kubocchi/million-pocket/`, Node.js v22, mise for toolchain management

**Recurring Themes**:
- "Increase win probability": the dominant recurring ask across sessions; each session often ends with "もっともっと上げる方法ってありますか？？"
- CI pipeline failures: PostgREST 502s, path resolution errors (`relative_to(ROOT)` failures), missing model connections
- Mobile UI: repeated requests for responsive table → card layout, font improvements
- Budget plan feature: v14, v15, v16 iterations of a "buy recommendation" section based on predicted numbers
- Git hygiene: user stages, agent commits with Conventional Commits format in Japanese

**Note on local repo path**: Local clone is at `/home/kbkkbk/Develop/kubocchi/million-pocket/` (different from the GitHub repo name `million-pocket-orchestra`).
