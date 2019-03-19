from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from numpy import mean
import copy
from biosppy import signals, clustering
import numpy as np
#TODO: Remove this after being used
import matplotlib.pyplot as plt


class Signal:
    def __init__(self, samples_array, fs, name, signal_type):
        self.summary = None
        self.raw = samples_array.T[1]
        self.filtered = None
        self.clusters = None
        self.time_array = samples_array.T[0]
        self.fs = fs
        self.name = name
        self.type = signal_type
        self.current_mode = self.raw
        self.create_summary()

    def create_summary(self):
        if 'EEG' in self.type:
            eeg = np.transpose(self.current_mode).reshape((self.current_mode.shape[0], 1))
            self.summary = signals.eeg.eeg(eeg, self.fs, show=False)
        elif 'ECG' in self.type:
            ecg = np.transpose(self.current_mode)
            self.summary = signals.ecg.ecg(ecg, self.fs, show=False)
            duration_between_r_peaks = np.zeros((self.summary[2].shape[0] - 1, 1))
            r_value = np.zeros((self.summary[2].shape[0] - 1, 1))

            current_index = 0

            for index, r_peak_index in enumerate(self.summary[2]):
                if current_index < duration_between_r_peaks.shape[0] and index < self.summary[2].shape[0]:
                    duration_between_r_peaks[current_index] = (self.summary[2][index + 1] - r_peak_index) * (1.0 / self.fs)
                    r_value[current_index] = self.current_mode[r_peak_index]
                    current_index += 1
                else:
                    break

            x = duration_between_r_peaks[:-1]
            y = np.delete(duration_between_r_peaks, 0)
            y = y.reshape(x.shape[0], x.shape[1])

            r_value = np.delete(r_value, r_value.shape[0] - 1)
            r_value = r_value.reshape(r_value.shape[0], 1)

            self.clusters = clustering.dbscan(np.hstack((x, y, r_value)), eps=0.05)

    def remove_dc(self):
        self.current_mode = self.current_mode - mean(self.current_mode)

class SignalListModel(QtCore.QAbstractListModel):
    added_signal = pyqtSignal(Signal)
    added_signals = pyqtSignal(list)
    plot_psd_signal = pyqtSignal(Signal)
    plot_time_freq_signal = pyqtSignal(Signal)
    update_plot = pyqtSignal(Signal, int)
    plot_ecg_summary = pyqtSignal(object, object)
    plot_eeg_summary = pyqtSignal(object, object)

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
        self.update_plot.emit(signal, QModelIndex.row())

    def plot_psd(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_psd_signal.emit(signal)

    def plot_time_freq(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_time_freq_signal.emit(signal)

    def plot_filtered_signal(self, signal):
        if signal.filtered is not None:
            signal.current_mode = signal.filtered
            signal.create_summary()
            self.update_plot.emit(signal, self._signals.index(signal))

    def toggle_mode(self, QModelIndex):
        signal = self.get_signal(QModelIndex)

        if signal.filtered is not None:
            signal.current_mode = signal.filtered if signal.current_mode is signal.raw else signal.raw
            self.update_plot.emit(signal, self._signals.index(signal))

    def view_ecg_summary(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_ecg_summary.emit(signal.summary, signal.current_mode)

    def view_eeg_summary(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        self.plot_eeg_summary.emit(signal.summary, signal.current_mode)

    def is_current_mode_raw(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.current_mode is signal.raw

    def is_ecg_signal(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.type == 'ECG'

    def is_eeg_signal(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.type == 'EEG'

    def get_signal(self, QModelIndex):
        row = QModelIndex.row()
        return self._signals[row]

    def create_child_signal(self, output, index):
        parent = self._signals[index]
        child_signal = Signal(output, parent.fs, parent.name, parent.type)
        self.add_signal(child_signal)

    def is_list_empty(self):
        return len(self._signals) == 0

    def does_signal_contain_filtered(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.filtered is not None



