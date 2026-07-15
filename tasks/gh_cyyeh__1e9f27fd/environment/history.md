> DEVELOPER

create new worktree from copying worktree opensandbox-integration, implement new functionality, please write design spec first: remove opensandbox and restore to current container_manager.py to support original docker workflow add direct agent-sandbox support for k8s workload

> AGENT

I'll start by exploring the project context, especially the opensandbox-integration worktree and the current codebase.

> AGENT

Let me explore the project context — the opensandbox-integration worktree, current container_manager.py, and existing design docs.

> AGENT

Good, I now have a thorough understanding of the codebase. Let me start with my first clarifying question. **Context recap**: The opensandbox-integration worktree replaced `ContainerManager` (Docker SDK) with `SandboxManager` (OpenSandbox SDK) and added K8s deployment manifests. You now want to: 1. Remove the OpenSandbox dependency and restore the original Docker workflow 2. Add direct K8s workload support (without OpenSandbox as the intermediary) **Question 1**: For the K8s support, when you say "direct agent-sandbox support for k8s workload" — do you mean the backend should use the Kubernetes Python client (e.g., `kubernetes` library) to directly create/manage Pods or Jobs for the sidecar containers, similar to how `container_manager.py` uses the Docker SDK directly? Or do you have a different K8s integration pattern in mind (e.g., Custom Resource + operator, Knative, etc.)?

> DEVELOPER

check agent-sandbox python library and propose solutions for me

> AGENT

Let me research the agent-sandbox Python library.

> AGENT

Now I have a thorough understanding of the `kubernetes-sigs/agent-sandbox` project. Let me also quickly check what the opensandbox worktree's sandbox_manager looks like for the K8s integration patterns.

> AGENT

Good. I've now researched the `kubernetes-sigs/agent-sandbox` project thoroughly. Here's what I found and my proposed approaches: --- ## Research Summary: `kubernetes-sigs/agent-sandbox` **What it is**: A Kubernetes SIG project (v0.1.1, Feb 2026) providing a Sandbox CRD + controller for managing isolated, stateful, singleton pods. Built for AI agent runtimes. **Key components**: - **Sandbox CRD** — declares a single stateful pod with stable identity - **SandboxTemplate** — reusable pod blueprints (custom image, resources, runtimeClass) - **SandboxWarmPool** — pre-warmed pods for sub-second allocation - **Sandbox Router** — central entry point for routing traffic to sandbox pods - **Python SDK** (`pip install k8s-agent-sandbox`) — context-manager based client with `SandboxClient.run()` method **Networking modes**: Gateway (production, via load balancer) and Tunnel (dev, via `kubectl port-forward`) **Key fit**: The SandboxTemplate lets us declare our sidecar image with resources/ports, and the Python SDK handles lifecycle (create, run commands, cleanup). gVisor and Kata isolation are supported natively. --- ## Proposed Approaches ### Approach A: Strategy Pattern — Docker + K8s backends behind a common interface - Keep the current `ContainerManager` (Docker SDK) as-is - Add a new `K8sSandboxManager` using `k8s-agent-sandbox` Python SDK - Create a thin `SandboxBackend` protocol/ABC that both implement - Runtime selection via `SANDBOX_RUNTIME=docker|kubernetes` env var - […]

> DEVELOPER

approach a

> AGENT

Let me read the integration points to ensure the design covers all touchpoints.

> AGENT

Now let me also check how `container_manager` is used in `agent.py`.

> AGENT

Now I have a complete picture. Let me present the design section by section. --- ## Design Section 1: Architecture Overview **Goal**: Replace the opensandbox-integration approach with a Strategy Pattern that keeps the original Docker workflow intact and adds `kubernetes-sigs/agent-sandbox` as a second runtime backend. ``` ┌─────────────────────┐ │ SANDBOX_RUNTIME env │ │ "docker" | "k8s" │ └────────┬────────────┘ │ ┌─────────────┴─────────────┐ │ SandboxBackend (ABC) │ │ create() / get() / touch()│ │ stop() / cleanup_expired()│ │ shutdown_all() / startup()│ └─────────────┬─────────────┘ ┌─────────────┴─────────────┐ ┌─────────┴──────────┐ ┌─────────────┴──────────┐ │ DockerBackend │ │ K8sBackend │ │ (current code, │ │ (k8s-agent-sandbox │ │ docker SDK) │ │ Python SDK) │ └────────────────────┘ └────────────────────────┘ ``` **Key decisions**: - `DockerBackend` = the existing `ContainerManager` code, minimally refactored to implement the ABC - `K8sBackend` = new class using `k8s-agent-sandbox` SDK (`SandboxClient`) - A factory function reads `SANDBOX_RUNTIME` and returns the right backend - `main.py` and `agent.py` only interact via the ABC — no runtime-specific imports - The ABC methods are **async** (Docker methods wrapped with `run_in_executor` as already done in `agent.py`) Does this section look right?