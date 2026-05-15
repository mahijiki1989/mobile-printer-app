"""Dark theme stylesheet and small color constants."""
from __future__ import annotations

DARK_QSS = """
* { font-family: "Segoe UI", "Inter", "Arial"; font-size: 13px; color: #E6E6E6; }

QWidget { background-color: #1E1F22; }
QMainWindow { background-color: #16171A; }

QToolBar { background-color: #16171A; border: 0; padding: 6px; spacing: 8px; }
QStatusBar { background-color: #16171A; color: #BBBBBB; border-top: 1px solid #2A2B30; }

QListWidget#sideNav {
    background-color: #16171A;
    border: 0;
    padding: 8px 0;
    outline: 0;
}
QListWidget#sideNav::item {
    padding: 12px 16px;
    border-left: 3px solid transparent;
    color: #BBBBBB;
}
QListWidget#sideNav::item:selected {
    background-color: #23252B;
    border-left: 3px solid #4C8DFF;
    color: #FFFFFF;
}

QPushButton {
    background-color: #2A2B30;
    border: 1px solid #34363C;
    padding: 6px 14px;
    border-radius: 4px;
    color: #E6E6E6;
}
QPushButton:hover  { background-color: #34363C; }
QPushButton:pressed{ background-color: #3D4047; }
QPushButton:disabled { color: #666; background-color: #202126; }

QPushButton#panicButton {
    background-color: #B23434;
    border: 1px solid #D14848;
    color: #FFFFFF;
    font-weight: 600;
}
QPushButton#panicButton:hover { background-color: #C73E3E; }

QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #2A2B30;
    border: 1px solid #34363C;
    padding: 6px 8px;
    border-radius: 4px;
    selection-background-color: #4C8DFF;
}

QHeaderView::section {
    background-color: #23252B;
    color: #BBBBBB;
    padding: 6px;
    border: 0;
    border-bottom: 1px solid #2A2B30;
}
QTableWidget, QTableView {
    background-color: #1E1F22;
    alternate-background-color: #23252B;
    gridline-color: #2A2B30;
    border: 1px solid #2A2B30;
    selection-background-color: #34363C;
}

QLabel#bigBadge {
    padding: 6px 12px;
    border-radius: 12px;
    font-weight: 700;
    color: #FFFFFF;
}

QLabel#liveBanner {
    background-color: #5D1A1A;
    color: #FFFFFF;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 700;
}

QGroupBox {
    border: 1px solid #2A2B30;
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #AAAAAA;
}
"""

# colors used by table cells / badges
COLOR_PROFIT = "#3FB950"
COLOR_LOSS = "#F85149"
COLOR_NEUTRAL = "#9CA3AF"

BADGE_COLORS = {
    "MONITORING": "#1F6FEB",
    "ARMED": "#D29922",
    "EXIT_TRIGGERED": "#FB8C00",
    "EXITED": "#2DA44E",
    "ERROR": "#CF222E",
}
