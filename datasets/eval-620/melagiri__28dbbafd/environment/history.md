> DEVELOPER

Thomas from entire.io wrote this on LinkedIn:
View Thomas Dohmke’s profile
Thomas Dohmke
  • Following
Co-founder & CEO at Entire
20h • 




Today, Entire is open sourcing our next release: Skills, teaching your agent how to use the full context the Entire CLI captures behind your code changes: prompts, transcripts, and the decisions behind every commit, alongside your git history.

Instead of looking up syntax or running commands yourself, you can ask in plain language and let your agent drive the workflow. This initial release enables your agent to:

Hand off between agents - The session-handoff skill picks up where another agent left off by reading the saved or active session and summarizing the task state, important discoveries, blockers, and next steps. 

Explain why code exists - The explain skill traces a function, file, or line back to the session that created it, so your agent can answer the intent behind code, not just describe what the code currently does. 

Investigate changes - The what-happened skill combines git blame with Entire checkpoint context to explain why a specific block of code looks the way it does. It is useful during code review or when you are investigating a regression. 

Search […]

> AGENT

This touches competitive landscape, feature viability, and product positioning — let me bring in the devtools-cofounder for a proper strategic read before I give you my own take.

> TOOL

tool_use Agent
id: toolu_01V5SJcLfZESgnLybiFRGAJF
```json
{
  "description": "Competitive analysis: Entire.io Skills vs Code Insights",
  "subagent_type": "devtools-cofounder",
  "prompt": "Entire.io just open-sourced a \"Skills\" system for AI agents. Thomas Dohmke (CEO) described it on LinkedIn. Here's what it does:\n\n**Entire.io Skills (just open-sourced):**\n- **session-handoff**: Picks up where another agent left off by reading saved/active sessions and summarizing task state, discoveries, blockers, next steps\n- **explain**: Traces a function/file/line back to the session that *created* it — answers \"why does this code exist\"\n- **what-happened**: Combines git blame with checkpoint context to explain why a block of code looks a specific way (useful during code review / regression investigation)\n- **search**: Finds prior work in Entire history by topic, repo, branch, author, or time window — brings past context into the current task before making changes\n\nGitHub: https://github.com/entireio/skills\n\n**Code Insights (what we build):**\n- Free, open-source, local-first tool for analyzing AI coding sessions\n- Multi-source: parses sessions from Claude Code, Cursor, Codex CLI, Copilot CLI, VS Code Copilot Chat (5 providers)\n- SQLite database at ~/.code-insights/data.db (Schema V9) with structured session analysis\n- CLI + browser dashboard (Vite + React SPA served by Hono)\n- **Session analysis**: 7 character types (deep_focus, bug_hunt, etc.), friction taxonomy (9 categories), effective patterns (8 categories), prompt quality scoring, […]

> TOOL

tool_result
id: toolu_01V5SJcLfZESgnLybiFRGAJF
```
## Strategic Assessment: Entire.io Skills vs Code Insights

### The Real Differentiation

These tools occupy **adjacent but distinct categories**:

| Dimension | Entire.io Skills | Code Insights |
|-----------|------------------|---------------|
| Primary user | The *active* AI agent | The *human* developer |
| Time orientation | Present ("what should I do now?") | Past + present ("how did I work?") |
| Output consumer | LLM context window | Human reflection |
| Scope | Single session continuity | Cross-session pattern aggregation |
| Question answered | "What was happening here?" | "How am I getting better?" |

Entire.io is **agent infrastructure** — runtime context plumbing so the next agent invocation has memory. Code Insights is **developer self-reflection** — analytics so the human builds metacognition about their AI usage.

These are not the same product. Entire.io's "explain" answers "why does this code exist" by replaying the session that created it. That's git blame for AI sessions. Code Insights' Reflect answers "are my prompts getting more specific over time?" That's a fitness tracker for AI collaboration.

### Risk Assessment

**Low overlap, but watch the boundary:**
- Entire.io's `search` (topic/repo/time window) brushes against our session search. If they […]

> AGENT

Really sharp analysis. Here's the synthesis:

---

**TL;DR: Complementary, not competitive. Don't pivot — but one idea is worth watching.**

### The Fundamental Difference

Entire.io Skills is **agent runtime infrastructure** — it gives the *active AI agent* memory and context during a task. Code Insights is **developer self-reflection** — it helps the *human* understand how they're working with AI over time.

| Dimension | Entire.io Skills | Code Insights |
|-----------|-----------------|---------------|
| Primary user | The AI agent | The human developer |
| Time frame | Present task continuity | Cross-session patterns |
| Output consumer | LLM context window | Human dashboard/reflection |
| Core question | "What was happening here?" | "How am I getting better?" |

They don't compete for the same install slot. Their skills plug into agents at runtime; our CLI is installed by humans who want metacognition.

---

### The One Idea Worth Watching

Their **`explain` skill** — "trace code back to the session that created it" — is genuinely interesting and adjacent to our data model. We already have tool calls with file edits in SQLite. A reverse index from code location → session is *theoretically* possible with what we have.

But […]

> DEVELOPER

does it have any impact in the new plan we are building at @docs/superpowers/specs/2026-05-05-codebase-knowledge-design.md

> AGENT

Let me cross-reference the spec sections against Entire.io's four skills carefully.

`★ Insight ─────────────────────────────────────`
- Design specs that name competitors by name become stale the moment those competitors ship — this is a good example of why specs should capture *principles* rather than competitor comparisons.
- The spec's `code-insights context <topic>` (Phase 2) and Entire.io's `search` skill solve adjacent problems at different granularities: Code Insights aggregates across 400 sessions into themes; Entire.io retrieves the specific session for a specific line of code.
`─────────────────────────────────────────────────`

Here's the impact breakdown:

---

### What Entire.io changes in the spec

**One concrete edit needed — Section 9.4 (`--check` CI staleness gate):**

> "Unique differentiator — CLAUDE.md, Cursor rules, and entire.io have no freshness enforcement mechanism."

That claim names Entire.io specifically and is now potentially stale. They may add a freshness mechanism post-open-source. The claim should be softened to remove the Entire.io reference — the uniqueness of `--check` stands on its own without the competitor comparison.

---

### What Entire.io *validates* in the spec (no changes needed, but good signal)

| Spec Feature | Validation Signal |
|---|---|
| Phase 2 `context <topic>` | Entire.io's `search` skill confirms "query past work by topic" is a real […]

> TOOL

tool_use Edit
id: toolu_01GG8iuBeWWEie3yYRQVT2Gt
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Workspace/codeInsights/code-insights/docs/superpowers/specs/2026-05-05-codebase-knowledge-design.md",
  "old_string": "**Verdict:** Include in Phase 1. Trivial to implement, zero LLM calls, direct SQLite read. Unique differentiator — CLAUDE.md, Cursor rules, and entire.io have no freshness enforcement mechanism.",
  "new_string": "**Verdict:** Include in Phase 1. Trivial to implement, zero LLM calls, direct SQLite read. No equivalent freshness enforcement exists in CLAUDE.md, `.cursorrules`, or competing knowledge extraction tools."
}
```

> TOOL

tool_result
id: toolu_01GG8iuBeWWEie3yYRQVT2Gt
```
The file /home/<USER>/Workspace/codeInsights/code-insights/docs/superpowers/specs/2026-05-05-codebase-knowledge-design.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

---

**Summary:** One sentence updated in Section 9.4 to remove the now-stale competitor name. Everything else in the spec stands — Entire.io's release mostly validates the direction rather than threatening it. The multi-source moat and the `--check` CI gate are both stronger differentiators than they were yesterday.