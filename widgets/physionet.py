import sys
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QSplitter
import pyqtgraph as pg
import wfdb
import matplotlib.pyplot as plt

class PhysioNetDialog(QDialog):
	def __init__(self, parent=None):
		self.record = wfdb.rdrecord('100', pb_dir='mitdb/', sampfrom=0, sampto=10**4)
		self.parent = parent
		super().__init__()
		self.initUI()
		self.initLayout()
		signals = self.record.p_signal.transpose()

		for signal in signals:
			self._sim_graph.plot(signal)

	def initUI(self):
		self.setWindowTitle('PhysioNet import')

		self._sim_graph = pg.PlotWidget()
		self._sim_graph.setBackground('w')

	def initLayout(self):
		splitter = QSplitter()

		splitter.addWidget(self._sim_graph)

		h_box = QHBoxLayout(self)

		h_box.addWidget(splitter)

		self.setLayout(h_box)

if __name__ == "__main__":
	global app
	app = QApplication([])
	q = PhysioNetDialog()
	q.showMaximized()
	sys.exit(app.exec_())
