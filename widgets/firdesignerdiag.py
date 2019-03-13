import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QModelIndex
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
        self.apply_filter_to_signal = None

        self.ui.apply_filter_list_view.setModel(self.signals)
        self.ui.channel_combo_box.setModel(self.signals)

        self.ui.channel_combo_box.currentIndexChanged.connect(self.item_changed)
        self.ui.signal_specific_filter_combo_box.currentIndexChanged.connect(self.update_filter_options)

        self.filter = None

        self.ui.apply_filter_list_view.clicked[QModelIndex].connect(self.apply_list_selected_item_change)

        self.ui.sampling_frequency_line_edit.textChanged.connect(self.change_desired_band_edges_text)
        self.ui.passband_edge_line_edit.textChanged.connect(self.change_desired_band_edges_text)
        self.ui.stopband_edge_line_edit.textChanged.connect(self.change_desired_band_edges_text)

        self.item_changed(0)

        self.ui.save_to_file_button.clicked.connect(self.save_filter_to_file)
        self.ui.estimate_taps_button.clicked.connect(self.estimate_taps_button_pressed)
        self.ui.design_filter_button.clicked.connect(self.design_filter)
        self.ui.preview_output_button.clicked.connect(self.apply_filter_to_test_signal)
        self.ui.apply_filter_button.clicked.connect(self.apply_filter)

    def change_desired_band_edges_text(self):
        self.ui.band_edges_line_edit.setText('{0} {1} {2} {3}'.format(0, self.ui.passband_edge_line_edit.text(),
                                                                      self.ui.stopband_edge_line_edit.text(),
                                                                      self.ui.sampling_frequency_line_edit.text()))

    def item_changed(self, index):
        self.current_signal = self.ui.channel_combo_box.itemData(index)
        self.ui.sampling_frequency_label.setText('fs: ' + str(self.current_signal.fs) + 'Hz')
        self.ui.sampling_frequency_line_edit.setText(str(int(self.current_signal.fs / 2)))

        self.ui.signal_specific_filter_combo_box.clear()

        if self.current_signal.type == 'EEG':
            self.ui.signal_specific_filter_combo_box.addItem('Custom Filter')
            self.ui.signal_specific_filter_combo_box.addItem('Alpha Filter', ['8', '13'])
            self.ui.signal_specific_filter_combo_box.addItem('Beta Filter', ['4', '7'])

    def update_filter_options(self, index):
        data = self.ui.signal_specific_filter_combo_box.itemData(index)
        if data is not None:
            self.ui.passband_edge_line_edit.setText(data[0])
            self.ui.stopband_edge_line_edit.setText(data[1])
            self.ui.estimate_taps_button.animateClick()

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

            self.ui.filter_graphics_view.clear()
            self.ui.filter_graphics_view.addLegend()
            self.ui.filter_graphics_view.plot(np.column_stack((bands, desired)), pen='r', name='Ideal Filter')
            self.ui.filter_graphics_view.plot(np.column_stack((0.5*fs*freq/np.pi, np.abs(response))), pen='g', name='Actual Filter')

    def apply_filter_to_test_signal(self):
        if self.current_signal is None:
            self.showError("Select an input channel")
            return
        self.ui.preview_output_button.setEnabled(False)
        filtered_samples = convolve(self.current_signal.raw, self.filter, mode='same')

        self.ui.signal_filter_graphics_view.clear()
        self.ui.signal_filter_graphics_view.addLegend()
        self.ui.signal_filter_graphics_view.plot(np.column_stack((self.current_signal.time_array,
                                                                  self.current_signal.raw)), pen='r', name='Raw Signal')
        self.ui.signal_filter_graphics_view.plot(np.column_stack((self.current_signal.time_array,
                                                                  filtered_samples)), pen='g', name='Filtered Signal')

    def apply_list_selected_item_change(self, index):
        self.apply_filter_to_signal = self.signals.get_signal(index)

        if not self.ui.apply_filter_list_view:
            self.ui.apply_filter_button.setEnabled(False)
        elif self.filter is not None:
            self.ui.apply_filter_button.setEnabled(True)

    def apply_filter(self):
        self.apply_filter_to_signal.filtered = convolve(self.current_signal.raw, self.filter, mode='same')
        self.signals.plot_filtered_signal(self.apply_filter_to_signal)
        self.close()

    def showError(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec()









