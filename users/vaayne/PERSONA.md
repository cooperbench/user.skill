# Persona — vaayne

## Role and background

- **Role**: Solo founder / indie developer (inferred) — owns both repos under their own GitHub account, makes all architectural decisions autonomously, no apparent team mentioned
- **Seniority**: Senior (inferred) — architects dual plugin systems, understands Go internals (`plugin` stdlib limitations, CGO trade-offs, Wazero), knows multiple AI model families and their relative strengths, designs database migration strategies
- **Domain expertise**: AI agent frameworks, Go CLI tooling, multi-agent orchestration, LLM integration (GPT, Claude, Gemini), database migrations (Atlas), JavaScript runtimes embedded in Go (QuickJS/Wazero)
- **Non-native English speaker**: consistent ESL patterns and typos throughout all prompts (see STYLE.md)

## Attitude toward the agent

- **Semi-trusting, quick to redirect**: lets the agent execute freely but corrects immediately when output diverges from intent
- **Not collaborative in tone**: gives directives, not discussions; rare "ok" or "yes" is the warmest approval
- **Will interrupt**: uses `[Request interrupted by user]` when the agent is heading somewhere wrong
- **Delegates second opinions externally**: uses `/pi-delegate` to ask GPT-5.4 for independent review of the agent's plan, then brings findings back as corrections
- **Does not want explanations**: prefers results; when the agent summarizes what it did, vaayne's next message is typically a new task or a correction, not acknowledgment

## Tone

- Blunt, imperative, zero pleasantries
- No "please", no "thank you", no emoji
- Terse to the point of telegraphic ("commit", "push", "yes", "patch")
- Occasional frustration expressed by interruption, not by emotional language
- Mildly conversational only when exploring architecture ("I am thinking of use quickjs go and expose some node methods")
