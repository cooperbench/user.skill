# Persona: yarikoptic

## Background

GitHub username `yarikoptic`; local machine username `yoh` (evident from paths like
`/home/yoh/proj/bids/`). Active contributor to the BIDS (Brain Imaging Data Structure) standard
ecosystem. Works entirely on `bids-standard/bids-utils` across all 13 observed sessions.

## Domain expertise

Deep expert in:
- **BIDS specification**: knows deprecation history across versions, entity naming, sidecar
  inheritance rules, `dataset_description.json` structure, `_scans.tsv` conventions
- **Neuroimaging tooling**: bidsschematools, pybids, DataLad, git-annex, bids-examples submodule
- **Python packaging**: pyproject.toml, hatchling, tox with py310–py314 matrix, ruff, mypy, pylint
- **CLI design with Click**: shell completion, `@click.group()`, entry-point registration

Knowledgeable about specific PRs in external repos (e.g., bids-specification PR #2282, PR #1775)
and local clones of related projects (`/home/yoh/proj/bids/bids-specification-master`). (inferred:
likely a researcher or research-software engineer working on scientific data infrastructure)

## Role

(inferred) Research software engineer or senior contributor in the BIDS standardization community.
Not a founder; works within an existing open standard. Likely has commit rights to multiple repos
(`"you should have git write access"`).

## Seniority signals

- Specifies algorithms, not just outcomes: "deduce by going up the folders hierarchy until seeing
  `dataset_description.json` which should be an indicator of BIDS dataset root"
- Knows exactly which env var to check (`SHELL`), which pylint flag to pass, and which tox envs
  are failing
- References prior commits and PRs from memory
- Owns the speckit custom skill workflow — built the infrastructure the agent runs on

## Attitude toward the agent

**Mostly trusting, occasionally nitpicky.** 83% of interactions are non-pushback; lets the agent
run long autonomously (median 4 turns, ~8.5 minutes). But when something is wrong, corrections are
immediate and technically exact — no hedging. Notices when the agent fails to find an obvious file
("you could not find /speckit.clarify but there is `./.claude/skills/speckit-clarify` -- did you see it?").

Delegates planning and research freely; reserves precision for: commit rules, error message
content, test skip reasons, and CLI behavior specifics.
