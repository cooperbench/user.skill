> DEVELOPER

/Users/jdsingh/Library/Application\ Support/Claude/local-agent-mode-sessions/761816a7-837d-4864-8aa8-faa8499e6aef/a93f257c-027e-4b3c-9ae1-97aba2fe0035/local_ff5d85f8-b376-45da-a6c9-bd86226d1ee7/outputs/gsd-claude-code

Using the above in context, lets add the following feature to the application:
- ability to see the 4 agents embedded in the system in detail with context

> AGENT

Let me explore the codebase to understand the agents and current structure.

> TOOL

tool_use Agent
id: toolu_01PPfYampFnR29YkvvPa7HZc
```json
{
  "description": "Explore agents in codebase",
  "prompt": "I need to understand the \"agents\" in this Forge application. The user says there are 4 agents embedded in the system. \n\nSearch for:\n1. Any agent definitions, configurations, or references to specific agent types/roles\n2. Look at the review system (src/review/specialists.rs, src/review/arbiter.rs) as these might be agents\n3. Look at the swarm executor (src/swarm/executor.rs) for agent roles\n4. Check the factory pipeline (src/factory/pipeline.rs) for agent references\n5. Check any config files or enums that define agent types\n6. Look at the UI (ui/src/) for any existing agent views\n7. Check README.md and .forge/spec.md for agent documentation\n\nI need to identify exactly what the 4 agents are and how they're configured/used.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: toolu_01VxxJLq125SAfxMqn5jx53C
```json
{
  "description": "Explore Factory UI structure",
  "prompt": "Explore the Factory UI at ui/src/ to understand:\n1. The overall structure (routes, components, pages)\n2. How the UI currently displays information\n3. What API endpoints are available (check src/factory/api.rs)\n4. The current navigation/sidebar structure\n5. Any existing detail views that could serve as templates for an \"agents\" view\n\nBe thorough - look at package.json, router config, main layout components, and existing views.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_01PPfYampFnR29YkvvPa7HZc
```
Perfect! Now I have comprehensive understanding. Let me compile this into a clear summary report for the user.

## Summary: The 4 Embedded Agents in Forge

Based on my thorough search through the Forge codebase, I can identify **4 built-in Review Specialist agents** that are embedded in the system. These are not separate autonomous agents, but rather **specialist roles that Claude Code swarms can assume** when running code reviews during swarm execution.

### The 4 Review Specialist Agents

All defined in `/Users/jdsingh/Projects/AI/forge/src/review/specialists.rs` and `/Users/jdsingh/Projects/AI/forge/src/swarm/context.rs`:

1. **Security Sentinel** (`security-sentinel`)
   - Type: `SpecialistType::SecuritySentinel`
   - Focus Areas: SQL injection, XSS, authentication bypass, secrets exposure, input validation, command injection, path traversal, insecure deserialization
   - Default: Gating (blocks phase completion if issues found)
   - Purpose: Security-focused code review

2. **Performance Oracle** (`performance-oracle`)
   - Type: `SpecialistType::PerformanceOracle`
   - Focus Areas: N+1 query patterns, missing indexes, memory leaks, algorithmic complexity, unnecessary allocations, blocking async operations, cache issues, inefficient data structures
   - Default: Non-gating (advisory only)
   - Purpose: Performance and resource usage analysis

3. **Architecture Strategist** (`architecture-strategist`)
   - Type: `SpecialistType::ArchitectureStrategist`
   - Focus Areas: SOLID violations, coupling, layering, separation of concerns, circular dependencies, abstraction levels, weak interfaces, god objects
   - Default: Gating (blocks phase completion if issues found)
   - Purpose: Architectural and design pattern review

4. **Simplicity Reviewer** (`simplicity-reviewer`)
   - Type: `SpecialistType::SimplicityReviewer`
   - Focus Areas: Over-engineering, premature abstraction, YAGNI violations, unnecessary complexity, dead code, overly clever solutions, excessive indirection, configuration abuse
   - Default: Non-gating (advisory only)
   - Purpose: Simplicity and code clarity analysis

### How They Work

The 4 agents operate within the **swarm orchestration system**:

1. **Orchestration**: When `forge swarm` is executed with review specialists enabled (e.g., `--review security,performance`), a **swarm leader agent** is spawned via Claude Code

2. **Task Distribution**: The leader creates a team (via `TeammateTool`) and spawns **worker agents** for task execution

3. **Review Phase**: After tasks complete, the leader spawns **review specialist agents** for each enabled specialist type (can run in parallel with `parallel: true`)

4. **Completion**: Reviews either gate or advisory based on configuration, and results are aggregated in the `<swarm_complete>` signal

### Key Files

- **Specialist Definitions**: `/Users/jdsingh/Projects/AI/forge/src/review/specialists.rs` (197 built-in types, can add custom)
- **Swarm Context Types**: `/Users/jdsingh/Projects/AI/forge/src/swarm/context.rs` (orchestration configuration)
- **Prompt Generation**: `/Users/jdsingh/Projects/AI/forge/src/swarm/prompts.rs` (instructions for spawning agents)
- **Execution**: `/Users/jdsingh/Projects/AI/forge/src/swarm/executor.rs` (manages Claude Code swarm lifecycle)

### CLI Usage

```bash
# Run with specific review specialists
forge swarm --review security,architecture

# Run with all built-in reviewers
forge swarm --review all

# Control gating behavior
forge swarm --review security --review-mode arbiter --arbiter-confidence 0.8
```

These agents are not separate CLI commands or independent processes—they're **specialized Claude Code agents spawned on-demand during swarm execution** to provide quality gates before phases complete.
agentId: a0065276dae01f32e (for resuming to continue this agent's work if needed)
<usage>total_tokens: 100818
tool_uses: 14
duration_ms: 31266</usage>
```

> TOOL

tool_result
id: toolu_01VxxJLq125SAfxMqn5jx53C
```
Perfect! Now I have all the information I need. Let me create a comprehensive summary document.

## Factory UI Exploration Report

Based on my thorough exploration of the Factory UI codebase, here's a comprehensive overview:

### Overall Structure

**Technology Stack:**
- React 19.2 with TypeScript
- Vite (v7.3.1) for bundling
- Tailwind CSS (v4.2) for styling
- No routing library — single-page app using view modes
- WebSocket for real-time updates
- Axios-style fetch API client

**Directory Structure:**
- `/ui/src/`
  - `App.tsx` — Main entry point (MissionControl wrapper with WebSocketProvider)
  - `main.tsx` — React root mount
  - `components/` — All UI components
  - `hooks/` — Custom hooks (useMissionControl, useAgentTeam)
  - `contexts/` — WebSocketContext for real-time pub/sub
  - `api/` — REST client wrapper
  - `types/` — Centralized TypeScript types
  - `index.css` — Tailwind + theme (CSS variables)

---

### Navigation & View Modes

The UI uses **view mode toggles** instead of traditional routing:

1. **Grid View** (default) — Cards in CSS grid layout
2. **List View** — Full-width flex column
3. **Analytics View** — Metrics dashboard

View mode toggle buttons in `StatusBar.tsx` (top-right):
```typescript
viewMode: 'grid' | 'list' | 'analytics'
```

**Navigation is simple:**
- Project sidebar (left) — filters by project
- Main area (center) — displays cards/lists/analytics
- Event log (bottom) — collapsible activity feed
- Floating action button (right) — quick actions (+New Issue, +New Project, +Sync GitHub)

---

### Core Components

#### 1. **App.tsx & MissionControl**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/App.tsx`

Main container component. Structure:
```
App
  └─ WebSocketProvider
      └─ MissionControl
          ├─ StatusBar (top)
          ├─ Flex row
          │  ├─ ProjectSidebar (left)
          │  └─ Main content (center)
          │     ├─ Grid/List/Analytics view
          │     └─ AgentRunCards + IdleIssueCards
          ├─ EventLog (bottom)
          ├─ FloatingActionButton (right)
          └─ Modals
              ├─ NewIssueModal
              ├─ ProjectSetup
              └─ ConfirmDialog
```

#### 2. **StatusBar**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/StatusBar.tsx`

Top bar displaying:
- "FORGE" logo
- System stats: `{running} running | {queued} queued | {completed} done | {failed} failed | {projects} projects`
- Command autocomplete input (center)
- View toggle buttons: grid/list/analytics
- Uptime counter (HH:MM:SS)
- WebSocket status indicator (colored dot)

#### 3. **ProjectSidebar**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/ProjectSidebar.tsx`

Left sidebar (fixed width: 200px) with:
- "All Projects" button (filter toggle)
- Project list with:
  - Status dot (pulsing if active runs)
  - Project name
  - Running count badge (if active)
  - Delete button (visible on hover)
- Selected project highlighted with green left border

#### 4. **AgentRunCard**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/AgentRunCard.tsx`

Expandable card showing:

**Collapsed view:**
- Status dot (colored by run status: running/queued/completed/failed/cancelled)
- Project badge + issue title
- Phase progress dots (visual representation of phase completion)
- Status label (RUNNING/QUEUED/DONE/FAILED/CANCELLED)
- Elapsed time (live counter)
- Expand chevron

**Expanded view (tabs):**
1. **Output Tab** — Terminal-like output showing:
   - Pipeline output events (rich text/thinking/tool_start)
   - Agent events (thinking/action/output/signal)
   - Auto-scroll to latest
   - Black background with syntax highlighting

2. **Phases Tab** — Shows all phases with:
   - Phase icon (checkmark/play/circle)
   - Phase name
   - Iteration count (e.g., "iter 2/5")
   - Review status badge (if applicable)

3. **Files Tab** — Shows:
   - Branch name (if created)
   - PR URL (if created, clickable)
   - File changes with action icons: `+ created`, `~ modified`, `- deleted`

**Props:**
- `card` — AgentRunCard (issue + run + project)
- `phases` — PipelinePhase[]
- `agentTeam` — AgentTeamDetail
- `agentEvents` — Map<taskId, AgentEvent[]>
- `pipelineEvents` — AgentEvent[] (fallback)
- `pipelineOutputEvents` — PipelineOutputEvent[]
- `pipelineFileChanges` — PipelineFileChange[]
- `onCancel` — callback for cancel button
- `viewMode` — 'grid' | 'list'

#### 5. **EventLog**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/EventLog.tsx`

Collapsible bottom panel (150px height when open) showing timestamped events:
- Color-coded by source: agent/phase/review/system/error/git
- Format: `[HH:MM:SS] [SOURCE] message`
- Auto-scrolls to latest
- Entry limit: 500 (oldest auto-pruned)

#### 6. **Analytics**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/Analytics.tsx`

Metrics dashboard with:
- Time range selector (7/30/90 days)
- Summary stats section
- Phase performance table (avg iterations, duration, success rate)
- Recent runs list with timestamps
- Fetches from `/api/metrics/summary`, `/api/metrics/phases`, `/api/metrics/runs/recent`

#### 7. **FloatingActionButton**
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/components/FloatingActionButton.tsx`

Fixed position (bottom-right, above EventLog):
- "+" button rotates 45° when open
- Vertical menu when expanded:
  - New Issue (green)
  - New Project (blue)
  - Sync GitHub (orange)

#### 8. **Supporting Components**
- **ProjectSetup.tsx** — Modal for creating/cloning projects
- **NewIssueModal.tsx** — Modal for creating issues
- **ConfirmDialog.tsx** — Generic confirmation dialog
- **CommandAutocomplete.tsx** — Command input with autocomplete

---

### Hooks

#### 1. **useMissionControl** (primary data hook)
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/hooks/useMissionControl.ts`

Aggregates all data for the dashboard:

**State managed:**
- `projects` — All projects
- `runs` — Map<runId, PipelineRun>
- `issues` — Map<issueId, Issue>
- `phases` — Map<runId, PipelinePhase[]>
- `agentTeams` — Map<runId, AgentTeamDetail>
- `agentEvents` — Map<taskId, AgentEvent[]>
- `pipelineEvents` — Map<runId, AgentEvent[]> (fallback path)
- `pipelineOutputEvents` — Map<runId, PipelineOutputEvent[]> (rich output)
- `pipelineFileChanges` — Map<runId, PipelineFileChange[]>
- `eventLog` — EventLogEntry[] (up to 500)

**Computed outputs:**
- `agentRunCards` — Sorted/filtered ActiveRunCard[] (running first, then queued, etc.)
- `idleIssueCards` — Issues without active runs
- `statusCounts` — { all, running, queued, completed, failed }

**Actions:**
- `triggerPipeline(issueId)` — Start a pipeline
- `cancelPipeline(runId)` — Cancel running pipeline
- `createIssue(projectId, title, description)`
- `createProject(name, path)`
- `cloneProject(repoUrl)`
- `deleteProject(projectId)`
- `refresh()` — Manual full reload

**WebSocket integration:**
- Subscribes to all message types
- Updates state reactively as events stream in
- Handles: PipelineStarted/Progress/Completed/Failed, TeamCreated, AgentTaskStarted/Completed, etc.

#### 2. **useAgentTeam** (agent-specific hook)
**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/hooks/useAgentTeam.ts`

Tracks agent team and merge/verification state for a single run:
- Fetches team data on mount (recovery after page refresh)
- Handles WebSocket messages: TeamCreated, AgentTaskStarted/Completed, MergeStarted/Completed, VerificationResult
- Returns: { agentTeam, agentEvents, mergeStatus, verificationResults }

---

### WebSocket Integration

**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/contexts/WebSocketContext.tsx`

Real-time pub/sub system:
- Connects to `/ws` endpoint
- Auto-reconnect logic (exponential backoff, max 20 attempts)
- Message type: `WsMessage` (union of 30+ message types)
- Usage: `useWsSubscribe(callback)` to listen to messages

**Message types include:**
- Pipeline: PipelineStarted, PipelineProgress, PipelineCompleted, PipelineFailed
- Phases: PipelinePhaseStarted, PipelinePhaseCompleted, PipelineReviewStarted/Completed
- Agent: TeamCreated, AgentTaskStarted/Completed/Failed, AgentThinking/Action/Output/Signal
- Merge: MergeStarted/Completed, MergeConflict
- Verification: VerificationResult
- Issues: IssueCreated/Updated/Moved/Deleted
- Projects: ProjectCreated/Deleted
- Output: PipelineOutputEvent, PipelineFileChanged, PipelineOutput

---

### API Client

**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/api/client.ts`

Thin wrapper over `/api` endpoints. Typed with types from `types/index.ts`.

**Available endpoints:**

| Method | Path | Function |
|--------|------|----------|
| GET | `/projects` | listProjects() |
| POST | `/projects` | createProject(name, path) |
| POST | `/projects/clone` | cloneProject(repoUrl) |
| GET | `/projects/:id` | getProject(id) |
| DELETE | `/projects/:id` | deleteProject(id) |
| GET | `/projects/:id/board` | getBoard(projectId) |
| POST | `/projects/:id/sync-github` | syncGithub(projectId) |
| POST | `/projects/:id/issues` | createIssue(projectId, title, description) |
| GET | `/issues/:id` | getIssue(id) |
| PATCH | `/issues/:id` | updateIssue(id, {title?, description?, priority?, labels?}) |
| PATCH | `/issues/:id/move` | moveIssue(id, column, position) |
| DELETE | `/issues/:id` | deleteIssue(id) |
| POST | `/issues/:id/run` | triggerPipeline(issueId) |
| GET | `/runs/:id` | getPipelineRun(id) |
| POST | `/runs/:id/cancel` | cancelPipelineRun(id) |
| GET | `/runs/:id/team` | getRunTeam(runId) |
| GET | `/runs/:id/phases` | getRunPhases(runId) |
| GET | `/tasks/:id/events` | getTaskEvents(taskId, limit=100) |
| GET | `/github/status` | githubStatus() |
| POST | `/github/device-code` | githubDeviceCode() |
| POST | `/github/poll` | githubPollToken(deviceCode) |
| POST | `/github/connect` | githubConnectToken(token) |
| GET | `/github/repos` | githubRepos() |
| POST | `/github/disconnect` | githubDisconnect() |
| GET | `/cli-help` | cliHelp() |

---

### Key Data Types

**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts`

Core entities:
- **Project** — { id, name, path, github_repo, created_at }
- **Issue** — { id, project_id, title, description, column, position, priority, labels, github_issue_number, created_at, updated_at }
- **PipelineRun** — { id, issue_id, status, phase_count, current_phase, iteration, summary, error, branch_name, pr_url, team_id, has_team, started_at, completed_at }
- **PipelinePhase** — { id, run_id, phase_number, phase_name, status, iteration, budget, started_at, completed_at, error, review_status, review_findings }
- **AgentTeam** — { id, run_id, strategy, isolation, plan_summary, created_at }
- **AgentTask** — { id, team_id, name, description, agent_role, wave, depends_on, status, isolation_type, worktree_path, container_id, branch_name, started_at, completed_at, error }
- **AgentEvent** — { id, task_id, event_type, content, metadata, created_at }

Status enums:
- **PipelineStatus** — 'queued' | 'running' | 'completed' | 'failed' | 'cancelled'
- **AgentTaskStatus** — 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
- **AgentRole** — 'planner' | 'coder' | 'tester' | 'reviewer' | 'browser_verifier' | 'test_verifier'
- **IssueColumn** — 'backlog' | 'ready' | 'in_progress' | 'in_review' | 'done'

---

### Styling & Theme

**Path:** `/Users/jdsingh/Projects/AI/forge/ui/src/index.css`

CSS variables (dark theme):
```css
--color-bg-primary: #0d1117          /* Main background */
--color-bg-card: #161b22             /* Card/panel background */
--color-bg-card-hover: #1c2333       /* Hover state */
--color-border: #30363d              /* Borders */
--color-text-primary: #e6edf3        /* Main text */
--color-text-secondary: #8b949e      /* Secondary text */
--color-success: #3fb950             /* Green: running/done */
--color-error: #f85149               /* Red: failed/error */
--color-warning: #d29922             /* Orange: queued/warnings */
--color-info: #58a6ff                /* Blue: phases/info */
--color-accent: #39d353              /* Bright green: actions */
```

Special animations:
- `.pulse-dot` — Pulsing animation for active agents (opacity 1 → 0.4 → 1)
- `.project-delete-btn` — Hidden by default, shown on hover

Layout uses **inline styles** (no CSS classes for layout) + Tailwind utility classes via `@import`.

---

### Existing Detail Views (Templates)

#### AgentRunCard Detail Tabs (Good Template)
- **Output tab** — Shows pipeline/agent output in rich format
  - Black background terminal style
  - Color-coded events by type
  - Auto-scroll
  - Max height with overflow

- **Phases tab** — Shows phase list with icons, names, iteration counts
  - Minimal styling
  - Status indicators

- **Files tab** — Shows branch, PR, file changes
  - Action indicators (+/~/-)
  - Monospace font for paths

#### Analytics View
- Time range selector (7/30/90 days)
- Multiple sections (summary stats, phase table, recent runs)
- Fetch from custom endpoints (`/api/metrics/*`)
- Error/loading states

---

### Key Architectural Insights

1. **No routing library** — Single component tree with view mode toggles
2. **Centralized state** — useMissionControl hook manages all data
3. **Real-time first** — WebSocket updates propagate immediately
4. **Card-based layout** — Everything is a card (runs, issues, projects)
5. **No detailed drill-down** — AgentRunCard is the only detail view; others are modal-based
6. **Responsive but not mobile** — Fixed sidebar, flex layouts, suitable for desktop

---

### Potential Templates for Agents View

1. **AgentRunCard detail structure** — Use the tabbed pattern for agent task details
2. **EventLog styling** — Source-colored tags + timestamps
3. **ProjectSidebar pattern** — Hierarchical list with badges and status indicators
4. **Analytics layout** — Multiple metric sections, time range selector
5. **Modal pattern** — NewIssueModal/ProjectSetup for creation dialogs

---

### Summary

The Factory UI is a **single-page React dashboard** with:
- **Left sidebar:** Project filtering
- **Center:** Grid/list/analytics of active runs and idle issues
- **Right:** Floating action button
- **Top:** Status bar with system stats and view toggle
- **Bottom:** Collapsible event log

All data flows through **useMissionControl hook** (aggregates from API + WebSocket), state updates trigger re-renders, and WebSocket messages provide real-time push updates. Component hierarchy is flat with no routing—just view mode toggles and modals for dialogs.
agentId: a4df45ef413f9807e (for resuming to continue this agent's work if needed)
<usage>total_tokens: 86248
tool_uses: 24
duration_ms: 65102</usage>
```

> AGENT

Now I understand. The 4 embedded agents are the **Review Specialists**:
1. **Security Sentinel** - SQL injection, XSS, auth bypass, etc.
2. **Performance Oracle** - N+1 queries, memory leaks, complexity, etc.
3. **Architecture Strategist** - SOLID violations, coupling, layering, etc.
4. **Simplicity Reviewer** - Over-engineering, YAGNI, dead code, etc.

Let me read the key source files to implement this properly.

> TOOL

tool_use Read
id: toolu_01JSkxoL8BizhRj4hsrLBLTG
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/review/specialists.rs"
}
```

> TOOL

tool_result
id: toolu_01JSkxoL8BizhRj4hsrLBLTG
```
     1→//! Review specialist types for quality gating.
     2→//!
     3→//! This module defines the review specialists that can examine phase outputs
     4→//! and provide quality gates before progression. Each specialist type has
     5→//! default focus areas appropriate to its domain.
     6→//!
     7→//! ## Specialist Types
     8→//!
     9→//! - [`SpecialistType::SecuritySentinel`]: Security-focused review
    10→//! - [`SpecialistType::PerformanceOracle`]: Performance-focused review
    11→//! - [`SpecialistType::ArchitectureStrategist`]: Architecture-focused review
    12→//! - [`SpecialistType::SimplicityReviewer`]: Simplicity/over-engineering review
    13→//! - [`SpecialistType::Custom`]: User-defined review type
    14→//!
    15→//! ## Example
    16→//!
    17→//! ```
    18→//! use forge::review::{ReviewSpecialist, SpecialistType};
    19→//!
    20→//! // Create a gating security review
    21→//! let security = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
    22→//! assert_eq!(security.display_name(), "Security Sentinel");
    23→//! assert!(security.focus_areas().iter().any(|a| a.contains("injection")));
    24→//!
    25→//! // Create a non-gating custom review
    26→//! let custom = ReviewSpecialist::new(
    27→//!     SpecialistType::Custom("API Compliance".to_string()),
    28→//!     false
    29→//! ).with_focus_areas(vec!["REST conventions".to_string()]);
    30→//! ```
    31→
    32→use serde::{Deserialize, Serialize};
    33→use std::str::FromStr;
    34→
    35→/// Type of review specialist.
    36→///
    37→/// Each type represents a domain of expertise with default focus areas.
    38→///
    39→/// ## Deserialization
    40→///
    41→/// This type supports multiple deserialization formats:
    42→/// - Short-form strings: `"security"`, `"performance"`, `"architecture"`, `"simplicity"`
    43→/// - Long-form strings: `"security_sentinel"`, `"performance_oracle"`, etc.
    44→/// - Hyphenated strings: `"security-sentinel"`, `"performance-oracle"`, etc.
    45→/// - Tagged object for custom: `{"custom": "my-review"}`
    46→#[derive(Debug, Clone, Default, Serialize, PartialEq, Eq, Hash)]
    47→#[serde(rename_all = "snake_case")]
    48→pub enum SpecialistType {
    49→    /// Security-focused review examining vulnerabilities and security best practices.
    50→    #[default]
    51→    SecuritySentinel,
    52→    /// Performance-focused review examining efficiency and resource usage.
    53→    PerformanceOracle,
    54→    /// Architecture-focused review examining design patterns and structure.
    55→    ArchitectureStrategist,
    56→    /// Simplicity-focused review examining over-engineering and complexity.
    57→    SimplicityReviewer,
    58→    /// Custom review type with user-defined name.
    59→    Custom(String),
    60→}
    61→
    62→impl SpecialistType {
    63→    /// Get the human-readable display name for this specialist type.
    64→    ///
    65→    /// # Examples
    66→    ///
    67→    /// ```
    68→    /// use forge::review::SpecialistType;
    69→    ///
    70→    /// assert_eq!(SpecialistType::SecuritySentinel.display_name(), "Security Sentinel");
    71→    /// assert_eq!(SpecialistType::Custom("My Review".to_string()).display_name(), "My Review");
    72→    /// ```
    73→    pub fn display_name(&self) -> &str {
    74→        match self {
    75→            Self::SecuritySentinel => "Security Sentinel",
    76→            Self::PerformanceOracle => "Performance Oracle",
    77→            Self::ArchitectureStrategist => "Architecture Strategist",
    78→            Self::SimplicityReviewer => "Simplicity Reviewer",
    79→            Self::Custom(name) => name,
    80→        }
    81→    }
    82→
    83→    /// Get the agent name used for spawning review agents.
    84→    ///
    85→    /// This is a lowercase, hyphenated version suitable for agent identifiers.
    86→    ///
    87→    /// # Examples
    88→    ///
    89→    /// ```
    90→    /// use forge::review::SpecialistType;
    91→    ///
    92→    /// assert_eq!(SpecialistType::SecuritySentinel.agent_name(), "security-sentinel");
    93→    /// assert_eq!(SpecialistType::Custom("Code Quality".to_string()).agent_name(), "code-quality");
    94→    /// ```
    95→    pub fn agent_name(&self) -> String {
    96→        match self {
    97→            Self::SecuritySentinel => "security-sentinel".to_string(),
    98→            Self::PerformanceOracle => "performance-oracle".to_string(),
    99→            Self::ArchitectureStrategist => "architecture-strategist".to_string(),
   100→            Self::SimplicityReviewer => "simplicity-reviewer".to_string(),
   101→            Self::Custom(name) => name.to_lowercase().replace(' ', "-"),
   102→        }
   103→    }
   104→
   105→    /// Get the default focus areas for this specialist type.
   106→    ///
   107→    /// Returns a list of specific concerns this specialist should examine.
   108→    /// Custom specialists return an empty list by default.
   109→    ///
   110→    /// # Examples
   111→    ///
   112→    /// ```
   113→    /// use forge::review::SpecialistType;
   114→    ///
   115→    /// let security = SpecialistType::SecuritySentinel;
   116→    /// let areas = security.focus_areas();
   117→    /// assert!(areas.iter().any(|a| a.contains("injection")));
   118→    /// ```
   119→    pub fn focus_areas(&self) -> Vec<&'static str> {
   120→        match self {
   121→            Self::SecuritySentinel => vec![
   122→                "SQL injection vulnerabilities",
   123→                "Cross-site scripting (XSS)",
   124→                "Authentication bypass risks",
   125→                "Secrets exposure in code or logs",
   126→                "Input validation gaps",
   127→                "Command injection vectors",
   128→                "Path traversal vulnerabilities",
   129→                "Insecure deserialization",
   130→            ],
   131→            Self::PerformanceOracle => vec![
   132→                "N+1 query patterns",
   133→                "Missing database indexes",
   134→                "Memory leaks and unbounded growth",
   135→                "Algorithmic complexity issues",
   136→                "Unnecessary allocations",
   137→                "Blocking operations in async code",
   138→                "Cache misuse or missing caching",
   139→                "Inefficient data structures",
   140→            ],
   141→            Self::ArchitectureStrategist => vec![
   142→                "SOLID principle violations",
   143→                "Excessive coupling between modules",
   144→                "Layering violations",
   145→                "Separation of concerns issues",
   146→                "Circular dependencies",
   147→                "Inconsistent abstraction levels",
   148→                "Missing or weak interfaces",
   149→                "God objects or functions",
   150→            ],
   151→            Self::SimplicityReviewer => vec![
   152→                "Over-engineering patterns",
   153→                "Premature abstraction",
   154→                "YAGNI violations",
   155→                "Unnecessary complexity",
   156→                "Dead code or unused features",
   157→                "Overly clever solutions",
   158→                "Excessive indirection",
   159→                "Configuration over convention abuse",
   160→            ],
   161→            Self::Custom(_) => vec![],
   162→        }
   163→    }
   164→
   165→    /// Check if this is a built-in specialist type.
   166→    ///
   167→    /// # Examples
   168→    ///
   169→    /// ```
   170→    /// use forge::review::SpecialistType;
   171→    ///
   172→    /// assert!(SpecialistType::SecuritySentinel.is_builtin());
   173→    /// assert!(!SpecialistType::Custom("Test".to_string()).is_builtin());
   174→    /// ```
   175→    pub fn is_builtin(&self) -> bool {
   176→        !matches!(self, Self::Custom(_))
   177→    }
   178→
   179→    /// Get all built-in specialist types.
   180→    ///
   181→    /// # Examples
   182→    ///
   183→    /// ```
   184→    /// use forge::review::SpecialistType;
   185→    ///
   186→    /// let builtins = SpecialistType::all_builtins();
   187→    /// assert_eq!(builtins.len(), 4);
   188→    /// ```
   189→    pub fn all_builtins() -> Vec<Self> {
   190→        vec![
   191→            Self::SecuritySentinel,
   192→            Self::PerformanceOracle,
   193→            Self::ArchitectureStrategist,
   194→            Self::SimplicityReviewer,
   195→        ]
   196→    }
   197→}
   198→
   199→impl std::fmt::Display for SpecialistType {
   200→    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
   201→        write!(f, "{}", self.display_name())
   202→    }
   203→}
   204→
   205→/// Custom `Deserialize` for `SpecialistType`.
   206→///
   207→/// Supports three formats:
   208→/// 1. Short-form string alias: `"security"`, `"perf"`, `"architecture"`, `"simplicity"`, etc.
   209→/// 2. Long-form snake_case string: `"security_sentinel"`, `"performance_oracle"`, etc.
   210→/// 3. Tagged object for custom variants: `{"custom": "my-review"}`
   211→///
   212→/// All string forms are routed through `FromStr`, which handles all known aliases and falls
   213→/// back to `Custom(...)` for unrecognized values. The tagged object form is handled by an
   214→/// internal visitor that mirrors the `#[serde(rename_all = "snake_case")]` enum layout.
   215→impl<'de> serde::Deserialize<'de> for SpecialistType {
   216→    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
   217→        use serde::de::{self, Visitor};
   218→
   219→        struct SpecialistTypeVisitor;
   220→
   221→        impl<'de> Visitor<'de> for SpecialistTypeVisitor {
   222→            type Value = SpecialistType;
   223→
   224→            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
   225→                formatter.write_str(
   226→                    r#"a specialist type string (e.g. "security", "security_sentinel") or a tagged object (e.g. {"custom": "my-review"})"#,
   227→                )
   228→            }
   229→
   230→            /// Handle plain string values via `FromStr` — supports all aliases.
   231→            fn visit_str<E: de::Error>(self, value: &str) -> Result<SpecialistType, E> {
   232→                SpecialistType::from_str(value).map_err(de::Error::custom)
   233→            }
   234→
   235→            /// Handle map values — only `{"custom": "<name>"}` is valid.
   236→            fn visit_map<A: de::MapAccess<'de>>(
   237→                self,
   238→                mut map: A,
   239→            ) -> Result<SpecialistType, A::Error> {
   240→                let key: String = map
   241→                    .next_key()?
   242→                    .ok_or_else(|| de::Error::custom("expected a key in specialist type object"))?;
   243→
   244→                if key == "custom" {
   245→                    let value: String = map.next_value()?;
   246→                    // Drain any remaining keys (there should be none).
   247→                    while map.next_key::<serde::de::IgnoredAny>()?.is_some() {
   248→                        map.next_value::<serde::de::IgnoredAny>()?;
   249→                    }
   250→                    Ok(SpecialistType::Custom(value))
   251→                } else {
   252→                    Err(de::Error::unknown_variant(
   253→                        &key,
   254→                        &[
   255→                            "security_sentinel",
   256→                            "performance_oracle",
   257→                            "architecture_strategist",
   258→                            "simplicity_reviewer",
   259→                            "custom",
   260→                        ],
   261→                    ))
   262→                }
   263→            }
   264→        }
   265→
   266→        deserializer.deserialize_any(SpecialistTypeVisitor)
   267→    }
   268→}
   269→
   270→impl FromStr for SpecialistType {
   271→    type Err = std::convert::Infallible;
   272→
   273→    /// Parse a specialist type from a string identifier.
   274→    ///
   275→    /// Recognizes common aliases and falls back to Custom for unknown values.
   276→    /// This implementation never fails - unknown strings become Custom variants.
   277→    ///
   278→    /// # Examples
   279→    ///
   280→    /// ```
   281→    /// use forge::review::SpecialistType;
   282→    /// use std::str::FromStr;
   283→    ///
   284→    /// assert_eq!(SpecialistType::from_str("security").unwrap(), SpecialistType::SecuritySentinel);
   285→    /// assert_eq!(SpecialistType::from_str("perf").unwrap(), SpecialistType::PerformanceOracle);
   286→    /// assert_eq!(SpecialistType::from_str("unknown").unwrap(), SpecialistType::Custom("unknown".to_string()));
   287→    /// ```
   288→    fn from_str(s: &str) -> Result<Self, Self::Err> {
   289→        Ok(match s.to_lowercase().as_str() {
   290→            "security" | "security-sentinel" | "security_sentinel" => Self::SecuritySentinel,
   291→            "performance" | "perf" | "performance-oracle" | "performance_oracle" => {
   292→                Self::PerformanceOracle
   293→            }
   294→            "architecture" | "arch" | "architecture-strategist" | "architecture_strategist" => {
   295→                Self::ArchitectureStrategist
   296→            }
   297→            "simplicity" | "simple" | "simplicity-reviewer" | "simplicity_reviewer" => {
   298→                Self::SimplicityReviewer
   299→            }
   300→            _ => Self::Custom(s.to_string()),
   301→        })
   302→    }
   303→}
   304→
   305→/// Configuration for a review specialist.
   306→///
   307→/// Combines a specialist type with gating behavior and optional custom focus areas.
   308→#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
   309→pub struct ReviewSpecialist {
   310→    /// Type of specialist.
   311→    pub specialist_type: SpecialistType,
   312→    /// Whether this review gates phase completion.
   313→    /// If true, failures must be resolved before proceeding.
   314→    #[serde(default)]
   315→    pub gate: bool,
   316→    /// Custom focus areas (overrides defaults if non-empty).
   317→    #[serde(default)]
   318→    pub custom_focus_areas: Vec<String>,
   319→}
   320→
   321→impl ReviewSpecialist {
   322→    /// Create a new review specialist configuration.
   323→    ///
   324→    /// # Arguments
   325→    ///
   326→    /// * `specialist_type` - The type of specialist
   327→    /// * `gate` - Whether failures should block phase completion
   328→    ///
   329→    /// # Examples
   330→    ///
   331→    /// ```
   332→    /// use forge::review::{ReviewSpecialist, SpecialistType};
   333→    ///
   334→    /// let gating = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   335→    /// assert!(gating.gate);
   336→    ///
   337→    /// let advisory = ReviewSpecialist::new(SpecialistType::PerformanceOracle, false);
   338→    /// assert!(!advisory.gate);
   339→    /// ```
   340→    pub fn new(specialist_type: SpecialistType, gate: bool) -> Self {
   341→        Self {
   342→            specialist_type,
   343→            gate,
   344→            custom_focus_areas: Vec::new(),
   345→        }
   346→    }
   347→
   348→    /// Create a gating review specialist.
   349→    ///
   350→    /// Convenience method for creating specialists that block on failures.
   351→    pub fn gating(specialist_type: SpecialistType) -> Self {
   352→        Self::new(specialist_type, true)
   353→    }
   354→
   355→    /// Create a non-gating (advisory) review specialist.
   356→    ///
   357→    /// Convenience method for creating specialists that only warn.
   358→    pub fn advisory(specialist_type: SpecialistType) -> Self {
   359→        Self::new(specialist_type, false)
   360→    }
   361→
   362→    /// Add custom focus areas to this specialist.
   363→    ///
   364→    /// Custom focus areas replace the default ones when non-empty.
   365→    ///
   366→    /// # Examples
   367→    ///
   368→    /// ```
   369→    /// use forge::review::{ReviewSpecialist, SpecialistType};
   370→    ///
   371→    /// let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true)
   372→    ///     .with_focus_areas(vec!["API key exposure".to_string()]);
   373→    ///
   374→    /// let areas = specialist.focus_areas();
   375→    /// assert_eq!(areas.len(), 1);
   376→    /// assert_eq!(areas[0], "API key exposure");
   377→    /// ```
   378→    pub fn with_focus_areas(mut self, areas: Vec<String>) -> Self {
   379→        self.custom_focus_areas = areas;
   380→        self
   381→    }
   382→
   383→    /// Get the display name for this specialist.
   384→    pub fn display_name(&self) -> &str {
   385→        self.specialist_type.display_name()
   386→    }
   387→
   388→    /// Get the agent name for this specialist.
   389→    pub fn agent_name(&self) -> String {
   390→        self.specialist_type.agent_name()
   391→    }
   392→
   393→    /// Get the focus areas for this specialist.
   394→    ///
   395→    /// Returns custom focus areas if set, otherwise returns default focus areas
   396→    /// for the specialist type.
   397→    ///
   398→    /// # Examples
   399→    ///
   400→    /// ```
   401→    /// use forge::review::{ReviewSpecialist, SpecialistType};
   402→    ///
   403→    /// // Default focus areas
   404→    /// let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   405→    /// let areas = specialist.focus_areas();
   406→    /// assert!(areas.iter().any(|a| a.contains("injection")));
   407→    ///
   408→    /// // Custom focus areas override defaults
   409→    /// let custom = specialist.with_focus_areas(vec!["Custom area".to_string()]);
   410→    /// assert_eq!(custom.focus_areas(), vec!["Custom area"]);
   411→    /// ```
   412→    pub fn focus_areas(&self) -> Vec<&str> {
   413→        if self.custom_focus_areas.is_empty() {
   414→            self.specialist_type.focus_areas()
   415→        } else {
   416→            self.custom_focus_areas.iter().map(|s| s.as_str()).collect()
   417→        }
   418→    }
   419→
   420→    /// Check if this specialist gates phase completion.
   421→    pub fn is_gating(&self) -> bool {
   422→        self.gate
   423→    }
   424→
   425→    /// Check if this is a built-in specialist type.
   426→    pub fn is_builtin(&self) -> bool {
   427→        self.specialist_type.is_builtin()
   428→    }
   429→
   430→    /// Create all built-in specialists configured as gating.
   431→    ///
   432→    /// Used by sensitive phase detection to enable full review coverage.
   433→    pub fn all_builtin_as_gating() -> Vec<Self> {
   434→        SpecialistType::all_builtins()
   435→            .into_iter()
   436→            .map(Self::gating)
   437→            .collect()
   438→    }
   439→}
   440→
   441→impl Default for ReviewSpecialist {
   442→    fn default() -> Self {
   443→        Self::gating(SpecialistType::SecuritySentinel)
   444→    }
   445→}
   446→
   447→impl std::fmt::Display for ReviewSpecialist {
   448→    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
   449→        if self.gate {
   450→            write!(f, "{} (gating)", self.specialist_type)
   451→        } else {
   452→            write!(f, "{} (advisory)", self.specialist_type)
   453→        }
   454→    }
   455→}
   456→
   457→#[cfg(test)]
   458→mod tests {
   459→    use super::*;
   460→
   461→    // =========================================
   462→    // SpecialistType tests
   463→    // =========================================
   464→
   465→    #[test]
   466→    fn test_specialist_type_display_name() {
   467→        assert_eq!(
   468→            SpecialistType::SecuritySentinel.display_name(),
   469→            "Security Sentinel"
   470→        );
   471→        assert_eq!(
   472→            SpecialistType::PerformanceOracle.display_name(),
   473→            "Performance Oracle"
   474→        );
   475→        assert_eq!(
   476→            SpecialistType::ArchitectureStrategist.display_name(),
   477→            "Architecture Strategist"
   478→        );
   479→        assert_eq!(
   480→            SpecialistType::SimplicityReviewer.display_name(),
   481→            "Simplicity Reviewer"
   482→        );
   483→        assert_eq!(
   484→            SpecialistType::Custom("My Review".to_string()).display_name(),
   485→            "My Review"
   486→        );
   487→    }
   488→
   489→    #[test]
   490→    fn test_specialist_type_agent_name() {
   491→        assert_eq!(
   492→            SpecialistType::SecuritySentinel.agent_name(),
   493→            "security-sentinel"
   494→        );
   495→        assert_eq!(
   496→            SpecialistType::PerformanceOracle.agent_name(),
   497→            "performance-oracle"
   498→        );
   499→        assert_eq!(
   500→            SpecialistType::ArchitectureStrategist.agent_name(),
   501→            "architecture-strategist"
   502→        );
   503→        assert_eq!(
   504→            SpecialistType::SimplicityReviewer.agent_name(),
   505→            "simplicity-reviewer"
   506→        );
   507→        assert_eq!(
   508→            SpecialistType::Custom("Code Quality".to_string()).agent_name(),
   509→            "code-quality"
   510→        );
   511→    }
   512→
   513→    #[test]
   514→    fn test_specialist_type_focus_areas_security() {
   515→        let areas = SpecialistType::SecuritySentinel.focus_areas();
   516→        assert!(!areas.is_empty());
   517→        assert!(areas.iter().any(|a| a.contains("injection")));
   518→        assert!(areas.iter().any(|a| a.contains("XSS")));
   519→    }
   520→
   521→    #[test]
   522→    fn test_specialist_type_focus_areas_performance() {
   523→        let areas = SpecialistType::PerformanceOracle.focus_areas();
   524→        assert!(!areas.is_empty());
   525→        assert!(areas.iter().any(|a| a.contains("N+1")));
   526→        assert!(areas.iter().any(|a| a.contains("index")));
   527→    }
   528→
   529→    #[test]
   530→    fn test_specialist_type_focus_areas_architecture() {
   531→        let areas = SpecialistType::ArchitectureStrategist.focus_areas();
   532→        assert!(!areas.is_empty());
   533→        assert!(areas.iter().any(|a| a.contains("SOLID")));
   534→        assert!(areas.iter().any(|a| a.contains("coupling")));
   535→    }
   536→
   537→    #[test]
   538→    fn test_specialist_type_focus_areas_simplicity() {
   539→        let areas = SpecialistType::SimplicityReviewer.focus_areas();
   540→        assert!(!areas.is_empty());
   541→        assert!(
   542→            areas
   543→                .iter()
   544→                .any(|a| a.to_lowercase().contains("over-engineering"))
   545→        );
   546→        assert!(areas.iter().any(|a| a.contains("YAGNI")));
   547→    }
   548→
   549→    #[test]
   550→    fn test_specialist_type_focus_areas_custom_empty() {
   551→        let areas = SpecialistType::Custom("Test".to_string()).focus_areas();
   552→        assert!(areas.is_empty());
   553→    }
   554→
   555→    #[test]
   556→    fn test_specialist_type_from_str() {
   557→        assert_eq!(
   558→            SpecialistType::from_str("security").unwrap(),
   559→            SpecialistType::SecuritySentinel
   560→        );
   561→        assert_eq!(
   562→            SpecialistType::from_str("SECURITY").unwrap(),
   563→            SpecialistType::SecuritySentinel
   564→        );
   565→        assert_eq!(
   566→            SpecialistType::from_str("security-sentinel").unwrap(),
   567→            SpecialistType::SecuritySentinel
   568→        );
   569→        assert_eq!(
   570→            SpecialistType::from_str("performance").unwrap(),
   571→            SpecialistType::PerformanceOracle
   572→        );
   573→        assert_eq!(
   574→            SpecialistType::from_str("perf").unwrap(),
   575→            SpecialistType::PerformanceOracle
   576→        );
   577→        assert_eq!(
   578→            SpecialistType::from_str("architecture").unwrap(),
   579→            SpecialistType::ArchitectureStrategist
   580→        );
   581→        assert_eq!(
   582→            SpecialistType::from_str("arch").unwrap(),
   583→            SpecialistType::ArchitectureStrategist
   584→        );
   585→        assert_eq!(
   586→            SpecialistType::from_str("simplicity").unwrap(),
   587→            SpecialistType::SimplicityReviewer
   588→        );
   589→        assert_eq!(
   590→            SpecialistType::from_str("simple").unwrap(),
   591→            SpecialistType::SimplicityReviewer
   592→        );
   593→        assert_eq!(
   594→            SpecialistType::from_str("unknown").unwrap(),
   595→            SpecialistType::Custom("unknown".to_string())
   596→        );
   597→    }
   598→
   599→    #[test]
   600→    fn test_specialist_type_is_builtin() {
   601→        assert!(SpecialistType::SecuritySentinel.is_builtin());
   602→        assert!(SpecialistType::PerformanceOracle.is_builtin());
   603→        assert!(SpecialistType::ArchitectureStrategist.is_builtin());
   604→        assert!(SpecialistType::SimplicityReviewer.is_builtin());
   605→        assert!(!SpecialistType::Custom("Test".to_string()).is_builtin());
   606→    }
   607→
   608→    #[test]
   609→    fn test_specialist_type_all_builtins() {
   610→        let builtins = SpecialistType::all_builtins();
   611→        assert_eq!(builtins.len(), 4);
   612→        assert!(builtins.contains(&SpecialistType::SecuritySentinel));
   613→        assert!(builtins.contains(&SpecialistType::PerformanceOracle));
   614→        assert!(builtins.contains(&SpecialistType::ArchitectureStrategist));
   615→        assert!(builtins.contains(&SpecialistType::SimplicityReviewer));
   616→    }
   617→
   618→    #[test]
   619→    fn test_specialist_type_serialization() {
   620→        let json = serde_json::to_string(&SpecialistType::SecuritySentinel).unwrap();
   621→        assert_eq!(json, "\"security_sentinel\"");
   622→
   623→        let custom = serde_json::to_string(&SpecialistType::Custom("Test".to_string())).unwrap();
   624→        assert_eq!(custom, "{\"custom\":\"Test\"}");
   625→    }
   626→
   627→    #[test]
   628→    fn test_specialist_type_deserialization() {
   629→        // Long-form snake_case strings (original format)
   630→        let security: SpecialistType = serde_json::from_str("\"security_sentinel\"").unwrap();
   631→        assert_eq!(security, SpecialistType::SecuritySentinel);
   632→
   633→        let custom: SpecialistType = serde_json::from_str("{\"custom\":\"Test\"}").unwrap();
   634→        assert_eq!(custom, SpecialistType::Custom("Test".to_string()));
   635→
   636→        // Short-form alias strings (used in phases.json configs)
   637→        let security_short: SpecialistType = serde_json::from_str("\"security\"").unwrap();
   638→        assert_eq!(security_short, SpecialistType::SecuritySentinel);
   639→
   640→        let perf_short: SpecialistType = serde_json::from_str("\"performance\"").unwrap();
   641→        assert_eq!(perf_short, SpecialistType::PerformanceOracle);
   642→
   643→        let arch_short: SpecialistType = serde_json::from_str("\"architecture\"").unwrap();
   644→        assert_eq!(arch_short, SpecialistType::ArchitectureStrategist);
   645→
   646→        let simplicity_short: SpecialistType = serde_json::from_str("\"simplicity\"").unwrap();
   647→        assert_eq!(simplicity_short, SpecialistType::SimplicityReviewer);
   648→
   649→        // Hyphenated strings
   650→        let security_hyphen: SpecialistType =
   651→            serde_json::from_str("\"security-sentinel\"").unwrap();
   652→        assert_eq!(security_hyphen, SpecialistType::SecuritySentinel);
   653→
   654→        // Unknown strings fall back to Custom
   655→        let unknown: SpecialistType = serde_json::from_str("\"my-custom-review\"").unwrap();
   656→        assert_eq!(
   657→            unknown,
   658→            SpecialistType::Custom("my-custom-review".to_string())
   659→        );
   660→    }
   661→
   662→    #[test]
   663→    fn test_specialist_type_deserialization_all_formats() {
   664→        // Verify the three formats described in the requirements:
   665→        // 1. Short-form string: "security" -> SecuritySentinel
   666→        let s1: SpecialistType = serde_json::from_str("\"security\"").unwrap();
   667→        assert_eq!(s1, SpecialistType::SecuritySentinel);
   668→
   669→        // 2. Long-form string: "security_sentinel" -> SecuritySentinel
   670→        let s2: SpecialistType = serde_json::from_str("\"security_sentinel\"").unwrap();
   671→        assert_eq!(s2, SpecialistType::SecuritySentinel);
   672→
   673→        // 3. Tagged object: {"custom": "my-review"} -> Custom("my-review")
   674→        let s3: SpecialistType = serde_json::from_str("{\"custom\":\"my-review\"}").unwrap();
   675→        assert_eq!(s3, SpecialistType::Custom("my-review".to_string()));
   676→    }
   677→
   678→    #[test]
   679→    fn test_specialist_type_display() {
   680→        assert_eq!(
   681→            format!("{}", SpecialistType::SecuritySentinel),
   682→            "Security Sentinel"
   683→        );
   684→        assert_eq!(
   685→            format!("{}", SpecialistType::Custom("My Type".to_string())),
   686→            "My Type"
   687→        );
   688→    }
   689→
   690→    #[test]
   691→    fn test_specialist_type_default() {
   692→        let default = SpecialistType::default();
   693→        assert_eq!(default, SpecialistType::SecuritySentinel);
   694→    }
   695→
   696→    // =========================================
   697→    // ReviewSpecialist tests
   698→    // =========================================
   699→
   700→    #[test]
   701→    fn test_review_specialist_new() {
   702→        let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   703→        assert_eq!(specialist.specialist_type, SpecialistType::SecuritySentinel);
   704→        assert!(specialist.gate);
   705→        assert!(specialist.custom_focus_areas.is_empty());
   706→    }
   707→
   708→    #[test]
   709→    fn test_review_specialist_gating() {
   710→        let specialist = ReviewSpecialist::gating(SpecialistType::PerformanceOracle);
   711→        assert!(specialist.gate);
   712→        assert!(specialist.is_gating());
   713→    }
   714→
   715→    #[test]
   716→    fn test_review_specialist_advisory() {
   717→        let specialist = ReviewSpecialist::advisory(SpecialistType::ArchitectureStrategist);
   718→        assert!(!specialist.gate);
   719→        assert!(!specialist.is_gating());
   720→    }
   721→
   722→    #[test]
   723→    fn test_review_specialist_with_focus_areas() {
   724→        let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true)
   725→            .with_focus_areas(vec![
   726→                "Custom area 1".to_string(),
   727→                "Custom area 2".to_string(),
   728→            ]);
   729→
   730→        let areas = specialist.focus_areas();
   731→        assert_eq!(areas.len(), 2);
   732→        assert_eq!(areas[0], "Custom area 1");
   733→        assert_eq!(areas[1], "Custom area 2");
   734→    }
   735→
   736→    #[test]
   737→    fn test_review_specialist_default_focus_areas() {
   738→        let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   739→        let areas = specialist.focus_areas();
   740→        assert!(!areas.is_empty());
   741→        assert!(areas.iter().any(|a| a.contains("injection")));
   742→    }
   743→
   744→    #[test]
   745→    fn test_review_specialist_display_name() {
   746→        let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   747→        assert_eq!(specialist.display_name(), "Security Sentinel");
   748→    }
   749→
   750→    #[test]
   751→    fn test_review_specialist_agent_name() {
   752→        let specialist = ReviewSpecialist::new(SpecialistType::PerformanceOracle, false);
   753→        assert_eq!(specialist.agent_name(), "performance-oracle");
   754→    }
   755→
   756→    #[test]
   757→    fn test_review_specialist_is_builtin() {
   758→        let builtin = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true);
   759→        assert!(builtin.is_builtin());
   760→
   761→        let custom = ReviewSpecialist::new(SpecialistType::Custom("Test".to_string()), false);
   762→        assert!(!custom.is_builtin());
   763→    }
   764→
   765→    #[test]
   766→    fn test_review_specialist_display() {
   767→        let gating = ReviewSpecialist::gating(SpecialistType::SecuritySentinel);
   768→        assert_eq!(format!("{}", gating), "Security Sentinel (gating)");
   769→
   770→        let advisory = ReviewSpecialist::advisory(SpecialistType::PerformanceOracle);
   771→        assert_eq!(format!("{}", advisory), "Performance Oracle (advisory)");
   772→    }
   773→
   774→    #[test]
   775→    fn test_review_specialist_default() {
   776→        let default = ReviewSpecialist::default();
   777→        assert_eq!(default.specialist_type, SpecialistType::SecuritySentinel);
   778→        assert!(default.gate);
   779→    }
   780→
   781→    #[test]
   782→    fn test_review_specialist_serialization() {
   783→        let specialist = ReviewSpecialist::new(SpecialistType::SecuritySentinel, true)
   784→            .with_focus_areas(vec!["Test area".to_string()]);
   785→
   786→        let json = serde_json::to_string(&specialist).unwrap();
   787→        let parsed: ReviewSpecialist = serde_json::from_str(&json).unwrap();
   788→
   789→        assert_eq!(specialist.specialist_type, parsed.specialist_type);
   790→        assert_eq!(specialist.gate, parsed.gate);
   791→        assert_eq!(specialist.custom_focus_areas, parsed.custom_focus_areas);
   792→    }
   793→
   794→    #[test]
   795→    fn test_review_specialist_deserialization_minimal() {
   796→        let json = r#"{"specialist_type":"performance_oracle"}"#;
   797→        let specialist: ReviewSpecialist = serde_json::from_str(json).unwrap();
   798→
   799→        assert_eq!(
   800→            specialist.specialist_type,
   801→            SpecialistType::PerformanceOracle
   802→        );
   803→        assert!(!specialist.gate); // defaults to false
   804→        assert!(specialist.custom_focus_areas.is_empty());
   805→    }
   806→
   807→    #[test]
   808→    fn test_all_builtin_as_gating() {
   809→        let specialists = ReviewSpecialist::all_builtin_as_gating();
   810→        assert_eq!(specialists.len(), 4);
   811→        for specialist in &specialists {
   812→            assert!(specialist.is_gating());
   813→            assert!(specialist.is_builtin());
   814→        }
   815→    }
   816→}
   817→
