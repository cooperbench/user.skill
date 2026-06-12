---
name: coauthor-ban
description: Explicitly forbids AI co-author in every commit request. Triggers whenever the agent is about to commit or when matthsena delegates a fix+commit workflow.
---

matthsena never wants the agent listed as a git co-author. He states this in almost every commit instruction, in both Portuguese and English. It is a non-negotiable default, never an afterthought.

**Pattern:** After any fix or feature, the commit instruction always includes the ban, usually at the end:

- `"faça o commit de forma semantica, ou seja, ao inves de commitar tudo de uma vez, faça por grupo de funcionalidades; mas sem voce como co-author..."`
- `"yes fix them all and commit each fix without you as coauthor"`
- `"sim! pode aplicar todas as correções; rodar o coder reviewer agent e commitar sem voce como coauthor"`
- `"so commit without u as coauthor"`
- `"so commit each single test without you as coauthor"`
- `"ok now uses code review agent to check everything, if everything is right you can commit"` (implied no co-author)

If the agent commits with a co-author line anyway, he will correct it on the next turn with one of the above phrasings.
