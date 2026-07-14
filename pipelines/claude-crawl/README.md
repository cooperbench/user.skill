# SWESimBench v2 cohort — 100 Claude Code / Codex users

**Goal:** 100 users, each with ≥400 training + ≥100 held-out user turns, from later non-overlapping
sessions; coding agent must be **Claude Code or Codex**; full (or close-to-full) native JSONL traces,
not lossy SpecStory markdown; minimal source count.

## Deliverable
- `meta/final_100.json` — 100 users. Per user: `sources`, `train_turns`, `held_turns`, and the
  `train_sessions` / `held_sessions` lists (session id + timestamp + user-turn count).
  99 strictly meet ≥400 train / ≥100 held; 1 (`gh:MabudAlam`, `meets_400:false`) is a genuine
  Claude Code human at 385 train / 102 held — 13 turns short of a clean split, included as the
  100th and transparently flagged.
- `meta/census_cc.json` — full census (all users incl. near-misses).
- `census_cc.py` — the census builder; `MINTRAIN=<n>` env var sets the train threshold.

## Sources (minimal set — all native full-trace Claude Code / Codex JSONL)
| source | qualified users | what it is |
|---|---|---|
| Entire checkpoints (+ SWE-chat) | 62 | `full.jsonl` committed to `entire/checkpoints/v1`; Claude Code + Codex, full user+assistant turns. SWE-chat (the packaged HF parquet of the same data) is merged and deduped by session id. |
| GitHub `.claude`/`.codex` crawl | 29 | committed `~/.claude/projects` & `.codex/sessions` dumps, discovered by tree-probing 4,612 repos, harvested with preserved sparse git clones. |
| DataClaw (HF donors) | 9 | per-donor `conversations.jsonl`; filtered to `claude*` / `codex` agent sources only. |

Pi, SpecStory, WildChat, cursor/opencode/gemini sources are **excluded** (not Claude Code/Codex, or
lossy). Three source families, one shared native-JSONL parser (`parse_claude.py`, Claude Code +
Codex) plus the DataClaw JSONL and SWE-chat parquet readers.

## Integrity (verified)
- **Disjoint sessions**: no session id in both a user's train and held-out sets; snapshot re-saves
  collapsed by content fingerprint.
- **Temporal ordering**: train/held boundary falls strictly between distinct timestamps — every
  training session precedes every held-out session. Verified: 0 split failures.
- **No cross-user contamination**: 0 session ids shared between two users (Entire fork-duplicated
  checkpoints deduped globally by session id, richest copy wins).
- **Real user turns only**: injected scaffolding (tool results, `<task-notification>`, IDE/hook
  wrappers, Codex `<environment_context>` etc.) excluded from counts.
- **Automation screened out**: org/bot/dogfood accounts (`entireio`), benchmark harnesses
  (`wolffbe` = 1,201×1-turn ml-platform prompts, `codeset-ai`, `tbench-runs`, `PGxQA-Harbor`, …),
  and observer scaffolding (`austinweitao` claude-mem) excluded; same-person accounts merged
  (`skogai`→`SkogBackup`).

## Cohort shape
Train turns: min 385 · median ~907 · max 17,539. Held turns: min 100 · median ~108 · max 465.
Full traces must be used for every retained source. Rebuild DataClaw from
`/data/dataclaw/raw/` with `reparse_dataclaw.py`; the clean cohort builder rejects the legacy
400-word-truncated corpus.

## Note on the ceiling
Committed public Claude Code/Codex agent dumps are a genuinely thin slice of GitHub (publishing raw
sessions is rare — privacy, secrets, gitignore, file size). After exhaustive enumeration (no
capped search partitions), tree-probing, harvest, and automation screening, the strict-≥400 genuine
population across these sources is **99**; MabudAlam (385) is the flagged 100th. Raising the bar to
≥1000 train yields ~62; lowering to ≥250 yields ~120+.
