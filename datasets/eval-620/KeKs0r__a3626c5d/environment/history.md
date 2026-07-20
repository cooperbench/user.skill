> SYSTEM

<system_instruction> You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel. Your work should take place in the /home/<USER>/conductor/workspaces/rudel/tunis-v1 directory (unless otherwise directed), which has been set up for you to work in. Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents. The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise. If the user asks you to work on several unrelated tasks in parallel, you can suggest they start new workspaces. If the user asks for help with Conductor, ask them to email [<REDACTED_EMAIL>](mailto:<REDACTED_EMAIL>) or click on the comment icon in the bottom left to send feedback. </system_instruction> add a hint to the readme, which information we are currently collecting: ``` ● Session ID & timestamps (start, last interaction) ● User ID & organization ID ● Project path & package name ● Git context (repository, branch, SHA, remote) ● Session transcript (full prompt & response content) ● Sub-agent usage ```

> AGENT

Let me find the README file first.

> AGENT

Done. Added a "What Data Is Collected" section to the README between "How It Works" and "Development".