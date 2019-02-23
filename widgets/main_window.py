import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
from widgets.firdesignerdiag import FIRDesignerDialog
from widgets.physionet_widget import PhysioNetWidget
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

        self.ui.main_tab.setEnabled(False)

        self.ui.actionEEG_Simulation.triggered.connect(self.launch_eeg_widget)
        self.ui.actionECG_Simulation.triggered.connect(self.launch_ecg_widget)
        self.ui.actionFIR_Filter_Designer.triggered.connect(self.launch_fir_filter_widget)
        self.ui.actionPhysioNet.triggered.connect(self.launch_physionet_widget)

    def launch_eeg_widget(self):
        # TODO: Provide parent
        eeg_sim_widget = EEGSimulationWidget()
        eeg_sim_widget.create_signal.connect(self.ui.channels.on_signal_loaded)
        eeg_sim_widget.create_signal.connect(self.plot_signal)
        eeg_sim_widget.exec_()

    def launch_ecg_widget(self):
        # TODO: Provide parent
        ecg_sim_widget = ECGSimulationWidget()
        ecg_sim_widget.create_signal.connect(self.ui.channels.on_signal_loaded)
        ecg_sim_widget.create_signal.connect(self.plot_signal)
        ecg_sim_widget.exec_()

    def launch_physionet_widget(self):
        physionet = PhysioNetWidget(self)
        physionet.create_signal.connect(self.ui.channels.on_signal_loaded)
        physionet.create_signal.connect(self.plot_signal)
        physionet.exec_()

    def launch_fir_filter_widget(self):
        fir_filter = FIRDesignerDialog(self)
        fir_filter.exec_()

    def plot_signal(self, signals):
        if not self.ui.main_tab.isEnabled():
            self.ui.main_tab.setEnabled(True)

        for signal in signals:
            self.ui.oscilloscope_tab.display_graph(signal.time_array, np.transpose(signal.samples_array))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())