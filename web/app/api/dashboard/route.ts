import { NextResponse } from "next/server";
import { humanVsLlm, pairwiseAgreements } from "@/lib/agreement";
import { itemGoldActs, normalizeActs, overlapKind } from "@/lib/acts";
import { getSessionUser } from "@/lib/auth";
import { getAllJudgments } from "@/lib/store";
import type { Item, Move } from "@/lib/types";
import { listUsers } from "@/lib/users";
import items from "@/public/data/items.json";

export async function GET() {
  const user = await getSessionUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const raters = listUsers();
  const raterIds = raters.map((r) => r.id);
  const allJudgments = await getAllJudgments(raterIds);
  const typedItems = items as Item[];

  const goldByItem: Record<string, Move[]> = {};
  const byItem: Record<string, Record<string, Move[] | null | undefined>> = {};

  for (const item of typedItems) {
    goldByItem[item.id] = itemGoldActs(item);
    byItem[item.id] = {};
    for (const r of raterIds) {
      const j = allJudgments[r]?.[item.id];
      if (!j) continue;
      if (j.skipped || !j.human_labels || j.human_labels.length === 0) {
        byItem[item.id]![r] = null;
      } else {
        byItem[item.id]![r] = normalizeActs(j.human_labels);
      }
    }
  }

  const rows = typedItems.map((item) => {
    const llm = itemGoldActs(item);
    const labels: Record<
      string,
      {
        labels: Move[] | null;
        skipped: boolean;
        note?: string;
        updatedAt?: string;
        vs_llm?: "exact" | "partial" | "disjoint" | "empty";
      }
    > = {};
    const humanSets: Move[][] = [];
    for (const r of raterIds) {
      const j = allJudgments[r]?.[item.id];
      if (!j) {
        labels[r] = { labels: null, skipped: false };
      } else {
        const skipped = Boolean(
          j.skipped || !j.human_labels || j.human_labels.length === 0,
        );
        const acts = skipped ? null : normalizeActs(j.human_labels);
        if (acts) humanSets.push(acts);
        labels[r] = {
          labels: acts,
          skipped,
          note: j.note,
          updatedAt: j.updatedAt,
          vs_llm: skipped || !acts ? "empty" : overlapKind(acts, llm),
        };
      }
    }

    let humansOverlap: "exact" | "partial" | "disjoint" | "empty" | "single" =
      "empty";
    if (humanSets.length === 1) humansOverlap = "single";
    else if (humanSets.length >= 2) {
      // Pairwise worst-case among humans for row tinting.
      let worst: "exact" | "partial" | "disjoint" = "exact";
      for (let i = 0; i < humanSets.length; i++) {
        for (let j = i + 1; j < humanSets.length; j++) {
          const k = overlapKind(humanSets[i]!, humanSets[j]!);
          if (k === "disjoint") worst = "disjoint";
          else if (k === "partial" && worst !== "disjoint") worst = "partial";
        }
      }
      humansOverlap = worst;
    }

    return {
      itemId: item.id,
      index: item.index,
      developer: item.developer,
      point_id: item.point_id,
      llm,
      labels,
      humansOverlap,
    };
  });

  const progress = raterIds.map((id) => {
    const judgments = allJudgments[id] || {};
    let labeled = 0;
    let skipped = 0;
    for (const item of typedItems) {
      const j = judgments[item.id];
      if (!j) continue;
      if (j.skipped || !j.human_labels || j.human_labels.length === 0) skipped++;
      else labeled++;
    }
    return {
      userId: id,
      labeled,
      skipped,
      done: labeled + skipped,
      total: typedItems.length,
    };
  });

  const pairwise = pairwiseAgreements(raterIds, byItem);
  const vsLlm = humanVsLlm(raterIds, byItem, goldByItem);

  return NextResponse.json({
    viewer: user,
    raters,
    progress,
    rows,
    agreement: {
      pairwise,
      humanVsLlm: vsLlm,
      metrics: "jaccard + per-label kappa",
    },
  });
}
