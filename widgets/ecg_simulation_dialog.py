from PyQt5.QtWidgets import QDialog, QGroupBox, QDockWidget, QHBoxLayout, QScrollArea, QApplication
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from .ecg_parameters import ECGSimulationParameters
from widgets.signal_properties import SignalProperties
from .simulation import Simulation

import sys

sys.path.append('simulations')
from ecg.ecg import generateECG

class ECGSimulation(Simulation):
	def __init__(self, title, parent):
		super().__init__(title, parent=parent)
		self.addSimAndSigParameters(ECGSimulationParameters())
		self.setupConnections()
		self.plotECGSignal()
		self.showMaximized()
		self.exec_()

	def setupConnections(self):
		for spin_box_type in self.all_spin_boxes:
			for spin_box in spin_box_type:
				spin_box.valueChanged.connect(self.onValueChanged)

		self.sig_params.noise_spin_box.valueChanged.connect(self.onValueChanged)
		self.sig_params.sampling_freq_spin_box.valueChanged.connect(self.onValueChanged)
		self.sig_params.period_spin_box.valueChanged.connect(self.onValueChanged)
		self.sig_params.reset_button.clicked.connect(self.onReset)
		self.sig_params.create_button.clicked.connect(self.onCreate)

	def onValueChanged(self):
		self.plotECGSignal()

	def onCreate(self):
		self.time_series, self.output = generateECG(self.sig_params.sampling_frequency, self.sig_params.noise_magnitude, self.sig_params.end_time, self.sig_params.period,
			self.sim_params.P, self.sim_params.Q, self.sim_params.R, self.sim_params.S, self.sim_params.T, is_for_graphing=False)

		self.parent.datasets.loadFromSimulation(self.output, self.time_series, self.sig_params.sampling_frequency, self.sig_params.name_text_field.text(), type=self.title)
		self.close()

	def plotECGSignal(self):
		self.sim_graph.clear()
		time, output = generateECG(self.sig_params.sampling_frequency, self.sig_params.noise_magnitude, self.sig_params.end_time, self.sig_params.period,
			self.sim_params.P, self.sim_params.Q, self.sim_params.R, self.sim_params.S, self.sim_params.T)
		self.sim_graph.plot(time, output, pen='k')