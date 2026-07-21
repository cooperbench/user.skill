import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "UserBench results — full 620 agentic eval",
  description:
    "Agentic next-move match rates on the full UserBench Hub eval (620 tasks / 62 developers), with and without train400 sessions. Harbor Hub jobs, dataset links, and methodology.",
};

const DATASET = "https://hub.harborframework.com/datasets/userbench/UserBench";
const DATASET_TRAIN = "https://hub.harborframework.com/datasets/userbench/UserBench-train400";
const DATASET_REF = "userbench/UserBench@v2";
const DATASET_TRAIN_REF = "userbench/UserBench-train400@v2";
const HUB_TASKS = 620;
const HUB_DEVS = 62;

/** Prior 226-point slice chance (majority gold) — kept for the archived slice table. */
const SLICE_CHANCE_MATCH = 110;
const SLICE_CHANCE_N = 226;
const SLICE_CHANCE = SLICE_CHANCE_MATCH / SLICE_CHANCE_N;

type Run = {
  id: string;
  model: string;
  condition: string;
  sandbox: string;
  match: number;
  n: number;
  rate: number;
  se: number;
  cost: string;
  job: string;
  headline: string;
  note?: string;
};

/** Binomial SE of a proportion: √(p(1−p)/n), returned in percentage points. */
function binomialSePp(match: number, n: number): number {
  const p = match / n;
  return 100 * Math.sqrt((p * (1 - p)) / n);
}

function pct(x: number) {
  return `${(100 * x).toFixed(1)}%`;
}

function fmtSe(sePp: number) {
  return `± ${sePp.toFixed(1)}%`;
}

function rateLabel(match: number, n: number) {
  const p = match / n;
  return `${pct(p)} ${fmtSe(binomialSePp(match, n))}`;
}

function matchHeadline(match: number, n: number) {
  return `${match}/${n} = ${rateLabel(match, n)}`;
}

/** Full Hub-scale Sol high dual eval (2026-07-20). Harbor mean reward → matches. */
const FULL_RUNS: Run[] = [
  {
    id: "sol-high-baseline",
    model: "gpt-5.6-sol [high]",
    condition: "UserBench (no train)",
    sandbox: "Modal",
    match: 288,
    n: 620,
    rate: 288 / 620,
    se: binomialSePp(288, 620),
    cost: "~$84.07",
    job: "https://hub.harborframework.com/jobs/c8958ef2-67c9-4116-9e86-b347f0f8f62d",
    headline: matchHeadline(288, 620),
    note: "Hub package rev 6 · agent-phase OpenRouter allowlist",
  },
  {
    id: "sol-high-train400",
    model: "gpt-5.6-sol [high]",
    condition: "UserBench-train400",
    sandbox: "Modal",
    match: 240,
    n: 620,
    rate: 240 / 620,
    se: binomialSePp(240, 620),
    cost: "~$213.86",
    job: "https://hub.harborframework.com/jobs/d8501a41-08f7-4945-8a23-f6a9f13e4308",
    headline: matchHeadline(240, 620),
    note: "Hub package rev 3 · 146 trial errors (mostly NonZeroAgentExitCode)",
  },
];

/** Archived 226-point / 10-dev slice (prior package). */
const SLICE_RUNS: Run[] = [
  {
    id: "sol-modal-slice",
    model: "gpt-5.6-sol",
    condition: "226-point slice",
    sandbox: "Modal",
    match: 113,
    n: 226,
    rate: 113 / 226,
    se: binomialSePp(113, 226),
    cost: "~$19.13",
    job: "https://hub.harborframework.com/jobs/f3ca33a9-3e22-4b0b-9fd4-d1a9ccd533d1",
    headline: matchHeadline(113, 226),
  },
  {
    id: "kimi-slice",
    model: "kimi-k3",
    condition: "226-point slice",
    sandbox: "Modal",
    match: 106,
    n: 226,
    rate: 106 / 226,
    se: binomialSePp(106, 226),
    cost: "~$20.01",
    job: "https://hub.harborframework.com/jobs/bb239f60-6303-4d11-a512-c2f4a0dbd928",
    headline: matchHeadline(106, 226),
  },
];

function ExtLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a href={href} target="_blank" rel="noreferrer" className="text-indigo-600 underline-offset-2 hover:underline">
      {children}
    </a>
  );
}

function StatCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white px-5 py-4">
      <div className="text-3xl font-semibold tracking-tight text-zinc-900">{value}</div>
      <div className="mt-1 text-sm font-medium text-zinc-600">{label}</div>
      {sub && <div className="mt-0.5 text-xs text-zinc-400">{sub}</div>}
    </div>
  );
}

