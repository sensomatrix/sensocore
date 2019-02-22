# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/cross_correlation.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(694, 469)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.signal_1_plot = PlotWidget(Form)
        self.signal_1_plot.setObjectName("signal_1_plot")
        self.verticalLayout.addWidget(self.signal_1_plot)
        self.signal_2_plot = PlotWidget(Form)
        self.signal_2_plot.setObjectName("signal_2_plot")
        self.verticalLayout.addWidget(self.signal_2_plot)
        self.cross_correlatoion_plot = PlotWidget(Form)
        self.cross_correlatoion_plot.setObjectName("cross_correlatoion_plot")
        self.verticalLayout.addWidget(self.cross_correlatoion_plot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

from pyqtgraph import PlotWidget
