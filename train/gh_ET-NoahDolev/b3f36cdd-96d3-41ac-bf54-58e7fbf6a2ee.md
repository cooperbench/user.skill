> DEVELOPER

I am not seeing the trace logging in Mlflow can you do a root cause analysis and diagnose the problem. Query MLFlow and see what was recorded in the last run - only api calls.

> AGENT

I'll investigate the MLflow tracing issue by first understanding the codebase and then querying MLflow directly.

> TOOL

tool_use Task
id: toolu_01SQ8krf1pyipbdJkdihQFaw
```json
{
  "description": "Explore MLflow tracing setup",
  "prompt": "Explore the codebase to understand how MLflow tracing is configured and used. I need to find:\n1. All files related to MLflow tracing configuration\n2. How traces are being created/logged\n3. The MLflow tracking URI and experiment setup\n4. Any tracing decorators or context managers being used\n5. The tracing.py file and trigger.py file contents\n\nFocus on:\n- services/protocol-processor-service/src/protocol_processor/tracing.py\n- services/protocol-processor-service/src/protocol_processor/trigger.py\n- Any MLflow configuration files\n- Docker compose or env files that set MLflow URI\n\nBe thorough - check for mlflow imports, @mlflow.trace decorators, mlflow.start_span, etc.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Bash
id: toolu_016TNkoYx2pcFtpTSVfDt6iD
```json
{
  "command": "curl -s http://localhost:5001/api/2.0/mlflow/experiments/search 2>/dev/null | python3 -m json.tool 2>/dev/null || echo \"MLflow not reachable on 5001, trying other ports...\" && curl -s http://localhost:5000/api/2.0/mlflow/experiments/search 2>/dev/null | python3 -m json.tool 2>/dev/null || echo \"Also not on 5000\"",
  "description": "Check MLflow API availability"
}
```

> TOOL

tool_result
id: toolu_01SQ8krf1pyipbdJkdihQFaw
```
Perfect! Now I have all the information needed. Let me compile a comprehensive report of my findings.

## MLflow Tracing Configuration and Usage - Comprehensive Report

I've thoroughly explored your codebase to understand the MLflow tracing configuration. Here are my findings:

### 1. Key Files Related to MLflow Tracing Configuration

**Core Tracing Files:**
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tracing.py` - Core tracing context manager and utilities
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/trigger.py` - Pipeline trigger with MLflow setup
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/api-service/src/api_service/middleware.py` - MLflow request tracing middleware
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/api-service/src/api_service/main.py` - FastAPI app with MLflow initialization

**Testing/Utility Files:**
- `/Users/noahdolevelixir/Code/medgemma-hackathon/scripts/verify_mlflow_tracing.py` - Verification script for trace behavior
- `/Users/noahdolevelixir/Code/medgemma-hackathon/scripts/clear_mlflow_traces.py` - Utility to clear traces from MLflow server

---

### 2. How Traces Are Created/Logged

#### **Pipeline Node Tracing Pattern**
Each pipeline node uses the `pipeline_span()` context manager from `tracing.py`:

```python
from protocol_processor.tracing import pipeline_span

with pipeline_span("node_name", span_type="CHAIN", protocol_id=protocol_id) as span:
    span.set_inputs({"input_key": value})
    # ... node logic ...
    span.set_outputs({"output_key": result})
```

**Nodes using this pattern:**
- `ingest_node` (span_type="CHAIN") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/ingest.py`
- `extract_node` (span_type="LLM") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/extract.py`
- `parse_node` (span_type="CHAIN") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/parse.py`
- `ground_node` (span_type="TOOL") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/ground.py`
- `persist_node` (span_type="CHAIN") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/persist.py`
- `structure_node` (span_type="CHAIN") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/structure.py`
- `ordinal_resolve_node` (span_type="CHAIN") - `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/ordinal_resolve.py`

#### **API Request Tracing**
FastAPI requests are traced via `MLflowRequestMiddleware` in the main.py app, which creates HTTP spans for API calls:

```python
with mlflow.start_span(name=f"{method} {path}", span_type="HTTP") as span:
    span.set_inputs({"method": method, "path": path, "query": query})
    # ... handle request ...
    span.set_outputs({"status_code": status_code, "latency_ms": latency})
```

---

### 3. MLflow Tracking URI and Experiment Setup

#### **Environment Variables**
- **MLFLOW_TRACKING_URI** - Set in environment, defaults to `http://localhost:5001` locally
- **MLFLOW_TRACE_TIMEOUT_SECONDS** - Set to 300 seconds in docker-compose (5 minute timeout)

#### **Experiment Naming Strategy**
One experiment per day to group all runs and workers:
- Pattern: `protocol-processing-{YYYYMMDD}` (e.g., `protocol-processing-20250224`)
- Function: `_get_experiment_name()` in `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/trigger.py` (lines 95-104)

#### **Setup Flow**
1. **API Startup** (main.py, lines 58-85):
   - Sets tracking URI via `mlflow.set_tracking_uri(tracking_uri)`
   - Creates/sets experiment via `mlflow.set_experiment(experiment_name)`
   - Explicitly does NOT enable `mlflow.langchain.autolog()`

2. **Pipeline Invocation** (trigger.py, lines 107-125):
   - `_ensure_mlflow()` configures MLflow for the current thread
   - Sets experiment ID in ContextVar for pipeline traces

3. **Context Vars for Tracing** (tracing.py, lines 33-43):
   - `_pipeline_run_id` - Set once per pipeline invocation to tag all node traces with a shared identifier
   - `_pipeline_experiment_id` - Stores experiment ID so export works from any thread

---

### 4. Tracing Decorators and Context Managers

#### **Core Context Manager: `pipeline_span()`**
**Location:** `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tracing.py` (lines 56-116)

**Signature:**
```python
@contextmanager
def pipeline_span(
    name: str,
    span_type: str = "CHAIN",
    protocol_id: str = "",
):
    """Create a separate MLflow trace for a pipeline node."""
```

**Key Features:**
- Creates independent top-level traces (not child spans)
- Falls back to `_NoOpSpan()` if MLflow is unavailable
- Automatically tags traces with:
  - `node` - span/node name for filtering
  - `protocol_id` - protocol identifier for session grouping
  - `run_id` - thread_id for grouping all traces from same pipeline invocation

**Important Implementation Detail:**
- Does NOT enable `mlflow.langchain.autolog()` because it wraps entire `graph.ainvoke()` in a single parent trace that only appears after the full pipeline finishes
- Instead, each node creates independent root traces that flush to MLflow immediately as context manager exits, enabling real-time trace appearance

#### **No-Op Fallback**
`_NoOpSpan` class (lines 119-129) provides silent fallback when MLflow unavailable:
```python
class _NoOpSpan:
    def set_inputs(self, inputs: dict[str, Any]) -> None: pass
    def set_outputs(self, outputs: dict[str, Any]) -> None: pass
    def set_status(self, status: str) -> None: pass
```

---

### 5. Tracing.py and Trigger.py Complete Contents

#### **tracing.py** (Complete)
See absolute path: `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tracing.py`

**Key Functions:**
- `set_pipeline_run_id(run_id)` - Sets run ID in ContextVar before graph.ainvoke
- `set_pipeline_experiment_id(experiment_id)` - Sets experiment ID for traces
- `pipeline_span()` - Main context manager for creating node traces
- `_NoOpSpan` - Fallback no-op implementation

**Critical Notes from Comments (lines 1-21):**
> "IMPORTANT: `mlflow.langchain.autolog()` must NOT be enabled. Autolog wraps `graph.ainvoke()` in a single parent trace and all node spans become children — producing one constantly-updating trace that only appears after the full pipeline finishes. Without autolog, each call to `mlflow.start_span()` inside a node creates an independent root trace that is flushed to MLflow as soon as the context manager exits."

#### **trigger.py** (Key Sections)

**Orphan Trace Cleanup** (lines 35-89):
- Runs once at module import (service startup)
- Closes stale IN_PROGRESS traces older than 1 hour
- Uses `client.search_traces()` and `client.end_trace()` from MLflow 3.x API

**Experiment Naming** (lines 92-104):
```python
def _get_experiment_name() -> str:
    """Return MLflow experiment name: one per day so all runs share it."""
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"protocol-processing-{date_str}"
```

**MLflow Setup** (lines 107-125):
```python
def _ensure_mlflow() -> bool:
    """Ensure MLflow tracking is configured in the current thread."""
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(_get_experiment_name())
        return True
    return False
```

**Pipeline Execution** (lines 227-264):
- `_run_pipeline()` async function executes graph with MLflow context set
- Sets `_pipeline_run_id` from thread_id before invocation
- Thread ID format: `"{protocol_id}:{uuid4()}"`

**Handler** (lines 326-438):
- `handle_protocol_uploaded()` - Main entry point for protocol processing
- Calls `_preflight_check()` to verify DB/OMOP/MLflow reachability
- Calls `_ensure_mlflow()` to configure MLflow for worker thread
- Generates unique thread_id and stores in protocol.metadata_
- Invokes pipeline via `asyncio.run(_run_pipeline())`

---

### 6. Docker Compose Configuration

**Location:** `/Users/noahdolevelixir/Code/medgemma-hackathon/infra/docker-compose.yml`

**MLflow Service** (lines 81-97):
```yaml
mlflow:
  image: ghcr.io/mlflow/mlflow:v3.9.0
  ports:
    - "${MLFLOW_PORT:-5001}:5000"
  command: >
    mlflow server
    --host 0.0.0.0
    --port 5000
    --backend-store-uri sqlite:///mlflow/mlflow.db
    --artifacts-destination /mlflow/artifacts
  volumes:
    - mlflow_data:/mlflow
  healthcheck:
    test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()"]
```

**API Service Environment** (lines 14-16):
```yaml
- MLFLOW_TRACKING_URI=http://mlflow:5000
- MLFLOW_TRACE_TIMEOUT_SECONDS=300
```

Note: Internal docker-compose uses `http://mlflow:5000`, local dev uses `http://localhost:5001`

---

### 7. Environment Configuration

**Location:** `/Users/noahdolevelixir/Code/medgemma-hackathon/.env.example` (lines 71-75)

```
# Observability: MLflow
# When running locally via "make run-dev", MLflow runs on localhost:5001
MLFLOW_TRACKING_URI=http://localhost:5001
```

---

### 8. Summary of Trace Flow

1. **Service Startup**
   - API service initializes MLflow with tracking URI
   - Sets experiment name (protocol-processing-YYYYMMDD)
   - Adds MLflowRequestMiddleware to FastAPI app

2. **Protocol Upload Event**
   - Outbox processor calls `handle_protocol_uploaded()`
   - Handler calls `_ensure_mlflow()` for worker thread
   - Sets experiment ID in ContextVar
   - Generates unique thread_id: `protocol_id:uuid4`

3. **Pipeline Execution**
   - Sets `_pipeline_run_id` ContextVar
   - Invokes LangGraph with configurable thread_id
   - Each node calls `pipeline_span()` context manager

4. **Node Tracing**
   - `pipeline_span()` creates independent MLflow trace via `mlflow.start_span()`
   - Immediately tags trace with `node`, `protocol_id`, `run_id`
   - Calls `span.set_inputs()` and `span.set_outputs()` to populate data
   - Trace flushed to MLflow as context manager exits (real-time appearance)

5. **API Request Tracing**
   - MLflowRequestMiddleware intercepts HTTP requests
   - Creates HTTP span with method and path
   - Records response status and latency
   - Skips health, ready, and root endpoints

---

### 9. Important Implementation Notes

**Why No Autolog:**
The codebase explicitly avoids `mlflow.langchain.autolog()` because it would wrap the entire pipeline in a single trace that updates constantly and only appears in MLflow after the full pipeline completes. Instead, independent node traces stream to MLflow in real-time.

**Thread Safety:**
- ContextVars ensure run_id and experiment_id propagate correctly across async/threading boundaries
- Orphan cleanup handles traces from crashed runs that didn't finish gracefully

**Fallback Behavior:**
- If MLFLOW_TRACKING_URI not set, all tracing is silently disabled
- If mlflow module not installed, ImportError is caught and tracing disabled
- If span creation fails, `_NoOpSpan` fallback prevents pipeline disruption

**Experiment Grouping:**
- One experiment per calendar day allows multiple workers/restarts to share same experiment
- All traces tagged with `protocol_id` and `run_id` for easy filtering in UI
agentId: a6bf29d2d20860017 (for resuming to continue this agent's work if needed)
<usage>total_tokens: 62039
tool_uses: 26
duration_ms: 54136</usage>
```

> TOOL

tool_result
id: toolu_016TNkoYx2pcFtpTSVfDt6iD
```
{
    "error_code": "INVALID_PARAMETER_VALUE",
    "message": "Invalid value 0 for parameter 'max_results' supplied. It must be a positive integer"
}
Also not on 5000
```

> AGENT

MLflow is reachable on port 5001. Let me query it properly and read the key tracing files.

> TOOL

tool_use Bash
id: toolu_01EbaJABNGfYAoe8m1ZCEwpv
```json
{
  "command": "curl -s 'http://localhost:5001/api/2.0/mlflow/experiments/search' -H 'Content-Type: application/json' -d '{\"max_results\": 10}' | python3 -m json.tool",
  "description": "Search MLflow experiments"
}
```

> TOOL

tool_result
id: toolu_01EbaJABNGfYAoe8m1ZCEwpv
```
{
    "experiments": [
        {
            "experiment_id": "17",
            "name": "protocol-processing-20260224",
            "artifact_location": "mlflow-artifacts:/17",
            "lifecycle_stage": "active",
            "last_update_time": 1771950502873,
            "creation_time": 1771950502873
        },
        {
            "experiment_id": "16",
            "name": "protocol-processing-20260224-162820",
            "artifact_location": "mlflow-artifacts:/16",
            "lifecycle_stage": "active",
            "last_update_time": 1771950500748,
            "creation_time": 1771950500748,
            "tags": [
                {
                    "key": "mlflow.experimentKind",
                    "value": "genai_development"
                }
            ]
        },
        {
            "experiment_id": "15",
            "name": "protocol-processing-20260224-162436",
            "artifact_location": "mlflow-artifacts:/15",
            "lifecycle_stage": "active",
            "last_update_time": 1771950276861,
            "creation_time": 1771950276861,
            "tags": [
                {
                    "key": "mlflow.experimentKind",
                    "value": "genai_development"
                }
            ]
        },
        {
            "experiment_id": "14",
            "name": "protocol-processing-20260224-162414",
            "artifact_location": "mlflow-artifacts:/14",
            "lifecycle_stage": "active",
            "last_update_time": 1771950255451,
            "creation_time": 1771950255451
        },
        {
            "experiment_id": "13",
            "name": "protocol-processing-20260224-162059",
            "artifact_location": "mlflow-artifacts:/13",
            "lifecycle_stage": "active",
            "last_update_time": 1771950059931,
            "creation_time": 1771950059931
        },
        {
            "experiment_id": "12",
            "name": "protocol-processing-20260224-161543",
            "artifact_location": "mlflow-artifacts:/12",
            "lifecycle_stage": "active",
            "last_update_time": 1771949744493,
            "creation_time": 1771949744493,
            "tags": [
                {
                    "key": "mlflow.experimentKind",
                    "value": "genai_development"
                }
            ]
        }
    ]
}
```

> TOOL

tool_use Read
id: toolu_01K7aNeCXduhZavVMpvYLPbs
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tracing.py"
}
```

> TOOL

tool_result
id: toolu_01K7aNeCXduhZavVMpvYLPbs
```
     1→"""MLflow tracing helpers for pipeline nodes.
     2→
     3→Provides a safe context manager that creates MLflow traces when available
     4→and falls back to a no-op when MLflow is not configured or installed.
     5→
     6→Each node creates its own separate top-level trace (not a child span),
     7→tagged with protocol_id and run_id so traces from the same pipeline run
     8→can be grouped and filtered in the MLflow UI.
     9→
    10→IMPORTANT: ``mlflow.langchain.autolog()`` must NOT be enabled.  Autolog
    11→wraps ``graph.ainvoke()`` in a single parent trace and all node spans
    12→become children — producing one constantly-updating trace that only
    13→appears after the full pipeline finishes.  Without autolog, each call to
    14→``mlflow.start_span()`` inside a node creates an independent root trace
    15→that is flushed to MLflow as soon as the context manager exits.
    16→
    17→Grouping tags set on every trace:
    18→    protocol_id  – groups all runs for a given protocol
    19→    run_id       – groups all node traces from the same pipeline invocation
    20→    node         – the node name (for easy filtering)
    21→"""
    22→
    23→from __future__ import annotations
    24→
    25→import contextvars
    26→import logging
    27→import os
    28→from contextlib import contextmanager
    29→from typing import Any
    30→
    31→logger = logging.getLogger(__name__)
    32→
    33→# ContextVar set once per pipeline invocation in trigger._run_pipeline().
    34→# Every node's pipeline_span() reads it to tag traces with a shared run_id.
    35→_pipeline_run_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    36→    "pipeline_run_id", default=""
    37→)
    38→
    39→# Experiment ID for pipeline traces. Set by trigger after _ensure_mlflow() so
    40→# spans carry the experiment ID; export then uses it even from another thread.
    41→_pipeline_experiment_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    42→    "pipeline_experiment_id", default=None
    43→)
    44→
    45→
    46→def set_pipeline_run_id(run_id: str) -> None:
    47→    """Set the current pipeline run_id (call before graph.ainvoke)."""
    48→    _pipeline_run_id.set(run_id)
    49→
    50→
    51→def set_pipeline_experiment_id(experiment_id: str | None) -> None:
    52→    """Set experiment ID for pipeline traces (after _ensure_mlflow in trigger)."""
    53→    _pipeline_experiment_id.set(experiment_id)
    54→
    55→
    56→@contextmanager
    57→def pipeline_span(
    58→    name: str,
    59→    span_type: str = "CHAIN",
    60→    protocol_id: str = "",
    61→):
    62→    """Create a separate MLflow trace for a pipeline node.
    63→
    64→    Each call creates its own top-level trace tagged with protocol_id
    65→    and run_id, so individual node traces appear in MLflow as they
    66→    complete rather than waiting for the entire pipeline to finish.
    67→
    68→    Filter in MLflow UI:
    69→        tags.protocol_id = "<id>"       – all runs for a protocol
    70→        tags.run_id      = "<run_id>"   – single pipeline invocation
    71→
    72→    Args:
    73→        name: Trace/span name (e.g., "ingest_node", "ground_node").
    74→        span_type: MLflow span type (default "CHAIN").
    75→        protocol_id: Protocol ID to tag the trace with for session grouping.
    76→
    77→    Yields:
    78→        MLflow Span object or a no-op wrapper.
    79→    """
    80→    try:
    81→        import mlflow
    82→        from mlflow.entities.trace_location import MlflowExperimentLocation
    83→
    84→        if os.getenv("MLFLOW_TRACKING_URI"):
    85→            # Pass experiment_id on span so export uses it even from another thread.
    86→            exp_id = _pipeline_experiment_id.get()
    87→            trace_destination = (
    88→                MlflowExperimentLocation(experiment_id=exp_id) if exp_id else None
    89→            )
    90→            with mlflow.start_span(
    91→                name=name,
    92→                span_type=span_type,
    93→                trace_destination=trace_destination,
    94→            ) as span:
    95→                # Tag the trace for grouping/filtering in the MLflow UI.
    96→                tags: dict[str, str] = {"node": name}
    97→                if protocol_id:
    98→                    tags["protocol_id"] = protocol_id
    99→                run_id = _pipeline_run_id.get()
   100→                if run_id:
   101→                    tags["run_id"] = run_id
   102→                try:
   103→                    mlflow.update_current_trace(tags=tags)
   104→                except Exception:
   105→                    logger.warning("MLflow tag update failed", exc_info=True)
   106→                yield span
   107→                return
   108→    except ImportError:
   109→        logger.warning("mlflow not installed — tracing disabled")
   110→    except Exception:
   111→        logger.warning(
   112→            "MLflow span creation failed, falling back to no-op", exc_info=True
   113→        )
   114→
   115→    # Fallback: no-op span
   116→    yield _NoOpSpan()
   117→
   118→
   119→class _NoOpSpan:
   120→    """No-op span that silently accepts MLflow span API calls."""
   121→
   122→    def set_inputs(self, inputs: dict[str, Any]) -> None:
   123→        pass
   124→
   125→    def set_outputs(self, outputs: dict[str, Any]) -> None:
   126→        pass
   127→
   128→    def set_status(self, status: str) -> None:
   129→        pass
   130→
```

> TOOL

tool_use Read
id: toolu_01VQUKwhDDfHMSGBFjMGPN3o
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/trigger.py"
}
```

> TOOL

tool_result
id: toolu_01VQUKwhDDfHMSGBFjMGPN3o
```
     1→"""Unified outbox event handler for ProtocolUploaded events.
     2→
     3→Replaces the two-service trigger pattern (extraction_service + grounding_service)
     4→with a single consolidated handler that invokes the full 5-node pipeline:
     5→ingest -> extract -> parse -> ground -> persist
     6→
     7→Per user decision (v2.0): "Remove criteria_extracted outbox, retain protocol_uploaded"
     8→
     9→The handler is synchronous (called by OutboxProcessor.poll_and_process) and
    10→bridges to the async graph via asyncio.run(). This works without event loop
    11→conflicts because the outbox processor runs handlers in a thread executor
    12→via run_in_executor, so there is no existing event loop in the current thread.
    13→
    14→Checkpointing: Each invocation generates a unique thread_id (protocol_id:uuid4)
    15→and stores it in protocol.metadata_ so that retry_from_checkpoint can look it up.
    16→This prevents checkpoint collision when re-extracting the same protocol.
    17→"""
    18→
    19→from __future__ import annotations
    20→
    21→import asyncio
    22→import logging
    23→import os
    24→from typing import Any
    25→from uuid import uuid4
    26→
    27→from api_service.storage import engine
    28→from shared.exceptions import AuthExpiredError
    29→from shared.models import Protocol
    30→from sqlmodel import Session
    31→
    32→logger = logging.getLogger(__name__)
    33→
    34→
    35→def _cleanup_orphan_traces() -> None:
    36→    """Close stale IN_PROGRESS MLflow traces from previous crashed runs.
    37→
    38→    Runs once at module import (service startup). Idempotent -- safe to
    39→    call multiple times. Only closes traces older than 1 hour to avoid
    40→    closing currently-running pipelines.
    41→    """
    42→    import time as _time
    43→
    44→    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    45→    if not tracking_uri:
    46→        return
    47→    try:
    48→        import mlflow
    49→
    50→        client = mlflow.MlflowClient()
    51→        cutoff_ms = int((_time.time() - 3600) * 1000)  # 1 hour ago
    52→
    53→        # MLflow 3.x: search for traces with IN_PROGRESS status
    54→        try:
    55→            traces = client.search_traces(
    56→                filter_string="status = 'IN_PROGRESS'",
    57→                max_results=50,
    58→            )
    59→        except (AttributeError, TypeError):
    60→            # search_traces may not exist or have different signature
    61→            logger.warning("MLflow search_traces API not available for orphan cleanup")
    62→            return
    63→
    64→        closed = 0
    65→        for trace in traces:
    66→            trace_ts = getattr(trace.info, "timestamp_ms", None) or 0
    67→            if trace_ts < cutoff_ms:
    68→                try:
    69→                    client.end_trace(
    70→                        request_id=trace.info.request_id,
    71→                        status="ERROR",
    72→                    )
    73→                    closed += 1
    74→                except Exception:
    75→                    logger.debug(
    76→                        "Trace %s already closed, skipping",
    77→                        trace.info.request_id,
    78→                    )
    79→        if closed:
    80→            logger.info(
    81→                "Startup orphan cleanup: closed %d stale IN_PROGRESS trace(s)",
    82→                closed,
    83→            )
    84→    except Exception:
    85→        logger.warning("Orphan trace cleanup failed (non-fatal)", exc_info=True)
    86→
    87→
    88→# Run once at startup to clean up orphaned traces from previous crashes
    89→_cleanup_orphan_traces()
    90→
    91→
    92→_mlflow_experiment_name: str | None = None
    93→
    94→
    95→def _get_experiment_name() -> str:
    96→    """Return MLflow experiment name: one per day so all runs share it."""
    97→    global _mlflow_experiment_name
    98→    if _mlflow_experiment_name is None:
    99→        from datetime import datetime, timezone
   100→
   101→        # Date only: one experiment per day; avoids one per process/restart.
   102→        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
   103→        _mlflow_experiment_name = f"protocol-processing-{date_str}"
   104→    return _mlflow_experiment_name
   105→
   106→
   107→def _ensure_mlflow() -> bool:
   108→    """Ensure MLflow tracking is configured in the current thread.
   109→
   110→    Uses one experiment per day (protocol-processing-YYYYMMDD) so all runs
   111→    and workers share the same experiment in the MLflow UI.
   112→    """
   113→    try:
   114→        import mlflow
   115→
   116→        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
   117→        if tracking_uri:
   118→            mlflow.set_tracking_uri(tracking_uri)
   119→            mlflow.set_experiment(_get_experiment_name())
   120→            return True
   121→    except ImportError:
   122→        logger.warning("mlflow not installed — tracing disabled")
   123→    except Exception:
   124→        logger.warning("MLflow setup failed — tracing disabled", exc_info=True)
   125→    return False
   126→
   127→
   128→def _is_auth_expired_error(e: BaseException) -> bool:
   129→    """Return True if the exception is or was caused by credential refresh failure.
   130→
   131→    Checks the exception and its __cause__ chain so gRPC-wrapped RefreshErrors
   132→    are detected. Used to avoid retries and to raise AuthExpiredError for the outbox.
   133→    """
   134→    try:
   135→        from google.auth.exceptions import RefreshError
   136→    except ImportError:
   137→        return False
   138→    exc: BaseException | None = e
   139→    while exc is not None:
   140→        if isinstance(exc, RefreshError):
   141→            return True
   142→        exc = getattr(exc, "__cause__", None)
   143→    return False
   144→
   145→
   146→def _categorize_pipeline_error(e: Exception) -> str:
   147→    """Convert exception to human-readable pipeline error reason.
   148→
   149→    Combines extraction and grounding error categorization from both
   150→    the old extraction_service and grounding_service triggers.
   151→
   152→    Args:
   153→        e: The exception that occurred during pipeline execution.
   154→
   155→    Returns:
   156→        Human-readable error message for the user.
   157→    """
   158→    if isinstance(e, DependencyCheckError):
   159→        return f"Infrastructure dependency unavailable: {e}"
   160→
   161→    error_str = str(e).lower()
   162→
   163→    # PDF / extraction errors
   164→    if "pdf" in error_str or "pymupdf" in error_str:
   165→        return "PDF text quality too low or file corrupted"
   166→    if "gcs" in error_str or "storage" in error_str or "bucket" in error_str:
   167→        return "File storage service unavailable"
   168→
   169→    # Auth / credential errors (do not retry — trigger login in UI)
   170→    if "credential" in error_str or "auth" in error_str or "refresherror" in error_str:
   171→        return "Google credentials expired — sign in again"
   172→
   173→    # UMLS / grounding errors
   174→    if "mcp" in error_str or "subprocess" in error_str:
   175→        return "UMLS grounding service unavailable"
   176→    if "concept_linking" in error_str or "concept_search" in error_str:
   177→        return "UMLS terminology service unavailable"
   178→
   179→    # Generic transient errors
   180→    if "circuit" in error_str:
   181→        return "AI service temporarily unavailable"
   182→    if "timeout" in error_str or "timed out" in error_str:
   183→        return "Processing timed out"
   184→    if "parse" in error_str:
   185→        return "Protocol parsing failed"
   186→
   187→    return f"Pipeline failed: {type(e).__name__}"
   188→
   189→
   190→def _update_protocol_failed(
   191→    protocol_id: str,
   192→    reason: str,
   193→    error_category: str,
   194→    exception_type: str,
   195→) -> None:
   196→    """Update protocol status to extraction_failed with error metadata.
   197→
   198→    Args:
   199→        protocol_id: Protocol ID to update.
   200→        reason: Human-readable error reason.
   201→        error_category: Short category string for the error type.
   202→        exception_type: Python exception class name.
   203→    """
   204→    try:
   205→        with Session(engine) as session:
   206→            protocol = session.get(Protocol, protocol_id)
   207→            if protocol:
   208→                protocol.status = "extraction_failed"
   209→                protocol.error_reason = reason
   210→                protocol.metadata_ = {
   211→                    **protocol.metadata_,
   212→                    "error": {
   213→                        "category": error_category,
   214→                        "reason": reason,
   215→                        "exception_type": exception_type,
   216→                    },
   217→                }
   218→                session.add(protocol)
   219→                session.commit()
   220→    except Exception:
   221→        logger.exception(
   222→            "Failed to update protocol %s status to extraction_failed",
   223→            protocol_id,
   224→        )
   225→
   226→
   227→async def _run_pipeline(
   228→    initial_state: dict[str, Any],
   229→    config: dict[str, Any],
   230→    payload: dict[str, Any],
   231→) -> dict[str, Any]:
   232→    """Run the pipeline graph with MLflow tracing inside the async context.
   233→
   234→    MLflow ContextVars must be created in the same async context as the
   235→    LangGraph invocation. asyncio.run() creates an isolated context, so
   236→    we initialize MLflow tracing HERE (inside asyncio.run) rather than
   237→    in the sync caller.
   238→
   239→    Each pipeline node creates its own separate MLflow trace tagged with
   240→    protocol_id and run_id, so traces appear in the MLflow UI as they
   241→    complete rather than waiting for the entire pipeline. Filter by the
   242→    run_id tag to see all traces from a single pipeline invocation.
   243→    """
   244→    from protocol_processor.graph import get_graph
   245→    from protocol_processor.tracing import set_pipeline_run_id
   246→
   247→    graph = await get_graph()
   248→
   249→    # MLflow tracing: do NOT enable langchain.autolog() here.
   250→    # Autolog wraps the entire ainvoke() in a single trace that only
   251→    # appears in MLflow after the full pipeline completes.  Instead,
   252→    # each node creates its own independent trace via pipeline_span()
   253→    # so traces appear in real-time as nodes finish.
   254→    # MLflow for this thread is set by handle_protocol_uploaded() via
   255→    # _ensure_mlflow() (protocol-processing-YYYYMMDD). Do not call
   256→    # _ensure_mlflow() again here.
   257→
   258→    # Set run_id so every node's pipeline_span() tags its trace with the
   259→    # same identifier.  Uses the thread_id which is "{protocol_id}:{uuid4}".
   260→    thread_id = config.get("configurable", {}).get("thread_id", "")
   261→    if thread_id:
   262→        set_pipeline_run_id(thread_id)
   263→
   264→    return await graph.ainvoke(initial_state, config)
   265→
   266→
   267→class DependencyCheckError(RuntimeError):
   268→    """Raised when a required infrastructure dependency is unreachable."""
   269→
   270→
   271→def _preflight_check() -> None:
   272→    """Verify infrastructure dependencies are reachable before starting the pipeline.
   273→
   274→    Checks: PostgreSQL (main DB), OMOP vocabulary DB, and MLflow tracking server.
   275→    Raises DependencyCheckError on the first failure so the pipeline never starts
   276→    and no API calls (Gemini, ToolUniverse, etc.) are wasted.
   277→    """
   278→    import urllib.request
   279→
   280→    from sqlalchemy import text
   281→
   282→    # 1. Main database (required for persist, parse, etc.)
   283→    try:
   284→        with engine.connect() as conn:
   285→            conn.execute(text("SELECT 1"))
   286→    except Exception as exc:
   287→        raise DependencyCheckError(
   288→            f"Main database (DATABASE_URL) is not reachable: {exc}"
   289→        ) from exc
   290→
   291→    # 2. OMOP vocabulary database (required for dual grounding)
   292→    try:
   293→        from protocol_processor.tools.omop_mapper import _get_omop_engine
   294→
   295→        omop_engine = _get_omop_engine()
   296→        with omop_engine.connect() as conn:
   297→            conn.execute(text("SELECT 1"))
   298→    except Exception as exc:
   299→        raise DependencyCheckError(
   300→            f"OMOP vocabulary database (OMOP_VOCAB_URL) is not reachable: {exc}"
   301→        ) from exc
   302→
   303→    # 3. MLflow tracking server (required for observability)
   304→    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
   305→    if not tracking_uri:
   306→        raise DependencyCheckError(
   307→            "MLFLOW_TRACKING_URI environment variable is not set"
   308→        )
   309→    try:
   310→        req = urllib.request.Request(f"{tracking_uri}/health", method="GET")
   311→        with urllib.request.urlopen(req, timeout=5) as resp:
   312→            if resp.status >= 400:
   313→                raise DependencyCheckError(
   314→                    f"MLflow health check returned HTTP {resp.status}"
   315→                )
   316→    except DependencyCheckError:
   317→        raise
   318→    except Exception as exc:
   319→        raise DependencyCheckError(
   320→            f"MLflow tracking server ({tracking_uri}) is not reachable: {exc}"
   321→        ) from exc
   322→
   323→    logger.info("Pre-flight checks passed: DB, OMOP, MLflow all reachable")
   324→
   325→
   326→def handle_protocol_uploaded(payload: dict[str, Any]) -> None:
   327→    """Handle a ProtocolUploaded event by running the full pipeline.
   328→
   329→    Constructs the initial PipelineState from the event payload and
   330→    invokes the consolidated 5-node LangGraph workflow via asyncio.run().
   331→
   332→    Uses protocol_id as the LangGraph thread_id so that retry_from_checkpoint
   333→    can locate the saved checkpoint by protocol_id alone.
   334→
   335→    Replaces both extraction_service.trigger.handle_protocol_uploaded and
   336→    grounding_service.trigger.handle_criteria_extracted from the v1.x
   337→    two-service architecture.
   338→
   339→    Args:
   340→        payload: Event payload dict containing protocol_id, file_uri, and title.
   341→
   342→    Raises:
   343→        DependencyCheckError: If DB, OMOP, or MLflow is unreachable.
   344→        Exception: Re-raised after logging to let the outbox processor
   345→            mark the event as failed for retry.
   346→    """
   347→    # Pre-flight: verify all infrastructure dependencies are up before
   348→    # spending any Gemini/ToolUniverse API calls.
   349→    _preflight_check()
   350→
   351→    # Set MLflow experiment for this worker thread (protocol-processing-YYYYMMDD).
   352→    # Without this, the thread would use default experiment ID 0, which may be deleted.
   353→    _ensure_mlflow()
   354→    # So pipeline spans carry the experiment ID and export works from any thread.
   355→    try:
   356→        import mlflow
   357→
   358→        from protocol_processor.tracing import set_pipeline_experiment_id
   359→
   360→        exp = mlflow.get_experiment_by_name(_get_experiment_name())
   361→        if exp:
   362→            set_pipeline_experiment_id(exp.experiment_id)
   363→        else:
   364→            set_pipeline_experiment_id(None)
   365→    except Exception:
   366→        logger.debug("Could not set pipeline experiment ID for tracing", exc_info=True)
   367→
   368→    protocol_id = payload.get("protocol_id", "unknown")
   369→    logger.info(
   370→        "Handling ProtocolUploaded event for protocol %s (consolidated pipeline)",
   371→        protocol_id,
   372→    )
   373→
   374→    try:
   375→        # Generate unique thread_id per pipeline run to prevent checkpoint collision
   376→        # on re-extraction (same protocol_id would resume old completed checkpoint)
   377→        thread_id = f"{protocol_id}:{uuid4()}"
   378→
   379→        initial_state: dict[str, Any] = {
   380→            "protocol_id": payload["protocol_id"],
   381→            "file_uri": payload["file_uri"],
   382→            "title": payload["title"],
   383→            "batch_id": None,
   384→            "pdf_bytes": None,
   385→            "extraction_json": None,
   386→            "entities_json": None,
   387→            "grounded_entities_json": None,
   388→            "archived_reviewed_criteria": payload.get("archived_reviewed_criteria"),
   389→            "status": "processing",
   390→            "error": None,
   391→            "errors": [],
   392→        }
   393→
   394→        # Store thread_id in protocol metadata for retry_from_checkpoint lookup
   395→        try:
   396→            with Session(engine) as session:
   397→                protocol = session.get(Protocol, protocol_id)
   398→                if protocol:
   399→                    meta = protocol.metadata_ or {}
   400→                    protocol.metadata_ = {
   401→                        **meta,
   402→                        "pipeline_thread_id": thread_id,
   403→                    }
   404→                    session.add(protocol)
   405→                    session.commit()
   406→        except Exception:
   407→            logger.warning(
   408→                "Failed to store pipeline_thread_id for protocol %s",
   409→                protocol_id,
   410→            )
   411→
   412→        config = {"configurable": {"thread_id": thread_id}}
   413→
   414→        asyncio.run(_run_pipeline(initial_state, config, payload))
   415→
   416→        logger.info(
   417→            "Protocol pipeline completed for protocol %s",
   418→            protocol_id,
   419→        )
   420→
   421→    except Exception as e:
   422→        logger.exception(
   423→            "Protocol pipeline failed for protocol %s",
   424→            protocol_id,
   425→        )
   426→        reason = _categorize_pipeline_error(e)
   427→        # Auth expiry: do not retry; outbox marks dead_letter, UI shows login.
   428→        is_auth_expired = _is_auth_expired_error(e)
   429→        category = "auth_expired" if is_auth_expired else "pipeline_failed"
   430→        _update_protocol_failed(
   431→            protocol_id,
   432→            reason,
   433→            category,
   434→            type(e).__name__,
   435→        )
   436→        if is_auth_expired:
   437→            raise AuthExpiredError("Google credentials expired — sign in again") from e
   438→        raise
   439→
   440→
   441→async def retry_from_checkpoint(protocol_id: str) -> dict[str, Any]:
   442→    """Resume pipeline from last checkpoint for a failed protocol.
   443→
   444→    Passes None as the input state to graph.ainvoke, which tells LangGraph
   445→    to resume from the last saved checkpoint for the given thread_id instead
   446→    of starting from scratch. Reads thread_id from protocol.metadata_ where
   447→    it was stored during the original pipeline invocation.
   448→
   449→    Args:
   450→        protocol_id: Protocol ID — used to look up thread_id from metadata.
   451→
   452→    Returns:
   453→        Final pipeline state dict after resuming from checkpoint.
   454→    """
   455→    with Session(engine) as session:
   456→        protocol = session.get(Protocol, protocol_id)
   457→        if not protocol:
   458→            raise ValueError(f"Protocol {protocol_id} not found")
   459→        thread_id = (protocol.metadata_ or {}).get("pipeline_thread_id", protocol_id)
   460→
   461→    from protocol_processor.graph import get_graph
   462→
   463→    graph = await get_graph()
   464→    config = {"configurable": {"thread_id": thread_id}}
   465→    # Pass None as input — LangGraph resumes from last checkpoint
   466→    result = await graph.ainvoke(None, config)
   467→    return result
   468→
