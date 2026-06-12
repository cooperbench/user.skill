# PROJECTS

## blittle/pressy ★ dominant repo (100% of sessions)

A Vite-based static-site framework for self-publishing books as PWAs. Authors write content in MDX, and pressy generates a multi-page HTML app with chapter-by-chapter paginated reading, offline support, and optional paywalling.

### Architecture (inferred from prompts)

```
packages/
  pressy/                   — core CLI + Vite plugin + runtime
    src/vite/plugin.ts      — virtual modules, chapter map, dev server, build pipeline
    src/runtime/client.tsx  — hydrate(), renderBookPage(), ChapterReaderWithProgress
    src/runtime/offline.ts  — service worker signals, install prompt, offline download
    src/runtime/sw.ts       — service worker (Workbox)
    src/types.ts            — BookMetadata, ChapterMapData, PaywallMode, etc.
    src/cli/index.ts        — pressy build / pressy dev CLI

  @pressy/components/
    src/Reader.tsx           — PaginatedReader, ScrollReader, TOC drawer, settings panel
    src/BookProgress.tsx
    src/DownloadBook.tsx
    src/Paywall.tsx

  @pressy/typography/
    src/themes/              — light.css, dark.css, sepia.css
    src/fluid.css            — --font-size-base, responsive typography
    src/prose.css

  @pressy-pub/shopify/       — Shopify checkout provider
  @pressy/cloudflare/        — Cloudflare Pages Functions middleware (server-side paywall)

examples/
  flatland/                  — primary test book (Edwin Abbott's Flatland)
  moby-dick/                 — used for paywall and Stripe testing
```

### Recurring themes

- **Chapter navigation**: paginated reading with swipe/keyboard/tap gestures, cross-chapter transitions, `?page=last` routing, progress tracking in localStorage/IndexedDB
- **Progress restoration**: saving and restoring scroll/page position on reload — recurring source of bugs; blittle has debugged this repeatedly
- **PWA features**: offline caching (Workbox), `beforeinstallprompt`, fullscreen API, PWA manifest, icon generation
- **Paywall system**: client-side (PR #21, localStorage-based, bypassable) → server-side (Cloudflare Workers, Stripe webhooks, HttpOnly cookies, KV storage, magic link auth)
- **Deployment**: GitHub Actions → GitHub Pages (static examples at `blittle.github.io/pressy/`), PR preview deploys via `rossjrw/pr-preview-action`, Cloudflare Pages for Stripe/workers
- **Home page UX**: iterated heavily — hero layout, cover image, CTA button ("Start Reading"/"Continue Reading"), install button, stats, animations
- **Reader footer**: settings gear, book title, TOC drawer, offline indicator — moved marketing content off home page into reader

### Tech stack

- **Runtime**: Preact + @preact/signals, TypeScript
- **Build**: Vite 5, Rollup (code splitting), tsup, pnpm workspaces
- **Content**: MDX, YAML (`_book.yaml` for metadata)
- **Infra**: GitHub Pages, Cloudflare Pages Functions, Stripe, Workbox

### Known pain points (from sessions)

- `dvh` viewport height behaves differently on Android PWA vs Chrome devtools emulator
- GitHub Pages base path (`/pressy/`) breaks root-relative asset URLs — requires `base` config
- pnpm build order issues in monorepo (packages must build before examples)
- Service worker cache invalidation after purchase (paid chapters cached as unauthenticated)
- `totalPages` race condition in scroll-restore logic causes off-by-one page restoration
