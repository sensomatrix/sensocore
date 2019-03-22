import pyqtgraph as pg
import os
import numpy as np
import copy


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/eeg_summary.ui')
EEGSummaryView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class EEGSummaryWidget(TemplateBaseClass):
    def __init__(self, eeg, raw):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = EEGSummaryView()
        self.ui.setupUi(self)

        self.ui.raw.plot(eeg[0], raw, pen='r')
        self.ui.raw.setLabel('left', "Amplitude", units='A')
        self.ui.raw.setLabel('bottom', "Time", units='s')
        self.ui.raw.getViewBox().setMouseEnabled(y=False)

        time = copy.deepcopy(eeg[0])
        time = np.reshape(time, (time.size, 1))

        filtered = np.hstack([time, eeg[1]])

        self.ui.filtered.plot(filtered, pen='g')
        self.ui.filtered.setLabel('left', "Amplitude", units='A')
        self.ui.filtered.setLabel('bottom', "Time", units='s')
        self.ui.filtered.getViewBox().setMouseEnabled(y=False)

        theta_band = np.linspace(4, 8, eeg[3].size)
        alpha_low_band = np.linspace(8, 10, eeg[4].size)
        alpha_high_band = np.linspace(10, 13, eeg[5].size)
        beta_band = np.linspace(13, 25, eeg[6].size)
        gamma_band = np.linspace(25, 40, eeg[7].size)

        self.ui.theta.plot(theta_band, eeg[3].reshape((eeg[3].size,)), pwn='w')
        self.ui.theta.setLabel('left', "Amplitude", units='A')
        self.ui.theta.setLabel('bottom', "Frequency", units='Hz')
        self.ui.theta.getViewBox().setMouseEnabled(y=False)

        self.ui.alpha_low.plot(alpha_low_band, eeg[4].reshape((eeg[4].size,)), pen='w')
        self.ui.alpha_low.setLabel('left', "Amplitude", units='A')
        self.ui.alpha_low.setLabel('bottom', "Frequency", units='Hz')
        self.ui.alpha_low.getViewBox().setMouseEnabled(y=False)

        self.ui.alpha_high.plot(alpha_high_band, eeg[5].reshape((eeg[5].size,)), pen='w')
        self.ui.alpha_high.setLabel('left', "Amplitude", units='A')
        self.ui.alpha_high.setLabel('bottom', "Frequency", units='Hz')
        self.ui.alpha_high.getViewBox().setMouseEnabled(y=False)

        self.ui.beta.plot(beta_band, eeg[6].reshape((eeg[6].size,)), pen='w')
        self.ui.beta.setLabel('left', "Amplitude", units='A')
        self.ui.beta.setLabel('bottom', "Frequency", units='Hz')
        self.ui.beta.getViewBox().setMouseEnabled(y=False)

        self.ui.gamma.plot(gamma_band, eeg[7].reshape((eeg[7].size,)), pen='w')
        self.ui.gamma.setLabel('left', "Amplitude", units='A')
        self.ui.gamma.setLabel('bottom', "Frequency", units='Hz')
        self.ui.gamma.getViewBox().setMouseEnabled(y=False)

        self.show()
