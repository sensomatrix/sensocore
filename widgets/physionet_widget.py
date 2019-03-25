from wfdb import rdrecord, rdann
from models.signal import Signal
from utils.timeutils import generate_time_array
import pyqtgraph as pg
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from pathlib import Path
import numpy as np
import wget
import os
from utils.file_read import load_from_edf


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
        self.ui.ecg.toggled.connect(self.toggle_annotate)

    def toggle_annotate(self, checked):
        self.ui.annotate_checkbox.setEnabled(checked)

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
            except:
                home = str(Path.home())
                bio_signals_path = os.path.join(home, 'Bio Signals')
                path = os.path.join(bio_signals_path, '{0}.edf'.format(self.record_name))
                if not os.path.exists(path):
                    wget.download(self.url_link + self.record_name + '.edf', os.path.join(home, 'Bio Signals'))
                signals = load_from_edf(path, self.ui.sample_from.value(), self.ui.sample_to.value())

                self.signals.add_signals(signals)

            self.close()

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