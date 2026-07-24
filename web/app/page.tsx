import {
  AnalysisSection,
  DatasetHubLinks,
  LabelExamplesSection,
  LeaderboardSection,
  ReasoningEffortSection,
  RunDetailsSection,
  TrainSameRepoOverlap,
  TypicalSessionsSection,
} from "./SolHighResults";
import { SectionHeading } from "./SectionHeading";

const EVAL_DEVS = 62;
const EVAL_TASKS = 620;

function StatCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub: string;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white px-5 py-4">
      <div className="text-3xl font-semibold tracking-tight text-zinc-900">
        {value}
      </div>
      <div className="mt-1 text-sm font-medium text-zinc-600">{label}</div>
      <div className="mt-0.5 text-xs text-zinc-400">{sub}</div>
    </div>
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
    { label: "Mean", short: "23.4k", value: 23_398.503, color: "bg-sky-600" },
    { label: "P90", short: "25.3k", value: 25_281.7, color: "bg-violet-600" },
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
        aria-label="Prior context tokens per published task on a log scale: median 4,214, mean 23,398.503, 90th percentile 25,281.7, maximum 1,344,149"
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
        <span className="absolute left-[32.4%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">
          100
        </span>
        <span className="absolute left-[64.8%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">
          10k
        </span>
        <span className="absolute left-[97.2%] top-10 -translate-x-1/2 text-[10px] text-zinc-400">
          1m
        </span>
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

