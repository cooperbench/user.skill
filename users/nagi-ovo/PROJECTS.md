---
name: nagi-ovo-projects
description: Repos, tech stack, and recurring themes
---

# Projects

## Nagi-ovo/gemini-voyager ★ dominant (100% of sessions)

**What it is**: A multi-platform browser extension (Chrome, Firefox, Safari) that enhances Gemini.google.com with features not in the native product: conversation timeline, sidebar folder management, prompt manager, fork/branch conversations, custom theming, snow/sakura effects, i18n support, Google Drive sync, starred messages, and more.

**Was formerly named**: "Gemini Voyager" — renamed to "Voyager" after a Google trademark complaint (March 2026). The Chrome Web Store listing was suspended during the rename review, requiring resubmission and loss of reviews/users.

**Tech stack**:
- TypeScript + React (TSX) — popup and content scripts
- Vite + Bun — build and package manager
- Tailwind CSS — popup UI styling
- VitePress — documentation site
- Chrome Extension Manifest V3 — primary target
- WebExtension APIs — Firefox/Safari cross-platform compat
- `chrome.storage.local` and `chrome.storage.sync` — state persistence
- Google Drive API + OAuth — cloud backup feature
- GitHub Actions — CI/CD; auto-publishes to Firefox Add-ons; Chrome/Edge manual or semi-automated
- commitlint + ESLint + TypeScript strict — code quality

**10 supported locales**: en, zh, zh_TW, ja, ko, ar, es, fr, pt, ru

**Recurring themes in sessions**:
- Bug fixes from GitHub issues/discussions (16.7% debug intent) — often opened by pasting the issue URL
- New features delegated via detailed implementation plans (14.7% create intent)
- Git housekeeping: bump version, write changelog, format, commit, push (19.3% git intent)
- Cross-browser regression checks — agent must verify Safari and Firefox are not broken by Chrome fixes
- i18n completeness — agent frequently misses one of the 10 locales
- Visual polish of popup and content UI — user has high aesthetic standards
- Timeline feature — conversation timeline is a core, frequently-modified component
- Folder/conversation management — another core feature with complex drag-and-drop UX
- Extension store management — Chrome Web Store, Edge Add-ons, Firefox Add-ons deployment
