from PyQt5.QtWidgets import QTabWidget, QTabBar
from .scopetab import ScopeTab
from widgets.cross_correlation_tab import CrossCorrelationTab

class Center(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.tabs = QTabWidget
        self.tabScope = ScopeTab(self)
        self.tabCrossCorre = CrossCorrelationTab(self)
        self.setTabsClosable(True)
        self.addTab(self.tabScope,"Oscilloscope")
        self.addTab(self.tabCrossCorre, "Cross Correlation")
        self.hideCloseButton(self.tabScope)

    def hideCloseButton(self, tab):
        if self.tabBar().tabButton(0, QTabBar.RightSide) is None:
            self.tabBar().tabButton(0, QTabBar.LeftSide).resize(0, 0)
            return
        self.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)

