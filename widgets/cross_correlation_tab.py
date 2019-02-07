from PyQt5.QtWidgets import QWidget, QVBoxLayout
from widgets.cross_correlation import CrossCorrelation
from scipy import signal
import numpy as np
import weakref
from PyQt5.Qt import Qt

class CrossCorrelationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.signal_1 = CrossCorrelation()
        self.signal_2 = CrossCorrelation()
        self.output = CrossCorrelation()
        self.setAttribute(Qt.WA_DeleteOnClose)

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
            signal1_normalized_samples = (signal_1.samples_array - np.mean(signal_1.samples_array)) / (
                        np.std(signal_1.samples_array) * signal_1.samples_array.size)
            signal2_normalized_samples = (signal_2.samples_array - np.mean(signal_2.samples_array)) / (
                np.std(signal_2.samples_array))
            corr = signal.correlate(signal1_normalized_samples, signal2_normalized_samples, mode='full')
            weakcorr = weakref.proxy(corr)
            offsets = -(np.arange(weakcorr.size) - signal1_normalized_samples.size + 1) / signal_1.fs
            self.output.plot_data(offsets, weakcorr,
                                  title='Cross-correlation of ' + signal_1.name + " and " + signal_2.name)
        else:
            print('not cool')

    def cleanup(self):
        self.signal_1.destroyPlots()
        self.signal_2.destroyPlots()
        self.output.destroyPlots()
        del self.signal_1
        del self.signal_2
        del self.output