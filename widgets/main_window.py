from views.main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()
        self.ui.oscilloscope_tab.display_graph([0,1,2,3,4,5,6,7,8,9,10], np.transpose([-10,0,4,1,2,7,5,3,8,0,1]))

    def init_ui(self):
        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setText('Testing trying to output something\nWith a new line')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())