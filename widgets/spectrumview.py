from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class SpectrumView(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.createpyqtgraph()

        # Selection Spectrum
    def createpyqtgraph(self):
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
        p = pg.PlotItem(name="test")
        p.plot(data)
        self.graphLayout.addItem(p)
