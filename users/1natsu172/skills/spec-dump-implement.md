---
name: spec-dump-implement
description: >
  How 1natsu172 kicks off implementation after planning. They exit plan mode,
  then forward the full AI-generated plan text verbatim as a message prefixed
  with "Implement the following plan:". Trigger: they have completed a planning
  session and are ready to implement.
---

# Spec-Dump Implement

After exiting EnterPlanMode, 1natsu172 forwards the full AI-generated plan back to the agent as a single large message. The plan text is verbatim agent output — markdown headers, code blocks, tables, Japanese mixed with English — with a fixed prefix. This is the dominant pattern for starting non-trivial implementation tasks.

## Verbatim example (abbreviated)

```
Implement the following plan:

# Plan: 1natsu-create-pr スキルに language 引数を追加

## Context

現在の `1natsu-create-pr` スキル（v1.2.0）はステップ2で「ユーザーが指定した言語を使用する。指定がなければ英語をデフォルトとする」と記載しているが、引数としての指定方法が定義されていない。...

## 変更対象ファイル

- `skills/1natsu-create-pr/SKILL.md`

## 変更内容

### 1. frontmatter に `argument-hint` を追加
...

If you need specific details from before exiting plan mode..., read the full transcript at:
/Users/1natsu/.claude/projects/.../xxxx.jsonl

If this plan can be broken down into multiple independent tasks, consider using the TeamCreate tool to create a team and parallelize the work.
```

## Characteristics

- Prefix is always exactly: `Implement the following plan:` followed by a newline and the plan
- Plan may contain Japanese section headers, English code blocks, YAML, tables
- The trailing footer ("If you need specific details...") is always agent-generated boilerplate, not 1natsu172's own words
- After this message, they expect the agent to execute silently and report only completion status

## What this means for roleplay

- When asked to implement a previously planned feature, use this prefix + plan format
- The plan body is AI output being forwarded — match the style (markdown headers, Japanese/English mixed) of the agent's planning output
- Do NOT add your own preamble or context before "Implement the following plan:"
- The user's authentic voice will not appear in this message — it is entirely the plan text
