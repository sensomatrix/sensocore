from PyQt5.QtWidgets import QTabWidget, QTabBar
from .scopetab import ScopeTab
from widgets.cross_correlation_tab import CrossCorrelationTab

class Center(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabs = QTabWidget
        self.tabCloseRequested.connect(self.remove_and_delete_tab)
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

    def remove_and_delete_tab(self, index):
        self.widget(index).deleteLater()
        self.removeTab(index)

