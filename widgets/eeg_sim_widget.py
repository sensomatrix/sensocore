import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from simulations.eeg.jansen import simulate_eeg_jansen
import os


pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/eeg_sim.ui')
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
        self.proxy = pg.SignalProxy(self.ui.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

# Saving default values
###############################################################################################
        self.c1_default = self.c1
        self.fs_default = self.sampling_frequency
        self.duration_default = self.duration
        self.noise_default = self.noise
        self.time = []
        self.eeg_output = []
###############################################################################################

# Connections
###############################################################################################
        # C1 values being updated
        self.ui.preview_button.clicked.connect(self.update_plot)
        self.ui.reset_signal_button.clicked.connect(self.reset_to_default)
###############################################################################################
        self.generate_plot()

        self.plot = self.ui.plot.plot(self.time, self.eeg_output)
        self.plot.getViewBox().setMouseEnabled(y=False)

        self.show()

# Methods
###############################################################################################
    def generate_plot(self):
        self.time, self.eeg_output = simulate_eeg_jansen(fs=self.sampling_frequency, C1=self.c1,
                                                         noise_magnitude=self.noise)

    def update_plot(self):
        self.generate_plot()
        self.plot.setData(self.time, self.eeg_output)

    def reset_to_default(self):
        self.ui.c1_spinbox.setValue(self.c1_default)

        self.ui.sampling_frequency_spinbox.setValue(self.fs_default)
        self.ui.noise_double_spinbox.setValue(self.noise_default)
        self.ui.duration_spinbox.setValue(self.duration_default)

    def mouse_moved(self, evt):
        pos = evt[0]
        if self.ui.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.ui.plot.plotItem.vb.mapSceneToView(pos)
            self.vLine.setPos(mousePoint.x())

            index = min(range(len(self.time)), key=lambda i: abs(self.time[i] - mousePoint.x()))
            self.hLine.setPos(self.eeg_output[index])
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
###############################################################################################

win = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
