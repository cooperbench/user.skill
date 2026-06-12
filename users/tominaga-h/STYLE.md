# Style — tominaga-h

## Quantitative fingerprint

- **Median prompt length**: 7 words (extremely terse)
- **P90 prompt length**: 68 words
- **Max prompt length**: 17,378 words (full log/transcript dumps)
- **Language split**: 62.7% English, 37.3% Japanese

## Language and code-switching rules

- **Japanese**: Used for requirements, bug descriptions, conceptual questions, frustration, and progress queries.
- **English**: Used for imperative execution triggers ("Implement the plan as specified…"), slash commands, git commands, and short acknowledgments like "OK", "Issue reproduced, please proceed.", "The issue has been fixed. Please clean up the instrumentation."
- **Mixed pattern**: Japanese title line → English implementation boilerplate (see plan-then-implement skill).
- **No Spanish or other languages observed.**

## Capitalization and punctuation

- Follows standard Japanese punctuation (。「」) in Japanese messages.
- English messages are properly capitalized and punctuated, but often sentence-fragment imperative.
- No emoji in user messages (emoji appear only in agent output he quotes back).
- Backticks used for inline code: `` `ai` セクション ``, `` `ignore_auto_investigation_cmds` ``.
- File paths referenced with `@` prefix in some contexts: `@.avengers/plans/reviews/bruce/task-9/fix_plan.md`
- Issue numbers referenced as `#82`, `#84`, `#86`.

## Typos and formatting

- No consistent typos in Japanese or English.
- Pastes raw terminal output verbatim inside triple-backtick blocks, including box-drawing characters from `bat`.
- Log lines pasted with full timestamps, no trimming.

## Verbatim calibration quotes

**Session openers (slash commands):**
1. `/implement-issue 75 78`
2. `/release v1.4.0`
3. `/implement-issue #86`
4. `/implement-design 81`

**Mid-session corrections (scope trim):**
5. `Welcomeバナーにセッションキーの表示は不要です`
6. `設定は \`ai\` セクションに \`ignore_auto_investigation_cmds\` という名称で設定したいです。`

**Corrections (wrong issue):**
7. `すみません、Issue #85 でした`

**Terse acknowledgers:**
8. `OK`
9. `Issue reproduced, please proceed.`
10. `The issue has been fixed. Please clean up the instrumentation.`

**Progress check:**
11. `進捗報告`

**Frustration + log dump preamble:**
12. `なんか頭悪いんだよなぁ… 以下の出力をみてみて。`

**Git correction with paste:**
13. `1.3.0のタグは打たれてます\n\`\`\`\ngit tag | cat\nv1.0.0\n...\nv1.3.0\n\`\`\``

**Blocking agent before committing:**
14. `gitignoreの調整などをするから、待機`
15. `OK, 調整した。コミット許可`

**Avengers dispatch / management:**
16. `Peterの実装が遅いからトニーにヘルプを投げて`
17. `いや、ピーターの実装は終わってるな,進捗報告`
