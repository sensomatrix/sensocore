import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from .Plotter import FilterPlotter, FilteredSignalPlotter
import numpy as np
from utils.filtersutils import design_FIR_ls, design_FIR_parks, estimate_order
from scipy.signal import freqz, convolve
import pickle
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/fir_filter_designer.ui')
FIRDesignerView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class FIRDesignerDialog(TemplateBaseClass):
    def __init__(self, signals):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = FIRDesignerView()
        self.ui.setupUi(self)

        self.signals = signals
        self.current_signal = None

        self.ui.channel_combo_box.setModel(self.signals)
        self.ui.channel_combo_box.currentIndexChanged.connect(self.item_changed)
        self.item_changed(0)

        self.ui.save_to_file_button.clicked.connect(self.save_filter_to_file)
        self.ui.estimate_taps_button.clicked.connect(self.estimate_taps_button_pressed)
        self.ui.design_filter_button.clicked.connect(self.design_filter)

    def item_changed(self, index):
        self.current_signal = self.ui.channel_combo_box.itemData(index)
        self.ui.sampling_frequency_label.setText('fs: ' + str(self.current_signal.fs) + 'Hz')

    def save_filter_to_file(self):
        savefilepath = QFileDialog.getSaveFileName(self.parent, "Save filter to file")
        if savefilepath[0]:
            self.save_object(self.filter, savefilepath[0])

    def save_object(self, obj, filename):
        with open(filename, 'wb') as outputfile:
            pickle.dump(obj, outputfile, pickle.HIGHEST_PROTOCOL)

    def estimate_taps_button_pressed(self):
        if '' in [self.ui.passband_ripple_line_edit.text(), self.ui.stopband_rejection_line_edit.text(),
                  self.ui.sampling_frequency_line_edit.text(), self.ui.passband_edge_line_edit.text(), self.ui.stopband_edge_line_edit.text()]:
            self.showError('Fill in  the design specifications.')
            return

        pbripple = abs(float(self.ui.passband_ripple_line_edit.text()))
        sbrejection = -1*abs(float(self.ui.stopband_rejection_line_edit.text()))
        fs = int(self.ui.sampling_frequency_line_edit.text())
        pbedge = float(self.ui.passband_edge_line_edit.text())
        sbedge = float(self.ui.stopband_edge_line_edit.text())

        pbdelta = (10**(pbripple/20))-1
        sbdelta = (10**(sbrejection/20))
        normalized_bw = (sbedge - pbedge) / fs
        taps = int(estimate_order(pbdelta, sbdelta, normalized_bw)) + 1
        if taps % 2 == 0:
            self.ui.taps_line_edit.setText(str(taps + 1))
        else:
            self.ui.taps_line_edit.setText(str(taps))

    def design_filter(self):
        if '' in [self.ui.taps_line_edit.text(), self.ui.band_edges_line_edit.text(), self.ui.ideal_gain_coefficients_line_edit.text()]:
            self.showError('Fill in the design parameters.')
            return

        # The number of taps is the same as the filter length
        # The order of an FIR filter is filter length minus 1
        # Keep number of taps odd for linear phase

        if self.current_signal is None:
            if not self.ui.sampling_frequency_line_edit.text():
                self.showError('Select a channel or enter a sampling frequency.')
                return
            fs = int(self.fsinput_lineedit.text())
        else:
            fs = int(self.current_signal.fs)
        if self.ui.least_squares_radio.isChecked() or self.ui.parks_mcclellan_radio.isChecked():
            # least squares or parks
            taps = int(self.ui.taps_line_edit.text())
            if taps % 2 is 0:
                self.showError('Number of taps must be odd for a linear-phase filter.')
                return
            bands = np.fromstring(self.ui.band_edges_line_edit.text(), dtype=float, count=-1, sep=" ")
            if bands.size % 2 is not 0:
                self.showError('Band edges are pairs of frequencies and must be even-numbered.')
                return
            if not np.all(np.diff(bands) > 0):
                self.showError('Band edges must be monotically increasing.')
                return
            if not all(i <= fs/2 for i in bands):
                self.showError('Band edges must be less or equal than Nyquist.')
                return
            desired = np.fromstring(self.ui.ideal_gain_coefficients_line_edit.text(), dtype=float, count=-1, sep=" ")
            if (desired.size != bands.size) and self.ui.least_squares_radio.isChecked():
                self.showError('Least squares: there must be as many gain coefficients as there are frequencies in band edges.')
                return
            if (desired.size != int(bands.size/2)) and self.ui.parks_mcclellan_radio.isChecked():
                self.showError('Parks–McClellan: ideal gain sequence must be half the size of bands')
                return
            #weights = np.fromstring(self.ls_weights_lineedit.text(), dtype=float, count=-1, sep=" ")
            if self.ui.least_squares_radio.isChecked():
                self.filter = design_FIR_ls(taps, bands, desired, fs)
            elif self.ui.parks_mcclellan_radio.isChecked():
                self.filter = design_FIR_parks(taps, bands, desired, fs)
            if self.filter.size != 0:
                self.ui.save_to_file_button.setEnabled(True)
                self.ui.preview_output_button.setEnabled(True)
            freq, response = freqz(self.filter)
            if self.ui.parks_mcclellan_radio.isChecked():
                desired_new = []
                for gain in desired:
                    desired_new.append(gain)
                    desired_new.append(gain)
                desired = np.asarray(desired_new, dtype=np.float32)
            self.ui.filter_graphics_view.plot(np.column_stack((bands, desired)), pen='r')
            self.ui.filter_graphics_view.plot(np.column_stack((0.5*fs*freq/np.pi, np.abs(response))), pen='g')
    #
    # def apply_filter_to_test_signal(self):
    #     selected_channel_id = self.channel_combobox.currentData()
    #     if selected_channel_id is None:
    #         self.showError("Select an input channel")
    #         return
    #     self.preview_button.setEnabled(False)
    #     selected_channel_id = self.channel_combobox.currentData()
    #     signal = self.signals_dic.get(selected_channel_id)
    #     filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
    #     self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)))
    #     self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)))
    #     #self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)), "Original signal")
    #     #self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)), "Filtered signal")
    #
    # def apply_list_selected_item_change(self, item):
    #     id_ = item.data(Qt.UserRole)
    #     if item.checkState() == Qt.Checked:
    #         if id_ not in self.checked_channels_list:
    #             self.checked_channels_list.append(id_)
    #     else:
    #         if id_ in self.checked_channels_list:
    #             self.checked_channels_list.remove(id_)
    #     if not self.checked_channels_list:
    #         self.apply_filter_button.setEnabled(False)
    #     else:
    #         if self.filter is not None:
    #             self.apply_filter_button.setEnabled(True)
    #
    # def apply_filter(self):
    #     for id_ in self.checked_channels_list:
    #         signal = self.signals_dic.get(id_)
    #         filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
    #         self.parent.datasets.changeSamplesArray(id_, filtered_samples)
    #         self.parent.console.write("Filter applied to channel " + signal.name)
    #     self.close()
    #
    def showError(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec()









