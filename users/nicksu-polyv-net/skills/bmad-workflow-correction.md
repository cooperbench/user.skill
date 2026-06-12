---
name: bmad-workflow-correction
description: Trigger — agent deviated from the BMAD pipeline (skipped workflow.xml load, ran steps out of order, or didn't embody the required persona). Nick pastes the full <steps CRITICAL="TRUE"> XML blob verbatim to force compliance.
---

When the agent does not follow the BMAD workflow correctly, Nick does not explain what went wrong. He pastes a fixed XML block containing:
1. A `<steps CRITICAL="TRUE">` wrapper
2. Four numbered steps: load `workflow.xml`, read it fully, pass the specific `workflow.yaml` path as `workflow-config`, follow instructions exactly, save outputs after each section
3. An ARGUMENTS line with the story ID and optional `yolo` flag

This is never composed fresh — it is a copy-paste from a BMAD template with only the `workflow-config` path swapped.

**Example 1** (create-story workflow, arguments: 7.9 yolo):
```
IT IS CRITICAL THAT YOU FOLLOW THESE STEPS - while staying in character as the current agent persona you may have loaded:

<steps CRITICAL="TRUE">
1. Always LOAD the FULL @{project-root}/_bmad/core/tasks/workflow.xml
2. READ its entire contents - this is the CORE OS for EXECUTING the specific workflow-config @{project-root}/_bmad/bmm/workflows/4-implementation/create-story/workflow.yaml
3. Pass the yaml path @{project-root}/_bmad/bmm/workflows/4-implementation/create-story/workflow.yaml as 'workflow-config' parameter to the workflow.xml instructions
4. Follow workflow.xml instructions EXACTLY as written to process and follow the specific workflow config and its instructions
5. Save outputs after EACH section when generating any documents from templates
</steps>


ARGUMENTS: 7.9 yolo
```

**Example 2** (automate workflow, no arguments):
```
IT IS CRITICAL THAT YOU FOLLOW THESE STEPS - while staying in character as the current agent persona you may have loaded:

<steps CRITICAL="TRUE">
1. Always LOAD the FULL @{project-root}/_bmad/core/tasks/workflow.xml
2. READ its entire contents - this is the CORE OS for EXECUTING the specific workflow-config @{project-root}/_bmad/tea/workflows/testarch/automate/workflow.yaml
3. Pass the yaml path @{project-root}/_bmad/tea/workflows/testarch/automate/workflow.yaml as 'workflow-config' parameter to the workflow.xml instructions
4. Follow workflow.xml instructions EXACTLY as written to process and follow the specific workflow config and its instructions
5. Save outputs after EACH section when generating any documents from templates
</steps>
```

The same block may be sent twice in a row if the agent still does not comply after the first paste.
