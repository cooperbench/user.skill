// SWESimBench v2 — exploratory data analysis of the authoritative clean harbor cohort.
// Data: app/v2data.json (regenerated via scripts/export_v2data.py from .private/v2-58/).
import data from "./v2data.json";

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

// per-user histogram from a numeric array
function Hist({ values, bins, unit }: { values: number[]; bins: number[]; unit: string }) {
  const counts = new Array(bins.length - 1).fill(0);
  values.forEach((v) => {
    for (let i = 0; i < bins.length - 1; i++) if (v >= bins[i] && v < bins[i + 1]) { counts[i]++; break; }
  });
  const max = Math.max(...counts, 1);
  return (
    <div>
      <div className="flex items-stretch gap-1" style={{ height: 120 }}>
        {counts.map((c, i) => (
          <div key={i} className="flex h-full flex-1 flex-col justify-end">
            <div
              className="w-full rounded-t bg-indigo-400"
              style={{ height: `${Math.max((100 * c) / max, c > 0 ? 3 : 0)}%` }}
              title={`${c} developers`}
            />
          </div>
        ))}
      </div>
      <div className="mt-1 flex gap-1 text-[9px] text-zinc-400">
        {counts.map((_, i) => {
          const k = (n: number) => (n >= 1000 ? `${n / 1000 % 1 === 0 ? n / 1000 : (n / 1000).toFixed(1)}k` : `${n}`);
          const lo = bins[i], hi = bins[i + 1];
          return (
            <div key={i} className="flex-1 text-center leading-tight">
              {i === counts.length - 1 ? `${k(lo)}+` : `${k(lo)}–${k(hi)}`}
            </div>
          );
        })}
      </div>
      <div className="mt-0.5 text-center text-[11px] text-zinc-400">{unit} per developer</div>
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

export default function V2Page() {
  const s = data.summary;
  const h = (data.harness ?? {}) as Record<string, { sessions: number; user_turns: number }>;
  const cc = h["claude-code"] ?? { sessions: 0, user_turns: 0 };
  const cx = h["codex"] ?? { sessions: 0, user_turns: 0 };
  const totTurns = cc.user_turns + cx.user_turns || 1;
  const totSess = cc.sessions + cx.sessions || 1;

  // model families: consolidate into a clean set
  const mfRaw = data.model_families as Record<string, number>;
  const famMap: Record<string, string> = {
    "claude-opus": "Claude Opus", "claude-sonnet": "Claude Sonnet", "claude-haiku": "Claude Haiku",
    "claude (other)": "Claude (other)", "codex (gpt-5-codex/…)": "Codex (gpt-5.x)",
    "gpt-5.5": "Codex (gpt-5.x)", "gpt-5.4": "Codex (gpt-5.x)", "gpt-5.4-mini": "Codex (gpt-5.x)",
    "gpt-5.6-sol": "Codex (gpt-5.x)", "gpt-5.6-terra": "Codex (gpt-5.x)",
    unknown: "Model not recorded", "<synthetic>": "Model not recorded", "?": "Model not recorded",
  };
  const famAgg: Record<string, number> = {};
  Object.entries(mfRaw).forEach(([k, v]) => {
    const key = famMap[k] ?? "Other proxied backends (GLM/MiniMax/Kimi/…)";
    famAgg[key] = (famAgg[key] ?? 0) + v;
  });
  const famRows = Object.entries(famAgg)
    .sort((a, b) => b[1] - a[1])
    .map(([label, value]) => ({ label, value }));

  const months = data.months as Record<string, number>;
  const monthRows = Object.entries(months).map(([label, value]) => ({ label, value }));
  const monthMax = Math.max(...monthRows.map((r) => r.value), 1);

  const pu = data.per_user as { train_sess: number; eval_sess: number; train_turns: number; eval_turns: number; tok_mean: number }[];
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
    <main className="mx-auto max-w-4xl px-6 py-14">
      <nav className="flex items-center justify-between text-sm">
        <span className="font-semibold text-zinc-900">SWESimBench</span>
        <div className="flex gap-4 text-zinc-500">
          <span className="rounded bg-zinc-900 px-2 py-0.5 text-xs font-medium text-white">v2 dataset</span>
          <a href="/samples" className="hover:text-zinc-900">message samples</a>
          <a href="/v1" className="hover:text-zinc-900">v1 leaderboard →</a>
        </div>
      </nav>

      <header className="mt-8">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">
          SWESimBench v2 — the {s.n_users}-developer harbor cohort
        </h1>
        <p className="mt-3 max-w-2xl text-zinc-600">
          Authoritative clean cohort: <strong>{fmt(s.n_users)}</strong> developers /{" "}
          <strong>{fmt(data.eval_dist.n_points)}</strong> held-out prediction points
          {("policy_version" in s) && <> under <code className="text-xs">{(s as { policy_version?: string }).policy_version}</code></>}.
          Each developer has a deep <strong>training</strong> history and a strictly-later, non-overlapping{" "}
          <strong>held-out</strong> set from full-fidelity <strong>Claude Code</strong> / <strong>Codex</strong> traces.
          Admission clears ≥400 training and ≥100 held-out user turns; the split is leakage-verified.
          Opus 4.6 era only (sessions on/after 2026-02-05). Source manifest had{" "}
          <strong>{fmt((data as { notes?: { source_manifest_users?: number } }).notes?.source_manifest_users ?? 80)}</strong> developers;{" "}
          <strong>{fmt((data as { notes?: { dropped?: number } }).notes?.dropped ?? 22)}</strong> were dropped in cleaning.
        </p>
      </header>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-5">
        <StatCard label="developers" value={fmt(s.n_users)} sub="clean cohort" />
        <StatCard label="eval points" value={fmt(data.eval_dist.n_points)} sub="held-out moments" />
        <StatCard label="sessions" value={fmt(s.n_sessions)} sub="full traces" />
        <StatCard label="user turns" value={fmt(s.n_user_turns)} />
        <StatCard label="assistant turns" value={fmt(s.n_assistant_turns)} />
      </div>
      <p className="mt-3 text-sm text-zinc-500">
        Sessions span <strong>{s.time_min}</strong> → <strong>{s.time_max}</strong>.
      </p>

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
            "GitHub .claude/.codex crawl": { color: "bg-teal-400", how: "Developers who committed their ~/.claude/projects or .codex/sessions dumps to public repos; found by tree-probing public GitHub for session-dense trees, then harvested with preserved sparse clones." },
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
          Three full-trace Claude Code / Codex sources, one shared native-JSONL parser. In this clean cohort,
          DataClaw contributes the most <em>sessions</em>; Entire (including SWE-chat overlap) and DataClaw
          dominate user turns. Lossy IDE-markdown (SpecStory) and non-CC/Codex agents (pi, Cursor, WildChat)
          are excluded. Every session id is deduped across sources, and the train/held split is
          leakage-verified.
        </p>
      </Section>

      <Section kicker="side by side" title="How the sources differ">
        {(() => {
          const sc = data.source_compare as Record<string, Record<string, string | number>>;
          const cols = ["Entire checkpoints", "GitHub .claude/.codex crawl", "DataClaw (HF donors)"];
          const short: Record<string, string> = { "Entire checkpoints": "Entire", "GitHub .claude/.codex crawl": "GitHub crawl", "DataClaw (HF donors)": "DataClaw" };
          const order = ["developers (dominant)", "sessions", "user turns", "assistant turns",
            "user turns / session (mean)", "assistant / user turn", "train:eval turn %"].filter((m) => !!sc[m]);
          const num = (x: string | number | undefined) => (x == null ? "—" : typeof x === "number" ? fmt(x) : x);
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
          Source mix for the retained {fmt(s.n_users)}-developer cohort. Entire dominates developer count;
          DataClaw still contributes a large share of sessions/turns. Figures above are recomputed from the
          clean cohort (not the pre-clean 80-developer harvest).
        </p>
      </Section>

      {Object.keys((data as { harness?: Record<string, unknown> }).harness ?? {}).length > 0 && (
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
      </Section>
      )}

      <Section kicker="the split" title="Train vs held-out (eval)">
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
          The split is deliberately train-heavy for rich developer profiles, with a lean held-out tail
          (median {r0(d.sessions.eval.median)} sessions / {r0(d.user_turns.eval.median)} user turns) that clears the ≥100 floor.
          Eval scoring uses <strong>{fmt(data.eval_dist.n_points)}</strong> held-out prediction points across{" "}
          <strong>{fmt(data.eval_dist.n_devs)}</strong> developers.
        </p>
      </Section>

      <Section kicker="per-developer spread" title="How deep is each developer?">
        <div className="grid gap-8 sm:grid-cols-2">
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="mb-3 text-sm font-medium text-zinc-700">Training user turns</div>
            <Hist values={pu.map((p) => p.train_turns)} bins={[400, 700, 1000, 1500, 2500, 5000, 100000]} unit="train user turns" />
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="mb-3 text-sm font-medium text-zinc-700">Held-out user turns</div>
            <Hist values={pu.map((p) => p.eval_turns)} bins={[100, 120, 150, 200, 300, 500, 100000]} unit="held-out user turns" />
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="mb-3 text-sm font-medium text-zinc-700">Total sessions</div>
            <Hist values={pu.map((p) => p.train_sess + p.eval_sess)} bins={[0, 30, 60, 100, 200, 400, 100000]} unit="sessions" />
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="mb-3 text-sm font-medium text-zinc-700">Mean tokens / user turn</div>
            <Hist values={pu.map((p) => p.tok_mean)} bins={[0, 40, 70, 100, 150, 250, 100000]} unit="mean tokens/turn" />
          </div>
        </div>
      </Section>

      <Section kicker="what gets scored" title="The eval set — held-out prediction points">
        {(() => {
          const e = data.eval_dist;
          const row = (o: { name: string; median: number; mean: number; p90: number; max: number }) => (
            <tr key={o.name} className="border-t border-zinc-100">
              <td className="py-1.5 pr-4 text-zinc-600">{o.name}</td>
              <td className="py-1.5 pr-4 text-right tabular-nums text-zinc-800">{fmt(Math.round(o.median))}</td>
              <td className="py-1.5 pr-4 text-right tabular-nums text-zinc-500">{fmt(Math.round(o.mean))}</td>
              <td className="py-1.5 pr-4 text-right tabular-nums text-zinc-500">{fmt(Math.round(o.p90))}</td>
              <td className="py-1.5 text-right tabular-nums text-zinc-500">{fmt(Math.round(o.max))}</td>
            </tr>
          );
          const hbins = e.prev_turns_hist.bins as number[];
          const hlabels = hbins.slice(0, -1).map((b, i) => (i === hbins.length - 2 ? `${b}+` : `${b}–${hbins[i + 1]}`));
          return (
            <>
              <p className="mb-4 max-w-2xl text-sm text-zinc-600">
                Each held-out point is a moment where the real developer typed a message; the model must predict
                it, conditioned on <strong>all previous turns of that session</strong>. {fmt(e.n_points)} points
                across {fmt(e.n_devs)} developers.
              </p>
              <div className="grid gap-6 sm:grid-cols-2">
                <table className="text-sm">
                  <thead>
                    <tr className="text-left text-xs uppercase tracking-wide text-zinc-400">
                      <th className="pb-2 pr-4 font-medium">per eval point / developer</th>
                      <th className="pb-2 pr-4 text-right font-medium">median</th>
                      <th className="pb-2 pr-4 text-right font-medium">mean</th>
                      <th className="pb-2 pr-4 text-right font-medium">p90</th>
                      <th className="pb-2 text-right font-medium">max</th>
                    </tr>
                  </thead>
                  <tbody>
                    {row(e.prev_turns)}
                    {row(e.ctx_tokens)}
                    {row(e.points_per_dev)}
                    {row(e.sess_per_dev)}
                  </tbody>
                </table>
                <div>
                  <div className="mb-2 text-sm font-medium text-zinc-700">Previous turns per eval point</div>
                  <Bars rows={hlabels.map((label, i) => ({ label, value: e.prev_turns_hist.counts[i], color: "bg-fuchsia-400" }))} />
                </div>
              </div>
              <p className="mt-3 text-sm text-zinc-500">
                The context depth is heavily skewed — median <strong>{fmt(e.prev_turns.median)}</strong> prior
                turns, but a long tail to <strong>{fmt(e.prev_turns.max)}</strong> (~{fmt(e.ctx_tokens.max)}{" "}
                tokens). That tail is why the eval is run <strong>agentically</strong>: the model reads the
                session history from disk rather than having it all stuffed into one prompt.
              </p>
            </>
          );
        })()}
      </Section>

      <Section kicker="prompt length" title="Tokens per user turn">
        <Bars
          rows={data.tok_hist.labels.map((label, i) => ({ label, value: data.tok_hist.counts[i], color: "bg-emerald-400" }))}
          fmtVal={(n) => fmt(n)}
        />
        <p className="mt-3 text-sm text-zinc-500">
          Heavily right-skewed: median <strong>{fmt(d.tok_per_turn.pooled_median)}</strong> tokens
          (short commands like "run it", "fix the test"), mean <strong>{fmt(d.tok_per_turn.pooled_mean)}</strong>{" "}
          (p90 {fmt(d.tok_per_turn.p90)}, p99 {fmt(d.tok_per_turn.p99)}) — the tail is pasted logs, errors,
          and file dumps. Token lengths are approximate (chars/4) on the clean cohort; {fmt(s.n_user_turns)} user turns.
        </p>
      </Section>

      {Object.keys((data as { model_families?: Record<string, number> }).model_families ?? {}).length > 0 && (
      <Section kicker="models" title="Backing model families">
        <Bars rows={famRows} />
      </Section>
      )}

      <Section kicker="recency" title="Sessions over time">
        <Bars rows={monthRows} max={monthMax} />
        <p className="mt-3 text-sm text-zinc-500">
          {s.time_min} → {s.time_max}, concentrated in early–mid 2026 as coding-agent adoption grew.
        </p>
      </Section>

      <Section kicker="peek inside" title="Read real developer messages">
        <p className="max-w-2xl text-sm text-zinc-600">
          For each of the {fmt(s.n_users)} retained developers we publish{" "}
          <strong>10 randomly sampled user messages</strong> with a few surrounding turns of context
          (lightly redacted/truncated). Useful for getting a feel for the cohort before downloading
          anything.
        </p>
        <a
          href="/samples"
          className="mt-4 inline-flex rounded-lg bg-zinc-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-zinc-700"
        >
          Browse message samples →
        </a>
      </Section>

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        SWESimBench v2 clean cohort · {fmt(s.n_users)} developers · {fmt(data.eval_dist.n_points)} eval points · Claude Code + Codex
        full traces · leakage-verified train/held-out split. See the{" "}
        <a href="/samples" className="text-zinc-600 hover:text-zinc-900">message samples</a>
        {" · "}
        <a href="/v1" className="text-zinc-600 hover:text-zinc-900">v1 leaderboard</a>{" "}
        for the next-action-prediction benchmark.
      </footer>
    </main>
  );
}
