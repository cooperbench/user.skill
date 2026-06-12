---
name: pr-merge-finish
description: >
  Triggered at the end of a work unit when the user wants to wrap up: format, push, create
  PR, and sometimes auto-merge. This is the user's standard "done" signal, often chained
  as a single short message.
---

After a sequence of fixes or refactors reaches a stable state, the user issues a finishing command that chains format + PR creation. Sometimes includes admin merge. The message is always short and lowercase.

## Examples

```
run make format and create PR
```

```
ok create PR and merge with admin priveleges
```

```
run `make format` and push
```

```
create PR
```

```
create PR and fix nix lint error
```

```
ok cool create PR
```

```
fix corresponding tests and create pR
```

## Roleplay behavior

The message is 3–8 words. Often starts with "run", "ok", or just the imperative directly. "admin priveleges" is the standard misspelling — reproduce it. May or may not include `make format` step. `create PR` alone is valid as a one-shot finish.
