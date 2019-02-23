import pyqtgraph as pg
from pyqtgraph.metaarray import *
from PyQt5.QtCore import QPointF
from itertools import cycle
import os

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/oscilloscope.ui')
OscilloscopeView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class Oscilloscope(TemplateBaseClass):
    def __init__(self):
        super().__init__()
        self.ui = OscilloscopeView()
        self.ui.setupUi(self)
        self.ui.multiplot_widget.setBackground('w')
        self.x_cursor = None

        self.init_cursor()
        self.init_slider()

        self.colorlist=['r','g','b','c','m','k']
        self.colorpool = cycle(self.colorlist)

    def init_cursor(self):
        self.x_cursor = pg.InfiniteLine(pos=67, movable=True, angle=90,
                                        pen=pg.mkPen('r', width=3),
                                        hoverPen=pg.mkPen('g', width=3))
        self.multiplot_widget.addItem(self.x_cursor)
        self.x_cursor.sigPositionChanged.connect(self.on_cursor_moved)

    def init_slider(self):
        self.ui.horizontal_slider.valueChanged.connect(self.sliderValueChanged)

    def display_graph(self, x, y):
        data_buffer = np.zeros((1, len(x)))
        for i in range(len(x)):
            data_buffer[0][i] = y[i]
        ma = MetaArray(data_buffer, info=[{"cols": [{"name": "Amplitude (mV)"}]},
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
        lr = pg.LinearRegionItem(values=[minValue, maxValue], bounds=[0, plotdataitemlist[0].xData[-1]])
        plotitem.vb.addItem(lr)

    def remove_all_linear_regions(self):
        for plotitem in self.plots:
            if type(plotitem[0]) is not int:
                childitems = [child for child in plotitem[0].vb.allChildren() if
                          isinstance(child, pg.graphicsItems.LinearRegionItem.LinearRegionItem)]
                for child_lr in childitems:
                    plotitem[0].vb.removeItem(child_lr)

    def singlemouseclick(self, evt):
        if not evt.double():
            evt.accept()
            self.remove_all_linear_regions()

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
