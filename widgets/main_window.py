import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
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

        self.init_ui()

        self.ui.actionEEG_Simulation.triggered.connect(self.launch_eeg_widget)
        self.ui.actionECG_Simulation.triggered.connect(self.launch_ecg_widget)

    def launch_eeg_widget(self):
        eeg_sim_widget = EEGSimulationWidget()
        eeg_sim_widget.exec_()

    def launch_ecg_widget(self):
        ecg_sim_widget = ECGSimulationWidget()
        ecg_sim_widget.exec_()

    def init_ui(self):
        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setText('Testing trying to output something\nWith a new line')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())