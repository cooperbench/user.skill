---
name: paste-and-fix
description: Reports failures by pasting terminal output verbatim then appending the fix directive. Trigger when the agent has committed or run code that failed.
---

# Paste-then-fix failure reporting

When something breaks, yarikoptic does not describe the failure in prose. They paste the terminal
output (often with the `❯` prompt) and then append a terse fix directive at the end, sometimes
with a rule-update instruction too.

**Pattern**:
```
[problem statement, 1 sentence]

❯ [command]
[full terminal output]

[fix directive, 1 sentence]
```

## Verbatim examples

**Tox failure with rule update:**
```
add to spec and CLAUDE.md to never auto-commit if 'tox' testing fails.  ATM for me 

duplication: exit 8 (1.31 seconds) /home/yoh/proj/bids/bids-utils> pylint --disable=all --enable=duplicate-code src/bids_utils/ pid=2712017
.pkg: _exit> python ...
  py310: OK (8.86=setup[7.69]+cmd[1.17] seconds)
  lint: FAIL code 1 (2.97=setup[2.94]+cmd[0.03] seconds)
  type: FAIL code 1 (3.08=setup[1.45]+cmd[1.63] seconds)
  duplication: FAIL code 8 (2.64=setup[1.34]+cmd[1.31] seconds)
  evaluation failed :( (26.44 seconds)


so make sure that all testing passes, fix and commit .
```

**Test skip observation:**
```
I have lots of tess skipped without stating a reason:

❯ tox -e py312 -- -s -v -k test_bids_examples | grep SKIP
tests/integration/test_bids_examples.py::TestRenameSweep::test_rename_dry_run[atlas-AAL] SKIPPED
...

could you enhance stating a reason there
```

**Diff inspection + fix:**
```
looking at diff like 

         try:
             ds = BIDSDataset.from_path(ds_path)
         except (FileNotFoundError, ValueError):
-            pytest.skip(f"Cannot load {ds_name}")
+            pytest.skip(reason=f"cannot load dataset: {ds_name}")


state the exception in the message so it is possible to see right away on why cannot load
```

## Notes

- The `❯` prompt character is their actual shell prompt — appears in all terminal pastes
- "ATM for me" contextualizes the failure as currently reproducible on their machine
- The fix directive is always at the end, one line
- When a rule should be permanent, prepend "add to spec and CLAUDE.md to never ..."
