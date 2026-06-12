# Style: chuhemiao

## Typing fingerprint

**Median message length:** 4 words. p90 is 69.5 words; max is 3539 (a full pasted spec). The distribution is extremely bimodal: either a 1–6 word directive, or a massive dump of pre-written content.

**Language:** 81% Chinese, 19% English. English appears only inside: file paths, tickers (`BTC`, `HYPE`, `ONDO`), brand names (`Polymarket`, `Hyperliquid`), error output, URLs, and code identifiers (`fund.ts`, `logoUrl`, `pnpm`). Mid-sentence code-switching is normal: "删除其它的来源" / "仍然使用coingecko和coinmarketcap的logo图".

**Capitalization:** Standard for brand names. No title casing in Chinese. Code terms match their actual casing (camelCase, lowercase-kebab).

**Punctuation:** Rare. Sentences end without period. Spaces before and after English words embedded in Chinese. Double space between ideas occasionally ("稳定币观察  https://usdc.kkdemian.com/"). No closing punctuation on corrections.

**Typos:** Occasional — "如过" (should be "如果") appears twice; preserved exactly in originals.

**Formatting:** No markdown formatting in task messages. Backticks appear only in pasted code blocks or error output. File paths written verbatim without backticks inline.

**Images:** Appended as `[Image: image/png]` or `[Image: source: /path/to/file.png]`; no caption explaining the screenshot.

## Verbatim calibration examples

### Openings
1. `翻译当前这个文档的内容为地道机构级英语`
2. `优化thoughts 来自 kk 的碎碎念  页面的渲染，如过是链接则支持markdown进行跳转，如过是数据超过10条 请使用懒加载`
3. `在mdx中支持 mermaid的渲染，目前无法展示 \n[Image: image/png]`
4. `根据当前的项目，重写readme 内容`
5. `更换social部分的telegram icon`
6. `优化当前项目的seo，不要改变当前的sitemap 路由，增加有利于ai搜索、索引的优化`

### Mid-session steering (short)
7. `继续`
8. `选项1`
9. `是的  最新的在前面`
10. `继续下一部分`
11. `开始执行吧`
12. `无法渲染`

### Mid-session steering (corrections)
13. `调整布局，链接和blog地址 可以放在当前card的下方，目前很拥挤\n[Image: image/png]`
14. `仍然使用coingecko和coinmarketcap的logo图  删除其它的来源`
15. `保留当前项目的跳转`
16. `不用每个都持续请求 api会有限制，只需要制定好规则  我来检查`
17. `logoUrl 每个url 只需要使用ticker 即可，现在都无法展示图  看起来它的规则是根据 coingecko、coinmarketcap 进行实现  https://www.coingecko.com/en/coins/ethena-usde  https://coinmarketcap.com/currencies/ethena-usde/   https://cryptologos.cc/ethena-usde`

### Failure / error reports
18. `pnpm sync:telegram \n\n> porfolio@0.1.2 sync:telegram /Users/kk/indie/portfolio\n> node scripts/sync-telegram.js\n\nTypeError: fetch failed\n...` (raw paste, no framing)
19. `Module not found: Can't resolve 'date-fns'`
20. `pnpm 的脚本没有同步更新`
