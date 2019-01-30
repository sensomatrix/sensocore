from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal


# implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QWidget):

    channel_selected_signal = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.signal_dict = parent.datasets.signals_dictionary  # this is a reference, not a copy
        self.statistics_dict = {}
        self.tabs = None
        self.channel_list = None
        self.create()

    def create(self):
        self.channel_list = QListWidget()
        self.channel_list.itemSelectionChanged.connect(self.selectionChanged)
        layout = QVBoxLayout()
        layout.addWidget(self.channel_list)
        self.setLayout(layout)

    def on_signal_loaded(self, signal):
        item = QListWidgetItem(signal.name)
        item.setData(Qt.UserRole, signal.id)
        self.channel_list.addItem(item)

    def selectionChanged(self):
        item = self.channel_list.selectedItems()[0]
        id = item.data(Qt.UserRole)
        sig = self.signal_dict.get(id)
        self.channel_selected_signal.emit(sig)
