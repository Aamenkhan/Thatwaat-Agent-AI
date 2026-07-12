import os
from PySide6.QtCore import QObject, Signal

class VoiceSynthesizer(QObject):
    status_updated = Signal(str)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.tts = None
        
    def initialize_model(self):
        if self.tts is None:
            self.status_updated.emit("Loading XTTS v2 (This takes time)...")
            try:
                from TTS.api import TTS
                self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
                self.status_updated.emit("XTTS v2 loaded.")
            except Exception as e:
                self.error_occurred.emit(f"Failed to load XTTS: {str(e)}")

    def process(self):
        text = getattr(self, "text", "")
        speaker_wav = getattr(self, "speaker_wav", None)
        language = getattr(self, "language", "en")
        speed = getattr(self, "speed", 1.0)
        volume = getattr(self, "volume", 1.0)
        
        self.initialize_model()
        if not self.tts:
            return
            
        self.status_updated.emit("Synthesizing audio...")
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np

            output_path = "temp_output.wav"
            
            if speaker_wav and os.path.exists(speaker_wav):
                self.tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_path)
            else:
                # If no speaker_wav, XTTS v2 requires one. We will use a default dummy or error out.
                # Since XTTS v2 explicitly requires a speaker sample for cloning, we must enforce it.
                self.error_occurred.emit("XTTS v2 requires a speaker WAV sample for cloning.")
                return
            
            data, fs = sf.read(output_path)
            
            # Apply volume and speed
            data = data * volume
            
            self.status_updated.emit("Playing...")
            sd.play(data, int(fs * speed))
            sd.wait()
            
            self.status_updated.emit("Ready.")
            
        except Exception as e:
            self.error_occurred.emit(str(e))
