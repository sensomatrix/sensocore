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

        # (ts, filtered, rpeaks, ts_tmpl, templates, ts_hr, hr)

        self.ui.raw.plot(ecg[0], raw)
        self.ui.filtered.plot(ecg[0], ecg[1])
        self.ui.hrv.plot(ecg[5], ecg[6])
        T = ecg[4].T
        template = np.zeros(T.shape[0])
        for index, row in enumerate(T):
            template[index] = row[0]
        self.ui.template_plot.plot(ecg[3], template)
        self.show()
