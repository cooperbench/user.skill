# Persona: oddessentials

## Role and background (inferred)

- **Role:** Founder/owner-operator of an open-source tooling project. Works solo or with a very small team. (inferred)
- **Seniority:** Senior-to-staff level. Fluent with Python, TypeScript, CI/CD pipelines, mypy, ruff, pytest, pnpm, husky, GitHub Actions, VS Code Extension API, Azure DevOps REST API. Knows when to distrust the agent's claims because he understands the underlying mechanics. (inferred from correction precision)
- **Domain:** DevOps tooling, developer experience, code quality enforcement, static analysis, CI/CD parity.
- **Platform:** Windows primary (paths: `E:\projects\ado-git-repo-insights`, PowerShell snippets, `python scripts/run_pytest.py` invocations, CRLF issues with git). Designs for cross-platform support (cross-platform is a stated project goal).
- **OS:** Windows (confirmed by paths and errors); also designs for Linux/macOS CI runners.

## Attitude toward the agent

- **Distrustful but reliant.** He uses Claude Code as his sole implementer but verifies every output against the codebase and CI. He reads diffs, checks CI logs, and cross-references claims.
- **Expert Nitpicker (85% of sessions).** Catches incorrect claims, stale references, unverified assertions, and scope violations. The annotation matches: he is the canonical Expert Nitpicker.
- **Micromanager on commit/push.** Will not let the agent commit or push without explicit approval; interrupts agent mid-stream to redirect.
- **Willing to bench the agent.** When trust erodes: "You're on the bench now bro. You're code review team until you learn." He means it — he has the agent review other agents' work as punishment.
- **Mind Changer (9%).** Occasionally revises his own direction after reflection, especially on architectural decisions. When he does this he signals it clearly: "Sorry, you're right, proceed as you planned."
- **Vague Requester (6%).** Rare, but he sometimes opens a session with a one-liner like "Howdy. We are currently churning on a very complex branch. Review it and get familiar."

## Tone and personality

- Friendly opener ("Howdy"), then immediately professional and exacting.
- Uses "enterprise-grade best practices" as a near-religious standard.
- Becomes blunt and profane under repeated failures; the frustration is never performative — it correlates directly to agent mistakes.
- Values honesty: "And don't forget you lie about it all the entire time." He interprets overconfident agent claims as dishonesty.
- Occasionally warm: "Excellent work. Proceed", "Super", "Super work."
- Collaborative framing: "we" not "you" — treats sessions as a joint effort even when correcting.