```

> AGENT

Now let me query the most recent experiment for traces.

> TOOL

tool_use Bash
id: toolu_013aSLhsYxPJQPoF9JYQ8e9z
```json
{
  "command": "curl -s 'http://localhost:5001/api/2.0/mlflow/traces?experiment_id=17&max_results=20' 2>/dev/null | python3 -m json.tool 2>/dev/null || echo \"Traces endpoint not available, trying search...\"",
  "description": "Query traces from latest experiment"
}
```

> TOOL

tool_result
id: toolu_013aSLhsYxPJQPoF9JYQ8e9z
```
{
    "error_code": "INVALID_PARAMETER_VALUE",
    "message": "Missing value for required parameter 'experiment_ids'. See the API docs for more information about request parameters."
}
```

> TOOL

tool_use Bash
id: toolu_01NxmpExKhnKzNWsuRU9rZoU
```json
{
  "command": "curl -s 'http://localhost:5001/api/2.0/mlflow/traces/search' -H 'Content-Type: application/json' -d '{\"experiment_ids\": [\"17\"], \"max_results\": 20}' 2>/dev/null | python3 -m json.tool 2>/dev/null || echo \"Search traces failed too\"",
  "description": "Search traces via POST"
}
```

> TOOL

tool_result
id: toolu_01NxmpExKhnKzNWsuRU9rZoU
```
Search traces failed too
```

> TOOL

tool_use Bash
id: toolu_01E97tsW3YXieKSWYXVpW5EW
```json
{
  "command": "# Try the MLflow 3.x REST API for traces\ncurl -s 'http://localhost:5001/api/2.0/mlflow/traces?experiment_ids=17&max_results=20' 2>/dev/null | python3 -m json.tool 2>/dev/null",
  "description": "Query traces with correct param format"
}
```

> TOOL

tool_result
id: toolu_01E97tsW3YXieKSWYXVpW5EW
```
<persisted-output>
Output too large (51.1KB). Full output saved to: /Users/noahdolevelixir/.REDACTED.txt

