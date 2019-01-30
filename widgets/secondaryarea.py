from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
from pyqtgraph.dockarea import *
import numpy as np

# implement a channel list and maybe some buttons for doing actions on select channels
class SecondaryArea(DockArea):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        #d1
        self.d1 = Dock("PSD", size=(500,300), closable=True)
        self.d1pgview = pg.GraphicsView()
        self.d1graphLayout = pg.GraphicsLayout()
        self.d1pgview.setCentralItem(self.d1graphLayout)
        self.d1.addWidget(self.d1pgview)
        self.addDock(self.d1)


        #d2
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.d2 = Dock("Time-frequency", size=(500, 300), closable=True)
        self.d2.glwid = pg.GraphicsLayoutWidget()
        self.d2.addWidget(self.d2.glwid)
        self.addDock(self.d2)

    def on_channel_selection_change(self, signal):
        print("gay")
        self.plot_PSD(signal)
        self.plot_TF(signal)

    def plot_PSD(self, signal):
        self.d1graphLayout.nextRow()
        self.d1graphLayout.addPlot(title="PSD of " + signal.name, left="PSD", bottom="freq (Hz)",
                                             x=signal.PSDfbins, y=signal.PSDxx)

    def plot_TF(self, signal):
        self.d2.glwid.nextRow()
        p1 = self.d2.glwid.addPlot(title= signal.name + " time-frequency plot")
        img = pg.ImageItem()
        p1.addItem(img)
        hist = pg.HistogramLUTItem()
        hist.setImageItem(img)
        #self.d2.glwid.addItem(hist)
        hist.setLevels(np.min(signal.TFSxx), np.max(signal.TFSxx))
        hist.gradient.restoreState(
            {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]})
        # Sxx contains the amplitude for each pixel
        img.setImage(signal.TFSxx)
        # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(signal.Tft[-1] / np.size(signal.TFSxx, axis=1),
                  signal.TFf[-1] / np.size(signal.TFSxx, axis=0))
        # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=signal.TFt[-1], yMin=0, yMax=signal.TFf[-1])
        # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')
        p1.setTitle(signal.name + " time-frequency plot")