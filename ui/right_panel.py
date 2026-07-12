from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class StatusCard(QFrame):
    def __init__(self, title, value, color="#3B82F6"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1E293B;
                border-radius: 10px;
                padding: 10px;
            }}
            QLabel {{ border: none; }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: bold;")
        
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)

class RightPanel(QWidget):
    """The right side dashboard panel."""
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                border-left: 1px solid rgba(255, 255, 255, 0.05);
            }
            QLabel.header {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 10px;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        header = QLabel("Dashboard")
        header.setProperty("class", "header")
        layout.addWidget(header)
        
        # Cards
        layout.addWidget(StatusCard("Current Model", "Qwen2.5-Coder", "#06B6D4"))
        layout.addWidget(StatusCard("Today's Tasks", "3 Pending", "#8B5CF6"))
        layout.addWidget(StatusCard("Memory Usage", "1.2 GB", "#3B82F6"))
        layout.addWidget(StatusCard("GPU Usage", "450 MB", "#10B981"))
        layout.addWidget(StatusCard("Camera Status", "Idle", "#9CA3AF"))
        layout.addWidget(StatusCard("Microphone Status", "Listening...", "#10B981"))
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
