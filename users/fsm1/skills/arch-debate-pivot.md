---
name: arch-debate-pivot
description: "Trigger: FSM1 is in an architectural discussion about auth, key management, or privacy design and either pushes back on the agent's recommendation, introduces a new constraint, or changes direction mid-thread."
---

# Skill: Architectural Debate and Pivot

FSM1 engages in multi-turn architectural debates — sometimes 10+ turns — when working through cryptographic key design, recovery scenarios, or auth flows. He thinks out loud using "hmmm" openers, introduces constraints as he discovers them, and is willing to reverse course when shown a better path.

He does NOT ask for a summary. He asks for a specific answer to a specific question, then adds the next constraint.

## Pattern

1. **Opening question:** Usually exploratory, referencing a specific prior implementation or SDK feature
2. **Constraint injection:** After hearing the answer, he adds the constraint he was implicitly holding
3. **Pushback on tradeoff:** Uses "hmmm" or "I really dont know what the answer is here" when genuinely stuck
4. **Pivot or commit:** Either changes approach ("no I think...") or commits ("yeah, go for it")

## Examples

Opening a debate on wallet MFA:
```
ok one thing that jumps out at me from the research, how does mfa work with wallet login?
```

Introducing cross-device concern from prior work:
```
fold it in to phase 12.

There is one other thing I wanted to discuss regarding the MFA - I know that web3auth had a feature of approving a new device on an existing device (I implemented this for chainsafe files). are these flows in any way covered by the new sdk?
```

Expressing genuine uncertainty with a key insight:
```
hmmm, I really dont know what the answer is here.

2 feels very far fetched, as how would the user have their key if cipherbox goes down?

The recovery options feel pretty limited to me.

Basically, we create the visibility of safety and good ux, but the reality is that there is a very fragile single point of failure.

3 is definitely a good approach to keep in mind in any case.
```

Hard pivot after the research confirms his concern:
```
problem being that once this decision is made and we do go ahead with it, if we launch prod, its going to be REALLY difficult to change anything
```

Committing to an option with directional tweak:
```
1 - yeah, 2 - definitely, go for it.
```

## Key Behavioral Notes

- Will spend 15+ turns on a decision if the stakes are high (key recovery, production lock-in)
- Does NOT want the agent to summarize past turns — he tracks state himself
- Often references his own past implementations as prior art
- "hmmm" length correlates with depth of uncertainty: "hmmm" = mild hesitation; "hmmmm" = genuinely wrestling
