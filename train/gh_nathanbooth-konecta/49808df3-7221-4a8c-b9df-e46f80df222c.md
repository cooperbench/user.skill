> AGENT

Prompt is too long

> DEVELOPER

, [2026-02-13T10:10:50.382437 #21]  INFO -- : [ActiveJob] [Provisioner::UpdateProvisionedCrewJob] [4a6307bf-aa61-4587-b659-d2dbad1c0b89] Ansible command stdout:

2026-02-13 10:10:50.383

crewai-platform-worker
2026-02-13 10:10:50.383

crewai-platform-worker
PLAY [Build and Push Docker Image with Cluster BuildKit] ***********************
2026-02-13 10:10:50.383

crewai-platform-worker
2026-02-13 10:10:50.383

crewai-platform-worker
TASK [Deploy BuildKit Pod to Build Image] **************************************
2026-02-13 10:10:50.383

crewai-platform-worker
[ERROR]: Task failed: Module failed: 401
2026-02-13 10:10:50.383

crewai-platform-worker
Reason: Unauthorized
2026-02-13 10:10:50.384

crewai-platform-worker
HTTP response headers: HTTPHeaderDict({'Audit-Id': '6c488bb3-8a2c-40f8-9ee4-f62cadb38e4a', 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'Date': 'Fri, 13 Feb 2026 10:10:42 GMT', 'Content-Length': '129'})
2026-02-13 10:10:50.384

crewai-platform-worker
HTTP response body: b'{"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}\n'
2026-02-13 10:10:50.384

crewai-platform-worker
Original traceback: 
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 55, in inner
2026-02-13 10:10:50.384

crewai-platform-worker
    resp = func(self, *args, **kwargs)
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 277, in request
2026-02-13 10:10:50.384

crewai-platform-worker
    api_response = self.client.call_api(
2026-02-13 10:10:50.384

crewai-platform-worker
                   ^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 348, in call_api
2026-02-13 10:10:50.384

crewai-platform-worker
    return self.__call_api(resource_path, method,
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 180, in __call_api
2026-02-13 10:10:50.384

crewai-platform-worker
    response_data = self.request(
2026-02-13 10:10:50.384

crewai-platform-worker
                    ^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 373, in request
2026-02-13 10:10:50.384

crewai-platform-worker
    return self.rest_client.GET(url,
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py", line 244, in GET
2026-02-13 10:10:50.384

crewai-platform-worker
    return self.request("GET", url,
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py", line 238, in request
2026-02-13 10:10:50.384

crewai-platform-worker
    raise ApiException(http_resp=r)
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
Task failed: Module failed.
2026-02-13 10:10:50.384

crewai-platform-worker
Origin: /app/app/services/provisioner/k8s/v1/ansible/buildkit_build.yml:16:11
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
14     - name: Execute BuildKit build process using cluster daemon
2026-02-13 10:10:50.384

crewai-platform-worker
15       block:
2026-02-13 10:10:50.384

crewai-platform-worker
16         - name: Deploy BuildKit Pod to Build Image
2026-02-13 10:10:50.384

crewai-platform-worker
             ^ column 11
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
<<< caused by >>>
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
401
2026-02-13 10:10:50.384

crewai-platform-worker
Reason: Unauthorized
2026-02-13 10:10:50.384

crewai-platform-worker
HTTP response headers: HTTPHeaderDict({'Audit-Id': '6c488bb3-8a2c-40f8-9ee4-f62cadb38e4a', 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'Date': 'Fri, 13 Feb 2026 10:10:42 GMT', 'Content-Length': '129'})
2026-02-13 10:10:50.384

crewai-platform-worker
HTTP response body: b'{"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}\n'
2026-02-13 10:10:50.384

crewai-platform-worker
Original traceback: 
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 55, in inner
2026-02-13 10:10:50.384

crewai-platform-worker
    resp = func(self, *args, **kwargs)
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 277, in request
2026-02-13 10:10:50.384

crewai-platform-worker
    api_response = self.client.call_api(
2026-02-13 10:10:50.384

crewai-platform-worker
                   ^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 348, in call_api
2026-02-13 10:10:50.384

crewai-platform-worker
    return self.__call_api(resource_path, method,
2026-02-13 10:10:50.384

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.384

crewai-platform-worker
2026-02-13 10:10:50.384

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 180, in __call_api
2026-02-13 10:10:50.384

crewai-platform-worker
    response_data = self.request(
2026-02-13 10:10:50.384

crewai-platform-worker
                    ^^^^^^^^^^^^^
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py", line 373, in request
2026-02-13 10:10:50.385

crewai-platform-worker
    return self.rest_client.GET(url,
2026-02-13 10:10:50.385

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py", line 244, in GET
2026-02-13 10:10:50.385

crewai-platform-worker
    return self.request("GET", url,
2026-02-13 10:10:50.385

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py", line 238, in request
2026-02-13 10:10:50.385

crewai-platform-worker
    raise ApiException(http_resp=r)
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
fatal: [localhost]: FAILED! => {"changed": false, "msg": "Task failed: Module failed: 401\nReason: Unauthorized\nHTTP response headers: HTTPHeaderDict({'Audit-Id': '6c488bb3-8a2c-40f8-9ee4-f62cadb38e4a', 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'Date': 'Fri, 13 Feb 2026 10:10:42 GMT', 'Content-Length': '129'})\nHTTP response body: b'{\"kind\":\"Status\",\"apiVersion\":\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"Unauthorized\",\"reason\":\"Unauthorized\",\"code\":401}\\n'\nOriginal traceback: \n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py\", line 55, in inner\n    resp = func(self, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py\", line 277, in request\n    api_response = self.client.call_api(\n                   ^^^^^^^^^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py\", line 348, in call_api\n    return self.__call_api(resource_path, method,\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py\", line 180, in __call_api\n    response_data = self.request(\n                    ^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/client/api_client.py\", line 373, in request\n    return self.rest_client.GET(url,\n           ^^^^^^^^^^^^^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py\", line 244, in GET\n    return self.request(\"GET\", url,\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n\n  File \"/usr/local/lib/python3.12/dist-packages/kubernetes/client/rest.py\", line 238, in request\n    raise ApiException(http_resp=r)"}
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
TASK [Get failed pod logs from build pod] **************************************
2026-02-13 10:10:50.385

crewai-platform-worker
[ERROR]: Task failed: Module failed: 401
2026-02-13 10:10:50.385

crewai-platform-worker
Reason: Unauthorized
2026-02-13 10:10:50.385

crewai-platform-worker
HTTP response headers: HTTPHeaderDict({'Audit-Id': '3128bdb6-77c2-4c8b-a7da-397af86abfa5', 'Cache-Control': 'no-cache, private', 'Content-Type': 'application/json', 'Date': 'Fri, 13 Feb 2026 10:10:44 GMT', 'Content-Length': '129'})
2026-02-13 10:10:50.385

crewai-platform-worker
HTTP response body: b'{"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}\n'
2026-02-13 10:10:50.385

crewai-platform-worker
Original traceback: 
2026-02-13 10:10:50.385

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 55, in inner
2026-02-13 10:10:50.385

crewai-platform-worker
    resp = func(self, *args, **kwargs)
2026-02-13 10:10:50.385

crewai-platform-worker
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-02-13 10:10:50.385

crewai-platform-worker
2026-02-13 10:10:50.385

crewai-platform-worker
  File "/usr/local/lib/python3.12/dist-packages/kubernetes/dynamic/client.py", line 277, in request

> AGENT

Prompt is too long

> DEVELOPER

The failure is straightforward: 401 Unauthorized when the crewai-platform-worker tries to interact with the Kubernetes API.
Specifically, the Ansible playbook buildkit_build.yml (line 16) is attempting to deploy a BuildKit pod, and the Kubernetes Python client is getting rejected at the API server level. The same 401 hits the follow-up task that tries to retrieve pod logs.
Root cause candidates, in order of likelihood:

Expired or invalid ServiceAccount token. If the worker pod is using a mounted SA token (especially a time-bound projected token), it may have expired. Check if the pod has been running for a long time or if the token volume is properly configured.
Kubeconfig / credentials not loaded. The Ansible task might be expecting in-cluster config but the environment variables (KUBERNETES_SERVICE_HOST, etc.) aren't set, or it's loading a kubeconfig with stale credentials.
ServiceAccount deleted or RBAC misconfigured. The SA the worker runs as may have been removed, or a ClusterRoleBinding/RoleBinding was changed so it no longer has permission to create pods in the target namespace.
GKE token refresh issue. Since you're on GCP, if this uses Workload Identity Federation or a GKE auth plugin, the token exchange may be failing silently, and the K8s client falls back to no auth.

Quickest debugging steps:

kubectl auth whoami from inside the worker pod (or equivalent kubectl auth can-i create pods --namespace=<target> using the SA)
Check if the SA and its token secret still exist: kubectl get sa -n <namespace> and inspect the mounted token
Look at the API server audit log for that Audit-Id: 6c488bb3-8a2c-40f8-9ee4-f62cadb38e4a to see exactly what identity (or lack thereof) was presented

The 401 (not 403) specifically means "no valid identity presented at all," not "identity lacks permission." So the credentials aren't reaching the API server, rather than being insufficient.

> AGENT

Prompt is too long
