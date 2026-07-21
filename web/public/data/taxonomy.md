Classify the developer's communicative ACTS by the observable function(s) of their message toward the agent's previous turn. Free multi-label: select EVERY act that applies (non-empty subset). Multiple acts are OK when a turn does several things (e.g. asks a question AND assigns a new task).

Acts:
- approve: greenlight the *current* proposal — proceed with what was already offered. Examples: go ahead; LGTM; "can you work on this/these?"; yes/ok/thanks as go-ahead; conditional "fine if X". No new task beyond that proposal.
- critical: asserts fault (something is WRONG) — not merely proposing an alternative. Examples: bug; wrong output; still failing; wrong approach; correcting a misunderstanding. Proposing a different plan without asserting fault → steer, not critical.
- steer: change *what to build/do* next — a NEW or DIFFERENT task from the current proposal (not mere go-ahead; not "go verify a fact"). May be phrased as a question ("can you…?"); still steer, not inquiry, when the ask is new/different work.
- inquiry: want information or confirmation (an answer), not a new build/do ask. Examples: status/why/what happened; "confirm after searching". "Go verify a fact" without changing what to build → inquiry, not steer.

Soft guidance (not hard exclusivity):
- Prefer including critical whenever fault/error/dissatisfaction is clearly asserted, even if the message also steers or asks.
- approve vs steer: go-ahead on the agent's plan (incl. "fine if X", "can you work on these?") → approve; new/changed ask → steer. Do not tag go-ahead as steer.
- Picking an option the agent already offered → approve, not steer. If the agent presents multiple options (e.g. A or B) and the user selects one (e.g. *"Yes it should be started automatically as part of the MCP fleet"*), that greenlights an already-offered option → approve.
- critical vs steer: assert fault → critical; propose alternative without asserting fault → steer.
- Decide steer vs inquiry by goal (new action vs answer/confirmation), not punctuation. "Confirm after searching" → inquiry; changing what to build/do → steer.
- Use both inquiry and steer only when both goals are genuinely present.
- approve+critical together is rare/contradictory; only use if both are genuinely present (e.g. the agent proposes a listed plan and the user approves parts of it but pushes back on other parts).
- Do NOT force a single winner via a first-match ladder.
