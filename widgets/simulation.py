import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QDockWidget, QHBoxLayout
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from ecg_parameters import ECGSimulationParameters

sys.path.append('simulations')
from ecg.ecg import generateECG, returnDefault

## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
 
class Simulation(QMainWindow):
	def __init__(self, title='ECG Simulation'):
		super().__init__()
		self.title = title
		self.initUI()
	 
	def initUI(self):
		self.setWindowTitle(self.title)
		self.sim_graph = SimulationGraph()
		self.setCentralWidget(self.sim_graph)

		self.initECGFunction()

		self.ecg_sim = ECGSimulationParameters(self)
		self.ecg_sim.connectParameters(self.changeInParameter)
		self.ecg_sim.connectProperties(self.changeInNoise)

		self.addDockWidget(Qt.LeftDockWidgetArea, self.ecg_sim)
		self.show()

	def changeInParameter(self, value):
		for param_type_index in range(len(self.ecg_sim.all_spin_boxes)):
			param_spin_box_index = self.getSenderIndex(self.sender(), param_type_index)
			
			if param_spin_box_index != -1:
				self.updateParameterValue(value, param_type_index, param_spin_box_index)
				return

	def changeInNoise(self, value):
		self.noise = value
		self.plotECG()
		
	def getSenderIndex(self, sender, param_type_index):
		spin_boxes = self.ecg_sim.all_spin_boxes[param_type_index]

		for i in range(len(spin_boxes)):
			if sender == spin_boxes[i]:
				return i

		return -1

	def updateParameterValue(self, value, param_type_index, param_spin_box_index):
		self.waves[param_type_index][param_spin_box_index] = value
		self.plotECG()

	def plotECG(self):
		self.sim_graph.clear()
		self.sim_graph.plot(generateECG(self.sampling_freq, self.noise, self.end_time, self.period,
				self.waves[0], self.waves[1], self.waves[2], self.waves[3], self.waves[4]))

	def initECGFunction(self):
		self.waves = returnDefault()
		self.sampling_freq = 256
		self.noise = 0
		self.end_time = 0.9
		self.period = 0.9
		self.plotECG()

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()

if __name__ == '__main__':
       app = QApplication(sys.argv)
       ex = Simulation()
       sys.exit(app.exec_())
