import pyqtgraph as pg
import os


path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, '../ui/ecg_summary.ui')
ECGSummaryView, TemplateBaseClass = pg.Qt.loadUiType(uiFile)


class ECGSummaryWidget(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)

        # Create the main window
        self.ui = ECGSummaryView()
        self.ui.setupUi(self)
        self.show()
