from views.cross_correlation import Ui_Form
from PyQt5.QtWidgets import QWidget
import weakref
from scipy import signal
import numpy as np


class CrossCorrelation(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def compute_cross_correlation(self, signal_1, signal_2):
        if signal_1 is not None and signal_2 is not None:
            self.ui.signal_1_plot.plotItem.plot(signal_1.time_array, signal_1.samples_array, title=signal_1.name)
            self.ui.signal_1_plot.plotItem.plot(signal_2.time_array, signal_2.samples_array, title=signal_2.name)
            signal1_normalized_samples = (signal_1.samples_array - np.mean(signal_1.samples_array)) / (
                        np.std(signal_1.samples_array) * signal_1.samples_array.size)
            signal2_normalized_samples = (signal_2.samples_array - np.mean(signal_2.samples_array)) / (
                np.std(signal_2.samples_array))
            corr = signal.correlate(signal1_normalized_samples, signal2_normalized_samples, mode='full')
            weakcorr = weakref.proxy(corr)
            offsets = -(np.arange(weakcorr.size) - signal1_normalized_samples.size + 1) / signal_1.fs
            self.ui.cross_correlatoion_plot.plotItem.plot(offsets, weakcorr,
                                  title='Cross-correlation of ' + signal_1.name + " and " + signal_2.name)

    def cleanup(self):
        self.signal_1.destroyPlots()
        self.signal_2.destroyPlots()
        self.output.destroyPlots()
        del self.signal_1
        del self.signal_2
        del self.output