from views.ecg_sim import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSignal
from models.ecg_sim import ECGSimulationModel
from models.signal import Signal


class ECGSimController(QDialog):
    signal_created = pyqtSignal(Signal)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._ecg_sim = ECGSimulationModel(self.p_values, self.q_values, self.r_values, self.s_values,
                                           self.t_values, self.sampling_frequency, self.noise_magnitude,
                                           self.duration, self.period)

        self.init_graph()
        self.init_connections()
        self.plot_ecg_signal()

    def init_graph(self):
        self.ui.graphicsView.setBackground('w')

    def init_connections(self):
        self.ui.p_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_p_magnitude)
        self.ui.p_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_p_widthness)
        self.ui.p_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_p_time)

        self.ui.q1_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_q_1_magnitude)
        self.ui.q1_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_q_1_widthness)
        self.ui.q1_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_q_1_time)

        self.ui.q2_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_q_2_magnitude)
        self.ui.q2_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_q_2_widthness)
        self.ui.q2_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_q2_time)

        self.ui.r_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_r_magnitude)
        self.ui.r_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_r_widthness)
        self.ui.r_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_r_time)

        self.ui.s_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_s_magnitude)
        self.ui.s_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_s_widthness)
        self.ui.s_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_s_time)

        self.ui.t_mag_double_spinbox.valueChanged.connect(self._ecg_sim.set_t_magnitude)
        self.ui.t_wid_double_spinbox.valueChanged.connect(self._ecg_sim.set_t_widthness)
        self.ui.t_time_double_spinbox.valueChanged.connect(self._ecg_sim.set_t_time)

        self.ui.sampling_frequency_spinbox.valueChanged.connect(self._ecg_sim.set_sampling_frequency)
        self.ui.noise_double_spinbox.valueChanged.connect(self._ecg_sim.set_noise)
        self.ui.period_spinbox.valueChanged.connect(self._ecg_sim.set_period)
        self.ui.duration_spinbox.valueChanged.connect(self._ecg_sim.set_duration)

        self.ui.reset_signal_button.clicked.connect(self.reset_values)
        self.ui.create_signal_button.clicked.connect(self.create_signal)

        self._ecg_sim.updated.connect(self.plot_ecg_signal)

    def plot_ecg_signal(self):
        self.ui.graphicsView.plotItem.clear()
        self.ui.graphicsView.plotItem.plot(self._ecg_sim.time, self._ecg_sim.output,
                                           pen='k')

    def reset_values(self):
        self.ui.p_mag_double_spinbox.setValue(0.18)
        self.ui.p_wid_double_spinbox.setValue(0.0178)
        self.ui.p_time_double_spinbox.setValue(0.2398)

        self.ui.q1_mag_double_spinbox.setValue(-0.1103)
        self.ui.q1_wid_double_spinbox.setValue(0.03064)
        self.ui.q1_time_double_spinbox.setValue(0.3218)

        self.ui.q2_mag_double_spinbox.setValue(-0.1075)
        self.ui.q2_wid_double_spinbox.setValue(0.00571)
        self.ui.q2_time_double_spinbox.setValue(0.37123)

        self.ui.r_mag_double_spinbox.setValue(0.05)
        self.ui.r_wid_double_spinbox.setValue(0.02987)
        self.ui.r_time_double_spinbox.setValue(0.46571)

        self.ui.s_mag_double_spinbox.setValue(0.509)
        self.ui.s_wid_double_spinbox.setValue(0.00909)
        self.ui.s_time_double_spinbox.setValue(0.4769)

        self.ui.t_mag_double_spinbox.setValue(0.3255)
        self.ui.t_wid_double_spinbox.setValue(0.02978)
        self.ui.t_time_double_spinbox.setValue(0.754300)

        self.ui.noise_double_spinbox.setValue(0)
        self.ui.sampling_frequency_spinbox.setValue(256)
        self.ui.duration_spinbox.setValue(0.9)
        self.ui.period_spinbox.setValue(0.9)
        self.ui.simulation_line_edit.clear()

    def create_signal(self):
        self._ecg_sim.create_signal()
        signal = Signal(self._ecg_sim.output, self._ecg_sim.time, self.sampling_frequency, self.name, 'ECG')
        self.signal_created.emit(signal)
        self.close()

    @property
    def p_values(self):
        return [
            self.ui.p_mag_double_spinbox.value(),
            self.ui.p_wid_double_spinbox.value(),
            self.ui.p_time_double_spinbox.value()
        ]

    @property
    def q_values(self):
        return [
            self.ui.q1_mag_double_spinbox.value(),
            self.ui.q1_wid_double_spinbox.value(),
            self.ui.q1_time_double_spinbox.value(),
            self.ui.q2_mag_double_spinbox.value(),
            self.ui.q2_wid_double_spinbox.value(),
            self.ui.q2_time_double_spinbox.value()
        ]

    @property
    def r_values(self):
        return [
            self.ui.r_mag_double_spinbox.value(),
            self.ui.r_wid_double_spinbox.value(),
            self.ui.r_time_double_spinbox.value()
        ]

    @property
    def s_values(self):
        return [
            self.ui.s_mag_double_spinbox.value(),
            self.ui.s_wid_double_spinbox.value(),
            self.ui.s_time_double_spinbox.value()
        ]

    @property
    def t_values(self):
        return [
            self.ui.t_mag_double_spinbox.value(),
            self.ui.t_wid_double_spinbox.value(),
            self.ui.t_time_double_spinbox.value()
        ]

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
    def period(self):
        return self.ui.period_spinbox.value()

    @property
    def name(self):
        if self.ui.simulation_line_edit.text() is '':
            return 'ECG Signal'
        else:
            return self.ui.simulation_line_edit.text()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ecg_sim = ECGSimController()

    ecg_sim.show()
    sys.exit(app.exec_())