---
# PROJECTS.md — pc035860
---

## pc035860/cee — **DOMINANT** (65.9% of sessions)

**What it is:** A personal macOS image viewer application, written in Swift (Swift 6).
AppKit-based with some SwiftUI elements. Targets macOS 14+, builds with XcodeGen (`project.yml`).

**What the user does here:**
- Implements and debugs complex trackpad gesture handling (`NSScrollView` subclass, `NSEvent.phase`,
  `momentumPhase`, page-turn momentum locking, overscroll accumulator)
- Builds new viewing modes: Continuous Scroll mode (phases 1–4+), Grid View (QuickGridView),
  DuoPage (dual-page) mode with RTL/LTR toggle
- Adds macOS localization: `zh-Hant.lproj/Localizable.strings` + `en.lproj/Localizable.strings`
- Manages window resizing behavior (auto-fit, position preservation on resize)
- Maintains spec files in `specs/brainstorm/` and `specs/plan/` directories
- Iterates on UX feel for trackpad (sensitivity thresholds, momentum isolation)

**Tech stack:**
- Swift 6, AppKit (`NSScrollView`, `NSEvent`, `NSWindowController`, `NSViewController`)
- XcodeGen (`project.yml`)
- Custom slash skills: `/auto-impl`, `/silennai:debug`, `/review-loop`, `/explore`
- Codex and Gemini used as cross-reviewers

**Recurring themes:**
- Trackpad gesture feel (momentum locking, sensitivity levels, edge lock behavior)
- Scroll position preservation during window resize and mode transitions
- Continuous scroll mode implementation (multi-phase spec)
- Grid View keyboard navigation and animation smoothness
- DuoPage RTL/LTR navigation logic
- Localization string alignment between zh-Hant and en

---

## pc035860/agent-tail (34.1% of sessions)

**What it is:** A terminal tool (Node.js/TypeScript) that monitors Claude Code and Codex AI agent
sessions, displaying output in tmux panes. Supports auto-switching, pane management, subagent
detection, and custom pane titles.

**What the user does here:**
- Adds Codex subagent support (flat subagent model, suppressing subagent history in main pane)
- Implements and refines pane title display (nickname-based, removing UUID prefixes)
- Debugs pane opening logic (infinite "Opening pane" log loop, timing issues)
- Maintains `specs/plan/` documents for features
- Uses `/commit --auto`, `/simplify`, `/review-loop` for git hygiene

**Tech stack:**
- TypeScript (Node.js), tmux (`tmux split-window`, `tmux select-pane -T`)
- File watchers for detecting agent session files
- Custom skills: `/review-loop`, `/commit`, `/simplify`, `/doc-update`, `/memory-cleanup`

**Recurring themes:**
- Subagent detection and pane assignment (Claude vs. Codex flat vs. hierarchical)
- Pane title formatting (nickname, agent type, no UUID prefix)
- Auto-switch suppression for subagents
- `--pane` mode startup behavior (suppressing historical subagent content)
