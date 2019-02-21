from views.oscilloscope import Ui_Form
from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from pyqtgraph.metaarray import *
from itertools import cycle
from PyQt5.QtWidgets import QMainWindow, QApplication


class Oscilloscope(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.init_cursor()

    def init_cursor(self):
        self.x_cursor = pg.InfiniteLine(pos=67, movable=True, angle=90,
                                        pen=pg.mkPen('r', width=3),
                                        hoverPen=pg.mkPen('g', width=3))
        self.multiplot_widget.addItem(self.x_cursor)

    def display_graph(self, x, y):
        data_buffer = np.zeros((1, len(x)))
        for i in range(len(x)):
            data_buffer[0][i] = y[i]
        ma = MetaArray(data_buffer, info=[{"cols": [{"name": "Testing"}]},
                                          {"name": "Time", "units": "sec",
                                           "values": x}])
        self.multiplot_widget.plot(ma)
        last_added_index = len(self.plots) - 1
        plot = self.get_plot(last_added_index)
        plot.getViewBox().setMouseEnabled(y=False)
        plot.scene().sigMouseClicked.connect(self.create_linear_region)
        plot.scene().sigMouseClicked.connect(self.singlemouseclick)

    def create_linear_region(self, evt):
        if evt.double():
            evt.accept()
            for plotitem in self.plots[0]:
                if type(plotitem) is not int:
                    mousePoint = plotitem.vb.mapSceneToView(evt.scenePos())
                    self.showLinearRegion(plotitem, mousePoint.x())

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
        for plotitem in self.plots[0]:
            if type(plotitem) is not int:
                childitems = [child for child in plotitem.vb.allChildren() if
                          isinstance(child, pg.graphicsItems.LinearRegionItem.LinearRegionItem)]
                for child_lr in childitems:
                    plotitem.vb.removeItem(child_lr)

    def singlemouseclick(self, evt):
        if not evt.double():
            evt.accept()
            self.remove_all_linear_regions()

    def get_plot(self, index):
        return self.plots[index][0]


    @property
    def plots(self):
        return self.ui.multiplot_widget.mPlotItem.plots

    @property
    def multiplot_widget(self):
        return self.ui.multiplot_widget
