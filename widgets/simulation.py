import sys
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout
import pyqtgraph as pg

class Simulation(QDialog):
	def __init__(self, title):
		self._title = title
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self._title)

		self._sim_graph = pg.PlotWidget()
		self._sim_graph.setBackground('w')

	def addSimParameters(self, sim_params):
		_h_box = QHBoxLayout()
		_h_box.addWidget(sim_params)
		_h_box.addWidget(self._sim_graph)

		self.setLayout(_h_box)