> DEVELOPER

@docs/quick-wins-todo.md /teach read then lets start

> TOOL

tool_use Skill
id: toolu_01D2jq6yKEgoAxAwqnuYvmiK
```json
{
  "skill": "teach"
}
```

> TOOL

tool_result
id: toolu_01D2jq6yKEgoAxAwqnuYvmiK
```
Launching skill: teach
```

> AGENT

Great, I've read your todo list. You've already knocked out #1 (trailer embed) — nice work!

The next unchecked item is **#2: Show streaming links on detail page**.

Before we dive in, let me ask you a couple of questions to see where your head's at:

1. **Where do streaming links come from?** The todo says "Already in detail response" — do you know which part of the Jikan anime detail response contains streaming info?

2. **Have you looked at how you implemented the trailer embed?** Since that's already done, the pattern for streaming links will be very similar. Can you describe the general flow of how data gets from Jikan → your Express backend → the detail page frontend?

Take a look at your detail page code if you need to refresh your memory. Which file would you check first?