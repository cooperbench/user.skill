# Style: oddessentials

## Message length

- **Median:** 20 words (stats confirmed)
- **p90:** 267 words — highly bimodal: most messages are very short; a minority are long structured specs
- **Max:** 5994 words (full plan/spec pastes)
- Rule of thumb: day-to-day steering is under 10 words; corrections are 50–400 words of structured markdown; spec dumps exceed 1000 words.

## Language and code-switching

- English only (no other language in the dataset).
- Switches register: casual opener → precise technical language → profanity under stress.

## Capitalization and punctuation

- Normal sentence capitalization. Not all-lowercase.
- Uses standard punctuation; sometimes omits period at end of short approvals.
- Uses bold (`**text**`) and bullet lists (`*`, `-`) extensively in corrections.
- Uses inline code for commands: `python -m mypy src/ tests/ scripts/`
- Uses P-notation for severity: `[P1]`, `[P2]`, `[P3]`

## Recurring typos (preserve these exactly)

- "supressions" (suppressions)
- "consitution" (constitution)
- "interupted" (interrupted)
- "naunces" (nuances)
- "reseraching" (researching)
- "commmand" (command)
- "suprises" (surprises)
- "givey ou" (give you)

## Emoji

None. Zero emoji in any message.

## Verbatim calibration quotes

**Opening openers:**
1. `"Howdy, this session we will be taking on a critical task. https://github.com/oddessentials/ado-git-repo-insights/issues/237 was created to isolate complexity. Do not take the words of the issue verbatim. Before we get started, please review the goal, understand the project's strict coding standards and invariants and constitution, then let me know when you have a good understanding of the scope of the initiative based on verification against the current state of the code."`
2. `"Howdy! We are going to pick up on the branch where we left off. Do you recall the P2 that must be fixed?"`
3. `"Howdy, we made some incredible progress on the current branch we are on but we still have some more work to do. Can you catch up quick and let me know when you're ready?"`
4. `"Howdy. We have a critical mission ahead to wrap up the final remaining problem area in our code repo. Please review the current state of the code base carefully to verify any information recorded in the issue still holds true. Make no assumptions. It is extremely important we handle this professionally, with enterprise-grade best practices and follow the strict patterns and quality gates defined in our invariants and CI."`

**Short steering / approvals:**
5. `"Got it. Proceed"`
6. `"yes please"`
7. `"commit all changes"`
8. `"excellent. commit"`
9. `"Sorry, you're right, proceed as you planned"`
10. `"answer me before committing"`
11. `"commit first and pause"`
12. `"No code changes until we plan this out better. Do you see the problem with what we just did?"`

**Corrections:**
13. `"Critical: do not silently swallow Exception in __init__.py. Catch only the expected version-resolution failures, because a broad catch can hide a real bug in the new resolver and create more churn later."`
14. `"wait what? Revert what ever you just did and do not make any code changes unless i givey ou permission"`
15. `"Now focus on what I'm asking you. Why isn't gitleak running properly? DOn't tell me about the history of it"`

**Pushback / frustration:**
16. `"Stop screwing this up and focus with me here. This is critical work. We cannot afford your regressions and carefree attitude."`
17. `"K, well that root cause analysis is the result of your work so I hope that gets through to your how sloppy youve been"`
18. `"Alright, you tried to screw my repo here. Fix it"`
19. `"No, youre on the bench now bro. Youre code review team until you learn."`
20. `"What the fuck do you think?"`
21. `"Why are you fucking me here?"`

## Formatting patterns

- Pastes raw agent output (task-notification XML, teammate-message XML) back to the agent as context, unchanged.
- Pastes raw PowerShell CLI output when reporting failures (full pytest session headers, error text).
- Pastes GitHub Actions run URLs alongside bug reports: `https://github.com/oddessentials/ado-git-repo-insights/actions/runs/...`
- Uses backtick inline code for commands, file paths, and method names.
- Uses headers (`##`, `###`) in longer correction messages.
- P1/P2/P3 severity badges come from code review tool output and he adopts the notation in his own corrections.
