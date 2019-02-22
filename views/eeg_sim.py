# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/eeg_sim.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(974, 559)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.zoomed_plot = PlotWidget(Dialog)
        self.zoomed_plot.setObjectName("zoomed_plot")
        self.gridLayout.addWidget(self.zoomed_plot, 0, 1, 1, 6)
        self.preview_button = QtWidgets.QPushButton(Dialog)
        self.preview_button.setObjectName("preview_button")
        self.gridLayout.addWidget(self.preview_button, 3, 4, 1, 1)
        self.reset_signal_button = QtWidgets.QPushButton(Dialog)
        self.reset_signal_button.setAutoDefault(False)
        self.reset_signal_button.setObjectName("reset_signal_button")
        self.gridLayout.addWidget(self.reset_signal_button, 3, 6, 1, 1)
        self.create_signal_button = QtWidgets.QPushButton(Dialog)
        self.create_signal_button.setAutoDefault(False)
        self.create_signal_button.setObjectName("create_signal_button")
        self.gridLayout.addWidget(self.create_signal_button, 3, 5, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.c1_label = QtWidgets.QLabel(Dialog)
        self.c1_label.setObjectName("c1_label")
        self.verticalLayout.addWidget(self.c1_label)
        self.c1_spinbox = QtWidgets.QSpinBox(Dialog)
        self.c1_spinbox.setMinimum(50)
        self.c1_spinbox.setMaximum(1500)
        self.c1_spinbox.setProperty("value", 135)
        self.c1_spinbox.setObjectName("c1_spinbox")
        self.verticalLayout.addWidget(self.c1_spinbox)
        self.signal_properties_groupbox = QtWidgets.QGroupBox(Dialog)
        self.signal_properties_groupbox.setObjectName("signal_properties_groupbox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.signal_properties_groupbox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.noise_double_spinbox = QtWidgets.QDoubleSpinBox(self.signal_properties_groupbox)
        self.noise_double_spinbox.setObjectName("noise_double_spinbox")
        self.gridLayout_6.addWidget(self.noise_double_spinbox, 3, 0, 1, 1)
        self.noise_label = QtWidgets.QLabel(self.signal_properties_groupbox)
        self.noise_label.setObjectName("noise_label")
        self.gridLayout_6.addWidget(self.noise_label, 2, 0, 1, 1)
        self.sampling_frequency_label = QtWidgets.QLabel(self.signal_properties_groupbox)
        self.sampling_frequency_label.setObjectName("sampling_frequency_label")
        self.gridLayout_6.addWidget(self.sampling_frequency_label, 4, 0, 1, 1)
        self.signal_name_label = QtWidgets.QLabel(self.signal_properties_groupbox)
        self.signal_name_label.setObjectName("signal_name_label")
        self.gridLayout_6.addWidget(self.signal_name_label, 0, 0, 1, 1)
        self.simulation_line_edit = QtWidgets.QLineEdit(self.signal_properties_groupbox)
        self.simulation_line_edit.setObjectName("simulation_line_edit")
        self.gridLayout_6.addWidget(self.simulation_line_edit, 1, 0, 1, 1)
        self.sampling_frequency_spinbox = QtWidgets.QSpinBox(self.signal_properties_groupbox)
        self.sampling_frequency_spinbox.setMinimum(10)
        self.sampling_frequency_spinbox.setMaximum(1000)
        self.sampling_frequency_spinbox.setSingleStep(1)
        self.sampling_frequency_spinbox.setProperty("value", 100)
        self.sampling_frequency_spinbox.setObjectName("sampling_frequency_spinbox")
        self.gridLayout_6.addWidget(self.sampling_frequency_spinbox, 5, 0, 1, 1)
        self.duration_spinbox = QtWidgets.QDoubleSpinBox(self.signal_properties_groupbox)
        self.duration_spinbox.setMinimum(10.0)
        self.duration_spinbox.setMaximum(1000.0)
        self.duration_spinbox.setObjectName("duration_spinbox")
        self.gridLayout_6.addWidget(self.duration_spinbox, 7, 0, 1, 1)
        self.duration_label = QtWidgets.QLabel(self.signal_properties_groupbox)
        self.duration_label.setObjectName("duration_label")
        self.gridLayout_6.addWidget(self.duration_label, 6, 0, 1, 1)
        self.verticalLayout.addWidget(self.signal_properties_groupbox)
        self.verticalLayout.setStretch(2, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.main_plot = PlotWidget(Dialog)
        self.main_plot.setObjectName("main_plot")
        self.gridLayout.addWidget(self.main_plot, 2, 0, 1, 7)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.preview_button.setText(_translate("Dialog", "Preview Signal"))
        self.reset_signal_button.setText(_translate("Dialog", "Reset Signal"))
        self.create_signal_button.setText(_translate("Dialog", "Create Signal"))
        self.c1_label.setText(_translate("Dialog", "C1"))
        self.signal_properties_groupbox.setTitle(_translate("Dialog", "Signal Properties"))
        self.noise_label.setText(_translate("Dialog", "Noise (Mean Value)"))
        self.sampling_frequency_label.setText(_translate("Dialog", "Sampling Frequency"))
        self.signal_name_label.setText(_translate("Dialog", "Signal Name"))
        self.simulation_line_edit.setPlaceholderText(_translate("Dialog", "Simulation Example"))
        self.duration_label.setText(_translate("Dialog", "Duration (s)"))

from pyqtgraph import PlotWidget
