---
# kubokawa-dev — Persona
---

## Background (inferred)

Japanese developer, personal project focus. Works under the username `kbkkbk` locally (`/home/kbkkbk/Develop/kubocchi/`), suggesting a separate personal identity from their GitHub handle. (inferred) Likely a hobbyist or side-project developer rather than a full-time engineer—the project is a lottery prediction system they're emotionally invested in winning, not a commercial product. (inferred) Comfortable with Python and GitHub Actions at a working level, but delegates deep implementation entirely to the agent.

## Domain

- **Primary domain**: Japanese Numbers4 lottery prediction (picking 4-digit numbers in order or as sets/boxes)
- ML/data pipeline: Python scripts, LightGBM, custom prediction models (box_model, cold_revival, ml_neighborhood)
- Web frontend: Next.js 16 + TypeScript, pnpm, Turbopack
- Infrastructure: GitHub Actions (scheduled daily prediction runs), Supabase/PostgreSQL

## Role (inferred)

Solo founder/owner of a personal project. Plays the product manager and QA role: decides what to add, reports what's broken, approves or steers. The agent writes all the code.

## Seniority Signals (inferred)

- Knows enough to stage files manually and then hand off commit/push
- Understands CI pipeline outputs (can identify which job failed, which model is missing)
- References specific model names and file paths from memory
- Does NOT write code, debug code, or propose architectural solutions themselves
- Asks "わかりますか？いいたいこと" (do you understand what I mean?) — aware that their requests are vague

## Attitude Toward the Agent

- **Trusting by default** (68.5% non-pushback): accepts most output without objection
- **Enthusiastic collaborator**: celebrates wins with "めっちゃいいですね！！", "おお！すごい👍"
- **Soft redirector**: when unsatisfied, asks "もっともっと上げる方法ってありますか？？" rather than criticizing
- **Impatient with stalls**: "あれ？終わった感じ？" when the agent seems to have stopped without completing
- **Not micromanaging**: gives direction, then says "おねがいします！！" and trusts the agent to handle everything

## Emotional Texture

Genuinely excited about the lottery prediction project. Uses phrases like "もう必死なんですよ" (I'm desperate now), "もう本気なので！！" (I'm serious this time!!). The enthusiasm is real, not performative. Celebrates agent output warmly. Occasionally frustrated by blockers (git push failures, invisible UI changes) but doesn't escalate to anger—just restates the desire.
