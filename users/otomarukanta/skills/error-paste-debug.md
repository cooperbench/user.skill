---
name: error-paste-debug
description: >
  Trigger: the user runs the built binary or tests against a real API/service and gets an error.
  They paste the error text verbatim, then append a short Japanese diagnosis or question.
---

The user does not describe the error — they paste it. English error text comes first, then a
Japanese postfix on a new line or after `\n`. The postfix is either a simple report
("〜で失敗した") or a hypothesis ("〜からでは？").

**Example 1 — simple report**:

> `"redirect_uri did not match any configured URIs. Passed URI: http://localhost:9876\nというエラーがSlack側で出た"`

Translation: "Got this error on the Slack side."

**Example 2 — same error, hypothesis added after second failure**:

> `"redirect_uri did not match any configured URIs. Passed URI: http://localhost:9876\n同じエラーのままです。Redirect URLsにhttpsが登録できないからでは？"`

Translation: "Still the same error. Maybe it's because Redirect URLs can't be registered with https?"

**Example 3 — TLS error**:

> `"Error: failed to read from TLS stream: received fatal alert: CertificateUnknown で失敗した"`

Translation: "Failed with CertificateUnknown."

**Structure**: `<verbatim error text>\n<Japanese postfix>`

The Japanese postfix vocabulary:
- `というエラーがSlack側で出た` — "got this error on the Slack side"
- `で失敗した` — "failed with [error]"
- `同じエラーのままです` — "still the same error"
- `〜からでは？` — "isn't it because 〜?"

The user does NOT add stack traces beyond what the runtime emits. They do NOT add context about
what they tried. They expect the agent to read the error and act.
