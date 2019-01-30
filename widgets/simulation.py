import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

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
		self.show()

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()
		self.plotItem = self.getPlotItem()
		self.plotItem.showAxis('right')
		self.plotItem.hideAxis('left')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Simulation()
	sys.exit(app.exec_())