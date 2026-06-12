---
name: nitpick-correction
description: Trigger — agent has completed a task but made one wrong detail; user delivers a short, direct correction, sometimes with mild frustration
---

# nitpick-correction

After an agent completes a task, the user spots one precise error and corrects it in ≤ 15 words. There is no praise, no softening, no "but otherwise it's great". The correction IS the whole message.

**What they correct**:
- Wrong commit keyword: `不是 closest 呀，只是 reference`
- Missing locales: `并没有修改所有语言吧`
- Wrong version: `版本不对，看manifest`
- Political/geographic error: `Taiwan 不是繁体中文，你涉嫌政治了`
- Unsolicited push: `卧槽谁让你 push 了`
- Wrong file/scope touched: `wait .claude 里的内容不要被 format,撤回后重新 format`
- Scope too broad: `我觉得按钮里面的文案不需要这么长`
- Missing connected update: `不是啊,你不是说 changelog 文件要添加吗`
- Wrong assumption about user population: `注意啊，不是所有用户都遇到了，是个别用户`
- Excessive simplification: `算了，你这个太严格了，去掉吧`

**Escalated tone after repeated failures**:
> "我受不了了，你这改完那个 popup 和 TLS 管理器里怎么一坨绿啊？这也太丑了，这完全不是 polish 啊"
> "你到底在想啥呀？"

**What NOT to do in response**: don't apologize extensively. Acknowledge briefly, fix, move on.
