# PERSONA — mheers

## Background (inferred)

- **Role:** Infrastructure-leaning developer or DevOps engineer (inferred from heavy Docker, shell scripting, and USB device passthrough work).
- **Seniority:** Mid-to-senior (inferred). He already knows the correct fix in most cases—corrections show he has the right answer and is checking whether the agent does too. He references specific Linux kernel capabilities (`CAP_MKNOD`), USB bus paths (`/dev/bus/usb/BUS/DEV`), and libnotify internals without explanation.
- **Domain expertise:** Docker container runtime, shell scripting (`oc` / `os` bash wrappers), Linux device management, Dockerfile layering, AI coding tool configuration (OpenCode plugins).
- **Platform:** Linux desktop (audio via libnotify/sound, USB device passthrough, `lsusb` usage).

## Attitude Toward the Agent

- **Skeptical and hands-on.** Nearly every agent turn gets pushed back on—53.8% as corrections, 38.5% as failure reports.
- **Transactional, not collaborative.** He states a problem and expects a working solution. He does not ask for explanations; he wants the agent to execute and verify.
- **Delegates execution aggressively.** He frequently tells the agent to run the container or build loop itself ("run the container yourself", "run 'make' yourself until it works"). He is comfortable treating the agent as an autonomous operator.
- **Not micromanaging on code style**, but precise about runtime behavior—he will correct wrong device paths, wrong package names, wrong capability flags.
- **No warmth signals.** No "thanks", no encouragement, no smalltalk. A terse "hm" is the closest he gets to expressing uncertainty.

## Tone

Factual, neutral, imperative. Sentence case with occasional lowercase informality. No emoji. Calm even when things are broken; frustration surfaces as a flat restatement of what already failed.
