import pyqtgraph as pg
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from models.patient import PatientListModel
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
from widgets.firdesignerdiag import FIRDesignerDialog
from widgets.physionet_widget import PhysioNetWidget
from widgets.ecg_summary_widget import ECGSummaryWidget
from widgets.eeg_summary_widget import EEGSummaryWidget
from models.signal import SignalListModel
from utils import file_read
from utils.frequtils import compute_psd
from utils.file_write import write_edf
import numpy as np
import os
import sys
from datetime import datetime as dt

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/main.ui')
MainWindowView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class MainWindow(TemplateBaseClass):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowView()
        self.ui.setupUi(self)

        self.ecg_sim_count = 0
        self.eeg_sim_count = 0
        self.patients = PatientListModel()
        self.signals = SignalListModel(self)
        self.signals.added_signal.connect(self.plot_signal)
        self.signals.added_signals.connect(self.plot_signals)
        self.signals.plot_psd_signal.connect(self.plot_psd_secondary)
        self.signals.plot_time_freq_signal.connect(self.plot_time_freq_secondary)
        self.signals.update_plot.connect(self.update_plot)
        self.signals.plot_ecg_summary.connect(self.launch_ecg_summary)
        self.signals.plot_eeg_summary.connect(self.launch_eeg_summary)
        self.signals.cross_correlation_signal.connect(self.launch_cross_corr)
        self.signals.removed_signal.connect(self.delete_plot)
        self.patients.patientCreated.connect(self.fill_widget)

        self.ui.oscilloscope_tab.region_updated.connect(self.display_psd)
        self.ui.oscilloscope_tab.region_cleared.connect(self.clear_psd)
        self.ui.oscilloscope_tab.create_signal.connect(self.create_signal)

        self.ui.channels.setModel(self.signals)

        self.ui.main_tab.setEnabled(False)

        self.ui.actionEEG_Simulation.triggered.connect(self.launch_eeg_widget)
        self.ui.actionECG_Simulation.triggered.connect(self.launch_ecg_widget)
        self.ui.actionFIR_Filter_Designer.triggered.connect(self.launch_fir_filter_widget)
        self.ui.actionPhysioNet.triggered.connect(self.launch_physionet_widget)
        self.ui.actionLocally.triggered.connect(self.launch_local_file)

        self.ui.spectrum_view_plot.setTitle('Spectrum View')
        self.ui.spectrum_view_plot.setLabel('left', text='PSD', units='V^2/Hz')
        self.ui.spectrum_view_plot.setLabel('bottom', text='Frequency', units='Hz')
        self.ui.spectrum_view_plot.showGrid(x=True, y=True)

    def launch_ecg_summary(self, ecg, raw):
        ecg_summary_widget = ECGSummaryWidget(ecg, raw)
        ecg_summary_widget.exec_()

    def launch_eeg_summary(self, eeg, raw):
        eeg_summary_widget = EEGSummaryWidget(eeg, raw)
        eeg_summary_widget.exec_()

    def launch_eeg_widget(self):
        eeg_sim_widget = EEGSimulationWidget(self.signals, self.eeg_sim_count)
        eeg_sim_widget.exec_()

        if eeg_sim_widget.signal_added:
            self.eeg_sim_count += 1

    def launch_ecg_widget(self):
        ecg_sim_widget = ECGSimulationWidget(self.signals, self.ecg_sim_count)
        ecg_sim_widget.exec_()

        if ecg_sim_widget.signal_added:
            self.ecg_sim_count += 1

    def launch_cross_corr(self, signal_1, signal_2):
        self.ui.main_tab.setCurrentIndex(1)
        self.ui.cross_correlation_tab.set_signals(signal_1, signal_2)

    def launch_physionet_widget(self):
        physionet = PhysioNetWidget(self.signals)
        physionet.exec_()

    def launch_fir_filter_widget(self):
        if not self.signals.is_list_empty():
            fir_filter = FIRDesignerDialog(self.signals)
            fir_filter.exec_()
        else:
            no_signals_message_box = QMessageBox()
            no_signals_message_box.setIcon(QMessageBox.Warning)
            no_signals_message_box.setText("There is no signal to filter")
            no_signals_message_box.setWindowTitle("FIR Filter Warning")
            no_signals_message_box.setStandardButtons(QMessageBox.Ok)
            no_signals_message_box.exec_()

    def launch_local_file(self):
        signals = file_read.open_dataset_dialog(self)
        if signals is not None:
            self.signals.add_signals(signals)

    def plot_signals(self, signals):
        for signal in signals:
            self.plot_signal(signal)

    def plot_signal(self, signal):
        if not self.ui.main_tab.isEnabled():
            self.ui.main_tab.setEnabled(True)

        self.ui.oscilloscope_tab.display_graph(signal)

    def plot_psd_secondary(self, signal):
        self.ui.secondary_area.plot_psd_slot(signal)

    def display_psd(self, output, index):

        fs = self.signals.data(self.signals.index(index)).fs

        fbins, pxx = compute_psd(output, fs)

        self.ui.spectrum_view_plot.clear()
        self.ui.spectrum_view_plot.setTitle('Spectrum View')
        self.ui.spectrum_view_plot.plot(fbins, pxx)

    def plot_time_freq_secondary(self, signal):
        self.ui.secondary_area.plot_tf_slot(signal)

    def clear_psd(self):
        self.ui.spectrum_view_plot.clear()
        self.ui.spectrum_view_plot.setTitle('Spectrum View')

    def update_plot(self, signal, index):
        self.ui.oscilloscope_tab.update_plot(signal.time_array, np.transpose(signal.current_mode), index)

    def delete_plot(self, signal, index):
        self.ui.oscilloscope_tab.delete_plot(index)
        self.ui.secondary_area.delete_signal(signal)

        if self.signals.rowCount() == 0:
            self.ui.main_tab.setEnabled(False)

    def create_signal(self, output, index):
        self.signals.create_child_signal(output, index)

    def fill_item(self, item, value):
        # part of this code was taken from
        # https://stackoverflow.com/questions/21805047/qtreewidget-to-mirror-python-dictionary
        if isinstance(value, dict):
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                child.setToolTip(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)
        elif isinstance(value, list):
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, list(val.keys())[0])
                    child.setToolTip(0, list(val.keys())[0])
                    self.fill_item(child, list(val.values())[0])
                elif type(val) is list:
                    child.setText(0, '[list]')
                    child.setToolTip(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, str(val))
                    child.setToolTip(0, str(val))
        else:
            child = QTreeWidgetItem()
            child.setText(0, str(value))
            child.setToolTip(0, str(value))
            item.addChild(child)

    def fill_widget(self, patient):
        d = patient.patient_info
        self.fill_item(self.patient_tree_widget.invisibleRootItem(), d)

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)

        if reply == QMessageBox.Close:
            sys.exit()
        elif reply == QMessageBox.Save and len(self.signals._signals) != 0:
            write_edf(self.signals._signals, str(dt.now()) + '.edf')
            sys.exit()
        else:
            event.ignore()

    @property
    def patient_tree_widget(self):
        return self.ui.treeWidgetPatient