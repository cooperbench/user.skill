---
name: allcaps-command-override
description: >
  Trigger: agent ignored a workflow command invocation, responded to a
  /slash-command with a menu or question instead of loading and executing
  the full workflow file, or drifted from the BMAD protocol.
---

When the BMAD agent fails to honor a workflow command, Armel escalates with an ALL CAPS
imperative. He quotes the exact path to the workflow file and demands it be loaded in full.
This is his strongest correction signal — it means the agent has fundamentally missed the
instruction and must reset.

The format is always: `IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL <path>, READ its entire contents and follow its directions exactly!`

The path uses `{project-root}` BMAD variable syntax.

## Examples

**Edit-module workflow override:**
> "IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL {project-root}/_bmad/bmb/workflows/module/workflow-edit-module.md, READ its entire contents and follow its directions exactly!"

**Party-mode workflow override:**
> "IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL {project-root}/_bmad/core/workflows/party-mode/workflow.md, READ its entire contents and follow its directions exactly!"

**Context**: These appear after the agent has already shown a menu or responded with a question
when a slash-command was expected to trigger a full workflow load. The override is not
aggressive in tone toward the agent — it is a system-level instruction reset.
