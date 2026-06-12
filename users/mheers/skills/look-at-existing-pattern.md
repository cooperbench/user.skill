---
name: look-at-existing-pattern
description: When adding something new that has an existing analog in the repo, point the agent at the existing pattern explicitly before stating the new requirement. Triggered when the agent might otherwise implement something from scratch that should follow an established convention.
---

mheers expects the agent to study the existing code structure before implementing. When something already exists that the new feature should mirror, he says so and names the location. He does not describe the existing pattern in detail — he trusts the agent to read it.

**Pattern:**
```
<point to existing analog> (look at <location> and how <mechanism> does it). I need to <new requirement>.
```

**Examples:**

> "we already have some skill installed (look at the skills folder and how the Dockerfile adds them). I need to add 'npx skills add pbakaus/impeccable'"

> "into the docker image add vuejs agent skills from https://github.com/antfu/skills"
(implicitly relies on agent knowing the existing skills-installation pattern from context)

**Note:** He uses parentheses for the "look at X" aside, keeping it subordinate to the main directive.
