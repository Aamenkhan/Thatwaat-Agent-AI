from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.top_bar import TopBar
from ui.right_panel import RightPanel
from ui.chat_page import ChatPage
from ui.vision_page import VisionPage
from ui.voice_page import VoicePage
from ui.automation_page import AutomationPage
from ui.settings_page import SettingsPage

class MainWindow(QMainWindow):
    """The main application shell incorporating the new complex layout."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thatwaat Agent AI")
        self.resize(1400, 900)
        self.setStyleSheet("background-color: #0B1220;")

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Vertical Layout (TopBar + Content)
        main_v_layout = QVBoxLayout(central_widget)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)
        
        # Top Bar
        self.top_bar = TopBar()
        main_v_layout.addWidget(self.top_bar)

        # Content Horizontal Layout (Sidebar + Router + RightPanel)
        content_h_layout = QHBoxLayout()
        content_h_layout.setContentsMargins(0, 0, 0, 0)
        content_h_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        content_h_layout.addWidget(self.sidebar)

        # Page Router (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #0B1220;")
        content_h_layout.addWidget(self.stacked_widget)
        
        # Right Panel
        self.right_panel = RightPanel()
        content_h_layout.addWidget(self.right_panel)

        main_v_layout.addLayout(content_h_layout)

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

    def closeEvent(self, event):
        """Gracefully stop all worker threads across the app before closing."""
        # Stop Chat threads
        if hasattr(self.chat_page, 'active_threads'):
            for thread in list(self.chat_page.active_threads):
                if thread.isRunning():
                    thread.quit()
                    thread.wait()
        event.accept()

