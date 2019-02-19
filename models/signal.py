from PyQt5 import QtCore


class SignalListModel(QtCore.QAbstractListModel):
    def __init__(self, signals=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self._signals = signals

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._signals)

    def data(self, QModelIndex, role=None):
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

    def insertRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), p_int, p_int_1)
        self._signals.insert(p_int, args[0])
        self.endInsertRows()

class Signal():
    def __init__(self, samples_array, time_array, fs, name, signal_type):
        self.samples_array = samples_array
        self.time_array = time_array
        self.fs = fs
        self.name = name
        self.type = signal_type
