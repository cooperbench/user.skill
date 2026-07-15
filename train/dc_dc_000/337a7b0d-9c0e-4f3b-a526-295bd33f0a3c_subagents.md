> DEVELOPER

Context: a multi-agent planning tool (megaplan) recently completed an M1-M6 state-management refactor in the reigh-app repo (a React/Zustand/React-Query app) at `/Users/user_c042661f/Documents/reigh-workspace/reigh-app`. The refactor replaced some React Contexts with Zustand stores to kill render storms. After pulling the chain's work locally, three browser-breaking bugs surfaced, all from the same anti-pattern: the new stores *mirror* state that's already authoritative elsewhere (RQ, React Context, Base UI popup open-state), with sync bridges that feedback-loop.

Bugs found today (each already patched as a symptom, not root):
1. `src/shared/state/panesStore.ts:519` — `bootstrapPanesStore(input)` called in render body → setState-in-render → app unclickable. Patched by moving to useEffect.
2. `src/shared/components/ui/overlay/select.tsx:198` via `src/shared/components/ui/overlay/overlayBridge.tsx` — Select registers as modal at mount (popup ref-attach) regardless of open state → `document.body.style.pointerEvents = 'none'` at mount → nothing clickable. Patched by gating `getTopModalOverlay` on `data-state`/`data-open` DOM attributes in `src/shared/state/overlayStack.ts`.
3. `src/shared/settings/hooks/useAutoSaveSettings.ts:304` — bootstrap `useEffect` copies React Query data (`useToolSettings` via line 215) into Zustand store (`createEntityStore`) on every effect fire; deep-equal guard compared against store state which other paths mutated, so guard never short-circuited → infinite update depth. Patched by adding a `lastBootstrapRef` self-tracking guard.

Adjacent latent sites with the same class (found via grep):
- `src/domains/media-lightbox/hooks/useLastUsedEditSettings.ts:155-179` — line-for-line same RQ→store sync as useAutoSaveSettings
- `src/shared/settings/hooks/useAutoSaveSettings.ts:275-302` — second bootstrap effect in same file (custom-mode path)
- `src/tools/video-editor/hooks/useTimelineState.ts:814` — `syncInitialTimelineStoreBootstrap` called in render body
- `src/shared/components/ui/overlay/{dialog,alert-dialog,lightbox,popover,dropdown-menu}.tsx` — all use `useOverlayBridge` with `modal: true` and ref-attach registration; the Select bug is a template

I just outlined seven principles of "excellent engineering" for this cleanup:
1. Failing test before each patch (testing-library with full provider tree, not Playwright)
2. Understand why the mirror existed before deleting it
3. Make the class impossible, not the instance fixed (e.g., `useOverlayBridge({ open })` required prop)
4. Delete more than you add (one source of truth per state concept)
5. Write down the rule (one markdown file, linked from CLAUDE.md)
6. Don't ship debug logs (`[PanesBoot]`, `[OverlayStack]`, `[AutoSave]` console.logs I added must go or be gated)
7. Own the followup list (tickets with owner+date)

The user is pushing back on vague prescriptions and wants to know what excellent engineering looks like **concretely for this codebase**.

Your task: read the actual code at the sites above and produce a concrete per-site action plan that an engineer could execute in 2-3 focused days. For each of the 5+ sites:
- What's the ONE failing test that encodes the bug? (File path and 5-10 line spec, runnable with vitest + testing-library)
- What's the minimal code change that makes it pass? (File, function, before/after in diff-fragment form, 5-15 lines each)
- What lines of code get DELETED in the process (make the change a net negative)?
- Is the mirror pattern load-bearing here? Git-blame / read plan metadata under `.megaplan/plans/milestone-m1-*` and `milestone-m1a-*` and `milestone-m4-*` to find the original justification. State your finding honestly — if you can't find a reason, say so.

Also answer these specifically:
- For `useAutoSaveSettings`, is there any consumer that actually depends on the store's `cleanSnapshot` being kept in sync with RQ? If no, the mirror is dead code and can be removed outright. If yes, identify the consumer.
- For `useOverlayBridge`, is there any caller that legitimately needs to register before being open? Or can the API be changed to require `open: boolean` across the board without breakage?
- For `panesStore`, does `usePaneLockPolicyState` still have other readers, or is the store the only consumer? If the store is the only consumer, we can delete the context.
- For `useTimelineState.ts:814`, is the render-body bootstrap compensating for a first-paint ordering issue? What breaks if you move it to useLayoutEffect?

Propose concrete tickets (title + one-line scope + suggested acceptance test). Not a megaplan chain — these are handwritten tickets an engineer picks up one at a time.

Budget: under 800 words in your report. Be specific with file:line references. Be honest about unknowns — "didn't find clear evidence" is a valid answer. The user explicitly asked me to stop spiraling with hedges, so your proposals should be actionable, not "it depends."

> AGENT

