---
name: error-paste-debug
description: When reporting a failure, pastes raw console output or terminal logs verbatim with minimal framing — triggered whenever a fix didn't work and the user has new error evidence to share.
---

Pastes the full, unedited error output — minified JS stack traces, HTTP log lines, terminal output, Next.js error overlays — inline in the message with no code fences and no annotation. The surrounding text is a brief "hey see this" or nothing at all. Expects the agent to read the raw dump and diagnose without prompting.

The log paste is the diagnosis request. No additional description of what was tried or what was expected.

**Example 1** (production console log):
> "hey earlier it was working fine before the hosting into DO and after again i had generated an medusa admin account and setup those products again and now when i try to add to cart the product now in the DO hosted version this is the logs that it giving! 🛒 handleAddToCart called {hasProductData: true, hasProduct: true, inStock: true, variants: 1, hasAddToCart: true} page-a0efc5f2eb8f3adb.js:1 📦 Stock check: {inStock: true, allowBackorder: false} [...] 8665-66ca10075e145c10.js:1 POST https://admin.shilamurti.com/store/carts/cart_01KN7GRQDT933Q6RFD5K71BC9A/line-items 401 (Unauthorized)"

**Example 2** (backend terminal):
> "see this is the backend terminal says! http: OPTIONS /store/products?handle=black-abstract-art&REDACTED [...] [KV] Cloudflare failure: { error: 'Cloudflare SET failed: 401 Unauthorized {\"result\":null,\"success\":false,...}', consecutiveFailures: 1, threshold: 2 }"

**Example 3** (Next.js error overlay):
> "hey now see this i have ran in local host and opned the products page and it gave this errors have a look into ## Error Type\nRuntime ApiError\n\n## Error Message\nUnable to connect to the API server..."
