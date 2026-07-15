> DEVELOPER

I need you to explore the reigh-worker repo at /Users/user_c042661f/Documents/reigh-workspace/reigh-worker for Sprint 3 of the Wan2GP fork migration. I need concrete findings — file paths, line numbers, current content — to write an implementation plan.

Please gather the following information:

1. **Wan2GP submodule state**: Is `Wan2GP/` a git submodule now? Check `.gitmodules` and `git submodule status` from the repo root. What commit is it pinned to? What does the `banodoco/Wan2GP` fork look like — is there a `reigh-sprint-2` branch? What about `reigh-sprint-3`? Run `cd Wan2GP && git log --oneline -10 && git status && git branch -a` to understand.

2. **models/ltx2/ hot zone current state**: List the files in `Wan2GP/models/ltx2/` (just the directory, not deep recursive). Of those 22 files mentioned as differing, what's the drift right now vs. upstream? Focus on:
   - `Wan2GP/models/ltx2/ltx_core/tools.py` — read lines 50-100 to confirm the `clear_conditioning` function is present, and capture its exact content (byte-level) so we know the baseline to compare against.
   - Does `Wan2GP/defaults/ltx2_22B_distilled_1_1.json` exist yet? If not, what other `ltx2_*.json` defaults exist for comparison?

3. **IC-LoRA override code**: Read `source/core/params/travel_guidance.py` to understand:
   - The `_IC_LORA_BY_MODE` registry (around line 32-37 per the plan) — what modes does it currently have, what are the paths/names/strengths?
   - The `get_ic_lora_entry()` function around line 310-314 and its cameraman override branch
   - `_IC_LORA_UNION_CONTROL` constant — what's its value?
   - `TravelGuidanceConfig` dataclass — what fields does it have (kind, mode, etc.)? Is `strength` a field?

4. **Task registry dedup**: Read `source/task_handlers/tasks/task_registry.py` lines 940-990 to understand the dedup logic that compares basenames. Capture how the auto-inject drives the dedup — function name, what keys it expects in the segment_loras list items, etc.

5. **Existing test patterns**: Look at `tests/test_travel_guidance_config.py` (first 80 lines or so, plus check for fixtures) so we know what existing helpers/imports are used. Also check `tests/` directory for any `conftest.py` and list all existing test files.

6. **clear_conditioning fixture**: Is there already a saved latent fixture anywhere? Search for `.pt`, `.npy`, `.safetensors` files under `tests/` and `fixtures/`. Also search for `clear_conditioning` references in `tests/` and `scripts/`.

