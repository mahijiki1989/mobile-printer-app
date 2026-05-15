# UI Wireframe

```
+----------------------------------------------------------------------+
| Groww Auto-Exit                                  [● LIVE] [PAPER]  X |
+----------------------------------------------------------------------+
| +----------+                                                         |
| |Dashboard |  STATUS: [ MONITORING ]   Connection: ● Connected       |
| |Positions |  Account MTM:  +Rs 1,240.50    Day P&L cap: -Rs 5,000   |
| |Rules     |  Open positions: 3   Rules armed: 2   Exits today: 1    |
| |Activity  |                                                         |
| |Settings  |  +-- Quick actions ----------------------------------+  |
| +----------+  | [ PANIC EXIT ALL ]  [ PAUSE ]  [ RESUME ]         |  |
|               +---------------------------------------------------+  |
+----------------------------------------------------------------------+
| Positions                                                            |
| +-Sym--------+Exch+Seg-+Prod+Qty-+Avg----+LTP----+MTM-----+Rule----+ |
| |NIFTY24500CE|NSE |FNO |NRML| 50 | 110.2 | 132.5 |+1,115  |+1000 A| |
| |RELIANCE    |NSE |CASH|MIS | 10 |2840.0 |2812.4 | -276   |-500   | |
| +------------+----+----+----+----+-------+-------+--------+-------+ |
+----------------------------------------------------------------------+
| Activity log (latest)                                                |
| 13:41:02  POSITION_DETECTED  RELIANCE qty=10 avg=2840.0              |
| 13:42:18  RULE_ARMED         NIFTY24500CE target=+1000               |
| 13:47:55  EXIT_TRIGGERED     NIFTY24500CE mtm=+1115 -> SELL MKT 50   |
| 13:47:56  ORDER_PLACED       id=GRW123 status=ACKED                  |
| 13:47:58  ORDER_FILLED       id=GRW123 status=EXECUTED price=132.4   |
+----------------------------------------------------------------------+
```

## Status badges

- `MONITORING` (blue)  - app is connected and watching positions
- `ARMED`      (amber) - at least one rule is attached and waiting
- `EXIT_TRIGGERED` (orange) - threshold met, exit order in flight
- `EXITED`     (green) - exit fully filled
- `ERROR`      (red)   - API disconnected, kill-switch tripped, or order rejected

## Color rules

- Profit MTM: green text
- Loss MTM:   red text
- Threshold within 20% of trigger: amber background

## Live mode protections

- A red banner is shown in LIVE mode at all times.
- If `GAE_REQUIRE_LIVE_CONFIRM=true`, a modal confirmation appears before each
  exit order is sent (with a 5 second auto-confirm timer).
- A persistent panic button is always visible in the toolbar.
