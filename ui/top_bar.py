from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class TopBar(QWidget):
    """The top navigation and status bar."""
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            QLabel {
                color: #9CA3AF;
                font-family: 'Segoe UI', Inter, sans-serif;
                font-size: 13px;
                border: none;
            }
            QLineEdit {
                background-color: #1E293B;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 5px 15px;
                color: white;
                font-size: 13px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Left: Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search...")
        self.search_box.setFixedWidth(250)
        layout.addWidget(self.search_box)
        
        layout.addStretch()
        
        # Middle: System Stats
        self.cpu_label = QLabel("CPU: 12%")
        self.ram_label = QLabel("RAM: 32%")
        self.gpu_label = QLabel("GPU: Ready")
        
        layout.addWidget(self.cpu_label)
        layout.addSpacing(15)
        layout.addWidget(self.ram_label)
        layout.addSpacing(15)
        layout.addWidget(self.gpu_label)
        
        layout.addStretch()
        
        # Right: Connection & Profile
        self.status_label = QLabel("🟢 Ollama Connected")
        self.status_label.setStyleSheet("color: #10B981; font-weight: bold;")
        
        self.notifications_icon = QLabel("🔔")
        self.profile_icon = QLabel("👤")
        
        layout.addWidget(self.status_label)
        layout.addSpacing(20)
        layout.addWidget(self.notifications_icon)
        layout.addSpacing(15)
        layout.addWidget(self.profile_icon)