```

> TOOL

tool_use Read
id: toolu_01Arukn5V6YcvyuDj4xo2Sfn
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs"
}
```

> TOOL

tool_result
id: toolu_01Arukn5V6YcvyuDj4xo2Sfn
```
<persisted-output>
Output too large (88.9KB). Full output saved to: /Users/jdsingh/.claude/projects/-Users-jdsingh-Projects-AI-forge/def6a66a-af8f-4f33-8f83-80cddd0da7f5/tool-results/REDACTED.txt

Preview (first 2KB):
     1→use std::collections::HashMap;
     2→use std::str::FromStr;
     3→use std::sync::{Arc, Mutex, OnceLock};
     4→
     5→use crate::errors::FactoryError;
     6→
     7→use axum::{
     8→    Json, Router,
     9→    extract::{Path, Query, State},
    10→    http::StatusCode,
    11→    response::{IntoResponse, Response},
    12→    routing::{get, patch, post},
    13→};
    14→use serde::Deserialize;
    15→use tokio::sync::broadcast;
    16→
    17→use super::db::DbHandle;
    18→#[cfg(test)]
    19→use super::db::FactoryDb;
    20→use super::models::IssueColumn;
    21→use super::pipeline::PipelineRunner;
    22→use super::ws::{WsMessage, broadcast_message};
    23→use crate::metrics::MetricsCollector;
    24→
    25→// ── Shared application state ──────────────────────────────────────────
    26→
    27→pub struct AppState {
    28→    pub db: DbHandle,
    29→    pub ws_tx: broadcast::Sender<String>,
    30→    pub pipeline_runner: PipelineRunner,
    31→    pub github_client_id: Option<String>,
    32→    pub github_token: Mutex<Option<String>>,
    33→    pub metrics: MetricsCollector,
    34→}
    35→
    36→pub type SharedState = Arc<AppState>;
    37→
    38→// ── Request payload types ─────────────────────────────────────────────
    39→
    40→#[derive(Deserialize)]
    41→pub struct CreateProjectRequest {
    42→    pub name: String,
    43→    pub path: String,
    44→}
    45→
    46→#[derive(Deserialize)]
    47→pub struct CloneProjectRequest {
    48→    pub repo_url: String,
    49→}
    50→
    51→#[derive(Deserialize)]
    52→pub struct CreateIssueRequest {
    53→    pub title: String,
    54→    pub description: Option<String>,
    55→    pub column: Option<String>,
    56→}
    57→
    58→#[derive(Deserialize)]
    59→pub struct UpdateIssueRequest {
    60→    pub title: Option<String>,
    61→    pub description: Option<String>,
    62→    pub priority: Option<String>,
    63→    pub labels: Option<String>,
    64→}
    65→
...
</persisted-output>
```

