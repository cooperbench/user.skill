---
name: bare-correction
description: When the agent produces something wrong, Tiryoh replies with only the corrected value or a one-sentence directive — no preamble, no explanation of what was wrong.
---

Corrections are the bare minimum needed to convey the fix. If a number is wrong, state the right number. If a language is wrong, state what language to use. No "you made a mistake" framing, no politeness padding.

Examples:

- Agent put `Copyright 2025 Tiryoh` in the LICENSE → user replied: `2026です`
- Agent mixed up Agent and User roles in transcript display → user replied: `transcriptの表示でAgentとUserが混同されています。確認して`
- Agent generated Japanese README when English was expected → user replied: `READMEを英語にして。日本語版についてはREADME.jp.mdにしてREADMEからリンクするようにして`

The correction is always a directive ("confirm it", "make it English") or a bare fact ("2026"), never a question or a negotiation.
