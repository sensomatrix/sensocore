import pyqtgraph as pg
from pyqtgraph.metaarray import *
import numpy as np
from PyQt5.QtCore import QPointF, QObject, pyqtSignal
from itertools import cycle
from frequtils import compute_psd


class Scope(QObject):

    cursor_moved_signal = pyqtSignal(str)
    plot_specview = pyqtSignal(np.ndarray)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.plotitems_dictionary = {}
        self.plotitems_isPlotted_dictionary = {}

        # pyqtgraph settings
        self.pw = pg.MultiPlotWidget()
        self.pw.setBackground('w')
        self.pw.setMinimumPlotHeight(100)
        self.addCursor()
        self.colorlist=['r','g','b','c','m','k']
        self.colorpool = cycle(self.colorlist)

        # test the console to see if other classes can call it:
        #self.parent.parent.parent.console.write("Scope loaded! (msg to test writing to console from another class).")


    def addCursor(self):

        # pen = pg.mkPen(width=1)
        self.xcursor = pg.InfiniteLine(movable=True, angle=90)
        self.xcursor.sigPositionChanged.connect(self.xcursor_moved)
        self.pw.addItem(self.xcursor)

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

        # deal with mouse clicks on plot
        self.pw.mPlotItem.plots[last_added_index][0].scene().sigMouseClicked.connect(self.mouseClickedLinearRegion)
        self.pw.mPlotItem.plots[last_added_index][0].scene().sigMouseClicked.connect(self.singlemouseclick)

    def mouseMoved(self, evt):
        pos = evt[0]
        for id, plotitem in self.plotitems_dictionary.items():
            if plotitem.sceneBoundingRect().contains(pos):
                mousePoint = plotitem.vb.mapSceneToView(pos)
                self.parent.chrono.coords.setText("<span style='font-size: 12pt'>t=%s, y=%0.3f</span>" % (self.secondsToHHMMSSMMM(mousePoint.x()), mousePoint.y()))

    def mouseClickedLinearRegion(self, evt):
        # if double click, plot linear region if there isnt one
        if evt.double():
            evt.accept()
            for id, plotitem in self.plotitems_dictionary.items():
                if plotitem.sceneBoundingRect().contains(evt.scenePos()):
                    if not self.doesplotcontainLR(id):
                        mousePoint = plotitem.vb.mapSceneToView(evt.scenePos())
                        self.showLinearRegion(id, mousePoint.x())

    def singlemouseclick(self, evt):
        if not evt.double():
            evt.accept()
            self.remove_all_linear_regions()

    def hideTrace(self, id):
        print("hide trace")

    def xcursor_moved(self, evt):
        if not self.plotitems_dictionary:
            return
        x = evt.value()
        pos = QPointF()
        pos.setX(x)
        pos.setY(0)
        mousePoint = (next(iter(self.plotitems_dictionary.values()))).vb.mapSceneToView(pos)
        self.cursor_moved_signal.emit(self.secondsToHHMMSSMMM(mousePoint.x()))

    def hideTimeAxis(self, lastAddedPlotItem):
        for id, isPlotted in self.plotitems_isPlotted_dictionary.items():
            (self.plotitems_dictionary.get(id)).hideAxis('bottom')
        lastAddedPlotItem.showAxis('bottom')

    def showLinearRegion(self, id, mousepos_x):
        self.remove_all_linear_regions()
        values = self.plotitems_dictionary.get(id).getAxis('bottom').range
        deltat = values[1] - values[0]
        minValue = mousepos_x
        maxValue = mousepos_x + 0.01 * deltat
        plotdataitemlist = [dataitem for dataitem in self.plotitems_dictionary.get(id).vb.allChildren()
                            if isinstance(dataitem, pg.graphicsItems.PlotDataItem.PlotDataItem)]
        lr = pg.LinearRegionItem(values=[minValue, maxValue], bounds=[0, plotdataitemlist[0].xData[-1]])
        self.plotitems_dictionary.get(id).vb.addItem(lr)
        self.plotitems_dictionary.get(id).vb.sigXRangeChanged.connect(self.lr_vb_x_range_changed)
        lrsig = self.parent.parent.parent.datasets.signals_dictionary.get(id)
        lr.sigRegionChangeFinished.connect(lambda sig: self.regionFinishChanged(sig, lrsig))

    def regionFinishChanged(self, regionItem, sig):
        lo, hi = regionItem.getRegion()
        idx_lo = int(sig.fs * lo)
        idx_hi = int(sig.fs * hi)
        fbins, pxx = compute_psd(sig.samples_array[idx_lo:idx_hi], sig.fs)
        data = np.column_stack((fbins, pxx))
        self.plot_specview.emit(data)

    def remove_all_linear_regions(self):
        for plotitem in self.plotitems_dictionary.values():
            childitems = [child for child in plotitem.vb.allChildren() if
                          isinstance(child, pg.graphicsItems.LinearRegionItem.LinearRegionItem)]
            for child_lr in childitems:
                plotitem.vb.removeItem(child_lr)
                plotitem.vb.sigXRangeChanged.disconnect(self.lr_vb_x_range_changed)

    def lr_vb_x_range_changed(self, ev):
        for plotitem in self.plotitems_dictionary.values():
            values = plotitem.getAxis('bottom').range
            lritemlist = [lr for lr in plotitem.vb.allChildren()
                          if isinstance(lr, pg.graphicsItems.LinearRegionItem.LinearRegionItem)]
            for lr in lritemlist:
                deltat = values[1] - values[0]
                minValue = values[0] + 0.45 * deltat
                maxValue = values[0] + 0.55 * deltat
                lr.setRegion([minValue, maxValue])

    def doesplotcontainLR(self, id):
        plotitem = self.plotitems_dictionary.get(id)
        for child in plotitem.vb.allChildren():
            if isinstance(child, pg.graphicsItems.LinearRegionItem.LinearRegionItem):
                print("yes")
                return True
        print("no")
        return False

    def signalChanged_signal(self, id_):
        plotitem = self.plotitems_dictionary.get(id_)
        dataitems = [dataitem for dataitem in plotitem.listDataItems() if isinstance(dataitem, pg.PlotDataItem)]
        for dataitem in dataitems:
            dataitem.setData(self.parent.parent.parent.datasets.signals_dictionary.get(id_).time_array,
                         self.parent.parent.parent.datasets.signals_dictionary.get(id_).samples_array)
        plotitem.vb.autoRange()

    def secondsToHHMMSSMMM(self, t):
        return "%02d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])
