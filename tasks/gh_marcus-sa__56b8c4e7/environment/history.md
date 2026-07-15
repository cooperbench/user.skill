> SYSTEM

<system_instruction>
You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel.
Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/munich-v2 directory (unless otherwise directed), which has been set up for you to work in.
Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents.
The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise.

By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default.

If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces.
Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. 
If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team.
</system_instruction>

/nw-bugfix  shadcn ui […]

> TOOL

tool_use Skill
id: toolu_01R4CDXtyYzD8agiRcdi5Uz6
```json
{
  "skill": "nw-bugfix",
  "args": "shadcn ui select component usage - all options are displaying the value instead of the label"
}
```

> TOOL

tool_result
id: toolu_01R4CDXtyYzD8agiRcdi5Uz6
```
Launching skill: nw-bugfix
```

> AGENT

Starting Phase 1: Root Cause Analysis for the Select component bug.

> TOOL

tool_use Agent
id: toolu_01AUp7GUV9kMCoGBfEgrizZ3
```json
{
  "subagent_type": "nw-troubleshooter",
  "description": "RCA: Select shows value not label",
  "prompt": "Execute *investigate-root-cause for the following defect:\n\n**Bug**: shadcn UI Select component usage - all options are displaying the value instead of the label\n\n**Context**: This is in a Brain project (TypeScript, React frontend). The agent picker dropdown was recently added to `AgentStatusSection.tsx` for selecting which agent to assign to a task. The Select component likely shows agent IDs (values) instead of agent names (labels) in the dropdown options.\n\nConfiguration:\n- investigation_depth: 5\n- multi_causal: true\n- evidence_required: true\n\nProduce:\n1. Root cause chain (5 Whys with evidence at each level)\n2. Contributing factors\n3. Proposed fix with specific code changes\n4. Files affected\n5. Risk assessment of the fix\n\nFocus on:\n- `app/src/client/components/graph/AgentStatusSection.tsx` - the component with the Select\n- How shadcn Select components work (SelectItem value vs children)\n- The agent data structure being mapped to Select options\n\nDo NOT make any code changes. Research only."
}
```

> TOOL

tool_result
id: toolu_01AUp7GUV9kMCoGBfEgrizZ3
```
All evidence gathered. Here is the complete Root Cause Analysis.

---

## Root Cause Analysis: shadcn Select Displays Values Instead of Labels

### Problem Statement

The agent picker dropdown in `AgentStatusSection.tsx` displays agent IDs (raw UUID values) instead of agent display names in the trigger area after selection. The dropdown options themselves render correctly (showing `{agent.name} ({agent.runtime})`), but once an option is selected, the trigger shows the raw `agent.id` string.

### Scope

- **Affected component**: `AgentStatusSection.tsx` lines 322-333
- **Affected UI**: Agent picker Select trigger text after selection
- **Not affected**: Dropdown option list (options render children correctly via `SelectItemText`)

---

### 5 Whys Analysis

**PROBLEM**: After selecting an agent from the dropdown, the trigger displays the agent's UUID (`agent.id`) instead of the agent's name.

---

**WHY 1A (Symptom)**: The `<SelectValue>` component renders the raw `value` string (the agent ID) as its display text.

**Evidence**: In `SelectValue.js` (line 51), when no `childrenProp` function, no `childrenProp` node, and no `placeholder` applies, the code falls through to:
```js
children = resolveSelectedLabel(value, items, itemToStringLabel);
```
The `value` here is the string passed to `<Select.Item value={agent.id}>` -- i.e., a UUID string.

---

**WHY 2A (Context)**: `resolveSelectedLabel()` has no `items` map […]

> AGENT

## Phase 1: Root Cause Analysis Complete

### Root Cause

The `Select` component in `AgentStatusSection.tsx` uses `@base-ui/react/select` (wrapped by shadcn), **not** Radix UI's Select. Base UI requires an explicit `items` prop on `Select.Root` for `SelectValue` to display labels. Without it, `SelectValue` falls back to rendering the raw `value` string (the agent UUID).

The shadcn wrapper hides this requirement behind a Radix-like API, creating a trap where correct-looking code produces wrong output.

### Evidence Chain

1. `SelectValue` calls `resolveSelectedLabel(value, items, itemToStringLabel)`
2. No `items` prop passed → all lookup branches skipped
3. Falls through to `serializeValue(value)` → returns the UUID string as-is
4. Dropdown options render correctly (via `SelectItemText` inside the popup) — it's only the trigger display that's broken

### Proposed Fix (Option 1 — recommended, minimal)

Pass an `items` record mapping agent IDs to display labels on the `<Select>` root:

```tsx
<Select
  value={selectedAgentId ?? ""}
  onValueChange={(v) => setSelectedAgentId(v ?? undefined)}
  items={Object.fromEntries(
    assignableAgents.map((agent) => [agent.id, `${agent.name} (${agent.runtime})`])
  )}
>
```

### Files Affected

- `app/src/client/components/graph/AgentStatusSection.tsx` (lines ~322-333)

### Risk: Low

Single component change using a documented Base UI API. No regression risk to other components.

---

**Does this root cause match your understanding? Do you approve the proposed fix direction?** […]