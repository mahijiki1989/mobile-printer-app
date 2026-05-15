"""Settings tab: mode, secrets, risk caps, account-level rule."""
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox,
    QVBoxLayout, QWidget,
)

from ..config import ExitOrderType, Mode, Settings


class SettingsView(QWidget):
    modeChangeRequested = Signal(object)   # Mode
    secretsSaveRequested = Signal(str, str, str)  # access_token, api_key, api_secret
    settingsChanged = Signal(object)       # Settings
    accountRuleChanged = Signal(object, object)   # target, stop (Optional[float])

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings
        self._build()
        self._populate()

    def _build(self) -> None:
        outer = QVBoxLayout(self)

        # --- Mode + secrets
        modeBox = QGroupBox("Mode and credentials")
        modeForm = QFormLayout(modeBox)

        self.modeCombo = QComboBox()
        for m in Mode:
            self.modeCombo.addItem(m.value, m)

        self.tokenEdit = QLineEdit()
        self.tokenEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.tokenEdit.setPlaceholderText("Stored in OS keyring after save")

        self.apiKeyEdit = QLineEdit()
        self.apiKeyEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.apiSecretEdit = QLineEdit()
        self.apiSecretEdit.setEchoMode(QLineEdit.EchoMode.Password)

        modeForm.addRow("Mode", self.modeCombo)
        modeForm.addRow("Access token", self.tokenEdit)
        modeForm.addRow("API key", self.apiKeyEdit)
        modeForm.addRow("API secret", self.apiSecretEdit)

        btnRow = QHBoxLayout()
        self.saveSecretsBtn = QPushButton("Save credentials to keyring")
        self.applyModeBtn = QPushButton("Apply mode")
        btnRow.addWidget(self.saveSecretsBtn)
        btnRow.addWidget(self.applyModeBtn)
        btnRow.addStretch()
        modeForm.addRow(btnRow)

        # --- Risk
        riskBox = QGroupBox("Risk caps")
        riskForm = QFormLayout(riskBox)

        self.dailyLossSpin = QDoubleSpinBox()
        self.dailyLossSpin.setRange(-10_000_000.0, 0.0)
        self.dailyLossSpin.setDecimals(2)

        self.maxOpenSpin = QSpinBox()
        self.maxOpenSpin.setRange(1, 500)

        self.cooldownSpin = QSpinBox()
        self.cooldownSpin.setRange(0, 3600)

        self.tradeStartEdit = QLineEdit()
        self.tradeEndEdit = QLineEdit()

        self.exitTypeCombo = QComboBox()
        for t in ExitOrderType:
            self.exitTypeCombo.addItem(t.value, t)

        self.slippageSpin = QDoubleSpinBox()
        self.slippageSpin.setRange(0.0, 10.0)
        self.slippageSpin.setDecimals(2)
        self.slippageSpin.setSingleStep(0.05)

        self.requireConfirmCheck = QCheckBox("Require manual confirmation in LIVE mode")

        riskForm.addRow("Daily max loss INR", self.dailyLossSpin)
        riskForm.addRow("Max open positions", self.maxOpenSpin)
        riskForm.addRow("Cooldown (s)", self.cooldownSpin)
        riskForm.addRow("Trading hours start (HH:MM)", self.tradeStartEdit)
        riskForm.addRow("Trading hours end (HH:MM)", self.tradeEndEdit)
        riskForm.addRow("Exit order type", self.exitTypeCombo)
        riskForm.addRow("Limit slippage %", self.slippageSpin)
        riskForm.addRow(self.requireConfirmCheck)

        # --- Account-level rule
        acctBox = QGroupBox("Account-level rule (optional)")
        acctForm = QFormLayout(acctBox)
        self.acctTargetSpin = QDoubleSpinBox()
        self.acctTargetSpin.setRange(0.0, 10_000_000.0)
        self.acctStopSpin = QDoubleSpinBox()
        self.acctStopSpin.setRange(-10_000_000.0, 0.0)
        acctForm.addRow("Account target +INR", self.acctTargetSpin)
        acctForm.addRow("Account stop -INR", self.acctStopSpin)

        # --- Apply
        applyRow = QHBoxLayout()
        self.applyBtn = QPushButton("Apply settings")
        applyRow.addStretch()
        applyRow.addWidget(self.applyBtn)

        outer.addWidget(modeBox)
        outer.addWidget(riskBox)
        outer.addWidget(acctBox)
        outer.addLayout(applyRow)
        outer.addStretch()

        self.saveSecretsBtn.clicked.connect(self._on_save_secrets)
        self.applyModeBtn.clicked.connect(self._on_apply_mode)
        self.applyBtn.clicked.connect(self._on_apply_settings)

    # ----- helpers --------------------------------------------------------

    def _populate(self) -> None:
        s = self._settings
        idx = self.modeCombo.findData(s.mode)
        self.modeCombo.setCurrentIndex(max(0, idx))
        self.dailyLossSpin.setValue(s.daily_max_loss_inr)
        self.maxOpenSpin.setValue(s.max_open_positions)
        self.cooldownSpin.setValue(s.cooldown_seconds)
        self.tradeStartEdit.setText(s.trading_hours_start)
        self.tradeEndEdit.setText(s.trading_hours_end)
        self.exitTypeCombo.setCurrentIndex(self.exitTypeCombo.findData(s.exit_order_type))
        self.slippageSpin.setValue(s.limit_slippage_pct)
        self.requireConfirmCheck.setChecked(s.require_live_confirm)

    def _on_save_secrets(self) -> None:
        token = self.tokenEdit.text().strip()
        ak = self.apiKeyEdit.text().strip()
        ase = self.apiSecretEdit.text().strip()
        if not (token or (ak and ase)):
            QMessageBox.warning(self, "Credentials", "Provide an access token or API key + secret.")
            return
        self.secretsSaveRequested.emit(token, ak, ase)
        self.tokenEdit.clear()
        self.apiKeyEdit.clear()
        self.apiSecretEdit.clear()
        QMessageBox.information(self, "Credentials", "Saved to OS keyring.")

    def _on_apply_mode(self) -> None:
        mode = self.modeCombo.currentData()
        if mode == Mode.LIVE:
            ok = QMessageBox.question(
                self, "Confirm LIVE mode",
                "You are switching to LIVE. Real orders will be placed when "
                "thresholds are met. Continue?",
            )
            if ok != QMessageBox.StandardButton.Yes:
                return
        self.modeChangeRequested.emit(mode)

    def _on_apply_settings(self) -> None:
        try:
            new = self._settings.model_copy(update=dict(
                daily_max_loss_inr=self.dailyLossSpin.value(),
                max_open_positions=self.maxOpenSpin.value(),
                cooldown_seconds=self.cooldownSpin.value(),
                trading_hours_start=self.tradeStartEdit.text().strip(),
                trading_hours_end=self.tradeEndEdit.text().strip(),
                exit_order_type=self.exitTypeCombo.currentData(),
                limit_slippage_pct=self.slippageSpin.value(),
                require_live_confirm=self.requireConfirmCheck.isChecked(),
            ))
        except Exception as e:
            QMessageBox.warning(self, "Settings", f"Invalid: {e}")
            return
        self._settings = new
        self.settingsChanged.emit(new)
        target = self.acctTargetSpin.value() or None
        stop = self.acctStopSpin.value() or None
        self.accountRuleChanged.emit(target, stop)
