# PERSONA — araitatsuya-code

## Background (inferred)

Japanese developer, likely working solo or in a very small team on a side/personal project. The project (atena-print) is a desktop app for printing Japanese postal address labels — a niche, practical tool suggesting this user scratches their own itch. Workspace path `/Users/ta/workspace/atena-print` indicates macOS.

## Seniority (inferred)

Mid-to-senior. Evidence:
- Designed the project with Clean Architecture (entity → usecase → infrastructure layering) and enforces it during review ("Clean Architecture違反").
- Writes precise technical inline review comments in English specifying the exact selector pattern and even the Zustand API (`useShallow`).
- Knows about table-driven tests, repository interface mocking, DI wiring — these are not beginner concerns.
- Built a phase-based issue system with GitHub labels and custom slash commands — significant upfront planning discipline.

## Role (inferred)

Solo founder / indie developer. Writes all the specs, sets up all the tooling, merges all the PRs — there's no team visible in the sessions. The agent is effectively the engineering team.

## Attitude Toward the Agent

**Trusting by default, precise when correcting.** 78% of prompts are non-pushback — the agent is given the wheel and left alone. But when something is wrong, corrections are laser-targeted: a GitHub comment URL, an exact selector API name, a one-phrase scope cut. No rambling feedback. The annotation "Expert Nitpicker" (50% of sessions) and "Vague Requester" (28.6%) coexist: vague for direction (a slash command kick-off), precise for quality gates.

## Privacy Sensitivity

Noticed their macOS username appearing in a settings.json path and immediately raised a concern: "個人のユーザ名などは表に出ない方がいいのですが難しい？" — privacy-conscious about leaking personal identifiers.

## Tone

Flat, efficient, zero padding. No greetings, no thanks, no sign-off. Not unfriendly — just fully task-mode. When asking something, ends with ？. When directing, no punctuation at all.
