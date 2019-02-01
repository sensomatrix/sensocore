from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class SpectrumView(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.createspecviewgraph()

        # Selection Spectrum
    def createspecviewgraph(self):
        self.pgview = pg.GraphicsView()
        self.graphLayout = pg.GraphicsLayout()
        self.graphLayout.layout.setContentsMargins(0, 0, 0, 0)
        self.pgview.setCentralItem(self.graphLayout)
        layout = QVBoxLayout()
        layout.addWidget(self.pgview)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def plot_selection(self, data):
        self.graphLayout.clear()
        self.graphLayout.nextRow()
        p = pg.PlotItem(name="selectedregionpsd")
        p.setLabel('left', text = "PSD", units="V^2/Hz")
        p.setLabel('bottom', text="frequency", units="Hz")
        p.plot(data)
        self.graphLayout.addItem(p)
