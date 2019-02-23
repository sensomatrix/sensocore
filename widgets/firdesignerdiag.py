import pyqtgraph as pg
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

    def __init__(self):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = FIRDesignerView()
        self.ui.setupUi(self)
    #
    # def populate_channels_combobox(self):
    #     pass
    #
    # def populate_channels_apply_list(self):
    #     pass
    #
    # def combobox_item_changed(self):
    #     selected_channel_id = self.channel_combobox.currentData()
    #     if selected_channel_id is not None:
    #         fs_str = str(int(self.signals_dic.get(selected_channel_id).fs))
    #         self.fs_label.setText("fs: " + fs_str + " Hz")
    #         self.fsinput_lineedit.setText(fs_str)
    #
    # def save_filter_to_file(self):
    #     savefilepath = QFileDialog.getSaveFileName(self.parent, "Save filter to file")
    #     if savefilepath[0]:
    #         self.save_object(self.filter, savefilepath[0])
    #
    # def save_object(self, obj, filename):
    #     with open(filename, 'wb') as outputfile:
    #         pickle.dump(obj, outputfile, pickle.HIGHEST_PROTOCOL)
    #
    # def estimate_taps_button_pressed(self):
    #     if '' in [self.pbripple_lineedit.text(), self.sbrejection_lineedit.text(),
    #               self.fsinput_lineedit.text(), self.pbedge_lineedit.text(), self.sbedge_lineedit.text()]:
    #         self.showError('Fill in  the design specifications.')
    #         return
    #
    #     pbripple = abs(float(self.pbripple_lineedit.text()))
    #     sbrejection = -1*abs(float(self.sbrejection_lineedit.text()))
    #     fs = int(self.fsinput_lineedit.text())
    #     pbedge = float(self.pbedge_lineedit.text())
    #     sbedge = float(self.sbedge_lineedit.text())
    #
    #     pbdelta = (10**(pbripple/20))-1
    #     sbdelta = (10**(sbrejection/20))
    #     normalized_bw = (sbedge - pbedge) / fs
    #     taps = int(estimate_order(pbdelta, sbdelta, normalized_bw)) + 1
    #     if taps % 2 == 0:
    #         self.taps_lineedit.setText(str(taps + 1))
    #     else:
    #         self.taps_lineedit.setText(str(taps))
    #
    # def design_filter(self):
    #     if '' in [self.taps_lineedit.text(), self.bands_lineedit.text(), self.desired_lineedit.text()]:
    #         self.showError('Fill in the design parameters.')
    #         return
    #
    #
    #     # The number of taps is the same as the filter length
    #     # The order of an FIR filter is filter length minus 1
    #     # Keep number of taps odd for linear phase
    #
    #     filtertype_id = self.filtertype_buttgroup.id(self.filtertype_buttgroup.checkedButton())
    #     selected_channel_id = self.channel_combobox.currentData()
    #     if selected_channel_id is None:
    #         if not self.fsinput_lineedit.text():
    #             self.showError('Select a channel or enter a sampling frequency.')
    #             return
    #         fs = int(self.fsinput_lineedit.text())
    #     else:
    #         fs = int(self.signals_dic.get(selected_channel_id).fs)
    #     if filtertype_id is self.filter_lookup.index('least_squares') or self.filter_lookup.index('parks'):
    #         # least squares or parks
    #         taps = int(self.taps_lineedit.text())
    #         if taps % 2 is 0:
    #             self.showError('Number of taps must be odd for a linear-phase filter.')
    #             return
    #         bands = np.fromstring(self.bands_lineedit.text(), dtype=float, count=-1, sep=" ")
    #         if bands.size % 2 is not 0:
    #             self.showError('Band edges are pairs of frequencies and must be even-numbered.')
    #             return
    #         if not np.all(np.diff(bands) > 0):
    #             self.showError('Band edges must be monotically increasing.')
    #             return
    #         if not all(i <= fs/2 for i in bands):
    #             self.showError('Band edges must be less or equal than Nyquist.')
    #             return
    #         desired = np.fromstring(self.desired_lineedit.text(), dtype=float, count=-1, sep=" ")
    #         if (desired.size != bands.size) and filtertype_id is self.filter_lookup.index('least_squares'):
    #             self.showError('Least squares: there must be as many gain coefficients as there are frequencies in band edges.')
    #             return
    #         if (desired.size != int(bands.size/2)) and filtertype_id is self.filter_lookup.index('parks'):
    #             self.showError('Parks–McClellan: ideal gain sequence must be half the size of bands')
    #             return
    #         #weights = np.fromstring(self.ls_weights_lineedit.text(), dtype=float, count=-1, sep=" ")
    #         if filtertype_id is self.filter_lookup.index('least_squares'):
    #             self.filter = design_FIR_ls(taps, bands, desired, fs)
    #         elif filtertype_id is self.filter_lookup.index('parks'):
    #             self.filter = design_FIR_parks(taps, bands, desired, fs)
    #         if self.filter.size != 0:
    #             self.export_button.setEnabled(True)
    #             self.preview_button.setEnabled(True)
    #         freq, response = freqz(self.filter)
    #         if filtertype_id is self.filter_lookup.index('parks'):
    #             desired_new = []
    #             for gain in desired:
    #                 desired_new.append(gain)
    #                 desired_new.append(gain)
    #             desired = np.asarray(desired_new, dtype=np.float32)
    #         self.filterplot.plot_data(np.column_stack((bands, desired)))
    #         self.filterplot.plot_data(np.column_stack((0.5*fs*freq/np.pi, np.abs(response))))
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
    # def showError(self, message):
    #     error_dialog = QMessageBox(self)
    #     error_dialog.setWindowModality(Qt.WindowModal)
    #     error_dialog.setIcon(QMessageBox.Critical)
    #     error_dialog.setText(message)
    #     error_dialog.exec()









