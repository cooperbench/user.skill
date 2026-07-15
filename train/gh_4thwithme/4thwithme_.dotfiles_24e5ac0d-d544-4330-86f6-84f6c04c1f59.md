> DEVELOPER

check replay file...can you extract from replay data about type game fraction, and length? @replays/examples/swg_vs_tox_domi_vs_scuba__[GameReplays.org].rep

> AGENT

Results for `swg_vs_tox_domi_vs_scuba__[GameReplays.org].rep`:

| Field | Value |
|-------|-------|
| **Game type** | 1v1 (`original_game_mode=1`, 2 human players) |
| **Map** | Canyon of the Dead v1 (ranked) |
| **Duration** | 36.77 min (2206.4s) |
| **Player 1** | `[GoDs]Odin` — **GLA** (team 6) |
| **Player 2** | `pLaYeR^oNe` — **GLA** (team 3) |
| **Completed** | Yes (no desync, no quit_early) |
| **Total commands** | 13,247 |

Both players are GLA. The `TT` faction code in the raw options string maps to GLA via `FACTION_CODE_MAP`.

> DEVELOPER

check all other games for me @replays/examples/

> AGENT

| File | Mode | Players | Factions | Duration | Map |
|------|------|---------|----------|----------|-----|
| `00000000` | 1 | 2 (1v1) | GLA vs GLA | 30.00 min | Gorge Drought |
| `12-40-26_OoETruCK_akaHuMMi` | 1 | 3 | All America | 8.59 min | Blue Hole ZH v1 |
| `18_50_26_Haubibba_Alphasta` | 5 | 3 | All GLA | 14.05 min | TD NoBugsCars ZH v1 |
| `19-11-22_OoEExCaL_OoEMarak` | 1 | 3 | All GLA | 5.72 min | Shiva's Paradise v4 |
| `swg_vs_tox_domi_vs_scuba` | 1 | 2 (1v1) | GLA vs GLA | 36.77 min | Canyon of the Dead v1 |

Notes:
- `is_1v1` is wrong for the 3-player files — the parser uses `num_players == 2` but those have 3 slots with `mode=1`. Likely team games (2v1 or observer in slot 0).
- `mode=5` on `Haubibba_Alphasta` is unusual — could be a non-standard game type (skirmish/coop vs AI).
- All example replays are GLA-heavy; only one file has America players.

> DEVELOPER

great lets change our 2b phase plan to analyze our datased (we will add data leter) to get this metadata and store to the single json file next to the data, we will use this json to mix replays , to avoid ovrfitting... it means we need script which will analyze our replays before we start training, and 2nd script we will need to create batches...as output we might have json with ids per batch.. what do you think about it??

@plans/ @docs/ @plans/IMPLEMENTATION.md @CLAUDE.md

> AGENT

Good picture of the current state. We have:
- 35,998 replay IDs in `data/replay_ids.json`
- `data/replays_index.jsonl` — empty (downloads didn't happen yet)
- `replay/analysis.py` already computes `ReplayStats` (duration, factions, map, desync, quit_early)
- `replay/game_options.py` parses player slots (name, faction, team, human)

The proposal is clean. One question before I go further:

**Where are the actual `.rep` files stored / going to be stored?** Choosing between these affects how the metadata script discovers and references them:

- **A)** Flat directory — `data/replays/<id>.rep` (one folder, 36K files)
- **B)** Sharded — `data/replays/<id[:3]>/<id>.rep` (subdirs to avoid filesystem limits)
- **C)** Something else (e.g., already decided in a scraper script)

> DEVELOPER

we will put them to @replays/dataset/ ..for now use @replays/examples/ as example of replays i will put to the dataset folder

> AGENT

`replays/dataset/` flat. Got it.

Next question: for batch creation, what dimensions matter most for stratification? Pick the ones you want the batcher to balance across batches:

- **A)** Faction matchup (GLA vs GLA, USA vs GLA, etc.)
- **B)** Game duration (short / medium / long buckets)
- **C)** Map
- **D)** Game mode (1v1 vs team)
- **E)** All of the above
- **F)** Something different

> DEVELOPER

E

> AGENT

Good. Now I have enough to propose approaches. Let me move forward.

> AGENT

Three approaches:

---

**A) Two standalone scripts in `scripts/`**
- `scripts/analyze_replays.py` + `scripts/create_batches.py`
- No package structure, just run directly
- Con: not importable by training pipeline — you'd have to re-parse or shell out

---

**B) Modules in `src/zh_copilot/data/` + thin CLI wrappers** ← recommended
- `src/zh_copilot/data/metadata.py` — `ReplayMetadata` dataclass + scanner
- `src/zh_copilot/data/batcher.py` — `StratifiedBatcher` class
- `scripts/analyze_replays.py` and `scripts/create_batches.py` are thin entry points that call the modules
- Pro: training pipeline can `import` the batcher directly later; testable; fits project conventions
- Con: slightly more structure upfront

---

**C) Extend `replay/analysis.py` + add `replay/batcher.py`**
- Keep everything in the `replay/` module
- Pro: metadata extraction is logically "replay analysis"
- Con: mixes replay parsing concerns with data pipeline concerns; `analysis.py` already does stats/filtering, batcher is a different responsibility

