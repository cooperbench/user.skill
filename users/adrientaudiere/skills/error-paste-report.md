---
name: error-paste-report
description: Reports a bug by pasting the raw error or stack trace verbatim, with no commentary. Trigger when a function or command has failed and the user needs to hand off debugging.
---

# Error paste report

When something breaks, adrientaudiere pastes the raw error output directly — R stack traces, hook error messages, ggplot layer errors — with no surrounding explanation. The agent is expected to diagnose and fix without prompting.

French-language errors are pasted in French without translation.

## Examples

Full R traceback, no preamble:
```
Bug in upset_pq(data_fungi_mini,
    fact = "Height", width_ratio = 0.2,
    taxa_fill = "Class"
  )

Error in `arrange()`:
ℹ In argument: `..1 = .`.
Caused by error:
! object '.' not found
     ▆
  1. ├─MiscMetabar::upset_pq(...)
  2. │ ├─dplyr::arrange(...)
...
```

French ggplot error:
```
Error in `geom_text()`:
! Problem while computing aesthetics.
ℹ Error occurred in the 6th layer.
Caused by error:
! objet '.stack_order' introuvable
```

Git hook failure:
```
When I push i obtainde the following error : .git/hooks/commit-msg: 4: entire: not found
```

Note: "obtainde" is a typo for "obtained". The message structure is always: what action was taken, what error appeared, the raw text. Sometimes the action context is omitted entirely and only the error is pasted.
