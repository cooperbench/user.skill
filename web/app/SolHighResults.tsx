import type { ReactNode } from "react";

const DATASET = "https://hub.harborframework.com/datasets/userbench/UserBench";
const DATASET_TRAIN =
  "https://hub.harborframework.com/datasets/userbench/UserBench-train400";
const DATASET_REF = "userbench/UserBench@v2";
const DATASET_TRAIN_REF = "userbench/UserBench-train400@v2";
const HUB_TASKS = 620;
const HUB_DEVS = 62;

/** Multilabel Hub jobs (offline Composer regrade; mean Jaccard primary). */
const ML = {
  baseline: {
    jaccard: 0.445,
    exact: 0.306,
    nExact: 190,
    chance: 0.439,
    vsChancePp: 0.6,
    macroF1: 0.439,
    n: 620,
    hub: "https://hub.harborframework.com/jobs/07243479-5d98-41e4-b9a9-4a9316fbaf33",
  },
  train400: {
    jaccard: 0.48,
    exact: 0.35,
    nExact: 217,
    chance: 0.434,
    vsChancePp: 4.6,
    macroF1: 0.468,
    n: 620,
    hub: "https://hub.harborframework.com/jobs/6eaeab92-f6b0-4e78-9304-3dc118040807",
  },
  archive3x: {
    jaccard: 0.5,
    n: 1386,
    hub: "https://hub.harborframework.com/jobs/e4a8dcba-53d4-483b-af58-e823d5d3a18a",
  },
};

