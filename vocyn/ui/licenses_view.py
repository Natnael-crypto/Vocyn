import os
import json
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView,
    QSplitter, QFrame
)
from PySide6.QtCore import Qt

def get_base_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'vocyn')
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LicensesView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #000000; color: #E0E0E0; font-family: 'Inter', 'Segoe UI', sans-serif; }
            QLabel { color: #E0E0E0; }
            QLabel#h1 { font-size: 24px; font-weight: bold; color: #FFFFFF; margin-bottom: 4px; }
            QLabel#h2 { font-size: 14px; color: #888888; margin-bottom: 20px; }
            QTableWidget {
                background-color: #111111;
                color: #FFFFFF;
                border: 1px solid #222222;
                border-radius: 8px;
                gridline-color: #1A1A1A;
            }
            QTableWidget::item { padding: 8px; }
            QTableWidget::item:selected { background-color: #222222; color: #FFFFFF; }
            QHeaderView::section {
                background-color: #111111;
                color: #888888;
                border: none;
                border-bottom: 1px solid #222222;
                padding: 8px;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 11px;
            }
            QTextEdit {
                background-color: #111111;
                color: #AAAAAA;
                border: 1px solid #222222;
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                padding: 15px;
            }
            QScrollBar:vertical {
                border: none;
                background: #000000;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical { background: #333333; border-radius: 4px; }
            QSplitter::handle {
                background-color: transparent;
                height: 24px;
            }
        """)

        self.licenses_data = []
        self.licenses_dir = os.path.join(get_base_path(), "licenses")

        self.setup_ui()
        self.load_licenses()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 100)
        layout.setSpacing(0)

        lbl_title = QLabel("Open Source Licenses")
        lbl_title.setObjectName("h1")
        lbl_subtitle = QLabel("Vocyn relies on the following open-source libraries")
        lbl_subtitle.setObjectName("h2")
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_subtitle)

        splitter = QSplitter(Qt.Vertical)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Library", "License"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        splitter.addWidget(self.table)

        # Text Area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        splitter.addWidget(self.text_area)
        
        splitter.setHandleWidth(24)
        splitter.setSizes([200, 400])
        layout.addWidget(splitter)

    def load_licenses(self):
        json_path = os.path.join(self.licenses_dir, "licenses.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.licenses_data = json.load(f)
        except Exception as e:
            self.text_area.setText(f"Failed to load licenses.json: {e}")
            return

        self.table.setRowCount(len(self.licenses_data))
        for row, pkg in enumerate(self.licenses_data):
            self.table.setItem(row, 0, QTableWidgetItem(pkg.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(pkg.get("license", "")))

        if len(self.licenses_data) > 0:
            self.table.selectRow(0)

    def on_selection_changed(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        row = selected[0].row()
        pkg = self.licenses_data[row]
        filename = pkg.get("file", "")
        
        if not filename:
            self.text_area.setText("No license file specified.")
            return

        file_path = os.path.join(self.licenses_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.text_area.setText(f.read())
        except Exception as e:
            self.text_area.setText(f"Failed to load {filename}: {e}")