Preview (first 2KB):
{
    "traces": [
        {
            "request_id": "tr-f1272edd03bf8a1be1a5ae453382f1d7",
            "experiment_id": "17",
            "timestamp_ms": 1771951413128,
            "execution_time_ms": 10,
            "status": "OK",
            "request_metadata": [
                {
                    "key": "mlflow.trace_schema.version",
                    "value": "3"
                },
                {
                    "key": "mlflow.traceInputs",
                    "value": "{\"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\"}"
                },
                {
                    "key": "mlflow.trace.sizeStats",
                    "value": "{\"total_size_bytes\": 1815, \"num_spans\": 1, \"max\": 621, \"p25\": 621, \"p50\": 621, \"p75\": 621}"
                },
                {
                    "key": "mlflow.source.type",
                    "value": "LOCAL"
                },
                {
                    "key": "mlflow.source.git.branch",
                    "value": "feat/submission-additions"
                },
                {
                    "key": "mlflow.source.name",
                    "value": "/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/bin/uvicorn"
                },
                {
                    "key": "mlflow.source.git.commit",
                    "value": "38b14c3888047698c3f98000257e48c9e4e4d033"
                },
                {
                    "key": "mlflow.user",
                    "value": "noahdolevelixir"
                },
                {
                    "key": "mlflow.traceOutputs",
                    "value": "{\"status_code\": 200, \"latency_ms\": 10.72}"
                },
                {
                    "key": "mlflow.source.git.repoURL",
                    "value": "git@github.com:ElixirTrials/medgemma-hackathon.git"
                },
                {
...
</persisted-output>
```

> TOOL

tool_use Bash
id: toolu_01H4iz7pE6VhFftYWNLjEYRL
```json
{
  "command": "# Also try using the MLflow Python client directly\nuv run python3 -c \"\nimport mlflow\nimport json\n\nmlflow.set_tracking_uri('http://localhost:5001')\nclient = mlflow.MlflowClient()\n\n# Check all experiments for traces\nfor exp_id in ['17', '16', '15', '14', '13', '12']:\n    try:\n        traces = client.search_traces(experiment_ids=[exp_id], max_results=5)\n        if traces:\n            print(f'=== Experiment {exp_id}: {len(traces)} traces ===')\n            for t in traces:\n                print(f'  request_id={t.info.request_id}, status={t.info.status}, timestamp={t.info.timestamp_ms}')\n                if hasattr(t.info, 'tags') and t.info.tags:\n                    print(f'    tags={t.info.tags}')\n        else:\n            print(f'=== Experiment {exp_id}: NO traces ===')\n    except Exception as e:\n        print(f'=== Experiment {exp_id}: ERROR - {e} ===')\n\" 2>&1",
  "description": "Query MLflow traces via Python client"
}
```

> TOOL

tool_result
id: toolu_01H4iz7pE6VhFftYWNLjEYRL
```
<string>:11: FutureWarning: Parameter 'experiment_ids' is deprecated. Please use 'locations' instead.
<string>:11: FutureWarning: Parameter 'experiment_ids' is deprecated. Please use 'locations' instead.
=== Experiment 17: 5 traces ===
  request_id=tr-f1272edd03bf8a1be1a5ae453382f1d7, status=TraceStatus.OK, timestamp=1771951413128
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/17/traces/tr-f1272edd03bf8a1be1a5ae453382f1d7/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /criteria/structured'}
  request_id=tr-ce99a5da5c57600365ab1c3e02a672cb, status=TraceStatus.OK, timestamp=1771951413095
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/17/traces/tr-ce99a5da5c57600365ab1c3e02a672cb/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'OPTIONS /criteria/structured'}
  request_id=tr-595f0b7f04bb092fd0649663c50125a6, status=TraceStatus.OK, timestamp=1771951408096
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/17/traces/tr-595f0b7f04bb092fd0649663c50125a6/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /api/terminology/umls/search'}
  request_id=tr-ddd9d87038ed2af04d3dfb3df8e3563c, status=TraceStatus.OK, timestamp=1771951408003
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/17/traces/tr-ddd9d87038ed2af04d3dfb3df8e3563c/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /api/terminology/umls/search'}
  request_id=tr-097c8fecefbdf521d71097762951d2f3, status=TraceStatus.OK, timestamp=1771951407979
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/17/traces/tr-097c8fecefbdf521d71097762951d2f3/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'OPTIONS /api/terminology/umls/search'}
=== Experiment 16: NO traces ===
=== Experiment 15: 5 traces ===
  request_id=tr-44629d1f8d607a8d7396d0170bfa45f6, status=TraceStatus.OK, timestamp=1771950497347
    tags={'node': 'ordinal_resolve_node', 'mlflow.traceName': 'ordinal_resolve_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/15/traces/tr-44629d1f8d607a8d7396d0170bfa45f6/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '54a7af98-770b-4275-9f57-ae74e06edc11:4a262846-fa8e-481c-b2fa-335bff02cded', 'protocol_id': '54a7af98-770b-4275-9f57-ae74e06edc11'}
  request_id=tr-83fe4068da1bfa77ed2ecc6381bd0fb0, status=TraceStatus.OK, timestamp=1771950490742
    tags={'node': 'structure_node', 'mlflow.traceName': 'structure_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/15/traces/tr-83fe4068da1bfa77ed2ecc6381bd0fb0/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '54a7af98-770b-4275-9f57-ae74e06edc11:4a262846-fa8e-481c-b2fa-335bff02cded', 'protocol_id': '54a7af98-770b-4275-9f57-ae74e06edc11'}
  request_id=tr-633562f95faf9694949228d988234174, status=TraceStatus.OK, timestamp=1771950490696
    tags={'node': 'persist_node', 'mlflow.traceName': 'persist_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/15/traces/tr-633562f95faf9694949228d988234174/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '54a7af98-770b-4275-9f57-ae74e06edc11:4a262846-fa8e-481c-b2fa-335bff02cded', 'protocol_id': '54a7af98-770b-4275-9f57-ae74e06edc11'}
  request_id=tr-c310a5577bb65f4c9cfbcab3f2049345, status=TraceStatus.OK, timestamp=1771950462179
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/15/traces/tr-c310a5577bb65f4c9cfbcab3f2049345/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /criteria/structured'}
  request_id=tr-468559911fe3e7fe423a8066a68579c2, status=TraceStatus.OK, timestamp=1771950462161
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/15/traces/tr-468559911fe3e7fe423a8066a68579c2/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'OPTIONS /criteria/structured'}
=== Experiment 14: 5 traces ===
  request_id=tr-e82f5921971f152d2c6eba92f4dcecce, status=TraceStatus.OK, timestamp=1771950255775
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/14/traces/tr-e82f5921971f152d2c6eba92f4dcecce/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /reviews/pending-summary'}
  request_id=tr-d23a1f9c0a9064d0cb3fbecb542ed01c, status=TraceStatus.OK, timestamp=1771950255761
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/14/traces/tr-d23a1f9c0a9064d0cb3fbecb542ed01c/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /reviews/audit-log'}
  request_id=tr-3f14143c093d8431b367a15c34dc8e56, status=TraceStatus.OK, timestamp=1771950255757
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/14/traces/tr-3f14143c093d8431b367a15c34dc8e56/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'GET /reviews/pipeline-summary'}
  request_id=tr-91e3689b4ff0ce2388b1ff1a9511ad77, status=TraceStatus.OK, timestamp=1771950255737
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/14/traces/tr-91e3689b4ff0ce2388b1ff1a9511ad77/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'OPTIONS /reviews/pending-summary'}
  request_id=tr-686b4da694f9cb6c931ed312f42b1ad1, status=TraceStatus.OK, timestamp=1771950255710
    tags={'mlflow.artifactLocation': 'mlflow-artifacts:/14/traces/tr-686b4da694f9cb6c931ed312f42b1ad1/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'mlflow.traceName': 'OPTIONS /reviews/audit-log'}
=== Experiment 13: 3 traces ===
  request_id=tr-b643b50bcfd7200d59e71075f3d6bb64, status=TraceStatus.OK, timestamp=1771950133682
    tags={'node': 'parse_node', 'mlflow.traceName': 'parse_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/13/traces/tr-b643b50bcfd7200d59e71075f3d6bb64/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc:9edd5fc5-c33e-4565-82d8-0c99171fb215', 'protocol_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc'}
  request_id=tr-6964a6004d7b7fdee324ca55380d623e, status=TraceStatus.OK, timestamp=1771950062853
    tags={'node': 'extract_node', 'mlflow.traceName': 'extract_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/13/traces/tr-6964a6004d7b7fdee324ca55380d623e/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc:9edd5fc5-c33e-4565-82d8-0c99171fb215', 'protocol_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc'}
  request_id=tr-68a9226a2ff4cb00a2354c31e35a5061, status=TraceStatus.OK, timestamp=1771950062758
    tags={'node': 'ingest_node', 'mlflow.traceName': 'ingest_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/13/traces/tr-68a9226a2ff4cb00a2354c31e35a5061/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc:9edd5fc5-c33e-4565-82d8-0c99171fb215', 'protocol_id': 'dea87c2d-b2b8-46eb-ac9b-dd28460f67dc'}
=== Experiment 12: 5 traces ===
  request_id=tr-560f69abb70a421c96a272edf0a41342, status=TraceStatus.OK, timestamp=1771950057733
    tags={'node': 'ordinal_resolve_node', 'mlflow.traceName': 'ordinal_resolve_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/12/traces/tr-560f69abb70a421c96a272edf0a41342/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a:8d361395-9da7-4962-8ae8-e5221f521f51', 'protocol_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a'}
  request_id=tr-603012345767f0c6a947816801f70d55, status=TraceStatus.OK, timestamp=1771950050718
    tags={'node': 'structure_node', 'mlflow.traceName': 'structure_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/12/traces/tr-603012345767f0c6a947816801f70d55/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a:8d361395-9da7-4962-8ae8-e5221f521f51', 'protocol_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a'}
  request_id=tr-3383fadc334c447ec626f86130b5d391, status=TraceStatus.OK, timestamp=1771950050669
    tags={'node': 'persist_node', 'mlflow.traceName': 'persist_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/12/traces/tr-3383fadc334c447ec626f86130b5d391/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a:8d361395-9da7-4962-8ae8-e5221f521f51', 'protocol_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a'}
  request_id=tr-b3596a3bd6e87d7b03d1a220b9784ed8, status=TraceStatus.OK, timestamp=1771949863722
    tags={'node': 'ground_node', 'mlflow.traceName': 'ground_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/12/traces/tr-b3596a3bd6e87d7b03d1a220b9784ed8/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a:8d361395-9da7-4962-8ae8-e5221f521f51', 'protocol_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a'}
  request_id=tr-92caa31fd99f933990ef869a6c234046, status=TraceStatus.OK, timestamp=1771949855635
    tags={'node': 'parse_node', 'mlflow.traceName': 'parse_node', 'mlflow.artifactLocation': 'mlflow-artifacts:/12/traces/tr-92caa31fd99f933990ef869a6c234046/artifacts', 'mlflow.trace.spansLocation': 'TRACKING_STORE', 'run_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a:8d361395-9da7-4962-8ae8-e5221f521f51', 'protocol_id': '80a24a86-3805-47f5-bf7b-6e7e77491f5a'}
```

> AGENT

Now let me get the full picture of experiment 17 (the most recent run) and check for pipeline node traces vs HTTP traces.

> TOOL

tool_use Bash
id: toolu_018UnpUwdHzas4bT6w6bVtXt
```json
{
  "command": "uv run python3 -c \"\nimport mlflow\n\nmlflow.set_tracking_uri('http://localhost:5001')\nclient = mlflow.MlflowClient()\n\n# Get ALL traces from experiment 17 (latest)\ntraces = client.search_traces(experiment_ids=['17'], max_results=100)\nprint(f'Total traces in experiment 17: {len(traces)}')\nprint()\n\npipeline_traces = []\nhttp_traces = []\n\nfor t in traces:\n    tags = t.info.tags or {}\n    name = tags.get('mlflow.traceName', 'unknown')\n    node = tags.get('node', '')\n    if node:\n        pipeline_traces.append((name, t.info.status, t.info.timestamp_ms, tags.get('protocol_id', ''), tags.get('run_id', '')))\n    else:\n        http_traces.append((name, t.info.status, t.info.timestamp_ms))\n\nprint(f'Pipeline node traces: {len(pipeline_traces)}')\nfor name, status, ts, pid, rid in pipeline_traces:\n    print(f'  {name} | status={status} | protocol={pid}')\n\nprint(f'\\nHTTP traces: {len(http_traces)}')\nfor name, status, ts in http_traces:\n    print(f'  {name} | status={status}')\n\" 2>&1 | grep -v FutureWarning",
  "description": "Categorize traces in latest experiment"
}
```

> TOOL

tool_result
id: toolu_018UnpUwdHzas4bT6w6bVtXt
```
Total traces in experiment 17: 67

Pipeline node traces: 7
  ordinal_resolve_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  structure_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  persist_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  ground_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  parse_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  extract_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
  ingest_node | status=TraceStatus.OK | protocol=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3

HTTP traces: 60
  GET /criteria/structured | status=TraceStatus.OK
  OPTIONS /criteria/structured | status=TraceStatus.OK
  GET /api/terminology/umls/search | status=TraceStatus.OK
  GET /api/terminology/umls/search | status=TraceStatus.OK
  OPTIONS /api/terminology/umls/search | status=TraceStatus.OK
  GET /local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf | status=TraceStatus.OK
  GET REDACTED | status=TraceStatus.OK
  OPTIONS REDACTED | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/batches | status=TraceStatus.OK
  GET /entities/batch/0b03d48a-4987-4085-b8a0-56046216778a | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /entities/batch/0b03d48a-4987-4085-b8a0-56046216778a | status=TraceStatus.OK
  OPTIONS /reviews/batches | status=TraceStatus.OK
  GET /reviews/batches/0b03d48a-4987-4085-b8a0-56046216778a/criteria | status=TraceStatus.OK
  OPTIONS /reviews/batches/0b03d48a-4987-4085-b8a0-56046216778a/criteria | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /reviews/batches/0b03d48a-4987-4085-b8a0-56046216778a/metrics | status=TraceStatus.OK
  OPTIONS /reviews/batches/0b03d48a-4987-4085-b8a0-56046216778a/metrics | status=TraceStatus.OK
  GET /reviews/batches | status=TraceStatus.OK
  GET /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /reviews/pending-summary | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/pipeline-summary | status=TraceStatus.OK
  OPTIONS /reviews/batches | status=TraceStatus.OK
  OPTIONS /protocols/165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3 | status=TraceStatus.OK
  GET /protocols | status=TraceStatus.OK
  POST REDACTED | status=TraceStatus.OK
  OPTIONS REDACTED | status=TraceStatus.OK
  PUT /local-upload/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf | status=TraceStatus.OK
  OPTIONS /local-upload/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf | status=TraceStatus.OK
  POST /protocols/upload | status=TraceStatus.OK
  OPTIONS /protocols/upload | status=TraceStatus.OK
  GET /protocols | status=TraceStatus.OK
  OPTIONS /protocols | status=TraceStatus.OK
  GET /reviews/audit-log | status=TraceStatus.OK
  GET /reviews/pending-summary | status=TraceStatus.OK
  GET /reviews/pipeline-summary | status=TraceStatus.OK
  OPTIONS /reviews/pending-summary | status=TraceStatus.OK
  OPTIONS /reviews/audit-log | status=TraceStatus.OK
  OPTIONS /reviews/pipeline-summary | status=TraceStatus.OK
```

> AGENT

The data is clear. Here's the root cause analysis:

## Root Cause Analysis: MLflow Tracing IS Working

**The traces are there.** Experiment 17 (`protocol-processing-20260224`) contains **67 traces total**:

- **7 pipeline node traces** — all 7 nodes recorded successfully for protocol `165bb2ac`:
  1. `ingest_node`
  2. `extract_node`
  3. `parse_node`
  4. `ground_node`
  5. `persist_node`
  6. `structure_node`
  7. `ordinal_resolve_node`

- **60 HTTP middleware traces** — API requests (GET/POST/PUT/OPTIONS)

### Why you may not be seeing them in the MLflow UI

The problem is **experiment fragmentation**. You have **6 experiments** created today alone:

| ID | Name | Has pipeline traces? |
|----|------|---------------------|
| 17 | `protocol-processing-20260224` | Yes (7 node + 60 HTTP) |
| 16 | `protocol-processing-20260224-162820` | No |
| 15 | `protocol-processing-20260224-162436` | Yes (3 node) |
| 14 | `protocol-processing-20260224-162414` | HTTP only |
| 13 | `protocol-processing-20260224-162059` | Yes (3 node — incomplete run) |
| 12 | `protocol-processing-20260224-161543` | Yes (full 7 node run) |

The `_get_experiment_name()` function at `trigger.py:95-104` is supposed to produce one experiment per day (`protocol-processing-YYYYMMDD`), but experiments 12-16 have **timestamp suffixes** (`-162820`, `-162436`, etc.). This means something else (likely the API service's `main.py` or the verification script) is creating experiments with different names, causing pipeline traces to land in different experiments than what you're looking at in the UI.

### The real issue: experiment name mismatch between API service and pipeline

The API service (`main.py`) and the pipeline trigger (`trigger.py`) may be using different experiment naming. Let me verify.

> TOOL

tool_use Read
id: toolu_01JeSo4swdVtJigeWJC3mKTB
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/api-service/src/api_service/main.py",
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_01JeSo4swdVtJigeWJC3mKTB
```
     1→import asyncio
     2→import logging
     3→import os
     4→from contextlib import asynccontextmanager
     5→from typing import Set
     6→
     7→from dotenv import load_dotenv
     8→
     9→load_dotenv(override=False)
    10→
    11→from events_py.outbox import OutboxProcessor  # noqa: E402
    12→from fastapi import Depends, FastAPI, Request  # noqa: E402
    13→from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
    14→from fastapi.responses import FileResponse, JSONResponse  # noqa: E402
    15→from protocol_processor.trigger import (  # noqa: E402
    16→    _get_experiment_name,
    17→    handle_protocol_uploaded,
    18→)
    19→from sqlalchemy import create_engine as sa_create_engine  # noqa: E402
    20→from sqlalchemy import text  # noqa: E402
    21→from sqlmodel import Session  # noqa: E402
    22→from starlette.middleware.sessions import SessionMiddleware  # noqa: E402
    23→
    24→from api_service.auth import router as auth_router  # noqa: E402
    25→from api_service.batch_compare import router as batch_compare_router  # noqa: E402
    26→from api_service.criteria_table import router as criteria_table_router  # noqa: E402
    27→from api_service.criterion_rerun import router as criterion_rerun_router  # noqa: E402
    28→from api_service.dependencies import get_current_user, get_db  # noqa: E402
    29→from api_service.entities import router as entities_router  # noqa: E402
    30→from api_service.exports import router as exports_router  # noqa: E402
    31→from api_service.integrity import router as integrity_router  # noqa: E402
    32→from api_service.middleware import MLflowRequestMiddleware  # noqa: E402
    33→from api_service.protocols import router as protocols_router  # noqa: E402
    34→from api_service.reviews import router as reviews_router  # noqa: E402
    35→from api_service.search import router as search_router  # noqa: E402
    36→from api_service.storage import create_db_and_tables, engine  # noqa: E402
    37→from api_service.terminology_search import (  # noqa: E402
    38→    router as terminology_search_router,
    39→)
    40→
    41→# Setup basic logging
    42→logging.basicConfig(level=logging.INFO)
    43→logger = logging.getLogger(__name__)
    44→
    45→# Track running background tasks
    46→_running_tasks: Set[asyncio.Task] = set()  # noqa: UP006
    47→
    48→
    49→@asynccontextmanager
    50→async def lifespan(app: FastAPI):
    51→    """Manage the lifecycle of the FastAPI application."""
    52→    # Startup
    53→    logger.info("Starting up API service...")
    54→    logger.info("Initializing database...")
    55→    create_db_and_tables()
    56→    logger.info("Database initialized successfully")
    57→
    58→    # Initialize MLflow
    59→    try:
    60→        import mlflow
    61→
    62→        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    63→        if tracking_uri:
    64→            mlflow.set_tracking_uri(tracking_uri)
    65→            experiment_name = _get_experiment_name()
    66→            mlflow.set_experiment(experiment_name)
    67→            # NOTE: Do NOT enable mlflow.langchain.autolog() here.
    68→            # Autolog wraps graph.ainvoke() in a single trace that only
    69→            # appears after the full pipeline finishes.  Each pipeline
    70→            # node creates its own independent trace via pipeline_span()
    71→            # so traces stream to MLflow in real-time as nodes complete.
    72→            logger.info(
    73→                "MLflow initialized: tracking_uri=%s, experiment=%s",
    74→                tracking_uri,
    75→                experiment_name,
    76→            )
    77→        else:
    78→            logger.info("MLFLOW_TRACKING_URI not set, skipping MLflow initialization")
    79→    except ImportError:
    80→        logger.info("mlflow not installed, skipping initialization")
    81→    except Exception:
    82→        logger.warning(
    83→            "MLflow initialization failed, continuing without tracing",
    84→            exc_info=True,
    85→        )
    86→
    87→    # Start outbox processor as background task (skip in tests — the poll loop
    88→    # and executor shutdown add seconds of overhead per TestClient instantiation).
    89→    processor = None
    90→    if not os.environ.get("TESTING"):
```

> TOOL

tool_use Grep
id: toolu_01Y65epMoTXq2EMZAwXSiAL4
```json
{
  "pattern": "experiment_name|set_experiment",
  "path": "/Users/noahdolevelixir/Code/medgemma-hackathon/scripts",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01Y65epMoTXq2EMZAwXSiAL4
```
scripts/verify_mlflow_tracing.py:29:mlflow.set_experiment("trace-test")
scripts/verify_mlflow_tracing.py:128:    mlflow.set_experiment("trace-test")
```

> AGENT

OK, so the verification script uses its own experiment (`trace-test`). Now let me confirm the core issue — the timestamped experiments are being created by something other than `_get_experiment_name()`.

> TOOL

tool_use Grep
id: toolu_01UMqW4HnGbCEWUNwTQyj8Hi
```json
{
  "pattern": "protocol-processing-.*16",
  "path": "/Users/noahdolevelixir/Code/medgemma-hackathon",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01UMqW4HnGbCEWUNwTQyj8Hi
```
No matches found
```

> AGENT

The timestamped experiment names aren't in the code — they were created by earlier versions of the code before you changed `_get_experiment_name()` to date-only. Those are stale experiments from earlier runs today.

## Final Diagnosis

**Tracing IS working correctly.** Here's the proof:

### Experiment 17 (`protocol-processing-20260224`) — the latest run:

All **7 pipeline nodes** traced successfully with proper tags:
- `ingest_node` → `extract_node` → `parse_node` → `ground_node` → `persist_node` → `structure_node` → `ordinal_resolve_node`
- All tagged with `protocol_id=165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3`
- All have matching `run_id` for grouping
- All status = `OK`

Plus **60 HTTP request traces** from the middleware.

### If you're not seeing traces in the MLflow UI, check:

1. **You may be looking at the wrong experiment.** Experiments 12-16 are from earlier runs with timestamped names. The current traces are in experiment **17** (`protocol-processing-20260224`). In the MLflow UI, make sure you select this experiment.

2. **The UI may be filtering.** The MLflow Traces tab requires you to select the correct experiment from the left sidebar. The default view may show experiment 0 (Default) which has nothing.

3. **No traces are missing.** The full 7-node pipeline completed: ingest → extract → parse → ground → persist → structure → ordinal_resolve. All returned `OK`.

Would you like me to open the MLflow UI in a browser to verify what's displayed?

> DEVELOPER

use playwright to navigate the UI: http://localhost:5001/#/experiments/17/traces

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_navigate
id: toolu_011FnuqHFwCLgUYeR9VuH8Pw
```json
{
  "url": "http://localhost:5001/#/experiments/17/traces"
}
```

> TOOL

tool_result
id: toolu_011FnuqHFwCLgUYeR9VuH8Pw
```
### Ran Playwright code
```js
await page.goto('http://localhost:5001/#/experiments/17/traces');
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - generic [ref=e5]:
      - button "Toggle sidebar" [ref=e6] [cursor=pointer]:
        - img [ref=e7]:
          - img [ref=e8]
      - link "MLflow" [ref=e10] [cursor=pointer]:
        - /url: "#/"
        - img "MLflow" [ref=e11]
      - generic [ref=e21]: 3.9.0
    - generic [ref=e22]:
      - button "Switch to dark theme" [ref=e23] [cursor=pointer]:
        - img [ref=e24]
      - link "GitHub" [ref=e26] [cursor=pointer]:
        - /url: https://github.com/mlflow/mlflow
      - link "Docs" [ref=e27] [cursor=pointer]:
        - /url: https://www.mlflow.org/docs/latest/index.html
  - generic [ref=e28]:
    - main [ref=e31]:
      - generic [ref=e58]:
        - generic [ref=e60]: Loading...
        - generic [ref=e63]: Loading...
        - generic [ref=e66]: Loading...
        - generic [ref=e69]: Loading...
        - generic [ref=e72]: Loading...
        - generic [ref=e75]: Loading...
        - generic [ref=e78]: Loading...
        - generic [ref=e81]: Loading...
    - generic [ref=e85]:
      - generic [ref=e86]:
        - generic [ref=e87]:
          - img [ref=e88]:
            - img [ref=e89]
            - img [ref=e92]
          - text: MLflow Assistant
          - status [ref=e93]:
            - generic [ref=e95]: Beta
        - button "Close" [ref=e97] [cursor=pointer]:
          - img [ref=e98]:
            - img [ref=e99]
      - generic [ref=e101]:
        - generic [ref=e102]:
          - heading "Welcome to MLflow Assistant" [level=3] [ref=e104]
          - generic [ref=e105]:
            - generic [ref=e106]:
              - button "Previous slide" [ref=e107] [cursor=pointer]:
                - img [ref=e108]:
                  - img [ref=e109]
              - generic [ref=e112]:
                - generic [ref=e113]:
                  - img "Debug Issues"
                - generic [ref=e114]:
                  - img "Set Up Evaluations"
                - generic [ref=e115]:
                  - img "Analyze Trends"
                - generic [ref=e116]:
                  - img "Debug Issues"
              - button "Next slide" [ref=e117] [cursor=pointer]:
                - img [ref=e118]:
                  - img [ref=e119]
            - generic [ref=e121]:
              - generic [ref=e122]: 1. Debug Issues
              - text: Ask questions about errors, identify root causes, and get actionable fixes for failed traces.
          - generic [ref=e123]:
            - 'button "Go to slide 1: Debug Issues" [ref=e124] [cursor=pointer]'
            - 'button "Go to slide 2: Set Up Evaluations" [ref=e125] [cursor=pointer]'
            - 'button "Go to slide 3: Analyze Trends" [ref=e126] [cursor=pointer]'
        - button "Get Started" [ref=e127] [cursor=pointer]:
          - generic [ref=e128]: Get Started
```
```

> AGENT

The page is still loading. Let me wait for the content to appear.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_wait_for
id: toolu_01FxHhVkBF1F1LFXTFnDy5Ls
```json
{
  "time": 3
}
```

> TOOL

tool_result
id: toolu_01FxHhVkBF1F1LFXTFnDy5Ls
```
### Result
Waited for 3
### Ran Playwright code
```js
await new Promise(f => setTimeout(f, 3 * 1000));
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> main [ref=e31]:
  - generic [ref=e32]:
    - generic [ref=e130]:
      - generic [ref=e131]:
        - button [ref=e132] [cursor=pointer]:
          - img [ref=e133]:
            - img [ref=e134]
        - img [ref=e137]:
          - img [ref=e138]
        - heading "protocol-processing-20260224" [level=2] [ref=e141]
        - status [ref=e142]:
          - generic [ref=e144] [cursor=pointer]:
            - text: GenAI apps & agents
            - img [ref=e145]:
              - img [ref=e146]
        - button "Info" [ref=e149] [cursor=pointer]:
          - img "Info" [ref=e150]:
            - img [ref=e151]
      - generic [ref=e154]:
        - button "Open header dropdown menu" [ref=e155] [cursor=pointer]:
          - img [ref=e156]:
            - img [ref=e157]
        - button "Share" [ref=e159] [cursor=pointer]:
          - generic [ref=e160]: Share
        - link "View docs" [ref=e161] [cursor=pointer]:
          - /url: https://mlflow.org/docs/latest/genai/?rel=mlflow_ui
          - button "View docs" [ref=e162]:
            - img [ref=e163]:
              - img [ref=e164]
            - generic [ref=e167]: View docs
    - generic [ref=e47]:
      - generic [ref=e170]:
        - generic [ref=e171]:
          - link "Overview" [ref=e173] [cursor=pointer]:
            - /url: "#/experiments/17/overview"
            - generic [ref=e174]:
              - img [ref=e176]:
                - img [ref=e177]
              - generic [ref=e180]: Overview
          - generic [ref=e181]:
            - generic [ref=e183]: Observability
            - link "Traces" [ref=e184] [cursor=pointer]:
              - /url: "#/experiments/17/traces"
              - generic [ref=e185]:
                - img [ref=e187]:
                  - img [ref=e188]
                - generic [ref=e190]: Traces
            - link "Sessions" [ref=e191] [cursor=pointer]:
              - /url: "#/experiments/17/chat-sessions"
              - generic [ref=e192]:
                - img [ref=e194]:
                  - img [ref=e195]
                - generic [ref=e198]: Sessions
          - generic [ref=e199]:
            - generic [ref=e201]: Evaluation
            - link "Judges" [ref=e202] [cursor=pointer]:
              - /url: "#/experiments/17/judges"
              - generic [ref=e203]:
                - img [ref=e205]:
                  - img [ref=e206]
                - generic [ref=e208]: Judges
            - link "Datasets" [ref=e209] [cursor=pointer]:
              - /url: "#/experiments/17/datasets"
              - generic [ref=e210]:
                - img [ref=e212]:
                  - img [ref=e213]
                - generic [ref=e215]: Datasets
            - link "Evaluation runs" [ref=e216] [cursor=pointer]:
              - /url: "#/experiments/17/evaluation-runs"
              - generic [ref=e217]:
                - img [ref=e219]:
                  - img [ref=e220]
                - generic [ref=e223]: Evaluation runs
          - generic [ref=e224]:
            - generic [ref=e226]: Prompts & versions
            - link "Prompts" [ref=e227] [cursor=pointer]:
              - /url: "#/experiments/17/prompts"
              - generic [ref=e228]:
                - img [ref=e230]:
                  - img [ref=e231]
                - generic [ref=e233]: Prompts
            - link "Agent versions" [ref=e234] [cursor=pointer]:
              - /url: "#/experiments/17/models"
              - generic [ref=e235]:
                - img [ref=e237]:
                  - img [ref=e238]
                - generic [ref=e241]: Agent versions
        - button "Assistant" [pressed] [ref=e243] [cursor=pointer]:
          - img [ref=e245]:
            - img [ref=e246]
            - img [ref=e248]
          - generic [ref=e249]: Assistant
          - status [ref=e250]:
            - generic [ref=e252]: Beta
      - generic [ref=e254]:
        - generic [ref=e256]:
          - 'combobox "Time Range, selected option: Last 7 days" [ref=e258] [cursor=pointer]':
            - generic [ref=e259]:
              - generic [ref=e260]: "Time Range:"
              - generic [ref=e261]: Last 7 days
            - img [ref=e262]:
              - img [ref=e263]
          - button [ref=e265] [cursor=pointer]:
            - img [ref=e267]:
              - img [ref=e268]
        - generic [ref=e270]:
          - generic [ref=e271]:
            - generic [ref=e273]:
              - generic [ref=e275]:
                - img [ref=e277]:
                  - img [ref=e278]
                - textbox "Search traces by request" [ref=e281]
              - button "Filters" [ref=e283] [cursor=pointer]:
                - generic [ref=e284]:
                  - generic [ref=e285]:
                    - img [ref=e286]:
                      - img [ref=e287]
                    - text: Filters
                  - img [ref=e290]:
                    - img [ref=e291]
              - 'button "Sort: Request time" [ref=e293] [cursor=pointer]':
                - img [ref=e294]:
                  - img [ref=e295]
                - generic [ref=e297]:
                  - text: "Sort: Request time"
                  - img [ref=e299]:
                    - img [ref=e300]
              - button "Columns" [ref=e302] [cursor=pointer]:
                - generic [ref=e303]:
                  - generic [ref=e304]:
                    - img [ref=e305]:
                      - img [ref=e306]
                    - text: Columns
                  - img [ref=e309]:
                    - img [ref=e310]
              - button "Actions" [disabled] [ref=e313]:
                - generic:
                  - text: Actions
                  - generic:
                    - img:
                      - img
            - generic [ref=e315]: 67 of 67
          - table [ref=e323]:
            - row "Resize Column" [ref=e324]:
              - generic [ref=e325]:
                - columnheader
              - columnheader "Resize Column" [ref=e326]:
                - generic "[object Object]" [ref=e329]
                - button "Resize Column" [ref=e332]
            - row "Select all Trace ID Resize Column Request Resize Column Response Resize Column Execution time Resize Column Request time Resize Column State Resize Column" [ref=e334]:
              - columnheader "Select all" [ref=e336]:
                - checkbox "Select all" [ref=e340] [cursor=pointer]
              - columnheader "Trace ID Resize Column" [ref=e342]:
                - generic "Trace ID" [ref=e345]
                - button "Resize Column" [ref=e346]
              - columnheader "Request Resize Column" [ref=e348]:
                - generic "Request" [ref=e351]
                - button "Resize Column" [ref=e352]
              - columnheader "Response Resize Column" [ref=e354]:
                - generic "Response" [ref=e357]
                - button "Resize Column" [ref=e358]
              - columnheader "Execution time Resize Column" [ref=e360]:
                - generic "Execution time" [ref=e363]
                - button "Resize Column" [ref=e364]
              - columnheader "Request time Resize Column" [ref=e366]:
                - generic "Request time" [ref=e369]
                - button "Resize Column" [ref=e370]
              - columnheader "State Resize Column" [ref=e372]:
                - generic "State" [ref=e375]
                - button "Resize Column" [ref=e376]
              - img [ref=e380] [cursor=pointer]:
                - img [ref=e381]
            - generic [ref=e383]:
              - 'row "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" } {\"status_code\": 200, \"latency_ms\": 10.72} 0.01s 02/24/2026, 17:43:33 OK" [ref=e385]':
                - cell [ref=e387]:
                  - checkbox [ref=e391] [cursor=pointer]
                - cell [ref=e393]:
                  - status [ref=e396]:
                    - generic [ref=e399] [cursor=pointer]: tr-f1272edd03bf8a1be1a5ae453382f1d7
                - 'cell "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }" [ref=e400]':
                  - generic [ref=e403] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 10.72}" [ref=e404]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 10.72}" [ref=e407]'
                - cell "0.01s" [ref=e408]:
                  - generic "0.01s" [ref=e411]
                - cell "02/24/2026, 17:43:33" [ref=e412]:
                  - generic [ref=e415]: 02/24/2026, 17:43:33
                - cell "OK" [ref=e416]:
                  - generic [ref=e419]:
                    - img [ref=e420]:
                      - img [ref=e421]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" } {\"status_code\": 200, \"latency_ms\": 0.87} 0s 02/24/2026, 17:43:33 OK" [ref=e425]':
                - cell [ref=e427]:
                  - checkbox [ref=e431] [cursor=pointer]
                - cell [ref=e433]:
                  - status [ref=e436]:
                    - generic [ref=e439] [cursor=pointer]: tr-ce99a5da5c57600365ab1c3e02a672cb
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }" [ref=e440]':
                  - generic [ref=e443] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.87}" [ref=e444]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.87}" [ref=e447]'
                - cell "0s" [ref=e448]:
                  - generic "0s" [ref=e451]
                - cell "02/24/2026, 17:43:33" [ref=e452]:
                  - generic [ref=e455]: 02/24/2026, 17:43:33
                - cell "OK" [ref=e456]:
                  - generic [ref=e459]:
                    - img [ref=e460]:
                      - img [ref=e461]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 596.48} 0.596s 02/24/2026, 17:43:28 OK" [ref=e465]':
                - cell [ref=e467]:
                  - checkbox [ref=e471] [cursor=pointer]
                - cell [ref=e473]:
                  - status [ref=e476]:
                    - generic [ref=e479] [cursor=pointer]: tr-595f0b7f04bb092fd0649663c50125a6
                - 'cell "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e480]':
                  - generic [ref=e483] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 596.48}" [ref=e484]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 596.48}" [ref=e487]'
                - cell "0.596s" [ref=e488]:
                  - generic "0.596s" [ref=e491]
                - cell "02/24/2026, 17:43:28" [ref=e492]:
                  - generic [ref=e495]: 02/24/2026, 17:43:28
                - cell "OK" [ref=e496]:
                  - generic [ref=e499]:
                    - img [ref=e500]:
                      - img [ref=e501]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 594.0} 0.594s 02/24/2026, 17:43:28 OK" [ref=e505]':
                - cell [ref=e507]:
                  - checkbox [ref=e511] [cursor=pointer]
                - cell [ref=e513]:
                  - status [ref=e516]:
                    - generic [ref=e519] [cursor=pointer]: tr-ddd9d87038ed2af04d3dfb3df8e3563c
                - 'cell "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e520]':
                  - generic [ref=e523] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 594.0}" [ref=e524]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 594.0}" [ref=e527]'
                - cell "0.594s" [ref=e528]:
                  - generic "0.594s" [ref=e531]
                - cell "02/24/2026, 17:43:28" [ref=e532]:
                  - generic [ref=e535]: 02/24/2026, 17:43:28
                - cell "OK" [ref=e536]:
                  - generic [ref=e539]:
                    - img [ref=e540]:
                      - img [ref=e541]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 0.73} 0s 02/24/2026, 17:43:27 OK" [ref=e545]':
                - cell [ref=e547]:
                  - checkbox [ref=e551] [cursor=pointer]
                - cell [ref=e553]:
                  - status [ref=e556]:
                    - generic [ref=e559] [cursor=pointer]: tr-097c8fecefbdf521d71097762951d2f3
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e560]':
                  - generic [ref=e563] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.73}" [ref=e564]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.73}" [ref=e567]'
                - cell "0s" [ref=e568]:
                  - generic "0s" [ref=e571]
                - cell "02/24/2026, 17:43:27" [ref=e572]:
                  - generic [ref=e575]: 02/24/2026, 17:43:27
                - cell "OK" [ref=e576]:
                  - generic [ref=e579]:
                    - img [ref=e580]:
                      - img [ref=e581]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 6.27} 0.006s 02/24/2026, 17:43:27 OK" [ref=e585]':
                - cell [ref=e587]:
                  - checkbox [ref=e591] [cursor=pointer]
                - cell [ref=e593]:
                  - status [ref=e596]:
                    - generic [ref=e599] [cursor=pointer]: tr-eedb6dbf8e0a82123d7a87160f3efa38
                - 'cell "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" }" [ref=e600]':
                  - generic [ref=e603] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 6.27}" [ref=e604]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 6.27}" [ref=e607]'
                - cell "0.006s" [ref=e608]:
                  - generic "0.006s" [ref=e611]
                - cell "02/24/2026, 17:43:27" [ref=e612]:
                  - generic [ref=e615]: 02/24/2026, 17:43:27
                - cell "OK" [ref=e616]:
                  - generic [ref=e619]:
                    - img [ref=e620]:
                      - img [ref=e621]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 147.33} 0.147s 02/24/2026, 17:43:26 OK" [ref=e625]':
                - cell [ref=e627]:
                  - checkbox [ref=e631] [cursor=pointer]
                - cell [ref=e633]:
                  - status [ref=e636]:
                    - generic [ref=e639] [cursor=pointer]: tr-1ddf02e879d6b363d69134759479c796
                - 'cell "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" }" [ref=e640]':
                  - generic [ref=e643] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 147.33}" [ref=e644]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 147.33}" [ref=e647]'
                - cell "0.147s" [ref=e648]:
                  - generic "0.147s" [ref=e651]
                - cell "02/24/2026, 17:43:26" [ref=e652]:
                  - generic [ref=e655]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e656]:
                  - generic [ref=e659]:
                    - img [ref=e660]:
                      - img [ref=e661]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e665]':
                - cell [ref=e667]:
                  - checkbox [ref=e671] [cursor=pointer]
                - cell [ref=e673]:
                  - status [ref=e676]:
                    - generic [ref=e679] [cursor=pointer]: tr-7bfe853c0f3dc89dd6ed1eea9f7a5c77
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" }" [ref=e680]':
                  - generic [ref=e683] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e684]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e687]'
                - cell "0s" [ref=e688]:
                  - generic "0s" [ref=e691]
                - cell "02/24/2026, 17:43:26" [ref=e692]:
                  - generic [ref=e695]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e696]:
                  - generic [ref=e699]:
                    - img [ref=e700]:
                      - img [ref=e701]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" } {\"status_code\": 200, \"latency_ms\": 23.32} 0.023s 02/24/2026, 17:43:26 OK" [ref=e705]':
                - cell [ref=e707]:
                  - checkbox [ref=e711] [cursor=pointer]
                - cell [ref=e713]:
                  - status [ref=e716]:
                    - generic [ref=e719] [cursor=pointer]: tr-393c15c74e635d6e1cf14bb3a5340925
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }" [ref=e720]':
                  - generic [ref=e723] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 23.32}" [ref=e724]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 23.32}" [ref=e727]'
                - cell "0.023s" [ref=e728]:
                  - generic "0.023s" [ref=e731]
                - cell "02/24/2026, 17:43:26" [ref=e732]:
                  - generic [ref=e735]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e736]:
                  - generic [ref=e739]:
                    - img [ref=e740]:
                      - img [ref=e741]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" } {\"status_code\": 200, \"latency_ms\": 75.1} 0.075s 02/24/2026, 17:43:26 OK" [ref=e745]':
                - cell [ref=e747]:
                  - checkbox [ref=e751] [cursor=pointer]
                - cell [ref=e753]:
                  - status [ref=e756]:
                    - generic [ref=e759] [cursor=pointer]: tr-6926948dae5f2c50451ba7f87e960485
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }" [ref=e760]':
                  - generic [ref=e763] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 75.1}" [ref=e764]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 75.1}" [ref=e767]'
                - cell "0.075s" [ref=e768]:
                  - generic "0.075s" [ref=e771]
                - cell "02/24/2026, 17:43:26" [ref=e772]:
                  - generic [ref=e775]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e776]:
                  - generic [ref=e779]:
                    - img [ref=e780]:
                      - img [ref=e781]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" } {\"status_code\": 200, \"latency_ms\": 37.25} 0.037s 02/24/2026, 17:43:26 OK" [ref=e785]':
                - cell [ref=e787]:
                  - checkbox [ref=e791] [cursor=pointer]
                - cell [ref=e793]:
                  - status [ref=e796]:
                    - generic [ref=e799] [cursor=pointer]: tr-7056f0c4530ee0f019f2092917fae048
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }" [ref=e800]':
                  - generic [ref=e803] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 37.25}" [ref=e804]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 37.25}" [ref=e807]'
                - cell "0.037s" [ref=e808]:
                  - generic "0.037s" [ref=e811]
                - cell "02/24/2026, 17:43:26" [ref=e812]:
                  - generic [ref=e815]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e816]:
                  - generic [ref=e819]:
                    - img [ref=e820]:
                      - img [ref=e821]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" } {\"status_code\": 200, \"latency_ms\": 62.57} 0.062s 02/24/2026, 17:43:26 OK" [ref=e825]':
                - cell [ref=e827]:
                  - checkbox [ref=e831] [cursor=pointer]
                - cell [ref=e833]:
                  - status [ref=e836]:
                    - generic [ref=e839] [cursor=pointer]: tr-b02fba3dacf5246e8c13ab703d1c0b7a
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }" [ref=e840]':
                  - generic [ref=e843] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 62.57}" [ref=e844]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 62.57}" [ref=e847]'
                - cell "0.062s" [ref=e848]:
                  - generic "0.062s" [ref=e851]
                - cell "02/24/2026, 17:43:26" [ref=e852]:
                  - generic [ref=e855]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e856]:
                  - generic [ref=e859]:
                    - img [ref=e860]:
                      - img [ref=e861]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" } {\"status_code\": 200, \"latency_ms\": 50.01} 0.049s 02/24/2026, 17:43:26 OK" [ref=e865]':
                - cell [ref=e867]:
                  - checkbox [ref=e871] [cursor=pointer]
                - cell [ref=e873]:
                  - status [ref=e876]:
                    - generic [ref=e879] [cursor=pointer]: tr-64fd850fb97e6c312c9512f7f5f0da55
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }" [ref=e880]':
                  - generic [ref=e883] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 50.01}" [ref=e884]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 50.01}" [ref=e887]'
                - cell "0.049s" [ref=e888]:
                  - generic "0.049s" [ref=e891]
                - cell "02/24/2026, 17:43:26" [ref=e892]:
                  - generic [ref=e895]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e896]:
                  - generic [ref=e899]:
                    - img [ref=e900]:
                      - img [ref=e901]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e905]':
                - cell [ref=e907]:
                  - checkbox [ref=e911] [cursor=pointer]
                - cell [ref=e913]:
                  - status [ref=e916]:
                    - generic [ref=e919] [cursor=pointer]: tr-9ad043291f87bb26e847dca9612481f0
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }" [ref=e920]':
                  - generic [ref=e923] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e924]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e927]'
                - cell "0s" [ref=e928]:
                  - generic "0s" [ref=e931]
                - cell "02/24/2026, 17:43:26" [ref=e932]:
                  - generic [ref=e935]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e936]:
                  - generic [ref=e939]:
                    - img [ref=e940]:
                      - img [ref=e941]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e945]':
                - cell [ref=e947]:
                  - checkbox [ref=e951] [cursor=pointer]
                - cell [ref=e953]:
                  - status [ref=e956]:
                    - generic [ref=e959] [cursor=pointer]: tr-8d2f5fce9a2d5831ec52fcb90e464e3d
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }" [ref=e960]':
                  - generic [ref=e963] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e964]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e967]'
                - cell "0s" [ref=e968]:
                  - generic "0s" [ref=e971]
                - cell "02/24/2026, 17:43:26" [ref=e972]:
                  - generic [ref=e975]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e976]:
                  - generic [ref=e979]:
                    - img [ref=e980]:
                      - img [ref=e981]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" } {\"status_code\": 200, \"latency_ms\": 0.33} 0s 02/24/2026, 17:43:26 OK" [ref=e985]':
                - cell [ref=e987]:
                  - checkbox [ref=e991] [cursor=pointer]
                - cell [ref=e993]:
                  - status [ref=e996]:
                    - generic [ref=e999] [cursor=pointer]: tr-647eecac135b098c6a6ceed3652dd326
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }" [ref=e1000]':
                  - generic [ref=e1003] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.33}" [ref=e1004]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.33}" [ref=e1007]'
                - cell "0s" [ref=e1008]:
                  - generic "0s" [ref=e1011]
                - cell "02/24/2026, 17:43:26" [ref=e1012]:
                  - generic [ref=e1015]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1016]:
                  - generic [ref=e1019]:
                    - img [ref=e1020]:
                      - img [ref=e1021]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" } {\"status_code\": 200, \"latency_ms\": 0.27} 0s 02/24/2026, 17:43:26 OK" [ref=e1025]':
                - cell [ref=e1027]:
                  - checkbox [ref=e1031] [cursor=pointer]
                - cell [ref=e1033]:
                  - status [ref=e1036]:
                    - generic [ref=e1039] [cursor=pointer]: tr-c41531fa1eb97b32d9d8f6530ab27835
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }" [ref=e1040]':
                  - generic [ref=e1043] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.27}" [ref=e1044]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.27}" [ref=e1047]'
                - cell "0s" [ref=e1048]:
                  - generic "0s" [ref=e1051]
                - cell "02/24/2026, 17:43:26" [ref=e1052]:
                  - generic [ref=e1055]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1056]:
                  - generic [ref=e1059]:
                    - img [ref=e1060]:
                      - img [ref=e1061]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" } {\"status_code\": 200, \"latency_ms\": 0.3} 0s 02/24/2026, 17:43:26 OK" [ref=e1065]':
                - cell [ref=e1067]:
                  - checkbox [ref=e1071] [cursor=pointer]
                - cell [ref=e1073]:
                  - status [ref=e1076]:
                    - generic [ref=e1079] [cursor=pointer]: tr-3a92fcbd6cd9aebbe1eef6e94655592f
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }" [ref=e1080]':
                  - generic [ref=e1083] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.3}" [ref=e1084]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.3}" [ref=e1087]'
                - cell "0s" [ref=e1088]:
                  - generic "0s" [ref=e1091]
                - cell "02/24/2026, 17:43:26" [ref=e1092]:
                  - generic [ref=e1095]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1096]:
                  - generic [ref=e1099]:
                    - img [ref=e1100]:
                      - img [ref=e1101]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" } {\"status_code\": 200, \"latency_ms\": 8.82} 0.008s 02/24/2026, 17:43:26 OK" [ref=e1105]':
                - cell [ref=e1107]:
                  - checkbox [ref=e1111] [cursor=pointer]
                - cell [ref=e1113]:
                  - status [ref=e1116]:
                    - generic [ref=e1119] [cursor=pointer]: tr-e0f11a6055448ae18adb7d31b1a736e1
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }" [ref=e1120]':
                  - generic [ref=e1123] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 8.82}" [ref=e1124]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 8.82}" [ref=e1127]'
                - cell "0.008s" [ref=e1128]:
                  - generic "0.008s" [ref=e1131]
                - cell "02/24/2026, 17:43:26" [ref=e1132]:
                  - generic [ref=e1135]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1136]:
                  - generic [ref=e1139]:
                    - img [ref=e1140]:
                      - img [ref=e1141]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" } {\"status_code\": 200, \"latency_ms\": 120.96} 0.12s 02/24/2026, 17:43:26 OK" [ref=e1145]':
                - cell [ref=e1147]:
                  - checkbox [ref=e1151] [cursor=pointer]
                - cell [ref=e1153]:
                  - status [ref=e1156]:
                    - generic [ref=e1159] [cursor=pointer]: tr-569dd4160866b91f78284dad4db0ab2d
                - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" }" [ref=e1160]':
                  - generic [ref=e1163] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 120.96}" [ref=e1164]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 120.96}" [ref=e1167]'
                - cell "0.12s" [ref=e1168]:
                  - generic "0.12s" [ref=e1171]
                - cell "02/24/2026, 17:43:26" [ref=e1172]:
                  - generic [ref=e1175]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1176]:
                  - generic [ref=e1179]:
                    - img [ref=e1180]:
                      - img [ref=e1181]
                    - text: OK
              - 'row "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 108.07} 0.108s 02/24/2026, 17:43:26 OK" [ref=e1185]':
                - cell [ref=e1187]:
                  - checkbox [ref=e1191] [cursor=pointer]
                - cell [ref=e1193]:
                  - status [ref=e1196]:
                    - generic [ref=e1199] [cursor=pointer]: tr-ffc510e366ed2b438d52af55cd48b7c1
                - 'cell "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" }" [ref=e1200]':
                  - generic [ref=e1203] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 108.07}" [ref=e1204]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 108.07}" [ref=e1207]'
                - cell "0.108s" [ref=e1208]:
                  - generic "0.108s" [ref=e1211]
                - cell "02/24/2026, 17:43:26" [ref=e1212]:
                  - generic [ref=e1215]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1216]:
                  - generic [ref=e1219]:
                    - img [ref=e1220]:
                      - img [ref=e1221]
                    - text: OK
              - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e1225]':
                - cell [ref=e1227]:
                  - checkbox [ref=e1231] [cursor=pointer]
                - cell [ref=e1233]:
                  - status [ref=e1236]:
                    - generic [ref=e1239] [cursor=pointer]: tr-6f6eab2b9f42d561b0b41f10c0daae3f
                - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }" [ref=e1240]':
                  - generic [ref=e1243] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }"
                - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1244]':
                  - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1247]'
                - cell "0s" [ref=e1248]:
                  - generic "0s" [ref=e1251]
                - cell "02/24/2026, 17:43:26" [ref=e1252]:
                  - generic [ref=e1255]: 02/24/2026, 17:43:26
                - cell "OK" [ref=e1256]:
                  - generic [ref=e1259]:
                    - img [ref=e1260]:
                      - img [ref=e1261]
                    - text: OK
- <changed> generic [ref=e112]:
  - img "Debug Issues" [ref=e1264]
  - img "Set Up Evaluations" [ref=e1265]
  - img "Analyze Trends" [ref=e1266]
  - img "Debug Issues" [ref=e1267]
```
```

> AGENT

I can see the traces page loaded. It shows **67 of 67 traces**, but they're all HTTP middleware traces (GET, OPTIONS, POST requests). The pipeline node traces are mixed in. Let me take a screenshot to show you what it looks like, and then scroll down to find the pipeline traces.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_take_screenshot
id: toolu_01RZgrSSpcaTXg8hLWq3TT2m
```json
{
  "type": "png",
  "filename": "mlflow-traces-page.png"
}
```

> TOOL

tool_result
id: toolu_01RZgrSSpcaTXg8hLWq3TT2m
```
### Result
- [Screenshot of viewport](mlflow-traces-page.png)
### Ran Playwright code
```js
// Screenshot viewport and save it as mlflow-traces-page.png
await page.screenshot({
path: 'mlflow-traces-page.png',
  scale: 'css',
  type: 'png'
});
```
{
  "type": "image",
  "source": {
    "data": "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",
    "media_type": "image/png",
    "type": "base64"
  }
}
```

> AGENT

Now I can see the issue clearly. The traces page shows **67 of 67** traces, but they're sorted by request time (newest first), so all you see are HTTP middleware traces from the API. The 7 pipeline node traces are buried further down in the list. Let me scroll down to find them, or better yet, let me use the search/filter to find the pipeline traces specifically.

Let me search for pipeline node traces using the search box.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01UGkUJbWF1CsYD1cHcrSGyd
```json
{
  "element": "Search traces textbox",
  "ref": "e281"
}
```

> TOOL

tool_result
id: toolu_01UGkUJbWF1CsYD1cHcrSGyd
```
### Ran Playwright code
```js
await page.getByRole('textbox', { name: 'Search traces by request' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> textbox "Search traces by request" [active] [ref=e281]
```
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_type
id: toolu_01FHpxD4m454VoLogJTDHwvV
```json
{
  "ref": "e281",
  "text": "ingest_node",
  "submit": true
}
```

> TOOL

tool_result
id: toolu_01FHpxD4m454VoLogJTDHwvV
```
### Ran Playwright code
```js
await page.getByRole('textbox', { name: 'Search traces by request' }).fill('ingest_node');
await page.getByRole('textbox', { name: 'Search traces by request' }).press('Enter');
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> generic [ref=e270]:
  - generic [ref=e271]:
    - generic [ref=e273]:
      - generic [ref=e275]:
        - ref=e277 [unchanged]
        - textbox "Search traces by request" [active] [ref=e281]: ingest_node
        - button "close-circle" [ref=e1268] [cursor=pointer]:
          - img [ref=e1269]
      - ref=e283 [unchanged]
      - ref=e293 [unchanged]
      - ref=e302 [unchanged]
      - ref=e313 [unchanged]
    - generic [ref=e1272]: 0 of 67
  - table [ref=e1278]:
    - row "Resize Column" [ref=e1279]:
      - generic [ref=e1280]:
        - columnheader
      - columnheader "Resize Column" [ref=e1281]:
        - generic "[object Object]" [ref=e1284]
        - button "Resize Column" [ref=e1287]
    - row "Select all Trace ID Resize Column Request Resize Column Response Resize Column Execution time Resize Column Request time Resize Column State Resize Column" [ref=e1289]:
      - columnheader "Select all" [ref=e1291]:
        - checkbox "Select all" [ref=e1295] [cursor=pointer]
      - columnheader "Trace ID Resize Column" [ref=e1297]:
        - generic "Trace ID" [ref=e1300]
        - button "Resize Column" [ref=e1301]
      - columnheader "Request Resize Column" [ref=e1303]:
        - generic "Request" [ref=e1306]
        - button "Resize Column" [ref=e1307]
      - columnheader "Response Resize Column" [ref=e1309]:
        - generic "Response" [ref=e1312]
        - button "Resize Column" [ref=e1313]
      - columnheader "Execution time Resize Column" [ref=e1315]:
        - generic "Execution time" [ref=e1318]
        - button "Resize Column" [ref=e1319]
      - columnheader "Request time Resize Column" [ref=e1321]:
        - generic "Request time" [ref=e1324]
        - button "Resize Column" [ref=e1325]
      - columnheader "State Resize Column" [ref=e1327]:
        - generic "State" [ref=e1330]
        - button "Resize Column" [ref=e1331]
      - img [ref=e1335] [cursor=pointer]:
        - img [ref=e1336]
    - generic [ref=e1340]:
      - img [ref=e1341]:
        - img [ref=e1342]
      - generic [ref=e1345]: No traces found. Try clearing your active filters to see more traces.
```
```

> AGENT

Interesting — **0 of 67** results for "ingest_node". The search only filters by the Request column (which contains HTTP method/path JSON), not by trace name/tags. The pipeline traces have their inputs in the Request column, not the node name. Let me clear the search and use Filters instead.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_012pzdj1jF3KyZTmayuoGASz
```json
{
  "element": "Clear search",
  "ref": "e1268"
}
```

> TOOL

tool_result
id: toolu_012pzdj1jF3KyZTmayuoGASz
```
### Ran Playwright code
```js
await page.getByRole('button', { name: 'close-circle' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> generic [ref=e275]:
  - ref=e277 [unchanged]
  - textbox "Search traces by request" [active] [ref=e281]
- <changed> generic [ref=e1272]: 67 of 67
- <changed> table [ref=e1278]:
  - ref=e1279 [unchanged]
  - ref=e1289 [unchanged]
  - generic [ref=e1346]:
    - 'row "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" } {\"status_code\": 200, \"latency_ms\": 10.72} 0.01s 02/24/2026, 17:43:33 OK" [ref=e1348]':
      - cell [ref=e1350]:
        - checkbox [ref=e1354] [cursor=pointer]
      - cell [ref=e1356]:
        - status [ref=e1359]:
          - generic [ref=e1362] [cursor=pointer]: tr-f1272edd03bf8a1be1a5ae453382f1d7
      - 'cell "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }" [ref=e1363]':
        - generic [ref=e1366] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 10.72}" [ref=e1367]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 10.72}" [ref=e1370]'
      - cell "0.01s" [ref=e1371]:
        - generic "0.01s" [ref=e1374]
      - cell "02/24/2026, 17:43:33" [ref=e1375]:
        - generic [ref=e1378]: 02/24/2026, 17:43:33
      - cell "OK" [ref=e1379]:
        - generic [ref=e1382]:
          - img [ref=e1383]:
            - img [ref=e1384]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" } {\"status_code\": 200, \"latency_ms\": 0.87} 0s 02/24/2026, 17:43:33 OK" [ref=e1388]':
      - cell [ref=e1390]:
        - checkbox [ref=e1394] [cursor=pointer]
      - cell [ref=e1396]:
        - status [ref=e1399]:
          - generic [ref=e1402] [cursor=pointer]: tr-ce99a5da5c57600365ab1c3e02a672cb
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }" [ref=e1403]':
        - generic [ref=e1406] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/criteria/structured\", \"query\": \"page=1&page_size=50&sort_by=confidence&sort_order=desc\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.87}" [ref=e1407]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.87}" [ref=e1410]'
      - cell "0s" [ref=e1411]:
        - generic "0s" [ref=e1414]
      - cell "02/24/2026, 17:43:33" [ref=e1415]:
        - generic [ref=e1418]: 02/24/2026, 17:43:33
      - cell "OK" [ref=e1419]:
        - generic [ref=e1422]:
          - img [ref=e1423]:
            - img [ref=e1424]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 596.48} 0.596s 02/24/2026, 17:43:28 OK" [ref=e1428]':
      - cell [ref=e1430]:
        - checkbox [ref=e1434] [cursor=pointer]
      - cell [ref=e1436]:
        - status [ref=e1439]:
          - generic [ref=e1442] [cursor=pointer]: tr-595f0b7f04bb092fd0649663c50125a6
      - 'cell "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e1443]':
        - generic [ref=e1446] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 596.48}" [ref=e1447]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 596.48}" [ref=e1450]'
      - cell "0.596s" [ref=e1451]:
        - generic "0.596s" [ref=e1454]
      - cell "02/24/2026, 17:43:28" [ref=e1455]:
        - generic [ref=e1458]: 02/24/2026, 17:43:28
      - cell "OK" [ref=e1459]:
        - generic [ref=e1462]:
          - img [ref=e1463]:
            - img [ref=e1464]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 594.0} 0.594s 02/24/2026, 17:43:28 OK" [ref=e1468]':
      - cell [ref=e1470]:
        - checkbox [ref=e1474] [cursor=pointer]
      - cell [ref=e1476]:
        - status [ref=e1479]:
          - generic [ref=e1482] [cursor=pointer]: tr-ddd9d87038ed2af04d3dfb3df8e3563c
      - 'cell "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e1483]':
        - generic [ref=e1486] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 594.0}" [ref=e1487]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 594.0}" [ref=e1490]'
      - cell "0.594s" [ref=e1491]:
        - generic "0.594s" [ref=e1494]
      - cell "02/24/2026, 17:43:28" [ref=e1495]:
        - generic [ref=e1498]: 02/24/2026, 17:43:28
      - cell "OK" [ref=e1499]:
        - generic [ref=e1502]:
          - img [ref=e1503]:
            - img [ref=e1504]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" } {\"status_code\": 200, \"latency_ms\": 0.73} 0s 02/24/2026, 17:43:27 OK" [ref=e1508]':
      - cell [ref=e1510]:
        - checkbox [ref=e1514] [cursor=pointer]
      - cell [ref=e1516]:
        - status [ref=e1519]:
          - generic [ref=e1522] [cursor=pointer]: tr-097c8fecefbdf521d71097762951d2f3
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }" [ref=e1523]':
        - generic [ref=e1526] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/api/terminology/umls/search\", \"query\": \"q=Written%20informed%20consent\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.73}" [ref=e1527]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.73}" [ref=e1530]'
      - cell "0s" [ref=e1531]:
        - generic "0s" [ref=e1534]
      - cell "02/24/2026, 17:43:27" [ref=e1535]:
        - generic [ref=e1538]: 02/24/2026, 17:43:27
      - cell "OK" [ref=e1539]:
        - generic [ref=e1542]:
          - img [ref=e1543]:
            - img [ref=e1544]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 6.27} 0.006s 02/24/2026, 17:43:27 OK" [ref=e1548]':
      - cell [ref=e1550]:
        - checkbox [ref=e1554] [cursor=pointer]
      - cell [ref=e1556]:
        - status [ref=e1559]:
          - generic [ref=e1562] [cursor=pointer]: tr-eedb6dbf8e0a82123d7a87160f3efa38
      - 'cell "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" }" [ref=e1563]':
        - generic [ref=e1566] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/local-files/76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\", \"query\": \"\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 6.27}" [ref=e1567]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 6.27}" [ref=e1570]'
      - cell "0.006s" [ref=e1571]:
        - generic "0.006s" [ref=e1574]
      - cell "02/24/2026, 17:43:27" [ref=e1575]:
        - generic [ref=e1578]: 02/24/2026, 17:43:27
      - cell "OK" [ref=e1579]:
        - generic [ref=e1582]:
          - img [ref=e1583]:
            - img [ref=e1584]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 147.33} 0.147s 02/24/2026, 17:43:26 OK" [ref=e1588]':
      - cell [ref=e1590]:
        - checkbox [ref=e1594] [cursor=pointer]
      - cell [ref=e1596]:
        - status [ref=e1599]:
          - generic [ref=e1602] [cursor=pointer]: tr-1ddf02e879d6b363d69134759479c796
      - 'cell "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" }" [ref=e1603]':
        - generic [ref=e1606] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"REDACTED\", \"query\": \"\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 147.33}" [ref=e1607]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 147.33}" [ref=e1610]'
      - cell "0.147s" [ref=e1611]:
        - generic "0.147s" [ref=e1614]
      - cell "02/24/2026, 17:43:26" [ref=e1615]:
        - generic [ref=e1618]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1619]:
        - generic [ref=e1622]:
          - img [ref=e1623]:
            - img [ref=e1624]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e1628]':
      - cell [ref=e1630]:
        - checkbox [ref=e1634] [cursor=pointer]
      - cell [ref=e1636]:
        - status [ref=e1639]:
          - generic [ref=e1642] [cursor=pointer]: tr-7bfe853c0f3dc89dd6ed1eea9f7a5c77
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" }" [ref=e1643]':
        - generic [ref=e1646] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"REDACTED\", \"query\": \"\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1647]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1650]'
      - cell "0s" [ref=e1651]:
        - generic "0s" [ref=e1654]
      - cell "02/24/2026, 17:43:26" [ref=e1655]:
        - generic [ref=e1658]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1659]:
        - generic [ref=e1662]:
          - img [ref=e1663]:
            - img [ref=e1664]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" } {\"status_code\": 200, \"latency_ms\": 23.32} 0.023s 02/24/2026, 17:43:26 OK" [ref=e1668]':
      - cell [ref=e1670]:
        - checkbox [ref=e1674] [cursor=pointer]
      - cell [ref=e1676]:
        - status [ref=e1679]:
          - generic [ref=e1682] [cursor=pointer]: tr-393c15c74e635d6e1cf14bb3a5340925
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }" [ref=e1683]':
        - generic [ref=e1686] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 23.32}" [ref=e1687]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 23.32}" [ref=e1690]'
      - cell "0.023s" [ref=e1691]:
        - generic "0.023s" [ref=e1694]
      - cell "02/24/2026, 17:43:26" [ref=e1695]:
        - generic [ref=e1698]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1699]:
        - generic [ref=e1702]:
          - img [ref=e1703]:
            - img [ref=e1704]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" } {\"status_code\": 200, \"latency_ms\": 75.1} 0.075s 02/24/2026, 17:43:26 OK" [ref=e1708]':
      - cell [ref=e1710]:
        - checkbox [ref=e1714] [cursor=pointer]
      - cell [ref=e1716]:
        - status [ref=e1719]:
          - generic [ref=e1722] [cursor=pointer]: tr-6926948dae5f2c50451ba7f87e960485
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }" [ref=e1723]':
        - generic [ref=e1726] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 75.1}" [ref=e1727]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 75.1}" [ref=e1730]'
      - cell "0.075s" [ref=e1731]:
        - generic "0.075s" [ref=e1734]
      - cell "02/24/2026, 17:43:26" [ref=e1735]:
        - generic [ref=e1738]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1739]:
        - generic [ref=e1742]:
          - img [ref=e1743]:
            - img [ref=e1744]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" } {\"status_code\": 200, \"latency_ms\": 37.25} 0.037s 02/24/2026, 17:43:26 OK" [ref=e1748]':
      - cell [ref=e1750]:
        - checkbox [ref=e1754] [cursor=pointer]
      - cell [ref=e1756]:
        - status [ref=e1759]:
          - generic [ref=e1762] [cursor=pointer]: tr-7056f0c4530ee0f019f2092917fae048
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }" [ref=e1763]':
        - generic [ref=e1766] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 37.25}" [ref=e1767]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 37.25}" [ref=e1770]'
      - cell "0.037s" [ref=e1771]:
        - generic "0.037s" [ref=e1774]
      - cell "02/24/2026, 17:43:26" [ref=e1775]:
        - generic [ref=e1778]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1779]:
        - generic [ref=e1782]:
          - img [ref=e1783]:
            - img [ref=e1784]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" } {\"status_code\": 200, \"latency_ms\": 62.57} 0.062s 02/24/2026, 17:43:26 OK" [ref=e1788]':
      - cell [ref=e1790]:
        - checkbox [ref=e1794] [cursor=pointer]
      - cell [ref=e1796]:
        - status [ref=e1799]:
          - generic [ref=e1802] [cursor=pointer]: tr-b02fba3dacf5246e8c13ab703d1c0b7a
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }" [ref=e1803]':
        - generic [ref=e1806] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 62.57}" [ref=e1807]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 62.57}" [ref=e1810]'
      - cell "0.062s" [ref=e1811]:
        - generic "0.062s" [ref=e1814]
      - cell "02/24/2026, 17:43:26" [ref=e1815]:
        - generic [ref=e1818]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1819]:
        - generic [ref=e1822]:
          - img [ref=e1823]:
            - img [ref=e1824]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" } {\"status_code\": 200, \"latency_ms\": 50.01} 0.049s 02/24/2026, 17:43:26 OK" [ref=e1828]':
      - cell [ref=e1830]:
        - checkbox [ref=e1834] [cursor=pointer]
      - cell [ref=e1836]:
        - status [ref=e1839]:
          - generic [ref=e1842] [cursor=pointer]: tr-64fd850fb97e6c312c9512f7f5f0da55
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }" [ref=e1843]':
        - generic [ref=e1846] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 50.01}" [ref=e1847]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 50.01}" [ref=e1850]'
      - cell "0.049s" [ref=e1851]:
        - generic "0.049s" [ref=e1854]
      - cell "02/24/2026, 17:43:26" [ref=e1855]:
        - generic [ref=e1858]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1859]:
        - generic [ref=e1862]:
          - img [ref=e1863]:
            - img [ref=e1864]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e1868]':
      - cell [ref=e1870]:
        - checkbox [ref=e1874] [cursor=pointer]
      - cell [ref=e1876]:
        - status [ref=e1879]:
          - generic [ref=e1882] [cursor=pointer]: tr-9ad043291f87bb26e847dca9612481f0
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }" [ref=e1883]':
        - generic [ref=e1886] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e9e53ef-7ff4-4b95-8bcc-db076e3624a3\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1887]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1890]'
      - cell "0s" [ref=e1891]:
        - generic "0s" [ref=e1894]
      - cell "02/24/2026, 17:43:26" [ref=e1895]:
        - generic [ref=e1898]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1899]:
        - generic [ref=e1902]:
          - img [ref=e1903]:
            - img [ref=e1904]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e1908]':
      - cell [ref=e1910]:
        - checkbox [ref=e1914] [cursor=pointer]
      - cell [ref=e1916]:
        - status [ref=e1919]:
          - generic [ref=e1922] [cursor=pointer]: tr-8d2f5fce9a2d5831ec52fcb90e464e3d
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }" [ref=e1923]':
        - generic [ref=e1926] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=f16412f0-cfe3-446d-bfd3-3d1a405ca962\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1927]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e1930]'
      - cell "0s" [ref=e1931]:
        - generic "0s" [ref=e1934]
      - cell "02/24/2026, 17:43:26" [ref=e1935]:
        - generic [ref=e1938]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1939]:
        - generic [ref=e1942]:
          - img [ref=e1943]:
            - img [ref=e1944]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" } {\"status_code\": 200, \"latency_ms\": 0.33} 0s 02/24/2026, 17:43:26 OK" [ref=e1948]':
      - cell [ref=e1950]:
        - checkbox [ref=e1954] [cursor=pointer]
      - cell [ref=e1956]:
        - status [ref=e1959]:
          - generic [ref=e1962] [cursor=pointer]: tr-647eecac135b098c6a6ceed3652dd326
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }" [ref=e1963]':
        - generic [ref=e1966] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=edefe813-2cd7-4bfc-ad3e-0968a8983811\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.33}" [ref=e1967]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.33}" [ref=e1970]'
      - cell "0s" [ref=e1971]:
        - generic "0s" [ref=e1974]
      - cell "02/24/2026, 17:43:26" [ref=e1975]:
        - generic [ref=e1978]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e1979]:
        - generic [ref=e1982]:
          - img [ref=e1983]:
            - img [ref=e1984]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" } {\"status_code\": 200, \"latency_ms\": 0.27} 0s 02/24/2026, 17:43:26 OK" [ref=e1988]':
      - cell [ref=e1990]:
        - checkbox [ref=e1994] [cursor=pointer]
      - cell [ref=e1996]:
        - status [ref=e1999]:
          - generic [ref=e2002] [cursor=pointer]: tr-c41531fa1eb97b32d9d8f6530ab27835
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }" [ref=e2003]':
        - generic [ref=e2006] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=b59268bb-13b0-4c7f-a20e-96cd941b2bee\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.27}" [ref=e2007]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.27}" [ref=e2010]'
      - cell "0s" [ref=e2011]:
        - generic "0s" [ref=e2014]
      - cell "02/24/2026, 17:43:26" [ref=e2015]:
        - generic [ref=e2018]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2019]:
        - generic [ref=e2022]:
          - img [ref=e2023]:
            - img [ref=e2024]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" } {\"status_code\": 200, \"latency_ms\": 0.3} 0s 02/24/2026, 17:43:26 OK" [ref=e2028]':
      - cell [ref=e2030]:
        - checkbox [ref=e2034] [cursor=pointer]
      - cell [ref=e2036]:
        - status [ref=e2039]:
          - generic [ref=e2042] [cursor=pointer]: tr-3a92fcbd6cd9aebbe1eef6e94655592f
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }" [ref=e2043]':
        - generic [ref=e2046] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria&target_id=0e887a8d-9c66-4ce9-bad3-9c00c18553f4\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.3}" [ref=e2047]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.3}" [ref=e2050]'
      - cell "0s" [ref=e2051]:
        - generic "0s" [ref=e2054]
      - cell "02/24/2026, 17:43:26" [ref=e2055]:
        - generic [ref=e2058]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2059]:
        - generic [ref=e2062]:
          - img [ref=e2063]:
            - img [ref=e2064]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" } {\"status_code\": 200, \"latency_ms\": 8.82} 0.008s 02/24/2026, 17:43:26 OK" [ref=e2068]':
      - cell [ref=e2070]:
        - checkbox [ref=e2074] [cursor=pointer]
      - cell [ref=e2076]:
        - status [ref=e2079]:
          - generic [ref=e2082] [cursor=pointer]: tr-e0f11a6055448ae18adb7d31b1a736e1
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }" [ref=e2083]':
        - generic [ref=e2086] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 8.82}" [ref=e2087]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 8.82}" [ref=e2090]'
      - cell "0.008s" [ref=e2091]:
        - generic "0.008s" [ref=e2094]
      - cell "02/24/2026, 17:43:26" [ref=e2095]:
        - generic [ref=e2098]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2099]:
        - generic [ref=e2102]:
          - img [ref=e2103]:
            - img [ref=e2104]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" } {\"status_code\": 200, \"latency_ms\": 120.96} 0.12s 02/24/2026, 17:43:26 OK" [ref=e2108]':
      - cell [ref=e2110]:
        - checkbox [ref=e2114] [cursor=pointer]
      - cell [ref=e2116]:
        - status [ref=e2119]:
          - generic [ref=e2122] [cursor=pointer]: tr-569dd4160866b91f78284dad4db0ab2d
      - 'cell "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" }" [ref=e2123]':
        - generic [ref=e2126] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/reviews/batches\", \"query\": \"page=1&page_size=100\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 120.96}" [ref=e2127]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 120.96}" [ref=e2130]'
      - cell "0.12s" [ref=e2131]:
        - generic "0.12s" [ref=e2134]
      - cell "02/24/2026, 17:43:26" [ref=e2135]:
        - generic [ref=e2138]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2139]:
        - generic [ref=e2142]:
          - img [ref=e2143]:
            - img [ref=e2144]
          - text: OK
    - 'row "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" } {\"status_code\": 200, \"latency_ms\": 108.07} 0.108s 02/24/2026, 17:43:26 OK" [ref=e2148]':
      - cell [ref=e2150]:
        - checkbox [ref=e2154] [cursor=pointer]
      - cell [ref=e2156]:
        - status [ref=e2159]:
          - generic [ref=e2162] [cursor=pointer]: tr-ffc510e366ed2b438d52af55cd48b7c1
      - 'cell "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" }" [ref=e2163]':
        - generic [ref=e2166] [cursor=pointer]: "{ \"method\": \"GET\", \"path\": \"/entities/batch/0b03d48a-4987-4085-b8a0-56046216778a\", \"query\": \"\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 108.07}" [ref=e2167]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 108.07}" [ref=e2170]'
      - cell "0.108s" [ref=e2171]:
        - generic "0.108s" [ref=e2174]
      - cell "02/24/2026, 17:43:26" [ref=e2175]:
        - generic [ref=e2178]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2179]:
        - generic [ref=e2182]:
          - img [ref=e2183]:
            - img [ref=e2184]
          - text: OK
    - 'row "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" } {\"status_code\": 200, \"latency_ms\": 0.26} 0s 02/24/2026, 17:43:26 OK" [ref=e2188]':
      - cell [ref=e2190]:
        - checkbox [ref=e2194] [cursor=pointer]
      - cell [ref=e2196]:
        - status [ref=e2199]:
          - generic [ref=e2202] [cursor=pointer]: tr-6f6eab2b9f42d561b0b41f10c0daae3f
      - 'cell "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }" [ref=e2203]':
        - generic [ref=e2206] [cursor=pointer]: "{ \"method\": \"OPTIONS\", \"path\": \"/reviews/audit-log\", \"query\": \"page=1&page_size=20&target_type=criteria\" }"
      - 'cell "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e2207]':
        - 'generic "{\"status_code\": 200, \"latency_ms\": 0.26}" [ref=e2210]'
      - cell "0s" [ref=e2211]:
        - generic "0s" [ref=e2214]
      - cell "02/24/2026, 17:43:26" [ref=e2215]:
        - generic [ref=e2218]: 02/24/2026, 17:43:26
      - cell "OK" [ref=e2219]:
        - generic [ref=e2222]:
          - img [ref=e2223]:
            - img [ref=e2224]
          - text: OK
