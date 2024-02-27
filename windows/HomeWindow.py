from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Home Page!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)