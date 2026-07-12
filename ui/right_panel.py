from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QTimer
import psutil

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
        
        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(self.val_lbl)

    def update_value(self, value):
        self.val_lbl.setText(value)

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
        self.cpu_card = StatusCard("CPU Usage", "0%", "#06B6D4")
        self.ram_card = StatusCard("RAM Usage", "0 GB", "#8B5CF6")
        self.gpu_card = StatusCard("GPU Usage", "N/A", "#10B981")
        self.model_card = StatusCard("Model Loaded", "Qwen2.5-Coder", "#3B82F6")
        self.camera_card = StatusCard("Camera Status", "Idle", "#9CA3AF")
        self.mic_card = StatusCard("Microphone Status", "Idle", "#10B981")
        self.internet_card = StatusCard("Internet", "Online", "#06B6D4")
        
        layout.addWidget(self.cpu_card)
        layout.addWidget(self.ram_card)
        layout.addWidget(self.gpu_card)
        layout.addWidget(self.model_card)
        layout.addWidget(self.camera_card)
        layout.addWidget(self.mic_card)
        layout.addWidget(self.internet_card)
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        try:
            cpu = psutil.cpu_percent()
            self.cpu_card.update_value(f"{cpu}%")
            
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024 ** 3)
            self.ram_card.update_value(f"{used_gb:.1f} GB")
        except Exception:
            pass