> TOOL

tool_use Read
id: toolu_017GpXbcsuXkXBe9dCPxMN6i
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/StatusBar.tsx"
}
```

> TOOL

tool_result
id: toolu_017GpXbcsuXkXBe9dCPxMN6i
```
     1→/** Top status bar — system stats, command input, view toggle, uptime, WebSocket indicator. */
     2→import { useState, useEffect } from 'react';
     3→import { useWsStatus } from '../contexts/WebSocketContext';
     4→import type { ViewMode } from '../types';
     5→import CommandAutocomplete from './CommandAutocomplete';
     6→
     7→/** Props for the StatusBar component */
     8→export interface StatusBarProps {
     9→  /** Counts of agent runs by status */
    10→  agentCounts: {
    11→    running: number;
    12→    queued: number;
    13→    completed: number;
    14→    failed: number;
    15→  };
    16→  /** Total number of projects loaded */
    17→  projectCount: number;
    18→  /** Callback when user submits a command via the input */
    19→  onCommand?: (command: string) => void;
    20→  /** Current view mode for the grid */
    21→  viewMode: ViewMode;
    22→  /** Callback when user toggles the view mode */
    23→  onViewModeChange: (mode: ViewMode) => void;
    24→}
    25→
    26→/** Format seconds into HH:MM:SS */
    27→function formatUptime(seconds: number): string {
    28→  const h = Math.floor(seconds / 3600);
    29→  const m = Math.floor((seconds % 3600) / 60);
    30→  const s = seconds % 60;
    31→  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    32→}
    33→
    34→/** Status bar displayed at the top of the Mission Control dashboard. */
    35→export default function StatusBar({
    36→  agentCounts,
    37→  projectCount,
    38→  onCommand,
    39→  viewMode,
    40→  onViewModeChange,
    41→}: StatusBarProps) {
    42→  const wsStatus = useWsStatus();
    43→  const [uptime, setUptime] = useState(0);
    44→
    45→  // Uptime counter
    46→  useEffect(() => {
    47→    const interval = setInterval(() => setUptime(u => u + 1), 1000);
    48→    return () => clearInterval(interval);
    49→  }, []);
    50→
    51→  const wsColor = wsStatus === 'connected'
    52→    ? 'var(--color-success)'
    53→    : wsStatus === 'connecting'
    54→      ? 'var(--color-warning)'
    55→      : 'var(--color-error)';
    56→
    57→  return (
    58→    <div style={{
    59→      display: 'flex',
    60→      alignItems: 'center',
    61→      height: '40px',
    62→      padding: '0 12px',
    63→      backgroundColor: 'var(--color-bg-card)',
    64→      borderBottom: '1px solid var(--color-border)',
    65→      gap: '16px',
    66→      fontSize: '13px',
    67→      flexShrink: 0,
    68→    }}>
    69→      {/* Logo */}
    70→      <span style={{ color: 'var(--color-success)', fontWeight: 700, letterSpacing: '2px' }}>
    71→        FORGE
    72→      </span>
    73→
    74→      {/* System stats */}
    75→      <div style={{ display: 'flex', gap: '12px', color: 'var(--color-text-secondary)' }}>
    76→        <span>
    77→          <span style={{ color: 'var(--color-success)' }}>{agentCounts.running}</span> running
    78→        </span>
    79→        <span>
    80→          <span style={{ color: 'var(--color-warning)' }}>{agentCounts.queued}</span> queued
    81→        </span>
    82→        <span>
    83→          <span style={{ color: 'var(--color-success)' }}>{agentCounts.completed}</span> done
    84→        </span>
    85→        <span>
    86→          <span style={{ color: 'var(--color-error)' }}>{agentCounts.failed}</span> failed
    87→        </span>
    88→        <span>{projectCount} projects</span>
    89→      </div>
    90→
    91→      {/* Command input */}
    92→      <div style={{
    93→        flex: 1,
    94→        display: 'flex',
    95→        alignItems: 'center',
    96→        maxWidth: '500px',
    97→        margin: '0 auto',
    98→      }}>
    99→        <span style={{ color: 'var(--color-accent)', marginRight: '8px' }}>forge&gt;</span>
   100→        <CommandAutocomplete onCommand={onCommand} />
   101→      </div>
   102→
   103→      {/* View toggle */}
   104→      <div style={{ display: 'flex', gap: '4px' }}>
   105→        <button
   106→          onClick={() => onViewModeChange('grid')}
   107→          style={{
   108→            padding: '4px 8px',
   109→            background: viewMode === 'grid' ? 'var(--color-border)' : 'transparent',
   110→            border: '1px solid var(--color-border)',
   111→            color: 'var(--color-text-primary)',
   112→            cursor: 'pointer',
   113→            fontSize: '12px',
   114→          }}
   115→          title="Grid view"
   116→        >
   117→          grid
   118→        </button>
   119→        <button
   120→          onClick={() => onViewModeChange('list')}
   121→          style={{
   122→            padding: '4px 8px',
   123→            background: viewMode === 'list' ? 'var(--color-border)' : 'transparent',
   124→            border: '1px solid var(--color-border)',
   125→            color: 'var(--color-text-primary)',
   126→            cursor: 'pointer',
   127→            fontSize: '12px',
   128→          }}
   129→          title="List view"
   130→        >
   131→          list
   132→        </button>
   133→        <button
   134→          onClick={() => onViewModeChange('analytics')}
   135→          style={{
   136→            padding: '4px 8px',
   137→            background: viewMode === 'analytics' ? 'var(--color-border)' : 'transparent',
   138→            border: '1px solid var(--color-border)',
   139→            color: 'var(--color-text-primary)',
   140→            cursor: 'pointer',
   141→            fontSize: '12px',
   142→          }}
   143→          title="Analytics view"
   144→        >
   145→          analytics
   146→        </button>
   147→      </div>
   148→
   149→      {/* Uptime + WS status */}
   150→      <span style={{ color: 'var(--color-text-secondary)' }}>
   151→        {formatUptime(uptime)}
   152→      </span>
   153→      <span
   154→        style={{
   155→          width: '8px',
   156→          height: '8px',
   157→          borderRadius: '50%',
   158→          backgroundColor: wsColor,
   159→        }}
   160→        title={`WebSocket: ${wsStatus}`}
   161→      />
   162→    </div>
   163→  );
   164→}
   165→
```

> TOOL

tool_use Read
id: toolu_01M4A9vvoiJKQ5LPWc2hTSAB
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts"
}
```

> TOOL

tool_result
id: toolu_01M4A9vvoiJKQ5LPWc2hTSAB
```
     1→export interface Project {
     2→  id: number;
     3→  name: string;
     4→  path: string;
     5→  github_repo: string | null;
     6→  created_at: string;
     7→}
     8→
     9→export type IssueColumn = 'backlog' | 'ready' | 'in_progress' | 'in_review' | 'done';
    10→export type Priority = 'low' | 'medium' | 'high' | 'critical';
    11→export type PipelineStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
    12→export type AgentTaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
    13→export type AgentRole = 'planner' | 'coder' | 'tester' | 'reviewer' | 'browser_verifier' | 'test_verifier';
    14→export type AgentEventType = 'thinking' | 'action' | 'output' | 'signal' | 'error';
    15→export type ExecutionStrategy = 'parallel' | 'sequential' | 'wave_pipeline' | 'adaptive';
    16→export type IsolationStrategy = 'worktree' | 'container' | 'hybrid' | 'shared';
    17→export type SignalType = 'progress' | 'blocker' | 'pivot';
    18→export type VerificationType = 'browser' | 'test_build';
    19→
    20→export interface Issue {
    21→  id: number;
    22→  project_id: number;
    23→  title: string;
    24→  description: string;
    25→  column: IssueColumn;
    26→  position: number;
    27→  priority: Priority;
    28→  labels: string[];
    29→  github_issue_number: number | null;
    30→  created_at: string;
    31→  updated_at: string;
    32→}
    33→
    34→export interface PipelineRun {
    35→  id: number;
    36→  issue_id: number;
    37→  status: PipelineStatus;
    38→  phase_count: number | null;
    39→  current_phase: number | null;
    40→  iteration: number | null;
    41→  summary: string | null;
    42→  error: string | null;
    43→  branch_name: string | null;
    44→  pr_url: string | null;
    45→  team_id: number | null;
    46→  has_team: boolean;
    47→  started_at: string;
    48→  completed_at: string | null;
    49→}
    50→
    51→export interface BoardView {
    52→  project: Project;
    53→  columns: ColumnView[];
    54→}
    55→
    56→export interface ColumnView {
    57→  name: IssueColumn;
    58→  issues: IssueWithStatus[];
    59→}
    60→
    61→export interface IssueWithStatus {
    62→  issue: Issue;
    63→  active_run: PipelineRun | null;
    64→}
    65→
    66→export interface PipelinePhase {
    67→  id: number;
    68→  run_id: number;
    69→  phase_number: string;
    70→  phase_name: string;
    71→  status: string;
    72→  iteration: number | null;
    73→  budget: number | null;
    74→  started_at: string | null;
    75→  completed_at: string | null;
    76→  error: string | null;
    77→  review_status?: 'pending' | 'reviewing' | 'passed' | 'failed';
    78→  review_findings?: number;
    79→}
    80→
    81→export interface PipelineRunDetail extends PipelineRun {
    82→  phases: PipelinePhase[];
    83→}
    84→
    85→export interface IssueDetail {
    86→  issue: Issue;
    87→  runs: PipelineRunDetail[];
    88→}
    89→
    90→export interface AgentTeam {
    91→  id: number;
    92→  run_id: number;
    93→  strategy: ExecutionStrategy;
    94→  isolation: IsolationStrategy;
    95→  plan_summary: string;
    96→  created_at: string;
    97→}
    98→
    99→export interface AgentTask {
   100→  id: number;
   101→  team_id: number;
   102→  name: string;
   103→  description: string;
   104→  agent_role: AgentRole;
   105→  wave: number;
   106→  depends_on: number[];
   107→  status: AgentTaskStatus;
   108→  isolation_type: IsolationStrategy;
   109→  worktree_path: string | null;
   110→  container_id: string | null;
   111→  branch_name: string | null;
   112→  started_at: string | null;
   113→  completed_at: string | null;
   114→  error: string | null;
   115→}
   116→
   117→export interface AgentEvent {
   118→  id: number;
   119→  task_id: number;
   120→  event_type: AgentEventType;
   121→  content: string;
   122→  metadata: Record<string, unknown> | null;
   123→  created_at: string;
   124→}
   125→
   126→export interface AgentTeamDetail {
   127→  team: AgentTeam;
   128→  tasks: AgentTask[];
   129→}
   130→
   131→export type PipelineContentType = 'text' | 'tool_start' | 'tool_end' | 'thinking';
   132→export type FileAction = 'created' | 'modified' | 'deleted';
   133→
   134→export interface PipelineOutputEvent {
   135→  run_id: number;
   136→  content_type: PipelineContentType;
   137→  content: string;
   138→  tool_id: string | null;
   139→  input_summary: string | null;
   140→}
   141→
   142→export interface PipelineFileChange {
   143→  run_id: number;
   144→  file_path: string;
   145→  action: FileAction;
   146→}
   147→
   148→export type WsMessage =
   149→  | { type: 'IssueCreated'; data: { issue: Issue } }
   150→  | { type: 'IssueUpdated'; data: { issue: Issue } }
   151→  | { type: 'IssueMoved'; data: { issue_id: number; from_column: string; to_column: string; position: number } }
   152→  | { type: 'IssueDeleted'; data: { issue_id: number } }
   153→  | { type: 'PipelineStarted'; data: { run: PipelineRun } }
   154→  | { type: 'PipelineProgress'; data: { run_id: number; phase: number; iteration: number; percent: number | null } }
   155→  | { type: 'PipelineCompleted'; data: { run: PipelineRun } }
   156→  | { type: 'PipelineFailed'; data: { run: PipelineRun } }
   157→  | { type: 'PipelineBranchCreated'; data: { run_id: number; branch_name: string } }
   158→  | { type: 'PipelinePrCreated'; data: { run_id: number; pr_url: string } }
   159→  | { type: 'PipelinePhaseStarted'; data: { run_id: number; phase_number: string; phase_name: string; wave: number } }
   160→  | { type: 'PipelinePhaseCompleted'; data: { run_id: number; phase_number: string; success: boolean } }
   161→  | { type: 'PipelineReviewStarted'; data: { run_id: number; phase_number: string } }
   162→  | { type: 'PipelineReviewCompleted'; data: { run_id: number; phase_number: string; passed: boolean; findings_count: number } }
   163→  | { type: 'TeamCreated'; data: { run_id: number; team_id: number; strategy: ExecutionStrategy; isolation: IsolationStrategy; plan_summary: string; tasks: AgentTask[] } }
   164→  | { type: 'WaveStarted'; data: { run_id: number; team_id: number; wave: number; task_ids: number[] } }
   165→  | { type: 'WaveCompleted'; data: { run_id: number; team_id: number; wave: number; success_count: number; failed_count: number } }
   166→  | { type: 'AgentTaskStarted'; data: { run_id: number; task_id: number; name: string; role: AgentRole; wave: number } }
   167→  | { type: 'AgentTaskCompleted'; data: { run_id: number; task_id: number; success: boolean } }
   168→  | { type: 'AgentTaskFailed'; data: { run_id: number; task_id: number; error: string } }
   169→  | { type: 'AgentThinking'; data: { run_id: number; task_id: number; content: string } }
   170→  | { type: 'AgentAction'; data: { run_id: number; task_id: number; action_type: string; summary: string; metadata: Record<string, unknown> } }
   171→  | { type: 'AgentOutput'; data: { run_id: number; task_id: number; content: string } }
   172→  | { type: 'AgentSignal'; data: { run_id: number; task_id: number; signal_type: SignalType; content: string } }
   173→  | { type: 'MergeStarted'; data: { run_id: number; wave: number } }
   174→  | { type: 'MergeCompleted'; data: { run_id: number; wave: number; conflicts: boolean } }
   175→  | { type: 'MergeConflict'; data: { run_id: number; wave: number; files: string[] } }
   176→  | { type: 'VerificationResult'; data: { run_id: number; task_id: number; verification_type: VerificationType; passed: boolean; summary: string; screenshots: string[]; details: Record<string, unknown> } }
   177→  | { type: 'PipelineOutputEvent'; data: PipelineOutputEvent }
   178→  | { type: 'PipelineFileChanged'; data: PipelineFileChange }
   179→  | { type: 'PipelineOutput'; data: { run_id: number; content: string } }
   180→  | { type: 'PipelineError'; data: { run_id: number; message: string } }
   181→  | { type: 'ProjectCreated'; data: { project: Project } }
   182→  | { type: 'ProjectDeleted'; data: { project_id: number } };
   183→
   184→// GitHub OAuth types
   185→export interface GitHubDeviceCode {
   186→  device_code: string;
   187→  user_code: string;
   188→  verification_uri: string;
   189→  expires_in: number;
   190→  interval: number;
   191→}
   192→
   193→export interface GitHubRepo {
   194→  full_name: string;
   195→  name: string;
   196→  private: boolean;
   197→  html_url: string;
   198→  clone_url: string;
   199→  description: string | null;
   200→  default_branch: string;
   201→}
   202→
   203→export interface GitHubAuthStatus {
   204→  connected: boolean;
   205→  client_id_configured: boolean;
   206→}
   207→
   208→export interface SyncResult {
   209→  imported: number;
   210→  skipped: number;
   211→  total_github: number;
   212→}
   213→
   214→// CLI Help types
   215→export interface CliHelpCommand {
   216→  name: string;
   217→  description: string;
   218→}
   219→
   220→export interface CliHelpOption {
   221→  flag: string;
   222→  description: string;
   223→}
   224→
   225→export interface CliHelpResponse {
   226→  commands: CliHelpCommand[];
   227→  options: CliHelpOption[];
   228→}
   229→
   230→// ── Analytics types ─────────────────────────────────────────────────
   231→
   232→export interface SummaryStats {
   233→  total_runs: number;
   234→  successful_runs: number;
   235→  success_rate: number;
   236→  avg_duration_secs: number;
   237→  total_phases: number;
   238→  avg_iterations_per_phase: number;
   239→}
   240→
   241→export interface PhaseNameStats {
   242→  phase_name: string;
   243→  run_count: number;
   244→  avg_iterations: number;
   245→  avg_duration_secs: number;
   246→  budget_utilization: number;
   247→  success_rate: number;
   248→}
   249→
   250→export interface RunSummary {
   251→  run_id: string;
   252→  issue_id: number | null;
   253→  success: boolean;
   254→  duration_secs: number | null;
   255→  phases_total: number | null;
   256→  started_at: string;
   257→}
   258→
   259→export interface ReviewStats {
   260→  specialist_type: string;
   261→  review_count: number;
   262→  pass_rate: number;
   263→  avg_findings: number;
   264→}
   265→
   266→export interface TokenDailyUsage {
   267→  date: string;
   268→  total_input: number;
   269→  total_output: number;
   270→  iteration_count: number;
   271→}
   272→
   273→// Column display configuration
   274→export const COLUMNS: { key: IssueColumn; label: string }[] = [
   275→  { key: 'backlog', label: 'Backlog' },
   276→  { key: 'ready', label: 'Ready' },
   277→  { key: 'in_progress', label: 'In Progress' },
   278→  { key: 'in_review', label: 'In Review' },
   279→  { key: 'done', label: 'Done' },
   280→];
   281→
   282→export const PRIORITY_COLORS: Record<Priority, string> = {
   283→  low: 'bg-gray-100 text-gray-700',
   284→  medium: 'bg-blue-100 text-blue-700',
   285→  high: 'bg-orange-100 text-orange-700',
   286→  critical: 'bg-red-100 text-red-700',
   287→};
   288→
   289→export const STATUS_COLORS: Record<PipelineStatus, string> = {
   290→  queued: 'text-gray-500',
   291→  running: 'text-blue-500',
   292→  completed: 'text-green-500',
   293→  failed: 'text-red-500',
   294→  cancelled: 'text-gray-400',
   295→};
   296→
   297→// ── Mission Control view types ──────────────────────────────────────
   298→
   299→/** Status filter for the agent run grid. 'all' shows every status. */
   300→export type RunStatusFilter = 'all' | 'running' | 'queued' | 'completed' | 'failed';
   301→
   302→/**
   303→ * An agent run card in the grid — combines issue, pipeline run, and project data
   304→ * into a single presentational unit.
   305→ */
   306→export interface AgentRunCard {
   307→  /** The issue being worked on */
   308→  issue: Issue;
   309→  /** The active or most recent pipeline run */
   310→  run: PipelineRun;
   311→  /** The project this run belongs to */
   312→  project: Project;
   313→}
   314→
   315→/**
   316→ * Event log entry for the bottom panel.
   317→ * Each entry represents a timestamped event from the system.
   318→ */
   319→export interface EventLogEntry {
   320→  /** Unique identifier for deduplication */
   321→  id: string;
   322→  /** ISO 8601 timestamp */
   323→  timestamp: string;
   324→  /** Origin of the event */
   325→  source: 'agent' | 'phase' | 'review' | 'system' | 'error' | 'git';
   326→  /** Human-readable event description */
   327→  message: string;
   328→  /** Name of the project this event relates to */
   329→  projectName?: string;
   330→  /** Pipeline run ID this event relates to */
   331→  runId?: number;
   332→}
   333→
   334→/** View mode for the main agent run grid */
   335→export type ViewMode = 'grid' | 'list' | 'analytics';
   336→
   337→/** Status colors mapped to CSS custom property values for the Mission Control theme */
   338→export const MC_STATUS_COLORS: Record<PipelineStatus, string> = {
   339→  running: 'var(--color-success)',
   340→  queued: 'var(--color-warning)',
   341→  completed: 'var(--color-success)',
   342→  failed: 'var(--color-error)',
   343→  cancelled: 'var(--color-text-secondary)',
   344→};
   345→
```

