> DEVELOPER

✓  242 …-anthropic.spec.js:73:2 › Onboarding Anthropic provider › configures Anthropic and loads models (8.2s)
  ✓  243 …g Anthropic provider › continue without selecting a model still persists Anthropic credentials (550ms)


  1) [default] › e2e/specs/sessions.spec.js:623:2 › Session management › deleting unmodified fork skips confirmation dialog

    Error: expect(locator).toHaveCount(expected) failed

    Locator:  locator('.provider-modal-backdrop:not(.hidden)').filter({ hasText: 'Delete this session?' })
    Expected: 0
    Received: 1
    Timeout:  10000ms

    Call log:
      - Expect "toHaveCount" with timeout 10000ms
      - waiting for locator('.provider-modal-backdrop:not(.hidden)').filter({ hasText: 'Delete this session?' })
        14 × locator resolved to 1 element
           - unexpected value "1"


      655 |                     hasText: "Delete this session?",
      656 |             });
    > 657 |             await expect(confirmModal).toHaveCount(0);
          |                                        ^
      658 |
      659 |             // The session should be deleted immediately (no dialog appeared)
      660 |             // so we should navigate away from the current session URL.
        at /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/sessions.spec.js:657:30

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: error-context (text/markdown) ───────────────────────────────────────────────────
    ## Error Context

    **Test**: deleting unmodified fork skips confirmation dialog
    **Status**: failed

    ### Page 1: e2e-bot
    - **URL**: http://127.0.0.1:56341/chats/session/8c7128bf-fbe6-4ea7-bbeb-9a93c2401220

    ```
    e2e-bot
    410MB · 18GB free / 68GB
    Settings
    Changelog
    Report issue
    +
    Sessions
    Cron
    2
    main
    02:...
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/trace.zip
    Usage:

        npx playwright show-trace test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────

  1 failed
    [default] › e2e/specs/sessions.spec.js:623:2 › Session management › deleting unmodified fork skips confirmation dialog
  4 skipped
  23 did not run
  238 passed (2.8m)
[local/e2e] failed in 168s
~/t/m/moltis main ❯

> AGENT

Context cleared.

> DEVELOPER

✓  243 …g Anthropic provider › continue without selecting a model still persists Anthropic credentials (571ms)


  1) [default] › e2e/specs/agents.spec.js:357:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist

    Error: expect(locator).toBeVisible() failed

    Locator: locator('#noProvidersCard').getByRole('heading', { name: 'No LLMs Connected', exact: true })
    Expected: visible
    Timeout: 10000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 10000ms
      - waiting for locator('#noProvidersCard').getByRole('heading', { name: 'No LLMs Connected', exact: true })


      51 |      const noProvidersVisible = await noProvidersCard.isVisible().catch(() => false);
      52 |      if (noProvidersVisible) {
    > 53 |              await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
         |                                                                                                             ^
      54 |              await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
      55 |              return null;
      56 |      }
        at waitForWelcomeOrNoProvidersCard (/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js:53:98)
        at /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js:381:23

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: error-context (text/markdown) ───────────────────────────────────────────────────
    ## Error Context

    **Test**: agent chips appear on welcome card when multiple agents exist
    **Status**: failed

    ### Page 1: e2e-bot
    - **URL**: http://127.0.0.1:62544/chats/session/f45b2df3-3a06-45ef-81b1-24dde4cd127f

    ```
    e2e-bot
    391MB · 17GB free / 68GB
    Settings
    Changelog
    Report issue
    +
    Sessions
    Cron...
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/trace.zip
    Usage:

        npx playwright show-trace test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────

  1 failed
    [default] › e2e/specs/agents.spec.js:357:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist
  4 skipped
  23 did not run
  238 passed (2.9m)
[local/e2e] failed in 175s
~/t/m/moltis main ❯

> TOOL

tool_use Read
id: toolu_01UwRLTETpVo1UHDEN3B6swM
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "offset": 1,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_01UwRLTETpVo1UHDEN3B6swM
```
     1→const { expect, test } = require("../base-test");
     2→const {
     3→	createSession,
     4→	expectPageContentMounted,
     5→	navigateAndWait,
     6→	waitForWsConnected,
     7→	watchPageErrors,
     8→} = require("../helpers");
     9→
    10→function isRetryableRpcError(message) {
    11→	if (typeof message !== "string") return false;
    12→	return message.includes("WebSocket not connected") || message.includes("WebSocket disconnected");
    13→}
    14→
    15→async function sendRpcFromPage(page, method, params) {
    16→	let lastResponse = null;
    17→	for (let attempt = 0; attempt < 30; attempt++) {
    18→		if (attempt > 0) {
    19→			await waitForWsConnected(page, 5_000).catch(() => {});
    20→		}
    21→		lastResponse = await page
    22→			.evaluate(
    23→				async ({ methodName, methodParams }) => {
    24→					var appScript = document.querySelector('script[type="module"][src*="js/app.js"]');
    25→					if (!appScript) throw new Error("app module script not found");
    26→					var appUrl = new URL(appScript.src, window.location.origin);
    27→					var prefix = appUrl.href.slice(0, appUrl.href.length - "js/app.js".length);
    28→					var helpers = await import(`${prefix}js/helpers.js`);
    29→					return helpers.sendRpc(methodName, methodParams);
    30→				},
    31→				{
    32→					methodName: method,
    33→					methodParams: params,
    34→				},
    35→			)
    36→			.catch((error) => ({ ok: false, error: { message: error?.message || String(error) } }));
    37→		if (lastResponse?.ok) return lastResponse;
    38→		var message = lastResponse?.error?.message || "";
    39→		if (!isRetryableRpcError(message)) break;
    40→	}
    41→	return lastResponse;
    42→}
    43→
    44→async function waitForWelcomeOrNoProvidersCard(page) {
    45→	await page.waitForSelector("#welcomeCard, #noProvidersCard", {
    46→		state: "visible",
    47→		timeout: 10_000,
    48→	});
    49→
    50→	const noProvidersCard = page.locator("#noProvidersCard");
    51→	const noProvidersVisible = await noProvidersCard.isVisible().catch(() => false);
    52→	if (noProvidersVisible) {
    53→		await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
    54→		await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
    55→		return null;
    56→	}
    57→
    58→	const welcomeCard = page.locator("#welcomeCard");
    59→	await expect(welcomeCard).toBeVisible({ timeout: 10_000 });
    60→	return welcomeCard;
    61→}
    62→
    63→async function deleteAgentByName(page, agentName) {
    64→	await navigateAndWait(page, "/settings/agents");
    65→	const testCard = page.locator(".backend-card").filter({ hasText: agentName });
    66→	await expect(testCard).toBeVisible({ timeout: 10_000 });
    67→	await testCard.getByRole("button", { name: "Delete", exact: true }).click();
    68→	await page.locator(".provider-modal").getByRole("button", { name: "Delete", exact: true }).click();
    69→	await expect(testCard).toHaveCount(0, { timeout: 10_000 });
    70→}
    71→
    72→test.describe("Agents settings page", () => {
    73→	test("settings/agents loads and shows heading", async ({ page }) => {
    74→		const pageErrors = watchPageErrors(page);
    75→		await navigateAndWait(page, "/settings/agents");
    76→
    77→		await expect(page).toHaveURL(/\/settings\/agents$/);
    78→		await expect(page.getByRole("heading", { name: "Agents", exact: true })).toBeVisible();
    79→
    80→		expect(pageErrors).toEqual([]);
    81→	});
    82→
    83→	test("main agent card is shown with Default badge", async ({ page }) => {
    84→		const pageErrors = watchPageErrors(page);
    85→		await navigateAndWait(page, "/settings/agents");
    86→
    87→		const mainCard = page.locator(".backend-card").filter({ hasText: "Default" });
    88→		await expect(mainCard).toBeVisible();
    89→
    90→		// Main agent should have an "Identity Settings" button, not Edit/Delete
    91→		await expect(mainCard.getByRole("button", { name: "Identity Settings", exact: true })).toBeVisible();
    92→		await expect(mainCard.getByRole("button", { name: "Edit", exact: true })).toHaveCount(0);
    93→		await expect(mainCard.getByRole("button", { name: "Delete", exact: true })).toHaveCount(0);
    94→
    95→		expect(pageErrors).toEqual([]);
    96→	});
    97→
    98→	test("New Agent button opens create form", async ({ page }) => {
    99→		const pageErrors = watchPageErrors(page);
   100→		await navigateAndWait(page, "/settings/agents");
   101→
   102→		const newBtn = page.getByRole("button", { name: "New Agent", exact: true });
   103→		await expect(newBtn).toBeVisible();
   104→		await newBtn.click();
   105→
   106→		// Form should be visible with ID, Name, and Create/Cancel buttons
   107→		await expect(page.getByText("Create Agent", { exact: true })).toBeVisible();
   108→		await expect(page.getByPlaceholder("e.g. writer, coder, researcher")).toBeVisible();
   109→		await expect(page.getByPlaceholder("Creative Writer")).toBeVisible();
   110→		await expect(page.getByRole("button", { name: "Create", exact: true })).toBeVisible();
   111→		await expect(page.getByRole("button", { name: "Cancel", exact: true })).toBeVisible();
   112→
   113→		expect(pageErrors).toEqual([]);
   114→	});
   115→
   116→	test("create form Cancel button returns to list", async ({ page }) => {
   117→		const pageErrors = watchPageErrors(page);
   118→		await navigateAndWait(page, "/settings/agents");
   119→
   120→		await page.getByRole("button", { name: "New Agent", exact: true }).click();
```

> TOOL

tool_use Read
id: toolu_01R1DW17HpfJdrqR7eRLKmzt
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "offset": 340,
  "limit": 130
}
```

> TOOL

tool_result
id: toolu_01R1DW17HpfJdrqR7eRLKmzt
```
   340→		if (!welcomeCard) {
   341→			expect(pageErrors).toEqual([]);
   342→			return;
   343→		}
   344→
   345→		// Click the "Hatch a new agent" button
   346→		const hatchBtn = page.locator("[data-welcome-agents]").getByRole("button", { name: /Hatch a new agent/ });
   347→		await expect(hatchBtn).toBeVisible();
   348→		await hatchBtn.click();
   349→
   350→		// Should navigate to /settings/agents/new and auto-open the create form
   351→		await expect(page).toHaveURL(/\/settings\/agents\/new/);
   352→		await expect(page.getByText("Create Agent", { exact: true })).toBeVisible({ timeout: 10_000 });
   353→
   354→		expect(pageErrors).toEqual([]);
   355→	});
   356→
   357→	test("agent chips appear on welcome card when multiple agents exist", async ({ page }) => {
   358→		const pageErrors = watchPageErrors(page);
   359→		const testAgentName = "Welcome Test Agent";
   360→
   361→		// Create a second agent via the settings page
   362→		await navigateAndWait(page, "/settings/agents");
   363→		await waitForWsConnected(page);
   364→
   365→		await page.getByRole("button", { name: "New Agent", exact: true }).click();
   366→		await expect(page.getByText("Create Agent", { exact: true })).toBeVisible();
   367→
   368→		await page.getByPlaceholder("e.g. writer, coder, researcher").fill("welcome-test");
   369→		await page.getByPlaceholder("Creative Writer").fill(testAgentName);
   370→		await page.getByRole("button", { name: "Create", exact: true }).click();
   371→
   372→		// Wait for the agent to appear in the list
   373→		await expect(page.getByRole("heading", { name: "Agents", exact: true })).toBeVisible({ timeout: 10_000 });
   374→		await expect(page.locator(".backend-card").filter({ hasText: testAgentName })).toBeVisible();
   375→
   376→		// Navigate to chats and create a new session — welcome card should show agent chips
   377→		await page.goto("/chats");
   378→		await expectPageContentMounted(page);
   379→		await createSession(page);
   380→
   381→		const welcomeCard = await waitForWelcomeOrNoProvidersCard(page);
   382→		if (!welcomeCard) {
   383→			await deleteAgentByName(page, testAgentName);
   384→			expect(pageErrors).toEqual([]);
   385→			return;
   386→		}
   387→
   388→		const agentsContainer = page.locator("[data-welcome-agents]");
   389→		await expect(agentsContainer).toBeVisible({ timeout: 10_000 });
   390→
   391→		// Should have at least 2 chip buttons (main + the new agent)
   392→		const chips = agentsContainer.getByRole("button");
   393→		const chipCount = await chips.count();
   394→		expect(chipCount).toBeGreaterThanOrEqual(2);
   395→		await expect(agentsContainer.getByRole("button", { name: new RegExp(testAgentName) })).toBeVisible();
   396→
   397→		// Clean up: delete the test agent
   398→		await deleteAgentByName(page, testAgentName);
   399→
   400→		expect(pageErrors).toEqual([]);
   401→	});
   402→});
   403→
