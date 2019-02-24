from wfdb import rdrecord
from models.signal import Signal
from utils.timeutils import generateTimeArrayFromNumberOfSamples
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal
import os


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
            sig_samples = record.p_signal[:, index]
            sig_timearray = generateTimeArrayFromNumberOfSamples(fs, sig_samples.size)
            sig = Signal(sig_samples,
                         time_array=sig_timearray,
                         fs=fs,
                         name=sig_name,signal_type='no type')
            siglist.append(sig)

        self.signals.add_signals(siglist)

        self.close()

    @property
    def url_link(self):
        return self.ui.physionet_url_line_edit.text()
    
    @property
    def record_name(self):
        return self.ui.record_name_line_edit.text()
