# SWESimBench website

Next.js static-export frontend for **SWESimBench** (https://swesimbench.vercel.app).

This directory was moved from [`AlienKevin/user-simulator`](https://github.com/AlienKevin/user-simulator)
into [`cooperbench/user.skill`](https://github.com/cooperbench/user.skill) so the public site and
benchmark code live in one repo.

## Develop

```bash
cd web
npm install
npm run dev      # local
npm run build    # static export → web/out
```

## Data on the site

| Artifact | What it is |
|---|---|
| `public/data/condagree.json` | Snapshot of the published CondAgree leaderboard (20 SWE-chat developers, 480 moments) |
| `public/data/v2_cohort.json` | **Public-safe** aggregate metadata for the authoritative v2 harbor cohort (57 developers, 1216 points). No session text. |
| `app/data/blobs.json` | Catalog of CondAgree trial files on Vercel Blob |

Regenerate the public v2 cohort file after hydrate:

```bash
python3 scripts/export_v2_cohort_public.py
```

Upload CondAgree Blob artifacts (needs `BLOB_READ_WRITE_TOKEN`):

```bash
cd web && BLOB_READ_WRITE_TOKEN=… node scripts/upload-blob.mjs
```

## Layout

- `app/` — pages (`/`, `/data`)
- `public/data/` — JSON shipped with the static export
- `scripts/upload-blob.mjs` — publish CondAgree trial files to Vercel Blob
