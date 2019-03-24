from wfdb import rdrecord, rdann
from models.signal import Signal
from utils.timeutils import generate_time_array
import pyqtgraph as pg
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
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
        if self.ui.sample_from.value() >= self.ui.sample_to.value():
            self.showError('Sample from must be less than Sample to')
        else:
            try:
                pb_dir = self.url_link.split("database/", 1)[1]

                record = rdrecord(self.record_name, pb_dir=pb_dir,
                                  sampfrom=self.ui.sample_from.value(),
                                  sampto=self.ui.sample_to.value())

                annotations = None
                if self.ui.annotate_checkbox.isChecked():
                    annotations = rdann(self.record_name,
                                        'atr', pb_dir=pb_dir,
                                        sampfrom=self.ui.sample_from.value(),
                                        sampto=self.ui.sample_to.value())

                    for i in range(annotations.ann_len):
                        annotations.sample[i] -= self.ui.sample_from.value()

            except:
                raise
            fs = record.fs
            # comments = record.comments TODO: Get comments and store them
            siglist = []
            for index, channel in enumerate(record.sig_name):
                sig_name = channel
                sig_samples = record.p_signal[:, index].reshape(record.p_signal.shape[0], 1)

                if record.base_time is None:
                    record.base_time = '00:00:00'

                sig_timearray = generate_time_array(record.base_time,
                                                    self.ui.sample_to.value() - self.ui.sample_from.value(),
                                                    record.fs)

                sig_timearray = sig_timearray.reshape((sig_timearray.shape[0], 1))

                output = np.hstack([sig_timearray, sig_samples])

                self.close()

                signal_type = ''

                if self.ui.ecg.isChecked():
                    signal_type = 'ECG'
                elif self.ui.eeg.isChecked():
                    signal_type = 'EEG'

                sig = Signal(output,
                             fs=fs,
                             name='Physionet {0} Signal (Record {1})'.format(sig_name, self.record_name),
                             signal_type=signal_type,
                             annotations=annotations)
                siglist.append(sig)

            self.signals.add_signals(siglist)


    def showError(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec()

    @property
    def url_link(self):
        return self.ui.physionet_url_line_edit.text()
    
    @property
    def record_name(self):
        return self.ui.record_name_line_edit.text()