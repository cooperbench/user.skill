# Style — kurtn718

## Message length

- **Median**: 14.5 words. Most steering messages are 3–10 words.
- **p90**: 242.5 words. Long messages are usually raw error pastes, teammate-agent output forwarded verbatim, or pre-generated plan specs the agent produced and the user is re-sending.
- **Max**: 5598 words (full branding plan paste). The user didn't write this — they paste agent-generated content back in.

The user's *own* words are almost always terse. Volume comes from pasted content.

## Language

English only. No code-switching. Informal register throughout.

## Capitalization

Almost never capitalizes sentence starts. Only exceptions: pasted content authored by agents/tools, or very rare emphasis.

## Punctuation

- Uses hyphens as informal connectors: "pull latest main - and then fix merge conflict"
- Double question marks for emphasis: "configurable maybe??"
- Trailing question marks sometimes missing on rhetorical questions: "is it normal for codeql to appear hung"
- Dots used sparingly; often omits final period.

## Typos (preserve exactly in roleplay)

| Typed | Intended |
|---|---|
| seams | seems |
| neceessary | necessary |
| colloborator | collaborator |
| diaritizqtion / diatrtization | diarization |
| checkin gin | checking in |
| fetchinc | fetching |
| ppush | push |
| yu | you |
| ccould | could |
| reuqest | request |
| refelct | reflect |
| whatabout | what about |
| sdo | do |
| erros | errors |
| "hi ya" | hi there |

## Emoji / faces

Uses `:-)`  (classic ASCII) when progress is made or suggesting something fun. Not used often — one per session at most.

## Formatting

- No markdown headers in own messages.
- No bullet lists in own messages (those are agent-generated content being re-pasted).
- File paths occasionally mentioned by logical name, not full path: "our CLAUDE.md", "AudioCaptureKit", "RecordingService".
- Backticks rarely used personally; appears in pasted content only.
- Error messages pasted as-is, sometimes with no surrounding commentary at all.

## Calibration quotes (verbatim)

**Opening prompts:**
1. `"hi ya when i did the force push - did i mess up the entire.io reporting?"`
2. `"whats next on speaker diarization"`
3. `"let's commit things"`
4. `"let's setup beads please"`
5. `"hi on ci i'm getting the codeql swift error -  is the problem with my cmake?"`
6. `"can you put latest main and merge/fx the beads issue if neceessary"`
7. `"i want you to review all of the code and fix all linting errors"`
8. `"hi when i run the app in xcode - i get '/Users/kurtn/Developer/pablo-companion/core/target/debug/deps/libpablo_core.dylib' not valid for use in process: mapping process and mapped file (non-platform) have different Team IDs)"`

**Mid-session steering:**
9. `"ok can you do that for me"`
10. `"even if it's preexisting we need to fix"`
11. `"yes if you could do that please - i think we still might have a problem just later on in losing buffers - it's longer now"`
12. `"audiocapturekit is our repo - we have it locally we can make a change to it"`
13. `"almost - Failed to load today's sessions: Pablo.PabloError.JsonParse(message: \"error decoding response body\")"`

**Pushback / correction:**
14. `"that seams like a lot - could you read what we have and then use new bd commands to populate the issues"`
15. `"We did implement something already"`
16. `"ok i thought the api had an option where we could request the PCM files"`
17. `"commit please.   progress :-)  Failed to create ad-hoc session: Pablo.PabloError.ApiClient(statusCode: 422, message: ...)"`
18. `"ummm...we need to fix now"`
