> DEVELOPER

give me the description

> AGENT

Let me get the PR description for the current branch.

> TOOL

tool_use Bash
id: toolu_0189bLwB6p7CyKcpg3RLo5R3
```json
{
  "command": "gh pr view --json title,body,number,state --jq '\"\\(.number): \\(.title)\\nState: \\(.state)\\n\\n\\(.body)\"'",
  "description": "Get PR description for current branch"
}
```

> TOOL

tool_result ERROR
id: toolu_0189bLwB6p7CyKcpg3RLo5R3
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.
```