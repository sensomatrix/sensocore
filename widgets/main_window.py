import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
from widgets.firdesignerdiag import FIRDesignerDialog
from widgets.physionet_widget import PhysioNetWidget
from models.signal import SignalListModel
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

        self.ui.channels.setModel(self.signals)

        self.ui.main_tab.setEnabled(False)

        self.ui.actionEEG_Simulation.triggered.connect(self.launch_eeg_widget)
        self.ui.actionECG_Simulation.triggered.connect(self.launch_ecg_widget)
        self.ui.actionFIR_Filter_Designer.triggered.connect(self.launch_fir_filter_widget)
        self.ui.actionPhysioNet.triggered.connect(self.launch_physionet_widget)

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
        fir_filter = FIRDesignerDialog()
        fir_filter.exec_()

    def plot_signals(self, signals):
        for signal in signals:
            self.plot_signal(signal)

    def plot_signal(self, signal):
        if not self.ui.main_tab.isEnabled():
            self.ui.main_tab.setEnabled(True)

        self.ui.oscilloscope_tab.display_graph(signal.time_array, np.transpose(signal.samples_array))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())