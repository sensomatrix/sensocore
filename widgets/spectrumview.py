from pyqtgraph.dockarea import *
from .graphdock import GraphDock
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QSize

class SpectrumView(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.area = DockArea()
        layout = QVBoxLayout()
        layout.addWidget(self.area)
        self.setLayout(layout)
        self.setMaximumHeight(130)

        # Selection Spectrum
        self.selection_spectrum = GraphDock(self, "Selection spectrum")
        self.area.addDock(self.selection_spectrum)
