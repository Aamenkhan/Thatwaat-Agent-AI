from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                               QComboBox, QSlider, QFrame, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox, QCheckBox, QListWidget)
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
        
        chk_layout = QHBoxLayout()
        self.chk_ptt = QCheckBox("Push-to-Talk")
        self.chk_ptt.setStyleSheet("color: white; border: none;")
        self.chk_wake = QCheckBox('Wake Word ("Hey Thatwaat")')
        self.chk_wake.setStyleSheet("color: white; border: none;")
        chk_layout.addWidget(self.chk_ptt)
        chk_layout.addWidget(self.chk_wake)
        rec_layout.addLayout(chk_layout)
        
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

        # --- Card 2: Voice Profile Manager ---
        clone_card = QFrame()
        clone_card.setStyleSheet("QFrame { background-color: #1E293B; border-radius: 12px; }")
        clone_layout = QVBoxLayout(clone_card)
        
        clone_title = QLabel("🎙️ Voice Profile Manager")
        clone_title.setStyleSheet("color: #9CA3AF; font-weight: bold; border: none;")
        clone_layout.addWidget(clone_title)
        
        self.voice_list = QListWidget()
        self.voice_list.addItems(["Default AI", "My Voice", "Female", "Male"])
        self.voice_list.setStyleSheet("""
            QListWidget {
                background-color: #111827; color: white; border-radius: 5px;
                padding: 8px; border: 1px solid rgba(255,255,255,0.1);
            }
            QListWidget::item:selected {
                background-color: #3B82F6; color: white; border-radius: 3px;
            }
        """)
        self.voice_list.setFixedHeight(100)
        clone_layout.addWidget(self.voice_list)
        
        clone_btn_layout1 = QHBoxLayout()
        self.btn_import_wav = QPushButton("Import WAV")
        self.btn_import_mp3 = QPushButton("Import MP3")
        self.btn_record_voice = QPushButton("Record Voice")
        
        clone_btn_layout2 = QHBoxLayout()
        self.btn_train_voice = QPushButton("Train Voice")
        self.btn_delete_voice = QPushButton("Delete Voice")
        
        all_clone_btns = [self.btn_import_wav, self.btn_import_mp3, self.btn_record_voice, self.btn_train_voice, self.btn_delete_voice]
        for btn in all_clone_btns:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #111827; color: #9CA3AF; padding: 8px 10px;
                    border-radius: 6px; border: 1px solid rgba(255,255,255,0.2);
                }
                QPushButton:hover { color: white; border: 1px solid #3B82F6; }
            """)
        
        clone_btn_layout1.addWidget(self.btn_import_wav)
        clone_btn_layout1.addWidget(self.btn_import_mp3)
        clone_btn_layout1.addWidget(self.btn_record_voice)
        clone_btn_layout2.addWidget(self.btn_train_voice)
        clone_btn_layout2.addWidget(self.btn_delete_voice)
        
        clone_layout.addLayout(clone_btn_layout1)
        clone_layout.addLayout(clone_btn_layout2)
        layout.addWidget(clone_card)

        # --- Card 3: Audio Export ---
        export_card = QFrame()
        export_card.setStyleSheet("QFrame { background-color: #1E293B; border-radius: 12px; }")
        export_layout = QVBoxLayout(export_card)
        
        export_title = QLabel("🎵 Audio Export")
        export_title.setStyleSheet("color: #9CA3AF; font-weight: bold; border: none;")
        export_layout.addWidget(export_title)
        
        export_btn_layout = QHBoxLayout()
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_save_mp3 = QPushButton("💾 Save as MP3")
        self.btn_save_wav = QPushButton("💾 Save as WAV")
        self.btn_share = QPushButton("📤 Share")
        
        for btn in [self.btn_play, self.btn_pause, self.btn_save_mp3, self.btn_save_wav, self.btn_share]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #111827; color: white; padding: 10px;
                    border-radius: 8px; border: 1px solid #3B82F6; font-weight: bold;
                }
                QPushButton:hover { background-color: #3B82F6; }
            """)
            export_btn_layout.addWidget(btn)
        
        export_layout.addLayout(export_btn_layout)
        layout.addWidget(export_card)

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
        
        self.btn_import_wav.clicked.connect(self.import_wav_sample)
        self.btn_import_mp3.clicked.connect(self.import_mp3_sample)
        self.btn_record_voice.clicked.connect(self.record_voice)
        self.btn_train_voice.clicked.connect(self.train_voice)
        self.btn_delete_voice.clicked.connect(self.delete_voice)
        
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_save_mp3.clicked.connect(self.save_as_mp3)
        self.btn_save_wav.clicked.connect(self.save_as_wav)
        self.btn_share.clicked.connect(self.share_audio)
        
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

    def on_voice_error(self, err):
        QMessageBox.critical(self, "Voice Error", err)

    def import_wav_sample(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select WAV Sample", "", "Audio Files (*.wav)")
        if file_path:
            import os
            import shutil
            os.makedirs("voices", exist_ok=True)
            filename = os.path.basename(file_path)
            dest = os.path.join("voices", filename)
            shutil.copy(file_path, dest)
            self.speaker_wav_path = dest
            self.voice_list.addItem(filename)
            
            # Auto-select the newly added item
            items = self.voice_list.findItems(filename, Qt.MatchExactly)
            if items:
                self.voice_list.setCurrentItem(items[0])
                
            QMessageBox.information(self, "Success", f"Voice sample {filename} imported successfully!")

    def import_mp3_sample(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MP3 Sample", "", "Audio Files (*.mp3)")
        if file_path:
            import os
            try:
                from pydub import AudioSegment
                os.makedirs("voices", exist_ok=True)
                filename = os.path.basename(file_path).replace(".mp3", ".wav")
                dest = os.path.join("voices", filename)
                
                audio = AudioSegment.from_mp3(file_path)
                audio.export(dest, format="wav")
                
                self.speaker_wav_path = dest
                self.voice_list.addItem(filename)
                
                items = self.voice_list.findItems(filename, Qt.MatchExactly)
                if items:
                    self.voice_list.setCurrentItem(items[0])
                    
                QMessageBox.information(self, "Success", f"MP3 converted to WAV: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import MP3. Ensure ffmpeg is installed.\nError: {str(e)}")
        
    def record_voice(self):
        QMessageBox.information(self, "Record", "Recording will start for 5 seconds when you click OK.")
        import sounddevice as sd
        import numpy as np
        import soundfile as sf
        import os
        import datetime
        
        fs = 44100
        duration = 5
        
        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            self.status_label.setText("Recording for 5 seconds...")
            sd.wait()
            self.status_label.setText("Recording finished.")
            
            os.makedirs("voices", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recorded_{timestamp}.wav"
            dest = os.path.join("voices", filename)
            
            sf.write(dest, recording, fs)
            
            self.speaker_wav_path = dest
            self.voice_list.addItem(filename)
            items = self.voice_list.findItems(filename, Qt.MatchExactly)
            if items:
                self.voice_list.setCurrentItem(items[0])
                
            QMessageBox.information(self, "Success", f"Voice recorded to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        
    def train_voice(self):
        QMessageBox.information(self, "Train Voice", "XTTS v2 is a zero-shot cloner.\n\n'Training' happens instantly when you select a Voice Profile. Just record or import a sample, select it, and you're good to go!")
        
    def delete_voice(self):
        selected = self.voice_list.currentItem()
        if selected:
            # Here we would also delete the actual file
            self.voice_list.takeItem(self.voice_list.row(selected))
            
    def play_audio(self):
        selected_items = self.voice_list.selectedItems()
        if not selected_items and not self.speaker_wav_path:
            QMessageBox.warning(self, "Error", "Please select a Voice Profile or Import a WAV sample first.")
            return
            
        speed = self.speed_slider.value() / 100.0
        volume = self.volume_slider.value() / 100.0
        
        self.synth_thread = QThread()
        self.synthesizer = VoiceSynthesizer()
        self.synthesizer.moveToThread(self.synth_thread)
        
        self.synthesizer.text = "Hello, this is a cloned voice test."
        self.synthesizer.speaker_wav = self.speaker_wav_path # Update this later to use selected item path
        self.synthesizer.language = "en"
        self.synthesizer.speed = speed
        self.synthesizer.volume = volume
        
        self.synth_thread.started.connect(self.synthesizer.process)
        self.synthesizer.status_updated.connect(lambda s: print(f"Synth: {s}"))
        self.synthesizer.error_occurred.connect(self.on_voice_error)
        
        self.synth_thread.start()
        self.active_threads.append(self.synth_thread)
        self.synth_thread.finished.connect(lambda: self.active_threads.remove(self.synth_thread) if self.synth_thread in self.active_threads else None)
    def pause_audio(self):
        QMessageBox.information(self, "Info", "Audio paused.")
        
    def save_as_mp3(self):
        import os
        if not os.path.exists("temp_output.wav"):
            QMessageBox.warning(self, "No Output", "Generate a voice clone first before saving.")
            return
            
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Audio", "cloned_voice.mp3", "Audio Files (*.mp3)")
        if save_path:
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_wav("temp_output.wav")
                audio.export(save_path, format="mp3")
                QMessageBox.information(self, "Success", f"Audio saved to:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save MP3. Make sure ffmpeg is installed.\nError: {str(e)}")

    def save_as_wav(self):
        import os
        import shutil
        if not os.path.exists("temp_output.wav"):
            QMessageBox.warning(self, "No Output", "Generate a voice clone first before saving.")
            return
            
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Audio", "cloned_voice.wav", "Audio Files (*.wav)")
        if save_path:
            try:
                shutil.copy("temp_output.wav", save_path)
                QMessageBox.information(self, "Success", f"Audio saved to:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def share_audio(self):
        QMessageBox.information(self, "Info", "Share feature coming soon.")

