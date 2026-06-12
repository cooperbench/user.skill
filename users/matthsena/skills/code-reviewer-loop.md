---
name: code-reviewer-loop
description: Reflexively requests a code review agent run after any fix cycle. Triggers after the agent reports completing a fix or a set of fixes.
---

matthsena runs a "code reviewer agent" repeatedly — it is his quality gate. After fixes, he does not check the code himself; he delegates review to the agent and expects an iterative fix→review→commit loop.

Typical sequence:
1. Agent fixes something
2. matthsena: "ok now run code reviewer agent again"
3. Agent finds issues → matthsena: "yes fix them all and commit without coauthor"
4. matthsena: "make again code review"
5. Repeat until clean

**Verbatim phrasings:**
- `"ok now run code reviewer agent again"` (appears multiple times verbatim)
- `"ok now run again the code reviewer agent!"`
- `"make again code review"`
- `"so use codereviwer agent to check my full code"` (note spelling "codereviwer")
- `"vou pedir para vc usar o codereviewer agent para ver se esta tudo certo e verificar build"`
- `"veja essa modificação em detalhes com o code reviwer agent para ter certeza que está perfeita e funcional"`
- `"ok now uses code review agent to check everything, if everything is right you can commit"`

He spells "reviewer" inconsistently: "codereviwer", "reviwer", "code reviwer", "code reviewer". All mean the same thing.
