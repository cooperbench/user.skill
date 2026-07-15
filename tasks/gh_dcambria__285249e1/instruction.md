You are role-playing the software developer in an ongoing AI coding-agent session.

The full conversation so far is in `/sim/history.md`. Each turn starts with a markdown
blockquote role label (`> DEVELOPER`, `> AGENT`, `> SYSTEM`, `> TOOL`, or `> METADATA`),
then the turn body. `DEVELOPER` is the human to imitate; `AGENT` is their coding agent.
`SYSTEM`, `TOOL`, and `METADATA` are context observed by the original agent, not
developer-authored messages. It MAY be long (thousands of lines) — read it however you
need: `cat`, `tail`, `head`, `grep`, `sed`, etc.

Your job: write the SINGLE next message THIS developer would type to their coding agent right
now — in their own language, length, casing, punctuation, typos and all. Do not solve their
problem, do not explain, do not add role labels or quotes — just the literal message text they
would send.

Write ONLY that literal message to `/sim/answer.txt` (overwrite it). No commentary anywhere else.

Developer style profiles are NOT part of the task. Inject them at job time as Harbor skills
(`--skill` / `agents[].skills`) in Agent Skills format.
