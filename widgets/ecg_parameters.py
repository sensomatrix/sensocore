from PyQt5.QtWidgets import QGroupBox, QDockWidget, QHBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout

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
			self.p_group = QGroupBox('P Wave Parameters',self)

			self.p_slider = [QSlider(Qt.Horizontal) for _ in range(3)]
			p_label = [QLabel('Widthness'), QLabel('Magnitude'), QLabel('Time')]

			layout = QGridLayout()

			for i in range(3):
				layout.addWidget(p_label[i],0,i)
				layout.addWidget(self.p_slider[i],1,i)

			self.p_group.setLayout(layout)

		def initQ(self):
			self.q_group = QGroupBox('Q Wave Parameters',self)

			self.q_slider = [QSlider(Qt.Horizontal) for _ in range(6)]
			q_label = [QLabel('Q1 Widthness'), QLabel('Q1 Magnitude'), QLabel('Q1 Time'),
					   QLabel('Q2 Widthness'), QLabel('Q2 Magnitude'), QLabel('Q2 Time')]

			layout = QGridLayout()

			for i in range(6):
				layout.addWidget(q_label[i],0,i)
				layout.addWidget(self.q_slider[i],1,i)
				
			self.q_group.setLayout(layout)

		def initR(self):
			self.r_group = QGroupBox('R Wave Parameters', self)

			self.r_w_slider = QSlider(Qt.Horizontal)
			self.r_m_slider = QSlider(Qt.Horizontal)
			self.r_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.r_w_slider)
			layout.addWidget(self.r_m_slider)
			layout.addWidget(self.r_t_slider)

			self.r_group.setLayout(layout)

		def initS(self):
			self.s_group = QGroupBox('S Wave Parameters', self)

			self.s_w_slider = QSlider(Qt.Horizontal)
			self.s_m_slider = QSlider(Qt.Horizontal)
			self.s_t_slider = QSlider(Qt.Horizontal)

			layout = QHBoxLayout()

			layout.addWidget(self.s_w_slider)
			layout.addWidget(self.s_m_slider)
			layout.addWidget(self.s_t_slider)

			self.s_group.setLayout(layout)

		def initT(self):
			self.t_group = QGroupBox('T Wave Parameters', self)

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