> AGENT

Now let me read the main App component and the API router to see how views are wired.

> TOOL

tool_use Read
id: toolu_01Bx2QtEVsg7QyyhZB79mWg5
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/App.tsx"
}
```

> TOOL

tool_result
id: toolu_01Bx2QtEVsg7QyyhZB79mWg5
```
     1→import { useState, useCallback, useMemo } from 'react';
     2→import type { ViewMode, Project } from './types';
     3→import useMissionControl from './hooks/useMissionControl';
     4→import { WebSocketProvider } from './contexts/WebSocketContext';
     5→import StatusBar from './components/StatusBar';
     6→import ProjectSidebar from './components/ProjectSidebar';
     7→import AgentRunCard from './components/AgentRunCard';
     8→import EventLog from './components/EventLog';
     9→import FloatingActionButton from './components/FloatingActionButton';
    10→import NewIssueModal from './components/NewIssueModal';
    11→import ConfirmDialog from './components/ConfirmDialog';
    12→import { ProjectSetup } from './components/ProjectSetup';
    13→import Analytics from './components/Analytics';
    14→import { api } from './api/client';
    15→
    16→/**
    17→ * Mission Control dashboard — the main application shell.
    18→ * Aggregates all projects and agent runs into a unified monitoring view.
    19→ * Layout: StatusBar (top) -> flex row [ProjectSidebar | Agent Grid] -> EventLog (bottom).
    20→ */
    21→function MissionControl() {
    22→  const {
    23→    projects,
    24→    agentRunCards,
    25→    idleIssueCards,
    26→    statusCounts,
    27→    eventLog,
    28→    phases,
    29→    agentTeams,
    30→    agentEvents,
    31→    pipelineEvents,
    32→    pipelineOutputEvents,
    33→    pipelineFileChanges,
    34→    loading,
    35→    selectedProjectId,
    36→    setSelectedProjectId,
    37→    triggerPipeline,
    38→    cancelPipeline,
    39→    createIssue,
    40→    createProject,
    41→    cloneProject,
    42→    deleteProject,
    43→    issuesByProject: _issuesByProject,
    44→  } = useMissionControl();
    45→
    46→  const [viewMode, setViewMode] = useState<ViewMode>('grid');
    47→  const [showNewIssueModal, setShowNewIssueModal] = useState(false);
    48→  const [newIssueProjectId, setNewIssueProjectId] = useState<number | null>(null);
    49→  const [showProjectSetup, setShowProjectSetup] = useState(false);
    50→  const [deleteConfirm, setDeleteConfirm] = useState<{ id: number; name: string } | null>(null);
    51→
    52→  /** Compute run counts by project for the sidebar */
    53→  const runsByProject = useMemo(() => {
    54→    const map = new Map<number, { running: number; total: number }>();
    55→    for (const card of agentRunCards) {
    56→      const pid = card.project.id;
    57→      const existing = map.get(pid) ?? { running: 0, total: 0 };
    58→      existing.total++;
    59→      if (card.run.status === 'running') existing.running++;
    60→      map.set(pid, existing);
    61→    }
    62→    return map;
    63→  }, [agentRunCards]);
    64→
    65→  /** Projects filtered by the current sidebar selection */
    66→  const displayedProjects = useMemo(() => {
    67→    if (selectedProjectId === null) return projects;
    68→    return projects.filter(p => p.id === selectedProjectId);
    69→  }, [projects, selectedProjectId]);
    70→
    71→  const handleNewIssue = useCallback(() => {
    72→    setNewIssueProjectId(null);
    73→    setShowNewIssueModal(true);
    74→  }, []);
    75→
    76→  const handleNewProject = useCallback(() => {
    77→    setShowProjectSetup(true);
    78→  }, []);
    79→
    80→  const handleSyncGithub = useCallback(async () => {
    81→    const project = projects.find(p =>
    82→      selectedProjectId === null ? true : p.id === selectedProjectId
    83→    );
    84→    if (project) {
    85→      try {
    86→        await api.syncGithub(project.id);
    87→      } catch (err) {
    88→        console.error('Sync failed:', err);
    89→      }
    90→    }
    91→  }, [projects, selectedProjectId]);
    92→
    93→  const handleIssueSubmit = useCallback(async (projectId: number, title: string, description: string) => {
    94→    const issue = await createIssue(projectId, title, description);
    95→    await triggerPipeline(issue.id);
    96→  }, [createIssue, triggerPipeline]);
    97→
    98→  const handleProjectSelect = useCallback((project: Project) => {
    99→    setSelectedProjectId(project.id);
   100→    setShowProjectSetup(false);
   101→  }, [setSelectedProjectId]);
   102→
   103→  const handleProjectCreate = useCallback((name: string, path: string) => {
   104→    createProject(name, path).then(() => {
   105→      setShowProjectSetup(false);
   106→    }).catch(console.error);
   107→  }, [createProject]);
   108→
   109→  const handleCloneProject = useCallback(async (repoUrl: string) => {
   110→    const project = await cloneProject(repoUrl);
   111→    setShowProjectSetup(false);
   112→    setSelectedProjectId(project.id);
   113→  }, [cloneProject, setSelectedProjectId]);
   114→
   115→  const handleDeleteProject = useCallback(async (projectId: number) => {
   116→    await deleteProject(projectId);
   117→    if (selectedProjectId === projectId) {
   118→      setSelectedProjectId(null);
   119→    }
   120→  }, [deleteProject, selectedProjectId, setSelectedProjectId]);
   121→
   122→  // Loading state
   123→  if (loading) {
   124→    return (
   125→      <div style={{
   126→        display: 'flex',
   127→        alignItems: 'center',
   128→        justifyContent: 'center',
   129→        height: '100vh',
   130→        backgroundColor: 'var(--color-bg-primary)',
   131→        color: 'var(--color-text-primary)',
   132→        gap: '12px',
   133→        fontSize: '14px',
   134→      }}>
   135→        <span className="pulse-dot" style={{
   136→          width: '8px',
   137→          height: '8px',
   138→          borderRadius: '50%',
   139→          backgroundColor: 'var(--color-success)',
   140→        }} />
   141→        Initializing Mission Control...
   142→      </div>
   143→    );
   144→  }
   145→
   146→  // No projects — show ProjectSetup full-screen
   147→  if (projects.length === 0) {
   148→    return (
   149→      <div style={{
   150→        height: '100vh',
   151→        backgroundColor: 'var(--color-bg-primary)',
   152→      }}>
   153→        <ProjectSetup
   154→          projects={[]}
   155→          onSelect={handleProjectSelect}
   156→          onCreate={handleProjectCreate}
   157→          onClone={handleCloneProject}
   158→        />
   159→      </div>
   160→    );
   161→  }
   162→
   163→  return (
   164→    <div style={{
   165→      display: 'flex',
   166→      flexDirection: 'column',
   167→      height: '100vh',
   168→      backgroundColor: 'var(--color-bg-primary)',
   169→      color: 'var(--color-text-primary)',
   170→    }}>
   171→      {/* Top bar */}
   172→      <StatusBar
   173→        agentCounts={{
   174→          running: statusCounts.running,
   175→          queued: statusCounts.queued,
   176→          completed: statusCounts.completed,
   177→          failed: statusCounts.failed,
   178→        }}
   179→        projectCount={projects.length}
   180→        viewMode={viewMode}
   181→        onViewModeChange={setViewMode}
   182→      />
   183→
   184→      {/* Main content: sidebar + agent grid */}
   185→      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
   186→        <ProjectSidebar
   187→          projects={projects}
   188→          selectedProjectId={selectedProjectId}
   189→          onSelectProject={setSelectedProjectId}
   190→          onDeleteProject={(id, name) => setDeleteConfirm({ id, name })}
   191→          runsByProject={runsByProject}
   192→        />
   193→
   194→        {/* Main content area */}
   195→        {viewMode === 'analytics' ? (
   196→          <div style={{ flex: 1, overflow: 'hidden' }}>
   197→            <Analytics />
   198→          </div>
   199→        ) : (
   200→          <div style={{
   201→            flex: 1,
   202→            overflowY: 'auto',
   203→            padding: '16px',
   204→          }}>
   205→            <div style={{
   206→              display: viewMode === 'grid' ? 'grid' : 'flex',
   207→              gridTemplateColumns: viewMode === 'grid' ? 'repeat(auto-fill, minmax(400px, 1fr))' : undefined,
   208→              flexDirection: viewMode === 'list' ? 'column' : undefined,
   209→              gap: '12px',
   210→            }}>
   211→              {/* Active pipeline run cards */}
   212→              {agentRunCards.map(card => (
   213→                <AgentRunCard
   214→                  key={`run-${card.run.id}`}
   215→                  card={card}
   216→                  phases={phases.get(card.run.id)}
   217→                  agentTeam={agentTeams.get(card.run.id)}
   218→                  agentEvents={agentEvents}
   219→                  pipelineEvents={pipelineEvents.get(card.run.id)}
   220→                  pipelineOutputEvents={pipelineOutputEvents.get(card.run.id)}
   221→                  pipelineFileChanges={pipelineFileChanges.get(card.run.id)}
   222→                  onCancel={cancelPipeline}
   223→                  viewMode={viewMode}
   224→                />
   225→              ))}
   226→
   227→              {/* Idle issue cards — issues without active pipeline runs */}
   228→              {idleIssueCards.map(({ issue, project }) => (
   229→                <div
   230→                  key={`idle-${issue.id}`}
   231→                  style={{
   232→                    backgroundColor: 'var(--color-bg-card)',
   233→                    border: '1px solid var(--color-border)',
   234→                    borderLeft: '3px solid var(--color-text-secondary)',
   235→                    transition: 'background-color 0.15s',
   236→                  }}
   237→                  onMouseEnter={e => (e.currentTarget.style.backgroundColor = 'var(--color-bg-card-hover)')}
   238→                  onMouseLeave={e => (e.currentTarget.style.backgroundColor = 'var(--color-bg-card)')}
   239→                >
   240→                  <div style={{
   241→                    display: 'flex',
   242→                    alignItems: 'center',
   243→                    padding: '12px',
   244→                    gap: '12px',
   245→                  }}>
   246→                    {/* Idle dot */}
   247→                    <span style={{
   248→                      width: '8px',
   249→                      height: '8px',
   250→                      borderRadius: '50%',
   251→                      backgroundColor: 'var(--color-text-secondary)',
   252→                      flexShrink: 0,
   253→                    }} />
   254→
   255→                    {/* Project badge + issue title */}
   256→                    <div style={{ flex: 1, minWidth: 0 }}>
   257→                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
   258→                        <span style={{
   259→                          fontSize: '10px',
   260→                          padding: '1px 6px',
   261→                          backgroundColor: 'var(--color-border)',
   262→                          color: 'var(--color-text-secondary)',
   263→                          textTransform: 'uppercase',
   264→                          letterSpacing: '0.5px',
   265→                          flexShrink: 0,
   266→                        }}>
   267→                          {project.name}
   268→                        </span>
   269→                        <span style={{
   270→                          overflow: 'hidden',
   271→                          textOverflow: 'ellipsis',
   272→                          whiteSpace: 'nowrap',
   273→                          fontSize: '13px',
   274→                        }}>
   275→                          {issue.title}
   276→                        </span>
   277→                      </div>
   278→                    </div>
   279→
   280→                    {/* Status label */}
   281→                    <span style={{
   282→                      fontSize: '11px',
   283→                      color: 'var(--color-text-secondary)',
   284→                      fontWeight: 600,
   285→                      flexShrink: 0,
   286→                    }}>
   287→                      IDLE
   288→                    </span>
   289→
   290→                    {/* Run button */}
   291→                    <button
   292→                      onClick={() => triggerPipeline(issue.id)}
   293→                      style={{
   294→                        padding: '4px 12px',
   295→                        fontSize: '11px',
   296→                        fontFamily: 'inherit',
   297→                        background: 'transparent',
   298→                        border: '1px solid var(--color-success)',
   299→                        color: 'var(--color-success)',
   300→                        cursor: 'pointer',
   301→                        flexShrink: 0,
   302→                      }}
   303→                      onMouseEnter={e => {
   304→                        e.currentTarget.style.backgroundColor = 'var(--color-success)';
   305→                        e.currentTarget.style.color = '#000';
   306→                      }}
   307→                      onMouseLeave={e => {
   308→                        e.currentTarget.style.backgroundColor = 'transparent';
   309→                        e.currentTarget.style.color = 'var(--color-success)';
   310→                      }}
   311→                    >
   312→                      Run
   313→                    </button>
   314→                  </div>
   315→                </div>
   316→              ))}
   317→
   318→              {/* Empty state — no issues at all */}
   319→              {agentRunCards.length === 0 && idleIssueCards.length === 0 && displayedProjects.map(project => (
   320→                <div
   321→                  key={`empty-${project.id}`}
   322→                  style={{
   323→                    backgroundColor: 'var(--color-bg-card)',
   324→                    border: '1px solid var(--color-border)',
   325→                    borderLeft: '3px solid var(--color-text-secondary)',
   326→                  }}
   327→                >
   328→                  <div style={{
   329→                    display: 'flex',
   330→                    alignItems: 'center',
   331→                    padding: '12px',
   332→                    gap: '12px',
   333→                  }}>
   334→                    <span style={{
   335→                      width: '8px',
   336→                      height: '8px',
   337→                      borderRadius: '50%',
   338→                      backgroundColor: 'var(--color-text-secondary)',
   339→                      flexShrink: 0,
   340→                    }} />
   341→                    <div style={{ flex: 1, minWidth: 0 }}>
   342→                      <div style={{
   343→                        fontSize: '13px',
   344→                        fontWeight: 600,
   345→                      }}>
   346→                        {project.name}
   347→                      </div>
   348→                      <div style={{
   349→                        fontSize: '11px',
   350→                        color: 'var(--color-text-secondary)',
   351→                        marginTop: '2px',
   352→                      }}>
   353→                        No issues yet
   354→                      </div>
   355→                    </div>
   356→                    <button
   357→                      onClick={() => {
   358→                        setNewIssueProjectId(project.id);
   359→                        setShowNewIssueModal(true);
   360→                      }}
   361→                      style={{
   362→                        padding: '4px 10px',
   363→                        fontSize: '11px',
   364→                        fontFamily: 'inherit',
   365→                        background: 'transparent',
   366→                        border: '1px solid var(--color-border)',
   367→                        color: 'var(--color-success)',
   368→                        cursor: 'pointer',
   369→                        flexShrink: 0,
   370→                      }}
   371→                      onMouseEnter={e => (e.currentTarget.style.backgroundColor = 'var(--color-bg-card-hover)')}
   372→                      onMouseLeave={e => (e.currentTarget.style.backgroundColor = 'transparent')}
   373→                    >
   374→                      + Issue
   375→                    </button>
   376→                  </div>
   377→                </div>
   378→              ))}
   379→            </div>
   380→          </div>
   381→        )}
   382→      </div>
   383→
   384→      {/* Bottom event log */}
   385→      <EventLog entries={eventLog} />
   386→
   387→      {/* Floating action button */}
   388→      <FloatingActionButton
   389→        onNewIssue={handleNewIssue}
   390→        onNewProject={handleNewProject}
   391→        onSyncGithub={handleSyncGithub}
   392→      />
   393→
   394→      {/* New Issue Modal */}
   395→      {showNewIssueModal && (
   396→        <NewIssueModal
   397→          projects={projects}
   398→          defaultProjectId={newIssueProjectId}
   399→          onSubmit={handleIssueSubmit}
   400→          onClose={() => { setShowNewIssueModal(false); setNewIssueProjectId(null); }}
   401→        />
   402→      )}
   403→
   404→      {/* Delete Confirmation Dialog */}
   405→      {deleteConfirm && (
   406→        <ConfirmDialog
   407→          title="Delete project"
   408→          message={`Delete "${deleteConfirm.name}"? This will remove all its issues and pipeline runs.`}
   409→          confirmLabel="Delete"
   410→          onConfirm={() => {
   411→            handleDeleteProject(deleteConfirm.id);
   412→            setDeleteConfirm(null);
   413→          }}
   414→          onCancel={() => setDeleteConfirm(null)}
   415→        />
   416→      )}
   417→
   418→      {/* Project Setup Modal */}
   419→      {showProjectSetup && (
   420→        <div
   421→          data-testid="project-setup-modal"
   422→          onClick={() => setShowProjectSetup(false)}
   423→          style={{
   424→            position: 'fixed',
   425→            inset: 0,
   426→            backgroundColor: 'rgba(0,0,0,0.7)',
   427→            display: 'flex',
   428→            alignItems: 'center',
   429→            justifyContent: 'center',
   430→            zIndex: 100,
   431→          }}
   432→        >
   433→          <div onClick={e => e.stopPropagation()} style={{ width: '100%', maxWidth: '500px' }}>
   434→            <ProjectSetup
   435→              projects={projects}
   436→              onSelect={handleProjectSelect}
   437→              onCreate={handleProjectCreate}
   438→              onClone={handleCloneProject}
   439→            />
   440→          </div>
   441→        </div>
   442→      )}
   443→    </div>
   444→  );
   445→}
   446→
   447→function App() {
   448→  const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`;
   449→  return (
   450→    <WebSocketProvider url={wsUrl}>
   451→      <MissionControl />
   452→    </WebSocketProvider>
   453→  );
   454→}
   455→
   456→export default App;
   457→
```

> TOOL

tool_use Read
id: toolu_01Vi82Abj3HycdBomHEajzSH
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/api/client.ts"
}
```

> TOOL

tool_result
id: toolu_01Vi82Abj3HycdBomHEajzSH
```
     1→const BASE_URL = '/api';
     2→
     3→async function request<T>(path: string, options?: RequestInit): Promise<T> {
     4→  const res = await fetch(`${BASE_URL}${path}`, {
     5→    headers: { 'Content-Type': 'application/json', ...options?.headers },
     6→    ...options,
     7→  });
     8→  if (!res.ok) {
     9→    const error = await res.text();
    10→    throw new Error(`API error ${res.status}: ${error}`);
    11→  }
    12→  if (res.status === 204) return undefined as T;
    13→  return res.json();
    14→}
    15→
    16→export const api = {
    17→  // Projects
    18→  listProjects: () => request<import('../types').Project[]>('/projects'),
    19→  createProject: (name: string, path: string) =>
    20→    request<import('../types').Project>('/projects', {
    21→      method: 'POST',
    22→      body: JSON.stringify({ name, path }),
    23→    }),
    24→  cloneProject: (repoUrl: string) =>
    25→    request<import('../types').Project>('/projects/clone', {
    26→      method: 'POST',
    27→      body: JSON.stringify({ repo_url: repoUrl }),
    28→    }),
    29→  getProject: (id: number) => request<import('../types').Project>(`/projects/${id}`),
    30→  deleteProject: (id: number) =>
    31→    request<void>(`/projects/${id}`, { method: 'DELETE' }),
    32→
    33→  // Board
    34→  getBoard: (projectId: number) =>
    35→    request<import('../types').BoardView>(`/projects/${projectId}/board`),
    36→
    37→  // Issues
    38→  createIssue: (projectId: number, title: string, description: string, column: string = 'backlog') =>
    39→    request<import('../types').Issue>(`/projects/${projectId}/issues`, {
    40→      method: 'POST',
    41→      body: JSON.stringify({ title, description, column }),
    42→    }),
    43→  getIssue: (id: number) => request<import('../types').IssueDetail>(`/issues/${id}`),
    44→  updateIssue: (id: number, data: { title?: string; description?: string; priority?: string; labels?: string[] }) =>
    45→    request<import('../types').Issue>(`/issues/${id}`, {
    46→      method: 'PATCH',
    47→      body: JSON.stringify({
    48→        ...data,
    49→        labels: data.labels ? JSON.stringify(data.labels) : undefined,
    50→      }),
    51→    }),
    52→  moveIssue: (id: number, column: string, position: number) =>
    53→    request<import('../types').Issue>(`/issues/${id}/move`, {
    54→      method: 'PATCH',
    55→      body: JSON.stringify({ column, position }),
    56→    }),
    57→  deleteIssue: (id: number) =>
    58→    request<void>(`/issues/${id}`, { method: 'DELETE' }),
    59→
    60→  // Pipeline
    61→  triggerPipeline: (issueId: number) =>
    62→    request<import('../types').PipelineRun>(`/issues/${issueId}/run`, { method: 'POST' }),
    63→  getPipelineRun: (id: number) =>
    64→    request<import('../types').PipelineRun>(`/runs/${id}`),
    65→  cancelPipelineRun: (id: number) =>
    66→    request<import('../types').PipelineRun>(`/runs/${id}/cancel`, { method: 'POST' }),
    67→
    68→  // Agent Team
    69→  getRunTeam: (runId: number) =>
    70→    request<import('../types').AgentTeamDetail>(`/runs/${runId}/team`),
    71→  getRunPhases: (runId: number) =>
    72→    request<import('../types').PipelinePhase[]>(`/runs/${runId}/phases`),
    73→  getTaskEvents: (taskId: number, limit: number = 100) =>
    74→    request<import('../types').AgentEvent[]>(`/tasks/${taskId}/events?limit=${limit}`),
    75→
    76→  // GitHub OAuth
    77→  githubStatus: () => request<import('../types').GitHubAuthStatus>('/github/status'),
    78→  githubDeviceCode: () => request<import('../types').GitHubDeviceCode>('/github/device-code', { method: 'POST' }),
    79→  githubPollToken: (deviceCode: string) =>
    80→    request<{ status: 'pending' | 'complete'; access_token?: string }>('/github/poll', {
    81→      method: 'POST',
    82→      body: JSON.stringify({ device_code: deviceCode }),
    83→    }),
    84→  githubConnectToken: (token: string) =>
    85→    request<{ status: string }>('/github/connect', {
    86→      method: 'POST',
    87→      body: JSON.stringify({ token }),
    88→    }),
    89→  githubRepos: () => request<import('../types').GitHubRepo[]>('/github/repos'),
    90→  githubDisconnect: () => request<{ status: string }>('/github/disconnect', { method: 'POST' }),
    91→
    92→  // GitHub Sync
    93→  syncGithub: (projectId: number) =>
    94→    request<import('../types').SyncResult>(`/projects/${projectId}/sync-github`, {
    95→      method: 'POST',
    96→    }),
    97→
    98→  // CLI Help
    99→  cliHelp: () => request<import('../types').CliHelpResponse>('/cli-help'),
   100→};
   101→
