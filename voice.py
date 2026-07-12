import numpy as np
import sounddevice as sd
import queue
from faster_whisper import WhisperModel
from PySide6.QtCore import QObject, Signal

class VoiceRecognizer(QObject):
    text_recognized = Signal(str)
    status_updated = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, model_size="tiny.en"):
        super().__init__()
        # Using tiny.en for speed in CPU environments, can be upgraded to base or small
        self.model_size = model_size
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.model = None

    def initialize_model(self):
        if self.model is None:
            self.status_updated.emit("Loading Faster-Whisper...")
            try:
                self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
                self.status_updated.emit("Ready.")
            except Exception as e:
                self.error_occurred.emit(f"Failed to load Whisper: {str(e)}")

    def audio_callback(self, indata, frames, time, status):
        """Sounddevice callback for streaming audio chunks."""
        if self.is_listening:
            self.audio_queue.put(indata.copy())

    def process(self):
        self.initialize_model()
        if not self.model:
            return

        self.is_listening = True
        self.status_updated.emit("Listening...")
        
        sample_rate = 16000
        channels = 1
        
        try:
            with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='float32', callback=self.audio_callback):
                audio_buffer = []
                while self.is_listening:
                    try:
                        chunk = self.audio_queue.get(timeout=0.5)
                        audio_buffer.append(chunk)
                        
                        # Process 3 seconds of audio at a time
                        if sum(len(c) for c in audio_buffer) >= sample_rate * 3:
                            audio_data = np.concatenate(audio_buffer).flatten()
                            audio_buffer = []
                            
                            # VAD threshold check
                            if np.max(np.abs(audio_data)) > 0.02:
                                self.status_updated.emit("Transcribing...")
                                segments, _ = self.model.transcribe(audio_data, beam_size=5, vad_filter=True)
                                text = "".join([segment.text for segment in segments]).strip()
                                if text:
                                    self.text_recognized.emit(text)
                                self.status_updated.emit("Listening...")
                                
                    except queue.Empty:
                        pass
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.status_updated.emit("Stopped.")

    def stop(self):
        self.is_listening = False
