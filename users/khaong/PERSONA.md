# Persona: khaong

## Role and Seniority (inferred)

Technical founder or principal engineer (inferred) — likely building Entire as a product, not just a personal tool. Owns the architecture: decides what goes into Linear, what lands in a PR, what gets brainstormed vs. spec'd vs. built. References a teammate ("soph") with stacked PRs, suggesting a small team. Operates across design, implementation, debugging, and review, all in the same session.

Go is the primary language (entireio/cli is Go). Comfortable at a depth where they can spot a go-git v5 index-write side-effect bug, challenge an agent's call-chain analysis ("are you sure?"), and distinguish between "stop hook caused the corruption" vs. "stop hook exposed it."

## Attitude Toward the Agent

**Trusting but skeptical.** Lets the agent write ~78% of code and run long autonomous stretches, but does not accept agent reasoning at face value. Common pattern: agent gives a confident explanation → khaong asks one targeted question that reveals the agent missed a constraint or assumed the wrong scope. Not hostile — just technically precise.

**Collaborative, not deferential.** Uses "let's" constantly, treating the agent as a pair partner, not a tool. But "let's" means "do it the way I'd do it if I had time," not "surprise me."

**Comfortable interrupting.** Uses `[Request interrupted by user]` and takeover moves ("I've done it on my end. let's switch back across now") without apology.

## Domains

- Git internals: worktrees, index files, pack objects, GC, go-git v5 bugs
- CI/CD: GitHub Actions, E2E test suites, artifact capture
- Developer tooling: Claude Code hooks, Gemini CLI hooks, session lifecycle management
- Linear for project management (ENT-XXX issue references throughout)
- TDD, state machines, hook-based architectures

## Tone

Casual, British/Australian register. Uses "feck," "HALP," "yuck," "blatted," "hmm," "nah," "oh." Emoticons used sparingly and meaningfully: "😬" = concern/warning, ":|" = skepticism/mild frustration, "😭" = genuine pain, ":(" = something broke. Swearing is light and typographical ("feck," not worse).

## Known Collaborators

- **soph** — teammate with stacked PRs and design opinions (#37, ENT-109 area)
- **alex** — branch naming convention ("alex/ent-221-..."), local workspace paths (`/Users/alex/workspace/cli`) — likely khaong's own username on the dev machine (inferred)
