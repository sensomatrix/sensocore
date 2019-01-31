from PyQt5.QtWidgets import QGroupBox, QDoubleSpinBox, QLabel, QGridLayout, QPushButton, QSpinBox

class SignalProperties(QGroupBox):
	def __init__(self):
		super().__init__('Signal Properties')

		self.initUI()
		self.initLayout()
		
	def initUI(self):
		self.initNoise()
		self.initSamplingFrequency()
		self.initDuration()
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

	def initDuration(self):
		self._duration_label = QLabel('Total Duration (S)')
		self._duration_spin_box = QDoubleSpinBox(self)

		self._duration_spin_box.setDecimals(1)
		self._duration_spin_box.setMinimum(0.9)
		self._duration_spin_box.setMaximum(21600) # 6 hours long
		self._duration_spin_box.setSingleStep(0.1)

	def setDefaultValues(self):
		self._noise_spin_box.setValue(0)
		self._sampling_freq_spin_box.setValue(256)
		self._duration_spin_box.setValue(0.9)

	def initLayout(self):
		layout = QGridLayout()

		layout.addWidget(self._noise_label)
		layout.addWidget(self._noise_spin_box)
		layout.addWidget(self._sampling_freq_label)
		layout.addWidget(self._sampling_freq_spin_box)
		layout.addWidget(self._duration_label)
		layout.addWidget(self._duration_spin_box)
		layout.addWidget(self._resetButton)

		self.setLayout(layout)

	@property
	def all_spin_boxes(self):
		return self._noise_spin_box

	def connectSignalProperties(self, noise_handler, sampling_freq_handler, duration_handler):
		self._noise_spin_box.valueChanged.connect(noise_handler)
		self._sampling_freq_spin_box.valueChanged.connect(sampling_freq_handler)
		self._duration_spin_box.valueChanged.connect(duration_handler)

	def connectResetButton(self, handler):
		self._resetButton.clicked.connect(handler)
