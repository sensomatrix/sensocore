from .eeg_parameters import EEGSimulationParameters
from .simulation import Simulation

import sys

sys.path.append('simulations')
from eeg.jansen import simulate_eeg_jansen

class EEGSimulation(Simulation):
	def __init__(self, title, parent):
		super().__init__(title, parent=parent)
		self.addSimAndSigParameters(EEGSimulationParameters(), props_to_remove=['N', 'P'])
		self.sig_params.setDefaultValues(sampling_frequency=100, duration=10)
		self.setupConnections()
		self.plotEEGSignal()
		self.exec_()

	def setupConnections(self):
		self.sim_params.preview_button.clicked.connect(self.onValueChanged)
		self.sig_params.reset_button.clicked.connect(self.onReset)
		self.sig_params.create_button.clicked.connect(self.onCreate)

	def onValueChanged(self):
		self.plotEEGSignal()

	def onCreate(self):
		self.time_series, self.output = simulate_eeg_jansen(duration=self.sig_params.end_time, fs=self.sig_params.sampling_frequency, C1=self.sim_params.C1)

		self.parent.datasets.loadFromSimulation(self.output, self.time_series, self.sig_params.sampling_frequency, self.sig_params.name_text_field.text(), type=self.title)
		self.close()

	def plotEEGSignal(self):
		self.sim_graph.clear()
		time, output = simulate_eeg_jansen()
		self.sim_graph.plot(time, output, pen='k')