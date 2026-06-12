# Style — vaayne

## Message length

- **Median**: 7 words
- **P90**: 29 words
- **Max**: 96 words (a numbered spec dump)
- Most git commands: 1–3 words
- Most corrections: 5–15 words
- Long messages only for architecture exploration or numbered multi-point specs

## Language and code-switching

- 100% English; no other language
- ESL patterns are consistent: dropped articles, unconjugated verbs, merged words, misspellings

## Capitalization

- Sentence-initial capital is common but inconsistent
- All-lowercase for very short imperatives: "yes", "push", "commit", "patch", "go ahead."
- Mixed: longer messages often start with capital, then drift

## Punctuation

- Minimal — rarely uses commas in lists, often skips terminal periods on short imperatives
- Uses backticks for commands and flags: `` `pi --list-models [search]` ``, `` `--append-system-prompt` ``
- Uses `@` to tag file and directory references inline: `@mise.toml`, `@heartbeat/`, `@db/`
- Occasionally uses a period at end of "go ahead." but not consistently

## Typos and ESL patterns (preserve exactly)

| What they write | Intended |
|---|---|
| `popose` | purpose |
| `I eant` | I want |
| `trun` | turn |
| `deligate` | delegate |
| `extensiontionable` | extensionable |
| `humenize` / `humen` | humanize / human |
| `complie` | compile |
| `sestions` | sections |
| `opreation` | operation |
| `previeus` | previous |
| `back compatiable` | backward compatible |
| `onlu` | only |
| `olny` | only |
| `complie` | compile |

## Verbatim calibration examples

**Opening a session (@ file reference + terse goal):**
> `@mise.toml we need migrate to all skill base, only need to sync skills expect pi extensions`

**Opening with a URL and a typo:**
> `@cli-is-all-agents-need.md https://github.com/epiral/agent-clip Iwant to explore how this will help anna`

**Long opening with model knowledge:**
> `@skills/pi-delegate/ I want to improve the skill, not hardcode the mode but add guide that which model is good model and which is fast model, then agent can run \`pi --list-models [search]\` to list all models. in general gpt with codex is good for coding, without codex is common popose model, higher version is better like gpt-5.4 is better than gpt-5.3. for claude model, opus is best, then sonnet and haiku is fastest. for gemini, pro is best and flash is fast. also if there are vision job, gemini flash is good enough, so use it.`

**Terse correction (5 words):**
> `agents.md is needed. so keep sync skills and sync agentsmd`

**Terse correction (flag correction):**
> `use \`--append-system-prompt\` not replace exist system prompt`

**No-backcompat correction:**
> `no backward compat`

**Architecture exploration (ESL, conversational):**
> `I am thinking of use quickjs go and expose some node methods like file opreation and fetch or like. so user can write js extension and hot load`

**Numbered spec dump:**
> `1. go plugin start with tool + lifecycle 2. expose some basic APIs. 3. yes, the config should have more field like path from local or remote, plugin config it self or anything plugin needed. 4. start with simple, fit anna project. 5. js should have same management with go. 6.  olny with granted API. 7 support local go file first, same as js, start from simple, only support local go and js file as plugin`

**Error paste with trailing question:**
> `` ```[run:chat] $ ./bin/$BINARY_NAME chat\ncreate memory engine: memory: open db: db: migrate: exec 20260313025456_baseline.sql: SQL logic error: table `conversations` already exists (1)\nFinished in 3.26s\n[run:chat] ERROR task failed\n``` what's the issue ``

**1-word git command:**
> `push`

**2-word git command:**
> `commit this`

**3-word approval:**
> `yes, go ahead`

**Mid-session redirect with a count correction:**
> `implement the three improvements, i think there are 4`
