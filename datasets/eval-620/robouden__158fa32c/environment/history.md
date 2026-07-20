> DEVELOPER

Can you check issue at https://codeberg.org/Safecast/bGeigieZen/issues/5?

> TOOL

tool_use ToolSearch
id: toolu_01Y14hgYr2nLSSp8MyQzeLnr
```json
{
  "query": "select:WebFetch",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01Y14hgYr2nLSSp8MyQzeLnr
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use WebFetch
id: toolu_01BmanNsrsheVgS2gQykfdy1
```json
{
  "url": "https://codeberg.org/Safecast/bGeigieZen/issues/5",
  "prompt": "Extract the full issue: title, author, status (open/closed), labels, body/description, and any comments with their authors. Include all technical details mentioned."
}
```

> TOOL

tool_result
id: toolu_01BmanNsrsheVgS2gQykfdy1
```
# Issue #5: GPS Coordinate Logging Problem

**Title:** "Occasional longitude, latitude all zeroes even when log_void is false"

**Author:** louisbertrand

**Status:** Open

**Labels:** development

**Assignee:** louisbertrand

---

## Issue Description

The bGeigieZen device occasionally records lines in the drive LOG file displaying "0000.0000,0000.0000" for latitude and longitude coordinates, despite the log_void parameter in SAFEZEN.TXT being set to 0 (false, indicating data should be logged).

The reporter suspects the root cause lies in `gps_connector.cpp`, specifically within the `int8_t GpsConnector::produce_data()` function. The issue appears related to how the U-Blox NavPVT fix type validation works—currently accepting status 2 or 3, but a 2D fix may be insufficiently reliable for data logging.

---

## Comments

**Rob Oudendijk** (Owner, 2026-04-25 22:29:11 +02:00) posed clarifying questions:

- Which U-Blox GPS model: M7, M8, or M10?
- What firmware version?
- Any proposed solutions?

---

## Technical Context

This represents a data quality issue where invalid GPS coordinates are being persisted despite filtering settings being disabled.
```

> AGENT

Here's the summary of [Issue #5](https://codeberg.org/Safecast/bGeigieZen/issues/5):

**Title:** Occasional longitude, latitude all zeroes even when log_void is false
**Author/Assignee:** louisbertrand
**Status:** Open · Label: `development`

**Problem:** LOG files occasionally contain `0000.0000,0000.0000` for lat/lon even though `log_void=0` in `SAFEZEN.TXT`.

**Suspected cause:** [gps_connector.cpp](src/gps_connector.cpp) — `GpsConnector::produce_data()`. The U-Blox NavPVT fix-type check accepts both `2` (2D) and `3` (3D); a 2D fix may not be reliable enough to log.

**Outstanding questions** (asked by you on 2026-04-25): which u-blox model (M7/M8/M10), firmware version, proposed fix.

Want me to open [gps_connector.cpp](src/gps_connector.cpp) and look at the fix-type gate + the zero-coord path to draft a response or patch?