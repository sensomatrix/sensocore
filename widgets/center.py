from PyQt5.QtWidgets import QTabWidget, QTabBar
from .scopetab import ScopeTab

class Center(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabScope = ScopeTab(self)
        self.setTabsClosable(True)
        self.addTab(self.tabScope,"Oscilloscope")
        self.hideCloseButton(self.tabScope)

    def hideCloseButton(self, tab):
        if self.tabBar().tabButton(0, QTabBar.RightSide) is None:
            self.tabBar().tabButton(0, QTabBar.LeftSide).resize(0, 0)
            return
        self.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)

