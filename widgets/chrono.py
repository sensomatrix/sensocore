from PyQt5.QtWidgets import QFrame, QSlider, QGridLayout, QLabel
from PyQt5.QtCore import Qt
import decimal
class Chrono(QFrame):
    
#class that contains the time-slider
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.create()
        
    def create(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.cursorValueLabel = QLabel("Cursor: ")
        grid_layout.addWidget(self.cursorValueLabel, 1, 1)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.sliderValueChanged)
        grid_layout.addWidget(self.slider, 2, 1)

    #dynamic time steps need to be added
    def sliderValueChanged(self):
        max_t = 0;
        for id, plotted_plot in self.parent.scope.plotitems_isPlotted_dictionary.items():
            if plotted_plot is True:
                last_t = (self.parent.parent.datasets.signals_dictionary.get(id)).time_array[-1]
                if last_t > max_t:
                    max_t = last_t
        window_size = max_t / 100
        lo_t = (self.slider.value() / 100) * max_t
        hi_t = lo_t + window_size
        for id, plotted_plot in self.parent.scope.plotitems_isPlotted_dictionary.items():
            if plotted_plot is True:
                (self.parent.scope.plotitems_dictionary.get(id)).setRange(xRange=[lo_t,hi_t])
                break
            else:
                continue
            break
            
    def on_cursor_moved(self, value):
        string_cursor = "Cursor: " + str(value) + " sec"
        self.cursorValueLabel.setText(string_cursor)



