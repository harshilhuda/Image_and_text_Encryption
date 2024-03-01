from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QLineEdit

import rust_hash_module

class UploadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(parent.go_to_main_page)

        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.setGeometry(50, 50, 150, 30)
        self.upload_button.clicked.connect(self.upload_file)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()

        self.file_label = QLabel(f"Selected File: {rust_hash_module.sum_as_string(5, 20)}", self)
        self.file_label.setGeometry(50, 100, 300, 30)

        self.username = parent.username
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.backButton)
        self.setLayout(self.layout)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_name = file_names[0]
                hashValue = rust_hash_module.calculate_file_hash(file_name)
                print(hashValue)
                fileName = getFileName(file_name)
                self.file_label.setText(f"Selected File: {fileName}")
                result = verifyHash(fileName, hashValue, self.username)
                print(result)
                if(result == "Success"):
                    password = self.password_input.text()
                    #                                   Filename   Filepath                       Password
                    r1 = rust_hash_module.encrypt_file(file_name, f"E:/project/cloud/{fileName}", password)
                    QMessageBox.information(self, "Success", f"File Added to cloud: {file_name}")
            else:
                self.file_label.setText("No file selected")


def getFileName(absolutePath):
    return absolutePath.split("/")[-1]

from PyQt5.QtSql import QSqlQuery

def verifyHash(filename, hash, username):
    query = QSqlQuery()
    query.exec_("CREATE TABLE IF NOT EXISTS files (filename TEXT, hash TEXT UNIQUE, username TEXT, FOREIGN KEY(username) REFERENCES users(username))")
    if not query.exec_():
        return "Duplicate Username"
    query.prepare("SELECT filename FROM files where hash=(?)")
    query.bindValue(0, hash)
    if not query.exec_():
        return "Invalid"
    if query.next():
        return "File Already Exists"
    else:
        query.prepare("INSERT INTO files (filename, hash, username) VALUES (?, ?, ?)")
        query.bindValue(0, filename)
        query.bindValue(1, hash)
        query.bindValue(2, username)
        if not query.exec_():
            return "Error in adding files"
        return "Success"