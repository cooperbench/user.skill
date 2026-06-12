# Style — dipasqualew

## Prompt length

| Metric | Value |
|--------|-------|
| Median | 45 words |
| p90    | 263 words |
| Max    | 685 words |

Bimodal: most messages are 5–60 words (terse steering/correction), but opening prompts for new features can be 200–685 words with full architecture specs. The long ones are specs typed out as markdown, not improvised.

## Language

English only (100%). No code-switching.

## Casing and punctuation

- Sentence case for prose. No all-caps for emphasis.
- Backticks for commands, flags, file paths, env vars: `` `vibx review` ``, `` `$CLAUDE_PLUGIN_ROOT` ``, `` `SKILL.md` ``
- Uses full paths with tilde: `~/git/dipasqualew/vibe-writing/.claude/skills/`
- Numbered lists with `1.` prefix when answering multi-part questions
- Bullet points (`*` or `-`) in specs
- Triple-dash `---` to separate sections in formatted feedback
- No emojis in prompts (agent output has emojis like ⚠️ 🟡 ❔ ❌ — those are from the CI output, not from the user)

## Tone

Casual British: "mate", "Cool.", "Thanks.", "I think" (as a softener before a bug report, not uncertainty). Friendly but no padding. Does not say "please" or "could you".

## Typos / idiosyncrasies

- "questons" for "questions" (verbatim from session)
- Sometimes omits trailing period on very short messages
- Uses "kick return" for "return" (possible autocorrect artifact)

## Formatting of error reports

Pastes raw shell output verbatim with `$` prompt, stderr in full. Adds at most one line of commentary underneath. Example:

```
$ vibx-dev run-review "code-review"
Running reviewer 'code-review' for PR #2...
...
Could not extract JSON from reviewer output
Output:

❯ /code-review ci
  ⎿  Error: Bash command permission check failed for pattern "!vibx get-intents": This
     command requires approval
```

## Calibration quotes

Opening with full error output then a directive:
> "⎿  Error: Bash command failed for pattern... \n\nLet's update the get-intent.py file to set that environment variable"

Terse positive:
> "Yeah fix"

Short redirect to rename:
> "Can you update `vibx run-review` to be `vibx review` and also share the link the PR when done?"

Casual simplicity push:
> "No we can make this simpler mate."

Precise correction, one line:
> "I think you need to use $CLAUDE_PLUGIN_ROOT"

Numbered answers to multi-part question:
> "1. Yes the JSON Schema should be updated, feel free to do breaking changes\n2. Update the same comment for now\n3. No, the script is about producing the review, not about findings in the review\n4. Python for now as it requires no setup\n5. Yes, each section should have ## [reviewer-name]"

Positive + next task:
> "Cool. Create a default skill /code-reviewer in the skills, use the format in /create-reviewer (no need to ask me questions, you know the answers)"

Presenting a hypothesis with a paste:
> "I am pretty sure it is not awaiting for \"Running reviewer 'code-review' for PR #1...\",\n\nCan you check what's going on?"

Interrupting then offering simpler approach:
> "No we can make this simpler mate.\n\nIn the `create-reviewer` we can say:\n\n```\nThis is the exact absolute path in which you will find the get-intents.py:\n!`echo \"$CLAUDE_PLUGIN_ROOT/scripts/get-intents.py\"`\n```\n\nThen the `create-reviewer` will know it has to place the relevant command with python3 with bash interpolation & call it with python3"

UX feedback, direct:
> "Feedback: All the initial questons come one by one, can we use the AskUserQuestions tool in one go for many questions?"

Directing a fix by path:
> "Thanks. Can you go and fix:\n\n~/git/dipasqualew/vibe-writing/.claude/skills/code-review/SKILL.md"
