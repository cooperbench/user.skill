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
  viewer: PublicUser;
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
}: {
  title: string;
  n: number;
  jaccard: number | null;
  kappa_macro: number | null;
  exact_pct: number | null;
  kappa_per_label: KappaMap;
  highlight?: boolean;
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

export function DashboardView({
  user,
  logout,
}: {
  user: PublicUser;
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
          "/data/judge_trials/irr_cross_summary_20260718.json",
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

  const { raters, rows, agreement, progress } = data;

  // Hide empty rows: only show cards / agreement rows that actually have data.
  const progressWithData = progress.filter((p) => p.done > 0);
  const pairwiseWithData = agreement.pairwise.filter((pair) => pair.n > 0);
  const perRaterWithData = agreement.humanVsLlm.perRater.filter(
    (row) => row.n > 0,
  );

  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-5 px-4 py-6 md:px-6">
      <header className="flex flex-col gap-3 border-b border-rule pb-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-accent">
            UserBench · Dashboard
          </p>
          <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">
            Inter-rater comparison
          </h1>
          <p className="mt-1 max-w-2xl text-sm text-stone-600">
            Free multi-label acts. Primary metrics: mean Jaccard over act-sets
            and per-label Cohen&apos;s κ. Signed in as{" "}
            <span className="font-medium text-ink">{user.displayName}</span>.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <Link
            href="/annotator"
            className="rounded-full border border-rule bg-panel px-3 py-1.5 text-xs font-medium hover:border-accent"
          >
            ← Annotator
          </Link>
          <button
            type="button"
            onClick={() => void logout()}
            className="rounded-full border border-ink/15 bg-ink px-3 py-1.5 text-xs font-medium text-paper hover:bg-stone-800"
          >
            Log out
          </button>
        </div>
      </header>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {progressWithData.map((p) => (
          <div
            key={p.userId}
            className="rounded-lg border border-rule bg-panel px-4 py-3"
          >
            <p className="font-medium text-ink">{nameOf(raters, p.userId)}</p>
            <p className="mt-1 font-mono text-xs text-stone-600">
              {p.done}/{p.total} done · {p.labeled} labeled · {p.skipped} skip
            </p>
          </div>
        ))}
      </section>

      <section className="rounded-lg border border-rule bg-panel p-4">
        <h2 className="font-display text-lg text-ink">Agreement summary</h2>
        <p className="mt-1 text-xs text-stone-500">
          Jaccard = |A∩B|/|A∪B| averaged over items both parties labeled
          (skips excluded). Per-label κ is binary presence/absence for each of
          the 4 acts; κ̄ is the macro-average. Exact-set % is secondary.
        </p>

        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <h3 className="text-sm font-medium text-stone-700">
              Pairwise human agreement
            </h3>
            <ul className="mt-2 space-y-2 text-sm">
              {pairwiseWithData.length === 0 && (
                <li className="rounded border border-rule/60 bg-paper/60 px-2 py-1.5 font-mono text-xs text-stone-400">
                  No overlapping human pairs yet.
                </li>
              )}
              {pairwiseWithData.map((pair) => (
                <li
                  key={`${pair.a}-${pair.b}`}
                  className="rounded border border-rule/60 bg-paper/60 px-2 py-1.5 font-mono text-xs"
                >
                  <div className="flex flex-wrap items-baseline gap-x-2">
                    <span className="font-medium text-ink">
                      {nameOf(raters, pair.a)} ↔ {nameOf(raters, pair.b)}
                    </span>
                    <span className="text-stone-500">n={pair.n}</span>
                    <span className="text-accent">
                      J={fmt(pair.jaccard)}
                    </span>
                    <span>κ̄={fmt(pair.kappa_macro)}</span>
                    <span className="text-stone-500">
                      exact{" "}
                      {pair.exact_pct === null ? "—" : `${pair.exact_pct}%`}
                    </span>
                  </div>
                  <div className="mt-0.5">
                    <KappaRow kappa={pair.kappa_per_label} />
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-medium text-stone-700">
              Human vs LLM gold
            </h3>
            <ul className="mt-2 space-y-2 text-sm">
              {perRaterWithData.map((row) => (
                <li
                  key={row.userId}
                  className="rounded border border-rule/60 bg-paper/60 px-2 py-1.5 font-mono text-xs"
                >
                  <div className="flex flex-wrap items-baseline gap-x-2">
                    <span className="font-medium text-ink">
                      {nameOf(raters, row.userId)} vs LLM
                    </span>
                    <span className="text-stone-500">n={row.n}</span>
                    <span className="text-accent">J={fmt(row.jaccard)}</span>
                    <span>κ̄={fmt(row.kappa_macro)}</span>
                    <span className="text-stone-500">
                      exact{" "}
                      {row.exact_pct === null ? "—" : `${row.exact_pct}%`}
                    </span>
                  </div>
                  <div className="mt-0.5">
                    <KappaRow kappa={row.kappa_per_label} />
                  </div>
                </li>
              ))}
              {agreement.humanVsLlm.pooled.n > 0 && (
              <li className="rounded border border-accent/30 bg-teal-50/40 px-2 py-1.5 font-mono text-xs font-medium">
                <div className="flex flex-wrap items-baseline gap-x-2">
                  <span>Pooled humans vs LLM</span>
                  <span className="text-stone-500">
                    n={agreement.humanVsLlm.pooled.n}
                  </span>
                  <span className="text-accent">
                    J={fmt(agreement.humanVsLlm.pooled.jaccard)}
                  </span>
                  <span>
                    κ̄={fmt(agreement.humanVsLlm.pooled.kappa_macro)}
                  </span>
                  <span className="text-stone-500">
                    exact{" "}
                    {agreement.humanVsLlm.pooled.exact_pct === null
                      ? "—"
                      : `${agreement.humanVsLlm.pooled.exact_pct}%`}
                  </span>
                </div>
                <div className="mt-0.5 font-normal">
                  <KappaRow
                    kappa={agreement.humanVsLlm.pooled.kappa_per_label}
                  />
                </div>
              </li>
              )}
            </ul>
          </div>
        </div>
      </section>

      {irr && (
        <section className="rounded-lg border border-rule bg-panel p-4">
          <h2 className="font-display text-lg text-ink">
            Judge IRR (independent trials)
          </h2>
          <p className="mt-1 text-xs text-stone-500">
            LLM-judge reliability from re-running the judge on the same items.
            Within-model = 3 independent trials of one judge (mean over the 3
            pairwise comparisons). Cross = one trial per judge on the shared
            items ({irr.cross.primary_trial}). trial_1 Composer = production
            gold_acts (post-rejudge), so Composer↔Kevin here matches the
            live Kevin-vs-gold section. Same J / κ̄ / per-label κ definitions as
            above.
          </p>

          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <h3 className="text-sm font-medium text-stone-700">
                Within-model 3× IRR (mean pairwise, per-label κ averaged)
              </h3>
              <ul className="mt-2 space-y-2 text-sm">
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
                />
                <MetricRow
                  title="Luna 3×"
                  n={irr.within_luna.n_items}
                  jaccard={irr.within_luna.pairwise_avg.jaccard}
                  kappa_macro={irr.within_luna.pairwise_avg.kappa_macro}
                  exact_pct={irr.within_luna.pairwise_avg.exact_pct}
                  kappa_per_label={avgKappaPerLabel(irr.within_luna.pairwise)}
                  highlight
                />
              </ul>
              <p className="mt-1.5 font-mono text-[11px] text-stone-500">
                all-3-identical: Composer{" "}
                {irr.within_composer.n_way.all_identical_pct}% · Luna{" "}
                {irr.within_luna.n_way.all_identical_pct}%
              </p>
            </div>

            <div>
              <h3 className="text-sm font-medium text-stone-700">
                Cross-judge agreement ({irr.cross.primary_trial})
              </h3>
              <ul className="mt-2 space-y-2 text-sm">
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
          </div>
        </section>
      )}

      <section className="rounded-lg border border-rule bg-panel p-4">
        <h2 className="mb-3 font-display text-lg text-ink">Per-item labels</h2>
        <p className="mb-2 text-xs text-stone-500">
          Row tint: humans exact (green) / partial overlap (amber) / disjoint
          (rose). Cell tint vs LLM: exact / partial / disjoint.
        </p>
        <div className="max-h-[60vh] overflow-auto rounded border border-rule">
          <table className="w-full min-w-[48rem] border-collapse text-left text-xs">
            <thead className="sticky top-0 bg-paper">
              <tr className="border-b border-rule text-stone-600">
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
                const rowTint =
                  row.humansOverlap === "exact"
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
                    </td>
                    {raters.map((r) => {
                      const cell = row.labels[r.id]!;
                      const vs = cell.vs_llm;
                      const tint =
                        vs === "exact"
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
