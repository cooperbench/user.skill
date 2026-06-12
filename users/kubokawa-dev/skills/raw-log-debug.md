---
name: raw-log-debug
description: "Trigger: CI or app fails. User drops the full log output verbatim—no diagnosis, no framing—sometimes with a brief trailing question, sometimes with nothing at all."
---

When something breaks in GitHub Actions or the local dev server, kubokawa-dev does not describe the problem in words. They paste the raw output exactly as it appears, preserving emoji from the CI script, timing markers (`0s 0s 0s`), full stack traces, and surrounding context lines. Commentary is minimal or absent.

**Pattern**:
1. (Sometimes) a one-line setup: `日次予測のgithub actionsで下記でこけています`
2. Raw log paste — unformatted, no code fences
3. (Optional) trailing question: `ここでテストこけているよ？修正調整おねがいできますか？？` or `みえてないんですよねー` or nothing at all

**Example 1** (with brief header):
```
日次予測のgithub actionsで下記でこけています　Run python tools/load_numbers4_daily_json_to_postgres.py --skip-if-unconfigured --chunk-size 12
🔑 環境変数（NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY）を使用します
📂 対象 654 件（パターン外・対象外スキップ 2）
🔌 PostgREST UPSERT（chunk=12）…
   … 12 / 654 件送信
❌ PostgREST HTTP 502 (chunk 4): error code: 502
Error: Process completed with exit code 1.
```

**Example 2** (log paste + trailing question):
```
    print(f"saved: {out_path.relative_to(ROOT)}")
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../pathlib.py", line 730, in relative_to
    raise ValueError("{!r} is not in the subpath of {!r}"
ValueError: '/tmp/numbers4_target_check.md' is not in the subpath of '...'
Error: Process completed with exit code 1.
0s
0s

ここでテストこけているよ？修正調整おねがいできますか？？
```
