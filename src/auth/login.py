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


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Sets up the login window UI"""
        self.setWindowTitle("Login")
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
        self.show_password = QCheckBox("Show Password", self)
        self.login_button = QPushButton("Login")
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_label = QLabel("Don't have an account ?")
        self.register_button = QPushButton("Register")

        register_layout = QHBoxLayout()
        register_layout.addWidget(self.register_label)
        register_layout.addWidget(self.register_button)
        register_layout.addStretch()

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)
        layout.addLayout(register_layout)

        self.setMinimumSize(350, 200)
        self.setMaximumSize(350, 300)

        self.setLayout(layout)

    def setup_connections(self):
        """Sets up signal/slot connections"""
        self.login_button.clicked.connect(self.login_user)
        self.show_password.stateChanged.connect(self.show_password_state_changed)
        self.register_button.clicked.connect(self.parent.show_register)

    def show_password_state_changed(self):
        """Changes the password input field's echo mode based on the checkbox state"""
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def login_user(self):
        """Handles user login"""
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("Please fill in all fields")
            return

        if User.verify_password(username, password):
            self.parent.logged_in_user = username
            self.parent.update_ui_state()
            self.close()
        else:
            self.error_label.setText("Invalid username or password")
