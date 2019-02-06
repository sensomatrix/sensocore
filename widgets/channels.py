from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QMenu
from PyQt5.QtCore import Qt, pyqtSignal


# implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QWidget):

    channel_selected_signal = pyqtSignal(object)
    plot_PSD_requested = pyqtSignal(object)

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
        self.channel_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.channel_list.customContextMenuRequested.connect(self.create_menu)
        # self.channel_list.setSelectionModel()
        layout = QVBoxLayout()
        layout.addWidget(self.channel_list)
        self.setLayout(layout)

    def on_signal_loaded(self, signal):
        item = QListWidgetItem(signal.name)
        item.setData(Qt.UserRole, signal.id)
        self.channel_list.addItem(item)

    # this is not used (old debugging code)
    def selectionChanged(self):
        item = self.channel_list.selectedItems()[0]
        id = item.data(Qt.UserRole)
        sig = self.signal_dict.get(id)
        self.channel_selected_signal.emit(sig)

    def create_menu(self, position):
        if self.channel_list.selectedItems():
            item = self.channel_list.selectedItems()[0]
            id = item.data(Qt.UserRole)
            sig = self.signal_dict.get(id)
            ChannelsRightClickMenu(self, sig, position)


class ChannelsRightClickMenu(QMenu):

    def __init__(self, parent, sig, position):
        super().__init__()
        self.parent = parent
        self.sig = sig
        self.create()
        self.exec(parent.mapToGlobal(position))

    def create(self):
        # Remove DC
        action = self.addAction("Remove DC")
        action.triggered.connect(lambda: self.parent.parent.datasets.removeDC(self.sig.id))
        self.addAction(action)

        #Plot PSD button
        action = self.addAction("Plot PSD")
        action.triggered.connect(lambda: self.parent.parent.secondary_area.plot_psd_slot(self.sig))
        self.addAction(action)

        #Plot Time-frequency button
        action = self.addAction("Plot Time-Frequency")
        action.triggered.connect(lambda: self.parent.parent.secondary_area.plot_tf_slot(self.sig))
        self.addAction(action)


