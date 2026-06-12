# Preferences: toothbrush

## Pushback Distribution

| Type | Rate |
|------|------|
| Non-pushback (accepted) | 55% |
| Correction | 36.7% |
| Failure report | 3.3% |
| Takeover | 3.3% |
| Rejection | 1.7% |

High correction rate (37%) signals that the agent frequently delivers something close but not quite right, requiring a specific follow-up tweak.

## What This User Corrects

**Test style — literal assertions over contains checks**  
Any test that uses `strings.Contains`, `len == 0`, or partial matches will be corrected to use exact byte/string equality against a literal expected value. This is the single most frequent correction pattern.  
> "i'd like to see literal expectations (either byte slices or strings) instead of strings.Contains checks"  
> "i'd like all those assertions replaced with a single comparison to what the result should be, literally"

**Duplication in production code**  
Immediately identifies copy-pasted logic across functions and asks for consolidation.  
> "That case statement looks duplicated.  Do we need all the logic in promptShellCompletion and setupShellCompletionNonInteractive to be duplicated?  Let's try and simplify."

**Loss of informative output after refactor**  
When a refactor removes user-visible status messages, restores them explicitly.  
> "I don't quite like e259b8e though - it gets rid of the informative output.  I'd like to bring that part back."

**Stdlib over custom reimplementations**  
Replaces hand-rolled utilities with standard library equivalents without hesitation.  
> "Replace the custom string contains implementation with the standard library's strings.Contains function."

**Edge case completeness in redaction/security logic**  
Catches cases the agent's implementation misses: top-level JSON arrays, field-skipping coverage, files omitted from filtering pipeline.  
> "The shouldFilterFile function determines which files get filtered for secrets, but it omits paths.SummaryFileName"

**Test multiline strings**  
Prefers backtick multiline string literals in Go tests over escaped single-line strings.  
> "They're hard to read.  Let's instead replace our expectations with literal multiline strings, nice and obvious."

## What This User Rejects

**Agent over-refusal on test/documentation values**  
Rejects moralizing when a "credential" is clearly a test fixture.  
> "it's a test value for gitleaks detection"

## What Satisfies This User

- Plans executed exactly as written, with no improvisation
- Commit messages composed by the agent without being asked for drafts
- Tests that compare against literal values (byte slices, exact strings, literal structs)
- Refactors that genuinely reduce line count and eliminate duplication
- Error paths that fail loudly instead of silently passing through

## Workflow Habits

- **Plan-first**: Opens big tasks with a complete implementation plan. Does not ask the agent to design; arrives with the design done.
- **No explanation requests**: Never asks "why does this work?" or "explain this code" — 1.5% understand intent, all other turns are action-oriented.
- **Commit cadence**: Issues `commit` as a standalone command after each meaningful unit of work. Frequency ~6 commit commands across 66 prompts = roughly every 10 prompts.
- **Tests are required**: 16.7% of prompts are test-focused; often adds tests as a distinct follow-up step after implementation.
- **Lint compliance**: Addresses lint issues as they arise; uses inline linter directives (`//nolint`) when removing the code is not acceptable.
- **Interrupt freely**: Does not wait for the agent to finish a long tool chain; interrupts and redirects.
- **File references**: Pins corrections to specific line ranges using `@path:L-L` syntax.

## Stack / Tool Preferences Visible in Prompts

- Go (primary language for `entireio/cli`)
- `mise` as task runner (`mise run lint`, `mise lint`)
- `gitleaks` for secrets detection
- cobra CLI framework (referenced in command structure)
- Fish, Zsh, Bash (shell completion targets)
- `slices.Equal` (Go stdlib, prefers modern stdlib APIs)
