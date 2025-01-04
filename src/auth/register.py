from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QCheckBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from ..models.user import User


class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Sets up the registration window UI"""
        self.setWindowTitle("Register")
        self.setup_layout()
        self.setup_connections()

    def setup_layout(self):
        """Creates and arranges UI elements"""
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_label = QLabel("Confirm Password:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_password = QCheckBox("Show Password", self)
        self.register_button = QPushButton("Register")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label = QLabel("Already have an account ?")
        self.login_button = QPushButton("Login")

        login_layout = QHBoxLayout()
        login_layout.addWidget(self.login_label)
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.show_password)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)
        layout.addLayout(login_layout)

        self.setMinimumSize(350, 250)
        self.setMaximumSize(350, 350)

        self.setLayout(layout)

    def setup_connections(self):
        """Sets up signal/slot connections"""
        self.register_button.clicked.connect(self.register_user)
        self.show_password.stateChanged.connect(self.show_password_state_changed)
        self.login_button.clicked.connect(self.parent.show_login)

    def show_password_state_changed(self):
        """Changes the password input field's echo mode based on the checkbox state"""
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

    def register_user(self):
        """Handles user registration"""
        username = self.username_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not password or not confirm:
            self.error_label.setText("Please fill in all fields")
            return

        if password != confirm:
            self.error_label.setText("Passwords do not match")
            return

        if len(password) < 8:
            self.error_label.setText("Password must be at least 8 characters")
            return

        try:
            User.create_user(username, password)
            self.parent.logged_in_user = username
            self.parent.update_ui_state()
            self.close()
        except Exception as e:
            self.error_label.setText("Username already exists")
