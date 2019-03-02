from PyQt5.QtWidgets import QListView, QListWidgetItem, QMenu, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal


# implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QListView):

    channel_selected_signal = pyqtSignal(object)
    plot_PSD_requested = pyqtSignal(object)

    def __init__(self, parent):
        QListView.__init__(self, parent=parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_menu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def create_menu(self, pos):
        menu = QMenu("Menu", self)
        item_index = self.selectedIndexes()[0]

        action = menu.addAction("Remove DC")
        action.triggered.connect(lambda: self.signals.remove_dc(item_index))

        # Plot PSD button
        action = menu.addAction("Plot PSD")
        action.triggered.connect(lambda: self.model().plot_psd(item_index))

        # Plot Time-frequency button
        action = menu.addAction("Plot Time-Frequency")
        action.triggered.connect(lambda: self.model().plot_time_freq(item_index))

        menu.exec_(self.mapToGlobal(pos))


