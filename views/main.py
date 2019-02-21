# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1078, 679)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.main_tab.setObjectName("main_tab")
        self.oscilloscope_tab = QtWidgets.QWidget()
        self.oscilloscope_tab.setObjectName("oscilloscope_tab")
        self.main_tab.addTab(self.oscilloscope_tab, "")
        self.cross_correlation_tab = QtWidgets.QWidget()
        self.cross_correlation_tab.setObjectName("cross_correlation_tab")
        self.main_tab.addTab(self.cross_correlation_tab, "")
        self.horizontalLayout.addWidget(self.main_tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1078, 22))
        self.menubar.setObjectName("menubar")
        self.menuLoad_Data = QtWidgets.QMenu(self.menubar)
        self.menuLoad_Data.setObjectName("menuLoad_Data")
        self.menuSimulate_Data = QtWidgets.QMenu(self.menubar)
        self.menuSimulate_Data.setObjectName("menuSimulate_Data")
        self.menuFiltering = QtWidgets.QMenu(self.menubar)
        self.menuFiltering.setObjectName("menuFiltering")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMaximumSize(QtCore.QSize(173, 524287))
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.channel_listview = QtWidgets.QListView(self.dockWidgetContents)
        self.channel_listview.setObjectName("channel_listview")
        self.verticalLayout.addWidget(self.channel_listview)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setMinimumSize(QtCore.QSize(175, 238))
        self.dockWidget_2.setMaximumSize(QtCore.QSize(185, 524287))
        self.dockWidget_2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsView_3 = PlotWidget(self.dockWidgetContents_2)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.verticalLayout_2.addWidget(self.graphicsView_3)
        self.graphicsView_4 = PlotWidget(self.dockWidgetContents_2)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.verticalLayout_2.addWidget(self.graphicsView_4)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_3.setMinimumSize(QtCore.QSize(149, 188))
        self.dockWidget_3.setMaximumSize(QtCore.QSize(524287, 188))
        self.dockWidget_3.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents_3)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphicsView_2 = PlotWidget(self.tab_2)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout_4.addWidget(self.graphicsView_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_3)
        self.actionEEG_Simulation = QtWidgets.QAction(MainWindow)
        self.actionEEG_Simulation.setObjectName("actionEEG_Simulation")
        self.actionECG_Simulation = QtWidgets.QAction(MainWindow)
        self.actionECG_Simulation.setObjectName("actionECG_Simulation")
        self.actionFIR_Filter_Designer = QtWidgets.QAction(MainWindow)
        self.actionFIR_Filter_Designer.setObjectName("actionFIR_Filter_Designer")
        self.menuSimulate_Data.addAction(self.actionEEG_Simulation)
        self.menuSimulate_Data.addAction(self.actionECG_Simulation)
        self.menuFiltering.addAction(self.actionFIR_Filter_Designer)
        self.menubar.addAction(self.menuLoad_Data.menuAction())
        self.menubar.addAction(self.menuSimulate_Data.menuAction())
        self.menubar.addAction(self.menuFiltering.menuAction())
        self.toolBar.addAction(self.actionECG_Simulation)
        self.toolBar.addAction(self.actionEEG_Simulation)
        self.toolBar.addAction(self.actionFIR_Filter_Designer)

        self.retranslateUi(MainWindow)
        self.main_tab.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_tab.setTabText(self.main_tab.indexOf(self.oscilloscope_tab), _translate("MainWindow", "Oscilloscope"))
        self.main_tab.setTabText(self.main_tab.indexOf(self.cross_correlation_tab), _translate("MainWindow", "Cross Correlation"))
        self.menuLoad_Data.setTitle(_translate("MainWindow", "Load Data"))
        self.menuSimulate_Data.setTitle(_translate("MainWindow", "Simulate Data"))
        self.menuFiltering.setTitle(_translate("MainWindow", "Filtering"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Channels"))
        self.dockWidget_2.setWindowTitle(_translate("MainWindow", "Secondary Plotting"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Output"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Spectrum View"))
        self.actionEEG_Simulation.setText(_translate("MainWindow", "EEG Simulation"))
        self.actionECG_Simulation.setText(_translate("MainWindow", "ECG Simulation"))
        self.actionFIR_Filter_Designer.setText(_translate("MainWindow", "FIR Filter Designer"))

from pyqtgraph import PlotWidget