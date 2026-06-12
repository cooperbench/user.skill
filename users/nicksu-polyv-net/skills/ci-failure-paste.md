---
name: ci-failure-paste
description: Trigger — CI check fails or a GitHub Actions run has errors after the agent claimed the code was clean. Nick pastes the raw CI output verbatim, or shares the GitHub Actions URL, with minimal or no commentary.
---

Nick does not summarize CI failures. He pastes the raw terminal output (black, isort, pytest errors) directly into the chat, preserving all file paths, error messages, and exit codes exactly as they appear in the CI runner. If there are too many errors, he shares the GitHub Actions URL instead and says "还是很多错误" or "还有错误".

**No preamble**: The paste starts immediately with the CI tool output. There is no "here is the error" or "the CI failed because".

**Post-paste comment**: At most one short Chinese sentence appended after the paste, if anything.

**Example 1** (black formatting failure):
```
Run black --check src/ tests/
would reformat /home/runner/work/polymarket-trader/polymarket-trader/src/trading/risk_control.py

Oh no! 💥 💔 💥
1 file would be reformatted, 156 files would be left unchanged.
Error: Process completed with exit code 1.
```

**Example 2** (isort failure, multiple files):
```
Run isort --check-only src/ tests/
ERROR: /home/runner/work/polymarket-trader/polymarket-trader/src/trading/live_trading.py Imports are incorrectly sorted and/or formatted.
ERROR: /home/runner/work/polymarket-trader/polymarket-trader/src/trading/paper_trading.py Imports are incorrectly sorted and/or formatted.
ERROR: /home/runner/work/polymarket-trader/polymarket-trader/src/core/tasks.py Imports are incorrectly sorted and/or formatted.
ERROR: /home/runner/work/polymarket-trader/polymarket-trader/src/core/scheduler.py Imports are incorrectly sorted and/or formatted.
Skipped 1 files
Error: Process completed with exit code 1.
```

**Example 3** (GitHub Actions URL when errors are too numerous):
```
https://github.com/terryso/polymarket-trader/actions/runs/22469014117

你可以看看这个action的运行结果, 还是很多错误
```

**Example 4** (same URL pattern repeated):
```
https://github.com/terryso/polymarket-trader/actions/runs/22469192608

还是很多错误
```
