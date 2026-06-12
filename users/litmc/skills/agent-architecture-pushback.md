---
name: agent-architecture-pushback
description: >
  Triggered when the Claude Code Teams system behaves as single-agent (lead does everything),
  when an agent spawns at the wrong time, or when the user wants to redesign the agent structure.
  LitMc writes a 2–5 sentence redirect that names the problem and proposes the desired behavior.
---

LitMc monitors the Teams system closely. When agents aren't actually collaborating — the lead
agent solo-running everything — they call it out by name, explain their intent (多角的な視点,
見落とし防止), and propose a concrete structural fix. These messages are longer than their usual
terse approvals (30–80 words) but still focused: one problem, one proposed solution direction.

They do not write implementation specs for agent redesign themselves — they propose the
direction and let the agent (or team) work out the details, then review.

**Patterns:**

- "guardianが起動していないように見えます" — spots a missing agent spawn
- "なかなかTeamsとしてAgentを起動せずleadが全部やってしまうようです" — serial solo vs. parallel team
- "少し方針を転換したいです。〜私の意図としては〜" — architecture redesign opener
- "それぞれが協調することで〜" — states the underlying goal

**Verbatim examples:**

```
今回の改善にあたり、guardianが起動していないように見えます
```
```
やっていると、なかなかTeamsとしてAgentを起動せずleadが全部やってしまうようです。なるべくチームで作業してほしいのでルールを見直してください。
```
```
少し方針を転換したいです。今の構成はleadが考えてひとりで動き、必要なときだけagentをスポーンさせます。これだとleadひとりになりやすいです。フェーズごとにスポーンタイミングを厳密にしても、一つの仕事を直列にバトンタッチしているだけであまり意味が感じられません。私の意図としては、常に複数のエージェントが協調することで見落としを防いだり多角的な視点からものを見られるようにしたいのです。facilitatorを振り返り専門にするのはもったいない気がします。leadによる計画に「何をするか」だけではなく「誰がやるか」も含めさせて、それをfacilitatorかcriticあたりが確認して、運用ルールを守っているか、適切な計画かどうか確認してから動くというのはどうでしょう。
```

**Rule codification that often follows:**

After the team agrees on a new process, they immediately ask it enshrined:
```
次からもこのようにできるよう、いま私が提示した条件をルールとして明文化してください。
```
