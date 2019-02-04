from PyQt5.QtWidgets import QDialog, QFrame, QLineEdit, QLabel, \
    QGroupBox, QComboBox, QVBoxLayout, QDialogButtonBox, QFileDialog, QListView, QRadioButton, \
    QPushButton, QMessageBox, QGridLayout, QHBoxLayout, QFormLayout, QButtonGroup, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from .Plotter import FilterPlotter, FilteredSignalPlotter
import numpy as np
from filtersutils import design_FIR_ls, design_FIR_parks, estimate_order
from scipy.signal import freqz, convolve
import pickle



class FIRDesignerDialog(QDialog):

    def __init__(self, parent):
        super(FIRDesignerDialog, self).__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.filter_lookup = ('least_squares', 'parks')
        self.filter = None
        self.create()
        self.signals_dic = self.parent.datasets.getSignalsList()
        self.populate_channels_combobox()
        self.populate_channels_apply_list()
        self.checked_channels_list = []
        self.setFixedSize(self.size())

    def create(self):

        #input channel
        self.input_gb = QGroupBox("1. Input channel")
        self.input_gb.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.channel_label = QLabel("Channel: ")
        self.channel_combobox = QComboBox()
        self.channel_combobox.currentIndexChanged.connect(self.combobox_item_changed)
        self.fs_label = QLabel("fs: ")
        formlayout = QFormLayout()
        formlayout.addRow(self.channel_label, self.channel_combobox)
        formlayout.addRow(self.fs_label)
        self.input_gb.setLayout(formlayout)


        # design specs
        self.designspecs_gb = QGroupBox("2. Design specifications")
        self.designspecs_gb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pbripple_label = QLabel("Passband ripple (dB): ±")
        self.pbripple_lineedit = QLineEdit()
        self.sbrejection_label = QLabel("Stopband rejection (dB): -")
        self.sbrejection_lineedit = QLineEdit()
        self.fsinput_label = QLabel("Sampling frequency (Hz):")
        self.fsinput_lineedit = QLineEdit()
        self.pbedge_label = QLabel("Passband edge (Hz):")
        self.pbedge_lineedit = QLineEdit()
        self.sbedge_label = QLabel("Stopband edge (Hz):")
        self.sbedge_lineedit = QLineEdit()
        self.estimate_taps_button = QPushButton('Estimate taps', self)
        self.estimate_taps_button.clicked.connect(self.estimate_taps_button_pressed)
        formlayout = QFormLayout()
        formlayout.addRow(self.pbripple_label, self.pbripple_lineedit)
        formlayout.addRow(self.sbrejection_label, self.sbrejection_lineedit)
        formlayout.addRow(self.fsinput_label, self.fsinput_lineedit)
        formlayout.addRow(self.pbedge_label, self.pbedge_lineedit)
        formlayout.addRow(self.sbedge_label, self.sbedge_lineedit)
        self.designspecs_gb.setLayout(formlayout)

        # filter type
        self.filtertype_buttgroup = QButtonGroup()
        self.ls_radio = QRadioButton("Least-squares")
        self.ls_radio.setChecked(True)
        self.filtertype_buttgroup.addButton(self.ls_radio)
        self.filtertype_buttgroup.setId(self.ls_radio, self.filter_lookup.index('least_squares'))
        self.parks_radio = QRadioButton("Parks-McClellan")
        self.parks_radio.setChecked(False)
        self.filtertype_buttgroup.addButton(self.parks_radio)
        self.filtertype_buttgroup.setId(self.parks_radio, self.filter_lookup.index('parks'))

        self.filtertype_gb = QGroupBox("3. Filter realization")
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.ls_radio, 0, 0)
        gridlayout.addWidget(self.parks_radio, 0, 1)
        self.filtertype_gb.setLayout(gridlayout)


        # filter parameters
        self.designparam_gb = QGroupBox("4. Design parameters")
        self.designparam_gb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.taps_label = QLabel("Taps: ")
        self.taps_lineedit = QLineEdit()
        self.bands_label = QLabel("Band edges: ")
        self.bands_lineedit = QLineEdit()
        self.desired_label = QLabel("Ideal gain coefficients: ")
        self.desired_lineedit = QLineEdit()
        #self.ls_weights_label = QLabel("Weights: ")
        #self.ls_weights_lineedit = QLineEdit()
        formlayout = QFormLayout()
        formlayout.addRow(self.taps_label, self.taps_lineedit)
        formlayout.addRow(self.bands_label, self.bands_lineedit)
        formlayout.addRow(self.desired_label, self.desired_lineedit)
        #formlayout.addRow(self.ls_weights_label, self.ls_weights_lineedit)
        self.designparam_gb.setLayout(formlayout)

        # channel list apply filters
        self.applyfilters_gb = QGroupBox("5. Apply filter")
        self.applyfilters_list = QListView()
        self.applyfilters_list.setEnabled(False)
        self.applyfilters_itemomodel = QStandardItemModel()
        self.applyfilters_itemomodel.itemChanged.connect(self.apply_list_selected_item_change)
        self.applyfilters_list.setModel(self.applyfilters_itemomodel)
        layout = QVBoxLayout()
        layout.addWidget(self.applyfilters_list)
        self.applyfilters_gb.setLayout(layout)



        #leftside
        layoutleftside = QVBoxLayout()
        layoutleftside.addWidget(self.input_gb)
        layoutleftside.addWidget(self.designspecs_gb)
        layoutleftside.addWidget(self.estimate_taps_button)
        layoutleftside.addWidget(self.filtertype_gb)
        layoutleftside.addWidget(self.designparam_gb)
        layoutleftside.addWidget(self.applyfilters_gb)
        spacer = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layoutleftside.addItem(spacer)
        frameLeft = QFrame()
        frameLeft.setLayout(layoutleftside)
        #frameLeft.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        #plotting areas
        self.filterplot = FilterPlotter(self)
        self.signalplot = FilteredSignalPlotter(self)
        layoutplots = QVBoxLayout()
        layoutplots.addWidget(self.filterplot)
        layoutplots.addWidget(self.signalplot)
        framePlots = QFrame()
        framePlots.setLayout(layoutplots)
        #framePlots.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        #button box
        self.buttonbox = QDialogButtonBox()
        self.designfilter_button = QPushButton("Design filter")
        self.buttonbox.addButton(self.designfilter_button, QDialogButtonBox.ActionRole)
        self.designfilter_button.clicked.connect(self.design_filter)
        self.preview_button = QPushButton("Preview output")
        self.buttonbox.addButton(self.preview_button, QDialogButtonBox.ActionRole)
        self.preview_button.clicked.connect(self.apply_filter_to_test_signal)
        self.preview_button.setEnabled(False)
        self.export_button = QPushButton("Save filter to file")
        self.export_button.setEnabled(False)
        self.buttonbox.addButton(self.export_button, QDialogButtonBox.ActionRole)
        self.export_button.clicked.connect(self.save_filter_to_file)
        self.apply_filter_button = QPushButton("Apply filter")
        self.apply_filter_button.setEnabled(False)
        self.buttonbox.addButton(self.apply_filter_button, QDialogButtonBox.ActionRole)
        self.apply_filter_button.clicked.connect(self.apply_filter)



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
        for id_, signal in self.signals_dic.items():
            self.channel_combobox.addItem(signal.name, signal.id)
        if self.signals_dic:
            self.applyfilters_list.setEnabled(True)

    def populate_channels_apply_list(self):
        for id_, signal in self.signals_dic.items():
            item = QStandardItem(signal.name + " (" + str(int(signal.fs)) + " Hz)")
            item.setCheckable(True)
            item.setEditable(False)
            item.setCheckState(Qt.Unchecked)
            item.setData(id_, Qt.UserRole)
            self.applyfilters_itemomodel.appendRow(item)

    def combobox_item_changed(self):
        selected_channel_id = self.channel_combobox.currentData()
        if selected_channel_id is not None:
            fs_str = str(int(self.signals_dic.get(selected_channel_id).fs))
            self.fs_label.setText("fs: " + fs_str + " Hz")
            self.fsinput_lineedit.setText(fs_str)

    def save_filter_to_file(self):
        savefilepath = QFileDialog.getSaveFileName(self.parent, "Save filter to file")
        if savefilepath[0]:
            self.save_object(self.filter, savefilepath[0])

    def save_object(self, obj, filename):
        with open(filename, 'wb') as outputfile:
            pickle.dump(obj, outputfile, pickle.HIGHEST_PROTOCOL)

    def estimate_taps_button_pressed(self):
        if '' in [self.pbripple_lineedit.text(), self.sbrejection_lineedit.text(),
                  self.fsinput_lineedit.text(), self.pbedge_lineedit.text(), self.sbedge_lineedit.text()]:
            self.showError('Fill in  the design specifications.')
            return

        pbripple = abs(float(self.pbripple_lineedit.text()))
        sbrejection = -1*abs(float(self.sbrejection_lineedit.text()))
        fs = int(self.fsinput_lineedit.text())
        pbedge = float(self.pbedge_lineedit.text())
        sbedge = float(self.sbedge_lineedit.text())

        pbdelta = (10**(pbripple/20))-1
        sbdelta = (10**(sbrejection/20))
        normalized_bw = (sbedge - pbedge) / fs
        taps = int(estimate_order(pbdelta, sbdelta, normalized_bw)) + 1
        if taps % 2 == 0:
            self.taps_lineedit.setText(str(taps + 1))
        else:
            self.taps_lineedit.setText(str(taps))

    def design_filter(self):
        if '' in [self.taps_lineedit.text(), self.bands_lineedit.text(), self.desired_lineedit.text()]:
            self.showError('Fill in the design parameters.')
            return


        # The number of taps is the same as the filter length
        # The order of an FIR filter is filter length minus 1
        # Keep number of taps odd for linear phase

        filtertype_id = self.filtertype_buttgroup.id(self.filtertype_buttgroup.checkedButton())
        selected_channel_id = self.channel_combobox.currentData()
        if selected_channel_id is None:
            if not self.fsinput_lineedit.text():
                self.showError('Select a channel or enter a sampling frequency.')
                return
            fs = int(self.fsinput_lineedit.text())
        else:
            fs = int(self.signals_dic.get(selected_channel_id).fs)
        if filtertype_id is self.filter_lookup.index('least_squares') or self.filter_lookup.index('parks'):
            # least squares or parks
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
            if (desired.size != bands.size) and filtertype_id is self.filter_lookup.index('least_squares'):
                self.showError('Least squares: there must be as many gain coefficients as there are frequencies in band edges.')
                return
            gay = desired.size
            tapet = int(bands.size/2)
            print("lol")
            if (desired.size != int(bands.size/2)) and filtertype_id is self.filter_lookup.index('parks'):
                self.showError('Parks–McClellan: ideal gain sequence must be half the size of bands')
                return
            #weights = np.fromstring(self.ls_weights_lineedit.text(), dtype=float, count=-1, sep=" ")
            if filtertype_id is self.filter_lookup.index('least_squares'):
                self.filter = design_FIR_ls(taps, bands, desired, fs)
            elif filtertype_id is self.filter_lookup.index('parks'):
                self.filter = design_FIR_parks(taps, bands, desired, fs)
            if self.filter.size != 0:
                self.export_button.setEnabled(True)
                self.preview_button.setEnabled(True)
            freq, response = freqz(self.filter)
            if filtertype_id is self.filter_lookup.index('parks'):
                desired_new = []
                for gain in desired:
                    desired_new.append(gain)
                    desired_new.append(gain)
                desired = np.asarray(desired_new, dtype=np.float32)
            self.filterplot.plot_data(np.column_stack((bands, desired)))
            self.filterplot.plot_data(np.column_stack((0.5*fs*freq/np.pi, np.abs(response))))

    def apply_filter_to_test_signal(self):
        selected_channel_id = self.channel_combobox.currentData()
        if selected_channel_id is None:
            self.showError("Select an input channel")
            return
        self.preview_button.setEnabled(False)
        selected_channel_id = self.channel_combobox.currentData()
        signal = self.signals_dic.get(selected_channel_id)
        filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
        self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)))
        self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)))
        #self.signalplot.plot_data(np.column_stack((signal.time_array, signal.samples_array)), "Original signal")
        #self.signalplot.plot_data(np.column_stack((signal.time_array, filtered_samples)), "Filtered signal")

    def apply_list_selected_item_change(self, item):
        id_ = item.data(Qt.UserRole)
        if item.checkState() == Qt.Checked:
            if id_ not in self.checked_channels_list:
                self.checked_channels_list.append(id_)
        else:
            if id_ in self.checked_channels_list:
                self.checked_channels_list.remove(id_)
        if not self.checked_channels_list:
            self.apply_filter_button.setEnabled(False)
        else:
            if self.filter is not None:
                self.apply_filter_button.setEnabled(True)

    def apply_filter(self):
        for id_ in self.checked_channels_list:
            signal = self.signals_dic.get(id_)
            filtered_samples = convolve(signal.samples_array, self.filter, mode='same')
            self.parent.datasets.changeSamplesArray(id_, filtered_samples)
            self.parent.console.write("Filter applied to channel " + signal.name)
        self.close()

    def showError(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowModality(Qt.WindowModal)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.exec()









