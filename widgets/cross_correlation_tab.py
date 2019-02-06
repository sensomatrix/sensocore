from PyQt5.QtWidgets import QWidget, QVBoxLayout
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

    def user_clicks_on_button(self, channels):
        signals = channels.selectedItems()
        print(signals)
        signal_1 = signals[0]
        signal_2 = signals[1]

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