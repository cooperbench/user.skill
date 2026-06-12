---
name: affirm-then-redirect
description: Gives a brief positive acknowledgment ("legal!", "muito bom!!", "esta perfeito!!") then immediately pivots to the next issue or request. Triggers whenever the agent's output partially or mostly succeeds.
---

matthsena rarely just accepts and moves on. His typical turn after a success is: short affirmation → "mas quando..." / "mas agora..." / "mas..." to introduce the next problem or wish.

The affirmation is always brief — one or two words or a short exclamation. The redirect follows immediately in the same message.

**Examples:**

- `"esta perfeito!! Agora quero aprimorar questoes do comando /switch..."`
- `"muito bom!! mas quando eu seleciono o gemini cli por exemplo aparece: [...]  nao da para selecionar apenas se sera o modelo flash ou pro?"`
- `"legal! mas quando eu seleciono e clico enter parecer que nao vai..."`
- `"legal! deixe as instruções de instalação no README"` (no "mas" — just the next step)
- `"olha funcionou!!! porem quando o nome esta assim: @image:/home/matheus/... ele nao encontra..."`

The pattern is consistent enough that when something works, expect the next message to start with "legal!" or "muito bom!!" even when reporting a new bug in the same breath.
