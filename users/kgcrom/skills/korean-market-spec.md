---
name: korean-market-spec
description: >-
  Trigger: kgcrom is designing a new screen, API integration, or data flow for
  cluefin-desk. They write highly structured Korean specs with ASCII box-drawing
  UI mockups (Bloomberg-style), API ID tables, and parameter Literal type
  definitions. They expect zero explanation from the agent about Korean financial
  terminology.
---

kgcrom designs Korean stock market UIs with Bloomberg Terminal as the reference point. Specs include ASCII art of the full screen layout with Korean column headers, API method tables with API IDs (e.g., ka10019, ka10034), and precise parameter values from official Kiwoom/KIS documentation.

**Format of a screen spec**:
- Screen name in Korean + Bloomberg analogue reference
- Full ASCII box mockup with `┌─┬─┐` box-drawing characters
- Korean column headers inside the boxes (종목명, 현재가, 등락률, 거래량, etc.)
- Navigation structure with numbered keys (`1·MKT`, `2·RANK`, etc.)
- API table: `| 영역 | API 메서드 | API ID | 상태 |`
- Literal type constraints for parameters: `mrkt_tp: Literal["000", "001", "101", "201"]`

**Domain terms kgcrom uses without defining**:
- `업종코드` (sector code): `001` = KOSPI 종합, `101` = KOSDAQ 종합
- `순매수` (net buy), `급등락` (rapid rise/fall), `외국인` (foreign investors), `기관` (institutions)
- `ka10019`, `ka10034`, `ka10063`, `ka90003` — Kiwoom API IDs
- `DART` — Korean corporate disclosure system
- `XBRL` — financial statement markup for DART

**Verbatim example (API table from spec)**:
```
| 영역 | API 메서드 | API ID | 상태 |
|------|-----------|--------|------|
| 외국인 순매수 (좌상) | `rank_info.get_top_foreigner_period_trading()` | ka10034 | **정상** |
| 기관 순매수 (우상) | `rank_info.get_top_intraday_trading_by_investor()` | ka10063 | **미표시** |
| 프로그램매매 (중앙) | `stock_info.get_top_50_program_net_buy()` | ka90003 | **미표시** |
```

**Verbatim example (parameter fix table)**:
```
| 파라미터 | 현재 (잘못됨) | 수정 | 이유 |
|---------|-------------|------|------|
| `tm_tp` | `"0"` | `"1"` | 분전 기준 (유효값: "1" or "2") |
| `tm` | `""` | `"60"` | 60분전 대비 |
| `trde_qty_tp` | `"0"` | `"00000"` | 전체조회 (5자리 코드) |
```
