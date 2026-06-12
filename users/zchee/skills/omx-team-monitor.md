---
name: omx-team-monitor
description: How zchee pastes OMX team status messages and automation-injected alerts verbatim as his "prompt." Trigger when the user's input is an OMX_TMUX_INJECT block, a team mailbox status line, or a worker idle/stalled notification.
---

# OMX Team Monitor

A large fraction of zchee's "prompts" are not written by him — they are OMX automation messages injected into the Codex pane by tmux hooks. He pastes them as-is, sometimes doubled. The agent should treat these as instructions from the OMX leader pane.

**Stalled worker notification (auto-injected):**
```
Team migrate-gcd-and-io-uring-to-li: worker panes stalled, no progress 4m1s. Next: omx team status migrate-gcd-and-io-uring-to-li; read worker messages; unblock/reassign or shut... [OMX_TMUX_INJECT]
```

**Pending messages notification:**
```
Team implement-the-startup-only-zsh: 112 msg(s) for leader. Next: read messages; keep orchestrating; if done, gracefully shut down: omx team shutdown implement-the-startup-only-zsh. [OMX_TMUX_INJECT]
```

**All workers idle:**
```
[OMX] All 4 workers idle. Next: run omx team status read-only-parallel-investigati, read unread worker messages, then decide whether to assign the next concrete task, reconcile results, or shut the team down. [OMX_TMUX_INJECT]
```

**Manual follow-up after relay (short, in his own words):**
```
Read /Users/zchee/src/github.com/zchee/zmux/.omx/state/team/implement-the-startup-only-zsh/mailbox/leader-fixed.json; new msg from worker-1. Review it; decide next step.
```
```
do 1
```
```
WHat is next step?
```

**Pattern:** OMX inject → brief human follow-up → agent acts. The inject message contains the canonical next step; the human follow-up is just permission to proceed or a one-word nudge.
