import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QDockWidget, QHBoxLayout, QSlider
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

		self.parameter_map = [
								[10 ** 3, 10 ** 4, 10 ** 4],
								[ -1 * 10 ** 4, 10 ** 5, 10 ** 4, 
								  -1 * 10 ** 4, 10 ** 6, 10 ** 5
								],
								[10 ** 3, 10 ** 5, 10 ** 5],
								[10 ** 3, 10 ** 5, 10 ** 4],
								[10 ** 4, 10 ** 5, 10 ** 4]
							 ]

		self.ecg_sim = ECGSimulationParameters(self)
		self.ecg_sim.connect(self.changeInParameter)

		self.addDockWidget(Qt.LeftDockWidgetArea, self.ecg_sim)
		self.show()

	def changeInParameter(self, value):
		for param_type_index in range(len(self.ecg_sim.all_sliders)):
			param_slider_index = self.getSenderIndex(self.sender(), param_type_index)
			
			if param_slider_index != -1:
				self.updateParameterValue(value, param_type_index, param_slider_index)
				return
		
	def getSenderIndex(self, sender, param_type_index):
		sliders = self.ecg_sim.all_sliders[param_type_index]

		for i in range(len(sliders)):
			if sender == sliders[i]:
				return i

		return -1

	def updateParameterValue(self, value, param_type_index, param_slider_index):
		divisor = self.parameter_map[param_type_index][param_slider_index ]

		if param_type_index == 0:
			self.P[param_slider_index] = value / divisor
		elif param_type_index == 1:
			self.Q[param_slider_index] = value / divisor
		elif param_type_index == 2:
			self.R[param_slider_index] = value / divisor
		elif param_type_index == 3:
			self.S[param_slider_index] = value / divisor
		elif param_type_index == 4:
			self.T[param_slider_index] = value / divisor

		self.plotECG()

	def plotECG(self):
		self.sim_graph.clear()
		self.sim_graph.plot(generateECG(self.sampling_freq, self.noise, self.end_time, self.period,
				self.P, self.Q, self.R, self.S, self.T))

	def initECGFunction(self):
		self.P, self.Q, self.R, self.S, self. T = returnDefault()
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
