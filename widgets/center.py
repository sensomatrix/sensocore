from PyQt5.QtWidgets import QTabWidget, QTabBar
from .scopetab import ScopeTab
from widgets.cross_correlation_tab import CrossCorrelationTab
from .errormessages import ErrorMessage

class Center(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabs = QTabWidget
        self.tabCloseRequested.connect(self.remove_and_delete_tab)
        self.tabScope = ScopeTab(self)
        self.setTabsClosable(True)
        self.addTab(self.tabScope,"Oscilloscope")
        self.hideCloseButton(self.tabScope)

    def hideCloseButton(self, tab):
        if self.tabBar().tabButton(0, QTabBar.RightSide) is None:
            self.tabBar().tabButton(0, QTabBar.LeftSide).resize(0, 0)
            return
        self.tabBar().tabButton(0, QTabBar.RightSide).resize(0, 0)

    def user_clicks_on_correlate_button(self, signals, selected_channels_list_by_id):
        if len(selected_channels_list_by_id) == 2:
            signal_1 = signals.get(selected_channels_list_by_id[0])
            signal_2 = signals.get(selected_channels_list_by_id[1])
            self.tabCrossCorre = CrossCorrelationTab(self)
            self.tabCrossCorre.computeCrossCor(signal_1, signal_2)
            index = self.addTab(self.tabCrossCorre,"CROSSCOR("+signal_1.name+","+signal_2.name+")")
            self.setCurrentIndex(index)
        else:
            ErrorMessage("Select two channels.")

    def remove_and_delete_tab(self, index):
        self.widget(index).deleteLater()
        self.removeTab(index)



