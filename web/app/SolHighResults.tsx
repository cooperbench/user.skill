import type { ReactNode } from "react";
import { SectionHeading } from "./SectionHeading";

const HUB_URLS = {
  datasets: {
    baseline:
      "https://hub.harborframework.com/datasets/userbench/UserBench",
    train400:
      "https://hub.harborframework.com/datasets/userbench/UserBench-train400",
  },
  agentTraces: {
    baseline:
      "https://hub.harborframework.com/jobs/4d0dccb6-08d2-4a56-ad47-bf52e7db2e64",
    train400:
      "https://hub.harborframework.com/jobs/af42da25-f641-49fe-8983-604839ddfcd5",
  },
  judgeTraces: {
    baseline:
      "https://hub.harborframework.com/jobs/722b2a3b-032b-494b-96f6-b8febdb54f4f",
    train400:
      "https://hub.harborframework.com/jobs/eb870d83-c07f-46b6-b12f-0b937d402d2a",
    threeRuns:
      "https://hub.harborframework.com/jobs/92a07167-8858-4316-8dbf-e2200ddf8361",
  },
} as const;

const DATASET = HUB_URLS.datasets.baseline;
const DATASET_TRAIN = HUB_URLS.datasets.train400;
const DATASET_REF = "userbench/UserBench";
const DATASET_TRAIN_REF = "userbench/UserBench-train400";
const HUB_TASKS = 620;
const HUB_DEVS = 62;

/**
 * Multilabel judge jobs; mean Jaccard is the benchmark metric.
 * Leaderboard means/SDs: mean of 3 trial-level mean Jaccards ± sample SD
 * across those 3 trial means (see THREE_TRIAL_JACCARD.json).
 */
const ML = {
  baseline: {
    jaccard: 0.445,
    /** Sample SD across 3 trial-level mean Jaccards. */
    trialSd: 0.00677,
    /** mean ± 1 SD over 3 trials. */
    sdBand: [0.4382, 0.4517] as const,
    exact: 0.306,
    exactChance: 0.326,
    nExact: 190,
    chance: 0.439,
    vsChancePp: 0.6,
    macroF1: 0.439,
    n: 620,
    hub: HUB_URLS.judgeTraces.baseline,
  },
  train400: {
    jaccard: 0.494,
    trialSd: 0.00277,
    sdBand: [0.4911, 0.4966] as const,
    exact: 0.35,
    exactChance: 0.324,
    nExact: 217,
    chance: 0.434,
    vsChancePp: 4.6,
    macroF1: 0.468,
    n: 620,
    hub: HUB_URLS.judgeTraces.train400,
  },
  archive3x: {
    jaccard: 0.5,
    n: 1386,
    hub: HUB_URLS.judgeTraces.threeRuns,
  },
  /** train400 − baseline, from means of 3 trials. */
  liftPp: 4.89,
};

/** Agent-trial Hub jobs (gpt-5.6-sol trajectories). */
const AGENT = {
  baseline3x: HUB_URLS.agentTraces.baseline,
  train4003x: HUB_URLS.agentTraces.train400,
};

function pct(x: number, digits = 1) {
  return `${(100 * x).toFixed(digits)}%`;
}

function ExtLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="text-indigo-600 underline-offset-2 hover:underline"
    >
      {children}
    </a>
  );
}

