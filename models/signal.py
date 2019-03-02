from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from numpy import mean


class Signal:
    def __init__(self, samples_array, time_array, fs, name, signal_type):
        self.samples_array = samples_array
        self.time_array = time_array
        self.fs = fs
        self.name = name
        self.type = signal_type

    def remove_dc(self):
        self.samples_array = self.samples_array - mean(self.samples_array)


class SignalListModel(QtCore.QAbstractListModel):
    added_signal = pyqtSignal(Signal)
    added_signals = pyqtSignal(list)
    plot_psd_signal = pyqtSignal(Signal)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self._signals = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._signals)

    def data(self, QModelIndex, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:
            row = QModelIndex.row()
            signal = self._signals[row]
            return signal.name

        if role == QtCore.Qt.UserRole:
            row = QModelIndex.row()
            signal = self._signals[row]
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
        row = QModelIndex.row()
        signal = self._signals[row]
        signal.remove_dc()

    def print(self):
        print('what is going on')

    def plot_psd(self, QModelIndex):
        row = QModelIndex.row()
        signal = self._signals[row]

        self.plot_psd_signal.emit(signal)




