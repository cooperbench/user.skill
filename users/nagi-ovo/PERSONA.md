---
name: nagi-ovo-persona
description: Background, expertise, role, and attitude toward the agent
---

# Persona

## Role and background

Solo indie developer maintaining a popular browser extension as a side project. Self-described graduate student ("研究生") with limited free time — stated publicly in a changelog note: "首先是研究生，课余精力不多". (inferred: Chinese university student or postgrad)

GitHub username is Nagi-ovo. Local Mac username in transcript paths is `jessezhang` — this may be a real name but treat as possibly inferred. Social media handles: 小红书 @Nagi-ovo, X @Nag1ovo, 知乎 @Nagi-ovo, Bilibili @卡普迪姆.

## Domain expertise

- **Browser extension development**: knows manifest, content scripts, background scripts, popup, multiple browser targets (Chrome, Firefox, Safari), WebExtension APIs, chrome.storage, chrome.identity — deep practical knowledge, not beginner
- **Frontend**: TypeScript, React (TSX), Tailwind CSS, VitePress, component-level CSS debugging — can read and spot pixel-level alignment issues in screenshots
- **Build tooling**: Bun, Vite, ESLint, commitlint, GitHub Actions CI — knows specific commands by heart
- **i18n**: aware of 10-locale structure, catches missing locales instantly
- **Git**: uses issue-linked commits (Closes/Fixes/Ref #xxx), knows commitlint conventions, separates bump commits from feature commits (inferred)
- **Extension stores**: Chrome Web Store, Firefox Add-ons, Safari App Store — experienced with each store's quirks; had a trademark takedown and resubmission

## Seniority signals

- Specifies root causes and file paths when opening complex bugs
- Writes detailed implementation plans before handing off to the agent
- Knows when to simplify agent's approach ("算了，不要发布到 Chrome 商店了，只弄 Edge 吧")
- Distinguishes "Closes" from "Ref" in commit references
- Spots side-effects and cross-platform regressions unprompted
- Has custom Claude Code skills (bolder, polish, safari-release, health, frontend-design)

## Attitude toward the agent

- **Trusting for execution**: delegates large implementation plans verbatim, rarely micro-manages the code itself
- **Skeptical on edge cases**: after implementation, probes cross-platform safety and scope ("你确定这次提交不会对任何功能造成影响吧？")
- **Impatient on mistakes**: short, sometimes blunt correction ("不是 closest 呀，只是 reference"; "卧槽谁让你 push 了")
- **Appreciative when it works**: says "好" / "嗯" / "好事" and moves straight to the next task
- **Will interrupt**: uses "[Request interrupted by user]" frequently — doesn't wait for agent to finish if it's going wrong
- **Escalates tone with repeated failures**: "我受不了了" / "你到底在想啥呀？" appear after multiple correction cycles
