import type { Metadata } from "next";
import blobs from "./blobs.json";

export const metadata: Metadata = {
  title: "Data: SWESimBench trial results",
  description: "Download the raw experiment data behind the accuracy results. Public, for readers and their agents.",
};

function human(b: number) {
  return b > 1e6 ? `${(b / 1e6).toFixed(1)} MB` : b > 1e3 ? `${(b / 1e3).toFixed(0)} KB` : `${b} B`;
}

export default function DataPage() {
  const { index, files, models } = blobs as { index: string; files: { name: string; url: string; bytes: number; description: string }[]; models: string[] };
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-3">
          <h1 className="text-sm font-semibold tracking-tight"><a href="/" className="hover:text-zinc-600">SWESimBench</a> · <span className="text-zinc-400">Data</span></h1>
          <div className="flex items-center gap-3 text-xs text-zinc-500">
            <a href="/" className="hover:text-zinc-900">results</a>
            <a href="https://github.com/AlienKevin/user-simulator" target="_blank" rel="noreferrer" className="hover:text-zinc-900">github</a>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 pb-20">
        <div className="py-10">
          <div className="font-mono text-[11px] uppercase tracking-wider text-zinc-400">download</div>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-900">Trial results: public, agent-readable</h2>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-zinc-700">
            Every artifact behind the <a href="/" className="text-blue-700 underline-offset-2 hover:underline">accuracy results</a> is
            here: the 7 leaderboard simulators × ±profile on a 20-developer, user- and repo-disjoint SWE-chat test split (the raw files also include 3 off-leaderboard runs: 2 DeepSeek variants and gemini-3.1-pro, which gemini-3.5-flash replaced on the leaderboard; 10 model conditions in total). Files are public on
            Vercel Blob. Point your agent at the machine-readable index, or download files directly below.
          </p>
        </div>

        {/* AGENT ENTRY POINT */}
        <section className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 font-mono text-[11px] leading-relaxed text-zinc-300">
          <div className="mb-2 text-[10px] uppercase tracking-wider text-zinc-500">for an agent: start here</div>
          <div className="text-zinc-400"># machine-readable catalog (lists every file + schema):</div>
          <div className="break-all text-emerald-300">{index}</div>
          <pre className="mt-3 whitespace-pre-wrap text-zinc-300">{`curl -s ${index} | jq .            # the catalog
curl -s ${files.find((f) => f.name === "summary.json")?.url}   # headline accuracy results
curl -s ${files.find((f) => f.name === "raw.jsonl")?.url} \\   # every generation + move label (NDJSON)
  | head -1 | jq .`}</pre>
        </section>

        {/* FILE TABLE */}
        <section className="mt-6 overflow-hidden rounded-lg border border-zinc-200">
          <table className="w-full text-sm">
            <thead><tr className="bg-zinc-50 text-left text-xs text-zinc-500">
              <th className="px-3 py-2 font-medium">File</th>
              <th className="px-3 py-2 font-medium">What it is</th>
              <th className="px-3 py-2 text-right font-medium">Size</th>
            </tr></thead>
            <tbody>
              {files.map((f) => (
                <tr key={f.name} className="border-t border-zinc-100 align-top">
                  <td className="px-3 py-2 whitespace-nowrap"><a href={f.url} className="font-mono text-xs text-blue-700 hover:underline">{f.name}</a></td>
                  <td className="px-3 py-2 text-xs text-zinc-600">{f.description}</td>
                  <td className="px-3 py-2 text-right font-mono text-xs text-zinc-500">{human(f.bytes)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* SCHEMA / WHAT'S IN IT */}
        <section className="mt-6 grid gap-3 md:grid-cols-2">
          <div className="rounded-lg border border-zinc-200 bg-white p-4">
            <h3 className="font-mono text-sm font-semibold text-zinc-900">raw.jsonl: every trial</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-zinc-600">
              NDJSON. Two record types. <span className="font-mono">gen</span>:{" "}
              <span className="font-mono text-zinc-700">{`{key, kind:"gen", point_id, slug, model, model_id, backend, effort, cond, text, ts, seed?}`}</span>.
              {" "}Move label: <span className="font-mono text-zinc-700">{`{key:"lab:haiku:<hash>", move}`}</span>. The label hash is over
              the (prev_agent, message) pair, so labels are shared across identical messages.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-200 bg-white p-4">
            <h3 className="font-mono text-sm font-semibold text-zinc-900">points.jsonl: the test set</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-zinc-600">
              The 480 frozen held-out moments:{" "}
              <span className="font-mono text-zinc-700">{`{point_id, slug, repo, turn_index, prev_agent, real_text}`}</span>.
              Each is one real developer turn the simulators had to predict, with the agent’s prior turn held fixed.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-200 bg-white p-4">
            <h3 className="font-mono text-sm font-semibold text-zinc-900">summary.json: results</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-zinc-600">
              Per <span className="font-mono">model/condition</span>: accuracy macro mean + 95% CI + the 20 per-developer values, plus
              the <span className="font-mono">lucky_guess</span> line and the real move distribution. Models:{" "}
              <span className="text-zinc-700">{models.join(", ")}</span>.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-200 bg-white p-4">
            <h3 className="font-mono text-sm font-semibold text-zinc-900">manifest · splits · taxonomy</h3>
            <p className="mt-1.5 text-xs leading-relaxed text-zinc-600">
              <span className="font-mono">manifest.json</span>: full config (models, OpenRouter ids, reasoning efforts, concurrency, git
              sha). <span className="font-mono">splits.json</span>: the user- and repo-disjoint train/val/test split.{" "}
              <span className="font-mono">taxonomy.json</span>: the 4-way move taxonomy + classifier prompt + inter-judge κ.
            </p>
          </div>
        </section>

        <section className="mt-6 border-t border-zinc-200 pt-6">
          <h3 className="mb-2 text-sm font-semibold text-zinc-900">Where everything lives</h3>
          <ul className="max-w-3xl space-y-1.5 text-xs leading-relaxed text-zinc-500">
            <li>
              <span className="font-semibold text-zinc-600">Website:</span> this site, open source at{" "}
              <a href="https://github.com/AlienKevin/user-simulator" className="text-blue-700 hover:underline">github.com/AlienKevin/user-simulator</a>{" "}
              (a Next.js static export under <span className="font-mono">web/</span>).
            </li>
            <li>
              <span className="font-semibold text-zinc-600">Benchmark code:</span> the eval harness, the 4-way move taxonomy + judge, the
              analysis and ablation scripts, and the Modal serving for the OSim models. Kept in a private repo
              (<span className="font-mono">AlienKevin/user.skill</span>, <span className="font-mono">swesimbench</span> branch); available on request.
            </li>
            <li>
              <span className="font-semibold text-zinc-600">Data:</span> everything on this page, public on Vercel Blob: the files above plus
              the machine-readable index.
            </li>
          </ul>
          <p className="mt-3 max-w-3xl text-xs leading-relaxed text-zinc-500">
            Prompts are reconstructable from <span className="font-mono">points.jsonl</span> + each developer’s{" "}
            <span className="font-mono">users/&lt;slug&gt;/</span> folder at <span className="font-mono">manifest.git_sha</span> via{" "}
            <span className="font-mono">validate.build_prompt</span> / <span className="font-mono">osim_backend.build_osim_messages</span>. Data
            derives from public <a href="https://huggingface.co/datasets/SALT-NLP/SWE-chat" className="text-blue-700 hover:underline">SWE-chat</a> (ODC-BY).
          </p>
        </section>

        <footer className="mt-8 border-t border-zinc-200 pt-6 text-xs text-zinc-400">
          SWESimBench · <a href="/" className="hover:text-zinc-700">results</a> · data on Vercel Blob (public).
        </footer>
      </main>
    </div>
  );
}
