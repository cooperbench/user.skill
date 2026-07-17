# SWESimBench v2 cohort policy decisions

Authoritative thresholds and predicates live in
`/data/claude-crawl/cohort_policy.py` (`POLICY_VERSION`,
`policy_fingerprint()`). This file records **why** selected gates exist.

## Secrets + PII scrub (2026-07-16)

Light regex scrubbing (API keys + SpecStory-style email / `/Users|/home`
username redaction) lives in `cohort_policy.scrub_text` and runs during
`build_clean_cohort.py` / `prepare.py` / `export_train_markdown.py`.

Heavy release scrubbing (Joe-style Presidio NER + TruffleHog verified secrets)
is a post-pass: `pii_redaction/scrub_artifacts.py` (see
`pii_redaction/README.md` for the step mapping to
`SWE-chat-private/release/pii_redaction/`). Reports land in
`meta/pii_scrub_report.json` and `meta/pii_scrub_verify.json`.

## Maximum human user-turn length (1000 cl100k tokens) — 2026-07-14

**Rule:** When selecting eval / prediction points (`prepare.py`, ATIF sample
builders), skip any human-target user message longer than **1000 tokens**
under OpenAI’s **`cl100k_base`** encoding (`tiktoken`). Sessions that contain
such turns are still retained in the clean cohort — megapastes may appear in
history context, but they are never chosen as the turn to predict.

Predicate: `is_predictable_human_turn()` (= human target and not
`is_oversized_human_turn()`).

Counting uses `developer_text()` first (Cursor `<user_query>` body when
present), then `tiktoken.get_encoding("cl100k_base").encode(...)`.

**Why**
- Clean-cohort user turns are typically short (median ~12 whitespace-words in
  exploratory stats).
- Sampled turns near 500 / 1000 / 2000 whitespace-words: ~500 can still be a
  real ask wrapped in IDE context; ≥1000 is dominated by bulk pastes (console
  dumps, kubectl/log walls, “summarize this conversation” blobs).
- Cap is framed in **tokens** (model units), not whitespace words.
- Skipping only at point selection (not dropping whole sessions) keeps
  developers/sessions in the cohort while avoiding unrealistic mega-pastes as
  prediction targets.

**Why not ~400**
- Entire harvest caps turns at ~300 words and DataClaw at ~400 words. A gate
  near those values would mostly measure source harvest caps, not realism.

**Not in scope**
- Assistant turn length is uncapped by this rule.
- Display truncation in `prepare.py` (`CTX_WORDS`) is separate and only
  affects rendered context strings.

**Policy version:** `swesimbench-v2-cohort-policy-2026-07-13.15`
(`TURN_LENGTH_THRESHOLDS.encoding = cl100k_base`,
`maximum_human_target_tokens = 1000`).

## Memory notes (rebuild)

`build_clean_cohort.py` keeps full session text (including long pastes) so
sessions stay intact. RAM mitigations: lazy `sequence` materialization, and
the multi-GB pickle cache disabled (`ENABLE_CANDIDATE_CACHE = False`).
tiktoken short-circuits on very long strings when checking prediction-point
eligibility. Delete `.clean_candidates.cache.pkl` if an old fat cache is
present.
