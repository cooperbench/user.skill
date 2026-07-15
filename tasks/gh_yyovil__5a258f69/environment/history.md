> SYSTEM

# AGENTS.md instructions for /Users/tanishqpalandurkar/Projects/yyork <INSTRUCTIONS> General instructions: follow these all the time. - whenever you are unaware of what a particular cli option does, refer to the man page or use the --help option to learn its behaviour but never assume based on typical examples of its use. --- project-doc --- # Agent workflow - User will assign one PRD at a time to an agent to implement. All the PRDs are available in the `./prds` dir. - At any time if you think you could do a better job if a CLI tool was available to you and it would take you lesser tokens to do the task in presence of that tool, explicitly ask user to install it. Do not install it directly on your own as there are security related issues regarding this way of installation. </INSTRUCTIONS> <environment_context> <cwd>/Users/tanishqpalandurkar/Projects/yyork</cwd> <shell>zsh</shell> <current_date>2026-06-09</current_date> <timezone>Asia/Kolkata</timezone> <filesystem><workspace_roots><root>/Users/tanishqpalandurkar/Projects/yyork</root></workspace_roots><permission_profile type="disabled"><file_system type="unrestricted" /></permission_profile></filesystem> </environment_context>

> DEVELOPER

I want to improve the project's branding. There's no fucking image in the project's README.md. We got to put an image right there. What you say?

> AGENT

I’ll treat this as a README/docs polish pass and first check what the project already has for visual assets and how the app presents itself, so the image we add matches the product instead of feeling bolted on.

> AGENT

I’m using the documentation-writing guidance for the README part, but this is a small branding fix rather than a full rewrite. The main decision is whether the image should be a real product screenshot or a generated brand banner; I’m leaning screenshot because it proves what yyork is.

> AGENT

The README already has a tiny favicon at the top, but I agree with your point: that does not read as a project image. I’m checking the existing diff and screenshot artifacts before choosing where to add a real visual.

> AGENT

There is already unrelated README work in this checkout around install instructions, so I’ll only make a narrow addition near the top and avoid touching that content. I also found `.github/assets/thumbnail.png`, which might already be the right branding asset if it is product-facing.

> AGENT

One important catch: the tracked brand logo component still says `Agent Orchestrator` internally, while the README is `yyork`. For this pass I’ll avoid broad brand refactors and just add a README image asset/reference.

> AGENT

The `.github/assets/thumbnail.png` is from the old Start UI starter, so it would make the branding worse. I’m going to build or capture a yyork-specific hero image instead of reusing that.

> AGENT

For the README itself, I’d put a wide hero image directly under the tagline and above the first divider. That gives the repo a first-screen visual without breaking the current install/quick-start flow.

> AGENT

I’m going to add a new tracked hero asset at `.github/assets/yyork-readme-hero.svg` and reference it from the README under the tagline. The SVG will be a product-style dashboard mockup, not the stale Start UI image.

> DEVELOPER

hold on that ain't gonna work. I want to put yyork's screenshot but I want to tk the screenshot using an app and mk the screenshot look very polished and aesthetically pleasing

> AGENT

Got it. I’ll stop the synthetic SVG route and remove the file I just added. The better approach is: run yyork or its UI with controlled demo data, capture a real product screenshot, then wrap/post-process it into a polished README hero.

> AGENT

I’m going to avoid local private data in the screenshot. I’ll look for the cleanest controlled path: either a seeded yyork server under a temp HOME, or a Storybook/demo route that renders the real UI components with fixture data.

> AGENT

The Browser tool is not exposed in this turn, so I’ll use repo-local Playwright from the terminal for the capture. That still gives us a real Chromium screenshot and lets us post-process it deterministically.

> AGENT

The app can render from `/api/sessions`, so the clean capture path is viable: create a temp yyork home, seed only fake session rows, run the dashboard against that, and screenshot the real UI. Then I can crop/frame it into a README image.

> AGENT

I found a straightforward seed point: yyork’s dashboard reads SQLite-backed `/api/sessions`. I can run the app with `HOME` pointing at a temp directory, insert polished fake sessions into that temp database, and capture the dashboard without touching your real `~/.yyork/state.db`.

> AGENT

Because yyork reconciles SQLite rows against real Zellij sessions on startup, seeded database rows would get swept. I’m switching to a safer screenshot setup: real yyork frontend, controlled fake `/api/sessions`, and no private local state.

> DEVELOPER

hold on. I'll tk the screenshot as I don't trust AI doing this for me

> AGENT

Fair. I removed the synthetic SVG I had started and did not add a README reference. When you have the screenshot, the clean path is to place it at `.github/assets/yyork-readme-hero.png` and put it directly under the README tagline, above the first divider: ```md <p align="center"> <img src=".github/assets/yyork-readme-hero.png" alt="yyork dashboard showing parallel AI coding agents in isolated workspaces" width="100%" /> </p> ``` That keeps the README first screen branded without disturbing the install docs. <oai-mem-citation> <citation_entries> MEMORY.md:188-190|note=[used yyork UI and dirty-checkout context] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>