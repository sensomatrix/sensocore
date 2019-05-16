from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

#Abstract class to make adding plots easier

class Plotter(QWidget):

    def __init__(self):
        super().__init__()
        self.creategraph()


    def creategraph(self):
        self.pgview = pg.GraphicsView()
        self.graphLayout = pg.GraphicsLayout()
        self.graphLayout.layout.setContentsMargins(0, 0, 0, 0)
        self.pgview.setCentralItem(self.graphLayout)
        layout = QVBoxLayout()
        layout.addWidget(self.pgview)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def plot_data(self, data):
        raise NotImplementedError("method not implemented")


class FilterPlotter(Plotter):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.p = self.graphLayout.addPlot()
        self.p.setLabel('bottom', text="frequency", units="Hz")
        self.p.setLabel('left', text="magnitude", units="")
        self.plotslist = []
        self.p.showGrid(x=True,y=True)

    def plot_data(self, data):
        if len(self.plotslist) == 0:
            self.plotslist.append(self.p.plot(data, pen='r'))
        elif len(self.plotslist) == 1:
            self.plotslist.append(self.p.plot(data, pen='g'))
        elif len(self.plotslist) == 2:
            self.plotslist.clear()
            self.plotslist.append(self.p.plot(data, clear=True, pen='r'))

class FilteredSignalPlotter(Plotter):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.p = self.graphLayout.addPlot()
        self.plotslist = []
    def plot_data(self, data):
        if len(self.plotslist) == 0:
            self.plotslist.append(self.p.plot(data, pen='r'))
            self.p.legend = self.p.addLegend()
            self.p.legend.setParentItem(self.p)
            self.p.legend.addItem(self.plotslist[0], "original")
        elif len(self.plotslist) == 1:
            self.plotslist.append(self.p.plot(data, pen='g'))
            self.p.legend.addItem(self.plotslist[1], "filtered")
        elif len(self.plotslist) == 2:
            self.plotslist.clear()
            self.p.legend = self.p.addLegend()
            self.p.legend.setParentItem(self.p)
            self.plotslist.append(self.p.plot(data, clear=True, pen='r'))
            self.p.legend.addItem(self.plotslist[0], "original")
        self.p.setClipToView(True)
        self.p.vb.setMouseEnabled(y=False)
        self.p.vb.setLimits(maxXRange=5)




