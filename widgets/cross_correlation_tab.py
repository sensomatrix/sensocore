from PyQt5.QtWidgets import QWidget, QVBoxLayout
from widgets.cross_correlation import CrossCorrelation
from scipy import signal
from timeutils import generateTimeArrayFromNumberOfSamples


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

    def user_clicks_on_button(self, signals, selected_channels_list_by_id):
        if len(selected_channels_list_by_id) == 2:
            print('yes')
            signal_1 = signals.get(selected_channels_list_by_id[0])
            signal_2 = signals.get(selected_channels_list_by_id[1])

            if signal_1 is not None and signal_2 is not None:
                print('cool')

                self.signal_1.plot_data(signal_1.time_array, signal_1.samples_array)
                self.signal_2.plot_data(signal_2.time_array, signal_2.samples_array)

                time_array = generateTimeArrayFromNumberOfSamples(signal_2.fs,
                                                                  len(signal_1.samples_array) + len(
                                                                      signal_2.samples_array) - 1)

                corr = signal.correlate(signal_1.samples_array, signal_2.samples_array, mode='full')

                self.output.plot_data(time_array, corr)
            else:
                print('not cool')