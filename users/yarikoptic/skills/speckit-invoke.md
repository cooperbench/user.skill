---
name: speckit-invoke
description: Opens every session with a /speckit.* slash command rather than plain prose. Trigger when starting a new coding session or a new phase of work.
---

# Session kickoff via /speckit.* commands

yarikoptic never begins a session with "please do X" prose. Every session opener is a slash
command from their speckit skill framework, optionally followed by a `--` clause that adds
context or scope.

**Pattern**: `/speckit.<phase> [task IDs] [-- additional context]`

## Verbatim examples

```
/speckit.plan proceed while also doing research on prototypes and related projects listed in  docs/design/00-initial-design.md file
```

```
/speckit.implement T054 T061 T068 T072 — sweep tests
```

```
/speckit.clarify - in prior commit I added some changes to user stories -- please analyze and potentially adjust user stories to reflect better. Also please add a user story for migrate within 1.x series.  Review bids-specification deprecations through the versions (specification is under /home/yoh/proj/bids/bids-specification-master and git grep there for DEPRECATED).
```

```
/speckit.specify Build a Python application/library following what is described in docs/design/00-initial-design.md file
```

```
/speckit.tasks
```

## Notes

- Task IDs like `T034 T035` reference items in the speckit task list
- The `-- clause` appends extra scope without changing the command verb
- When resuming after a commit, `/speckit.clarify` is the correction channel
- `/speckit.tasks` with no arguments is a status check, not an action
