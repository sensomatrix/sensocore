from PyQt5.QtWidgets import QDialog, QGroupBox, QDockWidget, QHBoxLayout, QScrollArea, QApplication
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from ecg_parameters import ECGSimulationParameters
from signal_properties import SignalProperties
from simulation import Simulation

import sys

sys.path.append('simulations')
from ecg.ecg import generateECG

class ECGSimulation(Simulation):
	def __init__(self, title):
		super().__init__(title)
		self.addSimParameters(ECGSimulationParameters())
		self.setupConnections()

	def setupConnections(self):
		self.all_spin_boxes[0][0].valueChanged.connect(self.onPMagnitudeChanged)
		self.all_spin_boxes[0][1].valueChanged.connect(self.onPWidthnessChanged)
		self.all_spin_boxes[0][2].valueChanged.connect(self.onPDelayChanged)

		self.all_spin_boxes[1][0].valueChanged.connect(self.onQ1MagnitudeChanged)
		self.all_spin_boxes[1][1].valueChanged.connect(self.onQ1WidthnessChanged)
		self.all_spin_boxes[1][2].valueChanged.connect(self.onQ1DelayChanged)

		self.all_spin_boxes[1][3].valueChanged.connect(self.onQ2MagnitudeChanged)
		self.all_spin_boxes[1][4].valueChanged.connect(self.onQ2WidthnessChanged)
		self.all_spin_boxes[1][5].valueChanged.connect(self.onQ2DelayChanged)

		self.all_spin_boxes[2][0].valueChanged.connect(self.onRMagnitudeChanged)
		self.all_spin_boxes[2][1].valueChanged.connect(self.onRWidthnessChanged)
		self.all_spin_boxes[2][2].valueChanged.connect(self.onRDelayChanged)

		self.all_spin_boxes[3][0].valueChanged.connect(self.onSMagnitudeChanged)
		self.all_spin_boxes[3][1].valueChanged.connect(self.onSWidthnessChanged)
		self.all_spin_boxes[3][2].valueChanged.connect(self.onSDelayChanged)

		self.all_spin_boxes[4][0].valueChanged.connect(self.onTMagnitudeChanged)
		self.all_spin_boxes[4][1].valueChanged.connect(self.onTWidthnessChanged)
		self.all_spin_boxes[4][2].valueChanged.connect(self.onTDelayChanged)

	def onPMagnitudeChanged(self, value):
		print('onPMagnitudeChanged')

	def onPWidthnessChanged(self, value):
		print('onPWidthnessChanged')

	def onPDelayChanged(self, value):
		print('onPDelayChanged')

	def onQ1MagnitudeChanged(self, value):
		print('onQ1MagnitudeChanged')

	def onQ1WidthnessChanged(self, value):
		print('onQ1WidthnessChanged')

	def onQ1DelayChanged(self, value):
		print('onQ1DelayChanged')

	def onQ2MagnitudeChanged(self, value):
		print('onQ2MagnitudeChanged')

	def onQ2WidthnessChanged(self, value):
		print('onQ2WidthnessChanged')

	def onQ2DelayChanged(self, value):
		print('onQ2DelayChanged')

	def onRMagnitudeChanged(self, value):
		print('onRMagnitudeChanged')

	def onRWidthnessChanged(self, value):
		print('onRWidthnessChanged')

	def onRDelayChanged(self, value):
		print('onRDelayChanged')

	def onSMagnitudeChanged(self, value):
		print('onSMagnitudeChanged')

	def onSWidthnessChanged(self, value):
		print('onSWidthnessChanged')

	def onSDelayChanged(self, value):
		print('onSDelayChanged')

	def onTMagnitudeChanged(self, value):
		print('onTMagnitudeChanged')

	def onTWidthnessChanged(self, value):
		print('onTWidthnessChanged')

	def onTDelayChanged(self, value):
		print('onTDelayChanged')
	

if __name__ == "__main__":
	global app
	app = QApplication([])
	q = ECGSimulation('ECG Simulation')
	q.showMaximized()
	sys.exit(app.exec_())