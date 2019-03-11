import pyqtgraph as pg
import os
import numpy as np


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/ecg_summary.ui')
ECGSummaryView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class ECGSummaryWidget(TemplateBaseClass):
    def __init__(self, ecg, raw):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = ECGSummaryView()
        self.ui.setupUi(self)

        self.ui.raw.plot(ecg[0], raw, pen='r')
        self.ui.raw.setLabel('left', "Amplitude", units='A')
        self.ui.raw.setLabel('bottom', "Time", units='s')

        self.ui.filtered.plot(ecg[0], ecg[1], pen='g')
        self.ui.filtered.setLabel('left', "Amplitude", units='A')
        self.ui.filtered.setLabel('bottom', "Time", units='s')

        self.ui.hrv.plot(ecg[5], ecg[6], pen='y')
        self.ui.hrv.setLabel('left', "Heart Rate")
        self.ui.hrv.setLabel('bottom', "Time", units='s')

        t = ecg[4].T
        template = np.zeros(t.shape[0])
        for index, row in enumerate(t):
            template[index] = row[0]
        self.ui.template_plot.plot(ecg[3], template, pen='w')
        self.show()
