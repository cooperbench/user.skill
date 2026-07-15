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