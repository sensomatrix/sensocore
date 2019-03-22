from __future__ import division, print_function
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from numpy import mean
from biosppy import signals, clustering
from utils.frequtils import compute_psd
from keras.models import load_model
import numpy as np
import biosppy
import cv2
import matplotlib.pyplot as plt

# TODO: Make sure to use a proper route to this file
trained_model = load_model('/home/niroigen/Dev/sensomatrix/src/sensobox/ecgScratchEpoch2.hdf5')
trained_model._make_predict_function()  # Necessary

class Signal:
    def __init__(self, samples_array, fs, name, signal_type, annotations=None):
        self.summary = None
        self.raw = samples_array.T[1]
        self.filtered = None
        self.clusters = None
        self.psd = None
        self.time_freq = None
        self.annotations = annotations
        self.time_array = samples_array.T[0]
        self.fs = fs
        self.name = name
        self.type = signal_type
        self.current_mode = self.raw
        self.create_summary()

    def create_summary(self):
        if 'EEG' in self.type:
            eeg = np.transpose(self.current_mode).reshape((self.current_mode.shape[0], 1))
            try:
                self.summary = signals.eeg.eeg(eeg, self.fs, show=False)
                diff = int(eeg.shape[0] % (self.fs / 2))
                if diff != 0:
                    eeg = np.delete(eeg, eeg.shape[0] - 1)
                rows = eeg.shape[0] // (self.fs // 2)
                eeg = eeg.reshape((rows, self.fs // 2))

                eeg_psd = np.array([compute_psd(eeg[0][:], self.fs)[1]])

                for row in range(1, rows):
                    eeg_psd = np.vstack([eeg_psd, compute_psd(eeg[row][:], self.fs)[1]])

                self.clusters = clustering.dbscan(eeg_psd)
            except Exception as e:
                print(e.args)
        elif 'ECG' in self.type:
            ecg = np.transpose(self.current_mode)
            try:
                self.summary = signals.ecg.ecg(ecg, self.fs, show=False)
            except Exception as e:
                print(e.args)
            # self.clusters = clustering.dbscan(self.summary[4])
            if self.annotations is None:
                self.model_predict()

    def model_predict(self):

        output = []

        flag = 1

        # index1 = str(path).find('sig-2') + 6
        # index2 = -4
        # ts = int(str(path)[index1:index2])
        APC, NORMAL, LBB, PVC, PAB, RBB, VEB = [], [], [], [], [], [], []
        # output.append(str(path))
        result = {"APC": APC, "Normal": NORMAL, "LBB": LBB, "PAB": PAB, "PVC": PVC, "RBB": RBB, "VEB": VEB}

        indices = []

        kernel = np.ones((4, 4), np.uint8)

        # csv = pd.read_csv(path)
        # csv_data = csv[' Sample Value']
        # data = np.array(csv_data)
        # signals = self.summary[4]
        signals =[]

        data = self.raw

        # for i in range(1, len(signals) + 1):
        #     indices.append((self.summary[2][i - 1], self.summary[2][i]))
        count = 1
        peaks = biosppy.signals.ecg.christov_segmenter(signal=data, sampling_rate=self.fs)[0]
        for i in (peaks[1:-1]):
            diff1 = abs(peaks[count - 1] - i)
            diff2 = abs(peaks[count + 1] - i)
            x = peaks[count - 1] + diff1 // 2
            y = peaks[count + 1] - diff2 // 2
            signal = data[x:y]
            signals.append(signal)
            count += 1
            indices.append((x, y))

        # TODO: Get a percentage of how much is left
        for count, i in enumerate(signals):
            print(count / len(signals))
            fig = plt.figure(frameon=False)
            plt.plot(i)
            plt.xticks([]), plt.yticks([])
            for spine in plt.gca().spines.values():
                spine.set_visible(False)

            filename = 'fig' + '.png'
            fig.savefig(filename)
            plt.close()
            im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            im_gray = cv2.erode(im_gray, kernel, iterations=1)
            im_gray = cv2.resize(im_gray, (128, 128), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(filename, im_gray)
            im_gray = cv2.imread(filename)
            pred = trained_model.predict(im_gray.reshape((1, 128, 128, 3)))
            pred_class = pred.argmax(axis=-1)
            if pred_class == 0:
                APC.append(indices[count])
            elif pred_class == 1:
                NORMAL.append(indices[count])
            elif pred_class == 2:
                LBB.append(indices[count])
            elif pred_class == 3:
                PAB.append(indices[count])
            elif pred_class == 4:
                PVC.append(indices[count])
            elif pred_class == 5:
                RBB.append(indices[count])
            elif pred_class == 6:
                VEB.append(indices[count])

        result = sorted(result.items(), key=lambda y: len(y[1]))[::-1]
        output.append(result)
        # data = {}
        # # data['filename' + str(flag)] = str(path)
        # data['result' + str(flag)] = str(result)

        # json_filename = 'data.txt'
        # with open(json_filename, 'a+') as outfile:
        #     json.dump(data, outfile)
        # flag += 1
        #
        # with open(json_filename, 'r') as file:
        #     filedata = file.read()
        # filedata = filedata.replace('}{', ',')
        # with open(json_filename, 'w') as file:
        #     file.write(filedata)
        # os.remove('fig.png')
        self.clusters = output

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
        return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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

    def is_psd_plotted(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.psd is not None

    def is_time_freq_plotted(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.time_freq is not None

    def contains_summary(self, QModelIndex):
        signal = self.get_signal(QModelIndex)
        return signal.summary is not None


