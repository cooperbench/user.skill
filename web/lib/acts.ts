import type { Move } from "./types";

export const ACTS: Move[] = ["approve", "critical", "steer", "inquiry"];
export const ACT_ORDER: Record<Move, number> = {
  approve: 0,
  critical: 1,
  steer: 2,
  inquiry: 3,
};

const ACT_SET = new Set<string>(ACTS);

/** Map retired label ids onto the current vocabulary. */
function canonicalizeAct(raw: string): Move | null {
  const t = raw.trim().toLowerCase();
  if (t === "directive") return "steer";
  if (ACT_SET.has(t)) return t as Move;
  return null;
}

/** Normalize any legacy/single/multi act payload into a stable sorted Move[]. */
export function normalizeActs(raw: unknown): Move[] {
  if (raw == null) return [];
  const list: unknown[] = Array.isArray(raw)
    ? raw
    : typeof raw === "string"
      ? [raw]
      : [];
  const seen = new Set<Move>();
  for (const v of list) {
    if (typeof v !== "string") continue;
    const act = canonicalizeAct(v);
    if (act) seen.add(act);
  }
  return [...seen].sort((a, b) => ACT_ORDER[a] - ACT_ORDER[b]);
}

export function actsEqual(a: Move[], b: Move[]): boolean {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

/** Jaccard over act-sets. Both empty → 1.0 (caller should usually exclude skips). */
export function jaccard(a: Move[], b: Move[]): number {
  if (a.length === 0 && b.length === 0) return 1;
  const A = new Set(a);
  const B = new Set(b);
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  const union = A.size + B.size - inter;
  return union === 0 ? 1 : inter / union;
}

export type OverlapKind = "exact" | "partial" | "disjoint" | "empty";

export function overlapKind(a: Move[], b: Move[]): OverlapKind {
  if (a.length === 0 || b.length === 0) return "empty";
  const score = jaccard(a, b);
  if (score === 1) return "exact";
  if (score === 0) return "disjoint";
  return "partial";
}

export function itemGoldActs(item: {
  gold_acts?: Move[] | string[] | null;
  gold_move?: Move | string | null;
}): Move[] {
  const fromActs = normalizeActs(item.gold_acts);
  if (fromActs.length > 0) return fromActs;
  return normalizeActs(item.gold_move);
}
