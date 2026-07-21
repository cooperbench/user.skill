import { ACTS, jaccard, normalizeActs } from "./acts";
import type { Move } from "./types";

export type PairAgreement = {
  a: string;
  b: string;
  n: number;
  /** Mean Jaccard across co-labeled items. */
  jaccard: number | null;
  /** Macro-average per-label Cohen's κ. */
  kappa_macro: number | null;
  /** Per-label binary Cohen's κ. */
  kappa_per_label: Record<Move, number | null>;
  /** Secondary: exact set-match %. */
  exact_pct: number | null;
};

export type RaterVsLlm = {
  userId: string;
  n: number;
  jaccard: number | null;
  kappa_macro: number | null;
  kappa_per_label: Record<Move, number | null>;
  exact_pct: number | null;
};

function round1(n: number): number {
  return Math.round(n * 10) / 10;
}

function round3(n: number): number {
  return Math.round(n * 1000) / 1000;
}

/** Binary Cohen's κ for presence/absence of one label. */
export function binaryCohensKappa(
  a: boolean[],
  b: boolean[],
): number | null {
  const n = Math.min(a.length, b.length);
  if (n === 0) return null;
  let both1 = 0;
  let both0 = 0;
  let a1b0 = 0;
  let a0b1 = 0;
  for (let i = 0; i < n; i++) {
    const x = a[i]!;
    const y = b[i]!;
    if (x && y) both1++;
    else if (!x && !y) both0++;
    else if (x && !y) a1b0++;
    else a0b1++;
  }
  const po = (both1 + both0) / n;
  const pYesA = (both1 + a1b0) / n;
  const pYesB = (both1 + a0b1) / n;
  const pe = pYesA * pYesB + (1 - pYesA) * (1 - pYesB);
  if (pe >= 1) return 1;
  return round3((po - pe) / (1 - pe));
}

function pairsFromSets(
  labelsA: (Move[] | null)[],
  labelsB: (Move[] | null)[],
): [Move[], Move[]][] {
  const pairs: [Move[], Move[]][] = [];
  for (let i = 0; i < labelsA.length; i++) {
    const a = labelsA[i];
    const b = labelsB[i];
    if (a && b && a.length > 0 && b.length > 0) pairs.push([a, b]);
  }
  return pairs;
}

export function setAgreement(
  labelsA: (Move[] | null)[],
  labelsB: (Move[] | null)[],
): {
  n: number;
  jaccard: number | null;
  kappa_macro: number | null;
  kappa_per_label: Record<Move, number | null>;
  exact_pct: number | null;
} {
  const pairs = pairsFromSets(labelsA, labelsB);
  const n = pairs.length;
  const emptyKappa = Object.fromEntries(ACTS.map((c) => [c, null])) as Record<
    Move,
    number | null
  >;
  if (n === 0) {
    return {
      n: 0,
      jaccard: null,
      kappa_macro: null,
      kappa_per_label: emptyKappa,
      exact_pct: null,
    };
  }

  let jacSum = 0;
  let exact = 0;
  const kappa_per_label = { ...emptyKappa };
  const kappas: number[] = [];

  for (const label of ACTS) {
    const binA = pairs.map(([a]) => a.includes(label));
    const binB = pairs.map(([, b]) => b.includes(label));
    const k = binaryCohensKappa(binA, binB);
    kappa_per_label[label] = k;
    if (k != null) kappas.push(k);
  }

  for (const [a, b] of pairs) {
    const j = jaccard(a, b);
    jacSum += j;
    if (j === 1) exact++;
  }

  return {
    n,
    jaccard: round3(jacSum / n),
    kappa_macro: kappas.length
      ? round3(kappas.reduce((s, x) => s + x, 0) / kappas.length)
      : null,
    kappa_per_label,
    exact_pct: round1((exact / n) * 100),
  };
}

export function pairwiseAgreements(
  raterIds: string[],
  /** itemId -> userId -> acts (null if skip/missing) */
  byItem: Record<string, Record<string, Move[] | null | undefined>>,
): PairAgreement[] {
  const pairs: PairAgreement[] = [];
  for (let i = 0; i < raterIds.length; i++) {
    for (let j = i + 1; j < raterIds.length; j++) {
      const a = raterIds[i]!;
      const b = raterIds[j]!;
      const labelsA: (Move[] | null)[] = [];
      const labelsB: (Move[] | null)[] = [];
      for (const itemId of Object.keys(byItem)) {
        const row = byItem[itemId]!;
        if (row[a] === undefined && row[b] === undefined) continue;
        labelsA.push(row[a] ?? null);
        labelsB.push(row[b] ?? null);
      }
      const stats = setAgreement(labelsA, labelsB);
      pairs.push({ a, b, ...stats });
    }
  }
  return pairs;
}

export function humanVsLlm(
  raterIds: string[],
  byItem: Record<string, Record<string, Move[] | null | undefined>>,
  goldByItem: Record<string, Move[]>,
): { perRater: RaterVsLlm[]; pooled: Omit<RaterVsLlm, "userId"> } {
  const perRater: RaterVsLlm[] = raterIds.map((userId) => {
    const human: (Move[] | null)[] = [];
    const llm: (Move[] | null)[] = [];
    for (const [itemId, gold] of Object.entries(goldByItem)) {
      const h = byItem[itemId]?.[userId];
      if (h === undefined) continue;
      human.push(h ?? null);
      llm.push(normalizeActs(gold));
    }
    const stats = setAgreement(human, llm);
    return { userId, ...stats };
  });

  const allH: (Move[] | null)[] = [];
  const allL: (Move[] | null)[] = [];
  for (const userId of raterIds) {
    for (const [itemId, gold] of Object.entries(goldByItem)) {
      const h = byItem[itemId]?.[userId];
      if (h === undefined || h === null || h.length === 0) continue;
      allH.push(h);
      allL.push(normalizeActs(gold));
    }
  }
  const pooled = setAgreement(allH, allL);
  return { perRater, pooled };
}

export { jaccard };
