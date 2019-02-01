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
		self.sim_params.connectParameters(self.onParameterChanged)

	def onParameterChanged(self, value):
		print(value)

if __name__ == "__main__":
	global app
	app = QApplication([])
	q = ECGSimulation('ECG Simulation')
	q.showMaximized()
	sys.exit(app.exec_())