# Persona: heath0xFF

## Role and background (inferred)

Solo indie developer / hobbyist building a Rust desktop app for personal use, likely also used to
showcase or share publicly (Homebrew distribution, GitHub releases). Not at a company — no
mentions of teammates, PRs, or code review from humans. The GitHub handle `hhheath` visible in
code comments suggests "heath" is a first name. (inferred)

## Seniority signals

- Knows Rust well enough to build a multi-module async GUI application from scratch
- Comfortable with tokio, egui, reqwest, rusqlite, serde, TOML config
- Writes structured code review prompts with precise file:line targets — knows what to look for
- Initiates security reviews, database transaction audits, performance reviews unprompted
- Aware of idiomatic Rust concerns (unwrap vs expect, Result<T, String> anti-pattern, clone hot paths)
- Reads agent findings critically: challenges priority ordering, notices when agents conflate issues
- (inferred) Mid-to-senior individual contributor with Rust backend experience; likely has a day
  job and builds hChat as a side project

## Domains

- **Primary**: Rust systems programming, GUI (egui/eframe), async (tokio), desktop apps
- **Secondary**: LLM API integration (OpenAI-compatible, Ollama, OpenRouter), TOML config,
  SQLite, macOS (Homebrew distribution, macOS file paths throughout)
- **Weak / delegated**: Testing, CI/CD, GitHub Actions, Homebrew formula details

## Attitude toward the agent

**Trusting but watchful.** He delegates all implementation and heavy lifting without second-guessing
the approach, but he monitors progress on long tasks ("so what's up? been working for a bit") and
calls out scope violations immediately when he notices them. He challenges agent rationale when it
doesn't make sense ("why would you fix those 5 first?") but accepts the explanation and moves on.
He does not micromanage the HOW — only the WHAT and the boundaries.

## Persona annotation

The session annotations classify 83% of sessions as "Other," with 8% "Vague Requester" and 8%
"Mind Changer." He is not vague in intent — he knows what he wants — but he often issues
short prompts and expects the agent to fill in the blanks based on context.
