from views.main import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from controllers.ecg_sim_controller import ECGSimController
from controllers.eeg_sim_controller import EEGSimController
from controllers.fir_filter_controller import FIRFilterDesignerController
from itertools import cycle
from models.signal import SignalListModel
from pyqtgraph.metaarray import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._current_item_size = 0

        self.model = SignalListModel(parent=self)

        self._latest_element = 0
        color_list = ['r', 'g', 'b', 'c', 'm', 'k']
        self.colorpool = cycle(color_list)

        self.init_ui()
        self.init_connections()

    def init_ui(self):
        self.ui.channel_listview.setModel(self.model)

        self.ui.graphicsView.setBackground('w')
        self.ui.graphicsView.setMinimumPlotHeight(100)

        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setText('Testing trying to output something\nWith a new line')

    def init_connections(self):
        self.ui.actionECG_Simulation.triggered.connect(self.open_ecg_simulation)
        self.ui.actionEEG_Simulation.triggered.connect(self.open_eeg_simulation)
        self.ui.actionFIR_Filter_Designer.triggered.connect(self.open_fir_filter)

    def add_signal(self, signal):
        self.model.insertRows(self._current_item_size, self._current_item_size + 1, 'signal', signal)
        self._current_item_size += 1

        self.add_trace(signal)

    def add_trace(self, signal):
        data_buffer = np.zeros((1, signal.samples_array.size))
        for i in range(signal.samples_array.size):
            data_buffer[0][i] = signal.samples_array[i]

        ma = MetaArray(data_buffer, info=[{"cols": [{"name": signal.name}]},
                                          {"name": "Time", "units": "sec",
                                           "values": signal.time_array}])

        self.ui.graphicsView.mPlotItem.plot(ma)

    def open_ecg_simulation(self):
        ecg_controller = ECGSimController()
        ecg_controller.signal_created.connect(self.add_signal)
        ecg_controller.exec_()

    def open_eeg_simulation(self):
        eeg_controller = EEGSimController()
        eeg_controller.signal_created.connect(self.add_signal)
        eeg_controller.exec_()

    def open_fir_filter(self):
        fir_filter = FIRFilterDesignerController(self.model)
        fir_filter.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())