7. **scripts/live_test/**: What's in this untracked directory (from `git status`)? It appeared in Sprint 2 — is there a smoke test setup there we should reuse?

8. **Sprint 2 smoke venv reference**: Search the docs or prior plan outputs for `/tmp/sprint2-smoke-venv` references — is there a script that builds that venv? Also check `.megaplan/` for any Sprint 2 outputs that might record the exact pip install commands.

9. **Current baseline tags**: Run `git tag -l 'wan2gp-mig-*'` to see what sprint baseline tags already exist.

Report your findings concisely — file paths with line numbers and short excerpts where relevant. Don't paraphrase code; quote the key lines. I need this to be accurate so I can write exact plan steps. Keep the report focused — under ~600 words if possible.

> AGENT

I'll systematically explore the repo to gather these Sprint 3 baseline findings. Let me start with parallel searches.

> TOOL

tool_use Bash
```json
{
  "command": "git status"
}
```

> TOOL

tool_result Bash
```
On branch main
Your branch is ahead of 'origin/main' by 2 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/wan2gp-triage.csv
	scripts/live_test/

nothing added to commit but untracked files present (use "git add" to track)
```

> AGENT

Now let me check the git submodule state and other foundational information:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.gitmodules"
}
```

> TOOL

tool_result Read
```
1	[submodule "Wan2GP"]
2		path = Wan2GP
3		url = https://github.com/banodoco/Wan2GP.git
4		branch = reigh-sprint-2
5
```

> TOOL

tool_use Bash
```json
{
  "command": "git submodule status"
}
```

> TOOL

tool_result Bash
```
This command requires approval
```

> TOOL

tool_use Bash
```json
{
  "command": "git tag -l 'wan2gp-mig-*'"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(git submodule status) errored</tool_use_error>
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la Wan2GP/ 2>&1 | head -20"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(git submodule status) errored</tool_use_error>
```

> AGENT

Good, `.gitmodules` shows it's a submodule on `reigh-sprint-2` branch. Let me check the Wan2GP state directly:

> TOOL

tool_use Bash
```json
{
  "command": "cd /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP && git log --oneline -10"
}
```

> TOOL

tool_result Bash
```
This command changes directory before running git, which can execute untrusted hooks from the target directory. Approve only if you trust it.
```

> TOOL

tool_use Bash
```json
{
  "command": "cd /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP && git status"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(cd /Users/user_c042661f/Documents/reigh-w…) errored</tool_use_error>
```

> TOOL

tool_use Bash
```json
{
  "command": "cd /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP && git branch -a | head -15"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(cd /Users/user_c042661f/Documents/reigh-w…) errored</tool_use_error>
```

> AGENT

Let me check these files without changing directory:

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP log --oneline -10"
}
```

> TOOL

tool_result Bash
```
This command requires approval
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP status"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(git -C /Users/user_c042661f/Documents/rei…) errored</tool_use_error>
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP branch -a"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(git -C /Users/user_c042661f/Documents/rei…) errored</tool_use_error>
```

> AGENT

Let me continue with file exploration while keeping the focus on reading the main repo files:

> TOOL

tool_use Glob
```json
{
  "pattern": "Wan2GP/models/ltx2",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""Travel guidance contract for orchestrator and segment payloads."""
2	
3	from __future__ import annotations
4	
5	from dataclasses import dataclass, field
6	from typing import Any, Dict, List, Literal, Optional, Tuple
7	
8	from source.runtime.wgp_bridge import get_model_def
9	
10	from .base import ParamGroup
11	from .structure_guidance import StructureGuidanceConfig, StructureVideoEntry
12	
13	_TRAVEL_GUIDANCE_KIND = Literal[
14	    "none",
15	    "vace",
16	    "ltx_control",
17	    "ltx_hybrid",
18	    "ltx_anchor",
19	    "uni3c",
20	]
21	_TRAVEL_GUIDANCE_LEGACY_KEYS = (
22	    "structure_type",
23	    "structure_video_path",
24	    "structure_videos",
25	    "use_uni3c",
26	)
27	_LTX_CONTROL_MODES = {"pose", "depth", "canny", "video", "cameraman"}
28	
29	# IC LoRA registry: mode → (filename, optional download URL).
30	# Modes not listed fall back to the preloaded union-control LoRA.
31	_IC_LORA_UNION_CONTROL = "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"
32	_IC_LORA_BY_MODE: dict[str, tuple[str, str | None]] = {
33	    "cameraman": (
34	        [REDACTED],
35	        "https://huggingface.co/Cseti/LTX2.3-22B_IC-LoRA-Cameraman_v1/resolve/main/LTX2.3-22B_IC-LoRA-Cameraman_v1_10500.safetensors",
36	    ),
37	}
38	
39	
40	def _has_payload_value(value: Any) -> bool:
41	    """Return True when a payload field should count as "present"."""
42	    if value is None or value is False:
43	        return False
44	    if isinstance(value, (list, dict, str)):
45	        return bool(value)
46	    return True
47	
48	
49	def _infer_allowed_kinds(model_name: str) -> set[str]:
50	    """Infer which travel guidance kinds are allowed for a model."""
51	    lowered = (model_name or "").lower()
52	
53	    if "ltx2" in lowered:
54	        pipeline_kind = None
55	        try:
56	            model_def = get_model_def(model_name)
57	            if isinstance(model_def, dict):
58	                pipeline_kind = model_def.get("ltx2_pipeline")
59	        except (ImportError, RuntimeError, TypeError, ValueError, KeyError, AttributeError):
60	            pipeline_kind = None
61	
62	        is_distilled = pipeline_kind == "distilled" or (
63	            pipeline_kind is None and "distilled" in lowered
64	        )
65	        if is_distilled:
66	            return {"none", "ltx_control", "ltx_hybrid", "ltx_anchor", "uni3c"}
67	        return {"none"}
68	
69	    return {"none", "vace", "uni3c"}
70	
71	
72	@dataclass
73	class AnchorEntry:
74	    """Single positioned image anchor for hybrid travel guidance."""
75	
76	    image_url: str
77	    frame_position: int
78	    strength: float = 1.0
79	
80	    @classmethod
81	    def from_dict(cls, d: dict) -> "AnchorEntry":
82	        return cls(
83	            image_url=str(d.get("image_url", "") or ""),
84	            frame_position=int(d.get("frame_position", 0) or 0),
85	            strength=float(d.get("strength", 1.0)),
86	        )
87	
88	    def to_dict(self) -> dict:
89	        return {
90	            "image_url": self.image_url,
91	            "frame_position": self.frame_position,
92	            "strength": self.strength,
93	        }
94	
95	
96	@dataclass
97	class AudioConditioningConfig:
98	    """Optional generation-time audio conditioning for hybrid travel guidance."""
99	
100	    source: Literal["external", "control_track"]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/tasks/task_registry.py",
  "offset": 940,
  "limit": 50
}
```

> TOOL

tool_result Read
```
940	    # Flow-shift tiers: top-level segment payload > orchestrator_details.
941	    explicit_flow_shift = _get_param("flow_shift", segment_params, orchestrator_details, prefer_truthy=True)
942	    if explicit_flow_shift:
943	        generation_params["flow_shift"] = explicit_flow_shift
944	
945	    # =============================================================================
946	    # Per-Segment Parameter Overrides
947	    # =============================================================================
948	    # Check for segment-specific LoRAs first (highest priority)
949	    # This allows per-segment LoRA overrides to take precedence over phase_config LoRAs
950	    segment_loras = _get_param("segment_loras", individual_params, default=None)
951	    segment_lora_config = None
952	    phase_config_source_name = "none"
953	    preset_name = None
954	
955	    # Auto-inject IC LoRA when travel guidance requires it (e.g. pose/depth/canny/cameraman).
956	    # This runs for both orchestrator-created and standalone individual_travel_segment tasks.
957	    if isinstance(structure.structure_config, TravelGuidanceConfig):
958	        ic_entry = structure.structure_config.get_ic_lora_entry()
959	        if ic_entry is not None:
960	            segment_loras = list(segment_loras or [])
961	            # Deduplicate: update strength if the same LoRA is already present
962	            ic_basename = os.path.basename(ic_entry["path"])
963	            found = False
964	            for existing in segment_loras:
965	                if os.path.basename(existing.get("path", "")) == ic_basename:
966	                    existing["strength"] = ic_entry["strength"]
967	                    found = True
968	                    break
969	            if not found:
970	                segment_loras.append(ic_entry)
971	            headless_logger.debug(f"IC LoRA for mode '{structure.structure_config.mode}': {ic_basename}", task_id=task_id)
972	
973	    if segment_loras:
974	        # Pass through URLs/filenames without downloading - convert_to_wgp_task_impl() handles resolution
975	        segment_lora_config = True  # Flag to skip phase_config LoRAs below
976	        activated = []
977	        mults = []
978	        for lora_dict in segment_loras:
979	            path = lora_dict.get("path", "")
980	            strength = lora_dict.get("strength", 1.0)
981	            if path:
982	                activated.append(path)
983	                mults.append(str(strength))
984	        if activated:
985	            generation_params["activated_loras"] = activated
986	            generation_params["loras_multipliers"] = " ".join(mults)
987	            headless_logger.debug(f"Set {len(activated)} segment-specific LoRAs (download deferred)", task_id=task_id)
988	
989	    # Determine phase_config source for logging
```

> AGENT

Now let me read more of the travel_guidance file to get the complete picture of the get_ic_lora_entry and TravelGuidanceConfig:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py",
  "offset": 300,
  "limit": 100
}
```

> TOOL

tool_result Read
```
300	            return self.mode in {"pose", "depth", "canny", "cameraman"}
301	        if self.kind == "ltx_hybrid":
302	            return self.has_control and self.mode in {"pose", "depth", "canny"}
303	        return False
304	
305	    def get_ic_lora_entry(self) -> Optional[Dict[str, Any]]:
306	        """Return the IC LoRA dict to inject into segment_loras, or None."""
307	        if not self.needs_ic_lora():
308	            return None
309	
310	        mode_entry = _IC_LORA_BY_MODE.get(self.mode)
311	        if mode_entry is not None:
312	            filename, url = mode_entry
313	        else:
314	            filename, url = _IC_LORA_UNION_CONTROL, None
315	
316	        strength = (
317	            self.control_strength if self.is_ltx_hybrid else self.strength
318	        )
319	        # Use URL when available so the download pipeline can fetch on demand;
320	        # bare filename relies on preload.
321	        return {
322	            "path": url or filename,
323	            "strength": strength,
324	            "name": f"ic-lora-{self.mode} (auto-injected)",
325	        }
326	
327	    def get_preprocessor_type(self) -> str:
328	        """Return the preprocessor/compositing type used for this guidance."""
329	        if self.kind == "vace":
330	            return "raw" if self.mode == "raw" else self.mode
331	        if self.kind == "ltx_control":
332	            return "raw" if self.mode in {"video", "cameraman"} else self.mode
333	        if self.kind == "ltx_hybrid":
334	            if not self.has_control:
335	                return "raw"
336	            return "raw" if self.mode == "video" else self.mode
337	        if self.kind == "ltx_anchor":
338	            return "raw"
339	        if self.kind == "uni3c":
340	            return "uni3c"
341	        return "raw"
342	
343	    def to_segment_payload(self, frame_offset: int) -> Dict[str, Any]:
344	        """Serialize to the segment-level ``travel_guidance`` payload."""
345	        if self.kind == "none":
346	            return {"kind": "none"}
347	        if self.kind == "ltx_anchor":
348	            return {
349	                "kind": self.kind,
350	                "anchors": [anchor.to_dict() for anchor in self.anchors],
351	                "_frame_offset": frame_offset,
352	            }
353	
354	        payload: Dict[str, Any] = {
355	            "kind": self.kind,
356	            "videos": [video.to_dict() for video in self.videos],
357	            "strength": self.strength,
358	            "_frame_offset": frame_offset,
359	        }
360	
361	        if self.mode:
362	            payload["mode"] = self.mode
363	        if self.kind in {"vace", "ltx_control"}:
364	            payload["canny_intensity"] = self.canny_intensity
365	            payload["depth_contrast"] = self.depth_contrast
366	        if self.kind == "ltx_hybrid":
367	            payload["anchors"] = [anchor.to_dict() for anchor in self.anchors]
368	            payload["control_strength"] = self.control_strength
369	            payload["canny_intensity"] = self.canny_intensity
370	            payload["depth_contrast"] = self.depth_contrast
371	            if self.audio is not None:
372	                payload["audio"] = self.audio.to_dict()
373	        if self.kind == "uni3c":
374	            payload["step_window"] = list(self.step_window)
375	            payload["frame_policy"] = self.frame_policy
376	            payload["zero_empty_frames"] = self.zero_empty_frames
377	            payload["keep_on_gpu"] = self.keep_on_gpu
378	        if self._guidance_video_url:
379	            payload["_guidance_video_url"] = self._guidance_video_url
380	
381	        return payload
382	
383	    def validate(self, model_name: str) -> List[str]:
384	        """Validate the parsed config against payload and model constraints."""
385	        errors: List[str] = []
386	        allowed_kinds = _infer_allowed_kinds(model_name)
387	
388	        if self.kind not in {"none", "vace", "ltx_control", "ltx_hybrid", "ltx_anchor", "uni3c"}:
389	            errors.append(
390	                "Invalid travel_guidance.kind "
391	                f"'{self.kind}'. Must be one of none, vace, ltx_control, ltx_hybrid, ltx_anchor, uni3c"
392	            )
393	            return errors
394	
395	        if self.kind not in allowed_kinds:
396	            errors.append(
397	                f"Model '{model_name}' does not support travel_guidance kind '{self.kind}'"
398	            )
399
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py",
  "offset": 100,
  "limit": 100
}
```

> TOOL

tool_result Read
```
100	    source: Literal["external", "control_track"]
101	    audio_url: Optional[str] = None
102	    strength: float = 1.0
103	
104	    @classmethod
105	    def from_dict(cls, d: dict) -> "AudioConditioningConfig":
106	        return cls(
107	            source=str(d.get("source", "") or ""),  # type: ignore[arg-type]
108	            audio_url=d.get("audio_url"),
109	            strength=float(d.get("strength", 1.0)),
110	        )
111	
112	    def to_dict(self) -> dict:
113	        result = {
114	            "source": self.source,
115	            "strength": self.strength,
116	        }
117	        if self.audio_url:
118	            result["audio_url"] = self.audio_url
119	        return result
120	
121	
122	@dataclass
123	class TravelGuidanceConfig(ParamGroup):
124	    """Discriminated union for travel guidance."""
125	
126	    kind: _TRAVEL_GUIDANCE_KIND = "none"
127	
128	    # Shared fields for all non-none kinds
129	    videos: List[StructureVideoEntry] = field(default_factory=list)
130	    strength: float = 0.0
131	
132	    # Hybrid-only fields
133	    anchors: List[AnchorEntry] = field(default_factory=list)
134	    control_strength: float = 1.0
135	    audio: Optional[AudioConditioningConfig] = None
136	
137	    # VACE / LTX control
138	    mode: str = ""
139	    canny_intensity: float = 1.0
140	    depth_contrast: float = 1.0
141	
142	    # Uni3C
143	    step_window: Tuple[float, float] = (0.0, 1.0)
144	    frame_policy: str = "fit"
145	    zero_empty_frames: bool = True
146	    keep_on_gpu: bool = False
147	
148	    # Internal orchestration state
149	    _guidance_video_url: Optional[str] = None
150	    _frame_offset: int = 0
151	    _raw_keys: frozenset[str] = field(default_factory=frozenset)
152	
153	    @classmethod
154	    def from_params(cls, params: Dict[str, Any], **context) -> "TravelGuidanceConfig":
155	        model_name = (
156	            context.get("model_name")
157	            or context.get("model")
158	            or params.get("model_name")
159	            or params.get("model")
160	            or ""
161	        )
162	        return cls.from_payload(params, model_name)
163	
164	    @classmethod
165	    def from_payload(cls, payload: Dict[str, Any], model_name: str) -> "TravelGuidanceConfig":
166	        """Parse from either a full params dict or a raw ``travel_guidance`` dict."""
167	        if not isinstance(payload, dict):
168	            raise ValueError("travel_guidance payload must be a dict")
169	
170	        if "travel_guidance" in payload:
171	            raw = payload.get("travel_guidance") or {}
172	            if not isinstance(raw, dict):
173	                raise ValueError("travel_guidance payload must be a dict")
174	            cls._validate_exclusive_payload(payload)
175	        else:
176	            raw = payload
177	
178	        kind = str(raw.get("kind", "none") or "none")
179	        mode = str(raw.get("mode", "") or "")
180	        strength_default = cls._default_strength(kind, mode)
181	        audio_raw = raw.get("audio")
182	        anchors_raw = raw.get("anchors", []) or []
183	        if kind == "ltx_anchor":
184	            anchors_raw = cls._apply_ltx_anchor_default_strengths(anchors_raw)
185	
186	        config = cls(
187	            kind=kind,  # type: ignore[arg-type]
188	            videos=[StructureVideoEntry.from_dict(v) for v in raw.get("videos", []) or []],
189	            strength=float(raw.get("strength", strength_default)),
190	            anchors=[AnchorEntry.from_dict(anchor) for anchor in anchors_raw],
191	            control_strength=float(raw.get("control_strength", 1.0)),
192	            audio=AudioConditioningConfig.from_dict(audio_raw) if isinstance(audio_raw, dict) else None,
193	            mode=mode,
194	            canny_intensity=float(raw.get("canny_intensity", 1.0)),
195	            depth_contrast=float(raw.get("depth_contrast", 1.0)),
196	            frame_policy=str(raw.get("frame_policy", "fit") or "fit"),
197	            zero_empty_frames=bool(raw.get("zero_empty_frames", True)),
198	            keep_on_gpu=bool(raw.get("keep_on_gpu", False)),
199	            _guidance_video_url=raw.get("_guidance_video_url"),
```

> AGENT

Now let me check the test files and fixtures:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_travel_guidance_config.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	import pytest
2	import ast
3	import sys
4	import textwrap
5	import types
6	from contextlib import contextmanager
7	from pathlib import Path
8	from types import SimpleNamespace
9	
10	from source.core.params.structure_guidance import StructureGuidanceConfig
11	from source.core.params.travel_guidance import TravelGuidanceConfig
12	
13	
14	VIDEO_ENTRY = {
15	    "path": "/tmp/guidance.mp4",
16	    "start_frame": 0,
17	    "end_frame": 16,
18	    "treatment": "adjust",
19	}
20	LTX_DISTILLED_MODEL = "ltx2_22B_distilled"
21	VACE_MODEL = "wan_2_2_vace_lightning_baseline_2_2_2"
22	
23	
24	def _anchor(image_url: str, frame_position: int, **extra):
25	    anchor = {"image_url": image_url, "frame_position": frame_position}
26	    anchor.update(extra)
27	    return anchor
28	
29	
30	def _ltx_anchor_payload(anchors, **extra):
31	    return {
32	        "travel_guidance": {
33	            "kind": "ltx_anchor",
34	            "anchors": anchors,
35	            **extra,
36	        }
37	    }
38	
39	
40	def test_parse_each_travel_guidance_kind():
41	    vace = TravelGuidanceConfig.from_payload(
42	        {"travel_guidance": {"kind": "vace", "mode": "flow", "videos": [VIDEO_ENTRY]}},
43	        "wan_2_2_vace_lightning_baseline_2_2_2",
44	    )
45	    ltx = TravelGuidanceConfig.from_payload(
46	        {"travel_guidance": {"kind": "ltx_control", "mode": "pose", "videos": [VIDEO_ENTRY]}},
47	        "ltx2_22B_distilled",
48	    )
49	    uni3c = TravelGuidanceConfig.from_payload(
50	        {"travel_guidance": {"kind": "uni3c", "videos": [VIDEO_ENTRY]}},
51	        "ltx2_22B_distilled",
52	    )
53	    none_cfg = TravelGuidanceConfig.from_payload(
54	        {"travel_guidance": {"kind": "none"}},
55	        "ltx2_22B",
56	    )
57	
58	    assert vace.kind == "vace"
59	    assert ltx.kind == "ltx_control"
60	    assert uni3c.kind == "uni3c"
61	    assert none_cfg.kind == "none"
62	
63	
64	def test_parse_ltx_control_cameraman():
65	    config = TravelGuidanceConfig.from_payload(
66	        {"travel_guidance": {"kind": "ltx_control", "mode": "cameraman", "videos": [VIDEO_ENTRY]}},
67	        "ltx2_22B_distilled",
68	    )
69	
70	    assert config.kind == "ltx_control"
71	    assert config.mode == "cameraman"
72	
73	
74	@pytest.mark.parametrize(
75	    ("payload", "model_name"),
76	    [
77	        ({"travel_guidance": {"kind": "vace", "mode": "flow", "videos": [VIDEO_ENTRY]}}, "ltx2_22B_distilled"),
78	        ({"travel_guidance": {"kind": "ltx_control", "mode": "pose", "videos": [VIDEO_ENTRY]}}, "wan_2_2_vace_lightning_baseline_2_2_2"),
79	        ({"travel_guidance": {"kind": "ltx_control", "mode": "pose", "videos": [VIDEO_ENTRY]}}, "ltx2_22B"),
80	    ],
```

> TOOL

tool_use Glob
```json
{
  "pattern": "tests/conftest.py",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Glob
```
tests/conftest.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "tests/test_*.py",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Glob
```
tests/test_join_orchestrator_and_registry.py
tests/test_task_result_protocol.py
tests/test_chatterbox_s3gen_direct_coverage.py
tests/test_lora_formats_baseline.py
tests/test_wan2gp_direct_coverage_remaining.py
tests/test_param_precedence_contracts.py
tests/test_plugin.py
tests/test_task_type_catalog.py
tests/test_wgp_output_contracts.py
tests/test_output_paths_contracts.py
tests/test_video_storage_upload_contracts.py
tests/test_structure_treatment_contracts.py
tests/test_travel_segment_types_contracts.py
tests/test_log_context_scoping.py
tests/test_clip_preprocessor.py
tests/test_video_info_contracts.py
tests/test_runtime_boundaries.py
tests/test_remaining_module_coverage.py
tests/test_split_helper_modules.py
tests/test_task_metadata_split.py
tests/test_structure_guidance_parsing_split.py
tests/test_transition_prompt_templates.py
tests/test_composite_result_split.py
tests/test_queue_status_wait.py
tests/test_task_dependencies_split_modules.py
tests/test_structure_pipeline_contracts.py
tests/test_wgp_patch_lifecycle.py
tests/test_wgp_params_overrides.py
tests/test_transition_prompt_api_contracts.py
tests/test_failure_semantics_contracts.py
tests/test_error_consistency_contracts.py
tests/test_vlm_service_contracts.py
tests/test_wan_orchestrator_collaborators.py
tests/test_task_polling_helpers.py
tests/test_guide_video_request_api.py
tests/test_travel_segment_queue_contracts.py
tests/test_dispatch_payload_contracts.py
tests/test_vace_frame_contracts.py
tests/test_join_transition_contracts.py
tests/test_travel_api_wrappers.py
tests/test_critical_seams_contracts.py
tests/test_debug_option_contracts.py
tests/test_debug_diagnostics_and_uni3c.py
tests/test_orchestrator_alias_resolution.py
tests/test_output_paths_filename_policy.py
tests/test_travel_payload_contracts.py
tests/test_dispatch_contracts.py
tests/test_travel_guide_module_alias.py
tests/test_polling_policy.py
tests/test_travel_orchestrator_terminal_gating.py
tests/test_join_shared_idempotency_gating.py
tests/test_wgp_bridge_contracts.py
tests/test_queue_runtime_and_finalization_service.py
tests/test_mask_generation_and_utils.py
tests/test_db_runtime_error_contracts.py
tests/test_uni3c_validation_contracts.py
tests/test_task_registry_lazy_contracts.py
tests/test_task_result_handler_contracts.py
tests/test_root_shims_contracts.py
tests/test_media_namespace_contracts.py
tests/test_wgp_init_bootstrap_contracts.py
tests/test_video_transform_api_contracts.py
tests/test_wgp_bridge_ports_contracts.py
tests/test_runtime_model_patch_contracts.py
tests/test_wgp_patch_context_contracts.py
tests/test_join_orchestrator_payload_contracts.py
tests/test_video_api_facade_contracts.py
tests/test_worker_postprocess_and_bootstrap_service_contracts.py
tests/test_debug_helper_coverage.py
tests/test_runtime_contracts_core_paths.py
tests/test_task_status_return_contract.py
tests/test_task_status_split_modules.py
tests/test_task_claim_flow.py
tests/test_svi_preflight.py
tests/test_debug_commands.py
tests/test_task_dependencies_query_helpers.py
tests/test_create_test_task_cli.py
tests/test_transitive_direct_links_pass3.py
tests/test_specialized_dispatch_contracts.py
tests/test_runtime_registry_readonly_contracts.py
tests/test_debug_cli_and_formatters.py
tests/test_debug_split_module_coverage.py
tests/test_edge_retry_contracts.py
tests/test_high_import_facade_contracts.py
tests/test_examples_cli.py
tests/test_worker_auth_mode_contracts.py
tests/test_worker_bootstrap_gate_contracts.py
tests/test_video_brightness_contracts.py
tests/test_edge_retry_helpers_contracts.py
tests/test_video_brightness_module_contracts.py
tests/test_debug_command_registry_contracts.py
tests/test_task_dispatch_manifest_contracts.py
tests/test_task_polling_contracts.py
tests/test_task_polling_result_contracts.py
tests/test_multi_structure_video.py
tests/test_lora_flow.py
tests/test_wan2gp_direct_coverage_contracts.py
tests/test_worker_matrix_runner_contracts.py
tests/test_param_resolution.py
tests/test_wan2gp_direct_coverage_open_findings.py
(Results are truncated. Consider using a more specific path or pattern.)
```

> AGENT

Let me search for fixture data and clear_conditioning references:

> TOOL

tool_use Grep
```json
{
  "pattern": "clear_conditioning",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests"
}
```

> TOOL

tool_result Grep
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/*.pt",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/*.safetensors",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Glob
```json
{
  "pattern": "scripts/live_test",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Glob
```
No files found
```

> AGENT

Let me check the scripts/live_test directory and conftest:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/ 2>&1 | head -30"
}
```

> TOOL

tool_result Bash
```
total 296
drwxr-xr-x@ 25 user_c042661f  staff    800 Apr 11 05:44 .
drwxr-xr-x  12 user_c042661f  staff    384 Apr 11 04:59 ..
-rw-r--r--@  1 user_c042661f  staff   1546 Apr 11 05:07 __init__.py
drwxr-xr-x@ 79 user_c042661f  staff   2528 Apr 13 01:13 __pycache__
-rw-r--r--@  1 user_c042661f  staff   6518 Apr 11 05:23 completion_poller.py
-rw-r--r--@  1 user_c042661f  staff   6269 Apr 11 05:07 config.py
-rw-r--r--@  1 user_c042661f  staff   4082 Apr 11 05:17 git_ops.py
-rw-r--r--@  1 user_c042661f  staff   2574 Apr 11 05:14 heartbeat_waiter.py
-rw-r--r--@  1 user_c042661f  staff   2071 Apr 11 05:05 launch_command.py
-rw-r--r--@  1 user_c042661f  staff   1262 Apr 11 05:05 logger.py
-rw-r--r--@  1 user_c042661f  staff   2920 Apr 11 05:44 main.py
-rw-r--r--@  1 user_c042661f  staff   9920 Apr 11 05:32 matrix.py
-rw-r--r--@  1 user_c042661f  staff   2589 Apr 11 05:14 preflight.py
-rw-r--r--@  1 user_c042661f  staff   2246 Apr 11 05:32 report.py
-rw-r--r--@  1 user_c042661f  staff   2788 Apr 11 05:15 safety_gate.py
-rw-r--r--@  1 user_c042661f  staff   5333 Apr 11 05:35 smoke.py
-rw-r--r--@  1 user_c042661f  staff   6238 Apr 11 05:15 ssh_bootstrap.py
-rw-r--r--@  1 user_c042661f  staff  18442 Apr 11 05:00 stage1_findings.md
-rw-r--r--@  1 user_c042661f  staff   8495 Apr 11 04:59 stage1_probe.py
-rw-r--r--@  1 user_c042661f  staff   3014 Apr 11 05:22 task_spoofer.py
-rw-r--r--@  1 user_c042661f  staff    574 Apr 11 05:14 terminate_guard.py
drwxr-xr-x@  4 user_c042661f  staff    128 Apr 11 05:35 tests
-rw-r--r--@  1 user_c042661f  staff   1025 Apr 11 05:14 token_resolver.py
-rw-r--r--@  1 user_c042661f  staff   6563 Apr 11 05:46 variant_fresh.py
-rw-r--r--@  1 user_c042661f  staff  12868 Apr 11 05:46 variant_update.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/conftest.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import os
4	import tempfile
5	from pathlib import Path
6	
7	
8	_TMP_ROOT = Path(tempfile.gettempdir()) / "reigh-worker-pytest"
9	_MPL_CACHE = _TMP_ROOT / "matplotlib"
10	_XDG_CACHE = _TMP_ROOT / "cache"
11	
12	_MPL_CACHE.mkdir(parents=True, exist_ok=True)
13	_XDG_CACHE.mkdir(parents=True, exist_ok=True)
14	
15	os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
16	os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CACHE))
17	os.environ.setdefault("XDG_CACHE_HOME", str(_XDG_CACHE))
18
```

> AGENT

Now let me search for .megaplan and any Sprint 2 venv references:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/reigh-worker -name \".megaplan\" -type d 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.megaplan
```

> TOOL

tool_use Grep
```json
{
  "pattern": "sprint2-smoke-venv",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Grep
```
No files found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "clear_conditioning",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker"
}
```

> TOOL

tool_result Grep
```
Found 4 files
docs/WAN2GP_FORK_MIGRATION_PLAN.md
Wan2GP/models/ltx2/ltx_pipelines/utils/helpers.py
Wan2GP/models/ltx2/ltx_core/tools.py
docs/wan2gp-triage.csv
```

> AGENT

Good! Let me check the Wan2GP tools.py file and the megaplan directory:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/ltx_core/tools.py",
  "offset": 50,
  "limit": 50
}
```

> TOOL

tool_result Read
```
50	        clean_latent = self.patchifier.patchify(latent_state.clean_latent)
51	        denoise_mask = self.patchifier.patchify(latent_state.denoise_mask)
52	        return replace(latent_state, latent=latent, denoise_mask=denoise_mask, clean_latent=clean_latent)
53	
54	    def unpatchify(self, latent_state: LatentState) -> LatentState:
55	        """
56	        Unpatchify the latent state.
57	        """
58	        latent_state = latent_state.clone()
59	        latent = self.patchifier.unpatchify(latent_state.latent, output_shape=self.target_shape)
60	        clean_latent = self.patchifier.unpatchify(latent_state.clean_latent, output_shape=self.target_shape)
61	        denoise_mask = self.patchifier.unpatchify(
62	            latent_state.denoise_mask, output_shape=self.target_shape.mask_shape()
63	        )
64	        return replace(latent_state, latent=latent, denoise_mask=denoise_mask, clean_latent=clean_latent)
65	
66	    def clear_conditioning(self, latent_state: LatentState) -> LatentState:
67	        """
68	        Clear the conditioning from the latent state. This method removes extra tokens from the end of the latent.
69	        Therefore, conditioning items should add extra tokens ONLY to the end of the latent.
70	        """
71	        latent_state = latent_state.clone()
72	
73	        num_tokens = self.patchifier.get_token_count(self.target_shape)
74	        latent = latent_state.latent[:, :num_tokens]
75	        clean_latent = latent_state.clean_latent[:, :num_tokens]
76	        denoise_mask = torch.ones_like(latent_state.denoise_mask)[:, :num_tokens]
77	        positions = latent_state.positions[:, :, :num_tokens]
78	
79	        return LatentState(latent=latent, denoise_mask=denoise_mask, positions=positions, clean_latent=clean_latent)
80	
81	
82	@dataclass(frozen=True)
83	class VideoLatentTools(LatentTools):
84	    """
85	    Tools for building video latent states.
86	    """
87	
88	    patchifier: VideoLatentPatchifier
89	    target_shape: VideoLatentShape
90	    fps: float
91	    scale_factors: SpatioTemporalScaleFactors = DEFAULT_SCALE_FACTORS
92	    causal_fix: bool = True
93	
94	    def create_initial_state(
95	        self,
96	        device: DeviceLikeType,
97	        dtype: torch.dtype,
98	        initial_latent: torch.Tensor | None = None,
99	    ) -> LatentState:
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.megaplan/"
}
```

> TOOL

tool_result Bash
```
total 16
drwxr-xr-x@  5 user_c042661f  staff   160 Apr  8 03:43 .
drwxr-xr-x  54 user_c042661f  staff  1728 Apr 22 00:45 ..
-rw-------@  1 user_c042661f  staff  6923 Apr  8 03:43 debt.json
drwxr-xr-x@ 19 user_c042661f  staff   608 Apr 22 01:32 plans
drwxr-xr-x@ 15 user_c042661f  staff   480 Apr 22 01:39 schemas
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/"
}
```

> TOOL

tool_result Bash
```
total 152
drwxr-xr-x   8 user_c042661f  staff    256 Apr 22 00:45 .
drwxr-xr-x  16 user_c042661f  staff    512 Apr 22 00:49 ..
-rw-r--r--   1 user_c042661f  staff     39 Apr 22 00:45 __init__.py
drwxr-xr-x   5 user_c042661f  staff    160 Apr 22 00:45 configs
-rw-r--r--   1 user_c042661f  staff  52038 Apr 22 00:45 ltx2.py
-rw-r--r--   1 user_c042661f  staff  17190 Apr 22 00:45 ltx2_handler.py
drwxr-xr-x  12 user_c042661f  staff    384 Apr 22 00:45 ltx_core
drwxr-xr-x   9 user_c042661f  staff    288 Apr 22 00:45 ltx_pipelines
```

> AGENT

Let me check the megaplan/plans directory and search for any ltx2_*.json defaults:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/reigh-worker -name \"ltx2*.json\" -type f 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/configs/ltx2_22b_config.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/configs/ltx2_rgb_factors.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/configs/ltx2_19b_config.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q4_k_m.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q8_0.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q6_k.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q8_0.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q6_k.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_19B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_19B_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q4_k_m.json
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.megaplan/plans/ | head -30"
}
```

> TOOL

tool_result Bash
```
total 0
drwxr-xr-x@ 19 user_c042661f  staff   608 Apr 22 01:32 .
drwxr-xr-x@  5 user_c042661f  staff   160 Apr  8 03:43 ..
drwxr-xr-x@ 23 user_c042661f  staff   736 Apr 11 01:19 actually-use-debugcard-at-20260411-0048
drwxr-xr-x@ 30 user_c042661f  staff   960 Apr  8 04:44 add-idle-release-feature-for-20260408-0309
drwxr-xr-x@ 16 user_c042661f  staff   512 Apr  7 19:00 add-idle-release-feature-when-20260407-1842
drwxr-xr-x@ 25 user_c042661f  staff   800 Apr 11 04:52 add-visual-flares-to-log-20260411-0323
drwxr-xr-x@ 25 user_c042661f  staff   800 Apr 11 06:11 clean-up-10-junk-sources-in-20260411-0458
drwxr-xr-x@ 22 user_c042661f  staff   704 Apr 10 18:58 clean-up-all-logging-in-the-20260410-1830
drwxr-xr-x@ 26 user_c042661f  staff   832 Apr 10 20:04 clean-up-debug-mode-logging-20260410-1833
drwxr-xr-x@ 25 user_c042661f  staff   800 Apr 21 21:59 execute-sprint-1-of-the-20260421-2130
drwxr-xr-x@ 44 user_c042661f  staff  1408 Apr 22 01:16 execute-sprint-2-of-the-20260421-2202
drwxr-xr-x@  5 user_c042661f  staff   160 Apr 22 01:39 execute-sprint-3-of-the-20260422-0132
drwxr-xr-x@ 24 user_c042661f  staff   768 Apr 11 00:45 finish-beautiful-log-redesign-20260410-2315
drwxr-xr-x@ 20 user_c042661f  staff   640 Apr 10 02:21 fix-windows-worker-launch-20260410-0159
drwxr-xr-x@ 24 user_c042661f  staff   768 Apr 10 23:10 implement-beautiful-log-20260410-2139
drwxr-xr-x@ 17 user_c042661f  staff   544 Apr 21 16:58 migrate-reigh-worker-s-ltx-20260421-1327
drwxr-xr-x@ 23 user_c042661f  staff   736 Apr 10 21:30 redesign-debug-mode-log-20260410-2019
drwxr-xr-x@ 22 user_c042661f  staff   704 Apr 10 20:48 redesign-normal-mode-log-20260410-2012
drwxr-xr-x@ 19 user_c042661f  staff   608 Apr  8 05:48 refactor-the-worker-idle-20260408-0520
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults -name \"*.json\" -type f 2>/dev/null | sort"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ace_step_v1.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ace_step_v1_5.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ace_step_v1_5_turbo_lm_0_6b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ace_step_v1_5_turbo_lm_1_7b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ace_step_v1_5_turbo_lm_4b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/alpha.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/alpha2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/alpha2_sf.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/alpha_sf.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/animate.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/chatterbox.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/chrono_edit.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/chrono_edit_distill.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/fantasy.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flf2v_720p.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_dev.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_dev_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_klein_4b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_klein_9b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_klein_base_4b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux2_klein_base_9b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_chroma.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_chroma_radiance.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_dev_kontext.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_dev_kontext_dreamomni2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_dev_umo.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_dev_uso.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_krea.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_schnell.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_srpo.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/flux_srpo_uso.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/fun_inp.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/fun_inp_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/heartmula_oss_3b.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/heartmula_rl_oss_3b_20260123.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_480_i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_480_i2v_step_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_480_t2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_480_t2v_lightx2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_t2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_upsampler.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_1_5_upsampler_1080.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_avatar.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_custom.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_custom_audio.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_custom_edit.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_t2v_accvideo.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/hunyuan_t2v_fast.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_2_2_Enhanced_Lightning_v2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_2_2_Enhanced_Lightning_v2_svi2pro.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_2_2_multitalk.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_2_2_svi2pro.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_720p.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_fusionix.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/i2v_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/index_tts2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/infinitetalk.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/infinitetalk_multi.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_lite_i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_lite_t2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_lite_t2v_10s_distil.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_lite_t2v_10s_distil_sparse.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_lite_t2v_5s_distil.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_pro_i2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_pro_t2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_pro_t2v_10s_sft.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/k5_pro_t2v_10s_sft_sparse.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/kiwi_edit.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/kiwi_edit_instruct_only.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/kiwi_edit_reference_only.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/kugelaudio_0_open.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/longcat_avatar.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/longcat_avatar_multi.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/longcat_video.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_19B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_19B_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q4_k_m.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q6_k.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled_gguf_q8_0.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q4_k_m.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q6_k.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_distilled_gguf_q8_0.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltxv_13B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltxv_distilled.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/lucy_edit.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/lucy_edit_1_1.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/lucy_edit_fastwan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/lucy_edit_fastwan_1_1.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/lynx.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/mocha.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/moviigen.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/multitalk.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/multitalk_720p.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi_1_1.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi_1_1_10s.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi_1_1_10s_fastwan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi_1_1_fastwan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ovi_fastwan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/phantom_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/phantom_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/pi_flux2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/pi_flux2_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen3_tts_base.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen3_tts_customvoice.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen3_tts_voicedesign.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_2512_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_edit_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_edit_plus2_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_edit_plus_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_edit_plus_20B_nunchaku_r128_fp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_edit_plus_20B_nunchaku_r128_int4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/qwen_image_layered_20B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/recam_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/scail.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/sky_df_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/sky_df_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/sky_df_720p_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/standin.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/steadydancer.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_1.3B_nvfp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_fusionix.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_nexus_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/t2v_sf.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ti2v_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ti2v_2_2_fastwan.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_1.3B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_cocktail.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_cocktail_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_fusionix.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_lightning_3p_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_14B_sf.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_ditto_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_fun_14B_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_fun_14B_cocktail_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_lynx_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_multitalk_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/vace_standin_14B.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_i2v_lightning_baseline_2_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_i2v_lightning_baseline_3_3.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_i2v_lightning_svi_3_3.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_i2v_lightning_svi_endframe.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_vace_lightning_baseline_2_2_2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wan_2_2_vace_lightning_baseline_3_3.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/wanmove.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_base.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_control.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_control2.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_control2_1.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_control2_1_8s.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_img2img.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_nunchaku_r128_fp4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_nunchaku_r256_int4.json
/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/z_image_twinflow_turbo.json
```

> AGENT

Now let me check the Sprint 2 plan outputs and look at the files more closely:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.megaplan/plans/execute-sprint-2-of-the-20260421-2202/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 7224
drwxr-xr-x@ 44 user_c042661f  staff     1408 Apr 22 01:16 .
drwxr-xr-x@ 19 user_c042661f  staff      608 Apr 22 01:32 ..
-rw-r--r--@  1 user_c042661f  staff        0 Apr 21 22:02 .plan.lock
-rw-r--r--@  1 user_c042661f  staff     9174 Apr 21 22:44 critique_output.json
-rw-------@  1 user_c042661f  staff     9314 Apr 21 22:13 critique_v1.json
-rw-------@  1 user_c042661f  staff    14516 Apr 21 22:26 critique_v2.json
-rw-------@  1 user_c042661f  staff    10969 Apr 21 22:36 critique_v3.json
-rw-------@  1 user_c042661f  staff    10307 Apr 21 22:44 critique_v4.json
-rw-------@  1 user_c042661f  staff   734837 Apr 22 01:10 execution.json
-rw-------@  1 user_c042661f  staff   156757 Apr 22 01:10 execution_audit.json
-rw-------@  1 user_c042661f  staff     9854 Apr 21 23:29 execution_batch_1.json
-rw-------@  1 user_c042661f  staff    76590 Apr 22 01:02 execution_batch_10.json
-rw-------@  1 user_c042661f  staff    77409 Apr 22 01:04 execution_batch_11.json
-rw-------@  1 user_c042661f  staff    75540 Apr 22 01:05 execution_batch_12.json
-rw-------@  1 user_c042661f  staff    75871 Apr 22 01:07 execution_batch_13.json
-rw-------@  1 user_c042661f  staff    78221 Apr 22 01:10 execution_batch_14.json
-rw-------@  1 user_c042661f  staff     5555 Apr 21 23:36 execution_batch_2.json
-rw-------@  1 user_c042661f  staff     7792 Apr 21 23:41 execution_batch_3.json
-rw-------@  1 user_c042661f  staff    10210 Apr 21 23:45 execution_batch_4.json
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/docs/WAN2GP_FORK_MIGRATION_PLAN.md",
  "limit": 50
}
```

> TOOL

tool_result Read
```
1	# Wan2GP Fork Migration — Design Document
2	
3	## 1. Executive Summary
4	`reigh-worker/Wan2GP/` is currently a flat vendored snapshot with no `.git` directory, so it cannot be cleanly rebased onto `deepbeepmeep/Wan2GP` even though it is roughly 50 days and about 9 minor versions behind. The hottest drift zone is `Wan2GP/models/ltx2/`, where 22 files differ and the working diff is roughly 4303 lines.
5	
6	This migration plan is intentionally a planning artifact, not an implementation batch. It breaks the migration into 4 sprints of 2 weeks each so the team can inventory drift first, cut over to a maintainable fork-plus-patch model second, resync the risky `models/ltx2/` surface third, and finish with sustainability controls last.
7	
8	The non-negotiable constraint is that no functionality may be lost during any sprint. The plan therefore treats these as protected behaviors that must survive with explicit verification: IC-LoRA auto-injection for pose, depth, canny, and cameraman modes; the newly landed `ltx_anchor` kind; the existing `ltx_control` pixel cross-fade guide-video path; the `ltx_hybrid` route; `clear_conditioning` keyframe-token stripping before VAE decode; the existing 6-file travel test suite; and the import-path contract that supports both dotted `Wan2GP.*` callers and bare-module callers.
9	
10	## 2. Current-State Inventory
11	
12	### 2a. Vendored tree facts
13	`reigh-worker/Wan2GP/` is currently a plain copied tree rather than a repository checkout, so there is no `.git` metadata to rebase, cherry-pick, or diff-history against. The vendored changelog currently tops out at `WanGP v10.01` dated January 1, 2026, while upstream context for this plan is `v10.951` dated February 19, 2026.
14	
15	The hottest resync zone is `Wan2GP/models/ltx2/`, where the working comparison indicates 22 differing files and about 4303 lines of diff. That is large enough that the migration cannot safely be framed as a single blind replacement.
16	
17	The repo also has a non-trivial import and runtime surface already coupled to the current mount path. The approved background for this plan treats that as a 26+ call-site contract, which is why the migration must preserve both filesystem location and import semantics rather than just swapping in a dependency reference.
18	
19	### 2b. Genuinely missing upstream items
20	The current vendored tree is missing several upstream features that are desired outcomes of the migration rather than already-carried drift. Confirmed missing items include `Wan2GP/models/ltx2/ltx_pipelines/utils/res2s.py` and `Wan2GP/defaults/ltx2_22B_distilled_1_1.json`.
21	
22	Other upstream-side capabilities that this design document should plan to absorb during the migration include `_apply_gamma_to_media`, `LTX2_OUTPAINT_GAMMA`, `LTX2_DISABLE_STAGE2_WITH_CONTROL_VIDEO`, and the newer prompt-enhancer improvements. These belong in the migration inventory because they are feature gaps, not just cleanup opportunities.
23	
24	### 2c. Already-vendored drift-only items
25	`Wan2GP/shared/utils/self_refiner.py` is already vendored in the current tree. It should therefore be treated as a drift candidate that may need reconciliation with upstream head, not as a missing upstream backfill.
26	
27	That distinction matters for sprint design: Sprint 2 can absorb `self_refiner` drift as a low-risk resync task, while `res2s.py` and `ltx2_22B_distilled_1_1.json` remain true additions.
28	
29	### 2d. Patch seam and lifecycle
30	The repo already has an established patch seam for Wan2GP-specific runtime behavior. The module-load trigger is `source/__init__.py:6`, which ensures `source.models.wgp.wgp_patches` is importable during bootstrap.
31	
32	Actual patch application happens later in the runtime lifecycle at `source/models/wgp/orchestrator.py:265-266`, where `apply_all_wgp_patches(wgp, self.wan_root)` is called after the Wan2GP module is loaded and before orchestration proceeds. The migration plan should preserve this existing seam instead of introducing a second patch package.
33	
34	### 2e. banodoco-carry items
35	Some behaviors are not generic upstream drift and must be treated as load-bearing banodoco carry items until they are either upstreamed or deliberately relocated. The clearest examples are `clear_conditioning` in `Wan2GP/models/ltx2/ltx_core/tools.py:66-79`, the `_IC_LORA_BY_MODE` registry in `source/core/params/travel_guidance.py`, and the `ltx_anchor`-related orchestrator rewiring around `_build_segment_anchor_guidance_config`, PATH A skip behavior, and segment-local anchor remapping.
36	
37	These items are the reason the migration cannot be framed as “replace vendor tree with upstream head.” Each one needs an explicit carry-location decision later in the plan.
38	
39	### 2f. Pre-existing test coverage gaps
40	The current test suite does not yet pin the cameraman-specific override branch or the task-registry dedup branch. T1 confirmed that current collected cameraman coverage is limited to `test_parse_ltx_control_cameraman` and `test_needs_ic_lora[cameraman-True]`, and neither one reaches `get_ic_lora_entry()`.
41	
42	That leaves the cameraman override branch at `source/core/params/travel_guidance.py:310-313` and the dedup logic at `source/task_handlers/tasks/task_registry.py:964-968` unexercised by current tests. Sprint 3 therefore needs new first-class test deliverables rather than relying on `-k` selectors over the existing suite.
43	
44	### 2g. Stale-doc inventory
45	T1 identified existing documentation that still describes `Wan2GP/` as a flat vendored tree prior to Sprint 2. Confirmed narrow-sweep hits are `README.md:39`, `STRUCTURE.md:22`, and `docs/KIJAI_SVI_IMPLEMENTATION.md:202`.
46	
47	The broader sweep also found `STRUCTURE.md:70`, which still describes `Wan2GP/` as “Upstream video generation engine (vendored, do-not-edit-in-place).” Sprint 2 therefore needs a doc-sweep gate that covers both the narrow regex and the broader `Wan2GP` plus `vendor` pass, followed by manual reviewer confirmation because the regex is heuristic.
48	
49	### 2h. Invocation contract
50	The repo’s test and worker invocation contract is `uv run --python 3.10 pytest …`, consistent with the locked Python 3.10 environment in `uv.lock` and the worker run examples in `docs/KIJAI_SVI_IMPLEMENTATION.md:195`. This document should treat that as the canonical pytest invocation form for every later verification gate.
```

> AGENT

Perfect! Now let me read the rest of the migration plan to understand the context for Sprint 3:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/docs/WAN2GP_FORK_MIGRATION_PLAN.md",
  "offset": 50,
  "limit": 150
}
```

> TOOL

tool_result Read
```
50	The repo’s test and worker invocation contract is `uv run --python 3.10 pytest …`, consistent with the locked Python 3.10 environment in `uv.lock` and the worker run examples in `docs/KIJAI_SVI_IMPLEMENTATION.md:195`. This document should treat that as the canonical pytest invocation form for every later verification gate.
51	
52	Plain `pytest` is not sufficient in this repo because it can fail with `ModuleNotFoundError: source` when the expected environment contract is not active. The migration plan therefore needs to standardize on the `uv run --python 3.10` prefix anywhere it names pytest.
53	
54	### 2i. Path-contract verification technique
55	The path contract has two caller classes that must both survive the migration. First, `ensure_wan2gp_on_path()` inserts the absolute `Wan2GP/` directory itself into `sys.path`, not the repo root. Second, the more common dotted `Wan2GP.*` callers can work when either the repo root or `Wan2GP/` is on `sys.path`, so they are necessary but not sufficient proof that the mount contract remains correct.
56	
57	The stricter contract is driven by the bare-module callers in `vendor_imports.py:76-88`: `models.qwen.qwen_handler`, `shared.utils.loras_mutipliers`, and `models.qwen.qwen_main`. Those class-b callers require the absolute `Wan2GP/` insertion specifically, which is why the Sprint 2 smoke must assert `os.path.abspath(str(get_wan2gp_path())) in [os.path.abspath(p) for p in sys.path]` with no repo-root fallback.
58	
59	Bare-import reachability should be verified only through filesystem proxies such as `os.path.isfile('Wan2GP/models/qwen/qwen_handler.py')`, `os.path.isfile('Wan2GP/models/qwen/qwen_main.py')`, and `os.path.isfile('Wan2GP/shared/utils/loras_mutipliers.py')`. `find_spec` and real imports on `shared.utils.*` are intentionally avoided because `Wan2GP/shared/utils/__init__.py` eagerly imports SciPy-sensitive solver modules. Full end-to-end validation of the bare-module callers should then come from the existing test suite exercising `vendor_imports.py` through normal codepaths.
60	
61	## 3. Fork Architecture Decisions
62	The migration will use the hybrid architecture defined by SD-001: `banodoco/Wan2GP` becomes the long-running fork, and `reigh-worker/Wan2GP/` becomes a git submodule pinned to that fork rather than a flat copied tree. That choice keeps the existing filesystem contract stable while making future rebases, drift review, and upstream comparison mechanically possible again.
63	
64	Patch ownership is split deliberately rather than informally. SD-002 defines the required triage buckets so every deviation is classified as accept-upstream, upstreamable, banodoco-fork-or-banodoco-patch, or cruft; SD-003 stages the resync by subsystem so low-risk `shared/` and `postprocessing/` work lands before the hot `models/ltx2/` zone; and SD-004 keeps LTX 2.3 distilled 1.1 default promotion out of the migration path so the migration is not coupled to a defaults experiment.
65	
66	Feature exposure is also staged. SD-005 keeps `res_2s` and `self_refiner` behind off-by-default flags until the fork relationship is stable, and SD-006 keeps any post-gen detailer work outside this initiative so the migration remains focused on source-of-truth and drift control instead of product expansion.
67	
68	Sustainability is handled as part of the architecture, not as follow-up cleanup. SD-007 sets a monthly rebase cadence with event-triggered syncs on upstream minor-version bumps, while SD-008 adds scheduled drift detection in CI so the repository does not slide back into another opaque vendor snapshot. Together, SD-001 through SD-008 define a maintainable fork-plus-patch-layer model rather than a one-time resync.
69	
70	## 4. Sprint Plan (4 × 2 weeks)
71	### Sprint 1 — Triage & Fork Cut (Weeks 1-2)
72	#### Goals
73	- Fork `banodoco/Wan2GP` at upstream HEAD and establish it as the future source of truth.
74	- Build `docs/wan2gp-triage.csv` and classify every differing file into the SD-002 buckets.
75	- Pre-classify `clear_conditioning` as bucket `(c)` before any hot-zone resync begins.
76	
77	#### Deliverables
78	- `banodoco/Wan2GP` fork created and available for migration work.
79	- `docs/wan2gp-triage.csv` with rows covering the 22-file `models/ltx2/` hot zone and every differing file elsewhere.
80	
81	#### Verification Gates
82	- `docs/wan2gp-triage.csv` contains at least one row for every differing file and explicit bucket decisions for all 22 `models/ltx2/` files.
83	- The `clear_conditioning` row remains pre-classified as bucket `(c)` with an explicit carry location and verification entry.
84	
85	#### Rollback Plan
86	- Record tag `wan2gp-mig-sprint-1-baseline` before opening the fork workstream.
87	- No `reigh-worker` code changes are planned in this sprint; if the fork cut is rejected, abandon the fork workstream and leave `reigh-worker` at `wan2gp-mig-sprint-1-baseline`.
88	
89	#### Functionality-Preservation Checks
90	- Zero `reigh-worker` code changes means zero risk to IC-LoRA behavior, `ltx_anchor`, `ltx_control`, `ltx_hybrid`, `clear_conditioning`, and the path/import contract during Sprint 1.
91	- The only outputs are the fork setup and the triage artifact, so every protected behavior is preserved by construction.
92	
93	### Sprint 2 — Submodule Cut-over, Low-Risk Resync, Doc Updates (Weeks 3-4)
94	#### Goals
95	- Replace the flat `Wan2GP/` tree with a git submodule at the same mount path.
96	- Resync `shared/` and `postprocessing/`, absorb `self_refiner` drift, and introduce `res2s.py` behind an off-by-default flag per SD-005.
97	- Update all stale docs identified in T1.
98	
99	#### Deliverables
100	- `.gitmodules` plus the submodule mounted at `reigh-worker/Wan2GP/`.
101	- `Wan2GP/shared/utils/self_refiner.py` aligned to fork HEAD.
102	- `Wan2GP/models/ltx2/ltx_pipelines/utils/res2s.py` present and gated off by default.
103	- `README.md`, `STRUCTURE.md`, and `docs/KIJAI_SVI_IMPLEMENTATION.md` updated to remove pre-Sprint-2 vendored-tree wording.
104	
105	#### Verification Gates
106	- Strict path-contract smoke:
107	  > ```bash
108	  > python -c "import os, sys; from source.core.runtime_paths import ensure_wan2gp_on_path, get_wan2gp_path; ensure_wan2gp_on_path(); assert os.path.abspath(str(get_wan2gp_path())) in [os.path.abspath(p) for p in sys.path]; assert os.path.isfile('Wan2GP/models/qwen/qwen_handler.py'); assert os.path.isfile('Wan2GP/models/qwen/qwen_main.py'); assert os.path.isfile('Wan2GP/shared/utils/loras_mutipliers.py'); assert os.path.isfile('Wan2GP/shared/utils/self_refiner.py'); assert os.path.isfile('Wan2GP/models/ltx2/ltx_core/tools.py'); print('path-contract smoke OK')"
109	  > ```
110	- Full 6-file suite:
111	  `uv run --python 3.10 pytest tests/test_travel_guidance_config.py tests/test_travel_ltx_vpt.py tests/test_ltx_hybrid_travel.py tests/test_ltx_hybrid_vgkfi.py tests/test_travel_payload_contracts.py tests/test_travel_orchestrator_terminal_gating.py`
112	- LTX-2 `self_refiner` smoke against the pre-sprint behavioral baseline.
113	- Doc-sweep gate: run the two regex sweeps specified in Sprint 2's brief (gate C). Both must return zero hits across `docs/`, `README.md`, and `STRUCTURE.md`. Regex literals are intentionally omitted here to avoid self-matching the gate commands.
114	
115	#### Rollback Plan
116	- Record tag `wan2gp-mig-sprint-2-baseline` before submodule cut-over.
117	- Roll back with `git submodule deinit` plus `git reset --hard wan2gp-mig-sprint-2-baseline`.
118	
119	#### Functionality-Preservation Checks
120	- No `models/ltx2/` files are touched in Sprint 2.
121	- The LTX-2 `self_refiner` smoke remains green.
122	- The strict path-contract smoke remains green and proves that `Wan2GP/` is on `sys.path` and all three bare-import targets still exist.
123	- The doc sweeps plus reviewer pass show no stale wording remains in approved locations.
124	
125	### Sprint 3 — `models/ltx2/` Resync + Write Cameraman/Dedup Tests (Weeks 5-6)
126	#### Goals
127	- Resync the 22-file `models/ltx2/` hot zone while explicitly carrying `clear_conditioning`.
128	- Add `ltx2_22B_distilled_1_1.json` as available-but-not-default per SD-004.
129	- Reconcile upstream `guide_phases=1` behavior and write the missing cameraman and dedup coverage as first-class deliverables.
130	
131	#### Deliverables
132	- `models/ltx2/` resynced against the fork.
133	- `clear_conditioning` preserved as byte-identical on a saved latent fixture.
134	- New file `tests/test_travel_guidance_ic_lora_override.py` containing `test_get_ic_lora_entry_cameraman_returns_cseti_url`, which builds `TravelGuidanceConfig(kind="ltx_control", mode="cameraman", ...)`, calls `get_ic_lora_entry()`, asserts `path == "https://huggingface.co/Cseti/LTX2.3-22B_IC-LoRA-Cameraman_v1/resolve/main/LTX2.3-22B_IC-LoRA-Cameraman_v1_10500.safetensors"`, `name == "ic-lora-cameraman (auto-injected)"`, and strength matches config, and `test_get_ic_lora_entry_pose_falls_back_to_union_control`, which uses `mode="pose"` and asserts the path equals the `_IC_LORA_UNION_CONTROL` filename.
135	- New file `tests/test_task_registry_ic_lora_dedup.py` containing `test_dedup_updates_strength_when_basename_matches`, which seeds `segment_loras=[{"path": "…/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors", "strength": 0.4}]`, drives auto-inject with the same basename at strength `0.8`, and asserts length `1` plus `strength == 0.8`, and `test_dedup_appends_when_no_match`, which seeds an empty list and asserts the injected entry appears once.
136	
137	#### Verification Gates
138	- New IC-LoRA tests:
139	  `uv run --python 3.10 pytest tests/test_travel_guidance_ic_lora_override.py tests/test_task_registry_ic_lora_dedup.py`
140	- Full 6-file suite:
141	  `uv run --python 3.10 pytest tests/test_travel_guidance_config.py tests/test_travel_ltx_vpt.py tests/test_ltx_hybrid_travel.py tests/test_ltx_hybrid_vgkfi.py tests/test_travel_payload_contracts.py tests/test_travel_orchestrator_terminal_gating.py`
142	- `clear_conditioning` byte-compare against a saved latent fixture.
143	- PATH A skip gate:
144	  `uv run --python 3.10 pytest tests/test_travel_orchestrator_terminal_gating.py`
145	- 20 anchor tests:
146	  `uv run --python 3.10 pytest tests/test_travel_guidance_config.py`
147	- No `pytest -k` selectors involving `cameraman` or `ic_lora and cameraman` are used anywhere in the sprint.
148	
149	#### Rollback Plan
150	- Record tag `wan2gp-mig-sprint-3-baseline` before the `models/ltx2/` resync.
151	- Revert the submodule pointer to the Sprint 2 state and run `git reset --hard wan2gp-mig-sprint-3-baseline`.
152	
153	#### Functionality-Preservation Checks
154	- The cameraman override branch is pinned by `test_get_ic_lora_entry_cameraman_returns_cseti_url`.
155	- The pose fallback branch is pinned by `test_get_ic_lora_entry_pose_falls_back_to_union_control`.
156	- Dedup is pinned by `test_dedup_updates_strength_when_basename_matches` and `test_dedup_appends_when_no_match`.
157	- `clear_conditioning` remains byte-identical.
158	- `ltx_anchor` PATH A skip remains intact.
159	- `ltx_control` pixel cross-fade remains intact.
160	- `ltx_hybrid` remains unchanged.
161	- The 26+ `Wan2GP.*` call sites and the bare-module callers still resolve after the hot-zone resync.
162	
163	### Sprint 4 — Patch Consolidation, Upstream PRs, Sustainability (Weeks 7-8)
164	#### Goals
165	- Extend `source/models/wgp/wgp_patches.py` using the existing runtime-patch primitives.
166	- Open upstream PRs for bucket `(b)` items.
167	- Land drift CI per SD-008 and publish the rebase runbook required by SD-007.
168	
169	#### Deliverables
170	- `source/models/wgp/wgp_patches.py` extended using the existing `_register_patch_application`, `begin_runtime_model_patch`, and `rollback_runtime_model_patch` primitives.
171	- Draft upstream PRs for upstreamable hunks.
172	- `.github/workflows/wan2gp-drift.yml` merged.
173	- `docs/wan2gp-rebase-runbook.md` published.
174	
175	#### Verification Gates
176	- Drift CI runs once successfully.
177	- Full regression suite:
178	  `uv run --python 3.10 pytest tests/test_travel_guidance_config.py tests/test_travel_ltx_vpt.py tests/test_ltx_hybrid_travel.py tests/test_ltx_hybrid_vgkfi.py tests/test_travel_payload_contracts.py tests/test_travel_orchestrator_terminal_gating.py tests/test_travel_guidance_ic_lora_override.py tests/test_task_registry_ic_lora_dedup.py`
179	- Patch-lifecycle smoke drives bootstrap to `source/models/wgp/orchestrator.py:265-266` via `apply_all_wgp_patches(wgp, self.wan_root)` and only then inspects `get_wgp_patch_state()`.
180	
181	#### Rollback Plan
182	- Record tag `wan2gp-mig-sprint-4-baseline` before patch consolidation lands.
183	- Because the Sprint 4 additions are isolated to `source/models/wgp/wgp_patches.py`, roll back with `git reset --hard wan2gp-mig-sprint-4-baseline` or disable the runtime patch context through `_PATCH_CONTEXT_ROLLBACKS`.
184	
185	#### Functionality-Preservation Checks
186	- Re-run the full Sprint 3 regression matrix.
187	- Confirm that patch-state verification sees a single registry rather than split runtime patch state.
188	
189	## 5. Functionality Preservation Matrix
190	| Behavior | Defining location | Sprint verifying it | Verification step |
191	| --- | --- | --- | --- |
192	| IC-LoRA union-control fallback for pose/depth/canny | `source/core/params/travel_guidance.py:314` plus `source/task_handlers/tasks/task_registry.py:955-987` | Sprint 3 | `tests/test_travel_guidance_ic_lora_override.py::test_get_ic_lora_entry_pose_falls_back_to_union_control` |
193	| IC-LoRA cameraman override | `source/core/params/travel_guidance.py:310-313` plus `_IC_LORA_BY_MODE` at `source/core/params/travel_guidance.py:32-37` | Sprint 3 | `tests/test_travel_guidance_ic_lora_override.py::test_get_ic_lora_entry_cameraman_returns_cseti_url` |
194	| IC-LoRA dedup | `source/task_handlers/tasks/task_registry.py:961-968` | Sprint 3 | `tests/test_task_registry_ic_lora_dedup.py::test_dedup_updates_strength_when_basename_matches` plus `tests/test_task_registry_ic_lora_dedup.py::test_dedup_appends_when_no_match` |
195	| Pixel cross-fade guide video for `ltx_control` | `source/media/video/travel_guide.py` | Sprint 3 | `uv run --python 3.10 pytest tests/test_ltx_hybrid_travel.py` plus manual smoke |
196	| `ltx_anchor` kind survives the resync | `source/task_handlers/travel/orchestrator.py:134,231,1272-1289,2115,2126` | Sprint 3 | `uv run --python 3.10 pytest tests/test_travel_guidance_config.py` |
197	| `clear_conditioning` keyframe strip before VAE decode | `Wan2GP/models/ltx2/ltx_core/tools.py:66-79` | Sprint 3 | Byte-compare against saved latent fixture |
198	| PATH A skip for `ltx_anchor` | `source/task_handlers/travel/orchestrator.py:1272-1289` | Sprint 3 | `uv run --python 3.10 pytest tests/test_travel_orchestrator_terminal_gating.py` |
199	| `_build_segment_anchor_guidance_config` rename remains intact | `source/task_handlers/travel/orchestrator.py:178` | Sprint 3 | `uv run --python 3.10 pytest tests/test_travel_guidance_config.py` |
```

> AGENT

Excellent! Now let me verify the exact content of the clear_conditioning function and check one more key registry detail:

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/ltx_core/tools.py"
}
```

> TOOL

tool_result Bash
```
188 /Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/ltx_core/tools.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "_IC_LORA_UNION_CONTROL",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py",
  "output_mode": "content",
  "context": 3
}
```

> TOOL

tool_result Grep
```
28-
29-# IC LoRA registry: mode → (filename, optional download URL).
30-# Modes not listed fall back to the preloaded union-control LoRA.
31:_IC_LORA_UNION_CONTROL = "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"
32-_IC_LORA_BY_MODE: dict[str, tuple[str, str | None]] = {
33-    "cameraman": (
34-        [REDACTED],
--
311-        if mode_entry is not None:
312-            filename, url = mode_entry
313-        else:
314:            filename, url = _IC_LORA_UNION_CONTROL, None
315-
316-        strength = (
317-            self.control_strength if self.is_ltx_hybrid else self.strength
```

> AGENT

Perfect! Now let me create a concise final report with all the key findings:

## Sprint 3 Baseline Findings Report

### 1. Wan2GP Submodule State
**File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.gitmodules`
- Wan2GP IS a git submodule (lines 1-4)
- Branch pinned to: `reigh-sprint-2`
- URL: `https://github.com/banodoco/Wan2GP.git`
- Directory: `Wan2GP/` at repo root

**Status:** Git submodule is already configured from Sprint 2. Awaiting branch creation for `reigh-sprint-3` on the banodoco fork.

### 2. Models/ltx2 Hot Zone — Current Baseline

**File Structure:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/` exists with subdirectories:
- `configs/` (ltx2_22b_config.json, ltx2_19b_config.json, ltx2_rgb_factors.json)
- `ltx_core/` (contains tools.py)
- `ltx_pipelines/` (contains utils/ subdirectory)
- Total tools.py file: 188 lines

**clear_conditioning Function:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/models/ltx2/ltx_core/tools.py:66-79`
```python
def clear_conditioning(self, latent_state: LatentState) -> LatentState:
    """
    Clear the conditioning from the latent state. This method removes extra tokens from the end of the latent.
    Therefore, conditioning items should add extra tokens ONLY to the end of the latent.
    """
    latent_state = latent_state.clone()

    num_tokens = self.patchifier.get_token_count(self.target_shape)
    latent = latent_state.latent[:, :num_tokens]
    clean_latent = latent_state.clean_latent[:, :num_tokens]
    denoise_mask = torch.ones_like(latent_state.denoise_mask)[:, :num_tokens]
    positions = latent_state.positions[:, :, :num_tokens]

    return LatentState(latent=latent, denoise_mask=denoise_mask, positions=positions, clean_latent=clean_latent)
```

**Defaults:** `ltx2_22B_distilled.json` exists at `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/Wan2GP/defaults/ltx2_22B_distilled.json`. **Missing:** `ltx2_22B_distilled_1_1.json` (planned addition per Sprint 3 spec, not yet present).

### 3. IC-LoRA Registry & Override Code

**File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/core/params/travel_guidance.py`

**Registry Location (lines 29-37):**
```python
_IC_LORA_UNION_CONTROL = "ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors"
_IC_LORA_BY_MODE: dict[str, tuple[str, str | None]] = {
    "cameraman": (
        [REDACTED],
        "https://huggingface.co/Cseti/LTX2.3-22B_IC-LoRA-Cameraman_v1/resolve/main/LTX2.3-22B_IC-LoRA-Cameraman_v1_10500.safetensors",
    ),
}
```

**get_ic_lora_entry() Method (lines 305-325):**
- Returns `None` if `needs_ic_lora()` is False
- For cameraman: uses URL from `_IC_LORA_BY_MODE` with strength
- For pose/depth/canny: falls back to `_IC_LORA_UNION_CONTROL` (filename only, no URL)
- Strength is pulled from `control_strength` (hybrid) or `strength` (ltx_control)
- Returns dict with keys: `path`, `strength`, `name`

**TravelGuidanceConfig Dataclass (lines 122-151):**
- `kind` field (Literal, default "none")
- `strength` field (float, default 0.0) — YES, exists at line 130
- `mode` field (str, default "")
- `control_strength` field (float, default 1.0)
- All control modes: `{"pose", "depth", "canny", "video", "cameraman"}` (line 27)

### 4. Task Registry Dedup Logic

**File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/source/task_handlers/tasks/task_registry.py:940-990`

**IC LoRA Auto-Inject + Dedup Flow (lines 955-970):**
- Triggers when `structure.structure_config` is `TravelGuidanceConfig` instance
- Calls `structure.structure_config.get_ic_lora_entry()` (line 958)
- Dedup compares `os.path.basename(existing.get("path", ""))` against `ic_basename` (lines 962-968)
- If match found: updates `strength` in-place and sets `found = True`
- If no match: appends `ic_entry` to `segment_loras` list
- Each dict item in `segment_loras` expects keys: `"path"` and `"strength"`

### 5. Existing Test Patterns

**File:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/test_travel_guidance_config.py:1-80`

**Imports & Fixtures:**
- Line 1: `import pytest`
- Lines 2-8: Standard imports (ast, sys, textwrap, types, contextlib, pathlib, SimpleNamespace)
- Lines 10-11: Import `TravelGuidanceConfig` from `source.core.params.travel_guidance`
- Line 14-19: `VIDEO_ENTRY` dict constant with fields: `path`, `start_frame`, `end_frame`, `treatment`
- Lines 20-21: Model name constants: `LTX_DISTILLED_MODEL = "ltx2_22B_distilled"`, `VACE_MODEL = "wan_2_2_vace_lightning_baseline_2_2_2"`

**Test Examples (lines 40-72):**
- `test_parse_each_travel_guidance_kind()` — instantiates with `from_payload()`
- `test_parse_ltx_control_cameraman()` — existing cameraman test (NOT reaching get_ic_lora_entry)
- Uses `@pytest.mark.parametrize` for multi-case tests

**conftest.py:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/tests/conftest.py:1-18`
- Minimal setup: temp directories for matplotlib and XDG cache
- No saved fixtures found (no `.pt`, `.npy`, `.safetensors` under `tests/`)

### 6. clear_conditioning Fixture Status

**Search Result:** No existing saved latent fixture found in `tests/` or `fixtures/` directories.
- No `.pt`, `.safetensors`, `.npy` files under `tests/`
- No references to `clear_conditioning` in test files
- No prior latent capture script found in `scripts/`

**Action Required:** Sprint 3 must create a saved latent fixture to enable byte-compare verification per the migration plan.

### 7. scripts/live_test/ Directory

**Contents:** `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/scripts/live_test/` is a full smoke/matrix test harness with 25 Python modules:
- `completion_poller.py`, `config.py`, `git_ops.py`, `heartbeat_waiter.py`, `launch_command.py`
- `smoke.py` — smoke test orchestration
- `matrix.py`, `variant_fresh.py`, `variant_update.py` — test matrix definition & variant management
- `stage1_findings.md` — detailed stage 1 probe output (18KB)
- Fully instrumented for SSH bootstrap, task spoofing, and multi-stage validation

**Status:** This is the Sprint 2 smoke test infrastructure. Can be reused for Sprint 3 verification if needed.

### 8. Sprint 2 Venv References

**Search Result:** No `/tmp/sprint2-smoke-venv` references found in codebase.
- `.megaplan/` directory exists with plan execution artifacts
- `/Users/user_c042661f/Documents/reigh-workspace/reigh-worker/.megaplan/plans/execute-sprint-2-of-the-20260421-2202/` contains execution logs and batch files
- No explicit pip install commands recorded for venv setup in megaplan outputs

### 9. Current Baseline Tags

**Result:** No `wan2gp-mig-*` tags exist yet. Tags should be created per migration plan:
- `wan2gp-mig-sprint-1-baseline` (not yet created)
- `wan2gp-mig-sprint-2-baseline` (not yet created)
- `wan2gp-mig-sprint-3-baseline` (should be created before Sprint 3 models/ltx2 resync begins)

### 10. Git Status & Untracked Files

**Current State:** Two untracked files:
- `docs/wan2gp-triage.csv` — Sprint 1 artifact (22-file bucket classification)
- `scripts/live_test/` — Sprint 2 smoke test harness (directory)

---

**Ready for Plan:** All baseline facts collected. Submodule is in place on `reigh-sprint-2` branch. IC-LoRA registry, dedup logic, and clear_conditioning function are correctly located and readable. Test suite framework is in place but cameraman/dedup coverage is missing. No saved fixture yet; must be created for verification gate.
