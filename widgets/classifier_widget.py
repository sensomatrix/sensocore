import pyqtgraph as pg
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/classification.ui')
ClassificationView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class ClassificationWidget(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = ClassificationView()
        self.ui.setupUi(self)