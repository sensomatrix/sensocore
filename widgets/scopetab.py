from PyQt5.QtWidgets import QWidget, QGridLayout
from .scope import Scope
from .chrono import Chrono


class ScopeTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.scope = Scope(self)
        gridlayout = QGridLayout()
        self.setLayout(gridlayout)
        gridlayout.addWidget(self.scope.pw, 1, 1)
        self.chrono = Chrono(self)
        # self.spectrum_view = SpectrumView(self)
        gridlayout.addWidget(self.chrono, 2, 1)
        # gridlayout.addWidget(self.spectrum_view, 3,1)