```

> AGENT

Now let me read the API router setup to see where routes are registered.

> TOOL

tool_use Read
id: toolu_012iFncT8UkNCmDqdbKqBMtR
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_012iFncT8UkNCmDqdbKqBMtR
```
     1→use std::collections::HashMap;
     2→use std::str::FromStr;
     3→use std::sync::{Arc, Mutex, OnceLock};
     4→
     5→use crate::errors::FactoryError;
     6→
     7→use axum::{
     8→    Json, Router,
     9→    extract::{Path, Query, State},
    10→    http::StatusCode,
    11→    response::{IntoResponse, Response},
    12→    routing::{get, patch, post},
    13→};
    14→use serde::Deserialize;
    15→use tokio::sync::broadcast;
    16→
    17→use super::db::DbHandle;
    18→#[cfg(test)]
    19→use super::db::FactoryDb;
    20→use super::models::IssueColumn;
    21→use super::pipeline::PipelineRunner;
    22→use super::ws::{WsMessage, broadcast_message};
    23→use crate::metrics::MetricsCollector;
    24→
    25→// ── Shared application state ──────────────────────────────────────────
    26→
    27→pub struct AppState {
    28→    pub db: DbHandle,
    29→    pub ws_tx: broadcast::Sender<String>,
    30→    pub pipeline_runner: PipelineRunner,
    31→    pub github_client_id: Option<String>,
    32→    pub github_token: Mutex<Option<String>>,
    33→    pub metrics: MetricsCollector,
    34→}
    35→
    36→pub type SharedState = Arc<AppState>;
    37→
    38→// ── Request payload types ─────────────────────────────────────────────
    39→
    40→#[derive(Deserialize)]
    41→pub struct CreateProjectRequest {
    42→    pub name: String,
    43→    pub path: String,
    44→}
    45→
    46→#[derive(Deserialize)]
    47→pub struct CloneProjectRequest {
    48→    pub repo_url: String,
    49→}
    50→
    51→#[derive(Deserialize)]
    52→pub struct CreateIssueRequest {
    53→    pub title: String,
    54→    pub description: Option<String>,
    55→    pub column: Option<String>,
    56→}
    57→
    58→#[derive(Deserialize)]
    59→pub struct UpdateIssueRequest {
    60→    pub title: Option<String>,
    61→    pub description: Option<String>,
    62→    pub priority: Option<String>,
    63→    pub labels: Option<String>,
    64→}
    65→
    66→#[derive(Deserialize)]
    67→pub struct MoveIssueRequest {
    68→    pub column: String,
    69→    pub position: i32,
    70→}
    71→
    72→#[derive(Deserialize)]
    73→pub struct PollTokenRequest {
    74→    pub device_code: String,
    75→}
    76→
    77→#[derive(Deserialize)]
    78→pub struct ConnectTokenRequest {
    79→    pub token: String,
    80→}
    81→
    82→#[derive(serde::Serialize)]
    83→pub struct GitHubAuthStatus {
    84→    pub connected: bool,
    85→    pub client_id_configured: bool,
    86→}
    87→
    88→#[derive(serde::Serialize)]
    89→pub struct SyncResult {
    90→    pub imported: usize,
    91→    pub skipped: usize,
    92→    pub total_github: usize,
    93→}
    94→
    95→#[derive(Clone, serde::Serialize)]
    96→pub struct CliCommand {
    97→    pub name: String,
    98→    pub description: String,
    99→}
   100→
```

> TOOL

tool_use Grep
id: toolu_01DHLYHddDPz5U9omDwFWawV
```json
{
  "pattern": "pub fn api_router|fn api_router|Router::new",
  "path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01DHLYHddDPz5U9omDwFWawV
```
192:pub fn api_router() -> Router<SharedState> {
193:    Router::new()
```

> TOOL

tool_use Read
id: toolu_011KxB4XJonnY841UbGqEBJL
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "offset": 192,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_011KxB4XJonnY841UbGqEBJL
```
   192→pub fn api_router() -> Router<SharedState> {
   193→    Router::new()
   194→        .route("/api/projects", get(list_projects).post(create_project))
   195→        .route("/api/projects/clone", post(clone_project))
   196→        .route(
   197→            "/api/projects/{id}",
   198→            get(get_project).delete(delete_project),
   199→        )
   200→        .route("/api/projects/{id}/board", get(get_board))
   201→        .route("/api/projects/{id}/sync-github", post(sync_github_issues))
   202→        .route("/api/projects/{id}/issues", post(create_issue))
   203→        .route(
   204→            "/api/issues/{id}",
   205→            get(get_issue).patch(update_issue).delete(delete_issue),
   206→        )
   207→        .route("/api/issues/{id}/move", patch(move_issue))
   208→        .route("/api/issues/{id}/run", post(trigger_pipeline))
   209→        .route("/api/runs/{id}", get(get_pipeline_run))
   210→        .route("/api/runs/{id}/cancel", post(cancel_pipeline_run))
   211→        .route("/api/runs/{id}/team", get(get_run_team))
   212→        .route("/api/runs/{id}/phases", get(get_run_phases))
   213→        .route("/api/tasks/{id}/events", get(get_task_events))
   214→        .route("/api/github/status", get(github_status))
   215→        .route("/api/github/device-code", post(github_device_code))
   216→        .route("/api/github/poll", post(github_poll_token))
   217→        .route("/api/github/connect", post(github_connect_token))
   218→        .route("/api/github/repos", get(github_list_repos))
   219→        .route("/api/github/disconnect", post(github_disconnect))
   220→        .route("/api/screenshots/{*path}", get(serve_screenshot))
   221→        .route("/api/cli-help", get(cli_help_handler))
   222→        .route("/api/metrics/summary", get(get_metrics_summary))
   223→        .route("/api/metrics/phases", get(get_metrics_phases))
   224→        .route("/api/metrics/reviews", get(get_metrics_reviews))
   225→        .route("/api/metrics/tokens", get(get_metrics_tokens))
   226→        .route("/api/metrics/runs/recent", get(get_metrics_recent_runs))
   227→        .route("/health", get(health_check))
   228→}
   229→
   230→// ── Helpers ───────────────────────────────────────────────────────────
   231→
   232→/// Extract "owner/repo" from various GitHub URL formats.
   233→fn parse_github_owner_repo(url: &str) -> Option<String> {
   234→    let url = url.trim().trim_end_matches('/').trim_end_matches(".git");
   235→    // Handle https://github.com/owner/repo and https://TOKEN@github.com/owner/repo
   236→    if let Some(github_pos) = url.find("github.com/") {
   237→        let rest = &url[github_pos + "github.com/".len()..];
   238→        let parts: Vec<&str> = rest.splitn(3, '/').collect();
   239→        if parts.len() >= 2 && !parts[0].is_empty() && !parts[1].is_empty() {
   240→            return Some(format!("{}/{}", parts[0], parts[1]));
   241→        }
   242→    }
   243→    if let Some(rest) = url.strip_prefix("git@github.com:") {
   244→        let parts: Vec<&str> = rest.splitn(3, '/').collect();
   245→        if parts.len() >= 2 {
   246→            return Some(format!("{}/{}", parts[0], parts[1]));
   247→        }
   248→    }
   249→    // Bare "owner/repo" format
   250→    let parts: Vec<&str> = url.splitn(3, '/').collect();
   251→    if parts.len() == 2 && !parts[0].contains(':') && !parts[0].contains('.') {
```

> TOOL

tool_use Read
id: toolu_01NCVjzwX6UxxdDUZZH2ZQC8
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/Analytics.tsx"
}
```

> TOOL

tool_result
id: toolu_01NCVjzwX6UxxdDUZZH2ZQC8
```
     1→/** Analytics dashboard — summary stats, phase performance, and recent runs. */
     2→import { useState, useEffect, useCallback } from 'react';
     3→import type { SummaryStats, PhaseNameStats, RunSummary } from '../types';
     4→
     5→type TimeRange = 7 | 30 | 90;
     6→
     7→// ── Helpers ─────────────────────────────────────────────────────────
     8→
     9→function formatDuration(secs: number): string {
    10→  if (secs < 60) return `${Math.round(secs)}s`;
    11→  if (secs < 3600) return `${Math.floor(secs / 60)}m ${Math.round(secs % 60)}s`;
    12→  const h = Math.floor(secs / 3600);
    13→  const m = Math.floor((secs % 3600) / 60);
    14→  return `${h}h ${m}m`;
    15→}
    16→
    17→function formatPercent(rate: number): string {
    18→  return `${(rate * 100).toFixed(1)}%`;
    19→}
    20→
    21→function formatDate(iso: string): string {
    22→  const d = new Date(iso);
    23→  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    24→}
    25→
    26→// ── Component ───────────────────────────────────────────────────────
    27→
    28→export default function Analytics() {
    29→  const [timeRange, setTimeRange] = useState<TimeRange>(30);
    30→  const [summary, setSummary] = useState<SummaryStats | null>(null);
    31→  const [phases, setPhases] = useState<PhaseNameStats[]>([]);
    32→  const [recentRuns, setRecentRuns] = useState<RunSummary[]>([]);
    33→  const [loading, setLoading] = useState(true);
    34→  const [error, setError] = useState<string | null>(null);
    35→
    36→  const fetchData = useCallback(async (days: TimeRange) => {
    37→    setLoading(true);
    38→    setError(null);
    39→    try {
    40→      const [summaryRes, phasesRes, runsRes] = await Promise.all([
    41→        fetch(`/api/metrics/summary?days=${days}`),
    42→        fetch(`/api/metrics/phases?days=${days}`),
    43→        fetch(`/api/metrics/runs/recent?limit=20`),
    44→      ]);
    45→
    46→      if (!summaryRes.ok || !phasesRes.ok || !runsRes.ok) {
    47→        throw new Error('Failed to fetch metrics data');
    48→      }
    49→
    50→      const [summaryData, phasesData, runsData] = await Promise.all([
    51→        summaryRes.json() as Promise<SummaryStats>,
    52→        phasesRes.json() as Promise<PhaseNameStats[]>,
    53→        runsRes.json() as Promise<RunSummary[]>,
    54→      ]);
    55→
    56→      setSummary(summaryData);
    57→      setPhases(phasesData);
    58→      setRecentRuns(runsData);
    59→    } catch (err) {
    60→      setError(err instanceof Error ? err.message : 'Unknown error');
    61→    } finally {
    62→      setLoading(false);
    63→    }
    64→  }, []);
    65→
    66→  useEffect(() => {
    67→    fetchData(timeRange);
    68→  }, [timeRange, fetchData]);
    69→
    70→  if (loading) {
    71→    return (
    72→      <div style={{
    73→        display: 'flex',
    74→        alignItems: 'center',
    75→        justifyContent: 'center',
    76→        height: '100%',
    77→        color: 'var(--color-text-secondary)',
    78→        fontSize: '13px',
    79→        gap: '8px',
    80→      }}>
    81→        <span className="pulse-dot" style={{
    82→          width: '8px',
    83→          height: '8px',
    84→          borderRadius: '50%',
    85→          backgroundColor: 'var(--color-success)',
    86→        }} />
    87→        Loading analytics...
    88→      </div>
    89→    );
    90→  }
    91→
    92→  if (error) {
    93→    return (
    94→      <div style={{
    95→        display: 'flex',
    96→        alignItems: 'center',
    97→        justifyContent: 'center',
    98→        height: '100%',
    99→        color: 'var(--color-error)',
   100→        fontSize: '13px',
   101→      }}>
   102→        Failed to load analytics: {error}
   103→      </div>
   104→    );
   105→  }
   106→
   107→  if (!summary || summary.total_runs === 0) {
   108→    return (
   109→      <div style={{
   110→        display: 'flex',
   111→        flexDirection: 'column',
   112→        alignItems: 'center',
   113→        justifyContent: 'center',
   114→        height: '100%',
   115→        gap: '8px',
   116→      }}>
   117→        <span style={{ color: 'var(--color-text-secondary)', fontSize: '13px' }}>
   118→          No pipeline metrics yet
   119→        </span>
   120→        <span style={{ color: 'var(--color-text-secondary)', fontSize: '11px' }}>
   121→          Run some pipelines to see analytics here
   122→        </span>
   123→      </div>
   124→    );
   125→  }
   126→
   127→  return (
   128→    <div style={{ padding: '16px', overflowY: 'auto', height: '100%' }}>
   129→      {/* Header + time range selector */}
   130→      <div style={{
   131→        display: 'flex',
   132→        alignItems: 'center',
   133→        justifyContent: 'space-between',
   134→        marginBottom: '16px',
   135→      }}>
   136→        <span style={{
   137→          fontSize: '14px',
   138→          fontWeight: 700,
   139→          color: 'var(--color-text-primary)',
   140→          letterSpacing: '1px',
   141→          textTransform: 'uppercase',
   142→        }}>
   143→          Analytics
   144→        </span>
   145→        <div style={{ display: 'flex', gap: '4px' }}>
   146→          {([7, 30, 90] as TimeRange[]).map(days => (
   147→            <button
   148→              key={days}
   149→              onClick={() => setTimeRange(days)}
   150→              style={{
   151→                padding: '4px 8px',
   152→                background: timeRange === days ? 'var(--color-border)' : 'transparent',
   153→                border: '1px solid var(--color-border)',
   154→                color: 'var(--color-text-primary)',
   155→                cursor: 'pointer',
   156→                fontSize: '12px',
   157→              }}
   158→            >
   159→              {days}d
   160→            </button>
   161→          ))}
   162→        </div>
   163→      </div>
   164→
   165→      {/* Summary cards */}
   166→      <div style={{
   167→        display: 'grid',
   168→        gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
   169→        gap: '12px',
   170→        marginBottom: '24px',
   171→      }}>
   172→        <SummaryCard label="Total Runs" value={String(summary.total_runs)} />
   173→        <SummaryCard
   174→          label="Success Rate"
   175→          value={formatPercent(summary.success_rate)}
   176→          valueColor={summary.success_rate >= 0.8 ? 'var(--color-success)' : summary.success_rate >= 0.5 ? 'var(--color-warning)' : 'var(--color-error)'}
   177→        />
   178→        <SummaryCard label="Avg Duration" value={formatDuration(summary.avg_duration_secs)} />
   179→        <SummaryCard label="Total Phases" value={String(summary.total_phases)} />
   180→        <SummaryCard label="Successful Runs" value={String(summary.successful_runs)} valueColor="var(--color-success)" />
   181→        <SummaryCard label="Avg Iterations / Phase" value={summary.avg_iterations_per_phase.toFixed(1)} />
   182→      </div>
   183→
   184→      {/* Phase performance table */}
   185→      {phases.length > 0 && (
   186→        <div style={{ marginBottom: '24px' }}>
   187→          <div style={{
   188→            fontSize: '12px',
   189→            fontWeight: 600,
   190→            color: 'var(--color-text-secondary)',
   191→            textTransform: 'uppercase',
   192→            letterSpacing: '0.5px',
   193→            marginBottom: '8px',
   194→          }}>
   195→            Phase Performance
   196→          </div>
   197→          <div style={{
   198→            backgroundColor: 'var(--color-bg-card)',
   199→            border: '1px solid var(--color-border)',
   200→          }}>
   201→            {/* Table header */}
   202→            <div style={{
   203→              display: 'grid',
   204→              gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr 1fr',
   205→              padding: '8px 12px',
   206→              borderBottom: '1px solid var(--color-border)',
   207→              fontSize: '11px',
   208→              fontWeight: 600,
   209→              color: 'var(--color-text-secondary)',
   210→              textTransform: 'uppercase',
   211→              letterSpacing: '0.5px',
   212→            }}>
   213→              <span>Phase</span>
   214→              <span style={{ textAlign: 'right' }}>Runs</span>
   215→              <span style={{ textAlign: 'right' }}>Avg Iters</span>
   216→              <span style={{ textAlign: 'right' }}>Avg Duration</span>
   217→              <span style={{ textAlign: 'right' }}>Budget Use</span>
   218→              <span style={{ textAlign: 'right' }}>Success</span>
   219→            </div>
   220→            {/* Table rows */}
   221→            {phases.map(phase => (
   222→              <div
   223→                key={phase.phase_name}
   224→                style={{
   225→                  display: 'grid',
   226→                  gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr 1fr',
   227→                  padding: '8px 12px',
   228→                  borderBottom: '1px solid var(--color-border)',
   229→                  fontSize: '12px',
   230→                  color: 'var(--color-text-primary)',
   231→                }}
   232→              >
   233→                <span style={{
   234→                  overflow: 'hidden',
   235→                  textOverflow: 'ellipsis',
   236→                  whiteSpace: 'nowrap',
   237→                }}>
   238→                  {phase.phase_name}
   239→                </span>
   240→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   241→                  {phase.run_count}
   242→                </span>
   243→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   244→                  {phase.avg_iterations.toFixed(1)}
   245→                </span>
   246→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   247→                  {formatDuration(phase.avg_duration_secs)}
   248→                </span>
   249→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   250→                  {formatPercent(phase.budget_utilization)}
   251→                </span>
   252→                <span style={{
   253→                  textAlign: 'right',
   254→                  color: phase.success_rate >= 0.8 ? 'var(--color-success)' : phase.success_rate >= 0.5 ? 'var(--color-warning)' : 'var(--color-error)',
   255→                }}>
   256→                  {formatPercent(phase.success_rate)}
   257→                </span>
   258→              </div>
   259→            ))}
   260→          </div>
   261→        </div>
   262→      )}
   263→
   264→      {/* Recent runs */}
   265→      {recentRuns.length > 0 && (
   266→        <div>
   267→          <div style={{
   268→            fontSize: '12px',
   269→            fontWeight: 600,
   270→            color: 'var(--color-text-secondary)',
   271→            textTransform: 'uppercase',
   272→            letterSpacing: '0.5px',
   273→            marginBottom: '8px',
   274→          }}>
   275→            Recent Runs
   276→          </div>
   277→          <div style={{
   278→            backgroundColor: 'var(--color-bg-card)',
   279→            border: '1px solid var(--color-border)',
   280→          }}>
   281→            {/* Table header */}
   282→            <div style={{
   283→              display: 'grid',
   284→              gridTemplateColumns: '1fr 1fr 80px 100px 80px 140px',
   285→              padding: '8px 12px',
   286→              borderBottom: '1px solid var(--color-border)',
   287→              fontSize: '11px',
   288→              fontWeight: 600,
   289→              color: 'var(--color-text-secondary)',
   290→              textTransform: 'uppercase',
   291→              letterSpacing: '0.5px',
   292→            }}>
   293→              <span>Run ID</span>
   294→              <span>Issue</span>
   295→              <span style={{ textAlign: 'center' }}>Status</span>
   296→              <span style={{ textAlign: 'right' }}>Duration</span>
   297→              <span style={{ textAlign: 'right' }}>Phases</span>
   298→              <span style={{ textAlign: 'right' }}>Started</span>
   299→            </div>
   300→            {/* Table rows */}
   301→            {recentRuns.map(run => (
   302→              <div
   303→                key={run.run_id}
   304→                style={{
   305→                  display: 'grid',
   306→                  gridTemplateColumns: '1fr 1fr 80px 100px 80px 140px',
   307→                  padding: '8px 12px',
   308→                  borderBottom: '1px solid var(--color-border)',
   309→                  fontSize: '12px',
   310→                  color: 'var(--color-text-primary)',
   311→                }}
   312→              >
   313→                <span style={{
   314→                  overflow: 'hidden',
   315→                  textOverflow: 'ellipsis',
   316→                  whiteSpace: 'nowrap',
   317→                  fontFamily: 'monospace',
   318→                  fontSize: '11px',
   319→                }}>
   320→                  {run.run_id}
   321→                </span>
   322→                <span style={{ color: 'var(--color-text-secondary)' }}>
   323→                  {run.issue_id !== null ? `#${run.issue_id}` : '--'}
   324→                </span>
   325→                <span style={{
   326→                  textAlign: 'center',
   327→                  color: run.success ? 'var(--color-success)' : 'var(--color-error)',
   328→                  fontWeight: 600,
   329→                  fontSize: '11px',
   330→                }}>
   331→                  {run.success ? 'PASS' : 'FAIL'}
   332→                </span>
   333→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   334→                  {run.duration_secs !== null ? formatDuration(run.duration_secs) : '--'}
   335→                </span>
   336→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)' }}>
   337→                  {run.phases_total !== null ? run.phases_total : '--'}
   338→                </span>
   339→                <span style={{ textAlign: 'right', color: 'var(--color-text-secondary)', fontSize: '11px' }}>
   340→                  {formatDate(run.started_at)}
   341→                </span>
   342→              </div>
   343→            ))}
   344→          </div>
   345→        </div>
   346→      )}
   347→    </div>
   348→  );
   349→}
   350→
   351→// ── Sub-components ──────────────────────────────────────────────────
   352→
   353→function SummaryCard({ label, value, valueColor }: {
   354→  label: string;
   355→  value: string;
   356→  valueColor?: string;
   357→}) {
   358→  return (
   359→    <div style={{
   360→      backgroundColor: 'var(--color-bg-card)',
   361→      border: '1px solid var(--color-border)',
   362→      padding: '12px',
   363→    }}>
   364→      <div style={{
   365→        fontSize: '11px',
   366→        color: 'var(--color-text-secondary)',
   367→        textTransform: 'uppercase',
   368→        letterSpacing: '0.5px',
   369→        marginBottom: '4px',
   370→      }}>
   371→        {label}
   372→      </div>
   373→      <div style={{
   374→        fontSize: '20px',
   375→        fontWeight: 700,
   376→        color: valueColor ?? 'var(--color-text-primary)',
   377→      }}>
   378→        {value}
   379→      </div>
   380→    </div>
   381→  );
   382→}
   383→
```

> AGENT

I have a complete picture. I'll implement this as:

1. **Backend**: New `/api/agents` endpoint returning the 4 built-in specialists with their details
2. **Frontend**: New "agents" view mode with detailed agent cards

Let me implement everything now.

> TOOL

tool_use Edit
id: toolu_01WtYXizLSi7LSzC4oUS1dqh
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/review/specialists.rs",
  "old_string": "    /// Get the default focus areas for this specialist type.",
  "new_string": "    /// Get a short description of what this specialist does.\n    pub fn description(&self) -> &str {\n        match self {\n            Self::SecuritySentinel => \"Examines code for security vulnerabilities, authentication weaknesses, and data exposure risks. Acts as a gating reviewer — issues must be resolved before a phase can complete.\",\n            Self::PerformanceOracle => \"Analyzes code for performance bottlenecks, resource inefficiencies, and scalability concerns. Operates in advisory mode — findings are reported but don't block progress.\",\n            Self::ArchitectureStrategist => \"Reviews structural design decisions, module boundaries, and dependency relationships. Acts as a gating reviewer — architectural issues must be addressed before proceeding.\",\n            Self::SimplicityReviewer => \"Identifies over-engineering, unnecessary complexity, and YAGNI violations. Operates in advisory mode — encourages simplicity without blocking delivery.\",\n            Self::Custom(name) => {\n                // Return static str not possible for dynamic, but we use a fallback\n                let _ = name;\n                \"Custom review specialist with user-defined focus areas.\"\n            }\n        }\n    }\n\n    /// Whether this specialist type gates phase completion by default.\n    pub fn default_gating(&self) -> bool {\n        match self {\n            Self::SecuritySentinel | Self::ArchitectureStrategist => true,\n            Self::PerformanceOracle | Self::SimplicityReviewer => false,\n            Self::Custom(_) => false,\n        }\n    }\n\n    /// Get the default focus areas for this specialist type."
}
```

> TOOL

tool_result
id: toolu_01WtYXizLSi7LSzC4oUS1dqh
```
The file /Users/jdsingh/Projects/AI/forge/src/review/specialists.rs has been updated successfully.
```

> AGENT

Now add the API endpoint. Let me find where to add it in api.rs.

> TOOL

