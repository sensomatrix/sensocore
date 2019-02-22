import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from simulations.ecg.ecg import generate_ecg
import os


pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/ecg_sim.ui')
ECGSimulation, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('ECG Simulation')

        # Create the main window
        self.ui = ECGSimulation()
        self.ui.setupUi(self)

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False, label='x={value:0.2f}')
        self.hLine = pg.InfiniteLine(angle=0, movable=False, label='y={value:0.2f}')
        self.ui.plot.addItem(self.vLine, ignoreBounds=True)
        self.ui.plot.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.ui.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

# Saving default values
###############################################################################################
        self.p_default = self.p
        self.q_default = self.q
        self.r_default = self.r
        self.s_default = self.s
        self.t_default = self.t
        self.fs_default = self.sampling_frequency
        self.delay_default = self.delay
        self.noise_default = self.noise
        self.period_default = self.period
###############################################################################################

# Connections
###############################################################################################
        # P values being updated
        self.ui.p_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.p_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.p_time_double_spinbox.valueChanged.connect(self.update_plot)

        # Q1 values being updated
        self.ui.q1_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.q1_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.q1_time_double_spinbox.valueChanged.connect(self.update_plot)

        # Q2 values being updated
        self.ui.q2_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.q2_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.q2_time_double_spinbox.valueChanged.connect(self.update_plot)

        # R values being updated
        self.ui.r_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.r_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.r_time_double_spinbox.valueChanged.connect(self.update_plot)

        # S values being updated
        self.ui.s_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.s_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.s_time_double_spinbox.valueChanged.connect(self.update_plot)

        # T values being updated
        self.ui.t_mag_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.t_wid_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.t_time_double_spinbox.valueChanged.connect(self.update_plot)

        self.ui.noise_double_spinbox.valueChanged.connect(self.update_plot)
        self.ui.period_spinbox.valueChanged.connect(self.update_plot)
        self.ui.sampling_frequency_spinbox.valueChanged.connect(self.update_plot)
        self.ui.delay_spin_box.valueChanged.connect(self.update_plot)

        self.ui.reset_signal_button.clicked.connect(self.reset_to_default)
###############################################################################################

        self.time, self.ecg_output = generate_ecg(self.sampling_frequency, self.noise, self.duration, self.period, self.delay,
                           self.p, self.q, self.r, self.s, self.t)

        self.plot = self.ui.plot.plot(self.time, self.ecg_output)

        self.show()

# Methods
###############################################################################################
    def update_plot(self):
        self.time, self.ecg_output = generate_ecg(self.sampling_frequency, self.noise, self.duration, self.period, self.delay,
                           self.p, self.q, self.r, self.s, self.t)

        self.plot.setData(self.time, self.ecg_output)

    def reset_to_default(self):
        self.ui.p_mag_double_spinbox.setValue(self.p_default[0])
        self.ui.p_time_double_spinbox.setValue(self.p_default[1])
        self.ui.p_wid_double_spinbox.setValue(self.p_default[2])

        self.ui.q1_mag_double_spinbox.setValue(self.q_default[0])
        self.ui.q1_time_double_spinbox.setValue(self.q_default[1])
        self.ui.q1_wid_double_spinbox.setValue(self.q_default[2])

        self.ui.q2_mag_double_spinbox.setValue(self.q_default[0])
        self.ui.q2_time_double_spinbox.setValue(self.q_default[1])
        self.ui.q2_wid_double_spinbox.setValue(self.q_default[2])

        self.ui.r_mag_double_spinbox.setValue(self.r_default[0])
        self.ui.r_time_double_spinbox.setValue(self.r_default[1])
        self.ui.r_wid_double_spinbox.setValue(self.r_default[2])

        self.ui.s_mag_double_spinbox.setValue(self.s_default[0])
        self.ui.s_time_double_spinbox.setValue(self.s_default[1])
        self.ui.s_wid_double_spinbox.setValue(self.s_default[2])

        self.ui.t_mag_double_spinbox.setValue(self.t_default[0])
        self.ui.t_time_double_spinbox.setValue(self.t_default[1])
        self.ui.t_wid_double_spinbox.setValue(self.t_default[2])

        self.ui.sampling_frequency_spinbox.setValue(self.fs_default)
        self.ui.delay_spin_box.setValue(self.delay_default)
        self.ui.period_spinbox.setValue(self.period_default)
        self.ui.noise_double_spinbox.setValue(self.noise_default)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.ui.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.ui.plot.plotItem.vb.mapSceneToView(pos)
            self.vLine.setPos(mousePoint.x())

            index = min(range(len(self.time)), key=lambda i: abs(self.time[i] - mousePoint.x()))
            self.hLine.setPos(self.ecg_output[index])
###############################################################################################

    # Properties
###############################################################################################
    @property
    def p(self):
        return [self.ui.p_mag_double_spinbox.value(), self.ui.p_time_double_spinbox.value(), self.ui.p_wid_double_spinbox.value()]

    @property
    def q(self):
        return [self.ui.q1_mag_double_spinbox.value(), self.ui.q1_time_double_spinbox.value(), self.ui.q1_wid_double_spinbox.value(),
                self.ui.q2_mag_double_spinbox.value(), self.ui.q2_time_double_spinbox.value(), self.ui.q2_wid_double_spinbox.value()]

    @property
    def r(self):
        return [self.ui.r_mag_double_spinbox.value(), self.ui.r_time_double_spinbox.value(), self.ui.r_wid_double_spinbox.value()]

    @property
    def s(self):
        return [self.ui.s_mag_double_spinbox.value(), self.ui.s_time_double_spinbox.value(), self.ui.s_wid_double_spinbox.value()]

    @property
    def t(self):
        return [self.ui.t_mag_double_spinbox.value(), self.ui.t_time_double_spinbox.value(), self.ui.t_wid_double_spinbox.value()]

    @property
    def noise(self):
        return self.ui.noise_double_spinbox.value()

    @property
    def period(self):
        return self.ui.period_spinbox.value()

    @property
    def sampling_frequency(self):
        return self.ui.sampling_frequency_spinbox.value()

    @property
    def delay(self):
        return self.ui.delay_spin_box.value()

    @property
    def duration(self):
        return self.ui.duration_spinbox.value()
###############################################################################################

win = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
