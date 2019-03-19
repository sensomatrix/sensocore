import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal
from simulations.ecg.ecg import generate_ecg
from models.signal import Signal
import os
import numpy as np


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/ecg_sim.ui')
ECGSimulationView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class ECGSimulationWidget(TemplateBaseClass):
    def __init__(self, signals):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('ECG Simulation')

        # Create the main window
        self.ui = ECGSimulationView()
        self.ui.setupUi(self)

        self.signals = signals

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False, label='x={value:0.2f}')
        self.hLine = pg.InfiniteLine(angle=0, movable=False, label='y={value:0.2f}')
        self.ui.plot.addItem(self.vLine, ignoreBounds=True)
        self.ui.plot.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.ui.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

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
        self.ecg_output = []
        self.init = True
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
        self.ui.duration_spinbox.valueChanged.connect(self.update_plot)
        self.ui.delay_spin_box.valueChanged.connect(self.update_plot)

        self.ui.reset_signal_button.clicked.connect(self.reset_to_default)
        self.ui.create_signal_button.clicked.connect(self.generate_signal)

        self.ui.scale_slider.sliderReleased.connect(self.scale_values)
###############################################################################################
        self.generate_plot()

        self.zoomed_plot = self.ui.plot.plot(self.ecg_output, pen="g")
        self.zoomed_plot.getViewBox().setMouseEnabled(y=False)

        self.main_plot = self.ui.main_plot.plot(self.ecg_output)
        self.main_plot.getViewBox().setMouseEnabled(x=False, y=False)

        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)

        self.region.sigRegionChanged.connect(self.update_graph)
        self.ui.plot.sigRangeChanged.connect(self.update_region)

        self.update_graph()

        self.ui.main_plot.addItem(self.region, ignoreBounds=True)

        # self.plot = self.ui.plot.plot(self.ecg_output)
        # self.plot.getViewBox().setMouseEnabled(y=False)

        self.init = False

        self.show()

# Methods
###############################################################################################
    def generate_plot(self, is_for_graphing=True):
        new_ecg_output = generate_ecg(self.sampling_frequency, self.noise, self.duration, self.period,
                                       self.delay, self.p, self.q, self.r, self.s, self.t, is_for_graphing=False)

        if not self.init:
            rgn = self.region.getRegion()
            time = self.ecg_output.transpose()[0]
            min_index = min(range(len(time)), key=lambda i: abs(time[i] - rgn[0]))
            max_index = min(range(len(time)), key=lambda i: abs(time[i] - rgn[1]))
            output = self.ecg_output.transpose()[1]
            new_output = new_ecg_output.transpose()[1]
            output[min_index:max_index] = new_output[min_index:max_index]

            output = output.transpose()
            self.ecg_output = self.ecg_output.transpose()
            self.ecg_output[1] = output
            self.ecg_output = self.ecg_output.transpose()
        else:
            self.ecg_output = np.zeros((new_ecg_output.shape[0], new_ecg_output.shape[1]))
            self.ecg_output = new_ecg_output
            return

        if new_ecg_output.shape[0] != self.ecg_output.shape[0]:
            self.ecg_output = np.zeros((new_ecg_output.shape[0], new_ecg_output.shape[1]))
            self.ecg_output = new_ecg_output

    def scale_values(self):
        scaled_value = self.ui.scale_slider.value() / 100.0
        self.ui.scale_value.setText('Scale: {0}'.format(str(scaled_value)))

        time = self.ecg_output.transpose()[0]

        minX, maxX = self.region.getRegion()
        min_idx = (np.abs(time - minX)).argmin()
        max_idx = (np.abs(time - maxX)).argmin()

        indices = range(min_idx, max_idx)

        self.ecg_output = self.ecg_output.transpose()
        for index in indices:
            self.ecg_output[1][index] *= scaled_value
        self.ecg_output = self.ecg_output.transpose()

        self.zoomed_plot.setData(self.ecg_output)
        self.main_plot.setData(self.ecg_output)

    def update_plot(self):
        self.generate_plot()
        self.zoomed_plot.setData(self.ecg_output)
        self.main_plot.setData(self.ecg_output)

    def update_graph(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.ui.plot.setXRange(minX, maxX, padding=0)

    def update_region(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def generate_signal(self):
        # self.generate_plot(is_for_graphing=False)
        signal = Signal(self.ecg_output, self.sampling_frequency, self.name, 'ECG')
        self.signals.add_signal(signal)
        self.close()

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

    def mouse_moved(self, evt):
        pos = evt[0]
        if self.ui.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.ui.plot.plotItem.vb.mapSceneToView(pos)
            self.vLine.setPos(mousePoint.x())

            time = self.ecg_output.transpose()[0]
            index = min(range(len(time)), key=lambda i: abs(time[i] - mousePoint.x()))
            self.hLine.setPos(self.ecg_output[index][1])
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

    @property
    def name(self):
        return self.ui.simulation_line_edit.placeholderText()