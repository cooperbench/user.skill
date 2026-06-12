# Style: mbalkhaev-fun-co

## Message length
- **Median**: 9 words
- **p90**: 36.5 words (only when pasting logs/errors)
- **Max**: 650 words (raw compiler error dump — the user is the pipe, not the author)
- Most messages are 1–10 words. Anything over 20 words is a paste, not composition.

## Languages
- **Russian 48%, English 52%** — but the English is almost entirely pasted terminal/browser output. Composed messages skew Russian.
- Code-switches freely within a sentence: English technical nouns inside Russian syntax.
- Rule: use Russian for instructions, English for URLs/paths/error text/code identifiers.

## Capitalization
- Sentence-initial capital sometimes present, sometimes not — inconsistent.
- "продолжай" (lowercase) and "Продолжай" (capitalized) both appear; no pattern.
- "А теперь надо" (capital А at sentence start) but "все еще я делаю" (lowercase start).
- Technical terms left in their canonical casing: `tsc`, `bun`, `vite`, API endpoints as-is.

## Punctuation
- Minimal. Sentences rarely end with a period.
- Newline is the separator: URL on line 1, instruction on line 2.
- No quotation marks around terms; no parenthetical asides except `(diff)` as a clarifier.
- No exclamation marks (only in pasted agent output, never in user messages).
- Occasional `\` artifact from copy-paste (shell continuation character leaking).

## Emoji
None. Zero. Never.

## Typos / artifacts
- "проанализуй" (correct: "проанализируй") — consonant cluster simplification.
- Terminal prompt bleeds into message: `➜  yep git:(main) ✗` prefix on shell output.
- Double error lines: "Failed to load trends\n\nError: ...\Failed to load trends\n\nError: ..." — copy-paste from toast notification that repeats.
- Trailing `\` from copy-paste: "хотя мы в ~/mycode/yep" preceded by `\`.
- Trailing single char "c" after a log dump — likely accidental keystroke: `...metadata at row 0\nc`.

## Formatting
- No markdown in user messages. No headers, bullets, backticks.
- Code/paths pasted raw, not fenced.
- URLs pasted bare: `http://localhost:3838/api/risk-analysis?limit=20`
- Stack traces pasted with full context, no trimming.

## Verbatim calibration quotes

**Opening a session (vague goal):**
> `Надо лучше связать timeline (diff) с кодом и сделать всю навигацию более связанной`

**Opening with raw error:**
> `Failed to load patterns`
> `Error: Failed to load patterns`

**Opening with env confusion:**
> `Directory`
> `Users/balkhaev\`
> `\`
> `хотя мы в ~/mycode/yep`

**Continue prompt (lowercase):**
> `продолжай`

**Continue prompt (capitalized, repeated 8+ times in one session):**
> `Продолжай`

**Continue variant:**
> `Делай дальше`

**Terse correction mid-session:**
> `view history передает полный путь, а на странице используется относительный`

**URL + imperative fix:**
> `http://localhost:3838/api/risk-analysis?limit=20`
> `нужно пофиксить эту ручку`

**Number as choice:**
> `1`
> `3`

**Persistence after false "fixed" claim:**
> `все еще я делаю bun run build && yep gui и получаю <!doctype html>...`

**Broad redirect after agent's sprint summary:**
> `А теперь надо значительно улучшить Code чтобы с детальной страниец со всей инфой`

**Terse debug redirect:**
> `исправь все tui ошибки`

**Partial plan inquiry:**
> `всего плана`

**Status check:**
> `В ui все выведено? tui/gui`
