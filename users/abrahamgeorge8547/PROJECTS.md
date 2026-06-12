---
# Projects — AbrahamGeorge8547

## Repos

| Repo | Share |
|------|-------|
| `osvauld/osvauld` | 100% |

---

## osvauld/osvauld ★ DOMINANT

### What It Is

A local-first, offline-capable P2P collaboration platform. Peers (owners, collaborators, viewers) sync CRDT documents (using [LoroDoc](https://loro.dev)) over a custom QUIC-based protocol. Authorization uses cryptographic permits signed with DID keys. A Lua scripting layer allows app-level logic (group chat, DMs, presence) to run on top of the protocol without touching protocol code.

### Crate Structure (inferred from prompts)

| Crate | Role |
|-------|------|
| `gurkha` | Permit parsing and authorization decisions |
| `scribe` | CRDT document actor — owns LayerUnits, manages sync state |
| `courier` | P2P networking, PeerActor, wire protocol messages |
| `butler` | Storage layer — SQLite tables for permits, layers, sync vectors |
| `sthalam` | Desktop app shell (Slint UI + Lua runtime) |
| `kunki` | Always-on node process |
| `lua_runtime` | Lua scripting host |
| `renderer_slint` | Slint UI renderer |
| `logging_utils` | JSONL event capture system |
| `integration_tests` | Rust integration test suite |
| `app_test` | Multi-peer test runner |
| `e2e_tests/` | Python end-to-end test scripts |
| `scripts/osvauld/` | Python scenario/client helpers |

### Key Concepts Abraham Works With

- **LayerUnit**: Per-layer CRDT unit owning `authorized_dids`, dirty flag, sync state
- **Permits**: Cryptographic capability tokens — page permits (static layer access), layer permits (dynamic layer access), authority permits (creator grants node rights)
- **sync_meta**: Protocol-owned `__sync_meta/{did}` layer tracking which layers a peer syncs; used for offline-first layer discovery
- **Dynamic layers**: Layers created at runtime (e.g., `channels/did:key:alice/project-x/messages`) vs static (e.g., `channels/general/messages`)
- **SyncOffer/SyncAccept/SyncAck**: 3-step CRDT delta sync protocol
- **LayerSync/LayerConsent**: Bundled permit+data messages replacing the old race-prone `LayerPermitMsg`+`SyncOffer` split

### Recurring Themes in Sessions (2026-02-13 to 2026-02-15)

1. **Per-layer authorization refactor**: Moving `authorized_dids` from `SubscriberInfo` to `LayerUnit`; replacing N×M permit checks with O(1) per-layer lookup
2. **LayerAccessPolicy**: Replacing ad-hoc `authorized_dids` HashSet with a first-class enum (`PagePermit`, `RoleBased`, `Explicit`)
3. **Custom channel / DM sync via sync_meta**: Making dynamic layer discovery offline-first through the `__sync_meta` protocol layer
4. **Unified LayerSync protocol**: Bundling permit + data to eliminate race conditions
5. **Observability / JSONL captures**: Adding structured event emissions across Scribe, Courier, Butler for AI-assisted debugging
6. **Panic isolation**: Wrapping Slint app timer callbacks in `catch_unwind` so one crashed app doesn't kill the whole shell
7. **Scribe decomposition**: Replacing 4 scattered collections in `ScribeState` with `LayerUnit` structs

### Sample Apps

- `sample_apps/group-chat/` — standalone group chat app used for testing (split from `osvauld-demos` for cleaner logs)
- `sample_apps/osvauld-demos/` — original demo collection (game + chat + other apps)

### Test Topology

Typical e2e test: alice (owner), bob + carol (viewers/collaborators), node (kunki). Test sessions kept alive in tmux (`tmux attach -t <test_name>`). Captures at `/tmp/<test_name>/captures/`.
