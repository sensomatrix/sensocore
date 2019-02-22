from views.cross_correlation import Ui_Form
from PyQt5.QtWidgets import QWidget
from itertools import cycle


class CrossCorrelation(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)