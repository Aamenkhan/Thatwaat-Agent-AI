from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextBrowser, QTextEdit, QHBoxLayout, 
                               QPushButton, QLabel, QScrollArea, QFrame, QGridLayout, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, QObject, Signal, QTimer
from agent import get_agent_response_stream
import markdown
import requests
import re
import uuid
from datetime import datetime
from pygments.formatters import HtmlFormatter

class AgentWorker(QObject):
    token_received = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.is_running = True

    def process(self):
        try:
            full_response = ""
            for token in get_agent_response_stream(self.prompt):
                if not self.is_running:
                    break
                full_response += token
                self.token_received.emit(token)
            self.finished.emit(full_response)
        except Exception as e:
            self.error.emit(str(e))
            
    def stop(self):
        self.is_running = False

class DropTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
        else:
            super().dragEnterEvent(e)
            
    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                file_path = url.toLocalFile()
                current_text = self.toPlainText()
                self.setText(f"{current_text}\n[Attached File: {file_path}]\n")
            e.acceptProposedAction()
        else:
            super().dropEvent(e)

class ChatPage(QWidget):
    """The main AI Chat interface with welcome card and modern input."""
    def __init__(self):
        super().__init__()
        self.chat_html_history = ""
        self.current_reply = ""
        self.code_blocks = {}
        self.last_prompt = ""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Chat History
        self.chat_history = QTextBrowser()
        self.chat_history.setReadOnly(True)
        self.chat_history.setOpenLinks(False)
        self.chat_history.anchorClicked.connect(self.handle_link_click)
        
        # Apply Pygments CSS for code highlighting
        css = HtmlFormatter(style="monokai").get_style_defs('.codehilite')
        self.chat_history.document().setDefaultStyleSheet(css + """
            QTextBrowser {
                background-color: transparent;
                border: none;
                color: white;
                font-family: 'Segoe UI', Inter, sans-serif;
                font-size: 15px;
            }
            a { color: #3B82F6; text-decoration: none; }
            code { background-color: #2D3748; padding: 2px 4px; border-radius: 4px; }
            pre { background-color: #1E293B; padding: 10px; border-radius: 8px; }
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
        
        # Toolbar (Icons & Status)
        toolbar_layout = QHBoxLayout()
        
        self.btn_attach = QPushButton("📎")
        self.btn_voice = QPushButton("🎤")
        self.btn_camera = QPushButton("📸")
        self.btn_emoji = QPushButton("😋")
        
        for btn in [self.btn_attach, self.btn_voice, self.btn_camera, self.btn_emoji]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #9CA3AF;
                    font-size: 16px;
                    border: none;
                    padding: 5px;
                }
                QPushButton:hover { color: white; background-color: rgba(255, 255, 255, 0.1); border-radius: 5px; }
            """)
            toolbar_layout.addWidget(btn)
            
        self.btn_attach.clicked.connect(self.action_attach_file)
        self.btn_voice.clicked.connect(self.action_voice_input)
        self.btn_camera.clicked.connect(self.action_camera)
        self.btn_emoji.clicked.connect(self.action_emoji)
        
        toolbar_layout.addStretch()
        
        self.lbl_status = QLabel("Checking connection...")
        self.lbl_status.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: bold;")
        toolbar_layout.addWidget(self.lbl_status)
        
        input_layout.addLayout(toolbar_layout)
        
        self.conn_timer = QTimer(self)
        self.conn_timer.timeout.connect(self.check_connection)
        self.conn_timer.start(5000)
        self.check_connection()
        
        # Text Input & Send Button
        text_row_layout = QHBoxLayout()
        self.input_field = DropTextEdit()
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
        
        self.btn_history = QPushButton("🔍 History")
        self.btn_history.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_history.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #8B5CF6; border: none; font-weight: bold; padding: 10px;
            }
            QPushButton:hover { color: #A78BFA; }
        """)
        self.btn_history.clicked.connect(self.action_history)
        
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
        
        self.btn_regenerate = QPushButton("🔄 Regenerate")
        self.btn_regenerate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_regenerate.setStyleSheet(self.send_btn.styleSheet().replace("#3B82F6", "#10B981").replace("#60A5FA", "#34D399"))
        self.btn_regenerate.clicked.connect(self.regenerate_message)
        self.btn_regenerate.hide()
        
        text_row_layout.addWidget(self.input_field)
        text_row_layout.addWidget(self.btn_history, 0, Qt.AlignmentFlag.AlignBottom)
        text_row_layout.addWidget(self.btn_regenerate, 0, Qt.AlignmentFlag.AlignBottom)
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
                    <td><a href="action:write_code" style='color: #3B82F6; text-decoration: none;'><b>[💻 Write Code]</b></a></td>
                    <td><a href="action:send_email" style='color: #8B5CF6; text-decoration: none;'><b>[📧 Send Email]</b></a></td>
                </tr>
                <tr>
                    <td><a href="action:analyze_image" style='color: #10B981; text-decoration: none;'><b>[👁️ Analyze Image]</b></a></td>
                    <td><a href="action:summarize_file" style='color: #06B6D4; text-decoration: none;'><b>[📄 Summarize File]</b></a></td>
                </tr>
                <tr>
                    <td><a href="action:search_web" style='color: #F59E0B; text-decoration: none;'><b>[🌐 Search Web]</b></a></td>
                    <td></td>
                </tr>
            </table>
        </div>
        """
        self.chat_html_history += welcome_html
        self.chat_history.setHtml(self.chat_html_history)

    def check_connection(self):
        try:
            r = requests.get("http://localhost:11434", timeout=1)
            if r.status_code == 200:
                self.lbl_status.setText("🟢 Ollama Connected")
            else:
                self.lbl_status.setText("🔴 Ollama Error")
        except:
            self.lbl_status.setText("🔴 Ollama Offline")

    def process_markdown(self, text):
        def code_replacer(match):
            code_raw = match.group(2)
            code_id = str(uuid.uuid4())
            self.code_blocks[code_id] = code_raw
            header = f"<div style='text-align:right; margin-bottom:-15px;'><a href='copy:{code_id}' style='color:#3B82F6; text-decoration:none; font-size:12px; font-weight:bold;'>[📋 Copy Code]</a></div>\n\n"
            return header + match.group(0)
            
        processed_text = re.sub(r'(```\w*\n)(.*?)```', code_replacer, text, flags=re.DOTALL)
        return markdown.markdown(processed_text, extensions=['fenced_code', 'tables', 'codehilite'])

    def handle_link_click(self, url):
        action = url.toString()
        if action.startswith("copy:"):
            code_id = action.split("copy:")[1]
            if code_id in self.code_blocks:
                from PySide6.QtGui import QGuiApplication
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(self.code_blocks[code_id])
                self.send_btn.setText("📋 Copied!")
                QTimer.singleShot(2000, lambda: self.send_btn.setText("➤ Send") if self.send_btn.text() == "📋 Copied!" else None)
            return
            
        prompts = {
            "action:write_code": "Write a python script to ",
            "action:send_email": "Draft an email to ",
            "action:analyze_image": "Analyze the attached image and ",
            "action:summarize_file": "Summarize this file: ",
            "action:search_web": "Search the web for "
        }
        if action in prompts:
            self.input_field.setText(prompts[action])
            self.input_field.setFocus()

    def regenerate_message(self):
        if self.last_prompt:
            self.input_field.setText(self.last_prompt)
            self.send_message()

    def send_message(self):
        text = self.input_field.toPlainText().strip()
        if not text:
            return
            
        self.input_field.clear()
        self.last_prompt = text
        self.btn_regenerate.hide()
        
        time_str = datetime.now().strftime('%I:%M %p')
        user_html = f"<div style='text-align:right;'><b style='color:#3B82F6;'>You:</b> <span style='color:gray;font-size:10px;'>{time_str}</span><br>{text}</div><br>"
        self.chat_html_history += user_html
        self.chat_history.setHtml(self.chat_html_history + "<i style='color:gray;'>Thatwaat AI is thinking...</i><br>")
        self.current_reply = ""
        
        # Change Send button to Stop button
        self.send_btn.setText("⏹️ Stop")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #EF4444;
                border: none;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover { color: #DC2626; }
        """)
        self.send_btn.clicked.disconnect()
        self.send_btn.clicked.connect(self.stop_generation)
        
        self.thread = QThread()
        self.worker = AgentWorker(text)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.process)
        self.worker.token_received.connect(self.on_token)
        self.worker.finished.connect(self.on_response)
        self.worker.error.connect(self.on_error)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()
        
        if not hasattr(self, 'active_threads'):
            self.active_threads = []
        self.active_threads.append(self.thread)
        self.thread.finished.connect(lambda t=self.thread: self.active_threads.remove(t) if t in self.active_threads else None)

    def stop_generation(self):
        if hasattr(self, 'worker'):
            self.worker.stop()
        self.reset_send_button()
        
    def reset_send_button(self):
        self.send_btn.setText("➤ Send")
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
        self.send_btn.clicked.disconnect()
        self.send_btn.clicked.connect(self.send_message)
        self.btn_regenerate.show()

    def on_token(self, token):
        self.current_reply += token
        html_text = self.process_markdown(self.current_reply)
        cursor = " <span style='background-color: white; width: 8px; display: inline-block;'>&nbsp;</span>"
        time_str = datetime.now().strftime('%I:%M %p')
        final_html = self.chat_html_history + f"<div style='background-color: #111827; padding: 15px; border-radius: 10px;'><b style='color:#10B981;'>Thatwaat AI:</b> <span style='color:gray;font-size:10px;'>{time_str}</span><br>{html_text}{cursor}</div><br><br>"
        self.chat_history.setHtml(final_html)
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def on_response(self, text):
        self.reset_send_button()
        html_text = self.process_markdown(text)
        time_str = datetime.now().strftime('%I:%M %p')
        agent_html = f"<div style='background-color: #111827; padding: 15px; border-radius: 10px;'><b style='color:#10B981;'>Thatwaat AI:</b> <span style='color:gray;font-size:10px;'>{time_str}</span><br>{html_text}</div><br><br>"
        self.chat_html_history += agent_html
        self.chat_history.setHtml(self.chat_html_history)
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        
        try:
            from database import save_chat
            save_chat(self.last_prompt, text)
        except Exception as e:
            print("Could not save to DB:", e)

    def on_error(self, err):
        self.reset_send_button()
        self.chat_html_history += f"<b style='color:#EF4444;'>Error:</b> {err}<br><br>"
        self.chat_history.setHtml(self.chat_html_history)

    def action_attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File to Attach")
        if file_path:
            current_text = self.input_field.toPlainText()
            self.input_field.setText(f"{current_text}\n[Attached File: {file_path}]\n")
            self.input_field.setFocus()
            
    def action_voice_input(self):
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, "Voice Input Simulation", "Pretend you just spoke. What did you say?")
        if ok and text:
            self.input_field.setText(self.input_field.toPlainText() + " " + text)
            self.input_field.setFocus()
        
    def action_camera(self):
        try:
            import cv2
            import os
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                os.makedirs("memory", exist_ok=True)
                path = os.path.abspath(os.path.join("memory", "capture.jpg"))
                cv2.imwrite(path, frame)
                self.input_field.setText(self.input_field.toPlainText() + f"\n[Attached Image: {path}]\n")
                QMessageBox.information(self, "Camera", "Snapshot taken and attached!")
            else:
                QMessageBox.warning(self, "Error", "Could not read from camera.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to access camera: {e}")
        
    def action_emoji(self):
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        emojis = ["😊", "😂", "🚀", "💡", "🔥", "👍", "👀"]
        for emoji in emojis:
            action = menu.addAction(emoji)
            action.triggered.connect(lambda checked=False, e=emoji: self.input_field.setText(self.input_field.toPlainText() + e))
        menu.exec(self.btn_emoji.mapToGlobal(self.btn_emoji.rect().bottomLeft()))

    def action_history(self):
        from PySide6.QtWidgets import QDialog, QListWidget, QVBoxLayout, QPushButton, QLabel
        from database import get_history
        dialog = QDialog(self)
        dialog.setWindowTitle("Chat History")
        dialog.setMinimumSize(600, 400)
        dialog.setStyleSheet("QDialog { background-color: #1E293B; color: white; }")
        
        dialog_layout = QVBoxLayout(dialog)
        
        lbl = QLabel("Past Conversations")
        lbl.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        dialog_layout.addWidget(lbl)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget { background-color: #111827; color: white; border: none; padding: 10px; border-radius: 5px; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #374151; }
            QListWidget::item:selected { background-color: #3B82F6; }
        """)
        
        history = get_history(50)
        for row in history:
            timestamp, prompt, response = row
            snippet = (prompt[:60] + "...") if len(prompt) > 60 else prompt
            list_widget.addItem(f"[{timestamp}] {snippet}")
            
        dialog_layout.addWidget(list_widget)
        btn_close = QPushButton("Close")
        btn_close.setStyleSheet("background-color: #3B82F6; color: white; padding: 10px; border-radius: 5px;")
        btn_close.clicked.connect(dialog.accept)
        dialog_layout.addWidget(btn_close)
        
        dialog.exec()

