from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal


# implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QListWidget):

    channel_selected_signal = pyqtSignal(object)
    plot_PSD_requested = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_menu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def on_signal_loaded(self, signal):
        item = QListWidgetItem(signal.name)
        item.setData(Qt.UserRole, signal)
        self.addItem(item)

    # # this is not used (old debugging code)
    # def selectionChanged(self):
    #     item = self.channel_list.selectedItems()[0]
    #     id = item.data(Qt.UserRole)
    #     sig = self.signal_dict.get(id)
    #     self.channel_selected_signal.emit(sig)

    def create_menu(self, position):
        if self.selectedItems():
            item = self.selectedItems()[0]
            signal = item.data(Qt.UserRole)
            ChannelsRightClickMenu(self, signal, position)

    def getSelectedChannels(self):
        channel_id_list = []
        for item in self.channel_list.selectedItems():
            channel_id_list.append(item.data(Qt.UserRole))
        return channel_id_list


class ChannelsRightClickMenu(QMenu):
    def __init__(self, parent, sig, position):
        super().__init__()
        self.parent = parent
        self.sig = sig
        self.init()
        self.exec(parent.mapToGlobal(position))

    def init(self):
        # Remove DC
        action = self.addAction("Remove DC")
        action.triggered.connect(lambda: self.parent.parent.datasets.removeDC(self.sig))
        self.addAction(action)

        #Plot PSD button
        action = self.addAction("Plot PSD")
        action.triggered.connect(lambda: self.parent.parent.secondary_area.plot_psd_slot(self.sig))
        self.addAction(action)

        #Plot Time-frequency button
        action = self.addAction("Plot Time-Frequency")
        action.triggered.connect(lambda: self.parent.parent.secondary_area.plot_tf_slot(self.sig))
        self.addAction(action)


