from simulations.ecg.ecg import generate_ecg
from PyQt5.Qt import pyqtSignal
from PyQt5.QtCore import QObject


class ECGSimulationModel(QObject):
    updated = pyqtSignal()

    def __init__(self, p, q, r, s, t, fs, noise, duration, delay, period):
        QObject.__init__(self)
        self._p = p
        self._q = q
        self._r = r
        self._s = s
        self._t = t
        self._fs = fs
        self._noise = noise
        self._duration = duration
        self._period = period
        self._delay = delay
        self.time = None
        self.output = None
        self.generate_signal_for_plotting()

    def update_signal(self):
        self.generate_signal_for_plotting()
        self.updated.emit()

    def generate_signal_for_plotting(self):
        self.time, self.output = generate_ecg(self._fs, self._noise, self._duration, self._period,
                                              self._delay, self._p, self._q, self._r, self._s, self._t)

    def create_signal(self):
        self.time, self.output = generate_ecg(self._fs, self._noise, self._duration, self._period,
                                              self._delay, self._p, self._q, self._r, self._s, self._t, is_for_graphing=False)

    def set_p_magnitude(self, value):
        self._p[0] = value
        self.update_signal()

    def set_p_widthness(self, value):
        self._p[1] = value
        self.update_signal()

    def set_p_time(self, value):
        self._p[2] = value
        self.update_signal()

    def set_q_1_magnitude(self, value):
        self._q[0] = value
        self.update_signal()

    def set_q_1_widthness(self, value):
        self._q[1] = value
        self.update_signal()

    def set_q_1_time(self, value):
        self._q[2] = value
        self.update_signal()

    def set_q_2_magnitude(self, value):
        self._q[3] = value
        self.update_signal()

    def set_q_2_widthness(self, value):
        self._q[4] = value
        self.update_signal()

    def set_q2_time(self, value):
        self._q[5] = value
        self.update_signal()

    def set_r_magnitude(self, value):
        self._r[0] = value
        self.update_signal()

    def set_r_widthness(self, value):
        self._r[1] = value
        self.update_signal()

    def set_r_time(self, value):
        self._r[2] = value
        self.update_signal()

    def set_s_magnitude(self, value):
        self._s[0] = value
        self.update_signal()

    def set_s_widthness(self, value):
        self._s[1] = value
        self.update_signal()

    def set_s_time(self, value):
        self._s[2] = value
        self.update_signal()

    def set_t_magnitude(self, value):
        self._t[0] = value
        self.update_signal()

    def set_t_widthness(self, value):
        self._t[1] = value
        self.update_signal()

    def set_t_time(self, value):
        self._t[2] = value
        self.update_signal()

    def set_noise(self, value):
        self._noise = value
        self.update_signal()

    def set_sampling_frequency(self, value):
        self._fs = value
        self.update_signal()

    def set_period(self, value):
        self._period = value
        self.update_signal()

    def set_duration(self, value):
        self._duration = value

    def set_delay(self, value):
        self._delay = value
        self.update_signal()
