# Projects — vfaraji89

## vfaraji89/tokalator ★ DOMINANT REPO (100% of sessions)

**What it is**: A context engineering toolkit for AI coding assistants — tracks token usage, manages open file tabs, and optimizes context window utilization. Distributed as:

1. **VS Code extension** (`tokalator-extension-vs/`) — TypeScript, published on VS Marketplace as `vfaraji89.tokalator`. At v3.1.3+ during sessions. 156 acquisitions in first 30 days.
2. **CLI / MCP server** (`tokalator-mcp/`) — developed mid-session as a parallel delivery channel
3. **Website** (`app/` Next.js) — deployed on Vercel, includes token calculator, cost economics, comparison tools, extension page, wiki of related papers
4. **Academic paper** (`paper/paper.txt` or `paper/tokalator-paper.tex`) — LaTeX, targeting JSS (Journal of Systems and Software, Q1). Co-authored with İlknur Köseoğlu Sarı and Engin Zeydan. Submitted to Overleaf, version-controlled via GitHub.

**Tech stack**:
- Extension: TypeScript, VS Code API, `vsce` packaging
- Web: Next.js, Recharts, Framer Motion (added mid-session), Tailwind
- Paper: LaTeX (`elsarticle` class, `natbib`, TikZ charts, BibTeX references)
- CI/CD: GitHub Actions (Node.js upgrade from 20→24 pending), Vercel

**Recurring themes in sessions**:
- Bug-fix cycles on the extension (context window setting ignored, webview memory leak, pin/unpin propagation)
- GitHub Actions CI failures (exit code 1, Node.js deprecation warnings)
- Website updates to stay in sync with each extension version bump
- LaTeX paper revision for Q1 standards: removing bold claims, adding citations, fixing TikZ charts, tracking commit statistics
- Version consistency across package.json, website JSON, CHANGELOG, and Marketplace listing
- Skills CLI integration (`npx skills add vfaraji89/tokalator`)
- Community event tracking (SaaS Bridge, TechCareer sessions, 170+ attendees)

**Mascot**: Red abacus (added to CLI and website per user direction: "add red abacus as moscot with this ui for cli and then add in website")
