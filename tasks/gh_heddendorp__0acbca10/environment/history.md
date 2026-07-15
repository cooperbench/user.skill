> SYSTEM

# AGENTS.md instructions for /Users/hedde/code/evorto <INSTRUCTIONS> # Repository Guidelines ## Context Discipline - Keep repository knowledge in small, relevant files. - Use this file as the map, not the full manual. - Read the nearest applicable guidance before editing: - root product/system context - module-level `AGENTS.md` - local README files - Update context files when reality changes, assumptions are invalidated, or new constraints are discovered. - Prefer small, accurate updates over large stale manuals. ## Root Context Files - `PRODUCT.md` - product goals, personas, core workflows, domain concepts, and product invariants. - `ARCHITECTURE.md` - high-level system shape, architectural boundaries, and where to look first for common changes. - `QUALITY.md` - behavior-focused verification guidance, Browser/Playwright expectations, and done criteria. Keep these files concise. Put implementation-specific guidance in the nearest module-level `AGENTS.md` or README. ## Project Structure - App code: `src/app/**` - Server runtime and APIs: `src/server/**` - Data layer: `src/db/**` - Shared contracts/types/utilities: `src/shared/**` and `src/types/**` - Unit tests: `*.spec.ts` in `src/**` - Playwright tests: `tests/**` - Legacy e2e reference: `e2e/**` - Assets/public: `public/` - Theming: `src/styles.scss` and `_theme-colors.scss` Start with the nearest applicable module guidance: - `src/app/AGENTS.md` - `src/server/AGENTS.md` - `src/db/AGENTS.md` - `tests/AGENTS.md` More specific guidance may exist deeper in […]

> DEVELOPER

Update our checkout to the latest from remote

> AGENT

I’ll first check the current branch and worktree state, then use the repo’s conservative update path so we don’t overwrite local work.

> AGENT

The checkout is on `main`, clean, and behind `origin/main` by one commit. The memory pointer mentions a sync skill, but that local skill path is not present in this checkout, so I’m falling back to direct Git verification and a fast-forward update.

> AGENT

The fetch succeeded and confirmed remote `main` is the target. I’m checking whether this can be fast-forwarded cleanly, then I’ll apply it.

> AGENT

`HEAD` is an ancestor of the fetched remote commit, so this is a clean fast-forward. I’m updating `main` now and then I’ll confirm the branch is current.

> AGENT

The fast-forward completed. I’m doing one final status check and recording the resulting commit so you have the exact state.

> AGENT

Updated `/Users/hedde/code/evorto` to the latest remote `main`. Current state: - Branch: `main` - Status: clean and aligned with `origin/main` - HEAD: `d1662b419c4 test: harden launch-critical Playwright coverage (#82)` No tests were run because this was a fast-forward-only checkout update with no local edits. <oai-mem-citation> <citation_entries> MEMORY.md:417-417|note=[checked repo sync guidance pointer] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>

> DEVELOPER

Are we using some image manipulation library in our application?

> AGENT

I’ll check the app and server dependencies plus code references for image processing terms, then distinguish between real manipulation libraries and browser/native image display utilities.

> AGENT

The dependency list does include image-adjacent packages: `pngjs`, `skia-canvas`, TipTap’s image extension, `qrcode`, and Cloudflare Images client usage. I’m reading the call sites now to separate “manipulates pixels” from “uploads/displays/generates image bytes.”

> AGENT

So far I’m not seeing Sharp/Jimp/ImageMagick-style processing. The only pixel-level code I found decodes PNGs to choose a Material color for icons; user uploads appear to be stored or sent through Cloudflare Images rather than transformed locally.

> AGENT

There’s no import use of `skia-canvas` in `src`, `tests`, or `helpers`, even though it is in `package.json`. I’m checking line numbers for the main evidence points so the answer can be precise.

> AGENT

Yes, but only narrowly. We are **not** using a typical image manipulation pipeline like `sharp`, `jimp`, ImageMagick, or canvas-based resizing/cropping in application code. What we do use: - `pngjs` in [src/server/utils/icon-color.ts](/Users/hedde/code/evorto/src/server/utils/icon-color.ts:6) to decode PNG bytes and inspect pixels for dominant/source color extraction. - `@material/material-color-utilities` in the same file to quantize/score those pixels. - `qrcode` in [src/server/http/qr-code.web-handler.ts](/Users/hedde/code/evorto/src/server/http/qr-code.web-handler.ts:160) to generate PNG QR code images. - TipTap’s image extension in [src/app/shared/components/controls/editor/editor.component.ts](/Users/hedde/code/evorto/src/app/shared/components/controls/editor/editor.component.ts:25) for editor image nodes and upload insertion. - Cloudflare Images direct uploads in [src/server/integrations/cloudflare-images.ts](/Users/hedde/code/evorto/src/server/integrations/cloudflare-images.ts:87), but our app initializes uploads/delivery URLs rather than transforming pixels locally. One oddity: `skia-canvas` is listed in [package.json](/Users/hedde/code/evorto/package.json:98), but I found no imports or usage of it under `src`, `tests`, or `helpers`.