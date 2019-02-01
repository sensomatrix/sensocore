import sys
from PyQt5.QtWidgets import QDialog, QApplication

class Simulation(QDialog):
	def __init__(self, title):
		self.title = title
		super().__init__()

	def initUI(self):
		self.setWindowTitle(self.title)

if __name__ == "__main__":
	global app
	app = QApplication([])
	q = Simulation('ECG Simulation')
	q.showMaximized()
	sys.exit(app.exec_())
