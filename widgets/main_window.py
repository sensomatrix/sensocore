from views import main, oscilloscope
from PyQt5.QtWidgets import QMainWindow, QApplication
from itertools import cycle
import pyqtgraph as pg
import numpy as np
from pyqtgraph.metaarray import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main.Ui_MainWindow()
        self.ui.oscilloscope = oscilloscope.Ui_Form()
        self.ui.setupUi(self)
        self.ui.oscilloscope.setupUi(self.ui.oscilloscope_tab)
        self.x_cursor = None

        self._current_item_size = 0

        self._latest_element = 0
        color_list = ['r', 'g', 'b', 'c', 'm', 'k']
        self.color_pool = cycle(color_list)

        self.init_ui()
        self.display_graph([1,2,3,4,5,6,7,8,9,10], np.transpose([0,4,1,2,7,5,3,8,0,1]))

    def init_ui(self):
        self.add_cursor()

        self.ui.textBrowser.setReadOnly(True)
        self.ui.textBrowser.setText('Testing trying to output something\nWith a new line')

    def add_cursor(self):
        self.x_cursor = pg.InfiniteLine(pos=67, movable=True, angle=90,
                                        pen=pg.mkPen('r', width=3),
                                        hoverPen=pg.mkPen('g', width=3))
        self.multiplot_widget.addItem(self.x_cursor)

    def display_graph(self, x, y):
        data_buffer = np.zeros((1, len(x)))
        for i in range(len(x)):
            data_buffer[0][i] = y[i]
        ma = MetaArray(data_buffer, info=[{"cols": [{"name": "Testing"}]},
                                          {"name": "Time", "units": "sec",
                                           "values": x}])
        self.multiplot_widget.plot(ma)
        last_added_index = len(self.plots) - 1
        self.plots[last_added_index][0].getViewBox().setMouseEnabled(y=False)

    @property
    def plots(self):
        return self.ui.oscilloscope.multiplot_widget.mPlotItem.plots

    @property
    def multiplot_widget(self):
        return self.ui.oscilloscope.multiplot_widget

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())