tool_use Read
id: toolu_01CFpQizVoqvgG8jJQkg79fu
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "offset": 95,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01CFpQizVoqvgG8jJQkg79fu
```
    95→#[derive(Clone, serde::Serialize)]
    96→pub struct CliCommand {
    97→    pub name: String,
    98→    pub description: String,
    99→}
   100→
   101→#[derive(Clone, serde::Serialize)]
   102→pub struct CliOption {
   103→    pub flag: String,
   104→    pub description: String,
   105→}
   106→
   107→#[derive(Clone, serde::Serialize)]
   108→pub struct CliHelpResponse {
   109→    pub commands: Vec<CliCommand>,
   110→    pub options: Vec<CliOption>,
   111→}
   112→
   113→// ── Error handling ────────────────────────────────────────────────────
   114→
   115→pub enum ApiError {
   116→    NotFound(String),
   117→    BadRequest(String),
   118→    Internal(String),
   119→}
   120→
   121→impl IntoResponse for ApiError {
   122→    fn into_response(self) -> Response {
   123→        let (status, message) = match self {
   124→            ApiError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
   125→            ApiError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
   126→            ApiError::Internal(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
   127→        };
   128→        (status, Json(serde_json::json!({"error": message}))).into_response()
   129→    }
   130→}
   131→
   132→impl From<FactoryError> for ApiError {
   133→    fn from(e: FactoryError) -> Self {
   134→        match e {
   135→            FactoryError::ProjectNotFound { id } => {
   136→                ApiError::NotFound(format!("Project {} not found", id))
   137→            }
   138→            FactoryError::IssueNotFound { id } => {
   139→                ApiError::NotFound(format!("Issue {} not found", id))
   140→            }
   141→            FactoryError::RunNotFound { id } => {
   142→                ApiError::NotFound(format!("Pipeline run {} not found", id))
   143→            }
   144→            FactoryError::LockPoisoned => ApiError::Internal("Internal lock poisoned".to_string()),
   145→            FactoryError::BadRequest(msg) => ApiError::BadRequest(msg),
   146→            FactoryError::InvalidColumn { column, message } => {
   147→                ApiError::BadRequest(format!("Invalid column '{}': {}", column, message))
   148→            }
   149→            FactoryError::PipelineAlreadyRunning { issue_id } => {
   150→                ApiError::BadRequest(format!("Pipeline already running for issue {}", issue_id))
   151→            }
   152→            FactoryError::GitHub(msg) => ApiError::Internal(format!("GitHub API error: {}", msg)),
   153→            FactoryError::Database(e) => ApiError::Internal(e.to_string()),
   154→            FactoryError::Other(e) => ApiError::Internal(e.to_string()),
   155→        }
   156→    }
   157→}
   158→
   159→// ── Router ────────────────────────────────────────────────────────────
   160→
   161→/// Build and return the complete Axum router for the Factory API.
   162→///
   163→/// All routes are prefixed with `/api/` except `/health`.
   164→///
   165→/// | Method | Route                           | Handler description       |
   166→/// |--------|---------------------------------|---------------------------|
   167→/// | GET    | `/api/projects`                 | List all projects         |
   168→/// | POST   | `/api/projects`                 | Create a project          |
   169→/// | POST   | `/api/projects/clone`           | Clone a GitHub repo       |
   170→/// | GET    | `/api/projects/:id`             | Get project details       |
   171→/// | GET    | `/api/projects/:id/board`       | Get Kanban board state    |
   172→/// | POST   | `/api/projects/:id/sync-github` | Sync issues from GitHub   |
   173→/// | POST   | `/api/projects/:id/issues`      | Create an issue           |
   174→/// | GET    | `/api/issues/:id`               | Get issue detail          |
   175→/// | PATCH  | `/api/issues/:id`               | Update issue title/body   |
   176→/// | DELETE | `/api/issues/:id`               | Delete an issue           |
   177→/// | PATCH  | `/api/issues/:id/move`          | Move to column/position   |
   178→/// | POST   | `/api/issues/:id/run`           | Trigger pipeline          |
   179→/// | GET    | `/api/runs/:id`                 | Get pipeline run status   |
   180→/// | POST   | `/api/runs/:id/cancel`          | Cancel a running pipeline |
   181→/// | GET    | `/api/runs/:id/team`            | Get agent team for run    |
   182→/// | GET    | `/api/runs/:id/phases`          | Get pipeline run phases   |
   183→/// | GET    | `/api/tasks/:id/events`         | Get agent task events     |
   184→/// | GET    | `/api/github/status`            | GitHub OAuth status       |
   185→/// | POST   | `/api/github/device-code`       | Initiate device flow      |
   186→/// | POST   | `/api/github/poll`              | Poll device code status   |
   187→/// | POST   | `/api/github/connect`           | Connect with PAT token    |
   188→/// | GET    | `/api/github/repos`             | List user's GitHub repos  |
   189→/// | POST   | `/api/github/disconnect`        | Remove GitHub token       |
   190→/// | GET    | `/api/cli-help`                 | Parsed CLI help data      |
   191→/// | GET    | `/health`                       | Liveness probe            |
   192→pub fn api_router() -> Router<SharedState> {
   193→    Router::new()
   194→        .route("/api/projects", get(list_projects).post(create_project))
```

> TOOL

tool_use Edit
id: toolu_01DwtyzhXb6BDF6unstfXVPT
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "old_string": "#[derive(Clone, serde::Serialize)]\npub struct CliHelpResponse {\n    pub commands: Vec<CliCommand>,\n    pub options: Vec<CliOption>,\n}",
  "new_string": "#[derive(Clone, serde::Serialize)]\npub struct CliHelpResponse {\n    pub commands: Vec<CliCommand>,\n    pub options: Vec<CliOption>,\n}\n\n#[derive(serde::Serialize)]\npub struct AgentInfo {\n    pub id: String,\n    pub name: String,\n    pub description: String,\n    pub focus_areas: Vec<String>,\n    pub default_gating: bool,\n}"
}
```

> TOOL

tool_result
id: toolu_01DwtyzhXb6BDF6unstfXVPT
```
The file /Users/jdsingh/Projects/AI/forge/src/factory/api.rs has been updated successfully.
```

> AGENT

Now add the route and handler. First, add the route:

> TOOL

tool_use Edit
id: toolu_01Qb2Ye5c8MUudj9q4VZUGvd
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "old_string": "        .route(\"/api/cli-help\", get(cli_help_handler))",
  "new_string": "        .route(\"/api/agents\", get(list_agents))\n        .route(\"/api/cli-help\", get(cli_help_handler))"
}
```

> TOOL

tool_result
id: toolu_01Qb2Ye5c8MUudj9q4VZUGvd
```
The file /Users/jdsingh/Projects/AI/forge/src/factory/api.rs has been updated successfully.
```

> AGENT

Now I need to add the handler function. Let me find where the CLI help handler is defined.

> TOOL

tool_use Grep
id: toolu_01MiFXeAEqKsG3EjuVyqPPo3
```json
{
  "pattern": "async fn cli_help_handler",
  "path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01MiFXeAEqKsG3EjuVyqPPo3
```
392:async fn cli_help_handler() -> Result<Json<CliHelpResponse>, ApiError> {
```

> TOOL

tool_use Read
id: toolu_01TL7ZYnbGud9DeeuGrCySzy
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "offset": 389,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01TL7ZYnbGud9DeeuGrCySzy
```
   389→/// `GET /api/cli-help` — return parsed CLI help (commands and options).
   390→///
   391→/// Runs `forge --help` once, caches the result, and returns it as JSON.
   392→async fn cli_help_handler() -> Result<Json<CliHelpResponse>, ApiError> {
   393→    static CACHED: OnceLock<Result<CliHelpResponse, String>> = OnceLock::new();
   394→
   395→    let result = CACHED.get_or_init(|| {
   396→        let forge_cmd = std::env::var("FORGE_CMD").unwrap_or_else(|_| "forge".to_string());
   397→        let output = std::process::Command::new(&forge_cmd)
   398→            .arg("--help")
   399→            .output()
   400→            .map_err(|e| format!("Failed to run {}: {}", forge_cmd, e))?;
   401→
   402→        let stdout = String::from_utf8_lossy(&output.stdout);
   403→        Ok(parse_cli_help(&stdout))
   404→    });
   405→
   406→    match result {
   407→        Ok(resp) => Ok(Json(resp.clone())),
   408→        Err(msg) => Err(ApiError::Internal(msg.clone())),
   409→    }
   410→}
   411→
   412→fn parse_cli_help(text: &str) -> CliHelpResponse {
   413→    let mut commands = Vec::new();
   414→    let mut options = Vec::new();
   415→
   416→    #[derive(PartialEq)]
   417→    enum Section {
   418→        None,
   419→        Commands,
   420→        Options,
   421→    }
   422→    let mut section = Section::None;
   423→
   424→    for line in text.lines() {
   425→        let trimmed = line.trim_end();
   426→        if trimmed == "Commands:" {
   427→            section = Section::Commands;
   428→            continue;
   429→        } else if trimmed == "Options:" {
   430→            section = Section::Options;
   431→            continue;
   432→        } else if !trimmed.is_empty() && !trimmed.starts_with(' ') {
   433→            // A non-indented line that isn't a section header ends the current section
   434→            section = Section::None;
   435→            continue;
   436→        }
   437→
   438→        let trimmed = trimmed.trim();
```

> AGENT

Now add the `list_agents` handler right before the `cli_help_handler`:

> TOOL

tool_use Edit
id: toolu_01YU7LCFQoo7EVCgw83SnWkv
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "old_string": "/// `GET /api/cli-help` — return parsed CLI help (commands and options).",
  "new_string": "/// `GET /api/agents` — return the built-in review specialist agents.\nasync fn list_agents() -> Json<Vec<AgentInfo>> {\n    use crate::review::SpecialistType;\n\n    let agents = SpecialistType::all_builtins()\n        .into_iter()\n        .map(|st| AgentInfo {\n            id: st.agent_name(),\n            name: st.display_name().to_string(),\n            description: st.description().to_string(),\n            focus_areas: st.focus_areas().into_iter().map(|s| s.to_string()).collect(),\n            default_gating: st.default_gating(),\n        })\n        .collect();\n\n    Json(agents)\n}\n\n/// `GET /api/cli-help` — return parsed CLI help (commands and options)."
}
```

> TOOL

tool_result
id: toolu_01YU7LCFQoo7EVCgw83SnWkv
```
The file /Users/jdsingh/Projects/AI/forge/src/factory/api.rs has been updated successfully.
```

> AGENT

Now let's update the frontend. First, update the `ViewMode` type:

> TOOL

tool_use Edit
id: toolu_01T3iZfFBuxpXdbk7FcSXfTu
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts",
  "old_string": "/** View mode for the main agent run grid */\nexport type ViewMode = 'grid' | 'list' | 'analytics';",
  "new_string": "/** View mode for the main agent run grid */\nexport type ViewMode = 'grid' | 'list' | 'analytics' | 'agents';\n\n/** A built-in review specialist agent */\nexport interface AgentInfo {\n  id: string;\n  name: string;\n  description: string;\n  focus_areas: string[];\n  default_gating: boolean;\n}"
}
```

> TOOL

tool_result
id: toolu_01T3iZfFBuxpXdbk7FcSXfTu
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts has been updated successfully.
```

> AGENT

Add the API client function:

> TOOL

tool_use Edit
id: toolu_014BueTNQKKUddZM5tdJhYbj
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/api/client.ts",
  "old_string": "  // CLI Help\n  cliHelp: () => request<import('../types').CliHelpResponse>('/cli-help'),",
  "new_string": "  // Agents\n  listAgents: () => request<import('../types').AgentInfo[]>('/agents'),\n\n  // CLI Help\n  cliHelp: () => request<import('../types').CliHelpResponse>('/cli-help'),"
}
```

> TOOL

tool_result
id: toolu_014BueTNQKKUddZM5tdJhYbj
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/api/client.ts has been updated successfully.
```

> AGENT

Now add the "agents" button to the StatusBar:

> TOOL

tool_use Edit
id: toolu_017s67ehPrW2YhFEq5pmjuim
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/StatusBar.tsx",
  "old_string": "        <button\n          onClick={() => onViewModeChange('analytics')}\n          style={{\n            padding: '4px 8px',\n            background: viewMode === 'analytics' ? 'var(--color-border)' : 'transparent',\n            border: '1px solid var(--color-border)',\n            color: 'var(--color-text-primary)',\n            cursor: 'pointer',\n            fontSize: '12px',\n          }}\n          title=\"Analytics view\"\n        >\n          analytics\n        </button>",
  "new_string": "        <button\n          onClick={() => onViewModeChange('analytics')}\n          style={{\n            padding: '4px 8px',\n            background: viewMode === 'analytics' ? 'var(--color-border)' : 'transparent',\n            border: '1px solid var(--color-border)',\n            color: 'var(--color-text-primary)',\n            cursor: 'pointer',\n            fontSize: '12px',\n          }}\n          title=\"Analytics view\"\n        >\n          analytics\n        </button>\n        <button\n          onClick={() => onViewModeChange('agents')}\n          style={{\n            padding: '4px 8px',\n            background: viewMode === 'agents' ? 'var(--color-border)' : 'transparent',\n            border: '1px solid var(--color-border)',\n            color: 'var(--color-text-primary)',\n            cursor: 'pointer',\n            fontSize: '12px',\n          }}\n          title=\"Review agents\"\n        >\n          agents\n        </button>"
}
```

> TOOL

tool_result
id: toolu_017s67ehPrW2YhFEq5pmjuim
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/components/StatusBar.tsx has been updated successfully.
```

> AGENT

Now create the Agents component:

> TOOL

tool_use Write
id: toolu_01Hh65pyiLScXWfgeDDaxp1i
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx",
  "content": "/** Agents view — displays the 4 built-in review specialist agents with their details. */\nimport { useState, useEffect, useCallback } from 'react';\nimport type { AgentInfo } from '../types';\nimport { api } from '../api/client';\n\n/** Icon + color mapping per agent */\nconst AGENT_THEME: Record<string, { icon: string; color: string; bgGlow: string }> = {\n  'security-sentinel': {\n    icon: '\\u{1F6E1}',\n    color: '#f85149',\n    bgGlow: 'rgba(248, 81, 73, 0.08)',\n  },\n  'performance-oracle': {\n    icon: '\\u{26A1}',\n    color: '#d29922',\n    bgGlow: 'rgba(210, 153, 34, 0.08)',\n  },\n  'architecture-strategist': {\n    icon: '\\u{1F3D7}',\n    color: '#58a6ff',\n    bgGlow: 'rgba(88, 166, 255, 0.08)',\n  },\n  'simplicity-reviewer': {\n    icon: '\\u{2728}',\n    color: '#3fb950',\n    bgGlow: 'rgba(63, 185, 80, 0.08)',\n  },\n};\n\nconst DEFAULT_THEME = { icon: '\\u{1F916}', color: 'var(--color-text-secondary)', bgGlow: 'transparent' };\n\nexport default function Agents() {\n  const [agents, setAgents] = useState<AgentInfo[]>([]);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState<string | null>(null);\n  const [expandedId, setExpandedId] = useState<string | null>(null);\n\n  const fetchAgents = useCallback(async () => {\n    setLoading(true);\n    setError(null);\n    try {\n      const data = await api.listAgents();\n      setAgents(data);\n    } catch (err) {\n      setError(err instanceof Error ? err.message : 'Failed to load agents');\n    } finally {\n      setLoading(false);\n    }\n  }, []);\n\n  useEffect(() => {\n    fetchAgents();\n  }, [fetchAgents]);\n\n  if (loading) {\n    return (\n      <div style={{\n        display: 'flex',\n        alignItems: 'center',\n        justifyContent: 'center',\n        height: '100%',\n        color: 'var(--color-text-secondary)',\n        fontSize: '13px',\n        gap: '8px',\n      }}>\n        <span className=\"pulse-dot\" style={{\n          width: '8px',\n          height: '8px',\n          borderRadius: '50%',\n          backgroundColor: 'var(--color-success)',\n        }} />\n        Loading agents...\n      </div>\n    );\n  }\n\n  if (error) {\n    return (\n      <div style={{\n        display: 'flex',\n        alignItems: 'center',\n        justifyContent: 'center',\n        height: '100%',\n        color: 'var(--color-error)',\n        fontSize: '13px',\n      }}>\n        Failed to load agents: {error}\n      </div>\n    );\n  }\n\n  return (\n    <div style={{ padding: '16px', overflowY: 'auto', height: '100%' }}>\n      {/* Header */}\n      <div style={{\n        display: 'flex',\n        alignItems: 'center',\n        justifyContent: 'space-between',\n        marginBottom: '16px',\n      }}>\n        <span style={{\n          fontSize: '14px',\n          fontWeight: 700,\n          color: 'var(--color-text-primary)',\n          letterSpacing: '1px',\n          textTransform: 'uppercase',\n        }}>\n          Review Agents\n        </span>\n        <span style={{\n          fontSize: '12px',\n          color: 'var(--color-text-secondary)',\n        }}>\n          {agents.length} built-in specialists\n        </span>\n      </div>\n\n      {/* Agent cards */}\n      <div style={{\n        display: 'grid',\n        gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))',\n        gap: '16px',\n      }}>\n        {agents.map(agent => {\n          const theme = AGENT_THEME[agent.id] ?? DEFAULT_THEME;\n          const isExpanded = expandedId === agent.id;\n\n          return (\n            <div\n              key={agent.id}\n              onClick={() => setExpandedId(isExpanded ? null : agent.id)}\n              style={{\n                backgroundColor: isExpanded ? theme.bgGlow : 'var(--color-bg-card)',\n                border: `1px solid ${isExpanded ? theme.color : 'var(--color-border)'}`,\n                borderLeft: `3px solid ${theme.color}`,\n                cursor: 'pointer',\n                transition: 'all 0.15s ease',\n              }}\n            >\n              {/* Card header */}\n              <div style={{\n                display: 'flex',\n                alignItems: 'center',\n                padding: '16px',\n                gap: '12px',\n              }}>\n                {/* Agent icon */}\n                <span style={{ fontSize: '24px', flexShrink: 0 }}>\n                  {theme.icon}\n                </span>\n\n                {/* Name + gating badge */}\n                <div style={{ flex: 1, minWidth: 0 }}>\n                  <div style={{\n                    display: 'flex',\n                    alignItems: 'center',\n                    gap: '8px',\n                  }}>\n                    <span style={{\n                      fontSize: '15px',\n                      fontWeight: 700,\n                      color: 'var(--color-text-primary)',\n                    }}>\n                      {agent.name}\n                    </span>\n                    <span style={{\n                      fontSize: '10px',\n                      padding: '2px 6px',\n                      backgroundColor: agent.default_gating\n                        ? 'rgba(248, 81, 73, 0.15)'\n                        : 'rgba(63, 185, 80, 0.15)',\n                      color: agent.default_gating\n                        ? 'var(--color-error)'\n                        : 'var(--color-success)',\n                      fontWeight: 600,\n                      textTransform: 'uppercase',\n                      letterSpacing: '0.5px',\n                    }}>\n                      {agent.default_gating ? 'gating' : 'advisory'}\n                    </span>\n                  </div>\n                  <div style={{\n                    fontSize: '11px',\n                    color: 'var(--color-text-secondary)',\n                    fontFamily: 'monospace',\n                    marginTop: '2px',\n                  }}>\n                    {agent.id}\n                  </div>\n                </div>\n\n                {/* Expand chevron */}\n                <span style={{\n                  color: 'var(--color-text-secondary)',\n                  fontSize: '14px',\n                  transition: 'transform 0.15s',\n                  transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',\n                  flexShrink: 0,\n                }}>\n                  ▾\n                </span>\n              </div>\n\n              {/* Description */}\n              <div style={{\n                padding: '0 16px 12px 52px',\n                fontSize: '12px',\n                color: 'var(--color-text-secondary)',\n                lineHeight: '1.5',\n              }}>\n                {agent.description}\n              </div>\n\n              {/* Expanded: focus areas */}\n              {isExpanded && (\n                <div style={{\n                  padding: '0 16px 16px 52px',\n                }}>\n                  <div style={{\n                    fontSize: '11px',\n                    fontWeight: 600,\n                    color: 'var(--color-text-secondary)',\n                    textTransform: 'uppercase',\n                    letterSpacing: '0.5px',\n                    marginBottom: '8px',\n                  }}>\n                    Focus Areas\n                  </div>\n                  <div style={{\n                    display: 'flex',\n                    flexWrap: 'wrap',\n                    gap: '6px',\n                  }}>\n                    {agent.focus_areas.map((area, i) => (\n                      <span\n                        key={i}\n                        style={{\n                          fontSize: '11px',\n                          padding: '3px 8px',\n                          backgroundColor: 'var(--color-bg-primary)',\n                          border: '1px solid var(--color-border)',\n                          color: 'var(--color-text-primary)',\n                        }}\n                      >\n                        {area}\n                      </span>\n                    ))}\n                  </div>\n\n                  {/* Usage hint */}\n                  <div style={{\n                    marginTop: '12px',\n                    padding: '8px 10px',\n                    backgroundColor: 'var(--color-bg-primary)',\n                    border: '1px solid var(--color-border)',\n                    fontSize: '11px',\n                    fontFamily: 'monospace',\n                    color: 'var(--color-text-secondary)',\n                  }}>\n                    <span style={{ color: theme.color }}>$</span> forge swarm --review {agent.id.split('-')[0]}\n                  </div>\n                </div>\n              )}\n            </div>\n          );\n        })}\n      </div>\n    </div>\n  );\n}\n"
}
```

> TOOL

tool_result
id: toolu_01Hh65pyiLScXWfgeDDaxp1i
```
File created successfully at: /Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx
```

> AGENT

Now wire it into App.tsx:

> TOOL

tool_use Edit
id: toolu_01MRQGaRjBKV1s1ZpZWbnnRq
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/App.tsx",
  "old_string": "import Analytics from './components/Analytics';",
  "new_string": "import Analytics from './components/Analytics';\nimport Agents from './components/Agents';"
}
```

> TOOL

tool_result
id: toolu_01MRQGaRjBKV1s1ZpZWbnnRq
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/App.tsx has been updated successfully.
```

> AGENT

Now update the main content area to handle the agents view:

> TOOL

tool_use Edit
id: toolu_01CRxJ2jPm2vcR7VJRYGLZNs
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/App.tsx",
  "old_string": "        {/* Main content area */}\n        {viewMode === 'analytics' ? (\n          <div style={{ flex: 1, overflow: 'hidden' }}>\n            <Analytics />\n          </div>\n        ) : (",
  "new_string": "        {/* Main content area */}\n        {viewMode === 'analytics' ? (\n          <div style={{ flex: 1, overflow: 'hidden' }}>\n            <Analytics />\n          </div>\n        ) : viewMode === 'agents' ? (\n          <div style={{ flex: 1, overflow: 'hidden' }}>\n            <Agents />\n          </div>\n        ) : ("
}
```

> TOOL

