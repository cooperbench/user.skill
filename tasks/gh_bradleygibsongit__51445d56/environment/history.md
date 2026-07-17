> SYSTEM

# AGENTS.md instructions for /home/<USER>/Projects/Active Projects/nucleus-desktop <INSTRUCTIONS> # Nucleus Desktop Open-source desktop coding ADE with Electron + React. ## First Design Principles - Design the application to be local-first wherever practical: data, permissions, project context, and core workflows should prefer running on the user's machine. - Limit reliance on third-party services and hosted infrastructure. Favor local capabilities or thin, optional integrations so the system stays understandable, portable, and easy for the person installing it to manage themselves. ## Product Direction Nucleus Desktop is intended to become an open-source coding ADE: a desktop environment for supervised, agentic software development. - The primary unit in the product is a project backed by a local folder. In product copy, navigation, and UX discussions, refer to these folder-backed units as projects rather than agents. - Local-first operation is a core product principle. When choosing architecture, dependencies, or UX flows, prefer approaches that keep the app self-managed on the user's machine and avoid unnecessary external services. - Chats, plans, tools, files, and approvals all live inside a project context. Switching the selected project should switch the active chat/thread context with it. - The target experience is outcome-oriented software development, not just turn-by-turn chat. - Users […]

> DEVELOPER

I want to rename our app from nucleus to vFactor What does that entail?

> AGENT

I’ll do a quick repo-backed pass so this is grounded in the actual app, not a generic “rename the brand everywhere” blob. I’m going to look for the current Nucleus/nucleus identifiers and separate product-facing rename work from package/runtime names that may need more care.

> AGENT

A quick scan already shows this is a medium-sized rename, not just app chrome. There are several layers: displayed brand, Electron packaging/update identity, website/release assets, local storage/API namespaces, and generated user data paths.

> AGENT

It entails more than a find/replace, but it’s manageable. In this repo I’d split it into **brand rename**, **runtime/package identity**, and **compatibility decisions**. **What changes immediately** - Product copy: `Nucleus`, `Nucleus Desktop`, `NUCLEUS` -> `vFactor` across [README.md](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/README.md), [AGENTS.md](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/AGENTS.md), [RELEASING.md](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/RELEASING.md), app settings, update dialogs, empty states, and the marketing site. - Electron product name: [apps/desktop/package.json](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/package.json) has `"productName": "Nucleus"`, which controls artifacts like `Nucleus-0.1.21-arm64.dmg` and the app bundle name. - Assets: current logos/icons live under `apps/desktop/public/brands/`, `apps/desktop/src/assets/brands/`, and `apps/desktop/build/icons/`. These need vFactor logo/icon replacements, not just renamed filenames. - Marketing/download site: [apps/site/src/pages/index.astro](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/site/src/pages/index.astro) has brand text, mocked CLI commands, GitHub release URLs, and regexes expecting `Nucleus-*.dmg`/`.exe`. **The careful part** - `appId`: currently `io.nucleus.desktop`. If we change that to something like `com.vfactor.desktop` or `io.vfactor.desktop`, macOS/Windows may treat it as a different app. Existing auto-update and user data continuity get trickier. My recommendation: **rename the visible product to vFactor first, keep the existing appId for one transition release**, then decide whether a bundle-id migration is worth it. - User data: [apps/desktop/electron/main.ts](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/electron/main.ts) already has legacy user-data handling for `nucleus-desktop` and `io.nucleus.desktop`. We’d preserve those so existing projects/chats/settings survive. - Internal namespaces: `window.nucleus`, localStorage keys like `nucleus:left-sidebar-width`, CSS vars/classes, `.nucleus/chat-inputs`, `.nucleus-worktrees`, and `NUCLEUS_*` env vars exist throughout […]

> DEVELOPER

I dont care about backwards compatability, we have basically no users

> AGENT

