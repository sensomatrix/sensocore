import pyqtgraph as pg
import numpy as np
from pyqtgraph.dockarea import *
from utils.frequtils import compute_psd, compute_time_freq

LINECOLORS = ['r', 'g', 'b', 'c', 'm', 'y', 'w']

class GraphDock(Dock):

    def __init__(self, parent, name):
        super().__init__(name, size=(1, 1), closable=True)
        self.parent = parent
        self.pgview = pg.GraphicsView()
        self.graphLayout = pg.GraphicsLayout()
        self.pgview.setCentralItem(self.graphLayout)
        self.p = pg.PlotItem()
        self.p.addLegend()
        self.graphLayout.addItem(self.p)
        self.addWidget(self.pgview)
        self.current_index = 0

    def plot(self, signal, title="", XAxisLabel="", YAxisLabel="", XAxisUnits="", YAxisUnits=""):
        XAxis = pg.AxisItem(orientation='bottom')
        XAxis.setLabel(text=XAxisLabel, units=XAxisUnits)
        YAxis = pg.AxisItem(orientation='left')
        YAxis.setLabel(text=YAxisLabel, units=YAxisUnits)
        axisdict = {
            'bottom': XAxis,
            'left': YAxis
        }
        PSDfbins, PSDxx = compute_psd(signal.current_mode, signal.fs)
        signal.psd = (PSDfbins, PSDxx)
        self.p.plot(PSDfbins, PSDxx, pen=pg.mkPen(LINECOLORS[self.current_index]), name=signal.name)
        self.current_index = (self.current_index + 1) % len(LINECOLORS)
        self.p.vb.autoRange()
        self.p.replot()

    # Following code is from: https://stackoverflow.com/questions/51312923/plotting-the-spectrum
    def plot_TF(self, signal):
        self.graphLayout.nextRow()
        p1 = self.graphLayout.addPlot(title="Time-Frequency - " + signal.name)
        img = pg.ImageItem()
        p1.addItem(img)
        hist = pg.HistogramLUTItem()
        hist.setImageItem(img)
        TFf, TFt, TFSxx = compute_time_freq(signal.current_mode, signal.fs)
        signal.time_freq = (TFf, TFt, TFSxx)
        hist.setLevels(np.min(TFSxx), np.max(TFSxx))
        hist.gradient.restoreState(
            {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]})
        img.setImage(TFSxx)
        img.scale(TFt[-1] / np.size(TFSxx, axis=1),
                  TFf[-1] / np.size(TFSxx, axis=0))
        # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=TFt[-1], yMin=0, yMax=TFf[-1])
        p1.setLabel('bottom', "Time", units='s')
        p1.setLabel('left', "Frequency", units='Hz')
