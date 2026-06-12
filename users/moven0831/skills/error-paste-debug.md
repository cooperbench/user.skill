---
name: error-paste-debug
description: >
  Triggered when something fails at runtime. moven0831 pastes the full log verbatim,
  labeled by source (blockchain node / relay / terminal), wrapped in triple-quotes with
  backslash line separators. The framing is one line or less; the log does the talking.
---

When a test or command fails, moven0831 pastes the raw output in a structured block:

**Pattern**:
```
<one-line question or context>\\ Log from <source>: \"\"\"\\ <full log content>\\ \"\"\"
```

Multiple log sources are stacked in sequence. No summary of what went wrong — the user expects the
agent to read and diagnose the log itself.

**Verbatim examples**:

Short trigger, single log:
```
what about now
```
(no log in this case — just checking if previous fix worked)

Long form with two log sources:
```
why are these error\\ Log from the blockchain node: \"\"\"\\ eth_sendRawTransaction Contract call: Unirep#userStateTransition Transaction: 0x863afc... \\ \"\"\"\\ \\ Log from the relay: \"\"\"\\ Epoch 0 ended Epoch 1 ended [signup] Error: <ref *1> Error: cannot estimate gas...\\ \"\"\"
```

After agent gives revised fix, same pattern repeats:
```
Got an error.\\ Log from blockchain node: \"\"\"\\ eth_chainId (2) eth_call Contract call: Unirep#attesterCurrentEpoch...\\ \"\"\"\\ \\ Log from the relay: \"\"\"\\ ❯ yarn relay start Listening: http://127.0.0.1:3000...\\ \"\"\"
```

Simpler failure report:
```
got this error when post anonymously\\ \\ Log from blockchain node: \"\"\"\\ ...\\ \"\"\"\\ \\ Log from relayer: \"\"\"\\ ...\\ \"\"\"
```

**Key traits**:
- Never summarizes the error in their own words
- Always includes the raw log, even if it's hundreds of lines
- Source labels are consistent: "blockchain node", "relay", "terminal"
- Repeats the same pattern each failure cycle until it works
