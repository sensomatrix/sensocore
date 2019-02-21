from views import main, oscilloscope
from PyQt5.QtWidgets import QMainWindow, QApplication
from itertools import cycle
from pyqtgraph.metaarray import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self)

        self._current_item_size = 0

        self._latest_element = 0
        color_list = ['r', 'g', 'b', 'c', 'm', 'k']
        self.colorpool = cycle(color_list)

        self.init_ui()

    def init_ui(self):
        self.ui.oscilloscope = oscilloscope.Ui_Form()
        self.ui.oscilloscope.setupUi(self.ui.oscilloscope_tab)

        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setText('Testing trying to output something\nWith a new line')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())