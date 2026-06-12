---
name: spec-dump-kickoff
description: For large or complex tasks, user pastes an entire pre-written spec, markdown table, or JSON blob directly into the chat with minimal framing. Trigger: user wants to create a substantial new feature or page.
---

# Spec dump kickoff

This user occasionally opens a session or a task phase by pasting a very large block of pre-written content — a structured spec, a data table, investment analysis, or JSON — directly into the chat. The framing is typically 0–15 words before the dump. After the dump they expect the agent to parse and execute without further clarification.

Characteristic patterns:
- Spec includes explicit section headers, tables, typed data structures
- May end with "进入代码实现阶段" or "开始执行吧" to signal "now implement it"
- User does not ask for a design review first
- If the agent offers options or asks clarifying questions, user picks by number: "选项1", "方案1"

## Examples

**Fund page spec dump** (opening, 400+ words):
> `Implement the following plan: # Plan: Create /fund Investment Portfolio Page ## Context User wants a dedicated page at /fund... ## Files to Create 1. src/data/fund.ts ...`

**Crypto oscillator analyst prompt** (opening, 600+ words):
> `增加一个新的页面，用来观察加密货币市场走势和行情趋势  ### **角色设定** 你是一位资深的加密货币市场分析师 ...`

**Fantastic 40 investment list** (mid-session, 40 rows of table data):
> `# 全球顶级企业 - 40家公司 # 一、Publics（30家上市公司） ## 🇺🇸 美股 & 全球科技核心 | 公司 | Ticker | 上市 | 一句话基本面 | ...`

After agent presented options for Telegram integration:
> `选项1`