/** Legacy single-label Harbor mean reward (exact move match) — secondary. */
const SL = {
  baseline: {
    match: 288,
    n: 620,
    rate: 288 / 620, // 46.5%
    cost: "~$84",
    hub: "https://hub.harborframework.com/jobs/c8958ef2-67c9-4116-9e86-b347f0f8f62d",
  },
  train400: {
    match: 309,
    n: 620,
    rate: 309 / 620, // 49.8% after retry429 backfill
    cost: "~$281",
    hub: "https://hub.harborframework.com/jobs/d8501a41-08f7-4945-8a23-f6a9f13e4308",
  },
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

function StatCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white px-5 py-4">
      <div className="text-3xl font-semibold tracking-tight text-zinc-900">
        {value}
      </div>
      <div className="mt-1 text-sm font-medium text-zinc-600">{label}</div>
      {sub && <div className="mt-0.5 text-xs text-zinc-400">{sub}</div>}
    </div>
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
  return (
    <section id={id} className="mt-12 scroll-mt-20">
      {kicker && (
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">
          {kicker}
        </div>
      )}
      <h2 className="mt-1 text-xl font-semibold tracking-tight text-zinc-900">
        {title}
      </h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function JaccardBar({ rate, max = 0.65 }: { rate: number; max?: number }) {
  return (
    <div className="relative h-7 flex-1 overflow-hidden rounded bg-zinc-100">
      <div
        className="h-full rounded bg-indigo-500"
        style={{ width: `${Math.min(100, (rate / max) * 100)}%` }}
      />
      <div className="absolute inset-y-0 left-2 flex items-center font-mono text-xs font-semibold text-zinc-800">
        {pct(rate)}
      </div>
    </div>
  );
}

/** Primary Sol-high multilabel leaderboard — sits above dataset intro. */
export function LeaderboardSection() {
  const deltaPp = (ML.train400.jaccard - ML.baseline.jaccard) * 100;
  return (
    <>
      <header className="mt-8">
        <h1 className="text-3xl font-semibold tracking-tight text-zinc-900">
          UserBench — {HUB_DEVS} developers, {HUB_TASKS} tasks
        </h1>
        <p className="mt-3 max-w-2xl text-zinc-600">
          Agentic next-move prediction for{" "}
          <strong>gpt-5.6-sol</strong> (reasoning{" "}
          <strong>high</strong>). Primary score:{" "}
          <strong>mean Jaccard</strong> over free multi-label acts (
          <span className="font-mono text-sm">
            approve / critical / steer / inquiry
          </span>
          ).
        </p>
        <p className="mt-2 text-sm text-zinc-500">
          <a href="#leaderboard" className="hover:text-zinc-800">
            Leaderboard
          </a>
          {" · "}
          <a href="#dataset" className="hover:text-zinc-800">
            Dataset
          </a>
          {" · "}
          <a href="#analysis" className="hover:text-zinc-800">
            Analysis
          </a>
        </p>
      </header>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard
          label="eval points"
          value={String(HUB_TASKS)}
          sub={`${HUB_DEVS} developers · Hub scale`}
        />
        <StatCard
          label="baseline Jaccard"
          value={pct(ML.baseline.jaccard)}
          sub="sol high · multilabel"
        />
        <StatCard
          label="train400 Jaccard"
          value={pct(ML.train400.jaccard)}
          sub="sol high · multilabel"
        />
        <StatCard
          label="Δ train400"
          value={`${deltaPp >= 0 ? "+" : ""}${deltaPp.toFixed(1)} pp`}
          sub="train400 above baseline"
        />
      </div>

      <Section
        id="leaderboard"
        kicker="leaderboard"
        title="Sol-high mean Jaccard (multilabel)"
      >
        <p className="mb-4 text-sm text-zinc-500">
          Offline Composer 2.5 regrade aligned with the annotator. Chance = mean
          Jaccard of always predicting the modal gold set (
          <span className="font-mono text-xs">[steer]</span>). Agent
          trajectories live on the Hub jobs below.
        </p>

        <div className="space-y-4 rounded-xl border border-zinc-200 bg-white p-5">
          {(
            [
              ["baseline", "UserBench (no train)", ML.baseline],
              ["train400", "UserBench-train400", ML.train400],
            ] as const
          ).map(([id, condition, r]) => (
            <div key={id}>
              <div className="mb-1.5 flex flex-wrap items-baseline gap-2">
                <span className="font-mono text-sm font-semibold text-zinc-900">
                  gpt-5.6-sol [high]
                </span>
                <span className="text-xs text-zinc-500">{condition}</span>
                <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-emerald-700 ring-1 ring-inset ring-emerald-200">
                  complete
                </span>
                <span className="ml-auto font-mono text-sm tabular-nums text-zinc-700">
                  {pct(r.jaccard)} Jaccard · exact {pct(r.exact)}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <JaccardBar rate={r.jaccard} />
                <div className="w-28 shrink-0 text-right text-xs tabular-nums text-zinc-500">
                  vs chance {r.vsChancePp >= 0 ? "+" : ""}
                  {r.vsChancePp.toFixed(1)} pp
                </div>
              </div>
              <div className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1 text-xs text-zinc-500">
                <ExtLink href={r.hub}>Harbor Hub job → trials</ExtLink>
                <span>
                  chance {pct(r.chance)} · macro-F1 {pct(r.macroF1)} · n=
                  {r.n}
                </span>
              </div>
            </div>
          ))}
          <p className="border-t border-zinc-100 pt-3 text-xs text-zinc-500">
            Scale 0–65%. Hub multilabel jobs:{" "}
            <ExtLink href={ML.baseline.hub}>baseline</ExtLink>
            {" · "}
            <ExtLink href={ML.train400.hub}>train400</ExtLink>
            {" · "}
            <ExtLink href={ML.archive3x.hub}>archive 3×</ExtLink>
            . Datasets:{" "}
            <ExtLink href={`${DATASET}?tag=v2`}>{DATASET_REF}</ExtLink>
            {" · "}
            <ExtLink href={`${DATASET_TRAIN}?tag=v2`}>
              {DATASET_TRAIN_REF}
            </ExtLink>
            .
          </p>
        </div>
      </Section>
    </>
  );
}

/** Post-dataset analysis: chance, pairwise, 3-trial variance, legacy SL. */
export function AnalysisSection() {
  return (
    <Section
      id="analysis"
      kicker="result analysis"
      title="What the numbers say"
    >
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-semibold text-zinc-800">
            Multilabel vs chance
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-zinc-600">
            Best constant predictor is always{" "}
            <span className="font-mono text-xs">[steer]</span> (modal gold
            set). Baseline clears chance by only{" "}
            <strong className="text-zinc-800">+0.6 pp</strong> Jaccard;
            train400 clears it by{" "}
            <strong className="text-zinc-800">+4.6 pp</strong>. Exact-set match
            stays harder ({pct(ML.baseline.exact)} → {pct(ML.train400.exact)}).
          </p>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-zinc-800">
            Train400 vs baseline
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-zinc-600">
            On the full {HUB_TASKS}-task multilabel regrade, train400 leads by{" "}
            <strong className="text-zinc-800">+3.5 pp</strong> mean Jaccard (
            {pct(ML.train400.jaccard)} vs {pct(ML.baseline.jaccard)}). The older
            single-label exact-match metric agrees on direction:{" "}
            {pct(SL.train400.rate)} vs {pct(SL.baseline.rate)} (+
            {((SL.train400.rate - SL.baseline.rate) * 100).toFixed(1)} pp) after
            retry backfill.
          </p>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-zinc-800">
            3-trial variance
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-zinc-600">
            Accidental Harbor replicas (3 per task) check stability. Single-label
            train400 lanes sit at{" "}
            <span className="font-mono text-xs">50.6% / 49.0% / 50.3%</span>{" "}
            (mean of means ≈ 50.0%). Archive 3× multilabel regrade averages{" "}
            <strong className="text-zinc-800">
              {pct(ML.archive3x.jaccard)} Jaccard
            </strong>{" "}
            (n={ML.archive3x.n}). Aggregate rates barely move across replicas.
          </p>
          <p className="mt-2 text-xs text-zinc-500">
            Archive 3× multilabel Hub job:{" "}
            <ExtLink href={ML.archive3x.hub}>e4a8dcba…</ExtLink>
          </p>
        </div>

        <details className="rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-600">
          <summary className="cursor-pointer font-medium text-zinc-800">
            Single-label Hub jobs (secondary)
          </summary>
          <p className="mt-3 text-xs text-zinc-500">
            Exact move match — not the primary score. Multilabel Jaccard above
            is the headline.
          </p>
          <ul className="mt-3 space-y-2 font-mono text-xs">
            <li>
              baseline {SL.baseline.match}/{SL.baseline.n} ={" "}
              {pct(SL.baseline.rate)} · {SL.baseline.cost} ·{" "}
              <ExtLink href={SL.baseline.hub}>job ↗</ExtLink>
            </li>
            <li>
              train400 {SL.train400.match}/{SL.train400.n} ={" "}
              {pct(SL.train400.rate)} · {SL.train400.cost} ·{" "}
              <ExtLink href={SL.train400.hub}>job ↗</ExtLink>
            </li>
          </ul>
          <p className="mt-3 text-xs leading-relaxed text-zinc-500">
            Stack: mini-swe-agent via OpenRouter; judge Composer 2.5; Modal
            sandboxes; agent-phase OpenRouter allowlist.
          </p>
        </details>
      </div>
    </Section>
  );
}

export function DatasetHubLinks() {
  return (
    <div className="mt-4 grid gap-3 sm:grid-cols-2">
      <div className="rounded-xl border border-zinc-200 bg-white p-4">
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">
          Harbor datasets
        </div>
        <p className="mt-2 text-sm text-zinc-700">
          <span className="font-mono text-xs">{DATASET_REF}</span> and{" "}
          <span className="font-mono text-xs">{DATASET_TRAIN_REF}</span> —{" "}
          <strong>{HUB_TASKS}</strong> held tasks / <strong>{HUB_DEVS}</strong>{" "}
          developers. Train twin adds earlier sessions under{" "}
          <span className="font-mono text-xs">/sim/train/</span>.
        </p>
        <div className="mt-3 flex flex-wrap gap-3 text-sm">
          <ExtLink href={DATASET}>UserBench ↗</ExtLink>
          <ExtLink href={DATASET_TRAIN}>train400 ↗</ExtLink>
        </div>
      </div>
      <div className="rounded-xl border border-zinc-200 bg-white p-4">
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">
          Scoring
        </div>
        <p className="mt-2 text-sm text-zinc-700">
          Primary reward is{" "}
          <strong>mean Jaccard</strong> of act-sets. Exact-set match and
          macro-F1 are secondary. Taxonomy matches the annotator (
          <span className="font-mono text-xs">directive→steer</span>).
        </p>
      </div>
    </div>
  );
}
