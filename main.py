import sys
from dataset import Dataset
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from types import MethodType
from widgets.initui import init_ui_widgets, init_ui_toolbar


class MainWindow(QMainWindow):
    print("Test")

    def __init__(self):
        super().__init__()
        self.channels = None
        self.scope = None
        self.chrono = None
        self.console = None
        self.datainfo = None
        self.datasets = Dataset(self)
        self.init_ui_widgets = MethodType(init_ui_widgets, self)
        self.init_ui_toolbar = MethodType(init_ui_toolbar, self)
        self.init_ui_widgets()
        self.init_ui_toolbar()


if __name__ == "__main__":
    global app
    app = QApplication([])
    q = MainWindow()
    q.showMaximized()
    sys.exit(app.exec_())
