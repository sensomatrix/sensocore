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
			self.p_group, self.p_slider = self.createWaveParameters('P')

		def initQ(self):
			q_label = [QLabel('Q1 Magnitude'), QLabel('Q1 Widthness'), QLabel('Q1 Time'),
					   QLabel('Q2 Magnitude'), QLabel('Q2 Widthness'), QLabel('Q2 Time')]

			self.q_group, self.q_slider = self.createWaveParameters('Q', wave_label=q_label, num_params=6)

		def initR(self):
			self.r_group, self.r_slider = self.createWaveParameters('R')

		def initS(self):
			self.s_group, self.s_slider = self.createWaveParameters('S')

		def initT(self):
			self.t_group, self.t_slider = self.createWaveParameters('T')

		def createWaveParameters(self, signal_type, wave_label=None,num_params=3):
			if wave_label == None:
				wave_label = [QLabel('Magnitude'), QLabel('Widthness'), QLabel('Time')]

			wave_group = QGroupBox(signal_type + ' Wave Parameters',self)

			wave_slider = [QSlider(Qt.Horizontal, self) for _ in range(num_params)]

			layout = QGridLayout()

			for i in range(num_params):
				layout.addWidget(wave_label[i],0,i)
				layout.addWidget(wave_slider[i],1,i)

			wave_group.setLayout(layout)

			return wave_group, wave_slider

		def initLayout(self):
			self.main_layout.addWidget(self.p_group,1,0)
			self.main_layout.addWidget(self.q_group,2,0)
			self.main_layout.addWidget(self.r_group,3,0)
			self.main_layout.addWidget(self.s_group,4,0)
			self.main_layout.addWidget(self.t_group,5,0)

			self.group_box.setLayout(self.main_layout)

			self.all_sliders = [self.p_slider, self.q_slider, self.r_slider,
								self.s_slider, self.t_slider]
			
			self.setWidget(self.group_box)

		def connect(self, handler):
			for param_slider in self.all_sliders:
				for slider in param_slider:
					slider.valueChanged.connect(handler)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Simulation()
	sys.exit(app.exec_())
