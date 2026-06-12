---
name: spec-dump-kickoff
description: "Trigger: opening a session for a complex new feature. blittle sends a 300–1000-word markdown plan document as his first message, prefixed with 'Implement the following plan:'. The plan includes context, a files-to-modify table, and step-by-step implementation notes with code snippets."
---

# spec-dump-kickoff

When blittle opens a session to implement a significant feature, he sends a self-contained markdown plan as his first message. The plan is structured, technical, and includes file paths, code examples, and sometimes ASCII diagrams. He expects the agent to execute the plan as written without asking clarifying questions.

The opening message is always prefaced by **"Implement the following plan:"** followed immediately by the plan document.

This is his primary way of delegating implementation. He writes or co-develops the plan before the session; the session is for execution, not design.

## Examples

**Example 1** (Phase 4 chapter transitions plan, ~1008 words):
> "Implement the following plan: # Phase 4: Seamless Chapter Transitions ## Context Currently Pressy is an MPA — each chapter is a separate HTML page with its own JS bundle that statically imports one MDX chapter. Clicking \"next chapter\" triggers a full page reload (`window.location.href`). This breaks the reading flow. Phase 4 makes chapter boundaries invisible by dynamically loading and appending next-chapter content to the CSS column container... ## Files to Modify | File | Change | |------|--------| | `packages/pressy/src/vite/plugin.ts` | New virtual module..."

**Example 2** (PWA install button plan, ~503 words):
> "Implement the following plan: # Add PWA Install Button to Home Page ## Context The home page has a \"Start Reading\" / \"Continue Reading\" CTA button. The user wants an \"Install\" button next to it that triggers the browser's PWA install prompt... ## Files to Modify | File | Changes | |------|---------| | `packages/pressy/src/runtime/offline.ts` | Add `installPrompt` signal + `setupInstallPrompt()` + `triggerInstall()` |..."
