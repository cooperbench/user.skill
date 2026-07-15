> DEVELOPER

gimme list of explanations of these http error codes 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416,
            417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451

> AGENT

| Code | Name | Meaning |
|------|------|---------|
| 400 | Bad Request | Malformed syntax, server can't parse |
| 401 | Unauthorized | Authentication required |
| 402 | Payment Required | Reserved for future use (digital payment) |
| 403 | Forbidden | Authenticated but lacks permission |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported for this endpoint |
| 406 | Not Acceptable | Can't produce response matching Accept headers |
| 407 | Proxy Authentication Required | Must authenticate with proxy first |
| 408 | Request Timeout | Server timed out waiting for request |
| 409 | Conflict | Request conflicts with current resource state |
| 410 | Gone | Resource permanently deleted, no forwarding |
| 411 | Length Required | Missing Content-Length header |
| 412 | Precondition Failed | Conditional header (If-Match, etc.) failed |
| 413 | Payload Too Large | Request body exceeds server limit |
| 414 | URI Too Long | URL exceeds server limit |
| 415 | Unsupported Media Type | Content-Type not supported |
| 416 | Range Not Satisfiable | Range header can't be fulfilled |
| 417 | Expectation Failed | Expect header can't be met |
| 418 | I'm a Teapot | RFC 2324 joke — refuses to brew coffee |
| 421 | Misdirected Request | Server can't produce response for this URI+scheme combo |
| 422 | Unprocessable Entity | Valid syntax but semantic errors (common in validation) |
| 423 | Locked | Resource is locked (WebDAV) |
| 424 | Failed Dependency | Failed because a dependent request failed (WebDAV) |
| 425 | Too Early | Server unwilling to process request that might be replayed (TLS early data) |
| 426 | Upgrade Required | Must switch protocols (e.g. to TLS) |
| 428 | Precondition Required | Request must be conditional to prevent lost updates |
| 429 | Too Many Requests | Rate limited |
| 431 | Request Header Fields Too Large | Headers exceed server limit |
| 451 | Unavailable For Legal Reasons | Censored/blocked by legal demand (named after Fahrenheit 451) |

> DEVELOPER

what is bad idea to sort out from new relic, what to keep

> AGENT

Not enough context. What are you sorting out?

- Alerts/policies?
- APM transactions?
- Dashboard widgets?
- Error groups?
- Log configurations?

Be specific about what you're evaluating and I can give a useful answer.

> DEVELOPER

we have new relic and we wantneed to understand what to log there what not to

> AGENT

## New Relic: What to Log vs Skip

### Keep (high value)

| What | Why |
|------|-----|
| HTTP transaction traces | Latency, throughput, error rates per endpoint |
| Error rates + stack traces | Root cause analysis |
| Database query performance | Slow queries, N+1 detection |
| External service calls | Algolia, OpenAI, MMS, SQS latency |
| Custom business metrics | Recommendation hit rates, cache hit/miss ratios |
| Apdex / response time percentiles | User experience |
| Memory + CPU per pod | Capacity planning |
| Redis latency + connection pool | Cache layer health |
| SQS queue depth + processing time | Queue backpressure |
| Deployment markers | Correlate perf changes to releases |

### Drop (noise / cost waste)

| What | Why |
|------|-----|
| Health check transactions (`/health`) | High volume, zero signal |
| Robots.txt requests | Irrelevant |
| Verbose debug-level logs | Kills your budget, search noise |
| Full request/response bodies | PII risk, storage cost |
| Successful 200 response details | Only log failures or slow responses |
| Load test endpoint traces | Pollutes real metrics |
| Static asset requests | No business value |
| High-cardinality custom attributes | Explodes NRDB costs |
| Every Redis GET/SET | Too granular, use aggregates |
| Cron job heartbeat pings | Use a dedicated uptime tool |

### Rules of Thumb

1. **Log anomalies, not norms** — alert on deviations, don't record every success
2. **Sample high-volume, keep low-volume** — 100% of errors, 10% of successful transactions
3. **Drop before ingest** — use New Relic drop rules, not post-query filtering (you pay for ingestion)
4. **Business metrics > infrastructure metrics** — "recommendations served per minute" > "CPU at 42%"
5. **Set data retention tiers** — 7 days for logs, 90 days for metrics, 30 days for traces

Want me to check your current New Relic config in the codebase for specific recommendations?
