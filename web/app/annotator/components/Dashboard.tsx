"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ACTS } from "@/lib/acts";
import type { Move } from "@/lib/types";
import type { PublicUser } from "@/lib/users";

const LABEL_COLORS: Record<Move, string> = {
  approve: "bg-emerald-100 text-emerald-900 border-emerald-300",
  critical: "bg-rose-100 text-rose-900 border-rose-300",
  steer: "bg-sky-100 text-sky-900 border-sky-300",
  inquiry: "bg-violet-100 text-violet-900 border-violet-300",
};

type KappaMap = Record<Move, number | null>;

type DashData = {
  viewer: PublicUser | null;
  raters: PublicUser[];
  progress: {
    userId: string;
    labeled: number;
    skipped: number;
    done: number;
    total: number;
  }[];
  rows: {
    itemId: string;
    index: number;
    developer: string;
    point_id: string;
    llm: Move[];
    humansOverlap: "exact" | "partial" | "disjoint" | "empty" | "single";
    excluded: boolean;
    labels: Record<
      string,
      {
        labels: Move[] | null;
        skipped: boolean;
        note?: string;
        vs_llm?: "exact" | "partial" | "disjoint" | "empty";
      }
    >;
  }[];
  agreement: {
    pairwise: {
      a: string;
      b: string;
      n: number;
      jaccard: number | null;
      kappa_macro: number | null;
      kappa_per_label: KappaMap;
      exact_pct: number | null;
    }[];
    humanVsLlm: {
      perRater: {
        userId: string;
        n: number;
        jaccard: number | null;
        kappa_macro: number | null;
        kappa_per_label: KappaMap;
        exact_pct: number | null;
      }[];
      pooled: {
        n: number;
        jaccard: number | null;
        kappa_macro: number | null;
        kappa_per_label: KappaMap;
        exact_pct: number | null;
      };
    };
  };
  exclusion: {
    developers: string[];
    items: number;
    totalItems: number;
    reason: string;
  };
};

type IrrPairwise = {
  a: string;
  b: string;
  n: number;
  jaccard: number;
  kappa_macro: number;
  kappa_per_label: KappaMap;
  exact_pct: number;
};

type WithinModelIrr = {
  n_items: number;
  trials: string[];
  pairwise: IrrPairwise[];
  pairwise_avg: {
    jaccard: number;
    kappa_macro: number;
    exact_pct: number;
  };
  n_way: {
    all_identical: number;
    all_identical_pct: number;
  };
};

type CrossPair = {
  n: number;
  jaccard: number;
  kappa_macro: number;
  kappa_per_label: KappaMap;
  exact_pct: number;
};

type IrrSummary = {
  within_composer: WithinModelIrr;
  within_luna: WithinModelIrr;
  cross: {
    primary_trial: string;
    primary_note: string;
    pairs: {
      luna_vs_composer: CrossPair;
      composer_vs_kevin: CrossPair;
      luna_vs_kevin: CrossPair;
    };
  };
};

function avgKappaPerLabel(pairs: IrrPairwise[]): KappaMap {
  const out = {} as KappaMap;
  for (const a of ACTS) {
    const vals = pairs
      .map((p) => p.kappa_per_label[a])
      .filter((v): v is number => v != null);
    out[a] = vals.length
      ? vals.reduce((s, v) => s + v, 0) / vals.length
      : null;
  }
  return out;
}

function MetricRow({
  title,
  n,
  jaccard,
  kappa_macro,
  exact_pct,
  kappa_per_label,
  highlight,
  extra,
}: {
  title: string;
  n: number;
  jaccard: number | null;
  kappa_macro: number | null;
  exact_pct: number | null;
  kappa_per_label: KappaMap;
  highlight?: boolean;
  extra?: string;
}) {
  if (!n || n <= 0) return null;
  return (
    <li
      className={[
        "rounded border px-2 py-1.5 font-mono text-xs",
        highlight
          ? "border-accent/30 bg-teal-50/40 font-medium"
          : "border-rule/60 bg-paper/60",
      ].join(" ")}
    >
      <div className="flex flex-wrap items-baseline gap-x-2">
        <span className="font-medium text-ink">{title}</span>
        <span className="text-stone-500">n={n}</span>
        <span className="text-accent">J={fmt(jaccard)}</span>
        <span>κ̄={fmt(kappa_macro)}</span>
        <span className="text-stone-500">
          exact {exact_pct === null ? "—" : `${exact_pct}%`}
        </span>
        {extra ? <span className="text-stone-500">{extra}</span> : null}
      </div>
      <div className={["mt-0.5", highlight ? "font-normal" : ""].join(" ")}>
        <KappaRow kappa={kappa_per_label} />
      </div>
    </li>
  );
}

