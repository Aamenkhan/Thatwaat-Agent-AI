from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtCore import Qt

class ModernButton(QPushButton):
    """A beautifully styled, animated button."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(59, 130, 246, 0.2);
                color: #3B82F6;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 8px 16px;
                font-family: 'Segoe UI', Inter, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(59, 130, 246, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(59, 130, 246, 0.6);
            }
        """)
