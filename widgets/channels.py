from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout


# implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabs = None
        self.channel_list = None
        self.create()

    def create(self):
        self.channel_list = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.channel_list)
        self.setLayout(layout)

    def on_signal_loaded(self, signal):
        self.channel_list.addItem(signal.name)