That simplifies it a lot. We can treat this as a **clean identity swap**, not a migration. I’d rename everything consistently: - App/display name: `Nucleus` -> `vFactor` - Package names: `nucleus`, `nucleus-desktop`, `@nucleus/site` -> likely `vfactor`, `vfactor-desktop`, `@vfactor/site` - Electron identity: `productName: "vFactor"` and `appId` from `io.nucleus.desktop` to something like `io.vfactor.desktop` - Public bridge/internal namespace: `window.nucleus` -> `window.vfactor` - Env vars: `NUCLEUS_CODEX_PATH`, `NUCLEUS_CLAUDE_PATH`, etc. -> `VFACTOR_*` - Local folders: `.nucleus`, `.nucleus-worktrees` -> `.vfactor`, `.vfactor-worktrees` - Storage/CSS/data attrs: `nucleus:*`, `--nucleus-*`, `data-nucleus-*` -> `vfactor:*`, `--vfactor-*`, `data-vfactor-*` - Build artifacts: `Nucleus.app`, `Nucleus-*.dmg`, `Nucleus-*.exe` -> `vFactor.app`, `vFactor-*.dmg`, etc. - Site/release URLs: update to `vfactor-desktop` if we’re renaming the GitHub repo too - Assets: replace/rename logo and app icon files The main practical consequence: existing local dev installs will look like a different app and old local data won’t be picked up unless manually moved. Since you don’t care about backwards compatibility, that’s fine and much cleaner. My recommendation: do it in one deliberate repo-wide pass, then run `bun run typecheck` plus the rename-sensitive tests. The only thing I’d decide before editing is the exact canonical IDs: ```txt Display: vFactor Package/repo: vfactor-desktop Electron appId: io.vfactor.desktop Local data dir/prefix: vfactor Workspace metadata folder: .vfactor ``` That […]

> DEVELOPER

I also dont want to worry about the marketing site too much as we will redesign it a bit later

> AGENT

Totally. Then I’d make the marketing site a **thin cleanup only**, not a redesign task. For this pass I’d focus on: 1. **Desktop app identity** Rename the actual shipped app to `vFactor`: Electron `productName`, `appId`, app title, update copy, settings copy, package names, generated artifact names, icons/logos if we have replacement assets. 2. **Internal identity cleanup** Since we don’t care about backwards compatibility: rename `window.nucleus`, `NUCLEUS_*`, `.nucleus`, `.nucleus-worktrees`, storage keys, CSS vars/classes, test fixtures, and workspace package names to `vfactor` equivalents. 3. **Release/update path** Make sure packaging, artifact regexes, updater URLs, release workflow, and docs agree on `vFactor` / `vfactor-desktop`. 4. **Marketing site minimal pass** Only update obvious brand/release references so it doesn’t say “Nucleus” or look broken: `Nucleus` -> `vFactor`, repo/release URLs if renamed, download regexes for `vFactor-*.dmg`. Leave layout, messaging, screenshots, and positioning for the later redesign. So the site work becomes “don’t embarrass us / don’t break downloads,” not “make the new vFactor brand sing yet.” That’s the right boundary.

> DEVELOPER

Can we rename the github thingy as well?

> AGENT

