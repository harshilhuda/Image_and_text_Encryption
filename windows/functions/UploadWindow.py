from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog

class UploadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(parent.go_to_main_page)

        self.upload_button = QPushButton("Upload File", self)
        self.upload_button.setGeometry(50, 50, 150, 30)
        self.upload_button.clicked.connect(self.upload_file)

        self.file_label = QLabel("Selected File: None", self)
        self.file_label.setGeometry(50, 100, 300, 30)

        self.layout.addWidget(self.file_label)
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
                self.file_label.setText(f"Selected File: {file_name}")
            else:
                self.file_label.setText("No file selected")