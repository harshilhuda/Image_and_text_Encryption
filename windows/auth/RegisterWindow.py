from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QPushButton, QWidget, QMessageBox
from modules.auth import login

class RegisterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.register_button = QPushButton("Register")
        self.back_button = QPushButton("Back")

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.back_button)

        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(parent.go_to_welcome_page)

        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Here you would implement your registration logic
        print(login.register(username, password))
        QMessageBox.information(self, "Registration", f"Registered with\nUsername: {username}\nPassword: {password}")
