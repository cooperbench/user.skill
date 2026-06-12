---
name: loop-mission-kickoff
description: How malkoG opens autonomous multi-feature sessions — dumps a numbered mission brief into /loop with an interval, then lets the agent run
---

# Loop Mission Kickoff

When malkoG wants the agent to work autonomously on a broad goal (e.g., "achieve iOS feature parity"), he invokes `/loop 30m` with a multi-paragraph mission brief. The brief:

1. States the top-level goal ("Your mission is building android client for HackersPub")
2. Explains the gap ("current implementation lacks of many features")
3. Points to the reference source ("For iOS app, see ../hackerspub-ios")
4. Gives an explicit process the agent must follow (branch → commit → PR workflow, numbered)
5. Ends with a confirmation prompt: "Do you got it?"

He does NOT describe individual features — the agent is expected to discover them by comparing the iOS app.

After the loop starts, malkoG monitors passively: he approves task completion notifications with "Keep go", "Good. Keep go", or "Yes. Sure". He interrupts with a terse correction only if something is visibly wrong.

**Example (condensed):**

> `/loop 30m`
> 
> Your mission is building android client for HackersPub.
> But, current implementation lacks of many features. So that, you need to make complete. At least, we need to satisfy 100% parity of iOS app.
> For iOS app, see ../hackerspub-ios
> 
> For satisfy 100% parity of iOS app, you can take a look using `git logs`
> And then see .swift changes, and then apply corresponding or similar changes using .kt (kotlin)
> 
> Before working through, You need to follow these things:
> 1. If you want to start working, spawn branch using `git switch -c <branch_name`
> 2. After single work unit done, add them to stage area, and then use `/commit` skill
> 3. After commit, use `/ghpr` skill.
>   - For first work unit, `/ghpr` onto upstream's main branch.
>   - And following work units, `/ghpr` onto previous PR's branch
> 
> Continue until i explicitly requesting stop
> 
> Do you got it?
