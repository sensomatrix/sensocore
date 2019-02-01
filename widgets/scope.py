import pyqtgraph as pg
from pyqtgraph.metaarray import *
import numpy as np
from PyQt5.QtCore import QPointF, QObject, pyqtSignal
from itertools import cycle


class Scope(QObject):

    cursor_moved_signal = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.plotitems_dictionary = {}
        self.plotitems_isPlotted_dictionary = {}

        # pyqtgraph settings
        self.pw = pg.MultiPlotWidget()
        self.pw.setBackground('w')
        self.pw.setMinimumPlotHeight(100)
        self.xcursor = None
        self.colorlist=['r','g','b','c','m','k']
        self.colorpool = cycle(self.colorlist)

        # test the console to see if other classes can call it:
        self.parent.parent.console.write("Scope loaded! (msg to test writing to console from another class).")

    # do not call the add_trace method directly from outside, go through the signal-slot qt mechanism (see initui.py)
    def on_signal_loaded(self, signal):
        self.add_trace(signal)
        self.pw.resizeEvent(None)

    def add_trace(self, signal):
        data_buffer = np.zeros((1, signal.samples_array.size))
        for i in range(signal.samples_array.size):
            data_buffer[0][i] = signal.samples_array[i]
        ma = MetaArray(data_buffer, info=[{"cols": [{"name": signal.name}]},
                                          {"name": "Time", "units": "sec",
                                           "values": signal.time_array}])
        self.pw.plot(ma)
        last_added_index = len(self.pw.mPlotItem.plots) - 1

        # view settings
        random_color = next(self.colorpool)
        self.pw.mPlotItem.plots[last_added_index][0].listDataItems()[0].setPen(pg.mkPen(random_color))
        self.pw.mPlotItem.plots[last_added_index][0].disableAutoRange()
        self.pw.mPlotItem.plots[last_added_index][0].setLimits(maxXRange=10,xMin=0)
        self.pw.mPlotItem.plots[last_added_index][0].setDownsampling(auto=True)
        self.pw.mPlotItem.plots[last_added_index][0].setClipToView(True)

        # trying to display coords
        self.proxy = pg.SignalProxy(self.pw.mPlotItem.plots[last_added_index][0].scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        # add infinite line
        if last_added_index is 0:
            #pen = pg.mkPen(width=1)
            self.xcursor = pg.InfiniteLine(movable=True, angle=90)
            self.xcursor.sigPositionChanged.connect(self.xcursor_moved)
            self.pw.addItem(self.xcursor)

        # link X-axis
        if last_added_index is not 0:
            self.pw.mPlotItem.plots[last_added_index][0].setXLink(self.pw.mPlotItem.plots[0][0].vb)

        # disable y-axis movement
        self.pw.mPlotItem.plots[last_added_index][0].getViewBox().setMouseEnabled(y=False)

        # update traces dictionary
        self.plotitems_dictionary[signal.id] = self.pw.mPlotItem.plots[last_added_index][0]
        
        # update isPlottedDictionary
        self.plotitems_isPlotted_dictionary[signal.id] = True

        # hideTimeAxis for all except last
        self.hideTimeAxis(self.pw.mPlotItem.plots[last_added_index][0])

    def mouseMoved(self, evt):
        pos = evt[0]
        for id, plotitem in self.plotitems_dictionary.items():
            if plotitem.sceneBoundingRect().contains(pos):
                mousePoint = plotitem.vb.mapSceneToView(pos)
                print(mousePoint.x(), mousePoint.y())
                
    def hideTrace(self, id):
        print("hide trace")

    def xcursor_moved(self, evt):
        x = evt.value()
        pos = QPointF()
        pos.setX(x)
        pos.setY(0)
        mousePoint = (next(iter(self.plotitems_dictionary.values()))).vb.mapSceneToView(pos)
        self.cursor_moved_signal.emit(mousePoint.x())
        print("gay")

    def hideTimeAxis(self, lastAddedPlotItem):
        for id, isPlotted in self.plotitems_isPlotted_dictionary.items():
            (self.plotitems_dictionary.get(id)).hideAxis('bottom')
        lastAddedPlotItem.showAxis('bottom')


