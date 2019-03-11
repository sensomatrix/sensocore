import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
from widgets.firdesignerdiag import FIRDesignerDialog
from widgets.physionet_widget import PhysioNetWidget
from widgets.ecg_summary_widget import ECGSummaryWidget
from models.signal import SignalListModel
from utils import file_read
from PyQt5.QtCore import QModelIndex
from utils.frequtils import compute_psd
import numpy as np
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/main.ui')
MainWindowView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class MainWindow(TemplateBaseClass):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowView()
        self.ui.setupUi(self)

        self.signals = SignalListModel(self)
        self.signals.added_signal.connect(self.plot_signal)
        self.signals.added_signals.connect(self.plot_signals)
        self.signals.plot_psd_signal.connect(self.plot_psd_secondary)
        self.signals.plot_time_freq_signal.connect(self.plot_time_freq_secondary)
        self.signals.update_plot.connect(self.update_plot)
        self.signals.plot_ecg_summary.connect(self.launch_ecg_summary)

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

    def launch_ecg_summary(self, ecg, raw):
        ecg_summary_widget = ECGSummaryWidget(ecg, raw)
        ecg_summary_widget.exec_()

    def launch_eeg_widget(self):
        eeg_sim_widget = EEGSimulationWidget(self.signals)
        eeg_sim_widget.exec_()

    def launch_ecg_widget(self):
        ecg_sim_widget = ECGSimulationWidget(self.signals)
        ecg_sim_widget.exec_()

    def launch_physionet_widget(self):
        physionet = PhysioNetWidget(self.signals)
        physionet.exec_()

    def launch_fir_filter_widget(self):
        fir_filter = FIRDesignerDialog(self.signals)
        fir_filter.exec_()

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

        self.ui.oscilloscope_tab.display_graph(signal.time_array, np.transpose(signal.raw))

    def plot_psd_secondary(self, signal):
        self.ui.secondary_area.plot_psd_slot(signal)

    def display_psd(self, output, index):

        fs = self.signals.data(self.signals.index(index)).fs

        fbins, pxx = compute_psd(output, fs)

        self.ui.spectrum_view_plot.clear()
        self.ui.spectrum_view_plot.plot(fbins, pxx)

    def plot_time_freq_secondary(self, signal):
        self.ui.secondary_area.plot_tf_slot(signal)

    def clear_psd(self):
        self.ui.spectrum_view_plot.clear()

    def update_plot(self, signal, index):
        self.ui.oscilloscope_tab.update_plot(signal.time_array, np.transpose(signal.current_mode), index)

    def create_signal(self, time, output, index):
        self.signals.create_child_signal(time, output, index)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())