```

> TOOL

tool_use Grep
id: toolu_01Gn4ux5MXCxMPgr2jQQX97d
```json
{
  "pattern": "noProvidersCard",
  "path": "/Users/penso/tmp/molt/moltis/crates/web",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01Gn4ux5MXCxMPgr2jQQX97d
```
Found 8 files
crates/web/ui/e2e/specs/agents.spec.js
crates/web/src/assets/js/sessions.js
crates/web/src/assets/js/websocket.js
crates/web/ui/input.css
crates/web/src/assets/style.css
crates/web/src/assets/css/style.css
crates/web/src/templates/index.html
crates/web/src/assets/js/chat-ui.js
```

> TOOL

tool_use Grep
id: toolu_01QVtkHVsMbf5J5X9Rk4jE9A
```json
{
  "pattern": "noProvidersCard|No LLMs Connected|No Providers Configured",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/src/templates/index.html",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result
id: toolu_01QVtkHVsMbf5J5X9Rk4jE9A
```
484-</template>
485-
486-<template id="tpl-no-providers-card">
487:  <div id="noProvidersCard" class="my-auto self-center flex flex-col items-center text-center px-6 py-10 max-w-md">
488:    <h2 class="text-lg font-medium text-[var(--text)] mb-1">No LLMs Connected</h2>
489-    <p class="text-sm text-[var(--muted)] mb-6">
490-      You have not connected any LLM providers yet. Add one to start chatting.
491-    </p>
```

> TOOL

tool_use Bash
id: toolu_013PrJBtq9H12hBR73oiWWoQ
```json
{
  "command": "git log --oneline -20 -- crates/web/src/templates/index.html crates/web/src/assets/js/chat-ui.js crates/web/ui/e2e/specs/agents.spec.js",
  "description": "Recent changes to relevant files"
}
```

> TOOL

tool_result
id: toolu_013PrJBtq9H12hBR73oiWWoQ
```
75ba6de7 fix(agents): surface workspace prompt truncation
0d30f86b feat(web): add live remote access settings
5e115929 fix(web): point report issue link to template chooser
37115cc9 feat(web): add changelog link to header nav
e492d900 feat(chat): tabs to filter chats between sessions and cron (#338)
bc33736e fix(web): align e2e with controls modal and daily model refresh
aede5586 fix(web): externalize SVG icons and restore empty-chat centering
f51e743c feat(web,tools): AOT WASM pre-compilation and Shiki CDN loading
801d4da8 fix(e2e): fix OAuth token-exchange failure test and add error-context capture
ca38d7de feat(macos): wire settings UI to rust config backend (#267)
b463d92c feat(sandbox): trusted network mode with domain-filtering proxy (#15)
953001de feat(web): internationalization (i18n) with English and French locales (#237)
9aa94188 fix(e2e): handle no-provider chat state in agent specs
fc1f546b feat(agents): add multi-agent personas with CRUD UI (#97)
c1ff376c refactor(web): extract web UI into dedicated moltis-web crate
```

> TOOL

tool_use Bash
id: toolu_01AZ49vBEg7D5rEBwodKyB5t
```json
{
  "command": "git log --oneline -5 -- crates/web/src/locales/ crates/web/ui/e2e/specs/agents.spec.js 2>/dev/null; git log --oneline -5 --all --source crates/web/src/assets/js/i18n* 2>/dev/null",
  "description": "Check i18n related changes"
}
```

> TOOL

tool_result
id: toolu_01AZ49vBEg7D5rEBwodKyB5t
```
75ba6de7 fix(agents): surface workspace prompt truncation
bc33736e fix(web): align e2e with controls modal and daily model refresh
801d4da8 fix(e2e): fix OAuth token-exchange failure test and add error-context capture
ca38d7de feat(macos): wire settings UI to rust config backend (#267)
b463d92c feat(sandbox): trusted network mode with domain-filtering proxy (#15)
4d308860	refs/heads/entire/96c3cd4-84d842 carry forward: uncommitted session files
323a1ea4	refs/heads/entire/cc7d041-84d842 carry forward: uncommitted session files
01bcd45d	refs/heads/entire/5447fa7-e3b0c4 Write a plan in plans/ as a markdown file so I can do it in another bran
5251c7eb	refs/heads/entire/dec2552-9e6a54 carry forward: uncommitted session files
38f07e1b	refs/heads/entire/4dcaaf5-9e6a54 Completed 'Explore' agent: Explore CI workflow structure (toolu_018R3y)
```

> TOOL

tool_use Read
id: toolu_01GViSiuGRYjZaRmvehK5LjZ
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/templates/index.html",
  "offset": 480,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01GViSiuGRYjZaRmvehK5LjZ
```
   480→    <div class="mt-6 text-xs text-[var(--muted)]">
   481→      Type a message or use <kbd class="px-1.5 py-0.5 bg-[var(--surface2)] border border-[var(--border)] rounded text-[var(--text)] text-xs font-mono">/</kbd> for commands
   482→    </div>
   483→  </div>
   484→</template>
   485→
   486→<template id="tpl-no-providers-card">
   487→  <div id="noProvidersCard" class="my-auto self-center flex flex-col items-center text-center px-6 py-10 max-w-md">
   488→    <h2 class="text-lg font-medium text-[var(--text)] mb-1">No LLMs Connected</h2>
   489→    <p class="text-sm text-[var(--muted)] mb-6">
   490→      You have not connected any LLM providers yet. Add one to start chatting.
   491→    </p>
   492→    <a href="{{ routes.providers }}" class="provider-btn">Go to LLMs</a>
   493→  </div>
   494→</template>
   495→
   496→<script nonce="{{ nonce }}" type="module" src="{{ asset_prefix }}js/app.js"></script>
   497→</body>
   498→</html>
   499→
```

> TOOL

tool_use Grep
id: toolu_013zZdxF1VE8PWJiQCBaSf7t
```json
{
  "pattern": "tpl-no-providers-card|noProvidersCard",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_013zZdxF1VE8PWJiQCBaSf7t
```
crates/web/src/assets/js/sessions.js:1117:		var noProvTpl = document.getElementById("tpl-no-providers-card");
crates/web/src/assets/js/sessions.js:1151:	var noProvCard = S.chatMsgBox.querySelector("#noProvidersCard");
crates/web/src/assets/js/chat-ui.js:10:	var noProviders = S.chatMsgBox.querySelector("#noProvidersCard");
crates/web/src/assets/js/websocket.js:61:	var noProviders = S.chatMsgBox.querySelector("#noProvidersCard");
```

> TOOL

tool_use Read
id: toolu_01XDU5BuaXE8zCr6tQH59xPK
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/sessions.js",
  "offset": 1100,
  "limit": 70
}
```

> TOOL

tool_result
id: toolu_01XDU5BuaXE8zCr6tQH59xPK
```
  1100→		hatchBtn.style.fontSize = "0.7rem";
  1101→		hatchBtn.style.padding = "3px 8px";
  1102→		hatchBtn.textContent = "\u{1F95A} Hatch a new agent";
  1103→		hatchBtn.addEventListener("click", () => {
  1104→			navigate(settingsPath("agents/new"));
  1105→		});
  1106→		container.appendChild(hatchBtn);
  1107→
  1108→		onActiveAgentResolved(activeAgent);
  1109→	});
  1110→}
  1111→
  1112→function showWelcomeCard() {
  1113→	if (!S.chatMsgBox) return;
  1114→	S.chatMsgBox.classList.add("chat-messages-empty");
  1115→
  1116→	if (modelStore.models.value.length === 0) {
  1117→		var noProvTpl = document.getElementById("tpl-no-providers-card");
  1118→		if (!noProvTpl) return;
  1119→		var noProvCard = noProvTpl.content.cloneNode(true).firstElementChild;
  1120→		S.chatMsgBox.appendChild(noProvCard);
  1121→		return;
  1122→	}
  1123→
  1124→	var tpl = document.getElementById("tpl-welcome-card");
  1125→	if (!tpl) return;
  1126→	var card = tpl.content.cloneNode(true).firstElementChild;
  1127→	var identity = gon.get("identity");
  1128→	var userName = identity?.user_name;
  1129→	var botName = identity?.name || "moltis";
  1130→	var botEmoji = identity?.emoji || "";
  1131→
  1132→	var greetingEl = card.querySelector("[data-welcome-greeting]");
  1133→	if (greetingEl) greetingEl.textContent = userName ? `Hello, ${userName}!` : "Hello!";
  1134→	var emojiEl = card.querySelector("[data-welcome-emoji]");
  1135→	if (emojiEl) emojiEl.textContent = botEmoji;
  1136→	var nameEl = card.querySelector("[data-welcome-bot-name]");
  1137→	if (nameEl) nameEl.textContent = botName;
  1138→	var activeAgentId = sessionStore.activeSession.value?.agent_id || "main";
  1139→	renderWelcomeAgentPicker(card, activeAgentId, (activeAgent) => {
  1140→		if (!activeAgent) return;
  1141→		if (emojiEl) emojiEl.textContent = activeAgent.emoji || "";
  1142→		if (nameEl) nameEl.textContent = activeAgent.name || botName;
  1143→	});
  1144→
  1145→	S.chatMsgBox.appendChild(card);
  1146→}
  1147→
  1148→export function refreshWelcomeCardIfNeeded() {
  1149→	if (!S.chatMsgBox) return;
  1150→	var welcomeCard = S.chatMsgBox.querySelector("#welcomeCard");
  1151→	var noProvCard = S.chatMsgBox.querySelector("#noProvidersCard");
  1152→	var hasModels = modelStore.models.value.length > 0;
  1153→
  1154→	// Wrong variant showing — swap it
  1155→	if (hasModels && noProvCard) {
  1156→		noProvCard.remove();
  1157→		showWelcomeCard();
  1158→	} else if (!hasModels && welcomeCard) {
  1159→		welcomeCard.remove();
  1160→		showWelcomeCard();
  1161→	}
  1162→}
  1163→
  1164→function ensureSessionInClientStore(key, entry, projectId) {
  1165→	var existing = sessionStore.getByKey(key);
  1166→	if (existing) return existing;
  1167→
  1168→	var created = { ...entry, key: key };
  1169→	if (projectId && !created.projectId) created.projectId = projectId;
```

> TOOL

tool_use Bash
id: toolu_01PCV66vKLYcsZ9jixf7ipsz
```json
{
  "command": "find /Users/penso/tmp/molt/moltis/crates/web -name \"*.json\" -path \"*locale*\" 2>/dev/null; find /Users/penso/tmp/molt/moltis/crates/web -name \"en.*\" -o -name \"fr.*\" 2>/dev/null | head -20",
  "description": "Find locale files"
}
```

> TOOL

tool_result
id: toolu_01PCV66vKLYcsZ9jixf7ipsz
```
(Bash completed with no output)
```

> TOOL

tool_use Grep
id: toolu_01FdyMEnHt9cudrDFZNFT6cS
```json
{
  "pattern": "No LLMs Connected",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01FdyMEnHt9cudrDFZNFT6cS
```
Found 2 files
crates/web/ui/e2e/specs/agents.spec.js
crates/web/src/templates/index.html
```

> TOOL

tool_use Bash
id: toolu_011Een1uNkx1YJfB5FscwdF8
```json
{
  "command": "git show 75ba6de7 --stat",
  "description": "Show latest commit stat"
}
```

> TOOL

tool_result
id: toolu_011Een1uNkx1YJfB5FscwdF8
```
commit 75ba6de79cb70baad5742ef07fc4601f43818523
Author: Fabien Penso <gpg@pen.so>
Date:   Thu Apr 9 12:09:57 2026 +0100

    fix(agents): surface workspace prompt truncation

 crates/agents/src/prompt.rs                | 229 ++++++++++++++++++++++++++---
 crates/chat/src/lib.rs                     |  54 +++++--
 crates/config/src/schema.rs                |  20 +++
 crates/config/src/template.rs              |   1 +
 crates/config/src/validate.rs              |   1 +
 crates/gateway/src/methods/services.rs     | 149 ++++++++++++++++---
 crates/gateway/src/server.rs               |  37 +++++
 crates/web/src/assets/js/page-agents.js    |  18 +++
 crates/web/src/assets/js/page-chat.js      |  21 +++
 crates/web/ui/e2e/specs/agents.spec.js     |  69 +++++++++
 crates/web/ui/e2e/specs/chat-input.spec.js |  39 +++++
 11 files changed, 582 insertions(+), 56 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01KJH7rXqHes1uVGdD4zVEWn
```json
{
  "command": "git show 75ba6de7 -- crates/web/ui/e2e/specs/agents.spec.js | head -120",
  "description": "Show agents.spec.js changes in latest commit"
}
```

> TOOL

tool_result
id: toolu_01KJH7rXqHes1uVGdD4zVEWn
```
commit 75ba6de79cb70baad5742ef07fc4601f43818523
Author: Fabien Penso <gpg@pen.so>
Date:   Thu Apr 9 12:09:57 2026 +0100

    fix(agents): surface workspace prompt truncation

diff --git a/crates/web/ui/e2e/specs/agents.spec.js b/crates/web/ui/e2e/specs/agents.spec.js
index 28bb5c36..0fb1f052 100644
--- a/crates/web/ui/e2e/specs/agents.spec.js
+++ b/crates/web/ui/e2e/specs/agents.spec.js
@@ -7,6 +7,40 @@ const {
 	watchPageErrors,
 } = require("../helpers");
 
+function isRetryableRpcError(message) {
+	if (typeof message !== "string") return false;
+	return message.includes("WebSocket not connected") || message.includes("WebSocket disconnected");
+}
+
+async function sendRpcFromPage(page, method, params) {
+	let lastResponse = null;
+	for (let attempt = 0; attempt < 30; attempt++) {
+		if (attempt > 0) {
+			await waitForWsConnected(page, 5_000).catch(() => {});
+		}
+		lastResponse = await page
+			.evaluate(
+				async ({ methodName, methodParams }) => {
+					var appScript = document.querySelector('script[type="module"][src*="js/app.js"]');
+					if (!appScript) throw new Error("app module script not found");
+					var appUrl = new URL(appScript.src, window.location.origin);
+					var prefix = appUrl.href.slice(0, appUrl.href.length - "js/app.js".length);
+					var helpers = await import(`${prefix}js/helpers.js`);
+					return helpers.sendRpc(methodName, methodParams);
+				},
+				{
+					methodName: method,
+					methodParams: params,
+				},
+			)
+			.catch((error) => ({ ok: false, error: { message: error?.message || String(error) } }));
+		if (lastResponse?.ok) return lastResponse;
+		var message = lastResponse?.error?.message || "";
+		if (!isRetryableRpcError(message)) break;
+	}
+	return lastResponse;
+}
+
 async function waitForWelcomeOrNoProvidersCard(page) {
 	await page.waitForSelector("#welcomeCard, #noProvidersCard", {
 		state: "visible",
@@ -231,6 +265,41 @@ test.describe("Agents settings page", () => {
 
 		expect(pageErrors).toEqual([]);
 	});
+
+	test("shows workspace prompt truncation warning when AGENTS.md exceeds the cap", async ({ page }) => {
+		const pageErrors = watchPageErrors(page);
+		await navigateAndWait(page, "/settings/agents");
+		await waitForWsConnected(page);
+
+		const originalResponse = await sendRpcFromPage(page, "agents.files.get", {
+			agent_id: "main",
+			path: "AGENTS.md",
+		});
+		const originalContent = originalResponse?.ok ? originalResponse.payload?.content || "" : "";
+		const oversizedContent = `${"A".repeat(32_050)}\n`;
+
+		try {
+			const setResponse = await sendRpcFromPage(page, "agents.files.set", {
+				agent_id: "main",
+				path: "AGENTS.md",
+				content: oversizedContent,
+			});
+			expect(setResponse?.ok).toBe(true);
+
+			await navigateAndWait(page, "/settings/agents");
+			const mainCard = page.locator(".backend-card").filter({ hasText: "Default" });
+			await expect(mainCard).toContainText("AGENTS.md", { timeout: 10_000 });
+			await expect(mainCard).toContainText("truncated by", { timeout: 10_000 });
+		} finally {
+			await sendRpcFromPage(page, "agents.files.set", {
+				agent_id: "main",
+				path: "AGENTS.md",
+				content: originalContent,
+			});
+		}
+
+		expect(pageErrors).toEqual([]);
+	});
 });
 
 test.describe("Welcome card agent picker", () => {
```

> TOOL

tool_use Bash
id: toolu_01NmMxjJgscKGNk6osq2XyNN
```json
{
  "command": "git show 953001de --stat | head -50",
  "description": "Show i18n commit stat"
}
```

> TOOL

tool_result
id: toolu_01NmMxjJgscKGNk6osq2XyNN
```
commit 953001de1a3f4b055084d41b6c4c369fb6e3ad66
Author: Fabien Penso <gpg@pen.so>
Date:   Wed Feb 25 15:52:59 2026 -0800

    feat(web): internationalization (i18n) with English and French locales (#237)
    
    * wip(i18n): snapshot before merging main
    
    * wip(i18n): snapshot after merging main
    
    Merge main into i18n branch, resolving conflicts in sandbox_packages.rs
    (added golang-go), api.rs/terminal.rs (structured error codes with
    .to_string()), and onboarding-view.js (new ChannelStep/TeamsForm
    structure with i18n t() calls on buttons and step labels).
    
    * docs: add i18n changelog entry
    
    * style: fix rustfmt and biome formatting after merge
    
    Apply nightly rustfmt and biome formatting fixes across crates touched
    by the main merge. Remove unused BASE_STEP_LABELS/VOICE_STEP_LABELS
    (replaced by inline dynamic label building with openclaw detection).
    
    * style: fix biome formatting with system biome v2.3.13
    
    Previous fix used npx biome v0.3.3 which silently no-oped. Apply
    biome v2.3.13 formatting to locale files (line wrapping), fix unused
    import in page-skills.js, import ordering in pwa-install.js, and
    formatting in page-projects.js/onboarding-view.js.
    
    * fix(web): stabilize onboarding and agents e2e under i18n

 .github/workflows/ci.yml                          |    3 +
 .github/workflows/release.yml                     |    1 +
 CHANGELOG.md                                      |    1 +
 crates/chat/src/chat_error.rs                     |   93 +-
 crates/gateway/src/auth_middleware.rs             |   12 +-
 crates/gateway/src/env_routes.rs                  |   92 +-
 crates/gateway/src/metrics_routes.rs              |    4 +
 crates/gateway/src/request_throttle.rs            |    2 +
 crates/gateway/src/tailscale_routes.rs            |   20 +-
 crates/gateway/src/tools_routes.rs                |   46 +-
 crates/gateway/src/upload_routes.rs               |   35 +-
 crates/web/src/api.rs                             |  187 +--
 crates/web/src/assets/index.html                  |    3 +-
 crates/web/src/assets/js/app.js                   |   23 +-
 crates/web/src/assets/js/helpers.js               |  156 ++-
 crates/web/src/assets/js/i18n.js                  |  221 ++++
 crates/web/src/assets/js/locales/en/channels.js   |   93 ++
 crates/web/src/assets/js/locales/en/chat.js       |  203 +++
```

> TOOL

tool_use Bash
id: toolu_01XmYXW1wtN3DCPZmG7qxfCU
```json
{
  "command": "ls /Users/penso/tmp/molt/moltis/crates/web/src/assets/js/locales/en/",
  "description": "List English locale files"
}
```

> TOOL

tool_result
id: toolu_01XmYXW1wtN3DCPZmG7qxfCU
```
channels.js
chat.js
common.js
crons.js
errors.js
hooks.js
images.js
login.js
logs.js
mcp.js
metrics.js
onboarding.js
projects.js
providers.js
pwa.js
sessions.js
settings.js
skills.js
```

> TOOL

tool_use Grep
id: toolu_01W88u939CQLEzQrX6xRR7cV
```json
{
  "pattern": "No LLMs Connected|noProvidersCard|welcomeCard|provider.*not.*connected",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/locales",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_01W88u939CQLEzQrX6xRR7cV
```
No matches found
```

> TOOL

tool_use Bash
id: toolu_014bDgi1D9nHLK488PuwAFXe
```json
{
  "command": "git log --oneline -10 --all -- crates/web/src/templates/index.html crates/web/src/assets/index.html 2>&1 | head -20",
  "description": "Recent template changes"
}
```

> TOOL

tool_result
id: toolu_014bDgi1D9nHLK488PuwAFXe
```
4d308860 carry forward: uncommitted session files
323a1ea4 carry forward: uncommitted session files
01bcd45d Write a plan in plans/ as a markdown file so I can do it in another bran
5251c7eb carry forward: uncommitted session files
38f07e1b Completed 'Explore' agent: Explore CI workflow structure (toolu_018R3y)
f692e604 carry forward: uncommitted session files
b56fd2f3 Completed 'Explore' agent: Explore Fireworks provider details (toolu_01U4dv)
4f340149 carry forward: uncommitted session files
e80c895b carry forward: uncommitted session files
788368e8 carry forward: uncommitted session files
```

> TOOL

tool_use Bash
id: toolu_01A2uJFzGXa6qGkPyPQH65hc
```json
{
  "command": "git log --oneline -10 -- crates/web/src/templates/index.html",
  "description": "Main branch template history"
}
```

> TOOL

tool_result
id: toolu_01A2uJFzGXa6qGkPyPQH65hc
```
0d30f86b feat(web): add live remote access settings
5e115929 fix(web): point report issue link to template chooser
37115cc9 feat(web): add changelog link to header nav
e492d900 feat(chat): tabs to filter chats between sessions and cron (#338)
aede5586 fix(web): externalize SVG icons and restore empty-chat centering
f51e743c feat(web,tools): AOT WASM pre-compilation and Shiki CDN loading
953001de feat(web): internationalization (i18n) with English and French locales (#237)
fc1f546b feat(agents): add multi-agent personas with CRUD UI (#97)
c1ff376c refactor(web): extract web UI into dedicated moltis-web crate
```

> TOOL

tool_use Bash
id: toolu_01Fm1X4MeekVsoJ6v9XxYYuS
```json
{
  "command": "ls test-results/ 2>/dev/null | head -20",
  "description": "Check test results dir"
}
```

> TOOL

tool_result
id: toolu_01Fm1X4MeekVsoJ6v9XxYYuS
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01PCsar6AF3wRyXRfQUasomz
```json
{
  "command": "find /Users/penso/tmp/molt/moltis/crates/web/ui -name \"test-results\" -type d 2>/dev/null",
  "description": "Find test-results dir"
}
```

> TOOL

tool_result
id: toolu_01PCsar6AF3wRyXRfQUasomz
```
/Users/penso/tmp/molt/moltis/crates/web/ui/test-results
```

> TOOL

tool_use Bash
id: toolu_014dA5oV6XXisvAajrrxjscY
```json
{
  "command": "ls /Users/penso/tmp/molt/moltis/crates/web/ui/test-results/ 2>/dev/null | head -20",
  "description": "List test-results"
}
```

> TOOL

tool_result
id: toolu_014dA5oV6XXisvAajrrxjscY
```
agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/
```

> TOOL

tool_use Bash
id: toolu_01TLpMrb1KWK1jxRQwJgbB6d
```json
{
  "command": "ls /Users/penso/tmp/molt/moltis/crates/web/ui/test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/",
  "description": "List test failure artifacts"
}
```

> TOOL

tool_result
id: toolu_01TLpMrb1KWK1jxRQwJgbB6d
```
test-failed-1.png
trace.zip
video.webm
```

> TOOL

tool_use Read
id: toolu_01BFJRdZozVDYfiLiBQYGu8o
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/test-failed-1.png"
}
```

> TOOL

tool_result
id: toolu_01BFJRdZozVDYfiLiBQYGu8o
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUgAABQAAAALQCAMAAAD4oy1kAAADAFBMVEX19fX///9xcXrq6uve7eQWo0rU1Nj6+vrr6+vk5Ofp6eny8vPy9POAgIg/P0Zycnvm5uj09PTw8PGenqTR0dTp6evIyMvh4eKlpavz8/Pn5+iEhIurq7Dd3d+UlJuJiZB+foeurrOQkJe2trp8fIT5+fnm5ubc3N7Y2Nnu7u+0tLigoKbj4+XW1th5eYLt7e67u7/v7/Da2tx7e4Pk5Obb293e3uCNjZTU1Nbx8vKwsLPPz9G+vsHi4uOdnaGHh463t7vQ0NL5+PiioqfGxsn39/eoqKzLy87Dw8XNzdCxsbWIiI+5ub3r6+329vZ3d4DZ2dubm6Ho6OjT09Sjo6mVlZzMzM92dn9ISE94eIDAwMTs7O3Kys3g4OGsrLGCgop9fYWVlZh0dH2ysraTk5qOjpWKipGZmZ9KSlHJyczBwcSRkZhPT1WXl526ur5naW2BgYmFho3ExMjFxcjn5+qhoaS5ubxNTVNFRUxRUVdra3Camp/ExMe/v8OMjJOLi5KWlp0YGBuSkpl5eX1UVFpXV12kpKjz8/SYmJ+pqa6Hh4uzs7VlZWpaWmC1tbhhYme8vMCnp6l1dX5fX2VRunjv7+9ubnOQkJOLjI6ZmZ2rq62YmJvn5+dcXWKFhYy9vb98fIAsrFtvcHSurrDAwMLDw8fb6uFzc3iDg4fq6uzd7OPl5OR+f4NBQUfV1db09PXC5c+Hh4+u3b9hwITIyMnz9PPL2NFCQkmAgYWSkpV2dnrZ5t/U49ulrqzS0tPQ3ta7u72VnJzk8emh2LY2sGNIt3HKysvh7+bo8+zBzcizvbq3wr2co6IbpU4lqVaqs7Ehp1PG080+PkFcvoCJ0KNrxYzW7t+PlZbc8eSuuLWiq6lkwoe+ycQ/s2otLTDI6NTa4d+P06ju+PLs9e86Ojy6xcGn27rt6uX7/vwhISP1/Ph9y5rW0suc17KW1a11yJSEioq95Mve2tTz8Ovl4tzNyMDQ69rz+PX28+/DvLKepqaz4cT8/Py3sKW/uKy0q59yAX6uAAAACXBIWXMAAAsTAAALEwEAmpwYAAAgAElEQVR42uy9CVwU2b33fdKNqbJ96La7jSxtszarLCJNA7ILshqhG4VmkAZEFBFFZZDNnWXEAdEh4oow6KgzKHNNvIPbOM5NxntnMslksk1myeRzbzI3b+5NcpO7P3nu+7zvqareQFYVN37fz0xX1TmnTlUvfP2fpaoIAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKZPwIvz5z5y5r8Yhk8WAPC08/rrCpdHX6uL4vVv4rMFADzl/psxT32TxacLwAw12x5ti210g+1R1/9kDzf+gUnA65N91Cv+52tj8j8rJttTfAw/VABmgG/Ml4jZR4hY4ioe8af7iOu//3Cvz+TbmfL7JORFxWT++9q4TGZAxYuP8zchl//1X8vl+NsAs8F/j94N879h778ZV9H812f27UzpfVLmT9L/J/+f8QX4P5PoxmX+47PfX/8vM38NB4Lnvf3rOiNmODaz9T/Zw411YI65k3zWLl+bgMkGT+Y+rl+EVX+8AvEXAp5rXpTMhBgkL85s/U/2cGMdeCqOip5IgNFPiQBH+A8GBM85c2ekw0w8d2brf7KHG+vAz4sAR/kPBgTPuQBnxgxzZ7j+J3u4MQ48lqOKdE9OgIUZhWOmX7tRNC3/wYAAAnxkRhrKiM0VP24Bxvk9IQEGlo0twFW1J6zUrhhLgGuiHk6Akob9+/d3BYyRc3z/rvsTT/WZV+T/awwwEgIeDvMk1kLxA+0dJhmdoliQM17hO+aZGK5Cn3q0uZPexVc+RQEuWJysHtnK8zOM0fe1S/wgRlqi3x4iy+obVVYbxL2mTC7G8YtMJMC77us9p2+2oryHEqB6rFWLAFtt/jtxqPN+AbKqyKKHE2DV/v5Tnft7pirA31WNHwAiBAQPR9o2dw/6L6yk/GzxxlA6TpksYskREW+mMhEhIlF4iJvWfgf5znVpJDkkJKSghBCnzSWOHnmExNJixVuFAsn7ksY5liKcF98m1QbNa9S4TaqEclq1QqnZXhAoJzpReHjJasUEAvRj16XErGHtQqbD4Vc1q60KvJPOsk6BLKu76vQgAoykbhUnpDrbp+Xu9dh2dYhlZYZJbTN+kQkE6FzGsiarARPXhRSoEic6SPodfrFw38NFgAcsX+b6+yLA4A77pm9XzmgBFobEFQQ8lAD99t+k3/pvvpy2AC3O+/Z7P/zhe9+2bOFvGDw4ARotMWRLiN6TEOdFxFflLWOpztK5Pw4RFSDNDl2stN/DTbknjV9JVxJxcayc+OerSWwyIf4yITBQ6cY7WK4b9xpUEke0KgMpS5YTbz2Rb1wcRiRnY4nOkRDf7bvHF2CUUv8Cy+7WK4csKf7hOnZwT6xlc6ueZXM0D9wm5QTIZqbsXmxL0nn0idn0cN+ZEqAyg3tdb1F6opJaPD9jgoPotz6qJvBCvX7hWE1g/x/bC/DHS0cLcGMGKZE8kAD7ur40Hqex/rUuznJd+88QknPxN7+5qbUXYN/NL6WHuKMdu1T/ZW8m/bf1x/t/9+MT9i3gb8/h+TbawODhBUilJaeWC6e/Qv91pOjrRFZIYiPLaVZSpIYXIHltjf0elcSNF6BcFUEqD3Jra5N4Acq3+XNb7jKPsmNnYzW5ZKVq+wv072p1SfnXhV0PB3KvK02E/82adhKSsYXEabigz08QIEn2HleA6j1sMOvkyw6xe3WWVudV+jIYxxoWayIz2PMh+Y7+JTLHPMM2drC4z6OcthOjygtWr97FRu0N2ew3JQFuUno6p1uTdm7hXjODWdlux200OTgyf0MUm6Z0DtdHsOz57ZojG3RshFvIPh0vwKVuIZtzrQedXICpSZu4xfZBOwGyBw+baxwsTvcoPsKyZxZrsipZdk1isck5P4Q/oww9K2738DhsfmXLc6hM75k/hykJ8IBy7VrlgQcQYL6CjBHiT0GAab/7zeXe/dctrQEuAjT8+MubA7+rUtgJcPjHA7/Zf5n+mjr2tzb/Zr83SWre/2XzOfsW8HuCAN9DGxg8ArR3VrcTkjVEf6EirmnDCXBRFvWi8gUqQFFN8O49uSP3EASYQsO5douuYhP8Y1KbeK8dc/SLDhCZtIq1WUFFxVGkfbEkw0PoZ9x3h3t1Xum2bg/tJozbs6QycohscjPXoRP55yZmGcYV4HnaWoy9ejaFCqnSnDTosSVFS5erlUUpHnES742D4ijNoMQgY7WiRXGHN7BnHL2DVmbvZvdWSjLbpyRANmNt5EFr0upMS3jnHLckX8LqV2oz97Ap+ZVF+nZ2KCSvaPU6teSqd5znZk6Aku1lQUc8Bi0HnVSAL5Sx6bTBW1nG2gnQ4JFhrlEr0usyQnLZ1U26JM0d1t3LX3tmo7cvV3CTF5uyYVC9QS28ssX+LOuWYv4cpiLAhXxUr9w0bQEGexGydfeDCLDiyzhCBvb7CVvX9ydzL+cJObq/zU6A9Qpy7Mp+HUncf5E2Fr780q4JbBHgjwQB/ggCBI+A2MiEGEJ2JiTFlMskFgHSKE3sIeEEWFKeFSkIMCdqhADdqc321dCeQr1+JW00l5d7mIR/ybfFkQAZValyIR/tce2lgzF8zBjOdy3uy84L210SQAxbtm+IVJOdbXxzbDUVYHl5cZN2/CZwe5JTFsuGDMUssvUKOpdk0z5ATRENkFKsTWBegIPsmfy4Bdtpob2x7NnDhik2gSl5KmuSm2VIRKZmxSE5fCAqY1PoaWRksWWrqYJlav+zNLVgkAowuJirJc9y0MkEGOe5hGUXb0qzNbkTHfUbw/USc41aEY0yUz1Z2s5nTSbWPcXWBKYCrNxOc82vFgGaP4dJBFhEA3H9WosGA4umJcAjS+jLWafpCzB6/4/v3bt3fP8yfqt2fzU/GkKT0vc3k4BLHE5UgLU0+SQN/E7s535lF/cXQYBghjGE0N/zyvJ9OSFyiwDFji5LTKy5CewndHq36e0FGLOHD+boyG7KaiXfBHbRl1kF+Arhxk88PERKlr56iPiQQb2Hz1/sQV/23iFb6N/h2mKSsoXmpKwsEZrASzZPIMAFTrTJGxK8oN0+Na3YM44/xsoRAnyFZmnUu9bTxcZYNmlPtj5iqgLMLbCNUZjsOviKg9ldGzQhIjbFjXY/FrPOXHgYrt7FHz2KFkl347r1dloOOsnhlDHXqPq2ZmptSYmRR8qyB1lzjVoZHVdeqYzLpzlHmlj3pBEClLSHJGw1v5oFaPkcJhGgrsxegGXTE2BeE/eLOeA0bQFG7Rfgu/Ne3t/A/WtpTmogBn6ZQQVIQ0Kyc38p6djPtRpu7L97vwDRBAaPjCKuVao8QiR0fDYni1gESPR5WUUWAcrD1cKNL+0FWM79Be3mdeVcxguQLGkaIcCDGXzYZxsyjDXxizKubHkMCad/eS4yQ1FIKNegPiAIUB0yrgB3c03gLNUmuybwHW5MNLBJnD04YhDEJkB/zRnWsI1zkW5x+eQCPKKnxAZ7WJOO8Dsd9jcLcPCVGFaXbRHgStpUzhGp77hbHJnLdUkeSLEddKLDZdIuxcR0fsHaN4HXZ7LmGrUiLvRbJM6mjVragBcEuNIiQDrbZ5Mmz/yqWkD7AVMsn8NMNoG1Kv7fzO2xMZKAoqhpCLBwf8cZDu7nkP47Iz/pqv5LPokl8jiOaCrAVD48PEdbx1y7o3+/v02AGAQBj5y4EjoK7OhPFptIgFulTYBJZ8uJWYDsyoLo+/oAh7ZzvztFyUo5iSlw4gQoX+qeOEKAS9wU8sBdpKlMHpDMG1S5VvgT0jiRoYJCsmWRnLywjZAmvYLEFe/iBahVrploEGSIdTpDXzYUWQZBVDpW6xXIbjGJtcooGp9JWKd1TnYCFLu5HdmyLdawJYetiZxcgH5JFD+draS2ONNAB1d8zQJ0ytexnvkWATp5ON/dnK329djE5qw5Q4ucKUlhk8KdzAed+HBxvOQ2xYyIZjkBxoRozTVqRaniIrp6sF3stG2TIEBnZ4sAz3uykg33hFd2zSKxf36K5XOY2iDIwoVjDoJ8bX+uv5Xc/ffNA9QLcwC2bikp2LtlOn2AP/4x7QFRn4qgrYcvr/jySRc5vx07dc2uD7CbvnbuDyan9h+nWT/m+wClBNNgwAyRrlGV0Al8vhtUmmS5TYByx3RegCKRLH9P8P2DIPvShQAyK6REk8bNA5TJHNujRwhQvrpEsyaUiDeXhJv4mj3MAxzpIQkaOo7oekDjkUXNGKrPL15Xxs0DlMnCt4w/CMLmxsfTkYU+u2kwYlN+cbbel3Uq14SkitnBvVRVi0PSbAJkBw8rU/S72Z3hV1UxkwtwkaMjDcjsBMgGbwjRFN+xNoHbsx1tAmRzTKv96TFiVB6a3XyRJFXJtmus5aATHs6Payez95LZ0QJkD5jMNWpfKdOE0P7OuHKNhra2eQEuKF5vFqAuctu2ZInwSrWr2VyeYvkcpjQNZpNyRPxnE2BE9Y8pX37JvVar7xOgXGZtPSRMaxDk1P6WU7W/+Z0T0X25v4Pr8ssluV/+Jv5cy/5EOwF+2RHfxVmwsP53l4620rYw58PruzARGswUEqEN4ftgN/WVaMdvgpiv9DgWbdd44lDECfuEhQrbx5yip3QliJpdn5TkxtpfC2LIEbrQBoVBDon5f+s1IZlF7BkNnZkiDpp8EGSPuWJ7AdKZ1Tr7LV9fO4eVidmoEO5wg1bpaO0POuHhPE18w3YcuBqpxH2Ft6W1k5rt7WkNtlfW/P4GDVNpAsutoZ/XeNcCnzgx3rXAATI+kg9Ymx0wvXmAJ3+zf/9wCiHe5q6/lwk5b9y//8taYifAZXX7f9fLDcbFtf5u/2/4DsPYqt8141I48KxTs5o89LXA6uRk3bSuGcvUbA5xFk9tZvKReDee+Ngp3m1qX3F5wfkpHHTsw3mu3943Yf18FDsj1wIXjbVqL8DMEw0NJ14e52YIcr3jxiXlBfrQaV8JEme4L4m977K6QYtXo60jLQo5boYAnnUCAp7EzRC0UYNTvjQjWGBoypXrhgxTOeg4h/MbnORuVroncjMEjmXchcAvj3s3GN+MJf64HRYABLfDenZvh1WEG6ICgBui4oaoz44AcUt8QHBLfNwSf7beEt9egdAfeO77DWfkKWrzA2a2/lG4hj3Ww431Pp8nAeKxmGD2MBOPrbR/TuXrj/exmOLH+ljM16f1WMxoZnz/MdFPzWMxASB4MPpDPDDcV/wYn1T+mA83/oEnfzC6ywQhYLTL0/RgdABmUSv4xbmPlBcDZrb+J3u48Q9MAr4xScNSoRgnBmQUikkanK+H4YcKAHia+eY3JwkBFaE0crwPlg1VuDxczQAA8KRhX5/YZHKX6DFxkU/szW/AfwCAZ6A7Yf6jb2vPfxHtXwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGeauQAAMEuZdb7HP3kAgFkb8OIjAABAgAAAAAECAAAECAAAECAAAECAAAAAAQIAAAQIAHhucfnm/GduKvf8b5qfIBWtzfn6feRooyFAAMiz8TTkaT5TOGw6ZzP5Q5Fc5rtK2GcNiet83oDREdox3mCYNiJ6MgE+0i8Rj54Cs4dvzJeIn9yfvljiKp762YwuPQbfdGWfRVxf505eqx37TY1MnzvDX+IUPmUAnhv/Pem//fnfmM7Z2Jcei/mSZ1KAkvncyeeME3qF5UwswEf+JU72KQPwnLR/n4KAaf6x6ZyNrfSYzGWfTXirfX28d/X1CQU4A1/iJJ8yAM8HLz4FAZPkxemcja00BDhzX+IknzIAzwdzxU/+b188dzpnI54LAc78lyjGUDOYFQJ8av74p3w2EODjeM8QIIAAIUAIEIDZLsDg8fqYcoS2V7DBmuJ7RzuyiG+O0KTyfwICjBuc8F3FTX6sqLhnS4ApYzWGN/lKdokhQACmIMDzWSH7dKPS8kcm+C81r9zZJyyz/SxZg9vKc0fue6eYZWOoRrYseNwCjIpPVp6aQGCn7kx+rHO5z5YAZYYxqtaodVedIEAAJhdgjEewdrXXxAJM9jSveN0bLcBNV0f/IXECLM5g2bzyxyxAcTyV187DDyfAJ9gEVgQ9OgGiCQzAJAIMXuScxrKVS2jD9hU6DeLI4sPW6Ck/qj05hS6HTMmVLLs7YW87n1xUQJvGC5ydczgBblpt8mcz3DycI9hdi52p8dI30ZoCOQGaCg4uYcUhuscrQN9Sev4G+v+do/E7xexg5snaNNa3NqVpiE2vje8Ts6dq2vR9giv74uN3sazuXNO5OMtGWm3TYQO7zJ81HI5vy6Ox4L3k2mssu/ToyVNFj0WAdxofTIBL3UI2U/UHR+ZviKLfwnbNEY3asI0dLO7zKKfvI6q8YPXqXRAgACP+dvw9vGO3pfCrsXtolLc+PTnSEk7k79m6RJPODmkCz7t7srnr9UK5dBrU5YYE7j6wzo89r9od6BER0X61Ji5WVeld4M+uXkYtsoET4KaSTNr+3Xz+MTeBl7Xd4xReFD8Ud66SrUkcjDp9xrd0Z5Ehr9ZPffQaeyrVyf8k3zV556hv0VEnSVvN4PlT5o3BkzrfzBg2dYhNzIzzj89hj56LGzo5yB7Nk1TefZoFKNleFnTEY5DVr9Rm7mH9QzYVKWVqg4zVihbFHd7AnnH0DlqZvXv00cuCuNegMggQzFIBrs6kXeh8M9W/ZAGrKzjDsll57BlfX18xm0/jvso9fNPXL19ibQIfVrLsYroeJfJjVUksm2pi0zezrNaXZTeutBMg3wRmF5dN/sdmL0CnIe7Vj+9vHHJ6AAGeqUwuPefEpiTSSPQol2CIz/EtpSe3jLbc4/zYU3Sx7BqXkZfMRacRtfTl5KCwEXeaPzwVoJ5aNDaWPUrf4Kkktjbd8FiawENJi+qTknynL8Bg+nmzkXnchlrGei+mb0UkCHCQPZMft2A7zdgbe9/hF9FPOK4dESCYrQIUiRISCkR0RbctnWUX0q0EkTeblZ+fH8PmUwtF5LN7OVuE+1sFaFpN/5ZoMCjO9/MVFdPybrwAnZwjVXTX0QJMXTT5H5udAAfXiWI5t4qoeGJF6wYfaBqM+twpNrM0Pv5kKRtxKr621N/3NE1t87f2AXrX8Jc93D2ZfI2NoQXjS5cKG+y92vi7BirAQW6Pe8vYo3SnzHusf+rJzMfRBG7ulUp7e+9OX4DpbnSh3Mnu2qAJEfH/rLEhvABf4XsDd62ni433C5B+KSO+EggQzC4B7uszGAy0Ty8u4Qjdyt1GtwyWuRP5VEILitmDNMdAVWQfAe6jaYM0Asz243fnBOi2Wi3Re7POVHgpY0WAE/yxPUoBOiVx83Sa2HShxZqaLmFrc3gBnqOnIzHYCZBu3mkaEsJE8wYXEaaepwIU03YvS1u9ZgHSD8j71NPcBM7lhqEOpAy+EsPqstky+m+Ur8hOgP6aM6xh2xgCZDPL0AcIZq8AV0YOsumL2MGslbwDPNJZrTLYIsCNBsPGZHalu1ZM+5VYk15ITqejxd5ZWnE7FWBTqljsWckLMKuPXRruzSZu0Er0ggAjt3J/lOcn/2OzD9+C0zn/5q3lBinSg6ffBB48SXfqO8fmxDuxSTvZtiR2yBwBphw9I1lWaSfAtPOs5GiuIf4ODRkNwkZEpoHdGcs1gZf1ieNq75gFaFimZpNS2aJrbFwKG1fzFArwTEkKmxTu5ERH7j3z2QUaP7HJXoBiN7cjW6gA1XdZXSLr5I1BEAABCiGSxiMrmPUUySjB7FCWR4jJOgrs7RGyngZC7RpNJO0gC766TRgFDhGz4sUhJWV0FFjrpgnfMsgL8FrINq+D3qw2Mru4XRBgpYfy8Y8CszFNtU1HaXM1JV5Zm8NmnKx9uU0QIJsYf3KZr50A41Jra70lbHBtfPw984b4cFMynURIBTh4Kj6e9oGaI8CUprbaYDYvXnxHbxg66TuDAly658FGgZNUJdtoE74925EKkC0L0Zg0dgJkBw8rU/S72XQP8bVwQ16IFgIEEKAwGSRoxF+A1v7yD4nwhyI2t0TNWV5p3HSTM+ZpJ1YbiOPuq0HCZkQ+9itBxDrziQzavQUew5lRdfoKQxuDYtuGwfp+zthfRiF8BGLLf0/jpXBa++9DMlJxEtqDeUaTO/k7gAABLoWbhAVbpl52YxKuBX4argXO1GwOcRZjHiAAD++L4CnHQOJg3Azh6bgZgjZqEFeCAIC7weBuMBAggAAhQNwQFTdEBbgjNPvk7wgNAeKW+ACQWfpMENwS/8EeivTon+w3PwB/G2AWEDD/yf/t2/7YHsFDkWblYzHFj/yxmK/jTwPMCsRP/rnAr09Lx5PEJiwejP7wD0b3xYPRAZk1T0aXPMF+wFF/bJPreLLYxGW+67MXA0pc57twJx8doR0jBgzTRkRPIkAS8OLcR8eLaP+CWdQKfpR/Ow/7xzaxjqcSm7iw8+c+a8x/3UU4+WhtztfvI0cbTSYTIADg+dcxYhMIEAAAAQIAAAQIAAAQIAAAQIAAAAABAgAABAgAABAgAOC5MwIAAMxSZp3vGQAAMAMBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAJg1Agwrko+dMRT82NQVbYAAAQCPXYAB16u6q86NmdWkfEz6C91YkuCxEAIEADxmAZ4aCCO6Ct2TbLnK3ZwVRK3JgQABAI9XgDf20JegAKI4VFV9j5DDnVWHjpHcjroBHak9SkhtZ2spIfHKgarjYcTQXNed8ugFWKRR0Ne1eeRgrKqMxJRrlKHkzuJ2jVILAQIAZlKAGfXH0+bR5Z7r2tgWV0mFuvDyTtLhHV17g5TqyeFef111G7nRkpvTfZ7ccHdJ73n0AlzoZl7Zu74oIE6TJE5tIhn5CyWLTRAgAGBGB0Hy+o0NqYRU0XDrZmxQPR/h9bZxMRkVYP/LhOxqJDeO0x7BSOJ+WTITTeCdyRYBxhAS60yIIj86YwMhUe4QIABghqfBKJbVXzNIGxoapKdIZmvDjWMko9p4WccJsDuDEF0VuVFLOwtVRNts7JmBJnDeZosA/QlpT6Qr24oy9tGmsQoCBADMpABjnejLzVNyI2uZ/FJ9kusVPNTICfDmXULSOiwCpOO1p+pDH7kAg0K4Y2fE8AJc2U5HRfKPQYAAgMcwCNJ/jKirkkjzSXnh9dyhywpyvFTRHEH6qjkBHm08pmgutQiw9C7RGgsffQio1BcSdYk/L0C/Ei1ZWU4gQADAzAtQ3GzsNFK/+TY21B2Xu1yq6m4cJKfqunvTOAHKD1VV9SssArzX2tuyaAY6AY9tLCgO2SE0gcluj5I9vhAgAOCx9AEWLp0nLBV8hyAf4cmtox3RYfZlJfKZmQqoCLKr+BjmAQIAcC0wBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAAAAABAgAgQAgQADALBTh3loGvHACACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIADgmROgX9Tayp3eW2sy/Cb3yc7Sx+8wF2ERfV9GNAQIAHg4AeqVB/TOnpmmsoNK/aQ+uXv6cetP7qxyT6IPad+cpUriE4I8HB0dowjZkaVyEx5VLNq2rTyFkDWZ3MadbAUECACYmgCdk2zrMc4TmejJtGGXKF2cHMVk40Ki1sjli3VkaDWfrk6QkK3t/KqMyIdKlpJyEae+SBEECACYogAPjLtBSOuyTmNtZavxUjTRXTRW3XAh51TkTvephs62xybActowX7yJxEQTecExUqYlmzJDxTTdszJMay4i4zy+kqxfk06Ia5YHBAgAmKIARYScF/Gk8xv21F9nM4ZvGnRV58mN0kL/qljS1kwyruhDdw0HPS4Bhh8jJNCbW+tT8gl9mze77wsjGz3dvbK0FgFGZ2WQ9WmRhJT1OUKAAICpC3CcDSrADEJ6Ewm5yQd8hQPxvADrqWGqPR+XAEPo0bwD6UqSeyGfkLaLxnve5ECxC9ndJJz1xi2aZBeyXr1vqcvZUAgQADDNCDB9TAH6E9J9npDmNpLeUdUp1fMCrKI5zUcflwD3FBHSRoc4/LNc6dZuCQmlg78ZSpJM+/+0xcJZ+/lxblyvzmtb60wgQADAVAUoCxu/D9AmQIXRW06an4QAA9uJxMOVqN255q7cLYJ4m/gev7wDLmSr0toHyAtQnhDpBwECAKYsQFOKbT0tdTwBHqtPJ0kVT0KA0fv2qugpusvo5JccLiF0354Neio5U3FkpGSkAIl3OYEAAQBTnweoVO6jvWoZJtNBpZKM2wQ+Wl91sf9JCJAQicvoBJZfhBowERoA8JBXguiSRKTGeWtNjG7CSMxACC6FAwA8d9cCi8oCcS0wAGCWCjAQN0MAAOBuMBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAIAAIUAAAAQIAQIAHq8AowtfnDubwFcOALAKcM6cOQ6zCAgQAAABAgAABAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAHgeBPjW+1998NFHn37/i7cgQADA7BLgvnfL3/3ws7c/e3t907tTF8vHN2+NlXz7Txf53O/T3He+T3nfweHSx+bMd95++x3z6gfvWsp+/PZXtyY+1IURi/szIEAAwAMK8MMvbOtffDh1ATaPqa0/VX+fM12dlEaT71Z1dXVdd3Co+krI+35d88UK89E+HDCX/VNDc1f3OxMc6I0PL22nO70TeXabsO87JR4eHtSrH5zd5nWbTxF5eOylVW1+m9t4P/8CBAgAmJoAy8fdGENGk3qx+jPu9eInV6gAT5gDSosAu6ighABRECBX9v262w5vdEwUeX7adOEtj9sObl85vBX+xhv6txzeFyz9luq2w6d/4ZKmDhkAACAASURBVFdlDm+8r/nYYYOIc7K76BYECACYmgBFNJYS8XzAb9jzQWdFLw2tvqg2dtDFx9V1DVQ+77ZUNFINdfLp3VRqH16/bqz+lKrq+w69w8ZWB4ePei9wArz8ttBIrfqsq76RNoPfpvHaZ100Euyq7/lkQCh7m+t3vDiRADfQEvqvHL644PBG9i0H2ob+6u1bXOD32Qe3LIGjjDPqpw7lm+k7eGd7CQQIAJi6AMfZcLhQ8YHDR41vvNPw2a2P6t5yGPjE4eOut76oe+fCJ3sc3q+gDd2/3PqKFnnX+Ontd6kPq/sdLlR/dsHhdsMXDpwAe/7UUE9V6VDV+v7tP3XyLrxQ/a7DWxV/ufVBxYBQlmr1gxPVtycQYAj12UcfCbGgEBJGRm7/5JaD22cJe86+YxHgBdpMLv/KnVr2Uw8IEAAwvQjwgzEEeKv+Q04mb3dcuHCh+m2Hxn7ON983fsB5iwrw7Q66PH7d4d1qOqAx/LHDBZpezTVz/+TAC7C7/zYVHxcBUkEZ3xe6CG8Ju/1pQCjr4PCXxoZ3bwsDJmMKsIATIFfyiwTBbF/RU/3wI4dyxwsOH6wRztrtk/D4Cw7lb33y8YXiWxAgAGCqApTdGr8P8IPq+uoPHD6RtrS0SGnodtPYS5vAH3Yamz/mBPjJZa4lWu3wbjNdVrwv9AG+7fB+1W1BgLepEC/Ufyz0AfZyQdy7nTSL3+1DqwCpZxs/oc1iypgCdKc1fcg1wLdz+v3gtsMtWu0X7zrE0/6/dxwFAb71Fvcmyt/66sOvPnSAAAEAUxXgZ3aB11d/uW9ay7vDtz9rtLaJPzV+yo0/NHfxESCN/DidjRLgJ8NGo1Fa/6HDh7eFyK/qbXP+X1rfEZRpiwC/z0Wen3VP0AR++y8Ot0vecXiL998bXh87fPQZHwF+VX7B4dN3rX2AvADfUFFdQoAAgCnPA3z33U+ohb747LP1744ajHirmg521N9+q+JTh3cGvnrj4qcOt1s++JTOf/mwgxPgWxUfOXxc9ZFVgB99wEvt1jsU6Re3HAYuveHwbsMbDlW971x4t+WCw0d1H9+6dcvhLeNHdPDXLMAPGj52uN34J+u5fOzw6UcOb31iN5PlwidZl6ijt8vo5Bd+QuGtT9wT9tECnzm6u98eKUCHj/Y6QIAAgOlcCfKFyOH7H451JcgnxtaGt/nBYOPxNxw+rWqpOnHh9k1ja+/7nAC59CrqTIsAey7bmrXcPMC3uiqqWqmzqj5sMdI9HIxSDirCloruTyxN4A/rqoz9FmXdqvvMoX/A4SPjiImBt0dPeL4teO/WbUyEBgA89LXAorc/Gmfi3zsjHPTOhVHiuT3xLMF3zEp9Y5SqRmy+c2HktR1vTO0SD1wKBwB4RALEzRAAALgbDAQIAIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECB4DEaWVDHOq1GXSgj5+wase4jg+PvisIUAIEDwpcqSNwkqzNM8u+bz0OMN0SUMn2722Qiqtv7H8gQ/fKo3CdwABQoDgmRRgk7QrNbVXuueBD98p9cd3AAFCgOBZFODyuoYwhjEMV6x40MP3SiPwHUCAECB4OgRYeb2q4zRrL8DQpuq6m6kjG7mWUkE3ldxmtzSO9uadulh3MdWuSy+zq4++3unSM4xiT7ex+hSXuHRPZ+cJLui72GHor1tGD6HDd/B8CPB7//zx3NkEvvLnUICVV4zNHdLGN20ClDdKW25WSG+M8J+llIDCaKR+LJW2XG6Vltp1D0qX0ddr0kOMT5e0+XgvlxdXNTwwMFxFfdlyZaC+6zDTwbkTPA8CnGVAgM+LAFtO83RSAbJGzk0npU02AZZKrzNMdK801raLrZRApJQGeTXSRsKs6pHeG0OAC6SXaR3N/T5M9RU6uLzrCnVui7RfTrOrpb74DiBACBA8MQFayWPSeam5XBmwCbBDSpu6TKx9CGgrxXNO2iHnAsBNdD1FGs8E6DgC7AQYI+0yCLHiFT7crB5eRQXIt30bpWJ8BxAgBAiemAC77vA0UgHGS6XVFKnRxyJAMtzAldJZGsoctlLcVuyVVs5uA9JOmtYibWZO8TZtsxPgqgHpcPVJOtqRZ95TGsy0DPN1DUgD8B1AgBAgeBr6AEulVYcoNw+tsggw+korl+kr7bDtYitFNzbVN/ChXIf0Mk273qxkUi5x7LITIPNmIu1GlJ6ksaNU2HOpRYDxfEMYQIAQIHjiAtwqTWZGTYPpveLCN22zbLvYSjFMlLFuKb9yQnpnVM1tXNcgc5cTIGVFX73UYJDetOSaBQggQAgQPCUCLJJ2K+jElyy9TYAq2qvH+FzkozkztlKMX50xWEgsk6roa+6hrdZilXzN/VSAu46n8N19cUyLkdNl06FoiwCj7q7AdwABQoDgqZgGEy/tjo9vlZbZBOjaeqU/vlF6cRVzreGEtRPQXCqgRSpt5rjGrLgovdh2w1ifY63ZYJR2nRzopAL0l1Y07dwrraYN5uGGG22N0kuWCDCsXpqI7wAChADB0zEROr5XKm0ps58IHXHTKG24REO+VGmmZSdLKZ1lAPllOsJ7qUEq7ciwqzqF6vFmLNcETqHljde54Y671cNSYymxCHBF63AavgMIEAIETwsSyeiUFVp+sVc6OFEpSpxiVIJvoWVNEWe5lkQRZH9VyapCfOIQIAQInn4GuvEZAAgQApyltJTiMwAQIAQ4S0kz4DMA0xGgX9Tayp3eW2sy/KYhFv9+xUTZhSk7ddaNY9d4CMngFhJr+iC3mcuvBl0LggABAI9dgHrlAb2zZ6ap7KBSPw0BXp9IgLktPf11tZatoA5K9zAhRm4lw1qqrYFuHuLWXKqHl41bmYuwiL4vIxoCBAA8lACdk2zrMc4T20Q+BePwZfpvEDI0bLBPP3mZHKsfWfSGVZFtAz3jCVDurHKnp+i7OUslnGmQh6OjYxQhO7JUbkI0Kdq2rTyFkDWZ3MadbAUECACYmgAPjLtBSHp3RTc1S1KPsZo2YP166lqOElLbUjegI0O9fHoXlU7qoUMVjZWE9NGiqS31HbRR20zLSepdiby0taJZy1XlWuFPdK1kHl/vy10VN2mT91KmeVtXpR5XgEuULk6OYrJxIVFr5PLF9Mir+XR1goRsbedXZUQ+VLKUlIs49UWKIEAAwBQFKCLkvIgnnd+wQ1FRQ+4OyLUNmQE7q5zIxdNkaYdTTNWg4nQpya0jQVWLAu7VpZNaY2yhkvqw5zrx68gtLO2gTeCO+EWNNL5r6vLTXrrI1VV6nXYBdvUPt7YRklKVwZe6eLzFOOBEMy/WknEFWE57JhdvIjHRRF5wjJRpyabMUDFN96wM05qLyLhAdiVZv4a+A9csDwgQADB1AY6zQcLqj4bShXe1QqHoySQDl7iBinsV6VzYRgV4uJoT2yFS20MHPYb9SDTfWRedISUkuKe7sfUcIZ1USQFcy1VLA0DSV1czL63KmxwqVSiODReRrusGyQlqzrtd88YXYPgxQgK9ubU+JZ/Qt3mz+74wstHT3StLaxFgdFYGWZ8WSUhZnyMECACYXgSYPoYASU1jfU8NOS1tbW2V1hJdv7H7FCGneo2X/TgBnr5Ei2Q2ktrLdFnBj+aGHmppMUqJvDWVa9fWRF+xDAXfuM5FlIX0Jf4yqecrvEbE1JiKev/CljQyvgBDqM+8A+lKknshn5C2i8Z73uRAsQvZ3SSc9cYtmmQXsl69b6nL2VAIEAAwVQHKwsbvA6SRXe2wOHPAOuwaa6R9fcTpegcnwEwa+ZEmlb0Aa6tdydAVEiTlQrOL8aSzhg7i0vVB41JOYefpS3I/uSSEcuQoHSVxqRhKkVZUVFypvzy2APcU0TES2rvon+VKt3ZLSCgd/M1QkmTa/6ctFgTo58e5cb06r22tM4EAAQBTFaApxbaeljoiq6iHDjnUs7q680R78568OZawrel9l8NIajUnwKKKuySi6q5VgN6V5GSPIvrSFdr0Pa4g14xp5Ea1JPoG9eQeLgAkSXXBJKjTk9xt8SNJjWJy8YSctLXIFVpK9VEx8W0KJUdzybVM+5MIbCcSD1eiduecKneLIN4mvscv74AL2aq09gHyApQnRPpBgACAqc8DVCr30UZlhsl0UKkcldVk7Gw5TAeDe+uMpXLS19BadcOF7a9o7c7lBEhqeisakolVgBdVdMafsaGNClDdaKxroB6bp6ozdkQQJ2MEX1+qsdV4gwsUG+oaEgmJq66r6vQXDsU1ge8Zl8pbksnx6hGT/fbtVVFHu8vo5Jccvpm9b88GPZWcqTgyUjJSgMS7nECAAIBpXAmiSxKRGuetNTG6+yfh+QpLiTBdxZUf5lCIrfni+2YASsyzk4+Zh2ijC0fYzN9sJ3O9QU6jpzy72GY+W5CM2iYSll+EGjARGgDw0NcCi8oCcS0wAGCWCjAQN0MAzwA+ujHudJDy8gwfNcd/om3cKx93g4EAwaPALZEhoqLx8xPrhqUdutGph3pHJbCpdnV4r+EXCSkPcD4y4cb5i5xHJttvpySEqNLxzUGAECB4FAL0EWnHzQ6Wnlvh2109qQD9pecflwB1BUFMkSwHXx0ECAGCRyBAJl/M5Ol3bVNF5WSFJJubl8H9dQOxDHPvOH3E+elhH6Ywq6Wr1k6ANd0tJ+hTMX3iuxou65jKVmlL41gC1OnDvTYxcxNWMCuuJjGMKZbPUTg7qsro7e8rEwoOxDGMV8xGzeqgUQIM9OAFmrdZs5jlBZinj1F5LFrFhNI9fErW4quDACFA8CgE2O7C7AhpLzKFe+Xkhr/AJ/s2DHgfGhaeY+TT0cisGGhdVjvcZhVgRW/yjSv0mUanr5w+19tZWKSXHt85hgBZD5P6tfwFPho/JkfWzjCqIS5j+Ro3/zRVGROVnaZOLmYYR1Wev5t+pAA1ZWpPmZbxz67xU5av4AS4I3x9cNLZRfwZlYUr8NVBgBAgeBQCpOwI8WGILIZhnIW2ZnxdNH1c72Vh/UoSkyFdwDAnG6wClFKTlUoVq+pLuQfALRvVBJblc4hSmK1edPPwGkZ5hDm8aDtTuI5w+er8MPrc4J1MNF2wIjHjuJK2ofPJCAFGUs2FL2Q2etOnI4Xn8AKUiWkx2Sqam1zshG8OAoQAwSMT4B76sk7NMJ7J/PZF6aFDh6St3Gqi9Bz34EvVoUNVUoN/A+Uuc6iOZlyTJvlLd9GVlhOjBBgZwbEthVnsSTejwpl0JePltF2c4cbnp+8xF4zb7bmYdkA6UvFGiwwjBMgFm+uPMKKrJpNJdJ4XIPd49VUyOtii41QIIEAIEDwqAUaOFGCPtKmp6TjX6ZcyfJq+1vLbTQbtaUowc6iFpmVI05Kk9+hKp2q8QRBlGTdAku0z3+MlR5/2FE/hYLvLhXJpBcqVsZwAF9wvQC4QdaMC1C9ZssR7KS/Aq1zreZ0fnROjx/cGAUKAYOYEeLqFjlG40CZqsPEEt10jpVNhVoX6WJvA9EHAR6XsvCs0UgsdTqUCvDuWAL030mUsbQcXv5DMxCSX+/EZOQW0uSuOYdyoHn0nFuD63VyXHyM0gemgi5PoJXxnECAECGZWgEP1WUtrWg4xTg1Xdt69ezdA0dmYFNXTaXlw+aH6xpRA4wDDXDbeTbpY4cRE19+8w4Qp40YJMC57F4kIp5P2nD1SmHkeGmF/krU6zFDuzCjXRAcoJxZgjSZieVS2mhdgvjLU4NVE04M3h+KLgwAhQDBjAmT6eqVX+hW0748nmFFX0wnRSxnrNJhT9VcaqbJc+o3S7jSaEt/SwARlLxg9DSbmqqwkkK6vFdG5LF6Wpqth8zqZPprRJshCNk0sQMbbQxa+S4gAI1e+InOjQSlTKYvDFwcBQoBgJmHfHLmtCBuxuco8EWVFAGO9Ps1njGqix6xcvopfhC2f/DwCzLVSR69wMf9F4duBACFAMKvgg1QAAUKAYDbitBCfwTMqwOjCF+fOJvCVAwAQAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBAA8cwL0i1pbudN7a02G3zTE4t+vGDPdb9nOQm45ePhwkP2SkIwMQoKuceQSErDrVC6fyG1LIEAAwJMRoF55QO/smWkqO6jUT0OA18cU4NGKyz2tEYSkVF1ursuwLQmpHG4hJLaD0jJAgro7rledpqlGLiFj4kO5CIvo+zKiIUAAwEMJ0DnJth7jPLFN5JPpRjdM47obNwnpKCPkeLNtSdiW+BZzocZFRNUvJ7q6JHKsflKDyZ1V7vQUfTdnqYQzDfJwdHSMImRHlspNiB1F27aVpxCyJpPbuJOtgAABAFMT4IFxNwhJ767opmZJ6jFWX6Ot2566lqOE1LbUDejIUC+f3kWlk3roUEVjJSF9KeTlLrpXrpQlL9N2cGYHsS7JiRPXzALc1aognbGcCG8QXSuZN4kAlyhdnBzFZONCotbI5YvpkVfz6eoECdnazq/KiHyoZCkpF3HqixRBgACAKQpQRMh5EU86v2GHoqKG3B2QaxsyA3ZWOZGLp8nSDqeYqkHF6VKSW0eCqhYF3KtLJ7XG2EIl9WHPdXKtjjZL70r57j2XxlpiXWa0iC0CrD5Hi7bRFWkzyejqH25tm1CA5bRncvEmEhNN5AXHSJmWbMoMFdN0z8owrbmIjAtkV5L1a+g7cM3ygAABAFMX4DgbJKz+aChdeFcrFIqeTDJwiRvOuFeRzgVtVICHq+my9BCp7SGkcNiPRLsQRcfNXS93Ge9xex9vFEzELed17SRmAVbSAJDsNJ5KudQ5QPrqaualVXlPJMDwY4QE8iX6lHxC3+bN7vvCyEZPd68srUWA0VkZZH1aJCFlfY4QIABgehFg+hgCJDWN9T015LS0tbVVWkt0/cbuU4Sc6jVe9uMEePoSLZLZSGov02UFH/URw43qy8H1nJdquw18Cr88epFYBNhxjrdYc2NbvDtRcCPG8ZcnEmAI9Zl3IF1JcueHl0naLhrveZMDxS5kd5Nw1hu3aJJdyHr1vqUuZ0MhQADAVAUoCxu/D5BGdrXD4swB67BrrJH29RGn6x2cADNp5EeaVPYCDNVxQyl19OVc5yC/i7Dsqa+oMEqNtExfKzd268TSl4tHSdJ5ukzun0iAe4oIaaMdkf5ZrnRrt4SE0goylCSZ9v9piwUB+vlxblyvzmtb60wgQADAVAVoSrGtp6WOyCrqoUMO9ayu7jzR3rwnb44lbGt63+UwklrNCbCo4i6JqLprFaB3JXE1nidB1bRTb2ddTkBAgHUp0Wq1d1u0tB+vaxlXc2lPoUtmi4Qk1QWToE5P4tsUSo7mkmuZ9wswsJ1IPFyJ2p0LK+VuEcTbxPf45R1wIVuV1j5AXoDyhEg/CBAAMPV5gErlPtqozDCZDiqVo7KajJ0th+lgcG+dsVRO+hpaq264sP0Vrd25nABJTW9FQzKxCvCiik70q2upOERnyxilHPOsS0oK1wRO5ANAUthsrOrmegpTja3GG7Rj0bhU3pJMjlfff3rR+/aqqKPdZXTySw4fZe7bs0FPJWcqjoyUjBQg8S4nECAAYBpXguiSRKTGeWtNjO7+SXi+wlIiTFZx5eckK8TWfPF9swTn5YRNaSK1q/lg0f4K82RnF9uc55FIRqdKWH4RasBEaADAQ18LLCoLxLXAAIBZKsBA3AwBAIC7wUCAYDr843denTNtXv3OP46sZd435s99Esz/RvTTcSLjnhCAACHApxaHb815QL7lYFfNN10lYvZJIJa4FjJPw4nYndA38bOCACHAZ4P35jww79lpZ/4TVM78wqfkRKwnBANCgBDgM8F35zwE37XUEu36ZIUz7yk5kftPCECAEOBTzLceRoDfstTyDckT9Y3kG0/Jidx/QgAChACfYl59GAG+aqll/hPudps/9okUhv5W8oRPCECAEOBTzJyHwlLL3Ccccc0d80QK//u//+23vk/2hAAECAE+WwL8weg4772HEKBv35knJcDQ/17+37/97b9PevyIXRAgBAgBQoBCv94v/ukXI433+c9H6PBfJhLguWqWzWiIYdnqZWa7SNWT2qK2geP6yDQ/c29aS/d4u2Xem1CAhf+2nAaA//6v/2revnmUq7bfkl3jbVlb1vtopGerEQKEACHAZ1OAP/ivn8z56S8mEOC3/msiAeZK/ViltJb1k0ZReVkFKPTEmfvjxLSfzmCfoE5Kkr6clGPZ5vOk14S8u3XSIn4n1n4PfrMxfkIB/tuK/+YF+Pt/F7arueKneyyVlF601EcFaO0ptOsyFI9OGFlk5AlJrDVCgBAgBPgsCvB7v/qv//zlnB/+jDrun+bM+enf/fqPVgF+l/n5e1zSP3z7B7/8r6/9w3sTNIFbD7MDNwfYw61sbrWxK48X4OHO+o477GBzRcNJlu08XlUR2DjcGGcuINiE811iZ8XFOPZed1VrJdsqNdbyOZdLe2jkpuup77iURauoaz1Hq7jR0HCUvTxc3zyhAMm/8f77/b8WjhBg3E1jxXH2aP1wFXdKdSfZZZ3X63tzuSJCFodwCOGUBuui2ObrNLA12IqkNhjjK3LMp3xJ1W08JNQIAUKAEOCzKcCf//OcfxFCvz//Yc5P/vbVH/78Z2YBfu1nP/r7v5nznV9/70e/+uMkESB76YSvMdfoe0LFduslR1s5AfrXJ2pP3GQPNcYl1SWyDdd9TwzfU1ctMxewCnCpsfLM5UvszRtsYq01AgwyxhylrerLPUV5dZfYEze194xRbEP/4NE6w6QRII3/qAD/4z9+L0Rp1Y0nTpyo7mHTj2uTruTy8Rp3SlXXll2pVHcc4oqYsyjCIcyn1HjK0NIibrtoK3JnOHHwhDTHnN/fGZE3fA8RIAQIAT67Avzh1/7407//Gjcr5ru/+sGcf/zaT3/6T/8459t//vPfz/n877jcV/9A50z/7D8nE2BmR2w1W32+42U/6YnS41J/KsBlnXxOL+0VvH6CbdjJvky111hrLmAVYKa0tLTayJ6uOt4nsQrwXEXwPekQ2/IyVeslVtpdWipdxDYksnHSO5MJ8Le8/37/H//7P4RhkOqB0tLSRtoETqktlZ7nddXJd1Quo6dzWpCXkMUJkD+E+ZROXkpv7rnXn2wrcop2TPpLc8z5/SdYtusoBPjYBBhd+OLc2QS+8scgwFe/9rPPP//ZD+fM+eN/0pd//Bu68d6c73z++bcsAvzuH6gAfz6ZAHX1J06yp0/UF+VIU5ctO6WzCZCzzaVDbMNd9uVOToDmAlYBekrpJhVd+o2WZqsAu+nDbKSn2e5UOohxia2/TIskcVWcmVSAkt/+m+C///sfkhFN4NpW5bKRAqSDICd5eZmzOAHyhzCf0r3e0tR4fcsdW5HAFpbNk+aY8/tpm7gDAkQEiAjwWW4C/+Jf5nzvDz+Y89O/ffUHP5jz+S9+OOeff2JpAn+H9v/N+fxvXv0BbRz/8v95dcJpMB3199h79R20N7CNvXPoDBVgcP159uR19tLFM0urMm0CNBewCnDIeI/dqWT1sawnDcmML3PpS68k0f62TvZkw6LTFZfYS/2SuEirAC8emlCA/y747//9v78XjxBg8yF2F7WcstvAXhrwzem+ZxOgOcsqQPMpias6/TN6hda6UERXdWnZgDTHnG8WIFcjBAgBQoDPpgB/+fNf/wN14Nc4vjfnj//wD7/6oVmAv/j2P/0NvWSOJv35R7SH8J8mGgRhb9CRAHHVDRohdVbVHeUHQc5VGTvz2LiBCm74wCZAoYBtEORcQ1XrLvblqs6Gw3RItULJxVvcHBjd8DVxW3N81iVaRZ1RZbAI0Lvl5kRN4EHBf//f/x41ClxZV3W54jw71F3BnZJxj10EaM6yCtB8Smw/LdEg6NZcJCbrcrp0qTnfLECuRggQAoQAn9VpMD+aM97Wj8aeIj3JRGgn6xwSJ0FJhnELCBQJrWjrZBkry9rYuF5uWDhIa1/eMOFEaMF///f3912nFmfbO8gwZtboUxpdJC5riE2tk4zORwQIAUKAuBTu0ZPUVWfsj5vmlSCG3/P+m5GrgUuNdS07cSUIBAgBQoCP5VrgQcn0rwVm6RyYf52pE4rDpXAQIATI4G4wzNN7N5in4IQABAgBMrgfIO4HCCBACPCp4/88jAD/j6WWeU/2RsyuT9sdoV1xR2gIEAJ83kPAn9hqKcQzQcY5IQABQoBPMT//wYP670d/y9iL54k9FW6kbp7YidhOyBf+gwAhQGZ2PRc4+sUn9FzgF6OfjhMZ94TAzAvQL2pt5U7vrTUZfhAgAGB2CVCvPKB39sw0lR1U6qcuFv9+xQS5JyLMK4UpO3WEHLvGY8vP8b4XRsjgJfOm+HjzBJW5CIvo+zKiIUAAwEMJ0DnJth7jPHUBXp9IgA0ZwjK3pae/rpYEdVC6h63Ze6oud3TryNJ6y3ZPyrhVyZ1V7vQUfTdnqYQzDfJwdHSMImRHlspNwqeItm0rpxWsyeQ27mQrIEAAwNQEeGDcjTFkNFU9WgTYf4OQoWEDv37ysiV3qF7LZ1kF2OM5flVLlC5OjmKycSFRa+TyxToytJpPVydIyNZ2flVG5EMlS0m5iFNfpAgCBABMUYAiQs6LeNL5DXvSuyu6aWiV1GOspu1Xv566lqOE1LbUDVAN9fLpXTTqSj10qKKxkpA+ruiAsZMmNXh21A/QZnAzLS+pd+Xqcq3wJ4bLdb2nqACraKv2xnEqwJ0tFZeOke7his5xBVhOeyYXbyIx0URecIyUacmmzFAxTfesDNOai8i4QHYlWb+GvgPXLA8IEAAwdQGOs0EUFTXk7oBc25AZsLPKiVw8TZZ2OMVUDSpOl5LcOhJUtSjgXl06qTXGFiqpD3uu06TU0BRjBmnoHJJEds8juR3xnb60lAAAIABJREFUixpr+cpKrxMycEIS1RJLyPGL50qraRNY2hxU1HiIzGvMnDeuAMOPERLoza31KfmEvs2b3feFkY2e7l5ZWosAo7MyyPq0SELK+hwhQADA9CLA9DEEGFZ/NJQuvKsVCkVPJhm4FES37lWkc7aiAjxczXntEKntoYMdw34k2kVIihgkDcsImWccIsE93Y2t57i6tDQADLpSqFA00ZEPZUtP500nKkA1IRl1hDRmjt8EDqE+8w6kK0nuhXxC2i4a73mTA8UuZHeTcNYbt2iSXch69b6lLmdDIUAAwFQFKAsbvw+wprG+p4acpncWb5XWEl2/sZs2YE/1Gi/7cQI8zQ3iZjaSWq5zryKX2+G0eVy34R596b4rb00lRFdVQzdu0AAwha/oIlnW60sTGsnSYdqpKJEaJhTgniJC2mjj2j+La0nvlpBQOviboSTJtP9PWywI0M+Pc+N6dV7bWmcCAQIApipAk90AbFrq6NzC2mFx5oB13kmskfb1EafrHZwAM2nkR5pU9gJ8uZG+sKGkoYxPCpJybdSL8XTGi3EpVWG90NI95M4FdPUuS6VONJSsmDgCDGwnEg9XonbnqpK7RRBvE9/jl3fAhWxVWvsAeQHKEyL9IEAAwNTnASqV+2ijMsNkOqhUjswp6qGDHfWsru480d68J2+OJWxret/lMJJazQmwqOIuiai6axWgdyVxqvCmSSmkoVs7L75VQTqPK8g1YxqN465zFXY3RSuOHyWHG6JI6OUB2gS+FFB487IgwKRUUtjkSs6ljZ7st2+vijraXUYnv+RwCaH79mzQU8mZiiMjJSMFSLzLCQQIAJjGlSC6JBGpcd5aE6MbndNk7Gw5TAeDe+uMpXLS19BadcOF7a9o7c7lBEhqeisakolVgBdVtJXbXWGkGm042mKkhYi60VjXQO3mZORnRjs1Vhib6RBubV2V8aKWjgKfqzMOiAUB1raSYDp80lV63/lJXEYnsPwi1ICJ0ACAh74WWFQWOM7EP1+zcoS2qyuvIoXYmi++f5agRFjIheCMHNOObFIHCMsgc5imKLS/4MPFetkHLoUDADwuAQbiZggAANwNBgIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQADA4xVgdOGLc2cT+MoBAIgAAQAQIAQIHiUvaX3o66rKlyYt+ZqvsMzxn7hcmlZYamtsaZPtMw2igoWlOGV6+01aPiZuJk4XQIAQ4FNLzubsbSGehFGIxCMzdhhGF12esJAJe2EFwyxynrhO94XC7juyfKxpo/bxXiMs3RKFpShZOET43slPuS1VWAaHT++tTlp+8/nxThdAgBDgs8qvf/otK3//61FSyH6NMKyb8n4BhieNVVecyGVqAhy9+2QCFIXxMZhozSMUGgQIAUKA4A9z3rP47705fxiZd3AR9+q62EUhivIKaVLQhqI+RBXoE6aSeZRzWXMTVjArrlKbmWIZt6g720SqRdQOgR4J5vakV96agsUvpYYkRDFMVhHdXeVCBSjsHrORkajU5SFKV8EoRfrwLTljC1CmWsIttqj28ZvW3bzS1ocwPoezPFYHMJ5lNOfIaqbMm2H83QqUeVRoPt5XVZ7LzeUMW0ISXjM3d/l3weTpU866c1qzlOfrDt4QvlK8r2AzVb7C2TGhjMapK0yOqjROgHmbNYtZ4XSPbA/Rs/j5QIAQ4LPN5z+xrf/k85F5HmnmFYWoPComgTZEy5XqtPCU5UUFsXyPmI/Gj8mRtTOMaohRZUTniXIMzCJNmdpTJnT0OSbcCXY8613krGGY/AiGMYiiqQCF3Re6M76iDWk5B/eu4owS6pip9g43jC3AJWephlzzvQUBWndz3FaZwwQWx+Qc3LwixpEW2fsa47yIkYQsUsc6UqElqu4MuZsYodzedknMK358BcK7YHaErFbHriuylefr1vvVyDakqcuVzHK3NTkxqkyG8SyO8XfTnGf8s2v8lOUruNON0eRolVvw84EAIcBnm+98Z+x1XntF1rUFDBOrogES7eRLdba1YZVHmMOLtjOF6wgVoLkJHEnFGL5QEGAsw5S505CLNqFtAhR25wW4lmHmhQRzRlniRss3JY4twLhtNITMTH7BIkDzbo5b6aGyaVZ0wdJVITpGIgvjBJhYTl24KJxm0YhSt245X265jJYLcBHCPOFd7Mimy/Xe1vJC3fQ9l1NpblIx6nwa8/q/snz5K7kMEyo7z2yk0eWq8BzudL29fJhVYvx8IEAI8LkV4PJ1wVYB0tDMv4D+vmIC20VNNgGmKxkvp+3iDGovqwDbaPr6I4IAabGVBxlGLvIdW4CcQrxiOaPsE5lMJpF+bAFqE5XMCk2EVYDm3bjqtdwxmfLzjHMgs3sjwwlQ6UlT0sKZuaJUk6ldFMeXY5yz29KI+a9EeBc7NtB102preaHul2hbmwpzgSPz2h6urCxOOETCeUZ0lTvH89zpBhXsTYzDrwcChACfXwEyG85bBUiVk1PArIjMyoz1UNoEON/jJUef9hTPRDsBciMEbmYBLphEgAFc2ZXcPusLlixZ4p02jgAL89m1GxirAM27cdU7yTirrV/CRLkzazbxAtRz3YEx4YyTaCVXp4Qvx/gEt3t48FN1LO9iR6QgQEt5oW65VYCxXty/AjJdEX+IvVSAeq6+pfxbDIjdJ8rEzwcChACfXwGmbljBzYXZNs8iwJx18xgmmRNgjLlI8QvJTExyuZ9ZgIrxBVhCxbfUIsAYswBp23J5yQK+Talkxh0Fpj2KSu8D6TYBmnfjql+xTk1fNEM0QVfwEi/AwINcHeHMChkXo/kIp8Gbb28gt7C8C4sALeVHCzAnhL59ar9VMnqIN/PPM+t3C/WZR4HzZKvw+4EAIcDnVoBh25KDlueoUq0RoFa0YHlSCFXVZudooYizRwozz0OznBfgS6/UrBpXgPvWSMI2mgXI7c4LcG+QYpFjNLdPXHYK0SYsEQRYzl3lqGDcTNyScAIMDilwsQnQvBsvttXl8xXtZ6n6Fu3hHEoFWLTuNRJcQoWW7OW6aomG8OVC89f6hKr4rknLu7AI0Fp+lADfTEgNc/VaTHs6I+cHJFMB1mgilkdlq7nTNXkpmCUq/HwgQAjw+RUgU7RZJnvFtMIqQKZsnWzLIuqZvO0aocRaEZ0L4sV13VEBMoEa5bgCjCsWhVSaBcjtzgswo0SW5SeEVDEJsnWLlgsCFHF4M278MocToM92OtZsFaB5N16ARJm9rpwbdF4qihEEyKQ4yrJeC+ezZAkR5nIp4QXZphV8BeZ3YRGgtfwoATLzvdZlK9+kYyxbZOsSuWkw3h6y8F386YZukRVc9cPPBwKEAJ95Af6VmT9/76f3ZbvELR+xvUJhWRmzNp/lExwqzC5zhdk2PgpbmmLF1E551G7M8pfuP5Qly75cgM9972J0+dHIzaf00qr76iDR+PFAgBDgs87nn//zHAvf+tvHe2w+3HpsuwEIEAIEoyPAOXO++6SOHb1kxWPcDUCAECC4T4B/wIcAIEAIcHby3T/iMwAQIAQIAIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBPj+oo+y3XI480FPeYuIY103TPdZotDX4NiBACBCMhZtMJvNIDn30FQcq7bectgU9SCX0SeUZqukeazQ7snymf2SnPPw2IEAI8PkXYCINkZQJMy3AB+SRCPCB2L0Xvw0IEAJ8PvjVrycUIKMWhTJZRQwjVrkwXjEbNavN4ZrC2VFVtpxhdPpwL9oSlaiCN4SvFO8r2Cwesc7klGdvSGMYz5Wmki25dL9K9/DMMiqlqD3Z5RF8TYWq6BE1m/fgf8+pHo6mVQwxOWqU0Yy11AqToyqNF2DU1RLnl/iTSSjzYdpMDLPUPYwp0odvybE7Foc5LU+fctb9PH03NLAlV4tiNtJa09aHWGqwHsIrb03B4pdSQxJoC9rH+6rKc7k177BmnWoTfjgQIAT4PPDqL/9uQgHu0Pgw+dRUBlE046jK83fT83nL17j5p6nKGNbDpH4tfwHjK9L71cg2pKnLlSPWFdneRVtl85lkzUp1e/hyJmZdpTrVQ8mEyVIkiSGEq0osUtjXbNmDw9NL65ewkilLCA6ObGOspTyLY/zdNFSABV65ue6LmeVua3JiVJmMNl/tszeWCXXMVHuHG6zH4rCk7QhZrY5dV8Rs2EF7ER19FrrTWrdV5lhqsB7CMeFOsONZ7yJnDcMkqu4MuZuseeLMhKIw/HAgQAjweeCN8Q3otjgmpqyEWsEqwJUM45/PW0udTx3gt5PZ6kU3Dq+h0qNRYjm1xCbViHVCg0Bm+yYmeR/9db7iz6yh1flsUDI56+ZR9a2wCtBWs2UP/gzKGGZeGBPqwjBraXPXXGr5KzSUDJVRAYporOYkClPnK2jGK8uZxMjKch9miRvdtSnReiwOS9qObHrM9d7MShr6OXsyvAC3cm/HXIPlRBxjGabMnTs5sU82jRx162x5aAJDgBDgLDCgW/h2lcibsRNgDMNEiwxcXvoeocxiT/oSFU6lR1uiW6hKFjiOWGdCUzJTRelMMvUhsyGFKUmiy3Yl86a7o2ewMADBC9BWs2UPjoWyjS8E0KX/SpNGxFhKaUVUiEwCFWAIV6jA/zXuZIgsjlnh/kocw+wTmUwmkd56LA5L2o4NdMO0mpHky300OkGAtJi1BsuJcIkrDzKMXOQ7V5RqMrWLbHkQIAQIAT4//PzVX/563CbwgWR7AS6wamp3uVBGWcb5KdvHVyS3E6BtXVuyxvsFToCeggBDuFkpnlRKZO3i/AO2JrCtZssePEGB7utiGJNH+xIlJ0ChVJGM228vFaAHVyZ8QSwXhi6X6ajnXvGlAV7BkiVLvNNsx2JsaTsiBQEyXhk5ZxlBgLRWaw2WE+GWZgE6iVZy+0qseRAgBAgBPkf885xfjStAfxltZZYspIMLIwWYU0AlJI5hvGlTktPHeAL05kTpaBPg5q2cjQQpidcFjyFAyx4WFm1e8Qo12Y4SqwBXydQM82Y+1wQu5BupOSG0XctpcaG7p5sP420e97A/liXNKsDzyZ6BNgFaaxhDgCtoYEjb0oxNgBvwm4EAIcDnx3/fnWAQZA01x741krCNIwVIslaHGcqdmbjsXSQiPH1cAaZrDG8mymwCrAzJkcdmK5kYTRzjJ5OMIUDLHhx7TWSF0pnxKFsRlGATIKOMnB+QzAlwXRPLHvRi3kxIDXP1WswEhPvLHWvoOaUQbcIS67E4LGlWAYZqiuNsArTUMJYAmWQv11VLNDY5Bq+LW46fDQQIAT7f/hMEGCFSM3HFopDKkQJkDJvXyfR0akrMVVkJDaXGE+BLG2XrysptAmRMBTI9bZYuN70SoqlhxhCgZQ9+qOXqK9lbQpmYENnZWDsBRm+RrUvkp8GkZ8u8WIaZ77UuW/kmo6QGSwuh5RNk6xYttx6Lx5xmFSCzxp2xCdBSw5gCJMpsWUKELW/5xvxK/G4gQAjw+fafPWFjhDzyVcIyeuJdXd4cub3CXN4nbCp7RPPdhD4Boy7YeGmVpbZ55pNZMSJfsWLEsezTxkM+QfZyxahtH/xwIEAI8Hng1e/iMwAQIAQ4m/npHI7v4YMAECAEOPv4xV9x/AofBIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoBPJWnaR1IqJk5YBtRsGjM/xx8fNYAAwUyhEslkJUrxdHYJe4E+Xdd94VSKTlqKPvmcJ8FthzVth8GWv8h58oMsWDpGon0lAAKEAGc3//Xtf/nJT/9qjAy3RIaZ67Z+OnXFiVwetQANIrsnqIcnTU+ASs8xEu0rARAgBDir+fOrc7733qtzfvI3YwqQeUHFMF5p60MYn8NZHqsDmE2LGcZPFcAw5REk1cPRtIr5/9s795g2zrzfT8Yhj+2sj7HNy80YG2yDuZn7xTGuwdwvL9gOF5FgQwDDGzhEkGyQziEJEUcK4a1OlKL06KSp0hM1jbStRNpu378qRVWSNvknVaS01Uqrqu1WWq12tbvaf9o/9p/zzM13GprbpvD9qJ3LM89lZhh/8nueGXtIwFc97+VL3Fpg9TnE2Kmzh+ro6tCcpUQuyKqRkMZBQrLdfVKq8Z1z9pBTvG6DKovOQRtyzlgGSglpC6r0HYIAu2iVmUSbaao/RSr1alOIa8++cpQTYLHJ3SpUYDX3jOuoKLWZKveklSj13nrVpJbM99v1BWJhMuRrvWq8LlUCIEAIEJD3BfW9f+3uj0kE2OZ1XyREtTDrJcVjTu/5uTZXv4eY1R1EOaHJy68pdPeSclW3wVzNdysdQ6zXT4wL6d4ZFSG2/hOFulAbt+H0eVqdupyk54dTjSZznXkjg29p0l1WVn+ONqQfsuX6CMkbc9pyLbwAtU62NtU6P1M1OuL0BEYaXURuWjccmmggOZZJQ55aGEk0L3TZzoaIJ3fQ69R3kwJ20DY01khKc1sCjFiYHLcPGBonAkIlAAKEAAH58dojYeH2w78kGwNkucBMdYzGWP0NVHAjVdbxAFnNaScdqyR3kpD9laQil+ZdborqAtN+ZwYrIzNmQvqq+djQZbcy4y2jpP1CONWo47qoOXyxclpqlIaaql6qzWHGs3GQpqmFLnANy5C6kTVCLg4KvddjISshR4dITj3dq2q+I23tv0XHH/MchmEtrWDDU8DWUilOCV1gqfDxfuriKTO6wBAgBAhEPnwgdX3/+sAaPwjXUlO6qfsgi6iaOQ9RSZHQdVJy/aZJpic5ZpKunjlE+8Jn2WAwyPqiBEj7pVY2QNgPuA2CxkyuTd9oJunxhlONtFdMLq4KTdl6gxaWCpB2iR2sX2jLHRHgKa6JaVZwV4k4rpdDQ0YydVHIk8UnvXOG+xCoXQUs1bZzQRCgVPj4NN0YHIAAIUAIEIj85Wtp6auUH5KNAVrtXUSVRkM6NcP5poKcKGnQEbd/hd5fLS02TjjJ1EhFRYW5I+4miJoK0MdtEO7DtnROzhbpHTQIk1KNnTT5ujAaFzStV+g4AabxAgzwba1EBNjIcmUqrLy7dJNRN0FyeQG6+AJ0mDGfTjzqugJWExGgVPh4PQQIAUKAIJovH0lL36f8I5kAHf0dvJfaJgx0Ytkk/oXu4yTYaPcIFpojZh2JugusjQhw6jQnUGFDa0uogEwfmifhVGM7nWfyd3LbNmj3+vh4WIB9atrWzeGIAG0Wq1ComoaITbQrTAK10QL0TFDN9nWsee20l0v1GRFgkIQLRwToxN8dAoQAAeVv10j4bsj3cdtWM/3+W7r+It5LZCCUql2/SofT9CYluWWaoSFakGnTZRJXfytT467gi6xtnOgLC/CEpdbT0G/gN8jG6RBft4nmklKN9i6mS90gdJAn20rdEQESXX1qUUuUAG8u5lRW6miTc5kOUtp/+mah/Wi0AEnmtEK7vmi96W6vzM4vIWEBFq/IrVLhsAC5SgAECAECqj0p7vv9NZJwE4Rlq3MDgpcIo+ufCHH3XNsXCdFM0BE8wwcb/fPl1DRu9USOEBCSYosuLEBiNqmrT4mVLdKAr4EODIZTjRdD6vEK8UsfdvXVxigBOubVE01zEQESRWiCHaRNDS1a6NPNbnU/fdYlWoB9JSNqI723m5o/0a+7GRFgaUjtkgqHBchXAiBACBBYL90VAr8/ptx5XF7PWnyKQxh6I9q2SIWe6AxF1mQVSana8FZrfMa1vrgyazeFeVtswcjO7RfmmrbY9LbowjGJAAKEAHc933967cN7P/7wxYMHd3AyAAQIAe62GPDO3ZSUB5d+uJPyV5wMAAFCgLsvCvyG+xbI31IQAwIIEALcrXwHAQIIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAX06yj76kO1ZzYpsZsy5qhIWOmnBa3+wa/rQQIAS4U7n9Ps/3iVty1Wq1qaV82zV16X9u22lVCUmVh579S3uP91i3lzFjoZRkDNEF/t3uAlpW9thiQ7iMIEAI8BfJFykCXycaMLeJBk8693MUoC4vIcnFZv1rT8jplZ8tQL4IgAAhwF8e177jph+mXEs0ICdAYmDLiTbTVH+KEKW+bLq6V3Z2ZI4qQUwb8p1a0Dd4e+wtbVSADR+MZ9IOo9X8gT7PQ/Mf7JkRJJKp0k96CKnzVecf5Qq1XjVeJ2S+364vIAFf9byX1C2mUiEeu7XA6nP4MjKfXV9MI7eAz75Cy+QtZY4YSMdqtc9Ar/N2kyrYJ834K19cFCoLr15ctPvkxDnD74J7klaX75yxDJQS4p+3u9/hix4tIaRQX0RIqPaw3nHBMqE/SoydOnuoLiJAsd283uD4/EFOecbq7os54nkSioRPyHVVBckfGhwpWWu3uxtwhUGAEOBLTMqHggC/+vzTXyUT4HGL1To/UzU64iQFrK/whHq6wxDSESntuH09EKzO9x6sPkS6RvIPHjRSnTTpb20agzR/foeLq8gzmGvr0E8SuSloeGc4jRYaMDROBEhpbkuAKVd1G8zVfjIwQ5yqLMcQ6/XzrYd0ho7qVlpm3XBoooG0VHfbHA3Ds3V540qSl19T6O6VZhziolSZuOq0eGt08yTdSDy5g16nvpsQlX7IlusjZGVd6dwo5GPOfg8xqzuIckIjY7WybnegkhgX0r0zqrAApXZbLL2G9WoPGd04blhX6cTzxBcJn5AR30ElUblvlamumgOZFlxhECAE+AsQ4Pt3Hl6KF2CJ0zk53k3qRmhUd3GQCi1AvRSkMZM+nHbcbiWM2klIZibpYmlklcFWWvtpDFY34SlgDUJFhuFKGmQtkWP5XLxEC/XTcb4ps9AFrsilictNRDveMdYc1QVW0jztmeRYiIZtR4dIy3madn6STqaaSC6d76+UZvy+CotSZeKqOd9K+mScAA3DWkJsGx6iosK0DTMeNY3NivimrOMBsprTTqM8QgUodoHzuCORSQKU2m05Sz9jGzayauYNHd0FDp+QERrpElUjIZNG6sbH958BBAgB/usFyBEvwOpFPUs/6qfYYDA4zVIB0s/4/DF670IVTjt+hmac4HqHLaTLzpUasSnY9mBwnXXx+Tk6zwjzEm7Ir6GaHJ+m8+CAIMCzXE0sjcmG1LroMUDGWbzOLgtlKC3c3EQNSSZ1JF09c4j2WcUZh7goVSaulo6sNNEYlArwHW4XGLWLqKisHayfZPaf62DE3bp+0yTTkxxzlABbqRg53wsClNptofYn061kZJPOu3UkME05yBeJOSFERQv0UmVr2AJcYhAgBPiyC1CQYJIu8GoLIY1sRUWFucJawGrCApTSjtdHCdDElapOy2B7uY1KPj8fIYXEex5cIGXrFwpJApwa4TJ3EFLFZkYJsK2+p7vRpBPKSAK0c0NqZjqiV1psnHCGZxzCYrgycUtR41m2mxNgIxd8etR1RJUmCNBatm4yCXY6UdKgI27/SlWUALmbIOqwAKV2+Z2gAlzoovN2HSlvpfj5IjEnhG8FAoQAIcBfugBt6lJis3BPkVhJtACltBgBsof5Tl+b2hXJz+EdobGWzMmri1NRRIA0ojKLPck+d6PdxglQK5SZ2E+tpyNNg3QlUCu4J7eCTnzFfIacueiZuGjWkehVjiF1HxWg10571AE1ExYg59gVoSb/QvdxEmy0ewQBTicKUGpXEqCOBqxFpkgXmBaJOSEQIAQIAe4IAZJBHbm5mFNZqZuJEaCUFiPAiWW5/DwNtVrys/sqLExYgEzPQKU/lElvN5xiaqs7IwIsXpFbXf2tTI27ghTnksZFhqxtnODv69awaZ5mu46U9p++WWg/Krin1e5lWocDZCXItOkypRmHuChVJq4G87WkQs9FgDfd7ZXZ+SVEEmD58Ki1XC8+7KI3Kckt0wzhBVg24fLEC1BqVxJggX01Z3EwLECuSMwJgQAhQAhwZwiwlt7JUIQm2MHyGAFKaTEC1Hf2q/Pl9DLU9avdtZEIkPjnJtQ+ByHOD9TjNOoKC7A0RINFp1s9keNxDZcSTw/t7xZbBLFMTqjnc+himlvdT59f4d1DzCa1m3Y/DR9s9M+XSzP+Pou4KFQmrZbPq0c+KOQESFLzJ/p1N8MCJK3VI/1B8Znr9kWqqolGQYCemeHZeAFK7UoCJNkX8wIXwgLki0SfEAgQAoQAf/ECjGLt5vbS2vaLStDGbdAIj+sRR3wB3jExX/6wesRNUh3a6O9xiBU4mOhZ9KJYmbjKRBrUxH3FpGirr4d4km2I2XEbd1Ok/kJckWQnBECAEOAvX4AgBttwyWRoLBsnAgKEACHAXYiiIu9EJU4DBAgBkh3xVTiOL67hbAAIEAIku/HHEChf4GwACBACJLvx57Def/8+zgWAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAB3INEvthBf8xGbdqHHNEB/djS/Y8qu1NMfQejrqcNZAxAgBLgjiH6xhfiaj5i04jGn9/xcG1EtzHrJdCf94RaTFWcNQIAQ4M4QYOTFFtJrPmLTaBToGKkiKvoLWaR3nv6sVBAnDUCAEOAOEWDkxRbSaz6i02r4H68PXefT6DvV9ltNtThpAAKEAHeIACO/6im95iMmTc395N5UBZ9c6yLEAAAgAElEQVRGTdhROIZzBiBACHDnCVB6zUdMGvdD0G2WTVGAp0smJ3HOAAQIAe48AUqv+YhJGwilatevrokCLN8YycA5AxAgBLgDBSi+5iM+bSJUQ0QBktwFnDIAAUKAO5OE13xwaWtRK1O9OEkAAoQAdyWF7eP7cRYABAgB7kqcZj9OAoAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgAAAAAECACBACBAAAAFCgAAACBACBABAgBAgeNY4XfEp7xQIc69ty0IeV9+2Ku+bXdtii1h51kUN6agh2Ue3VZ2hIXadloyHqxBAgBDgruHdd5Ol5rIc6eH141u99WPuerzc3Omk8lAbITmZkUQzK/y5Oln6ek25z77Q75MTomfV6rH1rK1b0LKyLZoVK89YKCXGdNKl39ahFuti143pCVm4CgEECAHuEr76bUrK779KIsCm2PXq5u0KkMPFZsULcJ2fq6kAZfpMLWGCqj6uEWtdbu7WLTxWgKLGnp0AAQQIAe4afniUcvfOnWspj37YQoBZ9R2EXNRV6tWmECFDc5YSGrjlO2csAzRQaguq9B2CABXuNtL2AVVYsJHkNtxaYPU51FHFJnerKEB9NdfpLbSM1JJj0x4uUMw0CI1sqrlXaoot1Pmq87nurDjnBOift7vfieyYuMoJ8FCu47DeIQmw4Ux/qDaqjxzqn6b7ntcbHJ8/SNdnjdXdk4IAh3xOvSmnjxdg5ixNWN0k5DTdfjGHcBVKxxfXMoAAIcCdxDdUf3+0UpH98W7Ko2+SR4CtpizZSJ0nMNLoIrb+E4W6UBtR6YdsuT4qlzGnLdfCC9BqKSReNY3y9JtE3+UYYr1+kmOZNOSphWE2c8kK57Vz3ZZa0tIe00jHRhvnQ74FuSloeGc4LTznBLiyrnRuFIZ3TFylAhxVpRIZqxUFWKluVTbZmXDs2G8OHFOnkhZLr2G92kOcE7OGdpMgwOPVU2XNV3N4Ac4s0YQxJxndOG5YV+n4CqXji2sZQIAQ4A7iHykP7liFRetfH6TEGjBX3U+hHdDBPF2e2EGdMdPbEtVeouolxDbMeDZoZFWuFrrAuovkQs4iOTzBUAGKXeB6WnF1uijA4/nUSsOpVIDGxmgBGkLnI13gYzQTuTAYnlMBetT0zkVRVniEUVzNyUxTUbdGBOidoIGkrC38aeD6zotHSctZurxhI4PddGemRQGq6Uabui9agKv02EhIFKB4fLEtAwgQAtxJfP/d5w+/+BW39IcvHn7+nTVWgO2FFOoT/4j+pqgn9oNgMMheJyonIQ7WX8NZjrgFAXbqSH7GoqyLDuiFBXiOpk9dFAWosbtI4zyhAswtlhq5yo5XsytFEQGWcK5tqA7PuQgws/9cBxPZMXE1R8VyveuIAG8aVXllUcdQ3trdznaSliBdnm4l49wI47ooQG7EsE8diBbgCO0Fk25RgMLxxbcMIEAIcEfx43fXrv3txx//9jmdbnUTRDvubpME6KuoqDBXEVUaL4iAmrPDiiDAVNOayrremtcUJUDuPkWuJECSs07cTk6AwfCtiNBUWZk/+jaLbpIu2Pqt0pwToLVs3WQqCO+YuJrDDtLRuigBEma0ZHg17Kua8UHzIU6AeYIA7dwTMHmiAD/gQsmJwrAAF5xkoYvO20UBCscX3zKAACHAncT7t8mPf7t2jdff7fe3EGBmez7XO6ymUdHUaU5ARBJEn9pAyM1h8S7w2KEW4mwJFYoC1CYI0DXSrPJwAhztT6UpDr0t9lYz14J5hi405ofn4l3gtpXi6H3jVnNa2miHNVqAXDw4USblMdM7KkQVEeDcMS4clbrAVM8Z7BpXUkd30rPhJDo65ldkihVgYssAAoQAdwxfPvj7PapAqr97f3/wZZwAgwrKfrJp0QaG6bPOc5kOcsJS62noN4QFoatPLWqRBJhpaiX7TRYPL8C1jRN98QIkc3ZqUipA68wZr6fgrNsaK0CuBVf/Kaa2ujM8pwIsHx61luvTSekhoWcrrtLK/fbGKAE6LS5SqFaSBqfQJbf4bzapIwKctXs1jf2iAId15f78Zf4myJLKwEyqnaTAvpqzOBgjQKkpAAFCgDszBLz04Mt7hOz98sGlb5I/CH1TT58DWc+3kqFFC9WYSV19KhwBEse8eqJJeg5wlOUekKFxFCdAUmzRJQjwqFrOC5A4dCNq9XxR3MOGfAvOD9TjXMwlzrkIsLV6pD/YRsyrQjZxlavcOWGICNAT3LBbTtA6L/DZ1mbUE5OhiABJcETtk7rA9b0b6txKXoBrU+xEEx0DJNkX8wIXYiNAsSkAAUKAO5H7nAJTfv/7lEvv8ys/DW+CothbJWtbfqPN6vmpujwuzVYtOMQVRySdb7SlKWY1WZOV3FRVJa5m3YyrPVzj8XrSFrm5u58fN7RxN0nqL8RVuVVTAAKEAH/xXPr6Qyt5/1OqP+uHX196yXe23rCtbBq757F5qAATsA2XTIbGsnFRQIAQ4G7hm0vig9B37qYk9IFfNi5uLxirPPH4PBnJxvUUFXknKnFNQIAQ4K4aBKRfhfvrXb4PDAAECAHuPgVCfwAChAB3K/+A/gAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAAAAAAQIAIEAIEAAAAUKAYNeSpVTEoszCSYEAIUCwO/ynyFbKo1FmK2BACBACBLsCZbY8nuxf47RAgBAg2A0olAkCVOJSgQAhQLA7BChPRLhUKp3KZ9FAQIaTDAFCgCABlb1fbbdPvjQC/OR/y6IEaB3LcT2LBkqO4i8NAUKAIAm1PS9TBPh/2qMjQJnl2TQAAUKAECDYUoCuObowGCgbmLTnFxLSljme7+U3Okrsi6P8UlPvlL3CqVJ1ENIQMuVYibVbtdAoTonTbfc5CBntGW+tP0z8M9W+cr5UX6ZphZZoasrP5VZXUwkZ2CQZoepB2rW9eNX9TpwAP/vvNVECrFGpx9JIxeLYZKQKcnFR1W2VKl4+tagqu2A3lpKylnW7rvSMvZs7mv76DKJZbFWt2gjJmLLn6I5KbQIIEAIEcQK0LtQQpcraPNyk7VzQkJyWomaVltt4el1rm7jJLeUtFmSMlGiHTMRvspUvN5G0eo2sXiZMmTNVRbpJ4qq2Fa1PyDzTp7XmQb7ydV154XgdyVuw8dVdrSHkfDMJdXh6u0mXMbtU740V4P+7HD0GaC01aTwd7hp/qDFcxdBijSJ0Sqr4jK6ytb8pK1hCmvvTiqaNqTX2GtLSub83RNbYSW1jPWlbrNA2Dh8V2wQQIAQIErrAecfI6SBpHqOL9V4yXkRjqzRxe9tCgBcgjcJCacSq1syuE1JXTzp6/DRZmHK0nicVOYRo1LJSN1218w/yWeSEFF8geaJ6RAG6G9voio5GcBfzYgRY9h91MTdB/CqajUagZavhKmgwRw7XSBWfaSB9rIZ460lziJBJWlsuv98yNRWgg/QNazMW6aoxXWwTQIAQIEgQYF0+OVtImrmwreSEllWpVGwnt7F00DTGGngB9hIyR3uUG2sldPMISzzd9p53xKnVvGhi9STYyzlP5uTLZ9Bl7TBnRh1fOEqAhaGREj9haTZWFyPA//uf8gQBGmmf3D8eroJbjVR8ppB4WEIKz5Dm89SIZr56Z72pmiVrGzTLuKzrPGfNdLFNAAFCgCDxJshi6qKVNHOh22qDdST8NYz8Rg9ZrIsVoBC1UTwN4zZh2rAoJ6MzpJPqLJWV1Z2RiltHaLd1qTtsLzd16WozXShvnyLLzSTuJkjgPzYTBehz0n0MhavwDdEm+6SKkwlQs1FLDvdLAjQY6SyULrYJIEAIECQKcDJEu5jN6i7ira4kPrN1rSWDj7ecxBYfAQYWZMSZR0bNxFO/KUy7Vjxt8zOkciF4anBExqgaSOpyH99h7bZW6hvC9louttYMN7f5UokznzSe7bOaW6MF6Ptf8kQBNq4ybXR8UapiNnTT46uQKk4mwMrhcmIelgR4czyNbKrTxTYBBAgBgkQBZrA0zmse1JlMNOCqXDVV51m55K6RsRZjnADJrGnBHSCH8/X6do8w1QxarubNEFJQvF5jkpFat8okPHiinTKZeknYXoUW0+BUM5m1GN21xJo5Pj7viBLgm//joyQCtLaPj+vawlWQ9fFqn0aqOGkXuHtkLCJA0rBgmvcdFdsEECAECBIp5DRIJZLFe49opDsGnv3JcvPaImttkel+D50oK6wkw84tOaxS1pvWJCWtwqxNE9MFfuN/JnwTRNiHvpgq2phkFcd+rGJW90e3CSBACBDE0TuWJgjwqfD4rq7aR8mTPghdl5FcgAAChADB86Sgkr8cK5+2nnJXG34MAUCAECAg+DksAAFCgIDgB1EBBAgBgq0M+Ou4n8T/NfwHAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAIAAIUAAAAQIAQIAIEAIEAAAAQIAAAQIAIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAIAAIUAAAAQIAQIAIEAIEAAAAQIAAAQIAIAAIUAAAAQIAQIAIEAIEAAAAUKAAAAIEAIEAECAECAAAAKEAAEAECAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgBAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAjwiQRI4acJk1SFQpNkssZNssKTuFVxkq1Q7Gd+rVA4hAm/GpcWmfybQqHdzuQ3CkVl/ESuUBQl3fDv3IbI5LBCUc4tiZPDsZPy6Mnh2Mm/hyeHmSJuKW5SqVD8JmpC0+TxafxEq1D823YmDoXi10kn+xWK7PjVLIUiNX6ylmSVn2hiJ8yWf/nHXghrsX/5taQXQtwf/aevgae5EPhrINmFkOwa2N6FcHirC+Fw0gsh2TWQ7EJ4NtdA5EKIrGZt9Ud/gmtglwmQAQCAXQoECACAAAEAAAIEAAAIEAAAIEAAAIAAAQAAAgQAAAgQAAAgQAAAgAABAAACBAAACBAAACBAAACAAAEAAAIEAIB/8Q+iAgCAQoEfRAUAAAgQAAAgQAAAgAABAAACBAAACHAXkCXOA8roVHlG7NZtVRFFjX87BR3b3Ulpd7ia923RRmHdiz1xGk307PlRk80Uan9ie3lAmL/ukv4cdbiqAQS4vU9xpt7YzC+1d0anV5i5qTJ3bLUmsVB2R/IqmMZwYs7s47W5PqbKD8Qler1JmxoqCWdYaJIyxbZxbGX08YcbX/32iTpmjdlUSY91cXGJkWbywSkDw5TqYoqoKGe2VeNP0n2MMbp+YvutZWEevMUwVcXMegEzU4MLG0CA26FCl5WhkiWm+8q46XIjcyo3cePm1BZVqH+OANd15YxzPC62KS5O2lREgL3d4UyxbZy/tY3Dja9++0SOOWs12P86U7VYVNnTIM1OdxrOMZrBWJ2rt1vjMxGgsofTcSsT0jCj7biwAQS4HUKFDFNylFvKG2WCxaHF00KQo+J6p1oL7d4JbisYvDpnYDLOM0zzeql7pN6RrIpBtt7GHDO683g5nWrJKhhcPOunn8d5/bqG6TjTUxKlO8dIEZ0eL2XS6hd95WKmdJNpgOFLaebTmNZwU5wAK3p6GplWk6mEz8QJMBgaa9cwjoHF0CYTtLt7xbaDBxYrhNwcTuPYvJzJPMgwZ0vF6rlDESgY1NfXMo5zi9Ot9ECajCsH51RBJns1yCVXtuj1x6lg6vXLMn5H5Be47q4jjbG/zuQdY5jOdWnWO1qjY3ormEQBCschHBMNU436YFb0WRR2szeb78vqztBQ2jWnNxZK50yrG8vNpALsNV49Lf0RqMQz5rRihcX6lWJBgO+sUzWz40Y2v6jcpMGVDSDAbVD9Ov0Q8d3d9hPMgE+TbeEdVcdHJwauAzfFx4L1o4xtTFNXzzBdurjYJVIF95F3hrRZy6epAE/MaJmQk2k9y5xakGupGceVzFuGSLFCozBXqlxMr07KxIVoQqk6d0GPMioCbJ7TVp6xMU3mSATYU57lq2AOBDUZC1pmsExqe2BZK+Xmgr4aZn2J8dFO+nQGX1I4FFHe6UzDKpOXo1Hq65ix00z34utFFlkBm87c0jNVjUx2dZZSlaFZyuN3pGZeFDgVoM9JY7hcaRaY840GzmoOx4hHbTabR8XjEI6p+czrWl1X1FkUdlPj48/LoUymdIlpbWbSw+csuK7JNlEBtmTJ9IXinlf2GHIPihUO1VdqcwUB5hyiwWm9ozlIR2QXlLiyAQS4Dez0I20ulgR4iiqhlh/M45MK6SeVyW3ggpNxOjlTFyvAjJA2tgpOgEEaqTh1TE5o3MEUsRUVx1jNKRqvHehlZs6fkvO50vn4zSsOj9H6mNctjJiJGkosxfRahqK7wAM9FRVjTTECbKIGWWYm1isqWBsnQLHtARrNibkpRV0VYy1RAhQPJW1gYMDFLzPMCu26BhuZMT9ztIUKMlDAJbtrGENnLyvr0iV2WKkAZ2iFtlVpxihdWVM1szNzRfxo3CHhbBw6dIhu5o5DPKYgH19HncXIblJspmKqbE1DYyYrnY5pumftVIA0Pa9C3HPGOx6MrjBdEGAJHVJ8PZfGokImACDAx3OGfsLOtUoCTGeY1SpuRXeQm1IvMYyeiybkJi5cMtRRaXWEBVjUGFcFJ8B1OjCXtszkGHtaGTk7OjramnWKDkkVLzGaW0ETH5MF+NF/7QjXt3XJO0q4vjYjZqKGEksxp0aaowXYMkNTC2ME2Ev7p/PM8DG6wc8JUGybOwwxN+2wXs1L12UyOhqpGXkBiodSc+vWrXJ+mWF6XJxfmDElc3SAFyCXbMzorD/Uxco6SpIKkAqTOZEpzbhIc5ZZdZid3GJzYfQYIHcc4jEJo5ZRZzG8mzz+03M+pkR3onFcOh3c4N86FSD9V6l7SdxzJmDJkyrkjrhDEGBLOnOIZevZ8WP8kQIAAT6e4nVGacpOEOCC0NdbPUp7bYIjNpmAKat8uIgJ6sK91/gqmBE5czRXwwz00i5wjaqQ6bEx/l7xw6w1a5mc6FGyEjrGlTGuzFYpmeMz0if+2Dojliow1l2VS01RAabPa5jWWl6AXCZOgHQMbcDMtC8xWU2HOQGKbXOHIeamhlVpGN06E+xm/MMZQvX8oQj70HOLCeiY9QuMtqcqSoDsQcZg0rTMMnVqmd+kZFqb+B1xHIwI8KAxSxPqkmY0WqYaWtUWOxNuggjHIRxTx2oWE2yOOovibu7jT3fzQUZezZhczOke6XRk0oh1jAowSHfQJu55VqhqxSZW2EqP2CcIkBuNPJbOhLhlSzmubAABbgPH2RW9EL1FCzAjJGx19YTcQm+qbnqa3uxkgpZQi47R5C46klXBHBijw1bunpYs7ibILb2sbnpF3yF9mPMWp3Kj7zdrfar6BSqM1sXpkFLKVNpTwvClNLldTG+L1BR3EyToNi6/zguQy8QJsH16cYZ2tM8a9fTWMBWg2DZ3GGJuLpi9GmpZZwIqo8+dIVbPHwpPYHp6LI0pmjcuUn1EBKhvMepvMTZV/YBJxqQvGutr+B0x2CNjgHS40B1kwjPtHP0n4MRgbmXUAbLcYzDicQhngp6DRZ02+izyu6kx8fsTMM4Z32HeMoVywgKUz/XUt1AB5hnHJqU/QnGQ8S5qxQrpI0hBQYBO2nsvqZHNc87twYUNIMDtoUzyGHPnAWkpO5wmfLS1jiSPPkeq4Bayoh9vLoq6LZD1elwz2oLoqqOqiCkVWaqMT9QINVZG2nck5n5d2FoeKRndXpGwJzF3LwrcQrKmPDoPLRmTq6g8eiZU8xPnWTimLG3cWeR3U6q3nL/LHFNLkfivjCPhTAkVaqVj10b+UWo047IGEOCTcy5tVx9+gfGXuNez0pPsWWcrcQkDCBAAACBAAAAECAAAECAAAECAAACAt8IBAPBWOESAAAAAAQIAAAQIAAAQIAAAQIAAAAABAgAABAgAABAgAABAgAAAAAECAAAECAAAL48Af3X/3l4AwPPh3n0H5PPyCtBx+8bH33rL9gEAnj1l3m8/vnEbCnxJBai5vffbqtpAjV8OAHj2+GsCtbXf7r2vSfzw7a/8TfZWv9SSLa9M8pKuO4+upTwJ1x7dgf+SCdBx+11vHS5SAJ4rdd537/1X/IevPDU1WylLXkCmzE7Njn+p8Y1LKU/OpRsQYGL8d+/GvhpcngA8Z2r23bgXGwNmZWc/rlB29lpMkU9TnoZPIcCElNvv7sO1CcALYN+7t2P6Xgrl48soFdFjh3dSno47EGAc3+/1Iv4D4IXEgN6930cN/ym2V0oRNRB46SkFeAkCjOPetxj/A+DFYPj2XuSjl6rcXiFlaqTMtacU4DUIMO4OyI0qXJYAvCCqboQ7tIezt1so9XD485rytECAsdz/uBBXJQAviNqP70sd4Oztl8rOggCfkwBvfxvAVQnACyLwrXQbpCh1+6VSiyDA5yTAe7gFAoD8xd0GkQYBf/NzIkA5BPicBLi3DN//AOBF4S/bK37yspXbL6XMhgCflwBjHgL8b7hCAXie7JMEqJBtv5BMAQFCgADsJAEmNd2mLWkpCBACBGCnC/CohWX1ByHAf50AjwiU4UIF4IULUDW1WTbl/rkCvHt3C9nd/QsE+LMjwKoj7+EqBeBfIMAM1imXl7GlP0uAv/3Dnj23k/9Ewu//BAE+mQA/eYuunHhVvjTbuNxygi6/d+GV1z4S8ry59IrvgCDJwMmGc8uzGW9cbg9EsnSevPy2KzzbfO3yuSGusnPLb3UuxVQEAAQYTSFbKE62L8DP//Tdw88/vA8BPlMBNr9Cb1G91ip/9ZULto+uDMllb7xd1nG5mc/z1smGg69d4Bfrjrxt++zKuSHbawfCWZp9m4UH3pZm712+7p09YpB3XPnI1vTKgZiKAIAAn1aAl/bQDvDnv32Y8vCvX/3jUUrK3z/88qt/0p9MuPbH3334dwjwCQXov2yTu6645K+epA8rXW+Xey8X0JjuDT6Pi27vOCkK0Es9SeO6z06Gs1xvl8n9GdKM/ieXn/xM3n6dztsPxFQEAAT41BHgH776kh8D/Mc3l/7y50sp3/35zm/fv52S8sPvfv+X7yHAJx0DvPCW/COqqVe5SO/gZflHR5aWls4dETJtzi75jogCpDp7Y5aLGMNZai+fm62VSzO567NPzEc+kl/mbm19ciC2IgAgwKcUYMrX/yR7vnqUcnfP1ykp/7yT8t0f6M+e7vn67h46LPg3CPBJBXjrpPztz6gAmzjhXZGdOtLZ2Xl9ln90c+mVps4DiQIMZ3GdeuPIJ3JxVrj8xvUTVIC6LprdfEAeXREAEGCE996TBPjeez/rLvCDS9/86e6jPX/+85/3fJPy3Ve0+7vn00d7HqakfAkBPqkAlcvey3T+6mvc/YvX5Js+Tlm8tvxXbsnlH72SIMCoLPKuI35xdp2r4JWP5AcOUCXSMcDoXABAgBEGBiQBDgxsX4Bff8k977Ln0dd7hJ8KFAR46WtuaPALCPCJH4NZWqbKkr96ZbbAttwpf/PkkstF72lwvPKWv/ZkogClLEvt79E7wNLsI1/dm7NXPpLXXW5fOvnGgXAu14Ha8P8AQIByuU5XyHKDR2yhTrd9AX665+8PP//rnz5PuffHz6/98y+SAB/c/8fdSxgDfHIBlh3hHl55denAkctNNGAzvHblyBsuPk/z5SMnTyUKUMrievvK5ZM2aVbw9pErb3HPvdR1fuJtPBDOVUvvBEv/AwAByuXdISV7Wi4/rZbVd/+MLvDff9yz5z697Xv3hz/t+edDSYApn/5uz+8QAT75V+E2L7/JCfATufS24II3pU0y1xZdWDGL/73o2Xt8YgPnudcaI7lkUf8DAAHKPxop1akyM1W69/qP/rxvgoi/k//wQUzyQ3wV7okFqOw8OSsXBPhs2LzS/dZrJ/H2EQABbiVAf31uqS4UKimdCinxXeB/rQD9Sx1Cd3fzWf3dDZ2ffObC5Q8gwC0fg8no6RkqdQ31GF34MQT8GgwAu+05QH+wmmWrg0r8Ggx+ERoA+Y7+RejkP4iqa5HjB1Ff6DtBqvBOEADkL+7V6OIn79dJfxI/8QkYOX4S/7kKEG+FA0D+4t4KJ70USZ74UiRzKGSxhEJmOV6KhPcCAyDfye8FTvJazK48ni45Xov5wgTouFGFqxKAF0TVjV8xeDH6SyRA+mZ0PJ0HwIvBEO4BM0z5tt+MnlrOQIDPS4COvXg1OgDyF3QLxBH56G33zcCRWyAMc+0p/XcNAozn/rv7cGUC8ALY9+79qE/emmJ7pRSaSJlLTynASxBgAvdu7EMMCMBzj//23bgX2/tSbCMGVCqigkbmw6cU4IcQYAL/tfddrwGXJwDPd/zP++69/4r96GlSHzsOmJqqiSnydCHgIwYCTERze++3VbWBGnwnBIDngb8mUFv17d7bmoTP3uHU1GzlFj+JJFNmp6Yejivww4On8N/DdyHApKnf37vx8bfesn0AgGdPmffbj2/c+z7ZRy+rSJat2IJsWc9GgiAAAABXSURBVFFWYok7j57sTsi1R3cYoNgi3XH/3l4AwPPh3v1fQT4vswABAAACBAAACBAAACBAAACAAAEAAAIEAAAIEAAAIEAAAIAAAQAAAgQAAAgQAPDS8v8BEzVP6YZV1c0AAAAASUVORK5CYII=",
    "media_type": "image/png"
  }
}
```

> TOOL

tool_use Read
id: toolu_01J3PzxgT2vHj6gMGVNq3AFg
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/chat-ui.js",
  "offset": 1,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01J3PzxgT2vHj6gMGVNq3AFg
```
     1→// ── Chat UI ─────────────────────────────────────────────────
     2→
     3→import { formatTokens, parseErrorMessage, sendRpc, updateCountdown } from "./helpers.js";
     4→import * as S from "./state.js";
     5→
     6→function clearChatEmptyState() {
     7→	if (!S.chatMsgBox) return;
     8→	var welcome = S.chatMsgBox.querySelector("#welcomeCard");
     9→	if (welcome) welcome.remove();
    10→	var noProviders = S.chatMsgBox.querySelector("#noProvidersCard");
    11→	if (noProviders) noProviders.remove();
    12→	S.chatMsgBox.classList.remove("chat-messages-empty");
    13→}
    14→
    15→// Scroll chat to bottom and keep it pinned until layout settles.
    16→// Uses a ResizeObserver to catch any late layout shifts (sidebar re-render,
    17→// font loading, async style recalc) and re-scrolls until stable.
    18→export function scrollChatToBottom() {
    19→	if (!S.chatMsgBox) return;
    20→	S.chatMsgBox.scrollTop = S.chatMsgBox.scrollHeight;
    21→	var box = S.chatMsgBox;
    22→	var observer = new ResizeObserver(() => {
    23→		box.scrollTop = box.scrollHeight;
    24→	});
    25→	observer.observe(box);
    26→	setTimeout(() => {
    27→		observer.disconnect();
    28→	}, 500);
    29→}
    30→
    31→export function chatAddMsg(cls, content, isHtml) {
    32→	if (!S.chatMsgBox) return null;
    33→	clearChatEmptyState();
    34→	var el = document.createElement("div");
    35→	el.className = `msg ${cls}`;
    36→	if (cls === "system") {
    37→		el.classList.add("system-notice");
    38→	}
    39→	if (isHtml) {
    40→		// Safe: content is produced by renderMarkdown which escapes via esc() first,
    41→		// then only adds our own formatting tags (pre, code, strong).
    42→		el.innerHTML = content;
    43→	} else {
    44→		el.textContent = content;
    45→	}
    46→	S.chatMsgBox.appendChild(el);
    47→	if (!S.chatBatchLoading) S.chatMsgBox.scrollTop = S.chatMsgBox.scrollHeight;
    48→	return el;
    49→}
    50→
```

> TOOL

tool_use Read
id: toolu_01Q4wfxxbLPAYMrprZpwrGjn
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/websocket.js",
  "offset": 50,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01Q4wfxxbLPAYMrprZpwrGjn
```
    50→import { connectWs, forceReconnect, subscribeEvents } from "./ws-connect.js";
    51→
    52→// ── Chat event handlers ──────────────────────────────────────
    53→
    54→var pendingToolCallEnds = new Map();
    55→var hasConnectedOnce = false;
    56→
    57→function clearChatEmptyState() {
    58→	if (!S.chatMsgBox) return;
    59→	var welcome = S.chatMsgBox.querySelector("#welcomeCard");
    60→	if (welcome) welcome.remove();
    61→	var noProviders = S.chatMsgBox.querySelector("#noProvidersCard");
    62→	if (noProviders) noProviders.remove();
    63→	S.chatMsgBox.classList.remove("chat-messages-empty");
    64→}
    65→
    66→function toolCallLogicalId(payload) {
    67→	if (!payload) return "";
    68→	if (payload.runId) return `${payload.runId}:${payload.toolCallId}`;
    69→	return String(payload.toolCallId || "");
    70→}
    71→
    72→function toolCallCardId(payload) {
    73→	if (payload?.runId) {
    74→		return `tool-${payload.runId}-${payload.toolCallId}`;
    75→	}
    76→	return `tool-${payload.toolCallId}`;
    77→}
    78→
    79→function toolCallEventKey(eventSession, payload) {
```

> TOOL

tool_use Grep
id: toolu_01CPvjAgtiUwKLwxes9CTes4
```json
{
  "pattern": "createSession|chat-messages-empty",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/helpers.js",
  "output_mode": "content",
  "-n": true,
  "-C": 3
}
```

> TOOL

tool_result
id: toolu_01CPvjAgtiUwKLwxes9CTes4
```
115- * session was created; individual tests can wait for store indexing
116- * if their assertions require it.
117- */
118:async function createSession(page) {
119-	const timeoutMs = 20_000;
120-	const previousActiveKey = await page.evaluate(() => {
121-		return window.__moltis_stores?.sessionStore?.activeSessionKey?.value || "";
--
174-	watchPageErrors,
175-	waitForWsConnected,
176-	navigateAndWait,
177:	createSession,
178-	openChatMoreModal,
179-	closeChatMoreModal,
180-};
```

> TOOL

tool_use Read
id: toolu_01XeWXfA6gpBbzR9TKYu5XZt
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/helpers.js",
  "offset": 115,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01XeWXfA6gpBbzR9TKYu5XZt
```
   115→ * session was created; individual tests can wait for store indexing
   116→ * if their assertions require it.
   117→ */
   118→async function createSession(page) {
   119→	const timeoutMs = 20_000;
   120→	const previousActiveKey = await page.evaluate(() => {
   121→		return window.__moltis_stores?.sessionStore?.activeSessionKey?.value || "";
   122→	});
   123→
   124→	await page.locator("#newSessionBtn").click();
   125→	await expect
   126→		.poll(
   127→			() =>
   128→				page.evaluate(() => {
   129→					return window.__moltis_stores?.sessionStore?.activeSessionKey?.value || "";
   130→				}),
   131→			{ timeout: timeoutMs },
   132→		)
   133→		.not.toBe(previousActiveKey);
   134→
   135→	await expect
   136→		.poll(
   137→			() =>
   138→				page.evaluate(() => {
   139→					const key = window.__moltis_stores?.sessionStore?.activeSessionKey?.value || "";
   140→					if (!key) return false;
   141→					return window.location.pathname === `/chats/${key.replace(/:/g, "/")}`;
   142→				}),
   143→			{ timeout: timeoutMs },
   144→		)
   145→		.toBe(true);
   146→
   147→	await expectPageContentMounted(page);
   148→}
   149→
   150→/**
   151→ * Open the chat "More controls" modal and wait for it to be visible.
   152→ */
   153→async function openChatMoreModal(page) {
   154→	const modal = page.locator("#chatMoreModal");
   155→	if (await modal.isVisible().catch(() => false)) return modal;
   156→	await expect(page.locator("#chatMoreBtn")).toBeVisible({ timeout: 10_000 });
   157→	await page.locator("#chatMoreBtn").click();
   158→	await expect(modal).toBeVisible({ timeout: 10_000 });
   159→	return modal;
   160→}
   161→
   162→/**
   163→ * Close the chat "More controls" modal by clicking the backdrop.
   164→ */
   165→async function closeChatMoreModal(page) {
   166→	const modal = page.locator("#chatMoreModal");
   167→	if (!(await modal.isVisible().catch(() => false))) return;
   168→	await modal.click({ position: { x: 8, y: 8 } });
   169→	await expect(modal).toBeHidden({ timeout: 10_000 });
   170→}
   171→
   172→module.exports = {
   173→	expectPageContentMounted,
   174→	watchPageErrors,
```

> TOOL

tool_use Grep
id: toolu_017BsT7Wttpt8XdaWyNcFtBL
```json
{
  "pattern": "modelStore|__moltis_stores",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js",
  "output_mode": "content",
  "-n": true,
  "head_limit": 20
}
```

> TOOL

tool_result
id: toolu_017BsT7Wttpt8XdaWyNcFtBL
```
crates/web/src/assets/js/app.js:24:import { modelStore } from "./stores/model-store.js";
crates/web/src/assets/js/app.js:31:window.__moltis_stores = { sessionStore, modelStore, projectStore };
crates/web/src/assets/js/app.js:331:	modelStore.setAll([]);
crates/web/src/assets/js/app.js:458:	modelStore.setAll(arr);
crates/web/src/assets/js/app.js:465:		modelStore.select(found.id);
crates/web/src/assets/js/app.js:468:		modelStore.select(arr[0].id);
crates/web/src/assets/js/app.js:470:		localStorage.setItem("moltis-model", modelStore.selectedModelId.value);
crates/web/src/assets/js/models.js:7:import { modelStore } from "./stores/model-store.js";
crates/web/src/assets/js/models.js:20:	return modelStore.fetch().then(() => {
crates/web/src/assets/js/models.js:22:		S.setModels(modelStore.models.value);
crates/web/src/assets/js/models.js:23:		S.setSelectedModelId(modelStore.selectedModelId.value);
crates/web/src/assets/js/models.js:24:		var model = modelStore.selectedModel.value;
crates/web/src/assets/js/models.js:37:	modelStore.select(m.id);
crates/web/src/assets/js/models.js:104:	var allModels = modelStore.models.value;
crates/web/src/assets/js/models.js:117:	var currentId = modelStore.selectedModelId.value;
crates/web/src/assets/js/sessions.js:36:import { modelStore } from "./stores/model-store.js";
crates/web/src/assets/js/sessions.js:605:		modelStore.select(entry.model);
crates/web/src/assets/js/sessions.js:609:		var found = modelStore.getById(entry.model);
crates/web/src/assets/js/sessions.js:1116:	if (modelStore.models.value.length === 0) {
crates/web/src/assets/js/sessions.js:1152:	var hasModels = modelStore.models.value.length > 0;

[Showing results with pagination = limit: 20, offset: 0]
```

> TOOL

tool_use Edit
id: toolu_01EUq5t2Egu2aKWrS36A5b1g
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "old_string": "async function waitForWelcomeOrNoProvidersCard(page) {\n\tawait page.waitForSelector(\"#welcomeCard, #noProvidersCard\", {\n\t\tstate: \"visible\",\n\t\ttimeout: 10_000,\n\t});\n\n\tconst noProvidersCard = page.locator(\"#noProvidersCard\");\n\tconst noProvidersVisible = await noProvidersCard.isVisible().catch(() => false);\n\tif (noProvidersVisible) {\n\t\tawait expect(noProvidersCard.getByRole(\"heading\", { name: \"No LLMs Connected\", exact: true })).toBeVisible();\n\t\tawait expect(noProvidersCard.getByRole(\"link\", { name: \"Go to LLMs\", exact: true })).toBeVisible();\n\t\treturn null;\n\t}\n\n\tconst welcomeCard = page.locator(\"#welcomeCard\");\n\tawait expect(welcomeCard).toBeVisible({ timeout: 10_000 });\n\treturn welcomeCard;\n}",
  "new_string": "async function waitForWelcomeOrNoProvidersCard(page) {\n\tawait page.waitForSelector(\"#welcomeCard, #noProvidersCard\", {\n\t\tstate: \"visible\",\n\t\ttimeout: 10_000,\n\t});\n\n\t// The two cards can swap during load: if models haven't arrived yet when the\n\t// session opens, #noProvidersCard is rendered first and then replaced with\n\t// #welcomeCard once models load (see refreshWelcomeCardIfNeeded in\n\t// sessions.js). Prefer the welcome card if it eventually appears, and only\n\t// treat the no-providers state as final when the welcome card never shows.\n\tconst welcomeCard = page.locator(\"#welcomeCard\");\n\ttry {\n\t\tawait expect(welcomeCard).toBeVisible({ timeout: 5_000 });\n\t\treturn welcomeCard;\n\t} catch {\n\t\t// Welcome card never materialized — we're in the no-providers state.\n\t}\n\n\tconst noProvidersCard = page.locator(\"#noProvidersCard\");\n\tawait expect(noProvidersCard).toBeVisible();\n\tawait expect(noProvidersCard.getByRole(\"heading\", { name: \"No LLMs Connected\", exact: true })).toBeVisible();\n\tawait expect(noProvidersCard.getByRole(\"link\", { name: \"Go to LLMs\", exact: true })).toBeVisible();\n\treturn null;\n}"
}
```

> TOOL

tool_result
id: toolu_01EUq5t2Egu2aKWrS36A5b1g
```
The file /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js has been updated successfully.
```

> AGENT

Now let me run biome on the edited file and re-run the failing test to confirm the fix.

> TOOL

tool_use Bash
id: toolu_01GbSKrfTePqRkW5cLyuSpZo
```json
{
  "command": "cd /Users/penso/tmp/molt/moltis/crates/web/ui && biome check --write e2e/specs/agents.spec.js 2>&1 | tail -20",
  "description": "Run biome on edited spec"
}
```

> TOOL

tool_result
id: toolu_01GbSKrfTePqRkW5cLyuSpZo
```
e2e/specs/agents.spec.js:19:54 lint/suspicious/noEmptyBlockStatements ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ! Unexpected empty block.
  
    17 │ 	for (let attempt = 0; attempt < 30; attempt++) {
    18 │ 		if (attempt > 0) {
  > 19 │ 			await waitForWsConnected(page, 5_000).catch(() => {});
       │ 			                                                  ^^
    20 │ 		}
    21 │ 		lastResponse = await page
  
  i Empty blocks are usually the result of an incomplete refactoring. Remove the empty block or add a comment inside it if it is intentional.
  

Checked 1 file in 40ms. No fixes applied.
Found 1 warning.
```

> TOOL

tool_use Bash
id: toolu_01RMMnCp4bEu3sECBrp8ERMZ
```json
{
  "command": "npx playwright test e2e/specs/agents.spec.js -g \"agent chips appear on welcome card when multiple agents exist\" 2>&1 | tail -40",
  "description": "Re-run the failing test",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01RMMnCp4bEu3sECBrp8ERMZ
```
npm warn Unknown user config "min-release-age". This will stop working in the next major version of npm.
[2m[WebServer] [22mMock OAuth server running on port 49320

Running 1 test using 1 worker

  ✓  1 [default] › e2e/specs/agents.spec.js:364:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist (1.9s)

  1 passed (12.6s)
```

> AGENT

Test passes. Let me also run the other tests using the same helper to make sure the fix doesn't break them.

> TOOL

tool_use Bash
id: toolu_01Up6gFF6Lex6MyXKHNpz23F
```json
{
  "command": "npx playwright test e2e/specs/agents.spec.js 2>&1 | tail -30",
  "description": "Run all agent tests",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01Up6gFF6Lex6MyXKHNpz23F
```
npm warn Unknown user config "min-release-age". This will stop working in the next major version of npm.
[2m[WebServer] [22mMock OAuth server running on port 49475

Running 12 tests using 1 worker

  ✓   1 [default] › e2e/specs/agents.spec.js:80:2 › Agents settings page › settings/agents loads and shows heading (620ms)
  ✓   2 [default] › e2e/specs/agents.spec.js:90:2 › Agents settings page › main agent card is shown with Default badge (655ms)
  ✓   3 [default] › e2e/specs/agents.spec.js:105:2 › Agents settings page › New Agent button opens create form (671ms)
  ✓   4 [default] › e2e/specs/agents.spec.js:123:2 › Agents settings page › create form Cancel button returns to list (583ms)
  ✓   5 [default] › e2e/specs/agents.spec.js:139:2 › Agents settings page › create, edit, and delete an agent (1.0s)
  ✓   6 [default] › e2e/specs/agents.spec.js:184:2 › Agents settings page › session header agent selector switches session agent and shows sidebar indicator (1.8s)
  ✓   7 [default] › e2e/specs/agents.spec.js:244:2 › Agents settings page › create form validates required fields (648ms)
  ✓   8 [default] › e2e/specs/agents.spec.js:263:2 › Agents settings page › Identity Settings button on main agent navigates to identity page (624ms)
  ✓   9 [default] › e2e/specs/agents.spec.js:276:2 › Agents settings page › shows workspace prompt truncation warning when AGENTS.md exceeds the cap (931ms)
  ✓  10 [default] › e2e/specs/agents.spec.js:313:2 › Welcome card agent picker › welcome card shows main agent chip and hatch button with one agent (521ms)
  ✓  11 [default] › e2e/specs/agents.spec.js:338:2 › Welcome card agent picker › hatch button navigates to agents page with create form open (717ms)
  ✓  12 [default] › e2e/specs/agents.spec.js:364:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist (1.6s)

  12 passed (20.9s)
```

> AGENT

All 12 agent tests pass. 

**Root cause:** Race condition in the `waitForWelcomeOrNoProvidersCard` helper. When a new session opens before models have finished loading, `showWelcomeCard` in `sessions.js:1116` renders `#noProvidersCard` first, then `refreshWelcomeCardIfNeeded` swaps it for `#welcomeCard` once models arrive. The old helper grabbed `#noProvidersCard` during that brief window, then its heading assertion failed because the card had already been replaced.

**Fix** (`crates/web/ui/e2e/specs/agents.spec.js:44`): prefer `#welcomeCard` with a 5s auto-retry wait; only fall back to the no-providers branch if the welcome card never materializes. The screenshot from the failing run confirmed the final state was the welcome card with the "Welcome Test Agent" chip, so this matches the intended behavior.

> DEVELOPER

✓  243 …g Anthropic provider › continue without selecting a model still persists Anthropic credentials (571ms)


  1) [default] › e2e/specs/agents.spec.js:357:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist

    Error: expect(locator).toBeVisible() failed

    Locator: locator('#noProvidersCard').getByRole('heading', { name: 'No LLMs Connected', exact: true })
    Expected: visible
    Timeout: 10000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 10000ms
      - waiting for locator('#noProvidersCard').getByRole('heading', { name: 'No LLMs Connected', exact: true })


      51 |      const noProvidersVisible = await noProvidersCard.isVisible().catch(() => false);
      52 |      if (noProvidersVisible) {
    > 53 |              await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
         |                                                                                                             ^
      54 |              await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
      55 |              return null;
      56 |      }
        at waitForWelcomeOrNoProvidersCard (/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js:53:98)
        at /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js:381:23

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: error-context (text/markdown) ───────────────────────────────────────────────────
    ## Error Context

    **Test**: agent chips appear on welcome card when multiple agents exist
    **Status**: failed

    ### Page 1: e2e-bot
    - **URL**: http://127.0.0.1:62544/chats/session/f45b2df3-3a06-45ef-81b1-24dde4cd127f

    ```
    e2e-bot
    391MB · 17GB free / 68GB
    Settings
    Changelog
    Report issue
    +
    Sessions
    Cron...
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/trace.zip
    Usage:

        npx playwright show-trace test-results/agents-Welcome-card-agent--13092--when-multiple-agents-exist-default/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────

  1 failed
    [default] › e2e/specs/agents.spec.js:357:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist
  4 skipped
  23 did not run
  238 passed (2.9m)
[local/e2e] failed in 175s
~/t/m/moltis main [!] ❯

> TOOL

tool_use Bash
id: toolu_01LMR5Ro9e7K1sYhGpmkTP4w
```json
{
  "command": "cd /Users/penso/tmp/molt/moltis && git status && git diff crates/web/ui/e2e/specs/agents.spec.js | head -50",
  "description": "Check current file state"
}
```

> TOOL

tool_result
id: toolu_01LMR5Ro9e7K1sYhGpmkTP4w
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   crates/web/ui/e2e/specs/agents.spec.js

no changes added to commit (use "git add" and/or "git commit -a")
diff --git a/crates/web/ui/e2e/specs/agents.spec.js b/crates/web/ui/e2e/specs/agents.spec.js
index 0fb1f052..81e06402 100644
--- a/crates/web/ui/e2e/specs/agents.spec.js
+++ b/crates/web/ui/e2e/specs/agents.spec.js
@@ -47,17 +47,24 @@ async function waitForWelcomeOrNoProvidersCard(page) {
 		timeout: 10_000,
 	});
 
-	const noProvidersCard = page.locator("#noProvidersCard");
-	const noProvidersVisible = await noProvidersCard.isVisible().catch(() => false);
-	if (noProvidersVisible) {
-		await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
-		await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
-		return null;
+	// The two cards can swap during load: if models haven't arrived yet when the
+	// session opens, #noProvidersCard is rendered first and then replaced with
+	// #welcomeCard once models load (see refreshWelcomeCardIfNeeded in
+	// sessions.js). Prefer the welcome card if it eventually appears, and only
+	// treat the no-providers state as final when the welcome card never shows.
+	const welcomeCard = page.locator("#welcomeCard");
+	try {
+		await expect(welcomeCard).toBeVisible({ timeout: 5_000 });
+		return welcomeCard;
+	} catch {
+		// Welcome card never materialized — we're in the no-providers state.
 	}
 
-	const welcomeCard = page.locator("#welcomeCard");
-	await expect(welcomeCard).toBeVisible({ timeout: 10_000 });
-	return welcomeCard;
+	const noProvidersCard = page.locator("#noProvidersCard");
+	await expect(noProvidersCard).toBeVisible();
+	await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
+	await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
+	return null;
 }
 
 async function deleteAgentByName(page, agentName) {
```

> TOOL

tool_use Read
id: toolu_01AQ7Lh9KmWnSqk7NPP5UhPK
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "offset": 44,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01AQ7Lh9KmWnSqk7NPP5UhPK
```
    44→async function waitForWelcomeOrNoProvidersCard(page) {
    45→	await page.waitForSelector("#welcomeCard, #noProvidersCard", {
    46→		state: "visible",
    47→		timeout: 10_000,
    48→	});
    49→
    50→	// The two cards can swap during load: if models haven't arrived yet when the
    51→	// session opens, #noProvidersCard is rendered first and then replaced with
    52→	// #welcomeCard once models load (see refreshWelcomeCardIfNeeded in
    53→	// sessions.js). Prefer the welcome card if it eventually appears, and only
    54→	// treat the no-providers state as final when the welcome card never shows.
    55→	const welcomeCard = page.locator("#welcomeCard");
    56→	try {
    57→		await expect(welcomeCard).toBeVisible({ timeout: 5_000 });
    58→		return welcomeCard;
    59→	} catch {
    60→		// Welcome card never materialized — we're in the no-providers state.
    61→	}
    62→
    63→	const noProvidersCard = page.locator("#noProvidersCard");
    64→	await expect(noProvidersCard).toBeVisible();
    65→	await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
    66→	await expect(noProvidersCard.getByRole("link", { name: "Go to LLMs", exact: true })).toBeVisible();
    67→	return null;
    68→}
```

> TOOL

tool_use Bash
id: toolu_01G5r6oJoDLJcVLupefnCPvV
```json
{
  "command": "grep -n \"stash\\|checkout\\|reset\\|branch\" /Users/penso/tmp/molt/moltis/scripts/local-validate.sh 2>/dev/null | head -20",
  "description": "Check local-validate for branch manipulation"
}
```

> TOOL

tool_result
id: toolu_01G5r6oJoDLJcVLupefnCPvV
```
53:# Detect local-only mode: no PR argument and no current PR on this branch.
59:    : # found a PR for the current branch
94:Current checkout does not match PR head commit.
141:Commit or stash all local changes (including untracked files) before running
```

> TOOL

tool_use Read
id: toolu_01EEVrbpnCkFx8fnJtKL8Wmm
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/scripts/local-validate.sh",
  "offset": 80,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01EEVrbpnCkFx8fnJtKL8Wmm
```
    80→
    81→  BASE_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
    82→  SHA="$(gh pr view "$PR_NUMBER" --repo "$BASE_REPO" --json headRefOid -q .headRefOid)"
    83→  HEAD_OWNER="$(gh pr view "$PR_NUMBER" --repo "$BASE_REPO" --json headRepositoryOwner -q .headRepositoryOwner.login)"
    84→  HEAD_REPO_NAME="$(gh pr view "$PR_NUMBER" --repo "$BASE_REPO" --json headRepository -q .headRepository.name)"
    85→
    86→  if [[ -n "$HEAD_OWNER" && -n "$HEAD_REPO_NAME" ]]; then
    87→    REPO="${HEAD_OWNER}/${HEAD_REPO_NAME}"
    88→  else
    89→    REPO="$BASE_REPO"
    90→  fi
    91→
    92→  if [[ "$(git rev-parse HEAD)" != "$SHA" ]]; then
    93→    cat >&2 <<EOF
    94→Current checkout does not match PR head commit.
    95→  local HEAD: $(git rev-parse --short HEAD)
    96→  PR head:    ${SHA:0:7}
    97→
    98→Check out the PR head commit before running local validation.
    99→EOF
   100→    exit 1
   101→  fi
   102→else
   103→  SHA="$(git rev-parse HEAD)"
   104→fi
   105→
   106→# Auto-sync Cargo.lock if stale (common after merging main).
   107→# Uses `cargo fetch` (without --locked) to resolve deps without compiling
   108→# or upgrading existing dependency versions.
   109→if ! cargo fetch --locked 2>/dev/null; then
   110→  echo "Cargo.lock is out of sync — running cargo fetch to update..."
   111→  if cargo fetch 2>/dev/null; then
   112→    if ! git diff --quiet -- Cargo.lock 2>/dev/null; then
   113→      git add Cargo.lock
   114→      git commit -m "chore: sync Cargo.lock"
   115→      SHA="$(git rev-parse HEAD)"
   116→      echo "Auto-committed Cargo.lock sync (new HEAD: ${SHA:0:7})"
   117→      if [[ "$LOCAL_ONLY" -eq 0 ]]; then
   118→        echo "Push this commit so CI sees the updated lockfile."
   119→      fi
   120→    else
   121→      echo "cargo fetch --locked failed but Cargo.lock is unchanged." >&2
   122→      echo "Run 'cargo fetch' manually to diagnose." >&2
   123→      exit 1
   124→    fi
   125→  else
   126→    echo "cargo fetch failed — check your network or Cargo.toml for errors." >&2
   127→    exit 1
   128→  fi
   129→fi
   130→
   131→# Reject dirty working trees in PR mode. Validating with uncommitted changes
   132→# publishes statuses for the wrong content. In local-only mode (no PR) we
   133→# allow a dirty tree so developers can lint/test without committing first.
   134→if [[ "$LOCAL_ONLY" -eq 0 ]]; then
   135→  if ! git diff --quiet --ignore-submodules -- || \
   136→     ! git diff --cached --quiet --ignore-submodules -- || \
   137→     [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
   138→    cat >&2 <<EOF
   139→Working tree is not clean.
   140→
   141→Commit or stash all local changes (including untracked files) before running
   142→local validation with a PR number.
   143→EOF
   144→    exit 1
   145→  fi
   146→fi
   147→
   148→detect_nightly_toolchain() {
   149→  if [[ -n "${LOCAL_VALIDATE_NIGHTLY_TOOLCHAIN:-}" ]]; then
   150→    printf '%s' "$LOCAL_VALIDATE_NIGHTLY_TOOLCHAIN"
   151→    return
   152→  fi
   153→
   154→  if [[ -f justfile ]]; then
   155→    local justfile_toolchain
   156→    justfile_toolchain="$(sed -nE 's/^nightly_toolchain := "([^"]+)"/\1/p' justfile | head -n1)"
   157→    if [[ -n "$justfile_toolchain" ]]; then
   158→      printf '%s' "$justfile_toolchain"
   159→      return
```

> TOOL

tool_use Bash
id: toolu_011q33gt1dd1YqyZajik5qx7
```json
{
  "command": "find /Users/penso/tmp/molt/moltis -name \"agents.spec.js\" 2>/dev/null",
  "description": "Find all agents.spec.js copies"
}
```

> TOOL

tool_result
id: toolu_011q33gt1dd1YqyZajik5qx7
```
/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js
/Users/penso/tmp/molt/moltis/.claude/worktrees/agent-a2e1a065/crates/web/ui/e2e/specs/agents.spec.js
```

> TOOL

tool_use Bash
id: toolu_01V9tJ6XHzBEmBwod478HYgR
```json
{
  "command": "sed -n '50,56p' /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "description": "Verify current line 50-56 of spec"
}
```

> TOOL

tool_result
id: toolu_01V9tJ6XHzBEmBwod478HYgR
```
	// The two cards can swap during load: if models haven't arrived yet when the
	// session opens, #noProvidersCard is rendered first and then replaced with
	// #welcomeCard once models load (see refreshWelcomeCardIfNeeded in
	// sessions.js). Prefer the welcome card if it eventually appears, and only
	// treat the no-providers state as final when the welcome card never shows.
	const welcomeCard = page.locator("#welcomeCard");
	try {
```

> TOOL

tool_use Bash
id: toolu_01B69QBBFCGn9ezYQtjJoPqG
```json
{
  "command": "grep -E \"local.*e2e|e2e.*local\" /Users/penso/tmp/molt/moltis/justfile 2>/dev/null | head -10",
  "description": "Find local e2e command in justfile"
}
```

> TOOL

tool_result
id: toolu_01B69QBBFCGn9ezYQtjJoPqG
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01KmN49mgY2AN591AZZhwNRR
```json
{
  "command": "grep -n \"local/e2e\\|local e2e\" /Users/penso/tmp/molt/moltis/scripts/*.sh /Users/penso/tmp/molt/moltis/justfile 2>/dev/null | head -10",
  "description": "Search for local/e2e label"
}
```

> TOOL

tool_result
id: toolu_01KmN49mgY2AN591AZZhwNRR
```
/Users/penso/tmp/molt/moltis/scripts/local-validate.sh:568:  run_check "local/e2e" "$e2e_cmd"
```

> TOOL

tool_use Read
id: toolu_01TGYk82ixRFpGiJcYKzZ7S7
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/scripts/local-validate.sh",
  "offset": 555,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01TGYk82ixRFpGiJcYKzZ7S7
```
   555→    run_check "local/ios-app" "$ios_app_cmd"
   556→  else
   557→    echo "Skipping iOS app checks (requires macOS host)."
   558→    set_status success "local/ios-app" "Skipped on non-macOS host"
   559→  fi
   560→else
   561→  echo "Skipping iOS app checks (LOCAL_VALIDATE_SKIP_IOS_APP=1)."
   562→  set_status success "local/ios-app" "Skipped via LOCAL_VALIDATE_SKIP_IOS_APP"
   563→fi
   564→
   565→# Gateway web UI e2e tests.
   566→if [[ "${LOCAL_VALIDATE_SKIP_E2E:-0}" != "1" ]]; then
   567→  cleanup_e2e_ports
   568→  run_check "local/e2e" "$e2e_cmd"
   569→else
   570→  echo "Skipping E2E checks (LOCAL_VALIDATE_SKIP_E2E=1)."
   571→fi
   572→
   573→# Coverage (optional — requires cargo-llvm-cov).
   574→# Skipped silently when the tool is not installed. Disable explicitly with
   575→# LOCAL_VALIDATE_SKIP_COVERAGE=1.
   576→if [[ "${LOCAL_VALIDATE_SKIP_COVERAGE:-0}" != "1" ]] && cargo llvm-cov --version >/dev/null 2>&1; then
   577→  run_check "local/coverage" "$coverage_cmd"
   578→  echo "Coverage report: target/llvm-cov/html/index.html"
   579→elif [[ "${LOCAL_VALIDATE_SKIP_COVERAGE:-0}" != "1" ]]; then
   580→  echo "Skipping coverage (cargo-llvm-cov not installed). Install with: cargo install cargo-llvm-cov"
   581→fi
   582→
   583→# Collect local/zizmor result at the end and fail if it found issues.
   584→zizmor_failed=0
```

> TOOL

tool_use Bash
id: toolu_01EFsKgsFyPMBXJe4VDzRhFy
```json
{
  "command": "grep -n \"e2e_cmd\\|playwright\" /Users/penso/tmp/molt/moltis/scripts/local-validate.sh | head -20",
  "description": "Find e2e_cmd definition"
}
```

> TOOL

tool_result
id: toolu_01EFsKgsFyPMBXJe4VDzRhFy
```
180:e2e_cmd="${LOCAL_VALIDATE_E2E_CMD:-cd crates/web/ui && if [ ! -d node_modules ]; then npm ci; fi && npm run e2e:install && npm run e2e}"
568:  run_check "local/e2e" "$e2e_cmd"
```

> TOOL

tool_use Bash
id: toolu_01VqaLCuXRGBCrY28EKTWyEx
```json
{
  "command": "wc -l /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js && md5 /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js 2>/dev/null || md5sum /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js",
  "description": "Check file size and hash"
}
```

> TOOL

tool_result
id: toolu_01VqaLCuXRGBCrY28EKTWyEx
```
     409 /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js
MD5 (/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/agents.spec.js) = 8d98b7958149bb8b112e5bde01b5f001
```

> AGENT

My fix is in place and the single test passes. Let me run the full agents suite one more time to be sure, and also check the video from the failed run to see if there's something beyond the race I already fixed.

> TOOL

tool_use Bash
id: toolu_01UUbkDwNYbxPMvf2eMiUz4T
```json
{
  "command": "cd /Users/penso/tmp/molt/moltis/crates/web/ui && npx playwright test e2e/specs/agents.spec.js 2>&1 | tail -20",
  "description": "Re-run full agents.spec.js",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01UUbkDwNYbxPMvf2eMiUz4T
```
npm warn Unknown user config "min-release-age". This will stop working in the next major version of npm.
[2m[WebServer] [22mMock OAuth server running on port 51004

Running 12 tests using 1 worker

  ✓   1 [default] › e2e/specs/agents.spec.js:80:2 › Agents settings page › settings/agents loads and shows heading (662ms)
  ✓   2 [default] › e2e/specs/agents.spec.js:90:2 › Agents settings page › main agent card is shown with Default badge (593ms)
  ✓   3 [default] › e2e/specs/agents.spec.js:105:2 › Agents settings page › New Agent button opens create form (649ms)
  ✓   4 [default] › e2e/specs/agents.spec.js:123:2 › Agents settings page › create form Cancel button returns to list (543ms)
  ✓   5 [default] › e2e/specs/agents.spec.js:139:2 › Agents settings page › create, edit, and delete an agent (993ms)
  ✓   6 [default] › e2e/specs/agents.spec.js:184:2 › Agents settings page › session header agent selector switches session agent and shows sidebar indicator (1.9s)
  ✓   7 [default] › e2e/specs/agents.spec.js:244:2 › Agents settings page › create form validates required fields (518ms)
  ✓   8 [default] › e2e/specs/agents.spec.js:263:2 › Agents settings page › Identity Settings button on main agent navigates to identity page (550ms)
  ✓   9 [default] › e2e/specs/agents.spec.js:276:2 › Agents settings page › shows workspace prompt truncation warning when AGENTS.md exceeds the cap (921ms)
  ✓  10 [default] › e2e/specs/agents.spec.js:313:2 › Welcome card agent picker › welcome card shows main agent chip and hatch button with one agent (488ms)
  ✓  11 [default] › e2e/specs/agents.spec.js:338:2 › Welcome card agent picker › hatch button navigates to agents page with create form open (565ms)
  ✓  12 [default] › e2e/specs/agents.spec.js:364:2 › Welcome card agent picker › agent chips appear on welcome card when multiple agents exist (1.5s)

  12 passed (20.6s)
```

> AGENT

All 12 pass, including the previously failing `agent chips appear on welcome card when multiple agents exist` test (now on line 364 — in your paste it was line 357, confirming the file in the failing run predates my fix).

The error output you just pasted references **line 53** for the heading assertion:

```
> 53 |              await expect(noProvidersCard.getByRole("heading", { name: "No LLMs Connected", exact: true })).toBeVisible();
```

But in the current file, line 53 is a comment — the assertion moved to line 65:

> TOOL

tool_use Bash
id: toolu_01DrrwUaTPeXMK8mu2nm8XbU
```json
{
  "command": "cd /Users/penso/tmp/molt/moltis && git diff --stat crates/web/ui/e2e/specs/agents.spec.js",
  "description": "Confirm fix staged"
}
```

> TOOL

tool_result
id: toolu_01DrrwUaTPeXMK8mu2nm8XbU
```
 crates/web/ui/e2e/specs/agents.spec.js | 25 ++++++++++++++++---------
 1 file changed, 16 insertions(+), 9 deletions(-)
```

> AGENT

The fix is uncommitted in the working tree. The pasted failure must be from a run that started before the fix landed (or scrolled-back terminal output) — the test title is now at `agents.spec.js:364`, not `:357`, and the failing assertion is at line `:65`, not `:53`. Running the full spec file now shows all 12 tests passing in 20.6s.

Please re-run `./scripts/local-validate.sh` (or `npm run e2e` in `crates/web/ui`) to confirm on your end. If you'd like me to commit and push the fix, say the word.

> DEVELOPER

✓  243 …g Anthropic provider › continue without selecting a model still persists Anthropic credentials (838ms)


  1) [default] › e2e/specs/node-selector.spec.js:45:2 › Node selector › node selector renders injected ssh target distinctly

    Error: expect(locator).toHaveText(expected) failed

    Locator:  locator('#nodeComboLabel')
    Expected: "SSH: deploy@box"
    Received: "Local"
    Timeout:  10000ms

    Call log:
      - Expect "toHaveText" with timeout 10000ms
      - waiting for locator('#nodeComboLabel')
        14 × locator resolved to <span id="nodeComboLabel">Local</span>
           - unexpected value "Local"


      73 |
      74 |              await expect(page.locator("#nodeCombo")).toBeVisible();
    > 75 |              await expect(page.locator("#nodeComboLabel")).toHaveText("SSH: deploy@box");
         |                                                            ^
      76 |              await page.locator("#nodeComboBtn").click();
      77 |              await expect(page.locator("#nodeDropdown")).toBeVisible();
      78 |              await expect(page.getByText("OpenSSH target", { exact: true })).toBeVisible();
        at /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/node-selector.spec.js:75:49

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: error-context (text/markdown) ───────────────────────────────────────────────────
    ## Error Context

    **Test**: node selector renders injected ssh target distinctly
    **Status**: failed

    ### Page 1: e2e-bot
    - **URL**: http://127.0.0.1:55109/chats/main

    ```
    e2e-bot
    399MB · 19GB free / 68GB
    Settings
    Changelog
    Report issue
    +
    Sessions
    Cron
    main
    03:32 PM
    session:828d9d8c-43e9-4f88-9569-21...
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/trace.zip
    Usage:

        npx playwright show-trace test-results/node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────

  2) [default] › e2e/specs/sessions.spec.js:623:2 › Session management › deleting unmodified fork skips confirmation dialog

    Error: expect(locator).toHaveCount(expected) failed

    Locator:  locator('.provider-modal-backdrop:not(.hidden)').filter({ hasText: 'Delete this session?' })
    Expected: 0
    Received: 1
    Timeout:  10000ms

    Call log:
      - Expect "toHaveCount" with timeout 10000ms
      - waiting for locator('.provider-modal-backdrop:not(.hidden)').filter({ hasText: 'Delete this session?' })
        14 × locator resolved to 1 element
           - unexpected value "1"


      655 |                     hasText: "Delete this session?",
      656 |             });
    > 657 |             await expect(confirmModal).toHaveCount(0);
          |                                        ^
      658 |
      659 |             // The session should be deleted immediately (no dialog appeared)
      660 |             // so we should navigate away from the current session URL.
        at /Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/sessions.spec.js:657:30

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: error-context (text/markdown) ───────────────────────────────────────────────────
    ## Error Context

    **Test**: deleting unmodified fork skips confirmation dialog
    **Status**: failed

    ### Page 1: e2e-bot
    - **URL**: http://127.0.0.1:55109/chats/session/ad471513-7ef1-41e1-a287-2deedb930765

    ```
    e2e-bot
    411MB · 20GB free / 68GB
    Settings
    Changelog
    Report issue
    +
    Sessions
    Cron
    2
    main
    03:...
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/trace.zip
    Usage:

        npx playwright show-trace test-results/sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────

  2 failed
    [default] › e2e/specs/node-selector.spec.js:45:2 › Node selector › node selector renders injected ssh target distinctly
    [default] › e2e/specs/sessions.spec.js:623:2 › Session management › deleting unmodified fork skips confirmation dialog
  4 skipped
  23 did not run
  237 passed (3.7m)
[local/e2e] failed in 226s
~/t/m/moltis main [!] ❯

> AGENT

My agents fix worked. Two new failures to tackle:
1. `node-selector.spec.js:45` — label shows "Local" instead of "SSH: deploy@box"
2. `sessions.spec.js:623` — confirmation dialog appears for unmodified fork delete

> TOOL

tool_use Read
id: toolu_01FoUwdTL6aibf67jstGT2FS
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/e2e/specs/node-selector.spec.js"
}
```

> TOOL

tool_result
id: toolu_01FoUwdTL6aibf67jstGT2FS
```
     1→const { expect, test } = require("../base-test");
     2→const { navigateAndWait, waitForWsConnected, watchPageErrors } = require("../helpers");
     3→
     4→test.describe("Node selector", () => {
     5→	test("node selector is hidden when no nodes connected", async ({ page }) => {
     6→		const pageErrors = watchPageErrors(page);
     7→		await navigateAndWait(page, "/chats/main");
     8→		await waitForWsConnected(page);
     9→
    10→		const nodeCombo = page.locator("#nodeCombo");
    11→		await expect(nodeCombo).toBeHidden();
    12→
    13→		expect(pageErrors).toEqual([]);
    14→	});
    15→
    16→	test("node selector exists in chat toolbar DOM", async ({ page }) => {
    17→		const pageErrors = watchPageErrors(page);
    18→		await navigateAndWait(page, "/chats/main");
    19→		await waitForWsConnected(page);
    20→
    21→		const nodeCombo = page.locator("#nodeCombo");
    22→		await expect(nodeCombo).toHaveCount(1);
    23→
    24→		const nodeComboBtn = page.locator("#nodeComboBtn");
    25→		await expect(nodeComboBtn).toHaveCount(1);
    26→
    27→		const nodeDropdown = page.locator("#nodeDropdown");
    28→		await expect(nodeDropdown).toHaveCount(1);
    29→		await expect(nodeDropdown).toBeHidden();
    30→
    31→		expect(pageErrors).toEqual([]);
    32→	});
    33→
    34→	test("node combo label shows Local by default", async ({ page }) => {
    35→		const pageErrors = watchPageErrors(page);
    36→		await navigateAndWait(page, "/chats/main");
    37→		await waitForWsConnected(page);
    38→
    39→		const label = page.locator("#nodeComboLabel");
    40→		await expect(label).toHaveText("Local");
    41→
    42→		expect(pageErrors).toEqual([]);
    43→	});
    44→
    45→	test("node selector renders injected ssh target distinctly", async ({ page }) => {
    46→		const pageErrors = watchPageErrors(page);
    47→		await navigateAndWait(page, "/chats/main");
    48→		await waitForWsConnected(page);
    49→
    50→		await page.evaluate(async () => {
    51→			const appScript = document.querySelector('script[type="module"][src*="js/app.js"]');
    52→			if (!appScript) throw new Error("app.js module not found");
    53→			const appUrl = new URL(appScript.src, window.location.origin);
    54→			const prefix = appUrl.href.slice(0, appUrl.href.length - "js/app.js".length);
    55→			const [{ setAll, select }, selector, state] = await Promise.all([
    56→				import(`${prefix}js/stores/node-store.js`),
    57→				import(`${prefix}js/nodes-selector.js`),
    58→				import(`${prefix}js/state.js`),
    59→			]);
    60→
    61→			setAll([
    62→				{
    63→					nodeId: "ssh:deploy@box",
    64→					displayName: "SSH: deploy@box",
    65→					platform: "ssh",
    66→				},
    67→			]);
    68→			select("ssh:deploy@box");
    69→			state.nodeCombo.classList.remove("hidden");
    70→			selector.restoreNodeSelection("ssh:deploy@box");
    71→			selector.renderNodeList();
    72→		});
    73→
    74→		await expect(page.locator("#nodeCombo")).toBeVisible();
    75→		await expect(page.locator("#nodeComboLabel")).toHaveText("SSH: deploy@box");
    76→		await page.locator("#nodeComboBtn").click();
    77→		await expect(page.locator("#nodeDropdown")).toBeVisible();
    78→		await expect(page.getByText("OpenSSH target", { exact: true })).toBeVisible();
    79→
    80→		expect(pageErrors).toEqual([]);
    81→	});
    82→});
    83→
```

> TOOL

tool_use Bash
id: toolu_01CnPJRsEfvfwn8gG3rB1JPP
```json
{
  "command": "find /Users/penso/tmp/molt/moltis/crates/web/ui/test-results -type d -newer /Users/penso/tmp/molt/moltis/crates/web/ui/test-results 2>/dev/null; ls /Users/penso/tmp/molt/moltis/crates/web/ui/test-results/",
  "description": "List test results"
}
```

> TOOL

tool_result
id: toolu_01CnPJRsEfvfwn8gG3rB1JPP
```
node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/
sessions-Session-managemen-5750c-k-skips-confirmation-dialog-default/
```

> TOOL

tool_use Read
id: toolu_01LmNMt5qTtDTH6u9pFVSYWS
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/ui/test-results/node-selector-Node-selecto-947f1-ected-ssh-target-distinctly-default/test-failed-1.png"
}
```

> TOOL

tool_result
id: toolu_01LmNMt5qTtDTH6u9pFVSYWS
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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rJslBrRa94x2AQGSxqdXPHw83bg8J/k0+r/gMWX+KGH2f/unCZBoWesVjxrWL+oNp0195vbcZ1K1ZCEBAgAei17w00v+t595wt4iCBAAAAECAAAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBAA8VgJcAQAATyhPXATIAACAAQgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQAQIAQIAIAAIUAAwJMiQEWYePaM12vum7qsVBAgAOC+C7DRsrenIm3WrM5j90l/UztLHFIaIEAAwH0W4OERBQlVhz7InqvYbnMkWSUPgQABAPdXgHua6INnIzkxVNFympDwuoohBYkZbh/pJtW5hFTX1e4j5ILN2d6LCqIarGjW3HsBdssj6ePBUnK0OOgdUh8st5kitrv3y21kECAAYDkFmNN2MYG7t1pT1kBx37hSfWsq6yUynGxVvYfsu0B9mB/a8gK5WBuT3+xB9vhp40buvQAb7PRPmo53N8bL610Lz5Ac/wbl7mgIEACwrJMgpU663puEVAwQcq3As82LS2ue5GIyKsDBckL2jpGLF+mI4NvE77JyObrAvukGAdYTUryZkEh/q5z1hAT4QYAAgGVeBhN5va1BJenr65McJl21XF83p0V3OZQTYHMOIaEV5GI1HSwMIrJB3cgydIFLHQ0CzCfkOV/6xDssJ4mQsEAIEACwnAIsbqUP126K1axh8UtLJzcqODTGCfBaBiEJwwYBErLucNu6ey5Azx1c2zl5vAAz99NZEX8FBAgAuA+TIIMKcqu3nlR1iqeyYo5knSAXT0VWVZLRFk6AuWOKyMF9BgHuyyAy9dS9DwFtylLJrZJ8XoD2JQMk04VAgACA5Rega5WuTneFEOux3vaLYu35iuYxGblZ0VyXwAlQPFRR4RRpEODp2ua+tGUYBFTsdPOeeFboApOCrJID1hAgAOC+jAFOndPy21Ru4oOcSOWX5hlnO6wU5mWV4uVZCrjG06xiBdYBAgBwLTAECACAACFAAAAECAECACBACBAAAAFCgAAACBACBABAgAAAAAECACBACBAA8ASy4gkDnzgAwMjKlSstniAgQAAABAgAABAgAAAChAABABAgBAgAgAAhQAAABAgBAgAgQAgQAAABQoAAAAgQAgQAQIAQIAAAAoQAAQCPsAA//eSzj//4xz9+9tGnC/vkj2/ff4e9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",
    "media_type": "image/png"
  }
}
```

> TOOL

tool_use Bash
id: toolu_01VjEtQktSRnors38NitT5pf
```json
{
  "command": "find /Users/penso/tmp/molt/moltis/crates/web/src/assets/js -name \"nodes-selector.js\" -o -name \"node-store.js\" 2>/dev/null",
  "description": "Find node selector files"
}
```

> TOOL

tool_result
id: toolu_01VjEtQktSRnors38NitT5pf
```
/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/stores/node-store.js
/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/nodes-selector.js
```

> TOOL

tool_use Read
id: toolu_019EPR7i4dvFa6bwEuG3biQs
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/nodes-selector.js"
}
```

> TOOL

tool_result
id: toolu_019EPR7i4dvFa6bwEuG3biQs
```
     1→// ── Node selector (chat toolbar dropdown) ───────────────────
     2→
     3→import { onEvent } from "./events.js";
     4→import { sendRpc } from "./helpers.js";
     5→import * as S from "./state.js";
     6→import { nodeStore } from "./stores/node-store.js";
     7→
     8→var nodeIdx = -1;
     9→var eventUnsubs = [];
    10→
    11→function isSshTargetNode(node) {
    12→	return node?.platform === "ssh" || String(node?.nodeId || "").startsWith("ssh:");
    13→}
    14→
    15→function nodeDisplayLabel(node) {
    16→	if (!node) return "Local";
    17→	if (node.displayName) return node.displayName;
    18→	if (isSshTargetNode(node)) {
    19→		var target = String(node.nodeId || "").replace(/^ssh:/, "");
    20→		return `SSH: ${target}`;
    21→	}
    22→	return node.nodeId;
    23→}
    24→
    25→function nodeMetaLabel(node) {
    26→	if (!node) return "";
    27→	return isSshTargetNode(node) ? "OpenSSH target" : node.platform;
    28→}
    29→
    30→function setSessionNode(sessionKey, nodeId) {
    31→	sendRpc("nodes.set_session", { session_key: sessionKey, node_id: nodeId || null });
    32→}
    33→
    34→function updateNodeComboLabel(node) {
    35→	if (S.nodeComboLabel) {
    36→		S.nodeComboLabel.textContent = nodeDisplayLabel(node);
    37→	}
    38→	if (S.nodeComboBtn) {
    39→		S.nodeComboBtn.title = node
    40→			? isSshTargetNode(node)
    41→				? `Execution target: ${nodeDisplayLabel(node)}`
    42→				: `Execution target: ${nodeDisplayLabel(node)}`
    43→			: "Execution target: Local";
    44→	}
    45→}
    46→
    47→export function fetchNodes() {
    48→	return nodeStore.fetch().then(() => {
    49→		var allNodes = nodeStore.nodes.value;
    50→		// Show or hide the node selector depending on whether nodes are connected.
    51→		if (S.nodeCombo) {
    52→			if (allNodes.length > 0) {
    53→				S.nodeCombo.classList.remove("hidden");
    54→			} else {
    55→				S.nodeCombo.classList.add("hidden");
    56→			}
    57→		}
    58→		var selected = nodeStore.selectedNode.value;
    59→		updateNodeComboLabel(selected);
    60→	});
    61→}
    62→
    63→export function selectNode(nodeId) {
    64→	nodeStore.select(nodeId);
    65→	var node = nodeId ? nodeStore.getById(nodeId) : null;
    66→	updateNodeComboLabel(node);
    67→	setSessionNode(S.activeSessionKey, nodeId);
    68→	closeNodeDropdown();
    69→}
    70→
    71→export function openNodeDropdown() {
    72→	if (!S.nodeDropdown) return;
    73→	S.nodeDropdown.classList.remove("hidden");
    74→	nodeIdx = -1;
    75→	renderNodeList();
    76→}
    77→
    78→export function closeNodeDropdown() {
    79→	if (!S.nodeDropdown) return;
    80→	S.nodeDropdown.classList.add("hidden");
    81→	nodeIdx = -1;
    82→}
    83→
    84→function buildNodeItem(node, currentId) {
    85→	var el = document.createElement("div");
    86→	el.className = "model-dropdown-item";
    87→	if (node && node.nodeId === currentId) el.classList.add("selected");
    88→	if (!(node || currentId)) {
    89→		// "Local" entry
    90→		el.classList.add("selected");
    91→	}
    92→
    93→	var label = document.createElement("span");
    94→	label.className = "model-item-label";
    95→	label.textContent = nodeDisplayLabel(node);
    96→	el.appendChild(label);
    97→
    98→	if (node) {
    99→		var meta = document.createElement("span");
   100→		meta.className = "model-item-meta";
   101→		var badge = document.createElement("span");
   102→		badge.className = "model-item-provider";
   103→		badge.textContent = nodeMetaLabel(node);
   104→		meta.appendChild(badge);
   105→		el.appendChild(meta);
   106→	}
   107→
   108→	el.addEventListener("click", () => selectNode(node ? node.nodeId : null));
   109→	return el;
   110→}
   111→
   112→export function renderNodeList() {
   113→	if (!S.nodeDropdownList) return;
   114→	S.nodeDropdownList.textContent = "";
   115→	var currentId = nodeStore.selectedNodeId.value;
   116→	var allNodes = nodeStore.nodes.value;
   117→
   118→	// "Local" as first item
   119→	S.nodeDropdownList.appendChild(buildNodeItem(null, currentId));
   120→
   121→	if (allNodes.length > 0) {
   122→		var divider = document.createElement("div");
   123→		divider.className = "model-dropdown-divider";
   124→		S.nodeDropdownList.appendChild(divider);
   125→	}
   126→
   127→	for (var n of allNodes) {
   128→		S.nodeDropdownList.appendChild(buildNodeItem(n, currentId));
   129→	}
   130→}
   131→
   132→function updateNodeActive() {
   133→	if (!S.nodeDropdownList) return;
   134→	var items = S.nodeDropdownList.querySelectorAll(".model-dropdown-item");
   135→	items.forEach((el, i) => {
   136→		el.classList.toggle("kb-active", i === nodeIdx);
   137→	});
   138→	if (nodeIdx >= 0 && items[nodeIdx]) {
   139→		items[nodeIdx].scrollIntoView({ block: "nearest" });
   140→	}
   141→}
   142→
   143→export function bindNodeComboEvents() {
   144→	if (!(S.nodeComboBtn && S.nodeDropdownList && S.nodeCombo)) return;
   145→
   146→	S.nodeComboBtn.addEventListener("click", () => {
   147→		if (S.nodeDropdown.classList.contains("hidden")) {
   148→			openNodeDropdown();
   149→		} else {
   150→			closeNodeDropdown();
   151→		}
   152→	});
   153→
   154→	S.nodeDropdown.addEventListener("keydown", (e) => {
   155→		var items = S.nodeDropdownList.querySelectorAll(".model-dropdown-item");
   156→		if (e.key === "ArrowDown") {
   157→			e.preventDefault();
   158→			nodeIdx = Math.min(nodeIdx + 1, items.length - 1);
   159→			updateNodeActive();
   160→		} else if (e.key === "ArrowUp") {
   161→			e.preventDefault();
   162→			nodeIdx = Math.max(nodeIdx - 1, 0);
   163→			updateNodeActive();
   164→		} else if (e.key === "Enter") {
   165→			e.preventDefault();
   166→			if (nodeIdx >= 0 && items[nodeIdx]) items[nodeIdx].click();
   167→		} else if (e.key === "Escape") {
   168→			closeNodeDropdown();
   169→			if (S.nodeComboBtn) S.nodeComboBtn.focus();
   170→		}
   171→	});
   172→
   173→	// Subscribe to presence and telemetry events for live updates.
   174→	eventUnsubs.push(onEvent("presence", () => fetchNodes()));
   175→	eventUnsubs.push(onEvent("node.telemetry", () => fetchNodes()));
   176→}
   177→
   178→export function unbindNodeEvents() {
   179→	for (var unsub of eventUnsubs) unsub();
   180→	eventUnsubs = [];
   181→}
   182→
   183→document.addEventListener("click", (e) => {
   184→	if (S.nodeCombo && !S.nodeCombo.contains(e.target)) {
   185→		closeNodeDropdown();
   186→	}
   187→});
   188→
   189→/** Restore node selection from session metadata (called on session switch). */
   190→export function restoreNodeSelection(nodeId) {
   191→	nodeStore.select(nodeId || null);
   192→	var node = nodeId ? nodeStore.getById(nodeId) : null;
   193→	updateNodeComboLabel(node);
   194→}
   195→
```

> TOOL

tool_use Read
id: toolu_01MakjzZjNKjzo9h4X8j1Pe5
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/stores/node-store.js"
}
```

> TOOL

tool_result
id: toolu_01MakjzZjNKjzo9h4X8j1Pe5
```
     1→// ── Node store (signal-based) ──────────────────────────────
     2→//
     3→// Single source of truth for connected remote nodes.
     4→
     5→import { computed, signal } from "@preact/signals";
     6→import { sendRpc } from "../helpers.js";
     7→
     8→// ── Signals ──────────────────────────────────────────────────
     9→export var nodes = signal([]);
    10→export var selectedNodeId = signal(null);
    11→
    12→export var selectedNode = computed(() => {
    13→	var id = selectedNodeId.value;
    14→	if (!id) return null;
    15→	return nodes.value.find((n) => n.nodeId === id) || null;
    16→});
    17→
    18→// ── Methods ──────────────────────────────────────────────────
    19→
    20→/** Replace the full node list from an RPC fetch. */
    21→export function setAll(arr) {
    22→	nodes.value = arr || [];
    23→}
    24→
    25→/** Fetch connected nodes from the server via RPC. */
    26→export function fetch() {
    27→	return sendRpc("node.list", {}).then((res) => {
    28→		if (!res?.ok) return;
    29→		setAll(res.payload || []);
    30→	});
    31→}
    32→
    33→/** Select a node by id. Pass null to clear (local execution). */
    34→export function select(id) {
    35→	selectedNodeId.value = id || null;
    36→}
    37→
    38→/** Look up a node by id. */
    39→export function getById(id) {
    40→	return nodes.value.find((n) => n.nodeId === id) || null;
    41→}
    42→
    43→export var nodeStore = { nodes, selectedNodeId, selectedNode, setAll, fetch, select, getById };
    44→
```

> TOOL

tool_use Grep
id: toolu_013RG6KUrNg36y5htb2TmTH2
```json
{
  "pattern": "fetchNodes|bindNodeComboEvents",
  "path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: toolu_013RG6KUrNg36y5htb2TmTH2
```
crates/web/src/assets/js/nodes-selector.js:47:export function fetchNodes() {
crates/web/src/assets/js/nodes-selector.js:143:export function bindNodeComboEvents() {
crates/web/src/assets/js/nodes-selector.js:174:	eventUnsubs.push(onEvent("presence", () => fetchNodes()));
crates/web/src/assets/js/nodes-selector.js:175:	eventUnsubs.push(onEvent("node.telemetry", () => fetchNodes()));
crates/web/src/assets/js/page-chat.js:18:import { bindNodeComboEvents, fetchNodes, unbindNodeEvents } from "./nodes-selector.js";
crates/web/src/assets/js/page-chat.js:1172:		bindNodeComboEvents();
crates/web/src/assets/js/page-chat.js:1173:		fetchNodes();
crates/web/src/assets/js/components/session-header.js:130:		var fetchNodes = () => {
crates/web/src/assets/js/components/session-header.js:136:		fetchNodes();
crates/web/src/assets/js/components/session-header.js:138:			if (!cancelled) fetchNodes();
```

> TOOL

tool_use Read
id: toolu_01WGSNqynqpPb37bs8bhWtZ3
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/components/session-header.js",
  "offset": 115,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01WGSNqynqpPb37bs8bhWtZ3
```
   115→				return;
   116→			}
   117→			var parsed = parseAgentsListPayload(res.payload);
   118→			setDefaultAgentId(parsed.defaultId);
   119→			setAgentOptions(parsed.agents);
   120→			setAgentOptionsLoaded(true);
   121→		});
   122→		return () => {
   123→			cancelled = true;
   124→		};
   125→	}, [currentKey]);
   126→
   127→	// Fetch connected nodes and subscribe to presence updates.
   128→	useEffect(() => {
   129→		var cancelled = false;
   130→		var fetchNodes = () => {
   131→			sendRpc("node.list", {}).then((res) => {
   132→				if (cancelled || !res?.ok) return;
   133→				setNodeOptions(Array.isArray(res.payload) ? res.payload : []);
   134→			});
   135→		};
   136→		fetchNodes();
   137→		var unsub = onEvent("presence", () => {
   138→			if (!cancelled) fetchNodes();
   139→		});
   140→		return () => {
   141→			cancelled = true;
   142→			unsub();
   143→		};
   144→	}, [currentKey]);
   145→
   146→	var startRename = useCallback(() => {
   147→		if (!canRename) return;
   148→		setRenaming(true);
   149→		requestAnimationFrame(() => {
   150→			if (inputRef.current) {
   151→				inputRef.current.value = fullName;
   152→				inputRef.current.focus();
   153→				inputRef.current.select();
   154→			}
   155→		});
   156→	}, [canRename, fullName]);
   157→
   158→	var commitRename = useCallback(() => {
   159→		var val = inputRef.current?.value.trim() || "";
   160→		setRenaming(false);
   161→		if (val && val !== fullName) {
   162→			sendRpc("sessions.patch", { key: currentKey, label: val }).then((res) => {
   163→				if (res?.ok) fetchSessions();
   164→			});
```

> TOOL

tool_use Read
id: toolu_01BqmQXYtbgUJFWYrM4zcknX
```json
{
  "file_path": "/Users/penso/tmp/molt/moltis/crates/web/src/assets/js/components/session-header.js",
  "offset": 1,
  "limit": 115
}
```

> TOOL

tool_result
id: toolu_01BqmQXYtbgUJFWYrM4zcknX
```
     1→// ── SessionHeader Preact component ───────────────────────────
     2→//
     3→// Replaces the imperative updateChatSessionHeader() with a reactive
     4→// Preact component reading sessionStore.activeSession.
     5→
     6→import { html } from "htm/preact";
     7→import { useCallback, useEffect, useRef, useState } from "preact/hooks";
     8→import { onEvent } from "../events.js";
     9→import * as gon from "../gon.js";
    10→import { parseAgentsListPayload, sendRpc } from "../helpers.js";
    11→import {
    12→	clearActiveSession,
    13→	fetchSessions,
    14→	setSessionActiveRunId,
    15→	setSessionReplying,
    16→	switchSession,
    17→} from "../sessions.js";
    18→import { sessionStore } from "../stores/session-store.js";
    19→import { ComboSelect, confirmDialog, shareLinkDialog, shareVisibilityDialog, showToast } from "../ui.js";
    20→
    21→function nextSessionKey(currentKey) {
    22→	var allSessions = sessionStore.sessions.value;
    23→	var s = allSessions.find((x) => x.key === currentKey);
    24→	if (s?.parentSessionKey) return s.parentSessionKey;
    25→	var idx = allSessions.findIndex((x) => x.key === currentKey);
    26→	if (idx >= 0 && idx + 1 < allSessions.length) return allSessions[idx + 1].key;
    27→	if (idx > 0) return allSessions[idx - 1].key;
    28→	return "main";
    29→}
    30→
    31→function buildShareUrl(payload) {
    32→	var url = `${window.location.origin}${payload.path}`;
    33→	if (payload.accessKey) {
    34→		url += `?k=${encodeURIComponent(payload.accessKey)}`;
    35→	}
    36→	return url;
    37→}
    38→
    39→function isSshTargetNode(node) {
    40→	return node?.platform === "ssh" || String(node?.nodeId || "").startsWith("ssh:");
    41→}
    42→
    43→function nodeOptionLabel(node) {
    44→	if (!node) return "Local";
    45→	if (node.displayName) return node.displayName;
    46→	if (isSshTargetNode(node)) {
    47→		var target = String(node.nodeId || "").replace(/^ssh:/, "");
    48→		return `SSH: ${target}`;
    49→	}
    50→	return node.nodeId;
    51→}
    52→
    53→async function copyShareUrl(url, visibility) {
    54→	try {
    55→		if (navigator.clipboard?.writeText) {
    56→			await navigator.clipboard.writeText(url);
    57→			showToast("Share link copied", "success");
    58→			return;
    59→		}
    60→	} catch (_err) {
    61→		// Clipboard APIs can fail on some browsers/permissions.
    62→	}
    63→	await shareLinkDialog(url, visibility);
    64→}
    65→
    66→export function SessionHeader({
    67→	showSelectors = true,
    68→	showName = true,
    69→	showShare = true,
    70→	showFork = true,
    71→	showStop = true,
    72→	showClear = true,
    73→	showDelete = true,
    74→	nameOwnLine = false,
    75→	showRenameButton = false,
    76→	actionButtonClass = "chat-session-btn",
    77→	onBeforeShare = null,
    78→	onBeforeDelete = null,
    79→} = {}) {
    80→	var session = sessionStore.activeSession.value;
    81→	var currentKey = sessionStore.activeSessionKey.value;
    82→	var gonAgentsPayload = parseAgentsListPayload(gon.get("agents"));
    83→	var initialAgentOptions = Array.isArray(gonAgentsPayload?.agents) ? gonAgentsPayload.agents : [];
    84→	var initialDefaultAgentId = typeof gonAgentsPayload?.defaultId === "string" ? gonAgentsPayload.defaultId : "main";
    85→
    86→	var [renaming, setRenaming] = useState(false);
    87→	var [clearing, setClearing] = useState(false);
    88→	var [stopping, setStopping] = useState(false);
    89→	var [switchingAgent, setSwitchingAgent] = useState(false);
    90→	var [agentOptions, setAgentOptions] = useState(initialAgentOptions);
    91→	var [defaultAgentId, setDefaultAgentId] = useState(initialDefaultAgentId);
    92→	var [agentOptionsLoaded, setAgentOptionsLoaded] = useState(initialAgentOptions.length > 0);
    93→	var [nodeOptions, setNodeOptions] = useState([]);
    94→	var [switchingNode, setSwitchingNode] = useState(false);
    95→	var inputRef = useRef(null);
    96→
    97→	var fullName = session ? session.label || session.key : currentKey;
    98→	var displayName = nameOwnLine ? fullName : fullName.length > 20 ? `${fullName.slice(0, 20)}\u2026` : fullName;
    99→	var replying = session?.replying.value;
   100→	var activeRunId = session?.activeRunId.value || null;
   101→
   102→	var isMain = currentKey === "main";
   103→	var isCron = currentKey.startsWith("cron:");
   104→	var canRename = !(isMain || isCron);
   105→	var canStop = !isCron && replying;
   106→	var currentAgentId = session?.agent_id || defaultAgentId || "main";
   107→	var currentNodeId = session?.node_id || "";
   108→
   109→	useEffect(() => {
   110→		var cancelled = false;
   111→		sendRpc("agents.list", {}).then((res) => {
   112→			if (cancelled) return;
   113→			if (!res?.ok) {
   114→				setAgentOptionsLoaded(true);
   115→				return;
```

> TOOL

tool_use Grep
id: toolu_01YJGAXgYNcfgzTcqA3TSoT1
```json
{
  "pattern": "nodeComboLabel|nodeCombo|nodeDropdown",
  "path": "/Users/penso/tmp/molt/moltis/crates/web",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01YJGAXgYNcfgzTcqA3TSoT1
```
Found 4 files
crates/web/src/assets/js/page-chat.js
crates/web/ui/e2e/specs/node-selector.spec.js
crates/web/src/assets/js/nodes-selector.js
crates/web/src/assets/js/state.js
```

> AGENT

You've hit your limit · resets 6pm (Europe/Lisbon)
