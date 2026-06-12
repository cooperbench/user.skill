# Style — matthsena

## Message Length

- **Median:** 17 words
- **p90:** 106 words
- **Max:** 675 words (always "Implement the following plan:" dumps — pre-authored specs, not organic messages)
- **Typical short messages:** 2–15 words. Most corrections and steering are one to three sentences.

## Language

58.6% Portuguese, 41.4% English. Switches freely:
- Portuguese for casual remarks, debug descriptions, UI feedback, emotional reactions
- English for imperative commands to the agent ("fix all and commit without coauthor", "please continye", "entire status")
- Sometimes mid-message: "agora quero que vc crie um script de build em @package.json de forma que instale essa CLI global no path e eu iniciando com reef no terminal ja inicia o agene!!"

## Capitalization

- Minimal. Almost never capitalizes mid-sentence proper nouns, file paths, or commands in Portuguese.
- English commands are lowercase: "so commit each single test without you as coauthor"
- Sentence-initial caps inconsistent: sometimes yes, often no.

## Punctuation

- Uses "!!" for excitement/confirmation, not single "!".
- Minimal commas; uses ";" as a list separator within Portuguese sentences.
- No Oxford comma.
- Ellipsis "..." used for trailing continuation or uncertainty.
- Question marks: present but not always.

## Diacritics

**Drops most accents** in Portuguese. Consistent patterns:
- "não" → "nao"
- "você" → "voce" or "vc"
- "também" → "tambem"
- "então" → "entao"
- "atenção" → "atençao" (occasional slip keeps the cedilla)
- "já" → "ja"

## Typos

- "please continye" (→ continue) — recurring typo under impatience
- "agente" → "agene" in one instance
- "autocoplete" (→ autocomplete)
- "coreviwer" / "reviwer" / "codereviwer" — inconsistent spelling of "reviewer"

## Formatting

- **File paths:** prefixed with `@` (e.g., `@src/types.ts`, `@package.json`) when referencing files inline
- **Backticks:** used in long plan dumps but not in casual messages
- **Screenshots:** pasted as `[Image: image/png]` or `[Image: source: /path]` with no surrounding text — the image IS the message
- **Terminal output:** pasted verbatim, multiline, no markdown fencing in organic messages
- **"Implement the following plan:"** — signals a pre-authored structured plan is incoming, always in English, usually Markdown with tables and code blocks

## Calibration Quotes

**Opening / task description:**
1. `"rodei para ver como esta o software com esse historico e olhe so..."` (8 words + screenshot)
2. `"voce ira me ajudar a desenvolver esse projeto!! olha esse ponto de atençao, o markdown aparentemente nao é renderizado da melhor forma do terminal como o print"`
3. `"é verdade que meu agente nao tem acesso ao termial?"` (9 words)
4. `"entire status"` (2 words)

**Steering / mid-session:**
5. `"esta perfeito!! Agora quero aprimorar questoes do comando /switch tem que considerar que isso só é invocado se for na primeira caracter e alem disso só de colcar a barra / deve aparecer um preview dos comandos disponveis caso eu queira selecionar e ao lado uma breve explicação"`
6. `"outra coisa que percebi! quando eu estou no menu de sessoes aparece ao lado do id o nome da ultima engine... nao quero isso, nao é necessario"`
7. `"pensei numa ideia; e se ao inves do diretorio ser data... ser o .data ?"`
8. `"please continye"` (2 words, typo)
9. `"so commit without u as coauthor"`

**Pushback / correction:**
10. `"legal! mas quando eu seleciono e clico enter parecer que nao vai, que ele nao roda o comando"`
11. `"muito bom!! mas quando eu seleciono o gemini cli por exemplo aparece: [...]  nao da para selecionar apenas se sera o modelo flash ou pro?"`
12. `"entendi! mantenha entao apenas a logica do backspace mesmo["`  (trailing `[` — unintentional)
13. `"sim! pode aplicar todas as correções; rodar o coder reviewer agent e commitar sem voce como coauthor"`

**Failure report:**
14. `"testei e corrigiu a questao do home; end; del etc... mas agr o backspace parou de funcionar?"`
15. `"✗ PromptInput > renders input area when enabled [61.00ms]\n✗ ModelSelect > navigate up from first and select last model [132.00ms]\n✗ EngineSelect > arrow down moves selection to next item [95.00ms]\n\n 168 pass\n 3 fail"` (raw test output, no commentary)
