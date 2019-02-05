from PyQt5.QtWidgets import QFrame, QSlider, QGridLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import decimal


class Chrono(QFrame):

    # class that contains the time-slider
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.create()

    def create(self):
        self.cursorValueLabel = QLabel("Cursor: ")
        self.coords = QLabel("")
        self.coords.setAlignment(Qt.AlignRight)
        #self.coords.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        frame_horizontal = QFrame()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.cursorValueLabel)
        hlayout.addWidget(self.coords)
        frame_horizontal.setLayout(hlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(frame_horizontal)
        vlayout.addWidget(self.slider)
        self.setLayout(vlayout)

    # dynamic time steps need to be added
    def sliderValueChanged(self):
        max_t = 0;
        for id, plotted_plot in self.parent.scope.plotitems_isPlotted_dictionary.items():
            if plotted_plot is True:
                last_t = (self.parent.parent.parent.datasets.signals_dictionary.get(id)).time_array[-1]
                if last_t > max_t:
                    max_t = last_t
        window_size = max_t / 100
        lo_t = (self.slider.value() / 100) * max_t
        hi_t = lo_t + window_size
        for id, plotted_plot in self.parent.scope.plotitems_isPlotted_dictionary.items():
            if plotted_plot is True:
                (self.parent.scope.plotitems_dictionary.get(id)).setRange(xRange=[lo_t, hi_t])
                break
            else:
                continue
            break

    def on_cursor_moved(self, value):
        string_cursor = "Cursor: " + value
        self.cursorValueLabel.setText(string_cursor)
