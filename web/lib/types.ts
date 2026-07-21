export type Move = "approve" | "critical" | "steer" | "inquiry";

export type PublicUser = {
  id: string;
  displayName: string;
};

export type Item = {
  id: string;
  index: number;
  source: string;
  task_id: string;
  point_id: string;
  developer: string;
  /** Legacy primary act (first of gold_acts). */
  gold_move?: Move | string;
  /** Multi-label model/gold acts. */
  gold_acts?: Move[] | string[];
  prev_agent?: string;
  real: string;
  context_md: string;
  target_md: string;
  judge_model?: string;
  /** True when display fields differ from stored originals. */
  translated?: boolean;
  real_original?: string;
  context_md_original?: string;
  target_md_original?: string;
  prev_agent_original?: string;
};

export type Judgment = {
  itemId: string;
  human_labels: Move[] | null;
  model_labels: Move[];
  /** Legacy mirrors */
  human_label?: Move | null;
  model_label?: Move;
  match: boolean | null;
  jaccard?: number | null;
  skipped?: boolean;
  note?: string;
  updatedAt: string;
};

export type Meta = {
  title?: string;
  n_items?: number;
  labels?: Move[];
  taxonomy: Record<string, string>;
  notes?: string;
  judge_model?: string;
  multi_label?: boolean;
  gold_mode?: string;
  n_multi_label_gold?: number;
  translated_to_english?: boolean;
  [key: string]: unknown;
};
