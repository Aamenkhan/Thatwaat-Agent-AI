from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout, QPushButton, QLabel, QScrollArea
from PySide6.QtCore import Qt, QThread, Signal
from agent import get_agent_response

class AgentWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            response = get_agent_response(self.prompt)
            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e))

class ChatPage(QWidget):
    """The main AI Chat interface."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Chat History
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: rgba(17, 24, 39, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
                color: white;
                font-family: 'Segoe UI', Inter, sans-serif;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.chat_history)
        
        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask anything...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 10px 20px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
            
        self.input_field.clear()
        self.chat_history.append(f"<b style='color:#3B82F6;'>You:</b> {text}<br>")
        self.chat_history.append("<i style='color:gray;'>Agent is thinking...</i><br>")
        
        self.worker = AgentWorker(text)
        self.worker.finished.connect(self.on_response)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_response(self, text):
        self.chat_history.append(f"<b style='color:#10B981;'>Thatwaat AI:</b> {text}<br><br>")
        # Scroll to bottom
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def on_error(self, err):
        self.chat_history.append(f"<b style='color:#EF4444;'>Error:</b> {err}<br><br>")
