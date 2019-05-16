from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qt import Qt


class ErrorMessage(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowModality(Qt.WindowModal)
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error")
        self.setText(message)
        self.exec()
