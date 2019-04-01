from pyqtgraph.dockarea import *
from widgets.graphdock import GraphDock
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QSize


class SecondaryArea(QWidget):

    def __init__(self):
        super().__init__()
        self.area = DockArea()
        layout = QVBoxLayout()
        layout.addWidget(self.area)
        self.setLayout(layout)

        # PSD Dock
        self.psd_dock = GraphDock(self, "Power Spectral Density")
        self.area.addDock(self.psd_dock)
        self.resize(self.sizeHint())

        # TF Dock
        self.tf_dock = GraphDock(self, "Time-Frequency view", add_legend=False)
        self.area.addDock(self.tf_dock)
        self.resize(self.sizeHint())

    def sizeHint(self):
        return QSize(50, 50)

    def plot_psd_slot(self, signal):
        self.psd_dock.plot(signal)

    def plot_tf_slot(self, signal):
        self.tf_dock.plot_TF(signal)

    def delete_signal(self, signal):
        self.psd_dock.delete_signal(signal.psd)
        self.tf_dock.clear()
        self.psd_dock.remove_legend_item(signal.name)

        signal.psd = None
        signal.time_freq = None