tool_result
id: toolu_01CRxJ2jPm2vcR7VJRYGLZNs
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/App.tsx has been updated successfully.
```

> AGENT

Now let's build and test. Let me build the backend first:

> TOOL

tool_use Bash
id: toolu_01NyyQnzphf1yman9iHjUYUs
```json
{
  "command": "cargo build 2>&1 | tail -20",
  "description": "Build Rust backend",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01NyyQnzphf1yman9iHjUYUs
```
   Compiling forge v0.1.0 (/Users/jdsingh/Projects/AI/forge)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 11.13s
```

> AGENT

Backend builds. Now build the frontend:

> TOOL

tool_use Bash
id: toolu_01B8uqhFAFD6j1iNuPF3DNxc
```json
{
  "command": "cd /Users/jdsingh/Projects/AI/forge/ui && npx vite build 2>&1 | tail -20",
  "description": "Build UI frontend",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01B8uqhFAFD6j1iNuPF3DNxc
```
vite v7.3.1 building client environment for production...
transforming...
✓ 43 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.73 kB │ gzip:  0.41 kB
dist/assets/index-ChFHATW8.css   20.44 kB │ gzip:  4.79 kB
dist/assets/index-Hf3YzZ40.js   263.23 kB │ gzip: 76.81 kB
✓ built in 389ms
```

> AGENT

Both build successfully. Let me also run the tests to make sure nothing broke:

> TOOL

tool_use Bash
id: toolu_01DUya2yUAd8wuYqhuxuEDtM
```json
{
  "command": "cd /Users/jdsingh/Projects/AI/forge && cargo test --lib -- review::specialists 2>&1 | tail -30",
  "description": "Run specialist tests",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01DUya2yUAd8wuYqhuxuEDtM
```
test review::specialists::tests::test_review_specialist_default ... ok
test review::specialists::tests::test_review_specialist_agent_name ... ok
test review::specialists::tests::test_review_specialist_display_name ... ok
test review::specialists::tests::test_review_specialist_gating ... ok
test review::specialists::tests::test_review_specialist_display ... ok
test review::specialists::tests::test_review_specialist_is_builtin ... ok
test review::specialists::tests::test_review_specialist_default_focus_areas ... ok
test review::specialists::tests::test_review_specialist_new ... ok
test review::specialists::tests::test_specialist_type_agent_name ... ok
test review::specialists::tests::test_specialist_type_default ... ok
test review::specialists::tests::test_review_specialist_with_focus_areas ... ok
test review::specialists::tests::test_specialist_type_all_builtins ... ok
test review::specialists::tests::test_all_builtin_as_gating ... ok
test review::specialists::tests::test_review_specialist_deserialization_minimal ... ok
test review::specialists::tests::test_specialist_type_display ... ok
test review::specialists::tests::test_specialist_type_display_name ... ok
test review::specialists::tests::test_specialist_type_deserialization_all_formats ... ok
test review::specialists::tests::test_specialist_type_focus_areas_architecture ... ok
test review::specialists::tests::test_specialist_type_deserialization ... ok
test review::specialists::tests::test_specialist_type_focus_areas_custom_empty ... ok
test review::specialists::tests::test_specialist_type_focus_areas_performance ... ok
test review::specialists::tests::test_specialist_type_focus_areas_security ... ok
test review::specialists::tests::test_specialist_type_focus_areas_simplicity ... ok
test review::specialists::tests::test_review_specialist_serialization ... ok
test review::specialists::tests::test_specialist_type_from_str ... ok
test review::specialists::tests::test_specialist_type_is_builtin ... ok
test review::specialists::tests::test_specialist_type_serialization ... ok

test result: ok. 28 passed; 0 failed; 0 ignored; 0 measured; 1248 filtered out; finished in 0.01s
```

> AGENT

All 28 tests pass. Here's a summary of the changes:

### Backend (Rust)

**`src/review/specialists.rs`** — Added two methods to `SpecialistType`:
- `description()` — Returns a detailed description of each agent's role and behavior
- `default_gating()` — Returns whether the agent gates by default (Security Sentinel and Architecture Strategist are gating; Performance Oracle and Simplicity Reviewer are advisory)

**`src/factory/api.rs`** — Added:
- `AgentInfo` response struct with `id`, `name`, `description`, `focus_areas`, `default_gating`
- `GET /api/agents` route and `list_agents` handler that returns all 4 built-in specialists

### Frontend (React)

**`ui/src/types/index.ts`** — Added `'agents'` to `ViewMode` union and `AgentInfo` interface

**`ui/src/api/client.ts`** — Added `listAgents()` API call

**`ui/src/components/StatusBar.tsx`** — Added "agents" toggle button in the view mode bar

**`ui/src/components/Agents.tsx`** — New component showing:
- Header with agent count
- Card grid with each agent featuring:
  - Color-coded left border and icon per agent type
  - Name, agent ID (monospace), and gating/advisory badge
  - Description text
  - Expandable focus areas section (click to toggle)
  - CLI usage hint showing the `forge swarm --review` command

**`ui/src/App.tsx`** — Wired the `Agents` component into the view mode switch

> DEVELOPER

lets commit the changes to a branch and create a PR

> TOOL

tool_use Bash
id: toolu_01UsmdUH6JR2wVvRK7jxdPDa
```json
{
  "command": "git status",
  "description": "Show working tree status"
}
```

> TOOL

tool_result
id: toolu_01UsmdUH6JR2wVvRK7jxdPDa
```
On branch main
Your branch and 'origin/main' have diverged,
and have 18 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/factory/api.rs
	modified:   src/review/specialists.rs
	modified:   ui/src/App.tsx
	modified:   ui/src/api/client.ts
	modified:   ui/src/components/StatusBar.tsx
	modified:   ui/src/types/index.ts

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.entire/
	.forge/factory.db-client_wal_index
	.forge/factory.db-info
	.forge/factory.db-shm
	.forge/factory.db-wal
	AGENTS.md
	ui/.vite/
	ui/src/components/Agents.tsx

no changes added to commit (use "git add" and/or "git commit -a")
```

> TOOL

tool_use Bash
id: toolu_01Cs26Y6DFRgWu5d9yZvRVPB
```json
{
  "command": "git diff",
  "description": "Show staged and unstaged changes"
}
```

> TOOL

tool_result
id: toolu_01Cs26Y6DFRgWu5d9yZvRVPB
```
diff --git a/src/factory/api.rs b/src/factory/api.rs
index 822189e..7f2a1cc 100644
--- a/src/factory/api.rs
+++ b/src/factory/api.rs
@@ -110,6 +110,15 @@ pub struct CliHelpResponse {
     pub options: Vec<CliOption>,
 }
 
+#[derive(serde::Serialize)]
+pub struct AgentInfo {
+    pub id: String,
+    pub name: String,
+    pub description: String,
+    pub focus_areas: Vec<String>,
+    pub default_gating: bool,
+}
+
 // ── Error handling ────────────────────────────────────────────────────
 
 pub enum ApiError {
@@ -218,6 +227,7 @@ pub fn api_router() -> Router<SharedState> {
         .route("/api/github/repos", get(github_list_repos))
         .route("/api/github/disconnect", post(github_disconnect))
         .route("/api/screenshots/{*path}", get(serve_screenshot))
+        .route("/api/agents", get(list_agents))
         .route("/api/cli-help", get(cli_help_handler))
         .route("/api/metrics/summary", get(get_metrics_summary))
         .route("/api/metrics/phases", get(get_metrics_phases))
@@ -376,6 +386,24 @@ async fn detect_github_repo_from_path(path: &str) -> Option<String> {
 
 // ── Handlers ──────────────────────────────────────────────────────────
 
+/// `GET /api/agents` — return the built-in review specialist agents.
+async fn list_agents() -> Json<Vec<AgentInfo>> {
+    use crate::review::SpecialistType;
+
+    let agents = SpecialistType::all_builtins()
+        .into_iter()
+        .map(|st| AgentInfo {
+            id: st.agent_name(),
+            name: st.display_name().to_string(),
+            description: st.description().to_string(),
+            focus_areas: st.focus_areas().into_iter().map(|s| s.to_string()).collect(),
+            default_gating: st.default_gating(),
+        })
+        .collect();
+
+    Json(agents)
+}
+
 /// `GET /api/cli-help` — return parsed CLI help (commands and options).
 ///
 /// Runs `forge --help` once, caches the result, and returns it as JSON.
diff --git a/src/review/specialists.rs b/src/review/specialists.rs
index 749e54f..9c08e65 100644
--- a/src/review/specialists.rs
+++ b/src/review/specialists.rs
@@ -102,6 +102,30 @@ impl SpecialistType {
         }
     }
 
+    /// Get a short description of what this specialist does.
+    pub fn description(&self) -> &str {
+        match self {
+            Self::SecuritySentinel => "Examines code for security vulnerabilities, authentication weaknesses, and data exposure risks. Acts as a gating reviewer — issues must be resolved before a phase can complete.",
+            Self::PerformanceOracle => "Analyzes code for performance bottlenecks, resource inefficiencies, and scalability concerns. Operates in advisory mode — findings are reported but don't block progress.",
+            Self::ArchitectureStrategist => "Reviews structural design decisions, module boundaries, and dependency relationships. Acts as a gating reviewer — architectural issues must be addressed before proceeding.",
+            Self::SimplicityReviewer => "Identifies over-engineering, unnecessary complexity, and YAGNI violations. Operates in advisory mode — encourages simplicity without blocking delivery.",
+            Self::Custom(name) => {
+                // Return static str not possible for dynamic, but we use a fallback
+                let _ = name;
+                "Custom review specialist with user-defined focus areas."
+            }
+        }
+    }
+
+    /// Whether this specialist type gates phase completion by default.
+    pub fn default_gating(&self) -> bool {
+        match self {
+            Self::SecuritySentinel | Self::ArchitectureStrategist => true,
+            Self::PerformanceOracle | Self::SimplicityReviewer => false,
+            Self::Custom(_) => false,
+        }
+    }
+
     /// Get the default focus areas for this specialist type.
     ///
     /// Returns a list of specific concerns this specialist should examine.
diff --git a/ui/src/App.tsx b/ui/src/App.tsx
index 9e55eab..392b470 100644
--- a/ui/src/App.tsx
+++ b/ui/src/App.tsx
@@ -11,6 +11,7 @@ import NewIssueModal from './components/NewIssueModal';
 import ConfirmDialog from './components/ConfirmDialog';
 import { ProjectSetup } from './components/ProjectSetup';
 import Analytics from './components/Analytics';
+import Agents from './components/Agents';
 import { api } from './api/client';
 
 /**
@@ -196,6 +197,10 @@ function MissionControl() {
           <div style={{ flex: 1, overflow: 'hidden' }}>
             <Analytics />
           </div>
+        ) : viewMode === 'agents' ? (
+          <div style={{ flex: 1, overflow: 'hidden' }}>
+            <Agents />
+          </div>
         ) : (
           <div style={{
             flex: 1,
diff --git a/ui/src/api/client.ts b/ui/src/api/client.ts
index cbc3494..191eacb 100644
--- a/ui/src/api/client.ts
+++ b/ui/src/api/client.ts
@@ -95,6 +95,9 @@ export const api = {
       method: 'POST',
     }),
 
+  // Agents
+  listAgents: () => request<import('../types').AgentInfo[]>('/agents'),
+
   // CLI Help
   cliHelp: () => request<import('../types').CliHelpResponse>('/cli-help'),
 };
diff --git a/ui/src/components/StatusBar.tsx b/ui/src/components/StatusBar.tsx
index 8377b4a..442ba47 100644
--- a/ui/src/components/StatusBar.tsx
+++ b/ui/src/components/StatusBar.tsx
@@ -144,6 +144,20 @@ export default function StatusBar({
         >
           analytics
         </button>
+        <button
+          onClick={() => onViewModeChange('agents')}
+          style={{
+            padding: '4px 8px',
+            background: viewMode === 'agents' ? 'var(--color-border)' : 'transparent',
+            border: '1px solid var(--color-border)',
+            color: 'var(--color-text-primary)',
+            cursor: 'pointer',
+            fontSize: '12px',
+          }}
+          title="Review agents"
+        >
+          agents
+        </button>
       </div>
 
       {/* Uptime + WS status */}
diff --git a/ui/src/types/index.ts b/ui/src/types/index.ts
index a92df6d..b297233 100644
--- a/ui/src/types/index.ts
+++ b/ui/src/types/index.ts
@@ -332,7 +332,16 @@ export interface EventLogEntry {
 }
 
 /** View mode for the main agent run grid */
-export type ViewMode = 'grid' | 'list' | 'analytics';
+export type ViewMode = 'grid' | 'list' | 'analytics' | 'agents';
+
+/** A built-in review specialist agent */
+export interface AgentInfo {
+  id: string;
+  name: string;
+  description: string;
+  focus_areas: string[];
+  default_gating: boolean;
+}
 
 /** Status colors mapped to CSS custom property values for the Mission Control theme */
 export const MC_STATUS_COLORS: Record<PipelineStatus, string> = {
```

> TOOL

tool_use Bash
id: toolu_019hDPjcnR7zJzmfX1C6FNZK
```json
{
  "command": "git log --oneline -5",
  "description": "Show recent commits"
}
```

> TOOL

tool_result
id: toolu_019hDPjcnR7zJzmfX1C6FNZK
```
37a9809 docs: add qmd-based context graphs
1ae3070 fix(observability): address PR review findings across telemetry, metrics, and UI
6a6c89d feat(observability): add Analytics view to Factory UI
7a2a13f feat(observability): extract token usage from Claude CLI output
75b6094 chore: update Cargo.lock for tracing dependencies
```

> TOOL

tool_use Bash
id: toolu_01P4jzVTaQgvED6LJ9Cb1EHd
```json
{
  "command": "git checkout -b feat/agents-detail-view",
  "description": "Create feature branch"
}
```

> TOOL

tool_result
id: toolu_01P4jzVTaQgvED6LJ9Cb1EHd
```
Switched to a new branch 'feat/agents-detail-view'
```

> TOOL

tool_use Bash
id: toolu_012sUkUJhXcPXr7hHaTHKJHd
```json
{
  "command": "git add src/review/specialists.rs src/factory/api.rs ui/src/App.tsx ui/src/api/client.ts ui/src/components/StatusBar.tsx ui/src/components/Agents.tsx ui/src/types/index.ts",
  "description": "Stage changed files"
}
```

> TOOL

tool_result
id: toolu_012sUkUJhXcPXr7hHaTHKJHd
```

```

> TOOL

tool_use Bash
id: toolu_01Edz2MHuenccy5qudfzU2W9
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\nfeat(factory): add Agents detail view for built-in review specialists\n\nExposes the 4 embedded review agents (Security Sentinel, Performance Oracle,\nArchitecture Strategist, Simplicity Reviewer) via a new /api/agents endpoint\nand a dedicated \"agents\" view in the Factory UI with expandable detail cards.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>\nEOF\n)\"",
  "description": "Create commit"
}
```

> TOOL

tool_result
id: toolu_01Edz2MHuenccy5qudfzU2W9
```
[feat/agents-detail-view 0b3f9d7] feat(factory): add Agents detail view for built-in review specialists
 7 files changed, 354 insertions(+), 1 deletion(-)
 create mode 100644 ui/src/components/Agents.tsx
```

> TOOL

tool_use Bash
id: toolu_01DQMXSoe94tLZxkBpgeqAfB
```json
{
  "command": "git push -u origin feat/agents-detail-view 2>&1",
  "description": "Push branch to remote"
}
```

> TOOL

tool_result
id: toolu_01DQMXSoe94tLZxkBpgeqAfB
```
[entire] Pushing session logs to origin...
remote: 
remote: Create a pull request for 'feat/agents-detail-view' on GitHub by visiting:        
remote:      https://github.com/jdsingh122918/forge/pull/new/feat/agents-detail-view        
remote: 
remote: GitHub found 1 vulnerability on jdsingh122918/forge's default branch (1 low). To find out more, visit:        
remote:      https://github.com/jdsingh122918/forge/security/dependabot/14        
remote: 
To github.com:jdsingh122918/forge.git
 * [new branch]      feat/agents-detail-view -> feat/agents-detail-view
branch 'feat/agents-detail-view' set up to track 'origin/feat/agents-detail-view'.
```

> TOOL

tool_use Bash
id: toolu_01J7GcFmyxVzmNM98gxMDz3s
```json
{
  "command": "gh pr create --title \"feat(factory): add Agents detail view\" --body \"$(cat <<'EOF'\n## Summary\n- Adds `GET /api/agents` endpoint returning the 4 built-in review specialist agents with their descriptions, focus areas, and gating behavior\n- Adds `description()` and `default_gating()` methods to `SpecialistType` in the review module\n- Introduces a new \"agents\" view mode in the Factory UI with expandable detail cards for each specialist (Security Sentinel, Performance Oracle, Architecture Strategist, Simplicity Reviewer)\n\n## Test plan\n- [x] `cargo build` passes\n- [x] `cargo test --lib -- review::specialists` — all 28 tests pass\n- [x] `npx vite build` — UI builds cleanly\n- [ ] Verify `/api/agents` returns correct JSON with all 4 agents\n- [ ] Click \"agents\" tab in Factory UI and confirm all 4 cards render\n- [ ] Expand each card and verify focus areas and CLI usage hint display correctly\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\"",
  "description": "Create pull request"
}
```

> TOOL

tool_result
id: toolu_01J7GcFmyxVzmNM98gxMDz3s
```
Warning: 8 uncommitted changes
https://github.com/jdsingh122918/forge/pull/17
```

> AGENT

PR created: https://github.com/jdsingh122918/forge/pull/17

> DEVELOPER

Agent default gating metadata disagrees with swarm behavior

This new metadata says Performance Oracle and Simplicity Reviewer are advisory by default, and the Agents screen renders that as the badge/copy. But cmd_swarm still converts every CLI-selected reviewer into DefaultSpecialist::gating(...), so forge swarm --review performance and --review simplicity remain blocking reviews. That means the new screen is currently misleading users about whether a review can fail a phase. Please source this from the same configuration path that builds swarm reviews, or expose the actual CLI/default gating semantics explicitly.

lets review the above assumption/statement using a subagent

> TOOL

tool_use Agent
id: toolu_01GAN9NJv16CZfhPg8HX9PYR
```json
{
  "description": "Verify gating behavior in swarm",
  "prompt": "I need to verify whether there's a disagreement between the new `default_gating()` method on `SpecialistType` and the actual gating behavior when specialists are used via `forge swarm --review`.\n\nThe claim is:\n- The new `SpecialistType::default_gating()` says Performance Oracle and Simplicity Reviewer are advisory (non-gating) by default\n- But `cmd_swarm` (or wherever CLI --review flags are processed) converts every CLI-selected reviewer into gating mode via `ReviewSpecialist::gating(...)`, making them all blocking\n\nPlease investigate thoroughly:\n\n1. Search for `cmd_swarm` or the swarm CLI command handler - look at how `--review` flags are parsed and converted into `ReviewSpecialist` instances. Check if they use `::gating()`, `::advisory()`, or `::new()`.\n\n2. Search for ALL call sites of `ReviewSpecialist::gating`, `ReviewSpecialist::advisory`, `ReviewSpecialist::new`, and `all_builtin_as_gating` across the entire codebase.\n\n3. Check `src/swarm/executor.rs` and `src/swarm/context.rs` for how review specialists are configured and used.\n\n4. Check `src/forge_config.rs` or any config files for how review specialists are configured in forge.toml/phases.json.\n\n5. Look at the swarm prompts (`src/swarm/prompts.rs`) to see if gating behavior is communicated to the agents.\n\n6. Check if there's a `--review-mode` or similar flag that controls gating vs advisory.\n\nReport the EXACT code paths and whether the PR reviewer's claim is correct or not. Include file paths and line numbers.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_01GAN9NJv16CZfhPg8HX9PYR
```
Now let me compile the complete findings. Here's what I found:

## Investigation Summary

The PR reviewer's claim is **CORRECT**. There is indeed a disagreement between the `default_gating()` method and the actual CLI behavior. Here are the exact findings:

### 1. The `default_gating()` Method (Claim A)

**File**: `/Users/jdsingh/Projects/AI/forge/src/review/specialists.rs` (lines 121-127)

```rust
pub fn default_gating(&self) -> bool {
    match self {
        Self::SecuritySentinel | Self::ArchitectureStrategist => true,
        Self::PerformanceOracle | Self::SimplicityReviewer => false,
        Self::Custom(_) => false,
    }
}
```

**What it says:**
- Performance Oracle: advisory (non-gating) by default
- Simplicity Reviewer: advisory (non-gating) by default

---

### 2. The CLI `cmd_swarm` Conversion (The Disagreement)

**File**: `/Users/jdsingh/Projects/AI/forge/src/cmd/swarm.rs` (lines 271-279)

```rust
let review_integration_config = if review_enabled {
    ReviewIntegrationConfig::enabled()
        .with_working_dir(project_dir.to_path_buf())
        .with_default_specialists(
            review_specialists
                .iter()
                .map(|s| DefaultSpecialist::gating(s))  // <-- HERE IS THE PROBLEM
                .collect(),
        )
        .with_verbose(cli.verbose)
} else {
    ReviewIntegrationConfig::default()
};
```

**What it does:**
- Every specialist selected via `--review` flag is explicitly converted to `DefaultSpecialist::gating(s)`
- This means ALL CLI-selected reviewers are forced to be **gating (blocking)**, regardless of their type

### 3. The `DefaultSpecialist::gating()` Method

**File**: `/Users/jdsingh/Projects/AI/forge/src/orchestrator/review_integration.rs` (lines 105-111)

```rust
pub fn gating(name: &str) -> Self {
    Self {
        specialist_type: SpecialistType::from_str(name)
            .unwrap_or_else(|_| SpecialistType::Custom(name.to_string())),
        gate: true,  // <-- ALWAYS SET TO TRUE
    }
}
```

---

### 4. Prompts Communicate Gating Status to Agents

**File**: `/Users/jdsingh/Projects/AI/forge/src/swarm/prompts.rs` (lines 180-186)

```rust
if specialist.gate {
    prompt.push_str(
        "**This is a GATING review.** Phase cannot proceed until issues are resolved.\n\n",
    );
} else {
    prompt.push_str("This is a non-gating review. Issues are advisory only.\n\n");
}
```

The prompts correctly communicate whether a review is gating or advisory to the agents. So agents will be told that Performance Oracle and Simplicity Reviewer are "gating" reviews, contradicting the intent of `default_gating()`.

---

### 5. Other Call Sites

All other call sites of `ReviewSpecialist::gating()` and `ReviewSpecialist::advisory()` are in:
- Test code in `src/review/specialists.rs` (tests 733-796)
- Test code in `src/review/dispatcher.rs`
- Test code in `src/orchestrator/review_integration.rs` (tests 319, 341, etc.)
- Documentation examples

The ONLY production use of `.gating()` conversion in the main code path is in `cmd_swarm` at line 277 of `src/cmd/swarm.rs`.

---

### Summary of the Bug

When users run `forge swarm --review security,performance,simplicity`, the CLI:
1. Parses the specialist names (lines 243 in cmd/swarm.rs)
2. **Forces all of them to gating mode** (line 277: `.map(|s| DefaultSpecialist::gating(s))`)
3. This contradicts `SpecialistType::default_gating()` which says Performance Oracle and Simplicity Reviewer should be advisory

**Result**: Performance Oracle and Simplicity Reviewer will block phase completion when selected via CLI, even though `default_gating()` declares they should be advisory. The agents will be told these are "GATING reviews" per the prompts.

**The issue**: The CLI should respect `default_gating()` and create specialists with their appropriate gating status, not force all to gating mode.
agentId: a068b3d30d925cc22 (for resuming to continue this agent's work if needed)
<usage>total_tokens: 86828
tool_uses: 24
duration_ms: 72369</usage>
```

> AGENT

The reviewer's claim is **confirmed correct**. Here's the issue:

### The Disagreement

| | `default_gating()` says | CLI actually does |
|---|---|---|
| Security Sentinel | gating | gating |
| Performance Oracle | **advisory** | **gating** |
| Architecture Strategist | gating | gating |
| Simplicity Reviewer | **advisory** | **gating** |

### Root Cause

In `src/cmd/swarm.rs:277`, every CLI-selected reviewer is forced to gating:
```rust
.map(|s| DefaultSpecialist::gating(s))  // all become gating regardless
```

This means `forge swarm --review performance` creates a **blocking** review, but the new Agents UI shows Performance Oracle as "advisory" — misleading users.

### Options to Fix

1. **Fix the CLI** — use `default_gating()` when constructing specialists from CLI flags (so Performance Oracle and Simplicity Reviewer become advisory as intended)
2. **Fix the metadata** — change `default_gating()` to return `true` for all, matching the current CLI behavior
3. **Show both** — the UI could show "default: advisory, CLI override: gating" or clarify that CLI always forces gating

Which approach would you prefer?

> DEVELOPER

lets have the UI show both

> AGENT

Let me read the current state of the files I need to change.

> TOOL

tool_use Read
id: toolu_01GzgJ6SmUUotSD3MQTZPi2v
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "offset": 111,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01GzgJ6SmUUotSD3MQTZPi2v
```
   111→}
   112→
   113→#[derive(serde::Serialize)]
   114→pub struct AgentInfo {
   115→    pub id: String,
   116→    pub name: String,
   117→    pub description: String,
   118→    pub focus_areas: Vec<String>,
   119→    pub default_gating: bool,
   120→}
   121→
   122→// ── Error handling ────────────────────────────────────────────────────
   123→
   124→pub enum ApiError {
   125→    NotFound(String),
```

> TOOL

tool_use Read
id: toolu_01CEYUp9GYhLomXAAPNhtnxA
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts",
  "offset": 335,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01CEYUp9GYhLomXAAPNhtnxA
```
   335→export type ViewMode = 'grid' | 'list' | 'analytics' | 'agents';
   336→
   337→/** A built-in review specialist agent */
   338→export interface AgentInfo {
   339→  id: string;
   340→  name: string;
   341→  description: string;
   342→  focus_areas: string[];
   343→  default_gating: boolean;
   344→}
   345→
   346→/** Status colors mapped to CSS custom property values for the Mission Control theme */
   347→export const MC_STATUS_COLORS: Record<PipelineStatus, string> = {
   348→  running: 'var(--color-success)',
   349→  queued: 'var(--color-warning)',
```

> TOOL

tool_use Read
id: toolu_01Uxy7BLQLgqEhaLuyDHDqQb
```json
{
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx"
}
```

> TOOL

tool_result
id: toolu_01Uxy7BLQLgqEhaLuyDHDqQb
```
     1→/** Agents view — displays the 4 built-in review specialist agents with their details. */
     2→import { useState, useEffect, useCallback } from 'react';
     3→import type { AgentInfo } from '../types';
     4→import { api } from '../api/client';
     5→
     6→/** Icon + color mapping per agent */
     7→const AGENT_THEME: Record<string, { icon: string; color: string; bgGlow: string }> = {
     8→  'security-sentinel': {
     9→    icon: '\u{1F6E1}',
    10→    color: '#f85149',
    11→    bgGlow: 'rgba(248, 81, 73, 0.08)',
    12→  },
    13→  'performance-oracle': {
    14→    icon: '\u{26A1}',
    15→    color: '#d29922',
    16→    bgGlow: 'rgba(210, 153, 34, 0.08)',
    17→  },
    18→  'architecture-strategist': {
    19→    icon: '\u{1F3D7}',
    20→    color: '#58a6ff',
    21→    bgGlow: 'rgba(88, 166, 255, 0.08)',
    22→  },
    23→  'simplicity-reviewer': {
    24→    icon: '\u{2728}',
    25→    color: '#3fb950',
    26→    bgGlow: 'rgba(63, 185, 80, 0.08)',
    27→  },
    28→};
    29→
    30→const DEFAULT_THEME = { icon: '\u{1F916}', color: 'var(--color-text-secondary)', bgGlow: 'transparent' };
    31→
    32→export default function Agents() {
    33→  const [agents, setAgents] = useState<AgentInfo[]>([]);
    34→  const [loading, setLoading] = useState(true);
    35→  const [error, setError] = useState<string | null>(null);
    36→  const [expandedId, setExpandedId] = useState<string | null>(null);
    37→
    38→  const fetchAgents = useCallback(async () => {
    39→    setLoading(true);
    40→    setError(null);
    41→    try {
    42→      const data = await api.listAgents();
    43→      setAgents(data);
    44→    } catch (err) {
    45→      setError(err instanceof Error ? err.message : 'Failed to load agents');
    46→    } finally {
    47→      setLoading(false);
    48→    }
    49→  }, []);
    50→
    51→  useEffect(() => {
    52→    fetchAgents();
    53→  }, [fetchAgents]);
    54→
    55→  if (loading) {
    56→    return (
    57→      <div style={{
    58→        display: 'flex',
    59→        alignItems: 'center',
    60→        justifyContent: 'center',
    61→        height: '100%',
    62→        color: 'var(--color-text-secondary)',
    63→        fontSize: '13px',
    64→        gap: '8px',
    65→      }}>
    66→        <span className="pulse-dot" style={{
    67→          width: '8px',
    68→          height: '8px',
    69→          borderRadius: '50%',
    70→          backgroundColor: 'var(--color-success)',
    71→        }} />
    72→        Loading agents...
    73→      </div>
    74→    );
    75→  }
    76→
    77→  if (error) {
    78→    return (
    79→      <div style={{
    80→        display: 'flex',
    81→        alignItems: 'center',
    82→        justifyContent: 'center',
    83→        height: '100%',
    84→        color: 'var(--color-error)',
    85→        fontSize: '13px',
    86→      }}>
    87→        Failed to load agents: {error}
    88→      </div>
    89→    );
    90→  }
    91→
    92→  return (
    93→    <div style={{ padding: '16px', overflowY: 'auto', height: '100%' }}>
    94→      {/* Header */}
    95→      <div style={{
    96→        display: 'flex',
    97→        alignItems: 'center',
    98→        justifyContent: 'space-between',
    99→        marginBottom: '16px',
   100→      }}>
   101→        <span style={{
   102→          fontSize: '14px',
   103→          fontWeight: 700,
   104→          color: 'var(--color-text-primary)',
   105→          letterSpacing: '1px',
   106→          textTransform: 'uppercase',
   107→        }}>
   108→          Review Agents
   109→        </span>
   110→        <span style={{
   111→          fontSize: '12px',
   112→          color: 'var(--color-text-secondary)',
   113→        }}>
   114→          {agents.length} built-in specialists
   115→        </span>
   116→      </div>
   117→
   118→      {/* Agent cards */}
   119→      <div style={{
   120→        display: 'grid',
   121→        gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))',
   122→        gap: '16px',
   123→      }}>
   124→        {agents.map(agent => {
   125→          const theme = AGENT_THEME[agent.id] ?? DEFAULT_THEME;
   126→          const isExpanded = expandedId === agent.id;
   127→
   128→          return (
   129→            <div
   130→              key={agent.id}
   131→              onClick={() => setExpandedId(isExpanded ? null : agent.id)}
   132→              style={{
   133→                backgroundColor: isExpanded ? theme.bgGlow : 'var(--color-bg-card)',
   134→                border: `1px solid ${isExpanded ? theme.color : 'var(--color-border)'}`,
   135→                borderLeft: `3px solid ${theme.color}`,
   136→                cursor: 'pointer',
   137→                transition: 'all 0.15s ease',
   138→              }}
   139→            >
   140→              {/* Card header */}
   141→              <div style={{
   142→                display: 'flex',
   143→                alignItems: 'center',
   144→                padding: '16px',
   145→                gap: '12px',
   146→              }}>
   147→                {/* Agent icon */}
   148→                <span style={{ fontSize: '24px', flexShrink: 0 }}>
   149→                  {theme.icon}
   150→                </span>
   151→
   152→                {/* Name + gating badge */}
   153→                <div style={{ flex: 1, minWidth: 0 }}>
   154→                  <div style={{
   155→                    display: 'flex',
   156→                    alignItems: 'center',
   157→                    gap: '8px',
   158→                  }}>
   159→                    <span style={{
   160→                      fontSize: '15px',
   161→                      fontWeight: 700,
   162→                      color: 'var(--color-text-primary)',
   163→                    }}>
   164→                      {agent.name}
   165→                    </span>
   166→                    <span style={{
   167→                      fontSize: '10px',
   168→                      padding: '2px 6px',
   169→                      backgroundColor: agent.default_gating
   170→                        ? 'rgba(248, 81, 73, 0.15)'
   171→                        : 'rgba(63, 185, 80, 0.15)',
   172→                      color: agent.default_gating
   173→                        ? 'var(--color-error)'
   174→                        : 'var(--color-success)',
   175→                      fontWeight: 600,
   176→                      textTransform: 'uppercase',
   177→                      letterSpacing: '0.5px',
   178→                    }}>
   179→                      {agent.default_gating ? 'gating' : 'advisory'}
   180→                    </span>
   181→                  </div>
   182→                  <div style={{
   183→                    fontSize: '11px',
   184→                    color: 'var(--color-text-secondary)',
   185→                    fontFamily: 'monospace',
   186→                    marginTop: '2px',
   187→                  }}>
   188→                    {agent.id}
   189→                  </div>
   190→                </div>
   191→
   192→                {/* Expand chevron */}
   193→                <span style={{
   194→                  color: 'var(--color-text-secondary)',
   195→                  fontSize: '14px',
   196→                  transition: 'transform 0.15s',
   197→                  transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
   198→                  flexShrink: 0,
   199→                }}>
   200→                  ▾
   201→                </span>
   202→              </div>
   203→
   204→              {/* Description */}
   205→              <div style={{
   206→                padding: '0 16px 12px 52px',
   207→                fontSize: '12px',
   208→                color: 'var(--color-text-secondary)',
   209→                lineHeight: '1.5',
   210→              }}>
   211→                {agent.description}
   212→              </div>
   213→
   214→              {/* Expanded: focus areas */}
   215→              {isExpanded && (
   216→                <div style={{
   217→                  padding: '0 16px 16px 52px',
   218→                }}>
   219→                  <div style={{
   220→                    fontSize: '11px',
   221→                    fontWeight: 600,
   222→                    color: 'var(--color-text-secondary)',
   223→                    textTransform: 'uppercase',
   224→                    letterSpacing: '0.5px',
   225→                    marginBottom: '8px',
   226→                  }}>
   227→                    Focus Areas
   228→                  </div>
   229→                  <div style={{
   230→                    display: 'flex',
   231→                    flexWrap: 'wrap',
   232→                    gap: '6px',
   233→                  }}>
   234→                    {agent.focus_areas.map((area, i) => (
   235→                      <span
   236→                        key={i}
   237→                        style={{
   238→                          fontSize: '11px',
   239→                          padding: '3px 8px',
   240→                          backgroundColor: 'var(--color-bg-primary)',
   241→                          border: '1px solid var(--color-border)',
   242→                          color: 'var(--color-text-primary)',
   243→                        }}
   244→                      >
   245→                        {area}
   246→                      </span>
   247→                    ))}
   248→                  </div>
   249→
   250→                  {/* Usage hint */}
   251→                  <div style={{
   252→                    marginTop: '12px',
   253→                    padding: '8px 10px',
   254→                    backgroundColor: 'var(--color-bg-primary)',
   255→                    border: '1px solid var(--color-border)',
   256→                    fontSize: '11px',
   257→                    fontFamily: 'monospace',
   258→                    color: 'var(--color-text-secondary)',
   259→                  }}>
   260→                    <span style={{ color: theme.color }}>$</span> forge swarm --review {agent.id.split('-')[0]}
   261→                  </div>
   262→                </div>
   263→              )}
   264→            </div>
   265→          );
   266→        })}
   267→      </div>
   268→    </div>
   269→  );
   270→}
   271→
```

> AGENT

Now I'll update all three layers — backend struct, TS type, and the UI rendering.

> TOOL

tool_use Edit
id: toolu_0131ScSHLsjMwAahumtqbo43
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "old_string": "#[derive(serde::Serialize)]\npub struct AgentInfo {\n    pub id: String,\n    pub name: String,\n    pub description: String,\n    pub focus_areas: Vec<String>,\n    pub default_gating: bool,\n}",
  "new_string": "#[derive(serde::Serialize)]\npub struct AgentInfo {\n    pub id: String,\n    pub name: String,\n    pub description: String,\n    pub focus_areas: Vec<String>,\n    pub default_gating: bool,\n    /// CLI `forge swarm --review` always forces gating mode regardless of default.\n    pub cli_gating: bool,\n}"
}
```

> TOOL

tool_result
id: toolu_0131ScSHLsjMwAahumtqbo43
```
The file /Users/jdsingh/Projects/AI/forge/src/factory/api.rs has been updated successfully.
```

> AGENT

Now update the handler to populate the new field.

> TOOL

tool_use Grep
id: toolu_01HrkhxScnh4Crs4qRYn7X4y
```json
{
  "pattern": "async fn list_agents",
  "path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "output_mode": "content",
  "-A": 18
}
```

> TOOL

tool_result
id: toolu_01HrkhxScnh4Crs4qRYn7X4y
```
392:async fn list_agents() -> Json<Vec<AgentInfo>> {
393-    use crate::review::SpecialistType;
394-
395-    let agents = SpecialistType::all_builtins()
396-        .into_iter()
397-        .map(|st| AgentInfo {
398-            id: st.agent_name(),
399-            name: st.display_name().to_string(),
400-            description: st.description().to_string(),
401-            focus_areas: st.focus_areas().into_iter().map(|s| s.to_string()).collect(),
402-            default_gating: st.default_gating(),
403-        })
404-        .collect();
405-
406-    Json(agents)
407-}
408-
409-/// `GET /api/cli-help` — return parsed CLI help (commands and options).
410-///
```

> TOOL

tool_use Edit
id: toolu_01GTVxnUspDvK2iUpA3ke5b9
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/src/factory/api.rs",
  "old_string": "        .map(|st| AgentInfo {\n            id: st.agent_name(),\n            name: st.display_name().to_string(),\n            description: st.description().to_string(),\n            focus_areas: st.focus_areas().into_iter().map(|s| s.to_string()).collect(),\n            default_gating: st.default_gating(),\n        })",
  "new_string": "        .map(|st| AgentInfo {\n            id: st.agent_name(),\n            name: st.display_name().to_string(),\n            description: st.description().to_string(),\n            focus_areas: st.focus_areas().into_iter().map(|s| s.to_string()).collect(),\n            default_gating: st.default_gating(),\n            cli_gating: true, // cmd_swarm forces all CLI-selected reviewers to gating\n        })"
}
```

> TOOL

tool_result
id: toolu_01GTVxnUspDvK2iUpA3ke5b9
```
The file /Users/jdsingh/Projects/AI/forge/src/factory/api.rs has been updated successfully.
```

> AGENT

Now update the TS type:

> TOOL

tool_use Edit
id: toolu_01VQ7ANFhaY8MbTMUe9KJw4b
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts",
  "old_string": "/** A built-in review specialist agent */\nexport interface AgentInfo {\n  id: string;\n  name: string;\n  description: string;\n  focus_areas: string[];\n  default_gating: boolean;\n}",
  "new_string": "/** A built-in review specialist agent */\nexport interface AgentInfo {\n  id: string;\n  name: string;\n  description: string;\n  focus_areas: string[];\n  default_gating: boolean;\n  /** CLI `forge swarm --review` always forces gating mode regardless of default. */\n  cli_gating: boolean;\n}"
}
```

> TOOL

tool_result
id: toolu_01VQ7ANFhaY8MbTMUe9KJw4b
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/types/index.ts has been updated successfully.
```

