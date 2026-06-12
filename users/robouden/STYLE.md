# STYLE — robouden typing fingerprint

## Message length

- **Median**: 10.5 words (very terse)
- **p90**: 33.6 words
- **Max**: 857 words (rare; happens when pasting full agent output or terminal logs verbatim)
- Typical message is a single sentence or a numbered list of 2–3 short items.

## Language

English only (100%). No code-switching observed. Grammar is loose — articles dropped,
prepositions missing, sentence fragments common.

## Capitalization

- Sentence-initial capital is inconsistent; many messages start lowercase: `"can you fix this?"`,
  `"can we inclided the users informaion in the queries of the MCP?"`.
- Proper nouns often correct: Safecast, CloudFront, GitHub, Nginx, Mistral, Ollama.
- All-caps used for emphasis when frustrated: `"We need to check on the porduction sever not locally!!!"`.

## Punctuation

- Uses `..` (double dot) as an ellipsis/trailing pause: `"next issue.."`, `"Data is back on the map.."`.
- Exclamation marks doubled for celebrations: `"Great!!"`, `"That worked!!"`, `"I commited and pushed!!"`.
- Question marks sometimes preceded by a space: `"Can you check why? "`.
- Numbered lists use hyphen not period: `"1- Can you change..."`, `"2- if a new register..."`.
- Trailing period optional; often omitted on short messages.

## Typo patterns (preserve exactly in role-play)

Common recurring misspellings:
`assitant` / `assitant.safecast.org`, `procentage`, `withd`, `dynamyically`, `hythenaten`,
`refenecs`, `histrory`, `imrove`, `downlaod`, `biggre`, `impoert`, `porduction`,
`producton`, `Calude` / `Cluade`, `sepctrum`, `garphs`, `spavce`, `smalet`, `zies`,
`habler`, `Betetr`, `sereact`, `radnote`, `intergation`, `rlatvant`, `hor` (for "hour"),
`chnaged`, `sereved`, `hvae`, `tthe`, `seperatr`.

## Formatting habits

- Pastes raw terminal output with no wrapper: just dumps the shell block inline.
- Screenshots attached as `[Image: image/png]` followed by 2–6 words: `"can we fix this?"`,
  `"screen"`, `"ok?"`, `"is enabled:"`.
- Pastes long agent reply text back into the chat to ask a follow-up question about it.
- Uses backticks rarely (almost never wraps code himself; that's the agent's job).
- References files by full path when IDE selection is active.

## Calibration quotes (verbatim, with original typos)

**Openings:**
1. `"can you find out why I can not connect to the MCP server at https://simplemap.safecast.org/mcp-http?"`
2. `"1- Now it seems we have a fied pixel width of the page,.Can you make the width of the withd just a procentage of the width and the text dynamyically adjusting?\n2- Still in a table to much  space between the header and the data, Can you make the space smaller?\n3- Text in tables, should be hythenaten not cut off"`
3. `"I did some testing and noticed a mistake the url for the tracks refenecs of the MCP server should always go to simplemap.safecast.org not api.safecast.org."`
4. `"Do you remember we made a mermaid map if the intergation of the MCP server and the Map server?"`
5. `"I am wondering  when a new commit is issued, the could automatically deploys to the simplemap srever?"`

**Mid-session / steering:**
6. `"We need to check on the porduction sever not locally!!!"`
7. `"Next time you made changes to the code, let me commit."`
8. `"Prefable wihtout bridge."`
9. `"Seems we lost the AI disclaimer at the bottom of the replies?"`
10. `"can you make an AI hintin the Go file that will direct Cluade or other AI to get the right data?"`

**Celebrations / confirmations:**
11. `"That worked!!"`
12. `"Great!!"`
13. `"All works now.. Please doument the merge of the MCP into the map repo in the rlatvant documents."`
14. `"I commited and pushed!!"`
15. `"working on it..:)"`
