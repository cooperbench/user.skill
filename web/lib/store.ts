import { Redis } from "@upstash/redis";
import { actsEqual, normalizeActs } from "./acts";
import type { Judgment, Move } from "./types";

function redis(): Redis {
  return Redis.fromEnv();
}

function userKey(userId: string): string {
  return `judgments:${userId}`;
}

/** Coerce legacy single-label judgments into multi-label shape. */
export function coerceJudgment(raw: unknown): Judgment | null {
  if (raw == null) return null;
  try {
    const value =
      typeof raw === "string"
        ? (JSON.parse(raw) as Record<string, unknown>)
        : (raw as Record<string, unknown>);
    if (!value || typeof value !== "object" || !("itemId" in value)) return null;

    const itemId = String(value.itemId);
    const skipped = Boolean(value.skipped);

    let human_labels: Move[] | null = null;
    if ("human_labels" in value) {
      human_labels = normalizeActs(value.human_labels);
    } else if ("human_label" in value) {
      human_labels = normalizeActs(value.human_label);
    }
    if (skipped) {
      human_labels = null;
    } else if (!human_labels || human_labels.length === 0) {
      human_labels = null;
    }

    let model_labels = normalizeActs(value.model_labels);
    if (model_labels.length === 0) {
      model_labels = normalizeActs(value.model_label);
    }

    const match =
      value.match === undefined
        ? human_labels === null
          ? null
          : actsEqual(human_labels, model_labels)
        : (value.match as boolean | null);

    const jaccard =
      typeof value.jaccard === "number" || value.jaccard === null
        ? (value.jaccard as number | null)
        : undefined;

    return {
      itemId,
      human_labels,
      model_labels,
      // Keep legacy mirrors for older clients / exports.
      human_label: human_labels?.[0] ?? null,
      model_label: model_labels[0],
      match,
      jaccard,
      skipped: skipped || undefined,
      note: typeof value.note === "string" ? value.note : undefined,
      updatedAt:
        typeof value.updatedAt === "string"
          ? value.updatedAt
          : new Date().toISOString(),
    };
  } catch {
    return null;
  }
}

export async function getUserJudgments(
  userId: string,
): Promise<Record<string, Judgment>> {
  const data = await redis().hgetall<Record<string, unknown>>(userKey(userId));
  if (!data) return {};
  const out: Record<string, Judgment> = {};
  for (const [itemId, raw] of Object.entries(data)) {
    const j = coerceJudgment(raw);
    if (j) out[itemId] = j;
  }
  return out;
}

export async function upsertJudgment(
  userId: string,
  judgment: Judgment,
): Promise<Judgment> {
  await redis().hset(userKey(userId), {
    [judgment.itemId]: JSON.stringify(judgment),
  });
  return judgment;
}

export async function deleteJudgment(
  userId: string,
  itemId: string,
): Promise<void> {
  await redis().hdel(userKey(userId), itemId);
}

export async function getAllJudgments(
  userIds: string[],
): Promise<Record<string, Record<string, Judgment>>> {
  const out: Record<string, Record<string, Judgment>> = {};
  await Promise.all(
    userIds.map(async (userId) => {
      out[userId] = await getUserJudgments(userId);
    }),
  );
  return out;
}