> AGENT

Now update the Agents component to show both semantics:

> TOOL

tool_use Edit
id: toolu_0168uqrzgJ83Q6cxj6HAkZZw
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx",
  "old_string": "                {/* Name + gating badge */}\n                <div style={{ flex: 1, minWidth: 0 }}>\n                  <div style={{\n                    display: 'flex',\n                    alignItems: 'center',\n                    gap: '8px',\n                  }}>\n                    <span style={{\n                      fontSize: '15px',\n                      fontWeight: 700,\n                      color: 'var(--color-text-primary)',\n                    }}>\n                      {agent.name}\n                    </span>\n                    <span style={{\n                      fontSize: '10px',\n                      padding: '2px 6px',\n                      backgroundColor: agent.default_gating\n                        ? 'rgba(248, 81, 73, 0.15)'\n                        : 'rgba(63, 185, 80, 0.15)',\n                      color: agent.default_gating\n                        ? 'var(--color-error)'\n                        : 'var(--color-success)',\n                      fontWeight: 600,\n                      textTransform: 'uppercase',\n                      letterSpacing: '0.5px',\n                    }}>\n                      {agent.default_gating ? 'gating' : 'advisory'}\n                    </span>\n                  </div>\n                  <div style={{\n                    fontSize: '11px',\n                    color: 'var(--color-text-secondary)',\n                    fontFamily: 'monospace',\n                    marginTop: '2px',\n                  }}>\n                    {agent.id}\n                  </div>\n                </div>",
  "new_string": "                {/* Name + gating badges */}\n                <div style={{ flex: 1, minWidth: 0 }}>\n                  <div style={{\n                    display: 'flex',\n                    alignItems: 'center',\n                    gap: '8px',\n                    flexWrap: 'wrap',\n                  }}>\n                    <span style={{\n                      fontSize: '15px',\n                      fontWeight: 700,\n                      color: 'var(--color-text-primary)',\n                    }}>\n                      {agent.name}\n                    </span>\n                    <span style={{\n                      fontSize: '10px',\n                      padding: '2px 6px',\n                      backgroundColor: agent.default_gating\n                        ? 'rgba(248, 81, 73, 0.15)'\n                        : 'rgba(63, 185, 80, 0.15)',\n                      color: agent.default_gating\n                        ? 'var(--color-error)'\n                        : 'var(--color-success)',\n                      fontWeight: 600,\n                      textTransform: 'uppercase',\n                      letterSpacing: '0.5px',\n                    }}>\n                      {agent.default_gating ? 'gating' : 'advisory'}\n                    </span>\n                    {agent.cli_gating && !agent.default_gating && (\n                      <span style={{\n                        fontSize: '10px',\n                        padding: '2px 6px',\n                        backgroundColor: 'rgba(210, 153, 34, 0.15)',\n                        color: 'var(--color-warning)',\n                        fontWeight: 600,\n                        textTransform: 'uppercase',\n                        letterSpacing: '0.5px',\n                      }}>\n                        cli: gating\n                      </span>\n                    )}\n                  </div>\n                  <div style={{\n                    fontSize: '11px',\n                    color: 'var(--color-text-secondary)',\n                    fontFamily: 'monospace',\n                    marginTop: '2px',\n                  }}>\n                    {agent.id}\n                  </div>\n                </div>"
}
```

> TOOL

tool_result
id: toolu_0168uqrzgJ83Q6cxj6HAkZZw
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx has been updated successfully.
```

> AGENT

Now add a note in the expanded section explaining the CLI override:

> TOOL

tool_use Edit
id: toolu_01QrUDrDT6hzE4aGzWpQtHCW
```json
{
  "replace_all": false,
  "file_path": "/Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx",
  "old_string": "                  {/* Usage hint */}\n                  <div style={{\n                    marginTop: '12px',\n                    padding: '8px 10px',\n                    backgroundColor: 'var(--color-bg-primary)',\n                    border: '1px solid var(--color-border)',\n                    fontSize: '11px',\n                    fontFamily: 'monospace',\n                    color: 'var(--color-text-secondary)',\n                  }}>\n                    <span style={{ color: theme.color }}>$</span> forge swarm --review {agent.id.split('-')[0]}\n                  </div>",
  "new_string": "                  {/* CLI override note */}\n                  {agent.cli_gating && !agent.default_gating && (\n                    <div style={{\n                      marginTop: '12px',\n                      padding: '8px 10px',\n                      backgroundColor: 'rgba(210, 153, 34, 0.06)',\n                      border: '1px solid rgba(210, 153, 34, 0.25)',\n                      fontSize: '11px',\n                      color: 'var(--color-warning)',\n                      lineHeight: '1.5',\n                    }}>\n                      Advisory by default, but <span style={{ fontWeight: 600 }}>forge swarm --review</span> forces\n                      all selected reviewers to gating mode. Findings will block phase completion when invoked via CLI.\n                    </div>\n                  )}\n\n                  {/* Usage hint */}\n                  <div style={{\n                    marginTop: '12px',\n                    padding: '8px 10px',\n                    backgroundColor: 'var(--color-bg-primary)',\n                    border: '1px solid var(--color-border)',\n                    fontSize: '11px',\n                    fontFamily: 'monospace',\n                    color: 'var(--color-text-secondary)',\n                  }}>\n                    <span style={{ color: theme.color }}>$</span> forge swarm --review {agent.id.split('-')[0]}\n                  </div>"
}
```

> TOOL

tool_result
id: toolu_01QrUDrDT6hzE4aGzWpQtHCW
```
The file /Users/jdsingh/Projects/AI/forge/ui/src/components/Agents.tsx has been updated successfully.
```

> AGENT

Now build both to verify:

> TOOL

tool_use Bash
id: toolu_011gLjfjBC83V6eeC44EZ9TB
```json
{
  "command": "cargo build 2>&1 | tail -5",
  "description": "Build Rust backend",
  "timeout": 120000
}
```

> TOOL

tool_use Bash
id: toolu_01VWD8g9hsS6NoY5wyBRhVn6
```json
{
  "command": "cd /Users/jdsingh/Projects/AI/forge/ui && npx vite build 2>&1 | tail -10",
  "description": "Build UI frontend",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_011gLjfjBC83V6eeC44EZ9TB
```
   Compiling forge v0.1.0 (/Users/jdsingh/Projects/AI/forge)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.55s
```

> TOOL

tool_result
id: toolu_01VWD8g9hsS6NoY5wyBRhVn6
```
vite v7.3.1 building client environment for production...
transforming...
✓ 43 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.73 kB │ gzip:  0.41 kB
dist/assets/index-ChFHATW8.css   20.44 kB │ gzip:  4.79 kB
dist/assets/index-CdmFS4QW.js   263.96 kB │ gzip: 76.97 kB
✓ built in 390ms
```

> AGENT

Both build clean. Now commit and push:

> TOOL

tool_use Bash
id: toolu_014gd7avtY6xGzekyDnjHd8i
```json
{
  "command": "git diff --stat",
  "description": "Show changed files"
}
```

> TOOL

tool_result
id: toolu_014gd7avtY6xGzekyDnjHd8i
```
 src/factory/api.rs           |  3 +++
 ui/src/components/Agents.tsx | 32 +++++++++++++++++++++++++++++++-
 ui/src/types/index.ts        |  2 ++
 3 files changed, 36 insertions(+), 1 deletion(-)
```

> TOOL

tool_use Bash
id: toolu_01YLUn6wrFWcMwFo9YEcmbVt
```json
{
  "command": "git add src/factory/api.rs ui/src/components/Agents.tsx ui/src/types/index.ts",
  "description": "Stage changed files"
}
```

> TOOL

tool_result ERROR
id: toolu_01YLUn6wrFWcMwFo9YEcmbVt
```
Exit code 128
fatal: pathspec 'src/factory/api.rs' did not match any files
```

> TOOL

tool_use Bash
id: toolu_012W5KhDUMvRsGoQYr4sS5Gr
```json
{
  "command": "pwd && git branch",
  "description": "Check working directory and branch"
}
```

> TOOL

tool_result
id: toolu_012W5KhDUMvRsGoQYr4sS5Gr
```
/Users/jdsingh/Projects/AI/forge/ui
  entire/00c0ad7-e3b0c4
  entire/00efa63-e3b0c4
  entire/04ff730-e3b0c4
  entire/06cd7fe-e3b0c4
  entire/0b3f9d7-e3b0c4
  entire/0c90928-e3b0c4
  entire/25deb65-e3b0c4
  entire/37a9809-e3b0c4
  entire/412828b-e3b0c4
  entire/475287a-e3b0c4
  entire/4bdfafc-e3b0c4
  entire/534c2a8-e3b0c4
  entire/55f05b4-e3b0c4
  entire/64232d5-e3b0c4
  entire/75081e9-e3b0c4
  entire/7692201-e3b0c4
  entire/8099da5-e3b0c4
  entire/837972a-e3b0c4
  entire/8c8ad45-e3b0c4
  entire/931a5a8-e3b0c4
  entire/c070cf8-e3b0c4
  entire/c0cc67c-e3b0c4
  entire/c17ca8f-e3b0c4
  entire/c6efb16-e3b0c4
  entire/ca722eb-e3b0c4
  entire/checkpoints/v1
  entire/d9fcb61-e3b0c4
  entire/e71c83c-e3b0c4
  entire/ea160b3-e3b0c4
  entire/f571c0f-e3b0c4
  entire/f71e2bf-e3b0c4
* feat/agents-detail-view
  fix/backend-frontend-gap-bridging
  main
```

> AGENT

The vite build `cd` left me in the `ui/` directory.

> TOOL

tool_use Bash
id: toolu_01JPYFqfui4GPipMNYuSk8PD
```json
{
  "command": "cd /Users/jdsingh/Projects/AI/forge && git add src/factory/api.rs ui/src/components/Agents.tsx ui/src/types/index.ts",
  "description": "Stage changed files from project root"
}
```

> TOOL

tool_result
id: toolu_01JPYFqfui4GPipMNYuSk8PD
```

```

> TOOL

tool_use Bash
id: toolu_01125HgP3W1DH2kCwdTznoRn
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\nfix(agents): surface CLI gating override in agent detail view\n\nThe CLI `forge swarm --review` forces all reviewers to gating mode,\nbut default_gating marked Performance Oracle and Simplicity Reviewer\nas advisory. Now the API returns a cli_gating field, and the UI shows\na \"CLI: GATING\" badge plus an explanatory note for affected agents.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>\nEOF\n)\"",
  "description": "Commit the fix"
}
```

> TOOL

tool_result
id: toolu_01125HgP3W1DH2kCwdTznoRn
```
[feat/agents-detail-view 30e95c3] fix(agents): surface CLI gating override in agent detail view
 3 files changed, 36 insertions(+), 1 deletion(-)
```

> TOOL

tool_use Bash
id: toolu_015XaF8FZaF2aMovZMxNaTPC
```json
{
  "command": "git push 2>&1",
  "description": "Push to remote"
}
```

> TOOL

tool_result
id: toolu_015XaF8FZaF2aMovZMxNaTPC
```
[entire] Pushing session logs to origin...
remote: 
remote: GitHub found 1 vulnerability on jdsingh122918/forge's default branch (1 low). To find out more, visit:        
remote:      https://github.com/jdsingh122918/forge/security/dependabot/14        
remote: 
To github.com:jdsingh122918/forge.git
   0b3f9d7..30e95c3  feat/agents-detail-view -> feat/agents-detail-view
```

> AGENT

Pushed. The PR at https://github.com/jdsingh122918/forge/pull/17 now has the fix.

Here's what changed:

- **`AgentInfo`** (backend + TS type): added `cli_gating: bool` — always `true` because `cmd_swarm` forces all CLI-selected reviewers to gating mode
- **Agents UI**: For agents where `default_gating` is false but `cli_gating` is true (Performance Oracle, Simplicity Reviewer):
  - A warning-colored **"CLI: GATING"** badge appears next to the existing "advisory" badge in the card header
  - An explanatory callout in the expanded section explains that `forge swarm --review` forces gating mode and findings will block phase completion