function Section({
  id,
  title,
  kicker,
  children,
}: {
  id?: string;
  title: string;
  kicker?: string;
  children: ReactNode;
}) {
  const sectionId =
    id ??
    title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  return (
    <section
      id={sectionId}
      aria-labelledby={`${sectionId}-title`}
      className="mt-12 scroll-mt-20"
    >
      {kicker && (
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">
          {kicker}
        </div>
      )}
      <SectionHeading
        id={sectionId}
        label={title}
        className="mt-1 text-xl font-semibold tracking-tight text-zinc-900"
      >
        {title}
      </SectionHeading>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ScoreRow({
  label,
  note,
  rate,
  sdBand,
  featured = false,
}: {
  label: string;
  note: string;
  rate: number;
  /** mean − SD … mean + SD across 3 trial-level means */
  sdBand: readonly [number, number];
  featured?: boolean;
}) {
  const chance = 0.437;
  const max = 0.6;
  const x = (value: number) => `${(value / max) * 100}%`;
  return (
    <div
      className={`grid grid-cols-[1fr_auto] items-center gap-x-4 gap-y-2 rounded-xl p-3 sm:grid-cols-[11rem_minmax(0,1fr)_5rem] sm:p-4 ${
        featured ? "bg-indigo-50/70" : "bg-zinc-50"
      }`}
    >
      <div className="sm:col-start-1 sm:row-start-1">
        <h3 className="font-semibold text-zinc-900">{label}</h3>
        <p className="mt-0.5 text-xs leading-5 text-zinc-500">{note}</p>
      </div>
      <div
        className="relative col-span-2 row-start-2 h-10 overflow-visible sm:col-span-1 sm:col-start-2 sm:row-start-1"
        role="img"
        aria-label={`${label}: ${pct(rate)} mean Jaccard over 3 trials; error bars ±1 standard deviation over 3 trials from ${pct(sdBand[0])} to ${pct(sdBand[1])}; chance is about 43.7% (always predict steer)`}
      >
        <div className="absolute inset-x-0 top-1/2 h-3 -translate-y-1/2 rounded-full bg-zinc-200" />
        <div
          className={`absolute left-0 top-1/2 h-3 -translate-y-1/2 rounded-full ${
            featured ? "bg-indigo-600" : "bg-zinc-600"
          }`}
          style={{ width: x(rate) }}
        />
        <span
          className="absolute inset-y-1 z-20 w-0.5 bg-amber-600"
          style={{ left: x(chance) }}
          aria-hidden="true"
        />
        <span
          className="absolute top-1/2 z-30 h-0.5 -translate-y-1/2 bg-zinc-950"
          style={{ left: x(sdBand[0]), width: x(sdBand[1] - sdBand[0]) }}
          aria-hidden="true"
        >
          <span className="absolute -left-px top-1/2 h-4 w-0.5 -translate-y-1/2 bg-zinc-950" />
          <span className="absolute -right-px top-1/2 h-4 w-0.5 -translate-y-1/2 bg-zinc-950" />
        </span>
        <span
          className="absolute top-1/2 z-40 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-zinc-950 shadow-sm"
          style={{ left: x(rate) }}
          aria-hidden="true"
        />
      </div>
      <p className="col-start-2 row-start-1 text-right text-2xl font-semibold tracking-tight tabular-nums text-zinc-950 sm:col-start-3">
        {pct(rate)}
      </p>
    </div>
  );
}

/** Primary result: one model, two conditions, current multilabel scoring. */
export function LeaderboardSection() {
  return (
    <>
      <header className="mt-10 max-w-3xl sm:mt-12">
        <h1 className="text-4xl font-semibold tracking-[-0.035em] text-zinc-950 sm:text-6xl sm:leading-[1.02]">
          How well can agents simulate users?
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-600">
          UserBench tests whether an agent can predict what a real developer
          will do next in a coding session. The main score is Jaccard (IoU).
        </p>
      </header>

      <section
        id="leaderboard"
        aria-labelledby="leaderboard-title"
        className="mt-14 scroll-mt-20"
      >
        <div className="flex flex-col gap-5 border-b border-zinc-200 pb-7 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
              Primary result
            </p>
            <SectionHeading
              id="leaderboard"
              label="leaderboard"
              className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950 sm:text-3xl"
            >
              Training history lifts baseline above chance
            </SectionHeading>
            <p className="mt-2 text-sm text-zinc-500">
              GPT-5.6 Sol (high) · mean Jaccard over 3 trials × 620 tasks
            </p>
          </div>
          <div className="sm:text-right">
            <p className="text-4xl font-semibold tracking-tight tabular-nums text-indigo-700">
              +{ML.liftPp.toFixed(2)} pp
            </p>
            <p className="mt-1 text-sm text-zinc-500">train400 vs baseline</p>
          </div>
        </div>

        <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-4 sm:p-6">
          <div className="space-y-3">
            <ScoreRow
              label="Baseline"
              note="No developer training history"
              rate={ML.baseline.jaccard}
              sdBand={ML.baseline.sdBand}
            />
            <ScoreRow
              label="Train400"
              note="400 prior turns from the same developer"
              rate={ML.train400.jaccard}
              sdBand={ML.train400.sdBand}
              featured
            />
          </div>
          <div className="mt-2 hidden grid-cols-[11rem_minmax(0,1fr)_5rem] px-4 text-[11px] tabular-nums text-zinc-400 sm:grid">
            <span />
            <div className="flex justify-between">
              <span>0%</span>
              <span>20%</span>
              <span>40%</span>
              <span>60%</span>
            </div>
            <span />
          </div>
          <div className="mt-4 flex flex-wrap gap-x-5 gap-y-2 border-t border-zinc-100 pt-4 text-xs text-zinc-500">
            <span>
              <span className="mr-2 inline-block h-3 w-0.5 bg-amber-600 align-[-2px]" />
              Chance ≈43.7% (always predict {"{steer}"})
            </span>
            <span>
              <span className="mr-2 inline-block h-0.5 w-5 bg-zinc-950 align-middle" />
              Error bars show ±1 SD over 3 trials
            </span>
          </div>
        </div>
        <div className="mt-4 text-sm text-zinc-600">
          <p className="tabular-nums">
            Lift (means of 3 trials):{" "}
            <strong className="text-zinc-800">+{ML.liftPp.toFixed(2)} pp</strong>
          </p>
        </div>

      </section>
    </>
  );
}

const LENGTH_ROWS = [
  { label: "Real turn", value: 53, color: "bg-zinc-900" },
  { label: "Baseline", value: 32.5, color: "bg-zinc-500" },
  { label: "Train400", value: 29.5, color: "bg-indigo-600" },
] as const;

const ACT_ROWS = [
  { label: "approve", gold: 28.4, baseline: 52.7, train400: 49.0 },
  { label: "critical", gold: 21.5, baseline: 15.8, train400: 16.1 },
  { label: "steer", gold: 56.1, baseline: 46.9, train400: 48.4 },
  { label: "inquiry", gold: 27.7, baseline: 10.8, train400: 14.2 },
] as const;

function LengthChart() {
  return (
    <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
      <figcaption className="font-semibold text-zinc-900">
        Predicted turns stay shorter
      </figcaption>
      <p className="mt-1 text-xs text-zinc-500">Median characters per turn</p>
      <div className="mt-5 space-y-3">
        {LENGTH_ROWS.map((row) => (
          <div
            key={row.label}
            className="grid grid-cols-[5rem_minmax(0,1fr)_3rem] items-center gap-3 text-xs"
          >
            <span className="text-zinc-600">{row.label}</span>
            <div className="h-3 rounded-full bg-zinc-100">
              <div
                className={`h-3 rounded-full ${row.color}`}
                style={{ width: `${(row.value / 60) * 100}%` }}
              />
            </div>
            <span className="text-right font-medium tabular-nums text-zinc-800">
              {row.value}
            </span>
          </div>
        ))}
      </div>
      <p className="mt-5 text-sm leading-6 text-zinc-600">
        The median absolute length gap changes little: 36 characters at
        baseline and 35 with train400. Training history does not make output
        length much more human-like.
      </p>
    </figure>
  );
}

function ActMixChart() {
  return (
    <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
      <figcaption className="font-semibold text-zinc-900">
        Training narrows the act-mix gap
      </figcaption>
      <p className="mt-1 text-xs text-zinc-500">
        Share of 620 turns containing each act
      </p>
      <div className="mt-5 space-y-4">
        {ACT_ROWS.map((row) => (
          <div key={row.label}>
            <div className="mb-1.5 flex items-center justify-between text-xs">
              <span className="font-mono text-zinc-700">{row.label}</span>
              <span className="text-zinc-400">0–60%</span>
            </div>
            <div
              className="space-y-1"
              role="img"
              aria-label={`${row.label}: gold ${row.gold}%, baseline ${row.baseline}%, train400 ${row.train400}%`}
            >
              {(
                [
                  ["Gold", row.gold, "bg-zinc-900"],
                  ["Baseline", row.baseline, "bg-zinc-400"],
                  ["Train400", row.train400, "bg-indigo-600"],
                ] as const
              ).map(([label, value, color]) => (
                <div
                  key={label}
                  className="grid grid-cols-[3.5rem_minmax(0,1fr)_2.75rem] items-center gap-2 text-[11px]"
                >
                  <span className="text-zinc-500">{label}</span>
                  <div className="h-1.5 rounded-full bg-zinc-100">
                    <div
                      className={`h-1.5 rounded-full ${color}`}
                      style={{ width: `${(value / 60) * 100}%` }}
                    />
                  </div>
                  <span className="text-right tabular-nums text-zinc-600">
                    {value.toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="mt-5 text-sm leading-6 text-zinc-600">
        Both conditions overpredict approval and miss inquiries. Train400 cuts
        those two gaps by about 3 percentage points each.
      </p>
    </figure>
  );
}

function TaskDeltaChart() {
  const total = 620;
  const segments = [
    { label: "Improved", value: 135, color: "bg-indigo-600" },
    { label: "Tied", value: 384, color: "bg-zinc-300" },
    { label: "Worsened", value: 101, color: "bg-rose-400" },
  ] as const;
  return (
    <figure className="rounded-2xl border border-zinc-200 bg-white p-5 sm:col-span-2">
      <figcaption className="font-semibold text-zinc-900">
        Most tasks tie; gains outnumber losses
      </figcaption>
      <div
        className="mt-5 flex h-5 overflow-hidden rounded-full"
        role="img"
        aria-label="Task-level Jaccard change: 135 improved, 384 tied, 101 worsened"
      >
        {segments.map((segment) => (
          <span
            key={segment.label}
            className={segment.color}
            style={{ width: `${(segment.value / total) * 100}%` }}
          />
        ))}
      </div>
      <div className="mt-4 grid grid-cols-3 gap-3">
        {segments.map((segment) => (
          <div key={segment.label}>
            <p className="text-xl font-semibold tabular-nums text-zinc-950">
              {segment.value}
            </p>
            <p className="text-xs text-zinc-500">{segment.label}</p>
          </div>
        ))}
      </div>
      <p className="mt-5 text-sm leading-6 text-zinc-600">
        Train400 improves Jaccard on 135 tasks and worsens it on 101; the other
        384 are unchanged. The mean gain comes from a minority of tasks.
      </p>
    </figure>
  );
}

function QualitativeComparison() {
  return (
    <article className="rounded-2xl border border-zinc-200 bg-white p-5 sm:col-span-2 sm:p-6">
      <h3 className="font-semibold text-zinc-950">When history helps</h3>
      <p className="mt-2 text-sm leading-6 text-zinc-600">
        The agent proposed shrinking several leaderboard elements; the
        developer&apos;s next turn pushed back on making everything smaller.
      </p>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl bg-zinc-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
            No history
          </p>
          <blockquote className="mt-3 text-sm leading-6 text-zinc-700">
            “yeah go ahead and apply it”
          </blockquote>
          <div className="mt-4 flex flex-wrap items-center gap-2">
            <LabelChip label="approve" />
            <span className="ml-auto text-sm font-semibold tabular-nums text-rose-700">
              Jaccard 0
            </span>
          </div>
        </div>
        <div className="rounded-xl bg-indigo-50/70 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
            400 prior turns
          </p>
          <blockquote className="mt-3 text-sm leading-6 text-zinc-700">
            “wait i dont want everything to be smaller..the second image still
            has big text. i want more spacing and balance so it doesnt feel like
            everything is crowded at the top”
          </blockquote>
          <div className="mt-4 flex flex-wrap items-center gap-2">
            <LabelChip label="critical" />
            <LabelChip label="steer" />
            <span className="ml-auto text-sm font-semibold tabular-nums text-indigo-700">
              Jaccard 1
            </span>
          </div>
        </div>
      </div>
      <div className="mt-4 border-l-2 border-zinc-300 pl-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Real next turn
        </p>
        <blockquote className="mt-2 text-sm leading-6 text-zinc-700">
          “i dont think thats part of the overcrowding to be honest..i think the
          letters might be a little too big and the the section where it says i
          got to level 1 2/5 20..thats way too much”
        </blockquote>
        <div className="mt-3 flex flex-wrap gap-2">
          <LabelChip label="critical" />
          <LabelChip label="steer" />
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-zinc-600">
        With history, the model captured both the correction and the requested
        direction. This case illustrates the pattern; the 620-task comparison
        above measures it.
      </p>
    </article>
  );
}

export function AnalysisSection() {
  return (
    <Section
      id="analysis"
      kicker="Results analysis"
      title="Where the modest gain comes from"
    >
      <p className="max-w-3xl text-sm leading-6 text-zinc-600">
        Baseline sits near chance. Four hundred prior turns raise mean Jaccard
        by {ML.liftPp.toFixed(2)} points (mean of 3 trials), with small shifts
        in act choice and many unchanged tasks.
      </p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <LengthChart />
        <ActMixChart />
        <TaskDeltaChart />
        <QualitativeComparison />
      </div>
    </Section>
  );
}

export function RunDetailsSection() {
  return (
    <Section
      id="run-details"
      kicker="Runs and reproducibility"
      title="Run details"
    >
      <div className="grid items-start gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">Scores</h3>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[22rem] text-sm tabular-nums">
              <thead>
                <tr className="border-b border-zinc-100 text-right text-xs text-zinc-500">
                  <th className="pb-2 text-left font-medium">Metric</th>
                  <th className="pb-2 font-medium">Baseline</th>
                  <th className="pb-2 font-medium">Train400</th>
                </tr>
              </thead>
              <tbody className="text-right text-zinc-700">
                {(
                  [
                    ["Mean Jaccard", ML.baseline.jaccard, ML.train400.jaccard],
                    ["Exact-set match", ML.baseline.exact, ML.train400.exact],
                    ["Jaccard chance", ML.baseline.chance, ML.train400.chance],
                    [
                      "Exact-set chance",
                      ML.baseline.exactChance,
                      ML.train400.exactChance,
                    ],
                    ["Macro-F1", ML.baseline.macroF1, ML.train400.macroF1],
                  ] as const
                ).map(([label, baseline, train400]) => (
                  <tr key={label} className="border-b border-zinc-100 last:border-0">
                    <th className="py-2.5 pr-4 text-left font-medium text-zinc-600">
                      {label}
                    </th>
                    <td className="py-2.5">{pct(baseline)}</td>
                    <td className="py-2.5">{pct(train400)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-xs leading-5 text-zinc-500">
            Leaderboard means are averages over 3 trials. SD over those 3
            trial means: baseline ±{(100 * ML.baseline.trialSd).toFixed(2)} pp,
            train400 ±{(100 * ML.train400.trialSd).toFixed(2)} pp. Lift: +
            {ML.liftPp.toFixed(2)} pp.
          </p>
        </div>
        <div className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">Public artifacts</h3>
          <div className="mt-4 space-y-4 text-sm text-zinc-600">
            <div>
              <p className="font-medium text-zinc-800">Datasets</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={DATASET}>Baseline dataset ↗</ExtLink>
                <ExtLink href={DATASET_TRAIN}>Train400 dataset ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Baseline</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT.baseline3x}>Agent traces ↗</ExtLink>
                <ExtLink href={ML.baseline.hub}>Judge traces ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Train400</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT.train4003x}>Agent traces ↗</ExtLink>
                <ExtLink href={ML.train400.hub}>Judge traces ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Independent runs</p>
              <p className="mt-1.5">
                <ExtLink href={ML.archive3x.hub}>
                  Three-run judge traces ↗
                </ExtLink>{" "}
                <span className="text-xs text-zinc-500">
                  ({ML.archive3x.n.toLocaleString()} scored turns)
                </span>
              </p>
            </div>
          </div>
          <p className="mt-5 border-t border-zinc-100 pt-4 text-xs leading-5 text-zinc-500">
            Composer 2.5 assigns approve, critical, steer, and inquiry act sets
            across 620 held-out tasks per condition.
          </p>
        </div>
      </div>
    </Section>
  );
}

export function DatasetHubLinks() {
  return (
    <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-5 sm:flex sm:items-center sm:justify-between sm:gap-8">
      <div>
        <h3 className="font-semibold text-zinc-900">Two public dataset views</h3>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-600">
          Both use the same 620 held-out turns. Train400 adds 400 earlier turns
          from each developer as context.
        </p>
      </div>
      <div className="mt-4 flex shrink-0 flex-wrap gap-4 text-sm sm:mt-0">
        <ExtLink href={DATASET}>{DATASET_REF} ↗</ExtLink>
        <ExtLink href={DATASET_TRAIN}>{DATASET_TRAIN_REF} ↗</ExtLink>
      </div>
    </div>
  );
}

const LABEL_STYLES = {
  approve: "border-emerald-200 bg-emerald-50 text-emerald-800",
  critical: "border-rose-200 bg-rose-50 text-rose-800",
  steer: "border-sky-200 bg-sky-50 text-sky-800",
  inquiry: "border-violet-200 bg-violet-50 text-violet-800",
};

function LabelChip({ label }: { label: keyof typeof LABEL_STYLES }) {
  return (
    <span
      className={`rounded-full border px-2.5 py-1 font-mono text-xs font-medium ${LABEL_STYLES[label]}`}
    >
      {label}
    </span>
  );
}

export function LabelExamplesSection() {
  return (
    <section
      id="labels"
      aria-labelledby="labels-title"
      className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
        The labels
      </p>
      <SectionHeading
        id="labels"
        label="labels"
        className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
      >
        One turn can do more than one thing
      </SectionHeading>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-600">
        <strong className="text-zinc-800">approve</strong> accepts,{" "}
        <strong className="text-zinc-800">critical</strong> flags a problem,{" "}
        <strong className="text-zinc-800">steer</strong> directs the next step,
        and <strong className="text-zinc-800">inquiry</strong> asks for
        information.
      </p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
          <blockquote className="text-sm leading-6 text-zinc-700">
            “1, should be fixed from the pyproject.toml and not uv.lock. 4, yes.
            5, yes.”
          </blockquote>
          <figcaption className="mt-4 flex flex-wrap items-center gap-2">
            <span className="mr-1 text-xs font-medium text-zinc-500">
              Kevin:
            </span>
            <LabelChip label="approve" />
            <LabelChip label="steer" />
          </figcaption>
        </figure>
        <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
          <blockquote className="text-sm leading-6 text-zinc-700">
            “I do not see the changes, did you build the extension?”
          </blockquote>
          <figcaption className="mt-4 flex flex-wrap items-center gap-2">
            <span className="mr-1 text-xs font-medium text-zinc-500">
              Kevin:
            </span>
            <LabelChip label="critical" />
            <LabelChip label="inquiry" />
          </figcaption>
        </figure>
      </div>
      <div className="mt-4 text-sm leading-6 text-zinc-600">
        <p>
          A turn can approve one choice and steer another, so one label would
          drop part of the intent.
        </p>
      </div>
      <div className="mt-6 max-w-3xl rounded-2xl border border-zinc-200 bg-white p-5 text-sm leading-6 text-zinc-600">
        <h3 className="font-semibold text-zinc-900">How Jaccard scores a turn</h3>
        <p className="mt-2">
          Each turn can carry more than one act. Jaccard = |intersection| /
          |union| of the predicted and gold sets. Gold{" "}
          <span className="font-mono text-xs text-zinc-700">
            {"{approve, steer}"}
          </span>{" "}
          vs pred{" "}
          <span className="font-mono text-xs text-zinc-700">{"{approve}"}</span>{" "}
          → 1/2 = 50% (exact match would be 0). The leaderboard is the mean of
          that score over 620 turns.
        </p>
        <p className="mt-3">
          Chance always predicts the most common gold set,{" "}
          <span className="font-mono text-xs text-zinc-700">{"{steer}"}</span>
          ; that baseline is about 43.7%.
        </p>
      </div>
      <aside className="mt-6 flex flex-col gap-4 border-l-2 border-indigo-500 bg-indigo-50/60 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="font-semibold text-zinc-950">
            Composer closely matches Kevin&apos;s labels
          </h3>
          <p className="mt-1 text-2xl font-semibold tracking-tight text-indigo-700">
            81% Jaccard agreement
          </p>
          <p className="mt-1 text-sm text-zinc-600">
            64% exact-set agreement across 50 co-labeled turns.{" "}
            <span className="text-zinc-500">Agreement, not accuracy.</span>
          </p>
        </div>
        <a
          href="/annotator/dashboard"
          className="shrink-0 font-medium text-indigo-600 underline-offset-4 hover:underline"
        >
          Open the public annotator dashboard →
        </a>
      </aside>
    </section>
  );
}
