from .eeg_parameters import EEGSimulationParameters
from .simulation import Simulation

import sys

sys.path.append('simulations')
from simulations.eeg.jansen import simulate_eeg_jansen

class EEGSimulation(Simulation):
	def __init__(self, title, parent):
		super().__init__(title, parent=parent)

		self.addSimAndSigParameters(EEGSimulationParameters(), props_to_remove=['P'])
		self.sig_params.setDefaultValues(sampling_frequency=256, duration=10)
		self.setupConnections()
		self.plotEEGSignal()
		self.sig_params.setDefaultName('EEG Simulation')
		self.exec_()

	def setupConnections(self):
		self.sim_params.preview_button.clicked.connect(self.onValueChanged)
		self.sig_params.reset_button.clicked.connect(self.onReset)
		self.sig_params.create_button.clicked.connect(self.onCreate)

	def onValueChanged(self):
		self.plotEEGSignal()

	def progress_handler(self, value):
		self.progress_bar.setValue(value)

	def onCreate(self):
		self.time_series, self.output = simulate_eeg_jansen(duration=self.sig_params.end_time, fs=self.sig_params.sampling_frequency,
						C1=self.sim_params.C1, noise_magnitude=self.sig_params.noise_magnitude, callback=self.progress_handler)

		self.parent.datasets.loadFromSimulation(self.output, self.time_series, self.sig_params.sampling_frequency,
							self.sig_params.name_text_field.text(), type=self.title)
		self.close()

	def plotEEGSignal(self):
		self.sim_graph.clear()
		time_series, output = simulate_eeg_jansen(fs=self.sig_params.sampling_frequency, C1=self.sim_params.C1,
												  noise_magnitude=self.sig_params.noise_magnitude, callback=self.progress_handler)
		self.sim_graph.plot(time_series, output, pen='k')