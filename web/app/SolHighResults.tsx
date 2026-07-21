import type { ReactNode } from "react";

const DATASET = "https://hub.harborframework.com/datasets/userbench/UserBench";
const DATASET_TRAIN =
  "https://hub.harborframework.com/datasets/userbench/UserBench-train400";
const DATASET_REF = "userbench/UserBench@v2";
const DATASET_TRAIN_REF = "userbench/UserBench-train400@v2";
const HUB_TASKS = 620;
const HUB_DEVS = 62;

/** Multilabel judge jobs; mean Jaccard is the benchmark metric. */
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

/** Agent-trial Hub jobs (gpt-5.6-sol trajectories). */
const AGENT = {
  baseline3x:
    "https://hub.harborframework.com/jobs/87adaae5-6152-4329-b0b1-85bd2a75ec2a",
  train4003x:
    "https://hub.harborframework.com/jobs/48321212-f765-48cd-962c-d5b4518a053f",
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

function ScoreRow({
  label,
  note,
  rate,
  featured = false,
}: {
  label: string;
  note: string;
  rate: number;
  featured?: boolean;
}) {
  const chance = 0.437;
  return (
    <div
      className={`rounded-2xl border p-4 sm:p-5 ${
        featured
          ? "border-indigo-200 bg-indigo-50/60"
          : "border-zinc-200 bg-white"
      }`}
    >
      <div className="flex items-end justify-between gap-4">
        <div>
          <h3 className="font-semibold text-zinc-900">{label}</h3>
          <p className="mt-0.5 text-sm text-zinc-500">{note}</p>
        </div>
        <p className="shrink-0 text-3xl font-semibold tracking-tight tabular-nums text-zinc-950">
          {pct(rate)}
        </p>
      </div>
      <div
        className="relative mt-4 h-2.5 rounded-full bg-zinc-200"
        role="img"
        aria-label={`${label}: ${pct(rate)} mean Jaccard; chance is about 43.7%`}
      >
        <div
          className={`h-full rounded-full ${
            featured ? "bg-indigo-600" : "bg-zinc-600"
          }`}
          style={{ width: `${rate * 100}%` }}
        />
        <span
          className="absolute -top-1 h-[18px] w-px bg-amber-600"
          style={{ left: `${chance * 100}%` }}
          aria-hidden="true"
        />
      </div>
    </div>
  );
}

/** Primary result: one model, two conditions, current multilabel scoring. */
export function LeaderboardSection() {
  return (
    <>
      <header className="mt-16 max-w-3xl sm:mt-20">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-indigo-600">
          UserBench
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-[-0.035em] text-zinc-950 sm:text-6xl sm:leading-[1.02]">
          How well can agents simulate users?
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-600">
          UserBench tests whether an agent can predict what a real developer
          will do next in a coding session. The main score is multilabel mean
          Jaccard (IoU).
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
            <h2
              id="leaderboard-title"
              className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950 sm:text-3xl"
            >
              Training history helps, modestly
            </h2>
          </div>
          <div className="sm:text-right">
            <p className="text-4xl font-semibold tracking-tight tabular-nums text-indigo-700">
              +3.48 pp
            </p>
            <p className="mt-1 text-sm text-zinc-500">train400 vs baseline</p>
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <ScoreRow
            label="Baseline"
            note="No developer training history"
            rate={ML.baseline.jaccard}
          />
          <ScoreRow
            label="Train400"
            note="400 prior turns from the same developer"
            rate={ML.train400.jaccard}
            featured
          />
        </div>
        <div className="mt-4 flex flex-col gap-2 text-sm text-zinc-600 sm:flex-row sm:items-center sm:justify-between">
          <p>
            <span className="mr-2 inline-block h-3 w-px bg-amber-600 align-[-1px]" />
            Chance is about <strong className="text-zinc-800">43.7%</strong>.
          </p>
          <p className="tabular-nums">
            95% CI for lift: <strong className="text-zinc-800">+0.26 to +6.64 pp</strong>
          </p>
        </div>

        <details className="group mt-6 rounded-2xl border border-zinc-200 bg-white">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-4 text-sm font-semibold text-zinc-800 marker:content-none">
            Run details
            <span
              aria-hidden="true"
              className="text-lg font-normal text-zinc-400 transition-transform group-open:rotate-45"
            >
              +
            </span>
          </summary>
          <div className="border-t border-zinc-100 px-5 py-5 text-sm text-zinc-600">
            <div className="grid gap-6 sm:grid-cols-2">
              <div>
                <h3 className="font-semibold text-zinc-900">Current scoring</h3>
                <dl className="mt-3 grid grid-cols-[1fr_auto] gap-x-5 gap-y-2 tabular-nums">
                  <dt>Baseline exact-set match</dt>
                  <dd>{pct(ML.baseline.exact)}</dd>
                  <dt>Train400 exact-set match</dt>
                  <dd>{pct(ML.train400.exact)}</dd>
                  <dt>Arm-specific chance</dt>
                  <dd>{pct(ML.baseline.chance)} / {pct(ML.train400.chance)}</dd>
                  <dt>Macro-F1</dt>
                  <dd>{pct(ML.baseline.macroF1)} / {pct(ML.train400.macroF1)}</dd>
                  <dt>Paired lift test</dt>
                  <dd>p≈0.033</dd>
                </dl>
              </div>
              <div>
                <h3 className="font-semibold text-zinc-900">Runs and artifacts</h3>
                <ul className="mt-3 space-y-2">
                  <li>
                    Baseline: <ExtLink href={AGENT.baseline3x}>agent traces</ExtLink>
                    {" · "}
                    <ExtLink href={ML.baseline.hub}>judge traces</ExtLink>
                  </li>
                  <li>
                    Train400: <ExtLink href={AGENT.train4003x}>agent traces</ExtLink>
                    {" · "}
                    <ExtLink href={ML.train400.hub}>judge traces</ExtLink>
                  </li>
                  <li>
                    <ExtLink href={ML.archive3x.hub}>
                      Judge traces: three independent runs
                    </ExtLink>{" "}
                    ({ML.archive3x.n.toLocaleString()} scored turns)
                  </li>
                </ul>
                <p className="mt-3 text-xs leading-5 text-zinc-500">
                  620 held-out turns per condition. Judge: Composer 2.5 using
                  approve, critical, steer, and inquiry act sets.
                </p>
              </div>
            </div>

          </div>
        </details>
      </section>
    </>
  );
}

/** Plain-language interpretation shown directly after the main result. */
export function AnalysisSection() {
  return (
    <Section
      id="analysis"
      kicker="What the result means"
      title="The model learns a little from a developer’s history"
    >
      <div className="grid gap-4 sm:grid-cols-3">
        <article className="rounded-2xl border border-zinc-200 bg-white p-5">
          <p className="text-2xl font-semibold tabular-nums text-zinc-950">+0.6 pp</p>
          <h3 className="mt-2 font-semibold text-zinc-800">Baseline vs chance</h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            With no personal history, the model lands near a fixed steer guess.
          </p>
        </article>
        <article className="rounded-2xl border border-indigo-200 bg-indigo-50/60 p-5">
          <p className="text-2xl font-semibold tabular-nums text-indigo-700">+3.48 pp</p>
          <h3 className="mt-2 font-semibold text-zinc-800">Training lift</h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Four hundred prior turns improve prediction, though the gain is
            small.
          </p>
        </article>
        <article className="rounded-2xl border border-zinc-200 bg-white p-5">
          <p className="text-2xl font-semibold tabular-nums text-zinc-950">+4.62 pp</p>
          <h3 className="mt-2 font-semibold text-zinc-800">Train400 vs chance</h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            The stricter fixed-chance test gives p≈0.030 one-sided and p≈0.060
            two-sided.
          </p>
        </article>
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
      <h2
        id="labels-title"
        className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
      >
        One turn can do more than one thing
      </h2>
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
      <div className="mt-4 flex flex-col gap-2 text-sm leading-6 text-zinc-600 sm:flex-row sm:items-center sm:justify-between">
        <p>
          A turn can approve one choice and steer another, so one label would
          drop part of the intent.
        </p>
        <a
          href="/annotator/dashboard"
          className="shrink-0 font-medium text-indigo-600 underline-offset-4 hover:underline"
        >
          Open the public annotator dashboard →
        </a>
      </div>
      <p className="mt-3 text-xs text-zinc-500">
        On 50 turns, Composer and Kevin agree at about 81% Jaccard and 64%
        exact-set match. These are agreement rates, not accuracy.
      </p>
    </section>
  );
}

export function MethodsSection() {
  return (
    <section
      id="methods"
      aria-labelledby="methods-title"
      className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
        Scoring and reproduction
      </p>
      <h2
        id="methods-title"
        className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
      >
        A score that gives partial credit
      </h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <article className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">How scoring works</h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Each turn can contain more than one act: approve, critical, steer,
            or inquiry. Jaccard divides the overlap between predicted and true
            act sets by their union, then averages across all 620 turns.
          </p>
          <p className="mt-3 text-sm leading-6 text-zinc-600">
            The chance reference always predicts the most common gold set,{" "}
            <span className="font-mono text-xs text-zinc-700">[steer]</span>.
            Its headline mean is about 43.7%.
          </p>
        </article>
        <article className="rounded-2xl border border-zinc-200 bg-white p-5">
          <h3 className="font-semibold text-zinc-900">Reproduce the result</h3>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Public Harbor pages hold the datasets, agent trajectories, and
            judge traces for both conditions.
          </p>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <ExtLink href={DATASET}>Baseline dataset ↗</ExtLink>
              {" · "}
              <ExtLink href={DATASET_TRAIN}>train400 dataset ↗</ExtLink>
            </li>
            <li>
              <ExtLink href={AGENT.baseline3x}>Baseline agent traces ↗</ExtLink>
              {" · "}
              <ExtLink href={AGENT.train4003x}>train400 agent traces ↗</ExtLink>
            </li>
            <li>
              <ExtLink href={ML.baseline.hub}>Baseline judge traces ↗</ExtLink>
              {" · "}
              <ExtLink href={ML.train400.hub}>train400 judge traces ↗</ExtLink>
            </li>
          </ul>
        </article>
      </div>
    </section>
  );
}
