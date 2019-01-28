import os
from itertools import islice
from signal import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog


class Dataset():

    def __init__(self, parent):
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
        
    def open_dataset_dialog(self):
        openfilepath = QFileDialog.getOpenFileName(self.parent)
        self.parent.datasets.load_from_file(openfilepath[0])
        for id, signal in self.parent.datasets.signals_dictionary.items():
            self.parent.center.scope.addTrace(signal)
        self.parent.info.set_opened_filename(os.path.basename(openfilepath[0]))
        self.parent.center.scope.pw.resizeEvent(None)

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

    def readnextlines(self, fileObject, n):
        return [x.strip() for x in islice(fileObject, n)]


