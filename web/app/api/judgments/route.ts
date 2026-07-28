import { NextResponse } from "next/server";
import { actsEqual, jaccard, normalizeActs } from "@/lib/acts";
import { getSessionUser } from "@/lib/auth";
import {
  deleteJudgment,
  getUserJudgments,
  upsertJudgment,
} from "@/lib/store";
import type { Judgment, Move } from "@/lib/types";

export async function GET() {
  const user = await getSessionUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const judgments = await getUserJudgments(user.id);
  return NextResponse.json({ judgments, user });
}

export async function PUT(req: Request) {
  const user = await getSessionUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let body: {
    itemId?: string;
    human_labels?: Move[] | null;
    human_label?: Move | null;
    model_labels?: Move[];
    model_label?: Move;
    match?: boolean | null;
    jaccard?: number | null;
    skipped?: boolean;
    note?: string;
    delete?: boolean;
  };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const itemId = body.itemId?.trim();
  if (!itemId) {
    return NextResponse.json({ error: "itemId required" }, { status: 400 });
  }

  if (body.delete) {
    await deleteJudgment(user.id, itemId);
    return NextResponse.json({ ok: true, deleted: itemId });
  }

  const skipped = Boolean(body.skipped);
  let human_labels: Move[] | null = null;
  if (!skipped) {
    const raw =
      body.human_labels !== undefined ? body.human_labels : body.human_label;
    human_labels = normalizeActs(raw);
    if (human_labels.length === 0) {
      return NextResponse.json(
        { error: "human_labels must be a non-empty subset of the 4 acts" },
        { status: 400 },
      );
    }
  }

  const model_labels = normalizeActs(
    body.model_labels !== undefined ? body.model_labels : body.model_label,
  );
  if (model_labels.length === 0) {
    return NextResponse.json(
      { error: "model_labels required (non-empty)" },
      { status: 400 },
    );
  }

  const match =
    body.match === undefined
      ? human_labels === null
        ? null
        : actsEqual(human_labels, model_labels)
      : body.match;

  const jac =
    body.jaccard !== undefined
      ? body.jaccard
      : human_labels === null
        ? null
        : jaccard(human_labels, model_labels);

  const judgment: Judgment = {
    itemId,
    human_labels,
    model_labels,
    human_label: human_labels?.[0] ?? null,
    model_label: model_labels[0],
    match,
    jaccard: jac,
    skipped: skipped || undefined,
    note: body.note?.trim() || undefined,
    updatedAt: new Date().toISOString(),
  };

  await upsertJudgment(user.id, judgment);
  return NextResponse.json({ judgment });
}
