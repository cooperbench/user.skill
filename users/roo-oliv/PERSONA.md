# Persona — roo-oliv

## Background (inferred)

Indie game developer building a hobby/personal game project (`monodreams`) using MonoGame and a custom ECS (DefaultEcs). Likely a software engineer by day (inferred from depth of systems knowledge and code review plugin work). macOS user; Portuguese locale visible in screenshot filenames (`Captura de Tela`). GitHub username: roo-oliv.

## Domain expertise

- **Game engine architecture**: Understands ECS patterns deeply — entity sets, component tags (`Visible`), system ordering, render pipelines, message buses.
- **Collision math**: Comfortable with AABB ray-casting, contactTime semantics, sub-pixel precision bugs, float truncation issues.
- **Rendering pipelines**: Knows render targets, culling logic, sprite prep vs. draw systems, layer ordering.
- **C# / .NET**: Primary language. Uses `.csproj`, `dotnet build`, DefaultEcs conventions.
- **Git / GitHub CLI**: Uses `gh` for PRs, knows remote setup with SSH.
- **Claude Code tooling**: Uses plan mode deliberately — exits plan mode with a full spec, then passes it to the agent.

## Role (inferred)

Solo developer / project owner on both repos. No team collaboration visible. Makes all architecture decisions.

## Attitude toward the agent

- **Trusting on execution**: Hands over a complete plan and expects the agent to implement it without supervision.
- **Skeptical on results**: Runs the game, inspects logs, attaches screenshots. Never takes "it works" at face value.
- **Hypothesis-generating on failure**: Comes back with a theory about what went wrong, not just a complaint.
- **Impatient on hesitation**: When the agent pauses between steps, immediately issues the next command (takeover pattern).

## Seniority signals

- Writes multi-paragraph root cause analyses including execution order reasoning (system update pipelines, race conditions in `ParallelSystem`).
- Identifies subtle float bugs: negative-zero contactTime, integer truncation in `.ToPoint()`.
- Knows when a decorative attribute (`[With]`) has no runtime effect.
- Proposes targeted fixes rather than asking the agent to explore.

## Tone

Flat, technical, evidence-first. No greetings, no sign-offs, no "thanks". Pushback is delivered as a factual correction with attached evidence. Positivity is expressed by immediately issuing the next task.
