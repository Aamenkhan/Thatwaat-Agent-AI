import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database import init_db

def main():
    """Main entry point for Thatwaat Agent AI Desktop Application."""
    
    # 1. Initialize Core Backend Services
    init_db()
    
    # 2. Initialize Qt Application
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Provides a cleaner base for our custom QSS
    
    # 3. Create and show Main Window
    window = MainWindow()
    window.show()
    
    # 4. Start Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
