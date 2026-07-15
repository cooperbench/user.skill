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

> DEVELOPER

2つとも実際にデプロイしたい。

> AGENT

実デプロイとなるとスライドのコードだけでは足りない要素 (Bindings 作成・依存関数の中身・トリガー方法) があるので、スコープを合わせさせてください。

★ Insight ─────────────────────────────────────
- スライドのコードは **教育用に切り出された抜粋** で、`this.env.BUCKET` (R2 binding) や `get_a()` / `get_b()` (Python 側) など外部依存が前提になっている — そのままでは `wrangler deploy` に通らない
- このリポジトリは Slidev 用に `wrangler.jsonc` が Static Assets 配信向けに構成されているので、Workflows は **別プロジェクト** として作るのが素直
─────────────────────────────────────────────────

> TOOL

tool_use AskUserQuestion
id: toolu_01MhvxG59aB9Gn51EGq41x9R
```json
{
  "questions": [
    {
      "question": "Workflows プロジェクトをどこに置きますか?",
      "header": "配置場所",
      "multiSelect": false,
      "options": [
        {
          "label": "別の新規リポジトリ (Recommended)",
          "description": "~/Developer/github.com/ta93abe/ 配下に新規 git リポジトリを作成。スライドリポと独立して wrangler / Workflows の設定を持てる。デプロイ後 URL をスライドの登壇デモ用にも使える"
        },
        {
          "label": "slides リポ内に examples/ ディレクトリ",
          "description": "このリポの examples/workflows-ts と examples/workflows-py を作る。スライドとコードが一箇所にまとまる利点があるが、ルートの wrangler.jsonc とは別管理になる"
        },
        {
          "label": "~/Developer 配下の作業ディレクトリ",
          "description": "git 管理しない作業用ディレクトリで動作確認のみ。手っ取り早いがコードが散逸する"
        }
      ]
    },
    {
      "question": "ゴールはどこまでですか?",
      "header": "デプロイ範囲",
      "multiSelect": false,
      "options": [
        {
          "label": "登壇で見せられる動くデモ (Recommended)",
          "description": "TS 側: R2 にサンプル画像を置き、LLaVA で説明生成、承認 API 叩いて publish まで通る。Py 側: fetch_a/fetch_b を実装して diamond DAG が Visualizer に出るとこまで"
        },
        {
          "label": "wrangler deploy が成功するだけ",
          "description": "Bindings 設定・依存関数の最小実装を入れて deploy が通れば OK。実行は確認しない"
        },
        {
          "label": "TS だけ動くデモ、Py は deploy が通るだけ",
          "description": "Python Workers は Beta + ローカル制約があるため (pywrangler 必要・wrangler dev 非対応)、TS を本命にして Py は最小構成"
        }
      ]
    },
    {
      "question": "Cloudflare アカウントと wrangler の準備は?",
      "header": "事前準備",
      "multiSelect": false,
      "options": [
        {
          "label": "wrangler ログイン済み・アカウント運用中",
          "description": "wrangler whoami が通る状態。R2 / Workers AI も使ったことがある"
        },
        {
          "label": "アカウントはあるが wrangler ログインから",
          "description": "Cloudflare アカウントはあるが wrangler login / R2 有効化はこれから"
        },
        {
          "label": "アカウント作成から",
          "description": "Cloudflare アカウントもこれから作る"
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01MhvxG59aB9Gn51EGq41x9R
```
User has answered your questions: "Workflows プロジェクトをどこに置きますか?"="別の新規リポジトリ (Recommended)", "ゴールはどこまでですか?"="wrangler deploy が成功するだけ", "Cloudflare アカウントと wrangler の準備は?"="wrangler ログイン済み・アカウント運用中". You can now continue with the user's answers in mind.
```

> AGENT

了解。最後にプロジェクト構造だけ確認させてください。

★ Insight ─────────────────────────────────────
- **1 Worker = 1 言語** という制約があるので TypeScript と Python は物理的に別 Worker = 別ディレクトリ (= 別 `wrangler.jsonc`) になる
- スライドの例で `await step.waitForEvent(...)` を使っているので、Worker からそのクラスを **`Workflow` binding として自己参照** する設定 (`wrangler.jsonc` の `workflows[]`) が `deploy` 通過の最小要件 — R2 / AI binding は実行時に必要だが `deploy` だけなら省略可
─────────────────────────────────────────────────

> TOOL

tool_use AskUserQuestion
id: toolu_0121agvEjwSK1RpajgcKiRQg
```json
{
  "questions": [
    {
      "question": "新規リポジトリ名をどうしますか?",
      "header": "repo 名",
      "multiSelect": false,
      "options": [
        {
          "label": "cf-workflows-examples (Recommended)",
          "description": "Cloudflare Workflows のサンプル集というニュートラルな名前。今後他の例も追加しやすい"
        },
        {
          "label": "cfdp-workflows-demo",
          "description": "Cloudflare Data Platform 登壇デモとしての位置づけを明示。スライドに URL を貼るならこちらが話の脈絡が伝わりやすい"
        },
        {
          "label": "workflows-tutorial",
          "description": "自学用チュートリアルとしての位置づけ"
        }
      ]
    },
    {
      "question": "TS と Python を 1 リポ内でどう分けますか?",
      "header": "レイアウト",
      "multiSelect": false,
      "options": [
        {
          "label": "ルート直下に ts/ と py/ (Recommended)",
          "description": "/ts と /py にそれぞれ wrangler.jsonc を持つシンプル構造。リポの README で両方を紹介"
        },
        {
          "label": "pnpm workspace + apps/ts apps/py",
          "description": "スライドリポと同じ pnpm workspace 構造。今後例を追加しやすいが Python は workspace の恩恵を受けにくい"
        },
        {
          "label": "Turborepo 型に examples/<name>",
          "description": "examples/image-processing-ts, examples/ingest-py のように例名で圧る。拡張性高"
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_0121agvEjwSK1RpajgcKiRQg
```
User has answered your questions: "新規リポジトリ名をどうしますか?"="cf-workflows-examples (Recommended)", "TS と Python を 1 リポ内でどう分けますか?"="ルート直下に ts/ と py/ (Recommended)". You can now continue with the user's answers in mind.
```

> AGENT

方針確定。`~/Developer/github.com/ta93abe/cf-workflows-examples/` に `ts/` と `py/` を並べる構成で進めます。まずは環境確認とリポジトリ準備から。

> TOOL

tool_use Bash
id: toolu_01RLwq8icMuNPUQsmpokKgAU
```json
{
  "command": "ls -la /Users/ta93abe/Developer/github.com/ta93abe/ 2>/dev/null | head -20",
  "description": "親ディレクトリの中身を確認"
}
```

> TOOL

tool_use Bash
id: toolu_012LCoNR7ZocxEW4S38t71m2
```json
{
  "command": "npx wrangler --version 2>&1 | tail -5; echo \"---\"; npx wrangler whoami 2>&1 | tail -10",
  "description": "wrangler バージョンとログイン状態確認"
}
```

> TOOL

tool_use ToolSearch
id: toolu_01MoCejQDqDgZmQNTPxeLd34
```json
{
  "query": "select:mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01RLwq8icMuNPUQsmpokKgAU
```
total 24
drwxr-xr-x@ 31 ta93abe  staff    992 May 12 21:30 .
drwxr-xr-x@ 10 ta93abe  staff    320 May  7 11:46 ..
drwxr-xr-x@  3 ta93abe  staff     96 Feb 18 23:20 .claude
-rw-r--r--@  1 ta93abe  staff  10244 Jan 27 20:01 .DS_Store
drwxr-xr-x@ 14 ta93abe  staff    448 May  7 20:46 arroyo-on-snowpark-container-sevices
drwxr-xr-x@ 24 ta93abe  staff    768 Jul 20  2025 bg-static-site
drwxr-xr-x@ 10 ta93abe  staff    320 May 12 00:25 cloudflare-demo
drwxr-xr-x@ 18 ta93abe  staff    576 May 11 20:56 cloudflare-observability-demo
drwxr-xr-x@  9 ta93abe  staff    288 Oct 16  2025 data-engineering
drwxr-xr-x@ 34 ta93abe  staff   1088 Apr 30 17:43 data-engineering-with-cloudflare
drwxr-xr-x@ 20 ta93abe  staff    640 Sep 30  2025 data-engineering-with-snowflake-and-aws
drwxr-xr-x@ 16 ta93abe  staff    512 Feb 18 23:11 dbt-docs-astronaut
drwxr-xr-x@  7 ta93abe  staff    224 Mar  9 19:55 dbt-glossary
drwxr-xr-x@ 15 ta93abe  staff    480 Feb 27 13:15 dbt-jobs
drwxr-xr-x@ 15 ta93abe  staff    480 May 12 15:17 dotfiles
drwxr-xr-x@  4 ta93abe  staff    128 Nov 15 19:53 enbu
drwxrwxr-x@ 14 ta93abe  staff    448 May 10 20:24 evidence-demo
drwxr-xr-x@  3 ta93abe  staff     96 May  7 16:14 frosty-friday
drwxr-xr-x@  3 ta93abe  staff     96 May 12 21:30 mai
```

> TOOL

tool_result
id: toolu_012LCoNR7ZocxEW4S38t71m2
```
npm warn exec The following package was not found and will be installed: wrangler@4.90.1
4.90.1
---
  - ai-search:write
  - ai-search:run
  - artifacts:write
  - flagship:write
  - connectivity:admin
  - email_routing:write
  - email_sending:write
  - browser:write
```

> TOOL

tool_result
id: toolu_01MoCejQDqDgZmQNTPxeLd34
```
{
  "type": "tool_reference",
  "tool_name": "mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation"
}
```

> AGENT

タスクを整理して進めます。

> TOOL

tool_use ToolSearch
id: toolu_01T2yrJhbfE7LFLfFKhqwita
```json
{
  "query": "select:TaskCreate,TaskUpdate,TaskList",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_01T2yrJhbfE7LFLfFKhqwita
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskList"
}
```

> TOOL

tool_use TaskCreate
id: toolu_018rEHwADk7rL9nWUqFhfpX6
```json
{
  "subject": "Workflows deploy 最小要件を調査",
  "description": "TS / Python それぞれの wrangler.jsonc 構造、必要な compatibility_flags、workflows binding 形式を Cloudflare docs で確認",
  "activeForm": "Cloudflare docs を確認中"
}
```

> TOOL

tool_result
id: toolu_018rEHwADk7rL9nWUqFhfpX6
```
Task #1 created successfully: Workflows deploy 最小要件を調査
```

> TOOL

tool_use TaskCreate
id: toolu_01D9qGsYY6HcKhW3N27TMcb2
```json
{
  "subject": "cf-workflows-examples リポジトリを scaffold",
  "description": "~/Developer/github.com/ta93abe/cf-workflows-examples/ を作成し、git init、README、.gitignore、ts/ と py/ ディレクトリを用意",
  "activeForm": "リポジトリを scaffold 中"
}
```

> TOOL

tool_result
id: toolu_01D9qGsYY6HcKhW3N27TMcb2
```
Task #2 created successfully: cf-workflows-examples リポジトリを scaffold
```

> TOOL

tool_use TaskCreate
id: toolu_01GCdeK3w2nGJrcvg491vDMd
```json
{
  "subject": "ts/ に ImageProcessingWorkflow Worker を作成",
  "description": "package.json、wrangler.jsonc (Workflow binding + R2/AI 設定)、src/index.ts (Workflow class + fetch handler)、tsconfig.json を作成。wrangler deploy --dry-run で通ることを確認",
  "activeForm": "TS Worker を作成中"
}
```

> TOOL

tool_result
id: toolu_01GCdeK3w2nGJrcvg491vDMd
```
Task #3 created successfully: ts/ に ImageProcessingWorkflow Worker を作成
```

> TOOL

tool_use TaskCreate
id: toolu_01JkV8xamRMNfVSL1V6MEvpt
```json
{
  "subject": "py/ に IngestWorkflow Worker を作成",
  "description": "wrangler.jsonc (python_workers compat flag + Workflow binding)、src/entry.py (WorkflowEntrypoint + fetch handler)、必要なら requirements.txt を作成。wrangler deploy --dry-run で通ることを確認",
  "activeForm": "Python Worker を作成中"
}
```

> TOOL

tool_result
id: toolu_01JkV8xamRMNfVSL1V6MEvpt
```
Task #4 created successfully: py/ に IngestWorkflow Worker を作成
```

> TOOL

tool_use TaskCreate
id: toolu_018aikrzoTVzYezHVzWguoim
```json
{
  "subject": "両 Worker で wrangler deploy を実行",
  "description": "ts/ と py/ で wrangler deploy を実行し、URL を取得",
  "activeForm": "wrangler deploy を実行中"
}
```

> TOOL

tool_result
id: toolu_018aikrzoTVzYezHVzWguoim
```
Task #5 created successfully: 両 Worker で wrangler deploy を実行
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01PCEppRYoQw6Vas6HDZw2UU
```json
{
  "query": "Workflows wrangler.jsonc minimum configuration WorkflowEntrypoint binding deploy TypeScript"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01415J6GVbojNdePMySCyxBN
```json
{
  "query": "Python Workflows WorkflowEntrypoint wrangler python_workers compatibility flag deploy"
}
```

> TOOL

tool_result
id: toolu_01PCEppRYoQw6Vas6HDZw2UU
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/ai-search/api/migration/workers-binding/</url>
<title></title>
<text>
## Requirements

The new bindings require the following minimum package versions for TypeScript types and local development support.

| Package                   | Minimum version |
| ------------------------- | --------------- |
| @cloudflare/workers-types | 4.20260304.0    |
| wrangler                  | 4.68.1          |

## Step 1: Update Wrangler configuration

Existing instances are in the default namespace. For a simple upgrade path, use the instance binding. For the namespace binding, refer to [AI Search bindings](#ai-search-bindings).

**Before:**

* [  wrangler.jsonc ](#tab-panel-5159)
* [  wrangler.toml ](#tab-panel-5160)

JSONC

```

{

  "$schema": "./node_modules/wrangler/config-schema.json",

  "ai": {

    "binding": "AI"

  }

}


```

TOML

```

[ai]

binding = "AI"


```

**After:**

* [  wrangler.jsonc ](#tab-panel-5161)
* [  wrangler.toml ](#tab-panel-5162)

JSONC

```

{

  "$schema": "./node_modules/wrangler/config-schema.json",

  "compatibility_date": "2026-03-27",

  "ai_search": [

    {

      "binding": "MY_INSTANCE",

      "instance_name": "my-instance"

    }

  ]

}


```

Explain Code

TOML

```

compatibility_date = "2026-03-27"


[[ai_search]]

binding = "MY_INSTANCE"

instance_name = "my-instance"


```

## Step 2: Update the type definition

Update the `Env` interface to use the new binding type.

**Before:**

TypeScript

```

export interface Env {

  AI: Ai;

}


```

**After:**

TypeScript

```

export interface Env {

  MY_INSTANCE: AiSearchInstance;

}


```

## Step 3: Update search calls

Replace `env.AI.autorag()` calls with the new binding. […]

> TOOL

tool_result
id: toolu_01415J6GVbojNdePMySCyxBN
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/python/</url>
<title></title>
<text>
## Get Started

The main entrypoint for a Python workflow is the [WorkflowEntrypoint](/workflows/build/workers-api/#workflowentrypoint) class. Your workflow logic should exist inside the [run](/workflows/build/workers-api/#run) handler.

Python

```

from workers import WorkflowEntrypoint


class MyWorkflow(WorkflowEntrypoint):

    async def run(self, event, step):

        # steps here


```

For example, a Workflow may be defined as:

Python

```

from workers import Response, WorkflowEntrypoint, WorkerEntrypoint


class PythonWorkflowStarter(WorkflowEntrypoint):

    async def run(self, event, step):


        @step.do('step1')

        async def step_1():

            # does stuff

            print('executing step1')


        @step.do('step2')

        async def step_2():

            # does stuff

            print('executing step2')


        await step_1()

        await step_2()


class Default(WorkerEntrypoint):

    async def fetch(self, request):

        await self.env.MY_WORKFLOW.create()

        return Response("Hello world!")


```

Explain Code

You must add both `python_workflows` and `python_workers` compatibility flags to your Wrangler configuration file.

* [  wrangler.jsonc ](#tab-panel-11123)
* [  wrangler.toml ](#tab-panel-11124)

JSONC

```

{

  "$schema": "./node_modules/wrangler/config-schema.json",

  "name": "hello-python",

  "main": "src/entry.py",

  "compatibility_flags": [

    "python_workers",

    "python_workflows"

  ],

  // Set this to today's date

  "compatibility_date": "2026-04-22",

  "workflows": [

    {

      "name": "workflows-demo",

      "binding": "MY_WORKFLOW",

      "class_name": "PythonWorkflowStarter"

    }

  ]

}


```

Explain Code

TOML

```

"$schema" = "./node_modules/wrangler/config-schema.json"

name = "hello-python"

main = "src/entry.py"

compatibility_flags = [ "python_workers", "python_workflows" ]

# Set this to today's date

compatibility_date = "2026-04-22"


[[workflows]]

name = "workflows-demo"

binding = "MY_WORKFLOW"


"$schema" […]

> AGENT

docs で要件が固まりました:

★ Insight ─────────────────────────────────────
- **TS**: `wrangler.jsonc` に `workflows[]` (name / binding / class_name) を書き、`WorkflowEntrypoint` を export + Worker の fetch handler を default export するだけ。R2 / Workers AI は実行時必要だが deploy 通過には不要
- **Python**: `compatibility_flags: ["python_workers", "python_workflows"]` が必須・`compatibility_date >= 2025-08-01`・Beta 状態。**現行の Python Worker は `Default(WorkerEntrypoint)` クラスに fetch を入れる新仕様** (2025-08-14 以降のデフォルト) なので、スライドの Workflow class とは別に Worker class が必要
- スライドの `step.waitForEvent` / `get_a` 等は deploy 通過に不要 — 残しても良いがダミー実装にする
─────────────────────────────────────────────────

> TOOL

tool_use TaskUpdate
id: toolu_01W3h3f2jGFFEPRdhNi52dDT
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01W3h3f2jGFFEPRdhNi52dDT
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01Eoa2q89GQmsQ6QAn6P197t
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01Eoa2q89GQmsQ6QAn6P197t
```
Updated task #2 status
```

> TOOL

tool_use Bash
id: toolu_01E3LXEnXNTDqart9vZBLXkj
```json
{
  "command": "mkdir -p /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/src /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/src && cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples && git init -b main && ls -la",
  "description": "cf-workflows-examples ディレクトリと ts/py サブディレクトリを作成し git init"
}
```

> TOOL

tool_result
id: toolu_01E3LXEnXNTDqart9vZBLXkj
```
Initialized empty Git repository in /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/.git/
total 0
drwxr-xr-x@  5 ta93abe  staff   160 May 13 17:41 .
drwxr-xr-x@ 32 ta93abe  staff  1024 May 13 17:41 ..
drwxr-xr-x@  9 ta93abe  staff   288 May 13 17:41 .git
drwxr-xr-x@  3 ta93abe  staff    96 May 13 17:41 py
drwxr-xr-x@  3 ta93abe  staff    96 May 13 17:41 ts
Shell cwd was reset to /Users/ta93abe/Developer/github.com/ta93abe/slides
```

> AGENT

リポジトリ scaffold OK。次は `.gitignore` と README、そして TS Worker から作っていきます。

> TOOL

tool_use Write
id: toolu_01W7MWKnEWuo6d4vPv8xJxbL
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/.gitignore",
  "content": "node_modules/\n.wrangler/\n.dev.vars\n.DS_Store\ndist/\n.venv/\n__pycache__/\n*.pyc\nworker-configuration.d.ts\n"
}
```

> TOOL

tool_use Write
id: toolu_01Cb6KPqYyS9Af9MGMtKD1BG
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/README.md",
  "content": "# cf-workflows-examples\n\nCloudflare Workflows のサンプル 2 種を 1 リポジトリにまとめたもの。Cloudflare Data Platform 登壇 (2026-05-13) のスライド `cloudflare-data-platform/pages/workflows.md` で取り上げたコードを実際にデプロイ可能な形にしたもの。\n\n## 構成\n\n```\n.\n├── ts/    TypeScript: ImageProcessingWorkflow (R2 → Workers AI → human approval → R2)\n└── py/    Python:     IngestWorkflow         (引数名で依存解決する diamond DAG)\n```\n\n両者は 1 Worker = 1 言語の制約があるため、独立した Worker としてデプロイされる。\n\n## デプロイ\n\n### TypeScript\n\n```sh\ncd ts\npnpm install\npnpm dlx wrangler deploy\n```\n\n### Python\n\n```sh\ncd py\npnpm dlx wrangler deploy\n```\n\n## ゴール\n\n`wrangler deploy` が成功する最小構成。R2 / Workers AI / 承認 API といった実行時依存は Workflow を実際に動かす段階で別途用意する想定。\n"
}
```

> TOOL

tool_result
id: toolu_01W7MWKnEWuo6d4vPv8xJxbL
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/.gitignore (file state is current in your context — no need to Read it back)
```

> TOOL

tool_result
id: toolu_01Cb6KPqYyS9Af9MGMtKD1BG
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/README.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
id: toolu_018k72gsU92huV2nHiE1fQNa
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_018k72gsU92huV2nHiE1fQNa
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01RFWJYKsJdWZQc2CqpafKn9
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01RFWJYKsJdWZQc2CqpafKn9
```
Updated task #3 status
```

> AGENT

## TS Worker を組み立て

スライドのコードに加えて、`wrangler deploy` を通すために必要な周辺ファイルを用意します。

> TOOL

tool_use Write
id: toolu_019HF1e51qt8jsBur8W1YidB
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/package.json",
  "content": "{\n  \"name\": \"image-processing-workflow\",\n  \"version\": \"0.0.0\",\n  \"private\": true,\n  \"type\": \"module\",\n  \"scripts\": {\n    \"deploy\": \"wrangler deploy\",\n    \"dev\": \"wrangler dev\",\n    \"types\": \"wrangler types\"\n  },\n  \"devDependencies\": {\n    \"@cloudflare/workers-types\": \"^4.20260304.0\",\n    \"typescript\": \"^5.6.0\",\n    \"wrangler\": \"^4.90.0\"\n  }\n}\n"
}
```

> TOOL

tool_result
id: toolu_019HF1e51qt8jsBur8W1YidB
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/package.json (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01Kp1oMYhQ9nYuS6bzeZZMqX
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/tsconfig.json",
  "content": "{\n  \"compilerOptions\": {\n    \"target\": \"es2022\",\n    \"module\": \"es2022\",\n    \"moduleResolution\": \"bundler\",\n    \"lib\": [\"es2022\"],\n    \"types\": [\"@cloudflare/workers-types\"],\n    \"strict\": true,\n    \"esModuleInterop\": true,\n    \"skipLibCheck\": true,\n    \"noEmit\": true\n  },\n  \"include\": [\"src/**/*.ts\"]\n}\n"
}
```

> TOOL

tool_result
id: toolu_01Kp1oMYhQ9nYuS6bzeZZMqX
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/tsconfig.json (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01MJRoPbeQiWisaESU1WvxZM
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/wrangler.jsonc",
  "content": "{\n  \"$schema\": \"./node_modules/wrangler/config-schema.json\",\n  \"name\": \"image-processing-workflow\",\n  \"main\": \"src/index.ts\",\n  \"compatibility_date\": \"2026-05-13\",\n  \"observability\": {\n    \"enabled\": true\n  },\n  \"workflows\": [\n    {\n      \"name\": \"image-processing\",\n      \"binding\": \"IMAGE_PROCESSING\",\n      \"class_name\": \"ImageProcessingWorkflow\"\n    }\n  ]\n  // R2 / Workers AI binding は Workflow を実行する段階で追加する。\n  // 例:\n  // \"r2_buckets\": [{ \"binding\": \"BUCKET\", \"bucket_name\": \"your-bucket\" }],\n  // \"ai\": { \"binding\": \"AI\" }\n}\n"
}
```

> TOOL

tool_result
id: toolu_01MJRoPbeQiWisaESU1WvxZM
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/wrangler.jsonc (file state is current in your context — no need to Read it back)
```

> AGENT

ここでスライドのコードをそのまま使った Workflow class を書きます。`step.waitForEvent` は実行時に必要だが deploy 通過には残しても OK。Worker から trigger するための fetch handler が追加で必要 (スライドには無い)。

> TOOL

tool_use Write
id: toolu_011e9CPNmLNwtmRSLabfKNR8
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/src/index.ts",
  "content": "import {\n  WorkflowEntrypoint,\n  type WorkflowEvent,\n  type WorkflowStep,\n} from \"cloudflare:workers\";\n\ntype Env = {\n  IMAGE_PROCESSING: Workflow;\n  BUCKET?: R2Bucket;\n  AI?: Ai;\n};\n\ntype Params = {\n  imageKey: string;\n};\n\nexport class ImageProcessingWorkflow extends WorkflowEntrypoint<Env, Params> {\n  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {\n    const imageData = await step.do(\"fetch image\", async () => {\n      const object = await this.env.BUCKET!.get(event.payload.imageKey);\n      return await object!.arrayBuffer();\n    });\n\n    const description = await step.do(\"generate description\", async () => {\n      const imageArray = Array.from(new Uint8Array(imageData));\n      return await this.env.AI!.run(\"@cf/llava-hf/llava-1.5-7b-hf\", {\n        image: imageArray,\n        prompt: \"Describe this image in one sentence\",\n        max_tokens: 50,\n      });\n    });\n\n    await step.waitForEvent(\"await approval\", {\n      type: \"approved\",\n      timeout: \"24 hours\",\n    });\n\n    await step.do(\"publish\", async () => {\n      await this.env.BUCKET!.put(`public/${event.payload.imageKey}`, imageData);\n      return { description };\n    });\n  }\n}\n\nexport default {\n  async fetch(request: Request, env: Env): Promise<Response> {\n    const url = new URL(request.url);\n\n    if (url.pathname === \"/start\") {\n      const imageKey = url.searchParams.get(\"imageKey\") ?? \"sample.jpg\";\n      const instance = await env.IMAGE_PROCESSING.create({\n        params: { imageKey },\n      });\n      return Response.json({ id: instance.id, status: await instance.status() });\n    }\n\n    if (url.pathname === \"/status\") {\n      const id = url.searchParams.get(\"id\");\n      if (!id) return new Response(\"missing id\", { status: 400 });\n      const instance = await env.IMAGE_PROCESSING.get(id);\n      return Response.json(await instance.status());\n    }\n\n    return new Response(\n      \"ImageProcessingWorkflow demo\\n\" +\n        \"POST or […]

> TOOL

tool_result
id: toolu_011e9CPNmLNwtmRSLabfKNR8
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/src/index.ts (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01KA3YFdqVP9U6qwe6Tig3GN
```json
{
  "command": "cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts && pnpm install 2>&1 | tail -15",
  "description": "TS Worker の依存をインストール"
}
```

> TOOL

tool_result
id: toolu_01KA3YFdqVP9U6qwe6Tig3GN
```
devDependencies:
+ @cloudflare/workers-types 4.20260511.1
+ typescript 5.9.3 (6.0.3 is available)
+ wrangler 4.90.1

╭ Warning ─────────────────────────────────────────────────────────────────────╮
│                                                                              │
│   Ignored build scripts: esbuild@0.27.3, sharp@0.34.5,                       │
│   workerd@1.20260508.1.                                                      │
│   Run "pnpm approve-builds" to pick which dependencies should be allowed     │
│   to run scripts.                                                            │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
Done in 3.1s using pnpm v10.33.2
```

> TOOL

tool_use Bash
id: toolu_01AqzifgqbtgMFPHkT1nAEoA
```json
{
  "command": "pnpm dlx wrangler deploy --dry-run 2>&1 | tail -40",
  "description": "TS Worker の deploy 検証 (dry-run)"
}
```

> TOOL

tool_result
id: toolu_01AqzifgqbtgMFPHkT1nAEoA
```
Progress: resolved 1, reused 0, downloaded 0, added 0
Packages: +36
++++++++++++++++++++++++++++++++++++
Progress: resolved 89, reused 38, downloaded 0, added 36, done
╭ Warning ─────────────────────────────────────────────────────────────────────╮
│                                                                              │
│   Ignored build scripts: esbuild@0.27.3, sharp@0.34.5,                       │
│   workerd@1.20260508.1.                                                      │
│   Run "pnpm approve-builds" to pick which dependencies should be allowed     │
│   to run scripts.                                                            │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

 ⛅️ wrangler 4.90.1
───────────────────

Cloudflare collects anonymous telemetry about your usage of Wrangler. Learn more at https://github.com/cloudflare/workers-sdk/tree/main/packages/wrangler/telemetry.md
Total Upload: 2.09 KiB / gzip: 0.92 KiB
Your Worker has access to the following bindings:
Binding                                             Resource      
env.IMAGE_PROCESSING (ImageProcessingWorkflow)      Workflow      

--dry-run: exiting now.
```

> AGENT

TS Worker dry-run 成功。`env.IMAGE_PROCESSING (ImageProcessingWorkflow) Workflow` が認識されました。Python に進みます。

> TOOL

tool_use TaskUpdate
id: toolu_01JQDLWfC41LP8fFSK8ng9qt
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01JQDLWfC41LP8fFSK8ng9qt
```
Updated task #3 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01AtmtqmTuiWxX4ZhzLnzzFW
```json
{
  "taskId": "4",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01AtmtqmTuiWxX4ZhzLnzzFW
```
Updated task #4 status
```

> TOOL

tool_use Write
id: toolu_01DTU2VWRkcJu7JhSQb61n3o
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/wrangler.jsonc",
  "content": "{\n  \"$schema\": \"./node_modules/wrangler/config-schema.json\",\n  \"name\": \"ingest-workflow-py\",\n  \"main\": \"src/entry.py\",\n  \"compatibility_date\": \"2026-05-13\",\n  \"compatibility_flags\": [\"python_workers\", \"python_workflows\"],\n  \"observability\": {\n    \"enabled\": true\n  },\n  \"workflows\": [\n    {\n      \"name\": \"ingest-workflow\",\n      \"binding\": \"INGEST\",\n      \"class_name\": \"IngestWorkflow\"\n    }\n  ]\n}\n"
}
```

> TOOL

tool_result
id: toolu_01DTU2VWRkcJu7JhSQb61n3o
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/wrangler.jsonc (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01XiPQvDHFhJ7ZCENGdowNWB
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/src/entry.py",
  "content": "from workers import Response, WorkerEntrypoint, WorkflowEntrypoint\n\n\nasync def get_a():\n    return {\"source\": \"a\", \"value\": 1}\n\n\nasync def get_b():\n    return {\"source\": \"b\", \"value\": 2}\n\n\ndef combine(a, b):\n    return {\"merged\": [a, b]}\n\n\nclass IngestWorkflow(WorkflowEntrypoint):\n    async def run(self, event, step):\n        @step.do()\n        async def fetch_a():\n            return await get_a()\n\n        @step.do()\n        async def fetch_b():\n            return await get_b()\n\n        @step.do(concurrent=True)\n        async def merge(fetch_a, fetch_b):\n            return combine(fetch_a, fetch_b)\n\n        return await merge()\n\n\nclass Default(WorkerEntrypoint):\n    async def fetch(self, request):\n        instance = await self.env.INGEST.create()\n        status = await instance.status()\n        return Response.json({\"id\": instance.id, \"status\": status})\n"
}
```

> TOOL

tool_result
id: toolu_01XiPQvDHFhJ7ZCENGdowNWB
```
File created successfully at: /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/src/entry.py (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01RboySgMbAyAYK79EQr66ro
```json
{
  "command": "cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py && pnpm dlx wrangler deploy --dry-run 2>&1 | tail -40",
  "description": "Python Worker の deploy 検証 (dry-run)"
}
```

> TOOL

tool_result
id: toolu_01RboySgMbAyAYK79EQr66ro
```
 ⛅️ wrangler 4.90.1
───────────────────
Total Upload: 0.85 KiB / gzip: 0.35 KiB
Your Worker has access to the following bindings:
Binding                          Resource      
env.INGEST (IngestWorkflow)      Workflow      

--dry-run: exiting now.
```

> AGENT

両方の dry-run が通りました。実際の deploy に進みます。

> TOOL

tool_use TaskUpdate
id: toolu_01CBgnpBjGCjCLSxW6bdPq5n
```json
{
  "taskId": "4",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01CBgnpBjGCjCLSxW6bdPq5n
```
Updated task #4 status
```

> TOOL

tool_use TaskUpdate
id: toolu_01YEKYw5ngBDPZhRM6iS47AC
```json
{
  "taskId": "5",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01YEKYw5ngBDPZhRM6iS47AC
```
Updated task #5 status
```

> TOOL

tool_use Bash
id: toolu_01KZBFCR3fUzHYWeZzJxTxjY
```json
{
  "command": "cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts && pnpm dlx wrangler deploy 2>&1 | tail -30",
  "description": "TS Worker を本番デプロイ"
}
```

> TOOL

tool_result
id: toolu_01KZBFCR3fUzHYWeZzJxTxjY
```
 ⛅️ wrangler 4.90.1
───────────────────
Total Upload: 2.09 KiB / gzip: 0.92 KiB
Your Worker has access to the following bindings:
Binding                                             Resource      
env.IMAGE_PROCESSING (ImageProcessingWorkflow)      Workflow      

Uploaded image-processing-workflow (2.00 sec)
Deployed image-processing-workflow triggers (3.18 sec)
  https://image-processing-workflow.ta93abe.workers.dev
  workflow: image-processing
Current Version ID: f5956acf-2f4a-49ca-8122-1589017d7c54
```

> AGENT

TS デプロイ成功 → `https://image-processing-workflow.ta93abe.workers.dev`。次は Python。

> TOOL

tool_use Bash
id: toolu_017Zwt16XBDDiaN3EG8MpWJZ
```json
{
  "command": "cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py && pnpm dlx wrangler deploy 2>&1 | tail -30",
  "description": "Python Worker を本番デプロイ"
}
```

> TOOL

tool_result
id: toolu_017Zwt16XBDDiaN3EG8MpWJZ
```
      .run(globals, locals)
       ~~~^^^^^^^^^^^^^^^^^
    File "/lib/python313.zip/_pyodide/_base.py", line 357, in run
      coroutine = eval(self.code, globals, locals)
    File "<exec>", line 9, in <module>
    File "/lib/python313.zip/_pyodide/_base.py", line 666, in pyimport_impl
      res = __import__(stem, fromlist=fromlist)
    File "/session/metadata/entry.py", line 1, in <module>
      from workers import Response, WorkerEntrypoint, WorkflowEntrypoint
    File "/lib/python3.13/site-packages/workers/__init__.py", line 3, in <module>
      raise err
  ModuleNotFoundError: No module named 'workers'
  You need to update to workers-py >= 1.90 or to pass disable_python_external_sdk
  
    at null.<anonymous> (pyodideRuntime-internal:emscriptenSetup:19917:14) in new_error
    at [object Object] in $wrap_exception
    at [object Object] in $pythonexc2js
    at null.<anonymous> (pyodideRuntime-internal:emscriptenSetup:22409:37) in callPyObjectKwargs
    at null.<anonymous> (pyodideRuntime-internal:emscriptenSetup:23307:20) in callKwargs
    at null.<anonymous> (pyodideRuntime-internal:emscriptenSetup:24467:87) in runPython
    at null.<anonymous> (pyodide:python-entrypoint-helper:76:17) in handleSrcImport
    at null.<anonymous> (pyodide:python-entrypoint-helper:198:17)
   [code: 10021]
  To learn more about this error, visit: [4mhttps://developers.cloudflare.com/workers/observability/errors/#validation-errors-10021[0m

  
  If you think this is a bug, please open an issue at: [4mhttps://github.com/cloudflare/workers-sdk/issues/new/choose[0m


🪵  Logs were written to "/Users/ta93abe/Library/Preferences/.wrangler/logs/wrangler-2026-05-13_08-43-32_574.log"
```

> AGENT

Python Worker のデプロイがエラー。`workers` モジュールが見つからない問題で、現代の Python Workers は外部 SDK モードがデフォルトで、ローカルに `workers-py>=1.90` を入れて bundle するか、`disable_python_external_sdk` flag で runtime 内蔵 SDK にフォールバックする必要があります。

★ Insight ─────────────────────────────────────
- Python Workers の最近のアップデート (2025-2026) で SDK が **外部パッケージ化** (workers-py) され、`uv` でローカルに入れて deploy 時に bundle する仕組みに変わった
- `disable_python_external_sdk` compatibility flag を付けると、旧来通り **runtime 内蔵の `workers` モジュール** を使える — 最小構成で deploy したいときの逃げ道
─────────────────────────────────────────────────

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01RNSTkT3jmFEwRQied5emBM
```json
{
  "query": "disable_python_external_sdk compatibility flag workers-py 1.90 bundling"
}
```

> TOOL

tool_result
id: toolu_01RNSTkT3jmFEwRQied5emBM
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workers/configuration/compatibility-flags/</url>
<title></title>
<text>
### Upper-case HTTP methods

| **Default as of**   | 2024-10-14                          |
| ------------------- | ----------------------------------- |
| **Flag to enable**  | upper\_case\_all\_http\_methods     |
| **Flag to disable** | no\_upper\_case\_all\_http\_methods |

HTTP methods are expected to be upper-cased. Per the fetch spec, if the method is specified as `get`, `post`, `put`, `delete`, `head`, or `options`, implementations are expected to uppercase the method. All other method names would generally be expected to throw as unrecognized (for example, `patch` would be an error while `PATCH` is accepted). This is a bit restrictive, even if it is in the spec. This flag modifies the behavior to uppercase all methods prior to parsing so that the method is always recognized if it is a known method.

To restore the standard behavior, use the `no_upper_case_all_http_methods`compatibility flag.

### Automatically set the Symbol.toStringTag for Workers API objects

| **Default as of**   | 2024-09-26                  |
| ------------------- | --------------------------- |
| **Flag to enable**  | set\_tostring\_tag          |
| **Flag to disable** | do\_not\_set\_tostring\_tag |

A change was made to set the Symbol.toStringTag on all Workers API objects in order to fix several spec compliance bugs. Unfortunately, this change was more breaking […]

> AGENT

エラーメッセージそのものが `disable_python_external_sdk` flag を提案してくれているので、それを追加します。

> TOOL

tool_use Edit
id: toolu_019dFHLDxbqqD2G7qVk9X2oh
```json
{
  "replace_all": false,
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/wrangler.jsonc",
  "old_string": "  \"compatibility_flags\": [\"python_workers\", \"python_workflows\"],",
  "new_string": "  \"compatibility_flags\": [\n    \"python_workers\",\n    \"python_workflows\",\n    \"disable_python_external_sdk\"\n  ],"
}
```

> TOOL

tool_result
id: toolu_019dFHLDxbqqD2G7qVk9X2oh
```
The file /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/py/wrangler.jsonc has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01P8FDTuFErFLV9VUVMGa7qj
```json
{
  "command": "pnpm dlx wrangler deploy 2>&1 | tail -30",
  "description": "Python Worker を再デプロイ"
}
```

> TOOL

tool_result
id: toolu_01P8FDTuFErFLV9VUVMGa7qj
```
 ⛅️ wrangler 4.90.1
───────────────────
Total Upload: 0.85 KiB / gzip: 0.35 KiB
Worker Startup Time: 468 ms
Your Worker has access to the following bindings:
Binding                          Resource      
env.INGEST (IngestWorkflow)      Workflow      

Uploaded ingest-workflow-py (7.02 sec)
Deployed ingest-workflow-py triggers (1.54 sec)
  https://ingest-workflow-py.ta93abe.workers.dev
  workflow: ingest-workflow
Current Version ID: 9b1deb73-1ee2-4a9e-b13b-4bc9afcae8e1
```

> AGENT

両方のデプロイが成功しました。

> TOOL

tool_use TaskUpdate
id: toolu_019ucuommtHdE6ScAwYurNsm
```json
{
  "taskId": "5",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_019ucuommtHdE6ScAwYurNsm
```
Updated task #5 status
```

> TOOL

tool_use Bash
id: toolu_016F2728KRAdExxMcdLetJJU
```json
{
  "command": "curl -s https://image-processing-workflow.ta93abe.workers.dev/ | head -5",
  "description": "TS Worker のルートエンドポイントを叩いて動作確認"
}
```

> TOOL

tool_result
id: toolu_016F2728KRAdExxMcdLetJJU
```
ImageProcessingWorkflow demo
POST or GET /start?imageKey=<key> to trigger a run
GET /status?id=<id> to inspect an instance
```

> AGENT

TS Worker は実際に応答してます。最終構成と次にやることをまとめます。

## 完了状況

| | Worker 名 | URL | binding 状態 |
|---|---|---|---|
| TS | `image-processing-workflow` | https://image-processing-workflow.ta93abe.workers.dev | `IMAGE_PROCESSING (ImageProcessingWorkflow)` 登録済 |
| Python | `ingest-workflow-py` | https://ingest-workflow-py.ta93abe.workers.dev | `INGEST (IngestWorkflow)` 登録済 |

★ Insight ─────────────────────────────────────
- **R2 / Workers AI binding を `wrangler.jsonc` から省いても deploy は通る** — Cloudflare の検証は「コードが parse できて Workflow class が見つかること」までで、bindings の整合性は実行時チェック。デモを段階的に組み立てやすい設計
- Python は **Beta** ゆえに SDK 配布方式が `workers-py` (uv 経由 bundle) と内蔵 SDK の二系統に分岐していて、`disable_python_external_sdk` が最小デプロイの逃げ道になる。**正式運用なら `uv run pywrangler deploy` パスに移行する** のが推奨
─────────────────────────────────────────────────

## 実行に進めるには

実際に Workflow を動かすには bindings を追加して再 deploy するだけです。

- **TS の `ImageProcessingWorkflow`**: `wrangler.jsonc` の末尾コメントにある `r2_buckets` と `ai` をアンコメント → R2 バケットを `wrangler r2 bucket create <name>` で作成 → `/start?imageKey=<key>` で trigger → 承認は `instance.sendEvent({ type: 'approved', payload: {} })` を別ルートで実装
- **Python の `IngestWorkflow`**: 現状でも `/` に GET すれば `INGEST.create()` が走る。Workflows ダッシュボードでビジュアライザを確認できる

## ファイル一覧

```
~/Developer/github.com/ta93abe/cf-workflows-examples/
├── .gitignore
├── README.md
├── ts/
│   ├── package.json
│   ├── tsconfig.json
│   ├── wrangler.jsonc
│   └── src/index.ts
└── py/
    ├── wrangler.jsonc
    └── src/entry.py
```

リポジトリは git init のみで未コミットです。GitHub に push する or 最初のコミットを作るのが必要なら、その指示ください。

> DEVELOPER

workflow de

> DEVELOPER

workflow で loop とか if else がかけたりするよね。ドキュメント確認して

> AGENT

確認します。Workflows での control flow がどう扱われているか docs を引きます。

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01SHuTURHajA1FcUwNosTvAw
```json
{
  "query": "Workflows control flow loop if else conditional branch step.do pattern"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01K6tLEw8nur19kUXjewBvbw
```json
{
  "query": "Workflows rules for writing workflow steps determinism non-deterministic loop iteration"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01T4echqJzcbSpNSrMWqDSTp
```json
{
  "query": "Workflows visualizer DAG loop for-loop try catch retry pattern detect"
}
```

> TOOL

tool_result
id: toolu_01SHuTURHajA1FcUwNosTvAw
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/rules-of-workflows/</url>
<title></title>
<text>
### Use conditional logic carefully

You can use `if` statements, loops, and other control flow outside of steps. However, conditions must be based on **deterministic values** — either values from `event.payload` or return values from previous steps. Non-deterministic conditions (such as `Math.random()` or `Date.now()`) outside of steps can cause unexpected behavior if the Workflow restarts.

* [  JavaScript ](#tab-panel-10093)
* [  TypeScript ](#tab-panel-10094)

index.js

```

export class MyWorkflow extends WorkflowEntrypoint {

  async run(event, step) {

    const config = await step.do("fetch config", async () => {

      return await this.env.KV.get("feature-flags", { type: "json" });

    });


    // ✅ Good: Condition based on step output (deterministic)

    if (config.enableEmailNotifications) {

      await step.do("send email", async () => {

        // Send email logic

      });

    }


    // ✅ Good: Condition based on event payload (deterministic)

    if (event.payload.userType === "premium") {

      await step.do("premium processing", async () => {

        // Premium-only logic

      });

    }


    // 🔴 Bad: Condition based on non-deterministic value outside a step

    // This could behave differently if the Workflow restarts

    if (Math.random() > 0.5) {

      await step.do("maybe do something", async () => {});

    }


    // ✅ Good: Wrap non-deterministic values in a step

    const shouldProcess = await step.do("decide […]

> TOOL

tool_result
id: toolu_01K6tLEw8nur19kUXjewBvbw
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/rules-of-workflows/</url>
<title></title>
<text>
### Use conditional logic carefully

You can use `if` statements, loops, and other control flow outside of steps. However, conditions must be based on **deterministic values** — either values from `event.payload` or return values from previous steps. Non-deterministic conditions (such as `Math.random()` or `Date.now()`) outside of steps can cause unexpected behavior if the Workflow restarts.

* [  JavaScript ](#tab-panel-10093)
* [  TypeScript ](#tab-panel-10094)

index.js

```

export class MyWorkflow extends WorkflowEntrypoint {

  async run(event, step) {

    const config = await step.do("fetch config", async () => {

      return await this.env.KV.get("feature-flags", { type: "json" });

    });


    // ✅ Good: Condition based on step output (deterministic)

    if (config.enableEmailNotifications) {

      await step.do("send email", async () => {

        // Send email logic

      });

    }


    // ✅ Good: Condition based on event payload (deterministic)

    if (event.payload.userType === "premium") {

      await step.do("premium processing", async () => {

        // Premium-only logic

      });

    }


    // 🔴 Bad: Condition based on non-deterministic value outside a step

    // This could behave differently if the Workflow restarts

    if (Math.random() > 0.5) {

      await step.do("maybe do something", async () => {});

    }


    // ✅ Good: Wrap non-deterministic values in a step

    const shouldProcess = await step.do("decide […]

> TOOL

tool_result
id: toolu_01T4echqJzcbSpNSrMWqDSTp
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/changelog/post/2026-03-06-step-context-available/</url>
<title></title>
<text>
---
title: Workflow steps now expose retry attempt number via step context
description: Cloudflare Workflows, our durable execution engine, now supports step context in production &#38; local development
image: https://developers.cloudflare.com/changelog-preview.png
---

> Documentation Index  
> Fetch the complete documentation index at: https://developers.cloudflare.com/changelog/llms.txt  
> Use this file to discover all available pages before exploring further.

[Skip to content](#%5Ftop) 

# Changelog

New updates and improvements at Cloudflare.

[ Subscribe to RSS ](/changelog/rss/index.xml) [ View RSS feeds ](/fundamentals/new-features/available-rss-feeds/) 

![hero image](/_astro/hero.CVYJHPAd_26AMqX.svg) 

[ ← Back to all posts ](/changelog/) 

## Workflow steps now expose retry attempt number via step context

Mar 06, 2026 

[ Workflows ](/workflows/)[ Workers ](/workers/) 

Cloudflare Workflows allows you to configure specific retry logic for each step in your workflow execution. Now, you can access **which** retry attempt is currently executing for calls to `step.do()`:

TypeScript

```

await step.do("my-step", async (ctx) => {

  // ctx.attempt is 1 on first try, 2 on first retry, etc.

  console.log(`Attempt ${ctx.attempt}`);

});


```

You can use the step context for improved logging & observability, progressive backoff, or conditional logic in your workflow definition.

Note that the current attempt number is 1-indexed. For more information on retry behavior, refer […]

> AGENT

書けます。ただし「**determinism rule**」が制約条件として明文化されています。

## 書けるパターン (公式 docs より)

**`if / else` (条件分岐)** ✅
```typescript
const config = await step.do("fetch config", async () => {
  return await this.env.KV.get("feature-flags", { type: "json" });
});

if (config.enableEmailNotifications) {
  await step.do("send email", async () => { /* ... */ });
}

if (event.payload.userType === "premium") {
  await step.do("premium processing", async () => { /* ... */ });
}
```

**`for` ループ (動的ステップ展開)** ✅
```typescript
const catList = await step.do("get cat list from KV", async () => {
  return await this.env.KV.get("cat-list");
});

for (const cat of catList) {
  await step.do(`get cat: ${cat}`, async () => {
    return await this.env.KV.get(cat);
  });
}
```

## やってはいけないパターン

🔴 **非決定的な値を条件にする**
```typescript
if (Math.random() > 0.5) {  // ❌ 再起動時に経路が変わる
  await step.do("maybe do something", async () => {});
}
```

✅ **step.do の中にラップして deterministic に**
```typescript
const shouldProcess = await step.do("decide randomly", async () => {
  return Math.random() > 0.5;  // 結果は step として永続化されるので再起動後も同じ
});
if (shouldProcess) {
  await step.do("conditionally do something", async () => {});
}
```

🔴 **step 名が非決定的**
```typescript
await step.do(`step #1 at: ${Date.now()}`, ...)  // ❌ 名前が cache key なので毎回ミスする
```

★ Insight ─────────────────────────────────────
- **核となるルール**: control flow は step **の外** に書ける。ただし条件式・ループ対象は `event.payload` か **過去の step の戻り値** […]

> DEVELOPER

ts の方は loop やif/elseを組み込んでほしい。

> AGENT

スライドの「画像処理」文脈を保ちつつ、loop と if/else が自然に登場するパターンに拡張します。

★ Insight ─────────────────────────────────────
- 画像処理に **loop** を入れるなら「複数画像をバッチ処理」が自然 — `event.payload.imageKeys[]` を受けて `for` で展開、step 名に imageKey を埋め込めば各画像ごとに独立した durable step として cache される
- **if/else** は「自動承認 vs 人間承認」が現実味のある分岐 — Workers AI の判定結果 (confidence や `safety` スコア) が閾値を超えたら `step.do` で即 publish、超えなければ `step.waitForEvent` で 24h durable に承認待ち
- どちらも **deterministic** に基づく分岐: `imageKeys` は `event.payload` 由来、confidence は前段 step の戻り値由来 — 公式 docs の制約をクリアしている
─────────────────────────────────────────────────

> TOOL

tool_use Write
id: toolu_01LSkfmbAxyzW1PBoeCt4wGb
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/src/index.ts",
  "content": "import {\n  WorkflowEntrypoint,\n  type WorkflowEvent,\n  type WorkflowStep,\n} from \"cloudflare:workers\";\n\ntype Env = {\n  IMAGE_PROCESSING: Workflow;\n  BUCKET?: R2Bucket;\n  AI?: Ai;\n};\n\ntype Params = {\n  imageKeys: string[];\n  autoApproveThreshold: number;\n};\n\ntype AnalysisResult = {\n  description: string;\n  confidence: number;\n};\n\ntype ProcessedImage = {\n  key: string;\n  description: string;\n  confidence: number;\n  approval: \"auto\" | \"human\";\n};\n\nexport class ImageProcessingWorkflow extends WorkflowEntrypoint<Env, Params> {\n  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {\n    const { imageKeys, autoApproveThreshold } = event.payload;\n    const processed: ProcessedImage[] = [];\n\n    for (const imageKey of imageKeys) {\n      const imageData = await step.do(`fetch image: ${imageKey}`, async () => {\n        const object = await this.env.BUCKET!.get(imageKey);\n        return await object!.arrayBuffer();\n      });\n\n      const analysis = await step.do(\n        `analyze: ${imageKey}`,\n        async (): Promise<AnalysisResult> => {\n          const imageArray = Array.from(new Uint8Array(imageData));\n          const result = await this.env.AI!.run(\n            \"@cf/llava-hf/llava-1.5-7b-hf\",\n            {\n              image: imageArray,\n              prompt: \"Describe this image in one sentence\",\n              max_tokens: 50,\n            },\n          );\n          const description = (result as { description: string }).description;\n          return {\n            description,\n            confidence: Math.min(description.length / 60, 1),\n          };\n        },\n      );\n\n      if (analysis.confidence >= autoApproveThreshold) {\n        await step.do(`auto-publish: ${imageKey}`, async () => {\n          await this.env.BUCKET!.put(`public/${imageKey}`, imageData);\n        });\n        processed.push({\n          key: imageKey,\n          description: analysis.description,\n          confidence: analysis.confidence,\n          approval: \"auto\",\n        });\n      } else {\n        await step.waitForEvent(`await approval: ${imageKey}`, {\n          type: `approved:${imageKey}`,\n          timeout: \"24 hours\",\n […]

> TOOL

tool_result
id: toolu_01LSkfmbAxyzW1PBoeCt4wGb
```
The file /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts/src/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01GC1DAihAjLfXANAFmSNHQt
```json
{
  "command": "cd /Users/ta93abe/Developer/github.com/ta93abe/cf-workflows-examples/ts && pnpm dlx wrangler deploy --dry-run 2>&1 | tail -15",
  "description": "変更後の TS Worker を dry-run 検証"
}
```

> TOOL

tool_result
id: toolu_01GC1DAihAjLfXANAFmSNHQt
```
 ⛅️ wrangler 4.90.1
───────────────────
Total Upload: 3.86 KiB / gzip: 1.33 KiB
Your Worker has access to the following bindings:
Binding                                             Resource      
env.IMAGE_PROCESSING (ImageProcessingWorkflow)      Workflow      

--dry-run: exiting now.
```

> AGENT

dry-run 通りました。loop/if/else 版の deploy を完了させてから、バウンドワーカーの話に答えます。

> TOOL

tool_use Bash
id: toolu_01LPpcZksRVSuoiUTt4EqDoC
```json
{
  "command": "pnpm dlx wrangler deploy 2>&1 | tail -15",
  "description": "loop/if/else 版 TS Worker を本番デプロイ"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_019Wqy5xZ5FzYQZx5Ws4u73R
```json
{
  "query": "Workflows bound worker dashboard binding relationship class deploy"
}
```

> TOOL

tool_result
id: toolu_01LPpcZksRVSuoiUTt4EqDoC
```
 ⛅️ wrangler 4.90.1
───────────────────
Total Upload: 3.86 KiB / gzip: 1.33 KiB
Your Worker has access to the following bindings:
Binding                                             Resource      
env.IMAGE_PROCESSING (ImageProcessingWorkflow)      Workflow      

Uploaded image-processing-workflow (2.97 sec)
Deployed image-processing-workflow triggers (3.20 sec)
  https://image-processing-workflow.ta93abe.workers.dev
  workflow: image-processing
Current Version ID: 80dff4b8-1cc7-40a4-8599-7d826ef3947d
```

> TOOL

tool_result
id: toolu_019Wqy5xZ5FzYQZx5Ws4u73R
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workers/wrangler/configuration/</url>
<title></title>
<text>
### Workflows

[Workflows](/workflows/) allow you to build durable, multi-step applications using the Workers platform. A Workflow binding enables your Worker to create and manage Workflow instances programmatically.

To bind Workflows to your Worker, assign an array of the below object to the `workflows` key.

* `binding` ` string ` required  
   * The binding name used to refer to the Workflow in your Worker. The binding must be [a valid JavaScript variable name ↗](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar%5Fand%5Ftypes#variables). For example, `binding = "MY_WORKFLOW"` would be a valid name for the binding.
* `name` ` string ` required  
   * The name of the Workflow.
* `class_name` ` string ` required  
   * The name of the exported Workflow class. The `class_name` must match the name of the Workflow class exported from your Worker code.
* `script_name` ` string ` optional  
   * The name of the Worker script where the Workflow class is defined. Only required if the Workflow is defined in a different Worker than the one the binding is configured on.

Example:

* [  wrangler.jsonc ](#tab-panel-10514)
* [  wrangler.toml ](#tab-panel-10515)

JSONC

```

{

  "workflows": [

    {

      "binding": "<BINDING_NAME>",

      "name": "<WORKFLOW_NAME>",

      "class_name": "<CLASS_NAME>",

    },

  ],

}


```

TOML

``` […]

> AGENT

loop/if/else 版の deploy も成功。新しい質問に答えます。

> TOOL

tool_use TaskCreate
id: toolu_01FLemMYe1WFmNj9DC4hpU4R
```json
{
  "subject": "TS Worker に loop / if-else を組み込む",
  "description": "バッチ画像処理 + 信頼度ベース自動承認パターンに拡張。imageKeys[] を for で展開し、confidence >= threshold なら auto-publish、未満なら step.waitForEvent で人間承認待ち"
}
```

> TOOL

tool_result
id: toolu_01FLemMYe1WFmNj9DC4hpU4R
```
Task #6 created successfully: TS Worker に loop / if-else を組み込む
```

> TOOL

tool_use TaskUpdate
id: toolu_01SzUFiuBLGGiXuis6hzQwuZ
```json
{
  "taskId": "6",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01SzUFiuBLGGiXuis6hzQwuZ
```
Updated task #6 status
```

> AGENT

## loop/if/else 版 deploy 完了

```
Uploaded image-processing-workflow (2.97 sec)
Deployed image-processing-workflow triggers (3.20 sec)
  https://image-processing-workflow.ta93abe.workers.dev
  workflow: image-processing
Current Version ID: 80dff4b8-1cc7-40a4-8599-7d826ef3947d
```

新しいエンドポイント:
- `GET /start?imageKeys=a.jpg,b.jpg&threshold=0.7` — バッチ起動
- `GET /approve?id=<id>&imageKey=<key>` — `step.waitForEvent` を release (人間承認パスのとき)

組み込んだパターン:
- **loop**: `for (const imageKey of imageKeys)` で各画像ごとに `step.do` (step 名に `imageKey` を埋めて cache key を deterministic に)
- **if/else**: `analysis.confidence >= autoApproveThreshold` で `auto-publish` vs `waitForEvent → 承認後 publish` を分岐

---

## 「バウンドワーカー (bound worker)」について

これは Workflows ダッシュボードでの用語で、**Workflow class を物理的に保持している Worker** のことです。

★ Insight ─────────────────────────────────────
- Cloudflare Workflows は「Workflow という独立リソース」ではなく、**Worker の中で `WorkflowEntrypoint` を継承したクラス** として実装される。だから 1 つの Workflow には必ず「そのクラスが書かれている Worker (= script)」が紐付く
- ダッシュボードで Workflow を開いたとき表示される「バウンドワーカー」は、その Workflow の `wrangler.jsonc` で `script_name` が指す Worker (省略時は同じ Worker) — 今回のケースだと `image-processing-workflow` Worker が `image-processing` Workflow の bound worker
─────────────────────────────────────────────────

### 今回の関係図

```
Worker:    image-processing-workflow
           ├── fetch handler (/start, /status, /approve)
           ├── class ImageProcessingWorkflow ← Workflow class
           └── binding: IMAGE_PROCESSING ──┐
                                            ↓
Workflow:  image-processing  ←─── bound worker: image-processing-workflow
```

`wrangler.jsonc` の対応関係:

| `wrangler.jsonc` のフィールド | ダッシュボード上の意味 |
|---|---|
| `name` (top-level): `image-processing-workflow` | **Worker 名** (= バウンドワーカー名) |
| `workflows[].name`: `image-processing` | **Workflow 名** |
| `workflows[].class_name`: `ImageProcessingWorkflow` | Worker 内のどのクラスが Workflow か |
| `workflows[].binding`: `IMAGE_PROCESSING` | Worker の `env` から参照するときの変数名 |
| `workflows[].script_name` (省略) […]

> AGENT

No response requested.

> DEVELOPER

workflow から workflow を呼べる？

> AGENT

docs で確認します。

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_016hpurSozgHsfWJ49P5Rue5
```json
{
  "query": "Workflow call another Workflow from inside step nested child sub workflow create"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01VsK3H3JpLe8jEuW8CXMJP9
```json
{
  "query": "Workflow binding multiple workflows trigger from workflow step.do create instance fan-out"
}
```

> TOOL

tool_result
id: toolu_016hpurSozgHsfWJ49P5Rue5
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/trigger-workflows/</url>
<title></title>
<text>
### Trigger a Workflow from another Workflow

You can create a new Workflow instance from within a step of another Workflow. The parent Workflow will not block waiting for the child Workflow to complete — it continues execution immediately after the child instance is successfully created.

* [  JavaScript ](#tab-panel-10626)
* [  TypeScript ](#tab-panel-10627)

JavaScript

```

export class ParentWorkflow extends WorkflowEntrypoint {

  async run(event, step) {

    // Perform initial work

    const result = await step.do("initial processing", async () => {

      // ... processing logic

      return { fileKey: "output.pdf" };

    });


    // Trigger a child workflow for additional processing

    const childInstance = await step.do("trigger child workflow", async () => {

      return await this.env.CHILD_WORKFLOW.create({

        id: `child-${event.instanceId}`,

        params: { fileKey: result.fileKey },

      });

    });


    // Parent continues immediately - not blocked by child workflow

    await step.do("continue with other work", async () => {

      console.log(`Started child workflow: ${childInstance.id}`);

      // This runs right away, regardless of child workflow status

    });

  }

}


```

TypeScript

```

export class ParentWorkflow extends WorkflowEntrypoint<Env, Params> {

  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {

    // Perform initial work

    const result = await step.do("initial processing", async () => {

      // ... processing logic

      return […]

> TOOL

tool_result
id: toolu_01VsK3H3JpLe8jEuW8CXMJP9
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/trigger-workflows/</url>
<title></title>
<text>
### Trigger a Workflow from another Workflow

You can create a new Workflow instance from within a step of another Workflow. The parent Workflow will not block waiting for the child Workflow to complete — it continues execution immediately after the child instance is successfully created.

* [  JavaScript ](#tab-panel-10626)
* [  TypeScript ](#tab-panel-10627)

JavaScript

```

export class ParentWorkflow extends WorkflowEntrypoint {

  async run(event, step) {

    // Perform initial work

    const result = await step.do("initial processing", async () => {

      // ... processing logic

      return { fileKey: "output.pdf" };

    });


    // Trigger a child workflow for additional processing

    const childInstance = await step.do("trigger child workflow", async () => {

      return await this.env.CHILD_WORKFLOW.create({

        id: `child-${event.instanceId}`,

        params: { fileKey: result.fileKey },

      });

    });


    // Parent continues immediately - not blocked by child workflow

    await step.do("continue with other work", async () => {

      console.log(`Started child workflow: ${childInstance.id}`);

      // This runs right away, regardless of child workflow status

    });

  }

}


```

TypeScript

```

export class ParentWorkflow extends WorkflowEntrypoint<Env, Params> {

  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {

    // Perform initial work

    const result = await step.do("initial processing", async () => {

      // ... processing logic

      return […]

> AGENT

呼べます。`step.do` の中で **child workflow の `create()` を呼ぶ** のが公式パターンです。

## 公式パターン (docs より)

```typescript
export class ParentWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event, step) {
    const result = await step.do("initial processing", async () => {
      return { fileKey: "output.pdf" };
    });

    // child workflow を起動
    const childInstance = await step.do("trigger child workflow", async () => {
      return await this.env.CHILD_WORKFLOW.create({
        id: `child-${event.instanceId}`,
        params: { fileKey: result.fileKey },
      });
    });

    // 親はここで即進む — 子の完了を待たない
    await step.do("continue with other work", async () => {
      console.log(`Started child workflow: ${childInstance.id}`);
    });
  }
}
```

★ Insight ─────────────────────────────────────
- **Fire-and-forget セマンティクス**: 親は `create()` が返ってきたらすぐ次へ進む。子は完全に独立して走る。「親が子を待つ」が欲しければ自前で `instance.status()` を polling するか、子から `sendEvent` で親に通知 + 親側で `step.waitForEvent` で受ける durable wait パターンを組む
- **必ず step.do で wrap する**: `create()` は副作用 (子インスタンス作成) を持つので、step 外で呼ぶと engine 再起動時に **子が二重起動** する可能性がある。これは [Rules of Workflows](https://developers.cloudflare.com/workflows/build/rules-of-workflows/) の「side effects は step に閉じ込めろ」の原則そのもの
- **ID を deterministic にする**: `id: \`child-${event.instanceId}\`` のように親 instance ID から導出すると、create 自体が冪等になる (重複 ID は `create` がエラーを返す = 重複防止になる)。`createBatch` を使うと最大 100 件一気に起動できて fan-out パターンに最適
─────────────────────────────────────────────────

## 設定上の必要事項

呼びたい子 Workflow への binding を **親 Worker の `wrangler.jsonc`** に追加するだけ:

```jsonc
{
  "name": "parent-worker",
  "workflows": [
    {
      "name": "parent",
      "binding": "PARENT",
      "class_name": "ParentWorkflow"
    },
    {
      "name": "child",
      "binding": "CHILD_WORKFLOW",
      "class_name": "ChildWorkflow"
      // 別 Worker にある場合は "script_name": "child-worker" を追加
    }
  ] […]

> DEVELOPER

Cloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。
DAGといいきっていいの？

> AGENT

良い突っ込み。公式 docs での表現を確認します。

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01U4rfMR1s4D9G2HL9CrbjGF
```json
{
  "query": "Workflows visualizer DAG directed acyclic graph diagram visualization loop control flow"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01QrYhaCwLmUkATpvSiY1KU7
```json
{
  "query": "Workflows visualizer graph structure flow chart parse code AST steps nodes"
}
```

> TOOL

tool_result
id: toolu_01U4rfMR1s4D9G2HL9CrbjGF
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/python/dag/</url>
<title></title>
<text>
---
title: DAG Workflows
description: Define directed acyclic graph (DAG) Workflows in Python with declarative step dependencies.
image: https://developers.cloudflare.com/dev-products-preview.png
---

[Skip to content](#%5Ftop) 

Was this helpful?

YesNo

[ Edit page ](https://github.com/cloudflare/cloudflare-docs/edit/production/src/content/docs/workflows/python/dag.mdx) [ Report issue ](https://github.com/cloudflare/cloudflare-docs/issues/new/choose) 

Copy page

# DAG Workflows

The Python Workflows SDK supports DAG workflows in a declarative way, using `step.do` and parameter names to define dependencies (other steps that must complete before a step can run).

Python

```

from workers import Response, WorkflowEntrypoint, WorkerEntrypoint



This pattern is useful for diamond shaped workflows, where a step depends on two or more other steps that can run concurrently.

```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"item":{"@id":"/directory/","name":"Directory"}},{"@type":"ListItem","position":2,"item":{"@id":"/workflows/","name":"Workflows"}},{"@type":"ListItem","position":3,"item":{"@id":"/workflows/python/","name":"Python Workflows SDK"}},{"@type":"ListItem","position":4,"item":{"@id":"/workflows/python/dag/","name":"DAG Workflows"}}]}
```
</text>
</result>
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/visualizer/</url>
<title></title>
<text>
## Execution order

Each node has a `starts` and `resolves` field that tracks execution order. These indices indicate when a promise began executing and when it ended, relative to the first promise that started without an immediate conclusion. This corresponds to vertical positioning in the diagram (i.e. all steps with `starts: 1` will appear inline).

When parsing, unawaited promises or `Promise.all()` calls are assigned an entry number stored in the `starts` field. When an `await` is encountered for that promise, the […]

> TOOL

tool_result
id: toolu_01QrYhaCwLmUkATpvSiY1KU7
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/visualizer/</url>
<title></title>
<text>
## Execution order

Each node has a `starts` and `resolves` field that tracks execution order. These indices indicate when a promise began executing and when it ended, relative to the first promise that started without an immediate conclusion. This corresponds to vertical positioning in the diagram (i.e. all steps with `starts: 1` will appear inline).

When parsing, unawaited promises or `Promise.all()` calls are assigned an entry number stored in the `starts` field. When an `await` is encountered for that promise, the entry number is incremented and saved as the exit number in the `resolves` field. This allows the diagram to determine which promises run concurrently and when each will complete relative to the others.

If steps are awaited at the point of declaration, `starts` and `resolves` will be undefined, and the Workflow executes in the order the steps appear to the runtime.

```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"item":{"@id":"/directory/","name":"Directory"}},{"@type":"ListItem","position":2,"item":{"@id":"/workflows/","name":"Workflows"}},{"@type":"ListItem","position":3,"item":{"@id":"/workflows/build/","name":"Build with Workflows"}},{"@type":"ListItem","position":4,"item":{"@id":"/workflows/build/visualizer/","name":"Visualize Workflows"}}]}
```
# Visualize Workflows

View a visual representation of your parsed Workflow code as a diagram on the Cloudflare dashboard.

The diagram illustrates your sequenced & parallel steps, conditionals, loops, and nested logic. To see the Workflow at a high level, view the diagram with […]

> AGENT

良い指摘です。**厳密には DAG と言い切れません**。Cloudflare 自身も Visualizer を "DAG" とは呼んでいません。

## 公式 docs での表現

`/workflows/build/visualizer/` を確認すると:

> View a visual representation of your parsed Workflow code as a **diagram** on the Cloudflare dashboard.
> The **diagram** illustrates your sequenced & parallel steps, conditionals, **loops**, and nested logic.

**"diagram"** または **"visual map"** と呼ばれていて、"DAG" という単語は出てきません。Changelog (2026-02-03 リリース) も同様。

## なぜ Cloudflare は "DAG" を避けているか

★ Insight ─────────────────────────────────────
- **DAG = Directed Acyclic Graph** で、定義上 **閉路 (cycle) を持たない**。`for` ループや `while` を含むコードはランタイム的には「同じ step 種が複数回実行される」= 概念的に閉路扱いになる
- Cloudflare の Visualizer はループを「折りたたんで 1 ノード ↔ 展開して各イテレーションを別ノード」として描く。**展開後は cycle が無いので描画上は DAG だが、コード構造としては cyclic** という二重性がある
- 一方 **Python Workflows SDK では明示的に "DAG Workflows" という章** がある (`/workflows/python/dag/`) — これは `@step.do(concurrent=True)` + 引数名依存で **静的に diamond shape の依存グラフ** を宣言するパターンを指す。**ループが含まれない、純粋に依存グラフだけで完結する書き方**なので DAG と呼べる
─────────────────────────────────────────────────

つまり:

| | 公式の呼び方 | DAG と呼べるか |
|---|---|---|
| TS/JS Visualizer (ループ含む) | "diagram" / "visual map" | △ 描画上は acyclic だが、コードは cyclic |
| Python `@step.do(concurrent=True)` パターン | "DAG Workflows" (明示) | ◎ ループ無しの純依存グラフ |
| スライドの dbt build 例 | (実体は TS/JS Visualizer) | △ Cloudflare は DAG と呼んでない |
| Airflow DAG View | "DAG" だが動的タスクは展開時のみ acyclic | △ 同じ二重性あり |

## スライドの該当箇所

`contents/cloudflare-data-platform/pages/workflows.md` を見ると、現状 3 箇所で "DAG" を使っています:

> TOOL

tool_use Bash
id: toolu_018F2s4DJjxVU93vNQn9T6M6
```json
{
  "command": "grep -n \"DAG\" /Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md",
  "description": "workflows.md の DAG 表記箇所をリストアップ"
}
```

> TOOL

tool_result
id: toolu_018F2s4DJjxVU93vNQn9T6M6
```
80:Cloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。
107:step・並列・条件分岐・ループの DAG を自動描画してくれます。
111:Airflow の DAG View に相当します。
120:`WorkflowEntrypoint` を Python で継承します。**関数パラメータ名で依存を暗黙解決** する DAG 表現が特徴です。引数名による暗黙的依存解決で DAG が宣言的に書けます。
154:  <li><span :class="['transition-opacity duration-300', $clicks === 0 || $clicks === 4 || $clicks > 4 ? '' : 'opacity-30']">`await merge()` 実行 — 依存先が並列起動 (diamond DAG)</span></li>
179:特徴的なのは DAG の表現方法です。
184:concurrent=True を付ければ、diamond shaped DAG が宣言的に書けます。
```

> AGENT

ビジュアライザのスライドだけ `layout` 未指定なので、`two-cols-header` に揃えます。

> TOOL

tool_use Read
id: toolu_01PNBwBnHPBPKjmbKeGWzP84
```json
{
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md",
  "offset": 76,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01PNBwBnHPBPKjmbKeGWzP84
```
76	---
77	
78	## ビジュアライザ
79	
80	Cloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。
81	
82	<div class="grid grid-cols-[3fr_2fr] gap-6 mt-3 text-sm">
83	
84	<div>
85	
86	- ループ / nested logic を **折りたたみ ↔ 展開** で切替
87	- 並列ステップ / 条件分岐も自動レイアウト
88	- TypeScript Workflows で利用可能 (Python は未対応)
89	
90	実例: 右図は一つ前のスライドの画像にアノテーションするコード例を無駄に複雑にしたものです。
91	
92	[Workflows Visualizer Doc](https://developers.cloudflare.com/workflows/build/visualizer/)
93	
94	</div>
95	
96	<div class="flex items-center justify-center">
97	
98	<img src="/image-processing-diagram.png" alt="Image Processing Workflow visualizer" class="scale-90 rounded border border-zinc-700/60 shadow-lg" />
99	
100	</div>
101	
102	</div>
103	
104	<!--
105	2026 年 2 月にリリースされた機能です。
106	Workflow コードをダッシュボードがパースして、
107	step・並列・条件分岐・ループの DAG を自動描画してくれます。
108	
109	右図は dbt build を Workflows で実行した例。
110	loop / try-catch / retry-backoff を含むパイプラインを一画面で俯瞰できます。
111	Airflow の DAG View に相当します。
112	-->
113	
114	---
115	layout: two-cols-header
```

> TOOL

tool_use Edit
id: toolu_01X1a3mLgGQ98TZp1wwn8fu8
```json
{
  "replace_all": false,
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md",
  "old_string": "---\n\n## ビジュアライザ\n\nCloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。\n\n<div class=\"grid grid-cols-[3fr_2fr] gap-6 mt-3 text-sm\">\n\n<div>\n\n- ループ / nested logic を **折りたたみ ↔ 展開** で切替\n- 並列ステップ / 条件分岐も自動レイアウト\n- TypeScript Workflows で利用可能 (Python は未対応)\n\n実例: 右図は一つ前のスライドの画像にアノテーションするコード例を無駄に複雑にしたものです。\n\n[Workflows Visualizer Doc](https://developers.cloudflare.com/workflows/build/visualizer/)\n\n</div>\n\n<div class=\"flex items-center justify-center\">\n\n<img src=\"/image-processing-diagram.png\" alt=\"Image Processing Workflow visualizer\" class=\"scale-90 rounded border border-zinc-700/60 shadow-lg\" />\n\n</div>\n\n</div>",
  "new_string": "---\nlayout: two-cols-header\n---\n\n## ビジュアライザ\n\nCloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。\n\n::left::\n\n- ループ / nested logic を **折りたたみ ↔ 展開** で切替\n- 並列ステップ / 条件分岐も自動レイアウト\n- TypeScript Workflows で利用可能 (Python は未対応)\n\n実例: 右図は一つ前のスライドの画像にアノテーションするコード例を無駄に複雑にしたものです。\n\n[Workflows Visualizer Doc](https://developers.cloudflare.com/workflows/build/visualizer/)\n\n::right::\n\n<img src=\"/image-processing-diagram.png\" alt=\"Image Processing Workflow visualizer\" class=\"scale-90 rounded border border-zinc-700/60 shadow-lg\" />"
}
```

> TOOL

tool_result
id: toolu_01X1a3mLgGQ98TZp1wwn8fu8
```
The file /Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

レイアウトを `two-cols-header` に変更しました。`grid` ベースの自前カラム指定をやめ、テーマの slot 機構 (`::left::` / `::right::`) に統一しています。

★ Insight ─────────────────────────────────────
- `two-cols-header` レイアウトはタイトルとリード文が **header 領域** を占め、`::left::` / `::right::` が **header の下** に左右に並ぶ — 自前 `grid grid-cols-[3fr_2fr]` だとタイトルもグリッド内に巻き込まれて header 領域に揃わない
- 他のスライドと同じレイアウト機構を使う利点: テーマ (`slidev-theme-enbu`) 側でタイポグラフィや余白を調整したときに **全スライドに一括反映される** — `grid grid-cols-...` の自前指定は孤島になってメンテ漏れする
─────────────────────────────────────────────────

---

## DAG 表記の修正は別件として残しています

先ほどの「DAG といい切っていいの?」への結論はこの行のままだとまだ Cloudflare 公式の言い回しと食い違っています:

```
80:  ...step / 並列 / 条件分岐 / ループの DAG 図 を自動生成
107: step・並列・条件分岐・ループの DAG を自動描画
111: Airflow の DAG View に相当します。  ← (ノート)
```

Python パートの DAG (`120, 154, 179, 184`) は公式 docs が "DAG Workflows" と章立てしてるので **そのまま残して OK**。問題は **TypeScript Visualizer 側の 2-3 箇所**。

修正候補:
- 「DAG 図」→「フロー図」or「ダイアグラム」(Cloudflare 公式の "diagram" に寄せる)
- 「Airflow の DAG View に相当」は note なのでそのまま残しても許容範囲 (Airflow も動的タスクは厳密 DAG ではないので類比としては成立)

修正しますか? Python パート (`@step.do(concurrent=True)` の方) は触らず、ビジュアライザの 80 行 + ノート 107 行だけ書き換える形が無難です。

> DEVELOPER

フロー図にしよ

> AGENT

ビジュアライザの 2 箇所 (本文 + ノート) だけ「フロー図」に直します。Python パートの "DAG" と Airflow の "DAG View" は固有名詞 / 公式章立てに合わせて残します。

> TOOL

tool_use Edit
id: toolu_01W5UWLj6gm6z2rKerhTuNNn
```json
{
  "replace_all": false,
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md",
  "old_string": "Cloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループの DAG 図** を自動生成します。",
  "new_string": "Cloudflare ダッシュボードが Workflow コードを parse し、**step / 並列 / 条件分岐 / ループのフロー図** を自動生成します。"
}
```

> TOOL

tool_result
id: toolu_01W5UWLj6gm6z2rKerhTuNNn
```
The file /Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_015aJvzfFn1gtsi56t2Whmq5
```json
{
  "replace_all": false,
  "file_path": "/Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md",
  "old_string": "step・並列・条件分岐・ループの DAG を自動描画してくれます。",
  "new_string": "step・並列・条件分岐・ループのフロー図を自動描画してくれます。"
}
```

> TOOL

tool_result
id: toolu_015aJvzfFn1gtsi56t2Whmq5
```
The file /Users/ta93abe/Developer/github.com/ta93abe/slides/contents/cloudflare-data-platform/pages/workflows.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

修正完了。

★ Insight ─────────────────────────────────────
- ビジュアライザ本文 (156行) とノート (175行) の 2 箇所だけ「フロー図」に変更。Cloudflare 公式の "diagram" 表現に寄り、かつ「ループを含むので厳密には DAG ではない」という突っ込みを回避
- Python パートの DAG (82, 141, 146行) と Airflow DAG View (179行) は意図的に残した — Python SDK の docs が `/workflows/python/dag/` という章を持っていて「DAG Workflows」は固有名詞、Airflow も同じ
─────────────────────────────────────────────────

残り `grep -n "DAG"` するとこうなります:

```
82:  ...DAG 表現が特徴です。引数名による暗黙的依存解決で DAG が宣言的に書けます。  ← Python (公式名称)
141: 特徴的なのは DAG の表現方法です。                                              ← Python ノート
146: diamond shaped DAG が宣言的に書けます。                                       ← Python ノート
179: Airflow の DAG View に相当します。                                            ← Airflow 固有名詞
```

すべて「Python の DAG Workflows」or「Airflow の DAG View」という固有名詞文脈なので、技術的に正確に残せています。

> DEVELOPER

workflowの起動はWorker経由なの？

> AGENT

確認します。

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01S1wMLYM7o1tUVhNW6DcYqc
```json
{
  "query": "trigger Workflow methods REST API CLI HTTP fetch handler queue cron scheduled durable object"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_016oJDpFLtGYCqp5UK75K8FH
```json
{
  "query": "Workflows REST API instances create curl POST endpoint without Worker"
}
```

> TOOL

tool_result
id: toolu_01S1wMLYM7o1tUVhNW6DcYqc
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workers/examples/cron-trigger/</url>
<title></title>
<text>
# Setting Cron Triggers

**Last reviewed:**  over 4 years ago 

Set a Cron Trigger for your Worker.

* [  JavaScript ](#tab-panel-9773)
* [  TypeScript ](#tab-panel-9774)
* [  Python ](#tab-panel-9775)
* [  Hono ](#tab-panel-9776)

JavaScript

```

export default {

  async scheduled(controller, env, ctx) {

    console.log("cron processed");

  },

};


```

TypeScript

```

interface Env {}

export default {

  async scheduled(

    controller: ScheduledController,

    env: Env,

    ctx: ExecutionContext,

  ) {

    console.log("cron processed");

  },

};


```

Explain Code

Python

```

from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):

    async def scheduled(self, controller, env, ctx):

        print("cron processed")


```

TypeScript

```

import { Hono } from "hono";


interface Env {}


// Create Hono app

const app = new Hono<{ Bindings: Env }>();


// Regular routes for normal HTTP requests

app.get("/", (c) => c.text("Hello World!"));


// Export both the app and a scheduled function

export default {

  // The Hono app handles regular HTTP requests

  fetch: app.fetch,


  // The scheduled function handles Cron triggers

  async scheduled(

    controller: ScheduledController,

    env: Env,

    ctx: ExecutionContext,

  ) {

    console.log("cron processed");


    // You could also perform actions like:

    // - Fetching data from external APIs

    // - Updating KV or Durable Object storage

    // - Running […]

> TOOL

tool_result
id: toolu_016oJDpFLtGYCqp5UK75K8FH
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/email-service/api/send-emails/rest-api/</url>
<title></title>
<text>
# REST API

The REST API allows you to send emails from any application using standard HTTP requests. Use it from any backend, serverless function, or CI/CD pipeline — no Cloudflare Workers binding is required.

For the full OpenAPI specification, refer to the [Email Sending API reference ↗](https://developers.cloudflare.com/api/resources/email%5Fsending/methods/send).

## Endpoint

```

POST https://api.cloudflare.com/client/v4/accounts/{account_id}/email/sending/send


```

## Authentication

Authenticate with a [Cloudflare API token](/fundamentals/api/get-started/create-token/) that has permission to send emails. Include it in the `Authorization` header:

```

Authorization: Bearer <API_TOKEN>


```

## Send an email

* [ Simple email ](#tab-panel-7027)
* [ Multiple recipients ](#tab-panel-7028)
* [ With CC and BCC ](#tab-panel-7029)

Terminal window

```

curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/email/sending/send" \

  --header "Authorization: Bearer <API_TOKEN>" \


</text>
</result>
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/call-workflows-from-pages/</url>
<title></title>
<text>
### Use Service Bindings

[Service Bindings](/workers/runtime-apis/bindings/service-bindings/) allow you to call a Worker from another Worker or a Pages Function without needing to expose it directly.

To do this, you will need to:

1. Deploy your Workflow in a Worker
2. Create a Service Binding to that Worker in your Pages project
3. Call the Worker remotely using the binding

For example, if you have a Worker called `workflows-starter`, you would create a new Service Binding […]

> AGENT

いえ、**Worker 経由は 3 通りある起動方法のうち 1 つ** です。docs (`/workflows/build/trigger-workflows/`) には明示的に 3 つの経路が並んでいます:

## Workflow を起動する 3 経路

### 1. Worker 経由 (Workers API / Bindings) — 最も典型

Worker の `wrangler.jsonc` に Workflow binding を持たせて、Worker のいずれかの handler から `env.MY_WORKFLOW.create()` を呼ぶ。Worker 内の起点は 4 種類:

| handler | きっかけ |
|---|---|
| `fetch` | HTTP リクエスト (今回のリポジトリの `/start` 方式) |
| `queue` | Cloudflare Queues のメッセージ消費 |
| `scheduled` | Cron Trigger (定期実行) |
| Durable Object 内 | DO 内のロジックから |

### 2. REST API (HTTP) — Worker を介さない外部呼び出し

```sh
POST https://api.cloudflare.com/client/v4/accounts/{account_id}/workflows/{workflow_name}/instances
```

API Token で認証して直接 `instances` リソースに POST する。外部システム (GitHub Actions、AWS Lambda、自社の Backend サーバなど) から Cloudflare Workflows を起動するときに使う経路。

### 3. Wrangler CLI — 手動オペレーション

```sh
npx wrangler workflows trigger image-processing '{"imageKeys":["a.jpg"],"autoApproveThreshold":0.7}'
```

CLI から直接 Workflow をトリガーできる。デバッグや運用時の手動起動、`--id` で固有 ID を渡せばリトライ運用にも使える。

★ Insight ─────────────────────────────────────
- **「Worker は管理面」** という見方が正しい — Workflow class 自体は Worker script に同梱されるが、**起動するだけ** なら REST API や CLI で十分。「Workflow を `class_name` として保持する Worker」と「Workflow を起動する手段」は別の話
- 今回のリポジトリの `image-processing-workflow` Worker は **fetch handler 経由の起動口を提供** しているが、これを消しても `wrangler workflows trigger image-processing ...` で外部から起動可能。バウンドワーカーは **class の置き場として必須** だが、**起動経路としては必須ではない**
- 設計上の含意: バックエンドが他社クラウド (AWS / GCP) にあって「処理だけ Cloudflare の durable 実行に流したい」場合、Worker の fetch handler を作らず **REST API で直接 instances を作る** 構成もあり得る。逆に「外部から叩かれたくない、Workers AI / R2 / Queue と密結合」なら Worker handler 経由が自然 […]

> DEVELOPER

Worker 経由ならばEmailトリガーとかで起動できる？

> AGENT

確認します。

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01JFhWv5YbUcPuuPDaLZhzGD
```json
{
  "query": "Email Worker email handler routing trigger from incoming message handler bindings"
}
```

> TOOL

tool_use mcp__plugin_cloudflare_cloudflare-bindings__search_cloudflare_documentation
id: toolu_01N42fkkPo3sEjCddLyBtuDp
```json
{
  "query": "Email Worker trigger Workflow from email handler bindings call workflow create"
}
```

> TOOL

tool_result
id: toolu_01JFhWv5YbUcPuuPDaLZhzGD
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/email-routing/email-workers/edit-email-workers/</url>
<title></title>
<text>
## Add an Email worker

1. In the Cloudflare dashboard, go to the **Email Routing** page.  
[ Go to **Email Routing** ](https://dash.cloudflare.com/?to=/:account/:zone/email/routing)
2. Select **Email Workers**.
3. Select **Create**.
1. (Optional) Enter a descriptive Email Worker name in **Create a worker name**.
2. In **Select a starter**, select the starter template that best suits your needs. You can also start from scratch and build your own Email Worker with **Create my own**. After choosing your template, select **Create**.
3. Now, configure your code on the left side of the screen. For example, if you are creating an Email Worker from the Allowlist template:  
   1. In `const allow = ["friend@example.com", "coworker@example.com"];` replace the email examples with the addresses you want to allow emails from.  
   2. In `await message.forward("inbox@corp");` replace the email address example with the address where emails should be forwarded to.
4. (Optional) You can test your logic on the right side of the screen. In the **From** field, enter either an email address from your approved senders list or one that is not on the approved list. When you select **Trigger email event** you should see a message telling you if […]

> TOOL

tool_result
id: toolu_01N42fkkPo3sEjCddLyBtuDp
```
<result>
<url>https://developers.cloudflare.com/https://developers.cloudflare.com/workflows/build/trigger-workflows/</url>
<title></title>
<text>
---
title: Trigger Workflows
description: Trigger Workflows from Workers bindings, the REST API, or the Wrangler CLI.
image: https://developers.cloudflare.com/dev-products-preview.png
---

> Documentation Index  
> Fetch the complete documentation index at: https://developers.cloudflare.com/workflows/llms.txt  
> Use this file to discover all available pages before exploring further.

[Skip to content](#%5Ftop) 

### Tags

[ Bindings ](/search/?tags=Bindings) 

# Trigger Workflows

You can trigger Workflows both programmatically and via the Workflows APIs, including:

1. With [Workers](/workers) via HTTP requests in a `fetch` handler, or bindings from a `queue` or `scheduled` handler
2. Using the [Workflows REST API](/api/resources/workflows/methods/list/)
3. Via the [wrangler CLI](/workers/wrangler/commands/workflows/#workflows) in your terminal

## Workers API (Bindings)

You can interact with Workflows programmatically from any Worker script by creating a binding to a Workflow. A Worker can bind to multiple Workflows, including Workflows defined in other Workers projects (scripts) within your account.

You can interact with a Workflow:


## Workers API (Bindings)

You can interact with Workflows programmatically from any Worker script by creating a binding to a Workflow. A Worker can bind to multiple Workflows, including Workflows defined in other Workers projects (scripts) within your account.

You can interact with a Workflow:

* Directly over HTTP […]

> AGENT

できます。Worker には `email()` handler があり、その中から Workflow binding を呼べます。

## `email()` handler の構造

```typescript
interface Env {
  MY_WORKFLOW: Workflow;
}

export default {
  async email(message, env, ctx): Promise<void> {
    // メールから抽出
    const from = message.from;
    const subject = message.headers.get("subject");
    const raw = new Response(message.raw);
    const body = await raw.arrayBuffer();

    // Workflow を起動 (fire-and-forget)
    const instance = await env.MY_WORKFLOW.create({
      id: message.headers.get("message-id") ?? crypto.randomUUID(),
      params: { from, subject, body },
    });

    // 必要なら forward / reject も併用可
    await message.forward("archive@example.com");
  },
} satisfies ExportedHandler<Env>;
```

`fetch` / `queue` / `scheduled` と同じ handler 一族で、`message` (= `ForwardableEmailMessage`) を受け取る点だけ違います。

★ Insight ─────────────────────────────────────
- **docs の trigger-workflows ページには `email()` handler が明示列挙されていない** (fetch / queue / scheduled / Durable Object の 4 つだけ書かれてる) が、これは網羅の手抜きで、原理的に **どの Worker handler からも Workflow binding を呼べる**。`email()` も Worker handler の一種なので例外ではない
- **冪等な ID として `message-id`** を渡せるのが Email トリガーの隠れた強み。SMTP の `Message-ID` ヘッダはメール 1 通につき一意なので、`MY_WORKFLOW.create({ id: messageId, ... })` とすると **同じメールが二度配送されても Workflow が二重起動しない** (create は ID 重複で失敗する)。`fetch` トリガーだと自前で冪等キーを作る必要があるが、Email は無料で手に入る
- **Email Routing の route 設定が前提**: Cloudflare ダッシュボードで `support@your-zone.com → このWorker` のような route を切ること、ゾーン側で MX レコードが Cloudflare に向いていることが必要。Workers AI や R2 などの他バインディングと違って **zone レベルの設定** が要る点だけ注意
─────────────────────────────────────────────────

## 典型ユースケース (durable な Email pipeline)

`email()` handler 自体は Worker の通常制限 (CPU 数十 ms 程度) があるので、**重い処理は Workflow に丸投げ** するのが定石です:

| パターン […]

> DEVELOPER

containerとworkflow no