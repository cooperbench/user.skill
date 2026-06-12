# Projects — eneakllomollari

## eneakllomollari/mpad ★ DOMINANT (100% of activity)

**What it is**: A WYSIWYG Markdown editor — desktop app, built on TipTap (ProseMirror-based rich-text framework) wrapped in a Tauri shell, served at `http://localhost:5173`.

**What the user does here**: Adversarial end-to-end testing of the editor's core interactions, fixing bugs found in those tests, and committing/pushing after each cycle.

**Tech stack**:
- TipTap (rich-text editor engine)
- Tauri (desktop shell / native wrapper)
- React + TypeScript (frontend)
- Vite (dev server at port 5173)
- Vitest (unit tests — 83 tests across 11 files, all passing)
- ESLint, oxlint, knip (linting and dead-code detection)
- `tsc` (TypeScript type checking)
- `/expect` CLI (E2E smoke test runner for browser interactions)

**Key file**: `src/components/Editor.tsx` — cited as the likely source of INP performance issues

**Test URL**: `http://localhost:5173?file=demo`

**Recurring themes**:
- Testing editor interactions adversarially (bubble menu, slash commands, undo/redo, source toggle, table editing)
- Markdown roundtrip fidelity (WYSIWYG ↔ source view)
- XSS prevention and content sanitization
- Performance (INP, Long Animation Frames)
- Accessibility (aria-label, WCAG contrast)
- Git push as punctuation between work cycles

**Known bugs found during sessions**:
- INP 536ms (poor) — 50 Long Animation Frames during formatting interactions
- Missing `aria-label` on editor textbox (WCAG violation)
- Code block syntax highlight contrast failures (2.74–3.70 vs required 4.5:1)
- `execCommand('insertHTML')` can bypass TipTap sanitization (low severity, requires existing JS context)
- CLAUDE.md documents heading cycling as "H1/H2/H3" but actual behavior is H1–H6 + paragraph
- Escape key conflict between find bar and command palette
