from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                               QComboBox, QSlider, QFrame, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread
from voice import VoiceRecognizer
from voice_clone import VoiceSynthesizer

class VoicePage(QWidget):
    """The Voice Assistant and Cloning interface."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Voice & Audio")
        header.setStyleSheet("color: white; font-size: 24px; font-weight: bold; border: none;")
        layout.addWidget(header)
        
        # --- Card 1: Speech Recognition ---
        rec_card = QFrame()
        rec_card.setStyleSheet("QFrame { background-color: #1E293B; border-radius: 12px; }")
        rec_layout = QVBoxLayout(rec_card)
        
        rec_title = QLabel("Speech Recognition (Faster-Whisper)")
        rec_title.setStyleSheet("color: #9CA3AF; font-weight: bold; border: none;")
        rec_layout.addWidget(rec_title)
        
        self.status_label = QLabel("Waiting to start...")
        self.status_label.setStyleSheet("color: #06B6D4; font-size: 14px; font-style: italic; border: none;")
        rec_layout.addWidget(self.status_label)
        
        rec_btn_layout = QHBoxLayout()
        self.btn_listen = QPushButton("🎤 Start Listening")
        self.btn_stop = QPushButton("⏹️ Stop")
        
        for btn in [self.btn_listen, self.btn_stop]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6; color: white; padding: 10px 20px;
                    border-radius: 8px; font-weight: bold; border: none;
                }
                QPushButton:hover { background-color: #2563EB; }
            """)
            rec_btn_layout.addWidget(btn)
        
        # Override stop button color to red
        self.btn_stop.setStyleSheet(self.btn_stop.styleSheet().replace("#3B82F6", "#EF4444").replace("#2563EB", "#DC2626"))
        
        rec_layout.addLayout(rec_btn_layout)
        layout.addWidget(rec_card)

        # --- Card 2: Voice Cloning ---
        clone_card = QFrame()
        clone_card.setStyleSheet("QFrame { background-color: #1E293B; border-radius: 12px; }")
        clone_layout = QVBoxLayout(clone_card)
        
        clone_title = QLabel("Voice Synthesis & Cloning (XTTS v2)")
        clone_title.setStyleSheet("color: #9CA3AF; font-weight: bold; border: none;")
        clone_layout.addWidget(clone_title)
        
        self.voice_selector = QComboBox()
        self.voice_selector.addItems(["Default AI Voice", "Anish (Cloned)", "Female Assistant"])
        self.voice_selector.setStyleSheet("""
            QComboBox {
                background-color: #111827; color: white; border-radius: 5px;
                padding: 8px; border: 1px solid rgba(255,255,255,0.1);
            }
            QComboBox QAbstractItemView {
                background-color: #111827; color: white; selection-background-color: #3B82F6;
            }
        """)
        clone_layout.addWidget(self.voice_selector)
        
        clone_btn_layout = QHBoxLayout()
        self.btn_import_voice = QPushButton("📁 Import Voice Sample")
        self.btn_test_voice = QPushButton("🔊 Test Voice")
        
        for btn in [self.btn_import_voice, self.btn_test_voice]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #111827; color: #9CA3AF; padding: 10px 20px;
                    border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);
                }
                QPushButton:hover { color: white; border: 1px solid #3B82F6; }
            """)
            clone_btn_layout.addWidget(btn)
        
        clone_layout.addLayout(clone_btn_layout)
        layout.addWidget(clone_card)

        # --- Card 3: Audio Settings ---
        settings_card = QFrame()
        settings_card.setStyleSheet("QFrame { background-color: #1E293B; border-radius: 12px; }")
        settings_layout = QVBoxLayout(settings_card)
        
        settings_title = QLabel("Playback Settings")
        settings_title.setStyleSheet("color: #9CA3AF; font-weight: bold; border: none;")
        settings_layout.addWidget(settings_title)
        
        speed_layout = QHBoxLayout()
        speed_lbl = QLabel("Speed")
        speed_lbl.setStyleSheet("color: white; border: none;")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(50, 200) # 0.5x to 2.0x
        self.speed_slider.setValue(100)
        speed_layout.addWidget(speed_lbl)
        speed_layout.addWidget(self.speed_slider)
        settings_layout.addLayout(speed_layout)
        
        volume_layout = QHBoxLayout()
        vol_lbl = QLabel("Volume")
        vol_lbl.setStyleSheet("color: white; border: none;")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        volume_layout.addWidget(vol_lbl)
        volume_layout.addWidget(self.volume_slider)
        settings_layout.addLayout(volume_layout)
        
        layout.addWidget(settings_card)
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # --- Function Connections ---
        self.btn_listen.clicked.connect(self.start_listening)
        self.btn_stop.clicked.connect(self.stop_listening)
        self.btn_import_voice.clicked.connect(self.import_voice_sample)
        self.btn_test_voice.clicked.connect(self.test_voice_clone)
        
        self.active_threads = []
        self.speaker_wav_path = None
        self.btn_stop.setEnabled(False)

    def start_listening(self):
        self.btn_listen.setEnabled(False)
        self.btn_stop.setEnabled(True)
        
        self.rec_thread = QThread()
        self.recognizer = VoiceRecognizer()
        self.recognizer.moveToThread(self.rec_thread)
        
        self.rec_thread.started.connect(self.recognizer.process)
        self.recognizer.text_recognized.connect(self.on_speech_recognized)
        self.recognizer.status_updated.connect(self.status_label.setText)
        self.recognizer.error_occurred.connect(self.on_voice_error)
        
        self.rec_thread.start()
        self.active_threads.append(self.rec_thread)
        self.rec_thread.finished.connect(lambda: self.active_threads.remove(self.rec_thread) if self.rec_thread in self.active_threads else None)

    def stop_listening(self):
        if hasattr(self, 'recognizer'):
            self.recognizer.stop()
        self.btn_listen.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def on_speech_recognized(self, text):
        from PySide6.QtWidgets import QMessageBox
        # Display the recognized text, or send to chat
        self.status_label.setText(f"Recognized: {text}")
        print(f"Recognized: {text}")

    def import_voice_sample(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select WAV Sample", "", "Audio Files (*.wav)")
        if file_path:
            import os
            import shutil
            os.makedirs("voices", exist_ok=True)
            filename = os.path.basename(file_path)
            dest = os.path.join("voices", filename)
            shutil.copy(file_path, dest)
            self.speaker_wav_path = dest
            self.voice_selector.addItem(filename)
            self.voice_selector.setCurrentText(filename)
            QMessageBox.information(self, "Success", f"Voice sample {filename} imported successfully!")

    def test_voice_clone(self):
        if not self.speaker_wav_path:
            QMessageBox.warning(self, "Error", "Please import a WAV voice sample first for XTTS v2.")
            return
            
        speed = self.speed_slider.value() / 100.0
        volume = self.volume_slider.value() / 100.0
        
        self.synth_thread = QThread()
        self.synthesizer = VoiceSynthesizer()
        self.synthesizer.moveToThread(self.synth_thread)
        
        # Avoid lambda to ensure process runs in the worker thread
        self.synthesizer.text = "Hello, this is a cloned voice test."
        self.synthesizer.speaker_wav = self.speaker_wav_path
        self.synthesizer.language = "en"
        self.synthesizer.speed = speed
        self.synthesizer.volume = volume
        
        self.synth_thread.started.connect(self.synthesizer.process)
        self.synthesizer.status_updated.connect(lambda s: print(f"Synth: {s}"))
        self.synthesizer.error_occurred.connect(self.on_voice_error)
        
        self.synth_thread.start()
        self.active_threads.append(self.synth_thread)
        self.synth_thread.finished.connect(lambda: self.active_threads.remove(self.synth_thread) if self.synth_thread in self.active_threads else None)

    def on_voice_error(self, err):
        QMessageBox.critical(self, "Voice Error", err)

