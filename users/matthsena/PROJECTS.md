# Projects — matthsena

## matthsena/reef-coder ★ DOMINANT (100% of sessions)

**What it is:** A terminal-based multi-agent ACP (Agent Client Protocol) client. Lets the user switch between multiple AI coding engines (Claude Code, Codex/OpenAI, formerly Gemini CLI) in a single terminal session, with shared context and persistent sessions.

**Formerly called:** agent-swarm → Relay → reef-coder (name iterated mid-development)

**Tech stack:**
- Bun runtime
- TypeScript + React (Ink terminal UI)
- ACP SDK (`@agentclientprotocol/sdk`)
- `bun:test` for testing
- `ink-testing-library` for component tests
- arecord + OpenAI Whisper (voice input feature)
- Sessions stored in `.reef/` directory (JSON files)

**Key subsystems the user works on:**

| Subsystem | Files | Recurring themes |
|-----------|-------|-----------------|
| Engine/model selection | `src/components/EngineSelect.tsx`, `src/components/ModelSelect.tsx`, `src/types.ts` | Adding predefined models, fixing navigation bugs |
| Session persistence | `src/session-manager.ts` | Directory naming (data → .data → .reef), session ID display |
| Agent client | `src/agent-client.ts` | Path traversal fixes, writeFile with mkdir, permission handling |
| Terminal manager | `src/terminal-manager.ts` | Shell execution, resource leaks, `releaseAll()` |
| Prompt input | `src/components/PromptInput.tsx` | Cursor behavior, keyboard shortcuts (Home/End/Del/Backspace), `@` file picker |
| Image/file references | `src/image-utils.ts`, `src/file-utils.ts` | `@image:path` → `@path` unification, base64 encoding, MIME detection |
| Voice input | `src/voice-input.ts`, `src/hooks/useVoiceInput.ts` | arecord + Whisper transcription, Tab toggle |
| Status bar / UI | `src/components/StatusBar.tsx`, `src/components/Chat.tsx` | Header pinning, session ID display, internationalization (PT→EN) |

**Recurring frustrations:**
- Gemini CLI support (eventually removed entirely — "olha o gemini esta dando muito problema... retire totalmente o suporte ao gemini")
- Git co-author lines appearing in commits
- Cursor not ending up where expected after UI interactions
- OpenAI API key not being embedded in built binary

**Product positioning (as the user described it):**
> "Voice-first terminal for AI coding agents. Speak or type, switch between Claude, Codex & more — sessions and memory persist across engines."

Logo: a coral/reef aesthetic. Sessions directory named `.reef`.