function Section({ title, kicker, children }: { title: string; kicker?: string; children: ReactNode }) {
  return (
    <section className="mt-12">
      {kicker && <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">{kicker}</div>}
      <h2 className="mt-1 text-xl font-semibold tracking-tight text-zinc-900">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function StatusPill() {
  return (
    <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-emerald-700 ring-1 ring-inset ring-emerald-200">
      complete
    </span>
  );
}

function MatchBar({ rate, se, max = 0.65 }: { rate: number; se: number; max?: number }) {
  return (
    <div className="relative h-7 flex-1 overflow-hidden rounded bg-zinc-100">
      <div className="h-full rounded bg-indigo-500" style={{ width: `${Math.min(100, (rate / max) * 100)}%` }} />
      <div className="absolute inset-y-0 left-2 flex items-center gap-1.5 font-mono text-xs font-semibold text-zinc-800">
        <span>{pct(rate)}</span>
        <span className="font-medium text-zinc-600">{fmtSe(se)}</span>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-14">
      <nav className="flex items-center justify-between text-sm">
        <a href="/" className="font-semibold text-zinc-900 hover:text-zinc-700">
          UserBench
        </a>
        <div className="flex flex-wrap items-center gap-4 text-zinc-500">
          <span className="rounded bg-zinc-900 px-2 py-0.5 text-xs font-medium text-white">results</span>
          <a href="/" className="hover:text-zinc-900">
            Dataset →
          </a>
          <a href="/annotator" className="hover:text-zinc-900">
            annotator →
          </a>
          <a href="/v1" className="hover:text-zinc-900">
            old leaderboard →
          </a>
        </div>
      </nav>

      <header className="mt-8">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">
          Agentic results — full Hub eval
        </h1>
        <p className="mt-3 max-w-2xl text-zinc-600">
          Move-match rates for <strong>gpt-5.6-sol</strong> (reasoning effort <strong>high</strong>) on the
          full <ExtLink href={`${DATASET}?tag=v2`}>{DATASET_REF}</ExtLink> cut:{" "}
          <strong>{HUB_DEVS} developers × 10 = {HUB_TASKS} tasks</strong>. Twin arm adds leak-safe train
          sessions via <ExtLink href={`${DATASET_TRAIN}?tag=v2`}>{DATASET_TRAIN_REF}</ExtLink>. Agent:{" "}
          <span className="font-mono text-sm">mini-swe-agent</span> via OpenRouter; judge:{" "}
          <strong>Composer 2.5</strong>; sandboxes: <strong>Modal</strong>. During agent.run, outbound
          internet is restricted to an OpenRouter allowlist.
        </p>
      </header>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard label="eval points" value={String(HUB_TASKS)} sub={`${HUB_DEVS} developers · Hub scale`} />
        <StatCard
          label="no-train match"
          value={pct(288 / 620)}
          sub={`${fmtSe(binomialSePp(288, 620))} SE · sol high`}
        />
        <StatCard
          label="train400 match"
          value={pct(240 / 620)}
          sub={`${fmtSe(binomialSePp(240, 620))} SE · sol high`}
        />
        <StatCard label="Δ train400" value="−7.7 pp" sub="train400 below no-train on this run" />
      </div>

      <Section kicker="leaderboard" title="Match rate on the full 620-task eval">
        <p className="mb-4 text-sm text-zinc-500">
          Numbers are <strong>Harbor mean reward</strong> as matches / {HUB_TASKS} ± binomial SE (
          <span className="font-mono text-xs">√(p(1−p)/n)</span>). Same model, judge, and Modal stack on
          both arms.
        </p>

        <div className="space-y-4 rounded-xl border border-zinc-200 bg-white p-5">
          {FULL_RUNS.map((r) => (
            <div key={r.id}>
              <div className="mb-1.5 flex flex-wrap items-baseline gap-2">
                <span className="font-mono text-sm font-semibold text-zinc-900">{r.model}</span>
                <span className="text-xs text-zinc-500">{r.condition}</span>
                <span className="text-xs text-zinc-400">{r.sandbox}</span>
                <StatusPill />
                <span className="ml-auto font-mono text-sm tabular-nums text-zinc-700">{r.headline}</span>
              </div>
              <div className="flex items-center gap-3">
                <MatchBar rate={r.rate} se={r.se} />
                <div className="w-20 shrink-0 text-right text-xs tabular-nums text-zinc-500">{r.cost}</div>
              </div>
              <div className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1 text-xs text-zinc-500">
                <ExtLink href={r.job}>Harbor Hub job → trials</ExtLink>
                {r.note ? <span>{r.note}</span> : null}
              </div>
            </div>
          ))}
          <p className="border-t border-zinc-100 pt-3 text-xs text-zinc-500">
            Scale 0–65%. ± is binomial SE in percentage points, not a confidence interval. Cost ≈
            OpenRouter + Harbor-reported agent spend. Train400 cost is higher (larger context under{" "}
            <span className="font-mono">/sim/train/</span>).
          </p>
        </div>
      </Section>

      <Section kicker="on harbor hub" title="Jobs and datasets">
        <div className="overflow-x-auto rounded-xl border border-zinc-200 bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-100 text-left text-xs uppercase tracking-wide text-zinc-400">
                <th className="px-4 py-3 font-medium">arm</th>
                <th className="px-4 py-3 font-medium">match</th>
                <th className="px-4 py-3 font-medium">cost</th>
                <th className="px-4 py-3 font-medium">hub</th>
              </tr>
            </thead>
            <tbody>
              {FULL_RUNS.map((r) => (
                <tr key={r.id} className="border-t border-zinc-50">
                  <td className="px-4 py-3">
                    <div className="font-mono text-xs font-semibold text-zinc-900">{r.condition}</div>
                    <div className="text-xs text-zinc-500">{r.model}</div>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs tabular-nums text-zinc-800">{r.headline}</td>
                  <td className="px-4 py-3 tabular-nums text-zinc-600">{r.cost}</td>
                  <td className="px-4 py-3">
                    <ExtLink href={r.job}>job / trials ↗</ExtLink>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">datasets</div>
            <p className="mt-2 text-sm text-zinc-700">
              <span className="font-mono text-xs">{DATASET_REF}</span> and{" "}
              <span className="font-mono text-xs">{DATASET_TRAIN_REF}</span> —{" "}
              <strong>{HUB_TASKS}</strong> held tasks / <strong>{HUB_DEVS}</strong> developers. Train twin
              adds earlier sessions under <span className="font-mono text-xs">/sim/train/</span>.
            </p>
            <div className="mt-3 flex flex-wrap gap-3 text-sm">
              <ExtLink href={DATASET}>UserBench ↗</ExtLink>
              <ExtLink href={DATASET_TRAIN}>train400 ↗</ExtLink>
            </div>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">network</div>
            <p className="mt-2 text-sm text-zinc-700">
              Environment baseline and verifier are <span className="font-mono text-xs">public</span>{" "}
              (image build, agent install, Composer judge). Agent phase is an OpenRouter{" "}
              <span className="font-mono text-xs">allowlist</span> so the sandbox cannot browse the open
              web while solving.
            </p>
          </div>
        </div>
      </Section>

      <Section kicker="archive" title="Earlier 226-point / 10-dev slice">
        <p className="mb-4 text-sm text-zinc-500">
          Complete Modal jobs on a cheaper-history 226-point slice from a prior package revision — not the
          full current Hub eval. Chance (majority gold) on that slice:{" "}
          {SLICE_CHANCE_MATCH}/{SLICE_CHANCE_N} = {rateLabel(SLICE_CHANCE_MATCH, SLICE_CHANCE_N)}.
        </p>
        <div className="space-y-3 rounded-xl border border-zinc-200 bg-white p-5">
          {SLICE_RUNS.map((r) => (
            <div key={r.id} className="flex flex-wrap items-baseline justify-between gap-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="font-mono font-semibold text-zinc-900">{r.model}</span>
                <span className="text-xs text-zinc-400">{r.sandbox}</span>
              </div>
              <span className="font-mono text-xs tabular-nums text-zinc-700">{r.headline}</span>
              <ExtLink href={r.job}>Hub job ↗</ExtLink>
            </div>
          ))}
          <p className="border-t border-zinc-100 pt-3 text-xs text-zinc-500">
            Slice chance line at {pct(SLICE_CHANCE)}. Kept for continuity with earlier write-ups.
          </p>
        </div>
      </Section>

      <Section kicker="how it was scored" title="Methodology">
        <div className="space-y-3 text-sm leading-relaxed text-zinc-600">
          <p>
            <strong className="text-zinc-800">Task.</strong> At a held-out user turn, the agent reads the
            session history from disk and produces the next user message. A judge labels the predicted
            message into the 4-way move taxonomy (
            <span className="font-mono text-xs">approve / critical / directive / inquiry</span>
            ). Reward is 1 iff predicted move equals gold move. Published tasks keep{" "}
            <span className="font-mono text-xs">gold_move = null</span>; the judge classifies gold{" "}
            <span className="font-mono text-xs">real</span> at verify time.
          </p>
          <p>
            <strong className="text-zinc-800">Full eval (headline numbers).</strong> Exactly 10
            shortest-history points per developer with ≥10 eval points → {HUB_DEVS}×10 = {HUB_TASKS}{" "}
            tasks. Train400 uses the same held points plus earlier train sessions.
          </p>
          <p>
            <strong className="text-zinc-800">Stack.</strong> Agent = mini-swe-agent 2.4.5 (OpenRouter,
            openai-only pin). Judge = Composer 2.5 (cursor-agent on Modal volume). Sandboxes = Modal
            (kevinli).
          </p>
          <p>
            <strong className="text-zinc-800">Uncertainty.</strong> Reported ± is the binomial standard
            error of the match rate, <span className="font-mono text-xs">SE = √(p(1−p)/n)</span>, in
            percentage points. It is not a Wilson confidence interval.
          </p>
        </div>
      </Section>

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        UserBench agentic results · full Hub eval {HUB_TASKS} tasks ·{" "}
        <ExtLink href={DATASET}>{DATASET_REF}</ExtLink> ·{" "}
        <ExtLink href={DATASET_TRAIN}>{DATASET_TRAIN_REF}</ExtLink> · see the{" "}
        <a href="/" className="text-zinc-600 hover:text-zinc-900">
          Dataset
        </a>{" "}
        and{" "}
        <a href="/v1" className="text-zinc-600 hover:text-zinc-900">
          old leaderboard
        </a>
        .
      </footer>
    </main>
  );
}
