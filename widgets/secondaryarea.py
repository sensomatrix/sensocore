from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

# implement a channel list and maybe some buttons for doing actions on select channels
class SecondaryArea(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.pgview = pg.GraphicsView()
        self.graphLayout = pg.GraphicsLayout()
        self.pgview.setCentralItem(self.graphLayout)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.pgview)

    def plotPSD(self, signal):
        self.graphLayout.nextRow()
        self.plot = self.graphLayout.addPlot(title="PSD of " + signal.name, left="PSD", bottom="freq (Hz)",
                                             x=signal.PSDfbins, y=signal.PSDxx)

    def plotTF(self, signal):
        print("gay")

    def on_channel_selection_change(self, signal):
        self.plotPSD(signal)
