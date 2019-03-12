from wfdb import rdrecord
from models.signal import Signal
from utils.timeutils import generateTimeArrayFromNumberOfSamples
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal
import os
import numpy as np


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/physionet.ui')
PhysioNetView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class PhysioNetWidget(TemplateBaseClass):
    def __init__(self, signals=None):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = PhysioNetView()
        self.ui.setupUi(self)

        self.signals = signals

        self.ui.import_button.clicked.connect(self.import_from_physio)

    def import_from_physio(self):
        try:
            pb_dir = self.url_link.split("database/",1)[1]

            record = rdrecord(self.record_name, pb_dir=pb_dir)
        except:
            raise
        fs = record.fs
        # comments = record.comments TODO: Get comments and store them
        siglist = []
        for index, channel in enumerate(record.sig_name):
            sig_name = channel
            sig_samples = record.p_signal[:, index].reshape(record.p_signal.size, 1)
            sig_timearray = generateTimeArrayFromNumberOfSamples(fs, sig_samples.size).reshape(sig_samples.size, 1)

            output = np.hstack([sig_timearray, sig_samples])

            sig = Signal(output,
                         fs=fs,
                         name='Physionet {0} Signal'.format(sig_name), signal_type=sig_name)
            siglist.append(sig)

        self.signals.add_signals(siglist)

        self.close()

    @property
    def url_link(self):
        return self.ui.physionet_url_line_edit.text()
    
    @property
    def record_name(self):
        return self.ui.record_name_line_edit.text()
