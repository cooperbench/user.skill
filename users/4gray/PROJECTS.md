---
name: PROJECTS
---

# Projects: 4gray

## [DOMINANT] 4gray/iptvnator

An open-source Electron desktop application for watching IPTV streams. Supports M3U playlists (URL, file, text), Xtream Codes API portals, and Stalker Middleware portals. Has a companion website/blog at `https://4gray.github.io/iptvnator/`.

### Tech stack

- **Framework**: Angular (signals, computed, `@ngrx` store implied by store patterns)
- **UI library**: Angular Material (MDC-based components: mat-list-item, mat-dialog, mat-icon, mat-progress-bar, etc.)
- **Styling**: SCSS with CSS custom properties (`--app-*` token system, `--mat-sys-*` Material tokens)
- **Monorepo**: Nx workspace
- **Desktop runtime**: Electron with Chrome DevTools Protocol (CDP) for automation
- **Website**: Astro (blog + landing page, deployed to GitHub Pages)
- **Testing**: Playwright e2e
- **Build/serve**: `nx serve`, `nx run`

### Workspace structure (inferred from `@` references)

```
apps/
  web/                          Angular renderer app
    src/app/
      home/                     Home screen, video player, Xtream import
      stalker/                  Stalker portal views
      xtream-tauri/             Xtream portal views (Tauri-era naming)
  electron-backend/             Electron main process
    src/app/events/             IPC event handlers (stalker.events.ts, etc.)
  website/                      Astro landing page + blog
  stalker-mock-server/          Express mock server for Stalker portal e2e
  xtream-mock-server/           Express mock server for Xtream Codes e2e
libs/
  playlist/shared/ui/           Playlist UI components (recent-playlists, playlist-switcher)
  portal/xtream/                Xtream portal feature + data-access
  portal/shared/ui/             Shared portal UI (grid-list, content-hero)
  portal/downloads/             Downloads feature
  workspace/shell/feature/      App shell: header, rail, context panel, command palette
  ui/epg/                       EPG progress panel
  ui/components/                Shared: channel-list-container, video-player, art-player
  services/                     Portal status service
```

### Recurring themes in sessions

- **UI consistency sweeps**: Checking that colors, typography, padding, hover states, and border-radius are consistent across M3U, Xtream, and Stalker views.
- **Angular Material density reduction**: The default Material components are too large; 4gray frequently asks to reduce padding/density and align with the app's compact style.
- **CSS token correctness**: Moving from hardcoded RGBA values to `--app-*` / `--mat-sys-*` custom properties so dark/light themes both work.
- **Feature additions from user feedback**: User issue reports (GitHub) trigger new features (audio track switching, EPG throttling).
- **Mock server infrastructure**: Building Stalker and Xtream mock servers for local development and Playwright e2e testing.
- **Website redesign**: Improving the Astro landing page to match the quality of design references like Gitbutler.
- **Favorites / recently-viewed refactor**: Ongoing multi-session effort to consolidate global and local playlist favorites.
- **Navigation architecture**: Rail sidebar vs. header global actions — repeatedly re-examining what belongs where.
