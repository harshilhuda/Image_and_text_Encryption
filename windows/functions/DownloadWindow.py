from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

class DownloadWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.backButton = QPushButton("Back")

        self.layout.addWidget(self.backButton)

        self.setLayout(self.layout)

        self.backButton.clicked.connect(parent.go_to_main_page)