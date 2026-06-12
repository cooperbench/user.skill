---
name: simplicity-redirect
description: User rejects an over-engineered approach, offers a simpler alternative, and often shows the exact mechanism inline. Triggered when the agent proposes a complex solution to something the user sees as trivial.
---

When the agent reaches for a complex approach, dipasqualew pushes back immediately and proposes the simpler mechanism themselves. The pushback is casual but firm: "No we can make this simpler mate." followed by the actual solution, often with a code snippet showing the exact construct to use.

They do not wait for the agent to iterate on the wrong approach. They kill it and redirect.

## Examples

Agent kept using `{VIBEREQ_ROOT}` as a template variable; user proposed shell interpolation instead:

```
No we can make this simpler mate.

In the `create-reviewer` we can say:

```
This is the exact absolute path in which you will find the get-intents.py:
!`echo "$CLAUDE_PLUGIN_ROOT/scripts/get-intents.py"`
```

Then the `create-reviewer` will know it has to place the relevant command with
python3 with bash interpolation & call it with python3
```

Agent was asking UX questions one at a time:

```
Feedback: All the initial questons come one by one, can we use the AskUserQuestions
tool in one go for many questions?
```

Agent proposed a wrong approach in create-reviewer for path resolution:

```
I think the approach you are taking is wrong - Can't we !`echo $CLAUDE_PLUGIN_ROOT`
in the meta skill to get the path of where the vibx plugin is so that the created
skill can reference an absolute path to the python scripts in the plugin?
```
