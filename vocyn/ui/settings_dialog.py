from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QCheckBox, QPushButton, QSlider,
    QRadioButton, QButtonGroup, QGroupBox, QScrollArea,
    QWidget, QFrame
)
from PySide6.QtCore import Qt
from vocyn.config import config
from vocyn.audio import get_available_microphones

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings - Vocyn")
        self.setFixedSize(500, 650)
        self.setStyleSheet("""
            QDialog { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
            QLabel { color: #E0E0E0; font-weight: bold; }
            QLabel#desc { color: #AAAAAA; font-weight: normal; font-size: 11px; margin-bottom: 5px; }
            
            QComboBox {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #383838;
                border-radius: 4px;
                padding: 4px 10px;
                min-height: 32px;
            }
            QComboBox:hover { border: 1px solid #505050; }
            QComboBox::drop-down { 
                border: none; 
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #AAAAAA;
                margin-right: 12px;
                margin-top: 2px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #1E1E1E;
                color: #FFFFFF;
                selection-background-color: #383838;
                border: 1px solid #383838;
                outline: none;
                padding: 5px 0px;
            }

            QScrollBar:vertical {
                border: none;
                background: #1E1E1E;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #383838;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QPushButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #383838;
                border-radius: 4px;
                padding: 6px 15px;
                min-height: 28px;
            }
            QPushButton:hover { background-color: #2C2C2C; border: 1px solid #505050; }
            QPushButton#save { background-color: white; color: black; font-weight: bold; border: none; }
            QPushButton#save:hover { background-color: #E0E0E0; }

            QCheckBox { spacing: 10px; color: #E0E0E0; }
            QCheckBox::indicator { width: 40px; height: 20px; border-radius: 10px; background-color: #383838; }
            QCheckBox::indicator:checked { background-color: #4CAF50; }
            
            QRadioButton { spacing: 10px; color: #E0E0E0; }
            QRadioButton::indicator { width: 12px; height: 12px; border-radius: 6px; background-color: #383838; border: 1px solid #505050; }
            QRadioButton::indicator:checked { background-color: #4CAF50; border: 1px solid #4CAF50; }
            QRadioButton::indicator:hover { border: 1px solid #808080; }
            
            QSlider::groove:horizontal {
                border: 1px solid #383838;
                height: 4px;
                background: #383838;
                margin: 2px 0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #2196F3;
                width: 14px;
                height: 14px;
                margin: -6px 0;
                border-radius: 7px;
            }
        """)
        
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("#container { background-color: transparent; }")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(18)
        
        # Audio Device
        self.create_section_label(layout, "Audio Device", "Select your microphone for dictation.")
        self.combo_mic = QComboBox()
        self.combo_mic.addItems(get_available_microphones())
        layout.addWidget(self.combo_mic)
        
        # Language
        self.create_section_label(layout, "Input Language", "Spoken language to detect.")
        self.combo_lang = QComboBox()
        
        # Whisper 99 languages + auto
        self.whisper_languages = {
            "auto": "Auto Detect",
            "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "as": "Assamese", "az": "Azerbaijani",
            "ba": "Bashkir", "be": "Belarusian", "bg": "Bulgarian", "bn": "Bengali", "bo": "Tibetan",
            "br": "Breton", "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh",
            "da": "Danish", "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
            "et": "Estonian", "eu": "Basque", "fa": "Persian", "fi": "Finnish", "fo": "Faroese",
            "fr": "French", "gl": "Galician", "gu": "Gujarati", "ha": "Hausa", "haw": "Hawaiian",
            "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian", "hy": "Armenian", "id": "Indonesian",
            "is": "Icelandic", "it": "Italian", "iw": "Hebrew", "ja": "Japanese", "jw": "Javanese",
            "ka": "Georgian", "kk": "Kazakh", "km": "Khmer", "kn": "Kannada", "ko": "Korean",
            "la": "Latin", "lb": "Luxembourgish", "ln": "Lingala", "lo": "Lao", "lt": "Lithuanian",
            "lv": "Latvian", "mg": "Malagasy", "mi": "Maori", "mk": "Macedonian", "ml": "Malayalam",
            "mn": "Mongolian", "mr": "Marathi", "ms": "Malay", "mt": "Maltese", "my": "Burmese",
            "ne": "Nepali", "nl": "Dutch", "nn": "Nynorsk", "no": "Norwegian", "oc": "Occitan",
            "pa": "Punjabi", "pl": "Polish", "ps": "Pashto", "pt": "Portuguese", "ro": "Romanian",
            "ru": "Russian", "sa": "Sanskrit", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak",
            "sl": "Slovenian", "sn": "Shona", "so": "Somali", "sq": "Albanian", "sr": "Serbian",
            "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", "ta": "Tamil", "te": "Telugu",
            "tg": "Tajik", "th": "Thai", "tk": "Turkmen", "tl": "Tagalog", "tr": "Turkish",
            "tt": "Tatar", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese",
            "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese"
        }
        
        for val, lbl in self.whisper_languages.items():
            self.combo_lang.addItem(lbl, userData=val)
        layout.addWidget(self.combo_lang)
        
        layout.addSpacing(25) # Gap between sections
        
        # Translation Mode
        self.create_section_label(layout, "Transcription Mode", "Choose if you want to transcribe or translate speech.")
        
        self.radio_group = QButtonGroup(self)
        self.radio_transcribe = QRadioButton("Transcribe only (Original language)")
        self.radio_translate = QRadioButton("Translation")
        
        self.radio_group.addButton(self.radio_transcribe)
        self.radio_group.addButton(self.radio_translate)
        
        self.radio_transcribe.toggled.connect(self.on_mode_changed)
        self.radio_translate.toggled.connect(self.on_mode_changed)
        
        layout.addWidget(self.radio_transcribe)
        
        self.trans_container = QGroupBox()
        self.trans_container.setStyleSheet("QGroupBox { border: none; margin-top: 0px; }")
        trans_container_layout = QHBoxLayout(self.trans_container)
        trans_container_layout.setContentsMargins(0, 2, 0, 0)
        
        trans_container_layout.addWidget(self.radio_translate)
        
        self.combo_target_lang = QComboBox()
        # Full list for translation
        for val, lbl in self.whisper_languages.items():
            if val != "auto":
                self.combo_target_lang.addItem(lbl, userData=val)
        
        trans_container_layout.addWidget(self.combo_target_lang)
        trans_container_layout.addStretch()
        layout.addWidget(self.trans_container)
        
        # Model
        self.create_section_label(layout, "Transcription Model", "Larger models are more accurate but slower.")
        self.combo_model = QComboBox()
        self.combo_model.addItems(["tiny", "base", "small"])
        layout.addWidget(self.combo_model)
        
        # Silence Timeout
        self.create_section_label(layout, "Silence Timeout (sec)", "Delay before transcribing speech.")
        self.slider_timeout = QSlider(Qt.Horizontal)
        self.slider_timeout.setRange(8, 25) # 0.8 to 2.5
        self.slider_timeout.setSingleStep(1)
        
        self.lbl_timeout_val = QLabel("1.5s")
        self.slider_timeout.valueChanged.connect(
            lambda v: self.lbl_timeout_val.setText(f"{v/10.0}s")
        )
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.slider_timeout)
        h_layout.addWidget(self.lbl_timeout_val)
        layout.addLayout(h_layout)
        
        # Hotkey (Simple placeholder, normally would hook keyboard library)
        self.create_section_label(layout, "Global Hotkey", "Shortcut to toggle recording.")
        self.combo_hotkey = QComboBox()
        self.combo_hotkey.addItems([
            "ctrl+alt+space",
            "ctrl+shift+space",
            "alt+space",
            "shift+f12"
        ])
        self.combo_hotkey.setEditable(True)
        layout.addWidget(self.combo_hotkey)
        
        # Run in tray
        self.check_tray = QCheckBox("Run minimized to tray")
        layout.addWidget(self.check_tray)
        
        layout.addStretch()
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
        # Save/Cancel
        btn_container = QWidget()
        btn_container.setObjectName("button_container")
        btn_container.setStyleSheet("#button_container { background-color: #1A1A1A; border-top: 1px solid #2A2A2A; }")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(20, 15, 20, 15)
        
        btn_save = QPushButton("Save")
        btn_save.setObjectName("save")
        btn_save.setMinimumWidth(80)
        btn_save.clicked.connect(self.save_settings)
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setMinimumWidth(80)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        main_layout.addWidget(btn_container)
        
    def create_section_label(self, layout, title, desc):
        lbl_title = QLabel(title)
        lbl_desc = QLabel(desc)
        lbl_desc.setObjectName("desc")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)

    def on_mode_changed(self):
        is_translate = self.radio_translate.isChecked()
        self.combo_target_lang.setVisible(is_translate)

    def load_current_settings(self):
        mic = config.get("audio_device")
        idx = self.combo_mic.findText(mic)
        if idx >= 0: self.combo_mic.setCurrentIndex(idx)
        
        lang = config.get("language")
        idx = self.combo_lang.findData(lang)
        if idx >= 0: self.combo_lang.setCurrentIndex(idx)
        
        is_translate = config.get("translate", False)
        if is_translate:
            self.radio_translate.setChecked(True)
        else:
            self.radio_transcribe.setChecked(True)
            
        target_lang = config.get("target_language", "en")
        idx = self.combo_target_lang.findData(target_lang)
        if idx >= 0: self.combo_target_lang.setCurrentIndex(idx)
        self.combo_target_lang.setVisible(is_translate)
        
        model = config.get("model")
        idx = self.combo_model.findText(model)
        if idx >= 0: self.combo_model.setCurrentIndex(idx)
        
        timeout = int(config.get("silence_timeout", 1.5) * 10)
        self.slider_timeout.setValue(timeout)
        
        hotkey = config.get("hotkey")
        self.combo_hotkey.setCurrentText(hotkey)
        
        self.check_tray.setChecked(config.get("run_minimized", True))
        
    def save_settings(self):
        config.set("audio_device", self.combo_mic.currentText())
        config.set("language", self.combo_lang.currentData())
        config.set("translate", self.radio_translate.isChecked())
        config.set("target_language", self.combo_target_lang.currentData())
        config.set("model", self.combo_model.currentText())
        config.set("silence_timeout", self.slider_timeout.value() / 10.0)
        config.set("hotkey", self.combo_hotkey.currentText().lower())
        config.set("run_minimized", self.check_tray.isChecked())
        
        self.accept()
