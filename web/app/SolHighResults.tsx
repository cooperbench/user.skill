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
    // Sol-high: 1860 trials; Avg reward = multilabel Jaccard (not exact-match 0/1)
    baseline:
      "https://hub.harborframework.com/jobs/14a20479-5716-4ed6-b3ec-3f4d772d9d34",
    train400:
      "https://hub.harborframework.com/jobs/dc87831c-402b-4d3a-b5ce-9ef4d039bb4a",
  },
  judgeTraces: {
    baseline:
      "https://hub.harborframework.com/jobs/722b2a3b-032b-494b-96f6-b8febdb54f4f",
    train400:
      "https://hub.harborframework.com/jobs/8ab68c38-f335-4adc-90b8-e833f5bc2aa2",
  },
  // Sol-low: 1×620; same multilabel Jaccard scoring
  agentTracesLow: {
    baseline:
      "https://hub.harborframework.com/jobs/fca0f1bb-87d0-4c5e-94e3-3a1e266efdf7",
    train400:
      "https://hub.harborframework.com/jobs/2947aead-6b34-4a6e-a0f4-30d84af7e655",
  },
  judgeTracesLow: {
    baseline:
      "https://hub.harborframework.com/jobs/91587726-5621-4a54-9659-b1ff343dfc4a",
    train400:
      "https://hub.harborframework.com/jobs/61078e64-1a3a-459c-b7bc-96e61caad127",
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
 * Leaderboard point: mean over tasks of (mean Jaccard across 3 trials).
 * Error bars: bootstrap 95% CI over the 620 per-task means (10k
 * percentile bootstrap of the mean). See THREE_TRIAL_JACCARD.json.
 */
const ML = {
  baseline: {
    jaccard: 0.445,
    /** Bootstrap 95% CI over 620 per-task means (each task = mean of 3 trials). */
    ci: [0.415, 0.474] as const,
    exact: 0.306,
    exactChance: 0.326,
    nExact: 190,
    chance: 0.439,
    vsChancePp: 0.6,
    macroF1: 0.439,
    n: 1860,
    hub: HUB_URLS.judgeTraces.baseline,
  },
  train400: {
    jaccard: 0.494,
    ci: [0.463, 0.524] as const,
    exact: 0.35,
    exactChance: 0.324,
    nExact: 217,
    chance: 0.434,
    vsChancePp: 4.6,
    macroF1: 0.468,
    n: 1860,
    hub: HUB_URLS.judgeTraces.train400,
  },
  /** train400 − baseline, from means of 3 trials. */
  liftPp: 4.89,
};

/**
 * Sol-low (reasoning_effort=low): 1 trial × 620 per arm.
 * No bootstrap CI / 3-trial SD — single-trial means only.
 * Source: jobs/sol-low-userbench/STATUS.md + REASONING_EFFORT_ANALYSIS.md
 */
const ML_LOW = {
  baseline: { jaccard: 0.4543, exact: 0.3274 },
  train400: { jaccard: 0.4591, exact: 0.3355 },
  liftPp: 0.48,
  nTrialsLabel: "1 trial × 620 tasks",
} as const;

/**
 * Sol-max (reasoning_effort=max): Train400 only, 1×620.
 * No baseline-max arm; no public Hub job yet.
 * Source: jobs/sol-max-userbench/STATUS.md (mean 0.5048387…; exact 0.377419…).
 * vsHighPp = max − Sol-high train400 mean-of-3 (0.493862…); not significant.
 */
const ML_MAX = {
  train400: { jaccard: 0.5048, exact: 0.3774 },
  /** vs Sol-high train400 mean-of-3 (49.39%). */
  vsHighPp: 1.1,
  nTrialsLabel: "1 trial × 620 tasks",
  highTrain400MeanOf3: 0.4939,
} as const;

/**
 * Trajectory cohort (active trials): sol-high / sol-low / sol-max train400.
 * Method: AGENT_READ_PATTERNS (active = ≥1 agent step + ≥1 tool call).
 * Max source: jobs/sol-max-userbench/MAX_READ_DEPTH.json (sol-max-full-train400).
 */
const EFFORT_TRAJ = {
  high: {
    tools: 15.8,
    steps: 7.7,
    trainCmds: 9.4,
    poolScanPct: 99.6,
    trainObsK: 73,
    inputTokensK: 182,
    overApprovePp: 21.0,
  },
  low: {
    tools: 7.3,
    steps: 5.2,
    trainCmds: 3.3,
    poolScanPct: 76.1,
    trainObsK: 26,
    inputTokensK: 52,
    overApprovePp: 24.0,
  },
  max: {
    tools: 20.1,
    steps: 9.2,
    trainCmds: 12.8,
    poolScanPct: 99.7,
    trainObsK: 109,
    inputTokensK: 310,
    overApprovePp: 19.0,
  },
} as const;

/** Agent-trial Hub jobs (gpt-5.6-sol trajectories). */
const AGENT = {
  baseline3x: HUB_URLS.agentTraces.baseline,
  train4003x: HUB_URLS.agentTraces.train400,
};

/** Sol-low (reasoning_effort=low) public Hub traces — 1×620. */
const AGENT_LOW = {
  baseline: HUB_URLS.agentTracesLow.baseline,
  train400: HUB_URLS.agentTracesLow.train400,
};
const JUDGE_LOW = {
  baseline: HUB_URLS.judgeTracesLow.baseline,
  train400: HUB_URLS.judgeTracesLow.train400,
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
  ci,
  featured = false,
  trialsNote = "3 trials × 620 tasks",
  digits = 1,
}: {
  label: string;
  note: string;
  rate: number;
  /** Bootstrap 95% CI over 620 per-task means; omit for single-trial rows */
  ci?: readonly [number, number];
  featured?: boolean;
  trialsNote?: string;
  /** Percent display digits (default 1; max uses 2 for 50.48%). */
  digits?: number;
}) {
  const chance = 0.437;
  const max = 0.6;
  const x = (value: number) => `${(value / max) * 100}%`;
  const aria = ci
    ? `${label}: ${pct(rate, digits)} mean Jaccard over ${trialsNote}; bootstrap 95% confidence interval ${pct(ci[0])} to ${pct(ci[1])}; chance is about 43.7% (always predict steer)`
    : `${label}: ${pct(rate, digits)} mean Jaccard over ${trialsNote}; no multi-trial confidence interval; chance is about 43.7% (always predict steer)`;
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
        aria-label={aria}
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
        {ci && (
          <span
            className="absolute top-1/2 z-30 h-0.5 -translate-y-1/2 bg-zinc-950"
            style={{ left: x(ci[0]), width: x(ci[1] - ci[0]) }}
            aria-hidden="true"
          >
            <span className="absolute -left-px top-1/2 h-4 w-0.5 -translate-y-1/2 bg-zinc-950" />
            <span className="absolute -right-px top-1/2 h-4 w-0.5 -translate-y-1/2 bg-zinc-950" />
          </span>
        )}
        <span
          className="absolute top-1/2 z-40 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-zinc-950 shadow-sm"
          style={{ left: x(rate) }}
          aria-hidden="true"
        />
      </div>
      <p className="col-start-2 row-start-1 text-right text-2xl font-semibold tracking-tight tabular-nums text-zinc-950 sm:col-start-3">
        {pct(rate, digits)}
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
              Conditioning on past sessions lifts baseline above chance
            </SectionHeading>
            <p className="mt-2 text-sm text-zinc-500">
              GPT-5.6 Sol (high) · mean Jaccard over 3 trials × 620 tasks
            </p>
          </div>
          <div className="sm:text-right">
            <p className="text-4xl font-semibold tracking-tight tabular-nums text-indigo-700">
              +{ML.liftPp.toFixed(1)} pp
            </p>
            <p className="mt-1 text-sm text-zinc-500">train400 vs baseline</p>
          </div>
        </div>

        <div className="mt-6 rounded-2xl border border-zinc-200 bg-white p-4 sm:p-6">
          <div className="space-y-3">
            <ScoreRow
              label="Baseline · high"
              note="No developer training history · effort high"
              rate={ML.baseline.jaccard}
              ci={ML.baseline.ci}
            />
            <ScoreRow
              label="Train400 · high"
              note="400 prior turns · effort high · primary"
              rate={ML.train400.jaccard}
              ci={ML.train400.ci}
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
              Error bars (high only): bootstrap 95% CIs over 620 tasks (10k
              resamples; each task = mean of 3 trials)
            </span>
          </div>
        </div>

        <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-4 sm:p-6">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
                Same model · effort low
              </p>
              <p className="mt-1 text-sm text-zinc-600">
                GPT-5.6 Sol (low) · {ML_LOW.nTrialsLabel} · no multi-trial CI
              </p>
            </div>
            <div className="sm:text-right">
              <p className="text-2xl font-semibold tracking-tight tabular-nums text-zinc-700">
                +{ML_LOW.liftPp.toFixed(1)} pp
              </p>
              <p className="text-xs text-zinc-500">train400 vs baseline</p>
            </div>
          </div>
          <div className="mt-4 space-y-3">
            <ScoreRow
              label="Baseline · low"
              note="No developer training history · effort low"
              rate={ML_LOW.baseline.jaccard}
              trialsNote={ML_LOW.nTrialsLabel}
            />
            <ScoreRow
              label="Train400 · low"
              note="400 prior turns · effort low"
              rate={ML_LOW.train400.jaccard}
              trialsNote={ML_LOW.nTrialsLabel}
            />
          </div>
          <p className="mt-4 border-t border-zinc-100 pt-4 text-xs leading-5 text-zinc-500">
            At low effort, baseline stays near high ({pct(ML_LOW.baseline.jaccard)}{" "}
            vs {pct(ML.baseline.jaccard)}), but train400 barely moves (+
            {ML_LOW.liftPp.toFixed(1)} pp vs +{ML.liftPp.toFixed(1)} pp). See{" "}
            <a
              href="#reasoning-effort"
              className="text-indigo-600 underline-offset-2 hover:underline"
            >
              impact of reasoning effort
            </a>
            .
          </p>
        </div>

        <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-4 sm:p-6">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
                Same model · effort max
              </p>
              <p className="mt-1 text-sm text-zinc-600">
                GPT-5.6 Sol (max) · {ML_MAX.nTrialsLabel} · train400 only · no
                multi-trial CI
              </p>
            </div>
            <div className="sm:text-right">
              <p className="text-2xl font-semibold tracking-tight tabular-nums text-zinc-700">
                +{ML_MAX.vsHighPp.toFixed(1)} pp
              </p>
              <p className="text-xs text-zinc-500">vs high train400</p>
            </div>
          </div>
          <div className="mt-4 space-y-3">
            <ScoreRow
              label="Train400 · max"
              note="400 prior turns · effort max · no baseline arm"
              rate={ML_MAX.train400.jaccard}
              trialsNote={ML_MAX.nTrialsLabel}
              digits={2}
            />
          </div>
          <p className="mt-4 border-t border-zinc-100 pt-4 text-xs leading-5 text-zinc-500">
            Max reaches {pct(ML_MAX.train400.jaccard, 2)} on train400 vs{" "}
            {pct(ML_MAX.highTrain400MeanOf3, 2)} high (mean of 3) — about +
            {ML_MAX.vsHighPp.toFixed(1)} pp, not significant. Exact-set{" "}
            {pct(ML_MAX.train400.exact)}. One unrecovered AgentTimeoutError; no
            baseline-max run. See{" "}
            <a
              href="#reasoning-effort"
              className="text-indigo-600 underline-offset-2 hover:underline"
            >
              impact of reasoning effort
            </a>
            .
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
        in act choice and many unchanged tasks. For a step-by-step look at how
        the agent spends its tools, see{" "}
        <a
          href="#sessions"
          className="text-indigo-600 underline-offset-2 hover:underline"
        >
          typical sessions
        </a>
        . For low / high / max effort on the same tasks, see{" "}
        <a
          href="#reasoning-effort"
          className="text-indigo-600 underline-offset-2 hover:underline"
        >
          reasoning effort
        </a>
        .
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

/** Low / high / max effort: scores + train400 read depth. */
export function ReasoningEffortSection() {
  const rows = [
    {
      label: "Mean tools",
      high: String(EFFORT_TRAJ.high.tools),
      low: String(EFFORT_TRAJ.low.tools),
      max: String(EFFORT_TRAJ.max.tools),
    },
    {
      label: "Mean train cmds",
      high: String(EFFORT_TRAJ.high.trainCmds),
      low: String(EFFORT_TRAJ.low.trainCmds),
      max: String(EFFORT_TRAJ.max.trainCmds),
    },
    {
      label: "Search coverage",
      high: `${EFFORT_TRAJ.high.poolScanPct}%`,
      low: `${EFFORT_TRAJ.low.poolScanPct}%`,
      max: `${EFFORT_TRAJ.max.poolScanPct}%`,
    },
    {
      label: "Train obs (mean)",
      high: `~${EFFORT_TRAJ.high.trainObsK}kB`,
      low: `~${EFFORT_TRAJ.low.trainObsK}kB`,
      max: `~${EFFORT_TRAJ.max.trainObsK}kB`,
    },
    {
      label: "Input tokens (mean)",
      high: `~${EFFORT_TRAJ.high.inputTokensK}k`,
      low: `~${EFFORT_TRAJ.low.inputTokensK}k`,
      max: `~${EFFORT_TRAJ.max.inputTokensK}k`,
    },
    {
      label: "Over-approve gap",
      high: `+${EFFORT_TRAJ.high.overApprovePp.toFixed(0)} pp`,
      low: `+${EFFORT_TRAJ.low.overApprovePp.toFixed(0)} pp`,
      max: `+${EFFORT_TRAJ.max.overApprovePp.toFixed(0)} pp`,
    },
  ] as const;

  return (
    <Section
      id="reasoning-effort"
      kicker="Ablation"
      title="Impact of reasoning effort"
    >
      <ul className="max-w-3xl list-disc space-y-2 pl-5 text-sm leading-6 text-zinc-700">
        <li>
          Baseline is about the same at low vs high (
          {pct(ML_LOW.baseline.jaccard)} vs {pct(ML.baseline.jaccard)}; chance
          ≈43.7%). No baseline-max arm was run.
        </li>
        <li>
          Train400 lift is flat at low (+{ML_LOW.liftPp.toFixed(1)} pp), clear at
          high (+{ML.liftPp.toFixed(1)} pp; 3-trial means), and max adds a small
          further bump on train400 only: {pct(ML_MAX.train400.jaccard, 2)} vs{" "}
          {pct(ML_MAX.highTrain400MeanOf3, 2)} high (+{ML_MAX.vsHighPp.toFixed(1)}{" "}
          pp; not significant).
        </li>
        <li>
          Effort matters more for using history than for cold next-act: low
          still opens{" "}
          <span className="font-mono text-xs">/sim/train</span> on every
          active trial, but runs fewer tools and weaker pool scans. Max does not
          clearly beat high on this 1×620 pass.
        </li>
      </ul>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">
            Train400 read depth (active trials)
          </h3>
          <p className="mt-1 text-xs text-zinc-500">
            Same held-out tasks. Low: 620 of 620. High: 1,587 active of 1,860.
            Max: 620 of 620. Active = ≥1 agent step + ≥1 tool call. Search
            coverage = share of active trials with a pool-wide search over{" "}
            <span className="font-mono">/sim/train</span> (grep/glob/listdir),
            not just opening a named session file.
          </p>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[22rem] text-sm tabular-nums">
              <thead>
                <tr className="border-b border-zinc-100 text-right text-xs text-zinc-500">
                  <th className="pb-2 text-left font-medium">Metric</th>
                  <th className="pb-2 font-medium">Low</th>
                  <th className="pb-2 font-medium">High</th>
                  <th className="pb-2 font-medium">Max</th>
                </tr>
              </thead>
              <tbody className="text-right text-zinc-700">
                {rows.map((row) => (
                  <tr
                    key={row.label}
                    className="border-b border-zinc-100 last:border-0"
                  >
                    <th className="py-2 pr-4 text-left font-medium text-zinc-600">
                      {row.label}
                    </th>
                    <td className="py-2">{row.low}</td>
                    <td className="py-2">{row.high}</td>
                    <td className="py-2">{row.max}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-xs leading-5 text-zinc-500">
            Low also shifts strategy: more often reads the train index then a
            few named sessions (22% vs &lt;1%), with less pack-wide search. Max
            reads deeper than high (more tools and tokens) with similar search
            coverage. Over-approve barely moves.
          </p>
        </div>

        <article className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">
            Same task, different effort
          </h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            <span className="font-mono text-xs text-zinc-700">
              admarble__dbb54fbd
            </span>
            : gold next turn is a short approve (“proceed”). High train400
            pool-scans interruption phrasing and answers correctly; low skims
            the index, then steers to “docs 574”.
          </p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl bg-indigo-50/70 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                High · train400
              </p>
              <p className="mt-2 text-xs leading-5 text-zinc-600">
                11 tools · 8 train cmds · pool-scan
              </p>
              <blockquote className="mt-3 text-sm leading-6 text-zinc-700">
                “proceed”
              </blockquote>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <LabelChip label="approve" />
                <span className="ml-auto text-sm font-semibold tabular-nums text-indigo-700">
                  J ↑
                </span>
              </div>
            </div>
            <div className="rounded-xl bg-zinc-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Low · train400
              </p>
              <p className="mt-2 text-xs leading-5 text-zinc-600">
                5 tools · 3 train cmds · thinner scan
              </p>
              <blockquote className="mt-3 text-sm leading-6 text-zinc-700">
                “docs 574”
              </blockquote>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <LabelChip label="steer" />
                <span className="ml-auto text-sm font-semibold tabular-nums text-rose-700">
                  J 0
                </span>
              </div>
            </div>
          </div>
          <p className="mt-4 text-xs leading-5 text-zinc-500">
            Second pattern on{" "}
            <span className="font-mono">alishakawaguchi__bd8cd4f9</span>: both
            say “commit”, but low only reads the index and a few named sessions
            and loses the approve label that high recovers. One-trial anecdotes;
            the 620-task means above measure the gap.
          </p>
        </article>
      </div>
    </Section>
  );
}

/**
 * Cohort means over active Sol-high trajectories
 * (AGENT_READ_PATTERNS.json, distributions_active_only).
 * Baseline: 1860 active / 1860. Train400: 1587 active / 1860
 * (273 empty trajectories excluded from train means).
 */
const SESSION_COHORT = {
  baselineN: 1860,
  trainActiveN: 1587,
  trainSelectedN: 1860,
  steps: { baseline: 5.2, train400: 7.7 },
  tools: { baseline: 6.8, train400: 15.8 },
  inputTokensK: { baseline: 42, train400: 182 },
  tokenRatio: "4.3×",
  /** Active-trial means; leaderboard uses 3-trial task means (44.5% / 49.4%). */
  jaccard: { baseline: "0.44", train400: "0.50" },
  costUsd: { baseline: 0.14, train400: 0.45 },
  costRatio: "3×",
} as const;

/** Real Sol-high pair: median-like baseline vs index_then_pool_scan train400. */
const SESSION_PAIR = {
  taskKey: "melagiri__25b8f546",
  goldMsg:
    "create feature branch and work on it.. but before that, try looking for similar errors that we may have introduced recently due the changes we made to codebase",
  goldActs: ["approve", "steer"] as const,
  baseline: {
    trial: "melagiri__25b8f546__77edbTD",
    tools: 9,
    inputTokens: 40415,
    costUsd: 0.147,
    jaccard: 0.5,
    predMsg: "Fix both issues..",
    predActs: ["approve"] as const,
    strategy: "history only",
    /** One entry per agent turn (n_agent_steps in the source traj). */
    timeline: [
      {
        label: "Read history",
        kind: "history" as const,
        cmds: ["wc -l /sim/history.md && tail -n 240 /sim/history.md"],
      },
      {
        label: "Map roles + pages",
        kind: "history" as const,
        cmds: [
          "grep -n '^> ' /sim/history.md",
          "sed -n '320,430p' /sim/history.md",
          "sed -n '1,180p' /sim/history.md",
        ],
      },
      {
        label: "Finish the transcript",
        kind: "history" as const,
        cmds: [
          "nl -ba /sim/history.md | sed -n '180,397p'",
          "tail -c 3000 /sim/history.md | cat -A",
        ],
      },
      {
        label: "Write answer",
        kind: "answer" as const,
        cmds: ["printf '%s' 'Fix both issues..' > /sim/answer.txt"],
      },
      {
        label: "Submit",
        kind: "submit" as const,
        cmds: ["echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"],
      },
    ],
  },
  train400: {
    trial: "melagiri__25b8f546__JQBmNSy",
    tools: 16,
    inputTokens: 143151,
    costUsd: 0.373,
    jaccard: 1.0,
    predMsg: "fix both issues and add tests to cover them",
    predActs: ["approve", "steer"] as const,
    strategy: "index_then_pool_scan",
    namedSessions: 2,
    /** One entry per agent turn (n_agent_steps in the source traj). */
    timeline: [
      {
        label: "History + index",
        kind: "index" as const,
        cmds: [
          "wc -l /sim/history.md && tail -n 240 /sim/history.md",
          "cat /sim/train/_index.json",
        ],
      },
      {
        label: "Named session reads",
        kind: "named" as const,
        cmds: [
          "sed -n '300,397p' /sim/history.md",
          "cat /sim/train/4b4b6503-….md; cat /sim/train/8ce492ed-….md",
        ],
      },
      {
        label: "Finish history + skim pool",
        kind: "history" as const,
        cmds: [
          "sed -n '1,180p' /sim/history.md",
          "tail -c 3000 /sim/history.md | cat -A",
          "Path('/sim/train').glob('*.md')  # python skim of developer turns",
        ],
      },
      {
        label: "Pool-scan train/*.md",
        kind: "scan" as const,
        cmds: [
          "for f in /sim/train/*.md; do grep -H -A4 '^> DEVELOPER$' …",
          "python skim of last sessions + named sessions again",
        ],
      },
      {
        label: "Phrase hunt in pool",
        kind: "scan" as const,
        cmds: [
          "grep -Rin -E '^fix (it|them|both)|…|add tests' /sim/train/*.md",
        ],
      },
      {
        label: "Write answer",
        kind: "answer" as const,
        cmds: [
          "cat <<'EOF' > /sim/answer.txt  # fix both issues and add tests…",
        ],
      },
      {
        label: "Submit",
        kind: "submit" as const,
        cmds: ["echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"],
      },
    ],
  },
} as const;

const STEP_KIND_STYLE = {
  history: "bg-zinc-200 text-zinc-700",
  index: "bg-indigo-100 text-indigo-800",
  named: "bg-sky-100 text-sky-800",
  scan: "bg-amber-100 text-amber-900",
  answer: "bg-emerald-100 text-emerald-800",
  submit: "bg-zinc-100 text-zinc-500",
} as const;

function SessionTimeline({
  arm,
  featured = false,
}: {
  arm: typeof SESSION_PAIR.baseline | typeof SESSION_PAIR.train400;
  featured?: boolean;
}) {
  const isTrain = "namedSessions" in arm;
  const stepCount = arm.timeline.length;
  return (
    <article
      className={`rounded-2xl border p-5 ${
        featured
          ? "border-indigo-200 bg-indigo-50/40"
          : "border-zinc-200 bg-white"
      }`}
    >
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p
            className={`text-xs font-semibold uppercase tracking-wide ${
              featured ? "text-indigo-600" : "text-zinc-500"
            }`}
          >
            {isTrain ? "Train400" : "Baseline"}
          </p>
          <h3 className="mt-1 font-semibold text-zinc-950">{arm.strategy}</h3>
          <p className="mt-1 font-mono text-[11px] text-zinc-400">{arm.trial}</p>
        </div>
        <div className="text-right">
          <p
            className={`text-2xl font-semibold tabular-nums ${
              arm.jaccard === 1 ? "text-indigo-700" : "text-zinc-800"
            }`}
          >
            Jaccard {arm.jaccard === 1 ? "1" : arm.jaccard}
          </p>
          <p className="text-xs text-zinc-500">
            {stepCount} steps · {arm.tools} tools
          </p>
        </div>
      </header>

      <dl className="mt-4 grid grid-cols-3 gap-2 text-center">
        <div className="rounded-xl bg-white/80 px-2 py-2 ring-1 ring-zinc-200/80">
          <dt className="text-[10px] uppercase tracking-wide text-zinc-400">
            Input tok
          </dt>
          <dd className="mt-0.5 text-sm font-semibold tabular-nums text-zinc-900">
            {(arm.inputTokens / 1000).toFixed(0)}k
          </dd>
        </div>
        <div className="rounded-xl bg-white/80 px-2 py-2 ring-1 ring-zinc-200/80">
          <dt className="text-[10px] uppercase tracking-wide text-zinc-400">
            Cost
          </dt>
          <dd className="mt-0.5 text-sm font-semibold tabular-nums text-zinc-900">
            ${arm.costUsd.toFixed(2)}
          </dd>
        </div>
        <div className="rounded-xl bg-white/80 px-2 py-2 ring-1 ring-zinc-200/80">
          <dt className="text-[10px] uppercase tracking-wide text-zinc-400">
            /sim/train
          </dt>
          <dd className="mt-0.5 text-sm font-semibold tabular-nums text-zinc-900">
            {isTrain ? "yes" : "no"}
          </dd>
        </div>
      </dl>

      <ol className="mt-5 space-y-3">
        {arm.timeline.map((step, index) => (
          <li key={step.label} className="flex gap-3">
            <div className="flex w-6 shrink-0 flex-col items-center">
              <span
                className={`flex h-6 w-6 items-center justify-center rounded-full text-[11px] font-semibold tabular-nums ${
                  featured
                    ? "bg-indigo-600 text-white"
                    : "bg-zinc-800 text-white"
                }`}
              >
                {index + 1}
              </span>
              {index < arm.timeline.length - 1 && (
                <span className="mt-1 w-px flex-1 bg-zinc-200" aria-hidden />
              )}
            </div>
            <div className="min-w-0 flex-1 pb-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium text-zinc-900">
                  {step.label}
                </span>
                <span
                  className={`rounded-md px-1.5 py-0.5 text-[10px] font-medium ${STEP_KIND_STYLE[step.kind]}`}
                >
                  {step.kind}
                </span>
              </div>
              <ul className="mt-1.5 space-y-1">
                {step.cmds.map((cmd) => (
                  <li
                    key={cmd}
                    className="truncate font-mono text-[11px] leading-5 text-zinc-500"
                    title={cmd}
                  >
                    <span className="text-zinc-300">$ </span>
                    {cmd}
                  </li>
                ))}
              </ul>
            </div>
          </li>
        ))}
      </ol>

      <div className="mt-5 border-t border-zinc-200/80 pt-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Predicted next turn
        </p>
        <blockquote className="mt-2 text-sm leading-6 text-zinc-700">
          “{arm.predMsg}”
        </blockquote>
        <div className="mt-3 flex flex-wrap items-center gap-2">
          {arm.predActs.map((act) => (
            <LabelChip key={act} label={act} />
          ))}
        </div>
      </div>
    </article>
  );
}

/** Cohort trend strip + one paired Sol-high trajectory example. */
export function TypicalSessionsSection() {
  const { baseline, train400, goldMsg, goldActs, taskKey } = SESSION_PAIR;
  const exampleTokenMult = (
    train400.inputTokens / baseline.inputTokens
  ).toFixed(1);

  return (
    <Section
      id="sessions"
      kicker="Agent trajectories"
      title="How sessions change with train400"
    >
      <aside className="grid gap-3 rounded-2xl border border-zinc-200 bg-white p-4 sm:grid-cols-4 sm:p-5">
        {(
          [
            [
              "Steps",
              `${SESSION_COHORT.steps.baseline} → ${SESSION_COHORT.steps.train400}`,
            ],
            [
              "Tools",
              `${SESSION_COHORT.tools.baseline} → ${SESSION_COHORT.tools.train400}`,
            ],
            [
              "Input tokens",
              `${SESSION_COHORT.inputTokensK.baseline}k → ${SESSION_COHORT.inputTokensK.train400}k`,
            ],
            [
              "Jaccard",
              `${SESSION_COHORT.jaccard.baseline} → ${SESSION_COHORT.jaccard.train400}`,
            ],
          ] as const
        ).map(([label, value]) => (
          <div key={label}>
            <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-400">
              {label}
            </p>
            <p className="mt-1 text-lg font-semibold tabular-nums text-zinc-950">
              {value}
            </p>
          </div>
        ))}
      </aside>
      <p className="mt-2 max-w-3xl text-xs leading-5 text-zinc-500">
        {`Means over active Sol-high trials (baseline ${SESSION_COHORT.baselineN.toLocaleString()}; train400 ${SESSION_COHORT.trainActiveN.toLocaleString()} of ${SESSION_COHORT.trainSelectedN.toLocaleString()}, excluding empty trajectories). Input tokens rise about ${SESSION_COHORT.tokenRatio}; mean cost about $${SESSION_COHORT.costUsd.baseline.toFixed(2)} → $${SESSION_COHORT.costUsd.train400.toFixed(2)} (~${SESSION_COHORT.costRatio}).`}
      </p>

      <div className="mt-8">
        <h3 className="text-sm font-semibold text-zinc-900">
          One paired example
        </h3>
        <p className="mt-1 font-mono text-[11px] text-zinc-400">{taskKey}</p>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-600">
          Same held-out task. Baseline stays in{" "}
          <span className="font-mono text-xs text-zinc-700">
            /sim/history.md
          </span>
          ; train400 opens{" "}
          <span className="font-mono text-xs text-zinc-700">_index.json</span>,
          reads two named sessions, then pool-scans{" "}
          <span className="font-mono text-xs text-zinc-700">/sim/train</span>.
          Each numbered timeline item is one agent turn.
        </p>
        <p className="mt-2 text-xs leading-5 text-zinc-500">
          This trial: {baseline.timeline.length} → {train400.timeline.length}{" "}
          steps · {baseline.tools} → {train400.tools} tools · {exampleTokenMult}
          × input tokens · Jaccard {baseline.jaccard} →{" "}
          {train400.jaccard === 1 ? "1" : train400.jaccard}.
        </p>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <SessionTimeline arm={baseline} />
        <SessionTimeline arm={train400} featured />
      </div>

      <div className="mt-4 rounded-2xl border border-zinc-200 bg-white p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Gold next turn (shared)
        </p>
        <blockquote className="mt-2 text-sm leading-6 text-zinc-700">
          “{goldMsg}”
        </blockquote>
        <div className="mt-3 flex flex-wrap items-center gap-2">
          {goldActs.map((act) => (
            <LabelChip key={act} label={act} />
          ))}
          <span className="ml-auto text-xs text-zinc-500">
            Train matched the act set; baseline caught approve only.
          </span>
        </div>
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
            Sol-high (primary): mean Jaccard over 3 trials per task, then 620
            tasks. Whiskers are bootstrap 95% CIs (baseline{" "}
            {pct(ML.baseline.ci[0])}–{pct(ML.baseline.ci[1])}; train400{" "}
            {pct(ML.train400.ci[0])}–{pct(ML.train400.ci[1])}). Lift: +
            {ML.liftPp.toFixed(1)} pp. Sol-low: single trial × 620 — baseline{" "}
            {pct(ML_LOW.baseline.jaccard)}, train400 {pct(ML_LOW.train400.jaccard)}{" "}
            (+{ML_LOW.liftPp.toFixed(1)} pp); no multi-trial CI. Sol-max: train400
            only, 1×620 — {pct(ML_MAX.train400.jaccard, 2)} (exact-set{" "}
            {pct(ML_MAX.train400.exact)}; +{ML_MAX.vsHighPp.toFixed(1)} pp vs high
            mean-of-3, not significant); ~$600 of a $1000 OpenRouter budget.
          </p>
        </div>
        <div className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">Public artifacts</h3>
          <div className="mt-4 space-y-4 text-sm text-zinc-600">
            <div>
              <p className="font-medium text-zinc-800">Source</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href="https://github.com/cooperbench/user.skill/tree/kevin">
                  Benchmark code (kevin) ↗
                </ExtLink>
                <ExtLink href="https://github.com/cooperbench/user.skill/tree/benchmark-website">
                  Website source (benchmark-website) ↗
                </ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Datasets</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={DATASET}>Baseline dataset ↗</ExtLink>
                <ExtLink href={DATASET_TRAIN}>Train400 dataset ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Sol-high baseline</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT.baseline3x}>Agent traces ↗</ExtLink>
                <ExtLink href={ML.baseline.hub}>Judge traces ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Sol-high train400</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT.train4003x}>Agent traces ↗</ExtLink>
                <ExtLink href={ML.train400.hub}>Judge traces ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Sol-low baseline</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT_LOW.baseline}>Agent traces ↗</ExtLink>
                <ExtLink href={JUDGE_LOW.baseline}>Judge traces ↗</ExtLink>
              </p>
            </div>
            <div>
              <p className="font-medium text-zinc-800">Sol-low train400</p>
              <p className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1">
                <ExtLink href={AGENT_LOW.train400}>Agent traces ↗</ExtLink>
                <ExtLink href={JUDGE_LOW.train400}>Judge traces ↗</ExtLink>
              </p>
            </div>
          </div>
          <p className="mt-5 border-t border-zinc-100 pt-4 text-xs leading-5 text-zinc-500">
            Composer 2.5 assigns approve, critical, steer, and inquiry act sets
            across 620 held-out tasks per condition. Sol-high Hub jobs are 3×620;
            Sol-low are 1×620 (reasoning_effort=low). Sol-max train400 is 1×620
            (reasoning_effort=max); Hub links not published yet.
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

/**
 * Same-repo overlap: share of Train400 pack sessions whose `repo` matches the
 * held-out task's session repo (clean_manifest ↔ /sim/train/_index.json).
 * Source: jobs/sol-high-userbench/TRAIN_SAME_REPO_OVERLAP.json
 */
const SAME_REPO = {
  meanSessionPct: 76.5,
  medianSessionPct: 100,
  meanTurnPct: 77.0,
  bucketPct: { mostlySame: 71.3, mixed: 12.7, mostlyOther: 16.0 },
  histLabels: [
    "0–10",
    "10–20",
    "20–30",
    "30–40",
    "40–50",
    "50–60",
    "60–70",
    "70–80",
    "80–90",
    "90–100",
  ],
  histCounts: [66, 24, 15, 40, 10, 0, 10, 13, 33, 409],
  nTasks: 620,
  nDevs: 62,
} as const;

export function TrainSameRepoOverlap() {
  const maxHist = Math.max(...SAME_REPO.histCounts);
  const buckets = [
    {
      label: "Mostly same",
      sub: "≥80% of pack sessions",
      pct: SAME_REPO.bucketPct.mostlySame,
      color: "bg-indigo-600",
    },
    {
      label: "Mixed",
      sub: "20–80%",
      pct: SAME_REPO.bucketPct.mixed,
      color: "bg-sky-500",
    },
    {
      label: "Mostly other",
      sub: "≤20%",
      pct: SAME_REPO.bucketPct.mostlyOther,
      color: "bg-zinc-400",
    },
  ] as const;

  return (
    <section
      id="same-repo"
      aria-labelledby="same-repo-title"
      className="mt-10 scroll-mt-20"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
        Train pack · project match
      </p>
      <SectionHeading
        id="same-repo"
        label="same repo"
        className="mt-2 text-xl font-semibold tracking-tight text-zinc-900"
      >
        Most Train400 sessions are from the same repo as the held-out task
      </SectionHeading>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-600">
        For each of {SAME_REPO.nTasks} tasks, compare the held session&apos;s{" "}
        <span className="font-mono text-xs">repo</span> to every prior session
        in that developer&apos;s train pack. Match = same normalized{" "}
        <span className="font-mono text-xs">owner/repo</span>.
      </p>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
          <figcaption className="font-semibold text-zinc-900">
            Most packs are mostly the same repo as the held-out task
          </figcaption>
          <p className="mt-1 text-xs text-zinc-500">
            Share of {SAME_REPO.nTasks} tasks by same-repo session fraction (
            {SAME_REPO.nDevs} developers).
          </p>
          <div className="mt-5 space-y-3">
            {buckets.map((b) => (
              <div key={b.label}>
                <div className="flex items-baseline justify-between gap-3 text-sm">
                  <div>
                    <span className="font-medium text-zinc-800">{b.label}</span>
                    <span className="ml-2 text-xs text-zinc-400">{b.sub}</span>
                  </div>
                  <span className="tabular-nums text-zinc-700">{b.pct}%</span>
                </div>
                <div className="mt-1.5 h-2.5 overflow-hidden rounded-full bg-zinc-100">
                  <div
                    className={`h-full rounded-full ${b.color}`}
                    style={{ width: `${b.pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </figure>

        <figure className="rounded-2xl border border-zinc-200 bg-white p-5">
          <figcaption className="font-semibold text-zinc-900">
            Most tasks draw nearly all train sessions from the same repo
          </figcaption>
          <p className="mt-1 text-xs text-zinc-500">
            Distribution of pack session fraction matching the held repo (%).
          </p>
          <div
            className="mt-5 grid h-28 items-end gap-1"
            style={{
              gridTemplateColumns: `repeat(${SAME_REPO.histCounts.length}, minmax(0, 1fr))`,
            }}
            role="img"
            aria-label={`Histogram of same-repo session share across ${SAME_REPO.nTasks} tasks: median ${SAME_REPO.medianSessionPct}%, mean ${SAME_REPO.meanSessionPct}%. Peak bin 90 to 100% has ${SAME_REPO.histCounts[9]} tasks.`}
          >
            {SAME_REPO.histCounts.map((count, index) => (
              <div key={SAME_REPO.histLabels[index]} className="flex h-full items-end">
                <div
                  className="w-full rounded-t bg-indigo-600"
                  style={{ height: `${(count / maxHist) * 100}%` }}
                />
              </div>
            ))}
          </div>
          <div
            className="mt-1 grid gap-1 text-center text-[9px] text-zinc-400"
            style={{
              gridTemplateColumns: `repeat(${SAME_REPO.histLabels.length}, minmax(0, 1fr))`,
            }}
          >
            {SAME_REPO.histLabels.map((label) => (
              <span key={label}>{label}</span>
            ))}
          </div>
          <p className="mt-4 text-sm leading-6 text-zinc-600">
            Most packs sit near 100% same-repo; a long left tail pulls the mean
            down to {SAME_REPO.meanSessionPct}% (turn-weighted mean{" "}
            {SAME_REPO.meanTurnPct}%).
          </p>
        </figure>
      </div>
    </section>
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
      <aside className="mt-6 flex flex-col gap-4 rounded-2xl border border-zinc-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="font-semibold text-zinc-900">
            Composer closely matches Kevin&apos;s labels
          </h3>
          <p className="mt-1 text-2xl font-semibold tracking-tight text-zinc-950">
            81% Jaccard agreement
          </p>
          <p className="mt-1 text-sm text-zinc-600">
            64% exact-set agreement across 50 co-labeled turns.{" "}
            <span className="text-zinc-500">Agreement, not accuracy.</span>
          </p>
        </div>
        <a
          href="/annotator/dashboard"
          className="shrink-0 text-sm font-medium text-indigo-600 underline-offset-2 hover:underline"
        >
          Open the public annotator dashboard →
        </a>
      </aside>
    </section>
  );
}
