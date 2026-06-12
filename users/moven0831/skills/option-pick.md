---
name: option-pick
description: >
  Triggered when the agent presents a numbered or lettered list of options (A/B/C or 1/2/3).
  moven0831 picks with a single letter, optionally prefixed with "go for" or "let's go for",
  sometimes adding a one-clause qualifier about documentation or future direction.
---

When an agent presents multiple options, moven0831 picks the fastest possible way:

- Bare letter: `A` or `B` or `C`
- With prefix: `go for option A`, `Go for option C`, `Go for B`
- With `let's`: `let's go for B, but document this as a future improvement direction`
- With mild uncertainty: `will go for option B better?`

**Verbatim examples**:

```
A
```

```
go for option A
```

```
Go for option C
```

```
Go for B
```

```
let's go for B, but document this as a future improvement direction
```

```
will go for option B better?
```

```
to answer the question above, let's go for Full create-unirep-app scaffold
```

No explanation is given for the choice. If the agent then asks a follow-up question about the picked
option, the user either picks again with the same pattern or gives a one-sentence constraint.
