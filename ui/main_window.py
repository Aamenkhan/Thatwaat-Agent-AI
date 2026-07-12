from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.chat_page import ChatPage
from ui.vision_page import VisionPage
from ui.voice_page import VoicePage
from ui.automation_page import AutomationPage
from ui.settings_page import SettingsPage

class MainWindow(QMainWindow):
    """The main application shell incorporating the sidebar and page router."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thatwaat Agent AI")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #0B1220;")

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Page Router (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Initialize Pages
        self.chat_page = ChatPage()
        self.vision_page = VisionPage()
        self.voice_page = VoicePage()
        self.automation_page = AutomationPage()
        self.settings_page = SettingsPage()

        # Add pages to router in same order as Sidebar nav items
        self.stacked_widget.addWidget(self.chat_page)       # Index 0
        self.stacked_widget.addWidget(self.vision_page)     # Index 1
        self.stacked_widget.addWidget(self.voice_page)      # Index 2
        self.stacked_widget.addWidget(self.automation_page) # Index 3
        self.stacked_widget.addWidget(self.settings_page)   # Index 4

        # Connect Sidebar events
        self.sidebar.page_changed.connect(self.switch_page)

    def switch_page(self, index):
        """Switch to the requested page index."""
        self.stacked_widget.setCurrentIndex(index)
