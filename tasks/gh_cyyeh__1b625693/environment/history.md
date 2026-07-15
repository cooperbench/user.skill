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

> DEVELOPER

ok, is gvisor still works here?

> AGENT

Yes, gVisor works on both backends: - **Docker**: The current `container_manager.py` already passes `runtime="runsc"` to Docker SDK (line 181). This is preserved as-is in `DockerBackend`. - **K8s**: `kubernetes-sigs/agent-sandbox` natively supports gVisor via `runtimeClassName: gvisor` in the SandboxTemplate spec. From their docs: ```yaml apiVersion: extensions.agents.x-k8s.io/v1alpha1 kind: SandboxTemplate spec: podTemplate: spec: runtimeClassName: gvisor # <-- gVisor isolation containers: - name: sidecar image: duckdb-agent-sidecar:latest ``` The agent-sandbox project was specifically designed around gVisor (and Kata Containers as an alternative). It's one of their core selling points. So the isolation model is consistent across both paths — gVisor sandboxing for the sidecar container regardless of whether you're running locally with Docker or in production on K8s. Shall I continue with the next design section (file structure and API surface)?

> DEVELOPER

continue please

> AGENT

## Design Section 2: File Structure & API Surface **New/modified files**: ``` backend/app/ ├── sandbox/ │ ├── __init__.py # factory: get_sandbox_backend() │ ├── base.py # SandboxBackend ABC + SandboxInfo dataclass │ ├── docker_backend.py # DockerBackend (current container_manager.py logic) │ └── k8s_backend.py # K8sBackend (k8s-agent-sandbox SDK) ├── config.py # add SANDBOX_RUNTIME, K8S_* config vars ├── main.py # import from sandbox/ instead of container_manager ├── agent.py # import from sandbox/ instead of container_manager ├── container_manager.py # DELETE (moved into sandbox/docker_backend.py) ``` **ABC definition** (`base.py`): ```python class SandboxInfo: sandbox_id: str session_id: str url: str # "http://host:port" — ready to use created_at: datetime last_activity: datetime class SandboxBackend(ABC): async def create(self, session_id: str, env: dict[str, str]) -> SandboxInfo def get(self, session_id: str) -> SandboxInfo | None def touch(self, session_id: str) -> None async def stop(self, session_id: str) -> None async def cleanup_expired(self) -> int async def shutdown_all(self) -> None async def cleanup_orphaned(self) -> int ``` **Factory** (`__init__.py`): ```python def get_sandbox_backend() -> SandboxBackend | None: if SANDBOX_RUNTIME == "docker": return DockerBackend(...) elif SANDBOX_RUNTIME == "k8s": return K8sBackend(...) ``` **Config additions** (`config.py`): ```python SANDBOX_RUNTIME = os.getenv("SANDBOX_RUNTIME", "docker") # "docker" | "k8s" # K8s-specific (only used when SANDBOX_RUNTIME="k8s") K8S_TEMPLATE_NAME = os.getenv("K8S_TEMPLATE_NAME", "duckdb-agent-sidecar") K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "default") K8S_GATEWAY_NAME = […]

> DEVELOPER

ok

> AGENT

## Design Section 3: DockerBackend Details This is essentially the current `container_manager.py` wrapped to implement the ABC. Minimal changes: **What stays the same**: - `ContainerConfig` dataclass (image, runtime, memory_limit, cpu_limit, network) - All Docker SDK logic: gVisor DNS workarounds, host gateway resolution, volume mounts, extra_hosts, labels - Synchronous Docker API calls (wrapped in `run_in_executor` by the caller, as already done in `agent.py`) - Label-based orphan cleanup (`_cleanup_by_label`) **What changes**: - Class renamed `DockerBackend`, implements `SandboxBackend` - `create()` returns `SandboxInfo` (maps `container_id` → `sandbox_id`, computes `url` internally) - `stop()` / `cleanup_expired()` / `shutdown_all()` become `async` (thin wrappers that run sync Docker calls in executor) - `cleanup_orphaned()` delegates to existing `_cleanup_by_label()` **Dependency**: `docker` (already in pyproject.toml, stays as-is) The Docker path should behave identically to today. Does this look right?

> DEVELOPER

ok

> AGENT

## Design Section 4: K8sBackend Details Uses the `k8s-agent-sandbox` Python SDK (`SandboxClient`). **How it works**: ```python class K8sBackend(SandboxBackend): def __init__(self, config: K8sConfig): # config holds template_name, namespace, gateway_name, # server_port, idle_timeout, max_lifetime ... async def create(self, session_id: str, env: dict[str, str]) -> SandboxInfo: # SandboxClient is a context manager — but we need long-lived sandboxes, # so we call __aenter__ on create and __aexit__ on stop. client = SandboxClient( template_name=self._config.template_name, namespace=self._config.namespace, gateway_name=self._config.gateway_name or None, # None = tunnel/dev mode server_port=self._config.server_port, # 3000 (sidecar port) ) sandbox = await client.__aenter__() # The SDK handles pod creation, readiness wait, and endpoint resolution # sandbox.run() is available but we don't use it — we POST to /query directly endpoint_url = f"http://{client.endpoint}" return SandboxInfo(sandbox_id=..., session_id=session_id, url=endpoint_url, ...) ``` **Lifecycle mapping**: | Operation | K8s SDK | Notes | |-----------|---------|-------| | Create | `SandboxClient.__aenter__()` | Creates Sandbox CR, waits for pod ready | | Stop | `SandboxClient.__aexit__()` | Deletes Sandbox CR, pod cleaned up by controller | | Cleanup orphaned | List Sandbox CRs with label selector | Find CRs not tracked in memory | | Warm pool | `SandboxWarmPool` CR (deployed separately) | Sub-second allocation | **Sidecar communication**: Same as Docker — backend POSTs […]