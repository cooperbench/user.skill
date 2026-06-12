# Projects: yarikoptic

## bids-standard/bids-utils ★ dominant (100% of sessions)

**What they do here**: Architect and primary developer of a new Python CLI library for manipulating
BIDS (Brain Imaging Data Structure) datasets. All 13 sessions are on this repo.

**Tech stack**:
- Language: Python 3.10–3.14
- CLI: Click with `bids-utils` entry point
- Packaging: pyproject.toml + hatchling + uv
- Testing: tox (py310, py311, py312, py313, py314, lint, type, duplication envs), pytest
- Code quality: ruff (lint + format), mypy (type checking), pylint (duplication detection)
- Docs: MkDocs
- Schema: bidsschematools (never hardcode BIDS knowledge — always derive from schema)
- Data provenance: DataLad / git-annex integration
- Integration tests: bids-examples as a git submodule

**Recurring themes**:
- BIDS file renaming with sidecar propagation (`_scans.tsv`, JSON sidecars)
- Subject and session renaming across dataset hierarchies
- BIDS 1.x → 1.x migration with deprecation handling (derived from `bidsschematools` schema)
- Shell completion for the CLI via Click 8's built-in mechanism
- Dataset root auto-detection by walking up to `dataset_description.json`
- Dry-run / preview mode before any mutating operation

**Speckit workflow phases** (custom skill framework driving sessions):
1. `/speckit.specify` — write the design spec
2. `/speckit.clarify` — refine user stories / resolve open questions
3. `/speckit.plan` — produce implementation plan with research on related projects
4. `/speckit.implement [T###...]` — implement specific task IDs
5. `/speckit.tasks` — review task status

**Related local repos** (referenced in prompts):
- `/home/yoh/proj/bids/bids-specification-master` — local clone of the BIDS spec (used for
  `git grep` on deprecated fields)
- bids-examples — git submodule in bids-utils for integration tests
