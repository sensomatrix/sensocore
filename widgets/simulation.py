import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QDockWidget, QHBoxLayout, QSlider
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout

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
		self.addDockWidget(Qt.LeftDockWidgetArea, self.ecg_sim)
		self.show()

class SimulationGraph(pg.PlotWidget):
	def __init__(self):
		super().__init__()
		self.plotItem = self.getPlotItem()

class ECGSimulationParameters(QDockWidget):
		def __init__(self, parent):
			super().__init__(parent=parent)
			self.group_box = QGroupBox('ECG Simulation Parameters')
			self.main_layout = QGridLayout()

			self.initP()
			self.initQ()
			self.initR()
			self.initS()
			self.initT()
			self.initLayout()

		def initP(self):
			self.p_group = QGroupBox(self)

			self.p_w_slider = QSlider(Qt.Horizontal)
			self.p_m_slider = QSlider(Qt.Horizontal)
			self.p_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.p_w_slider)
			layout.addWidget(self.p_m_slider)
			layout.addWidget(self.p_t_slider)

			self.p_group.setLayout(layout)

		def initQ(self):
			self.q_group = QGroupBox(self)
			
			self.q_1_w_slider = QSlider(Qt.Horizontal)
			self.q_1_m_slider = QSlider(Qt.Horizontal)
			self.q_1_t_slider = QSlider(Qt.Horizontal)

			self.q_2_w_slider = QSlider(Qt.Horizontal)
			self.q_2_m_slider = QSlider(Qt.Horizontal)
			self.q_2_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.q_1_w_slider)
			layout.addWidget(self.q_1_m_slider)
			layout.addWidget(self.q_1_t_slider)

			layout.addWidget(self.q_2_w_slider)
			layout.addWidget(self.q_2_m_slider)
			layout.addWidget(self.q_2_t_slider)

			self.q_group.setLayout(layout)

		def initR(self):
			self.r_group = QGroupBox(self)

			self.r_w_slider = QSlider(Qt.Horizontal)
			self.r_m_slider = QSlider(Qt.Horizontal)
			self.r_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.r_w_slider)
			layout.addWidget(self.r_m_slider)
			layout.addWidget(self.r_t_slider)

			self.r_group.setLayout(layout)

		def initS(self):
			self.s_group = QGroupBox(self)

			self.s_w_slider = QSlider(Qt.Horizontal)
			self.s_m_slider = QSlider(Qt.Horizontal)
			self.s_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.s_w_slider)
			layout.addWidget(self.s_m_slider)
			layout.addWidget(self.s_t_slider)

			self.s_group.setLayout(layout)

		def initT(self):
			self.t_group = QGroupBox(self)

			self.t_w_slider = QSlider(Qt.Horizontal)
			self.t_m_slider = QSlider(Qt.Horizontal)
			self.t_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.t_w_slider)
			layout.addWidget(self.t_m_slider)
			layout.addWidget(self.t_t_slider)

			self.t_group.setLayout(layout)

		def initLayout(self):
			self.main_layout.addWidget(self.p_group,1,0)
			self.main_layout.addWidget(self.q_group,2,0)
			self.main_layout.addWidget(self.r_group,3,0)
			self.main_layout.addWidget(self.s_group,4,0)
			self.main_layout.addWidget(self.t_group,5,0)

			self.group_box.setLayout(self.main_layout)
			
			self.setWidget(self.group_box)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Simulation()
	sys.exit(app.exec_())
