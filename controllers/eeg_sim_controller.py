from views.eeg_sim import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSignal
from models.signal import Signal
from models.eeg_sim import EEGSimulationModel


class EEGSimController(QDialog):
    signal_created = pyqtSignal(Signal)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._eeg_sim = EEGSimulationModel(self.c1, self.sampling_frequency, self.noise_magnitude, self.duration)

        self.init_graph()
        self.init_connections()
        self.plot_eeg_signal()

    def init_graph(self):
        self.ui.graphicsView.setBackground('w')

    def init_connections(self):
        self.ui.c1_spinbox.valueChanged.connect(self._eeg_sim.set_c1)

        self.ui.sampling_frequency_spinbox.valueChanged.connect(self._eeg_sim.set_sampling_frequency)
        self.ui.noise_double_spinbox.valueChanged.connect(self._eeg_sim.set_noise)
        self.ui.duration_spinbox.valueChanged.connect(self._eeg_sim.set_duration)

        self.ui.reset_signal_button.clicked.connect(self.reset_values)
        self.ui.create_signal_button.clicked.connect(self.create_signal)
        self.ui.preview_button.clicked.connect(self.plot_eeg_signal)

        self._eeg_sim.updated.connect(self.plot_eeg_signal)

    def plot_eeg_signal(self):
        self._eeg_sim.generate_signal_for_plotting()
        self.ui.graphicsView.plotItem.clear()
        self.ui.graphicsView.plotItem.plot(self._eeg_sim.time, self._eeg_sim.output,
                                           pen='k')

    def reset_values(self):
        self.ui.c1_spinbox.setValue(135)

        self.ui.noise_double_spinbox.setValue(0)
        self.ui.sampling_frequency_spinbox.setValue(100)
        self.ui.duration_spinbox.setValue(10)
        self.ui.simulation_line_edit.clear()

    def create_signal(self):
        self._eeg_sim.create_signal()
        signal = Signal(self._eeg_sim.output, self._eeg_sim.time, self.sampling_frequency, self.name, 'EEG')
        self.signal_created.emit(signal)
        self.close()

    @property
    def c1(self):
        return self.ui.c1_spinbox.value()

    @property
    def sampling_frequency(self):
        return self.ui.sampling_frequency_spinbox.value()

    @property
    def noise_magnitude(self):
        return self.ui.noise_double_spinbox.value()

    @property
    def duration(self):
        return self.ui.duration_spinbox.value()

    @property
    def name(self):
        if self.ui.simulation_line_edit.text() is '':
            return 'EEG Signal'
        else:
            return self.ui.simulation_line_edit.text()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    eeg_sim = EEGSimController()

    eeg_sim.show()
    sys.exit(app.exec_())