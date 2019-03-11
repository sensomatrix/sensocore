import os
from itertools import islice
from models.signal import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject


# dialog used to load a complete dataset. to do: deal with the case user clicks on "cancel"
def open_dataset_dialog(parent):
    openfilepath = QFileDialog.getOpenFileName(parent)
    if openfilepath[0]:
        return load_from_file(openfilepath[0])
        # for signal in signals:
        #     self.signal_loaded_signal.emit(sig)
        # self.parent.info.set_opened_filename(os.path.basename(openfilepath[0]))

def load_from_file(path_to_file):
    signals = []
    with open(path_to_file, 'r') as fileObject:
        lines = readnextlines(fileObject, 5)
        while len(lines) == 5:
            name = lines[0]
            typeofsignal = lines[1]
            samplingrate = int(lines[2])
            time_array = (np.asarray(lines[3].split(", "))).astype(np.float32)
            samples_array = (np.asarray(lines[4].split(", "))).astype(np.float32)
            sig = Signal(samples_array, time_array=time_array, name=name, signal_type=typeofsignal, fs=samplingrate)
            signals.append(sig)
            lines = readnextlines(fileObject, 5)

    return signals

    # def loadFromSimulation(self, samples_array, time_array, fs, name, type):
    #     sig = Signal(samples_array, time_array=time_array, fs=fs, name=name, type=type)
    #     self.signals_dictionary[sig.id] = sig
    #     self.signal_loaded_signal.emit(sig)
    #
    # def addSignaltoDataset(self, signal):
    #     self.signals_dictionary[signal.id] = signal
    #     self.signal_loaded_signal.emit(signal)
    #
def readnextlines(fileObject, n):
    return [x.strip() for x in islice(fileObject, n)]
    #
    # def getSignalsList(self):
    #     return self.signals_dictionary
    #
    # def removeDC(self, id_):
    #     self.signals_dictionary.get(id_).removeDC()
    #     self.signal_changed_signal.emit(id_)
    #
    # def changeSamplesArray(self, id_, new_samples_array):
    #     self.signals_dictionary.get(id_).samples_array = new_samples_array
    #     self.signal_changed_signal.emit(id_)

