import React from "react";
// SWESimBench — misprediction / homogeneity study.
// Data: ./data.json (regenerated via scripts/misprediction.py -> a compact export).
// Question: are the user-simulator's mispredictions a failure of *individuation* — does it
// default to task-completion and give every developer the same move-mix?
import data from "./data.json";

const CATS = ["approve", "critical", "directive", "inquiry"] as const;
const n3 = (n: number | null | undefined) => (typeof n === "number" ? n.toFixed(3) : "—");
const n1 = (n: number | null | undefined) => (typeof n === "number" ? n.toFixed(1) : "—");
const fmt = (n: number) => n.toLocaleString("en-US");

const VERDICT_CLS: Record<string, string> = {
  supported: "bg-emerald-100 text-emerald-700",
  refuted: "bg-rose-100 text-rose-700",
  mixed: "bg-amber-100 text-amber-700",
  "not run": "bg-zinc-100 text-zinc-500",
};

const CAT_COLOR: Record<string, string> = {
  approve: "text-emerald-600 bg-emerald-50",
  critical: "text-rose-600 bg-rose-50",
  directive: "text-indigo-600 bg-indigo-50",
  inquiry: "text-sky-600 bg-sky-50",
};

function Chip({ cat }: { cat: string }) {
  return (
    <span className={`inline-block rounded px-1.5 text-[10px] font-bold uppercase tracking-wide ${CAT_COLOR[cat] ?? "bg-zinc-100 text-zinc-500"}`}>
      {cat}
    </span>
  );
}

function StatCard({ label, value, sub }: { label: string; value: React.ReactNode; sub?: string }) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white px-5 py-4">
      <div className="text-2xl font-semibold tracking-tight text-zinc-900">{value}</div>
      <div className="mt-1 text-sm font-medium text-zinc-600">{label}</div>
      {sub && <div className="mt-0.5 text-xs text-zinc-400">{sub}</div>}
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

