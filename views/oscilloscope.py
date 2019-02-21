# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/oscilloscope.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(675, 445)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.label_y = QtWidgets.QLabel(Form)
        self.label_y.setObjectName("label_y")
        self.gridLayout_2.addWidget(self.label_y, 2, 3, 1, 1)
        self.label_x = QtWidgets.QLabel(Form)
        self.label_x.setObjectName("label_x")
        self.gridLayout_2.addWidget(self.label_x, 2, 2, 1, 1)
        self.cursor_label = QtWidgets.QLabel(Form)
        self.cursor_label.setObjectName("cursor_label")
        self.gridLayout_2.addWidget(self.cursor_label, 2, 0, 1, 1)
        self.multiplot_widget = MultiPlotWidget(Form)
        self.multiplot_widget.setObjectName("multiplot_widget")
        self.gridLayout_2.addWidget(self.multiplot_widget, 0, 0, 1, 4)
        self.horizontal_slider = QtWidgets.QSlider(Form)
        self.horizontal_slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_slider.setObjectName("horizontal_slider")
        self.gridLayout_2.addWidget(self.horizontal_slider, 4, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_y.setText(_translate("Form", "Y:"))
        self.label_x.setText(_translate("Form", "X:"))
        self.cursor_label.setText(_translate("Form", "Time: "))

from pyqtgraph import MultiPlotWidget
