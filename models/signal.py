from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from numpy import mean, array


class Signal:
    def __init__(self, samples_array, time_array, fs, name, signal_type):
        self.raw = samples_array
        self.filtered = None
        self.time_array = time_array
        self.fs = fs
        self.name = name
        self.type = signal_type
        self.current_mode = self.raw

    def remove_dc(self):
        self.raw = self.raw - mean(self.raw)
        if self.filtered:
            self.filtered = self.filtered - mean(self.filtered)


class SignalListModel(QtCore.QAbstractListModel):
    added_signal = pyqtSignal(Signal)
    added_signals = pyqtSignal(list)
    plot_psd_signal = pyqtSignal(Signal)
    plot_time_freq_signal = pyqtSignal(Signal)
    update_plot = pyqtSignal(Signal, int)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self._signals = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._signals)

    def data(self, QModelIndex, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:
            signal = self.get_signal(QModelIndex)
            return signal.name

        if role == QtCore.Qt.UserRole:
            signal = self.get_signal(QModelIndex)
            return signal

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, QModelIndex, Any, role=None):
        if role == QtCore.Qt.EditRole:
            row = QModelIndex.row()

            self._signals[row].name = Any
            return True

        if role == QtCore.Qt.CheckStateRole:
            print('fh')
            row = QModelIndex.row()
            if self._signals[row].isChecked():
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

    def add_signal(self, signal):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._signals.append(signal)
        self.endInsertRows()

        self.added_signal.emit(signal)

    def add_signals(self, signals):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        for signal in signals:
            self._signals.append(signal)
        self.endInsertRows()

        self.added_signals.emit(signals)

    def remove_dc(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        signal.remove_dc()

    def plot_psd(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_psd_signal.emit(signal)

    def plot_time_freq(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_time_freq_signal.emit(signal)

    def plot_filtered_signal(self, signal):
        if signal.filtered is not None:
            signal.current_mode = signal.filtered
            self.update_plot.emit(signal, self._signals.index(signal))

    def toggle_mode(self, QModelIndex):
        signal = self.get_signal(QModelIndex)

        if signal.filtered is not None:
            signal.current_mode = signal.filtered if signal.current_mode is signal.raw else signal.raw
            self.update_plot.emit(signal, self._signals.index(signal))

    def get_signal(self, QModelIndex):
        row = QModelIndex.row()
        return self._signals[row]




