from PyQt5.QtWidgets import QAction, QToolButton, QMenu
from PyQt5.QtGui import QIcon
from pathlib import Path
from .simulation import Simulation

class SimulateButton(QToolButton):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_simulate_button()

    def init_simulate_button(self):
        self.eeg_action()
        self.ecg_action()
        
        simulation_menu = QMenu()
        simulation_menu.addAction(self.eeg_action)
        simulation_menu.addAction(self.ecg_action)

        fn = Path(__file__).parent.parent / 'icons' / 'icon-simulate.png'

        self.setIcon(QIcon(str(fn)))
        self.setPopupMode(2)
        self.setMenu(simulation_menu)

    def eeg_action(self):
        self.eeg_action = QAction("EEG Simulation", self.parent)
        self.eeg_action.setStatusTip('Create EEG Simulation')
        self.eeg_action.triggered.connect(lambda: self.simulation_window('EEG Simulation'))

    def ecg_action(self):
        self.ecg_action = QAction("ECG Simulation", self.parent)
        self.ecg_action.setStatusTip('Create ECG Simulation')
        self.ecg_action.triggered.connect(lambda: self.simulation_window('ECG Simulation'))

    def simulation_window(self, title):
        sim = Simulation(title, self.parent)

        if sim.output is not None:
            self.parent.datasets.loadFromSimulation(sim.output, sim.time_series, sim.sampling_freq, 'Sim test', type=title)
        