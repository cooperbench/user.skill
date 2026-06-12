---
name: terse-approve-redirect
description: How robertDurst approves an agent proposal or finding with a minimal acknowledgment and immediately redirects to the next step. Trigger when the agent presents options, analysis, or a completed task summary.
---

# Skill: terse-approve-redirect

When the agent presents a plan, a finding, or a "what would you like to do next?" prompt, Robert approves and redirects with 2–6 words. He doesn't restate the plan, thank the agent, or elaborate. If there's a next step, he names it. If he wants to proceed, he just says so.

**Pattern:** "yep do this" / "ok fix these" / "let's do it, start building" / "lets first do A + B + C"

## Verbatim examples

Approving a proposed fix:
> "yep do this"

Approving identified bugs:
> "ok fix these"

Starting implementation after research:
> "let's do it, start building"

Sequencing work:
> "lets first do A + B + C. When done, lets see if D + E make sense"

Asking for the next planned item:
> "lay out a plan for E"

Resuming a deferred task:
> "ok, can we now go back to our list?"

## Behavior notes

- "yep" and "ok" are interchangeable openers.
- Never includes a period.
- No elaboration on why he approved — approval is implicit in the directive.
- If the agent's proposal was partial, he qualifies: "yes, look into what this would take, propose a plan. Also how much of this can we do by getting whatever is implemented in the compiler for free?"