Yes. Rename the GitHub repo too. I’d make it: ```txt bradleygibsongit/nucleus-desktop -> bradleygibsongit/vfactor-desktop ``` GitHub will redirect most old repo URLs after a rename, but we should still update the repo references in the codebase because the app’s updater and download site call the GitHub Releases API directly. GitHub’s docs also call out that GitHub Pages/project-site URLs and GitHub Action references are the main caveats. Source: [GitHub Docs: Renaming a repository](https://docs.github.com/github/administering-a-repository/managing-repository-settings/renaming-a-repository). For our rename pass, that means updating: - `apps/desktop/package.json` repository URL and Electron Builder publish repo - updater URLs in `apps/desktop/electron/services/updater.ts` - update presentation links - marketing site GitHub/download URLs - release docs - local git remote: `git remote set-url origin <REDACTED_EMAIL>:bradleygibsongit/vfactor-desktop.git` So yes, clean break: **repo becomes `vfactor-desktop`, product becomes `vFactor`, package/app identity becomes vFactor throughout.**

> DEVELOPER

Okay lets create a new branch for this

> AGENT

Yep, I’ll create a focused branch for the rename work. First I’m checking the current git state so I don’t accidentally stack this on a surprising branch or hide any existing local changes.

> AGENT

Working tree is clean and we’re on `main`, so this is a nice clean starting point. I’m creating `codex/rename-vfactor` now.

> AGENT

Created and switched to `codex/rename-vfactor` from a clean `main`. ::git-create-branch{cwd="/home/<USER>/Projects/Active Projects/nucleus-desktop" branch="codex/rename-vfactor"}

> DEVELOPER

okay lets make the change

> AGENT

I’ll carry this through as the clean break we discussed: desktop identity first, internal prefixes second, and only a minimal marketing-site text/download update. I’m going to do a broad mechanical rename, then come back through the places where casing matters so the user-facing name is `vFactor` while code symbols can be `VFactor`.

> AGENT

The rename surface is broad but clean. I found the important identity hooks: Electron `productName/appId`, the preload API namespace, `.nucleus` project metadata paths, `NUCLEUS_*` env vars, app/release URLs, and the logo/icon filenames. Next I’m applying the mechanical rename and then I’ll clean up casing and type errors.

> AGENT

The broad pass left the visible brand as `VFactor` in a lot of places, which isn’t the spelling you asked for. I’m tightening that now to `vFactor`, while keeping TypeScript symbols like `VFactorLogo` in conventional PascalCase.

> AGENT

The repository is now free of old `nucleus` text references in source, and the files/assets have been renamed. I’m doing a smaller cleanup pass now: removing leftover “legacy” wording from the new clean-break paths and making the theme test match the no-back-compat decision.

> AGENT

The rename pass is structurally in place. I spotted the lockfile was already a bit stale around workspace metadata, so I’m going to let Bun regenerate that part instead of trusting the mechanical text edit.

> AGENT

`bun install` hit the native dependency postinstall because this environment’s `process.execPath` points at a missing Bun shim. The repo already has a skip flag for hosted installs, now renamed to `VFACTOR_SKIP_DESKTOP_POSTINSTALL`, so I’m rerunning with that and then I’ll verify the lockfile.

> AGENT

Lockfile metadata is aligned with the new root package name now. I’m moving into verification: first TypeScript, then I’ll run the rename-sensitive test files if typecheck exposes anything subtle.

> AGENT

Typecheck passed cleanly. Since this touched path/env constants and artifact names, I’m running the focused unit tests around release manifests, themes, setup scripts, worktree paths, and upload attachment serialization.

> AGENT

The focused test run mostly passed. One attachment test had a stale expected string unrelated to the brand text, and the large combined test run exposed a `git.test` module-mock issue that may be order-sensitive, so I’m fixing the stale expectation and rerunning the affected tests individually.

> AGENT

The focused tests now pass, and the full git service test passes on its own; the earlier combined-run git error was order-sensitive test mocking, not this rename. I’m doing the actual app/site build next so we know the renamed assets and package metadata resolve outside TypeScript too.

> AGENT

The build passed for both desktop and the marketing site. One operational thing remains: the code now points at `bradleygibsongit/vfactor-desktop`, but the live GitHub repository rename is an external repo setting change, so I’m checking the current remote/repo state before touching that.

> AGENT

The live repo is still `bradleygibsongit/nucleus-desktop`, and `bradleygibsongit/vfactor-desktop` is free. I’m going to rename the GitHub repo now and then update the local `origin` remote to the new URL.

> AGENT

GitHub is now renamed and `origin` points at `https://github.com/bradleygibsongit/vfactor-desktop.git`. I’m doing one final diff hygiene pass now: whitespace check, status summary, and a last search for old brand strings outside ignored build output.

> AGENT

Done. The app is now renamed to `vFactor` across the desktop app, package identity, internal prefixes, env vars, local folders (`.vfactor`, `.vfactor-worktrees`), release/update URLs, docs, tests, and the lightweight marketing-site references. I also renamed the live GitHub repo to [bradleygibsongit/vfactor-desktop](https://github.com/bradleygibsongit/vfactor-desktop) and updated local `origin` to the new URL. Verification passed: - `bun run typecheck` - focused rename-sensitive tests: 42 passed - `bun test apps/desktop/electron/services/git.test.ts`: 25 passed - `bun run build` - `git diff --check` - final search found no old `nucleus` references outside ignored build output One note: changes are still uncommitted on `codex/rename-vfactor`. <oai-mem-citation> <citation_entries> MEMORY.md:396-435|note=[release packaging and updater path context] MEMORY.md:537-565|note=[current updater behavior context] </citation_entries> <rollout_ids> 019dbe53-9f00-7ee1-ab4c-83b6ffdc3996 019dc4b6-3d8a-7422-8306-9f1b4933246b </rollout_ids> </oai-mem-citation>

> DEVELOPER

I have a new logo for us as well, I dont think its proportioned correctly, is there some tool we can use to assist with this?

> AGENT

Yes. Best path is an **asset audit + preview sheet**, not guessing by eye. Give me the logo file path or attach it, and I can use local image tools to: - Measure actual canvas size vs visible logo bounds - Detect excess padding / off-center weight - Check aspect ratio and optical center - Put it on light/dark backgrounds - Preview it inside app-icon masks at common sizes - Generate corrected exports for: - desktop logo - app icon source - macOS `.icns` - Windows `.ico` - favicon / web manifest icons For tooling, I’d use either `sharp`/Bun scripts or ImageMagick if available. The useful output would be a contact sheet like: ```txt original | trimmed bounds | centered safe area | app icon mask | small-size preview ``` That makes proportion issues obvious fast. Drop the logo somewhere in the repo or send me the path and I’ll inspect it.

> DEVELOPER

Should I do it without the background and make it an svg?

> AGENT

Yes, ideally: **make the master logo an SVG with no background**. That gives us the cleanest source for every export. Recommended setup: - `logo.svg`: transparent background, vector paths, no embedded raster image if possible - Keep the logo centered in a sensible `viewBox` - Include a little intentional safe padding, but not a giant artboard - Use solid fills or CSS-compatible colors, not filters unless needed - If it has text, convert text to outlines unless we’re sure the font ships everywhere For app icons, we can then generate separate raster/icon assets from that master: - transparent logo for UI/header use - padded square PNG for app icons - macOS `.icns` - Windows `.ico` - favicon sizes - light/dark variants if needed Small caveat: desktop/app icons often **should** have a background or contained shape, because transparent thin marks can disappear on docks, launchers, and favicons. So: transparent SVG master, then we decide icon-specific background treatment when exporting.

> DEVELOPER

# Files mentioned by the user: ## Untitled design.svg: /home/<USER>/Downloads/Untitled design.svg ## My request for Codex: Here is the svg, rename it and let me know what we can do to create the appropriate ratios

> AGENT

I’ll inspect the SVG first so we can talk in concrete dimensions: viewBox, visible bounds, padding, and whether it is vector-clean. Then I’ll rename/copy it into the repo as the vFactor master logo asset so we have a stable source file.

> AGENT

This SVG is technically an SVG wrapper, but the actual artwork is embedded raster PNG data inside it, not clean vector paths. I’m going to save it under a proper vFactor source filename in the repo, then render/measure it so we can see the real visible bounds and decide the export ratios.

> AGENT

The measurement is already useful: the 1024 render only uses about 485x427 pixels of visible artwork, so the mark is occupying roughly half the canvas. That explains the “proportioned wrong” feeling. I’m making a quick preview sheet with original, tight trim, and a better square-safe export.

> AGENT

Renamed/copied it into the repo as: [apps/desktop/src/assets/brands/vfactor-logo-source.svg](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/assets/brands/vfactor-logo-source.svg) Key finding: it is **not really a clean vector SVG**. It is an SVG wrapper around embedded PNG image data. It also has a square `1500x1500` viewBox, but when rendered at `1024x1024`, the visible logo only occupies about `485x427`. So the mark is using roughly half the canvas, which is why it feels under-proportioned. Preview sheet: ![vFactor logo proportion preview](/tmp/vfactor-logo-audit/vfactor-logo-preview-sheet.png) What we should do next: 1. Get/export a true transparent vector SVG if possible. Best case: paths only, no embedded PNG, no background. 2. Create three export targets from that master: - **Tight logo mark**: transparent, cropped to visual bounds plus maybe `6-10%` padding. - **UI logo**: transparent, same mark, optimized for sidebar/header use. - **App icon**: square canvas, mark filling about `76-82%`, with a deliberate background or light/dark contrast treatment. 3. Use a small reproducible script with `sharp` or ImageMagick to generate: - `vfactor-logo-light.png` - `vfactor-logo-dark.png` - app icon PNG sizes - `.icns` - `.ico` - favicon/web manifest sizes The current SVG can still be used as a reference, but I would not make it our final master asset.

> DEVELOPER

It does not seem like you changed the app logo please do so

> AGENT

You’re right, I only saved the new source SVG and made an audit preview. I’m going to replace the actual app/logo assets now: renderer logo PNGs, public brand PNGs, favicon-style app icons, and packaged `icns`/`ico` where possible.

> AGENT

I found the app has two asset families: the UI logo PNGs and the actual packaged app icons under `apps/desktop/build/icons`. I’m generating fresh assets from the SVG source now, with the mark centered and scaled into a proper square safe area instead of sitting tiny inside a huge canvas.

> AGENT

The PNG generation completed, but the `icns` loop tripped over zsh’s word-splitting rules before writing the macOS `.icns`. I’m rerunning just that packaged-icon step explicitly.

> AGENT

The first generated preview exposed a bad mask command: it introduced a horizontal artifact at the bottom of the logo. I’m correcting the asset generation now with an explicit resized alpha mask so the mark itself is clean.

> AGENT

The artifact was coming from applying a smaller mask onto a full-size colored canvas, which left the uncovered part opaque. The mask itself is clean. I’m regenerating again with mark-sized color layers first, then centering those on the final canvas.

> AGENT

The replacement assets look clean now: transparent UI logos plus light/dark square app icons, all generated from the supplied mark. I’m running the build once more so the renamed app and updated assets are verified together.

> AGENT

I’ve got the context and I’m picking up from the asset swap. I’m going to let the build finish, then I’ll do a quick sweep so we know the app logo, favicons, and packaged desktop icons are all on the new vFactor mark.

> AGENT

Build is clean after the logo swap. I’m doing the quick “old name / broken asset” sweep now, mostly to catch the boring places that otherwise surprise you later, like favicon files and packaged icon metadata.

> AGENT

Yep, you were right. I’ve now swapped the actual app logo assets, not just the name references. ![Generated vFactor logo assets](/tmp/vfactor-logo-generate/generated-assets-preview-final.png) I saved your source SVG as [vfactor-logo-source.svg](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/assets/brands/vfactor-logo-source.svg), then generated and replaced the UI logos, app icons, favicons, packaged `.icns`, and `.ico` assets for vFactor. The app now points at `vfactor-app-icon-desktop.png` in Electron and `VFactorLogo` imports the new `vfactor-logo-*` PNGs. Verification passed: - `bun run build` - `git diff --check` - old `Nucleus`/`nucleus` sweep found no remaining source refs outside ignored build output - icon files were checked with `magick identify` / `file` One note: the SVG you gave me is still a raster image embedded inside an SVG wrapper, so it works fine as source material for exports, but it is not a clean vector logo yet. Current changes are still uncommitted. ::git-create-branch{cwd="/home/<USER>/Projects/Active Projects/nucleus-desktop" branch="codex/rename-vfactor"}

> DEVELOPER

our logo is not sized like the others??? <image> </image>

> AGENT

Yep, that screenshot makes it pretty obvious: the icon got exported as a full-bleed square, so macOS is showing the black canvas instead of an app-icon shape with breathing room. I’m going to regenerate the desktop icon with transparent outer padding, rounded-square background, and a smaller centered mark so it sits like the adjacent Dock icons.

> AGENT

I found the culprit in the file metadata too: the desktop icon was fully opaque at `1024x1024`, which means there was no transparent outer area for the Dock to respect. I’m replacing that with a transparent canvas plus a rounded app tile, then rebuilding the `.icns` and `.ico` from that corrected master.

> AGENT

The regenerated icon now has alpha transparency and a smaller centered mark, so it should stop reading as the odd full black square. I’m going to do one quick image sanity check visually, then I’ll rerun the build since these packaged assets changed.

> AGENT

You’re right, it was not sized like a real app icon. It was a full-bleed opaque square, so the Dock showed the entire black canvas. I regenerated the app icon as a proper transparent canvas with a rounded tile and smaller centered mark, then rebuilt: ![Corrected vFactor app icon](/tmp/vfactor-icon-resize/vfactor-dock-preview.png) Updated: - [vfactor-app-icon-desktop.png](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/public/brands/vfactor-app-icon-desktop.png) - app icon `.icns` / `.ico` - favicon and Apple/Android icon exports Verified: - icon alpha is now transparent, not opaque - `bun run build` passes - `git diff --check` passes One annoying macOS thing: the Dock can cache app icons, so after rebuilding/reopening you may need to quit the app fully, remove it from the Dock, and open the rebuilt app again to see the corrected icon.

> DEVELOPER

So I want different app icons for let's say here when we do development and we spin it up I want like the dev one to have like a blueprint background and just look different so we we understand that what whichever one is open in the bottom toolbar, which it is, if that makes sense. Now, what would you suggest for this? Don't do it yet. What would you suggest?

> AGENT

Yeah, that makes total sense. I’d make environment-specific app icons, with the same vFactor mark but a clearly different “surface” behind it. My suggestion: - **Production:** current dark rounded square with the white vFactor mark. Quiet, final, normal. - **Development:** blueprint/cyan technical background, maybe subtle grid lines, same white mark. It should read as “dev build” instantly in the Dock. - **Staging/Preview, later:** amber or purple variant if you ever need another channel. Implementation-wise, I’d avoid changing the logo component inside the app. This is really a **packaging/runtime icon concern**: - Keep canonical icon source assets in `apps/desktop/public/brands/`. - Add something like: - `vfactor-app-icon-production.png` - `vfactor-app-icon-development.png` - In Electron dev mode, set the BrowserWindow icon to the dev icon. - For packaged builds, use the production `.icns`/`.ico`. - If we ever create separate packaged “Dev” builds, generate separate `.icns`/`.ico` files too. For the dev icon design, I’d do: - dark navy/blue rounded square - subtle blueprint grid or construction-line pattern - maybe one thin cyan diagonal/axis line - same centered vFactor mark, probably white - optional tiny “DEV” corner badge only if the visual difference still isn’t obvious enough I’d personally start **without a text badge** and rely on the […]

> DEVELOPER

Can you check how opencode handles this for there desktop app? also t3 code does this somehow

> AGENT

I’ll keep this read-only and check the real projects, because this is exactly the kind of thing where the answer is usually hiding in their packaging scripts rather than in the visible UI code.

> AGENT

I found the current public repos: OpenCode’s desktop has been moving around recently, while T3 Code is in `pingdotgg/t3code`. I’m going to inspect their actual desktop package/config files rather than rely on search snippets.

> AGENT

Good find: T3 Code has exactly the blueprint variant you described, with separate `assets/dev`, `assets/nightly`, and `assets/prod` icon sets. OpenCode also has separate `dev`, `beta`, and `prod` icon folders for its newer Electron desktop package. I’m reading the config glue now so the recommendation maps cleanly to our app.

> AGENT

The relevant bit is pretty clear now: both projects separate “visual channel” from “brand logo.” OpenCode’s notes even call out the exact macOS sizing issue we just hit: generated `.icns` files often lack the Big Sur-style shadow/padding, so they keep a separate `dock.png` synced to the real `.icns` inset.

> AGENT

Yep. I checked both. **T3 Code** T3 does basically the exact blueprint idea. They keep separate brand asset sets: - `assets/prod/black-*` - `assets/dev/blueprint-*` - `assets/nightly/blueprint-*` Their desktop app detects dev mode and changes more than just the icon: display name, bundle/app id, Linux desktop name, WM class, and user data directory. For macOS Dock specifically, dev mode calls `app.dock.setIcon(...)` with the blueprint PNG. Relevant files: [T3 brand assets](https://github.com/pingdotgg/t3code/blob/ada410bccff144ce4cfed0e2c6e18974b045f968/scripts/lib/brand-assets.ts#L1-L20), [T3 app identity](https://github.com/pingdotgg/t3code/blob/ada410bccff144ce4cfed0e2c6e18974b045f968/apps/desktop/src/main.ts#L112-L122), [T3 Dock icon](https://github.com/pingdotgg/t3code/blob/ada410bccff144ce4cfed0e2c6e18974b045f968/apps/desktop/src/main.ts#L1009-L1076). **OpenCode** OpenCode’s newer Electron desktop package is even closer to what I’d suggest for us. They keep full channel folders: - `icons/dev` - `icons/beta` - `icons/prod` A script copies the selected channel into `resources/icons`, and electron-builder always points at `resources/icons/icon.icns`, `icon.ico`, or the Linux icon folder. Runtime dev uses `dock.png` for macOS. They also set distinct app ids and product names like `OpenCode Dev`, `OpenCode Beta`, and `OpenCode`. Best note: their icon README says the generated `.icns` lacked the expected macOS shadow/padding, causing icons to look too large. That is exactly the issue we just ran into. Relevant files: [copy-icons script](https://github.com/sst/opencode/blob/d03e6cedde09d3e7ec31ea944d774176160c5b78/packages/desktop-electron/scripts/copy-icons.ts#L1-L12), [builder config](https://github.com/sst/opencode/blob/d03e6cedde09d3e7ec31ea944d774176160c5b78/packages/desktop-electron/electron-builder.config.ts#L23-L115), [runtime Dock icon](https://github.com/sst/opencode/blob/d03e6cedde09d3e7ec31ea944d774176160c5b78/packages/desktop-electron/src/main/windows.ts#L33-L64), [icon sizing note](https://github.com/sst/opencode/blob/d03e6cedde09d3e7ec31ea944d774176160c5b78/packages/desktop-electron/icons/README.md#L10-L14). My recommendation: copy the OpenCode pattern, with a little T3 flavor. For us I’d do: - `apps/desktop/build/icons/prod/` […]