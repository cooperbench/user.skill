# Preferences — shunkakinoki

## Pushback Distribution

| Type | Rate |
|------|------|
| Non-pushback (accepts) | 44.6% |
| Correction | 37.8% |
| Failure report | 13.5% |
| Rejection | 3.4% |
| Takeover | 0.7% |

Over half of prompts result in some form of pushback. Corrections dominate — this user frequently steers mid-implementation rather than waiting for a full result.

## What Triggers Corrections

- **Agent overshoots scope**: Converts a single-file fix into a multi-file refactor → user says "no you made the entire thing a script i only want [specific part] as a script"
- **Wrong flag or option**: Agent uses `--worktree` after it was renamed to `--spawn worktree` → "also change both to dangerously skip permissions"
- **Aesthetic objection**: Ugly shell variable expansion in Makefile → "no; ... is ugly"
- **Unwanted documentation**: Agent adds permissions to wrong file → "no; permissions in README.md shoudl be managed in @config/claude/settings.json"
- **Wrong path or naming**: "hmm no - make it relative link like all of the other repos - i want to make it ./lua"
- **Missing detail from original ask**: Agent does X but forgets the also-do-Y from the original message → quick addendum correction
- **Over-explanation**: Long answer about WHY something is slow → "yea but it's so slow" (implicit: fix it, don't lecture)

## What Triggers Rejections

- Agent suggests something technically blocked: "can't do that" (git command that doesn't apply in current state)
- Agent puts content in the wrong location: "no in @config/claude/" 
- Agent has already prompted the user about something it should just do: "you've prompted everything", "don't do that"

## What Satisfies (non-pushback)

- Terse confirmation of fix: "Fix works. The `declare -A` error is gone." (user moves on without comment)
- PR created with correct title/body → "create PR" → no response needed beyond the PR URL
- `make shell-test` passing → user says "ok cool create PR" or just "push"
- Correct one-liner answer to a question → user says "yes that's what i want" or "ok; cool"

## Workflow Habits

**No planning phase.** Jumps straight to task. Does not ask for implementation plan, design discussion, or options — if the agent volunteers a multi-option breakdown, the user picks one immediately or cuts it off.

**Delegate then verify.** Kicks off long operations (nix switch, CI runs, background tasks) and returns with a follow-up check: "check if its working", "ssh into kyber machine (tailscale) and check if it's working there", "run makefile updater to check if the fix works?"

**Interrupts freely.** "[Request interrupted by user]" appears multiple times. Always followed by "continue" or a corrective prompt — not an apology or re-explanation.

**Test-driven as a quality gate, not design driver.** Does not write tests first; runs `make shell-test` after implementation and tells agent to fix failures. Expects tests to exist for any new script: "ok now create tests so `make shell-test` pass"

**Commit cadence: batch then PR.** Does not commit incrementally. When satisfied: "run make format and create PR" or "ok create PR and merge with admin priveleges". Uses admin merge via GH CLI.

**Format before push.** Always runs `make format` or `make format` + `push` as a finishing step.

**Stack preferences visible in prompts:**
- Nix / home-manager / nixpkgs
- Fish shell (custom functions, `make shell-test` / `make shell-lint`)
- Bun (package manager, `bun.lock`)
- Cargo / Rust (`Cargo.toml`, `Cargo.lock`)
- Neovim + Lua config
- tmux
- Tailscale
- Claude Code (heavily configured: hooks, settings.json, remote-control, worktrees)
- GitHub Actions as CI
- Pushover for notifications

## What They Do NOT Want

- Explanations of well-known tools (Bazaar, what `.bzr` is — user just wants to know what to exclude)
- Multiple-option breakdowns when they already know the answer
- Files put in the wrong directory
- Inline bash scripts in Nix modules (`home-manager/modules/local-binaries/default.nix` "shouldn't contain the inline bash scripts")
- Unsolicited complexity: "hmm this is too complex"
- Session-end notifications for Claude Code: "no need to have session end notification for claude code"
