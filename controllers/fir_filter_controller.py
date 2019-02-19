from views.fir_filter_designer import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
from models.signal import Signal
from scipy.signal import freqz, convolve
from filtersutils import design_FIR_ls, design_FIR_parks, estimate_order
import numpy as np
import pickle
from PyQt5.QtCore import Qt


class FIRFilterDesignerController(QDialog):
    signal_created = pyqtSignal(Signal)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.filter_lookup = ('least_squares', 'parks')
        self.filter = None

        self.init_ui()
        self.init_connections()

    def init_ui(self):
        self.ui.channel_combo_box.setModel(self.model)
        self.ui.channel_list_view.setModel(self.model)

    def init_connections(self):
        self.ui.estimate_taps_button.clicked.connect(self.estimate_taps_button_pressed)
        self.ui.design_filter_button.clicked.connect(self.design_filter)
        self.ui.preview_output_button.clicked.connect(self.apply_filter_to_test_signal)
        # self.ui.apply_filter_button.clicked.connect(self.apply_filter_to_test_signal)

    def estimate_taps_button_pressed(self):
        if '' in [self.ui.passband_edge_line_edit.text(), self.ui.stopband_rejection_line_edit.text(),
                  self.ui.sampling_frequency_line_edit.text(), self.ui.passband_edge_line_edit.text(),
                  self.ui.stopband_edge_line_edit.text()]:
            self.showError('Fill in  the design specifications.')
            return

        pbripple = abs(float(self.ui.passband_edge_line_edit.text()))
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

        filtertype_id = 0 if self.ui.least_squares_radio.isChecked() else 1
        selected_channel_id = self.ui.channel_combo_box.currentData()
        if selected_channel_id is None:
            if not self.ui.sampling_frequency_line_edit.text():
                self.showError('Select a channel or enter a sampling frequency.')
                return
            fs = int(self.ui.sampling_frequency_line_edit.text())
        else:
            # fs = int(self.model.index(selected_channel_id).data(role=Qt.UserRole).fs)
            test = self.model.data(selected_channel_id, role=Qt.UserRole).fs
            print(test)
        if filtertype_id is self.filter_lookup.index('least_squares') or self.filter_lookup.index('parks'):
            # least squares or parks
            print("yes..")
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
            if not all(i <= fs / 2 for i in bands):
                self.showError('Band edges must be less or equal than Nyquist.')
                return
            desired = np.fromstring(self.ui.ideal_gain_coefficients_line_edit.text(), dtype=float, count=-1, sep=" ")
            if (desired.size != bands.size) and filtertype_id is self.filter_lookup.index('least_squares'):
                self.showError(
                    'Least squares: there must be as many gain coefficients as there are frequencies in band edges.')
                return
            gay = desired.size
            tapet = int(bands.size / 2)
            print("lol")
            if (desired.size != int(bands.size / 2)) and filtertype_id is self.filter_lookup.index('parks'):
                self.showError('Parks–McClellan: ideal gain sequence must be half the size of bands')
                return
            # weights = np.fromstring(self.ls_weights_lineedit.text(), dtype=float, count=-1, sep=" ")
            if filtertype_id is self.filter_lookup.index('least_squares'):
                self.filter = design_FIR_ls(taps, bands, desired, fs)
            elif filtertype_id is self.filter_lookup.index('parks'):
                self.filter = design_FIR_parks(taps, bands, desired, fs)
            if self.filter.size != 0:
                self.ui.save_to_file_button.setEnabled(True)
                self.ui.preview_output_button.setEnabled(True)
            freq, response = freqz(self.filter)
            if filtertype_id is self.filter_lookup.index('parks'):
                desired_new = []
                for gain in desired:
                    desired_new.append(gain)
                    desired_new.append(gain)
                desired = np.asarray(desired_new, dtype=np.float32)
            self.ui.filter_graphics_view.plotItem.plot(np.column_stack((bands, desired)), pen='g')
            self.ui.filter_graphics_view.plotItem.plot(np.column_stack((0.5 * fs * freq / np.pi, np.abs(response))), pen='m')

    def apply_filter_to_test_signal(self):
        print('testingss')
        selected_channel_id = self.ui.channel_combo_box.currentIndex()
        if selected_channel_id is None:
            self.showError("Select an input channel")
            return
        self.ui.preview_output_button.setEnabled(False)
        selected_channel_id = self.ui.channel_combo_box.currentIndex()
        print(selected_channel_id)
        signal = self.model.index(selected_channel_id).data(role=Qt.UserRole)
        print(signal)
        filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
        self.ui.signal_filter_graphics_view.plotItem.plot(np.column_stack((signal.time_array, signal.samples_array)))
        self.ui.signal_filter_graphics_view.plotItem.plot(np.column_stack((signal.time_array, filtered_samples)))
        # self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)), "Original signal")
        # self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)), "Filtered signal")


    def apply_filter(self):
        for id_ in self.checked_channels_list:
            signal = self.signals_dic.get(id_)
            filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
            # self.parent.datasets.changeSamplesArray(id_, filtered_samples)
            # self.parent.console.write("Filter applied to channel " + signal.name)
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    fir_filter = FIRFilterDesignerController()

    fir_filter.show()
    sys.exit(app.exec_())