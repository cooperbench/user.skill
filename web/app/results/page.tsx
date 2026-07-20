import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "UserBench results — 10-dev agentic slice",
  description:
    "Agentic next-move match rates on a 226-point UserBench slice (10 cheapest-history-bytes developers from an earlier package). Harbor Hub jobs, dataset links, and methodology.",
};

const CHANCE_MATCH = 110;
const CHANCE_N = 226;
const CHANCE = CHANCE_MATCH / CHANCE_N;
const DATASET = "https://hub.harborframework.com/datasets/userbench/UserBench";
const DATASET_TASKS = "https://hub.harborframework.com/datasets/userbench/UserBench/tasks";
const DATASET_REF = "userbench/UserBench@v2";
const HUB_TASKS = 620;
const HUB_DEVS = 62;

type Run = {
  id: string;
  model: string;
  sandbox: string;
  match: number;
  n: number;
  rate: number;
  se: number;
  cost: string;
  job: string;
  headline: string;
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

const RUNS: Run[] = [
  {
    id: "sol-modal",
    model: "gpt-5.6-sol",
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
    id: "kimi",
    model: "kimi-k3",
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

/** Trial links are from the 226-point jobs (prior package task names on Hub job pages). */
const EXAMPLE_TRIALS = [
  {
    label: "match",
    task: "dc_004__0aba24d1",
    href: "https://hub.harborframework.com/jobs/f3ca33a9-3e22-4b0b-9fd4-d1a9ccd533d1/trials/0b7f1dd1-46b2-4d1b-b56e-9c6f79959eda",
  },
  {
    label: "miss",
    task: "dc_004__05fe03e7",
    href: "https://hub.harborframework.com/jobs/f3ca33a9-3e22-4b0b-9fd4-d1a9ccd533d1/trials/7c1fbe4f-598e-40f4-a75f-5111a979d803",
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

function MatchBar({ rate, se }: { rate: number; se: number }) {
  const max = 0.65;
  return (
    <div className="relative h-7 flex-1 overflow-hidden rounded bg-zinc-100">
      <div
        className="absolute bottom-0 top-0 border-l-2 border-dashed border-zinc-500/70"
        style={{ left: `${(CHANCE / max) * 100}%` }}
        title={`chance (majority) ${rateLabel(CHANCE_MATCH, CHANCE_N)}`}
      />
      <div className="h-full rounded bg-indigo-500" style={{ width: `${Math.min(100, (rate / max) * 100)}%` }} />
      <div className="absolute inset-y-0 left-2 flex items-center gap-1.5 font-mono text-xs font-semibold text-zinc-800">
        <span>{pct(rate)}</span>
        <span className="font-medium text-zinc-600">{fmtSe(se)}</span>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  const maxPrimary = Math.max(...RUNS.map((r) => r.rate), CHANCE);

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
          <a href="/v1" className="hover:text-zinc-900">
            old leaderboard →
          </a>
        </div>
      </nav>

      <header className="mt-8">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">
          Agentic results — 10-dev slice
        </h1>
        <p className="mt-3 max-w-2xl text-zinc-600">
          Move-match rates for models standing in for a software engineer mid-session. These complete
          Modal jobs scored a <strong>226-point / 10-developer</strong> slice (cheapest-history-bytes
          developers) from an <strong>earlier</strong> package revision —{" "}
          <strong>not</strong> the full current Hub eval (
          <ExtLink href={`${DATASET}?tag=v2`}>{DATASET_REF}</ExtLink>, {HUB_DEVS} developers /{" "}
          {HUB_TASKS} tasks). Agent: <span className="font-mono text-sm">mini-swe-agent</span> via
          OpenRouter; judge: <strong>Composer 2.5</strong>; sandboxes: <strong>Modal</strong> (kevinli).
        </p>
      </header>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard label="slice points" value="226" sub="10 developers · not full eval" />
        <StatCard
          label="chance (majority)"
          value={pct(CHANCE)}
          sub={`${fmtSe(binomialSePp(CHANCE_MATCH, CHANCE_N))} SE · always modal gold`}
        />
        <StatCard
          label="best complete"
          value={pct(113 / 226)}
          sub={`${fmtSe(binomialSePp(113, 226))} SE · gpt-5.6-sol · Modal`}
        />
        <StatCard label="Hub eval" value="620" sub={`${HUB_DEVS} developers · current package`} />
      </div>

      <Section kicker="leaderboard" title="Match rate on the 226-point slice">
        <p className="mb-4 text-sm text-zinc-500">
          Dashed line = chance baseline ({rateLabel(CHANCE_MATCH, CHANCE_N)}). Numbers are{" "}
          <strong>matches / scored trials</strong> ± binomial SE (
          <span className="font-mono text-xs">√(p(1−p)/n)</span>) for complete Modal runs on the same
          226-point slice.
        </p>

        <div className="space-y-4 rounded-xl border border-zinc-200 bg-white p-5">
          {RUNS.map((r) => (
            <div key={r.id}>
              <div className="mb-1.5 flex flex-wrap items-baseline gap-2">
                <span className="font-mono text-sm font-semibold text-zinc-900">{r.model}</span>
                <span className="text-xs text-zinc-400">{r.sandbox}</span>
                <StatusPill />
                <span className="ml-auto font-mono text-sm tabular-nums text-zinc-700">{r.headline}</span>
              </div>
              <div className="flex items-center gap-3">
                <MatchBar rate={r.rate} se={r.se} />
                <div className="w-20 shrink-0 text-right text-xs tabular-nums text-zinc-500">{r.cost}</div>
              </div>
              <div className="mt-1.5 text-xs">
                <ExtLink href={r.job}>Harbor Hub job → trials</ExtLink>
              </div>
            </div>
          ))}
          <p className="border-t border-zinc-100 pt-3 text-xs text-zinc-500">
            Scale 0–65%. Chance line at {rateLabel(CHANCE_MATCH, CHANCE_N)}. ± is binomial SE in
            percentage points, not a confidence interval. Cost ≈ OpenRouter + Harbor-reported agent
            spend.
            {maxPrimary > CHANCE ? " gpt-5.6-sol clears chance on the complete Modal slice." : null}
          </p>
        </div>
      </Section>
      <Section kicker="on harbor hub" title="Jobs, dataset, and example trials">
        <div className="overflow-x-auto rounded-xl border border-zinc-200 bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-100 text-left text-xs uppercase tracking-wide text-zinc-400">
                <th className="px-4 py-3 font-medium">model</th>
                <th className="px-4 py-3 font-medium">sandbox</th>
                <th className="px-4 py-3 font-medium">match</th>
                <th className="px-4 py-3 font-medium">cost</th>
                <th className="px-4 py-3 font-medium">hub</th>
              </tr>
            </thead>
            <tbody>
              {RUNS.map((r) => (
                <tr key={r.id} className="border-t border-zinc-50">
                  <td className="px-4 py-3">
                    <div className="font-mono text-xs font-semibold text-zinc-900">{r.model}</div>
                    <StatusPill />
                  </td>
                  <td className="px-4 py-3 text-zinc-600">{r.sandbox}</td>
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
            <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">dataset</div>
            <p className="mt-2 text-sm text-zinc-700">
              Package <span className="font-mono text-xs">{DATASET_REF}</span> —{" "}
              <strong>{HUB_TASKS}</strong> tasks / <strong>{HUB_DEVS}</strong> developers (exactly 10
              shortest-history points per developer with ≥10 eval points). Task refs:{" "}
              <span className="font-mono text-xs">userbench/&lt;username&gt;__&lt;hash&gt;@v2</span>.
            </p>
            <div className="mt-3 flex flex-wrap gap-3 text-sm">
              <ExtLink href={DATASET}>dataset ↗</ExtLink>
              <ExtLink href={DATASET_TASKS}>tasks ↗</ExtLink>
              <ExtLink href={`${DATASET}?tag=v2`}>tag v2 ↗</ExtLink>
            </div>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">example trials</div>
            <p className="mt-2 text-sm text-zinc-700">
              From the gpt-5.6-sol Modal 226-point job (short ids; job pages may still show prior package
              paths):
            </p>
            <ul className="mt-3 space-y-2 text-sm">
              {EXAMPLE_TRIALS.map((t) => (
                <li key={t.href}>
                  <span className="mr-2 rounded bg-zinc-100 px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase text-zinc-600">
                    {t.label}
                  </span>
                  <ExtLink href={t.href}>{t.task}</ExtLink>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Section>

      <Section kicker="how it was scored" title="Methodology">
        <div className="space-y-3 text-sm leading-relaxed text-zinc-600">
          <p>
            <strong className="text-zinc-800">Task.</strong> At a held-out user turn, the agent reads the
            session history from disk and produces the next user message. A judge labels the predicted
            message into the 4-way move taxonomy (
            <span className="font-mono text-xs">approve / critical / directive / inquiry</span>
            ). Reward is 1 iff predicted move equals gold move.
          </p>
          <p>
            <strong className="text-zinc-800">Slice (these numbers).</strong> 10 developers with the
            cheapest history byte footprints → 226 prediction points on a prior package revision. Same
            points for every complete Modal job below. The current Hub package is the full{" "}
            {HUB_DEVS}×10 = {HUB_TASKS}-task cut.
          </p>
          <p>
            <strong className="text-zinc-800">Stack.</strong> Agent = mini-swe-agent (OpenRouter). Judge =
            Composer 2.5 (cursor-agent). Sandboxes = Modal (kevinli).
          </p>
          <p>
            <strong className="text-zinc-800">Chance.</strong> Majority-class baseline on this slice ={" "}
            {CHANCE_MATCH}/{CHANCE_N} = {rateLabel(CHANCE_MATCH, CHANCE_N)} (always emit the most
            common gold move). gpt-5.6-sol Modal is slightly above; kimi-k3 is slightly below.
          </p>
          <p>
            <strong className="text-zinc-800">Uncertainty.</strong> Reported ± is the binomial
            standard error of the match rate,{" "}
            <span className="font-mono text-xs">SE = √(p(1−p)/n)</span>, in percentage points
            (rounded to 1 decimal). It is not a Wilson (or other) confidence interval.
          </p>
        </div>
      </Section>

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        UserBench agentic results · 10-dev / 226-point slice (prior package) · current Hub eval{" "}
        <ExtLink href={DATASET}>{DATASET_REF}</ExtLink> ({HUB_TASKS} tasks) · see the{" "}
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
