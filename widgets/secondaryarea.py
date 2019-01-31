from pyqtgraph.dockarea import *
from .graphdock import GraphDock
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QSize


class SecondaryArea(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.area = DockArea()
        layout = QVBoxLayout()
        layout.addWidget(self.area)
        self.setLayout(layout)

        # PSD Dock
        self.psd_dock = GraphDock(self, "Power Spectral Density")
        self.area.addDock(self.psd_dock)
        self.resize(self.sizeHint())

        # TF Dock
        self.tf_dock = GraphDock(self, "Time-Frequency view")
        self.area.addDock(self.tf_dock)
        self.resize(self.sizeHint())

    def sizeHint(self):
        return QSize(50, 50)

    def plot_psd_slot(self, signal):
        self.psd_dock.plot(signal, title="PSD - " + signal.name, XAxisLabel="frequency", YAxisLabel="PSD", XAxisUnits="Hz")

    def plot_tf_slot(self, signal):
        self.tf_dock.plot_TF(signal)
