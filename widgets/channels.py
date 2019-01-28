from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

#implement a channel list and maybe some buttons for doing actions on select channels
class Channels(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabs = None
        self.create()


    def create(self):
        print("nothing for now")