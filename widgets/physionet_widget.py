import pyqtgraph as pg
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/physionet.ui')
PhysioNetView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class PhysioNetWidget(TemplateBaseClass):
    def __init__(self, parent):
        TemplateBaseClass.__init__(self, parent=parent)

        # Create the main window
        self.ui = PhysioNetView()
        self.ui.setupUi(self)