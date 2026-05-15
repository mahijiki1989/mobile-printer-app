"""Rule engine: pure, deterministic, fully unit-testable.

Given a position and an exit rule, returns a `Decision` describing whether to
HOLD, ARM (rule attached but not yet triggered), TRIGGER_EXIT, or report a
THRESHOLD_NEAR alert. The engine also mutates the rule's trailing state when
trail_lock + trail_giveback are configured.

Important: this module has no I/O, no logging side-effects on hot paths, no
broker calls. Everything is a function of (position, rule).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..models import ExitMode, ExitRule, Position


class Action(str, Enum):
    HOLD = "HOLD"
    ARM = "ARM"
    THRESHOLD_NEAR = "THRESHOLD_NEAR"
    TRIGGER_EXIT = "TRIGGER_EXIT"


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str
    exit_quantity: int = 0  # how many units to square off when TRIGGER_EXIT
    near_pct: float = 0.0   # how close to trigger, 0.0..1.0


# Threshold within 20% of target/stop counts as "near".
_NEAR_BAND = 0.20


class RuleEngine:
    """Stateless evaluator. Trailing state lives on the rule object."""

    def __init__(self, near_band: float = _NEAR_BAND) -> None:
        self.near_band = near_band

    # ------------------------------------------------------------------ api

    def evaluate(self, position: Position, rule: ExitRule) -> Decision:
        if not rule.enabled:
            return Decision(Action.HOLD, "rule disabled")
        if rule.target_inr is None and rule.stop_inr is None and rule.trail_lock_inr is None:
            return Decision(Action.HOLD, "no thresholds configured")
        if position.quantity == 0:
            return Decision(Action.HOLD, "position is flat")

        mtm = position.mtm

        # --- update trailing state first so trigger logic sees it ----------
        self._update_trailing(rule, mtm)

        # --- absolute target ----------------------------------------------
        if rule.target_inr is not None and mtm >= rule.target_inr:
            qty = self._exit_qty(position, rule)
            return Decision(
                Action.TRIGGER_EXIT,
                f"MTM {mtm:.2f} >= target {rule.target_inr:.2f}",
                exit_quantity=qty,
            )

        # --- absolute stop ------------------------------------------------
        if rule.stop_inr is not None and mtm <= rule.stop_inr:
            qty = self._exit_qty(position, rule)
            return Decision(
                Action.TRIGGER_EXIT,
                f"MTM {mtm:.2f} <= stop {rule.stop_inr:.2f}",
                exit_quantity=qty,
            )

        # --- trailing exit ------------------------------------------------
        if rule.trail_locked and rule.trail_giveback_inr and rule.trail_high_water is not None:
            give = max(0.0, float(rule.trail_giveback_inr))
            if mtm <= rule.trail_high_water - give:
                qty = self._exit_qty(position, rule)
                return Decision(
                    Action.TRIGGER_EXIT,
                    (
                        f"trailing giveback hit: peak {rule.trail_high_water:.2f},"
                        f" now {mtm:.2f}, allowed {give:.2f}"
                    ),
                    exit_quantity=qty,
                )

        near = self._near_pct(rule, mtm)
        if near >= 1.0 - self.near_band:
            return Decision(
                Action.THRESHOLD_NEAR,
                f"MTM {mtm:.2f} within {self.near_band*100:.0f}% of trigger",
                near_pct=near,
            )

        return Decision(Action.ARM, f"armed (MTM {mtm:.2f})", near_pct=near)

    # -------------------------------------------------------------- helpers

    def _update_trailing(self, rule: ExitRule, mtm: float) -> None:
        if rule.trail_lock_inr is None:
            return
        if rule.trail_high_water is None or mtm > rule.trail_high_water:
            rule.trail_high_water = mtm
        if not rule.trail_locked and mtm >= rule.trail_lock_inr:
            rule.trail_locked = True

    def _near_pct(self, rule: ExitRule, mtm: float) -> float:
        """Return progress toward the closest configured threshold, [0..1+]."""
        candidates: list[float] = []
        if rule.target_inr is not None and rule.target_inr > 0:
            candidates.append(max(0.0, mtm) / rule.target_inr)
        if rule.stop_inr is not None and rule.stop_inr < 0:
            candidates.append(max(0.0, -mtm) / -rule.stop_inr)
        return max(candidates) if candidates else 0.0

    def _exit_qty(self, p: Position, rule: ExitRule) -> int:
        if rule.exit_mode == ExitMode.PARTIAL and rule.partial_qty:
            return min(p.abs_quantity, int(rule.partial_qty))
        return p.abs_quantity


# ---------------------------------------------------- account-level helper

def evaluate_account_rule(
    positions: list[Position],
    target_inr: Optional[float],
    stop_inr: Optional[float],
) -> Decision:
    """Combined account MTM rule. Returns TRIGGER_EXIT if the account total
    breaches either bound, otherwise HOLD/ARM. The caller is responsible for
    iterating through all positions and squaring off each one."""
    if not positions:
        return Decision(Action.HOLD, "no positions")
    total = sum(p.mtm for p in positions)
    if target_inr is not None and total >= target_inr:
        return Decision(Action.TRIGGER_EXIT, f"Account MTM {total:.2f} >= {target_inr:.2f}")
    if stop_inr is not None and total <= stop_inr:
        return Decision(Action.TRIGGER_EXIT, f"Account MTM {total:.2f} <= {stop_inr:.2f}")
    return Decision(Action.ARM, f"account armed (MTM {total:.2f})")
