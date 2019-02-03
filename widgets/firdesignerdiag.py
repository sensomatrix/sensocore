from PyQt5.QtWidgets import QDialog, QFrame, QLineEdit, QLabel, \
    QGroupBox, QComboBox, QVBoxLayout, QDialogButtonBox, QFileDialog, QRadioButton, QPushButton, QMessageBox, QGridLayout, QHBoxLayout, QFormLayout, QButtonGroup, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from .Plotter import FilterPlotter, FilteredSignalPlotter
import numpy as np
from filtersutils import design_FIR_ls
from scipy.signal import freqz, convolve
import pickle



class FIRDesignerDialog(QDialog):

    def __init__(self, parent):
        super(FIRDesignerDialog, self).__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.filter_lookup = ('least_squares', 'win_sinc')
        self.create()
        self.signals_dic = self.parent.datasets.getSignalsList()
        self.populate_channels_combobox()

    def create(self):

        #input channel
        self.input_gb = QGroupBox("Input channel")
        self.input_gb.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.channel_label = QLabel("Channel: ")
        self.channel_combobox = QComboBox()
        self.channel_combobox.currentIndexChanged.connect(self.combobox_item_changed)
        self.fs_label = QLabel("fs: ")
        formlayout = QFormLayout()
        formlayout.addRow(self.channel_label, self.channel_combobox)
        formlayout.addRow(self.fs_label)
        self.input_gb.setLayout(formlayout)

        #filter type
        self.filtertype_buttgroup = QButtonGroup()
        self.ls_radio = QRadioButton("Least-squares")
        self.ls_radio.setChecked(True)
        self.filtertype_buttgroup.addButton(self.ls_radio)
        self.filtertype_buttgroup.setId(self.ls_radio, self.filter_lookup.index('least_squares'))
        self.filtertype_gb = QGroupBox("Filter type")
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.ls_radio)
        self.filtertype_gb.setLayout(gridlayout)


        # filter parameters
        self.designspecs_gb = QGroupBox("Design specifications")
        self.designspecs_gb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.taps_label = QLabel("Taps: ")
        self.taps_lineedit = QLineEdit()
        self.bands_label = QLabel("Band edges: ")
        self.bands_lineedit = QLineEdit()
        self.desired_label = QLabel("Gain: ")
        self.desired_lineedit = QLineEdit()
        self.ls_weights_label = QLabel("Weights: ")
        self.ls_weights_lineedit = QLineEdit()
        formlayout = QFormLayout()
        formlayout.addRow(self.taps_label, self.taps_lineedit)
        formlayout.addRow(self.bands_label, self.bands_lineedit)
        formlayout.addRow(self.desired_label, self.desired_lineedit)
        formlayout.addRow(self.ls_weights_label, self.ls_weights_lineedit)
        self.designspecs_gb.setLayout(formlayout)



        #leftside
        layoutleftside = QVBoxLayout()
        layoutleftside.addWidget(self.input_gb)
        layoutleftside.addWidget(self.filtertype_gb)
        layoutleftside.addWidget(self.designspecs_gb)
        spacer = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layoutleftside.addItem(spacer)
        frameLeft = QFrame()
        frameLeft.setLayout(layoutleftside)
        frameLeft.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        #plotting areas
        self.filterplot = FilterPlotter(self)
        self.signalplot = FilteredSignalPlotter(self)
        layoutplots = QVBoxLayout()
        layoutplots.addWidget(self.filterplot)
        layoutplots.addWidget(self.signalplot)
        framePlots = QFrame()
        framePlots.setLayout(layoutplots)
        framePlots.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        #button box
        self.buttonbox = QDialogButtonBox()

        self.designfilter_button = QPushButton("Design filter")
        self.buttonbox.addButton(self.designfilter_button, QDialogButtonBox.ActionRole)
        self.designfilter_button.clicked.connect(self.design_filter)

        self.apply_button = QPushButton("Apply to signal")
        self.buttonbox.addButton(self.apply_button, QDialogButtonBox.ActionRole)
        self.apply_button.clicked.connect(self.apply_filter_to_signal)
        self.apply_button.setEnabled(False)
        self.export_button = QPushButton("Save filter to file")
        self.export_button.setEnabled(False)
        self.buttonbox.addButton(self.export_button, QDialogButtonBox.ActionRole)
        self.export_button.clicked.connect(self.save_filter_to_file)

        #content layout
        contentlayout = QHBoxLayout()
        contentlayout.addWidget(frameLeft)
        contentlayout.addWidget(framePlots)

        #main layout
        #mainlabel = QLabel("      FIR filter designer")
        #line = QFrame()
        #line.setGeometry(QRect(320, 150, 118, 3))
        #line.setFrameShape(QFrame.HLine)
        #line.setFrameShadow(QFrame.Sunken)

        mainlayout = QVBoxLayout()
        #mainlayout.addWidget(mainlabel)
        #mainlayout.addWidget(line)
        mainlayout.addLayout(contentlayout)
        mainlayout.addWidget(self.buttonbox)
        self.setLayout(mainlayout)
        self.setWindowTitle("FIR filter designer")
        self.show()

    def populate_channels_combobox(self):
        for id, signal in self.signals_dic.items():
            self.channel_combobox.addItem(signal.name, signal.id)

    def combobox_item_changed(self):
        selected_channel_id = self.channel_combobox.currentData()
        fs_str = str(int(self.signals_dic.get(selected_channel_id).fs))
        self.fs_label.setText("fs: " + fs_str + " Hz")

    def save_filter_to_file(self):
        savefilepath = QFileDialog.getSaveFileName(self.parent, "Save filter to file")
        if savefilepath[0]:
            self.save_object(self.filter, savefilepath[0])

    def save_object(self, obj, filename):
        with open(filename, 'wb') as outputfile:
            pickle.dump(obj, outputfile, pickle.HIGHEST_PROTOCOL)



    def design_filter(self):
        # The number of taps is the same as the filter length
        # The order of an FIR filter is filter length minus 1
        # Keep number of taps odd for linear phase

        id = self.filtertype_buttgroup.id(self.filtertype_buttgroup.checkedButton())
        selected_channel_id = self.channel_combobox.currentData()
        fs = int(self.signals_dic.get(selected_channel_id).fs)
        if id is self.filter_lookup.index('least_squares'):
            # least squares
            print("yes..")
            taps = int(self.taps_lineedit.text())
            if taps % 2 is 0:
                self.showError('Number of taps must be odd for a linear-phase filter.')
                return
            bands = np.fromstring(self.bands_lineedit.text(), dtype=float, count=-1, sep=" ")
            if bands.size % 2 is not 0:
                self.showError('Band edges are pairs of frequencies and must be even-numbered.')
                return
            if not np.all(np.diff(bands) > 0):
                self.showError('Band edges must be monotically increasing.')
                return
            if not all(i <= fs/2 for i in bands):
                self.showError('Band edges must be less or equal than Nyquist.')
                return
            desired = np.fromstring(self.desired_lineedit.text(), dtype=float, count=-1, sep=" ")
            if desired.size is not bands.size:
                self.showError('There must be as many gain coefficients as there are frequencies in band edges.')
                return
            weights = np.fromstring(self.ls_weights_lineedit.text(), dtype=float, count=-1, sep=" ")
            self.filter = design_FIR_ls(taps, bands, desired, fs)
            if self.filter.size != 0:
                self.export_button.setEnabled(True)
                self.apply_button.setEnabled(True)
            freq, response = freqz(self.filter)
            self.filterplot.plot_data(data=np.column_stack((0.5*fs*freq/np.pi, np.abs(response))))

    def apply_filter_to_signal(self):
        self.apply_button.setEnabled(False)
        selected_channel_id = self.channel_combobox.currentData()
        signal = self.signals_dic.get(selected_channel_id)
        filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
        self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)))
        self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)))
        #self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)), "Original signal")
        #self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)), "Filtered signal")

    def showError(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec()









