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

		self.ecg_sim = ECGSimulationParameters(self)
		self.ecg_sim.connect(self.changeInParameter)

		self.addDockWidget(Qt.LeftDockWidgetArea, self.ecg_sim)
		self.show()

	def changeInParameter(self, value):
		for param_slider in self.ecg_sim.all_sliders:
			i = self.getSenderIndex(self.sender(), param_slider)
			
			if i != -1:
				print(i)
				return
		
	def getSenderIndex(self, sender, sliders):
		for i in range(len(sliders)):
			if sender == sliders[i]:
				return i

		return -1

	def initECGFunction(self):
		self.P, self.Q, self.R, self.S, self. T = returnDefault()	
		self.sampling_freq = 256
		self.noise = 0.01
		self.end_time = 0.9
		self.period = 0.9
		self.sim_graph.plot(generateECG(self.sampling_freq, self.noise, self.end_time, self.period,
				self.P, self.Q, self.R, self.S, self.T))

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()

if __name__ == '__main__':
       app = QApplication(sys.argv)
       ex = Simulation()
       sys.exit(app.exec_())
