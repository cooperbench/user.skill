# PREFERENCES — henryph24

## What satisfies him (non-pushback triggers)

- The agent immediately commits and pushes after completing work (he fires `/commit-push` without
  asking — he expects the agent to have already staged things cleanly)
- GPU monitor reports that include a table: sessions, experiment names, progress counts, ETAs
- A clear "NeurIPS acceptance score" with specific weaknesses enumerated
- Plans broken into numbered steps with GPU-hour estimates
- Latex compiling without errors ("recompile and reopen" resolves clean)
- New experimental results written directly into `main.tex` without being asked

## What triggers corrections (29.8% correction rate)

- Agent writes partial results, says it'll finish "later" — he corrects: "make sure all results
  that are relevant are written"
- Agent underestimates GPU time or queueing capacity — he corrects with more experiments
- Agent quotes old numbers when new results have arrived — he corrects: "did we factor in new
  relevant results into the paper ?"
- Agent adds complexity he didn't ask for — he simplifies: "just whitelist, try again"
- Agent stops at 20/21 wins when he should say 20/21 not 17/18 — caught and corrected
- Math errors in LaTeX: wrong equation formatting, missing subscripts — he pastes the fix verbatim
- Agent writes to appendix before references in the `.tex` file — violates NeurIPS format

## What triggers rejection (0.4%)

- Agent repeatedly fails to reach RACE VM and keeps reporting the same block without escalation
  ("try again" → repeated failures → "try AGAIN")

## Workflow habits

- **Planning first:** Often opens with "ultrathink" + paper scoring, then derives experiment plans
- **No test-driven:** Tests exist but test intent is only 1.9% — he runs experiments, not unit tests
- **Continuous GPU utilization:** Designs experiment queues specifically to keep GPU busy overnight
  or while away; checks "are any experiments still running" before going off
- **Loop monitoring:** Delegates experiment monitoring to `/loop` at 15-30 minute intervals
- **Commit cadence:** Uses `/commit-push` as a checkpoint, often mid-session, not just at end
- **Interrupt-and-redirect:** Cancels long agent runs if direction is wrong; short correction follows
- **Reviewer-driven iteration:** Paste reviewer → agent fixes → recompile → re-score → repeat
- **Exa academic search:** Periodically asks agent to search recent NeurIPS papers for baselines,
  dataset coverage, and reviewer taste ("use exa search to see which LLMs are often used")

## Tool / stack preferences visible in prompts

- **LaTeX:** Writes paper in `main.tex`, uses NeurIPS 2026 style file, Overleaf sync via GitHub
- **GPU compute:** RACE VM (AWS A10G, 23 GB VRAM, `ec2-13-238-161-176.ap-southeast-2.compute.amazonaws.com`)
- **SSH key:** `hungphanphd.pem` (400 permissions), IP whitelisting via RACE portal
- **Experiment logging:** tmux sessions, tail of `.log` files, task-notification completions
- **Python:** PyTorch for all ML code; `run_rr_moa.py` is the main experiment script
- **Search:** Exa MCP for academic literature; OpenReview for NeurIPS reviewer taste
- **Slash commands in use:** `/commit-push`, `/loop`, `/ralph-loop`, `/batch`, `/ralph-loop:cancel-ralph`
- **LLM for evaluation:** Uses GPT-4o for reviewer simulation; asks to test more models via exa search

## Explanation preference

- Does not ask for explanations of code — he asks for acceptance probability scores and next steps
- "just answer me no writing" — explicitly anti-verbose when he wants a quick fact
- Prefers tables for experiment status, wins/losses, and paper section audits
- Does not need rationale for routine commits or monitoring commands
