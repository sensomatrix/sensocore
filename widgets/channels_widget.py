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
        action.triggered.connect(lambda: self.model().remove_dc(item_index))

        # Plot PSD button
        if not self.model().is_psd_plotted(item_index):
            action = menu.addAction("Plot PSD")
            action.triggered.connect(lambda: self.model().plot_psd(item_index))

        # Plot Time-frequency button
        action = menu.addAction("Plot Time-Frequency")
        action.triggered.connect(lambda: self.model().plot_time_freq(item_index))

        if self.model().does_signal_contain_filtered(item_index):
            is_raw = self.model().is_current_mode_raw(item_index)

            action_title = "View Filtered Signal" if is_raw else "View Raw Signal"

            action = menu.addAction(action_title)
            action.triggered.connect(lambda: self.model().toggle_mode(item_index))

        is_ecg = self.model().is_ecg_signal(item_index)
        is_eeg = self.model().is_eeg_signal(item_index)

        if is_ecg:
            action = menu.addAction('View ECG Summary')
            action.triggered.connect(lambda: self.model().view_ecg_summary(item_index))

        elif is_eeg:
            action = menu.addAction('View EEG Summary')
            action.triggered.connect(lambda: self.model().view_eeg_summary(item_index))

        menu.exec_(self.mapToGlobal(pos))


