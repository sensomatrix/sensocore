import sys
from PyQt5.QtWidgets import QDialog, QGroupBox, QDockWidget, QHBoxLayout
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from .ecg_parameters import ECGSimulationParameters

sys.path.append('simulations')
from ecg.ecg import generateECG

class Simulation(QDialog):
	def __init__(self, title='ECG Simulation', parent=None):
		super().__init__(parent=parent)
		self.title = title
		self.time_series = None
		self.output = None
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.sim_graph = SimulationGraph()

		self.ecg_params = ECGSimulationParameters(self)
		self.ecg_params.connectParameters(self.changeInParameter)
		self.ecg_params.connectProperties(self.changeInNoise, self.resetEvent, 
										  self.changeInFrequency, self.changeInDuration,
										  self.changeInPeriod, self.createSignal)

		self.initECGFunction()

		h_box = QHBoxLayout()
		h_box.addWidget(self.ecg_params)
		h_box.addWidget(self.sim_graph)

		self.setLayout(h_box)

		self.exec_()

	def changeInParameter(self, value):
		for param_type_index in range(len(self.ecg_params.all_spin_boxes)):
			param_spin_box_index = self.getSenderIndex(self.sender(), param_type_index)
			
			if param_spin_box_index != -1:
				self.updateParameterValue(value, param_type_index, param_spin_box_index)
				return

	def changeInNoise(self, value):
		self.noise = value
		self.plotECG()

	def resetEvent(self):
		self.ecg_params.setToDefaultValues()

	def changeInFrequency(self, value):
		self.sampling_freq = value
		self.plotECG()

	def changeInDuration(self, value):
		self.duration = value

	def changeInPeriod(self, value):
		if value > self.duration:
			self.duration = value
		self.period = value
		self.plotECG()

	def createSignal(self):
		self.time_series, self.output = generateECG(self.sampling_freq, self.noise, self.duration, self.period,
				self.waves[0], self.waves[1], self.waves[2], self.waves[3], self.waves[4], is_for_graphing=False)
		
	def getSenderIndex(self, sender, param_type_index):
		spin_boxes = self.ecg_params.all_spin_boxes[param_type_index]

		for i in range(len(spin_boxes)):
			if sender == spin_boxes[i]:
				return i

		return -1

	def updateParameterValue(self, value, param_type_index, param_spin_box_index):
		self.waves[param_type_index][param_spin_box_index] = value
		self.plotECG()

	def plotECG(self):
		self.sim_graph.clear()
		time, signal = generateECG(self.sampling_freq, self.noise, self.duration, self.period,
				self.waves[0], self.waves[1], self.waves[2], self.waves[3], self.waves[4])

		self.sim_graph.plot(time, signal, pen='k')

	def initECGFunction(self):
		self.waves = self.ecg_params.getDefaultValues()
		self.sampling_freq = 256
		self.noise = 0
		self.duration = 0.9
		self.period = 0.9
		self.plotECG()

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()
		self.setBackground('w')