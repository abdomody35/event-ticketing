from PyQt6.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from .pages.main_page import MainPage
from .pages.dashboard import Dashboard
from ..auth.login import LoginWindow
from ..auth.register import RegisterWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Sets up the main window UI"""
        self.setWindowTitle("Ticket Marketplace")
        self.setMinimumSize(900, 750)
        self.setStyleSheet("background-color: skyblue; color: black; font: bold 20px")
        self.setup_toolbar()
        self.setup_central_widget()

    def setup_toolbar(self):
        """Sets up the main toolbar"""
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.main_action = QAction("Marketplace", self)
        self.login_action = QAction("Login", self)
        self.register_action = QAction("Register", self)
        self.logout_action = QAction("Logout", self)
        self.dashboard_action = QAction("Dashboard", self)

        self.main_action.triggered.connect(self.setup_central_widget)
        self.login_action.triggered.connect(self.show_login)
        self.register_action.triggered.connect(self.show_register)
        self.logout_action.triggered.connect(self.logout)
        self.dashboard_action.triggered.connect(self.show_dashboard)

        self.toolbar.addAction(self.main_action)
        self.toolbar.addAction(self.login_action)
        self.toolbar.addAction(self.register_action)
        self.toolbar.addAction(self.dashboard_action)
        self.toolbar.addAction(self.logout_action)

        self.logged_in_user = None
        self.update_ui_state()

    def setup_central_widget(self):
        """Sets up the central widget"""
        self.main_page = MainPage(self)
        self.setCentralWidget(self.main_page)

    def show_login(self):
        """Shows the login window"""
        self.login_window = LoginWindow(self)
        self.set_central_widget(self.login_window)

    def show_register(self):
        """Shows the registration window"""
        self.register_window = RegisterWindow(self)
        self.set_central_widget(self.register_window)

    def show_dashboard(self):
        """Shows the user dashboard"""
        if self.logged_in_user:
            self.dashboard = Dashboard(self)
            self.setCentralWidget(self.dashboard)

    def logout(self):
        """Handles user logout"""
        self.logged_in_user = None
        self.update_ui_state()
        self.setup_central_widget()

    def update_ui_state(self):
        """Updates UI based on authentication state"""
        is_logged_in = self.logged_in_user is not None
        self.login_action.setVisible(not is_logged_in)
        self.register_action.setVisible(not is_logged_in)
        self.logout_action.setVisible(is_logged_in)
        self.dashboard_action.setVisible(is_logged_in)
        self.setup_central_widget()

    def set_central_widget(self, widget):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.setAlignment(widget, Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if isinstance(self.centralWidget(), MainPage):
            widget_count = self.width() / 650
            if widget_count > 2.92:
                widget_count = 3
            else:
                widget_count = int(widget_count)
            if not widget_count == self.centralWidget().num_columns:
                self.centralWidget().load_events()
