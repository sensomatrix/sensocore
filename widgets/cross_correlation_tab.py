from PyQt5.QtWidgets import QWidget, QVBoxLayout
from widgets.cross_correlation import CrossCorrelation
from scipy import signal
import numpy as np


class CrossCorrelationTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.signal_1 = CrossCorrelation(self)
        self.signal_2 = CrossCorrelation(self)
        self.output = CrossCorrelation(self)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.signal_1)
        vbox.addWidget(self.signal_2)
        vbox.addWidget(self.output)

    def find_item_index(self, item, items):
        for _item, i in enumerate(items):
            if _item == item:
                return i

    def computeCrossCor(self, signal_1, signal_2):

        if signal_1 is not None and signal_2 is not None:
            print('cool')
            self.signal_1.plot_data(signal_1.time_array, signal_1.samples_array, title=signal_1.name)
            self.signal_2.plot_data(signal_2.time_array, signal_2.samples_array, title=signal_2.name)
            signal1_normalized_samples = (signal_1.samples_array - np.mean(signal_1.samples_array)) / (np.std(signal_1.samples_array) * signal_1.samples_array.size)
            signal2_normalized_samples = (signal_2.samples_array - np.mean(signal_2.samples_array)) / (np.std(signal_2.samples_array))
            corr = signal.correlate(signal1_normalized_samples, signal2_normalized_samples, mode='full')
            x_corr_idx = np.arange(corr.size)
            samples_shift = x_corr_idx - signal1_normalized_samples.size + 1
            offsets = -samples_shift / signal_1.fs
            self.output.plot_data(offsets, corr, title='Cross-correlation of ' + signal_1.name + " and " + signal_2.name)
        else:
            print('not cool')
