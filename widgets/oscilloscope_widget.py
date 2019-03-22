import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.metaarray import *
from PyQt5.QtCore import QPointF, pyqtSignal
from itertools import cycle
from PyQt5.QtCore import Qt
import os
import numpy as np


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/oscilloscope.ui')
OscilloscopeView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class Oscilloscope(TemplateBaseClass):
    region_updated = pyqtSignal(np.ndarray, int)
    region_cleared = pyqtSignal()
    create_signal = pyqtSignal(np.ndarray, int)

    def __init__(self):
        super().__init__()
        self.ui = OscilloscopeView()
        self.ui.setupUi(self)
        self.x_cursor = None

        self.init_cursor()
        self.init_slider()

        self.colorlist = ['r', 'g', 'b', 'c', 'm', 'w']
        self.colorpool = cycle(self.colorlist)

        self.multiplot_widget.setMinimumPlotHeight(250)

        self.ui.epoch_creation_button.clicked.connect(self.create_lr)

        self.lr = None

    def init_cursor(self):
        self.x_cursor = pg.InfiniteLine(pos=67, movable=True, angle=90,
                                        pen=pg.mkPen('r', width=3),
                                        hoverPen=pg.mkPen('g', width=3))
        self.multiplot_widget.addItem(self.x_cursor)
        self.x_cursor.sigPositionChanged.connect(self.on_cursor_moved)

    def init_slider(self):
        self.ui.horizontal_slider.valueChanged.connect(self.sliderValueChanged)

    def display_graph(self, signal):
        self.multiplot_widget.resizeEvent(None)

        data_buffer = np.zeros((1, len(signal.time_array)))
        for i in range(len(signal.time_array)):
            data_buffer[0][i] = signal.current_mode[i]

        ma = MetaArray(data_buffer, info=[{"cols": [{"name": signal.name, 'units': 'V'}]},
                                          {"name": "Time", "units": "sec",
                                           "values": signal.time_array}])

        random_color = next(self.colorpool)

        self.multiplot_widget.plot(ma)
        last_added_index = len(self.plots) - 1
        plot = self.get_plot(last_added_index)
        plot.getViewBox().setMouseEnabled(y=False)
        plot.listDataItems()[0].setPen(pg.mkPen(random_color))
        plot.scene().sigMouseClicked.connect(self.create_linear_region)
        plot.scene().sigMouseClicked.connect(self.singlemouseclick)

        if 'ECG' in signal.type:
            if signal.clusters is not None and signal.clusters[0] is not None:
                for cluster in signal.clusters[0]:
                    for info in cluster[1]:
                        min_value = signal.time_array[info[0][0]]
                        max_value = signal.time_array[info[0][1]]

                        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))

                        tooltip_text = 'Normal beat'

                        probability = info[1]

                        if 'APC' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(250, 128, 114, 50))
                            tooltip_text = 'Premature Atrial Contraction'
                        elif 'Normal' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(173, 255, 47, 50))
                        elif 'LBB' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(175, 238, 238, 50))
                            tooltip_text = 'Left Bundle Branch Block'
                        elif 'PAB' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(255, 0, 255, 50))
                            tooltip_text = 'Paced Beat'
                        elif 'PVC' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(240, 230, 140, 50))
                            tooltip_text = 'Premature Ventricular Contraction'
                        elif 'RBB' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(169, 169, 169, 50))
                            tooltip_text = 'Right Bundle Branch Block'
                        elif 'VEB' in cluster[0]:
                            brush = QtGui.QBrush(QtGui.QColor(205, 133, 63, 50))
                            tooltip_text = 'Ventricular Contraction'

                        lr = pg.LinearRegionItem(values=[min_value, max_value], brush=brush, movable=False)
                        lr.setToolTip(tooltip_text + ' with probability ' + str(probability))

                        plot.vb.addItem(lr)

            elif signal.annotations is not None:
                current_index = 0
                for i in range(signal.annotations.ann_len):
                    min_value = signal.time_array[current_index]
                    max_value = signal.time_array[signal.annotations.sample[i]]

                    current_index = signal.annotations.sample[i] + 1

                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))

                    annotation = signal.annotations.symbol[i]

                    tooltip_text = 'Normal beat'

                    if 'N' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(197, 214, 54, 50))
                    elif 'R' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(193, 18, 54, 50))
                        tooltip_text = 'Right bundle branch block beat'
                    elif 'L' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(137, 29, 11, 50))
                        tooltip_text = 'Left bundle branch block beat'
                    elif 'B' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(119, 230, 81, 50))
                        tooltip_text = 'Bundle branch block beat'
                    elif 'A' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(243, 248, 54, 50))
                        tooltip_text = 'Atrial premature beat'
                    elif 'a' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(47,41,54, 50))
                        tooltip_text = 'Aberrated atrial premature beat'
                    elif 'J' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(85,140,114, 50))
                        tooltip_text = 'Nodal (junctional) premature beat'
                    elif 'S' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(207,99,44, 50))
                        tooltip_text = 'Supraventricular premature or ectopic beat (atrial or nodal)'
                    elif 'V' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(30,119,98, 50))
                        tooltip_text = 'Premature ventricular contraction'
                    elif 'r' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(248,164,146, 50))
                        tooltip_text = 'R-on-T premature ventricular contraction'
                    elif 'F' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(27,49,27, 50))
                        tooltip_text = 'Fusion of ventricular and normal beat'
                    elif 'e' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(179,71,53, 50))
                        tooltip_text = 'Atrial escape beat'
                    elif 'j' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(242,207,88, 50))
                        tooltip_text = 'Nodal (junctional) escape beat'
                    elif 'n' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(73,0,30, 50))
                        tooltip_text = 'Supraventricular escape beat (atrial or nodal)'
                    elif 'E' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(206,2,7, 50))
                        tooltip_text = 'Ventricular escape beat'
                    elif '/' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(171,184,198, 50))
                        tooltip_text = 'Paced beat'
                    elif 'f' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(22,211,105, 50))
                        tooltip_text = 'Fusion of paced and normal beat'
                    elif 'Q' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(245,125,15, 50))
                        tooltip_text = 'Unclassifiable beat'
                    elif '?' in annotation:
                        brush = QtGui.QBrush(QtGui.QColor(164,142,131, 50))
                        tooltip_text = 'Beat not classified during learning'
                    elif '[' in annotation:
                        tooltip_text = 'Start of ventricular flutter/fibrillation'
                    elif '!' in annotation:
                        tooltip_text = 'Ventricular flutter wave'
                    elif ']' in annotation:
                        tooltip_text = 'End of ventricular flutter/fibrillation'
                    elif 'x' in annotation:
                        tooltip_text = 'Non-conducted P-wave (blocked APC)'
                    elif '(' in annotation:
                        tooltip_text = 'Waveform onset'
                    elif ')' in annotation:
                        tooltip_text = 'Waveform end'
                    elif 'p' in annotation:
                        tooltip_text = 'Peak of P-wave'
                    elif 't' in annotation:
                        tooltip_text = 'Peak of T-wave'
                    elif 'u' in annotation:
                        tooltip_text = 'Peak of U-wave'
                    elif '`' in annotation:
                        tooltip_text = 'PQ junction'
                    elif '\'' in annotation:
                        tooltip_text = 'J-point'
                    elif '^' in annotation:
                        tooltip_text = '(Non-captured) pacemaker artifact'
                    elif '|' in annotation:
                        tooltip_text = 'Isolated QRS-like artifact'
                    elif '~' in annotation:
                        tooltip_text = 'Change in signal quality'
                    elif '+' in annotation:
                        tooltip_text = 'Rhythm change'
                    elif 's' in annotation:
                        tooltip_text = 'ST segment change'
                    elif 'T' in annotation:
                        tooltip_text = 'T-wave change'
                    elif '*' in annotation:
                        tooltip_text = 'Systole'
                    elif 'D' in annotation:
                        tooltip_text = 'Diastole'
                    elif '=' in annotation:
                        tooltip_text = 'Measurement annotation'
                    elif '\"' in annotation:
                        tooltip_text = 'Comment annotation'
                    elif '@' in annotation:
                        tooltip_text = 'Link to external data'

                    lr = pg.LinearRegionItem(values=[min_value, max_value], brush=brush, movable=False)

                    lr.setToolTip(tooltip_text)

                    plot.vb.addItem(lr)

        self.proxy = pg.SignalProxy(self.get_plot(last_added_index).scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def update_plot(self, x, y, index):
        plot = self.get_plot(index)
        plot.clear()

        signal_color = self.colorlist[int(index % len(self.colorlist))]

        plot.plot(x, y, pen=signal_color)

    def create_linear_region(self, evt):
        if evt.double():
            evt.accept()
            for plotitem in self.plots:
                if type(plotitem[0]) is not int and plotitem[0].sceneBoundingRect().contains(evt.scenePos()):
                    mousePoint = plotitem[0].vb.mapSceneToView(evt.scenePos())
                    self.showLinearRegion(plotitem[0], mousePoint.x())
            self.ui.epoch_creation_button.setEnabled(True)

    def showLinearRegion(self, plotitem, mousepos_x):
        self.remove_all_linear_regions()
        values = plotitem.getAxis('bottom').range
        deltat = values[1] - values[0]
        minValue = mousepos_x
        maxValue = mousepos_x + 0.01 * deltat
        plotdataitemlist = [dataitem for dataitem in plotitem.vb.allChildren()
                            if isinstance(dataitem, pg.graphicsItems.PlotDataItem.PlotDataItem)]
        self.lr = pg.LinearRegionItem(values=[minValue, maxValue], bounds=[0, plotdataitemlist[0].xData[-1]])

        self.lr.sigRegionChangeFinished.connect(self.update_graph)

        plotitem.vb.addItem(self.lr)

    def update_graph(self):
        for index, plotitem in enumerate(self.plots):
            if self.lr in plotitem[0].vb.addedItems:
                minX, maxX = self.lr.getRegion()
                time = plotitem[0].dataItems[0].xData
                output = plotitem[0].dataItems[0].yData
                min_index = min(range(len(time)), key=lambda i: abs(time[i] - minX))
                max_index = min(range(len(time)), key=lambda i: abs(time[i] - maxX))
                self.region_updated.emit(output[min_index:max_index], index)

    def remove_all_linear_regions(self):
        for plotitem in self.plots:
            if self.lr in plotitem[0].vb.addedItems:
                plotitem[0].vb.removeItem(self.lr)
                self.lr = None

                self.region_cleared.emit()

        self.ui.epoch_creation_button.setEnabled(False)

    def singlemouseclick(self, evt):
        if evt.button() == QtCore.Qt.RightButton and self.lr is not None:
            for plotitem in self.plots:
                if type(plotitem[0]) is not int and plotitem[0].sceneBoundingRect().contains(evt.scenePos()):
                    view = plotitem[0].vb

        elif not evt.double():
            evt.accept()
            self.remove_all_linear_regions()

    def create_lr(self):
        for index, plotitem in enumerate(self.plots):
            if self.lr in plotitem[0].vb.addedItems:
                minX, maxX = self.lr.getRegion()
                time = plotitem[0].dataItems[0].xData
                output = plotitem[0].dataItems[0].yData
                min_index = min(range(len(time)), key=lambda i: abs(time[i] - minX))
                max_index = min(range(len(time)), key=lambda i: abs(time[i] - maxX))

                time = time[min_index:max_index]
                time = time.reshape((time.shape[0], 1))
                output = output[min_index:max_index]
                output = output.reshape((output.shape[0], 1))

                signal = np.hstack([time, output])
                self.create_signal.emit(signal, index)

    def get_plot(self, index):
        return self.plots[index][0]

    # dynamic time steps need to be added
    def sliderValueChanged(self):
        max_t = self.get_largest_time()
        min_t = self.get_smallest_time()

        window_size = (max_t - min_t) / 100

        lo_t = (self.ui.horizontal_slider.value() / 100) * max_t + min_t

        if lo_t >= max_t:
            lo_t = max_t - window_size
            self.ui.horizontal_slider.setValue(100)

        hi_t = lo_t + window_size
        for plot in self.plots:
            if plot is not int:
                plot[0].setRange(xRange=[lo_t, hi_t])

    def get_largest_time(self):
        max_t = 0
        for plot in self.plots:
            if plot[0].items is not int:
                max_local_t = plot[0].items[0].xData.max()
                if max_local_t > max_t:
                    max_t = max_local_t

        return max_t

    def get_smallest_time(self):
        min_t = 10
        for plot in self.plots:
            if plot[0].items is not int:
                min_local_t = plot[0].items[0].xData.min()
                if min_local_t < min_t:
                    min_t = min_local_t

        return min_t

    def on_cursor_moved(self):
        x = self.x_cursor.value()
        pos = QPointF(x, 0)
        mousePoint = self.plots[0][0].vb.mapSceneToView(pos)
        string_cursor = "Time: " + str(round(mousePoint.x(),4))
        self.ui.cursor_label.setText(string_cursor)

    def mouseMoved(self, evt):
        pos = evt[0]
        for plot_item in self.plots:
            if plot_item[0].sceneBoundingRect().contains(pos):
                mousePoint = plot_item[0].vb.mapSceneToView(pos)
                self.ui.label_x.setText("X: " + str(round(mousePoint.x(), 4)))
                self.ui.label_y.setText("Y: " + str(round(mousePoint.y(), 4)))

    @property
    def plots(self):
        return self.ui.multiplot_widget.mPlotItem.plots

    @property
    def multiplot_widget(self):
        return self.ui.multiplot_widget