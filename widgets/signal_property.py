from PyQt5.QtWidgets import QGroupBox, QDoubleSpinBox, QLabel, QGridLayout

class SignalProperties(QGroupBox):
	def __init__(self):
		super().__init__('Signal Properties')

		self.initUI()
		self.initLayout()
		
	def initUI(self):
		self.initNoise()

	def initNoise(self):
		self._noise_label = QLabel('Noise (Mean Value)')
		self._noise_spin_box = QDoubleSpinBox(self)

		self._noise_spin_box.setDecimals(4)
		self._noise_spin_box.setMinimum(0)
		self._noise_spin_box.setMaximum(0.05)
		self._noise_spin_box.setSingleStep(0.0001)

	def initLayout(self):
		layout = QGridLayout()

		layout.addWidget(self._noise_label)
		layout.addWidget(self._noise_spin_box)

		self.setLayout(layout)

	@property
	def all_spin_boxes(self):
		return self._noise_spin_box

	def connectSignalProperties(self, handler):
		self._noise_spin_box.valueChanged.connect(handler)
	