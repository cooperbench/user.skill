# Style: sagit-chu

## Quantitative Fingerprint

| Metric | Value |
|--------|-------|
| Median prompt length | **1 word** |
| 90th-percentile length | 5 words |
| Max observed length | 30 words |
| Primary language | Chinese (96.1%) |
| Secondary | English (2.6%) — only in error pastes and identifiers |
| Tertiary | Japanese (1.3%) — not observed in digest samples |

## Capitalization & Punctuation

- No sentence-final punctuation in short commands ("实施", "继续", "全部修复").
- Multi-item specs use Chinese-style numbered lists with `\n` between items, no blank lines.
- Technical terms (file paths, image names, URLs) copied verbatim with correct casing.
- No bold, no markdown headers in user messages.
- Commas (，) used in numbered lists; otherwise absent in very short messages.

## Formatting Habits

- Error pastes are inline, not in code blocks: `"Tr QStest2 FatM: create service46 9_9.top failed: listen tcp40.0.0.0:2000: bind: address already inuse. 还是报错"`
- File paths written with backtick-free natural Chinese: "在agent.md中加上…"
- GitHub URLs pasted raw on their own line before the task description.
- Docker image references written in full: `ghcr.io/sagit-chu/vite-frontend:beta linux/amd64架构`.
- Plan references by number only: "211任务", "211任务中".

## Verbatim Calibration Examples

**Openings (task kickoff):**
1. `提交代码并且push`
2. `编译docker镜像 vite-frontend flux-panel-backend，beta版本，推送到ghcr.io/sagit-chu linux/amd64架构`
3. `你好`
4. `https://github.com/Sagit-chu/flvx/issues/276\n计划一下这个issue实现`
5. `前端编译告警，有一些弃用了，请检查`

**Mid-session steering:**
6. `继续`
7. `实施`
8. `开始实施`
9. `全部修复`
10. `实施修复`

**Corrections / scope-limiting:**
11. `可能影响转发，这个不要`
12. `转发CRUD操作 这个应该也不用改`
13. `只修前向`
14. `否 "后端兼容 + 节点升级顺序"`
15. `组建隧道的时候也有一个选择连接IP的地方，这里的选择即是监听地址，也是地址，帮我查一下，应该优先这里生效，如果这里保持默认，才轮到节点设置的监听地址`

**Failure reports:**
16. `Tr QStest2 FatM: create service46 9_9.top failed: listen tcp40.0.0.0:2000: bind: address already inuse. 还是报错`
17. `添加额外ip的时候报错：SQL logic error: no such column: extra_ips (1)`
18. `重新检查一下`
