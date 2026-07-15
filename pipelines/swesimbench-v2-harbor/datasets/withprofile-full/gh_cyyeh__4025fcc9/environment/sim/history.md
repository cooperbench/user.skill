[DEVELOPER]: failed to start opensandbox server using `make dev`: ERROR: 2026-03-04 06:15:19+0000 src.services.k8s.kubernetes_service: Failed to initialize Kubernetes client: Failed to load Kubernetes configuration: Invalid kube-config file. No configuration found. Traceback (most recent call last): File "/app/src/services/k8s/client.py", line 58, in _load_config config.load_kube_config(config_file=self.config.kubeconfig_path) File "/app/.venv/lib/python3.10/site-packages/kubernetes/config/kube_config.py", line 836, in load_kube_config loader = _get_kube_config_loader( File "/app/.venv/lib/python3.10/site-packages/kubernetes/config/kube_config.py", line 793, in _get_kube_config_loader raise ConfigException( kubernetes.config.config_exception.ConfigException: Invalid kube-config file. No configuration found. The above exception was the direct cause of the following exception: Traceback (most recent call last): File "/app/src/services/k8s/kubernetes_service.py", line 95, in __init__ self.k8s_client = K8sClient(self.app_config.kubernetes) File "/app/src/services/k8s/client.py", line 44, in __init__ self._load_config() File "/app/src/services/k8s/client.py", line 63, in _load_config raise Exception(f"Failed to load Kubernetes configuration: {e}") from e Exception: Failed to load Kubernetes configuration: Invalid kube-config file. No configuration found.

[AGENT]: The error is coming from the OpenSandbox server trying to initialize a Kubernetes client in local dev. Let me check the Makefile and configuration.

[AGENT]: The config looks correct — `sandbox/config.docker.toml` has `type = "docker"`. The error comes from inside the `opensandbox/server:latest` image trying to initialize a K8s client even when running in Docker mode. Let me check if the container actually crashed or if this is just a non-fatal log message.

[AGENT]: The container exited with code 1 — the K8s error is fatal. Let me check the full logs.

[AGENT]: The key issue: the log says `Creating sandbox service with type: kubernetes` even though `config.docker.toml` has `type = "docker"`. The config file isn't being read. Let me investigate.

[AGENT]: Found it. The OpenSandbox server image expects the config at `/etc/opensandbox/config.toml`, but the Makefile mounts it to `/root/.sandbox.toml`. The config is never read, so it defaults to Kubernetes.

[AGENT]: Now let me also check the deploy manifests for the same issue.

[AGENT]: All three deployment files have the same stale mount path. Let me fix them all.

[AGENT]: Also check if the docs reference the old path.

[AGENT]: Those are just plan docs, not runtime config — I'll leave them as historical reference. **Root cause:** The `opensandbox/server:latest` image changed its config path from `/root/.sandbox.toml` to `/etc/opensandbox/config.toml` (env var `REDACTED.toml`). The volume mounts were using the old path, so the config was never read, and the server defaulted to Kubernetes mode. **Fixed in 4 files:** - `Makefile` (line 21) - `docker-compose.yml` (line 28) - `deploy/kustomize/base/opensandbox-deployment.yaml` (line 25) - `deploy/helm/.../opensandbox-deployment.yaml` (line 31) Try running `make dev` again — the OpenSandbox server should now read the Docker config and start successfully.