function Chips({ labels }: { labels: Move[] | null | undefined }) {
  if (!labels || labels.length === 0) {
    return <span className="font-mono text-stone-400">—</span>;
  }
  return (
    <span className="inline-flex flex-wrap gap-0.5">
      {labels.map((label) => (
        <span
          key={label}
          className={[
            "rounded border px-1.5 py-0.5 font-mono text-[11px] font-medium",
            LABEL_COLORS[label],
          ].join(" ")}
        >
          {label}
        </span>
      ))}
    </span>
  );
}

function nameOf(raters: PublicUser[], id: string): string {
  return raters.find((r) => r.id === id)?.displayName || id;
}

function fmt(n: number | null | undefined, digits = 3): string {
  if (n == null) return "—";
  return n.toFixed(digits);
}

/** Jaccard 0–1 → whole-percent headline, e.g. 0.807 → "81%". */
function pctJ(n: number | null | undefined): string {
  if (n == null) return "—";
  return `${Math.round(n * 100)}%`;
}

function KappaRow({ kappa }: { kappa: KappaMap }) {
  return (
    <span className="text-stone-500">
      {ACTS.map((a) => (
        <span key={a} className="mr-1.5">
          {a[0]}={fmt(kappa[a])}
        </span>
      ))}
    </span>
  );
}

function Details({
  children,
  label = "Details",
}: {
  children: React.ReactNode;
  label?: string;
}) {
  return (
    <details className="mt-4 rounded-xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-xs text-zinc-600">
      <summary className="cursor-pointer font-medium text-zinc-800">
        {label}
      </summary>
      <div className="mt-2 space-y-3">{children}</div>
    </details>
  );
}

