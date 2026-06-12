# Projects — roo-oliv

## roo-oliv/monodreams ★ dominant (70% of sessions)

**What it is**: A personal MonoGame game framework built on the DefaultEcs ECS (Entity-Component-System) library. Contains both the core library (`MonoDreams/`) and an examples project (`MonoDreams.Examples/`) that doubles as a testbed for game features.

**Tech stack**: C# / .NET, MonoGame, DefaultEcs, float-precision AABB collision math.

**What roo-oliv does here**:
- Implements and debugs collision detection/resolution systems (AABB ray-casting, `DynamicRectVsRect`, contact time math, `ParallelSystem` → `SequentialSystem` fixes).
- Builds and debugs rendering pipelines (`MasterRenderSystem`, `CullingSystem`, `SpritePrepSystem`, `TextPrepSystem`) — particularly camera-based culling vs. UI render targets.
- Implements ECS-idiomatic systems with component tags (`Visible`, `DrawComponent`, `Transform` hierarchies).
- Builds game features: dialogue system with entity hierarchies, level selection screen, trigger zones.
- Configures development tooling (Claude Code hooks, macOS notifications via `osascript`).

**Recurring themes**:
- Render target distinction (Main world-space vs. UI/HUD screen-space) causing culling bugs.
- ECS system ordering issues (parallelism where sequentialism is required).
- Float-precision geometry bugs surfacing as gameplay issues (snapping, ghost collisions).
- Parent-child transform hierarchies for composing multi-sprite UI elements.

**Key files seen**: `CollisionDetectionSystem.cs`, `TransformCollisionDetectionSystem.cs`, `CollisionResolutionSystem.cs`, `MasterRenderSystem.cs`, `CullingSystem.cs`, `DialogueSystem.cs`, `LevelSelectionScreen.cs`, `LoadLevelExampleGameScreen.cs`.

---

## roo-oliv/claude-assisted-review-plugin (30% of sessions)

**What it is**: A code review plugin that uses Claude via MCP server to assist with PR reviews. Has a diff UI rendered in HTML/CSS (`mcp-server/template.mjs`).

**Tech stack**: JavaScript/Node.js MCP server, HTML/CSS diff viewer, GitHub (`gh` CLI for PR creation).

**What roo-oliv does here**:
- CSS/layout fixes for the diff gutter (line number wrapping at multi-digit line numbers).
- Initial project setup (first commit, push, remote configuration).
- PR creation via `gh`.

**Recurring themes**:
- Small, targeted CSS fixes — exact pixel values, calc expressions.
- Initial repo bootstrap (commit, push, PR).

**Key files seen**: `mcp-server/template.mjs` (CSS in template literal).
