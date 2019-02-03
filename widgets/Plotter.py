from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

#Abstract class to make adding plots easier

class Plotter(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
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

    def plot_data(self):
        raise NotImplementedError("method not implemented")


class FilterPlotter(Plotter):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def plot_data(self, data,):
        self.graphLayout.clear()
        self.graphLayout.nextRow()
        p = pg.PlotItem(title="Frequency response")
        p.setLabel('bottom', text="frequency", units="Hz")
        p.setLabel('left', text="magnitude", units="dB")
        p.setClipToView(True)
        p.setLogMode(y=True)
        p.plot(data)
        self.graphLayout.addItem(p)

class FilteredSignalPlotter(Plotter):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    def plot_data(self, data, title):
        if self.graphLayout.currentRow == 2:
            self.graphLayout.removeItem(self.plot1)
            self.graphLayout.removeItem(self.plot2)
            self.graphLayout.currentRow = 0
        p = pg.PlotItem(title=title)
        p.vb.setMouseEnabled(y=False)
        p.vb.setLimits(maxXRange=10)
        p.setLabel('bottom', text="time", units="sec")
        p.setLabel('left', text="amplitude")
        p.setClipToView(True)
        p.setLogMode(y=False)
        p.plot(data)
        self.graphLayout.addItem(p)
        self.graphLayout.nextRow()
        if self.graphLayout.currentRow == 1:
            self.plot1 = p
        if self.graphLayout.currentRow == 2:
            self.plot2 = p
            p.setXLink(self.plot1.vb)
        print("Current row:" + str(self.graphLayout.currentRow))
