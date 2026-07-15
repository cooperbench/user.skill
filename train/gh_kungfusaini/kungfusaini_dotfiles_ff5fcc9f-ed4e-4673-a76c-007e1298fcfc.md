> DEVELOPER

hey man so I pushe dto the project-writeups a new project called stleath ai startup. But how comes vulkan is not servingit (vulkan.sumeetsaini.com/projects) when the webhook delivery form the project0writeups repo went fi,e? Access-Control-Allow-Origin: *
Alt-Svc: h3=":443"; ma=86400
Cf-Cache-Status: DYNAMIC
Cf-Ray: a02500700ce7e670-IAD
Content-Length: 74
Content-Security-Policy: default-src 'self';base-uri 'self';font-src 'self' https: data:;form-action 'self';frame-ancestors 'self';img-src 'self' data:;object-src 'none';script-src 'self';script-src-attr 'none';style-src 'self' https: 'unsafe-inline';upgrade-insecure-requests
Content-Type: application/json; charset=utf-8
Cross-Origin-Resource-Policy: cross-origin
Date: Wed, 27 May 2026 12:25:23 GMT
Etag: W/"4a-xyNcfd+GEqdO8dCpEexVNnciBvQ"
Nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
Origin-Agent-Cluster: ?1
Referrer-Policy: no-referrer
Report-To: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=4AG%2F0i%2FgrxIbclxcYROnRk9Wu4doUWwwkbsqrxbVH7OsZSGvNyTi7UUGu5f9UPMvnq2B8T16WdqtgSqA5aCRwNmDPHAkWHjf04hEulH%2BypLiFRx7hfi43F2%2B2bATb3J5cl2ANN0Yr8YU"}]}
Server: cloudflare
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Dns-Prefetch-Control: off
X-Download-Options: noopen
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-Xss-Protection: 0
Body
{"success":true,"message":"Projects synced successfully","filesUpdated":9}

> AGENT

Found it. The webhook worked fine — sync pulled the new project. But `stealth-ai-startup` has `draft: true` in its frontmatter, and `GET /projects` filters out drafts unless you pass `?include_drafts=true`.

Two options:
- Flip `draft: true` → `draft: false` (or remove the line) in the project's `index.md` in the `project-writeups` repo
- Hit `https://vulkan.sumeetsaini.com/projects?include_drafts=true` if you want to see it without publishing

That's the whole story — the sync delivered 9 files (likely the `.md` + assets), but the draft flag is hiding it from the default list.
