> DEVELOPER

For this project follow this workflow
Branch — Cut a feature branch off the latest main (fix/…, feat/…, refactor/…, docs/…, chore/…). Never commit to main directly.
TDD (red → green → refactor) — Write the test first:
RED: smallest test that captures the next behaviour (or reproduces a bug); run it, confirm it fails for the right reason.
GREEN: minimum production code to make it pass.
REFACTOR: tidy code/test while keeping the suite green.
The test and the code that satisfies it land in the same commit, and the commit message names what the test covers.
Verify with a verifier subagent — Run it over the pending change. Runs Lint & format and tests and builds Required — fix every issue and re-run until it returns PASS before review.
Pre-PR review with a code-reviewer subagent — Run it over the diff; address every must-fix (and reasonable should-fix) finding. Required. If fixes change code, re-run the verifier.
Open a PR — Push and open via gh (GitHub CLI, never the web UI). Describe what changed, why, and how it was tested.
Green CI is the merge gate 
Address review feedback as it lands — Act on valid points, push fixes, reply/resolve […]

> AGENT

I'll help you with your task. What would you like me to work on in the agent-brain-visualizer project?