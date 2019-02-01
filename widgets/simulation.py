import sys
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QScrollArea, QVBoxLayout, QGroupBox, QSplitter
import pyqtgraph as pg
from .signal_properties import SignalProperties

class Simulation(QDialog):
	def __init__(self, title, parent=None):
		self._title = title
		self.parent = parent
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self._title)

		self._sim_graph = pg.PlotWidget()
		self._sim_graph.setBackground('w')

	def addSimAndSigParameters(self, sim_params, props_to_remove=[]):
		self._sig_params = SignalProperties(props_to_remove)
		self._sim_params = sim_params

		splitter = QSplitter()

		parameters_group_box = QGroupBox()

		v_box = QVBoxLayout()
		v_box.addWidget(self._sim_params)
		v_box.addWidget(self._sig_params)

		parameters_group_box.setLayout(v_box)

		scroll = QScrollArea()
		scroll.setWidget(parameters_group_box)

		splitter.addWidget(scroll)
		splitter.addWidget(self._sim_graph)

		h_box = QHBoxLayout(self)

		h_box.addWidget(splitter)

		self.setLayout(h_box)

	def onReset(self):
		self._sig_params.setToDefaultValues()
		self._sim_params.setToDefaultValues()

	@property
	def sim_params(self):
		return self._sim_params

	@property
	def sig_params(self):
		return self._sig_params

	@property
	def all_spin_boxes(self):
		return self._sim_params.all_spin_boxes
	
	@property
	def sim_graph(self):
		return self._sim_graph

	@property
	def title(self):
		return self._title
	
	