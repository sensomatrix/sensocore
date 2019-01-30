from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

# implement a channel list and maybe some buttons for doing actions on select channels
class PSDDock(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.pgview = pg.GraphicsView()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.pgview)

    def plotPSD(self, signal):
        self.plotitem = pg.PlotItem()
        self.pgview.setCentralWidget(self.plotitem)
        self.plotitem.plot(signal.PSDfbins, signal.PSDxx)

    def on_channel_selection_change(self, signal):
        self.plotPSD(signal)