---

**Recommendation: B.** The batcher will be needed by the training pipeline (`ILTrainer`) eventually — it needs to be importable, not just a script. And `data/` is already the right module for pipeline-level concerns (downloader, index are there). Fits the pattern.

Agree?

> DEVELOPER

lets have 2 stand alone scripts... its just data preparation.. when we finish it we will connect it to the codebase and model

> AGENT

Reasonable. No over-engineering for data prep. Standalone scripts it is.

> AGENT

**Design — Script 1: `scripts/analyze_replays.py`**

Scans `replays/dataset/` (or a path arg), parses each `.rep` using the existing `parser.py` + `game_options.py`, extracts:

```
replay_id       str    — filename stem (e.g. "369445")
path            str    — relative path to .rep file
duration_s      float  — game length in seconds
duration_bucket str    — "short" <5min / "medium" 5-20min / "long" >20min
game_mode       int    — original_game_mode from header
num_players     int    — human slot count
is_1v1          bool
map_path        str    — normalized map name
factions        list   — e.g. ["GLA", "America"]
matchup         str    — canonical sorted key e.g. "America_vs_GLA"
version         int
valid           bool   — passes is_valid_for_training filter
invalid_reason  str    — why it failed (or null)
```

Output: `data/replay_metadata.json` — a single JSON object: `{"replays": [...], "generated_at": "...", "total": N, "valid": N}`

Skips files that fail to parse (logs a warning, records `valid: false`). Progress bar via `tqdm`. Resumable — if `--force` not passed, skips already-indexed IDs.

Does this look right so far?

> DEVELOPER

also we need to have hash for each replay, to match in case of duplications

> AGENT

Good catch. Adding `md5` hash to each record — lets us deduplicate even if filenames differ.

Updated metadata record adds:

```
md5             str    — MD5 hex digest of the raw .rep file bytes
```

Dedup behavior in the script: after scanning, flag any records where `md5` appears more than once — mark duplicates as `valid: false`, `invalid_reason: "duplicate"`, keep the first occurrence. So the metadata file is the single source of truth for dedup.

Does the full Script 1 design look right now?

> DEVELOPER

y

> AGENT

**Design — Script 2: `scripts/create_batches.py`**

Reads `data/replay_metadata.json`, takes only `valid: true` records, stratifies across all 5 dimensions, outputs batches.

**Stratification logic:**
1. Build a `stratum_key` per replay: `f"{matchup}__{duration_bucket}__{map_bucket}__{game_mode}"`
   - `map_bucket` — top-N most common maps by name, rest binned as `"other"`
2. Sort strata by frequency, assign replays round-robin across batches — guarantees each batch has roughly equal representation of every stratum
3. Any stratum with too few replays to fill a batch gets distributed evenly rather than skipped

**CLI args:**
```
--metadata   path to replay_metadata.json  [default: data/replay_metadata.json]
--output     path to write batches JSON    [default: data/batches.json]
--batch-size N                             [default: 256]
--top-maps   N  top maps to keep as own bucket [default: 20]
--seed       int for reproducibility       [default: 42]
```

**Output format `data/batches.json`:**
```json
{
  "generated_at": "...",
  "batch_size": 256,
  "num_batches": 140,
  "strata_counts": {"GLA_vs_GLA__long__canyon_of_the_dead__1": 412, ...},
  "batches": [
    {"batch_id": 0, "replay_ids": ["369445", "369389", ...]},
    ...
  ]
}
```

Each batch has roughly equal stratum mix. `replay_ids` are the filename stems so the training loop can resolve `replays/dataset/<id>.rep`.

Does this look right?

> DEVELOPER

go for it.. when you finish it review it by yourself, check if no mistakes, run tests for them...then update plans, and set checkmarks you did it, do not forget add @docs/

> AGENT

Good. Writing doc, both scripts, tests, then updating plans — all now.

> AGENT

Now tests:

> AGENT

Bug on line 76 — sorting by `-x[1]` where `x[1]` is a list. Should be `-len(x[1])`.

> AGENT

Test bug — string sort `'10' < '2'`. Fix the comparison:

> AGENT

31/31. Now update IMPLEMENTATION.md:

> AGENT

31/31 tests green. All done:

| File | Status |
|------|--------|
| `scripts/analyze_replays.py` | New — scans `.rep` files, outputs `data/replay_metadata.json` with MD5, dedup, resume |
| `scripts/create_batches.py` | New — stratified round-robin batching → `data/batches.json` |
| `tests/data/test_analyze_replays.py` | 17 tests — helpers + real `.rep` file integration |
| `tests/data/test_create_batches.py` | 14 tests — helpers + batch logic including reproducibility |
| `docs/specs/2026-04-03-replay-metadata-batching-design.md` | Design doc |
| `plans/IMPLEMENTATION.md` | Checkboxes updated |

**Usage when dataset is ready:**
```bash
python scripts/analyze_replays.py                          # → data/replay_metadata.json
python scripts/create_batches.py --batch-size 256          # → data/batches.json
```
