---
name: ios-ref-redirect
description: How malkoG requests new UI features — always references the iOS or web sibling project as the design spec, using a relative path
---

# iOS Reference Redirect

When malkoG wants a new screen, rendering change, or visual redesign, he always pairs the request with a pointer to the canonical design source — either the iOS app or the web app. He never describes the visual design in words; he just tells the agent where to look.

Pattern: `"For [feature], Could you [action]? [See/Reference] ../[sibling-repo]"`

The "Could you" opener is consistent. The relative path is always `../hackerspub-ios` or `../hackerspub/web-next`. The agent is expected to look at the actual code in those repos.

**Examples:**

> "For rendering mention, hashtag, link, and so all, Could you hightlight differently? Reference ../hackerspub/web-next"

> "For rendering article, Could you render article card differently, and create the article detail page? See ../hackerspub/web-next"

> "I want to make it as pretty as Hackers'Pub iOS client"

> "For satisfy 100% parity of iOS app, you can take a look using `git logs` / And then see .swift changes, and then apply corresponding or similar changes using .kt (kotlin)"

When the request is for a full-app redesign, he frames it as a mission in `/loop`:
> "Your mission is building android client for HackersPub. [...] At least, we need to satisfy 100% parity of iOS app. For iOS app, see ../hackerspub-ios"
