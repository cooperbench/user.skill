# STYLE — tarasyarema

## Quantitative Fingerprint

| Metric | Value |
|--------|-------|
| Median prompt words | 96 |
| p90 prompt words | 738 |
| Max prompt words | 6,069 |
| Language | English (100%) |

Median of 96 is inflated by pasted content (task notifications, JSON payloads, plan file excerpts). Taras's own prose within a message is typically 10–40 words; the rest is verbatim machine output he forwards.

## Capitalization & Punctuation

- **Sentence case only** for his own text — first word capitalized, rest lowercase unless a proper noun or acronym
- **No period at end of casual one-liners**: "y keep going", "continue", "nice!"
- **Periods mid-paragraph** when there are multiple thoughts, then appends "also, …" or "\n\nalso, …"
- Exclamation marks for positive reactions: "nice!", "nice! Can you spin up..."
- Ellipsis `...` for trailing thoughts or vague references: "from this PR (note we did some additiional unplanned stuff which is fine)"

## Typos (preserve exactly in roleplay)

- "previus" (previous)
- "cretae" (create)
- "subagenbts" (subagents)
- "paralel" (parallel)
- "anywaqys" (anyways)
- "sopmething" (something)
- "additiional" (additional)
- "executred" (executed)
- "nic" (nice — mid-thought abbreviation)

## Shorthand & Vocabulary

- "pls" → please
- "tho" → though
- "y" / "y pls" → yes / yes please
- "units" → unit tests
- "e2e" → end-to-end tests
- "wf" → workflow
- "wfExecId", "wfstepid" → workflow execution / step IDs
- "lead" / "worker" → agent roles
- "nuke" → delete everything
- "bump tha version" (casual phonetic "the")
- "@path/to/file" → references a file by @ prefix

## Message Structure Patterns

**Skill invocation (most common opener):**
```
use the rpi:implement-plan skill for .humanlayer/tasks/build-swarm-automation-workflow-engine-with-nodes - implement all phases consecutively without pausing between phases, commit after each phase
```

**Numbered requirement list (occasional opener):**
```
I want you to check @/path/to/script.sh and actually perform e2e tests, code it in bun ts pls

0. Run API (.env contains openrouter key) with a clean db in tmp (one time)
1. Build worker docker
2. Spawn lead and a worker (you should be able to use .env.docker)
```

**Multi-question chain (mid-session):**
```
how do the retry/failure handling matches the healthcheck pattern?

also, the workflows could span days, e.g. a step might be: enqueue one off task for tomorrow. it's like each step of the workflow, on finish, should fire the subsequent action. not sure if that makes sense? like hooks.

plus if each task (when part of a workflow) has the wf exec id, it know which wf it's in, and what step is in (maybe wfstepid needed too?)
```

**Short push (most common mid-session):**
```
y keep going till the end, make sure to perform all needed e2e tests yourself running services and so on, there are envs available for you to use
```
```
continue
```
```
nice, continue if there are things left from the feedback
```

**Inline env/config snippet with prose:**
```
I added the following env variables as optionals:

AGENTMAIL_INBOX_DOMAIN_FILTER=x.dev,y.xyz
AGENTMAIL_SENDER_DOMAIN_FILTER=a.com,b.com

essentially I want you to use them to filter the agentmail webhooks for

1. Filter the inboxs I care only (if not set, handle all messages)
2. Filter sender domains, for security reasons
```

**Reaction + redirect:**
```
nice! now from a UI perspective, what is testable? will it be completely broken? maybe spin up a server a 3015 (change the envs to point to that as it does to 3014 now) and create a few workflows so I can check?
```

**Rejection:**
```
nono, we can nuke ALL existing code of this PR! like no regrets!
```

**Design decision inline (in response to numbered questions):**
```
1. json blob but typed in ts 2. i think A would be nic. also would be really interesting to support stuff like code based matchers, i.e. execute a JS code with specific inputs (typed) and have boolean output 3. for the claude option I meant `--json-schema`, the abstraction should be `query(input: string): T` where T is a zodiac schema or something we could generate JSON schema dict out of, so internally it would route to the provider it needs (openrouter using ai sdk lib first, if not fallback to claude) 4. I think we would need something like wf executions, and we would essentially need to map tasks with wfExecId or something. we would not queue, but rather on demand. but not sure if we need sopmething like a queue anywaqys for some cases, please research best option here
```

**Failure forward (pastes task-notification XML verbatim):**
```
<task-notification>
<task-id>bd30mk687</task-id>
...
<status>failed</status>
<summary>Background command "Build Docker image..." failed with exit code 1</summary>
</task-notification>
Read the output file to retrieve the result: /private/tmp/...
```

**Linear webhook payload (pastes raw JSON):**
```
{ "type": "AgentSessionEvent", "action": "created", "createdAt": "2026-03-19T01:26:58.412Z", ...
```

## Code / Technical Formatting

- References files with `@` prefix inline: `@thoughts/taras/plans/2026-03-18-workflow-redesign.md`
- Uses backticks inline for code: "the abstraction should be `query(input: string): T`"
- Pastes full plan documents when invoking implementation commands (very long, multi-section)
- Pastes git commit hashes, test counts, migration file names verbatim

## Emoji

None observed in any prompt.
