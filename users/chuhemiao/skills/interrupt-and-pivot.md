---
name: interrupt-and-pivot
description: User interrupts the agent mid-execution and immediately issues a new directive, often switching approach entirely. Trigger: agent is taking too long, going in the wrong direction, or user changes their mind.
---

# Interrupt and pivot

This user sends "[Request interrupted by user]" when the agent is executing something wrong or unwanted. They do not wait for the agent to finish. The next message is a new directive — sometimes a full reversal of approach.

Pivots range from:
- **Soft pivot**: "继续完成任务，之前超时了" — pick up where things left off after a timeout
- **Hard pivot**: "删除之前的文件   安装这个bot ..." — throw away the agent's work and switch to an entirely different approach
- **Redirect after interrupt**: user interrupts, then re-sends the same or a refined version of their original message

The user does not explain why they interrupted. They do not apologize. The new directive stands.

## Examples

Interrupted mid-task, then resumed with a clarification:
> `[Request interrupted by user]`  
> (next message) `增加新的来源， https://cryptologos.cc/  我认为cryptologos 有更完整的logo，去掉Clearbit Logo API`

Interrupted twice on the same session, then retried:
> `[Request interrupted by user]`  
> `[Request interrupted by user]`  
> `增加新的来源， https://cryptologos.cc/ ...`

Full approach reversal:
> `删除之前的文件   安装这个bot https://github.com/anthropics/claude-plugins-official/blob/main/external_plugins/telegram/README.md`

Resume after timeout:
> `继续完成任务，之前超时了`
