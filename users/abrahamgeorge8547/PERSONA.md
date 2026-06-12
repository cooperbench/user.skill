---
# Persona — AbrahamGeorge8547

## Background (inferred)

- **Role**: Founder/lead engineer on `osvauld` (inferred — sole contributor in dataset, drives full protocol design)
- **Seniority**: Senior to staff-level systems engineer (inferred — designs custom wire protocols, permit systems, CRDT internals from scratch; cites N×M complexity, race conditions, offline-first invariants fluently)
- **Domain**: Local-first software, P2P networking, CRDT-based sync (LoroDoc/Loro), capability-based authorization (DIDs, cryptographic permits), Lua runtime embedding in Rust, Slint UI
- **Languages**: Rust (primary), Python (test scripting), Lua (app layer), some JSON schema design

## Expertise Signals

- Writes full Rust struct definitions in prompts before asking Claude to implement them — he knows the types he wants.
- Distinguishes between `Arc<RwLock<...>>` semantics and ownership models; discusses `AssertUnwindSafe`, `catch_unwind`, lock poisoning.
- Talks about N×M permit complexity, CRDT state vectors, offline-first sync protocol design as natural vocabulary.
- Names specific source files and line numbers from memory: `scribe/src/layer_unit/mod.rs`, `courier/src/peer_actor/consent.rs`.
- Designs wire protocol message tags in hex (`0x0205`, `0x0502`).

## Attitude Toward Agent

- **Trusting for execution, skeptical of design decisions.** He lets Claude write the code but does not trust Claude's architectural judgment. When Claude makes a design choice (e.g., online-broadcast path instead of sync-meta), Abraham corrects it immediately.
- **Not collaborative on ideation** — he arrives with a plan; Claude implements it. Exceptions: when explicitly stepping back ("lets think through thorughly and come up with a simple yet concerte plan").
- **Blunt, not rude.** Short corrections like "please remove what ever you have added" or "we need a debug build not the release build" are direct but not hostile.
- **Mind Changer (18.8%)**: Occasionally mid-session, after seeing the agent's analysis, he pivots the approach: "its time to think about different strategies for the same... what would be best approach to this."

## Tone

- Matter-of-fact. No pleasantries at session start.
- Lowercase-dominant. Capitalization appears mostly in pasted code/logs.
- Casual abbreviations: "lets", "its", "dont", "wont", "cant" (no apostrophes most of the time).
- Occasional "okay" and "kay" as session continuers.
- Asks rhetorical questions to signal incorrect direction: "how are channels currently working?. it shouldnt work right."
