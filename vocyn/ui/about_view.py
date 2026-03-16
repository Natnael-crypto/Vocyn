from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PySide6.QtCore import Qt

class AboutView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #000000; color: #E0E0E0; font-family: 'Inter', 'Segoe UI', sans-serif; }
            QLabel { color: #E0E0E0; }
            QLabel#title { font-size: 32px; font-weight: bold; color: #FFFFFF; }
            QLabel#subtitle { font-size: 16px; color: #888888; margin-bottom: 20px; }
            QLabel#footer { font-size: 12px; color: #666666; }
            QFrame#card {
                background-color: #000000;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 60, 40, 60)
        layout.setAlignment(Qt.AlignCenter)

        # Title
        lbl_title = QLabel("Vocyn")
        lbl_title.setObjectName("title")
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)

        # Subtitle
        lbl_subtitle = QLabel("Local Voice Dictation Tool")
        lbl_subtitle.setObjectName("subtitle")
        lbl_subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_subtitle)
        
        layout.addSpacing(20)

        # Body
        lbl_body = QLabel("v1.0")
        lbl_body.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px 12px; background-color: #222; border-radius: 12px;")
        lbl_body.setAlignment(Qt.AlignCenter)
        
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(lbl_body)
        h_layout.addStretch()
        layout.addLayout(h_layout)

        layout.addStretch()

        # Footer
        lbl_footer = QLabel(
            "Powered by Qt, Faster Whisper, CTranslate2, and modern open-source technology."
        )
        lbl_footer.setObjectName("footer")
        lbl_footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_footer)
        
        main_layout.addStretch()
        main_layout.addWidget(card)
        main_layout.addStretch()
