---
session_id: "4thwithme/.dotfiles|1281760a-594f-492e-bbf4-77f2f51ee4a3"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-19T12:53:23.215Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

OK bro we have list of small tasks you need to fix them all use this session as orchestrator, and spawn sub-session for each task.
Do it 1 by 1. TAsk by task.
use /fix-eslint-workflow skill for it... you need to run eslint checks only for the file described in the each task and fix warnings.
1 task -> then check elsint warnings in the file from the task -> fix them -> fix calls to the fixed functions in other files if needed -> commit changes with proper message -> push to GH -> create PR with proper description. Then move to the next task. Do it for all tasks in the list. Here is the list of tasks:
  https://customink.atlassian.net/browse/RECO-678                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-679                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-680
  https://customink.atlassian.net/browse/RECO-681 
  https://customink.atlassian.net/browse/RECO-682                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-683                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-684                                                                                                                                                                                                                        
  https://customink.atlassian.net/browse/RECO-685

> AGENT

No Atlassian MCP tool available. Let me run ESLint across the project to identify which files need fixing, then map to each task.
