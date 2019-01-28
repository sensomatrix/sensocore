from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget
import logging

class ConsoleHandler(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.plain_text_widget = QPlainTextEdit()
        self.plain_text_widget.setReadOnly(True)

    def emit(self, msg):
        format_msg = self.format(msg)
        self.plain_text_widget.appendPlainText(format_msg)

class Console(QWidget):
    def __init__(self, parent):
        super().__init__()
        console_handler = ConsoleHandler(self)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger().addHandler(console_handler)
        logging.getLogger().setLevel(logging.INFO)
        layout = QVBoxLayout()
        layout.addWidget(console_handler.plain_text_widget)
        self.setLayout(layout)
        logging.info('Welcome to Sensomatrix')
        
    def write(self, msg):
        logging.info(msg)