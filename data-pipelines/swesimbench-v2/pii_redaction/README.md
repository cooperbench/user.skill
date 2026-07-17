# SWESimBench secrets + PII scrub pipeline

Closes gaps between the Harbor cohort path (regex-only `cohort_policy.scrub_text`)
and Joe's SWE-chat-private release pipeline (`release/pii_redaction/`), plus
SpecStory-style email / home-path redaction.

## Mapping to Joe's steps

| Joe (`release/pii_redaction/`) | Harbor (`pii_redaction/`) |
|---|---|
| 1. `extract_turns` (user/assistant only) | `pipeline.iter_nl_turns` / artifact walkers — NL roles only for Presidio |
| 2. `run_presidio_ner` (spaCy trf + GPU) | `presidio_engine.analyze` — CPU `en_core_web_sm` (no GPU here) |
| 3. `count_entity_freqs` | Optional `--collect-freqs` / `entity_freqs.json` (default: validators only) |
| 4. `redact_PII` (validators + code-fence guard) | Same validators in `validators.py` + `code_spans.py` |
| 5. `redact_trufflehog` (verified secrets on turns) | `trufflehog.scan_and_redact` |
| 6. `apply_redactions` onto transcripts | `scrub_artifacts.py` rewrites canonical files in place |
| 7. `redact_secrets_global` (tool/system/diffs too) | Global TruffleHog pass over whole artifact text |
| SpecStory `redact.py` email + `/Users\|/home` | `regex_scrub.py` (also wired into `cohort_policy.scrub_text`) |

**Not ported (intentionally):** torch `.pt` chunk sharding / SLURM array jobs —
Harbor artifacts are JSONL + markdown trees; we stream them instead.

## Stages (order)

1. **Regex** — existing `SECRET_PATTERNS` + email + `/Users/<name>` + `/home/<name>` (+ Windows `C:\Users\…`)
2. **Presidio NER** — user/assistant (or DEVELOPER/AGENT) natural language only; skip fenced/inline code spans; Joe-style validators
3. **TruffleHog** — verified findings; global string replace across the artifact

Idempotent placeholders (`[REDACTED_*]`, `<REDACTED_EMAIL>`, `/home/<USER>`, `<PRESIDIO_ANONYMIZED_*>`, `<TRUFFLEHOG_REDACTED_*>`) so a second pass is a no-op.

## Install

```bash
python3 -m venv /data/swesimbench-v2-harbor/.venv-pii
source /data/swesimbench-v2-harbor/.venv-pii/bin/activate
pip install -r /data/swesimbench-v2-harbor/pii_redaction/requirements.txt
python -m spacy download en_core_web_sm
# TruffleHog binary (if missing):
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /data/swesimbench-v2-harbor/.local/bin
```

## Usage

```bash
# Full clean of canonical train + eval artifacts (backs up large files first)
run-heavy /data/swesimbench-v2-harbor/.venv-pii/bin/python -u \
  /data/swesimbench-v2-harbor/pii_redaction/scrub_artifacts.py \
  --targets train,eval,v2tasks \
  --report /data/swesimbench-v2-harbor/meta/pii_scrub_report.json

# Verify idempotency + spot-check residual patterns
run-heavy /data/swesimbench-v2-harbor/.venv-pii/bin/python -u \
  /data/swesimbench-v2-harbor/pii_redaction/verify_scrub.py \
  --report /data/swesimbench-v2-harbor/meta/pii_scrub_verify.json
```

Light regex scrubbing remains in `cohort_policy.scrub_text` so
`build_clean_cohort.py` / `prepare.py` / `export_train_markdown.py` stay covered
on rebuild. Presidio + TruffleHog are a **release post-pass** (too heavy for
per-turn build loops).
