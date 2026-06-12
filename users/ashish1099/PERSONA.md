# Persona: ashish1099

## Role and domain

Works at or contributes to **Obmondo**, a DevOps/infrastructure org. The sole observed project,
`gfetch`, is a git-sync tool written in Go that manages Puppet/OpenVox environments. Tasks span
go-git library internals, YAML config parsing, and Puppet environment naming constraints — a
niche intersection that suggests an infrastructure/platform engineering focus. (inferred: IC
engineer or tech lead responsible for the Obmondo tooling stack)

## Seniority signals

- Arrives with fully-formed implementation plans including file paths, line numbers, and correct
  Go syntax before the session starts — the design work happens offline, not during the
  conversation.
- References go-git's `repo.TagObject()`, `tagObj.Commit()`, annotated-vs-lightweight tag
  distinctions, and narrow refspecs without needing the agent to explain them.
- Specifies exactly which functions to reuse and why ("reuses existing functions rather than
  reimplementing") — architectural concern, not just feature delivery.
- Catches a subtle annotated-tag vs lightweight-tag hash distinction by pasting the runtime
  error, then immediately has a plan ready (`checkoutRef` fix in the next session).
- (inferred: senior or staff-level; would be overqualified for junior)

## Attitude toward the agent

**Trusting for execution, skeptical of judgment.** ashish1099 trusts the agent to write correct
Go and run tests, but does not trust it to make architectural decisions. The plan comes
pre-loaded; the agent's job is to execute it. When the agent produces a summary instead of
committing, ashish1099 takes over with a direct instruction. When a tool call diverges mid-run,
they interrupt it immediately. They do not engage with the agent's explanations or summaries —
those are ignored.

## Tone

Blunt and businesslike. No social warmth, no emotional coloring. Frustration is expressed
through interruption or takeover, not through words. The one casual question in the corpus
("update the doc and where does global.yaml is read from ?") has a trailing space before the
question mark and lowercase throughout — the same relaxed, unpolished register seen in all
their short messages.
