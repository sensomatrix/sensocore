import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QDockWidget, QHBoxLayout, QSlider
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from ecg_parameters import ECGSimulationParameters

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

		self.ecg_sim = ECGSimulationParameters(self)
		self.ecg_sim.connect(self.mySlot)

		self.addDockWidget(Qt.LeftDockWidgetArea, self.ecg_sim)
		self.show()

	def mySlot(self, value):
		i = self.getSenderIndex(self.sender(), self.ecg_sim.p_slider)
		
		if i != -1:
			print(i)
		else:
			print('not in p group')
		
	def getSenderIndex(self, sender, sliders):
		for i in range(len(sliders)):
			if sender == sliders[i]:
				return i

		return -1

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()
		self.plotItem = self.getPlotItem()

if __name__ == '__main__':
       app = QApplication(sys.argv)
       ex = Simulation()
       sys.exit(app.exec_())
