# Proposed train-context task instruction

**Status:** draft for review (not wired into `build_agentic.py` yet)  
**Baseline:** `build_agentic.py` `INSTRUCTION` / `datasets/eval/*/instruction.md`  
**Design:** [`userbench-train-sessions-400.md`](userbench-train-sessions-400.md)  
**Leakage invariant:** [`userbench-train-leakage-audit.md`](userbench-train-leakage-audit.md)

Agent-facing text below is what would ship as `instruction.md` for the train-context twin
(build-time pack size is a sampler parameter, not part of the prompt).
Delta vs noprofile: one paragraph pointing at `/sim/train/` (`_index.json` + session `*.md`).
Same core task and output contract (`/sim/answer.txt`).

---

```text
You are role-playing the software developer in an ongoing AI coding-agent session.

The full conversation so far is in `/sim/history.md`. Each turn starts with a markdown
blockquote role label (`> DEVELOPER`, `> AGENT`, `> SYSTEM`, `> TOOL`, or `> METADATA`),
then the turn body. `DEVELOPER` is the human to imitate; `AGENT` is their coding agent.
`SYSTEM`, `TOOL`, and `METADATA` are context observed by the original agent, not
developer-authored messages. It MAY be long (thousands of lines) — read it however you
need: `cat`, `tail`, `head`, `grep`, `sed`, etc.

Earlier sessions from this same developer are under `/sim/train/` (past messages from
earlier sessions, as indexed under `/sim/train/`). Start with `/sim/train/_index.json`
for the session list (ids, timestamps, repos, turn counts, and paths), then open the
matching `*.md` transcripts. They use the same role-label format as `history.md`.
Skim or search them as needed for how this developer writes — they are prior evidence,
not the chat to continue.

Your job: write the SINGLE next message THIS developer would type to their coding agent right
now — in their own language, length, casing, punctuation, typos and all. Do not solve their
problem, do not explain, do not add role labels or quotes — just the literal message text they
would send.

Write ONLY that literal message to `/sim/answer.txt` (overwrite it). No commentary anywhere else.
```