export default function HomePage() {
  return (
    <main className="mx-auto max-w-5xl px-5 pb-16 pt-8 sm:px-8">
      <nav
        aria-label="Main navigation"
        className="flex flex-wrap items-center justify-between gap-4 text-sm"
      >
        <a href="/" className="font-semibold tracking-tight text-zinc-950">
          UserBench
        </a>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-zinc-500">
          <span aria-current="page" className="font-medium text-zinc-950">
            Dataset
          </span>
          <a href="#leaderboard" className="hover:text-zinc-950">
            Leaderboard
          </a>
          <a href="#same-repo" className="hover:text-zinc-950">
            Same repo
          </a>
          <a href="#sessions" className="hover:text-zinc-950">
            Sessions
          </a>
          <a href="#analysis" className="hover:text-zinc-950">
            Analysis
          </a>
          <a href="#reasoning-effort" className="hover:text-zinc-950">
            Effort
          </a>
          <a href="/misprediction" className="hover:text-zinc-950">
            Misprediction
          </a>
          <a href="/annotator/dashboard" className="hover:text-zinc-950">
            Annotator
          </a>
          <a href="/v1" className="hover:text-zinc-950">
            Old leaderboard
          </a>
        </div>
      </nav>

      <LeaderboardSection />

      <section
        id="dataset"
        aria-labelledby="dataset-title"
        className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12"
      >
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
          Dataset
        </p>
        <SectionHeading
          id="dataset"
          label="dataset"
          className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Same held-out tasks, with or without history
        </SectionHeading>
        <p className="mt-3 max-w-3xl text-base leading-7 text-zinc-600">
          The two public packages contain the same 620 coding-agent
          conversation tasks. Train400 adds an earlier, developer-specific
          history pack without changing the held-out message.
        </p>
        <div className="mt-7 grid gap-3 sm:grid-cols-3">
          <StatCard
            label="developer IDs"
            value={String(EVAL_DEVS)}
            sub="exactly 10 tasks each"
          />
          <StatCard
            label="held-out tasks"
            value={String(EVAL_TASKS)}
            sub="one next message per task"
          />
          <StatCard
            label="unique training turns"
            value="24,800"
            sub="400 per developer × 62 packs"
          />
        </div>
        <DatasetHubLinks />
        <TrainSameRepoOverlap />
      </section>

      <section
        id="dataset-details"
        aria-labelledby="dataset-details-title"
        className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12"
      >
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
          Dataset details
        </p>
        <SectionHeading
          id="dataset-details"
          label="dataset details"
          className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Published package facts
        </SectionHeading>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-zinc-200 bg-white p-5">
            <h3 className="font-semibold text-zinc-900">Matched tasks</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Baseline and train400 share all task IDs, histories, and real
              held-out messages.
            </p>
          </div>
          <div className="rounded-2xl border border-zinc-200 bg-white p-5">
            <h3 className="font-semibold text-zinc-900">Unique train packs</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-600">
              Each of 62 packs contains 400 developer turns and is reused
              across that developer&apos;s 10 tasks.
            </p>
          </div>
          <div className="rounded-2xl border border-zinc-200 bg-white p-5">
            <h3 className="font-semibold text-zinc-900">Time ordering</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-600">
              All 1,913 mounted training sessions end before their
              developer-specific cutoff.
            </p>
          </div>
        </div>
      </section>

      <section
        id="context"
        aria-labelledby="context-title"
        className="mt-16 scroll-mt-20 border-t border-zinc-200 pt-12"
      >
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
          Prediction context
        </p>
        <SectionHeading
          id="context"
          label="prediction context"
          className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
        >
          What the model sees and predicts
        </SectionHeading>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-600">
          These figures come from the 620 published tasks. Conversation blocks
          count the history, context tokens measure its size, and next-message
          tokens measure the text to predict.
        </p>
        <div className="mt-6 grid gap-4 lg:grid-cols-3">
          <CompactHistogram
            title="Conversation history before each prediction"
            subtitle="All prior role blocks: developer, agent, tool, system, metadata"
            labels={["0–4", "5–9", "10–19", "20–39", "40–79", "80–159", "160+"]}
            counts={[83, 74, 96, 119, 136, 55, 57]}
            color="bg-fuchsia-400"
            takeaway="Median depth is 28 prior role blocks."
            ariaLabel="All prior role blocks across 620 published tasks: 83 have 0 to 4, 74 have 5 to 9, 96 have 10 to 19, 119 have 20 to 39, 136 have 40 to 79, 55 have 80 to 159, and 57 have 160 or more"
          />
          <ContextTokenChart />
          <CompactHistogram
            title="Length of the developer’s next message"
            subtitle="cl100k tokens in the held-out message"
            labels={["1–9", "10–24", "25–49", "50–99", "100–249", "250+"]}
            counts={[231, 171, 128, 48, 29, 13]}
            color="bg-emerald-500"
            takeaway="Median length is 15 tokens, with a long tail from logs and pasted text."
            ariaLabel="Next-message token lengths across 620 published tasks: 231 have 1 to 9, 171 have 10 to 24, 128 have 25 to 49, 48 have 50 to 99, 29 have 100 to 249, and 13 have 250 or more"
          />
        </div>
      </section>

      <LabelExamplesSection />
      <AnalysisSection />
      <ReasoningEffortSection />
      <TypicalSessionsSection />
      <RunDetailsSection />

      <footer className="mt-16 border-t border-zinc-200 pt-6 text-sm text-zinc-400">
        UserBench · 62 developer IDs · 620 held-out tasks · 24,800 unique
        training turns. See{" "}
        <a href="#leaderboard" className="text-zinc-600 hover:text-zinc-900">
          leaderboard
        </a>
        ,{" "}
        <a href="#sessions" className="text-zinc-600 hover:text-zinc-900">
          sessions
        </a>
        ,{" "}
        <a
          href="#reasoning-effort"
          className="text-zinc-600 hover:text-zinc-900"
        >
          effort
        </a>
        ,{" "}
        <a
          href="/annotator/dashboard"
          className="text-zinc-600 hover:text-zinc-900"
        >
          annotator
        </a>
        , and the{" "}
        <a href="/v1" className="text-zinc-600 hover:text-zinc-900">
          old leaderboard
        </a>
        .
      </footer>
    </main>
  );
}
