# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
A Python research pipeline (`README.md`) that distills SWE-chat users into role-playable
"user folders" (`users/<slug>/`) and validates the personas by held-out next-message
prediction. It is a set of CLI scripts in `scripts/` — there is no web server, service, or GUI.
The human-facing deliverable is `results/report.html`.

### Python environment
- Dependencies live in a virtualenv at `.venv/` (created by the update script from
  `requirements.txt`: `pandas`, `pyarrow`, `sentence-transformers` + torch).
- Run everything with the venv interpreter, e.g. `.venv/bin/python scripts/report.py`
  (or `source .venv/bin/activate` first). The system `python3` does NOT have the deps.

### What runs offline vs. what needs external access
The pipeline has four stages; two require resources that are **not** present in this
environment, so scope local work accordingly:

| Stage | Command | Runs here? |
|---|---|---|
| Report | `.venv/bin/python scripts/report.py` | Yes — reads committed `results/*.json`, writes `results/report.html`. |
| Embedding scoring | the `SentenceTransformer` path in `scripts/validate.py` | Yes — downloads `paraphrase-multilingual-MiniLM-L12-v2` from HuggingFace on first use (needs network). |
| Prepare data | `scripts/prepare_data.py` | No — needs the SWE-chat parquet dataset (expects `/home/ubuntu/SWE-chat`, absent). |
| Distill / LLM-judge validation | `scripts/distill.py`, LLM parts of `scripts/validate.py`, `scripts/build_local_profile.py` | No — need the `claude` CLI and an Anthropic API key (neither is installed/set). |

- `data/` is gitignored and regenerable; it is empty until `prepare_data.py` is run against
  the dataset.
- Running `scripts/report.py` without the (uncommitted) `results/folder_v2_9users.json`
  intermediate simply omits that one "intent-first prompt" row from the report — this is
  expected, not a failure. Restore `results/report.html` with `git checkout` if you don't
  intend to change the committed artifact.

### Lint / test
There is no configured linter or test suite (no `pyproject.toml`, `pytest`, `ruff`, etc.).
`python -m py_compile scripts/*.py` is the available syntax sanity check.
