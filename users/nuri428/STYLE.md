# Style — nuri428

## Quantitative fingerprint

- Median prompt: **7 words**
- p90 prompt: 1,946 words (plugin skill dumps — not the user's own words)
- Natural user messages: 3–15 words; most under 10
- Languages: 59% English, 41% Korean (Korean rising in corrections and session management)
- Session median: 9.5 turns over ~33 minutes

## Language and code-switching rules

- Opens sessions in **either** language, often whichever fits the command
- Uses **Korean** for: corrections, session wrap-up, questions, explanations to the agent
- Uses **English** for: single-word commands, slash command args, git/Docker terms
- Mixes mid-sentence: "pdca design 프론트는 ibm black, data 기반 서비스 ui로 작성해줘"
- Has explicitly requested Korean responses from the agent

## Capitalization and punctuation

- All lowercase in English words: "entire status", "web socket issue 처해줘"
- Korean follows standard sentence-level capitalization
- Minimal punctuation: rarely uses periods, uses "?" for questions, "~" for casual warmth
- No comma-heavy sentences; thoughts are atomic, one per message

## Typos (preserve exactly)

- "ftrontend" (frontend)
- "znd" (and) — "load todo znd tasks and claude md files"
- "compsoe" (compose) — "운영 docker compsoe에서"
- "처해줘" used where "처리해줘" was likely intended — "web socket issue 처해줘"
- Slash command typos: "Unknown skill: pda" (pdca), "Unknown skill: paca" (pdca)

## Formatting

- Never uses markdown in own messages (headers, bullets, tables are agent output)
- Pastes errors verbatim inline: `Blocked request. This host ("greennuri.info") is not allowed.` + question
- Plugin commands trigger long skill-dump messages (system-injected, not user-written)
- Korean questions end with "?" directly, no leading explanation
- File paths cited by concept, not by path: "claude.md를 읽어서", "기능정의서 문서가 있을거야"

## Verbatim calibration quotes

### Openings
1. `"entire status"`
2. `"load todo znd tasks and claude md files"`
3. `"claude.md를 읽어서 이전 세션에서 중단한 내용을 로딩해줘"`
4. `"ohmyclaudecode를 설치할수 있을까?"`
5. `"status-line.sh를 통해서 사용량 추적이 되서 표시 되야 하는걸로 아는데 지금은 표시가 안되고 있네 ?"`

### Steering mid-session
6. `"앞으로 답은 최대한 한글로 해줘"`
7. `"순서대로 작업을 진행해줘"`
8. `"계속해"`
9. `"남은 토큰양이 얼마 안되네 프로젝트 전체 스펙에 관련된 내용을 기록해서 차후 작업도 바로 연동 가능하게 기록하고 마무리 하자"`
10. `"잔여 작업은 E2E로 접속 테스트인가 아직 docker compose가 정상으로 뜨는지 확인 안됐는데 ?"`

### Pushback
11. `"현재 프로젝트에서 mysql, opensearch, neo4j는 이미 존재하는 외부 서비스에 접속해서 진행하는거야 직접적으로 도커를 만들하지 말아"`
12. `"나 프로 플랜 쓰고 있고, https://... 여기에서 remote control 사용할수 있다고 하는데 넌 /rc, /remote-control 스킬을 인식 못하네?"`

### Wrap-up
13. `"오케이 수고 많았어요~"`
14. `"오케이 세션 종료 차후 로그인시 작업할 내용을 언급 바람"`
15. `"잔여작업을 기록해줘"`
