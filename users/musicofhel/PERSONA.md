# Persona: musicofhel

## Role and background

musicofhel is a developer building developer tooling — specifically a "dev-loop" automation system that integrates AI-powered code review into a CI/CD or pre-merge quality gate. (inferred) They are comfortable enough with LLM APIs and prompt engineering to design a full structured-output pipeline: role injection, criteria parameterization, JSON schema enforcement, severity mapping to pass/fail decisions.

**Role** (inferred): Platform/DevEx engineer, or a developer who treats their own workflow as a product. The project name `dev-loop` signals they are optimizing their own development feedback loop.

**Seniority signals** (inferred): The review criteria they chose (race conditions, memory leaks, logic errors, missing boundary error handling, performance antipatterns) reflect senior engineering concerns, not beginner checklist items. The decision to map severity levels to binary gate outcomes (critical=fail, others=pass) shows understanding of CI gate design. They are writing Python with type hints and proper docstrings in the reviewed code.

## Attitude toward the agent

**Fully trusting / zero supervision.** There is no human reviewing the agent's output before it is consumed. The pipeline fires a prompt, receives JSON, and acts on it. The agent is treated as a deterministic JSON function, not a collaborator. There is no dialogue, no clarification, no correction. `pushback_distribution: {non_pushback: 1.0}` across all 7 training prompts.

## Tone

There is no tone — the prompts are machine-generated. They are formal, imperative, and structured. The vocabulary is technical but not academic. There are no pleasantries, no hedging, no emotional register. The closest human analogue would be a meticulous engineer who has replaced their internal monologue with a YAML spec.

## Domain expertise visible in prompts

- Git diffs (reads and embeds them fluently)
- Python (calculator.py factorial with ValueError/TypeError, scoring.py type hints, test files)
- SQL injection awareness (one reviewed diff adds a raw SQL search endpoint — the pipeline is designed to catch this)
- Structured JSON output from LLMs (explicit schema definition with nullables, exact key names)
- CI/CD gate design (pass/fail severity mapping)
