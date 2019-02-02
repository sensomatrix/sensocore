from PyQt5.QtWidgets import (QGroupBox, QDoubleSpinBox, QLabel, 
							QGridLayout, QPushButton, QSpinBox, QLineEdit)

class SignalProperties(QGroupBox):
	def __init__(self, props_to_remove=[]):
		super().__init__('Signal Properties')

		self.initUI()
		self.initLayout(props_to_remove)
		
	def initUI(self):
		self.initNoise()
		self.initSamplingFrequency()
		self.initDuration()
		self.initResetButton()
		self.initPeriod()
		self.initCreateButton()
		self.initNameField()
		self.setDefaultValues()

	def initNoise(self):
		self._noise_label = QLabel('Noise (Mean Value)')
		self._noise_spin_box = QDoubleSpinBox(self)

		self._noise_spin_box.setDecimals(4)
		self._noise_spin_box.setMinimum(0)
		self._noise_spin_box.setMaximum(10)
		self._noise_spin_box.setSingleStep(0.0001)

	def initResetButton(self):
		self._reset_button = QPushButton("Reset to default")

	def initCreateButton(self):
		self._create_button = QPushButton("Create Signal")

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
		self._noise_spin_box.setValue(self._noise_magnitude)
		self._sampling_freq_spin_box.setValue(self._sampling_frequency)
		self._duration_spin_box.setValue(self._duration)
		self._period_spin_box.setValue(self._period)

	def setDefaultValues(self, noise_magnitude=0, sampling_frequency=256,
						 duration=0.9, period=0.9):
		self._noise_magnitude = noise_magnitude
		self._sampling_frequency = sampling_frequency
		self._duration = duration
		self._period = period
		self.setToDefaultValues()

	def initLayout(self, props_to_remove):
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
		layout.addWidget(self._reset_button)
		layout.addWidget(self._create_button)

		properties = {
					'F': [self._sampling_freq_label, self.sampling_freq_spin_box],
					'D': [self._duration_label, self.duration_spin_box],
					'P': [self._period_label, self._period_spin_box],
		}

		for prop in props_to_remove:
			properties[prop][0].close()
			properties[prop][1].close()

			layout.removeWidget(properties[prop][0])
			layout.removeWidget(properties[prop][1])

		self.setLayout(layout)

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

	@property
	def noise_spin_box(self):
		return self._noise_spin_box
	
	@property
	def sampling_freq_spin_box(self):
		return self._sampling_freq_spin_box
	
	@property
	def duration_spin_box(self):
		return self._duration_spin_box

	@property
	def period_spin_box(self):
		return self._period_spin_box

	@property
	def reset_button(self):
		return self._reset_button

	@property
	def create_button(self):
		return self._create_button