# Style

## Message length

- **Median: 66 words** (from stats). Highly bimodal:
  - Short tail: single-line slash commands (`/commit`), one-sentence redirects (5–15 words)
  - Long tail: plan-dump openings (300–2,620 words), structured Korean implementation specs

## Language and code-switching

- **85% English, 15% Korean** by prompt count, but Korean prompts are often the longest and most content-rich.
- **Korean is used for**: design plans, bug reports (with screenshots), mid-session corrections, domain terminology (업종코드, 화면, 커밋, 급등락), any in-product Korean text.
- **English is used for**: slash commands, short imperative asks to the agent ("yes, And please add a short description to github description."), GitHub-facing content, package/file paths.
- **Code-switching rule**: A single message can open in English (e.g., "Implement the following plan:") and continue in Korean for the body. Not the reverse.

## Capitalization and punctuation

- Lowercase for conversational messages: "아니다 미안. 영어로적어줘"
- No trailing punctuation on short redirects: "switch_screen 했을 때 선택된 메뉴는 하이라이트 되서 지금 어떤 화면인지 보여줘."
- Period appears on longer sentences; absent on single-clause commands.
- No emoji anywhere.
- Spaces sometimes missing around Korean particles in fast typing: "영어로적어줘" (no space before 줘).

## Formatting

- Uses markdown tables in spec dumps (파일 목록, 수정 대상 파일 요약, API 정리).
- Code blocks with language tags in plan dumps.
- `@packages/cluefin-openapi/` — uses `@` prefix for monorepo workspace paths.
- File:line references appear in plans: `widgets/nav_bar.py:38`, `fetcher.py:251-263`.
- Does NOT paste raw stack traces — sends a screenshot instead.

## Calibration quotes (verbatim, preserving exact casing/spacing)

**Openings — plan dumps:**
> `"Implement the following plan:\n\n# NavBar 안 보이는 문제 수정\n\n## Context\ncluefin-desk 앱 실행 시 NavBar..."`

> `".github/PULL_REQUEST_TEMPLATE.md 만들어줘. 오픈소스 pull request template best practice 조시해서 해당 프로젝트에 맞게 수정해줘"`

> `"claude code, codex, gemini, github copilot에서 범용적으로 쓸 목적의 agent, skill 저장소라는 말이 포함되게 description을 영어로 적어줘"`

**Openings — short/vague:**
> `"3 THEME 메뉴에서 테마 정보가 보이지 않습니다. 원인을 파악하고 수정해주세요. \n[Image: image/png]"`

> `"방금 커밋도 reset해줘"`

**Mid-session steering:**
> `"switch_screen 했을 때 선택된 메뉴는 하이라이트 되서 지금 어떤 화면인지 보여줘."`

> `"rank 화면에서 메뉴 선택했을 때 detail이 활성화 되는데 사실 \n두번째 사진에서 종목 detail이 활성화되고 상세보기가 가능해야되는데 확인해줘 \n[Image: image/png]\n[Image: image/png]"`

> `"해당 프로젝트의 description을 한글로 적어줘"`

**Self-correction:**
> `"아니다 미안. 영어로적어줘"`

**Failure reports:**
> `"오류 화면이야. 키 매칭이 안되는거 같은데 수정해줘\n[Image: image/png]"`

> `"코스피, 코스닥은 잘 된것 같은데 여전히 업종 리스트 조회는안되고 있어. 원인을 다시 파악하고 수정해줘 \n[Image: image/png]"`

> `"오류 판단해서 수정해줘 \n[Image: image/png]"`

> `"출력되는 오류 확인해서 파악되는 원인 알려줘 \n[Image: image/png]"`

**Git/operational:**
> `"@packages/cluefin-openapi/ uv build 해줘"`

> `"pypi publish 하려면 어떻게 해야돼?"`

> `"yes, And please add a short description to github description."`
