from PyQt5.QtWidgets import QGroupBox, QSpinBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGridLayout
import copy

class EEGSimulationParameters(QGroupBox):
		def __init__(self):
			super().__init__()
			self.main_layout = QGridLayout()
			
			self.sig_values = {
				"C1":
					{
						"init_value": 135,
						"min_value": 100,
						"max_value": 2000,
					},
			}

			self.initC1()
			self.initLayout()
			self.setToDefaultValues()

		def initC1(self):
			self._c_1_spin_box = QSpinBox(self)
			self._c_1_spin_box.setMinimum(self.sig_values['C1']['min_value'])
			self._c_1_spin_box.setMaximum(self.sig_values['C1']['max_value'])
				
		def initLayout(self):
			c_1_label = QLabel('C1')

			self.main_layout.addWidget(c_1_label)
			self.main_layout.addWidget(self._c_1_spin_box)

			self.setLayout(self.main_layout)
			
		def setToDefaultValues(self):
			self._c_1_spin_box.setValue(self.sig_values['C1']['init_value'])

		@property
		def c_1_spin_box(self):
			return self._c_1_spin_box

		@property
		def C1(self):
			return self._c_1_spin_box.value()