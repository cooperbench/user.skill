[DEVELOPER]: Can you explain to me why when I build and release/publish to steam workshop the stationpedia ascended mod the changelog is still saying 0.8.0?

[DEVELOPER]: So something odd is happening. It appears the version taht got pushed to the build and publish is not the latest version? The verison i have in my hot-reload seems to have lots of bug fixes and things that aren't in the version 8.5 i puhsed to steam. When I press f6 it works great but when I load the mod from steam workshop in game it seems to be old code that is broken

[AGENT]: The user is saying that the version they have locally (hot-reload via F6) works great with bug fixes, but the version published to Steam Workshop seems to be an older, broken version. Let me investigate the build and packaging

[DEVELOPER]: Please figure out why there is a discrepancy. The bug I am experiencing in particular is around the search function in the stationpedia

[AGENT]: The user is experiencing a bug specifically with the search function in the Stationpedia when loading from Steam Workshop (Release/SLP mod) vs F6 hot-reload (Debug/ScriptEngine). Let me dig into the search-related code to understand how it works and what might differ between the two loading paths.

[DEVELOPER]: But when i look in the game menu at the downloaded mods it says it is running the 8.5 version. You're saying the dll is not any different?

[AGENT]: <think></think>

[AGENT]: The user is saying the game's mod menu shows version 0.8.5, but the behavior is broken/old. Let me think about this more carefully. The game mod menu reads the version from `About.xml`, not from the DLL itself. Let me check what About.xml is in the Workshop download folder vs what's in the Documents folder. The Workshop cache shows `About.xml` was dated Feb 19. Let me check if the About.xml in the workshop cache matches the one in Documents. Actually, looking back at my data: - Workshop folder has `About.xml` dated `2/19/2026 8:35:22 PM` - Documents folder has `About.xml` dated `2/5/2026 10:59:11 PM` So the Workshop version is newer, which makes sense since that's where the Feb 19 publish would have updated it. But both copies have `<Version>0.8.5</Version>`, so the game displays 0.8.5 regardless of which folder it's reading from. The real issue is that the DLL's actual compiled code might be from different builds entirely. The About.xml version stayed at 0.8.5, but the Workshop DLL from Feb 19 is an older build compared to what the user just compiled today—they have different hashes and different code despite being the same file size. So the version number hasn't changed, but the […]

[DEVELOPER]: I unsubscribed and ere subscribed but the bugs are still there

[AGENT]: <think></think>

[AGENT]: The user unsubscribed and resubscribed but the bugs are still there. This means the Workshop DLL on Steam's servers might actually be the old one, OR the game isn't loading from the Workshop folder. Let me check: 1. First, let's see if the Workshop cache got refreshed after resubscribe 2. Then check if maybe the game loads from a different path (like the local mods folder which also has a copy) 3. Or maybe there are TWO copies loading and they conflict Let me check the current state of the Workshop cache after the resubscribe.