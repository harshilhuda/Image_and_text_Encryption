from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from modules.auth import login

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.login_button = QPushButton("Login")
        self.back_button = QPushButton("Back")

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.back_button)

        self.login_button.clicked.connect(self.login)
        self.back_button.clicked.connect(parent.go_to_welcome_page)
        self.parentClass = parent
        self.setLayout(self.layout)

    def login(self, parent):
        username = self.username_input.text()
        password = self.password_input.text()
        # Here you would implement your login logic
        result = login.login(username, password)
        if(result == "Success"):
            self.parentClass.go_to_home_page()
            self.parentClass.isLoggedIn = True
        print(result)
        QMessageBox.information(self, "Login", f"Logged in with\nUsername: {username}\nPassword: {password}")
