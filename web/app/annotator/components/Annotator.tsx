"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ACTS,
  actsEqual,
  itemGoldActs,
  jaccard,
  normalizeActs,
} from "@/lib/acts";
import type { PublicUser } from "@/lib/users";
import type { Item, Judgment, Meta, Move } from "@/lib/types";
import { HistoryBlocks, MarkdownProse } from "./HistoryBlocks";

const LEGACY_STORAGE_KEY = "swesimbench-annotator-v3-blind-deferred";
const LABELS = ACTS;

const LABEL_COLORS: Record<Move, string> = {
  approve: "bg-emerald-100 text-emerald-900 border-emerald-300",
  critical: "bg-rose-100 text-rose-900 border-rose-300",
  steer: "bg-sky-100 text-sky-900 border-sky-300",
  inquiry: "bg-violet-100 text-violet-900 border-violet-300",
};

function loadLegacyJudgments(): Record<string, Judgment> {
  try {
    const raw = localStorage.getItem(LEGACY_STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as Record<string, Judgment>;
    const out: Record<string, Judgment> = {};
    for (const [id, j] of Object.entries(parsed)) {
      const human = normalizeActs(
        j.human_labels ?? (j as { human_label?: Move | null }).human_label,
      );
      const model = normalizeActs(
        j.model_labels ?? (j as { model_label?: Move }).model_label,
      );
      out[id] = {
        ...j,
        human_labels: j.skipped ? null : human.length ? human : null,
        model_labels: model,
      };
    }
    return out;
  } catch {
    return {};
  }
}

function isLabeled(j?: Judgment): boolean {
  return Boolean(
    j && (j.skipped || (j.human_labels && j.human_labels.length > 0)),
  );
}

function hasOriginalLanguage(item: Item): boolean {
  return Boolean(
    item.translated ||
      item.context_md_original ||
      item.target_md_original ||
      item.real_original,
  );
}

function LabelChips({ labels }: { labels: Move[] | null | undefined }) {
  if (!labels || labels.length === 0) {
    return <span className="font-mono text-stone-500">—</span>;
  }
  return (
    <span className="inline-flex flex-wrap gap-1">
      {labels.map((label) => (
        <span
          key={label}
          className={[
            "rounded-md border px-2 py-0.5 font-mono text-xs font-medium",
            LABEL_COLORS[label],
          ].join(" ")}
        >
          {label}
        </span>
      ))}
    </span>
  );
}

export function Annotator({
  items,
  meta,
  user,
  logout,
}: {
  items: Item[];
  meta: Meta;
  user: PublicUser;
  logout: () => Promise<void>;
}) {
  const searchParams = useSearchParams();
  const [idx, setIdx] = useState(0);
  /** Guards the one-time initial-index resume so labeling never yanks the view. */
  const resumedRef = useRef(false);
  const [judgments, setJudgments] = useState<Record<string, Judgment>>({});
  const [draft, setDraft] = useState<Move[]>([]);
  const [note, setNote] = useState("");
  const [hydrated, setHydrated] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  /** false = English (default); true = original language */
  const [showOriginal, setShowOriginal] = useState(false);
  const [savedToast, setSavedToast] = useState(false);
  /** Brief attention pulse on Next → right after a save/skip. */
  const [nextPulse, setNextPulse] = useState(false);
  const [listOpen, setListOpen] = useState(false);
  /** Soft-guidance body synced from harbor taxonomy_body.txt → public/data/taxonomy.md */
  const [taxonomyMd, setTaxonomyMd] = useState<string>("");
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pulseTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const actsSaveTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const noteSaveTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  /** Pending act selection for debounced persist; null = nothing queued. */
  const pendingActsRef = useRef<{ itemId: string; acts: Move[] } | null>(
    null,
  );
  const pendingNoteRef = useRef<{ itemId: string; note: string } | null>(
    null,
  );
  const listRef = useRef<HTMLDivElement>(null);
  const listCurrentRef = useRef<HTMLButtonElement>(null);
  const contextScrollRef = useRef<HTMLDivElement>(null);
  const judgmentsRef = useRef(judgments);
  judgmentsRef.current = judgments;
  const noteRef = useRef(note);
  noteRef.current = note;
  const itemsRef = useRef(items);
  itemsRef.current = items;

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/data/taxonomy.md");
        if (!res.ok) return;
        const text = await res.text();
        if (!cancelled) setTaxonomyMd(text.trim());
      } catch {
        /* tip is optional; keep panel usable without it */
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
        const res = await fetch("/api/judgments");
        if (!res.ok) {
          throw new Error(`Failed to load judgments (${res.status})`);
        }
        const data = (await res.json()) as {
          judgments: Record<string, Judgment>;
        };
        let next = data.judgments || {};

        // One-time import from legacy localStorage if server is empty.
        if (Object.keys(next).length === 0) {
          const legacy = loadLegacyJudgments();
          const legacyEntries = Object.values(legacy);
          if (legacyEntries.length > 0) {
            await Promise.all(
              legacyEntries.map((j) =>
                fetch("/api/judgments", {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(j),
                }),
              ),
            );
            next = legacy;
            try {
              localStorage.removeItem(LEGACY_STORAGE_KEY);
            } catch {
              /* ignore */
            }
          }
        }

        if (!cancelled) {
          setJudgments(next);
          setHydrated(true);
        }
      } catch (e) {
        if (!cancelled) {
          setLoadError(e instanceof Error ? e.message : "Load failed");
          setHydrated(true);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  /**
   * On first load (once judgments are hydrated) pick the starting item:
   *   1. Honor an explicit deep-link (`?id=<itemId>` or `?i=<1-based index>`).
   *   2. Otherwise resume at the earliest unlabeled turn — "unlabeled" mirrors the
   *      item list's "todo" state: no acts saved AND not skipped (skip counts as done).
   *   3. If everything is done, stay on the last item (its Results row + newest work).
   * Runs once, guarded by `resumedRef`, so saving a label never jumps the view.
   */
  useEffect(() => {
    if (!hydrated || resumedRef.current || items.length === 0) return;
    resumedRef.current = true;

    const idParam = searchParams.get("id");
    if (idParam) {
      const byId = items.findIndex((it) => it.id === idParam);
      if (byId >= 0) {
        setIdx(byId);
        return;
      }
    }
    const iParam = searchParams.get("i") ?? searchParams.get("item");
    if (iParam != null && iParam !== "") {
      const n = Number.parseInt(iParam, 10);
      if (Number.isFinite(n)) {
        const byIndex = items.findIndex((it) => it.index === n);
        const target = byIndex >= 0 ? byIndex : n - 1;
        if (target >= 0 && target < items.length) {
          setIdx(target);
          return;
        }
      }
    }

    const firstUnlabeled = items.findIndex(
      (it) => !isLabeled(judgmentsRef.current[it.id]),
    );
    setIdx(firstUnlabeled >= 0 ? firstUnlabeled : items.length - 1);
    // judgments read via ref; guarded to run once after hydration.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hydrated, items, searchParams]);

  useEffect(() => {
    return () => {
      if (toastTimer.current) clearTimeout(toastTimer.current);
      if (pulseTimer.current) clearTimeout(pulseTimer.current);
      if (actsSaveTimer.current) clearTimeout(actsSaveTimer.current);
      if (noteSaveTimer.current) clearTimeout(noteSaveTimer.current);
    };
  }, []);

  /** Keep the labeling view viewport-locked; only section panes scroll. */
  useEffect(() => {
    const html = document.documentElement;
    const prevHtml = html.style.overflow;
    const prevBody = document.body.style.overflow;
    html.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    return () => {
      html.style.overflow = prevHtml;
      document.body.style.overflow = prevBody;
    };
  }, []);

  useEffect(() => {
    if (!listOpen) return;
    const onDown = (e: MouseEvent) => {
      if (listRef.current && !listRef.current.contains(e.target as Node)) {
        setListOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setListOpen(false);
    };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [listOpen]);

  useEffect(() => {
    if (!listOpen) return;
    listCurrentRef.current?.scrollIntoView({ block: "nearest" });
  }, [listOpen, idx]);

  const item = items[idx];
  const current = item ? judgments[item.id] : undefined;
  /** Has human label/skip — does not imply model reveal. */
  const saved = isLabeled(current);
  const goldActs = item ? itemGoldActs(item) : [];

  const unlabeledIdxs = useMemo(
    () =>
      items
        .map((it, i) => (!isLabeled(judgments[it.id]) ? i : -1))
        .filter((i) => i >= 0),
    [items, judgments],
  );

  const complete = hydrated && unlabeledIdxs.length === 0 && items.length > 0;
  const canToggleOriginal = item ? hasOriginalLanguage(item) : false;

  const flashSaved = useCallback(() => {
    setSavedToast(true);
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setSavedToast(false), 1200);

    setNextPulse(true);
    if (pulseTimer.current) clearTimeout(pulseTimer.current);
    pulseTimer.current = setTimeout(() => setNextPulse(false), 1400);
  }, []);

  const persistForItem = useCallback(
    (
      target: Item,
      human: Move[] | null,
      skipped = false,
      opts?: { toast?: boolean; note?: string },
    ) => {
      const model = itemGoldActs(target);
      const match = human === null ? null : actsEqual(human, model);
      const jac = human === null ? null : jaccard(human, model);
      const noteText = (opts?.note ?? noteRef.current).trim() || undefined;
      const judgment: Judgment = {
        itemId: target.id,
        human_labels: human,
        model_labels: model,
        human_label: human?.[0] ?? null,
        model_label: model[0],
        match,
        jaccard: jac,
        skipped: skipped || undefined,
        note: noteText,
        updatedAt: new Date().toISOString(),
      };
      setJudgments({
        ...judgmentsRef.current,
        [target.id]: judgment,
      });
      if (opts?.toast !== false) flashSaved();
      void fetch("/api/judgments", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(judgment),
      }).catch(() => {
        /* optimistic UI; reload recovers */
      });
    },
    [flashSaved],
  );

  const clearLabelForItem = useCallback(
    (itemId: string, resetLocal: boolean) => {
      if (
        pendingActsRef.current?.itemId === itemId &&
        actsSaveTimer.current
      ) {
        clearTimeout(actsSaveTimer.current);
        actsSaveTimer.current = null;
        pendingActsRef.current = null;
      }
      if (resetLocal && noteSaveTimer.current) {
        clearTimeout(noteSaveTimer.current);
        noteSaveTimer.current = null;
      }
      const next = { ...judgmentsRef.current };
      delete next[itemId];
      setJudgments(next);
      if (resetLocal) {
        setDraft([]);
        setNote("");
      }
      void fetch("/api/judgments", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ itemId, delete: true }),
      }).catch(() => {
        /* ignore */
      });
    },
    [],
  );

  const flushPendingActs = useCallback(() => {
    if (actsSaveTimer.current) {
      clearTimeout(actsSaveTimer.current);
      actsSaveTimer.current = null;
    }
    const pending = pendingActsRef.current;
    pendingActsRef.current = null;
    if (!pending) return;
    const target = itemsRef.current.find((it) => it.id === pending.itemId);
    if (!target) return;
    const acts = normalizeActs(pending.acts);
    if (acts.length === 0) {
      if (isLabeled(judgmentsRef.current[pending.itemId])) {
        clearLabelForItem(pending.itemId, item?.id === pending.itemId);
      }
      return;
    }
    persistForItem(target, acts, false);
  }, [clearLabelForItem, persistForItem, item?.id]);

  const scheduleActsSave = useCallback(
    (itemId: string, acts: Move[]) => {
      pendingActsRef.current = { itemId, acts };
      if (actsSaveTimer.current) clearTimeout(actsSaveTimer.current);
      actsSaveTimer.current = setTimeout(() => {
        actsSaveTimer.current = null;
        flushPendingActs();
      }, 300);
    },
    [flushPendingActs],
  );

  const flushPendingNote = useCallback(() => {
    if (noteSaveTimer.current) {
      clearTimeout(noteSaveTimer.current);
      noteSaveTimer.current = null;
    }
    const pending = pendingNoteRef.current;
    pendingNoteRef.current = null;
    if (!pending) return;
    const target = itemsRef.current.find((it) => it.id === pending.itemId);
    if (!target) return;
    const existing = judgmentsRef.current[pending.itemId];
    if (!isLabeled(existing)) return;
    if (existing.skipped) {
      persistForItem(target, null, true, {
        toast: false,
        note: pending.note,
      });
    } else {
      persistForItem(target, normalizeActs(existing.human_labels), false, {
        toast: false,
        note: pending.note,
      });
    }
  }, [persistForItem]);

  const scheduleNoteSave = useCallback(
    (noteValue: string) => {
      if (!item) return;
      pendingNoteRef.current = { itemId: item.id, note: noteValue };
      if (noteSaveTimer.current) clearTimeout(noteSaveTimer.current);
      noteSaveTimer.current = setTimeout(() => {
        noteSaveTimer.current = null;
        flushPendingNote();
      }, 400);
    },
    [item, flushPendingNote],
  );

  /** Sync draft/note from stored judgment only on navigate / first hydrate. */
  useEffect(() => {
    if (!hydrated || !item) return;
    flushPendingActs();
    flushPendingNote();
    const j = judgmentsRef.current[item.id];
    setNote(j?.note || "");
    if (j?.skipped) setDraft([]);
    else setDraft(normalizeActs(j?.human_labels));
    setShowOriginal(false);
    setNextPulse(false);
    // Only re-sync on item/hydrate change; flush helpers close over latest refs.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item?.id, hydrated]);

  const contextMd =
    showOriginal && canToggleOriginal
      ? item?.context_md_original || item?.context_md || ""
      : item?.context_md || "";
  const targetMd =
    showOriginal && canToggleOriginal
      ? item?.target_md_original ||
        (item?.real_original
          ? `> DEVELOPER\n\n${item.real_original}`
          : item?.target_md) ||
        ""
      : item?.target_md || "";

  /** Default Earlier context to the last pre-target turn (scroll to bottom). */
  useEffect(() => {
    const el = contextScrollRef.current;
    if (!el) return;
    const scrollToEnd = () => {
      el.scrollTop = el.scrollHeight;
    };
    scrollToEnd();
    const raf = requestAnimationFrame(() => {
      scrollToEnd();
      requestAnimationFrame(scrollToEnd);
    });
    // Markdown/layout can settle a beat later
    const t = window.setTimeout(scrollToEnd, 50);
    return () => {
      cancelAnimationFrame(raf);
      window.clearTimeout(t);
    };
  }, [item?.id, contextMd, showOriginal]);

  const goPrev = () => {
    setNextPulse(false);
    setIdx((v) => Math.max(0, v - 1));
  };
  const goNext = () => {
    setNextPulse(false);
    setIdx((v) => Math.min(items.length - 1, v + 1));
  };

  const clearLabel = useCallback(() => {
    if (!item) return;
    if (pendingNoteRef.current?.itemId === item.id) {
      pendingNoteRef.current = null;
    }
    clearLabelForItem(item.id, true);
  }, [item, clearLabelForItem]);

  const toggleAct = useCallback(
    (act: Move) => {
      if (!item) return;
      const itemId = item.id;
      setDraft((prev) => {
        const set = new Set(prev);
        if (set.has(act)) set.delete(act);
        else set.add(act);
        const next = normalizeActs([...set]);
        scheduleActsSave(itemId, next);
        return next;
      });
    },
    [item, scheduleActsSave],
  );

  const skipItem = useCallback(() => {
    if (!item) return;
    if (actsSaveTimer.current) {
      clearTimeout(actsSaveTimer.current);
      actsSaveTimer.current = null;
    }
    if (noteSaveTimer.current) {
      clearTimeout(noteSaveTimer.current);
      noteSaveTimer.current = null;
    }
    pendingActsRef.current = null;
    pendingNoteRef.current = null;
    setDraft([]);
    persistForItem(item, null, true);
  }, [item, persistForItem]);

  const stats = useMemo(() => {
    let exact = 0,
      partial = 0,
      mismatch = 0,
      skip = 0;
    let jacSum = 0;
    let jacN = 0;
    for (const it of items) {
      const j = judgments[it.id];
      if (!isLabeled(j)) continue;
      if (j!.skipped || !j!.human_labels || j!.human_labels.length === 0) {
        skip++;
        continue;
      }
      const gold = itemGoldActs(it);
      const jac = jaccard(j!.human_labels, gold);
      jacSum += jac;
      jacN++;
      if (jac === 1) exact++;
      else if (jac === 0) mismatch++;
      else partial++;
    }
    return {
      exact,
      partial,
      mismatch,
      skip,
      done: exact + partial + mismatch + skip,
      unlabeled: items.length - (exact + partial + mismatch + skip),
      meanJaccard: jacN > 0 ? Math.round((jacSum / jacN) * 1000) / 1000 : null,
    };
  }, [items, judgments]);

  const resultsRows = useMemo(() => {
    if (!complete) return [];
    return items.map((it) => {
      const j = judgments[it.id];
      const human = j?.human_labels ?? null;
      const skipped = Boolean(j?.skipped || !human || human.length === 0);
      const model = itemGoldActs(it);
      const jac = skipped || !human ? null : jaccard(human, model);
      return {
        item: it,
        human,
        model,
        skipped,
        jaccard: jac,
        match: jac === null ? null : jac === 1,
        note: j?.note,
      };
    });
  }, [complete, items, judgments]);

  if (!item) {
    return <p className="p-8">No items loaded.</p>;
  }

  return (
    <div className="mx-auto flex h-dvh max-w-5xl flex-col gap-2 overflow-hidden px-4 py-3 md:px-6">
      <header className="flex shrink-0 flex-col gap-1.5 border-b border-rule pb-2 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
            <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-accent">
              UserBench · MVP
            </p>
            <h1 className="font-display text-xl font-semibold tracking-tight text-ink">
              Gold-act annotator
            </h1>
          </div>
          <p className="mt-0.5 truncate text-xs text-stone-600">
            <span className="font-medium text-ink">{user.displayName}</span>
            {" · "}
            Blind multi-label · model hidden until all {items.length} done
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-1.5 text-sm">
          <span className="rounded-full border border-rule bg-panel px-2.5 py-0.5 font-mono text-xs">
            labeled {hydrated ? stats.done : "…"}/{items.length}
          </span>
          {!complete ? (
            <span className="rounded-full border border-amber-200 bg-amber-50 px-2.5 py-0.5 font-mono text-xs text-amber-900">
              unlabeled {stats.unlabeled}
            </span>
          ) : (
            <>
              <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-0.5 font-mono text-xs text-emerald-900">
                exact {stats.exact}
              </span>
              <span className="rounded-full border border-amber-200 bg-amber-50 px-2.5 py-0.5 font-mono text-xs text-amber-900">
                partial {stats.partial}
              </span>
              <span className="rounded-full border border-rose-200 bg-rose-50 px-2.5 py-0.5 font-mono text-xs text-rose-900">
                disjoint {stats.mismatch}
              </span>
              <span className="rounded-full border border-rule bg-panel px-2.5 py-0.5 font-mono text-xs">
                J̄{" "}
                {stats.meanJaccard === null ? "—" : stats.meanJaccard.toFixed(3)}
              </span>
            </>
          )}
          <Link
            href="/annotator/dashboard"
            className="rounded-full border border-rule bg-panel px-2.5 py-1 text-xs font-medium hover:border-accent"
          >
            Dashboard
          </Link>
          <button
            type="button"
            onClick={() => void logout()}
            className="rounded-full border border-rule px-2.5 py-1 text-xs font-medium text-stone-700 hover:border-accent"
          >
            Log out
          </button>
        </div>
      </header>

      {loadError ? (
        <div
          role="alert"
          className="shrink-0 rounded-md border border-rose-200 bg-rose-50 px-3 py-1.5 text-sm text-rose-900"
        >
          {loadError}
        </div>
      ) : null}

      {savedToast ? (
        <div
          role="status"
          className="fixed right-4 top-4 z-50 rounded-md border border-teal-700/30 bg-teal-800 px-3 py-2 text-sm font-medium text-white shadow-lg"
        >
          Saved
        </div>
      ) : null}

      {complete ? (
        <section className="flex min-h-0 shrink-0 flex-col rounded-lg border border-teal-700/25 bg-panel p-2.5">
          <div className="mb-1.5 flex flex-wrap items-end justify-between gap-2">
            <div>
              <h2 className="font-display text-base text-ink">Results</h2>
              <p className="text-xs text-stone-600">
                All {items.length} done · mean Jaccard vs LLM
              </p>
            </div>
            <div className="flex flex-wrap gap-2.5 font-mono text-xs text-stone-700">
              <span>exact {stats.exact}</span>
              <span>partial {stats.partial}</span>
              <span>disjoint {stats.mismatch}</span>
              <span>skip {stats.skip}</span>
              <span>
                mean J{" "}
                {stats.meanJaccard === null
                  ? "—"
                  : stats.meanJaccard.toFixed(3)}
              </span>
            </div>
          </div>
          <div className="history-scroll max-h-[22vh] overflow-auto rounded border border-rule">
            <table className="w-full min-w-[36rem] border-collapse text-left text-xs">
              <thead className="sticky top-0 bg-paper">
                <tr className="border-b border-rule text-stone-600">
                  <th className="px-2 py-1.5 font-medium">#</th>
                  <th className="px-2 py-1.5 font-medium">Human</th>
                  <th className="px-2 py-1.5 font-medium">Model</th>
                  <th className="px-2 py-1.5 font-medium">Jaccard</th>
                  <th className="px-2 py-1.5 font-medium">Note</th>
                </tr>
              </thead>
              <tbody>
                {resultsRows.map((row) => (
                  <tr
                    key={row.item.id}
                    className={[
                      "border-b border-rule/70 cursor-pointer hover:bg-stone-50",
                      items[idx]?.id === row.item.id ? "bg-teal-50/50" : "",
                    ].join(" ")}
                    onClick={() =>
                      setIdx(items.findIndex((it) => it.id === row.item.id))
                    }
                  >
                    <td className="px-2 py-1 font-mono text-stone-500">
                      {row.item.index}
                    </td>
                    <td className="px-2 py-1">
                      {row.skipped ? (
                        <span className="text-amber-800">skip</span>
                      ) : (
                        <LabelChips labels={row.human} />
                      )}
                    </td>
                    <td className="px-2 py-1">
                      <LabelChips labels={row.model} />
                    </td>
                    <td className="px-2 py-1 font-mono">
                      {row.jaccard === null ? (
                        <span className="text-stone-400">—</span>
                      ) : (
                        <span
                          className={
                            row.jaccard === 1
                              ? "text-emerald-800"
                              : row.jaccard === 0
                                ? "text-rose-800"
                                : "text-amber-800"
                          }
                        >
                          {row.jaccard.toFixed(2)}
                        </span>
                      )}
                    </td>
                    <td className="max-w-[12rem] truncate px-2 py-1 text-stone-500">
                      {row.note || ""}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ) : null}

      <main className="flex min-h-0 flex-1 flex-col gap-2">
        <section className="flex min-h-[7rem] flex-1 flex-col rounded-lg border border-rule bg-panel p-2.5">
          <div className="mb-1 flex shrink-0 flex-wrap items-center justify-between gap-2">
            <h2 className="font-display text-sm text-ink">Earlier context</h2>
            {canToggleOriginal ? (
              <button
                type="button"
                onClick={() => setShowOriginal((v) => !v)}
                className="rounded-md border border-ink/15 bg-ink px-2.5 py-1 text-xs font-medium text-paper hover:bg-stone-800"
              >
                {showOriginal ? "Show English" : "Show original"}
              </button>
            ) : null}
          </div>
          <div
            ref={contextScrollRef}
            className="history-scroll min-h-0 flex-1 overflow-y-auto pr-1"
          >
            {/* Pin turns to the bottom so they sit next to Target turn; scroll up for older. */}
            <div className="flex min-h-full flex-col justify-end">
              <HistoryBlocks
                markdown={contextMd}
                compact
                emptyLabel="No earlier turns before this target."
              />
            </div>
          </div>
        </section>

        <section className="flex max-h-[min(26vh,220px)] shrink-0 flex-col overflow-hidden rounded-lg border border-teal-700/25 bg-panel p-2.5">
          <h2 className="mb-1 shrink-0 font-display text-sm text-ink">
            Target turn{" "}
            <span className="text-xs font-body text-stone-500">(label this)</span>
          </h2>
          <div className="history-scroll min-h-0 flex-1 overflow-y-auto pr-1">
            <HistoryBlocks markdown={targetMd} compact />
          </div>
        </section>

        <section className="shrink-0 rounded-lg border border-rule bg-panel p-2.5">
          <div className="mb-1.5 flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm font-medium text-stone-700">
              Your acts{" "}
              <span className="font-normal text-stone-500">
                (multi-select · ≥1 required)
              </span>
            </p>
            {saved ? (
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-md border border-teal-700/20 bg-teal-50 px-2 py-0.5 text-xs text-teal-900">
                  {current?.skipped
                    ? "Skipped"
                    : `Saved: ${(current?.human_labels || []).join(", ")}`}
                </span>
                <button
                  type="button"
                  onClick={clearLabel}
                  className="text-xs text-stone-500 underline-offset-2 hover:text-stone-800 hover:underline"
                >
                  Relabel
                </button>
              </div>
            ) : null}
          </div>

          {complete && saved ? (
            <div className="mb-1.5 flex flex-wrap items-center gap-3 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-stone-600">You:</span>
                <LabelChips labels={current?.human_labels} />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-stone-600">Model:</span>
                <LabelChips labels={goldActs} />
              </div>
              <span
                className={[
                  "rounded-md border px-2 py-0.5 text-xs font-medium",
                  current?.skipped
                    ? "border-amber-300 bg-amber-50 text-amber-900"
                    : current?.match
                      ? "border-emerald-300 bg-emerald-50 text-emerald-900"
                      : (current?.jaccard ?? 0) > 0
                        ? "border-amber-300 bg-amber-50 text-amber-900"
                        : "border-rose-300 bg-rose-50 text-rose-900",
                ].join(" ")}
              >
                {current?.skipped
                  ? "Skipped"
                  : current?.match
                    ? "Exact match"
                    : `J=${(current?.jaccard ?? 0).toFixed(2)}`}
              </span>
            </div>
          ) : null}

          <div className="flex flex-wrap gap-1.5">
            {LABELS.map((l) => {
              const isSelected = draft.includes(l);
              const dimUnselected = draft.length > 0 && !isSelected;
              return (
                <button
                  key={l}
                  type="button"
                  onClick={() => toggleAct(l)}
                  aria-pressed={isSelected}
                  className={[
                    "rounded-md border px-3 py-1.5 text-sm font-medium hover:opacity-90",
                    LABEL_COLORS[l],
                    isSelected
                      ? "ring-2 ring-offset-1 ring-ink/40"
                      : dimUnselected
                        ? "opacity-40 hover:opacity-70"
                        : "",
                  ].join(" ")}
                >
                  {l}
                </button>
              );
            })}
            <button
              type="button"
              onClick={skipItem}
              className={[
                "rounded-md border border-amber-300 bg-amber-50 px-2.5 py-1.5 text-sm text-amber-900 hover:bg-amber-100",
                saved && current?.skipped
                  ? "ring-2 ring-offset-1 ring-ink/40"
                  : "",
              ].join(" ")}
              title="Skip for now — jump back via the item list"
            >
              Unsure / skip
            </button>
          </div>
          <p className="mt-1 text-[11px] leading-snug text-stone-500">
            Toggle any combination — saves automatically. Clearing all acts
            unlabels the item.
          </p>
          <textarea
            value={note}
            onChange={(e) => {
              const value = e.target.value;
              setNote(value);
              scheduleNoteSave(value);
            }}
            rows={1}
            placeholder="Optional note… (auto-saves when labeled)"
            className="mt-1.5 w-full resize-none rounded-md border border-rule bg-paper px-2.5 py-1.5 text-sm outline-none focus:border-accent"
          />
          <details className="mt-1.5 rounded border border-rule bg-paper px-2.5 py-1.5 text-xs text-stone-600">
            <summary className="cursor-pointer font-medium text-stone-700">
              Taxonomy (free multi-label)
            </summary>
            <div className="mt-2 max-h-[40vh] overflow-y-auto pr-1">
              <p className="text-stone-500">
                Select every act that applies. At least one act required (empty
                selection clears the label).
              </p>
              {taxonomyMd ? (
                <MarkdownProse
                  body={taxonomyMd}
                  compact
                  className="taxonomy-prose mt-2 text-xs leading-snug text-stone-600 [&_em]:italic [&_strong]:font-semibold [&_li]:text-xs [&_p]:mb-1.5 [&_p]:text-xs [&_ul]:mb-1.5 [&_ul]:space-y-1"
                />
              ) : null}
            </div>
          </details>
        </section>

        <nav className="sticky bottom-0 z-10 flex shrink-0 flex-wrap items-center gap-2 rounded-lg border border-rule bg-panel/95 px-3 py-1.5 shadow-sm backdrop-blur">
          <button
            type="button"
            disabled={idx === 0}
            onClick={goPrev}
            className="rounded-md border border-rule px-3 py-1.5 text-sm disabled:opacity-40"
          >
            ← Previous
          </button>
          <button
            type="button"
            disabled={idx >= items.length - 1}
            onClick={goNext}
            className={[
              "rounded-md px-3 py-1.5 text-sm disabled:opacity-40",
              saved
                ? "bg-accent font-medium text-white hover:bg-teal-800"
                : "border border-rule",
              nextPulse && saved ? "next-pulse" : "",
            ].join(" ")}
          >
            Next →
          </button>

          <div className="relative ml-auto" ref={listRef}>
            <button
              type="button"
              onClick={() => setListOpen((o) => !o)}
              aria-expanded={listOpen}
              aria-haspopup="listbox"
              className="flex items-center gap-1.5 rounded-md border border-rule px-2.5 py-1.5 font-mono text-xs text-stone-600 hover:border-accent hover:text-ink"
              title="Jump to any item"
            >
              <span>
                #{item.index}/{items.length}
                {item.developer ? ` · ${item.developer}` : ""}
              </span>
              <span className="text-stone-400" aria-hidden>
                {listOpen ? "▴" : "▾"}
              </span>
            </button>

            {listOpen ? (
              <div
                role="listbox"
                aria-label="Annotation items"
                className="absolute bottom-full right-0 z-20 mb-2 max-h-72 w-72 overflow-y-auto rounded-lg border border-rule bg-panel shadow-lg history-scroll"
              >
                <div className="sticky top-0 z-10 border-b border-rule bg-panel px-3 py-2 font-sans text-[11px] uppercase tracking-wide text-stone-500">
                  Jump to item
                  {unlabeledIdxs.length ? (
                    <span className="ml-1.5 normal-case tracking-normal text-amber-800">
                      · {unlabeledIdxs.length} unlabeled
                    </span>
                  ) : (
                    <span className="ml-1.5 normal-case tracking-normal text-emerald-800">
                      · all done
                    </span>
                  )}
                </div>
                <ul className="py-1">
                  {items.map((it, i) => {
                    const j = judgments[it.id];
                    const labeled = isLabeled(j);
                    const skipped = Boolean(j?.skipped);
                    const isCurrent = i === idx;
                    return (
                      <li key={it.id}>
                        <button
                          type="button"
                          role="option"
                          aria-selected={isCurrent}
                          ref={isCurrent ? listCurrentRef : undefined}
                          onClick={() => {
                            setIdx(i);
                            setListOpen(false);
                          }}
                          className={[
                            "flex w-full items-center gap-2 px-3 py-1.5 text-left",
                            isCurrent
                              ? "bg-teal-50 ring-1 ring-inset ring-accent/30"
                              : "hover:bg-stone-100/80",
                            !labeled && !isCurrent ? "bg-amber-50/40" : "",
                          ].join(" ")}
                        >
                          <span className="w-7 shrink-0 font-mono text-xs text-stone-500">
                            #{it.index}
                          </span>
                          <span
                            className={[
                              "min-w-0 flex-1 truncate font-mono text-xs",
                              labeled ? "text-stone-600" : "font-medium text-ink",
                            ].join(" ")}
                          >
                            {it.developer || it.id}
                          </span>
                          {skipped ? (
                            <span className="shrink-0 rounded border border-amber-200 bg-amber-50 px-1.5 py-0.5 font-mono text-[10px] text-amber-900">
                              skip
                            </span>
                          ) : labeled ? (
                            <span
                              className="shrink-0 font-mono text-xs text-emerald-700"
                              aria-label="labeled"
                            >
                              ✓
                            </span>
                          ) : (
                            <span className="shrink-0 rounded border border-amber-300 bg-amber-50 px-1.5 py-0.5 font-mono text-[10px] font-medium text-amber-900">
                              todo
                            </span>
                          )}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ) : null}
          </div>
        </nav>
      </main>
    </div>
  );
}
