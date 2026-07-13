// Upload UserSimBench trial artifacts to Vercel Blob (public) for readers' agents to download.
// Run: BLOB_READ_WRITE_TOKEN=... node scripts/upload-blob.mjs
import { put } from "@vercel/blob";
import { readFileSync, writeFileSync, mkdirSync } from "fs";

const token = process.env.BLOB_READ_WRITE_TOKEN;
if (!token) { console.error("set BLOB_READ_WRITE_TOKEN"); process.exit(1); }
const SRC = process.env.BENCH_SRC || "/Users/kevin/Dev/user.skill/bench/profileopt";
const PFX = "data/condagree_multi";

const files = [
  { local: `${SRC}/experiments/condagree_multi/summary.json`, name: "summary.json", ct: "application/json",
    desc: "Headline results: per (model, condition) next-action prediction accuracy (macro) mean + 95% CI + per-user array; lucky_guess line; real move distribution." },
  { local: `${SRC}/experiments/condagree_multi/manifest.json`, name: "manifest.json", ct: "application/json",
    desc: "Experiment config: the 10 models with backend ids (OpenRouter / Gemini API / Modal) + reasoning efforts + concurrency, split file, taxonomy, judge model, n_per_user, n_points, git sha, timestamp." },
  { local: `${SRC}/experiments/condagree_multi/taxonomy.json`, name: "taxonomy.json", ct: "application/json",
    desc: "The v2 4-way move taxonomy: categories (approve/critical/directive/inquiry), the exact classifier prompt body, OLD->NEW remap from the legacy 7-way, and inter-judge kappa." },
  { local: `${SRC}/splits.json`, name: "splits.json", ct: "application/json",
    desc: "Train/val/test split with NON-OVERLAPPING users AND repos (connected components of the user<->repo graph); qualifying eval-users per split." },
  { local: `${SRC}/experiments/condagree_multi/points.jsonl`, name: "points.jsonl", ct: "application/x-ndjson",
    desc: "The 480 frozen held-out prediction points (one JSON per line): {point_id, slug, repo, turn_index, prev_agent, real_text}." },
  { local: `${SRC}/experiments/condagree_multi/raw.jsonl`, name: "raw.jsonl", ct: "application/x-ndjson",
    desc: "Every trial (one JSON per line). Generation: {key, kind:'gen', point_id, slug, model, model_id, backend, effort, cond('distilled'|'generic'), text, ts, seed?}. Move label: {key:'lab:haiku:<hash>', move}. Join gens to labels via the 4-way classifier on (prev_agent, text)." },
  { local: `${SRC}/experiments/condagree_multi/cases.json`, name: "cases.json", ct: "application/json",
    desc: "Case-study data for glm-5.2 / gemini-3.1-pro / osim-4b: per-developer accuracy ±profile (delta), and every moment where the profile flipped the move (with the agent turn, real message+move, and both ±profile generations+moves)." },
  { local: `${SRC}/experiments/condagree_multi/category_recall.json`, name: "category_recall.json", ct: "application/json",
    desc: "Per-move agree-rate (recall) for all models, both conditions: of moments whose real move was X, the fraction the sim matched. Includes the profile delta per category. Drives the by-category heatmap." },
  { local: `${SRC}/experiments/condagree_multi/verbosity.json`, name: "verbosity.json", ct: "application/json",
    desc: "Average + median message length (words) per model, both conditions, vs the real developers; plus each model's accuracy no-profile/with-profile. Drives the verbosity chart." },
  { local: `${SRC}/experiments/condagree_multi/ablation.json`, name: "ablation.json", ct: "application/json",
    desc: "Contrastive-prefix ablation for glm-5.2 + gpt-5.5: accuracy under no-profile vs the real persona vs a content-free terse style prefix, with spurious-inquiry rate, word count, and per-move recall." },
  { local: `${SRC}/experiments/condagree_multi/scaling_context.json`, name: "scaling_context.json", ct: "application/json",
    desc: "Context-window ablation for gemini-3.5-flash (no profile): accuracy per N=1..10 prior session turns plus the full 14-turn anchor, per-developer values, on all 480 moments and the 166-moment constant-dose (>=10 prior turns) subset. Drives the context-window chart." },
  { local: `${SRC}/experiments/condagree_multi/scaling_flash_k.json`, name: "scaling_flash_k.json", ct: "application/json",
    desc: "Cross-session history sweep for gemini-3.5-flash (no profile): accuracy per K in {0,2,4,8,16,32,64} most recent train turns prepended at the full 14-turn live window (K=0 = the leaderboard generic run), plus K in {8,64} at a 1-turn live window (substitution test), per-developer values and paired tests. Drives the cross-session chart." },
  { local: `${SRC}/experiments/condagree_multi/scaling_grid.json`, name: "scaling_grid.json", ct: "application/json",
    desc: "The completed coarse N x K surface for gemini-3.5-flash (no profile): accuracy at every (N in {1,2,4,8,14} live turns) x (K in {0,4,16,64} history turns) cell, per-developer values, paired K-effect tests at each N and the N1-vs-N14 interaction test. Drives the grid table." },
];

const uploaded = [];
for (const f of files) {
  const body = readFileSync(f.local);
  const { url } = await put(`${PFX}/${f.name}`, body, { access: "public", contentType: f.ct, addRandomSuffix: false, allowOverwrite: true, token });
  uploaded.push({ name: f.name, url, bytes: body.length, description: f.desc });
  console.log(`✓ ${f.name}  ${body.length}b  ${url}`);
}

const index = {
  dataset: "SWESimBench — next-action prediction accuracy; 7 leaderboard simulators (raw includes 2 hidden DeepSeek variants + gemini-3.5-flash, 10 model conditions), repo-disjoint SWE-chat test split",
  generated_from: "website: github.com/AlienKevin/user-simulator (web/) · benchmark code: private repo AlienKevin/user.skill @ swesimbench (available on request)",
  metric: "next-action prediction accuracy = per-developer fraction of held-out moments where the simulator made the same 4-way next action (approve/critical/directive/inquiry) the real developer took, averaged across 20 developers (macro, 95% CI). Chance baseline = lucky_guess (per-developer Sigma p^2), here 0.419.",
  taxonomy: "v2 4-way; single Haiku-4.5 judge (inter-judge kappa ~0.80).",
  split: "20-user test split, user- AND repo-disjoint from train/val.",
  models: ["deepseek-v3.1", "deepseek-v4-flash", "deepseek-v4-pro", "gpt-5.5", "claude-opus-4.8", "glm-5.2", "gemini-3.1-pro", "osim-4b", "osim-8b"],
  conditions: ["generic (no profile)", "distilled (with a distilled user profile)"],
  files: uploaded,
  how_to_analyze: "Fetch summary.json for results. For trial-level analysis fetch raw.jsonl (NDJSON) + points.jsonl; reconstruct prompts via the user.skill repo at manifest.git_sha (validate.build_prompt / osim_backend.build_osim_messages from points + users/<slug>/ folder).",
};
const { url: indexUrl } = await put(`${PFX}/index.json`, JSON.stringify(index, null, 1), { access: "public", contentType: "application/json", addRandomSuffix: false, allowOverwrite: true, token });
console.log(`✓ index.json  ${indexUrl}`);

mkdirSync("app/data", { recursive: true });
writeFileSync("app/data/blobs.json", JSON.stringify({ index: indexUrl, files: uploaded, models: index.models }, null, 1));
console.log("wrote app/data/blobs.json");
