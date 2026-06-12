---
name: error-paste-debug
description: >
  Trigger: something broke during live testing — install CLI, website rendering,
  npm publish, or UI behavior. Armel pastes the full terminal output or describes
  the observed vs expected with a live URL.
---

Armel reports failures by pasting verbatim terminal output (including ASCII banners, prompts,
full install logs) or by stating the live URL and observed behavior. He does not summarize
or trim the output. He may ask a rhetorical question ("Are you sure it works?") before the paste.

For UI bugs he gives the live URL and one sentence on what's wrong.
For install/CLI bugs he pastes the full session from the `armel@dzeta:` prompt.

## Examples

**CLI install failure with full session paste:**
> "Are you sure it works? I just tried it here but look at the `fast` repo: armel@dzeta:~/Projects/demo/fast$ node /home/armel/Projects/OSS/bmad-module-skill-forge/tools/skf-npx-wrapper.js install ┌ ____ _ _______ ..."

**NPM publish failure:**
> "I have just publish skf to npm following @_bmad-output/npm-release-guide.md. However, my project is not avaible after run armel@dzeta:~/Projects/temp$ npx bmad-module-skill-forge install npm error could not determine executable to run ..."

**UI dark mode bug:**
> "the app is ready up at http://localhost:4321/. Why I have a different layout when I switch to dark mode?"

**UI diagram bug:**
> "The app is live at http://localhost:4321/architecture/. When I click on the diagram, it is shown too small."

**Untested state correction:**
> "you did not test it in light mode"

**YAML parse error paste:**
> "I got this error when I tried to install the skf module:  Module directories created │ │ ▲  Failed to parse workflow at /home/armel/Projects/demo/quick/_bmad/skf/workflows/audit-skill/workflow.md: Nested mappings are not allowed in compact mappings at line 2, column 14:"

**File reference for bug context:**
> "read the bug we described in @installation-bug.txt . See @temp/BMAD-METHOD-main/ reference that also generate IDE specfic configurations."
