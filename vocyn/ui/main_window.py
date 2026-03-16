from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QScrollArea, QSizePolicy,
    QApplication, QToolTip, QStackedWidget
)
from PySide6.QtCore import Qt, QSize, Signal, QPoint
from PySide6.QtGui import QFont, QIcon, QColor, QCursor
import os
import sys

def get_asset_path(filename):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'vocyn', 'assets', filename)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", filename)

from vocyn.config import config
from vocyn.ui.settings_view import SettingsView
from vocyn.ui.licenses_view import LicensesView
from vocyn.ui.about_view import AboutView


# Modern LiveKit-inspired dark theme
STYLESHEET = """
QMainWindow {
    background-color: #000000;
}
QWidget {
    background-color: transparent;
    color: #E0E0E0;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}
QFrame#card {
    background-color: #111111;
    border-radius: 12px;
    border: 1px solid #1A1A1A;
}
QPushButton {
    background-color: #222222;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #333333;
    border: 1px solid #444444;
}
QPushButton#action_btn {
    background-color: #FFFFFF;
    color: #000000;
    border: none;
}
QPushButton#action_btn:hover {
    background-color: #E0E0E0;
}
QLabel#h1 {
    font-size: 24px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#h2 {
    font-size: 14px;
    color: #888888;
    margin-bottom: 8px;
}
QLabel#metric_val {
    font-size: 16px;
    font-weight: bold;
    color: #FFFFFF;
}
QLabel#metric_lbl {
    font-size: 11px;
    color: #888888;
    text-transform: uppercase;
    font-weight: bold;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    border: none;
    background: #000000;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #333333;
    min-height: 20px;
    border-radius: 4px;
}
"""

class ClickableLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setWordWrap(True)
        self.setStyleSheet("""
            QLabel {
                color: #CCCCCC; 
                font-size: 13px; 
                margin: 4px 0px;
                padding: 8px;
                border-radius: 6px;
            }
            QLabel:hover {
                background-color: #1A1A1A;
                color: #FFFFFF;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.text())

class MainWindow(QMainWindow):
    dictation_toggled = Signal()
    settings_saved = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocyn")
        self.setFixedSize(540, 600)
        self.setStyleSheet(STYLESHEET)
        
        self.recent_transcriptions = []
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Main Content Area ---
        self.stacked_widget = QStackedWidget()
        
        # 1. Dashboard View
        self.dashboard_view = QWidget()
        self.setup_dashboard_view()
        self.stacked_widget.addWidget(self.dashboard_view)
        
        # 2. Settings View
        self.settings_view = SettingsView()
        self.settings_view.settings_saved.connect(self.on_settings_saved)
        self.stacked_widget.addWidget(self.settings_view)
        
        # 3. Licenses View
        self.licenses_view = LicensesView()
        self.stacked_widget.addWidget(self.licenses_view)
        
        # 4. About View
        self.about_view = AboutView()
        self.stacked_widget.addWidget(self.about_view)
        
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
        
        # --- Floating Nav ---
        self.floating_nav = QFrame(self)
        self.floating_nav.setObjectName("floating_nav")
        self.floating_nav.setStyleSheet("""
            QFrame#floating_nav {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 30px;
            }
        """)
        nav_layout = QHBoxLayout(self.floating_nav)
        nav_layout.setContentsMargins(15, 10, 15, 10)
        nav_layout.setSpacing(10)
        
        self.btn_dashboard = self.create_nav_button(get_asset_path("ic_home.svg"), "Dashboard", active=True)
        self.btn_settings = self.create_nav_button(get_asset_path("ic_settings.svg"), "Settings")
        self.btn_licenses = self.create_nav_button(get_asset_path("ic_licenses.svg"), "Licenses")
        self.btn_about = self.create_nav_button(get_asset_path("ic_about.svg"), "About")
        
        self.btn_dashboard.clicked.connect(lambda: self.switch_view(0))
        self.btn_settings.clicked.connect(lambda: self.switch_view(1))
        self.btn_licenses.clicked.connect(lambda: self.switch_view(2))
        self.btn_about.clicked.connect(lambda: self.switch_view(3))
        
        nav_layout.addWidget(self.btn_dashboard)
        nav_layout.addWidget(self.btn_settings)
        nav_layout.addWidget(self.btn_licenses)
        nav_layout.addWidget(self.btn_about)
        
        self.floating_nav.show()
        
        self.update_config_display()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        nav_width = 240
        nav_height = 60
        x = (self.width() - nav_width) // 2
        y = self.height() - nav_height - 30
        self.floating_nav.setGeometry(x, y, nav_width, nav_height)
        self.floating_nav.raise_()

    def create_nav_button(self, icon_path, tooltip, active=False):
        btn = QPushButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setToolTip(tooltip)
        btn.setCheckable(True)
        btn.setChecked(active)
        btn.setFixedSize(40, 40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#333333' if active else 'transparent'};
                border: {'1px solid #555555' if active else 'none'};
                border-radius: 20px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {'#444444' if active else '#222222'};
            }}
            QPushButton:checked {{
                background-color: #333333;
                border: 1px solid #555555;
            }}
        """)
        return btn
        
    def switch_view(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
        buttons = [self.btn_dashboard, self.btn_settings, self.btn_licenses, self.btn_about]
        for i, btn in enumerate(buttons):
            active = (i == index)
            btn.setChecked(active)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {'#333333' if active else 'transparent'};
                    border: {'1px solid #555555' if active else 'none'};
                    border-radius: 20px;
                    padding: 0px;
                }}
                QPushButton:hover {{
                    background-color: {'#444444' if active else '#222222'};
                }}
            """)
            
    def show_settings_view(self):
        self.switch_view(1)
        
    def on_settings_saved(self):
        self.update_config_display()
        self.settings_saved.emit()
        self.switch_view(0) # Go back to dashboard after save
        
    def setup_dashboard_view(self):
        content_layout = QVBoxLayout(self.dashboard_view)
        content_layout.setContentsMargins(40, 40, 40, 100) # bottom margin for nav
        content_layout.setSpacing(24)
        
        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        lbl_h1 = QLabel("System Status")
        lbl_h1.setObjectName("h1")
        lbl_h2 = QLabel("Monitor and control the transcription engine.")
        lbl_h2.setObjectName("h2")
        
        header_layout.addWidget(lbl_h1)
        header_layout.addWidget(lbl_h2)
        content_layout.addWidget(header_widget)
        
        # Control Card (Status & Stop/Start)
        self.card_control = QFrame()
        self.card_control.setObjectName("card")
        self.card_control.setFixedHeight(90)
        card_control_layout = QHBoxLayout(self.card_control)
        card_control_layout.setContentsMargins(24, 20, 24, 20)
        
        self.lbl_status_dot = QLabel("●")
        self.lbl_status_dot.setStyleSheet("color: #4CAF50; font-size: 20px;")
        
        status_text_layout = QVBoxLayout()
        status_text_layout.setSpacing(2)
        self.lbl_status_title = QLabel("Engine Idle")
        self.lbl_status_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #FFFFFF;")
        self.lbl_status_desc = QLabel(f"Ready on {config.get('audio_device')}")
        self.lbl_status_desc.setStyleSheet("color: #888888; font-size: 13px;")
        status_text_layout.addWidget(self.lbl_status_title)
        status_text_layout.addWidget(self.lbl_status_desc)
        
        self.btn_toggle = QPushButton("Start Dictation")
        self.btn_toggle.setObjectName("action_btn")
        self.btn_toggle.setFixedWidth(140)
        self.btn_toggle.clicked.connect(self.dictation_toggled.emit)
        
        card_control_layout.addWidget(self.lbl_status_dot)
        card_control_layout.addSpacing(16)
        card_control_layout.addLayout(status_text_layout)
        card_control_layout.addStretch()
        card_control_layout.addWidget(self.btn_toggle)
        
        content_layout.addWidget(self.card_control)
        
        # Metrics Cards
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        
        self.card_lang = self.create_metric_card("Language", "Auto / English")
        self.card_mode = self.create_metric_card("Model", "Loading...")
        self.card_device = self.create_metric_card("Audio Device", "Initializing...")
        
        metrics_layout.addWidget(self.card_lang)
        metrics_layout.addWidget(self.card_mode)
        metrics_layout.addWidget(self.card_device)
        content_layout.addLayout(metrics_layout)
        
        # Recent Transcriptions
        self.card_history = QFrame()
        self.card_history.setObjectName("card")
        history_layout = QVBoxLayout(self.card_history)
        history_layout.setContentsMargins(24, 24, 24, 24)
        
        header_history_layout = QHBoxLayout()
        header_history_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_history_title = QLabel("RECENT TRANSCRIPTIONS")
        lbl_history_title.setObjectName("metric_lbl")
        
        self.btn_clear_history = QPushButton("Clear")
        self.btn_clear_history.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                border: none;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 12px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #222222;
                border-radius: 4px;
            }
        """)
        self.btn_clear_history.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_clear_history.clicked.connect(self.clear_transcriptions)
        
        header_history_layout.addWidget(lbl_history_title)
        header_history_layout.addStretch()
        header_history_layout.addWidget(self.btn_clear_history)
        
        history_layout.addLayout(header_history_layout)
        history_layout.addSpacing(16)
        
        self.history_list_layout = QVBoxLayout()
        self.history_list_layout.setAlignment(Qt.AlignTop)
        self.history_list_layout.setSpacing(10)
        
        history_widget = QWidget()
        history_widget.setLayout(self.history_list_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(history_widget)
        
        history_layout.addWidget(scroll)
        
        content_layout.addWidget(self.card_history)

    def create_metric_card(self, title, initial_value):
        card = QFrame()
        card.setObjectName("card")
        card.setFixedHeight(95)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("metric_lbl")
        
        lbl_value = QLabel(initial_value)
        lbl_value.setObjectName("metric_val")
        
        layout.addWidget(lbl_title)
        layout.addStretch()
        layout.addWidget(lbl_value)
        
        card.val_label = lbl_value 
        return card

    def update_config_display(self):
        lang = config.get("language", "auto").capitalize()
        if config.get("translate"):
            lang += " (Translated)"
        self.card_lang.val_label.setText(lang)
        
        mode = config.get("model", "tiny").capitalize()
        self.card_mode.val_label.setText(mode)
        
        device = config.get("audio_device", "Default")
        self.card_device.val_label.setText(device)
        
        self.lbl_status_desc.setText(f"Listening on {config.get('audio_device')} • Hotkey: {config.get('hotkey').upper()}")
        
    def set_status(self, status):
        """Update UI based on dictation service status."""
        self.lbl_status_title.setText(f"Engine {status}")
        
        if status == "Listening":
            self.lbl_status_dot.setStyleSheet("color: #F44336; font-size: 20px;") # Red
            self.btn_toggle.setText("Stop Dictation")
        elif status == "Processing":
            self.lbl_status_dot.setStyleSheet("color: #2196F3; font-size: 20px;") # Blue
            self.btn_toggle.setText("Stop Dictation")
        else: # Idle / Loading Error
            self.lbl_status_dot.setStyleSheet("color: #4CAF50; font-size: 20px;") # Green
            self.btn_toggle.setText("Start Dictation")
            
        if "Loading" in status:
            self.lbl_status_dot.setStyleSheet("color: #FFC107; font-size: 20px;") # Yellow

    def add_transcription(self, text):
        """Adds a phrase to the recent transcriptions list."""
        if not text or not text.strip():
            return
            
        self.recent_transcriptions.insert(0, text)
        # Keep only the last 20 transcriptions to save memory
        if len(self.recent_transcriptions) > 20:
            self.recent_transcriptions = self.recent_transcriptions[:20]
            
        self.refresh_history_ui()

    def refresh_history_ui(self):
        """Rebuilds the history list UI."""
        # Clear existing items
        while self.history_list_layout.count():
            item = self.history_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        for t in self.recent_transcriptions:
            lbl = ClickableLabel(t)
            lbl.clicked.connect(self.copy_to_clipboard)
            self.history_list_layout.addWidget(lbl)
            
            # Add separation line
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("border-top: 1px solid #1A1A1A; margin: 0px 8px;")
            self.history_list_layout.addWidget(line)

    def copy_to_clipboard(self, text):
        """Copies text to clipboard and shows feedback."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Show a "Copied!" tooltip at the cursor position
        QToolTip.showText(QCursor.pos(), "Copied to clipboard!", msecShowTime=1500)

    def clear_transcriptions(self):
        """Clears all recent transcriptions."""
        self.recent_transcriptions = []
        self.refresh_history_ui()
