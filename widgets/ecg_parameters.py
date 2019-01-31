from PyQt5.QtWidgets import QGroupBox, QDockWidget, QHBoxLayout, QDoubleSpinBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
from signal_property import SignalProperties
import copy

class ECGSimulationParameters(QDockWidget):
		def __init__(self, parent):
			super().__init__(parent=parent)
			self.group_box = QGroupBox('ECG Simulation Parameters')
			self.main_layout = QGridLayout()

			self.sig_values = {
				"P":
					{
						"init_values": [0.185, 0.0178, 0.2369],
						"min_values": [0.1, 0.01, 0.2],
						"max_values": [0.3, 0.03, 0.3],
					},
				"Q":
					{
						"init_values": [-0.1103, 0.03064, 0.3218, -0.1075, 0.005705, 0.37123],
						"min_values": [-0.2, 0.025, 0.25, -0.15, 0.005, 0.36],
						"max_values": [-0.1, 0.035, 0.35, -0.05, 0.006, 0.38],
					},
				"R":
					{
						"init_values": [0.05, 0.02987, 0.46571],
						"min_values": [0.025, 0.029, 0.46],
						"max_values": [0.125, 0.031, 0.47],
					},
				"S":
					{
						"init_values": [0.509, 0.00909, 0.4769],
						"min_values": [0.4, 0.008, 0.46],
						"max_values": [0.6, 0.01, 0.48],
					},
				"T":
					{
						"init_values": [0.3255, 0.02978, 0.7543],
						"min_values": [0.31, 0.028, 0.74],
						"max_values": [0.33, 0.031, 0.76],
					}
			}

			self.initP()
			self.initQ()
			self.initR()
			self.initS()
			self.initT()
			self.sig_props = SignalProperties()
			self.initLayout()
			self.setToDefaultValues()


		def initP(self):
			self.p_group, self.p_spin_box = self.createWaveParameters('P')

		def initQ(self):
			q_label = [QLabel('Q1 Magnitude'), QLabel('Q1 Widthness'), QLabel('Q1 Time'),
					   QLabel('Q2 Magnitude'), QLabel('Q2 Widthness'), QLabel('Q2 Time')]

			self.q_group, self.q_spin_box = self.createWaveParameters('Q', wave_label=q_label, num_params=6)

		def initR(self):
			self.r_group, self.r_spin_box = self.createWaveParameters('R')

		def initS(self):
			self.s_group, self.s_spin_box = self.createWaveParameters('S')

		def initT(self):
			self.t_group, self.t_spin_box = self.createWaveParameters('T')

		def createWaveParameters(self, signal_type, wave_label=None, num_params=3):
			if wave_label == None:
				wave_label = [QLabel('Magnitude'), QLabel('Widthness'), QLabel('Time')]

			wave_group = QGroupBox(signal_type + ' Wave Parameters',self)

			wave_spin_box = [QDoubleSpinBox(self) for _ in range(num_params)]

			self.initDoubleSpinBox(signal_type, wave_spin_box)

			layout = QGridLayout()

			for i in range(num_params):
				layout.addWidget(wave_label[i],0,i)
				layout.addWidget(wave_spin_box[i],1,i)

			wave_group.setLayout(layout)

			return wave_group, wave_spin_box

		def initDoubleSpinBox(self, signal_type, spin_boxes, single_step=0.0001, precision=4):
			for i, spin_box in enumerate(spin_boxes):
				spin_box.setDecimals(precision)
				spin_box.setMinimum(self.sig_values[signal_type]['min_values'][i])
				spin_box.setMaximum(self.sig_values[signal_type]['max_values'][i])
				spin_box.setSingleStep(single_step)

		def initLayout(self):
			self.main_layout.addWidget(self.p_group,1,0)
			self.main_layout.addWidget(self.q_group,2,0)
			self.main_layout.addWidget(self.r_group,3,0)
			self.main_layout.addWidget(self.s_group,4,0)
			self.main_layout.addWidget(self.t_group,5,0)
			self.main_layout.addWidget(self.sig_props,6,0)

			self.group_box.setLayout(self.main_layout)

			self.all_spin_boxes = [self.p_spin_box, self.q_spin_box, self.r_spin_box,
								self.s_spin_box, self.t_spin_box]
			
			self.setWidget(self.group_box)

		def connectParameters(self, handler):
			for spin_boxes in self.all_spin_boxes:
				for spin_box in spin_boxes:
					spin_box.valueChanged.connect(handler)

		def connectProperties(self, noise_handler, reset_handler, sampling_freq_handler):
			self.sig_props.connectSignalProperties(noise_handler, sampling_freq_handler)
			self.sig_props.connectResetButton(reset_handler)

		def getDefaultValues(self):
			return  [
						copy.deepcopy(self.sig_values['P']['init_values']),
						copy.deepcopy(self.sig_values['Q']['init_values']),
						copy.deepcopy(self.sig_values['R']['init_values']),
						copy.deepcopy(self.sig_values['S']['init_values']),
						copy.deepcopy(self.sig_values['T']['init_values'])
					]

		def setToDefaultValues(self):
			signal_types = ['P', 'Q', 'R', 'S', 'T']

			for j, spin_box_type in enumerate(self.all_spin_boxes):
				for i, spin_box in enumerate(spin_box_type):
					spin_box.setValue(self.sig_values[signal_types[j]]['init_values'][i])

			self.sig_props.setDefaultValues()
