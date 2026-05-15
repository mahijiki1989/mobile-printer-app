# Groww Auto-Exit

A production-grade Windows desktop trading assistant for **Groww**, built using
Groww's **official Trade API** only. It detects positions you opened manually
(equity or F&O) and automatically squares them off when your user-defined
P&L threshold is reached.

This app does **not** automate the Groww mobile/desktop UI, scrape screens,
read OCR, or simulate keyboard/mouse input. All position data and order
placement go through the official `growwapi` Python SDK.

> Trading is risky. Read [Live trading risk and safety](#live-trading-risk-and-safety)
> before enabling LIVE mode.

---

## Features

- **Login / Auth** with Groww access token, stored in the Windows Credential
  Manager (via `keyring`), never in plain text once configured.
- **Position Monitor** with continuous polling and optional WebSocket
  (`GrowwFeed`) subscription. Detects newly opened manual trades.
- **Exit Rule Engine** supporting:
  - absolute target (`+1000`) and absolute stop (`-500`) per position
  - default global rule for newly detected positions
  - account-level combined MTM rule
  - trailing lock (lock once intermediate profit is hit, exit on reversal)
  - one-shot or partial exit
- **Exit Executor** that places market or limit square-off orders, dedups,
  verifies status, retries with exponential backoff, and reports failures.
- **Risk & Safety**: panic exit-all, daily max loss guard, max open positions,
  trading hours filter, cooldown after exit, manual confirmation toggle,
  kill-switch on repeated disconnects, circuit breaker on rejections.
- **Alerts**: desktop notifications + sound on every important event.
- **Modern dark UI** with five tabs: Dashboard, Positions, Rules, Activity,
  Settings. Live P&L color coding, big status badges.
- **SQLite audit log** of every event, exportable to CSV.
- **Modes**: `live` (real money), `paper` (real prices, simulated fills),
  `mock` (simulated prices and fills, no network).
- **Tests** for the rule engine, risk guard and DB layer.
- **PyInstaller** packaging script for a Windows `.exe`.

---

## Architecture

```
                +---------------------------------------------+
                |              PySide6 UI Layer                |
                |  Dashboard | Positions | Rules | Logs | Cfg  |
                +-------------^-------------------^-----------+
                              | signals/slots     | signals
                +-------------+-------------------+-----------+
                |              MonitorWorker (QThread)        |
                |   tick loop: poll positions + ltp + rules   |
                +--+---------------+-----------------+--------+
                   |               |                 |
        +----------v-----+ +-------v-----+ +---------v-------+
        | PositionMonitor| | RuleEngine  | | ExitExecutor    |
        +----------------+ +------+------+ +-----------------+
                                  |
                         +--------v--------+
                         |    RiskGuard    |
                         +--------+--------+
                                  |
        +-------------------------v-------------------------+
        |                BrokerAdapter (ABC)                |
        |  GrowwAdapter | PaperAdapter | MockAdapter        |
        +------------------------+--------------------------+
                                 |
              +------------------+------------------+
              |  Groww Trade API (REST + GrowwFeed) |
              +-------------------------------------+
```

See `docs/ui_wireframe.md` for the UI layout.

---

## Project layout

```
groww-auto-exit/
  README.md
  requirements.txt
  .env.example
  run.py
  build_windows.py
  app.spec
  docs/
  src/groww_auto_exit/
    main.py
    config.py  logging_setup.py  secrets_store.py
    models.py  db.py  notifications.py
    broker/   base.py  groww_adapter.py  paper_adapter.py  mock_adapter.py
    services/ position_monitor.py  rule_engine.py  exit_executor.py  risk_guard.py
    workers/  monitor_worker.py
    ui/       theme.py  main_window.py  dashboard_view.py
              positions_view.py  rules_view.py  activity_view.py  settings_view.py
    utils/    retry.py  timeutils.py
  tests/
    test_rule_engine.py  test_risk_guard.py  test_db.py
```

---

## Setup (Windows)

1. **Install Python 3.11** (64-bit). Make sure it is on `PATH`.
2. **Get a Groww API key** at <https://groww.in/trade-api>. Generate an
   access token (long-lived) or note your `api_key` + `api_secret`.
3. **Clone and create a venv:**

   ```powershell
   git clone <your-fork> groww-auto-exit
   cd groww-auto-exit
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Configure secrets.** Copy `.env.example` to `.env` and fill in either
   `GROWW_ACCESS_TOKEN` or the `GROWW_API_KEY` / `GROWW_API_SECRET` pair.
   Set `GAE_MODE=paper` for first-time use.

5. **Run the app:**

   ```powershell
   python run.py
   ```

   On the first launch the app reads `.env`, then **moves the secret into
   Windows Credential Manager** (via `keyring`). After that, you can blank
   the secret values in `.env`.

6. **Switch to LIVE.** Open Settings -> Mode -> Live, then re-enter your
   confirmation phrase. A red banner stays visible for the whole session.

---

## Run tests

```powershell
pytest -q
```

The tests cover the rule engine, the risk guard, and the SQLite layer.
They do not require Groww credentials or network access.

---

## Build a Windows .exe

```powershell
python build_windows.py
```

This writes a self-contained app to `dist\GrowwAutoExit\GrowwAutoExit.exe`.
Distribute the entire `dist\GrowwAutoExit\` folder; the `.exe` needs the
sibling DLLs and resource files.

---

## Modes

| Mode  | Prices  | Orders                | Network         | Use case                    |
|-------|---------|-----------------------|-----------------|-----------------------------|
| live  | real    | placed for real       | Groww API       | production                  |
| paper | real    | simulated (no fill)   | Groww API (RO)  | strategy validation         |
| mock  | fake    | simulated             | none            | offline/UI/regression tests |

`paper` and `mock` are perfectly safe and never place real orders.

---

## How auto-exit works

1. `PositionMonitor` polls `broker.get_positions()` every `GAE_POLL_INTERVAL_SECONDS`
   seconds and merges WebSocket position updates when available.
2. New positions appear in the `Positions` tab. If a default rule is set, it is
   auto-attached. You can override per position from the `Rules` tab.
3. On every tick, `RuleEngine.evaluate(position, rule)` returns one of
   `HOLD | ARM | TRIGGER_EXIT`, optionally tagged with `TRAIL_LOCKED`.
4. `RiskGuard` filters: trading hours, daily loss cap, cooldown, max open
   positions, kill-switch, dedup. If the trigger passes, ...
5. `ExitExecutor` calls `broker.place_order()` with reversed `transaction_type`
   and the position's quantity (full or partial). Order id, status and the
   raw API response are logged to SQLite.
6. The order is then re-checked via `broker.get_order_status()` until it
   reaches a terminal state. Failures are retried with exponential backoff
   up to a configurable count, then surface as `ERROR` in the UI.

---

## Live trading risk and safety

Real money is at stake the moment you switch to LIVE. Read this checklist.

- Always test in `paper` mode for at least one full session before going LIVE.
- Set a sensible `GAE_DAILY_MAX_LOSS_INR` (negative number). The kill-switch
  will refuse new orders past this loss for the day.
- Set `GAE_REQUIRE_LIVE_CONFIRM=true` initially. You can disable it later.
- Watch the **status badge**: `ERROR` means the app stopped acting on rules.
- The **Panic Exit All** button always works, regardless of rules.
- Verify the Groww API key has only the scopes you need.
- Never put real credentials in source control. `.env` is `.gitignore`d.
- The app does **not** place new entry trades. It only squares off positions
  it sees in your Groww account.

### Pre-flight checklist before going LIVE

- [ ] `pytest -q` is green
- [ ] `paper` mode ran for a full session without unexpected behaviour
- [ ] Default rule values look right (`+target`, `-stop`)
- [ ] Daily max loss cap is set
- [ ] Trading hours window matches your strategy
- [ ] Notifications work (you got a desktop popup in `paper` mode)
- [ ] Panic exit button has been tested in `paper` mode
- [ ] You have a manual fallback if the app crashes

---

## License and attribution

This project uses Groww's **official** [`growwapi`](https://pypi.org/project/growwapi/)
SDK and follows Groww's
[Trade API documentation](https://groww.in/trade-api/docs/python-sdk).
No reverse engineering, scraping, OCR or UI automation is performed.
