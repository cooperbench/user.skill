> SYSTEM

<system_instruction> You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel. Your work should take place in the /Users/fcamblor/conductor/workspaces/mac-ai-trackers/port-louis directory (unless otherwise directed), which has been set up for you to work in. Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents. The target branch for this workspace is origin/main. Use this for actions like diffing (`git diff origin/main...`) or creating PRs (`gh pr create --base main`). Do not rename the current branch unless the user explicitly tells you to do so. By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default. If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces. Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. If the user asks for help with Conductor, you can ask them […]

> AGENT

Le cas "0 entrée" est déjà géré ligne 189-192 mais avec un message minimal. Je l'enrichis pour mentionner le scénario UI (Cowork, Claude Desktop, Claude Chat) qui nécessite de se connecter au moins une fois via la CLI.

> AGENT

Modification ciblée : j'ai enrichi le sous-titre du badge "No Keychain entry found" dans `AssistantsSettingsView.swift:189-196` (rendu après un scan ne retournant aucune entrée) pour préciser que les utilisateurs de Claude via UI uniquement (Cowork, Claude Code Desktop, Claude Chat…) doivent se connecter au moins une fois via la CLI `claude` afin que les credentials soient écrits dans le Keychain — seul endroit où l'app peut les lire. Aucune action n'est ajoutée, c'est purement descriptif comme demandé.