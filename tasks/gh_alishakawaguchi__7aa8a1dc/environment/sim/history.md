[DEVELOPER]: some of the agent installs aren't working like cursor. can we update the repo to follow the smae skills install as this one /Users/alisha/Projects/cc-skills-golang

[AGENT]: I'll explore both repos to understand the install patterns.

[AGENT]: Now I understand the difference. `cc-skills-golang` uses a flat layout: skills live at `/skills/` at the repo root with `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, etc. at root. This repo nests everything under `plugins/entire/skills/`, which is why Cursor (and similar flat-discovery installs) break. Let me plan and execute the refactor.

[AGENT]: Now move the codex plugin manifest to the root, replace the claude marketplace with a plugin manifest, and delete the now-empty nested plugin dir.

[AGENT]: Now remove empty nested dirs.

[AGENT]: Now update all skill path references. Start with the cursor manifest, marketplace, opencode plugin, agents marketplace, and package.json.

[AGENT]: Actually the codex manifest already says `"skills": "./skills/"` which is correct since it's now at root. No change needed.

[AGENT]: Good — codex manifest is correct. Now update the marketplace.json to treat the root as the plugin source.

[AGENT]: Now let me check if there are any other references to the old `plugins/entire/skills` path.

[AGENT]: package.json main is fine (that's `.opencode/plugins/entire.js`, a real file path). Fix INSTALL.md.

[AGENT]: Now rewrite the README install section. I'll keep the existing skill descriptions but replace the install section to mirror cc-skills-golang's per-agent collapsibles.

[AGENT]: Let me verify the final state.

[AGENT]: All three are valid references to the real file `.opencode/plugins/entire.js` — those stay. Final check of git state:

[AGENT]: Layout now matches `cc-skills-golang`: - `skills/{explain,search,session-handoff}/SKILL.md` at repo root (git-tracked rename, history preserved) - `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (source now `./`) - `.cursor-plugin/plugin.json` with `"skills": "./skills/"` - `.codex-plugin/plugin.json` at root with `"skills": "./skills/"` - `.opencode/plugins/entire.js` resolves to `../../skills` - `.agents/plugins/marketplace.json` source `./` - `GEMINI.md` imports from `./skills/session-handoff/SKILL.md` - `plugins/` directory removed - `README.md` install section rewritten with per-agent collapsible sections (Claude Code, Cursor, Gemini, OpenCode, Codex, Copilot) The `git clone ... ~/.cursor/skills/entire` flow for Cursor will now work because skills live at the conventional top-level `skills/` path. Want me to commit and push, or test a specific agent install first?