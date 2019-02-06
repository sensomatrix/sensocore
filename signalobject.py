from numpy import random, mean
from PyQt5.QtCore import pyqtSignal

class Signal:
    # function to generate time array out of fs is not implemented yet

    id_list = [] # class-wide list that contains list of already-assigned unique IDs
    signalChanged = pyqtSignal(int)

    def __init__(self, samples_array, time_array=None, fs=None, name=None, type=None):
        super().__init__()
        self.id = random.randint(1,100)
        while self.id in Signal.id_list:
            self.id = random.randint(1,100)

        Signal.id_list.append(self.id)
        self.samples_array = samples_array
        self.name = name
        self.type = type
        if time_array is not None:
            self.time_array = time_array
            self.fs = 1/(time_array[1] - time_array[0])

    def removeDC(self):
        self.samples_array = self.samples_array - mean(self.samples_array)