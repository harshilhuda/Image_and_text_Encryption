from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

import rust_hash_module

class DownloadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.fileName_label = QLabel("FileName:")
        self.fileName_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.decrypt_button = QPushButton("Decrypt File")
        self.back_button = QPushButton("Back")

        self.layout.addWidget(self.fileName_label)
        self.layout.addWidget(self.fileName_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.decrypt_button)
        self.layout.addWidget(self.back_button)

        self.decrypt_button.clicked.connect(self.decrypt)
        self.back_button.clicked.connect(parent.go_to_main_page)
        self.parentClass = parent

        self.setLayout(self.layout)

    def decrypt(self):
        fileName = self.fileName_input.text()
        password = self.password_input.text()

        fileNameEdited = fileName.split("/")[-1]
        print(fileName)
        result = rust_hash_module.decrypt_file(fileName, f"E:/project/cloud_downloads/{fileNameEdited}", password)
        if (result == "Success"):
            QMessageBox.information(self, "Success", f"File Saved at : E:/project/cloud_downloads/{fileNameEdited}")
