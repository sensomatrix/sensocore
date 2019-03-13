import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.metaarray import *
from PyQt5.QtCore import QPointF, pyqtSignal
from itertools import cycle
import os
import numpy as np
from scipy import random


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/oscilloscope.ui')
OscilloscopeView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class Oscilloscope(TemplateBaseClass):
    region_updated = pyqtSignal(np.ndarray, int)
    region_cleared = pyqtSignal()
    create_signal = pyqtSignal(np.ndarray, int)

    def __init__(self):
        super().__init__()
        self.ui = OscilloscopeView()
        self.ui.setupUi(self)
        self.x_cursor = None

        self.init_cursor()
        self.init_slider()

        self.colorlist = ['r', 'g', 'b', 'c', 'm', 'w']
        self.colorpool = cycle(self.colorlist)

        self.multiplot_widget.setMinimumPlotHeight(250)

        self.lr = None
        self.save_lr = None

    def init_cursor(self):
        self.x_cursor = pg.InfiniteLine(pos=67, movable=True, angle=90,
                                        pen=pg.mkPen('r', width=3),
                                        hoverPen=pg.mkPen('g', width=3))
        self.multiplot_widget.addItem(self.x_cursor)
        self.x_cursor.sigPositionChanged.connect(self.on_cursor_moved)

    def init_slider(self):
        self.ui.horizontal_slider.valueChanged.connect(self.sliderValueChanged)

    def display_graph(self, x, y, name):
        self.multiplot_widget.resizeEvent(None)

        data_buffer = np.zeros((1, len(x)))
        for i in range(len(x)):
            data_buffer[0][i] = y[i]

        ma = MetaArray(data_buffer, info=[{"cols": [{"name": name, 'units': 'V'}]},
                                          {"name": "Time", "units": "sec",
                                           "values": x}])

        random_color = next(self.colorpool)

        self.multiplot_widget.plot(ma)
        last_added_index = len(self.plots) - 1
        plot = self.get_plot(last_added_index)
        plot.getViewBox().setMouseEnabled(y=False)
        plot.listDataItems()[0].setPen(pg.mkPen(random_color))
        plot.scene().sigMouseClicked.connect(self.create_linear_region)
        plot.scene().sigMouseClicked.connect(self.singlemouseclick)
        self.proxy = pg.SignalProxy(self.get_plot(last_added_index).scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def update_plot(self, x, y, index):
        plot = self.get_plot(index)
        plot.clear()

        plot.plot(x, y)

    def create_linear_region(self, evt):
        if evt.double():
            evt.accept()
            for plotitem in self.plots:
                if type(plotitem[0]) is not int and plotitem[0].sceneBoundingRect().contains(evt.scenePos()):
                    mousePoint = plotitem[0].vb.mapSceneToView(evt.scenePos())
                    self.showLinearRegion(plotitem[0], mousePoint.x())

    def showLinearRegion(self, plotitem, mousepos_x):
        self.remove_all_linear_regions()
        values = plotitem.getAxis('bottom').range
        deltat = values[1] - values[0]
        minValue = mousepos_x
        maxValue = mousepos_x + 0.01 * deltat
        plotdataitemlist = [dataitem for dataitem in plotitem.vb.allChildren()
                            if isinstance(dataitem, pg.graphicsItems.PlotDataItem.PlotDataItem)]
        self.lr = pg.LinearRegionItem(values=[minValue, maxValue], bounds=[0, plotdataitemlist[0].xData[-1]])

        self.lr.sigRegionChanged.connect(self.update_graph)

        plotitem.vb.addItem(self.lr)

    def update_graph(self):
        for index, plotitem in enumerate(self.plots):
            if self.lr in plotitem[0].vb.addedItems:
                minX, maxX = self.lr.getRegion()
                time = plotitem[0].dataItems[0].xData
                output = plotitem[0].dataItems[0].yData
                min_index = min(range(len(time)), key=lambda i: abs(time[i] - minX))
                max_index = min(range(len(time)), key=lambda i: abs(time[i] - maxX))
                self.region_updated.emit(output[min_index:max_index], index)

    def remove_all_linear_regions(self):
        for plotitem in self.plots:
            if self.lr in plotitem[0].vb.addedItems:
                plotitem[0].vb.removeItem(self.lr)
                self.lr = None

                if self.save_lr is not None:
                    plotitem[0].vb.menu.removeAction(self.save_lr)
                    self.save_lr = None

                self.region_cleared.emit()

    def singlemouseclick(self, evt):
        if evt.button() == QtCore.Qt.RightButton and self.lr is not None:
            for plotitem in self.plots:
                if type(plotitem[0]) is not int and plotitem[0].sceneBoundingRect().contains(evt.scenePos()):
                    view = plotitem[0].vb
                    if self.save_lr is None:
                        self.save_lr = view.menu.addAction('Save selected window')
                        self.save_lr.triggered.connect(self.create_lr)

        elif not evt.double():
            evt.accept()
            self.remove_all_linear_regions()

    def create_lr(self):
        for index, plotitem in enumerate(self.plots):
            if self.lr in plotitem[0].vb.addedItems:
                minX, maxX = self.lr.getRegion()
                time = plotitem[0].dataItems[0].xData
                output = plotitem[0].dataItems[0].yData
                min_index = min(range(len(time)), key=lambda i: abs(time[i] - minX))
                max_index = min(range(len(time)), key=lambda i: abs(time[i] - maxX))

                time = time[min_index:max_index]
                time = time.reshape((time.shape[0], 1))
                output = output[min_index:max_index]
                output = output.reshape((output.shape[0], 1))

                signal = np.hstack([time, output])
                self.create_signal.emit(signal, index)

    def get_plot(self, index):
        return self.plots[index][0]

    # dynamic time steps need to be added
    def sliderValueChanged(self):
        max_t = self.get_largest_time()
        min_t = self.get_smallest_time()

        window_size = (max_t - min_t) / 100

        lo_t = (self.ui.horizontal_slider.value() / 100) * max_t + min_t

        if lo_t >= max_t:
            lo_t = max_t - window_size
            self.ui.horizontal_slider.setValue(100)

        hi_t = lo_t + window_size
        for plot in self.plots:
            if plot is not int:
                plot[0].setRange(xRange=[lo_t, hi_t])

    def get_largest_time(self):
        max_t = 0
        for plot in self.plots:
            if plot[0].items is not int:
                max_local_t = plot[0].items[0].xData.max()
                if max_local_t > max_t:
                    max_t = max_local_t

        return max_t

    def get_smallest_time(self):
        min_t = 10
        for plot in self.plots:
            if plot[0].items is not int:
                min_local_t = plot[0].items[0].xData.min()
                if min_local_t < min_t:
                    min_t = min_local_t

        return min_t

    def on_cursor_moved(self):
        x = self.x_cursor.value()
        pos = QPointF(x, 0)
        mousePoint = self.plots[0][0].vb.mapSceneToView(pos)
        string_cursor = "Time: " + str(round(mousePoint.x(),4))
        self.ui.cursor_label.setText(string_cursor)

    def mouseMoved(self, evt):
        pos = evt[0]
        for plot_item in self.plots:
            if plot_item[0].sceneBoundingRect().contains(pos):
                mousePoint = plot_item[0].vb.mapSceneToView(pos)
                self.ui.label_x.setText("X: " + str(round(mousePoint.x(), 4)))
                self.ui.label_y.setText("Y: " + str(round(mousePoint.y(), 4)))

    @property
    def plots(self):
        return self.ui.multiplot_widget.mPlotItem.plots

    @property
    def multiplot_widget(self):
        return self.ui.multiplot_widget