// horizontal bars, matching app/page.tsx
function Bars({ rows, max }: { rows: { label: string; value: number; color?: string; note?: string }[]; max: number }) {
  return (
    <div className="space-y-1.5">
      {rows.map((r) => (
        <div key={r.label} className="flex items-center gap-3">
          <div className="w-44 shrink-0 text-right text-xs text-zinc-500">{r.label}</div>
          <div className="relative h-6 flex-1 rounded bg-zinc-100">
            <div className={`h-6 rounded ${r.color ?? "bg-indigo-400"}`} style={{ width: `${Math.max((100 * r.value) / max, 1.5)}%` }} />
            <div className="absolute inset-y-0 left-2 flex items-center text-xs font-medium text-zinc-700">
              {r.value.toFixed(3)}
              {r.note && <span className="ml-1 font-semibold text-indigo-500">{r.note}</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

const signed = (x: number | null | undefined, goodNeg = true) => {
  if (typeof x !== "number") return <span className="text-zinc-400">—</span>;
  const good = x < 0 === goodNeg && Math.abs(x) > 1e-9;
  const cls = Math.abs(x) < 1e-9 ? "text-zinc-400" : good ? "text-emerald-600" : "text-rose-600";
  return <span className={cls}>{x >= 0 ? "+" : ""}{x.toFixed(3)}</span>;
};

export default function MispredictionPage() {
  const d = data as any;
  const m = d.meta;
  const adj = d.adjudication;
  const e2 = d.e2.by_condition as Record<string, any>;
  const e3 = d.e3 as Record<string, any>;
  const e4 = d.e4 as Record<string, any>;
  const e5 = d.e5.by_condition as Record<string, any>;
  const conds = ["distilled", "generic", "wrong"];

  // folder-vs-inline comparison (both modes exported into data.json)
  const modes = [d.folder, d.inline].filter(Boolean) as any[];

  const e3Items = Object.entries(e3).filter(([, v]: any) => "spread_pred" in v) as [string, any][];
  const spreadMax = Math.max(...e3Items.flatMap(([, v]) => [v.spread_real, v.spread_pred]), 0.01);
  const barRows = e3Items.length
    ? [
        { label: "real developers", value: e3Items[0][1].spread_real, color: "bg-zinc-500", note: "actual" },
        ...e3Items.map(([c, v]) => ({
          label: `predicted · ${c}`,
          value: v.spread_pred,
          color: "bg-indigo-400",
          note: v.perm_p < 0.05 ? "p<.05" : "",
        })),
      ]
    : [];

  return (
    <main className="mx-auto max-w-4xl px-6 py-14">
      <nav className="flex items-center justify-between text-sm">
        <span className="font-semibold text-zinc-900">SWESimBench</span>
        <div className="flex gap-4 text-zinc-500">
          <span className="rounded bg-zinc-900 px-2 py-0.5 text-xs font-medium text-white">misprediction</span>
          <a href="/" className="hover:text-zinc-900">v2 dataset</a>
          <a href="/samples" className="hover:text-zinc-900">message samples</a>
          <a href="/v1" className="hover:text-zinc-900">v1 leaderboard →</a>
        </div>
      </nav>

      <header className="mt-8">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">
          Are the simulator&rsquo;s mispredictions <em>homogeneity</em>?
        </h1>
        <p className="mt-3 max-w-2xl text-zinc-600">
          <strong>Hypothesis.</strong>{" "}LLMs are trained to complete tasks, not to imitate humans — so
          they are systematically homogeneous, defaulting to task-driving behaviour instead of deciding
          from an individual developer&rsquo;s differences. If true, a user-simulator&rsquo;s errors
          should cluster on the human, friction-y moves (pushing back, interrupting, asking, redirecting)
          and regress every developer toward one &ldquo;average&rdquo; one.
        </p>
        <p className="mt-3 text-sm text-zinc-500">
          Powered run: <strong>{m.users}</strong> developers / <strong>{fmt(m.points)}</strong>{" "}
          move-labelled held-out points from the in-repo <code className="font-mono">tasks/</code> cohort.
          Folder mode is the product flow.
        </p>
      </header>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard label="developers" value={fmt(m.users)} sub="held-out cohort" />
        <StatCard label="labelled points" value={fmt(m.points)} sub="move-classified" />
        {e3.generic?.spread_pred != null && (
          <StatCard
            label="between-user spread"
            value={<>{n3(e3.generic.spread_pred).slice(0, 4)}<span className="ml-1 text-sm font-normal text-zinc-400">vs {n3(e3.generic.spread_real).slice(0, 4)}</span></>}
            sub="predicted (generic) vs real"
          />
        )}
        {adj && (
          <StatCard label="worst misses: homogeneity" value={`${Math.round(100 * adj.homogeneity_share)}%`} sub={`task-completion / generic (n=${adj.n_adjudicated})`} />
        )}
      </div>

      {d.scoreboard && (
        <Section kicker="Scoreboard" title="Which claims survived the data?">
          <p className="text-zinc-600">
            Each experiment made a falsifiable prediction before the run. Evidence columns are the{" "}
            <strong>generic</strong> condition for E2/E3 and <strong>distilled</strong> for E4 (the
            strongest test of each).
          </p>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-zinc-500">
                  <th className="py-1 text-left font-semibold">claim</th>
                  <th className="py-1 text-left font-semibold">prediction if the hypothesis is TRUE</th>
                  <th className="py-1 text-right font-semibold">folder</th>
                  <th className="py-1 pr-6 text-right font-semibold">inline</th>
                  <th className="py-1 text-left font-semibold">verdict</th>
                </tr>
              </thead>
              <tbody>
                {d.scoreboard.map((s: any) => (
                  <React.Fragment key={s.id}>
                    <tr className="border-t border-zinc-100">
                      <td className="py-2 font-medium text-zinc-900">{s.id}</td>
                      <td className="py-2 text-zinc-600">{s.claim}</td>
                      <td className="py-2 text-right tabular-nums text-zinc-600">{s.folder}</td>
                      <td className="py-2 pr-6 text-right tabular-nums text-zinc-600">{s.inline}</td>
                      <td className="py-2">
                        <span className={`inline-block whitespace-nowrap rounded px-1.5 py-0.5 text-[11px] font-bold uppercase tracking-wide ${VERDICT_CLS[s.verdict] ?? "bg-zinc-100 text-zinc-500"}`}>
                          {s.verdict}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td />
                      <td colSpan={4} className="pb-2 text-xs text-zinc-400">{s.note}</td>
                    </tr>
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 rounded-xl border border-zinc-200 border-l-[3px] border-l-indigo-500 bg-white px-4 py-3 text-sm text-zinc-700">
            <strong>What it adds up to.</strong> The simulator really is homogeneous — it compresses
            distinct developers into a narrow band of behaviour (H2) and its worst errors are
            task-completion substitutions (E1). But the mechanism is <em>not</em> the one H3 proposed:
            predictions do not shrink toward the average human, they cluster around the{" "}
            <strong>model&rsquo;s own attractor</strong>, which sits measurably away from the real
            developer average. Personalisation moves the voice, not the decision (E5).
          </div>
        </Section>
      )}

      <Section kicker="Method" title="Three falsifiable claims">
        <p className="text-zinc-600">
          Each held-out point carries the real next message plus a simulated one under three conditions —{" "}
          <strong>distilled</strong> (the user&rsquo;s own folder), <strong>generic</strong> (no folder /
          pure task prior) and <strong>wrong</strong>{" "}(a different user&rsquo;s folder). Every message is
          labelled with a conversational <strong>move</strong>, folded to four categories:{" "}
          <Chip cat="approve" /> accept · <Chip cat="critical" /> assert something is wrong ·{" "}
          <Chip cat="directive" /> say what to do next · <Chip cat="inquiry" /> ask for an answer.
        </p>
        <ul className="mt-3 space-y-2 text-zinc-600">
          <li>
            <span className="font-semibold text-zinc-900">H1 — central attractor</span>{" "}
            <span className="rounded bg-indigo-50 px-1.5 text-xs text-indigo-600">secondary</span> predictions
            over-produce approve/directive, under-produce critical/inquiry. Prompt-sensitive, so descriptive here.
          </li>
          <li>
            <span className="font-semibold text-zinc-900">H2 — between-user variance collapse</span>{" "}
            <span className="rounded bg-indigo-50 px-1.5 text-xs text-indigo-600">primary</span> predicted per-user
            move-mixes are more alike than real ones.
          </li>
          <li>
            <span className="font-semibold text-zinc-900">H3 — regression to the median developer</span>{" "}
            <span className="rounded bg-indigo-50 px-1.5 text-xs text-indigo-600">primary</span> each user&rsquo;s
            predicted mix sits closer to the population average than their real mix.
          </li>
        </ul>
      </Section>

      <Section kicker="E1 · direct audit" title="Worst mispredictions">
        <p className="text-zinc-600">
          The worst mispredictions (move mismatch × low realism), each LLM-adjudicated. The homogeneity
          signature is a high share of <strong>task-completion substitution</strong> (predicted keep-going
          where the real developer did something individual) and <strong>generic-not-specific</strong>.
        </p>
        {adj && (
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-zinc-500">
                  <th className="py-1 text-left font-semibold">error type</th>
                  <th className="py-1 text-right font-semibold">count</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(adj.error_type_counts as Record<string, number>)
                  .sort((a, b) => b[1] - a[1])
                  .map(([k, v]) => (
                    <tr key={k} className="border-t border-zinc-100">
                      <td className="py-2 font-medium text-zinc-700">
                        {k}
                        {["task_completion_substitution", "generic_not_specific"].includes(k) && (
                          <span className="ml-2 rounded bg-indigo-50 px-1.5 text-xs text-indigo-600">homogeneity</span>
                        )}
                      </td>
                      <td className="py-2 text-right tabular-nums text-zinc-600">{v}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
        <div className="mt-6 space-y-3">
          {d.worst.map((x: any, i: number) => (
            <div key={i} className="grid grid-cols-1 gap-3 rounded-lg border border-zinc-200 bg-white p-3 sm:grid-cols-[7rem_1fr_1fr]">
              <div>
                <div className="text-sm font-medium text-zinc-900">{x.slug}</div>
                <div className="text-xs text-zinc-400">realism {n1(x.judge_realism ?? 0).slice(0, 2)}</div>
              </div>
              <div className="border-l-2 border-zinc-300 pl-3">
                <Chip cat={x.real_cat} />
                <div className="mt-1 text-sm text-zinc-700">{(x.real ?? "").slice(0, 200)}</div>
              </div>
              <div className="border-l-2 border-indigo-300 pl-3">
                <Chip cat={x.pred_cat} />
                <div className="mt-1 text-sm text-zinc-700">{(x.generated ?? "").slice(0, 200)}</div>
                {x.error_type && (
                  <div className="mt-1 text-xs text-zinc-400">
                    → <span className="font-semibold text-zinc-600">{x.error_type}</span> · reasonable={String(x.reasonable)}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Section>

      {modes.length === 2 && (
        <Section kicker="Folder vs inline" title="Two ways to read the folder into the simulator">
          <p className="text-zinc-600">
            <strong>folder</strong> = the agent reads <code className="font-mono text-xs">users/&lt;slug&gt;/</code>{" "}
            itself (product flow); <strong>inline</strong> = the folder text is pasted into the prompt
            (controlled). They diverge: inline reproduces signature catchphrases verbatim, which{" "}
            <em>inflates</em> apparent between-user distinctiveness — masking the variance-collapse (E3) —
            yet E4 shows that distinctiveness points <em>away</em> from the real user, and its worst
            misses are even more homogeneity-driven.
          </p>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-zinc-500">
                  <th className="py-1 text-left font-semibold">mode</th>
                  <th className="py-1 text-right font-semibold">H2 generic spread (pred vs real)</th>
                  <th className="py-1 text-right font-semibold">perm p</th>
                  <th className="py-1 text-left font-semibold">E5 verdict</th>
                  <th className="py-1 text-right font-semibold">E1 homogeneity</th>
                </tr>
              </thead>
              <tbody>
                {modes.map((mm) => {
                  const g = mm.e3?.generic ?? {};
                  const a = mm.adjudication ?? {};
                  return (
                    <tr key={mm.meta.mode} className="border-t border-zinc-100">
                      <td className="py-2 font-medium text-zinc-700">{mm.meta.mode}</td>
                      <td className="py-2 text-right tabular-nums text-zinc-600">
                        {n3(g.spread_pred)} <span className="text-zinc-400">vs {n3(g.spread_real)}</span>
                      </td>
                      <td className="py-2 text-right tabular-nums text-zinc-600">
                        {g.perm_p < 0.05 ? <span className="font-semibold text-indigo-500">{n3(g.perm_p)}</span> : n3(g.perm_p)}
                      </td>
                      <td className="py-2 text-zinc-600">{mm.e5?.verdict}</td>
                      <td className="py-2 text-right tabular-nums text-zinc-600">
                        {a.homogeneity_share != null ? `${Math.round(100 * a.homogeneity_share)}%` : "—"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <Section kicker="E3 · primary result" title="Between-user variance collapse">
        <p className="text-zinc-600">
          Mean pairwise total-variation distance between developers&rsquo; move-mixes. If the model captured
          individual differences, predicted spread would match real spread; homogeneity predicts a{" "}
          <strong>narrower</strong> predicted spread. Shorter bar = developers look more alike.
        </p>
        <div className="mt-4">
          <Bars rows={barRows} max={spreadMax} />
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-zinc-500">
                <th className="py-1 text-left font-semibold">condition</th>
                <th className="py-1 text-right font-semibold">users</th>
                <th className="py-1 text-right font-semibold">spread real</th>
                <th className="py-1 text-right font-semibold">spread pred</th>
                <th className="py-1 text-right font-semibold">Δ</th>
                <th className="py-1 text-right font-semibold">perm p</th>
                <th className="py-1 text-right font-semibold">collapse?</th>
              </tr>
            </thead>
            <tbody>
              {e3Items.map(([c, v]) => (
                <tr key={c} className="border-t border-zinc-100">
                  <td className="py-2 font-medium text-zinc-700">{c}</td>
                  <td className="py-2 text-right tabular-nums text-zinc-600">{v.n_users}</td>
                  <td className="py-2 text-right tabular-nums text-zinc-600">{n3(v.spread_real)}</td>
                  <td className="py-2 text-right tabular-nums text-zinc-600">{n3(v.spread_pred)}</td>
                  <td className="py-2 text-right tabular-nums">{signed(v.pred_minus_real)}</td>
                  <td className="py-2 text-right tabular-nums text-zinc-600">{n3(v.perm_p)}</td>
                  <td className="py-2 text-right text-zinc-600">{v.collapse ? "collapse ✓" : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section kicker="E5 · decision vs. surface" title="Does the folder change the decision or only the voice?">
        <p className="text-zinc-600">
          Verdict: <strong>{d.e5.verdict}</strong>. {d.e5.reading} <code className="font-mono text-xs">move dist→real</code>{" "}
          is the move-mix distance to the real user (lower = better decisions); <code className="font-mono text-xs">judge style</code> is surface voice.
        </p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-zinc-500">
                <th className="py-1 text-left font-semibold">condition</th>
                <th className="py-1 text-right font-semibold">move dist→real</th>
                <th className="py-1 text-right font-semibold">judge style</th>
                <th className="py-1 text-right font-semibold">judge realism</th>
                <th className="py-1 text-right font-semibold">judge content</th>
              </tr>
            </thead>
            <tbody>
              {conds.map((c) =>
                e5[c] ? (
                  <tr key={c} className="border-t border-zinc-100">
                    <td className="py-2 font-medium text-zinc-700">{c}</td>
                    <td className="py-2 text-right tabular-nums text-zinc-600">{n3(e5[c].move_dist_to_real)}</td>
                    <td className="py-2 text-right tabular-nums text-zinc-600">{n1(e5[c].judge_style)}</td>
                    <td className="py-2 text-right tabular-nums text-zinc-600">{n1(e5[c].judge_realism)}</td>
                    <td className="py-2 text-right tabular-nums text-zinc-600">{n1(e5[c].judge_content)}</td>
                  </tr>
                ) : null
              )}
            </tbody>
          </table>
        </div>
      </Section>

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        Reproduce: <code className="font-mono">python3 scripts/misprediction.py --adjudicate</code>. Part of SWESimBench.
      </footer>
    </main>
  );
}
