from PyQt5.QtWidgets import QWidget, QGridLayout
from .scope import Scope
from .chrono import Chrono
class Center(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.scope = Scope(self)
        gridlayout = QGridLayout()
        self.setLayout(gridlayout)
        gridlayout.addWidget(self.scope.pw, 1, 1)
        self.chrono = Chrono(self)
        gridlayout.addWidget(self.chrono, 2,1)
