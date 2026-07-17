> SYSTEM

# AGENTS.md instructions for /home/<USER>/Projects/Active Projects/nucleus-desktop <INSTRUCTIONS> # Nucleus Desktop Open-source desktop coding ADE with Electron + React. ## First Design Principles - Design the application to be local-first wherever practical: data, permissions, project context, and core workflows should prefer running on the user's machine. - Limit reliance on third-party services and hosted infrastructure. Favor local capabilities or thin, optional integrations so the system stays understandable, portable, and easy for the person installing it to manage themselves. ## Product Direction Nucleus Desktop is intended to become an open-source coding ADE: a desktop environment for supervised, agentic software development. - The primary unit in the product is a project backed by a local folder. In product copy, navigation, and UX discussions, refer to these folder-backed units as projects rather than agents. - Local-first operation is a core product principle. When choosing architecture, dependencies, or UX flows, prefer approaches that keep the app self-managed on the user's machine and avoid unnecessary external services. - Chats, plans, tools, files, and approvals all live inside a project context. Switching the selected project should switch the active chat/thread context with it. - The target experience is outcome-oriented software development, not just turn-by-turn chat. - Users […]

> DEVELOPER

Here is the svg for openai/codex and claude code <svg xmlns="http://www.w3.org/2000/svg" width="256" height="260" preserveAspectRatio="xMidYMid" viewBox="0 0 256 260"><path d="M239.184 106.203a64.716 64.716 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.716 64.716 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.665 64.665 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.767 64.767 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483Zm-97.56 136.338a48.397 48.397 0 0 1-31.105-11.255l1.535-.87 51.67-29.825a8.595 8.595 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601Zm-104.466-44.61a48.345 48.345 0 0 1-5.781-32.589l1.534.921 51.722 29.826a8.339 8.339 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803ZM23.549 85.38a48.499 48.499 0 0 1 25.58-21.333v61.39a8.288 8.288 0 0 0 4.195 7.316l62.874 36.272-21.845 12.636a.819.819 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405v.256Zm179.466 41.695-63.08-36.63L161.73 77.86a.819.819 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.544 8.544 0 0 0-4.4-7.213Zm21.742-32.69-1.535-.922-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.716.716 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391v.205ZM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87-51.67 29.825a8.595 8.595 0 0 0-4.246 7.367l-.051 72.697Zm11.868-25.58 28.138-16.217 28.188 16.218v32.434l-28.086 16.218-28.188-16.218-.052-32.434Z"/></svg> <svg xmlns="http://www.w3.org/2000/svg" width="256" height="257" preserveAspectRatio="xMidYMid" viewBox="0 0 256 257"><path fill="#D97757" d="m50.228 170.321 50.357-28.257.843-2.463-.843-1.361h-2.462l-8.426-.518-28.775-.778-24.952-1.037-24.175-1.296-6.092-1.297L0 125.796l.583-3.759 5.12-3.434 7.324.648 16.202 1.101 24.304 1.685 17.629 1.037 26.118 2.722h4.148l.583-1.685-1.426-1.037-1.101-1.037-25.147-17.045-27.22-18.017-14.258-10.37-7.713-5.25-3.888-4.925-1.685-10.758 7-7.713 9.397.649 […]

> AGENT

I’m going to trace where the current provider/model icons are rendered, then I’ll swap in the provided SVGs and wire the OpenAI/Codex mark to follow light/dark theme anywhere that icon appears, including the model picker and chat tabs.

> AGENT

I’ve found the main seams: the app already centralizes provider marks in `ModelLogo.tsx`, and tab chrome appears to reuse that same logo path. I’m checking the exact call sites now so I can make one clean change instead of patching individual screens separately.

> AGENT

The shared logo component already exists, which is nice because it means we can fix the picker, sidebar, and tab icon usage centrally. I’m checking the actual brand asset files next so I can replace the right ones without breaking the existing theme switch behavior.

> AGENT

I’ve got the shape of the fix now: I’m going to make the OpenAI/Codex mark theme-aware in the shared `ModelLogo` component and swap the Claude asset to the SVG you pasted, so the picker and chat tabs update together from one place.

> AGENT

I’ve patched the shared logo path now. Next I’m verifying that the shared component compiles cleanly and that the Codex harness path is actually reusing the same theme-aware OpenAI mark instead of the old one-off asset.

> AGENT

The typecheck is clean, so this is a safe shared-ui change rather than something that just “looks right” in one file. I’m doing one last diff pass now and then I’ll summarize exactly what changed and where it takes effect.

> AGENT

I’m grabbing one exact memory citation before I close this out, just so the repo-context reference is precise. The code work is already done.

> AGENT

Updated the shared provider logo path so the new OpenAI/Codex and Claude SVGs now flow through the existing shared renderer in [ModelLogo.tsx](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/features/chat/components/ModelLogo.tsx:1). That means the model picker, chat tabs, and any other place using `ModelLogo` now pick up the new assets automatically. I treated Codex as sharing the same OpenAI/Codex mark you sent, and made both `openai` and `codex` use the same light/dark theme-aware logo path. I replaced the brand assets in [openai-symbol-light.svg](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/assets/brands/openai-symbol-light.svg:1), [openai-symbol-dark.svg](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/assets/brands/openai-symbol-dark.svg:1), and [claude-color.svg](/home/<USER>/Projects/Active%20Projects/nucleus-desktop/apps/desktop/src/assets/brands/claude-color.svg:1). `bun run typecheck` passes. I didn’t do a live visual app run in this turn. <oai-mem-citation> <citation_entries> MEMORY.md:1692-1693|note=[confirmed tab icons should keep using the shared icon slot] MEMORY.md:1796-1798|note=[reused repo context for harness and model UI surfaces] MEMORY.md:1612-1612|note=[captured related rollout id for the same nucleus-desktop UI area] </citation_entries> <rollout_ids> 019d67dd-2fcd-7f60-8928-7d5641b82393 </rollout_ids> </oai-mem-citation>