---
name: error-paste-debug
description: Reporting failures by pasting raw terminal output or status text verbatim; trigger when something broke or didn't work as expected
---

When something fails, this user pastes the raw error or status output as the entire prompt — usually with zero commentary, or at most a one-line label. They do not summarize or paraphrase errors. Screenshots also appear alone ("[Image: image/png]") as the entire message when the failure is visual.

Occasionally a brief observation is prepended as a sentence fragment or rhetorical note. The user rarely asks "why did this happen" — they expect the agent to diagnose from the paste.

**Verbatim examples:**

Raw paste with no commentary:
> "1. Firebase Intercommunication Availability: The Firebase intercommunication channel is fully functional. The health check confirms successful read and write operations to Firestore. 2. Agent Registration: While the communication channel is open, HYPERION is not yet registered..."
[user pasted Hyperion's own report as a bug report]

Paste with minimal label:
> "i do recieve a: \" Bash(/usr/bin/python3 /Users/sa/rh.1/ops/rhea_firebase.py health 2>&1)\n  ⎿  FIRESTORE HEALTH PROBE...\n  ⎿  API Error: 400 You have exceeded your daily token limit. You can resume at 2026-02-18 00:00 UTC.\""

Short one-line failure reports:
> "nothing happend after click\n[Image: image/png]"

> "the alarm is still ringing)"

> "why have you stopped"

> "the important poing: i im fully ready to test thism, but CHP has basic subsriptin and pretty much limited"

Debugging with a confused observation:
> "~/rh1 and /Users/sa/Library/Mobile Documents/com~apple~CloudDocs/ is so significant different an the mp3 file you pointed... well.. this is becomes ridicolouss"
