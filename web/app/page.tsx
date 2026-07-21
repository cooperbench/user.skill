// UserBench — leaderboard + dataset + analysis (results merged into this page).
// Data: app/v2data.json (computed from Entire / GitHub crawl / DataClaw full-trace sources).
import data from "./v2data.json";
import {
  AnalysisSection,
  DatasetHubLinks,
  LabelExamplesSection,
  LeaderboardSection,
  MethodsSection,
  RunDetailsSection,
} from "./SolHighResults";

const EVAL_DEVS = 62;
const EVAL_TASKS = 620;

const fmt = (n: number) => n.toLocaleString("en-US");
const pct = (a: number, b: number) => (b ? (100 * a) / b : 0);

type Split = { mean: number; median: number };

function StatCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white px-5 py-4">
      <div className="text-3xl font-semibold tracking-tight text-zinc-900">{value}</div>
      <div className="mt-1 text-sm font-medium text-zinc-600">{label}</div>
      {sub && <div className="mt-0.5 text-xs text-zinc-400">{sub}</div>}
    </div>
  );
}

// horizontal bar list
function Bars({
  rows,
  max,
  fmtVal = fmt,
}: {
  rows: { label: string; value: number; color?: string; note?: string }[];
  max?: number;
  fmtVal?: (n: number) => string;
}) {
  const m = max ?? Math.max(...rows.map((r) => r.value), 1);
  return (
    <div className="space-y-1.5">
      {rows.map((r) => (
        <div key={r.label} className="flex items-center gap-3">
          <div className="w-40 shrink-0 text-right text-xs text-zinc-500">{r.label}</div>
          <div className="relative h-6 flex-1 rounded bg-zinc-100">
            <div
              className={`h-6 rounded ${r.color ?? "bg-indigo-400"}`}
              style={{ width: `${Math.max(pct(r.value, m), 1.5)}%` }}
            />
            <div className="absolute inset-y-0 left-2 flex items-center text-xs font-medium text-zinc-700">
              {fmtVal(r.value)}
              {r.note && <span className="ml-1 text-zinc-400">{r.note}</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function Section({ title, kicker, children }: { title: string; kicker?: string; children: React.ReactNode }) {
  return (
    <section className="mt-12">
      {kicker && <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">{kicker}</div>}
      <h2 className="mt-1 text-xl font-semibold tracking-tight text-zinc-900">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function CompactHistogram({
  title,
  subtitle,
  labels,
  counts,
  color,
  takeaway,
  ariaLabel,
}: {
  title: string;
  subtitle: string;
  labels: string[];
  counts: number[];
  color: string;
  takeaway: string;
  ariaLabel: string;
}) {
  const max = Math.max(...counts);
  return (
    <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
      <figcaption className="font-semibold text-zinc-900">{title}</figcaption>
      <p className="mt-1 text-xs text-zinc-500">{subtitle}</p>
      <div
        className="mt-5 grid h-24 items-end gap-1"
        style={{ gridTemplateColumns: `repeat(${counts.length}, minmax(0, 1fr))` }}
        role="img"
        aria-label={ariaLabel}
      >
        {counts.map((count, index) => (
          <div key={labels[index]} className="flex h-full items-end">
            <div
              className={`w-full rounded-t ${color}`}
              style={{ height: `${(count / max) * 100}%` }}
            />
          </div>
        ))}
      </div>
      <div
        className="mt-1 grid gap-1 text-center text-[9px] text-zinc-400"
        style={{ gridTemplateColumns: `repeat(${counts.length}, minmax(0, 1fr))` }}
      >
        {labels.map((label) => (
          <span key={label}>{label}</span>
        ))}
      </div>
      <p className="mt-4 text-sm leading-6 text-zinc-600">{takeaway}</p>
    </figure>
  );
}

function ContextTokenChart() {
  const max = 1_500_000;
  const position = (value: number) =>
    `${(Math.log10(value) / Math.log10(max)) * 100}%`;
  const markers = [
    { label: "Median", short: "4.2k", value: 4_214, color: "bg-indigo-600" },
    { label: "Mean", short: "23.4k", value: 23_399, color: "bg-sky-600" },
    { label: "P90", short: "25.3k", value: 25_342, color: "bg-violet-600" },
    { label: "Max", short: "1.34m", value: 1_344_149, color: "bg-zinc-900" },
  ] as const;

  return (
    <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
      <figcaption className="font-semibold text-zinc-900">
        Context available before each prediction
      </figcaption>
      <div className="flex items-center justify-between gap-4 text-xs text-zinc-500">
        <span>Tokens in the published history file</span>
        <span>log scale</span>
      </div>
      <div
        className="relative mt-6 h-14"
        role="img"
        aria-label="Prior context tokens per published task on a log scale: median 4,214, mean 23,399, 90th percentile 25,342, maximum 1,344,149"
      >
        <div className="absolute inset-x-0 top-7 h-1 rounded-full bg-zinc-200" />
        {markers.map((marker) => (
          <span
            key={marker.label}
            className="absolute top-3 -translate-x-1/2"
            style={{ left: position(marker.value) }}
            aria-hidden="true"
          >
            <span className={`block h-8 w-1 rounded-full ${marker.color}`} />
          </span>
        ))}
        <span className="absolute left-0 top-10 text-[10px] text-zinc-400">1</span>
        <span className="absolute left-[32.4%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">100</span>
        <span className="absolute left-[64.8%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">10k</span>
        <span className="absolute left-[97.2%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">1m</span>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {markers.map((marker) => (
          <div key={marker.label}>
            <p className="text-xl font-semibold tabular-nums text-zinc-950">
              {marker.short}
            </p>
            <p className="text-xs text-zinc-500">{marker.label}</p>
          </div>
        ))}
      </div>
      <p className="mt-5 text-sm leading-6 text-zinc-600">
        The distribution has a long tail, but the median published task has
        4.2k tokens of prior context.
      </p>
    </figure>
  );
}

export default function V2Page() {
  const s = data.summary;
  const h = data.harness as Record<string, { sessions: number; user_turns: number }>;
  const cc = h["claude-code"];
  const cx = h["codex"];
  const totTurns = cc.user_turns + cx.user_turns;
  const totSess = cc.sessions + cx.sessions;

  const months = data.months as Record<string, number>;
  const monthRows = Object.entries(months).map(([label, value]) => ({ label, value }));
  const monthMax = Math.max(...monthRows.map((r) => r.value), 1);

  const d = data.dist;

  const r0 = (n: number) => fmt(Math.round(n));
  const distRow = (name: string, o: { train: Split; eval: Split; total?: Split }) => (
    <tr className="border-t border-zinc-100">
      <td className="py-2 pr-4 font-medium text-zinc-700">{name}</td>
      <td className="py-2 pr-4 tabular-nums text-zinc-600">{r0(o.train.mean)} <span className="text-zinc-400">/ {r0(o.train.median)}</span></td>
      <td className="py-2 pr-4 tabular-nums text-zinc-600">{r0(o.eval.mean)} <span className="text-zinc-400">/ {r0(o.eval.median)}</span></td>
      <td className="py-2 tabular-nums text-zinc-600">{o.total ? <>{r0(o.total.mean)} <span className="text-zinc-400">/ {r0(o.total.median)}</span></> : "—"}</td>
    </tr>
  );

  return (
    <main className="mx-auto max-w-5xl px-5 pb-16 pt-8 sm:px-8">
      <nav aria-label="Main navigation" className="flex flex-wrap items-center justify-between gap-4 text-sm">
        <a href="/" className="font-semibold tracking-tight text-zinc-950">UserBench</a>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-zinc-500">
          <span aria-current="page" className="font-medium text-zinc-950">Dataset</span>
          <a href="/annotator/dashboard" className="hover:text-zinc-950">Annotator</a>
          <a href="/v1" className="hover:text-zinc-950">Old leaderboard</a>
        </div>
      </nav>

      <LeaderboardSection />

      <section id="dataset" className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12">
        <div className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
          Dataset
        </div>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950">
          Real developers, later turns held out
        </h2>
        <p className="mt-3 max-w-3xl text-base leading-7 text-zinc-600">
          UserBench uses full Claude Code and Codex session traces. Each
          developer&apos;s training sessions come before every held-out
          session, so the model sees past behavior without seeing the answer.
        </p>

        <div className="mt-7 grid gap-3 sm:grid-cols-3">
          <StatCard label="developers" value={fmt(EVAL_DEVS)} sub="real coding-agent users" />
          <StatCard label="held-out tasks" value={fmt(EVAL_TASKS)} sub="one held-out turn each · 10 per developer" />
          <StatCard label="training turns" value="24,800" sub="400 per developer × 62 developers" />
        </div>
        <DatasetHubLinks />
      </section>

      <section
        aria-labelledby="dataset-depth-title"
        className="mt-16 border-t border-zinc-200 pt-12"
      >
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
          Dataset details
        </p>
        <h2
          id="dataset-depth-title"
          className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Explore the dataset in depth
        </h2>
        <div className="pb-4">
      <Section kicker="where it comes from" title="Data provenance">
        {(() => {
          const p = data.provenance;
          const merge = (o: Record<string, number>) => {
            const m = { ...o } as Record<string, number>;
            if (m["other"]) { m["GitHub .claude/.codex crawl"] = (m["GitHub .claude/.codex crawl"] ?? 0) + m["other"]; delete m["other"]; }
            return m;
          };
          const users = merge(p.users_by_dominant as Record<string, number>);
          const sess = merge(p.sessions_by_source as Record<string, number>);
          const turns = merge(p.turns_by_source as Record<string, number>);
          const meta: Record<string, { color: string; how: string }> = {
            "Entire checkpoints": { color: "bg-violet-400", how: "Entire CLI pushes each agent session to an entire/checkpoints branch; discovered via GH-Archive push events, harvested by cloning the branch. SWE-chat (the packaged HF parquet of the same stream) is merged and deduped by session id." },
            "GitHub .claude/.codex crawl": { color: "bg-teal-400", how: "developers who committed their ~/.claude/projects or .codex/sessions dumps to public repos; found by tree-probing ~4,600 candidate repos for session-dense trees, harvested with preserved sparse clones." },
            "DataClaw (HF donors)": { color: "bg-amber-400", how: "per-donor conversations.jsonl on HuggingFace; filtered to Claude / Codex sessions only." },
          };
          const order = ["Entire checkpoints", "GitHub .claude/.codex crawl", "DataClaw (HF donors)"];
          const tot = (o: Record<string, number>) => Object.values(o).reduce((a, b) => a + b, 0);
          return (
            <div className="space-y-4">
              {order.map((k) => (
                <div key={k} className="rounded-xl border border-zinc-200 bg-white p-4">
                  <div className="flex flex-wrap items-baseline justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className={`inline-block h-3 w-3 rounded-sm ${meta[k].color}`} />
                      <span className="font-medium text-zinc-800">{k}</span>
                    </div>
                    <div className="flex gap-4 text-sm tabular-nums text-zinc-600">
                      <span><strong>{fmt(users[k] ?? 0)}</strong> devs</span>
                      <span><strong>{fmt(sess[k] ?? 0)}</strong> sessions</span>
                      <span><strong>{fmt(turns[k] ?? 0)}</strong> user turns</span>
                    </div>
                  </div>
                  {/* proportion bars */}
                  <div className="mt-2 flex gap-3 text-[11px] text-zinc-400">
                    <div className="flex-1">
                      <div className="mb-0.5">sessions</div>
                      <div className="h-2 rounded bg-zinc-100"><div className={`h-2 rounded ${meta[k].color}`} style={{ width: `${pct(sess[k] ?? 0, tot(sess))}%` }} /></div>
                    </div>
                    <div className="flex-1">
                      <div className="mb-0.5">user turns</div>
                      <div className="h-2 rounded bg-zinc-100"><div className={`h-2 rounded ${meta[k].color}`} style={{ width: `${pct(turns[k] ?? 0, tot(turns))}%` }} /></div>
                    </div>
                  </div>
                  <p className="mt-2 text-xs text-zinc-500">{meta[k].how}</p>
                </div>
              ))}
            </div>
          );
        })()}
        <p className="mt-3 text-sm text-zinc-500">
          Three full-trace Claude Code / Codex sources, one shared native-JSONL parser. The crawl
          contributes the most <em>sessions</em> (many shallow committed dumps); Entire and DataClaw are
          turn-denser. Lossy IDE-markdown (SpecStory) and non-CC/Codex agents (pi, Cursor, WildChat) are
          excluded. Every session id is deduped across sources, and the train/held split is
          leakage-verified.
        </p>
      </Section>

      <details className="mt-12 rounded-2xl border border-zinc-200 bg-white">
        <summary className="cursor-pointer px-5 py-4 font-semibold text-zinc-900">
          Source breakdown
        </summary>
        <div className="border-t border-zinc-100 px-5 py-5">
        {(() => {
          const sc = data.source_compare as Record<string, Record<string, string | number>>;
          const cols = ["Entire checkpoints", "GitHub .claude/.codex crawl", "DataClaw"];
          const short: Record<string, string> = { "Entire checkpoints": "Entire", "GitHub .claude/.codex crawl": "GitHub crawl", DataClaw: "DataClaw" };
          const order = ["developers (dominant)", "sessions", "user turns", "assistant turns",
            "user turns / session (mean)", "user turns / session (median)", "assistant / user turn",
            "tokens/user turn (median)", "tokens/user turn (mean)", "Claude Code % of turns",
            "Codex % of turns", "train:eval turn %", "time span"];
          const num = (x: string | number) => (typeof x === "number" ? fmt(x) : x);
          return (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs uppercase tracking-wide text-zinc-400">
                    <th className="pb-2 pr-4 font-medium">metric</th>
                    {cols.map((c) => <th key={c} className="pb-2 pr-4 text-right font-medium">{short[c]}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {order.map((m) => (
                    <tr key={m} className="border-t border-zinc-100">
                      <td className="py-1.5 pr-4 text-zinc-600">{m}</td>
                      {cols.map((c) => (
                        <td key={c} className="py-1.5 pr-4 text-right tabular-nums text-zinc-800">{num(sc[m]?.[c])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        })()}
        <p className="mt-3 text-sm text-zinc-500">
          Entire skews toward deeper sessions, the GitHub crawl toward short
          sessions, and DataClaw toward Codex.
        </p>
        </div>
      </details>

      <Section kicker="agent harness" title="Claude Code vs Codex">
        <div className="grid gap-6 sm:grid-cols-2">
          <div>
            <div className="mb-2 text-sm text-zinc-500">by user turns</div>
            <Bars
              rows={[
                { label: "Claude Code", value: cc.user_turns, color: "bg-orange-400", note: `${pct(cc.user_turns, totTurns).toFixed(0)}%` },
                { label: "Codex", value: cx.user_turns, color: "bg-sky-500", note: `${pct(cx.user_turns, totTurns).toFixed(0)}%` },
              ]}
            />
          </div>
          <div>
            <div className="mb-2 text-sm text-zinc-500">by sessions</div>
            <Bars
              rows={[
                { label: "Claude Code", value: cc.sessions, color: "bg-orange-400", note: `${pct(cc.sessions, totSess).toFixed(0)}%` },
                { label: "Codex", value: cx.sessions, color: "bg-sky-500", note: `${pct(cx.sessions, totSess).toFixed(0)}%` },
              ]}
            />
          </div>
        </div>
        <p className="mt-3 text-sm text-zinc-500">
          Claude Code dominates (~81% of user turns). Codex sessions are far more tool-dense
          (~320 tool/shell calls per session vs ~63 for Claude Code), reflecting Codex's
          many-small-commands style.
        </p>
      </Section>

      <details className="mt-12 rounded-2xl border border-zinc-200 bg-white">
        <summary className="cursor-pointer px-5 py-4 font-semibold text-zinc-900">
          Train/eval split
        </summary>
        <div className="border-t border-zinc-100 px-5 py-5">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-zinc-400">
                <th className="pb-2 pr-4 font-medium">per developer (mean / median)</th>
                <th className="pb-2 pr-4 font-medium">train</th>
                <th className="pb-2 pr-4 font-medium">held-out (eval)</th>
                <th className="pb-2 font-medium">total</th>
              </tr>
            </thead>
            <tbody>
              {distRow("sessions", d.sessions)}
              {distRow("user turns", d.user_turns)}
              {distRow("assistant turns", d.asst_turns)}
              {distRow("user turns / session", d.turns_per_sess)}
            </tbody>
          </table>
        </div>
        <p className="mt-3 text-sm text-zinc-500">
          The split is deliberately train-heavy: ~92% of user turns and ~95% of sessions are training
          material (rich developer profiles), with a lean-but-sufficient held-out tail (median 11 sessions
          / 108 user turns) that just clears the ≥100 floor.
        </p>
        </div>
      </details>

      <Section kicker="prediction context" title="What the model sees and predicts">
        <p className="mb-6 max-w-3xl text-sm leading-6 text-zinc-600">
          These figures come from the 620 published tasks: conversation turns
          count the history, context tokens measure its size, and next-message
          tokens measure the held-out text to predict.
        </p>
        <div className="grid gap-4 lg:grid-cols-3">
          <CompactHistogram
            title="Conversation history before each prediction"
            subtitle="Previous turns before the held-out message"
            labels={["0–4", "5–9", "10–19", "20–39", "40–79", "80–159", "160+"]}
            counts={[83, 74, 96, 119, 136, 55, 57]}
            color="bg-fuchsia-400"
            takeaway="Median depth is 28 prior turns."
            ariaLabel="Previous turns across 620 published tasks: 83 have 0 to 4, 74 have 5 to 9, 96 have 10 to 19, 119 have 20 to 39, 136 have 40 to 79, 55 have 80 to 159, and 57 have 160 or more"
          />
          <ContextTokenChart />
          <CompactHistogram
            title="Length of the developer’s next message"
            subtitle="Tokens in the held-out message"
            labels={["1–9", "10–24", "25–49", "50–99", "100–249", "250+"]}
            counts={[231, 171, 128, 48, 29, 13]}
            color="bg-emerald-500"
            takeaway="Median length is 15 tokens, with a long tail from logs and pasted text."
            ariaLabel="Next-message token lengths across 620 published tasks: 231 have 1 to 9, 171 have 10 to 24, 128 have 25 to 49, 48 have 50 to 99, 29 have 100 to 249, and 13 have 250 or more"
          />
        </div>
      </Section>

      {(data.versions?.cc_total || data.versions?.cx_total) ? (
      <Section kicker="harness versions" title="Which Claude Code / Codex versions, over time">
        {(() => {
          const v = data.versions;
          const ccM = v.cc_by_month as Record<string, { n: number; modal: string }>;
          const cxM = v.cx_by_month as Record<string, { n: number; modal: string }>;
          const months = Array.from(new Set([...Object.keys(ccM), ...Object.keys(cxM)]))
            .filter((m) => m >= "2025-06" && m <= "2026-07")
            .sort();
          const ccMax = Math.max(...months.map((m) => ccM[m]?.n ?? 0), 1);
          const cxMax = Math.max(...months.map((m) => cxM[m]?.n ?? 0), 1);
          const ccColor = (mod: string) =>
            mod.startsWith("2.1") ? "bg-orange-500" : mod.startsWith("2.0") ? "bg-orange-300" : mod.startsWith("1.") ? "bg-amber-200" : "bg-zinc-200";
          const Cell = ({ mod, n, max, color }: { mod?: string; n: number; max: number; color: string }) => (
            <div className="flex flex-col items-center gap-1">
              <div className="text-[10px] font-medium tabular-nums text-zinc-600">{mod ?? "–"}</div>
              <div className="h-10 w-full self-stretch overflow-hidden rounded bg-zinc-100">
                {mod && <div className={color} style={{ height: "100%", opacity: 0.35 + 0.65 * (n / max) }} />}
              </div>
            </div>
          );
          const cols = `56px repeat(${months.length}, minmax(46px, 1fr))`;
          return (
            <div className="overflow-x-auto">
              <div className="grid items-center gap-1.5" style={{ gridTemplateColumns: cols }}>
                {/* month header */}
                <div />
                {months.map((m) => (
                  <div key={m} className="text-center text-[10px] text-zinc-400">{m.slice(2)}</div>
                ))}
                {/* Claude Code row */}
                <div className="pr-1 text-right text-xs font-semibold text-orange-600">Claude<br />Code</div>
                {months.map((m) => (
                  <Cell key={m} mod={ccM[m]?.modal} n={ccM[m]?.n ?? 0} max={ccMax} color={ccColor(ccM[m]?.modal ?? "")} />
                ))}
                {/* Codex row */}
                <div className="pr-1 text-right text-xs font-semibold text-sky-600">Codex</div>
                {months.map((m) => (
                  <Cell key={m} mod={cxM[m]?.modal?.replace(/-.*/, "")} n={cxM[m]?.n ?? 0} max={cxMax} color="bg-sky-500" />
                ))}
              </div>
              <div className="mt-2 text-[11px] text-zinc-400">
                modal (most-common) CLI version per month · bar shade ∝ session volume that month
              </div>
            </div>
          );
        })()}
        <p className="mt-3 text-sm text-zinc-500">
          Over the Feb–Jul 2026 window both harnesses march cleanly up their release lines. Claude Code
          stays on the <strong>2.1.x</strong> series throughout, climbing month over month from{" "}
          <strong>2.1.62</strong> to <strong>2.1.198</strong>; Codex climbs <strong>~0.104 → 0.142</strong>.
          Versions come from the raw traces and cover current Opus-4.6-era releases.
        </p>
      </Section>
      ) : null}

      <Section kicker="recency" title="Sessions over time">
        <Bars rows={monthRows} max={monthMax} />
        <p className="mt-3 text-sm text-zinc-500">
          {s.time_min} → {s.time_max}, concentrated in early–mid 2026 as coding-agent adoption grew.
        </p>
      </Section>

        </div>
      </section>

      <LabelExamplesSection />
      <MethodsSection />
      <AnalysisSection />
      <RunDetailsSection />

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        UserBench · {EVAL_DEVS} eval developers · {fmt(EVAL_TASKS)} Hub tasks · Claude Code + Codex full
        traces · Opus 4.6 era (≥2026-02-05) · leakage-verified train/held-out split. See{" "}
        <a href="#leaderboard" className="text-zinc-600 hover:text-zinc-900">leaderboard</a>
        ,{" "}
        <a href="/annotator/dashboard" className="text-zinc-600 hover:text-zinc-900">annotator</a>
        , and the{" "}
        <a href="/v1" className="text-zinc-600 hover:text-zinc-900">old leaderboard</a>.
      </footer>
    </main>
  );
}
