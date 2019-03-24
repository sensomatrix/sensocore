import weakref
from scipy import signal
import numpy as np
import pyqtgraph as pg
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/cross_correlation.ui')
CrossCorrelationView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class CrossCorrelationWidget(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)

        self.ui = CrossCorrelationView()
        self.ui.setupUi(self)
        self.signal_1 = None
        self.signal_2 = None

    def set_signals(self, signal_1, signal_2):
        self.signal_1 = signal_1
        self.signal_2 = signal_2
        self.compute_cross_correlation()

    def compute_cross_correlation(self):
        self.ui.signal_1_plot.clear()
        self.ui.signal_2_plot.clear()
        self.ui.cross_correlatoion_plot.clear()

        self.ui.signal_1_plot.plotItem.plot(self.signal_1.time_array, self.signal_1.current_mode, pen='g', title=self.signal_1.name)
        self.ui.signal_2_plot.plotItem.plot(self.signal_2.time_array, self.signal_2.current_mode, pen='r', title=self.signal_2.name)
        signal1_normalized_samples = (self.signal_1.current_mode - np.mean(self.signal_1.current_mode)) / (
                    np.std(self.signal_1.current_mode) * self.signal_1.current_mode.size)
        signal2_normalized_samples = (self.signal_2.current_mode - np.mean(self.signal_2.current_mode)) / (
            np.std(self.signal_2.current_mode))
        corr = signal.correlate(signal1_normalized_samples, signal2_normalized_samples, mode='full')
        weakcorr = weakref.proxy(corr)
        offsets = -(np.arange(weakcorr.size) - signal1_normalized_samples.size + 1) / self.signal_1.fs
        self.ui.cross_correlatoion_plot.plotItem.plot(offsets, weakcorr,
                              title='Cross-correlation of ' + self.signal_1.name + " and " + self.signal_2.name)
        self.ui.cross_correlatoion_plot.autoRange()

    # def cleanup(self):
    #     self.signal_1.destroyPlots()
    #     self.signal_2.destroyPlots()
    #     self.output.destroyPlots()
    #     del self.signal_1
    #     del self.signal_2
    #     del self.output