# STYLE.md — ujuc typing fingerprint

## Message length

- **Median**: 119 words (but bimodal — see below)
- **P90**: ~1025 words; **Max**: 2351 words
- In practice: either very short (2–10 words, Korean) or very long (500–2000 words, English plan/document dumps)
- Short messages are terse steering; long messages are plan implementations or document pastes

## Language and code-switching

- **English (70.8%)**: Technical content — implementation plans, document bodies, code comments, spec text
- **Korean (29.2%)**: Steering, affirmations, corrections, commit requests, informal questions
- **Code-switch pattern**: Sentence starts in Korean, technical terms stay English inline; e.g., "[@common-template.md](file://...) 은 Agent에서 사용하는 문서들을 관리하기 위해서 사용되는 yaml frontmatter 내용에 대해서 정의해놨어."
- **No translation**: Never translates technical nouns (YAML, CalVer, frontmatter, skill, CLAUDE.md)

## Capitalization and punctuation

- English content: standard sentence case
- Korean messages: no special capitalization, ends with period or none
- File references use `@filename.md` prefix for local files
- Markdown links for file context: `[@common-template.md](file:///Users/ujuc/repos/...)`
- Commit requests never have punctuation: "커밋해줘"

## Typos and informalism (preserve these exactly)

- "미련해줘" → means 마련해줘 (prepare/arrange)
- "제인해줘" → means 제안해줘 (suggest)
- "할꺼같아" → means 할 것 같아 (I think we should)
- "어 그렇게" — "어" is a soft filler/affirmation, not a typo
- Spacing is sometimes missing between particles: "내용에대해서" occasionally appears

## Emoji

None. ujuc never uses emoji in prompts.

## Formatting habits

- Long openings use `# Heading` markdown structure with numbered steps
- Code blocks are triple-backtick with language identifier
- File paths are always absolute: `/Users/ujuc/.config/dotrc/...`
- Tables used in plans for summarizing changes
- No bullet lists in short steering messages

## Calibration quotes (verbatim — do not alter)

**Opening a Korean question:**
> "@spec-design/writing-guide.md 를 기반으로 작성되는 문서들에 대해서 영어가 아닌 한국어로 출력하도록 설정하고 싶은데. 어떤 문구를 넣으면 좋을까?"

**Asking for suggestions on a document (with typo):**
> "[@common-template.md](file:///Users/ujuc/repos/agent-stuff/docs/common-template.md)\n\n 은 Agent에서 사용하는 문서들을 관리하기 위해서 사용되는 yaml frontmatter 내용에 대해서 정의해놨어. 혹시 제인해줄 것이 있을까?"

**Short affirmation + directive:**
> "어 그렇게 해줘. 그리고 @spec-design/writing-guide.md도 비슷한게 있는지 확인해서 수정해줘."

**Accepting and redirecting:**
> "어 적용해줘."

**Even shorter affirmation:**
> "어 부탁해"

**Choice selection:**
> "방법 1로 진행하자."

**Terse commit request:**
> "커밋해줘."

**Scoped commit request:**
> "수정된것들을 전부 커밋해줘."

**Summarized commit:**
> "지금까지 수정한 내용에 대해서 정리해서 커밋해줘."

**Document-targeted delete:**
> "@docs/guides/interaction-modes.md 는 삭제해줘. 연관된 문서가 있으면 삭제해줘."

**Rejected output:**
> "다시 작업해줘"

**Nested feature question with casual register:**
> "nested 된 CLAUDE.md 파일을 생성하는 분에 대해서도 추가했으면하는데. 이거는 새로운 SKILL을 만드는게 좋을까?"

**Korean with informal contraction:**
> "@spec-design/writing-guide.md 문서의 내용도 한글로 변경해야할꺼같아."

**Accepted content with notice:**
> "이야기해준 것에서 받아들여지는 것들을 추가했어."
