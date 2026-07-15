[DEVELOPER]: [23:27, 2026/5/8] Sergio Huainigg OE8CXC: erus schau mal beim qsl generator da kann ich mobile ned auf Download klicken [23:27, 2026/5/8] Sergio Huainigg OE8CXC: Kein Event wird getriggert

[AGENT]: Mobile download button not firing. Let me check the generator code.

[AGENT]: Found it. Line 806-821. Problem: `link.click()` on dynamically created `<a>` element — many mobile browsers block this. The link never gets appended to DOM, so mobile Safari/Chrome ignore the click.

[AGENT]: Fix: append link to DOM before clicking, then remove it. This is required for mobile browsers.

[AGENT]: **Problem:** Mobile browsers (Safari, Chrome) ignore `.click()` on `<a>` elements not in DOM. Link was created but never appended. **Fix:** Append link to `document.body` before clicking, remove after. Standard mobile download pattern. Sergio should be able to download on mobile now after deploy. Want me to commit and deploy?

[DEVELOPER]: yes

[AGENT]: Committed. Want me to push and deploy?

[DEVELOPER]: yes, push and deploy

[AGENT]: Remote has new commits. Pulling first.

[AGENT]: Pushed. Now deploying.

[AGENT]: Deployed. Site live at https://qsl.oeradio.at/ (HTTP 200). Deploy geht auf Synology NAS — Script pullt Code von GitHub, baut Docker Image direkt am NAS, startet Container neu. Sergio kann jetzt mobile Download testen.

[DEVELOPER]: check bitte mal auf achildrenmile@host-node-01, ob es nicht dort deployed ist

[AGENT]: Kein QSL Container oder Verzeichnis auf `host-node-01`. Deployment läuft nur auf Synology.

[DEVELOPER]: download funktioniert nicht am handy

[AGENT]: Problem wahrscheinlich: Mobile Safari blockiert `.click()` nach `await` — verliert den User-Gesture-Kontext. Auch sind Data-URLs bei einem 4837x3078 Canvas riesig, was auf Mobile Probleme macht. Besserer Ansatz: `canvas.toBlob()` mit `URL.createObjectURL()`, und den Blob-Link in neuem Tab öffnen als Fallback.

[AGENT]: Zwei Fixes: 1. **Kein `await` mehr** vor dem Download — Mobile Safari verliert User-Gesture nach async, blockiert dann den Click 2. **`toBlob()` + `createObjectURL()`** statt `toDataURL()` — viel kleiner im Speicher, funktioniert besser auf Mobile Commit und deploy?