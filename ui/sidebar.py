from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal

class Sidebar(QWidget):
    """Modern navigation sidebar component."""
    
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(17, 24, 39, 0.8);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
            QPushButton {
                background-color: transparent;
                color: #9CA3AF;
                text-align: left;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', Inter, sans-serif;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
                color: white;
            }
            QPushButton:checked {
                background-color: rgba(59, 130, 246, 0.15);
                color: #3B82F6;
                font-weight: bold;
                border-left: 3px solid #3B82F6;
                border-radius: 0px 8px 8px 0px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 15px;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Brand
        brand = QLabel("🤖 Thatwaat AI")
        layout.addWidget(brand)

        # Nav Buttons
        self.buttons = []
        nav_items = ["Chat", "Vision", "Voice", "Automation", "Settings"]
        
        for i, text in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setCheckable(True)
            if i == 0:
                btn.setChecked(True)
            
            # Capture the correct index using a default arg in the lambda
            btn.clicked.connect(lambda checked, idx=i: self._on_btn_clicked(idx))
            self.buttons.append(btn)
            layout.addWidget(btn)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _on_btn_clicked(self, index):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)
        self.page_changed.emit(index)
