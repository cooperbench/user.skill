> DEVELOPER

Is our code for running experiments ready for submission as well, structure ? Information  leakage ?

> AGENT

I'll audit the repo for submission readiness — anonymization, credentials, structure, reproducibility — in parallel.

> TOOL

tool_use Agent
id: toolu_01AQRtpiebCD3coBqib21hwk
```json
{
  "description": "Audit information leakage",
  "subagent_type": "general-purpose",
  "prompt": "You are auditing a NeurIPS 2026 submission code repository at /home/<USER>/neuralips26 for **information leakage that would break double-blind review** or expose secrets. NeurIPS 2026 is double-blind: reviewers should not be able to identify authors, institutions, or infrastructure.\n\nFind and list every concrete instance (file_path:line_number when possible) of the following classes of leakage:\n\n1. **Author / personal identifying info** in source files (Python, shell, LaTeX, Markdown, JSON config), including:\n   - Personal names (\"Hung\", \"Henry\", \"Phan\", \"hungpq\", \"hpq2412\", any author name)\n   - Personal email addresses (gmail, outlook, etc.)\n   - Personal GitHub usernames or repo URLs\n   - Author affiliations (university name, lab name) — for example RMIT, the supervisor's name, team names\n\n2. **Institution / infrastructure identifiers** that would deanonymize:\n   - \"RMIT\", \"RACE\", \"race.rmit.edu.au\"\n   - AWS hostnames (`ec2-...amazonaws.com`)\n   - Internal IPs\n   - SSH key filenames (`hungphanphd.pem`)\n   - Internal URLs, Slack/Linear references\n\n3. **Credentials / secrets** even if benign-looking:\n   - API keys (OpenAI, Anthropic, HuggingFace, AWS, etc.)\n   - `.env` files with values\n   - Tokens in code\n   - Hardcoded passwords\n   - Any `.pem`, `.key`, `id_rsa` etc. checked into the repo\n\n4. **Hardcoded user paths** like `/home/<USER>/` or `/home/<USER>/` that scream a single author's machine. These don't strictly […]

> TOOL

tool_use Agent
id: toolu_011Z82qifSvuSCjqoQHBvxt6
```json
{
  "description": "Audit code submission structure",
  "subagent_type": "general-purpose",
  "prompt": "You are auditing a NeurIPS 2026 submission code repository at /home/<USER>/neuralips26 for **submission readiness in terms of structure, reproducibility, and code hygiene**. The paper is the \"RR-MoA\" (Raw-Routed Mixture of Adapters) paper, complete and ready for submission. The deadline is May 4-6, 2026 (today is May 5).\n\nBackground context (from the project's CLAUDE.md):\n- Active library: `feasibility/`\n- Experiment runners: `scripts/` (Python files like `run_rr_moa.py`, `run_adamix.py`, etc., plus shell orchestrators `run_*_race.sh`)\n- Legacy code archive: `scripts/legacy/` and a few legacy modules in `feasibility/` (`evolution.py`, `code_evolution.py`, `modal_app.py`, `proxy_gp.py`, `scores.py`, `features.py`, `viz.py`, `statistics.py`)\n- Verification: `evidence_vm/verify.py` — should exit 0 with \"PASS: 107 numeric claims\"\n- Paper: `main.tex`\n- Vendored legacy: `template_code/`\n- Datasets: `data/`, results: `results/`, figures: `figures/`\n\nYour task: produce a structured readiness assessment covering the items below. Be specific with file paths and line numbers.\n\n## 1. Repository structure & cleanliness\n- List the top-level directory tree (one level deep, plus a second level for `feasibility/` and `scripts/`). Use `ls -la` and `tree -L 2 -I '.git|__pycache__|.venv|venv|node_modules|data|results'`.\n- Is there a `README.md` at repo root? Does it explain what the code does, dependencies, how to reproduce key results, and how to run `verify.py`? If absent or thin, […]

> TOOL

tool_result
id: toolu_01AQRtpiebCD3coBqib21hwk
```
I have enough to produce the final report.

# NeurIPS 2026 Double-Blind Anonymization Audit — Findings

## CRITICAL

- **CRITICAL — `/home/<USER>/neuralips26/.env`** — Contains live API keys: `REDACTED...` (real OpenAI project key) and `GEMINI_API_KEY=AIzaSyCAep...` (real Google Gemini key). Although `.env` is `.gitignore`'d (line 6 of `.gitignore`) and is NOT git-tracked, these are live secrets sitting on disk. **Fix:** rotate both keys immediately at OpenAI/Google consoles, regardless of whether the repo gets uploaded.

- **CRITICAL — `/home/<USER>/neuralips26/hungphanphd.pem`** — A 3294-byte SSH private key in the repo root, filename embeds the author's personal identifier. Not git-tracked (covered by `*.pem` rule in `.gitignore`), but: (a) the filename itself deanonymizes if the directory is ever zipped, and (b) the key's existence on the same machine is a security risk. **Fix:** move out of the repo to `~/.ssh/` and rename; rotate the key on the server.

## HIGH

- **HIGH — `scripts/race_quick_connect.sh:6-7`** — Tracked file containing `KEY="hungphanphd.pem"` and `HOST="<REDACTED_EMAIL>"`. This single file leaks the author's name (`hungphanphd`), the institution (RMIT RACE — see HIGH below), the AWS region (`ap-southeast-2` = Sydney, narrows institution geography), and a public IP. **Fix:** `git rm scripts/race_quick_connect.sh` and add to `.gitignore`.

- **HIGH — `scripts/race_whitelist_ip.sh:1-58`** — […]

> TOOL

tool_result
id: toolu_011Z82qifSvuSCjqoQHBvxt6
```
All evidence in. Generating the report now.

---

# RR-MoA Submission Readiness Audit

Repository at `/home/<USER>/neuralips26`, audit date 2026-05-05 (T-1).

**Important context for the verdicts below:** `.gitignore` is unusually aggressive — `*.md`, `*.pdf`, `*.log`, `*.pem`, `.env`, `data/`, `results/`, `*.pptx`, `*.docx`, `*.html`, `slide_images/`, `experiments/finetune_training_data.json`, `experiments/sft_dataset.jsonl`, and `evidence_vm_private/` are all excluded. The on-disk working tree contains many scratch artifacts but **only 675 files are git-tracked**. I distinguish "in working tree" vs "tracked" throughout, since only the latter ships if the user pushes/zips from `git ls-files`.

## 1. Repository structure & cleanliness

**Verdict: NEEDS WORK** (clean if you ship `git ls-files`; messy if you tarball the working tree).

- `tree -L 2` (excluding `.git/data/results`) is in the bash output above. 19 top-level directories. 269 files in working tree, 675 tracked.
- **No top-level `README.md`.** The only README is `scripts/README.md` (lines 1-80), which is somewhat stale — it lists "AAS" and "Code Evolution" as primary methods (legacy framing) and only briefly mentions RR-MoA. It does not explain `verify.py`, dataset setup, or the LICENSE.
- **No `LICENSE` file at repo root.** A vendored MIT `template_code/LICENSE` (from upstream "ooooooover") exists but does not cover this repo's own code.
- `requirements.txt` exists at […]

> AGENT

Let me verify the two most consequential claims before reporting — the tracking status of `CLAUDE.md` and the `race_*` scripts.

> TOOL

tool_use Bash
id: toolu_01MD3zSc8iRFViPszetb1ADj
```json
{
  "command": "git ls-files | grep -E '^(CLAUDE\\.md|scripts/race_quick_connect\\.sh|scripts/race_whitelist_ip\\.sh|tasks/|experiments/|RACE_SSH\\.md)' ; echo \"---\" ; git ls-files | grep -c '_race\\.sh$' ; echo \"---\" ; git check-ignore -v .env hungphanphd.pem 2>&1 | head -5",
  "description": "Verify tracking status of high-risk anonymization files"
}
```

> TOOL

tool_result
id: toolu_01MD3zSc8iRFViPszetb1ADj
```
scripts/race_quick_connect.sh
scripts/race_whitelist_ip.sh
---
58
---
.gitignore:7:.env	.env
.gitignore:8:*.pem	hungphanphd.pem
```

> TOOL

tool_use Bash
id: toolu_01JHqQ7JNEUL6vnCtDTEyHab
```json
{
  "command": "head -25 main.tex | grep -iE 'author|thanks|anonymous' ; echo \"---author block---\" ; grep -nE '\\\\(author|thanks|email|institute|address)' main.tex | head -20",
  "description": "Verify main.tex anonymization"
}
```

> TOOL

tool_result
id: toolu_01JHqQ7JNEUL6vnCtDTEyHab
```
---author block---
39:\author{
```

> TOOL

tool_use Read
id: toolu_01TNjHsxwckHnVoX9CEF7qPW
```json
{
  "file_path": "/home/<USER>/neuralips26/main.tex",
  "offset": 35,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01TNjHsxwckHnVoX9CEF7qPW
```
35	\pgfplotsset{compat=1.18}
36	
37	\title{Raw-Routed Mixture of Adapters: A Causal Intervention for Routing Collapse in Time Series Foundation Models}
38	
39	\author{
40	  Anonymous Author 1 \\
41	  Anonymous Institution\\
42	  \texttt{<REDACTED_EMAIL>}
43	  \And
44	  Anonymous Author 2 \\
45	  Anonymous Institution\\
46	  \texttt{<REDACTED_EMAIL>}
47	  \And
48	  Anonymous Author 3 \\
49	  Anonymous Institution\\
50	  \texttt{<REDACTED_EMAIL>}
51	}
52	
53	\begin{document}
54	
55	\maketitle
56	
57	\begin{abstract}
58	Many time series foundation models (TSFMs) adapt to a target dataset by attaching a single trainable head to a frozen backbone. A single head is one-size-fits-all, yet target series mix heterogeneous regimes that a single head may underfit. The natural upgrade is to replace the single head with a mixture-of-experts (MoE) head whose router dispatches each window to a specialist. This upgrade fails on instance-normalized backbones, a dominant TSFM design class that strips each window's mean and variance before encoding. We call this failure \emph{normalization-induced routing collapse}. Once joint training makes even one backbone transformer block trainable, routing entropy falls to $0.000$. Every input is sent to a single expert; the rest are never activated. A $720$-run sweep across standard MoE rescue mechanisms recovers at most $10.9\%$ MSE, […]

> AGENT

## Verdict: Not ready as-is, but fixable in ~1–2 hours.

`main.tex` is properly anonymized (line 39: `Anonymous Author 1/2/3` / `author{1,2,3}@example.com`, no `\thanks`, no acknowledgements). `verify.py` runs clean (107/107 PASS). The problems are in the **code archive** and missing repro infrastructure.

### Anonymization — tracked-file leaks (will reach reviewers)

- **DELETE: `scripts/race_quick_connect.sh`, `scripts/race_whitelist_ip.sh`** (both tracked) — contain `hungphanphd.pem`, `ec2-13-238-161-176.ap-southeast-2.compute.amazonaws.com`, your IP, and "the professor must also whitelist…". This is a single grep from full deanonymization.
- **RENAME: 58 tracked `*_race.sh` filenames** → `*_vm.sh`. "RACE" is the public name of RMIT's HPC service (`race.rmit.edu.au`); reviewers running `git ls-files | grep race` recover the institution instantly.
- **SED comments**: ~25 tracked scripts contain "RACE VM", "RMIT", or "the professor" in comments/docstrings/echoes (e.g. `run_freeze_ablation.py:8`, `finetune_qwen.py:3`, `run_local_evolution.py:3`, `legacy/compare_results.py:102`, `run_strengthening_race.sh:7-8,122-144`). Bulk-replace to neutral language ("GPU VM", "remote GPU").
- **FIX path**: `scripts/build_bib_verification.py:135` — `out = "/home/<USER>/neuralips26/bib_verification.xlsx"` → relative path.

### Workspace landmines — gitignored but on disk

If you ship via `git archive HEAD` you avoid these. If you `tar -czf .` from cwd, all of these leak:

- **`.env`** — live `OPENAI_API_KEY` (`sk-proj-…`) and `GEMINI_API_KEY` (`AIzaSy…`). **Rotate both immediately, regardless of submission**.
- **`hungphanphd.pem`** — SSH private key in repo root; filename alone deanonymizes. […]