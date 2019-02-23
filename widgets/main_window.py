import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from widgets.eeg_sim_widget import EEGSimulationWidget
from widgets.ecg_sim_widget import ECGSimulationWidget
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/main.ui')
MainWindowView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class MainWindow(TemplateBaseClass):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowView()
        self.ui.setupUi(self)

        self.ui.main_tab.setEnabled(True)
        # self.ui.oscilloscope_tab.display_graph([1,2,3,4,5,6,7,8,9,10], np.transpose([-10,0,4,1,2,7,5,3,8,0]))
        # self.ui.oscilloscope_tab.display_graph([0,1,2,3,4,5,6,7,8,9,20], np.transpose([1,5,3,8,9,24,2,5,12,10,33]))

        self.ui.actionEEG_Simulation.triggered.connect(self.launch_eeg_widget)
        self.ui.actionECG_Simulation.triggered.connect(self.launch_ecg_widget)

    def launch_eeg_widget(self):
        eeg_sim_widget = EEGSimulationWidget()
        eeg_sim_widget.exec_()

    def launch_ecg_widget(self):
        ecg_sim_widget = ECGSimulationWidget()
        ecg_sim_widget.exec_()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())