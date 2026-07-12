# Thatwaat Agent AI

A production-ready, modular, scalable desktop AI assistant.

## Tech Stack
- **UI:** PySide6 (Modern, dark-themed GUI)
- **AI Backend:** Ollama (qwen2.5-coder:3b)
- **Computer Vision:** OpenCV, YOLOv8, EasyOCR
- **Voice:** SpeechRecognition, Faster-Whisper, pyttsx3, XTTS v2
- **Automation:** Selenium, PyWhatKit, smtplib
- **Database:** SQLite

## Architecture
The project follows a modular architecture:
- `ui/`: Contains all PySide6 frontend components and page layouts.
- `plugins/`: Directory for dynamically loaded agent skills.
- `memory/`: Contains the SQLite database and JSON states.
- `assets/`: Icons, images, and static files.

## Installation
1. Install Python 3.11+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Ollama is installed and the `qwen2.5-coder:3b` model is downloaded:
   ```bash
   ollama run qwen2.5-coder:3b
   ```

## Running the App
```bash
python main.py
```
