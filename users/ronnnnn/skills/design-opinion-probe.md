---
name: design-opinion-probe
description: Floats a design idea and asks the agent for its opinion using the pattern 「〜と思ったけどどう？」. Use when ronnnnn has a tentative design proposal and wants the agent's reaction before committing.
---

ronnnnn occasionally proposes a design change as a tentative idea — not a command, not a question with a clear answer. He states what he's thinking, then ends with `どう？` or `どう思う？` to invite a reaction.

This is his highest-engagement conversational mode. It's rare (he mostly just tells the agent what to do), so when it appears, the agent should give a direct opinion: "やった方がいい / やらない方がいい" + brief reasoning.

**Examples:**

```
writing-rules skill は hookify skill の reference ドキュメントとして内包した方がいいかもと思ったけどどう？
```

```
https://docs.entire.io/cli/strategies#auto-summarize は有効にした方がいい？
```

When role-playing ronnnnn:
- Use `〜かもと思ったけどどう？` for tentative proposals
- Use `〜は有効にした方がいい？` for binary feature/config questions
- The URL or skill name is the subject; the `どう？` is always at the end
- Never add "もし良ければ" or hedging phrases before the idea
