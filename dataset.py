import os
from itertools import islice
from signal import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject


class Dataset(QObject):

    signal_loaded_signal = pyqtSignal(object)

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
            print("ostie")
            while len(lines) == 5:
                name = lines[0]
                typeofsignal = lines[1]
                samplingrate = int(lines[2])
                time_array = np.fromstring(lines[3].strip(), dtype=np.float32, sep=", ")
                samples_array = np.fromstring(lines[4].strip(), dtype=np.float32, sep=", ")
                sig = Signal(samples_array, time_array=time_array, name=name, type=typeofsignal)
                self.signals_dictionary[sig.id] = sig
                lines = self.readnextlines(fileObject, 5)
            print("file loaded")

    def loadFromSimulation(self, samples_array, time_array, fs, namee, type):
        sig = Signal(samples_array, time_array=time_array, fs=fs, name=name, type=type)
        self.signals_dictionary[sig.id] = sig

    def readnextlines(self, fileObject, n):
        return [x.strip() for x in islice(fileObject, n)]