```
```

> AGENT

The visible traces are all HTTP middleware. The pipeline node traces are further down the list. Let me use the Filters to isolate them.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01KjwvAxwFZGwDrZLu4h8xxn
```json
{
  "element": "Filters button",
  "ref": "e283"
}
```

> TOOL

tool_result
id: toolu_01KjwvAxwFZGwDrZLu4h8xxn
```
### Ran Playwright code
```js
await page.getByRole('button', { name: 'Filters' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> generic [ref=e1]:
  - generic [ref=e3]:
    - ref=e4 [unchanged]
    - generic [ref=e28]:
      - main [ref=e31]:
        - generic [ref=e32]:
          - ref=e130 [unchanged]
          - generic [ref=e47]:
            - ref=e170 [unchanged]
            - generic [ref=e254]:
              - ref=e256 [unchanged]
              - generic [ref=e270]:
                - generic [ref=e271]:
                  - generic [ref=e273]:
                    - generic [ref=e275]:
                      - ref=e277 [unchanged]
                      - textbox "Search traces by request" [ref=e281]
                    - button "Filters" [expanded] [ref=e283] [cursor=pointer]:
                      - ref=e284 [unchanged]
                    - ref=e293 [unchanged]
                    - ref=e302 [unchanged]
                    - ref=e313 [unchanged]
                  - ref=e1272 [unchanged]
                - ref=e1278 [unchanged]
      - ref=e85 [unchanged]
  - dialog "Popover content" [ref=e2228]:
    - generic [ref=e2229]:
      - generic [ref=e2231]:
        - generic [ref=e2232]:
          - generic [ref=e2234]: Field
          - combobox "Field" [active] [ref=e2236] [cursor=pointer]:
            - generic [ref=e2238]: Select column
            - img [ref=e2239]:
              - img [ref=e2240]
        - generic [ref=e2242]:
          - generic [ref=e2244]: Operator
          - combobox "Operator" [ref=e2246] [cursor=pointer]:
            - generic [ref=e2247]: =
            - img [ref=e2248]:
              - img [ref=e2249]
        - generic [ref=e2251]:
          - generic [ref=e2253]: Value
          - textbox "Value" [ref=e2254]
        - button [ref=e2256] [cursor=pointer]:
          - img [ref=e2257]:
            - img [ref=e2258]
      - button "Add filter" [ref=e2261] [cursor=pointer]:
        - img [ref=e2262]:
          - img [ref=e2263]
        - generic [ref=e2265]: Add filter
      - button "Apply filters" [ref=e2267] [cursor=pointer]:
        - generic [ref=e2268]: Apply filters
```
```

> AGENT

I can see the filter dialog. Let me select the "Field" dropdown to see what filter options are available.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_0182TQEYGEx73wKhyzQR1yPE
```json
{
  "element": "Field combobox",
  "ref": "e2236"
}
```

> TOOL

tool_result
id: toolu_0182TQEYGEx73wKhyzQR1yPE
```
### Ran Playwright code
```js
await page.getByRole('combobox', { name: 'Field' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> generic [ref=e1]:
  - ref=e3 [unchanged]
  - dialog "Popover content" [ref=e2228]:
    - generic [ref=e2229]:
      - generic [ref=e2231]:
        - generic [ref=e2232]:
          - ref=e2234 [unchanged]
          - combobox "Field" [expanded] [ref=e2236] [cursor=pointer]:
            - ref=e2238 [unchanged]
            - ref=e2239 [unchanged]
        - ref=e2242 [unchanged]
        - ref=e2251 [unchanged]
        - ref=e2256 [unchanged]
      - ref=e2261 [unchanged]
      - ref=e2267 [unchanged]
  - listbox "undefined options" [ref=e2270]:
    - generic [ref=e2272]:
      - generic [ref=e2275]:
        - img [ref=e2277]:
          - img [ref=e2278]
        - searchbox "Search" [active] [ref=e2281]
      - generic [ref=e2282]:
        - option "Request" [ref=e2283] [cursor=pointer]:
          - generic [ref=e2284]: Request
        - option "Response" [ref=e2285] [cursor=pointer]:
          - generic [ref=e2286]: Response
        - option "Trace name" [ref=e2287] [cursor=pointer]:
          - generic [ref=e2288]: Trace name
        - option "User" [ref=e2289] [cursor=pointer]:
          - generic [ref=e2290]: User
        - option "Execution time (ms)" [ref=e2291] [cursor=pointer]:
          - generic [ref=e2292]: Execution time (ms)
        - option "State" [ref=e2293] [cursor=pointer]:
          - generic [ref=e2294]: State
        - option "Source" [ref=e2295] [cursor=pointer]:
          - generic [ref=e2296]: Source
        - option "Version" [ref=e2297] [cursor=pointer]:
          - generic [ref=e2298]: Version
        - option "Prompt" [ref=e2299] [cursor=pointer]:
          - generic [ref=e2300]: Prompt
        - option "Run name" [ref=e2301] [cursor=pointer]:
          - generic [ref=e2302]: Run name
        - option "Tags" [ref=e2303] [cursor=pointer]:
          - generic [ref=e2304]: Tags
        - option "Assessments" [ref=e2305] [cursor=pointer]:
          - generic [ref=e2306]: Assessments
        - option "Span content" [ref=e2307] [cursor=pointer]:
          - generic [ref=e2308]: Span content
        - option "Span name" [ref=e2309] [cursor=pointer]:
          - generic [ref=e2310]: Span name
        - option "Span type" [ref=e2311] [cursor=pointer]:
          - generic [ref=e2312]: Span type
```
```

> AGENT

I can see "Trace name" as a filter option. Let me select it and filter for pipeline node traces.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01LBAhJt7DXbQ4zygnonWN3v
```json
{
  "element": "Trace name option",
  "ref": "e2287"
}
```

> TOOL

tool_result
id: toolu_01LBAhJt7DXbQ4zygnonWN3v
```
### Ran Playwright code
```js
await page.getByRole('option', { name: 'Trace name' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> generic [active] [ref=e1]:
  - ref=e3 [unchanged]
  - dialog "Popover content" [ref=e2228]:
    - generic [ref=e2229]:
      - generic [ref=e2313]:
        - generic [ref=e2314]:
          - generic [ref=e2316]: Field
          - combobox "Field" [ref=e2318] [cursor=pointer]:
            - generic [ref=e2320]: Trace name
            - img [ref=e2321]:
              - img [ref=e2322]
        - generic [ref=e2324]:
          - generic [ref=e2326]: Operator
          - generic [ref=e2327]:
            - combobox "Operator" [disabled]:
              - generic: =
              - img:
                - img
        - generic [ref=e2328]:
          - generic [ref=e2330]: Value
          - textbox "Value" [ref=e2331]
        - button [ref=e2333] [cursor=pointer]:
          - img [ref=e2334]:
            - img [ref=e2335]
      - ref=e2261 [unchanged]
      - ref=e2267 [unchanged]
```
```

> AGENT

Now let me type "ingest_node" as the value to filter for a pipeline trace.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_type
id: toolu_01Ag11H3xXNqf3fYHQ4q4PA5
```json
{
  "ref": "e2331",
  "text": "ingest_node"
}
```

> TOOL

tool_result
id: toolu_01Ag11H3xXNqf3fYHQ4q4PA5
```
### Ran Playwright code
```js
await page.getByRole('textbox', { name: 'Value' }).fill('ingest_node');
```
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_012UPD4mnmtuLTscopm9gLk5
```json
{
  "element": "Apply filters button",
  "ref": "e2267"
}
```

> TOOL

tool_result
id: toolu_012UPD4mnmtuLTscopm9gLk5
```
### Ran Playwright code
```js
await page.getByRole('button', { name: 'Apply filters' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A
- Page Title: Traces - Experiment 17 - MLflow
### Snapshot
```yaml
- <changed> link "Overview" [ref=e173] [cursor=pointer]:
  - /url: "#/experiments/17/overview?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e174 [unchanged]
- <changed> link "Traces" [ref=e184] [cursor=pointer]:
  - /url: "#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e185 [unchanged]
- <changed> link "Sessions" [ref=e191] [cursor=pointer]:
  - /url: "#/experiments/17/chat-sessions?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e192 [unchanged]
- <changed> generic [ref=e270]:
  - generic [ref=e271]:
    - generic [ref=e273]:
      - ref=e275 [unchanged]
      - button "Filters (1)" [expanded] [ref=e2337] [cursor=pointer]:
        - generic [ref=e284]:
          - generic [ref=e285]:
            - ref=e286 [unchanged]
            - text: Filters (1)
            - img [ref=e2338]:
              - img [ref=e2339]
          - ref=e290 [unchanged]
      - ref=e293 [unchanged]
      - ref=e302 [unchanged]
      - ref=e313 [unchanged]
    - generic [ref=e2342]: 1 of 67
  - table [ref=e2348]:
    - row "Resize Column" [ref=e2349]:
      - generic [ref=e2350]:
        - columnheader
      - columnheader "Resize Column" [ref=e2351]:
        - generic "[object Object]" [ref=e2354]
        - button "Resize Column" [ref=e2357]
    - row "Select all Trace ID Resize Column Request Resize Column Response Resize Column Execution time Resize Column Request time Resize Column State Resize Column" [ref=e2359]:
      - columnheader "Select all" [ref=e2361]:
        - checkbox "Select all" [ref=e2365] [cursor=pointer]
      - columnheader "Trace ID Resize Column" [ref=e2367]:
        - generic "Trace ID" [ref=e2370]
        - button "Resize Column" [ref=e2371]
      - columnheader "Request Resize Column" [ref=e2373]:
        - generic "Request" [ref=e2376]
        - button "Resize Column" [ref=e2377]
      - columnheader "Response Resize Column" [ref=e2379]:
        - generic "Response" [ref=e2382]
        - button "Resize Column" [ref=e2383]
      - columnheader "Execution time Resize Column" [ref=e2385]:
        - generic "Execution time" [ref=e2388]
        - button "Resize Column" [ref=e2389]
      - columnheader "Request time Resize Column" [ref=e2391]:
        - generic "Request time" [ref=e2394]
        - button "Resize Column" [ref=e2395]
      - columnheader "State Resize Column" [ref=e2397]:
        - generic "State" [ref=e2400]
        - button "Resize Column" [ref=e2401]
      - img [ref=e2405] [cursor=pointer]:
        - img [ref=e2406]
    - 'row "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" } {\"pdf_bytes_len\": 1108708, \"status\": \"processing\"} 0.003s 02/24/2026, 17:38:53 OK" [ref=e2410]':
      - cell [ref=e2412]:
        - checkbox [ref=e2416] [cursor=pointer]
      - cell [ref=e2418]:
        - status [ref=e2421]:
          - generic [ref=e2424] [cursor=pointer]: tr-749c04951569d85fcc0a8c62c83583f8
      - 'cell "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }" [ref=e2425]':
        - generic [ref=e2428] [cursor=pointer]: "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }"
      - 'cell "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2429]':
        - 'generic "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2432]'
      - cell "0.003s" [ref=e2433]:
        - generic "0.003s" [ref=e2436]
      - cell "02/24/2026, 17:38:53" [ref=e2437]:
        - generic [ref=e2440]: 02/24/2026, 17:38:53
      - cell "OK" [ref=e2441]:
        - generic [ref=e2444]:
          - img [ref=e2445]:
            - img [ref=e2446]
          - text: OK
- <changed> generic [ref=e2229]:
  - generic [ref=e2449]:
    - generic [ref=e2450]:
      - generic [ref=e2452]: Field
      - combobox "Field" [ref=e2454] [cursor=pointer]:
        - generic [ref=e2456]: Trace name
        - img [ref=e2457]:
          - img [ref=e2458]
    - generic [ref=e2460]:
      - generic [ref=e2462]: Operator
      - generic [ref=e2463]:
        - combobox "Operator" [disabled]:
          - generic: =
          - img:
            - img
    - generic [ref=e2464]:
      - generic [ref=e2466]: Value
      - textbox "Value" [ref=e2467]: ingest_node
    - button [ref=e2469] [cursor=pointer]:
      - img [ref=e2470]:
        - img [ref=e2471]
  - ref=e2261 [unchanged]
  - button "Apply filters" [active] [ref=e2267] [cursor=pointer]:
    - ref=e2268 [unchanged]
```
```

> AGENT

There it is. **1 of 67** — the `ingest_node` trace is found with proper inputs/outputs:

- **Request**: `{"protocol_id": "165bb2ac...", "file_uri": "local://76d62a3d.../Prot_001-6e2e98f7.pdf"}`
- **Response**: `{"pdf_bytes_len": 1108708, "status": "processing"}`
- **Execution time**: 0.003s
- **Request time**: 02/24/2026, 17:38:53
- **State**: OK

Let me take a screenshot and then click into this trace for detail.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_take_screenshot
id: toolu_019TCybFSA1QVtyJ3X5iDYkN
```json
{
  "type": "png",
  "filename": "mlflow-ingest-node-trace.png"
}
```

> TOOL

tool_result
id: toolu_019TCybFSA1QVtyJ3X5iDYkN
```
### Result
- [Screenshot of viewport](mlflow-ingest-node-trace.png)
### Ran Playwright code
```js
// Screenshot viewport and save it as mlflow-ingest-node-trace.png
await page.screenshot({
path: 'mlflow-ingest-node-trace.png',
  scale: 'css',
  type: 'png'
});
```
{
  "type": "image",
  "source": {
    "data": "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",
    "media_type": "image/png",
    "type": "base64"
  }
}
```

> AGENT

The screenshot confirms it — the `ingest_node` pipeline trace is there in MLflow, filtered by `Trace name = ingest_node`. Now I can see the core issue clearly.

## Root Cause Summary

**Tracing IS working.** All 7 pipeline node traces are recorded in experiment 17. The reason you're "not seeing" them is a **signal-to-noise problem**: 60 HTTP middleware traces (GET, OPTIONS, POST from the API) drown out the 7 actual pipeline traces. When you open the Traces tab, you see a wall of `{"method": "GET", "path": "/reviews/audit-log"...}` entries and the pipeline traces are buried at the bottom.

### Two issues to fix:

1. **HTTP middleware is too noisy** — The `MLflowRequestMiddleware` traces every single API request including CORS preflight `OPTIONS` requests, static file serves, and polling endpoints. This creates ~60 traces that obscure the 7 meaningful pipeline traces.

2. **Pipeline traces lack a distinguishing "Trace name"** — The HTTP traces show as `GET /reviews/audit-log`, `OPTIONS /criteria/structured`, etc. in the Trace name column. Pipeline traces show as `ingest_node`, `extract_node`, etc. But they're visually identical in the table since the Trace name column isn't shown by default — you have to use Filters to find them.

### Recommended fixes:

1. **Filter out noisy routes in the middleware** — Skip tracing for `OPTIONS` requests, health checks, and high-frequency polling endpoints (audit-log, protocol status polls)
2. **Add a "Trace name" or "Tags" column** to the default view so pipeline traces are visually distinct

Would you like me to implement these fixes?

> DEVELOPER

No that's not the proper trace logs. If you look inside it tells you nothing of the tool uses or prompts or responses of gemini or medgemma.

> AGENT

You're right — let me click into a trace to see what's actually inside, then look at how the LLM calls are made.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_012AXRM2D2t5QKeNYAvkLEeH
```json
{
  "element": "ingest_node trace row",
  "ref": "e2424"
}
```

> TOOL

tool_result ERROR
id: toolu_012AXRM2D2t5QKeNYAvkLEeH
```
### Error
Error: Ref e2424 not found in the current page snapshot. Try capturing new snapshot.
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_snapshot
id: toolu_01AajQDPVFg4a6SJ6dDy8xL4
```json
{}
```

> TOOL

tool_result
id: toolu_01AajQDPVFg4a6SJ6dDy8xL4
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A&REDACTED
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- generic [ref=e1]:
  - generic [ref=e3]:
    - banner [ref=e4]:
      - generic [ref=e5]:
        - button "Toggle sidebar" [ref=e6] [cursor=pointer]:
          - img [ref=e7]:
            - img [ref=e8]
        - link "MLflow" [ref=e10] [cursor=pointer]:
          - /url: "#/"
          - img "MLflow" [ref=e11]
        - generic [ref=e21]: 3.9.0
      - generic [ref=e22]:
        - button "Switch to dark theme" [ref=e23] [cursor=pointer]:
          - img [ref=e24]
        - link "GitHub" [ref=e26] [cursor=pointer]:
          - /url: https://github.com/mlflow/mlflow
        - link "Docs" [ref=e27] [cursor=pointer]:
          - /url: https://www.mlflow.org/docs/latest/index.html
    - generic [ref=e28]:
      - main [ref=e31]:
        - generic [ref=e32]:
          - generic [ref=e130]:
            - generic [ref=e131]:
              - button [ref=e132] [cursor=pointer]:
                - img [ref=e133]:
                  - img [ref=e134]
              - img [ref=e137]:
                - img [ref=e138]
              - heading "protocol-processing-20260224" [level=2] [ref=e141]
              - status [ref=e142]:
                - generic [ref=e144] [cursor=pointer]:
                  - text: GenAI apps & agents
                  - img [ref=e145]:
                    - img [ref=e146]
              - button "Info" [ref=e149] [cursor=pointer]:
                - img "Info" [ref=e150]:
                  - img [ref=e151]
            - generic [ref=e154]:
              - button "Open header dropdown menu" [ref=e155] [cursor=pointer]:
                - img [ref=e156]:
                  - img [ref=e157]
              - button "Share" [ref=e159] [cursor=pointer]:
                - generic [ref=e160]: Share
              - link "View docs" [ref=e161] [cursor=pointer]:
                - /url: https://mlflow.org/docs/latest/genai/?rel=mlflow_ui
                - button "View docs" [ref=e162]:
                  - img [ref=e163]:
                    - img [ref=e164]
                  - generic [ref=e167]: View docs
          - generic [ref=e47]:
            - generic [ref=e170]:
              - generic [ref=e171]:
                - link "Overview" [ref=e173] [cursor=pointer]:
                  - /url: "#/experiments/17/overview?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A&REDACTED"
                  - generic [ref=e174]:
                    - img [ref=e176]:
                      - img [ref=e177]
                    - generic [ref=e180]: Overview
                - generic [ref=e181]:
                  - generic [ref=e183]: Observability
                  - link "Traces" [ref=e184] [cursor=pointer]:
                    - /url: "#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A&REDACTED"
                    - generic [ref=e185]:
                      - img [ref=e187]:
                        - img [ref=e188]
                      - generic [ref=e190]: Traces
                  - link "Sessions" [ref=e191] [cursor=pointer]:
                    - /url: "#/experiments/17/chat-sessions?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A&REDACTED"
                    - generic [ref=e192]:
                      - img [ref=e194]:
                        - img [ref=e195]
                      - generic [ref=e198]: Sessions
                - generic [ref=e199]:
                  - generic [ref=e201]: Evaluation
                  - link "Judges" [ref=e202] [cursor=pointer]:
                    - /url: "#/experiments/17/judges"
                    - generic [ref=e203]:
                      - img [ref=e205]:
                        - img [ref=e206]
                      - generic [ref=e208]: Judges
                  - link "Datasets" [ref=e209] [cursor=pointer]:
                    - /url: "#/experiments/17/datasets"
                    - generic [ref=e210]:
                      - img [ref=e212]:
                        - img [ref=e213]
                      - generic [ref=e215]: Datasets
                  - link "Evaluation runs" [ref=e216] [cursor=pointer]:
                    - /url: "#/experiments/17/evaluation-runs"
                    - generic [ref=e217]:
                      - img [ref=e219]:
                        - img [ref=e220]
                      - generic [ref=e223]: Evaluation runs
                - generic [ref=e224]:
                  - generic [ref=e226]: Prompts & versions
                  - link "Prompts" [ref=e227] [cursor=pointer]:
                    - /url: "#/experiments/17/prompts"
                    - generic [ref=e228]:
                      - img [ref=e230]:
                        - img [ref=e231]
                      - generic [ref=e233]: Prompts
                  - link "Agent versions" [ref=e234] [cursor=pointer]:
                    - /url: "#/experiments/17/models"
                    - generic [ref=e235]:
                      - img [ref=e237]:
                        - img [ref=e238]
                      - generic [ref=e241]: Agent versions
              - button "Assistant" [pressed] [ref=e243] [cursor=pointer]:
                - img [ref=e245]:
                  - img [ref=e246]
                  - img [ref=e248]
                - generic [ref=e249]: Assistant
                - status [ref=e250]:
                  - generic [ref=e252]: Beta
            - generic [ref=e254]:
              - generic [ref=e256]:
                - 'combobox "Time Range, selected option: Last 7 days" [ref=e258] [cursor=pointer]':
                  - generic [ref=e259]:
                    - generic [ref=e260]: "Time Range:"
                    - generic [ref=e261]: Last 7 days
                  - img [ref=e262]:
                    - img [ref=e263]
                - button [ref=e265] [cursor=pointer]:
                  - img [ref=e267]:
                    - img [ref=e268]
              - generic [ref=e270]:
                - generic [ref=e271]:
                  - generic [ref=e273]:
                    - generic [ref=e275]:
                      - img [ref=e277]:
                        - img [ref=e278]
                      - textbox "Search traces by request" [ref=e281]
                    - button "Filters (1)" [ref=e2337] [cursor=pointer]:
                      - generic [ref=e284]:
                        - generic [ref=e285]:
                          - img [ref=e286]:
                            - img [ref=e287]
                          - text: Filters (1)
                          - img [ref=e2338]:
                            - img [ref=e2339]
                        - img [ref=e290]:
                          - img [ref=e291]
                    - 'button "Sort: Request time" [ref=e293] [cursor=pointer]':
                      - img [ref=e294]:
                        - img [ref=e295]
                      - generic [ref=e297]:
                        - text: "Sort: Request time"
                        - img [ref=e299]:
                          - img [ref=e300]
                    - button "Columns" [ref=e302] [cursor=pointer]:
                      - generic [ref=e303]:
                        - generic [ref=e304]:
                          - img [ref=e305]:
                            - img [ref=e306]
                          - text: Columns
                        - img [ref=e309]:
                          - img [ref=e310]
                    - button "Actions" [disabled] [ref=e313]:
                      - generic:
                        - text: Actions
                        - generic:
                          - img:
                            - img
                  - generic [ref=e2342]: 1 of 67
                - table [ref=e2348]:
                  - row "Resize Column" [ref=e2349]:
                    - generic [ref=e2350]:
                      - columnheader
                    - columnheader "Resize Column" [ref=e2351]:
                      - generic "[object Object]" [ref=e2354]
                      - button "Resize Column" [ref=e2357]
                  - row "Select all Trace ID Resize Column Request Resize Column Response Resize Column Execution time Resize Column Request time Resize Column State Resize Column" [ref=e2359]:
                    - columnheader "Select all" [ref=e2361]:
                      - checkbox "Select all" [ref=e2365] [cursor=pointer]
                    - columnheader "Trace ID Resize Column" [ref=e2367]:
                      - generic "Trace ID" [ref=e2370]
                      - button "Resize Column" [ref=e2371]
                    - columnheader "Request Resize Column" [ref=e2373]:
                      - generic "Request" [ref=e2376]
                      - button "Resize Column" [ref=e2377]
                    - columnheader "Response Resize Column" [ref=e2379]:
                      - generic "Response" [ref=e2382]
                      - button "Resize Column" [ref=e2383]
                    - columnheader "Execution time Resize Column" [ref=e2385]:
                      - generic "Execution time" [ref=e2388]
                      - button "Resize Column" [ref=e2389]
                    - columnheader "Request time Resize Column" [ref=e2391]:
                      - generic "Request time" [ref=e2394]
                      - button "Resize Column" [ref=e2395]
                    - columnheader "State Resize Column" [ref=e2397]:
                      - generic "State" [ref=e2400]
                      - button "Resize Column" [ref=e2401]
                    - img [ref=e2405] [cursor=pointer]:
                      - img [ref=e2406]
                  - 'row "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" } {\"pdf_bytes_len\": 1108708, \"status\": \"processing\"} 0.003s 02/24/2026, 17:38:53 OK" [ref=e2410]':
                    - cell [ref=e2412]:
                      - checkbox [ref=e2416] [cursor=pointer]
                    - cell [ref=e2418]:
                      - status [ref=e2474]:
                        - generic [ref=e2477] [cursor=pointer]: tr-749c04951569d85fcc0a8c62c83583f8
                    - 'cell "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }" [ref=e2425]':
                      - generic [ref=e2479] [cursor=pointer]: "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }"
                    - 'cell "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2429]':
                      - 'generic "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2481]'
                    - cell "0.003s" [ref=e2433]:
                      - generic "0.003s" [ref=e2483]
                    - cell "02/24/2026, 17:38:53" [ref=e2437]:
                      - generic [ref=e2485]: 02/24/2026, 17:38:53
                    - cell "OK" [ref=e2441]:
                      - generic [ref=e2487]:
                        - img [ref=e2488]:
                          - img [ref=e2489]
                        - text: OK
      - generic [ref=e85]:
        - generic [ref=e86]:
          - generic [ref=e87]:
            - img [ref=e88]:
              - img [ref=e89]
              - img [ref=e92]
            - text: MLflow Assistant
            - status [ref=e93]:
              - generic [ref=e95]: Beta
          - button "Close" [ref=e97] [cursor=pointer]:
            - img [ref=e98]:
              - img [ref=e99]
        - generic [ref=e101]:
          - generic [ref=e102]:
            - heading "Welcome to MLflow Assistant" [level=3] [ref=e104]
            - generic [ref=e105]:
              - generic [ref=e106]:
                - button "Previous slide" [ref=e107] [cursor=pointer]:
                  - img [ref=e108]:
                    - img [ref=e109]
                - generic [ref=e112]:
                  - img "Debug Issues" [ref=e1264]
                  - img "Set Up Evaluations" [ref=e1265]
                  - img "Analyze Trends" [ref=e1266]
                  - img "Debug Issues" [ref=e1267]
                - button "Next slide" [ref=e117] [cursor=pointer]:
                  - img [ref=e118]:
                    - img [ref=e119]
              - generic [ref=e121]:
                - generic [ref=e122]: 1. Debug Issues
                - text: Ask questions about errors, identify root causes, and get actionable fixes for failed traces.
            - generic [ref=e123]:
              - 'button "Go to slide 1: Debug Issues" [ref=e124] [cursor=pointer]'
              - 'button "Go to slide 2: Set Up Evaluations" [ref=e125] [cursor=pointer]'
              - 'button "Go to slide 3: Analyze Trends" [ref=e126] [cursor=pointer]'
          - button "Get Started" [ref=e127] [cursor=pointer]:
            - generic [ref=e128]: Get Started
  - 'dialog "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" } Add to dataset" [ref=e2492]':
    - generic [ref=e2493]:
      - 'heading "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" } Add to dataset" [level=2] [ref=e2494]':
        - generic [ref=e2495]:
          - button [disabled] [ref=e2496]:
            - generic:
              - img:
                - img
          - button [disabled] [ref=e2497]:
            - generic:
              - img:
                - img
          - 'heading "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }" [level=2] [ref=e2500]'
          - button "Add to dataset" [active] [ref=e2501] [cursor=pointer]:
            - img [ref=e2502]:
              - img [ref=e2503]
            - generic [ref=e2505]: Add to dataset
      - button "Close" [ref=e2506] [cursor=pointer]:
        - img [ref=e2507]:
          - img [ref=e2508]
    - generic [ref=e2511]:
      - generic [ref=e2513]:
        - generic [ref=e2514]:
          - generic [ref=e2515]: Status
          - status [ref=e2516] [cursor=pointer]:
            - generic [ref=e2519]:
              - img [ref=e2521]:
                - img [ref=e2522]
              - generic [ref=e2525]: OK
        - generic [ref=e2526]:
          - generic [ref=e2527]: ID
          - status [ref=e2528] [cursor=pointer]:
            - generic [ref=e2532]: tr-749c04951569d85fcc0a8c62c83583f8
        - generic [ref=e2533]:
          - generic [ref=e2534]: Latency
          - status [ref=e2535] [cursor=pointer]:
            - generic [ref=e2538]:
              - img [ref=e2540]:
                - img [ref=e2541]
              - generic [ref=e2544]: 3.63ms
        - generic [ref=e2545]:
          - generic [ref=e2546]: Tags
          - generic [ref=e2547]:
            - status [ref=e2548] [cursor=pointer]:
              - generic [ref=e2550]: "node: ingest_node"
            - button [ref=e2552] [cursor=pointer]:
              - status [ref=e2554]:
                - generic [ref=e2556]: "+2"
      - generic [ref=e2557]:
        - tablist [ref=e2562]:
          - tab "Summary" [selected] [ref=e2563]
          - tab "Details & Timeline" [ref=e2564]
        - tabpanel "Summary" [ref=e2565]:
          - generic [ref=e2566]:
            - generic [ref=e2568]:
              - generic [ref=e2569]:
                - generic [ref=e2570] [cursor=pointer]:
                  - generic [ref=e2571]:
                    - radio "Default" [checked]
                  - generic [ref=e2572]: Default
                - generic [ref=e2573] [cursor=pointer]:
                  - generic [ref=e2574]:
                    - radio "JSON"
                  - generic [ref=e2575]: JSON
              - generic [ref=e2577] [cursor=pointer]:
                - generic [ref=e2578]:
                  - radio "Assessments"
                - generic [ref=e2580]:
                  - img [ref=e2581]:
                    - img [ref=e2582]
                  - text: Assessments
            - generic [ref=e2584]:
              - generic [ref=e2585]:
                - button [ref=e2586] [cursor=pointer]:
                  - img [ref=e2587]:
                    - img [ref=e2588]
                - heading "Inputs" [level=4] [ref=e2590]
              - generic [ref=e2592]:
                - generic [ref=e2593]:
                  - button "protocol_id" [ref=e2594]:
                    - heading "protocol_id" [level=4] [ref=e2595]
                  - generic [ref=e2597]: 165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
                - generic [ref=e2598]:
                  - button "file_uri" [ref=e2599]:
                    - heading "file_uri" [level=4] [ref=e2600]
                  - generic [ref=e2602]: local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf
            - generic [ref=e2603]:
              - generic [ref=e2604]:
                - button [ref=e2605] [cursor=pointer]:
                  - img [ref=e2606]:
                    - img [ref=e2607]
                - heading "Outputs" [level=4] [ref=e2609]
              - generic [ref=e2611]:
                - generic [ref=e2612]:
                  - button "pdf_bytes_len" [ref=e2613]:
                    - heading "pdf_bytes_len" [level=4] [ref=e2614]
                  - generic [ref=e2616]: "1108708"
                - generic [ref=e2617]:
                  - button "status" [ref=e2618]:
                    - heading "status" [level=4] [ref=e2619]
                  - generic [ref=e2621]: processing
```
### Events
- New console entries: .REDACTED.log#L1-L2
- [ERROR] null ResizeObserver loop completed with un...alhost:5001/static-files/static/js/main.9e6a97ae.js:1
- [ERROR] null ResizeObserver loop completed with un...alhost:5001/static-files/static/js/main.9e6a97ae.js:1
```

> AGENT

Now I can see the trace detail panel. It opened the `ingest_node` trace. Here's what's inside:

- **Inputs**: `protocol_id` and `file_uri`
- **Outputs**: `pdf_bytes_len: 1108708` and `status: processing`
- **Latency**: 3.63ms
- **Tags**: `node: ingest_node` (+2 more)

This is exactly the problem you're describing — **there's no LLM call detail**. The ingest node is just file loading so that's expected, but let me now look at the `extract_node` trace which is where Gemini is called. Let me first clear the filter and find the extract_node.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01SV4aARngoWm2DddZEmPshA
```json
{
  "element": "Close trace detail",
  "ref": "e2506"
}
```

> TOOL

tool_result
id: toolu_01SV4aARngoWm2DddZEmPshA
```
### Ran Playwright code
```js
await page.getByRole('dialog', { name: '{ "protocol_id": "165bb2ac-' }).getByLabel('Close').click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- <changed> link "Overview" [ref=e173] [cursor=pointer]:
  - /url: "#/experiments/17/overview?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e174 [unchanged]
- <changed> link "Traces" [ref=e184] [cursor=pointer]:
  - /url: "#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e185 [unchanged]
- <changed> link "Sessions" [ref=e191] [cursor=pointer]:
  - /url: "#/experiments/17/chat-sessions?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A"
  - ref=e192 [unchanged]
- <changed> cell [ref=e2418]:
  - status [ref=e2624]:
    - generic [ref=e2627] [cursor=pointer]: tr-749c04951569d85fcc0a8c62c83583f8
- <changed> 'cell "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }" [ref=e2425]':
  - generic [ref=e2629] [cursor=pointer]: "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"file_uri\": \"local://76d62a3d-d0f1-406e-b4dd-950a05e5a794/Prot_001-6e2e98f7.pdf\" }"
- <changed> 'cell "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2429]':
  - 'generic "{\"pdf_bytes_len\": 1108708, \"status\": \"processing\"}" [ref=e2631]'
- <changed> cell "0.003s" [ref=e2433]:
  - generic "0.003s" [ref=e2633]
- <changed> cell "02/24/2026, 17:38:53" [ref=e2437]:
  - generic [ref=e2635]: 02/24/2026, 17:38:53
- <changed> cell "OK" [ref=e2441]:
  - generic [ref=e2637]:
    - img [ref=e2638]:
      - img [ref=e2639]
    - text: OK
```
```

> AGENT

Now let me change the filter to `extract_node` — that's the node where Gemini LLM calls happen.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01MSAR55qepT3HtyUR2Y5nWr
```json
{
  "element": "Filters button",
  "ref": "e2337"
}
```

> TOOL

tool_result
id: toolu_01MSAR55qepT3HtyUR2Y5nWr
```
### Ran Playwright code
```js
await page.getByRole('button', { name: 'Filters (1)' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- <changed> generic [ref=e1]:
  - generic [ref=e3]:
    - ref=e4 [unchanged]
    - generic [ref=e28]:
      - main [ref=e31]:
        - generic [ref=e32]:
          - ref=e130 [unchanged]
          - generic [ref=e47]:
            - ref=e170 [unchanged]
            - generic [ref=e254]:
              - ref=e256 [unchanged]
              - generic [ref=e270]:
                - generic [ref=e271]:
                  - generic [ref=e273]:
                    - ref=e275 [unchanged]
                    - button "Filters (1)" [expanded] [ref=e2337] [cursor=pointer]:
                      - ref=e284 [unchanged]
                    - ref=e293 [unchanged]
                    - ref=e302 [unchanged]
                    - ref=e313 [unchanged]
                  - ref=e2342 [unchanged]
                - ref=e2348 [unchanged]
      - ref=e85 [unchanged]
  - dialog "Popover content" [ref=e2643]:
    - generic [ref=e2644]:
      - generic [ref=e2646]:
        - generic [ref=e2647]:
          - generic [ref=e2649]: Field
          - combobox "Field" [active] [ref=e2651] [cursor=pointer]:
            - generic [ref=e2653]: Trace name
            - img [ref=e2654]:
              - img [ref=e2655]
        - generic [ref=e2657]:
          - generic [ref=e2659]: Operator
          - generic [ref=e2660]:
            - combobox "Operator" [disabled]:
              - generic: =
              - img:
                - img
        - generic [ref=e2661]:
          - generic [ref=e2663]: Value
          - textbox "Value" [ref=e2664]: ingest_node
        - button [ref=e2666] [cursor=pointer]:
          - img [ref=e2667]:
            - img [ref=e2668]
      - button "Add filter" [ref=e2671] [cursor=pointer]:
        - img [ref=e2672]:
          - img [ref=e2673]
        - generic [ref=e2675]: Add filter
      - button "Apply filters" [ref=e2677] [cursor=pointer]:
        - generic [ref=e2678]: Apply filters
```
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_0199xGbKPANY1noumU4gEpSo
```json
{
  "element": "Value textbox",
  "ref": "e2664"
}
```

> TOOL

tool_result
id: toolu_0199xGbKPANY1noumU4gEpSo
```
### Ran Playwright code
```js
await page.getByRole('textbox', { name: 'Value' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aingest_node%3A%3A
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- <changed> combobox "Field" [ref=e2651] [cursor=pointer]:
  - ref=e2653 [unchanged]
  - ref=e2654 [unchanged]
- <changed> textbox "Value" [active] [ref=e2664]: ingest_node
```
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_type
id: toolu_01FEzHztrAddGtt4LUHhQecS
```json
{
  "ref": "e2664",
  "text": "extract_node"
}
```

> TOOL

tool_result
id: toolu_01FEzHztrAddGtt4LUHhQecS
```
### Ran Playwright code
```js
await page.getByRole('textbox', { name: 'Value' }).fill('extract_node');
```
```

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_01MZ6Nit7iqAKjmUb3d5m1py
```json
{
  "element": "Apply filters button",
  "ref": "e2677"
}
```

> TOOL

tool_result
id: toolu_01MZ6Nit7iqAKjmUb3d5m1py
```
### Ran Playwright code
```js
await page.getByRole('button', { name: 'Apply filters' }).click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- <changed> link "Overview" [ref=e173] [cursor=pointer]:
  - /url: "#/experiments/17/overview?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A"
  - ref=e174 [unchanged]
- <changed> link "Traces" [ref=e184] [cursor=pointer]:
  - /url: "#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A"
  - ref=e185 [unchanged]
- <changed> link "Sessions" [ref=e191] [cursor=pointer]:
  - /url: "#/experiments/17/chat-sessions?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A"
  - ref=e192 [unchanged]
- <changed> generic [ref=e270]:
  - generic [ref=e271]:
    - ref=e273 [unchanged]
    - generic [ref=e2680]: 1 of 67
  - table [ref=e2686]:
    - row "Resize Column" [ref=e2687]:
      - generic [ref=e2688]:
        - columnheader
      - columnheader "Resize Column" [ref=e2689]:
        - generic "[object Object]" [ref=e2692]
        - button "Resize Column" [ref=e2695]
    - row "Select all Trace ID Resize Column Request Resize Column Response Resize Column Execution time Resize Column Request time Resize Column State Resize Column" [ref=e2697]:
      - columnheader "Select all" [ref=e2699]:
        - checkbox "Select all" [ref=e2703] [cursor=pointer]
      - columnheader "Trace ID Resize Column" [ref=e2705]:
        - generic "Trace ID" [ref=e2708]
        - button "Resize Column" [ref=e2709]
      - columnheader "Request Resize Column" [ref=e2711]:
        - generic "Request" [ref=e2714]
        - button "Resize Column" [ref=e2715]
      - columnheader "Response Resize Column" [ref=e2717]:
        - generic "Response" [ref=e2720]
        - button "Resize Column" [ref=e2721]
      - columnheader "Execution time Resize Column" [ref=e2723]:
        - generic "Execution time" [ref=e2726]
        - button "Resize Column" [ref=e2727]
      - columnheader "Request time Resize Column" [ref=e2729]:
        - generic "Request time" [ref=e2732]
        - button "Resize Column" [ref=e2733]
      - columnheader "State Resize Column" [ref=e2735]:
        - generic "State" [ref=e2738]
        - button "Resize Column" [ref=e2739]
      - img [ref=e2743] [cursor=pointer]:
        - img [ref=e2744]
    - 'row "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 } {\"extraction_json_len\": 33875} 107.673s 02/24/2026, 17:38:53 OK" [ref=e2748]':
      - cell [ref=e2750]:
        - checkbox [ref=e2754] [cursor=pointer]
      - cell [ref=e2756]:
        - status [ref=e2759]:
          - generic [ref=e2762] [cursor=pointer]: tr-7381e06b9f81a1c9382368be8c26297f
      - 'cell "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 }" [ref=e2763]':
        - generic [ref=e2766] [cursor=pointer]: "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 }"
      - 'cell "{\"extraction_json_len\": 33875}" [ref=e2767]':
        - 'generic "{\"extraction_json_len\": 33875}" [ref=e2770]'
      - cell "107.673s" [ref=e2771]:
        - generic "107.673s" [ref=e2774]
      - cell "02/24/2026, 17:38:53" [ref=e2775]:
        - generic [ref=e2778]: 02/24/2026, 17:38:53
      - cell "OK" [ref=e2779]:
        - generic [ref=e2782]:
          - img [ref=e2783]:
            - img [ref=e2784]
          - text: OK
- <changed> generic [ref=e2644]:
  - generic [ref=e2787]:
    - generic [ref=e2788]:
      - generic [ref=e2790]: Field
      - combobox "Field" [ref=e2792] [cursor=pointer]:
        - generic [ref=e2794]: Trace name
        - img [ref=e2795]:
          - img [ref=e2796]
    - generic [ref=e2798]:
      - generic [ref=e2800]: Operator
      - generic [ref=e2801]:
        - combobox "Operator" [disabled]:
          - generic: =
          - img:
            - img
    - generic [ref=e2802]:
      - generic [ref=e2804]: Value
      - textbox "Value" [ref=e2805]: extract_node
    - button [ref=e2807] [cursor=pointer]:
      - img [ref=e2808]:
        - img [ref=e2809]
  - ref=e2671 [unchanged]
  - button "Apply filters" [active] [ref=e2677] [cursor=pointer]:
    - ref=e2678 [unchanged]
```
```

> AGENT

Found the `extract_node` trace — 107.673s execution time (the Gemini LLM call). Let me click into it to see the detail.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_click
id: toolu_014doRe2ZwYkLAWTWquwWwCw
```json
{
  "element": "extract_node trace ID",
  "ref": "e2762"
}
```

> TOOL

tool_result
id: toolu_014doRe2ZwYkLAWTWquwWwCw
```
### Ran Playwright code
```js
await page.getByText('tr-').click();
```
### Page
- Page URL: http://localhost:5001/#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A&REDACTED
- Page Title: Traces - Experiment 17 - MLflow
- Console: 2 errors, 0 warnings
### Snapshot
```yaml
- <changed> generic [ref=e1]:
  - generic [ref=e3]:
    - ref=e4 [unchanged]
    - generic [ref=e28]:
      - main [ref=e31]:
        - generic [ref=e32]:
          - ref=e130 [unchanged]
          - generic [ref=e47]:
            - generic [ref=e170]:
              - generic [ref=e171]:
                - link "Overview" [ref=e173] [cursor=pointer]:
                  - /url: "#/experiments/17/overview?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A&REDACTED"
                  - ref=e174 [unchanged]
                - generic [ref=e181]:
                  - ref=e183 [unchanged]
                  - link "Traces" [ref=e184] [cursor=pointer]:
                    - /url: "#/experiments/17/traces?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A&REDACTED"
                    - ref=e185 [unchanged]
                  - link "Sessions" [ref=e191] [cursor=pointer]:
                    - /url: "#/experiments/17/chat-sessions?filter=trace_name%3A%3A%3D%3A%3Aextract_node%3A%3A&REDACTED"
                    - ref=e192 [unchanged]
                - ref=e199 [unchanged]
                - ref=e224 [unchanged]
              - ref=e243 [unchanged]
            - generic [ref=e254]:
              - ref=e256 [unchanged]
              - generic [ref=e270]:
                - generic [ref=e271]:
                  - generic [ref=e273]:
                    - ref=e275 [unchanged]
                    - button "Filters (1)" [ref=e2337] [cursor=pointer]:
                      - ref=e284 [unchanged]
                    - ref=e293 [unchanged]
                    - ref=e302 [unchanged]
                    - ref=e313 [unchanged]
                  - ref=e2680 [unchanged]
                - table [ref=e2686]:
                  - ref=e2687 [unchanged]
                  - ref=e2697 [unchanged]
                  - 'row "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 } {\"extraction_json_len\": 33875} 107.673s 02/24/2026, 17:38:53 OK" [ref=e2748]':
                    - ref=e2750 [unchanged]
                    - cell [ref=e2756]:
                      - status [ref=e2812]:
                        - generic [ref=e2815] [cursor=pointer]: tr-7381e06b9f81a1c9382368be8c26297f
                    - 'cell "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 }" [ref=e2763]':
                      - generic [ref=e2817] [cursor=pointer]: "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 }"
                    - 'cell "{\"extraction_json_len\": 33875}" [ref=e2767]':
                      - 'generic "{\"extraction_json_len\": 33875}" [ref=e2819]'
                    - cell "107.673s" [ref=e2771]:
                      - generic "107.673s" [ref=e2821]
                    - cell "02/24/2026, 17:38:53" [ref=e2775]:
                      - generic [ref=e2823]: 02/24/2026, 17:38:53
                    - cell "OK" [ref=e2779]:
                      - generic [ref=e2825]:
                        - img [ref=e2826]:
                          - img [ref=e2827]
                        - text: OK
      - ref=e85 [unchanged]
  - 'dialog "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 } Add to dataset" [ref=e2830]':
    - generic [ref=e2831]:
      - 'heading "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 } Add to dataset" [level=2] [ref=e2832]':
        - generic [ref=e2833]:
          - button [disabled] [ref=e2834]:
            - generic:
              - img:
                - img
          - button [disabled] [ref=e2835]:
            - generic:
              - img:
                - img
          - 'heading "{ \"protocol_id\": \"165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3\", \"title\": \"Prot_001-6e2e98f7\", \"pdf_bytes_len\": 1108708 }" [level=2] [ref=e2838]'
          - button "Add to dataset" [active] [ref=e2839] [cursor=pointer]:
            - img [ref=e2840]:
              - img [ref=e2841]
            - generic [ref=e2843]: Add to dataset
      - button "Close" [ref=e2844] [cursor=pointer]:
        - img [ref=e2845]:
          - img [ref=e2846]
    - generic [ref=e2849]:
      - generic [ref=e2851]:
        - generic [ref=e2852]:
          - generic [ref=e2853]: Status
          - status [ref=e2854] [cursor=pointer]:
            - generic [ref=e2857]:
              - img [ref=e2859]:
                - img [ref=e2860]
              - generic [ref=e2863]: OK
        - generic [ref=e2864]:
          - generic [ref=e2865]: ID
          - status [ref=e2866] [cursor=pointer]:
            - generic [ref=e2870]: tr-7381e06b9f81a1c9382368be8c26297f
        - generic [ref=e2871]:
          - generic [ref=e2872]: Latency
          - status [ref=e2873] [cursor=pointer]:
            - generic [ref=e2876]:
              - img [ref=e2878]:
                - img [ref=e2879]
              - generic [ref=e2882]: 1.79m
        - generic [ref=e2883]:
          - generic [ref=e2884]: Tags
          - generic [ref=e2885]:
            - status [ref=e2886] [cursor=pointer]:
              - generic [ref=e2888]: "node: extract_node"
            - button [ref=e2890] [cursor=pointer]:
              - status [ref=e2892]:
                - generic [ref=e2894]: "+2"
      - generic [ref=e2895]:
        - tablist [ref=e2900]:
          - tab "Summary" [selected] [ref=e2901]
          - tab "Details & Timeline" [ref=e2902]
        - tabpanel "Summary" [ref=e2903]:
          - generic [ref=e2904]:
            - generic [ref=e2906]:
              - generic [ref=e2907]:
                - generic [ref=e2908] [cursor=pointer]:
                  - generic [ref=e2909]:
                    - radio "Default" [checked]
                  - generic [ref=e2910]: Default
                - generic [ref=e2911] [cursor=pointer]:
                  - generic [ref=e2912]:
                    - radio "JSON"
                  - generic [ref=e2913]: JSON
              - generic [ref=e2915] [cursor=pointer]:
                - generic [ref=e2916]:
                  - radio "Assessments"
                - generic [ref=e2918]:
                  - img [ref=e2919]:
                    - img [ref=e2920]
                  - text: Assessments
            - generic [ref=e2922]:
              - generic [ref=e2923]:
                - button [ref=e2924] [cursor=pointer]:
                  - img [ref=e2925]:
                    - img [ref=e2926]
                - heading "Inputs" [level=4] [ref=e2928]
              - generic [ref=e2930]:
                - generic [ref=e2931]:
                  - button "protocol_id" [ref=e2932]:
                    - heading "protocol_id" [level=4] [ref=e2933]
                  - generic [ref=e2935]: 165bb2ac-6fe7-4110-9b6b-7d5a37d15ee3
                - generic [ref=e2936]:
                  - button "title" [ref=e2937]:
                    - heading "title" [level=4] [ref=e2938]
                  - generic [ref=e2940]: Prot_001-6e2e98f7
                - generic [ref=e2941]:
                  - button "pdf_bytes_len" [ref=e2942]:
                    - heading "pdf_bytes_len" [level=4] [ref=e2943]
                  - generic [ref=e2945]: "1108708"
            - generic [ref=e2946]:
              - generic [ref=e2947]:
                - button [ref=e2948] [cursor=pointer]:
                  - img [ref=e2949]:
                    - img [ref=e2950]
                - heading "Outputs" [level=4] [ref=e2952]
              - generic [ref=e2955]:
                - button "extraction_json_len" [ref=e2956]:
                  - heading "extraction_json_len" [level=4] [ref=e2957]
                - generic [ref=e2959]: "33875"
```
```

> AGENT

Now I can see the problem clearly. The `extract_node` trace detail shows:

- **Inputs**: `protocol_id`, `title`, `pdf_bytes_len`  
- **Outputs**: `extraction_json_len: 33875`
- **Latency**: 1.79 minutes
- **Only 1 span** (the top-level CHAIN span)

**No LLM call details whatsoever** — no prompts, no Gemini responses, no tool uses, no token counts. Just a summary wrapper.

Now let me look at the actual extract node code to understand how it calls Gemini and why those calls aren't being traced.

> TOOL

tool_use mcp__plugin_playwright_playwright__browser_take_screenshot
id: toolu_01KJ3w4dBAKvCM7uhcDz8th6
```json
{
  "type": "png",
  "filename": "mlflow-extract-node-detail.png"
}
```

> TOOL

tool_result
id: toolu_01KJ3w4dBAKvCM7uhcDz8th6
```
### Result
- [Screenshot of viewport](mlflow-extract-node-detail.png)
### Ran Playwright code
```js
// Screenshot viewport and save it as mlflow-extract-node-detail.png
await page.screenshot({
path: 'mlflow-extract-node-detail.png',
  scale: 'css',
  type: 'png'
});
```
{
  "type": "image",
  "source": {
    "data": "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",
    "media_type": "image/png",
    "type": "base64"
  }
}
```

> TOOL

tool_use Task
id: toolu_01TAEVJWM57bPczJtZpgNgzN
```json
{
  "description": "Find LLM call patterns in nodes",
  "prompt": "I need to understand how LLM calls (Gemini, MedGemma) are made in the pipeline nodes, specifically:\n\n1. Read services/protocol-processor-service/src/protocol_processor/nodes/extract.py - how does it call Gemini? What library/client does it use?\n2. Read services/protocol-processor-service/src/protocol_processor/nodes/ground.py - how does it call MedGemma or other models?\n3. Check any other nodes that make LLM calls\n4. Look for how the LLM client is configured - is it using google.generativeai, vertexai, langchain ChatGoogleGenerativeAI, or something else?\n5. Check if there's any mlflow.google or mlflow autolog configuration that could capture LLM call details\n\nThe goal is to understand WHY the MLflow traces only show high-level inputs/outputs (like protocol_id, extraction_json_len) but NOT the actual LLM prompts, responses, tool uses, and token counts. The pipeline_span() context manager in tracing.py only creates a single top-level span with set_inputs/set_outputs - it doesn't create child spans for the actual LLM API calls.\n\nReport: what LLM library is used, how calls are made, and what MLflow integration would be needed to capture the full LLM call details.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_01TAEVJWM57bPczJtZpgNgzN
```
Now let me create a comprehensive summary document. Based on my thorough exploration, I have all the information needed:

## Report: LLM Call Integration and MLflow Tracing Architecture

Based on my comprehensive analysis of the codebase, here's how LLM calls are made in the pipeline and why MLflow traces lack detailed LLM telemetry:

---

### 1. **LLM Libraries and Clients Used**

The pipeline uses **three different LLM client libraries**:

#### A. Google GenAI SDK (for Gemini extraction via File API)
**File**: `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/gemini_extractor.py`
- **Library**: `google.genai` (google-genai package v1.55.0+)
- **Client**: `genai.Client(api_key=...)`
- **Usage**: Direct SDK calls for structured PDF extraction
- **Method**: `client.aio.models.generate_content()` with `response_schema=ExtractionResult`
- **Key Code**:
  ```python
  from google import genai
  client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
  response = await client.aio.models.generate_content(
      model=model,
      contents=[uploaded_file, user_prompt],
      config=types.GenerateContentConfig(
          system_instruction=system_prompt,
          response_mime_type="application/json",
          response_schema=ExtractionResult,
      ),
  )
  ```

#### B. LangChain ChatGoogleGenerativeAI (for structured output decisions)
**Files**:
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py`
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py`
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py`
- `/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/gemini_utils.py`

- **Library**: `langchain-google-genai` (v4.2.0+)
- **Client**: `ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=...)`
- **Usage**: Structured output formatting for medical reasoning and decision-making
- **Method**: `gemini.with_structured_output(GroundingDecision)` → `structured_llm.ainvoke(prompt)`
- **Key Code**:
  ```python
  from langchain_google_genai import ChatGoogleGenerativeAI
  
  gemini = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash",
      google_api_key=google_api_key,
  )
  structured_llm = gemini.with_structured_output(GroundingDecision)
  result = await structured_llm.ainvoke(prompt)
  ```

#### C. LangChain BaseChatModel (for MedGemma local/Vertex deployment)
**File**: `/Users/noahdolevelixir/Code/medgemma-hackathon/libs/inference/src/inference/model_garden.py`
- **Library**: `langchain-core` (part of langchain>=1.2.6)
- **Models**:
  - `ModelGardenChatModel` (Vertex AI deployment of MedGemma)
  - `LocalMedGemmaChatModel` (local GPU deployment)
- **Usage**: Medical reasoning for entity grounding decisions
- **Method**: `model.ainvoke(messages)` where messages are `[SystemMessage(...), HumanMessage(...)]`
- **Key Code** (in medgemma_decider.py):
  ```python
  from langchain_core.messages import HumanMessage, SystemMessage
  
  model = _get_medgemma_model()  # Returns Vertex or Local BaseChatModel
  messages = [
      SystemMessage(content=system_prompt),
      HumanMessage(content=evaluate_prompt),
  ]
  raw_response = await model.ainvoke(messages)
  ```

---

### 2. **LLM Call Locations and Pipeline Flow**

| Node | LLM Library | Models Called | Purpose |
|------|-------------|---------------|---------|
| **extract_node** | google.genai | Gemini 2.5 Flash | Extract structured criteria from PDF using File API |
| **parse_node** | langchain-google-genai | Gemini 2.5 Flash | Decompose criteria into entities via `decompose_entities_from_criterion()` |
| **ground_node** | 1. langchain (MedGemma) 2. langchain-google-genai (Gemini) | MedGemma + Gemini | Candidate evaluation and agentic retry loop |
| **structure_node** | langchain-google-genai | Gemini 2.5 Flash | Logic detection for AND/OR/NOT structure |
| **ordinal_resolve** | langchain-google-genai | Gemini 2.5 Flash | Clinical ordinal scale identification |
| **field_mapper** | langchain-google-genai | Gemini 2.5 Flash | Auto-generate field mappings |

---

### 3. **MLflow Tracing Architecture - Why Details Are Missing**

**MLflow Configuration**:
- **Tracking URI**: Environment variable `MLFLOW_TRACKING_URI` (required, checked in preflight)
- **Experiment**: One per day: `protocol-processing-YYYYMMDD`
- **Status**: **Autolog is EXPLICITLY DISABLED** (see tracing.py lines 10-15)

**Current Architecture** (`pipeline_span()` context manager in tracing.py):
```python
@contextmanager
def pipeline_span(
    name: str,
    span_type: str = "CHAIN",
    protocol_id: str = "",
):
    """Create a separate MLflow trace for a pipeline node.
    
    Each call creates its own top-level trace tagged with protocol_id
    and run_id, so individual node traces appear in MLflow as they
    complete rather than waiting for the entire pipeline to finish.
    """
    with mlflow.start_span(name=name, span_type=span_type, ...) as span:
        span.set_inputs({...})
        # --- NODE WORK HAPPENS HERE ---
        span.set_outputs({...})
```

**The Problem**:
1. **No Child Spans**: Each node creates a single top-level span with only `set_inputs()` and `set_outputs()`
2. **No LLM Detail Capture**: The LLM calls inside the node (via google.genai, ChatGoogleGenerativeAI, MedGemma) are **completely invisible** to MLflow
3. **Example from extract_node** (lines 35-63):
   ```python
   with pipeline_span("extract_node", span_type="LLM", protocol_id=protocol_id) as span:
       span.set_inputs({
           "protocol_id": state.get("protocol_id", ""),
           "title": state.get("title", ""),
           "pdf_bytes_len": len(state.get("pdf_bytes") or b""),
       })
       
       extraction_json = await extract_criteria_structured(...)  # <-- LLM call hidden
       
       span.set_outputs({
           "extraction_json_len": len(extraction_json) if extraction_json else 0,
       })
   ```

4. **Metadata Loss**:
   - ❌ Gemini prompts and responses
   - ❌ Token counts (input/output/total)
   - ❌ Model latency
   - ❌ API errors and retries
   - ❌ Structured output schema usage
   - ❌ Tool/function calls (if any)
   - ❌ MedGemma medical reasoning steps
   - ✓ Only sees: high-level node inputs (metadata like `protocol_id`, file size) and outputs (JSON length)

---

### 4. **Why Autolog is Disabled**

From `trigger.py` lines 249-256:
```python
# MLflow tracing: do NOT enable langchain.autolog() here.
# Autolog wraps the entire ainvoke() in a single trace that only
# appears in MLflow after the full pipeline completes.  Instead,
# each node creates its own independent trace via pipeline_span()
# so traces appear in real-time as nodes finish.
```

**Decision Rationale**:
- If `mlflow.langchain.autolog()` were enabled, the entire 5-node pipeline would be wrapped in a **single parent trace** created when `graph.ainvoke()` starts
- This means MLflow wouldn't show any trace until the **entire 20-60 minute pipeline completes**
- Instead, the current design creates **independent traces per node** so you see progress in MLflow as each node finishes

**Tradeoff**: Faster per-node visibility ↔ Loss of detailed LLM telemetry

---

### 5. **What Would Be Needed to Capture LLM Details**

To capture prompts, responses, token counts, and latency for each LLM call:

#### Option A: LangChain CallbackHandler (Lightweight, Recommended)
```python
# Create custom callback to wrap LLM calls
from langchain_core.callbacks import BaseCallbackHandler

class MLflowLLMCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        # Create MLflow child span for this LLM call
        mlflow.start_span(name=f"llm_call_{serialized['id'][-1]}")
        
    def on_llm_end(self, response, **kwargs):
        # Log token counts from response.llm_output
        mlflow.end_span()
```

Then inject into each LLM call:
```python
gemini = ChatGoogleGenerativeAI(..., callbacks=[MLflowLLMCallback()])
```

#### Option B: google.genai Instrumentation
The `google.genai` SDK doesn't have built-in MLflow integration, but you could wrap calls:
```python
@mlflow.trace
async def invoke_gemini_traced(client, model, contents, config):
    with mlflow.start_span(name="gemini_api_call") as span:
        span.set_inputs({"model": model, "num_contents": len(contents)})
        response = await client.aio.models.generate_content(
            model=model, contents=contents, config=config
        )
        if response.usage_metadata:
            span.set_outputs({
                "input_tokens": response.usage_metadata.input_tokens,
                "output_tokens": response.usage_metadata.output_tokens,
                "total_tokens": response.usage_metadata.total_tokens,
            })
        return response
```

#### Option C: Full LangChain Instrumentation (Heavy-handed)
Enable selective autolog for just the LLM providers:
```python
import mlflow.langchain
mlflow.langchain.autolog(log_models=False, log_input_examples=False)
```
But this would require restructuring the pipeline to use autolog at a different level.

#### Option D: MLflow Tracing API Enhancement (Current Code)
Modify `pipeline_span()` to create child spans:
```python
@contextmanager
def pipeline_span(...):
    with mlflow.start_span(name=name, ...) as parent_span:
        span.set_inputs({...})
        
        # Pass parent_span reference to tools so they can create children
        # This requires threading context through the call stack
        
        yield parent_span
        span.set_outputs({...})
```

Then in `medgemma_decide()`:
```python
async def medgemma_decide(entity, candidates, criterion_context):
    parent_span = mlflow.get_current_span()  # Get from context
    
    with mlflow.start_span(
        "medgemma_decision",
        parent_run_id=parent_span.request_id
    ) as span:
        # Log prompts, decisions, etc.
        pass
```

---

### 6. **Summary Table: LLM Integration**

| Aspect | Current State | Gap | Needed for Full Observability |
|--------|---------------|-----|-------------------------------|
| **Gemini Extraction** | google.genai SDK, File API | No MLflow logging | Wrap `_invoke_gemini()` with MLflow span |
| **MedGemma Reasoning** | LangChain BaseChatModel | No child spans | Add LangChain CallbackHandler |
| **Gemini Structuring** | ChatGoogleGenerativeAI.with_structured_output() | No prompt logging | Create wrapper or callback |
| **Token Counting** | Not captured | Missing | Extract from response.usage_metadata |
| **Prompt Visibility** | Lost at function boundary | Invisible to MLflow | Log prompts in span inputs |
| **Error Tracking** | Circuit breaker + retry in code | Not in MLflow traces | Add exception logging to spans |
| **Latency** | Implicit in node timing | Coarse-grained | Create sub-spans for each LLM call |

---

### Conclusion

The pipeline uses **three distinct LLM client libraries** (google.genai, langchain-google-genai, langchain-core) but MLflow sees only **node-level I/O** because:

1. **Autolog disabled** to show real-time per-node progress instead of waiting for full pipeline completion
2. **No child spans created** inside nodes for individual LLM calls
3. **LLM calls are encapsulated** in tool functions without MLflow instrumentation

To capture full LLM telemetry (prompts, responses, tokens, latency), you'd need to instrument the LLM calls directly using LangChain CallbackHandlers or wrap the google.genai calls with MLflow span creation, threading context through the call stack so child spans can be created within the parent node span.
agentId: ade8155c709af6e0e (for resuming to continue this agent's work if needed)
<usage>total_tokens: 65923
tool_uses: 22
duration_ms: 119990</usage>
```

> AGENT

The screenshot and code analysis confirm the root cause. Here's the real diagnosis:

## Root Cause: No LLM-level instrumentation inside pipeline spans

The `extract_node` trace (screenshot above) shows only:
- **Inputs**: `protocol_id`, `title`, `pdf_bytes_len` 
- **Outputs**: `extraction_json_len: 33875`

That's it. No prompts, no Gemini responses, no token counts, no tool uses.

### Why

The pipeline uses **3 different LLM libraries**, none of which are instrumented:

| Library | Used In | What It Does |
|---------|---------|-------------|
| `google.genai` (SDK) | `gemini_extractor.py` | Gemini 2.5 Flash PDF extraction via File API |
| `langchain-google-genai` | `medgemma_decider.py`, `entity_decomposer.py`, `field_mapper.py`, `gemini_utils.py` | Structured output (grounding decisions, entity decomposition) |
| `langchain-core` BaseChatModel | `model_garden.py` | MedGemma reasoning (Vertex AI or local) |

The `pipeline_span()` context manager in `tracing.py` creates **one flat span per node** with `set_inputs()`/`set_outputs()` — but the actual LLM calls inside (`client.aio.models.generate_content()`, `structured_llm.ainvoke()`, `model.ainvoke()`) create **zero child spans**. MLflow never sees them.

`mlflow.langchain.autolog()` is explicitly disabled because it wraps the entire `graph.ainvoke()` in a single trace that only appears after the full pipeline finishes (~20 min).

### The fix needed

Each LLM call needs to create child spans inside the parent node span, logging:
- The prompt/messages sent
- The model response
- Token counts (input/output/total)  
- Model name and latency

Want me to implement this instrumentation?

> DEVELOPER

Yes. Implement the changes, make sure ruff, mypy and pytest pass. Then run a smoke test (which you don't commit) to make sure your solution works.

> TOOL

tool_use EnterPlanMode
id: toolu_019bosAgpuFjhpm6YdQr989m
```json
{}
```

> TOOL

tool_result
id: toolu_019bosAgpuFjhpm6YdQr989m
```
Entered plan mode. You should now focus on exploring the codebase and designing an implementation approach.

In plan mode, you should:
1. Thoroughly explore the codebase to understand existing patterns
2. Identify similar features and architectural approaches
3. Consider multiple approaches and their trade-offs
4. Use AskUserQuestion if you need to clarify the approach
5. Design a concrete implementation strategy
6. When ready, use ExitPlanMode to present your plan for approval

Remember: DO NOT write or edit any files yet. This is a read-only exploration and planning phase.
```

> TOOL

tool_use Task
id: toolu_01Kvv4UKkDLpRSfZHeHV3JBU
```json
{
  "description": "Explore LLM call sites",
  "prompt": "I need to understand exactly how LLM calls are made in the pipeline so I can add MLflow child span instrumentation. Please find and read these files thoroughly:\n\n1. `services/protocol-processor-service/src/protocol_processor/tools/gemini_extractor.py` - The Gemini extraction using google.genai SDK\n2. `services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py` - MedGemma decision making  \n3. `services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py` - Entity decomposition\n4. `services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py` - Field mapping\n5. `services/protocol-processor-service/src/protocol_processor/tools/gemini_utils.py` - Gemini utilities\n6. `services/protocol-processor-service/src/protocol_processor/nodes/extract.py` - Extract node\n7. `services/protocol-processor-service/src/protocol_processor/nodes/ground.py` - Ground node\n8. `services/protocol-processor-service/src/protocol_processor/nodes/parse.py` - Parse node  \n9. `services/protocol-processor-service/src/protocol_processor/nodes/structure.py` - Structure node\n10. `services/protocol-processor-service/src/protocol_processor/nodes/ordinal_resolve.py` - Ordinal resolve node\n\nFor each file, I need:\n- The exact function signature that calls the LLM\n- What library/client it uses (google.genai, ChatGoogleGenerativeAI, BaseChatModel)\n- What arguments it passes (model name, prompts, config)\n- Whether it returns token counts / usage metadata\n- How the response is processed\n\nAlso check:\n- `libs/inference/src/inference/model_garden.py` - MedGemma model implementation\n- Any existing MLflow integration patterns in the codebase\n\nReport exact function names, signatures, and the pattern of how they call LLMs.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Task
id: toolu_01JnEjpcEK9YN2GmcMbdxM2a
```json
{
  "description": "Explore MLflow span nesting API",
  "prompt": "I need to understand how MLflow 3.x span nesting works. Please:\n\n1. Read `services/protocol-processor-service/src/protocol_processor/tracing.py` fully\n2. Search the codebase for any existing usage of `mlflow.start_span` with nesting/parent contexts\n3. Check what version of mlflow is in use (look at pyproject.toml or requirements files)\n4. Search for `mlflow.trace` decorator usage anywhere in the codebase\n5. Check if `mlflow.get_current_active_span()` or similar APIs are used\n6. Look at the test files for tracing - find any test patterns: `tests/**/test_trac*` or similar\n7. Check `services/protocol-processor-service/pyproject.toml` for mlflow version and any google-genai / langchain dependencies\n\nThe key question: In MLflow 3.x, if I create a span with `mlflow.start_span()` inside an existing `mlflow.start_span()` context, does it automatically become a child span? Or does the current code's `pipeline_span()` somehow prevent nesting because each node creates independent top-level traces?\n\nReport the exact MLflow version, the nesting behavior, and any relevant test patterns.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_01Kvv4UKkDLpRSfZHeHV3JBU
```
Perfect! Now I have a comprehensive understanding of the LLM call patterns. Let me compile the detailed analysis:

## Summary of LLM Calls in the Pipeline

Based on my thorough analysis of the codebase, here's the exact breakdown of how LLM calls are made and where you need to add MLflow child span instrumentation:

### **1. GEMINI EXTRACTION (gemini_extractor.py)**

**Function:** `_invoke_gemini()` (lines 73-108)
- **Signature:** `async def _invoke_gemini(client: genai.Client, model: str, uploaded_file: types.File, system_prompt: str, user_prompt: str) -> ExtractionResult`
- **Library/Client:** `google.genai.Client` (direct SDK, not LangChain)
- **Call Pattern:**
  ```python
  response = await client.aio.models.generate_content(
      model=model,
      contents=cast(Any, [uploaded_file, user_prompt]),
      config=types.GenerateContentConfig(
          system_instruction=system_prompt,
          response_mime_type="application/json",
          response_schema=ExtractionResult,
      ),
  )
  ```
- **Returns:** `response.parsed` (Pydantic ExtractionResult) or falls back to `response.text`
- **Token Metadata:** Not explicitly extracted in code
- **Wrapper Function:** `extract_criteria_structured()` (lines 156-261) — main entry point
- **Node Entry:** Called from `extract_node()` in extract.py (line 47)

---

### **2. MEDGEMMA DECISION MAKING (medgemma_decider.py)**

**Function A:** `medgemma_decide()` (lines 177-283)
- **Signature:** `async def medgemma_decide(entity: dict, candidates: list[GroundingCandidate], criterion_context: str) -> EntityGroundingResult`
- **Library/Client:** `BaseChatModel` via `_get_medgemma_model()` (lazy-loaded from model_garden.py)
- **Call Pattern:**
  ```python
  model = _get_medgemma_model()  # Returns BaseChatModel (Vertex/Local/Ollama)
  messages = [
      SystemMessage(content=system_prompt),
      HumanMessage(content=evaluate_prompt),
  ]
  raw_response = await model.ainvoke(messages)  # Line 237
  raw_text = raw_response.content
  ```
- **LLM Response Processing:** Raw text passed to `_structure_decision_with_gemini()` for structuring
- **Node Entry:** Called from `ground_node()` → `_ground_entity_with_retry()` (line 266)

**Function B:** `_structure_decision_with_gemini()` (lines 144-174)
- **Signature:** `async def _structure_decision_with_gemini(raw_text: str) -> GroundingDecision`
- **Library/Client:** `ChatGoogleGenerativeAI` (LangChain wrapper around Gemini)
- **Call Pattern:**
  ```python
  gemini = ChatGoogleGenerativeAI(model=gemini_model_name, google_api_key=google_api_key)
  structured_llm = gemini.with_structured_output(GroundingDecision)
  result = await structured_llm.ainvoke(prompt)  # Line 171
  ```
- **Returns:** `GroundingDecision` Pydantic model (dict or instance)
- **Token Metadata:** Not extracted
- **Called From:** `medgemma_decide()` (line 246)

**Function C:** `agentic_reasoning_loop()` (lines 327-421)
- **Signature:** `async def agentic_reasoning_loop(entity: dict, criterion_context: str, router: TerminologyRouter, attempt: int = 1) -> AgenticReasoningResult`
- **MedGemma Call:** 
  ```python
  model = _get_medgemma_model()
  messages = [SystemMessage(...), HumanMessage(...)]
  raw_response = await model.ainvoke(messages)  # Line 384
  raw_text = raw_response.content
  ```
- **Gemini Structuring Call:** `await _structure_reasoning_with_gemini(raw_text)` (line 393)

**Function D:** `_structure_reasoning_with_gemini()` (lines 286-324)
- **Signature:** `async def _structure_reasoning_with_gemini(raw_text: str) -> AgenticReasoningResult`
- **Library/Client:** `ChatGoogleGenerativeAI` with structured output
- **Call Pattern:** Same as `_structure_decision_with_gemini()` but returns `AgenticReasoningResult`

---

### **3. ENTITY DECOMPOSITION (entity_decomposer.py)**

**Function:** `decompose_entities_from_criterion()` (lines 62-97)
- **Signature:** `async def decompose_entities_from_criterion(criterion_text: str, category: str | None) -> list[dict]`
- **Library/Client:** `ChatGoogleGenerativeAI` (LangChain)
- **Call Pattern:**
  ```python
  gemini = ChatGoogleGenerativeAI(
      model=os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash"),
      google_api_key=os.getenv("GOOGLE_API_KEY"),
  )
  structured = gemini.with_structured_output(DecomposedEntityList)
  result = await structured.ainvoke(prompt)  # Line 86
  ```
- **Returns:** `DecomposedEntityList` (list of `DecomposedEntity` dicts)
- **Node Entry:** Called from `parse_node()` (line 138)

---

### **4. FIELD MAPPING GENERATION (field_mapper.py)**

**Function:** `generate_field_mappings()` (lines 123-217)
- **Signature:** `async def generate_field_mappings(entity: EntityGroundingResult, criterion_text: str) -> list[dict[str, Any]]`
- **Library/Client:** Uses `create_structured_llm()` from gemini_utils.py
- **Call Pattern:**
  ```python
  structured_llm = create_structured_llm(FieldMappingResponse)
  result = await structured_llm.ainvoke(prompt)  # Line 184
  response = parse_structured_output(result, FieldMappingResponse)
  ```
- **Returns:** List of field mapping dicts
- **Node Entry:** Called from `ground_node()` → `_ground_entity_parallel()` (line 495)

---

### **5. STRUCTURE DETECTION (structure_builder.py)**

**Function:** `detect_logic_structure()` (lines 107-181)
- **Signature:** `async def detect_logic_structure(criterion_text: str, field_mappings: list[dict[str, Any]]) -> LogicDetectionResponse | None`
- **Library/Client:** `create_structured_llm(LogicDetectionResponse)` (Gemini or Ollama)
- **Call Pattern:**
  ```python
  structured_llm = create_structured_llm(LogicDetectionResponse)
  result = await structured_llm.ainvoke(prompt)  # Line 161
  response = parse_structured_output(result, LogicDetectionResponse)
  ```
- **Returns:** `LogicDetectionResponse` with logic tree
- **Node Entry:** Called from `structure_node()` → `_process_criterion()` → `build_expression_tree()` (line 393)

---

### **6. ORDINAL RESOLUTION (ordinal_resolver.py)**

**Function:** `resolve_ordinal_candidates()` (lines 31-103)
- **Signature:** `async def resolve_ordinal_candidates(candidates: list[dict[str, Any]]) -> OrdinalResolutionResponse | None`
- **Library/Client:** `create_structured_llm(OrdinalResolutionResponse)` (Gemini or Ollama)
- **Call Pattern:**
  ```python
  structured_llm = create_structured_llm(OrdinalResolutionResponse)
  result = await structured_llm.ainvoke(prompt)  # Line 87
  response = parse_structured_output(result, OrdinalResolutionResponse)
  ```
- **Returns:** `OrdinalResolutionResponse` with proposals
- **Node Entry:** Called from `ordinal_resolve_node()` → `_process_batch()` (line 225)

---

### **7. GEMINI UTILITIES (gemini_utils.py)**

**Helper Functions:**
- `create_structured_llm(output_schema)` — Factory that creates either `ChatGoogleGenerativeAI.with_structured_output()` or `ChatOllama.with_structured_output()` (lines 24-75)
- `parse_structured_output(result, model)` — Parses dict or Pydantic model (lines 78-93)

---

### **8. MEDGEMMA MODEL LOADING (model_garden.py)**

**Classes:**
- `ModelGardenChatModel` (BaseChatModel) — Vertex AI endpoint (lines 176-266)
  - `_generate()` method calls `_predict_with_retry()` (line 239) → `endpoint.predict()`
  
- `LocalMedGemmaChatModel` (BaseChatModel) — Local HuggingFace model (lines 299-442)
  - `_generate()` method uses `model.generate()` with torch (lines 415-422)

**Factory:** `create_model_loader(config)` returns lazy-loading callable (lines 445-469)

---

### **EXISTING MLFLOW INTEGRATION (tracing.py)**

**Current Pattern:**
- `pipeline_span(name, span_type, protocol_id)` — Context manager that creates **top-level MLflow spans** (lines 56-116)
- Each node creates its own trace, tagged with `protocol_id`, `run_id`, `node`
- Uses `mlflow.start_span()`, `span.set_inputs()`, `span.set_outputs()`
- **IMPORTANT:** `mlflow.langchain.autolog()` is explicitly disabled (docs say so)

**What's Missing:** **No child spans for individual LLM calls within nodes**

---

### **INSTRUMENTATION TARGETS FOR CHILD SPANS**

You need to add **child spans** inside these functions:

| Function | File | LLM Library | Call Line | Span Name |
|----------|------|-------------|-----------|-----------|
| `_invoke_gemini()` | gemini_extractor.py | google.genai | 92 | `gemini_file_api_extraction` |
| `medgemma_decide()` | medgemma_decider.py | BaseChatModel.ainvoke | 237 | `medgemma_entity_decision` |
| `_structure_decision_with_gemini()` | medgemma_decider.py | ChatGoogleGenerativeAI | 171 | `gemini_structure_decision` |
| `agentic_reasoning_loop()` | medgemma_decider.py | BaseChatModel.ainvoke | 384 | `medgemma_agentic_reasoning` |
| `_structure_reasoning_with_gemini()` | medgemma_decider.py | ChatGoogleGenerativeAI | 321 | `gemini_structure_reasoning` |
| `decompose_entities_from_criterion()` | entity_decomposer.py | ChatGoogleGenerativeAI | 86 | `gemini_entity_decompose` |
| `generate_field_mappings()` | field_mapper.py | ChatGoogleGenerativeAI | 184 | `gemini_field_mapping` |
| `detect_logic_structure()` | structure_builder.py | ChatGoogleGenerativeAI/ChatOllama | 161 | `gemini_logic_detection` |
| `resolve_ordinal_candidates()` | ordinal_resolver.py | ChatGoogleGenerativeAI/ChatOllama | 87 | `gemini_ordinal_resolution` |

---

### **KEY IMPLEMENTATION NOTES**

1. **Two-Library Pattern:** 
   - `google.genai` (direct SDK) in gemini_extractor.py
   - `ChatGoogleGenerativeAI` (LangChain wrapper) everywhere else

2. **Response Handling:**
   - google.genai: `response.parsed` (Pydantic) or `response.text` (JSON string)
   - LangChain: `result` is dict or Pydantic model

3. **Token Usage:** Not currently captured in code — would need to be added from response metadata

4. **MedGemma Backend Abstraction:** MedGemma uses `BaseChatModel` interface, so it can be Vertex AI, Local, or Ollama — all compatible with `.ainvoke()`

5. **Existing Span Infrastructure:** You can use the same `pipeline_span()` context manager pattern for child spans, or use `mlflow.start_span()` directly for finer control

This comprehensive mapping gives you all the exact locations and patterns needed to add child span instrumentation!
agentId: aa21da58a8660451f (for resuming to continue this agent's work if needed)
<usage>total_tokens: 71947
tool_uses: 17
duration_ms: 42780</usage>
```

> TOOL

tool_result
id: toolu_01JnEjpcEK9YN2GmcMbdxM2a
```
Excellent! Now I have all the information I need to provide a comprehensive answer. Let me compile the findings:

## MLflow 3.x Span Nesting Analysis Report

Based on my thorough analysis of your codebase, here's what I found:

### 1. **Exact MLflow Version**
```
MLflow >= 3.8.1
```
From `/services/protocol-processor-service/pyproject.toml` (line 27):
```
mlflow>=3.8.1
```

### 2. **MLflow 3.x Nesting Behavior**

In MLflow 3.x, **if you create a span with `mlflow.start_span()` inside an existing `mlflow.start_span()` context, it AUTOMATICALLY becomes a child span**. However, your codebase **explicitly prevents this nesting** through design decisions:

**Current Design - No Nesting:**
- Each node calls `mlflow.start_span()` at the **top level** (not nested within the graph's ainvoke)
- Each call creates an **independent root trace** tagged with protocol_id and run_id
- Traces flush to MLflow **as soon as the context manager exits**
- This produces separate, real-time traces visible in MLflow UI incrementally

### 3. **Why Nesting is Prevented**

From the critical documentation in your code:

**In `/services/protocol-processor-service/src/protocol_processor/tracing.py` (lines 10-15):**
```python
IMPORTANT: ``mlflow.langchain.autolog()`` must NOT be enabled.  Autolog
wraps ``graph.ainvoke()`` in a single parent trace and all node spans
become children — producing one constantly-updating trace that only
appears after the full pipeline finishes.  Without autolog, each call to
``mlflow.start_span()`` inside a node creates an independent root trace
that is flushed to MLflow as soon as the context manager exits.
```

**In `/services/api-service/src/api_service/main.py` (lines 67-71):**
```python
# NOTE: Do NOT enable mlflow.langchain.autolog() here.
# Autolog wraps graph.ainvoke() in a single trace that only
# appears after the full pipeline finishes.  Each pipeline
# node creates its own independent trace via pipeline_span()
# so traces stream to MLflow in real-time as nodes complete.
```

### 4. **The `pipeline_span()` Implementation**

Located in `/services/protocol-processor-service/src/protocol_processor/tracing.py` (lines 56-117):

**Key mechanism:**
```python
@contextmanager
def pipeline_span(
    name: str,
    span_type: str = "CHAIN",
    protocol_id: str = "",
):
    """Create a separate MLflow trace for a pipeline node.
    
    Each call creates its own top-level trace tagged with protocol_id
    and run_id, so individual node traces appear in MLflow as they
    complete rather than waiting for the entire pipeline to finish.
    """
```

The context manager uses `trace_destination` parameter to control which experiment the span goes to:
```python
trace_destination = (
    MlflowExperimentLocation(experiment_id=exp_id) if exp_id else None
)
with mlflow.start_span(
    name=name,
    span_type=span_type,
    trace_destination=trace_destination,
) as span:
```

### 5. **MLflow 3.x Parent Context Handling**

Based on the code design and comments, **MLflow 3.x has a context stack mechanism**:
- When you call `mlflow.start_span()` **without a trace_destination**, it respects the current active span context
- **With `trace_destination` explicitly set**, it creates a new root trace (breaking the parent-child relationship)
- The `MlflowExperimentLocation` parameter forces the span to be a root trace in a specific experiment

### 6. **Usage Pattern in Pipeline Nodes**

All nodes follow this pattern. Example from `/services/protocol-processor-service/src/protocol_processor/nodes/ingest.py` (lines 42-47):

```python
with pipeline_span("ingest_node", protocol_id=state.get("protocol_id", "")) as span:
    span.set_inputs({
        "protocol_id": state.get("protocol_id", ""),
        "file_uri": state.get("file_uri", ""),
    })
```

Each node:
1. Ingest → Extract → Parse → Ground → Persist
2. All use `pipeline_span()` wrapper
3. Each creates its own independent trace

### 7. **Verification Script**

Your codebase includes `/scripts/verify_mlflow_tracing.py` which validates this behavior. It confirms:
- **3 separate traces** appear (not 1 parent + 3 children)
- **Real-time appearance**: traces show up incrementally as nodes complete
- **Consistent tagging**: all traces share protocol_id and run_id for grouping

### 8. **API Request Tracing**

Additionally, `/services/api-service/src/api_service/middleware.py` creates **HTTP span traces** for FastAPI requests (lines 63-79), which are also independent root traces.

And `/libs/shared/src/shared/resilience.py` creates spans for **circuit breaker state changes** (lines 37-48).

---

## Key Answer to Your Question

**In MLflow 3.x, if I create a span with `mlflow.start_span()` inside an existing `mlflow.start_span()` context, does it automatically become a child span?**

**YES** — it automatically becomes a child span. However, your code **prevents this** by:
1. **Not nesting spans** — each node's pipeline_span() is called at the top level
2. **Using `trace_destination=MlflowExperimentLocation(...)`** to force independent root traces
3. **Never enabling `mlflow.langchain.autolog()`** which would create the parent-child hierarchy

This design gives you **real-time, independent trace visualization** instead of a single updating trace that only appears when the pipeline completes.
agentId: ac4610a5f3cb3bfba (for resuming to continue this agent's work if needed)
<usage>total_tokens: 48049
tool_uses: 23
duration_ms: 39738</usage>
```

> AGENT

Good — now I know that MLflow 3.x automatically nests `start_span()` calls inside an existing span context. Since `pipeline_span()` already creates a top-level span per node, any `mlflow.start_span()` called inside will automatically become a child. Let me read the key files to nail down the exact implementation.

> TOOL

tool_use Read
id: toolu_01SkdzqD83Jckd5jcygmcGyP
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/gemini_extractor.py"
}
```

> TOOL

tool_result
id: toolu_01SkdzqD83Jckd5jcygmcGyP
```
     1→"""Gemini extractor tool: structured criteria extraction via Gemini File API.
     2→
     3→Uploads PDF to Gemini File API, calls Gemini with structured output using
     4→ExtractionResult as the response schema, and returns a JSON string.
     5→
     6→Returns JSON string (not dict) to minimize LangGraph state size.
     7→"""
     8→
     9→from __future__ import annotations
    10→
    11→import logging
    12→import os
    13→import tempfile
    14→from pathlib import Path
    15→from typing import Any, cast
    16→
    17→from google import genai
    18→from google.genai import types
    19→from inference.factory import render_prompts
    20→from pydantic import ValidationError
    21→from shared.resilience import gemini_breaker
    22→from tenacity import (
    23→    before_sleep_log,
    24→    retry,
    25→    retry_if_exception_type,
    26→    stop_after_attempt,
    27→    wait_random_exponential,
    28→)
    29→
    30→from protocol_processor.schemas.extraction import ExtractionResult
    31→
    32→logger = logging.getLogger(__name__)
    33→
    34→PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
    35→
    36→# Max length when formatting validation errors (avoids huge console dumps)
    37→_VALIDATION_ERROR_STR_MAX = 200
    38→
    39→
    40→def _truncate(s: str, max_len: int = _VALIDATION_ERROR_STR_MAX) -> str:
    41→    """Truncate string for safe inclusion in error messages."""
    42→    if len(s) <= max_len:
    43→        return s
    44→    return s[:max_len] + "..."
    45→
    46→
    47→def _format_validation_error(err: ValidationError) -> str:
    48→    """Format ValidationError with truncated input/context for safe logging."""
    49→    errors = err.errors()
    50→    parts = [f"ValidationError ({len(errors)} error(s))"]
    51→    for e in errors:
    52→        loc = ".".join(str(x) for x in e.get("loc", ()))
    53→        msg = e.get("msg", "")
    54→        ctx = e.get("ctx") or {}
    55→        inp = e.get("input")
    56→        part = f"  {loc}: {msg}"
    57→        if ctx:
    58→            part += f" (ctx: {_truncate(str(ctx))})"
    59→        if inp is not None:
    60→            part += f" | input: {_truncate(str(inp))}"
    61→        parts.append(part)
    62→    return "\n".join(parts)
    63→
    64→
    65→@gemini_breaker
    66→@retry(
    67→    retry=retry_if_exception_type(Exception),
    68→    stop=stop_after_attempt(3),
    69→    wait=wait_random_exponential(multiplier=1, min=2, max=10),
    70→    before_sleep=before_sleep_log(logger, logging.WARNING),
    71→    reraise=True,
    72→)
    73→async def _invoke_gemini(
    74→    client: genai.Client,
    75→    model: str,
    76→    uploaded_file: types.File,
    77→    system_prompt: str,
    78→    user_prompt: str,
    79→) -> ExtractionResult:
    80→    """Invoke Gemini with retry and circuit breaker.
    81→
    82→    Args:
    83→        client: Google GenAI client instance.
    84→        model: Model name to use.
    85→        uploaded_file: Uploaded PDF file from File API.
    86→        system_prompt: System instruction.
    87→        user_prompt: User prompt text.
    88→
    89→    Returns:
    90→        ExtractionResult parsed from Gemini's structured output.
    91→    """
    92→    response = await client.aio.models.generate_content(
    93→        model=model,
    94→        contents=cast(Any, [uploaded_file, user_prompt]),
    95→        config=types.GenerateContentConfig(
    96→            system_instruction=system_prompt,
    97→            response_mime_type="application/json",
    98→            response_schema=ExtractionResult,
    99→        ),
   100→    )
   101→
   102→    # Return parsed Pydantic model directly
   103→    if response.parsed is not None:
   104→        return cast(ExtractionResult, response.parsed)
   105→
   106→    # Fallback to parsing response.text if parsed is None
   107→    text = response.text or ""
   108→    return ExtractionResult.model_validate_json(text)
   109→
   110→
   111→async def _extract_via_gateway(
   112→    pdf_bytes: bytes,
   113→    protocol_id: str,
   114→    title: str,
   115→) -> str:
   116→    """Extract criteria using the unified InferenceGateway (local/Ollama path).
   117→
   118→    Used when LOCAL_EXTRACTION_ENABLED=true. Routes through InferenceGateway
   119→    instead of direct google.genai.Client.
   120→    """
   121→    from inference.gateway import InferenceGateway
   122→
   123→    gateway = InferenceGateway()
   124→
   125→    system_prompt, user_prompt = render_prompts(
   126→        prompts_dir=PROMPTS_DIR,
   127→        system_template="system.jinja2",
   128→        user_template="user.jinja2",
   129→        prompt_vars={"title": title},
   130→    )
   131→
   132→    file_id = await gateway.upload_file(pdf_bytes, f"{protocol_id}.pdf")
   133→    try:
   134→        result = await gateway.generate_structured(
   135→            role="extraction",
   136→            file_id=file_id,
   137→            input_text=user_prompt,
   138→            system_prompt=system_prompt,
   139→            output_schema=ExtractionResult,
   140→        )
   141→        extraction_result = (
   142→            result
   143→            if isinstance(result, ExtractionResult)
   144→            else ExtractionResult.model_validate(result.model_dump())
   145→        )
   146→        logger.info(
   147→            "Extracted %d criteria from protocol %s (gateway)",
   148→            len(extraction_result.criteria),
   149→            protocol_id,
   150→        )
   151→        return extraction_result.model_dump_json()
   152→    finally:
   153→        gateway.cleanup(file_id)
   154→
   155→
   156→async def extract_criteria_structured(
   157→    pdf_bytes: bytes,
   158→    protocol_id: str,
   159→    title: str,
   160→) -> str:
   161→    """Extract criteria from PDF using Gemini File API with structured output.
   162→
   163→    Uploads the PDF to Gemini File API, calls Gemini with ExtractionResult
   164→    as the response schema, and returns the result as a JSON string.
   165→
   166→    When LOCAL_EXTRACTION_ENABLED=true, routes through InferenceGateway
   167→    instead of direct google.genai.Client.
   168→
   169→    Returns JSON string (not dict) to minimize LangGraph state size.
   170→
   171→    Args:
   172→        pdf_bytes: Raw PDF bytes to extract criteria from.
   173→        protocol_id: UUID of the protocol (for logging).
   174→        title: Protocol title (used in user prompt).
   175→
   176→    Returns:
   177→        JSON string representation of ExtractionResult.
   178→
   179→    Raises:
   180→        ValidationError: If Gemini response cannot be parsed as ExtractionResult.
   181→        Exception: On Gemini API or File API errors after retries exhausted.
   182→    """
   183→    # Route through gateway when local extraction is enabled
   184→    if os.getenv("LOCAL_EXTRACTION_ENABLED", "").lower() == "true":
   185→        return await _extract_via_gateway(pdf_bytes, protocol_id, title)
   186→
   187→    tmp_path = None
   188→    uploaded_file = None
   189→    client = None
   190→
   191→    try:
   192→        # Instantiate client
   193→        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
   194→        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
   195→
   196→        # Write PDF to temp file for File API upload
   197→        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
   198→            tmp.write(pdf_bytes)
   199→            tmp_path = tmp.name
   200→
   201→        # Upload via File API
   202→        uploaded_file = client.files.upload(file=tmp_path)
   203→
   204→        system_prompt, user_prompt = render_prompts(
   205→            prompts_dir=PROMPTS_DIR,
   206→            system_template="system.jinja2",
   207→            user_template="user.jinja2",
   208→            prompt_vars={
   209→                "title": title,
   210→            },
   211→        )
   212→
   213→        extraction_result = await _invoke_gemini(
   214→            client, model_name, uploaded_file, system_prompt, user_prompt
   215→        )
   216→
   217→        logger.info(
   218→            "Extracted %d criteria from protocol %s (Gemini File API)",
   219→            len(extraction_result.criteria),
   220→            protocol_id,
   221→        )
   222→
   223→        # Return as JSON string (not dict) for minimal state
   224→        return extraction_result.model_dump_json()
   225→
   226→    except ValidationError as e:
   227→        msg = _format_validation_error(e)
   228→        logger.error(
   229→            "Extraction validation failed for protocol %s: %s",
   230→            protocol_id,
   231→            msg,
   232→        )
   233→        raise
   234→
   235→    except Exception:
   236→        logger.exception(
   237→            "Extraction failed for protocol %s",
   238→            protocol_id,
   239→        )
   240→        raise
   241→
   242→    finally:
   243→        # Clean up temp file
   244→        if tmp_path:
   245→            try:
   246→                os.unlink(tmp_path)
   247→            except Exception as cleanup_err:
   248→                logger.warning(
   249→                    "Failed to delete temp file %s: %s", tmp_path, cleanup_err
   250→                )
   251→
   252→        # Clean up uploaded file
   253→        if uploaded_file and client and uploaded_file.name:
   254→            try:
   255→                client.files.delete(name=uploaded_file.name)
   256→            except Exception as cleanup_err:
   257→                logger.warning(
   258→                    "Failed to delete uploaded file %s: %s",
   259→                    uploaded_file.name,
   260→                    cleanup_err,
   261→                )
   262→
```

> TOOL

tool_use Read
id: toolu_01TPG1Q6RpqQ3qJzxfP1LoAY
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/gemini_utils.py"
}
```

> TOOL

tool_result
id: toolu_01TPG1Q6RpqQ3qJzxfP1LoAY
```
     1→"""Shared Gemini LLM utilities for protocol processor tools.
     2→
     3→Centralizes the repeated pattern of creating a ChatGoogleGenerativeAI
     4→client with structured output and parsing its response. Used by
     5→structure_builder, ordinal_resolver, and field_mapper.
     6→
     7→Falls back to Ollama when GOOGLE_API_KEY is not set but OLLAMA_BASE_URL
     8→is configured.
     9→"""
    10→
    11→from __future__ import annotations
    12→
    13→import logging
    14→import os
    15→from typing import Any, TypeVar
    16→
    17→from pydantic import BaseModel
    18→
    19→logger = logging.getLogger(__name__)
    20→
    21→T = TypeVar("T", bound=BaseModel)
    22→
    23→
    24→def create_structured_llm(
    25→    output_schema: type[T],
    26→) -> Any | None:
    27→    """Create an LLM client with structured output.
    28→
    29→    Tries Gemini first (GOOGLE_API_KEY), falls back to Ollama
    30→    (OLLAMA_BASE_URL) if Gemini is not configured.
    31→
    32→    Args:
    33→        output_schema: Pydantic model class for structured output.
    34→
    35→    Returns:
    36→        A structured LLM instance, or None if no backend is available.
    37→    """
    38→    google_api_key = os.getenv("GOOGLE_API_KEY")
    39→    if google_api_key:
    40→        try:
    41→            from langchain_google_genai import ChatGoogleGenerativeAI
    42→
    43→            gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    44→            gemini = ChatGoogleGenerativeAI(
    45→                model=gemini_model_name,
    46→                google_api_key=google_api_key,
    47→            )
    48→            return gemini.with_structured_output(output_schema)
    49→        except Exception as e:
    50→            logger.warning("Failed to create Gemini client: %s", e)
    51→
    52→    # Fallback to Ollama
    53→    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    54→    if ollama_base_url:
    55→        try:
    56→            from langchain_community.chat_models import ChatOllama
    57→
    58→            ollama_model = os.getenv("OLLAMA_MODEL", "gemma2:9b")
    59→            logger.info(
    60→                "Using Ollama for structured output: %s/%s",
    61→                ollama_base_url,
    62→                ollama_model,
    63→            )
    64→            ollama = ChatOllama(
    65→                base_url=ollama_base_url,
    66→                model=ollama_model,
    67→                format="json",
    68→                temperature=0.1,
    69→            )
    70→            return ollama.with_structured_output(output_schema)
    71→        except Exception as e:
    72→            logger.warning("Failed to create Ollama client: %s", e)
    73→
    74→    logger.warning("No LLM backend available — skipping structured output call")
    75→    return None
    76→
    77→
    78→def parse_structured_output(result: Any, model: type[T]) -> T:
    79→    """Parse a structured LLM output into a Pydantic model.
    80→
    81→    Handles both dict and already-parsed model instances returned
    82→    by LangChain's with_structured_output().
    83→
    84→    Args:
    85→        result: Raw LLM output (dict or model instance).
    86→        model: Pydantic model class to validate against.
    87→
    88→    Returns:
    89→        Validated model instance.
    90→    """
    91→    if isinstance(result, dict):
    92→        return model.model_validate(result)
    93→    return result  # type: ignore[return-value]
    94→
```

> TOOL

tool_use Read
id: toolu_017JVzJzLL5MzSPQXJe5JcvY
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py"
}
```

> TOOL

tool_result
id: toolu_017JVzJzLL5MzSPQXJe5JcvY
```
     1→"""MedGemma decision tool for best-match selection from TerminologyRouter candidates.
     2→
     3→Per user decision: "MedGemma acts as decision-maker, minimum token usage."
     4→MedGemma evaluates candidates returned by TerminologyRouter and selects the best
     5→match for each entity. Uses the two-model architecture: MedGemma for medical
     6→reasoning, Gemini for structured output parsing.
     7→"""
     8→
     9→from __future__ import annotations
    10→
    11→import logging
    12→import os
    13→from typing import TYPE_CHECKING, Any
    14→
    15→if TYPE_CHECKING:
    16→    from protocol_processor.tools.terminology_router import TerminologyRouter
    17→
    18→from langchain_core.messages import HumanMessage, SystemMessage
    19→from langchain_google_genai import ChatGoogleGenerativeAI
    20→from pydantic import BaseModel, Field
    21→
    22→from protocol_processor.schemas.grounding import (
    23→    EntityGroundingResult,
    24→    GroundingCandidate,
    25→)
    26→
    27→logger = logging.getLogger(__name__)
    28→
    29→_model_loader = None
    30→_PROMPTS_DIR = None
    31→
    32→
    33→def _get_prompts_dir():
    34→    from pathlib import Path
    35→
    36→    return Path(__file__).parent.parent / "prompts"
    37→
    38→
    39→def _render_template(template_name: str, **kwargs: Any) -> str:
    40→    """Render a Jinja2 template from the prompts directory."""
    41→    from jinja2 import Environment, FileSystemLoader
    42→
    43→    prompts_dir = _get_prompts_dir()
    44→    env = Environment(loader=FileSystemLoader(str(prompts_dir)), autoescape=False)
    45→    template = env.get_template(template_name)
    46→    return template.render(**kwargs)
    47→
    48→
    49→class AgenticReasoningResult(BaseModel):
    50→    """MedGemma's 3-question reasoning output for failed grounding retry.
    51→
    52→    Used by agentic_reasoning_loop to determine whether to skip an entity,
    53→    apply derived entity mapping, or rephrase the query for a better search.
    54→
    55→    Attributes:
    56→        should_skip: True if entity is not a valid medical criterion.
    57→        is_derived: True if entity maps to a more standard medical concept.
    58→        derived_term: Standard concept term if is_derived is True.
    59→        rephrased_query: Rephrased medical terminology query if applicable.
    60→        gemini_suggestion: Optional additional reformulation from Gemini.
    61→        reasoning: Brief explanation of the reasoning decisions.
    62→    """
    63→
    64→    should_skip: bool = Field(
    65→        default=False,
    66→        description=(
    67→            "True if entity is not a valid medical criterion "
    68→            "(e.g., consent, participation, willingness)"
    69→        ),
    70→    )
    71→    is_derived: bool = Field(
    72→        default=False,
    73→        description="True if entity maps to a more standard medical concept",
    74→    )
    75→    derived_term: str | None = Field(
    76→        default=None,
    77→        description=(
    78→            "Standard concept term if is_derived is True "
    79→            "(e.g., 'age' for 'age >= 18 years')"
    80→        ),
    81→    )
    82→    rephrased_query: str | None = Field(
    83→        default=None,
    84→        description=(
    85→            "Rephrased medical terminology query for better search "
    86→            "(e.g., 'hypertension' for 'high blood pressure')"
    87→        ),
    88→    )
    89→    gemini_suggestion: str | None = Field(
    90→        default=None,
    91→        description=("Optional reformulation suggestion from Gemini structuring step"),
    92→    )
    93→    reasoning: str = Field(
    94→        default="",
    95→        description="Brief explanation of the three-question reasoning",
    96→    )
    97→
    98→
    99→class GroundingDecision(BaseModel):
   100→    """MedGemma's decision for the best terminology match."""
   101→
   102→    selected_code: str | None = Field(
   103→        default=None,
   104→        description=(
   105→            "Selected terminology code (CUI for UMLS, SNOMED code, etc)."
   106→            " Null if no good match."
   107→        ),
   108→    )
   109→    selected_system: str | None = Field(
   110→        default=None,
   111→        description=(
   112→            "The API/system that produced the selected code (e.g. 'umls', 'snomed')."
   113→        ),
   114→    )
   115→    preferred_term: str | None = Field(
   116→        default=None,
   117→        description="Canonical preferred term for the selected code.",
   118→    )
   119→    confidence: float = Field(
   120→        ge=0.0,
   121→        le=1.0,
   122→        description=(
   123→            "Confidence score 0.0-1.0."
   124→            " 0.9-1.0=exact, 0.7-0.8=synonym, 0.5-0.6=partial, 0.0=no match."
   125→        ),
   126→    )
   127→    reasoning: str = Field(
   128→        default="",
   129→        description="Brief explanation for selection.",
   130→    )
   131→
   132→
   133→def _get_medgemma_model() -> Any:
   134→    """Get or create MedGemma model instance."""
   135→    global _model_loader  # noqa: PLW0603
   136→    if _model_loader is None:
   137→        from inference.config import AgentConfig
   138→        from inference.model_garden import create_model_loader
   139→
   140→        _model_loader = create_model_loader(AgentConfig.from_env())
   141→    return _model_loader()
   142→
   143→
   144→async def _structure_decision_with_gemini(raw_text: str) -> GroundingDecision:
   145→    """Structure raw MedGemma output using Gemini with_structured_output.
   146→
   147→    Args:
   148→        raw_text: Raw MedGemma output (free-form medical reasoning).
   149→
   150→    Returns:
   151→        GroundingDecision with selected code and confidence.
   152→    """
   153→    gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
   154→    google_api_key = os.getenv("GOOGLE_API_KEY")
   155→
   156→    if not google_api_key:
   157→        raise ValueError("GOOGLE_API_KEY environment variable is required")
   158→
   159→    gemini = ChatGoogleGenerativeAI(
   160→        model=gemini_model_name,
   161→        google_api_key=google_api_key,
   162→    )
   163→    structured_llm = gemini.with_structured_output(GroundingDecision)
   164→
   165→    prompt = (
   166→        "Extract the grounding decision from this medical terminology analysis."
   167→        " Return the selected code, system, preferred term, confidence,"
   168→        f" and reasoning.\n\n{raw_text}"
   169→    )
   170→
   171→    result = await structured_llm.ainvoke(prompt)
   172→    if isinstance(result, dict):
   173→        return GroundingDecision.model_validate(result)
   174→    return result  # type: ignore[return-value]
   175→
   176→
   177→async def medgemma_decide(
   178→    entity: dict,
   179→    candidates: list[GroundingCandidate],
   180→    criterion_context: str,
   181→) -> EntityGroundingResult:
   182→    """Use MedGemma to select the best terminology match for an entity.
   183→
   184→    MedGemma evaluates the candidates returned by TerminologyRouter and
   185→    selects the most appropriate code for the entity. Returns a result with
   186→    confidence=0.0 and no code if no candidates are available or none are
   187→    appropriate.
   188→
   189→    Args:
   190→        entity: Entity dict with keys: text, entity_type, criterion_id.
   191→        candidates: List of GroundingCandidate objects from TerminologyRouter.
   192→        criterion_context: The full criterion text for context.
   193→
   194→    Returns:
   195→        EntityGroundingResult with the selected code, confidence, and reasoning.
   196→    """
   197→    entity_text = entity.get("text", "")
   198→    entity_type = entity.get("entity_type", "")
   199→    criterion_id = entity.get("criterion_id", "")
   200→
   201→    # If no candidates, return result with confidence=0.0
   202→    if not candidates:
   203→        logger.info(
   204→            "No candidates for entity '%s' (type=%s, criterion=%s)"
   205→            " — returning empty grounding",
   206→            entity_text[:50],
   207→            entity_type,
   208→            criterion_id[:12],
   209→        )
   210→        return EntityGroundingResult(
   211→            entity_text=entity_text,
   212→            entity_type=entity_type,
   213→            selected_code=None,
   214→            selected_system=None,
   215→            preferred_term=None,
   216→            confidence=0.0,
   217→            candidates=[],
   218→            reasoning="No terminology candidates available from any API",
   219→        )
   220→
   221→    try:
   222→        model = _get_medgemma_model()
   223→
   224→        system_prompt = _render_template("grounding_system.jinja2")
   225→        evaluate_prompt = _render_template(
   226→            "grounding_evaluate.jinja2",
   227→            entity_text=entity_text,
   228→            entity_type=entity_type,
   229→            criterion_context=criterion_context,
   230→            candidates=candidates,
   231→        )
   232→
   233→        messages = [
   234→            SystemMessage(content=system_prompt),
   235→            HumanMessage(content=evaluate_prompt),
   236→        ]
   237→        raw_response = await model.ainvoke(messages)
   238→        raw_text = raw_response.content
   239→
   240→        logger.debug(
   241→            "MedGemma evaluate response for '%s' (first 200 chars): %s",
   242→            entity_text[:30],
   243→            raw_text[:200],
   244→        )
   245→
   246→        decision = await _structure_decision_with_gemini(raw_text)
   247→
   248→        logger.info(
   249→            "Grounding decision for '%s': code=%s, system=%s, conf=%.2f",
   250→            entity_text[:50],
   251→            decision.selected_code,
   252→            decision.selected_system,
   253→            decision.confidence,
   254→        )
   255→
   256→        return EntityGroundingResult(
   257→            entity_text=entity_text,
   258→            entity_type=entity_type,
   259→            selected_code=decision.selected_code,
   260→            selected_system=decision.selected_system,
   261→            preferred_term=decision.preferred_term,
   262→            confidence=decision.confidence,
   263→            candidates=candidates,
   264→            reasoning=decision.reasoning,
   265→        )
   266→
   267→    except Exception as e:
   268→        logger.error(
   269→            "MedGemma decision failed for entity '%s': %s",
   270→            entity_text[:50],
   271→            e,
   272→            exc_info=True,
   273→        )
   274→        return EntityGroundingResult(
   275→            entity_text=entity_text,
   276→            entity_type=entity_type,
   277→            selected_code=None,
   278→            selected_system=None,
   279→            preferred_term=None,
   280→            confidence=0.0,
   281→            candidates=candidates,
   282→            reasoning=f"MedGemma decision failed: {e}",
   283→        )
   284→
   285→
   286→async def _structure_reasoning_with_gemini(raw_text: str) -> AgenticReasoningResult:
   287→    """Structure raw MedGemma reasoning output using Gemini with_structured_output.
   288→
   289→    Gemini also acts as a collaborating agent here — it can add its own
   290→    reformulation suggestions via the gemini_suggestion field when structuring
   291→    the output.
   292→
   293→    Args:
   294→        raw_text: Raw MedGemma reasoning output (free-form text).
   295→
   296→    Returns:
   297→        AgenticReasoningResult with structured 3-question answers.
   298→    """
   299→    gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
   300→    google_api_key = os.getenv("GOOGLE_API_KEY")
   301→
   302→    if not google_api_key:
   303→        raise ValueError("GOOGLE_API_KEY environment variable is required")
   304→
   305→    gemini = ChatGoogleGenerativeAI(
   306→        model=gemini_model_name,
   307→        google_api_key=google_api_key,
   308→    )
   309→    structured_llm = gemini.with_structured_output(AgenticReasoningResult)
   310→
   311→    prompt = (
   312→        "Extract the structured reasoning from this medical entity analysis. "
   313→        "Determine: (1) should_skip if entity is not a valid medical criterion, "
   314→        "(2) is_derived and derived_term if entity maps to a standard concept, "
   315→        "(3) rephrased_query if a better medical term would improve search. "
   316→        "You may also add a gemini_suggestion with your own reformulation if "
   317→        "you can improve on the analysis.\n\n"
   318→        f"{raw_text}"
   319→    )
   320→
   321→    result = await structured_llm.ainvoke(prompt)
   322→    if isinstance(result, dict):
   323→        return AgenticReasoningResult.model_validate(result)
   324→    return result  # type: ignore[return-value]
   325→
   326→
   327→async def agentic_reasoning_loop(
   328→    entity: dict,
   329→    criterion_context: str,
   330→    router: "TerminologyRouter",
   331→    attempt: int = 1,
   332→) -> AgenticReasoningResult:
   333→    """Ask MedGemma 3 reasoning questions to determine retry strategy.
   334→
   335→    Called by ground_node when an entity fails initial grounding (zero
   336→    candidates or confidence < 0.5). Asks MedGemma in a single prompt:
   337→    - Q1: Is this a valid medical criterion (or should it be skipped)?
   338→    - Q2: Is this a derived entity that maps to a standard concept?
   339→    - Q3: Can this entity be rephrased for better terminology search?
   340→
   341→    Uses the two-model architecture: MedGemma for medical reasoning, Gemini
   342→    for structured output parsing (and optional reformulation suggestion).
   343→
   344→    Args:
   345→        entity: Entity dict with keys: text, entity_type, criterion_id.
   346→        criterion_context: The full criterion text for context.
   347→        router: TerminologyRouter instance (for get_apis_for_entity context).
   348→        attempt: Current attempt number (1-3) for prompt context.
   349→
   350→    Returns:
   351→        AgenticReasoningResult with should_skip, is_derived, derived_term,
   352→        rephrased_query, gemini_suggestion, and reasoning fields.
   353→        On error, returns default result (no skip, no rephrase) to allow
   354→        the retry loop to continue with the original query.
   355→    """
   356→    entity_text = entity.get("text", "")
   357→    entity_type = entity.get("entity_type", "")
   358→    previous_query = entity.get("_previous_query", entity_text)
   359→
   360→    logger.info(
   361→        "Agentic reasoning (attempt %d) for entity '%s' (type=%s)",
   362→        attempt,
   363→        entity_text[:50],
   364→        entity_type,
   365→    )
   366→
   367→    try:
   368→        model = _get_medgemma_model()
   369→
   370→        system_prompt = _render_template("grounding_system.jinja2")
   371→        reasoning_prompt = _render_template(
   372→            "grounding_reasoning.jinja2",
   373→            entity_text=entity_text,
   374→            entity_type=entity_type,
   375→            criterion_context=criterion_context,
   376→            previous_query=previous_query,
   377→            attempt=attempt,
   378→        )
   379→
   380→        messages = [
   381→            SystemMessage(content=system_prompt),
   382→            HumanMessage(content=reasoning_prompt),
   383→        ]
   384→        raw_response = await model.ainvoke(messages)
   385→        raw_text = raw_response.content
   386→
   387→        logger.debug(
   388→            "MedGemma reasoning response for '%s' (first 300 chars): %s",
   389→            entity_text[:30],
   390→            raw_text[:300],
   391→        )
   392→
   393→        result = await _structure_reasoning_with_gemini(raw_text)
   394→
   395→        logger.info(
   396→            "Agentic reasoning result for '%s': skip=%s, derived=%s, "
   397→            "derived_term=%s, rephrased=%s",
   398→            entity_text[:50],
   399→            result.should_skip,
   400→            result.is_derived,
   401→            result.derived_term,
   402→            result.rephrased_query,
   403→        )
   404→
   405→        return result
   406→
   407→    except Exception as e:
   408→        logger.error(
   409→            "Agentic reasoning loop failed for entity '%s': %s",
   410→            entity_text[:50],
   411→            e,
   412→            exc_info=True,
   413→        )
   414→        # Return default result (no skip, no rephrase) — retry with original query
   415→        return AgenticReasoningResult(
   416→            should_skip=False,
   417→            is_derived=False,
   418→            derived_term=None,
   419→            rephrased_query=None,
   420→            reasoning=f"Reasoning loop failed: {e}",
   421→        )
   422→
```

> TOOL

tool_use Read
id: toolu_01Nd5qqgiSVvPgXtwU5whAYM
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py"
}
```

> TOOL

tool_result
id: toolu_01Nd5qqgiSVvPgXtwU5whAYM
```
     1→"""Entity decomposition: extract discrete medical entities from criteria.
     2→
     3→Criterion sentences like "eGFR >= 30 mL/min/1.73m2 or sCr <= 2.0 mg/dL" contain
     4→multiple groundable medical concepts. This tool decomposes them into discrete
     5→entities with correct types for TerminologyRouter dispatch.
     6→
     7→Uses the two-model architecture pattern: Gemini for structured output via
     8→LangChain's with_structured_output, matching the medgemma_decider.py pattern.
     9→"""
    10→
    11→from __future__ import annotations
    12→
    13→import logging
    14→import os
    15→from pathlib import Path
    16→from typing import Literal, cast
    17→
    18→from jinja2 import Environment, FileSystemLoader
    19→from langchain_google_genai import ChatGoogleGenerativeAI
    20→from pydantic import BaseModel, Field
    21→
    22→logger = logging.getLogger(__name__)
    23→
    24→PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
    25→
    26→
    27→class DecomposedEntity(BaseModel):
    28→    """A single medical entity extracted from a criterion sentence.
    29→
    30→    Attributes:
    31→        text: The specific medical term to ground (e.g. "eGFR", not the full sentence).
    32→        entity_type: Entity type matching routing.yaml keys exactly.
    33→    """
    34→
    35→    text: str = Field(description="The specific medical term to ground")
    36→    entity_type: Literal[
    37→        "Condition", "Medication", "Lab_Value", "Procedure", "Demographic", "Other"
    38→    ] = Field(description="Entity type for terminology routing")
    39→
    40→
    41→class DecomposedEntityList(BaseModel):
    42→    """List of decomposed entities from a single criterion sentence."""
    43→
    44→    entities: list[DecomposedEntity] = Field(default_factory=list)
    45→
    46→
    47→def _render_decompose_prompt(criterion_text: str, category: str | None) -> str:
    48→    """Render the entity decomposition Jinja2 prompt template.
    49→
    50→    Args:
    51→        criterion_text: Full criterion sentence to decompose.
    52→        category: Optional category hint from extraction (e.g. "lab_values").
    53→
    54→    Returns:
    55→        Rendered prompt string for Gemini.
    56→    """
    57→    env = Environment(loader=FileSystemLoader(str(PROMPTS_DIR)), autoescape=False)
    58→    template = env.get_template("entity_decompose.jinja2")
    59→    return template.render(criterion_text=criterion_text, category=category or "")
    60→
    61→
    62→async def decompose_entities_from_criterion(
    63→    criterion_text: str,
    64→    category: str | None,
    65→) -> list[dict]:
    66→    """Extract discrete medical entities from a criterion sentence.
    67→
    68→    Uses Gemini with structured output to decompose a criterion sentence
    69→    into individual medical terms with correct entity types. Falls back
    70→    to empty list on failure -- caller handles fallback to full-text entity.
    71→
    72→    Args:
    73→        criterion_text: The full criterion sentence to decompose.
    74→        category: Optional category hint from extraction.
    75→
    76→    Returns:
    77→        List of dicts with "text" and "entity_type" keys, or empty list on failure.
    78→    """
    79→    try:
    80→        gemini = ChatGoogleGenerativeAI(
    81→            model=os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash"),
    82→            google_api_key=os.getenv("GOOGLE_API_KEY"),
    83→        )
    84→        structured = gemini.with_structured_output(DecomposedEntityList)
    85→        prompt = _render_decompose_prompt(criterion_text, category)
    86→        result = await structured.ainvoke(prompt)
    87→        if isinstance(result, dict):
    88→            result = DecomposedEntityList.model_validate(result)
    89→        decomposed = cast(DecomposedEntityList, result)
    90→        return [e.model_dump() for e in decomposed.entities]
    91→    except Exception as e:
    92→        logger.error(
    93→            "Entity decomposition failed for criterion '%s': %s",
    94→            criterion_text[:80],
    95→            e,
    96→        )
    97→        return []  # Caller falls back to full-text entity
    98→
```

> TOOL

tool_use Read
id: toolu_019Ux86UQ7JbvfcTaSmgy32e
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py"
}
```

> TOOL

tool_result
id: toolu_019Ux86UQ7JbvfcTaSmgy32e
```
     1→"""Field mapping generation tool for grounded entities.
     2→
     3→Per user decision: "Generate suggested field_mappings during grounding (ground node)"
     4→Per CONTEXT.md: "Criteria should be decomposed per AutoCriteria pattern: separate
     5→Entity, Operator, Value, Unit, Time"
     6→Per user decision: "MedGemma and Gemini collaborate: Gemini uses MedGemma as
     7→medical expert"
     8→
     9→Uses Gemini to generate suggested field mappings for the grounded entity +
    10→criterion text. These are best-effort suggestions — reviewer can edit in UI.
    11→"""
    12→
    13→from __future__ import annotations
    14→
    15→import logging
    16→from typing import Any, Literal
    17→
    18→from pydantic import BaseModel, Field, field_validator
    19→
    20→from protocol_processor.schemas.grounding import EntityGroundingResult
    21→from protocol_processor.tools.gemini_utils import (
    22→    create_structured_llm,
    23→    parse_structured_output,
    24→)
    25→
    26→logger = logging.getLogger(__name__)
    27→
    28→# Mapping from legacy/LLM relation operators to the frontend's RelationOperator set
    29→_RELATION_MAP: dict[str, str] = {
    30→    "has": "contains",
    31→    "is": "=",
    32→    "not": "not_contains",
    33→    "==": "=",
    34→    "range": "within",
    35→}
    36→
    37→
    38→def _normalize_relation(rel: str) -> str:
    39→    """Normalize a relation operator to the frontend's accepted set.
    40→
    41→    Maps legacy operators (has, is, not, ==, range) to the standard set:
    42→    =, !=, >, >=, <, <=, within, not_in_last, contains, not_contains.
    43→    """
    44→    return _RELATION_MAP.get(rel, rel)
    45→
    46→
    47→class FieldMappingValue(BaseModel):
    48→    """Typed value object for field mappings with type discriminator.
    49→
    50→    Supports three value shapes:
    51→    - standard: single value + unit (e.g. HbA1c < 7%)
    52→    - range: min/max + unit (e.g. Age 18-65 years)
    53→    - temporal: duration + unit (e.g. within 6 months)
    54→    """
    55→
    56→    type: Literal["standard", "range", "temporal"] = Field(
    57→        description="Value type discriminator"
    58→    )
    59→    value: str | None = Field(
    60→        default=None, description="Value for standard type (e.g. '7')"
    61→    )
    62→    unit: str | None = Field(
    63→        default=None, description="Unit of measurement (e.g. '%', 'mg/dL', 'months')"
    64→    )
    65→    min: str | None = Field(default=None, description="Minimum value for range type")
    66→    max: str | None = Field(default=None, description="Maximum value for range type")
    67→    duration: str | None = Field(
    68→        default=None, description="Duration value for temporal type"
    69→    )
    70→
    71→
    72→# The set of valid relation operators accepted by the frontend
    73→RelationOperator = Literal[
    74→    "=", "!=", ">", ">=", "<", "<=", "within", "not_in_last", "contains", "not_contains"
    75→]
    76→
    77→
    78→class FieldMappingItem(BaseModel):
    79→    """A single AutoCriteria field mapping decomposition.
    80→
    81→    Per the AutoCriteria pattern, each criterion is decomposed into
    82→    separate Entity, Operator, Value, Unit, and Time components.
    83→    """
    84→
    85→    entity: str = Field(description="The medical entity name (e.g. 'HbA1c')")
    86→    relation: RelationOperator = Field(
    87→        description="The logical operator/relation (e.g. '<', '>', '=', 'contains')"
    88→    )
    89→    value: FieldMappingValue = Field(
    90→        description="Typed value object with type discriminator"
    91→    )
    92→    unit: str | None = Field(
    93→        default=None,
    94→        description="Optional unit of measurement (e.g. '%', 'mg/dL', 'years')",
    95→    )
    96→    value_concept_id: str | None = Field(
    97→        default=None,
    98→        description="OMOP concept ID for categorical values",
    99→    )
   100→    value_concept_system: str | None = Field(
   101→        default=None,
   102→        description="Terminology system for value_concept_id (e.g. 'SNOMED', 'OMOP')",
   103→    )
   104→
   105→    @field_validator("relation", mode="before")
   106→    @classmethod
   107→    def normalize_relation(cls, v: str) -> str:
   108→        """Normalize LLM-generated relation operators before Literal validation."""
   109→        if isinstance(v, str):
   110→            return _normalize_relation(v)
   111→        return v
   112→
   113→
   114→class FieldMappingResponse(BaseModel):
   115→    """Gemini structured output for field mappings."""
   116→
   117→    mappings: list[FieldMappingItem] = Field(
   118→        default_factory=list,
   119→        description="List of AutoCriteria field mapping decompositions",
   120→    )
   121→
   122→
   123→async def generate_field_mappings(
   124→    entity: EntityGroundingResult,
   125→    criterion_text: str,
   126→) -> list[dict[str, Any]]:
   127→    """Generate suggested field mappings for a grounded entity.
   128→
   129→    Uses Gemini to decompose the criterion text into AutoCriteria field mappings:
   130→    Entity, Operator, Value, Unit, Time components for each discrete condition.
   131→
   132→    This is a best-effort suggestion — reviewer can edit in the UI. Errors
   133→    are logged and an empty list returned (not propagated as failures).
   134→
   135→    Args:
   136→        entity: Grounded EntityGroundingResult with code and preferred term.
   137→        criterion_text: Full criterion text for context.
   138→
   139→    Returns:
   140→        List of field mapping dicts with keys: entity, relation, value,
   141→        entity_code, entity_system, omop_concept_id, entity_type.
   142→        Empty list if generation fails.
   143→    """
   144→    if not criterion_text:
   145→        return []
   146→
   147→    structured_llm = create_structured_llm(FieldMappingResponse)
   148→    if structured_llm is None:
   149→        return []
   150→
   151→    try:
   152→        # Build a context-rich prompt for field mapping generation
   153→        grounded_term = entity.preferred_term or entity.entity_text
   154→        code_context = ""
   155→        if entity.selected_code and entity.selected_system:
   156→            system = entity.selected_system.upper()
   157→            code_context = f"(grounded to {system} code: {entity.selected_code})"
   158→
   159→        prompt = (
   160→            "You are a clinical trial protocol analyst. Decompose the"
   161→            " following criterion into structured AutoCriteria field"
   162→            " mappings using the Entity-Relation-Value-Unit pattern.\n\n"
   163→            f"Medical entity: {grounded_term} {code_context}\n"
   164→            f"Criterion text: {criterion_text}\n\n"
   165→            "Instructions:\n"
   166→            "- Extract each discrete measurement, threshold, or condition"
   167→            " as a separate mapping\n"
   168→            "- entity: the specific measurement or concept"
   169→            " (e.g. 'HbA1c', 'Age', 'eGFR')\n"
   170→            "- relation: MUST be one of: =, !=, >, >=, <, <=, within,"
   171→            " not_in_last, contains, not_contains\n"
   172→            '- value: a typed object with a "type" discriminator:\n'
   173→            '  - Standard: {"type": "standard", "value": "7", "unit": "%"}\n'
   174→            '  - Range: {"type": "range", "min": "18", "max": "65",'
   175→            ' "unit": "years"}\n'
   176→            '  - Temporal: {"type": "temporal", "duration": "6",'
   177→            ' "unit": "months"}\n'
   178→            "- Create one mapping per discrete condition in the criterion\n"
   179→            "- If no clear measurement exists, create one mapping with"
   180→            " relation='contains',"
   181→            ' value={"type": "standard", "value": "confirmed", "unit": ""}'
   182→        )
   183→
   184→        result = await structured_llm.ainvoke(prompt)
   185→        response = parse_structured_output(result, FieldMappingResponse)
   186→
   187→        mappings = [
   188→            {
   189→                "entity": m.entity,
   190→                "relation": m.relation,
   191→                "value": m.value.model_dump(exclude_none=True),
   192→                "entity_code": entity.selected_code,
   193→                "entity_system": entity.selected_system,
   194→                "omop_concept_id": entity.omop_concept_id,
   195→                "entity_type": entity.entity_type,
   196→                "value_concept_id": m.value_concept_id,
   197→                "value_concept_system": m.value_concept_system,
   198→            }
   199→            for m in response.mappings
   200→        ]
   201→
   202→        logger.info(
   203→            "Generated %d field mapping(s) for entity '%s'",
   204→            len(mappings),
   205→            entity.entity_text[:50],
   206→        )
   207→        return mappings
   208→
   209→    except Exception as e:
   210→        logger.warning(
   211→            "Field mapping generation failed for entity '%s': %s",
   212→            entity.entity_text[:50],
   213→            e,
   214→            exc_info=True,
   215→        )
   216→        # Best-effort: return empty list on failure
   217→        return []
   218→
```

> AGENT

Now let me check the existing tests for tracing patterns.

> TOOL

tool_use Glob
id: toolu_01XxMhURCF6A1ggSqk4dDhSq
```json
{
  "pattern": "**/test*trac*"
}
```

> TOOL

tool_use Glob
id: toolu_01VVDEqjYuwZxKTSUngWAQBG
```json
{
  "pattern": "**/test*mlflow*"
}
```

> TOOL

tool_result
id: toolu_01XxMhURCF6A1ggSqk4dDhSq
```
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/sympy/codegen/tests/test_abstract_nodes.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/networkx/algorithms/components/tests/test_attracting.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/networkx/algorithms/minors/tests/test_contraction.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/sympy/matrices/expressions/tests/test_trace.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/sympy/physics/quantum/tests/test_trace.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/__pycache__/test_sentence_extraction.cpython-312-pytest-9.0.2.pyc
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/greenlet/tests/test_tracing.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/torch/_dynamo/test_dont_skip_tracing_functions.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/pandas/tests/strings/test_extract.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/numpy/f2py/tests/test_abstract_interface.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/pandas/tests/construction/test_extract_array.py
/Users/noahdolevelixir/Code/medgemma-hackathon/.venv/lib/python3.13/site-packages/scipy/sparse/tests/test_extract.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_sentence_extraction.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/__pycache__/test_sentence_extraction.cpython-313-pytest-9.0.2.pyc
```

> TOOL

tool_result
id: toolu_01VVDEqjYuwZxKTSUngWAQBG
```
No files found
```

> TOOL

tool_use Glob
id: toolu_01Gt7647hhK9hyBNSzL43Tq7
```json
{
  "pattern": "services/protocol-processor-service/tests/**/*.py"
}
```

> TOOL

tool_result
id: toolu_01Gt7647hhK9hyBNSzL43Tq7
```
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/__init__.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/conftest.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_graph.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_ordinal_resolve.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_phase2_structure.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_sentence_extraction.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_terminology_router.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_phase1b_wiring.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/tools/__init__.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/tools/test_field_mapper_format.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_omop_mapper.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_grounding_fixes.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_unit_normalizer.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_phase3b_e2e.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_ordinal_full_cycle.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_phase2_e2e.py
/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/tests/test_phase3_integration.py
```

> AGENT

Now I have a complete picture. Let me design the approach and write the plan.

> TOOL

tool_use Read
id: toolu_01KvUi2rCRyJNYRMx9NE5uwV
```json
{
  "file_path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/nodes/extract.py"
}
```

> TOOL

tool_result
id: toolu_01KvUi2rCRyJNYRMx9NE5uwV
```
     1→"""Extract node: call Gemini with structured output for criteria extraction.
     2→
     3→Thin orchestration node — delegates all LLM logic to the gemini_extractor tool.
     4→Returns extraction_json as a JSON string to minimize LangGraph state size.
     5→"""
     6→
     7→from __future__ import annotations
     8→
     9→import logging
    10→from typing import Any
    11→
    12→from protocol_processor.state import PipelineState
    13→from protocol_processor.tools.gemini_extractor import extract_criteria_structured
    14→from protocol_processor.tracing import pipeline_span
    15→
    16→logger = logging.getLogger(__name__)
    17→
    18→
    19→async def extract_node(state: PipelineState) -> dict[str, Any]:
    20→    """Extract structured criteria from PDF using Gemini File API.
    21→
    22→    Delegates to extract_criteria_structured tool. Returns a JSON string
    23→    (not dict) to minimize LangGraph state overhead.
    24→
    25→    Args:
    26→        state: Current pipeline state with pdf_bytes, protocol_id, and title.
    27→
    28→    Returns:
    29→        Dict with extraction_json (JSON string), or error dict on failure.
    30→    """
    31→    if state.get("error"):
    32→        return {}
    33→
    34→    protocol_id = state.get("protocol_id", "")
    35→    with pipeline_span(
    36→        "extract_node", span_type="LLM", protocol_id=protocol_id
    37→    ) as span:
    38→        span.set_inputs(
    39→            {
    40→                "protocol_id": state.get("protocol_id", ""),
    41→                "title": state.get("title", ""),
    42→                "pdf_bytes_len": len(state.get("pdf_bytes") or b""),
    43→            }
    44→        )
    45→
    46→        try:
    47→            extraction_json = await extract_criteria_structured(
    48→                pdf_bytes=state["pdf_bytes"],  # type: ignore[arg-type]
    49→                protocol_id=state["protocol_id"],
    50→                title=state["title"],
    51→            )
    52→
    53→            logger.info(
    54→                "Extraction complete for protocol %s",
    55→                state["protocol_id"],
    56→            )
    57→            span.set_outputs(
    58→                {
    59→                    "extraction_json_len": len(extraction_json)
    60→                    if extraction_json
    61→                    else 0,
    62→                }
    63→            )
    64→            return {"extraction_json": extraction_json, "pdf_bytes": None}
    65→
    66→        except Exception as e:
    67→            logger.exception(
    68→                "Extraction failed for protocol %s: %s",
    69→                state.get("protocol_id", "unknown"),
    70→                e,
    71→            )
    72→            span.set_outputs({"error": str(e)})
    73→            return {"error": f"Extraction failed: {e}"}
    74→
```

> AGENT

Now I have everything I need. Let me write the plan.

> TOOL

tool_use Write
id: toolu_01RyghXVMfPxFhoYgXNYKWjh
```json
{
  "file_path": "/Users/noahdolevelixir/.claude-elixirtrials/plans/rippling-squishing-clock.md",
  "content": "# Plan: Add LLM-level tracing to MLflow pipeline spans\n\n## Context\n\nMLflow traces currently show only high-level node I/O (e.g. `protocol_id`, `extraction_json_len`) but contain zero detail about the actual LLM calls — no prompts, responses, token counts, or model names. The `pipeline_span()` context manager creates one flat span per node. Since MLflow 3.x automatically nests `start_span()` calls, any `mlflow.start_span()` invoked inside an existing `pipeline_span()` will automatically become a child span. This means we can add instrumentation at the tool level without changing the node or tracing architecture.\n\n## Approach: Add a reusable `llm_span()` context manager to `tracing.py`\n\nCreate a lightweight `llm_span()` helper (sibling to `pipeline_span()`) that wraps individual LLM calls. When called inside a `pipeline_span()`, it automatically becomes a child span. When MLflow is unavailable, it's a no-op. Apply it to each LLM call site in the tool modules.\n\n## Files to modify\n\n### 1. `services/protocol-processor-service/src/protocol_processor/tracing.py`\n- Add `llm_span(name, model_name, span_type=\"LLM\")` context manager\n- It creates a child span inside the current trace, logging:\n  - **Inputs**: `model`, `prompt` (truncated to 10k chars), `prompt_tokens` (if available)\n  - **Outputs**: `response` (truncated to 10k chars), `input_tokens`, `output_tokens`, `total_tokens`\n- Falls back to `_NoOpLLMSpan` when MLflow unavailable\n- The yielded object has `set_request(model, prompt_text)` and `set_response(response_text, usage_metadata=None)` helpers\n\n### 2. `services/protocol-processor-service/src/protocol_processor/tools/gemini_extractor.py`\n- Wrap `_invoke_gemini()` body with `llm_span(\"gemini_extraction\", model)`\n- Log: system_prompt + user_prompt as input, response.text as output\n- Extract `response.usage_metadata` for token counts (google.genai provides `prompt_token_count`, `candidates_token_count`, `total_token_count`)\n\n### 3. `services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py`\n- `medgemma_decide()`: wrap `model.ainvoke(messages)` with `llm_span(\"medgemma_evaluate\", model_name)`\n- `_structure_decision_with_gemini()`: wrap `structured_llm.ainvoke(prompt)` with `llm_span(\"gemini_structure_decision\", model_name)`\n- `agentic_reasoning_loop()`: wrap `model.ainvoke(messages)` with `llm_span(\"medgemma_reasoning\", model_name)`\n- `_structure_reasoning_with_gemini()`: wrap `structured_llm.ainvoke(prompt)` with `llm_span(\"gemini_structure_reasoning\", model_name)`\n- For LangChain responses: extract token counts from `raw_response.usage_metadata` or `raw_response.response_metadata`\n\n### 4. `services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py`\n- Wrap `structured.ainvoke(prompt)` in `decompose_entities_from_criterion()` with `llm_span(\"gemini_entity_decompose\", model_name)`\n\n### 5. `services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py`\n- Wrap `structured_llm.ainvoke(prompt)` in `generate_field_mappings()` with `llm_span(\"gemini_field_mapping\")`\n\n### 6. `services/protocol-processor-service/src/protocol_processor/tools/gemini_utils.py`\n- No changes needed — `create_structured_llm()` is a factory, instrumentation belongs at call sites\n\n### 7. Tool files using `create_structured_llm` (via grep: structure_builder.py, ordinal_resolver.py)\n- Wrap their `structured_llm.ainvoke(prompt)` calls similarly\n\n## `llm_span()` design\n\n```python\n@contextmanager\ndef llm_span(name: str, model_name: str = \"\"):\n    \"\"\"Create an MLflow child span for an individual LLM call.\"\"\"\n    # Inside existing pipeline_span → auto-nests as child\n    # No pipeline_span active → creates independent trace (still useful)\n    try:\n        import mlflow\n        if os.getenv(\"MLFLOW_TRACKING_URI\"):\n            with mlflow.start_span(name=name, span_type=\"LLM\") as span:\n                ctx = _LLMSpanCtx(span, model_name)\n                yield ctx\n                ctx._finalize()\n                return\n    except ImportError: ...\n    except Exception: ...\n    yield _NoOpLLMSpan()\n```\n\nThe `_LLMSpanCtx` object exposes:\n- `set_request(prompt_text)` — logs prompt + model to span inputs\n- `set_response(response_text, usage=None)` — logs response + tokens to span outputs\n\n## Verification\n\n1. `uv run ruff check .` — passes\n2. `uv run mypy services/protocol-processor-service` — passes\n3. `uv run pytest services/protocol-processor-service/tests/ -x` — passes\n4. Smoke test script (not committed): triggers a pipeline run and queries MLflow to verify child spans appear with prompt/response/token data inside node traces\n"
}
```

> TOOL

tool_result
id: toolu_01RyghXVMfPxFhoYgXNYKWjh
```
File created successfully at: /Users/noahdolevelixir/.claude-elixirtrials/plans/rippling-squishing-clock.md
```

> AGENT

I need to also check the structure_builder and ordinal_resolver files for their LLM call sites.

> TOOL

tool_use Grep
id: toolu_01Efr35jdHpPzaKejymtdBK5
```json
{
  "pattern": "structured_llm\\.ainvoke|structured\\.ainvoke",
  "path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01Efr35jdHpPzaKejymtdBK5
```
services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py:171:    result = await structured_llm.ainvoke(prompt)
services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py:321:    result = await structured_llm.ainvoke(prompt)
services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py:86:        result = await structured.ainvoke(prompt)
services/protocol-processor-service/src/protocol_processor/tools/ordinal_resolver.py:87:        result = await structured_llm.ainvoke(prompt)
services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py:184:        result = await structured_llm.ainvoke(prompt)
services/protocol-processor-service/src/protocol_processor/tools/structure_builder.py:161:        result = await structured_llm.ainvoke(prompt)
```

> AGENT

Good — 6 LangChain `.ainvoke()` call sites plus 1 `google.genai` call site. Let me also check how MedGemma model name is accessible.

> TOOL

tool_use Grep
id: toolu_01Ti4EiLi41aM35SDNs9VMxU
```json
{
  "pattern": "MEDGEMMA_MODEL|model_name|GEMINI_MODEL_NAME",
  "path": "/Users/noahdolevelixir/Code/medgemma-hackathon/services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01Ti4EiLi41aM35SDNs9VMxU
```
153:    gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
160:        model=gemini_model_name,
299:    gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
306:        model=gemini_model_name,
```

> TOOL

tool_use Grep
id: toolu_016X9kkvZ39ncXfzCseRaFnZ
```json
{
  "pattern": "MEDGEMMA_MODEL|model_id|model_name",
  "path": "/Users/noahdolevelixir/Code/medgemma-hackathon/libs/inference/src/inference/config.py",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_016X9kkvZ39ncXfzCseRaFnZ
```
24:        vertex_model_name: Vertex model name (optional alternative to endpoint).
35:    vertex_model_name: str = ""
46:        return bool(self.vertex_model_name)
67:            model_path=os.getenv("MEDGEMMA_MODEL_PATH", cls.model_path),
73:            vertex_model_name=os.getenv("VERTEX_MODEL_NAME", cls.vertex_model_name),
```

> AGENT

I have all the information needed. The plan is complete and covers all call sites. Let me finalize it.

> TOOL

tool_use ExitPlanMode
id: toolu_01CLyChKF8oaj6TuKatTtqpM
```json
{
  "allowedPrompts": [
    {
      "tool": "Bash",
      "prompt": "run ruff check"
    },
    {
      "tool": "Bash",
      "prompt": "run mypy"
    },
    {
      "tool": "Bash",
      "prompt": "run pytest"
    },
    {
      "tool": "Bash",
      "prompt": "run smoke test script"
    }
  ],
  "plan": "# Plan: Add LLM-level tracing to MLflow pipeline spans\n\n## Context\n\nMLflow traces currently show only high-level node I/O (e.g. `protocol_id`, `extraction_json_len`) but contain zero detail about the actual LLM calls — no prompts, responses, token counts, or model names. The `pipeline_span()` context manager creates one flat span per node. Since MLflow 3.x automatically nests `start_span()` calls, any `mlflow.start_span()` invoked inside an existing `pipeline_span()` will automatically become a child span. This means we can add instrumentation at the tool level without changing the node or tracing architecture.\n\n## Approach: Add a reusable `llm_span()` context manager to `tracing.py`\n\nCreate a lightweight `llm_span()` helper (sibling to `pipeline_span()`) that wraps individual LLM calls. When called inside a `pipeline_span()`, it automatically becomes a child span. When MLflow is unavailable, it's a no-op. Apply it to each LLM call site in the tool modules.\n\n## Files to modify\n\n### 1. `services/protocol-processor-service/src/protocol_processor/tracing.py`\n- Add `llm_span(name, model_name, span_type=\"LLM\")` context manager\n- It creates a child span inside the current trace, logging:\n  - **Inputs**: `model`, `prompt` (truncated to 10k chars), `prompt_tokens` (if available)\n  - **Outputs**: `response` (truncated to 10k chars), `input_tokens`, `output_tokens`, `total_tokens`\n- Falls back to `_NoOpLLMSpan` when MLflow unavailable\n- The yielded object has `set_request(model, prompt_text)` and `set_response(response_text, usage_metadata=None)` helpers\n\n### 2. `services/protocol-processor-service/src/protocol_processor/tools/gemini_extractor.py`\n- Wrap `_invoke_gemini()` body with `llm_span(\"gemini_extraction\", model)`\n- Log: system_prompt + user_prompt as input, response.text as output\n- Extract `response.usage_metadata` for token counts (google.genai provides `prompt_token_count`, `candidates_token_count`, `total_token_count`)\n\n### 3. `services/protocol-processor-service/src/protocol_processor/tools/medgemma_decider.py`\n- `medgemma_decide()`: wrap `model.ainvoke(messages)` with `llm_span(\"medgemma_evaluate\", model_name)`\n- `_structure_decision_with_gemini()`: wrap `structured_llm.ainvoke(prompt)` with `llm_span(\"gemini_structure_decision\", model_name)`\n- `agentic_reasoning_loop()`: wrap `model.ainvoke(messages)` with `llm_span(\"medgemma_reasoning\", model_name)`\n- `_structure_reasoning_with_gemini()`: wrap `structured_llm.ainvoke(prompt)` with `llm_span(\"gemini_structure_reasoning\", model_name)`\n- For LangChain responses: extract token counts from `raw_response.usage_metadata` or `raw_response.response_metadata`\n\n### 4. `services/protocol-processor-service/src/protocol_processor/tools/entity_decomposer.py`\n- Wrap `structured.ainvoke(prompt)` in `decompose_entities_from_criterion()` with `llm_span(\"gemini_entity_decompose\", model_name)`\n\n### 5. `services/protocol-processor-service/src/protocol_processor/tools/field_mapper.py`\n- Wrap `structured_llm.ainvoke(prompt)` in `generate_field_mappings()` with `llm_span(\"gemini_field_mapping\")`\n\n### 6. `services/protocol-processor-service/src/protocol_processor/tools/gemini_utils.py`\n- No changes needed — `create_structured_llm()` is a factory, instrumentation belongs at call sites\n\n### 7. Tool files using `create_structured_llm` (via grep: structure_builder.py, ordinal_resolver.py)\n- Wrap their `structured_llm.ainvoke(prompt)` calls similarly\n\n## `llm_span()` design\n\n```python\n@contextmanager\ndef llm_span(name: str, model_name: str = \"\"):\n    \"\"\"Create an MLflow child span for an individual LLM call.\"\"\"\n    # Inside existing pipeline_span → auto-nests as child\n    # No pipeline_span active → creates independent trace (still useful)\n    try:\n        import mlflow\n        if os.getenv(\"MLFLOW_TRACKING_URI\"):\n            with mlflow.start_span(name=name, span_type=\"LLM\") as span:\n                ctx = _LLMSpanCtx(span, model_name)\n                yield ctx\n                ctx._finalize()\n                return\n    except ImportError: ...\n    except Exception: ...\n    yield _NoOpLLMSpan()\n```\n\nThe `_LLMSpanCtx` object exposes:\n- `set_request(prompt_text)` — logs prompt + model to span inputs\n- `set_response(response_text, usage=None)` — logs response + tokens to span outputs\n\n## Verification\n\n1. `uv run ruff check .` — passes\n2. `uv run mypy services/protocol-processor-service` — passes\n3. `uv run pytest services/protocol-processor-service/tests/ -x` — passes\n4. Smoke test script (not committed): triggers a pipeline run and queries MLflow to verify child spans appear with prompt/response/token data inside node traces\n"
}
```

> TOOL

tool_result ERROR
id: toolu_01CLyChKF8oaj6TuKatTtqpM
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.
```
