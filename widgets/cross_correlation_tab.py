from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5 import Qt
from widgets.cross_correlation import CrossCorrelation
import numpy as np
from scipy import signal


class CrossCorrelationTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.signal_1 = CrossCorrelation(self)
        self.signal_2 = CrossCorrelation(self)
        self.output = CrossCorrelation(self)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.signal_1)
        vbox.addWidget(self.signal_2)
        vbox.addWidget(self.output)

    def find_item_index(self, item, items):
        for _item, i in enumerate(items):
            if _item == item:
                return i

    def user_clicks_on_button(self, signals, channels):
        items = channels.selectedItems()

        if len(items) == 2:
            print('yes')
            print(items[0].data())

            signal_1 = signals.get(items[0].data(Qt.UserRole))
            signal_2 = signals.get(items[1].data(Qt.UserRole))

            if signal_1 is not None and signal_2 is not None:
                print('cool')

                x = np.linspace(0, 10 * np.pi, 200)
                cos = np.cos(x)

                self.signal_1.plot_data(cos)

                sin = np.sin(x)

                self.signal_2.plot_data(sin)

                corr = signal.correlate(cos, sin, mode='same')

                self.output.plot_data(corr)
            else:
                print('not cool')