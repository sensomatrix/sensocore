from PyQt5.QtWidgets import (QGroupBox, QDoubleSpinBox, QLabel, 
							QGridLayout, QPushButton, QSpinBox, QLineEdit)

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
		self.initPeriod()
		self.initCreateButton()
		self.initNameField()
		self.setToDefaultValues()

	def initNoise(self):
		self._noise_label = QLabel('Noise (Mean Value)')
		self._noise_spin_box = QDoubleSpinBox(self)

		self._noise_spin_box.setDecimals(4)
		self._noise_spin_box.setMinimum(0)
		self._noise_spin_box.setMaximum(0.05)
		self._noise_spin_box.setSingleStep(0.0001)

	def initResetButton(self):
		self._resetButton = QPushButton("Reset to default")

	def initCreateButton(self):
		self._createButton = QPushButton("Create Signal")

	def initSamplingFrequency(self):
		self._sampling_freq_label = QLabel('Sampling Frequency (Hz)')
		self._sampling_freq_spin_box = QSpinBox(self)

		self._sampling_freq_spin_box.setMinimum(100)
		self._sampling_freq_spin_box.setMaximum(10 ** 4)

	def initDuration(self):
		self._duration_label = QLabel('Total Duration (s)')
		self._duration_spin_box = QDoubleSpinBox(self)

		self._duration_spin_box.setDecimals(1)
		self._duration_spin_box.setMinimum(0.9)
		self._duration_spin_box.setMaximum(21600) # 6 hours long
		self._duration_spin_box.setSingleStep(0.1)

	def initPeriod(self):
		self._period_label = QLabel('Period (s)')
		self._period_spin_box = QDoubleSpinBox(self)

		self._period_spin_box.setDecimals(3)
		self._period_spin_box.setMinimum(0.5)
		self._period_spin_box.setMaximum(1.5)
		self._period_spin_box.setSingleStep(0.001)

	def initNameField(self):
		self._name_label = QLabel('Signal Name')
		self._name_text_field = QLineEdit(self)

	def setToDefaultValues(self):
		self._name_text_field.setText('Sim Example')
		self._noise_spin_box.setValue(0)
		self._sampling_freq_spin_box.setValue(256)
		self._duration_spin_box.setValue(0.9)
		self._period_spin_box.setValue(0.9)

	def initLayout(self):
		layout = QGridLayout()

		layout.addWidget(self._name_label)
		layout.addWidget(self._name_text_field)
		layout.addWidget(self._noise_label)
		layout.addWidget(self._noise_spin_box)
		layout.addWidget(self._sampling_freq_label)
		layout.addWidget(self._sampling_freq_spin_box)
		layout.addWidget(self._duration_label)
		layout.addWidget(self._duration_spin_box)
		layout.addWidget(self._period_label)
		layout.addWidget(self._period_spin_box)
		layout.addWidget(self._resetButton)
		layout.addWidget(self._createButton)

		self.setLayout(layout)

	@property
	def all_spin_boxes(self):
		return self._noise_spin_box

	@property
	def name_text_field(self):
		return self._name_text_field
	
	@property
	def sampling_frequency(self):
		return self._sampling_freq_spin_box.value()

	@property
	def noise_magnitude(self):
		return self._noise_spin_box.value()

	@property
	def end_time(self):
		return self._duration_spin_box.value()
	
	@property
	def period(self):
		return self._period_spin_box.value()

	def connectSignalProperties(self, noise_handler, sampling_freq_handler, 
								duration_handler, period_handler, reset_handler, create_handler):
		self._noise_spin_box.valueChanged.connect(noise_handler)
		self._sampling_freq_spin_box.valueChanged.connect(sampling_freq_handler)
		self._duration_spin_box.valueChanged.connect(duration_handler)
		self._period_spin_box.valueChanged.connect(period_handler)
		self.connectResetButton(reset_handler)
		self.connectCreateButton(create_handler)

	def connectResetButton(self, handler):
		self._resetButton.clicked.connect(handler)

	def connectCreateButton(self, handler):
		self._createButton.clicked.connect(handler)