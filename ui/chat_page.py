from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, 
                               QPushButton, QLabel, QScrollArea, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QThread, Signal
from agent import get_agent_response
import markdown

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
    """The main AI Chat interface with welcome card and modern input."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Chat History
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: white;
                font-family: 'Segoe UI', Inter, sans-serif;
                font-size: 15px;
            }
        """)
        layout.addWidget(self.chat_history)
        
        # Insert Welcome Card
        self.show_welcome_message()
        
        # Input Area (Redesigned)
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(5)
        
        # Toolbar (Icons)
        toolbar_layout = QHBoxLayout()
        icons = ["📎", "🎤", "📸", "😋"]
        for icon in icons:
            btn = QPushButton(icon)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #9CA3AF;
                    font-size: 16px;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover { color: white; }
            """)
            toolbar_layout.addWidget(btn)
        toolbar_layout.addStretch()
        input_layout.addLayout(toolbar_layout)
        
        # Text Input & Send Button
        text_row_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 14px;
            }
        """)
        
        self.send_btn = QPushButton("➤ Send")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3B82F6;
                border: none;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover { color: #60A5FA; }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        text_row_layout.addWidget(self.input_field)
        text_row_layout.addWidget(self.send_btn, 0, Qt.AlignmentFlag.AlignBottom)
        
        input_layout.addLayout(text_row_layout)
        layout.addWidget(input_container)

    def show_welcome_message(self):
        welcome_html = """
        <div style='background-color: #1E293B; padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
            <h2 style='color: white; margin-top: 0;'>👋 Welcome to Thatwaat AI</h2>
            <p style='color: #9CA3AF;'>What would you like to do today?</p>
            <table cellpadding="5" cellspacing="0" style="width: 100%;">
                <tr>
                    <td><b style='color: #3B82F6;'>[💻 Write Code]</b></td>
                    <td><b style='color: #8B5CF6;'>[📧 Send Email]</b></td>
                </tr>
                <tr>
                    <td><b style='color: #10B981;'>[👁️ Analyze Image]</b></td>
                    <td><b style='color: #06B6D4;'>[📄 Summarize File]</b></td>
                </tr>
                <tr>
                    <td><b style='color: #F59E0B;'>[🌐 Search Web]</b></td>
                    <td></td>
                </tr>
            </table>
        </div>
        """
        self.chat_history.append(welcome_html)

    def send_message(self):
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        self.input_field.clear()
        self.chat_history.append(f"<div style='text-align:right;'><b style='color:#3B82F6;'>You:</b><br>{text}</div><br>")
        self.chat_history.append("<i style='color:gray;'>Agent is thinking...</i><br>")
        
        self.worker = AgentWorker(text)
        self.worker.finished.connect(self.on_response)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_response(self, text):
        html_text = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        self.chat_history.append(f"<div style='background-color: #111827; padding: 15px; border-radius: 10px;'><b style='color:#10B981;'>Thatwaat AI:</b><br>{html_text}</div><br><br>")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def on_error(self, err):
        self.chat_history.append(f"<b style='color:#EF4444;'>Error:</b> {err}<br><br>")