I'll investigate each site concretely.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/state/panesStore.ts",
  "offset": 490,
  "limit": 60
}
```

> TOOL

tool_result Read
```
490	    setIsEditorPaneLocked,
491	    setIsShotsPaneLocked,
492	    setIsTasksPaneLocked,
493	    setIsGenerationsPaneOpen,
494	    setIsEditorPaneOpen,
495	    setIsTasksPaneOpen,
496	    resetAllPaneLocks,
497	  }), [
498	    locks,
499	    isGenerationsPaneOpenState,
500	    isEditorPaneOpenState,
501	    isTasksPaneOpenState,
502	    setIsGenerationsPaneLocked,
503	    setIsEditorPaneLocked,
504	    setIsShotsPaneLocked,
505	    setIsTasksPaneLocked,
506	    setIsGenerationsPaneOpen,
507	    setIsEditorPaneOpen,
508	    setIsTasksPaneOpen,
509	    resetAllPaneLocks,
510	  ]);
511	
512	  console.log('[PanesBoot] useBootstrapPanesStore render', {
513	    owner: ownerRef.current?.toString(),
514	    inputId: bootstrapInput && (bootstrapInput as unknown as { __id?: number }).__id,
515	  });
516	
517	  useEffect(() => {
518	    console.log('[PanesBoot] effect fires (bootstrapInput changed identity)');
519	    bootstrapPanesStore(bootstrapInput);
520	  }, [bootstrapInput]);
521	
522	  useEffect(() => {
523	    return () => {
524	      console.log('[PanesBoot] CLEANUP unmount', { owner: ownerRef.current?.toString() });
525	      clearPanesStoreBootstrap(ownerRef.current ?? undefined);
526	    };
527	  }, []);
528	}
529	
530	export function PanesStoreBootstrapBoundary({ children }: { children: ReactNode }) {
531	  console.log('[PanesBoot] PanesStoreBootstrapBoundary render');
532	  useBootstrapPanesStore();
533	  return children;
534	}
535	
536	export function __resetPanesStoreForTests(): void {
537	  resetPanesStore();
538	}
539
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/components/ui/overlay/select.tsx",
  "offset": 180,
  "limit": 50
}
```

> TOOL

tool_result Read
```
180	const SelectContent = React.forwardRef<HTMLDivElement, SelectContentProps>(
181	  (
182	    {
183	      className,
184	      children,
185	      position = 'popper',
186	      header,
187	      container,
188	      variant,
189	      side = 'bottom',
190	      sideOffset = 0,
191	      align,
192	      style,
193	      ...props
194	    },
195	    ref,
196	  ) => {
197	    const modal = React.useContext(SelectModalContext);
198	    const bridge = useOverlayBridge({ type: 'select', modal });
199	    const layer = useOverlayLayer(bridge.handle.id);
200	    const popupRef = React.useMemo(
201	      () => composeRefs(ref, (node: HTMLDivElement | null) => bridge.registerElement('popup', node)),
202	      [bridge, ref],
203	    );
204	    const isCompact = variant === 'retro' || variant === 'retro-dark' || variant === 'zinc';
205	    const isPopper = position === 'popper';
206	
207	    return (
208	      <SelectPrimitive.Portal container={container ?? undefined}>
209	        <OverlayInstanceProvider value={bridge}>
210	          <SelectPrimitive.Positioner
211	            side={side}
212	            sideOffset={sideOffset}
213	            align={align}
214	            alignItemWithTrigger={!isPopper}
215	            style={getOverlayLayerStyle(layer, 'positioner')}
216	          >
217	            <SelectPrimitive.Popup
218	              ref={popupRef}
219	              className={cn(
220	                selectContentVariants({ variant }),
221	                isPopper &&
222	                  'data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1',
223	                className,
224	              )}
225	              style={style}
226	              onClick={(e: React.MouseEvent) => e.stopPropagation()}
227	              {...props}
228	            >
229	              {header}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/components/ui/overlay/overlayBridge.tsx"
}
```

> TOOL

tool_result Read
```
1	import * as React from 'react';
2	import {
3	  useIsOverlayTopmost,
4	  useOverlayStackApi,
5	  useTopmostOverlayContainingElement,
6	} from '@/shared/state/overlayStack';
7	
8	export type OverlayElementKind = 'popup' | 'backdrop';
9	
10	interface OverlayElements {
11	  popup: HTMLElement | null;
12	  backdrop: HTMLElement | null;
13	}
14	
15	export interface OverlayHandle {
16	  id: string;
17	  getType: () => string;
18	  isModal: () => boolean;
19	  getElement: (kind: OverlayElementKind) => HTMLElement | null;
20	  getElements: () => readonly HTMLElement[];
21	  isRegistered: () => boolean;
22	  containsElement: (element: Element | null) => boolean;
23	}
24	
25	export interface UseOverlayBridgeOptions {
26	  id?: string;
27	  type: string;
28	  modal?: boolean;
29	  restoreFocusTo?: HTMLElement | null;
30	}
31	
32	interface OverlayBridgeContextValue {
33	  handle: OverlayHandle;
34	  registerElement: (kind: OverlayElementKind, element: HTMLElement | null) => void;
35	}
36	
37	const OverlayBridgeContext = React.createContext<OverlayBridgeContextValue | null>(null);
38	
39	const OVERLAY_ID_PREFIX = 'overlay';
40	
41	function isHTMLElement(value: unknown): value is HTMLElement {
42	  return value instanceof HTMLElement;
43	}
44	
45	function sanitizeOverlayId(id: string): string {
46	  return id.replace(/[^a-zA-Z0-9_-]/g, '-');
47	}
48	
49	function setOverlayMetadata(
50	  element: HTMLElement,
51	  handle: OverlayHandle,
52	  kind: OverlayElementKind,
53	): void {
54	  element.dataset.overlayStackId = handle.id;
55	  element.dataset.overlayStackType = handle.getType();
56	  element.dataset.overlayStackKind = kind;
57	}
58	
59	function clearOverlayMetadata(element: HTMLElement): void {
60	  delete element.dataset.overlayStackId;
61	  delete element.dataset.overlayStackType;
62	  delete element.dataset.overlayStackKind;
63	}
64	
65	function getTrackedElements(elements: OverlayElements): readonly HTMLElement[] {
66	  return [elements.popup, elements.backdrop].filter(isHTMLElement);
67	}
68	
69	function getRestoreFocusTarget(
70	  explicitTarget: HTMLElement | null | undefined,
71	  elements: readonly HTMLElement[],
72	): HTMLElement | null {
73	  if (explicitTarget !== undefined) {
74	    return explicitTarget;
75	  }
76	
77	  const activeElement = document.activeElement;
78	  if (!(activeElement instanceof HTMLElement)) {
79	    return null;
80	  }
81	
82	  if (elements.some((element) => element === activeElement || element.contains(activeElement))) {
83	    return null;
84	  }
85	
86	  return activeElement;
87	}
88	
89	function useOverlayBridgeContextValue(): OverlayBridgeContextValue {
90	  const context = React.useContext(OverlayBridgeContext);
91	  if (!context) {
92	    throw new Error('Overlay bridge hooks must be used within an OverlayInstanceProvider.');
93	  }
94	
95	  return context;
96	}
97	
98	/**
99	 * Creates a stable overlay bridge that registers the overlay only while popup/backdrop
100	 * DOM is actually present and keeps the stack entry updated as refs change.
101	 */
102	export function useOverlayBridge(options: UseOverlayBridgeOptions): OverlayBridgeContextValue {
103	  const stackApi = useOverlayStackApi();
104	  const reactId = React.useId();
105	  const overlayId = React.useMemo(
106	    () => sanitizeOverlayId(options.id ?? `${OVERLAY_ID_PREFIX}-${reactId}`),
107	    [options.id, reactId],
108	  );
109	  const elementsRef = React.useRef<OverlayElements>({ popup: null, backdrop: null });
110	  const registeredRef = React.useRef(false);
111	  const typeRef = React.useRef(options.type);
112	  const modalRef = React.useRef(options.modal ?? false);
113	  const restoreFocusToRef = React.useRef<HTMLElement | null | undefined>(options.restoreFocusTo);
114	
115	  typeRef.current = options.type;
116	  modalRef.current = options.modal ?? false;
117	  restoreFocusToRef.current = options.restoreFocusTo;
118	
119	  const handleRef = React.useRef<OverlayHandle | null>(null);
120	  if (!handleRef.current) {
121	    handleRef.current = {
122	      id: overlayId,
123	      getType: () => typeRef.current,
124	      isModal: () => modalRef.current,
125	      getElement: (kind) => elementsRef.current[kind],
126	      getElements: () => getTrackedElements(elementsRef.current),
127	      isRegistered: () => registeredRef.current,
128	      containsElement: (element) =>
129	        getTrackedElements(elementsRef.current).some(
130	          (candidate) => candidate === element || candidate.contains(element),
131	        ),
132	    };
133	  }
134	  const handle = handleRef.current;
135	
136	  const syncRegistration = React.useCallback(() => {
137	    const elements = getTrackedElements(elementsRef.current);
138	
139	    if (elements.length === 0) {
140	      if (registeredRef.current) {
141	        stackApi.getState().popOverlay(handle.id);
142	        registeredRef.current = false;
143	      }
144	      return;
145	    }
146	
147	    const payload = {
148	      type: handle.getType(),
149	      modal: handle.isModal(),
150	      restoreFocusTo: getRestoreFocusTarget(restoreFocusToRef.current, elements),
151	      elements,
152	    };
153	
154	    if (!registeredRef.current) {
155	      stackApi.getState().pushOverlay({ id: handle.id, ...payload });
156	      registeredRef.current = true;
157	      return;
158	    }
159	
160	    stackApi.getState().updateOverlay(handle.id, payload);
161	  }, [handle, stackApi]);
162	
163	  const registerElement = React.useCallback(
164	    (kind: OverlayElementKind, element: HTMLElement | null) => {
165	      const previous = elementsRef.current[kind];
166	      if (previous === element) {
167	        syncRegistration();
168	        return;
169	      }
170	
171	      if (previous) {
172	        clearOverlayMetadata(previous);
173	      }
174	
175	      elementsRef.current[kind] = element;
176	
177	      if (element) {
178	        setOverlayMetadata(element, handle, kind);
179	      }
180	
181	      syncRegistration();
182	    },
183	    [handle, syncRegistration],
184	  );
185	
186	  React.useEffect(() => {
187	    syncRegistration();
188	  }, [syncRegistration, options.modal, options.restoreFocusTo, options.type]);
189	
190	  React.useEffect(() => {
191	    return () => {
192	      const elements = elementsRef.current;
193	      if (elements.popup) {
194	        clearOverlayMetadata(elements.popup);
195	      }
196	      if (elements.backdrop) {
197	        clearOverlayMetadata(elements.backdrop);
198	      }
199	      if (registeredRef.current) {
200	        stackApi.getState().popOverlay(handle.id);
201	        registeredRef.current = false;
202	      }
203	    };
204	  }, [handle, stackApi]);
205	
206	  return React.useMemo(
207	    () => ({
208	      handle,
209	      registerElement,
210	    }),
211	    [handle, registerElement],
212	  );
213	}
214	
215	/** Provides the current overlay bridge to popup/backdrop descendants. */
216	export function OverlayInstanceProvider({
217	  value,
218	  children,
219	}: React.PropsWithChildren<{ value: OverlayBridgeContextValue }>) {
220	  return (
221	    <OverlayBridgeContext.Provider value={value}>{children}</OverlayBridgeContext.Provider>
222	  );
223	}
224	
225	/** Returns the current overlay handle for bridge-aware descendants. */
226	export function useCurrentOverlayHandle(): OverlayHandle {
227	  return useOverlayBridgeContextValue().handle;
228	}
229	
230	/** Returns a ref callback that registers the popup or backdrop with the overlay stack. */
231	export function useOverlayElementRegistration(
232	  kind: OverlayElementKind,
233	): React.RefCallback<HTMLElement> {
234	  const { registerElement } = useOverlayBridgeContextValue();
235	
236	  return React.useCallback(
237	    (element: HTMLElement | null) => {
238	      registerElement(kind, element);
239	    },
240	    [kind, registerElement],
241	  );
242	}
243	
244	/** Subscribes to whether the current overlay is the topmost stack entry. */
245	export function useCurrentOverlayTopmost(): boolean {
246	  const handle = useCurrentOverlayHandle();
247	  return useIsOverlayTopmost(handle.id);
248	}
249	
250	/** Subscribes to whether the given element belongs to the current topmost overlay. */
251	export function useCurrentOverlayTopmostForElement(element: Element | null): boolean {
252	  const handle = useCurrentOverlayHandle();
253	  const topmostOverlay = useTopmostOverlayContainingElement(element);
254	  return topmostOverlay?.id === handle.id;
255	}
256
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/settings/hooks/useAutoSaveSettings.ts",
  "offset": 200,
  "limit": 120
}
```

> TOOL

tool_result Read
```
200	  runtime.mode = isCustomMode ? 'custom' : 'react-query';
201	  runtime.loadRef.current = customLoadSave?.load ?? null;
202	  runtime.saveRef.current = customLoadSave?.save ?? null;
203	  runtime.scopeRef.current = scope;
204	  runtime.onSaveSuccessRef.current = onSaveSuccess;
205	  runtime.onSaveErrorRef.current = onSaveError;
206	  runtime.onFlushRef.current = customLoadSave?.onFlush;
207	  runtime.bootstrapRef.current = bootstrapData ? cloneValue(bootstrapData) : null;
208	
209	  const {
210	    settings: authoritativeSettings,
211	    isLoading: authoritativeIsLoading,
212	    error: authoritativeError,
213	    update: updateSettings,
214	    hasShotSettings,
215	  } = useToolSettings<T>(toolId, {
216	    shotId: !isCustomMode && scope === 'shot' ? (shotId ?? undefined) : undefined,
217	    projectId: !isCustomMode ? (projectId ?? undefined) : undefined,
218	    enabled: !isCustomMode && isEntityValid,
219	  });
220	
221	  runtime.updateRef.current = updateSettings;
222	
223	  const localEntity = store.useEntity(activeEntityId);
224	  const storeState = store.getState();
225	  const bootstrapEntity = storeState.bootstrapEntity;
226	  const updateStoredField = storeState.updateField;
227	  const updateStoredFields = storeState.updateFields;
228	  const updateStoredTextField = storeState.updateTextField;
229	  const saveStoredEntity = storeState.save;
230	  const saveStoredEntityImmediate = storeState.saveImmediate;
231	  const revertStoredEntity = storeState.revert;
232	  const resetStoredEntity = storeState.reset;
233	  const isStoredEntityDirty = storeState.isDirty;
234	  const reloadStoredEntity = storeState.reloadEntity;
235	  const activeEntityRef = useRef<string | null>(entityId ?? null);
236	  const lastBootstrapRef = useRef<{
237	    entityId: string | null;
238	    seed: T | null;
239	    hasShotSettings: boolean;
240	  }>({ entityId: null, seed: null, hasShotSettings: false });
241	
242	  useEffect(() => {
243	    activeEntityRef.current = entityId ?? null;
244	  }, [entityId]);
245	
246	  useEffect(() => {
247	    const currentEntityId = entityId;
248	
249	    return () => {
250	      if (!currentEntityId) {
251	        return;
252	      }
253	
254	      void store.getState().saveImmediate(currentEntityId);
255	    };
256	  }, [entityId, store]);
257	
258	  useEffect(() => {
259	    const handleBeforeUnload = () => {
260	      const currentEntityId = activeEntityRef.current;
261	      if (!currentEntityId) {
262	        return;
263	      }
264	
265	      void store.getState().saveImmediate(currentEntityId);
266	    };
267	
268	    window.addEventListener('beforeunload', handleBeforeUnload);
269	    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
270	  }, [store]);
271	
272	  useEffect(() => {
273	    if (!isCustomMode || !isEntityValid) {
274	      return;
275	    }
276	
277	    void reloadStoredEntity(activeEntityId).catch(() => {});
278	  }, [activeEntityId, isCustomMode, isEntityValid, reloadStoredEntity]);
279	
280	  useEffect(() => {
281	    if (!isCustomMode || !isEntityValid || !bootstrapData) {
282	      return;
283	    }
284	
285	    const currentEntity = store.getState().entities[activeEntityId];
286	    if (!currentEntity || currentEntity.status === 'loading' || currentEntity.hasPersistedData) {
287	      return;
288	    }
289	
290	    const bootstrapSnapshot = cloneValue(bootstrapData);
291	    if (currentEntity.loaded && deepEqual(currentEntity.cleanSnapshot, bootstrapSnapshot)) {
292	      return;
293	    }
294	
295	    bootstrapEntity({
296	      entityId: activeEntityId,
297	      db: null,
298	      lastUsed: bootstrapSnapshot,
299	    });
300	  }, [
301	    activeEntityId,
302	    bootstrapData,
303	    bootstrapEntity,
304	    isCustomMode,
305	    isEntityValid,
306	    store,
307	  ]);
308	
309	  useEffect(() => {
310	    if (isCustomMode || !isEntityValid || authoritativeIsLoading || authoritativeError) {
311	      return;
312	    }
313	
314	    const seed = cloneValue(authoritativeSettings ?? defaults);
315	
316	    // Self-tracking guard: this effect is the one-and-only writer for
317	    // RQ→store sync here, so it compares against its own last-known seed
318	    // (not against store state, which can be mutated by other paths and
319	    // cause a feedback loop).
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/settings/hooks/useAutoSaveSettings.ts",
  "offset": 320,
  "limit": 80
}
```

> TOOL

tool_result Read
```
320	    if (
321	      lastBootstrapRef.current.entityId === activeEntityId
322	      && lastBootstrapRef.current.hasShotSettings === hasShotSettings
323	      && deepEqual(lastBootstrapRef.current.seed, seed)
324	    ) {
325	      return;
326	    }
327	
328	    // Secondary guard: if the store already has the same clean snapshot
329	    // from some earlier path, skip re-bootstrapping but still record it.
330	    const currentEntity = store.getState().entities[activeEntityId];
331	    if (
332	      currentEntity
333	      && currentEntity.loaded
334	      && currentEntity.hasPersistedData === hasShotSettings
335	      && deepEqual(currentEntity.cleanSnapshot, seed)
336	    ) {
337	      lastBootstrapRef.current = { entityId: activeEntityId, seed, hasShotSettings };
338	      return;
339	    }
340	
341	    lastBootstrapRef.current = { entityId: activeEntityId, seed, hasShotSettings };
342	
343	    bootstrapEntity({
344	      entityId: activeEntityId,
345	      db: hasShotSettings ? seed : null,
346	      lastUsed: hasShotSettings ? null : seed,
347	    });
348	  }, [
349	    activeEntityId,
350	    authoritativeIsLoading,
351	    authoritativeError,
352	    authoritativeSettings,
353	    defaults,
354	    hasShotSettings,
355	    isCustomMode,
356	    isEntityValid,
357	    bootstrapEntity,
358	    store,
359	  ]);
360	
361	  useRenderLogger(`AutoSaveSettings:${toolId || domainKey}`, {
362	    entityId,
363	    status: localEntity.status,
364	  });
365	
366	  const updateField = useCallback(<K extends keyof T>(key: K, value: T[K]) => {
367	    if (!isEntityValid) {
368	      return;
369	    }
370	
371	    updateStoredField(activeEntityId, key, value, {
372	      deferPersistence: !isCustomMode && authoritativeIsLoading,
373	    });
374	  }, [activeEntityId, authoritativeIsLoading, isCustomMode, isEntityValid, updateStoredField]);
375	
376	  const updateFields = useCallback((updates: Partial<T>) => {
377	    if (!isEntityValid) {
378	      return;
379	    }
380	
381	    const deferKeys = !isCustomMode && authoritativeIsLoading
382	      ? (Object.keys(updates) as Array<keyof T>)
383	      : undefined;
384	    updateStoredFields(activeEntityId, updates, deferKeys ? { deferKeys } : undefined);
385	  }, [activeEntityId, authoritativeIsLoading, isCustomMode, isEntityValid, updateStoredFields]);
386	
387	  const updateTextField = useCallback(<K extends keyof T>(key: K, value: T[K]) => {
388	    if (!isEntityValid) {
389	      return;
390	    }
391	
392	    updateStoredTextField(activeEntityId, key, value);
393	  }, [activeEntityId, isEntityValid, updateStoredTextField]);
394	
395	  const updateTextFields = useCallback((updates: Partial<T>) => {
396	    if (!isEntityValid) {
397	      return;
398	    }
399
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/domains/media-lightbox/hooks/useLastUsedEditSettings.ts",
  "offset": 140,
  "limit": 50
}
```

> TOOL

tool_result Read
```
140	  const saveStoredEntityImmediately = storeState.saveImmediate;
141	  const reloadStoredEntity = storeState.reloadEntity;
142	  const fallbackLastUsed = useMemo(
143	    () => (entityId ? readLocalStorageSettings(entityId) : DEFAULT_LAST_USED),
144	    [entityId]
145	  );
146	
147	  useEffect(() => {
148	    if (!entityId) {
149	      return;
150	    }
151	
152	    void reloadStoredEntity(entityId).catch(() => {});
153	  }, [entityId, reloadStoredEntity]);
154	
155	  useEffect(() => {
156	    if (!entityId) {
157	      return;
158	    }
159	
160	    const localSettings = readLocalStorageSettings(entityId);
161	    const dbSnapshot = dbSettings ? { ...localSettings, ...dbSettings } : null;
162	    const currentEntity = store.getState().entities[entityId];
163	    const nextSeed = dbSnapshot ?? localSettings;
164	
165	    if (
166	      currentEntity
167	      && currentEntity.loaded
168	      && currentEntity.hasPersistedData === (dbSnapshot !== null)
169	      && deepEqual(currentEntity.cleanSnapshot, nextSeed)
170	    ) {
171	      return;
172	    }
173	
174	    bootstrapEntity({
175	      entityId,
176	      db: dbSnapshot,
177	      lastUsed: localSettings,
178	    });
179	  }, [bootstrapEntity, dbSettings, entityId, store]);
180	
181	  const updateLastUsed = useCallback((updates: Partial<LastUsedEditSettings>) => {
182	    if (!entityId) {
183	      return;
184	    }
185	
186	    const currentSettings = store.getState().entities[entityId]?.settings ?? readLocalStorageSettings(entityId);
187	    const nextSettings = { ...currentSettings, ...updates };
188	    if (!hasSettingsChanged(currentSettings, nextSettings)) {
189	      return;
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks/useTimelineState.ts",
  "offset": 795,
  "limit": 60
}
```

> TOOL

tool_result Read
```
795	    trackManagement: {
796	      handleAddTrack: trackManagement.handleAddTrack,
797	      handleClearUnusedTracks: trackManagement.handleClearUnusedTracks,
798	      unusedTrackCount: trackManagement.unusedTrackCount,
799	    },
800	    clipEditing: {
801	      handleAddText: clipEditing.handleAddText,
802	      handleAddTextAt: clipEditing.handleAddTextAt,
803	    },
804	    reloadFromServer,
805	    retrySaveAfterConflict,
806	    startRender,
807	  });
808	
809	  const playbackValue = useTimelinePlaybackContextValue({ playback });
810	
811	  // Seed the external store before descendants render for the first time so
812	  // mounted-provider readers such as AgentChat and pending-add helpers do not
813	  // observe the placeholder slice values from createTimelineStore().
814	  syncInitialTimelineStoreBootstrap(storeRef.current, {
815	    data: editorData,
816	    ops: editorOps,
817	    chrome,
818	    playback: playbackValue,
819	  });
820	
821	  useLayoutEffect(() => {
822	    storeRef.current.getState().syncSlices({
823	      data: editorData,
824	      ops: editorOps,
825	      chrome,
826	      playback: playbackValue,
827	    });
828	  }, [chrome, editorData, editorOps, playbackValue]);
829	
830	  return {
831	    store: storeRef.current,
832	    editor,
833	    editorData,
834	    editorOps,
835	    chrome,
836	    playback: playbackValue,
837	  };
838	}
839
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/state/overlayStack.ts"
}
```

> TOOL

tool_result Read
```
1	import { shallow } from 'zustand/shallow';
2	import { useStoreWithEqualityFn } from 'zustand/traditional';
3	import { createStore } from 'zustand/vanilla';
4	
5	export interface OverlayStackOpenInput {
6	  id: string;
7	  type: string;
8	  modal?: boolean;
9	  restoreFocusTo?: HTMLElement | null;
10	  elements?: Iterable<Element | null | undefined>;
11	}
12	
13	export interface OverlayStackUpdateInput {
14	  type?: string;
15	  modal?: boolean;
16	  restoreFocusTo?: HTMLElement | null;
17	  elements?: Iterable<Element | null | undefined>;
18	}
19	
20	export interface OverlayStackEntry {
21	  id: string;
22	  type: string;
23	  modal: boolean;
24	  restoreFocusTo: HTMLElement | null;
25	  elements: readonly HTMLElement[];
26	}
27	
28	export interface OverlayStackState {
29	  overlays: OverlayStackEntry[];
30	  /** Registers or re-registers an overlay at the top of the ordering stack. */
31	  pushOverlay: (input: OverlayStackOpenInput) => void;
32	  /** Updates a registered overlay without changing its ordering position. */
33	  updateOverlay: (id: string, patch: OverlayStackUpdateInput) => void;
34	  /** Unregisters an overlay and applies any pending cleanup side effects. */
35	  popOverlay: (id: string) => void;
36	  /** Returns the current topmost overlay, regardless of modality. */
37	  getTopOverlay: () => OverlayStackEntry | null;
38	  /** Returns the current topmost modal overlay, if one is registered. */
39	  getTopModalOverlay: () => OverlayStackEntry | null;
40	  /** Returns true when the given overlay is the topmost registered overlay. */
41	  isOverlayTopmost: (id: string) => boolean;
42	  /** Returns true when the given overlay is the topmost modal overlay. */
43	  isTopmostModalOverlay: (id: string) => boolean;
44	  /** Returns the overlay's 1-based stack layer, or null when not registered. */
45	  getOverlayLayer: (id: string) => number | null;
46	  /** Returns true when the element is the overlay or a descendant of any tracked overlay element. */
47	  overlayContainsElement: (id: string, element: Element | null) => boolean;
48	  /** Returns true when any overlay contains the given element. */
49	  isElementWithinAnyOverlay: (element: Element | null) => boolean;
50	  /** Returns the topmost overlay containing the given element, if one exists. */
51	  getTopmostOverlayContainingElement: (element: Element | null) => OverlayStackEntry | null;
52	}
53	
54	type OverlayStackSnapshot = Pick<OverlayStackState, 'overlays'>;
55	
56	let bodyPointerEventsSnapshot: string | null = null;
57	
58	function isBrowser(): boolean {
59	  return typeof document !== 'undefined';
60	}
61	
62	function isHTMLElement(value: unknown): value is HTMLElement {
63	  return value instanceof HTMLElement;
64	}
65	
66	function normalizeElements(
67	  elements?: Iterable<Element | null | undefined>,
68	): readonly HTMLElement[] {
69	  if (!elements) {
70	    return [];
71	  }
72	
73	  const nextElements: HTMLElement[] = [];
74	  for (const element of elements) {
75	    if (!isHTMLElement(element) || nextElements.includes(element)) {
76	      continue;
77	    }
78	    nextElements.push(element);
79	  }
80	
81	  return nextElements;
82	}
83	
84	function getTopOverlay(overlays: readonly OverlayStackEntry[]): OverlayStackEntry | null {
85	  return overlays.at(-1) ?? null;
86	}
87	
88	function isOverlayActuallyOpen(overlay: OverlayStackEntry): boolean {
89	  if (overlay.elements.length === 0) {
90	    return false;
91	  }
92	  return overlay.elements.some((element) => {
93	    const state = element.getAttribute('data-state');
94	    if (state === 'closed') return false;
95	    if (element.hasAttribute('data-open')) return true;
96	    if (state === 'open') return true;
97	    // Fallback for overlays without base-ui open/close state markers:
98	    // treat as open only when rendered with non-zero box.
99	    return element.offsetParent !== null || element.getClientRects().length > 0;
100	  });
101	}
102	
103	function getTopModalOverlay(overlays: readonly OverlayStackEntry[]): OverlayStackEntry | null {
104	  for (let index = overlays.length - 1; index >= 0; index -= 1) {
105	    const overlay = overlays[index];
106	    if (overlay.modal && isOverlayActuallyOpen(overlay)) {
107	      return overlay;
108	    }
109	  }
110	
111	  return null;
112	}
113	
114	function canRestoreFocusTo(element: HTMLElement | null): element is HTMLElement {
115	  return isHTMLElement(element) && element.isConnected && typeof element.focus === 'function';
116	}
117	
118	function restoreFocus(element: HTMLElement | null): void {
119	  if (!canRestoreFocusTo(element)) {
120	    return;
121	  }
122	
123	  queueMicrotask(() => {
124	    if (!canRestoreFocusTo(element)) {
125	      return;
126	    }
127	
128	    try {
129	      element.focus({ preventScroll: true });
130	    } catch {
131	      element.focus();
132	    }
133	  });
134	}
135	
136	function syncBodyPointerEvents(
137	  previousOverlays: readonly OverlayStackEntry[],
138	  nextOverlays: readonly OverlayStackEntry[],
139	): void {
140	  if (!isBrowser()) {
141	    return;
142	  }
143	
144	  const previousTopModal = getTopModalOverlay(previousOverlays);
145	  const nextTopModal = getTopModalOverlay(nextOverlays);
146	
147	  if (!previousTopModal && nextTopModal) {
148	    bodyPointerEventsSnapshot = document.body.style.pointerEvents;
149	    document.body.style.pointerEvents = 'none';
150	    console.warn('[OverlayStack] body pointer-events LOCKED (none)', {
151	      modalId: nextTopModal.id,
152	      modalType: nextTopModal.type,
153	      totalOverlays: nextOverlays.length,
154	      snapshot: bodyPointerEventsSnapshot,
155	    });
156	    return;
157	  }
158	
159	  if (previousTopModal && !nextTopModal) {
160	    document.body.style.pointerEvents = bodyPointerEventsSnapshot ?? '';
161	    console.log('[OverlayStack] body pointer-events RELEASED', {
162	      prevModalId: previousTopModal.id,
163	      restoredTo: bodyPointerEventsSnapshot ?? '(empty)',
164	      totalOverlays: nextOverlays.length,
165	    });
166	    bodyPointerEventsSnapshot = null;
167	    return;
168	  }
169	
170	  if (nextTopModal) {
171	    document.body.style.pointerEvents = 'none';
172	    console.log('[OverlayStack] body stays LOCKED (modal swap)', {
173	      modalId: nextTopModal.id,
174	      modalType: nextTopModal.type,
175	    });
176	  }
177	}
178	
179	function createOverlayEntry(input: OverlayStackOpenInput): OverlayStackEntry {
180	  return {
181	    id: input.id,
182	    type: input.type,
183	    modal: input.modal ?? false,
184	    restoreFocusTo: input.restoreFocusTo ?? null,
185	    elements: normalizeElements(input.elements),
186	  };
187	}
188	
189	function containsElement(
190	  overlay: OverlayStackEntry | undefined,
191	  element: Element | null,
192	): boolean {
193	  if (!overlay || !element) {
194	    return false;
195	  }
196	
197	  return overlay.elements.some((candidate) => candidate === element || candidate.contains(element));
198	}
199	
200	const overlayStackStore = createStore<OverlayStackState>((set, get) => ({
201	  overlays: [],
202	
203	  pushOverlay: (input) => {
204	    console.log('[OverlayStack] PUSH', { id: input.id, type: input.type, modal: input.modal, stackSizeBefore: get().overlays.length });
205	    const nextEntry = createOverlayEntry(input);
206	    set((state) => {
207	      const nextOverlays = [
208	        ...state.overlays.filter((overlay) => overlay.id !== input.id),
209	        nextEntry,
210	      ];
211	      syncBodyPointerEvents(state.overlays, nextOverlays);
212	      return { overlays: nextOverlays };
213	    });
214	  },
215	
216	  updateOverlay: (id, patch) => {
217	    set((state) => {
218	      const index = state.overlays.findIndex((overlay) => overlay.id === id);
219	      if (index === -1) {
220	        return state;
221	      }
222	
223	      const current = state.overlays[index];
224	      const nextOverlay: OverlayStackEntry = {
225	        ...current,
226	        ...(patch.type === undefined ? null : { type: patch.type }),
227	        ...(patch.modal === undefined ? null : { modal: patch.modal }),
228	        ...(patch.restoreFocusTo === undefined
229	          ? null
230	          : { restoreFocusTo: patch.restoreFocusTo }),
231	        ...(patch.elements === undefined
232	          ? null
233	          : { elements: normalizeElements(patch.elements) }),
234	      };
235	      const nextOverlays = [...state.overlays];
236	      nextOverlays[index] = nextOverlay;
237	      syncBodyPointerEvents(state.overlays, nextOverlays);
238	      return { overlays: nextOverlays };
239	    });
240	  },
241	
242	  popOverlay: (id) => {
243	    const previousOverlays = get().overlays;
244	    const removedOverlay = previousOverlays.find((overlay) => overlay.id === id);
245	    if (!removedOverlay) {
246	      console.log('[OverlayStack] POP skipped (id not found)', { id });
247	      return;
248	    }
249	    console.log('[OverlayStack] POP', { id, type: removedOverlay.type, modal: removedOverlay.modal, stackSizeBefore: previousOverlays.length });
250	
251	    const previousTopModal = getTopModalOverlay(previousOverlays);
252	    const nextOverlays = previousOverlays.filter((overlay) => overlay.id !== id);
253	
254	    set(() => {
255	      syncBodyPointerEvents(previousOverlays, nextOverlays);
256	      return { overlays: nextOverlays };
257	    });
258	
259	    if (previousTopModal?.id === id && removedOverlay.modal) {
260	      restoreFocus(removedOverlay.restoreFocusTo);
261	    }
262	  },
263	
264	  getTopOverlay: () => getTopOverlay(get().overlays),
265	
266	  getTopModalOverlay: () => getTopModalOverlay(get().overlays),
267	
268	  isOverlayTopmost: (id) => getTopOverlay(get().overlays)?.id === id,
269	
270	  isTopmostModalOverlay: (id) => getTopModalOverlay(get().overlays)?.id === id,
271	
272	  getOverlayLayer: (id) => {
273	    const index = get().overlays.findIndex((overlay) => overlay.id === id);
274	    return index === -1 ? null : index + 1;
275	  },
276	
277	  overlayContainsElement: (id, element) => {
278	    return containsElement(
279	      get().overlays.find((overlay) => overlay.id === id),
280	      element,
281	    );
282	  },
283	
284	  isElementWithinAnyOverlay: (element) => {
285	    return get().overlays.some((overlay) => containsElement(overlay, element));
286	  },
287	
288	  getTopmostOverlayContainingElement: (element) => {
289	    const { overlays } = get();
290	    for (let index = overlays.length - 1; index >= 0; index -= 1) {
291	      const overlay = overlays[index];
292	      if (containsElement(overlay, element)) {
293	        return overlay;
294	      }
295	    }
296	
297	    return null;
298	  },
299	}));
300	
301	/** Returns the vanilla store API for imperative overlay registration and queries. */
302	export function useOverlayStackApi() {
303	  return overlayStackStore;
304	}
305	
306	function useOverlayStack<T>(
307	  selector: (state: OverlayStackState) => T,
308	  equalityFn?: (left: T, right: T) => boolean,
309	): T {
310	  return useStoreWithEqualityFn(overlayStackStore, selector, equalityFn);
311	}
312	
313	/** Subscribes to the current ordered overlay snapshot. */
314	export function useOverlayStackState(): OverlayStackSnapshot {
315	  return useOverlayStack((state) => ({ overlays: state.overlays }), shallow);
316	}
317	
318	/** Subscribes to the current topmost overlay, regardless of modality. */
319	export function useTopOverlay(): OverlayStackEntry | null {
320	  return useOverlayStack((state) => state.getTopOverlay());
321	}
322	
323	/** Subscribes to the current topmost modal overlay. */
324	export function useTopModalOverlay(): OverlayStackEntry | null {
325	  return useOverlayStack((state) => state.getTopModalOverlay());
326	}
327	
328	/** Subscribes to the overlay's 1-based stack layer. */
329	export function useOverlayLayer(id: string): number | null {
330	  return useOverlayStack((state) => state.getOverlayLayer(id));
331	}
332	
333	/** Subscribes to whether the overlay is the current topmost entry. */
334	export function useIsOverlayTopmost(id: string): boolean {
335	  return useOverlayStack((state) => state.isOverlayTopmost(id));
336	}
337	
338	/** Subscribes to whether the overlay is the current topmost modal entry. */
339	export function useIsTopmostModalOverlay(id: string): boolean {
340	  return useOverlayStack((state) => state.isTopmostModalOverlay(id));
341	}
342	
343	/** Subscribes to the topmost overlay that currently owns the provided element. */
344	export function useTopmostOverlayContainingElement(
345	  element: Element | null,
346	): OverlayStackEntry | null {
347	  return useOverlayStack((state) => state.getTopmostOverlayContainingElement(element));
348	}
349	
350	/** Resets overlay ordering and global side effects for isolated tests. */
351	export function __resetOverlayStackForTests(): void {
352	  overlayStackStore.setState({ overlays: [] });
353	  if (isBrowser()) {
354	    document.body.style.pointerEvents = '';
355	  }
356	  bodyPointerEventsSnapshot = null;
357	}
358
```

> TOOL

tool_use Grep
```json
{
  "pattern": "cleanSnapshot",
  "output_mode": "files_with_matches",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
Found 3 files
src/shared/settings/hooks/useAutoSaveSettings.ts
src/shared/state/createEntityStore.ts
src/domains/media-lightbox/hooks/useLastUsedEditSettings.ts
```

> TOOL

tool_use Grep
```json
{
  "pattern": "usePaneLockPolicyState|PaneLockPolicyProvider|PaneLockPolicyContext",
  "output_mode": "content",
  "-n": true,
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
src/shared/state/panesStore.ts:7:import { usePaneLockPolicyState } from '@/shared/contexts/usePaneLockPolicyState';
src/shared/state/panesStore.ts:480:  } = usePaneLockPolicyState();
src/shared/contexts/__tests__/PanesContext.test.tsx:6:  usePaneLockPolicyState: vi.fn(),
src/shared/contexts/__tests__/PanesContext.test.tsx:17:vi.mock('../usePaneLockPolicyState', () => ({
src/shared/contexts/__tests__/PanesContext.test.tsx:18:  usePaneLockPolicyState: (...args: unknown[]) => mocks.usePaneLockPolicyState(...args),
src/shared/contexts/__tests__/PanesContext.test.tsx:113:    mocks.usePaneLockPolicyState.mockReturnValue({
src/shared/contexts/__tests__/PanesContext.test.tsx:150:    mocks.usePaneLockPolicyState.mockReturnValue({
src/shared/contexts/usePaneLockPolicyState.test.ts:3:import { usePaneLockPolicyState } from './usePaneLockPolicyState';
src/shared/contexts/usePaneLockPolicyState.test.ts:18:describe('usePaneLockPolicyState', () => {
src/shared/contexts/usePaneLockPolicyState.test.ts:33:    const { result } = renderHook(() => usePaneLockPolicyState());
src/shared/contexts/usePaneLockPolicyState.test.ts:69:    const { result, rerender } = renderHook(() => usePaneLockPolicyState());
src/shared/contexts/usePaneLockPolicyState.test.ts:102:    const { result } = renderHook(() => usePaneLockPolicyState());
src/shared/contexts/usePaneLockPolicyState.ts:21:export function usePaneLockPolicyState() {
```

> TOOL

tool_use Glob
```json
{
  "pattern": ".megaplan/plans/milestone-m1-*/**"
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
  "pattern": ".megaplan/plans/milestone-m4-*/**"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "useOverlayBridge",
  "output_mode": "content",
  "-n": true,
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
src/shared/components/ui/overlay/lightbox.tsx:3:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/lightbox.tsx:11:  registerElement: ReturnType<typeof useOverlayBridge>['registerElement'];
src/shared/components/ui/overlay/lightbox.tsx:38:  const bridge = useOverlayBridge({ type: 'lightbox', modal });
src/shared/components/ui/overlay/select.tsx:6:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/select.tsx:198:    const bridge = useOverlayBridge({ type: 'select', modal });
src/shared/components/ui/overlay/dropdown-menu.tsx:7:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/dropdown-menu.tsx:83:  const bridge = useOverlayBridge({ type: 'menu-submenu', modal: false });
src/shared/components/ui/overlay/dropdown-menu.tsx:140:    const bridge = useOverlayBridge({ type: 'menu', modal });
src/shared/components/ui/overlay/dialog.tsx:12:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/dialog.tsx:68:    const bridge = useOverlayBridge({ type: 'dialog', modal: true });
src/shared/components/ui/overlay/tooltip.tsx:4:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/tooltip.tsx:49:  const bridge = useOverlayBridge({ type: 'tooltip', modal: false });
src/shared/components/ui/overlay/overlayBridge.test.tsx:19:  useOverlayBridge,
src/shared/components/ui/overlay/overlayBridge.test.tsx:75:  const bridge = useOverlayBridge({ id, type, modal });
src/shared/components/ui/overlay/overlayBridge.test.tsx:198:      const bridge = useOverlayBridge({ id: 'menu-a', type: 'menu' });
src/shared/components/ui/overlay/overlayBridge.tsx:89:function useOverlayBridgeContextValue(): OverlayBridgeContextValue {
src/shared/components/ui/overlay/overlayBridge.tsx:102:export function useOverlayBridge(options: UseOverlayBridgeOptions): OverlayBridgeContextValue {
src/shared/components/ui/overlay/overlayBridge.tsx:227:  return useOverlayBridgeContextValue().handle;
src/shared/components/ui/overlay/overlayBridge.tsx:234:  const { registerElement } = useOverlayBridgeContextValue();
src/shared/components/ui/overlay/hover-card.tsx:4:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/hover-card.tsx:40:  const bridge = useOverlayBridge({ type: 'preview-card', modal: false });
src/shared/components/ui/overlay/popover.tsx:4:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/popover.tsx:51:  const bridge = useOverlayBridge({ type: 'popover', modal });
src/shared/components/ui/overlay/alert-dialog.tsx:5:import { OverlayInstanceProvider, useOverlayBridge } from '@/shared/components/ui/overlay/overlayBridge';
src/shared/components/ui/overlay/alert-dialog.tsx:56:  const bridge = useOverlayBridge({ type: 'alert-dialog', modal: true });
```

> TOOL

tool_use Grep
```json
{
  "pattern": "syncInitialTimelineStoreBootstrap",
  "output_mode": "content",
  "-n": true,
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
src/tools/video-editor/hooks/useTimelineState.ts:401:function syncInitialTimelineStoreBootstrap(
src/tools/video-editor/hooks/useTimelineState.ts:814:  syncInitialTimelineStoreBootstrap(storeRef.current, {
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/shared/contexts/usePaneLockPolicyState.ts"
}
```

> TOOL

tool_result Read
```
1	import { useCallback, useEffect, useMemo, useState } from 'react';
2	import { useUserUIState } from '@/shared/hooks/useUserUIState';
3	import { useIsMobile, useIsTablet } from '@/shared/hooks/mobile';
4	
5	type PaneLockKey = 'shots' | 'tasks' | 'gens' | 'editor';
6	
7	interface PaneLocksState {
8	  shots: boolean;
9	  tasks: boolean;
10	  gens: boolean;
11	  editor: boolean;
12	}
13	
14	const UNLOCKED_PANES: PaneLocksState = {
15	  shots: false,
16	  tasks: false,
17	  gens: false,
18	  editor: false,
19	};
20	
21	export function usePaneLockPolicyState() {
22	  const isMobile = useIsMobile();
23	  const isTablet = useIsTablet();
24	  const isSmallMobile = isMobile && !isTablet;
25	
26	  const { value: paneLocks, update: savePaneLocks, isLoading } = useUserUIState('paneLocks', UNLOCKED_PANES);
27	  const [locks, setLocks] = useState(paneLocks);
28	
29	  const [isGenerationsPaneOpenState, setIsGenerationsPaneOpenState] = useState(false);
30	  const [isEditorPaneOpenState, setIsEditorPaneOpenState] = useState(false);
31	  const [isTasksPaneOpenState, setIsTasksPaneOpenState] = useState(false);
32	
33	  useEffect(() => {
34	    if (isSmallMobile) {
35	      setLocks(UNLOCKED_PANES);
36	      return;
37	    }
38	
39	    if (!isLoading) {
40	      let newLocks = paneLocks;
41	      if (isTablet) {
42	        const activeLocks = Object.entries(paneLocks).filter(([_, locked]) => locked);
43	        if (activeLocks.length > 1) {
44	          const firstLocked = activeLocks[0][0] as PaneLockKey;
45	          newLocks = {
46	            shots: firstLocked === 'shots',
47	            tasks: firstLocked === 'tasks',
48	            gens: firstLocked === 'gens',
49	            editor: firstLocked === 'editor',
50	          };
51	        }
52	      }
53	      setLocks(newLocks);
54	      setIsTasksPaneOpenState(newLocks.tasks);
55	    }
56	  }, [isLoading, paneLocks, isSmallMobile, isTablet]);
57	
58	  const createPaneLockSetter = useCallback(
59	    (lockKey: PaneLockKey) => (isLocked: boolean) => {
60	      if (typeof isLocked !== 'boolean') {
61	        return;
62	      }
63	      setLocks((prev) => {
64	        if (prev[lockKey] === isLocked) return prev;
65	        const exclusiveLock = (isMobile || isTablet) && isLocked;
66	        return exclusiveLock
67	          ? { ...UNLOCKED_PANES, [lockKey]: isLocked }
68	          : { ...prev, [lockKey]: isLocked };
69	      });
70	
71	      if (!isSmallMobile) {
72	        const exclusiveLock = (isMobile || isTablet) && isLocked;
73	        savePaneLocks(
74	          exclusiveLock
75	            ? { ...UNLOCKED_PANES, [lockKey]: isLocked }
76	            : { [lockKey]: isLocked },
77	        );
78	      }
79	
80	      if (lockKey === 'tasks') {
81	        setIsTasksPaneOpenState(isLocked);
82	      } else if ((isMobile || isTablet) && isLocked) {
83	        setIsTasksPaneOpenState(false);
84	      }
85	    },
86	    [isMobile, isTablet, isSmallMobile, savePaneLocks],
87	  );
88	
89	  const setIsGenerationsPaneLocked = useMemo(() => createPaneLockSetter('gens'), [createPaneLockSetter]);
90	  const setIsEditorPaneLocked = useMemo(() => createPaneLockSetter('editor'), [createPaneLockSetter]);
91	  const setIsShotsPaneLocked = useMemo(() => createPaneLockSetter('shots'), [createPaneLockSetter]);
92	  const setIsTasksPaneLocked = useMemo(() => createPaneLockSetter('tasks'), [createPaneLockSetter]);
93	
94	  const setIsGenerationsPaneOpen = useCallback((isOpen: boolean) => {
95	    setIsGenerationsPaneOpenState(isOpen);
96	  }, []);
97	
98	  const setIsEditorPaneOpen = useCallback((isOpen: boolean) => {
99	    setIsEditorPaneOpenState(isOpen);
100	  }, []);
101	
102	  const setIsTasksPaneOpen = useCallback((isOpen: boolean) => {
103	    if (!isSmallMobile) {
104	      setIsTasksPaneOpenState(isOpen);
105	    }
106	  }, [isSmallMobile]);
107	
108	  const resetAllPaneLocks = useCallback(() => {
109	    setLocks(UNLOCKED_PANES);
110	    setIsTasksPaneOpenState(false);
111	    savePaneLocks(UNLOCKED_PANES);
112	  }, [savePaneLocks]);
113	
114	  return {
115	    locks,
116	    isGenerationsPaneOpenState,
117	    isEditorPaneOpenState,
118	    isTasksPaneOpenState,
119	    setIsGenerationsPaneLocked,
120	    setIsEditorPaneLocked,
121	    setIsShotsPaneLocked,
122	    setIsTasksPaneLocked,
123	    setIsGenerationsPaneOpen,
124	    setIsEditorPaneOpen,
125	    setIsTasksPaneOpen,
126	    resetAllPaneLocks,
127	  };
128	}
129
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks/useTimelineState.ts",
  "offset": 390,
  "limit": 60
}
```

> TOOL

tool_result Read
```
390	    onPreviewTimeUpdate: playback.onPreviewTimeUpdate,
391	    formatTime: playback.formatTime,
392	  }), [
393	    playback.currentTime,
394	    playback.formatTime,
395	    playback.onPreviewTimeUpdate,
396	    playback.playerContainerRef,
397	    playback.previewRef,
398	  ]);
399	}
400	
401	function syncInitialTimelineStoreBootstrap(
402	  store: TimelineStoreApi,
403	  bootstrap: TimelineStoreBootstrap,
404	) {
405	  const state = store.getState();
406	  if (state.availability.mounted) {
407	    return;
408	  }
409	
410	  store.getState().syncSlices(bootstrap);
411	}
412	
413	export function useTimelineState(): UseTimelineStateResult {
414	  const runtime = useVideoEditorRuntime();
415	  const queryClient = useQueryClient();
416	  const isMobile = useIsMobile();
417	  const isTablet = useIsTablet();
418	  const playback = useTimelinePlayback();
419	  const preferences = useEditorPreferences(runtime.timelineId);
420	  const queries = useTimelineQueries(runtime.provider, runtime.timelineId);
421	  // Shared gate observed by drag/resize writers and read by save/persistence/poll.
422	  const interactionStateRef = useRef(createInteractionState());
423	  const storeRef = useRef<ReturnType<typeof createTimelineStore> | null>(null);
424	  if (storeRef.current === null) {
425	    storeRef.current = createTimelineStore();
426	  }
427	  const deviceClass = useMemo(
428	    () => resolveTimelineDeviceClass({ isMobile, isTablet }),
429	    [isMobile, isTablet],
430	  );
431	  const defaultInteractionMode = getDefaultInteractionMode(deviceClass);
432	  const initialInteractionPolicyRef = useRef(createMobileInteractionPolicy(deviceClass));
433	  const previousDefaultInteractionModeRef = useRef(defaultInteractionMode);
434	  const [inputModality, setInputModality] = useState(initialInteractionPolicyRef.current.inputModality);
435	  const [interactionMode, setInteractionMode] = useState(initialInteractionPolicyRef.current.interactionMode);
436	  const [gestureOwner, setGestureOwner] = useState(initialInteractionPolicyRef.current.gestureOwner);
437	  const [precisionEnabled, setPrecisionEnabled] = useState(initialInteractionPolicyRef.current.precisionEnabled);
438	  const [contextTarget, setContextTarget] = useState(initialInteractionPolicyRef.current.contextTarget);
439	  const [inspectorTarget, setInspectorTarget] = useState(initialInteractionPolicyRef.current.inspectorTarget);
440	  const save = useTimelineSave(queries, runtime.provider, interactionStateRef, storeRef.current);
441	  const history = useTimelineHistory({
442	    dataRef: save.dataRef,
443	    commitData: save.commitData,
444	    interactionStateRef,
445	  });
446	  const derived = useDerivedTimeline(save.data, save.selectedClipId, save.selectedTrackId);
447	  const render = useRenderState(derived.resolvedConfig, derived.renderMetadata);
448	  const assetOperations = useAssetOperations(
449	    runtime.provider,
```

> TOOL

tool_use Glob
```json
{
  "pattern": ".megaplan/plans/**/*.md"
}
```

> TOOL

tool_result Glob
```
.megaplan/plans/fix-editor-pane-snap-jump-20260325-0420/plan_v1.md
.megaplan/plans/fix-editor-pane-snap-jump-20260325-0420/plan_v2.md
.megaplan/plans/fix-editor-pane-snap-jump-20260325-0420/final.md
.megaplan/plans/polish-and-integrate-video-20260325-0449/plan_v1.md
.megaplan/plans/polish-and-integrate-video-20260325-0449/plan_v2.md
.megaplan/plans/polish-and-integrate-video-20260325-0449/final.md
.megaplan/plans/debug-and-fix-all-video-20260325-0525/plan_v1.md
.megaplan/plans/debug-and-fix-all-video-20260325-0525/plan_v2.md
.megaplan/plans/debug-and-fix-all-video-20260325-0525/final.md
.megaplan/plans/video-editor-final-polish-20260325-0602/plan_v1.md
.megaplan/plans/video-editor-final-polish-20260325-0602/final.md
.megaplan/plans/video-editor-tool-fixes-8-20260325-1537/plan_v1.md
.megaplan/plans/video-editor-tool-fixes-8-20260325-1537/plan_v2.md
.megaplan/plans/video-editor-tool-fixes-8-20260325-1537/plan_v3.md
.megaplan/plans/video-editor-tool-fixes-8-20260325-1537/final.md
.megaplan/plans/clean-up-video-editor-20260325-1828/plan_v1.md
.megaplan/plans/clean-up-video-editor-20260325-1828/plan_v2.md
.megaplan/plans/fix-three-editor-pane-issues-20260325-1841/plan_v1.md
.megaplan/plans/clean-up-video-editor-20260325-1828/final.md
.megaplan/plans/investigate-why-locking-the-20260325-1840/plan_v1.md
.megaplan/plans/fix-the-video-editor-s-20260325-1831/plan_v1.md
.megaplan/plans/video-editor-timeline-well-20260325-1848/plan_v1.md
.megaplan/plans/investigate-why-locking-the-20260325-1840/plan_v2.md
.megaplan/plans/fix-three-editor-pane-issues-20260325-1841/plan_v2.md
.megaplan/plans/investigate-why-locking-the-20260325-1840/final.md
.megaplan/plans/fix-three-editor-pane-issues-20260325-1841/final.md
.megaplan/plans/fix-the-video-editor-s-20260325-1831/final.md
.megaplan/plans/video-editor-timeline-well-20260325-1848/plan_v2.md
.megaplan/plans/video-editor-timeline-well-20260325-1848/final.md
.megaplan/plans/split-usetimelinedata-ts-678-20260325-2047/plan_v1.md
.megaplan/plans/investigate-and-fix-visual-20260325-2044/plan_v1.md
.megaplan/plans/investigate-and-fix-visual-20260325-2044/plan_v2.md
.megaplan/plans/split-usetimelinedata-ts-678-20260325-2047/plan_v2.md
.megaplan/plans/replace-xzdarcy-react-20260325-2054/plan_v1.md
.megaplan/plans/split-usetimelinedata-ts-678-20260325-2047/final.md
.megaplan/plans/investigate-and-fix-visual-20260325-2044/final.md
.megaplan/plans/replace-xzdarcy-react-20260325-2054/final.md
.megaplan/plans/migrate-all-ta[REDACTED_SK]/plan_v1.md
.megaplan/plans/build-a-turn-based-timeline-20260326-0005/plan_v1.md
.megaplan/plans/migrate-all-ta[REDACTED_SK]/plan_v2.md
.megaplan/plans/build-a-turn-based-timeline-20260326-0005/final.md
.megaplan/plans/migrate-all-ta[REDACTED_SK]/final.md
.megaplan/plans/refactor-ai-timeline-agent-20260326-0157/plan_v1.md
.megaplan/plans/refactor-ai-timeline-agent-20260326-0157/final.md
.megaplan/plans/multi-select-timeline-clips-20260326-0415/plan_v1.md
.megaplan/plans/multi-select-timeline-clips-20260326-0415/plan_v2.md
.megaplan/plans/multi-select-timeline-clips-20260326-0415/final.md
.megaplan/plans/multi-select-feature-parity-20260326-0548/plan_v1.md
.megaplan/plans/multi-select-feature-parity-20260326-0548/plan_v2.md
.megaplan/plans/multi-select-feature-parity-20260326-0548/final.md
.megaplan/plans/fix-track-reordering-bugs-and-20260326-1856/plan_v1.md
.megaplan/plans/fix-track-reordering-bugs-and-20260326-1856/final.md
.megaplan/plans/make-track-labels-part-of-the-20260326-2002/plan_v1.md
.megaplan/plans/make-track-labels-part-of-the-20260326-2002/plan_v2.md
.megaplan/plans/make-track-labels-part-of-the-20260326-2002/final.md
.megaplan/plans/add-auto-scroll-to-the-20260326-2119/plan_v1.md
.megaplan/plans/add-auto-scroll-to-the-20260326-2119/plan_v2.md
.megaplan/plans/add-auto-scroll-to-the-20260326-2119/final.md
.megaplan/plans/build-an-llm-powered-custom-20260326-2230/plan_v1.md
.megaplan/plans/build-an-llm-powered-custom-20260326-2230/plan_v2.md
.megaplan/plans/implement-undo-redo-history-20260326-2240/plan_v1.md
.megaplan/plans/implement-undo-redo-history-20260326-2240/plan_v2.md
.megaplan/plans/build-an-llm-powered-custom-20260326-2230/final.md
.megaplan/plans/implement-undo-redo-history-20260326-2240/final.md
.megaplan/plans/add-tuneable-parameters-to-20260326-2332/plan_v1.md
.megaplan/plans/add-tuneable-parameters-to-20260326-2332/plan_v2.md
.megaplan/plans/add-tuneable-parameters-to-20260326-2332/final.md
.megaplan/plans/light-megaplan-consolidate-20260327-0022/plan_v1.md
.megaplan/plans/light-megaplan-consolidate-20260327-0022/plan_v2.md
.megaplan/plans/light-megaplan-consolidate-20260327-0022/final.md
.megaplan/plans/light-megaplan-fix-the-20260327-0056/plan_v1.md
.megaplan/plans/light-megaplan-fix-the-20260327-0056/final.md
.megaplan/plans/add-adjustment-layer-effect-20260327-0358/plan_v1.md
.megaplan/plans/add-adjustment-layer-effect-20260327-0358/plan_v2.md
.megaplan/plans/add-adjustment-layer-effect-20260327-0358/final.md
.megaplan/plans/two-ux-improvements-1-drop-to-20260327-0520/plan_v1.md
.megaplan/plans/two-ux-improvements-1-drop-to-20260327-0520/plan_v2.md
.megaplan/plans/two-ux-improvements-1-drop-to-20260327-0520/final.md
.megaplan/plans/fix-worker-zombie-bug-when-20260330-2035/plan_v1.md
.megaplan/plans/fix-worker-zombie-bug-when-20260330-2035/plan_v2.md
.megaplan/plans/fix-worker-zombie-bug-when-20260330-2035/final.md
.megaplan/plans/refactor-edit-mode-ownership-20260331-1842/plan_v1.md
.megaplan/plans/refactor-edit-mode-ownership-20260331-1842/plan_v2.md
.megaplan/plans/refactor-edit-mode-ownership-20260331-1842/final.md
.megaplan/plans/standardize-video-editor-20260331-2343/plan_v1.md
.megaplan/plans/add-agent-response-messages-20260401-0221/plan_v1.md
.megaplan/plans/add-agent-response-messages-20260401-0221/plan_v2.md
.megaplan/plans/add-agent-response-messages-20260401-0221/final.md
.megaplan/plans/feature-timeline-agent-task-20260403-2324/plan_v1.md
.megaplan/plans/feature-timeline-agent-task-20260403-2324/plan_v2.md
.megaplan/plans/feature-timeline-agent-task-20260403-2324/final.md
.megaplan/plans/feature-gallery-media-20260404-0010/plan_v1.md
.megaplan/plans/feature-gallery-media-20260404-0010/plan_v2.md
.megaplan/plans/feature-gallery-media-20260404-0010/final.md
.megaplan/plans/cleanup-and-quality-pass-on-20260404-0138/plan_v1.md
.megaplan/plans/cleanup-and-quality-pass-on-20260404-0138/plan_v2.md
.megaplan/plans/cleanup-and-quality-pass-on-20260404-0138/plan_v3.md
.megaplan/plans/cleanup-and-quality-pass-on-20260404-0138/final.md
.megaplan/plans/fix-unify-timeline-and-20260404-0324/plan_v1.md
.megaplan/plans/fix-unify-timeline-and-20260404-0324/plan_v2.md
(Results are truncated. Consider using a more specific path or pattern.)
```

> TOOL

tool_use Grep
```json
{
  "pattern": "entity\\.cleanSnapshot|cleanSnapshot:",
  "output_mode": "content",
  "-n": true,
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
src/shared/state/createEntityStore.ts:44:  cleanSnapshot: T;
src/shared/state/createEntityStore.ts:119:    cleanSnapshot: cloneValue(seed),
src/shared/state/createEntityStore.ts:250:                cleanSnapshot: snapshot,
src/shared/state/createEntityStore.ts:377:                  cleanSnapshot: cloneValue(seed),
src/shared/state/createEntityStore.ts:541:              cleanSnapshot: cloneValue(resetSnapshot),
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/reigh-workspace/reigh-app/.megaplan/plans/ | grep -E \"(milestone-m|M1|M2|M3|M4|M5|M6|state.*manage|render.*storm|zustand|panes|overlay|autosave)\" | head -30",
  "description": "List megaplan directories matching milestone keywords"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Grep
```json
{
  "pattern": "usePaneLockPolicyState",
  "output_mode": "files_with_matches",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app"
}
```

> TOOL

tool_result Grep
```
Found 4 files
src/shared/state/panesStore.ts
src/shared/contexts/__tests__/PanesContext.test.tsx
src/shared/contexts/usePaneLockPolicyState.test.ts
src/shared/contexts/usePaneLockPolicyState.ts
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/reigh-workspace/reigh-app/.megaplan/plans/ | grep -iE \"(state|render|storm|zustand|pane|overlay|auto.?save|m1|m2|m3|m4|m5|m6)\" | tail -50",
  "description": "Find megaplan dirs with state management keywords"
}
```

> TOOL

tool_result Bash
```
fix-editor-pane-snap-jump-20260325-0420
fix-three-editor-pane-issues-20260325-1841
replace-the-preview-panel-in-20260406-1826
```

> TOOL

tool_use Grep
```json
{
  "pattern": "PanesContext|usePanes\\b",
  "output_mode": "files_with_matches",
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src"
}
```

> TOOL

tool_result Grep
```
Found 3 files
src/tools/travel-between-images/components/ShotEditor/useShotEditorController.ts
src/domains/media-lightbox/hooks/useImageLightboxEnvironment.ts
src/domains/media-lightbox/hooks/__tests__/useImageLightboxEnvironment.test.ts
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/reigh-workspace/reigh-app/.megaplan/plans/ | grep -iE \"(storm|zustand|mirror|sync|bootstrap|render)\" ",
  "description": "Find megaplan dirs by more keywords"
}
```

> TOOL

tool_result Bash
```
unify-shot-group-sync-into-a-20260406-1746
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -lt /Users/user_c042661f/Documents/reigh-workspace/reigh-app/.megaplan/plans/ | head -30",
  "description": "List most recent megaplan dirs"
}
```

> TOOL

tool_result Bash
```
total 0
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 wire-image-selection-across-20260413-1425
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 visualize-audio-waveforms-on-20260406-0611
drwxr-xr-x@ 6 user_c042661f  staff  192 Apr 17 23:17 video-editor-tool-fixes-8-20260325-1537
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 video-editor-timeline-well-20260325-1848
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 video-editor-final-polish-20260325-0602
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 unify-shot-group-sync-into-a-20260406-1746
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 two-ux-improvements-1-drop-to-20260327-0520
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 two-related-changes-to-the-20260408-0320
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 two-changes-to-the-video-20260408-0346
drwxr-xr-x@ 3 user_c042661f  staff   96 Apr 17 23:17 timeline-agent-improvements-1-20260409-1943
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 take-the-video-editor-20260406-0351
drwxr-xr-x@ 3 user_c042661f  staff   96 Apr 17 23:17 standardize-video-editor-20260331-2343
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 split-usetimelinedata-ts-678-20260325-2047
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 smooth-the-video-editor-20260406-0728
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 show-in-progress-spinners-on-20260406-0925
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 shot-bounding-boxes-on-20260406-0333
drwxr-xr-x@ 8 user_c042661f  staff  256 Apr 17 23:17 roll-back-the-first-class-20260408-1337
drwxr-xr-x@ 6 user_c042661f  staff  192 Apr 17 23:17 restructure-the-video-editor-20260406-0206
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 replace-xzdarcy-react-20260325-2054
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 remove-the-video-editor-20260408-0311
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 remove-inferred-shot-groups-20260406-1532
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 register-uploaded-dropped-20260406-2144
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 refactor-travel-segment-20260413-2020
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 refactor-the-phase-config-20260414-0017
drwxr-xr-x@ 6 user_c042661f  staff  192 Apr 17 23:17 refactor-pinned-shot-groups-20260408-0508
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 refactor-edit-mode-ownership-20260331-1842
drwxr-xr-x@ 4 user_c042661f  staff  128 Apr 17 23:17 refactor-ai-timeline-agent-20260326-0157
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 polish-the-video-editor-20260406-0351
drwxr-xr-x@ 5 user_c042661f  staff  160 Apr 17 23:17 polish-and-integrate-video-20260325-0449
```

> AGENT

I have enough context. Let me check a couple more key things quickly.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks/useTimelineState.ts",
  "offset": 750,
  "limit": 70
}
```

> TOOL

tool_result Read
```
750	    handleSelectedClipChange: editor.handleSelectedClipChange,
751	    handleResetClipPosition: editor.handleResetClipPosition,
752	    handleResetClipsPosition: editor.handleResetClipsPosition,
753	    handleSplitSelectedClip: editor.handleSplitSelectedClip,
754	    handleSplitClipAtTime: editor.handleSplitClipAtTime,
755	    handleSplitClipsAtPlayhead: editor.handleSplitClipsAtPlayhead,
756	    handleToggleMuteClips: editor.handleToggleMuteClips,
757	    handleToggleMute: editor.handleToggleMute,
758	    handleDetachAudioClip: editor.handleDetachAudioClip,
759	    handleTrackPopoverChange: editor.handleTrackPopoverChange,
760	    handleMoveTrack: editor.handleMoveTrack,
761	    handleRemoveTrack: editor.handleRemoveTrack,
762	    moveSelectedClipToTrack: editor.moveSelectedClipToTrack,
763	    moveSelectedClipsToTrack: editor.moveSelectedClipsToTrack,
764	    moveClipToRow: editor.moveClipToRow,
765	    createTrackAndMoveClip: editor.createTrackAndMoveClip,
766	    uploadFiles: editor.uploadFiles,
767	    applyEdit: editor.applyEdit,
768	    patchRegistry: editor.patchRegistry,
769	    unpatchRegistry: editor.unpatchRegistry,
770	    registerAsset: editor.registerAsset,
771	  }), [editor, onActionResizeStart, onClipEdgeResizeEnd]);
772	
773	  const chrome = useTimelineChromeContextValue({
774	    timelineName: runtime.timelineName ?? null,
775	    saveStatus,
776	    isConflictExhausted,
777	    render: {
778	      renderStatus,
779	      renderLog,
780	      renderDirty,
781	      renderProgress,
782	      renderResultUrl,
783	      renderResultFilename,
784	    },
785	    history: {
786	      undo,
787	      redo,
788	      canUndo,
789	      canRedo,
790	      checkpoints,
791	      jumpToCheckpoint,
792	      createManualCheckpoint,
793	    },
794	    setScaleWidth,
795	    trackManagement: {
796	      handleAddTrack: trackManagement.handleAddTrack,
797	      handleClearUnusedTracks: trackManagement.handleClearUnusedTracks,
798	      unusedTrackCount: trackManagement.unusedTrackCount,
799	    },
800	    clipEditing: {
801	      handleAddText: clipEditing.handleAddText,
802	      handleAddTextAt: clipEditing.handleAddTextAt,
803	    },
804	    reloadFromServer,
805	    retrySaveAfterConflict,
806	    startRender,
807	  });
808	
809	  const playbackValue = useTimelinePlaybackContextValue({ playback });
810	
811	  // Seed the external store before descendants render for the first time so
812	  // mounted-provider readers such as AgentChat and pending-add helpers do not
813	  // observe the placeholder slice values from createTimelineStore().
814	  syncInitialTimelineStoreBootstrap(storeRef.current, {
815	    data: editorData,
816	    ops: editorOps,
817	    chrome,
818	    playback: playbackValue,
819	  });
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/reigh-workspace/reigh-app/.megaplan/plans/ | grep -iE \"(milestone|state-management|context.*zustand|kill.*render|refactor-state)\" ",
  "description": "Look for state management megaplan"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Grep
```json
{
  "pattern": "mounted.*false|availability\\.mounted",
  "output_mode": "content",
  "-n": true,
  "path": "/Users/user_c042661f/Documents/reigh-workspace/reigh-app/src/tools/video-editor/hooks"
}
```

> TOOL

tool_result Grep
```
src/tools/video-editor/hooks/useTimelineState.ts:406:  if (state.availability.mounted) {
src/tools/video-editor/hooks/timelineStore.ts:317:        state.availability.mounted === mounted
src/tools/video-editor/hooks/timelineStore.ts:324:        state.data === data && state.availability.mounted
src/tools/video-editor/hooks/timelineStore.ts:327:              availability: state.availability.mounted ? state.availability : { mounted: true },
src/tools/video-editor/hooks/timelineStore.ts:334:        state.ops === ops && state.availability.mounted
src/tools/video-editor/hooks/timelineStore.ts:337:              availability: state.availability.mounted ? state.availability : { mounted: true },
src/tools/video-editor/hooks/timelineStore.ts:344:        state.chrome === chrome && state.availability.mounted
src/tools/video-editor/hooks/timelineStore.ts:347:              availability: state.availability.mounted ? state.availability : { mounted: true },
src/tools/video-editor/hooks/timelineStore.ts:354:        state.playback === playback && state.availability.mounted
src/tools/video-editor/hooks/timelineStore.ts:357:              availability: state.availability.mounted ? state.availability : { mounted: true },
src/tools/video-editor/hooks/timelineStore.ts:375:          && state.availability.mounted === nextMounted
src/tools/video-editor/hooks/timelineStore.ts:391:        availability: { mounted: false },
src/tools/video-editor/hooks/timelineStore.ts:434:  const mounted = useStoreWithEqualityFn(store, (state) => state.availability.mounted);
src/tools/video-editor/hooks/timelineStore.ts:442:  const mounted = useStoreWithEqualityFn(store, (state) => state.availability.mounted);
src/tools/video-editor/hooks/timelineStore.ts:452:    mounted: state.availability.mounted,
```

> AGENT

I have enough to write the concrete plan. Note: no milestone-m1/m4 plan directories exist, so I'll be honest about that.

---

# Concrete per-site action plan

**Megaplan metadata check:** No `milestone-m1-*`, `milestone-m1a-*`, or `milestone-m4-*` directories exist under `.megaplan/plans/`. The M1-M6 chain the user referenced is not persisted locally — I cannot quote the original justification for any mirror. All "was this load-bearing" answers below are derived from reading the code, not plan metadata.

---

### Site 1 — `panesStore.ts:517-520` (setState-in-render already patched)
- **Mirror load-bearing?** `src/shared/contexts/usePaneLockPolicyState.ts` has **no other readers** (Grep results: only `panesStore.ts` imports it + two tests). The context hook is a zombie. The store is the sole consumer.
- **Failing test:** `src/shared/state/__tests__/panesStore.bootstrap.test.tsx` — render `<PanesStoreBootstrapBoundary>` twice with different inputs, spy on `console.error` for "Cannot update a component while rendering"; assert zero warnings and that `usePanesStore.getState().isGenerationsPaneOpen` reflects the latest input.
- **Minimal change (net-negative):** Inline `usePaneLockPolicyState`'s body directly into `panesStore`'s bootstrap hook, delete `src/shared/contexts/usePaneLockPolicyState.ts` + its test, delete `src/shared/contexts/__tests__/PanesContext.test.tsx` mock of it. Remove `[PanesBoot]` logs at lines 512-515, 518, 524, 531.
- **Deleted:** ~128 LOC (usePaneLockPolicyState.ts) + 3 console.logs + mock scaffolding. Added: ~40 LOC inlined into `useBootstrapPanesStore`. Net: **~-100 LOC.**

### Site 2 — `overlayBridge.tsx` + `select.tsx:198` (register-before-open)
- **Mirror load-bearing?** No caller legitimately needs to register before open. `select.tsx:198`, `dialog.tsx:68`, `popover.tsx:51`, `alert-dialog.tsx:56`, `lightbox.tsx:38`, `dropdown-menu.tsx:140`, `hover-card.tsx:40`, `tooltip.tsx:49` — every one lives inside a `SelectPrimitive.Portal`/equivalent, so the bridge only mounts when the popup is already open per Base UI semantics. The Select bug is a Base UI quirk where `Portal` mounts the popup ref before the `data-state=open` flip. Making `open` a required prop is safe for all 8 callers.
- **Failing test:** `src/shared/components/ui/overlay/__tests__/select.closed.test.tsx` — mount `<Select>` without opening it; assert `document.body.style.pointerEvents !== 'none'` and `useOverlayStackState().overlays.length === 0`.
- **Minimal change:** Make `useOverlayBridge({ type, modal, open })` require `open: boolean`. In `syncRegistration` (line 136), early-return when `!open`. Delete the DOM-attribute `isOverlayActuallyOpen` fallback in `overlayStack.ts:88-101` — the prop is authoritative. For each of the 8 callers, read open from the Base UI root context (e.g., `SelectPrimitive.useSelectRootContext().open`).
- **Deleted:** `isOverlayActuallyOpen` (~14 LOC), `[OverlayStack] body pointer-events` console.warns at lines 150-155, 161-165, 172-175, `[OverlayStack] PUSH/POP` logs at 204, 246, 249. Net: **~-40 LOC, +8 callers touched by one line each = ~-32 LOC.**

### Site 3 — `useAutoSaveSettings.ts:309-359` (RQ→store mirror, main bootstrap)
- **Does any consumer read `cleanSnapshot`?** Yes, but only **inside `createEntityStore` itself** (`src/shared/state/createEntityStore.ts:44, 119, 250, 377, 541` — the `isDirty` computation and `revert()`). **No external consumer** (Grep for `cleanSnapshot` returns 3 files, all either the store internals or the two mirror hooks). So `cleanSnapshot` is not leaked — the mirror exists only so the store can compute `isDirty` against the RQ-supplied seed.
- **Verdict:** The mirror is load-bearing for `isDirty`/`revert` semantics but does not need to be a *mirror*. Alternatives: (a) make `isDirty` a selector that takes the authoritative RQ value as arg; (b) pass `seed` imperatively once per entity-change, not on every effect run.
- **Failing test:** `src/shared/settings/hooks/__tests__/useAutoSaveSettings.bootstrap.test.tsx` — wrap `renderHook(useAutoSaveSettings)` with a QueryClient seeded with toolSettings; rerender 5x with a new reference to `authoritativeSettings` that is deep-equal; assert `bootstrapEntity` mock called exactly once.
- **Minimal change:** Collapse the two bootstrap effects (lines 280-307 custom-mode, 309-359 RQ mode) into one effect keyed on `[activeEntityId, hasShotSettings]` only; pull `authoritativeSettings` through a ref. Delete `lastBootstrapRef` (lines 236-240, 321-326, 337-341) — redundant once the effect deps are right. Delete `[AutoSave]` logs.
- **Deleted:** ~30 LOC of guard logic + logs. Net: **~-30 LOC.**

### Site 4 — `useLastUsedEditSettings.ts:155-179` (template duplicate)
- **Verdict:** Same class as site 3. After site 3 is fixed, port the same shape (key on `entityId` only, pull `dbSettings` through a ref). Keep a separate test in `src/domains/media-lightbox/hooks/__tests__/useLastUsedEditSettings.bootstrap.test.tsx`.
- **Deleted:** `currentEntity.cleanSnapshot` comparison (lines 162-172). Net: **~-12 LOC.**

### Site 5 — `useTimelineState.ts:814` (render-body bootstrap)
- **What breaks on move?** `syncInitialTimelineStoreBootstrap` is guarded by `if (state.availability.mounted) return` (line 406), and `mounted` flips true the first time any slice differs from placeholder (`timelineStore.ts:327, 337, 347, 357`). So calling it in render body ≠ calling it in effect — in render, it runs once before children render, seeding the store so `AgentChat`/pending-add helpers read real data on **their first render**. In `useLayoutEffect`, children render once with placeholders first.
- **Verdict:** This is genuinely compensating for a first-paint ordering issue. Moving to `useLayoutEffect` will cause placeholder reads in descendants for one frame.
- **Failing test:** `src/tools/video-editor/hooks/__tests__/useTimelineState.bootstrap.test.tsx` — assert no `setState-in-render` console.error + store state has non-placeholder data when a child renders.
- **Minimal change:** Move the placeholder-default into the store's initial state (populate `createTimelineStore()` at line 425 with real defaults derived from `editorData`/`editorOps`). Then delete `syncInitialTimelineStoreBootstrap` entirely (lines 401-411, 814-819). The `useLayoutEffect` at 821-828 remains.
- **Deleted:** function + call site = ~18 LOC. Net: **~-18 LOC.**

---

## Tickets (handwritten, pick one at a time)

1. **overlay: require `open` prop in `useOverlayBridge`, drop DOM-attr fallback** — Thread `open` through all 8 overlay wrappers; early-return from `syncRegistration` when `!open`. *AT: closed `<Select>` does not set `body.pointerEvents`.*
2. **panes: delete `usePaneLockPolicyState`, inline into `useBootstrapPanesStore`** — `panesStore` is the sole reader. *AT: 2x rerender of `PanesStoreBootstrapBoundary` produces no setState-in-render warnings.*
3. **settings: collapse `useAutoSaveSettings` bootstraps, remove `lastBootstrapRef`** — Key the one remaining effect on `[entityId, hasShotSettings]`; ref the RQ seed. *AT: 5x deep-equal rerender calls `bootstrapEntity` once.*
4. **media-lightbox: apply settings-bootstrap shape to `useLastUsedEditSettings`** — mechanical port of ticket 3. *AT: same, for `useLastUsedEditSettings`.*
5. **video-editor: seed `createTimelineStore()` with real initial slices, delete `syncInitialTimelineStoreBootstrap`** — move placeholder removal out of render. *AT: `AgentChat` sees real `chrome` on first render without a render-body store write.*
6. **chore: strip `[PanesBoot]` / `[OverlayStack]` / `[AutoSave]` console logs** — one commit, no behavior change. *AT: ripgrep for those tags returns zero production hits.*
7. **docs: add `docs/structure_detail/state_ownership.md`** — one page: "RQ owns server state; Zustand owns ephemeral UI; Context is legal only for provider-scoped handles; never mirror." Link from `CLAUDE.md`. *AT: linked.*

Tickets 1, 2, 6 are the unblockers (do day 1). Ticket 3 is the hard one (day 2). Tickets 4, 5, 7 are day 3.

**Key relevant paths:** `src/shared/state/panesStore.ts`, `src/shared/contexts/usePaneLockPolicyState.ts`, `src/shared/components/ui/overlay/overlayBridge.tsx`, `src/shared/state/overlayStack.ts`, `src/shared/settings/hooks/useAutoSaveSettings.ts`, `src/shared/state/createEntityStore.ts`, `src/domains/media-lightbox/hooks/useLastUsedEditSettings.ts`, `src/tools/video-editor/hooks/useTimelineState.ts`, `src/tools/video-editor/hooks/timelineStore.ts`.
