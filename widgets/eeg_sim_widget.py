import pyqtgraph as pg
from PyQt5.QtCore import QThread
from simulations.eeg.jansen import simulate_eeg_jansen
from models.signal import Signal
import os
import time


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/eeg_sim.ui')
EEGSimulationView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class SimulateEEGThread(QThread):
    def __init__(self, fs=None, c1=None, noise=None, callback=None, duration=None, output=None):
        QThread.__init__(self)
        self.output = None
        self.fs = fs
        self.c1 = c1
        self.noise = noise
        self.callback = callback
        self.duration = duration
        self.output = output

    def __del__(self):
        self.wait()

    def run(self):
        self.output = simulate_eeg_jansen(fs=self.fs, C1=self.c1,
                            noise_magnitude=self.noise, callback=self.callback, duration=self.duration)


class EEGSimulationWidget(TemplateBaseClass):
    def __init__(self, signals, sim_count=0):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('ECG Simulation')

        # Create the main window
        self.ui = EEGSimulationView()
        self.ui.setupUi(self)

        self.signals = signals

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False, label='x={value:0.2f}')
        self.hLine = pg.InfiniteLine(angle=0, movable=False, label='y={value:0.2f}')
        self.ui.zoomed_plot.addItem(self.vLine, ignoreBounds=True)
        self.ui.zoomed_plot.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.ui.zoomed_plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)
        self.current_percentage = 0

# Saving default values
###############################################################################################
        self.c1_default = self.c1
        self.fs_default = self.sampling_frequency
        self.duration_default = self.duration
        self.noise_default = self.noise
        self.eeg_output = []
###############################################################################################

# Connections
###############################################################################################
        # C1 values being updated
        self.ui.preview_button.clicked.connect(self.update_plot)
        self.ui.reset_signal_button.clicked.connect(self.reset_to_default)
        self.ui.create_signal_button.clicked.connect(self.generate_signal)
###############################################################################################
        self.eeg_sim_thread = SimulateEEGThread(self.sampling_frequency, self.c1, self.noise, self.current_progress,
                                                duration=self.duration)

        self.eeg_sim_thread.finished.connect(self.update_output)

        self.generate_plot(True)

        self.zoomed_plot = self.ui.zoomed_plot.plot(self.eeg_output, pen="g")
        self.zoomed_plot.getViewBox().setMouseEnabled(y=False)

        self.main_plot = self.ui.main_plot.plot(self.eeg_output)
        self.main_plot.getViewBox().setMouseEnabled(x=False, y=False)

        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)

        self.region.sigRegionChanged.connect(self.update_graph)
        self.ui.zoomed_plot.sigRangeChanged.connect(self.update_region)

        self.update_graph()

        self.ui.main_plot.addItem(self.region, ignoreBounds=True)

        name = 'EEG Simulation'

        if sim_count > 0:
            name += ' ' + str(sim_count)

        self.ui.simulation_line_edit.setText(name)

        self.show()

# Methods
###############################################################################################
    def update_output(self):
        self.eeg_output = self.eeg_sim_thread.output

    def update_graph(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.ui.zoomed_plot.setXRange(minX, maxX, padding=0)

    def update_region(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def generate_signal(self):
        if self.duration != self.duration_default:
            self.generate_plot(False)
        signal = Signal(self.eeg_output, self.sampling_frequency, self.name, 'EEG')
        self.signals.add_signal(signal)
        self.close()

    def generate_plot(self, for_graphing):
        self.current_percentage = 0

        self.simulate_eeg(for_graphing)

        self.simulate_progress_bar()

    def simulate_progress_bar(self):
        with pg.ProgressDialog("Simulating EEG Signal", maximum=100) as dlg:
            dlg.setWindowTitle('EEG Sim')
            while self.eeg_sim_thread.isRunning():
                time.sleep(0.02)
                dlg.setValue(self.current_percentage)

    def simulate_eeg(self, for_graphing):
        duration = self.duration_default if for_graphing else self.duration

        self.eeg_sim_thread.fs = self.sampling_frequency
        self.eeg_sim_thread.c1 = self.c1
        self.eeg_sim_thread.noise = self.noise
        self.eeg_sim_thread.duration = duration

        self.eeg_sim_thread.start()

    def current_progress(self, current_percentage):
        self.current_percentage = current_percentage

    def update_plot(self):
        self.generate_plot(True)
        self.zoomed_plot.setData(self.eeg_output)
        self.main_plot.setData(self.eeg_output)
        self.ui.zoomed_plot.autoRange()

    def reset_to_default(self):
        self.ui.c1_spinbox.setValue(self.c1_default)
        self.ui.sampling_frequency_spinbox.setValue(self.fs_default)
        self.ui.noise_double_spinbox.setValue(self.noise_default)
        self.ui.duration_spinbox.setValue(self.duration_default)
        self.update_plot()

    def mouse_moved(self, evt):
        pos = evt[0]
        if self.ui.zoomed_plot.sceneBoundingRect().contains(pos):
            mousePoint = self.ui.zoomed_plot.plotItem.vb.mapSceneToView(pos)
            self.vLine.setPos(mousePoint.x())

            time = self.eeg_output.transpose()[0]

            index = min(range(len(time)), key=lambda i: abs(time[i] - mousePoint.x()))
            self.hLine.setPos(self.eeg_output[index][1])
###############################################################################################

    # Properties
###############################################################################################
    @property
    def c1(self):
        return self.ui.c1_spinbox.value()

    @property
    def noise(self):
        return self.ui.noise_double_spinbox.value()

    @property
    def sampling_frequency(self):
        return self.ui.sampling_frequency_spinbox.value()

    @property
    def duration(self):
        return self.ui.duration_spinbox.value()

    @property
    def name(self):
        return self.ui.simulation_line_edit.text()