export function DashboardView({
  user,
  logout,
}: {
  user: PublicUser | null;
  logout: () => Promise<void>;
}) {
  const [data, setData] = useState<DashData | null>(null);
  const [irr, setIrr] = useState<IrrSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/dashboard");
        if (!res.ok) {
          const body = (await res.json().catch(() => ({}))) as {
            error?: string;
          };
          throw new Error(body.error || `HTTP ${res.status}`);
        }
        const json = (await res.json()) as DashData;
        if (!cancelled) setData(json);
      } catch (e) {
        if (!cancelled)
          setError(e instanceof Error ? e.message : "Failed to load");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch(
          "/data/judge_trials/irr_cross_summary_20260718_no_dataclaw.json",
        );
        if (!res.ok) return;
        const json = (await res.json()) as IrrSummary;
        if (!cancelled) setIrr(json);
      } catch {
        // IRR summary is optional/additive; ignore load failures.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-stone-600">
        Loading dashboard…
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="mx-auto max-w-lg px-4 py-16 text-center">
        <p className="text-rose-700">{error || "No data"}</p>
        <Link href="/annotator" className="mt-4 inline-block text-sm underline">
          Back to annotator
        </Link>
      </div>
    );
  }

  const { raters, rows, agreement, progress, exclusion } = data;

  // Hide empty rows: only show cards / agreement rows that actually have data.
  const progressWithData = progress.filter((p) => p.done > 0);
  const pairwiseWithData = agreement.pairwise.filter((pair) => pair.n > 0);
  const perRaterWithData = agreement.humanVsLlm.perRater.filter(
    (row) => row.n > 0,
  );

  const kevinVsLlm =
    perRaterWithData.find((row) =>
      nameOf(raters, row.userId).toLowerCase().includes("kevin"),
    ) ??
    perRaterWithData[0] ??
    null;

  return (
    <div className="mx-auto flex min-h-screen max-w-5xl flex-col gap-5 px-5 pb-16 pt-8 sm:px-8">
      <nav
        aria-label="Main navigation"
        className="flex flex-wrap items-center justify-between gap-4 text-sm"
      >
        <Link href="/" className="font-semibold tracking-tight text-zinc-950">
          UserBench
        </Link>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-zinc-500">
          <Link href="/" className="hover:text-zinc-950">
            Dataset
          </Link>
          {user ? (
            <Link href="/annotator" className="hover:text-zinc-950">
              Annotator
            </Link>
          ) : null}
          <span aria-current="page" className="font-medium text-zinc-950">
            Dashboard
          </span>
        </div>
      </nav>

      <header className="mt-8 flex flex-col gap-4 border-b border-zinc-200 pb-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-indigo-600">
            Public annotator
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-zinc-950 sm:text-4xl">
            Label agreement
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-600">
            Compare multilabel judgments for approve, critical, steer, and
            inquiry.
            {user ? (
              <>
                {" "}
                Signed in as{" "}
                <span className="font-medium text-zinc-900">
                  {user.displayName}
                </span>
                .
              </>
            ) : (
              <> This page is public and read-only.</>
            )}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <Link
            href="/annotator"
            className="rounded-full border border-zinc-200 bg-white px-3 py-1.5 text-xs font-medium text-zinc-700 hover:border-indigo-300 hover:text-indigo-700"
          >
            {user ? "← Annotator" : "Log in to label →"}
          </Link>
          {user ? (
            <button
              type="button"
              onClick={() => void logout()}
              className="rounded-full bg-zinc-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-zinc-700"
            >
              Log out
            </button>
          ) : null}
        </div>
      </header>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {progressWithData.map((p) => (
          <div
            key={p.userId}
            className="rounded-2xl border border-zinc-200 bg-white px-4 py-3"
          >
            <p className="font-medium text-zinc-900">{nameOf(raters, p.userId)}</p>
            <p className="mt-1 font-mono text-xs text-zinc-500">
              {p.done}/{p.total} done · {p.labeled} labeled · {p.skipped} skip
            </p>
          </div>
        ))}
      </section>

      <section className="rounded-2xl border border-zinc-200 bg-white p-5 sm:p-6">
        <h2 className="text-xl font-semibold tracking-tight text-zinc-950">
          Human and LLM labels agree strongly
        </h2>
        {kevinVsLlm ? (
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Kevin and the LLM judge reach{" "}
            <strong className="text-indigo-700">
              {pctJ(kevinVsLlm.jaccard)} Jaccard agreement
            </strong>{" "}
            across {kevinVsLlm.n} co-labeled turns, DataClaw turns excluded.
          </p>
        ) : (
          <p className="mt-2 text-sm text-zinc-500">
            No human and LLM overlap yet.
          </p>
        )}

        {exclusion.items > 0 && (
          <p className="mt-2 text-sm leading-6 text-zinc-500">
            {exclusion.items} of the {exclusion.totalItems} items come from
            DataClaw donors, who are left out of every published UserBench
            number. Keep labeling them: they count toward your progress, not
            toward the agreement figures here.
          </p>
        )}

        <Details label="Details — exact match, κ, and definitions">
          <p>
            Jaccard = |A∩B|/|A∪B| averaged over items both parties labeled
            (skips excluded). Per-label κ is binary presence/absence for each of
            the 4 acts; κ̄ is the macro-average. Turns from{" "}
            {exclusion.developers.join(", ")} are dropped before any of this is
            computed.
          </p>

          <div>
            <h3 className="text-sm font-medium text-stone-700">
              Pairwise human agreement
            </h3>
            <ul className="mt-2 space-y-2">
              {pairwiseWithData.length === 0 && (
                <li className="rounded border border-rule/60 bg-paper/60 px-2 py-1.5 font-mono text-xs text-stone-400">
                  No overlapping human pairs yet.
                </li>
              )}
              {pairwiseWithData.map((pair) => (
                <MetricRow
                  key={`${pair.a}-${pair.b}`}
                  title={`${nameOf(raters, pair.a)} ↔ ${nameOf(raters, pair.b)}`}
                  n={pair.n}
                  jaccard={pair.jaccard}
                  kappa_macro={pair.kappa_macro}
                  exact_pct={pair.exact_pct}
                  kappa_per_label={pair.kappa_per_label}
                />
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-medium text-stone-700">
              Human vs LLM gold
            </h3>
            <ul className="mt-2 space-y-2">
              {perRaterWithData.map((row) => (
                <MetricRow
                  key={row.userId}
                  title={`${nameOf(raters, row.userId)} vs LLM`}
                  n={row.n}
                  jaccard={row.jaccard}
                  kappa_macro={row.kappa_macro}
                  exact_pct={row.exact_pct}
                  kappa_per_label={row.kappa_per_label}
                />
              ))}
              {agreement.humanVsLlm.pooled.n > 0 && (
                <MetricRow
                  title="Pooled humans vs LLM"
                  n={agreement.humanVsLlm.pooled.n}
                  jaccard={agreement.humanVsLlm.pooled.jaccard}
                  kappa_macro={agreement.humanVsLlm.pooled.kappa_macro}
                  exact_pct={agreement.humanVsLlm.pooled.exact_pct}
                  kappa_per_label={
                    agreement.humanVsLlm.pooled.kappa_per_label
                  }
                  highlight
                />
              )}
            </ul>
          </div>
        </Details>
      </section>

      {irr && (
        <section className="rounded-2xl border border-zinc-200 bg-white p-5 sm:p-6">
          <h2 className="text-xl font-semibold tracking-tight text-zinc-950">
            The LLM judge is highly consistent
          </h2>
          <p className="mt-2 text-sm leading-6 text-zinc-600">
            Composer reaches{" "}
            <strong className="text-indigo-700">
              {pctJ(irr.within_composer.pairwise_avg.jaccard)} Jaccard agreement
            </strong>{" "}
            across independent runs.
          </p>

          <Details label="Details — IRR, exact match, and other judges">
            <p>
              Within-model = mean of the 3 pairwise comparisons across
              independent trials. Cross = one trial per judge (
              {irr.cross.primary_trial}). trial_1 Composer = production
              gold_acts. Same J / κ̄ / per-label κ as Agreement, over the same
              cohort: DataClaw turns are dropped here too. Kevin&apos;s side is
              the labels frozen when the trials ran, so Composer↔Kevin covers
              fewer turns than the live count above.
            </p>

            <div>
              <h3 className="text-sm font-medium text-stone-700">
                Within-model 3× IRR
              </h3>
              <ul className="mt-2 space-y-2">
                <MetricRow
                  title="Composer 3×"
                  n={irr.within_composer.n_items}
                  jaccard={irr.within_composer.pairwise_avg.jaccard}
                  kappa_macro={irr.within_composer.pairwise_avg.kappa_macro}
                  exact_pct={irr.within_composer.pairwise_avg.exact_pct}
                  kappa_per_label={avgKappaPerLabel(
                    irr.within_composer.pairwise,
                  )}
                  highlight
                  extra={`all3 ${irr.within_composer.n_way.all_identical_pct}%`}
                />
                <MetricRow
                  title="Luna 3×"
                  n={irr.within_luna.n_items}
                  jaccard={irr.within_luna.pairwise_avg.jaccard}
                  kappa_macro={irr.within_luna.pairwise_avg.kappa_macro}
                  exact_pct={irr.within_luna.pairwise_avg.exact_pct}
                  kappa_per_label={avgKappaPerLabel(irr.within_luna.pairwise)}
                  highlight
                  extra={`all3 ${irr.within_luna.n_way.all_identical_pct}%`}
                />
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-medium text-stone-700">
                Cross-judge ({irr.cross.primary_trial})
              </h3>
              <ul className="mt-2 space-y-2">
                <MetricRow
                  title="Luna ↔ Composer"
                  n={irr.cross.pairs.luna_vs_composer.n}
                  jaccard={irr.cross.pairs.luna_vs_composer.jaccard}
                  kappa_macro={irr.cross.pairs.luna_vs_composer.kappa_macro}
                  exact_pct={irr.cross.pairs.luna_vs_composer.exact_pct}
                  kappa_per_label={
                    irr.cross.pairs.luna_vs_composer.kappa_per_label
                  }
                />
                <MetricRow
                  title="Composer ↔ Kevin"
                  n={irr.cross.pairs.composer_vs_kevin.n}
                  jaccard={irr.cross.pairs.composer_vs_kevin.jaccard}
                  kappa_macro={irr.cross.pairs.composer_vs_kevin.kappa_macro}
                  exact_pct={irr.cross.pairs.composer_vs_kevin.exact_pct}
                  kappa_per_label={
                    irr.cross.pairs.composer_vs_kevin.kappa_per_label
                  }
                />
                <MetricRow
                  title="Luna ↔ Kevin"
                  n={irr.cross.pairs.luna_vs_kevin.n}
                  jaccard={irr.cross.pairs.luna_vs_kevin.jaccard}
                  kappa_macro={irr.cross.pairs.luna_vs_kevin.kappa_macro}
                  exact_pct={irr.cross.pairs.luna_vs_kevin.exact_pct}
                  kappa_per_label={
                    irr.cross.pairs.luna_vs_kevin.kappa_per_label
                  }
                />
              </ul>
            </div>
          </Details>
        </section>
      )}

      <section className="rounded-2xl border border-zinc-200 bg-white p-5 sm:p-6">
        <h2 className="mb-3 text-xl font-semibold tracking-tight text-zinc-950">
          Per-item labels
        </h2>
        <p className="mb-2 text-xs text-zinc-500">
          Row tint: humans exact (green) / partial overlap (amber) / disjoint
          (rose). Cell tint vs LLM: exact / partial / disjoint. Rows tagged{" "}
          <span className="font-mono">excl</span> are DataClaw turns; they stay
          labelable but sit outside the figures above.
        </p>
        <div className="max-h-[60vh] overflow-auto rounded-xl border border-zinc-200">
          <table className="w-full min-w-[48rem] border-collapse text-left text-xs">
            <thead className="sticky top-0 bg-zinc-50">
              <tr className="border-b border-zinc-200 text-zinc-600">
                <th className="px-2 py-2 font-medium">#</th>
                <th className="px-2 py-2 font-medium">Item</th>
                {raters.map((r) => (
                  <th key={r.id} className="px-2 py-2 font-medium">
                    {r.displayName}
                  </th>
                ))}
                <th className="px-2 py-2 font-medium">LLM</th>
                <th className="px-2 py-2 font-medium">Humans</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => {
                // Excluded turns feed no statistic, so no agreement tint.
                const rowTint = row.excluded
                  ? "bg-zinc-50 text-zinc-400"
                  : row.humansOverlap === "exact"
                    ? "bg-emerald-50/30"
                    : row.humansOverlap === "partial"
                      ? "bg-amber-50/40"
                      : row.humansOverlap === "disjoint"
                        ? "bg-rose-50/40"
                        : "";

                return (
                  <tr
                    key={row.itemId}
                    className={["border-b border-rule/70", rowTint].join(" ")}
                  >
                    <td className="px-2 py-1.5 font-mono text-stone-500">
                      {row.index}
                    </td>
                    <td className="max-w-[10rem] truncate px-2 py-1.5 font-mono text-stone-600">
                      {row.developer || row.point_id}
                      {row.excluded ? (
                        <span
                          className="ml-1 rounded border border-zinc-300 px-1 text-[10px] uppercase tracking-wide text-zinc-500"
                          title="DataClaw donor — outside the published cohort"
                        >
                          excl
                        </span>
                      ) : null}
                    </td>
                    {raters.map((r) => {
                      const cell = row.labels[r.id]!;
                      const vs = cell.vs_llm;
                      const tint = row.excluded
                        ? ""
                        : vs === "exact"
                          ? "bg-emerald-50/60"
                          : vs === "partial"
                            ? "bg-amber-50/50"
                            : vs === "disjoint"
                              ? "bg-rose-50/40"
                              : "";
                      return (
                        <td
                          key={r.id}
                          className={["px-2 py-1.5", tint].join(" ")}
                          title={cell.note || undefined}
                        >
                          {cell.skipped ? (
                            <span className="text-amber-800">skip</span>
                          ) : cell.labels ? (
                            <Chips labels={cell.labels} />
                          ) : (
                            <span className="text-stone-300">·</span>
                          )}
                        </td>
                      );
                    })}
                    <td className="px-2 py-1.5">
                      <Chips labels={row.llm} />
                    </td>
                    <td className="px-2 py-1.5 font-mono text-[11px]">
                      {row.humansOverlap === "empty"
                        ? "—"
                        : row.humansOverlap === "single"
                          ? "single"
                          : row.humansOverlap}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
