---
name: manual-step-loop
description: >
  Trigger: agent asks the user to run a command or install a dependency themselves.
  User offers to do it with a polite question, then confirms completion with a short status message.
---

When the agent reaches a step that requires the user to act (install, run, approve), the user does not just say "ok" — they ask if it's their role to do it, then confirm when done. Both messages are short.

**Offer:**
> `こちらでインストールしましょうか？`
> *(Should I install it on my end?)*

**Confirmation after completing the step:**
> `インストールできました`
> *(Installation is done)*

These two messages arrive close together and function as a handshake: the agent should resume its task after the second message, not re-ask or re-explain.
