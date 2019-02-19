from simulation.eeg.jansen import simulate_eeg_jansen
from PyQt5.Qt import pyqtSignal
from PyQt5.QtCore import QObject


class EEGSimulationModel(QObject):
    updated = pyqtSignal()

    def __init__(self, c1, fs, noise, duration):
        QObject.__init__(self)
        self._c1 = c1
        self._fs = fs
        self._noise = noise
        self._duration = duration
        self.time = None
        self.output = None
        self.generate_signal_for_plotting()

    def update_signal(self):
        self.generate_signal_for_plotting()
        self.updated.emit()

    def generate_signal_for_plotting(self):
        # Difference between this and create_signal is
        # This one uses the default time for faster preview time
        self.time, self.output = simulate_eeg_jansen(fs=self._fs, C1=self._c1, noise_magnitude=self._noise)

    def create_signal(self):
        self.time, self.output = simulate_eeg_jansen(self._duration, self._fs, self._c1, self._noise)

    def set_c1(self, value):
        self._c1 = value

    def set_noise(self, value):
        self._noise = value

    def set_sampling_frequency(self, value):
        self._fs = value

    def set_duration(self, value):
        self._duration = value
