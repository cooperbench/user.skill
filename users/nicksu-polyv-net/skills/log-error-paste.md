---
name: log-error-paste
description: Trigger — runtime error appears in the trading bot logs. Nick pastes the raw loguru-formatted log lines verbatim, sometimes with a single Chinese question appended.
---

Nick pastes raw log output from the Python `loguru` logger (format: `YYYY-MM-DD HH:MM:SS | LEVEL | ThreadName | module | message`). He does not reformat, truncate, or summarize the log. The Chinese commentary, if present, is one line appended at the end.

**Pattern**:
- One or more raw log lines starting with timestamp
- Optional one-line Chinese question at the end

**Example 1** (API error, no commentary):
```
2026-02-27 03:39:30 | ERROR    | ThreadPoolExecutor-0_0 | src.trading.live_trading | ❌ ❌ Unexpected error in sell position: PolyApiException[status_code=400, error_message={'error': 'the orderbook 13815952460361514493880496712561164230868624302562138286445313445449019645304 does not exist'}]
2026-02-27 03:39:30 | ERROR    | ThreadPoolExecutor-0_0 | __main__ | ❌ Exit failed for position 46: Unexpected error: PolyApiException[status_code=400, error_message={'error': 'the orderbook 13815952460361514493880496712561164230868624302562138286445313445449019645304 does not exist'}]
```

**Example 2** (API credential error + Chinese question):
```
2026-02-27 14:59:38 | ERROR    | ThreadPoolExecutor-0_3 | src.trading.live_trading | ❌ ❌ Unexpected error in sell position: API Credentials are needed to interact with this endpoint!
2026-02-27 14:59:38 | ERROR    | ThreadPoolExecutor-0_3 | __main__ | ❌ Exit failed for position 86: Unexpected error: API Credentials are needed to interact with this endpoint!

这个错误是什么问题
```

**Example 3** (state error, single line):
```
2026-02-27 09:28:11 | ERROR    | MainThread   | src.core.state | ❌ Daily PnL (-71.23660164000002) exceeds capital (32.404225)
```

**Example 4** (JSON API error body + Chinese context):
```
{
    "detail": {
        "success": false,
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "'MarketRepository' object has no attribute 'get_by_id'"
        }
    }
}

退出接口报上面的错误
```
