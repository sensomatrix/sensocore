from PyQt5.QtWidgets import QGroupBox, QDoubleSpinBox, QLabel, QGridLayout, QPushButton, QSpinBox

class SignalProperties(QGroupBox):
	def __init__(self):
		super().__init__('Signal Properties')

		self.initUI()
		self.initLayout()
		
	def initUI(self):
		self.initNoise()
		self.initSamplingFrequency()
		self.initResetButton()
		self.setDefaultValues()

	def initNoise(self):
		self._noise_label = QLabel('Noise (Mean Value)')
		self._noise_spin_box = QDoubleSpinBox(self)

		self._noise_spin_box.setDecimals(4)
		self._noise_spin_box.setMinimum(0)
		self._noise_spin_box.setMaximum(0.05)
		self._noise_spin_box.setSingleStep(0.0001)

	def initResetButton(self):
		self._resetButton = QPushButton("Reset to default")

	def initSamplingFrequency(self):
		self._sampling_freq_label = QLabel('Sampling Frequency (Hz)')
		self._sampling_freq_spin_box = QSpinBox(self)

		self._sampling_freq_spin_box.setMinimum(100)
		self._sampling_freq_spin_box.setMaximum(10 ** 4)

	def setDefaultValues(self):
		self._noise_spin_box.setValue(0)
		self._sampling_freq_spin_box.setValue(256)

	def initLayout(self):
		layout = QGridLayout()

		layout.addWidget(self._noise_label)
		layout.addWidget(self._noise_spin_box)
		layout.addWidget(self._sampling_freq_label)
		layout.addWidget(self._sampling_freq_spin_box)
		layout.addWidget(self._resetButton)

		self.setLayout(layout)

	@property
	def all_spin_boxes(self):
		return self._noise_spin_box

	def connectSignalProperties(self, noise_handler, sampling_freq_handler):
		self._noise_spin_box.valueChanged.connect(noise_handler)
		self._sampling_freq_spin_box.valueChanged.connect(sampling_freq_handler)

	def connectResetButton(self, handler):
		self._resetButton.clicked.connect(handler)
