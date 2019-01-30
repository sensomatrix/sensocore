from numpy import random
from scipy.signal import welch, spectrogram

class Signal:
    # function to generate time array out of fs is not implemented yet

    id_list = [] # class-wide list that contains list of already-assigned unique IDs

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
        self.PSDfbins, self.PSDxx = self.compute_psd(self.samples_array, self.fs)
        self.TFf, self.Tft, self.TFSxx = self.compute_time_freq(self.samples_array, self.fs)

    def compute_psd(self, samplesarray, fs):
        fbins, pxx = welch(samplesarray, fs=fs, nperseg=int(min((fs, len(samplesarray)))))
        return fbins, pxx

    def compute_time_freq(self, samplesarray, fs):
        f, t, Sxx = spectrogram(samplesarray, fs)
        return f, t, Sxx