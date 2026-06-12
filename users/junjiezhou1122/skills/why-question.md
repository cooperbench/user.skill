---
name: why-question
description: "Trigger: agent introduces a concept, tool, or architectural choice that junjie doesn't understand or suspects is unnecessary; user asks a short 'why' or 'what is' question, often in Chinese."
---

Junjie asks "why" questions when he encounters something that seems complex, unnecessary, or that he wants to understand before accepting. These questions are short — often 5–10 Chinese characters or a brief English phrase — and carry a skeptical undertone. He challenges agent recommendations.

**Chinese pattern**: `"[concept]是干嘛的！"` / `"为啥[mechanism]就可以[result]呀"` / `"啥意思"`
**English pattern**: `"why not [alternative]??"` / `"Then what's the strength of [X]"`

**Examples**:
- `"sdk是干嘛的！"` (What's the SDK even for!)
- `"为啥mcp server就可以通信呀"` (Why can the MCP server communicate?)
- `"啥意思"` (What does this mean) + attaches screenshot
- `"why not recommend other language like rust or go to build backend??"`
- `"Then what's the strength of Go"`
- `"Do u think next.js is also a good choice?"`

These often precede a pivot — junjie asks "why" to confirm his instinct that the agent's choice is wrong. After a satisfying answer he may accept it (`"用mcp吧 也可以的！"`) or reject and pivot (`"So I wanna change..."`).
