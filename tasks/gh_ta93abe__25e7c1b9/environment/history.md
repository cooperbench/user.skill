> DEVELOPER

workflow のスライドのコード例はそれぞれ何をやるもの？

> TOOL

tool_use Bash
id: toolu_01PLmzcm6pyMnvcA3NdSS6fe
```json
{
  "command": "find /Users/ta93abe/Developer/github.com/ta93abe/slides/contents -type f -name \"*.md\" | xargs grep -l -i \"workflow\" 2>/dev/null | head -20",
  "description": "Find slides containing workflow references"
}
```

> TOOL

tool_result
id: toolu_01PLmzcm6pyMnvcA3NdSS6fe
```
/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/slides.md
/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/note.md
/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md
/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workers.md
/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/observability.md
```

> TOOL

tool_use Read
id: toolu_01HnJrUvTzPWvN55TSh3AGH4
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md"
}
```

> TOOL

tool_result
id: toolu_01HnJrUvTzPWvN55TSh3AGH4
```
1	---
2	layout: two-cols-header
3	---
4	
5	# [Cloudflare Workflows](https://developers.cloudflare.com/workflows/)
6	
7	Cloudflare Workflows は耐久性のある実行エンジンです。ステップを連鎖させ、失敗時には自動で再試行し、長期間実行されるプロセス全体で状態を保持します。各 step には Workers Bindings を組み込めます。
8	
9	::left::
10	
11	<div class="agent-example">
12	
13	```typescript {all|3-6|8-15|17-20|22-24|all}
14	export class ImageProcessingWorkflow extends WorkflowEntrypoint {
15	  async run(event: WorkflowEvent, step: WorkflowStep) {
16	    const imageData = await step.do('fetch image', async () => {
17	      const object = await this.env.BUCKET.get(event.params.imageKey);
18	      return await object.arrayBuffer();
19	    });
20	
21	    const description = await step.do('generate description', async () => {
22	      const imageArray = Array.from(new Uint8Array(imageData));
23	      return await this.env.AI.run('@cf/llava-hf/llava-1.5-7b-hf', {
24	        image: imageArray,
25	        prompt: 'Describe this image in one sentence',
26	        max_tokens: 50,
27	      });
28	    });
29	
30	    await step.waitForEvent('await approval', {
31	      event: 'approved',
32	      timeout: '24 hours',
33	    });
34	
35	    await step.do('publish', async () => {
36	      await this.env.BUCKET.put(`public/${event.params.imageKey}`, imageData);
37	    });
38	  }
39	}
40	```
41	
42	</div>
43	
44	::right::
45	
46	<ol class="ml-4">
47	  <li><span :class="['transition-opacity duration-300', $clicks === 0 || $clicks === 1 || $clicks > 4 ? '' : 'opacity-30']">R2 から画像を取得</span></li>
48	  <li><span :class="['transition-opacity duration-300', $clicks === 0 || $clicks === 2 || $clicks > 4 ? '' : 'opacity-30']">LLaVA で […]

> AGENT

workflows ページ (`contents/cloudflare-data-platform/pages/workflows.md`) に2つのコード例があります。

## 1. TypeScript: `ImageProcessingWorkflow` (pages/workflows.md:14-39)

**画像処理パイプライン** を題材に Workflows の核となる 3 機能を見せる例:

| ステップ | 役割 | 見せたい機能 |
|---|---|---|
| `step.do('fetch image')` | R2 から画像を `arrayBuffer()` で取得 | **Workers Bindings 統合** (`this.env.BUCKET`) |
| `step.do('generate description')` | Workers AI の LLaVA で「1 文の説明」を生成 | **Workers AI も同じ step で使える** |
| `step.waitForEvent('await approval', { timeout: '24 hours' })` | 外部からの `approved` イベントを最大 24 時間待つ | **durable な人間承認待ち** (これが目玉) |
| `step.do('publish')` | `public/` プレフィックスで R2 に書き戻す | 承認後の最終ステップ |

★ Insight ─────────────────────────────────────
- `step.waitForEvent` の 24h タイムアウトはプロセスが寝てる間も課金されず再開できる — これが「耐久性のある実行エンジン」の象徴で、Lambda + Step Functions 相当の世界を Worker 単体で表現できる
- 各 step が冪等な単位として retry されるので、外部 API の重複呼び出しを避けるなら step 境界の切り方が設計上のキモになる
─────────────────────────────────────────────────

## 2. Python: `IngestWorkflow` (pages/workflows.md:126-144)

**diamond shape DAG (並列 fan-out → join)** を題材に、TypeScript 版と違う Python SDK 独自の DSL を見せる例:

```
        fetch_a ─┐
                 ├─► merge
        fetch_b ─┘
```

- `@step.do()` デコレータで `fetch_a` / `fetch_b` を独立ステップとして宣言
- `merge(fetch_a, fetch_b)` の **引数名がそのまま依存宣言** になる — `fetch_a` という引数があれば `fetch_a` step の完了を待つ
- `concurrent=True` で `fetch_a` / `fetch_b` が並列起動 → 両方終わったら `merge` が実行される

★ Insight ─────────────────────────────────────
- TypeScript 版は「順序 = `await` の並び」だが、Python 版は「依存 = 引数名」という宣言的 DAG。Airflow / Prefect の世代を経た現代的な書き方で、ML / data pipeline 文脈と相性がいい
- 同じ Workflows ランタイムなのに SDK によって DSL が違うのは Cloudflare の典型的なアプローチ (Durable Objects の […]