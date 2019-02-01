import sys
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QGridLayout, QScrollArea, QVBoxLayout, QGroupBox
import pyqtgraph as pg
from signal_properties import SignalProperties

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
		self._sig_params = SignalProperties()
		self._sim_params = sim_params

		grid_layout = QGridLayout()

		parameters_group_box = QGroupBox()

		v_box = QVBoxLayout()
		v_box.addWidget(self._sim_params)
		v_box.addWidget(self._sig_params)

		parameters_group_box.setLayout(v_box)

		scroll = QScrollArea()
		scroll.setWidget(parameters_group_box)

		grid_layout.addWidget(scroll, 0, 0, 2, 1)
		grid_layout.addWidget(self._sim_graph, 0, 1, 2, 1)

		self.setLayout(grid_layout)


	@property
	def sim_params(self):
		return self._sim_params

	@property
	def sig_params(self):
		return self._sig_params

	@property
	def all_spin_boxes(self):
		return self._sim_params.all_spin_boxes
	
	