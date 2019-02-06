import os
from itertools import islice
from signalobject import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject


class Dataset(QObject):

    signal_loaded_signal = pyqtSignal(object)
    signal_changed_signal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.signals_dictionary = {}
        self.actions = None
        self.create_action()
        
    def create_action(self):
        output = {}
        act = QAction('Load dataset', self.parent)
        act.triggered.connect(self.open_dataset_dialog)
        output['open_dataset'] = act
        self.actions = output

    # dialog used to load a complete dataset. to do: deal with the case user clicks on "cancel"
    def open_dataset_dialog(self):
        openfilepath = QFileDialog.getOpenFileName(self.parent)
        if openfilepath[0]:
            self.load_from_file(openfilepath[0])
            for sig in self.signals_dictionary.values():
                self.signal_loaded_signal.emit(sig)
            self.parent.info.set_opened_filename(os.path.basename(openfilepath[0]))

    def load_from_file(self, path_to_file):
        with open(path_to_file, 'r') as fileObject:
            lines = self.readnextlines(fileObject, 5)
            while len(lines) == 5:
                name = lines[0]
                typeofsignal = lines[1]
                samplingrate = int(lines[2])
                time_array = (np.asarray(lines[3].split(", "))).astype(np.float32)
                samples_array = (np.asarray(lines[4].split(", "))).astype(np.float32)
                sig = Signal(samples_array, time_array=time_array, name=name, type=typeofsignal)
                self.signals_dictionary[sig.id] = sig
                lines = self.readnextlines(fileObject, 5)

    def loadFromSimulation(self, samples_array, time_array, fs, name, type):
        sig = Signal(samples_array, time_array=time_array, fs=fs, name=name, type=type)
        self.signals_dictionary[sig.id] = sig
        self.signal_loaded_signal.emit(sig)

    def addSignaltoDataset(self, signal):
        self.signals_dictionary[signal.id] = signal
        self.signal_loaded_signal.emit(signal)

    def readnextlines(self, fileObject, n):
        return [x.strip() for x in islice(fileObject, n)]

    def getSignalsList(self):
        return self.signals_dictionary

    def removeDC(self, id_):
        self.signals_dictionary.get(id_).removeDC()
        self.signal_changed_signal.emit(id_)

    def changeSamplesArray(self, id_, new_samples_array):
        self.signals_dictionary.get(id_).samples_array = new_samples_array
        self.signal_changed_signal.emit(id_)


